# LLM Topic Discovery - 2026-05-16T19:02:24Z

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

Improves the match for players searching for redeem codes, gift center login, and UID help without forcing them to hunt across the site.

Rationale:

This is the clearest analytics-backed opportunity. The page already ranks and receives meaningful impressions for gift center queries, but the low CTR suggests a possible query-to-page mismatch. It fits an existing cornerstone page and preserves cluster ownership if scope stays narrow. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. There is some risk of overlapping with other economy pages, but the canonical claim protections and existing route make the update path manageable.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether the query intent for last z gift center is best served by codes.html and not another canonical page.
- Whether any proposed copy would preserve gift-center-only-redeem-flow, gift-rewards-mailbox, and gift-center-cluster-role-separation.
- Whether prior backlog item gift-center-ctr-pass:done already covers the same fix.

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
  "notes": "This is the clearest analytics-backed opportunity. The page already ranks and receives meaningful impressions for gift center queries, but the low CTR suggests a possible query-to-page mismatch. It fits an existing cornerstone page and preserves cluster ownership if scope stays narrow. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should confirm whether the improvement can be handled within the current codes.html template and whether the protected canonical claims stay intact.

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

Helps players confirm official Gift Center setup, UID usage, and routing so they can redeem rewards correctly.

Rationale:

This is a strong cross-validation topic because official routing and store flow accuracy matter to the economy cluster. It is still only an external-source signal, so it needs verification before any content work.

Duplication risk:

Medium. The topic may overlap with codes.html unless the intended job is specifically UID and routing validation.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- Whether last-z.com is the authoritative route for the Gift Center or store flow.
- Whether the UID guidance adds a distinct user job from the main redeem codes page.
- Whether any public mechanic or routing detail can be confirmed by a second reliable source.

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
  "notes": "This is a strong cross-validation topic because official routing and store flow accuracy matter to the economy cluster. It is still only an external-source signal, so it needs verification before any content work."
}
```

Next step:

Verify the official service claims against canonical site memory plus another reliable source or owner confirmation before deciding whether this belongs on gift-center-uid.html or remains part of codes.html.

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

Helps players plan HQ requirements, dependencies, and upgrade order without misinformation.

Rationale:

HQ and progression planning is a real player job and the page fit is clear. The proposal is useful as a validation topic, but the source alone is not enough to justify public claims. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. It could overlap with other progression pages if scope is not tightly defined around HQ planning.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement steps and dependency order.
- Whether the referenced wiki content matches game reality.
- Whether the topic adds a distinct player job compared with existing progression coverage.

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
  "notes": "HQ and progression planning is a real player job and the page fit is clear. The proposal is useful as a validation topic, but the source alone is not enough to justify public claims. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Review canonical memory and a second reliable source to verify progression requirements before considering any page update on hq.html.

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

Useful discovery signal, but it is still a single external-source reference and the proposed cost and branch coverage claims are high risk without verification. Future trigger: Reconsider if official or owner-confirmed research tables expose a clear coverage gap or if a second reliable source corroborates the costs and branch naming. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "Useful discovery signal, but it is still a single external-source reference and the proposed cost and branch coverage claims are high risk without verification. Future trigger: Reconsider if official or owner-confirmed research tables expose a clear coverage gap or if a second reliable source corroborates the costs and branch naming. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if official or owner-confirmed research tables expose a clear coverage gap or if a second reliable source corroborates the costs and branch naming.

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

External search result only; the event claim is not verified and could easily duplicate or conflict with existing events coverage. Future trigger: Reopen if event mechanics and rewards are confirmed by canonical memory plus another reliable source or owner approval.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event with a research-focused cycle; one theme is Age of Science, which awards points for completing and speeding up technologies research.

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
  "notes": "External search result only; the event claim is not verified and could easily duplicate or conflict with existing events coverage. Future trigger: Reopen if event mechanics and rewards are confirmed by canonical memory plus another reliable source or owner approval."
}
```

Next step:

Reopen if event mechanics and rewards are confirmed by canonical memory plus another reliable source or owner approval.

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

This is a broad research/search discovery signal rather than a distinct page-ready opportunity, and it risks overlapping with other hero or research pages. Future trigger: Monitor for a clearly distinct player job, such as a hero-research linkage gap that is verified by reliable sources.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page that defines hero classes and power factors, useful for linking hero upgrade mechanics to event tasks.

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
  "notes": "This is a broad research/search discovery signal rather than a distinct page-ready opportunity, and it risks overlapping with other hero or research pages. Future trigger: Monitor for a clearly distinct player job, such as a hero-research linkage gap that is verified by reliable sources."
}
```

Next step:

Monitor for a clearly distinct player job, such as a hero-research linkage gap that is verified by reliable sources.

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

The hero hub is relevant, but the search result is source discovery only and may duplicate existing hero coverage without a distinct update need. Future trigger: Reconsider if human review confirms a specific missing roster, stat, or build gap that is verified and not already covered.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Core hero hub with character list, factions, levels, and equipment section; good lead for hero roster discovery and build references.

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
  "notes": "The hero hub is relevant, but the search result is source discovery only and may duplicate existing hero coverage without a distinct update need. Future trigger: Reconsider if human review confirms a specific missing roster, stat, or build gap that is verified and not already covered."
}
```

Next step:

Reconsider if human review confirms a specific missing roster, stat, or build gap that is verified and not already covered.

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

Research guide search result is informative, but the claim set is too dependent on external wording and may duplicate research.html without a unique player job. Future trigger: Reopen if verification shows a missing research subsection, badge-cost table, or branch coverage gap that is not already represented.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research hub with category tabs and level cost tables; useful for locating research categories and badge-cost structure.

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
  "notes": "Research guide search result is informative, but the claim set is too dependent on external wording and may duplicate research.html without a unique player job. Future trigger: Reopen if verification shows a missing research subsection, badge-cost table, or branch coverage gap that is not already represented."
}
```

Next step:

Reopen if verification shows a missing research subsection, badge-cost table, or branch coverage gap that is not already represented.
