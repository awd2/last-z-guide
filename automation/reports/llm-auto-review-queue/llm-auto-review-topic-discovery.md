# LLM Topic Discovery - 2026-05-18T18:42:12Z

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

Better match for last z vs schedule intent, faster event navigation, and clearer Day 1 to Day 6 planning for players searching the guide.

Rationale:

This is a strong page-level opportunity with meaningful impressions and clicks, and the target page already matches the event-guide archetype in the Events cluster. The request is focused on improving query-to-page alignment and first-screen usefulness rather than creating a new page, which fits the guardrails. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low. The proposal points to an existing canonical page and does not suggest a new competing guide.

Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- Whether alliance-duel.html is still the best canonical page for the target query intent.
- Whether any proposed content changes stay within approved scope and do not blur event cluster roles.

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
  "notes": "This is a strong page-level opportunity with meaningful impressions and clicks, and the target page already matches the event-guide archetype in the Events cluster. The request is focused on improving query-to-page alignment and first-screen usefulness rather than creating a new page, which fits the guardrails. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for scope confirmation against the existing event-guide template and cluster separation rules.

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

Better support for players searching for Gift Center login, UID, and redeem flow help, while keeping them on the correct canonical page.

Rationale:

This is the strongest signal in the set because the page already has significant impressions with low CTR and multiple low-CTR gift center queries. The page is a canonical cornerstone guide in Economy, so a careful update may improve query match and first-screen clarity without requiring structural changes. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. Gift Center intent can overlap with other economy pages, so role separation must be checked carefully.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether codes.html remains the correct canonical page for gift center intent.
- Whether the proposed update preserves gift-center-only-redeem-flow, gift-rewards-mailbox, and gift-center-cluster-role-separation claims.
- Whether any content changes would require moving the user to another canonical page instead.

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
  "notes": "This is the strongest signal in the set because the page already has significant impressions with low CTR and multiple low-CTR gift center queries. The page is a canonical cornerstone guide in Economy, so a careful update may improve query match and first-screen clarity without requiring structural changes. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Escalate for human review with a tight scope check focused on canonical claims and cluster separation.

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

Potentially improves accuracy for players trying to confirm official Gift Center setup and UID usage.

Rationale:

This is worth human review only as a validation topic, not as copy source material. The external official service domain may help confirm routing and flow details, but the claim set is thin and cannot be treated as proof without independent verification.

Duplication risk:

Medium to high. It may overlap with the existing Gift Center page unless a distinct player job is identified.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Whether the official routing and redeem/store flow details are still current.
- Whether this topic adds a distinct player job beyond the existing Gift Center page.
- Whether any phrasing would copy competitor wording or rely on a single external source.

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
  "notes": "This is worth human review only as a validation topic, not as copy source material. The external official service domain may help confirm routing and flow details, but the claim set is thin and cannot be treated as proof without independent verification."
}
```

Next step:

Review only if the team can verify the claims against canonical memory and at least one additional reliable source or owner confirmation.

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

Useful only as a verification lead, but the claim set is not yet strong enough for a reviewed content opportunity. It depends on external reference data and may duplicate existing progression coverage unless a distinct planning gap is proven. Future trigger: Move forward only after canonical-memory cross-checks and a second reliable source confirm a real progression planning gap. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful only as a verification lead, but the claim set is not yet strong enough for a reviewed content opportunity. It depends on external reference data and may duplicate existing progression coverage unless a distinct planning gap is proven. Future trigger: Move forward only after canonical-memory cross-checks and a second reliable source confirm a real progression planning gap. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Move forward only after canonical-memory cross-checks and a second reliable source confirm a real progression planning gap.

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

This is a discovery signal for branch coverage and cost drift, but it is too dependent on a single external source and carries high duplication risk with existing research coverage. Future trigger: Reconsider if multiple reliable sources or owner confirmation reveal a concrete cost-table or branch-name mismatch. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "This is a discovery signal for branch coverage and cost drift, but it is too dependent on a single external source and carries high duplication risk with existing research coverage. Future trigger: Reconsider if multiple reliable sources or owner confirmation reveal a concrete cost-table or branch-name mismatch. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if multiple reliable sources or owner confirmation reveal a concrete cost-table or branch-name mismatch.

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

External search result is discovery only and does not establish a distinct, verified player job. It is too speculative and could duplicate existing events coverage. Future trigger: Revisit if a verified event-category gap is identified and supported by canonical sources plus owner approval.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycles include research-speed tasks and hero upgrade tasks; useful for cross-checking event categories and rewards.

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
  "notes": "External search result is discovery only and does not establish a distinct, verified player job. It is too speculative and could duplicate existing events coverage. Future trigger: Revisit if a verified event-category gap is identified and supported by canonical sources plus owner approval."
}
```

Next step:

Revisit if a verified event-category gap is identified and supported by canonical sources plus owner approval.

### external-search-lastz-fandom-reference-heroes-5

- Title: External search opportunity: Heroes
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

This is a broad external discovery result with weak specificity. It does not justify a reviewed update without verified claims and a distinct content gap. Future trigger: Reconsider if there is a clearly missing hero-system explanation that cannot be served by existing research or heroes pages.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page with hero classes and power factors; useful for entity discovery around hero systems.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-heroes-5",
  "title": "External search opportunity: Heroes",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This is a broad external discovery result with weak specificity. It does not justify a reviewed update without verified claims and a distinct content gap. Future trigger: Reconsider if there is a clearly missing hero-system explanation that cannot be served by existing research or heroes pages."
}
```

Next step:

Reconsider if there is a clearly missing hero-system explanation that cannot be served by existing research or heroes pages.

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

The topic appears to be a generic hero index or tier-list style result and is likely to duplicate existing heroes coverage. It also depends on external wording that must not be copied. Future trigger: Only re-open if verification shows a non-duplicative player job, such as a missing roster or stats gap not already covered.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Core hero index with roster, faction tabs, levels, and equipment; useful for hero discovery and cross-checking character names.

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
  "notes": "The topic appears to be a generic hero index or tier-list style result and is likely to duplicate existing heroes coverage. It also depends on external wording that must not be copied. Future trigger: Only re-open if verification shows a non-duplicative player job, such as a missing roster or stats gap not already covered."
}
```

Next step:

Only re-open if verification shows a non-duplicative player job, such as a missing roster or stats gap not already covered.
