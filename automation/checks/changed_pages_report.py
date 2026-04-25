#!/usr/bin/env python3
"""Build a compact report for changed or target pages."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_content_index, load_run_manifest
from scripts.site_utils import load_all_pages, load_search_index


HUB_EXPECTATIONS = {
    "Research": ["index.html", "research.html", "research-costs.html"],
    "Economy": ["index.html", "codes.html"],
    "Events": ["index.html", "events.html"],
    "PvP": ["index.html", "pvp.html"],
    "Progression": ["index.html", "start.html"],
    "Heroes": ["index.html", "heroes.html"],
}


def manifest_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or path.suffix == ".json":
        return path if path.is_absolute() else ROOT / path
    return ROOT / "automation" / "manifests" / f"{value}.json"


def inbound_map() -> dict[str, set[str]]:
    inbound: dict[str, set[str]] = defaultdict(set)
    for page in load_all_pages():
        for href in page.internal_links:
            if href.endswith(".html"):
                inbound[href].add(page.filename)
    return inbound


def page_lookup() -> dict[str, dict]:
    return {page.filename: asdict(page) for page in load_content_index()}


def search_index_pages() -> set[str]:
    pages = set()
    for entry in load_search_index():
        url = entry.get("url", "")
        if url == "/":
            pages.add("index.html")
        elif url.endswith(".html") and not url.startswith("http"):
            pages.add(Path(url).name)
        elif url.startswith("/"):
            pages.add(url.lstrip("/"))
    return pages


def resolve_targets(files: list[str], manifest_name: str | None) -> list[str]:
    targets: set[str] = set()
    if files:
        for name in files:
            targets.add(Path(name).name)
    if manifest_name:
        manifest = load_run_manifest(manifest_path(manifest_name))
        targets.update(Path(path).name for path in manifest.changed_files if path.endswith(".html"))
        plan = manifest.plan or {}
        target = plan.get("target_page_or_slug")
        if isinstance(target, str) and target.endswith(".html"):
            targets.add(Path(target).name)
        for page in plan.get("related_pages", []):
            if isinstance(page, str) and page.endswith(".html"):
                targets.add(Path(page).name)
        review_context = (manifest.artifacts or {}).get("review_context", {})
        for page in review_context.get("related_filenames", []):
            if isinstance(page, str) and page.endswith(".html"):
                targets.add(Path(page).name)
    return sorted(targets)


def main() -> int:
    parser = argparse.ArgumentParser(description="Report cluster/index/link context for changed pages.")
    parser.add_argument("--manifest", help="Manifest basename or path.")
    parser.add_argument("files", nargs="*", help="HTML filenames to report.")
    args = parser.parse_args()

    targets = resolve_targets(args.files, args.manifest)
    if not targets:
        print("No target pages resolved. Provide HTML files or --manifest.")
        return 1

    index_pages = search_index_pages()
    pages = {page.filename: page for page in load_all_pages()}
    memory = page_lookup()
    inbound = inbound_map()

    print("Changed Pages Report")
    for filename in targets:
        memory_row = memory.get(filename)
        if not memory_row:
            print(f"\n- {filename}")
            print("  missing from content_index memory")
            continue

        cluster = memory_row["cluster"]
        archetype = memory_row["archetype"]
        inlinks = sorted(inbound.get(filename, set()))
        same_cluster_inlinks = sorted(
            source
            for source in inlinks
            if memory.get(source, {}).get("cluster") == cluster
        )
        expected_hubs = HUB_EXPECTATIONS.get(cluster, ["index.html"])
        linked_from_hubs = [hub for hub in expected_hubs if hub in inlinks]

        in_repo = filename in pages
        in_search_index = filename in index_pages
        in_sitemap = in_repo and not pages[filename].noindex

        print(f"\n- {filename}")
        print(f"  cluster: {cluster}")
        print(f"  archetype: {archetype}")
        print(f"  in repo: {'yes' if in_repo else 'no'}")
        print(f"  in sitemap candidate: {'yes' if in_sitemap else 'no'}")
        print(f"  in search-index: {'yes' if in_search_index else 'no'}")
        print(f"  inbound links: {len(inlinks)}")
        print(f"  same-cluster inbound links: {len(same_cluster_inlinks)}")
        print(f"  expected hubs: {', '.join(expected_hubs)}")
        print(f"  linked from hubs: {', '.join(linked_from_hubs) if linked_from_hubs else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
