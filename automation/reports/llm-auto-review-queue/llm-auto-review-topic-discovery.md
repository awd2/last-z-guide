# LLM Topic Discovery - 2026-05-17T09:03:01Z

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

Better answer matching for players searching gift center login, redeem flow, and code access. Could reduce friction for users who need the official path quickly.

Rationale:

This is the clearest high-signal opportunity. The page already exists, the cluster role is defined, and GSC shows meaningful impressions with low CTR on gift-center queries. That supports a human review for first-screen and query-match improvements without changing the page into a different intent. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low if scope stays on the existing cornerstone guide and does not blur into UID or support intents that belong elsewhere.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the current intro and headings already cover gift center login intent sufficiently
- Whether any proposed additions would conflict with gift-center-only-redeem-flow
- Whether UID and mailbox references remain accurate and within approved scope

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
  "notes": "This is the clearest high-signal opportunity. The page already exists, the cluster role is defined, and GSC shows meaningful impressions with low CTR on gift-center queries. That supports a human review for first-screen and query-match improvements without changing the page into a different intent. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for scoped update analysis against the current codes.html outline and canonical claim set.

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

Improved trust and route clarity for players using the official Gift Center and store flow.

Rationale:

The official domain is a plausible cross-validation source for routing and flow accuracy, but it is not proof by itself. The topic is worth human review because it may help validate official service paths and reduce drift on the Gift Center page.

Duplication risk:

Medium because it could overlap with the existing codes page unless the job is narrowly defined around routing and validation only.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Exact official Gift Center routing and setup flow
- Whether UID usage is still current
- Whether this topic adds a distinct job beyond the existing codes page

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
  "notes": "The official domain is a plausible cross-validation source for routing and flow accuracy, but it is not proof by itself. The topic is worth human review because it may help validate official service paths and reduce drift on the Gift Center page."
}
```

Next step:

Verify the official routing claims against canonical site memory and at least one additional reliable source before any content proposal.

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

Helps players plan HQ upgrades and dependencies without relying on stale or incomplete advice.

Rationale:

HQ and progression dependency coverage is a distinct user job and may expose planning gaps. The topic is worthwhile because it can improve accuracy on progression requirements, but only after verification beyond the single external reference. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium to high if the existing HQ page already covers the same dependency path. Scope must remain on verification and gap filling, not rewriting the whole page.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ construction dependencies
- Requirement thresholds and progression order
- Whether the source adds anything beyond existing page intent

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
  "notes": "HQ and progression dependency coverage is a distinct user job and may expose planning gaps. The topic is worthwhile because it can improve accuracy on progression requirements, but only after verification beyond the single external reference. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have a human confirm whether hq.html has a coverage gap and validate any requirement claims from at least one more reliable source.

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

Useful as a research validation signal, but too dependent on a single external source and too likely to overlap with existing research-cost coverage. Future trigger: Revisit if an owner confirms a concrete branch-name or cost-table gap on research-costs.html. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful as a research validation signal, but too dependent on a single external source and too likely to overlap with existing research-cost coverage. Future trigger: Revisit if an owner confirms a concrete branch-name or cost-table gap on research-costs.html. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Revisit if an owner confirms a concrete branch-name or cost-table gap on research-costs.html.

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

Search-result discovery only, with high duplication risk against an existing events guide and no verified claim set. Future trigger: Revisit if multiple reliable sources confirm a distinct event mechanic or schedule gap.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle; includes Age of Science for tech research and Hero Initiative for hero upgrades and tickets.

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
  "notes": "Search-result discovery only, with high duplication risk against an existing events guide and no verified claim set. Future trigger: Revisit if multiple reliable sources confirm a distinct event mechanic or schedule gap."
}
```

Next step:

Revisit if multiple reliable sources confirm a distinct event mechanic or schedule gap.

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

Likely duplicates existing research coverage and depends on a single external search result rather than verified mechanics. Future trigger: Revisit if research.html is missing the Laboratory overview or if owner review identifies a specific gap.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research building page; shows Laboratory unlock and that it is used to research Technologies.

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
  "notes": "Likely duplicates existing research coverage and depends on a single external search result rather than verified mechanics. Future trigger: Revisit if research.html is missing the Laboratory overview or if owner review identifies a specific gap."
}
```

Next step:

Revisit if research.html is missing the Laboratory overview or if owner review identifies a specific gap.

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

Potentially useful, but the topic title signals competitor-style tier-list framing and could copy or overextend existing heroes coverage. Future trigger: Revisit if a distinct player job emerges, such as equipment or roster explanation not already covered by heroes.html.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero roster page with character list, levels, and hero equipment sections. Good for hero discovery and equipment cross-checking.

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
  "notes": "Potentially useful, but the topic title signals competitor-style tier-list framing and could copy or overextend existing heroes coverage. Future trigger: Revisit if a distinct player job emerges, such as equipment or roster explanation not already covered by heroes.html."
}
```

Next step:

Revisit if a distinct player job emerges, such as equipment or roster explanation not already covered by heroes.html.

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

Research cost cross-check idea is plausible but too thin and too dependent on a competitor source without verification. Future trigger: Revisit if multiple sources or owner confirmation validate a specific badge-cost discrepancy.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page covering badge costs by level across laboratory categories. Useful for research discovery and cost cross-checking.

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
  "notes": "Research cost cross-check idea is plausible but too thin and too dependent on a competitor source without verification. Future trigger: Revisit if multiple sources or owner confirmation validate a specific badge-cost discrepancy."
}
```

Next step:

Revisit if multiple sources or owner confirmation validate a specific badge-cost discrepancy.
