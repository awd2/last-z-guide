# Proposed Edits: 2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `hq.html` from `external-hq-and-progression-reference-cross-check`.
- Status: `partially_approved`
- Risk: `high`
- Cluster: `Progression`
- Target: `hq.html`
- Archetype: `cornerstone-guide`

## Review Rule

- This report is proposal-only.
- It does not modify site content.
- Apply only after human review changes `approval_state` from `proposed` to `approved` in a future approved-apply workflow.
- Generated research pages must be edited through JSON source files and regenerated.

## Source Files

- hq.html

## `hq.html`

### safe_exact_replace

- Target output: `hq.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `p.qa-lede`
- Risk: `medium`
- Approval state: `approved`
- Generator command: `None`

Before:
title: Last Z HQ Upgrade Guide (2026) — Requirements, Fast Path to HQ 30/35 | h1: Last Z HQ Upgrade Guide — Requirements, Fast Path, and HQ 30/35 Strategy | meta: Best HQ strategy for Last Z: rush early levels, upgrade required buildings only, push efficiently to HQ30, and prepare steel for HQ31-35. | verified: Best HQ strategy for most players: rush early levels, upgrade only the buildings required for the next HQ checkpoint, push efficiently to HQ30, and prepare for steel and long timers before starting the HQ31-35 journey.

Desired after:
Replace the exact old snippet with the exact new snippet only after owner approval. The apply step must fail closed if the source text has drifted or appears more than once.

Suggested content:
Exact approved replacement candidate:

```diff
- <p class="qa-lede"><strong>Best Last Z HQ upgrade path for most players:</strong> rush early levels, upgrade only required buildings, push efficiently to HQ30 first, and treat HQ31-35 as a separate steel-based progression phase with much heavier timers.</p>
+ <p class="qa-lede"><strong>Best Last Z HQ upgrade path for most players:</strong> rush early levels, upgrade only the buildings required for the next HQ checkpoint, push efficiently to HQ30 first, and treat HQ31-35 as a separate steel-based progression phase with much heavier timers.</p>
```

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### meta_refresh

- Target output: `hq.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z HQ Upgrade Guide (2026) — Requirements, Fast Path to HQ 30/35 | h1: Last Z HQ Upgrade Guide — Requirements, Fast Path, and HQ 30/35 Strategy | meta: Best HQ strategy for Last Z: rush early levels, upgrade required buildings only, push efficiently to HQ30, and prepare steel for HQ31-35. | verified: Best HQ strategy for most players: rush early levels, upgrade only the buildings required for the next HQ checkpoint, push efficiently to HQ30, and prepare for steel and long timers before starting the HQ31-35 journey.

Desired after:
Title, H1, and meta description use the same exact intent: hq.html.

Suggested content:
No exact snippet generated; use the desired-after summary as the review target.

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

