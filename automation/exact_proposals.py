#!/usr/bin/env python3
"""Render compact owner review for exact Patch Spec proposals."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_run_manifest, write_json
from automation.proposal_renderer import (
    REPORTS_DIR,
    SAFE_EXACT_REPLACE_OPERATION,
    build_rendered_specs,
    rel,
    resolve_manifest_path,
    resolve_path,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fence(value: str, lang: str = "html") -> str:
    marker = "````" if "```" in value else "```"
    return f"{marker}{lang}\n{value}\n{marker}"


def exact_review_items(rendered_specs: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    items: list[dict[str, Any]] = []
    non_exact_count = 0
    for index, spec in enumerate(rendered_specs, start=1):
        if spec.get("operation_type") != SAFE_EXACT_REPLACE_OPERATION:
            non_exact_count += 1
            continue
        old = spec.get("exact_old")
        new = spec.get("exact_new")
        if not isinstance(old, str) or not isinstance(new, str) or not old or not new:
            non_exact_count += 1
            continue
        items.append(
            {
                "index": index,
                "target_file": spec.get("target_file", ""),
                "source_of_truth_file": spec.get("source_of_truth_file", ""),
                "output_file": spec.get("output_file", ""),
                "selector_or_anchor": spec.get("selector_or_anchor", ""),
                "operation_type": SAFE_EXACT_REPLACE_OPERATION,
                "risk_level": spec.get("risk_level") or "medium",
                "approval_state": spec.get("approval_state") or "proposed",
                "human_approval_required": bool(spec.get("human_approval_required", True)),
                "proposed_change_summary": spec.get("proposed_change_summary", ""),
                "exact_old": old,
                "exact_new": new,
                "validation_commands": [str(command) for command in spec.get("validation_commands", [])],
            }
        )
    return items, non_exact_count


def build_exact_review(manifest) -> dict[str, Any]:
    artifacts = manifest.artifacts or {}
    proposal = artifacts.get("proposal", {})
    rendered_specs = proposal.get("rendered_specs") or build_rendered_specs(manifest)
    items, non_exact_count = exact_review_items(rendered_specs)
    plan = manifest.plan or {}
    return {
        "schema_version": 1,
        "report_type": "exact_proposal_owner_review",
        "generated_at": utc_now(),
        "run_id": manifest.run_id,
        "status": manifest.status,
        "summary": manifest.summary,
        "risk_level": manifest.risk_level,
        "target_page_or_slug": plan.get("target_page_or_slug", ""),
        "exact_proposal_count": len(items),
        "non_exact_proposal_count": non_exact_count,
        "items": items,
        "safety": {
            "content_edit": False,
            "manifest_mutation": False,
            "approval_mutation": False,
            "purpose": "Owner review only. This report does not approve, apply, commit, push, or deploy changes.",
        },
    }


def render_markdown(review: dict[str, Any]) -> str:
    lines = [
        f"# Exact Proposals: {review.get('run_id', '')}",
        "",
        "## Overview",
        "",
        f"- Summary: {review.get('summary', '')}",
        f"- Status: `{review.get('status', '')}`",
        f"- Risk: `{review.get('risk_level', '')}`",
        f"- Target: `{review.get('target_page_or_slug', '')}`",
        f"- Exact proposals: `{review.get('exact_proposal_count', 0)}`",
        f"- Non-exact proposals hidden: `{review.get('non_exact_proposal_count', 0)}`",
        "",
        "## Safety",
        "",
        "- This report is owner-review only.",
        "- It does not edit content, mutate the manifest, record approval, commit, push, or deploy.",
        "- Approve only after checking the exact Before / After text below.",
        "",
    ]

    items = review.get("items", [])
    if not items:
        lines.extend(["## No Exact Proposals", "", "No `safe_exact_replace` before/after proposals were found."])
        return "\n".join(lines) + "\n"

    for item in items:
        commands = item.get("validation_commands", [])
        lines.extend(
            [
                f"## {item.get('source_of_truth_file', '')} -> {item.get('selector_or_anchor', '')}",
                "",
                f"- Risk: `{item.get('risk_level', '')}`",
                f"- Approval state: `{item.get('approval_state', '')}`",
                f"- Human approval required: `{str(item.get('human_approval_required', True)).lower()}`",
                f"- Summary: {item.get('proposed_change_summary', '')}",
                "",
                "Before:",
                "",
                fence(str(item.get("exact_old", ""))),
                "",
                "After:",
                "",
                fence(str(item.get("exact_new", ""))),
                "",
                "Required checks:",
                "",
            ]
        )
        if commands:
            lines.extend(f"- `{command}`" for command in commands)
        else:
            lines.append("- No validation commands recorded on this spec.")
        lines.append("")
    return "\n".join(lines)


def render_exact_proposals(path: Path, output_dir: Path = REPORTS_DIR) -> dict[str, Any]:
    manifest = load_run_manifest(path)
    review = build_exact_review(manifest)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{manifest.run_id}.exact-proposals.json"
    markdown_path = output_dir / f"{manifest.run_id}.exact-proposals.md"
    review["report_paths"] = {
        "json": rel(json_path),
        "markdown": rel(markdown_path),
    }
    write_json(json_path, review)
    markdown_path.write_text(render_markdown(review), encoding="utf-8")
    return review


def main() -> int:
    parser = argparse.ArgumentParser(description="Render compact owner review for exact Patch Spec proposals.")
    parser.add_argument("manifest", help="Manifest path or basename without .json")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for exact proposal reports.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    manifest_path = resolve_manifest_path(args.manifest)
    output_dir = resolve_path(args.output_dir)
    review = render_exact_proposals(manifest_path, output_dir)
    if args.json:
        print(json.dumps(review, indent=2, ensure_ascii=False))
    else:
        paths = review["report_paths"]
        print(f"Wrote {paths['markdown']}")
        print(f"Wrote {paths['json']}")
        print(f"Exact proposals: {review['exact_proposal_count']}")
        print(f"Non-exact proposals hidden: {review['non_exact_proposal_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
