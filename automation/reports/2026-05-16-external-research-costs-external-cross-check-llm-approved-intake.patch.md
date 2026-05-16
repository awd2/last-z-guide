# Patch Plan: 2026-05-16-external-research-costs-external-cross-check-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `research-costs.html` from `external-research-costs-external-cross-check`.
- Status: `patch_plan_ready`
- Risk: `high`
- Cluster: `Research`
- Target: `research-costs.html`
- Archetype: `atlas-page`

## Proposed File Changes

- `research-costs.html` -> `first_screen_update`
  reason: Align the opening answer with the run summary, target intent, and cluster role.
- `research-costs.html` -> `meta_refresh`
  reason: Tighten title/meta/H1 alignment around the page’s exact search intent.
- `research-costs.html` -> `atlas_card_update`
  reason: Adjust atlas cards or route blocks to improve cluster navigation and page choice.

## Candidate Changed Files

- research-costs.html

## Source Files To Edit

- research-costs.html

## Patch Spec v1

- `research-costs.html` -> `first_screen_update`
  source: `research-costs.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `research-costs.html` -> `meta_refresh`
  source: `research-costs.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `research-costs.html` -> `atlas_card_update`
  source: `research-costs.html`
  generated: `false`
  generator: `None`
  approval: `required`

## Canonical Claims To Protect

- `field-research-follows-siege`: Field Research follows 100% Siege to Seize and contains the final Recharge Shield path and major late badge pressure.
- `research-atlas-role`: research-costs.html is the atlas/hub for the research cost cluster. It should compare branches and route to exact tree pages, not replace them.
- `research-best-mainline`: The main research route for most players is Hero Training to Cockpit, then Military Strategies, then Peace Shield/Urgent Rescue. After that, players should choose by goal: use the shortest practical UST/T10 path for tier progression, or push Siege to Seize into Field Research only for late-game Recharge Shield/deep combat scaling.

## Deterministic Checks To Run After Patch Review

- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## Notes

- This is a proposal-only artifact.
- No site files were modified by this step.
- Use this plan to decide whether the next step should be manual editing or a low-risk auto-edit worker.
