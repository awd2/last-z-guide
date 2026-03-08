#!/usr/bin/env python3
"""Lightweight audit for static HTML pages."""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from dataclasses import dataclass

from site_utils import canonical_url, load_all_pages, normalize_whitespace, strip_tags


BROKEN_MARKERS = [
    "cite",
    "turn1reddit",
    "turn0search",
    "turn0fetch",
]


@dataclass
class Issue:
    severity: str
    page: str
    message: str


def normalized_title(text: str) -> str:
    return normalize_whitespace(text).casefold()


def similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def find_paragraph_duplicates(text: str) -> list[str]:
    paragraphs = [
        strip_tags(match)
        for match in re.findall(r"<p\b[^>]*>(.*?)</p>", text, flags=re.I | re.S)
    ]
    duplicates: list[str] = []
    for left, right in zip(paragraphs, paragraphs[1:]):
        if len(left) < 90 or len(right) < 90:
            continue
        ratio = similar(left.casefold(), right.casefold())
        if ratio >= 0.84:
            preview = left[:90].rstrip()
            duplicates.append(f"Possible duplicate paragraphs ({ratio:.2f}): {preview}...")
    return duplicates


def audit() -> list[Issue]:
    issues: list[Issue] = []
    for page in load_all_pages():
        expected_canonical = canonical_url(page.filename)

        if not page.title:
            issues.append(Issue("error", page.filename, "Missing <title>"))
        if not page.meta_description and not page.noindex:
            issues.append(Issue("error", page.filename, "Missing meta description"))
        if not page.h1:
            issues.append(Issue("error", page.filename, "Missing <h1>"))
        if not page.canonical and not page.noindex:
            issues.append(Issue("error", page.filename, "Missing canonical URL"))
        elif page.canonical and page.canonical != expected_canonical:
            issues.append(
                Issue(
                    "error",
                    page.filename,
                    f"Canonical mismatch: expected {expected_canonical}, found {page.canonical}",
                )
            )
        if not page.og_title and not page.noindex:
            issues.append(Issue("warn", page.filename, "Missing og:title"))
        if not page.twitter_title and not page.noindex:
            issues.append(Issue("warn", page.filename, "Missing twitter:title"))
        if "<a " in page.raw_title.lower():
            issues.append(Issue("error", page.filename, "Broken HTML inside <title>"))
        if page.og_title and similar(normalized_title(page.title), normalized_title(page.og_title)) < 0.45:
            issues.append(Issue("warn", page.filename, "Title and og:title look too far apart"))
        if page.twitter_title and similar(normalized_title(page.title), normalized_title(page.twitter_title)) < 0.45:
            issues.append(Issue("warn", page.filename, "Title and twitter:title look too far apart"))
        if not page.internal_links and page.filename not in {
            "index.html",
            "privacy.html",
            "terms.html",
            "disclosure.html",
            "contact.html",
            "about.html",
        } and not page.noindex:
            issues.append(Issue("warn", page.filename, "No internal .html links found"))

        for marker in BROKEN_MARKERS:
            if marker in page.text:
                issues.append(Issue("error", page.filename, f"Broken marker found: {marker}"))

        for duplicate in find_paragraph_duplicates(page.text):
            issues.append(Issue("warn", page.filename, duplicate))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit HTML pages for common issues.")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings too.")
    args = parser.parse_args()

    issues = audit()
    if not issues:
        print("Audit passed: no issues found.")
        return 0

    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity != "error"]

    for issue in issues:
        print(f"[{issue.severity.upper()}] {issue.page}: {issue.message}")

    print(
        f"\nSummary: {len(errors)} error(s), {len(warnings)} warning(s), {len(issues)} total issue(s)."
    )
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
