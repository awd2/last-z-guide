# Review Bundle: 2026-04-22-research-cluster-nav

## Overview

- Summary: Update the existing page `research-costs.html` for the `Research` cluster using the `atlas-page` archetype.
- Status: `reviewed`
- Risk: `medium`
- Run type: `update_existing`

## Inputs

- Topic ID: `research-cluster-nav`
- Title: Research cost cluster local navigation
- Cluster: `Research`
- Source type: `product`
- Source reference: Known rollout next step from research atlas project
- Confidence: `high`
- Priority: `high`

## Plan

- Target: `research-costs.html`
- Recommended action: `update_existing`
- Archetype: `atlas-page`
- Plan summary: Update the existing page `research-costs.html` for the `Research` cluster using the `atlas-page` archetype.

### Memory Files To Consult

- automation/memory/content_index.json
- automation/memory/site_style_guide.md
- automation/memory/page_archetypes.md
- automation/memory/release_checklist.md
- automation/memory/topic_backlog.csv
- automation/memory/canonical_claims.json
- automation/memory/entities.json

### Related Pages

- alliance-recognition-cost.html
- army-building-cost.html
- field-research.html
- fully-armed-alliance-cost.html
- hero-training-cost.html
- military-strategies-cost.html
- research-costs.html

### Deterministic Checks

- python3 automation/run_checks.py
- python3 scripts/generate_research_branch.py <data-file-if-applicable>
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py

## Review Context

### Canonical Claims To Respect

- alliance-recognition-utility-page
- field-research-follows-siege
- hero-training-cockpit-stop
- peace-shield-value
- research-atlas-role
- research-best-mainline

## Reviewer Scaffold

- Verdict: `needs_human_review`
- Next action: `review_human`

### Open Questions

- None

### Reviewer Notes

Deterministic review scaffold complete. The run should explicitly respect these canonical claims: alliance-recognition-utility-page, field-research-follows-siege, hero-training-cockpit-stop, peace-shield-value, research-atlas-role, research-best-mainline.

## Existing Check Results

- None
