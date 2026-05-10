# HQ / Tyrant / Steel Correction Closeout

Generated: 2026-05-10

## Scope Closed

This closeout covers the approved content-consistency hardening around:

- `hq.html`
- `steel.html`
- `tyrant.html`
- `resources.html`
- `gear.html`
- `pvp.html`
- `index.html`

## Completed Changes

### HQ guidance cleanup

Commit: `663ef23 fix: clean up HQ progression guidance`

Closed issues:

- removed unsupported Tyrant-as-main-Steel-source wording from `hq.html`
- clarified HQ8-30 requirement pattern versus HQ31-35 planning
- normalized `Assaulter Camp` terminology
- softened unconfirmed T11 requirement claims
- made HQ31-35 timer language less absolute
- softened Sophia guidance while keeping the early-build recommendation
- synchronized visible FAQ and JSON-LD FAQ text
- updated `sitemap.xml` through prepublish sync

### Tyrant / Steel sitewide correction

Commit: `b59f27f fix: correct Tyrant and steel guidance`

Closed issues:

- removed Tyrant from confirmed Steel-source guidance across public pages
- repositioned `tyrant.html` as an alliance rally / damage-tier / Power Core rewards guide
- repositioned `steel.html` around confirmed or safer Steel sources:
  - orange bounties
  - Steel Mine
  - steel nodes
  - Hub Shop
  - Furylord
  - seasonal rewards
  - HQ31-35 launch-event rewards
- corrected home card routing so Tyrant and Steel keep distinct page roles
- synchronized structured data, search index, and sitemap through prepublish sync

## Research Basis

Owner in-game check:

- Tyrant does not award Steel.

External cross-check:

- `last-z.wiki/events/the-tyrant/` lists Tyrant rewards such as Enhancement Alloy, speedups, Hero Exp, Zent, Food, Wood, Electricity, Gift Vouchers, Diamonds, Power Cores, and related reward tiers; it does not list Steel in the visible Tyrant reward tables.
- `ztools.co.uk/wiki/` positions Tyrant as an event/reward topic, not as the canonical Steel source.
- `lastz.info/the-tyrant-basics/` explains Tyrant timing, offline engagement, and rally behavior, but does not identify Tyrant as a Steel source.

Working rule now used by the site:

- do not describe Tyrant as a confirmed Steel source
- use Tyrant for alliance reward / damage-tier / Power Core guidance
- use the Steel guide for confirmed Steel planning

## Verification

Checks run after the approved public-content edits:

```bash
python3 scripts/prepublish_check.py --fix
python3 scripts/prepublish_check.py
python3 automation/pipeline.py checks --strict
git diff --check
```

Result:

- prepublish check passed
- strict automation checks passed
- SEO/LLM alignment passed
- content consistency passed
- search-index and sitemap were rebuilt and committed
- worktree was clean after commit/push

Additional text scan:

```bash
rg -n "Steel Rewards|steel rewards|Steel from Tyrant|Tyrant is #1 source|Tyrant is the primary way to farm|main weekly steel|single biggest repeatable steel|provides Steel|free Steel|Gives ~500\\+ Steel|Tyrant rallies are the main steel|Tyrant rallies first" *.html search-index.json -S
```

Result:

- no remaining Tyrant-as-Steel-source claims found
- remaining `steel rewards` matches are the HQ31-35 launch-event context in `hq.html`, not Tyrant

## Residual Risks

- Live game rewards can change by server stage or future update. If Tyrant later shows Steel in the live reward screen, this correction should be revisited with a server-stage clarification rather than silently reverting to a broad Tyrant = Steel claim.
- Some third-party SEO pages still claim Tyrant gives Steel. The site now intentionally follows owner in-game validation and more specific reward references instead.
- The exact values for Steel income from bounties, nodes, shops, Furylord, and launch events still need ongoing player validation as servers mature.

## Current State

This block is complete.

The public site is now safer for players on the Tyrant / Steel issue:

- `hq.html` no longer misleads players into planning Steel around Tyrant
- `steel.html` is the canonical Steel planning page
- `tyrant.html` is the canonical Tyrant execution / reward coordination page
- surrounding pages no longer reinforce the incorrect Tyrant-to-Steel claim

## Recommended Next Step

Return to LLM worker infrastructure.

Next implementation step:

- continue the LLM worker MVP by hardening the OpenAI-backed worker chain around the current proposal-first model
- keep all future public content outputs behind:
  - proposal artifact
  - owner approval
  - deterministic checks
  - content consistency scan
  - no autonomous publishing

