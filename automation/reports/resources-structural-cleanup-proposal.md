# Resources Guide Structural Cleanup Proposal

Status: proposal only, not applied to public HTML
Target page: `resources.html`
Cluster: Economy
Archetype: cornerstone-guide

## Why This Page Is Next

`python3 automation/pipeline.py content-voice --top 12` still flags
`resources.html` as high risk:

- score: 12.2
- specificity: 10.8
- genericity: 17.0
- main issue: useful page structure, but several broad lines still read like
  generic guide copy or overstate jackpot outcomes.

The page already has strong SEO basics:

- title, H1, meta, canonical, Article schema, FAQ schema, and related links exist
- primary query match is clear: resource farming, steel, diamonds, farm accounts
- template should be preserved

This proposal keeps the current page template and search intent, while tightening
the copy around resource decision-making.

## Canonical Constraints

Keep:

- diamonds are reserve-first
- food, wood, and electricity are daily flow resources
- steel is a separate late-game bottleneck
- farm accounts are not an early-game requirement for most players
- resource buildings should stay near requirement levels unless HQ progression
  forces upgrades
- visible FAQ and FAQPage JSON-LD must stay synchronized

Do not change:

- title
- H1
- meta description
- canonical URL
- navigation
- related guide set
- page archetype

## Proposed User-Visible Changes

### 1. Guide Verified Summary

Current:

```html
<p class="guide-verified">Resource growth starts with full gathering marches, not production buildings. Save chests for bulk openings, treat steel as its own bottleneck, and add farm accounts only when your main account regularly runs short.</p>
```

Proposed:

```html
<p class="guide-verified">Resource growth starts with full gathering marches and daily rewards. Keep builders off production buildings unless HQ requires them, save chests for bulk openings, treat steel separately, and add farms only after regular shortages appear.</p>
```

Reason:

- keeps the same first-screen answer
- makes the builder decision more concrete
- avoids sounding like a broad resource-guide opener

### 2. Quick Answer Lead

Current:

```html
<p class="qa-lede"><strong>Best way to get resources fast in Last Z:</strong> send full marches before downtime, clear daily tasks and bounty rewards, avoid overbuilding production buildings, save chests for bulk openings, and add farms only after regular shortages appear.</p>
```

Proposed:

```html
<p class="qa-lede"><strong>Best way to get resources fast in Last Z:</strong> run full gathering marches during downtime, clear daily tasks and bounties, keep production buildings at requirement levels, save chests for bulk openings, and treat steel and farm accounts as later bottleneck tools.</p>
```

Reason:

- replaces "avoid overbuilding" with a clearer operational rule
- keeps steel and farm accounts from looking like generic beginner advice

### 3. Add A Decision Table After The Resource Overview Table

Proposed insertion after the first resource table:

```html
<table class="data-table">
    <thead>
        <tr>
            <th>If you need...</th>
            <th>Use this source first</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Food, wood, or electricity for daily upgrades</td>
            <td>Full gathering marches, daily tasks, bounty rewards, and trucks</td>
        </tr>
        <tr>
            <td>Steel for HQ or late systems</td>
            <td>Tyrant rallies first, then steel nodes and events</td>
        </tr>
        <tr>
            <td>Diamonds</td>
            <td>Saved chests, events, arena, achievements, and redeem codes</td>
        </tr>
        <tr>
            <td>Long-term extra income</td>
            <td>Farm account after regular shortages appear</td>
        </tr>
        <tr>
            <td>Raid safety</td>
            <td>Warehouse limit, spending before logout, and shields when exposed</td>
        </tr>
    </tbody>
</table>
```

Reason:

- adds a concrete player-stage decision signal
- improves answer-engine extraction without changing the page template
- makes the broad resource page more useful than a list of resource names

### 4. Daily Resource Sources Opener

Current:

```html
<p>Do not depend on one source. Stack gathering, daily tasks, bounties, trucks, events, and alliance activity so a missed node or bad chest day does not stop progression. For the routine, use the <a href="daily.html">Daily Checklist</a> and <a href="events.html">Events Schedule</a>.</p>
```

Proposed:

```html
<p>Treat resources as a routine, not a jackpot. Gathering covers baseline needs; tasks, bounties, trucks, events, and alliance activity fill the gaps. For the daily loop, use the <a href="daily.html">Daily Checklist</a> and <a href="events.html">Events Schedule</a>.</p>
```

Reason:

- keeps both internal links
- reduces generic "stack everything" phrasing
- reinforces the operational resource-flow model

### 5. Chest / Diamond Opener

Current:

```html
<p>Chests are a major source of diamonds, fragments, and rare items. Save them and open in bulk for better chances at rare drops.</p>
```

Proposed:

```html
<p>Use chest saving as a bonus diamond strategy, not a daily income plan. Bulk opening does not change the odds per chest, but it gives more chances at rare drops and makes jackpot results easier to notice.</p>
```

Reason:

- removes possible misunderstanding that bulk opening changes individual odds
- keeps the practical recommendation to save chests
- sounds more human and less generic

### 6. Diamond Section Opener

Current:

```html
<p>Diamonds are Diamonds. F2P can accumulate 20k+ diamonds from chest opening alone.</p>
```

Proposed:

```html
<p>Diamonds are reserve currency, not just another resource. Saved chests can create big spikes, but regular diamond income still comes from tasks, achievements, events, arena, and codes.</p>
```

Reason:

- removes awkward phrasing
- aligns with the site-wide diamond reserve rule
- avoids implying that every F2P player should expect 20k+ diamonds from chests

### 7. Chest Opening Strategy Bullets

Current:

```html
<li><strong>Save chests</strong> — don't open daily, accumulate for bulk opening</li>
<li><strong>Open in bulk</strong> — better psychological feel, same odds but more chances</li>
<li><strong>Bounty chests:</strong> ~90% are resource boxes, 10% have good rewards</li>
<li><strong>Realistic expectations:</strong> 10k diamonds from 1,000+ chests is lucky</li>
```

Proposed:

```html
<li><strong>Save chests</strong> — avoid daily trickle opening if you are building a larger reserve</li>
<li><strong>Open in bulk</strong> — same odds per chest, but more total chances at rare drops</li>
<li><strong>Bounty chests:</strong> most results are resource boxes; diamond drops are the exception</li>
<li><strong>Realistic expectations:</strong> 10k diamonds from 1,000+ chests is lucky, not normal</li>
```

Reason:

- tightens player expectations
- avoids presenting chest jackpots as normal income

### 8. Diamond Spend Bullets

Current:

```html
<li><strong>DO:</strong> Save for <a href="lucky-discounter.html">Lucky Discounter</a> (90% off) and <a href="gacha-go.html">Gacha Go</a> events</li>
<li><strong>DO:</strong> Buy VIP shop items (wrenches, badges)</li>
<li><strong>DON'T:</strong> Speed up random timers</li>
<li><strong>DON'T:</strong> Buy random chests (earn them instead)</li>
```

Proposed:

```html
<li><strong>Do:</strong> keep a reserve for <a href="lucky-discounter.html">Lucky Discounter</a>, <a href="gacha-go.html">Gacha Go</a>, and other high-value event windows</li>
<li><strong>Do:</strong> consider VIP shop items when the account needs wrenches, badges, or other bottleneck materials</li>
<li><strong>Do not:</strong> speed up random timers just because diamonds are available</li>
<li><strong>Do not:</strong> buy random chests when the same chest type can be earned through routine play</li>
```

Reason:

- keeps recommendations but makes them less absolute
- aligns with reserve-first diamond guidance

### 9. Farm Account Opener

Current:

```html
<p>Farm accounts are not an early-game requirement for most players. They become useful when your main account starts hitting regular resource shortages and you need extra long-term gathering support on the same server. For the full setup process, use the <a href="farm-account.html">Farm Account Guide</a>.</p>
```

Proposed:

```html
<p>Do not start a farm account just because you are new. Add one when your main account repeatedly runs out of food, wood, or electricity even after full marches and daily tasks. For setup, use the <a href="farm-account.html">Farm Account Guide</a>.</p>
```

Reason:

- preserves the existing link
- gives a clearer trigger for farm-account timing
- prevents new players from treating farms as mandatory setup work

### 10. Farm Account Definition Bullets

Current:

```html
<li>Secondary account focused only on gathering</li>
<li>Transfers resources to your main account</li>
<li>Essential for F2P players in late game</li>
```

Proposed:

```html
<li>Secondary account focused mostly on gathering and resource support</li>
<li>Feeds extra resources toward your main account through alliance systems</li>
<li>Useful for F2P late-game shortages, but not mandatory for every player</li>
```

Reason:

- softens an overclaim
- stays consistent with the earlier "not early-game requirement" guidance

### 11. Farm Account Tips

Current:

```html
<li>Keep HQ low — no need to upgrade past gathering unlocks</li>
<li>Max gathering research</li>
<li>Build multiple farms if needed (1-2 is enough)</li>
<li>Don't invest in combat — only gathering</li>
```

Proposed:

```html
<li>Keep HQ only as high as needed for gathering and transfer utility</li>
<li>Prioritize gathering research and march capacity</li>
<li>Start with one farm before adding more account upkeep</li>
<li>Avoid combat investment unless it directly protects the farm's resource role</li>
```

Reason:

- removes conflicting "multiple farms" / "1-2 is enough" phrasing
- makes the advice easier to follow

### 12. FAQ: More Resources Fast

Current visible FAQ and JSON-LD answer:

```html
Use full marches for world gathering, complete daily tasks and bounty missions, run trucks, save chests for bulk openings, and add farm accounts later if your main account starts falling behind on resources.
```

Proposed visible FAQ and JSON-LD answer:

```html
Use full gathering marches, daily tasks, bounties, trucks, and events first. Save chests for bulk openings, and add farm accounts only after your main account has regular shortages.
```

Reason:

- shorter, more answer-friendly
- aligns with the farm-account timing rule

### 13. FAQ: Open Chests Daily Or Save Them

Current visible FAQ:

```html
Save chests and open in bulk. Bounty mission chests give 90% resource boxes anyway. Saving thousands and opening at once gives more chances at rare drops (5k diamonds, 10k diamonds, fragments). One bulk opening can yield 20k+ diamonds.
```

Current JSON-LD answer:

```html
Save chests and open in bulk. Bounty mission chests give 90% resource boxes. Saving thousands and opening at once gives more chances at rare drops like 5k or 10k diamonds. One bulk opening of 10k chests can yield 20k+ diamonds.
```

Proposed visible FAQ and JSON-LD answer:

```html
Usually save them. Bulk opening does not improve the odds per chest, but it gives more total chances at rare drops. Treat jackpot diamonds as a bonus, not guaranteed income.
```

Reason:

- removes overconfidence around jackpot outcomes
- keeps the useful player action
- fixes visible/schema wording drift

### 14. FAQ: Free Diamonds

Current visible FAQ:

```html
Save bounty mission chests (can give 5k each), daily tasks, achievements, events, arena rankings, and redeem codes. Bulk opening 10k chests can yield 20k+ diamonds. Save diamonds for Lucky Discounter and Gacha Go events.
```

Current JSON-LD answer:

```html
Save bounty mission chests for weeks, then open thousands at once - can yield 20k+ diamonds including 5k and 10k jackpots. Also: daily tasks, achievements, events, arena rankings, and redeem codes.
```

Proposed visible FAQ and JSON-LD answer:

```html
Use daily tasks, achievements, events, arena rankings, redeem codes, and saved chest openings. Keep diamonds reserve-first before spending them on Lucky Discounter, Gacha Go, or other high-value event windows.
```

Reason:

- removes jackpot-heavy framing
- aligns with the Diamond Reserve Guide
- keeps all normal diamond sources

## Expected Effect

Expected improvements:

- lower `content-voice` risk for `resources.html`
- clearer player decisions for resource bottlenecks
- less AI-ish generic guide language
- fewer overclaims about chest jackpot outcomes
- better FAQ/schema synchronization

Expected risk:

- low content risk if applied exactly
- no template risk
- no cluster role change
- no sitemap/indexing change beyond modified page content and timestamp if the normal prepublish fix updates metadata

## Approval Needed

If approved, apply these exact text changes to `resources.html`, then run:

```bash
python3 scripts/prepublish_check.py --fix
python3 scripts/prepublish_check.py
python3 automation/pipeline.py checks
python3 automation/pipeline.py checks --strict
python3 automation/pipeline.py content-voice --top 12
```

