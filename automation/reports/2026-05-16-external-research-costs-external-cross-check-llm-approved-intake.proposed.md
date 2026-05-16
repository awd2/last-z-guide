# Proposed Edits: 2026-05-16-external-research-costs-external-cross-check-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `research-costs.html` from `external-research-costs-external-cross-check`.
- Status: `proposal_ready`
- Risk: `high`
- Cluster: `Research`
- Target: `research-costs.html`
- Archetype: `atlas-page`

## Review Rule

- This report is proposal-only.
- It does not modify site content.
- Apply only after human review changes `approval_state` from `proposed` to `approved` in a future approved-apply workflow.
- Generated research pages must be edited through JSON source files and regenerated.

## Source Files

- research-costs.html

## `research-costs.html`

### first_screen_update

- Target output: `research-costs.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Research Costs Atlas (2026) — Branch Comparison, Badge Totals, and Unlock Paths | h1: Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths | meta: Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page before spending badges. | verified: This atlas is the branch router for Last Z research costs: compare badge totals and unlock paths here, then open the exact branch page for node-by-node costs before spending badges.

Desired after:
Opening answer names the atlas role, main research route, and exact branch-page routing without turning the atlas into a giant guide.

Suggested content:
No exact snippet generated; use the desired-after summary as the review target.

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### meta_refresh

- Target output: `research-costs.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Research Costs Atlas (2026) — Branch Comparison, Badge Totals, and Unlock Paths | h1: Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths | meta: Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page before spending badges. | verified: This atlas is the branch router for Last Z research costs: compare badge totals and unlock paths here, then open the exact branch page for node-by-node costs before spending badges.

Desired after:
Title, H1, and meta description use the same exact intent: research costs atlas, branch comparison, badge totals, and unlock paths.

Suggested content:
No exact snippet generated; use the desired-after summary as the review target.

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### atlas_card_update

- Target output: `research-costs.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `atlas cards / branch comparison route block`
- Risk: `low`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Research Costs Atlas (2026) — Branch Comparison, Badge Totals, and Unlock Paths | h1: Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths | meta: Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page before spending badges. | verified: This atlas is the branch router for Last Z research costs: compare badge totals and unlock paths here, then open the exact branch page for node-by-node costs before spending badges.

Desired after:
Atlas cards help users choose the correct branch page and keep the core order visible: Hero Training, Military Strategies, Peace Shield, Siege to Seize, Field Research.

Suggested content:
No exact snippet generated; use the desired-after summary as the review target.

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

