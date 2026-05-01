#!/usr/bin/env python3
"""No-write Reviewer worker for Scout proposals and Editor briefs."""

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

from automation.io import load_canonical_claims, load_content_index, load_json, write_json
from automation.proposal_renderer import md_list


DEFAULT_PROPOSALS_PATH = ROOT / "automation" / "reports" / "scout-topic-proposals.json"
REPORTS_DIR = ROOT / "automation" / "reports"

HIGH_RISK_ARCHETYPES = {"cornerstone-guide", "home-hub"}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def content_pages() -> dict[str, Any]:
    return {page.filename: page for page in load_content_index()}


def claim_ids() -> set[str]:
    return {claim.id for claim in load_canonical_claims()}


def load_proposal(path: Path, topic_id: str) -> dict[str, Any] | None:
    payload = load_json(path)
    for proposal in payload.get("proposals", []):
        if proposal.get("topic_id") == topic_id:
            return proposal
    return None


def infer_brief_path(value: str | None, topic_id: str | None) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else ROOT / path
    if not topic_id:
        raise ValueError("Either --brief or --topic-id is required.")
    return REPORTS_DIR / f"editor-brief-{topic_id}.json"


def issue(severity: str, text: str, fix: str) -> dict[str, str]:
    return {
        "severity": severity,
        "issue": text,
        "required_fix": fix,
    }


def validate_brief_shape(brief: dict[str, Any]) -> list[dict[str, str]]:
    required = [
        "source_topic_id",
        "target_page_or_slug",
        "page_role",
        "primary_query_family",
        "primary_user_job",
        "first_screen_answer",
        "template_reference",
        "required_sections",
        "internal_links",
        "protected_claims",
        "required_context_before_patch",
        "acceptance_checks",
    ]
    blockers = []
    for key in required:
        if not brief.get(key):
            blockers.append(issue("high", f"Editor brief is missing `{key}`.", f"Regenerate or revise the brief with `{key}` populated."))
    return blockers


def validate_target_page(brief: dict[str, Any], proposal: dict[str, Any] | None) -> list[dict[str, str]]:
    blockers = []
    pages = content_pages()
    target = brief.get("target_page_or_slug", "")
    page = pages.get(target)
    action = proposal.get("recommended_action") if proposal else "update_existing"

    if action == "update_existing" and not page:
        blockers.append(issue("high", f"Target page `{target}` is not in content_index.json.", "Update content_index.json or choose a real existing target page."))
    if page and page.status == "archived-noindex":
        blockers.append(issue("high", f"Target page `{target}` is archived/noindex.", "Do not route LLM worker edits into archived pages."))
    if page and brief.get("page_role") != page.archetype:
        blockers.append(issue("high", f"Brief page_role `{brief.get('page_role')}` does not match content index archetype `{page.archetype}`.", "Revise the brief to preserve the indexed page archetype."))
    if proposal and page and proposal.get("cluster") != page.cluster:
        blockers.append(issue("high", f"Scout cluster `{proposal.get('cluster')}` does not match content index cluster `{page.cluster}`.", "Resolve cluster ownership before writing any patch plan."))
    return blockers


def validate_links_and_context(brief: dict[str, Any]) -> tuple[list[dict[str, str]], list[str]]:
    blockers = []
    warnings = []
    links = brief.get("internal_links", {})
    context = brief.get("required_context_before_patch", [])
    target = brief.get("target_page_or_slug", "")

    if target and target not in context:
        blockers.append(issue("high", f"Required context does not include target page `{target}`.", "Add the target page to required_context_before_patch."))
    if not links.get("upstream"):
        warnings.append("Brief has no upstream route; human should verify whether this page can be reached from a hub or home route.")
    if not links.get("lateral") and brief.get("page_role") not in {"home-hub", "site-page"}:
        warnings.append("Brief has no lateral same-cluster pages; check for weak cluster routing or a possible cluster ownership issue.")
    for path in [
        "AGENTS.md",
        "automation/memory/site_style_guide.md",
        "automation/memory/page_archetypes.md",
        "automation/memory/seo_llm_optimization.md",
        "automation/memory/canonical_claims.json",
    ]:
        if path not in context:
            blockers.append(issue("medium", f"Required context is missing `{path}`.", "Include the core instruction and memory file before patch planning."))
    return blockers, warnings


def validate_claims(brief: dict[str, Any]) -> list[dict[str, str]]:
    blockers = []
    known_claims = claim_ids()
    do_not_change = "\n".join(brief.get("do_not_change", []))
    for claim_id in brief.get("protected_claims", []):
        if claim_id not in known_claims:
            blockers.append(issue("medium", f"Unknown protected claim `{claim_id}`.", "Remove the bad claim id or add the claim to canonical_claims.json intentionally."))
        if claim_id not in do_not_change:
            blockers.append(issue("medium", f"Protected claim `{claim_id}` is not represented in do_not_change.", "Make the claim protection explicit in the brief."))
    return blockers


def validate_checks(brief: dict[str, Any]) -> list[dict[str, str]]:
    checks = set(brief.get("acceptance_checks", []))
    blockers = []
    if "python3 scripts/prepublish_check.py" not in checks:
        blockers.append(issue("medium", "Acceptance checks omit prepublish_check.", "Add `python3 scripts/prepublish_check.py`."))
    if "python3 automation/pipeline.py checks --strict" not in checks:
        blockers.append(issue("medium", "Acceptance checks omit strict automation checks.", "Add `python3 automation/pipeline.py checks --strict`."))
    return blockers


def review_warnings(brief: dict[str, Any], proposal: dict[str, Any] | None) -> list[str]:
    warnings = []
    role = brief.get("page_role", "")
    risk = proposal.get("risk_level") if proposal else None
    if role in HIGH_RISK_ARCHETYPES:
        warnings.append("Target is a cornerstone/home archetype; require explicit human approval before any patch plan or apply step.")
    if risk == "high":
        warnings.append("Scout marked this opportunity as high risk; analytics should guide review, not force a rewrite.")
    if proposal and proposal.get("recommended_action") == "create_new":
        warnings.append("New indexable page creation requires human approval and stronger duplicate-intent review.")
    if brief.get("current_page_snapshot", {}).get("quick_answer") and "Preserve the existing answer-first shape" in brief.get("first_screen_answer", ""):
        warnings.append("Brief intentionally preserves the current first-screen pattern; patch planning should be narrow.")
    return warnings


def risk_level(brief: dict[str, Any], proposal: dict[str, Any] | None, blockers: list[dict[str, str]]) -> str:
    if any(item["severity"] == "high" for item in blockers):
        return "high"
    if proposal and proposal.get("risk_level") in {"high", "medium"}:
        return proposal["risk_level"]
    if brief.get("page_role") in HIGH_RISK_ARCHETYPES:
        return "high"
    if brief.get("protected_claims"):
        return "medium"
    return "low"


def verdict_for(blockers: list[dict[str, str]], warnings: list[str], risk: str) -> tuple[str, str]:
    if any(item["severity"] == "high" for item in blockers):
        return "revise", "none"
    if blockers:
        return "needs_human_review", "brief"
    if risk == "high" or warnings:
        return "needs_human_review", "patch_plan"
    return "pass", "patch_plan"


def build_review(brief: dict[str, Any], proposal: dict[str, Any] | None, brief_path: Path, proposals_path: Path) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    warnings: list[str] = []
    blockers.extend(validate_brief_shape(brief))
    blockers.extend(validate_target_page(brief, proposal))
    link_blockers, link_warnings = validate_links_and_context(brief)
    blockers.extend(link_blockers)
    warnings.extend(link_warnings)
    blockers.extend(validate_claims(brief))
    blockers.extend(validate_checks(brief))
    warnings.extend(review_warnings(brief, proposal))

    risk = risk_level(brief, proposal, blockers)
    verdict, next_stage = verdict_for(blockers, warnings, risk)
    required_context = list(dict.fromkeys(brief.get("required_context_before_patch", [])))
    required_checks = list(dict.fromkeys(brief.get("acceptance_checks", [])))

    return {
        "schema_version": 1,
        "report_type": "worker_review",
        "generated_at": now_utc(),
        "source_topic_id": brief.get("source_topic_id", ""),
        "source_brief_file": str(brief_path.relative_to(ROOT) if brief_path.is_relative_to(ROOT) else brief_path),
        "source_proposal_file": str(proposals_path.relative_to(ROOT) if proposals_path.is_relative_to(ROOT) else proposals_path),
        "target_page_or_slug": brief.get("target_page_or_slug", ""),
        "verdict": verdict,
        "risk_level": risk,
        "approved_next_stage": next_stage,
        "blocking_issues": blockers,
        "warnings": warnings,
        "required_context_before_edit": required_context,
        "required_checks": required_checks,
        "human_approval_required": True,
    }


def render_markdown(review: dict[str, Any]) -> str:
    issue_lines = [
        f"{item['severity']}: {item['issue']} Required fix: {item['required_fix']}"
        for item in review["blocking_issues"]
    ]
    lines = [
        f"# Worker Review - {review['source_topic_id']}",
        "",
        "## Verdict",
        "",
        f"- Verdict: `{review['verdict']}`",
        f"- Risk: `{review['risk_level']}`",
        f"- Approved next stage: `{review['approved_next_stage']}`",
        f"- Target: `{review['target_page_or_slug']}`",
        f"- Human approval required: `{str(review['human_approval_required']).lower()}`",
        "- Safety: no content, backlog, or manifest files were modified by Reviewer.",
        "",
        "## Blocking Issues",
        "",
        md_list(issue_lines),
        "",
        "## Warnings",
        "",
        md_list(review["warnings"]),
        "",
        "## Required Context Before Edit",
        "",
        md_list([f"`{path}`" for path in review["required_context_before_edit"]]),
        "",
        "## Required Checks",
        "",
        md_list([f"`{check}`" for check in review["required_checks"]]),
        "",
    ]
    return "\n".join(lines)


def write_outputs(review: dict[str, Any], output_dir: Path, basename: str | None) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = basename or f"worker-review-{review['source_topic_id']}"
    json_path = output_dir / f"{name}.json"
    md_path = output_dir / f"{name}.md"
    write_json(json_path, review)
    md_path.write_text(render_markdown(review), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a no-write Reviewer gate artifact from an Editor brief.")
    parser.add_argument("--brief", help="Path to editor-brief-<topic_id>.json.")
    parser.add_argument("--topic-id", help="Topic id used to infer the default brief path.")
    parser.add_argument("--proposals", default=str(DEFAULT_PROPOSALS_PATH), help="Path to scout-topic-proposals.json.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for Reviewer artifacts.")
    parser.add_argument("--basename", help="Output basename without extension.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    brief_path = infer_brief_path(args.brief, args.topic_id)
    proposals_path = Path(args.proposals)
    if not proposals_path.is_absolute():
        proposals_path = ROOT / proposals_path
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    brief = load_json(brief_path)
    topic_id = brief.get("source_topic_id") or args.topic_id
    proposal = load_proposal(proposals_path, topic_id) if topic_id else None
    review = build_review(brief, proposal, brief_path, proposals_path)
    json_path, md_path = write_outputs(review, output_dir, args.basename)

    summary = {
        "source_topic_id": review["source_topic_id"],
        "target_page_or_slug": review["target_page_or_slug"],
        "verdict": review["verdict"],
        "risk_level": review["risk_level"],
        "approved_next_stage": review["approved_next_stage"],
        "json_path": str(json_path.relative_to(ROOT)),
        "markdown_path": str(md_path.relative_to(ROOT)),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Wrote {summary['json_path']}")
        print(f"Wrote {summary['markdown_path']}")
        print(f"Verdict: {summary['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
