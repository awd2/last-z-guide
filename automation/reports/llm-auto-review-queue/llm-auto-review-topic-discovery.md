# LLM Topic Discovery - 2026-05-15T10:39:24Z

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

Faster entry to the site and better routing for players searching for the main guide hub.

Rationale:

This is a clear existing-page update candidate. The home page already captures broad navigation intent, and the GSC signals show meaningful impressions with a rising research-related query. The opportunity is to improve first-screen usefulness and query-to-page match without changing the page role.

Duplication risk:

Low if kept as a home-hub refinement; medium if it starts absorbing cluster-specific intent.

Expected route:

- index.html

Claims to verify:

- Whether the rising query truly reflects guide-hub intent rather than a specific cluster page.
- Whether any home-page claim changes would weaken cluster role separation.

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
  "notes": "This is a clear existing-page update candidate. The home page already captures broad navigation intent, and the GSC signals show meaningful impressions with a rising research-related query. The opportunity is to improve first-screen usefulness and query-to-page match without changing the page role."
}
```

Next step:

Send to human review for an existing-page optimization brief focused on home-hub clarity and navigation.

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

Better answer coverage for research-order, urgent-rescue, and progression planning searches.

Rationale:

This is a strong cornerstone-page refresh candidate because the Research page has high impressions, relevant rising queries, and protected canonical claims. The proposed work fits an existing guide update, but only if it preserves the Research cluster role and does not overreach into other pages. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because some intent may overlap with other Research or Progression pages.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- That the research-order intent is not already better served by another canonical page.
- That protected claims such as research-best-mainline and peace-shield-value remain accurate.

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
  "notes": "This is a strong cornerstone-page refresh candidate because the Research page has high impressions, relevant rising queries, and protected canonical claims. The proposed work fits an existing guide update, but only if it preserves the Research cluster role and does not overreach into other pages. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Route to human review with a scope check against existing Research and Progression pages.

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

More direct help for players looking for redeem codes, Gift Center login, and UID-related entry points.

Rationale:

The codes page has strong volume and the listed queries show a focused Gift Center login and redeem-flow intent. This is a sensible update-existing candidate, but it must preserve canonical claims and avoid blurring the role with the UID support page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because Gift Center and UID intent can overlap with adjacent support content.

Expected route:

- index.html
- codes.html

Claims to verify:

- That gift-center-only-redeem-flow and gift-rewards-mailbox remain correct and unchanged.
- That the query intent is not better handled by gift-center-uid.html or another support page.

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
  "notes": "The codes page has strong volume and the listed queries show a focused Gift Center login and redeem-flow intent. This is a sensible update-existing candidate, but it must preserve canonical claims and avoid blurring the role with the UID support page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have a human reviewer confirm that the intended update stays inside the current codes page scope.

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

Monitor only. The proposal is based on a single external source and cannot be treated as proof for public routing or flow claims. It also risks duplication with existing Gift Center support intent. Future trigger: Move to review only if the official service flow is verified by another reliable source or owner confirmation.

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
  "source_reference": "official-functap-store: https://www.last-z.com",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor only. The proposal is based on a single external source and cannot be treated as proof for public routing or flow claims. It also risks duplication with existing Gift Center support intent. Future trigger: Move to review only if the official service flow is verified by another reliable source or owner confirmation."
}
```

Next step:

Move to review only if the official service flow is verified by another reliable source or owner confirmation.

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

Monitor only. This is discovery input, not enough to justify a page change. The source may help validate planning gaps later, but it does not yet support a content decision. Future trigger: Reconsider if HQ requirement details are verified against canonical site memory and another reliable source.

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
  "notes": "Monitor only. This is discovery input, not enough to justify a page change. The source may help validate planning gaps later, but it does not yet support a content decision. Future trigger: Reconsider if HQ requirement details are verified against canonical site memory and another reliable source."
}
```

Next step:

Reconsider if HQ requirement details are verified against canonical site memory and another reliable source.

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

Reject for now. The proposal depends on one external reference and could copy or mirror competitor wording if advanced too early. It is not ready for human content review. Future trigger: Only revisit if branch coverage, cost names, and claim accuracy are confirmed by independent sources or owner review.

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
  "notes": "Reject for now. The proposal depends on one external reference and could copy or mirror competitor wording if advanced too early. It is not ready for human content review. Future trigger: Only revisit if branch coverage, cost names, and claim accuracy are confirmed by independent sources or owner review."
}
```

Next step:

Only revisit if branch coverage, cost names, and claim accuracy are confirmed by independent sources or owner review.

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

Reject for now. The page signal is real, but the proposal text is too generic and the target intent is not yet specific enough to prove a distinct player job beyond an existing cost-page update. Future trigger: Reconsider if query analysis shows a specific vehicle upgrade task that is not already covered by the current Equipment page set.

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
  "notes": "Reject for now. The page signal is real, but the proposal text is too generic and the target intent is not yet specific enough to prove a distinct player job beyond an existing cost-page update. Future trigger: Reconsider if query analysis shows a specific vehicle upgrade task that is not already covered by the current Equipment page set."
}
```

Next step:

Reconsider if query analysis shows a specific vehicle upgrade task that is not already covered by the current Equipment page set.

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

Reject for now. The signal supports monitoring, but the proposed event framing is still broad and may not justify a human-review slot until the exact player job is clearer. Future trigger: Reconsider if season, schedule, or VS intent becomes more distinct and can be validated without changing scope. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Reject for now. The signal supports monitoring, but the proposed event framing is still broad and may not justify a human-review slot until the exact player job is clearer. Future trigger: Reconsider if season, schedule, or VS intent becomes more distinct and can be validated without changing scope. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if season, schedule, or VS intent becomes more distinct and can be validated without changing scope.
