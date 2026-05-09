# HQ Content Cleanup Proposal

Generated: 2026-05-06

## Scope

Target: `hq.html`

This is a proposal only. No public HTML has been changed.

Goal:

- keep `hq.html` as the canonical HQ upgrade strategy page
- preserve the existing template, navigation, schema family, and cluster role
- fix misleading or inconsistent public copy before any LLM-assisted content work continues
- keep the change narrow; no rewrite

Approval required before applying.

## Research Update: Tyrant and Steel

Updated: 2026-05-09

Owner in-game check: Tyrant does not award Steel.

External cross-check:

- `last-z.wiki/events/the-tyrant/` lists Tyrant rewards as Enhancement Alloy, speedups, Hero Exp, Zent, Food, Wood, Electricity, Gift Vouchers, and related reward tiers; it does not list Steel in the visible Tyrant reward tables.
- `ztools.co.uk/bcem` describes Tyrant as a Power Cores and decoration shop voucher event.
- `lastz.info/the-tyrant-basics/` explains Tyrant execution, timing, offline engagement, and rally behavior, but does not identify Tyrant as a Steel source.
- Some SEO/commercial pages do claim Tyrant produces Steel, but they conflict with the more specific reward references above and with the owner in-game check.

Proposal impact:

- Do not add Tyrant as a Steel source in `hq.html`.
- Keep Tyrant guidance separate as an alliance event / Power Core progression topic unless future in-game evidence proves Steel was added to Tyrant rewards on a specific server stage.
- Treat current site pages that call Tyrant a Steel source as follow-up correction candidates.

## Proposed Changes

### 1. Fix corrupted early-phase bullet

Current:

```html
<li>Clubely costs anything</li>
```

Proposed:

```html
<li>Costs stay low compared with later HQ checkpoints</li>
```

Reason:

- The current sentence is visibly broken.
- The replacement keeps the same early-phase meaning without adding an unsupported number.

### 2. Normalize building terminology

Current:

```html
<li>Assault Camp</li>
```

Proposed:

```html
<li>Assaulter Camp</li>
```

Reason:

- `hq-construction-cost.html`, `early-game-optimization.html`, and `base-building-order.html` use `Assaulter Camp`.
- This keeps entity naming consistent.

### 3. Clarify HQ8-30 vs HQ31-35 requirements

Current:

```html
<p>These move in a predictable pattern all the way to HQ35. Keep them on your upgrade radar.</p>
```

Proposed:

```html
<p>From HQ8 to HQ30, this Lab + rotating prerequisite pattern is the core rule. For HQ31-35, check the <a href="hq-construction-cost.html">HQ Construction Cost Table</a> because later requirements and steel costs should be planned level by level.</p>
```

Current FAQ answer:

```html
<p>From HQ8 to HQ30, Laboratory is mandatory. Other key requirements rotate through buildings like City Walls, Alliance Center, and troop camps. The same pattern continues later, so the efficient rule is to upgrade only what the next HQ level demands.</p>
```

Proposed FAQ answer:

```html
<p>From HQ8 to HQ30, Laboratory is mandatory and the second prerequisite rotates through buildings like City Walls, Alliance Center, Assaulter Camp, Shooter Camp, and Rider Camp. For HQ31-35, use the <a href="hq-construction-cost.html">HQ Construction Cost Table</a> because steel and later prerequisites should be planned level by level.</p>
```

Matching JSON-LD FAQ answer should use the same text without HTML link markup:

```json
"From HQ8 to HQ30, Laboratory is mandatory and the second prerequisite rotates through buildings like City Walls, Alliance Center, Assaulter Camp, Shooter Camp, and Rider Camp. For HQ31-35, use the HQ Construction Cost Table because steel and later prerequisites should be planned level by level."
```

Reason:

- The cost table shows HQ31-35 differently from the HQ8-30 Lab + second-building pattern.
- This reduces risk of misleading players about late requirements.

### 4. Correct steel source priority without adding Tyrant

Current steel source list:

```html
<ul>
    <li>Build a <strong>Steel Mine</strong> in your town</li>
    <li>Earn from <strong>Bounties</strong></li>
    <li>Get from <strong><a href="furylord.html">Furylord</a></strong></li>
    <li>Buy in <strong>Hub Shop</strong></li>
    <li>Season 4 events</li>
    <li><strong>Best method:</strong> Orange Bounties (very large amounts)</li>
</ul>
```

Proposed steel source list:

```html
<ul>
    <li><strong>Orange Bounties</strong> — high steel per bounty in late game</li>
    <li><strong>Steel Mine and steel nodes</strong> — steady daily income once unlocked</li>
    <li><strong>Hub Shop and seasonal rewards</strong> — useful supporting sources</li>
    <li><strong><a href="furylord.html">Furylord</a></strong> — event source when active</li>
    <li><strong>HQ31-35 launch event</strong> — temporary steel boost when available on your server</li>
</ul>
```

Current section heading and text:

```html
<h3>Steel Is NOT the Problem</h3>
<p>Steel is easy to collect with orange bounties. Resources are manageable with the new vault system (hundreds of millions per week possible).</p>
<p><strong>The real bottleneck:</strong> Speedups. Those will stop you, not steel or resources.</p>
```

Proposed section heading and text:

```html
<h3>Steel Is Only One Bottleneck</h3>
<p>Steel adds pressure after HQ30, but it is not the only HQ31-35 blocker. Orange bounties, the Steel Mine, steel nodes, the Hub Shop, Furylord, and server events build your steel supply over time.</p>
<p><strong>The other bottleneck:</strong> speedups. Long construction timers can stop progress even when your steel plan is on track.</p>
```

Current key tip:

```html
<li><strong>Steel from orange bounties</strong> — best source by far</li>
```

Proposed key tip:

```html
<li><strong>Orange bounties and steel nodes</strong> — keep repeatable steel sources active</li>
```

Current FAQ answer:

```html
<p>Steel only appears after HQ30. Best sources: <a href="tyrant.html">Tyrant rallies</a> (main source), orange bounties (most steel per bounty), steel mine, Fury Lord, hub shop, Season 4 events. A special event after HQ31-35 update gives huge steel.</p>
```

Proposed FAQ answer:

```html
<p>Steel only appears after HQ30 once HQ31-35 is active on your server. Best sources are orange bounties, Steel Mine or steel nodes, Hub Shop, Furylord, seasonal rewards, and any active HQ31-35 launch event. Do not count Tyrant as a steel source unless your live reward screen shows steel.</p>
```

Matching JSON-LD FAQ answer should use the same text without HTML link markup:

```json
"Steel only appears after HQ30 once HQ31-35 is active on your server. Best sources are orange bounties, Steel Mine or steel nodes, Hub Shop, Furylord, seasonal rewards, and any active HQ31-35 launch event. Do not count Tyrant as a steel source unless your live reward screen shows steel."
```

Reason:

- Owner in-game check says Tyrant does not award Steel.
- More specific external Tyrant reward references list Power Core / voucher / resource-style rewards, not Steel.
- `hq.html` should avoid repeating unsupported Tyrant-to-Steel claims. `steel.html`, `tyrant.html`, `resources.html`, and `gear.html` should be handled as follow-up correction candidates before any site-wide Steel update is applied.

### 5. Soften unconfirmed T11 claims

Current quick-answer detail:

```html
<span class="qa-detail">hero cap 175, prepares for T11</span>
```

Proposed:

```html
<span class="qa-detail">hero cap 175 on older servers</span>
```

Current section:

```html
<h3>Future Content: T11 Units</h3>
<p>T11 units are likely coming. When they arrive, only HQ35 players will be ready. Upgrade now to prepare for what's next.</p>
```

Proposed:

```html
<h3>Future-Proofing Note</h3>
<p>HQ35 is useful future-proofing on older servers because it raises hero cap to 175 and leaves your account better positioned for later server unlocks. Do not rush HQ35 only because of unconfirmed unit timing.</p>
```

Current FAQ answer:

```html
<p>Yes, 100%. Each level unlocks +5 hero levels = massive free power. HQ35 heroes reach level 175. Also prepares you for T11 units which will require HQ35.</p>
```

Proposed FAQ answer:

```html
<p>For long-term accounts, usually yes: each HQ level raises hero level cap by +5, and HQ35 reaches hero cap 175 on older servers. Do not rush past HQ30 only because of unconfirmed unit timing; make the push when your resources, steel, and speedups can support it.</p>
```

Matching JSON-LD FAQ answer should use the same text:

```json
"For long-term accounts, usually yes: each HQ level raises hero level cap by +5, and HQ35 reaches hero cap 175 on older servers. Do not rush past HQ30 only because of unconfirmed unit timing; make the push when your resources, steel, and speedups can support it."
```

Current key tip:

```html
<li><strong>Prepare for T11</strong> — will require HQ35</li>
```

Proposed:

```html
<li><strong>Treat HQ35 as future-proofing</strong> — valuable for hero cap and later server unlocks</li>
```

Reason:

- Current T11 wording is stronger than the verified page evidence.
- The proposed wording keeps the long-term planning value without publishing an unsupported requirement claim.

### 6. Make HQ31-35 timer wording less absolute

Current:

```html
<p><strong>Reality check:</strong> Some upgrades take <strong>over 6 months</strong> without bonuses. "You could grow a small real-life garden in that time."</p>
```

Proposed:

```html
<p><strong>Reality check:</strong> the longest unbuffed HQ31-35 timers can run for several months. Use every construction bonus you can before committing to these levels.</p>
```

Current FAQ answer:

```html
<p>Without bonuses, some final upgrades take 6+ months EACH. With full construction speed setup (villa, refugees, Sophia, alliance buffs), it's much faster. Speedups are the main bottleneck.</p>
```

Proposed FAQ answer:

```html
<p>Without bonuses, the longest HQ31-35 timers can run for several months. With a full construction speed setup such as villa, refugees, Sophia, and alliance buffs, they become much faster. Speedups remain the main bottleneck.</p>
```

Matching JSON-LD FAQ answer should use the same text:

```json
"Without bonuses, the longest HQ31-35 timers can run for several months. With a full construction speed setup such as villa, refugees, Sophia, and alliance buffs, they become much faster. Speedups remain the main bottleneck."
```

Reason:

- The cost table supports very long timers, but the current FAQ wording reads broader and more absolute than needed.

### 7. Soften the strongest Sophia wording without weakening the recommendation

Current quick-answer title:

```html
<strong class="qa-title">Sophia to 5 stars first</strong>
```

Proposed:

```html
<strong class="qa-title">Build Sophia early</strong>
```

Current section:

```html
<p><strong>"If you reach HQ30 without Sophia at 5 stars, something went wrong."</strong></p>
<p>Her bonus applies to EVERY building. Since you upgrade tons of buildings to reach HQ35, Sophia saves resources at every step. Push her to 5 stars as early as possible.</p>
```

Proposed:

```html
<p><strong>Try to have Sophia at 5 stars before the expensive HQ30+ push.</strong></p>
<p>Her bonus applies to every building. Since the HQ path forces many prerequisite upgrades, Sophia saves resources at every step. Build her early if you are committed to long-term HQ progression.</p>
```

Current key tip:

```html
<li><strong>Sophia first</strong> — 5 stars as early as possible, saves billions</li>
```

Proposed:

```html
<li><strong>Sophia early</strong> — 5 stars before the expensive HQ30+ push saves major resources</li>
```

Reason:

- Sophia remains a strong recommendation.
- The new wording avoids sounding like a hard failure state for every player/account path.

## Acceptance Checks If Approved

After applying, run:

```bash
python3 scripts/prepublish_check.py --fix
python3 scripts/prepublish_check.py
python3 automation/pipeline.py checks --strict
```

Manual review:

- confirm visible FAQ and JSON-LD FAQ answers match
- confirm no template/schema family drift
- confirm `hq.html` still links to `hq-construction-cost.html` and `steel.html`
- confirm no new `hq.html` text describes Tyrant as a Steel source

## Approval Gate

Do not apply this proposal until the owner explicitly approves the exact proposed text.
