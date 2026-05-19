# LLM Topic Discovery - 2026-05-19T09:07:49Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`
- Source Scout request: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`
- Topics: 7
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

Helps players quickly find the event schedule, day-by-day plan, and matchup strategy without forcing them to hunt across the site.

Rationale:

This is a strong existing-page opportunity with high impressions, decent clicks, and a clear user job around schedule and strategy. The page already exists in the correct cluster, so the best path is to improve query alignment and first-screen usefulness rather than create new content. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low, because the page already exists and the topic is narrowly tied to the event-guide role.

Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- The search intent behind last z vs schedule is best served by alliance-duel.html.
- The page can be improved within the current template without altering cornerstone scope.

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
  "notes": "This is a strong existing-page opportunity with high impressions, decent clicks, and a clear user job around schedule and strategy. The page already exists in the correct cluster, so the best path is to improve query alignment and first-screen usefulness rather than create new content. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have an editor review the current page against the target query set and confirm whether a scoped update can improve intent match without changing cluster role.

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

Improves access to redeem and gift-center information for players who are searching for login, UID, or codes help.

Rationale:

This is the highest-signal opportunity in the set: the codes page has very large impressions and multiple low-CTR gift center queries that clearly indicate a query-to-page match issue. It is an existing cornerstone page, so an update review is appropriate if canonical claims remain protected. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low to medium, because the page is canonical but must preserve role separation and avoid overlap with other economy pages.

Expected route:

- index.html
- codes.html

Claims to verify:

- The query cluster around last z gift center belongs on codes.html.
- The update can preserve gift-center-only-redeem-flow, gift-rewards-mailbox, and gift-center-cluster-role-separation.

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
  "notes": "This is the highest-signal opportunity in the set: the codes page has very large impressions and multiple low-CTR gift center queries that clearly indicate a query-to-page match issue. It is an existing cornerstone page, so an update review is appropriate if canonical claims remain protected. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Route to human review for a scoped update plan that preserves canonical claims and checks whether the current page already covers the search intent adequately.

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

Useful discovery signal, but it depends on a single external source and could duplicate existing economy coverage. It is not verifiable enough for selection yet. Future trigger: Move forward only after canonical memory plus a second reliable source or owner confirmation validates the public routing and redeem flow claims.

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
  "notes": "Useful discovery signal, but it depends on a single external source and could duplicate existing economy coverage. It is not verifiable enough for selection yet. Future trigger: Move forward only after canonical memory plus a second reliable source or owner confirmation validates the public routing and redeem flow claims."
}
```

Next step:

Move forward only after canonical memory plus a second reliable source or owner confirmation validates the public routing and redeem flow claims.

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

This is external-source discovery only and carries high verification risk. It should not advance without stronger evidence. Future trigger: Reconsider if owner-confirmed progression data or another reliable source confirms the HQ requirement and dependency claims. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "This is external-source discovery only and carries high verification risk. It should not advance without stronger evidence. Future trigger: Reconsider if owner-confirmed progression data or another reliable source confirms the HQ requirement and dependency claims. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if owner-confirmed progression data or another reliable source confirms the HQ requirement and dependency claims.

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

The proposal is based on one external reference and is not yet safe to turn into an actionable content opportunity. Future trigger: Review again if multiple reliable sources confirm cost, branch coverage, or naming drift issues. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "The proposal is based on one external reference and is not yet safe to turn into an actionable content opportunity. Future trigger: Review again if multiple reliable sources confirm cost, branch coverage, or naming drift issues. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Review again if multiple reliable sources confirm cost, branch coverage, or naming drift issues.

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

Search-result evidence is too thin and may duplicate existing events coverage or rely on competitor phrasing. Not ready for human review as a content proposal. Future trigger: Reassess when claims are validated against canonical memory and a second source, and when a distinct player job is identified.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle includes an Age of Science theme for tech research and a Hero Initiative theme for hero upgrades; useful for event discovery and reward cross-checks.

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
  "notes": "Search-result evidence is too thin and may duplicate existing events coverage or rely on competitor phrasing. Not ready for human review as a content proposal. Future trigger: Reassess when claims are validated against canonical memory and a second source, and when a distinct player job is identified."
}
```

Next step:

Reassess when claims are validated against canonical memory and a second source, and when a distinct player job is identified.

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

This is discovery-only evidence and needs verification before it can become a content proposal. It also risks duplicating existing research coverage. Future trigger: Reconsider if official or owner-confirmed sources validate the lab and technology claims as a distinct update need.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core research building page; confirms where technologies are researched and that an extra lab can unlock later.

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
  "notes": "This is discovery-only evidence and needs verification before it can become a content proposal. It also risks duplicating existing research coverage. Future trigger: Reconsider if official or owner-confirmed sources validate the lab and technology claims as a distinct update need."
}
```

Next step:

Reconsider if official or owner-confirmed sources validate the lab and technology claims as a distinct update need.
