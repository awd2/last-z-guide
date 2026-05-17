# LLM Topic Discovery - 2026-05-17T09:49:03Z

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

Better match for users searching redeem codes and gift center login help; likely improves first-screen usefulness and query satisfaction.

Rationale:

This is the strongest signal-based opportunity because it targets an existing cornerstone page with measurable query demand and low CTR on related gift center searches. The page already owns this cluster role, so an update review is more appropriate than a new page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium because the topic is adjacent to existing gift center and redeem coverage, but the canonical claim protections lower the chance of overlap if scope stays narrow.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the query intent is best served by codes.html rather than another canonical page.
- Whether any suggested revision can stay within existing cornerstone scope.
- Whether protected claims remain intact: gift-center-only-redeem-flow, gift-rewards-mailbox, and gift-center-cluster-role-separation.

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
  "notes": "This is the strongest signal-based opportunity because it targets an existing cornerstone page with measurable query demand and low CTR on related gift center searches. The page already owns this cluster role, so an update review is more appropriate than a new page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human owner review for scope validation against canonical claims and cluster role separation before any proposal drafting.

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

Helps players confirm where to redeem, how UID fits in, and whether the official route remains accurate.

Rationale:

The official domain is a strong cross-validation lead for Gift Center routing and redeem/store flow, but it is not proof by itself. This is worth human review because it may confirm user-facing flow details that support an existing page.

Duplication risk:

High because it overlaps the existing Gift Center page intent and could easily duplicate or blur current coverage.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Official routing for Gift Center and store flow.
- Whether UID guidance belongs on gift-center-uid.html or another existing page.
- Whether the source adds a distinct player job beyond existing Gift Center coverage.

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
  "notes": "The official domain is a strong cross-validation lead for Gift Center routing and redeem/store flow, but it is not proof by itself. This is worth human review because it may confirm user-facing flow details that support an existing page."
}
```

Next step:

Verify the claim against canonical site memory and at least one additional reliable source or owner confirmation before any content proposal.

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

Reduces confusion about HQ requirements, prerequisites, and construction order.

Rationale:

HQ and progression requirements are a meaningful player job and fit an existing progression page, but the external source is only discovery input. Human review is justified because dependency and construction-route accuracy matter to progression planning. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium because it likely overlaps with existing progression content but may add missing dependency coverage.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement and dependency details.
- Whether progression route coverage is missing on hq.html.
- Whether the source introduces any duplicate or conflicting naming.

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
  "notes": "HQ and progression requirements are a meaningful player job and fit an existing progression page, but the external source is only discovery input. Human review is justified because dependency and construction-route accuracy matter to progression planning. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Cross-check the HQ claims against canonical memory and another reliable source before deciding whether the existing page needs expansion.

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

Useful as discovery signal, but the claim set is too source-dependent and high risk for immediate review without stronger cross-validation. It also appears likely to overlap with existing research coverage. Future trigger: Move to human review only if a second reliable source or owner confirmation verifies the cost and branch coverage claims. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful as discovery signal, but the claim set is too source-dependent and high risk for immediate review without stronger cross-validation. It also appears likely to overlap with existing research coverage. Future trigger: Move to human review only if a second reliable source or owner confirmation verifies the cost and branch coverage claims. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Move to human review only if a second reliable source or owner confirmation verifies the cost and branch coverage claims.

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

Search result is discovery only and the event claims are not verified. Event mechanics and reward tiers are especially sensitive to single-source drift. Future trigger: Review only after canonical memory and a second reliable source confirm the event cycle and reward structure.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle with an 'Age of Science' phase for speeding research and a 'Hero Initiative' phase for hero upgrades; also shows reward tiers.

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
  "notes": "Search result is discovery only and the event claims are not verified. Event mechanics and reward tiers are especially sensitive to single-source drift. Future trigger: Review only after canonical memory and a second reliable source confirm the event cycle and reward structure."
}
```

Next step:

Review only after canonical memory and a second reliable source confirm the event cycle and reward structure.

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

The hero overview appears to be generic roster reference content and may duplicate existing hero/research coverage. External search alone is not enough to justify an immediate review. Future trigger: Reconsider if there is a clearly distinct user job not already covered by research.html or heroes.html.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page listing hero classes and the main hero power components.

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
  "notes": "The hero overview appears to be generic roster reference content and may duplicate existing hero/research coverage. External search alone is not enough to justify an immediate review. Future trigger: Reconsider if there is a clearly distinct user job not already covered by research.html or heroes.html."
}
```

Next step:

Reconsider if there is a clearly distinct user job not already covered by research.html or heroes.html.

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

This is highly likely to duplicate existing research coverage and is based on a single external search signal. It also risks copying competitor structure or wording. Future trigger: Promote only if a verified gap in research cost coverage is found and the scope can stay clearly distinct.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page with categories and per-level badge costs. Strong lead for research discovery, especially hero-related research grouping.

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
  "notes": "This is highly likely to duplicate existing research coverage and is based on a single external search signal. It also risks copying competitor structure or wording. Future trigger: Promote only if a verified gap in research cost coverage is found and the scope can stay clearly distinct."
}
```

Next step:

Promote only if a verified gap in research cost coverage is found and the scope can stay clearly distinct.
