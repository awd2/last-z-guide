# LLM Topic Discovery - 2026-05-17T15:21:37Z

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

Better first-screen usefulness and faster routing for players searching Gift Center, login, and code redemption help.

Rationale:

This is the clearest high-value opportunity because it is backed by strong GSC signals on an existing cornerstone page and the user job is well defined: improve query-to-page match for Gift Center and redeem-code searchers. The page already exists in the Economy cluster, so updating it is more appropriate than creating new content. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. The topic could overlap with adjacent Economy pages if scope is not kept on redeem flow and Gift Center routing only.

Expected route:

- index.html
- codes.html

Claims to verify:

- That codes.html is still the correct canonical page for Gift Center and redeem flow intent.
- That any query refinement can be addressed without changing protected canonical claims or blurring cluster roles.
- That current search intent has not shifted to another canonical page.

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
  "notes": "This is the clearest high-value opportunity because it is backed by strong GSC signals on an existing cornerstone page and the user job is well defined: improve query-to-page match for Gift Center and redeem-code searchers. The page already exists in the Economy cluster, so updating it is more appropriate than creating new content. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should confirm scope, protect canonical claims, and decide whether the update stays within the current template and cluster role.

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

Reduces confusion about official routing, UID usage, and store flow details for players trying to redeem or set up Gift Center correctly.

Rationale:

This is a useful cross-validation topic because it may help confirm official Gift Center routing and store flow details, but it is only a discovery signal from one external source. It is still worth review because the player job is distinct and tied to an existing Economy page.

Duplication risk:

Medium to high. The topic may duplicate the existing Gift Center intent unless it adds a clearly separate verification job.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- That the official domain truly reflects current Gift Center routing and flow behavior.
- That UID usage and store flow details are current and not outdated.
- That the topic adds a distinct player job beyond existing codes.html coverage.

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
  "notes": "This is a useful cross-validation topic because it may help confirm official Gift Center routing and store flow details, but it is only a discovery signal from one external source. It is still worth review because the player job is distinct and tied to an existing Economy page."
}
```

Next step:

Verify the public claims against canonical site memory and at least one additional reliable source or owner confirmation before any content proposal.

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

Helps players verify HQ requirements, construction dependencies, and progression planning with less guesswork.

Rationale:

HQ planning and progression dependency coverage are important player jobs, and this topic could fill a real gap if verified. It is better framed as an update to hq.html than a new page because it aligns with an existing Progression cluster page. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. The page may overlap with existing progression guidance unless it adds a specific verification layer.

Expected route:

- index.html
- hq.html

Claims to verify:

- That the external wiki reference is accurate for current HQ requirements.
- That the progression dependency data matches canonical site memory.
- That the update would not duplicate another Progression page's intent.

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
  "notes": "HQ planning and progression dependency coverage are important player jobs, and this topic could fill a real gap if verified. It is better framed as an update to hq.html than a new page because it aligns with an existing Progression cluster page. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should validate the external reference with a second source or owner confirmation and confirm the intended scope for hq.html.

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

Useful as a research signal, but it depends on a single external source and the claim set is not yet verified enough for a human-review opportunity beyond monitoring. Future trigger: Move forward only if a second reliable source or owner confirmation validates branch coverage and cost drift. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful as a research signal, but it depends on a single external source and the claim set is not yet verified enough for a human-review opportunity beyond monitoring. Future trigger: Move forward only if a second reliable source or owner confirmation validates branch coverage and cost drift. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Move forward only if a second reliable source or owner confirmation validates branch coverage and cost drift.

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

External search evidence only; the event claims are not verified and may duplicate existing Events coverage. Future trigger: Reconsider if canonical memory and a second source confirm the event structure and reward details.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily world event with a Hero Initiative phase that awards points for hero XP, fragments, and prime recruitment tickets; also includes a research-focused Age of Science phase.

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
  "notes": "External search evidence only; the event claims are not verified and may duplicate existing Events coverage. Future trigger: Reconsider if canonical memory and a second source confirm the event structure and reward details."
}
```

Next step:

Reconsider if canonical memory and a second source confirm the event structure and reward details.

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

This looks like a broad reference page and is too thin as a standalone opportunity without verified distinct player value. Future trigger: Reconsider if it reveals a specific missing hero-growth job or a verifiable gap not already covered by research.html.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page listing hero classes and power factors; useful for linking hero-event guidance to hero growth systems.

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
  "notes": "This looks like a broad reference page and is too thin as a standalone opportunity without verified distinct player value. Future trigger: Reconsider if it reveals a specific missing hero-growth job or a verifiable gap not already covered by research.html."
}
```

Next step:

Reconsider if it reveals a specific missing hero-growth job or a verifiable gap not already covered by research.html.

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

Potentially useful reference material, but the topic is broad and search-driven with high duplication risk against existing Heroes coverage. Future trigger: Reconsider if a verified niche gap emerges, such as roster filtering or stat cross-checking that is not already covered.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Dedicated hero reference page with hero roster, faction filters, levels, and hero equipment listings; useful for hero discovery and cross-checking character data.

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
  "notes": "Potentially useful reference material, but the topic is broad and search-driven with high duplication risk against existing Heroes coverage. Future trigger: Reconsider if a verified niche gap emerges, such as roster filtering or stat cross-checking that is not already covered."
}
```

Next step:

Reconsider if a verified niche gap emerges, such as roster filtering or stat cross-checking that is not already covered.

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

The topic is too close to general research reference content and remains unverified; it should not advance without stronger validation. Future trigger: Reconsider if Lab badge costs and research-name coverage are confirmed against canonical data and a second source.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page covering Laboratory categories and per-level badge costs, including a search interface for specific research names.

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
  "notes": "The topic is too close to general research reference content and remains unverified; it should not advance without stronger validation. Future trigger: Reconsider if Lab badge costs and research-name coverage are confirmed against canonical data and a second source."
}
```

Next step:

Reconsider if Lab badge costs and research-name coverage are confirmed against canonical data and a second source.
