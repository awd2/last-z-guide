# LLM Worker Chain - research-gsc-opportunity

## Outcome

- State: `completed`
- Provider: `openai`
- Target: `research.html`
- Page role: `cornerstone-guide`
- Review verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `none`
- Owner approval required: `true`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Stage Artifacts

- llm_scout: state `completed`, request `automation/reports/llm-worker-chain-scout-request.json`, result `automation/reports/llm-worker-chain-scout-result.json`, markdown `automation/reports/llm-worker-chain-scout.md`
- llm_editor: state `completed`, request `automation/reports/llm-worker-chain-editor-research-gsc-opportunity-request.json`, result `automation/reports/llm-worker-chain-editor-research-gsc-opportunity-result.json`, markdown `automation/reports/llm-worker-chain-editor-research-gsc-opportunity.md`
- llm_reviewer: state `completed`, request `automation/reports/llm-worker-chain-reviewer-research-gsc-opportunity-request.json`, result `automation/reports/llm-worker-chain-reviewer-research-gsc-opportunity-result.json`, markdown `automation/reports/llm-worker-chain-reviewer-research-gsc-opportunity.md`

## Editor Brief Summary

Refine the existing cornerstone research guide so the opening immediately answers research-order intent, while keeping the page in-role and preserving protected canonical claims. Emphasize a clear priority framework, then support it with a concise route through key nodes and related cluster pages.

## First-Screen Plan

Keep the answer-first structure, but tighten the opening so it explicitly resolves the priority question in plain terms. The first screen should identify the recommended early research sequence, note the practical reason for that sequence, and point to the key decision split between general progression, Peace Shield timing, and the T10 path. Avoid expanding into deep explanations before the user gets the actionable answer. Do not change the page into a different cluster role or dilute the canonical mainline framing.

## Reviewer Blocking Issues

- high: High-risk cornerstone page opportunity cannot be advanced automatically without explicit owner review. Required fix: Obtain Research owner validation before any user-visible content change is planned or approved.
- high: The brief identifies overlap risk with progression and economy guidance, which could blur cluster role separation if scoped too broadly. Required fix: Confirm the update remains strictly within research-order intent and does not re-home adjacent intents from tech, field research, or cost pages.
- medium: Protected canonical claims must be verified against exact current wording before any edit planning proceeds. Required fix: Review canonical claim references for hero-training-cockpit-stop, peace-shield-value, research-atlas-role, and research-best-mainline in the source canon files.

## Reviewer Warnings

- Analytics signals are suggestive but not proof of a rewrite need.
- The page should remain in-role as a cornerstone guide and not become a different page type.
- Template, navigation pattern, and schema family must remain unchanged.
- No public copy or patch details should be generated at this stage.

## Owner Questions

- Does the current opening answer the research-priority question in the first screen quickly enough for searchers?
- Should the priority framing lean more toward general progression, defense timing, or T10 progression for the intended audience?
- Are there any current FAQ items that should be elevated into the opening or decision framework instead?
- Is any internal link emphasis missing for the current cluster route block?
- Do any protected claims need exact wording verification before a content update is planned?

## Required Checks

- `python3 scripts/prepublish_check.py`
- `python3 automation/pipeline.py checks --strict`
- `manual review: first-screen answer and internal links on research.html`

## Next Step

Request Research owner review to confirm scope, then prepare a narrowly scoped update plan only if the opening can be improved without changing page role or protected claims.
