#!/usr/bin/env python3
"""Run owner-approved planned manifest lifecycle steps from GitHub issue comments."""

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

from automation import editor as brief_editor
from automation import exact_proposals, patch_planner, proposal_renderer, reviewer
from automation.io import load_run_manifest, write_json, write_run_manifest
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
COMMANDS = {"/review-run", "/brief-run", "/patch-plan-run", "/propose-run"}
RUN_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,180}$")
EXPECTED_STATUS = {
    "/review-run": "planned",
    "/brief-run": "reviewed",
    "/patch-plan-run": "draft_brief_ready",
    "/propose-run": "patch_plan_ready",
}
NEXT_STATUS = {
    "/review-run": "reviewed",
    "/brief-run": "draft_brief_ready",
    "/patch-plan-run": "patch_plan_ready",
    "/propose-run": "proposal_ready",
}


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
    run_id = parts[1].strip()
    inline_note = parts[2].strip() if len(parts) == 3 else ""
    note = "\n".join(part for part in (inline_note, remainder.strip()) if part).strip()
    return command, run_id, note


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
        errors.append("No supported owner lifecycle command found. Use /review-run, /brief-run, /patch-plan-run, or /propose-run.")
        return 1, {
            "command": "",
            "run_id": "",
            "approved_by": author,
            "approval_note": "",
            "errors": errors,
        }

    command, run_id, note = parsed
    if not RUN_ID_PATTERN.match(run_id):
        errors.append(f"Unsafe or unsupported run id: {run_id}")
    if not note:
        errors.append("Lifecycle approval note is required after the run id.")
    if "<" in note or ">" in note:
        errors.append("Lifecycle approval note still contains placeholder brackets; replace placeholders with a real owner note.")

    return (1 if errors else 0), {
        "command": command,
        "run_id": run_id,
        "approved_by": author,
        "approval_note": note,
        "errors": errors,
    }


def manifest_path_for(run_id: str, manifest_dir: Path, explicit_manifest: Path | None) -> Path:
    if explicit_manifest:
        return explicit_manifest
    return manifest_dir / f"{run_id}.json"


def write_brief_artifact(manifest_path: Path, output_dir: Path) -> dict[str, Any]:
    manifest = load_run_manifest(manifest_path)
    out_path = output_dir / f"{manifest.run_id}.brief.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(brief_editor.build_brief(manifest), encoding="utf-8")
    manifest.artifacts.setdefault("editor", {})
    manifest.artifacts["editor"]["brief_path"] = rel(out_path)
    manifest.status = "draft_brief_ready"
    write_run_manifest(manifest_path, manifest)
    return {
        "artifact_type": "brief",
        "path": rel(out_path),
        "status": manifest.status,
    }


def write_patch_plan_artifact(manifest_path: Path, output_dir: Path) -> dict[str, Any]:
    manifest = load_run_manifest(manifest_path)
    manifest.status = "patch_plan_ready"
    patch_plan, markdown = patch_planner.build_patch_plan(manifest)
    out_path = output_dir / f"{manifest.run_id}.patch.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    manifest.artifacts.setdefault("patch_plan", {})
    manifest.artifacts["patch_plan"] = patch_plan
    manifest.artifacts["patch_plan"]["report_path"] = rel(out_path)
    manifest.changed_files = list(patch_plan.get("changed_files", []))
    write_run_manifest(manifest_path, manifest)
    return {
        "artifact_type": "patch_plan",
        "path": rel(out_path),
        "status": manifest.status,
        "changed_files": manifest.changed_files,
        "patch_spec_count": len(patch_plan.get("patch_specs", [])),
    }


def write_proposal_artifacts(manifest_path: Path, output_dir: Path) -> dict[str, Any]:
    proposal_path, rendered_specs = proposal_renderer.render_proposal(manifest_path, output_dir)
    exact_review = exact_proposals.render_exact_proposals(manifest_path, output_dir)
    manifest = load_run_manifest(manifest_path)
    return {
        "artifact_type": "proposal",
        "path": rel(proposal_path),
        "status": manifest.status,
        "rendered_spec_count": len(rendered_specs),
        "exact_proposal_count": int(exact_review.get("exact_proposal_count", 0)),
        "exact_proposal_json": exact_review.get("report_paths", {}).get("json", ""),
        "exact_proposal_markdown": exact_review.get("report_paths", {}).get("markdown", ""),
    }


def run_lifecycle_step(
    validation: dict[str, Any],
    manifest_dir: Path,
    manifest_path: Path | None,
    output_dir: Path,
) -> tuple[int, dict[str, Any] | None, list[str]]:
    errors = validation["errors"]
    command = validation.get("command", "")
    run_id = validation.get("run_id", "")
    if errors:
        return 1, None, errors

    selected_manifest = manifest_path_for(run_id, manifest_dir, manifest_path)
    if not selected_manifest.exists():
        return 1, None, [f"Manifest does not exist: {rel(selected_manifest)}"]

    try:
        before = load_run_manifest(selected_manifest)
    except Exception as exc:
        return 1, None, [f"Failed to load manifest: {exc}"]

    expected = EXPECTED_STATUS[command]
    if before.status != expected:
        return 1, None, [
            f"Manifest status must be `{expected}` before {command}; current status is `{before.status}`."
        ]

    try:
        if command == "/review-run":
            manifest = reviewer.review_manifest(selected_manifest)
            result = {
                "artifact_type": "review",
                "path": rel(selected_manifest),
                "status": manifest.status,
                "canonical_claim_count": len(
                    manifest.artifacts.get("review_context", {}).get("canonical_claim_ids", [])
                ),
            }
        elif command == "/brief-run":
            result = write_brief_artifact(selected_manifest, output_dir)
        elif command == "/patch-plan-run":
            result = write_patch_plan_artifact(selected_manifest, output_dir)
        elif command == "/propose-run":
            result = write_proposal_artifacts(selected_manifest, output_dir)
        else:
            return 1, None, [f"Unsupported lifecycle command: {command}"]
    except Exception as exc:
        return 1, None, [f"Failed to run lifecycle step: {exc}"]

    after = load_run_manifest(selected_manifest)
    return 0, {
        "run_id": after.run_id,
        "manifest_path": rel(selected_manifest),
        "before_status": before.status,
        "after_status": after.status,
        "result": result,
    }, []


def next_actions(summary: dict[str, Any]) -> list[str]:
    run_id = summary.get("run_id", "") or "<run_id>"
    command = summary.get("command", "")
    errors = summary.get("errors", [])
    if errors:
        return [
            "Fix the GitHub issue command, manifest path, or manifest status, then post a new owner command.",
            "Lifecycle commands must run in order: /review-run -> /brief-run -> /patch-plan-run -> /propose-run.",
        ]
    if command == "/review-run":
        return [
            f"Review the deterministic review context, then use: /brief-run {run_id} <owner confirms brief generation>",
            "No public content is approved by this step.",
        ]
    if command == "/brief-run":
        return [
            f"Review the brief artifact, then use: /patch-plan-run {run_id} <owner confirms proposal-only patch planning>",
            "No public content is approved by this step.",
        ]
    if command == "/patch-plan-run":
        return [
            f"Render owner-review proposals: /propose-run {run_id} <owner confirms proposal rendering>",
            "Public content may be changed only after exact proposed text/spec approval, apply-preview, apply-approved, and strict QA.",
        ]
    if command == "/propose-run":
        return [
            f"Review proposal artifacts, then record exact proposal approval only if the visible Before/After text is correct: /approve-proposal {run_id} <owner approval note>",
            "Public content is still unchanged until apply-preview, apply-approved, and strict QA.",
        ]
    return []


def build_summary(
    validation: dict[str, Any],
    lifecycle_result: dict[str, Any] | None,
    lifecycle_errors: list[str],
    issue_title: str,
    author_association: str,
) -> dict[str, Any]:
    errors = list(validation.get("errors", []))
    errors.extend(lifecycle_errors)
    command = validation.get("command", "")
    run_id = validation.get("run_id", "")
    state = "blocked"
    if lifecycle_result and not errors:
        state = {
            "/review-run": "run_reviewed",
            "/brief-run": "run_brief_ready",
            "/patch-plan-run": "run_patch_plan_ready",
            "/propose-run": "run_proposal_ready",
        }.get(command, "blocked")
        run_id = lifecycle_result.get("run_id", run_id)
    summary = {
        "schema_version": 1,
        "report_type": "llm_issue_lifecycle",
        "generated_at": now_utc(),
        "state": state,
        "issue_title": issue_title,
        "comment_author": validation.get("approved_by", ""),
        "author_association": author_association,
        "command": command,
        "run_id": run_id,
        "approval_note": validation.get("approval_note", ""),
        "manifest_path": lifecycle_result.get("manifest_path", "") if lifecycle_result else "",
        "before_status": lifecycle_result.get("before_status", "") if lifecycle_result else "",
        "after_status": lifecycle_result.get("after_status", "") if lifecycle_result else "",
        "expected_before_status": EXPECTED_STATUS.get(command, ""),
        "expected_after_status": NEXT_STATUS.get(command, ""),
        "result": lifecycle_result.get("result", {}) if lifecycle_result else {},
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": bool(lifecycle_result and not errors),
        "allows_pr_creation": False,
        "allows_deploy": False,
        "errors": errors,
        "safety": "No public content, backlog, PR, or production files were modified. This step may only mutate automation manifests and reports.",
    }
    summary["next_actions"] = next_actions(summary)
    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    result = summary.get("result", {})
    lines = [
        f"# LLM Issue Lifecycle - {summary.get('run_id', '') or 'blocked'}",
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
        f"- Result artifact: `{result.get('path', '')}`",
        f"- Exact proposal review: `{result.get('exact_proposal_markdown', '')}`",
        f"- Allows content edit: `{str(summary.get('allows_content_edit', False)).lower()}`",
        f"- Allows backlog mutation: `{str(summary.get('allows_backlog_mutation', False)).lower()}`",
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


def run_issue_lifecycle(
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
    lifecycle_result: dict[str, Any] | None = None
    lifecycle_errors: list[str] = []
    code = validation_code
    if validation_code == 0:
        code, lifecycle_result, lifecycle_errors = run_lifecycle_step(validation, manifest_dir, manifest_path, output_dir)
    summary = build_summary(validation, lifecycle_result, lifecycle_errors, issue_title, association)
    write_optional_outputs(summary, summary_output, markdown_output)
    return code, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a planned manifest lifecycle step from a GitHub owner issue comment.")
    parser.add_argument("--comment-body", required=True, help="Raw GitHub issue comment body.")
    parser.add_argument("--comment-author", help="GitHub login for the comment author.")
    parser.add_argument("--author-association", help="GitHub author association, such as OWNER or COLLABORATOR.")
    parser.add_argument("--issue-title", default=DEFAULT_ISSUE_TITLE, help="GitHub issue title the comment was posted on.")
    parser.add_argument("--manifest-dir", default=str(MANIFESTS_DIR), help="Directory where planned manifests are stored.")
    parser.add_argument("--manifest", help="Optional explicit run manifest path.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for brief or patch-plan artifacts.")
    parser.add_argument("--summary-output", help="Optional JSON summary output path.")
    parser.add_argument("--markdown-output", help="Optional markdown summary output path.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, summary = run_issue_lifecycle(
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
