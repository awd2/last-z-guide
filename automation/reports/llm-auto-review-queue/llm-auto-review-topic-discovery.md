# LLM Topic Discovery - 2026-05-16T18:50:42Z

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

Better first-screen match for players searching redeem codes, Gift Center login, and UID-related help.

Rationale:

This is the strongest opportunity because it combines a high-impression page signal with several low-CTR gift center queries that clearly point to a query-to-page mismatch. The page already exists as a cornerstone guide, so the safest path is to improve the existing asset rather than create new content. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low to medium. The topic is on the correct existing page, but changes must preserve cluster role separation and protected canonical claims.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the current page already satisfies the Gift Center and redeem intent.
- Whether any proposed content change would blur the Economy cluster role separation.
- Whether the low CTR is caused by snippet mismatch, page layout, or intent mismatch rather than content gaps.

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
  "notes": "This is the strongest opportunity because it combines a high-impression page signal with several low-CTR gift center queries that clearly point to a query-to-page mismatch. The page already exists as a cornerstone guide, so the safest path is to improve the existing asset rather than create new content. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for an existing-page scope check against the approved template and protected claims.

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

Helps players confirm official routing, UID usage, and setup steps without relying on stale or confusing guidance.

Rationale:

The official service domain is a useful cross-validation signal for Gift Center routing and store flow, but it is not proof on its own. The topic could support a useful update to an existing page if claims are verified and scoped narrowly.

Duplication risk:

Medium. It appears adjacent to an existing Gift Center page intent and could duplicate or blur the same user job if not handled carefully.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Official Gift Center routing and whether it is still current.
- UID usage steps and whether they remain valid.
- Whether this topic adds a distinct player job beyond the existing Gift Center page.

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
  "notes": "The official service domain is a useful cross-validation signal for Gift Center routing and store flow, but it is not proof on its own. The topic could support a useful update to an existing page if claims are verified and scoped narrowly."
}
```

Next step:

Hold for verification against canonical site memory plus one additional reliable source or owner confirmation before any content proposal.

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

Improves progression planning, construction dependency accuracy, and HQ requirement confidence.

Rationale:

HQ planning and dependency verification is a plausible player job, but the external wiki reference is discovery only. This is worth human review because progression accuracy can create real player frustration if stale. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium to high. It may overlap with existing progression coverage unless the exact gap is clearly defined.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement details.
- Construction dependency ordering.
- Whether the referenced source matches current game state and not outdated wiki content.

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
  "notes": "HQ planning and dependency verification is a plausible player job, but the external wiki reference is discovery only. This is worth human review because progression accuracy can create real player frustration if stale. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Require manual validation of the referenced claims and compare against current canonical progression coverage before accepting any scope.

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

Useful discovery signal, but the claim set is too dependent on one external reference and could copy competitor framing. It should not advance until verified with stronger sources or owner confirmation. Future trigger: Revisit if a second reliable source or canonical owner confirmation validates the research cost and branch coverage gaps. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful discovery signal, but the claim set is too dependent on one external reference and could copy competitor framing. It should not advance until verified with stronger sources or owner confirmation. Future trigger: Revisit if a second reliable source or canonical owner confirmation validates the research cost and branch coverage gaps. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Revisit if a second reliable source or canonical owner confirmation validates the research cost and branch coverage gaps.

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

External search result is discovery only and is too thin to justify advancement without verified, distinct player value. It also risks duplicating existing event coverage. Future trigger: Reassess if a verified event mechanic gap appears that is not already covered by the current events page.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event page with a specific research-themed cycle and hero-related scoring tasks; useful for event mechanics cross-checks.

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
  "notes": "External search result is discovery only and is too thin to justify advancement without verified, distinct player value. It also risks duplicating existing event coverage. Future trigger: Reassess if a verified event mechanic gap appears that is not already covered by the current events page."
}
```

Next step:

Reassess if a verified event mechanic gap appears that is not already covered by the current events page.

### external-search-lastz-fandom-reference-heroes-last-z-survival-shooter-wiki-fandom-5

- Title: External search opportunity: Heroes | Last Z: Survival Shooter Wiki | Fandom
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

This looks duplicate-adjacent to the existing research/hero taxonomy surface and is not yet clearly distinct enough for a new or updated page decision. Future trigger: Revisit if a specific missing hero taxonomy or system page gap is confirmed by owner review and source validation.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page; useful for hero taxonomy, power factors, and links into hero systems.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-heroes-last-z-survival-shooter-wiki-fandom-5",
  "title": "External search opportunity: Heroes | Last Z: Survival Shooter Wiki | Fandom",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This looks duplicate-adjacent to the existing research/hero taxonomy surface and is not yet clearly distinct enough for a new or updated page decision. Future trigger: Revisit if a specific missing hero taxonomy or system page gap is confirmed by owner review and source validation."
}
```

Next step:

Revisit if a specific missing hero taxonomy or system page gap is confirmed by owner review and source validation.

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

The external search result is promising but still speculative and heavily source-dependent. It should remain on hold until claims about badge costs and research tables are verified. Future trigger: Reassess after confirmation of current badge costs, level tables, and whether the page would add unique value beyond existing research coverage.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page covering laboratory categories and badge costs per level, including T10-related research.

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
  "notes": "The external search result is promising but still speculative and heavily source-dependent. It should remain on hold until claims about badge costs and research tables are verified. Future trigger: Reassess after confirmation of current badge costs, level tables, and whether the page would add unique value beyond existing research coverage."
}
```

Next step:

Reassess after confirmation of current badge costs, level tables, and whether the page would add unique value beyond existing research coverage.

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

This appears to be a new hero hub idea, but it is not yet verified as distinct enough from existing hero and research coverage. The topic also carries high duplication risk if it mirrors competitor structure too closely. Future trigger: Consider if a verified hero-system gap emerges that cannot be served by current pages and if the outline can be made clearly unique. 

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero hub with character list, equipment section, and likely entry point for hero builds and stats.

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
  "notes": "This appears to be a new hero hub idea, but it is not yet verified as distinct enough from existing hero and research coverage. The topic also carries high duplication risk if it mirrors competitor structure too closely. Future trigger: Consider if a verified hero-system gap emerges that cannot be served by current pages and if the outline can be made clearly unique. "
}
```

Next step:

Consider if a verified hero-system gap emerges that cannot be served by current pages and if the outline can be made clearly unique.
