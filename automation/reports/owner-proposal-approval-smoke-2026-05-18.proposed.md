# Proposed Edits: owner-proposal-approval-smoke-2026-05-18

## Overview

- Summary: Temporary smoke fixture for GitHub issue /approve-proposal workflow validation.
- Status: `approved_for_apply`
- Risk: `low`
- Cluster: ``
- Target: `automation/reports/owner-proposal-approval-smoke-source.txt`
- Archetype: ``

## Review Rule

- This report is proposal-only.
- It does not modify site content.
- Apply only after human review changes `approval_state` from `proposed` to `approved` in a future approved-apply workflow.
- Generated research pages must be edited through JSON source files and regenerated.

## Source Files

- automation/reports/owner-proposal-approval-smoke-source.txt

## `automation/reports/owner-proposal-approval-smoke-source.txt`

### safe_exact_replace

- Target output: `automation/reports/owner-proposal-approval-smoke-source.txt`
- Source type: `None`
- Generated page: `none`
- Selector or anchor: `#smoke`
- Risk: `medium`
- Approval state: `approved`
- Generator command: `None`

Before:
No compact source summary available.

Desired after:
Replace the exact old snippet with the exact new snippet only after owner approval. The apply step must fail closed if the source text has drifted or appears more than once.

Suggested content:
Exact approved replacement candidate:

```diff
- Before owner proposal approval smoke fixture.
+ After owner proposal approval smoke fixture.
```

Validation:
- python3 -m unittest automation.tests.test_worker_contracts.WorkerContractTests.test_issue_lifecycle_runs_review_brief_and_patch_plan_comments

