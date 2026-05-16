# LLM Reviewer Gate - external-research-costs-external-cross-check

## Overview

- State: `completed`
- Provider: `openai`
- Target: `research-costs.html`
- Request: `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-external-research-costs-external-cross-check-request.json`
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-external-research-costs-external-cross-check-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: review gate only; no final public page copy or patch specs were generated.

## Verdict

- Verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `proposal`
- Owner approval required: `true`

## Blocking Issues

- high: The brief confirms the topic duplicates an existing page intent and does not add a distinct player job. Required fix: Get owner confirmation that research-costs.html should remain an atlas router and that no separate page or broadened scope is needed.
- high: The external claim cannot be verified from the provided material alone. Required fix: Verify the branch coverage and cost-table claims against canonical site memory plus one additional reliable source or owner confirmation before any copy change.
- medium: The request is close to a cross-check maintenance pass but still risks blurring cluster roles if widened beyond the opening answer and route clarity. Required fix: Keep any future work narrowly scoped to first-screen clarity and verified link coverage only, with no new research guide behavior.

## Warnings

- No exact_replacements were provided, so there is no candidate replacement to approve or reject.
- Canonical claims must remain intact, especially field-research-follows-siege, research-atlas-role, and research-best-mainline.
- Do not treat the external reference as proof; it is only a discovery signal.
- Manual first-screen and internal-link review is required before any edit decision.

## Duplicate Intent Review

Duplicate intent is present. This page already serves as a research atlas and router, so the new request overlaps existing intent rather than introducing a new user job.

## Cluster Role Review

Cluster role is mostly safe if kept as an atlas-page. The brief should not expand into a general research guide or separate cost calculator.

## Canonical Claim Review

Protected claims are explicitly preserved and must not be contradicted. The requested direction appears compatible only if the mainline route wording stays stable.

## Template Safety Review

Template safety is acceptable at a planning level because no template change is requested. Any future edit must avoid changing the page archetype, navigation pattern, or schema family.

## Exact Replacement Review

No exact_replacements were provided. No literal candidate pairs to review.

## Owner Questions

- Do you want research-costs.html to stay strictly as a branch router and cross-check hub, or should any section become more explicit about coverage validation?
- Are the current downstream branch links the final verified set for the comparison grid?
- Should the recommended route wording remain locked to the current canonical order, even if future balance changes occur?

## Required Context Before Edit

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

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on research-costs.html`

## Next Step

Collect owner confirmation and verify the claims against canonical memory and a second reliable source, then return with a narrowly scoped proposal for first-screen clarity only if the page role remains unchanged.
