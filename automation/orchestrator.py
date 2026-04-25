#!/usr/bin/env python3
"""Minimal orchestrator for the automation MVP."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import write_run_manifest
from automation.models import RunManifest
from automation.planner import build_change_plan, get_backlog_item


MANIFESTS_DIR = ROOT / "automation" / "manifests"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def build_run_id(topic_id: str, created_at: datetime) -> str:
    stamp = created_at.strftime("%Y-%m-%d")
    return f"{stamp}-{topic_id}"


def build_manifest_for_topic(topic_id: str) -> RunManifest:
    created_at = utc_now()
    item = get_backlog_item(topic_id)
    plan = build_change_plan(item)
    run_id = build_run_id(topic_id, created_at)

    return RunManifest(
        run_id=run_id,
        created_at=created_at.isoformat().replace("+00:00", "Z"),
        run_type=item.recommended_action,
        status="planned",
        risk_level=plan.risk_level,
        summary=plan.plan_summary,
        inputs={
            "topic_id": item.topic_id,
            "title": item.title,
            "cluster": item.cluster,
            "source_type": item.source_type,
            "source_reference": item.source_reference,
            "confidence": item.confidence,
            "priority": item.priority,
            "status": item.status,
        },
        plan=asdict(plan),
        artifacts={
            "memory_files_used": plan.memory_files,
        },
        changed_files=[],
        checks={},
        review=None,
    )


def manifest_path(run_id: str) -> Path:
    return MANIFESTS_DIR / f"{run_id}.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an initial automation run manifest for one backlog topic.")
    parser.add_argument("topic_id", help="Backlog topic_id to orchestrate.")
    parser.add_argument("--stdout", action="store_true", help="Print manifest JSON to stdout as well.")
    args = parser.parse_args()

    manifest = build_manifest_for_topic(args.topic_id)
    path = manifest_path(manifest.run_id)
    write_run_manifest(path, manifest)

    print(f"Wrote {path.relative_to(ROOT)}")
    print(f"Run: {manifest.run_id}")
    print(f"Status: {manifest.status}")
    print(f"Risk: {manifest.risk_level}")

    if args.stdout:
        print(json.dumps(asdict(manifest), indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
