# Apply Preview: 2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `hq.html` from `external-hq-and-progression-reference-cross-check`.
- Status before preview: `partially_approved`
- Target: `hq.html`
- Approved specs: 1
- Generated at: `2026-05-16T18:24:51Z`

## Safety Rule

- This report is preview-only.
- It does not modify site content.
- It only renders operations with `approval_state=approved`.
- Generated research pages must still be edited through JSON source files and regenerated.

## Source Files

- hq.html

## `hq.html`

### safe_exact_replace

- Target output: `hq.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `safe_exact_replace`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# p.qa-lede
- <p class="qa-lede"><strong>Best Last Z HQ upgrade path for most players:</strong> rush early levels, upgrade only required buildings, push efficiently to HQ30 first, and treat HQ31-35 as a separate steel-based progression phase with much heavier timers.</p>
+ <p class="qa-lede"><strong>Best Last Z HQ upgrade path for most players:</strong> rush early levels, upgrade only the buildings required for the next HQ checkpoint, push efficiently to HQ30 first, and treat HQ31-35 as a separate steel-based progression phase with much heavier timers.</p>
```

Validation:
- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

