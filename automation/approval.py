#!/usr/bin/env python3
"""Record human approval decisions for rendered Patch Spec v1 proposals."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_run_manifest, write_run_manifest
from automation.proposal_renderer import render_proposal, resolve_manifest_path


ALLOWED_STATES = {"proposed", "approved", "rejected"}
TERMINAL_STATES = {"approved", "rejected"}


def spec_key(spec: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(spec.get("source_of_truth_file", "")),
        str(spec.get("output_file", "")),
        str(spec.get("operation_type", "")),
    )


def matches_filters(spec: dict[str, Any], args: argparse.Namespace) -> bool:
    if args.all:
        return True
    if args.source and spec.get("source_of_truth_file") != args.source:
        return False
    if args.target and spec.get("output_file") != args.target:
        return False
    if args.operation and spec.get("operation_type") != args.operation:
        return False
    return True


def compute_status(states: list[str], current_status: str) -> str:
    if not states:
        return current_status
    if all(state == "proposed" for state in states):
        return "proposal_ready"
    if all(state == "approved" for state in states):
        return "approved_for_apply"
    if all(state == "rejected" for state in states):
        return "rejected"
    if any(state in TERMINAL_STATES for state in states):
        return "partially_approved"
    return current_status


def update_spec(spec: dict[str, Any], state: str, note: str | None, timestamp: str) -> None:
    spec["approval_state"] = state
    spec["approval_updated_at"] = timestamp
    if note:
        spec["approval_note"] = note


def cmd_approval(args: argparse.Namespace) -> int:
    if not args.all and not any([args.source, args.target, args.operation]):
        print("Refusing to update every spec implicitly. Pass --all or at least one filter.")
        return 1

    manifest_path = resolve_manifest_path(args.run_id)
    if not manifest_path.exists():
        print(f"Run manifest not found: {manifest_path.relative_to(ROOT)}")
        return 1

    manifest = load_run_manifest(manifest_path)
    artifacts = manifest.artifacts or {}
    proposal = artifacts.get("proposal", {})
    patch_plan = artifacts.get("patch_plan", {})
    rendered_specs = proposal.get("rendered_specs", [])
    patch_specs = patch_plan.get("patch_specs", [])

    if not rendered_specs:
        print("No rendered proposal specs found. Run `python3 automation/pipeline.py propose <run_id>` first.")
        return 1

    matched_keys: set[tuple[str, str, str]] = set()
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    for spec in rendered_specs:
        if matches_filters(spec, args):
            matched_keys.add(spec_key(spec))
            if not args.dry_run:
                update_spec(spec, args.state, args.note, timestamp)

    if not matched_keys:
        print("No proposal specs matched the provided filters.")
        return 1

    if not args.dry_run:
        for spec in patch_specs:
            if spec_key(spec) in matched_keys:
                update_spec(spec, args.state, args.note, timestamp)

        states = [str(spec.get("approval_state") or "proposed") for spec in rendered_specs]
        manifest.status = compute_status(states, manifest.status)
        artifacts["proposal"] = proposal
        artifacts["patch_plan"] = patch_plan
        manifest.artifacts = artifacts
        write_run_manifest(manifest_path, manifest)
        render_proposal(manifest_path)

    action = "Would update" if args.dry_run else "Updated"
    print(
        f"{action} {len(matched_keys)} proposal spec(s) in {manifest_path.relative_to(ROOT)} "
        f"to approval_state={args.state}."
    )
    if args.dry_run:
        print("Dry run only; manifest and proposal report were not changed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Record approval decisions for proposal specs.")
    parser.add_argument("run_id", help="Run manifest basename without .json, or path to a manifest JSON file.")
    parser.add_argument("--state", required=True, choices=sorted(ALLOWED_STATES), help="Approval state to write.")
    parser.add_argument("--source", help="Only update specs for this source_of_truth_file.")
    parser.add_argument("--target", help="Only update specs for this output_file.")
    parser.add_argument("--operation", help="Only update specs for this operation_type.")
    parser.add_argument("--all", action="store_true", help="Update every rendered proposal spec.")
    parser.add_argument("--note", help="Optional human review note to store with matched specs.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing files.")
    return parser


def main() -> int:
    return cmd_approval(build_parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
