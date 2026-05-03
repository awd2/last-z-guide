#!/usr/bin/env python3
"""No-write LLM Editor brief worker for one selected Scout opportunity."""

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
from automation.workers import editor, llm_adapter


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_LLM_SCOUT_RESULT = REPORTS_DIR / "llm-scout-review-result.json"
DEFAULT_LLM_SCOUT_REQUEST = REPORTS_DIR / "llm-scout-review-request.json"


EDITOR_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "brief_summary": {
            "type": "string",
            "maxLength": 700,
            "description": "Short no-write summary of the recommended content planning direction.",
        },
        "target_page_or_slug": {"type": "string", "maxLength": 160},
        "page_role": {"type": "string", "maxLength": 80},
        "primary_user_job": {"type": "string", "maxLength": 500},
        "first_screen_plan": {
            "type": "string",
            "maxLength": 700,
            "description": "Planning guidance for the first screen. Do not write final public copy.",
        },
        "section_plan": {
            "type": "array",
            "maxItems": 8,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "section": {"type": "string", "maxLength": 120},
                    "action": {"type": "string", "maxLength": 350},
                    "reason": {"type": "string", "maxLength": 350},
                },
                "required": ["section", "action", "reason"],
            },
        },
        "internal_link_plan": {
            "type": "array",
            "maxItems": 8,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "page": {"type": "string", "maxLength": 160},
                    "role": {"type": "string", "enum": ["upstream", "downstream", "lateral"]},
                    "reason": {"type": "string", "maxLength": 300},
                },
                "required": ["page", "role", "reason"],
            },
        },
        "protected_claims": {
            "type": "array",
            "maxItems": 12,
            "items": {"type": "string", "maxLength": 160},
        },
        "do_not_change": {
            "type": "array",
            "maxItems": 10,
            "items": {"type": "string", "maxLength": 350},
        },
        "owner_questions": {
            "type": "array",
            "maxItems": 8,
            "items": {"type": "string", "maxLength": 350},
        },
        "required_context_before_patch": {
            "type": "array",
            "maxItems": 20,
            "items": {"type": "string", "maxLength": 220},
        },
        "acceptance_checks": {
            "type": "array",
            "maxItems": 10,
            "items": {"type": "string", "maxLength": 220},
        },
        "next_step": {"type": "string", "maxLength": 350},
    },
    "required": [
        "brief_summary",
        "target_page_or_slug",
        "page_role",
        "primary_user_job",
        "first_screen_plan",
        "section_plan",
        "internal_link_plan",
        "protected_claims",
        "do_not_change",
        "owner_questions",
        "required_context_before_patch",
        "acceptance_checks",
        "next_step",
    ],
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def selected_opportunity(scout_result: dict[str, Any], topic_id: str | None) -> dict[str, Any]:
    response = scout_result.get("response_json")
    if not isinstance(response, dict):
        raise ValueError("LLM Scout result does not contain response_json.")
    selected = response.get("selected_opportunities", [])
    if not selected:
        raise ValueError("LLM Scout result has no selected opportunities.")
    if topic_id:
        for item in selected:
            if item.get("topic_id") == topic_id:
                return item
        raise ValueError(f"Selected LLM Scout opportunity not found: {topic_id}")
    return selected[0]


def deterministic_proposal(scout_request: dict[str, Any], topic_id: str) -> dict[str, Any]:
    proposals = scout_request.get("inputs", {}).get("proposals", [])
    for proposal in proposals:
        if proposal.get("topic_id") == topic_id:
            return proposal
    raise ValueError(f"Deterministic Scout proposal not found in request: {topic_id}")


def compact_page_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": snapshot.get("title", ""),
        "h1": snapshot.get("h1", ""),
        "meta_description": snapshot.get("meta_description", ""),
        "quick_answer": snapshot.get("quick_answer", ""),
        "data_lede": snapshot.get("data_lede", ""),
        "h2_headings": snapshot.get("h2_headings", [])[:8],
        "internal_links": snapshot.get("internal_links", [])[:20],
    }


def build_request(
    selected: dict[str, Any],
    proposal: dict[str, Any],
    deterministic_brief: dict[str, Any],
    request_id: str,
    scout_result_path: Path,
    scout_request_path: Path,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "request_id": request_id,
        "worker_role": "editor",
        "task": "Create a no-write Editor planning brief for one approved Scout opportunity.",
        "prompt": (
            "Act as the LLM Editor planner for lastzguides.com. Return a planning brief only. "
            "Do not write final public page copy, HTML, patch specs, or publishable text. "
            "Preserve the existing page template, cluster role, canonical claims, internal routing, SEO/LLM eligibility, "
            "and owner approval gate. Treat analytics as signals, not proof. Return JSON only."
        ),
        "inputs": {
            "source_llm_scout_result": rel(scout_result_path),
            "source_llm_scout_request": rel(scout_request_path),
            "selected_opportunity": selected,
            "deterministic_proposal": proposal,
            "deterministic_editor_brief": {
                "target_page_or_slug": deterministic_brief.get("target_page_or_slug", ""),
                "page_role": deterministic_brief.get("page_role", ""),
                "primary_query_family": deterministic_brief.get("primary_query_family", ""),
                "primary_user_job": deterministic_brief.get("primary_user_job", ""),
                "first_screen_answer": deterministic_brief.get("first_screen_answer", ""),
                "template_reference": deterministic_brief.get("template_reference", ""),
                "required_sections": deterministic_brief.get("required_sections", []),
                "internal_links": deterministic_brief.get("internal_links", {}),
                "protected_claims": deterministic_brief.get("protected_claims", []),
                "do_not_change": deterministic_brief.get("do_not_change", []),
                "required_context_before_patch": deterministic_brief.get("required_context_before_patch", []),
                "acceptance_checks": deterministic_brief.get("acceptance_checks", []),
                "current_page_snapshot": compact_page_snapshot(deterministic_brief.get("current_page_snapshot", {})),
            },
            "guardrails": [
                "No content files may be edited by this worker.",
                "Do not generate final user-visible page copy.",
                "Do not create a patch plan or Patch Spec.",
                "Do not mutate backlog, manifests, PRs, or production state.",
                "Owner approval is required before any user-visible content change.",
            ],
        },
        "expected_response_keys": [
            "brief_summary",
            "target_page_or_slug",
            "page_role",
            "primary_user_job",
            "first_screen_plan",
            "section_plan",
            "internal_link_plan",
            "protected_claims",
            "do_not_change",
            "owner_questions",
            "required_context_before_patch",
            "acceptance_checks",
            "next_step",
        ],
        "response_schema": EDITOR_RESPONSE_SCHEMA,
        "max_output_tokens": 4000,
    }


def validate_editor_response(result: dict[str, Any], topic_id: str, deterministic_brief: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    response = result.get("response_json")
    if result.get("state") != "completed" or not isinstance(response, dict):
        return errors
    target = deterministic_brief.get("target_page_or_slug", "")
    role = deterministic_brief.get("page_role", "")
    if response.get("target_page_or_slug") != target:
        errors.append(f"LLM Editor target `{response.get('target_page_or_slug')}` does not match deterministic target `{target}` for `{topic_id}`.")
    if response.get("page_role") != role:
        errors.append(f"LLM Editor page_role `{response.get('page_role')}` does not match deterministic page_role `{role}` for `{topic_id}`.")
    for path in deterministic_brief.get("required_context_before_patch", [])[:5]:
        if path not in response.get("required_context_before_patch", []):
            errors.append(f"LLM Editor omitted required context `{path}`.")
    return errors


def render_markdown(payload: dict[str, Any]) -> str:
    result = payload["adapter_result"]
    response = result.get("response_json") or {}
    lines = [
        f"# LLM Editor Brief - {payload['source_topic_id']}",
        "",
        "## Overview",
        "",
        f"- State: `{result.get('state')}`",
        f"- Provider: `{result.get('provider')}`",
        f"- Target: `{payload['target_page_or_slug']}`",
        f"- Request: `{payload['request_path']}`",
        f"- Result: `{payload['result_path']}`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "- Scope: planning brief only; no final public page copy was generated.",
        "",
    ]
    if result.get("errors"):
        lines.extend(["## Errors", "", md_list(result["errors"]), ""])
    if response:
        lines.extend(
            [
                "## Brief Summary",
                "",
                response.get("brief_summary", ""),
                "",
                "## First-Screen Plan",
                "",
                response.get("first_screen_plan", ""),
                "",
                "## Section Plan",
                "",
                md_list([
                    f"{item.get('section', '')}: {item.get('action', '')} Reason: {item.get('reason', '')}"
                    for item in response.get("section_plan", [])
                ]),
                "",
                "## Internal Link Plan",
                "",
                md_list([
                    f"{item.get('role', '')} `{item.get('page', '')}`: {item.get('reason', '')}"
                    for item in response.get("internal_link_plan", [])
                ]),
                "",
                "## Protected Claims",
                "",
                md_list([f"`{claim}`" for claim in response.get("protected_claims", [])]),
                "",
                "## Do Not Change",
                "",
                md_list(response.get("do_not_change", [])),
                "",
                "## Owner Questions",
                "",
                md_list(response.get("owner_questions", [])),
                "",
                "## Required Context Before Patch",
                "",
                md_list([f"`{path}`" for path in response.get("required_context_before_patch", [])]),
                "",
                "## Acceptance Checks",
                "",
                md_list([f"`{check}`" for check in response.get("acceptance_checks", [])]),
                "",
                "## Next Step",
                "",
                response.get("next_step", ""),
                "",
            ]
        )
    return "\n".join(lines)


def run_llm_editor(
    scout_result_path: Path,
    scout_request_path: Path,
    topic_id: str | None,
    output_dir: Path,
    basename: str | None,
    provider: str,
    fixture_path: Path | None,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    scout_result = load_json(scout_result_path)
    scout_request = load_json(scout_request_path)
    selected = selected_opportunity(scout_result, topic_id)
    source_topic_id = str(selected.get("topic_id", ""))
    proposal = deterministic_proposal(scout_request, source_topic_id)
    deterministic_brief = editor.build_editor_brief(proposal, scout_request_path)
    name = basename or f"llm-editor-brief-{source_topic_id}"
    request_path = output_dir / f"{name}-request.json"
    result_path = output_dir / f"{name}-result.json"
    markdown_path = output_dir / f"{name}.md"

    request = build_request(
        selected=selected,
        proposal=proposal,
        deterministic_brief=deterministic_brief,
        request_id=name,
        scout_result_path=scout_result_path,
        scout_request_path=scout_request_path,
    )
    write_json(request_path, request)
    code, result = llm_adapter.run_adapter(request_path, provider, fixture_path)
    validation_errors = validate_editor_response(result, source_topic_id, deterministic_brief)
    if validation_errors:
        result = llm_adapter.blocked_result(request, provider, validation_errors, request_path)
        code = 1
    write_json(result_path, result)

    payload = {
        "schema_version": 1,
        "report_type": "llm_editor_brief",
        "generated_at": now_utc(),
        "source_topic_id": source_topic_id,
        "target_page_or_slug": deterministic_brief.get("target_page_or_slug", ""),
        "source_llm_scout_result": rel(scout_result_path),
        "source_llm_scout_request": rel(scout_request_path),
        "request_path": rel(request_path),
        "result_path": rel(result_path),
        "markdown_path": rel(markdown_path),
        "adapter_result": result,
        "safety": "No content, backlog, manifest, PR, or production files were modified by LLM Editor.",
    }
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return code, payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a no-write LLM Editor brief from one selected LLM Scout opportunity.")
    parser.add_argument("--scout-result", default=str(DEFAULT_LLM_SCOUT_RESULT), help="Path to llm-scout-review-result.json.")
    parser.add_argument("--scout-request", default=str(DEFAULT_LLM_SCOUT_REQUEST), help="Path to llm-scout-review-request.json.")
    parser.add_argument("--topic-id", help="Selected LLM Scout topic_id. Defaults to the first selected opportunity.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for LLM Editor artifacts.")
    parser.add_argument("--basename", help="Output basename without extension.")
    parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider passed to llm_adapter. Defaults to disabled/fail-closed.",
    )
    parser.add_argument("--fixture", help="Fixture response JSON for offline provider tests.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    scout_result_path = resolve_path(args.scout_result)
    scout_request_path = resolve_path(args.scout_request)
    output_dir = resolve_path(args.output_dir)
    fixture_path = resolve_path(args.fixture) if args.fixture else None
    code, payload = run_llm_editor(
        scout_result_path=scout_result_path,
        scout_request_path=scout_request_path,
        topic_id=args.topic_id,
        output_dir=output_dir,
        basename=args.basename,
        provider=args.provider,
        fixture_path=fixture_path,
    )
    summary = {
        "state": payload["adapter_result"].get("state"),
        "provider": payload["adapter_result"].get("provider"),
        "source_topic_id": payload["source_topic_id"],
        "target_page_or_slug": payload["target_page_or_slug"],
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
        print(f"Topic: {summary['source_topic_id']}")
        print(f"Target: {summary['target_page_or_slug']}")
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
