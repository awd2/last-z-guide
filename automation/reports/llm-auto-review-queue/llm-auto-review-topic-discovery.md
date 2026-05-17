# LLM Topic Discovery - 2026-05-17T15:36:01Z

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

Helps searchers land faster on the redeem-code and gift-center answer they already want, with better first-screen clarity and less friction from ambiguous query intent.

Rationale:

This is the clearest high-value opportunity. The GSC signal shows strong impressions and a low CTR on the existing codes page, and the proposal is already aligned to an existing cornerstone page and route. It appears to improve query-page fit without needing a new page or cluster change, as long as the approved scope keeps the cluster role intact. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low. This is anchored to an existing page and canonical route, with explicit role-separation constraints.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the query set is best served by codes.html rather than another canonical page
- Whether any proposed copy changes preserve gift-center-only-redeem-flow
- Whether gift-rewards-mailbox and gift-center-cluster-role-separation remain intact

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
  "notes": "This is the clearest high-value opportunity. The GSC signal shows strong impressions and a low CTR on the existing codes page, and the proposal is already aligned to an existing cornerstone page and route. It appears to improve query-page fit without needing a new page or cluster change, as long as the approved scope keeps the cluster role intact. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for scoped update planning, with explicit checks on canonical claims and no cluster-role drift.

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

Reduces confusion about official routing, UID usage, and where players should complete gift-center actions.

Rationale:

The official site reference may help validate routing and flow terminology for the Gift Center, but it is only a discovery signal. It is still worth human review because it can improve accuracy on an existing Economy page if verified against canonical memory and another reliable source.

Duplication risk:

Medium. The topic is close to the existing Gift Center intent and could duplicate current coverage if not narrowed to a distinct verification job.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Exact official Gift Center routing and store flow
- Whether UID usage is described accurately on the target page
- Whether the topic adds a distinct player job beyond existing Gift Center coverage

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
  "notes": "The official site reference may help validate routing and flow terminology for the Gift Center, but it is only a discovery signal. It is still worth human review because it can improve accuracy on an existing Economy page if verified against canonical memory and another reliable source."
}
```

Next step:

Verify the claim set with canonical site memory and at least one additional reliable source or owner confirmation before any content proposal work.

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

Helps players plan headquarters progression, dependencies, and unlock timing more reliably.

Rationale:

HQ and progression dependency accuracy is a useful verification task for the Progression cluster, and the page fit is plausible. However, the proposal remains source-dependent and needs validation before it can become a content direction. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. It may overlap with current HQ or progression explanations unless a specific gap is identified.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement sequence
- Construction dependency ordering
- Whether the external reference exposes a real coverage gap

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
  "notes": "HQ and progression dependency accuracy is a useful verification task for the Progression cluster, and the page fit is plausible. However, the proposal remains source-dependent and needs validation before it can become a content direction. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Treat as a verification-only candidate and confirm the specific missing dependency or planning gap before any page-level recommendation.

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

Useful as a verification signal, but too dependent on a single external reference and too likely to overlap existing Research coverage without a clearly distinct user job. Future trigger: Advance only if a second reliable source or owner confirmation shows a concrete branch, naming, or cost-table gap. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful as a verification signal, but too dependent on a single external reference and too likely to overlap existing Research coverage without a clearly distinct user job. Future trigger: Advance only if a second reliable source or owner confirmation shows a concrete branch, naming, or cost-table gap. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Advance only if a second reliable source or owner confirmation shows a concrete branch, naming, or cost-table gap.

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

External search result only; claims are not verified enough for a page update decision, and the event scope may overlap existing event coverage. Future trigger: Revisit if the event mechanic and date-specific details are confirmed by canonical memory and a second source.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle includes an Age of Science theme for technology research, plus a Hero Initiative theme tied to hero XP, fragments, and recruitment tickets.

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
  "notes": "External search result only; claims are not verified enough for a page update decision, and the event scope may overlap existing event coverage. Future trigger: Revisit if the event mechanic and date-specific details are confirmed by canonical memory and a second source."
}
```

Next step:

Revisit if the event mechanic and date-specific details are confirmed by canonical memory and a second source.

### external-search-lastz-fandom-reference-laboratory-last-z-survival-shooter-wiki-fa-6

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

The topic is a source-led validation idea for Research, not a ready content opportunity. It needs verification before it can be advanced. Future trigger: Revisit if a verified gap in research unlock rules or badge costs is identified.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Explains the building used to research technologies and its unlock rules.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-laboratory-last-z-survival-shooter-wiki-fa-6",
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
  "notes": "The topic is a source-led validation idea for Research, not a ready content opportunity. It needs verification before it can be advanced. Future trigger: Revisit if a verified gap in research unlock rules or badge costs is identified."
}
```

Next step:

Revisit if a verified gap in research unlock rules or badge costs is identified.

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

This is too close to a general hero hub and could duplicate existing Heroes coverage without a distinct player job. Future trigger: Monitor for a specific roster, faction, or equipment coverage gap that is not already handled by the hub.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Main hero hub with a long roster, faction filters, levels, and hero equipment sections; good for hero discovery and cross-checking character names.

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
  "notes": "This is too close to a general hero hub and could duplicate existing Heroes coverage without a distinct player job. Future trigger: Monitor for a specific roster, faction, or equipment coverage gap that is not already handled by the hub."
}
```

Next step:

Monitor for a specific roster, faction, or equipment coverage gap that is not already handled by the hub.

### external-search-lastzwiki-reference-laboratory-badges-in-last-z-complete-resea-2

- Title: External search opportunity: Laboratory Badges in Last Z - Complete Research Guide | Last Z Wiki
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

External search evidence is too thin and the likely subject overlaps other Research pages; not ready for human review as a page opportunity. Future trigger: Revisit only if the page reveals a unique badge-cost structure or unlock rule gap that can be verified.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page with category tabs and level-by-level badge costs; useful for locating research names and checking upgrade costs.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastzwiki-reference-laboratory-badges-in-last-z-complete-resea-2",
  "title": "External search opportunity: Laboratory Badges in Last Z - Complete Research Guide | Last Z Wiki",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastzwiki.com/en Last Z guide heroes research",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "External search evidence is too thin and the likely subject overlaps other Research pages; not ready for human review as a page opportunity. Future trigger: Revisit only if the page reveals a unique badge-cost structure or unlock rule gap that can be verified."
}
```

Next step:

Revisit only if the page reveals a unique badge-cost structure or unlock rule gap that can be verified.
