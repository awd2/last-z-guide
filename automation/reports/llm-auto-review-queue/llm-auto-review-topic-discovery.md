# LLM Topic Discovery - 2026-05-17T08:36:29Z

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

Better query-to-page match for players looking for redeem codes, gift center login, and UID help.

Rationale:

This has the clearest page-level search signal: a specific existing page with strong impressions, low CTR, and query patterns that indicate a mismatch between search intent and the current first screen. It is also already anchored to an existing cornerstone guide, so updating the existing page is the right form if scope stays within protected claims and cluster separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low if the scope remains on codes.html and does not expand into another canonical page's job.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the low-CTR queries map to the existing codes.html intent without needing a new page
- Whether any proposed change would blur role separation with gift center or UID coverage
- Whether protected canonical claims can remain unchanged while improving snippet usefulness

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
  "notes": "This has the clearest page-level search signal: a specific existing page with strong impressions, low CTR, and query patterns that indicate a mismatch between search intent and the current first screen. It is also already anchored to an existing cornerstone guide, so updating the existing page is the right form if scope stays within protected claims and cluster separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for a scoped update plan that preserves protected claims and current routing.

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

Improved confidence that Gift Center setup, UID usage, and official routing guidance are accurate.

Rationale:

The official service domain is a strong discovery signal for validating Gift Center routing and store flow accuracy, but it is not proof by itself. It is still worth human review because it can strengthen an existing Economy page if verified against canonical site memory and a second reliable source.

Duplication risk:

Medium because the topic may overlap with existing Gift Center and redeem coverage.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Exact official Gift Center routing and store flow
- Whether the page would add a distinct player job beyond existing codes or UID coverage
- Whether any claim can be supported without copying source wording

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
  "notes": "The official service domain is a strong discovery signal for validating Gift Center routing and store flow accuracy, but it is not proof by itself. It is still worth human review because it can strengthen an existing Economy page if verified against canonical site memory and a second reliable source."
}
```

Next step:

Verify the external claim against canonical memory and one additional reliable source before any content proposal.

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

Better planning help for HQ requirements, dependencies, and progression order.

Rationale:

This is a useful progression cross-check opportunity because HQ and construction dependency accuracy matters, but the current evidence is only a discovery signal. It deserves review if the goal is to validate existing HQ guidance rather than create new speculative coverage. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium because HQ content often overlaps with broader progression pages.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement rules and progression dependencies
- Whether the topic adds a distinct player job beyond the current HQ page
- Whether source claims match current game state

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
  "notes": "This is a useful progression cross-check opportunity because HQ and construction dependency accuracy matters, but the current evidence is only a discovery signal. It deserves review if the goal is to validate existing HQ guidance rather than create new speculative coverage. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Cross-check claims with canonical memory, owner confirmation, and another reliable source before accepting.

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

Useful discovery signal, but the claim set is too dependent on a single external source and overlaps existing research coverage. It should not advance until verified against stronger references. Future trigger: Only revisit if a second reliable source or owner confirmation validates specific research cost or branch drift issues. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful discovery signal, but the claim set is too dependent on a single external source and overlaps existing research coverage. It should not advance until verified against stronger references. Future trigger: Only revisit if a second reliable source or owner confirmation validates specific research cost or branch drift issues. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Only revisit if a second reliable source or owner confirmation validates specific research cost or branch drift issues.

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

External search result is discovery only and the event mechanic claim cannot be treated as proof. It is too risky to advance without stronger validation and may overlap existing events coverage. Future trigger: Reconsider if owner-confirmed event mechanics or a reliable second source confirms a distinct event guide gap.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event that includes an Age of Science round for research speed-ups and a Hero Initiative round for hero upgrades; useful for event-mechanics cross-checks.

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
  "notes": "External search result is discovery only and the event mechanic claim cannot be treated as proof. It is too risky to advance without stronger validation and may overlap existing events coverage. Future trigger: Reconsider if owner-confirmed event mechanics or a reliable second source confirms a distinct event guide gap."
}
```

Next step:

Reconsider if owner-confirmed event mechanics or a reliable second source confirms a distinct event guide gap.

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

This is a broad hero overview signal, but the proposal is thin and likely duplicates existing hero coverage. It needs stronger evidence of a distinct player job before human review. Future trigger: Revisit if a specific hero system gap, roster change, or new verification source creates a clearer update need.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page listing hero types and the main hero power factors, helpful for identifying hero-related guide topics.

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
  "notes": "This is a broad hero overview signal, but the proposal is thin and likely duplicates existing hero coverage. It needs stronger evidence of a distinct player job before human review. Future trigger: Revisit if a specific hero system gap, roster change, or new verification source creates a clearer update need."
}
```

Next step:

Revisit if a specific hero system gap, roster change, or new verification source creates a clearer update need.

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

Research cost tables and badge data are highly sensitive to drift, so a single external search result is not enough. This is better monitored until verified against canonical memory and another source. Future trigger: Only advance if verified cost or branch changes are confirmed by owner-approved references.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research hub with category tabs, search, and per-level badge cost tables; useful for discovery of research names and cost structure.

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
  "notes": "Research cost tables and badge data are highly sensitive to drift, so a single external search result is not enough. This is better monitored until verified against canonical memory and another source. Future trigger: Only advance if verified cost or branch changes are confirmed by owner-approved references."
}
```

Next step:

Only advance if verified cost or branch changes are confirmed by owner-approved references.
