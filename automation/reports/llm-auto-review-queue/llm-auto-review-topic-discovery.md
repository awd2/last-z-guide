# LLM Topic Discovery - 2026-05-16T16:56:23Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`
- Source Scout request: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`
- Topics: 8
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Topic Proposals

### index-gsc-opportunity

- Title: GSC opportunity review: Last Z Guides — Research, Events, HQ, Heroes, and F2P Strategy
- Target: `index.html`
- Cluster: `Home`
- Action: `update_existing`
- Archetype: `home-hub`
- Priority: `high`
- Risk: `high`
- Confidence: `high`
- Prior review: `none`
- Human approval required: `true`

Player value:

Helps users land on the main hub faster and find the right cluster entry points for research and broader site navigation.

Rationale:

Strong GSC signal on the home hub with rising branded and research-related queries suggests a high-value improvement to query match and first-screen usefulness. It stays within the existing Home cluster and aligns with the site pattern of updating an established hub rather than creating new content.

Duplication risk:

Low, because this is a hub-page refinement with no obvious duplicate intent and an existing backlog history already points to a prior home-promotion effort.

Expected route:

- index.html

Claims to verify:

- Whether the rising query set reflects a stable intent pattern rather than a short-term fluctuation.
- Whether any alternate canonical page already serves the branded or research-guide intent better.

Evidence:

- GSC page signal: index.html had 10947 impressions, 823 clicks, 7.52% CTR, avg position 6.64.
- Rising query: `last z research guide` gained 11 impressions in the last 7-day comparison window.
- Rising query: `lastzguides.com` gained 3 impressions in the last 7-day comparison window.

Backlog Row Preview:

```json
{
  "topic_id": "index-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Guides — Research, Events, HQ, Heroes, and F2P Strategy",
  "cluster": "Home",
  "recommended_action": "update_existing",
  "archetype_suggestion": "home-hub",
  "target_page_or_slug": "index.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "high",
  "status": "candidate",
  "notes": "Strong GSC signal on the home hub with rising branded and research-related queries suggests a high-value improvement to query match and first-screen usefulness. It stays within the existing Home cluster and aligns with the site pattern of updating an established hub rather than creating new content."
}
```

Next step:

Send to human review for scoped update planning of index.html, with emphasis on headline, nav prominence, and query alignment without cluster drift.

### research-gsc-opportunity

- Title: GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path
- Target: `research.html`
- Cluster: `Research`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: `high`
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:

Improves access to the research order, peace shield context, and progression guidance for players seeking a reliable research route.

Rationale:

This is one of the strongest opportunities because the Research cornerstone has both page-level GSC signals and rising queries that point to concrete player jobs. It is also explicitly anchored to an existing cornerstone page, which makes it suitable for a controlled update review. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low to medium, because the query set could overlap with adjacent Research and progression content, but the canonical claims and route are already defined.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- Whether the rising queries map to the intended research-guide job rather than a different progression topic.
- Whether peace shield and rescue-related phrasing can be supported without changing the page beyond approved scope.

Evidence:

- GSC page signal: research.html had 13619 impressions, 670 clicks, 4.92% CTR, avg position 7.16.
- Rising query: `last z research guide` gained 11 impressions in the last 7-day comparison window.
- Rising query: `last z urgent rescue` gained 8 impressions in the last 7-day comparison window.
- Rising query: `urgent rescue last z` gained 3 impressions in the last 7-day comparison window.

Backlog Row Preview:

```json
{
  "topic_id": "research-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This is one of the strongest opportunities because the Research cornerstone has both page-level GSC signals and rising queries that point to concrete player jobs. It is also explicitly anchored to an existing cornerstone page, which makes it suitable for a controlled update review. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Route to human review for a constrained update proposal on research.html, with explicit protection of the listed canonical claims and cluster separation.

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

Improves the path for users looking for redeem codes, gift center login, and UID-related instructions.

Rationale:

The Economy cornerstone page shows meaningful impressions and low CTR on gift center and codes queries, which supports a targeted improvement review. The page already exists and has a clear internal route, so this is better treated as an update than a new page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because gift center and codes intents may overlap with other Economy pages or adjacent utility pages, so the role boundaries need review.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the page can satisfy the gift-center and redeem-code intent without breaking protected canonical claims.
- Whether another canonical page already serves the login or UID sub-intent more precisely.

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
  "notes": "The Economy cornerstone page shows meaningful impressions and low CTR on gift center and codes queries, which supports a targeted improvement review. The page already exists and has a clear internal route, so this is better treated as an update than a new page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for a scoped update proposal on codes.html, with checks that the page does not absorb content better handled by another canonical page.

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

Useful as a discovery signal, but it relies on a single external source and cannot be treated as proof for public routing or flow claims. It should not advance without additional verification. Future trigger: Revisit only after owner confirmation or a second reliable source validates the official flow and UID handling.

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
  "notes": "Useful as a discovery signal, but it relies on a single external source and cannot be treated as proof for public routing or flow claims. It should not advance without additional verification. Future trigger: Revisit only after owner confirmation or a second reliable source validates the official flow and UID handling."
}
```

Next step:

Revisit only after owner confirmation or a second reliable source validates the official flow and UID handling.

### external-hq-and-progression-reference-cross-check

- Title: External source opportunity: HQ and progression requirement cross-check
- Target: `hq.html`
- Cluster: `Progression`
- Action: `monitor`
- Archetype: `cornerstone-guide`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

This is an external-source cross-check idea with high verification risk and no evidence beyond the recorded reference. It is not ready for human review as a content opportunity. Future trigger: Revisit if the HQ dependency claims are confirmed by canonical site memory and an additional reliable source or owner approval.

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
  "notes": "This is an external-source cross-check idea with high verification risk and no evidence beyond the recorded reference. It is not ready for human review as a content opportunity. Future trigger: Revisit if the HQ dependency claims are confirmed by canonical site memory and an additional reliable source or owner approval."
}
```

Next step:

Revisit if the HQ dependency claims are confirmed by canonical site memory and an additional reliable source or owner approval.

### external-research-costs-external-cross-check

- Title: External source opportunity: research cost and branch coverage cross-check
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

The topic is too dependent on a single external reference and could easily drift into unverified cost or branch claims. It is discovery-only for now. Future trigger: Revisit after verification of branch names, costs, and naming drift from a second reliable source or owner input.

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
  "notes": "The topic is too dependent on a single external reference and could easily drift into unverified cost or branch claims. It is discovery-only for now. Future trigger: Revisit after verification of branch names, costs, and naming drift from a second reliable source or owner input."
}
```

Next step:

Revisit after verification of branch names, costs, and naming drift from a second reliable source or owner input.

### vehicle-modification-cost-gsc-opportunity

- Title: GSC opportunity review: Last Z Vehicle Modification Costs — Wrenches, Milestones, and Unlock Path
- Target: `vehicle-modification-cost.html`
- Cluster: `Equipment`
- Action: `monitor`
- Archetype: `cost-page`
- Priority: `low`
- Risk: ``
- Confidence: `high`
- Prior review: `none`
- Human approval required: `false`

Player value:



Rationale:

A valid existing-page update signal, but lower priority than Home, Research, and Economy because the evidence is weaker and the user job is less clearly differentiated. Future trigger: Revisit if vehicle-upgrade related queries continue to rise or if human review finds a strong unmet player job distinct from adjacent Equipment content.

Duplication risk:



Expected route:

- index.html
- gear.html
- vehicle-modification-cost.html

Claims to verify:

- None

Evidence:

- GSC page signal: vehicle-modification-cost.html had 7319 impressions, 480 clicks, 6.56% CTR, avg position 5.82.

Backlog Row Preview:

```json
{
  "topic_id": "vehicle-modification-cost-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Vehicle Modification Costs — Wrenches, Milestones, and Unlock Path",
  "cluster": "Equipment",
  "recommended_action": "monitor",
  "archetype_suggestion": "cost-page",
  "target_page_or_slug": "vehicle-modification-cost.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "A valid existing-page update signal, but lower priority than Home, Research, and Economy because the evidence is weaker and the user job is less clearly differentiated. Future trigger: Revisit if vehicle-upgrade related queries continue to rise or if human review finds a strong unmet player job distinct from adjacent Equipment content."
}
```

Next step:

Revisit if vehicle-upgrade related queries continue to rise or if human review finds a strong unmet player job distinct from adjacent Equipment content.

### alliance-duel-gsc-opportunity

- Title: GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy
- Target: `alliance-duel.html`
- Cluster: `Events`
- Action: `monitor`
- Archetype: `event-guide`
- Priority: `low`
- Risk: ``
- Confidence: `medium`
- Prior review: `closed`
- Human approval required: `false`

Player value:



Rationale:

A plausible existing-page update signal, but the evidence is comparatively narrow and does not rise above the top-priority opportunities. Future trigger: Revisit if event-related query demand increases or if schedule and VS intent prove to be a distinct, underserved player job. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:



Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- None

Evidence:

- GSC page signal: alliance-duel.html had 8965 impressions, 407 clicks, 4.54% CTR, avg position 6.19.

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
  "source_reference": "GSC weekly 2026-05-10: page opportunity and query-page signals",
  "confidence": "medium",
  "priority": "low",
  "status": "monitor",
  "notes": "A plausible existing-page update signal, but the evidence is comparatively narrow and does not rise above the top-priority opportunities. Future trigger: Revisit if event-related query demand increases or if schedule and VS intent prove to be a distinct, underserved player job. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Revisit if event-related query demand increases or if schedule and VS intent prove to be a distinct, underserved player job.
