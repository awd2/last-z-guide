#!/usr/bin/env python3
"""Render human-reviewable edit proposals from Patch Spec v1 entries."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from html import unescape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_run_manifest, write_run_manifest


REPORTS_DIR = ROOT / "automation" / "reports"
MANIFESTS_DIR = ROOT / "automation" / "manifests"
SAFE_EXACT_REPLACE_OPERATION = "safe_exact_replace"


def resolve_manifest_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or path.suffix == ".json":
        return path if path.is_absolute() else ROOT / path
    return MANIFESTS_DIR / f"{value}.json"


def md_list(items: list[str]) -> str:
    if not items:
        return "- None"
    return "\n".join(f"- {item}" for item in items)


def diff_lines(prefix: str, value: str) -> str:
    return "\n".join(f"{prefix} {line}" for line in value.splitlines() or [""])


def strip_tags(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(value)).strip()


def extract_first(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.I | re.S)
    return strip_tags(match.group(1)) if match else ""


def html_context(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    headings = [strip_tags(match) for match in re.findall(r"<h2[^>]*>(.*?)</h2>", text, flags=re.I | re.S)]
    links = sorted(set(re.findall(r'href="([^"]+\.html(?:#[^"]+)?)"', text, flags=re.I)))
    return {
        "title": extract_first(r"<title>(.*?)</title>", text),
        "h1": extract_first(r"<h1[^>]*>(.*?)</h1>", text),
        "meta_description": extract_first(r'<meta\s+name="description"\s+content="([^"]*)"', text),
        "guide_verified": extract_first(r'<p class="guide-verified">(.*?)</p>', text),
        "quick_answer": extract_first(r'<p class="qa-lede">(.*?)</p>', text),
        "data_lede": extract_first(r'<p class="data-lede">(.*?)</p>', text),
        "h2_headings": headings[:8],
        "internal_links": links[:16],
    }


def json_context(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    page = payload.get("page", {})
    quick = payload.get("quick_answer", {})
    related = payload.get("related_guides", [])
    next_steps = payload.get("next_steps", {})
    return {
        "title": page.get("title", ""),
        "h1": page.get("h1", ""),
        "meta_description": page.get("meta_description", ""),
        "guide_verified": payload.get("guide_verified", ""),
        "quick_answer": quick.get("lede", ""),
        "related_guides": [item.get("href", "") for item in related if isinstance(item, dict)],
        "next_steps_title": next_steps.get("title", ""),
    }


def source_context(source_file: str) -> dict[str, Any]:
    path = ROOT / source_file
    if not path.exists():
        return {"missing": True}
    if path.suffix == ".json":
        return json_context(path)
    if path.suffix == ".html":
        return html_context(path)
    return {"path": source_file}


def infer_anchor(spec: dict[str, Any], context: dict[str, Any]) -> str:
    operation = spec.get("operation_type", "")
    source = spec.get("source_of_truth_file", "")
    if operation == SAFE_EXACT_REPLACE_OPERATION:
        return str(spec.get("selector_or_anchor") or "exact approved snippet")
    if (
        source == "start.html"
        and operation == "first_screen_update"
        and protects_claim(spec, "season-2-winter-current-naming")
    ):
        return "Quick Answer -> .qa-callouts"
    if operation in {"first_screen_update", "meta_refresh"}:
        return "page.title / page.h1 / meta_description" if source.endswith(".json") else "<title>, meta description, H1, first-screen block"
    if operation == "atlas_card_update":
        return "atlas cards / branch comparison route block"
    if operation == "internal_link_addition":
        if source.endswith(".json"):
            return "related_guides or next_steps"
        headings = context.get("h2_headings", [])
        for heading in headings:
            if "Related" in heading or "Next" in heading:
                return heading
        return "related-guides section or nearest relevant paragraph"
    return "manual review"


def before_summary(context: dict[str, Any]) -> str:
    parts = []
    for label, key in [
        ("title", "title"),
        ("h1", "h1"),
        ("meta", "meta_description"),
        ("verified", "guide_verified"),
        ("quick", "quick_answer"),
        ("data", "data_lede"),
    ]:
        value = context.get(key)
        if value:
            parts.append(f"{label}: {value}")
    if not parts:
        links = context.get("related_guides") or context.get("internal_links") or []
        if links:
            parts.append("links: " + ", ".join(links[:6]))
    return " | ".join(parts[:4]) if parts else "No compact source summary available."


def target_topic_label(run_target: str) -> str:
    labels = {
        "codes.html": "redeem codes hub, Gift Center login, UID, and redemption routing",
        "gift-center-uid.html": "Gift Center login setup and UID lookup",
        "redeem-code-not-working.html": "Gift Center troubleshooting, failed code redemption, UID, expired/already-used codes, and mailbox delay fixes",
        "research-costs.html": "research costs atlas",
        "start.html": "beginner start guide and season naming clarification",
    }
    return labels.get(run_target, run_target or "the target page")


def protects_claim(spec: dict[str, Any], claim_id: str) -> bool:
    return claim_id in {str(item) for item in spec.get("canonical_claims_to_protect", [])}


def desired_after_summary(spec: dict[str, Any], run_target: str) -> str:
    operation = spec.get("operation_type", "")
    source = spec.get("source_of_truth_file", "")
    source_type = spec.get("source_type", "")
    topic = target_topic_label(run_target)
    if operation == SAFE_EXACT_REPLACE_OPERATION:
        return (
            "Replace the exact old snippet with the exact new snippet only after owner approval. "
            "The apply step must fail closed if the source text has drifted or appears more than once."
        )
    if run_target == "codes.html":
        if source == "codes.html" and operation == "first_screen_update":
            return (
                "Tighten the first-screen answer so the page remains the codes hub: active codes first, "
                "official Gift Center redemption second, UID and mailbox facts visible without drifting into setup or troubleshooting."
            )
        if source == "codes.html" and operation == "meta_refresh":
            return (
                "No metadata change is recommended unless analytics show a specific query mismatch. "
                "The current title/H1/meta already include active codes, Gift Center login, and UID intent."
            )
        if source == "codes.html" and operation == "internal_link_addition":
            return "Do not add a self-link. Dedupe the early setup/troubleshooting routing so users choose the right adjacent Gift Center page."
        if source == "diamond-reserve.html" and operation == "internal_link_addition":
            return "Add a `Redeem Codes` related-card because this page already references free diamonds from codes in body copy."
        if source == "f2p.html" and operation == "internal_link_addition":
            return "No edit recommended: this page already links to `codes.html` in the Gift Codes section and related-guides grid."
        if source == "farm-account.html" and operation == "internal_link_addition":
            return "Add a `Redeem Codes` related-card near Gift Center UID Setup so farm-account readers can route to free-code redemption."
    if run_target == "redeem-code-not-working.html":
        if source == "redeem-code-not-working.html" and operation == "first_screen_update":
            return (
                "Add one first-screen clarification for failure-type sorting: wrong UID/typo, expired/already-used code, "
                "and mailbox delay are different checks. Keep the page as troubleshooting, not the codes hub."
            )
        if source == "redeem-code-not-working.html" and operation == "meta_refresh":
            return (
                "No metadata change is recommended. The current title, H1, and meta already target code-not-working, "
                "Gift Center, UID, login, reward, expired, already-used, and mailbox intent."
            )
        if source == "redeem-code-not-working.html" and operation == "internal_link_addition":
            return "Add `Gift Center UID Setup` to related guides because failed-code troubleshooting often starts with setup validation."
        if source == "codes.html" and operation == "internal_link_addition":
            return "No edit recommended: `codes.html` already links to this troubleshooting page in the early routing block, troubleshooting section, FAQ, and related-guides grid."
        if source == "gift-center-uid.html" and operation == "internal_link_addition":
            return "No edit recommended: `gift-center-uid.html` already links to this troubleshooting page in body copy and related guides."
        if source in {"diamond-reserve.html", "f2p.html", "farm-account.html"} and operation == "internal_link_addition":
            return "No edit recommended: this page is not a close troubleshooting source for failed code redemption."
    if run_target == "start.html" and protects_claim(spec, "season-2-winter-current-naming"):
        if operation == "first_screen_update":
            return (
                "Add a concise early clarification that for newer servers Season 2 is Winter, "
                "Desert was canceled or skipped, and older guides that call Season 2 Desert may be outdated. "
                "Keep the page primarily a beginner start guide."
            )
        if operation == "meta_refresh":
            return (
                "Preserve the beginner-guide title and H1. Only adjust metadata if needed to support "
                "the season naming clarification without turning `start.html` into a season guide."
            )
    if operation == "first_screen_update" and run_target == "research-costs.html":
        return "Opening answer names the atlas role, main research route, and exact branch-page routing without turning the atlas into a giant guide."
    if operation == "first_screen_update":
        return f"Opening answer matches the page role for {topic}, gives the exact setup answer quickly, and avoids drifting into a broader hub page."
    if operation == "meta_refresh" and run_target == "research-costs.html":
        return "Title, H1, and meta description use the same exact intent: research costs atlas, branch comparison, badge totals, and unlock paths."
    if operation == "meta_refresh":
        return f"Title, H1, and meta description use the same exact intent: {topic}."
    if operation == "atlas_card_update" and run_target == "research-costs.html":
        return "Atlas cards help users choose the correct branch page and keep the core order visible: Hero Training, Military Strategies, Peace Shield, Siege to Seize, Field Research."
    if operation == "atlas_card_update":
        return "Card or route blocks stay scoped to the target page role and help users choose the correct next page."
    if operation == "internal_link_addition" and source_type == "generated_research_branch":
        return f"JSON source adds or strengthens a route back to `{run_target}` through `related_guides` or `next_steps`, then regenerates the HTML output."
    if operation == "internal_link_addition" and spec.get("source_of_truth_file") == run_target:
        return "Do not add a self-link. Strengthen outbound routing to the correct hub, troubleshooting page, or adjacent support page instead."
    if operation == "internal_link_addition":
        return f"Source adds a crawlable, user-visible bridge to `{run_target}` in the relevant section or related-guides block."
    return "Edit remains scoped to the stated run summary and canonical claims."


def suggested_content(spec: dict[str, Any], run_target: str) -> str:
    operation = spec.get("operation_type", "")
    source = spec.get("source_of_truth_file", "")
    if operation == SAFE_EXACT_REPLACE_OPERATION:
        old = spec.get("exact_old")
        new = spec.get("exact_new")
        if not isinstance(old, str) or not isinstance(new, str):
            return "Missing exact_old or exact_new; this spec is not applyable."
        return f"""Exact approved replacement candidate:

```diff
{diff_lines("-", old)}
{diff_lines("+", new)}
```"""
    if run_target == "codes.html" and source == "codes.html" and operation == "first_screen_update":
        return """Replace the current `guide-verified` paragraph with:

```html
<p class="guide-verified">Use this page for active Last Z codes first, then redeem them through the official Gift Center. Copy your UID from Avatar &gt; Settings &gt; Copy ID, paste the code exactly, and check your in-game mailbox for rewards.</p>
```"""
    if run_target == "codes.html" and source == "codes.html" and operation == "meta_refresh":
        return "No metadata edit is recommended for this pass. Keep the current title, H1, and meta description focused on active codes, Gift Center login, and UID intent."
    if run_target == "codes.html" and source == "codes.html" and operation == "internal_link_addition":
        return """Replace the two early troubleshooting/setup routing paragraphs in the highlight box with one deduped routing paragraph:

```html
<p><strong>Need setup only?</strong> Use the <a href="gift-center-uid.html">Gift Center &amp; UID Guide</a>. <strong>Code failed?</strong> Use the <a href="redeem-code-not-working.html">Last Z Code Not Working?</a> guide.</p>
```"""
    if run_target == "codes.html" and source == "diamond-reserve.html" and operation == "internal_link_addition":
        return """Add this related-card inside the existing `Related Guides` grid, after `Resources Guide`:

```html
<a href="codes.html" class="related-card">Redeem Codes</a>
```"""
    if run_target == "codes.html" and source == "f2p.html" and operation == "internal_link_addition":
        return "Reject this spec for this pass. `f2p.html` already has an inline `Redeem Codes` link in the Gift Codes bullet and a `Redeem Codes` related-card."
    if run_target == "codes.html" and source == "farm-account.html" and operation == "internal_link_addition":
        return """Add this related-card inside the existing `Related Guides` grid, after `Gift Center UID Setup`:

```html
<a href="codes.html" class="related-card">Redeem Codes</a>
```"""
    if run_target == "redeem-code-not-working.html" and source == "redeem-code-not-working.html" and operation == "first_screen_update":
        return """Add this callout inside the existing `Quick Answer` `.qa-callouts` block, after the mailbox callout:

```html
<p class="qa-callout qa-callout--note">
    <span class="qa-icon" aria-hidden="true">i</span>
    <span class="qa-callout-text"><strong>Sort the failure first:</strong> wrong UID or typo means the redemption failed, expired or already-used means the code is no longer claimable for that account, and missing rewards means you should check mailbox timing before retrying.</span>
</p>
```"""
    if run_target == "redeem-code-not-working.html" and source == "redeem-code-not-working.html" and operation == "meta_refresh":
        return "No metadata edit is recommended for this pass. Keep the current title, H1, and meta description focused on failed redemption, Gift Center, UID, expired/already-used codes, and mailbox delays."
    if run_target == "redeem-code-not-working.html" and source == "redeem-code-not-working.html" and operation == "internal_link_addition":
        return """Add this related-card inside the existing `Related Guides` grid, after `Redeem Codes`:

```html
<a href="gift-center-uid.html" class="related-card">Gift Center UID Setup</a>
```"""
    if run_target == "redeem-code-not-working.html" and source == "codes.html" and operation == "internal_link_addition":
        return "Reject this spec for this pass. `codes.html` already links to `redeem-code-not-working.html` in the early routing block, troubleshooting section, FAQ, and related-guides grid."
    if run_target == "redeem-code-not-working.html" and source in {"diamond-reserve.html", "f2p.html", "farm-account.html"} and operation == "internal_link_addition":
        return "Reject this spec for this pass. The source page is not close enough to failed-code troubleshooting to justify another cross-link."
    if (
        run_target == "start.html"
        and source == "start.html"
        and operation == "first_screen_update"
        and protects_claim(spec, "season-2-winter-current-naming")
    ):
        return """Add this callout inside the existing `Quick Answer` `.qa-callouts` block, after the current `Core rule` callout:

```html
<p class="qa-callout qa-callout--note">
    <span class="qa-icon" aria-hidden="true">i</span>
    <span class="qa-callout-text"><strong>Season naming note:</strong> on newer servers, Season 2 is Winter. Older guides may call Season 2 Desert, but Desert was canceled or skipped for current servers, so follow Winter naming when planning your early timeline.</span>
</p>
```"""
    if (
        run_target == "start.html"
        and source == "start.html"
        and operation == "meta_refresh"
        and protects_claim(spec, "season-2-winter-current-naming")
    ):
        return "No metadata edit is recommended for this pass. Keep the current title, H1, and meta description focused on beginner intent."
    return ""


def risk_level(spec: dict[str, Any]) -> str:
    if spec.get("is_generated"):
        return "medium"
    if spec.get("operation_type") == SAFE_EXACT_REPLACE_OPERATION:
        return "medium"
    if spec.get("operation_type") in {"meta_refresh", "first_screen_update"}:
        return "medium"
    return "low"


def approval_state(spec: dict[str, Any]) -> str:
    return str(spec.get("approval_state") or "proposed")


def build_rendered_specs(manifest) -> list[dict[str, Any]]:
    patch_plan = (manifest.artifacts or {}).get("patch_plan", {})
    specs = patch_plan.get("patch_specs", [])
    target = patch_plan.get("target_page_or_slug") or (manifest.plan or {}).get("target_page_or_slug", "")
    rendered: list[dict[str, Any]] = []
    for spec in specs:
        context = source_context(str(spec.get("source_of_truth_file", "")))
        item = dict(spec)
        item["selector_or_anchor"] = infer_anchor(spec, context)
        item["before_summary"] = before_summary(context)
        item["desired_after_summary"] = desired_after_summary(spec, str(target))
        item["suggested_content"] = suggested_content(spec, str(target))
        item["risk_level"] = risk_level(spec)
        item["approval_state"] = approval_state(spec)
        rendered.append(item)
    return rendered


def render_markdown(manifest, rendered_specs: list[dict[str, Any]]) -> str:
    plan = manifest.plan or {}
    inputs = manifest.inputs or {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for spec in rendered_specs:
        grouped[str(spec["source_of_truth_file"])].append(spec)

    source_sections = []
    for source_file, specs in sorted(grouped.items()):
        lines = [f"## `{source_file}`"]
        for spec in specs:
            generator = spec.get("generator_command") or "None"
            lines.append(
                f"""
### {spec.get("operation_type")}

- Target output: `{spec.get("output_file")}`
- Source type: `{spec.get("source_type")}`
- Generated page: `{str(spec.get("is_generated")).lower()}`
- Selector or anchor: `{spec.get("selector_or_anchor")}`
- Risk: `{spec.get("risk_level")}`
- Approval state: `{spec.get("approval_state")}`
- Generator command: `{generator}`

Before:
{spec.get("before_summary")}

Desired after:
{spec.get("desired_after_summary")}

Suggested content:
{spec.get("suggested_content") or "No exact snippet generated; use the desired-after summary as the review target."}

Validation:
{md_list([str(item) for item in spec.get("validation_commands", [])])}
"""
            )
        source_sections.append("\n".join(lines))

    return f"""# Proposed Edits: {manifest.run_id}

## Overview

- Summary: {manifest.summary}
- Status: `{manifest.status}`
- Risk: `{manifest.risk_level}`
- Cluster: `{inputs.get("cluster", "")}`
- Target: `{plan.get("target_page_or_slug", "")}`
- Archetype: `{plan.get("archetype_suggestion", "")}`

## Review Rule

- This report is proposal-only.
- It does not modify site content.
- Apply only after human review changes `approval_state` from `proposed` to `approved` in a future approved-apply workflow.
- Generated research pages must be edited through JSON source files and regenerated.

## Source Files

{md_list(sorted(grouped))}

{chr(10).join(source_sections) if source_sections else "## No Patch Specs Found"}
"""


def render_proposal(path: Path):
    manifest = load_run_manifest(path)
    if manifest.status == "patch_plan_ready":
        manifest.status = "proposal_ready"
    rendered_specs = build_rendered_specs(manifest)
    markdown = render_markdown(manifest, rendered_specs)
    out_path = REPORTS_DIR / f"{manifest.run_id}.proposed.md"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")

    manifest.artifacts.setdefault("proposal", {})
    manifest.artifacts["proposal"] = {
        "report_path": str(out_path.relative_to(ROOT)),
        "rendered_specs": rendered_specs,
    }
    write_run_manifest(path, manifest)
    return out_path, rendered_specs


def main() -> int:
    parser = argparse.ArgumentParser(description="Render human-reviewable edit proposals from a run manifest.")
    parser.add_argument("manifest", help="Manifest path or basename without .json")
    args = parser.parse_args()

    manifest_path = resolve_manifest_path(args.manifest)
    out_path, rendered_specs = render_proposal(manifest_path)
    print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f"Rendered specs: {len(rendered_specs)}")
    print(f"Updated {manifest_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
