#!/usr/bin/env python3
"""Fetch Bing Webmaster weekly performance signals for humans and agents."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timezone
from statistics import median
from typing import Any

OUT_DIR = "content/bing"
AGENT_SIGNALS_PATH = os.path.join(OUT_DIR, "latest-bing-agent-signals.json")
LATEST_REPORT_PATH = os.path.join(OUT_DIR, "latest-bing-report.md")
API_ROOT = "https://ssl.bing.com/webmaster/api.svc/json"


def get_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing env var: {name}")
    return value


def api_param(value: str, *, json_string: bool = False) -> str:
    return json.dumps(value) if json_string else value


def get_json(method: str, api_key: str, site_url: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    query = {"siteUrl": api_param(site_url), "apikey": api_key}
    if params:
        query.update(params)
    url = f"{API_ROOT}/{method}?{urllib.parse.urlencode(query)}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Bing Webmaster API {method} failed: HTTP {exc.code}: {error_body}") from exc
    return json.loads(raw) if raw else {}


def parse_bing_date(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if text.startswith("/Date("):
        inner = text.removeprefix("/Date(").removesuffix(")/")
        sign_indexes = [idx for idx in (inner.find("+", 1), inner.find("-", 1)) if idx != -1]
        ms_text = inner[: min(sign_indexes)] if sign_indexes else inner
        try:
            return datetime.fromtimestamp(int(ms_text) / 1000, tz=timezone.utc).date().isoformat()
        except ValueError:
            return ""
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return text[:10]


def metric(row: dict[str, Any], *names: str) -> float:
    for name in names:
        value = row.get(name)
        if value is None:
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return 0.0


def normalize_stats(rows: list[dict[str, Any]], label_field: str) -> list[dict[str, Any]]:
    normalized = []
    for row in rows:
        impressions = metric(row, "Impressions", "impressions")
        clicks = metric(row, "Clicks", "clicks")
        ctr = clicks / impressions if impressions else 0.0
        normalized.append(
            {
                label_field: str(row.get("Query") or row.get(label_field) or ""),
                "date": parse_bing_date(row.get("Date") or row.get("date")),
                "clicks": round(clicks, 2),
                "impressions": round(impressions, 2),
                "ctr": round(ctr, 6),
                "position": round(metric(row, "AvgImpressionPosition", "position"), 4),
                "avg_click_position": round(metric(row, "AvgClickPosition"), 4),
            }
        )
    return [row for row in normalized if row[label_field]]


def latest_bucket(rows: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    dates = sorted({row["date"] for row in rows if row.get("date")})
    if not dates:
        return "", rows
    latest = dates[-1]
    return latest, [row for row in rows if row.get("date") == latest]


def previous_bucket(rows: list[dict[str, Any]], latest: str) -> tuple[str, list[dict[str, Any]]]:
    dates = sorted({row["date"] for row in rows if row.get("date") and row.get("date") != latest})
    if not dates:
        return "", []
    previous = dates[-1]
    return previous, [row for row in rows if row.get("date") == previous]


def local_page_path(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lstrip("/")
    if not path:
        return "index.html"
    if path.endswith("/"):
        return path + "index.html"
    return path


def potential(row: dict[str, Any]) -> float:
    pos = float(row.get("position", 0.0))
    pos_factor = 1.2 if 4 <= pos <= 10 else 1.0
    return float(row.get("impressions", 0.0)) * (1 - float(row.get("ctr", 0.0))) * pos_factor


def ctr_median(rows: list[dict[str, Any]], min_impr: int) -> float:
    values = [float(r["ctr"]) for r in rows if float(r["impressions"]) >= min_impr]
    return median(values) if values else 0.0


def pick_insights(queries: list[dict[str, Any]], pages: list[dict[str, Any]], min_impr: int = 25) -> dict[str, Any]:
    query_ctr_median = ctr_median(queries, min_impr)
    page_ctr_median = ctr_median(pages, 100)
    low_ctr_good_pos = [
        row
        for row in queries
        if 4 <= float(row.get("position", 0)) <= 10
        and float(row.get("impressions", 0)) >= min_impr
        and float(row.get("ctr", 0)) <= query_ctr_median
    ]
    low_ctr_good_pos.sort(key=potential, reverse=True)
    high_impr_low_clicks = [
        row for row in queries if float(row.get("impressions", 0)) >= 100 and float(row.get("clicks", 0)) <= 3
    ]
    high_impr_low_clicks.sort(key=lambda row: float(row.get("impressions", 0)), reverse=True)
    quick_wins = [
        row
        for row in queries
        if 11 <= float(row.get("position", 0)) <= 20 and float(row.get("impressions", 0)) >= min_impr
    ]
    quick_wins.sort(key=potential, reverse=True)
    page_underperform = [
        row
        for row in pages
        if float(row.get("impressions", 0)) >= 100
        and float(row.get("ctr", 0)) <= page_ctr_median
        and 1 <= float(row.get("position", 0)) <= 15
    ]
    page_underperform.sort(key=lambda row: float(row.get("impressions", 0)), reverse=True)
    return {
        "ctr_median": query_ctr_median,
        "query_ctr_median": query_ctr_median,
        "page_ctr_median": page_ctr_median,
        "low_ctr_good_pos": low_ctr_good_pos[:25],
        "high_impr_low_clicks": high_impr_low_clicks[:25],
        "quick_wins": quick_wins[:25],
        "page_underperform": page_underperform[:25],
    }


def compute_rising(current: list[dict[str, Any]], previous: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    previous_map = {row[key]: row for row in previous}
    rows = []
    for row in current:
        prev = previous_map.get(row[key])
        if not prev:
            continue
        delta = float(row.get("impressions", 0)) - float(prev.get("impressions", 0))
        if delta <= 0:
            continue
        rows.append({**row, "delta_impressions": round(delta, 2)})
    rows.sort(key=lambda row: float(row["delta_impressions"]), reverse=True)
    return rows


def compute_new(current: list[dict[str, Any]], previous: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    previous_keys = {row[key] for row in previous}
    rows = [row for row in current if row[key] not in previous_keys]
    rows.sort(key=lambda row: float(row.get("impressions", 0)), reverse=True)
    return rows


def render_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def row_table(rows: list[dict[str, Any]], label_key: str) -> list[list[str]]:
    return [
        [
            str(row.get(label_key, "")),
            f'{row.get("clicks", 0):.0f}',
            f'{row.get("impressions", 0):.0f}',
            f'{row.get("ctr", 0) * 100:.2f}%',
            f'{row.get("position", 0):.2f}',
        ]
        for row in rows
    ]


def render_insight_list(rows: list[dict[str, Any]], label_key: str) -> list[str]:
    if not rows:
        return ["- (no items)"]
    return [
        (
            f"- {row.get(label_key, '')} - {row.get('impressions', 0):.0f} impr, "
            f"{row.get('clicks', 0):.0f} clicks, {row.get('ctr', 0) * 100:.2f}% CTR, "
            f"pos {row.get('position', 0):.2f}"
        )
        for row in rows
    ]


def query_page_rows(page_query_map: dict[str, list[dict[str, Any]]], latest_date: str) -> list[dict[str, Any]]:
    rows = []
    for page, page_rows in page_query_map.items():
        for row in page_rows:
            row_date = row.get("date")
            if latest_date and row_date and row_date != latest_date:
                continue
            rows.append(
                {
                    "query": row.get("query", ""),
                    "page": page,
                    "local_page": local_page_path(page),
                    "date": row_date or None,
                    "date_scope": "latest_week" if row_date else "page_query_detail_no_date",
                    "clicks": row.get("clicks", 0),
                    "impressions": row.get("impressions", 0),
                    "ctr": row.get("ctr", 0),
                    "position": row.get("position", 0),
                }
            )
    rows.sort(key=lambda row: float(row.get("impressions", 0)), reverse=True)
    return rows


def build_agent_signals(
    *,
    site_url: str,
    generated_for: str,
    latest_date: str,
    previous_date: str,
    rows_limit: int,
    query_rows: list[dict[str, Any]],
    page_rows: list[dict[str, Any]],
    query_page: list[dict[str, Any]],
    new_queries: list[dict[str, Any]],
    rising_queries: list[dict[str, Any]],
    fetch_errors: list[str],
    insights: dict[str, Any],
) -> dict[str, Any]:
    page_opportunities = []
    for row in insights["page_underperform"][:25]:
        item = {**row, "local_page": local_page_path(str(row.get("page", "")))}
        item["reason"] = "Bing page has high impressions with below-median CTR"
        page_opportunities.append(item)
    return {
        "schema_version": 1,
        "report_type": "bing_weekly_agent_signals",
        "generated_for": generated_for,
        "property": site_url,
        "data_window": {
            "latest_week": latest_date,
            "previous_week": previous_date or None,
            "source": "Bing Webmaster API weekly buckets",
        },
        "rows_limit": rows_limit,
        "agent_use": [
            "Use Bing query_opportunities to compare Bing intent against GSC before changing page snippets.",
            "Use Bing page_opportunities to find pages with impressions but weak Bing CTR.",
            "Use query_page_pairs to verify Bing query-to-page intent match and cannibalization risk.",
            "Do not create content from Bing data alone; check site memory, GSC signals, and canonical claims first.",
        ],
        "summary": {
            "query_rows": len(query_rows),
            "page_rows": len(page_rows),
            "query_page_rows": len(query_page),
            "fetch_errors": fetch_errors,
            "ctr_median_queries_min_25_impressions": round(float(insights["ctr_median"]), 6),
            "ctr_median_pages_min_100_impressions": round(float(insights["page_ctr_median"]), 6),
        },
        "query_opportunities": {
            "low_ctr_good_positions": insights["low_ctr_good_pos"][:25],
            "high_impressions_low_clicks": insights["high_impr_low_clicks"][:25],
            "quick_wins_positions_11_20": insights["quick_wins"][:25],
        },
        "trend_signals": {
            "new_queries_latest_week": new_queries[:25],
            "rising_queries_latest_vs_previous_week": rising_queries[:25],
        },
        "page_opportunities": page_opportunities,
        "query_page_pairs": query_page[:75],
    }


def fetch_page_query_rows(api_key: str, site_url: str, pages: list[str]) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    page_query_map: dict[str, list[dict[str, Any]]] = {}
    errors: list[str] = []
    for page in pages:
        try:
            data = get_json(
                "GetPageQueryStats",
                api_key,
                site_url,
                {"page": api_param(page, json_string=True)},
            )
        except RuntimeError as exc:
            errors.append(f"{page}: {exc}")
            continue
        page_query_map[page] = normalize_stats(data.get("d", []), "query")
    return page_query_map, errors


def main() -> int:
    site_url = get_env("BING_SITE_URL")
    api_key = get_env("BING_WEBMASTER_API_KEY")
    rows_limit = int(os.getenv("BING_ROWS", "250"))
    pair_pages = int(os.getenv("BING_PAIR_PAGES", "20"))

    query_raw = get_json("GetQueryStats", api_key, site_url).get("d", [])
    page_raw = get_json("GetPageStats", api_key, site_url).get("d", [])
    all_queries = normalize_stats(query_raw, "query")
    all_pages = normalize_stats(page_raw, "page")

    latest_query_date, query_rows = latest_bucket(all_queries)
    previous_query_date, previous_query_rows = previous_bucket(all_queries, latest_query_date)
    latest_page_date, page_rows = latest_bucket(all_pages)
    previous_page_date, _ = previous_bucket(all_pages, latest_page_date)
    latest_date = latest_query_date or latest_page_date
    previous_date = previous_query_date or previous_page_date

    query_rows.sort(key=lambda row: float(row.get("impressions", 0)), reverse=True)
    page_rows.sort(key=lambda row: float(row.get("impressions", 0)), reverse=True)
    query_rows = query_rows[:rows_limit]
    page_rows = page_rows[:rows_limit]

    top_pages = [str(row["page"]) for row in page_rows[:pair_pages]]
    page_query_map, fetch_errors = fetch_page_query_rows(api_key, site_url, top_pages)
    query_page = query_page_rows(page_query_map, latest_date)
    insights = pick_insights(query_rows, page_rows)
    new_queries = compute_new(query_rows, previous_query_rows, "query")
    rising_queries = compute_rising(query_rows, previous_query_rows, "query")

    os.makedirs(OUT_DIR, exist_ok=True)
    report_date = latest_date or date.today().isoformat()
    out_path = os.path.join(OUT_DIR, f"{report_date}-bing-report.md")

    lines = [
        f"# Bing Weekly Report - {report_date}",
        "",
        f"- Property: `{site_url}`",
        f"- Latest Bing bucket: {latest_date or 'unknown'}",
        f"- Previous Bing bucket: {previous_date or 'not available'}",
        f"- Rows limit: {rows_limit}",
        f"- Page-query detail pages requested: {len(top_pages)}",
        "",
        "## Queries (latest week, top by impressions)",
        "",
        *render_table(["Query", "Clicks", "Impr.", "CTR", "Pos."], row_table(query_rows, "query")),
        "",
        "## Pages (latest week, top by impressions)",
        "",
        *render_table(["Page", "Clicks", "Impr.", "CTR", "Pos."], row_table(page_rows, "page")),
        "",
        "## Query -> Page (top pages)",
        "",
    ]
    qp_table = [
        [
            row.get("query", ""),
            row.get("page", ""),
            f'{row.get("clicks", 0):.0f}',
            f'{row.get("impressions", 0):.0f}',
            f'{row.get("ctr", 0) * 100:.2f}%',
            f'{row.get("position", 0):.2f}',
        ]
        for row in query_page[:75]
    ]
    lines.extend(render_table(["Query", "Page", "Clicks", "Impr.", "CTR", "Pos."], qp_table))
    lines.extend(
        [
            "",
            "## New queries (latest week vs previous Bing bucket)",
            "",
        ]
    )
    lines.extend(render_table(["Query", "Clicks", "Impr.", "CTR", "Pos."], row_table(new_queries[:20], "query")) if new_queries else ["_No new queries in the latest Bing bucket._"])
    lines.extend(["", "## Rising queries (impression delta)", ""])
    if rising_queries:
        lines.extend(
            render_table(
                ["Query", "Delta Impr.", "Clicks", "Impr.", "CTR", "Pos."],
                [
                    [
                        row.get("query", ""),
                        f'{row.get("delta_impressions", 0):.0f}',
                        f'{row.get("clicks", 0):.0f}',
                        f'{row.get("impressions", 0):.0f}',
                        f'{row.get("ctr", 0) * 100:.2f}%',
                        f'{row.get("position", 0):.2f}',
                    ]
                    for row in rising_queries[:20]
                ],
            )
        )
    else:
        lines.append("_No rising queries by impressions._")
    lines.extend(
        [
            "",
            "## Insights (auto)",
            "",
            f"- CTR median for queries (impr >= 25): {insights['ctr_median'] * 100:.2f}%",
            f"- Page-query fetch warnings: {len(fetch_errors)}",
            "",
            "### Low CTR, good positions (4-10)",
            *render_insight_list(insights["low_ctr_good_pos"], "query"),
            "",
            "### High impressions, low clicks",
            *render_insight_list(insights["high_impr_low_clicks"], "query"),
            "",
            "### Quick wins (positions 11-20)",
            *render_insight_list(insights["quick_wins"], "query"),
            "",
            "### Pages underperforming (high impressions, low CTR)",
            *render_insight_list(insights["page_underperform"], "page"),
            "",
        ]
    )
    if fetch_errors:
        lines.extend(["## Fetch Warnings", ""])
        lines.extend(f"- {error}" for error in fetch_errors[:20])
        lines.append("")

    report_text = "\n".join(lines)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    with open(LATEST_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_text)

    agent_signals = build_agent_signals(
        site_url=site_url,
        generated_for=report_date,
        latest_date=latest_date,
        previous_date=previous_date,
        rows_limit=rows_limit,
        query_rows=query_rows,
        page_rows=page_rows,
        query_page=query_page,
        new_queries=new_queries,
        rising_queries=rising_queries,
        fetch_errors=fetch_errors,
        insights=insights,
    )
    with open(AGENT_SIGNALS_PATH, "w", encoding="utf-8") as f:
        json.dump(agent_signals, f, indent=2, sort_keys=True)
        f.write("\n")

    for name in os.listdir(OUT_DIR):
        if not name.endswith("-bing-report.md"):
            continue
        if name == os.path.basename(LATEST_REPORT_PATH):
            continue
        path = os.path.join(OUT_DIR, name)
        if os.path.abspath(path) == os.path.abspath(out_path):
            continue
        os.remove(path)

    print(f"Wrote {out_path} with {len(query_rows)} queries and {len(page_rows)} pages.")
    print(f"Wrote {LATEST_REPORT_PATH}.")
    print(f"Wrote {AGENT_SIGNALS_PATH}.")
    if fetch_errors:
        print(f"Warning: {len(fetch_errors)} page-query fetches failed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
