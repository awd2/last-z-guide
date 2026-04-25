#!/usr/bin/env python3
"""Export a human-readable review bundle from a run manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_run_manifest


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


def build_bundle(manifest) -> str:
    plan = manifest.plan or {}
    inputs = manifest.inputs or {}
    review = manifest.review
    review_context = (manifest.artifacts or {}).get("review_context", {})
    canonical_claim_ids = review_context.get("canonical_claim_ids", [])
    related_filenames = review_context.get("related_filenames", plan.get("related_pages", []))

    checks = []
    for name, result in manifest.checks.items():
        checks.append(f"{name}: {result.status}" + (f" — {result.notes}" if result.notes else ""))

    return f"""# Review Bundle: {manifest.run_id}

## Overview

- Summary: {manifest.summary}
- Status: `{manifest.status}`
- Risk: `{manifest.risk_level}`
- Run type: `{manifest.run_type}`

## Inputs

- Topic ID: `{inputs.get("topic_id", "")}`
- Title: {inputs.get("title", "")}
- Cluster: `{inputs.get("cluster", "")}`
- Source type: `{inputs.get("source_type", "")}`
- Source reference: {inputs.get("source_reference", "")}
- Confidence: `{inputs.get("confidence", "")}`
- Priority: `{inputs.get("priority", "")}`

## Plan

- Target: `{plan.get("target_page_or_slug", "")}`
- Recommended action: `{plan.get("recommended_action", "")}`
- Archetype: `{plan.get("archetype_suggestion", "")}`
- Plan summary: {plan.get("plan_summary", "")}

### Memory Files To Consult

{md_list(plan.get("memory_files", []))}

### Related Pages

{md_list(related_filenames)}

### Deterministic Checks

{md_list(plan.get("deterministic_checks", []))}

## Review Context

### Canonical Claims To Respect

{md_list(canonical_claim_ids)}

## Reviewer Scaffold

- Verdict: `{review.verdict if review else ""}`
- Next action: `{review.next_action if review else ""}`

### Open Questions

{md_list(review.open_questions if review else [])}

### Reviewer Notes

{review.reviewer_notes if review else "No reviewer notes."}

## Existing Check Results

{md_list(checks)}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a markdown review bundle from a run manifest.")
    parser.add_argument("manifest", help="Manifest path or basename without .json")
    args = parser.parse_args()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = resolve_manifest_path(args.manifest)
    manifest = load_run_manifest(manifest_path)

    out_path = REPORTS_DIR / f"{manifest.run_id}.md"
    out_path.write_text(build_bundle(manifest), encoding="utf-8")

    print(f"Wrote {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
