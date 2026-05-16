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
- Approved next stage: `none`
- Owner approval required: `true`

## Blocking Issues

- high: High-risk cornerstone page with an external claim that is explicitly not verified beyond the provided source. Required fix: Obtain owner confirmation or a second reliable reference before any user-visible wording is approved.
- high: The brief indicates the topic duplicates an existing page intent and may blur cluster roles. Required fix: Confirm that hq.html has a distinct planning job and that no separate page or broader reference-dump scope is being introduced.
- high: Exact replacement candidate is proposal-only and cannot be approved from this review. Required fix: Keep the replacement as a candidate only and route it through owner review before any apply step.

## Warnings

- The current page already appears to have an answer-first structure, so changes should remain narrow and scope-safe.
- Internal link changes should preserve the existing progression cluster route and avoid role drift.
- Analytics should not be used as evidence that copy changes are required.

## Duplicate Intent Review

Medium to high duplication risk. The page intent appears to overlap with existing HQ and progression planning coverage, so the update must stay as a narrow clarification rather than a new intent.

## Cluster Role Review

The page fits the Progression cluster as a cornerstone guide, but it must not expand into a generic reference hub or competitor-style dump.

## Canonical Claim Review

The external HQ requirement and dependency claims are unverified beyond the supplied source. Canonical protection requires owner confirmation or another reliable source before approval.

## Template Safety Review

Template and schema changes are not requested. Keeping the existing page template, navigation pattern, and schema family is safe, but must be enforced.

## Exact Replacement Review

One exact replacement candidate is present. It is narrow and target-only in form, but it remains proposal-only and owner approval is required. Do not approve apply_preview from this review.

## Owner Questions

- Can the external HQ and progression reference be confirmed against canonical site memory or another owner-approved source?
- Should the first-screen answer explicitly name HQ30 and HQ31-35, or should the current phrasing be kept and only the supporting sentence clarified?
- Do you want to keep the cluster route block unchanged structurally and only tighten the wording?

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

## Next Step

Request owner verification of the external claim and scope confirmation, then return for a narrow approval review before any apply step.
