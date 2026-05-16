#!/usr/bin/env python3
"""Single entrypoint for the current automation MVP."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_run_manifest, load_topic_backlog, write_run_manifest
from automation.models import RunCheckResult

AUTOMATION_DIR = ROOT / "automation"
MEMORY_DIR = AUTOMATION_DIR / "memory"
MANIFESTS_DIR = AUTOMATION_DIR / "manifests"
REPORTS_DIR = AUTOMATION_DIR / "reports"


def run_step(name: str, command: list[str]) -> int:
    print(f"\n== {name} ==")
    result = subprocess.run(command, cwd=ROOT)
    return result.returncode


def run_step_capture(name: str, command: list[str]) -> tuple[int, str]:
    print(f"\n== {name} ==")
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    output = (result.stdout or "") + (result.stderr or "")
    print(output, end="" if output.endswith("\n") else "\n")
    return result.returncode, output


def summarize_check_output(output: str) -> str:
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    interesting = [
        line
        for line in lines
        if "passed" in line.lower()
        or "failed" in line.lower()
        or "warning" in line.lower()
        or line.startswith("Checked ")
    ]
    if not interesting:
        interesting = lines[-3:]
    return " | ".join(interesting[-6:])[:800]


def record_check_result(run_id: str, name: str, returncode: int, output: str) -> None:
    manifest_path = AUTOMATION_DIR / "manifests" / f"{run_id}.json"
    if not manifest_path.exists():
        print(f"Manifest not found; could not record check result: {manifest_path.relative_to(ROOT)}")
        return
    manifest = load_run_manifest(manifest_path)
    manifest.checks[name] = RunCheckResult(
        status="pass" if returncode == 0 else "fail",
        notes=summarize_check_output(output),
    )
    write_run_manifest(manifest_path, manifest)
    print(f"Recorded `{name}` in {manifest_path.relative_to(ROOT)}")


def advance_manifest_after_checks(run_id: str, strict: bool, checks_code: int, report_code: int) -> None:
    if not strict or checks_code or report_code:
        return
    manifest_path = AUTOMATION_DIR / "manifests" / f"{run_id}.json"
    if not manifest_path.exists():
        return
    manifest = load_run_manifest(manifest_path)
    if manifest.status != "applied_pending_qa":
        return
    manifest.status = "qa_passed"
    write_run_manifest(manifest_path, manifest)
    print(f"Advanced `{run_id}` to qa_passed.")


def cmd_checks(strict: bool, manifest: str | None) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "run_checks.py")]
    if strict:
        command.append("--strict")
    if manifest:
        code, output = run_step_capture("Automation Checks", command)
        record_check_result(
            manifest,
            "automation_checks_strict" if strict else "automation_checks",
            code,
            output,
        )
        report_cmd = [
            sys.executable,
            str(AUTOMATION_DIR / "checks" / "changed_pages_report.py"),
            "--manifest",
            manifest,
        ]
        report_code, report_output = run_step_capture("Changed Pages Report", report_cmd)
        record_check_result(manifest, "changed_pages_report", report_code, report_output)
        advance_manifest_after_checks(manifest, strict, code, report_code)
        return 1 if code or report_code else 0
    return run_step("Automation Checks", command)


def cmd_plan(topic_id: str, as_json: bool) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "planner.py"), topic_id]
    if as_json:
        command.append("--json")
    return run_step("Plan", command)


def cmd_run(topic_id: str) -> int:
    return run_step(
        "Run",
        [sys.executable, str(AUTOMATION_DIR / "demo_run.py"), topic_id],
    )


def cmd_init_run(topic_id: str) -> int:
    return run_step(
        "Init Run",
        [sys.executable, str(AUTOMATION_DIR / "orchestrator.py"), topic_id],
    )


def cmd_review(run_id: str) -> int:
    return run_step(
        "Review",
        [sys.executable, str(AUTOMATION_DIR / "reviewer.py"), run_id],
    )


def cmd_brief(run_id: str, output_dir: str | None) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "editor.py"), run_id]
    if output_dir:
        command.extend(["--output-dir", output_dir])
    return run_step("Editor Brief", command)


def cmd_patch_plan(run_id: str, output_dir: str | None) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "patch_planner.py"), run_id]
    if output_dir:
        command.extend(["--output-dir", output_dir])
    return run_step("Patch Plan", command)


def cmd_propose(run_id: str, output_dir: str | None) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "proposal_renderer.py"), run_id]
    if output_dir:
        command.extend(["--output-dir", output_dir])
    return run_step("Proposal Renderer", command)


def cmd_approval(
    run_id: str,
    state: str,
    all_specs: bool,
    source: str | None,
    target: str | None,
    operation: str | None,
    note: str | None,
    dry_run: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "approval.py"),
        run_id,
        "--state",
        state,
    ]
    if all_specs:
        command.append("--all")
    if source:
        command.extend(["--source", source])
    if target:
        command.extend(["--target", target])
    if operation:
        command.extend(["--operation", operation])
    if note:
        command.extend(["--note", note])
    if dry_run:
        command.append("--dry-run")
    return run_step("Proposal Approval", command)


def cmd_apply_preview(run_id: str) -> int:
    return run_step(
        "Apply Preview",
        [sys.executable, str(AUTOMATION_DIR / "apply_preview.py"), run_id],
    )


def cmd_apply_approved(run_id: str) -> int:
    return run_step(
        "Apply Approved",
        [sys.executable, str(AUTOMATION_DIR / "apply_approved.py"), run_id],
    )


def cmd_close_run(run_id: str, note: str | None) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "close_run.py"), run_id]
    if note:
        command.extend(["--note", note])
    return run_step("Close Run", command)


def cmd_bundle(topic_id: str) -> int:
    return run_step(
        "Review Bundle",
        [sys.executable, str(AUTOMATION_DIR / "demo_review_bundle.py"), topic_id],
    )


def cmd_bundle_run(run_id: str) -> int:
    return run_step(
        "Bundle Existing Run",
        [sys.executable, str(AUTOMATION_DIR / "export_review_bundle.py"), run_id],
    )


def cmd_worker_chain(
    topic_id: str | None,
    target: str | None,
    limit: int,
    min_impressions: int,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "run_chain.py"),
        "--limit",
        str(limit),
        "--min-impressions",
        str(min_impressions),
    ]
    if topic_id:
        command.extend(["--topic-id", topic_id])
    if target:
        command.extend(["--target", target])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== Worker Chain ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_worker_intake(
    topic_id: str | None,
    chain: str | None,
    approved_by: str | None,
    note: str | None,
    as_json: bool,
) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "workers" / "intake.py")]
    if topic_id:
        command.extend(["--topic-id", topic_id])
    if chain:
        command.extend(["--chain", chain])
    if approved_by:
        command.extend(["--approved-by", approved_by])
    if note:
        command.extend(["--note", note])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== Worker Intake ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_worker_run_plan(
    topic_id: str | None,
    intake: str | None,
    output_dir: str | None,
    basename: str | None,
    as_json: bool,
) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "workers" / "intake_to_run.py")]
    if topic_id:
        command.extend(["--topic-id", topic_id])
    if intake:
        command.extend(["--intake", intake])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== Worker Run Plan ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_worker_manifest(
    topic_id: str | None,
    run_plan: str | None,
    manifest_dir: str | None,
    created_by: str | None,
    dry_run: bool,
    as_json: bool,
) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "workers" / "write_manifest.py")]
    if topic_id:
        command.extend(["--topic-id", topic_id])
    if run_plan:
        command.extend(["--run-plan", run_plan])
    if manifest_dir:
        command.extend(["--manifest-dir", manifest_dir])
    if created_by:
        command.extend(["--created-by", created_by])
    if dry_run:
        command.append("--dry-run")
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== Worker Manifest ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_adapter(
    request: str,
    provider: str,
    fixture: str | None,
    output: str | None,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "llm_adapter.py"),
        "--request",
        request,
        "--provider",
        provider,
    ]
    if fixture:
        command.extend(["--fixture", fixture])
    if output:
        command.extend(["--output", output])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Adapter ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_scout(
    signals: list[str] | None,
    external_proposals: list[str] | None,
    provider: str,
    fixture: str | None,
    output_dir: str | None,
    basename: str | None,
    limit: int,
    min_impressions: int,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "llm_scout.py"),
        "--provider",
        provider,
        "--limit",
        str(limit),
        "--min-impressions",
        str(min_impressions),
    ]
    for signal_path in signals or []:
        command.extend(["--signals", signal_path])
    for proposal_path in external_proposals or []:
        command.extend(["--external-proposals", proposal_path])
    if fixture:
        command.extend(["--fixture", fixture])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Scout ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_candidate_refresh(
    signals: list[str] | None,
    external_proposals: list[str] | None,
    provider: str,
    fixture: str | None,
    output_dir: str | None,
    basename: str | None,
    scout_basename: str | None,
    discovery_basename: str | None,
    limit: int,
    min_impressions: int,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "llm_candidate_refresh.py"),
        "--provider",
        provider,
        "--limit",
        str(limit),
        "--min-impressions",
        str(min_impressions),
    ]
    for signal_path in signals or []:
        command.extend(["--signals", signal_path])
    for proposal_path in external_proposals or []:
        command.extend(["--external-proposals", proposal_path])
    if fixture:
        command.extend(["--fixture", fixture])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if scout_basename:
        command.extend(["--scout-basename", scout_basename])
    if discovery_basename:
        command.extend(["--discovery-basename", discovery_basename])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Candidate Refresh ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_auto_review_queue(
    signals: list[str] | None,
    external_proposals: list[str] | None,
    output_dir: str | None,
    basename: str | None,
    provider: str,
    scout_fixture: str | None,
    editor_fixture: str | None,
    reviewer_fixture: str | None,
    limit: int,
    min_impressions: int,
    max_chains: int,
    include_existing: bool,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "llm_auto_review_queue.py"),
        "--provider",
        provider,
        "--limit",
        str(limit),
        "--min-impressions",
        str(min_impressions),
        "--max-chains",
        str(max_chains),
    ]
    for signal_path in signals or []:
        command.extend(["--signals", signal_path])
    for proposal_path in external_proposals or []:
        command.extend(["--external-proposals", proposal_path])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if scout_fixture:
        command.extend(["--scout-fixture", scout_fixture])
    if editor_fixture:
        command.extend(["--editor-fixture", editor_fixture])
    if reviewer_fixture:
        command.extend(["--reviewer-fixture", reviewer_fixture])
    if include_existing:
        command.append("--include-existing")
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Auto Review Queue ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_external_scout(
    registry: str | None,
    output_dir: str | None,
    basename: str | None,
    include_proposed: bool,
    limit: int,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "external_scout.py"),
        "--limit",
        str(limit),
    ]
    if registry:
        command.extend(["--registry", registry])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if include_proposed:
        command.append("--include-proposed")
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== External Scout ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_external_evidence_refresh(
    external_scout: str | None,
    output_dir: str | None,
    basename: str | None,
    limit: int,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "external_evidence_refresh.py"),
        "--limit",
        str(limit),
    ]
    if external_scout:
        command.extend(["--external-scout", external_scout])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== External Evidence Refresh ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_external_evidence_collect(
    evidence_refresh: str | None,
    output_dir: str | None,
    basename: str | None,
    provider: str,
    limit: int,
    timeout: float,
    max_bytes: int,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "external_evidence_collect.py"),
        "--provider",
        provider,
        "--limit",
        str(limit),
        "--timeout",
        str(timeout),
        "--max-bytes",
        str(max_bytes),
    ]
    if evidence_refresh:
        command.extend(["--evidence-refresh", evidence_refresh])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== External Evidence Collect ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_external_search_collect(
    evidence_refresh: str | None,
    output_dir: str | None,
    basename: str | None,
    provider: str,
    limit: int,
    per_query_results: int,
    proposal_limit: int,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "external_search_collect.py"),
        "--provider",
        provider,
        "--limit",
        str(limit),
        "--per-query-results",
        str(per_query_results),
        "--proposal-limit",
        str(proposal_limit),
    ]
    if evidence_refresh:
        command.extend(["--evidence-refresh", evidence_refresh])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== External Search Collect ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_editor(
    scout_result: str | None,
    scout_request: str | None,
    topic_id: str | None,
    provider: str,
    fixture: str | None,
    output_dir: str | None,
    basename: str | None,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "llm_editor.py"),
        "--provider",
        provider,
    ]
    if scout_result:
        command.extend(["--scout-result", scout_result])
    if scout_request:
        command.extend(["--scout-request", scout_request])
    if topic_id:
        command.extend(["--topic-id", topic_id])
    if fixture:
        command.extend(["--fixture", fixture])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Editor ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_reviewer(
    topic_id: str | None,
    editor_result: str | None,
    editor_request: str | None,
    provider: str,
    fixture: str | None,
    output_dir: str | None,
    basename: str | None,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "llm_reviewer.py"),
        "--provider",
        provider,
    ]
    if topic_id:
        command.extend(["--topic-id", topic_id])
    if editor_result:
        command.extend(["--editor-result", editor_result])
    if editor_request:
        command.extend(["--editor-request", editor_request])
    if fixture:
        command.extend(["--fixture", fixture])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Reviewer ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_worker_chain(
    signals: list[str] | None,
    from_decision: str | None,
    topic_id: str | None,
    provider: str,
    output_dir: str | None,
    basename: str | None,
    scout_basename: str | None,
    editor_basename: str | None,
    reviewer_basename: str | None,
    scout_fixture: str | None,
    editor_fixture: str | None,
    reviewer_fixture: str | None,
    limit: int,
    min_impressions: int,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "llm_worker_chain.py"),
        "--provider",
        provider,
        "--limit",
        str(limit),
        "--min-impressions",
        str(min_impressions),
    ]
    for signal in signals or []:
        command.extend(["--signals", signal])
    if from_decision:
        command.extend(["--from-decision", from_decision])
    if topic_id:
        command.extend(["--topic-id", topic_id])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if scout_basename:
        command.extend(["--scout-basename", scout_basename])
    if editor_basename:
        command.extend(["--editor-basename", editor_basename])
    if reviewer_basename:
        command.extend(["--reviewer-basename", reviewer_basename])
    if scout_fixture:
        command.extend(["--scout-fixture", scout_fixture])
    if editor_fixture:
        command.extend(["--editor-fixture", editor_fixture])
    if reviewer_fixture:
        command.extend(["--reviewer-fixture", reviewer_fixture])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Worker Chain ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_review_latest(
    chain: str | None,
    reports_dir: str | None,
    as_json: bool,
) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "reports" / "llm_review_latest.py")]
    if chain:
        command.extend(["--chain", chain])
    if reports_dir:
        command.extend(["--reports-dir", reports_dir])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Latest Owner Review ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_intake_latest(
    chain: str | None,
    reports_dir: str | None,
    approved_by: str | None,
    note: str | None,
    output_dir: str | None,
    basename: str | None,
    resolve_reviewer_blockers: bool,
    as_json: bool,
) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "workers" / "llm_intake.py")]
    if chain:
        command.extend(["--chain", chain])
    if reports_dir:
        command.extend(["--reports-dir", reports_dir])
    if approved_by:
        command.extend(["--approved-by", approved_by])
    if note:
        command.extend(["--note", note])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if resolve_reviewer_blockers:
        command.append("--resolve-reviewer-blockers")
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Intake Latest ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_topic_discovery(
    scout_result: str | None,
    scout_request: str | None,
    output_dir: str | None,
    basename: str | None,
    as_json: bool,
) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "workers" / "llm_topic_discovery.py")]
    if scout_result:
        command.extend(["--scout-result", scout_result])
    if scout_request:
        command.extend(["--scout-request", scout_request])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Topic Discovery ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_topic_decision(
    discovery: str | None,
    from_decision: str | None,
    topic_id: str | None,
    state: str,
    decided_by: str,
    note: str | None,
    output_dir: str | None,
    basename: str | None,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "llm_topic_decision.py"),
        "--state",
        state,
        "--decided-by",
        decided_by,
    ]
    if topic_id:
        command.extend(["--topic-id", topic_id])
    if discovery:
        command.extend(["--discovery", discovery])
    if from_decision:
        command.extend(["--from-decision", from_decision])
    if note:
        command.extend(["--note", note])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Topic Decision ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_topic_decisions(
    reports_dir: str | None,
    json_output: str | None,
    markdown_output: str | None,
    no_write: bool,
    as_json: bool,
) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "reports" / "llm_topic_decisions.py")]
    if reports_dir:
        command.extend(["--reports-dir", reports_dir])
    if json_output:
        command.extend(["--json-output", json_output])
    if markdown_output:
        command.extend(["--markdown-output", markdown_output])
    if no_write:
        command.append("--no-write")
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Topic Decisions ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_approved_handoffs(
    reports_dir: str | None,
    provider: str,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "reports" / "llm_approved_handoffs.py"),
        "--provider",
        provider,
    ]
    if reports_dir:
        command.extend(["--reports-dir", reports_dir])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Approved Handoffs ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_llm_run_approved_handoffs(
    reports_dir: str | None,
    output_dir: str | None,
    basename: str | None,
    provider: str,
    max_handoffs: int,
    include_current: bool,
    editor_fixture: str | None,
    reviewer_fixture: str | None,
    as_json: bool,
) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "workers" / "llm_run_approved_handoffs.py"),
        "--provider",
        provider,
        "--max-handoffs",
        str(max_handoffs),
    ]
    if reports_dir:
        command.extend(["--reports-dir", reports_dir])
    if output_dir:
        command.extend(["--output-dir", output_dir])
    if basename:
        command.extend(["--basename", basename])
    if include_current:
        command.append("--include-current")
    if editor_fixture:
        command.extend(["--editor-fixture", editor_fixture])
    if reviewer_fixture:
        command.extend(["--reviewer-fixture", reviewer_fixture])
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== LLM Run Approved Handoffs ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_content_seo_opportunities(
    json_output: str | None,
    markdown_output: str | None,
    no_write: bool,
    as_json: bool,
) -> int:
    command = [sys.executable, str(AUTOMATION_DIR / "reports" / "content_seo_opportunities.py")]
    if json_output:
        command.extend(["--json-output", json_output])
    if markdown_output:
        command.extend(["--markdown-output", markdown_output])
    if no_write:
        command.append("--no-write")
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== Content SEO Opportunities ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_bing_report() -> int:
    print("\n== Bing Weekly Report ==", flush=True)
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "bing_weekly.py")], cwd=ROOT).returncode


def cmd_content_voice(top: int, fail_on_high_risk: bool, as_json: bool) -> int:
    command = [
        sys.executable,
        str(AUTOMATION_DIR / "checks" / "content_voice.py"),
        "--top",
        str(top),
    ]
    if fail_on_high_risk:
        command.append("--fail-on-high-risk")
    if as_json:
        command.append("--json")
        return subprocess.run(command, cwd=ROOT).returncode
    print("\n== Content Voice Audit ==", flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def cmd_list(status: str | None, cluster: str | None, priority: str | None, as_json: bool) -> int:
    items = load_topic_backlog()

    if status:
        items = [item for item in items if item.status == status]
    if cluster:
        items = [item for item in items if item.cluster == cluster]
    if priority:
        items = [item for item in items if item.priority == priority]

    if not items:
        if as_json:
            print("[]")
        else:
            print("No backlog items matched the filters.")
        return 0

    rows = [
        {
            "topic_id": item.topic_id,
            "title": item.title,
            "cluster": item.cluster,
            "priority": item.priority,
            "status": item.status,
            "recommended_action": item.recommended_action,
            "target_page_or_slug": item.target_page_or_slug,
        }
        for item in items
    ]

    if as_json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return 0

    print("Backlog Items")
    for item in rows:
        print(
            f"- {item['topic_id']} | cluster={item['cluster']} | priority={item['priority']} | "
            f"status={item['status']} | action={item['recommended_action']} | target={item['target_page_or_slug']}"
        )
        print(f"  title: {item['title']}")
    return 0


def cmd_open_topic(topic_id: str, as_json: bool) -> int:
    items = load_topic_backlog()
    for item in items:
        if item.topic_id != topic_id:
            continue

        payload = {
            "topic_id": item.topic_id,
            "title": item.title,
            "cluster": item.cluster,
            "recommended_action": item.recommended_action,
            "archetype_suggestion": item.archetype_suggestion,
            "target_page_or_slug": item.target_page_or_slug,
            "source_type": item.source_type,
            "source_reference": item.source_reference,
            "confidence": item.confidence,
            "priority": item.priority,
            "status": item.status,
            "notes": item.notes,
        }
        if as_json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return 0

        print(f"Topic: {item.topic_id}")
        print(f"Title: {item.title}")
        print(f"Cluster: {item.cluster}")
        print(f"Recommended action: {item.recommended_action}")
        print(f"Archetype suggestion: {item.archetype_suggestion}")
        print(f"Target page or slug: {item.target_page_or_slug}")
        print(f"Source type: {item.source_type}")
        print(f"Source reference: {item.source_reference}")
        print(f"Confidence: {item.confidence}")
        print(f"Priority: {item.priority}")
        print(f"Status: {item.status}")
        print(f"Notes: {item.notes or '(none)'}")
        return 0

    if as_json:
        print("{}")
    else:
        print(f"Backlog topic not found: {topic_id}")
    return 1


def cmd_backlog_summary(as_json: bool) -> int:
    items = load_topic_backlog()
    if not items:
        if as_json:
            print("{}")
        else:
            print("No backlog items found.")
        return 0

    by_cluster: dict[str, int] = {}
    by_priority: dict[str, int] = {}
    by_status: dict[str, int] = {}

    for item in items:
        by_cluster[item.cluster] = by_cluster.get(item.cluster, 0) + 1
        by_priority[item.priority] = by_priority.get(item.priority, 0) + 1
        by_status[item.status] = by_status.get(item.status, 0) + 1

    payload = {
        "total_items": len(items),
        "by_cluster": dict(sorted(by_cluster.items())),
        "by_priority": dict(sorted(by_priority.items())),
        "by_status": dict(sorted(by_status.items())),
    }

    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print("Backlog Summary")
    print(f"- total items: {payload['total_items']}")

    print("- by cluster:")
    for key, count in payload["by_cluster"].items():
        print(f"  - {key}: {count}")

    print("- by priority:")
    for key, count in payload["by_priority"].items():
        print(f"  - {key}: {count}")

    print("- by status:")
    for key, count in payload["by_status"].items():
        print(f"  - {key}: {count}")
    return 0


def load_run_manifests() -> list:
    manifest_files = sorted(
        [
            path for path in MANIFESTS_DIR.glob("*.json") if path.name != "run_manifest.example.json"
        ],
        key=lambda path: path.name,
    )
    return [load_run_manifest(path) for path in manifest_files]


def lifecycle_group(status: str) -> str:
    if status == "closed":
        return "closed"
    if status in {"qa_passed", "applied_pending_qa", "apply_preview_ready", "approved_for_apply"}:
        return "post_apply"
    if status in {"reviewed", "draft_brief_ready", "patch_plan_ready", "proposal_ready", "partially_approved"}:
        return "active"
    if status == "rejected":
        return "rejected"
    return "planned"


def backlog_sync_rows() -> tuple[list[dict], list[dict]]:
    backlog_items = load_topic_backlog()
    manifests = load_run_manifests()
    manifests_by_topic: dict[str, list] = {}
    for manifest in manifests:
        topic_id = str((manifest.inputs or {}).get("topic_id") or (manifest.plan or {}).get("topic_id") or "")
        if not topic_id:
            continue
        manifests_by_topic.setdefault(topic_id, []).append(manifest)

    rows: list[dict] = []
    for item in backlog_items:
        topic_runs = sorted(
            manifests_by_topic.get(item.topic_id, []),
            key=lambda manifest: manifest.created_at,
            reverse=True,
        )
        latest = topic_runs[0] if topic_runs else None
        latest_status = latest.status if latest else None
        latest_group = lifecycle_group(latest_status) if latest_status else "no_run"

        if latest is None and item.status == "done":
            sync_state = "manual_completed"
            recommendation = "no_action"
        elif latest is None:
            sync_state = "available"
            recommendation = "ready_for_run"
        elif latest.status == "closed" and item.status == "backlog":
            sync_state = "stale_backlog_completed"
            recommendation = "mark_backlog_done_or_remove_from_active_queue"
        elif latest.status == "closed":
            sync_state = "completed"
            recommendation = "no_action"
        elif latest.status == "rejected":
            sync_state = "rejected_run"
            recommendation = "revise_or_reopen_topic"
        else:
            sync_state = "active_run"
            recommendation = f"continue_with_next_step_for_{latest.run_id}"

        rows.append(
            {
                "topic_id": item.topic_id,
                "title": item.title,
                "cluster": item.cluster,
                "priority": item.priority,
                "backlog_status": item.status,
                "target": item.target_page_or_slug,
                "run_count": len(topic_runs),
                "latest_run_id": latest.run_id if latest else None,
                "latest_run_status": latest_status,
                "latest_run_group": latest_group,
                "sync_state": sync_state,
                "recommendation": recommendation,
            }
        )

    backlog_topic_ids = {item.topic_id for item in backlog_items}
    orphan_runs = []
    for manifest in manifests:
        topic_id = str((manifest.inputs or {}).get("topic_id") or (manifest.plan or {}).get("topic_id") or "")
        if topic_id and topic_id in backlog_topic_ids:
            continue
        orphan_runs.append(
            {
                "run_id": manifest.run_id,
                "topic_id": topic_id or None,
                "status": manifest.status,
                "summary": manifest.summary,
            }
        )

    return rows, orphan_runs


def cmd_backlog_sync(as_json: bool) -> int:
    rows, orphan_runs = backlog_sync_rows()
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["sync_state"]] = counts.get(row["sync_state"], 0) + 1

    payload = {
        "total_topics": len(rows),
        "sync_states": dict(sorted(counts.items())),
        "topics": rows,
        "runs_without_backlog_topic": orphan_runs,
    }

    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print("Backlog / Run Sync")
    print(f"- total topics: {payload['total_topics']}")
    if payload["sync_states"]:
        print(
            "- sync states: "
            + ", ".join(f"{state}={count}" for state, count in payload["sync_states"].items())
        )
    for row in rows:
        run = row["latest_run_id"] or "none"
        run_status = row["latest_run_status"] or "none"
        print(
            f"- {row['topic_id']} | backlog={row['backlog_status']} | "
            f"latest_run={run} ({run_status}) | sync={row['sync_state']}"
        )
        print(f"  recommendation: {row['recommendation']}")
    if orphan_runs:
        print("- runs without backlog topic:")
        for run in orphan_runs:
            print(f"  - {run['run_id']} | topic={run['topic_id'] or 'none'} | status={run['status']}")
    return 0


def cmd_open_run(run_id: str, as_json: bool) -> int:
    manifest_path = AUTOMATION_DIR / "manifests" / f"{run_id}.json"
    if not manifest_path.exists():
        print(f"Run manifest not found: {manifest_path.relative_to(ROOT)}")
        return 1

    manifest = load_run_manifest(manifest_path)
    inputs = manifest.inputs or {}
    plan = manifest.plan or {}
    review_context = (manifest.artifacts or {}).get("review_context", {})
    editor_context = (manifest.artifacts or {}).get("editor", {})
    patch_plan_context = (manifest.artifacts or {}).get("patch_plan", {})
    proposal_context = (manifest.artifacts or {}).get("proposal", {})
    apply_preview_context = (manifest.artifacts or {}).get("apply_preview", {})
    apply_result_context = (manifest.artifacts or {}).get("apply_result", {})
    closeout_context = (manifest.artifacts or {}).get("closeout", {})

    bundle_path = AUTOMATION_DIR / "reports" / f"{run_id}.md"
    brief_path_value = editor_context.get("brief_path")
    brief_path = ROOT / brief_path_value if brief_path_value else None
    patch_path_value = patch_plan_context.get("report_path")
    patch_path = ROOT / patch_path_value if patch_path_value else None
    proposal_path_value = proposal_context.get("report_path")
    proposal_path = ROOT / proposal_path_value if proposal_path_value else None
    apply_preview_path_value = apply_preview_context.get("report_path")
    apply_preview_path = ROOT / apply_preview_path_value if apply_preview_path_value else None
    apply_result_path_value = apply_result_context.get("report_path")
    apply_result_path = ROOT / apply_result_path_value if apply_result_path_value else None
    closeout_path_value = closeout_context.get("report_path")
    closeout_path = ROOT / closeout_path_value if closeout_path_value else None

    payload = {
        "run_id": manifest.run_id,
        "status": manifest.status,
        "risk": manifest.risk_level,
        "run_type": manifest.run_type,
        "summary": manifest.summary,
        "created_at": manifest.created_at,
        "changed_files": manifest.changed_files,
        "inputs": inputs,
        "plan": plan,
        "review": {
            "verdict": manifest.review.verdict,
            "next_action": manifest.review.next_action,
            "open_questions": manifest.review.open_questions,
            "reviewer_notes": manifest.review.reviewer_notes,
        }
        if manifest.review
        else None,
        "review_context": review_context,
        "patch_plan_context": patch_plan_context,
        "proposal_context": proposal_context,
        "apply_preview_context": apply_preview_context,
        "apply_result_context": apply_result_context,
        "closeout_context": closeout_context,
        "checks": {
            name: {"status": result.status, "notes": result.notes}
            for name, result in manifest.checks.items()
        },
        "artifacts": {
            "manifest": str(manifest_path.relative_to(ROOT)),
            "review_bundle": str(bundle_path.relative_to(ROOT)) if bundle_path.exists() else None,
            "editor_brief": str(brief_path.relative_to(ROOT)) if brief_path and brief_path.exists() else None,
            "patch_plan": str(patch_path.relative_to(ROOT)) if patch_path and patch_path.exists() else None,
            "proposal": str(proposal_path.relative_to(ROOT)) if proposal_path and proposal_path.exists() else None,
            "apply_preview": str(apply_preview_path.relative_to(ROOT))
            if apply_preview_path and apply_preview_path.exists()
            else None,
            "apply_result": str(apply_result_path.relative_to(ROOT))
            if apply_result_path and apply_result_path.exists()
            else None,
            "closeout": str(closeout_path.relative_to(ROOT)) if closeout_path and closeout_path.exists() else None,
        },
    }

    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print(f"Run: {manifest.run_id}")
    print(f"Status: {manifest.status}")
    print(f"Risk: {manifest.risk_level}")
    print(f"Type: {manifest.run_type}")
    print(f"Summary: {manifest.summary}")
    print(f"Created: {manifest.created_at}")

    if inputs:
        print("\nInputs")
        for key in [
            "topic_id",
            "title",
            "cluster",
            "source_type",
            "source_reference",
            "confidence",
            "priority",
        ]:
            if key in inputs:
                print(f"- {key}: {inputs[key]}")

    if plan:
        print("\nPlan")
        for key, label in [
            ("target_page_or_slug", "target"),
            ("recommended_action", "recommended_action"),
            ("archetype_suggestion", "archetype"),
            ("plan_summary", "plan_summary"),
        ]:
            if key in plan and plan[key]:
                print(f"- {label}: {plan[key]}")
        if plan.get("memory_files"):
            print("- memory_files:")
            for value in plan["memory_files"]:
                print(f"  - {value}")
        if plan.get("related_pages"):
            print("- related_pages:")
            for value in plan["related_pages"]:
                print(f"  - {value}")
        if plan.get("deterministic_checks"):
            print("- deterministic_checks:")
            for value in plan["deterministic_checks"]:
                print(f"  - {value}")

    if manifest.review:
        print("\nReview")
        print(f"- verdict: {manifest.review.verdict}")
        print(f"- next_action: {manifest.review.next_action}")
        if manifest.review.open_questions:
            print("- open_questions:")
            for question in manifest.review.open_questions:
                print(f"  - {question}")
        if manifest.review.reviewer_notes:
            print(f"- reviewer_notes: {manifest.review.reviewer_notes}")

    if review_context:
        print("\nReview Context")
        claim_ids = review_context.get("canonical_claim_ids", [])
        related_filenames = review_context.get("related_filenames", [])
        if claim_ids:
            print("- canonical_claim_ids:")
            for claim_id in claim_ids:
                print(f"  - {claim_id}")
        if related_filenames:
            print("- related_filenames:")
            for filename in related_filenames:
                print(f"  - {filename}")

    if patch_plan_context:
        print("\nPatch Plan Context")
        proposed_changes = patch_plan_context.get("proposed_changes", [])
        if proposed_changes:
            print("- proposed_changes:")
            for proposal in proposed_changes:
                print(
                    f"  - {proposal.get('file')} -> {proposal.get('change_type')} "
                    f"({proposal.get('reason')})"
                )
    if proposal_context:
        print("\nProposal Context")
        rendered_specs = proposal_context.get("rendered_specs", [])
        report_path = proposal_context.get("report_path")
        print(f"- rendered_specs: {len(rendered_specs)}")
        if report_path:
            print(f"- report_path: {report_path}")
    if apply_preview_context:
        print("\nApply Preview Context")
        report_path = apply_preview_context.get("report_path")
        print(f"- approved_specs_count: {apply_preview_context.get('approved_specs_count', 0)}")
        if report_path:
            print(f"- report_path: {report_path}")
    if apply_result_context:
        print("\nApply Result Context")
        report_path = apply_result_context.get("report_path")
        print(f"- applied_operations: {len(apply_result_context.get('applied_operations', []))}")
        print(f"- generator_commands: {len(apply_result_context.get('generator_commands', []))}")
        if report_path:
            print(f"- report_path: {report_path}")
    if closeout_context:
        print("\nCloseout Context")
        report_path = closeout_context.get("report_path")
        print(f"- closed_at: {closeout_context.get('closed_at', '')}")
        if report_path:
            print(f"- report_path: {report_path}")

    if manifest.changed_files:
        print("\nChanged Files")
        for filename in manifest.changed_files:
            print(f"- {filename}")

    if manifest.checks:
        print("\nChecks")
        for name, result in manifest.checks.items():
            suffix = f" — {result.notes}" if result.notes else ""
            print(f"- {name}: {result.status}{suffix}")

    print("\nArtifacts")
    print(f"- manifest: {manifest_path.relative_to(ROOT)}")
    print(f"- review bundle: {bundle_path.relative_to(ROOT) if bundle_path.exists() else 'not generated yet'}")
    print(f"- editor brief: {brief_path.relative_to(ROOT) if brief_path and brief_path.exists() else 'not generated yet'}")
    print(f"- patch plan: {patch_path.relative_to(ROOT) if patch_path and patch_path.exists() else 'not generated yet'}")
    print(f"- proposal: {proposal_path.relative_to(ROOT) if proposal_path and proposal_path.exists() else 'not generated yet'}")
    print(
        f"- apply preview: {apply_preview_path.relative_to(ROOT) if apply_preview_path and apply_preview_path.exists() else 'not generated yet'}"
    )
    print(
        f"- apply result: {apply_result_path.relative_to(ROOT) if apply_result_path and apply_result_path.exists() else 'not generated yet'}"
    )
    print(f"- closeout: {closeout_path.relative_to(ROOT) if closeout_path and closeout_path.exists() else 'not generated yet'}")
    return 0


def cmd_next_step(run_id: str, as_json: bool) -> int:
    manifest_path = AUTOMATION_DIR / "manifests" / f"{run_id}.json"
    if not manifest_path.exists():
        print(f"Run manifest not found: {manifest_path.relative_to(ROOT)}")
        return 1

    manifest = load_run_manifest(manifest_path)
    status = manifest.status

    guidance = {
        "planned": {
            "next_step": f"python3 automation/pipeline.py review {run_id}",
            "recommended_command": f"python3 automation/pipeline.py review {run_id}",
            "requires_human_review": False,
            "requires_manual_edit_gate": False,
            "reason": "The run exists but has not gone through the reviewer scaffold yet.",
        },
        "reviewed": {
            "next_step": f"python3 automation/pipeline.py brief {run_id}",
            "recommended_command": f"python3 automation/pipeline.py brief {run_id}",
            "requires_human_review": False,
            "requires_manual_edit_gate": False,
            "reason": "The run has reviewer context and is ready for a brief-only editor artifact.",
        },
        "draft_brief_ready": {
            "next_step": f"python3 automation/pipeline.py patch-plan {run_id}",
            "recommended_command": f"python3 automation/pipeline.py patch-plan {run_id}",
            "requires_human_review": False,
            "requires_manual_edit_gate": False,
            "reason": "The editor brief exists and the next safe step is a proposal-only patch plan.",
        },
        "patch_plan_ready": {
            "next_step": f"python3 automation/pipeline.py propose {run_id}",
            "recommended_command": f"python3 automation/pipeline.py propose {run_id}",
            "requires_human_review": False,
            "requires_manual_edit_gate": False,
            "reason": "The run has Patch Spec v1 metadata and can render a human-reviewable proposal artifact next.",
        },
        "proposal_ready": {
            "next_step": f"python3 automation/pipeline.py approval {run_id} --state approved --all",
            "recommended_command": None,
            "requires_human_review": True,
            "requires_manual_edit_gate": True,
            "reason": "The run has proposed edits and now needs human review. Approve or reject specs before any apply step.",
        },
        "partially_approved": {
            "next_step": "review_remaining_proposal_specs",
            "recommended_command": None,
            "requires_human_review": True,
            "requires_manual_edit_gate": True,
            "reason": "Some proposal specs have approval decisions, but the run is not fully approved or rejected.",
        },
        "approved_for_apply": {
            "next_step": f"python3 automation/pipeline.py apply-preview {run_id}",
            "recommended_command": f"python3 automation/pipeline.py apply-preview {run_id}",
            "requires_human_review": False,
            "requires_manual_edit_gate": True,
            "reason": "All proposal specs have terminal review decisions and at least one spec is approved. The next safe automation step is a no-write apply preview for approved specs only.",
        },
        "apply_preview_ready": {
            "next_step": f"python3 automation/pipeline.py apply-approved {run_id}",
            "recommended_command": f"python3 automation/pipeline.py apply-approved {run_id}",
            "requires_human_review": True,
            "requires_manual_edit_gate": True,
            "reason": "The run has a no-write apply preview. After review, the controlled apply step may edit approved source files.",
        },
        "applied_pending_qa": {
            "next_step": f"python3 automation/pipeline.py checks --strict --manifest {run_id}",
            "recommended_command": f"python3 automation/pipeline.py checks --strict --manifest {run_id}",
            "requires_human_review": False,
            "requires_manual_edit_gate": True,
            "reason": "Approved specs were applied. Run strict automation checks and prepublish checks before merge/deploy.",
        },
        "qa_passed": {
            "next_step": f"python3 automation/pipeline.py close-run {run_id}",
            "recommended_command": f"python3 automation/pipeline.py close-run {run_id}",
            "requires_human_review": True,
            "requires_manual_edit_gate": True,
            "reason": "Approved specs were applied, strict checks passed, and the result needs a final closeout artifact after human review.",
        },
        "closed": {
            "next_step": "manual_release_decision_or_next_backlog_topic",
            "recommended_command": None,
            "requires_human_review": True,
            "requires_manual_edit_gate": True,
            "reason": "The run is closed locally. Production deployment remains manual; otherwise choose the next backlog topic.",
        },
        "rejected": {
            "next_step": "revise_or_close_run",
            "recommended_command": None,
            "requires_human_review": False,
            "requires_manual_edit_gate": True,
            "reason": "All proposal specs were rejected. Revise the plan before creating any content edits.",
        },
    }

    item = guidance.get(status)
    payload = {
        "run_id": manifest.run_id,
        "status": status,
        "next_step": item["next_step"] if item else "inspect_manually",
        "recommended_command": item["recommended_command"] if item else None,
        "requires_human_review": item["requires_human_review"] if item else True,
        "requires_manual_edit_gate": item["requires_manual_edit_gate"] if item else True,
        "reason": item["reason"] if item else "This status does not have a predefined lifecycle mapping yet.",
    }

    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print(f"Run: {manifest.run_id}")
    print(f"Status: {status}")
    if item:
        print(f"Next step: {item['next_step']}")
        if item["recommended_command"]:
            print(f"Recommended command: {item['recommended_command']}")
        print(f"Requires human review: {'yes' if item['requires_human_review'] else 'no'}")
        print(f"Requires manual edit gate: {'yes' if item['requires_manual_edit_gate'] else 'no'}")
        print(f"Why: {item['reason']}")
    else:
        print("Next step: inspect manually")
        print("Requires human review: yes")
        print("Requires manual edit gate: yes")
        print("Why: This status does not have a predefined lifecycle mapping yet.")
    return 0


def cmd_show(run_id: str, as_json: bool) -> int:
    manifest_path = AUTOMATION_DIR / "manifests" / f"{run_id}.json"
    if not manifest_path.exists():
        print(f"Run manifest not found: {manifest_path.relative_to(ROOT)}")
        return 1

    manifest = load_run_manifest(manifest_path)
    review_context = (manifest.artifacts or {}).get("review_context", {})
    editor_context = (manifest.artifacts or {}).get("editor", {})
    patch_plan_context = (manifest.artifacts or {}).get("patch_plan", {})
    proposal_context = (manifest.artifacts or {}).get("proposal", {})
    apply_preview_context = (manifest.artifacts or {}).get("apply_preview", {})
    apply_result_context = (manifest.artifacts or {}).get("apply_result", {})
    closeout_context = (manifest.artifacts or {}).get("closeout", {})
    claim_ids = review_context.get("canonical_claim_ids", [])
    related_pages = review_context.get("related_filenames", [])
    bundle_path = AUTOMATION_DIR / "reports" / f"{run_id}.md"
    brief_path_value = editor_context.get("brief_path")
    brief_path = ROOT / brief_path_value if brief_path_value else None
    patch_path_value = patch_plan_context.get("report_path")
    patch_path = ROOT / patch_path_value if patch_path_value else None
    proposal_path_value = proposal_context.get("report_path")
    proposal_path = ROOT / proposal_path_value if proposal_path_value else None
    apply_preview_path_value = apply_preview_context.get("report_path")
    apply_preview_path = ROOT / apply_preview_path_value if apply_preview_path_value else None
    apply_result_path_value = apply_result_context.get("report_path")
    apply_result_path = ROOT / apply_result_path_value if apply_result_path_value else None
    closeout_path_value = closeout_context.get("report_path")
    closeout_path = ROOT / closeout_path_value if closeout_path_value else None

    payload = {
        "run_id": manifest.run_id,
        "status": manifest.status,
        "risk": manifest.risk_level,
        "run_type": manifest.run_type,
        "summary": manifest.summary,
        "created_at": manifest.created_at,
        "changed_files_count": len(manifest.changed_files),
        "review_verdict": manifest.review.verdict if manifest.review else None,
        "next_action": manifest.review.next_action if manifest.review else None,
        "canonical_claim_ids": claim_ids,
        "related_pages": related_pages,
        "artifacts": {
            "review_bundle": str(bundle_path.relative_to(ROOT)) if bundle_path.exists() else None,
            "editor_brief": str(brief_path.relative_to(ROOT)) if brief_path and brief_path.exists() else None,
            "patch_plan": str(patch_path.relative_to(ROOT)) if patch_path and patch_path.exists() else None,
            "proposal": str(proposal_path.relative_to(ROOT)) if proposal_path and proposal_path.exists() else None,
            "apply_preview": str(apply_preview_path.relative_to(ROOT))
            if apply_preview_path and apply_preview_path.exists()
            else None,
            "apply_result": str(apply_result_path.relative_to(ROOT))
            if apply_result_path and apply_result_path.exists()
            else None,
            "closeout": str(closeout_path.relative_to(ROOT)) if closeout_path and closeout_path.exists() else None,
        },
    }

    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print(f"Run: {manifest.run_id}")
    print(f"Status: {manifest.status}")
    print(f"Risk: {manifest.risk_level}")
    print(f"Type: {manifest.run_type}")
    print(f"Summary: {manifest.summary}")
    print(f"Created: {manifest.created_at}")
    print(f"Changed files count: {payload['changed_files_count']}")
    if manifest.review:
        print(f"Review verdict: {manifest.review.verdict}")
        print(f"Next action: {manifest.review.next_action}")
    if claim_ids:
        print("Canonical claims:")
        for claim_id in claim_ids:
            print(f"  - {claim_id}")
    if related_pages:
        print("Related pages:")
        for page in related_pages:
            print(f"  - {page}")
    if bundle_path.exists():
        print(f"Review bundle: {bundle_path.relative_to(ROOT)}")
    else:
        print("Review bundle: not generated yet")
    if brief_path and brief_path.exists():
        print(f"Editor brief: {brief_path.relative_to(ROOT)}")
    else:
        print("Editor brief: not generated yet")
    if patch_path and patch_path.exists():
        print(f"Patch plan: {patch_path.relative_to(ROOT)}")
    else:
        print("Patch plan: not generated yet")
    if proposal_path and proposal_path.exists():
        print(f"Proposal: {proposal_path.relative_to(ROOT)}")
    else:
        print("Proposal: not generated yet")
    if apply_preview_path and apply_preview_path.exists():
        print(f"Apply preview: {apply_preview_path.relative_to(ROOT)}")
    else:
        print("Apply preview: not generated yet")
    if apply_result_path and apply_result_path.exists():
        print(f"Apply result: {apply_result_path.relative_to(ROOT)}")
    else:
        print("Apply result: not generated yet")
    if closeout_path and closeout_path.exists():
        print(f"Closeout: {closeout_path.relative_to(ROOT)}")
    else:
        print("Closeout: not generated yet")
    return 0


def cmd_recent_runs(limit: int, status: str | None, as_json: bool) -> int:
    manifest_files = sorted(
        [
            path for path in MANIFESTS_DIR.glob("*.json") if path.name != "run_manifest.example.json"
        ],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    if not manifest_files:
        print("No run manifests found.")
        return 0

    manifests = [load_run_manifest(path) for path in manifest_files]
    if status:
        manifests = [manifest for manifest in manifests if manifest.status == status]

    if not manifests:
        if as_json:
            print("[]")
        else:
            print("No run manifests matched the filters.")
        return 0

    rows = []
    for manifest in manifests[:limit]:
        bundle_path = REPORTS_DIR / f"{manifest.run_id}.md"
        editor_context = (manifest.artifacts or {}).get("editor", {})
        patch_plan_context = (manifest.artifacts or {}).get("patch_plan", {})
        proposal_context = (manifest.artifacts or {}).get("proposal", {})
        apply_preview_context = (manifest.artifacts or {}).get("apply_preview", {})
        apply_result_context = (manifest.artifacts or {}).get("apply_result", {})
        closeout_context = (manifest.artifacts or {}).get("closeout", {})
        brief_path_value = editor_context.get("brief_path")
        patch_path_value = patch_plan_context.get("report_path")
        proposal_path_value = proposal_context.get("report_path")
        apply_preview_path_value = apply_preview_context.get("report_path")
        apply_result_path_value = apply_result_context.get("report_path")
        closeout_path_value = closeout_context.get("report_path")
        has_brief = False
        has_patch_plan = False
        has_proposal = False
        has_apply_preview = False
        has_apply_result = False
        has_closeout = False
        if brief_path_value:
            has_brief = (ROOT / brief_path_value).exists()
        if patch_path_value:
            has_patch_plan = (ROOT / patch_path_value).exists()
        if proposal_path_value:
            has_proposal = (ROOT / proposal_path_value).exists()
        if apply_preview_path_value:
            has_apply_preview = (ROOT / apply_preview_path_value).exists()
        if apply_result_path_value:
            has_apply_result = (ROOT / apply_result_path_value).exists()
        if closeout_path_value:
            has_closeout = (ROOT / closeout_path_value).exists()

        rows.append(
            {
                "run_id": manifest.run_id,
                "status": manifest.status,
                "risk": manifest.risk_level,
                "created_at": manifest.created_at,
                "run_type": manifest.run_type,
                "changed_files_count": len(manifest.changed_files),
                "has_bundle": bundle_path.exists(),
                "has_brief": has_brief,
                "has_patch_plan": has_patch_plan,
                "has_proposal": has_proposal,
                "has_apply_preview": has_apply_preview,
                "has_apply_result": has_apply_result,
                "has_closeout": has_closeout,
                "summary": manifest.summary,
            }
        )

    if as_json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return 0

    print("Recent Runs")
    for row in rows:
        print(
            f"- {row['run_id']} | status={row['status']} | risk={row['risk']} | "
            f"created={row['created_at']}"
        )
        print(
            f"  type={row['run_type']} | changed={row['changed_files_count']} | "
            f"bundle={'yes' if row['has_bundle'] else 'no'} | "
            f"brief={'yes' if row['has_brief'] else 'no'} | patch={'yes' if row['has_patch_plan'] else 'no'} | "
            f"proposal={'yes' if row['has_proposal'] else 'no'} | "
            f"apply_preview={'yes' if row['has_apply_preview'] else 'no'} | "
            f"apply_result={'yes' if row['has_apply_result'] else 'no'} | "
            f"closeout={'yes' if row['has_closeout'] else 'no'}"
        )
        print(f"  summary: {row['summary']}")
    return 0


def cmd_health(as_json: bool) -> int:
    backlog_items = load_topic_backlog()
    backlog_count = len(backlog_items)

    content_index_path = MEMORY_DIR / "content_index.json"
    canonical_claims_path = MEMORY_DIR / "canonical_claims.json"
    entities_path = MEMORY_DIR / "entities.json"

    content_index_count = 0
    canonical_claims_count = 0
    entities_group_count = 0
    backlog_by_cluster: dict[str, int] = {}
    backlog_by_priority: dict[str, int] = {}
    backlog_by_status: dict[str, int] = {}

    for item in backlog_items:
        backlog_by_cluster[item.cluster] = backlog_by_cluster.get(item.cluster, 0) + 1
        backlog_by_priority[item.priority] = backlog_by_priority.get(item.priority, 0) + 1
        backlog_by_status[item.status] = backlog_by_status.get(item.status, 0) + 1

    if content_index_path.exists():
        payload = json.loads(content_index_path.read_text(encoding="utf-8"))
        content_index_count = len(payload.get("pages", []))
    if canonical_claims_path.exists():
        payload = json.loads(canonical_claims_path.read_text(encoding="utf-8"))
        canonical_claims_count = len(payload.get("claims", []))
    if entities_path.exists():
        payload = json.loads(entities_path.read_text(encoding="utf-8"))
        entities_group_count = len(payload.get("entities", {}))

    manifest_files = [
        path for path in MANIFESTS_DIR.glob("*.json") if path.name != "run_manifest.example.json"
    ]
    manifest_status_counts: dict[str, int] = {}
    for manifest_path in manifest_files:
        manifest = load_run_manifest(manifest_path)
        manifest_status_counts[manifest.status] = manifest_status_counts.get(manifest.status, 0) + 1
    report_files = list(REPORTS_DIR.glob("*.md")) if REPORTS_DIR.exists() else []

    baseline = subprocess.run(
        [sys.executable, str(AUTOMATION_DIR / "run_checks.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    strict = subprocess.run(
        [sys.executable, str(AUTOMATION_DIR / "run_checks.py"), "--strict"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    payload = {
        "content_index_pages": content_index_count,
        "canonical_claims": canonical_claims_count,
        "entity_groups": entities_group_count,
        "backlog_items": backlog_count,
        "backlog_by_cluster": dict(sorted(backlog_by_cluster.items())),
        "backlog_by_priority": dict(sorted(backlog_by_priority.items())),
        "backlog_by_status": dict(sorted(backlog_by_status.items())),
        "run_manifests": len(manifest_files),
        "manifest_statuses": dict(sorted(manifest_status_counts.items())),
        "draft_brief_ready_runs": manifest_status_counts.get("draft_brief_ready", 0),
        "review_bundles": len(report_files),
        "checks": "pass" if baseline.returncode == 0 else "fail",
        "checks_strict": "pass" if strict.returncode == 0 else "fail",
    }

    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print("Automation Health")
    print(f"- content_index pages: {payload['content_index_pages']}")
    print(f"- canonical claims: {payload['canonical_claims']}")
    print(f"- entity groups: {payload['entity_groups']}")
    print(f"- backlog items: {payload['backlog_items']}")
    if payload["backlog_by_cluster"]:
        print(
            "- backlog by cluster: "
            + ", ".join(f"{key}={count}" for key, count in payload["backlog_by_cluster"].items())
        )
    if payload["backlog_by_priority"]:
        print(
            "- backlog by priority: "
            + ", ".join(f"{key}={count}" for key, count in payload["backlog_by_priority"].items())
        )
    if payload["backlog_by_status"]:
        print(
            "- backlog by status: "
            + ", ".join(f"{key}={count}" for key, count in payload["backlog_by_status"].items())
        )
    print(f"- run manifests: {payload['run_manifests']}")
    if payload["manifest_statuses"]:
        status_summary = ", ".join(
            f"{status}={count}" for status, count in payload["manifest_statuses"].items()
        )
        print(f"- manifest statuses: {status_summary}")
        print(f"- draft_brief_ready runs: {payload['draft_brief_ready_runs']}")
    print(f"- review bundles: {payload['review_bundles']}")
    print(f"- checks: {payload['checks']}")
    print(f"- checks --strict: {payload['checks_strict']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Single entrypoint for the automation MVP.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List backlog items from topic_backlog.csv.")
    list_parser.add_argument("--status", help="Filter by backlog status.")
    list_parser.add_argument("--cluster", help="Filter by cluster.")
    list_parser.add_argument("--priority", help="Filter by priority.")
    list_parser.add_argument("--json", action="store_true", help="Print backlog items as JSON.")

    open_topic_parser = subparsers.add_parser(
        "open-topic",
        help="Show a detailed view for one backlog topic.",
    )
    open_topic_parser.add_argument("topic_id", help="Backlog topic_id to inspect.")
    open_topic_parser.add_argument("--json", action="store_true", help="Print the topic as JSON.")

    subparsers.add_parser(
        "backlog-summary",
        help="Show aggregate counts for backlog items by cluster, priority, and status.",
    )
    backlog_summary_parser = subparsers.choices["backlog-summary"]
    backlog_summary_parser.add_argument("--json", action="store_true", help="Print the backlog summary as JSON.")

    backlog_sync_parser = subparsers.add_parser(
        "backlog-sync",
        help="Compare topic_backlog.csv with run manifests and report stale or active topics.",
    )
    backlog_sync_parser.add_argument("--json", action="store_true", help="Print the backlog/run sync report as JSON.")

    open_run_parser = subparsers.add_parser(
        "open-run",
        help="Show a detailed view for one run manifest.",
    )
    open_run_parser.add_argument("run_id", help="Run manifest basename without .json")
    open_run_parser.add_argument("--json", action="store_true", help="Print the run as JSON.")

    next_step_parser = subparsers.add_parser(
        "next-step",
        help="Show the expected next lifecycle action for one run manifest.",
    )
    next_step_parser.add_argument("run_id", help="Run manifest basename without .json")
    next_step_parser.add_argument("--json", action="store_true", help="Print the next-step guidance as JSON.")

    recent_runs_parser = subparsers.add_parser(
        "recent-runs",
        help="List the most recent run manifests with compact status info.",
    )
    recent_runs_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of recent runs to show.",
    )
    recent_runs_parser.add_argument(
        "--status",
        help="Filter recent runs by manifest status.",
    )
    recent_runs_parser.add_argument(
        "--json",
        action="store_true",
        help="Print recent runs as JSON.",
    )

    show_parser = subparsers.add_parser("show", help="Show a compact summary for one run manifest.")
    show_parser.add_argument("run_id", help="Run manifest basename without .json")
    show_parser.add_argument("--json", action="store_true", help="Print the compact run summary as JSON.")

    health_parser = subparsers.add_parser("health", help="Show a compact health summary for the automation layer.")
    health_parser.add_argument("--json", action="store_true", help="Print the health snapshot as JSON.")
    status_parser = subparsers.add_parser("status", help="Alias for `health`.")
    status_parser.add_argument("--json", action="store_true", help="Print the status snapshot as JSON.")

    checks_parser = subparsers.add_parser("checks", help="Run deterministic automation-layer checks.")
    checks_parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on weak-cluster warnings in addition to hard failures.",
    )
    checks_parser.add_argument(
        "--manifest",
        help="Record automation check results into the given run manifest.",
    )

    plan_parser = subparsers.add_parser("plan", help="Build a deterministic change plan for one backlog topic.")
    plan_parser.add_argument("topic_id", help="Backlog topic_id to plan.")
    plan_parser.add_argument("--json", action="store_true", help="Print the plan as JSON.")

    init_run_parser = subparsers.add_parser(
        "init-run",
        help="Create a planned run manifest for one backlog topic without running the reviewer.",
    )
    init_run_parser.add_argument("topic_id", help="Backlog topic_id to initialize.")

    review_parser = subparsers.add_parser(
        "review",
        help="Run the deterministic reviewer for an existing manifest.",
    )
    review_parser.add_argument("run_id", help="Run manifest basename without .json")

    brief_parser = subparsers.add_parser(
        "brief",
        help="Create a brief-only editor artifact from an existing reviewed manifest.",
    )
    brief_parser.add_argument("run_id", help="Run manifest path or basename without .json")
    brief_parser.add_argument("--output-dir", help="Directory for the brief artifact.")

    patch_parser = subparsers.add_parser(
        "patch-plan",
        help="Create a proposal-only patch plan from an existing draft brief run.",
    )
    patch_parser.add_argument("run_id", help="Run manifest path or basename without .json")
    patch_parser.add_argument("--output-dir", help="Directory for the patch-plan report.")

    propose_parser = subparsers.add_parser(
        "propose",
        help="Render human-reviewable proposed edits from Patch Spec v1.",
    )
    propose_parser.add_argument("run_id", help="Run manifest path or basename without .json")
    propose_parser.add_argument("--output-dir", help="Directory for the proposal report.")

    approval_parser = subparsers.add_parser(
        "approval",
        help="Record human approval decisions for rendered proposal specs.",
    )
    approval_parser.add_argument("run_id", help="Run manifest basename without .json")
    approval_parser.add_argument(
        "--state",
        required=True,
        choices=["approved", "proposed", "rejected"],
        help="Approval state to write to matching proposal specs.",
    )
    approval_parser.add_argument("--source", help="Only update specs for this source_of_truth_file.")
    approval_parser.add_argument("--target", help="Only update specs for this output_file.")
    approval_parser.add_argument("--operation", help="Only update specs for this operation_type.")
    approval_parser.add_argument("--all", action="store_true", help="Update every rendered proposal spec.")
    approval_parser.add_argument("--note", help="Optional human review note to store with matched specs.")
    approval_parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing files.")

    apply_preview_parser = subparsers.add_parser(
        "apply-preview",
        help="Render a no-write apply preview from approved Patch Spec v1 entries.",
    )
    apply_preview_parser.add_argument("run_id", help="Run manifest basename without .json")

    apply_approved_parser = subparsers.add_parser(
        "apply-approved",
        help="Apply approved Patch Spec v1 entries with conservative deterministic templates.",
    )
    apply_approved_parser.add_argument("run_id", help="Run manifest basename without .json")

    close_run_parser = subparsers.add_parser(
        "close-run",
        help="Close a QA-passed run with a final summary artifact.",
    )
    close_run_parser.add_argument("run_id", help="Run manifest basename without .json")
    close_run_parser.add_argument("--note", help="Optional human closeout note.")

    run_parser = subparsers.add_parser("run", help="Create and review a manifest for one backlog topic.")
    run_parser.add_argument("topic_id", help="Backlog topic_id to run.")

    bundle_parser = subparsers.add_parser(
        "bundle",
        help="Run the MVP flow and export a markdown review bundle for one backlog topic.",
    )
    bundle_parser.add_argument("topic_id", help="Backlog topic_id to bundle.")

    bundle_run_parser = subparsers.add_parser(
        "bundle-run",
        help="Export a markdown review bundle for an existing run manifest.",
    )
    bundle_run_parser.add_argument("run_id", help="Run manifest basename without .json")

    worker_chain_parser = subparsers.add_parser(
        "worker-chain",
        help="Run the no-write Scout -> Editor -> Reviewer chain for one topic proposal.",
    )
    worker_chain_parser.add_argument("--topic-id", help="Scout topic_id to select after Scout runs.")
    worker_chain_parser.add_argument("--target", help="Alternative selector: target page or slug.")
    worker_chain_parser.add_argument("--limit", type=int, default=8, help="Maximum Scout proposals to render.")
    worker_chain_parser.add_argument(
        "--min-impressions",
        type=int,
        default=200,
        help="Minimum page impressions for Scout proposals.",
    )
    worker_chain_parser.add_argument("--json", action="store_true", help="Print the chain summary as JSON.")

    worker_intake_parser = subparsers.add_parser(
        "worker-intake",
        help="Generate a no-write intake gate artifact from one Worker chain summary.",
    )
    worker_intake_parser.add_argument("--topic-id", help="Topic id used to infer the default chain path.")
    worker_intake_parser.add_argument("--chain", help="Path to worker-chain-<topic_id>.json.")
    worker_intake_parser.add_argument("--approved-by", help="Human approver name or handle.")
    worker_intake_parser.add_argument("--note", help="Optional approval note.")
    worker_intake_parser.add_argument("--json", action="store_true", help="Print the intake summary as JSON.")

    worker_run_plan_parser = subparsers.add_parser(
        "worker-run-plan",
        help="Generate a no-write run-plan proposal from one Worker intake artifact.",
    )
    worker_run_plan_parser.add_argument("--topic-id", help="Topic id used to infer the default intake path.")
    worker_run_plan_parser.add_argument("--intake", help="Path to worker-intake-<topic_id>.json.")
    worker_run_plan_parser.add_argument("--output-dir", help="Directory for run-plan proposal artifacts.")
    worker_run_plan_parser.add_argument("--basename", help="Output basename without extension.")
    worker_run_plan_parser.add_argument("--json", action="store_true", help="Print the run-plan summary as JSON.")

    worker_manifest_parser = subparsers.add_parser(
        "worker-manifest",
        help="Create a planned manifest from one approved Worker run-plan proposal.",
    )
    worker_manifest_parser.add_argument("--topic-id", help="Topic id used to infer the default run-plan path.")
    worker_manifest_parser.add_argument("--run-plan", help="Path to worker-run-plan-<topic_id>.json.")
    worker_manifest_parser.add_argument("--manifest-dir", help="Override manifest output directory.")
    worker_manifest_parser.add_argument("--created-by", help="Human operator name or handle.")
    worker_manifest_parser.add_argument("--dry-run", action="store_true", help="Validate without writing a manifest.")
    worker_manifest_parser.add_argument("--json", action="store_true", help="Print the manifest writer summary as JSON.")

    llm_adapter_parser = subparsers.add_parser(
        "llm-adapter",
        help="Run the fail-closed LLM adapter for a structured Worker request.",
    )
    llm_adapter_parser.add_argument("--request", required=True, help="Path to a structured LLM request JSON file.")
    llm_adapter_parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider to use. Defaults to disabled/fail-closed.",
    )
    llm_adapter_parser.add_argument("--fixture", help="Fixture response JSON for offline provider tests.")
    llm_adapter_parser.add_argument("--output", help="Optional path for the adapter result artifact.")
    llm_adapter_parser.add_argument("--json", action="store_true", help="Print the adapter summary as JSON.")

    llm_scout_parser = subparsers.add_parser(
        "llm-scout",
        help="Run a no-write LLM Scout review over deterministic Scout proposals.",
    )
    llm_scout_parser.add_argument(
        "--signals",
        action="append",
        help="Path to a GSC/Bing agent signals JSON file. Can be supplied more than once.",
    )
    llm_scout_parser.add_argument(
        "--external-proposals",
        action="append",
        help="Path to an External Scout JSON artifact with candidate_proposals. Can be supplied more than once.",
    )
    llm_scout_parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider to use through llm_adapter. Defaults to disabled/fail-closed.",
    )
    llm_scout_parser.add_argument("--fixture", help="Fixture response JSON for offline provider tests.")
    llm_scout_parser.add_argument("--output-dir", help="Directory for LLM Scout artifacts.")
    llm_scout_parser.add_argument("--basename", help="Output basename without extension.")
    llm_scout_parser.add_argument("--limit", type=int, default=8, help="Maximum deterministic proposals to review.")
    llm_scout_parser.add_argument(
        "--min-impressions",
        type=int,
        default=200,
        help="Minimum page impressions for deterministic Scout proposals.",
    )
    llm_scout_parser.add_argument("--json", action="store_true", help="Print the LLM Scout summary as JSON.")

    llm_candidate_refresh_parser = subparsers.add_parser(
        "llm-candidate-refresh",
        help="Run no-write LLM Scout plus topic discovery to refresh owner-review candidate topics.",
    )
    llm_candidate_refresh_parser.add_argument(
        "--signals",
        action="append",
        help="Path to a GSC/Bing agent signals JSON file. Can be supplied more than once.",
    )
    llm_candidate_refresh_parser.add_argument(
        "--external-proposals",
        action="append",
        help="Path to an External Scout JSON artifact with candidate_proposals. Can be supplied more than once.",
    )
    llm_candidate_refresh_parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider to use through llm_adapter. Defaults to disabled/fail-closed.",
    )
    llm_candidate_refresh_parser.add_argument("--fixture", help="Fixture response JSON for offline provider tests.")
    llm_candidate_refresh_parser.add_argument("--output-dir", help="Directory for candidate refresh artifacts.")
    llm_candidate_refresh_parser.add_argument("--basename", help="Refresh summary basename without extension.")
    llm_candidate_refresh_parser.add_argument("--scout-basename", help="LLM Scout output basename without extension.")
    llm_candidate_refresh_parser.add_argument("--discovery-basename", help="Topic discovery output basename without extension.")
    llm_candidate_refresh_parser.add_argument("--limit", type=int, default=8, help="Maximum deterministic proposals to review.")
    llm_candidate_refresh_parser.add_argument(
        "--min-impressions",
        type=int,
        default=200,
        help="Minimum page impressions for deterministic Scout proposals.",
    )
    llm_candidate_refresh_parser.add_argument("--json", action="store_true", help="Print the candidate refresh summary as JSON.")

    llm_auto_review_queue_parser = subparsers.add_parser(
        "llm-auto-review-queue",
        help="Run candidate refresh and auto-review top candidates through no-write Editor/Reviewer.",
    )
    llm_auto_review_queue_parser.add_argument(
        "--signals",
        action="append",
        help="Path to a GSC/Bing agent signals JSON file. Can be supplied more than once.",
    )
    llm_auto_review_queue_parser.add_argument(
        "--external-proposals",
        action="append",
        help="Path to an External Scout JSON artifact with candidate_proposals. Can be supplied more than once.",
    )
    llm_auto_review_queue_parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider passed to LLM stages. Defaults to disabled/fail-closed.",
    )
    llm_auto_review_queue_parser.add_argument("--output-dir", help="Directory for auto-review queue artifacts.")
    llm_auto_review_queue_parser.add_argument("--basename", help="Queue summary basename.")
    llm_auto_review_queue_parser.add_argument("--scout-fixture", help="Fixture response JSON for offline Scout tests.")
    llm_auto_review_queue_parser.add_argument("--editor-fixture", help="Fixture response JSON for offline Editor tests.")
    llm_auto_review_queue_parser.add_argument("--reviewer-fixture", help="Fixture response JSON for offline Reviewer tests.")
    llm_auto_review_queue_parser.add_argument("--limit", type=int, default=8, help="Maximum deterministic Scout proposals to review.")
    llm_auto_review_queue_parser.add_argument("--min-impressions", type=int, default=200, help="Minimum page impressions for Scout proposals.")
    llm_auto_review_queue_parser.add_argument("--max-chains", type=int, default=3, help="Maximum top candidates to auto-review.")
    llm_auto_review_queue_parser.add_argument(
        "--include-existing",
        action="store_true",
        help="Rerun topics that already have completed chain summaries.",
    )
    llm_auto_review_queue_parser.add_argument("--json", action="store_true", help="Print the auto-review queue summary as JSON.")

    external_scout_parser = subparsers.add_parser(
        "external-scout",
        help="Run no-write external source scout from source_registry.json.",
    )
    external_scout_parser.add_argument("--registry", help="Path to source_registry.json.")
    external_scout_parser.add_argument("--output-dir", help="Directory for External Scout artifacts.")
    external_scout_parser.add_argument("--basename", help="Output basename without extension.")
    external_scout_parser.add_argument(
        "--include-proposed",
        action="store_true",
        help="Include proposed sources for manual testing only.",
    )
    external_scout_parser.add_argument("--limit", type=int, default=12, help="Maximum external candidate proposals.")
    external_scout_parser.add_argument("--json", action="store_true", help="Print the External Scout summary as JSON.")

    external_evidence_refresh_parser = subparsers.add_parser(
        "external-evidence-refresh",
        help="Build a no-write evidence queue from External Scout artifacts.",
    )
    external_evidence_refresh_parser.add_argument("--external-scout", help="Path to an External Scout JSON artifact.")
    external_evidence_refresh_parser.add_argument("--output-dir", help="Directory for External Evidence Refresh artifacts.")
    external_evidence_refresh_parser.add_argument("--basename", help="Output basename without extension.")
    external_evidence_refresh_parser.add_argument("--limit", type=int, default=20, help="Maximum query tasks and URL leads to include.")
    external_evidence_refresh_parser.add_argument("--json", action="store_true", help="Print the External Evidence Refresh summary as JSON.")

    external_evidence_collect_parser = subparsers.add_parser(
        "external-evidence-collect",
        help="Collect no-write evidence from explicit URL leads.",
    )
    external_evidence_collect_parser.add_argument("--evidence-refresh", help="Path to external-evidence-refresh.json.")
    external_evidence_collect_parser.add_argument("--output-dir", help="Directory for External Evidence Collect artifacts.")
    external_evidence_collect_parser.add_argument("--basename", help="Output basename without extension.")
    external_evidence_collect_parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "fetch"],
        help="Evidence provider. `fetch` reads only explicit URL leads. Defaults to disabled/fail-closed.",
    )
    external_evidence_collect_parser.add_argument("--limit", type=int, default=20, help="Maximum explicit URL leads to collect.")
    external_evidence_collect_parser.add_argument("--timeout", type=float, default=10.0, help="Per-URL fetch timeout in seconds.")
    external_evidence_collect_parser.add_argument("--max-bytes", type=int, default=750000, help="Maximum bytes to read per URL.")
    external_evidence_collect_parser.add_argument("--json", action="store_true", help="Print the External Evidence Collect summary as JSON.")

    external_search_collect_parser = subparsers.add_parser(
        "external-search-collect",
        help="Collect no-write search evidence from approved source query tasks.",
    )
    external_search_collect_parser.add_argument("--evidence-refresh", help="Path to external-evidence-refresh.json.")
    external_search_collect_parser.add_argument("--output-dir", help="Directory for External Search Collect artifacts.")
    external_search_collect_parser.add_argument("--basename", help="Output basename without extension.")
    external_search_collect_parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Search provider. `openai` uses Responses API web_search. Defaults to disabled/fail-closed.",
    )
    external_search_collect_parser.add_argument("--limit", type=int, default=6, help="Maximum query tasks to search.")
    external_search_collect_parser.add_argument("--per-query-results", type=int, default=3, help="Maximum results per query task.")
    external_search_collect_parser.add_argument("--proposal-limit", type=int, default=10, help="Maximum search candidate proposals.")
    external_search_collect_parser.add_argument("--json", action="store_true", help="Print the External Search Collect summary as JSON.")

    llm_editor_parser = subparsers.add_parser(
        "llm-editor",
        help="Run a no-write LLM Editor planning brief from one selected LLM Scout opportunity.",
    )
    llm_editor_parser.add_argument("--scout-result", help="Path to llm-scout-review-result.json.")
    llm_editor_parser.add_argument("--scout-request", help="Path to llm-scout-review-request.json.")
    llm_editor_parser.add_argument("--topic-id", help="Selected LLM Scout topic_id. Defaults to the first selected opportunity.")
    llm_editor_parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider to use through llm_adapter. Defaults to disabled/fail-closed.",
    )
    llm_editor_parser.add_argument("--fixture", help="Fixture response JSON for offline provider tests.")
    llm_editor_parser.add_argument("--output-dir", help="Directory for LLM Editor artifacts.")
    llm_editor_parser.add_argument("--basename", help="Output basename without extension.")
    llm_editor_parser.add_argument("--json", action="store_true", help="Print the LLM Editor summary as JSON.")

    llm_reviewer_parser = subparsers.add_parser(
        "llm-reviewer",
        help="Run a no-write LLM Reviewer gate from one LLM Editor planning brief.",
    )
    llm_reviewer_parser.add_argument("--topic-id", help="Topic id used to infer default LLM Editor artifacts.")
    llm_reviewer_parser.add_argument("--editor-result", help="Path to llm-editor-brief-<topic_id>-result.json.")
    llm_reviewer_parser.add_argument("--editor-request", help="Path to llm-editor-brief-<topic_id>-request.json.")
    llm_reviewer_parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider to use through llm_adapter. Defaults to disabled/fail-closed.",
    )
    llm_reviewer_parser.add_argument("--fixture", help="Fixture response JSON for offline provider tests.")
    llm_reviewer_parser.add_argument("--output-dir", help="Directory for LLM Reviewer artifacts.")
    llm_reviewer_parser.add_argument("--basename", help="Output basename without extension.")
    llm_reviewer_parser.add_argument("--json", action="store_true", help="Print the LLM Reviewer summary as JSON.")

    llm_worker_chain_parser = subparsers.add_parser(
        "llm-worker-chain",
        help="Run the no-write live LLM Scout -> Editor -> Reviewer chain.",
    )
    llm_worker_chain_parser.add_argument(
        "--signals",
        action="append",
        help="Path to a GSC/Bing agent signals JSON file. Can be supplied more than once.",
    )
    llm_worker_chain_parser.add_argument(
        "--from-decision",
        help="Path to an approved_for_chain llm-topic-decision-<topic_id>.json artifact. Replays the saved decision instead of rerunning Scout.",
    )
    llm_worker_chain_parser.add_argument("--topic-id", help="Selected LLM Scout topic_id. Defaults to the first selected opportunity.")
    llm_worker_chain_parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider to use through llm_adapter for each LLM stage. Defaults to disabled/fail-closed.",
    )
    llm_worker_chain_parser.add_argument("--output-dir", help="Directory for LLM worker chain artifacts.")
    llm_worker_chain_parser.add_argument("--basename", help="Chain summary basename without extension.")
    llm_worker_chain_parser.add_argument("--scout-basename", help="LLM Scout output basename without extension.")
    llm_worker_chain_parser.add_argument("--editor-basename", help="LLM Editor output basename without extension.")
    llm_worker_chain_parser.add_argument("--reviewer-basename", help="LLM Reviewer output basename without extension.")
    llm_worker_chain_parser.add_argument("--scout-fixture", help="Fixture response JSON for the Scout stage.")
    llm_worker_chain_parser.add_argument("--editor-fixture", help="Fixture response JSON for the Editor stage.")
    llm_worker_chain_parser.add_argument("--reviewer-fixture", help="Fixture response JSON for the Reviewer stage.")
    llm_worker_chain_parser.add_argument("--limit", type=int, default=8, help="Maximum deterministic Scout proposals to review.")
    llm_worker_chain_parser.add_argument("--min-impressions", type=int, default=200, help="Minimum page impressions for Scout proposals.")
    llm_worker_chain_parser.add_argument("--json", action="store_true", help="Print the LLM worker chain summary as JSON.")

    llm_review_latest_parser = subparsers.add_parser(
        "llm-review-latest",
        help="Read the latest no-write LLM worker chain owner-review summary.",
    )
    llm_review_latest_parser.add_argument("--chain", help="Path to a specific llm-worker-chain-<topic_id>.json summary.")
    llm_review_latest_parser.add_argument("--reports-dir", help="Directory to search for LLM worker chain summaries.")
    llm_review_latest_parser.add_argument("--json", action="store_true", help="Print the owner-review summary as JSON.")

    llm_intake_latest_parser = subparsers.add_parser(
        "llm-intake-latest",
        help="Generate a no-write intake artifact from the latest LLM worker chain.",
    )
    llm_intake_latest_parser.add_argument("--chain", help="Path to a specific llm-worker-chain-<topic_id>.json summary.")
    llm_intake_latest_parser.add_argument("--reports-dir", help="Directory to search for LLM worker chain summaries.")
    llm_intake_latest_parser.add_argument("--approved-by", help="Human approver name or handle.")
    llm_intake_latest_parser.add_argument("--note", help="Optional approval note.")
    llm_intake_latest_parser.add_argument(
        "--resolve-reviewer-blockers",
        action="store_true",
        help="Allow owner-confirmed Reviewer blocking issues to become intake warnings. Requires --approved-by and --note.",
    )
    llm_intake_latest_parser.add_argument("--output-dir", help="Directory for LLM intake artifacts.")
    llm_intake_latest_parser.add_argument("--basename", help="Output basename without extension.")
    llm_intake_latest_parser.add_argument("--json", action="store_true", help="Print the LLM intake summary as JSON.")

    llm_topic_discovery_parser = subparsers.add_parser(
        "llm-topic-discovery",
        help="Build no-write topic discovery proposals from LLM Scout output.",
    )
    llm_topic_discovery_parser.add_argument("--scout-result", help="Path to llm-scout-review-result.json.")
    llm_topic_discovery_parser.add_argument("--scout-request", help="Path to llm-scout-review-request.json.")
    llm_topic_discovery_parser.add_argument("--output-dir", help="Directory for topic discovery artifacts.")
    llm_topic_discovery_parser.add_argument("--basename", help="Output basename without extension.")
    llm_topic_discovery_parser.add_argument("--json", action="store_true", help="Print the topic discovery summary as JSON.")

    llm_topic_decision_parser = subparsers.add_parser(
        "llm-topic-decision",
        help="Record an owner decision for one LLM topic discovery proposal.",
    )
    llm_topic_decision_parser.add_argument("--discovery", help="Path to llm-topic-discovery.json.")
    llm_topic_decision_parser.add_argument("--from-decision", help="Path to an existing llm-topic-decision-<topic_id>.json artifact to rerecord.")
    llm_topic_decision_parser.add_argument("--topic-id", help="Discovered topic_id to decide. Required unless --from-decision is supplied.")
    llm_topic_decision_parser.add_argument(
        "--state",
        required=True,
        choices=["approved_for_chain", "monitor", "rejected"],
        help="Owner decision for this topic.",
    )
    llm_topic_decision_parser.add_argument("--decided-by", required=True, help="Human owner/operator name or handle.")
    llm_topic_decision_parser.add_argument("--note", help="Optional decision note.")
    llm_topic_decision_parser.add_argument("--output-dir", help="Directory for decision artifacts.")
    llm_topic_decision_parser.add_argument("--basename", help="Output basename without extension.")
    llm_topic_decision_parser.add_argument("--json", action="store_true", help="Print the topic decision summary as JSON.")

    llm_topic_decisions_parser = subparsers.add_parser(
        "llm-topic-decisions",
        help="Build a consolidated no-write report for LLM topic decisions.",
    )
    llm_topic_decisions_parser.add_argument("--reports-dir", help="Directory containing llm-topic-decision-*.json files.")
    llm_topic_decisions_parser.add_argument("--json-output", help="Path for the consolidated JSON artifact.")
    llm_topic_decisions_parser.add_argument("--markdown-output", help="Path for the consolidated markdown artifact.")
    llm_topic_decisions_parser.add_argument("--no-write", action="store_true", help="Build and print only; do not write artifacts.")
    llm_topic_decisions_parser.add_argument("--json", action="store_true", help="Print the topic decisions summary as JSON.")

    llm_approved_handoffs_parser = subparsers.add_parser(
        "llm-approved-handoffs",
        help="Show approved LLM topic decisions ready for deterministic worker-chain replay.",
    )
    llm_approved_handoffs_parser.add_argument("--reports-dir", help="Directory containing llm-topic-decision-*.json files.")
    llm_approved_handoffs_parser.add_argument(
        "--provider",
        default="openai",
        choices=["fixture", "openai"],
        help="Provider to include in printed worker-chain commands.",
    )
    llm_approved_handoffs_parser.add_argument("--json", action="store_true", help="Print approved handoffs as JSON.")

    llm_run_approved_handoffs_parser = subparsers.add_parser(
        "llm-run-approved-handoffs",
        help="Run pending approved LLM topic decisions through no-write worker-chain replay.",
    )
    llm_run_approved_handoffs_parser.add_argument("--reports-dir", help="Directory containing llm-topic-decision-*.json files.")
    llm_run_approved_handoffs_parser.add_argument("--output-dir", help="Directory for approved-handoff run artifacts.")
    llm_run_approved_handoffs_parser.add_argument("--basename", help="Aggregate summary basename.")
    llm_run_approved_handoffs_parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider passed to no-write LLM worker chains. Defaults to disabled/fail-closed.",
    )
    llm_run_approved_handoffs_parser.add_argument("--max-handoffs", type=int, default=3, help="Maximum pending handoffs to run.")
    llm_run_approved_handoffs_parser.add_argument(
        "--include-current",
        action="store_true",
        help="Rerun handoffs even when a current chain summary already exists.",
    )
    llm_run_approved_handoffs_parser.add_argument("--editor-fixture", help="Fixture response JSON for offline Editor tests.")
    llm_run_approved_handoffs_parser.add_argument("--reviewer-fixture", help="Fixture response JSON for offline Reviewer tests.")
    llm_run_approved_handoffs_parser.add_argument("--json", action="store_true", help="Print approved-handoff run summary as JSON.")

    content_seo_parser = subparsers.add_parser(
        "content-seo-opportunities",
        help="Build a no-write SEO/LLM content opportunity report.",
    )
    content_seo_parser.add_argument("--json-output", help="Path for the full JSON artifact.")
    content_seo_parser.add_argument("--markdown-output", help="Path for the markdown artifact.")
    content_seo_parser.add_argument("--no-write", action="store_true", help="Build and print only; do not write artifacts.")
    content_seo_parser.add_argument("--json", action="store_true", help="Print the report summary as JSON.")

    subparsers.add_parser(
        "bing-report",
        help="Fetch Bing Webmaster weekly report artifacts for humans and future agents.",
    )

    content_voice_parser = subparsers.add_parser(
        "content-voice",
        help="Run a no-write audit for generic or low-utility public content signals.",
    )
    content_voice_parser.add_argument("--top", type=int, default=12, help="Number of top opportunities to print.")
    content_voice_parser.add_argument(
        "--fail-on-high-risk",
        action="store_true",
        help="Return non-zero when high-risk voice findings exist. Not used by default checks.",
    )
    content_voice_parser.add_argument("--json", action="store_true", help="Print the audit as JSON.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "checks":
        return cmd_checks(args.strict, args.manifest)
    if args.command == "list":
        return cmd_list(args.status, args.cluster, args.priority, args.json)
    if args.command == "open-topic":
        return cmd_open_topic(args.topic_id, args.json)
    if args.command == "backlog-summary":
        return cmd_backlog_summary(args.json)
    if args.command == "backlog-sync":
        return cmd_backlog_sync(args.json)
    if args.command == "open-run":
        return cmd_open_run(args.run_id, args.json)
    if args.command == "next-step":
        return cmd_next_step(args.run_id, args.json)
    if args.command == "recent-runs":
        return cmd_recent_runs(args.limit, args.status, args.json)
    if args.command == "show":
        return cmd_show(args.run_id, args.json)
    if args.command in {"health", "status"}:
        return cmd_health(args.json)
    if args.command == "plan":
        return cmd_plan(args.topic_id, args.json)
    if args.command == "init-run":
        return cmd_init_run(args.topic_id)
    if args.command == "review":
        return cmd_review(args.run_id)
    if args.command == "brief":
        return cmd_brief(args.run_id, args.output_dir)
    if args.command == "patch-plan":
        return cmd_patch_plan(args.run_id, args.output_dir)
    if args.command == "propose":
        return cmd_propose(args.run_id, args.output_dir)
    if args.command == "approval":
        return cmd_approval(
            args.run_id,
            args.state,
            args.all,
            args.source,
            args.target,
            args.operation,
            args.note,
            args.dry_run,
        )
    if args.command == "apply-preview":
        return cmd_apply_preview(args.run_id)
    if args.command == "apply-approved":
        return cmd_apply_approved(args.run_id)
    if args.command == "close-run":
        return cmd_close_run(args.run_id, args.note)
    if args.command == "run":
        return cmd_run(args.topic_id)
    if args.command == "bundle":
        return cmd_bundle(args.topic_id)
    if args.command == "bundle-run":
        return cmd_bundle_run(args.run_id)
    if args.command == "worker-chain":
        return cmd_worker_chain(args.topic_id, args.target, args.limit, args.min_impressions, args.json)
    if args.command == "worker-intake":
        return cmd_worker_intake(args.topic_id, args.chain, args.approved_by, args.note, args.json)
    if args.command == "worker-run-plan":
        return cmd_worker_run_plan(args.topic_id, args.intake, args.output_dir, args.basename, args.json)
    if args.command == "worker-manifest":
        return cmd_worker_manifest(
            args.topic_id,
            args.run_plan,
            args.manifest_dir,
            args.created_by,
            args.dry_run,
            args.json,
        )
    if args.command == "llm-adapter":
        return cmd_llm_adapter(args.request, args.provider, args.fixture, args.output, args.json)
    if args.command == "llm-scout":
        return cmd_llm_scout(
            args.signals,
            args.external_proposals,
            args.provider,
            args.fixture,
            args.output_dir,
            args.basename,
            args.limit,
            args.min_impressions,
            args.json,
        )
    if args.command == "llm-candidate-refresh":
        return cmd_llm_candidate_refresh(
            args.signals,
            args.external_proposals,
            args.provider,
            args.fixture,
            args.output_dir,
            args.basename,
            args.scout_basename,
            args.discovery_basename,
            args.limit,
            args.min_impressions,
            args.json,
        )
    if args.command == "llm-auto-review-queue":
        return cmd_llm_auto_review_queue(
            args.signals,
            args.external_proposals,
            args.output_dir,
            args.basename,
            args.provider,
            args.scout_fixture,
            args.editor_fixture,
            args.reviewer_fixture,
            args.limit,
            args.min_impressions,
            args.max_chains,
            args.include_existing,
            args.json,
        )
    if args.command == "external-scout":
        return cmd_external_scout(
            args.registry,
            args.output_dir,
            args.basename,
            args.include_proposed,
            args.limit,
            args.json,
        )
    if args.command == "external-evidence-refresh":
        return cmd_external_evidence_refresh(
            args.external_scout,
            args.output_dir,
            args.basename,
            args.limit,
            args.json,
        )
    if args.command == "external-evidence-collect":
        return cmd_external_evidence_collect(
            args.evidence_refresh,
            args.output_dir,
            args.basename,
            args.provider,
            args.limit,
            args.timeout,
            args.max_bytes,
            args.json,
        )
    if args.command == "external-search-collect":
        return cmd_external_search_collect(
            args.evidence_refresh,
            args.output_dir,
            args.basename,
            args.provider,
            args.limit,
            args.per_query_results,
            args.proposal_limit,
            args.json,
        )
    if args.command == "llm-editor":
        return cmd_llm_editor(
            args.scout_result,
            args.scout_request,
            args.topic_id,
            args.provider,
            args.fixture,
            args.output_dir,
            args.basename,
            args.json,
        )
    if args.command == "llm-reviewer":
        return cmd_llm_reviewer(
            args.topic_id,
            args.editor_result,
            args.editor_request,
            args.provider,
            args.fixture,
            args.output_dir,
            args.basename,
            args.json,
        )
    if args.command == "llm-worker-chain":
        return cmd_llm_worker_chain(
            args.signals,
            args.from_decision,
            args.topic_id,
            args.provider,
            args.output_dir,
            args.basename,
            args.scout_basename,
            args.editor_basename,
            args.reviewer_basename,
            args.scout_fixture,
            args.editor_fixture,
            args.reviewer_fixture,
            args.limit,
            args.min_impressions,
            args.json,
        )
    if args.command == "llm-review-latest":
        return cmd_llm_review_latest(args.chain, args.reports_dir, args.json)
    if args.command == "llm-intake-latest":
        return cmd_llm_intake_latest(
            args.chain,
            args.reports_dir,
            args.approved_by,
            args.note,
            args.output_dir,
            args.basename,
            args.resolve_reviewer_blockers,
            args.json,
        )
    if args.command == "llm-topic-discovery":
        return cmd_llm_topic_discovery(
            args.scout_result,
            args.scout_request,
            args.output_dir,
            args.basename,
            args.json,
        )
    if args.command == "llm-topic-decision":
        return cmd_llm_topic_decision(
            args.discovery,
            args.from_decision,
            args.topic_id,
            args.state,
            args.decided_by,
            args.note,
            args.output_dir,
            args.basename,
            args.json,
        )
    if args.command == "llm-topic-decisions":
        return cmd_llm_topic_decisions(
            args.reports_dir,
            args.json_output,
            args.markdown_output,
            args.no_write,
            args.json,
        )
    if args.command == "llm-approved-handoffs":
        return cmd_llm_approved_handoffs(args.reports_dir, args.provider, args.json)
    if args.command == "llm-run-approved-handoffs":
        return cmd_llm_run_approved_handoffs(
            args.reports_dir,
            args.output_dir,
            args.basename,
            args.provider,
            args.max_handoffs,
            args.include_current,
            args.editor_fixture,
            args.reviewer_fixture,
            args.json,
        )
    if args.command == "content-seo-opportunities":
        return cmd_content_seo_opportunities(
            args.json_output,
            args.markdown_output,
            args.no_write,
            args.json,
        )
    if args.command == "bing-report":
        return cmd_bing_report()
    if args.command == "content-voice":
        return cmd_content_voice(args.top, args.fail_on_high_risk, args.json)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
