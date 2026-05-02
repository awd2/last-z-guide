# Content Consistency Audit

Generated: 2026-05-02

This is a no-write review artifact for public user-facing content. It focuses on avoiding misleading guidance and cross-page contradictions before the LLM worker provider is added.

## Scope

- Public HTML reviewed: 62 pages
- Noindex/archive HTML excluded from user-facing audit: `news-preview.html`
- Main consistency areas checked:
  - Season naming and Desert/Winter ambiguity
  - Gift Center redemption flow
  - Research priority path and badge spending
  - Alliance Recognition event economy vs combat research
  - Formation and PvP claims
  - Shield/diamond economy guidance
  - Archived Reddit/news experiment visibility

## Fixes Applied

- `research.html`
  - clarified the main route as Hero Training to Cockpit, Military Strategies, Peace Shield, then the shortest practical path toward UST and T10
  - replaced `Special Unit Training` with `Unit Special Training`
  - changed UST cost shorthand to the exact 1,488,100 badge total
  - kept an explicit warning not to rush UST before efficient mid-game value branches
- `power-guide.html`
  - replaced absolute `Alliance Recognition FIRST` guidance with balanced core-combat plus Alliance Recognition checkpoint guidance
- `formation-power.html`
  - owner review restored the stronger raw-power and Alliance Recognition badge-sustainability wording for this page
- `formations.html`
  - kept the structured-data softening from absolute "best formation" to a strong default on many Blood Rose-heavy servers
  - clarified that an underbuilt new-season hero should not break a working synergy core by itself
- `pvp.html`
  - removed outdated `S3 > S2 > S1` priority wording and aligned with current newer-season hero guidance
- `alliance-duel.html`
  - reframed Alliance Recognition as early event-economy value, not a universal first badge rule
- `tips.html`
  - owner review restored the stronger Alliance Recognition-first quick-tip wording
- `tech.html`
  - owner review restored the original Alliance Recognition-first section heading

## Current Result

- No active public page now matches the audited high-risk contradiction patterns for:
  - unqualified `Season 2 = Desert`
  - redeeming codes inside the game as the actual flow
  - UST/Special Unit Training as an early or first research path
  - diamond shields being preferred over Alliance Shop shields
  - Reddit/news digest exposure
- Owner-approved stronger wording remains on selected Alliance Recognition and raw formation power pages where it reflects the intended page stance.

## Follow-Up Recommendation

Convert these audit patterns into a deterministic `content_consistency` check before allowing future LLM worker edits to advance to approval. The check should warn on risky wording and allow explicit safe contexts such as historical season clarification or FAQ questions that immediately answer with the canonical flow.
