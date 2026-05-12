# Proposed Edits: 2026-05-12-research-gsc-opportunity-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `research.html` from `research-gsc-opportunity`.
- Status: `approved_for_apply`
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
- Approval state: `approved`
- Generator command: `None`

Before:
title: Last Z Research Guide (2026) - Best Research Order, Peace Shield, UST/T10 Path | h1: Last Z Research Guide - Best Research Order, Peace Shield, and UST/T10 Path | meta: Best Last Z research order for most players: Hero Training to Cockpit, Military Strategies, Peace Shield for Urgent Rescue, then choose UST/T10 or late Field Research by goal. | verified: Best Last Z research order for most players: Hero Training to Cockpit, Military Strategies for efficient combat stats, Peace Shield for Urgent Rescue, then choose between the shortest practical UST/T10 path or late Field Research based on your account goal.

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
- Approval state: `approved`
- Generator command: `None`

Before:
title: Last Z Research Guide (2026) - Best Research Order, Peace Shield, UST/T10 Path | h1: Last Z Research Guide - Best Research Order, Peace Shield, and UST/T10 Path | meta: Best Last Z research order for most players: Hero Training to Cockpit, Military Strategies, Peace Shield for Urgent Rescue, then choose UST/T10 or late Field Research by goal. | verified: Best Last Z research order for most players: Hero Training to Cockpit, Military Strategies for efficient combat stats, Peace Shield for Urgent Rescue, then choose between the shortest practical UST/T10 path or late Field Research based on your account goal.

Desired after:
Title, H1, and meta description use the same exact intent: research.html.

Suggested content:
No exact snippet generated; use the desired-after summary as the review target.

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

