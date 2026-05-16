#!/usr/bin/env python3
"""Build a no-write LLM auto-review queue from current candidate signals."""

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
from automation.workers import llm_candidate_refresh, llm_editor, llm_reviewer, llm_scout, llm_worker_chain


REPORTS_DIR = ROOT / "automation" / "reports"
DEFAULT_OUTPUT_DIR = REPORTS_DIR / "llm-auto-review-queue"


PRIORITY_SCORE = {"high": 45, "medium": 25, "low": 5}
CONFIDENCE_SCORE = {"high": 20, "medium": 10, "low": 0}
RISK_SCORE = {"low": 15, "medium": 8, "high": 0}
ACTION_SCORE = {"create_new": 10, "update_existing": 8, "consolidate": 5, "monitor": -20, "reject": -40}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def normalized(value: Any) -> str:
    return str(value or "").strip().lower()


def score_topic(topic: dict[str, Any]) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = 0
    priority = normalized(topic.get("priority"))
    confidence = normalized(topic.get("confidence"))
    risk = normalized(topic.get("risk_level"))
    action = normalized(topic.get("recommended_action"))
    status = normalized(topic.get("status"))

    score += PRIORITY_SCORE.get(priority, 0)
    reasons.append(f"priority:{priority or 'unknown'}={PRIORITY_SCORE.get(priority, 0)}")
    score += CONFIDENCE_SCORE.get(confidence, 0)
    reasons.append(f"confidence:{confidence or 'unknown'}={CONFIDENCE_SCORE.get(confidence, 0)}")
    score += RISK_SCORE.get(risk, 0)
    reasons.append(f"risk:{risk or 'unknown'}={RISK_SCORE.get(risk, 0)}")
    score += ACTION_SCORE.get(action, 0)
    reasons.append(f"action:{action or 'unknown'}={ACTION_SCORE.get(action, 0)}")
    if status == "candidate":
        score += 10
        reasons.append("candidate_status=10")
    if topic.get("prior_review"):
        score -= 30
        reasons.append("prior_review=-30")
    if topic.get("target_page_or_slug") == "news-preview.html":
        score -= 100
        reasons.append("archived_news_preview=-100")
    return score, reasons


def chain_summary_candidates(topic_id: str, search_dirs: list[Path]) -> list[Path]:
    candidates: list[Path] = []
    for directory in search_dirs:
        path = directory / f"llm-worker-chain-{topic_id}.json"
        if path.exists():
            candidates.append(path)
    return candidates


def chain_contract_version(payload: dict[str, Any]) -> int:
    try:
        return int(payload.get("worker_chain_contract_version") or 0)
    except (TypeError, ValueError):
        return 0


def completed_chain_status(topic_id: str, search_dirs: list[Path]) -> dict[str, Any] | None:
    for path in chain_summary_candidates(topic_id, search_dirs):
        try:
            payload = load_json(path)
        except Exception:
            continue
        if payload.get("state") == "completed":
            version = chain_contract_version(payload)
            required = llm_worker_chain.WORKER_CHAIN_CONTRACT_VERSION
            return {
                "path": rel(path),
                "contract_version": version,
                "required_contract_version": required,
                "is_current": version >= required,
                "stale_reason": "" if version >= required else "worker_chain_contract_version is missing or outdated",
            }
    return None


def candidate_topics(discovery_payload: dict[str, Any]) -> list[dict[str, Any]]:
    topics = discovery_payload.get("topics", [])
    if not isinstance(topics, list):
        return []
    return [
        topic
        for topic in topics
        if normalized(topic.get("status")) == "candidate"
        and normalized(topic.get("recommended_action")) in llm_scout.READY_DECISIONS
        and normalized(topic.get("priority")) != "low"
    ]


def build_scout_payload(refresh_payload: dict[str, Any]) -> dict[str, Any]:
    scout_stage = next(
        (stage for stage in refresh_payload.get("stages", []) if stage.get("stage") == "llm_scout"),
        {},
    )
    result_path = str(scout_stage.get("result_path") or "")
    return {
        "request_path": scout_stage.get("request_path"),
        "result_path": result_path,
        "markdown_path": scout_stage.get("markdown_path"),
        "adapter_result": load_json(resolve_path(result_path)) if result_path else {},
    }


def run_queue_item(
    topic: dict[str, Any],
    refresh_payload: dict[str, Any],
    output_dir: Path,
    provider: str,
    editor_fixture_path: Path | None,
    reviewer_fixture_path: Path | None,
) -> dict[str, Any]:
    topic_id = str(topic.get("topic_id") or "")
    scout_payload = build_scout_payload(refresh_payload)
    editor_payload: dict[str, Any] | None = None
    reviewer_payload: dict[str, Any] | None = None
    errors: list[str] = []

    try:
        editor_code, editor_payload = llm_editor.run_llm_editor(
            scout_result_path=resolve_path(str(scout_payload["result_path"])),
            scout_request_path=resolve_path(str(scout_payload["request_path"])),
            topic_id=topic_id,
            output_dir=output_dir,
            basename=f"llm-auto-review-editor-{topic_id}",
            provider=provider,
            fixture_path=editor_fixture_path,
        )
    except ValueError as exc:
        editor_code = 1
        errors.append(f"LLM Editor stage blocked: {exc}")
    if editor_code:
        errors.append("LLM Editor stage failed; Reviewer was not run.")

    if editor_payload and not errors:
        try:
            reviewer_code, reviewer_payload = llm_reviewer.run_llm_reviewer(
                editor_result_path=resolve_path(str(editor_payload["result_path"])),
                editor_request_path=resolve_path(str(editor_payload["request_path"])),
                output_dir=output_dir,
                basename=f"llm-auto-review-reviewer-{topic_id}",
                provider=provider,
                fixture_path=reviewer_fixture_path,
            )
        except ValueError as exc:
            reviewer_code = 1
            errors.append(f"LLM Reviewer stage blocked: {exc}")
        if reviewer_code:
            errors.append("LLM Reviewer stage failed.")

    summary = llm_worker_chain.build_summary(
        provider=provider,
        topic_id=topic_id,
        decision_path=None,
        scout_payload=scout_payload,
        editor_payload=editor_payload,
        reviewer_payload=reviewer_payload,
        generated_at=now_utc(),
        errors=errors,
    )
    chain_json, chain_markdown = llm_worker_chain.write_summary(
        summary,
        output_dir,
        f"llm-worker-chain-{topic_id}",
    )
    return {
        "topic_id": topic_id,
        "target_page_or_slug": topic.get("target_page_or_slug", ""),
        "cluster": topic.get("cluster", ""),
        "priority": topic.get("priority", ""),
        "risk_level": topic.get("risk_level", ""),
        "status": "completed" if summary.get("state") == "completed" else "failed",
        "review_verdict": summary.get("review_verdict"),
        "approved_next_stage": summary.get("approved_next_stage"),
        "owner_approval_required": summary.get("owner_approval_required"),
        "chain_json": rel(chain_json),
        "chain_markdown": rel(chain_markdown),
        "errors": errors,
    }


def blocked_summary(output_dir: Path, basename: str, errors: list[str]) -> dict[str, Any]:
    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    return {
        "schema_version": 1,
        "report_type": "llm_auto_review_queue",
        "generated_at": now_utc(),
        "state": "blocked",
        "provider": "",
        "candidate_topic_count": 0,
        "queued_topic_count": 0,
        "completed_item_count": 0,
        "failed_item_count": 0,
        "skipped_existing_count": 0,
        "queue_items": [],
        "skipped_topics": [],
        "errors": errors,
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "safety": "No content, backlog, manifest, PR, or production files were modified.",
    }


def run_auto_review_queue(
    signal_paths: list[Path],
    external_proposal_paths: list[Path],
    output_dir: Path,
    basename: str,
    provider: str,
    scout_fixture_path: Path | None,
    editor_fixture_path: Path | None,
    reviewer_fixture_path: Path | None,
    limit: int,
    min_impressions: int,
    max_chains: int,
    include_existing: bool,
) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if not signal_paths and not external_proposal_paths:
        summary = blocked_summary(output_dir, basename, ["No Scout signal files or external proposal files were found."])
        write_queue(summary)
        return 1, summary

    refresh_code, refresh_payload = llm_candidate_refresh.run_candidate_refresh(
        signal_paths=signal_paths,
        external_proposal_paths=external_proposal_paths,
        output_dir=output_dir,
        basename="llm-auto-review-candidate-refresh",
        scout_basename="llm-auto-review-scout",
        discovery_basename="llm-auto-review-topic-discovery",
        provider=provider,
        fixture_path=scout_fixture_path,
        limit=limit,
        min_impressions=min_impressions,
    )
    if refresh_code:
        summary = blocked_summary(output_dir, basename, refresh_payload.get("errors", []) or ["Candidate refresh failed."])
        summary["candidate_refresh_path"] = refresh_payload.get("output_path", "")
        summary["candidate_refresh_markdown"] = refresh_payload.get("markdown_path", "")
        write_queue(summary)
        return 1, summary

    discovery_path = resolve_path(str(refresh_payload.get("topic_discovery_path")))
    discovery_payload = load_json(discovery_path)
    candidates = candidate_topics(discovery_payload)
    scored: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    search_dirs = [output_dir, REPORTS_DIR]
    for topic in candidates:
        score, reasons = score_topic(topic)
        topic_id = str(topic.get("topic_id") or "")
        existing_chain = completed_chain_status(topic_id, search_dirs)
        record = {
            "topic_id": topic_id,
            "target_page_or_slug": topic.get("target_page_or_slug", ""),
            "cluster": topic.get("cluster", ""),
            "priority": topic.get("priority", ""),
            "risk_level": topic.get("risk_level", ""),
            "score": score,
            "score_reasons": reasons,
        }
        if existing_chain:
            record["existing_chain"] = existing_chain["path"]
            record["existing_chain_contract_version"] = existing_chain["contract_version"]
            record["required_chain_contract_version"] = existing_chain["required_contract_version"]
            record["existing_chain_current"] = existing_chain["is_current"]
            if not existing_chain["is_current"]:
                record["stale_existing_chain"] = True
                record["stale_reason"] = existing_chain["stale_reason"]
                reasons.append(
                    f"stale_existing_chain_contract={existing_chain['contract_version']}<"
                    f"{existing_chain['required_contract_version']}"
                )
        if existing_chain and existing_chain["is_current"] and not include_existing:
            record["status"] = "skipped_existing_chain"
            skipped.append(record)
            continue
        scored.append({**record, "topic": topic})

    scored.sort(key=lambda item: (-int(item["score"]), str(item["topic_id"])))
    max_chains = max(1, max_chains)
    selected = scored[:max_chains]
    deferred = scored[max_chains:]
    for item in deferred:
        skipped.append({k: v for k, v in item.items() if k != "topic"} | {"status": "deferred_by_limit"})

    queue_items: list[dict[str, Any]] = []
    for item in selected:
        run_record = run_queue_item(
            topic=item["topic"],
            refresh_payload=refresh_payload,
            output_dir=output_dir,
            provider=provider,
            editor_fixture_path=editor_fixture_path,
            reviewer_fixture_path=reviewer_fixture_path,
        )
        queue_items.append(
            {
                **{k: v for k, v in item.items() if k != "topic"},
                **run_record,
            }
        )

    completed = sum(1 for item in queue_items if item.get("status") == "completed")
    failed = sum(1 for item in queue_items if item.get("status") == "failed")
    state = "queue_ready"
    if failed:
        state = "completed_with_failures"
    elif not candidates:
        state = "no_candidates"
    elif not queue_items and skipped:
        state = "current"

    json_path = output_dir / f"{basename}.json"
    markdown_path = output_dir / f"{basename}.md"
    summary = {
        "schema_version": 1,
        "report_type": "llm_auto_review_queue",
        "generated_at": now_utc(),
        "state": state,
        "provider": provider,
        "source_signal_files": [rel(path) for path in signal_paths],
        "external_proposal_files": [rel(path) for path in external_proposal_paths],
        "candidate_refresh_path": refresh_payload.get("output_path", ""),
        "candidate_refresh_markdown": refresh_payload.get("markdown_path", ""),
        "topic_discovery_path": refresh_payload.get("topic_discovery_path", ""),
        "topic_discovery_markdown": refresh_payload.get("topic_discovery_markdown", ""),
        "candidate_topic_count": len(candidates),
        "queued_topic_count": len(queue_items),
        "completed_item_count": completed,
        "failed_item_count": failed,
        "skipped_existing_count": sum(1 for item in skipped if item.get("status") == "skipped_existing_chain"),
        "stale_existing_count": sum(1 for item in queue_items if item.get("stale_existing_chain")),
        "deferred_count": sum(1 for item in skipped if item.get("status") == "deferred_by_limit"),
        "max_chains": max_chains,
        "include_existing": include_existing,
        "required_chain_contract_version": llm_worker_chain.WORKER_CHAIN_CONTRACT_VERSION,
        "required_chain_contract_label": llm_worker_chain.WORKER_CHAIN_CONTRACT_LABEL,
        "queue_items": queue_items,
        "skipped_topics": skipped,
        "errors": [error for item in queue_items for error in item.get("errors", [])],
        "output_path": rel(json_path),
        "markdown_path": rel(markdown_path),
        "allows_content_edit": False,
        "allows_backlog_mutation": False,
        "allows_manifest_mutation": False,
        "allows_pr_or_deploy": False,
        "next_actions": [
            "Review queue_items and open the referenced chain markdown for the best candidate.",
            "Approve only final public content diffs, not this queue artifact.",
            "If a queue item is worth drafting, move it through llm-intake-latest and the existing run-plan/proposal lifecycle.",
        ],
        "safety": "No content, backlog, manifest, PR, or production files were modified.",
    }
    write_queue(summary)
    return (1 if failed else 0), summary


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# LLM Auto Review Queue - {summary['generated_at']}",
        "",
        "## Outcome",
        "",
        f"- State: `{summary['state']}`",
        f"- Provider: `{summary.get('provider', '')}`",
        f"- Candidate topics: `{summary.get('candidate_topic_count', 0)}`",
        f"- Queued topics: `{summary.get('queued_topic_count', 0)}`",
        f"- Completed items: `{summary.get('completed_item_count', 0)}`",
        f"- Failed items: `{summary.get('failed_item_count', 0)}`",
        f"- Skipped existing: `{summary.get('skipped_existing_count', 0)}`",
        f"- Stale existing reruns: `{summary.get('stale_existing_count', 0)}`",
        f"- Required chain contract: `{summary.get('required_chain_contract_version', '')}` `{summary.get('required_chain_contract_label', '')}`",
        f"- Deferred by limit: `{summary.get('deferred_count', 0)}`",
        f"- Candidate refresh: `{summary.get('candidate_refresh_markdown', '')}`",
        f"- Topic discovery: `{summary.get('topic_discovery_markdown', '')}`",
        "- Allows content edit: `false`",
        "- Allows backlog mutation: `false`",
        "- Allows manifest mutation: `false`",
        "- Allows PR/deploy: `false`",
        "- Safety: no content, backlog, manifest, PR, or production files were modified.",
        "",
    ]
    if summary.get("errors"):
        lines.extend(["## Errors", "", md_list(summary["errors"]), ""])
    lines.extend(["## Review Queue", ""])
    if not summary.get("queue_items"):
        lines.extend(["- None", ""])
    for item in summary.get("queue_items", []):
        lines.extend(
            [
                f"### {item.get('topic_id', '')}",
                "",
                f"- Status: `{item.get('status', '')}`",
                f"- Score: `{item.get('score', '')}`",
                f"- Target: `{item.get('target_page_or_slug', '')}`",
                f"- Cluster: `{item.get('cluster', '')}`",
                f"- Priority: `{item.get('priority', '')}`",
                f"- Risk: `{item.get('risk_level', '')}`",
                f"- Verdict: `{item.get('review_verdict')}`",
                f"- Owner approval required: `{str(item.get('owner_approval_required')).lower()}`",
                f"- Chain: `{item.get('chain_markdown', '')}`",
                f"- Existing chain rerun: `{str(item.get('stale_existing_chain', False)).lower()}`",
                "",
                "Score reasons:",
                "",
                md_list(item.get("score_reasons", [])),
                "",
            ]
        )
    if summary.get("skipped_topics"):
        lines.extend(["## Skipped Topics", ""])
        for item in summary["skipped_topics"]:
            lines.extend(
                [
                    f"- `{item.get('topic_id', '')}`: `{item.get('status', '')}`, score `{item.get('score', '')}`"
                    + (f", existing `{item.get('existing_chain')}`" if item.get("existing_chain") else "")
                ]
            )
        lines.append("")
    lines.extend(["## Next Actions", "", md_list(summary.get("next_actions", [])), ""])
    return "\n".join(lines)


def write_queue(summary: dict[str, Any]) -> tuple[Path, Path]:
    json_path = resolve_path(summary["output_path"])
    markdown_path = resolve_path(summary["markdown_path"])
    json_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(json_path, summary)
    markdown_path.write_text(render_markdown(summary), encoding="utf-8")
    return json_path, markdown_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a no-write LLM auto-review queue from current candidate signals.")
    parser.add_argument(
        "--signals",
        action="append",
        help="Path to a GSC/Bing agent signals JSON file. Can be supplied more than once. Defaults to latest GSC and Bing when present.",
    )
    parser.add_argument(
        "--external-proposals",
        action="append",
        help="Path to an External Scout JSON artifact with candidate_proposals. Can be supplied more than once.",
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for auto-review queue artifacts.")
    parser.add_argument("--basename", default="llm-auto-review-queue", help="Queue summary basename.")
    parser.add_argument(
        "--provider",
        default="disabled",
        choices=["disabled", "fixture", "openai"],
        help="Provider passed to LLM stages. Defaults to disabled/fail-closed.",
    )
    parser.add_argument("--scout-fixture", help="Fixture response JSON for offline Scout tests.")
    parser.add_argument("--editor-fixture", help="Fixture response JSON for offline Editor tests.")
    parser.add_argument("--reviewer-fixture", help="Fixture response JSON for offline Reviewer tests.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum deterministic Scout proposals to review.")
    parser.add_argument("--min-impressions", type=int, default=200, help="Minimum page impressions for Scout proposals.")
    parser.add_argument("--max-chains", type=int, default=3, help="Maximum top candidates to auto-review.")
    parser.add_argument("--include-existing", action="store_true", help="Rerun topics with existing completed chain summaries.")
    parser.add_argument("--json", action="store_true", help="Print the queue summary as JSON.")
    args = parser.parse_args()

    signal_paths = [resolve_path(value) for value in args.signals] if args.signals else llm_scout.default_signal_paths()
    external_proposal_paths = [resolve_path(value) for value in args.external_proposals or []]
    code, summary = run_auto_review_queue(
        signal_paths=signal_paths,
        external_proposal_paths=external_proposal_paths,
        output_dir=resolve_path(args.output_dir),
        basename=args.basename,
        provider=args.provider,
        scout_fixture_path=resolve_path(args.scout_fixture) if args.scout_fixture else None,
        editor_fixture_path=resolve_path(args.editor_fixture) if args.editor_fixture else None,
        reviewer_fixture_path=resolve_path(args.reviewer_fixture) if args.reviewer_fixture else None,
        limit=args.limit,
        min_impressions=args.min_impressions,
        max_chains=args.max_chains,
        include_existing=args.include_existing,
    )
    output = {
        "state": summary["state"],
        "provider": summary.get("provider", ""),
        "candidate_topic_count": summary.get("candidate_topic_count", 0),
        "queued_topic_count": summary.get("queued_topic_count", 0),
        "completed_item_count": summary.get("completed_item_count", 0),
        "failed_item_count": summary.get("failed_item_count", 0),
        "skipped_existing_count": summary.get("skipped_existing_count", 0),
        "stale_existing_count": summary.get("stale_existing_count", 0),
        "output_path": summary["output_path"],
        "markdown_path": summary["markdown_path"],
        "errors": summary.get("errors", []),
        "safety": summary["safety"],
    }
    if args.json:
        print(json.dumps(output, indent=2))
    else:
        print(f"State: {output['state']}")
        print(f"Queued topics: {output['queued_topic_count']}")
        print(f"Completed items: {output['completed_item_count']}")
        print(f"Markdown: {output['markdown_path']}")
        if output["errors"]:
            print("Errors:")
            for error in output["errors"]:
                print(f"- {error}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
