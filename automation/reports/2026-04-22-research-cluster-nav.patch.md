# Patch Plan: 2026-04-22-research-cluster-nav

## Overview

- Summary: Update the existing page `research-costs.html` for the `Research` cluster using the `atlas-page` archetype.
- Status: `patch_plan_ready`
- Risk: `medium`
- Cluster: `Research`
- Target: `research-costs.html`
- Archetype: `atlas-page`

## Proposed File Changes

- `research-costs.html` -> `first_screen_update`
  reason: Align the opening answer with the run summary, target intent, and cluster role.
- `research-costs.html` -> `meta_refresh`
  reason: Tighten title/meta/H1 alignment around the page’s exact search intent.
- `research-costs.html` -> `internal_link_addition`
  reason: Strengthen routing between the target page and adjacent cluster pages.
- `research-costs.html` -> `atlas_card_update`
  reason: Adjust atlas cards or route blocks to improve cluster navigation and page choice.
- `alliance-recognition-cost.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `research-costs.html` from a related cluster page.
- `army-building-cost.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `research-costs.html` from a related cluster page.
- `field-research.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `research-costs.html` from a related cluster page.
- `fully-armed-alliance-cost.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `research-costs.html` from a related cluster page.

## Candidate Changed Files

- alliance-recognition-cost.html
- army-building-cost.html
- field-research.html
- fully-armed-alliance-cost.html
- research-costs.html

## Source Files To Edit

- alliance-recognition-cost.html
- data/research_branches/army-building.json
- data/research_branches/field-research.json
- data/research_branches/fully-armed-alliance.json
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
- `research-costs.html` -> `internal_link_addition`
  source: `research-costs.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `research-costs.html` -> `atlas_card_update`
  source: `research-costs.html`
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
- `research-atlas-role`: research-costs.html is the atlas/hub for the research cost cluster. It should compare branches and route to exact tree pages, not replace them.
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
