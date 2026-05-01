# Apply Preview: 2026-04-22-gift-center-ctr-pass

## Overview

- Summary: Update the existing page `codes.html` for the `Economy` cluster using the `support-guide` archetype.
- Status before preview: `qa_passed`
- Target: `codes.html`
- Approved specs: 4
- Generated at: `2026-05-01T09:55:58Z`

## Safety Rule

- This report is preview-only.
- It does not modify site content.
- It only renders operations with `approval_state=approved`.
- Generated research pages must still be edited through JSON source files and regenerated.

## Source Files

- codes.html
- diamond-reserve.html
- farm-account.html

## `codes.html`

### first_screen_update

- Target output: `codes.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `replace_first_screen_answer`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# guide-verified
- Use the official Last Z Gift Center to redeem active codes. This page gives you the current verified codes, the official login page, the fastest UID steps, and the main reasons redemption fails.
+ <p class="guide-verified">Use this page for active Last Z codes first, then redeem them through the official Gift Center. Copy your UID from Avatar &gt; Settings &gt; Copy ID, paste the code exactly, and check your in-game mailbox for rewards.</p>
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### internal_link_addition

- Target output: `codes.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `dedupe_gift_center_routing`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# early Gift Center routing
- Two overlapping setup/troubleshooting paragraphs in the highlight box.
+ <p><strong>Need setup only?</strong> Use the <a href="gift-center-uid.html">Gift Center &amp; UID Guide</a>. <strong>Code failed?</strong> Use the <a href="redeem-code-not-working.html">Last Z Code Not Working?</a> guide.</p>
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## `diamond-reserve.html`

### internal_link_addition

- Target output: `diamond-reserve.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `add_related_card`
- Generator command: `None`

Warnings:
- `diamond-reserve.html` already links to `codes.html`.

Preview patch:
```diff
# related guide card
- <div class="related-grid"> ... </div>
+ <div class="related-grid"> ... <a href="codes.html" class="related-card">Redeem Codes</a> ... </div>
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## `farm-account.html`

### internal_link_addition

- Target output: `farm-account.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `add_related_card`
- Generator command: `None`

Warnings:
- `farm-account.html` already links to `codes.html`.

Preview patch:
```diff
# related guide card
- <div class="related-grid"> ... </div>
+ <div class="related-grid"> ... <a href="codes.html" class="related-card">Redeem Codes</a> ... </div>
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

