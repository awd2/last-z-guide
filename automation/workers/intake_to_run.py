#!/usr/bin/env python3
"""Convert an approved worker intake artifact into a no-write run-plan proposal."""

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

from automation.io import load_json, write_json
from automation.proposal_renderer import md_list


REPORTS_DIR = ROOT / "automation" / "reports"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def infer_intake_path(value: str | None, topic_id: str | None) -> Path:
    if value:
        path = Path(value)
        return path if path.is_absolute() else ROOT / path
    if not topic_id:
        raise ValueError("Either --intake or --topic-id is required.")
    return REPORTS_DIR / f"worker-intake-{topic_id}.json"


def build_run_id(topic_id: str, generated_at: str) -> str:
    return f"{generated_at[:10]}-{topic_id}"


def proposed_manifest(intake: dict[str, Any], generated_at: str) -> dict[str, Any]:
    backlog = intake.get("proposed_backlog_item", {})
    topic_id = str(backlog.get("topic_id") or intake.get("source_topic_id", "worker-topic"))
    run_id = build_run_id(topic_id, generated_at)
    target = backlog.get("target_page_or_slug", intake.get("target_page_or_slug", ""))
    return {
        "run_id": run_id,
        "created_at": generated_at,
        "run_type": backlog.get("recommended_action", ""),
        "status": "planned",
        "risk_level": intake.get("risk_level", ""),
        "summary": f"Worker-approved intake for `{target}` from `{intake.get('source_topic_id', '')}`.",
        "inputs": {
            "topic_id": topic_id,
            "title": backlog.get("title", ""),
            "cluster": backlog.get("cluster", ""),
            "source_type": backlog.get("source_type", ""),
            "source_reference": backlog.get("source_reference", ""),
            "confidence": backlog.get("confidence", ""),
            "priority": backlog.get("priority", ""),
            "status": backlog.get("status", ""),
            "approved_by": intake.get("approved_by"),
            "approval_note": intake.get("approval_note"),
        },
        "plan": {
            "topic_id": topic_id,
            "title": backlog.get("title", ""),
            "cluster": backlog.get("cluster", ""),
            "recommended_action": backlog.get("recommended_action", ""),
            "archetype_suggestion": backlog.get("archetype_suggestion", ""),
            "target_page_or_slug": target,
            "source_type": backlog.get("source_type", ""),
            "source_reference": backlog.get("source_reference", ""),
            "confidence": backlog.get("confidence", ""),
            "priority": backlog.get("priority", ""),
            "status": backlog.get("status", ""),
            "risk_level": intake.get("risk_level", ""),
            "plan_summary": f"Prepare a controlled content run for `{target}` from an approved Worker intake artifact.",
            "memory_files": [
                "AGENTS.md",
                "automation/memory/site_style_guide.md",
                "automation/memory/page_archetypes.md",
                "automation/memory/seo_llm_optimization.md",
                "automation/memory/canonical_claims.json",
                "automation/memory/content_index.json",
                "automation/memory/entities.json",
                "automation/memory/release_checklist.md",
            ],
            "related_pages": [target] if target else [],
            "deterministic_checks": [
                "python3 scripts/prepublish_check.py",
                "python3 automation/pipeline.py checks --strict",
            ],
            "notes": backlog.get("notes", ""),
        },
        "artifacts": {
            "worker_intake": "",
            "source_chain": intake.get("source_chain_file", ""),
        },
        "changed_files": [],
        "checks": {},
        "review": None,
    }


def proposal_state(intake: dict[str, Any]) -> tuple[str, list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []
    if intake.get("state") != "approved_for_intake":
        blockers.append(f"Intake state is `{intake.get('state')}`; run-plan proposal requires `approved_for_intake`.")
    if intake.get("blockers"):
        blockers.extend(str(item) for item in intake.get("blockers", []))
    if not blockers and intake.get("risk_level") == "high":
        warnings.append("Approved intake is high risk; later patch planning must stay narrow and human-reviewed.")
    if blockers:
        return "blocked", blockers, warnings
    return "run_plan_ready", blockers, warnings


def build_proposal(intake: dict[str, Any], intake_path: Path) -> dict[str, Any]:
    generated_at = now_utc()
    state, blockers, warnings = proposal_state(intake)
    manifest = proposed_manifest(intake, generated_at) if state == "run_plan_ready" else None
    if manifest:
        manifest["artifacts"]["worker_intake"] = rel(intake_path)
    return {
        "schema_version": 1,
        "report_type": "worker_intake_run_plan",
        "generated_at": generated_at,
        "source_intake_file": rel(intake_path),
        "source_topic_id": intake.get("source_topic_id", ""),
        "target_page_or_slug": intake.get("target_page_or_slug", ""),
        "state": state,
        "blockers": blockers,
        "warnings": warnings,
        "proposed_backlog_item": intake.get("proposed_backlog_item"),
        "proposed_manifest": manifest,
        "next_actions": next_actions_for(state, manifest),
        "safety": "No content, backlog, or manifest files were modified by this run-plan proposal.",
    }


def next_actions_for(state: str, manifest: dict[str, Any] | None) -> list[str]:
    if state == "blocked":
        return [
            "Get explicit human approval through the worker-intake gate first.",
            "Rerun intake-to-run after the intake state is `approved_for_intake`.",
        ]
    run_id = manifest["run_id"] if manifest else "<run_id>"
    return [
        "Review proposed_manifest before creating any actual manifest file.",
        f"If accepted, create `automation/manifests/{run_id}.json` from proposed_manifest.",
        f"Then continue with: python3 automation/pipeline.py review {run_id}",
    ]


def render_markdown(proposal: dict[str, Any]) -> str:
    manifest = proposal.get("proposed_manifest")
    lines = [
        f"# Worker Intake Run Plan - {proposal['source_topic_id']}",
        "",
        "## Status",
        "",
        f"- State: `{proposal['state']}`",
        f"- Target: `{proposal['target_page_or_slug']}`",
        "- Safety: no content, backlog, or manifest files were modified by this run-plan proposal.",
        "",
        "## Blockers",
        "",
        md_list(proposal["blockers"]),
        "",
        "## Warnings",
        "",
        md_list(proposal["warnings"]),
        "",
    ]
    if manifest:
        lines.extend(
            [
                "## Proposed Manifest",
                "",
                f"- Run ID: `{manifest['run_id']}`",
                f"- Status: `{manifest['status']}`",
                f"- Risk: `{manifest['risk_level']}`",
                f"- Summary: {manifest['summary']}",
                f"- Target: `{manifest['plan']['target_page_or_slug']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Next Actions",
            "",
            md_list(proposal["next_actions"]),
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(proposal: dict[str, Any], output_dir: Path, basename: str | None) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    name = basename or f"worker-run-plan-{proposal['source_topic_id']}"
    json_path = output_dir / f"{name}.json"
    md_path = output_dir / f"{name}.md"
    write_json(json_path, proposal)
    md_path.write_text(render_markdown(proposal), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a no-write run-plan proposal from an approved Worker intake artifact.")
    parser.add_argument("--intake", help="Path to worker-intake-<topic_id>.json.")
    parser.add_argument("--topic-id", help="Topic id used to infer the default intake path.")
    parser.add_argument("--output-dir", default=str(REPORTS_DIR), help="Directory for run-plan proposal artifacts.")
    parser.add_argument("--basename", help="Output basename without extension.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    intake_path = infer_intake_path(args.intake, args.topic_id)
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    intake = load_json(intake_path)
    proposal = build_proposal(intake, intake_path)
    json_path, md_path = write_outputs(proposal, output_dir, args.basename)

    summary = {
        "source_topic_id": proposal["source_topic_id"],
        "target_page_or_slug": proposal["target_page_or_slug"],
        "state": proposal["state"],
        "json_path": rel(json_path),
        "markdown_path": rel(md_path),
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Topic: {summary['source_topic_id']}")
        print(f"State: {summary['state']}")
        print(f"Run plan: {summary['markdown_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
