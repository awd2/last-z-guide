# LLM Topic Discovery - 2026-05-18T19:30:53Z

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

Improves findability for players searching for redeem codes, Gift Center login, and UID guidance without forcing them through a less relevant page.

Rationale:

This is a strong existing-page opportunity with substantial impression volume, low CTR, and a clear query cluster around Gift Center intent. The page already has a known backlog history and an established cornerstone role, so an update review is higher value than new content creation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because Gift Center intent can overlap with other Economy pages if cluster roles are not protected.

Expected route:

- index.html
- codes.html

Claims to verify:

- The page should remain the canonical Gift Center / redeem codes destination.
- The existing claims about Gift Center login and UID flow match current canonical site memory.
- The update can be made without blurring Economy cluster role separation.

Evidence:

- GSC page signal: codes.html had 40033 impressions, 733 clicks, 1.83% CTR, avg position 6.01.
- Low CTR query: `last z gift center` had 3169 impressions, 121 clicks, 3.82% CTR, position 6.58.
- Low CTR query: `last z gift center login` had 903 impressions, 46 clicks, 5.09% CTR, position 5.14.
- Low CTR query: `lastz gift center` had 683 impressions, 29 clicks, 4.25% CTR, position 5.96.
- Low CTR query: `last-z.com gift center` had 508 impressions, 25 clicks, 4.92% CTR, position 6.00.

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
  "source_reference": "GSC weekly 2026-05-17: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This is a strong existing-page opportunity with substantial impression volume, low CTR, and a clear query cluster around Gift Center intent. The page already has a known backlog history and an established cornerstone role, so an update review is higher value than new content creation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review to confirm query intent, protect canonical claims, and define the smallest safe update scope for codes.html.

### alliance-duel-gsc-opportunity

- Title: GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy
- Target: `alliance-duel.html`
- Cluster: `Events`
- Action: `monitor`
- Archetype: `event-guide`
- Priority: `low`
- Risk: `medium`
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:

Helps players quickly find event schedule, day-by-day planning, and versus strategy details for the Alliance Duel event.

Rationale:

The page has meaningful impressions and clicks with a mid-range CTR, suggesting a practical opportunity to improve the first-screen match for schedule-seeking users. It fits the current event-guide archetype and should be reviewed as an existing-page optimization. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because event intent may be shared with other event pages if the scope is not tightly controlled.

Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- The query intent is primarily schedule and strategy related.
- The page is the correct canonical event-guide target.
- The update will not require scope expansion beyond approved event-guide patterns.

Evidence:

- GSC page signal: alliance-duel.html had 8912 impressions, 434 clicks, 4.87% CTR, avg position 6.10.

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
  "source_reference": "GSC weekly 2026-05-17: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "The page has meaningful impressions and clicks with a mid-range CTR, suggesting a practical opportunity to improve the first-screen match for schedule-seeking users. It fits the current event-guide archetype and should be reviewed as an existing-page optimization. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have a human reviewer validate whether alliance-duel.html is the best canonical match for the query set and whether the update stays within template and cluster rules.

### external-gift-center-official-flow-validation

- Title: External source opportunity: official Gift Center and store flow validation
- Target: `gift-center-uid.html`
- Cluster: `Economy`
- Action: `update_existing`
- Archetype: `support-guide`
- Priority: `medium`
- Risk: `medium`
- Confidence: `high`
- Prior review: `none`
- Human approval required: `true`

Player value:

Could improve accuracy for players trying to confirm official Gift Center setup, UID usage, and store flow.

Rationale:

The external official domain is a useful discovery and cross-validation signal for Gift Center routing, but it is not proof by itself. The topic is worth human review because it may confirm or refine existing Economy guidance, provided claims are verified before any apply step.

Duplication risk:

High, because this could duplicate existing Gift Center coverage or copy external wording if not tightly controlled.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Official service routing details are accurate and current.
- Gift Center setup and UID usage are still the correct player flow.
- No canonical claims are being copied from the external source.

Evidence:

- Official service domain is the strongest source for Gift Center routing and redeem/store flow validation.
- External source URL recorded for later manual verification.

Backlog Row Preview:

```json
{
  "topic_id": "external-gift-center-official-flow-validation",
  "title": "External source opportunity: official Gift Center and store flow validation",
  "cluster": "Economy",
  "recommended_action": "update_existing",
  "archetype_suggestion": "support-guide",
  "target_page_or_slug": "gift-center-uid.html",
  "source_type": "llm_scout",
  "source_reference": "official-functap-store: https://last-z.com",
  "confidence": "high",
  "priority": "medium",
  "status": "candidate",
  "notes": "The external official domain is a useful discovery and cross-validation signal for Gift Center routing, but it is not proof by itself. The topic is worth human review because it may confirm or refine existing Economy guidance, provided claims are verified before any apply step."
}
```

Next step:

Route to human verification only, with explicit requirement for canonical memory plus a second reliable source or owner confirmation before any content proposal.

### external-hq-and-progression-reference-cross-check

- Title: External source opportunity: HQ and progression requirement cross-check
- Target: `hq.html`
- Cluster: `Progression`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:



Rationale:

Useful as discovery, but too dependent on a single external reference and too likely to overlap existing HQ/progression coverage without a distinct player job. Future trigger: Reconsider only if owner-confirmed progression data or a second reliable source exposes a clear gap in hq.html. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:



Expected route:

- index.html
- hq.html

Claims to verify:

- None

Evidence:

- Owner-approved wiki/reference source can reveal HQ and progression planning gaps.
- External source URL recorded for later manual verification.

Backlog Row Preview:

```json
{
  "topic_id": "external-hq-and-progression-reference-cross-check",
  "title": "External source opportunity: HQ and progression requirement cross-check",
  "cluster": "Progression",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "hq.html",
  "source_type": "llm_scout",
  "source_reference": "lastzwiki-reference: https://lastzwiki.com",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Useful as discovery, but too dependent on a single external reference and too likely to overlap existing HQ/progression coverage without a distinct player job. Future trigger: Reconsider only if owner-confirmed progression data or a second reliable source exposes a clear gap in hq.html. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider only if owner-confirmed progression data or a second reliable source exposes a clear gap in hq.html.

### external-research-costs-external-cross-check

- Title: External source opportunity: research cost and branch coverage cross-check
- Target: `research-costs.html`
- Cluster: `Research`
- Action: `monitor`
- Archetype: `atlas-page`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:



Rationale:

High verification risk and likely overlap with existing Research coverage; the external source is only a cross-check signal, not enough for a content proposal. Future trigger: Revisit if canonical memory plus another reliable source confirms a specific missing branch or cost-table drift in research-costs.html. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:



Expected route:

- index.html
- research-costs.html

Claims to verify:

- None

Evidence:

- Owner-approved research reference source can reveal branch coverage gaps and cost/name drift.
- External source URL recorded for later manual verification.

Backlog Row Preview:

```json
{
  "topic_id": "external-research-costs-external-cross-check",
  "title": "External source opportunity: research cost and branch coverage cross-check",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "atlas-page",
  "target_page_or_slug": "research-costs.html",
  "source_type": "llm_scout",
  "source_reference": "stresswar-lastz-reference: https://lastz.stresswar.com",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "High verification risk and likely overlap with existing Research coverage; the external source is only a cross-check signal, not enough for a content proposal. Future trigger: Revisit if canonical memory plus another reliable source confirms a specific missing branch or cost-table drift in research-costs.html. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Revisit if canonical memory plus another reliable source confirms a specific missing branch or cost-table drift in research-costs.html.

### external-search-lastz-fandom-reference-event-center-last-z-survival-shooter-wiki--5

- Title: External search opportunity: Event Center | Last Z: Survival Shooter Wiki | Fandom
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

Search result is discovery only and the title suggests possible duplication with existing Research pages rather than a distinct player job. Future trigger: Monitor for a verified research-events gap that cannot be handled by existing research.html coverage.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Hub page for regular and special events, useful for finding where research-linked events are organized.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-event-center-last-z-survival-shooter-wiki--5",
  "title": "External search opportunity: Event Center | Last Z: Survival Shooter Wiki | Fandom",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Search result is discovery only and the title suggests possible duplication with existing Research pages rather than a distinct player job. Future trigger: Monitor for a verified research-events gap that cannot be handled by existing research.html coverage."
}
```

Next step:

Monitor for a verified research-events gap that cannot be handled by existing research.html coverage.

### external-search-lastz-fandom-reference-full-preparedness-last-z-survival-shooter--4

- Title: External search opportunity: Full Preparedness | Last Z: Survival Shooter Wiki | Fandom
- Target: `events.html`
- Cluster: `Events`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

The event description is too thin and verification-dependent to move forward now; it remains a discovery signal only. Future trigger: Reassess if the event has verified structure and a clear fit for events.html after cross-validation.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event page that includes an Age of Science phase for technology research and a Hero Initiative phase for hero upgrades.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-full-preparedness-last-z-survival-shooter--4",
  "title": "External search opportunity: Full Preparedness | Last Z: Survival Shooter Wiki | Fandom",
  "cluster": "Events",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "events.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "The event description is too thin and verification-dependent to move forward now; it remains a discovery signal only. Future trigger: Reassess if the event has verified structure and a clear fit for events.html after cross-validation."
}
```

Next step:

Reassess if the event has verified structure and a clear fit for events.html after cross-validation.

### external-search-lastzwiki-reference-heroes-last-z-wiki-tier-list-stats-complet-1

- Title: External search opportunity: Heroes - Last Z Wiki | Tier List, Stats & Complete Character Guide 2026
- Target: `heroes.html`
- Cluster: `Heroes`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

The hero roster search result is likely duplicative of existing Heroes coverage and cannot be trusted without source validation. Future trigger: Reconsider if owner-approved data shows a real roster or stats gap in heroes.html.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero roster page with faction filters, hero levels, and equipment sections; useful for hero discovery and cross-checking character list.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastzwiki-reference-heroes-last-z-wiki-tier-list-stats-complet-1",
  "title": "External search opportunity: Heroes - Last Z Wiki | Tier List, Stats & Complete Character Guide 2026",
  "cluster": "Heroes",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "heroes.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastzwiki.com/en Last Z guide heroes research",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "The hero roster search result is likely duplicative of existing Heroes coverage and cannot be trusted without source validation. Future trigger: Reconsider if owner-approved data shows a real roster or stats gap in heroes.html."
}
```

Next step:

Reconsider if owner-approved data shows a real roster or stats gap in heroes.html.
