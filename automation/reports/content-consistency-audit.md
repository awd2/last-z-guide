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
  - aligned the main research route with the canonical path: Hero Training, Military Strategies, Peace Shield, Siege to Seize, then Field Research before late Unit Special Training planning
  - removed outdated `Special Unit Training` naming and over-strong UST-first guidance
  - removed unsupported dollar-cost framing
- `power-guide.html`
  - replaced absolute `Alliance Recognition FIRST` guidance with balanced core-combat plus Alliance Recognition checkpoint guidance
- `formation-power.html`
  - clarified raw formation power vs real PvP counter value
  - softened Alliance Recognition language so it does not override core combat research needs
- `formations.html`
  - replaced absolute formation claims with server-meta-aware wording
  - clarified that an underbuilt new-season hero should not break a working synergy core by itself
- `pvp.html`
  - removed outdated `S3 > S2 > S1` priority wording and aligned with current newer-season hero guidance
- `alliance-duel.html`
  - reframed Alliance Recognition as early event-economy value, not a universal first badge rule
- `tips.html`
  - removed absolute `before any badge research` advice
- `tech.html`
  - changed the Alliance Recognition section heading to avoid a false absolute-first signal

## Current Result

- No active public page now matches the audited high-risk contradiction patterns for:
  - unqualified `Season 2 = Desert`
  - redeeming codes inside the game as the actual flow
  - UST/Special Unit Training as an early or first research path
  - absolute Alliance Recognition-first badge advice
  - single absolute best formation claims
  - diamond shields being preferred over Alliance Shop shields
  - Reddit/news digest exposure

## Follow-Up Recommendation

Convert these audit patterns into a deterministic `content_consistency` check before allowing future LLM worker edits to advance to approval. The check should warn on risky wording and allow explicit safe contexts such as historical season clarification or FAQ questions that immediately answer with the canonical flow.
