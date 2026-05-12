# Exact Content Proposal: research.html

Run: `2026-05-12-research-gsc-opportunity-llm-approved-intake`
Target: `research.html`
Status: proposal-only

This proposal does not modify public content. It converts the existing summary-level proposal into exact before/after text for owner approval.

## Goal

Clarify that the core research route is:

- Hero Training to Cockpit
- Military Strategies
- Peace Shield / Urgent Rescue
- then choose by goal:
  - shortest practical UST/T10 path for tier progression
  - Siege to Seize into Field Research only for late-game Recharge Shield / deep combat scaling

This avoids implying that Field Research is required before UST/T10.

## Proposed Replacements

### 1. Title

Before:

```html
<title>Last Z Research Guide (2026) — Research Tree, Peace Shield, Urgent Rescue, T10 Order</title>
```

After:

```html
<title>Last Z Research Guide (2026) - Best Research Order, Peace Shield, UST/T10 Path</title>
```

### 2. Meta Description

Before:

```html
<meta name="description" content="Step-by-step Last Z research tree guide: what to research first, how to unlock Peace Shield and Urgent Rescue, and the best path toward T10.">
```

After:

```html
<meta name="description" content="Best Last Z research order for most players: Hero Training to Cockpit, Military Strategies, Peace Shield for Urgent Rescue, then choose UST/T10 or late Field Research by goal.">
```

### 3. Open Graph

Before:

```html
<meta property="og:title" content="Last Z Research Guide — Research Tree, Peace Shield, Urgent Rescue, T10 Order">
<meta property="og:description" content="What to research first in Last Z: research tree order, Peace Shield unlock path, Urgent Rescue priority, and the best route toward T10.">
```

After:

```html
<meta property="og:title" content="Last Z Research Guide - Best Research Order, Peace Shield, UST/T10 Path">
<meta property="og:description" content="What to research first in Last Z: start with Hero Training to Cockpit, Military Strategies, and Peace Shield, then choose UST/T10 or Field Research by account goal.">
```

### 4. Twitter Metadata

Before:

```html
<meta name="twitter:title" content="Last Z Research Guide — Research Tree, Peace Shield, Urgent Rescue, T10 Order">
<meta name="twitter:description" content="What to research first in Last Z: research tree order, Peace Shield unlock path, Urgent Rescue priority, and the best route toward T10.">
```

After:

```html
<meta name="twitter:title" content="Last Z Research Guide - Best Research Order, Peace Shield, UST/T10 Path">
<meta name="twitter:description" content="What to research first in Last Z: start with Hero Training to Cockpit, Military Strategies, and Peace Shield, then choose UST/T10 or Field Research by account goal.">
```

### 5. Article JSON-LD

Before:

```json
"headline": "Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path",
"description": "Step-by-step Last Z research tree guide covering what to research first, Peace Shield, Urgent Rescue, and the best path toward T10",
```

After:

```json
"headline": "Last Z Research Guide - Best Research Order, Peace Shield, and UST/T10 Path",
"description": "Step-by-step Last Z research guide covering Hero Training to Cockpit, Military Strategies, Peace Shield, Urgent Rescue, and when to choose UST/T10 or Field Research",
```

### 6. Modified Date Metadata

Before:

```html
<meta property="article:modified_time" content="2026-05-03">
```

```json
"dateModified": "2026-05-03"}
```

After:

```html
<meta property="article:modified_time" content="2026-05-12">
```

```json
"dateModified": "2026-05-12"}
```

### 7. HowTo JSON-LD Steps 4-5

Before:

```json
{
    "@type": "HowToStep",
    "position": 4,
    "name": "Siege to Seize",
    "text": "Research Siege to Seize for offensive bonuses. Warning: increases your Destruction Value."
},
{
    "@type": "HowToStep",
    "position": 5,
    "name": "UST (Unit Special Training)",
    "text": "Start UST for T10 units. Requires 1,488,100 badges total — long-term goal for most players."
}
```

After:

```json
{
    "@type": "HowToStep",
    "position": 4,
    "name": "Choose UST/T10 or Siege to Seize by account goal",
    "text": "After Peace Shield and Urgent Rescue, choose by goal. Use the shortest practical UST/T10 path for tier progression, or push Siege to Seize only if you want the later Field Research and Recharge Shield route."
},
{
    "@type": "HowToStep",
    "position": 5,
    "name": "UST (Unit Special Training)",
    "text": "Commit to UST for T10 units when your account can support the 1,488,100 badge path without starving higher-value intermediate research."
}
```

### 8. FAQ JSON-LD: Best Research Order

Before:

```json
"text": "For most players: Hero Training to Cockpit, Military Strategies for efficient troop stats, Peace Shield for Urgent Rescue, then the shortest practical path toward UST and T10."
```

After:

```json
"text": "For most players: Hero Training to Cockpit, Military Strategies for efficient troop stats, and Peace Shield for Urgent Rescue. After that, choose the shortest practical UST/T10 path for tier progression, or Siege to Seize into Field Research only if you want late Recharge Shield and deep combat scaling."
```

### 9. H1

Before:

```html
<h1>Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path</h1>
```

After:

```html
<h1>Last Z Research Guide - Best Research Order, Peace Shield, and UST/T10 Path</h1>
```

### 10. Guide Meta Date

Before:

```html
<p class="guide-meta">Research Guide &bull; Updated <time datetime="2026-02-01">February 1, 2026</time> &bull; 8 min read</p>
```

After:

```html
<p class="guide-meta">Research Guide &bull; Updated <time datetime="2026-05-12">May 12, 2026</time> &bull; 8 min read</p>
```

### 11. Guide Verified Summary

Before:

```html
<p class="guide-verified">Best Last Z research order for most players: Hero Training to Cockpit, Military Strategies for efficient combat stats, Peace Shield for Urgent Rescue, then the shortest practical path toward UST and T10.</p>
```

After:

```html
<p class="guide-verified">Best Last Z research order for most players: Hero Training to Cockpit, Military Strategies for efficient combat stats, Peace Shield for Urgent Rescue, then choose between the shortest practical UST/T10 path or late Field Research based on your account goal.</p>
```

### 12. Quick Answer Lede

Before:

```html
<p class="qa-lede"><strong>Best Last Z research order for most players:</strong> Hero Training to Cockpit, Military Strategies for efficient troop stats, Peace Shield for Urgent Rescue, then the shortest practical path toward UST and T10.</p>
```

After:

```html
<p class="qa-lede"><strong>Best Last Z research order for most players:</strong> Hero Training to Cockpit, Military Strategies for efficient troop stats, Peace Shield for Urgent Rescue, then choose the shortest practical UST/T10 path for tier progression or Siege to Seize into Field Research for late Recharge Shield scaling.</p>
```

### 13. Quick Answer Item 4

Before:

```html
<li class="qa-item">
    <span class="qa-num" aria-hidden="true">④</span>
    <span class="qa-line">
        <strong class="qa-title">Siege to Seize</strong>
        <span class="qa-sep">·</span>
        <span class="qa-detail">optional research tree</span>
    </span>
</li>
```

After:

```html
<li class="qa-item">
    <span class="qa-num" aria-hidden="true">④</span>
    <span class="qa-line">
        <strong class="qa-title">Choose next path</strong>
        <span class="qa-sep">·</span>
        <span class="qa-detail">UST/T10 for tier progression, or Siege to Seize for Field Research</span>
    </span>
</li>
```

### 14. Quick Answer Callout: Best Overall Order

Before:

```html
<span class="qa-callout-text"><strong>Best overall order:</strong> Hero Training to Cockpit → Military Strategies → Peace Shield</span>
```

After:

```html
<span class="qa-callout-text"><strong>Best overall order:</strong> Hero Training to Cockpit -> Military Strategies -> Peace Shield, then choose UST/T10 or Field Research by goal</span>
```

### 15. Main Opening Paragraph

Before:

```html
<p>If you are asking what to research first in Last Z, the best answer for most players is not "rush everything toward T10." The stronger route is to take the most efficient unlocks first: Hero Training to Cockpit, Military Strategies for efficient troop stats, Peace Shield for Urgent Rescue, and only then commit to the long UST path.</p>
```

After:

```html
<p>If you are asking what to research first in Last Z, the best answer for most players is not "rush everything toward T10." The stronger route is to take the most efficient unlocks first: Hero Training to Cockpit, Military Strategies for efficient troop stats, and Peace Shield for Urgent Rescue. After that, choose by goal: the shortest practical UST/T10 path for tier progression, or Siege to Seize into Field Research only if you want late Recharge Shield and deep combat scaling.</p>
```

### 16. T10 Path Paragraph 2

Before:

```html
<p>If your goal is T10 units, keep your path narrow and avoid spending badges on unrelated branches. Push the prerequisite gates that unlock higher troop tiers, then stack efficiency research around that path.</p>
```

After:

```html
<p>If your goal is T10 units, keep your path narrow and avoid spending badges on unrelated branches. Do not push into Field Research just because it exists after Siege to Seize; treat that as a late combat-scaling route, not a required stop before UST/T10.</p>
```

### 17. Step 4 Visible Section

Before:

```html
<div class="step">
    <h3>Step 4: Siege to Seize (Situational)</h3>
    <p><strong>Warning:</strong> This tree increases your Destruction Value. Only research if you're ready for more aggressive gameplay.</p>
    <p><strong>When to skip:</strong> If you prefer defensive play or are in a NAP alliance, delay this tree.</p>
    <p>If you do want the offensive path and Field Research unlock chain, use the <a href="siege-to-seize-cost.html">Siege to Seize Costs</a> page.</p>
</div>
```

After:

```html
<div class="step">
    <h3>Step 4: Choose UST/T10 or Siege to Seize by Goal</h3>
    <p><strong>Main decision:</strong> after Peace Shield and Urgent Rescue, do not treat Field Research as mandatory. If your goal is tier progression, stay on the shortest practical path toward UST and T10. If your goal is late PvP scaling and Recharge Shield, then push Siege to Seize and later Field Research.</p>
    <p><strong>When to delay Siege to Seize:</strong> If you prefer defensive play, are in a NAP alliance, or need badges for UST/T10 gates, delay this tree.</p>
    <p>If you choose the offensive / Recharge Shield route, use the <a href="siege-to-seize-cost.html">Siege to Seize Costs</a> page and then the <a href="field-research.html">Field Research Costs</a> page.</p>
</div>
```

### 18. Step 5 Final Warning

Before:

```html
<p><strong>Do not rush it:</strong> if your account still lacks efficient mid-game value in Hero Training, Military Strategies, Peace Shield, or Siege to Seize, those branches usually deserve badges first.</p>
```

After:

```html
<p><strong>Do not rush it:</strong> if your account still lacks efficient mid-game value in Hero Training, Military Strategies, or Peace Shield, those branches usually deserve badges first. Compare Siege to Seize and Field Research against your UST/T10 goal before spending rare badges there.</p>
```

### 19. Research Trees Unlock Order Note

Before:

```html
<li><strong>100% Siege to Seize</strong> → unlocks <strong><a href="field-research.html">Field Research</a></strong> (594k badges for Recharge Shield)</li>
```

After:

```html
<li><strong>100% Siege to Seize</strong> -> unlocks <strong><a href="field-research.html">Field Research</a></strong> (594k badges for Recharge Shield; late combat-scaling route, not required before UST/T10)</li>
```

### 20. Visible FAQ: Best Research Order

Before:

```html
<p>For most players: Hero Training to Cockpit, Military Strategies for efficient troop stats, Peace Shield for Urgent Rescue, then the shortest practical path toward UST and T10.</p>
```

After:

```html
<p>For most players: Hero Training to Cockpit, Military Strategies for efficient troop stats, and Peace Shield for Urgent Rescue. After that, choose the shortest practical UST/T10 path for tier progression, or Siege to Seize into Field Research only if you want late Recharge Shield and deep combat scaling.</p>
```

### 21. Verification Note

Before:

```html
<li><strong>Checked against:</strong> the canonical route from Hero Training to Cockpit, Military Strategies, Peace Shield, Siege to Seize, Field Research, linked branch cost pages, and UST planning context.</li>
```

After:

```html
<li><strong>Checked against:</strong> the canonical route from Hero Training to Cockpit, Military Strategies, Peace Shield/Urgent Rescue, the optional Siege to Seize -> Field Research route, linked branch cost pages, and UST/T10 planning context.</li>
```

### 22. Verification Review Month

Before:

```html
<li><strong>Last reviewed for research order and T10 planning:</strong> March 2026.</li>
```

After:

```html
<li><strong>Last reviewed for research order and T10 planning:</strong> May 2026.</li>
```

## Approval Scope

If approved, only `research.html` should be edited with the exact replacements above.

After applying approved changes, run:

```bash
python3 scripts/prepublish_check.py --fix
python3 scripts/prepublish_check.py
python3 automation/pipeline.py checks
python3 automation/pipeline.py checks --strict --manifest 2026-05-12-research-gsc-opportunity-llm-approved-intake
```
