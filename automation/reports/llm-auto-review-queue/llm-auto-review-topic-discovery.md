# LLM Topic Discovery - 2026-05-18T18:29:58Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`
- Source Scout request: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`
- Topics: 7
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

Helps players quickly find the alliance duel schedule, day-by-day plan, and strategy in one canonical place.

Rationale:

This is a strong existing-page opportunity with direct GSC signal, clear user intent around schedule and strategy, and low template risk. It aligns with the Events cluster and does not require a new content type. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Low if the page remains the canonical event guide and does not overlap another event page's role.

Expected route:

- index.html
- events.html
- alliance-duel.html

Claims to verify:

- Whether alliance-duel.html is still the best canonical page for last z vs schedule queries.
- Whether the proposed adjustments can stay within the existing event-guide template and cluster role.

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
  "notes": "This is a strong existing-page opportunity with direct GSC signal, clear user intent around schedule and strategy, and low template risk. It aligns with the Events cluster and does not require a new content type. Prior run `2026-05-10-alliance-duel-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review for scope confirmation against the current Events page map and query intent.

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

Improves findability for players trying to redeem codes, reach Gift Center, or confirm login and UID steps.

Rationale:

This page has the strongest analytics signal in the set and a well-defined search intent around Gift Center login and redeem flow. It is a valuable candidate for review, but it carries higher risk because protected canonical claims must stay intact. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium to high if the page starts overlapping with a separate Gift Center or account-setup page.

Expected route:

- index.html
- codes.html

Claims to verify:

- That codes.html remains the correct canonical page for redeem-code and Gift Center queries.
- That any revision preserves gift-center-only-redeem-flow, gift-rewards-mailbox, and gift-center-cluster-role-separation claims.
- That the improvement can be made without broadening the page beyond approved scope.

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
  "notes": "This page has the strongest analytics signal in the set and a well-defined search intent around Gift Center login and redeem flow. It is a valuable candidate for review, but it carries higher risk because protected canonical claims must stay intact. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Send to human review with explicit checks for cluster separation, protected claims, and whether another canonical page already serves the intent better.

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

External-source discovery only. It may be useful for later verification, but it is not ready for human review because the claim set is not yet cross-validated and could duplicate existing Gift Center guidance. Future trigger: Move to review only after canonical memory and at least one additional reliable source or owner confirmation verify the routing and redeem flow claims.

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
  "notes": "External-source discovery only. It may be useful for later verification, but it is not ready for human review because the claim set is not yet cross-validated and could duplicate existing Gift Center guidance. Future trigger: Move to review only after canonical memory and at least one additional reliable source or owner confirmation verify the routing and redeem flow claims."
}
```

Next step:

Move to review only after canonical memory and at least one additional reliable source or owner confirmation verify the routing and redeem flow claims.

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

External-source discovery only. The topic is plausible but currently lacks independent verification and could blur progression page boundaries. Future trigger: Reconsider if owner confirmation or a second reliable source validates the HQ requirement and dependency claims. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "External-source discovery only. The topic is plausible but currently lacks independent verification and could blur progression page boundaries. Future trigger: Reconsider if owner confirmation or a second reliable source validates the HQ requirement and dependency claims. Prior run `2026-05-16-external-hq-and-progression-reference-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Reconsider if owner confirmation or a second reliable source validates the HQ requirement and dependency claims.

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

External-source discovery only. The cost and branch coverage claims are not verified enough for a review step, and the topic risks copying reference framing. Future trigger: Promote only after the underlying cost-table and branch-name facts are confirmed from canonical memory plus another reliable source. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

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
  "notes": "External-source discovery only. The cost and branch coverage claims are not verified enough for a review step, and the topic risks copying reference framing. Future trigger: Promote only after the underlying cost-table and branch-name facts are confirmed from canonical memory plus another reliable source. Prior run `2026-05-16-external-research-costs-external-cross-check-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Promote only after the underlying cost-table and branch-name facts are confirmed from canonical memory plus another reliable source.

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

Monitor only. The source is a search-result discovery signal and does not yet justify a page change or a new topic without verification. Future trigger: Advance if a verified player job emerges and the event task mapping is confirmed by reliable sources or owner review.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycles include a research-focused phase and a hero-upgrade phase, useful for mapping event tasks tied to research and heroes.

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
  "notes": "Monitor only. The source is a search-result discovery signal and does not yet justify a page change or a new topic without verification. Future trigger: Advance if a verified player job emerges and the event task mapping is confirmed by reliable sources or owner review."
}
```

Next step:

Advance if a verified player job emerges and the event task mapping is confirmed by reliable sources or owner review.

### external-search-lastz-fandom-reference-laboratory-5

- Title: External search opportunity: Laboratory
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

Monitor only. This is a discovery signal for research-related routing, but the claim set is not yet strong enough for a review workflow. Future trigger: Revisit after validation confirms that Laboratory is the right canonical target for the research setup and unlock coverage.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Explains the building used for technologies research and unlock conditions, useful for cross-checking research-related event tasks.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-lastz-fandom-reference-laboratory-5",
  "title": "External search opportunity: Laboratory",
  "cluster": "Research",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:lastz.fandom.com Last Z heroes research events",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "Monitor only. This is a discovery signal for research-related routing, but the claim set is not yet strong enough for a review workflow. Future trigger: Revisit after validation confirms that Laboratory is the right canonical target for the research setup and unlock coverage."
}
```

Next step:

Revisit after validation confirms that Laboratory is the right canonical target for the research setup and unlock coverage.
