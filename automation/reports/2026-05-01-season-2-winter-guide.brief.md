# Content Brief: 2026-05-01-season-2-winter-guide

## Overview

- Summary: Create a new page or file `season-2-winter.html` for the `Seasons` cluster using the `support-guide` archetype.
- Status: `reviewed`
- Risk: `high`
- Cluster: `Seasons`
- Archetype: `support-guide`
- Target: `season-2-winter.html`

## Page Goal

This run is meant to create_new `season-2-winter.html` inside the `Seasons` cluster.

## Source Context

- Topic ID: `season-2-winter-guide`
- Title: Season 2 Winter clarification page
- Source type: `research`
- Source reference: Community clarification need: newer servers use Winter as Season 2 and Desert is skipped
- Confidence: `medium`
- Priority: `medium`

## First-Screen Guidance

- State the main answer near the top.
- Keep the page’s role distinct from neighboring pages in the same cluster.
- Use exact game terminology and preserve canonical claims.
- Lead with a procedural or decision-first answer rather than a broad explanation.

## Canonical Claims To Respect

- None

## Related Pages To Consider

- season-2-winter.html

## Suggested Page Skeleton

- Quick Answer
- What the user needs to do first
- Common mistake or confusion block
- Step-by-step setup or decision path
- Related links / next step

## SEO / Intent Notes

- Primary target page: `season-2-winter.html`
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

Deterministic review scaffold complete. No canonical claims matched automatically, so this run should be reviewed carefully before drafting content.
