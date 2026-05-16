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

Keep hq.html as a cornerstone progression guide, but tighten the first-screen answer so it explicitly cross-checks HQ requirements and dependency planning without changing page role or cluster fit.

## First-Screen Plan

Preserve the answer-first structure. Keep the opening focused on the best HQ path for most players, but make the first visible answer clearly state the requirement cross-check angle: early rush, required-buildings-only upgrades, HQ30 target, then a separate HQ31-35 steel phase. Avoid adding a new intent or expanding into a different guide type. Keep the short supporting line immediately after the answer so users can confirm this is a planning guide, not a full route map.

## Section Plan

- Quick Answer: Keep the existing answer-first block, but make the promise more explicit about HQ requirement verification and progression planning. Reason: This is the highest-value first-screen area and should immediately satisfy the cross-check intent.
- Best overall recommendation: Add or refine the summary logic around when to rush, when to stop for required buildings, and when HQ30 becomes the main checkpoint. Reason: Users need a simple decision rule, not just a level list.
- Decision framework: Clarify the difference between normal early progression and the heavier HQ31-35 phase, including why steel changes the plan. Reason: This keeps the guide useful for planning and reduces confusion about the late-game jump.
- Cluster route block: Keep the route block limited to the existing progression cluster and make the internal route order explicit. Reason: The page should reinforce the existing cluster role and avoid drifting into unrelated topics.
- Related guides / FAQ: Retain related links, but prioritize pages that support progression, leveling, building order, and resource planning. Reason: This helps users move to adjacent planning pages without broadening the page intent.

## Internal Link Plan

- upstream `index.html`: Keep the main hub link as the top-level route into the progression cluster.
- lateral `start.html`: Supports new players who need the earliest progression context before HQ planning.
- lateral `early-game-optimization.html`: Helps users optimize the pre-HQ30 phase without duplicating HQ-specific coverage.
- lateral `base-building-order.html`: Directly supports dependency and building-priority planning.
- downstream `hq-construction-cost.html`: Useful follow-up for users who want detailed HQ cost and requirement data.
- downstream `resources.html`: Supports resource planning around upgrade timing and bottlenecks.
- downstream `steel.html`: Relevant for the HQ31-35 progression phase where steel becomes the limiter.

## Protected Claims

- None

## Do Not Change

- Do not change the existing page template, navigation pattern, or schema family.
- Do not turn hq.html into a different page role or a new intent.
- Do not add unsupported external game claims beyond the current canonical framing.
- Do not use analytics as proof of a rewrite need.
- Do not broaden the page into a competitor-style reference dump.
- Do not create a new page for this opportunity.

## Owner Questions

- Can the external HQ and progression reference be confirmed against canonical site memory or owner-approved reference data before any user-visible wording is finalized?
- Do you want the first-screen answer to mention HQ30 and HQ31-35 explicitly, or keep the current phrasing and only sharpen the supporting sentence?
- Should the cluster route block stay exactly as-is structurally, with only wording tightened for route clarity?

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

- first_screen_update `hq.html` at `p.qa-lede`; owner approval required: `true`

## Next Step

Have an owner verify the external reference against canonical knowledge, then decide whether this can be applied as a narrow first-screen clarification with no page-role change.
