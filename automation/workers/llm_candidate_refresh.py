#!/usr/bin/env python3
"""No-write weekly candidate refresh for LLM-assisted topic discovery."""

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

from automation.io import write_json
from automation.proposal_renderer import md_list
from automation.workers import llm_scout, llm_topic_discovery


REPORTS_DIR = ROOT / "automation" / "reports"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def stage_summary(name: str, code: int, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": name,
        "state": payload.get("state") or payload.get("adapter_result", {}).get("state") or ("completed" if code == 0 else "blocked"),
        "returncode": code,
        "request_path": payload.get("request_path"),
        "result_path": payload.get("result_path"),
        "output_path": payload.get("output_path"),
        "markdown_path": payload.get("markdown_path"),
        "errors": payload.get("errors") or payload.get("adapter_result", {}).get("errors", []),
    }


def topic_ids(topics: list[dict[str, Any]], status: str) -> list[str]:
    return [str(topic.get("topic_id", "")) for topic in topics if topic.get("status") == status and topic.get("topic_id")]


def blocked_payload(
    output_dir: Path,
    basename: str,
    errors: list[str],
    stages: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    return {
        "schema_version": 1,
        "report_type": "llm_candidate_refresh",
        "generated_at": now_utc(),
        "state": "blocked",
        "provider": "",
        "source_signal_files": [],
        "candidate_topic_count": 0,
        "monitor_topic_count": 0,
        "candidate_topic_ids": [],
        "monitor_topic_ids": [],
        "stages": stages or [],
        "errors": errors,
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": False,
        "allows_pr_or_deploy": False,
        "next_actions": [
            "Fix the blocked candidate refresh stage, then rerun llm-candidate-refresh.",
        ],
        "safety": "No content, backlog, manifest, PR, or production files were modified by LLM candidate refresh.",
    }


def build_payload(
    provider: str,
    signal_paths: list[Path],
    output_dir: Path,
    basename: str,
    scout_payload: dict[str, Any],
    scout_code: int,
    discovery_payload: dict[str, Any] | None,
    discovery_code: int | None,
) -> dict[str, Any]:
    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    stages = [stage_summary("llm_scout", scout_code, scout_payload)]
    if discovery_payload is not None and discovery_code is not None:
        stages.append(stage_summary("llm_topic_discovery", discovery_code, discovery_payload))

    errors: list[str] = []
    for stage in stages:
        errors.extend(str(error) for error in stage.get("errors", []) if error)

    topics = discovery_payload.get("topics", []) if discovery_payload else []
    candidates = topic_ids(topics, "candidate")
    monitors = topic_ids(topics, "monitor")
    state = "candidate_refresh_ready" if scout_code == 0 and discovery_code == 0 else "blocked"
    next_actions = [
        f"Review `{discovery_payload.get('markdown_path')}` before approving any topic." if discovery_payload else "Review the Scout errors before rerunning discovery.",
        "Record owner decisions with `python3 automation/pipeline.py llm-topic-decision --topic-id <topic_id> --state monitor|approved_for_chain|rejected --decided-by <name> --json`.",
        "Only `approved_for_chain` topics may move to the no-write llm-worker-chain stage.",
        "Public content edits still require exact proposed text, explicit owner approval, apply-preview, apply-approved, and strict QA.",
    ]
    return {
        "schema_version": 1,
        "report_type": "llm_candidate_refresh",
        "generated_at": now_utc(),
        "state": state,
        "provider": provider,
        "source_signal_files": [rel(path) for path in signal_paths],
        "source_proposal_count": scout_payload.get("source_proposal_count", 0),
        "candidate_topic_count": len(candidates),
        "monitor_topic_count": len(monitors),
        "candidate_topic_ids": candidates,
        "monitor_topic_ids": monitors,
        "topic_discovery_path": discovery_payload.get("output_path") if discovery_payload else "",
        "topic_discovery_markdown": discovery_payload.get("markdown_path") if discovery_payload else "",
        "stages": stages,
        "errors": errors,
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": False,
        "allows_pr_or_deploy": False,
        "next_actions": next_actions,
        "safety": "No content, backlog, manifest, PR, or production files were modified by LLM candidate refresh.",
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# LLM Candidate Refresh - {payload['generated_at']}",
        "",
        "## Overview",
        "",
        f"- State: `{payload['state']}`",
        f"- Provider: `{payload.get('provider', '')}`",
        f"- Source proposals: {payload.get('source_proposal_count', 0)}",
        f"- Candidate topics: {payload.get('candidate_topic_count', 0)}",
        f"- Monitor topics: {payload.get('monitor_topic_count', 0)}",
        f"- Topic discovery: `{payload.get('topic_discovery_markdown', '')}`",
        "- Allows content edit: `false`",
        "- Allows backlog mutation: `false`",
        "- Allows manifest mutation: `false`",
        "- Allows PR/deploy: `false`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if payload.get("source_signal_files"):
        lines.extend(["## Source Signals", "", md_list(payload["source_signal_files"]), ""])
    if payload.get("candidate_topic_ids"):
        lines.extend(["## Candidate Topics", "", md_list(payload["candidate_topic_ids"]), ""])
    if payload.get("monitor_topic_ids"):
        lines.extend(["## Monitor Topics", "", md_list(payload["monitor_topic_ids"]), ""])
    if payload.get("errors"):
        lines.extend(["## Errors", "", md_list(payload["errors"]), ""])
    lines.extend(["## Stages", ""])
    for stage in payload.get("stages", []):
        lines.extend(
            [
                f"### {stage['stage']}",
                "",
                f"- State: `{stage.get('state', '')}`",
                f"- Return code: `{stage.get('returncode', '')}`",
                f"- Request: `{stage.get('request_path') or ''}`",
                f"- Result: `{stage.get('result_path') or stage.get('output_path') or ''}`",
                f"- Markdown: `{stage.get('markdown_path') or ''}`",
                "",
            ]
        )
    lines.extend(["## Next Actions", "", md_list(payload.get("next_actions", [])), ""])
    return "\n".join(lines)


def write_refresh(payload: dict[str, Any]) -> tuple[Path, Path]:
    json_path = resolve_path(payload["output_path"])
    markdown_path = resolve_path(payload["markdown_path"])
    json_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(json_path, payload)
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return json_path, markdown_path


def run_candidate_refresh(
    signal_paths: list[Path],
    output_dir: Path,
    basename: str,
    scout_basename: str,
    discovery_basename: str,
    provider: str,
    fixture_path: Path | None,
    limit: int,
    min_impressions: int,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not signal_paths:
        payload = blocked_payload(output_dir, basename, ["No Scout signal files were found."])
        write_refresh(payload)
        return 1, payload

    scout_code, scout_payload = llm_scout.run_llm_scout(
        signal_paths=signal_paths,
        output_dir=output_dir,
        basename=scout_basename,
        provider=provider,
        fixture_path=fixture_path,
        limit=limit,
        min_impressions=min_impressions,
    )
    discovery_payload: dict[str, Any] | None = None
    discovery_code: int | None = None
    if scout_code == 0:
        discovery_code, discovery_payload = llm_topic_discovery.run_topic_discovery(
            scout_result_path=resolve_path(str(scout_payload["result_path"])),
            scout_request_path=resolve_path(str(scout_payload["request_path"])),
            output_dir=output_dir,
            basename=discovery_basename,
        )

    payload = build_payload(
        provider=provider,
        signal_paths=signal_paths,
        output_dir=output_dir,
        basename=basename,
        scout_payload=scout_payload,
        scout_code=scout_code,
        discovery_payload=discovery_payload,
        discovery_code=discovery_code,
    )
    write_refresh(payload)
    return (0 if payload["state"] == "candidate_refresh_ready" else 1), payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a no-write LLM candidate refresh from latest Scout signals.")
    parser.add_argument(
        "--signals",
        action="append",
        help="Path to a GSC/Bing agent signals JSON file. Can be supplied more than once. Defaults to latest GSC and Bing when present.",
    )
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for candidate refresh artifacts.")
    parser.add_argument("--basename", default="llm-candidate-refresh", help="Refresh summary basename without extension.")
    parser.add_argument("--scout-basename", default="llm-candidate-refresh-scout", help="LLM Scout basename without extension.")
    parser.add_argument(
        "--discovery-basename",
        default="llm-candidate-refresh-topic-discovery",
        help="LLM topic discovery basename without extension.",
    )
    parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider passed to llm_adapter through LLM Scout. Defaults to disabled/fail-closed.",
    )
    parser.add_argument("--fixture", help="Fixture response JSON for offline Scout provider tests.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum deterministic Scout proposals to review.")
    parser.add_argument("--min-impressions", type=int, default=200, help="Minimum page impressions for Scout proposals.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    signal_paths = [resolve_path(value) for value in args.signals] if args.signals else llm_scout.default_signal_paths()
    fixture_path = resolve_path(args.fixture) if args.fixture else None
    code, payload = run_candidate_refresh(
        signal_paths=signal_paths,
        output_dir=resolve_path(args.output_dir),
        basename=args.basename,
        scout_basename=args.scout_basename,
        discovery_basename=args.discovery_basename,
        provider=args.provider,
        fixture_path=fixture_path,
        limit=args.limit,
        min_impressions=args.min_impressions,
    )
    summary = {
        "state": payload["state"],
        "provider": payload.get("provider", ""),
        "candidate_topic_count": payload["candidate_topic_count"],
        "monitor_topic_count": payload["monitor_topic_count"],
        "candidate_topic_ids": payload["candidate_topic_ids"],
        "monitor_topic_ids": payload["monitor_topic_ids"],
        "output_path": payload["output_path"],
        "markdown_path": payload["markdown_path"],
        "topic_discovery_path": payload.get("topic_discovery_path", ""),
        "topic_discovery_markdown": payload.get("topic_discovery_markdown", ""),
        "errors": payload.get("errors", []),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Provider: {summary['provider']}")
        print(f"Candidate topics: {summary['candidate_topic_count']}")
        print(f"Monitor topics: {summary['monitor_topic_count']}")
        print(f"Output: {summary['output_path']}")
        print(f"Markdown: {summary['markdown_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
