# LLM Topic Discovery - 2026-05-05T19:27:12Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-worker-chain-scout-result.json`
- Source Scout request: `automation/reports/llm-worker-chain-scout-request.json`
- Topics: 8
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Topic Proposals

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

Faster understanding of where to start for broad Last Z searches; improved navigation into the most relevant cluster pages.

Rationale:

High-volume home-page signal with low CTR on broad and rising Last Z queries suggests the homepage may need better query-to-page alignment and above-the-fold utility. This is a strong candidate for human review because the existing page already serves the home-hub role and the opportunity is to improve entry-point relevance without introducing new content.

Duplication risk:

Medium, because broad intent could overlap with other canonical guides if the homepage becomes too content-heavy.

Expected route:

- index.html

Claims to verify:

- Whether the broad query intent is already better matched by another canonical page
- Whether any proposed homepage additions would blur the home-hub role
- Whether the improvement can be achieved within approved scope without a cornerstone rewrite

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
  "notes": "High-volume home-page signal with low CTR on broad and rising Last Z queries suggests the homepage may need better query-to-page alignment and above-the-fold utility. This is a strong candidate for human review because the existing page already serves the home-hub role and the opportunity is to improve entry-point relevance without introducing new content."
}
```

Next step:

Review whether a minimal homepage refresh can improve entry intent while preserving cluster separation and existing template patterns.

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

Clearer research prioritization guidance and faster path to the most valuable research decisions.

Rationale:

Research page shows meaningful impressions with average position in the upper SERP and a rising research-priority query. This is a strong candidate for targeted updates because the page is clearly the canonical research hub and the opportunity seems tied to ranking clarity rather than new topic creation.

Duplication risk:

Medium, because research content can easily overlap with progression or economy guidance if scope is expanded too much.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- Whether the intent is better served elsewhere
- Whether proposed edits preserve research cluster boundaries
- Whether the required improvements fit within the existing cornerstone-page scope

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
  "notes": "Research page shows meaningful impressions with average position in the upper SERP and a rising research-priority query. This is a strong candidate for targeted updates because the page is clearly the canonical research hub and the opportunity seems tied to ranking clarity rather than new topic creation."
}
```

Next step:

Check whether the current research page can be strengthened with a sharper first-screen answer and refined section order while protecting canonical claims.

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

Improved ability to find active codes and understand the gift center/login/redeem path quickly.

Rationale:

Economy/codes page has the largest impression volume among the reviewed pages and several weak-CTR gift-center queries. Because this page already anchors critical canonical claims, it is worth human review to determine if query alignment can be improved without breaking role separation or the protected redeem-flow logic. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

High, because this topic risks overlapping with login/help flows and could easily blur canonical boundaries.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether another canonical page better serves gift-center-login intent
- Whether the update would blur cluster role separation
- Whether the protected redeem and mailbox claims remain intact

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
  "notes": "Economy/codes page has the largest impression volume among the reviewed pages and several weak-CTR gift-center queries. Because this page already anchors critical canonical claims, it is worth human review to determine if query alignment can be improved without breaking role separation or the protected redeem-flow logic. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have an owner review whether a constrained update can address query mismatch while preserving the protected canonical claims and existing backlog status.

### alliance-duel-gsc-opportunity

- Title: GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy
- Target: `alliance-duel.html`
- Cluster: `Events`
- Action: `monitor`
- Archetype: `event-guide`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

Worth monitoring but lower urgency than the core hub pages; the user job appears narrower and the existing signal is sufficient only for review, not immediate action. Future trigger: If alliance-duel queries continue rising or CTR drops further while intent stays schedule-oriented.

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
  "notes": "Worth monitoring but lower urgency than the core hub pages; the user job appears narrower and the existing signal is sufficient only for review, not immediate action. Future trigger: If alliance-duel queries continue rising or CTR drops further while intent stays schedule-oriented."
}
```

Next step:

If alliance-duel queries continue rising or CTR drops further while intent stays schedule-oriented.

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

Solid opportunity, but it is narrower and more constrained than the top-priority hub pages. It should remain on the shortlist without displacing higher-leverage pages. Future trigger: If equipment/upgrade intent expands or related queries show sustained growth.

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
  "notes": "Solid opportunity, but it is narrower and more constrained than the top-priority hub pages. It should remain on the shortlist without displacing higher-leverage pages. Future trigger: If equipment/upgrade intent expands or related queries show sustained growth."
}
```

Next step:

If equipment/upgrade intent expands or related queries show sustained growth.

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

Interesting but currently less differentiated from other hero-ranking content and more likely to require careful scope control before any update. Future trigger: If seasonal or faction-specific hero queries rise materially.

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
  "notes": "Interesting but currently less differentiated from other hero-ranking content and more likely to require careful scope control before any update. Future trigger: If seasonal or faction-specific hero queries rise materially."
}
```

Next step:

If seasonal or faction-specific hero queries rise materially.

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

Reasonable review candidate, but the title/intent appears broad and could overlap with progression/start content; better to monitor until query patterns become clearer. Future trigger: If HQ upgrade queries gain stronger volume or a more specific intent cluster emerges.

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
  "notes": "Reasonable review candidate, but the title/intent appears broad and could overlap with progression/start content; better to monitor until query patterns become clearer. Future trigger: If HQ upgrade queries gain stronger volume or a more specific intent cluster emerges."
}
```

Next step:

If HQ upgrade queries gain stronger volume or a more specific intent cluster emerges.

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

Very low CTR indicates opportunity, but the intent may be too ambiguous without additional query-level evidence; monitoring is safer than immediate action. Future trigger: If combat power queries become more explicit and sustained in the next reporting window.

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
  "notes": "Very low CTR indicates opportunity, but the intent may be too ambiguous without additional query-level evidence; monitoring is safer than immediate action. Future trigger: If combat power queries become more explicit and sustained in the next reporting window."
}
```

Next step:

If combat power queries become more explicit and sustained in the next reporting window.
