#!/usr/bin/env python3
"""Close a QA-passed automation run with a final handoff summary."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_run_manifest, write_run_manifest
from automation.proposal_renderer import REPORTS_DIR, md_list, resolve_manifest_path


def check_lines(manifest) -> list[str]:
    lines = []
    for name, result in manifest.checks.items():
        suffix = f" -- {result.notes}" if result.notes else ""
        lines.append(f"{name}: {result.status}{suffix}")
    return lines


def render_close_report(manifest, closed_at: str, note: str) -> str:
    artifacts = manifest.artifacts or {}
    apply_result = artifacts.get("apply_result", {})
    applied_operations = apply_result.get("applied_operations", [])
    generator_commands = apply_result.get("generator_commands", [])

    artifact_lines = []
    for label, context_key in [
        ("Review bundle", "review_context"),
        ("Editor brief", "editor"),
        ("Patch plan", "patch_plan"),
        ("Proposal", "proposal"),
        ("Apply preview", "apply_preview"),
        ("Apply result", "apply_result"),
    ]:
        context = artifacts.get(context_key, {})
        path = context.get("report_path") or context.get("brief_path")
        if path:
            artifact_lines.append(f"{label}: `{path}`")

    return f"""# Closed Run: {manifest.run_id}

## Overview

- Summary: {manifest.summary}
- Final status: `closed`
- Closed at: `{closed_at}`
- Human note: {note or "No extra note."}

## Applied Scope

{md_list(manifest.changed_files)}

## Applied Operations

{md_list(applied_operations)}

## Generator Commands

{md_list(generator_commands)}

## Check Results

{md_list(check_lines(manifest))}

## Artifacts

{md_list(artifact_lines)}

## Release Rule

- This run is closed locally.
- This is not an autonomous production deployment.
- GitHub Pages deployment remains manual or governed by the repository's normal branch workflow.
"""


def close_run(path: Path, note: str):
    manifest = load_run_manifest(path)
    if manifest.status != "qa_passed":
        raise ValueError(f"Run must be qa_passed before close-run. Current status: {manifest.status}")

    closed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    out_path = REPORTS_DIR / f"{manifest.run_id}.closed.md"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_close_report(manifest, closed_at, note), encoding="utf-8")

    manifest.artifacts.setdefault("closeout", {})
    manifest.artifacts["closeout"] = {
        "report_path": str(out_path.relative_to(ROOT)),
        "closed_at": closed_at,
        "note": note,
    }
    manifest.status = "closed"
    write_run_manifest(path, manifest)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Close a QA-passed run with a final summary artifact.")
    parser.add_argument("manifest", help="Manifest path or basename without .json")
    parser.add_argument("--note", default="", help="Optional human closeout note.")
    args = parser.parse_args()

    manifest_path = resolve_manifest_path(args.manifest)
    try:
        out_path = close_run(manifest_path, args.note)
    except ValueError as exc:
        print(str(exc))
        return 1

    print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f"Updated {manifest_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
