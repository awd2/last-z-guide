# Proposed Edits: 2026-04-22-gift-center-login-setup

## Overview

- Summary: Update the existing page `gift-center-uid.html` for the `Economy` cluster using the `support-guide` archetype.
- Status: `proposal_ready`
- Risk: `medium`
- Cluster: `Economy`
- Target: `gift-center-uid.html`
- Archetype: `support-guide`

## Review Rule

- This report is proposal-only.
- It does not modify site content.
- Apply only after human review changes `approval_state` from `proposed` to `approved` in a future approved-apply workflow.
- Generated research pages must be edited through JSON source files and regenerated.

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
- Selector or anchor: `related-guides section or nearest relevant paragraph`
- Risk: `low`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Redeem Codes (2026) — Active Codes, Gift Center Login, UID | h1: Last Z Redeem Codes — Active Codes, Gift Center Login, and UID | meta: Active Last Z redeem codes, official Gift Center login, how to copy your UID, and the fastest fixes when a code does not work. | verified: Use the official Last Z Gift Center to redeem active codes. This page gives you the current verified codes, the official login page, the fastest UID steps, and the main reasons redemption fails.

Desired after:
Source adds a crawlable, user-visible bridge to `gift-center-uid.html` in the relevant section or related-guides block.

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
- Selector or anchor: `Related Guides`
- Risk: `low`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Diamond Reserve Guide (2026) — What to Save Diamonds For First | h1: Last Z Diamond Reserve Guide — What to Save Diamonds For First | meta: Best Last Z diamond reserve strategy: what to save diamonds for first, how the Friday shield reserve works, when Lucky Discounter is worth it, and which purchases are a waste for F2P. | verified: Best diamond rule for most F2P and low spenders: keep a protected reserve for shields first, spend only on high-value event discounts or long-term account value you can actually buy with diamonds second, and avoid reactive purchases that do not improve your account long term.

Desired after:
Source adds a crawlable, user-visible bridge to `gift-center-uid.html` in the relevant section or related-guides block.

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
- Selector or anchor: `related-guides section or nearest relevant paragraph`
- Risk: `low`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z F2P Guide (2026) — Best Diamond Spending, Free Sources, What to Buy First | h1: Last Z F2P Guide — Best Diamond Spending, Free Sources, and What to Buy First | meta: Complete Last Z F2P guide: how to get free diamonds, what to save them for first, the best spending priority for shields, refugees, and event value, and how F2P players stay competitive. | verified: Best F2P plan for most players: protect your weekly shield reserve first, invest in refugees for long-term speed, and only spend diamonds aggressively when events improve the value instead of wasting them on random convenience.

Desired after:
Source adds a crawlable, user-visible bridge to `gift-center-uid.html` in the relevant section or related-guides block.

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
- Selector or anchor: `Related Guides`
- Risk: `low`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Farm Account Guide (2026) - How to Create a Farm Before Season 2 | h1: Last Z Farm Account Guide - How to Create a Farm Before Season 2 | meta: How to create a Last Z farm account on your server before Season 2, what you need, how to set up a farm alt, and how to use it to support your main account. | verified: Best farm account setup for most players: create the farm before Season 2 starts on your server, place it on the same server as your main account, and use it for steady resource support instead of trying to turn it into a second main.

Desired after:
Source adds a crawlable, user-visible bridge to `gift-center-uid.html` in the relevant section or related-guides block.

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
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Gift Center Login & UID Guide (2026) — Official Redeem Page | h1: Last Z Gift Center Login & UID Guide — Official Redeem Page | meta: Official Last Z Gift Center login, how to find and copy your UID, how to redeem codes on iPhone or Android, and where rewards appear after redemption. | verified: The official Last Z Gift Center login page is the only place where codes are redeemed. Copy your UID from Avatar → Settings → Copy ID, redeem in a browser, and collect rewards from your mailbox.

Desired after:
Opening answer matches the page role for Gift Center login setup and UID lookup, gives the exact setup answer quickly, and avoids drifting into a broader hub page.

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
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Gift Center Login & UID Guide (2026) — Official Redeem Page | h1: Last Z Gift Center Login & UID Guide — Official Redeem Page | meta: Official Last Z Gift Center login, how to find and copy your UID, how to redeem codes on iPhone or Android, and where rewards appear after redemption. | verified: The official Last Z Gift Center login page is the only place where codes are redeemed. Copy your UID from Avatar → Settings → Copy ID, redeem in a browser, and collect rewards from your mailbox.

Desired after:
Title, H1, and meta description use the same exact intent: Gift Center login setup and UID lookup.

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
- Selector or anchor: `Related Guides`
- Risk: `low`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Gift Center Login & UID Guide (2026) — Official Redeem Page | h1: Last Z Gift Center Login & UID Guide — Official Redeem Page | meta: Official Last Z Gift Center login, how to find and copy your UID, how to redeem codes on iPhone or Android, and where rewards appear after redemption. | verified: The official Last Z Gift Center login page is the only place where codes are redeemed. Copy your UID from Avatar → Settings → Copy ID, redeem in a browser, and collect rewards from your mailbox.

Desired after:
Do not add a self-link. Strengthen outbound routing to the correct hub, troubleshooting page, or adjacent support page instead.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

