# LLM Topic Discovery - 2026-05-19T09:28:16Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`
- Source Scout request: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`
- Topics: 7
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

Faster access to redeem-code, Gift Center login, and UID guidance from the canonical codes page.

Rationale:

High volume GSC signals show strong demand around Gift Center and redeem-code intents, and the proposal fits an existing cornerstone page. It is the clearest candidate for improving query-to-page match without changing site structure. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. Gift Center and redeem flows may overlap with existing economy or UID coverage, so role separation must be checked.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether codes.html is still the best canonical page for Gift Center and redeem-code intent
- Whether the update can avoid blurring Gift Center routing with mailbox or rewards claims
- Whether any phrasing changes stay within approved scope for a cornerstone page

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
  "notes": "High volume GSC signals show strong demand around Gift Center and redeem-code intents, and the proposal fits an existing cornerstone page. It is the clearest candidate for improving query-to-page match without changing site structure. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review to confirm canonical claims, preserve cluster separation, and define a narrow update scope for codes.html.

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

Clearer event timing and strategy guidance for players searching for Last Z Alliance Duel scheduling and prep info.

Rationale:

This is a strong page-level opportunity because the existing alliance-duel.html already ranks and receives meaningful impressions, but the user intent around schedule and VS strategy can likely be better served on the same page. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. Event guide coverage could overlap with a broader events hub or another event page if scope is not controlled.

Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- Whether alliance-duel.html remains the best canonical page for the query cluster
- Whether the intended update can be expressed without changing a cornerstone page beyond scope
- Whether event role separation with the main events hub stays intact

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
  "notes": "This is a strong page-level opportunity because the existing alliance-duel.html already ranks and receives meaningful impressions, but the user intent around schedule and VS strategy can likely be better served on the same page. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review to validate that the page remains the right canonical destination and that any improvement stays within the event-guide template.

### external-gift-center-official-flow-validation

- Title: External source opportunity: official Gift Center and store flow validation
- Target: `gift-center-uid.html`
- Cluster: `Economy`
- Action: `monitor`
- Archetype: `support-guide`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

Useful as a verification lead, but it depends on one external source and does not yet meet the standard for a ready review item. It also risks overlapping with the codes page intent. Future trigger: Move forward only after owner confirmation or a second reliable source verifies the Gift Center routing and redeem flow claims.

Duplication risk:



Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- None

Evidence:

- Official service domain is the strongest source for Gift Center routing and redeem/store flow validation.
- External source URL recorded for later manual verification.

Backlog Row Preview:

```json
{
  "topic_id": "external-gift-center-official-flow-validation",
  "title": "External source opportunity: official Gift Center and store flow validation",
  "cluster": "Economy",
  "recommended_action": "monitor",
  "archetype_suggestion": "support-guide",
  "target_page_or_slug": "gift-center-uid.html",
  "source_type": "llm_scout",
  "source_reference": "official-functap-store: https://last-z.com",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Useful as a verification lead, but it depends on one external source and does not yet meet the standard for a ready review item. It also risks overlapping with the codes page intent. Future trigger: Move forward only after owner confirmation or a second reliable source verifies the Gift Center routing and redeem flow claims."
}
```

Next step:

Move forward only after owner confirmation or a second reliable source verifies the Gift Center routing and redeem flow claims.

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

This is a discovery signal only. The claim set is not verified and could duplicate existing progression coverage. Future trigger: Reconsider if canonical HQ requirements or progression dependencies are confirmed by a reliable second source or owner memory. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "This is a discovery signal only. The claim set is not verified and could duplicate existing progression coverage. Future trigger: Reconsider if canonical HQ requirements or progression dependencies are confirmed by a reliable second source or owner memory. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if canonical HQ requirements or progression dependencies are confirmed by a reliable second source or owner memory.

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

External reference only, with risk of cost-table drift and branch-name duplication. Not ready for human review as a content opportunity. Future trigger: Promote only after cross-checking against canonical site memory and another reliable source. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "External reference only, with risk of cost-table drift and branch-name duplication. Not ready for human review as a content opportunity. Future trigger: Promote only after cross-checking against canonical site memory and another reliable source. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Promote only after cross-checking against canonical site memory and another reliable source.

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

Search-result discovery only. It is speculative, source wording should not be copied, and the topic may duplicate broader events coverage. Future trigger: Only revisit if the event mechanics and reward claims can be verified and mapped to a distinct player job.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event page with a research-focused cycle called Age of Science, plus hero upgrade and reward details.

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
  "notes": "Search-result discovery only. It is speculative, source wording should not be copied, and the topic may duplicate broader events coverage. Future trigger: Only revisit if the event mechanics and reward claims can be verified and mapped to a distinct player job."
}
```

Next step:

Only revisit if the event mechanics and reward claims can be verified and mapped to a distinct player job.

### external-search-lastz-fandom-reference-laboratory-last-z-survival-shooter-wiki-fa-5

- Title: External search opportunity: Laboratory | Last Z: Survival Shooter Wiki | Fandom
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

Search-result discovery only. It is not verified and appears to map to existing research coverage rather than a distinct new need. Future trigger: Revisit only if a verified gap exists in research mechanics or unlock coverage.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core building page for technology research and unlocks; useful for mechanics cross-checking.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-laboratory-last-z-survival-shooter-wiki-fa-5",
  "title": "External search opportunity: Laboratory | Last Z: Survival Shooter Wiki | Fandom",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Search-result discovery only. It is not verified and appears to map to existing research coverage rather than a distinct new need. Future trigger: Revisit only if a verified gap exists in research mechanics or unlock coverage."
}
```

Next step:

Revisit only if a verified gap exists in research mechanics or unlock coverage.
