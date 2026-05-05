# LLM Topic Discovery - 2026-05-05T19:24:04Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-worker-chain-scout-result.json`
- Source Scout request: `automation/reports/llm-worker-chain-scout-request.json`
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

Faster path to redeem codes and gift-center answers, reducing friction for users searching login/redeem flow information.

Rationale:

Highest-value opportunity: very large impression volume on a cornerstone economy page with multiple low-CTR gift center queries, indicating strong potential for better intent alignment while preserving the canonical role of the page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium; there is some risk of overlapping with other economy/codes intents, but the constraints explicitly protect canonical claim separation.

Expected route:

- index.html
- codes.html

Claims to verify:

- The existing page can cover gift center login intent without blurring role separation.
- Any added guidance preserves gift-center-only-redeem-flow and gift-rewards-mailbox claims.
- The backlog history does not already exhaust the likely opportunity.

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
  "notes": "Highest-value opportunity: very large impression volume on a cornerstone economy page with multiple low-CTR gift center queries, indicating strong potential for better intent alignment while preserving the canonical role of the page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human owner review to confirm whether a scoped first-screen and section-structure update can improve intent match without expanding the page beyond its canonical role.

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

Clearer research path for players deciding what to prioritize, especially around peace shield and mainline progression questions.

Rationale:

Strong cornerstone opportunity with healthy impressions and a rising research-priority query signal; likely a good candidate for tightening the guide's hierarchy and first-screen utility.

Duplication risk:

Medium; research topics can overlap with progression and hero guidance, so role boundaries need review.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- The page remains the best canonical home for research-order guidance.
- The update will not conflict with hero-training-cockpit-stop or peace-shield-value claims.
- The page can absorb the new query intent without needing a new page.

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
  "notes": "Strong cornerstone opportunity with healthy impressions and a rising research-priority query signal; likely a good candidate for tightening the guide's hierarchy and first-screen utility."
}
```

Next step:

Have the Research owner validate whether a scoped update can better answer 'research priority' and related queries while preserving canonical claims.

### hq-gsc-opportunity

- Title: GSC opportunity review: Last Z HQ Upgrade Guide — Requirements, Fast Path, and HQ 30/35 Strategy
- Target: `hq.html`
- Cluster: `Progression`
- Action: `update_existing`
- Archetype: `cornerstone-guide`
- Priority: `high`
- Risk: `high`
- Confidence: `medium`
- Prior review: `none`
- Human approval required: `true`

Player value:

Players can find the fastest HQ upgrade path and level-specific requirements more quickly.

Rationale:

HQ guide has substantial impressions with weak CTR and a highly specific upgrade-query fit, making it a strong candidate for improving top-of-page clarity and progression sequencing.

Duplication risk:

Low to medium; likely contained within progression, but should still be checked against start-page and other progression guides.

Expected route:

- index.html
- start.html
- hq.html

Claims to verify:

- HQ guidance is not better served by another canonical progression page.
- The update stays within the existing progression cluster role.
- No unsupported claim about exact level strategy is introduced.

Evidence:

- GSC page signal: hq.html had 12579 impressions, 338 clicks, 2.69% CTR, avg position 7.69.

Backlog Row Preview:

```json
{
  "topic_id": "hq-gsc-opportunity",
  "title": "GSC opportunity review: Last Z HQ Upgrade Guide — Requirements, Fast Path, and HQ 30/35 Strategy",
  "cluster": "Progression",
  "recommended_action": "update_existing",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "hq.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-03: page opportunity and query-page signals",
  "confidence": "medium",
  "priority": "high",
  "status": "candidate",
  "notes": "HQ guide has substantial impressions with weak CTR and a highly specific upgrade-query fit, making it a strong candidate for improving top-of-page clarity and progression sequencing."
}
```

Next step:

Owner review for a focused HQ content refresh, likely emphasizing requirements, fast path, and level 30/35 strategy in the existing structure.

### index-bing-opportunity

- Title: Bing opportunity review: Last Z Guides — Research, Events, HQ, Heroes, and F2P Strategy
- Target: `index.html`
- Cluster: `Home`
- Action: `monitor`
- Archetype: `home-hub`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

Useful signal, but the homepage is too broad and the query data is sparse; the opportunity is real yet should be monitored rather than acted on immediately as a rewrite target. Future trigger: If repeated Bing/GSC signals show a stable last z navigation/query pattern and the homepage underperforms relative to other hubs.

Duplication risk:



Expected route:

- index.html

Claims to verify:

- None

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
  "recommended_action": "monitor",
  "archetype_suggestion": "home-hub",
  "target_page_or_slug": "index.html",
  "source_type": "llm_scout",
  "source_reference": "Bing weekly 2026-05-01: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Useful signal, but the homepage is too broad and the query data is sparse; the opportunity is real yet should be monitored rather than acted on immediately as a rewrite target. Future trigger: If repeated Bing/GSC signals show a stable last z navigation/query pattern and the homepage underperforms relative to other hubs."
}
```

Next step:

If repeated Bing/GSC signals show a stable last z navigation/query pattern and the homepage underperforms relative to other hubs.

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

Plausible update_existing candidate, but the query intent is narrower and more event-specific; worth monitoring until stronger evidence confirms the page is the best canonical fit. Future trigger: If schedule/duel-related queries continue to climb and no other event canonical page serves them better.

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
  "notes": "Plausible update_existing candidate, but the query intent is narrower and more event-specific; worth monitoring until stronger evidence confirms the page is the best canonical fit. Future trigger: If schedule/duel-related queries continue to climb and no other event canonical page serves them better."
}
```

Next step:

If schedule/duel-related queries continue to climb and no other event canonical page serves them better.

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

Good traffic and CTR, but the evidence is weaker than the top-tier cornerstone opportunities and the improvement appears more specialized, so it is lower priority for human review now. Future trigger: If vehicle upgrade intent grows or conversion/engagement data shows the page is underperforming against similar equipment pages.

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
  "notes": "Good traffic and CTR, but the evidence is weaker than the top-tier cornerstone opportunities and the improvement appears more specialized, so it is lower priority for human review now. Future trigger: If vehicle upgrade intent grows or conversion/engagement data shows the page is underperforming against similar equipment pages."
}
```

Next step:

If vehicle upgrade intent grows or conversion/engagement data shows the page is underperforming against similar equipment pages.

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

Worth attention, but medium-confidence evidence and broad hero-tier-list intent make this somewhat more speculative than the highest-priority pages. Future trigger: If season/faction hero queries keep rising or CTR declines further on the existing page.

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
  "notes": "Worth attention, but medium-confidence evidence and broad hero-tier-list intent make this somewhat more speculative than the highest-priority pages. Future trigger: If season/faction hero queries keep rising or CTR declines further on the existing page."
}
```

Next step:

If season/faction hero queries keep rising or CTR declines further on the existing page.

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

Very low CTR is notable, but the evidence is weaker and may reflect broad, ambiguous intent rather than a clear page mismatch. Future trigger: If additional rising queries cluster around combat power and the page continues to attract impressions without clicks.

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
  "notes": "Very low CTR is notable, but the evidence is weaker and may reflect broad, ambiguous intent rather than a clear page mismatch. Future trigger: If additional rising queries cluster around combat power and the page continues to attract impressions without clicks."
}
```

Next step:

If additional rising queries cluster around combat power and the page continues to attract impressions without clicks.
