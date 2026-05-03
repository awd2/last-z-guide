# Trust Block Rewrite Proposal: Events

Status: proposal only  
Public HTML changes: none  
Prepared: 2026-05-03

## Goal

Replace the remaining generic verification boilerplate on event pages with event-specific trust and caution language.

This batch targets event timing, scoring, reward, spend/save, rally, and war-state guidance. It does not change event recommendations, schedules, links, or page structure.

## Current Audit Baseline

After the Hero / PvP / Meta pass:

- high risk: 14
- medium risk: 17
- low risk: 26

Event pages still carrying the old boilerplate include:

- `alliance-duel.html`
- `events.html`
- `daily.html`
- `svs.html`
- `lucky-discounter.html`
- `gacha-go.html`
- `tyrant.html`
- `canyon-clash.html`
- `zombie-siege.html`
- `furylord.html`

`alliance-duel-rewards.html` is not included here because it was already handled in the Static Cost / Data Pages batch.

## Implementation Rule

Apply only after owner approval.

The right implementation path is:

1. Update `scripts/sync_verification_blocks.py` with the page-family mappings below.
2. Run `python3 scripts/prepublish_check.py --fix`.
3. Review the HTML diff manually.
4. Run `python3 scripts/prepublish_check.py`.
5. Run `python3 automation/pipeline.py checks`.
6. Run `python3 automation/pipeline.py checks --strict`.
7. Run `python3 automation/pipeline.py content-voice --top 40`.
8. Commit only after owner review/approval of the resulting public diff.

## Proposed Page Families

### 1. Event Hub Page

Use for:

- `events.html`

Why this family exists:

`events.html` is a routing and priority hub. Its trust language should reference event rotation, spend/save routing, and linked event pages, not a single event mechanic.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Event priority advice was checked against current event routing, spend/save timing, linked event guides, and site economy rules.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> event rotation, reward screens, scoring windows, and server-specific timing can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this page to choose which event guide to open next, then verify the live event timer and reward screen before spending saved items.</p>
</section>
```

### 2. Daily Routine Page

Use for:

- `daily.html`

Why this family exists:

`daily.html` is a routine/checklist page. It should caution around login timing, exposed resources, and daily resets rather than generic mechanic changes.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Daily routine advice was checked against common reset tasks, event routing, exposed-resource risk, and linked safety/economy guides.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> daily reset timing, event tasks, shop stock, and server risk windows can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as a daily checklist, then confirm live timers, exposed resources, and shield needs before logging off or spending saved items.</p>
</section>
```

### 3. Alliance Duel Page

Use for:

- `alliance-duel.html`

Why this family exists:

Alliance Duel has day-by-day scoring and resource timing. Its trust language should reference weekly scoring, day roles, Duel Shop, and saved items.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Alliance Duel advice was checked against day-by-day scoring, saved-item timing, Duel Shop value, and linked reward/research pages.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> scoring tasks, reward thresholds, shop stock, and server event timing can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this to plan your week, then verify the live Alliance Duel day, scoring task, and reward screen before spending speed-ups, badges, or saved items.</p>
</section>
```

### 4. SVS / War-State Page

Use for:

- `svs.html`

Why this family exists:

SVS combines event strategy, PvP risk, shield discipline, and state/server rules. It needs stronger caution language than normal event pages.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> SVS advice was checked against war-state timing, invasion/defense roles, shield discipline, PvP risk, and linked event/economy guidance.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> war rules, state matchmaking, shield timing, scoring windows, and troop-loss risk can change after updates or by server group.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as SVS planning support, then check live state rules, timers, shield coverage, and alliance calls before teleporting or attacking.</p>
</section>
```

### 5. Spend / Save Event Pages

Use for:

- `lucky-discounter.html`
- `gacha-go.html`

Why this family exists:

These pages guide spending and saved-currency timing. Their trust language should reference diamond/event-value decisions and not imply fixed permanent rewards.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Spend-event advice was checked against current reward logic, saved-currency timing, site economy rules, and linked F2P/value guides.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> reward pools, discount values, milestone thresholds, and event timing can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this to decide whether the event is worth your saved currency, then confirm the live reward pool and milestone values before spending diamonds or tickets.</p>
</section>
```

### 6. Combat / Rally Event Pages

Use for:

- `furylord.html`
- `tyrant.html`
- `zombie-siege.html`
- `canyon-clash.html`

Why this family exists:

These pages cover combat/rally/event execution. Their trust language should reference live event rules, damage/scoring, formation choices, and alliance coordination.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Combat-event advice was checked against current event flow, scoring logic, rally/formation requirements, reward timing, and linked PvP/event guides.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> event rules, damage scaling, reward tiers, formation value, and alliance timing can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as event execution guidance, then verify the live event rules, reward tiers, and alliance timing before committing troops, stamina, or saved combat items.</p>
</section>
```

## Pages Not Included In This Batch

These still have generic trust language but should be handled separately:

- `codes.html`
- `gift-center-uid.html`
- `redeem-code-not-working.html`
- `research.html`
- `research-costs.html`
- `tips.html`

Recommended next batches:

- Gift Center / Codes pages
- Research hub / atlas pages
- General tips / sitewide guidance page

## Expected Risk

Low to medium.

Why:

- The change is limited to trust/disclaimer copy.
- No event strategies, reward values, schedules, headings, or links are changed.
- Main risk is overclaiming event freshness, so the wording uses `checked against` and repeatedly tells users to verify live timers/reward screens.

Main review point:

- Confirm the proposed event-language accurately reflects the review level for event rotation and rewards.
