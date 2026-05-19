#!/usr/bin/env python3
"""Render a no-write apply preview from approved Patch Spec v1 entries."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_run_manifest, write_run_manifest
from automation.proposal_renderer import REPORTS_DIR, md_list, resolve_manifest_path, resolve_path


TARGET_LABELS = {
    "codes.html": "Redeem Codes",
    "gift-center-uid.html": "Gift Center UID Setup",
    "redeem-code-not-working.html": "Code Not Working",
    "research-costs.html": "Research Costs Atlas",
}

START_SEASON_NOTE = (
    '<p class="qa-callout qa-callout--note">\n'
    '    <span class="qa-icon" aria-hidden="true">i</span>\n'
    '    <span class="qa-callout-text"><strong>Season naming note:</strong> on newer servers, Season 2 is Winter. Older guides may call Season 2 Desert, but Desert was canceled or skipped for current servers, so follow Winter naming when planning your early timeline.</span>\n'
    "</p>"
)

CODES_GUIDE_VERIFIED = (
    '<p class="guide-verified">Use this page for active Last Z codes first, then redeem them through the official Gift Center. '
    'Copy your UID from Avatar &gt; Settings &gt; Copy ID, paste the code exactly, and check your in-game mailbox for rewards.</p>'
)

CODES_ROUTING_PARAGRAPH = (
    '<p><strong>Need setup only?</strong> Use the <a href="gift-center-uid.html">Gift Center &amp; UID Guide</a>. '
    '<strong>Code failed?</strong> Use the <a href="redeem-code-not-working.html">Last Z Code Not Working?</a> guide.</p>'
)

REDEEM_FAILURE_SORTING_CALLOUT = (
    '<p class="qa-callout qa-callout--note">\n'
    '    <span class="qa-icon" aria-hidden="true">i</span>\n'
    '    <span class="qa-callout-text"><strong>Sort the failure first:</strong> wrong UID or typo means the redemption failed, expired or already-used means the code is no longer claimable for that account, and missing rewards means you should check mailbox timing before retrying.</span>\n'
    "</p>"
)

SAFE_EXACT_REPLACE_OPERATION = "safe_exact_replace"


def approved_specs(manifest) -> list[dict[str, Any]]:
    patch_plan = (manifest.artifacts or {}).get("patch_plan", {})
    return [
        spec
        for spec in patch_plan.get("patch_specs", [])
        if spec.get("approval_state") == "approved"
    ]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def json_has_related_link(path: Path, href: str) -> bool:
    if not path.exists():
        return False
    payload = json.loads(path.read_text(encoding="utf-8"))
    return any(item.get("href") == href for item in payload.get("related_guides", []) if isinstance(item, dict))


def html_has_link(path: Path, href: str) -> bool:
    return f'href="{href}"' in read_text(path)


def html_related_grid_has_link(path: Path, href: str) -> bool:
    text = read_text(path)
    marker = '<div class="related-grid">'
    start = text.find(marker)
    if start == -1:
        return False
    end = text.find("</div>", start)
    if end == -1:
        return False
    return f'href="{href}"' in text[start:end]


def diff_block(title: str, before: str, after: str) -> str:
    return f"""```diff
# {title}
- {before}
+ {after}
```"""


def exact_replace_values(spec: dict[str, Any]) -> tuple[str | None, str | None]:
    old = spec.get("exact_old")
    new = spec.get("exact_new")
    return (old if isinstance(old, str) else None, new if isinstance(new, str) else None)


def target_label(target_page: str) -> str:
    return TARGET_LABELS.get(target_page, target_page)


def meta_preview_for_target(source_file: str) -> str | None:
    if source_file == "research-costs.html":
        return "\n\n".join(
            [
                diff_block(
                    "<title>",
                    "Last Z Research Costs Atlas (2026) -- All Research Trees, Badge Totals, and Unlock Paths",
                    "Last Z Research Costs Atlas (2026) -- Branch Comparison, Badge Totals, and Unlock Paths",
                ),
                diff_block(
                    "meta description",
                    "All major Last Z research trees in one place: total badge costs, unlock requirements, best stopping points, and links to every exact node-cost tree.",
                    "Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page before spending badges.",
                ),
                diff_block(
                    "H1",
                    "Last Z Research Costs Atlas -- All Research Trees, Badge Totals, and Unlock Paths",
                    "Last Z Research Costs Atlas -- Branch Comparison, Badge Totals, and Unlock Paths",
                ),
            ]
        )
    if source_file == "gift-center-uid.html":
        return "\n\n".join(
            [
                diff_block(
                    "<title>",
                    "Last Z Gift Center Login & UID Guide (2026) -- Official Redeem Page",
                    "Last Z Gift Center Login and UID Setup (2026) -- Official Redeem Page",
                ),
                diff_block(
                    "meta description",
                    "Official Last Z Gift Center login, how to find and copy your UID, how to redeem codes on iPhone or Android, and where rewards appear after redemption.",
                    "Official Last Z Gift Center login setup: how to copy your UID from Avatar > Settings > Copy ID, redeem in a browser, and collect rewards from mailbox.",
                ),
                diff_block(
                    "H1",
                    "Last Z Gift Center Login & UID Guide -- Official Redeem Page",
                    "Last Z Gift Center Login and UID Setup -- Official Redeem Page",
                ),
            ]
        )
    return None


def first_screen_preview_for_target(source_file: str) -> str | None:
    if source_file == "research-costs.html":
        return diff_block(
            "first-screen answer",
            "Best way to use the research atlas: start with Hero Training to Cockpit...",
            "Best way to use the research atlas: use this page as the branch router, then open the exact cost page for node totals. For most players, the main route is Hero Training to Cockpit, Military Strategies, Peace Shield, Siege to Seize, then Field Research.",
        )
    if source_file == "gift-center-uid.html":
        return diff_block(
            "first-screen answer",
            "The official Last Z Gift Center login page is the only place where codes are redeemed...",
            "Use the official Last Z Gift Center in a browser, copy your UID from Avatar > Settings > Copy ID, redeem the code outside the game, then collect rewards from mailbox.",
        )
    if source_file == "start.html":
        return diff_block(
            "Quick Answer callout",
            "Only the existing Core rule callout appears in `.qa-callouts`.",
            START_SEASON_NOTE,
        )
    if source_file == "codes.html":
        return diff_block(
            "guide-verified",
            "Use the official Last Z Gift Center to redeem active codes. This page gives you the current verified codes, the official login page, the fastest UID steps, and the main reasons redemption fails.",
            CODES_GUIDE_VERIFIED,
        )
    if source_file == "redeem-code-not-working.html":
        return diff_block(
            "Quick Answer callout",
            "Existing callouts explain official Gift Center, UID copying, and mailbox rewards.",
            REDEEM_FAILURE_SORTING_CALLOUT,
        )
    return None


def preview_for_spec(spec: dict[str, Any], target_page: str) -> dict[str, Any]:
    source_file = str(spec.get("source_of_truth_file", ""))
    operation = str(spec.get("operation_type", ""))
    source_type = str(spec.get("source_type", ""))
    path = ROOT / source_file
    warnings: list[str] = []
    preview = ""
    action = "manual_review"

    if operation == "meta_refresh":
        action = "replace_metadata_strings"
        preview = meta_preview_for_target(source_file) or "Manual metadata preview required."
        if preview.startswith("Manual"):
            warnings.append("No deterministic metadata preview template exists for this target yet.")

    elif operation == SAFE_EXACT_REPLACE_OPERATION:
        action = "safe_exact_replace"
        old, new = exact_replace_values(spec)
        if not old or not new:
            warnings.append("Missing `exact_old` or `exact_new`; apply-approved will fail closed.")
            preview = "Manual exact replacement preview unavailable."
        else:
            text = read_text(path)
            old_count = text.count(old)
            new_count = text.count(new)
            if old_count != 1:
                warnings.append(f"`exact_old` occurs {old_count} time(s); apply-approved requires exactly one match.")
            if old_count == 0 and new_count == 1:
                warnings.append("`exact_new` already appears once and `exact_old` is absent; apply-approved will treat this as already applied.")
            if spec.get("is_generated"):
                warnings.append("Generated sources are not allowed for safe_exact_replace.")
            if spec.get("source_type") != "html_file":
                warnings.append("safe_exact_replace currently supports only `html_file` sources.")
            preview = diff_block(str(spec.get("selector_or_anchor") or "exact replacement"), old, new)

    elif operation == "first_screen_update":
        action = "replace_first_screen_answer"
        preview = first_screen_preview_for_target(source_file) or "Manual first-screen preview required."
        if preview.startswith("Manual"):
            warnings.append("No deterministic first-screen preview template exists for this target yet.")

    elif operation == "atlas_card_update" and source_file == "research-costs.html":
        action = "tighten_atlas_card_copy"
        preview = diff_block(
            "atlas card routing copy",
            "View tree ->",
            "View exact cost tree ->",
        )

    elif operation == "internal_link_addition" and source_type == "generated_research_branch":
        action = "add_json_related_guide"
        exists = json_has_related_link(path, target_page)
        if exists:
            warnings.append(f"`{source_file}` already links to `{target_page}` in `related_guides`.")
        preview = diff_block(
            "related_guides JSON entry",
            '"related_guides": [ ... ]',
            f'"related_guides": [ ..., {{ "href": "{target_page}", "label": "{target_label(target_page)}" }} ]',
        )

    elif operation == "internal_link_addition" and source_file == target_page:
        if source_file == "codes.html":
            action = "dedupe_gift_center_routing"
            preview = diff_block(
                "early Gift Center routing",
                "Two overlapping setup/troubleshooting paragraphs in the highlight box.",
                CODES_ROUTING_PARAGRAPH,
            )
        elif source_file == "redeem-code-not-working.html":
            action = "add_setup_related_card"
            exists = html_related_grid_has_link(path, "gift-center-uid.html")
            if exists:
                warnings.append("`redeem-code-not-working.html` already links to `gift-center-uid.html` in related guides.")
            preview = diff_block(
                "related guide card",
                '<a href="codes.html" class="related-card">Redeem Codes</a>',
                '<a href="codes.html" class="related-card">Redeem Codes</a>\n<a href="gift-center-uid.html" class="related-card">Gift Center UID Setup</a>',
            )
        else:
            action = "no_self_link_strengthen_outbound_routes"
            warnings.append(f"Do not add a self-link from `{source_file}` to itself.")
            preview = diff_block(
                "outbound routing",
                "Related guides stay unchanged or underspecified.",
                "Strengthen links to the correct hub, troubleshooting page, or adjacent support page instead of adding a self-link.",
            )

    elif operation == "internal_link_addition":
        action = "add_related_card"
        exists = html_related_grid_has_link(path, target_page)
        if exists:
            warnings.append(f"`{source_file}` already links to `{target_page}`.")
        preview = diff_block(
            "related guide card",
            '<div class="related-grid"> ... </div>',
            f'<div class="related-grid"> ... <a href="{target_page}" class="related-card">{target_label(target_page)}</a> ... </div>',
        )

    else:
        warnings.append("No deterministic preview template exists for this operation yet.")
        preview = "Manual preview required."

    return {
        "source_of_truth_file": source_file,
        "output_file": spec.get("output_file"),
        "operation_type": operation,
        "source_type": source_type,
        "is_generated": bool(spec.get("is_generated")),
        "generator_command": spec.get("generator_command"),
        "approval_state": spec.get("approval_state"),
        "preview_action": action,
        "warnings": warnings,
        "preview": preview,
        "validation_commands": spec.get("validation_commands", []),
        "target_page": target_page,
    }


def render_markdown(manifest, preview_items: list[dict[str, Any]], generated_at: str) -> str:
    plan = manifest.plan or {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in preview_items:
        grouped[str(item["source_of_truth_file"])].append(item)

    sections: list[str] = []
    for source_file, items in sorted(grouped.items()):
        lines = [f"## `{source_file}`"]
        for item in items:
            generator = item.get("generator_command") or "None"
            warnings = [escape(str(value)) for value in item.get("warnings", [])]
            lines.append(
                f"""
### {item.get("operation_type")}

- Target output: `{item.get("output_file")}`
- Source type: `{item.get("source_type")}`
- Generated page: `{str(item.get("is_generated")).lower()}`
- Approval state: `{item.get("approval_state")}`
- Preview action: `{item.get("preview_action")}`
- Generator command: `{generator}`

Warnings:
{md_list(warnings)}

Preview patch:
{item.get("preview")}

Validation:
{md_list([str(command) for command in item.get("validation_commands", [])])}
"""
            )
        sections.append("\n".join(lines))

    return f"""# Apply Preview: {manifest.run_id}

## Overview

- Summary: {manifest.summary}
- Status before preview: `{manifest.status}`
- Target: `{plan.get("target_page_or_slug", "")}`
- Approved specs: {len(preview_items)}
- Generated at: `{generated_at}`

## Safety Rule

- This report is preview-only.
- It does not modify site content.
- It only renders operations with `approval_state=approved`.
- Generated research pages must still be edited through JSON source files and regenerated.

## Source Files

{md_list(sorted(grouped))}

{chr(10).join(sections) if sections else "## No Approved Specs Found"}
"""


def render_apply_preview(path: Path, reports_dir: Path = REPORTS_DIR):
    manifest = load_run_manifest(path)
    specs = approved_specs(manifest)
    if not specs:
        raise ValueError("No approved Patch Spec v1 entries found.")

    target_page = str((manifest.plan or {}).get("target_page_or_slug", ""))
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    preview_items = [preview_for_spec(spec, target_page) for spec in specs]
    markdown = render_markdown(manifest, preview_items, generated_at)

    out_path = reports_dir / f"{manifest.run_id}.apply-preview.md"
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")

    manifest.artifacts.setdefault("apply_preview", {})
    manifest.artifacts["apply_preview"] = {
        "report_path": rel(out_path),
        "generated_at": generated_at,
        "approved_specs_count": len(preview_items),
        "preview_items": preview_items,
    }
    if manifest.status == "approved_for_apply":
        manifest.status = "apply_preview_ready"
    write_run_manifest(path, manifest)
    return out_path, preview_items


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a no-write apply preview for approved proposal specs.")
    parser.add_argument("manifest", help="Manifest path or basename without .json")
    parser.add_argument("--output-dir", help="Directory for the apply-preview report.")
    args = parser.parse_args()

    manifest_path = resolve_manifest_path(args.manifest)
    report_dir = resolve_path(args.output_dir) if args.output_dir else REPORTS_DIR
    try:
        out_path, preview_items = render_apply_preview(manifest_path, report_dir)
    except ValueError as exc:
        print(str(exc))
        return 1

    print(f"Wrote {rel(out_path)}")
    print(f"Previewed approved specs: {len(preview_items)}")
    print(f"Updated {rel(manifest_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
