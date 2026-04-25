#!/usr/bin/env python3
"""Proposal-only patch planner for the automation MVP."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_canonical_claims, load_run_manifest, write_run_manifest
from automation.source_resolver import resolve_source


REPORTS_DIR = ROOT / "automation" / "reports"
MANIFESTS_DIR = ROOT / "automation" / "manifests"


def resolve_manifest_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or path.suffix == ".json":
        return path if path.is_absolute() else ROOT / path
    return MANIFESTS_DIR / f"{value}.json"


def md_list(items: list[str]) -> str:
    if not items:
        return "- None"
    return "\n".join(f"- {item}" for item in items)


def claim_lookup() -> dict[str, object]:
    return {claim.id: claim for claim in load_canonical_claims()}


def propose_change_types(manifest) -> list[dict[str, object]]:
    plan = manifest.plan or {}
    inputs = manifest.inputs or {}
    target = plan.get("target_page_or_slug", "")
    archetype = plan.get("archetype_suggestion", "")
    related_pages = (manifest.artifacts or {}).get("review_context", {}).get(
        "related_filenames", plan.get("related_pages", [])
    )

    proposals: list[dict[str, object]] = []

    if target:
        proposals.append(
            {
                "file": target,
                "change_type": "first_screen_update",
                "reason": "Align the opening answer with the run summary, target intent, and cluster role.",
            }
        )
        proposals.append(
            {
                "file": target,
                "change_type": "meta_refresh",
                "reason": "Tighten title/meta/H1 alignment around the page’s exact search intent.",
            }
        )

    if archetype in {"atlas-page", "support-guide", "cornerstone-guide"} and target:
        proposals.append(
            {
                "file": target,
                "change_type": "internal_link_addition",
                "reason": "Strengthen routing between the target page and adjacent cluster pages.",
            }
        )

    if archetype == "atlas-page" and target:
        proposals.append(
            {
                "file": target,
                "change_type": "atlas_card_update",
                "reason": "Adjust atlas cards or route blocks to improve cluster navigation and page choice.",
            }
        )

    for page in related_pages[:4]:
        if page == target:
            continue
        proposals.append(
            {
                "file": page,
                "change_type": "internal_link_addition",
                "reason": f"Add or strengthen the expected bridge into `{target}` from a related cluster page.",
            }
        )

    unique: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for proposal in proposals:
        key = (str(proposal["file"]), str(proposal["change_type"]))
        if key in seen:
            continue
        seen.add(key)
        unique.append(proposal)
    return unique


def build_patch_specs(
    proposed_changes: list[dict[str, object]],
    canonical_ids: list[str],
    deterministic_checks: list[str],
) -> list[dict[str, object]]:
    specs: list[dict[str, object]] = []
    for proposal in proposed_changes:
        target_file = str(proposal["file"])
        source = resolve_source(target_file)
        validation_commands = [
            check
            for check in deterministic_checks
            if check != "python3 scripts/generate_research_branch.py <data-file-if-applicable>"
        ]
        if source.generator_command and source.generator_command not in validation_commands:
            validation_commands.insert(0, source.generator_command)

        specs.append(
            {
                "target_file": target_file,
                "source_of_truth_file": source.source_of_truth_file,
                "output_file": source.output_file,
                "source_type": source.source_type,
                "is_generated": source.is_generated,
                "generator_command": source.generator_command,
                "operation_type": str(proposal["change_type"]),
                "selector_or_anchor": "manual_review_required",
                "required_preconditions": [
                    source.edit_policy,
                    "Read the target/source file before editing.",
                    "Protect the canonical claims listed on this patch spec.",
                ],
                "proposed_change_summary": str(proposal["reason"]),
                "canonical_claims_to_protect": canonical_ids,
                "validation_commands": validation_commands,
                "human_approval_required": True,
            }
        )
    return specs


def build_patch_plan(manifest) -> tuple[dict[str, object], str]:
    plan = manifest.plan or {}
    inputs = manifest.inputs or {}
    review_context = (manifest.artifacts or {}).get("review_context", {})
    canonical_ids = review_context.get("canonical_claim_ids", [])
    claims = claim_lookup()

    proposed_changes = propose_change_types(manifest)
    changed_files = sorted({str(proposal["file"]) for proposal in proposed_changes})
    deterministic_checks = list(plan.get("deterministic_checks", []))
    for check in [
        "python3 automation/checks/changed_pages_report.py --manifest <run_id>",
        "python3 automation/pipeline.py checks",
    ]:
        if check not in deterministic_checks:
            deterministic_checks.append(check)

    patch_specs = build_patch_specs(proposed_changes, canonical_ids, deterministic_checks)
    source_files = sorted({str(spec["source_of_truth_file"]) for spec in patch_specs})

    patch_plan = {
        "target_page_or_slug": plan.get("target_page_or_slug", ""),
        "archetype_suggestion": plan.get("archetype_suggestion", ""),
        "recommended_action": plan.get("recommended_action", ""),
        "proposed_changes": proposed_changes,
        "patch_specs": patch_specs,
        "changed_files": changed_files,
        "source_files": source_files,
        "canonical_claim_ids": canonical_ids,
        "deterministic_checks": deterministic_checks,
    }

    claim_lines = []
    for claim_id in canonical_ids:
        claim = claims.get(claim_id)
        if claim:
            claim_lines.append(f"- `{claim_id}`: {claim.summary}")
        else:
            claim_lines.append(f"- `{claim_id}`")

    change_lines = []
    for proposal in proposed_changes:
        change_lines.append(
            f"- `{proposal['file']}` -> `{proposal['change_type']}`\n"
            f"  reason: {proposal['reason']}"
        )

    spec_lines = []
    for spec in patch_specs:
        generator = spec["generator_command"] or "None"
        spec_lines.append(
            f"- `{spec['target_file']}` -> `{spec['operation_type']}`\n"
            f"  source: `{spec['source_of_truth_file']}`\n"
            f"  generated: `{str(spec['is_generated']).lower()}`\n"
            f"  generator: `{generator}`\n"
            f"  approval: `required`"
        )

    markdown = f"""# Patch Plan: {manifest.run_id}

## Overview

- Summary: {manifest.summary}
- Status: `{manifest.status}`
- Risk: `{manifest.risk_level}`
- Cluster: `{inputs.get("cluster", "")}`
- Target: `{plan.get("target_page_or_slug", "")}`
- Archetype: `{plan.get("archetype_suggestion", "")}`

## Proposed File Changes

{chr(10).join(change_lines) if change_lines else "- None"}

## Candidate Changed Files

{md_list(changed_files)}

## Source Files To Edit

{md_list(source_files)}

## Patch Spec v1

{chr(10).join(spec_lines) if spec_lines else "- None"}

## Canonical Claims To Protect

{chr(10).join(claim_lines) if claim_lines else "- None"}

## Deterministic Checks To Run After Patch Review

{md_list(deterministic_checks)}

## Notes

- This is a proposal-only artifact.
- No site files were modified by this step.
- Use this plan to decide whether the next step should be manual editing or a low-risk auto-edit worker.
"""
    return patch_plan, markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a proposal-only patch plan from a draft brief run.")
    parser.add_argument("manifest", help="Manifest path or basename without .json")
    args = parser.parse_args()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = resolve_manifest_path(args.manifest)
    manifest = load_run_manifest(manifest_path)

    patch_plan, markdown = build_patch_plan(manifest)
    out_path = REPORTS_DIR / f"{manifest.run_id}.patch.md"
    out_path.write_text(markdown, encoding="utf-8")

    manifest.artifacts.setdefault("patch_plan", {})
    manifest.artifacts["patch_plan"] = patch_plan
    manifest.artifacts["patch_plan"]["report_path"] = str(out_path.relative_to(ROOT))
    manifest.changed_files = list(patch_plan.get("changed_files", []))
    if manifest.status == "draft_brief_ready":
        manifest.status = "patch_plan_ready"
    write_run_manifest(manifest_path, manifest)

    print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f"Updated {manifest_path.relative_to(ROOT)}")
    print(f"Status: {manifest.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
