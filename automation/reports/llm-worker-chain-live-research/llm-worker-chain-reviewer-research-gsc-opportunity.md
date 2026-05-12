# LLM Reviewer Gate - research-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `research.html`
- Request: `automation/reports/llm-worker-chain-live-research/llm-worker-chain-reviewer-research-gsc-opportunity-request.json`
- Result: `automation/reports/llm-worker-chain-live-research/llm-worker-chain-reviewer-research-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: review gate only; no final public page copy or patch specs were generated.

## Verdict

- Verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `brief`
- Owner approval required: `true`

## Blocking Issues

- high: The page is a cornerstone guide and the request touches first-screen positioning for a protected query family. That raises cluster-role and canonical-claim risk even without copy changes. Required fix: Require human owner review before any drafting or content adjustment. Confirm the opening can be tightened without changing page role or contradicting protected claims.
- high: Duplicate intent risk remains medium because the opportunity must stay distinct from costs, hero training, Peace Shield, and other adjacent research pages. Required fix: Verify the page can satisfy last z research priority intent while preserving separation from research-costs.html, hero-training-cost pages, and peace-shield guidance.
- medium: No exact replacements are provided, so there is no narrow literal candidate set to review for safe replacement behavior. Required fix: If an Editor follow-up introduces exact replacements, require literal exact_old/exact_new scope, target-only edits, and owner approval before any apply_preview path.

## Warnings

- Analytics signals support the opportunity, but they do not prove a rewrite is required.
- The brief asks for stronger first-screen intent match, which may affect cornerstone framing if handled too aggressively.
- The required checks include manual first-screen and internal-link review, so readiness depends on human validation after any drafting.

## Duplicate Intent Review

Medium duplicate-intent risk. The target page is already the canonical research overview, but the requested improvement could overlap with costs, progression, and specialist subguides if not tightly scoped.

## Cluster Role Review

Pass on current scope only if the page remains the Research cluster cornerstone. The brief correctly says not to create a new page and not to blur cluster separation, but this still needs owner confirmation because the opening answer is being reoriented toward query intent.

## Canonical Claim Review

Protected claims are explicitly listed and must not be contradicted. Current brief is compatible in principle, but the first-screen emphasis on priority and T10/UST should be checked against research-best-mainline, hero-training-cockpit-stop, peace-shield-value, and research-atlas-role before drafting.

## Template Safety Review

Template safety is acceptable at the planning level because the brief preserves the existing template, navigation pattern, and schema family. No template change is approved.

## Exact Replacement Review

No exact replacements were provided. No candidate replacements to review. If later supplied, they must remain narrow, literal, and target-only, and they still cannot bypass owner approval or advance directly to apply_preview.

## Owner Questions

- Should the opening line explicitly mention last z research priority, or should the intent stay implied through the existing quick-answer structure?
- Do you want the related-links block to foreground progression pages or keep the current mixed Research cluster balance?
- Is there any approved wording boundary for emphasizing T10 and Urgent Rescue in the first screen?

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

Route to human owner review. If approved, proceed with a brief-level planning pass only, then validate against the required checks before any edit draft is prepared.
