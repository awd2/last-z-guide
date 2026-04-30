# Proposed Edits: 2026-04-22-season-alias-clarification

## Overview

- Summary: Update the existing page `start.html` for the `Seasons` cluster using the `support-guide` archetype.
- Status: `proposal_ready`
- Risk: `low`
- Cluster: `Seasons`
- Target: `start.html`
- Archetype: `support-guide`

## Review Rule

- This report is proposal-only.
- It does not modify site content.
- Apply only after human review changes `approval_state` from `proposed` to `approved` in a future approved-apply workflow.
- Generated research pages must be edited through JSON source files and regenerated.

## Source Files

- start.html

## `start.html`

### first_screen_update

- Target output: `start.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Beginner Guide (2026) — Best Start and Early Mistakes to Avoid | h1: Last Z Beginner Guide — Best Start and Early Mistakes to Avoid | meta: Best beginner path in Last Z: early priorities, key upgrades, alliance timing, and the first mistakes to avoid in your opening days. | verified: Best early plan for most players: finish the tutorial, follow main quests, join an active alliance fast, push HQ correctly, and save diamonds for long-term value instead of random early spending.

Desired after:
Opening answer matches the page role for start.html, gives the exact setup answer quickly, and avoids drifting into a broader hub page.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### meta_refresh

- Target output: `start.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Beginner Guide (2026) — Best Start and Early Mistakes to Avoid | h1: Last Z Beginner Guide — Best Start and Early Mistakes to Avoid | meta: Best beginner path in Last Z: early priorities, key upgrades, alliance timing, and the first mistakes to avoid in your opening days. | verified: Best early plan for most players: finish the tutorial, follow main quests, join an active alliance fast, push HQ correctly, and save diamonds for long-term value instead of random early spending.

Desired after:
Title, H1, and meta description use the same exact intent: start.html.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### internal_link_addition

- Target output: `start.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `Related Guides`
- Risk: `low`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Beginner Guide (2026) — Best Start and Early Mistakes to Avoid | h1: Last Z Beginner Guide — Best Start and Early Mistakes to Avoid | meta: Best beginner path in Last Z: early priorities, key upgrades, alliance timing, and the first mistakes to avoid in your opening days. | verified: Best early plan for most players: finish the tutorial, follow main quests, join an active alliance fast, push HQ correctly, and save diamonds for long-term value instead of random early spending.

Desired after:
Do not add a self-link. Strengthen outbound routing to the correct hub, troubleshooting page, or adjacent support page instead.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

