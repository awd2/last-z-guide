# AGENTS.md

Project-level instructions for `lastzguides.com`.

This repo is a static guide site for **Last Z: Survival Shooter**. Treat this file as the default operating manual for any future content, SEO, UX, or automation task in this repository.

## Instruction Hierarchy

These instructions are meant to guide both:

- agent-like automated workflows
- normal chat-based requests in this repo

They apply by default whenever work happens inside this project.

Priority order is:

1. platform/system instructions
2. developer instructions
3. task-specific user request
4. this file: `AGENTS.md`
5. repo source-of-truth files and local file details discovered during the task

Implications:

- global platform instructions are always higher than this file
- developer instructions are always higher than this file
- this file is the main **repo-level default** for both agents and ordinary chat requests in this repository
- user requests should be followed unless they conflict with higher-level instructions
- this file should shape default behavior, but it should not override explicit higher-level instructions
- when repo source-of-truth files disagree with old assumptions or stale memory, the repo source-of-truth wins

## Mission

Optimize for:

- exact, useful answers
- strong internal knowledge graph
- high-consistency page roles
- safe, reviewable changes
- people-first SEO and LLM-friendly structure
- clear query-to-page match
- citation-friendly first-screen answers

Do **not** optimize for:

- generic gaming-blog prose
- keyword stuffing
- thin pages
- duplicate intent pages
- uncontrolled autonomous publishing

## Authority Map

Use these files as explicit authorities for different concerns:

- `AGENTS.md`
  - instruction hierarchy
  - file-reading flow
  - repo-level operating defaults
- `automation/memory/site_style_guide.md`
  - tone
  - writing shape
  - first-screen expectations
- `automation/memory/seo_llm_optimization.md`
  - query strategy
  - title / H1 / meta rules
  - cluster routing for search and answer engines
  - cannibalization and citation-fit rules
- `automation/memory/page_archetypes.md`
  - page-type selection
  - URL creation decision ladder
  - archetype-specific expectations
- `automation/memory/canonical_claims.json`
  - protected truths that must not be contradicted
- `automation/memory/content_index.json`
  - current page inventory
  - cluster membership
  - archetype map
- `automation/memory/entities.json`
  - canonical entity names and aliases
- `automation/memory/source_registry.json`
  - approved/proposed external sources for topic discovery and claim cross-validation
- `automation/memory/release_checklist.md`
  - merge/readiness gate
- `automation/README.md`
  - automation operator reference
- `automation/workers/README.md`
  - future `Scout -> Editor -> Reviewer` worker contracts
  - structured worker outputs and human-gate rules

## Required Context Before Any Content Edit

### Always-load core

For most non-trivial content, SEO, UX, or architecture tasks, load these first:

1. [automation/memory/site_style_guide.md](/Users/oleg/Projects/claude-playground/automation/memory/site_style_guide.md)
2. [automation/memory/page_archetypes.md](/Users/oleg/Projects/claude-playground/automation/memory/page_archetypes.md)
3. [automation/memory/seo_llm_optimization.md](/Users/oleg/Projects/claude-playground/automation/memory/seo_llm_optimization.md)
4. [automation/memory/canonical_claims.json](/Users/oleg/Projects/claude-playground/automation/memory/canonical_claims.json)

### Load-on-trigger files

Load these when the task specifically needs them:

- [automation/memory/content_index.json](/Users/oleg/Projects/claude-playground/automation/memory/content_index.json)
  - when cluster membership, page inventory, or archetype mapping matters
- [automation/memory/entities.json](/Users/oleg/Projects/claude-playground/automation/memory/entities.json)
  - when terminology, aliases, or entity naming matters
- [automation/memory/source_registry.json](/Users/oleg/Projects/claude-playground/automation/memory/source_registry.json)
  - when the task touches competitor/source discovery, external validation, or web-source intake
- [automation/memory/release_checklist.md](/Users/oleg/Projects/claude-playground/automation/memory/release_checklist.md)
  - when evaluating merge-readiness, SEO/publishing quality, or final QA
- [automation/README.md](/Users/oleg/Projects/claude-playground/automation/README.md)
  - when the task touches automation, manifests, pipeline commands, or reports
- [automation/workers/README.md](/Users/oleg/Projects/claude-playground/automation/workers/README.md)
  - when the task designs, reviews, or implements LLM workers / agents
- [automation/memory/topic_backlog.csv](/Users/oleg/Projects/claude-playground/automation/memory/topic_backlog.csv)
  - when the task is about planning, backlog, prioritization, or automation intake

Do not rely on memory alone when one of these files is the natural source-of-truth for the task.

## File Reading Policy

Use this policy for both normal chat requests and agent-style workflows.

Goal:

- load enough repo context to be accurate and safe
- avoid blind assumptions
- avoid opening the whole repo when it is not necessary

### Always read first

For any non-trivial content, SEO, UX, automation, architecture, or publishing task, read:

1. this file: `AGENTS.md`
2. the always-load core files
3. any load-on-trigger files that the task clearly requires

This is the default flow for both:

- explicit agent-like workflows
- ordinary chat requests about this repo

### When it is acceptable not to open extra files

You do not need to open additional files when the request is:

- purely high-level and already answered by this file plus the memory files
- about workflow or policy rather than page/script specifics
- answerable without depending on current repo state

If the answer depends on the actual implementation, current page copy, file relationships, generators, or automation state, open the relevant files.

### Then read only what is necessary

After the global/project context is loaded:

- open the directly affected page(s)
- open neighboring cluster pages if the task affects routing, role separation, or canonical claims
- open the generating script/data source if the page is generated or data-driven
- open the relevant check script if the task touches publishing, indexing, or structured data

### Do not over-read the repo

Do not read the entire repo by default for every request.

Instead:

- start with project instructions and memory files
- then load only the files that are directly relevant to the task
- widen the context only when there is real ambiguity or integration risk

### When deeper file reading is required

You must inspect additional files when:

- the page belongs to a content cluster and role separation matters
- the task changes internal links, hubs, atlases, or navigation
- the page is generated from JSON/scripts
- the task touches a canonical claim
- the task affects layout/components shared by many pages
- the task affects indexing, schema, sitemap, or search-index generation

### Specific file-reading defaults

Use these defaults unless there is a good reason not to:

- for content changes to an existing page:
  - open the target page
  - open `content_index.json` if cluster membership or archetype is not obvious
  - open one upstream hub or atlas page
  - open one adjacent page in the same cluster if role separation matters
- for new pages:
  - open the closest existing archetype example
  - open the relevant cluster hub
  - open `content_index.json`
  - open the canonical claims and entities files for the topic
- for research branch pages:
  - open the JSON source in `data/research_branches/`
  - open `data/research_branch_schema.md`
  - open `scripts/generate_research_branch.py`
  - do not rely on generated HTML alone
- for automation tasks:
  - open `automation/README.md`
  - open `automation/workers/README.md` when the task touches LLM workers / agents
  - open the relevant memory file(s)
  - open the exact script or CLI entrypoint being changed
- for SEO/indexing/publishing tasks:
  - open `automation/memory/seo_llm_optimization.md`
  - open the target page(s)
  - open the relevant script in `scripts/`
  - consult `automation/memory/release_checklist.md`

### Safe default behavior

If uncertain:

- prefer consulting the repo source-of-truth files
- prefer reading one more relevant page/script over making an assumption
- prefer the smallest safe edit over a broad rewrite

## Core Product Model

This site is not a general wiki. It is a **practical operations-first guide site**.

Primary page families:

- `home-hub`: `index.html`
- `cornerstone-guide`: broad winners like `research.html`, `heroes.html`, `events.html`, `codes.html`, `f2p.html`
- `support-guide`: exact operational pages like `gift-center-uid.html`, `redeem-code-not-working.html`, `shield.html`, `arena.html`, `radar.html`
- `atlas-page`: navigational cluster hub like `research-costs.html`
- `cost-page`: exact utility pages like research branch pages, `alliance-recognition-cost.html`, `vehicle-modification-cost.html`
- `event-guide`, `hero-profile`, `comparison-guide`, `site-page`

Always choose the **smallest correct archetype**. Do not default to “new article”.

## Critical Cluster Rules

### Gift Center cluster

Roles are fixed:

- `codes.html` = hub
- `gift-center-uid.html` = setup
- `redeem-code-not-working.html` = troubleshooting

Do not blur these roles without a strong reason.

Canonical flow:

- redeem via official Gift Center, not inside the game
- UID path: `Avatar -> Settings -> Copy ID`
- rewards go to mailbox

### Research cluster

Mainline guidance is fixed unless strong evidence says otherwise:

- Hero Training to Cockpit
- Military Strategies
- Peace Shield / Urgent Rescue
- then choose by account goal:
  - shortest practical UST/T10 path for tier progression
  - Siege to Seize into Field Research only for late-game Recharge Shield / deep combat scaling

Additional rules:

- `Hero Training` is mainly for `Cockpit`
- `Peace Shield` is high-value because of `Urgent Rescue`
- `Field Research` follows `100% Siege to Seize`, but it is badge-heavy and should not be treated as a required step before UST/T10
- `research-costs.html` is the atlas/hub and should route into exact branch pages, not replace them

### Seasons

Current canonical interpretation:

- for newer servers, `Season 2 = Winter`
- `Desert` was canceled or skipped
- older guides may still map `Season 2 = Desert`

When a page touches seasons, ambiguity must be clarified explicitly.

### News preview / Reddit digest

`news-preview.html` and `content/news/*reddit-lastz-digest.md` are archived internal experiments.

Rules:

- do not optimize, modernize, link, or include them in editorial / LLM automation unless explicitly requested
- keep `news-preview.html` noindex-only and outside user-facing navigation
- do not run `scripts/reddit_ingest.py` unless the task explicitly resumes the news experiment

### Economy / diamonds / shields

Current canonical stance:

- diamonds are reserve-first, not reactive convenience spend
- Alliance Shop shields are usually better value than buying shields directly with diamonds when stock exists

## Data-Driven Research Pages

Research branch cost/tree pages are **data-driven**.

If you need to change or add one of these pages:

- edit the source JSON under [data/research_branches](/Users/oleg/Projects/claude-playground/data/research_branches)
- follow [data/research_branch_schema.md](/Users/oleg/Projects/claude-playground/data/research_branch_schema.md)
- regenerate with [scripts/generate_research_branch.py](/Users/oleg/Projects/claude-playground/scripts/generate_research_branch.py)

Do **not** hand-edit generated research branch HTML unless there is a very good reason and the generator cannot express the change.

Current generated branch set includes:

- `hero-training-cost.html`
- `military-strategies-cost.html`
- `peace-shield-cost.html`
- `siege-to-seize-cost.html`
- `field-research.html`
- `army-building-cost.html`
- `fully-armed-alliance-cost.html`
- `unit-special-training-cost.html`

## Content Editing Rules

### User-Visible Content Approval Gate

Any change that affects content real users can read or search/AI systems can quote requires explicit user approval before it is applied, committed, or pushed.

This includes:

- visible page copy
- titles, H1s, meta descriptions, canonical tags, robots directives, and structured data
- sitemap/search-index changes caused by content updates
- public navigation, internal links, cards, FAQs, tables, and first-screen answers

Required flow:

1. prepare a proposed text diff or exact before/after text
2. show it to the user for review
3. wait for explicit approval
4. only then apply the content change and continue with checks, commit, and push

Do not treat general permission to work on the project as approval for user-visible content edits. Approval must be tied to the proposed content change or exact diff.

For every content task:

1. Identify the page’s **primary job**.
2. Preserve or improve the page’s role inside its cluster.
3. Improve:
   - first-screen answer
   - title/H1/meta fit
   - canonical terminology
   - internal routing
   - exact utility
   - concrete human utility beyond generic rewording
4. Avoid:
   - rewriting winners without evidence
   - duplicate pages for near-identical intent
   - long intros that delay the answer
   - unsupported event/season/mechanic claims
   - generic AI-guide prose that sounds polished but does not help a player decide
   - repeated trust/freshness boilerplate without page-specific evidence

Always consider:

- upstream hub
- downstream support page or atlas
- one lateral related page if useful

## Technical / Publishing Rules

After meaningful content changes, run:

```bash
python3 scripts/prepublish_check.py --fix
python3 scripts/prepublish_check.py
```

Use the automation-layer checks when they help:

```bash
python3 automation/pipeline.py checks
python3 automation/pipeline.py checks --strict
```

Remember:

- `checks` = baseline health
- `checks --strict` = stronger gate, includes weak-cluster, content-consistency, and SEO/LLM warning-level failures
- site structure, search visibility, and content-consistency hard failures are always hard failures because they protect shared navigation, guide template signals, generated research branch boundaries, canonical player guidance, and AI/search snippet eligibility

No autonomous production publish.

Required path:

1. draft
2. review
3. green checks
4. manual approval
5. merge / deploy

## Automation Layer Rules

The `automation/` layer is a **draft-first editorial automation MVP**, not a self-publishing agent swarm.

Use [automation/pipeline.py](/Users/oleg/Projects/claude-playground/automation/pipeline.py) as the default operator entrypoint.

Important commands:

```bash
python3 automation/pipeline.py health
python3 automation/pipeline.py list
python3 automation/pipeline.py backlog-sync
python3 automation/pipeline.py open-topic <topic_id>
python3 automation/pipeline.py open-run <run_id>
python3 automation/pipeline.py next-step <run_id>
python3 automation/pipeline.py recent-runs
python3 automation/pipeline.py propose <run_id>
python3 automation/pipeline.py approval <run_id> --state approved --all
python3 automation/pipeline.py apply-preview <run_id>
python3 automation/pipeline.py apply-approved <run_id>
python3 automation/pipeline.py close-run <run_id>
python3 automation/pipeline.py worker-chain --topic-id <topic_id> --json
python3 automation/pipeline.py worker-intake --topic-id <topic_id> --json
python3 automation/pipeline.py worker-run-plan --topic-id <topic_id> --json
python3 automation/pipeline.py worker-run-plan --intake <intake.json> --basename <basename> --json
python3 automation/pipeline.py worker-manifest --topic-id <topic_id> --created-by <name> --json
python3 automation/pipeline.py llm-adapter --request <request.json> --provider fixture --fixture <response.json> --json
python3 automation/pipeline.py llm-adapter --request <request.json> --provider openai --json
python3 automation/pipeline.py external-scout --json
python3 automation/pipeline.py external-evidence-refresh --external-scout automation/reports/external-scout.json --json
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
python3 automation/pipeline.py content-seo-opportunities --json
python3 automation/pipeline.py bing-report
python3 automation/pipeline.py content-voice --json
python3 automation/workers/scout.py --json
python3 automation/workers/editor.py --topic-id <topic_id> --json
python3 automation/workers/reviewer.py --topic-id <topic_id> --json
python3 automation/workers/run_chain.py --topic-id <topic_id> --json
python3 automation/workers/intake.py --topic-id <topic_id> --json
python3 automation/workers/intake_to_run.py --topic-id <topic_id> --json
python3 automation/workers/write_manifest.py --topic-id <topic_id> --created-by <name> --json
python3 automation/workers/llm_adapter.py --request <request.json> --provider fixture --fixture <response.json> --json
python3 automation/workers/llm_adapter.py --request <request.json> --provider openai --json
python3 automation/workers/external_scout.py --json
python3 automation/workers/external_evidence_refresh.py --external-scout automation/reports/external-scout.json --json
python3 automation/workers/llm_scout.py --provider openai --json
python3 automation/workers/llm_scout.py --external-proposals automation/reports/external-scout.json --provider openai --json
python3 automation/workers/llm_candidate_refresh.py --provider openai --json
python3 automation/workers/llm_auto_review_queue.py --provider openai --json
python3 automation/workers/llm_topic_discovery.py --json
python3 automation/workers/llm_topic_decision.py --topic-id <topic_id> --state monitor --decided-by <name> --json
python3 automation/workers/llm_run_approved_handoffs.py --provider openai --json
python3 automation/workers/llm_editor.py --topic-id <topic_id> --provider openai --json
python3 automation/workers/llm_reviewer.py --topic-id <topic_id> --provider openai --json
python3 automation/workers/llm_worker_chain.py --topic-id <topic_id> --provider openai --json
python3 automation/workers/llm_worker_chain.py --from-decision automation/reports/llm-topic-decision-<topic_id>.json --provider openai --json
python3 automation/workers/llm_intake.py --approved-by <name> --note "<owner answer / approval scope>" --json
python3 automation/reports/llm_review_latest.py --json
python3 automation/reports/content_seo_opportunities.py --json
python3 -m unittest discover -s automation/tests -p 'test_*.py'
```

The `openai` LLM adapter provider is live but still no-write and fail-closed. It requires `OPENAI_API_KEY`, uses `OPENAI_MODEL` when set, defaults to `gpt-5.4-mini`, and returns only validated plain-ASCII JSON artifacts. It must not edit content, backlog, manifests, or production state.

`external-scout` is the no-write external source discovery layer. It reads `automation/memory/source_registry.json`, emits candidate proposals from approved source/topic seeds, and records proposed sources that still need owner approval. External sources are discovery and cross-validation signals only: they must not be used to copy competitor wording, prove public claims from one source, mutate backlog/manifests, edit content, open PRs, or deploy. Public claims found externally still require canonical-memory checks, cross-validation, exact proposed text, and explicit owner approval.

`external-evidence-refresh` is the no-write evidence queue layer for External Scout artifacts. It turns approved `source_query_tasks` and explicit `source_urls` into provider-ready query tasks, URL evidence leads, and claim review groups. It does not fetch live web content yet, prove claims, approve public copy, mutate backlog/manifests, edit content, open PRs, or deploy.

`llm-scout` is the first live LLM worker wrapper. It reviews deterministic Scout proposals from GSC/Bing agent signals and optional External Scout proposals through `llm_adapter`, writes request/result/markdown artifacts, and must not edit content, backlog, manifests, PRs, or production state. Monitor-only and reject decisions belong in `rejected_or_monitor`, not selected handoffs.

`llm-candidate-refresh` is the scheduled no-write candidate generation step. It runs LLM Scout, converts the result into topic discovery proposals, and writes a compact owner-review summary. It may accept External Scout proposal artifacts through `--external-proposals`. It must not record owner decisions, edit content, mutate `topic_backlog.csv`, create manifests, open PRs, or deploy.

`llm-auto-review-queue` runs candidate refresh, scores candidate topics, and automatically runs the top no-write Editor/Reviewer chains into one consolidated owner-review queue. It may accept External Scout proposal artifacts through `--external-proposals`. It skips topics that already have completed chain summaries unless `--include-existing` is supplied. It must not approve public copy, mutate backlog, create manifests, edit content, open PRs, or deploy.

`llm-topic-discovery` converts selected and monitored LLM Scout opportunities into backlog-shaped topic proposals for owner review. It must not edit `topic_backlog.csv`, manifests, content, PRs, or production state.

`llm-topic-decision` records an owner decision for one LLM topic discovery proposal. It may also rerecord an existing decision through `--from-decision` to move a saved topic from `monitor` or `rejected` to `approved_for_chain` without manual JSON edits. `approved_for_chain` only allows the next no-write worker chain; `monitor` and `rejected` keep the topic out of intake. It must not approve public copy, patch specs, backlog edits, manifests, PRs, or production state.

`llm-topic-decisions` consolidates all LLM topic decision artifacts into one read-only operator report. It must not approve content edits or mutate backlog, manifests, PRs, or production state.

`llm-approved-handoffs` is a read-only operator view over `approved_for_chain` decisions. It prints ready-to-run deterministic `llm-worker-chain --from-decision ...` commands and must not approve content edits or mutate backlog, manifests, PRs, or production state.

`llm-run-approved-handoffs` runs pending `approved_for_chain` decision artifacts through the no-write `llm-worker-chain --from-decision` path. It skips decisions that already have a current completed chain summary unless `--include-current` is supplied. It must not call live Scout reranking, approve public copy, mutate backlog, create manifests, edit content, open PRs, or deploy.

`llm-editor` is the second live LLM worker wrapper. It creates a planning brief from one selected LLM Scout opportunity and deterministic Editor context. It may include `exact_replacements` only as draft proposal data with `owner_approval_required: true`; this does not approve copy, create Patch Specs, edit files, or bypass the proposal/approval/apply lifecycle. It must not write final public page copy, patch specs, content edits, backlog entries, manifests, PRs, or production state.

`llm-reviewer` is the third live LLM worker wrapper. It reviews one LLM Editor planning brief for duplicate intent, cluster role fit, canonical claims, template safety, draft exact replacement safety, owner questions, and readiness. It must not write final public page copy, patch specs, content edits, backlog entries, manifests, PRs, or production state. It cannot advance LLM exact replacements directly to `apply-preview`.

`llm-worker-chain` runs the no-write live LLM Scout -> Editor -> Reviewer sequence and writes one summary artifact. Prefer `--from-decision automation/reports/llm-topic-decision-<topic_id>.json` after owner approval so the chain replays the saved `approved_for_chain` decision instead of rerunning Scout and changing the topic handoff. Live Scout handoffs may advance only `ready_for_chain` opportunities: `update_existing`, `create_new`, or `consolidate` with non-low priority. Monitor-only, reject, and low-priority topics must stop before Editor/Reviewer. It must preserve each stage's fail-closed behavior and must not write content, backlog entries, manifests, PRs, or production state.

GitHub workflow `.github/workflows/llm-candidate-refresh.yml` runs weekly and by manual dispatch to refresh no-write candidate topic artifacts from GSC/Bing signals. It uploads artifacts only and must not commit reports, record owner decisions, edit content, open PRs, or deploy.

GitHub workflow `.github/workflows/llm-auto-review-queue.yml` runs daily, after signal-file or external-source infrastructure pushes, and by manual dispatch. It runs `external-scout` first, runs `external-evidence-refresh` over the generated External Scout artifact, passes `automation/reports/llm-auto-review-queue/external-scout.json` into `llm-auto-review-queue --external-proposals`, uploads artifacts, and may commit only `automation/reports/llm-auto-review-queue/` report artifacts. It must not edit content, backlog, manifests, PRs, or production state.

GitHub workflow `.github/workflows/llm-worker-chain.yml` runs pending owner-approved handoffs after committed `llm-topic-decision-*.json` pushes and can manually replay one approved decision path. It is not scheduled, to avoid rerunning the same approved decision every week without committing generated reports. It uploads artifacts only and must not commit reports, edit content, open PRs, or deploy.

`llm-review-latest` reads the latest local LLM worker chain summary and renders a compact owner-review view. It is read-only and must not call an LLM provider, edit content, or mutate repository state.

`llm-intake-latest` bridges a latest or specified LLM worker chain summary into a no-write, owner-gated intake artifact. It may carry draft `exact_replacements` into intake as proposal-only data, but it may record `--approved-by <name>` only as intake approval. Approval is intake-only and does not approve public copy, patch specs, backlog mutation, manifest creation, PR creation, deployment, or production publishing. If the LLM Reviewer left owner questions, `--note` is required before intake can become `approved_for_intake`. If the Reviewer used `blocking_issues` for owner-confirmation items, `--resolve-reviewer-blockers` may downgrade them to intake warnings only when `--approved-by` and `--note` are both present. Approved LLM intake must still move through the existing run-plan/proposal lifecycle before any public content edit.

Machine-readable snapshots exist for:

- `health --json`
- `status --json`
- `list --json`
- `backlog-summary --json`
- `backlog-sync --json`
- `open-topic --json`
- `show --json`
- `open-run --json`
- `recent-runs --json`
- `next-step --json`
- `content-seo-opportunities --json`

Lifecycle currently:

- `plan`
- `init-run`
- `review`
- `brief`
- `patch-plan`
- `propose`
- `approval`
- `apply-preview`
- `apply-approved`
- `close-run`
- `bundle-run`

`patch-plan` is still safe/proposal-only. It may populate candidate `changed_files` in the manifest, but it must not edit site content automatically.

`propose` renders human-reviewable proposed edits from Patch Spec v1 entries. It must not edit site content.

`brief`, `patch-plan`, and `propose` may take a manifest path instead of only a run ID, and each supports `--output-dir <dir>` for staged Worker e2e checks that should not write reports into `automation/reports`.

Patch plans may emit `safe_exact_replace` specs only when they contain exact `exact_old` and `exact_new` strings for a non-generated HTML file. These specs are still proposal-only until explicit owner approval.

Future worker/run-plan artifacts may carry exact snippets through `plan.exact_replacements`. This field is allowed only as proposal data; it does not approve copy or bypass `propose`, `approval`, `apply-preview`, `apply-approved`, or strict QA. LLM Editor receives limited raw target-page snippets in `current_page_snapshot.source_snippets` so `exact_old` can be copied literally; any LLM exact replacement must still match the current target HTML exactly once or the worker fails closed.

`approval` records human approval decisions for proposal specs. `approved_for_apply` is still not an autonomous publishing state; it only gates a future controlled manual apply or safe apply worker.

`apply-preview` renders a no-write preview from approved specs. It may write manifest/report artifacts, but it must not edit site content.

`apply-approved` may edit source files, but only from approved Patch Spec v1 entries and only through conservative deterministic templates. Unsupported approved operations must fail loudly instead of being silently skipped. Generated research branch pages must still be edited through JSON source files and regenerated.

`safe_exact_replace` is the only generic content-side apply operation. It may replace an exact owner-approved `exact_old` snippet with an exact owner-approved `exact_new` snippet, but only when the old snippet appears exactly once in a non-generated HTML source file and `target_file`, `source_of_truth_file`, and `output_file` all match. It must fail closed on missing text, duplicate matches, generated files, unsafe paths, or unsupported source types. It must not generate or infer public copy.

`content-seo-opportunities` is a no-write report that combines GSC signals, content index memory, page structure, metadata, trust signals, and generated-page boundaries. It is planning context only and must not be treated as automatic approval to edit high-risk pages.

`bing-report` fetches Bing Webmaster weekly buckets into `content/bing/latest-bing-report.md` and `content/bing/latest-bing-agent-signals.json`. Bing signals are planning context only. Compare them with GSC/site memory before proposing content changes, and never treat Bing impressions or query drift as automatic approval to edit.

`content-voice` is a no-write audit for generic, low-utility, or mass-produced writing signals. It is planning context only and must not be treated as automatic approval to rewrite public pages. Public content changes still require exact proposed text and explicit human approval.

When `checks --strict --manifest <run_id>` passes after `apply-approved`, the run may advance from `applied_pending_qa` to `qa_passed`. `qa_passed` is still not an autonomous production publishing state.

`close-run` closes a `qa_passed` run, or a fully `rejected` proposal run that needs no content changes, with a final handoff artifact. It must not deploy.

Whenever automation commands, lifecycle stages, manifest states, instructions, or operator workflows are added or changed, update the relevant documentation in the same change. At minimum, check:

- `AGENTS.md`
- `automation/README.md`
- `automation/manifests/README.md`
- root `README.md` when the operator-facing summary changes

## Preferred Behavior For Future Agents

When given a new request:

1. Read this file first.
2. Load the relevant memory files listed above.
3. Follow the file reading policy in this file.
4. Make the smallest useful, safest change.
5. Keep cluster roles and canonical claims intact.
6. Update documentation when automation, instructions, lifecycle states, or operator commands change.
7. Run the appropriate checks.
8. Report concrete outcomes and residual risks.

If there is ambiguity between:

- old vs new season naming
- hub vs support page role
- manual HTML vs generated page source

prefer the canonical memory files and the generator/data source over ad hoc edits.
