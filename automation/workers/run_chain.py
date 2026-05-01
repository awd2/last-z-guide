#!/usr/bin/env python3
"""Run the no-write Scout -> Editor -> Reviewer worker chain."""

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
from automation.workers import editor, reviewer, scout


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_SIGNALS_PATH = ROOT / "content" / "gsc" / "latest-gsc-agent-signals.json"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def select_topic(proposals: list[dict[str, Any]], topic_id: str | None, target: str | None) -> dict[str, Any]:
    if topic_id:
        for proposal in proposals:
            if proposal.get("topic_id") == topic_id:
                return proposal
        raise ValueError(f"Topic proposal not found: {topic_id}")
    if target:
        for proposal in proposals:
            if proposal.get("target_page_or_slug") == target:
                return proposal
        raise ValueError(f"Target proposal not found: {target}")
    if not proposals:
        raise ValueError("Scout produced no proposals.")
    return proposals[0]


def build_chain_summary(
    proposal: dict[str, Any],
    brief: dict[str, Any],
    review: dict[str, Any],
    artifacts: dict[str, str],
    generated_at: str,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "report_type": "worker_chain_summary",
        "generated_at": generated_at,
        "source_topic_id": proposal.get("topic_id", ""),
        "target_page_or_slug": proposal.get("target_page_or_slug", ""),
        "cluster": proposal.get("cluster", ""),
        "recommended_action": proposal.get("recommended_action", ""),
        "page_role": brief.get("page_role", ""),
        "primary_query_family": brief.get("primary_query_family", ""),
        "review_verdict": review.get("verdict", ""),
        "risk_level": review.get("risk_level", ""),
        "approved_next_stage": review.get("approved_next_stage", ""),
        "human_approval_required": review.get("human_approval_required", True),
        "blocking_issue_count": len(review.get("blocking_issues", [])),
        "warning_count": len(review.get("warnings", [])),
        "artifacts": artifacts,
        "safety": "No content, backlog, or manifest files were modified by this worker chain.",
    }


def render_markdown(summary: dict[str, Any], proposal: dict[str, Any], brief: dict[str, Any], review: dict[str, Any]) -> str:
    artifacts = summary["artifacts"]
    blocking = [
        f"{item['severity']}: {item['issue']} Required fix: {item['required_fix']}"
        for item in review.get("blocking_issues", [])
    ]
    lines = [
        f"# Worker Chain Summary - {summary['source_topic_id']}",
        "",
        "## Outcome",
        "",
        f"- Target: `{summary['target_page_or_slug']}`",
        f"- Cluster: `{summary['cluster']}`",
        f"- Action: `{summary['recommended_action']}`",
        f"- Page role: `{summary['page_role']}`",
        f"- Primary query family: {summary['primary_query_family']}",
        f"- Review verdict: `{summary['review_verdict']}`",
        f"- Risk: `{summary['risk_level']}`",
        f"- Approved next stage: `{summary['approved_next_stage']}`",
        f"- Human approval required: `{str(summary['human_approval_required']).lower()}`",
        "- Safety: no content, backlog, or manifest files were modified by this worker chain.",
        "",
        "## Artifacts",
        "",
        md_list([f"{name}: `{path}`" for name, path in artifacts.items()]),
        "",
        "## Scout Evidence",
        "",
        md_list(proposal.get("evidence", [])),
        "",
        "## Editor First-Screen Answer",
        "",
        brief.get("first_screen_answer", ""),
        "",
        "## Reviewer Blocking Issues",
        "",
        md_list(blocking),
        "",
        "## Reviewer Warnings",
        "",
        md_list(review.get("warnings", [])),
        "",
        "## Required Checks",
        "",
        md_list([f"`{check}`" for check in review.get("required_checks", [])]),
        "",
    ]
    return "\n".join(lines)


def write_chain_outputs(
    summary: dict[str, Any],
    proposal: dict[str, Any],
    brief: dict[str, Any],
    review: dict[str, Any],
    output_dir: Path,
    basename: str | None,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = basename or f"worker-chain-{summary['source_topic_id']}"
    json_path = output_dir / f"{name}.json"
    md_path = output_dir / f"{name}.md"
    summary["artifacts"]["chain_json"] = rel(json_path)
    summary["artifacts"]["chain_markdown"] = rel(md_path)
    write_json(json_path, summary)
    md_path.write_text(render_markdown(summary, proposal, brief, review), encoding="utf-8")
    return json_path, md_path


def run_chain(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    signals_path = Path(args.signals)
    if not signals_path.is_absolute():
        signals_path = ROOT / signals_path

    generated_at = now_utc()

    scout_payload = scout.build_payload(signals_path, limit=args.limit, min_impressions=args.min_impressions)
    scout_json, scout_md = scout.write_outputs(scout_payload, output_dir, args.scout_basename)
    proposal = select_topic(scout_payload["proposals"], args.topic_id, args.target)

    brief = editor.build_editor_brief(proposal, scout_json)
    editor_json, editor_md = editor.write_outputs(brief, output_dir, args.editor_basename)

    review = reviewer.build_review(brief, proposal, editor_json, scout_json)
    reviewer_json, reviewer_md = reviewer.write_outputs(review, output_dir, args.reviewer_basename)

    artifacts = {
        "scout_json": rel(scout_json),
        "scout_markdown": rel(scout_md),
        "editor_json": rel(editor_json),
        "editor_markdown": rel(editor_md),
        "reviewer_json": rel(reviewer_json),
        "reviewer_markdown": rel(reviewer_md),
    }
    summary = build_chain_summary(proposal, brief, review, artifacts, generated_at)
    write_chain_outputs(summary, proposal, brief, review, output_dir, args.basename)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the no-write Scout -> Editor -> Reviewer worker chain.")
    parser.add_argument("--topic-id", help="Scout topic_id to select after Scout runs.")
    parser.add_argument("--target", help="Alternative selector: target page or slug.")
    parser.add_argument("--signals", default=str(DEFAULT_SIGNALS_PATH), help="Path to latest-gsc-agent-signals.json.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for worker artifacts.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum Scout proposals to render.")
    parser.add_argument("--min-impressions", type=int, default=200, help="Minimum page impressions for Scout proposals.")
    parser.add_argument("--scout-basename", default="scout-topic-proposals", help="Scout output basename.")
    parser.add_argument("--editor-basename", help="Editor output basename. Defaults to editor-brief-<topic_id>.")
    parser.add_argument("--reviewer-basename", help="Reviewer output basename. Defaults to worker-review-<topic_id>.")
    parser.add_argument("--basename", help="Chain summary basename. Defaults to worker-chain-<topic_id>.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    summary = run_chain(args)
    output = {
        "source_topic_id": summary["source_topic_id"],
        "target_page_or_slug": summary["target_page_or_slug"],
        "review_verdict": summary["review_verdict"],
        "risk_level": summary["risk_level"],
        "approved_next_stage": summary["approved_next_stage"],
        "human_approval_required": summary["human_approval_required"],
        "artifacts": summary["artifacts"],
    }
    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"Topic: {output['source_topic_id']}")
        print(f"Target: {output['target_page_or_slug']}")
        print(f"Verdict: {output['review_verdict']}")
        print(f"Chain summary: {output['artifacts']['chain_markdown']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
