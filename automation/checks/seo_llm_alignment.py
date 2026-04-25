#!/usr/bin/env python3
"""Report basic SEO/LLM alignment issues and simple cannibalization risks."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
MEMORY_PATH = ROOT / "automation" / "memory" / "content_index.json"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.site_utils import load_all_pages, normalize_whitespace, strip_tags


TARGET_ARCHETYPES = {
    "cornerstone-guide",
    "support-guide",
    "atlas-page",
    "cost-page",
    "comparison-guide",
    "event-guide",
}
EXCLUDED_CLUSTERS = {"Home", "Site", "News"}
EXCLUDED_STATUSES = {"draft-noindex"}
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "best",
    "by",
    "for",
    "from",
    "guide",
    "how",
    "in",
    "is",
    "it",
    "last",
    "most",
    "of",
    "on",
    "or",
    "page",
    "path",
    "the",
    "this",
    "to",
    "what",
    "when",
    "why",
    "with",
    "z",
    "2026",
}


@dataclass(slots=True)
class WarningRecord:
    page: str
    kind: str
    details: str


def load_memory_pages() -> dict[str, dict]:
    payload = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    return {page["filename"]: page for page in payload["pages"]}


def normalize_for_similarity(text: str) -> str:
    return normalize_whitespace(text).casefold()


def similarity(left: str, right: str) -> float:
    return difflib.SequenceMatcher(None, normalize_for_similarity(left), normalize_for_similarity(right)).ratio()


def token_set(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9][a-z0-9+'/-]*", normalize_for_similarity(text)))
    return {token for token in tokens if len(token) > 2 and token not in STOPWORDS}


def overlap(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / min(len(left), len(right))


def extract_first_screen_text(raw_html: str) -> str:
    patterns = [
        r'<p class="guide-verified">(.*?)</p>',
        r'<p class="qa-lede">(.*?)</p>',
        r'<div class="qa-callout[^"]*">.*?<span class="qa-callout-text">(.*?)</span>',
        r'<main\b[^>]*>.*?<p\b[^>]*>(.*?)</p>',
    ]
    parts: list[str] = []
    for pattern in patterns:
        match = re.search(pattern, raw_html, flags=re.I | re.S)
        if match:
            parts.append(strip_tags(match.group(1)))
    return normalize_whitespace(" ".join(parts[:2]))


def alignment_warnings(memory_pages: dict[str, dict]) -> list[WarningRecord]:
    warnings: list[WarningRecord] = []

    for page in load_all_pages():
        meta = memory_pages.get(page.filename)
        if not meta:
            continue
        if meta.get("cluster") in EXCLUDED_CLUSTERS:
            continue
        if meta.get("status") in EXCLUDED_STATUSES:
            continue
        if meta.get("archetype") not in TARGET_ARCHETYPES:
            continue
        if page.noindex:
            continue

        first_screen = extract_first_screen_text(page.text)
        if not first_screen:
            warnings.append(
                WarningRecord(
                    page.filename,
                    "missing_first_screen_signal",
                    "No guide-verified, qa-lede, or early paragraph signal found.",
                )
            )
            continue

        title_tokens = token_set(page.title)
        h1_tokens = token_set(page.h1)
        meta_tokens = token_set(page.meta_description)
        first_tokens = token_set(first_screen)

        title_h1_overlap = overlap(title_tokens, h1_tokens)
        title_first_overlap = overlap(title_tokens | h1_tokens, first_tokens)
        meta_first_overlap = overlap(meta_tokens, first_tokens)

        if title_h1_overlap < 0.45 and similarity(page.title, page.h1) < 0.55:
            warnings.append(
                WarningRecord(
                    page.filename,
                    "title_h1_misalignment",
                    f"title/h1 overlap too low ({title_h1_overlap:.2f})",
                )
            )

        if title_first_overlap < 0.28:
            warnings.append(
                WarningRecord(
                    page.filename,
                    "first_screen_intent_mismatch",
                    f"title+h1 vs first-screen overlap too low ({title_first_overlap:.2f})",
                )
            )

        if meta_first_overlap < 0.20:
            warnings.append(
                WarningRecord(
                    page.filename,
                    "meta_first_screen_mismatch",
                    f"meta vs first-screen overlap too low ({meta_first_overlap:.2f})",
                )
            )

    return warnings


def cannibalization_warnings(memory_pages: dict[str, dict]) -> list[WarningRecord]:
    warnings: list[WarningRecord] = []
    loaded_pages = {page.filename: page for page in load_all_pages()}
    pages: list[tuple[dict, object]] = []

    for filename, meta in memory_pages.items():
        page = loaded_pages.get(filename)
        if not page:
            continue
        if meta.get("cluster") in EXCLUDED_CLUSTERS:
            continue
        if meta.get("status") in EXCLUDED_STATUSES:
            continue
        if meta.get("archetype") not in TARGET_ARCHETYPES:
            continue
        if page.noindex:
            continue
        pages.append((meta, page))

    for (left_meta, left_page), (right_meta, right_page) in combinations(pages, 2):
        if left_meta["cluster"] != right_meta["cluster"]:
            continue
        if left_meta["archetype"] != right_meta["archetype"]:
            continue

        title_overlap = overlap(token_set(left_page.title), token_set(right_page.title))
        h1_overlap = overlap(token_set(left_page.h1), token_set(right_page.h1))
        title_similarity = similarity(left_page.title, right_page.title)
        h1_similarity = similarity(left_page.h1, right_page.h1)

        if (
            title_overlap >= 0.75
            and h1_overlap >= 0.75
            and title_similarity >= 0.72
            and h1_similarity >= 0.72
        ):
            warnings.append(
                WarningRecord(
                    f"{left_page.filename} <-> {right_page.filename}",
                    "cannibalization_risk",
                    (
                        "Same-cluster pages have highly overlapping title/H1 language "
                        f"(title={title_overlap:.2f}, h1={h1_overlap:.2f})"
                    ),
                )
            )

    return warnings


def print_records(title: str, rows: list[WarningRecord]) -> None:
    if not rows:
        return
    print(title)
    for row in rows:
        print(f"  - {row.page} [{row.kind}] {row.details}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report title/H1/meta/first-screen misalignment and basic cannibalization risks."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings instead of reporting them as advisory output.",
    )
    args = parser.parse_args()

    memory_pages = load_memory_pages()
    align = alignment_warnings(memory_pages)
    cannibal = cannibalization_warnings(memory_pages)
    all_warnings = align + cannibal

    print_records("SEO/LLM alignment warnings:", align)
    print_records("Potential cannibalization warnings:", cannibal)
    print(
        f"Checked SEO/LLM alignment on {len(memory_pages)} memory pages: "
        f"{len(align)} alignment warning(s), {len(cannibal)} cannibalization warning(s)."
    )

    if all_warnings and args.strict:
        return 1

    if all_warnings:
        print("SEO/LLM alignment baseline passed with warnings. Re-run with --strict to fail on them.")
    else:
        print("SEO/LLM alignment check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
