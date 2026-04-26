# Apply Result: 2026-04-22-research-cluster-nav

## Overview

- Summary: Update the existing page `research-costs.html` for the `Research` cluster using the `atlas-page` archetype.
- Applied at: `2026-04-26T10:27:56Z`
- Applied operations: 17
- Generator commands: 3
- Status after apply: `applied_pending_qa`

## Safety Rule

- Only approved Patch Spec v1 entries were considered.
- Generated research pages were changed through JSON source files and regenerated.
- This is still not a production publish step.

## Applied Operations

- research-costs:title
- research-costs:meta_description
- research-costs:og_title
- research-costs:og_description
- research-costs:twitter_title
- research-costs:twitter_description
- research-costs:article_headline
- research-costs:article_description
- research-costs:h1
- research-costs:guide_verified
- research-costs:data_lede
- research-costs:qa_lede
- research-costs:atlas_link_copy:9
- alliance-recognition-cost.html:related_card
- data/research_branches/army-building.json:related_guides
- data/research_branches/field-research.json:related_guides
- data/research_branches/fully-armed-alliance.json:related_guides

## Generator Commands

- python3 scripts/generate_research_branch.py data/research_branches/army-building.json
- python3 scripts/generate_research_branch.py data/research_branches/field-research.json
- python3 scripts/generate_research_branch.py data/research_branches/fully-armed-alliance.json
