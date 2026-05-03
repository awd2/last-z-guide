# Power Guide Structural Cleanup Proposal

Scope:

- `power-guide.html`

Purpose:

- Reduce the remaining `content-voice` high-risk signal on `power-guide.html`.
- Remove repeated five-power-type phrasing from first screen, FAQ, and JSON-LD.
- Add one compact decision table so the page helps players choose the next bottleneck instead of repeating broad advice.
- Preserve the page's title, H1, meta description, navigation, related links, cluster role, and current recommendations.

## Current Audit Signal

From `python3 automation/pipeline.py content-voice --top 10`:

- `power-guide.html` remains high risk.
- Main issue: repeated broad summary language around the same five power types.
- The page already has strong structure, but the first screen, intro, FAQ, and JSON-LD repeat the same answer with slightly different wording.

## Proposed Visible Copy Changes

### First-screen trust line

Replace:

```html
            <p class="guide-verified">Power grows fastest when each bottleneck has a job: HQ and Lab unlock the account, core research adds combat value, troops fill capacity, main 5 heroes carry fights, and vehicle level 100 opens components.</p>
```

With:

```html
            <p class="guide-verified">Power grows fastest when you fix the blocker in front of you: HQ/Lab for unlocks, research for combat value, troop queues for capacity, main 5 heroes for fights, and vehicle level 100 for components.</p>
```

### Quick Answer lead

Replace:

```html
                <p class="qa-lede"><strong>Best way to increase power fast in Last Z:</strong> remove the current bottleneck instead of chasing one CP source. Push HQ and Lab first, keep core research moving, train constantly, build the main 5 heroes, and take the vehicle toward level 100.</p>
```

With:

```html
                <p class="qa-lede"><strong>Best way to increase power fast in Last Z:</strong> identify the bottleneck, fix it, then move to the next one. Early accounts usually start with HQ/Lab; mid-game accounts get more from research, troop queues, main heroes, and vehicle level 100.</p>
```

### Quick Answer callout

Replace:

```html
                        <span class="qa-callout-text"><strong>Key rule:</strong> the fastest accounts do not chase one fake power source. They build structure, research, troop, hero, and vehicle power together.</span>
```

With:

```html
                        <span class="qa-callout-text"><strong>Key rule:</strong> do not chase empty CP. Upgrade the system that is currently blocking unlocks, combat value, troop count, hero output, or vehicle components.</span>
```

### Opening explanation

Replace:

```html
                <p>Combat Power is split across five buckets. If one bucket is far behind, it becomes the bottleneck: low HQ blocks unlocks, weak research lowers real combat value, empty training queues waste troop power, underbuilt heroes lose fights, and a stalled vehicle delays components.</p>
```

With:

```html
                <p>Combat Power is split across five buckets. The fastest upgrade is the one that removes the current blocker, not the one that only raises the visible number.</p>
```

After the existing five-item list, add this compact decision table before the current real example:

```html
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>If this is blocked...</th>
                            <th>Push this next</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>New buildings, troop tiers, or research are locked</td>
                            <td>HQ and Laboratory</td>
                        </tr>
                        <tr>
                            <td>You have badges but weak combat stats</td>
                            <td>Hero Training to Cockpit, Military Strategies, and Peace Shield</td>
                        </tr>
                        <tr>
                            <td>Training queues sit idle or troop tier is behind</td>
                            <td>Troop training and Elite Troops path</td>
                        </tr>
                        <tr>
                            <td>You lose fights despite decent CP</td>
                            <td>Main 5 heroes, orange gear, and combat skills</td>
                        </tr>
                        <tr>
                            <td>Vehicle components are still locked</td>
                            <td>Vehicle level 100 path</td>
                        </tr>
                    </tbody>
                </table>
```

### Troop section opener

Replace:

```html
            <p>Troop power is the simplest power source in the game: more troops and better troop tiers mean more CP. But the strongest growth comes from training consistently, not from random one-time pushes.</p>
```

With:

```html
            <p>Troop power comes from two habits: keep queues running and unlock better troop tiers. Random speedup bursts help less than never letting camps sit idle.</p>
```

### Hero section opener

Replace:

```html
            <p>Hero power is where many players waste resources. The fastest path is not upgrading everyone — it is concentrating levels, equipment, skill books, and fragments on your main 5 heroes first.</p>
```

With:

```html
            <p>Hero power is easy to waste because every hero can consume resources. Spend on the main 5 first: levels, stars, skill books, orange gear, and combat-focused skills.</p>
```

### Vehicle section opener

Replace:

```html
            <p>Vehicle power is one of the biggest hidden power spikes in Last Z. Many accounts underestimate it early, but reaching level 100 and unlocking components creates a major jump in both visible CP and real combat value.</p>
```

With:

```html
            <p>Vehicle power becomes a serious spike once components unlock. The practical checkpoint is level 100; before that, keep progress moving without starving HQ, research, troops, or main heroes.</p>
```

## Proposed FAQ Copy Changes

### Visible FAQ answer: fastest power

Replace:

```html
                <p>Fix the current bottleneck: HQ and Lab for unlocks, core research for combat value, training queues for troop power, main 5 heroes for battle output, and vehicle level 100 for components.</p>
```

With:

```html
                <p>Fix the current bottleneck. If unlocks are blocked, push HQ and Lab. If combat value is low, push core research. If queues are idle, train troops. If fights are weak, invest in the main 5 heroes. If components are locked, move the vehicle toward level 100.</p>
```

### Visible FAQ answer: five power types

Replace:

```html
                <p>Structure power, research power, troop power, hero power, and vehicle power. Fast growth comes from improving all five together instead of chasing only one visible power source.</p>
```

With:

```html
                <p>The five power types are structure, research, troop, hero, and vehicle power. Use them as a checklist: the lowest or most blocked category is usually the next useful upgrade.</p>
```

### Visible FAQ answer: first focus

Replace:

```html
                <p>Early on, focus on HQ and Lab for structure power, then keep research, troops, heroes, and vehicle moving behind them. The best power growth comes from removing bottlenecks, not from over-investing in one category.</p>
```

With:

```html
                <p>Start with HQ and Lab if they block unlocks. After that, choose the slowest useful system: research for stats, troop queues for capacity, main heroes for battle output, or vehicle level 100 for components.</p>
```

## Proposed JSON-LD FAQ Sync

Update the matching `FAQPage` answers so structured data matches the visible FAQ.

Replace the JSON-LD answer text for `What is the fastest way to increase power in Last Z?` with:

```json
"Fix the current bottleneck. If unlocks are blocked, push HQ and Lab. If combat value is low, push core research. If queues are idle, train troops. If fights are weak, invest in the main 5 heroes. If components are locked, move the vehicle toward level 100."
```

Replace the JSON-LD answer text for `What are the 5 power types in Last Z?` with:

```json
"The five power types are structure, research, troop, hero, and vehicle power. Use them as a checklist: the lowest or most blocked category is usually the next useful upgrade."
```

Replace the JSON-LD answer text for `Which power source should I focus on first?` with:

```json
"Start with HQ and Lab if they block unlocks. After that, choose the slowest useful system: research for stats, troop queues for capacity, main heroes for battle output, or vehicle level 100 for components."
```

## Not Included

- No title, H1, meta description, navigation, or related-link change.
- No change to the research route or Alliance Recognition nuance.
- No change to vehicle cost or modifier claims.
- No change to page archetype or cluster role.
- No commit/push before owner approval.

## Implementation Path After Approval

1. Apply the approved visible copy replacements to `power-guide.html`.
2. Add the approved bottleneck table after the five power-type list.
3. Update the three matching `FAQPage` JSON-LD answers.
4. Run:
   - `python3 scripts/prepublish_check.py --fix`
   - `python3 scripts/prepublish_check.py`
   - `python3 automation/pipeline.py checks`
   - `python3 automation/pipeline.py checks --strict`
   - `python3 automation/pipeline.py content-voice --top 40`
5. Show the exact diff before commit.

## Follow-Up To Consider Separately

- After this cleanup, if `power-guide.html` still remains high risk, the next pass should review the shops/events sections. Those sections are useful but list-heavy and may need a sharper "buy / skip / when" table.
