#!/usr/bin/env python3
"""Inventory page templates, component signals, and generated-source boundaries."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent.parent
MEMORY_PATH = ROOT / "automation" / "memory" / "content_index.json"
RESEARCH_BRANCH_DIR = ROOT / "data" / "research_branches"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.site_utils import load_all_pages


SIGNAL_PATTERNS = {
    "site_nav": r'<nav class="home-nav site-nav"',
    "home_nav": r'<nav class="home-nav"',
    "breadcrumb": r'class="breadcrumb"',
    "guide_article": r'<article class="[^"]*\bguide\b',
    "data_guide_article": r'<article class="[^"]*\bdata-guide\b',
    "quick_answer": r'class="quick-answer',
    "qa_lede": r'class="qa-lede"',
    "guide_verified": r'class="guide-verified"',
    "data_lede": r'class="data-lede"',
    "related_grid": r'class="related-grid"',
    "faq_section": r'class="faq-section"',
    "toc_placeholder": r'class="toc-placeholder"',
    "site_footer": r'class="site-footer"',
    "analytics_script": r'src="analytics\.js"',
    "search_loader_script": r'src="search-loader\.js"',
    "legacy_site_script": r'src="assets/site\.js"',
    "legacy_search_script": r'src="search\.js"',
}


def load_memory_pages() -> dict[str, dict[str, Any]]:
    payload = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    return {page["filename"]: page for page in payload["pages"]}


def generated_research_sources() -> dict[str, str]:
    outputs: dict[str, str] = {}
    for path in sorted(RESEARCH_BRANCH_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        slug = payload.get("page", {}).get("slug")
        if slug:
            outputs[f"{slug}.html"] = str(path.relative_to(ROOT))
    return outputs


def schema_types(text: str) -> list[str]:
    found: list[str] = []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S):
        try:
            payload = json.loads(block)
        except json.JSONDecodeError:
            found.append("invalid-json-ld")
            continue
        collect_schema_types(payload, found)
    return sorted(set(found))


def collect_schema_types(value: Any, found: list[str]) -> None:
    if isinstance(value, dict):
        item_type = value.get("@type")
        if isinstance(item_type, str):
            found.append(item_type)
        elif isinstance(item_type, list):
            found.extend(str(item) for item in item_type)
        for child in value.values():
            collect_schema_types(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_schema_types(child, found)


def active_nav_labels(text: str) -> list[str]:
    match = re.search(r'<nav class="home-nav site-nav"[^>]*>(.*?)</nav>', text, flags=re.S)
    if not match:
        return []
    labels = []
    for attrs, label in re.findall(r'<a\s+([^>]*)>(.*?)</a>', match.group(1), flags=re.S):
        if "is-active" not in attrs:
            continue
        clean = re.sub(r"<[^>]+>", " ", label)
        clean = re.sub(r"\s+", " ", clean).strip()
        labels.append(clean)
    return labels


def count_related_cards(text: str) -> int:
    match = re.search(r'<div class="related-grid">(.*?)</div>', text, flags=re.S)
    if not match:
        return 0
    return len(re.findall(r'<a\s+[^>]*class="related-card"', match.group(1)))


def page_record(page, memory: dict[str, dict[str, Any]], generated_sources: dict[str, str]) -> dict[str, Any]:
    meta = memory.get(page.filename, {})
    signals = {
        name: bool(re.search(pattern, page.text, flags=re.I))
        for name, pattern in SIGNAL_PATTERNS.items()
    }
    return {
        "filename": page.filename,
        "cluster": meta.get("cluster", "(missing memory)"),
        "archetype": meta.get("archetype", "(missing memory)"),
        "status": meta.get("status", "(missing memory)"),
        "noindex": page.noindex,
        "article_class": re.search(r'<article class="([^"]+)"', page.text).group(1)
        if re.search(r'<article class="([^"]+)"', page.text)
        else "",
        "active_nav": active_nav_labels(page.text),
        "schema_types": schema_types(page.text),
        "related_cards": count_related_cards(page.text),
        "signals": signals,
        "generated_source": generated_sources.get(page.filename, ""),
    }


def build_inventory() -> dict[str, Any]:
    memory = load_memory_pages()
    generated_sources = generated_research_sources()
    records = [page_record(page, memory, generated_sources) for page in load_all_pages()]

    by_cluster = Counter(record["cluster"] for record in records)
    by_archetype = Counter(record["archetype"] for record in records)
    schema_counts: Counter[str] = Counter()
    signal_coverage: dict[str, int] = {}
    for record in records:
        schema_counts.update(record["schema_types"])
    for signal in SIGNAL_PATTERNS:
        signal_coverage[signal] = sum(1 for record in records if record["signals"][signal])

    missing_by_signal: dict[str, list[str]] = defaultdict(list)
    for record in records:
        for signal, present in record["signals"].items():
            if not present:
                missing_by_signal[signal].append(record["filename"])

    return {
        "total_pages": len(records),
        "by_cluster": dict(sorted(by_cluster.items())),
        "by_archetype": dict(sorted(by_archetype.items())),
        "schema_counts": dict(sorted(schema_counts.items())),
        "signal_coverage": signal_coverage,
        "generated_research_pages": {
            record["filename"]: record["generated_source"]
            for record in records
            if record["generated_source"]
        },
        "pages": records,
        "missing_by_signal": dict(missing_by_signal),
    }


def md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def render_markdown(inventory: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Template Inventory",
        "",
        f"- Total HTML pages: {inventory['total_pages']}",
        f"- Generated research pages: {len(inventory['generated_research_pages'])}",
        "",
        "## Clusters",
        "",
        *md_table(
            ["Cluster", "Pages"],
            [[name, str(count)] for name, count in inventory["by_cluster"].items()],
        ),
        "",
        "## Archetypes",
        "",
        *md_table(
            ["Archetype", "Pages"],
            [[name, str(count)] for name, count in inventory["by_archetype"].items()],
        ),
        "",
        "## Component Coverage",
        "",
        *md_table(
            ["Signal", "Pages"],
            [[name, str(count)] for name, count in inventory["signal_coverage"].items()],
        ),
        "",
        "## Schema Types",
        "",
        *md_table(
            ["Schema Type", "Occurrences"],
            [[name, str(count)] for name, count in inventory["schema_counts"].items()],
        ),
        "",
        "## Generated Research Pages",
        "",
    ]

    generated_rows = [
        [filename, source]
        for filename, source in inventory["generated_research_pages"].items()
    ]
    lines.extend(md_table(["Output", "Source"], generated_rows or [["None", ""]]))
    lines.extend(["", "## Page Details", ""])
    page_rows = []
    for record in inventory["pages"]:
        schema = ", ".join(record["schema_types"]) or "none"
        active_nav = ", ".join(record["active_nav"]) or "none"
        page_rows.append(
            [
                record["filename"],
                record["cluster"],
                record["archetype"],
                record["article_class"] or "none",
                active_nav,
                str(record["related_cards"]),
                schema,
            ]
        )
    lines.extend(
        md_table(
            ["File", "Cluster", "Archetype", "Article Class", "Active Nav", "Related Cards", "Schema"],
            page_rows,
        )
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory page templates and component coverage.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown.")
    parser.add_argument("--output", help="Optional output path.")
    args = parser.parse_args()

    inventory = build_inventory()
    output = json.dumps(inventory, indent=2, ensure_ascii=False) if args.json else render_markdown(inventory)

    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
