#!/usr/bin/env python3
"""Sync structured-data freshness and sitewide organization schema."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from site_utils import ROOT, list_html_pages


ORG_COMMENT = "    <!-- Schema.org: Organization -->\n"
ORG_SCHEMA = """    <script type="application/ld+json">
{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Last Z Guides",
        "url": "https://lastzguides.com/",
        "logo": "https://lastzguides.com/favicon-192.png",
        "email": "lastzguides@gmail.com",
        "description": "Independent Last Z guides focused on research, events, heroes, HQ progression, and F2P strategy.",
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "contactType": "editorial support",
                "email": "lastzguides@gmail.com",
                "url": "https://lastzguides.com/contact.html"
            }
        ]
    }
    </script>
"""


def sync_page(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    modified = datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()

    text = re.sub(
        r'(<meta\s+property="article:modified_time"\s+content=")([^"]*)(">)',
        rf"\g<1>{modified}\3",
        text,
    )
    text = re.sub(r'("dateModified":\s*")([^"]*)(")', rf'\g<1>{modified}\3', text)

    org_block = ORG_COMMENT + ORG_SCHEMA
    org_pattern = re.compile(
        r"\s*<!-- Schema\.org: Organization -->\s*<script type=\"application/ld\+json\">\s*\{.*?\"@type\": \"Organization\".*?\}\s*</script>\s*",
        re.S,
    )
    if org_pattern.search(text):
        text = org_pattern.sub("\n" + org_block + "\n", text, count=1)
    elif "</head>" in text:
        text = text.replace("</head>", "\n" + org_block + "\n</head>", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    updated = 0
    for path in list_html_pages():
        if sync_page(path):
            updated += 1
    print(f"Updated structured data on {updated} HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
