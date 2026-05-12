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

- `source_registry.json`
  - approved/proposed external sources for topic discovery and claim cross-validation
  - keeps competitor/reference sources owner-gated and prevents single-source public claims

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
  - records intake-only approval scope; it does not approve public content edits
  - does not mutate backlog, manifests, or content

- `workers/intake_to_run.py`
  - reads one Worker intake artifact
  - writes a no-change run-plan proposal
  - only proposes a manifest when intake is `approved_for_intake`
  - does not mutate backlog, manifests, or content

- `workers/llm_adapter.py`
  - validates structured future LLM request/response JSON
  - defaults to fail-closed `disabled` provider
  - supports offline `fixture` provider for deterministic tests
  - supports live `openai` provider through the OpenAI Responses API when `OPENAI_API_KEY` is set
  - uses `OPENAI_MODEL` when set and otherwise defaults to `gpt-5.4-mini`
  - does not mutate backlog, manifests, or content

- `workers/llm_scout.py`
  - builds deterministic Scout proposals from latest GSC/Bing agent signals
  - can also accept External Scout candidate proposal artifacts
  - sends a compact JSON-only Scout review request through `llm_adapter`
  - writes request/result/markdown artifacts for human review
  - does not mutate backlog, manifests, content, PRs, or production state

- `workers/llm_candidate_refresh.py`
  - runs the no-write LLM Scout review plus LLM topic discovery bridge in one command
  - can merge External Scout proposals with GSC/Bing proposals before LLM Scout review
  - writes a compact candidate refresh summary for owner review
  - does not record owner decisions, mutate backlog, manifests, content, PRs, or production state

- `workers/llm_topic_discovery.py`
  - reads one LLM Scout request/result pair
  - converts selected and monitored opportunities into backlog-shaped topic discovery proposals
  - writes no-write JSON/markdown artifacts for owner review
  - does not mutate `topic_backlog.csv`, manifests, content, PRs, or production state

- `workers/llm_topic_decision.py`
  - records the owner decision for one LLM topic discovery proposal
  - supports `approved_for_chain`, `monitor`, and `rejected`
  - writes no-write JSON/markdown artifacts for durable topic routing
  - does not mutate `topic_backlog.csv`, manifests, content, PRs, or production state

- `reports/llm_topic_decisions.py`
  - consolidates all LLM topic decision artifacts into one operator summary
  - shows which topics, if any, are currently allowed for the next no-write worker chain
  - does not mutate `topic_backlog.csv`, manifests, content, PRs, or production state

- `reports/llm_approved_handoffs.py`
  - prints only `approved_for_chain` decisions with ready deterministic `llm-worker-chain --from-decision ...` commands
  - does not mutate `topic_backlog.csv`, manifests, content, PRs, or production state

- `workers/llm_run_approved_handoffs.py`
  - runs pending `approved_for_chain` decisions through deterministic no-write worker-chain replay
  - skips decisions that already have a current completed chain summary unless explicitly told to rerun
  - does not run live Scout reranking, mutate backlog, create manifests, edit content, open PRs, or deploy

- `workers/llm_auto_review_queue.py`
  - runs candidate refresh, scores candidate topics, and auto-runs the top no-write Editor/Reviewer chains
  - can include External Scout proposals when passed through `--external-proposals`
  - writes one consolidated owner-review queue artifact
  - skips topics with existing completed chain summaries unless explicitly told to rerun
  - does not approve public copy, mutate backlog, create manifests, edit content, open PRs, or deploy

- `workers/external_scout.py`
  - reads `memory/source_registry.json`
  - emits no-write external topic candidates from approved source/topic seeds
  - records proposed sources that still need owner approval before scheduled discovery use
  - does not crawl broadly, copy competitor text, mutate backlog/manifests, edit content, open PRs, or deploy

- `workers/llm_editor.py`
  - reads one selected LLM Scout opportunity and deterministic Editor context
  - sends a JSON-only planning brief request through `llm_adapter`
  - writes request/result/markdown artifacts for human review
  - does not generate final public page copy, patch specs, backlog entries, manifests, content edits, PRs, or production state

- `workers/llm_reviewer.py`
  - reads one LLM Editor planning brief
  - sends a JSON-only review gate request through `llm_adapter`
  - writes request/result/markdown artifacts for human review
  - checks duplicate intent, cluster role fit, canonical claims, template safety, owner questions, and readiness without applying changes
  - does not generate final public page copy, patch specs, backlog entries, manifests, content edits, PRs, or production state

- `workers/llm_worker_chain.py`
  - runs the no-write live LLM Scout -> Editor -> Reviewer sequence through `llm_adapter`
  - writes one compact chain summary plus per-stage request/result/markdown artifacts
  - fails closed when any stage is blocked or invalid
  - does not generate final public page copy, patch specs, backlog entries, manifests, content edits, PRs, or production state

- `workers/llm_intake.py`
  - reads the latest or specified LLM worker-chain summary
  - writes a no-write LLM intake artifact for owner approval
  - stays in `approval_required` until `--approved-by` is supplied when owner review is required
  - does not edit content, backlog, manifests, PRs, or production state

- `.github/workflows/llm-worker-chain.yml`
  - runs pending owner-approved no-write worker-chain handoffs by manual dispatch or committed decision artifact push
  - uploads artifacts from `automation/reports/llm-worker-chain-gha/`
  - does not commit generated reports, edit content, open PRs, or deploy

- `.github/workflows/llm-auto-review-queue.yml`
  - runs the no-write auto-review queue daily, by manual dispatch, or after signal-file pushes
  - uploads artifacts from `automation/reports/llm-auto-review-queue/`
  - may commit only queue report artifacts
  - does not edit content, backlog, manifests, PRs, or production state

- `.github/workflows/llm-candidate-refresh.yml`
  - runs the no-write LLM candidate refresh by manual dispatch and weekly schedule after analytics report jobs
  - uploads artifacts from `automation/reports/llm-candidate-refresh-gha/`
  - does not commit generated reports, record owner decisions, edit content, open PRs, or deploy

- `checks/content_voice.py`
  - runs a no-write audit for generic, mass-produced, or low-utility writing signals
  - reports repeated trust boilerplate, generic phrases, long smooth paragraphs, and low specificity
  - does not edit content and is not part of the default strict gate until a human approves baseline policy changes

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
python3 automation/pipeline.py worker-run-plan --topic-id <topic_id>
python3 automation/pipeline.py worker-run-plan --intake <intake.json> --basename <basename> --json
python3 automation/pipeline.py worker-manifest --topic-id <topic_id> --created-by <name>
python3 automation/pipeline.py llm-adapter --request <request.json> --provider fixture --fixture <response.json>
python3 automation/pipeline.py external-scout --json
python3 automation/pipeline.py llm-scout --provider openai --json
python3 automation/pipeline.py llm-scout --external-proposals automation/reports/external-scout.json --provider openai --json
python3 automation/pipeline.py llm-candidate-refresh --provider openai --json
python3 automation/pipeline.py llm-candidate-refresh --external-proposals automation/reports/external-scout.json --provider openai --json
python3 automation/pipeline.py llm-auto-review-queue --provider openai --json
python3 automation/pipeline.py llm-auto-review-queue --external-proposals automation/reports/external-scout.json --provider openai --json
python3 automation/pipeline.py llm-topic-discovery --json
python3 automation/pipeline.py llm-topic-decision --topic-id <topic_id> --state monitor --decided-by <name> --json
python3 automation/pipeline.py llm-topic-decision --from-decision automation/reports/llm-topic-decision-<topic_id>.json --state approved_for_chain --decided-by <name> --note "<approval note>" --json
python3 automation/pipeline.py llm-topic-decisions --json
python3 automation/pipeline.py llm-approved-handoffs --json
python3 automation/pipeline.py llm-run-approved-handoffs --provider openai --json
python3 automation/pipeline.py llm-editor --topic-id <topic_id> --provider openai --json
python3 automation/pipeline.py llm-reviewer --topic-id <topic_id> --provider openai --json
python3 automation/pipeline.py llm-worker-chain --topic-id <topic_id> --provider openai --json
python3 automation/pipeline.py llm-worker-chain --from-decision automation/reports/llm-topic-decision-<topic_id>.json --provider openai --json
python3 automation/pipeline.py llm-review-latest --json
python3 automation/pipeline.py llm-intake-latest --json
python3 automation/pipeline.py llm-intake-latest --approved-by <name> --note "<owner answer / approval scope>" --json
python3 automation/pipeline.py content-seo-opportunities
python3 automation/pipeline.py bing-report
python3 automation/pipeline.py content-voice
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
python3 automation/workers/write_manifest.py --topic-id <topic_id> --created-by <name> --json
python3 automation/workers/llm_adapter.py --request <request.json> --provider fixture --fixture <response.json> --json
python3 automation/workers/external_scout.py --json
python3 automation/workers/llm_scout.py --provider openai --json
python3 automation/workers/llm_scout.py --external-proposals automation/reports/external-scout.json --provider openai --json
python3 automation/workers/llm_candidate_refresh.py --provider openai --json
python3 automation/workers/llm_topic_discovery.py --json
python3 automation/workers/llm_topic_decision.py --topic-id <topic_id> --state monitor --decided-by <name> --json
python3 automation/workers/llm_editor.py --topic-id <topic_id> --provider openai --json
python3 automation/workers/llm_reviewer.py --topic-id <topic_id> --provider openai --json
python3 automation/workers/llm_worker_chain.py --topic-id <topic_id> --provider openai --json
python3 automation/workers/llm_intake.py --approved-by <name> --note "<owner answer / approval scope>" --json
python3 automation/reports/llm_review_latest.py --json
python3 automation/reports/content_seo_opportunities.py --json
python3 -m unittest discover -s automation/tests -p 'test_*.py'
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
python3 automation/pipeline.py worker-run-plan --topic-id codes-gsc-opportunity --json
python3 automation/pipeline.py worker-run-plan --intake automation/reports/llm-intake-codes-gsc-opportunity.json --basename llm-worker-run-plan-codes-gsc-opportunity --json
python3 automation/pipeline.py worker-manifest --topic-id codes-gsc-opportunity --created-by oleg --dry-run --json
python3 automation/pipeline.py llm-adapter --request automation/reports/example-llm-request.json --provider fixture --fixture automation/reports/example-llm-response.json --json
python3 automation/pipeline.py llm-adapter --request automation/reports/example-llm-request.json --provider openai --json
python3 automation/pipeline.py llm-scout --provider openai --json
python3 automation/pipeline.py llm-candidate-refresh --provider openai --json
python3 automation/pipeline.py llm-editor --topic-id codes-gsc-opportunity --provider openai --json
python3 automation/pipeline.py llm-reviewer --topic-id codes-gsc-opportunity --provider openai --json
python3 automation/pipeline.py llm-worker-chain --topic-id codes-gsc-opportunity --provider openai --json
python3 automation/pipeline.py llm-review-latest --json
python3 automation/pipeline.py llm-intake-latest --json
python3 automation/pipeline.py llm-intake-latest --approved-by oleg --note "<owner answer / approval scope>" --json
python3 automation/pipeline.py content-seo-opportunities --json
python3 automation/pipeline.py bing-report
python3 automation/pipeline.py content-voice --json
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
python3 automation/workers/write_manifest.py --topic-id codes-gsc-opportunity --created-by oleg --dry-run --json
python3 -m unittest discover -s automation/tests -p 'test_*.py'
```

Lifecycle shorthand:

- `plan` -> inspect the deterministic change plan
- `init-run` -> create a `planned` manifest only
- `review` -> take an existing `planned` manifest to `reviewed`
- `brief` -> create a brief-only editor artifact and move the run to `draft_brief_ready`
- `patch-plan` -> create a proposal-only patch artifact and move the run to `patch_plan_ready`
- `propose` -> render human-reviewable proposed edits and move the run to `proposal_ready`
- `brief`, `patch-plan`, and `propose` also accept a manifest path plus `--output-dir <dir>` for staged Worker e2e checks outside `automation/reports`
- `approval` -> record human approval decisions for proposal specs; still does not edit site content
- `apply-preview` -> render a no-write preview from approved specs and move the run to `apply_preview_ready`
- `apply-approved` -> apply approved specs with conservative deterministic templates and move the run to `applied_pending_qa`
- `checks --strict --manifest <run_id>` -> record strict QA and move `applied_pending_qa` to `qa_passed` when all checks pass
- `close-run` -> close a `qa_passed` run with a final handoff artifact
- `worker-chain` -> run the no-write `Scout -> Editor -> Reviewer` chain for one topic proposal
- `worker-intake` -> generate a no-write human-gated intake artifact from a Worker chain summary
- `worker-run-plan` -> generate a no-write run-plan proposal from a Worker intake artifact
- `worker-manifest` -> create a `planned` manifest from an approved Worker run-plan proposal
- `llm-adapter` -> validate future LLM request/response contracts through a fail-closed provider adapter
- `external-scout` -> create no-write external source/topic proposal artifacts from the approved source registry
- `llm-scout` -> run a no-write LLM review over deterministic Scout proposals from GSC/Bing and optional External Scout signals
- `llm-candidate-refresh` -> run no-write LLM Scout plus topic discovery and write owner-review candidate artifacts
- `llm-auto-review-queue` -> score candidates and auto-run top no-write Editor/Reviewer chains into one queue
- `llm-topic-discovery` -> convert selected LLM Scout opportunities into no-write topic proposals
- `llm-topic-decision` -> record an owner decision for one discovered topic
- `llm-approved-handoffs` -> list owner-approved decisions ready for no-write chain replay
- `llm-run-approved-handoffs` -> run pending owner-approved decisions through no-write chain replay
- `llm-editor` -> run a no-write LLM planning brief from one selected LLM Scout opportunity
- `llm-reviewer` -> run a no-write LLM review gate from one LLM Editor planning brief
- `llm-worker-chain` -> run the no-write live LLM Scout -> Editor -> Reviewer sequence and write one owner-review summary
- `llm-review-latest` -> read the latest local LLM worker chain summary without calling an LLM provider
- `llm-intake-latest` -> bridge the latest LLM worker chain summary into a no-write, owner-gated intake artifact
- `content-seo-opportunities` -> build a no-write SEO/LLM opportunity report from GSC signals and page structure
- `bing-report` -> fetch Bing Webmaster weekly performance artifacts for humans and future agents
- `content-voice` -> run a no-write audit for generic, mass-produced, or low-utility public content signals
- `bundle-run` -> export a markdown review bundle from an existing run
- `run` -> create and review the manifest in one step
- `bundle` -> produce the reviewed manifest plus markdown review bundle in one step

Scout discovery:

- `python3 automation/workers/scout.py --json` -> generate reviewable topic proposals from `content/gsc/latest-gsc-agent-signals.json`
- `python3 automation/workers/scout.py --signals content/bing/latest-bing-agent-signals.json --basename scout-topic-proposals-bing --json` -> generate reviewable topic proposals from Bing signals
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

- `python3 automation/pipeline.py worker-run-plan --topic-id <topic_id> --json` -> generate a no-write run-plan proposal from one Worker intake artifact
- output lives in `automation/reports/worker-run-plan-<topic_id>.json` and `automation/reports/worker-run-plan-<topic_id>.md`
- if intake is not `approved_for_intake`, the run-plan artifact is blocked and contains no `proposed_manifest`
- if the approved intake includes `exact_replacements`, they are copied into
  `proposed_manifest.plan.exact_replacements` as proposal-only data for later
  Patch Spec rendering

Worker approved manifest writer:

- `python3 automation/pipeline.py worker-manifest --topic-id <topic_id> --created-by <name> --json` -> create a `planned` run manifest from one approved Worker run-plan proposal
- default output lives in `automation/manifests/<run_id>.json`
- the writer fails closed unless the run-plan state is `run_plan_ready`, the proposed manifest validates, and the target manifest does not already exist
- use `--dry-run` to validate without writing

Worker contract tests:

- `python3 -m unittest discover -s automation/tests -p 'test_*.py'` -> run deterministic fixture tests for Scout, Editor, Reviewer, intake, run-plan, manifest writer, and LLM adapter contracts
- tests use temporary directories for generated artifacts and must not write real site content or production manifests

LLM adapter:

- `python3 automation/pipeline.py llm-adapter --request <request.json> --provider fixture --fixture <response.json> --json` -> validate a future LLM request/response contract offline
- `python3 automation/pipeline.py llm-adapter --request <request.json> --provider openai --json` -> call the OpenAI Responses API and return a validated JSON artifact
- default provider is `disabled` and returns a blocked result
- `openai` requires `OPENAI_API_KEY`, uses `OPENAI_MODEL` when set, defaults to `gpt-5.4-mini`, and must remain no-write
- adapter output is structured, plain ASCII English, and must not directly edit content, backlog, manifests, or production state

LLM Scout review:

- `python3 automation/pipeline.py llm-scout --provider openai --json` -> review deterministic GSC/Bing Scout proposals with the live OpenAI provider
- `python3 automation/pipeline.py external-scout --json` -> create a no-write external source report from `automation/memory/source_registry.json`
- `python3 automation/pipeline.py llm-scout --external-proposals automation/reports/external-scout.json --provider openai --json` -> merge External Scout proposals into LLM Scout review
- default input uses `content/gsc/latest-gsc-agent-signals.json` and `content/bing/latest-bing-agent-signals.json` when present
- output lives in `automation/reports/llm-scout-review-request.json`, `automation/reports/llm-scout-review-result.json`, and `automation/reports/llm-scout-review.md`
- Scout must put `monitor` and `reject` decisions in `rejected_or_monitor`; selected opportunities are allowed to advance only when they are `update_existing`, `create_new`, or `consolidate` with non-low priority
- this is a no-write opportunity review; selected topics still require deterministic Editor/Reviewer steps and human approval before content work

LLM candidate refresh:

- `python3 automation/pipeline.py llm-candidate-refresh --provider openai --json` -> run LLM Scout plus topic discovery in one no-write command
- `python3 automation/pipeline.py llm-candidate-refresh --external-proposals automation/reports/external-scout.json --provider openai --json` -> include External Scout proposals in the candidate refresh
- default input uses `content/gsc/latest-gsc-agent-signals.json` and `content/bing/latest-bing-agent-signals.json` when present
- output lives in `automation/reports/llm-candidate-refresh.json`, `automation/reports/llm-candidate-refresh.md`, and the referenced Scout/discovery artifacts
- this is the scheduled candidate-generation layer: it prepares topics for owner review but does not approve them
- it must not edit content, mutate `topic_backlog.csv`, create manifests, record topic decisions, open PRs, or deploy

LLM auto review queue:

- `python3 automation/pipeline.py llm-auto-review-queue --provider openai --json` -> run candidate refresh, score candidates, and auto-review the top candidates through no-write Editor/Reviewer chains
- `python3 automation/pipeline.py llm-auto-review-queue --external-proposals automation/reports/external-scout.json --provider openai --json` -> include External Scout proposals in the consolidated queue
- default input uses `content/gsc/latest-gsc-agent-signals.json` and `content/bing/latest-bing-agent-signals.json` when present
- output lives in `automation/reports/llm-auto-review-queue/`
- this is the consolidated owner-review layer: it reduces manual step-by-step approval by presenting ready queue items
- it skips topics with existing completed chain summaries unless `--include-existing` is supplied
- it must not approve public copy, mutate `topic_backlog.csv`, create manifests, edit content, open PRs, or deploy

LLM topic discovery:

- `python3 automation/pipeline.py llm-topic-discovery --json` -> convert selected and monitored LLM Scout opportunities into backlog-shaped topic proposals for owner review
- default input uses `automation/reports/llm-scout-review-result.json` and `automation/reports/llm-scout-review-request.json`
- output lives in `automation/reports/llm-topic-discovery.json` and `automation/reports/llm-topic-discovery.md`
- this is a no-write bridge; it does not update `topic_backlog.csv`, manifests, content, PRs, or production state

LLM topic decision:

- `python3 automation/pipeline.py llm-topic-decision --topic-id <topic_id> --state monitor --decided-by <name> --json` -> record an owner decision for one discovered topic
- `python3 automation/pipeline.py llm-topic-decision --from-decision automation/reports/llm-topic-decision-<topic_id>.json --state approved_for_chain --decided-by <name> --note "<approval note>" --json` -> rerecord an existing saved decision without manual JSON edits
- `--state approved_for_chain` allows only the next no-write `llm-worker-chain` step
- `--state monitor` keeps the topic out of intake until materially new evidence appears
- `--state rejected` blocks the topic unless the owner explicitly reopens it
- output lives in `automation/reports/llm-topic-decision-<topic_id>.json` and `.md`
- `--from-decision` preserves the saved topic snapshot and records the prior state in `previous_decision`
- this is a no-write decision artifact; it does not update `topic_backlog.csv`, manifests, content, PRs, or production state

LLM topic decisions summary:

- `python3 automation/pipeline.py llm-topic-decisions --json` -> consolidate all `llm-topic-decision-*.json` artifacts
- output lives in `automation/reports/llm-topic-decisions.json` and `.md`
- this report is read-only over decision artifacts; it does not update `topic_backlog.csv`, manifests, content, PRs, or production state

LLM approved handoffs:

- `python3 automation/pipeline.py llm-approved-handoffs --json` -> list only decisions that are currently `approved_for_chain`
- prints ready deterministic `llm-worker-chain --from-decision ...` commands
- this view is read-only; it does not update `topic_backlog.csv`, manifests, content, PRs, or production state

LLM run approved handoffs:

- `python3 automation/pipeline.py llm-run-approved-handoffs --provider openai --json` -> run pending `approved_for_chain` decisions through no-write worker-chain replay
- each handoff uses the saved decision artifact, equivalent to `llm-worker-chain --from-decision ...`
- decisions with a current completed `llm-worker-chain-<topic_id>.json` summary are skipped by default
- use `--include-current` only when intentionally rerunning an already-current handoff
- output lives in `automation/reports/llm-approved-handoff-run/` by default, or the supplied `--output-dir`
- this command does not run live Scout reranking, approve public copy, mutate backlog/manifests, edit content, open PRs, or deploy

LLM Editor planning brief:

- `python3 automation/pipeline.py llm-editor --topic-id <topic_id> --provider openai --json` -> create a no-write planning brief from one selected LLM Scout opportunity
- default input uses `automation/reports/llm-scout-review-result.json` and `automation/reports/llm-scout-review-request.json`
- output lives in `automation/reports/llm-editor-brief-<topic_id>-request.json`, `automation/reports/llm-editor-brief-<topic_id>-result.json`, and `automation/reports/llm-editor-brief-<topic_id>.md`
- this must not generate final public page copy or patch specs; it only prepares planning context for deterministic Reviewer and later owner-approved proposals
- optional `exact_replacements` are draft proposal data only; every item must set `owner_approval_required: true` and still needs the later proposal/approval/apply lifecycle
- for safer exact proposals, the deterministic Editor context includes limited raw target-page snippets under `current_page_snapshot.source_snippets`; this covers common guide-page snippets and home-hub hero/header snippets; `exact_old` must be copied literally from current HTML and must match the target page exactly once or the LLM Editor result is blocked

LLM Reviewer gate:

- `python3 automation/pipeline.py llm-reviewer --topic-id <topic_id> --provider openai --json` -> review one LLM Editor planning brief for site fit and readiness
- default input uses `automation/reports/llm-editor-brief-<topic_id>-result.json` and `automation/reports/llm-editor-brief-<topic_id>-request.json`
- output lives in `automation/reports/llm-reviewer-gate-<topic_id>-request.json`, `automation/reports/llm-reviewer-gate-<topic_id>-result.json`, and `automation/reports/llm-reviewer-gate-<topic_id>.md`
- this is a gate artifact only; high-risk user-visible content changes still require owner approval and later proposal-only patch planning
- if Editor `exact_replacements` are present, Reviewer must review them and cannot advance them directly to `apply-preview`

LLM worker chain:

- `python3 automation/pipeline.py llm-worker-chain --topic-id <topic_id> --provider openai --json` -> run the no-write live LLM Scout -> Editor -> Reviewer sequence
- `python3 automation/pipeline.py llm-worker-chain --from-decision automation/reports/llm-topic-decision-<topic_id>.json --provider openai --json` -> replay one saved `approved_for_chain` decision as the deterministic chain handoff
- default input uses latest GSC/Bing agent signal files when present
- live Scout handoffs advance only `ready_for_chain` opportunities; monitor-only, reject, or low-priority selected topics stop before Editor/Reviewer
- output lives in `automation/reports/llm-worker-chain-<topic_id>.json` and `automation/reports/llm-worker-chain-<topic_id>.md`
- per-stage request/result/markdown artifacts are also written and referenced from the summary
- `--from-decision` skips live Scout rerank and blocks unless the decision artifact is `approved_for_chain`
- this is an owner-review summary only; it must not write content, backlog entries, manifests, PRs, or production state

LLM candidate refresh workflow:

- `.github/workflows/llm-candidate-refresh.yml` -> refresh candidate topic artifacts in GitHub Actions
- trigger modes: weekly schedule, manual dispatch, path-limited LLM worker infrastructure push, or committed `llm-topic-decision-*.json` push
- required secret: `OPENAI_API_KEY`
- optional manual input: `model`
- output is an uploaded workflow artifact named `llm-candidate-refresh-<run_number>`
- this workflow intentionally does not commit reports, record owner decisions, edit content, open PRs, or deploy

LLM auto review queue workflow:

- `.github/workflows/llm-auto-review-queue.yml` -> run the consolidated no-write queue in GitHub Actions
- trigger modes: daily schedule, manual dispatch, signal-file push, source-registry push, External Scout worker push, or path-limited LLM worker infrastructure push
- required secret: `OPENAI_API_KEY`
- optional manual inputs: `model`, `max_chains`, `include_existing`
- output is an uploaded workflow artifact named `llm-auto-review-queue-<run_number>`
- before queueing, the workflow runs `external-scout` into `automation/reports/llm-auto-review-queue/external-scout.json` and passes it through `--external-proposals`
- it may commit only `automation/reports/llm-auto-review-queue/` report artifacts
- this workflow intentionally does not edit content, backlog, manifests, PRs, or deploy

LLM worker chain workflow:

- `.github/workflows/llm-worker-chain.yml` -> run pending owner-approved no-write chain handoffs in GitHub Actions
- trigger modes: manual dispatch, path-limited LLM worker infrastructure push, or committed `llm-topic-decision-*.json` push
- required secret: `OPENAI_API_KEY`
- optional manual inputs: `decision_path`, `model`, `include_current`
- output is an uploaded workflow artifact named `llm-worker-chain-<run_number>`
- this workflow intentionally does not commit reports to `main`
- on decision-artifact pushes, it reads committed `llm-topic-decision-*.json` artifacts and runs only decisions approved for chain replay
- manual `decision_path` can replay one approved decision artifact directly

LLM latest owner review:

- `python3 automation/pipeline.py llm-review-latest` -> print the latest local LLM worker chain owner-review view
- `python3 automation/pipeline.py llm-review-latest --json` -> print the same view as JSON
- `--chain <path>` can read a specific `llm-worker-chain-<topic_id>.json`
- output includes target page, verdict, risk, blocking issues, warnings, owner questions, required checks, and next step
- this is read-only and does not call OpenAI or mutate files

LLM intake latest:

- `python3 automation/pipeline.py llm-intake-latest --json` -> write a no-change intake artifact from the latest local LLM worker chain summary
- `python3 automation/pipeline.py llm-intake-latest --chain <path> --approved-by <name> --note "<owner answer / approval scope>" --json` -> record intake-only owner approval for that artifact
- output lives in `automation/reports/llm-intake-<topic_id>.json` and `.md`
- if the LLM Reviewer left owner questions, `--note` is required before the intake can become `approved_for_intake`
- if the LLM Reviewer used `blocking_issues` for owner-confirmation items, add `--resolve-reviewer-blockers` only with `--approved-by` and `--note`; this downgrades them to intake warnings and still does not approve public copy
- approval is scoped to intake/run-plan only; it does not approve public copy, patch specs, backlog mutation, manifests, PRs, deployment, or production publishing
- draft `exact_replacements` can be carried into the intake artifact as proposal-only data, but they are not content approval
- approved intake can move into the existing run-plan proposal flow with `python3 automation/pipeline.py worker-run-plan --intake automation/reports/llm-intake-<topic_id>.json --basename llm-worker-run-plan-<topic_id> --json`
- this step still does not edit content, backlog, manifests, PRs, or production state
- after `worker-manifest`, staged e2e tests can keep artifacts outside the repo reports directory with `brief <manifest-path> --output-dir <dir>`, `patch-plan <manifest-path> --output-dir <dir>`, and `propose <manifest-path> --output-dir <dir>`

Content SEO opportunity report:

- `python3 automation/pipeline.py content-seo-opportunities --json` -> build a no-write page opportunity artifact from `content/gsc/latest-gsc-agent-signals.json`, `content_index.json`, page structure, and `sitemap.xml`
- output lives in `automation/reports/content-seo-opportunities.json` and `automation/reports/content-seo-opportunities.md`
- use it as planning context for future workers; it is not permission to edit high-risk pages or generated research HTML directly

Bing weekly report:

- `python3 automation/pipeline.py bing-report` -> fetch Bing Webmaster weekly query/page/page-query data
- GitHub workflow: `.github/workflows/bing-weekly.yml`
- required secrets: `BING_WEBMASTER_API_KEY`, `BING_SITE_URL`
- optional env knobs: `BING_ROWS`, `BING_PAIR_PAGES`
- output lives in `content/bing/latest-bing-report.md` and `content/bing/latest-bing-agent-signals.json`
- use Bing as an additional search signal; compare with GSC and site memory before proposing content changes

Content voice audit:

- `python3 automation/pipeline.py content-voice` -> audit public pages for generic or low-utility writing signals
- `python3 automation/pipeline.py content-voice --json` -> emit the full machine-readable audit
- `python3 automation/pipeline.py content-voice --top 20` -> show more opportunities in the human-readable output
- `python3 automation/pipeline.py content-voice --fail-on-high-risk` -> optionally return non-zero when high-risk findings exist
- this is a no-write planning audit; it is not automatic approval to rewrite public pages
- use findings to prepare exact before/after content proposals for human approval

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
- search visibility controls:
  - sitemap declaration in `robots.txt`
  - no accidental public-guide `noindex`, `nosnippet`, or `max-snippet:0`
  - no first-screen answer block hidden with `data-nosnippet`
- content consistency controls:
  - no unqualified old Season 2 Desert wording
  - no wrong Gift Center redemption flow
  - no stale `Special Unit Training` naming
  - no public exposure of archived Reddit/news experiments
  - no shield economy claim that prefers direct diamond shields over Alliance Shop shields when stock exists
  - owner-approved strong wording is reported as allowed context on explicitly approved pages
- basic SEO/LLM alignment checks
- basic cannibalization warnings

`checks --strict` escalates weak-cluster, content-consistency warning-level findings, and SEO/LLM warning-level findings into a failing gate. Site structure, search visibility, and content-consistency failures are always hard failures because they protect shared templates, navigation, generated-source boundaries, canonical player guidance, and AI/search snippet eligibility.

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
- `rejected` -> `close-run` if the rejected proposal needs no revision

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

When a proposed change already contains exact before/after strings, `patch-plan`
may emit a `safe_exact_replace` Patch Spec instead of a broad
`first_screen_update` or `meta_refresh` placeholder. This is allowed only when:

- `exact_old` and `exact_new` are present
- the source is a non-generated HTML file
- `target_file`, `source_of_truth_file`, and `output_file` all match
- the spec still requires owner approval before apply

Future Worker run-plan artifacts may pass exact snippets through
`plan.exact_replacements`:

```json
{
  "file": "example.html",
  "change_type": "first_screen_update",
  "selector_or_anchor": ".guide-verified",
  "exact_old": "<p>Old approved-before text.</p>",
  "exact_new": "<p>New owner-approved text.</p>"
}
```

This is still no-write proposal data. It only becomes applyable after
`propose`, explicit owner `approval`, `apply-preview`, and `apply-approved`.
When these snippets originate from LLM Editor, `exact_old` is validated against
the current target HTML before the chain can continue.

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
If all specs are rejected because the proposal is a reviewed no-op or should not
move forward, use `close-run` to produce a final no-content-change handoff.

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
- `safe_exact_replace` is the only generic content-side operation. It requires
  exact owner-approved `exact_old` and `exact_new` strings, only supports
  non-generated HTML files, requires the old string to appear exactly once, and
  fails closed instead of guessing when the source has drifted.
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

Minimal `safe_exact_replace` Patch Spec shape:

```json
{
  "target_file": "example.html",
  "source_of_truth_file": "example.html",
  "output_file": "example.html",
  "source_type": "html_file",
  "is_generated": false,
  "operation_type": "safe_exact_replace",
  "selector_or_anchor": "<title>",
  "approval_state": "approved",
  "exact_old": "<title>Old approved-before text</title>",
  "exact_new": "<title>New owner-approved text</title>"
}
```

This operation is for mechanically applying reviewed text. It is not an LLM
writing step and must not be used with paraphrased summaries or desired-after
notes.

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

It can also close a fully rejected proposal run when no content change should be
applied:

```bash
python3 automation/pipeline.py close-run <run_id> --note "Proposal reviewed; no content change needed."
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
