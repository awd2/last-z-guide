#!/usr/bin/env python3
"""Render a local-only final review before content-changing apply-approved."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.apply_approved import (  # noqa: E402
    SAFE_EXACT_REPLACE_OPERATION,
    approved_specs,
    exact_replace_texts,
    validate_supported_specs,
)
from automation.io import load_run_manifest, write_json  # noqa: E402
from automation.proposal_renderer import REPORTS_DIR, md_list, rel, resolve_manifest_path  # noqa: E402


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def local_source_path(source_file: str, root: Path) -> Path:
    path = Path(source_file)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe source path: {source_file}")
    resolved = (root / path).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"Source path escapes repository root: {source_file}") from exc
    return resolved


def preview_path_from_manifest(manifest, root: Path = ROOT) -> Path | None:
    report_path = (manifest.artifacts or {}).get("apply_preview", {}).get("report_path")
    if not isinstance(report_path, str) or not report_path:
        return None
    path = Path(report_path)
    return path if path.is_absolute() else root / path


def inspect_safe_exact_replace(spec: dict[str, Any], root: Path) -> dict[str, Any]:
    source_file = str(spec.get("source_of_truth_file") or "")
    selector = str(spec.get("selector_or_anchor") or "exact")
    item: dict[str, Any] = {
        "source_of_truth_file": source_file,
        "output_file": spec.get("output_file"),
        "operation_type": spec.get("operation_type"),
        "selector_or_anchor": selector,
        "status": "blocked",
        "old_count": 0,
        "new_count": 0,
        "errors": [],
        "warnings": [],
    }
    try:
        old, new = exact_replace_texts(spec)
        path = local_source_path(source_file, root)
        if not path.exists():
            item["errors"].append(f"Source file not found: {source_file}")
            return item
        text = path.read_text(encoding="utf-8")
        old_count = text.count(old)
        new_count = text.count(new)
        item["old_count"] = old_count
        item["new_count"] = new_count
        if old_count == 1:
            item["status"] = "ready"
        elif old_count == 0 and new_count == 1:
            item["status"] = "already_applied"
            item["warnings"].append("The approved new text already appears and old text is absent.")
        elif old_count == 0:
            item["status"] = "missing_old"
            item["errors"].append("Approved old text is absent.")
        else:
            item["status"] = "ambiguous_old"
            item["errors"].append(f"Approved old text appears {old_count} times.")
    except ValueError as exc:
        item["errors"].append(str(exc))
    return item


def inspect_spec(spec: dict[str, Any], root: Path) -> dict[str, Any]:
    if spec.get("operation_type") == SAFE_EXACT_REPLACE_OPERATION:
        return inspect_safe_exact_replace(spec, root)
    return {
        "source_of_truth_file": spec.get("source_of_truth_file"),
        "output_file": spec.get("output_file"),
        "operation_type": spec.get("operation_type"),
        "selector_or_anchor": spec.get("selector_or_anchor"),
        "status": "validated_by_apply_engine",
        "old_count": None,
        "new_count": None,
        "errors": [],
        "warnings": [
            "This non-exact operation is validated against deterministic apply-approved support, not by text-count inspection."
        ],
    }


def build_pre_apply_review(manifest_path: Path, root: Path = ROOT, reports_dir: Path = REPORTS_DIR) -> dict[str, Any]:
    manifest = load_run_manifest(manifest_path)
    specs = approved_specs(manifest)
    target_page = str((manifest.plan or {}).get("target_page_or_slug", ""))
    generated_at = utc_now()
    errors: list[str] = []
    warnings: list[str] = []

    if manifest.status != "apply_preview_ready":
        errors.append(f"Manifest status must be apply_preview_ready, got {manifest.status}.")
    if not specs:
        errors.append("No approved Patch Spec v1 entries found.")

    apply_preview_path = preview_path_from_manifest(manifest, root=root)
    if not apply_preview_path:
        errors.append("Manifest has no apply_preview report_path artifact.")
    elif not apply_preview_path.exists():
        errors.append(f"Apply preview report is missing: {rel(apply_preview_path)}")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for spec in specs:
        grouped[str(spec.get("source_of_truth_file") or "")].append(spec)
    try:
        validate_supported_specs(grouped, target_page)
    except ValueError as exc:
        errors.append(str(exc))

    source_checks = [inspect_spec(spec, root) for spec in specs]
    for item in source_checks:
        errors.extend(str(value) for value in item.get("errors", []))
        warnings.extend(str(value) for value in item.get("warnings", []))

    preview_warning_count = 0
    for item in (manifest.artifacts or {}).get("apply_preview", {}).get("preview_items", []):
        if isinstance(item, dict):
            preview_warning_count += len(item.get("warnings") or [])

    state = "blocked" if errors else "ready_for_local_apply_review"
    run_id = manifest.run_id
    local_commands = [
        f"python3 automation/pipeline.py apply-approved {run_id}",
        f"python3 automation/pipeline.py checks --strict --manifest {run_id}",
        f'python3 automation/pipeline.py close-run {run_id} --note "Owner reviewed local output and strict QA passed."',
    ]
    safety = {
        "allows_content_edit": False,
        "runs_apply_approved": False,
        "allows_manifest_mutation": False,
        "allows_pr_creation": False,
        "allows_deploy": False,
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "generated_at": generated_at,
        "state": state,
        "manifest_path": rel(manifest_path),
        "manifest_status": manifest.status,
        "target_page_or_slug": target_page,
        "apply_preview_path": rel(apply_preview_path) if apply_preview_path else None,
        "approved_specs_count": len(specs),
        "preview_warning_count": preview_warning_count,
        "source_check_count": len(source_checks),
        "source_checks": source_checks,
        "errors": errors,
        "warnings": warnings,
        "local_only_next_commands": local_commands,
        "safety": safety,
    }


def render_markdown(review: dict[str, Any]) -> str:
    result = "Ready for local final approval review." if review["state"] != "blocked" else "Blocked."
    check_lines = []
    for item in review.get("source_checks", []):
        counts = ""
        if item.get("old_count") is not None:
            counts = f" old_count={item.get('old_count')}, new_count={item.get('new_count')}"
        check_lines.append(
            "- "
            f"`{item.get('source_of_truth_file')}` "
            f"`{item.get('operation_type')}` "
            f"`{item.get('selector_or_anchor')}`: "
            f"`{item.get('status')}`{counts}"
        )

    safety = review.get("safety", {})
    safety_lines = [f"- `{key}`: `{str(value).lower()}`" for key, value in sorted(safety.items())]

    return f"""# Pre-Apply Review: {review['run_id']}

## Result

- State: `{review['state']}`
- Result: {result}
- Manifest status: `{review['manifest_status']}`
- Target: `{review.get('target_page_or_slug')}`
- Approved specs: {review['approved_specs_count']}
- Source checks: {review['source_check_count']}
- Apply preview warnings: {review['preview_warning_count']}
- Generated at: `{review['generated_at']}`

## Safety

This is a local-only, no-write final review before `apply-approved`.

{chr(10).join(safety_lines)}

## Apply Preview

- Preview report: `{review.get('apply_preview_path') or 'missing'}`

## Source Checks

{chr(10).join(check_lines) if check_lines else "- None"}

## Errors

{md_list([str(value) for value in review.get('errors', [])])}

## Warnings

{md_list([str(value) for value in review.get('warnings', [])])}

## Local Commands After Final Owner Approval

{md_list([f"`{command}`" for command in review.get('local_only_next_commands', [])])}
"""


def write_pre_apply_review(manifest_path: Path, root: Path = ROOT, reports_dir: Path = REPORTS_DIR) -> dict[str, Any]:
    review = build_pre_apply_review(manifest_path, root=root, reports_dir=reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / f"{review['run_id']}.pre-apply-review.json"
    md_path = reports_dir / f"{review['run_id']}.pre-apply-review.md"
    review["report_paths"] = {
        "json": rel(json_path),
        "markdown": rel(md_path),
    }
    write_json(json_path, review)
    md_path.write_text(render_markdown(review), encoding="utf-8")
    return review


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a local-only final review before apply-approved.")
    parser.add_argument("manifest", help="Manifest path or basename without .json")
    parser.add_argument("--json", action="store_true", help="Print the review summary as JSON.")
    args = parser.parse_args()

    manifest_path = resolve_manifest_path(args.manifest)
    review = write_pre_apply_review(manifest_path)
    if args.json:
        print(json.dumps(review, indent=2, ensure_ascii=False))
    else:
        paths = review["report_paths"]
        print(f"State: {review['state']}")
        print(f"Markdown: {paths['markdown']}")
        print(f"JSON: {paths['json']}")
        if review["state"] != "blocked":
            print("Review the report, then run apply-approved only after final owner approval.")
    return 1 if review["state"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
