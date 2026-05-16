# LLM Topic Discovery - 2026-05-16T17:05:08Z

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

Improve the match between search intent and the existing redeem-codes page so players can find gift center, login, and UID help faster.

Rationale:

This is the clearest on-site signal with strong query and page data, and it aligns to an existing cornerstone guide rather than a new page. The intent is specific enough to justify human review, while still respecting cluster role separation and protected canonical claims. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because the topic already exists as a cornerstone page and must not drift into a duplicate or role-blurring rewrite.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the low CTR queries reflect a true page mismatch or normal SERP noise
- Whether codes.html can cover gift center and UID intent without violating canonical claim boundaries
- Whether the existing page already satisfies the current user job better than a broader rewrite

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
  "notes": "This is the clearest on-site signal with strong query and page data, and it aligns to an existing cornerstone guide rather than a new page. The intent is specific enough to justify human review, while still respecting cluster role separation and protected canonical claims. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have an owner review the query set against the current codes.html scope and confirm whether a scoped update is warranted.

### external-gift-center-official-flow-validation

- Title: External source opportunity: official Gift Center and store flow validation
- Target: `gift-center-uid.html`
- Cluster: `Economy`
- Action: `update_existing`
- Archetype: `support-guide`
- Priority: `high`
- Risk: `medium`
- Confidence: `high`
- Prior review: `none`
- Human approval required: `true`

Player value:

Reduce confusion around Gift Center setup, UID usage, and official routing so players do not get misdirected.

Rationale:

The official service domain is a plausible validation source for routing and flow accuracy, but it is not proof on its own. The topic maps to an existing support-style page and is useful as a cross-check opportunity for human review.

Duplication risk:

Medium, because it may overlap with other Gift Center or redeem flow pages if the intent is not narrowly defined.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Exact Gift Center routing on the official domain
- Whether UID usage is part of the public player flow or a support-specific detail
- Whether this topic adds a distinct player job beyond the existing redeem guidance

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
  "priority": "high",
  "status": "candidate",
  "notes": "The official service domain is a plausible validation source for routing and flow accuracy, but it is not proof on its own. The topic maps to an existing support-style page and is useful as a cross-check opportunity for human review."
}
```

Next step:

Verify the public flow against canonical site memory and one additional reliable source before deciding whether the existing page needs adjustment.

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

Help players verify HQ requirement planning and dependency coverage before they invest resources.

Rationale:

This is a credible cross-check topic for progression planning and HQ requirements, but it depends on external validation and owner confirmation. It fits the current HQ page rather than a new page, so it is worth human review as an update_existing candidate.

Duplication risk:

Medium, because HQ and progression topics can easily overlap with broader base-building content if scope is not controlled.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement and dependency details
- Whether the reference source reflects current game state
- Whether the topic is distinct from existing progression guidance

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
  "notes": "This is a credible cross-check topic for progression planning and HQ requirements, but it depends on external validation and owner confirmation. It fits the current HQ page rather than a new page, so it is worth human review as an update_existing candidate."
}
```

Next step:

Cross-verify HQ requirement claims against canonical memory and a second reliable source before any content proposal is shaped.

### external-research-costs-external-cross-check

- Title: External source opportunity: research cost and branch coverage cross-check
- Target: `research-costs.html`
- Cluster: `Research`
- Action: `monitor`
- Archetype: `atlas-page`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

Useful as a cross-validation signal, but the topic is too dependent on a single external reference and risks claim drift on costs and branches. Future trigger: Move forward only if a second reliable source or owner confirmation validates the branch and cost data.

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
  "notes": "Useful as a cross-validation signal, but the topic is too dependent on a single external reference and risks claim drift on costs and branches. Future trigger: Move forward only if a second reliable source or owner confirmation validates the branch and cost data."
}
```

Next step:

Move forward only if a second reliable source or owner confirmation validates the branch and cost data.

### external-search-lastz-fandom-reference-full-preparedness-4

- Title: External search opportunity: Full Preparedness
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

The search result is discovery-only and references event claims that cannot be trusted without stronger validation. Future trigger: Reconsider if canonical memory plus another reliable source confirms the event mechanics and rotation details.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event with rotating cycles; one theme rewards tech research speed-ups and another rewards hero upgrades/recruitment items.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-full-preparedness-4",
  "title": "External search opportunity: Full Preparedness",
  "cluster": "Events",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "events.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "The search result is discovery-only and references event claims that cannot be trusted without stronger validation. Future trigger: Reconsider if canonical memory plus another reliable source confirms the event mechanics and rotation details."
}
```

Next step:

Reconsider if canonical memory plus another reliable source confirms the event mechanics and rotation details.

### external-search-lastz-fandom-reference-heroes-5

- Title: External search opportunity: Heroes
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

The topic is broadly useful but currently functions as a generic cross-reference rather than a distinct, verified player job. Future trigger: Revisit if there is verified evidence that the existing tech or hero page is missing a specific, user-facing gap.

Duplication risk:



Expected route:

- tech.html

Claims to verify:

- None

Evidence:

- Core hero overview page with hero types and what affects hero power, including tech-related boosts.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-heroes-5",
  "title": "External search opportunity: Heroes",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "tech.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "The topic is broadly useful but currently functions as a generic cross-reference rather than a distinct, verified player job. Future trigger: Revisit if there is verified evidence that the existing tech or hero page is missing a specific, user-facing gap."
}
```

Next step:

Revisit if there is verified evidence that the existing tech or hero page is missing a specific, user-facing gap.

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

This is too close to a generic roster/tier-list discovery signal and could duplicate existing hero content intent without a verified gap. Future trigger: Consider only after confirming a unique player task that the current heroes page does not already solve.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero roster and equipment page; useful for hero discovery, faction grouping, and gear lookup.

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
  "notes": "This is too close to a generic roster/tier-list discovery signal and could duplicate existing hero content intent without a verified gap. Future trigger: Consider only after confirming a unique player task that the current heroes page does not already solve."
}
```

Next step:

Consider only after confirming a unique player task that the current heroes page does not already solve.

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

The research table topic is likely overlapping with existing research coverage and depends on source validation for costs and badge totals. Future trigger: Promote only if a verified data drift or missing branch coverage issue is confirmed.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page with categories, level costs, and badge totals; useful for research discovery and cross-checking.

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
  "notes": "The research table topic is likely overlapping with existing research coverage and depends on source validation for costs and badge totals. Future trigger: Promote only if a verified data drift or missing branch coverage issue is confirmed."
}
```

Next step:

Promote only if a verified data drift or missing branch coverage issue is confirmed.
