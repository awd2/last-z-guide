# Trust Block Rewrite Proposal: Hero / PvP / Meta

Status: proposal only  
Public HTML changes: none  
Prepared: 2026-05-03

## Goal

Replace the remaining generic trust boilerplate on Hero / PvP / Meta pages with page-family-specific verification language.

This batch is higher-risk than the progression/economy batch because these pages contain faction, meta, hero-ranking, formation, and server-specific claims. The proposal below changes only trust/disclaimer wording. It does not rewrite gameplay recommendations.

## Current Audit Baseline

After the progression/economy/utility pass:

- high risk: 18
- medium risk: 16
- low risk: 23

The main pages for this batch are:

- `heroes.html`
- `heroes-es.html`
- `queenie.html`
- `yu-chan.html`
- `formations.html`
- `formation-power.html`
- `pvp.html`
- `trap.html`
- `gear.html`

## Implementation Rule

Apply only after owner approval.

The right implementation path is:

1. Update `scripts/sync_verification_blocks.py` with the page-family mappings below.
2. Run `python3 scripts/prepublish_check.py --fix`.
3. Review the HTML diff manually.
4. Run `python3 scripts/prepublish_check.py`.
5. Run `python3 automation/pipeline.py checks`.
6. Run `python3 automation/pipeline.py checks --strict`.
7. Run `python3 automation/pipeline.py content-voice --top 35`.
8. Commit only after owner review/approval of the resulting public diff.

## Proposed Page Families

### 1. Hero Hub Page

Use for:

- `heroes.html`

Why this family exists:

`heroes.html` is the main hero-ranking hub. Its trust block should reference faction roles, troop matching, linked hero profiles, and server meta sensitivity.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Hero priorities were checked against current faction roles, troop matching, linked hero profiles, formation guidance, and PvP matchup logic.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> hero balance, server meta, faction prevalence, and new-season heroes can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as a prioritization guide, then compare it against your built roster and server meta before spending fragments, books, gear, or exclusive items.</p>
</section>
```

### 2. Spanish Hero Hub Page

Use for:

- `heroes-es.html`

Why this page is separate:

The page is user-facing Spanish content. The trust block should not remain English if we are improving visible user-facing copy.

Proposed block:

```html
<section class="verification-note" aria-label="Verificación y revisión">
    <p class="verification-note-title">Verificación y revisión</p>
    <ul>
        <li><strong>Base de revisión:</strong> Las prioridades de héroes se revisaron contra roles de facción, emparejamiento de tropas, guías de formación/PvP enlazadas y recomendaciones canónicas del sitio.</li>
        <li><strong>Última revisión para el parche y contexto de temporada actuales:</strong> marzo de 2026.</li>
        <li><strong>Ten cuidado:</strong> el balance de héroes, la meta del servidor, la popularidad de facciones y los héroes de nuevas temporadas pueden cambiar con actualizaciones.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Usa esta guía para priorizar héroes, pero compara la recomendación con tu formación ya construida y la meta de tu servidor antes de gastar fragmentos, libros o equipo.</p>
</section>
```

### 3. Hero Profile Pages

Use for:

- `queenie.html`
- `yu-chan.html`

Why this family exists:

These are individual hero pages. Their trust language should reference skill text, faction role, troop alignment, and linked formation guidance, not a broad hero-tier list.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Hero build advice was checked against visible skill text, faction role, troop alignment, exclusive talent effects, and linked formation guidance.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> skill values, talent effects, hero balance, and faction meta can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as hero-build guidance, then confirm the current skill text and star/talent values in-game before committing rare hero resources.</p>
</section>
```

### 4. Formation Strategy Page

Use for:

- `formations.html`

Why this family exists:

`formations.html` is about matchup logic and formation composition, not raw power display. It should mention server meta and the difference between labels and built heroes.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Formation advice was checked against faction counters, 3+2 matchup logic, troop alignment, hero role coverage, and related PvP guidance.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> server faction mix, available heroes, new-season releases, and PvP meta can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this to choose formation logic, then test it against your server matchups and your strongest built heroes before changing faction investment.</p>
</section>
```

### 5. Formation Power Page

Use for:

- `formation-power.html`

Why this page is separate:

`formation-power.html` is about displayed power levers, same-faction bonuses, troop capacity, and raw power math. It should not use the same trust language as PvP formation-counter pages.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Formation power guidance was checked against displayed power levers, same-faction bonuses, troop-capacity sources, research effects, and related formation/PvP pages.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> power formulas, faction bonuses, research effects, and Hall of Honor values can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this to understand displayed formation power, but do not treat the power number as the only PvP goal; test matchups against your server meta.</p>
</section>
```

### 6. PvP / Trap Pages

Use for:

- `pvp.html`
- `trap.html`

Why this family exists:

These pages guide attack/defense decisions and can affect player losses. Their trust language should emphasize scouting, live server conditions, and risk.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> PvP guidance was checked against scouting signals, faction-counter logic, formation matchup rules, shield discipline, and related SVS/trap guidance.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> server meta, shield timing, war rules, matchmaking, and troop-loss risk can change after updates or by server group.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Use this as PvP decision support, then scout, check live server conditions, and protect critical resources before attacking or setting a trap.</p>
</section>
```

### 7. Equipment / Gear Page

Use for:

- `gear.html`

Why this page is separate:

`gear.html` is equipment progression and paid-resource planning. It should reference gear tiers, enhancement caps, promotion stages, Power Cores, and mythic material risk.

Proposed block:

```html
<section class="verification-note" aria-label="Verification and review">
    <p class="verification-note-title">Verification &amp; Review</p>
    <ul>
        <li><strong>Review basis:</strong> Gear advice was checked against equipment tiers, enhancement caps, promotion stages, Power Core use, mythic requirements, and main-formation priority.</li>
        <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
        <li><strong>Use caution:</strong> gear costs, paid material availability, enhancement caps, and event/shop sources can change after updates.</li>
    </ul>
</section>
```

Disclaimer variant:

```html
<section class="disclaimer">
    <p>Confirm current gear costs and upgrade caps in-game before spending Power Cores, alloys, mythic materials, or saved equipment resources.</p>
</section>
```

## Pages Not Included In This Batch

These still have generic trust language but should be handled later:

- `alliance-duel.html`
- `daily.html`
- `events.html`
- `svs.html`
- `lucky-discounter.html`
- `gacha-go.html`
- `tyrant.html`
- `canyon-clash.html`
- `zombie-siege.html`
- `codes.html`
- `gift-center-uid.html`
- `redeem-code-not-working.html`
- `research.html`
- `research-costs.html`

Recommended next batches:

- Event pages
- Gift Center / Codes pages
- Research hub / atlas pages

## Expected Risk

Medium.

Why:

- Trust/disclaimer language only, but the pages discuss server meta, faction counters, hero tiers, and paid-resource decisions.
- `heroes-es.html` needs Spanish-visible text, which requires closer review than English-only pages.
- `formation-power.html` has owner-approved strong raw-power wording; the disclaimer should clarify displayed power without weakening those approved claims.

Main review point:

- Confirm the proposed wording does not imply stronger validation than the site actually performs for hero rankings and PvP meta.
