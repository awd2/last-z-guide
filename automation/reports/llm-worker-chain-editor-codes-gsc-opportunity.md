# LLM Editor Brief - codes-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `codes.html`
- Request: `automation/reports/llm-worker-chain-editor-codes-gsc-opportunity-request.json`
- Result: `automation/reports/llm-worker-chain-editor-codes-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Brief Summary

Refine the existing cornerstone codes page to better answer “last z gift center” on the first screen while keeping the page in the redeem-codes cluster and preserving the official Gift Center login + UID + mailbox flow boundaries.

## First-Screen Plan

Keep answer-first structure, but make the opening clearly orient users to the official Gift Center redeem path: state that codes are redeemed through the official Gift Center using UID, then point to the exact next action and the mailbox reward retrieval step. The first screen should reduce ambiguity for gift-center searchers, reinforce that this is the codes page, and avoid drifting into a standalone login hub or mailbox explainer.

## Section Plan

- Quick Answer: Tighten the opening to satisfy gift-center intent immediately with a concise redeem-path summary and next-step guidance. Reason: This is the highest-impact place to improve query-page match and reduce pogo-sticking for gift-center searchers.
- Best overall recommendation: Keep the recommended path as the official redeem flow via Gift Center, with a short decision rule for when to use this page versus related guides. Reason: Supports the task without changing page role and helps distinguish redeem flow from troubleshooting or UID lookup.
- Decision framework: Clarify when users should use the codes page, when to open the UID guide, and when to use the code-not-working guide. Reason: Improves navigation and preserves cluster separation by routing users to the right supporting page.
- Cluster route block: Strengthen the internal route guidance so the page points to UID help, troubleshooting, and broader economy guides without duplicating those pages. Reason: Helps the page function as a cornerstone hub while avoiding scope creep.
- Related guides / FAQ: Ensure related links and FAQ entries support the redeem-code task and adjacent help paths, not mailbox or reward-claim ownership claims. Reason: Maintains canonical claim boundaries and gives users a clean path to downstream/lateral resources.

## Internal Link Plan

- upstream `index.html`: Keep the path from the homepage into the cornerstone guide clear for users entering from site navigation.
- lateral `gift-center-uid.html`: This is the closest support page for users who need to locate their UID before redeeming codes.
- lateral `redeem-code-not-working.html`: This is the natural troubleshooting destination when code redemption fails.
- lateral `resources.html`: Useful for broader help context and supporting references without overlapping core redeem instructions.
- downstream `start.html`: Good for onboarding users who need a broader getting-started path after redeem-code intent is satisfied.
- downstream `f2p.html`: Supports adjacent economy guidance for users exploring progression or resource planning after redemption.
- downstream `events.html`: Relevant adjacent gameplay/loot context that may follow from redeem-code interest without duplicating the redeem flow.
- downstream `diamond-reserve.html`: Broader economy adjacency that can support related resource-management intent.

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

- Should the opening phrase explicitly include the Gift Center name in the first sentence, or keep it implied to avoid overfitting to one query variant?
- Do you want the related-guides block to prioritize UID help or troubleshooting first?
- Is the current quick answer phrasing already acceptable if only the surrounding framing is sharpened?
- Are there any additional canonical claims tied to mailbox wording that should be reviewed before drafting copy?

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

Owner review of the proposed first-screen framing, link boundaries, and canonical-claim guardrails before any content draft is attempted.
