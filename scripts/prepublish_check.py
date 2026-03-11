#!/usr/bin/env python3
"""One-command prepublish check for the static site."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def run_step(name: str, command: list[str]) -> int:
    print(f"\n== {name} ==")
    result = subprocess.run(command, cwd=SCRIPT_DIR.parent)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all local site checks before publish.")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="First sync structured data, verification blocks, sitemap/search-index, then run the audit.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings from the page audit too.",
    )
    args = parser.parse_args()

    failures = 0

    if args.fix:
        failures += run_step(
            "Structured Data Sync",
            [sys.executable, str(SCRIPT_DIR / "sync_structured_data.py")],
        )
        failures += run_step(
            "Verification Blocks Sync",
            [sys.executable, str(SCRIPT_DIR / "sync_verification_blocks.py")],
        )

    indexing_cmd = [sys.executable, str(SCRIPT_DIR / "check_site_indexing.py")]
    if args.fix:
        indexing_cmd.append("--fix")
    failures += run_step("Indexing", indexing_cmd)

    audit_cmd = [sys.executable, str(SCRIPT_DIR / "audit_site.py")]
    if args.strict:
        audit_cmd.append("--strict")
    failures += run_step("HTML Audit", audit_cmd)

    if failures:
        print("\nPrepublish check failed.")
        return 1

    print("\nPrepublish check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
