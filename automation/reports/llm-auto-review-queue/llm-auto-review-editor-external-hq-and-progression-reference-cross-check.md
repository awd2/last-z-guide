# LLM Editor Brief - external-hq-and-progression-reference-cross-check

## Overview

- State: `completed`
- Provider: `openai`
- Target: `hq.html`
- Request: `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-hq-and-progression-reference-cross-check-request.json`
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-hq-and-progression-reference-cross-check-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Brief Summary

Keep hq.html as the cornerstone HQ guide, but tighten the opening to foreground the HQ and progression requirement cross-check job, then validate section order and internal routes without changing page role or template.

## First-Screen Plan

Preserve the answer-first opening and make sure the first screen immediately states the HQ planning recommendation, the HQ30 to HQ35 split, and the construction requirement cross-check angle. Keep the current page role and do not introduce a new intent or a different content type. The opening should stay concise, direct, and useful for players comparing requirements and progression timing.

## Section Plan

- Quick Answer: Keep the answer-first structure and ensure it resolves the cross-check query fast. Reason: This is the highest-value matching section for the target job and should remain the primary entry point.
- Best overall recommendation: Retain the current recommendation shape, but align wording to HQ requirement verification and progression planning. Reason: Supports the same user job without changing the page archetype.
- Decision framework: Keep as the place where players compare rush, requirement, and steel-timer tradeoffs. Reason: Useful for distinguishing HQ30 from HQ31-35 planning.
- Cluster route block: Verify that the route block points users to progression and base-building supporting guides, not unrelated pages. Reason: Prevents cluster drift and keeps internal routing aligned with the page role.
- Related guides / FAQ: Trim or reorder links so supporting pages reinforce HQ, progression, and construction dependency planning. Reason: Helps the page act as a cornerstone within the Progression cluster.

## Internal Link Plan

- upstream `index.html`: Keeps the page anchored in the main site hierarchy.
- lateral `start.html`: Supports players who need an early entry point before HQ planning.
- lateral `early-game-optimization.html`: Complements early progression decisions that feed into HQ planning.
- lateral `base-building-order.html`: Directly supports building dependency and construction order planning.
- downstream `alliance-duel.html`: Relevant only as a progression-adjacent support link if the guide already references alliance timing.
- downstream `arena.html`: Optional supporting link for broader progression context if already used in the cluster.
- downstream `emergency-hospital-cost.html`: Useful if the guide discusses build prioritization and upgrade tradeoffs.
- downstream `furylord.html`: Keep only if the current guide already uses it as a related progression reference.

## Protected Claims

- `HQ requirement and dependency details must remain consistent with canonical site memory and owner-confirmed references.`
- `Any guidance about HQ30 to HQ35 progression timing should stay aligned with verified steel and construction constraints.`
- `Do not convert this page into a distinct reference-comparison article or a new page intent.`

## Do Not Change

- Do not publish or apply content changes from this brief automatically.
- Do not change the existing page template, navigation pattern, or schema family without separate approval.
- Do not create a new page when the Scout proposal recommends updating an existing page.
- Do not use analytics signals as proof that a rewrite is required.
- The topic duplicates an existing page intent without adding a distinct player job.
- The external claim cannot be verified beyond this source.
- The proposal would blur existing cluster roles.

## Owner Questions

- Do you want the first screen to explicitly name the HQ and progression requirement cross-check job, or keep it implicit within the existing answer-first lede?
- Should the cluster route block prioritize base-building support pages, or keep the current mix of progression-adjacent links?
- Are there any HQ requirement claims that must be locked to canonical memory before we touch section wording?

## Required Context Before Patch

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `hq.html`
- `index.html`
- `start.html`
- `early-game-optimization.html`
- `base-building-order.html`

## Acceptance Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on hq.html`

## Draft Exact Replacements

Proposal-only candidates. They do not approve copy, create Patch Specs, edit files, or bypass owner review.

- None

## Next Step

Cross-verify HQ requirement claims against canonical memory and a second reliable source before any content proposal is shaped.
