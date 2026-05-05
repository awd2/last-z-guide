# LLM Topic Discovery - 2026-05-05T18:50:04Z

## Overview

- State: `topic_discovery_ready`
- Source Scout result: `automation/reports/llm-scout-review-result.json`
- Source Scout request: `automation/reports/llm-scout-review-request.json`
- Topics: 3
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

Faster access to gift center login, redeem flow, and UID guidance from the main redeem-codes entry page.

Rationale:

High impressions with weak CTR on a cornerstone Economy page and multiple related gift-center queries suggest a meaningful existing-page optimization opportunity. The intent appears close to the current canonical role, so this is a strong candidate for a scoped update rather than new content. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity.

Duplication risk:

Medium; gift-center intent could overlap with other Economy pages if the rewrite expands beyond the canonical redeem flow.

Expected route:

- index.html
- codes.html

Claims to verify:

- Whether `last z gift center` intent is fully served by codes.html as the canonical page.
- Whether protected claims `gift-center-only-redeem-flow`, `gift-rewards-mailbox`, and `gift-center-cluster-role-separation` remain intact after any change.
- Whether the prior `gift-center-ctr-pass:done` history already exhausted the safest optimization surface.

Evidence:

- GSC page signal: codes.html had 14781 impressions, 254 clicks, 1.72% CTR, avg position 6.55.
- Low CTR query: `last z gift center` had 1548 impressions, 51 clicks, 3.29% CTR, position 7.25.
- Low CTR query: `last z gift center login` had 511 impressions, 13 clicks, 2.54% CTR, position 6.04.
- Low CTR query: `last-z.com gift center` had 276 impressions, 13 clicks, 4.71% CTR, position 6.25.
- Rising query: `last z gift center` gained 350 impressions in the last 7-day comparison window.

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
  "source_reference": "GSC weekly 2026-04-30: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "low",
  "status": "monitor",
  "notes": "High impressions with weak CTR on a cornerstone Economy page and multiple related gift-center queries suggest a meaningful existing-page optimization opportunity. The intent appears close to the current canonical role, so this is a strong candidate for a scoped update rather than new content. Prior run `2026-05-05-codes-gsc-opportunity-llm-approved-intake` is `closed`; keep this topic in monitoring unless new evidence materially changes the opportunity."
}
```

Next step:

Have the page owner review whether the first screen, headings, and snippet alignment can better answer gift-center queries without altering cluster separation.

### research-gsc-opportunity

- Title: GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path
- Target: `research.html`
- Cluster: `Research`
- Action: `update_existing`
- Archetype: `cornerstone-guide`
- Priority: `high`
- Risk: `high`
- Confidence: `high`
- Prior review: `none`
- Human approval required: `true`

Player value:

Helps players find the best research order, peace shield guidance, and T10 progression path more quickly.

Rationale:

Research.html shows strong impressions but middling CTR, and the rising rescue-related query suggests an adjacent, high-value intent to test against the current page framing. This is a solid human-review candidate because it could improve navigation to the correct research path without creating a duplicate guide.

Duplication risk:

Medium; rescue-intent coverage could blur Research cluster boundaries if it begins to absorb battle or event content.

Expected route:

- index.html
- research.html
- research-costs.html

Claims to verify:

- Whether `urgent rescue last z` belongs on research.html or a different canonical page.
- Whether protected claims `research-best-mainline`, `hero-training-cockpit-stop`, `peace-shield-value`, and `research-atlas-role` remain true after updates.

Evidence:

- GSC page signal: research.html had 11557 impressions, 519 clicks, 4.49% CTR, avg position 7.34.
- Rising query: `urgent rescue last z` gained 13 impressions in the last 7-day comparison window.

Backlog Row Preview:

```json
{
  "topic_id": "research-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path",
  "cluster": "Research",
  "recommended_action": "update_existing",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "research.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-04-30: page opportunity and query-page signals",
  "confidence": "high",
  "priority": "high",
  "status": "candidate",
  "notes": "Research.html shows strong impressions but middling CTR, and the rising rescue-related query suggests an adjacent, high-value intent to test against the current page framing. This is a solid human-review candidate because it could improve navigation to the correct research path without creating a duplicate guide."
}
```

Next step:

Review whether the page intro and section ordering can address search intent better while preserving Research cluster roles and protected claims.

### heroes-gsc-opportunity

- Title: GSC opportunity review: Last Z Best Heroes Tier List — Season 4 Rankings by Faction
- Target: `heroes.html`
- Cluster: `Heroes`
- Action: `update_existing`
- Archetype: `cornerstone-guide`
- Priority: `high`
- Risk: `high`
- Confidence: `medium`
- Prior review: `none`
- Human approval required: `true`

Player value:

Helps players quickly identify the best heroes and faction rankings for the current season.

Rationale:

Heroes.html has substantial impressions but low CTR, indicating a likely query-to-page mismatch or weak snippet/intro performance. A scoped cornerstone refresh could better satisfy season-specific hero tier-list searches while staying within the current page archetype.

Duplication risk:

Medium; tier-list framing can overlap with other hero or faction pages if the scope expands too broadly.

Expected route:

- index.html
- heroes.html

Claims to verify:

- Whether `last z season 4 heroes` is best answered by heroes.html.
- Whether the page can remain the canonical hero cornerstone without crossing into faction-specific duplication.

Evidence:

- GSC page signal: heroes.html had 12912 impressions, 298 clicks, 2.31% CTR, avg position 7.98.

Backlog Row Preview:

```json
{
  "topic_id": "heroes-gsc-opportunity",
  "title": "GSC opportunity review: Last Z Best Heroes Tier List — Season 4 Rankings by Faction",
  "cluster": "Heroes",
  "recommended_action": "update_existing",
  "archetype_suggestion": "cornerstone-guide",
  "target_page_or_slug": "heroes.html",
  "source_type": "llm_scout",
  "source_reference": "GSC weekly 2026-04-30: page opportunity and query-page signals",
  "confidence": "medium",
  "priority": "high",
  "status": "candidate",
  "notes": "Heroes.html has substantial impressions but low CTR, indicating a likely query-to-page mismatch or weak snippet/intro performance. A scoped cornerstone refresh could better satisfy season-specific hero tier-list searches while staying within the current page archetype."
}
```

Next step:

Have the owner confirm whether the title, intro, and top-of-page content can better reflect seasonal hero ranking intent without creating a redundant hero guide.
