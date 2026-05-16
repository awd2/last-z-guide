# LLM Topic Discovery - 2026-05-16T17:27:25Z

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

Helps players reach the redeem flow faster and find the correct gift center path, UID usage, and active code context with less friction.

Rationale:

This is the clearest high-value opportunity. The page already has strong impressions and mid-page ranking signals, and the query set suggests a query-to-page mismatch problem rather than a need for a new page. The opportunity fits the existing cornerstone-guide role for codes.html and should be reviewed as an update to improve usefulness and CTR without changing cluster boundaries. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium. The topic could overlap with other economy or redeem pages if the scope expands beyond the approved cornerstone role, so role separation must be protected.

Expected route:

- index.html
- codes.html

Claims to verify:

- The query intent is best served by codes.html and not another canonical page.
- Any suggested improvement can be made without changing approved canonical claims or blurring cluster role separation.
- The reported GSC signals are sufficient to justify review but not proof of rewrite need.

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
  "notes": "This is the clearest high-value opportunity. The page already has strong impressions and mid-page ranking signals, and the query set suggests a query-to-page mismatch problem rather than a need for a new page. The opportunity fits the existing cornerstone-guide role for codes.html and should be reviewed as an update to improve usefulness and CTR without changing cluster boundaries. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Human review should confirm whether the current codes.html can satisfy the search intent with scoped improvements only, and verify that no other canonical page serves the intent better.

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

Helps players confirm the official gift center route, UID usage, and store flow so they do not waste time on incorrect setup steps.

Rationale:

This is a valid cross-validation opportunity because it points to official routing and gift center flow accuracy, which can improve trust and reduce confusion. It is still source-light and must not be treated as proof, but it is aligned with the existing gift-center-uid.html intent and worth human review if the claims can be verified.

Duplication risk:

Medium. This may duplicate existing economy content unless the validation angle creates a distinct player job.

Expected route:

- index.html
- gift-center-uid.html

Claims to verify:

- The official service domain really supports the described Gift Center and store flow.
- UID handling and routing details match current canonical knowledge.
- The topic adds a distinct player job beyond existing economy content.

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
  "notes": "This is a valid cross-validation opportunity because it points to official routing and gift center flow accuracy, which can improve trust and reduce confusion. It is still source-light and must not be treated as proof, but it is aligned with the existing gift-center-uid.html intent and worth human review if the claims can be verified."
}
```

Next step:

Verify the official routing and gift center behavior against canonical site memory plus at least one additional reliable source or owner confirmation.

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

Helps players plan HQ upgrades, construction dependencies, and progression order with fewer mistakes.

Rationale:

HQ and progression dependency coverage is a strong fit for the Progression cluster and likely improves planning accuracy for players. It is appropriate as an update_existing candidate only if the claims are confirmed beyond the single external reference and the page can stay within its existing role.

Duplication risk:

Medium. The topic could overlap with generic progression or base-building coverage if scope is not tightly defined.

Expected route:

- index.html
- hq.html

Claims to verify:

- HQ requirement and dependency details are accurate.
- The external reference is consistent with canonical game knowledge.
- The update does not blur progression cluster boundaries.

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
  "notes": "HQ and progression dependency coverage is a strong fit for the Progression cluster and likely improves planning accuracy for players. It is appropriate as an update_existing candidate only if the claims are confirmed beyond the single external reference and the page can stay within its existing role."
}
```

Next step:

Check whether hq.html already covers the same dependency set and validate any missing claims with reliable sources or owner confirmation.

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

Monitor-only for now. It is a useful validation signal for research cost and branch coverage, but it depends on external information that is not yet verified beyond one source. Future trigger: Move forward only if canonical memory plus another reliable source or owner approval confirms the branch and cost details.

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
  "notes": "Monitor-only for now. It is a useful validation signal for research cost and branch coverage, but it depends on external information that is not yet verified beyond one source. Future trigger: Move forward only if canonical memory plus another reliable source or owner approval confirms the branch and cost details."
}
```

Next step:

Move forward only if canonical memory plus another reliable source or owner approval confirms the branch and cost details.

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

Monitor-only for now. The event claims are discovery signals, but the source is not enough to support public mechanic or cycle claims without additional verification. Future trigger: Advance only after second-source validation and confirmation that the event cycle is current and not outdated or duplicated.

Duplication risk:



Expected route:

- events.html

Claims to verify:

- None

Evidence:

- Daily event cycle with an Age of Science phase tied to technologic research, plus a Hero Initiative phase tied to hero upgrades and recruitment tickets.

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
  "notes": "Monitor-only for now. The event claims are discovery signals, but the source is not enough to support public mechanic or cycle claims without additional verification. Future trigger: Advance only after second-source validation and confirmation that the event cycle is current and not outdated or duplicated."
}
```

Next step:

Advance only after second-source validation and confirmation that the event cycle is current and not outdated or duplicated.

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

Monitor-only for now. This looks like a broad research cross-check rather than a distinct player job, and it needs stronger validation before review. Future trigger: Proceed only if it exposes a specific gap in research.html that cannot be covered by existing content.

Duplication risk:



Expected route:

- research.html

Claims to verify:

- None

Evidence:

- Core hero overview page with hero classes, power sources, and upgrade-related concepts that can support hero event cross-checking.

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
  "notes": "Monitor-only for now. This looks like a broad research cross-check rather than a distinct player job, and it needs stronger validation before review. Future trigger: Proceed only if it exposes a specific gap in research.html that cannot be covered by existing content."
}
```

Next step:

Proceed only if it exposes a specific gap in research.html that cannot be covered by existing content.

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

Monitor-only for now. The hero roster and equipment hub may be useful, but it is still an external-search signal and could duplicate existing heroes coverage. Future trigger: Advance if a distinct hero discovery or faction-browsing gap is confirmed by canonical review.

Duplication risk:



Expected route:

- heroes.html

Claims to verify:

- None

Evidence:

- Hero roster and equipment hub; useful for hero discovery, faction browsing, and character/equipment cross-checks.

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
  "notes": "Monitor-only for now. The hero roster and equipment hub may be useful, but it is still an external-search signal and could duplicate existing heroes coverage. Future trigger: Advance if a distinct hero discovery or faction-browsing gap is confirmed by canonical review."
}
```

Next step:

Advance if a distinct hero discovery or faction-browsing gap is confirmed by canonical review.

### external-search-mmediamreza-last-z-reference-assaulter-camp-guide-train-faster-gain-pow-8

- Title: External search opportunity: Assaulter Camp Guide - Train Faster & Gain Power - | Last Z: Survival Shooter
- Target: `power-guide.html`
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

High verification risk and possible duplicate or speculative mechanic claims. This could be a distinct player job, but the external source alone is not enough to prove the mechanic, cost, reward, or progression details. Future trigger: Reconsider only if the Assaulter Camp claims are verified by canonical memory plus an additional reliable source or owner confirmation.

Duplication risk:



Expected route:

- power-guide.html

Claims to verify:

- None

Evidence:

- Guide page for the Assaulter Camp with training cap, speed bonuses, power gains, and progression milestones.

Backlog Row Preview:

```json
{
  "topic_id": "external-search-mmediamreza-last-z-reference-assaulter-camp-guide-train-faster-gain-pow-8",
  "title": "External search opportunity: Assaulter Camp Guide - Train Faster & Gain Power - | Last Z: Survival Shooter",
  "cluster": "Progression",
  "recommended_action": "monitor",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "power-guide.html",
  "source_type": "llm_scout",
  "source_reference": "External search: site:mmediamreza.com Last Z Survival Shooter",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "High verification risk and possible duplicate or speculative mechanic claims. This could be a distinct player job, but the external source alone is not enough to prove the mechanic, cost, reward, or progression details. Future trigger: Reconsider only if the Assaulter Camp claims are verified by canonical memory plus an additional reliable source or owner confirmation."
}
```

Next step:

Reconsider only if the Assaulter Camp claims are verified by canonical memory plus an additional reliable source or owner confirmation.
