# Core Guides Content Tightening Proposal

Scope:

- `power-guide.html`
- `f2p.html`
- `resources.html`

Purpose:

- Reduce remaining `content-voice` high-risk signals caused by smooth/generic guide language.
- Keep each page's current title, H1, meta, schema, navigation, related links, and canonical recommendations unchanged.
- Replace only selected first-screen and section-opener paragraphs with sharper decision rules.
- Preserve current guidance around HQ/Lab priority, core research, diamond reserve, shields, gathering, steel, and farm accounts.

## Current Audit Signal

From `python3 automation/pipeline.py content-voice --top 15`:

- `power-guide.html` remains high risk: `overall`, `various`, generic guide language.
- `f2p.html` remains high risk: `overall`, `various`, generic guide language.
- `resources.html` remains high risk: `various`, generic guide language.

This proposal does not attempt a broad rewrite. It targets the copy that readers see first and the section openers that repeat broad phrasing.

## Proposed Copy

### power-guide.html

Replace:

```html
            <p class="guide-verified">Best way to increase power in Last Z: grow all 5 power types together, but prioritize HQ and Lab, core research, Alliance Recognition checkpoints, constant troop training, orange gear for your main 5 heroes, and vehicle progression to level 100.</p>
```

With:

```html
            <p class="guide-verified">Power grows fastest when each bottleneck has a job: HQ and Lab unlock the account, core research adds combat value, troops fill capacity, main 5 heroes carry fights, and vehicle level 100 opens components.</p>
```

Replace:

```html
                <p class="qa-lede"><strong>Best way to increase power fast in Last Z:</strong> upgrade all 5 power types together, but put your biggest focus on HQ and Lab, core research, Alliance Recognition checkpoints, troop training, your main 5 heroes, and vehicle progression.</p>
```

With:

```html
                <p class="qa-lede"><strong>Best way to increase power fast in Last Z:</strong> remove the current bottleneck instead of chasing one CP source. Push HQ and Lab first, keep core research moving, train constantly, build the main 5 heroes, and take the vehicle toward level 100.</p>
```

Replace:

```html
                <p>If you want to increase combat power fast in Last Z, the first thing to understand is that CP does not come from one source. Your account grows through 5 separate power types, and the strongest accounts keep all five moving instead of over-investing in only one area.</p>
```

With:

```html
                <p>Combat Power is split across five buckets. If one bucket is far behind, it becomes the bottleneck: low HQ blocks unlocks, weak research lowers real combat value, empty training queues waste troop power, underbuilt heroes lose fights, and a stalled vehicle delays components.</p>
```

Replace:

```html
            <p>For most players, structure power is the fastest reliable early-game source of visible CP because HQ and Laboratory upgrades unlock almost everything else. If your HQ and Lab are behind, your research, troops, and overall progression slow down with them.</p>
```

With:

```html
            <p>Start with HQ and Laboratory because they unlock the rest of the account. If either one is behind, new research, troop tiers, buildings, and event scoring windows all slow down.</p>
```

Replace:

```html
            <p>Research power is one of the best long-term sources of combat value because it improves everything else you do. If you are trying to grow faster without wasting badges, treat Alliance Recognition as an important event-economy branch, but do not let it starve the core combat route when Hero Training, Military Strategies, or Peace Shield are still missing.</p>
```

With:

```html
            <p>Research should answer one question: does the next badge spend unlock more combat value or more event value? Build Alliance Recognition checkpoints when they improve your weekly rewards, but compare each deeper push against Hero Training, Military Strategies, and Peace Shield.</p>
```

Replace:

```html
                <p>Grow all 5 power types together, but prioritize HQ and Lab, core research, Alliance Recognition checkpoints, constant troop training, your main 5 heroes, and vehicle progression to level 100.</p>
```

With:

```html
                <p>Fix the current bottleneck: HQ and Lab for unlocks, core research for combat value, training queues for troop power, main 5 heroes for battle output, and vehicle level 100 for components.</p>
```

### f2p.html

Replace:

```html
            <p class="guide-verified">Best F2P plan for most players: protect your weekly shield reserve first, invest in refugees for long-term speed, and only spend diamonds aggressively when events improve the value instead of wasting them on random convenience.</p>
```

With:

```html
            <p class="guide-verified">F2P diamonds need a job before you spend them: keep 2,000 ready for Friday shields, use extra for refugees or real event discounts, and skip convenience buys that do not protect or compound the account.</p>
```

Replace:

```html
                <p class="qa-lede"><strong>Best Last Z F2P spending priority:</strong> keep 2,000 diamonds by Friday for shields first, then use extra diamonds for refugee tickets, strong discounted events, and other long-term account value instead of random convenience spending.</p>
```

With:

```html
                <p class="qa-lede"><strong>Best Last Z F2P spending priority:</strong> protect 2,000 diamonds for Friday shields, then spend only the surplus on refugee tickets, strong discounts, or event-timed upgrades that return lasting value.</p>
```

Replace:

```html
            <p>F2P diamond income comes from many small and medium sources rather than one jackpot system. The strongest free-to-play accounts stay consistent with arena, events, Furylord, gift codes, and long-term chest value instead of relying on random luck alone.</p>
```

With:

```html
            <p>Treat free diamonds as a weekly budget, not a lucky windfall. Arena, events, Furylord, gift codes, and saved chests all matter because they refill the shield reserve and leave surplus for growth buys.</p>
```

Replace:

```html
            <p>If you are wondering what to buy first as F2P, the best answer is long-term account growth plus reserve discipline. Diamonds should support protection, strong value windows, and lasting account progress instead of random convenience spending.</p>
```

With:

```html
            <p>Before any diamond buy, ask three questions: does it protect my account, create permanent speed, or score during a good event window? If the answer is no, keep the diamonds.</p>
```

Replace:

```html
            <p>One of the biggest differences between weak and strong F2P accounts is timing. Buying the right item during the right event often matters more than buying more items overall.</p>
```

With:

```html
            <p>Timing changes the value of the same purchase. A speedup used on the right Alliance Duel day is worth more than the same speedup used just to finish a timer early.</p>
```

Replace:

```html
            <p>F2P success in Last Z is less about perfect luck and more about discipline. A few repeated rules — shield planning, event timing, focused spending, and avoiding waste — create most of the gap between stable growth and stalled accounts.</p>
```

With:

```html
            <p>Most F2P mistakes are repeat mistakes: breaking the shield reserve, buying speedups directly, spending before the event day, and spreading resources across too many goals. Avoid those first.</p>
```

### resources.html

Replace:

```html
            <p class="guide-verified">Best resource strategy for most players: gather on the world map, skip most resource production buildings, save chests for bulk openings, and treat steel and farm accounts as separate late-game systems.</p>
```

With:

```html
            <p class="guide-verified">Resource growth starts with full gathering marches, not production buildings. Save chests for bulk openings, treat steel as its own bottleneck, and add farm accounts only when your main account regularly runs short.</p>
```

Replace:

```html
                <p class="qa-lede"><strong>Best way to get resources fast in Last Z:</strong> send full marches to gather, prioritize daily tasks and bounty rewards, skip most resource buildings, save chests for bulk openings, and use farm accounts only when your main account starts hitting late-game shortages.</p>
```

With:

```html
                <p class="qa-lede"><strong>Best way to get resources fast in Last Z:</strong> send full marches before downtime, clear daily tasks and bounty rewards, avoid overbuilding production buildings, save chests for bulk openings, and add farms only after regular shortages appear.</p>
```

Replace:

```html
            <p>Not all resources matter in the same way. Food, wood, and electricity drive daily progression, steel becomes a major late-game bottleneck, and diamonds are your flexible premium resource for speeding up key account decisions.</p>
```

With:

```html
            <p>Food, wood, and electricity are daily fuel. Steel is a separate late-game bottleneck. Diamonds are reserve currency, so spend them only when the event or shop value justifies it.</p>
```

Replace:

```html
            <p>If you want resources fast in Last Z, world gathering is the core system to optimize first. Full marches, overnight gathering, high-level nodes, and gathering bonuses do more for your economy than passive production buildings ever will.</p>
```

With:

```html
            <p>Optimize gathering before production. A full overnight march on good nodes usually beats hours of passive building output, especially when gathering heroes and alliance territory bonuses are active.</p>
```

Replace:

```html
            <p>The strongest resource income does not come from one source. The best accounts stack gathering, daily tasks, bounties, events, trucks, and alliance activity so no single shortage slows progression for long. If you want the routine behind this, use the <a href="daily.html">Daily Checklist</a> and the <a href="events.html">Events Schedule</a>.</p>
```

With:

```html
            <p>Do not depend on one source. Stack gathering, daily tasks, bounties, trucks, events, and alliance activity so a missed node or bad chest day does not stop progression. For the routine, use the <a href="daily.html">Daily Checklist</a> and <a href="events.html">Events Schedule</a>.</p>
```

Replace:

```html
            <p>Steel is different from normal resource flow. Once HQ and late-game systems start demanding it, steel becomes a separate bottleneck that needs its own farming plan through Tyrant, nodes, and event sources. See the dedicated <a href="steel.html">Steel Guide</a> for a full breakdown.</p>
```

With:

```html
            <p>Plan steel separately from food, wood, and electricity. When HQ and late-game systems start asking for it, Tyrant rallies, steel nodes, and event rewards become the routine. See the dedicated <a href="steel.html">Steel Guide</a> for the full breakdown.</p>
```

Replace:

```html
            <p>Many players waste builder time on food, wood, electricity, and steel production buildings. In most cases, these buildings are much weaker than map gathering and should stay at minimum levels unless an <a href="hq.html">HQ requirement</a> forces them higher.</p>
```

With:

```html
            <p>Do not spend builder time on production buildings unless an <a href="hq.html">HQ requirement</a> forces it. Gathering creates the real resource flow; production buildings usually cost more attention than they return.</p>
```

## Not Included

- No title, H1, meta, schema, navigation, sitemap, or related-link change is included in this proposal.
- No changes to page recommendations beyond sharper wording of the existing advice.
- No edits to trust/disclaimer blocks in this batch; those were already handled.
- No changes to `diamond-reserve.html`, `shield.html`, `steel.html`, or `farm-account.html`.

## Implementation Path After Approval

1. Apply only the approved paragraph replacements to `power-guide.html`, `f2p.html`, and `resources.html`.
2. Run:
   - `python3 scripts/prepublish_check.py --fix`
   - `python3 scripts/prepublish_check.py`
   - `python3 automation/pipeline.py checks`
   - `python3 automation/pipeline.py checks --strict`
   - `python3 automation/pipeline.py content-voice --top 40`
3. Show the exact diff before commit.

## Follow-Up To Consider Separately

- `power-guide.html` may still need a deeper structure pass later because it repeats the same five-power-type answer in multiple FAQ/summary locations.
- `f2p.html` may need a future diamond-budget table that separates shield reserve, event budget, and surplus growth spending.
- `resources.html` may need future validation of chest jackpot examples and exact bulk-opening claims before any broader rewrite.
