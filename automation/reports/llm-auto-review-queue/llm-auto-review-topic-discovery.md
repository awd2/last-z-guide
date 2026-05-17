# LLM Topic Discovery - 2026-05-17T09:25:27Z

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

Players searching for Gift Center and redeem-code help should get a faster path to the correct flow, with less confusion around login, UID, and redeem steps.

Rationale:

This is a strong existing-page opportunity with clear GSC signals and an existing cornerstone route. The query set suggests mismatch between search intent and current snippet or first-screen utility, but the change should stay within the approved template and preserve cluster separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. The topic is close to current codes coverage, so scope must avoid overlapping with other canonical economy pages.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the current page already fully serves the Gift Center login intent
- Whether any snippet or heading changes would blur role separation
- Whether the protected canonical claims remain accurate and unchanged

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
  "notes": "This is a strong existing-page opportunity with clear GSC signals and an existing cornerstone route. The query set suggests mismatch between search intent and current snippet or first-screen utility, but the change should stay within the approved template and preserve cluster separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have an owner review the current codes page intent, confirm the exact query segments worth addressing, and define a narrow update scope that keeps canonical claims intact.

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

Players get more reliable HQ planning, fewer dependency mistakes, and better progression guidance.

Rationale:

This is a useful cross-check opportunity for an existing progression page. The proposal points to verification of HQ requirements and dependency planning, which can help fill coverage gaps, but all claims are external-source driven and need independent confirmation. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. It may overlap with other progression guidance unless the distinct player job is kept narrow.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement thresholds
- Construction dependency order
- Any route or progression claims implied by the source

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
  "notes": "This is a useful cross-check opportunity for an existing progression page. The proposal points to verification of HQ requirements and dependency planning, which can help fill coverage gaps, but all claims are external-source driven and need independent confirmation. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Verify HQ requirement data against canonical memory and at least one additional reliable source before deciding whether a focused update is warranted.

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

Players and planners get more dependable research cost references and fewer outdated branch assumptions.

Rationale:

This is a strong research-coverage verification task for an existing page. It appears valuable for catching branch coverage and cost drift, but the external source is only a discovery signal, not proof. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. It could overlap with existing research tables unless scoped to a clear gap or drift fix.

Expected route:

- index.html
- research-costs.html

Claims to verify:

- Research branch names
- Research cost values
- Coverage gaps in the current table

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
  "notes": "This is a strong research-coverage verification task for an existing page. It appears valuable for catching branch coverage and cost drift, but the external source is only a discovery signal, not proof. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Cross-validate branch names and cost tables against canonical site memory and another reliable source before any content proposal is drafted.

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

Monitor only until the official-domain claims are verified by a second reliable source or owner confirmation. As written, it is too dependent on a single external source and could duplicate existing economy coverage. Future trigger: Move forward only if independent verification confirms a distinct player job for Gift Center routing or UID flow.

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
  "notes": "Monitor only until the official-domain claims are verified by a second reliable source or owner confirmation. As written, it is too dependent on a single external source and could duplicate existing economy coverage. Future trigger: Move forward only if independent verification confirms a distinct player job for Gift Center routing or UID flow."
}
```

Next step:

Move forward only if independent verification confirms a distinct player job for Gift Center routing or UID flow.

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

Monitor only. The event reference is too source-dependent and may duplicate an existing events page job. It cannot advance without verification of the event theme and relevance. Future trigger: Consider again if canonical memory and a second source confirm a distinct Events coverage gap.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycles include an Age of Science theme for research actions and a Hero Initiative theme for hero upgrades.

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
  "notes": "Monitor only. The event reference is too source-dependent and may duplicate an existing events page job. It cannot advance without verification of the event theme and relevance. Future trigger: Consider again if canonical memory and a second source confirm a distinct Events coverage gap."
}
```

Next step:

Consider again if canonical memory and a second source confirm a distinct Events coverage gap.

### external-search-lastz-fandom-reference-heroes-5

- Title: External search opportunity: Heroes
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

Monitor only. The page appears broad and potentially duplicative of existing research or hero coverage, and the source is not enough to justify a new or updated page yet. Future trigger: Reassess if a distinct player job emerges, such as event scoring linkage or roster comparison, backed by verification.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Main hero roster page with hero classes and power factors; useful for linking hero upgrade mechanics to event scoring.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-heroes-5",
  "title": "External search opportunity: Heroes",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor only. The page appears broad and potentially duplicative of existing research or hero coverage, and the source is not enough to justify a new or updated page yet. Future trigger: Reassess if a distinct player job emerges, such as event scoring linkage or roster comparison, backed by verification."
}
```

Next step:

Reassess if a distinct player job emerges, such as event scoring linkage or roster comparison, backed by verification.

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

Reject for now. The proposal is too close to generic hero roster content and risks copying competitor framing. The source is not sufficient proof for a public-facing guide. Future trigger: Only revisit if owner-approved cross-validation reveals a unique hero-use case not already covered elsewhere.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero roster and equipment catalog; useful for hero discovery, faction filtering, and gear cross-checks.

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
  "notes": "Reject for now. The proposal is too close to generic hero roster content and risks copying competitor framing. The source is not sufficient proof for a public-facing guide. Future trigger: Only revisit if owner-approved cross-validation reveals a unique hero-use case not already covered elsewhere."
}
```

Next step:

Only revisit if owner-approved cross-validation reveals a unique hero-use case not already covered elsewhere.

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

Monitor only. It may be useful for research discovery, but the claim set is entirely external-source based and needs stronger validation before any review workflow advances. Future trigger: Reassess if badge costs and research tables are confirmed by canonical memory or another reliable source.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research tables by category with badge costs per level; useful for research discovery and cost cross-checking.

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
  "notes": "Monitor only. It may be useful for research discovery, but the claim set is entirely external-source based and needs stronger validation before any review workflow advances. Future trigger: Reassess if badge costs and research tables are confirmed by canonical memory or another reliable source."
}
```

Next step:

Reassess if badge costs and research tables are confirmed by canonical memory or another reliable source.
