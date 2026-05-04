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
) -> tuple[int, dict[str, Any]]:
    generated_at = now_utc()
    errors: list[str] = []
    scout_payload: dict[str, Any] | None = None
    editor_payload: dict[str, Any] | None = None
    reviewer_payload: dict[str, Any] | None = None
    selected_topic_id = topic_id

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
            selected_topic_id = selected_topic_id or first_selected_topic(scout_payload)
        except ValueError as exc:
            errors.append(str(exc))

    if not errors and selected_topic_id:
        editor_stage_basename = editor_basename or f"llm-worker-chain-editor-{selected_topic_id}"
        editor_code, editor_payload = llm_editor.run_llm_editor(
            scout_result_path=resolve_path(str(scout_payload["result_path"])),
            scout_request_path=resolve_path(str(scout_payload["request_path"])),
            topic_id=selected_topic_id,
            output_dir=output_dir,
            basename=editor_stage_basename,
            provider=provider,
            fixture_path=editor_fixture_path,
        )
        if editor_code:
            errors.append("LLM Editor stage failed; Reviewer was not run.")

    if not errors and editor_payload:
        reviewer_stage_basename = reviewer_basename or f"llm-worker-chain-reviewer-{selected_topic_id}"
        reviewer_code, reviewer_payload = llm_reviewer.run_llm_reviewer(
            editor_result_path=resolve_path(str(editor_payload["result_path"])),
            editor_request_path=resolve_path(str(editor_payload["request_path"])),
            output_dir=output_dir,
            basename=reviewer_stage_basename,
            provider=provider,
            fixture_path=reviewer_fixture_path,
        )
        if reviewer_code:
            errors.append("LLM Reviewer stage failed.")

    summary = build_summary(
        provider=provider,
        topic_id=selected_topic_id,
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
    if not signal_paths:
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
    )
    output = {
        "state": summary["state"],
        "provider": summary["provider"],
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
