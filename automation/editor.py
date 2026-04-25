#!/usr/bin/env python3
"""Brief-only editor worker for the automation MVP."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_canonical_claims, load_run_manifest, write_run_manifest


REPORTS_DIR = ROOT / "automation" / "reports"
MANIFESTS_DIR = ROOT / "automation" / "manifests"


def resolve_manifest_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or path.suffix == ".json":
        return path if path.is_absolute() else ROOT / path
    return MANIFESTS_DIR / f"{value}.json"


def claim_lookup() -> dict[str, object]:
    return {claim.id: claim for claim in load_canonical_claims()}


def md_list(items: list[str]) -> str:
    if not items:
        return "- None"
    return "\n".join(f"- {item}" for item in items)


def skeleton_for(archetype: str) -> list[str]:
    mapping = {
        "support-guide": [
            "Quick Answer",
            "What the user needs to do first",
            "Common mistake or confusion block",
            "Step-by-step setup or decision path",
            "Related links / next step",
        ],
        "cornerstone-guide": [
            "Quick Answer",
            "Best overall recommendation",
            "Decision framework",
            "Links into narrower support pages",
            "FAQ / related guides",
        ],
        "atlas-page": [
            "Quick Answer",
            "Cluster overview",
            "Comparison grid / card list",
            "Recommended route or progression path",
            "Links into exact pages",
        ],
        "cost-page": [
            "Quick Answer",
            "Summary card",
            "Tree / table / planner block",
            "Key checkpoints",
            "Related guides",
        ],
        "comparison-guide": [
            "Quick Answer",
            "Comparison criteria",
            "Best fit by user need",
            "Tradeoff summary",
            "Related pages",
        ],
        "event-guide": [
            "Quick Answer",
            "Timing / schedule block",
            "Best strategy block",
            "Rewards / value block",
            "Related links",
        ],
    }
    return mapping.get(
        archetype,
        [
            "Quick Answer",
            "Core explanation",
            "Decision or action block",
            "Related links",
        ],
    )


def build_brief(manifest) -> str:
    plan = manifest.plan or {}
    inputs = manifest.inputs or {}
    review = manifest.review
    review_context = (manifest.artifacts or {}).get("review_context", {})
    canonical_ids = review_context.get("canonical_claim_ids", [])
    related_pages = review_context.get("related_filenames", plan.get("related_pages", []))
    archetype = plan.get("archetype_suggestion", "")
    target = plan.get("target_page_or_slug", "")
    checks = plan.get("deterministic_checks", [])

    claims = claim_lookup()
    claim_lines = []
    for claim_id in canonical_ids:
        claim = claims.get(claim_id)
        if claim:
            claim_lines.append(f"- `{claim_id}`: {claim.summary}")
        else:
            claim_lines.append(f"- `{claim_id}`")

    page_goal = (
        f"This run is meant to {plan.get('recommended_action', 'work on')} `{target}` "
        f"inside the `{inputs.get('cluster', '')}` cluster."
    )

    first_screen_guidance = [
        "State the main answer near the top.",
        "Keep the page’s role distinct from neighboring pages in the same cluster.",
        "Use exact game terminology and preserve canonical claims.",
    ]
    if archetype == "support-guide":
        first_screen_guidance.append(
            "Lead with a procedural or decision-first answer rather than a broad explanation."
        )
    if archetype == "atlas-page":
        first_screen_guidance.append(
            "Help users choose the correct detailed page instead of over-expanding the hub."
        )
    if archetype == "cost-page":
        first_screen_guidance.append(
            "Keep totals, thresholds, and structured utility visible before longer prose."
        )

    seo_notes = [
        f"Primary target page: `{target}`",
        f"Archetype: `{archetype}`",
        "Preserve title/H1/meta alignment with the page’s exact user intent.",
        "Strengthen internal routing inside the cluster rather than creating duplicate intent pages.",
    ]

    return f"""# Content Brief: {manifest.run_id}

## Overview

- Summary: {manifest.summary}
- Status: `{manifest.status}`
- Risk: `{manifest.risk_level}`
- Cluster: `{inputs.get("cluster", "")}`
- Archetype: `{archetype}`
- Target: `{target}`

## Page Goal

{page_goal}

## Source Context

- Topic ID: `{inputs.get("topic_id", "")}`
- Title: {inputs.get("title", "")}
- Source type: `{inputs.get("source_type", "")}`
- Source reference: {inputs.get("source_reference", "")}
- Confidence: `{inputs.get("confidence", "")}`
- Priority: `{inputs.get("priority", "")}`

## First-Screen Guidance

{md_list(first_screen_guidance)}

## Canonical Claims To Respect

{chr(10).join(claim_lines) if claim_lines else "- None"}

## Related Pages To Consider

{md_list(related_pages)}

## Suggested Page Skeleton

{md_list(skeleton_for(archetype))}

## SEO / Intent Notes

{md_list(seo_notes)}

## Deterministic Checks To Run Later

{md_list(checks)}

## Reviewer Context

- Verdict: `{review.verdict if review else ""}`
- Next action: `{review.next_action if review else ""}`

### Reviewer Notes

{review.reviewer_notes if review else "No reviewer notes."}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a brief-only editor artifact from a reviewed run manifest.")
    parser.add_argument("manifest", help="Manifest path or basename without .json")
    args = parser.parse_args()

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = resolve_manifest_path(args.manifest)
    manifest = load_run_manifest(path)

    out_path = REPORTS_DIR / f"{manifest.run_id}.brief.md"
    out_path.write_text(build_brief(manifest), encoding="utf-8")

    manifest.artifacts.setdefault("editor", {})
    manifest.artifacts["editor"]["brief_path"] = str(out_path.relative_to(ROOT))
    if manifest.status == "reviewed":
        manifest.status = "draft_brief_ready"
    write_run_manifest(path, manifest)

    print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f"Updated {path.relative_to(ROOT)}")
    print(f"Status: {manifest.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
