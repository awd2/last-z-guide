# Patch Plan: 2026-04-22-gift-center-ctr-pass

## Overview

- Summary: Update the existing page `codes.html` for the `Economy` cluster using the `support-guide` archetype.
- Status: `draft_brief_ready`
- Risk: `high`
- Cluster: `Economy`
- Target: `codes.html`
- Archetype: `support-guide`

## Proposed File Changes

- `codes.html` -> `first_screen_update`
  reason: Align the opening answer with the run summary, target intent, and cluster role.
- `codes.html` -> `meta_refresh`
  reason: Tighten title/meta/H1 alignment around the page’s exact search intent.
- `codes.html` -> `internal_link_addition`
  reason: Strengthen routing between the target page and adjacent cluster pages.
- `diamond-reserve.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `codes.html` from a related cluster page.
- `f2p.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `codes.html` from a related cluster page.
- `farm-account.html` -> `internal_link_addition`
  reason: Add or strengthen the expected bridge into `codes.html` from a related cluster page.

## Candidate Changed Files

- codes.html
- diamond-reserve.html
- f2p.html
- farm-account.html

## Source Files To Edit

- codes.html
- diamond-reserve.html
- f2p.html
- farm-account.html

## Patch Spec v1

- `codes.html` -> `first_screen_update`
  source: `codes.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `codes.html` -> `meta_refresh`
  source: `codes.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `codes.html` -> `internal_link_addition`
  source: `codes.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `diamond-reserve.html` -> `internal_link_addition`
  source: `diamond-reserve.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `f2p.html` -> `internal_link_addition`
  source: `f2p.html`
  generated: `false`
  generator: `None`
  approval: `required`
- `farm-account.html` -> `internal_link_addition`
  source: `farm-account.html`
  generated: `false`
  generator: `None`
  approval: `required`

## Canonical Claims To Protect

- `diamond-reserve-before-reactive-spend`: Diamonds should be protected as reserve first, especially for shield safety and high-value event decisions, not spent reactively on low-value convenience buys.
- `gift-center-cluster-role-separation`: The Gift Center cluster has three distinct roles: codes.html is the hub, gift-center-uid.html is the setup page, and redeem-code-not-working.html is the troubleshooting page.
- `gift-center-only-redeem-flow`: Last Z redeem codes are claimed through the official Gift Center website, not inside the game client.
- `gift-rewards-mailbox`: Redeemed code rewards appear in the in-game mailbox, not as an instant in-page inventory grant.
- `shield-alliance-shop-first`: 8h and 24h shields from the Alliance Shop using alliance points are usually better value than buying shields directly with diamonds when stock is available.
- `uid-copy-path`: The clean UID path is Avatar → Settings → Copy ID.

## Deterministic Checks To Run After Patch Review

- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## Notes

- This is a proposal-only artifact.
- No site files were modified by this step.
- Use this plan to decide whether the next step should be manual editing or a low-risk auto-edit worker.
