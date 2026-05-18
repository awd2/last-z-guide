# Exact Proposals: owner-proposal-approval-smoke-2026-05-18

## Overview

- Summary: Temporary smoke fixture for GitHub issue /approve-proposal workflow validation.
- Status: `approved_for_apply`
- Risk: `low`
- Target: `automation/reports/owner-proposal-approval-smoke-source.txt`
- Exact proposals: `1`
- Non-exact proposals hidden: `0`

## Safety

- This report is owner-review only.
- It does not edit content, mutate the manifest, record approval, commit, push, or deploy.
- Approve only after checking the exact Before / After text below.

## automation/reports/owner-proposal-approval-smoke-source.txt -> #smoke

- Risk: `medium`
- Approval state: `approved`
- Human approval required: `true`
- Summary: Temporary smoke-only exact replacement proposal.

Before:

```html
Before owner proposal approval smoke fixture.
```

After:

```html
After owner proposal approval smoke fixture.
```

Required checks:

- `python3 -m unittest automation.tests.test_worker_contracts.WorkerContractTests.test_issue_lifecycle_runs_review_brief_and_patch_plan_comments`
