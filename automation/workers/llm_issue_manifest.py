#!/usr/bin/env python3
"""Ingest owner manifest approvals from GitHub owner handoff issue comments."""

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
from automation.workers import write_manifest
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


MANIFESTS_DIR = ROOT / "automation" / "manifests"
COMMANDS = {"/dry-run-manifest", "/approve-manifest"}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_command(comment_body: str) -> tuple[str, str, str] | None:
    body = comment_body.strip()
    if not body:
        return None
    first_line, _, remainder = body.partition("\n")
    parts = first_line.strip().split(maxsplit=2)
    if len(parts) < 2:
        return None
    command = parts[0].strip().lower()
    if command not in COMMANDS:
        return None
    topic_id = parts[1].strip()
    inline_note = parts[2].strip() if len(parts) == 3 else ""
    note = "\n".join(part for part in (inline_note, remainder.strip()) if part).strip()
    return command, topic_id, note


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
        errors.append("No supported owner manifest command found. Use /dry-run-manifest or /approve-manifest.")
        return 1, {
            "command": "",
            "topic_id": "",
            "approved_by": author,
            "approval_note": "",
            "errors": errors,
        }

    command, topic_id, note = parsed
    if not TOPIC_ID_PATTERN.match(topic_id):
        errors.append(f"Unsafe or unsupported topic id: {topic_id}")
    if not note:
        errors.append("Manifest approval note is required after the topic id.")
    if "<" in note or ">" in note:
        errors.append("Manifest approval note still contains placeholder brackets; replace placeholders with a real owner note.")

    return (1 if errors else 0), {
        "command": command,
        "topic_id": topic_id,
        "approved_by": author,
        "approval_note": note,
        "errors": errors,
    }


def run_plan_candidates(topic_id: str, reports_dir: Path, explicit_run_plan: Path | None) -> list[Path]:
    candidates: list[Path] = []
    if explicit_run_plan:
        candidates.append(explicit_run_plan)
    candidates.extend(
        [
            reports_dir / f"llm-worker-run-plan-{topic_id}.json",
            reports_dir / f"worker-run-plan-{topic_id}.json",
            reports_dir / "llm-owner-run-plan-gha" / f"llm-worker-run-plan-{topic_id}.json",
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


def find_run_plan(topic_id: str, reports_dir: Path, explicit_run_plan: Path | None) -> tuple[Path | None, list[str]]:
    checked: list[str] = []
    for candidate in run_plan_candidates(topic_id, reports_dir, explicit_run_plan):
        checked.append(rel(candidate))
        if not candidate.exists():
            continue
        try:
            payload = load_json(candidate)
        except Exception:
            continue
        if payload.get("report_type") != "worker_intake_run_plan":
            continue
        if str(payload.get("source_topic_id") or "") != topic_id:
            continue
        return candidate, checked
    return None, checked


def build_summary(
    validation: dict[str, Any],
    manifest_summary: dict[str, Any] | None,
    run_plan_path: Path | None,
    checked_run_plans: list[str],
    issue_title: str,
    author_association: str,
) -> dict[str, Any]:
    errors = list(validation.get("errors", []))
    if manifest_summary:
        errors.extend(str(item) for item in manifest_summary.get("errors", []))
    if not run_plan_path and not errors:
        errors.append("No matching run-plan artifact was found for this topic.")
    command = validation.get("command", "")
    expected_state = "dry_run_ready" if command == "/dry-run-manifest" else "manifest_created"
    state = "manifest_dry_run_ready" if manifest_summary and manifest_summary.get("state") == "dry_run_ready" and not errors else "blocked"
    if command == "/approve-manifest" and manifest_summary and manifest_summary.get("state") == "manifest_created" and not errors:
        state = "manifest_created"
    return {
        "schema_version": 1,
        "report_type": "llm_issue_manifest",
        "generated_at": now_utc(),
        "state": state,
        "issue_title": issue_title,
        "comment_author": validation.get("approved_by", ""),
        "author_association": author_association,
        "command": command,
        "topic_id": validation.get("topic_id", ""),
        "approval_note": validation.get("approval_note", ""),
        "source_run_plan": rel(run_plan_path) if run_plan_path else "",
        "checked_run_plans": checked_run_plans,
        "manifest_command_state": manifest_summary.get("state", "") if manifest_summary else "",
        "expected_manifest_state": expected_state,
        "run_id": manifest_summary.get("run_id", "") if manifest_summary else "",
        "manifest_path": manifest_summary.get("manifest_path", "") if manifest_summary else "",
        "dry_run": bool(manifest_summary.get("dry_run", False)) if manifest_summary else command == "/dry-run-manifest",
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_creation": command == "/approve-manifest" and state == "manifest_created",
        "errors": errors,
        "next_actions": next_actions(validation, manifest_summary, errors),
        "safety": "No public content, backlog, PR, or production files were modified. /approve-manifest may create only a planned run manifest.",
    }


def next_actions(
    validation: dict[str, Any],
    manifest_summary: dict[str, Any] | None,
    errors: list[str],
) -> list[str]:
    topic_id = validation.get("topic_id", "")
    if errors:
        return [
            "Fix the GitHub issue comment command or make sure a run-plan artifact exists for the topic.",
            "Use /approve-run-plan first if no run-plan artifact has been recorded for this topic.",
            f"Then use: /dry-run-manifest {topic_id or '<topic_id>'} <owner confirms manifest scope>.",
        ]
    if validation.get("command") == "/dry-run-manifest" and manifest_summary:
        return [
            "Review the dry-run manifest path before creating the planned manifest.",
            f"Use: /approve-manifest {topic_id} <owner confirms planned manifest creation>",
            "Do not write public content until a later proposal artifact receives explicit owner approval.",
        ]
    if manifest_summary:
        run_id = manifest_summary.get("run_id", "<run_id>")
        return [
            "Review the planned manifest before running review/brief/patch-plan.",
            f"Use: /review-run {run_id} <owner confirms deterministic review>",
            "Do not write public content until a later proposal artifact receives explicit owner approval.",
        ]
    return []


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# LLM Issue Manifest - {summary.get('topic_id', '') or 'blocked'}",
        "",
        "## Result",
        "",
        f"- State: `{summary.get('state', '')}`",
        f"- Command: `{summary.get('command', '')}`",
        f"- Topic: `{summary.get('topic_id', '')}`",
        f"- Comment author: `{summary.get('comment_author', '')}`",
        f"- Author association: `{summary.get('author_association', '')}`",
        f"- Source run-plan: `{summary.get('source_run_plan', '')}`",
        f"- Manifest command state: `{summary.get('manifest_command_state', '')}`",
        f"- Run ID: `{summary.get('run_id', '')}`",
        f"- Manifest path: `{summary.get('manifest_path', '')}`",
        f"- Dry run: `{str(summary.get('dry_run', False)).lower()}`",
        f"- Allows content edit: `{str(summary.get('allows_content_edit', False)).lower()}`",
        f"- Allows backlog mutation: `{str(summary.get('allows_backlog_mutation', False)).lower()}`",
        f"- Allows manifest creation: `{str(summary.get('allows_manifest_creation', False)).lower()}`",
        "- Safety: no public content, backlog, PR, or production files were modified.",
        "",
    ]
    if summary.get("approval_note"):
        lines.extend(["Approval note:", "", summary["approval_note"], ""])
    if summary.get("checked_run_plans"):
        lines.extend(["## Checked Run Plans", "", md_list([f"`{item}`" for item in summary["checked_run_plans"]]), ""])
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


def run_issue_manifest(
    comment_body: str,
    comment_author: str | None,
    author_association: str | None,
    issue_title: str,
    reports_dir: Path,
    run_plan_path: Path | None,
    manifest_dir: Path,
    summary_output: Path | None,
    markdown_output: Path | None,
) -> tuple[int, dict[str, Any]]:
    author = normalize_author(comment_author)
    association = normalize_association(author_association)
    validation_code, validation = validate_command(issue_title, comment_body, author, association)
    manifest_summary: dict[str, Any] | None = None
    selected_run_plan: Path | None = None
    checked_run_plans: list[str] = []
    code = validation_code
    if validation_code == 0:
        selected_run_plan, checked_run_plans = find_run_plan(validation["topic_id"], reports_dir, run_plan_path)
        if selected_run_plan:
            try:
                dry_run = validation["command"] == "/dry-run-manifest"
                code, manifest_summary = write_manifest.write_manifest(
                    run_plan_path=selected_run_plan,
                    manifest_dir=manifest_dir,
                    created_by=author,
                    dry_run=dry_run,
                )
            except Exception as exc:
                validation["errors"].append(f"Failed to process planned manifest: {exc}")
                code = 1
        else:
            code = 1
    summary = build_summary(validation, manifest_summary, selected_run_plan, checked_run_plans, issue_title, association)
    write_optional_outputs(summary, summary_output, markdown_output)
    return code, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Record manifest approval from a GitHub owner issue comment.")
    parser.add_argument("--comment-body", required=True, help="Raw GitHub issue comment body.")
    parser.add_argument("--comment-author", help="GitHub login for the comment author.")
    parser.add_argument("--author-association", help="GitHub author association, such as OWNER or COLLABORATOR.")
    parser.add_argument("--issue-title", default=DEFAULT_ISSUE_TITLE, help="GitHub issue title the comment was posted on.")
    parser.add_argument("--reports-dir", default=str(REPORTS_DIR), help="Directory to search for run-plan artifacts.")
    parser.add_argument("--run-plan", help="Optional explicit llm-worker-run-plan-<topic_id>.json path.")
    parser.add_argument("--manifest-dir", default=str(MANIFESTS_DIR), help="Directory where planned manifests are written.")
    parser.add_argument("--summary-output", help="Optional JSON summary output path.")
    parser.add_argument("--markdown-output", help="Optional markdown summary output path.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, summary = run_issue_manifest(
        comment_body=args.comment_body,
        comment_author=args.comment_author,
        author_association=args.author_association,
        issue_title=args.issue_title,
        reports_dir=resolve_path(args.reports_dir),
        run_plan_path=resolve_path(args.run_plan) if args.run_plan else None,
        manifest_dir=resolve_path(args.manifest_dir),
        summary_output=resolve_path(args.summary_output) if args.summary_output else None,
        markdown_output=resolve_path(args.markdown_output) if args.markdown_output else None,
    )
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Topic: {summary['topic_id']}")
        print(f"Manifest: {summary['manifest_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
