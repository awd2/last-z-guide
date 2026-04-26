# Automation Layer

This directory contains the foundation for a controlled editorial automation system for `lastzguides.com`.

The goal is **not** to create an autonomous publishing swarm. The goal is to build a safe editorial machine:

- explicit site memory
- structured backlog
- deterministic checks
- draft-first automation
- manual approval before production

This file is the detailed operator reference for the automation layer.
Root `README.md` should stay shorter and only point here, rather than mirror this command surface in full.

## Current structure

### `memory/`

Hand-curated or generated reference files used by future Scout / Editor / Reviewer flows.

- `content_index.json`
  - the canonical page inventory for the site
  - tracks page cluster, archetype, status, and freshness priority

- `content_index.current.json`
  - an auto-derived snapshot of the current repo inventory
  - safe to regenerate
  - used to compare the real repo state against hand-curated memory

- `page_archetypes.md`
  - defines the page families used across the site
  - helps the system choose the right output shape before drafting

- `site_style_guide.md`
  - canonical editorial tone and page-structure rules
  - documents first-screen rules, linking expectations, and forbidden patterns

- `release_checklist.md`
  - the minimum editorial + QA gate before a change should be considered merge-ready

- `canonical_claims.json`
  - the highest-priority truths the site should protect from contradiction
  - especially useful for season naming, research path, and Gift Center logic

- `entities.json`
  - shared registry of core game entities and aliases
  - keeps terminology stable across planning, writing, and review

- `topic_backlog.csv`
  - intake backlog for candidate topics, updates, and known opportunities
  - should become the working input for the future Scout / Planner layer

### scripts

- `build_content_index.py`
  - compares the current repo inventory against `memory/content_index.json`
  - can also write `memory/content_index.current.json`

- `run_checks.py`
  - runs the deterministic automation-layer checks as one bundle

- `planner.py`
  - builds a deterministic change plan from one backlog item

- `orchestrator.py`
  - creates an initial run manifest from one backlog item

- `reviewer.py`
  - adds a deterministic review scaffold to a run manifest

- `export_review_bundle.py`
  - exports a markdown review bundle from a reviewed manifest

- `demo_run.py`
  - runs the minimal orchestrator + reviewer MVP flow for one topic

- `demo_review_bundle.py`
  - one-command flow that creates a reviewed manifest and a markdown review bundle

## Current operating model

Right now this layer is **foundation only**.

It does not:
- publish changes
- create PRs
- run autonomous edits

It does:
- store site memory explicitly
- keep content inventory auditable
- create a structured backlog for future automation

## Basic commands

Recommended entrypoint:

```bash
python3 automation/pipeline.py list
python3 automation/pipeline.py list --json
python3 automation/pipeline.py backlog-summary
python3 automation/pipeline.py backlog-summary --json
python3 automation/pipeline.py open-topic <topic_id>
python3 automation/pipeline.py open-topic <topic_id> --json
python3 automation/pipeline.py open-run <run_id>
python3 automation/pipeline.py open-run <run_id> --json
python3 automation/pipeline.py next-step <run_id>
python3 automation/pipeline.py next-step <run_id> --json
python3 automation/pipeline.py recent-runs
python3 automation/pipeline.py recent-runs --status <status>
python3 automation/pipeline.py recent-runs --json
python3 automation/pipeline.py health
python3 automation/pipeline.py health --json
python3 automation/pipeline.py status
python3 automation/pipeline.py status --json
python3 automation/pipeline.py checks
python3 automation/pipeline.py checks --strict
python3 automation/pipeline.py checks --manifest <run_id>
python3 automation/pipeline.py plan <topic_id>
python3 automation/pipeline.py init-run <topic_id>
python3 automation/pipeline.py review <run_id>
python3 automation/pipeline.py brief <run_id>
python3 automation/pipeline.py patch-plan <run_id>
python3 automation/pipeline.py propose <run_id>
python3 automation/pipeline.py approval <run_id> --state approved --all
python3 automation/pipeline.py bundle-run <run_id>
python3 automation/pipeline.py run <topic_id>
python3 automation/pipeline.py bundle <topic_id>
python3 automation/pipeline.py show <run_id>
python3 automation/pipeline.py show <run_id> --json
```

Example:

```bash
python3 automation/pipeline.py list --cluster Research --priority high
python3 automation/pipeline.py list --cluster Research --priority high --json
python3 automation/pipeline.py backlog-summary
python3 automation/pipeline.py backlog-summary --json
python3 automation/pipeline.py open-topic gift-center-ctr-pass
python3 automation/pipeline.py open-topic gift-center-ctr-pass --json
python3 automation/pipeline.py open-run 2026-04-22-research-cluster-nav
python3 automation/pipeline.py open-run 2026-04-22-research-cluster-nav --json
python3 automation/pipeline.py next-step 2026-04-22-research-cluster-nav
python3 automation/pipeline.py next-step 2026-04-22-research-cluster-nav --json
python3 automation/pipeline.py recent-runs --limit 5
python3 automation/pipeline.py recent-runs --status patch_plan_ready
python3 automation/pipeline.py recent-runs --json
python3 automation/pipeline.py health
python3 automation/pipeline.py health --json
python3 automation/pipeline.py status
python3 automation/pipeline.py checks --strict
python3 automation/pipeline.py checks --manifest 2026-04-22-research-cluster-nav
python3 automation/pipeline.py init-run season-alias-clarification
python3 automation/pipeline.py review 2026-04-22-season-alias-clarification
python3 automation/pipeline.py brief 2026-04-22-season-alias-clarification
python3 automation/pipeline.py patch-plan 2026-04-22-research-cluster-nav
python3 automation/pipeline.py propose 2026-04-22-research-cluster-nav
python3 automation/pipeline.py approval 2026-04-22-research-cluster-nav --state approved --all --dry-run
python3 automation/pipeline.py bundle-run 2026-04-22-season-alias-clarification
python3 automation/pipeline.py bundle gift-center-ctr-pass
python3 automation/pipeline.py show 2026-04-22-gift-center-ctr-pass
python3 automation/pipeline.py show 2026-04-22-research-cluster-nav --json
```

Lifecycle shorthand:

- `plan` -> inspect the deterministic change plan
- `init-run` -> create a `planned` manifest only
- `review` -> take an existing `planned` manifest to `reviewed`
- `brief` -> create a brief-only editor artifact and move the run to `draft_brief_ready`
- `patch-plan` -> create a proposal-only patch artifact and move the run to `patch_plan_ready`
- `propose` -> render human-reviewable proposed edits and move the run to `proposal_ready`
- `approval` -> record human approval decisions for proposal specs; still does not edit site content
- `bundle-run` -> export a markdown review bundle from an existing run
- `run` -> create and review the manifest in one step
- `bundle` -> produce the reviewed manifest plus markdown review bundle in one step

Lower-level helpers are still available when needed.

Check memory coverage against the repo:

```bash
python3 automation/build_content_index.py
```

Write a fresh current inventory snapshot:

```bash
python3 automation/build_content_index.py --write-current
```

Run deterministic automation-layer checks:

```bash
python3 automation/pipeline.py checks
```

Run stricter PR-grade automation checks:

```bash
python3 automation/pipeline.py checks --strict
```

Record automation check results into a run manifest:

```bash
python3 automation/pipeline.py checks --manifest <run_id>
```

This records:

- `automation_checks` or `automation_checks_strict`
- `changed_pages_report`

The manifest is the durable run record; check outcomes should not live only in
terminal logs.

`checks` now includes:

- content index memory sync
- orphan / weak-cluster coverage
- cluster-link expectations
- basic SEO/LLM alignment checks
- basic cannibalization warnings

`checks --strict` escalates weak-cluster and SEO/LLM warning-level findings into a failing gate.

Show a compact health summary for the automation layer:

```bash
python3 automation/pipeline.py health
python3 automation/pipeline.py status
```

`health` and `status` include:
- memory coverage counts
- backlog count
- backlog breakdown by cluster / priority / status
- total run manifests
- manifest status breakdown
- `draft_brief_ready` run count
- baseline vs strict check status

Both commands also support `--json` for machine-readable output in future CI or draft workflows.

Create a reviewed manifest and markdown bundle for one backlog topic:

```bash
python3 automation/pipeline.py bundle <topic_id>
```

Show a compact summary for one reviewed run:

```bash
python3 automation/pipeline.py show <run_id>
python3 automation/pipeline.py show <run_id> --json
```

`show` includes links to generated review artifacts when they exist:
- changed files count
- markdown review bundle
- editor brief
- patch plan
- proposed edits report

`show --json` gives the same compact run summary in machine-readable form.

List the most recent run manifests with compact status info:

```bash
python3 automation/pipeline.py recent-runs
python3 automation/pipeline.py recent-runs --limit 5
```

`recent-runs` shows whether each recent run already has:
- changed files count
- markdown review bundle
- editor brief
- patch plan

You can filter `recent-runs` by lifecycle status, for example:
- `reviewed`
- `draft_brief_ready`
- `patch_plan_ready`
- `proposal_ready`
- `partially_approved`
- `approved_for_apply`
- `rejected`

`recent-runs` also supports `--json` for machine-readable recent run feeds.

Show one backlog topic in a review-friendly form:

```bash
python3 automation/pipeline.py open-topic <topic_id>
python3 automation/pipeline.py open-topic <topic_id> --json
```

`open-topic` includes:
- cluster
- recommended action
- archetype suggestion
- target page or slug
- source context
- confidence / priority / status
- notes

`open-topic --json` gives the same backlog item in machine-readable form.

`list --json` gives the backlog listing in machine-readable form.

Show an aggregate backlog view:

```bash
python3 automation/pipeline.py backlog-summary
python3 automation/pipeline.py backlog-summary --json
```

`backlog-summary` includes counts by:
- cluster
- priority
- status

`backlog-summary --json` gives the same intake snapshot in machine-readable form.

Show one run manifest in a detailed review-friendly form:

```bash
python3 automation/pipeline.py open-run <run_id>
python3 automation/pipeline.py open-run <run_id> --json
```

`open-run` includes:
- inputs
- plan
- review scaffold
- review context
- patch plan context
- candidate changed files
- artifact paths

`open-run --json` gives the same run as a deep machine-readable snapshot.

Show the expected next lifecycle action for one run:

```bash
python3 automation/pipeline.py next-step <run_id>
python3 automation/pipeline.py next-step <run_id> --json
```

`next-step` maps the current run status to the expected next action, for example:
- `planned` -> `review`
- `reviewed` -> `brief`
- `draft_brief_ready` -> `patch-plan`
- `patch_plan_ready` -> `propose`
- `proposal_ready` -> human review, then `approval`
- `partially_approved` -> review remaining proposal specs
- `approved_for_apply` -> manual apply or future safe apply worker
- `rejected` -> revise or close the run

`next-step --json` gives the same lifecycle hint in machine-readable form.
It now includes structured fields such as:
- `recommended_command`
- `requires_human_review`
- `requires_manual_edit_gate`

`patch-plan` also populates candidate `changed_files` in the run manifest as safe metadata for future PR/CI steps.
Patch plans include `Patch Spec v1` entries with:

- target file
- source-of-truth file
- generated-page status
- generator command when applicable
- required preconditions
- validation commands
- explicit human approval requirement

`propose` reads Patch Spec v1 entries and renders a human-reviewable proposed
edit report at:

- `automation/reports/<run_id>.proposed.md`

It does not edit site content. Generated research pages are still routed through
their JSON source files and generator commands in the report.

`approval` records human review decisions against rendered proposal specs:

```bash
python3 automation/pipeline.py approval <run_id> --state approved --all
python3 automation/pipeline.py approval <run_id> --state rejected --source research-costs.html --note "Needs a narrower scope."
python3 automation/pipeline.py approval <run_id> --state approved --all --dry-run
```

The command updates `approval_state` in both the proposal artifact and Patch
Spec v1 entries. It also refreshes the proposed edit report so the markdown
artifact stays aligned with the manifest.

Approval states:

- `proposed`
- `approved`
- `rejected`

Lifecycle status after approval:

- all proposed -> `proposal_ready`
- mixed decisions -> `partially_approved`
- all approved -> `approved_for_apply`
- all rejected -> `rejected`

`approved_for_apply` is not an automatic publishing state. It only means a
future controlled apply step may use the approved specs as input.

Run review as a separate lifecycle step:

```bash
python3 automation/pipeline.py review <run_id>
```

Create a brief-only editor artifact from an existing reviewed run:

```bash
python3 automation/pipeline.py brief <run_id>
```

Create a proposal-only patch plan from an existing draft brief run:

```bash
python3 automation/pipeline.py patch-plan <run_id>
```

Render proposed edits from an existing patch plan:

```bash
python3 automation/pipeline.py propose <run_id>
```

Export a markdown bundle for an existing run:

```bash
python3 automation/pipeline.py bundle-run <run_id>
```

Example:

```bash
python3 automation/pipeline.py bundle gift-center-ctr-pass
```

Outputs:
- `automation/manifests/<run_id>.json`
- `automation/reports/<run_id>.md`
- `automation/reports/<run_id>.brief.md`
- `automation/reports/<run_id>.patch.md`

## Intended next steps

The next pieces should be added in this order:

1. more deterministic QA helpers
   - changed-pages report
   - metadata coverage report
   - cluster health summaries

2. draft-first workflow expansion
   - topic selection helpers
   - richer plan outputs
   - reviewer heuristics

3. CI/CD wrappers
   - draft workflow
   - PR checks
   - keep manual approval before production

4. content-edit workers
   - only after the planning/review spine is stable
   - still no autonomous push to production

## Rule of thumb

If a change makes the system more autonomous but less auditable, do not add it yet.

The system should evolve from:

`explicit memory -> deterministic checks -> draft automation -> controlled release`

not the other way around.
