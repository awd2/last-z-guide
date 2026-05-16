# LLM Topic Discovery - 2026-05-16T19:15:38Z

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

Helps players find the correct redeem flow faster and reduces confusion for gift center and code lookup searches.

Rationale:

This is the clearest high-signal opportunity. The page already exists, the cluster role is defined, and the GSC data shows meaningful impressions with low CTR on gift center related queries. It is suitable for human review because the task is to improve query match and first-screen usefulness without changing canonical claims or cluster separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low duplication risk if the update stays within the existing codes.html intent and preserves canonical claim boundaries.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the low CTR is caused by intent mismatch, snippet competition, or page presentation rather than missing content.
- Whether codes.html remains the best canonical page for gift center queries.
- Whether the existing canonical claims must remain unchanged.

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
  "notes": "This is the clearest high-signal opportunity. The page already exists, the cluster role is defined, and the GSC data shows meaningful impressions with low CTR on gift center related queries. It is suitable for human review because the task is to improve query match and first-screen usefulness without changing canonical claims or cluster separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review to check whether the current page already satisfies the query intent and whether any update can stay within approved scope.

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

Improves confidence that players are using the official Gift Center path and correct UID-related flow.

Rationale:

This topic is worth review because official routing and Gift Center flow accuracy are important to player trust, but the proposal is discovery only and must be verified against additional sources or owner confirmation. It may justify an existing-page refresh if the current page leaves routing unclear.

Duplication risk:

Medium duplication risk because it may overlap with existing gift center and redeem guidance unless a distinct validation gap is found.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Official Gift Center routing and store flow details.
- Whether UID usage is described accurately and is still current.
- Whether this topic adds a distinct player job beyond existing gift center guidance.

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
  "notes": "This topic is worth review because official routing and Gift Center flow accuracy are important to player trust, but the proposal is discovery only and must be verified against additional sources or owner confirmation. It may justify an existing-page refresh if the current page leaves routing unclear."
}
```

Next step:

Verify against canonical site memory and at least one other reliable source before deciding whether the page needs a targeted update.

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

Helps players plan progression, avoid dependency mistakes, and understand HQ-related requirements more reliably.

Rationale:

This is a plausible update_existing candidate because HQ and progression planning are core user jobs, but the external source is only a discovery signal. Human review should confirm whether it adds new dependency or requirement coverage before any content work is proposed. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium duplication risk if hq.html already covers the same dependency logic and route coverage.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement planning details.
- Construction dependency relationships.
- Whether there are missing progression-route gaps that are not already covered.

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
  "notes": "This is a plausible update_existing candidate because HQ and progression planning are core user jobs, but the external source is only a discovery signal. Human review should confirm whether it adds new dependency or requirement coverage before any content work is proposed. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Cross-check the claim set against canonical knowledge and a second reliable source, then assess whether the page needs a narrow expansion or remains sufficient.

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

Useful as a discovery signal, but too dependent on a single external source and too likely to overlap with existing research-cost coverage without a clearly distinct player job. Future trigger: Reconsider if a second reliable source or owner confirmation reveals a specific missing branch, cost drift, or naming conflict that is not already covered. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful as a discovery signal, but too dependent on a single external source and too likely to overlap with existing research-cost coverage without a clearly distinct player job. Future trigger: Reconsider if a second reliable source or owner confirmation reveals a specific missing branch, cost drift, or naming conflict that is not already covered. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if a second reliable source or owner confirmation reveals a specific missing branch, cost drift, or naming conflict that is not already covered.

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

External search result only; the topic is too thin and may duplicate existing events coverage. It also lacks verified public claims and could blur cluster roles. Future trigger: Revisit if verified event mechanics or a clearly missing event subtopic emerges from canonical memory and a second reliable source.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle page linking research tasks to the Age of Science theme, and hero upgrade tasks to Hero Initiative.

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
  "notes": "External search result only; the topic is too thin and may duplicate existing events coverage. It also lacks verified public claims and could blur cluster roles. Future trigger: Revisit if verified event mechanics or a clearly missing event subtopic emerges from canonical memory and a second reliable source."
}
```

Next step:

Revisit if verified event mechanics or a clearly missing event subtopic emerges from canonical memory and a second reliable source.

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

The result is discovery-only and currently too generic. It likely duplicates existing heroes or research intent without a distinct player job. Future trigger: Reconsider if source verification shows a concrete gap in hero discovery, equipment guidance, or roster structure that is not covered elsewhere.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero roster and power overview page for hero discovery and cross-linking to hero systems.

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
  "notes": "The result is discovery-only and currently too generic. It likely duplicates existing heroes or research intent without a distinct player job. Future trigger: Reconsider if source verification shows a concrete gap in hero discovery, equipment guidance, or roster structure that is not covered elsewhere."
}
```

Next step:

Reconsider if source verification shows a concrete gap in hero discovery, equipment guidance, or roster structure that is not covered elsewhere.

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

This is a likely duplicate of existing heroes coverage and depends on a competitor-style source that cannot be used as a copy target. Future trigger: Revisit if a verified, non-duplicative hero job emerges, such as a distinct loadout or roster navigation gap.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Core heroes hub with hero list and equipment section; good lead for character discovery and loadout cross-checks.

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
  "notes": "This is a likely duplicate of existing heroes coverage and depends on a competitor-style source that cannot be used as a copy target. Future trigger: Revisit if a verified, non-duplicative hero job emerges, such as a distinct loadout or roster navigation gap."
}
```

Next step:

Revisit if a verified, non-duplicative hero job emerges, such as a distinct loadout or roster navigation gap.

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

This research guide concept is too close to existing research-cost coverage and is based on search discovery only, with no proof of a separate user job. Future trigger: Reconsider if verified evidence shows a missing badge-cost branch or a real mismatch in research table structure that cannot be handled in the current page.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table hub with category navigation and per-level badge costs; strong lead for research discovery and cost cross-checks.

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
  "notes": "This research guide concept is too close to existing research-cost coverage and is based on search discovery only, with no proof of a separate user job. Future trigger: Reconsider if verified evidence shows a missing badge-cost branch or a real mismatch in research table structure that cannot be handled in the current page."
}
```

Next step:

Reconsider if verified evidence shows a missing badge-cost branch or a real mismatch in research table structure that cannot be handled in the current page.
