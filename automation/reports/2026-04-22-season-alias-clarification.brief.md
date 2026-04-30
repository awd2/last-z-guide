# Content Brief: 2026-04-22-season-alias-clarification

## Overview

- Summary: Update the existing page `start.html` for the `Seasons` cluster using the `support-guide` archetype.
- Status: `reviewed`
- Risk: `low`
- Cluster: `Seasons`
- Archetype: `support-guide`
- Target: `start.html`

## Page Goal

This run is meant to update_existing `start.html` inside the `Seasons` cluster.

## Source Context

- Topic ID: `season-alias-clarification`
- Title: Season naming clarification update
- Source type: `research`
- Source reference: Canonical claims: Season 2 now maps to Winter on newer servers
- Confidence: `medium`
- Priority: `medium`

## First-Screen Guidance

- State the main answer near the top.
- Keep the page’s role distinct from neighboring pages in the same cluster.
- Use exact game terminology and preserve canonical claims.
- Lead with a procedural or decision-first answer rather than a broad explanation.

## Canonical Claims To Respect

- `season-2-winter-current-naming`: For newer servers, Season 2 is Winter. Desert was canceled or skipped, so older guides that map Season 2 to Desert may be outdated for current players.

## Related Pages To Consider

- start.html

## Suggested Page Skeleton

- Quick Answer
- What the user needs to do first
- Common mistake or confusion block
- Step-by-step setup or decision path
- Related links / next step

## SEO / Intent Notes

- Primary target page: `start.html`
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

Deterministic review scaffold complete. The run should explicitly respect these canonical claims: season-2-winter-current-naming.
