# LLM Editor Brief - research-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `research.html`
- Request: `automation/reports/llm-worker-chain-live-research/llm-worker-chain-editor-research-gsc-opportunity-request.json`
- Result: `automation/reports/llm-worker-chain-live-research/llm-worker-chain-editor-research-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Brief Summary

Tighten the existing research.html opening so it answers research priority intent faster, while keeping the page a cornerstone research guide and preserving protected claims plus cluster separation.

## First-Screen Plan

Keep the answer-first structure, but make the opening explicitly orient around best research order and progression. The first screen should state the practical sequence, the main decision criteria, and the reason the page exists without drifting into a costs-only, hero-only, or Peace Shield-only angle. Preserve the current canonical claims and ensure the opening remains consistent with the existing mainline guidance.

## Section Plan

- Quick Answer: Tighten the answer so it directly satisfies last z research priority intent and names the practical order at a high level. Reason: This is the highest-value fix for query match and CTR without changing the page role.
- Best overall recommendation: Make the main recommendation more explicit about the overall path and decision logic. Reason: Helps users understand what to do first and keeps the cornerstone framing intact.
- Decision framework: Emphasize the criteria for choosing what to research next, including progression and unlock considerations. Reason: Supports users who need a reasoned path rather than a flat list.
- Cluster route block: Confirm the route from research overview into related research subpages without overpromoting any single downstream topic. Reason: Preserves cluster structure and helps avoid duplication with adjacent canonical pages.
- Related guides / FAQ: Keep supporting links focused on adjacent research questions and common follow-ups. Reason: Maintains internal routing and helps searchers continue from the overview page.

## Internal Link Plan

- upstream `index.html`: Main hub route into the Research cluster.
- upstream `research-costs.html`: Cost context supports the research overview without replacing it.
- downstream `hero-training-cost.html`: Related progression topic that can support the recommended early path.
- downstream `military-strategies-cost.html`: Useful follow-on for players comparing early research priorities.
- downstream `hq.html`: Progression context tied to research gating and planning.
- downstream `lucky-discounter.html`: Adjacent optimization topic that can help with progression decisions.
- downstream `alliance-duel.html`: Relevant game mode context for research prioritization.
- lateral `tech.html`: Adjacent systems page that should remain distinct from the main research guide.

## Protected Claims

- `hero-training-cockpit-stop`
- `peace-shield-value`
- `research-atlas-role`
- `research-best-mainline`

## Do Not Change

- Do not change the existing page template, navigation pattern, or schema family without separate approval.
- Do not create a new page when the Scout proposal recommends updating an existing page.
- Do not contradict canonical claim hero-training-cockpit-stop.
- Do not contradict canonical claim peace-shield-value.
- Do not contradict canonical claim research-atlas-role.
- Do not contradict canonical claim research-best-mainline.
- Do not blur the Research cluster boundary with costs-only or single-topic subguides.
- Do not treat analytics as proof of a rewrite requirement.

## Owner Questions

- Should the opening line explicitly mention last z research priority, or should that phrase stay implied through the existing quick-answer structure?
- Do you want the related-links block to foreground progression pages or keep the current mixed Research cluster balance?
- Is there any approved wording boundary for emphasizing T10 and Urgent Rescue in the first screen?

## Required Context Before Patch

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `research.html`
- `index.html`
- `research-costs.html`
- `tech.html`
- `field-research.html`
- `alliance-recognition-cost.html`

## Acceptance Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on research.html`

## Draft Exact Replacements

Proposal-only candidates. They do not approve copy, create Patch Specs, edit files, or bypass owner review.

- None

## Next Step

Send to human owner review for approval of first-screen emphasis and link emphasis before any content change is prepared.
