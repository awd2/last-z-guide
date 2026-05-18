# Apply Preview: owner-apply-preview-smoke-2026-05-18

## Overview

- Summary: Temporary smoke fixture for GitHub issue /preview-apply workflow validation.
- Status before preview: `approved_for_apply`
- Target: `automation/reports/owner-apply-preview-smoke-source.txt`
- Approved specs: 1
- Generated at: `2026-05-18T19:51:00Z`

## Safety Rule

- This report is preview-only.
- It does not modify site content.
- It only renders operations with `approval_state=approved`.
- Generated research pages must still be edited through JSON source files and regenerated.

## Source Files

- automation/reports/owner-apply-preview-smoke-source.txt

## `automation/reports/owner-apply-preview-smoke-source.txt`

### safe_exact_replace

- Target output: `automation/reports/owner-apply-preview-smoke-source.txt`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `safe_exact_replace`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# #smoke
- Before owner apply preview smoke fixture.
+ After owner apply preview smoke fixture.
```

Validation:
- python3 -m unittest automation.tests.test_worker_contracts.WorkerContractTests.test_issue_lifecycle_runs_review_brief_and_patch_plan_comments

