#!/usr/bin/env python3
"""No-write external source scout for topic discovery and claim validation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_content_index, load_json, write_json
from automation.proposal_renderer import md_list


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_REGISTRY = ROOT / "automation" / "memory" / "source_registry.json"
READY_ACTIONS = {"update_existing", "create_new", "consolidate"}
SOURCE_STATUSES = {"approved", "proposed", "blocked"}
TRUST_LEVELS = {"high", "medium", "low"}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "topic"


def page_by_filename() -> dict[str, Any]:
    return {page.filename: page for page in load_content_index()}


def validate_registry(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != 1:
        errors.append(f"Unsupported source registry schema_version `{payload.get('schema_version')}`; expected `1`.")
    if not isinstance(payload.get("policy"), dict):
        errors.append("Source registry `policy` must be an object.")
    sources = payload.get("sources")
    if not isinstance(sources, list):
        errors.append("Source registry `sources` must be a list.")
        return errors
    ids: set[str] = set()
    for index, source in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{label} must be an object.")
            continue
        source_id = str(source.get("id", "")).strip()
        if not source_id:
            errors.append(f"{label}.id is required.")
        elif source_id in ids:
            errors.append(f"Duplicate source id `{source_id}`.")
        ids.add(source_id)
        status = str(source.get("status", "")).strip().lower()
        if status not in SOURCE_STATUSES:
            errors.append(f"{label}.status must be one of: {', '.join(sorted(SOURCE_STATUSES))}.")
        trust = str(source.get("trust_level", "")).strip().lower()
        if trust not in TRUST_LEVELS:
            errors.append(f"{label}.trust_level must be one of: {', '.join(sorted(TRUST_LEVELS))}.")
        if not str(source.get("base_url", "")).startswith("https://"):
            errors.append(f"{label}.base_url must be an https URL.")
        for key in ["allowed_uses", "disallowed_uses", "discovery_queries", "topic_seeds"]:
            if not isinstance(source.get(key, []), list):
                errors.append(f"{label}.{key} must be a list.")
    return errors


def normalize_seed(seed: dict[str, Any], source: dict[str, Any], content_pages: dict[str, Any]) -> dict[str, Any]:
    source_id = str(source.get("id", "external-source"))
    raw_topic_id = str(seed.get("topic_id") or seed.get("title") or source_id)
    topic_id = f"external-{slugify(raw_topic_id)}"
    target = str(seed.get("target_page_or_slug", "")).strip()
    page = content_pages.get(target)
    cluster = str(seed.get("cluster") or getattr(page, "cluster", "") or "Site")
    action = str(seed.get("recommended_action") or ("update_existing" if target else "monitor")).strip().lower()
    if action not in READY_ACTIONS | {"monitor", "reject"}:
        action = "monitor"
    source_urls = [
        str(url)
        for url in seed.get("source_urls", [])
        if isinstance(url, str) and url.startswith("https://")
    ]
    evidence = [str(item) for item in seed.get("evidence", []) if str(item).strip()]
    if source_urls:
        evidence.append("External source URL recorded for later manual verification.")
    trust = str(source.get("trust_level", "low")).lower()
    confidence = str(seed.get("confidence") or ("medium" if trust in {"high", "medium"} else "low")).lower()
    if confidence not in {"high", "medium", "low"}:
        confidence = "low"
    priority = str(seed.get("priority") or "medium").lower()
    if priority not in {"high", "medium", "low"}:
        priority = "medium"
    risk = str(seed.get("risk_level") or "high").lower()
    if risk not in {"high", "medium", "low"}:
        risk = "high"
    claims_to_verify = [str(item) for item in seed.get("claims_to_verify", []) if str(item).strip()]
    if action in READY_ACTIONS and not claims_to_verify:
        claims_to_verify = ["external_source_claims"]
    return {
        "topic_id": topic_id,
        "title": str(seed.get("title") or f"External source opportunity: {raw_topic_id}"),
        "cluster": cluster,
        "recommended_action": action,
        "archetype_suggestion": str(seed.get("archetype_suggestion") or getattr(page, "archetype", "") or "support-guide"),
        "target_page_or_slug": target,
        "source_type": "external",
        "source_reference": f"{source_id}: {source.get('base_url', '')}",
        "source_id": source_id,
        "source_name": source.get("name", ""),
        "source_urls": source_urls,
        "confidence": confidence,
        "priority": priority,
        "risk_level": risk,
        "status": "candidate" if action in READY_ACTIONS else "monitor",
        "notes": str(seed.get("notes") or "External source signal; no public copy approved."),
        "evidence": evidence[:8],
        "site_fit": {
            "primary_user_job": str(seed.get("primary_user_job") or ""),
            "cluster_owner": cluster,
            "expected_internal_route": [page for page in ["index.html", target] if page],
            "archetype_reason": str(seed.get("archetype_reason") or "External source indicates a possible player job to validate."),
        },
        "constraints": [
            "Do not copy competitor wording.",
            "Use this as topic discovery and cross-validation context only.",
            "Verify public claims against canonical site memory and at least one additional reliable source or owner confirmation.",
        ],
        "reject_if": [
            "The topic duplicates an existing page intent without adding a distinct player job.",
            "The external claim cannot be verified beyond this source.",
            "The proposal would blur existing cluster roles.",
        ],
        "claims_to_verify": claims_to_verify[:8],
        "cross_validation_status": str(seed.get("cross_validation_status") or "needs_second_source"),
        "copying_risk": "high if the future draft follows source wording; use only the player job and independently verified facts.",
    }


def candidate_sources(payload: dict[str, Any], include_proposed: bool) -> list[dict[str, Any]]:
    allowed = {"approved"}
    if include_proposed:
        allowed.add("proposed")
    return [
        source
        for source in payload.get("sources", [])
        if str(source.get("status", "")).lower() in allowed
    ]


def build_external_scout(
    registry_path: Path,
    output_dir: Path,
    basename: str,
    include_proposed: bool,
    limit: int,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    registry = load_json(registry_path)
    errors = validate_registry(registry)
    if errors:
        payload = {
            "schema_version": 1,
            "report_type": "external_scout",
            "generated_at": now_utc(),
            "state": "blocked",
            "registry_path": rel(registry_path),
            "candidate_proposals": [],
            "source_review_queue": [],
            "errors": errors,
            "output_path": rel(json_path),
            "markdown_path": rel(markdown_path),
            "allows_content_edit": False,
            "allows_backlog_mutation": False,
            "allows_manifest_mutation": False,
            "allows_pr_or_deploy": False,
            "safety": "No content, backlog, manifest, PR, or production files were modified by External Scout.",
        }
        write_external_scout(payload)
        return 1, payload

    content_pages = page_by_filename()
    sources = candidate_sources(registry, include_proposed)
    proposed_sources = [
        {
            "source_id": source.get("id", ""),
            "name": source.get("name", ""),
            "base_url": source.get("base_url", ""),
            "trust_level": source.get("trust_level", ""),
            "notes": source.get("notes", ""),
        }
        for source in registry.get("sources", [])
        if str(source.get("status", "")).lower() == "proposed"
    ]
    proposals: list[dict[str, Any]] = []
    for source in sources:
        for seed in source.get("topic_seeds", []):
            if not isinstance(seed, dict):
                continue
            proposals.append(normalize_seed(seed, source, content_pages))
    proposals.sort(
        key=lambda item: (
            {"high": 0, "medium": 1, "low": 2}.get(str(item.get("priority")), 3),
            {"high": 0, "medium": 1, "low": 2}.get(str(item.get("confidence")), 3),
            str(item.get("topic_id", "")),
        )
    )
    proposals = proposals[: max(0, limit)]
    state = "external_scout_ready"
    if not proposals and proposed_sources and not include_proposed:
        state = "source_approval_needed"
    payload = {
        "schema_version": 1,
        "report_type": "external_scout",
        "generated_at": now_utc(),
        "state": state,
        "registry_path": rel(registry_path),
        "include_proposed": include_proposed,
        "approved_or_included_source_count": len(sources),
        "candidate_proposal_count": len(proposals),
        "source_review_count": len(proposed_sources),
        "candidate_proposals": proposals,
        "source_review_queue": proposed_sources,
        "errors": [],
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": False,
        "allows_pr_or_deploy": False,
        "next_actions": [
            "Approve or reject proposed sources before using them in scheduled discovery.",
            "Add explicit topic_seeds or approved search tooling before expecting external topic candidates.",
            "Pass this JSON to llm-scout with --external-proposals when candidate_proposals are ready.",
            "Public content edits still require exact proposed text, owner approval, apply-preview, apply-approved, and strict QA.",
        ],
        "safety": "No content, backlog, manifest, PR, or production files were modified by External Scout.",
    }
    write_external_scout(payload)
    return 0, payload


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# External Scout - {payload['generated_at']}",
        "",
        "## Outcome",
        "",
        f"- State: `{payload['state']}`",
        f"- Registry: `{payload.get('registry_path', '')}`",
        f"- Included sources: `{payload.get('approved_or_included_source_count', 0)}`",
        f"- Candidate proposals: `{payload.get('candidate_proposal_count', 0)}`",
        f"- Proposed sources awaiting owner review: `{payload.get('source_review_count', 0)}`",
        "- Allows content edit: `false`",
        "- Allows backlog mutation: `false`",
        "- Allows manifest mutation: `false`",
        "- Allows PR/deploy: `false`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if payload.get("errors"):
        lines.extend(["## Errors", "", md_list(payload["errors"]), ""])
    if payload.get("source_review_queue"):
        lines.extend(["## Source Review Queue", ""])
        for source in payload["source_review_queue"]:
            lines.extend(
                [
                    f"### {source.get('source_id', '')}",
                    "",
                    f"- Name: {source.get('name', '')}",
                    f"- Base URL: `{source.get('base_url', '')}`",
                    f"- Trust level: `{source.get('trust_level', '')}`",
                    f"- Notes: {source.get('notes', '')}",
                    "",
                ]
            )
    lines.extend(["## Candidate Proposals", ""])
    if not payload.get("candidate_proposals"):
        lines.extend(["- None", ""])
    for proposal in payload.get("candidate_proposals", []):
        lines.extend(
            [
                f"### {proposal.get('topic_id', '')}",
                "",
                f"- Title: {proposal.get('title', '')}",
                f"- Source: `{proposal.get('source_reference', '')}`",
                f"- Decision hint: `{proposal.get('recommended_action', '')}`",
                f"- Target: `{proposal.get('target_page_or_slug', '')}`",
                f"- Priority: `{proposal.get('priority', '')}`",
                f"- Risk: `{proposal.get('risk_level', '')}`",
                f"- Cross-validation: `{proposal.get('cross_validation_status', '')}`",
                "",
                "Evidence:",
                "",
                md_list(proposal.get("evidence", [])),
                "",
                "Claims to verify:",
                "",
                md_list(proposal.get("claims_to_verify", [])),
                "",
            ]
        )
    lines.extend(["## Next Actions", "", md_list(payload.get("next_actions", [])), ""])
    return "\n".join(lines)


def write_external_scout(payload: dict[str, Any]) -> tuple[Path, Path]:
    json_path = resolve_path(payload["output_path"])
    markdown_path = resolve_path(payload["markdown_path"])
    json_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(json_path, payload)
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return json_path, markdown_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run no-write external source scout from the source registry.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="Path to source_registry.json.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for External Scout artifacts.")
    parser.add_argument("--basename", default="external-scout", help="Output basename without extension.")
    parser.add_argument("--include-proposed", action="store_true", help="Include proposed sources for manual testing only.")
    parser.add_argument("--limit", type=int, default=12, help="Maximum external candidate proposals.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, payload = build_external_scout(
        registry_path=resolve_path(args.registry),
        output_dir=resolve_path(args.output_dir),
        basename=args.basename,
        include_proposed=args.include_proposed,
        limit=args.limit,
    )
    summary = {
        "state": payload["state"],
        "candidate_proposal_count": payload.get("candidate_proposal_count", 0),
        "source_review_count": payload.get("source_review_count", 0),
        "output_path": payload["output_path"],
        "markdown_path": payload["markdown_path"],
        "errors": payload.get("errors", []),
        "safety": payload["safety"],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Candidate proposals: {summary['candidate_proposal_count']}")
        print(f"Source review queue: {summary['source_review_count']}")
        print(f"Markdown: {summary['markdown_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
