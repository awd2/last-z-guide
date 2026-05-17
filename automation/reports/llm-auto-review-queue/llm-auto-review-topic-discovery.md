# LLM Topic Discovery - 2026-05-17T08:46:59Z

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

Better first-screen help for players searching for redeem codes, Gift Center login, and UID flow.

Rationale:

This is the clearest high-value opportunity because it is backed by page-level and query-level search signals and maps to an existing cornerstone page. The proposal fits the current Economy cluster and can likely improve query-to-page match without creating a new content surface. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because the query intent could overlap with other Economy pages if scope is not kept tight.

Expected route:

- index.html
- codes.html

Claims to verify:

- The search query patterns still justify a codes-page update.
- Any rewrite can be done without changing the protected canonical claims or cluster role separation.
- The target page is still the best canonical home for this intent.

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
  "notes": "This is the clearest high-value opportunity because it is backed by page-level and query-level search signals and maps to an existing cornerstone page. The proposal fits the current Economy cluster and can likely improve query-to-page match without creating a new content surface. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review to confirm the exact scope for an existing-page update and check that the canonical claims remain protected.

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

Clearer guidance for players on Gift Center setup and official routing.

Rationale:

This is a useful verification opportunity because the official service domain may help validate Gift Center routing and store flow details. It is worth review only as cross-validation, not as a source of copy or a reason to create new content.

Duplication risk:

High, because it may duplicate existing Gift Center intent unless a distinct user job is proven.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- The official domain confirms current Gift Center routing.
- The topic adds a distinct player job beyond existing Gift Center coverage.
- No competitor wording would be copied.

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
  "notes": "This is a useful verification opportunity because the official service domain may help validate Gift Center routing and store flow details. It is worth review only as cross-validation, not as a source of copy or a reason to create new content."
}
```

Next step:

Have a human verify the external source against canonical site memory and a second reliable source before any proposal is made.

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

More reliable HQ planning and dependency guidance for players.

Rationale:

This topic could help validate HQ requirement planning and progression dependencies, but the source is only a discovery signal. It is worth human review because progression accuracy matters and the expected page fit is plausible. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because HQ intent may already be covered elsewhere in the Progression cluster.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirements and dependencies match current game knowledge.
- The page remains the right canonical home for this progression topic.
- The source does not conflict with existing cluster boundaries.

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
  "notes": "This topic could help validate HQ requirement planning and progression dependencies, but the source is only a discovery signal. It is worth human review because progression accuracy matters and the expected page fit is plausible. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Verify the claims against canonical memory and a second reliable source before deciding whether this belongs on the HQ page.

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

Useful as a verification signal, but the claim set is too dependent on a single external source and may overlap with existing Research coverage. It should not advance until validated. Future trigger: Reconsider if a second reliable source or owner confirmation verifies the research cost and branch coverage gaps. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful as a verification signal, but the claim set is too dependent on a single external source and may overlap with existing Research coverage. It should not advance until validated. Future trigger: Reconsider if a second reliable source or owner confirmation verifies the research cost and branch coverage gaps. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if a second reliable source or owner confirmation verifies the research cost and branch coverage gaps.

### external-search-lastz-fandom-reference-bookstore-last-z-survival-shooter-wiki-fan-5

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

Search result discovery only; not enough proof for a public claim, and the topic title suggests possible mismatch or duplication risk. Future trigger: Reconsider only if the external page clearly maps to a distinct player job and is validated by canonical memory plus another source.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Bonus building tied to faster research; useful for cross-checking research-speed mechanics.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-bookstore-last-z-survival-shooter-wiki-fan-5",
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
  "notes": "Search result discovery only; not enough proof for a public claim, and the topic title suggests possible mismatch or duplication risk. Future trigger: Reconsider only if the external page clearly maps to a distinct player job and is validated by canonical memory plus another source."
}
```

Next step:

Reconsider only if the external page clearly maps to a distinct player job and is validated by canonical memory plus another source.

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

Discovery-only event topic with high duplication and verification risk. It must not advance from monitor status based on search snippets alone. Future trigger: Reconsider if the event structure is confirmed by owner-approved memory and a second source. 

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily rotating event with an Age of Science theme for research speed-ups and a Hero Initiative theme for hero upgrades.

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
  "notes": "Discovery-only event topic with high duplication and verification risk. It must not advance from monitor status based on search snippets alone. Future trigger: Reconsider if the event structure is confirmed by owner-approved memory and a second source. "
}
```

Next step:

Reconsider if the event structure is confirmed by owner-approved memory and a second source.

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

Hero index content is broad and likely overlaps existing Heroes coverage. The external search result is not enough to justify a new or expanded proposal without verification. Future trigger: Reconsider if there is a clearly distinct hero job, such as roster discovery or stat comparison, that is missing from current coverage.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero index and equipment page with character roster, faction filters, levels, and gear stats; good for hero discovery and cross-checking hero-related pages.

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
  "notes": "Hero index content is broad and likely overlaps existing Heroes coverage. The external search result is not enough to justify a new or expanded proposal without verification. Future trigger: Reconsider if there is a clearly distinct hero job, such as roster discovery or stat comparison, that is missing from current coverage."
}
```

Next step:

Reconsider if there is a clearly distinct hero job, such as roster discovery or stat comparison, that is missing from current coverage.

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

Research table and badge cost content is discovery-only and may duplicate current Research pages. The claim set needs stronger validation before any workflow advance. Future trigger: Reconsider if verified costs or table gaps are confirmed by canonical memory and a second source.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page with category navigation and badge costs by level; useful for locating research topics and checking cost structures.

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
  "notes": "Research table and badge cost content is discovery-only and may duplicate current Research pages. The claim set needs stronger validation before any workflow advance. Future trigger: Reconsider if verified costs or table gaps are confirmed by canonical memory and a second source."
}
```

Next step:

Reconsider if verified costs or table gaps are confirmed by canonical memory and a second source.
