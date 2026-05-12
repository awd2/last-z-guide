# Patch Plan: 2026-05-12-research-gsc-opportunity-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `research.html` from `research-gsc-opportunity`.
- Status: `patch_plan_ready`
- Risk: `high`
- Cluster: `Research`
- Target: `research.html`
- Archetype: `cornerstone-guide`

## Proposed File Changes

- `research.html` -> `first_screen_update`
  reason: Align the opening answer with the run summary, target intent, and cluster role.
- `research.html` -> `meta_refresh`
  reason: Tighten title/meta/H1 alignment around the page’s exact search intent.

## Candidate Changed Files

- research.html

## Source Files To Edit

- research.html

## Patch Spec v1

- `research.html` -> `first_screen_update`
  source: `research.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `research.html` -> `meta_refresh`
  source: `research.html`
  generated: `false`
  generator: `None`
  approval: `required`

## Canonical Claims To Protect

- `hero-training-cockpit-stop`: Hero Training is mainly valuable for Cockpit. Most players should stop at Cockpit instead of fully clearing the branch early.
- `peace-shield-value`: Peace Shield is a high-value survivability branch because of Urgent Rescue and its wider PvP value.
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
