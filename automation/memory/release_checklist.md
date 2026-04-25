# Release Checklist

This checklist is the minimum editorial and QA gate before a content change should be considered ready for merge.

## Editorial Gate

- The page has one clear primary query family.
- The page has one clear primary job.
- The first screen answers the main user question.
- The title, H1, and meta description match the real intent of the page.
- The title, H1, meta description, and first-screen answer are aligned with each other.
- New or changed claims do not contradict canonical site knowledge.
- The terminology matches the rest of the site.
- The page is linked into the correct cluster:
  - upstream hub
  - downstream support page or atlas
  - related guide if relevant
- The change does not create avoidable keyword or intent cannibalization with an existing winner.

## Content Quality Gate

- The page is materially useful, not just longer.
- Any FAQ added is justified by real user intent.
- Numbers, totals, and unlock requirements are internally consistent.
- If the page touches seasons/events/community naming, ambiguity is explicitly clarified.
- If a narrow support page was created, its role is distinct from existing nearby pages.

## Technical Gate

- Run `python3 scripts/prepublish_check.py --fix`
- Run `python3 scripts/prepublish_check.py`
- Confirm `sitemap.xml` and `search-index.json` are in sync.
- Confirm modified pages still have valid canonical/meta/structured data.
- Confirm structured data still matches visible page content.
- Confirm important new/changed pages are reachable through crawlable internal links, not only through sitemap inclusion.

## UI / Integration Gate

- New blocks match the site’s spacing and typography rhythm.
- Mobile layout was checked for the changed pages.
- Internal cards, tree views, tables, and planners still render correctly.
- Home and hub integrations are intentional, not accidental noise.

## Release Decision

The change should be marked:

- `low-risk` if:
  - it is a focused update to an existing page
  - it uses a stable template
  - it does not change canonical claims

- `high-risk` if:
  - it introduces a new cornerstone page
  - it changes season/event interpretation
  - it rewrites a winning hub page
  - it changes high-traffic layouts or cluster routing

## Production Rule

No autonomous publish to production.

Required path:
1. draft changes
2. review
3. green deterministic checks
4. manual approval
5. merge / deploy
