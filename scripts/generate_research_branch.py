#!/usr/bin/env python3
"""Generate a static research branch page from JSON data."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def fmt_num(value: int) -> str:
    return f"{value:,}"


def compact_name(name: str) -> str:
    replacements = [
        ("Attack Special Training", "Atk Special"),
        ("Strength Training", "Strength"),
        ("Resource Gathering", "Res. Gather."),
        ("Weapon Upgrading", "Weapon Upg."),
        ("Mobility Enhancement", "Mobility Enh."),
        ("Armor upgrade", "Armor Upg."),
        ("Armor Upgrade", "Armor Upg."),
        ("Aerocraft Material", "Aircraft Mat."),
        ("Camo cloating", "Camo"),
        ("Camo Coating", "Camo"),
        ("Camo Coding", "Camo"),
        ("Field training", "Field Training"),
        ("Field Training", "Field Training"),
        ("Target training", "Target Training"),
        ("Target Training", "Target Training"),
        ("Quick assembly", "Quick Assembly"),
        ("Quick Assembly", "Quick Assembly"),
        ("Arms assembly", "Arms Assembly"),
        ("Arms Assembly", "Arms Assembly"),
        ("Rider's Attack Training", "Rider Atk"),
        ("Shooter's Attack Training", "Shooter Atk"),
        ("Assaulter's Attack Training", "Assaulter Atk"),
        ("Rider's Defense Training", "Rider Def"),
        ("Shooter's Defense Training", "Shooter Def"),
        ("Assaulter's Defense Training", "Assaulter Def"),
        ("Circuitous Tactics", "Circuitous"),
        ("Unit Special Training", "UST"),
    ]
    compact = name
    for source, target in replacements:
        compact = compact.replace(source, target)
    return compact


def compact_levels(levels: str) -> str:
    return levels.replace("Lv. ", "")


def row_class_for(row: list[str]) -> str:
    return {
        1: "tree-row--single",
        2: "tree-row--two",
        3: "tree-row--three",
    }[len(row)]


def render_quick_answer(data: dict) -> str:
    items_html = []
    for idx, item in enumerate(data["items"], start=1):
        circled = ["①", "②", "③", "④", "⑤"][idx - 1]
        items_html.append(
            f"""                    <li class="qa-item">
                        <span class="qa-num" aria-hidden="true">{circled}</span>
                        <span class="qa-line">
                            <strong class="qa-title">{escape(item["title"])}</strong>
                            <span class="qa-sep">·</span>
                            <span class="qa-detail">{escape(item["detail"])}</span>
                        </span>
                    </li>"""
        )
    callout = ""
    if data.get("callout"):
        callout = f"""
                <div class="qa-callouts" role="note">
                    <p class="qa-callout qa-callout--tip">
                        <span class="qa-icon" aria-hidden="true">💡</span>
                        <span class="qa-callout-text"><strong>Key note:</strong> {data["callout"]}</span>
                    </p>
                </div>"""
    return f"""
        <section class="quick-answer quick-answer--modern" aria-label="Quick Answer">
            <p class="qa-kicker">Quick Answer</p>
            <div class="qa-body">
                <p class="qa-lede">{data["lede"]}</p>
                <ol class="qa-list">
{chr(10).join(items_html)}
                </ol>{callout}
            </div>
        </section>"""


def render_summary(summary: dict) -> str:
    bullets = []
    for item in summary["bullets"]:
        bullets.append(f'                <li><strong>{escape(item["label"])}:</strong> {item["value"]}</li>')
    return f"""
        <section class="info-card table-followup" aria-label="Summary">
            <div class="panel-title">{escape(summary["title"])}</div>
            <p>{summary["body"]}</p>
            <ul>
{chr(10).join(bullets)}
            </ul>
        </section>"""


def render_tree_node(node: dict) -> str:
    classes = ["tree-node"]
    if node["type"] == "highlight":
        classes.append("tree-node--highlight")
    elif node["type"] == "reward":
        classes.append("tree-node--reward")
    mobile_name = node.get("mobile_name", compact_name(node["name"]))
    full_levels = node["levels"]
    mobile_levels = node.get("mobile_levels", compact_levels(full_levels))
    return f"""                    <div class="{' '.join(classes)}">
                        <div class="tree-node-title tree-node-title--desktop">{escape(node["name"])}</div>
                        <div class="tree-node-title tree-node-title--mobile">{escape(mobile_name)}</div>
                        <div class="tree-node-meta">
                            <span class="tree-node-meta-full">{escape(full_levels)}</span>
                            <span class="tree-node-meta-mobile">{escape(mobile_levels)}</span>
                        </div>
                        <div class="tree-node-cost">
                            <span class="tree-node-cost-value">{fmt_num(node["total_badges"])}</span>
                            <span class="tree-node-cost-unit"> badges</span>
                        </div>
                    </div>"""


def slot_centers(row: list[str], nodes: dict[str, dict]) -> dict[str, float]:
    explicit_cols = [nodes[node_id].get("col") for node_id in row]
    if any(col is not None for col in explicit_cols):
        total_cols = max(
            len(row),
            max(int(col) for col in explicit_cols if col is not None) + 1,
        )
        centers = {}
        for index, node_id in enumerate(row):
            col = nodes[node_id].get("col", index)
            centers[node_id] = ((float(col) + 0.5) / float(total_cols)) * 100.0
        return centers

    return {
        node_id: ((float(index) + 0.5) / float(len(row))) * 100.0
        for index, node_id in enumerate(row)
    }


def segment_key(x1: float, y1: float, x2: float, y2: float) -> tuple[float, float, float, float]:
    start = (round(x1, 4), round(y1, 4))
    end = (round(x2, 4), round(y2, 4))
    if start <= end:
        return (*start, *end)
    return (*end, *start)


def render_connector_svg(source_row: list[str], target_row: list[str], nodes: dict[str, dict]) -> str:
    source_centers = slot_centers(source_row, nodes)
    target_centers = slot_centers(target_row, nodes)
    source_ids = set(source_row)
    segments: list[tuple[float, float, float, float]] = []
    seen: set[tuple[float, float, float, float]] = set()

    for child_id in target_row:
        child = nodes[child_id]
        for parent_id in child.get("parents", []):
            if parent_id not in source_ids:
                continue
            parent_x = source_centers[parent_id]
            child_x = target_centers[child_id]
            for raw_segment in (
                (parent_x, 0.0, parent_x, 50.0),
                (min(parent_x, child_x), 50.0, max(parent_x, child_x), 50.0),
                (child_x, 50.0, child_x, 100.0),
            ):
                if raw_segment[0] == raw_segment[2] and raw_segment[1] == raw_segment[3]:
                    continue
                key = segment_key(*raw_segment)
                if key in seen:
                    continue
                seen.add(key)
                segments.append(raw_segment)

    if not segments:
        return ""

    lines = []
    for x1, y1, x2, y2 in segments:
        lines.append(
            f'                    <line x1="{x1:.4f}" y1="{y1:.4f}" x2="{x2:.4f}" y2="{y2:.4f}" />'
        )

    return f"""                <svg class="tree-connector" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
{chr(10).join(lines)}
                </svg>"""


def render_tree(tree: dict, nodes: dict[str, dict]) -> str:
    uses_explicit_edges = any(node.get("parents") for node in nodes.values())
    chunks = []
    rows = tree["rows"]
    for index, row in enumerate(rows):
        row_class = row_class_for(row)
        node_html = [render_tree_node(nodes[node_id]) for node_id in row]
        chunks.append(
            f"""                <div class="tree-row {row_class}">
{chr(10).join(node_html)}
                </div>"""
        )
        if uses_explicit_edges and index < len(rows) - 1:
            connector_svg = render_connector_svg(row, rows[index + 1], nodes)
            if connector_svg:
                chunks.append(connector_svg)

    tree_class = "ar-tree ar-tree--svg" if uses_explicit_edges else "ar-tree"
    return f"""
        <section class="guide-content research-branch-content ar-tree-section" aria-labelledby="research-tree-overview">
            <h2 id="research-tree-overview">{escape(tree["title"])}</h2>
            <p class="tree-lede">{escape(tree["lede"])}</p>
            <div class="research-tree-scroll" role="region" aria-label="{escape(tree['title'])}">
                <div class="{tree_class}">
{chr(10).join(chunks)}
                </div>
            </div>
        </section>"""


def render_table(table_data: dict, nodes: list[dict]) -> str:
    rows = []
    for node in nodes:
        rows.append(
            f"""                <tr>
                    <td data-label="Node">{escape(node["name"])}</td>
                    <td data-label="Levels">{escape(node["levels"])}</td>
                    <td data-label="Total Badges">{fmt_num(node["total_badges"])}</td>
                </tr>"""
        )
    return f"""
        <section class="guide-content research-branch-content" aria-labelledby="node-cost-table">
            <h2 id="node-cost-table">{escape(table_data["title"])}</h2>
            <p>{escape(table_data["intro"])}</p>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Node</th>
                        <th>Levels</th>
                        <th>Total Badges</th>
                    </tr>
                </thead>
                <tbody>
{chr(10).join(rows)}
                </tbody>
            </table>
        </section>"""


def render_checkpoints(checkpoints: dict) -> str:
    items = []
    for item in checkpoints["items"]:
        items.append(
            f"""            <div class="step">
                <h3>{escape(item["title"])} — {escape(item["badges"])}</h3>
                <p>{escape(item["text"])}</p>
            </div>"""
        )
    return f"""
        <section class="guide-content research-branch-content">
            <h2>{escape(checkpoints["title"])}</h2>
{chr(10).join(items)}
        </section>"""


def render_requirements(data: dict | None) -> str:
    if not data:
        return ""
    bullets = [f"                <li>{item}</li>" for item in data.get("bullets", [])]
    followup = ""
    if data.get("followup"):
        followup = f"\n            <p>{data['followup']}</p>"
    return f"""
        <section class="guide-content research-branch-content">
            <h2>{escape(data["title"])}</h2>
            <p>{data["intro"]}</p>
            <ul>
{chr(10).join(bullets)}
            </ul>{followup}
        </section>"""


def render_next_steps(data: dict) -> str:
    paras = [f"            <p>{p}</p>" for p in data["paragraphs"]]
    return f"""
        <section class="guide-content research-branch-content">
            <h2>{escape(data["title"])}</h2>
{chr(10).join(paras)}
        </section>"""


def render_faq(branch_name: str, faq: list[dict]) -> str:
    items = []
    for qa in faq:
        items.append(
            f"""            <div class="faq-item">
                <h3>{escape(qa["question"])}</h3>
                <p>{escape(qa["answer"])}</p>
            </div>"""
        )
    return f"""
        <section class="faq-section">
            <h2>{escape(branch_name)} FAQ</h2>
{chr(10).join(items)}
        </section>"""


def render_related(guides: list[dict]) -> str:
    links = [
        f'                <a href="{escape(item["href"])}" class="related-card">{escape(item["label"])}</a>'
        for item in guides
    ]
    return f"""
        <section class="related-guides">
            <h2>Related Guides</h2>
            <div class="related-grid">
{chr(10).join(links)}
            </div>
        </section>"""


def render_page(data: dict) -> str:
    page = data["page"]
    slug = page["slug"]
    nodes = {node["id"]: node for node in data["nodes"]}

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "author": {"@type": "Organization", "name": "Last Z Guides"},
        "publisher": {"@type": "Organization", "name": "Last Z Guides"},
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
            }
            for item in data["faq"]
        ],
    }
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "publisher": {"@type": "Organization", "name": "Last Z Guides"},
        "headline": page["headline"],
        "description": page["meta_description"],
        "author": {"@type": "Organization", "name": "Last Z Guides"},
        "datePublished": page["updated_iso"],
        "dateModified": page["updated_iso"],
    }
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://lastzguides.com/"},
            {"@type": "ListItem", "position": 2, "name": "Research Guide", "item": "https://lastzguides.com/research.html"},
            {"@type": "ListItem", "position": 3, "name": page["h1"], "item": f"https://lastzguides.com/{slug}.html"},
        ],
    }
    dataset_schema = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": page["h1"],
        "description": page["meta_description"],
        "creator": {"@type": "Organization", "name": "Last Z Guides"},
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "variableMeasured": ["Node", "Levels", "Total Badges"],
    }
    org_schema = {
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
                "url": "https://lastzguides.com/contact.html",
            }
        ],
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://www.google-analytics.com" crossorigin>

    <script async src="https://www.googletagmanager.com/gtag/js?id=G-PYBSRQ1QFP"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-PYBSRQ1QFP');
    </script>
    <title>{escape(page["title"])}</title>
    <meta name="description" content="{escape(page["meta_description"])}">
    <meta name="keywords" content="{escape(page["keywords"])}">
    <link rel="canonical" href="https://lastzguides.com/{slug}.html">
    <link rel="stylesheet" href="style.css">
    <link rel="preload" as="style" href="quick-answer.css" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="quick-answer.css"></noscript>
    <link rel="stylesheet" href="search.css">
    <link rel="stylesheet" href="vehicle-table.css">
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="icon" type="image/png" href="favicon.png">
    <link rel="icon" href="favicon.ico" sizes="any">
    <link rel="icon" type="image/png" href="favicon-32.png" sizes="32x32">
    <link rel="icon" type="image/png" href="favicon-48.png" sizes="48x48">
    <link rel="icon" type="image/png" href="favicon-192.png" sizes="192x192">

    <meta property="og:title" content="{escape(page["h1"])}">
    <meta property="og:description" content="{escape(page["meta_description"])}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://lastzguides.com/{slug}.html">
    <meta property="og:image" content="https://lastzguides.com/og-image.png">
    <meta property="og:image:alt" content="Last Z Survival Shooter — Complete Game Guides">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="Last Z Guides">
    <meta property="article:published_time" content="{page["updated_iso"]}">
    <meta property="article:modified_time" content="{page["updated_iso"]}">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape(page["h1"])}">
    <meta name="twitter:description" content="{escape(page["meta_description"])}">
    <meta name="twitter:image" content="https://lastzguides.com/og-image.png">
    <meta name="twitter:image:alt" content="Last Z Survival Shooter — Complete Game Guides">
    <meta name="robots" content="max-image-preview:large">

    <script type="application/ld+json">{json.dumps(article_schema, separators=(",", ":"))}</script>
    <script type="application/ld+json">{json.dumps(faq_schema, separators=(",", ":"))}</script>
    <script type="application/ld+json">{json.dumps(breadcrumb_schema, separators=(",", ":"))}</script>
    <script type="application/ld+json">{json.dumps(dataset_schema, separators=(",", ":"))}</script>
    <script type="application/ld+json">{json.dumps(org_schema, separators=(",", ":"))}</script>
</head>
<body>
    <header class="site-header">
        <a href="/" class="logo-link">
            <img decoding="async" class="site-logo" src="favicon-32.png" alt="Last Z Guides" width="18" height="18">
            <span>Last Z Guides</span>
        </a>
        <button class="search-trigger" aria-label="Search">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <span>Search...</span>
            <kbd><span>⌘</span>K</kbd>
        </button>
        <nav class="home-nav site-nav" aria-label="Guide categories">
            <a href="/#progression">Progression</a>
            <a href="/#research-tech" class="is-active">Research</a>
            <a href="/#heroes-gear">Heroes</a>
            <a href="/#pvp-formations">PvP</a>
            <a href="/#events-competitive">Events</a>
            <a href="/#economy-f2p">Economy</a>
        </nav>
    </header>

    <nav class="breadcrumb">
        <a href="/">Home</a>
        <span>›</span>
        <a href="research.html">Research Guide</a>
        <span>›</span>
        <span>{escape(page["h1"])}</span>
    </nav>

    <article class="guide data-guide research-branch-guide">
        <header class="guide-header">
            <h1>{escape(page["h1"])}</h1>
            <div class="guide-meta">{escape(page["guide_meta"])}</div>
            <p class="guide-author">By <a href="about.html">Last Z Guides</a></p>
            <p class="guide-verified">{data["guide_verified"]}</p>
            <p class="data-lede">{data["data_lede"]}</p>
        </header>

        <div class="toc-placeholder"></div>
{render_quick_answer(data["quick_answer"])}
{render_summary(data["summary"])}
{render_tree(data["tree"], nodes)}
{render_table(data["table"], data["nodes"])}
{render_requirements(data.get("requirements"))}
{render_checkpoints(data["checkpoints"])}
{render_next_steps(data["next_steps"])}
{render_faq(page.get("short_name", page["h1"]), data["faq"])}
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>How this guide was verified:</strong> Based on in-game data, tested results, and cross-checks against community validation.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Source pattern:</strong> In-game data + tested results + community validation.</li>
            </ul>
        </section>

        <section class="disclaimer">
            <p>Game mechanics and numbers may change with updates. This guide was last validated in March 2026.</p>
        </section>
{render_related(data["related_guides"])}
    </article>

    <footer class="site-footer">
        <a href="/">All Guides</a>
        <div class="footer-links">
            <a href="about.html">About</a>
            <a href="contact.html">Contact</a>
            <a href="privacy.html">Privacy</a>
            <a href="terms.html">Terms</a>
            <a href="disclosure.html">Disclosure</a>
        </div>
    </footer>
    <script src="analytics.js" defer></script>
    <script src="search-loader.js" defer></script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a static research branch page from JSON data.")
    parser.add_argument("source", type=Path, help="Path to the branch JSON file.")
    args = parser.parse_args()

    source = args.source
    if not source.is_absolute():
        source = ROOT / source

    data = json.loads(source.read_text())
    output = ROOT / f'{data["page"]["slug"]}.html'
    output.write_text(render_page(data))
    print(f"Generated {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
