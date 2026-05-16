# Last Z Guides

Static guide site for `lastzguides.com`.

## Project Instructions

Root [AGENTS.md](/Users/oleg/Projects/claude-playground/AGENTS.md) is the main repo-level instruction file for this project.

Use it as the default operating manual for both:

- agent-style workflows
- ordinary chat requests about this repository

It does not override platform or developer instructions, but it is the default local source for:

- project rules
- file-reading flow
- cluster roles
- canonical content constraints
- SEO / LLM optimization rules
- safe editing and publishing behavior

## Local workflow

The publish flow stays the same:

1. Edit pages locally in VS Code.
2. Run the local checks when needed.
3. Commit and `Sync Changes`.

## Local automation

These scripts are meant to be run locally before publishing. I will also use them automatically during larger edit passes.

### One-command check

```bash
python3 scripts/prepublish_check.py
```

What it does:

- checks that `sitemap.xml` and `search-index.json` match the current HTML pages
- audits HTML pages for common issues like missing metadata, broken markers, broken `<title>` content, canonical mismatches, and likely duplicate paragraphs

### Auto-fix indexing files

```bash
python3 scripts/prepublish_check.py --fix
```

What `--fix` does:

- syncs `dateModified` / `article:modified_time` from real file mtimes
- injects or refreshes sitewide `Organization` JSON-LD
- syncs verification blocks across content pages
- rebuilds `sitemap.xml`
- rebuilds `search-index.json` while preserving existing titles, categories, descriptions, and keywords when they already exist

### Individual scripts

```bash
python3 scripts/audit_site.py
python3 scripts/check_site_indexing.py
python3 scripts/check_site_indexing.py --fix
python3 scripts/sync_structured_data.py
python3 scripts/sync_verification_blocks.py
```

## Automation MVP

The repo now also contains a separate `automation/` layer for a controlled editorial automation MVP.

This is **not** an autonomous publishing system. It is a draft-first planning and review foundation:

- explicit site memory
- structured backlog
- deterministic QA helpers
- run manifests
- human-readable review bundles
- editor briefs
- proposal approval records
- no-write apply previews
- controlled apply results
- closeout reports

Root `README.md` only gives the short project-level view.
Use [automation/README.md](/Users/oleg/Projects/claude-playground/automation/README.md) as the full operator reference for:

- CLI commands
- lifecycle states
- manifests and report artifacts
- baseline vs strict automation checks

Most useful entrypoints:

```bash
python3 automation/pipeline.py checks
python3 automation/pipeline.py checks --strict
python3 automation/pipeline.py status
python3 automation/pipeline.py list
python3 automation/pipeline.py backlog-sync
python3 automation/pipeline.py open-topic <topic_id>
python3 automation/pipeline.py open-run <run_id>
python3 automation/pipeline.py recent-runs
python3 automation/pipeline.py propose <run_id>
python3 automation/pipeline.py exact-proposals <run_id>
python3 automation/pipeline.py approval <run_id> --state approved --all --dry-run
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
python3 automation/pipeline.py external-evidence-collect --provider fetch --evidence-refresh automation/reports/external-evidence-refresh.json --json
python3 automation/pipeline.py external-search-collect --provider openai --evidence-refresh automation/reports/external-evidence-refresh.json --json
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
python3 automation/pipeline.py llm-auto-review-latest --json
python3 automation/pipeline.py llm-intake-latest --json
python3 automation/pipeline.py llm-intake-latest --approved-by <name> --note "<owner answer / approval scope>" --json
python3 automation/pipeline.py llm-intake-latest --approved-by <name> --note "<owner answers>" --resolve-reviewer-blockers --json
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
python3 automation/workers/external_evidence_collect.py --provider fetch --evidence-refresh automation/reports/external-evidence-refresh.json --json
python3 automation/workers/external_search_collect.py --provider openai --evidence-refresh automation/reports/external-evidence-refresh.json --json
python3 automation/workers/llm_scout.py --provider openai --json
python3 automation/workers/llm_scout.py --external-proposals automation/reports/external-scout.json --provider openai --json
python3 automation/workers/llm_candidate_refresh.py --provider openai --json
python3 automation/workers/llm_editor.py --topic-id <topic_id> --provider openai --json
python3 automation/workers/llm_reviewer.py --topic-id <topic_id> --provider openai --json
python3 automation/workers/llm_worker_chain.py --topic-id <topic_id> --provider openai --json
python3 automation/workers/llm_intake.py --approved-by <name> --note "<owner answer / approval scope>" --json
python3 automation/reports/llm_review_latest.py --json
python3 automation/reports/llm_auto_review_latest.py --json
python3 -m unittest discover -s automation/tests -p 'test_*.py'
```

`checks` includes:

- content index memory sync
- orphan / weak-cluster coverage
- cluster-link expectations
- site structure consistency for shared navigation, guide template signals, and generated research branch boundaries
- search visibility controls for robots.txt, snippets, and first-screen answer blocks
- content consistency protection for canonical player guidance
- SEO/LLM alignment warnings
- basic cannibalization warnings

`checks --strict` turns weak-cluster and SEO/LLM warnings into a failing gate. Site structure and search visibility issues are always hard failures.

`content-voice` is a separate no-write audit for generic, mass-produced, or low-utility writing signals. It is planning context only; public content rewrites still require exact proposed text and explicit human approval.

Automation artifacts live in:

- `automation/manifests/<run_id>.json`
- `automation/reports/<run_id>.md`
- `automation/reports/<run_id>.brief.md`
- `automation/reports/<run_id>.patch.md`
- `automation/reports/<run_id>.proposed.md`
- `automation/reports/<run_id>.apply-preview.md`
- `automation/reports/<run_id>.apply-result.md`
- `automation/reports/<run_id>.closed.md`
- `automation/reports/content-seo-opportunities.md`
- `automation/reports/content-seo-opportunities.json`
- `automation/reports/llm-scout-review.md`
- `automation/reports/llm-scout-review-result.json`
- `automation/reports/llm-candidate-refresh.md`
- `automation/reports/llm-candidate-refresh.json`
- `automation/reports/llm-editor-brief-<topic_id>.md`
- `automation/reports/llm-editor-brief-<topic_id>-result.json`
- `automation/reports/llm-reviewer-gate-<topic_id>.md`
- `automation/reports/llm-reviewer-gate-<topic_id>-result.json`
- `automation/reports/llm-worker-chain-<topic_id>.md`
- `automation/reports/llm-worker-chain-<topic_id>.json`

Future LLM worker contracts live in:

- `automation/workers/README.md`

That contract layer defines the planned `Scout -> Editor -> Reviewer` flow. The first implemented workers are no-write `Scout`, `Editor`, and `Reviewer` steps plus a chain runner, intake gate, run-plan proposal step, LLM Scout review wrapper, scheduled candidate refresh, LLM topic discovery/decision gates, LLM Editor planning wrapper, LLM Reviewer gate wrapper, and live LLM worker-chain wrapper that turn weekly GSC/Bing agent signals into reviewable topic proposals, content briefs, readiness verdicts, explicit human-gated intake artifacts, draft run-plan proposals, JSON-only LLM opportunity reviews, durable owner topic decisions, no-copy planning briefs, no-write review gates, and one-command LLM chain summaries.

For staged Worker e2e checks, `brief`, `patch-plan`, and `propose` can read a manifest path and write reports to a custom `--output-dir`, so fixture runs do not need to dirty `automation/reports`.

## GSC Analytics Automation

The weekly GSC workflow writes:

- `content/gsc/latest-gsc-report.md` for human review
- `content/gsc/latest-gsc-agent-signals.json` for LLM-agent planning input

The weekly Bing workflow writes:

- `content/bing/latest-bing-report.md` for human review
- `content/bing/latest-bing-agent-signals.json` for LLM-agent planning input

Use the JSON file as an analytics signal source only. Before turning a signal into a content task, check `AGENTS.md`, site memory, canonical claims, cluster roles, and the relevant page source.

For a no-write sitewide opportunity review, run:

```bash
python3 automation/pipeline.py content-seo-opportunities --json
```

The report combines GSC page/query signals with page structure, metadata length, first-screen answer coverage, trust-signal coverage, and generated-page boundaries.

For Bing-specific Scout input, run:

```bash
python3 automation/workers/scout.py --signals content/bing/latest-bing-agent-signals.json --basename scout-topic-proposals-bing --json
```

Bing data should be compared with GSC and site memory before creating any content task.

For a no-write LLM Scout review over the latest GSC and Bing agent signals, run:

```bash
python3 automation/pipeline.py llm-scout --provider openai --json
```

This writes `automation/reports/llm-scout-review-request.json`, `automation/reports/llm-scout-review-result.json`, and `automation/reports/llm-scout-review.md`. It is review context only; it does not edit content, backlog, manifests, PRs, or production state. Monitor/reject outcomes stay out of selected chain handoffs.

For no-write external source discovery from the approved source registry:

```bash
python3 automation/pipeline.py external-scout --json
```

This reads `automation/memory/source_registry.json` and writes `automation/reports/external-scout.json` / `.md`. External sources are topic-discovery and cross-validation signals only; they must not be used to copy competitor wording or prove public claims from one source.

To build a provider-ready no-write evidence queue from External Scout output:

```bash
python3 automation/pipeline.py external-evidence-refresh --external-scout automation/reports/external-scout.json --json
```

This writes `automation/reports/external-evidence-refresh.json` / `.md` with approved source queries, explicit URL leads, and claim review groups. It does not fetch live web content yet, prove claims, approve public copy, edit content, mutate backlog/manifests, open PRs, or deploy.

To collect limited metadata/snippets from explicit URL leads:

```bash
python3 automation/pipeline.py external-evidence-collect --provider fetch --evidence-refresh automation/reports/external-evidence-refresh.json --json
```

This writes `automation/reports/external-evidence-collect.json` / `.md`. The fetch provider reads only explicit HTTPS URL leads, stores short metadata/snippet evidence, defers search query tasks, and never marks public claims as ready.

To collect search-backed discovery leads from approved source queries:

```bash
python3 automation/pipeline.py external-search-collect --provider openai --evidence-refresh automation/reports/external-evidence-refresh.json --json
```

This writes `automation/reports/external-search-collect.json` / `.md`. The OpenAI provider uses Responses API `web_search` over approved source-query tasks, applies source-domain filters when possible, normalizes raw clusters/targets against `content_index.json`, emits proposal-shaped discovery leads for Scout, and never marks public claims as ready.

For scheduled-style candidate generation from current GSC/Bing signals:

```bash
python3 automation/pipeline.py llm-candidate-refresh --provider openai --json
```

This runs LLM Scout plus topic discovery and writes `automation/reports/llm-candidate-refresh.json`, `automation/reports/llm-candidate-refresh.md`, and referenced Scout/discovery artifacts. Use `--external-proposals automation/reports/external-scout.json` to include approved External Scout proposals. It prepares topics for owner review only; it does not record owner decisions, edit content, mutate backlog/manifests, open PRs, or deploy.

For a consolidated no-write queue that automatically reviews the strongest candidates:

```bash
python3 automation/pipeline.py llm-auto-review-queue --provider openai --json
```

This runs candidate refresh, scores candidate topics, auto-runs the top Editor/Reviewer chains, and writes `automation/reports/llm-auto-review-queue/llm-auto-review-queue.md`. Use `--external-proposals automation/reports/external-scout.json` to include approved External Scout proposals. It skips only current completed chain summaries; stale summaries with missing or old `worker_chain_contract_version` are rerun automatically. Per-topic LLM failures are captured in `completed_with_failures` reports without failing the scheduled command. It still does not approve public copy, edit content, mutate backlog/manifests, open PRs, or deploy.

For a durable no-write owner decision on one discovered topic, run:

```bash
python3 automation/pipeline.py llm-topic-decision --topic-id <topic_id> --state monitor --decided-by <name> --json
```

Use `approved_for_chain`, `monitor`, or `rejected`. This writes `automation/reports/llm-topic-decision-<topic_id>.json` and `.md`; it does not approve public content edits.

To reopen or approve an existing saved decision without editing JSON manually, run:

```bash
python3 automation/pipeline.py llm-topic-decision --from-decision automation/reports/llm-topic-decision-<topic_id>.json --state approved_for_chain --decided-by <name> --note "<approval note>" --json
```

This preserves the saved topic snapshot and records the previous decision in `previous_decision`.

To see the current decision state across all discovered topics, run:

```bash
python3 automation/pipeline.py llm-topic-decisions --json
```

This writes `automation/reports/llm-topic-decisions.json` and `.md`.

To list only topic decisions that are currently approved for deterministic worker-chain replay, run:

```bash
python3 automation/pipeline.py llm-approved-handoffs --json
```

This is read-only and prints ready-to-run `llm-worker-chain --from-decision ...` commands.

To run pending approved handoffs without live Scout reranking, run:

```bash
python3 automation/pipeline.py llm-run-approved-handoffs --provider openai --json
```

This reads committed `approved_for_chain` decision artifacts, skips already-current completed chain summaries by default, and writes no-write owner-review artifacts only.

For a no-write LLM Editor planning brief from one selected Scout opportunity, run:

```bash
python3 automation/pipeline.py llm-editor --topic-id <topic_id> --provider openai --json
```

This writes `automation/reports/llm-editor-brief-<topic_id>-request.json`, `automation/reports/llm-editor-brief-<topic_id>-result.json`, and `automation/reports/llm-editor-brief-<topic_id>.md`. It is a planning brief only; it must not contain final user-visible page copy or applyable patch specs. For existing HTML update opportunities, optional `exact_replacements` are preferred when the deterministic context has safe source snippets, but they remain draft proposal data only and require later owner approval. No-op exact candidates are dropped with a warning; unsafe candidates still block the Editor result.

When those exact replacements move through intake into `patch-plan`, the
proposal flow stays exact-only: it does not add broad manual placeholders like
`meta_refresh` beside the approved before/after candidate.

For a no-write LLM Reviewer gate from one LLM Editor brief, run:

```bash
python3 automation/pipeline.py llm-reviewer --topic-id <topic_id> --provider openai --json
```

This writes `automation/reports/llm-reviewer-gate-<topic_id>-request.json`, `automation/reports/llm-reviewer-gate-<topic_id>-result.json`, and `automation/reports/llm-reviewer-gate-<topic_id>.md`. It is a gate artifact only; it cannot approve high-risk user-visible changes without owner review or advance LLM exact replacements directly to apply.

For the full no-write live LLM worker chain, run:

```bash
python3 automation/pipeline.py llm-worker-chain --topic-id <topic_id> --provider openai --json
```

This runs `llm-scout -> llm-editor -> llm-reviewer` and writes `automation/reports/llm-worker-chain-<topic_id>.json` and `automation/reports/llm-worker-chain-<topic_id>.md` as a compact owner-review summary. It advances only `ready_for_chain` topics, and still cannot edit content, open PRs, or approve high-risk user-visible changes by itself.

After a topic has an owner decision of `approved_for_chain`, prefer the deterministic handoff:

```bash
python3 automation/pipeline.py llm-worker-chain --from-decision automation/reports/llm-topic-decision-<topic_id>.json --provider openai --json
```

This replays the saved decision snapshot instead of rerunning Scout, so the approved topic cannot be lost by a later LLM rerank.

To read the latest local chain summary without calling OpenAI again, run:

```bash
python3 automation/pipeline.py llm-review-latest
```

This prints the target page, verdict, risk, owner questions, blocking issues, required checks, and next step. Use `--json` for machine-readable output.

To read the latest consolidated auto-review queue as one owner decision screen, run:

```bash
python3 automation/pipeline.py llm-auto-review-latest
```

This prints queued topics, skipped-existing chain summaries, player-value checks, blocking issues, owner questions, and ready-to-run intake commands. It is read-only and does not approve public copy.

The same no-write chain is available in GitHub Actions:

- Workflow: `.github/workflows/llm-candidate-refresh.yml`
- Schedule: weekly after the GSC/Bing report windows
- Manual dispatch: optional `model` input
- Output: uploaded candidate refresh artifact only, no commits, decisions, content edits, or PRs

The consolidated no-write queue is available in GitHub Actions:

- Workflow: `.github/workflows/llm-auto-review-queue.yml`
- Schedule: daily
- Manual dispatch: optional `model`, `max_chains`, and `include_existing` inputs
- Push trigger: signal files, source registry, External Scout / Evidence workers, and LLM worker infrastructure
- External discovery: runs `external-scout`, builds `external-evidence-refresh`, collects explicit URL evidence with `external-evidence-collect --provider fetch`, collects approved source-query leads with `external-search-collect --provider openai`, and passes External Scout plus External Search proposal artifacts into `llm-auto-review-queue --external-proposals`
- Output: uploaded artifact plus committed `automation/reports/llm-auto-review-queue/` report artifacts only
- Content/backlog/manifests/PRs/deploy modified: `false`

The owner-approved no-write handoff runner is also available in GitHub Actions:

- Workflow: `.github/workflows/llm-worker-chain.yml`
- Schedule: none; weekly discovery stays in `llm-candidate-refresh.yml`
- Manual dispatch: optional `decision_path`, `model`, and `include_current` inputs
- Push trigger: path-limited to LLM worker infrastructure and committed `llm-topic-decision-*.json` artifacts
- Output: uploaded artifact only, no commits or PRs

## Notes

- No CI or deploy changes are required.
- The scripts are local safety rails, not a new publishing system.
- `search-index.json` can still be edited manually when you want custom wording or keywords.

## LLM referral observability

The site tracks a lightweight `llm_referral_session` event when a visit appears to come from:

- `utm_source=chatgpt.com`
- `chatgpt.com`
- `perplexity.ai`
- `copilot.microsoft.com`
- `bing.com`
- `grok.com`
- `x.com`

Suggested GA4 views:

- segment or exploration filtered to `event_name = llm_referral_session`
- breakdown by the event parameter `llm_source`
- breakdown by the event parameter `llm_channel`
- landing pages filtered by the event parameter `landing_page`
- optional secondary breakdown by `referrer_host`

Suggested GA4 setup:

- register `llm_source`, `llm_source_type`, `llm_channel`, `landing_page`, and `referrer_host` as event-scoped custom dimensions
- build an exploration filtered to `event_name = llm_referral_session`
- compare `chatgpt`, `perplexity`, `copilot`, `bing`, and `grok` over time
- use `llm_channel` to separate true LLM traffic from Bing/search-surface traffic

Local reporting helper:

```bash
python3 automation/reports/llm_referral_report.py path/to/ga4-llm-referrals.csv --output automation/reports/llm-referrals.md
```

The helper expects a GA4 CSV export with dimensions such as `llm_source`, `llm_channel`, `landing_page`, and `referrer_host`, plus metrics such as `sessions`, `event_count`, or `total_users`. It does not call GA4 directly.

This is meant to answer:

- which pages get LLM referrals
- whether ChatGPT/Perplexity/Copilot traffic is growing
- whether LLM traffic behaves differently from standard search traffic

## llms.txt

The root `llms.txt` file is an optional discovery aid. It is not a substitute for crawlability, structured data, or page quality.
