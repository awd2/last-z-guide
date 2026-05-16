#!/usr/bin/env python3
"""No-write external evidence collector for approved explicit URL leads."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_json, write_json
from automation.proposal_renderer import md_list


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_EVIDENCE_REFRESH = REPORTS_DIR / "external-evidence-refresh.json"
USER_AGENT = "lastzguides-evidence-bot/1.0 (+https://lastzguides.com)"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def clean_text(value: str, limit: int = 320) -> str:
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def extract_first(pattern: str, source: str) -> str:
    match = re.search(pattern, source, flags=re.IGNORECASE | re.DOTALL)
    return clean_text(match.group(1)) if match else ""


def extract_all(pattern: str, source: str, limit: int) -> list[str]:
    values: list[str] = []
    for match in re.finditer(pattern, source, flags=re.IGNORECASE | re.DOTALL):
        value = clean_text(re.sub(r"<[^>]+>", " ", match.group(1)), limit=140)
        if value and value not in values:
            values.append(value)
        if len(values) >= limit:
            break
    return values


def visible_text_sample(source: str) -> str:
    source = re.sub(r"<script\b[^>]*>.*?</script>", " ", source, flags=re.IGNORECASE | re.DOTALL)
    source = re.sub(r"<style\b[^>]*>.*?</style>", " ", source, flags=re.IGNORECASE | re.DOTALL)
    source = re.sub(r"<[^>]+>", " ", source)
    return clean_text(source, limit=260)


def extract_html_summary(body: bytes, content_type: str) -> dict[str, Any]:
    charset = "utf-8"
    charset_match = re.search(r"charset=([^;\s]+)", content_type, flags=re.IGNORECASE)
    if charset_match:
        charset = charset_match.group(1).strip("\"'")
    text = body.decode(charset, errors="replace")
    title = extract_first(r"<title[^>]*>(.*?)</title>", text)
    meta_description = extract_first(
        r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"'](.*?)[\"'][^>]*>",
        text,
    )
    if not meta_description:
        meta_description = extract_first(
            r"<meta[^>]+content=[\"'](.*?)[\"'][^>]+name=[\"']description[\"'][^>]*>",
            text,
        )
    canonical_url = extract_first(
        r"<link[^>]+rel=[\"']canonical[\"'][^>]+href=[\"'](.*?)[\"'][^>]*>",
        text,
    )
    h1s = extract_all(r"<h1[^>]*>(.*?)</h1>", text, limit=3)
    return {
        "title": title,
        "meta_description": meta_description,
        "canonical_url": canonical_url,
        "h1s": h1s,
        "short_text_sample": visible_text_sample(text),
    }


def fetch_url(url: str, timeout: float, max_bytes: int) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        body = response.read(max_bytes + 1)
        truncated = len(body) > max_bytes
        if truncated:
            body = body[:max_bytes]
        content_type = response.headers.get("content-type", "")
        summary = extract_html_summary(body, content_type) if "html" in content_type.lower() else {}
        return {
            "status_code": getattr(response, "status", 0),
            "final_url": response.geturl(),
            "content_type": content_type,
            "bytes_read": len(body),
            "truncated": truncated,
            **summary,
        }


def fixture_fetch(lead: dict[str, Any]) -> dict[str, Any]:
    return {
        "status_code": 200,
        "final_url": lead.get("url", ""),
        "content_type": "text/html; charset=utf-8",
        "bytes_read": 0,
        "truncated": False,
        "title": f"Fixture evidence for {lead.get('lead_id', '')}",
        "meta_description": "Fixture metadata for offline external evidence collection tests.",
        "canonical_url": lead.get("url", ""),
        "h1s": [],
        "short_text_sample": "Fixture sample. Not public evidence.",
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


def collect_lead(lead: dict[str, Any], provider: str, timeout: float, max_bytes: int) -> dict[str, Any]:
    url = str(lead.get("url", "")).strip()
    base = {
        "lead_id": lead.get("lead_id", ""),
        "topic_id": lead.get("topic_id", ""),
        "source_id": lead.get("source_id", ""),
        "source_reference": lead.get("source_reference", ""),
        "target_page_or_slug": lead.get("target_page_or_slug", ""),
        "url": url,
        "claims_to_verify": lead.get("claims_to_verify", []),
        "public_claim_ready": False,
        "collected_at": now_utc(),
    }
    if not url.startswith("https://"):
        return {**base, "collection_status": "blocked_invalid_url", "error": "Only https explicit URL leads are allowed."}
    try:
        evidence = fixture_fetch(lead) if provider == "fixture" else fetch_url(url, timeout=timeout, max_bytes=max_bytes)
    except HTTPError as exc:
        return {**base, "collection_status": "fetch_failed", "status_code": exc.code, "error": str(exc)}
    except URLError as exc:
        return {**base, "collection_status": "fetch_failed", "error": str(exc.reason)}
    except Exception as exc:  # noqa: BLE001 - collect errors as artifact data, not workflow crashes.
        return {**base, "collection_status": "fetch_failed", "error": str(exc)}
    return {
        **base,
        "collection_status": "collected",
        "evidence_type": "metadata_and_short_snippet",
        "copyright_policy": "Short metadata/snippet only. Do not copy source wording into public content.",
        **evidence,
    }


def build_claim_collection_summary(collected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    claims: dict[str, dict[str, Any]] = {}
    for item in collected:
        if item.get("collection_status") != "collected":
            continue
        for raw_claim in item.get("claims_to_verify", []):
            claim = str(raw_claim).strip()
            if not claim:
                continue
            summary = claims.setdefault(
                claim,
                {
                    "claim_id": claim,
                    "collected_source_ids": [],
                    "collected_urls": [],
                    "review_status": "collected_single_source_needs_cross_validation",
                    "public_claim_ready": False,
                },
            )
            for key, value in [
                ("collected_source_ids", item.get("source_id", "")),
                ("collected_urls", item.get("url", "")),
            ]:
                if value and value not in summary[key]:
                    summary[key].append(value)
    for summary in claims.values():
        if len(summary["collected_source_ids"]) >= 2 or len(summary["collected_urls"]) >= 2:
            summary["review_status"] = "collected_multiple_sources_needs_human_validation"
    return sorted(claims.values(), key=lambda item: item["claim_id"])


def build_external_evidence_collect(
    evidence_refresh_path: Path,
    output_dir: Path,
    basename: str,
    provider: str,
    limit: int,
    timeout: float,
    max_bytes: int,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    if provider == "disabled":
        payload = {
            "schema_version": 1,
            "report_type": "external_evidence_collect",
            "generated_at": now_utc(),
            "state": "blocked",
            "provider": provider,
            "evidence_refresh_path": rel(evidence_refresh_path),
            "collected_evidence": [],
            "query_tasks_deferred": [],
            "claim_collection_summary": [],
            "errors": ["No external evidence collection provider is enabled."],
            "output_path": rel(json_path),
            "markdown_path": rel(markdown_path),
            "allows_content_edit": False,
            "allows_backlog_mutation": False,
            "allows_manifest_mutation": False,
            "allows_pr_or_deploy": False,
            "safety": "No content, backlog, manifest, PR, or production files were modified by External Evidence Collect.",
        }
        write_json(json_path, payload)
        markdown_path.write_text(render_markdown(payload), encoding="utf-8")
        return 1, payload

    errors, refresh = load_evidence_refresh(evidence_refresh_path)
    if errors:
        payload = {
            "schema_version": 1,
            "report_type": "external_evidence_collect",
            "generated_at": now_utc(),
            "state": "blocked",
            "provider": provider,
            "evidence_refresh_path": rel(evidence_refresh_path),
            "collected_evidence": [],
            "query_tasks_deferred": [],
            "claim_collection_summary": [],
            "errors": errors,
            "output_path": rel(json_path),
            "markdown_path": rel(markdown_path),
            "allows_content_edit": False,
            "allows_backlog_mutation": False,
            "allows_manifest_mutation": False,
            "allows_pr_or_deploy": False,
            "safety": "No content, backlog, manifest, PR, or production files were modified by External Evidence Collect.",
        }
        write_json(json_path, payload)
        markdown_path.write_text(render_markdown(payload), encoding="utf-8")
        return 1, payload

    leads = [lead for lead in refresh.get("url_evidence_leads", []) if isinstance(lead, dict)][: max(0, limit)]
    collected = [collect_lead(lead, provider=provider, timeout=timeout, max_bytes=max_bytes) for lead in leads]
    collected_count = sum(1 for item in collected if item.get("collection_status") == "collected")
    failed_count = sum(1 for item in collected if item.get("collection_status") != "collected")
    query_tasks = refresh.get("source_query_tasks", [])
    if collected_count and failed_count:
        state = "evidence_collection_partial"
    elif collected_count:
        state = "evidence_collected"
    elif leads:
        state = "evidence_collection_failed"
    else:
        state = "no_fetchable_url_leads"
    payload = {
        "schema_version": 1,
        "report_type": "external_evidence_collect",
        "generated_at": now_utc(),
        "state": state,
        "provider": provider,
        "evidence_refresh_path": rel(evidence_refresh_path),
        "url_lead_count": len(leads),
        "collected_count": collected_count,
        "failed_count": failed_count,
        "query_task_count": len(query_tasks) if isinstance(query_tasks, list) else 0,
        "collected_evidence": collected,
        "query_tasks_deferred": query_tasks if isinstance(query_tasks, list) else [],
        "claim_collection_summary": build_claim_collection_summary(collected),
        "errors": [],
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": False,
        "allows_pr_or_deploy": False,
        "next_actions": [
            "Review collected metadata/snippets as discovery evidence only.",
            "Use a separate search provider for deferred source_query_tasks before treating topic discovery as complete.",
            "Never use one external source as proof for public mechanic, cost, reward, season, or event claims.",
            "Public content still requires exact proposed text, owner approval, apply-preview, apply-approved, and strict QA.",
        ],
        "safety": "No content, backlog, manifest, PR, or production files were modified by External Evidence Collect.",
    }
    write_json(json_path, payload)
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return 0, payload


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# External Evidence Collect - {payload.get('generated_at', '')}",
        "",
        "## Outcome",
        "",
        f"- State: `{payload.get('state', '')}`",
        f"- Provider: `{payload.get('provider', '')}`",
        f"- Evidence Refresh: `{payload.get('evidence_refresh_path', '')}`",
        f"- URL leads: `{payload.get('url_lead_count', 0)}`",
        f"- Collected: `{payload.get('collected_count', 0)}`",
        f"- Failed: `{payload.get('failed_count', 0)}`",
        f"- Deferred query tasks: `{payload.get('query_task_count', 0)}`",
        "- Allows content edit: `false`",
        "- Allows backlog mutation: `false`",
        "- Allows manifest mutation: `false`",
        "- Allows PR/deploy: `false`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if payload.get("errors"):
        lines.extend(["## Errors", "", md_list(payload["errors"]), ""])
    if payload.get("collected_evidence"):
        lines.extend(["## Collected Evidence", ""])
        for item in payload["collected_evidence"]:
            lines.extend(
                [
                    f"### {item.get('lead_id', '')}",
                    "",
                    f"- Status: `{item.get('collection_status', '')}`",
                    f"- Topic: `{item.get('topic_id', '')}`",
                    f"- Source: `{item.get('source_reference', '')}`",
                    f"- URL: `{item.get('url', '')}`",
                    f"- Final URL: `{item.get('final_url', '')}`",
                    f"- HTTP status: `{item.get('status_code', '')}`",
                    f"- Title: {item.get('title', '')}",
                    f"- Meta description: {item.get('meta_description', '')}",
                    "- Public claim ready: `false`",
                    "",
                ]
            )
            if item.get("error"):
                lines.extend(["Error:", "", f"- {item.get('error', '')}", ""])
    if payload.get("claim_collection_summary"):
        lines.extend(["## Claim Collection Summary", ""])
        for item in payload["claim_collection_summary"]:
            lines.append(
                f"- `{item.get('claim_id', '')}`: {item.get('review_status', '')}; collected_sources={len(item.get('collected_source_ids', []))}; public_claim_ready=false"
            )
        lines.append("")
    if payload.get("query_tasks_deferred"):
        lines.extend(["## Deferred Search Tasks", ""])
        lines.append("Search tasks are not executed by the fetch provider.")
        lines.append("")
        for task in payload["query_tasks_deferred"]:
            lines.append(f"- `{task.get('task_id', '')}`: {task.get('query', '')}")
        lines.append("")
    lines.extend(["## Next Actions", "", md_list(payload.get("next_actions", [])), ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect no-write external evidence from explicit URL leads.")
    parser.add_argument("--evidence-refresh", default=str(DEFAULT_EVIDENCE_REFRESH), help="Path to external-evidence-refresh.json.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for External Evidence Collect artifacts.")
    parser.add_argument("--basename", default="external-evidence-collect", help="Output basename without extension.")
    parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "fetch"],
        help="Evidence provider. `fetch` reads only explicit URL leads. Defaults to disabled/fail-closed.",
    )
    parser.add_argument("--limit", type=int, default=20, help="Maximum explicit URL leads to collect.")
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-URL fetch timeout in seconds.")
    parser.add_argument("--max-bytes", type=int, default=750000, help="Maximum bytes to read per URL.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    code, payload = build_external_evidence_collect(
        evidence_refresh_path=resolve_path(args.evidence_refresh),
        output_dir=resolve_path(args.output_dir),
        basename=args.basename,
        provider=args.provider,
        limit=args.limit,
        timeout=args.timeout,
        max_bytes=args.max_bytes,
    )
    summary = {
        "state": payload["state"],
        "provider": payload["provider"],
        "url_lead_count": payload.get("url_lead_count", 0),
        "collected_count": payload.get("collected_count", 0),
        "failed_count": payload.get("failed_count", 0),
        "query_task_count": payload.get("query_task_count", 0),
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
        print(f"URL leads: {summary['url_lead_count']}")
        print(f"Collected: {summary['collected_count']}")
        print(f"Failed: {summary['failed_count']}")
        print(f"Deferred query tasks: {summary['query_task_count']}")
        print(f"Output: {summary['output_path']}")
        print(f"Markdown: {summary['markdown_path']}")
        if summary["errors"]:
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
