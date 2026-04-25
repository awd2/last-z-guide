#!/usr/bin/env python3
"""Build a deterministic change plan from a backlog item."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_canonical_claims, load_content_index, load_topic_backlog
from automation.models import TopicBacklogItem


@dataclass(slots=True)
class ChangePlan:
    topic_id: str
    title: str
    cluster: str
    recommended_action: str
    archetype_suggestion: str
    target_page_or_slug: str
    source_type: str
    source_reference: str
    confidence: str
    priority: str
    status: str
    risk_level: str
    plan_summary: str
    memory_files: list[str] = field(default_factory=list)
    related_pages: list[str] = field(default_factory=list)
    deterministic_checks: list[str] = field(default_factory=list)
    notes: str = ""


def infer_risk(item: TopicBacklogItem) -> str:
    target = item.target_page_or_slug
    if item.recommended_action == "create_new":
        return "high"
    if target in {"index.html", "research.html", "heroes.html", "events.html", "codes.html"}:
        return "high"
    if item.cluster in {"Seasons", "Research"} and item.recommended_action != "update_existing":
        return "high"
    if item.priority == "high":
        return "medium"
    return "low"


def build_plan_summary(item: TopicBacklogItem) -> str:
    action_map = {
        "update_existing": "Update the existing page",
        "create_new": "Create a new page or file",
        "atlas_update": "Update the relevant atlas or hub",
        "reject": "Reject this item",
    }
    prefix = action_map.get(item.recommended_action, "Handle this item")
    return (
        f"{prefix} `{item.target_page_or_slug}` for the `{item.cluster}` cluster "
        f"using the `{item.archetype_suggestion}` archetype."
    )


def select_memory_files(item: TopicBacklogItem) -> list[str]:
    files = [
        "automation/memory/content_index.json",
        "automation/memory/site_style_guide.md",
        "automation/memory/page_archetypes.md",
        "automation/memory/release_checklist.md",
        "automation/memory/topic_backlog.csv",
    ]

    cluster_specific = {
        "Research": "automation/memory/canonical_claims.json",
        "Economy": "automation/memory/canonical_claims.json",
        "Seasons": "automation/memory/canonical_claims.json",
        "Events": "automation/memory/entities.json",
        "PvP": "automation/memory/entities.json",
    }
    extra = cluster_specific.get(item.cluster)
    if extra and extra not in files:
        files.append(extra)

    if "entities.json" not in files:
        files.append("automation/memory/entities.json")

    return files


def find_related_pages(item: TopicBacklogItem) -> list[str]:
    pages = load_content_index()
    filename = Path(item.target_page_or_slug).name

    cluster_pages = sorted(
        page.filename
        for page in pages
        if page.cluster == item.cluster and page.filename != filename
    )

    related = []
    if filename.endswith(".html"):
        related.append(filename)
    related.extend(cluster_pages[:6])
    return related


def deterministic_checks_for(item: TopicBacklogItem) -> list[str]:
    checks = [
        "python3 automation/run_checks.py",
        "python3 scripts/prepublish_check.py --fix",
        "python3 scripts/prepublish_check.py",
    ]
    if item.cluster == "Research" and item.target_page_or_slug.endswith(".html"):
        checks.insert(1, "python3 scripts/generate_research_branch.py <data-file-if-applicable>")
    return checks


def get_backlog_item(topic_id: str) -> TopicBacklogItem:
    for item in load_topic_backlog():
        if item.topic_id == topic_id:
            return item
    raise KeyError(f"Unknown topic_id: {topic_id}")


def build_change_plan(item: TopicBacklogItem) -> ChangePlan:
    # Touch the memory layers intentionally so planner stays aligned with them.
    _ = load_canonical_claims()

    return ChangePlan(
        topic_id=item.topic_id,
        title=item.title,
        cluster=item.cluster,
        recommended_action=item.recommended_action,
        archetype_suggestion=item.archetype_suggestion,
        target_page_or_slug=item.target_page_or_slug,
        source_type=item.source_type,
        source_reference=item.source_reference,
        confidence=item.confidence,
        priority=item.priority,
        status=item.status,
        risk_level=infer_risk(item),
        plan_summary=build_plan_summary(item),
        memory_files=select_memory_files(item),
        related_pages=find_related_pages(item),
        deterministic_checks=deterministic_checks_for(item),
        notes=item.notes,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic change plan from a backlog item.")
    parser.add_argument("topic_id", help="Backlog topic_id to plan.")
    parser.add_argument("--json", action="store_true", help="Print the plan as JSON.")
    args = parser.parse_args()

    item = get_backlog_item(args.topic_id)
    plan = build_change_plan(item)

    if args.json:
        print(json.dumps(asdict(plan), indent=2, ensure_ascii=False))
    else:
        print(f"Topic: {plan.topic_id}")
        print(f"Title: {plan.title}")
        print(f"Cluster: {plan.cluster}")
        print(f"Action: {plan.recommended_action}")
        print(f"Archetype: {plan.archetype_suggestion}")
        print(f"Target: {plan.target_page_or_slug}")
        print(f"Risk: {plan.risk_level}")
        print(f"Summary: {plan.plan_summary}")
        print("Memory files:")
        for path in plan.memory_files:
            print(f"  - {path}")
        print("Related pages:")
        for path in plan.related_pages:
            print(f"  - {path}")
        print("Deterministic checks:")
        for check in plan.deterministic_checks:
            print(f"  - {check}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
