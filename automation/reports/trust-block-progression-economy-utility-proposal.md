# Trust Block Rewrite Proposal: Progression, Economy, Utility

Status: proposal only  
Public HTML changes: none  
Prepared: 2026-05-03

## Goal

Replace the remaining generic verification boilerplate on progression, economy, and utility pages with page-family-specific trust language.

This is the next batch after the approved data/cost-page rewrite. It targets pages that still rank high in `content-voice` because they repeat the old generic pattern:

- `How this guide was verified`
- `Source pattern: In-game data + tested results + community validation`
- `Game mechanics and numbers may change with updates`
- `This guide was last validated in March 2026`

The goal is not to remove trust signals. The goal is to make them more precise and less mass-produced.

## Current Audit Baseline

After the data/cost-page pass:

- high risk: 22
- medium risk: 21
- low risk: 14

Top remaining pages in this batch include:

- `power-guide.html`
- `f2p.html`
- `resources.html`
- `hq.html`
- `tech.html`
- `shield.html`
- `radar.html`
- `diamond-reserve.html`
- `shooter-stages.html`
- `arena.html`
- `steel.html`
- `refugees.html`
- `base-building-order.html`

## Implementation Rule

Apply only after owner approval.

The right implementation path is:

1. Update `scripts/sync_verification_blocks.py` with the page-family mappings below.
2. Run `python3 scripts/prepublish_check.py --fix`.
3. Review the HTML diff manually.
4. Run `python3 scripts/prepublish_check.py`.
5. Run `python3 automation/pipeline.py checks`.
6. Run `python3 automation/pipeline.py checks --strict`.
7. Run `python3 automation/pipeline.py content-voice --top 30`.
8. Commit only after owner review/approval of the resulting public diff.

## Proposed Page Families

### 1. Progression Planning Pages

Use for:

- `start.html`
- `early-game-optimization.html`
- `base-building-order.html`
- `shooter-stages.html`
- `hq.html`
- `leveling.html`
- `power-guide.html`

Why this family exists:

These pages are not pure data tables. They help players decide progression order, account-stage priorities, and where not to waste speedups/resources.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Progression advice was checked against current in-game systems, HQ and resource bottlenecks, unlock flow, and practical account-stage tradeoffs.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> upgrade requirements, event rewards, shop stock, and server timing can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as decision support, then confirm current in-game values before spending diamonds, speedups, badges, or saved resources.</p>
</section>
```

### 2. Economy / Reserve Pages

Use for:

- `f2p.html`
- `resources.html`
- `diamond-reserve.html`
- `steel.html`
- `refugees.html`

Why this family exists:

These pages are tied to the site's canonical economy stance: reserve-first diamonds, shield safety, and avoiding reactive low-value spending.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Economy advice was checked against site canonical reserve-first rules, resource bottlenecks, event-value tradeoffs, and F2P account constraints.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> shop stock, event rewards, resource packages, and server pressure can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Protect reserve resources first, then confirm current shop and event values before spending diamonds or saved items.</p>
</section>
```

### 3. Farm Account Page

Use for:

- `farm-account.html`

Why this page is separate:

`farm-account.html` is economy-adjacent, but it also touches account behavior and rules. It should not use the same spend/value disclaimer as normal resource pages.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Farm-account guidance was checked against practical resource-transfer use cases, account safety concerns, and current site economy rules.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> account rules, transfer limits, event behavior, and server enforcement can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as a risk-aware planning guide, and check current game/account rules before building a long-term farm setup.</p>
</section>
```

### 4. Shield Safety Page

Use for:

- `shield.html`

Why this page is separate:

`shield.html` is governed by two canonical economy claims:

- diamonds should stay reserve-first
- Alliance Shop shields are usually better value than direct diamond shield buys when stock exists

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Shield guidance was checked against reserve-first diamond rules, Alliance Shop shield value, PvP risk windows, and saved-resource protection.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> Alliance Shop stock, shield pricing, server war timing, and event pressure can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Check Alliance Shop stock and current server risk before spending diamonds on shields directly.</p>
</section>
```

### 5. Daily Utility Pages

Use for:

- `radar.html`

Why this family exists:

Radar is a support workflow page. It should explain that task pools and rewards can move, not use broad `game mechanics and numbers` language.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Radar advice was checked against the current Radar workflow, task priority logic, refresh value, and daily event routing.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> task pools, refresh value, rewards, and daily-event timing can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this to choose Radar tasks faster, then confirm the live task reward before spending refreshes or saved resources.</p>
</section>
```

### 6. Arena Support Page

Use for:

- `arena.html`

Why this page is separate:

Arena is a PvP support page, but not a full meta page. The trust language should reference matchup logic and attempts/rewards, not hero-tier claims.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Arena advice was checked against daily attempt flow, reward timing, formation matchup logic, and related PvP guidance.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> matchmaking, rewards, formation meta, and server competition can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as a daily Arena checklist, then compare matchups against your server meta before spending extra attempts or formation resources.</p>
</section>
```

### 7. Research-System Edge Case

Use for:

- `tech.html`

Why this page is included carefully:

`tech.html` is a Research cluster page, but it appears in the same voice-risk group as broad progression pages. Its trust language should reference research priority and unlock checkpoints, not generic guide verification.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Research and tech-priority advice was checked against the site's mainline research route, unlock checkpoints, and linked branch cost pages.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> branch prerequisites, badge costs, unlock names, and late-game tech value can change after research updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this to choose research direction, then confirm exact branch requirements on the linked cost pages and in-game before spending badges.</p>
</section>
```

## Pages Not Included In This Batch

These pages still have repeated trust language, but should be handled in later, more specific batches:

- `heroes.html`
- `heroes-es.html`
- `formations.html`
- `formation-power.html`
- `pvp.html`
- `trap.html`
- `gear.html`
- `queenie.html`
- `yu-chan.html`

Recommended later batch:

- Hero / PvP / Meta trust blocks, including a Spanish-language version for `heroes-es.html`.

These pages should not be mixed into the progression/economy batch because they depend on meta, faction, hero-role, and server-specific language.

## Recommended Approval Path

Recommended apply scope:

1. Full apply for all pages listed in this proposal.
2. Keep Hero / PvP / Meta pages for the next batch.
3. Keep Gift Center / Codes pages for a separate small batch.

Reason:

This batch is large enough to materially reduce boilerplate, but still coherent: it covers account progression, resource economy, and operational support pages without touching hero/meta claims.

## Expected Risk

Low to medium.

Why:

- The copy changes trust/disclaimer language only.
- No gameplay recommendation sections are being rewritten.
- No title/H1/meta/internal-link changes are proposed.
- The implementation should be deterministic through `scripts/sync_verification_blocks.py`.

Main review point:

- Confirm that the proposed trust language accurately describes how much validation these broad pages actually receive.
