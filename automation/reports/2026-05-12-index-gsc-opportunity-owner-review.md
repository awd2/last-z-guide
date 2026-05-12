# Index GSC Opportunity Owner Review

Date: 2026-05-12
Topic: `index-gsc-opportunity`
Target page: `index.html`
Recommended action: narrow home-hub routing copy only
Content status: proposal only, not applied

## Signal Summary

The latest LLM candidate refresh selected `index-gsc-opportunity` from search-performance signals.

- Page: `index.html`
- Clicks: 823
- Impressions: 10,947
- CTR: 7.52%
- Average position: 6.64
- Rising queries noted by the Scout handoff:
  - `last z research guide`
  - `lastzguides.com`

## Page Role Decision

`index.html` should remain the home hub. It should not become the canonical research guide.

The broad research-guide intent should continue to resolve through:

- `research.html` for research priority and decision flow
- `research-costs.html` for cost atlas routing
- generated research branch pages for exact branch costs

The home page can support this intent by making the routing clearer, but it should not absorb the job of `research.html`.

## Risk Review

Risk level: high

Reason:

- `index.html` is the home hub and a high-visibility page.
- It already ranks and receives meaningful search traffic.
- Broad changes to title, H1, metadata, or first-screen structure could disturb current positions.
- The safe opportunity is to clarify routing language, not rewrite the page.

## Recommendation

Do not change:

- `<title>`
- `<h1>`
- meta description
- Open Graph / Twitter metadata
- navigation structure
- page template

Propose only three small copy replacements that preserve the existing template and strengthen hub routing.

## Proposed User-Visible Changes

### 1. Hero paragraph

Before:

```html
<p>Step-by-step guides for what to research first, how event timing works, which heroes to build, how to push HQ efficiently, and how to grow faster as F2P.</p>
```

After:

```html
<p>Use this hub to jump to the right Last Z guide: research order, HQ upgrades, events, heroes, formations, resources, and F2P progression.</p>
```

Reason:

- Makes the page role explicit as a hub.
- Keeps research intent visible without making the home page a research article.
- Avoids generic intro language.

### 2. Featured Guides intro

Before:

```html
<p>The strongest starting points for most players.</p>
```

After:

```html
<p>Start with the page that matches your current goal.</p>
```

Reason:

- Improves routing intent.
- Keeps the section short and utility-first.

### 3. Featured Research card

Before:

```html
<p>Best research order, Peace Shield, Urgent Rescue, and T10 path.</p>
```

After:

```html
<p>Best research order, Peace Shield / Urgent Rescue, and when to choose UST/T10 or late Field Research.</p>
```

Reason:

- Aligns the home-page card with the newer research guidance.
- Avoids implying a single mandatory late path for every player.
- Routes players to `research.html` for the full decision.

## Approval Gate

These changes affect public page copy and require explicit owner approval before application.

If approved, the next implementation step is:

1. Apply only the three exact replacements above to `index.html`.
2. Run:

```bash
python3 scripts/prepublish_check.py --fix
python3 scripts/prepublish_check.py
python3 automation/pipeline.py checks
python3 automation/pipeline.py checks --strict
```

3. Review the diff.
4. Commit and push after checks pass.

