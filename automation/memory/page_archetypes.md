# Page Archetypes

This file defines the page families the editorial pipeline should choose from before drafting or editing content. The system should pick the smallest archetype that fits the user intent instead of defaulting to “new article”.

## `home-hub`
- Example: `index.html`
- Purpose: route users into the strongest topic clusters.
- Must do:
  - sell the site’s main clusters
  - keep cards concise and scannable
  - avoid overloading home with too many deep-support pages

## `site-page`
- Examples: `about.html`, `privacy.html`, `terms.html`
- Purpose: trust/legal/site utility.
- Must do:
  - stay factual
  - stay stable
  - avoid SEO stuffing or editorial experimentation

## `cornerstone-guide`
- Examples: `research.html`, `heroes.html`, `events.html`, `codes.html`, `f2p.html`
- Purpose: broad topic winner for a core intent cluster.
- Must do:
  - answer the main query immediately
  - establish canonical stance for the cluster
  - route users into narrower support pages and atlases
- Good for:
  - broad search intents
  - LLM citations when the user asks a high-level question

## `support-guide`
- Examples: `gift-center-uid.html`, `radar.html`, `shield.html`, `arena.html`
- Purpose: narrow intent, one concrete problem or workflow.
- Must do:
  - have a very clear first-screen answer
  - solve one exact job
  - link back into the hub and sideways into adjacent support pages
- Good for:
  - CTR improvement on exact queries
  - LLM answers for operational questions

## `event-guide`
- Examples: `alliance-duel.html`, `furylord.html`, `lucky-discounter.html`
- Purpose: event-specific strategy, timing, scoring, rewards, or preparation.
- Must do:
  - clarify schedule or rotation when relevant
  - say who the event matters for
  - bridge into supporting economy/progression pages

## `hero-profile`
- Examples: `queenie.html`, `yu-chan.html`
- Purpose: profile of one hero/unit with build and prioritization guidance.
- Must do:
  - keep entity naming consistent with the rest of the site
  - connect back to hero hubs, formations, and role-specific guides

## `comparison-guide`
- Examples: `formations.html`
- Purpose: compare options, routes, builds, or tradeoffs.
- Must do:
  - compare clearly and explicitly
  - avoid vague “it depends” language without decision criteria

## `atlas-page`
- Examples: `research-costs.html`
- Purpose: directory or map into a cluster of exact-intent pages.
- Must do:
  - summarize the landscape quickly
  - compare entities/pages at a glance
  - route users into the correct detailed page
- Good for:
  - cluster discoverability
  - query families like “all X”, “best X paths”, “compare X branches”

## `cost-page`
- Examples: `alliance-recognition-cost.html`, `vehicle-modification-cost.html`, research branch cost pages
- Purpose: exact numbers, totals, planners, tables, or tree breakdowns.
- Must do:
  - use answer-first framing
  - present exact values cleanly
  - prefer structured, scannable layouts over long prose
  - keep the source of truth consistent across tables, trees, and summaries

## `news-digest`
- Example: `news-preview.html`
- Purpose: internal or preview-style digest, not a stable evergreen winner.
- Must do:
  - stay clearly marked as preview/draft when applicable
  - avoid being treated as a canonical evergreen guide

## Archetype Selection Rules

When choosing an archetype:

1. Prefer updating an existing `cornerstone-guide` or `support-guide` before creating a duplicate.
2. Use `atlas-page` when the real job is navigation across multiple related pages, not just a single answer.
3. Use `cost-page` when the value comes from exact figures, planners, node maps, or structured breakdowns.
4. Use `support-guide` when the query is highly operational:
   - login
   - where to find X
   - how to redeem/fix/unlock/claim
5. Escalate to human review when a new page could also plausibly fit two archetypes.

## URL / Scope Decision Ladder

Before creating a new URL, decide in this order:

1. **Sharpen an existing winner**
   - If the real issue is title/meta/first-screen fit, improve the current page first.
2. **Add a section to an existing page**
   - If the user job is adjacent to a strong current page and does not justify a separate workflow.
3. **Create or refine a `support-guide`**
   - If the user job is exact, operational, and distinct.
4. **Add or refine an `atlas-page` entry**
   - If discoverability across a cluster is the real problem.
5. **Create a new `cornerstone-guide`**
   - Only when the topic is broad enough to own a full cluster and route users into narrower pages.

Use a new page only when it improves intent fit without creating avoidable cannibalization.
