#!/usr/bin/env python3
"""Check required internal links for key site clusters."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.site_utils import load_all_pages


REQUIRED_LINKS: dict[str, list[str]] = {
    "research.html": [
        "research-costs.html",
        "hero-training-cost.html",
        "military-strategies-cost.html",
        "peace-shield-cost.html",
        "siege-to-seize-cost.html",
        "field-research.html",
    ],
    "research-costs.html": [
        "hero-training-cost.html",
        "military-strategies-cost.html",
        "peace-shield-cost.html",
        "siege-to-seize-cost.html",
        "field-research.html",
        "alliance-recognition-cost.html",
        "army-building-cost.html",
        "fully-armed-alliance-cost.html",
        "unit-special-training-cost.html",
    ],
    "codes.html": [
        "gift-center-uid.html",
        "redeem-code-not-working.html",
    ],
    "gift-center-uid.html": [
        "codes.html",
        "redeem-code-not-working.html",
    ],
    "redeem-code-not-working.html": [
        "codes.html",
        "gift-center-uid.html",
    ],
    "index.html": [
        "research-costs.html",
        "codes.html",
        "gift-center-uid.html",
    ],
}


def main() -> int:
    pages = {page.filename: page for page in load_all_pages()}
    failures: list[str] = []

    for source, targets in REQUIRED_LINKS.items():
        if source not in pages:
            failures.append(f"{source}: source page missing from repo")
            continue

        source_links = set(pages[source].internal_links)
        for target in targets:
            if target not in source_links:
                failures.append(f"{source} -> {target}")

    if failures:
        print("Missing required cluster links:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("Cluster link check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
