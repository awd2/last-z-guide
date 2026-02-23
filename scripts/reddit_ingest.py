import html
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

FEED_URL = "https://old.reddit.com/r/LastZShooterRun/new/.rss"
STATE_PATH = "data/state/reddit_lastz.json"
RAW_DIR = "data/raw"
OUT_DIR = "content/news"
PREVIEW_PATH = "news-preview.html"
MAX_SEEN = 300


def load_state():
    if not os.path.exists(STATE_PATH):
        return {"seen": []}
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "lastzguides-bot/1.0 (rss ingest)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def safe_slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:60] or "post"


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def make_preview(text: str, limit: int = 240) -> str:
    text = strip_html(text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def extract_element_text(el: ET.Element | None) -> str:
    if el is None:
        return ""
    text = el.text or ""
    if text.strip():
        return text
    return "".join(el.itertext()).strip()


def normalize_date(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    try:
        dt = parsedate_to_datetime(text)
        if dt is not None:
            dt = dt.astimezone(timezone.utc)
            return dt.strftime("%b %d, %Y, %H:%M UTC")
    except (TypeError, ValueError):
        pass
    try:
        iso = text.replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso)
        dt = dt.astimezone(timezone.utc)
        return dt.strftime("%b %d, %Y, %H:%M UTC")
    except ValueError:
        return text


def main():
    debug_raw = os.getenv("DEBUG_RAW") == "1"
    if debug_raw:
        os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)

    xml_bytes = fetch(FEED_URL)

    # Save raw for debugging only when explicitly enabled
    if debug_raw:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        raw_path = os.path.join(RAW_DIR, f"reddit_lastz_{today}.rss")
        with open(raw_path, "wb") as f:
            f.write(xml_bytes)

    # Parse RSS/Atom
    root = ET.fromstring(xml_bytes)

    # Try RSS first
    items = [el for el in root.iter() if el.tag.endswith("item")]
    total_items = 0

    state = load_state()
    seen = set(state.get("seen", []))

    new_items = []
    if items:
        total_items = len(items)
        for item in items:
            title = next((c.text for c in item if c.tag.endswith("title")), "") or ""
            link = next((c.text for c in item if c.tag.endswith("link")), "") or ""
            pub = next((c.text for c in item if c.tag.endswith("pubDate")), "") or ""
            author = next((c.text for c in item if c.tag.endswith("creator")), "") or ""
            if not author:
                author = next((c.text for c in item if c.tag.endswith("author")), "") or ""
            content = next((c.text for c in item if c.tag.endswith("encoded")), "") or ""
            if not content:
                content = next((c.text for c in item if c.tag.endswith("description")), "") or ""
            if not link or link in seen:
                continue
            new_items.append(
                {
                    "title": title.strip(),
                    "link": link.strip(),
                    "pubDate": pub.strip(),
                    "author": author.strip(),
                    "content": content.strip(),
                }
            )
    else:
        # Atom fallback
        ns = {"a": "http://www.w3.org/2005/Atom"}
        atom_entries = root.findall(".//a:entry", ns)
        total_items = len(atom_entries)
        for entry in atom_entries:
            title_el = entry.find("a:title", ns)
            link_el = entry.find("a:link[@rel='alternate']", ns) or entry.find("a:link", ns)
            pub_el = entry.find("a:updated", ns) or entry.find("a:published", ns)
            author_el = entry.find("a:author/a:name", ns)
            content_el = entry.find("a:content", ns) or entry.find("a:summary", ns)
            title = (title_el.text or "").strip() if title_el is not None else ""
            link = (link_el.get("href") or "").strip() if link_el is not None else ""
            pub = (pub_el.text or "").strip() if pub_el is not None else ""
            author = (author_el.text or "").strip() if author_el is not None else ""
            content = extract_element_text(content_el)
            if not link or link in seen:
                continue
            new_items.append(
                {
                    "title": title,
                    "link": link,
                    "pubDate": pub,
                    "author": author,
                    "content": content,
                }
            )

    print(f"Found {total_items} posts, new {len(new_items)}.")

    if not new_items:
        print("No new posts.")
        return 0

    # Create one "daily digest" markdown file with all new posts
    local_date = datetime.now().strftime("%Y-%m-%d")
    out_name = f"{local_date}-reddit-lastz-digest.md"
    out_path = os.path.join(OUT_DIR, out_name)

    lines = []
    lines.append("---")
    lines.append(f'title: "Reddit digest — LastZShooterRun ({local_date})"')
    lines.append(f"date: {local_date}")
    lines.append("source: reddit")
    lines.append(f'feed: "{FEED_URL}"')
    lines.append("---\n")
    lines.append("## New posts\n")

    for it in new_items:
        full_text = strip_html(it.get("content", ""))
        author = it.get("author") or ""
        pub = normalize_date(it.get("pubDate") or "")
        lines.append(f'### [{it["title"]}]({it["link"]})')
        if author:
            lines.append(f"- **Author:** {author}")
        if pub:
            lines.append(f"- **Date:** {pub}")
        if full_text:
            lines.append(f"- **Text:** {full_text}")
        lines.append("")
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Update hidden HTML preview page (noindex)
    preview_lines = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"utf-8\">",
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        "  <meta name=\"robots\" content=\"noindex, nofollow\">",
        f"  <title>Reddit digest — LastZShooterRun ({local_date})</title>",
        "</head>",
        "<body>",
        f"  <h1>Reddit digest — LastZShooterRun ({local_date})</h1>",
        f"  <p>Feed: <a href=\"{FEED_URL}\">{FEED_URL}</a></p>",
        "  <h2>New posts</h2>",
        "  <ul>",
    ]
    for it in new_items:
        full_text = strip_html(it.get("content", ""))
        author = it.get("author") or ""
        pub = normalize_date(it.get("pubDate") or "")
        title = html.escape(it["title"])
        link = html.escape(it["link"])
        preview_lines.append("    <li>")
        preview_lines.append(f'      <a href="{link}">{title}</a>')
        if author:
            preview_lines.append(f'      <div><strong>Author:</strong> {html.escape(author)}</div>')
        if pub:
            preview_lines.append(f'      <div><strong>Date:</strong> {html.escape(pub)}</div>')
        if full_text:
            preview_lines.append(f'      <div><strong>Text:</strong> {html.escape(full_text)}</div>')
        preview_lines.append("    </li>")
    preview_lines += [
        "  </ul>",
        "</body>",
        "</html>",
    ]
    with open(PREVIEW_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(preview_lines))

    # Update state
    for it in new_items:
        seen.add(it["link"])
    state["seen"] = list(seen)[-MAX_SEEN:]
    save_state(state)

    print(f"Created {out_path} with {len(new_items)} items.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
