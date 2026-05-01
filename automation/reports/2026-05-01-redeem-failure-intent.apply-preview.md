# Apply Preview: 2026-05-01-redeem-failure-intent

## Overview

- Summary: Update the existing page `redeem-code-not-working.html` for the `Economy` cluster using the `support-guide` archetype.
- Status before preview: `approved_for_apply`
- Target: `redeem-code-not-working.html`
- Approved specs: 2
- Generated at: `2026-05-01T15:26:59Z`

## Safety Rule

- This report is preview-only.
- It does not modify site content.
- It only renders operations with `approval_state=approved`.
- Generated research pages must still be edited through JSON source files and regenerated.

## Source Files

- redeem-code-not-working.html

## `redeem-code-not-working.html`

### first_screen_update

- Target output: `redeem-code-not-working.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `replace_first_screen_answer`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# Quick Answer callout
- Existing callouts explain official Gift Center, UID copying, and mailbox rewards.
+ <p class="qa-callout qa-callout--note">
    <span class="qa-icon" aria-hidden="true">i</span>
    <span class="qa-callout-text"><strong>Sort the failure first:</strong> wrong UID or typo means the redemption failed, expired or already-used means the code is no longer claimable for that account, and missing rewards means you should check mailbox timing before retrying.</span>
</p>
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### internal_link_addition

- Target output: `redeem-code-not-working.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `add_setup_related_card`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# related guide card
- <a href="codes.html" class="related-card">Redeem Codes</a>
+ <a href="codes.html" class="related-card">Redeem Codes</a>
<a href="gift-center-uid.html" class="related-card">Gift Center UID Setup</a>
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

