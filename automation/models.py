#!/usr/bin/env python3
"""Typed models for the automation layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ContentIndexPage:
    filename: str
    url: str
    cluster: str
    archetype: str
    status: str | None = None
    freshness_priority: str | None = None
    title_hint: str | None = None


@dataclass(slots=True)
class CanonicalClaim:
    id: str
    category: str
    status: str
    confidence: str
    summary: str
    implications: list[str] = field(default_factory=list)
    related_pages: list[str] = field(default_factory=list)


@dataclass(slots=True)
class TopicBacklogItem:
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
    notes: str = ""


@dataclass(slots=True)
class RunCheckResult:
    status: str
    notes: str = ""


@dataclass(slots=True)
class RunReview:
    verdict: str
    open_questions: list[str] = field(default_factory=list)
    next_action: str = ""
    reviewer_notes: str = ""


@dataclass(slots=True)
class RunManifest:
    run_id: str
    created_at: str
    run_type: str
    status: str
    risk_level: str
    summary: str
    inputs: dict[str, Any] = field(default_factory=dict)
    plan: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, Any] = field(default_factory=dict)
    changed_files: list[str] = field(default_factory=list)
    checks: dict[str, RunCheckResult] = field(default_factory=dict)
    review: RunReview | None = None
