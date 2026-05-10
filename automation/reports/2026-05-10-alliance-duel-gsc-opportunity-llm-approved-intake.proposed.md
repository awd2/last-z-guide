# Proposed Edits: 2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `alliance-duel.html` from `alliance-duel-gsc-opportunity`.
- Status: `proposal_ready`
- Risk: `medium`
- Cluster: `Events`
- Target: `alliance-duel.html`
- Archetype: `event-guide`

## Review Rule

- This report is proposal-only.
- It does not modify site content.
- Apply only after human review changes `approval_state` from `proposed` to `approved` in a future approved-apply workflow.
- Generated research pages must be edited through JSON source files and regenerated.

## Source Files

- alliance-duel.html

## `alliance-duel.html`

### first_screen_update

- Target output: `alliance-duel.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Alliance Duel Guide (2026) — Schedule, Day 1–6 Plan, VS Strategy | h1: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy | meta: Complete Last Z Alliance Duel schedule: Day 1–6 plan, when to use speed-ups, how VS schedule works, and the best F2P strategy for more weekly chests. | verified: Best Alliance Duel plan for most players: follow the Day 1–6 schedule, match speed-ups to the right day, sync with Full Preparedness, and prioritize Alliance Recognition for long-term rewards.

Desired after:
Opening answer matches the page role for alliance-duel.html, gives the exact setup answer quickly, and avoids drifting into a broader hub page.

Suggested content:
No exact snippet generated; use the desired-after summary as the review target.

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### meta_refresh

- Target output: `alliance-duel.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Alliance Duel Guide (2026) — Schedule, Day 1–6 Plan, VS Strategy | h1: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy | meta: Complete Last Z Alliance Duel schedule: Day 1–6 plan, when to use speed-ups, how VS schedule works, and the best F2P strategy for more weekly chests. | verified: Best Alliance Duel plan for most players: follow the Day 1–6 schedule, match speed-ups to the right day, sync with Full Preparedness, and prioritize Alliance Recognition for long-term rewards.

Desired after:
Title, H1, and meta description use the same exact intent: alliance-duel.html.

Suggested content:
No exact snippet generated; use the desired-after summary as the review target.

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

