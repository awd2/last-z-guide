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

from automation.io import load_content_index, load_json, write_json
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
READY_CHAIN_ACTIONS = {"update_existing", "create_new", "consolidate"}
CLUSTER_ALIASES = {
    "base": "Progression",
    "base-development": "Progression",
    "base development": "Progression",
    "building": "Progression",
    "codes": "Economy",
    "daily": "Routine",
    "events_daily_cycle": "Events",
    "events hub": "Events",
    "events_hub": "Events",
    "gear": "Equipment",
    "hero": "Heroes",
    "heroes_core": "Heroes",
    "home": "Home",
    "laboratory": "Research",
    "research-and-tech": "Research",
    "research and tech": "Research",
    "store": "Site",
    "tech": "Research",
}
CLUSTER_DEFAULT_TARGETS = {
    "Economy": "resources.html",
    "Equipment": "gear.html",
    "Events": "events.html",
    "Heroes": "heroes.html",
    "Home": "index.html",
    "Progression": "hq.html",
    "PvP": "pvp.html",
    "Research": "research.html",
    "Routine": "daily.html",
    "Seasons": "season-2-winter.html",
    "Site": "about.html",
    "Strategy": "tips.html",
}
NOISE_TITLE_PATTERNS = {
    "home",
    "index",
    "android apps on google play",
    "last z: survival shooter",
}
NOISE_URL_PARTS = {
    "/main/",
    "/main/vn/",
    "/en/index.html",
    "/store/apps/collection/",
}


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


def token_set(value: str) -> set[str]:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    stop = {"and", "for", "the", "last", "with", "guide", "guides", "wiki", "html", "survival", "shooter"}
    return {part for part in value.split() if len(part) > 2 and part not in stop}


def canonical_cluster(value: str, known_clusters: set[str]) -> str:
    raw = value.strip()
    if raw in known_clusters:
        return raw
    normalized = raw.lower().replace("_", " ").replace("-", " ")
    if normalized.title() in known_clusters:
        return normalized.title()
    if raw.lower() in CLUSTER_ALIASES:
        return CLUSTER_ALIASES[raw.lower()]
    if normalized in CLUSTER_ALIASES:
        return CLUSTER_ALIASES[normalized]
    for cluster in known_clusters:
        cluster_l = cluster.lower()
        if cluster_l in normalized or normalized in cluster_l:
            return cluster
    return ""


def page_lookup() -> tuple[dict[str, Any], set[str]]:
    pages = {page.filename: page for page in load_content_index()}
    clusters = {page.cluster for page in pages.values()}
    return pages, clusters


def score_page_match(result: dict[str, Any], task_record: dict[str, Any], page: Any) -> int:
    haystack = " ".join(
        [
            str(result.get("title", "")),
            str(result.get("url", "")),
            str(result.get("evidence_summary", "")),
            str(result.get("primary_user_job", "")),
            str(task_record.get("query", "")),
        ]
    )
    page_text = " ".join([page.filename, page.cluster, page.archetype, page.title_hint or ""])
    overlap = token_set(haystack) & token_set(page_text)
    score = len(overlap) * 6
    filename_stem = page.filename.removesuffix(".html").replace("-", " ")
    if filename_stem and filename_stem in haystack.lower():
        score += 24
    if page.cluster.lower() in haystack.lower():
        score += 10
    if page.archetype in {"cornerstone-guide", "atlas-page"}:
        score += 3
    return score


def infer_page_from_index(result: dict[str, Any], task_record: dict[str, Any], pages: dict[str, Any]) -> tuple[str, int, str]:
    target = safe_target_page(str(result.get("target_page_or_slug", "")).strip())
    if target in pages:
        return target, 100, "search_target_exact_content_index_match"

    best_page = ""
    best_score = 0
    for page in pages.values():
        if page.cluster == "News" or page.status != "published":
            continue
        score = score_page_match(result, task_record, page)
        if score > best_score:
            best_page = page.filename
            best_score = score
    reason = "content_index_token_match" if best_score >= 18 else "no_strong_page_match"
    return (best_page if best_score >= 18 else "", best_score, reason)


def is_noise_result(result: dict[str, Any]) -> tuple[bool, str]:
    title = str(result.get("title", "")).strip().lower()
    url = str(result.get("url", "")).strip().lower()
    if title in NOISE_TITLE_PATTERNS:
        return True, "generic_title"
    if any(part in url for part in NOISE_URL_PARTS):
        return True, "generic_or_locale_url"
    return False, ""


def trust_score(value: str) -> int:
    return {"high": 15, "medium": 8, "low": 0}.get(value.strip().lower(), 0)


def normalized_search_result(
    task_record: dict[str, Any],
    result: dict[str, Any],
    pages: dict[str, Any],
    known_clusters: set[str],
) -> dict[str, Any]:
    noise, noise_reason = is_noise_result(result)
    inferred_page, page_score, page_reason = infer_page_from_index(result, task_record, pages)
    explicit_target = safe_target_page(str(result.get("target_page_or_slug", "")).strip())
    target = inferred_page or explicit_target
    target_page = pages.get(target)
    raw_cluster = str(result.get("suggested_cluster", "")).strip()
    cluster = target_page.cluster if target_page else canonical_cluster(raw_cluster, known_clusters)
    if not cluster and target_page:
        cluster = target_page.cluster
    if not cluster:
        cluster = "Site"

    if not target and cluster in CLUSTER_DEFAULT_TARGETS:
        default_target = CLUSTER_DEFAULT_TARGETS[cluster]
        if default_target in pages:
            target = default_target
            page_reason = "cluster_default_target"
            page_score = max(page_score, 12)

    topic_fit = str(result.get("topic_fit", "low")).lower()
    action = str(result.get("recommended_action", "monitor")).strip()
    if action not in READY_ACTIONS:
        action = "monitor"
    score = {
        "high": 40,
        "medium": 22,
        "low": 0,
    }.get(topic_fit, 0)
    score += trust_score(str(task_record.get("trust_level", "")))
    if action in READY_CHAIN_ACTIONS:
        score += 10
    if cluster in known_clusters:
        score += 12
    if target in pages:
        score += 12
    if page_score >= 24:
        score += 8
    if noise:
        score -= 35
        action = "monitor"
    if not target:
        score -= 15
        action = "monitor"

    if score >= 62 and action in READY_CHAIN_ACTIONS:
        priority = "high"
        status = "candidate"
        confidence = "high" if topic_fit == "high" else "medium"
    elif score >= 42 and action in READY_CHAIN_ACTIONS:
        priority = "medium"
        status = "candidate"
        confidence = "medium"
    else:
        priority = "low" if score < 35 else "medium"
        status = "monitor"
        if action in READY_CHAIN_ACTIONS:
            action = "monitor"
        confidence = "low" if score < 35 else "medium"

    return {
        "cluster": cluster,
        "target_page_or_slug": target,
        "recommended_action": action,
        "priority": priority,
        "confidence": confidence,
        "status": status,
        "score": score,
        "mapping": {
            "raw_suggested_cluster": raw_cluster,
            "canonical_cluster": cluster,
            "raw_target_page_or_slug": result.get("target_page_or_slug", ""),
            "canonical_target_page_or_slug": target,
            "page_match_score": page_score,
            "page_match_reason": page_reason,
            "noise_result": noise,
            "noise_reason": noise_reason,
        },
    }


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


def proposal_from_result(
    task_record: dict[str, Any],
    result: dict[str, Any],
    index: int,
    pages: dict[str, Any],
    known_clusters: set[str],
) -> dict[str, Any]:
    source_id = str(task_record.get("source_id", "external-source"))
    title = str(result.get("title", "External search result")).strip() or "External search result"
    normalized = normalized_search_result(task_record, result, pages, known_clusters)
    action = normalized["recommended_action"]
    target = normalized["target_page_or_slug"]
    return {
        "topic_id": f"external-search-{slugify(source_id)}-{slugify(title)[:42]}-{index}",
        "title": f"External search opportunity: {title}",
        "cluster": normalized["cluster"],
        "recommended_action": action,
        "archetype_suggestion": pages[target].archetype if target in pages else "support-guide",
        "target_page_or_slug": target,
        "source_type": "external_search",
        "source_id": source_id,
        "source_name": task_record.get("source_name", ""),
        "source_reference": f"External search: {task_record.get('query', '')}",
        "confidence": normalized["confidence"],
        "priority": normalized["priority"],
        "risk_level": "high",
        "status": normalized["status"],
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
        "deterministic_mapping": normalized["mapping"],
        "opportunity_score": normalized["score"],
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
    pages, known_clusters = page_lookup()
    for record in search_records:
        if record.get("search_status") != "searched":
            continue
        for result in record.get("results", []):
            url = str(result.get("url", "")).strip()
            if not url or url in seen_urls or result.get("topic_fit") == "low":
                continue
            seen_urls.add(url)
            proposals.append(proposal_from_result(record, result, len(proposals) + 1, pages, known_clusters))
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
                    f"- Cluster: `{proposal.get('cluster', '')}`",
                    f"- Score: `{proposal.get('opportunity_score', '')}`",
                    f"- Source: `{proposal.get('source_reference', '')}`",
                    f"- URL: `{(proposal.get('source_urls') or [''])[0]}`",
                    f"- Mapping: `{proposal.get('deterministic_mapping', {}).get('page_match_reason', '')}`",
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
