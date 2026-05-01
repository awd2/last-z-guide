# Worker Review - codes-gsc-opportunity

## Verdict

- Verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `patch_plan`
- Target: `codes.html`
- Human approval required: `true`
- Safety: no content, backlog, or manifest files were modified by Reviewer.

## Blocking Issues

- None

## Warnings

- Target is a cornerstone/home archetype; require explicit human approval before any patch plan or apply step.
- Scout marked this opportunity as high risk; analytics should guide review, not force a rewrite.
- Brief intentionally preserves the current first-screen pattern; patch planning should be narrow.

## Required Context Before Edit

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

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on codes.html`
