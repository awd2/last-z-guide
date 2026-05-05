# LLM Editor Brief - research-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `research.html`
- Request: `automation/reports/llm-worker-chain-editor-research-gsc-opportunity-request.json`
- Result: `automation/reports/llm-worker-chain-editor-research-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Brief Summary

Refine the existing cornerstone research guide so the opening immediately answers research-order intent, while keeping the page in-role and preserving protected canonical claims. Emphasize a clear priority framework, then support it with a concise route through key nodes and related cluster pages.

## First-Screen Plan

Keep the answer-first structure, but tighten the opening so it explicitly resolves the priority question in plain terms. The first screen should identify the recommended early research sequence, note the practical reason for that sequence, and point to the key decision split between general progression, Peace Shield timing, and the T10 path. Avoid expanding into deep explanations before the user gets the actionable answer. Do not change the page into a different cluster role or dilute the canonical mainline framing.

## Section Plan

- Quick Answer: Strengthen the opening response to directly satisfy research-priority intent with a clearer one-paragraph answer and a compact order summary. Reason: This is the highest-impact area for query match and snippet usefulness.
- Best overall recommendation: Add or refine a concise recommendation block that explains when the default order applies and when a player might deviate. Reason: Helps users decide whether to follow the mainline path or branch by progression stage.
- Decision framework: Structure the rationale around player stage, troop goals, defense needs, and whether to push toward T10 now or later. Reason: Supports intent without overloading the first screen.
- Cluster route block: Keep a visible route to adjacent research and progression pages, especially economy, tech, and cost-related references. Reason: Preserves cluster navigation and clarifies next-click paths.
- Related guides / FAQ: Trim or reorder FAQ entries so they resolve the most common research-order and Peace Shield timing questions sooner. Reason: Improves scanability and aligns supporting content with search intent.

## Internal Link Plan

- upstream `research-costs.html`: Supports users who need cost context after choosing a research order.
- upstream `index.html`: Maintains canonical hub access and cluster entry context.
- downstream `hero-training-cost.html`: Matches the early-game research priority path and reinforces the cockpit stop claim without expanding scope.
- downstream `military-strategies-cost.html`: Supports the recommended stat-focused branch in the mainline order.
- downstream `peace-shield-cost.html`: Directly relevant to the timing decision around protection and Urgent Rescue.
- downstream `hq.html`: Helps tie research progression to account progression milestones.
- downstream `lucky-discounter.html`: Useful for cost-efficient progression decisions without changing page role.
- lateral `alliance-duel.html`: Provides adjacent strategic context for players balancing research with broader competition.

## Protected Claims

- `hero-training-cockpit-stop`
- `peace-shield-value`
- `research-atlas-role`
- `research-best-mainline`

## Do Not Change

- Do not change the existing page template, navigation pattern, or schema family.
- Do not create a new page or re-home the intent to a different canonical target.
- Do not contradict canonical claim hero-training-cockpit-stop.
- Do not contradict canonical claim peace-shield-value.
- Do not contradict canonical claim research-atlas-role.
- Do not contradict canonical claim research-best-mainline.
- Do not use analytics signals as proof that a rewrite is required.
- Do not blur cluster role separation between research, cost, and progression pages.
- Do not publish or apply content changes from this brief automatically.

## Owner Questions

- Does the current opening answer the research-priority question in the first screen quickly enough for searchers?
- Should the priority framing lean more toward general progression, defense timing, or T10 progression for the intended audience?
- Are there any current FAQ items that should be elevated into the opening or decision framework instead?
- Is any internal link emphasis missing for the current cluster route block?
- Do any protected claims need exact wording verification before a content update is planned?

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

## Next Step

Ask the Research owner to validate whether the opening section already satisfies research-order intent well enough; if not, prepare a scoped update plan that preserves the current cornerstone role and protected claims.
