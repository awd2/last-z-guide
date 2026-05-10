# LLM Editor Brief - alliance-duel-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `alliance-duel.html`
- Request: `automation/reports/llm-worker-chain-editor-alliance-duel-gsc-opportunity-request.json`
- Result: `automation/reports/llm-worker-chain-editor-alliance-duel-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Brief Summary

Keep the existing event-guide page and improve only the opening answer, schedule framing, and related-link usefulness for last z vs schedule intent. Do not broaden the page into a hub or change the cluster role.

## First-Screen Plan

Preserve the answer-first structure. Make the opening clearly state the Day 1 to Day 6 VS schedule and the main timing rule, then point users to the best matching action for the day. Keep the page anchored to alliance duel schedule intent, not general event browsing. The first screen should answer who this is for, what the weekly rotation is, and when to commit bigger actions using Full Preparedness timing, without changing the page role or introducing a broader event overview.

## Section Plan

- Quick Answer: Tighten the opening so it directly answers the schedule query and summarizes the day-by-day rotation plus the main timing rule. Reason: The current page already has answer-first structure, but the query match needs to be more explicit for last z vs schedule searchers.
- Schedule or timing block: Keep a compact Day 1 to Day 6 timing block with clear labels for each day and the recommended action type. Reason: This is the core intent for the page and supports fast scanning.
- Best strategy: Clarify the spend-when-matching-day rule and the idea of saving bigger actions for Full Preparedness windows. Reason: This improves usefulness without expanding scope beyond the existing event guide.
- Rewards and tradeoffs: Keep the rewards discussion focused on weekly value and tradeoffs of skipping non-matching days. Reason: Users need decision support, but the page should remain a schedule guide, not a rewards hub.
- Related event links: Audit the related links so they reinforce the Events cluster and point to closely related pages only. Reason: This preserves cluster separation and helps internal routing.
- Frequently Asked Questions: Ensure FAQs answer common schedule questions, timing questions, and what to do if a player cannot hit every day. Reason: FAQ content can capture long-tail schedule intent while staying on-topic.
- Related Guides: Keep only lateral or downstream event-related links that support the same user job. Reason: Prevents the page from drifting into unrelated guide territory.

## Internal Link Plan

- upstream `index.html`: Homepage is a natural top-level route into the Events cluster.
- upstream `events.html`: Events hub supports discovery while keeping cluster structure intact.
- lateral `alliance-duel-rewards.html`: Close sibling page for users who want rewards detail after reading the schedule.
- lateral `canyon-clash.html`: Nearby event guide that may satisfy adjacent event intent without duplicating this page.
- lateral `zombie-siege.html`: Another event guide in the same cluster for related event browsing.
- downstream `alliance-recognition-cost.html`: Supportive detail page for players planning event spend and recognition timing.
- downstream `heroes.html`: Useful supporting system page when the schedule involves hero-focused actions.
- downstream `lucky-discounter.html`: Potentially relevant planning page for spending efficiency during event windows.

## Protected Claims

- None

## Do Not Change

- Do not change the existing page template, navigation pattern, or schema family without separate approval.
- Do not create a new page when the Scout proposal recommends updating an existing page.
- Do not broaden alliance-duel.html into a generic event hub.
- Do not use analytics signals as proof that a rewrite is required.
- Do not change canonical cluster separation between Events pages and adjacent guide pages.
- Do not publish or apply content changes from this brief automatically.

## Owner Questions

- Is alliance-duel.html still the best canonical home for last z vs schedule intent, or should another Events page own the primary query?
- Should the update stay limited to the first screen and related links, or is a deeper schedule and FAQ refinement approved?
- Are there any cluster boundary concerns with linking to or from rewards and recognition detail pages?
- Should Full Preparedness timing be emphasized on the first screen or kept lower on the page?

## Required Context Before Patch

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `alliance-duel.html`
- `index.html`
- `events.html`
- `alliance-duel-rewards.html`
- `canyon-clash.html`
- `zombie-siege.html`

## Acceptance Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on alliance-duel.html`

## Draft Exact Replacements

Proposal-only candidates. They do not approve copy, create Patch Specs, edit files, or bypass owner review.

- None

## Next Step

Run the no-write Editor and Reviewer stages on alliance-duel.html, then ask the owner to approve any narrow first-screen or link-only adjustment before any content patch is drafted.
