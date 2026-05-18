#!/usr/bin/env python3
"""Record owner approval for rendered proposal specs from GitHub issue comments."""

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

from automation import exact_proposals, proposal_renderer
from automation.approval import compute_status, update_spec
from automation.io import load_run_manifest, write_json, write_run_manifest
from automation.proposal_renderer import SAFE_EXACT_REPLACE_OPERATION, md_list
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
COMMAND = "/approve-proposal"
RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,180}$")
APPROVABLE_STATUSES = {"proposal_ready", "partially_approved", "approved_for_apply"}


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
        errors.append("No supported owner proposal approval command found. Use /approve-proposal <run_id> <owner note>.")
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
        errors.append("Proposal approval note is required after the run id.")
    if "<" in note or ">" in note:
        errors.append("Proposal approval note still contains placeholder brackets; replace placeholders with a real owner note.")

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


def proposal_counts(rendered_specs: list[dict[str, Any]]) -> dict[str, int]:
    exact_count = sum(1 for spec in rendered_specs if spec.get("operation_type") == SAFE_EXACT_REPLACE_OPERATION)
    return {
        "rendered_spec_count": len(rendered_specs),
        "exact_spec_count": exact_count,
        "non_exact_spec_count": len(rendered_specs) - exact_count,
    }


def approve_specs(
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
    if before_status not in APPROVABLE_STATUSES:
        return 1, None, [
            "Manifest status must be `proposal_ready`, `partially_approved`, or `approved_for_apply` "
            f"before /approve-proposal; current status is `{before_status}`."
        ]

    artifacts = manifest.artifacts or {}
    proposal = artifacts.get("proposal", {})
    patch_plan = artifacts.get("patch_plan", {})
    rendered_specs = proposal.get("rendered_specs", [])
    patch_specs = patch_plan.get("patch_specs", [])
    if not rendered_specs:
        return 1, None, ["No rendered proposal specs found. Run /propose-run before /approve-proposal."]

    counts = proposal_counts(rendered_specs)
    timestamp = now_utc()
    note = validation.get("approval_note", "")
    rendered_already_approved = all(str(spec.get("approval_state") or "proposed") == "approved" for spec in rendered_specs)
    patch_already_approved = all(str(spec.get("approval_state") or "proposed") == "approved" for spec in patch_specs)
    already_approved = rendered_already_approved and patch_already_approved

    if not already_approved:
        for spec in rendered_specs:
            update_spec(spec, "approved", note, timestamp)
        for spec in patch_specs:
            update_spec(spec, "approved", note, timestamp)

        states = [str(spec.get("approval_state") or "proposed") for spec in rendered_specs]
        manifest.status = compute_status(states, manifest.status)
        proposal["rendered_specs"] = rendered_specs
        artifacts["proposal"] = proposal
        artifacts["patch_plan"] = patch_plan
        manifest.artifacts = artifacts
        write_run_manifest(selected_manifest, manifest)

    proposal_path, refreshed_specs = proposal_renderer.render_proposal(selected_manifest, output_dir)
    exact_review = exact_proposals.render_exact_proposals(selected_manifest, output_dir)
    refreshed_manifest = load_run_manifest(selected_manifest)

    return 0, {
        "run_id": refreshed_manifest.run_id,
        "manifest_path": rel(selected_manifest),
        "before_status": before_status,
        "after_status": refreshed_manifest.status,
        "already_approved": already_approved,
        "approval_state": "approved",
        "approved_spec_count": len(rendered_specs),
        "rendered_spec_count": len(refreshed_specs),
        "exact_spec_count": counts["exact_spec_count"],
        "non_exact_spec_count": counts["non_exact_spec_count"],
        "proposal_markdown": rel(proposal_path),
        "exact_proposal_json": exact_review.get("report_paths", {}).get("json", ""),
        "exact_proposal_markdown": exact_review.get("report_paths", {}).get("markdown", ""),
    }, []


def next_actions(summary: dict[str, Any]) -> list[str]:
    run_id = summary.get("run_id", "") or "<run_id>"
    if summary.get("errors"):
        return [
            "Fix the GitHub issue command, manifest path, or manifest status, then post a new owner command.",
            "Proposal approval requires a prior /propose-run artifact and does not apply content.",
        ]
    return [
        f"Review approved proposal artifacts, then run apply preview locally: python3 automation/pipeline.py apply-preview {run_id}",
        "Do not run apply-approved until apply-preview output is reviewed and the owner confirms the exact content change.",
        "Public content is still unchanged until apply-approved and strict QA pass.",
    ]


def build_summary(
    validation: dict[str, Any],
    approval_result: dict[str, Any] | None,
    approval_errors: list[str],
    issue_title: str,
    author_association: str,
) -> dict[str, Any]:
    errors = list(validation.get("errors", []))
    errors.extend(approval_errors)
    run_id = approval_result.get("run_id", validation.get("run_id", "")) if approval_result else validation.get("run_id", "")
    state = "proposal_approved" if approval_result and not errors else "blocked"
    if approval_result and approval_result.get("already_approved") and not errors:
        state = "proposal_already_approved"
    summary = {
        "schema_version": 1,
        "report_type": "llm_issue_proposal_approval",
        "generated_at": now_utc(),
        "state": state,
        "issue_title": issue_title,
        "comment_author": validation.get("approved_by", ""),
        "author_association": author_association,
        "command": validation.get("command", ""),
        "run_id": run_id,
        "approval_note": validation.get("approval_note", ""),
        "manifest_path": approval_result.get("manifest_path", "") if approval_result else "",
        "before_status": approval_result.get("before_status", "") if approval_result else "",
        "after_status": approval_result.get("after_status", "") if approval_result else "",
        "approved_spec_count": approval_result.get("approved_spec_count", 0) if approval_result else 0,
        "rendered_spec_count": approval_result.get("rendered_spec_count", 0) if approval_result else 0,
        "exact_spec_count": approval_result.get("exact_spec_count", 0) if approval_result else 0,
        "non_exact_spec_count": approval_result.get("non_exact_spec_count", 0) if approval_result else 0,
        "proposal_markdown": approval_result.get("proposal_markdown", "") if approval_result else "",
        "exact_proposal_json": approval_result.get("exact_proposal_json", "") if approval_result else "",
        "exact_proposal_markdown": approval_result.get("exact_proposal_markdown", "") if approval_result else "",
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": bool(approval_result and not errors),
        "allows_apply_preview": bool(approval_result and not errors),
        "allows_apply_approved": False,
        "allows_pr_creation": False,
        "allows_deploy": False,
        "errors": errors,
        "safety": "No public content, backlog, PR, or production files were modified. This command only records owner approval on proposal specs.",
    }
    summary["next_actions"] = next_actions(summary)
    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# LLM Issue Proposal Approval - {summary.get('run_id', '') or 'blocked'}",
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
        f"- Approved specs: `{summary.get('approved_spec_count', 0)}`",
        f"- Exact specs: `{summary.get('exact_spec_count', 0)}`",
        f"- Non-exact specs: `{summary.get('non_exact_spec_count', 0)}`",
        f"- Proposal report: `{summary.get('proposal_markdown', '')}`",
        f"- Exact proposal review: `{summary.get('exact_proposal_markdown', '')}`",
        f"- Allows content edit: `{str(summary.get('allows_content_edit', False)).lower()}`",
        f"- Allows apply-preview: `{str(summary.get('allows_apply_preview', False)).lower()}`",
        f"- Allows apply-approved: `{str(summary.get('allows_apply_approved', False)).lower()}`",
        f"- Allows manifest mutation: `{str(summary.get('allows_manifest_mutation', False)).lower()}`",
        f"- Allows PR creation: `{str(summary.get('allows_pr_creation', False)).lower()}`",
        f"- Allows deploy: `{str(summary.get('allows_deploy', False)).lower()}`",
        "- Safety: no public content, backlog, PR, or production files were modified.",
        "",
    ]
    if summary.get("approval_note"):
        lines.extend(["Approval note:", "", summary["approval_note"], ""])
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


def run_issue_proposal_approval(
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
    approval_result: dict[str, Any] | None = None
    approval_errors: list[str] = []
    code = validation_code
    if validation_code == 0:
        code, approval_result, approval_errors = approve_specs(validation, manifest_dir, manifest_path, output_dir)
    summary = build_summary(validation, approval_result, approval_errors, issue_title, association)
    write_optional_outputs(summary, summary_output, markdown_output)
    return code, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Record proposal approval from a GitHub owner issue comment.")
    parser.add_argument("--comment-body", required=True, help="Raw GitHub issue comment body.")
    parser.add_argument("--comment-author", help="GitHub login for the comment author.")
    parser.add_argument("--author-association", help="GitHub author association, such as OWNER or COLLABORATOR.")
    parser.add_argument("--issue-title", default=DEFAULT_ISSUE_TITLE, help="GitHub issue title the comment was posted on.")
    parser.add_argument("--manifest-dir", default=str(MANIFESTS_DIR), help="Directory where manifests are stored.")
    parser.add_argument("--manifest", help="Optional explicit run manifest path.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for refreshed proposal artifacts.")
    parser.add_argument("--summary-output", help="Optional JSON summary output path.")
    parser.add_argument("--markdown-output", help="Optional markdown summary output path.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, summary = run_issue_proposal_approval(
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
