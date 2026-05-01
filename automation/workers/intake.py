#!/usr/bin/env python3
"""No-write intake gate for reviewed worker-chain opportunities."""

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


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def infer_chain_path(value: str | None, topic_id: str | None) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else ROOT / path
    if not topic_id:
        raise ValueError("Either --chain or --topic-id is required.")
    return REPORTS_DIR / f"worker-chain-{topic_id}.json"


def proposed_backlog_item(chain: dict[str, Any]) -> dict[str, str]:
    topic_id = str(chain.get("source_topic_id", "worker-topic"))
    return {
        "topic_id": f"{topic_id}-approved-intake",
        "title": f"Worker-reviewed opportunity: {chain.get('target_page_or_slug', topic_id)}",
        "cluster": str(chain.get("cluster", "")),
        "recommended_action": str(chain.get("recommended_action", "")),
        "archetype_suggestion": str(chain.get("page_role", "")),
        "target_page_or_slug": str(chain.get("target_page_or_slug", "")),
        "source_type": "analytics",
        "source_reference": f"Worker chain review: {topic_id}",
        "confidence": "medium",
        "priority": "high" if chain.get("risk_level") == "high" else "medium",
        "status": "backlog",
        "notes": "Created as a proposed intake record only. Do not add to topic_backlog.csv without human review.",
    }


def intake_state(chain: dict[str, Any], approved_by: str | None) -> tuple[str, list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []
    verdict = chain.get("review_verdict")
    blocking_count = int(chain.get("blocking_issue_count", 0))
    human_required = bool(chain.get("human_approval_required", True))

    if blocking_count:
        blockers.append("Worker review has blocking issues; revise the brief/review before intake.")
    if verdict in {"revise", "reject"}:
        blockers.append(f"Worker review verdict is `{verdict}`; intake is blocked.")
    if blockers:
        return "blocked", blockers, warnings
    if human_required and not approved_by:
        warnings.append("Human approval is required before this opportunity can become backlog/run intake.")
        return "approval_required", blockers, warnings
    if verdict == "needs_human_review" and approved_by:
        warnings.append("Human approved a high-risk or warning-level opportunity; keep next patch plan narrow.")
    return "approved_for_intake", blockers, warnings


def build_intake(chain: dict[str, Any], chain_path: Path, approved_by: str | None, note: str | None) -> dict[str, Any]:
    state, blockers, warnings = intake_state(chain, approved_by)
    generated_at = now_utc()
    topic_id = str(chain.get("source_topic_id", "worker-topic"))
    return {
        "schema_version": 1,
        "report_type": "worker_proposal_intake",
        "generated_at": generated_at,
        "source_chain_file": rel(chain_path),
        "source_topic_id": topic_id,
        "target_page_or_slug": chain.get("target_page_or_slug", ""),
        "state": state,
        "approved_by": approved_by,
        "approval_note": note,
        "review_verdict": chain.get("review_verdict", ""),
        "risk_level": chain.get("risk_level", ""),
        "approved_next_stage": chain.get("approved_next_stage", ""),
        "blockers": blockers,
        "warnings": warnings,
        "proposed_backlog_item": proposed_backlog_item(chain),
        "next_actions": next_actions_for(state, topic_id),
        "safety": "No content, backlog, or manifest files were modified by this intake gate.",
    }


def next_actions_for(state: str, topic_id: str) -> list[str]:
    if state == "blocked":
        return [
            "Review worker-review blocking issues.",
            "Regenerate the Editor brief and Worker review after fixes.",
        ]
    if state == "approval_required":
        return [
            f"Human reviews automation/reports/worker-chain-{topic_id}.md.",
            f"If approved, run: python3 automation/workers/intake.py --topic-id {topic_id} --approved-by <name> --json",
        ]
    return [
        "Manually copy proposed_backlog_item into topic_backlog.csv only if it still fits editorial priorities.",
        "Run python3 automation/pipeline.py backlog-summary --json after any manual backlog update.",
        "Use the existing plan/init-run/review lifecycle for any accepted content work.",
    ]


def render_markdown(intake: dict[str, Any]) -> str:
    backlog = intake["proposed_backlog_item"]
    backlog_lines = [f"{key}: `{value}`" for key, value in backlog.items()]
    lines = [
        f"# Worker Proposal Intake - {intake['source_topic_id']}",
        "",
        "## Status",
        "",
        f"- State: `{intake['state']}`",
        f"- Target: `{intake['target_page_or_slug']}`",
        f"- Review verdict: `{intake['review_verdict']}`",
        f"- Risk: `{intake['risk_level']}`",
        f"- Approved next stage: `{intake['approved_next_stage']}`",
        f"- Approved by: `{intake['approved_by'] or ''}`",
        "- Safety: no content, backlog, or manifest files were modified by this intake gate.",
        "",
        "## Blockers",
        "",
        md_list(intake["blockers"]),
        "",
        "## Warnings",
        "",
        md_list(intake["warnings"]),
        "",
        "## Proposed Backlog Item",
        "",
        md_list(backlog_lines),
        "",
        "## Next Actions",
        "",
        md_list(intake["next_actions"]),
        "",
    ]
    return "\n".join(lines)


def write_outputs(intake: dict[str, Any], output_dir: Path, basename: str | None) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = basename or f"worker-intake-{intake['source_topic_id']}"
    json_path = output_dir / f"{name}.json"
    md_path = output_dir / f"{name}.md"
    write_json(json_path, intake)
    md_path.write_text(render_markdown(intake), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a no-write intake artifact from a worker-chain summary.")
    parser.add_argument("--chain", help="Path to worker-chain-<topic_id>.json.")
    parser.add_argument("--topic-id", help="Topic id used to infer the default chain path.")
    parser.add_argument("--approved-by", help="Human approver name or handle.")
    parser.add_argument("--note", help="Optional approval note.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for intake artifacts.")
    parser.add_argument("--basename", help="Output basename without extension.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    chain_path = infer_chain_path(args.chain, args.topic_id)
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    chain = load_json(chain_path)
    intake = build_intake(chain, chain_path, args.approved_by, args.note)
    json_path, md_path = write_outputs(intake, output_dir, args.basename)

    summary = {
        "source_topic_id": intake["source_topic_id"],
        "target_page_or_slug": intake["target_page_or_slug"],
        "state": intake["state"],
        "json_path": rel(json_path),
        "markdown_path": rel(md_path),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Topic: {summary['source_topic_id']}")
        print(f"State: {summary['state']}")
        print(f"Intake: {summary['markdown_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
