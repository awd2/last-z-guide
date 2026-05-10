# LLM Topic Discovery - 2026-05-10T08:07:50Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-scout-review-result.json`
- Source Scout request: `automation/reports/llm-scout-review-request.json`
- Topics: 8
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Topic Proposals

### alliance-duel-gsc-opportunity

- Title: GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy
- Target: `alliance-duel.html`
- Cluster: `Events`
- Action: `update_existing`
- Archetype: `event-guide`
- Priority: `high`
- Risk: `medium`
- Confidence: `high`
- Prior review: `none`
- Human approval required: `true`

Player value:

Helps players quickly find event timing, day-by-day plan, and matchup guidance on the existing guide.

Rationale:

High-impression event page with a clear query intent around schedule and VS strategy. This is a good candidate for a scoped update to improve query-to-page match without creating new content.

Duplication risk:

Medium. The topic could overlap with other event or schedule pages if cluster separation is not kept strict.

Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- The current page remains the best canonical fit for schedule-related intent.
- The update can be done without turning the page into a broader event hub.
- No protected claims or cluster role boundaries are crossed.

Evidence:

- GSC page signal: alliance-duel.html had 8212 impressions, 378 clicks, 4.60% CTR, avg position 6.26.

Backlog Row Preview:

```json
{
  "topic_id": "alliance-duel-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy",
  "cluster": "Events",
  "recommended_action": "update_existing",
  "archetype_suggestion": "event-guide",
  "target_page_or_slug": "alliance-duel.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-03: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "high",
  "status": "candidate",
  "notes": "High-impression event page with a clear query intent around schedule and VS strategy. This is a good candidate for a scoped update to improve query-to-page match without creating new content."
}
```

Next step:

Human review should confirm the page is still the best canonical home for this intent and define a narrow update scope.

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

Improves navigation for users searching redeem codes, gift center login, and UID-related redemption help.

Rationale:

This is a strong existing-page candidate because the page already gets substantial impressions and the low CTR queries point to gift center and redeem flow intent. It should be reviewed carefully as a cornerstone update, but it is not obviously a new page need. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

High. The page must not duplicate mailbox or alternate redeem-flow explanations and must preserve canonical claim boundaries.

Expected route:

- index.html
- codes.html

Claims to verify:

- gift-center-only-redeem-flow
- gift-rewards-mailbox
- gift-center-cluster-role-separation
- The existing page still owns this intent better than any other canonical page.

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
  "notes": "This is a strong existing-page candidate because the page already gets substantial impressions and the low CTR queries point to gift center and redeem flow intent. It should be reviewed carefully as a cornerstone update, but it is not obviously a new page need. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should verify the existing page can absorb the query intent while preserving protected claims and role separation.

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

Improves the entry point for broad searchers looking for the site, guides, and navigation to major clusters.

Rationale:

The homepage shows weak CTR on broad brand queries and rising interest in guide-style queries. This is worth review because the home page may need better first-screen clarity and routing, but changes must stay narrowly focused.

Duplication risk:

High. Homepage edits can easily blur the role of cluster landing pages and over-expand the page scope.

Expected route:

- index.html

Claims to verify:

- The homepage is still the right canonical entry point for broad brand intent.
- Any update can preserve navigation hierarchy and cluster separation.
- The change will not duplicate content owned by other hubs or guides.

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
  "notes": "The homepage shows weak CTR on broad brand queries and rising interest in guide-style queries. This is worth review because the home page may need better first-screen clarity and routing, but changes must stay narrowly focused."
}
```

Next step:

Human review should decide whether the homepage can be tightened for clarity without becoming a duplicate guide or cluster hub.

### research-gsc-opportunity

- Title: GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path
- Target: `research.html`
- Cluster: `Research`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

Worth monitoring but not selected over other stronger existing-page opportunities. It is a valid cornerstone update candidate, yet the evidence is thinner than the top picks and should wait for a more specific intent or stronger query pattern. Future trigger: Select if query trends become more specific around research priority, peace shield, or mainline path intent.

Duplication risk:



Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- None

Evidence:

- GSC page signal: research.html had 12710 impressions, 597 clicks, 4.70% CTR, avg position 7.27.
- Rising query: `last z research priority` gained 11 impressions in the last 7-day comparison window.

Backlog Row Preview:

```json
{
  "topic_id": "research-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-03: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Worth monitoring but not selected over other stronger existing-page opportunities. It is a valid cornerstone update candidate, yet the evidence is thinner than the top picks and should wait for a more specific intent or stronger query pattern. Future trigger: Select if query trends become more specific around research priority, peace shield, or mainline path intent."
}
```

Next step:

Select if query trends become more specific around research priority, peace shield, or mainline path intent.

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

Useful existing-page candidate, but lower urgency than the strongest selected opportunities and more constrained by protected claim separation. Future trigger: Select if vehicle upgrade intent continues to rise or if a clearer cost-related query cluster emerges.

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
  "notes": "Useful existing-page candidate, but lower urgency than the strongest selected opportunities and more constrained by protected claim separation. Future trigger: Select if vehicle upgrade intent continues to rise or if a clearer cost-related query cluster emerges."
}
```

Next step:

Select if vehicle upgrade intent continues to rise or if a clearer cost-related query cluster emerges.

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

Reasonable cornerstone page opportunity, but the evidence is moderate and the page may need broader intent validation before human review proceeds. Future trigger: Select if season-specific hero ranking queries continue rising or if CTR remains weak across the cluster.

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
  "notes": "Reasonable cornerstone page opportunity, but the evidence is moderate and the page may need broader intent validation before human review proceeds. Future trigger: Select if season-specific hero ranking queries continue rising or if CTR remains weak across the cluster."
}
```

Next step:

Select if season-specific hero ranking queries continue rising or if CTR remains weak across the cluster.

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

Worth monitoring, but the query intent is currently too close to a broad progression guide to justify selection ahead of stronger opportunities. Future trigger: Select if HQ upgrade and requirement queries show clearer separation from other progression pages.

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
  "notes": "Worth monitoring, but the query intent is currently too close to a broad progression guide to justify selection ahead of stronger opportunities. Future trigger: Select if HQ upgrade and requirement queries show clearer separation from other progression pages."
}
```

Next step:

Select if HQ upgrade and requirement queries show clearer separation from other progression pages.

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

The very low CTR suggests a possible mismatch, but the topic is still analytics-led and needs stronger intent confirmation before review. Future trigger: Select if combat power queries grow or if search intent becomes more explicit around fast power gain.

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
  "notes": "The very low CTR suggests a possible mismatch, but the topic is still analytics-led and needs stronger intent confirmation before review. Future trigger: Select if combat power queries grow or if search intent becomes more explicit around fast power gain."
}
```

Next step:

Select if combat power queries grow or if search intent becomes more explicit around fast power gain.
