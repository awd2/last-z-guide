#!/usr/bin/env python3
"""No-write Editor worker for Scout topic proposals."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_canonical_claims, load_content_index, load_json, write_json
from automation.proposal_renderer import md_list


DEFAULT_PROPOSALS_PATH = ROOT / "automation" / "reports" / "scout-topic-proposals.json"
REPORTS_DIR = ROOT / "automation" / "reports"

CORE_CONTEXT_FILES = [
    "AGENTS.md",
    "automation/memory/site_style_guide.md",
    "automation/memory/page_archetypes.md",
    "automation/memory/seo_llm_optimization.md",
    "automation/memory/canonical_claims.json",
    "automation/memory/content_index.json",
    "automation/memory/entities.json",
    "automation/memory/release_checklist.md",
]

ARCHETYPE_SECTIONS = {
    "home-hub": [
        "First-screen site routing answer",
        "Primary cluster cards",
        "Featured exact-answer links",
        "Freshness and trust signals",
    ],
    "cornerstone-guide": [
        "Quick Answer",
        "Best overall recommendation",
        "Decision framework",
        "Cluster route block",
        "Related guides / FAQ",
    ],
    "support-guide": [
        "Quick Answer",
        "Exact procedural answer",
        "Common mistakes or edge cases",
        "Step-by-step checks",
        "Related next step",
    ],
    "atlas-page": [
        "Quick Answer",
        "Cluster overview",
        "Comparison grid or card list",
        "Recommended route",
        "Exact page links",
    ],
    "cost-page": [
        "Quick Answer",
        "Cost summary",
        "Table, tree, or planner block",
        "Key breakpoints",
        "Related guides",
    ],
    "event-guide": [
        "Quick Answer",
        "Schedule or timing block",
        "Best strategy",
        "Rewards and tradeoffs",
        "Related event links",
    ],
    "hero-profile": [
        "Quick Answer",
        "Best use case",
        "Skill and gear priority",
        "Team fit",
        "Related heroes or guides",
    ],
    "comparison-guide": [
        "Quick Answer",
        "Comparison criteria",
        "Best fit by player need",
        "Tradeoffs",
        "Related pages",
    ],
    "site-page": [
        "Purpose",
        "Inputs",
        "Output contract",
        "Operator workflow",
        "Safety constraints",
    ],
}


def strip_tags(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def extract_first(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.I | re.S)
    return strip_tags(match.group(1)) if match else ""


def extract_raw_first(pattern: str, text: str, max_length: int = 1600) -> str:
    match = re.search(pattern, text, flags=re.I | re.S)
    if not match:
        return ""
    value = match.group(0).strip()
    return value if len(value) <= max_length else ""


def html_source_snippets(text: str) -> dict[str, str]:
    candidates = {
        "title_tag": r"<title>.*?</title>",
        "meta_description_tag": r'<meta\s+name="description"\s+content="[^"]*"\s*/?>',
        "og_title_tag": r'<meta\s+property="og:title"\s+content="[^"]*"\s*/?>',
        "og_description_tag": r'<meta\s+property="og:description"\s+content="[^"]*"\s*/?>',
        "twitter_title_tag": r'<meta\s+name="twitter:title"\s+content="[^"]*"\s*/?>',
        "twitter_description_tag": r'<meta\s+name="twitter:description"\s+content="[^"]*"\s*/?>',
        "h1_tag": r"<h1[^>]*>.*?</h1>",
        "guide_meta": r'<p class="guide-meta">.*?</p>',
        "guide_verified": r'<p class="guide-verified">.*?</p>',
        "quick_answer_lede": r'<p class="qa-lede">.*?</p>',
        "data_lede": r'<p class="data-lede">.*?</p>',
        "home_hero_block": r'<header class="hero">.*?</header>',
        "home_featured_header": r'<div class="home-featured-header">\s*<h2 id="featured-guides">.*?</div>',
        "home_paths_header": r'<div class="home-featured-header">\s*<h2 id="starting-paths">.*?</div>',
    }
    snippets = {
        label: extract_raw_first(pattern, text)
        for label, pattern in candidates.items()
    }
    return {label: snippet for label, snippet in snippets.items() if snippet}


def html_context(filename: str) -> dict[str, Any]:
    path = ROOT / filename
    if not path.exists() or path.suffix != ".html":
        return {"exists": False, "filename": filename}
    text = path.read_text(encoding="utf-8")
    return {
        "exists": True,
        "filename": filename,
        "title": extract_first(r"<title>(.*?)</title>", text),
        "h1": extract_first(r"<h1[^>]*>(.*?)</h1>", text),
        "meta_description": extract_first(r'<meta\s+name="description"\s+content="([^"]*)"', text),
        "quick_answer": extract_first(r'<p class="qa-lede">(.*?)</p>', text),
        "data_lede": extract_first(r'<p class="data-lede">(.*?)</p>', text),
        "source_snippets": html_source_snippets(text),
        "h2_headings": [
            strip_tags(match)
            for match in re.findall(r"<h2[^>]*>(.*?)</h2>", text, flags=re.I | re.S)
        ][:10],
        "internal_links": sorted(set(re.findall(r'href="([^"]+\.html(?:#[^"]+)?)"', text, flags=re.I)))[:30],
    }


def content_page_lookup() -> dict[str, Any]:
    return {page.filename: page for page in load_content_index()}


def same_cluster_pages(cluster: str, target: str, limit: int = 4) -> list[str]:
    pages = [
        page.filename
        for page in load_content_index()
        if page.cluster == cluster and page.filename != target and page.status != "archived-noindex"
    ]
    return pages[:limit]


def local_page(value: str) -> str:
    if value.startswith("http"):
        path = re.sub(r"^https?://[^/]+/?", "", value).split("#", 1)[0].split("?", 1)[0]
    else:
        path = value.split("#", 1)[0].split("?", 1)[0]
    return path or "index.html"


def claim_lookup() -> dict[str, Any]:
    return {claim.id: claim for claim in load_canonical_claims()}


def claims_for_page(filename: str, proposal: dict[str, Any]) -> list[str]:
    ids = {
        claim.id
        for claim in load_canonical_claims()
        if filename in claim.related_pages
    }
    for value in proposal.get("constraints", []):
        match = re.search(r"`([^`]+)`", str(value))
        if match:
            ids.add(match.group(1))
    return sorted(ids)


def primary_query_family(proposal: dict[str, Any]) -> str:
    evidence = proposal.get("evidence", [])
    for line in evidence:
        match = re.search(r"query: `([^`]+)`", str(line))
        if match:
            return match.group(1)
    user_job = proposal.get("site_fit", {}).get("primary_user_job", "")
    match = re.search(r"`([^`]+)`", user_job)
    if match:
        return match.group(1)
    return proposal.get("title", "")


def first_screen_answer(proposal: dict[str, Any], context: dict[str, Any]) -> str:
    target = proposal.get("target_page_or_slug", "")
    query = primary_query_family(proposal)
    current = context.get("quick_answer") or context.get("data_lede")
    if current:
        return (
            f"Preserve the existing answer-first shape, but make the opening answer clearly satisfy "
            f"`{query}` without changing `{target}` into a different page role."
        )
    return (
        f"Add a concise answer-first opening for `{query}` that states the useful player action, "
        f"then routes readers to the correct section or adjacent guide."
    )


def template_reference(proposal: dict[str, Any], pages: dict[str, Any]) -> str:
    target = proposal.get("target_page_or_slug", "")
    action = proposal.get("recommended_action")
    if action == "update_existing" and target in pages:
        return target
    archetype = proposal.get("archetype_suggestion", "")
    cluster = proposal.get("cluster", "")
    for page in pages.values():
        if page.archetype == archetype and page.cluster == cluster and page.status != "archived-noindex":
            return page.filename
    for page in pages.values():
        if page.archetype == archetype and page.status != "archived-noindex":
            return page.filename
    return target


def internal_links(proposal: dict[str, Any], context: dict[str, Any]) -> dict[str, list[str]]:
    target = proposal.get("target_page_or_slug", "")
    route = proposal.get("site_fit", {}).get("expected_internal_route", [])
    upstream = [page for page in route if page != target]
    indexed_pages = {
        page.filename
        for page in load_content_index()
        if page.archetype != "site-page" and page.status != "archived-noindex"
    }
    current_links = [
        local_page(link)
        for link in context.get("internal_links", [])
        if local_page(link) in indexed_pages
    ]
    lateral = [
        page
        for page in same_cluster_pages(proposal.get("cluster", ""), target)
        if page not in upstream
    ][:3]
    downstream = [
        page
        for page in current_links
        if page not in upstream and page != target and page not in lateral
    ][:5]
    return {
        "upstream": upstream,
        "downstream": downstream,
        "lateral": lateral,
    }


def required_context_files(proposal: dict[str, Any], links: dict[str, list[str]], template: str) -> list[str]:
    files = list(CORE_CONTEXT_FILES)
    target = proposal.get("target_page_or_slug", "")
    for filename in [target, template, *links.get("upstream", []), *links.get("lateral", [])]:
        if filename and filename not in files:
            files.append(filename)
    return files


def do_not_change(proposal: dict[str, Any], protected_claims: list[str]) -> list[str]:
    items = [
        "Do not publish or apply content changes from this brief automatically.",
        "Do not change the existing page template, navigation pattern, or schema family without separate approval.",
        "Do not create a new page when the Scout proposal recommends updating an existing page.",
        "Do not use analytics signals as proof that a rewrite is required.",
        *proposal.get("reject_if", []),
    ]
    for claim_id in protected_claims:
        items.append(f"Do not contradict canonical claim `{claim_id}`.")
    return items


def acceptance_checks(target: str) -> list[str]:
    checks = [
        "python3 scripts/prepublish_check.py",
        "python3 automation/pipeline.py checks --strict",
    ]
    if target.endswith(".html"):
        checks.append(f"manual review: first-screen answer and internal links on {target}")
    return checks


def build_editor_brief(proposal: dict[str, Any], source_path: Path) -> dict[str, Any]:
    pages = content_page_lookup()
    target = proposal.get("target_page_or_slug", "")
    context = html_context(target)
    template = template_reference(proposal, pages)
    links = internal_links(proposal, context)
    protected_claims = claims_for_page(target, proposal)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    topic_id = proposal.get("topic_id", "topic")

    return {
        "schema_version": 1,
        "report_type": "editor_brief",
        "generated_at": generated_at,
        "source_proposal_file": str(source_path.relative_to(ROOT) if source_path.is_relative_to(ROOT) else source_path),
        "source_topic_id": topic_id,
        "run_id": f"{generated_at[:10]}-{topic_id}",
        "target_page_or_slug": target,
        "page_role": proposal.get("archetype_suggestion", ""),
        "primary_query_family": primary_query_family(proposal),
        "primary_user_job": proposal.get("site_fit", {}).get("primary_user_job", ""),
        "first_screen_answer": first_screen_answer(proposal, context),
        "template_reference": template,
        "required_sections": ARCHETYPE_SECTIONS.get(proposal.get("archetype_suggestion", ""), ARCHETYPE_SECTIONS["support-guide"]),
        "internal_links": links,
        "protected_claims": protected_claims,
        "do_not_change": do_not_change(proposal, protected_claims),
        "required_context_before_patch": required_context_files(proposal, links, template),
        "source_evidence": proposal.get("evidence", []),
        "source_constraints": proposal.get("constraints", []),
        "current_page_snapshot": context,
        "acceptance_checks": acceptance_checks(target),
    }


def load_proposal(path: Path, topic_id: str | None, target: str | None) -> dict[str, Any]:
    payload = load_json(path)
    proposals = payload.get("proposals", [])
    if not proposals:
        raise ValueError(f"No proposals found in {path}")
    if topic_id:
        for proposal in proposals:
            if proposal.get("topic_id") == topic_id:
                return proposal
        raise ValueError(f"Topic proposal not found: {topic_id}")
    if target:
        for proposal in proposals:
            if proposal.get("target_page_or_slug") == target:
                return proposal
        raise ValueError(f"Target proposal not found: {target}")
    return proposals[0]


def render_markdown(brief: dict[str, Any]) -> str:
    links = brief["internal_links"]
    lines = [
        f"# Editor Brief - {brief['source_topic_id']}",
        "",
        "## Overview",
        "",
        f"- Run ID: `{brief['run_id']}`",
        f"- Target: `{brief['target_page_or_slug']}`",
        f"- Page role: `{brief['page_role']}`",
        f"- Template reference: `{brief['template_reference']}`",
        f"- Primary query family: {brief['primary_query_family']}",
        f"- Primary user job: {brief['primary_user_job']}",
        "- Safety: no content, backlog, or manifest files were modified by Editor.",
        "",
        "## First-Screen Answer",
        "",
        brief["first_screen_answer"],
        "",
        "## Required Sections",
        "",
        md_list(brief["required_sections"]),
        "",
        "## Internal Links",
        "",
        f"- Upstream: {', '.join(links['upstream']) if links['upstream'] else 'None'}",
        f"- Downstream: {', '.join(links['downstream']) if links['downstream'] else 'None'}",
        f"- Lateral: {', '.join(links['lateral']) if links['lateral'] else 'None'}",
        "",
        "## Protected Claims",
        "",
        md_list([f"`{claim}`" for claim in brief["protected_claims"]]),
        "",
        "## Required Context Before Patch",
        "",
        md_list([f"`{path}`" for path in brief["required_context_before_patch"]]),
        "",
        "## Source Evidence",
        "",
        md_list(brief["source_evidence"]),
        "",
        "## Do Not Change",
        "",
        md_list(brief["do_not_change"]),
        "",
        "## Acceptance Checks",
        "",
        md_list([f"`{check}`" for check in brief["acceptance_checks"]]),
        "",
    ]
    return "\n".join(lines)


def write_outputs(brief: dict[str, Any], output_dir: Path, basename: str | None) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = basename or f"editor-brief-{brief['source_topic_id']}"
    json_path = output_dir / f"{name}.json"
    md_path = output_dir / f"{name}.md"
    write_json(json_path, brief)
    md_path.write_text(render_markdown(brief), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a no-write Editor brief from a Scout topic proposal.")
    parser.add_argument("--proposals", default=str(DEFAULT_PROPOSALS_PATH), help="Path to scout-topic-proposals.json.")
    parser.add_argument("--topic-id", help="Scout topic_id to turn into an Editor brief.")
    parser.add_argument("--target", help="Alternative selector: target page or slug.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for Editor brief artifacts.")
    parser.add_argument("--basename", help="Output basename without extension.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    proposals_path = Path(args.proposals)
    if not proposals_path.is_absolute():
        proposals_path = ROOT / proposals_path
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    proposal = load_proposal(proposals_path, topic_id=args.topic_id, target=args.target)
    brief = build_editor_brief(proposal, proposals_path)
    json_path, md_path = write_outputs(brief, output_dir, args.basename)

    summary = {
        "source_topic_id": brief["source_topic_id"],
        "target_page_or_slug": brief["target_page_or_slug"],
        "json_path": str(json_path.relative_to(ROOT)),
        "markdown_path": str(md_path.relative_to(ROOT)),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Wrote {summary['json_path']}")
        print(f"Wrote {summary['markdown_path']}")
        print(f"Topic: {summary['source_topic_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
