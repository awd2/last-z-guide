# Content Brief: 2026-04-22-research-cluster-nav

## Overview

- Summary: Update the existing page `research-costs.html` for the `Research` cluster using the `atlas-page` archetype.
- Status: `reviewed`
- Risk: `medium`
- Cluster: `Research`
- Archetype: `atlas-page`
- Target: `research-costs.html`

## Page Goal

This run is meant to update_existing `research-costs.html` inside the `Research` cluster.

## Source Context

- Topic ID: `research-cluster-nav`
- Title: Research cost cluster local navigation
- Source type: `product`
- Source reference: Known rollout next step from research atlas project
- Confidence: `high`
- Priority: `high`

## First-Screen Guidance

- State the main answer near the top.
- Keep the page’s role distinct from neighboring pages in the same cluster.
- Use exact game terminology and preserve canonical claims.
- Help users choose the correct detailed page instead of over-expanding the hub.

## Canonical Claims To Respect

- `alliance-recognition-utility-page`: Alliance Recognition is a proven utility page family: tree overview, exact costs, and planner-driven UX outperform generic explanation.
- `field-research-follows-siege`: Field Research follows 100% Siege to Seize and contains the final Recharge Shield path and major late badge pressure.
- `hero-training-cockpit-stop`: Hero Training is mainly valuable for Cockpit. Most players should stop at Cockpit instead of fully clearing the branch early.
- `peace-shield-value`: Peace Shield is a high-value survivability branch because of Urgent Rescue and its wider PvP value.
- `research-atlas-role`: research-costs.html is the atlas/hub for the research cost cluster. It should compare branches and route to exact tree pages, not replace them.
- `research-best-mainline`: The main research route for most players is Hero Training to Cockpit, then Military Strategies, then Peace Shield, then Siege to Seize, then Field Research.

## Related Pages To Consider

- alliance-recognition-cost.html
- army-building-cost.html
- field-research.html
- fully-armed-alliance-cost.html
- hero-training-cost.html
- military-strategies-cost.html
- research-costs.html

## Suggested Page Skeleton

- Quick Answer
- Cluster overview
- Comparison grid / card list
- Recommended route or progression path
- Links into exact pages

## SEO / Intent Notes

- Primary target page: `research-costs.html`
- Archetype: `atlas-page`
- Preserve title/H1/meta alignment with the page’s exact user intent.
- Strengthen internal routing inside the cluster rather than creating duplicate intent pages.

## Deterministic Checks To Run Later

- python3 automation/run_checks.py
- python3 scripts/generate_research_branch.py <data-file-if-applicable>
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py

## Reviewer Context

- Verdict: `needs_human_review`
- Next action: `review_human`

### Reviewer Notes

Deterministic review scaffold complete. The run should explicitly respect these canonical claims: alliance-recognition-utility-page, field-research-follows-siege, hero-training-cockpit-stop, peace-shield-value, research-atlas-role, research-best-mainline.
