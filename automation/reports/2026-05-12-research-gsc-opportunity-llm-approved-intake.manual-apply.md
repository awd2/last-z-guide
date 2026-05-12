# Manual Apply Result: 2026-05-12-research-gsc-opportunity-llm-approved-intake

## Overview

- Target: `research.html`
- Apply mode: `manual_exact_proposal_apply`
- Source proposal: `automation/reports/2026-05-12-research-gsc-opportunity-llm-approved-intake.exact-proposal.md`
- Owner approval: approved in chat before apply
- Status after apply: `applied_pending_qa`

## Applied Scope

- `research.html`
- `scripts/sync_verification_blocks.py`
- `search-index.json`
- `sitemap.xml`
- `automation/manifests/2026-05-12-research-gsc-opportunity-llm-approved-intake.json`

## Applied Operations

- `research.html:title_meta_social_schema`
- `research.html:first_screen_research_route`
- `research.html:howto_steps_4_5`
- `research.html:visible_step_4_goal_split`
- `research.html:visible_faq_best_order`
- `research.html:verification_note`
- `scripts/sync_verification_blocks.py:research_guide_block`
- `search-index.json:research_description_sync`
- `sitemap.xml:research_lastmod_sync`
- `manifest:strict_check_result`

## Generator / Sync Commands

- `python3 scripts/prepublish_check.py --fix`

## Checks Run

- `python3 scripts/prepublish_check.py --fix`
- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks`
- `python3 automation/pipeline.py checks --strict --manifest 2026-05-12-research-gsc-opportunity-llm-approved-intake`

## Result

All checks passed after apply. The content now clarifies that Field Research is a late combat-scaling / Recharge Shield route, not a required stop before UST/T10.
