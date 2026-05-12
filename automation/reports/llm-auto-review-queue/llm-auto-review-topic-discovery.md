# LLM Topic Discovery - 2026-05-12T19:14:41Z

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

Better match for gift center and redeem-code searchers, faster path to active codes, login, UID, and related redemption flow questions.

Rationale:

High impression volume on an established cornerstone page plus several gift-center related queries suggest a likely first-screen and query-match opportunity. The page already has backlog history, so this should be reviewed as a controlled existing-page update rather than a new topic. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. There is a risk of overlapping with other gift-center or redemption pages, so cluster separation and canonical claims must be protected.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the low CTR is caused by snippet mismatch, intent mismatch, or both.
- Whether any competing canonical page already serves gift-center login intent better.
- Whether proposed changes can preserve gift-center-only-redeem-flow, gift-rewards-mailbox, and gift-center-cluster-role-separation.

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
  "notes": "High impression volume on an established cornerstone page plus several gift-center related queries suggest a likely first-screen and query-match opportunity. The page already has backlog history, so this should be reviewed as a controlled existing-page update rather than a new topic. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human owner should review whether the current codes page can satisfy gift-center intent without expanding scope beyond the approved cornerstone template.

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

Improved first-screen clarity for users arriving from branded or research-guide queries, with better routing to core site areas.

Rationale:

The home page has strong volume and a rising branded research query signal. This is a good candidate for a lightweight hub refinement if it can better route visitors without changing role or structure.

Duplication risk:

Low to medium. The main risk is making the home page too specific and weakening its hub role.

Expected route:

- index.html

Claims to verify:

- Whether the rising query volume is enough to justify a visible navigation or summary adjustment.
- Whether another page already better satisfies research-guide intent.
- Whether the home page can stay within its existing hub template and role.

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
  "notes": "The home page has strong volume and a rising branded research query signal. This is a good candidate for a lightweight hub refinement if it can better route visitors without changing role or structure."
}
```

Next step:

Human owner should confirm whether the home page can better surface the right navigation and summary blocks while staying a true hub.

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

Better support for research order, urgent rescue questions, peace shield value, and mainline progression planning.

Rationale:

This is one of the strongest opportunities because the research page has substantial volume and multiple rising queries tied to a clear player job. The proposal still needs human review to ensure it does not blur into other progression or hero guidance pages. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium to high. Research overlaps with progression, heroes, and event guidance, so cross-cluster clarity matters.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- Whether last z research guide intent belongs primarily on research.html.
- Whether urgent rescue is distinct from other progression or event guidance topics.
- Whether the protected canonical claims remain accurate and sufficient.

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
  "notes": "This is one of the strongest opportunities because the research page has substantial volume and multiple rising queries tied to a clear player job. The proposal still needs human review to ensure it does not blur into other progression or hero guidance pages. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human owner should review query intent mapping and confirm the page can answer the rising research questions without taking over adjacent canonical topics.

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

Monitor only for now. The signal is useful, but the evidence is limited to page-level GSC data and the proposed title suggests a possible wording drift from the existing canonical topic. Future trigger: Promote only if query-level intent around vehicle upgrade costs becomes clearer and can be verified without copying competitor phrasing.

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
  "notes": "Monitor only for now. The signal is useful, but the evidence is limited to page-level GSC data and the proposed title suggests a possible wording drift from the existing canonical topic. Future trigger: Promote only if query-level intent around vehicle upgrade costs becomes clearer and can be verified without copying competitor phrasing."
}
```

Next step:

Promote only if query-level intent around vehicle upgrade costs becomes clearer and can be verified without copying competitor phrasing.

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

Monitor only for now. The page-level signal is real, but there is not enough query evidence here to confirm that the proposed schedule-focused angle is the best fit. Future trigger: Revisit if query logs show sustained demand for schedule, day-by-day planning, or VS strategy around alliance duel. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Monitor only for now. The page-level signal is real, but there is not enough query evidence here to confirm that the proposed schedule-focused angle is the best fit. Future trigger: Revisit if query logs show sustained demand for schedule, day-by-day planning, or VS strategy around alliance duel. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Revisit if query logs show sustained demand for schedule, day-by-day planning, or VS strategy around alliance duel.

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

Monitor only for now. The page has volume, but the proposal is still too dependent on a seasonal ranking angle that may overlap with other hero guidance pages. Future trigger: Revisit if seasonal hero tier queries become more explicit and can be mapped cleanly to the heroes page without duplication.

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
  "notes": "Monitor only for now. The page has volume, but the proposal is still too dependent on a seasonal ranking angle that may overlap with other hero guidance pages. Future trigger: Revisit if seasonal hero tier queries become more explicit and can be mapped cleanly to the heroes page without duplication."
}
```

Next step:

Revisit if seasonal hero tier queries become more explicit and can be mapped cleanly to the heroes page without duplication.

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

Monitor only for now. The HQ page shows strong volume, but the current proposal is broad and could easily overlap with progression or start-hub intent. Future trigger: Revisit if the highest-value queries clearly point to HQ upgrade requirements and fast-path planning on the canonical HQ page.

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
  "notes": "Monitor only for now. The HQ page shows strong volume, but the current proposal is broad and could easily overlap with progression or start-hub intent. Future trigger: Revisit if the highest-value queries clearly point to HQ upgrade requirements and fast-path planning on the canonical HQ page."
}
```

Next step:

Revisit if the highest-value queries clearly point to HQ upgrade requirements and fast-path planning on the canonical HQ page.

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

Monitor only for now. The very low CTR is notable, but analytics alone do not prove a rewrite need, and the current signal is too weak to justify human review as a priority item. Future trigger: Revisit if query-level evidence shows a stable pattern of combat power search intent tied to this exact page.

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
  "notes": "Monitor only for now. The very low CTR is notable, but analytics alone do not prove a rewrite need, and the current signal is too weak to justify human review as a priority item. Future trigger: Revisit if query-level evidence shows a stable pattern of combat power search intent tied to this exact page."
}
```

Next step:

Revisit if query-level evidence shows a stable pattern of combat power search intent tied to this exact page.
