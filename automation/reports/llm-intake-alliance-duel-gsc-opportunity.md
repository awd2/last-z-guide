# LLM Proposal Intake - alliance-duel-gsc-opportunity

## Status

- State: `approved_for_intake`
- Target: `alliance-duel.html`
- Review verdict: `pass`
- Risk: `medium`
- Approved next stage: `approval`
- Approved by: `oleg`
- Approval scope: `intake_only_no_content_edits`
- Content edit approved: `false`
- Public content change allowed: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified by this LLM intake bridge.

## Approval Guardrails

- Approval is intake-only: it allows conversion into the existing run-plan/proposal flow.
- Approval does not approve public page copy, patch specs, backlog mutation, manifest creation, PR creation, deployment, or production publishing.
- Any future public content change still requires exact proposed text/diff and explicit owner approval.
- Future content proposals must still pass deterministic checks before closeout.

## Blockers

- None

## Warnings

- Owner questions must be answered before any public content proposal is written.

## Owner Questions

- Should the opening sentence be sharpened beyond the current quick answer to better match last z vs schedule intent?
- Should the schedule block emphasize only the Day 1 to Day 6 order, or also retain any existing timing caveats?
- Should the related guides set be trimmed further to reduce any cluster overlap risk?

## Reviewer Blocking Issues

- None

## Reviewer Warnings

- Analytics should remain a signal only, not proof of a rewrite need.
- Keep the update narrowly scoped so the page does not drift into a broader event hub.
- Related links should stay within the Events cluster and avoid introducing new intent overlap.

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

Keep alliance-duel.html as the canonical event-guide page, but sharpen the opening to answer last z vs schedule search intent immediately and keep the update narrowly scoped to schedule, best strategy, rewards, and related event routing.

## First-Screen Plan

Preserve the answer-first layout. Make the first screen clearly state the day-by-day Alliance Duel schedule and the key rule that players should spend only matching speed-ups on the matching day. Keep the opening focused on schedule, strategy, and weekly value so the page satisfies the query without changing its role into a broader event hub. Avoid adding unrelated event context or new promises.

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on alliance-duel.html`

## Next Actions

- Review this intake artifact before converting it into a run-plan proposal.
- Run: python3 automation/pipeline.py worker-run-plan --intake automation/reports/llm-intake-alliance-duel-gsc-opportunity.json --json
- Do not write public content until a later proposal artifact receives explicit owner approval.
