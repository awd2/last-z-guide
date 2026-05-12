# LLM Editor Brief - index-gsc-opportunity

## Overview

- State: `completed`
- Provider: `openai`
- Target: `index.html`
- Request: `automation/reports/llm-auto-review-queue/llm-auto-review-editor-index-gsc-opportunity-request.json`
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-editor-index-gsc-opportunity-result.json`
- Safety: no content, backlog, manifest, PR, or production files were modified.
- Scope: planning brief only; no final public page copy was generated.

## Brief Summary

Refine the home hub so the first screen answers the rising research-guide intent immediately, then routes users into the correct cluster page or related guide without changing the site structure or home-hub role.

## First-Screen Plan

Keep the hero and template intact, but make the opening more answer-first: state the immediate user action for research-guide seekers, then point them to the best next destination within the existing hub structure. The first screen should clarify that the homepage is a routing page, not a deep research article, and should surface the most relevant nearby guide path without adding cluster-specific depth.

## Section Plan

- First-screen site routing answer: Tighten the opening so it quickly answers what a research-guide visitor should do next and directs them to the most relevant page. Reason: The query signal suggests users want fast routing, not a full rewrite; this improves usability while preserving hub intent.
- Primary cluster cards: Reorder or emphasize the most relevant cluster cards so research and core progression paths are easier to find above the fold or near it. Reason: A home hub should surface the highest-value paths without taking on the content role of those destination pages.
- Featured exact-answer links: Ensure the featured links point to the most exact-answer destinations for common starting intents, especially research and adjacent progression topics. Reason: This strengthens query-to-destination matching while keeping the home page broad and navigational.
- Freshness and trust signals: Keep any existing freshness or credibility cues lightweight and hub-appropriate, avoiding new claims that would need verification or expand the page scope. Reason: The page should feel current and trustworthy without becoming a claim-heavy guide page.

## Internal Link Plan

- downstream `field-research.html`: Likely the most direct research destination for users who arrive on the hub with a research-guide intent.
- downstream `base-building-order.html`: Supports adjacent early progression intent without overlapping the hub's role.
- downstream `early-game-optimization.html`: Useful adjacent path for players who need a broader starting guide after the hub routes them.
- downstream `f2p.html`: Keeps the home hub useful for budget-conscious players while maintaining cluster separation.
- downstream `events.html`: Provides another common hub destination for users who need timing and progression context.

## Protected Claims

- None

## Do Not Change

- Do not change the existing page template, navigation pattern, or schema family without separate approval.
- Do not create a new page when the Scout proposal recommends updating an existing page.
- Do not blur hub versus cluster-page responsibilities.
- Do not add unsupported performance, ranking, or freshness claims.
- Do not treat analytics as proof that a rewrite is required.

## Owner Questions

- Should the first screen explicitly mention research routing, or should it stay broader to protect the home-hub role?
- Which downstream guide should be the primary first click for research-intent visitors: field-research.html or another canonical page?
- Is it acceptable to reorder featured cards, or should only copy and emphasis change within the existing layout?
- Are there any trust or freshness cues already approved for the home page that can be reused here?

## Required Context Before Patch

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`
- `index.html`

## Acceptance Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on index.html`

## Draft Exact Replacements

Proposal-only candidates. They do not approve copy, create Patch Specs, edit files, or bypass owner review.

- None

## Next Step

Request human review to confirm whether a limited homepage update can better surface research routing and related cluster links without weakening the home hub role.
