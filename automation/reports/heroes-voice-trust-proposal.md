# Heroes Voice / Trust Proposal

Scope:

- `heroes.html`
- `heroes-es.html`

Purpose:

- Reduce remaining `content-voice` risk on the hero pages.
- Replace repeated or broad trust wording with page-specific hero/faction review context.
- Tighten a small number of smooth first-screen and summary paragraphs.
- Preserve current hero rankings, faction order, troop matching, schema intent, hreflang pairing, and internal links.

## Current Audit Signal

From `python3 automation/pipeline.py content-voice --top 20`:

- `heroes-es.html` is high risk because several visible paragraphs are long and smooth.
- `heroes.html` is high risk partly because the trust block still repeats sitewide wording.
- Neither page should be broadly rewritten in one batch because hero pages carry ranking, faction, and localization risk.

## Proposed Trust Block Copy

### heroes.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for Season 4 hero priorities and faction routing:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> faction roles, troop matching, 3rd-skill value, linked Queenie and Yu Chan profiles, formation guidance, PvP counter logic, and current hero-resource constraints.</li>
                <li><strong>Changes to watch:</strong> new-season heroes, faction prevalence, hero balance, exclusive equipment timing, and server meta can change which heroes are safest to invest in first.</li>
            </ul>
        </section>
        <section class="disclaimer">
            <p>Use this tier list to choose a main faction and main five heroes, then compare it against your built roster and server meta before spending fragments, books, gear, or exclusive items.</p>
        </section>
```

### heroes-es.html

```html
        <section class="verification-note" aria-label="Verificación y revisión">
            <p class="verification-note-title">Verificación y revisión</p>
            <ul>
                <li><strong>Última revisión para prioridades de héroes de Temporada 4 y rutas de facción:</strong> marzo de 2026.</li>
                <li><strong>Revisado contra:</strong> roles de facción, emparejamiento de tropas, valor de la 3.ª habilidad, perfiles enlazados de Queenie y Yu Chan, formación, lógica PvP y límites de recursos de héroes.</li>
                <li><strong>Cambios a vigilar:</strong> nuevos héroes de temporada, popularidad de facciones, balance, equipo exclusivo y meta del servidor pueden cambiar qué héroes conviene potenciar primero.</li>
            </ul>
        </section>
        <section class="disclaimer">
            <p>Usa esta tier list para elegir facción y cinco héroes principales, pero compárala con tu roster construido y la meta de tu servidor antes de gastar fragmentos, libros, equipo o piezas exclusivas.</p>
        </section>
```

## Proposed Voice Tightening

### heroes.html first-screen copy

Replace:

```html
            <p class="guide-verified">Best heroes for most players: Queenie for Wings of Dawn, Yu Chan for Blood Rose, and Amber for Guard of Order, with Wings of Dawn currently the safest faction recommendation for newer accounts.</p>
```

With:

```html
            <p class="guide-verified">Best hero priorities: Queenie for Wings of Dawn, Yu Chan for Blood Rose, and Amber for Guard of Order. Newer accounts usually get the safest start with Wings of Dawn.</p>
```

Replace:

```html
                <p class="qa-lede"><strong>Best Last Z heroes in Season 4:</strong> Queenie leads Wings of Dawn, Yu Chan leads Blood Rose, and Amber leads Guard of Order, while Wings of Dawn is currently the strongest beginner-friendly faction in the meta.</p>
```

With:

```html
                <p class="qa-lede"><strong>Best Last Z heroes in Season 4:</strong> Queenie leads Wings of Dawn, Yu Chan leads Blood Rose, and Amber leads Guard of Order. Build one main faction before spreading hero resources.</p>
```

### heroes.html main summary copy

Replace:

```html
                <p>If you are looking for the best heroes in Last Z, the fastest way to improve your account is not upgrading everyone. Start with your strongest orange combat heroes, match troops to faction, and build one reliable formation before spending on weaker side options.</p>
```

With:

```html
                <p>The fastest hero upgrade path is not upgrading everyone. Start with your strongest orange combat heroes, match troops to faction, and build one reliable formation before spending on side options.</p>
```

Replace:

```html
                <p>The strongest faction in Last Z depends on the current meta, but for most players Wings of Dawn is the safest recommendation because it performs well into the most common Blood Rose teams. Blood Rose remains very strong, while Guard of Order is more niche and matchup-dependent.</p>
```

With:

```html
                <p>For most players, Wings of Dawn is the safest faction route because it plays well into common Blood Rose teams. Blood Rose is still strong; Guard of Order is more niche and matchup-dependent.</p>
```

Replace:

```html
                <p><strong>Key insight:</strong> Defense heroes have ~200k+ stamina and damage absorption. DPS heroes have high damage but die fast when attacked directly. For power optimization, see our <a href="formation-power.html">Formation Power Guide</a>. If you want to turn stronger hero choices into steady weekly value, use the <a href="arena.html">Arena Guide</a>.</p>
```

With:

```html
                <p><strong>Key insight:</strong> defense heroes survive first contact; DPS heroes should stay protected. For power optimization, use the <a href="formation-power.html">Formation Power Guide</a>. For weekly roster value, use the <a href="arena.html">Arena Guide</a>.</p>
```

### heroes-es.html first-screen copy

Replace:

```html
            <p class="guide-verified">Si juegas Last Z y no sabes qué héroes potenciar primero, empieza por tus héroes naranjas principales y prioriza Queenie, Yu Chan o Amber según tu facción. Para la mayoría de cuentas nuevas, Alas del Amanecer es la opción más segura.</p>
```

With:

```html
            <p class="guide-verified">Prioridad rápida: sube tus 5 héroes naranjas principales. Queenie, Yu Chan y Amber son las mejores prioridades por facción; para cuentas nuevas, Alas del Amanecer suele ser la opción más segura.</p>
```

Replace:

```html
                <p class="qa-lede"><strong>Qué héroes potenciar primero en Last Z:</strong> sube antes a tus héroes naranjas principales, céntrate en una sola formación, y prioriza Queenie, Yu Chan o Amber según la facción que uses.</p>
```

With:

```html
                <p class="qa-lede"><strong>Qué héroes potenciar primero en Last Z:</strong> sube tus héroes naranjas principales, juega una sola formación y prioriza Queenie, Yu Chan o Amber según tu facción.</p>
```

### heroes-es.html main summary copy

Replace:

```html
            <p>Si tu pregunta es qué héroes potenciar en Last Z, la respuesta corta es esta: no subas a todos. Invierte primero en tus héroes naranjas de combate y construye una sola formación fuerte antes de repartir recursos entre personajes secundarios.</p>
```

With:

```html
            <p>No subas a todos. Invierte primero en tus héroes naranjas de combate y construye una sola formación fuerte antes de repartir recursos en personajes secundarios.</p>
```

Replace:

```html
            <p>La mejor facción depende del meta, pero para la mayoría de jugadores nuevos Alas del Amanecer es la recomendación más segura. Funciona bien contra composiciones comunes y tiene uno de los mejores héroes de la Temporada 4.</p>
```

With:

```html
            <p>Para la mayoría de jugadores nuevos, Alas del Amanecer es la ruta más segura. Funciona bien contra composiciones comunes y tiene uno de los mejores héroes de Temporada 4.</p>
```

Replace:

```html
            <p>Guardia del Orden puede funcionar, pero normalmente es una opción más específica. Para la mayoría de cuentas no es la mejor primera facción, aunque Amber sigue siendo la prioridad clara si ya juegas con Jinetes.</p>
```

With:

```html
            <p>Guardia del Orden funciona mejor como elección específica. No suele ser la primera facción para una cuenta nueva, pero Amber sigue siendo prioridad si ya juegas con Jinetes.</p>
```

Replace:

```html
                <p><strong>Idea clave:</strong> defensas tienen ~200k+ de stamina y absorción; los DPS tienen alto daño pero mueren rápido si reciben golpes directos. Para optimizar poder, ver <a href="formation-power.html">Guía de Poder de Formaciones</a>.</p>
```

With:

```html
                <p><strong>Idea clave:</strong> las defensas aguantan el primer golpe; los DPS deben quedar protegidos. Para optimizar poder, ver <a href="formation-power.html">Guía de Poder de Formaciones</a>.</p>
```

Replace:

```html
                <p><strong>Rosa Sangrienta</strong> = Asaltantes, <strong>Alas del Amanecer</strong> = Tiradores, <strong>Guardia del Orden</strong> = Jinetes. La 3.ª habilidad de los héroes mejora tipos de tropa específicos y a 5 estrellas el bono suele pasar a todas las tropas.</p>
```

With:

```html
                <p><strong>Rosa Sangrienta</strong> = Asaltantes, <strong>Alas del Amanecer</strong> = Tiradores, <strong>Guardia del Orden</strong> = Jinetes. La 3.ª habilidad mejora tipos concretos de tropa; a 5 estrellas, el bono suele pasar a todas las tropas.</p>
```

## Not Included

- No hero rankings changed.
- No faction order changed.
- No title, H1, meta description, schema, or hreflang change is included.
- No changes to `queenie.html` or `yu-chan.html`.
- No broad localization rewrite.

## Implementation Path After Approval

1. Update `scripts/sync_verification_blocks.py` only for the trust/disclaimer blocks.
2. Apply the approved paragraph replacements directly to `heroes.html` and `heroes-es.html`.
3. Run:
   - `python3 scripts/prepublish_check.py --fix`
   - `python3 scripts/prepublish_check.py`
   - `python3 automation/pipeline.py checks`
   - `python3 automation/pipeline.py checks --strict`
   - `python3 automation/pipeline.py content-voice --top 40`
4. Show the exact diff before commit.

## Follow-Up To Consider Separately

- The hero pages still contain strong claims like `~70% of players`, `S4 heroes are mandatory`, and `all heroes become available within 90 days`. They are existing claims and are not changed in this proposal. A later hero-meta validation pass should review those claims against current evidence before any broader rewrite.
