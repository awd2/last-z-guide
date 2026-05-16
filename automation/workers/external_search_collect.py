#!/usr/bin/env python3
"""No-write external search collector for approved source query tasks."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_json, write_json
from automation.proposal_renderer import md_list
from automation.workers.llm_adapter import (
    OPENAI_RESPONSES_ENDPOINT,
    post_openai_response,
    safe_schema_name,
)


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_EVIDENCE_REFRESH = REPORTS_DIR / "external-evidence-refresh.json"
DEFAULT_MODEL = "gpt-5.4-mini"
READY_ACTIONS = {"update_existing", "create_new", "consolidate", "monitor", "reject"}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "item"


def ascii_clean(value: str) -> str:
    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value.encode("ascii", errors="ignore").decode("ascii")


def normalize_ascii(value: Any) -> Any:
    if isinstance(value, str):
        return ascii_clean(value)
    if isinstance(value, list):
        return [normalize_ascii(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_ascii(item) for key, item in value.items()}
    return value


def domain_from_url(value: str) -> str:
    parsed = urlparse(value)
    return parsed.netloc.lower().strip()


def load_evidence_refresh(path: Path) -> tuple[list[str], dict[str, Any]]:
    if not path.exists():
        return [f"External Evidence Refresh artifact not found: {rel(path)}"], {}
    payload = load_json(path)
    if payload.get("report_type") != "external_evidence_refresh":
        return [f"Unsupported evidence refresh report type in {rel(path)}: {payload.get('report_type')}"], payload
    if payload.get("state") not in {"evidence_queue_ready", "no_external_evidence_tasks"}:
        return [f"External Evidence Refresh artifact is not ready: {payload.get('state')}"], payload
    return [], payload


def search_response_schema(per_query_results: int) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "query_task_id": {"type": "string"},
            "searched_query": {"type": "string"},
            "source_id": {"type": "string"},
            "source_domain": {"type": "string"},
            "results": {
                "type": "array",
                "maxItems": per_query_results,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "url": {"type": "string"},
                        "title": {"type": "string"},
                        "evidence_summary": {"type": "string"},
                        "topic_fit": {"type": "string", "enum": ["high", "medium", "low"]},
                        "suggested_cluster": {"type": "string"},
                        "recommended_action": {
                            "type": "string",
                            "enum": ["update_existing", "create_new", "consolidate", "monitor", "reject"],
                        },
                        "target_page_or_slug": {"type": "string"},
                        "primary_user_job": {"type": "string"},
                        "claims_to_verify": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
                        "public_claim_ready": {"type": "boolean"},
                    },
                    "required": [
                        "url",
                        "title",
                        "evidence_summary",
                        "topic_fit",
                        "suggested_cluster",
                        "recommended_action",
                        "target_page_or_slug",
                        "primary_user_job",
                        "claims_to_verify",
                        "public_claim_ready",
                    ],
                },
            },
            "search_notes": {"type": "string"},
            "no_results_reason": {"type": "string"},
        },
        "required": [
            "query_task_id",
            "searched_query",
            "source_id",
            "source_domain",
            "results",
            "search_notes",
            "no_results_reason",
        ],
    }


def openai_search_body(task: dict[str, Any], per_query_results: int) -> dict[str, Any]:
    model = os.getenv("OPENAI_SEARCH_MODEL", os.getenv("OPENAI_MODEL", DEFAULT_MODEL)).strip() or DEFAULT_MODEL
    domain = domain_from_url(str(task.get("base_url", "")))
    tool: dict[str, Any] = {
        "type": "web_search",
        "search_context_size": os.getenv("OPENAI_SEARCH_CONTEXT_SIZE", "low").strip() or "low",
    }
    if domain:
        tool["filters"] = {"allowed_domains": [domain]}

    prompt = {
        "task": "Search approved Last Z external source query tasks for topic discovery and cross-validation leads.",
        "query_task": task,
        "rules": [
            "Use web search. Keep results limited to the allowed source domain when one is provided.",
            "Return discovery leads only. Do not mark public claims ready.",
            "Do not copy source wording. Summarize the player job or evidence category in your own short words.",
            "Prefer concrete Last Z guide/wiki/tool pages over generic home pages.",
            "Reject or use low topic_fit for off-topic, generic, spam, or unrelated pages.",
            "A single result is never proof for player-facing mechanics, costs, rewards, seasons, or events.",
        ],
    }
    body: dict[str, Any] = {
        "model": model,
        "tools": [tool],
        "tool_choice": "required",
        "include": ["web_search_call.action.sources"],
        "input": [
            {
                "role": "system",
                "content": (
                    "You are a constrained external-source Scout for lastzguides.com. "
                    "Return only JSON that matches the schema. Use plain ASCII English only. "
                    "Never say public claims are ready."
                ),
            },
            {"role": "user", "content": json.dumps(prompt, indent=2, sort_keys=True)},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": safe_schema_name(f"external_search_{task.get('task_id', 'task')}"),
                "strict": True,
                "schema": search_response_schema(per_query_results),
            }
        },
        "max_output_tokens": int(os.getenv("OPENAI_SEARCH_MAX_OUTPUT_TOKENS", "1600")),
    }
    reasoning_effort = os.getenv("OPENAI_SEARCH_REASONING_EFFORT", "").strip()
    if reasoning_effort:
        body["reasoning"] = {"effort": reasoning_effort}
    return body


def extract_output_text(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("output_text"), str):
        return payload["output_text"]
    chunks: list[str] = []
    for item in payload.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                chunks.append(content["text"])
    return "".join(chunks).strip()


def extract_provider_sources(payload: dict[str, Any]) -> list[dict[str, str]]:
    sources: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in payload.get("output", []):
        if item.get("type") == "web_search_call":
            action = item.get("action", {})
            for source in action.get("sources", []) if isinstance(action, dict) else []:
                url = str(source.get("url", "")).strip()
                if url and url not in seen:
                    sources.append({"url": url, "title": str(source.get("title", "")).strip()})
                    seen.add(url)
        if item.get("type") == "message":
            for content in item.get("content", []):
                for annotation in content.get("annotations", []) if isinstance(content, dict) else []:
                    if annotation.get("type") != "url_citation":
                        continue
                    url = str(annotation.get("url", "")).strip()
                    if url and url not in seen:
                        sources.append({"url": url, "title": str(annotation.get("title", "")).strip()})
                        seen.add(url)
    return sources


def fixture_search(task: dict[str, Any], per_query_results: int) -> tuple[dict[str, Any], dict[str, Any]]:
    domain = domain_from_url(str(task.get("base_url", "https://example.com"))) or "example.com"
    result = {
        "query_task_id": str(task.get("task_id", "")),
        "searched_query": str(task.get("query", "")),
        "source_id": str(task.get("source_id", "")),
        "source_domain": domain,
        "results": [
            {
                "url": f"https://{domain}/fixture-last-z-result",
                "title": "Fixture Last Z result",
                "evidence_summary": "Fixture search result for offline contract tests.",
                "topic_fit": "medium",
                "suggested_cluster": "Progression",
                "recommended_action": "update_existing",
                "target_page_or_slug": "hq.html",
                "primary_user_job": "Check whether HQ progression coverage needs a source-backed review.",
                "claims_to_verify": ["hq_upgrade_requirements"],
                "public_claim_ready": False,
            }
        ][:per_query_results],
        "search_notes": "Fixture provider did not search the web.",
        "no_results_reason": "",
    }
    provider_payload = {
        "id": "fixture",
        "model": "fixture",
        "output": [],
    }
    return result, provider_payload


def validate_search_result(task: dict[str, Any], result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    domain = domain_from_url(str(task.get("base_url", "")))
    errors.extend(non_ascii_errors(result))
    if result.get("query_task_id") != task.get("task_id"):
        errors.append(f"Search result task id mismatch for `{task.get('task_id', '')}`.")
    for item in result.get("results", []):
        url = str(item.get("url", "")).strip()
        if not url.startswith("https://"):
            errors.append(f"Search result URL must be https: `{url}`.")
        if domain and domain not in domain_from_url(url):
            errors.append(f"Search result URL `{url}` is outside allowed domain `{domain}`.")
        if item.get("public_claim_ready") is not False:
            errors.append(f"Search result `{url}` must keep public_claim_ready=false.")
        if len(str(item.get("evidence_summary", ""))) > 320:
            errors.append(f"Search result `{url}` evidence_summary is too long.")
        if item.get("recommended_action") not in READY_ACTIONS:
            errors.append(f"Search result `{url}` has unsupported recommended_action.")
    return errors


def non_ascii_errors(value: Any, path: str = "search_result") -> list[str]:
    errors: list[str] = []
    if isinstance(value, str):
        if not value.isascii():
            errors.append(f"`{path}` must use plain ASCII English only.")
        return errors
    if isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(non_ascii_errors(item, f"{path}[{index}]"))
        return errors
    if isinstance(value, dict):
        for key, item in value.items():
            errors.extend(non_ascii_errors(item, f"{path}.{key}"))
    return errors


def run_search_task(task: dict[str, Any], provider: str, per_query_results: int) -> dict[str, Any]:
    base = {
        "task_id": task.get("task_id", ""),
        "source_id": task.get("source_id", ""),
        "source_name": task.get("source_name", ""),
        "base_url": task.get("base_url", ""),
        "query": task.get("query", ""),
        "public_claim_ready": False,
        "searched_at": now_utc(),
    }
    if provider == "fixture":
        result, provider_payload = fixture_search(task, per_query_results)
    else:
        try:
            provider_payload = post_openai_response(openai_search_body(task, per_query_results))
            output_text = extract_output_text(provider_payload)
            result = json.loads(output_text)
            result = normalize_ascii(result)
        except Exception as exc:  # noqa: BLE001 - collect provider failures as artifact data.
            return {**base, "search_status": "search_failed", "error": str(exc), "results": []}

    validation_errors = validate_search_result(task, result)
    if validation_errors:
        return {
            **base,
            "search_status": "search_failed_validation",
            "error": "; ".join(validation_errors),
            "results": [],
            "raw_result": result,
        }
    return {
        **base,
        "search_status": "searched",
        "source_domain": result.get("source_domain", ""),
        "searched_query": result.get("searched_query", ""),
        "search_notes": result.get("search_notes", ""),
        "no_results_reason": result.get("no_results_reason", ""),
        "results": result.get("results", []),
        "provider_sources": extract_provider_sources(provider_payload),
        "provider_metadata": {
            "model": provider_payload.get("model", ""),
            "response_id": provider_payload.get("id", ""),
            "status": provider_payload.get("status", ""),
            "endpoint": os.getenv("OPENAI_RESPONSES_ENDPOINT", OPENAI_RESPONSES_ENDPOINT).strip()
            or OPENAI_RESPONSES_ENDPOINT,
        },
    }


def proposal_from_result(task_record: dict[str, Any], result: dict[str, Any], index: int) -> dict[str, Any]:
    source_id = str(task_record.get("source_id", "external-source"))
    title = str(result.get("title", "External search result")).strip() or "External search result"
    action = str(result.get("recommended_action", "monitor")).strip()
    if action not in READY_ACTIONS:
        action = "monitor"
    topic_fit = str(result.get("topic_fit", "low")).strip()
    priority = "medium" if topic_fit == "high" and action != "monitor" else "low" if topic_fit == "low" else "medium"
    target = safe_target_page(str(result.get("target_page_or_slug", "")).strip())
    return {
        "topic_id": f"external-search-{slugify(source_id)}-{slugify(title)[:42]}-{index}",
        "title": f"External search opportunity: {title}",
        "cluster": result.get("suggested_cluster", "Site"),
        "recommended_action": action,
        "archetype_suggestion": "support-guide" if action == "create_new" else "cornerstone-guide",
        "target_page_or_slug": target,
        "source_type": "external_search",
        "source_id": source_id,
        "source_name": task_record.get("source_name", ""),
        "source_reference": f"External search: {task_record.get('query', '')}",
        "confidence": "medium" if topic_fit in {"high", "medium"} else "low",
        "priority": priority,
        "risk_level": "high",
        "status": "candidate" if action in {"update_existing", "create_new", "consolidate"} and priority != "low" else "monitor",
        "primary_user_job": result.get("primary_user_job", ""),
        "source_urls": [result.get("url", "")],
        "evidence": [result.get("evidence_summary", "")],
        "claims_to_verify": result.get("claims_to_verify", []),
        "cross_validation_status": "search_result_needs_canonical_and_second_source_validation",
        "site_fit": {
            "expected_internal_route": [target] if target else [],
            "external_source_id": source_id,
        },
        "constraints": [
            "External search result is discovery evidence only.",
            "Do not copy source wording.",
            "Do not publish any public claim without canonical memory, second-source validation, and owner approval.",
        ],
        "reject_if": [
            "The result is off-topic or duplicates an existing page job.",
            "The claim cannot be validated against reliable sources or owner-confirmed game knowledge.",
        ],
    }


def safe_target_page(value: str) -> str:
    if not value or value.startswith("/") or value.startswith("http"):
        return ""
    if "/" in value or "\\" in value:
        return ""
    return value if value.endswith(".html") else ""


def build_candidate_proposals(search_records: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    for record in search_records:
        if record.get("search_status") != "searched":
            continue
        for result in record.get("results", []):
            url = str(result.get("url", "")).strip()
            if not url or url in seen_urls or result.get("topic_fit") == "low":
                continue
            seen_urls.add(url)
            proposals.append(proposal_from_result(record, result, len(proposals) + 1))
            if len(proposals) >= limit:
                return proposals
    return proposals


def build_external_search_collect(
    evidence_refresh_path: Path,
    output_dir: Path,
    basename: str,
    provider: str,
    limit: int,
    per_query_results: int,
    proposal_limit: int,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    if provider == "disabled":
        payload = {
            "schema_version": 1,
            "report_type": "external_search_collect",
            "generated_at": now_utc(),
            "state": "blocked",
            "provider": provider,
            "evidence_refresh_path": rel(evidence_refresh_path),
            "search_task_count": 0,
            "searched_count": 0,
            "failed_count": 0,
            "candidate_proposal_count": 0,
            "search_records": [],
            "candidate_proposals": [],
            "errors": ["No external search provider is enabled."],
            "output_path": rel(json_path),
            "markdown_path": rel(markdown_path),
            "allows_content_edit": False,
            "allows_backlog_mutation": False,
            "allows_manifest_mutation": False,
            "allows_pr_or_deploy": False,
            "safety": "No content, backlog, manifest, PR, or production files were modified by External Search Collect.",
        }
        write_json(json_path, payload)
        markdown_path.write_text(render_markdown(payload), encoding="utf-8")
        return 1, payload

    errors, refresh = load_evidence_refresh(evidence_refresh_path)
    if errors:
        payload = blocked_payload(json_path, markdown_path, provider, evidence_refresh_path, errors)
        write_json(json_path, payload)
        markdown_path.write_text(render_markdown(payload), encoding="utf-8")
        return 1, payload

    tasks = [task for task in refresh.get("source_query_tasks", []) if isinstance(task, dict)]
    tasks = tasks[: max(0, limit)]
    records = [run_search_task(task, provider=provider, per_query_results=per_query_results) for task in tasks]
    searched_count = sum(1 for item in records if item.get("search_status") == "searched")
    failed_count = sum(1 for item in records if item.get("search_status") != "searched")
    proposals = build_candidate_proposals(records, limit=proposal_limit)
    if searched_count and failed_count:
        state = "search_collection_partial"
    elif searched_count:
        state = "search_collected"
    elif tasks:
        state = "search_collection_failed"
    else:
        state = "no_search_tasks"
    payload = {
        "schema_version": 1,
        "report_type": "external_search_collect",
        "generated_at": now_utc(),
        "state": state,
        "provider": provider,
        "evidence_refresh_path": rel(evidence_refresh_path),
        "search_task_count": len(tasks),
        "searched_count": searched_count,
        "failed_count": failed_count,
        "candidate_proposal_count": len(proposals),
        "search_records": records,
        "candidate_proposals": proposals,
        "errors": [],
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": False,
        "allows_pr_or_deploy": False,
        "next_actions": [
            "Feed candidate_proposals into LLM Scout as external proposal inputs.",
            "Treat search results as discovery evidence only, not proof.",
            "Validate any public claim against canonical memory, a second reliable source, or explicit owner confirmation.",
            "Public content still requires exact proposed text, owner approval, apply-preview, apply-approved, and strict QA.",
        ],
        "safety": "No content, backlog, manifest, PR, or production files were modified by External Search Collect.",
    }
    write_json(json_path, payload)
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return 0, payload


def blocked_payload(
    json_path: Path,
    markdown_path: Path,
    provider: str,
    evidence_refresh_path: Path,
    errors: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "report_type": "external_search_collect",
        "generated_at": now_utc(),
        "state": "blocked",
        "provider": provider,
        "evidence_refresh_path": rel(evidence_refresh_path),
        "search_task_count": 0,
        "searched_count": 0,
        "failed_count": 0,
        "candidate_proposal_count": 0,
        "search_records": [],
        "candidate_proposals": [],
        "errors": errors,
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": False,
        "allows_pr_or_deploy": False,
        "safety": "No content, backlog, manifest, PR, or production files were modified by External Search Collect.",
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# External Search Collect - {payload.get('generated_at', '')}",
        "",
        "## Outcome",
        "",
        f"- State: `{payload.get('state', '')}`",
        f"- Provider: `{payload.get('provider', '')}`",
        f"- Evidence Refresh: `{payload.get('evidence_refresh_path', '')}`",
        f"- Search tasks: `{payload.get('search_task_count', 0)}`",
        f"- Searched: `{payload.get('searched_count', 0)}`",
        f"- Failed: `{payload.get('failed_count', 0)}`",
        f"- Candidate proposals: `{payload.get('candidate_proposal_count', 0)}`",
        "- Allows content edit: `false`",
        "- Allows backlog mutation: `false`",
        "- Allows manifest mutation: `false`",
        "- Allows PR/deploy: `false`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if payload.get("errors"):
        lines.extend(["## Errors", "", md_list(payload["errors"]), ""])
    if payload.get("candidate_proposals"):
        lines.extend(["## Candidate Proposals", ""])
        for proposal in payload["candidate_proposals"]:
            lines.extend(
                [
                    f"### {proposal.get('topic_id', '')}",
                    "",
                    f"- Title: {proposal.get('title', '')}",
                    f"- Action: `{proposal.get('recommended_action', '')}`",
                    f"- Target: `{proposal.get('target_page_or_slug', '')}`",
                    f"- Source: `{proposal.get('source_reference', '')}`",
                    f"- URL: `{(proposal.get('source_urls') or [''])[0]}`",
                    "- Public claim ready: `false`",
                    "",
                ]
            )
    if payload.get("search_records"):
        lines.extend(["## Search Records", ""])
        for record in payload["search_records"]:
            lines.extend(
                [
                    f"### {record.get('task_id', '')}",
                    "",
                    f"- Status: `{record.get('search_status', '')}`",
                    f"- Source: `{record.get('source_id', '')}`",
                    f"- Query: {record.get('query', '')}",
                    f"- Results: `{len(record.get('results', []))}`",
                    "",
                ]
            )
            if record.get("error"):
                lines.extend(["Error:", "", f"- {record.get('error', '')}", ""])
    lines.extend(["## Next Actions", "", md_list(payload.get("next_actions", [])), ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect no-write external search evidence from approved source query tasks.")
    parser.add_argument("--evidence-refresh", default=str(DEFAULT_EVIDENCE_REFRESH), help="Path to external-evidence-refresh.json.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for External Search Collect artifacts.")
    parser.add_argument("--basename", default="external-search-collect", help="Output basename without extension.")
    parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Search provider. `openai` uses the Responses API web_search tool. Defaults to disabled/fail-closed.",
    )
    parser.add_argument("--limit", type=int, default=6, help="Maximum query tasks to search.")
    parser.add_argument("--per-query-results", type=int, default=3, help="Maximum results per query task.")
    parser.add_argument("--proposal-limit", type=int, default=10, help="Maximum candidate proposals to emit.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, payload = build_external_search_collect(
        evidence_refresh_path=resolve_path(args.evidence_refresh),
        output_dir=resolve_path(args.output_dir),
        basename=args.basename,
        provider=args.provider,
        limit=args.limit,
        per_query_results=max(1, min(args.per_query_results, 5)),
        proposal_limit=max(1, args.proposal_limit),
    )
    summary = {
        "state": payload["state"],
        "provider": payload["provider"],
        "search_task_count": payload.get("search_task_count", 0),
        "searched_count": payload.get("searched_count", 0),
        "failed_count": payload.get("failed_count", 0),
        "candidate_proposal_count": payload.get("candidate_proposal_count", 0),
        "output_path": payload["output_path"],
        "markdown_path": payload["markdown_path"],
        "errors": payload.get("errors", []),
        "safety": payload["safety"],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Provider: {summary['provider']}")
        print(f"Search tasks: {summary['search_task_count']}")
        print(f"Searched: {summary['searched_count']}")
        print(f"Failed: {summary['failed_count']}")
        print(f"Candidate proposals: {summary['candidate_proposal_count']}")
        print(f"Output: {summary['output_path']}")
        print(f"Markdown: {summary['markdown_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
