# LLM Proposal Intake - hq-gsc-opportunity

## Status

- State: `blocked`
- Target: `hq.html`
- Review verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `none`
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

- LLM Reviewer returned blocking issues; resolve them before LLM intake.

## Warnings

- None

## Owner Questions

- Should hq.html remain the canonical page for HQ upgrade strategy, or is another progression page the better canonical match?
- Should the opening answer explicitly foreground HQ30 as the main breakpoint, or keep that detail secondary?
- Do any HQ requirement/cost/timing details need to be locked to canonical wording before editing?
- Is the desired emphasis closer to speed-rush guidance or resource-efficiency guidance for this page?

## Reviewer Blocking Issues

- high: The opportunity is explicitly flagged as low-priority/monitor-only and the current query appears possibly better served by another canonical page, so the brief does not justify advancing beyond review. Required fix: Obtain owner confirmation that hq.html remains the correct canonical target for this query family before any edit or proposal work.
- high: Cluster role separation is at risk: the brief aims to improve HQ guidance while preserving a cornerstone progression role, but the intent may overlap with start/onboarding and adjacent progression pages. Required fix: Verify against content index and canonical page mapping that hq.html should stay the primary HQ strategy destination and will not blur into start.html or other progression pages.
- medium: Canonical HQ requirement claims are not verified in the brief, yet the planned edit would likely depend on specific requirements, costs, and timing statements. Required fix: Cross-check canonical claims and source-backed HQ requirements before any content change is drafted.
- medium: Template and schema safety cannot be fully confirmed from the planning brief alone, even though the request says to preserve the existing template and navigation pattern. Required fix: Run the deterministic QA checks and confirm no template, schema family, or navigation pattern changes are needed.

## Reviewer Warnings

- Analytics signals are present but are not proof that a rewrite is required.
- The brief is no-write only; no public copy, patch specs, or backlog artifacts should be produced from this review.
- The requested first-screen improvement is directionally consistent with the page role, but the scope may still be too close to a broader onboarding or progression hub.
- Owner approval is required before any user-visible change on a cornerstone page.

## Proposed Backlog Item

- topic_id: `hq-gsc-opportunity-llm-approved-intake`
- title: `GSC opportunity review: Last Z HQ Upgrade Guide — Requirements, Fast Path, and HQ 30/35 Strategy`
- cluster: `Progression`
- recommended_action: `monitor`
- archetype_suggestion: `cornerstone-guide`
- target_page_or_slug: `hq.html`
- source_type: `llm_scout`
- source_reference: `LLM worker chain review: hq-gsc-opportunity`
- confidence: `medium`
- priority: `high`
- status: `backlog`
- notes: `Created as a proposed LLM intake record only. Do not add to topic_backlog.csv or create content changes without human review.`

## Editor Brief Summary

Keep hq.html as the cornerstone progression guide, but tighten the opening to answer the HQ upgrade query immediately, then structure the page around fast-path leveling, required-building decisions, and the HQ30→35 steel phase without shifting cluster role.

## First-Screen Plan

Preserve answer-first layout. The first screen should immediately confirm the page solves HQ upgrade requirements and fast-path strategy, then signal the split between early rush progression and the heavier HQ31–35 steel phase. Keep the existing template and avoid introducing a different content mission or persona. The opening should help users decide whether to rush, what to upgrade now, and when the guide changes after HQ30.

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on hq.html`

## Next Actions

- Read the LLM latest owner review and resolve blocking issues.
- Rerun the LLM worker chain after the Scout/Editor/Reviewer issue is fixed.
