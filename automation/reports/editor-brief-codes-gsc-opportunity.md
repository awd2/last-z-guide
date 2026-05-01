# Editor Brief - codes-gsc-opportunity

## Overview

- Run ID: `2026-05-01-codes-gsc-opportunity`
- Target: `codes.html`
- Page role: `cornerstone-guide`
- Template reference: `codes.html`
- Primary query family: last z gift center
- Primary user job: Improve query-to-page match and first-screen usefulness for `last z gift center` searchers.
- Safety: no content, backlog, or manifest files were modified by Editor.

## First-Screen Answer

Preserve the existing answer-first shape, but make the opening answer clearly satisfy `last z gift center` without changing `codes.html` into a different page role.

## Required Sections

- Quick Answer
- Best overall recommendation
- Decision framework
- Cluster route block
- Related guides / FAQ

## Internal Links

- Upstream: index.html
- Downstream: diamond-reserve.html, events.html, f2p.html, lucky-discounter.html, start.html
- Lateral: gift-center-uid.html, redeem-code-not-working.html, resources.html

## Protected Claims

- `gift-center-cluster-role-separation`
- `gift-center-only-redeem-flow`
- `gift-rewards-mailbox`

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

## Source Evidence

- GSC page signal: codes.html had 14781 impressions, 254 clicks, 1.72% CTR, avg position 6.55.
- Low CTR query: `last z gift center` had 1548 impressions, 51 clicks, 3.29% CTR, position 7.25.
- Low CTR query: `last z gift center login` had 511 impressions, 13 clicks, 2.54% CTR, position 6.04.
- Low CTR query: `last-z.com gift center` had 276 impressions, 13 clicks, 4.71% CTR, position 6.25.
- Rising query: `last z gift center` gained 350 impressions in the last 7-day comparison window.
- Rising query: `last z gift center login` gained 66 impressions in the last 7-day comparison window.
- Rising query: `last-z.com gift center` gained 46 impressions in the last 7-day comparison window.

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

## Acceptance Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on codes.html`
