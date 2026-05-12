# LLM Topic Discovery - 2026-05-10T09:57:25Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-candidate-refresh-live/llm-candidate-refresh-scout-result.json`
- Source Scout request: `automation/reports/llm-candidate-refresh-live/llm-candidate-refresh-scout-request.json`
- Topics: 8
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Topic Proposals

### codes-gsc-opportunity

- Title: GSC opportunity review: Last Z Redeem Codes — Active Codes, Gift Center Login, and UID
- Target: `codes.html`
- Cluster: `Economy`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: `high`
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:

Better match for gift center and redeem-intent searches should reduce friction for players trying to redeem codes or locate the correct flow.

Rationale:

High impression volume plus multiple low-CTR gift center queries make codes.html a strong candidate for human review. The page already has backlog history and clear canonical protections, so the opportunity is to improve query match and first-screen usefulness without altering cluster role separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium; must avoid overlapping with mailbox or login guidance and keep redeem flow canonical.

Expected route:

- index.html
- codes.html

Claims to verify:

- gift-center-only-redeem-flow
- gift-rewards-mailbox
- gift-center-cluster-role-separation

Evidence:

- GSC page signal: codes.html had 24154 impressions, 503 clicks, 2.08% CTR, avg position 6.46.
- Low CTR query: `last z gift center` had 3048 impressions, 104 clicks, 3.41% CTR, position 6.98.
- Low CTR query: `last z gift center login` had 959 impressions, 44 clicks, 4.59% CTR, position 5.56.
- Low CTR query: `lastz gift center` had 501 impressions, 20 clicks, 3.99% CTR, position 6.89.
- Low CTR query: `last-z.com gift center` had 472 impressions, 20 clicks, 4.24% CTR, position 6.22.

Backlog Row Preview:

```json
{
  "topic_id": "codes-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Redeem Codes — Active Codes, Gift Center Login, and UID",
  "cluster": "Economy",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "codes.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-03: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "High impression volume plus multiple low-CTR gift center queries make codes.html a strong candidate for human review. The page already has backlog history and clear canonical protections, so the opportunity is to improve query match and first-screen usefulness without altering cluster role separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human owner review for a scoped update plan on codes.html, with explicit checks against canonical claim boundaries.

### index-bing-opportunity

- Title: Bing opportunity review: Last Z Guides — Research, Events, HQ, Heroes, and F2P Strategy
- Target: `index.html`
- Cluster: `Home`
- Action: `update_existing`
- Archetype: `home-hub`
- Priority: `high`
- Risk: `high`
- Confidence: `high`
- Prior review: `none`
- Human approval required: `true`

Player value:

Players searching the brand or broad game term should land faster on the right cluster routes and primary entry points.

Rationale:

The home page has a broad query footprint and rising generic interest in last z terms. Because it is a hub page, small navigation or intro refinements could improve entry-point relevance without creating new content.

Duplication risk:

Low to medium; the main risk is overloading the home page with topic content instead of hub navigation.

Expected route:

- index.html

Claims to verify:

- research-atlas-home-promotion

Evidence:

- Bing page signal: index.html had 1157 impressions, 32 clicks, 2.77% CTR, avg position 6.00.
- Low CTR query: `last z` had 337 impressions, 1 clicks, 0.30% CTR, position 7.00.
- Rising query: `last z` gained 75 impressions in the last 7-day comparison window.
- Rising query: `last z guide` gained 17 impressions in the last 7-day comparison window.
- Rising query: `last z survival shooter guide` gained 2 impressions in the last 7-day comparison window.

Backlog Row Preview:

```json
{
  "topic_id": "index-bing-opportunity",
  "title": "Bing opportunity review: Last Z Guides — Research, Events, HQ, Heroes, and F2P Strategy",
  "cluster": "Home",
  "recommended_action": "update_existing",
  "archetype_suggestion": "home-hub",
  "target_page_or_slug": "index.html",
  "source_type": "llm_scout",
  "source_reference": "Bing weekly 2026-05-01: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "high",
  "status": "candidate",
  "notes": "The home page has a broad query footprint and rising generic interest in last z terms. Because it is a hub page, small navigation or intro refinements could improve entry-point relevance without creating new content."
}
```

Next step:

Have a human review whether index.html can be tuned as a clearer hub for broad discovery queries.

### research-gsc-opportunity

- Title: GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path
- Target: `research.html`
- Cluster: `Research`
- Action: `update_existing`
- Archetype: `cornerstone-guide`
- Priority: `high`
- Risk: `high`
- Confidence: `high`
- Prior review: `none`
- Human approval required: `true`

Player value:

Players get a more useful research path and faster understanding of what to prioritize first.

Rationale:

research.html shows meaningful impressions but middling CTR, plus a rising research priority query. This suggests the page likely needs clearer positioning of order, scope, and progression value rather than new content.

Duplication risk:

Medium; must stay distinct from costs, hero training, and peace shield guidance.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- research-best-mainline
- hero-training-cockpit-stop
- peace-shield-value
- research-atlas-role

Evidence:

- GSC page signal: research.html had 12710 impressions, 597 clicks, 4.70% CTR, avg position 7.27.
- Rising query: `last z research priority` gained 11 impressions in the last 7-day comparison window.

Backlog Row Preview:

```json
{
  "topic_id": "research-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path",
  "cluster": "Research",
  "recommended_action": "update_existing",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-03: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "high",
  "status": "candidate",
  "notes": "research.html shows meaningful impressions but middling CTR, plus a rising research priority query. This suggests the page likely needs clearer positioning of order, scope, and progression value rather than new content."
}
```

Next step:

Route to human review to test whether the page can better answer research priority intent within current structure.

### alliance-duel-gsc-opportunity

- Title: GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy
- Target: `alliance-duel.html`
- Cluster: `Events`
- Action: `monitor`
- Archetype: `event-guide`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:



Rationale:

Worth monitoring, but the user job is narrower and the evidence is less broad than the top page opportunities. It should not advance without a careful canonical overlap check against schedule-related pages. Future trigger: Prominent growth in schedule or day-by-day intent queries, or clear evidence that alliance-duel.html is the best canonical route. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:



Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- None

Evidence:

- GSC page signal: alliance-duel.html had 8212 impressions, 378 clicks, 4.60% CTR, avg position 6.26.

Backlog Row Preview:

```json
{
  "topic_id": "alliance-duel-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy",
  "cluster": "Events",
  "recommended_action": "monitor",
  "archetype_suggestion": "event-guide",
  "target_page_or_slug": "alliance-duel.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-03: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Worth monitoring, but the user job is narrower and the evidence is less broad than the top page opportunities. It should not advance without a careful canonical overlap check against schedule-related pages. Future trigger: Prominent growth in schedule or day-by-day intent queries, or clear evidence that alliance-duel.html is the best canonical route. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Prominent growth in schedule or day-by-day intent queries, or clear evidence that alliance-duel.html is the best canonical route.

### vehicle-modification-cost-gsc-opportunity

- Title: GSC opportunity review: Last Z Vehicle Modification Costs — Wrenches, Milestones, and Unlock Path
- Target: `vehicle-modification-cost.html`
- Cluster: `Equipment`
- Action: `monitor`
- Archetype: `cost-page`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

Monitor for now. The page has good CTR already, so the case for change is weaker and may not justify human review ahead of higher-impact pages. Future trigger: CTR decline, new high-volume upgrade-cost queries, or stronger evidence of unmet vehicle upgrade intent.

Duplication risk:



Expected route:

- index.html
- gear.html
- vehicle-modification-cost.html

Claims to verify:

- None

Evidence:

- GSC page signal: vehicle-modification-cost.html had 7918 impressions, 573 clicks, 7.24% CTR, avg position 5.69.

Backlog Row Preview:

```json
{
  "topic_id": "vehicle-modification-cost-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Vehicle Modification Costs — Wrenches, Milestones, and Unlock Path",
  "cluster": "Equipment",
  "recommended_action": "monitor",
  "archetype_suggestion": "cost-page",
  "target_page_or_slug": "vehicle-modification-cost.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-03: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor for now. The page has good CTR already, so the case for change is weaker and may not justify human review ahead of higher-impact pages. Future trigger: CTR decline, new high-volume upgrade-cost queries, or stronger evidence of unmet vehicle upgrade intent."
}
```

Next step:

CTR decline, new high-volume upgrade-cost queries, or stronger evidence of unmet vehicle upgrade intent.

### heroes-gsc-opportunity

- Title: GSC opportunity review: Last Z Best Heroes Tier List — Season 4 Rankings by Faction
- Target: `heroes.html`
- Cluster: `Heroes`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: ``
- Confidence: `medium`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

Monitor for now because the data supports attention, but the query target is likely to overlap with other hero list or faction pages and needs more intent clarity before review. Future trigger: Stronger season 4 hero ranking demand or clearer evidence that heroes.html is the primary canonical answer.

Duplication risk:



Expected route:

- index.html
- heroes.html

Claims to verify:

- None

Evidence:

- GSC page signal: heroes.html had 14143 impressions, 325 clicks, 2.30% CTR, avg position 7.94.

Backlog Row Preview:

```json
{
  "topic_id": "heroes-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Best Heroes Tier List — Season 4 Rankings by Faction",
  "cluster": "Heroes",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "heroes.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-03: page opportunity and query-page signals",
  "confidence": "medium",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor for now because the data supports attention, but the query target is likely to overlap with other hero list or faction pages and needs more intent clarity before review. Future trigger: Stronger season 4 hero ranking demand or clearer evidence that heroes.html is the primary canonical answer."
}
```

Next step:

Stronger season 4 hero ranking demand or clearer evidence that heroes.html is the primary canonical answer.

### hq-gsc-opportunity

- Title: GSC opportunity review: Last Z HQ Upgrade Guide — Requirements, Fast Path, and HQ 30/35 Strategy
- Target: `hq.html`
- Cluster: `Progression`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: ``
- Confidence: `medium`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

Monitor for now. The topic appears valuable but may be too close to other progression and upgrade pages unless query intent is sharply defined. Future trigger: Clearer HQ upgrade demand, especially around specific levels or fast path wording.

Duplication risk:



Expected route:

- index.html
- start.html
- hq.html

Claims to verify:

- None

Evidence:

- GSC page signal: hq.html had 12579 impressions, 338 clicks, 2.69% CTR, avg position 7.69.

Backlog Row Preview:

```json
{
  "topic_id": "hq-gsc-opportunity",
  "title": "GSC opportunity review: Last Z HQ Upgrade Guide — Requirements, Fast Path, and HQ 30/35 Strategy",
  "cluster": "Progression",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "hq.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-03: page opportunity and query-page signals",
  "confidence": "medium",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor for now. The topic appears valuable but may be too close to other progression and upgrade pages unless query intent is sharply defined. Future trigger: Clearer HQ upgrade demand, especially around specific levels or fast path wording."
}
```

Next step:

Clearer HQ upgrade demand, especially around specific levels or fast path wording.

### power-guide-gsc-opportunity

- Title: GSC opportunity review: Last Z Power Guide — How to Increase Combat Power Fast
- Target: `power-guide.html`
- Cluster: `Progression`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: ``
- Confidence: `medium`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

Reject for now. The very low CTR suggests a problem, but the proposal is still too analytics-led and may need a deeper intent diagnosis before any human review step. Future trigger: A clearer player job emerges from query clustering or supporting behavior signals.

Duplication risk:



Expected route:

- index.html
- start.html
- power-guide.html

Claims to verify:

- None

Evidence:

- GSC page signal: power-guide.html had 8657 impressions, 78 clicks, 0.90% CTR, avg position 7.61.

Backlog Row Preview:

```json
{
  "topic_id": "power-guide-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Power Guide — How to Increase Combat Power Fast",
  "cluster": "Progression",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "power-guide.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-03: page opportunity and query-page signals",
  "confidence": "medium",
  "priority": "low",
  "status": "monitor",
  "notes": "Reject for now. The very low CTR suggests a problem, but the proposal is still too analytics-led and may need a deeper intent diagnosis before any human review step. Future trigger: A clearer player job emerges from query clustering or supporting behavior signals."
}
```

Next step:

A clearer player job emerges from query clustering or supporting behavior signals.
