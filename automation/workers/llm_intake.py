#!/usr/bin/env python3
"""No-write intake bridge for latest LLM worker-chain opportunities."""

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
from automation.reports import llm_review_latest


REPORTS_DIR = ROOT / "automation" / "reports"

APPROVAL_GUARDRAILS = [
    "Approval is intake-only: it allows conversion into the existing run-plan/proposal flow.",
    "Approval does not approve public page copy, patch specs, backlog mutation, manifest creation, PR creation, deployment, or production publishing.",
    "Any carried exact_replacements are proposal-only data and still require propose, owner approval, apply-preview, apply-approved, and strict QA.",
    "Any future public content change still requires exact proposed text/diff and explicit owner approval.",
    "Future content proposals must still pass deterministic checks before closeout.",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def infer_chain_path(value: str | None, reports_dir: Path) -> Path:
    if value:
        return resolve_path(value)
    return llm_review_latest.latest_chain_path(reports_dir)


def load_stage_file(chain: dict[str, Any], stage_name: str, kind: str) -> dict[str, Any]:
    value = chain.get("stages", {}).get(stage_name, {}).get(kind)
    if not value:
        return {}
    path = resolve_path(str(value))
    if not path.exists():
        return {}
    payload = load_json(path)
    return payload if isinstance(payload, dict) else {}


def scout_request_proposal(chain: dict[str, Any], topic_id: str) -> dict[str, Any]:
    request = load_stage_file(chain, "llm_scout", "request_path")
    for proposal in request.get("inputs", {}).get("proposals", []):
        if proposal.get("topic_id") == topic_id:
            return proposal
    return {}


def scout_selected_opportunity(chain: dict[str, Any], topic_id: str) -> dict[str, Any]:
    response = llm_review_latest.load_stage_response(chain, "llm_scout")
    for opportunity in response.get("selected_opportunities", []):
        if opportunity.get("topic_id") == topic_id:
            return opportunity
    return {}


def editor_exact_replacements(chain: dict[str, Any]) -> list[dict[str, Any]]:
    editor_response = llm_review_latest.load_stage_response(chain, "llm_editor")
    replacements = editor_response.get("exact_replacements", [])
    if not isinstance(replacements, list):
        return []
    return [item for item in replacements if isinstance(item, dict)]


def issue_line(item: dict[str, Any]) -> str:
    severity = item.get("severity", "")
    issue = item.get("issue", "")
    required_fix = item.get("required_fix", "")
    if required_fix:
        return f"{severity}: {issue} Required fix: {required_fix}".strip()
    return f"{severity}: {issue}".strip()


def proposed_backlog_item(
    review: dict[str, Any],
    scout_proposal: dict[str, Any],
    scout_opportunity: dict[str, Any],
) -> dict[str, str]:
    topic_id = str(review.get("source_topic_id") or "llm-topic")
    target = str(review.get("target_page_or_slug") or scout_proposal.get("target_page_or_slug") or "")
    risk = str(review.get("risk_level") or scout_opportunity.get("risk_level") or scout_proposal.get("risk_level") or "")
    title = scout_proposal.get("title") or f"LLM-reviewed opportunity: {target or topic_id}"
    return {
        "topic_id": f"{topic_id}-llm-approved-intake",
        "title": str(title),
        "cluster": str(scout_proposal.get("cluster", "")),
        "recommended_action": str(scout_proposal.get("recommended_action") or scout_opportunity.get("decision", "")),
        "archetype_suggestion": str(scout_proposal.get("archetype_suggestion") or review.get("page_role", "")),
        "target_page_or_slug": target,
        "source_type": str(scout_proposal.get("source_type", "analytics")),
        "source_reference": f"LLM worker chain review: {topic_id}",
        "confidence": str(scout_proposal.get("confidence", "medium")),
        "priority": "high" if risk == "high" else str(scout_proposal.get("priority") or scout_opportunity.get("priority") or "medium"),
        "status": "backlog",
        "notes": "Created as a proposed LLM intake record only. Do not add to topic_backlog.csv or create content changes without human review.",
    }


def intake_state(
    review: dict[str, Any],
    approved_by: str | None,
    note: str | None,
    resolve_reviewer_blockers: bool = False,
) -> tuple[str, list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []
    verdict = review.get("review_verdict")
    reviewer_blocking_issues = review.get("blocking_issues", [])

    if review.get("state") != "completed":
        blockers.append("LLM worker chain is not completed; rerun or inspect the chain before intake.")
    for error in review.get("errors", []):
        blockers.append(f"LLM worker chain error: {error}")
    if verdict in {"revise", "reject"}:
        blockers.append(f"LLM Reviewer verdict is `{verdict}`; revise or reject before intake.")
    if reviewer_blocking_issues and not resolve_reviewer_blockers:
        blockers.append("LLM Reviewer returned blocking issues; resolve them before LLM intake.")
    if reviewer_blocking_issues and resolve_reviewer_blockers and (not approved_by or not note):
        blockers.append("Resolving LLM Reviewer blocking issues requires --approved-by and --note.")
    if blockers:
        return "blocked", blockers, warnings

    if reviewer_blocking_issues and resolve_reviewer_blockers:
        warnings.append("LLM Reviewer blocking issues were owner-resolved for intake only; public content is still not approved.")

    if review.get("risk_level") == "high":
        warnings.append("High-risk opportunity; keep the future proposal narrow and owner-reviewed.")
    if review.get("approved_next_stage") in {None, "", "none"}:
        warnings.append("LLM Reviewer did not approve an automatic next stage; human approval is required.")
    if review.get("owner_questions"):
        warnings.append("Owner questions must be answered before any public content proposal is written.")

    owner_required = bool(review.get("owner_approval_required", True))
    if owner_required and not approved_by:
        warnings.append("Owner approval is required before this LLM opportunity can become run intake.")
        return "approval_required", blockers, warnings
    if not approved_by and verdict == "needs_human_review":
        warnings.append("Reviewer requested human review before intake.")
        return "approval_required", blockers, warnings
    if approved_by and review.get("owner_questions") and not note:
        warnings.append("Approval note is required when the LLM Reviewer left owner questions.")
        return "approval_required", blockers, warnings
    return "approved_for_intake", blockers, warnings


def approval_scope(approved_by: str | None) -> str:
    if approved_by:
        return "intake_only_no_content_edits"
    return "none"


def next_actions_for(state: str, topic_id: str, intake_path: str | None = None) -> list[str]:
    if state == "blocked":
        return [
            "Read the LLM latest owner review and resolve blocking issues.",
            "Rerun the LLM worker chain after the Scout/Editor/Reviewer issue is fixed.",
        ]
    if state == "approval_required":
        return [
            "Human reviews the LLM latest owner review and answers owner questions.",
            f"If approved, run: python3 automation/pipeline.py llm-intake-latest --chain automation/reports/llm-worker-chain-{topic_id}.json --approved-by <name> --note \"<owner answer / approval scope>\" --json",
        ]
    return [
        "Review this intake artifact before converting it into a run-plan proposal.",
        f"Run: python3 automation/pipeline.py worker-run-plan --intake {intake_path or '<llm-intake.json>'} --json",
        "Do not write public content until a later proposal artifact receives explicit owner approval.",
    ]


def build_intake(
    chain_path: Path,
    approved_by: str | None,
    note: str | None,
    resolve_reviewer_blockers: bool = False,
) -> dict[str, Any]:
    chain = load_json(chain_path)
    review = llm_review_latest.build_review(chain_path)
    topic_id = str(review.get("source_topic_id") or "llm-topic")
    scout_proposal = scout_request_proposal(chain, topic_id)
    scout_opportunity = scout_selected_opportunity(chain, topic_id)
    exact_replacements = editor_exact_replacements(chain)
    state, blockers, warnings = intake_state(review, approved_by, note, resolve_reviewer_blockers)
    intake = {
        "schema_version": 1,
        "report_type": "llm_worker_proposal_intake",
        "generated_at": now_utc(),
        "source_chain_file": rel(chain_path),
        "source_topic_id": topic_id,
        "target_page_or_slug": review.get("target_page_or_slug", ""),
        "state": state,
        "approved_by": approved_by,
        "approval_note": note,
        "approval_scope": approval_scope(approved_by),
        "content_edit_approved": False,
        "public_content_change_allowed": False,
        "requires_owner_answers": bool(review.get("owner_questions")),
        "owner_answers_recorded": bool(note),
        "reviewer_blockers_resolved_by_owner": bool(resolve_reviewer_blockers and review.get("blocking_issues")),
        "approval_guardrails": APPROVAL_GUARDRAILS,
        "review_verdict": review.get("review_verdict", ""),
        "risk_level": review.get("risk_level", ""),
        "approved_next_stage": review.get("approved_next_stage", ""),
        "blockers": blockers,
        "warnings": warnings,
        "owner_questions": review.get("owner_questions", []),
        "reviewer_blocking_issues": [issue_line(item) for item in review.get("blocking_issues", [])],
        "reviewer_warnings": review.get("warnings", []),
        "required_checks": review.get("required_checks", []),
        "editor_brief_summary": review.get("brief_summary", ""),
        "first_screen_plan": review.get("first_screen_plan", ""),
        "exact_replacements": exact_replacements,
        "exact_replacements_count": len(exact_replacements),
        "proposed_backlog_item": proposed_backlog_item(review, scout_proposal, scout_opportunity),
        "source_artifacts": {
            "llm_review_latest": review,
            "stage_artifacts": review.get("stage_artifacts", {}),
        },
        "next_actions": [],
        "safety": "No content, backlog, manifest, PR, or production files were modified by this LLM intake bridge.",
    }
    intake["next_actions"] = next_actions_for(state, topic_id, f"automation/reports/llm-intake-{topic_id}.json")
    return intake


def render_markdown(intake: dict[str, Any]) -> str:
    backlog = intake["proposed_backlog_item"]
    backlog_lines = [f"{key}: `{value}`" for key, value in backlog.items()]
    lines = [
        f"# LLM Proposal Intake - {intake['source_topic_id']}",
        "",
        "## Status",
        "",
        f"- State: `{intake['state']}`",
        f"- Target: `{intake['target_page_or_slug']}`",
        f"- Review verdict: `{intake['review_verdict']}`",
        f"- Risk: `{intake['risk_level']}`",
        f"- Approved next stage: `{intake['approved_next_stage']}`",
        f"- Approved by: `{intake['approved_by'] or ''}`",
        f"- Approval scope: `{intake['approval_scope']}`",
        f"- Content edit approved: `{str(intake['content_edit_approved']).lower()}`",
        f"- Public content change allowed: `{str(intake['public_content_change_allowed']).lower()}`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified by this LLM intake bridge.",
        "",
        "## Approval Guardrails",
        "",
        md_list(intake["approval_guardrails"]),
        "",
        "## Blockers",
        "",
        md_list(intake["blockers"]),
        "",
        "## Warnings",
        "",
        md_list(intake["warnings"]),
        "",
        "## Owner Questions",
        "",
        md_list(intake["owner_questions"]),
        "",
        "## Reviewer Blocking Issues",
        "",
        md_list(intake["reviewer_blocking_issues"]),
        "",
        "## Reviewer Warnings",
        "",
        md_list(intake["reviewer_warnings"]),
        "",
        "## Proposed Backlog Item",
        "",
        md_list(backlog_lines),
        "",
        "## Editor Brief Summary",
        "",
        intake.get("editor_brief_summary", ""),
        "",
        "## First-Screen Plan",
        "",
        intake.get("first_screen_plan", ""),
        "",
        "## Draft Exact Replacements",
        "",
        f"- Count: `{intake.get('exact_replacements_count', 0)}`",
        "- Scope: proposal-only data; no public content edit is approved here.",
        "",
        "## Required Checks",
        "",
        md_list([f"`{check}`" for check in intake.get("required_checks", [])]),
        "",
        "## Next Actions",
        "",
        md_list(intake["next_actions"]),
        "",
    ]
    return "\n".join(lines)


def write_outputs(intake: dict[str, Any], output_dir: Path, basename: str | None) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = basename or f"llm-intake-{intake['source_topic_id']}"
    json_path = output_dir / f"{name}.json"
    md_path = output_dir / f"{name}.md"
    write_json(json_path, intake)
    md_path.write_text(render_markdown(intake), encoding="utf-8")
    return json_path, md_path


def run_llm_intake_latest(
    chain_path: Path,
    output_dir: Path,
    approved_by: str | None,
    note: str | None,
    basename: str | None,
    resolve_reviewer_blockers: bool,
) -> tuple[int, dict[str, Any]]:
    intake = build_intake(chain_path, approved_by, note, resolve_reviewer_blockers)
    json_path, md_path = write_outputs(intake, output_dir, basename)
    intake["next_actions"] = next_actions_for(intake["state"], intake["source_topic_id"], rel(json_path))
    write_json(json_path, intake)
    md_path.write_text(render_markdown(intake), encoding="utf-8")
    summary = {
        "source_topic_id": intake["source_topic_id"],
        "target_page_or_slug": intake["target_page_or_slug"],
        "state": intake["state"],
        "approved_by": intake["approved_by"],
        "json_path": rel(json_path),
        "markdown_path": rel(md_path),
        "next_actions": intake["next_actions"],
    }
    return (0 if intake["state"] != "blocked" else 1), summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a no-write intake artifact from the latest LLM worker chain.")
    parser.add_argument("--chain", help="Path to a specific llm-worker-chain-<topic_id>.json summary.")
    parser.add_argument("--reports-dir", default=str(REPORTS_DIR), help="Directory to search for LLM worker chain summaries.")
    parser.add_argument("--approved-by", help="Human approver name or handle.")
    parser.add_argument("--note", help="Optional approval note.")
    parser.add_argument(
        "--resolve-reviewer-blockers",
        action="store_true",
        help="Allow owner-confirmed Reviewer blocking issues to become intake warnings. Requires --approved-by and --note.",
    )
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for LLM intake artifacts.")
    parser.add_argument("--basename", help="Output basename without extension.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    reports_dir = resolve_path(args.reports_dir)
    output_dir = resolve_path(args.output_dir)
    chain_path = infer_chain_path(args.chain, reports_dir)
    code, summary = run_llm_intake_latest(
        chain_path=chain_path,
        output_dir=output_dir,
        approved_by=args.approved_by,
        note=args.note,
        basename=args.basename,
        resolve_reviewer_blockers=args.resolve_reviewer_blockers,
    )
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Topic: {summary['source_topic_id']}")
        print(f"State: {summary['state']}")
        print(f"Intake: {summary['markdown_path']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
