#!/usr/bin/env python3
"""Build a consolidated no-write report for LLM topic decisions."""

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


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_JSON_OUTPUT = REPORTS_DIR / "llm-topic-decisions.json"
DEFAULT_MARKDOWN_OUTPUT = REPORTS_DIR / "llm-topic-decisions.md"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def decision_files(reports_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in reports_dir.glob("llm-topic-decision-*.json")
        if path.name != "llm-topic-decisions.json"
    )


def compact_decision(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    topic = payload.get("topic_snapshot") or {}
    return {
        "topic_id": payload.get("topic_id", ""),
        "decision_state": payload.get("decision_state", ""),
        "decided_by": payload.get("decided_by", ""),
        "generated_at": payload.get("generated_at", ""),
        "target_page_or_slug": topic.get("target_page_or_slug", ""),
        "cluster": topic.get("cluster", ""),
        "risk_level": topic.get("risk_level", ""),
        "priority": topic.get("priority", ""),
        "allows_worker_chain": bool(payload.get("allows_worker_chain", False)),
        "allows_content_edit": bool(payload.get("allows_content_edit", False)),
        "decision_note": payload.get("decision_note", ""),
        "next_actions": payload.get("next_actions", []),
        "source_discovery": payload.get("source_discovery", ""),
        "artifact_path": rel(path),
        "markdown_path": payload.get("markdown_path", ""),
    }


def build_report(reports_dir: Path) -> dict[str, Any]:
    decisions = [compact_decision(path) for path in decision_files(reports_dir)]
    counts: dict[str, int] = {}
    for decision in decisions:
        state = str(decision.get("decision_state", ""))
        counts[state] = counts.get(state, 0) + 1
    allowed = [item for item in decisions if item.get("allows_worker_chain")]
    return {
        "schema_version": 1,
        "report_type": "llm_topic_decisions_summary",
        "generated_at": now_utc(),
        "decision_count": len(decisions),
        "counts_by_state": dict(sorted(counts.items())),
        "allowed_worker_chain_count": len(allowed),
        "allowed_worker_chain_topics": [item["topic_id"] for item in allowed],
        "content_edit_allowed_count": sum(1 for item in decisions if item.get("allows_content_edit")),
        "decisions": decisions,
        "safety": "No content, backlog, manifest, PR, or production files were modified by this report.",
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# LLM Topic Decisions - {report['generated_at']}",
        "",
        "## Overview",
        "",
        f"- Decisions: {report['decision_count']}",
        f"- Counts by state: `{json.dumps(report['counts_by_state'], sort_keys=True)}`",
        f"- Topics currently allowed for worker chain: {report['allowed_worker_chain_count']}",
        f"- Topics currently allowed for content edit: {report['content_edit_allowed_count']}",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if report.get("allowed_worker_chain_topics"):
        lines.extend(
            [
                "## Allowed Worker Chain Topics",
                "",
                md_list(report["allowed_worker_chain_topics"]),
                "",
            ]
        )

    lines.extend(["## Decisions", ""])
    if not report.get("decisions"):
        lines.append("- None")
        return "\n".join(lines) + "\n"

    for decision in report["decisions"]:
        lines.extend(
            [
                f"### {decision['topic_id']}",
                "",
                f"- Decision: `{decision['decision_state']}`",
                f"- Target: `{decision['target_page_or_slug']}`",
                f"- Cluster: `{decision['cluster']}`",
                f"- Priority: `{decision['priority']}`",
                f"- Risk: `{decision['risk_level']}`",
                f"- Allows worker chain: `{str(decision['allows_worker_chain']).lower()}`",
                f"- Allows content edit: `{str(decision['allows_content_edit']).lower()}`",
                f"- Artifact: `{decision['artifact_path']}`",
                "",
                "Decision note:",
                "",
                decision.get("decision_note", ""),
                "",
                "Next actions:",
                "",
                md_list(decision.get("next_actions", [])),
                "",
            ]
        )
    return "\n".join(lines)


def write_report(report: dict[str, Any], json_output: Path, markdown_output: Path) -> tuple[Path, Path]:
    json_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    write_json(json_output, report)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    return json_output, markdown_output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a consolidated no-write report for LLM topic decisions.")
    parser.add_argument("--reports-dir", default=str(REPORTS_DIR), help="Directory containing llm-topic-decision-*.json files.")
    parser.add_argument("--json-output", default=str(DEFAULT_JSON_OUTPUT), help="Path for the consolidated JSON artifact.")
    parser.add_argument("--markdown-output", default=str(DEFAULT_MARKDOWN_OUTPUT), help="Path for the consolidated markdown artifact.")
    parser.add_argument("--no-write", action="store_true", help="Build and print only; do not write artifacts.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    report = build_report(resolve_path(args.reports_dir))
    if not args.no_write:
        json_path, markdown_path = write_report(
            report,
            resolve_path(args.json_output),
            resolve_path(args.markdown_output),
        )
    else:
        json_path = resolve_path(args.json_output)
        markdown_path = resolve_path(args.markdown_output)

    summary = {
        "report_type": report["report_type"],
        "decision_count": report["decision_count"],
        "counts_by_state": report["counts_by_state"],
        "allowed_worker_chain_topics": report["allowed_worker_chain_topics"],
        "content_edit_allowed_count": report["content_edit_allowed_count"],
        "json_output": rel(json_path),
        "markdown_output": rel(markdown_path),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Decisions: {summary['decision_count']}")
        print(f"Counts by state: {summary['counts_by_state']}")
        print(f"Allowed worker chain topics: {summary['allowed_worker_chain_topics']}")
        print(f"Content edit allowed count: {summary['content_edit_allowed_count']}")
        if not args.no_write:
            print(f"JSON: {summary['json_output']}")
            print(f"Markdown: {summary['markdown_output']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
