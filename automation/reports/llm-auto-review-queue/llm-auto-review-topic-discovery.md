# LLM Topic Discovery - 2026-05-16T17:32:09Z

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

Better query match for players searching for Gift Center, redeem codes, and UID help, which can improve findability and reduce confusion on an already important page.

Rationale:

This is the clearest on-site opportunity: strong GSC signals show the codes page already ranks and gets significant impressions, while the low CTR queries suggest a query-page fit issue rather than a need for new content. It matches an existing cornerstone guide and a known backlog history, so human review should focus on first-screen usefulness and intent alignment without crossing canonical claim boundaries. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium to high because the query intent may already be served by another canonical page and any rewrite could blur cluster role separation.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the query intent is best served by codes.html or another canonical page
- Whether any page-level changes can be made without altering protected canonical claims
- Whether the improvement stays within approved cornerstone scope

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
  "notes": "This is the clearest on-site opportunity: strong GSC signals show the codes page already ranks and gets significant impressions, while the low CTR queries suggest a query-page fit issue rather than a need for new content. It matches an existing cornerstone guide and a known backlog history, so human review should focus on first-screen usefulness and intent alignment without crossing canonical claim boundaries. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have the owner review whether the page can be improved within current scope while preserving canonical claims and cluster separation.

### external-hq-and-progression-reference-cross-check

- Title: External source opportunity: HQ and progression requirement cross-check
- Target: `hq.html`
- Cluster: `Progression`
- Action: `update_existing`
- Archetype: `cornerstone-guide`
- Priority: `high`
- Risk: `high`
- Confidence: `high`
- Prior review: `none`
- Human approval required: `true`

Player value:

Helps players understand HQ requirements, construction dependencies, and progression planning with fewer mistakes.

Rationale:

This is a useful cross-validation opportunity for HQ progression guidance, but it should only proceed if the external reference can be verified against canonical memory and at least one additional reliable source. The player job is distinct enough to justify human review, and it fits the existing Progression cluster without implying a new page.

Duplication risk:

Medium because it could duplicate existing HQ guidance if the cross-check does not add a distinct planning job.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement thresholds
- Construction dependency order
- Whether the source adds new information beyond existing canonical coverage

Evidence:

- Owner-approved wiki/reference source can reveal HQ and progression planning gaps.
- External source URL recorded for later manual verification.

Backlog Row Preview:

```json
{
  "topic_id": "external-hq-and-progression-reference-cross-check",
  "title": "External source opportunity: HQ and progression requirement cross-check",
  "cluster": "Progression",
  "recommended_action": "update_existing",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "hq.html",
  "source_type": "llm_scout",
  "source_reference": "lastzwiki-reference: https://lastzwiki.com",
  "confidence": "high",
  "priority": "high",
  "status": "candidate",
  "notes": "This is a useful cross-validation opportunity for HQ progression guidance, but it should only proceed if the external reference can be verified against canonical memory and at least one additional reliable source. The player job is distinct enough to justify human review, and it fits the existing Progression cluster without implying a new page."
}
```

Next step:

Verify the external claims against canonical sources and confirm whether hq.html needs a scoped update or only a note for follow-up.

### external-research-costs-external-cross-check

- Title: External source opportunity: research cost and branch coverage cross-check
- Target: `research-costs.html`
- Cluster: `Research`
- Action: `update_existing`
- Archetype: `atlas-page`
- Priority: `high`
- Risk: `high`
- Confidence: `high`
- Prior review: `none`
- Human approval required: `true`

Player value:

Reduces planning errors by helping players avoid outdated research costs, missing branches, and naming conflicts.

Rationale:

This is a strong candidate for human review because research cost and branch coverage drift are practical player pain points, and the topic aligns with an existing Research page instead of suggesting a new structure. However, the external source is only a discovery signal, so the claims need independent verification before any content work is considered.

Duplication risk:

Medium because it may overlap with existing research tables or branch coverage pages if the verified scope is narrow.

Expected route:

- index.html
- research-costs.html

Claims to verify:

- Research cost tables
- Branch coverage completeness
- Branch naming consistency

Evidence:

- Owner-approved research reference source can reveal branch coverage gaps and cost/name drift.
- External source URL recorded for later manual verification.

Backlog Row Preview:

```json
{
  "topic_id": "external-research-costs-external-cross-check",
  "title": "External source opportunity: research cost and branch coverage cross-check",
  "cluster": "Research",
  "recommended_action": "update_existing",
  "archetype_suggestion": "atlas-page",
  "target_page_or_slug": "research-costs.html",
  "source_type": "llm_scout",
  "source_reference": "stresswar-lastz-reference: https://lastz.stresswar.com",
  "confidence": "high",
  "priority": "high",
  "status": "candidate",
  "notes": "This is a strong candidate for human review because research cost and branch coverage drift are practical player pain points, and the topic aligns with an existing Research page instead of suggesting a new structure. However, the external source is only a discovery signal, so the claims need independent verification before any content work is considered."
}
```

Next step:

Cross-check the research cost and branch data against canonical memory and a second reliable source before deciding whether research-costs.html needs an update.

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

Useful as a validation signal, but it depends on a single external source and does not yet prove a distinct player job beyond existing Gift Center coverage. Future trigger: Revisit if official routing or UID flow is confirmed by a second reliable source or owner confirmation.

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
  "notes": "Useful as a validation signal, but it depends on a single external source and does not yet prove a distinct player job beyond existing Gift Center coverage. Future trigger: Revisit if official routing or UID flow is confirmed by a second reliable source or owner confirmation."
}
```

Next step:

Revisit if official routing or UID flow is confirmed by a second reliable source or owner confirmation.

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

Monitor only. The event claim is derived from an external search result and is not yet verified enough to support a page update. Future trigger: Revisit when event mechanics, theme rotation, or rewards are confirmed by canonical memory plus a second source.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle includes an Age of Science theme for technology research and a Hero Initiative theme for hero leveling and recruitment items.

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
  "notes": "Monitor only. The event claim is derived from an external search result and is not yet verified enough to support a page update. Future trigger: Revisit when event mechanics, theme rotation, or rewards are confirmed by canonical memory plus a second source."
}
```

Next step:

Revisit when event mechanics, theme rotation, or rewards are confirmed by canonical memory plus a second source.

### external-search-lastz-fandom-reference-heroes-last-z-survival-shooter-wiki-fandom-5

- Title: External search opportunity: Heroes | Last Z: Survival Shooter Wiki | Fandom
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

Monitor only. This is a general hero index signal and may duplicate existing hero coverage without adding a distinct player job. Future trigger: Revisit if a verified gap appears in hero class coverage, growth mechanics, or roster navigation.

Duplication risk:



Expected route:

- index.html

Claims to verify:

- None

Evidence:

- Core hero index page; describes hero classes and the main hero power factors used for cross-checking hero growth mechanics.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-heroes-last-z-survival-shooter-wiki-fandom-5",
  "title": "External search opportunity: Heroes | Last Z: Survival Shooter Wiki | Fandom",
  "cluster": "Home",
  "recommended_action": "monitor",
  "archetype_suggestion": "home-hub",
  "target_page_or_slug": "index.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor only. This is a general hero index signal and may duplicate existing hero coverage without adding a distinct player job. Future trigger: Revisit if a verified gap appears in hero class coverage, growth mechanics, or roster navigation."
}
```

Next step:

Revisit if a verified gap appears in hero class coverage, growth mechanics, or roster navigation.

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

Monitor only. The source looks like a broad hero guide and could easily copy competitor framing or overlap with existing hero pages without new value. Future trigger: Revisit if a verified hero roster or stats gap is identified and can be covered without copying wording.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero roster and equipment page with character list, faction filters, levels, and gear stats; good for hero discovery and cross-checking hero names.

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
  "notes": "Monitor only. The source looks like a broad hero guide and could easily copy competitor framing or overlap with existing hero pages without new value. Future trigger: Revisit if a verified hero roster or stats gap is identified and can be covered without copying wording."
}
```

Next step:

Revisit if a verified hero roster or stats gap is identified and can be covered without copying wording.

### external-search-lastzwiki-reference-laboratory-badges-in-last-z-complete-resea-2

- Title: External search opportunity: Laboratory Badges in Last Z - Complete Research Guide | Last Z Wiki
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

Monitor only. Research tables can be high-risk for copy and drift, and this source is not enough to justify an update by itself. Future trigger: Revisit if laboratory badge costs are confirmed against canonical data and an owner approves the scope.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page showing laboratory categories and per-level badge costs; useful for finding research paths and cost tables.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastzwiki-reference-laboratory-badges-in-last-z-complete-resea-2",
  "title": "External search opportunity: Laboratory Badges in Last Z - Complete Research Guide | Last Z Wiki",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastzwiki.com/en Last Z guide heroes research",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor only. Research tables can be high-risk for copy and drift, and this source is not enough to justify an update by itself. Future trigger: Revisit if laboratory badge costs are confirmed against canonical data and an owner approves the scope."
}
```

Next step:

Revisit if laboratory badge costs are confirmed against canonical data and an owner approves the scope.
