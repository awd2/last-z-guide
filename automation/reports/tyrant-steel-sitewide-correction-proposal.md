# Tyrant / Steel Sitewide Correction Proposal

Generated: 2026-05-10

## Scope

Target files:

- `steel.html`
- `tyrant.html`
- `resources.html`
- `gear.html`
- `pvp.html`
- `index.html`

This is a proposal only. No public HTML has been changed.

Goal:

- remove unsupported claims that Tyrant is a Steel source
- preserve existing page templates, navigation, schema families, and cluster roles
- keep Tyrant positioned as an alliance rally / Power Core / reward coordination event
- keep Steel positioned as a late-game HQ31-35 resource from bounties, Steel Mine/nodes, Hub Shop, Furylord, seasonal rewards, and launch-event rewards
- avoid overcorrecting into a broad rewrite

Approval required before applying.

## Research Basis

Owner in-game check: Tyrant does not award Steel.

External cross-check:

- `last-z.wiki/events/the-tyrant/` lists Tyrant rewards as Enhancement Alloy, speedups, Hero Exp, Zent, Food, Wood, Electricity, Gift Vouchers, Diamonds, Power Cores, and related reward tiers; it does not list Steel in the visible Tyrant reward tables.
- `ztools.co.uk/wiki/` positions Tyrant as a server wiki event page and broader event/reward topic, not as the canonical Steel source.
- `lastz.info/the-tyrant-basics/` explains Tyrant execution, timing, offline engagement, and rally behavior, but does not identify Tyrant as a Steel source.
- Some SEO/commercial pages claim Tyrant produces Steel, but those claims conflict with the owner in-game check and with more specific Tyrant reward references.

Correction rule:

- Do not describe Tyrant as a Steel source unless the page explicitly says to verify a live reward screen first.
- Prefer: Tyrant gives alliance/personal rewards and can provide Power Cores / gear-related materials depending reward tier.
- For Steel source guidance, prefer: orange bounties, Steel Mine, steel nodes, Hub Shop, Furylord, seasonal rewards, and active HQ31-35 launch events.

## Proposed Changes

### 1. `steel.html`

Purpose: keep this as the canonical Steel guide, but remove Tyrant from the page's Steel-source promise.

#### Head metadata

Current:

```html
<title>Last Z Steel Guide (2026) — How to Get Steel, Tyrant, HQ31-35</title>
<meta name="description" content="How to get steel in Last Z: when steel unlocks, why Tyrant is the best source, how steel nodes work, and where steel matters for HQ31-35 and Steel Age research.">
<meta name="keywords" content="Last Z steel, Last Z steel guide, Last Z steel farming, Last Z Tyrant steel, Last Z steel mine, Last Z steel nodes, Last Z Steel Age, Last Z HQ 31, Last Z HQ 35">
```

Proposed:

```html
<title>Last Z Steel Guide (2026) — How to Get Steel, HQ31-35, Steel Nodes</title>
<meta name="description" content="How to get steel in Last Z: when steel unlocks, orange bounties, Steel Mine, steel nodes, Hub Shop, Furylord, events, HQ31-35, and Steel Age priorities.">
<meta name="keywords" content="Last Z steel, Last Z steel guide, Last Z steel farming, Last Z orange bounties steel, Last Z steel mine, Last Z steel nodes, Last Z Steel Age, Last Z HQ 31, Last Z HQ 35">
```

Current:

```html
<meta property="og:title" content="Last Z Steel Guide — How to Get Steel, Tyrant, HQ31-35">
<meta property="og:description" content="When steel unlocks, how to farm it, why Tyrant matters most, and where steel is used in HQ31-35 and late-game research.">
<meta name="twitter:title" content="Last Z Steel Guide — How to Get Steel, Tyrant, HQ31-35">
<meta name="twitter:description" content="When steel unlocks, how to farm it, why Tyrant matters most, and where steel is used in HQ31-35 and late-game research.">
```

Proposed:

```html
<meta property="og:title" content="Last Z Steel Guide — How to Get Steel, HQ31-35, Steel Nodes">
<meta property="og:description" content="When steel unlocks, how to farm it from bounties, Steel Mine, nodes, shops, and events, and where steel is used in HQ31-35 and late-game research.">
<meta name="twitter:title" content="Last Z Steel Guide — How to Get Steel, HQ31-35, Steel Nodes">
<meta name="twitter:description" content="When steel unlocks, how to farm it from bounties, Steel Mine, nodes, shops, and events, and where steel is used in HQ31-35 and late-game research.">
```

Current Article JSON-LD:

```json
"headline": "Last Z Steel Guide — How to Get Steel, Tyrant, HQ31-35",
"description": "Complete steel guide for Last Z covering unlock timing, Tyrant, farming sources, HQ31-35 progression, and late-game usage"
```

Proposed:

```json
"headline": "Last Z Steel Guide — How to Get Steel, HQ31-35, Steel Nodes",
"description": "Complete steel guide for Last Z covering unlock timing, bounties, Steel Mine, steel nodes, shops, events, HQ31-35 progression, and late-game usage"
```

#### FAQ JSON-LD

Current:

```json
"text": "Tyrant rallies are the main weekly source. Always enable Engage Offline if you cannot join live and focus on full alliance rallies for better rewards."
```

Proposed:

```json
"text": "For most players, practical steel sources are orange bounties, Steel Mine or steel nodes, Hub Shop, Furylord, seasonal rewards, and any active HQ31-35 launch event. Do not count Tyrant as a steel source unless your live reward screen shows steel."
```

#### Visible header and quick answer

Current:

```html
<h1>Last Z Steel Guide — How to Get Steel, Tyrant, and HQ31-35</h1>
<p class="guide-verified">Best steel strategy for most players: unlock HQ31-35 first, treat Tyrant as your main weekly steel source, gather steel nodes consistently, and do not confuse Steel Factory with actual steel resource.</p>
```

Proposed:

```html
<h1>Last Z Steel Guide — How to Get Steel, Steel Nodes, and HQ31-35</h1>
<p class="guide-verified">Best steel strategy for most players: unlock HQ31-35 first, use orange bounties, Steel Mine, steel nodes, Hub Shop, Furylord, and events for steel income, and do not confuse Steel Factory with actual steel resource.</p>
```

Current:

```html
<p class="qa-lede"><strong>Best way to get steel in Last Z:</strong> unlock the HQ31-35 stage, prioritize Tyrant rallies first, collect orange bounties and steel nodes, and save most steel for HQ31-35 before spreading it into Steel Age research.</p>
```

Proposed:

```html
<p class="qa-lede"><strong>Best way to get steel in Last Z:</strong> unlock the HQ31-35 stage, prioritize orange bounties, Steel Mine, steel nodes, Hub Shop, Furylord, and active steel events, then save most steel for HQ31-35 before spreading it into Steel Age research.</p>
```

Current:

```html
<strong class="qa-title">Tyrant is #1 source</strong>
<span class="qa-detail">enable Engage Offline if busy</span>
```

Proposed:

```html
<strong class="qa-title">Use repeatable sources</strong>
<span class="qa-detail">bounties, mine, nodes, shops</span>
```

Current:

```html
<span class="qa-callout-text"><strong>Core rule:</strong> Tyrant is the main steel engine for most accounts, so missing it regularly is the fastest way to fall behind on HQ31-35 progression.</span>
```

Proposed:

```html
<span class="qa-callout-text"><strong>Core rule:</strong> do not plan HQ31-35 around Tyrant unless your live reward screen shows steel. Build steel from bounties, Steel Mine, nodes, shops, Furylord, and events.</span>
```

#### Steel source section

Current:

```html
<p>Not all steel sources are equal. Tyrant is the main weekly source for most accounts, while bounties, steel nodes, and other smaller sources help smooth daily progress between Tyrant cycles.</p>
<ol>
    <li><strong>Tyrant rallies</strong> — the main weekly source of steel. Don’t miss them. See the full <a href="tyrant.html">Tyrant Rally Guide</a>.</li>
    <li><strong>Orange bounty missions</strong> — best steel per bounty in late game.</li>
    <li><strong>Steel Mine in your town</strong> — a steady daily trickle.</li>
    <li><strong>Events &amp; rewards</strong> — seasonal events and special updates often boost steel income.</li>
    <li><strong>Steel nodes on the world map</strong> — a safe way to add extra steel each day.</li>
</ol>
```

Proposed:

```html
<p>Not all steel sources are equal. Orange bounties and server-stage events can give large bursts, while Steel Mine, steel nodes, Hub Shop, Furylord, and recurring rewards help smooth daily progress.</p>
<ol>
    <li><strong>Orange bounty missions</strong> — high steel per bounty in late game.</li>
    <li><strong>Steel Mine and steel nodes</strong> — steady daily income once unlocked.</li>
    <li><strong>Hub Shop and seasonal rewards</strong> — useful supporting sources.</li>
    <li><strong><a href="furylord.html">Furylord</a></strong> — event source when active.</li>
    <li><strong>HQ31-35 launch event</strong> — temporary steel boost when available on your server.</li>
</ol>
```

#### Tyrant section rewrite

Current:

```html
<h2>Tyrant: The Steel Engine</h2>
<p>If you only optimize one steel source, optimize Tyrant. For most players it is the single biggest repeatable steel injection in the game, which is why missing Tyrant regularly slows HQ31-35 progression so hard.</p>
<p>Tyrant events run frequently and are the single biggest steel injection for most alliances. If you can’t join live, enable <strong>Engage Offline</strong> in the Event Center to auto-join rallies while you’re away.</p>
<ul>
    <li>Tyrant runs on a short schedule window and rewards scale with alliance damage.</li>
    <li>Alliance leaders (R4/R5) can set the start time for the event.</li>
    <li>Because it repeats often, missing Tyrant is the fastest way to fall behind on steel.</li>
</ul>
<p>See the full <a href="tyrant.html">Tyrant Rally Guide</a> for the 7-8 member rally strategy that maximizes rewards.</p>
```

Proposed:

```html
<h2>Do Not Confuse Tyrant Rewards With Steel</h2>
<p>Tyrant is still worth doing, but it should not be treated as your steel plan unless your live reward screen shows steel. Use Tyrant for alliance rewards, damage-based rewards, and Power Core progression instead.</p>
<p>If you can’t join live, enable <strong>Engage Offline</strong> in the Event Center so your troops can auto-join rallies while you’re away.</p>
<ul>
    <li>Tyrant runs on a short schedule window and rewards scale with alliance damage.</li>
    <li>Alliance leaders (R4/R5) can set the start time for the event.</li>
    <li>Check the live reward screen before counting any event as a steel source.</li>
</ul>
<p>See the full <a href="tyrant.html">Tyrant Rally Guide</a> for the 7-8 member rally strategy that maximizes rewards.</p>
```

#### Common mistakes and visible FAQ

Current:

```html
<li><strong>Skipping Tyrant</strong> — steel income drops sharply without it.</li>
```

Proposed:

```html
<li><strong>Counting Tyrant as guaranteed steel</strong> — check the live reward screen before planning HQ31-35 steel around it.</li>
```

Current:

```html
<p>Tyrant rallies are the main source. Even if you can’t join live, enable Engage Offline to auto-join and secure rewards.</p>
```

Proposed:

```html
<p>For most players, practical steel sources are orange bounties, Steel Mine or steel nodes, Hub Shop, Furylord, seasonal rewards, and any active HQ31-35 launch event. Do not count Tyrant as a steel source unless your live reward screen shows steel.</p>
```

### 2. `tyrant.html`

Purpose: keep this as the Tyrant execution guide, but stop promising Steel rewards.

#### Head metadata

Current:

```html
<title>Last Z Tyrant Rally Guide (2026) — Best Rally Size, Max Damage, Steel Rewards</title>
<meta name="description" content="Best Tyrant rally strategy in Last Z: ideal rally size, max damage setup, Engage Offline, steel rewards, and the key mistakes that lower alliance results.">
<meta name="keywords" content="Last Z Tyrant, Last Z Tyrant rally, Last Z Tyrant strategy, Last Z Tyrant rewards, Last Z steel, Last Z rally guide, Last Z alliance event, Last Z engage offline">
```

Proposed:

```html
<title>Last Z Tyrant Rally Guide (2026) — Best Rally Size, Max Damage, Power Cores</title>
<meta name="description" content="Best Tyrant rally strategy in Last Z: ideal rally size, max damage setup, Engage Offline, Power Core rewards, and the key mistakes that lower alliance results.">
<meta name="keywords" content="Last Z Tyrant, Last Z Tyrant rally, Last Z Tyrant strategy, Last Z Tyrant rewards, Last Z Power Cores, Last Z rally guide, Last Z alliance event, Last Z engage offline">
```

Current:

```html
<meta property="og:title" content="Last Z Tyrant Rally Guide — Best Rally Size, Max Damage, Steel Rewards">
<meta property="og:description" content="How to maximize Tyrant damage, why 7-8 member rallies matter, and how Tyrant supports steel progression.">
<meta name="twitter:title" content="Last Z Tyrant Rally Guide — Best Rally Size, Max Damage, Steel Rewards">
<meta name="twitter:description" content="How to maximize Tyrant damage, why 7-8 member rallies matter, and how Tyrant supports steel progression.">
```

Proposed:

```html
<meta property="og:title" content="Last Z Tyrant Rally Guide — Best Rally Size, Max Damage, Power Cores">
<meta property="og:description" content="How to maximize Tyrant damage, why 7-8 member rallies matter, and how Tyrant supports alliance rewards and Power Core progression.">
<meta name="twitter:title" content="Last Z Tyrant Rally Guide — Best Rally Size, Max Damage, Power Cores">
<meta name="twitter:description" content="How to maximize Tyrant damage, why 7-8 member rallies matter, and how Tyrant supports alliance rewards and Power Core progression.">
```

Current Article JSON-LD:

```json
"headline": "Last Z Tyrant Rally Guide — Best Rally Size, Max Damage, and Steel Rewards",
"description": "Complete Tyrant rally guide for Last Z with 7-8 member strategy, Engage Offline, steel rewards, and max damage tips"
```

Proposed:

```json
"headline": "Last Z Tyrant Rally Guide — Best Rally Size, Max Damage, and Power Cores",
"description": "Complete Tyrant rally guide for Last Z with 7-8 member strategy, Engage Offline, alliance rewards, Power Cores, and max damage tips"
```

#### FAQ JSON-LD

Current:

```json
"name": "How do I get Steel from Tyrant?",
"text": "Participate in every Tyrant event with full power. Enable \"Engage offline\" if you can't join live. Steel rewards scale with your alliance's total damage — stronger coordination means more Steel for everyone."
```

Proposed:

```json
"name": "What rewards does Tyrant give?",
"text": "Tyrant rewards scale with alliance and personal damage. Reward tiers can include Power Cores, Enhancement Alloy, speedups, Hero EXP, normal resources, Gift Vouchers, and diamonds. Check the live reward screen before assuming Tyrant gives steel on your server."
```

#### Visible header and quick answer

Current:

```html
<h1>Last Z Tyrant Rally Guide — Best Rally Size, Max Damage, and Steel Rewards</h1>
<p class="guide-verified">Best Tyrant plan for most alliances: run only 7-8 member rallies, fill existing rallies first, recall troops before start, and use Engage Offline so you never miss one of the main steel events in the game.</p>
```

Proposed:

```html
<h1>Last Z Tyrant Rally Guide — Best Rally Size, Max Damage, and Power Cores</h1>
<p class="guide-verified">Best Tyrant plan for most alliances: run only 7-8 member rallies, fill existing rallies first, recall troops before start, and use Engage Offline so you do not miss damage-based alliance and personal rewards.</p>
```

Current:

```html
<p class="qa-lede"><strong>Best Tyrant rally strategy in Last Z:</strong> use only 7-8 member rallies, fill open rallies before making new ones, recall troops before start, and treat Tyrant as one of the main steel sources for HQ31-35 progression.</p>
```

Proposed:

```html
<p class="qa-lede"><strong>Best Tyrant rally strategy in Last Z:</strong> use only 7-8 member rallies, fill open rallies before making new ones, recall troops before start, and treat Tyrant as a damage-based alliance reward event, not your default steel plan.</p>
```

#### Main Tyrant value section

Current:

```html
<h2>Why Tyrant Matters for Steel and Progression</h2>
<h3>Main Source of Steel</h3>
<p>Tyrant is the primary way to farm <strong>Steel</strong> in Last Z. Steel is required for HQ upgrades from level 31 to 35. The more damage your alliance deals, the better rewards everyone receives. See our <a href="hq.html">HQ Upgrade Guide</a> for Steel requirements and the <a href="steel.html">Steel Guide</a> for all sources.</p>
```

Proposed:

```html
<h2>Why Tyrant Matters for Power Cores and Progression</h2>
<h3>Damage-Based Alliance Rewards</h3>
<p>Tyrant is a repeatable alliance reward event where rewards scale with alliance and personal damage. Use it for Power Cores, gear-related progression, and other damage-tier rewards, then use the <a href="steel.html">Steel Guide</a> separately for confirmed steel sources.</p>
```

Current:

```html
<p>Tyrant is too valuable to skip. Even if you can't join live, enable "Engage offline" to participate automatically. Steel is essential for late-game progression.</p>
```

Proposed:

```html
<p>Tyrant is too valuable to skip. Even if you can't join live, enable "Engage offline" to participate automatically and secure damage-based rewards.</p>
```

#### Visible FAQ

Current:

```html
<h3>How do I get Steel from Tyrant?</h3>
<p>Participate in every Tyrant event with full power. Enable "Engage offline" if you can't join live. Steel rewards scale with your alliance's total damage — stronger coordination means more Steel for everyone.</p>
```

Proposed:

```html
<h3>What rewards does Tyrant give?</h3>
<p>Tyrant rewards scale with alliance and personal damage. Reward tiers can include Power Cores, Enhancement Alloy, speedups, Hero EXP, normal resources, Gift Vouchers, and diamonds. Check the live reward screen before assuming Tyrant gives steel on your server.</p>
```

### 3. `resources.html`

Purpose: keep resources page broad, but correct all Steel-source routing.

Current JSON-LD FAQ:

```json
"text": "For most players, Tyrant rallies are the main steel source, followed by steel nodes, events, and other late-game reward systems. Steel should be treated as a separate bottleneck from food, wood, and electricity."
```

Proposed:

```json
"text": "For most players, practical steel sources are orange bounties, Steel Mine or steel nodes, Hub Shop, Furylord, seasonal rewards, and any active HQ31-35 launch event. Steel should be treated as a separate bottleneck from food, wood, and electricity."
```

Current quick-answer item:

```html
<strong class="qa-title">Steel from Tyrant</strong>
<span class="qa-detail">enable "Engage Offline"</span>
```

Proposed:

```html
<strong class="qa-title">Steel from bounties/nodes</strong>
<span class="qa-detail">plus mine, shops, events</span>
```

Current callout:

```html
<span class="qa-callout-text"><strong>Steel source:</strong> Tyrant rallies and steel nodes matter more than normal resource flow once HQ upgrades get expensive.</span>
```

Proposed:

```html
<span class="qa-callout-text"><strong>Steel source:</strong> orange bounties, Steel Mine, steel nodes, Hub Shop, Furylord, and seasonal events matter once HQ upgrades get expensive.</span>
```

Current table rows:

```html
<td>Tyrant, Steel nodes, events</td>
<td>Tyrant rallies first, then steel nodes and events</td>
<td><strong>Tyrant Rallies</strong></td>
<td>Steel (main source)</td>
```

Proposed:

```html
<td>Orange bounties, Steel nodes, events</td>
<td>Orange bounties first, then steel nodes, Steel Mine, shops, and events</td>
<td><strong>Tyrant Rallies</strong></td>
<td>Power Cores, alloy, vouchers, and damage-tier rewards</td>
```

Current steel section:

```html
<p>Plan steel separately from food, wood, and electricity. When HQ and late-game systems start asking for it, Tyrant rallies, steel nodes, and event rewards become the routine. See the dedicated <a href="steel.html">Steel Guide</a> for the full breakdown.</p>

<h3>1. <a href="tyrant.html">Tyrant Rallies</a> (Best Source)</h3>
<ul>
    <li>Join alliance Tyrant rallies daily</li>
    <li><strong>Enable "Engage Offline"</strong> — auto-join rallies when you're not playing</li>
    <li>Gives ~500+ Steel per week</li>
    <li>Also gives Power Cores and other materials</li>
</ul>
```

Proposed:

```html
<p>Plan steel separately from food, wood, and electricity. When HQ and late-game systems start asking for it, orange bounties, Steel Mine, steel nodes, shops, Furylord, and event rewards become the routine. See the dedicated <a href="steel.html">Steel Guide</a> for the full breakdown.</p>

<h3>1. Orange Bounty Missions</h3>
<ul>
    <li>Prioritize orange bounties once steel is active on your server</li>
    <li>Use refreshes carefully when you need steel for HQ31-35</li>
    <li>Confirm the reward preview before spending refresh items</li>
</ul>
```

Current:

```html
<h3>2. Steel Nodes on World Map</h3>
<ul>
    <li>Gather from Steel nodes (appear at higher levels)</li>
    <li>Lower yield than Tyrant but always available</li>
</ul>

<h3>3. Events & Tasks</h3>
```

Proposed:

```html
<h3>2. Steel Mine and Steel Nodes</h3>
<ul>
    <li>Gather from steel nodes once they appear at higher levels</li>
    <li>Use Steel Mine output as steady background income</li>
</ul>

<h3>3. Shops, Furylord, Events, and Tasks</h3>
```

Current:

```html
<p><strong>Critical tip:</strong> Always enable "Engage Offline" for Tyrant. You get Steel passively without being online.</p>
```

Proposed:

```html
<p><strong>Critical tip:</strong> check the live reward screen before counting any event as a steel source. Tyrant is still useful for alliance rewards and Power Cores, but do not plan steel around it unless the game shows steel.</p>
```

Visible FAQ should match the JSON-LD FAQ answer.

### 4. `gear.html`

Purpose: keep gear guide focused on Power Cores; remove the one Steel claim from the Power Core section.

Current:

```html
<p><strong>Tip:</strong> Enable "Engage Offline" for Tyrant rallies to get free Steel and Power Core materials without being online.</p>
```

Proposed:

```html
<p><strong>Tip:</strong> Enable "Engage Offline" for Tyrant rallies to get Power Core materials and other damage-tier rewards without being online.</p>
```

### 5. `pvp.html`

Purpose: keep boss-fight checklist useful without claiming Tyrant provides Steel.

Current:

```html
<li><strong>Tyrant:</strong> Enable "Engage Offline" for auto-join rallies, provides Steel</li>
```

Proposed:

```html
<li><strong>Tyrant:</strong> Enable "Engage Offline" for auto-join rallies and damage-tier rewards</li>
```

### 6. `index.html`

Purpose: keep home routing accurate.

Current:

```html
<p>Maximum damage strategy — 7-8 member rallies, Steel farming</p>
```

Proposed:

```html
<p>Maximum damage strategy — 7-8 member rallies, Power Core rewards</p>
```

Current:

```html
<p>How to get steel fast — Tyrant, nodes, HQ31-35, and Steel Age priorities</p>
```

Proposed:

```html
<p>How to get steel fast — bounties, nodes, HQ31-35, and Steel Age priorities</p>
```

## Acceptance Checks If Approved

After applying, run:

```bash
python3 scripts/prepublish_check.py --fix
python3 scripts/prepublish_check.py
python3 automation/pipeline.py checks --strict
```

Manual review:

- visible FAQ and JSON-LD FAQ answers match on `steel.html`, `tyrant.html`, and `resources.html`
- no page says Tyrant is a confirmed Steel source
- `tyrant.html` still links to `steel.html` only as separate Steel planning, not as Tyrant reward proof
- `steel.html` still preserves the Steel Factory vs Steel resource clarification
- home cards still route to `tyrant.html` and `steel.html` with distinct page roles

## Approval Gate

Do not apply this proposal until the owner explicitly approves the exact proposed text.
