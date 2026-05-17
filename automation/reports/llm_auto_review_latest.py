#!/usr/bin/env python3
"""Read the latest LLM auto-review queue as an owner decision view."""

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

from automation.io import load_json
from automation.proposal_renderer import md_list


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_QUEUE_PATH = REPORTS_DIR / "llm-auto-review-queue" / "llm-auto-review-queue.json"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def load_stage_response(chain: dict[str, Any], stage_name: str) -> dict[str, Any]:
    result_path = chain.get("stages", {}).get(stage_name, {}).get("result_path")
    if not result_path:
        return {}
    path = resolve_path(str(result_path))
    if not path.exists():
        return {}
    result = load_json(path)
    response = result.get("response_json")
    return response if isinstance(response, dict) else {}


def load_chain(path_value: str) -> dict[str, Any]:
    if not path_value:
        return {}
    path = resolve_path(path_value)
    if not path.exists():
        return {}
    return load_json(path)


def decision_reports_dir(queue_path: Path) -> Path:
    if queue_path.parent.name == "llm-auto-review-queue":
        return queue_path.parent.parent
    return queue_path.parent


def load_topic_decisions(queue_path: Path) -> dict[str, dict[str, Any]]:
    reports_dir = decision_reports_dir(queue_path)
    decisions: dict[str, dict[str, Any]] = {}
    for path in sorted(reports_dir.glob("llm-topic-decision-*.json")):
        if path.name == "llm-topic-decisions.json":
            continue
        payload = load_json(path)
        if payload.get("report_type") != "llm_topic_decision":
            continue
        topic_id = str(payload.get("topic_id") or "")
        if not topic_id:
            continue
        decisions[topic_id] = {
            "decision_state": payload.get("decision_state", ""),
            "decision_note": payload.get("decision_note", ""),
            "artifact_path": rel(path),
            "markdown_path": payload.get("markdown_path", ""),
            "allows_worker_chain": bool(payload.get("allows_worker_chain", False)),
            "allows_content_edit": bool(payload.get("allows_content_edit", False)),
        }
    return decisions


def blocking_issue_lines(reviewer: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for issue in reviewer.get("blocking_issues", []):
        if not isinstance(issue, dict):
            continue
        severity = issue.get("severity", "")
        text = issue.get("issue", "")
        fix = issue.get("required_fix", "")
        lines.append(f"{severity}: {text} Required fix: {fix}".strip())
    return lines


def recommended_owner_action(queue_item: dict[str, Any], chain: dict[str, Any], reviewer: dict[str, Any]) -> str:
    item_status = queue_item.get("status")
    if item_status not in {"completed", "skipped_existing_chain"} or chain.get("state") != "completed":
        return "review_failed_chain_before_decision"
    if chain.get("review_verdict") in {"reject", "revise"}:
        return "reject_or_request_revision"
    if reviewer.get("blocking_issues"):
        return "answer_owner_questions_before_intake"
    if chain.get("approved_next_stage") in {"proposal", "patch_plan"}:
        return "approve_for_intake_if_player_value_and_claims_are_valid"
    if chain.get("approved_next_stage") == "brief":
        return "approve_narrow_brief_or_monitor"
    return "manual_owner_review"


def decision_owner_action(decision: dict[str, Any] | None, fallback_action: str) -> str:
    if not decision:
        return fallback_action
    state = decision.get("decision_state")
    if state == "monitor":
        return "decision_recorded_monitor"
    if state == "rejected":
        return "decision_recorded_rejected"
    if state == "approved_for_chain":
        return "decision_recorded_approved_for_chain"
    return fallback_action


def intake_command(chain_path: str, topic_id: str) -> str:
    return (
        "python3 automation/pipeline.py llm-intake-latest "
        f"--chain {chain_path} "
        "--approved-by <owner> "
        f"--note \"Approved owner scope for {topic_id}: <answer reviewer questions and validation scope>\" "
        "--resolve-reviewer-blockers --json"
    )


def compact_queue_item(queue_item: dict[str, Any], decisions: dict[str, dict[str, Any]]) -> dict[str, Any]:
    chain_path = str(queue_item.get("chain_json") or queue_item.get("existing_chain") or "")
    chain = load_chain(chain_path)
    editor = load_stage_response(chain, "llm_editor")
    reviewer = load_stage_response(chain, "llm_reviewer")
    topic_id = str(queue_item.get("topic_id") or chain.get("source_topic_id") or "")
    owner_questions = reviewer.get("owner_questions", [])
    if not isinstance(owner_questions, list):
        owner_questions = []
    warnings = reviewer.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = []
    required_checks = reviewer.get("required_checks", [])
    if not isinstance(required_checks, list):
        required_checks = []
    exact_replacements = editor.get("exact_replacements", [])
    if not isinstance(exact_replacements, list):
        exact_replacements = []
    inferred_chain_markdown = ""
    if chain_path:
        markdown_path = resolve_path(chain_path).with_suffix(".md")
        inferred_chain_markdown = rel(markdown_path) if markdown_path.exists() else ""
    decision = decisions.get(topic_id)
    fallback_action = recommended_owner_action(queue_item, chain, reviewer)
    owner_action = decision_owner_action(decision, fallback_action)
    owner_decision_resolved = bool(decision and decision.get("decision_state") in {"monitor", "rejected", "approved_for_chain"})
    return {
        "topic_id": topic_id,
        "target_page_or_slug": queue_item.get("target_page_or_slug") or chain.get("target_page_or_slug", ""),
        "cluster": queue_item.get("cluster", ""),
        "priority": queue_item.get("priority", ""),
        "risk_level": queue_item.get("risk_level") or chain.get("risk_level"),
        "score": queue_item.get("score"),
        "status": queue_item.get("status", ""),
        "review_verdict": chain.get("review_verdict") or queue_item.get("review_verdict"),
        "approved_next_stage": chain.get("approved_next_stage") or queue_item.get("approved_next_stage"),
        "owner_approval_required": bool(chain.get("owner_approval_required", queue_item.get("owner_approval_required", False))),
        "recommended_owner_action": owner_action,
        "owner_decision_resolved": owner_decision_resolved,
        "owner_decision_state": decision.get("decision_state", "") if decision else "",
        "owner_decision_note": decision.get("decision_note", "") if decision else "",
        "owner_decision_artifact": decision.get("artifact_path", "") if decision else "",
        "owner_decision_markdown": decision.get("markdown_path", "") if decision else "",
        "player_value_check": "Approve only if this solves a real player job and the mechanics/source claims match owner game knowledge.",
        "brief_summary": editor.get("brief_summary", ""),
        "primary_user_job": editor.get("primary_user_job", ""),
        "first_screen_plan": editor.get("first_screen_plan", ""),
        "blocking_issues": reviewer.get("blocking_issues", []),
        "blocking_issue_summary": blocking_issue_lines(reviewer),
        "warnings": warnings,
        "owner_questions": owner_questions,
        "required_checks": required_checks,
        "exact_replacements_count": len(exact_replacements),
        "chain_json": chain_path,
        "chain_markdown": queue_item.get("chain_markdown") or inferred_chain_markdown,
        "editor_markdown": chain.get("stages", {}).get("llm_editor", {}).get("markdown_path", ""),
        "reviewer_markdown": chain.get("stages", {}).get("llm_reviewer", {}).get("markdown_path", ""),
        "approve_for_intake_command": "" if owner_decision_resolved or not chain_path else intake_command(chain_path, topic_id),
        "monitor_decision_guidance": "Leave this item as monitor-only if the player job is not important enough, overlaps an existing page, or needs better evidence.",
        "reject_decision_guidance": "Reject if the topic would mislead players, blur page roles, or cannot be validated from game knowledge and reliable sources.",
    }


def build_view(queue_path: Path) -> dict[str, Any]:
    if not queue_path.exists():
        raise FileNotFoundError(f"LLM auto-review queue artifact not found: {rel(queue_path)}")
    queue = load_json(queue_path)
    queue_items = queue.get("queue_items", [])
    if not isinstance(queue_items, list):
        queue_items = []
    skipped_topics = queue.get("skipped_topics", [])
    if not isinstance(skipped_topics, list):
        skipped_topics = []
    resolved_topics = queue.get("resolved_by_decision", [])
    if not isinstance(resolved_topics, list):
        resolved_topics = []
    review_items = list(queue_items)
    review_items.extend(
        item
        for item in skipped_topics
        if isinstance(item, dict) and item.get("status") == "skipped_existing_chain" and item.get("existing_chain")
    )
    review_items.extend(item for item in resolved_topics if isinstance(item, dict))
    decisions = load_topic_decisions(queue_path)
    items = [compact_queue_item(item, decisions) for item in review_items if isinstance(item, dict)]
    needs_owner = [
        item
        for item in items
        if not item.get("owner_decision_resolved")
        and (item.get("owner_approval_required") or item.get("recommended_owner_action") != "manual_owner_review")
    ]
    resolved_by_decision = [item for item in items if item.get("owner_decision_resolved")]
    return {
        "schema_version": 1,
        "report_type": "llm_auto_review_latest_owner_view",
        "generated_at": now_utc(),
        "queue_path": rel(queue_path),
        "queue_state": queue.get("state", ""),
        "queue_provider": queue.get("provider", ""),
        "candidate_topic_count": queue.get("candidate_topic_count", 0),
        "queued_topic_count": queue.get("queued_topic_count", 0),
        "completed_item_count": queue.get("completed_item_count", 0),
        "failed_item_count": queue.get("failed_item_count", 0),
        "skipped_existing_count": queue.get("skipped_existing_count", 0),
        "needs_owner_decision_count": len(needs_owner),
        "resolved_by_owner_decision_count": len(resolved_by_decision),
        "items": items,
        "owner_decision_policy": [
            "Approve for intake only after owner validates player value, source fit, and non-misleading claims.",
            "Intake approval does not approve public copy, patch specs, backlog mutation, PR creation, deployment, or production publishing.",
            "Public content still requires exact proposed text, owner approval, apply-preview, apply-approved, and strict QA.",
        ],
        "safety": "Read-only auto-review owner view. No content, backlog, manifest, PR, or production files were modified.",
    }


def render_markdown(view: dict[str, Any]) -> str:
    lines = [
        f"# LLM Auto Review Latest - {view['generated_at']}",
        "",
        "## Queue",
        "",
        f"- State: `{view.get('queue_state', '')}`",
        f"- Provider: `{view.get('queue_provider', '')}`",
        f"- Candidate topics: `{view.get('candidate_topic_count', 0)}`",
        f"- Queued topics: `{view.get('queued_topic_count', 0)}`",
        f"- Completed items: `{view.get('completed_item_count', 0)}`",
        f"- Failed items: `{view.get('failed_item_count', 0)}`",
        f"- Needs owner decision: `{view.get('needs_owner_decision_count', 0)}`",
        f"- Resolved by owner decision: `{view.get('resolved_by_owner_decision_count', 0)}`",
        f"- Queue artifact: `{view.get('queue_path', '')}`",
        "- Safety: read-only; no content, backlog, manifest, PR, or production files were modified.",
        "",
        "## Owner Decision Policy",
        "",
        md_list(view.get("owner_decision_policy", [])),
        "",
        "## Items",
        "",
    ]
    if not view.get("items"):
        lines.extend(["- None", ""])
        return "\n".join(lines)

    for index, item in enumerate(view["items"], start=1):
        lines.extend(
            [
                f"### {index}. {item.get('topic_id', '')}",
                "",
                f"- Target: `{item.get('target_page_or_slug', '')}`",
                f"- Cluster: `{item.get('cluster', '')}`",
                f"- Priority: `{item.get('priority', '')}`",
                f"- Risk: `{item.get('risk_level')}`",
                f"- Score: `{item.get('score')}`",
                f"- Verdict: `{item.get('review_verdict')}`",
                f"- Approved next stage: `{item.get('approved_next_stage')}`",
                f"- Recommended owner action: `{item.get('recommended_owner_action')}`",
                f"- Owner decision: `{item.get('owner_decision_state', '')}`",
                f"- Owner decision artifact: `{item.get('owner_decision_markdown', '')}`",
                f"- Chain: `{item.get('chain_markdown', '')}`",
                "",
                "Player value check:",
                "",
                item.get("player_value_check", ""),
                "",
                "Brief:",
                "",
                item.get("brief_summary", ""),
                "",
                "Primary user job:",
                "",
                item.get("primary_user_job", ""),
                "",
                "Owner questions:",
                "",
                md_list(item.get("owner_questions", [])),
                "",
                "Blocking issues:",
                "",
                md_list(item.get("blocking_issue_summary", [])),
                "",
                "Warnings:",
                "",
                md_list(item.get("warnings", [])),
                "",
                "Owner decision note:",
                "",
                item.get("owner_decision_note", ""),
                "",
                "Approve for intake command:",
                "",
                f"```bash\n{item.get('approve_for_intake_command', '')}\n```",
                "",
                "Monitor / reject guidance:",
                "",
                md_list([item.get("monitor_decision_guidance", ""), item.get("reject_decision_guidance", "")]),
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read the latest LLM auto-review queue as an owner decision view.")
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE_PATH), help="Path to llm-auto-review-queue.json.")
    parser.add_argument("--json", action="store_true", help="Print the owner decision view as JSON.")
    args = parser.parse_args()

    view = build_view(resolve_path(args.queue))
    if args.json:
        print(json.dumps(view, indent=2))
    else:
        print(render_markdown(view))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
