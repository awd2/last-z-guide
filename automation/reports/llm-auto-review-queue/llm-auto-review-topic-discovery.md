# LLM Topic Discovery - 2026-05-17T08:51:53Z

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

Helps players find redeem, gift center, and login guidance faster when searching for codes and related account flow questions.

Rationale:

This has the clearest first-party signal: high impressions on a relevant page plus multiple low-CTR gift center queries. The opportunity fits the existing cornerstone guide and can improve query-to-page match while preserving cluster separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. The page already owns the core redeem intent, so changes must stay within the approved scope and avoid overlap with adjacent support content.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the low CTR is caused by title, snippet, or page structure rather than intent mismatch
- Whether any proposed wording preserves gift-center-only-redeem-flow, gift-rewards-mailbox, and gift-center-cluster-role-separation
- Whether another canonical page already serves part of the gift center login intent better

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
  "notes": "This has the clearest first-party signal: high impressions on a relevant page plus multiple low-CTR gift center queries. The opportunity fits the existing cornerstone guide and can improve query-to-page match while preserving cluster separation. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for scoped update planning against codes.html, with explicit protection of the canonical gift center claims.

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

Could improve confidence that players are using the correct official Gift Center route and setup flow.

Rationale:

The official service domain is a strong cross-validation candidate for Gift Center routing and store flow, but it is still only a discovery signal. It is useful if verified, because it may tighten accuracy around a high-value player task.

Duplication risk:

Medium. This may duplicate existing redeem or account-flow guidance unless the topic is narrowed to a distinct verification job.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Official routing and domain ownership
- Whether UID usage and store flow details are current
- Whether this adds a distinct player job beyond existing redeem guidance

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
  "notes": "The official service domain is a strong cross-validation candidate for Gift Center routing and store flow, but it is still only a discovery signal. It is useful if verified, because it may tighten accuracy around a high-value player task."
}
```

Next step:

Keep as a human-reviewed verification task for gift-center-uid.html, with at least one additional reliable source or owner confirmation before any content proposal.

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

Can help players plan HQ progression, dependencies, and route order more reliably.

Rationale:

HQ and progression dependencies are important guide material, but this proposal is still only a cross-check signal from an external reference. It is worth review because progression gaps can create broad player confusion if the page is stale. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. HQ content may already be covered elsewhere, so this must stay focused on requirement planning rather than general progression copy.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement chain
- Construction dependencies
- Any progression-route coverage gaps versus current canonical knowledge

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
  "notes": "HQ and progression dependencies are important guide material, but this proposal is still only a cross-check signal from an external reference. It is worth review because progression gaps can create broad player confusion if the page is stale. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Route to human review for hq.html as a verification task, not a content rewrite, and require corroboration from another source or owner memory.

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

Useful only as a discovery signal until verified; the topic is high risk for cost and naming accuracy and could easily duplicate existing research coverage. Future trigger: Revisit if a second reliable source or owner confirmation validates a specific missing research branch or cost drift. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful only as a discovery signal until verified; the topic is high risk for cost and naming accuracy and could easily duplicate existing research coverage. Future trigger: Revisit if a second reliable source or owner confirmation validates a specific missing research branch or cost drift. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Revisit if a second reliable source or owner confirmation validates a specific missing research branch or cost drift.

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

External search result is discovery only and appears broad. It needs verification before any page-level action, and may overlap with existing events coverage. Future trigger: Reconsider if event timing, reward mechanics, or hero-use cycles are confirmed by canonical memory plus another reliable source.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event with a research-focused cycle and hero-use cycle; useful for linking research, heroes, and reward timing.

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
  "notes": "External search result is discovery only and appears broad. It needs verification before any page-level action, and may overlap with existing events coverage. Future trigger: Reconsider if event timing, reward mechanics, or hero-use cycles are confirmed by canonical memory plus another reliable source."
}
```

Next step:

Reconsider if event timing, reward mechanics, or hero-use cycles are confirmed by canonical memory plus another reliable source.

### external-search-lastz-fandom-reference-heroes-last-z-survival-shooter-wiki-fandom-5

- Title: External search opportunity: Heroes | Last Z: Survival Shooter Wiki | Fandom
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

This is a generic heroes overview search result and likely duplicates existing hero coverage unless a distinct player job is proven. Future trigger: Monitor for a verified gap in hero classes, stat systems, or event-linked hero planning that is not already covered.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page listing hero classes and the main stat systems that can tie into event scoring or upgrade planning.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-heroes-last-z-survival-shooter-wiki-fandom-5",
  "title": "External search opportunity: Heroes | Last Z: Survival Shooter Wiki | Fandom",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "This is a generic heroes overview search result and likely duplicates existing hero coverage unless a distinct player job is proven. Future trigger: Monitor for a verified gap in hero classes, stat systems, or event-linked hero planning that is not already covered."
}
```

Next step:

Monitor for a verified gap in hero classes, stat systems, or event-linked hero planning that is not already covered.

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

Search result is discovery-only and may copy or duplicate competitor structure. It is not ready for a human review slot without verified differentiation. Future trigger: Reconsider if a unique hero discovery or faction-check job is validated against canonical memory and another source.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Detailed hero roster page with hero lists, levels, and equipment sections; useful for hero discovery and faction checks.

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
  "notes": "Search result is discovery-only and may copy or duplicate competitor structure. It is not ready for a human review slot without verified differentiation. Future trigger: Reconsider if a unique hero discovery or faction-check job is validated against canonical memory and another source."
}
```

Next step:

Reconsider if a unique hero discovery or faction-check job is validated against canonical memory and another source.

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

This is a research-table discovery signal only. It is too easy to overfit to a competitor layout or duplicate existing research coverage without a distinct player job. Future trigger: Revisit if a verified research cost drift or missing badge-cost branch is confirmed by a second source or owner approval.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page with category breakdowns and level-by-level badge costs; useful for research discovery and cost cross-checks.

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
  "notes": "This is a research-table discovery signal only. It is too easy to overfit to a competitor layout or duplicate existing research coverage without a distinct player job. Future trigger: Revisit if a verified research cost drift or missing badge-cost branch is confirmed by a second source or owner approval."
}
```

Next step:

Revisit if a verified research cost drift or missing badge-cost branch is confirmed by a second source or owner approval.
