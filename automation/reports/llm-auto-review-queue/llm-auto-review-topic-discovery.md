# LLM Topic Discovery - 2026-05-12T19:43:56Z

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

Helps players reach the correct redeem path faster and reduces confusion around login, UID, and gift-center entry points.

Rationale:

This is a strong existing-page opportunity. The query cluster shows repeated interest in Gift Center and redeem code intent, and the page already has a defined cornerstone role in Economy. The improvement likely belongs on codes.html, but only within the approved scope and without weakening cluster separation or protected claims. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. The query intent may overlap with other Economy pages, so the page role must stay sharply defined.

Expected route:

- index.html
- codes.html

Claims to verify:

- gift-center-only-redeem-flow
- gift-rewards-mailbox
- gift-center-cluster-role-separation

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
  "notes": "This is a strong existing-page opportunity. The query cluster shows repeated interest in Gift Center and redeem code intent, and the page already has a defined cornerstone role in Economy. The improvement likely belongs on codes.html, but only within the approved scope and without weakening cluster separation or protected claims. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for a scoped update_existing proposal on codes.html with claim protection checks.

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

Improves the landing experience for players looking for the main guide hub and helps route them to the right cluster pages.

Rationale:

Home page has meaningful traffic and rising branded/research-guide signals, which suggests an opportunity to improve first-screen routing and query match. This is appropriate as an existing-page optimization, not a new page.

Duplication risk:

Low to medium. The home page must not start acting like a duplicate of cluster pages.

Expected route:

- index.html

Claims to verify:

- None

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
  "notes": "Home page has meaningful traffic and rising branded/research-guide signals, which suggests an opportunity to improve first-screen routing and query match. This is appropriate as an existing-page optimization, not a new page."
}
```

Next step:

Route to human review for a constrained homepage update plan that preserves navigation patterns and cluster separation.

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

Gives players a clearer path for research order, rescue timing, and progression planning.

Rationale:

This is one of the strongest opportunities. Research.html has broad interest, rising research-guide queries, and additional urgent-rescue signals that suggest a real content alignment gap. It is already a cornerstone page, so the appropriate action is a controlled update, not a new article. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. It could overlap with other Research pages if the role is not kept focused.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- research-best-mainline
- hero-training-cockpit-stop
- peace-shield-value
- research-atlas-role

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
  "notes": "This is one of the strongest opportunities. Research.html has broad interest, rising research-guide queries, and additional urgent-rescue signals that suggest a real content alignment gap. It is already a cornerstone page, so the appropriate action is a controlled update, not a new article. Prior run `2026-05-12-research-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Move to human review for a scoped update_existing proposal on research.html with explicit claim protection and internal-route alignment.

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

Useful as discovery, but it depends on a single external source and cannot yet verify public claims. It also risks duplicating the existing Economy intent without a clearly distinct player job. Future trigger: Reconsider only after verification from canonical site memory plus at least one additional reliable source or owner confirmation.

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
  "notes": "Useful as discovery, but it depends on a single external source and cannot yet verify public claims. It also risks duplicating the existing Economy intent without a clearly distinct player job. Future trigger: Reconsider only after verification from canonical site memory plus at least one additional reliable source or owner confirmation."
}
```

Next step:

Reconsider only after verification from canonical site memory plus at least one additional reliable source or owner confirmation.

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

This is a cross-validation lead, not a content-ready opportunity. The proposal is too dependent on an external reference and lacks enough verified scope for human content review. Future trigger: Reconsider if HQ requirement data is confirmed by owner review or another reliable source and a distinct player job is identified.

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
  "notes": "This is a cross-validation lead, not a content-ready opportunity. The proposal is too dependent on an external reference and lacks enough verified scope for human content review. Future trigger: Reconsider if HQ requirement data is confirmed by owner review or another reliable source and a distinct player job is identified."
}
```

Next step:

Reconsider if HQ requirement data is confirmed by owner review or another reliable source and a distinct player job is identified.

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

Discovery-only signal. The proposed topic is speculative without verification and could duplicate existing Research intent without a distinct player need. Future trigger: Reconsider if branch and cost claims are confirmed by at least one additional reliable source and a clear coverage gap remains.

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
  "notes": "Discovery-only signal. The proposed topic is speculative without verification and could duplicate existing Research intent without a distinct player need. Future trigger: Reconsider if branch and cost claims are confirmed by at least one additional reliable source and a clear coverage gap remains."
}
```

Next step:

Reconsider if branch and cost claims are confirmed by at least one additional reliable source and a clear coverage gap remains.

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

A valid existing-page signal, but weaker than the selected Research, Home, and Economy items. It is better treated as lower-priority monitoring until stronger intent evidence appears. Future trigger: Reconsider if query volume, click trends, or support tickets show a more specific vehicle-upgrade intent gap.

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
  "notes": "A valid existing-page signal, but weaker than the selected Research, Home, and Economy items. It is better treated as lower-priority monitoring until stronger intent evidence appears. Future trigger: Reconsider if query volume, click trends, or support tickets show a more specific vehicle-upgrade intent gap."
}
```

Next step:

Reconsider if query volume, click trends, or support tickets show a more specific vehicle-upgrade intent gap.

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

A reasonable existing-page signal, but the evidence is only moderate and the query intent is less distinct than the selected opportunities. It does not need immediate human review ahead of higher-value items. Future trigger: Reconsider if event-season or schedule-related queries rise materially or if support data shows confusion around alliance duel timing. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "A reasonable existing-page signal, but the evidence is only moderate and the query intent is less distinct than the selected opportunities. It does not need immediate human review ahead of higher-value items. Future trigger: Reconsider if event-season or schedule-related queries rise materially or if support data shows confusion around alliance duel timing. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if event-season or schedule-related queries rise materially or if support data shows confusion around alliance duel timing.
