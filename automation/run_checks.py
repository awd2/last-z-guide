#!/usr/bin/env python3
"""Run deterministic automation-layer checks."""

from __future__ import annotations

import subprocess
import sys
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AUTOMATION_DIR = ROOT / "automation"


def run_step(name: str, command: list[str]) -> int:
    print(f"\n== {name} ==")
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic automation-layer checks.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on weak-cluster warnings in addition to hard failures.",
    )
    args = parser.parse_args()

    failures = 0

    failures += run_step(
        "Content Index Memory",
        [sys.executable, str(AUTOMATION_DIR / "build_content_index.py")],
    )
    orphan_cmd = [sys.executable, str(AUTOMATION_DIR / "checks" / "orphan_pages.py")]
    if args.strict:
        orphan_cmd.append("--strict")
    failures += run_step(
        "Orphan Pages",
        orphan_cmd,
    )
    failures += run_step(
        "Cluster Links",
        [sys.executable, str(AUTOMATION_DIR / "checks" / "cluster_links.py")],
    )
    seo_cmd = [sys.executable, str(AUTOMATION_DIR / "checks" / "seo_llm_alignment.py")]
    if args.strict:
        seo_cmd.append("--strict")
    failures += run_step(
        "SEO LLM Alignment",
        seo_cmd,
    )

    if failures:
        print("\nAutomation checks failed.")
        return 1

    print("\nAutomation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
