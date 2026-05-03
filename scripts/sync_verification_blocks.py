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

RESEARCH_BRANCH_PAGES = {
    "army-building-cost.html",
    "field-research.html",
    "fully-armed-alliance-cost.html",
    "hero-training-cost.html",
    "military-strategies-cost.html",
    "peace-shield-cost.html",
    "siege-to-seize-cost.html",
    "unit-special-training-cost.html",
}

STATIC_DATA_PAGES = {
    "alliance-duel-rewards.html",
    "alliance-recognition-cost.html",
    "emergency-hospital-cost.html",
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

RESEARCH_BRANCH_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Branch totals were checked against the generated research data source, in-game value checks, and cumulative badge calculations.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> badge costs, unlock requirements, node names, and branch prerequisites can change after research updates.</li>
            </ul>
        </section>

"""

STATIC_DATA_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Tables and totals were checked against in-game values, visible requirements, and practical planning use cases.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> costs, rewards, shop values, and event thresholds can change after updates or by server group.</li>
            </ul>
        </section>

"""

RESEARCH_BRANCH_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this page as planning data before spending badges or saved resources, and confirm final values in-game before committing rare materials.</p>
        </section>
"""

STATIC_DATA_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this page for planning, then confirm the current in-game value before spending badges, diamonds, speedups, or rare event items.</p>
        </section>
"""


def verification_block_for(page_name: str) -> str:
    if page_name in RESEARCH_BRANCH_PAGES:
        return RESEARCH_BRANCH_BLOCK
    if page_name in STATIC_DATA_PAGES:
        return STATIC_DATA_BLOCK
    return FULL_BLOCK


def disclaimer_for(page_name: str) -> str | None:
    if page_name in RESEARCH_BRANCH_PAGES:
        return RESEARCH_BRANCH_DISCLAIMER
    if page_name in STATIC_DATA_PAGES:
        return STATIC_DATA_DISCLAIMER
    return None


def sync_page(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    block = verification_block_for(path.name)
    disclaimer = disclaimer_for(path.name)

    verification_pattern = re.compile(
        r'\s*<section class="verification-note" aria-label="Verification and review">.*?</section>\s*',
        re.S,
    )
    disclaimer_pattern = re.compile(r'(<section class="disclaimer">)', re.S)
    full_disclaimer_pattern = re.compile(
        r'\s*<section class="disclaimer">.*?</section>',
        re.S,
    )

    if verification_pattern.search(text):
        text = verification_pattern.sub("\n" + block, text, count=1)
    elif disclaimer_pattern.search(text):
        text = disclaimer_pattern.sub("\n" + block + r"\1", text, count=1)

    if disclaimer and full_disclaimer_pattern.search(text):
        text = full_disclaimer_pattern.sub("\n" + disclaimer, text, count=1)
        text = text.replace(
            '\n<section class="related-guides">',
            '\n\n        <section class="related-guides">',
        )
    else:
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
