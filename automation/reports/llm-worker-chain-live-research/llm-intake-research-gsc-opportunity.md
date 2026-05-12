# LLM Proposal Intake - research-gsc-opportunity

## Status

- State: `approved_for_intake`
- Target: `research.html`
- Review verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `brief`
- Approved by: `oleg`
- Approval scope: `intake_only_no_content_edits`
- Content edit approved: `false`
- Public content change allowed: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified by this LLM intake bridge.

## Approval Guardrails

- Approval is intake-only: it allows conversion into the existing run-plan/proposal flow.
- Approval does not approve public page copy, patch specs, backlog mutation, manifest creation, PR creation, deployment, or production publishing.
- Any carried exact_replacements are proposal-only data and still require propose, owner approval, apply-preview, apply-approved, and strict QA.
- Any future public content change still requires exact proposed text/diff and explicit owner approval.
- Future content proposals must still pass deterministic checks before closeout.

## Blockers

- None

## Warnings

- LLM Reviewer blocking issues were owner-resolved for intake only; public content is still not approved.
- High-risk opportunity; keep the future proposal narrow and owner-reviewed.
- Owner questions must be answered before any public content proposal is written.

## Owner Questions

- Should the opening line explicitly mention last z research priority, or should the intent stay implied through the existing quick-answer structure?
- Do you want the related-links block to foreground progression pages or keep the current mixed Research cluster balance?
- Is there any approved wording boundary for emphasizing T10 and Urgent Rescue in the first screen?

## Reviewer Blocking Issues

- high: The page is a cornerstone guide and the request touches first-screen positioning for a protected query family. That raises cluster-role and canonical-claim risk even without copy changes. Required fix: Require human owner review before any drafting or content adjustment. Confirm the opening can be tightened without changing page role or contradicting protected claims.
- high: Duplicate intent risk remains medium because the opportunity must stay distinct from costs, hero training, Peace Shield, and other adjacent research pages. Required fix: Verify the page can satisfy last z research priority intent while preserving separation from research-costs.html, hero-training-cost pages, and peace-shield guidance.
- medium: No exact replacements are provided, so there is no narrow literal candidate set to review for safe replacement behavior. Required fix: If an Editor follow-up introduces exact replacements, require literal exact_old/exact_new scope, target-only edits, and owner approval before any apply_preview path.

## Reviewer Warnings

- Analytics signals support the opportunity, but they do not prove a rewrite is required.
- The brief asks for stronger first-screen intent match, which may affect cornerstone framing if handled too aggressively.
- The required checks include manual first-screen and internal-link review, so readiness depends on human validation after any drafting.

## Proposed Backlog Item

- topic_id: `research-gsc-opportunity-llm-approved-intake`
- title: `GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path`
- cluster: `Research`
- recommended_action: `update_existing`
- archetype_suggestion: `cornerstone-guide`
- target_page_or_slug: `research.html`
- source_type: `llm_scout`
- source_reference: `LLM worker chain review: research-gsc-opportunity`
- confidence: `high`
- priority: `high`
- status: `backlog`
- notes: `Created as a proposed LLM intake record only. Do not add to topic_backlog.csv or create content changes without human review.`

## Editor Brief Summary

Tighten the existing research.html opening so it answers research priority intent faster, while keeping the page a cornerstone research guide and preserving protected claims plus cluster separation.

## First-Screen Plan

Keep the answer-first structure, but make the opening explicitly orient around best research order and progression. The first screen should state the practical sequence, the main decision criteria, and the reason the page exists without drifting into a costs-only, hero-only, or Peace Shield-only angle. Preserve the current canonical claims and ensure the opening remains consistent with the existing mainline guidance.

## Draft Exact Replacements

- Count: `0`
- Scope: proposal-only data; no public content edit is approved here.

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on research.html`

## Next Actions

- Review this intake artifact before converting it into a run-plan proposal.
- Run: python3 automation/pipeline.py worker-run-plan --intake automation/reports/llm-worker-chain-live-research/llm-intake-research-gsc-opportunity.json --json
- Do not write public content until a later proposal artifact receives explicit owner approval.
