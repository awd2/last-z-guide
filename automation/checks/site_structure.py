#!/usr/bin/env python3
"""Check site-wide template, navigation, and generated-source boundaries."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
MEMORY_PATH = ROOT / "automation" / "memory" / "content_index.json"
RESEARCH_BRANCH_DIR = ROOT / "data" / "research_branches"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.site_utils import load_all_pages


NAV_LINKS = [
    ("/#progression", "Progression"),
    ("/#research-tech", "Research"),
    ("/#heroes-gear", "Heroes"),
    ("/#pvp-formations", "PvP"),
    ("/#events-competitive", "Events"),
    ("/#economy-f2p", "Economy"),
]

SPANISH_NAV_LINKS = [
    ("/#progression", "Progresión"),
    ("/#research-tech", "Investigación"),
    ("/#heroes-gear", "Héroes"),
    ("/#pvp-formations", "PvP"),
    ("/#events-competitive", "Eventos"),
    ("/#economy-f2p", "Economía"),
]

NAV_GROUP_BY_CLUSTER = {
    "Economy": "Economy",
    "Equipment": "Heroes",
    "Events": "Events",
    "Heroes": "Heroes",
    "Progression": "Progression",
    "PvP": "PvP",
    "Research": "Research",
    "Routine": "Events",
    "Strategy": "PvP",
}

NAV_GROUP_OVERRIDES = {
    "lucky-discounter.html": "Economy",
    "shield.html": "Economy",
    "svs.html": "PvP",
    "tips.html": "Economy",
    "vehicle-modification-cost.html": "Progression",
}

SITE_ONLY_CLUSTERS = {"Home", "Site", "News"}
NO_ARTICLE_ARCHETYPES = {"home-hub", "site-page", "news-digest"}
GUIDE_ARCHETYPES = {
    "cornerstone-guide",
    "support-guide",
    "event-guide",
    "hero-profile",
    "comparison-guide",
}
DATA_ARCHETYPES = {"atlas-page", "cost-page"}


def load_memory_pages() -> dict[str, dict]:
    payload = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    return {page["filename"]: page for page in payload["pages"]}


def research_generated_outputs() -> dict[str, str]:
    outputs: dict[str, str] = {}
    for path in sorted(RESEARCH_BRANCH_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        slug = payload.get("page", {}).get("slug")
        if slug:
            outputs[f"{slug}.html"] = str(path.relative_to(ROOT))
    return outputs


def extract_nav(text: str) -> list[tuple[str, str, bool]]:
    match = re.search(r'<nav class="home-nav site-nav"[^>]*>(.*?)</nav>', text, flags=re.S)
    if not match:
        return []
    nav_links: list[tuple[str, str, bool]] = []
    for raw_attrs, label in re.findall(r'<a\s+([^>]*href="[^"]+"[^>]*)>(.*?)</a>', match.group(1), flags=re.S):
        href_match = re.search(r'href="([^"]+)"', raw_attrs)
        if not href_match:
            continue
        href = href_match.group(1)
        clean_label = re.sub(r"<[^>]+>", " ", label)
        clean_label = re.sub(r"\s+", " ", clean_label).strip()
        nav_links.append((href, clean_label, "is-active" in raw_attrs))
    return nav_links


def expected_nav_group(filename: str, meta: dict) -> str | None:
    if filename in NAV_GROUP_OVERRIDES:
        return NAV_GROUP_OVERRIDES[filename]
    return NAV_GROUP_BY_CLUSTER.get(meta.get("cluster"))


def check_navigation(pages: dict[str, object], memory: dict[str, dict]) -> list[str]:
    failures: list[str] = []

    for filename, page in sorted(pages.items()):
        meta = memory.get(filename)
        nav = extract_nav(page.text)
        if not nav:
            if meta and meta.get("cluster") not in {"Home", "News"}:
                failures.append(f"{filename}: missing site-nav")
            continue

        expected_links = SPANISH_NAV_LINKS if filename == "heroes-es.html" else NAV_LINKS
        actual_links = [(href, label) for href, label, _active in nav]
        if actual_links != expected_links:
            failures.append(f"{filename}: site-nav link order or labels drifted")

        if not meta or meta.get("cluster") in SITE_ONLY_CLUSTERS:
            continue

        active = [label for _href, label, is_active in nav if is_active]
        expected_group = expected_nav_group(filename, meta)
        if expected_group is None:
            continue
        if filename == "heroes-es.html":
            expected_group = "Héroes"

        if active != [expected_group]:
            failures.append(f"{filename}: expected active nav `{expected_group}`, found {active or 'none'}")

    return failures


def check_template_signals(pages: dict[str, object], memory: dict[str, dict]) -> list[str]:
    failures: list[str] = []
    for filename, meta in sorted(memory.items()):
        if filename not in pages:
            continue
        if meta.get("cluster") in SITE_ONLY_CLUSTERS or meta.get("archetype") in NO_ARTICLE_ARCHETYPES:
            continue

        text = pages[filename].text
        article_class = re.search(r'<article class="([^"]+)"', text)
        if not article_class:
            failures.append(f"{filename}: missing article wrapper")
            continue

        classes = set(article_class.group(1).split())
        archetype = meta.get("archetype")
        if archetype in GUIDE_ARCHETYPES and not ({"guide", "guide-content"} & classes):
            failures.append(f"{filename}: guide archetype missing guide article class")
        if archetype in DATA_ARCHETYPES and "data-guide" not in classes:
            failures.append(f"{filename}: data archetype missing data-guide article class")

        if 'class="breadcrumb"' not in text:
            failures.append(f"{filename}: missing breadcrumb")
        if 'class="related-grid"' not in text:
            failures.append(f"{filename}: missing related-grid")
        if 'class="qa-lede"' not in text and 'class="guide-verified"' not in text and 'class="data-lede"' not in text:
            failures.append(f"{filename}: missing first-screen answer signal")

    return failures


def check_generated_research_sources(memory: dict[str, dict]) -> list[str]:
    failures: list[str] = []
    generated_outputs = research_generated_outputs()
    for filename, source in generated_outputs.items():
        path = ROOT / filename
        if not path.exists():
            failures.append(f"{filename}: generated output missing for {source}")
            continue
        meta = memory.get(filename)
        if not meta:
            failures.append(f"{filename}: generated output missing from content_index memory")
            continue
        if meta.get("cluster") != "Research" or meta.get("archetype") != "cost-page":
            failures.append(f"{filename}: generated research output has wrong memory role")
        if "research-branch-guide" not in path.read_text(encoding="utf-8"):
            failures.append(f"{filename}: generated research output missing research-branch-guide class")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Check site structure and template consistency.")
    parser.parse_args()

    memory = load_memory_pages()
    pages = {page.filename: page for page in load_all_pages()}

    failures = []
    failures.extend(check_navigation(pages, memory))
    failures.extend(check_template_signals(pages, memory))
    failures.extend(check_generated_research_sources(memory))

    checked_guides = sum(
        1
        for filename, meta in memory.items()
        if filename in pages
        and meta.get("cluster") not in SITE_ONLY_CLUSTERS
        and meta.get("archetype") not in NO_ARTICLE_ARCHETYPES
    )
    print(f"Checked site structure on {len(pages)} HTML pages and {checked_guides} guide/data pages.")

    if failures:
        print("Site structure issues:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("Site structure check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
