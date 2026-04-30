# Proposed Edits: 2026-04-22-season-alias-clarification

## Overview

- Summary: Update the existing page `start.html` for the `Seasons` cluster using the `support-guide` archetype.
- Status: `partially_approved`
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
- Selector or anchor: `Quick Answer -> .qa-callouts`
- Risk: `medium`
- Approval state: `approved`
- Generator command: `None`

Before:
title: Last Z Beginner Guide (2026) — Best Start and Early Mistakes to Avoid | h1: Last Z Beginner Guide — Best Start and Early Mistakes to Avoid | meta: Best beginner path in Last Z: early priorities, key upgrades, alliance timing, and the first mistakes to avoid in your opening days. | verified: Best early plan for most players: finish the tutorial, follow main quests, join an active alliance fast, push HQ correctly, and save diamonds for long-term value instead of random early spending.

Desired after:
Add a concise early clarification that for newer servers Season 2 is Winter, Desert was canceled or skipped, and older guides that call Season 2 Desert may be outdated. Keep the page primarily a beginner start guide.

Suggested content:
Add this callout inside the existing `Quick Answer` `.qa-callouts` block, after the current `Core rule` callout:

```html
<p class="qa-callout qa-callout--note">
    <span class="qa-icon" aria-hidden="true">i</span>
    <span class="qa-callout-text"><strong>Season naming note:</strong> on newer servers, Season 2 is Winter. Older guides may call Season 2 Desert, but Desert was canceled or skipped for current servers, so follow Winter naming when planning your early timeline.</span>
</p>
```

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
- Approval state: `rejected`
- Generator command: `None`

Before:
title: Last Z Beginner Guide (2026) — Best Start and Early Mistakes to Avoid | h1: Last Z Beginner Guide — Best Start and Early Mistakes to Avoid | meta: Best beginner path in Last Z: early priorities, key upgrades, alliance timing, and the first mistakes to avoid in your opening days. | verified: Best early plan for most players: finish the tutorial, follow main quests, join an active alliance fast, push HQ correctly, and save diamonds for long-term value instead of random early spending.

Desired after:
Preserve the beginner-guide title and H1. Only adjust metadata if needed to support the season naming clarification without turning `start.html` into a season guide.

Suggested content:
No metadata edit is recommended for this pass. Keep the current title, H1, and meta description focused on beginner intent.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

