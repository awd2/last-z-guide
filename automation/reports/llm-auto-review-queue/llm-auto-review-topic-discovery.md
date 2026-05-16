# LLM Topic Discovery - 2026-05-16T18:04:55Z

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

Players searching for Gift Center and redeem code help should reach the right page faster and understand the login, UID, and redemption flow more quickly.

Rationale:

This is the strongest signal-based opportunity. The page already exists, the query intent is clear, and the proposed change stays within an established cornerstone-guide scope. It can improve query-to-page match without needing a new page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low if role separation is preserved; medium if the page expands into overlapping economy topics beyond its current scope.

Expected route:

- index.html
- codes.html

Claims to verify:

- The search queries actually indicate a page mismatch rather than a temporary ranking fluctuation.
- The canonical claims gift-center-only-redeem-flow, gift-rewards-mailbox, and gift-center-cluster-role-separation remain intact after any update.
- The target page is still the best canonical home for Gift Center and redeem code intent.

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
  "notes": "This is the strongest signal-based opportunity. The page already exists, the query intent is clear, and the proposed change stays within an established cornerstone-guide scope. It can improve query-to-page match without needing a new page. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should validate whether the current first-screen content can be improved without changing canonical claims or blurring cluster boundaries.

### external-hq-and-progression-reference-cross-check

- Title: External source opportunity: HQ and progression requirement cross-check
- Target: `hq.html`
- Cluster: `Progression`
- Action: `update_existing`
- Archetype: `cornerstone-guide`
- Priority: `high`
- Risk: `high`
- Confidence: `high`
- Prior review: `none`
- Human approval required: `true`

Player value:

Players planning upgrades get more reliable dependency and requirement guidance, which helps avoid wasted resources and mis-sequenced builds.

Rationale:

The topic has a distinct player job: verifying HQ requirements and progression dependencies. It fits the existing Progression cluster and is better treated as a refinement of hq.html than a new page.

Duplication risk:

Medium, because progression content often overlaps with broader base and upgrade guides.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement and dependency details can be verified from canonical memory plus a second reliable source or owner confirmation.
- The page does not duplicate existing progression coverage on another page.
- The external source is supportive only and not used as proof on its own.

Evidence:

- Owner-approved wiki/reference source can reveal HQ and progression planning gaps.
- External source URL recorded for later manual verification.

Backlog Row Preview:

```json
{
  "topic_id": "external-hq-and-progression-reference-cross-check",
  "title": "External source opportunity: HQ and progression requirement cross-check",
  "cluster": "Progression",
  "recommended_action": "update_existing",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "hq.html",
  "source_type": "llm_scout",
  "source_reference": "lastzwiki-reference: https://lastzwiki.com",
  "confidence": "high",
  "priority": "high",
  "status": "candidate",
  "notes": "The topic has a distinct player job: verifying HQ requirements and progression dependencies. It fits the existing Progression cluster and is better treated as a refinement of hq.html than a new page."
}
```

Next step:

Human review should confirm that the page can add verifiable requirement details without copying external wording or duplicating other progression pages.

### external-research-costs-external-cross-check

- Title: External source opportunity: research cost and branch coverage cross-check
- Target: `research-costs.html`
- Cluster: `Research`
- Action: `monitor`
- Archetype: `atlas-page`
- Priority: `low`
- Risk: `high`
- Confidence: `high`
- Prior review: `closed`
- Human approval required: `false`

Player value:

Players can avoid outdated research planning if branch names, costs, and table coverage are accurate and current.

Rationale:

This is a useful cross-check opportunity for research-cost and branch coverage drift. It has enough practical player value to justify review, but only as an update to the existing research-costs page. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium, since cost and branch coverage can overlap with general research and HQ planning pages.

Expected route:

- index.html
- research-costs.html

Claims to verify:

- Research branch naming and cost tables can be verified against reliable references.
- The topic does not merely restate what research.html already covers.
- No single external source is treated as proof for costs or progression claims.

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
  "notes": "This is a useful cross-check opportunity for research-cost and branch coverage drift. It has enough practical player value to justify review, but only as an update to the existing research-costs page. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should verify whether the page needs a targeted correction pass or only a small coverage expansion.

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

The source is useful for discovery, but the proposal is too dependent on a single external reference and could duplicate existing Gift Center intent without adding a clearly distinct player job. Future trigger: Move to review only if official routing or UID flow changes are confirmed by canonical memory plus another reliable source or owner confirmation.

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
  "notes": "The source is useful for discovery, but the proposal is too dependent on a single external reference and could duplicate existing Gift Center intent without adding a clearly distinct player job. Future trigger: Move to review only if official routing or UID flow changes are confirmed by canonical memory plus another reliable source or owner confirmation."
}
```

Next step:

Move to review only if official routing or UID flow changes are confirmed by canonical memory plus another reliable source or owner confirmation.

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

The event concept is interesting but currently too speculative. It relies on external search discovery and unverified claims about event themes and rewards. Future trigger: Reconsider if event mechanics and rewards are confirmed by canonical memory and at least one additional reliable source or owner approval.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycles include a research-focused theme and a hero-upgrade theme, with points tied to research speedups and hero materials.

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
  "notes": "The event concept is interesting but currently too speculative. It relies on external search discovery and unverified claims about event themes and rewards. Future trigger: Reconsider if event mechanics and rewards are confirmed by canonical memory and at least one additional reliable source or owner approval."
}
```

Next step:

Reconsider if event mechanics and rewards are confirmed by canonical memory and at least one additional reliable source or owner approval.

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

This appears to duplicate a broader heroes overview intent and does not yet show a distinct enough player job to justify a separate update. Future trigger: Reconsider if the page scope can be narrowed to a concrete gap such as class explanation, stat interpretation, or event linkage.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page; identifies hero classes and lists the main power factors, useful for linking hero growth to event objectives.

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
  "notes": "This appears to duplicate a broader heroes overview intent and does not yet show a distinct enough player job to justify a separate update. Future trigger: Reconsider if the page scope can be narrowed to a concrete gap such as class explanation, stat interpretation, or event linkage."
}
```

Next step:

Reconsider if the page scope can be narrowed to a concrete gap such as class explanation, stat interpretation, or event linkage.

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

Likely duplicate of existing heroes coverage and too dependent on external wording patterns, with a high risk of overlapping with current roster content. Future trigger: Reconsider if there is a clear missing subtopic, such as a structured stats glossary or a verified roster gap.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Dedicated heroes page with roster, hero stats/equipment sections, and character-level guide content.

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
  "notes": "Likely duplicate of existing heroes coverage and too dependent on external wording patterns, with a high risk of overlapping with current roster content. Future trigger: Reconsider if there is a clear missing subtopic, such as a structured stats glossary or a verified roster gap."
}
```

Next step:

Reconsider if there is a clear missing subtopic, such as a structured stats glossary or a verified roster gap.

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

This is research-only discovery material and may overlap with broader research guidance. It is not clearly distinct enough to advance now. Future trigger: Reconsider if players need a dedicated lab badge cost reference that cannot be cleanly integrated into research.html. 

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Research table page covering 9 laboratory categories and level-by-level badge costs.

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
  "notes": "This is research-only discovery material and may overlap with broader research guidance. It is not clearly distinct enough to advance now. Future trigger: Reconsider if players need a dedicated lab badge cost reference that cannot be cleanly integrated into research.html. "
}
```

Next step:

Reconsider if players need a dedicated lab badge cost reference that cannot be cleanly integrated into research.html.
