#!/usr/bin/env python3
"""No-write LLM Scout reviewer for deterministic Scout proposals."""

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
from automation.workers import llm_adapter, scout


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_GSC_SIGNALS = ROOT / "content" / "gsc" / "latest-gsc-agent-signals.json"
DEFAULT_BING_SIGNALS = ROOT / "content" / "bing" / "latest-bing-agent-signals.json"
READY_DECISIONS = {"update_existing", "create_new", "consolidate"}
MONITOR_DECISIONS = {"monitor", "reject"}


SCOUT_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "overview": {
            "type": "string",
            "maxLength": 600,
            "description": "Brief synthesis of the strongest content opportunities and why they matter.",
        },
        "selected_opportunities": {
            "type": "array",
            "maxItems": 3,
            "description": "Highest-value opportunities that are worth human review.",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "topic_id": {"type": "string", "maxLength": 120},
                    "decision": {
                        "type": "string",
                        "enum": ["update_existing", "create_new", "consolidate", "monitor", "reject"],
                    },
                    "rationale": {"type": "string", "maxLength": 500},
                    "player_value": {"type": "string", "maxLength": 400},
                    "duplication_risk": {"type": "string", "maxLength": 350},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                    "risk_level": {"type": "string", "enum": ["high", "medium", "low"]},
                    "next_step": {"type": "string", "maxLength": 300},
                    "claims_to_verify": {
                        "type": "array",
                        "maxItems": 5,
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "topic_id",
                    "decision",
                    "rationale",
                    "player_value",
                    "duplication_risk",
                    "priority",
                    "risk_level",
                    "next_step",
                    "claims_to_verify",
                ],
            },
        },
        "rejected_or_monitor": {
            "type": "array",
            "maxItems": 5,
            "description": "Opportunities that should not move forward now.",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "topic_id": {"type": "string", "maxLength": 120},
                    "reason": {"type": "string", "maxLength": 350},
                    "future_trigger": {"type": "string", "maxLength": 250},
                },
                "required": ["topic_id", "reason", "future_trigger"],
            },
        },
        "global_risks": {
            "type": "array",
            "maxItems": 5,
            "items": {"type": "string", "maxLength": 300},
        },
        "next_actions": {
            "type": "array",
            "maxItems": 5,
            "items": {"type": "string", "maxLength": 300},
        },
    },
    "required": [
        "overview",
        "selected_opportunities",
        "rejected_or_monitor",
        "global_risks",
        "next_actions",
    ],
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def default_signal_paths() -> list[Path]:
    return [path for path in [DEFAULT_GSC_SIGNALS, DEFAULT_BING_SIGNALS] if path.exists()]


def proposal_key(proposal: dict[str, Any]) -> tuple[str, str]:
    return (str(proposal.get("target_page_or_slug", "")), str(proposal.get("source_reference", "")))


def build_source_proposals(signal_paths: list[Path], limit: int, min_impressions: int) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for path in signal_paths:
        payload = scout.build_payload(path, limit=limit, min_impressions=min_impressions)
        for proposal in payload.get("proposals", []):
            key = proposal_key(proposal)
            if key in seen:
                continue
            proposals.append(proposal)
            seen.add(key)
    proposals.sort(
        key=lambda item: (
            {"high": 0, "medium": 1, "low": 2}.get(str(item.get("priority")), 3),
            {"high": 0, "medium": 1, "low": 2}.get(str(item.get("confidence")), 3),
            str(item.get("topic_id", "")),
        )
    )
    return proposals[:limit]


def load_external_proposals(paths: list[Path]) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    supported_report_types = {"external_scout", "external_search_collect"}
    for path in paths:
        payload = load_json(path)
        if payload.get("report_type") not in supported_report_types:
            raise ValueError(f"Unsupported external proposals report type in {rel(path)}: {payload.get('report_type')}")
        for proposal in payload.get("candidate_proposals", []):
            if not isinstance(proposal, dict):
                continue
            proposals.append(proposal)
    return proposals


def merge_proposals(source_proposals: list[dict[str, Any]], external_proposals: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for proposal in source_proposals + external_proposals:
        key = proposal_key(proposal)
        if key in seen:
            continue
        merged.append(proposal)
        seen.add(key)
    merged.sort(
        key=lambda item: (
            {"high": 0, "medium": 1, "low": 2}.get(str(item.get("priority")), 3),
            {"high": 0, "medium": 1, "low": 2}.get(str(item.get("confidence")), 3),
            str(item.get("topic_id", "")),
        )
    )
    return merged[:limit]


def compact_proposal(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "topic_id": proposal.get("topic_id", ""),
        "title": proposal.get("title", ""),
        "cluster": proposal.get("cluster", ""),
        "recommended_action": proposal.get("recommended_action", ""),
        "archetype_suggestion": proposal.get("archetype_suggestion", ""),
        "target_page_or_slug": proposal.get("target_page_or_slug", ""),
        "source_reference": proposal.get("source_reference", ""),
        "confidence": proposal.get("confidence", ""),
        "priority": proposal.get("priority", ""),
        "risk_level": proposal.get("risk_level", ""),
        "evidence": proposal.get("evidence", [])[:5],
        "site_fit": proposal.get("site_fit", {}),
        "constraints": proposal.get("constraints", []),
        "reject_if": proposal.get("reject_if", []),
    }


def normalized_decision(value: Any) -> str:
    decision = str(value or "").strip().lower()
    return decision if decision in READY_DECISIONS | MONITOR_DECISIONS else ""


def is_ready_for_chain(item: dict[str, Any]) -> bool:
    return normalized_decision(item.get("decision")) in READY_DECISIONS and str(item.get("priority", "")).lower() != "low"


def ready_topic_ids(response: dict[str, Any]) -> list[str]:
    selected = response.get("selected_opportunities", [])
    if not isinstance(selected, list):
        return []
    return [
        str(item.get("topic_id", ""))
        for item in selected
        if item.get("topic_id") and is_ready_for_chain(item)
    ]


def monitor_only_topic_ids(response: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    selected = response.get("selected_opportunities", [])
    if isinstance(selected, list):
        ids.extend(
            str(item.get("topic_id", ""))
            for item in selected
            if item.get("topic_id") and not is_ready_for_chain(item)
        )
    rejected_or_monitor = response.get("rejected_or_monitor", [])
    if isinstance(rejected_or_monitor, list):
        ids.extend(str(item.get("topic_id", "")) for item in rejected_or_monitor if item.get("topic_id"))
    return ids


def build_request(
    source_proposals: list[dict[str, Any]],
    signal_paths: list[Path],
    external_proposal_paths: list[Path],
    request_id: str,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "request_id": request_id,
        "worker_role": "scout",
        "task": "Review deterministic Scout topic proposals and select only opportunities worth human review.",
        "prompt": (
            "Act as the LLM Scout reviewer for lastzguides.com. Use the deterministic proposals as signals, "
            "not proof. Prefer updates to existing pages unless there is a clearly distinct player job. "
            "Protect current templates, cluster roles, canonical claims, SEO/LLM search eligibility, and human approval gates. "
            "Reject thin, duplicate, speculative, or analytics-only ideas. Put monitor/reject decisions in rejected_or_monitor, "
            "not selected_opportunities. Only select update_existing, create_new, or consolidate opportunities that are ready for "
            "human review and a later proposal-only workflow. Use plain ASCII English only. Return JSON only."
        ),
        "inputs": {
            "source_signal_files": [rel(path) for path in signal_paths],
            "external_proposal_files": [rel(path) for path in external_proposal_paths],
            "proposal_count": len(source_proposals),
            "proposals": [compact_proposal(proposal) for proposal in source_proposals],
            "guardrails": [
                "No content files may be edited by Scout.",
                "No backlog, manifest, PR, or production state may be changed by Scout.",
                "User-visible content proposals require owner approval before any apply step.",
                "Do not use archived Reddit/news experiments as inputs or targets.",
                "Treat GSC and Bing as opportunity signals, not as instructions to rewrite pages.",
                "Treat external-source proposals as discovery and cross-validation signals, not as copy sources.",
                "Do not use a single external source as proof for public mechanic, cost, reward, season, or event claims.",
                "Reject external-source ideas that cannot be verified or would copy competitor wording.",
                "Monitor-only and reject topics must not advance to Editor, Reviewer, intake, run-plan, or content proposal.",
                "Use plain ASCII English only in every string field.",
            ],
        },
        "expected_response_keys": [
            "overview",
            "selected_opportunities",
            "rejected_or_monitor",
            "global_risks",
            "next_actions",
        ],
        "response_schema": SCOUT_RESPONSE_SCHEMA,
        "max_output_tokens": 4000,
    }


def validate_scout_response(result: dict[str, Any], source_topic_ids: set[str]) -> list[str]:
    errors: list[str] = []
    response = result.get("response_json")
    if result.get("state") != "completed" or not isinstance(response, dict):
        return errors
    selected = response.get("selected_opportunities", [])
    monitor = response.get("rejected_or_monitor", [])
    if not isinstance(selected, list):
        errors.append("Response `selected_opportunities` must be a list.")
    if not isinstance(monitor, list):
        errors.append("Response `rejected_or_monitor` must be a list.")
    for item in selected if isinstance(selected, list) else []:
        topic_id = str(item.get("topic_id", ""))
        if topic_id not in source_topic_ids:
            errors.append(f"Selected topic `{topic_id}` was not present in deterministic Scout proposals.")
        decision = normalized_decision(item.get("decision"))
        if decision in MONITOR_DECISIONS:
            errors.append(f"Selected topic `{topic_id}` has monitor/reject decision `{decision}`; move it to rejected_or_monitor.")
    for item in monitor if isinstance(monitor, list) else []:
        topic_id = str(item.get("topic_id", ""))
        if topic_id and topic_id not in source_topic_ids:
            errors.append(f"Monitor/reject topic `{topic_id}` was not present in deterministic Scout proposals.")
    return errors


def render_markdown(payload: dict[str, Any]) -> str:
    result = payload["adapter_result"]
    response = result.get("response_json") or {}
    lines = [
        f"# LLM Scout Review - {payload['generated_at']}",
        "",
        "## Overview",
        "",
        f"- State: `{result.get('state')}`",
        f"- Provider: `{result.get('provider')}`",
        f"- Source proposals: {payload['source_proposal_count']}",
        f"- Ready for chain: {len(payload.get('ready_topic_ids', []))}",
        f"- Monitor only: {len(payload.get('monitor_only_topic_ids', []))}",
        f"- Request: `{payload['request_path']}`",
        f"- Result: `{payload['result_path']}`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if result.get("errors"):
        lines.extend(["## Errors", "", md_list(result["errors"]), ""])
    if response:
        lines.extend(
            [
                "## LLM Summary",
                "",
                response.get("overview", ""),
                "",
                "## Selected Opportunities",
                "",
            ]
        )
        selected = response.get("selected_opportunities", [])
        if selected:
            for item in selected:
                lines.extend(
                    [
                        f"### {item.get('topic_id', '')}",
                        "",
                        f"- Decision: `{item.get('decision', '')}`",
                        f"- Ready for chain: `{str(is_ready_for_chain(item)).lower()}`",
                        f"- Priority: `{item.get('priority', '')}`",
                        f"- Risk: `{item.get('risk_level', '')}`",
                        f"- Player value: {item.get('player_value', '')}",
                        f"- Duplication risk: {item.get('duplication_risk', '')}",
                        f"- Next step: {item.get('next_step', '')}",
                        "",
                        "Rationale:",
                        "",
                        item.get("rationale", ""),
                        "",
                        "Claims to verify:",
                        md_list(item.get("claims_to_verify", [])),
                        "",
                    ]
                )
        else:
            lines.extend(["- None", ""])
        lines.extend(["## Rejected Or Monitor", "", md_list([
            f"{item.get('topic_id', '')}: {item.get('reason', '')} Future trigger: {item.get('future_trigger', '')}"
            for item in response.get("rejected_or_monitor", [])
        ]), ""])
        lines.extend(["## Global Risks", "", md_list(response.get("global_risks", [])), ""])
        lines.extend(["## Next Actions", "", md_list(response.get("next_actions", [])), ""])
    return "\n".join(lines)


def run_llm_scout(
    signal_paths: list[Path],
    external_proposal_paths: list[Path],
    output_dir: Path,
    basename: str,
    provider: str,
    fixture_path: Path | None,
    limit: int,
    min_impressions: int,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_proposals = build_source_proposals(signal_paths, limit=limit, min_impressions=min_impressions)
    external_proposals = load_external_proposals(external_proposal_paths) if external_proposal_paths else []
    source_proposals = merge_proposals(source_proposals, external_proposals, limit=limit)
    request_path = output_dir / f"{basename}-request.json"
    result_path = output_dir / f"{basename}-result.json"
    markdown_path = output_dir / f"{basename}.md"

    request = build_request(source_proposals, signal_paths, external_proposal_paths, request_id=basename)
    write_json(request_path, request)
    code, result = llm_adapter.run_adapter(request_path, provider, fixture_path)
    validation_errors = validate_scout_response(result, {str(proposal["topic_id"]) for proposal in source_proposals})
    if validation_errors:
        result = llm_adapter.blocked_result(request, provider, validation_errors, request_path)
        code = 1
    write_json(result_path, result)

    payload = {
        "schema_version": 1,
        "report_type": "llm_scout_review",
        "generated_at": now_utc(),
        "source_signal_files": [rel(path) for path in signal_paths],
        "external_proposal_files": [rel(path) for path in external_proposal_paths],
        "source_proposal_count": len(source_proposals),
        "external_proposal_count": len(external_proposals),
        "source_topic_ids": [proposal.get("topic_id", "") for proposal in source_proposals],
        "ready_topic_ids": ready_topic_ids(result.get("response_json") or {}),
        "monitor_only_topic_ids": monitor_only_topic_ids(result.get("response_json") or {}),
        "request_path": rel(request_path),
        "result_path": rel(result_path),
        "markdown_path": rel(markdown_path),
        "adapter_result": result,
        "safety": "No content, backlog, manifest, PR, or production files were modified by LLM Scout.",
    }
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return code, payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a no-write LLM Scout review over deterministic Scout proposals.")
    parser.add_argument(
        "--signals",
        action="append",
        help="Path to a GSC/Bing agent signals JSON file. Can be supplied more than once. Defaults to latest GSC and Bing when present.",
    )
    parser.add_argument(
        "--external-proposals",
        action="append",
        help="Path to an External Scout JSON artifact with candidate_proposals. Can be supplied more than once.",
    )
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for LLM Scout artifacts.")
    parser.add_argument("--basename", default="llm-scout-review", help="Output basename without extension.")
    parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider passed to llm_adapter. Defaults to disabled/fail-closed.",
    )
    parser.add_argument("--fixture", help="Fixture response JSON for offline provider tests.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum deterministic proposals to review.")
    parser.add_argument("--min-impressions", type=int, default=200, help="Minimum page impressions for Scout proposals.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    signal_paths = [resolve_path(value) for value in args.signals] if args.signals else default_signal_paths()
    external_proposal_paths = [resolve_path(value) for value in args.external_proposals or []]
    if not signal_paths and not external_proposal_paths:
        print("No Scout signal files or external proposal files were found.", file=sys.stderr)
        return 1
    output_dir = resolve_path(args.output_dir)
    fixture_path = resolve_path(args.fixture) if args.fixture else None

    code, payload = run_llm_scout(
        signal_paths=signal_paths,
        external_proposal_paths=external_proposal_paths,
        output_dir=output_dir,
        basename=args.basename,
        provider=args.provider,
        fixture_path=fixture_path,
        limit=args.limit,
        min_impressions=args.min_impressions,
    )
    summary = {
        "state": payload["adapter_result"].get("state"),
        "provider": payload["adapter_result"].get("provider"),
        "source_proposal_count": payload["source_proposal_count"],
        "request_path": payload["request_path"],
        "result_path": payload["result_path"],
        "markdown_path": payload["markdown_path"],
        "errors": payload["adapter_result"].get("errors", []),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Provider: {summary['provider']}")
        print(f"Source proposals: {summary['source_proposal_count']}")
        print(f"Request: {summary['request_path']}")
        print(f"Result: {summary['result_path']}")
        print(f"Markdown: {summary['markdown_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
