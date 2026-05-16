# LLM Editor Brief - external-gift-center-official-flow-validation

## Overview

- State: `completed`
- Provider: `openai`
- Target: `gift-center-uid.html`
- Request: `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-gift-center-official-flow-validation-request.json`
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-gift-center-official-flow-validation-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Warnings

- Dropped unsafe LLM Editor exact_replacements[1]: LLM Editor exact_replacements[1].exact_old must match `gift-center-uid.html` exactly once; found 0 matches.

## Brief Summary

Keep the page as a support guide on official Gift Center login and UID setup, with a narrow first-screen clarification that strengthens route validation without changing cluster role or adding a new player job.

## First-Screen Plan

Preserve the answer-first layout. Make the opening answer explicitly validate the official browser-based Gift Center flow, UID copy path, and mailbox reward delivery in a way that reinforces the existing support-guide role. Keep the same template wrapper, class names, and route labels. Do not broaden into a general redemption or store-guide page.

## Section Plan

- Quick Answer: Tighten the lead so the first screen clearly states the official browser flow, UID copy path, and mailbox outcome. Reason: This is the highest-value place to answer the user job quickly while staying within the existing page role.
- Exact procedural answer: Keep the step order focused on official login, UID copy, browser redemption, and reward delivery. Reason: The user needs a precise validation flow, not a new topic or a generic help article.
- Common mistakes or edge cases: Retain and, if needed, slightly sharpen the warnings about wrong UID entry, in-app redemption, and checking the mailbox. Reason: These are the main failure points for the existing user job.
- Step-by-step checks: Ensure the checks map directly to the official flow and can be scanned quickly on mobile. Reason: Supports fast validation without altering the page structure.
- Related next step: Keep internal routing toward start, f2p, codes, and redeem-code-not-working as the next logical paths. Reason: Preserves cluster separation and helps users branch to adjacent intent pages.

## Internal Link Plan

- upstream `index.html`: Keeps the page anchored in the main site hub and preserves existing information architecture.
- downstream `start.html`: Useful for players who need onboarding after confirming the Gift Center flow.
- downstream `f2p.html`: Relevant follow-on guidance for players evaluating progression and economy context.
- lateral `codes.html`: Adjacent but distinct intent for players looking for code lists rather than setup validation.
- lateral `redeem-code-not-working.html`: Useful fallback when the official flow does not work as expected.
- lateral `resources.html`: Potential supporting guide destination if the site uses it for related help content.

## Protected Claims

- `gift-center-cluster-role-separation`
- `gift-center-only-redeem-flow`
- `gift-rewards-mailbox`
- `uid-copy-path`

## Do Not Change

- Do not publish or apply content changes from this brief automatically.
- Do not change the existing page template, navigation pattern, or schema family without separate approval.
- Do not create a new page when the Scout proposal recommends updating an existing page.
- Do not use analytics signals as proof that a rewrite is required.
- The topic duplicates an existing page intent without adding a distinct player job.
- The external claim cannot be verified beyond this source.
- The proposal would blur existing cluster roles.
- Do not contradict canonical claim `gift-center-cluster-role-separation`.
- Do not contradict canonical claim `gift-center-only-redeem-flow`.
- Do not contradict canonical claim `gift-rewards-mailbox`.

## Owner Questions

- Do you want the first screen to emphasize official routing verification more strongly, or should it stay almost unchanged aside from minor clarity edits?
- Is `resources.html` still a valid related destination for this cluster, or should it be removed from the internal link plan?
- Should we keep the page title as a pure setup/login framing, or is a subtle clarity tweak approved for the first-screen heading only?

## Required Context Before Patch

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `gift-center-uid.html`
- `index.html`
- `codes.html`
- `redeem-code-not-working.html`
- `resources.html`

## Acceptance Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on gift-center-uid.html`

## Draft Exact Replacements

Proposal-only candidates. They do not approve copy, create Patch Specs, edit files, or bypass owner review.

- safe_exact_replace `gift-center-uid.html` at `meta[name="description"]`; owner approval required: `true`

## Next Step

Verify the current file against canonical claims and nearby cluster pages, then decide whether only the first-screen and meta description need narrow approval-ready edits or whether the page should stay unchanged.
