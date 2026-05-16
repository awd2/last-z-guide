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
- Approved next stage: `none`
- Owner approval required: `true`
- Draft exact replacements: `1`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Stage Artifacts

- llm_scout: state `completed`, request `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`, result `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`, markdown `automation/reports/llm-auto-review-queue/llm-auto-review-scout.md`
- llm_editor: state `completed`, request `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-hq-and-progression-reference-cross-check-request.json`, result `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-hq-and-progression-reference-cross-check-result.json`, markdown `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-hq-and-progression-reference-cross-check.md`
- llm_reviewer: state `completed`, request `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-external-hq-and-progression-reference-cross-check-request.json`, result `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-external-hq-and-progression-reference-cross-check-result.json`, markdown `automation/reports/llm-auto-review-queue/llm-auto-review-reviewer-external-hq-and-progression-reference-cross-check.md`

## Editor Brief Summary

Keep hq.html as a cornerstone progression guide, but tighten the first-screen answer so it explicitly cross-checks HQ requirements and dependency planning without changing page role or cluster fit.

## First-Screen Plan

Preserve the answer-first structure. Keep the opening focused on the best HQ path for most players, but make the first visible answer clearly state the requirement cross-check angle: early rush, required-buildings-only upgrades, HQ30 target, then a separate HQ31-35 steel phase. Avoid adding a new intent or expanding into a different guide type. Keep the short supporting line immediately after the answer so users can confirm this is a planning guide, not a full route map.

## Draft Exact Replacements

Count: `1`

## Reviewer Blocking Issues

- high: High-risk cornerstone page with an external claim that is explicitly not verified beyond the provided source. Required fix: Obtain owner confirmation or a second reliable reference before any user-visible wording is approved.
- high: The brief indicates the topic duplicates an existing page intent and may blur cluster roles. Required fix: Confirm that hq.html has a distinct planning job and that no separate page or broader reference-dump scope is being introduced.
- high: Exact replacement candidate is proposal-only and cannot be approved from this review. Required fix: Keep the replacement as a candidate only and route it through owner review before any apply step.

## Reviewer Warnings

- The current page already appears to have an answer-first structure, so changes should remain narrow and scope-safe.
- Internal link changes should preserve the existing progression cluster route and avoid role drift.
- Analytics should not be used as evidence that copy changes are required.

## Owner Questions

- Can the external HQ and progression reference be confirmed against canonical site memory or another owner-approved source?
- Should the first-screen answer explicitly name HQ30 and HQ31-35, or should the current phrasing be kept and only the supporting sentence clarified?
- Do you want to keep the cluster route block unchanged structurally and only tighten the wording?

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on hq.html`

## Next Step

Request owner verification of the external claim and scope confirmation, then return for a narrow approval review before any apply step.
