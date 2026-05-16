# LLM Proposal Intake - external-research-costs-external-cross-check

## Status

- State: `approved_for_intake`
- Target: `research-costs.html`
- Review verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `proposal`
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
- Owner questions must be answered before any public content proposal is written.

## Owner Questions

- Do you want research-costs.html to stay strictly as a branch router and cross-check hub, or should any section become more explicit about coverage validation?
- Are the current downstream branch links the final verified set for the comparison grid?
- Should the recommended route wording remain locked to the current canonical order, even if future balance changes occur?

## Reviewer Blocking Issues

- high: The brief confirms the topic duplicates an existing page intent and does not add a distinct player job. Required fix: Get owner confirmation that research-costs.html should remain an atlas router and that no separate page or broadened scope is needed.
- high: The external claim cannot be verified from the provided material alone. Required fix: Verify the branch coverage and cost-table claims against canonical site memory plus one additional reliable source or owner confirmation before any copy change.
- medium: The request is close to a cross-check maintenance pass but still risks blurring cluster roles if widened beyond the opening answer and route clarity. Required fix: Keep any future work narrowly scoped to first-screen clarity and verified link coverage only, with no new research guide behavior.

## Reviewer Warnings

- No exact_replacements were provided, so there is no candidate replacement to approve or reject.
- Canonical claims must remain intact, especially field-research-follows-siege, research-atlas-role, and research-best-mainline.
- Do not treat the external reference as proof; it is only a discovery signal.
- Manual first-screen and internal-link review is required before any edit decision.

## Proposed Backlog Item

- topic_id: `external-research-costs-external-cross-check-llm-approved-intake`
- title: `External source opportunity: research cost and branch coverage cross-check`
- cluster: `Research`
- recommended_action: `update_existing`
- archetype_suggestion: `atlas-page`
- target_page_or_slug: `research-costs.html`
- source_type: `analytics`
- source_reference: `LLM worker chain review: external-research-costs-external-cross-check`
- confidence: `high`
- priority: `high`
- status: `backlog`
- notes: `Created as a proposed LLM intake record only. Do not add to topic_backlog.csv or create content changes without human review.`

## Editor Brief Summary

Keep research-costs.html as an atlas page and improve only the first-screen answer and route clarity so it better supports branch coverage cross-checking. Maintain the existing Research cluster role, canonical claims, and downstream branch links; do not widen scope into a new page type.

## First-Screen Plan

Preserve the answer-first structure. Make the opening paragraph or quick answer clearly state that this page is a branch router and cross-check hub, then point users to the exact branch cost pages for node-by-node totals. Keep the main route guidance intact and do not add new claims that would change the page role. The first screen should immediately answer what the page is for, how to use it, and which route is the default for most players.

## Draft Exact Replacements

- Count: `0`
- Scope: proposal-only data; no public content edit is approved here.

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on research-costs.html`

## Next Actions

- Review this intake artifact before converting it into a run-plan proposal.
- Run: python3 automation/pipeline.py worker-run-plan --intake automation/reports/llm-intake-external-research-costs-external-cross-check.json --json
- Do not write public content until a later proposal artifact receives explicit owner approval.
