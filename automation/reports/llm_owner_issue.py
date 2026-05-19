#!/usr/bin/env python3
"""Create or update one GitHub owner handoff issue for actionable LLM digests."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_json


REPORTS_DIR = ROOT / "automation" / "reports"
MANIFESTS_DIR = ROOT / "automation" / "manifests"
DEFAULT_DIGEST_PATH = REPORTS_DIR / "llm-owner-digest.json"
DEFAULT_MARKDOWN_PATH = REPORTS_DIR / "llm-owner-digest.md"
DEFAULT_TITLE = "LLM Owner Digest: Action Needed"
ACTIONABLE_STATES = {"owner_review_needed", "ready_for_intake", "blocked_or_failed"}
ACTIVE_RUN_STATUSES = {
    "planned",
    "reviewed",
    "draft_brief_ready",
    "patch_plan_ready",
    "proposal_ready",
    "approved_for_apply",
    "apply_preview_ready",
    "applied_pending_qa",
    "qa_passed",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_url(repository: str, server_url: str, explicit_url: str | None = None) -> str:
    if explicit_url:
        return explicit_url
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if run_id:
        return f"{server_url.rstrip('/')}/{repository}/actions/runs/{run_id}"
    return ""


def read_markdown(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = load_json(path)
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def shell_safe(value: Any) -> str:
    return str(value or "").replace('"', "'")


def discovery_path_for(digest: dict[str, Any]) -> str:
    queue_path = str(digest.get("queue_path") or "")
    if not queue_path:
        return "automation/reports/llm-topic-discovery.json"
    path = Path(queue_path)
    if path.parent.name == "llm-auto-review-queue":
        return str(path.parent / "llm-auto-review-topic-discovery.json")
    return str(path.parent / "llm-topic-discovery.json")


def unique_action_items(digest: dict[str, Any]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    items: list[dict[str, Any]] = []
    for bucket in ("blocked_or_failed", "ready_for_intake", "needs_review"):
        bucket_items = digest.get(bucket, [])
        if not isinstance(bucket_items, list):
            continue
        for item in bucket_items:
            if not isinstance(item, dict):
                continue
            topic_id = str(item.get("topic_id") or "")
            if not topic_id or topic_id in seen:
                continue
            seen.add(topic_id)
            items.append(item)
    return items


def topic_decision_command(discovery_path: str, topic_id: str, state: str, note: str) -> str:
    return (
        "python3 automation/pipeline.py llm-topic-decision "
        f"--discovery {discovery_path} "
        f"--topic-id {topic_id} "
        f"--state {state} "
        "--decided-by OWNER_NAME "
        f"--note \"{shell_safe(note)}\" "
        "--json"
    )


def approved_intake_path(topic_id: str) -> Path | None:
    path = REPORTS_DIR / f"llm-intake-{topic_id}.json"
    if not path.exists():
        return None
    try:
        payload = load_json(path)
    except Exception:
        return None
    if payload.get("state") == "approved_for_intake":
        return path
    return None


def ready_run_plan_path(topic_id: str) -> Path | None:
    path = REPORTS_DIR / f"llm-worker-run-plan-{topic_id}.json"
    if not path.exists():
        path = REPORTS_DIR / f"worker-run-plan-{topic_id}.json"
    if not path.exists():
        return None
    try:
        payload = load_json(path)
    except Exception:
        return None
    if payload.get("state") == "run_plan_ready":
        return path
    return None


def run_topic_label(manifest: dict[str, Any]) -> str:
    topic = manifest.get("topic")
    if isinstance(topic, dict):
        return str(topic.get("id") or topic.get("title") or "")
    artifacts = manifest.get("artifacts")
    if isinstance(artifacts, dict):
        for key in ("worker_intake", "source_chain", "worker_run_plan"):
            value = str(artifacts.get(key) or "")
            if "llm-intake-" in value:
                return value.rsplit("llm-intake-", 1)[-1].removesuffix(".json")
            if "llm-worker-chain-" in value:
                return value.rsplit("llm-worker-chain-", 1)[-1].removesuffix(".json")
            if "worker-run-plan-" in value:
                return value.rsplit("worker-run-plan-", 1)[-1].removesuffix(".json")
    return ""


def run_artifact_path(reports_dir: Path, run_id: str, suffix: str) -> Path | None:
    path = reports_dir / f"{run_id}{suffix}"
    return path if path.exists() else None


def next_run_command(run_id: str, status: str) -> tuple[str, str]:
    commands = {
        "planned": (
            f"/review-run {run_id} Review planned run only: <owner confirms deterministic review scope>",
            "Run deterministic review.",
        ),
        "reviewed": (
            f"/brief-run {run_id} Create brief only: <owner confirms brief scope>",
            "Create the draft brief artifact.",
        ),
        "draft_brief_ready": (
            f"/patch-plan-run {run_id} Create proposal-only patch plan: <owner confirms patch-planning scope>",
            "Create the proposal-only patch plan.",
        ),
        "patch_plan_ready": (
            f"/propose-run {run_id} Render owner-review proposal: <owner confirms proposal rendering scope>",
            "Render exact owner-review proposal text.",
        ),
        "proposal_ready": (
            f"/approve-proposal {run_id} Approve rendered proposal specs only: <owner confirms exact before/after text>",
            "Approve rendered proposal specs only; this still does not apply content.",
        ),
        "approved_for_apply": (
            f"/preview-apply {run_id} Render no-write apply preview only: <owner requests final preview before any apply>",
            "Render no-write apply preview.",
        ),
        "apply_preview_ready": (
            "",
            "Ready for local final apply review; no GitHub content-apply command is available.",
        ),
        "applied_pending_qa": (
            "",
            "Run strict QA locally before closeout.",
        ),
        "qa_passed": (
            "",
            "Run closeout locally after final owner review.",
        ),
    }
    return commands.get(status, ("", "No issue-command next step is available for this status."))


def active_run_lifecycle(manifest_dir: Path = MANIFESTS_DIR, reports_dir: Path = REPORTS_DIR) -> list[dict[str, Any]]:
    if not manifest_dir.exists():
        return []
    items: list[dict[str, Any]] = []
    for path in sorted(manifest_dir.glob("*.json")):
        if path.name == "run_manifest.example.json":
            continue
        manifest = load_json_if_exists(path)
        if not manifest:
            continue
        status = str(manifest.get("status") or "")
        if status not in ACTIVE_RUN_STATUSES:
            continue
        run_id = str(manifest.get("run_id") or path.stem)
        command, next_step = next_run_command(run_id, status)
        artifact_paths = {
            "brief_path": run_artifact_path(reports_dir, run_id, ".brief.md"),
            "patch_path": run_artifact_path(reports_dir, run_id, ".patch.md"),
            "proposal_path": run_artifact_path(reports_dir, run_id, ".proposed.md"),
            "apply_preview_path": run_artifact_path(reports_dir, run_id, ".apply-preview.md"),
        }
        items.append(
            {
                "run_id": run_id,
                "status": status,
                "topic": run_topic_label(manifest),
                "manifest_path": rel(path),
                "changed_files": manifest.get("changed_files") if isinstance(manifest.get("changed_files"), list) else [],
                "next_step": next_step,
                "comment_command": command,
                **{key: rel(value) if value else "" for key, value in artifact_paths.items()},
            }
        )
    return items


def render_local_apply_handoff(item: dict[str, Any]) -> list[str]:
    if item.get("status") != "apply_preview_ready":
        return []
    run_id = str(item.get("run_id") or "")
    preview_path = str(item.get("apply_preview_path") or "")
    lines = [
        "",
        "Local final apply review:",
        "",
        "- GitHub automation has stopped before any content-changing step.",
        "- Review the apply preview and approved proposal artifacts locally.",
        "- Continue only after explicit final owner approval for the exact content change.",
        "- `apply-approved` is intentionally local-only and is not available as a GitHub issue comment command.",
    ]
    if preview_path:
        lines.append(f"- Apply preview: `{preview_path}`")
    lines.extend(
        [
            "",
            "Local-only commands after final owner approval:",
            "",
            "```bash",
            f"python3 automation/pipeline.py apply-approved {run_id}",
            f"python3 automation/pipeline.py checks --strict --manifest {run_id}",
            f"python3 automation/pipeline.py close-run {run_id} --note \"Owner reviewed local output and strict QA passed.\"",
            "```",
        ]
    )
    return lines


def render_run_lifecycle(manifest_dir: Path = MANIFESTS_DIR, reports_dir: Path = REPORTS_DIR) -> list[str]:
    items = active_run_lifecycle(manifest_dir, reports_dir)
    if not items:
        return []
    lines = [
        "## Active Run Lifecycle",
        "",
        "These are existing automation manifests that still have a safe next owner step. Commands below continue the controlled lifecycle and do not apply public content.",
        "",
    ]
    for item in items:
        changed = item.get("changed_files") or []
        artifacts = [
            item.get("brief_path", ""),
            item.get("patch_path", ""),
            item.get("proposal_path", ""),
            item.get("apply_preview_path", ""),
        ]
        artifact_lines = [f"- Artifact: `{artifact}`" for artifact in artifacts if artifact]
        lines.extend(
            [
                f"### `{item['run_id']}`",
                "",
                f"- Status: `{item['status']}`",
                f"- Topic: `{item.get('topic', '')}`",
                f"- Manifest: `{item['manifest_path']}`",
                f"- Changed files: `{', '.join(changed) if changed else ''}`",
                f"- Next step: {item['next_step']}",
            ]
        )
        lines.extend(artifact_lines)
        if item.get("comment_command"):
            lines.extend(["", "GitHub issue comment command:", "", "```text", str(item["comment_command"]), "```"])
        else:
            lines.append("- GitHub issue comment command: `none`")
        lines.extend(render_local_apply_handoff(item))
        lines.append("")
    return lines


def render_owner_commands(digest: dict[str, Any]) -> list[str]:
    items = unique_action_items(digest)
    if not items:
        return []
    discovery_path = discovery_path_for(digest)
    lines = [
        "## Owner Commands",
        "",
        "Choose at most one decision command per topic. GitHub comment commands are preferred; local CLI commands are included as a fallback. These commands only record owner decisions, intake scope, run-plan scope, or planned-manifest scope; they do not approve public copy, patch specs, PRs, or deployment.",
        "",
    ]
    for item in items:
        topic_id = str(item.get("topic_id") or "")
        target = str(item.get("target_page_or_slug") or "")
        priority = str(item.get("priority") or "")
        risk = str(item.get("risk_level") or "")
        comment_commands = [
            f"/monitor {topic_id} Monitor {topic_id}: <why this should wait>",
            f"/reject {topic_id} Reject {topic_id}: <why this should not proceed>",
            f"/approve-chain {topic_id} Approve {topic_id} for no-write chain: <validated player value and claim scope>",
        ]
        intake = str(item.get("approve_for_intake_command") or "")
        if intake:
            comment_commands.append(f"/approve-intake {topic_id} Approve {topic_id} for intake only: <owner answers and intake scope>")
        if approved_intake_path(topic_id):
            comment_commands.append(f"/approve-run-plan {topic_id} Approve {topic_id} for no-write run-plan only: <owner confirms run-plan scope>")
        if ready_run_plan_path(topic_id):
            comment_commands.append(f"/dry-run-manifest {topic_id} Dry-run planned manifest for {topic_id}: <owner confirms manifest scope>")
            comment_commands.append(f"/approve-manifest {topic_id} Create planned manifest for {topic_id}: <owner confirms manifest creation>")
        lines.extend(
            [
                f"### `{topic_id}`",
                "",
                f"- Target: `{target}`",
                f"- Priority: `{priority}`",
                f"- Risk: `{risk}`",
                "",
                "GitHub issue comment commands:",
                "",
                "```text",
                *comment_commands,
                "```",
                "",
                "Monitor:",
                "",
                "```bash",
                topic_decision_command(discovery_path, topic_id, "monitor", f"Monitor {topic_id}: <why this should wait>"),
                "```",
                "",
                "Reject:",
                "",
                "```bash",
                topic_decision_command(discovery_path, topic_id, "rejected", f"Reject {topic_id}: <why this should not proceed>"),
                "```",
                "",
                "Approve for no-write worker chain:",
                "",
                "```bash",
                topic_decision_command(
                    discovery_path,
                    topic_id,
                    "approved_for_chain",
                    f"Approve {topic_id} for no-write chain: <validated player value and claim scope>",
                ),
                "```",
                "",
            ]
        )
        if intake:
            intake = intake.replace("--approved-by <owner>", "--approved-by OWNER_NAME")
            lines.extend(["Approve intake from completed chain:", "", "```bash", intake, "```", ""])
        approved_intake = approved_intake_path(topic_id)
        if approved_intake:
            lines.extend(
                [
                    "Approve run-plan from committed intake:",
                    "",
                    "```bash",
                    "python3 automation/pipeline.py worker-run-plan "
                    f"--intake {rel(approved_intake)} "
                    f"--basename llm-worker-run-plan-{topic_id} "
                    "--json",
                    "```",
                    "",
                ]
            )
        ready_run_plan = ready_run_plan_path(topic_id)
        if ready_run_plan:
            lines.extend(
                [
                    "Dry-run planned manifest from run-plan:",
                    "",
                    "```bash",
                    "python3 automation/pipeline.py worker-manifest "
                    f"--run-plan {rel(ready_run_plan)} "
                    "--created-by OWNER_NAME "
                    "--dry-run "
                    "--json",
                    "```",
                    "",
                ]
            )
        chain_markdown = str(item.get("chain_markdown") or "")
        if chain_markdown:
            lines.extend([f"- Review artifact: `{chain_markdown}`", ""])
    return lines


def render_issue_body(
    digest: dict[str, Any],
    markdown: str,
    workflow_url: str,
    manifest_dir: Path = MANIFESTS_DIR,
    reports_dir: Path = REPORTS_DIR,
) -> str:
    counts = digest.get("counts", {}) if isinstance(digest.get("counts"), dict) else {}
    lines = [
        "<!-- llm-owner-digest-handoff -->",
        "# LLM Owner Digest: Action Needed",
        "",
        "This issue was generated by the no-write LLM auto-review queue because the owner digest needs attention.",
        "",
        "## Summary",
        "",
        f"- State: `{digest.get('state', '')}`",
        f"- Recommended next action: {digest.get('recommended_next_action', '')}",
        f"- Generated at: `{digest.get('generated_at', '')}`",
        f"- Candidate topics: `{counts.get('candidate_topics', 0)}`",
        f"- Needs owner review: `{counts.get('digest_needs_review', 0)}`",
        f"- Ready for intake: `{counts.get('digest_ready_for_intake', 0)}`",
        f"- Blocked or failed: `{counts.get('digest_failed', 0)}`",
        f"- Resolved by decision: `{counts.get('resolved_by_owner_decision', 0)}`",
    ]
    if workflow_url:
        lines.append(f"- Workflow run: {workflow_url}")
    lines.extend(
        [
            "",
            "## Safety",
            "",
            "- This issue does not approve public copy.",
            "- The underlying automation did not edit content, backlog, manifests, PRs, or production state.",
            "- Public content still requires exact proposed text, owner approval, apply-preview, apply-approved, and strict QA.",
        ]
    )
    lines.extend(["", *render_owner_commands(digest)])
    lines.extend(["", *render_run_lifecycle(manifest_dir, reports_dir)])
    if markdown:
        lines.extend(["", "## Digest", "", markdown])
    return "\n".join(lines)


def render_resolved_issue_body(digest: dict[str, Any], workflow_url: str) -> str:
    counts = digest.get("counts", {}) if isinstance(digest.get("counts"), dict) else {}
    lines = [
        "<!-- llm-owner-digest-handoff -->",
        "# LLM Owner Digest: Resolved",
        "",
        "The latest no-write LLM owner digest no longer needs owner action, so this handoff issue was closed automatically.",
        "",
        "## Latest Digest",
        "",
        f"- State: `{digest.get('state', '')}`",
        f"- Recommended next action: {digest.get('recommended_next_action', '')}",
        f"- Generated at: `{digest.get('generated_at', '')}`",
        f"- Candidate topics: `{counts.get('candidate_topics', 0)}`",
        f"- Needs owner review: `{counts.get('digest_needs_review', 0)}`",
        f"- Ready for intake: `{counts.get('digest_ready_for_intake', 0)}`",
        f"- Blocked or failed: `{counts.get('digest_failed', 0)}`",
        f"- Resolved by decision: `{counts.get('resolved_by_owner_decision', 0)}`",
    ]
    if workflow_url:
        lines.append(f"- Workflow run: {workflow_url}")
    lines.extend(
        [
            "",
            "## Safety",
            "",
            "- This closure does not approve public copy.",
            "- The underlying automation did not edit content, backlog, manifests, PRs, or production state.",
        ]
    )
    return "\n".join(lines)


def github_request(
    api_url: str,
    token: str,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> Any:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        f"{api_url.rstrip('/')}{path}",
        data=body,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {method} {path} failed with {exc.code}: {details}") from exc
    return json.loads(text) if text else {}


def find_open_issue(api_url: str, token: str, repository: str, title: str) -> dict[str, Any] | None:
    issues = github_request(api_url, token, "GET", f"/repos/{repository}/issues?state=open&per_page=100")
    if not isinstance(issues, list):
        return None
    for issue in issues:
        if issue.get("pull_request"):
            continue
        if issue.get("title") == title:
            return issue
    return None


def upsert_issue(
    digest: dict[str, Any],
    markdown: str,
    repository: str,
    token: str,
    api_url: str,
    server_url: str,
    title: str,
    explicit_run_url: str | None,
    manifest_dir: Path,
    reports_dir: Path,
) -> dict[str, Any]:
    body = render_issue_body(digest, markdown, run_url(repository, server_url, explicit_run_url), manifest_dir, reports_dir)
    existing = find_open_issue(api_url, token, repository, title)
    if existing:
        issue = github_request(
            api_url,
            token,
            "PATCH",
            f"/repos/{repository}/issues/{existing['number']}",
            {"title": title, "body": body},
        )
        return {"action": "updated", "issue_number": issue.get("number"), "issue_url": issue.get("html_url")}
    issue = github_request(
        api_url,
        token,
        "POST",
        f"/repos/{repository}/issues",
        {"title": title, "body": body},
    )
    return {"action": "created", "issue_number": issue.get("number"), "issue_url": issue.get("html_url")}


def close_resolved_issue(
    digest: dict[str, Any],
    repository: str,
    token: str,
    api_url: str,
    server_url: str,
    title: str,
    explicit_run_url: str | None,
) -> dict[str, Any]:
    existing = find_open_issue(api_url, token, repository, title)
    if not existing:
        return {"action": "skipped_non_actionable", "issue_number": None, "issue_url": None}
    body = render_resolved_issue_body(digest, run_url(repository, server_url, explicit_run_url))
    issue = github_request(
        api_url,
        token,
        "PATCH",
        f"/repos/{repository}/issues/{existing['number']}",
        {
            "title": title,
            "body": body,
            "state": "closed",
            "state_reason": "completed",
        },
    )
    return {"action": "closed_resolved", "issue_number": issue.get("number"), "issue_url": issue.get("html_url")}


def build_summary(
    digest_path: Path,
    markdown_path: Path,
    repository: str,
    token: str,
    api_url: str,
    server_url: str,
    title: str,
    explicit_run_url: str | None,
    dry_run: bool,
    manifest_dir: Path = MANIFESTS_DIR,
    reports_dir: Path = REPORTS_DIR,
) -> dict[str, Any]:
    digest = load_json(digest_path)
    state = digest.get("state", "")
    lifecycle_items = active_run_lifecycle(manifest_dir, reports_dir)
    actionable = state in ACTIONABLE_STATES or bool(lifecycle_items)
    summary: dict[str, Any] = {
        "state": state,
        "actionable": actionable,
        "active_run_count": len(lifecycle_items),
        "digest_path": rel(digest_path),
        "markdown_path": rel(markdown_path),
        "issue_title": title,
        "action": "skipped_non_actionable",
        "issue_number": None,
        "issue_url": None,
        "safety": "Owner issue handoff only. No content, backlog, manifest, PR, or production files were modified.",
    }
    if not actionable:
        if dry_run:
            summary.update(
                {
                    "action": "dry_run_non_actionable",
                    "resolved_issue_body": render_resolved_issue_body(
                        digest,
                        run_url(repository, server_url, explicit_run_url),
                    ),
                }
            )
            return summary
        if repository and token:
            summary.update(close_resolved_issue(digest, repository, token, api_url, server_url, title, explicit_run_url))
        return summary
    markdown = read_markdown(markdown_path)
    if dry_run:
        summary.update(
            {
                "action": "dry_run",
                "issue_body": render_issue_body(
                    digest,
                    markdown,
                    run_url(repository, server_url, explicit_run_url),
                    manifest_dir,
                    reports_dir,
                ),
            }
        )
        return summary
    if not repository:
        raise RuntimeError("GITHUB_REPOSITORY or --repository is required for actionable owner issue handoff.")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required for actionable owner issue handoff.")
    summary.update(upsert_issue(digest, markdown, repository, token, api_url, server_url, title, explicit_run_url, manifest_dir, reports_dir))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Create/update one GitHub owner issue for actionable LLM owner digests.")
    parser.add_argument("--digest", default=str(DEFAULT_DIGEST_PATH), help="Path to llm-owner-digest.json.")
    parser.add_argument("--markdown", default=str(DEFAULT_MARKDOWN_PATH), help="Path to llm-owner-digest.md.")
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", ""), help="Repository in owner/name form.")
    parser.add_argument("--api-url", default=os.environ.get("GITHUB_API_URL", "https://api.github.com"), help="GitHub API base URL.")
    parser.add_argument("--server-url", default=os.environ.get("GITHUB_SERVER_URL", "https://github.com"), help="GitHub web base URL.")
    parser.add_argument("--run-url", help="Explicit workflow run URL.")
    parser.add_argument("--title", default=DEFAULT_TITLE, help="GitHub issue title to create/update.")
    parser.add_argument("--token-env", default="GITHUB_TOKEN", help="Environment variable containing the GitHub token.")
    parser.add_argument("--manifest-dir", default=str(MANIFESTS_DIR), help="Directory to scan for active lifecycle manifests.")
    parser.add_argument("--reports-dir", default=str(REPORTS_DIR), help="Directory to scan for lifecycle reports.")
    parser.add_argument("--dry-run", action="store_true", help="Render the handoff without calling the GitHub API.")
    parser.add_argument("--body-output", help="Optional path to write the rendered dry-run issue body.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    args = parser.parse_args()

    try:
        summary = build_summary(
            resolve_path(args.digest),
            resolve_path(args.markdown),
            args.repository,
            os.environ.get(args.token_env, ""),
            args.api_url,
            args.server_url,
            args.title,
            args.run_url,
            args.dry_run,
            resolve_path(args.manifest_dir),
            resolve_path(args.reports_dir),
        )
    except Exception as exc:
        if args.json:
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"LLM owner issue handoff failed: {exc}")
        return 1
    if args.body_output:
        body = summary.get("issue_body") or summary.get("resolved_issue_body") or ""
        if body:
            body_path = resolve_path(args.body_output)
            write_text(body_path, body)
            summary["body_output"] = rel(body_path)
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"State: {summary['state']}")
        print(f"Action: {summary['action']}")
        if summary.get("issue_url"):
            print(f"Issue: {summary['issue_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
