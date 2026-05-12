# LLM Worker Chain - index-gsc-opportunity

## Outcome

- State: `completed`
- Provider: `openai`
- Handoff source: `live_scout`
- Source decision: `None`
- Target: `index.html`
- Page role: `home-hub`
- Review verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `brief`
- Owner approval required: `true`
- Draft exact replacements: `0`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Stage Artifacts

- llm_scout: state `completed`, request `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`, result `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`, markdown `automation/reports/llm-auto-review-queue/llm-auto-review-scout.md`
- llm_editor: state `completed`, request `automation/reports/llm-auto-review-queue/llm-auto-review-editor-index-gsc-opportunity-request.json`, result `automation/reports/llm-auto-review-queue/llm-auto-review-editor-index-gsc-opportunity-result.json`, markdown `automation/reports/llm-auto-review-queue/llm-auto-review-editor-index-gsc-opportunity.md`
- llm_reviewer: state `completed`, request `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-index-gsc-opportunity-request.json`, result `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-index-gsc-opportunity-result.json`, markdown `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-index-gsc-opportunity.md`

## Editor Brief Summary

Refine the home hub so the first screen answers the rising research-guide intent immediately, then routes users into the correct cluster page or related guide without changing the site structure or home-hub role.

## First-Screen Plan

Keep the hero and template intact, but make the opening more answer-first: state the immediate user action for research-guide seekers, then point them to the best next destination within the existing hub structure. The first screen should clarify that the homepage is a routing page, not a deep research article, and should surface the most relevant nearby guide path without adding cluster-specific depth.

## Draft Exact Replacements

Count: `0`

## Reviewer Blocking Issues

- high: The target is a cornerstone home hub page with high risk. The brief suggests a limited update, but the change could still affect cluster role boundaries and first-screen routing behavior. Required fix: Obtain explicit owner review confirming that only narrow routing and emphasis changes are allowed, and that home-hub scope will not expand into research-guide depth.
- high: Duplicate intent is plausible with field-research.html and adjacent progression guides. The homepage is not clearly the best canonical answer for the research-guide query if the user wants deep research guidance. Required fix: Verify that the home page should remain the canonical entry point for this query family and confirm the exact first-click destination for research-intent visitors.
- high: The brief includes no exact_replacements, but the suggested first-screen change still needs human approval because it may alter visible homepage copy and above-the-fold routing. Required fix: Have the owner approve the proposed direction before any user-visible homepage copy is drafted or applied.

## Reviewer Warnings

- GSC impressions and CTR are only signals, not proof that a rewrite is required.
- The brief is directionally safe but still high risk because it touches a home-hub page.
- The reviewer should confirm that template, navigation pattern, and schema family remain unchanged.
- Manual QA is required for first-screen answer quality and internal links on index.html.

## Owner Questions

- Should the homepage explicitly mention research routing, or should it remain broader to preserve the home-hub role?
- Which downstream guide should be the primary first click for research-intent visitors: field-research.html or another canonical page?
- Is it acceptable to reorder featured cards, or should only copy and emphasis change within the existing layout?
- Are there any approved trust or freshness cues that can be reused on the home page?

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on index.html`

## Next Step

Request human review to confirm whether a limited homepage update can improve research routing without weakening the home-hub role. If approved, proceed only to a narrow brief or patch plan, not to apply_preview.
