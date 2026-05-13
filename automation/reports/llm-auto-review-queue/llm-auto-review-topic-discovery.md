# LLM Topic Discovery - 2026-05-13T10:44:49Z

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

Better answer for players searching gift center, login, and redeem code flow terms; faster path to the right page from search.

Rationale:

Strong GSC signal for an existing cornerstone page with relevant low-CTR and mid-position queries. The topic matches the current page intent and can likely improve query-to-page fit without changing cluster roles. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because gift center intent may overlap with other economy pages and must preserve canonical claim boundaries.

Expected route:

- index.html
- codes.html

Claims to verify:

- The page can address the target queries without introducing new mechanics claims.
- The protected canonical claims remain intact: gift-center-only-redeem-flow, gift-rewards-mailbox, gift-center-cluster-role-separation.

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
  "notes": "Strong GSC signal for an existing cornerstone page with relevant low-CTR and mid-position queries. The topic matches the current page intent and can likely improve query-to-page fit without changing cluster roles. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should confirm whether codes.html can be improved within current scope while preserving the protected canonical claims and cluster separation.

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

Improves discoverability of the main guide hub and helps players reach research, events, HQ, heroes, and F2P strategy faster.

Rationale:

Strong home-page GSC signal with a clear need to improve first-screen usefulness for guide-oriented searches. The page already serves as the main entry point, so updating it is the lowest-risk path.

Duplication risk:

Low to medium, since home hub changes can accidentally overlap with cluster landing pages if scope is not controlled.

Expected route:

- index.html

Claims to verify:

- The homepage change can stay within existing template and navigation patterns.
- The page can support guide intent without collapsing into a duplicate of cluster pages.

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
  "notes": "Strong home-page GSC signal with a clear need to improve first-screen usefulness for guide-oriented searches. The page already serves as the main entry point, so updating it is the lowest-risk path."
}
```

Next step:

Human review should check whether the home page can better route searchers without weakening cluster navigation or duplicating topical hub content.

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

Helps players choose the best research path, understand peace shield value, and find urgent rescue guidance sooner.

Rationale:

This is a strong cornerstone-page opportunity with multiple rising queries and a clear user job around research order and urgent rescue intent. It also has explicit protected claims, which makes a careful update worthwhile for review. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, because research intent can overlap with costs, HQ, and progression pages if role boundaries are loosened.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- The target queries really belong on research.html rather than another canonical page.
- The protected canonical claims remain valid and do not conflict with adjacent pages: research-best-mainline, hero-training-cockpit-stop, peace-shield-value, research-atlas-role.

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
  "notes": "This is a strong cornerstone-page opportunity with multiple rising queries and a clear user job around research order and urgent rescue intent. It also has explicit protected claims, which makes a careful update worthwhile for review. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should verify that the page can cover the target queries while preserving the protected claims and not duplicating research-costs.html or HQ content.

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

Monitor only. It is based on a single external source and needs independent verification before any content workflow. It also risks duplicating existing gift center intent. Future trigger: Move forward only if the official flow and UID claims are confirmed by canonical site memory plus another reliable source or owner confirmation.

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
  "notes": "Monitor only. It is based on a single external source and needs independent verification before any content workflow. It also risks duplicating existing gift center intent. Future trigger: Move forward only if the official flow and UID claims are confirmed by canonical site memory plus another reliable source or owner confirmation."
}
```

Next step:

Move forward only if the official flow and UID claims are confirmed by canonical site memory plus another reliable source or owner confirmation.

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

Monitor only. The proposal depends on an external reference source and does not yet demonstrate a distinct player job that justifies a page update. Future trigger: Reconsider if HQ dependency data is verified from at least one additional reliable source and the topic can be framed as a distinct player need.

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
  "notes": "Monitor only. The proposal depends on an external reference source and does not yet demonstrate a distinct player job that justifies a page update. Future trigger: Reconsider if HQ dependency data is verified from at least one additional reliable source and the topic can be framed as a distinct player need."
}
```

Next step:

Reconsider if HQ dependency data is verified from at least one additional reliable source and the topic can be framed as a distinct player need.

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

Monitor only. It is research discovery, not a verified content need, and it risks importing source-specific wording or unsupported claims. Future trigger: Reconsider if cost and branch coverage gaps are confirmed by an additional source and map cleanly to an existing page role.

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
  "notes": "Monitor only. It is research discovery, not a verified content need, and it risks importing source-specific wording or unsupported claims. Future trigger: Reconsider if cost and branch coverage gaps are confirmed by an additional source and map cleanly to an existing page role."
}
```

Next step:

Reconsider if cost and branch coverage gaps are confirmed by an additional source and map cleanly to an existing page role.

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

Monitor only for now. The GSC signal is useful, but the topic appears to be a standard update to an existing cost page with no clear evidence of a distinct new player job beyond current coverage. Future trigger: Reconsider if query analysis shows a specific unmet intent that vehicle-modification-cost.html does not already cover.

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
  "notes": "Monitor only for now. The GSC signal is useful, but the topic appears to be a standard update to an existing cost page with no clear evidence of a distinct new player job beyond current coverage. Future trigger: Reconsider if query analysis shows a specific unmet intent that vehicle-modification-cost.html does not already cover."
}
```

Next step:

Reconsider if query analysis shows a specific unmet intent that vehicle-modification-cost.html does not already cover.

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

Monitor only for now. This is a routine event-page optimization with a weaker signal than the higher-priority cornerstone pages, and no new distinct player job is demonstrated. Future trigger: Reconsider if query patterns show a clear gap in event scheduling or VS strategy coverage that cannot be met by the current page. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Monitor only for now. This is a routine event-page optimization with a weaker signal than the higher-priority cornerstone pages, and no new distinct player job is demonstrated. Future trigger: Reconsider if query patterns show a clear gap in event scheduling or VS strategy coverage that cannot be met by the current page. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if query patterns show a clear gap in event scheduling or VS strategy coverage that cannot be met by the current page.
