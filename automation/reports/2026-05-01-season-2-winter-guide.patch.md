# Patch Plan: 2026-05-01-season-2-winter-guide

## Overview

- Summary: Create a new page or file `season-2-winter.html` for the `Seasons` cluster using the `support-guide` archetype.
- Status: `reviewed`
- Risk: `high`
- Cluster: `Seasons`
- Target: `season-2-winter.html`
- Archetype: `support-guide`

## Proposed File Changes

- `season-2-winter.html` -> `first_screen_update`
  reason: Align the opening answer with the run summary, target intent, and cluster role.
- `season-2-winter.html` -> `meta_refresh`
  reason: Tighten title/meta/H1 alignment around the page’s exact search intent.

## Candidate Changed Files

- season-2-winter.html

## Source Files To Edit

- season-2-winter.html

## Patch Spec v1

- `season-2-winter.html` -> `first_screen_update`
  source: `season-2-winter.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `season-2-winter.html` -> `meta_refresh`
  source: `season-2-winter.html`
  generated: `false`
  generator: `None`
  approval: `required`

## Canonical Claims To Protect

- None

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
