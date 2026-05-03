# Radar Guide Voice Cleanup Proposal

Status: proposal only, not applied to public HTML
Target page: `radar.html`
Cluster: Events
Archetype: support-guide

## Why This Page Is Next

`python3 automation/pipeline.py content-voice --top 12` currently reports:

- `radar.html`
- risk: `medium`
- score: `6.2`
- specificity: `5.2`
- genericity: `8.5`
- phrase hit: `overall`
- repeated boilerplate hit: `last reviewed for the current`

The page already has a clear job:

- explain the 8-hour radar rhythm
- explain when saving radar for Alliance Duel makes sense
- warn players not to overcap just to force Sunday/Monday or Thursday/Friday timing

This proposal keeps the current page template, title/H1/meta, navigation, and
cluster role. It only tightens a few user-facing lines, adds one small decision
table, and keeps structured data synchronized.

## Canonical Constraints

Keep:

- radar timing rule: check roughly every 8 hours
- do not let radar overcap just to force a save
- Sunday -> Monday and Thursday -> Friday are the main Alliance Duel sync points
- `daily.html`, `events.html`, `alliance-duel.html`, and `resources.html` remain the related route set
- visible FAQ and FAQPage JSON-LD must stay synchronized if FAQ answers change
- HowTo JSON-LD should keep the same 5-step shape unless a visible step changes

Do not change:

- title
- H1
- meta description
- canonical URL
- main navigation
- related guides
- page archetype

## Proposed User-Visible Changes

### 1. HowTo Step 1 Text

Current JSON-LD:

```json
"text": "Radar value comes from consistency. Do not let radar sit too long or you lose possible refreshes and overall daily progress."
```

Proposed JSON-LD:

```json
"text": "Radar value comes from consistency. Do not let radar sit too long or you lose possible refreshes and daily task rhythm."
```

Reason:

- removes generic `overall`
- keeps the same HowTo meaning
- better matches the visible page emphasis on routine

### 2. Quick Answer Callout: Best Tradeoff

Current:

```html
<span class="qa-callout-text"><strong>Best tradeoff:</strong> overall consistency matters more than forcing perfect timing once in a while.</span>
```

Proposed:

```html
<span class="qa-callout-text"><strong>Best tradeoff:</strong> steady 8-hour claims matter more than forcing one perfect weekly save.</span>
```

Reason:

- removes generic `overall`
- makes the tradeoff concrete
- reinforces the page's main player decision

### 3. Add A Small Cap / Save Decision Table

Proposed insertion after the `Best Radar Timing for Daily Progress` section:

```html
<section class="guide-content">
    <h2>Radar Claim Decision Table</h2>
    <table class="data-table">
        <thead>
            <tr>
                <th>Situation</th>
                <th>Best action</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Normal day and radar is not near cap</td>
                <td>Claim roughly every 8 hours</td>
            </tr>
            <tr>
                <td>Sunday and you can hold without capping</td>
                <td>Save claims for Monday Alliance Duel Day 1</td>
            </tr>
            <tr>
                <td>Thursday and you can hold without capping</td>
                <td>Save claims for Friday Alliance Duel Day 5</td>
            </tr>
            <tr>
                <td>Radar is full or close to full</td>
                <td>Claim now instead of forcing the weekly sync</td>
            </tr>
            <tr>
                <td>You will be offline past the next refresh window</td>
                <td>Claim before logging off</td>
            </tr>
        </tbody>
    </table>
</section>
```

Reason:

- adds exact player-useful utility without changing page scope
- makes the overcap rule easier to apply
- improves structured extraction for answer engines

### 4. Verification Block

Current:

```html
<li><strong>Review basis:</strong> Radar advice was checked against the current Radar workflow, task priority logic, refresh value, and daily event routing.</li>
<li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
<li><strong>Use caution:</strong> task pools, refresh value, rewards, and daily-event timing can change after updates.</li>
```

Proposed:

```html
<li><strong>Review basis:</strong> Radar advice was checked against refresh timing, cap-loss risk, Sunday/Monday and Thursday/Friday Alliance Duel sync, and daily event routing.</li>
<li><strong>Last checked:</strong> March 2026 for radar timing and weekly event alignment.</li>
<li><strong>Watch for changes:</strong> task pools, refresh value, rewards, and daily-event timing can change after updates.</li>
```

Reason:

- removes repeated sitewide `Last reviewed for the current...` wording
- makes the verification note page-specific
- keeps the same caution without boilerplate phrasing

## Expected Effect

Expected improvements:

- `radar.html` should move from `medium` to `low` in `content-voice`
- removes all `overall` phrase hits from the page
- removes the repeated verification boilerplate hit
- adds one concrete decision aid for players

Expected risk:

- low content risk if applied exactly
- no template risk
- no cluster role change
- no metadata/title/H1 change
- sitemap/search-index may rebuild normally through prepublish checks

## Approval Needed

If approved, apply these exact changes to `radar.html`, then run:

```bash
python3 scripts/prepublish_check.py --fix
python3 scripts/prepublish_check.py
python3 automation/pipeline.py checks
python3 automation/pipeline.py checks --strict
python3 automation/pipeline.py content-voice --top 12
```

