#!/usr/bin/env python3
"""No-write LLM Reviewer gate for one LLM Editor planning brief."""

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
from automation.workers import llm_adapter


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_TOPIC_ID = "codes-gsc-opportunity"
HIGH_RISK_PAGE_ROLES = {"cornerstone-guide", "home-hub"}


REVIEWER_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "target_page_or_slug": {"type": "string", "maxLength": 160},
        "page_role": {"type": "string", "maxLength": 80},
        "verdict": {
            "type": "string",
            "enum": ["pass", "needs_human_review", "revise", "reject"],
        },
        "risk_level": {"type": "string", "enum": ["high", "medium", "low"]},
        "approved_next_stage": {
            "type": "string",
            "enum": ["none", "brief", "patch_plan", "proposal", "approval", "apply_preview"],
        },
        "blocking_issues": {
            "type": "array",
            "maxItems": 8,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "severity": {"type": "string", "enum": ["high", "medium", "low"]},
                    "issue": {"type": "string", "maxLength": 450},
                    "required_fix": {"type": "string", "maxLength": 450},
                },
                "required": ["severity", "issue", "required_fix"],
            },
        },
        "warnings": {
            "type": "array",
            "maxItems": 10,
            "items": {"type": "string", "maxLength": 400},
        },
        "duplicate_intent_review": {"type": "string", "maxLength": 700},
        "cluster_role_review": {"type": "string", "maxLength": 700},
        "canonical_claim_review": {"type": "string", "maxLength": 700},
        "template_safety_review": {"type": "string", "maxLength": 700},
        "owner_approval_required": {"type": "boolean"},
        "owner_questions": {
            "type": "array",
            "maxItems": 8,
            "items": {"type": "string", "maxLength": 350},
        },
        "required_context_before_edit": {
            "type": "array",
            "maxItems": 20,
            "items": {"type": "string", "maxLength": 220},
        },
        "required_checks": {
            "type": "array",
            "maxItems": 10,
            "items": {"type": "string", "maxLength": 220},
        },
        "next_step": {"type": "string", "maxLength": 450},
    },
    "required": [
        "target_page_or_slug",
        "page_role",
        "verdict",
        "risk_level",
        "approved_next_stage",
        "blocking_issues",
        "warnings",
        "duplicate_intent_review",
        "cluster_role_review",
        "canonical_claim_review",
        "template_safety_review",
        "owner_approval_required",
        "owner_questions",
        "required_context_before_edit",
        "required_checks",
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


def default_editor_result_path(topic_id: str) -> Path:
    return REPORTS_DIR / f"llm-editor-brief-{topic_id}-result.json"


def default_editor_request_path(topic_id: str) -> Path:
    return REPORTS_DIR / f"llm-editor-brief-{topic_id}-request.json"


def response_json(payload: dict[str, Any], label: str) -> dict[str, Any]:
    response = payload.get("response_json")
    if not isinstance(response, dict):
        raise ValueError(f"{label} does not contain a response_json object.")
    return response


def source_topic_id(editor_result_path: Path, editor_request: dict[str, Any]) -> str:
    selected = editor_request.get("inputs", {}).get("selected_opportunity", {})
    if selected.get("topic_id"):
        return str(selected["topic_id"])
    name = editor_result_path.name
    prefix = "llm-editor-brief-"
    suffix = "-result.json"
    if name.startswith(prefix) and name.endswith(suffix):
        return name[len(prefix) : -len(suffix)]
    return DEFAULT_TOPIC_ID


def build_request(
    editor_result_path: Path,
    editor_request_path: Path,
    request_id: str,
) -> dict[str, Any]:
    editor_result = load_json(editor_result_path)
    editor_request = load_json(editor_request_path)
    editor_response = response_json(editor_result, "LLM Editor result")
    deterministic_brief = editor_request.get("inputs", {}).get("deterministic_editor_brief", {})
    selected = editor_request.get("inputs", {}).get("selected_opportunity", {})
    proposal = editor_request.get("inputs", {}).get("deterministic_proposal", {})

    return {
        "schema_version": 1,
        "request_id": request_id,
        "worker_role": "reviewer",
        "task": "Review one no-write LLM Editor planning brief for site fit, risk, and readiness.",
        "prompt": (
            "Act as the LLM Reviewer gate for lastzguides.com. Review the planning brief only. "
            "Do not write or rewrite public page copy. Do not create patch specs. "
            "Check duplicate intent, cluster role separation, canonical claim protection, template safety, owner questions, "
            "and deterministic QA readiness. Treat analytics as signals, not proof. Return JSON only."
        ),
        "inputs": {
            "source_llm_editor_result": rel(editor_result_path),
            "source_llm_editor_request": rel(editor_request_path),
            "selected_opportunity": selected,
            "deterministic_proposal": proposal,
            "deterministic_editor_context": deterministic_brief,
            "llm_editor_brief": editor_response,
            "guardrails": [
                "No content files may be edited by Reviewer.",
                "No final public page copy may be generated.",
                "No patch specs, backlog entries, manifests, PRs, or production changes may be created.",
                "High-risk cornerstone/home pages cannot be advanced without explicit owner review.",
                "Owner approval is required before any user-visible content change.",
            ],
        },
        "expected_response_keys": [
            "target_page_or_slug",
            "page_role",
            "verdict",
            "risk_level",
            "approved_next_stage",
            "blocking_issues",
            "warnings",
            "duplicate_intent_review",
            "cluster_role_review",
            "canonical_claim_review",
            "template_safety_review",
            "owner_approval_required",
            "owner_questions",
            "required_context_before_edit",
            "required_checks",
            "next_step",
        ],
        "response_schema": REVIEWER_RESPONSE_SCHEMA,
        "max_output_tokens": 4000,
    }


def validate_reviewer_response(result: dict[str, Any], request: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    response = result.get("response_json")
    if result.get("state") != "completed" or not isinstance(response, dict):
        return errors

    editor_brief = request.get("inputs", {}).get("llm_editor_brief", {})
    target = editor_brief.get("target_page_or_slug", "")
    page_role = editor_brief.get("page_role", "")
    if response.get("target_page_or_slug") != target:
        errors.append(f"LLM Reviewer target `{response.get('target_page_or_slug')}` does not match LLM Editor target `{target}`.")
    if response.get("page_role") != page_role:
        errors.append(f"LLM Reviewer page_role `{response.get('page_role')}` does not match LLM Editor page_role `{page_role}`.")
    if not response.get("owner_approval_required"):
        errors.append("LLM Reviewer must require owner approval before user-visible content changes.")
    if page_role in HIGH_RISK_PAGE_ROLES and response.get("verdict") == "pass":
        errors.append("LLM Reviewer cannot return `pass` for a high-risk cornerstone/home page; use `needs_human_review` or stricter.")
    if page_role in HIGH_RISK_PAGE_ROLES and response.get("approved_next_stage") not in {"none", "brief", "patch_plan", "proposal", "approval"}:
        errors.append("LLM Reviewer approved an unsafe next stage for a high-risk page.")
    for required in ["python3 scripts/prepublish_check.py", "python3 automation/pipeline.py checks --strict"]:
        if required not in response.get("required_checks", []):
            errors.append(f"LLM Reviewer omitted required check `{required}`.")
    return errors


def render_markdown(payload: dict[str, Any]) -> str:
    result = payload["adapter_result"]
    response = result.get("response_json") or {}
    issue_lines = [
        f"{item.get('severity', '')}: {item.get('issue', '')} Required fix: {item.get('required_fix', '')}"
        for item in response.get("blocking_issues", [])
    ]
    lines = [
        f"# LLM Reviewer Gate - {payload['source_topic_id']}",
        "",
        "## Overview",
        "",
        f"- State: `{result.get('state')}`",
        f"- Provider: `{result.get('provider')}`",
        f"- Target: `{payload['target_page_or_slug']}`",
        f"- Request: `{payload['request_path']}`",
        f"- Result: `{payload['result_path']}`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "- Scope: review gate only; no final public page copy or patch specs were generated.",
        "",
    ]
    if result.get("errors"):
        lines.extend(["## Errors", "", md_list(result["errors"]), ""])
    if response:
        lines.extend(
            [
                "## Verdict",
                "",
                f"- Verdict: `{response.get('verdict', '')}`",
                f"- Risk: `{response.get('risk_level', '')}`",
                f"- Approved next stage: `{response.get('approved_next_stage', '')}`",
                f"- Owner approval required: `{str(response.get('owner_approval_required')).lower()}`",
                "",
                "## Blocking Issues",
                "",
                md_list(issue_lines),
                "",
                "## Warnings",
                "",
                md_list(response.get("warnings", [])),
                "",
                "## Duplicate Intent Review",
                "",
                response.get("duplicate_intent_review", ""),
                "",
                "## Cluster Role Review",
                "",
                response.get("cluster_role_review", ""),
                "",
                "## Canonical Claim Review",
                "",
                response.get("canonical_claim_review", ""),
                "",
                "## Template Safety Review",
                "",
                response.get("template_safety_review", ""),
                "",
                "## Owner Questions",
                "",
                md_list(response.get("owner_questions", [])),
                "",
                "## Required Context Before Edit",
                "",
                md_list([f"`{path}`" for path in response.get("required_context_before_edit", [])]),
                "",
                "## Required Checks",
                "",
                md_list([f"`{check}`" for check in response.get("required_checks", [])]),
                "",
                "## Next Step",
                "",
                response.get("next_step", ""),
                "",
            ]
        )
    return "\n".join(lines)


def run_llm_reviewer(
    editor_result_path: Path,
    editor_request_path: Path,
    output_dir: Path,
    basename: str | None,
    provider: str,
    fixture_path: Path | None,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    editor_result = load_json(editor_result_path)
    editor_request = load_json(editor_request_path)
    editor_response = response_json(editor_result, "LLM Editor result")
    topic_id = source_topic_id(editor_result_path, editor_request)
    name = basename or f"llm-reviewer-gate-{topic_id}"
    request_path = output_dir / f"{name}-request.json"
    result_path = output_dir / f"{name}-result.json"
    markdown_path = output_dir / f"{name}.md"

    request = build_request(editor_result_path, editor_request_path, request_id=name)
    write_json(request_path, request)
    code, result = llm_adapter.run_adapter(request_path, provider, fixture_path)
    validation_errors = validate_reviewer_response(result, request)
    if validation_errors:
        result = llm_adapter.blocked_result(request, provider, validation_errors, request_path)
        code = 1
    write_json(result_path, result)

    payload = {
        "schema_version": 1,
        "report_type": "llm_reviewer_gate",
        "generated_at": now_utc(),
        "source_topic_id": topic_id,
        "target_page_or_slug": editor_response.get("target_page_or_slug", ""),
        "source_llm_editor_result": rel(editor_result_path),
        "source_llm_editor_request": rel(editor_request_path),
        "request_path": rel(request_path),
        "result_path": rel(result_path),
        "markdown_path": rel(markdown_path),
        "adapter_result": result,
        "safety": "No content, backlog, manifest, PR, or production files were modified by LLM Reviewer.",
    }
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return code, payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a no-write LLM Reviewer gate from one LLM Editor brief.")
    parser.add_argument("--topic-id", default=DEFAULT_TOPIC_ID, help="Topic id used to infer default LLM Editor artifacts.")
    parser.add_argument("--editor-result", help="Path to llm-editor-brief-<topic_id>-result.json.")
    parser.add_argument("--editor-request", help="Path to llm-editor-brief-<topic_id>-request.json.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for LLM Reviewer artifacts.")
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

    editor_result_path = resolve_path(args.editor_result) if args.editor_result else default_editor_result_path(args.topic_id)
    editor_request_path = resolve_path(args.editor_request) if args.editor_request else default_editor_request_path(args.topic_id)
    output_dir = resolve_path(args.output_dir)
    fixture_path = resolve_path(args.fixture) if args.fixture else None
    code, payload = run_llm_reviewer(
        editor_result_path=editor_result_path,
        editor_request_path=editor_request_path,
        output_dir=output_dir,
        basename=args.basename,
        provider=args.provider,
        fixture_path=fixture_path,
    )
    response = payload["adapter_result"].get("response_json") or {}
    summary = {
        "state": payload["adapter_result"].get("state"),
        "provider": payload["adapter_result"].get("provider"),
        "source_topic_id": payload["source_topic_id"],
        "target_page_or_slug": payload["target_page_or_slug"],
        "verdict": response.get("verdict"),
        "risk_level": response.get("risk_level"),
        "approved_next_stage": response.get("approved_next_stage"),
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
        print(f"Verdict: {summary['verdict']}")
        print(f"Risk: {summary['risk_level']}")
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
