# Exact Content Proposal: Alliance Duel Schedule / VS Intent

Source run: `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake`
Target page: `alliance-duel.html`
Status: owner review required before any page edit

## Scope

This is a proposal-only artifact. No public content has been changed.

Goal:

- sharpen the first-screen match for `last z vs schedule` and `Last Z Alliance Duel schedule`
- keep `alliance-duel.html` as an `event-guide`, not a broader Events hub
- keep the Day 1-6 schedule plus existing timing caveats
- keep related guides unchanged unless a later review finds obvious overlap

## Recommended Decision

Approve a narrow first-screen and metadata update only.

Do not add new sections, change the page template, change schema family, or rewrite the full guide.

## Exact Proposed Replacements

### 1. HTML title

Before:

```html
<title>Last Z Alliance Duel Guide (2026) — Schedule, Day 1–6 Plan, VS Strategy</title>
```

After:

```html
<title>Last Z Alliance Duel Schedule (2026) — Day 1–6 VS Guide and Strategy</title>
```

Reason:

- leads with `Alliance Duel Schedule`, the strongest exact query family
- keeps `VS Guide` for players who search for the VS schedule
- preserves the existing guide/strategy role

### 2. Meta description

Before:

```html
<meta name="description" content="Complete Last Z Alliance Duel schedule: Day 1–6 plan, when to use speed-ups, how VS schedule works, and the best F2P strategy for more weekly chests.">
```

After:

```html
<meta name="description" content="Use this Last Z Alliance Duel schedule to follow the Day 1–6 VS rotation, match speed-ups to each day, sync Full Preparedness, and plan weekly rewards.">
```

Reason:

- gives the concrete player action immediately
- keeps Full Preparedness timing in the snippet
- avoids promising a broader event hub

### 3. Open Graph title

Before:

```html
<meta property="og:title" content="Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, VS Strategy">
```

After:

```html
<meta property="og:title" content="Last Z Alliance Duel Schedule — Day 1–6 VS Guide">
```

### 4. Open Graph description

Before:

```html
<meta property="og:description" content="Alliance Duel schedule by day, best speed-up timing, VS plan, and the most efficient F2P strategy for weekly rewards.">
```

After:

```html
<meta property="og:description" content="Alliance Duel Day 1–6 schedule, VS timing, matching speed-up rules, Full Preparedness sync, and weekly reward planning.">
```

### 5. Twitter title

Before:

```html
<meta name="twitter:title" content="Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, VS Strategy">
```

After:

```html
<meta name="twitter:title" content="Last Z Alliance Duel Schedule — Day 1–6 VS Guide">
```

### 6. Twitter description

Before:

```html
<meta name="twitter:description" content="Alliance Duel schedule by day, best speed-up timing, VS plan, and the most efficient F2P strategy for weekly rewards.">
```

After:

```html
<meta name="twitter:description" content="Alliance Duel Day 1–6 schedule, VS timing, matching speed-up rules, Full Preparedness sync, and weekly reward planning.">
```

### 7. Article headline

Before:

```json
"headline": "Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy"
```

After:

```json
"headline": "Last Z Alliance Duel Schedule and VS Guide — Day 1–6 Plan"
```

### 8. Article description

Before:

```json
"description": "Complete Alliance Duel guide for Last Z: Survival Shooter with a day 1–6 schedule, VS timing strategy, and F2P tips"
```

After:

```json
"description": "Day 1–6 Alliance Duel schedule for Last Z with VS timing, matching speed-up rules, Full Preparedness sync, and weekly reward planning"
```

### 9. H1

Before:

```html
<h1>Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy</h1>
```

After:

```html
<h1>Last Z Alliance Duel Schedule and VS Guide — Day 1–6 Plan</h1>
```

Reason:

- keeps the page readable as a guide
- makes schedule/VS intent explicit in the visible H1

### 10. Guide verified line

Before:

```html
<p class="guide-verified">Best Alliance Duel plan for most players: follow the Day 1–6 schedule, match speed-ups to the right day, sync with Full Preparedness, and prioritize Alliance Recognition for long-term rewards.</p>
```

After:

```html
<p class="guide-verified">Best Alliance Duel / VS schedule plan for most players: follow the Day 1–6 rotation, spend saved items only on the matching day, sync big actions with Full Preparedness, and use Alliance Recognition for long-term reward value.</p>
```

Reason:

- adds the VS schedule alias without changing the event role
- keeps the existing Full Preparedness and Alliance Recognition guidance

### 11. Quick Answer lede

Before:

```html
<p class="qa-lede"><strong>Best Last Z Alliance Duel schedule for most players:</strong> Day 1 Vehicle, Day 2 Building, Day 3 Research, Day 4 Heroes, Day 5 Training, Day 6 Combat — and you should only use the matching speed-ups on the correct day.</p>
```

After:

```html
<p class="qa-lede"><strong>Best Last Z Alliance Duel / VS schedule for most players:</strong> Day 1 Vehicle, Day 2 Building, Day 3 Research, Day 4 Heroes, Day 5 Training, Day 6 Combat — spend only on the matching day, and time your biggest actions with Full Preparedness at Apocalypse Time 08:00 or 20:00 when you can.</p>
```

Reason:

- answers the VS schedule intent on the first screen
- keeps the Day 1-6 order
- keeps the timing caveat requested by the owner

## Related Guides Decision

Recommended: no change for this proposal.

Current related links:

- `events.html`
- `radar.html`
- `alliance-duel-rewards.html`
- `lucky-discounter.html`
- `svs.html`

Reason:

- `events.html` is the upstream Events hub
- `radar.html`, `alliance-duel-rewards.html`, and `lucky-discounter.html` support current page sections
- `svs.html` may help users who confuse VS, Alliance Duel, and State vs State
- no obvious overlap requires trimming before a content edit

## Approval Required

Owner approval is required before applying this proposal to `alliance-duel.html`.

Approval should be explicit for the exact text above. If approved, the apply step should:

1. edit only `alliance-duel.html`
2. preserve the existing template and structured data types
3. run:
   - `python3 scripts/prepublish_check.py --fix`
   - `python3 scripts/prepublish_check.py`
   - `python3 automation/pipeline.py checks --strict --manifest 2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake`
4. verify `search-index.json` and `sitemap.xml` only change as expected
