# LLM Reviewer Gate - external-hq-and-progression-reference-cross-check

## Overview

- State: `completed`
- Provider: `openai`
- Target: `hq.html`
- Request: `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-external-hq-and-progression-reference-cross-check-request.json`
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-external-hq-and-progression-reference-cross-check-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: review gate only; no final public page copy or patch specs were generated.

## Verdict

- Verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `proposal`
- Owner approval required: `true`

## Blocking Issues

- high: The brief depends on external claim validation and owner confirmation before any content proposal can be shaped. Required fix: Cross-verify HQ requirement claims against canonical site memory and a second reliable source, then obtain owner confirmation for any claim changes.
- high: The topic overlaps existing HQ, progression, and base-building guidance and could blur cluster roles if scope is expanded. Required fix: Keep the scope limited to the current HQ cornerstone intent and do not convert it into a distinct reference-comparison article or new page intent.
- medium: No exact replacement candidates are provided, so there is no narrow, literal edit path to review for safe execution. Required fix: If later edits are proposed, provide only target-only exact_old/exact_new candidates with a clear no-template-change boundary.

## Warnings

- High-risk cornerstone page: owner approval is required before any user-visible content change.
- Do not use analytics signals as proof that a rewrite is required.
- The opening should remain answer-first and preserve the existing page role.

## Duplicate Intent Review

The page appears to duplicate existing HQ and progression intent rather than introduce a distinct player job. This supports update_existing only if scope stays tightly constrained.

## Cluster Role Review

Cluster role is acceptable as a Progression cornerstone guide, but the brief warns against blurring into a general reference-comparison article. Supporting routes should stay aligned to HQ, progression, and base-building.

## Canonical Claim Review

Canonical claims about HQ requirements, dependencies, steel timing, and progression thresholds must remain locked to site memory and owner-confirmed references. External source validation is required before any claim-level proposal.

## Template Safety Review

Template safety is acceptable only if the page template, navigation pattern, and schema family remain unchanged. No template changes are approved in this brief.

## Exact Replacement Review

No exact_replacements were provided. That is safe for review, but it also means there is no candidate-level edit to approve or validate for apply_preview.

## Owner Questions

- Do you want the first screen to explicitly name the HQ and progression requirement cross-check job, or keep it implicit within the existing answer-first lede?
- Should the cluster route block prioritize base-building support pages, or keep the current mix of progression-adjacent links?
- Are there any HQ requirement claims that must be locked to canonical memory before we touch section wording?

## Required Context Before Edit

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `hq.html`
- `index.html`
- `start.html`
- `early-game-optimization.html`
- `base-building-order.html`

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on hq.html`
- `Cross-verify HQ requirement claims against canonical memory and a second reliable source`
- `Confirm the page still reads as a cornerstone guide and not a separate reference-comparison article`

## Next Step

Run canonical and second-source verification, then move to a proposal only if the scope stays within the existing HQ cornerstone guide.
