# Proposed Edits: 2026-05-01-redeem-failure-intent

## Overview

- Summary: Update the existing page `redeem-code-not-working.html` for the `Economy` cluster using the `support-guide` archetype.
- Status: `proposal_ready`
- Risk: `low`
- Cluster: `Economy`
- Target: `redeem-code-not-working.html`
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
- redeem-code-not-working.html

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
title: Last Z Redeem Codes (2026) — Active Codes, Gift Center Login, UID | h1: Last Z Redeem Codes — Active Codes, Gift Center Login, and UID | meta: Active Last Z redeem codes, official Gift Center login, how to copy your UID, and the fastest fixes when a code does not work. | verified: Use this page for active Last Z codes first, then redeem them through the official Gift Center. Copy your UID from Avatar > Settings > Copy ID, paste the code exactly, and check your in-game mailbox for rewards.

Desired after:
No edit recommended: `codes.html` already links to this troubleshooting page in the early routing block, troubleshooting section, FAQ, and related-guides grid.

Suggested content:
Reject this spec for this pass. `codes.html` already links to `redeem-code-not-working.html` in the early routing block, troubleshooting section, FAQ, and related-guides grid.

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
No edit recommended: this page is not a close troubleshooting source for failed code redemption.

Suggested content:
Reject this spec for this pass. The source page is not close enough to failed-code troubleshooting to justify another cross-link.

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
No edit recommended: this page is not a close troubleshooting source for failed code redemption.

Suggested content:
Reject this spec for this pass. The source page is not close enough to failed-code troubleshooting to justify another cross-link.

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
No edit recommended: this page is not a close troubleshooting source for failed code redemption.

Suggested content:
Reject this spec for this pass. The source page is not close enough to failed-code troubleshooting to justify another cross-link.

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## `redeem-code-not-working.html`

### first_screen_update

- Target output: `redeem-code-not-working.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Gift Center Code Not Working? (2026) — UID, Login, Reward Fixes | h1: Last Z Code Not Working? Gift Center, UID, and Reward Fixes | meta: Last Z code not working? Check Gift Center login, UID mistakes, expired or already-used codes, mailbox delays, and the fastest fixes for failed redemption. | verified: If your Last Z code is not working, the most common causes are a wrong UID, expired code, already-used code, typo, or checking the wrong place for rewards. Start with the official Gift Center and this checklist before assuming the code is dead.

Desired after:
Add one first-screen clarification for failure-type sorting: wrong UID/typo, expired/already-used code, and mailbox delay are different checks. Keep the page as troubleshooting, not the codes hub.

Suggested content:
Add this callout inside the existing `Quick Answer` `.qa-callouts` block, after the mailbox callout:

```html
<p class="qa-callout qa-callout--note">
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


### meta_refresh

- Target output: `redeem-code-not-working.html`
- Source type: `html_file`
- Generated page: `false`
- Selector or anchor: `<title>, meta description, H1, first-screen block`
- Risk: `medium`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Gift Center Code Not Working? (2026) — UID, Login, Reward Fixes | h1: Last Z Code Not Working? Gift Center, UID, and Reward Fixes | meta: Last Z code not working? Check Gift Center login, UID mistakes, expired or already-used codes, mailbox delays, and the fastest fixes for failed redemption. | verified: If your Last Z code is not working, the most common causes are a wrong UID, expired code, already-used code, typo, or checking the wrong place for rewards. Start with the official Gift Center and this checklist before assuming the code is dead.

Desired after:
No metadata change is recommended. The current title, H1, and meta already target code-not-working, Gift Center, UID, login, reward, expired, already-used, and mailbox intent.

Suggested content:
No metadata edit is recommended for this pass. Keep the current title, H1, and meta description focused on failed redemption, Gift Center, UID, expired/already-used codes, and mailbox delays.

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
- Selector or anchor: `related-guides section or nearest relevant paragraph`
- Risk: `low`
- Approval state: `proposed`
- Generator command: `None`

Before:
title: Last Z Gift Center Code Not Working? (2026) — UID, Login, Reward Fixes | h1: Last Z Code Not Working? Gift Center, UID, and Reward Fixes | meta: Last Z code not working? Check Gift Center login, UID mistakes, expired or already-used codes, mailbox delays, and the fastest fixes for failed redemption. | verified: If your Last Z code is not working, the most common causes are a wrong UID, expired code, already-used code, typo, or checking the wrong place for rewards. Start with the official Gift Center and this checklist before assuming the code is dead.

Desired after:
Add `Gift Center UID Setup` to related guides because failed-code troubleshooting often starts with setup validation.

Suggested content:
Add this related-card inside the existing `Related Guides` grid, after `Redeem Codes`:

```html
<a href="gift-center-uid.html" class="related-card">Gift Center UID Setup</a>
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

