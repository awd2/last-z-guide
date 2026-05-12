# LLM Topic Discovery - 2026-05-12T18:35:43Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`
- Source Scout request: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`
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

Better first-screen help for gift center searchers, faster path to active codes and login-related tasks, and improved match for high-volume queries.

Rationale:

This is a high-value existing cornerstone page with strong impression volume and multiple low-CTR gift center queries pointing to a query-page mismatch. The page already owns the relevant intent, so an update_existing review is appropriate if it can preserve canonical claims and cluster role separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because gift center intent may overlap with home or research content if boundaries are not kept clear.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether codes.html can address the query intent without broadening into another cluster's responsibilities.
- Whether the current first-screen content already satisfies the login and active-codes intent adequately.
- Whether the existing canonical claims fully cover the intended page sections.

Evidence:

- GSC page signal: codes.html had 33220 impressions, 586 clicks, 1.76% CTR, avg position 6.11.
- Low CTR query: `last z gift center` had 3075 impressions, 113 clicks, 3.67% CTR, position 6.83.
- Low CTR query: `last z gift center login` had 943 impressions, 43 clicks, 4.56% CTR, position 5.41.
- Low CTR query: `lastz gift center` had 555 impressions, 23 clicks, 4.14% CTR, position 6.37.
- Low CTR query: `last-z.com gift center` had 479 impressions, 22 clicks, 4.59% CTR, position 6.00.

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
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This is a high-value existing cornerstone page with strong impression volume and multiple low-CTR gift center queries pointing to a query-page mismatch. The page already owns the relevant intent, so an update_existing review is appropriate if it can preserve canonical claims and cluster role separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human owner review for a scoped content proposal that preserves gift-center-only-redeem-flow, gift-rewards-mailbox, and gift-center-cluster-role-separation.

### index-gsc-opportunity

- Title: GSC opportunity review: Last Z Guides — Research, Events, HQ, Heroes, and F2P Strategy
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

Clearer entry point for new and returning users, better routing into research and related hub pages, and improved brand-query handling.

Rationale:

The home hub has meaningful traffic and a rising branded/research query signal. Since it is the existing home page, it is a suitable candidate for a limited update_existing review rather than a new page.

Duplication risk:

Low, because home hub intent is naturally broad, but it must not absorb cluster-specific content.

Expected route:

- index.html

Claims to verify:

- Whether the homepage is currently the best canonical answer for the rising research-guide query.
- Whether any proposed additions would blur hub versus cluster-page responsibilities.
- Whether the existing template can support the needed navigation emphasis.

Evidence:

- GSC page signal: index.html had 10947 impressions, 823 clicks, 7.52% CTR, avg position 6.64.
- Rising query: `last z research guide` gained 11 impressions in the last 7-day comparison window.
- Rising query: `lastzguides.com` gained 3 impressions in the last 7-day comparison window.

Backlog Row Preview:

```json
{
  "topic_id": "index-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Guides — Research, Events, HQ, Heroes, and F2P Strategy",
  "cluster": "Home",
  "recommended_action": "update_existing",
  "archetype_suggestion": "home-hub",
  "target_page_or_slug": "index.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "high",
  "status": "candidate",
  "notes": "The home hub has meaningful traffic and a rising branded/research query signal. Since it is the existing home page, it is a suitable candidate for a limited update_existing review rather than a new page."
}
```

Next step:

Request human review to determine whether the homepage can better surface research and site navigation without weakening the home role.

### research-gsc-opportunity

- Title: GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path
- Target: `research.html`
- Cluster: `Research`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: `high`
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:

Improved guidance for research planning, rescue timing, and related progression decisions for players who need a central research roadmap.

Rationale:

This is a strong cornerstone-guide candidate with rising research and rescue queries, and the page already owns the relevant user job. The signal supports a focused update_existing review, not a new page. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because research, progression, and hero-training topics can overlap if the page is expanded too broadly.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- Whether research-best-mainline remains the correct canonical emphasis.
- Whether hero-training-cockpit-stop and peace-shield-value remain distinct and protected.
- Whether research-atlas-role needs any boundary clarification before a proposal is drafted.

Evidence:

- GSC page signal: research.html had 13619 impressions, 670 clicks, 4.92% CTR, avg position 7.16.
- Rising query: `last z research guide` gained 11 impressions in the last 7-day comparison window.
- Rising query: `last z urgent rescue` gained 8 impressions in the last 7-day comparison window.
- Rising query: `urgent rescue last z` gained 3 impressions in the last 7-day comparison window.

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
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This is a strong cornerstone-guide candidate with rising research and rescue queries, and the page already owns the relevant user job. The signal supports a focused update_existing review, not a new page. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Route to human review to confirm whether research.html can absorb the new query intents while protecting canonical claims and cluster roles.

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

Worth monitoring but not a top human-review priority compared with the stronger cornerstone and hub opportunities. The signal is useful, but the intent appears narrower and less urgent than the leading pages. Future trigger: Revisit if vehicle upgrade queries grow, or if equipment-related search volume increases across multiple related queries.

Duplication risk:



Expected route:

- index.html
- gear.html
- vehicle-modification-cost.html

Claims to verify:

- None

Evidence:

- GSC page signal: vehicle-modification-cost.html had 7319 impressions, 480 clicks, 6.56% CTR, avg position 5.82.

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
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Worth monitoring but not a top human-review priority compared with the stronger cornerstone and hub opportunities. The signal is useful, but the intent appears narrower and less urgent than the leading pages. Future trigger: Revisit if vehicle upgrade queries grow, or if equipment-related search volume increases across multiple related queries."
}
```

Next step:

Revisit if vehicle upgrade queries grow, or if equipment-related search volume increases across multiple related queries.

### alliance-duel-gsc-opportunity

- Title: GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy
- Target: `alliance-duel.html`
- Cluster: `Events`
- Action: `monitor`
- Archetype: `event-guide`
- Priority: `low`
- Risk: ``
- Confidence: `medium`
- Prior review: `closed`
- Human approval required: `false`

Player value:



Rationale:

Monitor only for now. The event-guide signal is real, but the topic appears less distinct and more likely to overlap with scheduling or competition content without a clear unique player job. Future trigger: Move up if alliance duel query volume rises or if there is evidence of repeated schedule-specific search intent. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:



Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- None

Evidence:

- GSC page signal: alliance-duel.html had 8965 impressions, 407 clicks, 4.54% CTR, avg position 6.19.

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
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "medium",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor only for now. The event-guide signal is real, but the topic appears less distinct and more likely to overlap with scheduling or competition content without a clear unique player job. Future trigger: Move up if alliance duel query volume rises or if there is evidence of repeated schedule-specific search intent. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Move up if alliance duel query volume rises or if there is evidence of repeated schedule-specific search intent.

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

Monitor only. The page has traffic, but the proposed title and intent suggest potential overlap with broader tier-list content, and the current signal does not clearly justify immediate review over stronger opportunities. Future trigger: Reconsider if season 4 hero queries rise sharply or if a distinct faction-based intent becomes dominant.

Duplication risk:



Expected route:

- index.html
- heroes.html

Claims to verify:

- None

Evidence:

- GSC page signal: heroes.html had 15334 impressions, 343 clicks, 2.24% CTR, avg position 7.93.

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
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "medium",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor only. The page has traffic, but the proposed title and intent suggest potential overlap with broader tier-list content, and the current signal does not clearly justify immediate review over stronger opportunities. Future trigger: Reconsider if season 4 hero queries rise sharply or if a distinct faction-based intent becomes dominant."
}
```

Next step:

Reconsider if season 4 hero queries rise sharply or if a distinct faction-based intent becomes dominant.

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

Monitor only. The page is a valid cornerstone candidate, but the current evidence is less specific about the exact query mismatch than the top opportunities. Future trigger: Promote to review if HQ upgrade queries show stronger growth or if a clearly distinct fast-path intent emerges.

Duplication risk:



Expected route:

- index.html
- start.html
- hq.html

Claims to verify:

- None

Evidence:

- GSC page signal: hq.html had 15316 impressions, 394 clicks, 2.57% CTR, avg position 7.56.

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
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "medium",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor only. The page is a valid cornerstone candidate, but the current evidence is less specific about the exact query mismatch than the top opportunities. Future trigger: Promote to review if HQ upgrade queries show stronger growth or if a clearly distinct fast-path intent emerges."
}
```

Next step:

Promote to review if HQ upgrade queries show stronger growth or if a clearly distinct fast-path intent emerges.

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

Monitor only. The CTR is weak, but the evidence is still just an analytics signal and does not yet prove that a rewrite is needed or that the page should be prioritized over stronger existing opportunities. Future trigger: Reconsider if low-CTR power queries persist or if there is a clear increase in combat-power search demand.

Duplication risk:



Expected route:

- index.html
- start.html
- power-guide.html

Claims to verify:

- None

Evidence:

- GSC page signal: power-guide.html had 9465 impressions, 92 clicks, 0.97% CTR, avg position 7.53.

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
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "medium",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor only. The CTR is weak, but the evidence is still just an analytics signal and does not yet prove that a rewrite is needed or that the page should be prioritized over stronger existing opportunities. Future trigger: Reconsider if low-CTR power queries persist or if there is a clear increase in combat-power search demand."
}
```

Next step:

Reconsider if low-CTR power queries persist or if there is a clear increase in combat-power search demand.
