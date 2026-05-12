# LLM Worker Chain - research-gsc-opportunity

## Outcome

- State: `completed`
- Provider: `openai`
- Handoff source: `topic_decision`
- Source decision: `automation/reports/llm-candidate-refresh-live/llm-topic-decision-research-gsc-opportunity.json`
- Target: `research.html`
- Page role: `cornerstone-guide`
- Review verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `brief`
- Owner approval required: `true`
- Draft exact replacements: `0`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Stage Artifacts

- llm_scout: state `completed`, request `automation/reports/llm-worker-chain-live-research/llm-worker-chain-scout-request.json`, result `automation/reports/llm-worker-chain-live-research/llm-worker-chain-scout-result.json`, markdown `automation/reports/llm-worker-chain-live-research/llm-worker-chain-scout.md`
- llm_editor: state `completed`, request `automation/reports/llm-worker-chain-live-research/llm-worker-chain-editor-research-gsc-opportunity-request.json`, result `automation/reports/llm-worker-chain-live-research/llm-worker-chain-editor-research-gsc-opportunity-result.json`, markdown `automation/reports/llm-worker-chain-live-research/llm-worker-chain-editor-research-gsc-opportunity.md`
- llm_reviewer: state `completed`, request `automation/reports/llm-worker-chain-live-research/llm-worker-chain-reviewer-research-gsc-opportunity-request.json`, result `automation/reports/llm-worker-chain-live-research/llm-worker-chain-reviewer-research-gsc-opportunity-result.json`, markdown `automation/reports/llm-worker-chain-live-research/llm-worker-chain-reviewer-research-gsc-opportunity.md`

## Editor Brief Summary

Tighten the existing research.html opening so it answers research priority intent faster, while keeping the page a cornerstone research guide and preserving protected claims plus cluster separation.

## First-Screen Plan

Keep the answer-first structure, but make the opening explicitly orient around best research order and progression. The first screen should state the practical sequence, the main decision criteria, and the reason the page exists without drifting into a costs-only, hero-only, or Peace Shield-only angle. Preserve the current canonical claims and ensure the opening remains consistent with the existing mainline guidance.

## Draft Exact Replacements

Count: `0`

## Reviewer Blocking Issues

- high: The page is a cornerstone guide and the request touches first-screen positioning for a protected query family. That raises cluster-role and canonical-claim risk even without copy changes. Required fix: Require human owner review before any drafting or content adjustment. Confirm the opening can be tightened without changing page role or contradicting protected claims.
- high: Duplicate intent risk remains medium because the opportunity must stay distinct from costs, hero training, Peace Shield, and other adjacent research pages. Required fix: Verify the page can satisfy last z research priority intent while preserving separation from research-costs.html, hero-training-cost pages, and peace-shield guidance.
- medium: No exact replacements are provided, so there is no narrow literal candidate set to review for safe replacement behavior. Required fix: If an Editor follow-up introduces exact replacements, require literal exact_old/exact_new scope, target-only edits, and owner approval before any apply_preview path.

## Reviewer Warnings

- Analytics signals support the opportunity, but they do not prove a rewrite is required.
- The brief asks for stronger first-screen intent match, which may affect cornerstone framing if handled too aggressively.
- The required checks include manual first-screen and internal-link review, so readiness depends on human validation after any drafting.

## Owner Questions

- Should the opening line explicitly mention last z research priority, or should the intent stay implied through the existing quick-answer structure?
- Do you want the related-links block to foreground progression pages or keep the current mixed Research cluster balance?
- Is there any approved wording boundary for emphasizing T10 and Urgent Rescue in the first screen?

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on research.html`

## Next Step

Route to human owner review. If approved, proceed with a brief-level planning pass only, then validate against the required checks before any edit draft is prepared.
