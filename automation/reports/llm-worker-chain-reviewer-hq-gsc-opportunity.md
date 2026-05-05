# LLM Reviewer Gate - hq-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `hq.html`
- Request: `automation/reports/llm-worker-chain-reviewer-hq-gsc-opportunity-request.json`
- Result: `automation/reports/llm-worker-chain-reviewer-hq-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: review gate only; no final public page copy or patch specs were generated.

## Verdict

- Verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `none`
- Owner approval required: `true`

## Blocking Issues

- high: The opportunity is explicitly flagged as low-priority/monitor-only and the current query appears possibly better served by another canonical page, so the brief does not justify advancing beyond review. Required fix: Obtain owner confirmation that hq.html remains the correct canonical target for this query family before any edit or proposal work.
- high: Cluster role separation is at risk: the brief aims to improve HQ guidance while preserving a cornerstone progression role, but the intent may overlap with start/onboarding and adjacent progression pages. Required fix: Verify against content index and canonical page mapping that hq.html should stay the primary HQ strategy destination and will not blur into start.html or other progression pages.
- medium: Canonical HQ requirement claims are not verified in the brief, yet the planned edit would likely depend on specific requirements, costs, and timing statements. Required fix: Cross-check canonical claims and source-backed HQ requirements before any content change is drafted.
- medium: Template and schema safety cannot be fully confirmed from the planning brief alone, even though the request says to preserve the existing template and navigation pattern. Required fix: Run the deterministic QA checks and confirm no template, schema family, or navigation pattern changes are needed.

## Warnings

- Analytics signals are present but are not proof that a rewrite is required.
- The brief is no-write only; no public copy, patch specs, or backlog artifacts should be produced from this review.
- The requested first-screen improvement is directionally consistent with the page role, but the scope may still be too close to a broader onboarding or progression hub.
- Owner approval is required before any user-visible change on a cornerstone page.

## Duplicate Intent Review

Potential overlap exists with start.html and general progression content. The query looks HQ-specific, but the brief itself acknowledges that the title/intent is broad and could overlap with onboarding/progression search intent. Do not advance until canonical intent ownership is confirmed.

## Cluster Role Review

Page is correctly labeled cornerstone-guide in the Progression cluster, and the proposed adjustment preserves that role in principle. However, the requested opening-answer rewrite could pull the page toward a broader planning hub if not tightly constrained to HQ strategy only.

## Canonical Claim Review

No protected claims are listed, but HQ requirements, costs, and timing statements are likely factual claims that must be verified against canonical sources before editing. Treat any exact upgrade thresholds or resource requirements as requiring source confirmation.

## Template Safety Review

Safe to keep the existing template and nav pattern only if the change remains within the current answer-first structure and does not alter schema family or page archetype. The brief does not provide enough evidence to approve template safety beyond no-write planning.

## Owner Questions

- Should hq.html remain the canonical page for HQ upgrade strategy, or is another progression page the better canonical match?
- Should the opening answer explicitly foreground HQ30 as the main breakpoint, or keep that detail secondary?
- Do any HQ requirement/cost/timing details need to be locked to canonical wording before editing?
- Is the desired emphasis closer to speed-rush guidance or resource-efficiency guidance for this page?

## Required Context Before Edit

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `hq.html`
- `start.html`
- `index.html`
- `early-game-optimization.html`
- `base-building-order.html`
- `shooter-stages.html`

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on hq.html`

## Next Step

Pause for owner clarification and canonical-source verification; if confirmed, run the no-write reviewer/editor QA path before any proposal or edit stage.
