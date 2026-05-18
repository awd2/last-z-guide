# LLM Topic Discovery - 2026-05-18T20:19:38Z

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

Improves query-to-page match for Gift Center and redeem-code searchers, especially users looking for login, UID, and code redemption flow clarity.

Rationale:

Strong GSC signal on an existing cornerstone page with clear low-CTR queries and established cluster fit. This is a high-value candidate for human review because the user job is specific and the page already exists, reducing duplication risk. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. The page already serves the core intent, so any change must avoid overlapping with other economy pages or blurring cluster roles.

Expected route:

- index.html
- codes.html

Claims to verify:

- Gift Center-only redeem flow remains canonical.
- Gift rewards are delivered through the mailbox.
- Query intent is not already better served by another canonical page.

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
  "notes": "Strong GSC signal on an existing cornerstone page with clear low-CTR queries and established cluster fit. This is a high-value candidate for human review because the user job is specific and the page already exists, reducing duplication risk. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have an owner review the existing page intent, confirm canonical claims, and define a constrained update brief that preserves the Gift Center-only redeem flow.

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

Helps players quickly find schedule, day-by-day plan, and versus strategy details for the Alliance Duel event.

Rationale:

This is a clean existing-page opportunity with meaningful impressions, clicks, and position data. The search intent appears specific enough to justify human review for a targeted improvement rather than new content. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. The topic must stay within the Events cluster and avoid absorbing broader event-guide content that belongs elsewhere.

Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- The query intent is best served by alliance-duel.html.
- A first-screen improvement can solve the need without altering cornerstone structure beyond approved scope.

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
  "notes": "This is a clean existing-page opportunity with meaningful impressions, clicks, and position data. The search intent appears specific enough to justify human review for a targeted improvement rather than new content. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Review current event-page coverage, verify the primary query intent, and decide whether a narrow first-screen update would better satisfy searchers without expanding scope.

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

Reduces confusion around official routing, UID usage, and setup steps for players trying to redeem rewards or confirm the correct service flow.

Rationale:

The official domain reference is a useful discovery signal for validating Gift Center routing and redeem/store flow details. It is not proof by itself, but it is strong enough to merit a controlled human review because it aligns with a high-value existing page.

Duplication risk:

Medium. The topic could duplicate existing redeem-code or support guidance unless the distinct player job is defined carefully.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Official service routing matches the intended Gift Center flow.
- UID usage is current and accurate.
- The topic adds a distinct player job beyond existing redeem-code coverage.

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
  "notes": "The official domain reference is a useful discovery signal for validating Gift Center routing and redeem/store flow details. It is not proof by itself, but it is strong enough to merit a controlled human review because it aligns with a high-value existing page."
}
```

Next step:

Cross-check the official flow against canonical site memory and one additional reliable source before deciding whether gift-center-uid.html needs a scoped update.

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

Useful discovery signal, but too dependent on a single external source and high risk of duplicating existing progression coverage without a clearly distinct player job. Future trigger: Move forward only if canonical site memory and a second reliable source confirm a real gap in HQ planning or construction dependency coverage. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful discovery signal, but too dependent on a single external source and high risk of duplicating existing progression coverage without a clearly distinct player job. Future trigger: Move forward only if canonical site memory and a second reliable source confirm a real gap in HQ planning or construction dependency coverage. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Move forward only if canonical site memory and a second reliable source confirm a real gap in HQ planning or construction dependency coverage.

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

Research cost and branch coverage is plausible, but the external source is not enough proof and the topic risks becoming a broad catch-all for cost drift. Future trigger: Reconsider if owner review confirms missing branch coverage or repeated player confusion around research cost tables. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Research cost and branch coverage is plausible, but the external source is not enough proof and the topic risks becoming a broad catch-all for cost drift. Future trigger: Reconsider if owner review confirms missing branch coverage or repeated player confusion around research cost tables. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if owner review confirms missing branch coverage or repeated player confusion around research cost tables.

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

Search result is discovery-only and too dependent on external wording and unverified event claims; it also risks duplicating existing Events coverage. Future trigger: Monitor only until event mechanics, reward structure, and theme details are verified against canonical memory plus a second source.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Regular event with a Hero Initiative theme that awards points for using Heroic Experience, Fragments, and Prime Recruitment Tickets; also includes an Age of Science research theme.

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
  "notes": "Search result is discovery-only and too dependent on external wording and unverified event claims; it also risks duplicating existing Events coverage. Future trigger: Monitor only until event mechanics, reward structure, and theme details are verified against canonical memory plus a second source."
}
```

Next step:

Monitor only until event mechanics, reward structure, and theme details are verified against canonical memory plus a second source.

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

Discovery-only source with generic hero-context value, but not enough to justify a separate update without a verified gap or distinct player job. Future trigger: Revisit if hero-system coverage is shown to be incomplete or search demand indicates a specific missing hero overview gap.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page listing hero classes and major power components, useful for hero system context and cross-checking hero-related event hooks.

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
  "notes": "Discovery-only source with generic hero-context value, but not enough to justify a separate update without a verified gap or distinct player job. Future trigger: Revisit if hero-system coverage is shown to be incomplete or search demand indicates a specific missing hero overview gap."
}
```

Next step:

Revisit if hero-system coverage is shown to be incomplete or search demand indicates a specific missing hero overview gap.

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

Likely duplicates existing heroes coverage and relies on an external roster page as input, which is not sufficient for a new or updated proposal without cross-validation. Future trigger: Monitor for confirmed hero roster drift or a clearly missing hero page that cannot be satisfied by current heroes.html coverage.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero roster page with faction filters, hero levels, and equipment listings; useful for hero discovery and cross-checking character pages.

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
  "notes": "Likely duplicates existing heroes coverage and relies on an external roster page as input, which is not sufficient for a new or updated proposal without cross-validation. Future trigger: Monitor for confirmed hero roster drift or a clearly missing hero page that cannot be satisfied by current heroes.html coverage."
}
```

Next step:

Monitor for confirmed hero roster drift or a clearly missing hero page that cannot be satisfied by current heroes.html coverage.
