# LLM Editor Brief - codes-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `codes.html`
- Request: `automation/reports/llm-editor-brief-codes-gsc-opportunity-request.json`
- Result: `automation/reports/llm-editor-brief-codes-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Brief Summary

Update the existing codes.html cornerstone guide with a tighter first-screen answer and supporting structure for gift center searchers, while preserving the redeem-codes page role, canonical claims, and cluster separation. The main opportunity is query-to-page match improvement, not a content expansion into a different intent.

## First-Screen Plan

Keep the answer-first format, but make the opening immediately clarify that the official redeem flow happens through the Gift Center, that the user needs their UID, and that rewards arrive in the in-game mailbox. The first screen should resolve the `last z gift center` intent faster than the current version while staying within the existing page role and avoiding any suggestion that codes are redeemed directly in-game or on a different canonical page.

## Section Plan

- Quick Answer: Tighten the opening to lead with the official Gift Center path, UID requirement, and mailbox reward collection in a concise, scannable way. Reason: This is the strongest query-intent alignment lever for users arriving on a gift-center query and is the safest surface for CTR and usefulness improvements.
- Best overall recommendation: Reframe the recommendation ordering so the official Gift Center flow is clearly the default path before secondary troubleshooting or contextual details. Reason: Preserves answer-first behavior while reducing ambiguity for searchers who want the login/redeem destination immediately.
- Decision framework: Keep the framework focused on when to use the Gift Center, where to get the UID, and what to check if redemption fails, without broadening into unrelated economy topics. Reason: Supports decision-making without diluting the page’s canonical role or cluster boundaries.
- Cluster route block: Retain and sharpen routing to related pages so gift-center-uid.html and redeem-code-not-working.html handle adjacent needs, while downstream pages cover progression/economy context. Reason: Reinforces cluster role separation and reduces overlap with other Economy pages.
- Related guides / FAQ: Audit FAQs for duplication and keep only questions that support the official redeem flow, UID lookup, and mailbox delivery. Reason: Prevents intent drift and protects canonical claims while still giving users next-step help.
- Active Last Z Codes (Verified): Keep the verified codes area, but ensure it does not overshadow the Gift Center intent on first load. Reason: Maintains the page’s existing utility while improving query match for gift-center searches.
- Verification Protocol: Preserve the verification notes, but align them with the same official flow and avoid adding new claims beyond approved scope. Reason: Supports trust without changing the page into a different archetype.
- Important Notes: Trim or reorder notes so the essential redeem path remains prominent and the page does not read like a general help hub. Reason: Keeps the cornerstone page focused and reduces fragmentation of the primary answer.

## Internal Link Plan

- lateral `gift-center-uid.html`: Best next step for users who need help locating or copying their UID for the official Gift Center flow.
- lateral `redeem-code-not-working.html`: Handles troubleshooting when a code fails after the user follows the official redeem flow.
- lateral `resources.html`: Useful hub for related help and supporting references without expanding the main page’s role.
- upstream `index.html`: Primary site entry point that can contextualize the main economy/codes cluster.
- downstream `diamond-reserve.html`: Adjacent economy topic that can receive users after they understand the redeem flow.
- downstream `events.html`: Relevant downstream destination for reward-related progression after redemption.
- downstream `f2p.html`: Supports players looking for broader economy guidance beyond the redeem flow.
- downstream `lucky-discounter.html`: Related economy guide that can serve users exploring optimization and value topics.

## Protected Claims

- `gift-center-cluster-role-separation`
- `gift-center-only-redeem-flow`
- `gift-rewards-mailbox`

## Do Not Change

- Do not publish or apply content changes from this brief automatically.
- Do not change the existing page template, navigation pattern, or schema family without separate approval.
- Do not create a new page when the Scout proposal recommends updating an existing page.
- Do not use analytics signals as proof that a rewrite is required.
- The query intent is already better served by another canonical page.
- The proposed change would blur cluster role separation.
- The improvement cannot be expressed without changing a cornerstone page beyond the approved scope.
- Do not contradict canonical claim `gift-center-cluster-role-separation`.
- Do not contradict canonical claim `gift-center-only-redeem-flow`.
- Do not contradict canonical claim `gift-rewards-mailbox`.

## Owner Questions

- Can we tighten the first-screen answer on codes.html so it more explicitly resolves `last z gift center` while keeping the page a redeem-codes cornerstone guide?
- Should the current heading order be adjusted so the Gift Center login/UID guidance appears before deeper code lists and reference sections?
- Are there any phrases in the existing FAQs or notes that risk implying a different redeem flow or weakening cluster separation?
- Should the related-links block prioritize gift-center-uid.html and redeem-code-not-working.html more prominently for gift-center searchers?
- Is the current scope limited to clarity and ordering, or do you want any section-level pruning to reduce overlap with adjacent Economy pages?

## Required Context Before Patch

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `codes.html`
- `index.html`
- `gift-center-uid.html`
- `redeem-code-not-working.html`
- `resources.html`

## Acceptance Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on codes.html`

## Next Step

Have the page owner confirm whether a scoped first-screen and heading-order adjustment is acceptable for codes.html, with explicit review of cluster separation and protected claims before any content work.
