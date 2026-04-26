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
from automation.proposal_renderer import REPORTS_DIR, md_list, resolve_manifest_path


TARGET_LABELS = {
    "gift-center-uid.html": "Gift Center UID Setup",
    "research-costs.html": "Research Costs Atlas",
}


def approved_specs(manifest) -> list[dict[str, Any]]:
    patch_plan = (manifest.artifacts or {}).get("patch_plan", {})
    return [
        spec
        for spec in patch_plan.get("patch_specs", [])
        if spec.get("approval_state") == "approved"
    ]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def json_has_related_link(path: Path, href: str) -> bool:
    if not path.exists():
        return False
    payload = json.loads(path.read_text(encoding="utf-8"))
    return any(item.get("href") == href for item in payload.get("related_guides", []) if isinstance(item, dict))


def html_has_link(path: Path, href: str) -> bool:
    return f'href="{href}"' in read_text(path)


def diff_block(title: str, before: str, after: str) -> str:
    return f"""```diff
# {title}
- {before}
+ {after}
```"""


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
        action = "no_self_link_strengthen_outbound_routes"
        warnings.append(f"Do not add a self-link from `{source_file}` to itself.")
        preview = diff_block(
            "outbound routing",
            "Related guides stay unchanged or underspecified.",
            "Strengthen links to the correct hub, troubleshooting page, or adjacent support page instead of adding a self-link.",
        )

    elif operation == "internal_link_addition":
        action = "add_related_card"
        exists = html_has_link(path, target_page)
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


def render_apply_preview(path: Path):
    manifest = load_run_manifest(path)
    specs = approved_specs(manifest)
    if not specs:
        raise ValueError("No approved Patch Spec v1 entries found.")

    target_page = str((manifest.plan or {}).get("target_page_or_slug", ""))
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    preview_items = [preview_for_spec(spec, target_page) for spec in specs]
    markdown = render_markdown(manifest, preview_items, generated_at)

    out_path = REPORTS_DIR / f"{manifest.run_id}.apply-preview.md"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")

    manifest.artifacts.setdefault("apply_preview", {})
    manifest.artifacts["apply_preview"] = {
        "report_path": str(out_path.relative_to(ROOT)),
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
    args = parser.parse_args()

    manifest_path = resolve_manifest_path(args.manifest)
    try:
        out_path, preview_items = render_apply_preview(manifest_path)
    except ValueError as exc:
        print(str(exc))
        return 1

    print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f"Previewed approved specs: {len(preview_items)}")
    print(f"Updated {manifest_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
