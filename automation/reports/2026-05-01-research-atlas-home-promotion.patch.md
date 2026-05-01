# Patch Plan: 2026-05-01-research-atlas-home-promotion

## Overview

- Summary: Update the existing page `index.html` for the `Research` cluster using the `atlas-page` archetype.
- Status: `reviewed`
- Risk: `high`
- Cluster: `Research`
- Target: `index.html`
- Archetype: `atlas-page`

## Proposed File Changes

- `index.html` -> `first_screen_update`
  reason: Align the opening answer with the run summary, target intent, and cluster role.
- `index.html` -> `meta_refresh`
  reason: Tighten title/meta/H1 alignment around the page’s exact search intent.
- `index.html` -> `internal_link_addition`
  reason: Strengthen routing between the target page and adjacent cluster pages.
- `index.html` -> `atlas_card_update`
  reason: Adjust atlas cards or route blocks to improve cluster navigation and page choice.
- `alliance-recognition-cost.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `index.html` from a related cluster page.
- `army-building-cost.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `index.html` from a related cluster page.
- `field-research.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `index.html` from a related cluster page.
- `fully-armed-alliance-cost.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `index.html` from a related cluster page.

## Candidate Changed Files

- alliance-recognition-cost.html
- army-building-cost.html
- field-research.html
- fully-armed-alliance-cost.html
- index.html

## Source Files To Edit

- alliance-recognition-cost.html
- data/research_branches/army-building.json
- data/research_branches/field-research.json
- data/research_branches/fully-armed-alliance.json
- index.html

## Patch Spec v1

- `index.html` -> `first_screen_update`
  source: `index.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `index.html` -> `meta_refresh`
  source: `index.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `index.html` -> `internal_link_addition`
  source: `index.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `index.html` -> `atlas_card_update`
  source: `index.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `alliance-recognition-cost.html` -> `internal_link_addition`
  source: `alliance-recognition-cost.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `army-building-cost.html` -> `internal_link_addition`
  source: `data/research_branches/army-building.json`
  generated: `true`
  generator: `python3 scripts/generate_research_branch.py data/research_branches/army-building.json`
  approval: `required`
- `field-research.html` -> `internal_link_addition`
  source: `data/research_branches/field-research.json`
  generated: `true`
  generator: `python3 scripts/generate_research_branch.py data/research_branches/field-research.json`
  approval: `required`
- `fully-armed-alliance-cost.html` -> `internal_link_addition`
  source: `data/research_branches/fully-armed-alliance.json`
  generated: `true`
  generator: `python3 scripts/generate_research_branch.py data/research_branches/fully-armed-alliance.json`
  approval: `required`

## Canonical Claims To Protect

- `alliance-recognition-utility-page`: Alliance Recognition is a proven utility page family: tree overview, exact costs, and planner-driven UX outperform generic explanation.
- `field-research-follows-siege`: Field Research follows 100% Siege to Seize and contains the final Recharge Shield path and major late badge pressure.
- `hero-training-cockpit-stop`: Hero Training is mainly valuable for Cockpit. Most players should stop at Cockpit instead of fully clearing the branch early.
- `peace-shield-value`: Peace Shield is a high-value survivability branch because of Urgent Rescue and its wider PvP value.
- `research-best-mainline`: The main research route for most players is Hero Training to Cockpit, then Military Strategies, then Peace Shield, then Siege to Seize, then Field Research.

## Deterministic Checks To Run After Patch Review

- python3 automation/run_checks.py
- python3 scripts/generate_research_branch.py <data-file-if-applicable>
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## Notes

- This is a proposal-only artifact.
- No site files were modified by this step.
- Use this plan to decide whether the next step should be manual editing or a low-risk auto-edit worker.
