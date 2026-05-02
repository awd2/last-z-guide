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

### `workers/`

- `workers/README.md`
  - defines the contracts for future `Scout -> Editor -> Reviewer` LLM workers
  - keeps worker outputs structured and reviewable before any implementation work
  - protects templates, cluster roles, canonical claims, and human approval gates

- `workers/scout.py`
  - reads weekly GSC agent signals and site memory
  - writes no-change Scout topic proposals for human review
  - does not mutate backlog, manifests, or content

- `workers/editor.py`
  - reads one Scout topic proposal
  - writes a no-change Editor brief with context, links, protected claims, and checks
  - does not mutate backlog, manifests, or content

- `workers/reviewer.py`
  - reads one Editor brief and its Scout proposal
  - writes a no-change Worker review verdict with blockers, warnings, required context, and checks
  - does not mutate backlog, manifests, or content

- `workers/run_chain.py`
  - runs `Scout -> Editor -> Reviewer` for one selected topic proposal
  - writes a no-change chain summary artifact
  - does not mutate backlog, manifests, or content

- `workers/intake.py`
  - reads one Worker chain summary
  - writes a no-change intake gate artifact
  - keeps high-risk or human-review opportunities in `approval_required` until `--approved-by` is supplied
  - does not mutate backlog, manifests, or content

- `workers/intake_to_run.py`
  - reads one Worker intake artifact
  - writes a no-change run-plan proposal
  - only proposes a manifest when intake is `approved_for_intake`
  - does not mutate backlog, manifests, or content

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

The next worker milestone is contracts-first:

- `Scout` finds topic/update opportunities from GSC signals, backlog, and site memory.
- `Editor` turns approved opportunities into structured content briefs.
- `Reviewer` checks fit, risk, duplication, canonical claims, and required QA.

See `automation/workers/README.md` before adding or changing worker behavior.

## Archived experiments

`news-preview.html` and `content/news/*reddit-lastz-digest.md` are archived internal experiments from an abandoned Reddit/news digest test.

They are intentionally:

- `noindex`
- excluded from user-facing navigation
- outside editorial / LLM automation scope

Do not optimize, modernize, link, or regenerate them unless a task explicitly resumes the news experiment. `scripts/reddit_ingest.py` is disabled by default and requires `ENABLE_REDDIT_INGEST=1` to run intentionally.

## Basic commands

Recommended entrypoint:

```bash
python3 automation/pipeline.py list
python3 automation/pipeline.py list --json
python3 automation/pipeline.py backlog-summary
python3 automation/pipeline.py backlog-summary --json
python3 automation/pipeline.py backlog-sync
python3 automation/pipeline.py backlog-sync --json
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
python3 automation/pipeline.py apply-preview <run_id>
python3 automation/pipeline.py apply-approved <run_id>
python3 automation/pipeline.py close-run <run_id>
python3 automation/pipeline.py worker-chain --topic-id <topic_id>
python3 automation/pipeline.py worker-intake --topic-id <topic_id>
python3 automation/pipeline.py bundle-run <run_id>
python3 automation/pipeline.py run <topic_id>
python3 automation/pipeline.py bundle <topic_id>
python3 automation/pipeline.py show <run_id>
python3 automation/pipeline.py show <run_id> --json
python3 automation/workers/scout.py --json
python3 automation/workers/editor.py --topic-id <topic_id> --json
python3 automation/workers/reviewer.py --topic-id <topic_id> --json
python3 automation/workers/run_chain.py --topic-id <topic_id> --json
python3 automation/workers/intake.py --topic-id <topic_id> --json
python3 automation/workers/intake_to_run.py --topic-id <topic_id> --json
```

Example:

```bash
python3 automation/pipeline.py list --cluster Research --priority high
python3 automation/pipeline.py list --cluster Research --priority high --json
python3 automation/pipeline.py backlog-summary
python3 automation/pipeline.py backlog-summary --json
python3 automation/pipeline.py backlog-sync
python3 automation/pipeline.py backlog-sync --json
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
python3 automation/pipeline.py apply-preview 2026-04-22-research-cluster-nav
python3 automation/pipeline.py apply-approved 2026-04-22-research-cluster-nav
python3 automation/pipeline.py close-run 2026-04-22-research-cluster-nav --note "Human reviewed local page output."
python3 automation/pipeline.py worker-chain --topic-id codes-gsc-opportunity --json
python3 automation/pipeline.py worker-intake --topic-id codes-gsc-opportunity --json
python3 automation/pipeline.py bundle-run 2026-04-22-season-alias-clarification
python3 automation/pipeline.py bundle gift-center-ctr-pass
python3 automation/pipeline.py show 2026-04-22-gift-center-ctr-pass
python3 automation/pipeline.py show 2026-04-22-research-cluster-nav --json
python3 automation/workers/scout.py --json
python3 automation/workers/editor.py --topic-id codes-gsc-opportunity --json
python3 automation/workers/reviewer.py --topic-id codes-gsc-opportunity --json
python3 automation/workers/run_chain.py --topic-id codes-gsc-opportunity --json
python3 automation/workers/intake.py --topic-id codes-gsc-opportunity --json
python3 automation/workers/intake_to_run.py --topic-id codes-gsc-opportunity --json
```

Lifecycle shorthand:

- `plan` -> inspect the deterministic change plan
- `init-run` -> create a `planned` manifest only
- `review` -> take an existing `planned` manifest to `reviewed`
- `brief` -> create a brief-only editor artifact and move the run to `draft_brief_ready`
- `patch-plan` -> create a proposal-only patch artifact and move the run to `patch_plan_ready`
- `propose` -> render human-reviewable proposed edits and move the run to `proposal_ready`
- `approval` -> record human approval decisions for proposal specs; still does not edit site content
- `apply-preview` -> render a no-write preview from approved specs and move the run to `apply_preview_ready`
- `apply-approved` -> apply approved specs with conservative deterministic templates and move the run to `applied_pending_qa`
- `checks --strict --manifest <run_id>` -> record strict QA and move `applied_pending_qa` to `qa_passed` when all checks pass
- `close-run` -> close a `qa_passed` run with a final handoff artifact
- `worker-chain` -> run the no-write `Scout -> Editor -> Reviewer` chain for one topic proposal
- `worker-intake` -> generate a no-write human-gated intake artifact from a Worker chain summary
- `bundle-run` -> export a markdown review bundle from an existing run
- `run` -> create and review the manifest in one step
- `bundle` -> produce the reviewed manifest plus markdown review bundle in one step

Scout discovery:

- `python3 automation/workers/scout.py --json` -> generate reviewable topic proposals from `content/gsc/latest-gsc-agent-signals.json`
- output lives in `automation/reports/scout-topic-proposals.json` and `automation/reports/scout-topic-proposals.md`
- operators decide which proposals become backlog items; Scout does not update the backlog automatically

Editor brief generation:

- `python3 automation/workers/editor.py --topic-id <topic_id> --json` -> generate a no-write Editor brief from one Scout proposal
- output lives in `automation/reports/editor-brief-<topic_id>.json` and `automation/reports/editor-brief-<topic_id>.md`
- operators still approve any later patch plan or content apply step separately

Reviewer gate generation:

- `python3 automation/workers/reviewer.py --topic-id <topic_id> --json` -> generate a no-write Worker review from one Editor brief
- output lives in `automation/reports/worker-review-<topic_id>.json` and `automation/reports/worker-review-<topic_id>.md`
- `needs_human_review` is expected for high-risk cornerstone opportunities and does not mean the proposal failed

Worker chain:

- `python3 automation/pipeline.py worker-chain --topic-id <topic_id> --json` -> run `Scout -> Editor -> Reviewer` and generate a chain summary
- output lives in `automation/reports/worker-chain-<topic_id>.json` and `automation/reports/worker-chain-<topic_id>.md`
- this is the preferred no-write operator command for reviewing one analytics-backed opportunity end to end

Worker intake gate:

- `python3 automation/pipeline.py worker-intake --topic-id <topic_id> --json` -> generate a no-write intake artifact from one Worker chain summary
- output lives in `automation/reports/worker-intake-<topic_id>.json` and `automation/reports/worker-intake-<topic_id>.md`
- if human approval is required, intake remains `approval_required` until rerun with `--approved-by <name>`

Worker run-plan proposal:

- `python3 automation/workers/intake_to_run.py --topic-id <topic_id> --json` -> generate a no-write run-plan proposal from one Worker intake artifact
- output lives in `automation/reports/worker-run-plan-<topic_id>.json` and `automation/reports/worker-run-plan-<topic_id>.md`
- if intake is not `approved_for_intake`, the run-plan artifact is blocked and contains no `proposed_manifest`

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
- site structure consistency:
  - shared top navigation link order and active section
  - breadcrumb / related-grid / first-screen signal presence on guide pages
  - generated research branch output boundaries
- basic SEO/LLM alignment checks
- basic cannibalization warnings

`checks --strict` escalates weak-cluster and SEO/LLM warning-level findings into a failing gate. Site structure failures are always hard failures because they protect shared templates, navigation, and generated-source boundaries.

Render a template/component inventory report:

```bash
python3 automation/checks/template_inventory.py
python3 automation/checks/template_inventory.py --json
```

This report is informational. It inventories clusters, archetypes, article classes, nav state, footer/script patterns, first-screen signals, related-guide grids, schema families, and generated research branch boundaries.

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
- apply preview report
- apply result report
- closeout report

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
- `apply_preview_ready`
- `applied_pending_qa`
- `qa_passed`
- `closed`
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

Compare the backlog against active and closed run manifests:

```bash
python3 automation/pipeline.py backlog-sync
python3 automation/pipeline.py backlog-sync --json
```

`backlog-sync` is report-only. It does not edit `topic_backlog.csv`.
Use it before starting LLM/editorial work to avoid re-running closed topics or ignoring active runs.
It reports:

- topics with no run yet
- done topics with no run manifest
- topics with active runs
- backlog rows whose latest run is already closed
- run manifests that no longer map to a backlog topic

`backlog-sync --json` gives the same reconciliation snapshot in machine-readable form.

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
- `approved_for_apply` -> `apply-preview`
- `apply_preview_ready` -> `apply-approved`
- `applied_pending_qa` -> strict checks + prepublish checks
- `qa_passed` -> `close-run`
- `closed` -> manual release decision or next backlog topic
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
- approved/rejected plus at least one still proposed -> `partially_approved`
- approved/rejected with no proposed specs left and at least one approved -> `approved_for_apply`
- all rejected -> `rejected`

`approved_for_apply` is not an automatic publishing state. It only means a
future controlled apply step may use the approved specs as input. Rejected specs
stay recorded in the manifest, but apply-preview and apply-approved ignore them.

`apply-preview` renders a no-write preview from approved Patch Spec v1 entries:

```bash
python3 automation/pipeline.py apply-preview <run_id>
```

The output lives at:

- `automation/reports/<run_id>.apply-preview.md`

It does not edit site content. It records an `apply_preview` artifact in the
manifest and moves `approved_for_apply` runs to `apply_preview_ready`.

The preview is intentionally conservative:

- only `approval_state=approved` specs are included
- generated research branch edits are represented as JSON-source changes plus
  generator commands
- potential self-link or duplicate-link cases are called out as warnings
- it is a review artifact, not an apply engine

`apply-approved` applies approved specs with deterministic templates:

```bash
python3 automation/pipeline.py apply-approved <run_id>
```

The output lives at:

- `automation/reports/<run_id>.apply-result.md`

The command may edit site source files, but only for approved Patch Spec v1
entries. It is intentionally narrower than a general writing worker:

- HTML edits are limited to known safe metadata, first-screen, and related-link
  templates
- every apply route must map to a specialized deterministic handler or an
  explicitly allowlisted generic related-link route
- generated research branch pages are edited through their JSON source files
  and regenerated; generated related-guide targets are allowlisted instead of
  inferred from arbitrary specs
- duplicate related links and target-page self-links are skipped and recorded
- unsupported approved operations fail loudly instead of being silently skipped
  in the apply result artifact
- the manifest moves to `applied_pending_qa`
- production publishing is still manual and still requires green checks

When strict manifest checks pass after apply:

```bash
python3 automation/pipeline.py checks --strict --manifest <run_id>
```

the pipeline records `automation_checks_strict` and `changed_pages_report`.
If both pass and the run was `applied_pending_qa`, it advances the manifest to
`qa_passed`. This is still not a deployment state; it only means the local
automation gate is green.

`close-run` closes a QA-passed run after human review:

```bash
python3 automation/pipeline.py close-run <run_id> --note "Human reviewed local page output."
```

The output lives at:

- `automation/reports/<run_id>.closed.md`

The command only updates the manifest and report artifacts. It does not deploy.
Use it when the local automation lifecycle is complete and the remaining choice
is either manual release/deploy or moving to the next backlog topic.

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

## LLM Referral Report

Use the local helper when you export `llm_referral_session` rows from GA4:

```bash
python3 automation/reports/llm_referral_report.py path/to/ga4-llm-referrals.csv
```

Optional outputs:

```bash
python3 automation/reports/llm_referral_report.py path/to/ga4-llm-referrals.csv --output automation/reports/llm-referrals.md
python3 automation/reports/llm_referral_report.py path/to/ga4-llm-referrals.csv --json
```

Expected CSV dimensions include `llm_source`, `llm_channel`, `landing_page`, and `referrer_host`. Expected metrics include `sessions`, `event_count`, and `total_users`. The helper is intentionally offline and deterministic; it reads exported CSV only.

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
