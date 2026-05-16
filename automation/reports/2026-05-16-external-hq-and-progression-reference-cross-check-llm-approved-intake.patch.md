# Patch Plan: 2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `hq.html` from `external-hq-and-progression-reference-cross-check`.
- Status: `planned`
- Risk: `high`
- Cluster: `Progression`
- Target: `hq.html`
- Archetype: `cornerstone-guide`

## Proposed File Changes

- `hq.html` -> `first_screen_update`
  reason: This is a narrow first-screen refinement that preserves the current structure while improving requirement clarity.
- `hq.html` -> `meta_refresh`
  reason: Tighten title/meta/H1 alignment around the page’s exact search intent.

## Candidate Changed Files

- hq.html

## Source Files To Edit

- hq.html

## Patch Spec v1

- `hq.html` -> `safe_exact_replace`
  source: `hq.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `hq.html` -> `meta_refresh`
  source: `hq.html`
  generated: `false`
  generator: `None`
  approval: `required`

## Canonical Claims To Protect

- None

## Deterministic Checks To Run After Patch Review

- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## Notes

- This is a proposal-only artifact.
- No site files were modified by this step.
- Use this plan to decide whether the next step should be manual editing or a low-risk auto-edit worker.
