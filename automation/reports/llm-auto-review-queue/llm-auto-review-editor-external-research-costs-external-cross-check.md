# LLM Editor Brief - external-research-costs-external-cross-check

## Overview

- State: `completed`
- Provider: `openai`
- Target: `research-costs.html`
- Request: `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-research-costs-external-cross-check-request.json`
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-research-costs-external-cross-check-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Brief Summary

Keep research-costs.html as an atlas page and improve only the first-screen answer and route clarity so it better supports branch coverage cross-checking. Maintain the existing Research cluster role, canonical claims, and downstream branch links; do not widen scope into a new page type.

## First-Screen Plan

Preserve the answer-first structure. Make the opening paragraph or quick answer clearly state that this page is a branch router and cross-check hub, then point users to the exact branch cost pages for node-by-node totals. Keep the main route guidance intact and do not add new claims that would change the page role. The first screen should immediately answer what the page is for, how to use it, and which route is the default for most players.

## Section Plan

- Quick Answer: Keep the answer-first intro, but tighten it so the page purpose, route order, and cross-check function are obvious immediately. Reason: The opening must satisfy the cross-check intent without changing the atlas role.
- Cluster overview: Ensure the overview frames the page as a Research cluster router, not a standalone cost calculator. Reason: This protects the existing page archetype and avoids scope creep.
- Comparison grid or card list: Retain the branch comparison layout and confirm it covers the major branches with stable naming. Reason: This is the core utility for spotting missing branches and drift.
- Recommended route: Keep the current mainline order and reinforce that the route is the default planning path for most players. Reason: Must not contradict the canonical mainline claims.
- Exact page links: Keep downstream links to the exact branch pages and add no new branch destinations unless verified later. Reason: Users need the direct handoff from atlas to detailed cost pages.

## Internal Link Plan

- upstream `index.html`: Home entry point for the Research cluster and the natural upstream route.
- lateral `research.html`: Cluster hub that supports navigation and contextual understanding.
- lateral `tech.html`: Related navigation page in the same research and progression area.
- lateral `field-research.html`: Relevant adjacent branch page and a key part of the current route.
- downstream `hero-training-cost.html`: Exact branch cost page for the first step in the recommended route.
- downstream `military-strategies-cost.html`: Exact branch cost page for the next major route step.
- downstream `peace-shield-cost.html`: Important branch page in the main route sequence.
- downstream `siege-to-seize-cost.html`: Route branch page that must remain visible in the mainline chain.

## Protected Claims

- `field-research-follows-siege`
- `research-atlas-role`
- `research-best-mainline`

## Do Not Change

- Do not change the existing page template, navigation pattern, or schema family without separate approval.
- Do not create a new page when the Scout proposal recommends updating an existing page.
- Do not contradict canonical claim field-research-follows-siege.
- Do not contradict canonical claim research-atlas-role.
- Do not contradict canonical claim research-best-mainline.
- Do not broaden the page into a new player job or a general research guide.
- Do not rely on analytics as proof that a rewrite is needed.

## Owner Questions

- Should the first-screen wording emphasize cross-checking branch coverage more explicitly, or keep it subtle and utility-focused?
- Are there any additional verified branch links that should appear in the comparison grid, or should the current branch set remain unchanged?
- Is the current recommended route still the preferred canonical order for the atlas intro, or should any wording be softened to match future balance changes?

## Required Context Before Patch

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `research-costs.html`
- `index.html`
- `research.html`
- `tech.html`
- `field-research.html`

## Acceptance Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on research-costs.html`

## Draft Exact Replacements

Proposal-only candidates. They do not approve copy, create Patch Specs, edit files, or bypass owner review.

- None

## Next Step

Verify the current page content against canonical memory and the secondary source, then decide whether only the opening answer needs a narrow wording update or whether the branch grid also needs a verified maintenance pass.
