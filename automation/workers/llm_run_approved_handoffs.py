#!/usr/bin/env python3
"""Run pending owner-approved no-write LLM worker-chain handoffs."""

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
from automation.reports import llm_approved_handoffs
from automation.workers import llm_worker_chain


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_OUTPUT_DIR = REPORTS_DIR / "llm-approved-handoff-run"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def current_chain_path(reports_dir: Path, topic_id: str) -> Path:
    return reports_dir / f"llm-worker-chain-{topic_id}.json"


def chain_is_current(decision_path: Path, reports_dir: Path, topic_id: str) -> bool:
    chain_path = current_chain_path(reports_dir, topic_id)
    if not chain_path.exists():
        return False
    try:
        decision = load_json(decision_path)
        chain = load_json(chain_path)
    except Exception:
        return False
    if chain.get("state") != "completed":
        return False
    if chain.get("handoff_source") != "topic_decision":
        return False
    if chain.get("source_decision") != rel(decision_path):
        return False
    decision_time = str(decision.get("generated_at") or "")
    chain_time = str(chain.get("generated_at") or "")
    if not decision_time or not chain_time:
        return False
    return chain_time >= decision_time


def handoff_record(handoff: dict[str, Any], status: str, **extra: Any) -> dict[str, Any]:
    record = {
        "topic_id": handoff.get("topic_id", ""),
        "target_page_or_slug": handoff.get("target_page_or_slug", ""),
        "cluster": handoff.get("cluster", ""),
        "priority": handoff.get("priority", ""),
        "risk_level": handoff.get("risk_level", ""),
        "decision_artifact": handoff.get("decision_artifact", ""),
        "status": status,
    }
    record.update(extra)
    return record


def run_approved_handoffs(
    reports_dir: Path,
    output_dir: Path,
    provider: str,
    max_handoffs: int,
    include_current: bool,
    basename: str,
    editor_fixture_path: Path | None = None,
    reviewer_fixture_path: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_at = now_utc()
    view = llm_approved_handoffs.build_view(reports_dir, provider=provider)
    handoffs = list(view.get("handoffs", []))
    records: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []

    for handoff in handoffs:
        topic_id = str(handoff.get("topic_id") or "")
        decision_artifact = str(handoff.get("decision_artifact") or "")
        decision_path = resolve_path(decision_artifact)
        if not topic_id or not decision_artifact:
            records.append(handoff_record(handoff, "skipped_invalid", errors=["Missing topic_id or decision artifact."]))
            continue
        if not include_current and chain_is_current(decision_path, reports_dir, topic_id):
            records.append(
                handoff_record(
                    handoff,
                    "skipped_current",
                    existing_chain=rel(current_chain_path(reports_dir, topic_id)),
                )
            )
            continue
        pending.append(handoff)

    if max_handoffs < 1:
        max_handoffs = 1
    selected = pending[:max_handoffs]
    deferred = pending[max_handoffs:]
    for handoff in deferred:
        records.append(handoff_record(handoff, "deferred_by_limit"))

    for handoff in selected:
        topic_id = str(handoff.get("topic_id") or "")
        decision_path = resolve_path(str(handoff.get("decision_artifact") or ""))
        chain_basename = f"llm-worker-chain-{topic_id}"
        code, chain_summary = llm_worker_chain.run_llm_worker_chain(
            signal_paths=[],
            output_dir=output_dir,
            provider=provider,
            topic_id=None,
            basename=chain_basename,
            scout_basename=f"llm-worker-chain-scout-{topic_id}",
            editor_basename=None,
            reviewer_basename=None,
            scout_fixture_path=None,
            editor_fixture_path=editor_fixture_path,
            reviewer_fixture_path=reviewer_fixture_path,
            limit=8,
            min_impressions=200,
            decision_path=decision_path,
        )
        records.append(
            handoff_record(
                handoff,
                "completed" if code == 0 else "failed",
                chain_state=chain_summary.get("state"),
                review_verdict=chain_summary.get("review_verdict"),
                owner_approval_required=chain_summary.get("owner_approval_required"),
                chain_json=chain_summary.get("artifacts", {}).get("chain_json"),
                chain_markdown=chain_summary.get("artifacts", {}).get("chain_markdown"),
                errors=chain_summary.get("errors", []),
            )
        )

    run_count = sum(1 for record in records if record["status"] in {"completed", "failed"})
    success_count = sum(1 for record in records if record["status"] == "completed")
    failure_count = sum(1 for record in records if record["status"] == "failed")
    skipped_current_count = sum(1 for record in records if record["status"] == "skipped_current")
    deferred_count = sum(1 for record in records if record["status"] == "deferred_by_limit")
    pending_count = len(pending)
    state = "no_handoffs"
    if failure_count:
        state = "completed_with_failures"
    elif run_count:
        state = "completed"
    elif skipped_current_count:
        state = "current"
    elif deferred_count:
        state = "deferred"

    summary = {
        "schema_version": 1,
        "report_type": "llm_approved_handoff_run",
        "generated_at": generated_at,
        "state": state,
        "provider": provider,
        "reports_dir": rel(reports_dir),
        "output_dir": rel(output_dir),
        "approved_handoff_count": len(handoffs),
        "pending_handoff_count": pending_count,
        "run_count": run_count,
        "success_count": success_count,
        "failure_count": failure_count,
        "skipped_current_count": skipped_current_count,
        "deferred_count": deferred_count,
        "max_handoffs": max_handoffs,
        "include_current": include_current,
        "handoffs": records,
        "safety": "No content, backlog, manifest, PR, or production files were modified.",
    }
    json_path, markdown_path = write_summary(summary, output_dir, basename)
    summary["artifacts"] = {
        "handoff_run_json": rel(json_path),
        "handoff_run_markdown": rel(markdown_path),
    }
    write_json(json_path, summary)
    markdown_path.write_text(render_markdown(summary), encoding="utf-8")
    return (1 if failure_count else 0), summary


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# LLM Approved Handoff Run - {summary['generated_at']}",
        "",
        "## Outcome",
        "",
        f"- State: `{summary['state']}`",
        f"- Provider: `{summary['provider']}`",
        f"- Approved handoffs: `{summary['approved_handoff_count']}`",
        f"- Pending handoffs: `{summary['pending_handoff_count']}`",
        f"- Run count: `{summary['run_count']}`",
        f"- Success count: `{summary['success_count']}`",
        f"- Failure count: `{summary['failure_count']}`",
        f"- Skipped current: `{summary['skipped_current_count']}`",
        f"- Deferred by limit: `{summary['deferred_count']}`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
        "## Handoffs",
        "",
    ]
    if not summary.get("handoffs"):
        lines.extend(["- None", ""])
        return "\n".join(lines)

    for handoff in summary["handoffs"]:
        details = [
            f"Status: `{handoff.get('status')}`",
            f"Target: `{handoff.get('target_page_or_slug')}`",
            f"Decision: `{handoff.get('decision_artifact')}`",
        ]
        if handoff.get("chain_markdown"):
            details.append(f"Chain markdown: `{handoff.get('chain_markdown')}`")
        if handoff.get("existing_chain"):
            details.append(f"Existing chain: `{handoff.get('existing_chain')}`")
        if handoff.get("errors"):
            details.append(f"Errors: `{json.dumps(handoff.get('errors'))}`")
        lines.extend([f"### {handoff.get('topic_id')}", "", md_list(details), ""])
    return "\n".join(lines)


def write_summary(summary: dict[str, Any], output_dir: Path, basename: str) -> tuple[Path, Path]:
    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    write_json(json_path, summary)
    markdown_path.write_text(render_markdown(summary), encoding="utf-8")
    return json_path, markdown_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run pending owner-approved no-write LLM worker-chain handoffs.")
    parser.add_argument("--reports-dir", default=str(REPORTS_DIR), help="Directory containing llm-topic-decision-*.json files.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for handoff-run artifacts.")
    parser.add_argument("--basename", default="llm-approved-handoff-run", help="Aggregate summary basename.")
    parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider passed to no-write LLM worker chains.",
    )
    parser.add_argument("--max-handoffs", type=int, default=3, help="Maximum pending handoffs to run in one execution.")
    parser.add_argument("--include-current", action="store_true", help="Rerun handoffs even when a current chain summary exists.")
    parser.add_argument("--editor-fixture", help="Fixture response JSON for offline Editor tests.")
    parser.add_argument("--reviewer-fixture", help="Fixture response JSON for offline Reviewer tests.")
    parser.add_argument("--json", action="store_true", help="Print the handoff-run summary as JSON.")
    args = parser.parse_args()

    code, summary = run_approved_handoffs(
        reports_dir=resolve_path(args.reports_dir),
        output_dir=resolve_path(args.output_dir),
        provider=args.provider,
        max_handoffs=args.max_handoffs,
        include_current=args.include_current,
        basename=args.basename,
        editor_fixture_path=resolve_path(args.editor_fixture) if args.editor_fixture else None,
        reviewer_fixture_path=resolve_path(args.reviewer_fixture) if args.reviewer_fixture else None,
    )
    output = {
        "state": summary["state"],
        "provider": summary["provider"],
        "approved_handoff_count": summary["approved_handoff_count"],
        "pending_handoff_count": summary["pending_handoff_count"],
        "run_count": summary["run_count"],
        "success_count": summary["success_count"],
        "failure_count": summary["failure_count"],
        "skipped_current_count": summary["skipped_current_count"],
        "deferred_count": summary["deferred_count"],
        "artifacts": summary.get("artifacts", {}),
        "safety": summary["safety"],
    }
    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"State: {output['state']}")
        print(f"Approved handoffs: {output['approved_handoff_count']}")
        print(f"Run count: {output['run_count']}")
        print(f"Skipped current: {output['skipped_current_count']}")
        print(f"Summary: {output['artifacts'].get('handoff_run_markdown')}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())

