#!/usr/bin/env python3
"""Apply approved Patch Spec v1 entries with conservative deterministic templates."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_run_manifest, write_json, write_run_manifest
from automation.proposal_renderer import REPORTS_DIR, md_list, resolve_manifest_path


TARGET_ATLAS = "research-costs.html"
ATLAS_CARD = {"href": "research-costs.html", "label": "Research Costs Atlas"}


def approved_specs(manifest) -> list[dict[str, Any]]:
    patch_plan = (manifest.artifacts or {}).get("patch_plan", {})
    return [
        spec
        for spec in patch_plan.get("patch_specs", [])
        if spec.get("approval_state") == "approved"
    ]


def replace_once(text: str, old: str, new: str, applied: list[str], label: str) -> str:
    if old not in text:
        return text
    applied.append(label)
    return text.replace(old, new, 1)


def apply_research_costs(specs: list[dict[str, Any]]) -> list[str]:
    path = ROOT / TARGET_ATLAS
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []
    operations = {spec.get("operation_type") for spec in specs}

    if "meta_refresh" in operations:
        replacements = [
            (
                "<title>Last Z Research Costs Atlas (2026) — All Research Trees, Badge Totals, and Unlock Paths</title>",
                "<title>Last Z Research Costs Atlas (2026) — Branch Comparison, Badge Totals, and Unlock Paths</title>",
                "title",
            ),
            (
                '<meta name="description" content="All major Last Z research trees in one place: total badge costs, unlock requirements, best stopping points, and links to every exact node-cost tree.">',
                '<meta name="description" content="Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page before spending badges.">',
                "meta_description",
            ),
            (
                '<meta property="og:title" content="Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths">',
                '<meta property="og:title" content="Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths">',
                "og_title",
            ),
            (
                '<meta property="og:description" content="Compare all major Last Z research trees by total badges, unlock requirements, and exact node-cost pages.">',
                '<meta property="og:description" content="Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page.">',
                "og_description",
            ),
            (
                '<meta name="twitter:title" content="Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths">',
                '<meta name="twitter:title" content="Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths">',
                "twitter_title",
            ),
            (
                '<meta name="twitter:description" content="Compare all major Last Z research trees by total badges, unlock requirements, and exact node-cost pages.">',
                '<meta name="twitter:description" content="Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page.">',
                "twitter_description",
            ),
            (
                '"headline": "Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths"',
                '"headline": "Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths"',
                "article_headline",
            ),
            (
                '"description": "All major Last Z research trees in one place: total badge costs, unlock requirements, best stopping points, and links to every exact node-cost tree."',
                '"description": "Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page before spending badges."',
                "article_description",
            ),
            (
                "<h1>Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths</h1>",
                "<h1>Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths</h1>",
                "h1",
            ),
        ]
        for old, new, label in replacements:
            text = replace_once(text, old, new, applied, f"research-costs:{label}")

    if "first_screen_update" in operations:
        text = replace_once(
            text,
            '<p class="guide-verified">This atlas is the fastest way to compare all major badge-heavy research trees in Last Z. Use it when you want to see total branch cost, unlock requirements, and the exact tree page for each branch without jumping through the whole site blindly.</p>',
            '<p class="guide-verified">This atlas is the branch router for Last Z research costs: compare badge totals and unlock paths here, then open the exact branch page for node-by-node costs before spending badges.</p>',
            applied,
            "research-costs:guide_verified",
        )
        text = replace_once(
            text,
            '<p class="data-lede">Use this page to compare every major research branch by total badge cost, unlock path, and practical value. It is the main entry point for exact node trees and badge planning across the whole research cluster.</p>',
            '<p class="data-lede">Use this page to compare every major research branch by badge total, unlock path, and priority role. The main route for most players is Hero Training to Cockpit, Military Strategies, Peace Shield, Siege to Seize, then Field Research.</p>',
            applied,
            "research-costs:data_lede",
        )
        text = replace_once(
            text,
            '<p class="qa-lede"><strong>Best way to use the research atlas:</strong> start with Hero Training to Cockpit, move into Military Strategies and Peace Shield for efficient mid-game value, and treat Unit Special Training as the biggest late-game badge sink rather than an early goal.</p>',
            '<p class="qa-lede"><strong>Best way to use the research atlas:</strong> use this page as the branch router, then open the exact cost page for node totals. For most players, the main route is Hero Training to Cockpit, Military Strategies, Peace Shield, Siege to Seize, then Field Research.</p>',
            applied,
            "research-costs:qa_lede",
        )

    if {"internal_link_addition", "atlas_card_update"} & operations:
        count = text.count('<span class="atlas-link">View tree →</span>')
        if count:
            text = text.replace(
                '<span class="atlas-link">View tree →</span>',
                '<span class="atlas-link">View exact cost tree →</span>',
            )
            applied.append(f"research-costs:atlas_link_copy:{count}")

    path.write_text(text, encoding="utf-8")
    return applied


def add_html_related_card(source_file: str) -> list[str]:
    path = ROOT / source_file
    text = path.read_text(encoding="utf-8")
    if f'href="{TARGET_ATLAS}"' in text:
        return []
    anchor = '                <a href="research.html" class="related-card">Research Priority</a>'
    if anchor not in text:
        anchor = '                <a href="research.html" class="related-card">Research Guide</a>'
    if anchor not in text:
        return []
    replacement = anchor + '\n                <a href="research-costs.html" class="related-card">Research Costs Atlas</a>'
    text = text.replace(anchor, replacement, 1)
    path.write_text(text, encoding="utf-8")
    return [f"{source_file}:related_card"]


def add_json_related_guide(source_file: str) -> list[str]:
    path = ROOT / source_file
    payload = json.loads(path.read_text(encoding="utf-8"))
    related = payload.setdefault("related_guides", [])
    if any(item.get("href") == TARGET_ATLAS for item in related if isinstance(item, dict)):
        return []

    insert_at = len(related)
    for index, item in enumerate(related):
        if isinstance(item, dict) and item.get("href") == "research.html":
            insert_at = index + 1
            break
    related.insert(insert_at, dict(ATLAS_CARD))
    write_json(path, payload)
    return [f"{source_file}:related_guides"]


def run_generators(specs: list[dict[str, Any]]) -> list[str]:
    commands = []
    for spec in specs:
        command = spec.get("generator_command")
        if command and command not in commands:
            commands.append(command)

    ran: list[str] = []
    for command in commands:
        subprocess.run(command.split(), cwd=ROOT, check=True)
        ran.append(command)
    return ran


def render_report(manifest, applied: list[str], generators: list[str], applied_at: str) -> str:
    return f"""# Apply Result: {manifest.run_id}

## Overview

- Summary: {manifest.summary}
- Applied at: `{applied_at}`
- Applied operations: {len(applied)}
- Generator commands: {len(generators)}
- Status after apply: `applied_pending_qa`

## Safety Rule

- Only approved Patch Spec v1 entries were considered.
- Generated research pages were changed through JSON source files and regenerated.
- This is still not a production publish step.

## Applied Operations

{md_list(applied)}

## Generator Commands

{md_list(generators)}
"""


def apply_approved(path: Path):
    manifest = load_run_manifest(path)
    specs = approved_specs(manifest)
    if not specs:
        raise ValueError("No approved Patch Spec v1 entries found.")

    grouped: dict[str, list[dict[str, Any]]] = {}
    for spec in specs:
        grouped.setdefault(str(spec.get("source_of_truth_file")), []).append(spec)

    applied: list[str] = []
    generated_specs: list[dict[str, Any]] = []
    for source_file, source_specs in grouped.items():
        if source_file == TARGET_ATLAS:
            applied.extend(apply_research_costs(source_specs))
            continue
        for spec in source_specs:
            operation = spec.get("operation_type")
            source_type = spec.get("source_type")
            if operation != "internal_link_addition":
                continue
            if source_type == "generated_research_branch":
                applied.extend(add_json_related_guide(source_file))
                generated_specs.append(spec)
            elif source_type == "html_file":
                applied.extend(add_html_related_card(source_file))

    generators = run_generators(generated_specs)
    applied_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    out_path = REPORTS_DIR / f"{manifest.run_id}.apply-result.md"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_report(manifest, applied, generators, applied_at), encoding="utf-8")

    manifest.artifacts.setdefault("apply_result", {})
    manifest.artifacts["apply_result"] = {
        "report_path": str(out_path.relative_to(ROOT)),
        "applied_at": applied_at,
        "applied_operations": applied,
        "generator_commands": generators,
    }
    manifest.status = "applied_pending_qa"
    write_run_manifest(path, manifest)
    return out_path, applied, generators


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply approved Patch Spec v1 entries with safe templates.")
    parser.add_argument("manifest", help="Manifest path or basename without .json")
    args = parser.parse_args()

    manifest_path = resolve_manifest_path(args.manifest)
    try:
        out_path, applied, generators = apply_approved(manifest_path)
    except ValueError as exc:
        print(str(exc))
        return 1

    print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f"Applied operations: {len(applied)}")
    print(f"Generator commands: {len(generators)}")
    print(f"Updated {manifest_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
