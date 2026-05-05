#!/usr/bin/env python3
"""Record owner decisions for no-write LLM topic discovery proposals."""

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
DEFAULT_DISCOVERY = REPORTS_DIR / "llm-topic-discovery.json"
DECISION_STATES = {"approved_for_chain", "monitor", "rejected"}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def find_topic(discovery: dict[str, Any], topic_id: str) -> dict[str, Any] | None:
    for topic in discovery.get("topics", []):
        if topic.get("topic_id") == topic_id:
            return topic
    return None


def next_actions_for(topic_id: str, decision_state: str) -> list[str]:
    if decision_state == "approved_for_chain":
        return [
            f"Run the no-write LLM worker chain from this saved decision: python3 automation/pipeline.py llm-worker-chain --from-decision automation/reports/llm-topic-decision-{topic_id}.json --provider openai --json",
            "Review the generated LLM Reviewer gate before any intake, run-plan, or public content proposal.",
            "Public content still requires exact text/spec proposal, explicit owner approval, and strict checks.",
        ]
    if decision_state == "monitor":
        return [
            "Keep this topic out of content intake for now.",
            "Reconsider only after materially new GSC/Bing/query evidence or an explicit owner request.",
            "Do not create public content edits from this topic decision.",
        ]
    return [
        "Do not run this topic through the worker chain unless the owner explicitly reopens it.",
        "Keep future Scout output from reintroducing the same opportunity without materially new evidence.",
        "Do not create public content edits from this topic decision.",
    ]


def build_decision(
    discovery_path: Path,
    topic_id: str,
    decision_state: str,
    decided_by: str,
    note: str | None,
    output_dir: Path,
    basename: str | None,
) -> tuple[int, dict[str, Any]]:
    if decision_state not in DECISION_STATES:
        return 1, {
            "schema_version": 1,
            "report_type": "llm_topic_decision",
            "generated_at": now_utc(),
            "state": "blocked",
            "topic_id": topic_id,
            "decision_state": decision_state,
            "errors": [f"Unsupported decision state: {decision_state}"],
            "safety": "No content, backlog, manifest, PR, or production files were modified.",
        }

    discovery = load_json(discovery_path)
    topic = find_topic(discovery, topic_id)
    if not topic:
        return 1, {
            "schema_version": 1,
            "report_type": "llm_topic_decision",
            "generated_at": now_utc(),
            "state": "blocked",
            "topic_id": topic_id,
            "decision_state": decision_state,
            "source_discovery": rel(discovery_path),
            "errors": [f"Topic not found in discovery artifact: {topic_id}"],
            "safety": "No content, backlog, manifest, PR, or production files were modified.",
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_name = basename or f"llm-topic-decision-{topic_id}"
    json_path = output_dir / f"{output_name}.json"
    markdown_path = output_dir / f"{output_name}.md"
    state = "decision_recorded"
    payload = {
        "schema_version": 1,
        "report_type": "llm_topic_decision",
        "generated_at": now_utc(),
        "state": state,
        "topic_id": topic_id,
        "decision_state": decision_state,
        "decided_by": decided_by,
        "decision_note": note or "",
        "source_discovery": rel(discovery_path),
        "topic_snapshot": topic,
        "allows_worker_chain": decision_state == "approved_for_chain",
        "allows_content_edit": False,
        "next_actions": next_actions_for(topic_id, decision_state),
        "errors": [],
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "safety": "No content, backlog, manifest, PR, or production files were modified. This decision only controls whether a discovered topic may proceed to the next no-write worker stage.",
    }
    return 0, payload


def previous_decision_summary(payload: dict[str, Any], source_path: Path) -> dict[str, Any]:
    return {
        "source_path": rel(source_path),
        "generated_at": payload.get("generated_at", ""),
        "state": payload.get("state", ""),
        "topic_id": payload.get("topic_id", ""),
        "decision_state": payload.get("decision_state", ""),
        "decided_by": payload.get("decided_by", ""),
        "decision_note": payload.get("decision_note", ""),
        "allows_worker_chain": bool(payload.get("allows_worker_chain", False)),
        "allows_content_edit": bool(payload.get("allows_content_edit", False)),
    }


def build_decision_from_prior(
    prior_decision_path: Path,
    topic_id: str | None,
    decision_state: str,
    decided_by: str,
    note: str | None,
    output_dir: Path,
    basename: str | None,
) -> tuple[int, dict[str, Any]]:
    if decision_state not in DECISION_STATES:
        return 1, {
            "schema_version": 1,
            "report_type": "llm_topic_decision",
            "generated_at": now_utc(),
            "state": "blocked",
            "topic_id": topic_id or "",
            "decision_state": decision_state,
            "errors": [f"Unsupported decision state: {decision_state}"],
            "safety": "No content, backlog, manifest, PR, or production files were modified.",
        }

    prior = load_json(prior_decision_path)
    prior_topic_id = str(prior.get("topic_id") or "")
    if prior.get("report_type") != "llm_topic_decision":
        return 1, {
            "schema_version": 1,
            "report_type": "llm_topic_decision",
            "generated_at": now_utc(),
            "state": "blocked",
            "topic_id": topic_id or prior_topic_id,
            "decision_state": decision_state,
            "source_decision": rel(prior_decision_path),
            "errors": ["Source artifact is not an llm_topic_decision."],
            "safety": "No content, backlog, manifest, PR, or production files were modified.",
        }
    if topic_id and topic_id != prior_topic_id:
        return 1, {
            "schema_version": 1,
            "report_type": "llm_topic_decision",
            "generated_at": now_utc(),
            "state": "blocked",
            "topic_id": topic_id,
            "decision_state": decision_state,
            "source_decision": rel(prior_decision_path),
            "errors": [f"Requested topic `{topic_id}` does not match source decision topic `{prior_topic_id}`."],
            "safety": "No content, backlog, manifest, PR, or production files were modified.",
        }

    topic = prior.get("topic_snapshot")
    if not prior_topic_id or not isinstance(topic, dict):
        return 1, {
            "schema_version": 1,
            "report_type": "llm_topic_decision",
            "generated_at": now_utc(),
            "state": "blocked",
            "topic_id": topic_id or prior_topic_id,
            "decision_state": decision_state,
            "source_decision": rel(prior_decision_path),
            "errors": ["Source decision is missing topic_id or topic_snapshot."],
            "safety": "No content, backlog, manifest, PR, or production files were modified.",
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_name = basename or prior_decision_path.stem
    json_path = output_dir / f"{output_name}.json"
    markdown_path = output_dir / f"{output_name}.md"
    payload = {
        "schema_version": 1,
        "report_type": "llm_topic_decision",
        "generated_at": now_utc(),
        "state": "decision_recorded",
        "topic_id": prior_topic_id,
        "decision_state": decision_state,
        "decided_by": decided_by,
        "decision_note": note or "",
        "source_discovery": prior.get("source_discovery", ""),
        "source_decision": rel(prior_decision_path),
        "previous_decision": previous_decision_summary(prior, prior_decision_path),
        "topic_snapshot": topic,
        "allows_worker_chain": decision_state == "approved_for_chain",
        "allows_content_edit": False,
        "next_actions": next_actions_for(prior_topic_id, decision_state),
        "errors": [],
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "safety": "No content, backlog, manifest, PR, or production files were modified. This decision only controls whether a discovered topic may proceed to the next no-write worker stage.",
    }
    return 0, payload


def render_markdown(payload: dict[str, Any]) -> str:
    topic = payload.get("topic_snapshot") or {}
    lines = [
        f"# LLM Topic Decision - {payload.get('topic_id', '')}",
        "",
        "## Decision",
        "",
        f"- State: `{payload.get('state', '')}`",
        f"- Decision: `{payload.get('decision_state', '')}`",
        f"- Decided by: `{payload.get('decided_by', '')}`",
        f"- Source discovery: `{payload.get('source_discovery', '')}`",
        f"- Source decision: `{payload.get('source_decision', '')}`",
        f"- Allows worker chain: `{str(payload.get('allows_worker_chain', False)).lower()}`",
        f"- Allows content edit: `{str(payload.get('allows_content_edit', False)).lower()}`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if payload.get("decision_note"):
        lines.extend(["Decision note:", "", payload["decision_note"], ""])
    if payload.get("previous_decision"):
        previous = payload["previous_decision"]
        lines.extend(
            [
                "Previous decision:",
                "",
                f"- Source: `{previous.get('source_path', '')}`",
                f"- Decision: `{previous.get('decision_state', '')}`",
                f"- Decided by: `{previous.get('decided_by', '')}`",
                f"- Generated at: `{previous.get('generated_at', '')}`",
                "",
            ]
        )
    if payload.get("errors"):
        lines.extend(["## Errors", "", md_list(payload["errors"]), ""])
    if topic:
        lines.extend(
            [
                "## Topic Snapshot",
                "",
                f"- Title: {topic.get('title', '')}",
                f"- Target: `{topic.get('target_page_or_slug', '')}`",
                f"- Cluster: `{topic.get('cluster', '')}`",
                f"- Action: `{topic.get('recommended_action', '')}`",
                f"- Priority: `{topic.get('priority', '')}`",
                f"- Risk: `{topic.get('risk_level', '')}`",
                f"- Status at discovery: `{topic.get('status', '')}`",
                "",
                "Rationale:",
                "",
                topic.get("notes", ""),
                "",
            ]
        )
    lines.extend(["## Next Actions", "", md_list(payload.get("next_actions", [])), ""])
    return "\n".join(lines)


def write_decision(payload: dict[str, Any], output_dir: Path, basename: str | None) -> tuple[Path, Path]:
    if payload.get("output_path"):
        json_path = resolve_path(payload["output_path"])
        markdown_path = resolve_path(payload["markdown_path"])
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_name = basename or f"llm-topic-decision-{payload.get('topic_id', 'blocked')}"
        json_path = output_dir / f"{output_name}.json"
        markdown_path = output_dir / f"{output_name}.md"
        payload["output_path"] = rel(json_path)
        payload["markdown_path"] = rel(markdown_path)
    write_json(json_path, payload)
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return json_path, markdown_path


def run_topic_decision(
    discovery_path: Path,
    topic_id: str | None,
    decision_state: str,
    decided_by: str,
    note: str | None,
    output_dir: Path,
    basename: str | None,
    from_decision_path: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    if from_decision_path:
        code, payload = build_decision_from_prior(
            prior_decision_path=from_decision_path,
            topic_id=topic_id,
            decision_state=decision_state,
            decided_by=decided_by,
            note=note,
            output_dir=output_dir,
            basename=basename,
        )
    else:
        if not topic_id:
            code, payload = 1, {
                "schema_version": 1,
                "report_type": "llm_topic_decision",
                "generated_at": now_utc(),
                "state": "blocked",
                "topic_id": "",
                "decision_state": decision_state,
                "source_discovery": rel(discovery_path),
                "errors": ["--topic-id is required when --from-decision is not supplied."],
                "safety": "No content, backlog, manifest, PR, or production files were modified.",
            }
        else:
            code, payload = build_decision(
                discovery_path=discovery_path,
                topic_id=topic_id,
                decision_state=decision_state,
                decided_by=decided_by,
                note=note,
                output_dir=output_dir,
                basename=basename,
            )
    write_decision(payload, output_dir, basename)
    return code, payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Record an owner decision for one LLM topic discovery proposal.")
    parser.add_argument("--discovery", default=str(DEFAULT_DISCOVERY), help="Path to llm-topic-discovery.json.")
    parser.add_argument("--from-decision", help="Path to an existing llm-topic-decision-<topic_id>.json artifact to rerecord.")
    parser.add_argument("--topic-id", help="Discovered topic_id to decide. Required unless --from-decision is supplied.")
    parser.add_argument(
        "--state",
        required=True,
        choices=sorted(DECISION_STATES),
        help="Owner decision for this topic.",
    )
    parser.add_argument("--decided-by", required=True, help="Human owner/operator name or handle.")
    parser.add_argument("--note", help="Optional decision note.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for decision artifacts.")
    parser.add_argument("--basename", help="Output basename without extension.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, payload = run_topic_decision(
        discovery_path=resolve_path(args.discovery),
        topic_id=args.topic_id,
        decision_state=args.state,
        decided_by=args.decided_by,
        note=args.note,
        output_dir=resolve_path(args.output_dir),
        basename=args.basename,
        from_decision_path=resolve_path(args.from_decision) if args.from_decision else None,
    )
    summary = {
        "state": payload["state"],
        "topic_id": payload["topic_id"],
        "decision_state": payload["decision_state"],
        "allows_worker_chain": payload.get("allows_worker_chain", False),
        "output_path": payload.get("output_path"),
        "markdown_path": payload.get("markdown_path"),
        "errors": payload.get("errors", []),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Topic: {summary['topic_id']}")
        print(f"Decision: {summary['decision_state']}")
        print(f"Allows worker chain: {'yes' if summary['allows_worker_chain'] else 'no'}")
        print(f"Output: {summary['output_path']}")
        print(f"Markdown: {summary['markdown_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
