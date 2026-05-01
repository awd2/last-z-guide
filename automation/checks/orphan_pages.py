#!/usr/bin/env python3
"""Report weakly linked pages and cluster-link gaps."""

from __future__ import annotations

import json
import sys
import argparse
from collections import defaultdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent.parent
MEMORY_PATH = ROOT / "automation" / "memory" / "content_index.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.site_utils import load_all_pages

EXCLUDED_CLUSTERS = {"Home", "Site", "News"}
EXCLUDED_STATUSES = {"archived-noindex", "draft-noindex"}


def load_memory_pages() -> dict[str, dict]:
    payload = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    return {page["filename"]: page for page in payload["pages"]}


def build_inlink_maps(filenames: Iterable[str]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    filename_set = set(filenames)
    inbound: dict[str, set[str]] = defaultdict(set)
    cluster_inbound: dict[str, set[str]] = defaultdict(set)

    memory_pages = load_memory_pages()
    page_cluster = {filename: meta["cluster"] for filename, meta in memory_pages.items()}

    for page in load_all_pages():
        source = page.filename
        for href in page.internal_links:
            if href not in filename_set:
                continue
            inbound[href].add(source)
            if page_cluster.get(source) == page_cluster.get(href):
                cluster_inbound[href].add(source)

    return inbound, cluster_inbound


def classify_pages() -> tuple[list[dict], list[dict], list[dict]]:
    memory_pages = load_memory_pages()
    candidates = []

    for filename, meta in memory_pages.items():
        if meta.get("cluster") in EXCLUDED_CLUSTERS:
            continue
        if meta.get("status") in EXCLUDED_STATUSES:
            continue
        candidates.append(meta)

    cluster_sizes: dict[str, int] = defaultdict(int)
    for meta in candidates:
        cluster_sizes[meta["cluster"]] += 1

    inbound, cluster_inbound = build_inlink_maps(page["filename"] for page in candidates)

    orphaned = []
    weak_cluster = []
    healthy = []

    for meta in sorted(candidates, key=lambda item: (item["cluster"], item["filename"])):
        filename = meta["filename"]
        total_inlinks = len(inbound.get(filename, set()))
        same_cluster_inlinks = len(cluster_inbound.get(filename, set()))
        record = {
            "filename": filename,
            "cluster": meta["cluster"],
            "archetype": meta["archetype"],
            "total_inlinks": total_inlinks,
            "same_cluster_inlinks": same_cluster_inlinks,
        }

        if total_inlinks == 0:
            orphaned.append(record)
        elif (
            meta["archetype"] != "cornerstone-guide"
            and cluster_sizes[meta["cluster"]] > 1
            and same_cluster_inlinks == 0
        ):
            weak_cluster.append(record)
        else:
            healthy.append(record)

    return orphaned, weak_cluster, healthy


def print_records(title: str, rows: list[dict]) -> None:
    if not rows:
        return
    print(title)
    for row in rows:
        print(
            f"  - {row['filename']} "
            f"[cluster={row['cluster']}, archetype={row['archetype']}, "
            f"inlinks={row['total_inlinks']}, same_cluster={row['same_cluster_inlinks']}]"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Report orphan pages and weak same-cluster support.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on weak same-cluster support in addition to true orphan pages.",
    )
    args = parser.parse_args()

    orphaned, weak_cluster, healthy = classify_pages()

    print_records("Pages with zero internal inlinks:", orphaned)
    print_records("Pages with weak same-cluster support:", weak_cluster)

    print(
        f"Checked {len(orphaned) + len(weak_cluster) + len(healthy)} pages: "
        f"{len(healthy)} healthy, {len(weak_cluster)} weak-cluster, {len(orphaned)} orphaned."
    )

    if orphaned:
        return 1

    if weak_cluster and args.strict:
        return 1

    if weak_cluster:
        print("Orphan page baseline passed with warnings. Re-run with --strict to fail on weak same-cluster support.")
    else:
        print("Orphan page check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
