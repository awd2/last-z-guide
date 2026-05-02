#!/usr/bin/env python3
"""Audit public pages for generic, mass-produced, or low-utility writing signals."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent.parent
MEMORY_PATH = ROOT / "automation" / "memory" / "content_index.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.site_utils import load_page, strip_tags


PUBLIC_ARCHETYPES = {
    "home-hub",
    "cornerstone-guide",
    "support-guide",
    "event-guide",
    "hero-profile",
    "comparison-guide",
    "atlas-page",
    "cost-page",
}
EXCLUDED_STATUSES = {"archived-noindex", "draft-noindex"}
BOILERPLATE_STARTS = {
    "last reviewed for the current",
    "this guide was last validated",
    "source pattern in-game data tested",
    "source pattern in-game values tested",
    "game mechanics and numbers may",
    "verification review how this guide",
}
GENERIC_PHRASES = {
    "as much as possible",
    "at the end of the day",
    "best possible",
    "comprehensive guide",
    "crucial role",
    "delve",
    "designed to help",
    "dive into",
    "ensure that",
    "game changer",
    "in order to",
    "in this guide",
    "important to note",
    "important to understand",
    "keep in mind",
    "leverage",
    "maximize your",
    "not only",
    "but also",
    "overall",
    "plays a crucial role",
    "provide a",
    "robust",
    "seamless",
    "take your",
    "to the next level",
    "ultimate guide",
    "unlock the full potential",
    "various",
    "when it comes to",
    "whether you are",
    "whether you're",
}
VAGUE_VALUE_WORDS = {
    "better",
    "best",
    "efficient",
    "focus",
    "growth",
    "important",
    "maximize",
    "optimize",
    "priority",
    "strong",
    "usually",
    "value",
}


@dataclass(slots=True)
class PageVoiceRecord:
    filename: str
    cluster: str
    archetype: str
    h1: str
    word_count: int
    avg_sentence_words: float
    long_sentences: int
    numbers: int
    internal_links: int
    tables: int
    list_items: int
    generic_phrase_hits: dict[str, int]
    repeated_boilerplate_hits: list[str]
    specificity_score: float
    generic_score: float
    risk_score: float
    risk_level: str
    recommendations: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "filename": self.filename,
            "cluster": self.cluster,
            "archetype": self.archetype,
            "h1": self.h1,
            "word_count": self.word_count,
            "avg_sentence_words": round(self.avg_sentence_words, 1),
            "long_sentences": self.long_sentences,
            "numbers": self.numbers,
            "internal_links": self.internal_links,
            "tables": self.tables,
            "list_items": self.list_items,
            "generic_phrase_hits": self.generic_phrase_hits,
            "repeated_boilerplate_hits": self.repeated_boilerplate_hits,
            "specificity_score": round(self.specificity_score, 1),
            "generic_score": round(self.generic_score, 1),
            "risk_score": round(self.risk_score, 1),
            "risk_level": self.risk_level,
            "recommendations": self.recommendations,
        }


def load_memory_pages() -> list[dict[str, Any]]:
    payload = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    return list(payload.get("pages", []))


def public_memory_pages() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for record in load_memory_pages():
        if record.get("status") in EXCLUDED_STATUSES:
            continue
        if record.get("archetype") not in PUBLIC_ARCHETYPES:
            continue
        path = ROOT / str(record.get("filename", ""))
        if not path.exists() or not path.is_file():
            continue
        page = load_page(path)
        if page.noindex:
            continue
        records.append(record)
    return records


def main_html(raw_html: str) -> str:
    match = re.search(r"<main\b[^>]*>(.*?)</main>", raw_html, flags=re.I | re.S)
    if match:
        return match.group(1)
    body = re.search(r"<body\b[^>]*>(.*?)</body>", raw_html, flags=re.I | re.S)
    return body.group(1) if body else raw_html


def visible_main_text(raw_html: str) -> str:
    html = main_html(raw_html)
    html = re.sub(
        r"<script\b.*?</script>|<style\b.*?</style>|<nav\b.*?</nav>|<footer\b.*?</footer>|<header\b.*?</header>",
        " ",
        html,
        flags=re.I | re.S,
    )
    return strip_tags(html)


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z0-9'/-]*", text.lower())


def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if len(part.strip()) > 20]


def count_numbers(text: str) -> int:
    return len(
        re.findall(
            r"\b\d+(?:[.,]\d+)?\s*(?:%|M|K|k|m|days?|hours?|h|badges?|diamonds?|levels?|HQ\s*\d+)?\b",
            text,
            flags=re.I,
        )
    )


def repeated_sentence_starts(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for sentence in sentences(text):
        seed = words(sentence)[:5]
        if len(seed) >= 4:
            counts[" ".join(seed)] += 1
    return counts


def phrase_hits(text: str) -> dict[str, int]:
    lower = text.lower()
    hits = {phrase: lower.count(phrase) for phrase in sorted(GENERIC_PHRASES) if lower.count(phrase)}
    return hits


def boilerplate_hits(text: str, sitewide_starts: Counter[str]) -> list[str]:
    page_starts = repeated_sentence_starts(text)
    hits: list[str] = []
    for start in BOILERPLATE_STARTS:
        if page_starts.get(start, 0) or sitewide_starts.get(start, 0) >= 20 and start in text.lower():
            hits.append(start)
    return hits


def score_page(record: dict[str, Any], sitewide_starts: Counter[str]) -> PageVoiceRecord:
    page = load_page(ROOT / record["filename"])
    raw_main = main_html(page.text)
    visible = visible_main_text(page.text)
    page_words = words(visible)
    page_sentences = sentences(visible)
    avg_sentence_words = (
        sum(len(words(sentence)) for sentence in page_sentences) / len(page_sentences)
        if page_sentences
        else 0.0
    )
    long_sentences = sum(1 for sentence in page_sentences if len(words(sentence)) > 28)
    internal_links = len(re.findall(r'<a\b[^>]*href="[^#][^"]+"', raw_main, flags=re.I))
    tables = len(re.findall(r"<table\b", raw_main, flags=re.I))
    list_items = len(re.findall(r"<li\b", raw_main, flags=re.I))
    numbers = count_numbers(visible)
    hits = phrase_hits(visible)
    repeated = boilerplate_hits(visible, sitewide_starts)
    vague_word_count = sum(1 for word in page_words if word in VAGUE_VALUE_WORDS)
    word_units = max(len(page_words) / 100, 1)

    specificity_score = (numbers * 2 + internal_links + tables * 4 + min(list_items, 30) * 0.4) / word_units
    generic_score = (
        sum(hits.values()) * 1.8
        + long_sentences * 0.8
        + max(0.0, avg_sentence_words - 20) * 0.25
        + vague_word_count / word_units * 0.15
        + len(repeated) * 2.0
    )
    risk_score = generic_score - specificity_score * 0.45

    if risk_score >= 12:
        risk_level = "high"
    elif len(repeated) >= 3 or risk_score >= 6 or sum(hits.values()) >= 4 or avg_sentence_words > 28:
        risk_level = "medium"
    else:
        risk_level = "low"

    recommendations: list[str] = []
    if repeated:
        recommendations.append("Replace repeated trust/review boilerplate with page-specific verification context.")
    if sum(hits.values()) >= 2:
        recommendations.append("Replace generic guide language with concrete player decisions, examples, or constraints.")
    if avg_sentence_words > 24 or long_sentences >= 8:
        recommendations.append("Shorten long smooth paragraphs into sharper human-readable rules or checklists.")
    if specificity_score < 6 and len(page_words) > 300:
        recommendations.append("Add exact utility: thresholds, UI path, timing, cost, exception, or stop/go rule.")
    if not recommendations:
        recommendations.append("No immediate voice action; preserve current utility and page role.")

    return PageVoiceRecord(
        filename=record["filename"],
        cluster=str(record.get("cluster", "")),
        archetype=str(record.get("archetype", "")),
        h1=page.h1,
        word_count=len(page_words),
        avg_sentence_words=avg_sentence_words,
        long_sentences=long_sentences,
        numbers=numbers,
        internal_links=internal_links,
        tables=tables,
        list_items=list_items,
        generic_phrase_hits=hits,
        repeated_boilerplate_hits=repeated,
        specificity_score=specificity_score,
        generic_score=generic_score,
        risk_score=risk_score,
        risk_level=risk_level,
        recommendations=recommendations,
    )


def build_report() -> dict[str, Any]:
    records = public_memory_pages()
    text_by_page = {
        record["filename"]: visible_main_text(load_page(ROOT / record["filename"]).text)
        for record in records
    }
    sitewide_starts: Counter[str] = Counter()
    start_pages: defaultdict[str, set[str]] = defaultdict(set)
    for filename, text in text_by_page.items():
        for start, count in repeated_sentence_starts(text).items():
            sitewide_starts[start] += count
            start_pages[start].add(filename)

    page_records = [score_page(record, sitewide_starts) for record in records]
    page_records.sort(key=lambda item: item.risk_score, reverse=True)
    risk_counts = Counter(record.risk_level for record in page_records)
    repeated_sitewide = [
        {
            "sentence_start": start,
            "count": count,
            "pages": sorted(start_pages[start])[:12],
        }
        for start, count in sitewide_starts.most_common(30)
        if count >= 4
    ]
    return {
        "report_type": "content_voice_audit",
        "public_pages_checked": len(page_records),
        "risk_counts": dict(sorted(risk_counts.items())),
        "summary": {
            "high_risk_pages": risk_counts.get("high", 0),
            "medium_risk_pages": risk_counts.get("medium", 0),
            "low_risk_pages": risk_counts.get("low", 0),
            "audit_policy": "No-write planning audit. Findings are prompts for human review, not automatic approval to edit content.",
        },
        "pages": [record.as_dict() for record in page_records],
        "repeated_sentence_starts": repeated_sitewide,
    }


def print_report(report: dict[str, Any], top: int) -> None:
    summary = report["summary"]
    print("Content Voice Audit")
    print(f"- public pages checked: {report['public_pages_checked']}")
    print(
        "- risk counts: "
        f"high={summary['high_risk_pages']}, "
        f"medium={summary['medium_risk_pages']}, "
        f"low={summary['low_risk_pages']}"
    )
    print("- policy: no-write planning audit; human approval is required before content edits")
    print(f"\nTop {top} voice opportunities")
    for page in report["pages"][:top]:
        phrases = ", ".join(page["generic_phrase_hits"].keys()) or "none"
        boilerplate = ", ".join(page["repeated_boilerplate_hits"]) or "none"
        print(
            f"- {page['filename']} | risk={page['risk_level']} "
            f"| score={page['risk_score']} | spec={page['specificity_score']} "
            f"| generic={page['generic_score']}"
        )
        print(f"  phrases: {phrases}")
        print(f"  repeated: {boilerplate}")
        print(f"  next: {page['recommendations'][0]}")

    repeated = report["repeated_sentence_starts"][:8]
    if repeated:
        print("\nRepeated sitewide sentence starts")
        for item in repeated:
            print(f"- {item['count']}x `{item['sentence_start']}`")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit public pages for generic or low-utility writing signals.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--top", type=int, default=12, help="Number of top opportunities to print.")
    parser.add_argument(
        "--fail-on-high-risk",
        action="store_true",
        help="Return non-zero when high-risk voice findings exist. Not used by default automation checks.",
    )
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report, args.top)

    if args.fail_on_high_risk and report["summary"]["high_risk_pages"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
