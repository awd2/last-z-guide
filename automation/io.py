#!/usr/bin/env python3
"""I/O helpers for the automation layer."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from automation.models import (
    CanonicalClaim,
    ContentIndexPage,
    RunCheckResult,
    RunManifest,
    RunReview,
    TopicBacklogItem,
)


ROOT = Path(__file__).resolve().parent.parent
AUTOMATION_DIR = ROOT / "automation"
MEMORY_DIR = AUTOMATION_DIR / "memory"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_content_index(path: Path | None = None) -> list[ContentIndexPage]:
    payload = load_json(path or MEMORY_DIR / "content_index.json")
    return [ContentIndexPage(**page) for page in payload.get("pages", [])]


def load_canonical_claims(path: Path | None = None) -> list[CanonicalClaim]:
    payload = load_json(path or MEMORY_DIR / "canonical_claims.json")
    return [CanonicalClaim(**claim) for claim in payload.get("claims", [])]


def load_topic_backlog(path: Path | None = None) -> list[TopicBacklogItem]:
    backlog_path = path or MEMORY_DIR / "topic_backlog.csv"
    with backlog_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [TopicBacklogItem(**row) for row in reader]


def run_manifest_from_dict(payload: dict) -> RunManifest:
    checks = {
        name: RunCheckResult(**result)
        for name, result in payload.get("checks", {}).items()
    }
    review_payload = payload.get("review")
    review = RunReview(**review_payload) if review_payload else None
    return RunManifest(
        run_id=payload["run_id"],
        created_at=payload["created_at"],
        run_type=payload["run_type"],
        status=payload["status"],
        risk_level=payload["risk_level"],
        summary=payload["summary"],
        inputs=payload.get("inputs", {}),
        plan=payload.get("plan", {}),
        artifacts=payload.get("artifacts", {}),
        changed_files=payload.get("changed_files", []),
        checks=checks,
        review=review,
    )


def load_run_manifest(path: Path) -> RunManifest:
    return run_manifest_from_dict(load_json(path))


def run_manifest_to_dict(manifest: RunManifest) -> dict:
    payload = {
        "run_id": manifest.run_id,
        "created_at": manifest.created_at,
        "run_type": manifest.run_type,
        "status": manifest.status,
        "risk_level": manifest.risk_level,
        "summary": manifest.summary,
        "inputs": manifest.inputs,
        "plan": manifest.plan,
        "artifacts": manifest.artifacts,
        "changed_files": manifest.changed_files,
        "checks": {
            name: {"status": result.status, "notes": result.notes}
            for name, result in manifest.checks.items()
        },
    }
    if manifest.review:
        payload["review"] = {
            "verdict": manifest.review.verdict,
            "open_questions": manifest.review.open_questions,
            "next_action": manifest.review.next_action,
            "reviewer_notes": manifest.review.reviewer_notes,
        }
    return payload


def write_run_manifest(path: Path, manifest: RunManifest) -> None:
    write_json(path, run_manifest_to_dict(manifest))
