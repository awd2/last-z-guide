# Content Brief: 2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `alliance-duel.html` from `alliance-duel-gsc-opportunity`.
- Status: `reviewed`
- Risk: `medium`
- Cluster: `Events`
- Archetype: `event-guide`
- Target: `alliance-duel.html`

## Page Goal

This run is meant to update_existing `alliance-duel.html` inside the `Events` cluster.

## Source Context

- Topic ID: `alliance-duel-gsc-opportunity-llm-approved-intake`
- Title: GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy
- Source type: `llm_scout`
- Source reference: LLM worker chain review: alliance-duel-gsc-opportunity
- Confidence: `high`
- Priority: `high`

## First-Screen Guidance

- State the main answer near the top.
- Keep the page’s role distinct from neighboring pages in the same cluster.
- Use exact game terminology and preserve canonical claims.

## Canonical Claims To Respect

- None

## Related Pages To Consider

- alliance-duel.html

## Suggested Page Skeleton

- Quick Answer
- Timing / schedule block
- Best strategy block
- Rewards / value block
- Related links

## SEO / Intent Notes

- Primary target page: `alliance-duel.html`
- Archetype: `event-guide`
- Preserve title/H1/meta alignment with the page’s exact user intent.
- Strengthen internal routing inside the cluster rather than creating duplicate intent pages.

## Deterministic Checks To Run Later

- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict

## Reviewer Context

- Verdict: `needs_human_review`
- Next action: `review_human`

### Reviewer Notes

Deterministic review scaffold complete. No canonical claims matched automatically, so this run should be reviewed carefully before drafting content.
