# LLM Topic Discovery - 2026-05-18T17:25:25Z

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

Helps players find schedule, day-by-day plan, and matchup strategy faster from the existing Alliance Duel page.

Rationale:

This is a clear existing-page opportunity with strong GSC signals and a well-matched event-guide archetype. The query intent appears aligned to an existing Events page, and the proposal fits the prefer-update-existing rule without requiring new content. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low, because the topic maps to an established event-guide page and does not require a new page if scope stays within the current cluster role.

Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- Whether the current page already satisfies the dominant query intent better than a rewrite.
- Whether the proposed improvements can be made without changing the page beyond approved scope.

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
  "notes": "This is a clear existing-page opportunity with strong GSC signals and a well-matched event-guide archetype. The query intent appears aligned to an existing Events page, and the proposal fits the prefer-update-existing rule without requiring new content. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have an editor confirm query intent, first-screen usefulness, and whether the current page can cover the search need without broad scope changes.

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

Improves how players reach redeem codes and Gift Center login help from the current cornerstone page.

Rationale:

This is the highest-value page opportunity by volume, with multiple low-CTR gift-center queries pointing at the existing codes page. It is still a high-risk page because the canonical gift-center claims must be protected and cluster roles should remain distinct, but the signal is strong enough for human review. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because gift-center intent can overlap with UID, login, and redeem flow topics if cluster separation is not preserved.

Expected route:

- index.html
- codes.html

Claims to verify:

- That the gift-center-only redeem flow remains accurate and unchanged.
- That Gift Center mailbox reward handling and UID guidance are still correct.
- That the page can absorb the query intent without violating cluster role separation.

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
  "notes": "This is the highest-value page opportunity by volume, with multiple low-CTR gift-center queries pointing at the existing codes page. It is still a high-risk page because the canonical gift-center claims must be protected and cluster roles should remain distinct, but the signal is strong enough for human review. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Review the current codes page against the protected canonical claims and confirm whether a scoped update can improve query match without blurring other Economy pages.

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

Could improve trust and clarity for players trying to reach the official Gift Center and understand the redeem/store flow.

Rationale:

This is worth human review as a verification task, not as a copy source. The official domain may help validate routing and flow accuracy for an existing Economy support page, but the claim set must be independently confirmed before any content work.

Duplication risk:

High, because this likely overlaps with existing Gift Center and codes intent and may duplicate established coverage.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Official service routing for Gift Center.
- Whether the Gift Center flow differs from current canonical guidance.
- Whether this topic adds a distinct user job beyond existing Economy coverage.

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
  "notes": "This is worth human review as a verification task, not as a copy source. The official domain may help validate routing and flow accuracy for an existing Economy support page, but the claim set must be independently confirmed before any content work."
}
```

Next step:

Verify the official routing and flow against canonical site memory and one additional reliable source before deciding whether the current page needs a scoped update.

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

Monitor only until the reference can be verified against canonical memory and a second reliable source. It is a useful discovery signal, but not ready for content workflow because the external source alone cannot prove public HQ claims. Future trigger: Move to review only after owner confirmation or independent cross-validation of HQ requirements and progression dependencies. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Monitor only until the reference can be verified against canonical memory and a second reliable source. It is a useful discovery signal, but not ready for content workflow because the external source alone cannot prove public HQ claims. Future trigger: Move to review only after owner confirmation or independent cross-validation of HQ requirements and progression dependencies. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Move to review only after owner confirmation or independent cross-validation of HQ requirements and progression dependencies.

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

Monitor only. The source suggests a possible research cost and branch coverage check, but the claims are unverified and could overlap with existing Research pages. Future trigger: Advance only if a second source or owner confirmation shows a genuine gap in research cost or branch coverage coverage. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Monitor only. The source suggests a possible research cost and branch coverage check, but the claims are unverified and could overlap with existing Research pages. Future trigger: Advance only if a second source or owner confirmation shows a genuine gap in research cost or branch coverage coverage. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Advance only if a second source or owner confirmation shows a genuine gap in research cost or branch coverage coverage.

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

Reject for now. The search result is discovery evidence only, and the page/topic appears too broad and too dependent on third-party wording to justify a content proposal. Future trigger: Reconsider only if independent verification identifies a distinct event-job gap that cannot be served by the current Events page.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle page with a research-focused theme and a hero-focused theme; useful for cross-checking event tasks and rewards structure.

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
  "notes": "Reject for now. The search result is discovery evidence only, and the page/topic appears too broad and too dependent on third-party wording to justify a content proposal. Future trigger: Reconsider only if independent verification identifies a distinct event-job gap that cannot be served by the current Events page."
}
```

Next step:

Reconsider only if independent verification identifies a distinct event-job gap that cannot be served by the current Events page.

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

Reject for now. This is a generic search discovery item and does not establish a distinct enough new user job beyond existing Research coverage. Future trigger: Reconsider only if owner review confirms a specific missing research mechanic or progression detail that is not already covered.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research building page; confirms the Lab unlock and that it handles technology research, which fits research-event cross checks.

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
  "notes": "Reject for now. This is a generic search discovery item and does not establish a distinct enough new user job beyond existing Research coverage. Future trigger: Reconsider only if owner review confirms a specific missing research mechanic or progression detail that is not already covered."
}
```

Next step:

Reconsider only if owner review confirms a specific missing research mechanic or progression detail that is not already covered.

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

Reject for now. The hero roster and tier-list search result is too broad and too risky for duplication, and it depends on competitor framing that should not be copied. Future trigger: Reconsider only if there is a verified, site-specific gap in Heroes coverage that cannot be served by the current page set.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero roster and equipment page; useful for hero discovery, factions, levels, and gear categories.

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
  "notes": "Reject for now. The hero roster and tier-list search result is too broad and too risky for duplication, and it depends on competitor framing that should not be copied. Future trigger: Reconsider only if there is a verified, site-specific gap in Heroes coverage that cannot be served by the current page set."
}
```

Next step:

Reconsider only if there is a verified, site-specific gap in Heroes coverage that cannot be served by the current page set.
