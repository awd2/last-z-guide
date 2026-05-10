#!/usr/bin/env python3
"""Deterministic reviewer scaffold for automation runs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_canonical_claims, load_run_manifest, write_run_manifest
from automation.models import RunReview


def manifest_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or path.suffix == ".json":
        return path if path.is_absolute() else ROOT / path
    return ROOT / "automation" / "manifests" / f"{value}.json"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def collect_related_filenames(manifest) -> set[str]:
    filenames = set(manifest.changed_files)
    plan = manifest.plan or {}
    target = plan.get("target_page_or_slug")
    if isinstance(target, str) and target.endswith(".html"):
        filenames.add(Path(target).name)
    for page in plan.get("related_pages", []):
        if isinstance(page, str) and page.endswith(".html"):
            filenames.add(Path(page).name)
    return filenames


def relevant_claims(manifest) -> list[str]:
    plan = manifest.plan or {}
    cluster = plan.get("cluster") or manifest.inputs.get("cluster", "")
    filenames = collect_related_filenames(manifest)
    matched: list[str] = []

    category_map = {
        "Research": {"research", "architecture"},
        "Economy": {"economy", "gift-center", "architecture"},
        "Seasons": {"seasons", "architecture"},
        "Events": {"architecture"},
        "PvP": {"architecture"},
    }
    allowed_categories = category_map.get(cluster, {"architecture"})

    for claim in load_canonical_claims():
        if claim.category not in allowed_categories:
            continue
        if filenames.intersection(claim.related_pages):
            matched.append(claim.id)
    return sorted(set(matched))


def build_open_questions(manifest, matched_claim_ids: list[str]) -> list[str]:
    questions: list[str] = []
    if manifest.risk_level == "high":
        questions.append("Does this run need human approval before any content drafting or merge?")
    if manifest.run_type == "create_new":
        questions.append("Does this topic deserve a new URL, or should it be folded into an existing page or atlas?")
    if not matched_claim_ids:
        questions.append("No canonical claims matched automatically. Should the claim layer be expanded for this topic?")
    return questions


def reviewer_notes(manifest, matched_claim_ids: list[str]) -> str:
    if matched_claim_ids:
        claim_text = ", ".join(matched_claim_ids)
        return (
            "Deterministic review scaffold complete. The run should explicitly respect these canonical claims: "
            f"{claim_text}."
        )
    return (
        "Deterministic review scaffold complete. No canonical claims matched automatically, so this run "
        "should be reviewed carefully before drafting content."
    )


def review_manifest(path: Path):
    manifest = load_run_manifest(path)

    matched_claim_ids = relevant_claims(manifest)
    review = RunReview(
        verdict="needs_human_review",
        open_questions=build_open_questions(manifest, matched_claim_ids),
        next_action="review_human",
        reviewer_notes=reviewer_notes(manifest, matched_claim_ids),
    )

    manifest.review = review
    manifest.status = "reviewed"
    manifest.artifacts.setdefault("review_context", {})
    manifest.artifacts["review_context"]["canonical_claim_ids"] = matched_claim_ids
    manifest.artifacts["review_context"]["related_filenames"] = sorted(collect_related_filenames(manifest))

    write_run_manifest(path, manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a deterministic review scaffold to an automation run manifest.")
    parser.add_argument("manifest", help="Manifest path or manifest basename without .json")
    args = parser.parse_args()

    path = manifest_path(args.manifest)
    manifest = review_manifest(path)
    matched_claim_ids = manifest.artifacts.get("review_context", {}).get("canonical_claim_ids", [])
    review = manifest.review

    print(f"Updated {rel(path)}")
    print(f"Status: {manifest.status}")
    print(f"Verdict: {review.verdict if review else 'unknown'}")
    print(f"Canonical claims: {len(matched_claim_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
