# Content Brief: 2026-05-01-redeem-failure-intent

## Overview

- Summary: Update the existing page `redeem-code-not-working.html` for the `Economy` cluster using the `support-guide` archetype.
- Status: `reviewed`
- Risk: `low`
- Cluster: `Economy`
- Archetype: `support-guide`
- Target: `redeem-code-not-working.html`

## Page Goal

This run is meant to update_existing `redeem-code-not-working.html` inside the `Economy` cluster.

## Source Context

- Topic ID: `redeem-failure-intent`
- Title: Redeem code not working refinement
- Source type: `analytics`
- Source reference: GSC/Bing: failure intent early signals
- Confidence: `medium`
- Priority: `medium`

## First-Screen Guidance

- State the main answer near the top.
- Keep the page’s role distinct from neighboring pages in the same cluster.
- Use exact game terminology and preserve canonical claims.
- Lead with a procedural or decision-first answer rather than a broad explanation.

## Canonical Claims To Respect

- `diamond-reserve-before-reactive-spend`: Diamonds should be protected as reserve first, especially for shield safety and high-value event decisions, not spent reactively on low-value convenience buys.
- `gift-center-cluster-role-separation`: The Gift Center cluster has three distinct roles: codes.html is the hub, gift-center-uid.html is the setup page, and redeem-code-not-working.html is the troubleshooting page.
- `gift-center-only-redeem-flow`: Last Z redeem codes are claimed through the official Gift Center website, not inside the game client.
- `gift-rewards-mailbox`: Redeemed code rewards appear in the in-game mailbox, not as an instant in-page inventory grant.
- `shield-alliance-shop-first`: 8h and 24h shields from the Alliance Shop using alliance points are usually better value than buying shields directly with diamonds when stock is available.
- `uid-copy-path`: The clean UID path is Avatar → Settings → Copy ID.

## Related Pages To Consider

- codes.html
- diamond-reserve.html
- f2p.html
- farm-account.html
- gift-center-uid.html
- redeem-code-not-working.html
- refugees.html

## Suggested Page Skeleton

- Quick Answer
- What the user needs to do first
- Common mistake or confusion block
- Step-by-step setup or decision path
- Related links / next step

## SEO / Intent Notes

- Primary target page: `redeem-code-not-working.html`
- Archetype: `support-guide`
- Preserve title/H1/meta alignment with the page’s exact user intent.
- Strengthen internal routing inside the cluster rather than creating duplicate intent pages.

## Deterministic Checks To Run Later

- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py

## Reviewer Context

- Verdict: `needs_human_review`
- Next action: `review_human`

### Reviewer Notes

Deterministic review scaffold complete. The run should explicitly respect these canonical claims: diamond-reserve-before-reactive-spend, gift-center-cluster-role-separation, gift-center-only-redeem-flow, gift-rewards-mailbox, shield-alliance-shop-first, uid-copy-path.
