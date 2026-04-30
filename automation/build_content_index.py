#!/usr/bin/env python3
"""Build and compare the current HTML inventory against automation memory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MEMORY_PATH = ROOT / "automation" / "memory" / "content_index.json"
CURRENT_PATH = ROOT / "automation" / "memory" / "content_index.current.json"

SITE_PAGES = {
    "about.html",
    "contact.html",
    "disclosure.html",
    "privacy.html",
    "terms.html",
}

ARCHIVED_INTERNAL_PAGES = {
    "news-preview.html",
}

HOMEPAGE_CARD_CATEGORY_MAP = {
    "start.html": "Progression",
    "early-game-optimization.html": "Progression",
    "base-building-order.html": "Progression",
    "shooter-stages.html": "Progression",
    "hq.html": "Progression",
    "hq-construction-cost.html": "Progression",
    "emergency-hospital-cost.html": "Progression",
    "research.html": "Research",
    "field-research.html": "Research",
    "alliance-recognition-cost.html": "Research",
    "heroes.html": "Heroes",
    "heroes-es.html": "Heroes",
    "queenie.html": "Heroes",
    "yu-chan.html": "Heroes",
    "gear.html": "Equipment",
    "formations.html": "Strategy",
    "formation-power.html": "Strategy",
    "pvp.html": "PvP",
    "trap.html": "PvP",
    "alliance-duel.html": "Events",
    "alliance-duel-rewards.html": "Events",
    "events.html": "Events",
    "daily.html": "Routine",
    "svs.html": "PvP",
    "canyon-clash.html": "Events",
    "zombie-siege.html": "Events",
    "tyrant.html": "Events",
    "furylord.html": "Events",
    "lucky-discounter.html": "Events",
    "gacha-go.html": "Events",
    "codes.html": "Economy",
    "resources.html": "Economy",
    "steel.html": "Economy",
    "farm-account.html": "Economy",
    "f2p.html": "Economy",
    "refugees.html": "Economy",
    "vehicle-modification-cost.html": "Equipment",
    "power-guide.html": "Progression",
    "leveling.html": "Progression",
    "tips.html": "Strategy",
    "tech.html": "Research",
}

ARCHETYPE_OVERRIDES = {
    "index.html": "home-hub",
    "about.html": "site-page",
    "contact.html": "site-page",
    "disclosure.html": "site-page",
    "privacy.html": "site-page",
    "terms.html": "site-page",
    "research-costs.html": "atlas-page",
    "news-preview.html": "news-digest",
    "heroes-es.html": "cornerstone-guide",
    "codes.html": "cornerstone-guide",
    "research.html": "cornerstone-guide",
    "tech.html": "cornerstone-guide",
    "heroes.html": "cornerstone-guide",
    "events.html": "cornerstone-guide",
    "f2p.html": "cornerstone-guide",
    "resources.html": "cornerstone-guide",
    "daily.html": "cornerstone-guide",
    "power-guide.html": "cornerstone-guide",
    "hq.html": "cornerstone-guide",
}


def list_html_pages() -> list[Path]:
    return sorted(path for path in ROOT.glob("*.html") if path.is_file())


def page_url(filename: str) -> str:
    return "/" if filename == "index.html" else f"/{filename}"


def guess_cluster(filename: str) -> str:
    if filename == "index.html":
        return "Home"
    if filename in SITE_PAGES:
        return "Site"
    if filename in ARCHIVED_INTERNAL_PAGES:
        return "News"
    return HOMEPAGE_CARD_CATEGORY_MAP.get(filename, "Guides")


def guess_archetype(filename: str) -> str:
    if filename in ARCHETYPE_OVERRIDES:
        return ARCHETYPE_OVERRIDES[filename]
    if filename.endswith("-cost.html") or filename in {
        "field-research.html",
        "alliance-recognition-cost.html",
        "vehicle-modification-cost.html",
    }:
        return "cost-page"
    return "support-guide"


def load_memory() -> dict:
    return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))


def build_current_inventory() -> dict:
    pages = []
    for path in list_html_pages():
        filename = path.name
        pages.append(
            {
                "filename": filename,
                "url": page_url(filename),
                "cluster": guess_cluster(filename),
                "archetype": guess_archetype(filename),
            }
        )
    return {
        "generated_at": "current",
        "notes": "Auto-derived current repo inventory. This file is safe to regenerate.",
        "pages": pages,
    }


def compare(memory: dict, current: dict) -> tuple[list[str], list[str], list[str]]:
    memory_pages = {page["filename"] for page in memory.get("pages", [])}
    current_pages = {page["filename"] for page in current.get("pages", [])}

    missing_in_memory = sorted(current_pages - memory_pages)
    stale_in_memory = sorted(memory_pages - current_pages)

    incomplete_entries = []
    for page in memory.get("pages", []):
        missing_fields = [
            field
            for field in ("filename", "url", "cluster", "archetype", "status", "freshness_priority")
            if not page.get(field)
        ]
        if missing_fields:
            incomplete_entries.append(f"{page.get('filename', '<missing filename>')}: {', '.join(missing_fields)}")

    return missing_in_memory, stale_in_memory, incomplete_entries


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and compare the current repo inventory against content_index memory.")
    parser.add_argument(
        "--write-current",
        action="store_true",
        help="Write automation/memory/content_index.current.json with the auto-derived current inventory.",
    )
    args = parser.parse_args()

    memory = load_memory()
    current = build_current_inventory()

    if args.write_current:
        write_json(CURRENT_PATH, current)
        print(f"Wrote {CURRENT_PATH.relative_to(ROOT)}")

    missing_in_memory, stale_in_memory, incomplete_entries = compare(memory, current)

    if missing_in_memory:
        print("Missing from memory:")
        for filename in missing_in_memory:
            print(f"  - {filename}")

    if stale_in_memory:
        print("Stale in memory:")
        for filename in stale_in_memory:
            print(f"  - {filename}")

    if incomplete_entries:
        print("Incomplete memory entries:")
        for row in incomplete_entries:
            print(f"  - {row}")

    if not any([missing_in_memory, stale_in_memory, incomplete_entries]):
        print("Content index memory check passed.")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
