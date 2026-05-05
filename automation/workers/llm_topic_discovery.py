#!/usr/bin/env python3
"""No-write topic discovery bridge from LLM Scout output to backlog-shaped proposals."""

from __future__ import annotations

import argparse
import json
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
MANIFESTS_DIR = ROOT / "automation" / "manifests"
DEFAULT_LLM_SCOUT_RESULT = REPORTS_DIR / "llm-scout-review-result.json"
DEFAULT_LLM_SCOUT_REQUEST = REPORTS_DIR / "llm-scout-review-request.json"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def proposal_index(scout_request: dict[str, Any]) -> dict[str, dict[str, Any]]:
    proposals = scout_request.get("inputs", {}).get("proposals", [])
    return {
        str(proposal.get("topic_id", "")): proposal
        for proposal in proposals
        if proposal.get("topic_id")
    }


def selected_opportunities(scout_result: dict[str, Any]) -> list[dict[str, Any]]:
    response = scout_result.get("response_json")
    if not isinstance(response, dict):
        return []
    selected = response.get("selected_opportunities", [])
    return selected if isinstance(selected, list) else []


def existing_topic_review(topic_id: str) -> dict[str, Any] | None:
    if not MANIFESTS_DIR.exists():
        return None
    candidates: list[dict[str, Any]] = []
    for path in sorted(MANIFESTS_DIR.glob("*.json")):
        try:
            manifest = load_json(path)
        except json.JSONDecodeError:
            continue
        inputs = manifest.get("inputs", {})
        source_reference = str(inputs.get("source_reference", ""))
        run_id = str(manifest.get("run_id", path.stem))
        if topic_id not in run_id and topic_id not in source_reference:
            continue
        candidates.append(
            {
                "run_id": run_id,
                "status": manifest.get("status", ""),
                "risk_level": manifest.get("risk_level", ""),
                "summary": manifest.get("summary", ""),
                "closeout": (manifest.get("artifacts", {}) or {}).get("closeout", {}),
            }
        )
    terminal = [item for item in candidates if item.get("status") in {"closed", "rejected"}]
    if terminal:
        return terminal[-1]
    return candidates[-1] if candidates else None


def blocked_payload(
    scout_result_path: Path,
    scout_request_path: Path,
    output_dir: Path,
    basename: str,
    errors: list[str],
) -> dict[str, Any]:
    generated_at = now_utc()
    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    return {
        "schema_version": 1,
        "report_type": "llm_topic_discovery",
        "generated_at": generated_at,
        "state": "blocked",
        "source_llm_scout_result": rel(scout_result_path),
        "source_llm_scout_request": rel(scout_request_path),
        "topic_count": 0,
        "topics": [],
        "errors": errors,
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "safety": "No content, backlog, manifest, PR, or production files were modified by LLM topic discovery.",
    }


def topic_from_selection(selected: dict[str, Any], deterministic: dict[str, Any]) -> dict[str, Any]:
    decision = str(selected.get("decision", "monitor"))
    prior_review = existing_topic_review(str(selected.get("topic_id") or deterministic.get("topic_id") or ""))
    status = "candidate" if decision in {"update_existing", "create_new", "consolidate"} else "monitor"
    if prior_review and prior_review.get("status") in {"closed", "rejected"}:
        status = "monitor"
        decision = "monitor"
    confidence = str(deterministic.get("confidence", "medium"))
    priority = str(selected.get("priority") or deterministic.get("priority") or "medium")
    if prior_review and prior_review.get("status") in {"closed", "rejected"}:
        priority = "low"
    target = str(deterministic.get("target_page_or_slug", ""))
    topic_id = str(selected.get("topic_id") or deterministic.get("topic_id") or "")
    title = str(deterministic.get("title") or topic_id.replace("-", " ").title())
    rationale = str(selected.get("rationale", ""))
    if prior_review and prior_review.get("status") in {"closed", "rejected"}:
        rationale = (
            f"{rationale} Prior run `{prior_review.get('run_id')}` is `{prior_review.get('status')}`; "
            "keep this topic in monitoring unless new evidence materially changes the opportunity."
        ).strip()
    recommended_action = decision if decision != "monitor" else ("monitor" if status == "monitor" else deterministic.get("recommended_action", "update_existing"))
    return {
        "topic_id": topic_id,
        "title": title,
        "cluster": deterministic.get("cluster", ""),
        "recommended_action": recommended_action,
        "archetype_suggestion": deterministic.get("archetype_suggestion", ""),
        "target_page_or_slug": target,
        "source_type": "llm_scout",
        "source_reference": deterministic.get("source_reference", ""),
        "confidence": confidence,
        "priority": priority,
        "status": status,
        "notes": rationale,
        "risk_level": selected.get("risk_level", deterministic.get("risk_level", "")),
        "player_value": selected.get("player_value", ""),
        "duplication_risk": selected.get("duplication_risk", ""),
        "claims_to_verify": selected.get("claims_to_verify", []),
        "next_step": selected.get("next_step", ""),
        "evidence": deterministic.get("evidence", []),
        "site_fit": deterministic.get("site_fit", {}),
        "constraints": deterministic.get("constraints", []),
        "reject_if": deterministic.get("reject_if", []),
        "prior_review": prior_review,
        "human_approval_required": status == "candidate",
        "backlog_row_preview": {
            "topic_id": topic_id,
            "title": title,
            "cluster": deterministic.get("cluster", ""),
            "recommended_action": recommended_action,
            "archetype_suggestion": deterministic.get("archetype_suggestion", ""),
            "target_page_or_slug": target,
            "source_type": "llm_scout",
            "source_reference": deterministic.get("source_reference", ""),
            "confidence": confidence,
            "priority": priority,
            "status": status,
            "notes": rationale,
        },
    }


def build_discovery(
    scout_result_path: Path,
    scout_request_path: Path,
    output_dir: Path,
    basename: str,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    scout_result = load_json(scout_result_path)
    scout_request = load_json(scout_request_path)
    result_state = scout_result.get("state")
    errors = list(scout_result.get("errors", []))
    source_index = proposal_index(scout_request)

    if result_state != "completed":
        payload = blocked_payload(
            scout_result_path,
            scout_request_path,
            output_dir,
            basename,
            errors or [f"LLM Scout result is not completed: {result_state}"],
        )
        return 1, payload

    topics: list[dict[str, Any]] = []
    for selected in selected_opportunities(scout_result):
        topic_id = str(selected.get("topic_id", ""))
        deterministic = source_index.get(topic_id)
        if not deterministic:
            errors.append(f"Selected topic `{topic_id}` was not found in the source Scout request.")
            continue
        topics.append(topic_from_selection(selected, deterministic))

    state = "topic_discovery_ready" if topics and not errors else "blocked"
    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    payload = {
        "schema_version": 1,
        "report_type": "llm_topic_discovery",
        "generated_at": now_utc(),
        "state": state,
        "source_llm_scout_result": rel(scout_result_path),
        "source_llm_scout_request": rel(scout_request_path),
        "topic_count": len(topics),
        "topics": topics,
        "errors": errors,
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "safety": "No content, backlog, manifest, PR, or production files were modified by LLM topic discovery.",
    }
    return (0 if state == "topic_discovery_ready" else 1), payload


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# LLM Topic Discovery - {payload['generated_at']}",
        "",
        "## Overview",
        "",
        f"- State: `{payload['state']}`",
        f"- Source Scout result: `{payload['source_llm_scout_result']}`",
        f"- Source Scout request: `{payload['source_llm_scout_request']}`",
        f"- Topics: {payload['topic_count']}",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if payload.get("errors"):
        lines.extend(["## Errors", "", md_list(payload["errors"]), ""])

    lines.extend(["## Topic Proposals", ""])
    if not payload.get("topics"):
        lines.append("- None")
        return "\n".join(lines) + "\n"

    for topic in payload["topics"]:
        route = topic.get("site_fit", {}).get("expected_internal_route", [])
        lines.extend(
            [
                f"### {topic['topic_id']}",
                "",
                f"- Title: {topic['title']}",
                f"- Target: `{topic['target_page_or_slug']}`",
                f"- Cluster: `{topic['cluster']}`",
                f"- Action: `{topic['recommended_action']}`",
                f"- Archetype: `{topic['archetype_suggestion']}`",
                f"- Priority: `{topic['priority']}`",
                f"- Risk: `{topic['risk_level']}`",
                f"- Confidence: `{topic['confidence']}`",
                f"- Prior review: `{(topic.get('prior_review') or {}).get('status', 'none')}`",
                f"- Human approval required: `{str(topic['human_approval_required']).lower()}`",
                "",
                "Player value:",
                "",
                topic.get("player_value", ""),
                "",
                "Rationale:",
                "",
                topic.get("notes", ""),
                "",
                "Duplication risk:",
                "",
                topic.get("duplication_risk", ""),
                "",
                "Expected route:",
                "",
                md_list(route),
                "",
                "Claims to verify:",
                "",
                md_list(topic.get("claims_to_verify", [])),
                "",
                "Evidence:",
                "",
                md_list(topic.get("evidence", [])),
                "",
                "Backlog Row Preview:",
                "",
                "```json",
                json.dumps(topic["backlog_row_preview"], indent=2, ensure_ascii=False),
                "```",
                "",
                "Next step:",
                "",
                topic.get("next_step", ""),
                "",
            ]
        )
    return "\n".join(lines)


def write_discovery(payload: dict[str, Any]) -> tuple[Path, Path]:
    json_path = resolve_path(payload["output_path"])
    markdown_path = resolve_path(payload["markdown_path"])
    json_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(json_path, payload)
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return json_path, markdown_path


def run_topic_discovery(
    scout_result_path: Path,
    scout_request_path: Path,
    output_dir: Path,
    basename: str,
) -> tuple[int, dict[str, Any]]:
    code, payload = build_discovery(scout_result_path, scout_request_path, output_dir, basename)
    write_discovery(payload)
    return code, payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build no-write topic discovery proposals from LLM Scout output.")
    parser.add_argument("--scout-result", default=str(DEFAULT_LLM_SCOUT_RESULT), help="Path to llm-scout-review-result.json.")
    parser.add_argument("--scout-request", default=str(DEFAULT_LLM_SCOUT_REQUEST), help="Path to llm-scout-review-request.json.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for topic discovery artifacts.")
    parser.add_argument("--basename", default="llm-topic-discovery", help="Output basename without extension.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    scout_result_path = resolve_path(args.scout_result)
    scout_request_path = resolve_path(args.scout_request)
    code, payload = run_topic_discovery(
        scout_result_path=scout_result_path,
        scout_request_path=scout_request_path,
        output_dir=resolve_path(args.output_dir),
        basename=args.basename,
    )
    summary = {
        "state": payload["state"],
        "topic_count": payload["topic_count"],
        "output_path": payload["output_path"],
        "markdown_path": payload["markdown_path"],
        "errors": payload.get("errors", []),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Topics: {summary['topic_count']}")
        print(f"Output: {summary['output_path']}")
        print(f"Markdown: {summary['markdown_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
