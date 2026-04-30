# Patch Plan: 2026-04-22-season-alias-clarification

## Overview

- Summary: Update the existing page `start.html` for the `Seasons` cluster using the `support-guide` archetype.
- Status: `draft_brief_ready`
- Risk: `low`
- Cluster: `Seasons`
- Target: `start.html`
- Archetype: `support-guide`

## Proposed File Changes

- `start.html` -> `first_screen_update`
  reason: Align the opening answer with the run summary, target intent, and cluster role.
- `start.html` -> `meta_refresh`
  reason: Tighten title/meta/H1 alignment around the page’s exact search intent.
- `start.html` -> `internal_link_addition`
  reason: Strengthen routing between the target page and adjacent cluster pages.

## Candidate Changed Files

- start.html

## Source Files To Edit

- start.html

## Patch Spec v1

- `start.html` -> `first_screen_update`
  source: `start.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `start.html` -> `meta_refresh`
  source: `start.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `start.html` -> `internal_link_addition`
  source: `start.html`
  generated: `false`
  generator: `None`
  approval: `required`

## Canonical Claims To Protect

- `season-2-winter-current-naming`: For newer servers, Season 2 is Winter. Desert was canceled or skipped, so older guides that map Season 2 to Desert may be outdated for current players.

## Deterministic Checks To Run After Patch Review

- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## Notes

- This is a proposal-only artifact.
- No site files were modified by this step.
- Use this plan to decide whether the next step should be manual editing or a low-risk auto-edit worker.
