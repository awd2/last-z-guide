import html
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

FEEDS = [
    {
        "name": "Reddit",
        "label": "Reddit",
        "url": "https://old.reddit.com/r/LastZShooterRun/new/.rss",
        "hours_back": 24,
    },
    {
        "name": "Facebook",
        "label": "Facebook (FetchRSS #1)",
        "url": "https://fetchrss.com/feed/1vuYpg5Bj8Go1vuYq6GGU414.rss",
        "hours_back": None,
    },
    {
        "name": "Facebook",
        "label": "Facebook (FetchRSS #2)",
        "url": "https://fetchrss.com/feed/1vuYpg5Bj8Go1vuYsj5hi7kb.rss",
        "hours_back": None,
    },
]
RAW_DIR = "data/raw"
OUT_DIR = "content/news"
PREVIEW_PATH = "news-preview.html"


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
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.split(r"\bsubmitted by\b", text, 1)[0].strip()
    text = text.replace("(Feed generated with FetchRSS )", "").strip()
    return text


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


def fetch_post_text_fallback(link: str) -> str:
    if not link:
        return ""
    json_url = link.replace("old.reddit.com", "www.reddit.com").rstrip("/") + ".json?raw_json=1"
    try:
        data = json.loads(fetch(json_url).decode("utf-8"))
    except Exception:
        return ""
    try:
        post = data[0]["data"]["children"][0]["data"]
        selftext = (post.get("selftext") or "").strip()
        if selftext:
            return selftext
    except Exception:
        pass
    # HTML fallback (old reddit)
    try:
        html_text = fetch(link).decode("utf-8", errors="ignore")
    except Exception:
        return ""
    m = re.search(r'class="usertext-body"[^>]*>.*?<div class="md">(.*?)</div>', html_text, re.S)
    if not m:
        return ""
    return strip_html(m.group(1))


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


def parse_date_to_utc(text: str) -> datetime | None:
    text = (text or "").strip()
    if not text:
        return None
    try:
        dt = parsedate_to_datetime(text)
        if dt is not None:
            return dt.astimezone(timezone.utc)
    except (TypeError, ValueError):
        pass
    try:
        iso = text.replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def parse_feed(
    feed_name: str,
    feed_label: str,
    feed_url: str,
    hours_back: int | None,
):
    xml_bytes = fetch(feed_url)

    # Parse RSS/Atom
    root = ET.fromstring(xml_bytes)

    # Try RSS first
    items = [el for el in root.iter() if el.tag.endswith("item")]
    total_items = 0
    new_items = []

    now = datetime.now(timezone.utc)
    cutoff = None
    if hours_back is not None:
        cutoff = now - timedelta(hours=hours_back)
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
            if not link:
                continue
            if feed_name == "Reddit":
                pub_dt = parse_date_to_utc(pub)
                if cutoff is not None and pub_dt is not None and pub_dt < cutoff:
                    continue
            if not content and link:
                content = fetch_post_text_fallback(link)
            if not strip_html(content):
                print(f"No text for {link}")
            new_items.append(
                {
                    "source": feed_label,
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
            if not link:
                continue
            if feed_name == "Reddit":
                pub_dt = parse_date_to_utc(pub)
                if cutoff is not None and pub_dt is not None and pub_dt < cutoff:
                    continue
            if not content and link:
                content = fetch_post_text_fallback(link)
            if not strip_html(content):
                print(f"No text for {link}")
            new_items.append(
                {
                    "source": feed_label,
                    "title": title,
                    "link": link,
                    "pubDate": pub,
                    "author": author,
                    "content": content,
                }
            )

    return total_items, new_items


def main():
    debug_raw = os.getenv("DEBUG_RAW") == "1"
    if debug_raw:
        os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)

    new_items = []
    total_items = 0
    for feed in FEEDS:
        if debug_raw:
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            raw_path = os.path.join(RAW_DIR, f"{safe_slug(feed['label'])}_{today}.rss")
            with open(raw_path, "wb") as f:
                f.write(fetch(feed["url"]))
        feed_total, feed_new = parse_feed(
            feed["name"],
            feed["label"],
            feed["url"],
            feed["hours_back"],
        )
        total_items += feed_total
        new_items.extend(feed_new)

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
    lines.append("source: reddit+facebook")
    lines.append("feeds:")
    for feed in FEEDS:
        lines.append(f'  - "{feed["url"]}"')
    lines.append("---\n")
    lines.append("## New posts\n")

    sources_order = [feed["label"] for feed in FEEDS]
    items_by_source: dict[str, list[dict]] = {s: [] for s in sources_order}
    for it in new_items:
        items_by_source.setdefault(it.get("source", "unknown"), []).append(it)

    for source in sources_order:
        source_items = items_by_source.get(source, [])
        lines.append(f"### {source}")
        if not source_items:
            lines.append("- (no new posts)")
            lines.append("")
            continue
        for it in source_items:
            full_text = strip_html(it.get("content", ""))
            author = it.get("author") or ""
            pub = normalize_date(it.get("pubDate") or "")
            lines.append(f'- [{it["title"]}]({it["link"]})')
            if author:
                lines.append(f"  - **Author:** {author}")
            if pub:
                lines.append(f"  - **Date:** {pub}")
            if full_text:
                lines.append(f"  - **Text:** {full_text}")
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
        "  <p>Feeds:</p>",
        "  <ul>",
    ]
    for feed in FEEDS:
        preview_lines.append(f'    <li><a href="{feed["url"]}">{feed["url"]}</a></li>')
    preview_lines.append("  </ul>")
    preview_lines.append("  <h2>New posts</h2>")

    sources_order = [feed["label"] for feed in FEEDS]
    items_by_source: dict[str, list[dict]] = {s: [] for s in sources_order}
    for it in new_items:
        items_by_source.setdefault(it.get("source", "unknown"), []).append(it)

    for source in sources_order:
        source_items = items_by_source.get(source, [])
        preview_lines.append(f"  <h3>{html.escape(source)}</h3>")
        preview_lines.append("  <ul>")
        if not source_items:
            preview_lines.append("    <li>(no new posts)</li>")
        else:
            for it in source_items:
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
        preview_lines.append("  </ul>")
    preview_lines += [
        "</body>",
        "</html>",
    ]
    with open(PREVIEW_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(preview_lines))

    print(f"Created {out_path} with {len(new_items)} items.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
