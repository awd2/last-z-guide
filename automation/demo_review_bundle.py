#!/usr/bin/env python3
"""Run the minimal MVP flow and export a markdown review bundle."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AUTOMATION_DIR = ROOT / "automation"


def run_step(name: str, command: list[str]) -> int:
    print(f"\n== {name} ==")
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the minimal automation MVP flow and export a review bundle.")
    parser.add_argument("topic_id", help="Backlog topic_id to run through the bundle flow.")
    args = parser.parse_args()

    run_id = f"2026-04-22-{args.topic_id}"

    failures = 0
    failures += run_step(
        "Demo Run",
        [sys.executable, str(AUTOMATION_DIR / "demo_run.py"), args.topic_id],
    )
    failures += run_step(
        "Export Review Bundle",
        [sys.executable, str(AUTOMATION_DIR / "export_review_bundle.py"), run_id],
    )

    if failures:
        print("\nDemo review bundle flow failed.")
        return 1

    print("\nDemo review bundle flow passed.")
    print(f"Manifest: automation/manifests/{run_id}.json")
    print(f"Bundle: automation/reports/{run_id}.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
