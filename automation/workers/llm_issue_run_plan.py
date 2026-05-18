#!/usr/bin/env python3
"""Ingest owner run-plan approvals from GitHub owner handoff issue comments."""

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
from automation.workers import intake_to_run
from automation.workers.llm_issue_decision import (
    ALLOWED_ASSOCIATIONS,
    DEFAULT_ISSUE_TITLE,
    REPORTS_DIR,
    TOPIC_ID_PATTERN,
    normalize_association,
    normalize_author,
    rel,
    resolve_path,
)


COMMAND = "/approve-run-plan"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_command(comment_body: str) -> tuple[str, str] | None:
    body = comment_body.strip()
    if not body:
        return None
    first_line, _, remainder = body.partition("\n")
    parts = first_line.strip().split(maxsplit=2)
    if len(parts) < 2:
        return None
    command = parts[0].strip().lower()
    if command != COMMAND:
        return None
    topic_id = parts[1].strip()
    inline_note = parts[2].strip() if len(parts) == 3 else ""
    note = "\n".join(part for part in (inline_note, remainder.strip()) if part).strip()
    return topic_id, note


def validate_command(
    issue_title: str,
    comment_body: str,
    author: str,
    author_association: str,
) -> tuple[int, dict[str, Any]]:
    errors: list[str] = []
    parsed = parse_command(comment_body)
    if issue_title != DEFAULT_ISSUE_TITLE:
        errors.append(f"Unsupported issue title: {issue_title}")
    if author_association not in ALLOWED_ASSOCIATIONS:
        errors.append(f"Unsupported comment author association: {author_association or 'unknown'}")
    if not parsed:
        errors.append("No supported owner run-plan command found. Use /approve-run-plan <topic_id> <owner note>.")
        return 1, {
            "command": "",
            "topic_id": "",
            "approved_by": author,
            "approval_note": "",
            "errors": errors,
        }

    topic_id, note = parsed
    if not TOPIC_ID_PATTERN.match(topic_id):
        errors.append(f"Unsafe or unsupported topic id: {topic_id}")
    if not note:
        errors.append("Run-plan approval note is required after the topic id.")
    if "<" in note or ">" in note:
        errors.append("Run-plan approval note still contains placeholder brackets; replace placeholders with a real owner note.")

    return (1 if errors else 0), {
        "command": COMMAND,
        "topic_id": topic_id,
        "approved_by": author,
        "approval_note": note,
        "errors": errors,
    }


def intake_candidates(topic_id: str, reports_dir: Path, explicit_intake: Path | None) -> list[Path]:
    candidates: list[Path] = []
    if explicit_intake:
        candidates.append(explicit_intake)
    candidates.extend(
        [
            reports_dir / f"llm-intake-{topic_id}.json",
            reports_dir / f"worker-intake-{topic_id}.json",
            reports_dir / "llm-worker-chain-gha" / f"llm-intake-{topic_id}.json",
        ]
    )
    deduped: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved not in seen:
            seen.add(resolved)
            deduped.append(candidate)
    return deduped


def find_intake(topic_id: str, reports_dir: Path, explicit_intake: Path | None) -> tuple[Path | None, list[str]]:
    checked: list[str] = []
    for candidate in intake_candidates(topic_id, reports_dir, explicit_intake):
        checked.append(rel(candidate))
        if not candidate.exists():
            continue
        try:
            payload = load_json(candidate)
        except Exception:
            continue
        if payload.get("report_type") not in {"llm_worker_proposal_intake", "worker_proposal_intake"}:
            continue
        if str(payload.get("source_topic_id") or "") != topic_id:
            continue
        return candidate, checked
    return None, checked


def build_summary(
    validation: dict[str, Any],
    run_plan_summary: dict[str, Any] | None,
    intake_path: Path | None,
    checked_intakes: list[str],
    issue_title: str,
    author_association: str,
) -> dict[str, Any]:
    errors = list(validation.get("errors", []))
    if run_plan_summary and run_plan_summary.get("state") == "blocked":
        errors.append("Worker run-plan artifact is blocked; inspect the run-plan report before continuing.")
    if not intake_path and not errors:
        errors.append("No matching approved LLM intake artifact was found for this topic.")
    state = "run_plan_recorded" if run_plan_summary and run_plan_summary.get("state") == "run_plan_ready" and not errors else "blocked"
    return {
        "schema_version": 1,
        "report_type": "llm_issue_run_plan",
        "generated_at": now_utc(),
        "state": state,
        "issue_title": issue_title,
        "comment_author": validation.get("approved_by", ""),
        "author_association": author_association,
        "command": validation.get("command", ""),
        "topic_id": validation.get("topic_id", ""),
        "approval_note": validation.get("approval_note", ""),
        "source_intake": rel(intake_path) if intake_path else "",
        "checked_intakes": checked_intakes,
        "run_plan_state": run_plan_summary.get("state", "") if run_plan_summary else "",
        "run_plan_output_path": run_plan_summary.get("json_path", "") if run_plan_summary else "",
        "run_plan_markdown_path": run_plan_summary.get("markdown_path", "") if run_plan_summary else "",
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_creation": False,
        "errors": errors,
        "next_actions": next_actions(validation, run_plan_summary, errors),
        "safety": "No content, backlog, manifest, PR, or production files were modified. This command only creates a no-write run-plan proposal from an approved intake artifact.",
    }


def next_actions(
    validation: dict[str, Any],
    run_plan_summary: dict[str, Any] | None,
    errors: list[str],
) -> list[str]:
    topic_id = validation.get("topic_id", "")
    if errors:
        return [
            "Fix the GitHub issue comment command or make sure an approved intake artifact exists for the topic.",
            "Use /approve-intake first if no approved intake artifact has been recorded for this topic.",
            f"Then use: /approve-run-plan {topic_id or '<topic_id>'} <owner confirms run-plan scope>.",
        ]
    if run_plan_summary:
        return [
            "Review the committed run-plan artifact before creating a planned manifest.",
            f"Run: python3 automation/pipeline.py worker-manifest --run-plan {run_plan_summary.get('json_path')} --created-by <name> --dry-run --json",
            "Do not write public content until a later proposal artifact receives explicit owner approval.",
        ]
    return []


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# LLM Issue Run Plan - {summary.get('topic_id', '') or 'blocked'}",
        "",
        "## Result",
        "",
        f"- State: `{summary.get('state', '')}`",
        f"- Command: `{summary.get('command', '')}`",
        f"- Topic: `{summary.get('topic_id', '')}`",
        f"- Comment author: `{summary.get('comment_author', '')}`",
        f"- Author association: `{summary.get('author_association', '')}`",
        f"- Source intake: `{summary.get('source_intake', '')}`",
        f"- Run-plan state: `{summary.get('run_plan_state', '')}`",
        f"- Run-plan artifact: `{summary.get('run_plan_output_path', '')}`",
        f"- Allows content edit: `{str(summary.get('allows_content_edit', False)).lower()}`",
        f"- Allows backlog mutation: `{str(summary.get('allows_backlog_mutation', False)).lower()}`",
        f"- Allows manifest creation: `{str(summary.get('allows_manifest_creation', False)).lower()}`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if summary.get("approval_note"):
        lines.extend(["Approval note:", "", summary["approval_note"], ""])
    if summary.get("checked_intakes"):
        lines.extend(["## Checked Intakes", "", md_list([f"`{item}`" for item in summary["checked_intakes"]]), ""])
    if summary.get("errors"):
        lines.extend(["## Errors", "", md_list(summary["errors"]), ""])
    lines.extend(["## Next Actions", "", md_list(summary.get("next_actions", [])), ""])
    return "\n".join(lines)


def write_optional_outputs(summary: dict[str, Any], summary_output: Path | None, markdown_output: Path | None) -> None:
    if summary_output:
        write_json(summary_output, summary)
    if markdown_output:
        markdown_output.parent.mkdir(parents=True, exist_ok=True)
        markdown_output.write_text(render_markdown(summary), encoding="utf-8")


def run_issue_run_plan(
    comment_body: str,
    comment_author: str | None,
    author_association: str | None,
    issue_title: str,
    reports_dir: Path,
    intake_path: Path | None,
    output_dir: Path,
    summary_output: Path | None,
    markdown_output: Path | None,
) -> tuple[int, dict[str, Any]]:
    author = normalize_author(comment_author)
    association = normalize_association(author_association)
    validation_code, validation = validate_command(issue_title, comment_body, author, association)
    run_plan_summary: dict[str, Any] | None = None
    selected_intake: Path | None = None
    checked_intakes: list[str] = []
    code = validation_code
    if validation_code == 0:
        selected_intake, checked_intakes = find_intake(validation["topic_id"], reports_dir, intake_path)
        if selected_intake:
            try:
                intake = load_json(selected_intake)
                proposal = intake_to_run.build_proposal(intake, selected_intake)
                proposal["owner_run_plan_approval"] = {
                    "approved_by": author,
                    "approval_note": validation["approval_note"],
                    "approval_scope": "run_plan_only_no_content_edits",
                    "content_edit_approved": False,
                    "manifest_creation_approved": False,
                    "recorded_at": now_utc(),
                }
                json_path, md_path = intake_to_run.write_outputs(
                    proposal,
                    output_dir,
                    f"llm-worker-run-plan-{validation['topic_id']}",
                )
                run_plan_summary = {
                    "source_topic_id": proposal["source_topic_id"],
                    "target_page_or_slug": proposal["target_page_or_slug"],
                    "state": proposal["state"],
                    "json_path": rel(json_path),
                    "markdown_path": rel(md_path),
                }
                code = 0 if proposal["state"] == "run_plan_ready" else 1
            except Exception as exc:
                validation["errors"].append(f"Failed to build Worker run-plan: {exc}")
                code = 1
        else:
            code = 1
    summary = build_summary(validation, run_plan_summary, selected_intake, checked_intakes, issue_title, association)
    write_optional_outputs(summary, summary_output, markdown_output)
    return code, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Record run-plan approval from a GitHub owner issue comment.")
    parser.add_argument("--comment-body", required=True, help="Raw GitHub issue comment body.")
    parser.add_argument("--comment-author", help="GitHub login for the comment author.")
    parser.add_argument("--author-association", help="GitHub author association, such as OWNER or COLLABORATOR.")
    parser.add_argument("--issue-title", default=DEFAULT_ISSUE_TITLE, help="GitHub issue title the comment was posted on.")
    parser.add_argument("--reports-dir", default=str(REPORTS_DIR), help="Directory to search for intake artifacts.")
    parser.add_argument("--intake", help="Optional explicit llm-intake-<topic_id>.json path.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for run-plan artifacts.")
    parser.add_argument("--summary-output", help="Optional JSON summary output path.")
    parser.add_argument("--markdown-output", help="Optional markdown summary output path.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, summary = run_issue_run_plan(
        comment_body=args.comment_body,
        comment_author=args.comment_author,
        author_association=args.author_association,
        issue_title=args.issue_title,
        reports_dir=resolve_path(args.reports_dir),
        intake_path=resolve_path(args.intake) if args.intake else None,
        output_dir=resolve_path(args.output_dir),
        summary_output=resolve_path(args.summary_output) if args.summary_output else None,
        markdown_output=resolve_path(args.markdown_output) if args.markdown_output else None,
    )
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Topic: {summary['topic_id']}")
        print(f"Run plan: {summary['run_plan_output_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
