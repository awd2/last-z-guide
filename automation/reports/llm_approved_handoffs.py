#!/usr/bin/env python3
"""Show approved LLM topic-decision handoffs ready for worker-chain replay."""

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

from automation.proposal_renderer import md_list
from automation.reports import llm_topic_decisions


REPORTS_DIR = ROOT / "automation" / "reports"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def command_for(decision: dict[str, Any], provider: str) -> str:
    return (
        "python3 automation/pipeline.py llm-worker-chain "
        f"--from-decision {decision['artifact_path']} "
        f"--provider {provider} --json"
    )


def build_view(reports_dir: Path, provider: str) -> dict[str, Any]:
    decisions_report = llm_topic_decisions.build_report(reports_dir)
    handoffs: list[dict[str, Any]] = []
    for decision in decisions_report.get("decisions", []):
        if not decision.get("allows_worker_chain"):
            continue
        handoffs.append(
            {
                "topic_id": decision.get("topic_id", ""),
                "target_page_or_slug": decision.get("target_page_or_slug", ""),
                "cluster": decision.get("cluster", ""),
                "priority": decision.get("priority", ""),
                "risk_level": decision.get("risk_level", ""),
                "decision_state": decision.get("decision_state", ""),
                "decision_artifact": decision.get("artifact_path", ""),
                "decision_markdown": decision.get("markdown_path", ""),
                "worker_chain_command": command_for(decision, provider),
            }
        )
    return {
        "schema_version": 1,
        "report_type": "llm_approved_handoffs",
        "generated_at": now_utc(),
        "provider": provider,
        "approved_handoff_count": len(handoffs),
        "handoffs": handoffs,
        "safety": "Read-only operator view. No content, backlog, manifest, PR, or production files were modified.",
    }


def render_markdown(view: dict[str, Any]) -> str:
    lines = [
        f"# LLM Approved Handoffs - {view['generated_at']}",
        "",
        "## Overview",
        "",
        f"- Approved handoffs: {view['approved_handoff_count']}",
        f"- Provider: `{view['provider']}`",
        "- Safety: read-only view; no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if not view.get("handoffs"):
        lines.extend(
            [
                "## Ready Commands",
                "",
                "- None. No topic decision is currently `approved_for_chain`.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(["## Ready Commands", ""])
    for handoff in view["handoffs"]:
        lines.extend(
            [
                f"### {handoff['topic_id']}",
                "",
                f"- Target: `{handoff['target_page_or_slug']}`",
                f"- Cluster: `{handoff['cluster']}`",
                f"- Priority: `{handoff['priority']}`",
                f"- Risk: `{handoff['risk_level']}`",
                f"- Decision artifact: `{handoff['decision_artifact']}`",
                "",
                "Run:",
                "",
                f"```bash\n{handoff['worker_chain_command']}\n```",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Show approved LLM topic-decision handoffs ready for worker-chain replay.")
    parser.add_argument("--reports-dir", default=str(REPORTS_DIR), help="Directory containing llm-topic-decision-*.json files.")
    parser.add_argument("--provider", default="openai", choices=["fixture", "openai"], help="Provider to include in printed worker-chain commands.")
    parser.add_argument("--json", action="store_true", help="Print approved handoffs as JSON.")
    args = parser.parse_args()

    view = build_view(resolve_path(args.reports_dir), args.provider)
    if args.json:
        print(json.dumps(view, indent=2))
    else:
        print(render_markdown(view))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
