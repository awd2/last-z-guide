# Patch Plan: 2026-05-05-codes-gsc-opportunity-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `codes.html` from `codes-gsc-opportunity`.
- Status: `patch_plan_ready`
- Risk: `high`
- Cluster: `Economy`
- Target: `codes.html`
- Archetype: `cornerstone-guide`

## Proposed File Changes

- `codes.html` -> `first_screen_update`
  reason: Align the opening answer with the run summary, target intent, and cluster role.
- `codes.html` -> `meta_refresh`
  reason: Tighten title/meta/H1 alignment around the page’s exact search intent.

## Candidate Changed Files

- codes.html

## Source Files To Edit

- codes.html

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

## Canonical Claims To Protect

- `gift-center-cluster-role-separation`: The Gift Center cluster has three distinct roles: codes.html is the hub, gift-center-uid.html is the setup page, and redeem-code-not-working.html is the troubleshooting page.
- `gift-center-only-redeem-flow`: Last Z redeem codes are claimed through the official Gift Center website, not inside the game client.
- `gift-rewards-mailbox`: Redeemed code rewards appear in the in-game mailbox, not as an instant in-page inventory grant.

## Deterministic Checks To Run After Patch Review

- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

## Notes

- This is a proposal-only artifact.
- No site files were modified by this step.
- Use this plan to decide whether the next step should be manual editing or a low-risk auto-edit worker.
