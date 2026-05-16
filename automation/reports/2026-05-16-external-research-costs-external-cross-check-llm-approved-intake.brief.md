# Content Brief: 2026-05-16-external-research-costs-external-cross-check-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `research-costs.html` from `external-research-costs-external-cross-check`.
- Status: `reviewed`
- Risk: `high`
- Cluster: `Research`
- Archetype: `atlas-page`
- Target: `research-costs.html`

## Page Goal

This run is meant to update_existing `research-costs.html` inside the `Research` cluster.

## Source Context

- Topic ID: `external-research-costs-external-cross-check-llm-approved-intake`
- Title: External source opportunity: research cost and branch coverage cross-check
- Source type: `analytics`
- Source reference: LLM worker chain review: external-research-costs-external-cross-check
- Confidence: `high`
- Priority: `high`

## First-Screen Guidance

- State the main answer near the top.
- Keep the page’s role distinct from neighboring pages in the same cluster.
- Use exact game terminology and preserve canonical claims.
- Help users choose the correct detailed page instead of over-expanding the hub.

## Canonical Claims To Respect

- `field-research-follows-siege`: Field Research follows 100% Siege to Seize and contains the final Recharge Shield path and major late badge pressure.
- `research-atlas-role`: research-costs.html is the atlas/hub for the research cost cluster. It should compare branches and route to exact tree pages, not replace them.
- `research-best-mainline`: The main research route for most players is Hero Training to Cockpit, then Military Strategies, then Peace Shield/Urgent Rescue. After that, players should choose by goal: use the shortest practical UST/T10 path for tier progression, or push Siege to Seize into Field Research only for late-game Recharge Shield/deep combat scaling.

## Related Pages To Consider

- research-costs.html

## Suggested Page Skeleton

- Quick Answer
- Cluster overview
- Comparison grid / card list
- Recommended route or progression path
- Links into exact pages

## SEO / Intent Notes

- Primary target page: `research-costs.html`
- Archetype: `atlas-page`
- Preserve title/H1/meta alignment with the page’s exact user intent.
- Strengthen internal routing inside the cluster rather than creating duplicate intent pages.

## Deterministic Checks To Run Later

- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict

## Reviewer Context

- Verdict: `needs_human_review`
- Next action: `review_human`

### Reviewer Notes

Deterministic review scaffold complete. The run should explicitly respect these canonical claims: field-research-follows-siege, research-atlas-role, research-best-mainline.
