# Patch Plan: 2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `alliance-duel.html` from `alliance-duel-gsc-opportunity`.
- Status: `patch_plan_ready`
- Risk: `medium`
- Cluster: `Events`
- Target: `alliance-duel.html`
- Archetype: `event-guide`

## Proposed File Changes

- `alliance-duel.html` -> `first_screen_update`
  reason: Align the opening answer with the run summary, target intent, and cluster role.
- `alliance-duel.html` -> `meta_refresh`
  reason: Tighten title/meta/H1 alignment around the page’s exact search intent.

## Candidate Changed Files

- alliance-duel.html

## Source Files To Edit

- alliance-duel.html

## Patch Spec v1

- `alliance-duel.html` -> `first_screen_update`
  source: `alliance-duel.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `alliance-duel.html` -> `meta_refresh`
  source: `alliance-duel.html`
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
