# Content Brief: 2026-05-12-research-gsc-opportunity-llm-approved-intake

## Overview

- Summary: Worker-approved intake for `research.html` from `research-gsc-opportunity`.
- Status: `reviewed`
- Risk: `high`
- Cluster: `Research`
- Archetype: `cornerstone-guide`
- Target: `research.html`

## Page Goal

This run is meant to update_existing `research.html` inside the `Research` cluster.

## Source Context

- Topic ID: `research-gsc-opportunity-llm-approved-intake`
- Title: GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path
- Source type: `llm_scout`
- Source reference: LLM worker chain review: research-gsc-opportunity
- Confidence: `high`
- Priority: `high`

## First-Screen Guidance

- State the main answer near the top.
- Keep the page’s role distinct from neighboring pages in the same cluster.
- Use exact game terminology and preserve canonical claims.

## Canonical Claims To Respect

- `hero-training-cockpit-stop`: Hero Training is mainly valuable for Cockpit. Most players should stop at Cockpit instead of fully clearing the branch early.
- `peace-shield-value`: Peace Shield is a high-value survivability branch because of Urgent Rescue and its wider PvP value.
- `research-atlas-role`: research-costs.html is the atlas/hub for the research cost cluster. It should compare branches and route to exact tree pages, not replace them.
- `research-best-mainline`: The main research route for most players is Hero Training to Cockpit, then Military Strategies, then Peace Shield/Urgent Rescue. After that, players should choose by goal: use the shortest practical UST/T10 path for tier progression, or push Siege to Seize into Field Research only for late-game Recharge Shield/deep combat scaling.

## Related Pages To Consider

- research.html

## Suggested Page Skeleton

- Quick Answer
- Best overall recommendation
- Decision framework
- Links into narrower support pages
- FAQ / related guides

## SEO / Intent Notes

- Primary target page: `research.html`
- Archetype: `cornerstone-guide`
- Preserve title/H1/meta alignment with the page’s exact user intent.
- Strengthen internal routing inside the cluster rather than creating duplicate intent pages.

## Deterministic Checks To Run Later

- python3 scripts/prepublish_check.py
- python3 automation/pipeline.py checks --strict

## Reviewer Context

- Verdict: `needs_human_review`
- Next action: `review_human`

### Reviewer Notes

Deterministic review scaffold complete. The run should explicitly respect these canonical claims: hero-training-cockpit-stop, peace-shield-value, research-atlas-role, research-best-mainline.
