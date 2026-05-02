#!/usr/bin/env python3
"""Check public content for high-risk guidance contradictions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent
MEMORY_PATH = ROOT / "automation" / "memory" / "content_index.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.site_utils import load_all_pages, strip_tags


PUBLIC_ARCHETYPES = {
    "cornerstone-guide",
    "support-guide",
    "event-guide",
    "hero-profile",
    "comparison-guide",
    "atlas-page",
    "cost-page",
}
EXCLUDED_STATUSES = {"archived-noindex", "draft-noindex"}

SAFE_SEASON_CONTEXT = ("older guide", "older guides", "outdated", "canceled", "cancelled", "skipped")
GIFT_CENTER_SAFE_CONTEXT = (
    "can i redeem codes inside the game",
    "can you redeem codes inside the game",
    "cannot redeem codes inside the game",
    "you cannot redeem codes inside the game",
    "official gift center",
)

OWNER_APPROVED_AR_PAGES = {"formation-power.html", "tips.html"}
OWNER_APPROVED_RAW_POWER_PAGES = {"formation-power.html"}
OWNER_APPROVED_FORMATION_PAGES = {"formations.html"}
OWNER_APPROVED_SEASON_PRIORITY_PAGES = {"heroes.html", "heroes-es.html", "pvp.html"}


@dataclass(slots=True)
class Finding:
    page: str
    rule: str
    severity: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "page": self.page,
            "rule": self.rule,
            "severity": self.severity,
            "message": self.message,
        }


def load_memory_pages() -> dict[str, dict]:
    payload = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    return {page["filename"]: page for page in payload["pages"]}


def public_pages(memory: dict[str, dict]) -> list[tuple[str, str]]:
    pages: list[tuple[str, str]] = []
    for page in load_all_pages():
        meta = memory.get(page.filename)
        if not meta:
            continue
        if meta.get("status") in EXCLUDED_STATUSES:
            continue
        if meta.get("archetype") not in PUBLIC_ARCHETYPES:
            continue
        if page.noindex:
            continue
        pages.append((page.filename, page.text))
    return pages


def plain_text(raw_html: str) -> str:
    return strip_tags(raw_html).casefold()


def has_safe_context(text: str, needle_match: re.Match[str], safe_terms: tuple[str, ...]) -> bool:
    start = max(0, needle_match.start() - 220)
    end = min(len(text), needle_match.end() + 220)
    window = text[start:end].casefold()
    return any(term in window for term in safe_terms)


def add(
    findings: list[Finding],
    page: str,
    rule: str,
    severity: str,
    message: str,
) -> None:
    if any(
        finding.page == page
        and finding.rule == rule
        and finding.severity == severity
        and finding.message == message
        for finding in findings
    ):
        return
    findings.append(Finding(page=page, rule=rule, severity=severity, message=message))


def check_season_naming(page: str, text: str, findings: list[Finding]) -> None:
    for match in re.finditer(r"\bSeason\s*2\s*(?:=|is)\s*Desert\b", text, flags=re.I):
        if has_safe_context(text, match, SAFE_SEASON_CONTEXT):
            continue
        add(
            findings,
            page,
            "season_desert_unqualified",
            "failure",
            "Unqualified `Season 2 = Desert` wording needs old-guide/canceled/skipped context.",
        )


def check_gift_center_flow(page: str, visible: str, findings: list[Finding]) -> None:
    risky = (
        "redeem codes inside the game",
        "redeem code inside the game",
        "in-game redeem",
        "ingame redeem",
    )
    for phrase in risky:
        if phrase not in visible:
            continue
        if any(safe in visible for safe in GIFT_CENTER_SAFE_CONTEXT):
            continue
        add(
            findings,
            page,
            "gift_center_wrong_flow",
            "failure",
            "Gift Center flow may imply in-game code redemption instead of official Gift Center redemption.",
        )


def check_ust_name(page: str, text: str, findings: list[Finding]) -> None:
    if re.search(r"\bSpecial Unit Training\b", text):
        add(
            findings,
            page,
            "wrong_ust_name",
            "failure",
            "Use canonical `Unit Special Training`, including `UST (Unit Special Training)` when expanding UST.",
        )


def check_reddit_news_exposure(page: str, text: str, visible: str, findings: list[Finding]) -> None:
    if "news-preview.html" in text or "reddit digest" in visible or "reddit-lastz-digest" in text:
        add(
            findings,
            page,
            "reddit_news_public_exposure",
            "failure",
            "Archived Reddit/news experiment is exposed from public indexable content.",
        )


def check_shield_priority(page: str, visible: str, findings: list[Finding]) -> None:
    risky_patterns = [
        r"buy shields directly with diamonds first",
        r"diamond shields are better than alliance shop",
        r"direct diamond shield(?:s)? (?:is|are) better",
    ]
    for pattern in risky_patterns:
        if re.search(pattern, visible):
            add(
                findings,
                page,
                "diamond_shield_wrong_priority",
                "failure",
                "Shield economy contradicts Alliance Shop shield preference when stock exists.",
            )


def check_alliance_recognition(page: str, text: str, visible: str, findings: list[Finding]) -> None:
    patterns = [
        r"Alliance Recognition\s+FIRST",
        r"before any badge research",
        r"before any other badge research",
        r"Do NOT start any badge-consuming research until Alliance Recognition is maxed",
        r"Ignore other research trees.*until you(?:'|’)ve maxed Alliance Recognition",
        r"Alliance Recognition\s+must be maxed first",
    ]
    for pattern in patterns:
        if not re.search(pattern, text, flags=re.I | re.S):
            continue
        if page in OWNER_APPROVED_AR_PAGES:
            add(
                findings,
                page,
                "alliance_recognition_absolute_first",
                "allowed",
                "Owner-approved strong Alliance Recognition wording on this page.",
            )
        elif page == "tech.html" and "should you do alliance recognition first" in visible:
            add(
                findings,
                page,
                "alliance_recognition_absolute_first",
                "allowed",
                "Allowed question-heading context; page argues the nuance below the heading.",
            )
        else:
            add(
                findings,
                page,
                "alliance_recognition_absolute_first",
                "warning",
                "Absolute Alliance Recognition-first wording appears outside owner-approved pages.",
            )


def check_raw_formation_power(page: str, text: str, findings: list[Finding]) -> None:
    patterns = [
        r"Absolutely YES",
        r"5 same-faction heroes activates massive bonuses",
        r"40M\+ power",
        r"Removing 1 hero can drop power from 72M to 31M",
    ]
    for pattern in patterns:
        if not re.search(pattern, text, flags=re.I):
            continue
        if page in OWNER_APPROVED_RAW_POWER_PAGES:
            add(
                findings,
                page,
                "raw_formation_absolute_claim",
                "allowed",
                "Owner-approved raw formation power wording on this page.",
            )
        else:
            add(
                findings,
                page,
                "raw_formation_absolute_claim",
                "warning",
                "Raw formation power claim appears outside owner-approved formation-power context.",
            )


def check_single_best_formation(page: str, text: str, findings: list[Finding]) -> None:
    patterns = [
        r"best formation is 3 Wings of Dawn \+ 2 Blood Rose",
        r"By focusing on Wings of Dawn, you automatically counter the majority of opponents",
    ]
    for pattern in patterns:
        if not re.search(pattern, text, flags=re.I):
            continue
        if page in OWNER_APPROVED_FORMATION_PAGES:
            add(
                findings,
                page,
                "single_best_formation_absolute",
                "allowed",
                "Owner-approved strong formation wording on this page.",
            )
        else:
            add(
                findings,
                page,
                "single_best_formation_absolute",
                "warning",
                "Single best formation wording appears outside owner-approved formations context.",
            )


def check_old_season_priority(page: str, text: str, findings: list[Finding]) -> None:
    if not re.search(r"\bS3\s*>\s*S2\s*>\s*S1\b", text):
        return
    if page in OWNER_APPROVED_SEASON_PRIORITY_PAGES:
        add(
            findings,
            page,
            "old_season_priority",
            "allowed",
            "Owner-approved season priority shorthand on this page.",
        )
    else:
        add(
            findings,
            page,
            "old_season_priority",
            "warning",
            "Old season priority shorthand appears outside approved hero/PvP context.",
        )


def check_pages(pages: list[tuple[str, str]]) -> tuple[list[Finding], list[Finding], list[Finding]]:
    findings: list[Finding] = []
    for page, text in pages:
        visible = plain_text(text)
        check_season_naming(page, text, findings)
        check_gift_center_flow(page, visible, findings)
        check_ust_name(page, text, findings)
        check_reddit_news_exposure(page, text, visible, findings)
        check_shield_priority(page, visible, findings)
        check_alliance_recognition(page, text, visible, findings)
        check_raw_formation_power(page, text, findings)
        check_single_best_formation(page, text, findings)
        check_old_season_priority(page, text, findings)

    failures = [finding for finding in findings if finding.severity == "failure"]
    warnings = [finding for finding in findings if finding.severity == "warning"]
    allowed = [finding for finding in findings if finding.severity == "allowed"]
    return failures, warnings, allowed


def print_findings(title: str, findings: list[Finding]) -> None:
    if not findings:
        return
    print(title)
    seen: set[tuple[str, str, str]] = set()
    for finding in findings:
        key = (finding.page, finding.rule, finding.message)
        if key in seen:
            continue
        seen.add(key)
        print(f"  - {finding.page} [{finding.rule}] {finding.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check public content for high-risk guidance contradictions.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings in addition to hard content-consistency failures.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    pages = public_pages(load_memory_pages())
    failures, warnings, allowed = check_pages(pages)

    if args.json:
        payload = {
            "public_pages_checked": len(pages),
            "failures": [finding.as_dict() for finding in failures],
            "warnings": [finding.as_dict() for finding in warnings],
            "allowed": [finding.as_dict() for finding in allowed],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print_findings("Content consistency failures:", failures)
        print_findings("Content consistency warnings:", warnings)
        print_findings("Content consistency allowed contexts:", allowed)
        print(
            f"Checked content consistency on {len(pages)} public pages: "
            f"{len(failures)} failure(s), {len(warnings)} warning(s), {len(allowed)} allowed context(s)."
        )
        if warnings and not args.strict:
            print("Content consistency baseline passed with warnings. Re-run with --strict to fail on them.")
        elif not failures and not warnings:
            print("Content consistency check passed.")

    if failures or (warnings and args.strict):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
