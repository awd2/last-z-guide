#!/usr/bin/env python3
"""Check or sync sitemap.xml and search-index.json against HTML pages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from site_utils import (
    BASE_URL,
    ROOT,
    canonical_url,
    derive_keywords,
    derive_search_description,
    derive_search_title,
    guess_search_category,
    list_html_pages,
    list_indexable_html_pages,
    load_all_pages,
    load_search_index,
    page_url,
    sitemap_changefreq,
    sitemap_priority,
    site_now_iso,
    write_search_index,
)


def parse_sitemap() -> dict[str, dict[str, str]]:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    entries: dict[str, dict[str, str]] = {}
    for block in re.findall(r"<url>(.*?)</url>", text, flags=re.S):
        loc = re.search(r"<loc>(.*?)</loc>", block)
        if not loc:
            continue
        url = loc.group(1).strip()
        path_part = url.replace(BASE_URL, "", 1) or "/"
        filename = "index.html" if path_part == "/" else path_part.lstrip("/")
        entries[filename] = {
            "loc": url,
            "lastmod": _match_or_default(block, "lastmod", site_now_iso()),
            "changefreq": _match_or_default(block, "changefreq", sitemap_changefreq(filename)),
            "priority": _match_or_default(block, "priority", sitemap_priority(filename)),
        }
    return entries


def _match_or_default(block: str, tag: str, default: str) -> str:
    match = re.search(fr"<{tag}>(.*?)</{tag}>", block)
    return match.group(1).strip() if match else default


def build_sitemap_entries() -> list[dict[str, str]]:
    existing = parse_sitemap()
    entries: list[dict[str, str]] = []
    for page in list_indexable_html_pages():
        filename = page.name
        lastmod = site_now_iso()
        if page.exists():
            lastmod = page.stat().st_mtime_ns
            lastmod = Path(page).stat().st_mtime
            from datetime import datetime

            lastmod = datetime.fromtimestamp(lastmod).date().isoformat()
        current = existing.get(filename, {})
        entries.append(
            {
                "filename": filename,
                "loc": canonical_url(filename),
                "lastmod": lastmod,
                "changefreq": current.get("changefreq", sitemap_changefreq(filename)),
                "priority": current.get("priority", sitemap_priority(filename)),
            }
        )

    def sort_key(item: dict[str, str]) -> tuple[int, str]:
        return (0 if item["filename"] == "index.html" else 1, item["filename"])

    return sorted(entries, key=sort_key)


def write_sitemap(entries: list[dict[str, str]]) -> None:
    path = ROOT / "sitemap.xml"
    lines = ['<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for entry in entries:
        lines.extend(
            [
                "    <url>",
                f"        <loc>{entry['loc']}</loc>",
                f"        <lastmod>{entry['lastmod']}</lastmod>",
                f"        <changefreq>{entry['changefreq']}</changefreq>",
                f"        <priority>{entry['priority']}</priority>",
                "    </url>",
            ]
        )
    lines.append("</urlset>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_search_entries() -> list[dict]:
    existing = {entry["url"]: entry for entry in load_search_index()}
    pages = [page for page in load_all_pages() if not page.noindex]
    entries: list[dict] = []
    for page in pages:
        url = page.filename
        current = existing.get(url, {})
        entry = {
            "url": url,
            "title": derive_search_title(page),
            "category": current.get("category") or guess_search_category(url),
            "description": derive_search_description(page),
            "keywords": current.get("keywords") or derive_keywords(page),
        }
        entries.append(entry)

    def sort_key(item: dict) -> tuple[int, str]:
        return (0 if item["url"] == "index.html" else 1, item["url"])

    return sorted(entries, key=sort_key)


def report_diffs() -> tuple[list[str], list[str], list[str], list[str]]:
    html_pages = {page.name for page in list_indexable_html_pages()}
    sitemap_pages = set(parse_sitemap())
    search_pages = {entry["url"] for entry in load_search_index()}

    missing_sitemap = sorted(html_pages - sitemap_pages)
    stale_sitemap = sorted(sitemap_pages - html_pages)
    missing_search = sorted(html_pages - search_pages)
    stale_search = sorted(search_pages - html_pages)
    return missing_sitemap, stale_sitemap, missing_search, stale_search


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or sync sitemap.xml and search-index.json."
    )
    parser.add_argument("--fix", action="store_true", help="Rewrite sitemap and search index.")
    args = parser.parse_args()

    missing_sitemap, stale_sitemap, missing_search, stale_search = report_diffs()

    if missing_sitemap:
        print("Missing from sitemap.xml:", ", ".join(missing_sitemap))
    if stale_sitemap:
        print("Stale in sitemap.xml:", ", ".join(stale_sitemap))
    if missing_search:
        print("Missing from search-index.json:", ", ".join(missing_search))
    if stale_search:
        print("Stale in search-index.json:", ", ".join(stale_search))

    if args.fix:
        write_sitemap(build_sitemap_entries())
        write_search_index(build_search_entries())
        print("Rebuilt sitemap.xml and search-index.json.")
        return 0

    if not any([missing_sitemap, stale_sitemap, missing_search, stale_search]):
        print("Indexing check passed: sitemap.xml and search-index.json are in sync.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
