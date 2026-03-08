#!/usr/bin/env python3
"""Shared helpers for static-site audit and indexing scripts."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://lastzguides.com"
SITE_PAGES = {
    "about.html",
    "contact.html",
    "disclosure.html",
    "privacy.html",
    "terms.html",
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


@dataclass
class PageData:
    path: Path
    text: str
    raw_title: str
    title: str
    meta_description: str
    og_title: str
    twitter_title: str
    canonical: str
    h1: str
    internal_links: list[str]
    noindex: bool

    @property
    def filename(self) -> str:
        return self.path.name


def site_now_iso() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def list_html_pages() -> list[Path]:
    pages = sorted(ROOT.glob("*.html"))
    return [page for page in pages if page.is_file()]


def list_indexable_html_pages() -> list[Path]:
    pages: list[Path] = []
    for page in list_html_pages():
        text = page.read_text(encoding="utf-8")
        if re.search(
            r'<meta\s+name="robots"\s+content="[^"]*noindex',
            text,
            flags=re.I,
        ):
            continue
        pages.append(page)
    return pages


def page_url(filename: str) -> str:
    return "/" if filename == "index.html" else f"/{filename}"


def canonical_url(filename: str) -> str:
    return f"{BASE_URL}{page_url(filename)}"


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def strip_tags(text: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return normalize_whitespace(unescape(text))


def extract_first(pattern: str, text: str, flags: int = re.I | re.S) -> str:
    match = re.search(pattern, text, flags)
    if not match:
        return ""
    return normalize_whitespace(unescape(match.group(1)))


def load_page(path: Path) -> PageData:
    text = path.read_text(encoding="utf-8")
    raw_title = extract_first(r"<title>(.*?)</title>", text)
    return PageData(
        path=path,
        text=text,
        raw_title=raw_title,
        title=strip_tags(raw_title),
        meta_description=extract_first(
            r'<meta\s+name="description"\s+content="([^"]*)"', text
        ),
        og_title=extract_first(r'<meta\s+property="og:title"\s+content="([^"]*)"', text),
        twitter_title=extract_first(
            r'<meta\s+name="twitter:title"\s+content="([^"]*)"', text
        ),
        canonical=extract_first(r'<link\s+rel="canonical"\s+href="([^"]*)"', text),
        h1=extract_first(r"<h1[^>]*>(.*?)</h1>", text),
        internal_links=sorted(
            {
                match
                for match in re.findall(r'href="([^"]+\.html)"', text, flags=re.I)
                if not match.startswith("http")
            }
        ),
        noindex=bool(
            re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', text, flags=re.I)
        ),
    )


def load_all_pages() -> list[PageData]:
    return [load_page(path) for path in list_html_pages()]


def guess_search_category(filename: str) -> str:
    if filename == "index.html":
        return "Home"
    if filename in SITE_PAGES:
        return "Site"
    return HOMEPAGE_CARD_CATEGORY_MAP.get(filename, "Guides")


def derive_search_title(page: PageData) -> str:
    source = page.h1 or page.title or page.filename.replace(".html", "")
    cleaned = re.sub(r"\s+[—-].*$", "", source).strip()
    cleaned = re.sub(r"^Last Z\s+", "", cleaned).strip()
    return cleaned or source


def derive_search_description(page: PageData) -> str:
    source = page.meta_description or page.h1 or page.title
    source = normalize_whitespace(source)
    if len(source) <= 160:
        return source
    return source[:157].rstrip() + "..."


def derive_keywords(page: PageData) -> list[str]:
    seed = strip_tags(" ".join([page.title, page.h1, page.meta_description]))
    tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9+/-]*", seed)
    keywords: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        lower = token.lower()
        if len(lower) < 3:
            continue
        if lower in seen:
            continue
        seen.add(lower)
        keywords.append(token)
        if len(keywords) == 10:
            break
    if page.filename == "index.html":
        return ["Last Z guides", "home", "directory", "research", "events"]
    return keywords


def load_search_index() -> list[dict]:
    path = ROOT / "search-index.json"
    return json.loads(path.read_text(encoding="utf-8"))


def write_search_index(entries: Iterable[dict]) -> None:
    path = ROOT / "search-index.json"
    data = json.dumps(list(entries), indent=2, ensure_ascii=False)
    path.write_text(data + "\n", encoding="utf-8")


def sitemap_priority(filename: str) -> str:
    if filename == "index.html":
        return "1.0"
    if filename in {"codes.html", "research.html", "daily.html"}:
        return "0.9"
    if filename in SITE_PAGES:
        return "0.3"
    return "0.8"


def sitemap_changefreq(filename: str) -> str:
    if filename == "index.html":
        return "weekly"
    if filename == "codes.html":
        return "daily"
    if filename in SITE_PAGES:
        return "yearly"
    return "monthly"
