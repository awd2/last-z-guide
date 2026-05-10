#!/usr/bin/env python3
"""Read the latest no-write LLM worker chain summary for owner review."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_json
from automation.proposal_renderer import md_list


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_GLOB = "llm-worker-chain-*.json"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def latest_chain_path(reports_dir: Path) -> Path:
    candidates = [
        path
        for path in reports_dir.glob(DEFAULT_GLOB)
        if path.is_file() and not path.name.endswith("-request.json") and not path.name.endswith("-result.json")
    ]
    if not candidates:
        raise FileNotFoundError(f"No LLM worker chain summary files found in {rel(reports_dir)}.")
    return max(candidates, key=lambda path: (path.stat().st_mtime, path.name))


def load_stage_response(chain: dict[str, Any], stage_name: str) -> dict[str, Any]:
    result_path = chain.get("stages", {}).get(stage_name, {}).get("result_path")
    if not result_path:
        return {}
    path = resolve_path(str(result_path))
    if not path.exists():
        return {}
    result = load_json(path)
    response = result.get("response_json")
    return response if isinstance(response, dict) else {}


def recommended_operator_action(chain: dict[str, Any], reviewer: dict[str, Any]) -> str:
    if chain.get("state") != "completed":
        return "blocked_review_chain_first"
    verdict = reviewer.get("verdict") or chain.get("review_verdict")
    if reviewer.get("owner_approval_required") or chain.get("owner_approval_required"):
        return "owner_review_required"
    if verdict in {"revise", "reject"}:
        return "revise_or_reject_before_proposal"
    if reviewer.get("approved_next_stage") in {"proposal", "patch_plan"}:
        return "ready_for_proposal_planning"
    return "review_manually"


def build_review(chain_path: Path) -> dict[str, Any]:
    chain = load_json(chain_path)
    editor = load_stage_response(chain, "llm_editor")
    reviewer = load_stage_response(chain, "llm_reviewer")
    exact_replacements = editor.get("exact_replacements", [])
    if not isinstance(exact_replacements, list):
        exact_replacements = []
    return {
        "schema_version": 1,
        "report_type": "llm_latest_owner_review",
        "source_chain_path": rel(chain_path),
        "source_topic_id": chain.get("source_topic_id", ""),
        "target_page_or_slug": chain.get("target_page_or_slug", ""),
        "page_role": chain.get("page_role", ""),
        "state": chain.get("state", ""),
        "provider": chain.get("provider", ""),
        "review_verdict": chain.get("review_verdict"),
        "risk_level": chain.get("risk_level"),
        "approved_next_stage": chain.get("approved_next_stage"),
        "owner_approval_required": chain.get("owner_approval_required"),
        "recommended_operator_action": recommended_operator_action(chain, reviewer),
        "brief_summary": editor.get("brief_summary", ""),
        "first_screen_plan": editor.get("first_screen_plan", ""),
        "exact_replacements_count": len(exact_replacements),
        "exact_replacement_review": reviewer.get("exact_replacement_review", ""),
        "blocking_issues": reviewer.get("blocking_issues", []),
        "warnings": reviewer.get("warnings", []),
        "owner_questions": reviewer.get("owner_questions", []),
        "required_checks": reviewer.get("required_checks", []),
        "next_step": reviewer.get("next_step", ""),
        "stage_artifacts": chain.get("stages", {}),
        "chain_artifacts": chain.get("artifacts", {}),
        "errors": chain.get("errors", []),
        "safety": "Read-only owner review. No content, backlog, manifest, PR, or production files were modified.",
    }


def render_markdown(review: dict[str, Any]) -> str:
    blocking = [
        f"{item.get('severity', '')}: {item.get('issue', '')} Required fix: {item.get('required_fix', '')}"
        for item in review.get("blocking_issues", [])
    ]
    stage_lines = [
        f"{name}: state `{stage.get('state')}`, result `{stage.get('result_path')}`"
        for name, stage in review.get("stage_artifacts", {}).items()
    ]
    lines = [
        f"# LLM Latest Owner Review - {review.get('source_topic_id', '')}",
        "",
        "## Outcome",
        "",
        f"- State: `{review.get('state', '')}`",
        f"- Provider: `{review.get('provider', '')}`",
        f"- Target: `{review.get('target_page_or_slug', '')}`",
        f"- Page role: `{review.get('page_role', '')}`",
        f"- Verdict: `{review.get('review_verdict')}`",
        f"- Risk: `{review.get('risk_level')}`",
        f"- Approved next stage: `{review.get('approved_next_stage')}`",
        f"- Owner approval required: `{str(review.get('owner_approval_required')).lower()}`",
        f"- Draft exact replacements: `{review.get('exact_replacements_count', 0)}`",
        f"- Recommended operator action: `{review.get('recommended_operator_action')}`",
        f"- Source chain: `{review.get('source_chain_path')}`",
        "- Safety: read-only; no content, backlog, manifest, PR, or production files were modified.",
        "",
        "## Stage Artifacts",
        "",
        md_list(stage_lines),
        "",
    ]
    if review.get("errors"):
        lines.extend(["## Chain Errors", "", md_list(review["errors"]), ""])
    lines.extend(
        [
            "## Editor Brief Summary",
            "",
            review.get("brief_summary", ""),
            "",
            "## First-Screen Plan",
            "",
            review.get("first_screen_plan", ""),
            "",
            "## Exact Replacement Review",
            "",
            review.get("exact_replacement_review", ""),
            "",
            "## Blocking Issues",
            "",
            md_list(blocking),
            "",
            "## Warnings",
            "",
            md_list(review.get("warnings", [])),
            "",
            "## Owner Questions",
            "",
            md_list(review.get("owner_questions", [])),
            "",
            "## Required Checks",
            "",
            md_list([f"`{check}`" for check in review.get("required_checks", [])]),
            "",
            "## Next Step",
            "",
            review.get("next_step", ""),
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read the latest no-write LLM worker chain summary.")
    parser.add_argument("--chain", help="Path to a specific llm-worker-chain-<topic_id>.json summary.")
    parser.add_argument("--reports-dir", default=str(REPORTS_DIR), help="Directory to search for LLM worker chain summaries.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable owner review JSON.")
    args = parser.parse_args()

    reports_dir = resolve_path(args.reports_dir)
    chain_path = resolve_path(args.chain) if args.chain else latest_chain_path(reports_dir)
    review = build_review(chain_path)
    if args.json:
        print(json.dumps(review, indent=2))
    else:
        print(render_markdown(review))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
