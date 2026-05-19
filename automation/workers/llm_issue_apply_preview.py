#!/usr/bin/env python3
"""Render no-write apply preview from GitHub issue comments."""

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

from automation import apply_preview
from automation.io import load_run_manifest, write_json
from automation.proposal_renderer import md_list
from automation.workers.llm_issue_decision import (
    ALLOWED_ASSOCIATIONS,
    DEFAULT_ISSUE_TITLE,
    normalize_association,
    normalize_author,
    rel,
    resolve_path,
)


MANIFESTS_DIR = ROOT / "automation" / "manifests"
REPORTS_DIR = ROOT / "automation" / "reports"
COMMAND = "/preview-apply"
RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,180}$")
PREVIEWABLE_STATUSES = {"approved_for_apply", "apply_preview_ready"}


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
    run_id = parts[1].strip()
    inline_note = parts[2].strip() if len(parts) == 3 else ""
    note = "\n".join(part for part in (inline_note, remainder.strip()) if part).strip()
    return run_id, note


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
        errors.append("No supported apply preview command found. Use /preview-apply <run_id> <owner note>.")
        return 1, {
            "command": "",
            "run_id": "",
            "approved_by": author,
            "approval_note": "",
            "errors": errors,
        }

    run_id, note = parsed
    if not RUN_ID_PATTERN.match(run_id):
        errors.append(f"Unsafe or unsupported run id: {run_id}")
    if not note:
        errors.append("Apply preview note is required after the run id.")
    if "<" in note or ">" in note:
        errors.append("Apply preview note still contains placeholder brackets; replace placeholders with a real owner note.")

    return (1 if errors else 0), {
        "command": COMMAND,
        "run_id": run_id,
        "approved_by": author,
        "approval_note": note,
        "errors": errors,
    }


def manifest_path_for(run_id: str, manifest_dir: Path, explicit_manifest: Path | None) -> Path:
    if explicit_manifest:
        return explicit_manifest
    return manifest_dir / f"{run_id}.json"


def render_preview(
    validation: dict[str, Any],
    manifest_dir: Path,
    manifest_path: Path | None,
    output_dir: Path,
) -> tuple[int, dict[str, Any] | None, list[str]]:
    errors = validation["errors"]
    run_id = validation.get("run_id", "")
    if errors:
        return 1, None, errors

    selected_manifest = manifest_path_for(run_id, manifest_dir, manifest_path)
    if not selected_manifest.exists():
        return 1, None, [f"Manifest does not exist: {rel(selected_manifest)}"]

    try:
        manifest = load_run_manifest(selected_manifest)
    except Exception as exc:
        return 1, None, [f"Failed to load manifest: {exc}"]

    before_status = manifest.status
    if before_status not in PREVIEWABLE_STATUSES:
        return 1, None, [
            "Manifest status must be `approved_for_apply` or `apply_preview_ready` "
            f"before /preview-apply; current status is `{before_status}`."
        ]

    try:
        preview_path, preview_items = apply_preview.render_apply_preview(selected_manifest, output_dir)
    except Exception as exc:
        return 1, None, [f"Failed to render apply preview: {exc}"]

    refreshed_manifest = load_run_manifest(selected_manifest)
    warning_count = sum(len(item.get("warnings", [])) for item in preview_items)
    return 0, {
        "run_id": refreshed_manifest.run_id,
        "manifest_path": rel(selected_manifest),
        "before_status": before_status,
        "after_status": refreshed_manifest.status,
        "preview_markdown": rel(preview_path),
        "approved_specs_count": len(preview_items),
        "preview_warning_count": warning_count,
        "already_preview_ready": before_status == "apply_preview_ready",
        "manifest_ready_for_apply_approved": refreshed_manifest.status == "apply_preview_ready",
    }, []


def next_actions(summary: dict[str, Any]) -> list[str]:
    run_id = summary.get("run_id", "") or "<run_id>"
    if summary.get("errors"):
        return [
            "Fix the GitHub issue command, manifest path, manifest status, or approved specs, then post a new owner command.",
            "Apply preview requires approved proposal specs and does not apply content.",
        ]
    return [
        f"Review the apply preview report: {summary.get('preview_markdown', '')}",
        f"Only after owner review, run content apply locally: python3 automation/pipeline.py apply-approved {run_id}",
        "Public content is still unchanged until apply-approved and strict QA pass.",
    ]


def build_summary(
    validation: dict[str, Any],
    preview_result: dict[str, Any] | None,
    preview_errors: list[str],
    issue_title: str,
    author_association: str,
) -> dict[str, Any]:
    errors = list(validation.get("errors", []))
    errors.extend(preview_errors)
    run_id = preview_result.get("run_id", validation.get("run_id", "")) if preview_result else validation.get("run_id", "")
    state = "apply_preview_ready" if preview_result and not errors else "blocked"
    if preview_result and preview_result.get("already_preview_ready") and not errors:
        state = "apply_preview_refreshed"
    summary = {
        "schema_version": 1,
        "report_type": "llm_issue_apply_preview",
        "generated_at": now_utc(),
        "state": state,
        "issue_title": issue_title,
        "comment_author": validation.get("approved_by", ""),
        "author_association": author_association,
        "command": validation.get("command", ""),
        "run_id": run_id,
        "approval_note": validation.get("approval_note", ""),
        "manifest_path": preview_result.get("manifest_path", "") if preview_result else "",
        "before_status": preview_result.get("before_status", "") if preview_result else "",
        "after_status": preview_result.get("after_status", "") if preview_result else "",
        "preview_markdown": preview_result.get("preview_markdown", "") if preview_result else "",
        "approved_specs_count": preview_result.get("approved_specs_count", 0) if preview_result else 0,
        "preview_warning_count": preview_result.get("preview_warning_count", 0) if preview_result else 0,
        "manifest_ready_for_apply_approved": bool(
            preview_result and preview_result.get("manifest_ready_for_apply_approved") and not errors
        ),
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": bool(preview_result and not errors),
        "runs_apply_approved": False,
        "allows_pr_creation": False,
        "allows_deploy": False,
        "errors": errors,
        "safety": "No public content, backlog, PR, or production files were modified. This command only renders a no-write apply preview.",
    }
    summary["next_actions"] = next_actions(summary)
    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# LLM Issue Apply Preview - {summary.get('run_id', '') or 'blocked'}",
        "",
        "## Result",
        "",
        f"- State: `{summary.get('state', '')}`",
        f"- Command: `{summary.get('command', '')}`",
        f"- Run ID: `{summary.get('run_id', '')}`",
        f"- Comment author: `{summary.get('comment_author', '')}`",
        f"- Author association: `{summary.get('author_association', '')}`",
        f"- Manifest path: `{summary.get('manifest_path', '')}`",
        f"- Before status: `{summary.get('before_status', '')}`",
        f"- After status: `{summary.get('after_status', '')}`",
        f"- Preview report: `{summary.get('preview_markdown', '')}`",
        f"- Approved specs: `{summary.get('approved_specs_count', 0)}`",
        f"- Preview warnings: `{summary.get('preview_warning_count', 0)}`",
        f"- Manifest ready for apply-approved: `{str(summary.get('manifest_ready_for_apply_approved', False)).lower()}`",
        f"- Allows content edit: `{str(summary.get('allows_content_edit', False)).lower()}`",
        f"- Runs apply-approved: `{str(summary.get('runs_apply_approved', False)).lower()}`",
        f"- Allows manifest mutation: `{str(summary.get('allows_manifest_mutation', False)).lower()}`",
        f"- Allows PR creation: `{str(summary.get('allows_pr_creation', False)).lower()}`",
        f"- Allows deploy: `{str(summary.get('allows_deploy', False)).lower()}`",
        "- Safety: no public content, backlog, PR, or production files were modified.",
        "",
    ]
    if summary.get("approval_note"):
        lines.extend(["Owner note:", "", summary["approval_note"], ""])
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


def run_issue_apply_preview(
    comment_body: str,
    comment_author: str | None,
    author_association: str | None,
    issue_title: str,
    manifest_dir: Path,
    manifest_path: Path | None,
    output_dir: Path,
    summary_output: Path | None,
    markdown_output: Path | None,
) -> tuple[int, dict[str, Any]]:
    author = normalize_author(comment_author)
    association = normalize_association(author_association)
    validation_code, validation = validate_command(issue_title, comment_body, author, association)
    preview_result: dict[str, Any] | None = None
    preview_errors: list[str] = []
    code = validation_code
    if validation_code == 0:
        code, preview_result, preview_errors = render_preview(validation, manifest_dir, manifest_path, output_dir)
    summary = build_summary(validation, preview_result, preview_errors, issue_title, association)
    write_optional_outputs(summary, summary_output, markdown_output)
    return code, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Render apply preview from a GitHub owner issue comment.")
    parser.add_argument("--comment-body", required=True, help="Raw GitHub issue comment body.")
    parser.add_argument("--comment-author", help="GitHub login for the comment author.")
    parser.add_argument("--author-association", help="GitHub author association, such as OWNER or COLLABORATOR.")
    parser.add_argument("--issue-title", default=DEFAULT_ISSUE_TITLE, help="GitHub issue title the comment was posted on.")
    parser.add_argument("--manifest-dir", default=str(MANIFESTS_DIR), help="Directory where manifests are stored.")
    parser.add_argument("--manifest", help="Optional explicit run manifest path.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for apply preview artifacts.")
    parser.add_argument("--summary-output", help="Optional JSON summary output path.")
    parser.add_argument("--markdown-output", help="Optional markdown summary output path.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, summary = run_issue_apply_preview(
        comment_body=args.comment_body,
        comment_author=args.comment_author,
        author_association=args.author_association,
        issue_title=args.issue_title,
        manifest_dir=resolve_path(args.manifest_dir),
        manifest_path=resolve_path(args.manifest) if args.manifest else None,
        output_dir=resolve_path(args.output_dir),
        summary_output=resolve_path(args.summary_output) if args.summary_output else None,
        markdown_output=resolve_path(args.markdown_output) if args.markdown_output else None,
    )
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Run ID: {summary['run_id']}")
        print(f"Manifest: {summary['manifest_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
