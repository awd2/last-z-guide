# LLM Topic Discovery - 2026-05-14T10:36:12Z

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

Better matches the main gift center and redeem-code intent, improving first-screen usefulness for searchers trying to find codes, login, UID, and redemption flow information.

Rationale:

This is a strong existing-page opportunity with clear query-page mismatch signals, high impressions, and an established canonical target page. It is also explicitly within a cornerstone page pattern, so the right action is to review an existing page rather than create new content. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. Similar intent may already be partially served by index.html or a related gift-center page, so role separation must be checked carefully.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether codes.html remains the best canonical page for these queries
- Whether the proposed changes preserve gift-center-only-redeem-flow
- Whether gift-rewards-mailbox and gift-center-cluster-role-separation stay intact

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
  "notes": "This is a strong existing-page opportunity with clear query-page mismatch signals, high impressions, and an established canonical target page. It is also explicitly within a cornerstone page pattern, so the right action is to review an existing page rather than create new content. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review to validate query intent, confirm canonical claim protection, and decide whether a scoped update to codes.html is justified.

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

Improves the landing experience for users who arrive with broad Last Z guides intent and may need a clearer path to research, events, HQ, heroes, or F2P strategy content.

Rationale:

The home page has strong impressions and some rising branded/research queries, which makes it a good candidate for a focused existing-page review. The evidence supports query-to-page alignment work, not a new page.

Duplication risk:

Medium. The home hub must not absorb topic-specific content that belongs in cluster pages.

Expected route:

- index.html

Claims to verify:

- Whether the rising queries represent durable intent
- Whether index.html can be improved without duplicating cluster pages
- Whether prior home-promotion work already covers the same need

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
  "notes": "The home page has strong impressions and some rising branded/research queries, which makes it a good candidate for a focused existing-page review. The evidence supports query-to-page alignment work, not a new page."
}
```

Next step:

Human review should confirm whether the home page can surface navigation and intent cues more effectively without blurring cluster roles.

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

Helps players find the correct research order, emergency coverage, Peace Shield context, and path guidance more quickly.

Rationale:

This is a high-value cornerstone-page review because the research page has meaningful traffic and query growth around research guide and urgent rescue terms. The page should be reviewed for query coverage and first-screen usefulness rather than replaced. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

High. Research content can easily overlap with HQ, costs, and the home hub, so the scope needs tight role separation.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- Whether research.html is still the best canonical destination for the reported queries
- Whether urgent rescue intent belongs here or on another page
- Whether the protected canonical claims remain accurate

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
  "notes": "This is a high-value cornerstone-page review because the research page has meaningful traffic and query growth around research guide and urgent rescue terms. The page should be reviewed for query coverage and first-screen usefulness rather than replaced. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Route to human review to validate intent splits and confirm that the page can be updated within the approved cornerstone scope.

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

Monitor only for now. The proposal depends on a single external source and is framed as cross-validation, not proof. It could be useful, but it does not yet meet the verification threshold for human content review. Future trigger: Reconsider if the official domain and at least one additional reliable source or owner confirmation validate the routing and UID claims.

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
  "notes": "Monitor only for now. The proposal depends on a single external source and is framed as cross-validation, not proof. It could be useful, but it does not yet meet the verification threshold for human content review. Future trigger: Reconsider if the official domain and at least one additional reliable source or owner confirmation validate the routing and UID claims."
}
```

Next step:

Reconsider if the official domain and at least one additional reliable source or owner confirmation validate the routing and UID claims.

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

Monitor only for now. The topic may be useful for verification, but it is still source-dependent and could duplicate existing HQ intent. It should not advance without stronger evidence. Future trigger: Reconsider after independent verification of HQ requirements and progression dependencies from another reliable source or owner confirmation.

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
  "notes": "Monitor only for now. The topic may be useful for verification, but it is still source-dependent and could duplicate existing HQ intent. It should not advance without stronger evidence. Future trigger: Reconsider after independent verification of HQ requirements and progression dependencies from another reliable source or owner confirmation."
}
```

Next step:

Reconsider after independent verification of HQ requirements and progression dependencies from another reliable source or owner confirmation.

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

Monitor only for now. The item is discovery-only and risks copying or overfitting to an external reference without enough validation. Future trigger: Reconsider if branch coverage and cost-table drift are confirmed by canonical site memory plus another reliable source.

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
  "notes": "Monitor only for now. The item is discovery-only and risks copying or overfitting to an external reference without enough validation. Future trigger: Reconsider if branch coverage and cost-table drift are confirmed by canonical site memory plus another reliable source."
}
```

Next step:

Reconsider if branch coverage and cost-table drift are confirmed by canonical site memory plus another reliable source.

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

Monitor for now. The GSC signal is useful, but the proposal is narrower than the strongest cornerstone opportunities and may already be covered by an existing equipment page without a distinct new player job. Future trigger: Reconsider if query analysis shows a persistent mismatch for vehicle upgrade intent that cannot be handled by another canonical page.

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
  "notes": "Monitor for now. The GSC signal is useful, but the proposal is narrower than the strongest cornerstone opportunities and may already be covered by an existing equipment page without a distinct new player job. Future trigger: Reconsider if query analysis shows a persistent mismatch for vehicle upgrade intent that cannot be handled by another canonical page."
}
```

Next step:

Reconsider if query analysis shows a persistent mismatch for vehicle upgrade intent that cannot be handled by another canonical page.

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

Monitor for now. This is a standard event-guide update candidate, but it is less compelling than the top cornerstone opportunities and currently lacks distinct evidence beyond page-level GSC signals. Future trigger: Reconsider if additional query data or owner feedback shows a clear schedule or VS-strategy gap on alliance-duel.html. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Monitor for now. This is a standard event-guide update candidate, but it is less compelling than the top cornerstone opportunities and currently lacks distinct evidence beyond page-level GSC signals. Future trigger: Reconsider if additional query data or owner feedback shows a clear schedule or VS-strategy gap on alliance-duel.html. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if additional query data or owner feedback shows a clear schedule or VS-strategy gap on alliance-duel.html.
