# LLM Topic Discovery - 2026-05-17T09:36:41Z

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

Improves first-screen usefulness and helps players find the right redeem and gift-center flow faster.

Rationale:

This is the clearest direct opportunity because it combines strong GSC demand with an existing cornerstone page and an existing backlog history. It is a real query-to-page mismatch signal, not just generic traffic. Human review is warranted to see whether the current page can better answer Gift Center and login-intent queries without breaking cluster boundaries. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because the intent may already be partially covered by a canonical economy page and could overlap with other code or gift-center content.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the current page already fully covers Gift Center login and UID intent.
- Whether any rewrite would blur separation from other Economy cluster pages.
- Whether the approved scope can stay within the existing cornerstone template.

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
  "notes": "This is the clearest direct opportunity because it combines strong GSC demand with an existing cornerstone page and an existing backlog history. It is a real query-to-page mismatch signal, not just generic traffic. Human review is warranted to see whether the current page can better answer Gift Center and login-intent queries without breaking cluster boundaries. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for scope check against canonical claims and cluster separation before any proposal work.

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

Helps players confirm the official Gift Center flow, UID usage, and where to go for setup or redemption.

Rationale:

The official domain is a strong validation source for routing and flow questions, but this is still discovery-only and cannot stand alone as proof. It is worth human review because it may resolve a real player job around setup and service routing if corroborated by canonical memory and another reliable source.

Duplication risk:

Medium, because it may overlap with the existing Gift Center or codes pages if the job is not carefully separated.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Official routing and whether it matches the current site structure.
- Whether UID usage details are still current.
- Whether the topic adds a distinct job beyond the existing Gift Center and codes pages.

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
  "notes": "The official domain is a strong validation source for routing and flow questions, but this is still discovery-only and cannot stand alone as proof. It is worth human review because it may resolve a real player job around setup and service routing if corroborated by canonical memory and another reliable source."
}
```

Next step:

Verify against canonical site memory and a second reliable source or owner confirmation before any content proposal.

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

Reduces confusion about HQ requirements, dependencies, and progression planning.

Rationale:

HQ and progression planning is a plausible player job and the reference source may expose gaps in requirement coverage. It is suitable for human review because progression pages often drift and need periodic cross-checking, but the claims must be independently verified before they can shape any proposal. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, since it could overlap with an existing HQ or progression page unless a distinct gap is confirmed.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement chain and dependency order.
- Whether the reference data matches the current game state.
- Whether there is a distinct progression gap not already covered elsewhere.

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
  "notes": "HQ and progression planning is a plausible player job and the reference source may expose gaps in requirement coverage. It is suitable for human review because progression pages often drift and need periodic cross-checking, but the claims must be independently verified before they can shape any proposal. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Cross-check against canonical memory and at least one additional reliable source before deciding whether a proposal is warranted.

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

Useful as discovery, but too source-dependent and too close to existing Research coverage to advance now. It needs stronger verification and a clearer unique player job. Future trigger: Revisit if multiple independent sources confirm a missing research branch or cost-table drift. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful as discovery, but too source-dependent and too close to existing Research coverage to advance now. It needs stronger verification and a clearer unique player job. Future trigger: Revisit if multiple independent sources confirm a missing research branch or cost-table drift. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Revisit if multiple independent sources confirm a missing research branch or cost-table drift.

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

Event claims are highly sensitive and the proposal is based on search discovery only. It is not ready for human review without stronger validation and a clearer scope. Future trigger: Revisit if the event is confirmed in canonical memory or by reliable second-source evidence.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event with an Age of Science research theme and a Hero Initiative hero-upgrade theme, plus reward tiers and ranking payouts.

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
  "notes": "Event claims are highly sensitive and the proposal is based on search discovery only. It is not ready for human review without stronger validation and a clearer scope. Future trigger: Revisit if the event is confirmed in canonical memory or by reliable second-source evidence."
}
```

Next step:

Revisit if the event is confirmed in canonical memory or by reliable second-source evidence.

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

This is likely a general Heroes index or tier-list style result and may duplicate existing Heroes coverage. It needs a clearly distinct player job before moving forward. Future trigger: Revisit if a verifiable coverage gap appears, such as missing roster metadata or filtering structure.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero index page with roster, faction filters, levels, and equipment entries; good lead for hero discovery and character cross-checking.

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
  "notes": "This is likely a general Heroes index or tier-list style result and may duplicate existing Heroes coverage. It needs a clearly distinct player job before moving forward. Future trigger: Revisit if a verifiable coverage gap appears, such as missing roster metadata or filtering structure."
}
```

Next step:

Revisit if a verifiable coverage gap appears, such as missing roster metadata or filtering structure.

### external-search-lastzwiki-reference-laboratory-badges-in-last-z-complete-resea-2

- Title: External search opportunity: Laboratory Badges in Last Z - Complete Research Guide | Last Z Wiki
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

Research-cost coverage is already a likely existing intent, and this search result is not enough to prove a new page need. Treat as monitor-only until a real gap is verified. Future trigger: Revisit if there is confirmed cost-table drift or a missing research category that players need.

Duplication risk:



Expected route:

- research-costs.html

Claims to verify:

- None

Evidence:

- Research table page with category tabs and per-level badge cost tables; useful for locating research names and cost patterns.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastzwiki-reference-laboratory-badges-in-last-z-complete-resea-2",
  "title": "External search opportunity: Laboratory Badges in Last Z - Complete Research Guide | Last Z Wiki",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "atlas-page",
  "target_page_or_slug": "research-costs.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastzwiki.com/en Last Z guide heroes research",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Research-cost coverage is already a likely existing intent, and this search result is not enough to prove a new page need. Treat as monitor-only until a real gap is verified. Future trigger: Revisit if there is confirmed cost-table drift or a missing research category that players need."
}
```

Next step:

Revisit if there is confirmed cost-table drift or a missing research category that players need.

### external-search-mmediamreza-last-z-reference-assaulter-camp-guide-train-faster-gain-pow-8

- Title: External search opportunity: Assaulter Camp Guide - Train Faster & Gain Power - | Last Z: Survival Shooter
- Target: `about.html`
- Cluster: `Site`
- Action: `monitor`
- Archetype: `site-page`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

This is too thin and looks more like a generic troop-building article than a distinct opportunity for this site. It risks duplication and source copying concerns. Future trigger: Revisit only if a clearly unique troop progression job is identified and verified independently.

Duplication risk:



Expected route:

- about.html

Claims to verify:

- None

Evidence:

- Dedicated guide for Assaulter Camp training, cap, speed bonuses, and power growth; good compare point for troop-building pages.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-mmediamreza-last-z-reference-assaulter-camp-guide-train-faster-gain-pow-8",
  "title": "External search opportunity: Assaulter Camp Guide - Train Faster & Gain Power - | Last Z: Survival Shooter",
  "cluster": "Site",
  "recommended_action": "monitor",
  "archetype_suggestion": "site-page",
  "target_page_or_slug": "about.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:mmediamreza.com Last Z Survival Shooter",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This is too thin and looks more like a generic troop-building article than a distinct opportunity for this site. It risks duplication and source copying concerns. Future trigger: Revisit only if a clearly unique troop progression job is identified and verified independently."
}
```

Next step:

Revisit only if a clearly unique troop progression job is identified and verified independently.
