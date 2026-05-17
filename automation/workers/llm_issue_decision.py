#!/usr/bin/env python3
"""Ingest owner decisions from GitHub owner handoff issue comments."""

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

from automation.io import write_json
from automation.proposal_renderer import md_list
from automation.workers.llm_topic_decision import (
    DEFAULT_DISCOVERY,
    REPORTS_DIR,
    rel,
    resolve_path,
    run_topic_decision,
)


DEFAULT_QUEUE_DISCOVERY = REPORTS_DIR / "llm-auto-review-queue" / "llm-auto-review-topic-discovery.json"
DEFAULT_ISSUE_TITLE = "LLM Owner Digest: Action Needed"
ALLOWED_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}
COMMAND_STATES = {
    "/approve-chain": "approved_for_chain",
    "/monitor": "monitor",
    "/reject": "rejected",
}
TOPIC_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,119}$")


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_discovery_path() -> Path:
    if DEFAULT_QUEUE_DISCOVERY.exists():
        return DEFAULT_QUEUE_DISCOVERY
    return DEFAULT_DISCOVERY


def normalize_author(author: str | None) -> str:
    value = (author or "").strip()
    return value or "unknown"


def normalize_association(value: str | None) -> str:
    return (value or "").strip().upper()


def parse_command(comment_body: str) -> tuple[str, str, str] | None:
    body = comment_body.strip()
    if not body:
        return None
    first_line, _, remainder = body.partition("\n")
    parts = first_line.strip().split(maxsplit=2)
    if len(parts) < 2:
        return None
    command = parts[0].strip().lower()
    if command not in COMMAND_STATES:
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
        errors.append("No supported owner decision command found. Use /monitor, /reject, or /approve-chain.")
        return 1, {
            "command": "",
            "topic_id": "",
            "decision_state": "",
            "decided_by": author,
            "decision_note": "",
            "errors": errors,
        }

    command, topic_id, note = parsed
    if not TOPIC_ID_PATTERN.match(topic_id):
        errors.append(f"Unsafe or unsupported topic id: {topic_id}")
    if not note:
        errors.append("Decision note is required after the topic id.")
    if "<" in note or ">" in note:
        errors.append("Decision note still contains placeholder brackets; replace placeholders with a real owner note.")

    return (1 if errors else 0), {
        "command": command,
        "topic_id": topic_id,
        "decision_state": COMMAND_STATES[command],
        "decided_by": author,
        "decision_note": note,
        "errors": errors,
    }


def build_summary(
    validation: dict[str, Any],
    decision_payload: dict[str, Any] | None,
    discovery_path: Path,
    issue_title: str,
    author_association: str,
) -> dict[str, Any]:
    errors = list(validation.get("errors", []))
    if decision_payload:
        errors.extend(decision_payload.get("errors", []))
    state = "decision_recorded" if decision_payload and not errors else "blocked"
    return {
        "schema_version": 1,
        "report_type": "llm_issue_decision",
        "generated_at": now_utc(),
        "state": state,
        "issue_title": issue_title,
        "comment_author": validation.get("decided_by", ""),
        "author_association": author_association,
        "command": validation.get("command", ""),
        "topic_id": validation.get("topic_id", ""),
        "decision_state": validation.get("decision_state", ""),
        "decision_note": validation.get("decision_note", ""),
        "source_discovery": rel(discovery_path),
        "decision_output_path": decision_payload.get("output_path", "") if decision_payload else "",
        "decision_markdown_path": decision_payload.get("markdown_path", "") if decision_payload else "",
        "allows_worker_chain": bool(decision_payload.get("allows_worker_chain", False)) if decision_payload else False,
        "allows_content_edit": False,
        "errors": errors,
        "next_actions": next_actions(validation, decision_payload, errors),
        "safety": "No content, backlog, manifest, PR, or production files were modified. This command only records a no-write owner topic decision.",
    }


def next_actions(
    validation: dict[str, Any],
    decision_payload: dict[str, Any] | None,
    errors: list[str],
) -> list[str]:
    if errors:
        return [
            "Fix the GitHub issue comment command and rerun by posting a new comment.",
            "Use: /monitor <topic_id> <why>, /reject <topic_id> <why>, or /approve-chain <topic_id> <validated player value and scope>.",
        ]
    if validation.get("decision_state") == "approved_for_chain":
        topic_id = validation.get("topic_id", "")
        return [
            f"The committed decision artifact can trigger the no-write worker-chain workflow for `{topic_id}`.",
            "Review the generated worker-chain summary before any intake, proposal, or public content edit.",
        ]
    if decision_payload:
        return list(decision_payload.get("next_actions", []))
    return []


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# LLM Issue Decision - {summary.get('topic_id', '') or 'blocked'}",
        "",
        "## Result",
        "",
        f"- State: `{summary.get('state', '')}`",
        f"- Command: `{summary.get('command', '')}`",
        f"- Topic: `{summary.get('topic_id', '')}`",
        f"- Decision: `{summary.get('decision_state', '')}`",
        f"- Comment author: `{summary.get('comment_author', '')}`",
        f"- Author association: `{summary.get('author_association', '')}`",
        f"- Source discovery: `{summary.get('source_discovery', '')}`",
        f"- Decision artifact: `{summary.get('decision_output_path', '')}`",
        f"- Allows worker chain: `{str(summary.get('allows_worker_chain', False)).lower()}`",
        f"- Allows content edit: `{str(summary.get('allows_content_edit', False)).lower()}`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if summary.get("decision_note"):
        lines.extend(["Decision note:", "", summary["decision_note"], ""])
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


def run_issue_decision(
    comment_body: str,
    comment_author: str | None,
    author_association: str | None,
    issue_title: str,
    discovery_path: Path,
    output_dir: Path,
    summary_output: Path | None,
    markdown_output: Path | None,
) -> tuple[int, dict[str, Any]]:
    author = normalize_author(comment_author)
    association = normalize_association(author_association)
    validation_code, validation = validate_command(issue_title, comment_body, author, association)
    decision_payload: dict[str, Any] | None = None
    code = validation_code
    if validation_code == 0:
        decision_code, decision_payload = run_topic_decision(
            discovery_path=discovery_path,
            topic_id=validation["topic_id"],
            decision_state=validation["decision_state"],
            decided_by=author,
            note=validation["decision_note"],
            output_dir=output_dir,
            basename=None,
        )
        code = decision_code
    summary = build_summary(validation, decision_payload, discovery_path, issue_title, association)
    write_optional_outputs(summary, summary_output, markdown_output)
    return code, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Record an LLM topic decision from a GitHub owner issue comment.")
    parser.add_argument("--comment-body", required=True, help="Raw GitHub issue comment body.")
    parser.add_argument("--comment-author", help="GitHub login for the comment author.")
    parser.add_argument("--author-association", help="GitHub author association, such as OWNER or COLLABORATOR.")
    parser.add_argument("--issue-title", default=DEFAULT_ISSUE_TITLE, help="GitHub issue title the comment was posted on.")
    parser.add_argument("--discovery", help="Path to the topic discovery artifact.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for llm-topic-decision artifacts.")
    parser.add_argument("--summary-output", help="Optional JSON summary output path.")
    parser.add_argument("--markdown-output", help="Optional markdown summary output path.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, summary = run_issue_decision(
        comment_body=args.comment_body,
        comment_author=args.comment_author,
        author_association=args.author_association,
        issue_title=args.issue_title,
        discovery_path=resolve_path(args.discovery) if args.discovery else default_discovery_path(),
        output_dir=resolve_path(args.output_dir),
        summary_output=resolve_path(args.summary_output) if args.summary_output else None,
        markdown_output=resolve_path(args.markdown_output) if args.markdown_output else None,
    )
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Topic: {summary['topic_id']}")
        print(f"Decision: {summary['decision_state']}")
        print(f"Output: {summary['decision_output_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
