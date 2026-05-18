# LLM Topic Discovery - 2026-05-18T18:15:10Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`
- Source Scout request: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`
- Topics: 8
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Topic Proposals

### alliance-duel-gsc-opportunity

- Title: GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy
- Target: `alliance-duel.html`
- Cluster: `Events`
- Action: `monitor`
- Archetype: `event-guide`
- Priority: `low`
- Risk: `medium`
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:

Better match for last z vs schedule intent, faster access to schedule and day-by-day strategy, and improved first-screen usefulness.

Rationale:

This is a strong page-level opportunity because the existing event guide already matches the cluster, the route is clear, and the GSC signal suggests meaningful visibility with moderate CTR room. It is suitable for a scoped update rather than new content. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low, because the proposal targets an existing canonical event page and the cluster role is already established.

Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- Whether alliance-duel.html is still the best canonical page for the target query set.
- Whether the proposed schedule and day 1-6 plan fit existing page scope without expanding into a broader events hub.
- Whether any schedule or strategy claims need fresh owner confirmation before a proposal is drafted.

Evidence:

- GSC page signal: alliance-duel.html had 8912 impressions, 434 clicks, 4.87% CTR, avg position 6.10.

Backlog Row Preview:

```json
{
  "topic_id": "alliance-duel-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy",
  "cluster": "Events",
  "recommended_action": "monitor",
  "archetype_suggestion": "event-guide",
  "target_page_or_slug": "alliance-duel.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-17: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This is a strong page-level opportunity because the existing event guide already matches the cluster, the route is clear, and the GSC signal suggests meaningful visibility with moderate CTR room. It is suitable for a scoped update rather than new content. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have an editor confirm query intent, compare the page against the current canonical event guide, and define a scoped update that preserves cluster separation.

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

Cleaner path to redeem codes, gift center login, and UID guidance with less friction for searchers who need quick action.

Rationale:

This is the strongest opportunity in the set because the page has large impression volume, low CTR signals on multiple gift center queries, and an existing backlog history that suggests prior optimization work. The page is clearly canonical for redeem codes and gift center intent, but the update must preserve protected claims and cluster separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low to medium, because the topic overlaps the existing cornerstone guide and must avoid creating a competing page intent.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the current page still owns the primary redeem and gift center intent.
- Whether protected canonical claims remain accurate and unchanged.
- Whether any mention of login, UID, or redeem flow needs direct owner validation before an apply step.

Evidence:

- GSC page signal: codes.html had 40033 impressions, 733 clicks, 1.83% CTR, avg position 6.01.
- Low CTR query: `last z gift center` had 3169 impressions, 121 clicks, 3.82% CTR, position 6.58.
- Low CTR query: `last z gift center login` had 903 impressions, 46 clicks, 5.09% CTR, position 5.14.
- Low CTR query: `lastz gift center` had 683 impressions, 29 clicks, 4.25% CTR, position 5.96.
- Low CTR query: `last-z.com gift center` had 508 impressions, 25 clicks, 4.92% CTR, position 6.00.

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
  "source_reference": "GSC weekly 2026-05-17: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This is the strongest opportunity in the set because the page has large impression volume, low CTR signals on multiple gift center queries, and an existing backlog history that suggests prior optimization work. The page is clearly canonical for redeem codes and gift center intent, but the update must preserve protected claims and cluster separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have a human reviewer verify that the page can be improved without changing protected claims or blurring roles with any gift center support page.

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

More reliable guidance for setup, UID usage, and official service routing, reducing confusion around redeem flow.

Rationale:

The official service domain is a potentially strong verification lead for Gift Center routing and redeem flow accuracy, but it is not proof by itself. The opportunity is worth human review only as a validation task for the existing support guide.

Duplication risk:

Medium, because the topic may overlap existing gift center coverage and could duplicate current support intent if not scoped carefully.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Whether the official site confirms the same Gift Center routing currently described on the site.
- Whether UID and store flow instructions align with owner-confirmed knowledge.
- Whether the topic adds a distinct player job beyond existing gift center coverage.

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
  "notes": "The official service domain is a potentially strong verification lead for Gift Center routing and redeem flow accuracy, but it is not proof by itself. The opportunity is worth human review only as a validation task for the existing support guide."
}
```

Next step:

Cross-check the official site against canonical memory and one additional reliable source before deciding whether a scoped update is justified.

### external-hq-and-progression-reference-cross-check

- Title: External source opportunity: HQ and progression requirement cross-check
- Target: `hq.html`
- Cluster: `Progression`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:



Rationale:

This is a verification lead, but the current evidence is too thin and external-source based to move forward without stronger validation. It overlaps existing HQ/progression intent and should not advance to a content workflow yet. Future trigger: Move to review only if canonical memory plus a second reliable source confirm a real dependency or planning gap. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:



Expected route:

- index.html
- hq.html

Claims to verify:

- None

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
  "notes": "This is a verification lead, but the current evidence is too thin and external-source based to move forward without stronger validation. It overlaps existing HQ/progression intent and should not advance to a content workflow yet. Future trigger: Move to review only if canonical memory plus a second reliable source confirm a real dependency or planning gap. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Move to review only if canonical memory plus a second reliable source confirm a real dependency or planning gap.

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

The proposal is useful as a research validation signal, but the current evidence does not justify a content opportunity. It risks duplicating existing research coverage and relies on one external source. Future trigger: Revisit if branch naming, cost-table drift, or missing coverage is confirmed by owner review or a second authoritative source. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "The proposal is useful as a research validation signal, but the current evidence does not justify a content opportunity. It risks duplicating existing research coverage and relies on one external source. Future trigger: Revisit if branch naming, cost-table drift, or missing coverage is confirmed by owner review or a second authoritative source. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Revisit if branch naming, cost-table drift, or missing coverage is confirmed by owner review or a second authoritative source.

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

Search result evidence is too generic and can easily overlap the existing events guide without a distinct player job. It is not ready for human content review beyond monitoring. Future trigger: Reconsider if a specific event mechanic or schedule pattern is verified and clearly distinct from the current events page role.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle includes a science day for research points and a hero day for leveling heroes.

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
  "notes": "Search result evidence is too generic and can easily overlap the existing events guide without a distinct player job. It is not ready for human content review beyond monitoring. Future trigger: Reconsider if a specific event mechanic or schedule pattern is verified and clearly distinct from the current events page role."
}
```

Next step:

Reconsider if a specific event mechanic or schedule pattern is verified and clearly distinct from the current events page role.

### external-search-lastz-fandom-reference-laboratory-5

- Title: External search opportunity: Laboratory
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

The laboratory idea is a broad research topic with high duplication risk and no verified gap. The current signal is not strong enough for a new or updated content opportunity. Future trigger: Revisit if a verified missing mechanic, cost, or lab progression detail emerges from canonical memory plus another source.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research building page; confirms technologies are unlocked and improved through the lab.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-laboratory-5",
  "title": "External search opportunity: Laboratory",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "The laboratory idea is a broad research topic with high duplication risk and no verified gap. The current signal is not strong enough for a new or updated content opportunity. Future trigger: Revisit if a verified missing mechanic, cost, or lab progression detail emerges from canonical memory plus another source."
}
```

Next step:

Revisit if a verified missing mechanic, cost, or lab progression detail emerges from canonical memory plus another source.

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

The hero roster reference is likely to overlap existing heroes coverage and the source is not sufficient to justify a new action. It is better treated as monitor-only until a clear gap is verified. Future trigger: Move forward only if a distinct player job appears, such as a missing hero filter, stats conflict, or roster coverage gap confirmed by owner review.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero roster and equipment reference page with faction filters, level listings, and gear stat examples; useful for hero discovery and cross-checking hero-related entries.

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
  "notes": "The hero roster reference is likely to overlap existing heroes coverage and the source is not sufficient to justify a new action. It is better treated as monitor-only until a clear gap is verified. Future trigger: Move forward only if a distinct player job appears, such as a missing hero filter, stats conflict, or roster coverage gap confirmed by owner review."
}
```

Next step:

Move forward only if a distinct player job appears, such as a missing hero filter, stats conflict, or roster coverage gap confirmed by owner review.
