# LLM Topic Discovery - 2026-05-17T08:44:29Z

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

Helps players quickly find redeem code and Gift Center login guidance from the page they are already reaching.

Rationale:

This has the clearest first-party signal: strong impressions on codes.html plus multiple low-CTR gift center queries. It fits the existing cornerstone guide and can likely improve query-to-page match without creating a new page, as long as cluster boundaries stay intact. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. The topic could overlap with a dedicated Gift Center page if scope is not tightly controlled.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the current codes page already covers the gift center intent adequately
- Which query intent belongs on codes.html versus a separate Gift Center page
- Whether any wording change can be done without expanding beyond approved cornerstone scope

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
  "notes": "This has the clearest first-party signal: strong impressions on codes.html plus multiple low-CTR gift center queries. It fits the existing cornerstone guide and can likely improve query-to-page match without creating a new page, as long as cluster boundaries stay intact. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for scoped update planning against codes.html, with explicit protection of canonical claims and role separation.

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

Reduces confusion around Gift Center setup, UID use, and official routing.

Rationale:

The official domain is a plausible validation source for Gift Center routing and store flow. This is worth human review because it may confirm or refine the existing Gift Center page intent, but it must not rely on the external source alone.

Duplication risk:

Medium. It may duplicate an existing Gift Center or redeem flow page unless a distinct user job is confirmed.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Exact official routing for Gift Center and store flow
- Whether UID usage guidance is current and accurate
- Whether this topic is distinct from existing redeem or login coverage

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
  "notes": "The official domain is a plausible validation source for Gift Center routing and store flow. This is worth human review because it may confirm or refine the existing Gift Center page intent, but it must not rely on the external source alone."
}
```

Next step:

Verify against canonical site memory and one additional reliable source before any content proposal is made.

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

Helps players plan HQ upgrades, dependencies, and progression order more reliably.

Rationale:

HQ and progression dependency checks are valuable and potentially high impact, but the topic is only a discovery signal right now. It merits human review because it could close a real coverage gap in progression planning if verified. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low to medium. It likely fits an existing HQ page unless another progression page already owns the same intent.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement and dependency details
- Whether the progression coverage already exists elsewhere
- Any terminology or ordering differences that would affect the page structure

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
  "notes": "HQ and progression dependency checks are valuable and potentially high impact, but the topic is only a discovery signal right now. It merits human review because it could close a real coverage gap in progression planning if verified. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Verify the external reference against canonical memory and at least one second source before deciding scope.

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

Useful as a cross-check signal, but still dependent on a single external source and may duplicate existing research-cost coverage. Future trigger: Monitor until another reliable source or owner confirmation validates cost, branch, or naming claims. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful as a cross-check signal, but still dependent on a single external source and may duplicate existing research-cost coverage. Future trigger: Monitor until another reliable source or owner confirmation validates cost, branch, or naming claims. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Monitor until another reliable source or owner confirmation validates cost, branch, or naming claims.

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

External search result only; too thin and too tied to search discovery to advance now. It may also blur events and hero/research roles. Future trigger: Revisit only if canonical memory and a second source confirm a distinct event-related player job.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle includes a research-focused theme and a hero-focused theme; useful for linking research and hero upgrade mechanics to event scoring.

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
  "notes": "External search result only; too thin and too tied to search discovery to advance now. It may also blur events and hero/research roles. Future trigger: Revisit only if canonical memory and a second source confirm a distinct event-related player job."
}
```

Next step:

Revisit only if canonical memory and a second source confirm a distinct event-related player job.

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

Search discovery only, with high duplication risk against existing research tech coverage. Future trigger: Reconsider if the Laboratory page is confirmed to own a unique research mechanic not covered elsewhere.

Duplication risk:



Expected route:

- tech.html

Claims to verify:

- None

Evidence:

- Core building for technology research; good cross-check for research-related event tasks.

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
  "notes": "Search discovery only, with high duplication risk against existing research tech coverage. Future trigger: Reconsider if the Laboratory page is confirmed to own a unique research mechanic not covered elsewhere."
}
```

Next step:

Reconsider if the Laboratory page is confirmed to own a unique research mechanic not covered elsewhere.

### external-search-lastz-fandom-reference-technologies-last-z-survival-shooter-wiki--6

- Title: External search opportunity: Technologies | Last Z: Survival Shooter Wiki | Fandom
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

Search discovery only and likely duplicates research-costs.html intent. Future trigger: Reopen if a verified gap appears in tech-tree coverage or branch naming changes.

Duplication risk:



Expected route:

- research-costs.html

Claims to verify:

- None

Evidence:

- Main tech tree page showing research costs and research-speed techs; useful for identifying research mechanics touched by events.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-technologies-last-z-survival-shooter-wiki--6",
  "title": "External search opportunity: Technologies | Last Z: Survival Shooter Wiki | Fandom",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "atlas-page",
  "target_page_or_slug": "research-costs.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Search discovery only and likely duplicates research-costs.html intent. Future trigger: Reopen if a verified gap appears in tech-tree coverage or branch naming changes."
}
```

Next step:

Reopen if a verified gap appears in tech-tree coverage or branch naming changes.

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

Hero hub discovery is not enough by itself, and the topic risks collapsing into existing hero hub or roster coverage. Future trigger: Monitor for a verified roster coverage gap or owner-confirmed need for a consolidated hero hub update.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero hub with tier list, stats, factions, and hero equipment sections; useful for hero roster discovery and cross-checking character pages.

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
  "notes": "Hero hub discovery is not enough by itself, and the topic risks collapsing into existing hero hub or roster coverage. Future trigger: Monitor for a verified roster coverage gap or owner-confirmed need for a consolidated hero hub update."
}
```

Next step:

Monitor for a verified roster coverage gap or owner-confirmed need for a consolidated hero hub update.
