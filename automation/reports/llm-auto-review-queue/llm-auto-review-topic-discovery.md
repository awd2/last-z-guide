# LLM Topic Discovery - 2026-05-16T18:11:29Z

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

Players searching for gift center, login, or redeem code help should find the right page faster and get a clearer first-screen answer.

Rationale:

Strong first-party search signal, clear page intent, and an existing cornerstone page make this a good human review candidate. The opportunity is to improve query-to-page match without breaking cluster role separation or protected canonical claims. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium because the page already serves this intent and must not be broadened into a catch-all.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the current page scope can improve CTR without changing protected canonical claims.
- Whether another canonical page already serves part of the search intent better.
- Whether any new wording would blur the gift center, mailbox, or role-separation rules.

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
  "notes": "Strong first-party search signal, clear page intent, and an existing cornerstone page make this a good human review candidate. The opportunity is to improve query-to-page match without breaking cluster role separation or protected canonical claims. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for scope validation against the protected canonical claims and the current page template.

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

Players can verify HQ requirements and construction dependencies before making progression mistakes.

Rationale:

This is a plausible progression support update if the reference can be verified against other reliable sources or owner confirmation. It aligns with an existing HQ page and has a distinct planning job.

Duplication risk:

Medium because HQ coverage may already exist elsewhere in the cluster and needs intent checking.

Expected route:

- index.html
- hq.html

Claims to verify:

- The actual HQ requirement and dependency structure.
- Whether the external reference matches canonical game knowledge.
- Whether the page already covers this planning job adequately.

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
  "notes": "This is a plausible progression support update if the reference can be verified against other reliable sources or owner confirmation. It aligns with an existing HQ page and has a distinct planning job."
}
```

Next step:

Human review should confirm the external claim, then determine whether this is a scope-safe update to the existing HQ page.

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

Players get more reliable cost and branch coverage information for planning research efficiently.

Rationale:

A research-cost cross-check can be valuable if the source is verified, especially where cost or branch naming drift could affect player planning. The topic is relevant to the existing research costs page and is not obviously duplicative. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium because cost-table content can overlap with other research pages and must stay tightly scoped.

Expected route:

- index.html
- research-costs.html

Claims to verify:

- Branch coverage and naming accuracy.
- Cost values or table structure if any public claim is implied.
- Whether the page intent differs from other research guides.

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
  "notes": "A research-cost cross-check can be valuable if the source is verified, especially where cost or branch naming drift could affect player planning. The topic is relevant to the existing research costs page and is not obviously duplicative. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Review the external source against canonical memory and another reliable source before deciding scope.

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

Useful as a discovery signal, but too dependent on a single official-looking source and too close to the existing Gift Center page to justify advancement now. Future trigger: Revisit only if a second reliable source or owner confirmation verifies a distinct player job.

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
  "notes": "Useful as a discovery signal, but too dependent on a single official-looking source and too close to the existing Gift Center page to justify advancement now. Future trigger: Revisit only if a second reliable source or owner confirmation verifies a distinct player job."
}
```

Next step:

Revisit only if a second reliable source or owner confirmation verifies a distinct player job.

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

Search-result evidence is too thin and externally sourced claims about event mechanics cannot advance without stronger verification. Future trigger: Revisit if official or owner-confirmed event details are available and the topic has a distinct event-help job.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Regular event with a Hero Initiative theme that uses Heroic Experience and Hero Fragments to improve Heroes and earn points; also includes an Age of Science research theme.

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
  "notes": "Search-result evidence is too thin and externally sourced claims about event mechanics cannot advance without stronger verification. Future trigger: Revisit if official or owner-confirmed event details are available and the topic has a distinct event-help job."
}
```

Next step:

Revisit if official or owner-confirmed event details are available and the topic has a distinct event-help job.

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

This is a broad hero hub search result with unclear incremental value versus existing hero/research coverage. Future trigger: Revisit if a specific gap in hero coverage or build guidance is identified with verified evidence.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page listing hero classes and the main stats/power inputs, useful for linking event tasks to hero progression.

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
  "notes": "This is a broad hero hub search result with unclear incremental value versus existing hero/research coverage. Future trigger: Revisit if a specific gap in hero coverage or build guidance is identified with verified evidence."
}
```

Next step:

Revisit if a specific gap in hero coverage or build guidance is identified with verified evidence.

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

Likely duplicates general hero coverage and relies on external search discovery rather than verified need. Future trigger: Revisit if there is a precise hero-coverage gap that cannot be handled by the current page set.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Main hero hub with character listings, levels, and equipment sections; useful for hero discovery and build cross-checks.

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
  "notes": "Likely duplicates general hero coverage and relies on external search discovery rather than verified need. Future trigger: Revisit if there is a precise hero-coverage gap that cannot be handled by the current page set."
}
```

Next step:

Revisit if there is a precise hero-coverage gap that cannot be handled by the current page set.

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

Potentially relevant, but still too dependent on external search discovery and may overlap existing research content. Future trigger: Revisit if verified badge-cost data shows a concrete gap in the current research pages.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page with badge costs and category structure; useful for research discovery and cost cross-validation leads.

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
  "notes": "Potentially relevant, but still too dependent on external search discovery and may overlap existing research content. Future trigger: Revisit if verified badge-cost data shows a concrete gap in the current research pages."
}
```

Next step:

Revisit if verified badge-cost data shows a concrete gap in the current research pages.
