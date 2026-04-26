# Proposed Edits: 2026-04-22-research-cluster-nav

## Overview

- Summary: Update the existing page `research-costs.html` for the `Research` cluster using the `atlas-page` archetype.
- Status: `approved_for_apply`
- Risk: `medium`
- Cluster: `Research`
- Target: `research-costs.html`
- Archetype: `atlas-page`

## Review Rule

- This report is proposal-only.
- It does not modify site content.
- Apply only after human review changes `approval_state` from `proposed` to `approved` in a future approved-apply workflow.
- Generated research pages must be edited through JSON source files and regenerated.

## Source Files

- alliance-recognition-cost.html
- data/research_branches/army-building.json
- data/research_branches/field-research.json
- data/research_branches/fully-armed-alliance.json
- research-costs.html

## `alliance-recognition-cost.html`

### internal_link_addition

- Target output: `alliance-recognition-cost.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `Related Guides`
- Risk: `low`
- Approval state: `approved`
- Generator command: `None`

Before:
title: Last Z Alliance Recognition Costs (2026) — Total Badge Cost and Research Path | h1: Last Z Alliance Recognition Costs — Total Badge Cost and Research Path | meta: Total Alliance Recognition badge cost in Last Z: full research path, key checkpoints, and how many badges you need before spending on this tree. | verified: Alliance Recognition costs 356,770 badges in total; use this research path and badge planner before committing badges to the full tree.

Desired after:
Source adds a crawlable, user-visible bridge to `research-costs.html` in the relevant section or related-guides block.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## `data/research_branches/army-building.json`

### internal_link_addition

- Target output: `army-building-cost.html`
- Source type: `generated_research_branch`
- Generated page: `true`
- Selector or anchor: `related_guides or next_steps`
- Risk: `medium`
- Approval state: `approved`
- Generator command: `python3 scripts/generate_research_branch.py data/research_branches/army-building.json`

Before:
title: Last Z Army Building Costs (2026) — Total Badge Cost and Peace Shield Follow-Up | h1: Last Z Army Building Costs — Total Badge Cost and Peace Shield Follow-Up | meta: Army Building badge costs in Last Z: total branch cost, exact node totals, Peace Shield follow-up path, and the later Recharge Shield checkpoint for deep combat research. | verified: Army Building is a deep combat branch that opens only after Peace Shield is fully complete. It is much more serious than the mid-game branches before it, so exact node totals matter before you commit.

Desired after:
JSON source adds or strengthens a route back to `research-costs.html` through `related_guides` or `next_steps`, then regenerates the HTML output.

Validation:
- python3 scripts/generate_research_branch.py data/research_branches/army-building.json
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## `data/research_branches/field-research.json`

### internal_link_addition

- Target output: `field-research.html`
- Source type: `generated_research_branch`
- Generated page: `true`
- Selector or anchor: `related_guides or next_steps`
- Risk: `medium`
- Approval state: `approved`
- Generator command: `python3 scripts/generate_research_branch.py data/research_branches/field-research.json`

Before:
title: Last Z Field Research Costs (2026) — Recharge Shield Path and Total Badge Cost | h1: Last Z Field Research Costs — Recharge Shield Path and Total Badge Cost | meta: Field Research badge costs in Last Z: total branch cost, Recharge Shield path, node-by-node totals, and what unlocks after Siege to Seize is fully complete. | verified: Field Research is the heavy follow-up branch after Siege to Seize. It matters because Recharge Shield sits at the end of an already expensive path, so this page shows exactly where the real badge wall begins.

Desired after:
JSON source adds or strengthens a route back to `research-costs.html` through `related_guides` or `next_steps`, then regenerates the HTML output.

Validation:
- python3 scripts/generate_research_branch.py data/research_branches/field-research.json
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## `data/research_branches/fully-armed-alliance.json`

### internal_link_addition

- Target output: `fully-armed-alliance-cost.html`
- Source type: `generated_research_branch`
- Generated page: `true`
- Selector or anchor: `related_guides or next_steps`
- Risk: `medium`
- Approval state: `approved`
- Generator command: `python3 scripts/generate_research_branch.py data/research_branches/fully-armed-alliance.json`

Before:
title: Last Z Fully Armed Alliance Costs (2026) — Annihilation, Move Out, and Total Badge Cost | h1: Last Z Fully Armed Alliance Costs — Annihilation, Move Out, and Total Badge Cost | meta: Fully Armed Alliance badge costs in Last Z: total branch cost, Annihilation and Move Out totals, and the exact node costs behind one of the most aggressive late combat trees. | verified: Fully Armed Alliance is one of the most aggressive combat branches in Last Z. Players usually ask about it for Annihilation and Move Out, but the full branch is a serious badge sink and should not be treated as an automatic early priority.

Desired after:
JSON source adds or strengthens a route back to `research-costs.html` through `related_guides` or `next_steps`, then regenerates the HTML output.

Validation:
- python3 scripts/generate_research_branch.py data/research_branches/fully-armed-alliance.json
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## `research-costs.html`

### first_screen_update

- Target output: `research-costs.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `approved`
- Generator command: `None`

Before:
title: Last Z Research Costs Atlas (2026) — All Research Trees, Badge Totals, and Unlock Paths | h1: Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths | meta: All major Last Z research trees in one place: total badge costs, unlock requirements, best stopping points, and links to every exact node-cost tree. | verified: This atlas is the fastest way to compare all major badge-heavy research trees in Last Z. Use it when you want to see total branch cost, unlock requirements, and the exact tree page for each branch without jumping through the whole site blindly.

Desired after:
Opening answer names the atlas role, main research route, and exact branch-page routing without turning the atlas into a giant guide.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### meta_refresh

- Target output: `research-costs.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `approved`
- Generator command: `None`

Before:
title: Last Z Research Costs Atlas (2026) — All Research Trees, Badge Totals, and Unlock Paths | h1: Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths | meta: All major Last Z research trees in one place: total badge costs, unlock requirements, best stopping points, and links to every exact node-cost tree. | verified: This atlas is the fastest way to compare all major badge-heavy research trees in Last Z. Use it when you want to see total branch cost, unlock requirements, and the exact tree page for each branch without jumping through the whole site blindly.

Desired after:
Title, H1, and meta description use the same exact intent: research costs atlas, branch comparison, badge totals, and unlock paths.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### internal_link_addition

- Target output: `research-costs.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `Related Guides`
- Risk: `low`
- Approval state: `approved`
- Generator command: `None`

Before:
title: Last Z Research Costs Atlas (2026) — All Research Trees, Badge Totals, and Unlock Paths | h1: Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths | meta: All major Last Z research trees in one place: total badge costs, unlock requirements, best stopping points, and links to every exact node-cost tree. | verified: This atlas is the fastest way to compare all major badge-heavy research trees in Last Z. Use it when you want to see total branch cost, unlock requirements, and the exact tree page for each branch without jumping through the whole site blindly.

Desired after:
Source adds a crawlable, user-visible bridge to `research-costs.html` in the relevant section or related-guides block.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### atlas_card_update

- Target output: `research-costs.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `atlas cards / branch comparison route block`
- Risk: `low`
- Approval state: `approved`
- Generator command: `None`

Before:
title: Last Z Research Costs Atlas (2026) — All Research Trees, Badge Totals, and Unlock Paths | h1: Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths | meta: All major Last Z research trees in one place: total badge costs, unlock requirements, best stopping points, and links to every exact node-cost tree. | verified: This atlas is the fastest way to compare all major badge-heavy research trees in Last Z. Use it when you want to see total branch cost, unlock requirements, and the exact tree page for each branch without jumping through the whole site blindly.

Desired after:
Atlas cards help users choose the correct branch page and keep the core order visible: Hero Training, Military Strategies, Peace Shield, Siege to Seize, Field Research.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

