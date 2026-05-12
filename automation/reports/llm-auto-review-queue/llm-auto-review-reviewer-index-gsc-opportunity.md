# LLM Reviewer Gate - index-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `index.html`
- Request: `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-index-gsc-opportunity-request.json`
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-index-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: review gate only; no final public page copy or patch specs were generated.

## Verdict

- Verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `brief`
- Owner approval required: `true`

## Blocking Issues

- high: The target is a cornerstone home hub page with high risk. The brief suggests a limited update, but the change could still affect cluster role boundaries and first-screen routing behavior. Required fix: Obtain explicit owner review confirming that only narrow routing and emphasis changes are allowed, and that home-hub scope will not expand into research-guide depth.
- high: Duplicate intent is plausible with field-research.html and adjacent progression guides. The homepage is not clearly the best canonical answer for the research-guide query if the user wants deep research guidance. Required fix: Verify that the home page should remain the canonical entry point for this query family and confirm the exact first-click destination for research-intent visitors.
- high: The brief includes no exact_replacements, but the suggested first-screen change still needs human approval because it may alter visible homepage copy and above-the-fold routing. Required fix: Have the owner approve the proposed direction before any user-visible homepage copy is drafted or applied.

## Warnings

- GSC impressions and CTR are only signals, not proof that a rewrite is required.
- The brief is directionally safe but still high risk because it touches a home-hub page.
- The reviewer should confirm that template, navigation pattern, and schema family remain unchanged.
- Manual QA is required for first-screen answer quality and internal links on index.html.

## Duplicate Intent Review

Moderate risk. The query family 'last z research guide' may be better served by a dedicated research page such as field-research.html, while the homepage should stay a routing hub.

## Cluster Role Review

Acceptable only if the page remains a hub. The homepage should route users to cluster pages, not absorb research-guide content or blur hub versus guide roles.

## Canonical Claim Review

Safe for now. No protected claims are listed, but any new freshness, trust, or performance wording must avoid unsupported claims.

## Template Safety Review

Safe if the existing template and navigation pattern are preserved exactly. No schema or layout changes should be attempted in this brief.

## Exact Replacement Review

No exact_replacements were provided. There are no candidate literal swaps to review, so no exact-replacement approval path is applicable.

## Owner Questions

- Should the homepage explicitly mention research routing, or should it remain broader to preserve the home-hub role?
- Which downstream guide should be the primary first click for research-intent visitors: field-research.html or another canonical page?
- Is it acceptable to reorder featured cards, or should only copy and emphasis change within the existing layout?
- Are there any approved trust or freshness cues that can be reused on the home page?

## Required Context Before Edit

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `index.html`

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on index.html`

## Next Step

Request human review to confirm whether a limited homepage update can improve research routing without weakening the home-hub role. If approved, proceed only to a narrow brief or patch plan, not to apply_preview.
