# Core Cornerstone Trust Block Proposal

Scope:

- `power-guide.html`
- `f2p.html`
- `research.html`
- `tips.html`
- `resources.html`
- `hq.html`
- `tech.html`

Purpose:

- Replace repeated trust/disclaimer wording with page-specific verification context.
- Keep current page roles, titles, H1s, internal links, and recommendations unchanged.
- Reduce sitewide repeated trust boilerplate flagged by `content-voice`.
- Preserve canonical claims around research order, diamond reserve, shield value, and resource/progression tradeoffs.

## Proposed Copy

### power-guide.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for power-growth routing:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> HQ requirements, research power, troop training, hero investment, vehicle upgrades, shop priorities, and related progression/economy guides.</li>
                <li><strong>Changes to watch:</strong> displayed power formulas, event rewards, shop stock, vehicle materials, VIP value, and research unlocks can change after updates.</li>
            </ul>
        </section>
        <section class="disclaimer">
            <p>Use this page to choose the next useful power source, not to chase empty CP. Confirm live costs before spending speedups, badges, diamonds, vehicle parts, or hero materials.</p>
        </section>
```

### f2p.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for F2P diamond and shop priorities:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> reserve-first diamond rules, shield safety, refugee value, free diamond sources, shop priority, event timing, and low-spender/F2P constraints.</li>
                <li><strong>Changes to watch:</strong> shop stock, event milestones, shield pricing, refugee value, diamond sources, and server pressure can change after updates.</li>
            </ul>
        </section>
        <section class="disclaimer">
            <p>Use this as a F2P spending filter before buying. Keep emergency diamonds protected first, then compare the live shop or event screen before spending saved currency.</p>
        </section>
```

### research.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for research order and T10 planning:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> the canonical route from Hero Training to Cockpit, Military Strategies, Peace Shield, Siege to Seize, Field Research, linked branch cost pages, and UST planning context.</li>
                <li><strong>Changes to watch:</strong> badge costs, branch prerequisites, node names, unlock requirements, and late-game research value can change after research updates.</li>
            </ul>
        </section>
        <section class="disclaimer">
            <p>Use this page for research direction, then verify exact badge costs and unlock requirements on the linked branch pages and in-game before committing rare badges.</p>
        </section>
```

### tips.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for practical strategy coverage:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> HQ priority, alliance value, focused hero development, daily activity routing, saved-resource timing, and linked progression/economy guides.</li>
                <li><strong>Changes to watch:</strong> event tasks, alliance rewards, building requirements, hero meta, and resource bottlenecks can change after updates or by server age.</li>
            </ul>
        </section>
        <section class="disclaimer">
            <p>Use these tips as a decision checklist, then adapt them to your server age, alliance quality, current event calendar, and strongest built heroes.</p>
        </section>
```

### resources.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for resource farming and protection:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> gathering value, steel sources, chest timing, diamond reserve rules, warehouse protection, farm-account use cases, and related economy guides.</li>
                <li><strong>Changes to watch:</strong> gathering rewards, chest payouts, steel sources, raid pressure, resource building output, and farm-account rules can change after updates.</li>
            </ul>
        </section>
        <section class="disclaimer">
            <p>Use this page to plan resource flow, then confirm live event timing, warehouse safety, and current steel or diamond sources before opening saved chests or exposing resources.</p>
        </section>
```

### hq.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for HQ path and construction requirements:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> HQ level gates, required-building patterns, Sophia construction value, steel phase planning, Alliance Duel timing, and related progression/resource guides.</li>
                <li><strong>Changes to watch:</strong> required buildings, steel availability, construction bonuses, HQ skin values, T11 timing, and server-stage unlocks can change after updates.</li>
            </ul>
        </section>
        <section class="disclaimer">
            <p>Use this page to plan HQ pushes, then check the live requirement screen before spending construction speedups, steel, diamonds, or saved resource boxes.</p>
        </section>
```

### tech.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for F2P and low-spender tech routing:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> Alliance Recognition tradeoffs, Hero Training to Cockpit, Military Strategies, Peace Shield, Siege to Seize, HP stacking, HQ27 trap context, and linked research cost pages.</li>
                <li><strong>Changes to watch:</strong> branch prerequisites, badge costs, unlock names, Fully Armed Alliance value, HP stacking effects, and server meta can change after updates.</li>
            </ul>
        </section>
        <section class="disclaimer">
            <p>Use this page to choose a tech route for your account type, then confirm branch costs in-game before spending badges or delaying core combat research.</p>
        </section>
```

## Not Included

- No public HTML should be changed before owner approval.
- No title, H1, meta, schema, navigation, or recommendation rewrite is included in this batch.
- No generated research branch HTML is included.
- `news-preview.html` remains excluded.

## Implementation Path After Approval

1. Add page-specific groups and blocks to `scripts/sync_verification_blocks.py`.
2. Run `python3 scripts/sync_verification_blocks.py`.
3. Run:
   - `python3 scripts/prepublish_check.py --fix`
   - `python3 scripts/prepublish_check.py`
   - `python3 automation/pipeline.py checks`
   - `python3 automation/pipeline.py checks --strict`
   - `python3 automation/pipeline.py content-voice --top 40`
4. Show the exact diff before commit.

## Follow-Up To Consider Separately

- `tips.html` has hype-style heading language (`Life-Changing Pro Secrets`) that should be reviewed as a separate SEO/voice change, not bundled into this trust-block update.
- `heroes-es.html` and `heroes.html` remain high-risk in `content-voice`, but they are intentionally outside this batch because hero pages need a more careful localized/hero-meta review.
