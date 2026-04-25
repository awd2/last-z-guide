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


def cmd_brief(run_id: str) -> int:
    return run_step(
        "Editor Brief",
        [sys.executable, str(AUTOMATION_DIR / "editor.py"), run_id],
    )


def cmd_patch_plan(run_id: str) -> int:
    return run_step(
        "Patch Plan",
        [sys.executable, str(AUTOMATION_DIR / "patch_planner.py"), run_id],
    )


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

    bundle_path = AUTOMATION_DIR / "reports" / f"{run_id}.md"
    brief_path_value = editor_context.get("brief_path")
    brief_path = ROOT / brief_path_value if brief_path_value else None
    patch_path_value = patch_plan_context.get("report_path")
    patch_path = ROOT / patch_path_value if patch_path_value else None

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
        "checks": {
            name: {"status": result.status, "notes": result.notes}
            for name, result in manifest.checks.items()
        },
        "artifacts": {
            "manifest": str(manifest_path.relative_to(ROOT)),
            "review_bundle": str(bundle_path.relative_to(ROOT)) if bundle_path.exists() else None,
            "editor_brief": str(brief_path.relative_to(ROOT)) if brief_path and brief_path.exists() else None,
            "patch_plan": str(patch_path.relative_to(ROOT)) if patch_path and patch_path.exists() else None,
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
            "next_step": "human_review_then_manual_edit",
            "recommended_command": None,
            "requires_human_review": True,
            "requires_manual_edit_gate": True,
            "reason": "The run has a proposal-only patch plan and now needs human review before any site edits.",
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
    claim_ids = review_context.get("canonical_claim_ids", [])
    related_pages = review_context.get("related_filenames", [])
    bundle_path = AUTOMATION_DIR / "reports" / f"{run_id}.md"
    brief_path_value = editor_context.get("brief_path")
    brief_path = ROOT / brief_path_value if brief_path_value else None
    patch_path_value = patch_plan_context.get("report_path")
    patch_path = ROOT / patch_path_value if patch_path_value else None

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
        brief_path_value = editor_context.get("brief_path")
        patch_path_value = patch_plan_context.get("report_path")
        has_brief = False
        has_patch_plan = False
        if brief_path_value:
            has_brief = (ROOT / brief_path_value).exists()
        if patch_path_value:
            has_patch_plan = (ROOT / patch_path_value).exists()

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
            f"brief={'yes' if row['has_brief'] else 'no'} | patch={'yes' if row['has_patch_plan'] else 'no'}"
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
    brief_parser.add_argument("run_id", help="Run manifest basename without .json")

    patch_parser = subparsers.add_parser(
        "patch-plan",
        help="Create a proposal-only patch plan from an existing draft brief run.",
    )
    patch_parser.add_argument("run_id", help="Run manifest basename without .json")

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
        return cmd_brief(args.run_id)
    if args.command == "patch-plan":
        return cmd_patch_plan(args.run_id)
    if args.command == "run":
        return cmd_run(args.topic_id)
    if args.command == "bundle":
        return cmd_bundle(args.topic_id)
    if args.command == "bundle-run":
        return cmd_bundle_run(args.run_id)

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
