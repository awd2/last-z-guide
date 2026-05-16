# LLM Editor Brief - external-gift-center-official-flow-validation

## Overview

- State: `completed`
- Provider: `openai`
- Target: `gift-center-uid.html`
- Request: `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-gift-center-official-flow-validation-request.json`
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-editor-external-gift-center-official-flow-validation-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Brief Summary

Keep the page as an answer-first support guide for Gift Center routing and UID setup, but tighten the opening so it clearly validates the official browser redeem flow without shifting page role or cluster boundaries.

## First-Screen Plan

Preserve the existing answer-first structure. The first screen should immediately state the official flow: open the Gift Center in a browser, copy UID from Avatar -> Settings -> Copy ID, redeem outside the game client, and expect rewards in the in-game mailbox. Keep the framing as verification and setup guidance, not a broader store or account help page. Do not introduce new claims beyond the canonical flow.

## Section Plan

- Quick Answer: Keep the answer-first lead and make sure the opening directly resolves the routing and UID setup question. Reason: This matches the page job and gives the quickest confirmation for users checking the official redeem flow.
- Exact procedural answer: Retain the step sequence for browser redemption and UID copy path, with no expansion into unrelated account topics. Reason: The page must preserve the canonical redeem-only flow and avoid cluster drift.
- Common mistakes or edge cases: Keep only narrowly relevant mistakes such as using the game client instead of the browser or pasting the wrong UID. Reason: Helps users avoid the main failure points without changing the page scope.
- Step-by-step checks: Ensure the verification steps map to the official flow and are easy to scan on mobile. Reason: Supports the user job of confirming setup accuracy quickly.
- Related next step: Point users to downstream or adjacent help pages that solve follow-on issues, not to unrelated store or general support content. Reason: Keeps internal routing aligned with the support cluster and avoids role blur.

## Internal Link Plan

- upstream `index.html`: Main hub entry point for the site and a logical parent route.
- downstream `f2p.html`: Helpful follow-on for players who want economy or progression context after redeem setup.
- downstream `start.html`: Useful next step for onboarding after confirming the redemption flow.
- lateral `codes.html`: Adjacent page for code discovery and redemption context.
- lateral `redeem-code-not-working.html`: Best troubleshooting companion when the redeem flow fails.
- lateral `resources.html`: Optional reference hub if it exists in the site map and remains relevant to support guidance.

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

- Is the official routing check meant to validate only the browser redeem flow, or also a store purchase flow on the same domain?
- Should UID setup remain framed as a support detail, or do we want to surface it as part of the main player flow?
- Is `resources.html` still an approved lateral destination for this cluster?

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

- None

## Next Step

Verify the public flow against canonical site memory and one additional reliable source, then decide whether a narrow first-screen adjustment is needed on the existing page.
