# Trust Block Rewrite Proposal

Status: proposal only  
Public HTML changes: none  
Prepared: 2026-05-02

## Goal

Reduce repeated sitewide verification boilerplate without weakening trust signals.

The current pattern is useful for SEO and user trust, but it repeats almost the same language across most public pages:

- `How this guide was verified: Based on in-game data, tested results, and cross-checks against community validation.`
- `Last reviewed for the current patch and season context: March 2026.`
- `Source pattern: In-game data + tested results + community validation.`
- `Game mechanics and numbers may change with updates. This guide was last validated in March 2026.`

This proposal keeps the visible `Verification & Review` block, but makes the wording specific to each page family.

## Why This Change Helps

- Makes repeated trust copy less template-like.
- Makes each page clearer about what was actually checked.
- Avoids overclaiming `tested results` on pages that are mostly strategic guidance, routing, or evergreen planning.
- Gives future LLM workers a reusable, page-family-specific pattern instead of one generic trust block.
- Preserves the existing disclaimer and review-date structure unless explicitly changed later.

## Important Implementation Rule

Do not hand-edit generated research branch pages directly.

Generated branch pages should be updated through:

- `scripts/generate_research_branch.py`
- source JSON under `data/research_branches/`
- regeneration with `scripts/generate_research_branch.py`

The shared sync script also needs to be updated:

- `scripts/sync_verification_blocks.py`

Otherwise future `prepublish_check.py --fix` runs may overwrite manual edits with the old generic block.

## Current Source Locations

The repeated trust block currently comes from:

- direct HTML blocks across public guide pages
- `scripts/sync_verification_blocks.py`
- `scripts/generate_research_branch.py`

The proposal below should be applied by updating script-level sources first, then regenerating or syncing affected HTML.

## Proposed Page Families

### 1. Research Branch Cost Pages

Use for generated research branch pages:

- `hero-training-cost.html`
- `military-strategies-cost.html`
- `peace-shield-cost.html`
- `siege-to-seize-cost.html`
- `field-research.html`
- `army-building-cost.html`
- `fully-armed-alliance-cost.html`
- `unit-special-training-cost.html`

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Branch totals were checked against the generated research data source, in-game value checks, and cumulative badge calculations.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> badge costs, unlock requirements, node names, and branch prerequisites can change after research updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this page as planning data before spending badges or saved resources, and confirm final values in-game before committing rare materials.</p>
</section>
```

### 2. Static Cost / Data Pages

Use for non-generated data and cost pages:

- `alliance-recognition-cost.html`
- `alliance-duel-rewards.html`
- `emergency-hospital-cost.html`
- `hq-construction-cost.html`
- `vehicle-modification-cost.html`

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Tables and totals were checked against in-game values, visible requirements, and practical planning use cases.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> costs, rewards, shop values, and event thresholds can change after updates or by server group.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this page for planning, then confirm the current in-game value before spending badges, diamonds, speedups, or rare event items.</p>
</section>
```

### 3. Gift Center / Codes Pages

Use for:

- `codes.html`
- `gift-center-uid.html`
- `redeem-code-not-working.html`

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> The Gift Center flow, UID path, mailbox reward behavior, and code-status guidance were checked against the redemption flow used by this site.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> codes can expire, campaign pages can change, and rewards may vary by account state or server group.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Redeem only through the official Gift Center flow described on this site, then confirm rewards in your in-game mailbox.</p>
</section>
```

### 4. Event Pages

Use for:

- `alliance-duel.html`
- `alliance-duel-rewards.html`
- `events.html`
- `daily.html`
- `furylord.html`
- `gacha-go.html`
- `lucky-discounter.html`
- `svs.html`
- `canyon-clash.html`
- `zombie-siege.html`
- `tyrant.html`

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Event timing, reward logic, preparation advice, and spend/save recommendations were checked against current event structure and site event-routing rules.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> event rotation, rewards, thresholds, and server timing can change after updates or by server group.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as a planning guide, then verify live event timers and reward screens before spending saved items.</p>
</section>
```

### 5. Hero / PvP / Meta Pages

Use for:

- `heroes.html`
- `heroes-es.html`
- `queenie.html`
- `yu-chan.html`
- `formations.html`
- `formation-power.html`
- `pvp.html`
- `trap.html`
- `gear.html`

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Hero, faction, formation, and PvP guidance was checked against current hero roles, faction counters, formation logic, and site canonical PvP guidance.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> hero balance, server meta, faction prevalence, and new-season heroes can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as strategic guidance, then compare it against your server meta and your already-built hero core before spending fragments, gear, or exclusive items.</p>
</section>
```

Spanish page note:

- `heroes-es.html` should receive a Spanish-language equivalent, not the English block above.

### 6. Progression / Economy / Utility Pages

Use for:

- `start.html`
- `early-game-optimization.html`
- `base-building-order.html`
- `shooter-stages.html`
- `hq.html`
- `leveling.html`
- `power-guide.html`
- `resources.html`
- `f2p.html`
- `diamond-reserve.html`
- `refugees.html`
- `farm-account.html`
- `steel.html`
- `shield.html`
- `radar.html`
- `arena.html`
- `tech.html`

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Progression advice was checked against current in-game systems, site canonical economy rules, and practical account-stage tradeoffs.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> costs, event rewards, shop stock, server timing, and upgrade requirements can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as decision support, then verify current in-game values before spending diamonds, speedups, badges, or saved resources.</p>
</section>
```

### 7. Research Hub / Atlas Pages

Use for:

- `research.html`
- `research-costs.html`

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Research priority, branch routing, unlock logic, and cost-page links were checked against the site's research cluster rules and current branch data.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> branch prerequisites, badge costs, unlock names, and long-term priority can change after research updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this page to choose the right research path, then confirm exact branch requirements on the linked cost pages and in-game before spending badges.</p>
</section>
```

## Recommended Application Sequence

1. Update `scripts/sync_verification_blocks.py` to support page-family-specific blocks.
2. Update `scripts/generate_research_branch.py` for generated research branch pages.
3. Run the generator for research branch pages.
4. Run `python3 scripts/sync_verification_blocks.py`.
5. Review the HTML diff manually.
6. Run `python3 scripts/prepublish_check.py --fix`.
7. Run `python3 scripts/prepublish_check.py`.
8. Run `python3 automation/pipeline.py content-voice --top 20`.
9. Run `python3 automation/pipeline.py checks`.
10. Ask for owner approval before committing public content changes.

## Approval Questions

Please approve one of these paths before implementation:

- Full apply: update all page families in one pass.
- Conservative apply: update only generated research cost pages and static cost pages first.
- Copy edit first: adjust the proposed wording, then apply.

My recommended path is conservative apply first, because it fixes the most obviously mismatched wording on data-heavy pages while keeping the blast radius smaller.
