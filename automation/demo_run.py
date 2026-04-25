#!/usr/bin/env python3
"""Run the minimal automation MVP flow for one topic."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.orchestrator import build_manifest_for_topic, manifest_path
from automation.io import write_run_manifest
from automation.reviewer import review_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the minimal automation MVP flow for one backlog topic.")
    parser.add_argument("topic_id", help="Backlog topic_id to run through the MVP flow.")
    args = parser.parse_args()

    manifest = build_manifest_for_topic(args.topic_id)
    path = manifest_path(manifest.run_id)
    write_run_manifest(path, manifest)

    reviewed_manifest = review_manifest(path)

    print(f"Run complete: {reviewed_manifest.run_id}")
    print(f"Manifest: {path.relative_to(ROOT)}")
    print(f"Status: {reviewed_manifest.status}")
    if reviewed_manifest.review:
        print(f"Verdict: {reviewed_manifest.review.verdict}")
        print(f"Next action: {reviewed_manifest.review.next_action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
