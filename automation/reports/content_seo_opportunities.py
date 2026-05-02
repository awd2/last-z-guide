#!/usr/bin/env python3
"""Build a no-write SEO/LLM content opportunity report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_content_index, write_json
from scripts.site_utils import load_all_pages, normalize_whitespace, strip_tags

REPORTS_DIR = ROOT / "automation" / "reports"
GSC_SIGNALS_PATH = ROOT / "content" / "gsc" / "latest-gsc-agent-signals.json"
DEFAULT_JSON_OUTPUT = REPORTS_DIR / "content-seo-opportunities.json"
DEFAULT_MD_OUTPUT = REPORTS_DIR / "content-seo-opportunities.md"

TITLE_SOFT_LIMIT = 70
META_SOFT_LIMIT = 170
GUIDE_ARCHETYPES = {
    "cornerstone-guide",
    "support-guide",
    "event-guide",
    "comparison-guide",
    "hero-profile",
}
HIGH_RISK_ARCHETYPES = {"home-hub", "cornerstone-guide"}
GENERATED_RESEARCH_PAGES = {
    "hero-training-cost.html",
    "military-strategies-cost.html",
    "peace-shield-cost.html",
    "siege-to-seize-cost.html",
    "field-research.html",
    "army-building-cost.html",
    "fully-armed-alliance-cost.html",
    "unit-special-training-cost.html",
}


def rel(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def output_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def extract_section_text(class_name: str, html: str) -> str:
    pattern = rf'<section[^>]*class="[^"]*\b{re.escape(class_name)}\b[^"]*"[^>]*>(.*?)</section>'
    match = re.search(pattern, html, flags=re.I | re.S)
    if not match:
        return ""
    return strip_tags(match.group(1))


def count_related_cards(html: str) -> int:
    section = extract_section_text("related-guides", html)
    if not section:
        return 0
    related_match = re.search(
        r'<section[^>]*class="[^"]*\brelated-guides\b[^"]*"[^>]*>(.*?)</section>',
        html,
        flags=re.I | re.S,
    )
    if not related_match:
        return 0
    return len(re.findall(r'<a\b[^>]*href="[^"]+\.html"', related_match.group(1), flags=re.I))


def load_sitemap_lastmods() -> dict[str, str]:
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        return {}
    text = sitemap.read_text(encoding="utf-8")
    rows: dict[str, str] = {}
    for block in re.findall(r"<url>(.*?)</url>", text, flags=re.S | re.I):
        loc = re.search(r"<loc>(.*?)</loc>", block, flags=re.S | re.I)
        lastmod = re.search(r"<lastmod>(.*?)</lastmod>", block, flags=re.S | re.I)
        if not loc or not lastmod:
            continue
        filename = loc.group(1).rstrip("/").split("/")[-1] or "index.html"
        rows[filename] = normalize_whitespace(lastmod.group(1))
    return rows


def build_gsc_maps(payload: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    page_opportunities: dict[str, dict[str, Any]] = {}
    for row in payload.get("page_opportunities", []):
        local_page = row.get("local_page")
        if local_page:
            page_opportunities[str(local_page)] = row

    query_pairs: dict[str, list[dict[str, Any]]] = {}
    for row in payload.get("query_page_pairs", []):
        local_page = row.get("local_page")
        if not local_page:
            continue
        query_pairs.setdefault(str(local_page), []).append(row)

    low_ctr = payload.get("query_opportunities", {}).get("low_ctr_good_positions", [])
    for query in low_ctr:
        q = str(query.get("query", "")).lower()
        for local_page, rows in query_pairs.items():
            if any(str(row.get("query", "")).lower() == q for row in rows):
                continue
            # Keep query-to-page inference conservative and only attach exact topic hints.
            stem = local_page.replace(".html", "").replace("-", " ")
            if any(token in q for token in stem.split() if len(token) >= 4):
                rows.append({**query, "local_page": local_page, "inferred": True})

    return page_opportunities, query_pairs


def classify_risk(archetype: str, impressions: float, filename: str) -> str:
    if filename in GENERATED_RESEARCH_PAGES:
        return "medium"
    if archetype in HIGH_RISK_ARCHETYPES or impressions >= 7000:
        return "high"
    if impressions >= 2000:
        return "medium"
    return "low"


def score_page(
    *,
    impressions: float,
    ctr: float | None,
    position: float | None,
    title_len: int,
    meta_len: int,
    has_guide_verified: bool,
    archetype: str,
    filename: str,
    has_gsc_opportunity: bool,
) -> int:
    score = 0
    if impressions >= 7000:
        score += 5
    elif impressions >= 3000:
        score += 4
    elif impressions >= 1000:
        score += 2

    if has_gsc_opportunity:
        score += 3
    if ctr is not None and ctr < 0.025 and (position is None or position <= 9):
        score += 3
    if title_len > TITLE_SOFT_LIMIT:
        score += 2
    if meta_len > META_SOFT_LIMIT:
        score += 2
    if archetype in GUIDE_ARCHETYPES and not has_guide_verified:
        score += 1
    if filename in GENERATED_RESEARCH_PAGES:
        score += 1
    return score


def choose_action(
    *,
    filename: str,
    risk: str,
    archetype: str,
    has_gsc_opportunity: bool,
    title_len: int,
    meta_len: int,
    has_guide_verified: bool,
    impressions: float,
    ctr: float | None,
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    long_title = title_len > TITLE_SOFT_LIMIT
    long_meta = meta_len > META_SOFT_LIMIT
    low_ctr = ctr is not None and ctr < 0.025

    if has_gsc_opportunity:
        reasons.append("GSC page opportunity")
    if low_ctr:
        reasons.append("below-target CTR")
    if long_title:
        reasons.append("title is long")
    if long_meta:
        reasons.append("meta description is long")
    if archetype in GUIDE_ARCHETYPES and not has_guide_verified:
        reasons.append("missing guide-verified trust block")

    if filename in GENERATED_RESEARCH_PAGES and (has_gsc_opportunity or long_title or long_meta):
        return "generated_source_pass", reasons or ["generated research page"]
    if risk == "high" and has_gsc_opportunity:
        return "proposal_only_snippet_pass", reasons
    if has_gsc_opportunity and (low_ctr or long_title or long_meta):
        return "snippet_pass", reasons
    if impressions >= 2000 and archetype in GUIDE_ARCHETYPES and not has_guide_verified:
        return "trust_block_pass", reasons
    if long_title or long_meta:
        return "metadata_review", reasons
    return "monitor", reasons or ["no immediate deterministic issue"]


def build_report() -> dict[str, Any]:
    pages = {page.filename: page for page in load_all_pages() if not page.noindex}
    content_index = {page.filename: page for page in load_content_index()}
    sitemap_lastmods = load_sitemap_lastmods()
    gsc_payload = load_json_if_exists(GSC_SIGNALS_PATH)
    gsc_pages, gsc_pairs = build_gsc_maps(gsc_payload)

    opportunities: list[dict[str, Any]] = []
    for filename, page in sorted(pages.items()):
        index_row = content_index.get(filename)
        if not index_row:
            continue
        if index_row.status == "archived":
            continue

        quick_answer_text = extract_section_text("quick-answer", page.text)
        data_lede_text = extract_section_text("data-page-lede", page.text)
        first_screen_text = quick_answer_text or data_lede_text
        has_guide_verified = "guide-verified" in page.text
        gsc = gsc_pages.get(filename, {})
        impressions = float(gsc.get("impressions", 0) or 0)
        ctr = float(gsc["ctr"]) if "ctr" in gsc and gsc.get("ctr") is not None else None
        position = (
            float(gsc["position"])
            if "position" in gsc and gsc.get("position") is not None
            else None
        )
        title_len = len(page.title)
        meta_len = len(page.meta_description)
        risk = classify_risk(index_row.archetype, impressions, filename)
        score = score_page(
            impressions=impressions,
            ctr=ctr,
            position=position,
            title_len=title_len,
            meta_len=meta_len,
            has_guide_verified=has_guide_verified,
            archetype=index_row.archetype,
            filename=filename,
            has_gsc_opportunity=filename in gsc_pages,
        )
        action, reasons = choose_action(
            filename=filename,
            risk=risk,
            archetype=index_row.archetype,
            has_gsc_opportunity=filename in gsc_pages,
            title_len=title_len,
            meta_len=meta_len,
            has_guide_verified=has_guide_verified,
            impressions=impressions,
            ctr=ctr,
        )
        flags = []
        if filename in gsc_pages:
            flags.append("gsc_page_opportunity")
        if title_len > TITLE_SOFT_LIMIT:
            flags.append("long_title")
        if meta_len > META_SOFT_LIMIT:
            flags.append("long_meta")
        if index_row.archetype in GUIDE_ARCHETYPES and not has_guide_verified:
            flags.append("missing_trust_signal")
        if filename in GENERATED_RESEARCH_PAGES:
            flags.append("generated_research_page")
        if len(first_screen_text) < 250 and index_row.archetype in GUIDE_ARCHETYPES:
            flags.append("short_first_screen_answer")

        query_rows = sorted(
            gsc_pairs.get(filename, []),
            key=lambda row: float(row.get("impressions", 0) or 0),
            reverse=True,
        )
        opportunities.append(
            {
                "page": filename,
                "cluster": index_row.cluster,
                "archetype": index_row.archetype,
                "risk_level": risk,
                "priority_score": score,
                "safe_action": action,
                "reasons": reasons,
                "flags": flags,
                "metrics": {
                    "impressions": impressions,
                    "clicks": float(gsc.get("clicks", 0) or 0),
                    "ctr": ctr,
                    "position": position,
                    "title_len": title_len,
                    "meta_len": meta_len,
                    "first_screen_answer_len": len(first_screen_text),
                    "internal_links": len(page.internal_links),
                    "related_cards": count_related_cards(page.text),
                    "has_guide_verified": has_guide_verified,
                    "lastmod": sitemap_lastmods.get(filename),
                },
                "top_queries": [
                    {
                        "query": row.get("query"),
                        "impressions": float(row.get("impressions", 0) or 0),
                        "clicks": float(row.get("clicks", 0) or 0),
                        "ctr": float(row["ctr"]) if row.get("ctr") is not None else None,
                        "position": float(row["position"]) if row.get("position") is not None else None,
                        "inferred": bool(row.get("inferred", False)),
                    }
                    for row in query_rows[:5]
                ],
            }
        )

    opportunities.sort(
        key=lambda row: (
            row["priority_score"],
            row["metrics"]["impressions"],
            -1 if row["safe_action"] == "monitor" else 0,
        ),
        reverse=True,
    )
    action_counts: dict[str, int] = {}
    risk_counts: dict[str, int] = {}
    flag_counts: dict[str, int] = {}
    for row in opportunities:
        action_counts[row["safe_action"]] = action_counts.get(row["safe_action"], 0) + 1
        risk_counts[row["risk_level"]] = risk_counts.get(row["risk_level"], 0) + 1
        for flag in row["flags"]:
            flag_counts[flag] = flag_counts.get(flag, 0) + 1

    return {
        "report_type": "content_seo_opportunities",
        "generated_on": date.today().isoformat(),
        "source_inputs": {
            "content_index": "automation/memory/content_index.json",
            "gsc_signals": rel(GSC_SIGNALS_PATH) if GSC_SIGNALS_PATH.exists() else None,
            "sitemap": "sitemap.xml",
        },
        "policy": {
            "no_write_content": True,
            "do_not_rewrite_winners": True,
            "high_risk_pages_require_proposal_only_review": True,
            "generated_research_pages_use_json_source": True,
        },
        "summary": {
            "pages_evaluated": len(opportunities),
            "action_counts": dict(sorted(action_counts.items())),
            "risk_counts": dict(sorted(risk_counts.items())),
            "flag_counts": dict(sorted(flag_counts.items())),
            "gsc_generated_for": gsc_payload.get("generated_for"),
        },
        "opportunities": opportunities,
    }


def pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.2f}%"


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Content SEO / LLM Opportunity Report",
        "",
        f"Generated: {report['generated_on']}",
        f"GSC signals: {summary.get('gsc_generated_for') or 'not available'}",
        "",
        "This is a no-write review artifact. It prioritizes safe review passes; it does not recommend broad rewrites of pages that already rank.",
        "",
        "## Summary",
        "",
        f"- pages evaluated: {summary['pages_evaluated']}",
        "- action counts: "
        + ", ".join(f"{key}={value}" for key, value in summary["action_counts"].items()),
        "- risk counts: "
        + ", ".join(f"{key}={value}" for key, value in summary["risk_counts"].items()),
        "- flag counts: "
        + ", ".join(f"{key}={value}" for key, value in summary["flag_counts"].items()),
        "",
        "## Top Opportunities",
        "",
        "| Page | Cluster | Risk | Score | Action | GSC | Reasons |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for row in report["opportunities"][:20]:
        metrics = row["metrics"]
        gsc = (
            f"{int(metrics['impressions'])} impr / {pct(metrics['ctr'])} CTR / pos "
            f"{metrics['position']:.1f}"
            if metrics["impressions"]
            else "no GSC page signal"
        )
        reasons = ", ".join(row["reasons"])
        lines.append(
            f"| `{row['page']}` | {row['cluster']} | {row['risk_level']} | "
            f"{row['priority_score']} | `{row['safe_action']}` | {gsc} | {reasons} |"
        )

    lines.extend(
        [
            "",
            "## Safe Action Meanings",
            "",
            "- `proposal_only_snippet_pass`: high-risk page; only prepare a reviewed title/meta/first-screen proposal.",
            "- `snippet_pass`: review title, meta, H1 fit, and first-screen answer against GSC queries.",
            "- `generated_source_pass`: inspect JSON/source generator before changing generated research HTML.",
            "- `trust_block_pass`: consider adding or normalizing visible review/update trust signals.",
            "- `metadata_review`: inspect title/meta length and snippet fit before changing copy.",
            "- `monitor`: no immediate deterministic content issue.",
            "",
            "## Notes For Future Workers",
            "",
            "- Use this report as input context, not as permission to edit.",
            "- Cross-check `top_queries` in the JSON artifact before proposing changes.",
            "- Keep high-risk pages in proposal-only mode until human review.",
            "- Do not touch archived news / Reddit digest experiments.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(report: dict[str, Any], json_output: Path, markdown_output: Path) -> None:
    json_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    write_json(json_output, report)
    markdown_output.write_text(render_markdown(report) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print the report summary as JSON.")
    parser.add_argument(
        "--json-output",
        default=rel(DEFAULT_JSON_OUTPUT),
        help="Path for the full JSON artifact.",
    )
    parser.add_argument(
        "--markdown-output",
        default=rel(DEFAULT_MD_OUTPUT),
        help="Path for the markdown artifact.",
    )
    parser.add_argument("--no-write", action="store_true", help="Build and print only; do not write artifacts.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = build_report()
    if not args.no_write:
        write_report(report, output_path(args.json_output), output_path(args.markdown_output))

    payload = {
        "report_type": report["report_type"],
        "generated_on": report["generated_on"],
        "summary": report["summary"],
        "artifacts": {
            "json": None if args.no_write else rel(output_path(args.json_output)),
            "markdown": None if args.no_write else rel(output_path(args.markdown_output)),
        },
        "top_opportunities": [
            {
                "page": row["page"],
                "risk_level": row["risk_level"],
                "priority_score": row["priority_score"],
                "safe_action": row["safe_action"],
                "reasons": row["reasons"],
            }
            for row in report["opportunities"][:10]
        ],
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print("Content SEO / LLM Opportunity Report")
        print(f"- generated_on: {payload['generated_on']}")
        print(f"- pages_evaluated: {payload['summary']['pages_evaluated']}")
        print(f"- json: {payload['artifacts']['json'] or 'not written'}")
        print(f"- markdown: {payload['artifacts']['markdown'] or 'not written'}")
        print("- top opportunities:")
        for row in payload["top_opportunities"]:
            print(
                f"  - {row['page']} | risk={row['risk_level']} | score={row['priority_score']} | "
                f"action={row['safe_action']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
