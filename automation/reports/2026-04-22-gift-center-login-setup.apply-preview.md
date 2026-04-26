# Apply Preview: 2026-04-22-gift-center-login-setup

## Overview

- Summary: Update the existing page `gift-center-uid.html` for the `Economy` cluster using the `support-guide` archetype.
- Status before preview: `approved_for_apply`
- Target: `gift-center-uid.html`
- Approved specs: 7
- Generated at: `2026-04-26T10:46:43Z`

## Safety Rule

- This report is preview-only.
- It does not modify site content.
- It only renders operations with `approval_state=approved`.
- Generated research pages must still be edited through JSON source files and regenerated.

## Source Files

- codes.html
- diamond-reserve.html
- f2p.html
- farm-account.html
- gift-center-uid.html

## `codes.html`

### internal_link_addition

- Target output: `codes.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `add_related_card`
- Generator command: `None`

Warnings:
- `codes.html` already links to `gift-center-uid.html`.

Preview patch:
```diff
# related guide card
- <div class="related-grid"> ... </div>
+ <div class="related-grid"> ... <a href="gift-center-uid.html" class="related-card">Gift Center UID Setup</a> ... </div>
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
- None

Preview patch:
```diff
# related guide card
- <div class="related-grid"> ... </div>
+ <div class="related-grid"> ... <a href="gift-center-uid.html" class="related-card">Gift Center UID Setup</a> ... </div>
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## `f2p.html`

### internal_link_addition

- Target output: `f2p.html`
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
+ <div class="related-grid"> ... <a href="gift-center-uid.html" class="related-card">Gift Center UID Setup</a> ... </div>
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
- None

Preview patch:
```diff
# related guide card
- <div class="related-grid"> ... </div>
+ <div class="related-grid"> ... <a href="gift-center-uid.html" class="related-card">Gift Center UID Setup</a> ... </div>
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## `gift-center-uid.html`

### first_screen_update

- Target output: `gift-center-uid.html`
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
- The official Last Z Gift Center login page is the only place where codes are redeemed...
+ Use the official Last Z Gift Center in a browser, copy your UID from Avatar > Settings > Copy ID, redeem the code outside the game, then collect rewards from mailbox.
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### meta_refresh

- Target output: `gift-center-uid.html`
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
- Last Z Gift Center Login & UID Guide (2026) -- Official Redeem Page
+ Last Z Gift Center Login and UID Setup (2026) -- Official Redeem Page
```

```diff
# meta description
- Official Last Z Gift Center login, how to find and copy your UID, how to redeem codes on iPhone or Android, and where rewards appear after redemption.
+ Official Last Z Gift Center login setup: how to copy your UID from Avatar > Settings > Copy ID, redeem in a browser, and collect rewards from mailbox.
```

```diff
# H1
- Last Z Gift Center Login & UID Guide -- Official Redeem Page
+ Last Z Gift Center Login and UID Setup -- Official Redeem Page
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks


### internal_link_addition

- Target output: `gift-center-uid.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `no_self_link_strengthen_outbound_routes`
- Generator command: `None`

Warnings:
- Do not add a self-link from `gift-center-uid.html` to itself.

Preview patch:
```diff
# outbound routing
- Related guides stay unchanged or underspecified.
+ Strengthen links to the correct hub, troubleshooting page, or adjacent support page instead of adding a self-link.
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

