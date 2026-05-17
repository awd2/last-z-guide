#!/usr/bin/env python3
"""Build a compact owner digest from the latest LLM auto-review queue."""

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

from automation.io import write_json
from automation.proposal_renderer import md_list
from automation.reports import llm_auto_review_latest


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_QUEUE_PATH = REPORTS_DIR / "llm-auto-review-queue" / "llm-auto-review-queue.json"
DEFAULT_JSON_OUTPUT = REPORTS_DIR / "llm-owner-digest.json"
DEFAULT_MARKDOWN_OUTPUT = REPORTS_DIR / "llm-owner-digest.md"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def compact_item(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "topic_id": item.get("topic_id", ""),
        "target_page_or_slug": item.get("target_page_or_slug", ""),
        "cluster": item.get("cluster", ""),
        "priority": item.get("priority", ""),
        "risk_level": item.get("risk_level", ""),
        "score": item.get("score"),
        "status": item.get("status", ""),
        "recommended_owner_action": item.get("recommended_owner_action", ""),
        "owner_decision_state": item.get("owner_decision_state", ""),
        "owner_decision_note": item.get("owner_decision_note", ""),
        "chain_markdown": item.get("chain_markdown", ""),
        "owner_decision_markdown": item.get("owner_decision_markdown", ""),
        "approve_for_intake_command": item.get("approve_for_intake_command", ""),
        "blocking_issue_count": len(item.get("blocking_issues", []) or []),
        "owner_question_count": len(item.get("owner_questions", []) or []),
    }


def digest_state(view: dict[str, Any], needs_review: list[dict[str, Any]], failed: list[dict[str, Any]]) -> str:
    if failed:
        return "blocked_or_failed"
    if needs_review:
        return "owner_review_needed"
    if view.get("resolved_by_owner_decision_count", 0):
        return "no_action_needed"
    if not view.get("items"):
        return "no_candidates"
    return "monitor"


def recommended_next_action(state: str) -> str:
    if state == "blocked_or_failed":
        return "Open the failed chain artifact and fix the blocked worker stage before approving intake."
    if state == "owner_review_needed":
        return "Review the listed topics and approve only if the player value and claims are valid."
    if state == "no_action_needed":
        return "No owner action needed; wait for new GSC/Bing/external-source signals."
    if state == "no_candidates":
        return "No candidate topics are ready; wait for new signals."
    return "Monitor the queue; no content action is approved by this digest."


def build_digest(queue_path: Path = DEFAULT_QUEUE_PATH) -> dict[str, Any]:
    view = llm_auto_review_latest.build_view(queue_path)
    items = view.get("items", [])
    if not isinstance(items, list):
        items = []
    resolved = [item for item in items if item.get("owner_decision_resolved")]
    failed = [
        item
        for item in items
        if item.get("status") == "failed" or item.get("recommended_owner_action") == "review_failed_chain_before_decision"
    ]
    needs_review = [
        item
        for item in items
        if not item.get("owner_decision_resolved")
        and item not in failed
        and (item.get("owner_approval_required") or item.get("recommended_owner_action") != "manual_owner_review")
    ]
    ready_for_intake = [
        item
        for item in needs_review
        if item.get("approve_for_intake_command") and item.get("recommended_owner_action") != "answer_owner_questions_before_intake"
    ]
    state = digest_state(view, needs_review, failed)
    return {
        "schema_version": 1,
        "report_type": "llm_owner_digest",
        "generated_at": now_utc(),
        "state": state,
        "recommended_next_action": recommended_next_action(state),
        "queue_path": view.get("queue_path", rel(queue_path)),
        "queue_state": view.get("queue_state", ""),
        "queue_provider": view.get("queue_provider", ""),
        "counts": {
            "candidate_topics": view.get("candidate_topic_count", 0),
            "queued_topics": view.get("queued_topic_count", 0),
            "failed_items": view.get("failed_item_count", 0),
            "needs_owner_decision": view.get("needs_owner_decision_count", 0),
            "resolved_by_owner_decision": view.get("resolved_by_owner_decision_count", 0),
            "digest_needs_review": len(needs_review),
            "digest_failed": len(failed),
            "digest_ready_for_intake": len(ready_for_intake),
        },
        "needs_review": [compact_item(item) for item in needs_review],
        "ready_for_intake": [compact_item(item) for item in ready_for_intake],
        "blocked_or_failed": [compact_item(item) for item in failed],
        "resolved": [compact_item(item) for item in resolved],
        "safety": "Read-only owner digest. No LLM calls, content edits, backlog changes, manifests, PRs, or production changes were made.",
    }


def render_markdown(digest: dict[str, Any]) -> str:
    counts = digest.get("counts", {})
    lines = [
        f"# LLM Owner Digest - {digest['generated_at']}",
        "",
        "## Summary",
        "",
        f"- State: `{digest.get('state', '')}`",
        f"- Recommended next action: {digest.get('recommended_next_action', '')}",
        f"- Queue: `{digest.get('queue_path', '')}`",
        f"- Candidate topics: `{counts.get('candidate_topics', 0)}`",
        f"- Needs owner review: `{counts.get('digest_needs_review', 0)}`",
        f"- Ready for intake: `{counts.get('digest_ready_for_intake', 0)}`",
        f"- Blocked or failed: `{counts.get('digest_failed', 0)}`",
        f"- Resolved by decision: `{counts.get('resolved_by_owner_decision', 0)}`",
        "- Safety: read-only; no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    sections = [
        ("Needs Owner Review", digest.get("needs_review", [])),
        ("Ready For Intake", digest.get("ready_for_intake", [])),
        ("Blocked Or Failed", digest.get("blocked_or_failed", [])),
        ("Resolved", digest.get("resolved", [])),
    ]
    for title, items in sections:
        lines.extend([f"## {title}", ""])
        if not items:
            lines.extend(["- None", ""])
            continue
        for item in items:
            details = [
                f"target `{item.get('target_page_or_slug', '')}`",
                f"priority `{item.get('priority', '')}`",
                f"risk `{item.get('risk_level', '')}`",
                f"action `{item.get('recommended_owner_action', '')}`",
            ]
            lines.append(f"- `{item.get('topic_id', '')}`: " + ", ".join(details))
            if item.get("chain_markdown"):
                lines.append(f"  - Chain: `{item['chain_markdown']}`")
            if item.get("owner_decision_markdown"):
                lines.append(f"  - Decision: `{item['owner_decision_markdown']}`")
            if item.get("approve_for_intake_command"):
                lines.append("  - Intake command:")
                lines.append(f"    ```bash\n    {item['approve_for_intake_command']}\n    ```")
        lines.append("")
    lines.extend(["## Policy", "", md_list([
        "This digest does not approve public copy.",
        "Public content still requires exact proposed text, owner approval, apply-preview, apply-approved, and strict QA.",
        "Use this digest to decide whether any queue item deserves owner attention today.",
    ])])
    return "\n".join(lines)


def write_digest(digest: dict[str, Any], json_output: Path, markdown_output: Path) -> tuple[Path, Path]:
    json_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    write_json(json_output, digest)
    markdown_output.write_text(render_markdown(digest), encoding="utf-8")
    return json_output, markdown_output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a compact owner digest from the latest LLM auto-review queue.")
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE_PATH), help="Path to llm-auto-review-queue.json.")
    parser.add_argument("--json-output", default=str(DEFAULT_JSON_OUTPUT), help="Path for the digest JSON artifact.")
    parser.add_argument("--markdown-output", default=str(DEFAULT_MARKDOWN_OUTPUT), help="Path for the digest markdown artifact.")
    parser.add_argument("--no-write", action="store_true", help="Build and print only; do not write digest artifacts.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    digest = build_digest(resolve_path(args.queue))
    json_path = resolve_path(args.json_output)
    markdown_path = resolve_path(args.markdown_output)
    if not args.no_write:
        write_digest(digest, json_path, markdown_path)
    summary = {
        "state": digest["state"],
        "recommended_next_action": digest["recommended_next_action"],
        "counts": digest["counts"],
        "json_output": rel(json_path),
        "markdown_output": rel(markdown_path),
        "safety": digest["safety"],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(render_markdown(digest))
        if not args.no_write:
            print(f"\nJSON: {summary['json_output']}")
            print(f"Markdown: {summary['markdown_output']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
