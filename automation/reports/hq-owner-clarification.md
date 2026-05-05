# HQ Owner Clarification / Canonical Verification

Generated: 2026-05-05

## Scope

This is a no-write clarification pass for `hq-gsc-opportunity` after the LLM worker chain returned:

- Verdict: `needs_human_review`
- Risk: `high`
- Approved next stage: `none`
- Target: `hq.html`

No public content, patch specs, backlog rows, manifests, PRs, or production files were modified by this pass.

## Canonical Target Decision

`hq.html` should remain the canonical page for **HQ upgrade strategy**.

Rationale:

- `hq.html` owns the broad HQ query family in title, H1, meta, canonical URL, first-screen answer, FAQ, and structured data.
- `hq-construction-cost.html` owns the exact cost/table intent and links back to `hq.html`.
- `start.html` is a beginner/start guide. It mentions HQ as a beginner priority, but routes detailed HQ strategy to `hq.html`.
- `early-game-optimization.html` and `base-building-order.html` are support guides for early optimization and building order. They route HQ planning to `hq.html`.
- `shooter-stages.html` is not an HQ strategy page. It only mentions HQ as part of the broader progression loop.
- `index.html` routes users into both the Progression cluster and the dedicated HQ guide.

Recommended topic state:

- Keep `hq-gsc-opportunity` out of autonomous content intake.
- Do not advance to proposal/apply without owner approval.
- If the owner approves a public content proposal, keep the proposal tightly scoped to `hq.html` first-screen/factual cleanup and preserve the current template.

## Role Separation

Current role map:

- `hq.html`: canonical HQ upgrade strategy, HQ30/HQ35 path, steel phase, Sophia, requirements rule, Alliance Duel completion timing.
- `hq-construction-cost.html`: exact HQ cost/prerequisite table.
- `start.html`: beginner first steps and early mistake avoidance.
- `early-game-optimization.html`: first 3-7 day optimization, shooter stages, Lab/HQ requirement awareness.
- `base-building-order.html`: shelter building order and prerequisite cycle support page.
- `shooter-stages.html`: shooter stage mechanics and stage progression.

This role map is coherent. The main risk is not canonical ownership; the main risk is current `hq.html` factual/wording cleanup.

## Issues Found Before Any Public Edit

These are proposed content fixes only. They are not applied.

1. `hq.html` contains a clear typo or corrupted sentence:
   - Current: `Clubely costs anything`
   - Suggested direction: replace with a concrete early-phase cost statement, or remove the bullet.

2. `hq.html` mixes building terminology:
   - Current: `Assault Camp`
   - Site/table terminology: `Assaulter Camp`
   - Suggested direction: use `Assaulter Camp` consistently.

3. `hq.html` has speculative T11 language that is too strong for a public guide:
   - Current direction: `T11 units are likely coming`, `will require HQ35`, `prepare for T11`
   - Suggested direction: soften or remove unless owner has current source confirmation. If kept, mark it clearly as future-looking/server-dependent.

4. Steel source priority is inconsistent across pages:
   - `hq.html`: `Steel from orange bounties — best source by far`, and says steel is easy to collect with orange bounties.
   - `steel.html`: says best steel path is unlock HQ31-35, prioritize Tyrant rallies first, then orange bounties and steel nodes.
   - Suggested direction: align `hq.html` with `steel.html`: Tyrant rallies first, orange bounties as high-value/scaling source, steel nodes/mines/events as supporting sources.

5. `hq.html` says the requirement pattern continues to HQ35, but `hq-construction-cost.html` table shows HQ31-35 with only one prerequisite column filled.
   - Suggested direction: change `hq.html` wording to distinguish HQ8-30 Lab + second requirement from HQ31-35 later requirements shown in the table.

6. `hq.html` includes broad/absolute claims that should be owner-confirmed before any future edit:
   - `Yes, 100%` for upgrading past HQ30.
   - `Steel is NOT the problem`.
   - `some final upgrades take 6+ months EACH`.
   - `Sophia to 5 stars first`.
   - Suggested direction: keep strong recommendations only where they are grounded in the current table/page evidence or owner-approved gameplay knowledge.

## Recommended Next Step

Ask the owner to approve or reject a **small public content cleanup proposal** for `hq.html`.

If approved, the proposal should be limited to:

- fix the corrupted `Clubely costs anything` line
- normalize `Assaulter Camp`
- align steel source priority with `steel.html`
- soften or qualify T11 claims
- clarify HQ8-30 vs HQ31-35 prerequisite wording
- preserve the existing page template, schema family, navigation, and cluster role

Do not create a broader rewrite from the LLM chain output.
