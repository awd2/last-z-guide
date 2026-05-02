#!/usr/bin/env python3
"""Check crawler and snippet controls for public guide visibility."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
MEMORY_PATH = ROOT / "automation" / "memory" / "content_index.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.site_utils import load_all_pages


PUBLIC_ARCHETYPES = {
    "cornerstone-guide",
    "support-guide",
    "event-guide",
    "hero-profile",
    "comparison-guide",
    "atlas-page",
    "cost-page",
}
EXCLUDED_STATUSES = {"archived-noindex", "draft-noindex"}
FIRST_SCREEN_CLASSES = ("qa-lede", "guide-verified", "data-lede", "qa-callout")


def load_memory_pages() -> dict[str, dict]:
    payload = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    return {page["filename"]: page for page in payload["pages"]}


def robots_blocks_public_search(robots_text: str) -> list[str]:
    failures: list[str] = []
    if "Sitemap: https://lastzguides.com/sitemap.xml" not in robots_text:
        failures.append("robots.txt: missing canonical sitemap declaration")

    current_agents: list[str] = []
    for raw_line in robots_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = [part.strip() for part in line.split(":", 1)]
        key = key.lower()
        if key == "user-agent":
            current_agents = [value.lower()]
            continue
        if key != "disallow":
            continue
        if value in {"", "#"}:
            continue
        if value == "/" and any(agent in {"*", "googlebot", "bingbot", "oai-searchbot"} for agent in current_agents):
            failures.append(f"robots.txt: blocks public search crawler group `{', '.join(current_agents)}`")
    return failures


def robots_meta_content(raw_html: str) -> str:
    match = re.search(r'<meta\s+name="robots"\s+content="([^"]*)"', raw_html, flags=re.I)
    return match.group(1).casefold() if match else ""


def has_first_screen_data_nosnippet(raw_html: str) -> bool:
    for class_name in FIRST_SCREEN_CLASSES:
        patterns = [
            rf'<[^>]*data-nosnippet[^>]*class="[^"]*\b{re.escape(class_name)}\b[^"]*"',
            rf'<[^>]*class="[^"]*\b{re.escape(class_name)}\b[^"]*"[^>]*data-nosnippet',
        ]
        if any(re.search(pattern, raw_html, flags=re.I | re.S) for pattern in patterns):
            return True
    return False


def check_pages(memory: dict[str, dict]) -> list[str]:
    failures: list[str] = []
    for page in load_all_pages():
        meta = memory.get(page.filename)
        if not meta:
            continue
        if meta.get("status") in EXCLUDED_STATUSES:
            continue
        if meta.get("archetype") not in PUBLIC_ARCHETYPES:
            continue

        robots = robots_meta_content(page.text)
        if page.noindex:
            failures.append(f"{page.filename}: public guide is noindex")
        if "nosnippet" in robots:
            failures.append(f"{page.filename}: public guide disables snippets with nosnippet")
        if re.search(r"max-snippet\s*:\s*0(?:\D|$)", robots):
            failures.append(f"{page.filename}: public guide disables snippets with max-snippet:0")
        if has_first_screen_data_nosnippet(page.text):
            failures.append(f"{page.filename}: first-screen answer signal uses data-nosnippet")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Check public guide search and answer-feature visibility controls.")
    parser.parse_args()

    failures: list[str] = []
    robots_path = ROOT / "robots.txt"
    if not robots_path.exists():
        failures.append("robots.txt: missing")
    else:
        failures.extend(robots_blocks_public_search(robots_path.read_text(encoding="utf-8")))
    failures.extend(check_pages(load_memory_pages()))

    print("Checked search visibility controls for robots.txt and public guide pages.")
    if failures:
        print("Search visibility issues:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("Search visibility check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
