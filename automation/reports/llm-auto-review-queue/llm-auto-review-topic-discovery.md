# LLM Topic Discovery - 2026-05-16T17:54:41Z

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

Improves query-to-page match for players searching gift center and redeem code help, especially login and UID related intent.

Rationale:

This is the clearest high-value signal. The page already exists as a cornerstone guide in the Economy cluster, and the GSC data shows meaningful impressions with weaker CTR on gift center related queries. The proposal also protects canonical claims and preserves cluster separation, which makes it suitable for a human review of an existing page rather than a new page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low if scoped to the current codes page and kept within the existing Economy cluster role.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the low CTR queries reflect a true content gap or just ranking position effects.
- Whether any copy changes would preserve gift-center-only-redeem-flow, gift-rewards-mailbox, and gift-center-cluster-role-separation.
- Whether another canonical page already better satisfies the gift center login intent.

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
  "notes": "This is the clearest high-value signal. The page already exists as a cornerstone guide in the Economy cluster, and the GSC data shows meaningful impressions with weaker CTR on gift center related queries. The proposal also protects canonical claims and preserves cluster separation, which makes it suitable for a human review of an existing page rather than a new page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human owner review should confirm whether the page can be adjusted within current template and claim boundaries without expanding scope.

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

Helps players confirm HQ requirements and progression dependencies before they invest resources.

Rationale:

This is a useful cross-check opportunity for HQ and progression planning. It is tied to an existing page, has a clear player job, and is explicitly framed as verification rather than copy sourcing. The topic is useful if it helps validate dependency coverage and avoids role drift.

Duplication risk:

Medium because it may overlap with existing progression guidance if the distinct job is not kept narrow.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement details and construction dependency order.
- Whether the proposed coverage adds a distinct job beyond existing progression guidance.
- Whether the source can be corroborated without using competitor wording.

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
  "notes": "This is a useful cross-check opportunity for HQ and progression planning. It is tied to an existing page, has a clear player job, and is explicitly framed as verification rather than copy sourcing. The topic is useful if it helps validate dependency coverage and avoids role drift."
}
```

Next step:

Verify the external claims against canonical memory and one additional reliable source before any content proposal is drafted.

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

Reduces the chance that players rely on stale research cost tables or incomplete branch coverage.

Rationale:

This is a strong verification-oriented opportunity for the Research cluster. The proposal focuses on branch coverage, cost-name drift, and planning gaps, which are valuable maintenance issues for an existing atlas page rather than a new content initiative. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium because research cost topics often overlap with other mechanics pages unless the scope is tightly defined.

Expected route:

- index.html
- research-costs.html

Claims to verify:

- Research branch names and cost table accuracy.
- Whether the external reference covers unique gaps not already handled elsewhere.
- Whether the proposal can be expressed without copying source wording.

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
  "notes": "This is a strong verification-oriented opportunity for the Research cluster. The proposal focuses on branch coverage, cost-name drift, and planning gaps, which are valuable maintenance issues for an existing atlas page rather than a new content initiative. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Check canonical site memory and owner notes for the current research page scope before any proposal-only workflow starts.

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

Monitor only. The idea is plausible, but it relies on a single external official source and does not yet establish a distinct enough player job beyond the existing codes or gift center route. Future trigger: Move forward only if a second reliable source or owner confirmation validates a unique gap in UID or official routing coverage.

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
  "notes": "Monitor only. The idea is plausible, but it relies on a single external official source and does not yet establish a distinct enough player job beyond the existing codes or gift center route. Future trigger: Move forward only if a second reliable source or owner confirmation validates a unique gap in UID or official routing coverage."
}
```

Next step:

Move forward only if a second reliable source or owner confirmation validates a unique gap in UID or official routing coverage.

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

Reject for now. This is based on external search discovery and appears too dependent on unverified claims about event structure and rewards. It may also duplicate event coverage without a clearly proven need. Future trigger: Reconsider if canonical memory plus a second reliable source confirms a distinct event mechanic or reward pattern not covered elsewhere.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle page. Includes a research-themed phase ('Age of Science') plus a hero-growth phase ('Hero Initiative') and ranking rewards.

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
  "notes": "Reject for now. This is based on external search discovery and appears too dependent on unverified claims about event structure and rewards. It may also duplicate event coverage without a clearly proven need. Future trigger: Reconsider if canonical memory plus a second reliable source confirms a distinct event mechanic or reward pattern not covered elsewhere."
}
```

Next step:

Reconsider if canonical memory plus a second reliable source confirms a distinct event mechanic or reward pattern not covered elsewhere.

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

Monitor only. The hero overview looks useful, but the proposal is search-result driven and may overlap with existing hero coverage without proving a new user job. Future trigger: Advance only if human review confirms a specific hero coverage gap, such as missing class mapping or build context.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page. Lists hero classes and the main power inputs, useful for linking heroes to event goals.

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
  "notes": "Monitor only. The hero overview looks useful, but the proposal is search-result driven and may overlap with existing hero coverage without proving a new user job. Future trigger: Advance only if human review confirms a specific hero coverage gap, such as missing class mapping or build context."
}
```

Next step:

Advance only if human review confirms a specific hero coverage gap, such as missing class mapping or build context.

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

Monitor only. Research cost-table maintenance is valuable, but this specific search result is not enough to prove a distinct update beyond the existing research page. Future trigger: Advance if owner review confirms the badge cost data is materially incomplete or stale and the topic can be scoped narrowly.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research guide with category tabs and per-level badge cost tables; useful for locating research mechanics and cost data.

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
  "notes": "Monitor only. Research cost-table maintenance is valuable, but this specific search result is not enough to prove a distinct update beyond the existing research page. Future trigger: Advance if owner review confirms the badge cost data is materially incomplete or stale and the topic can be scoped narrowly."
}
```

Next step:

Advance if owner review confirms the badge cost data is materially incomplete or stale and the topic can be scoped narrowly.
