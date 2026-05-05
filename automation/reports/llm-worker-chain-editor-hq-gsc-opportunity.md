# LLM Editor Brief - hq-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `hq.html`
- Request: `automation/reports/llm-worker-chain-editor-hq-gsc-opportunity-request.json`
- Result: `automation/reports/llm-worker-chain-editor-hq-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Brief Summary

Keep hq.html as the cornerstone progression guide, but tighten the opening to answer the HQ upgrade query immediately, then structure the page around fast-path leveling, required-building decisions, and the HQ30→35 steel phase without shifting cluster role.

## First-Screen Plan

Preserve answer-first layout. The first screen should immediately confirm the page solves HQ upgrade requirements and fast-path strategy, then signal the split between early rush progression and the heavier HQ31–35 steel phase. Keep the existing template and avoid introducing a different content mission or persona. The opening should help users decide whether to rush, what to upgrade now, and when the guide changes after HQ30.

## Section Plan

- Quick Answer: Keep it as the immediate answer block and make sure it names the best overall HQ path, the required-building rule, and the HQ30/35 split. Reason: This is the highest-intent section and should resolve the query before users scroll.
- Best overall recommendation: Frame the recommended route as a practical default for most players, with clear conditions for when to deviate. Reason: Searchers need a concise decision, not just raw requirements.
- Decision framework: Organize the choice points by early-game speed, required upgrade dependencies, and whether the player is pre- or post-HQ30. Reason: The query implies planning tradeoffs, so this section should reduce ambiguity.
- Cluster route block: Keep the internal route block and ensure it points to adjacent progression topics instead of replacing the page’s role. Reason: Supports navigation while protecting cluster separation.
- Related guides / FAQ: Use this area to connect HQ strategy with adjacent progression questions and common follow-ups. Reason: Improves satisfaction and internal pathing without overexpanding the cornerstone guide.

## Internal Link Plan

- upstream `index.html`: Entry point for broader site navigation and progression discovery.
- upstream `start.html`: Matches the upstream route and supports users who are still orienting early progression choices.
- lateral `early-game-optimization.html`: Adjacent planning topic for players deciding how aggressively to progress before HQ milestones.
- lateral `base-building-order.html`: Useful companion for upgrade sequencing and building priority decisions.
- lateral `shooter-stages.html`: Related progression-adjacent content that can answer broader early-game route questions.
- downstream `alliance-duel.html`: Specific tactical follow-up that benefits players after understanding HQ progression timing.
- downstream `arena.html`: Downstream optimization topic for players who have moved beyond core HQ planning.
- downstream `emergency-hospital-cost.html`: Supporting guide for a concrete building-cost or upgrade concern likely encountered during HQ planning.

## Protected Claims

- None

## Do Not Change

- Do not alter the page into a start-page replacement or broader onboarding guide.
- Do not change the existing page template, navigation pattern, or schema family.
- Do not remove the cornerstone-guide role or blur the Progression cluster boundary.
- Do not create a new page or split the topic into multiple pages.
- Do not introduce unverifiable claims about HQ requirements, costs, or timings without canonical source confirmation.
- Do not use analytics metrics as proof that a rewrite is required.

## Owner Questions

- Should the opening answer explicitly mention HQ30 as the main breakpoint, or keep that detail deeper in the page?
- Do you want the decision framework to lean more toward speed-rush guidance or resource-efficiency guidance?
- Are there any canonical HQ requirement details that must remain verbatim in the requirements section?

## Required Context Before Patch

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `hq.html`
- `start.html`
- `index.html`
- `early-game-optimization.html`
- `base-building-order.html`
- `shooter-stages.html`

## Acceptance Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on hq.html`

## Next Step

Run the no-write Editor and Reviewer stages against hq.html, verifying that the first screen answers the query immediately and that internal links preserve the Progression cluster routing.
