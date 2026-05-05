# LLM Reviewer Gate - research-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `research.html`
- Request: `automation/reports/llm-worker-chain-reviewer-research-gsc-opportunity-request.json`
- Result: `automation/reports/llm-worker-chain-reviewer-research-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: review gate only; no final public page copy or patch specs were generated.

## Verdict

- Verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `none`
- Owner approval required: `true`

## Blocking Issues

- high: High-risk cornerstone page opportunity cannot be advanced automatically without explicit owner review. Required fix: Obtain Research owner validation before any user-visible content change is planned or approved.
- high: The brief identifies overlap risk with progression and economy guidance, which could blur cluster role separation if scoped too broadly. Required fix: Confirm the update remains strictly within research-order intent and does not re-home adjacent intents from tech, field research, or cost pages.
- medium: Protected canonical claims must be verified against exact current wording before any edit planning proceeds. Required fix: Review canonical claim references for hero-training-cockpit-stop, peace-shield-value, research-atlas-role, and research-best-mainline in the source canon files.

## Warnings

- Analytics signals are suggestive but not proof of a rewrite need.
- The page should remain in-role as a cornerstone guide and not become a different page type.
- Template, navigation pattern, and schema family must remain unchanged.
- No public copy or patch details should be generated at this stage.

## Duplicate Intent Review

Low to medium duplication risk. The query intent is still appropriately served by research.html, but the brief could overlap with progression, economy, and defense-cost content if the scope widens beyond research-order guidance.

## Cluster Role Review

Pass conditionally. Research.html remains the correct cornerstone target for research-order intent, but the update must preserve clear separation from cost, tech, and progression-support pages.

## Canonical Claim Review

Conditional pass. The brief explicitly protects the required canonical claims and does not contradict them, but exact claim wording should be verified before any edit planning.

## Template Safety Review

Pass. The brief respects the existing template, navigation pattern, and schema family, and does not request a page type change.

## Owner Questions

- Does the current opening answer the research-priority question in the first screen quickly enough for searchers?
- Should the priority framing lean more toward general progression, defense timing, or T10 progression for the intended audience?
- Are there any current FAQ items that should be elevated into the opening or decision framework instead?
- Is any internal link emphasis missing for the current cluster route block?
- Do any protected claims need exact wording verification before a content update is planned?

## Required Context Before Edit

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

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on research.html`

## Next Step

Request Research owner review to confirm scope, then prepare a narrowly scoped update plan only if the opening can be improved without changing page role or protected claims.
