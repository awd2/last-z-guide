#!/usr/bin/env python3
"""Render a compact LLM referral report from a GA4 CSV export."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


METRIC_ALIASES = {
    "sessions": ["sessions", "session", "ga4_sessions"],
    "events": ["event_count", "events", "event_count_per_user", "count"],
    "users": ["total_users", "users", "active_users"],
}

DIMENSION_ALIASES = {
    "event_name": ["event_name", "event name"],
    "llm_source": ["llm_source", "llm source"],
    "llm_channel": ["llm_channel", "llm channel"],
    "landing_page": ["landing_page", "landing page", "page_path", "page path", "page_location", "page location"],
    "referrer_host": ["referrer_host", "referrer host", "page_referrer", "page referrer"],
}


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def parse_number(value: str | None) -> float:
    if value is None:
        return 0.0
    cleaned = value.strip().replace(",", "")
    if not cleaned:
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def first_present(row: dict[str, str], aliases: list[str]) -> str:
    for alias in aliases:
        value = row.get(normalize_header(alias), "").strip()
        if value:
            return value
    return ""


def metric_value(row: dict[str, str], metric: str) -> float:
    for alias in METRIC_ALIASES[metric]:
        key = normalize_header(alias)
        if key in row:
            return parse_number(row.get(key))
    return 0.0


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")
        rows = []
        for raw_row in reader:
            rows.append({normalize_header(key or ""): value or "" for key, value in raw_row.items()})
    return rows


def is_llm_referral_row(row: dict[str, str]) -> bool:
    event_name = first_present(row, DIMENSION_ALIASES["event_name"])
    return not event_name or event_name == "llm_referral_session"


def summarize_dimension(rows: list[dict[str, Any]], dimension: str, top: int) -> list[dict[str, Any]]:
    totals: dict[str, dict[str, float]] = defaultdict(lambda: {"sessions": 0.0, "events": 0.0, "users": 0.0})
    for row in rows:
        label = row.get(dimension) or "(not set)"
        bucket = totals[label]
        bucket["sessions"] += row["sessions"]
        bucket["events"] += row["events"]
        bucket["users"] += row["users"]

    ranked = [
        {"label": label, **metrics}
        for label, metrics in totals.items()
    ]
    ranked.sort(key=lambda item: (item["sessions"], item["events"], item["users"]), reverse=True)
    return ranked[:top]


def build_report(rows: list[dict[str, str]], top: int) -> dict[str, Any]:
    normalized_rows = []
    skipped_non_event = 0
    for row in rows:
        if not is_llm_referral_row(row):
            skipped_non_event += 1
            continue
        normalized_rows.append(
            {
                "llm_source": first_present(row, DIMENSION_ALIASES["llm_source"]) or "(not set)",
                "llm_channel": first_present(row, DIMENSION_ALIASES["llm_channel"]) or "(not set)",
                "landing_page": first_present(row, DIMENSION_ALIASES["landing_page"]) or "(not set)",
                "referrer_host": first_present(row, DIMENSION_ALIASES["referrer_host"]) or "(not set)",
                "sessions": metric_value(row, "sessions"),
                "events": metric_value(row, "events"),
                "users": metric_value(row, "users"),
            }
        )

    totals = {
        "sessions": sum(row["sessions"] for row in normalized_rows),
        "events": sum(row["events"] for row in normalized_rows),
        "users": sum(row["users"] for row in normalized_rows),
    }
    missing = {
        "llm_source": sum(1 for row in normalized_rows if row["llm_source"] == "(not set)"),
        "llm_channel": sum(1 for row in normalized_rows if row["llm_channel"] == "(not set)"),
        "landing_page": sum(1 for row in normalized_rows if row["landing_page"] == "(not set)"),
        "referrer_host": sum(1 for row in normalized_rows if row["referrer_host"] == "(not set)"),
    }
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "input_rows": len(rows),
        "included_rows": len(normalized_rows),
        "skipped_non_llm_referral_rows": skipped_non_event,
        "totals": totals,
        "missing_dimensions": missing,
        "by_channel": summarize_dimension(normalized_rows, "llm_channel", top),
        "by_source": summarize_dimension(normalized_rows, "llm_source", top),
        "by_landing_page": summarize_dimension(normalized_rows, "landing_page", top),
        "by_referrer_host": summarize_dimension(normalized_rows, "referrer_host", top),
    }


def fmt(value: float) -> str:
    return str(int(value)) if value == int(value) else f"{value:.2f}"


def render_table(rows: list[dict[str, Any]], label_header: str) -> list[str]:
    lines = [
        f"| {label_header} | Sessions | Events | Users |",
        "| --- | ---: | ---: | ---: |",
    ]
    if not rows:
        lines.append("| None | 0 | 0 | 0 |")
        return lines
    for row in rows:
        lines.append(
            f"| {row['label']} | {fmt(row['sessions'])} | {fmt(row['events'])} | {fmt(row['users'])} |"
        )
    return lines


def render_markdown(report: dict[str, Any], source_path: Path) -> str:
    totals = report["totals"]
    missing = report["missing_dimensions"]
    lines = [
        "# LLM Referral Report",
        "",
        f"- Source CSV: `{source_path}`",
        f"- Generated at: `{report['generated_at']}`",
        f"- Input rows: {report['input_rows']}",
        f"- Included `llm_referral_session` rows: {report['included_rows']}",
        f"- Skipped non-LLM rows: {report['skipped_non_llm_referral_rows']}",
        f"- Total sessions: {fmt(totals['sessions'])}",
        f"- Total events: {fmt(totals['events'])}",
        f"- Total users: {fmt(totals['users'])}",
        "",
        "## Missing Dimensions",
        "",
        f"- `llm_source`: {missing['llm_source']}",
        f"- `llm_channel`: {missing['llm_channel']}",
        f"- `landing_page`: {missing['landing_page']}",
        f"- `referrer_host`: {missing['referrer_host']}",
        "",
        "## By Channel",
        "",
        *render_table(report["by_channel"], "Channel"),
        "",
        "## By Source",
        "",
        *render_table(report["by_source"], "Source"),
        "",
        "## By Landing Page",
        "",
        *render_table(report["by_landing_page"], "Landing Page"),
        "",
        "## By Referrer Host",
        "",
        *render_table(report["by_referrer_host"], "Referrer Host"),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render a deterministic LLM referral report from a GA4 Exploration CSV export."
    )
    parser.add_argument("csv_path", help="Path to a GA4 CSV export containing llm_referral_session rows.")
    parser.add_argument("--top", type=int, default=15, help="Number of rows to show per breakdown.")
    parser.add_argument("--output", help="Optional markdown output path. Defaults to stdout.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown.")
    args = parser.parse_args()

    source_path = Path(args.csv_path)
    if not source_path.exists():
        print(f"CSV not found: {source_path}", file=sys.stderr)
        return 1

    try:
        report = build_report(load_rows(source_path), max(args.top, 1))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        output = json.dumps(report, indent=2, ensure_ascii=False)
    else:
        output = render_markdown(report, source_path)

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
