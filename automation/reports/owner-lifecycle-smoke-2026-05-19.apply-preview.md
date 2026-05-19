# Apply Preview: owner-lifecycle-smoke-2026-05-19

## Overview

- Summary: Temporary owner issue lifecycle smoke fixture. This must not touch public site content.
- Status before preview: `approved_for_apply`
- Target: ``
- Approved specs: 1
- Generated at: `2026-05-19T07:16:10Z`

## Safety Rule

- This report is preview-only.
- It does not modify site content.
- It only renders operations with `approval_state=approved`.
- Generated research pages must still be edited through JSON source files and regenerated.

## Source Files

- automation/reports/owner-lifecycle-smoke-source.html

## `automation/reports/owner-lifecycle-smoke-source.html`

### safe_exact_replace

- Target output: `automation/reports/owner-lifecycle-smoke-source.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `safe_exact_replace`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# p
- <p>Before owner lifecycle smoke fixture.</p>
+ <p>After owner lifecycle smoke fixture.</p>
```

Validation:
- python3 automation/pipeline.py checks --strict

