# LLM Topic Discovery - 2026-05-17T10:01:15Z

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

Help players find the correct Gift Center and redeem-code flow faster, especially when searching for login, UID, or Gift Center routing terms.

Rationale:

This has the clearest on-site demand signal. The page already exists, the query set shows meaningful impressions with weak CTR, and the topic fits the current cornerstone guide role. It is a strong candidate for human review because the gap appears to be query-to-page matching rather than a new content need. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. The topic could overlap with another redeem or login help page if intent is not tightly scoped.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the low CTR queries reflect a true page mismatch rather than normal SERP volatility.
- Whether any title or intro adjustments stay within approved scope.
- Whether the protected canonical claims remain intact and unchanged.

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
  "notes": "This has the clearest on-site demand signal. The page already exists, the query set shows meaningful impressions with weak CTR, and the topic fits the current cornerstone guide role. It is a strong candidate for human review because the gap appears to be query-to-page matching rather than a new content need. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should confirm whether the existing page can address the query set without changing canonical claims or blurring cluster separation.

### external-hq-and-progression-reference-cross-check

- Title: External source opportunity: HQ and progression requirement cross-check
- Target: `hq.html`
- Cluster: `Progression`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: `high`
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:

Reduce planning mistakes by clarifying HQ requirements, dependencies, and route order.

Rationale:

This is a plausible support update for an existing progression page, but it depends on external verification. The proposal is useful because it points to a distinct player job: checking HQ requirements and progression dependencies before planning upgrades. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. It may duplicate an existing HQ or progression overview unless the review finds a distinct gap.

Expected route:

- index.html
- hq.html

Claims to verify:

- Exact HQ requirement and dependency claims.
- Whether the external source adds new verified information beyond existing coverage.
- Whether the page can be updated without introducing unsupported mechanics or roadmap claims.

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
  "notes": "This is a plausible support update for an existing progression page, but it depends on external verification. The proposal is useful because it points to a distinct player job: checking HQ requirements and progression dependencies before planning upgrades. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should verify the claims against canonical memory and at least one additional reliable source before any proposal is drafted.

### external-research-costs-external-cross-check

- Title: External source opportunity: research cost and branch coverage cross-check
- Target: `research-costs.html`
- Cluster: `Research`
- Action: `monitor`
- Archetype: `atlas-page`
- Priority: `low`
- Risk: `high`
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:

Help players avoid stale cost planning and missing branch coverage when researching upgrades.

Rationale:

This is a strong cross-validation candidate for the Research costs page because it targets branch coverage, cost drift, and naming conflicts. It is worth review, but only as a verification-driven update, not as a copy source. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. Could overlap with existing research or tech pages if the scope is not narrowly defined.

Expected route:

- index.html
- research-costs.html

Claims to verify:

- Branch coverage and cost-table details.
- Whether any naming drift is real and relevant.
- Whether the topic is already covered on another page.

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
  "notes": "This is a strong cross-validation candidate for the Research costs page because it targets branch coverage, cost drift, and naming conflicts. It is worth review, but only as a verification-driven update, not as a copy source. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Verify the external reference against internal canonical knowledge and a second reliable source before considering a content proposal.

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

Useful as a verification signal, but it is too dependent on a single external source and risks duplicating the existing Gift Center/Codes intent. It should not advance without stronger validation. Future trigger: Reconsider if owner confirmation or a second reliable source confirms a distinct Gift Center routing or store-flow gap.

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
  "notes": "Useful as a verification signal, but it is too dependent on a single external source and risks duplicating the existing Gift Center/Codes intent. It should not advance without stronger validation. Future trigger: Reconsider if owner confirmation or a second reliable source confirms a distinct Gift Center routing or store-flow gap."
}
```

Next step:

Reconsider if owner confirmation or a second reliable source confirms a distinct Gift Center routing or store-flow gap.

### external-search-lastz-fandom-reference-bookstore-last-z-survival-shooter-wiki-fan-6

- Title: External search opportunity: Bookstore | Last Z: Survival Shooter Wiki | Fandom
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

The search result is discovery-only and the claim is too thin to support a page decision without stronger verification. It may also duplicate existing research coverage. Future trigger: Reconsider if canonical memory and another source confirm a distinct Research page gap around Bookstore or related upgrade paths.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Bonus building that increases research speed and has upgrade data.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-bookstore-last-z-survival-shooter-wiki-fan-6",
  "title": "External search opportunity: Bookstore | Last Z: Survival Shooter Wiki | Fandom",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "The search result is discovery-only and the claim is too thin to support a page decision without stronger verification. It may also duplicate existing research coverage. Future trigger: Reconsider if canonical memory and another source confirm a distinct Research page gap around Bookstore or related upgrade paths."
}
```

Next step:

Reconsider if canonical memory and another source confirm a distinct Research page gap around Bookstore or related upgrade paths.

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

The result is a discovery signal for events, but the description is too generic and likely overlaps with existing event coverage. It is not ready for human review as a distinct opportunity. Future trigger: Reconsider if validated timing, reward, or cycle data shows a real gap not already covered on events.html.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event overview with a research-themed round and a hero-upgrade round, plus reward tables and cycle timing.

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
  "notes": "The result is a discovery signal for events, but the description is too generic and likely overlaps with existing event coverage. It is not ready for human review as a distinct opportunity. Future trigger: Reconsider if validated timing, reward, or cycle data shows a real gap not already covered on events.html."
}
```

Next step:

Reconsider if validated timing, reward, or cycle data shows a real gap not already covered on events.html.

### external-search-lastz-fandom-reference-laboratory-last-z-survival-shooter-wiki-fa-5

- Title: External search opportunity: Laboratory | Last Z: Survival Shooter Wiki | Fandom
- Target: `tech.html`
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

This appears to be a generic building reference and is not yet a distinct content opportunity. It also carries high duplication risk with the existing tech page. Future trigger: Reconsider if verified claims show missing tech unlock or upgrade coverage that cannot be handled within the current page.

Duplication risk:



Expected route:

- tech.html

Claims to verify:

- None

Evidence:

- Core building page for unlocking and upgrading tech research.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-laboratory-last-z-survival-shooter-wiki-fa-5",
  "title": "External search opportunity: Laboratory | Last Z: Survival Shooter Wiki | Fandom",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "tech.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This appears to be a generic building reference and is not yet a distinct content opportunity. It also carries high duplication risk with the existing tech page. Future trigger: Reconsider if verified claims show missing tech unlock or upgrade coverage that cannot be handled within the current page."
}
```

Next step:

Reconsider if verified claims show missing tech unlock or upgrade coverage that cannot be handled within the current page.

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

This is a broad hero roster/tier-list discovery signal and may conflict with existing hero roster or tier content. It needs stronger differentiation before review. Future trigger: Reconsider if a specific missing player job emerges, such as equipment filtering, faction sorting, or roster coverage that is not already present.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero roster page with character list, hero equipment, and faction/filter views. Good lead for hero discovery and equipment cross-checks.

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
  "notes": "This is a broad hero roster/tier-list discovery signal and may conflict with existing hero roster or tier content. It needs stronger differentiation before review. Future trigger: Reconsider if a specific missing player job emerges, such as equipment filtering, faction sorting, or roster coverage that is not already present."
}
```

Next step:

Reconsider if a specific missing player job emerges, such as equipment filtering, faction sorting, or roster coverage that is not already present.
