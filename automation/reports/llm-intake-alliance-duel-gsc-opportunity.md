# LLM Proposal Intake - alliance-duel-gsc-opportunity

## Status

- State: `approved_for_intake`
- Target: `alliance-duel.html`
- Review verdict: `needs_human_review`
- Risk: `medium`
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
- Owner questions must be answered before any public content proposal is written.

## Owner Questions

- Is alliance-duel.html still the best canonical home for last z vs schedule intent, or should another Events page own the primary query?
- Should the update stay limited to the first screen and related links, or is a deeper schedule and FAQ refinement approved?
- Are there any cluster boundary concerns with linking to or from rewards and recognition detail pages?
- Should Full Preparedness timing be emphasized on the first screen or kept lower on the page?

## Reviewer Blocking Issues

- medium: The brief is directionally consistent, but canonical ownership for last z vs schedule intent is not fully proven from the provided context alone. Required fix: Have an owner confirm alliance-duel.html remains the best canonical home before any scoped content work is drafted.
- medium: Cluster separation could blur if the update expands beyond the first screen and compact schedule framing. Required fix: Keep the scope limited to answer-first opening, schedule block, strategy, rewards tradeoffs, and related links only, with no hub-style expansion.

## Reviewer Warnings

- Analytics signals are supportive but not proof of rewrite need.
- No exact_replacements were provided, so there is no replacement safety candidate to approve.
- The page already has a strong event-guide role, so changes must stay narrow to avoid role drift.

## Proposed Backlog Item

- topic_id: `alliance-duel-gsc-opportunity-llm-approved-intake`
- title: `GSC opportunity review: Last Z Alliance Duel Guide — Schedule, Day 1–6 Plan, and VS Strategy`
- cluster: `Events`
- recommended_action: `update_existing`
- archetype_suggestion: `event-guide`
- target_page_or_slug: `alliance-duel.html`
- source_type: `llm_scout`
- source_reference: `LLM worker chain review: alliance-duel-gsc-opportunity`
- confidence: `high`
- priority: `high`
- status: `backlog`
- notes: `Created as a proposed LLM intake record only. Do not add to topic_backlog.csv or create content changes without human review.`

## Editor Brief Summary

Keep the existing event-guide page and improve only the opening answer, schedule framing, and related-link usefulness for last z vs schedule intent. Do not broaden the page into a hub or change the cluster role.

## First-Screen Plan

Preserve the answer-first structure. Make the opening clearly state the Day 1 to Day 6 VS schedule and the main timing rule, then point users to the best matching action for the day. Keep the page anchored to alliance duel schedule intent, not general event browsing. The first screen should answer who this is for, what the weekly rotation is, and when to commit bigger actions using Full Preparedness timing, without changing the page role or introducing a broader event overview.

## Draft Exact Replacements

- Count: `0`
- Scope: proposal-only data; no public content edit is approved here.

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on alliance-duel.html`

## Next Actions

- Review this intake artifact before converting it into a run-plan proposal.
- Run: python3 automation/pipeline.py worker-run-plan --intake automation/reports/llm-intake-alliance-duel-gsc-opportunity.json --json
- Do not write public content until a later proposal artifact receives explicit owner approval.
