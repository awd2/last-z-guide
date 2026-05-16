# LLM Worker Chain - external-hq-and-progression-reference-cross-check

## Outcome

- State: `completed`
- Provider: `openai`
- Handoff source: `live_scout`
- Source decision: `None`
- Target: `hq.html`
- Page role: `cornerstone-guide`
- Review verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `proposal`
- Owner approval required: `true`
- Draft exact replacements: `0`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Stage Artifacts

- llm_scout: state `completed`, request `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`, result `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`, markdown `automation/reports/llm-auto-review-queue/llm-auto-review-scout.md`
- llm_editor: state `completed`, request `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-hq-and-progression-reference-cross-check-request.json`, result `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-hq-and-progression-reference-cross-check-result.json`, markdown `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-hq-and-progression-reference-cross-check.md`
- llm_reviewer: state `completed`, request `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-external-hq-and-progression-reference-cross-check-request.json`, result `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-external-hq-and-progression-reference-cross-check-result.json`, markdown `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-external-hq-and-progression-reference-cross-check.md`

## Editor Brief Summary

Keep hq.html as the cornerstone HQ guide, but tighten the opening to foreground the HQ and progression requirement cross-check job, then validate section order and internal routes without changing page role or template.

## First-Screen Plan

Preserve the answer-first opening and make sure the first screen immediately states the HQ planning recommendation, the HQ30 to HQ35 split, and the construction requirement cross-check angle. Keep the current page role and do not introduce a new intent or a different content type. The opening should stay concise, direct, and useful for players comparing requirements and progression timing.

## Draft Exact Replacements

Count: `0`

## Reviewer Blocking Issues

- high: The brief depends on external claim validation and owner confirmation before any content proposal can be shaped. Required fix: Cross-verify HQ requirement claims against canonical site memory and a second reliable source, then obtain owner confirmation for any claim changes.
- high: The topic overlaps existing HQ, progression, and base-building guidance and could blur cluster roles if scope is expanded. Required fix: Keep the scope limited to the current HQ cornerstone intent and do not convert it into a distinct reference-comparison article or new page intent.
- medium: No exact replacement candidates are provided, so there is no narrow, literal edit path to review for safe execution. Required fix: If later edits are proposed, provide only target-only exact_old/exact_new candidates with a clear no-template-change boundary.

## Reviewer Warnings

- High-risk cornerstone page: owner approval is required before any user-visible content change.
- Do not use analytics signals as proof that a rewrite is required.
- The opening should remain answer-first and preserve the existing page role.

## Owner Questions

- Do you want the first screen to explicitly name the HQ and progression requirement cross-check job, or keep it implicit within the existing answer-first lede?
- Should the cluster route block prioritize base-building support pages, or keep the current mix of progression-adjacent links?
- Are there any HQ requirement claims that must be locked to canonical memory before we touch section wording?

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on hq.html`
- `Cross-verify HQ requirement claims against canonical memory and a second reliable source`
- `Confirm the page still reads as a cornerstone guide and not a separate reference-comparison article`

## Next Step

Run canonical and second-source verification, then move to a proposal only if the scope stays within the existing HQ cornerstone guide.
