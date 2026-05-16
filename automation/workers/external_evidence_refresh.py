#!/usr/bin/env python3
"""No-write evidence queue builder for approved external source leads."""

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

from automation.io import load_json, write_json
from automation.proposal_renderer import md_list


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_EXTERNAL_SCOUT = REPORTS_DIR / "external-scout.json"


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
    return value.strip("-") or "item"


def load_external_scout(path: Path) -> tuple[list[str], dict[str, Any]]:
    if not path.exists():
        return [f"External Scout artifact not found: {rel(path)}"], {}
    payload = load_json(path)
    if payload.get("report_type") != "external_scout":
        return [f"Unsupported External Scout report type in {rel(path)}: {payload.get('report_type')}"], payload
    if payload.get("state") not in {"external_scout_ready", "source_approval_needed"}:
        return [f"External Scout artifact is not ready: {payload.get('state')}"], payload
    return [], payload


def normalize_query_tasks(payload: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for task in payload.get("source_query_tasks", []):
        if not isinstance(task, dict):
            continue
        query = str(task.get("query", "")).strip()
        if not query:
            continue
        tasks.append(
            {
                "task_id": str(task.get("task_id") or f"{task.get('source_id', 'source')}-query"),
                "task_type": "source_query",
                "source_id": task.get("source_id", ""),
                "source_name": task.get("source_name", ""),
                "base_url": task.get("base_url", ""),
                "trust_level": task.get("trust_level", ""),
                "query": query,
                "allowed_uses": task.get("allowed_uses", []),
                "crawl_policy": task.get("crawl_policy", ""),
                "freshness_window_days": task.get("freshness_window_days", 0),
                "collection_status": "pending_search_provider",
                "public_claim_ready": False,
                "notes": task.get("notes", ""),
            }
        )
    return tasks[: max(0, limit)]


def normalize_url_leads(payload: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    leads: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for proposal in payload.get("candidate_proposals", []):
        if not isinstance(proposal, dict):
            continue
        topic_id = str(proposal.get("topic_id", "external-topic"))
        for index, url in enumerate(proposal.get("source_urls", []), start=1):
            if not isinstance(url, str) or not url.startswith("https://"):
                continue
            key = (topic_id, url)
            if key in seen:
                continue
            seen.add(key)
            leads.append(
                {
                    "lead_id": f"url-{slugify(topic_id)}-{index}",
                    "task_type": "explicit_url",
                    "topic_id": topic_id,
                    "title": proposal.get("title", ""),
                    "source_id": proposal.get("source_id", ""),
                    "source_name": proposal.get("source_name", ""),
                    "source_reference": proposal.get("source_reference", ""),
                    "target_page_or_slug": proposal.get("target_page_or_slug", ""),
                    "cluster": proposal.get("cluster", ""),
                    "url": url,
                    "claims_to_verify": proposal.get("claims_to_verify", []),
                    "cross_validation_status": proposal.get("cross_validation_status", "needs_second_source"),
                    "collection_status": "pending_fetch_provider_or_manual_check",
                    "public_claim_ready": False,
                    "copying_risk": proposal.get("copying_risk", "Do not copy source wording."),
                }
            )
    return leads[: max(0, limit)]


def build_claim_review_queue(url_leads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    claims: dict[str, dict[str, Any]] = {}
    for lead in url_leads:
        for raw_claim in lead.get("claims_to_verify", []):
            claim = str(raw_claim).strip()
            if not claim:
                continue
            item = claims.setdefault(
                claim,
                {
                    "claim_id": claim,
                    "topic_ids": [],
                    "source_ids": [],
                    "source_urls": [],
                    "review_status": "needs_cross_validation",
                    "public_claim_ready": False,
                    "minimum_standard": "Needs canonical memory plus at least one additional reliable source or explicit owner confirmation before public copy.",
                },
            )
            for key, value in [
                ("topic_ids", lead.get("topic_id", "")),
                ("source_ids", lead.get("source_id", "")),
                ("source_urls", lead.get("url", "")),
            ]:
                if value and value not in item[key]:
                    item[key].append(value)
    for item in claims.values():
        if len(item["source_ids"]) >= 2 or len(item["source_urls"]) >= 2:
            item["review_status"] = "has_multiple_source_leads_needs_human_validation"
    return sorted(claims.values(), key=lambda item: item["claim_id"])


def build_external_evidence_refresh(
    external_scout_path: Path,
    output_dir: Path,
    basename: str,
    limit: int,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    errors, scout_payload = load_external_scout(external_scout_path)
    if errors:
        payload = {
            "schema_version": 1,
            "report_type": "external_evidence_refresh",
            "generated_at": now_utc(),
            "state": "blocked",
            "external_scout_path": rel(external_scout_path),
            "source_query_tasks": [],
            "url_evidence_leads": [],
            "claim_review_queue": [],
            "errors": errors,
            "output_path": rel(json_path),
            "markdown_path": rel(markdown_path),
            "allows_content_edit": False,
            "allows_backlog_mutation": False,
            "allows_manifest_mutation": False,
            "allows_pr_or_deploy": False,
            "safety": "No content, backlog, manifest, PR, or production files were modified by External Evidence Refresh.",
        }
        write_json(json_path, payload)
        markdown_path.write_text(render_markdown(payload), encoding="utf-8")
        return 1, payload

    query_tasks = normalize_query_tasks(scout_payload, limit=limit)
    url_leads = normalize_url_leads(scout_payload, limit=limit)
    claim_queue = build_claim_review_queue(url_leads)
    state = "evidence_queue_ready" if query_tasks or url_leads else "no_external_evidence_tasks"
    payload = {
        "schema_version": 1,
        "report_type": "external_evidence_refresh",
        "generated_at": now_utc(),
        "state": state,
        "external_scout_path": rel(external_scout_path),
        "source_query_task_count": len(query_tasks),
        "url_evidence_lead_count": len(url_leads),
        "claim_review_count": len(claim_queue),
        "source_query_tasks": query_tasks,
        "url_evidence_leads": url_leads,
        "claim_review_queue": claim_queue,
        "errors": [],
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": False,
        "allows_pr_or_deploy": False,
        "next_actions": [
            "Run a future approved search/fetch provider over source_query_tasks and url_evidence_leads.",
            "Treat collected external evidence as discovery context only until canonical memory and cross-source validation are complete.",
            "Do not use any single external source as proof for public mechanic, cost, reward, season, or event claims.",
            "Route verified opportunities back through LLM Scout, Editor, Reviewer, owner approval, proposal, apply-preview, apply-approved, and strict QA.",
        ],
        "safety": "No content, backlog, manifest, PR, or production files were modified by External Evidence Refresh.",
    }
    write_json(json_path, payload)
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return 0, payload


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# External Evidence Refresh - {payload.get('generated_at', '')}",
        "",
        "## Outcome",
        "",
        f"- State: `{payload.get('state', '')}`",
        f"- External Scout: `{payload.get('external_scout_path', '')}`",
        f"- Source query tasks: `{payload.get('source_query_task_count', 0)}`",
        f"- URL evidence leads: `{payload.get('url_evidence_lead_count', 0)}`",
        f"- Claim review groups: `{payload.get('claim_review_count', 0)}`",
        "- Allows content edit: `false`",
        "- Allows backlog mutation: `false`",
        "- Allows manifest mutation: `false`",
        "- Allows PR/deploy: `false`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if payload.get("errors"):
        lines.extend(["## Errors", "", md_list(payload["errors"]), ""])
    if payload.get("source_query_tasks"):
        lines.extend(["## Source Query Tasks", ""])
        for task in payload["source_query_tasks"]:
            lines.append(f"- `{task.get('task_id', '')}` ({task.get('trust_level', '')}): {task.get('query', '')}")
        lines.append("")
    if payload.get("url_evidence_leads"):
        lines.extend(["## URL Evidence Leads", ""])
        for lead in payload["url_evidence_leads"]:
            lines.extend(
                [
                    f"### {lead.get('lead_id', '')}",
                    "",
                    f"- Topic: `{lead.get('topic_id', '')}`",
                    f"- Source: `{lead.get('source_reference', '')}`",
                    f"- Target: `{lead.get('target_page_or_slug', '')}`",
                    f"- URL: `{lead.get('url', '')}`",
                    f"- Cross-validation: `{lead.get('cross_validation_status', '')}`",
                    "- Public claim ready: `false`",
                    "",
                    "Claims to verify:",
                    md_list(lead.get("claims_to_verify", [])),
                    "",
                ]
            )
    if payload.get("claim_review_queue"):
        lines.extend(["## Claim Review Queue", ""])
        for item in payload["claim_review_queue"]:
            lines.extend(
                [
                    f"- `{item.get('claim_id', '')}`: {item.get('review_status', '')}; sources={len(item.get('source_ids', []))}; public_claim_ready=false",
                ]
            )
        lines.append("")
    lines.extend(["## Next Actions", "", md_list(payload.get("next_actions", [])), ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a no-write external evidence queue from External Scout artifacts.")
    parser.add_argument("--external-scout", default=str(DEFAULT_EXTERNAL_SCOUT), help="Path to an External Scout JSON artifact.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for External Evidence Refresh artifacts.")
    parser.add_argument("--basename", default="external-evidence-refresh", help="Output basename without extension.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum query tasks and URL leads to include.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, payload = build_external_evidence_refresh(
        external_scout_path=resolve_path(args.external_scout),
        output_dir=resolve_path(args.output_dir),
        basename=args.basename,
        limit=args.limit,
    )
    summary = {
        "state": payload["state"],
        "source_query_task_count": payload.get("source_query_task_count", 0),
        "url_evidence_lead_count": payload.get("url_evidence_lead_count", 0),
        "claim_review_count": payload.get("claim_review_count", 0),
        "output_path": payload["output_path"],
        "markdown_path": payload["markdown_path"],
        "errors": payload.get("errors", []),
        "safety": payload["safety"],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Source query tasks: {summary['source_query_task_count']}")
        print(f"URL evidence leads: {summary['url_evidence_lead_count']}")
        print(f"Claim review groups: {summary['claim_review_count']}")
        print(f"Output: {summary['output_path']}")
        print(f"Markdown: {summary['markdown_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
