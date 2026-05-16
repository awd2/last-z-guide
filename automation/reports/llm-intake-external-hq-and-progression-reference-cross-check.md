# LLM Proposal Intake - external-hq-and-progression-reference-cross-check

## Status

- State: `approved_for_intake`
- Target: `hq.html`
- Review verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `none`
- Approved by: `Oleg`
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
- LLM Reviewer did not approve an automatic next stage; human approval is required.
- Owner questions must be answered before any public content proposal is written.

## Owner Questions

- Can the external HQ and progression reference be confirmed against canonical site memory or another owner-approved source?
- Should the first-screen answer explicitly name HQ30 and HQ31-35, or should the current phrasing be kept and only the supporting sentence clarified?
- Do you want to keep the cluster route block unchanged structurally and only tighten the wording?

## Reviewer Blocking Issues

- high: High-risk cornerstone page with an external claim that is explicitly not verified beyond the provided source. Required fix: Obtain owner confirmation or a second reliable reference before any user-visible wording is approved.
- high: The brief indicates the topic duplicates an existing page intent and may blur cluster roles. Required fix: Confirm that hq.html has a distinct planning job and that no separate page or broader reference-dump scope is being introduced.
- high: Exact replacement candidate is proposal-only and cannot be approved from this review. Required fix: Keep the replacement as a candidate only and route it through owner review before any apply step.

## Reviewer Warnings

- The current page already appears to have an answer-first structure, so changes should remain narrow and scope-safe.
- Internal link changes should preserve the existing progression cluster route and avoid role drift.
- Analytics should not be used as evidence that copy changes are required.

## Proposed Backlog Item

- topic_id: `external-hq-and-progression-reference-cross-check-llm-approved-intake`
- title: `External source opportunity: HQ and progression requirement cross-check`
- cluster: `Progression`
- recommended_action: `update_existing`
- archetype_suggestion: `cornerstone-guide`
- target_page_or_slug: `hq.html`
- source_type: `analytics`
- source_reference: `LLM worker chain review: external-hq-and-progression-reference-cross-check`
- confidence: `high`
- priority: `high`
- status: `backlog`
- notes: `Created as a proposed LLM intake record only. Do not add to topic_backlog.csv or create content changes without human review.`

## Editor Brief Summary

Keep hq.html as a cornerstone progression guide, but tighten the first-screen answer so it explicitly cross-checks HQ requirements and dependency planning without changing page role or cluster fit.

## First-Screen Plan

Preserve the answer-first structure. Keep the opening focused on the best HQ path for most players, but make the first visible answer clearly state the requirement cross-check angle: early rush, required-buildings-only upgrades, HQ30 target, then a separate HQ31-35 steel phase. Avoid adding a new intent or expanding into a different guide type. Keep the short supporting line immediately after the answer so users can confirm this is a planning guide, not a full route map.

## Draft Exact Replacements

- Count: `1`
- Scope: proposal-only data; no public content edit is approved here.

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on hq.html`

## Next Actions

- Review this intake artifact before converting it into a run-plan proposal.
- Run: python3 automation/pipeline.py worker-run-plan --intake automation/reports/llm-intake-external-hq-and-progression-reference-cross-check.json --json
- Do not write public content until a later proposal artifact receives explicit owner approval.
