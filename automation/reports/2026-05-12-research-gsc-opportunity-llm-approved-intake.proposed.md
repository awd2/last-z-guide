# Proposed Edits: 2026-05-12-research-gsc-opportunity-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `research.html` from `research-gsc-opportunity`.
- Status: `proposal_ready`
- Risk: `high`
- Cluster: `Research`
- Target: `research.html`
- Archetype: `cornerstone-guide`

## Review Rule

- This report is proposal-only.
- It does not modify site content.
- Apply only after human review changes `approval_state` from `proposed` to `approved` in a future approved-apply workflow.
- Generated research pages must be edited through JSON source files and regenerated.

## Source Files

- research.html

## `research.html`

### first_screen_update

- Target output: `research.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Research Guide (2026) — Research Tree, Peace Shield, Urgent Rescue, T10 Order | h1: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path | meta: Step-by-step Last Z research tree guide: what to research first, how to unlock Peace Shield and Urgent Rescue, and the best path toward T10. | verified: Best Last Z research order for most players: Hero Training to Cockpit, Military Strategies for efficient combat stats, Peace Shield for Urgent Rescue, then the shortest practical path toward UST and T10.

Desired after:
Opening answer matches the page role for research.html, gives the exact setup answer quickly, and avoids drifting into a broader hub page.

Suggested content:
No exact snippet generated; use the desired-after summary as the review target.

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### meta_refresh

- Target output: `research.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Research Guide (2026) — Research Tree, Peace Shield, Urgent Rescue, T10 Order | h1: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path | meta: Step-by-step Last Z research tree guide: what to research first, how to unlock Peace Shield and Urgent Rescue, and the best path toward T10. | verified: Best Last Z research order for most players: Hero Training to Cockpit, Military Strategies for efficient combat stats, Peace Shield for Urgent Rescue, then the shortest practical path toward UST and T10.

Desired after:
Title, H1, and meta description use the same exact intent: research.html.

Suggested content:
No exact snippet generated; use the desired-after summary as the review target.

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

