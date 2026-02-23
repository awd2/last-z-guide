import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

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

    state = load_state()
    seen = set(state.get("seen", []))

    new_items = []
    if items:
        for item in items:
            title = next((c.text for c in item if c.tag.endswith("title")), "") or ""
            link = next((c.text for c in item if c.tag.endswith("link")), "") or ""
            pub = next((c.text for c in item if c.tag.endswith("pubDate")), "") or ""
            if not link or link in seen:
                continue
            new_items.append({"title": title.strip(), "link": link.strip(), "pubDate": pub.strip()})
    else:
        # Atom fallback
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for entry in root.findall(".//a:entry", ns):
            title_el = entry.find("a:title", ns)
            link_el = entry.find("a:link[@rel='alternate']", ns) or entry.find("a:link", ns)
            pub_el = entry.find("a:updated", ns) or entry.find("a:published", ns)
            title = (title_el.text or "").strip() if title_el is not None else ""
            link = (link_el.get("href") or "").strip() if link_el is not None else ""
            pub = (pub_el.text or "").strip() if pub_el is not None else ""
            if not link or link in seen:
                continue
            new_items.append({"title": title, "link": link, "pubDate": pub})

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
        lines.append(f'- [{it["title"]}]({it["link"]})')
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
        preview_lines.append(f'    <li><a href="{it["link"]}">{it["title"]}</a></li>')
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
