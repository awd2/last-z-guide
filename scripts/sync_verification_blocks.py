#!/usr/bin/env python3
"""Insert or refresh verification blocks across content pages."""

from __future__ import annotations

import re
from pathlib import Path

from site_utils import ROOT, list_html_pages


EXCLUDED = {
    "index.html",
    "about.html",
    "contact.html",
    "privacy.html",
    "terms.html",
    "disclosure.html",
    "news-preview.html",
}

COMPACT_PAGES = {
    "alliance-duel-rewards.html",
    "alliance-recognition-cost.html",
    "emergency-hospital-cost.html",
    "field-research.html",
    "hq-construction-cost.html",
    "vehicle-modification-cost.html",
}

FULL_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>How this guide was verified:</strong> Based on in-game data, tested results, and cross-checks against community validation.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Source pattern:</strong> In-game data + tested results + community validation.</li>
            </ul>
        </section>

"""

COMPACT_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>How this data was reviewed:</strong> Based on in-game values, tested checks, and cross-checks against community validation.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Source pattern:</strong> In-game values + tested checks + community validation.</li>
            </ul>
        </section>

"""


def sync_page(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    block = COMPACT_BLOCK if path.name in COMPACT_PAGES else FULL_BLOCK

    verification_pattern = re.compile(
        r'\s*<section class="verification-note" aria-label="Verification and review">.*?</section>\s*',
        re.S,
    )
    disclaimer_pattern = re.compile(r'(<section class="disclaimer">)', re.S)

    if verification_pattern.search(text):
        text = verification_pattern.sub("\n" + block, text, count=1)
    elif disclaimer_pattern.search(text):
        text = disclaimer_pattern.sub("\n" + block + r"\1", text, count=1)

    text = re.sub(
        r'(This guide was last validated in )([A-Za-z]+ \d{4})(\.)',
        r"\1March 2026\3",
        text,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    updated = 0
    for path in list_html_pages():
        if path.name in EXCLUDED:
            continue
        if sync_page(path):
            updated += 1
    print(f"Updated verification blocks on {updated} HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
