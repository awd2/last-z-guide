#!/usr/bin/env python3
"""Run the no-write LLM Scout -> Editor -> Reviewer worker chain."""

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
from automation.workers import llm_editor, llm_reviewer, llm_scout


REPORTS_DIR = ROOT / "automation" / "reports"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def first_selected_topic(scout_payload: dict[str, Any]) -> str:
    response = scout_payload.get("adapter_result", {}).get("response_json")
    if not isinstance(response, dict):
        raise ValueError("LLM Scout did not return response_json.")
    selected = response.get("selected_opportunities", [])
    if not selected:
        raise ValueError("LLM Scout returned no selected opportunities.")
    topic_id = selected[0].get("topic_id")
    if not topic_id:
        raise ValueError("First selected LLM Scout opportunity does not have topic_id.")
    return str(topic_id)


def first_ready_topic(scout_payload: dict[str, Any]) -> str:
    response = scout_payload.get("adapter_result", {}).get("response_json")
    if not isinstance(response, dict):
        raise ValueError("LLM Scout did not return response_json.")
    ready = llm_scout.ready_topic_ids(response)
    if not ready:
        raise ValueError(
            "LLM Scout returned no ready-for-chain opportunities; monitor-only topics were not advanced."
        )
    return ready[0]


def selected_topic_ids(scout_payload: dict[str, Any]) -> set[str]:
    response = scout_payload.get("adapter_result", {}).get("response_json")
    if not isinstance(response, dict):
        return set()
    selected = response.get("selected_opportunities", [])
    if not isinstance(selected, list):
        return set()
    return {
        str(item.get("topic_id", ""))
        for item in selected
        if item.get("topic_id")
    }


def ready_topic_ids(scout_payload: dict[str, Any]) -> set[str]:
    response = scout_payload.get("adapter_result", {}).get("response_json")
    if not isinstance(response, dict):
        return set()
    return set(llm_scout.ready_topic_ids(response))


def normalized_priority(value: Any) -> str:
    text = str(value or "").strip().lower()
    return text if text in {"high", "medium", "low"} else "medium"


def normalized_risk(value: Any) -> str:
    text = str(value or "").strip().lower()
    return text if text in {"high", "medium", "low"} else "high"


def normalized_action(value: Any) -> str:
    text = str(value or "").strip().lower()
    allowed = {"update_existing", "create_new", "consolidate", "monitor", "reject"}
    return text if text in allowed else "update_existing"


def selected_opportunity_from_decision(decision: dict[str, Any], topic: dict[str, Any]) -> dict[str, Any]:
    note = str(decision.get("decision_note") or topic.get("notes") or "Owner-approved no-write worker-chain handoff.")
    site_fit = topic.get("site_fit") if isinstance(topic.get("site_fit"), dict) else {}
    return {
        "topic_id": str(topic.get("topic_id", "")),
        "decision": normalized_action(topic.get("recommended_action")),
        "rationale": note[:500],
        "player_value": str(topic.get("player_value") or site_fit.get("primary_user_job") or topic.get("title") or "")[:400],
        "duplication_risk": str(
            topic.get("duplication_risk")
            or "Review against the current cluster role before any content proposal."
        )[:350],
        "priority": normalized_priority(topic.get("priority")),
        "risk_level": normalized_risk(topic.get("risk_level")),
        "next_step": "Run the no-write Editor and Reviewer stages from this approved decision snapshot.",
        "claims_to_verify": topic.get("claims_to_verify", []) if isinstance(topic.get("claims_to_verify"), list) else [],
    }


def validate_decision_handoff(decision: dict[str, Any], topic_id: str | None) -> tuple[str, dict[str, Any]]:
    if decision.get("report_type") != "llm_topic_decision":
        raise ValueError("Decision handoff must point to an llm_topic_decision artifact.")
    if decision.get("state") != "decision_recorded":
        raise ValueError("Decision handoff is not recorded.")
    if decision.get("decision_state") != "approved_for_chain" or not decision.get("allows_worker_chain"):
        raise ValueError("Decision handoff is not approved_for_chain; worker chain cannot run.")
    topic = decision.get("topic_snapshot")
    if not isinstance(topic, dict):
        raise ValueError("Decision handoff is missing topic_snapshot.")
    decision_topic_id = str(decision.get("topic_id") or topic.get("topic_id") or "")
    snapshot_topic_id = str(topic.get("topic_id") or "")
    if not decision_topic_id or not snapshot_topic_id or decision_topic_id != snapshot_topic_id:
        raise ValueError("Decision handoff topic_id does not match topic_snapshot.topic_id.")
    if topic_id and topic_id != decision_topic_id:
        raise ValueError(f"Requested topic `{topic_id}` does not match decision topic `{decision_topic_id}`.")
    return decision_topic_id, topic


def write_decision_replay_scout(
    decision_path: Path,
    output_dir: Path,
    scout_basename: str,
    topic_id: str | None,
) -> tuple[str, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    decision = load_json(decision_path)
    source_topic_id, topic = validate_decision_handoff(decision, topic_id)
    request_path = output_dir / f"{scout_basename}-request.json"
    result_path = output_dir / f"{scout_basename}-result.json"
    markdown_path = output_dir / f"{scout_basename}.md"
    selected = selected_opportunity_from_decision(decision, topic)
    request = {
        "schema_version": 1,
        "request_id": scout_basename,
        "worker_role": "scout",
        "task": "Replay one owner-approved LLM topic decision as the Scout handoff for the no-write worker chain.",
        "prompt": (
            "This is a deterministic replay artifact created from a human-approved topic decision. "
            "No live Scout rerank is performed."
        ),
        "inputs": {
            "source_decision": rel(decision_path),
            "proposal_count": 1,
            "proposals": [topic],
            "guardrails": [
                "Only approved_for_chain decisions may be replayed.",
                "Replay does not approve public copy, patch specs, backlog edits, manifests, PRs, or deployment.",
                "Owner approval remains required before any user-visible content change.",
            ],
        },
        "expected_response_keys": [
            "overview",
            "selected_opportunities",
            "rejected_or_monitor",
            "global_risks",
            "next_actions",
        ],
        "response_schema": llm_scout.SCOUT_RESPONSE_SCHEMA,
        "max_output_tokens": 4000,
    }
    result = {
        "state": "completed",
        "provider": "decision_replay",
        "request_id": scout_basename,
        "response_json": {
            "overview": f"Deterministic replay of owner-approved topic decision `{source_topic_id}`.",
            "selected_opportunities": [selected],
            "rejected_or_monitor": [],
            "global_risks": [
                "This handoff only authorizes the next no-write worker-chain stage.",
                "It does not authorize content edits or publication.",
            ],
            "next_actions": ["Run the no-write Editor and Reviewer stages."],
        },
        "raw_response": None,
        "errors": [],
    }
    payload = {
        "schema_version": 1,
        "report_type": "llm_scout_review",
        "generated_at": now_utc(),
        "source_signal_files": [],
        "source_decision": rel(decision_path),
        "source_proposal_count": 1,
        "source_topic_ids": [source_topic_id],
        "request_path": rel(request_path),
        "result_path": rel(result_path),
        "markdown_path": rel(markdown_path),
        "adapter_result": result,
        "safety": "No content, backlog, manifest, PR, or production files were modified by LLM Scout decision replay.",
    }
    write_json(request_path, request)
    write_json(result_path, result)
    markdown_path.write_text(llm_scout.render_markdown(payload), encoding="utf-8")
    return source_topic_id, payload


def stage_summary(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not payload:
        return {
            "state": "not_run",
            "provider": None,
            "request_path": None,
            "result_path": None,
            "markdown_path": None,
            "errors": [],
        }
    result = payload.get("adapter_result", {})
    return {
        "state": result.get("state"),
        "provider": result.get("provider"),
        "request_path": payload.get("request_path"),
        "result_path": payload.get("result_path"),
        "markdown_path": payload.get("markdown_path"),
        "errors": result.get("errors", []),
    }


def response_json(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not payload:
        return {}
    response = payload.get("adapter_result", {}).get("response_json")
    return response if isinstance(response, dict) else {}


def build_summary(
    provider: str,
    topic_id: str | None,
    decision_path: Path | None,
    scout_payload: dict[str, Any] | None,
    editor_payload: dict[str, Any] | None,
    reviewer_payload: dict[str, Any] | None,
    generated_at: str,
    errors: list[str],
) -> dict[str, Any]:
    reviewer_response = response_json(reviewer_payload)
    editor_response = response_json(editor_payload)
    source_topic_id = topic_id or (editor_payload or {}).get("source_topic_id", "")
    target = (reviewer_payload or {}).get("target_page_or_slug") or (editor_payload or {}).get("target_page_or_slug", "")
    chain_state = "completed" if not errors and reviewer_payload else "blocked"
    return {
        "schema_version": 1,
        "report_type": "llm_worker_chain_summary",
        "generated_at": generated_at,
        "state": chain_state,
        "provider": provider,
        "handoff_source": "topic_decision" if decision_path else "live_scout",
        "source_decision": rel(decision_path) if decision_path else None,
        "source_topic_id": source_topic_id,
        "target_page_or_slug": target,
        "page_role": editor_response.get("page_role", ""),
        "review_verdict": reviewer_response.get("verdict"),
        "risk_level": reviewer_response.get("risk_level"),
        "approved_next_stage": reviewer_response.get("approved_next_stage"),
        "owner_approval_required": reviewer_response.get("owner_approval_required"),
        "errors": errors,
        "stages": {
            "llm_scout": stage_summary(scout_payload),
            "llm_editor": stage_summary(editor_payload),
            "llm_reviewer": stage_summary(reviewer_payload),
        },
        "safety": "No content, backlog, manifest, PR, or production files were modified by the LLM worker chain.",
    }


def render_markdown(summary: dict[str, Any], editor_response: dict[str, Any], reviewer_response: dict[str, Any]) -> str:
    stages = summary["stages"]
    stage_lines = [
        f"{name}: state `{stage.get('state')}`, request `{stage.get('request_path')}`, result `{stage.get('result_path')}`, markdown `{stage.get('markdown_path')}`"
        for name, stage in stages.items()
    ]
    error_lines = list(summary.get("errors", []))
    for name, stage in stages.items():
        for error in stage.get("errors", []):
            error_lines.append(f"{name}: {error}")
    blocking = [
        f"{item.get('severity', '')}: {item.get('issue', '')} Required fix: {item.get('required_fix', '')}"
        for item in reviewer_response.get("blocking_issues", [])
    ]
    lines = [
        f"# LLM Worker Chain - {summary.get('source_topic_id', '')}",
        "",
        "## Outcome",
        "",
        f"- State: `{summary.get('state')}`",
        f"- Provider: `{summary.get('provider')}`",
        f"- Handoff source: `{summary.get('handoff_source')}`",
        f"- Source decision: `{summary.get('source_decision')}`",
        f"- Target: `{summary.get('target_page_or_slug', '')}`",
        f"- Page role: `{summary.get('page_role', '')}`",
        f"- Review verdict: `{summary.get('review_verdict')}`",
        f"- Risk: `{summary.get('risk_level')}`",
        f"- Approved next stage: `{summary.get('approved_next_stage')}`",
        f"- Owner approval required: `{str(summary.get('owner_approval_required')).lower()}`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
        "## Stage Artifacts",
        "",
        md_list(stage_lines),
        "",
    ]
    if error_lines:
        lines.extend(["## Errors", "", md_list(error_lines), ""])
    if editor_response:
        lines.extend(
            [
                "## Editor Brief Summary",
                "",
                editor_response.get("brief_summary", ""),
                "",
                "## First-Screen Plan",
                "",
                editor_response.get("first_screen_plan", ""),
                "",
            ]
        )
    if reviewer_response:
        lines.extend(
            [
                "## Reviewer Blocking Issues",
                "",
                md_list(blocking),
                "",
                "## Reviewer Warnings",
                "",
                md_list(reviewer_response.get("warnings", [])),
                "",
                "## Owner Questions",
                "",
                md_list(reviewer_response.get("owner_questions", [])),
                "",
                "## Required Checks",
                "",
                md_list([f"`{check}`" for check in reviewer_response.get("required_checks", [])]),
                "",
                "## Next Step",
                "",
                reviewer_response.get("next_step", ""),
                "",
            ]
        )
    return "\n".join(lines)


def write_summary(summary: dict[str, Any], output_dir: Path, basename: str | None) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    topic_id = summary.get("source_topic_id") or "unselected"
    name = basename or f"llm-worker-chain-{topic_id}"
    json_path = output_dir / f"{name}.json"
    markdown_path = output_dir / f"{name}.md"
    summary["artifacts"] = {
        "chain_json": rel(json_path),
        "chain_markdown": rel(markdown_path),
    }
    write_json(json_path, summary)
    markdown_path.write_text(
        render_markdown(summary, response_json_from_stage(summary, "llm_editor"), response_json_from_stage(summary, "llm_reviewer")),
        encoding="utf-8",
    )
    return json_path, markdown_path


def response_json_from_stage(summary: dict[str, Any], stage_name: str) -> dict[str, Any]:
    result_path = summary.get("stages", {}).get(stage_name, {}).get("result_path")
    if not result_path:
        return {}
    path = resolve_path(result_path)
    if not path.exists():
        return {}
    result = load_json(path)
    response = result.get("response_json")
    return response if isinstance(response, dict) else {}


def run_llm_worker_chain(
    signal_paths: list[Path],
    output_dir: Path,
    provider: str,
    topic_id: str | None,
    basename: str | None,
    scout_basename: str,
    editor_basename: str | None,
    reviewer_basename: str | None,
    scout_fixture_path: Path | None,
    editor_fixture_path: Path | None,
    reviewer_fixture_path: Path | None,
    limit: int,
    min_impressions: int,
    decision_path: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    generated_at = now_utc()
    errors: list[str] = []
    scout_payload: dict[str, Any] | None = None
    editor_payload: dict[str, Any] | None = None
    reviewer_payload: dict[str, Any] | None = None
    selected_topic_id = topic_id

    if decision_path:
        try:
            selected_topic_id, scout_payload = write_decision_replay_scout(
                decision_path=decision_path,
                output_dir=output_dir,
                scout_basename=scout_basename,
                topic_id=topic_id,
            )
        except ValueError as exc:
            try:
                selected_topic_id = selected_topic_id or str(load_json(decision_path).get("topic_id") or "")
            except Exception:
                pass
            errors.append(f"Decision handoff blocked: {exc}")
    else:
        scout_code, scout_payload = llm_scout.run_llm_scout(
            signal_paths=signal_paths,
            output_dir=output_dir,
            basename=scout_basename,
            provider=provider,
            fixture_path=scout_fixture_path,
            limit=limit,
            min_impressions=min_impressions,
        )
        if scout_code:
            errors.append("LLM Scout stage failed; Editor and Reviewer were not run.")
        else:
            try:
                selected_topic_id = selected_topic_id or first_ready_topic(scout_payload)
            except ValueError as exc:
                errors.append(str(exc))
            if selected_topic_id and selected_topic_id not in selected_topic_ids(scout_payload):
                errors.append(
                    f"Requested topic `{selected_topic_id}` was not selected by LLM Scout; "
                    "Editor and Reviewer were not run."
                )
            elif selected_topic_id and selected_topic_id not in ready_topic_ids(scout_payload):
                errors.append(
                    f"Requested topic `{selected_topic_id}` is not ready_for_chain; "
                    "monitor-only or low-priority opportunities cannot run Editor and Reviewer."
                )

    if not errors and selected_topic_id:
        editor_stage_basename = editor_basename or f"llm-worker-chain-editor-{selected_topic_id}"
        try:
            editor_code, editor_payload = llm_editor.run_llm_editor(
                scout_result_path=resolve_path(str(scout_payload["result_path"])),
                scout_request_path=resolve_path(str(scout_payload["request_path"])),
                topic_id=selected_topic_id,
                output_dir=output_dir,
                basename=editor_stage_basename,
                provider=provider,
                fixture_path=editor_fixture_path,
            )
        except ValueError as exc:
            editor_code = 1
            editor_payload = None
            errors.append(f"LLM Editor stage blocked: {exc}")
        if editor_code and not any(error.startswith("LLM Editor stage blocked:") for error in errors):
            errors.append("LLM Editor stage failed; Reviewer was not run.")

    if not errors and editor_payload:
        reviewer_stage_basename = reviewer_basename or f"llm-worker-chain-reviewer-{selected_topic_id}"
        try:
            reviewer_code, reviewer_payload = llm_reviewer.run_llm_reviewer(
                editor_result_path=resolve_path(str(editor_payload["result_path"])),
                editor_request_path=resolve_path(str(editor_payload["request_path"])),
                output_dir=output_dir,
                basename=reviewer_stage_basename,
                provider=provider,
                fixture_path=reviewer_fixture_path,
            )
        except ValueError as exc:
            reviewer_code = 1
            reviewer_payload = None
            errors.append(f"LLM Reviewer stage blocked: {exc}")
        if reviewer_code and not any(error.startswith("LLM Reviewer stage blocked:") for error in errors):
            errors.append("LLM Reviewer stage failed.")

    summary = build_summary(
        provider=provider,
        topic_id=selected_topic_id,
        decision_path=decision_path,
        scout_payload=scout_payload,
        editor_payload=editor_payload,
        reviewer_payload=reviewer_payload,
        generated_at=generated_at,
        errors=errors,
    )
    json_path, markdown_path = write_summary(summary, output_dir, basename)
    summary["artifacts"]["chain_json"] = rel(json_path)
    summary["artifacts"]["chain_markdown"] = rel(markdown_path)
    return (0 if summary["state"] == "completed" else 1), summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the no-write LLM Scout -> Editor -> Reviewer chain.")
    parser.add_argument(
        "--signals",
        action="append",
        help="Path to a GSC/Bing agent signals JSON file. Can be supplied more than once. Defaults to latest GSC and Bing when present.",
    )
    parser.add_argument(
        "--from-decision",
        help="Path to an approved_for_chain llm-topic-decision-<topic_id>.json artifact. Replays the saved decision instead of rerunning Scout.",
    )
    parser.add_argument("--topic-id", help="Selected LLM Scout topic_id. Defaults to the first selected opportunity.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for LLM worker chain artifacts.")
    parser.add_argument("--basename", help="Chain summary basename. Defaults to llm-worker-chain-<topic_id>.")
    parser.add_argument("--scout-basename", default="llm-worker-chain-scout", help="LLM Scout output basename.")
    parser.add_argument("--editor-basename", help="LLM Editor output basename. Defaults to llm-editor-brief-<topic_id>.")
    parser.add_argument("--reviewer-basename", help="LLM Reviewer output basename. Defaults to llm-reviewer-gate-<topic_id>.")
    parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider passed to llm_adapter for each LLM stage. Defaults to disabled/fail-closed.",
    )
    parser.add_argument("--scout-fixture", help="Fixture response JSON for the Scout stage.")
    parser.add_argument("--editor-fixture", help="Fixture response JSON for the Editor stage.")
    parser.add_argument("--reviewer-fixture", help="Fixture response JSON for the Reviewer stage.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum deterministic Scout proposals to review.")
    parser.add_argument("--min-impressions", type=int, default=200, help="Minimum page impressions for Scout proposals.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    signal_paths = [resolve_path(value) for value in args.signals] if args.signals else llm_scout.default_signal_paths()
    decision_path = resolve_path(args.from_decision) if args.from_decision else None
    if not signal_paths and not decision_path:
        print("No Scout signal files were found.", file=sys.stderr)
        return 1
    output_dir = resolve_path(args.output_dir)
    code, summary = run_llm_worker_chain(
        signal_paths=signal_paths,
        output_dir=output_dir,
        provider=args.provider,
        topic_id=args.topic_id,
        basename=args.basename,
        scout_basename=args.scout_basename,
        editor_basename=args.editor_basename,
        reviewer_basename=args.reviewer_basename,
        scout_fixture_path=resolve_path(args.scout_fixture) if args.scout_fixture else None,
        editor_fixture_path=resolve_path(args.editor_fixture) if args.editor_fixture else None,
        reviewer_fixture_path=resolve_path(args.reviewer_fixture) if args.reviewer_fixture else None,
        limit=args.limit,
        min_impressions=args.min_impressions,
        decision_path=decision_path,
    )
    output = {
        "state": summary["state"],
        "provider": summary["provider"],
        "handoff_source": summary["handoff_source"],
        "source_decision": summary["source_decision"],
        "source_topic_id": summary["source_topic_id"],
        "target_page_or_slug": summary["target_page_or_slug"],
        "review_verdict": summary["review_verdict"],
        "risk_level": summary["risk_level"],
        "approved_next_stage": summary["approved_next_stage"],
        "owner_approval_required": summary["owner_approval_required"],
        "artifacts": summary.get("artifacts", {}),
        "errors": summary.get("errors", []),
    }
    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"State: {output['state']}")
        print(f"Topic: {output['source_topic_id']}")
        print(f"Target: {output['target_page_or_slug']}")
        print(f"Verdict: {output['review_verdict']}")
        print(f"Chain summary: {output['artifacts'].get('chain_markdown')}")
        if output["errors"]:
            print("Errors:")
            for error in output["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
