#!/usr/bin/env python3
"""Create a planned run manifest from an approved Worker run-plan proposal."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import run_manifest_from_dict, write_run_manifest


REPORTS_DIR = ROOT / "automation" / "reports"
MANIFESTS_DIR = ROOT / "automation" / "manifests"


REQUIRED_MANIFEST_FIELDS = {
    "run_id",
    "created_at",
    "run_type",
    "status",
    "risk_level",
    "summary",
    "inputs",
    "plan",
    "artifacts",
    "changed_files",
    "checks",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def infer_run_plan_path(value: str | None, topic_id: str | None) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else ROOT / path
    if not topic_id:
        raise ValueError("Either --run-plan or --topic-id is required.")
    return REPORTS_DIR / f"worker-run-plan-{topic_id}.json"


def validate_run_plan(run_plan: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    if run_plan.get("state") != "run_plan_ready":
        errors.append(f"Run-plan state is `{run_plan.get('state')}`; expected `run_plan_ready`.")

    manifest = run_plan.get("proposed_manifest")
    if not isinstance(manifest, dict):
        errors.append("Run-plan does not contain a proposed_manifest object.")
        return {}, errors

    missing = sorted(REQUIRED_MANIFEST_FIELDS - set(manifest))
    if missing:
        errors.append("Proposed manifest is missing required fields: " + ", ".join(missing))

    if manifest.get("status") != "planned":
        errors.append(f"Proposed manifest status is `{manifest.get('status')}`; expected `planned`.")
    if manifest.get("changed_files") not in ([], None):
        errors.append("Proposed manifest must not declare changed_files at creation time.")
    if manifest.get("checks") not in ({}, None):
        errors.append("Proposed manifest must not declare check results at creation time.")

    try:
        run_manifest_from_dict(manifest)
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"Proposed manifest does not match RunManifest schema: {exc}")

    return manifest, errors


def build_manifest_payload(manifest: dict[str, Any], run_plan_path: Path, created_by: str | None) -> dict[str, Any]:
    payload = json.loads(json.dumps(manifest))
    artifacts = payload.setdefault("artifacts", {})
    artifacts["worker_run_plan"] = rel(run_plan_path)
    artifacts["worker_manifest_writer"] = {
        "created_at": now_utc(),
        "created_by": created_by or "",
        "safety": "Created planned run manifest only; no content files were modified.",
    }
    payload["changed_files"] = []
    payload["checks"] = {}
    payload["review"] = None
    return payload


def write_manifest(
    run_plan_path: Path,
    manifest_dir: Path,
    created_by: str | None,
    dry_run: bool,
) -> tuple[int, dict[str, Any]]:
    run_plan = load_json(run_plan_path)
    manifest, errors = validate_run_plan(run_plan)
    if errors:
        return 1, {
            "state": "blocked",
            "run_plan_path": rel(run_plan_path),
            "errors": errors,
            "manifest_path": None,
            "dry_run": dry_run,
        }

    payload = build_manifest_payload(manifest, run_plan_path, created_by)
    run_id = str(payload["run_id"])
    manifest_path = manifest_dir / f"{run_id}.json"

    if manifest_path.exists():
        return 1, {
            "state": "blocked",
            "run_id": run_id,
            "run_plan_path": rel(run_plan_path),
            "errors": [f"Manifest already exists: {rel(manifest_path)}"],
            "manifest_path": rel(manifest_path),
            "dry_run": dry_run,
        }

    if dry_run:
        return 0, {
            "state": "dry_run_ready",
            "run_id": run_id,
            "run_plan_path": rel(run_plan_path),
            "errors": [],
            "manifest_path": rel(manifest_path),
            "dry_run": dry_run,
        }

    manifest_dir.mkdir(parents=True, exist_ok=True)
    write_run_manifest(manifest_path, run_manifest_from_dict(payload))
    return 0, {
        "state": "manifest_created",
        "run_id": run_id,
        "run_plan_path": rel(run_plan_path),
        "errors": [],
        "manifest_path": rel(manifest_path),
        "dry_run": dry_run,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a planned run manifest from an approved Worker run-plan proposal.")
    parser.add_argument("--run-plan", help="Path to worker-run-plan-<topic_id>.json.")
    parser.add_argument("--topic-id", help="Topic id used to infer the default run-plan path.")
    parser.add_argument("--manifest-dir", default=str(MANIFESTS_DIR), help="Directory where the manifest should be written.")
    parser.add_argument("--created-by", help="Human operator name or handle for the manifest writer artifact.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and report the manifest path without writing.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    run_plan_path = infer_run_plan_path(args.run_plan, args.topic_id)
    manifest_dir = Path(args.manifest_dir)
    if not manifest_dir.is_absolute():
        manifest_dir = ROOT / manifest_dir

    code, summary = write_manifest(run_plan_path, manifest_dir, args.created_by, args.dry_run)
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        if summary.get("run_id"):
            print(f"Run: {summary['run_id']}")
        if summary.get("manifest_path"):
            print(f"Manifest: {summary['manifest_path']}")
        if summary.get("errors"):
            print("Errors:")
            for error in summary["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
