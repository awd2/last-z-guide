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

Keep alliance-duel.html as the canonical event-guide page, but sharpen the opening to answer last z vs schedule search intent immediately and keep the update narrowly scoped to schedule, best strategy, rewards, and related event routing.

## First-Screen Plan

Preserve the answer-first layout. Make the first screen clearly state the day-by-day Alliance Duel schedule and the key rule that players should spend only matching speed-ups on the matching day. Keep the opening focused on schedule, strategy, and weekly value so the page satisfies the query without changing its role into a broader event hub. Avoid adding unrelated event context or new promises.

## Section Plan

- Quick Answer: Tighten the first-answer framing so it directly resolves last z vs schedule intent with the Day 1 to Day 6 pattern and the matching speed-up rule. Reason: The current page already has a quick answer, but the opening should better match the target query and improve first-screen utility.
- Schedule or timing block: Keep the Day 1 to Day 6 plan prominent and easy to scan, with a clear schedule order and any timing logic already supported by the page. Reason: Schedule intent is the main search driver, so the timing block should carry the strongest query match.
- Best strategy: Keep the VS strategy guidance narrow and practical, centered on when to hold, spend, or save resources by day. Reason: Users want actionable guidance tied to the schedule, not a generic event overview.
- Rewards and tradeoffs: Retain a compact explanation of weekly chest potential, F2P tradeoffs, and why matching tasks matter. Reason: This preserves player value while supporting the decision logic behind the schedule.
- Frequently Asked Questions: Keep only questions that support schedule, speed-up use, and day selection intent; avoid expanding into unrelated event mechanics. Reason: FAQ should reinforce the canonical query match without broadening scope.
- Related event links: Keep the related links section and align it to adjacent event guides only. Reason: This supports navigation and cluster separation while keeping the page focused.

## Internal Link Plan

- upstream `events.html`: Primary hub for the Events cluster and a natural entry point to this guide.
- upstream `index.html`: Site root path for broad discovery and cluster routing.
- lateral `alliance-duel-rewards.html`: Closest sibling topic for reward-focused follow-up without changing the main page role.
- lateral `canyon-clash.html`: Adjacent event guide that supports related event navigation within the same cluster.
- lateral `zombie-siege.html`: Another event guide to preserve cluster navigation and avoid isolation.
- downstream `alliance-recognition-cost.html`: Useful deeper follow-up for players who need progression or cost context after the schedule overview.
- downstream `heroes.html`: Supports hero-related planning that can influence event preparation.
- downstream `lucky-discounter.html`: Relevant for resource management and spending decisions tied to event planning.

## Protected Claims

- None

## Do Not Change

- Do not change the existing page template, navigation pattern, or schema family.
- Do not turn alliance-duel.html into an event hub or cluster index.
- Do not create a new page or split the topic into a different canonical page.
- Do not make analytics-based claims that the page must be rewritten.
- Do not alter canonical claims, site-wide routing, or approval gates.
- Do not write publishable copy, HTML, or patch specs in this planning brief.

## Owner Questions

- Is the existing Quick Answer wording enough to satisfy last z vs schedule intent, or should the first sentence be sharpened further?
- Do you want the Schedule or timing block to emphasize Day 1 to Day 6 order only, or also call out any timing caveats already present on the page?
- Should the Related Guides section keep the current sibling set, or should any links be reduced to preserve tighter cluster separation?

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

## Next Step

Run the no-write Editor and Reviewer stages from this approved decision snapshot, then confirm the opening answer and related links stay within the existing event-guide scope.
