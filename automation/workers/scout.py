#!/usr/bin/env python3
"""No-write Scout worker for analytics-backed topic proposals."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_canonical_claims, load_content_index, load_json, load_topic_backlog, write_json
from automation.proposal_renderer import md_list


DEFAULT_SIGNALS_PATH = ROOT / "content" / "gsc" / "latest-gsc-agent-signals.json"
REPORTS_DIR = ROOT / "automation" / "reports"

HUB_ROUTES = {
    "Economy": ["index.html", "codes.html"],
    "Events": ["index.html", "events.html"],
    "Equipment": ["index.html", "gear.html"],
    "Heroes": ["index.html", "heroes.html"],
    "Progression": ["index.html", "start.html"],
    "PvP": ["index.html", "pvp.html"],
    "Research": ["index.html", "research.html", "research-costs.html"],
    "Seasons": ["index.html", "start.html", "season-2-winter.html"],
    "Site": ["index.html"],
}

CORNERSTONE_RISK_ARCHETYPES = {"cornerstone-guide", "home-hub"}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "topic"


def local_page(value: str) -> str:
    if not value:
        return ""
    if value.startswith("http"):
        path = re.sub(r"^https?://[^/]+/?", "", value).split("#", 1)[0].split("?", 1)[0]
    else:
        path = value.split("#", 1)[0].split("?", 1)[0]
    return path or "index.html"


def load_signals(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"GSC agent signals not found: {path}")
    payload = load_json(path)
    if payload.get("report_type") != "gsc_weekly_agent_signals":
        raise ValueError(f"Unsupported GSC signal report type: {payload.get('report_type')}")
    return payload


def page_lookup() -> dict[str, Any]:
    return {page.filename: page for page in load_content_index()}


def existing_backlog_index() -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for item in load_topic_backlog():
        index.setdefault(item.target_page_or_slug, []).append(f"{item.topic_id}:{item.status}")
    return index


def protected_claims_for_page(filename: str) -> list[str]:
    claims = []
    for claim in load_canonical_claims():
        if filename in claim.related_pages:
            claims.append(claim.id)
    return claims


def expected_route(cluster: str, target: str) -> list[str]:
    route = []
    for page in HUB_ROUTES.get(cluster, ["index.html"]):
        if page not in route:
            route.append(page)
    if target not in route:
        route.append(target)
    return route


def risk_for_page(archetype: str, claims: list[str], impressions: float) -> str:
    if archetype in CORNERSTONE_RISK_ARCHETYPES:
        return "high"
    if claims:
        return "medium"
    if impressions >= 5000:
        return "medium"
    return "low"


def priority_for_signal(impressions: float, ctr: float, position: float) -> str:
    if impressions >= 5000:
        return "high"
    if impressions >= 1000 and ctr < 0.04 and position <= 10:
        return "high"
    return "medium"


def confidence_for_signal(query_count: int, impressions: float) -> str:
    if query_count >= 3 and impressions >= 1000:
        return "high"
    if impressions >= 300:
        return "medium"
    return "low"


def query_rows_for_page(signals: dict[str, Any], filename: str) -> list[dict[str, Any]]:
    rows = [
        row
        for row in signals.get("query_page_pairs", [])
        if local_page(str(row.get("local_page") or row.get("page", ""))) == filename
    ]
    rows.sort(key=lambda row: float(row.get("impressions", 0)), reverse=True)
    return rows


def low_ctr_queries_for_page(signals: dict[str, Any], filename: str) -> list[dict[str, Any]]:
    page_queries = {str(row.get("query", "")) for row in query_rows_for_page(signals, filename)}
    rows = [
        row
        for row in signals.get("query_opportunities", {}).get("low_ctr_good_positions", [])
        if str(row.get("query", "")) in page_queries
    ]
    rows.sort(key=lambda row: float(row.get("impressions", 0)), reverse=True)
    return rows


def rising_queries_for_page(signals: dict[str, Any], filename: str) -> list[dict[str, Any]]:
    page_queries = {str(row.get("query", "")) for row in query_rows_for_page(signals, filename)}
    rows = [
        row
        for row in signals.get("trend_signals", {}).get("rising_queries_last_7_vs_previous_7", [])
        if str(row.get("query", "")) in page_queries
    ]
    rows.sort(key=lambda row: float(row.get("delta_impressions", 0)), reverse=True)
    return rows


def evidence_for_page(signals: dict[str, Any], page_signal: dict[str, Any], filename: str) -> list[str]:
    evidence = [
        (
            f"GSC page signal: {filename} had {page_signal.get('impressions', 0):.0f} impressions, "
            f"{page_signal.get('clicks', 0):.0f} clicks, {page_signal.get('ctr', 0) * 100:.2f}% CTR, "
            f"avg position {page_signal.get('position', 0):.2f}."
        )
    ]
    for row in low_ctr_queries_for_page(signals, filename)[:5]:
        evidence.append(
            (
                f"Low CTR query: `{row.get('query')}` had {row.get('impressions', 0):.0f} impressions, "
                f"{row.get('clicks', 0):.0f} clicks, {row.get('ctr', 0) * 100:.2f}% CTR, "
                f"position {row.get('position', 0):.2f}."
            )
        )
    for row in rising_queries_for_page(signals, filename)[:3]:
        evidence.append(
            (
                f"Rising query: `{row.get('query')}` gained {row.get('delta_impressions', 0):.0f} impressions "
                f"in the last 7-day comparison window."
            )
        )
    return evidence


def primary_query(rows: list[dict[str, Any]], fallback: str) -> str:
    if rows:
        return str(rows[0].get("query", fallback))
    return fallback


def title_for_page(filename: str, title_hint: str | None) -> str:
    label = title_hint or filename.replace(".html", "").replace("-", " ").title()
    return f"GSC opportunity review: {label}"


def proposal_for_page(
    signals: dict[str, Any],
    page_signal: dict[str, Any],
    content_pages: dict[str, Any],
    backlog_index: dict[str, list[str]],
) -> dict[str, Any] | None:
    filename = local_page(str(page_signal.get("local_page") or page_signal.get("page", "")))
    page = content_pages.get(filename)
    if not page:
        return None
    if filename == "news-preview.html" or page.status == "archived-noindex":
        return None

    query_rows = query_rows_for_page(signals, filename)
    claims = protected_claims_for_page(filename)
    impressions = float(page_signal.get("impressions", 0))
    ctr = float(page_signal.get("ctr", 0))
    position = float(page_signal.get("position", 0))
    query = primary_query(query_rows, page.title_hint or filename)
    topic_id = f"{slugify(filename.removesuffix('.html'))}-gsc-opportunity"
    existing = backlog_index.get(filename, [])

    return {
        "topic_id": topic_id,
        "title": title_for_page(filename, page.title_hint),
        "cluster": page.cluster,
        "recommended_action": "update_existing",
        "archetype_suggestion": page.archetype,
        "target_page_or_slug": filename,
        "source_type": "analytics",
        "source_reference": f"GSC weekly {signals.get('generated_for')}: page opportunity and query-page signals",
        "confidence": confidence_for_signal(len(query_rows), impressions),
        "priority": priority_for_signal(impressions, ctr, position),
        "risk_level": risk_for_page(page.archetype, claims, impressions),
        "evidence": evidence_for_page(signals, page_signal, filename),
        "site_fit": {
            "primary_user_job": f"Improve query-to-page match and first-screen usefulness for `{query}` searchers.",
            "cluster_owner": page.cluster,
            "expected_internal_route": expected_route(page.cluster, filename),
            "archetype_reason": f"Existing page is `{page.archetype}` in the `{page.cluster}` cluster; Scout should prefer updating the existing page before proposing new content.",
        },
        "constraints": [
            "Use existing page template and navigation patterns.",
            "Treat GSC data as a signal, not proof that a rewrite is needed.",
            *[f"Protect canonical claim `{claim}`." for claim in claims],
            *([f"Existing backlog history for this page: {', '.join(existing)}."] if existing else []),
        ],
        "reject_if": [
            "The query intent is already better served by another canonical page.",
            "The proposed change would blur cluster role separation.",
            "The improvement cannot be expressed without changing a cornerstone page beyond the approved scope.",
        ],
    }


def build_proposals(signals: dict[str, Any], limit: int, min_impressions: int) -> list[dict[str, Any]]:
    content_pages = page_lookup()
    backlog_index = existing_backlog_index()
    proposals: list[dict[str, Any]] = []
    seen: set[str] = set()

    for page_signal in signals.get("page_opportunities", []):
        if float(page_signal.get("impressions", 0)) < min_impressions:
            continue
        proposal = proposal_for_page(signals, page_signal, content_pages, backlog_index)
        if not proposal:
            continue
        if proposal["topic_id"] in seen:
            continue
        proposals.append(proposal)
        seen.add(proposal["topic_id"])
        if len(proposals) >= limit:
            break
    return proposals


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Scout Topic Proposals - {payload['generated_at']}",
        "",
        "## Overview",
        "",
        f"- Source signals: `{payload['source_signals']}`",
        f"- Proposals: {payload['proposal_count']}",
        "- Safety: no backlog, content, or manifest files were modified by Scout.",
        "",
        "## Proposals",
        "",
    ]
    if not payload["proposals"]:
        lines.append("- None")
        return "\n".join(lines) + "\n"

    for proposal in payload["proposals"]:
        lines.extend(
            [
                f"### {proposal['topic_id']}",
                "",
                f"- Title: {proposal['title']}",
                f"- Target: `{proposal['target_page_or_slug']}`",
                f"- Cluster: `{proposal['cluster']}`",
                f"- Action: `{proposal['recommended_action']}`",
                f"- Archetype: `{proposal['archetype_suggestion']}`",
                f"- Priority: `{proposal['priority']}`",
                f"- Risk: `{proposal['risk_level']}`",
                f"- Confidence: `{proposal['confidence']}`",
                "",
                "Site Fit:",
                md_list(
                    [
                        f"Primary user job: {proposal['site_fit']['primary_user_job']}",
                        f"Expected internal route: {', '.join(proposal['site_fit']['expected_internal_route'])}",
                        proposal["site_fit"]["archetype_reason"],
                    ]
                ),
                "",
                "Evidence:",
                md_list(proposal["evidence"]),
                "",
                "Constraints:",
                md_list(proposal["constraints"]),
                "",
                "Reject If:",
                md_list(proposal["reject_if"]),
                "",
            ]
        )
    return "\n".join(lines)


def write_outputs(payload: dict[str, Any], output_dir: Path, basename: str) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{basename}.json"
    md_path = output_dir / f"{basename}.md"
    write_json(json_path, payload)
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    return json_path, md_path


def build_payload(signals_path: Path, limit: int, min_impressions: int) -> dict[str, Any]:
    signals = load_signals(signals_path)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    proposals = build_proposals(signals, limit=limit, min_impressions=min_impressions)
    return {
        "schema_version": 1,
        "report_type": "scout_topic_proposals",
        "generated_at": generated_at,
        "source_signals": str(signals_path.relative_to(ROOT) if signals_path.is_relative_to(ROOT) else signals_path),
        "source_generated_for": signals.get("generated_for"),
        "proposal_count": len(proposals),
        "proposals": proposals,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate no-write Scout topic proposals from GSC agent signals.")
    parser.add_argument("--signals", default=str(DEFAULT_SIGNALS_PATH), help="Path to latest-gsc-agent-signals.json.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for Scout proposal artifacts.")
    parser.add_argument("--basename", default="scout-topic-proposals", help="Output basename without extension.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum proposals to render.")
    parser.add_argument("--min-impressions", type=int, default=200, help="Minimum page impressions for a proposal.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    signals_path = Path(args.signals)
    if not signals_path.is_absolute():
        signals_path = ROOT / signals_path
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    payload = build_payload(signals_path, limit=args.limit, min_impressions=args.min_impressions)
    json_path, md_path = write_outputs(payload, output_dir, args.basename)

    summary = {
        "proposal_count": payload["proposal_count"],
        "json_path": str(json_path.relative_to(ROOT)),
        "markdown_path": str(md_path.relative_to(ROOT)),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Wrote {summary['json_path']}")
        print(f"Wrote {summary['markdown_path']}")
        print(f"Proposal count: {summary['proposal_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
