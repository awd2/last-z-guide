# Apply Preview: 2026-04-22-research-cluster-nav

## Overview

- Summary: Update the existing page `research-costs.html` for the `Research` cluster using the `atlas-page` archetype.
- Status before preview: `approved_for_apply`
- Target: `research-costs.html`
- Approved specs: 8
- Generated at: `2026-04-26T10:23:32Z`

## Safety Rule

- This report is preview-only.
- It does not modify site content.
- It only renders operations with `approval_state=approved`.
- Generated research pages must still be edited through JSON source files and regenerated.

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
- Approval state: `approved`
- Preview action: `add_related_card`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# related guide card
- <div class="related-grid"> ... </div>
+ <div class="related-grid"> ... <a href="research-costs.html" class="related-card">Research Costs Atlas</a> ... </div>
```

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
- Approval state: `approved`
- Preview action: `add_json_related_guide`
- Generator command: `python3 scripts/generate_research_branch.py data/research_branches/army-building.json`

Warnings:
- None

Preview patch:
```diff
# related_guides JSON entry
- "related_guides": [ ... ]
+ "related_guides": [ ..., { "href": "research-costs.html", "label": "Research Costs Atlas" } ]
```

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
- Approval state: `approved`
- Preview action: `add_json_related_guide`
- Generator command: `python3 scripts/generate_research_branch.py data/research_branches/field-research.json`

Warnings:
- None

Preview patch:
```diff
# related_guides JSON entry
- "related_guides": [ ... ]
+ "related_guides": [ ..., { "href": "research-costs.html", "label": "Research Costs Atlas" } ]
```

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
- Approval state: `approved`
- Preview action: `add_json_related_guide`
- Generator command: `python3 scripts/generate_research_branch.py data/research_branches/fully-armed-alliance.json`

Warnings:
- None

Preview patch:
```diff
# related_guides JSON entry
- "related_guides": [ ... ]
+ "related_guides": [ ..., { "href": "research-costs.html", "label": "Research Costs Atlas" } ]
```

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
- Approval state: `approved`
- Preview action: `replace_first_screen_answer`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# first-screen answer
- Best way to use the research atlas: start with Hero Training to Cockpit...
+ Best way to use the research atlas: use this page as the branch router, then open the exact cost page for node totals. For most players, the main route is Hero Training to Cockpit, Military Strategies, Peace Shield, Siege to Seize, then Field Research.
```

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
- Approval state: `approved`
- Preview action: `replace_metadata_strings`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# <title>
- Last Z Research Costs Atlas (2026) -- All Research Trees, Badge Totals, and Unlock Paths
+ Last Z Research Costs Atlas (2026) -- Branch Comparison, Badge Totals, and Unlock Paths
```

```diff
# meta description
- All major Last Z research trees in one place: total badge costs, unlock requirements, best stopping points, and links to every exact node-cost tree.
+ Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page before spending badges.
```

```diff
# H1
- Last Z Research Costs Atlas -- All Research Trees, Badge Totals, and Unlock Paths
+ Last Z Research Costs Atlas -- Branch Comparison, Badge Totals, and Unlock Paths
```

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
- Approval state: `approved`
- Preview action: `no_self_link_strengthen_outbound_routes`
- Generator command: `None`

Warnings:
- Do not add a self-link from the atlas to itself.

Preview patch:
```diff
# outbound atlas routing
- <span class="atlas-link">View tree -></span>
+ <span class="atlas-link">View exact cost tree -></span>
```

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
- Approval state: `approved`
- Preview action: `tighten_atlas_card_copy`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# atlas card routing copy
- View tree ->
+ View exact cost tree ->
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

