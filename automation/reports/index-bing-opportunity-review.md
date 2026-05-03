# Index Bing Opportunity Review - 2026-05-03

## Verdict

No homepage content edit is recommended right now.

The Bing signal is useful, but it is not strong enough to justify changing `index.html`, because GSC shows the homepage already performs well for its core branded and guide-navigation intent. The current issue looks like Bing broad-query ambiguity around `last z`, not a clear homepage snippet or first-screen failure.

## Source Signals

- Bing latest bucket: `2026-05-01`
- Bing page opportunity: `index.html`
  - impressions: `977`
  - clicks: `23`
  - CTR: `2.35%`
  - position: `6.00`
- Bing query opportunity:
  - query: `last z`
  - impressions: `337`
  - clicks: `1`
  - CTR: `0.30%`
  - position: `7.00`
- Bing `query_page_pairs`: `0`
  - no fetch errors were reported
  - current Bing API output does not confirm which page served the `last z` query

## GSC Cross-Check

GSC does not show a matching homepage weakness.

Homepage query-page pairs in `content/gsc/latest-gsc-agent-signals.json`:

| Query | Clicks | Impr. | CTR | Pos. |
| --- | ---: | ---: | ---: | ---: |
| last z guide | 270 | 417 | 64.75% | 1.34 |
| last z guides | 47 | 61 | 77.05% | 1.03 |
| last z research | 44 | 205 | 21.46% | 4.19 |
| lastz guide | 41 | 57 | 71.93% | 1.16 |
| lastzguides.com | 16 | 32 | 50.00% | 1.00 |
| lastzguides | 13 | 23 | 56.52% | 2.78 |
| last z research guide | 11 | 209 | 5.26% | 8.35 |

Interpretation:

- branded guide queries are strong
- the homepage is already a useful route for `last z guide`, `last z guides`, and `lastz guide`
- the weaker `last z research guide` intent is better handled by `research.html`, not by making the homepage more research-heavy

## Current Homepage Fit

`index.html` is correctly classified as:

- cluster: `Home`
- archetype: `home-hub`
- primary job: route users into the strongest clusters
- freshness priority: `high`

Current first-screen elements are aligned:

- title: `Last Z Guides (2026) - Research, Events, HQ, Heroes, and F2P Strategy`
- H1: `Last Z Guides - Research, Events, HQ, Heroes, and F2P Strategy`
- meta description: covers research order, HQ upgrades, events, heroes, formations, resource planning, and F2P progression
- visible hero copy: explains the same route-first value
- featured guides: routes to `research.html`, `alliance-duel.html`, `hq.html`, `heroes.html`, `f2p.html`, and `events.html`

The page matches the `home-hub` archetype. A larger rewrite would be high risk and could weaken established branded-guide performance.

## Recommendation

Do not edit `index.html` from this Bing signal alone.

Keep the Bing signal as a watch item:

- watch `last z` in the next 2-3 Bing weekly reports
- wait for Bing query-page detail, if available later
- compare against future GSC homepage query-page rows
- only propose a homepage metadata or hero-copy change if both Bing and GSC show a persistent homepage CTR issue

If action becomes justified later, prefer a small snippet-level test, not a layout or routing rewrite.

## Possible Future Test

Only if future data confirms the issue, consider testing a slightly more direct homepage meta description:

```text
Last Z guides for research priority, HQ upgrades, events, heroes, formations, F2P diamonds, and weekly progression routes. Pick the guide that matches your next upgrade.
```

This is not approved for application. It is a future test candidate only.

## Next Step

Use Bing weekly reports as agent context, but do not let Bing-only signals create content tasks on high-risk pages without GSC confirmation and owner approval.
