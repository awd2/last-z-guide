# LLM Worker Contracts

This document defines the first safe contract layer for future LLM-assisted workers in the `lastzguides.com` automation system.

The goal is to help the site find useful new content and update opportunities while preserving:

- current page templates
- cluster roles
- canonical claims
- internal navigation patterns
- human review before publication
- deterministic QA as the final gate

This is a contracts-first layer. It is not an autonomous publishing system.

## Worker Chain

The intended chain is:

1. `Scout`
2. `Editor`
3. `Reviewer`

Each worker must write structured output into run artifacts or explicit proposal files. Workers must not directly publish production content.

The current no-write chain command is:

```bash
python3 automation/workers/run_chain.py --topic-id <topic_id> --json
```

It runs `Scout -> Editor -> Reviewer` and writes a summary artifact:

- `automation/reports/worker-chain-<topic_id>.json`
- `automation/reports/worker-chain-<topic_id>.md`

The current no-write intake gate is:

```bash
python3 automation/workers/intake.py --topic-id <topic_id> --json
```

It reads `automation/reports/worker-chain-<topic_id>.json` and writes:

- `automation/reports/worker-intake-<topic_id>.json`
- `automation/reports/worker-intake-<topic_id>.md`

If the worker review requires human approval, intake remains `approval_required` until rerun with `--approved-by <name>`. If the LLM Reviewer left owner questions, rerun with `--approved-by <name> --note "<owner answer / approval scope>"`; the note is required before LLM intake can become `approved_for_intake`.

The current no-write run-plan proposal step is:

```bash
python3 automation/workers/intake_to_run.py --topic-id <topic_id> --json
```

It reads `automation/reports/worker-intake-<topic_id>.json` and writes:

- `automation/reports/worker-run-plan-<topic_id>.json`
- `automation/reports/worker-run-plan-<topic_id>.md`

It only produces a `proposed_manifest` when the intake state is `approved_for_intake`; otherwise it emits a blocked artifact.

The current approved manifest writer is:

```bash
python3 automation/pipeline.py worker-manifest --topic-id <topic_id> --created-by <name> --json
```

It reads `automation/reports/worker-run-plan-<topic_id>.json` and writes:

- `automation/manifests/<run_id>.json`

It only writes when the run-plan state is `run_plan_ready` and the proposed manifest validates against the run manifest schema. It does not edit content files, backlog files, or production state. Use `--dry-run` to validate the target manifest path without writing.

After a staged manifest is created, `brief`, `patch-plan`, and `propose` can read that manifest path directly and write reports to a custom `--output-dir`. This keeps fixture or staging e2e checks outside `automation/reports` while preserving the normal lifecycle.

The lower-level helper remains available at:

```bash
python3 automation/workers/write_manifest.py --topic-id <topic_id> --created-by <name> --json
```

Worker contract fixture tests live at:

```bash
python3 -m unittest discover -s automation/tests -p 'test_*.py'
```

They validate the deterministic contract shape for Scout, Editor, Reviewer, intake, run-plan, and manifest writer steps using temporary output directories.

The current LLM provider adapter is fail-closed and artifact-only:

```bash
python3 automation/pipeline.py llm-adapter --request <request.json> --provider fixture --fixture <response.json> --json
python3 automation/pipeline.py llm-adapter --request <request.json> --provider openai --json
python3 automation/pipeline.py external-scout --json
python3 automation/pipeline.py external-evidence-refresh --external-scout automation/reports/external-scout.json --json
python3 automation/pipeline.py external-evidence-collect --provider fetch --evidence-refresh automation/reports/external-evidence-refresh.json --json
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
```

It validates structured request/response JSON for future LLM calls. The default provider is `disabled`, which returns a blocked result. `fixture` remains the deterministic offline provider for tests. `openai` calls the OpenAI Responses API and requires `OPENAI_API_KEY`; it uses `OPENAI_MODEL` when set and otherwise defaults to `gpt-5.4-mini`. The adapter requires plain ASCII English output and must not edit content, backlog, manifests, or production state.

The lower-level helper remains available at:

```bash
python3 automation/workers/llm_adapter.py --request <request.json> --provider fixture --fixture <response.json> --json
python3 automation/workers/llm_adapter.py --request <request.json> --provider openai --json
python3 automation/workers/external_scout.py --json
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
```

`external-scout` is the no-write external source discovery layer. It reads `automation/memory/source_registry.json`, emits candidate proposals from approved source/topic seeds, and records proposed sources that still need owner approval. It must not crawl broadly, copy competitor wording, use one external source as proof for public claims, mutate backlog/manifests, edit content, open PRs, or deploy. External claims are discovery and cross-validation signals only.

`external-evidence-refresh` is the no-write evidence queue layer. It reads an External Scout artifact and converts approved source queries plus explicit source URLs into provider-ready query tasks, URL evidence leads, and claim review groups. It does not fetch live web content yet, prove claims, approve public copy, mutate backlog/manifests, edit content, open PRs, or deploy.

`external-evidence-collect` is the no-write external fetch layer. With `--provider fetch`, it fetches only explicit HTTPS URL leads from `external-evidence-refresh`, stores limited metadata and short snippets for review, and leaves search query tasks deferred for a future search provider. It must not broadly crawl, prove public claims, approve public copy, mutate backlog/manifests, edit content, open PRs, or deploy.

`llm-scout` is the first live LLM worker wrapper. It builds deterministic Scout proposals from the latest GSC/Bing agent signals and optional External Scout proposal artifacts, sends a compact JSON-only review request through `llm_adapter`, and writes:

- `automation/reports/llm-scout-review-request.json`
- `automation/reports/llm-scout-review-result.json`
- `automation/reports/llm-scout-review.md`

It does not mutate backlog, manifests, content, PRs, or production state. `monitor` and `reject` decisions belong in `rejected_or_monitor`, not `selected_opportunities`. Selected opportunities remain review context only until a human approves the deterministic worker chain and any later content proposal.

`llm-candidate-refresh` is the scheduled no-write candidate generation wrapper. It runs LLM Scout, can merge External Scout proposals through `--external-proposals`, converts the Scout result into topic discovery proposals, and writes:

- `automation/reports/llm-candidate-refresh.json`
- `automation/reports/llm-candidate-refresh.md`
- referenced Scout request/result/markdown artifacts
- referenced topic discovery JSON/markdown artifacts

It prepares candidate and monitor topics for owner review. It does not record owner decisions, mutate `topic_backlog.csv`, create manifests, edit content, open PRs, or deploy. The GitHub Actions wrapper `.github/workflows/llm-candidate-refresh.yml` runs the same no-write refresh by weekly schedule and manual dispatch, uploads artifacts only, and does not commit generated reports. The higher-throughput `.github/workflows/llm-auto-review-queue.yml` runs daily and may commit only queue report artifacts under `automation/reports/llm-auto-review-queue/`.

`llm-topic-discovery` is the no-write bridge from LLM Scout selection and
monitoring output to owner-reviewed topic intake. It reads one LLM Scout
request/result pair and writes backlog-shaped proposals:

- `automation/reports/llm-topic-discovery.json`
- `automation/reports/llm-topic-discovery.md`

It does not mutate `topic_backlog.csv`, manifests, content, PRs, or production
state. The output is a review artifact only; a human still chooses whether a
topic should enter the worker chain, backlog, or monitoring queue. Topics from
LLM Scout's `rejected_or_monitor` list are preserved as `monitor` proposals so
owner decisions can still be recorded durably.

`llm-topic-decision` records that human choice as a durable no-write artifact.
It reads `automation/reports/llm-topic-discovery.json` by default and writes:

- `automation/reports/llm-topic-decision-<topic_id>.json`
- `automation/reports/llm-topic-decision-<topic_id>.md`

Supported decisions are:

- `approved_for_chain` -> the topic may proceed only to the next no-write LLM worker chain
- `monitor` -> keep the topic out of intake until materially new evidence appears
- `rejected` -> do not rerun the topic unless the owner explicitly reopens it

This decision artifact does not approve public copy, patch specs, backlog
mutation, manifest creation, PRs, or deployment.

To reopen or approve a saved decision without editing JSON manually, use:

```bash
python3 automation/pipeline.py llm-topic-decision --from-decision automation/reports/llm-topic-decision-<topic_id>.json --state approved_for_chain --decided-by <name> --note "<approval note>" --json
```

This preserves the saved `topic_snapshot`, writes the new decision artifact,
and records the previous state in `previous_decision`.

`llm-topic-decisions` consolidates the decision artifacts into one operator
summary:

- `automation/reports/llm-topic-decisions.json`
- `automation/reports/llm-topic-decisions.md`

It shows current counts by decision state and which topics, if any, are allowed
to proceed to the next no-write worker chain. It does not approve content edits
or mutate backlog, manifests, PRs, or production state.

`llm-approved-handoffs` is a read-only operator view over the same decision
artifacts. It lists only topics currently approved for chain replay and prints
ready `llm-worker-chain --from-decision ...` commands. It does not approve
content edits or mutate backlog, manifests, PRs, or production state.

`llm-run-approved-handoffs` is the scheduled owner-handoff runner. It reads the
same `approved_for_chain` decision artifacts and runs only pending handoffs
through deterministic `llm-worker-chain --from-decision` replay. If a completed
current chain summary already exists for the decision, it skips the handoff
unless `--include-current` is supplied. It does not run live Scout reranking,
approve public copy, mutate backlog, create manifests, edit content, open PRs,
or deploy.

`llm-auto-review-queue` is the higher-throughput no-write automation layer. It
runs candidate refresh, can merge External Scout proposals through
`--external-proposals`, scores candidate topics, auto-runs the top candidates
through Editor and Reviewer, and writes one consolidated owner-review queue. It
skips topics with existing completed chain summaries unless `--include-existing`
is supplied. This reduces owner involvement to reviewing ready queue packages,
but it still does not approve public copy, mutate backlog, create manifests,
edit content, open PRs, or deploy.

In GitHub Actions, `.github/workflows/llm-auto-review-queue.yml` runs
`external-scout` first, builds an `external-evidence-refresh` queue artifact,
collects explicit URL evidence with `external-evidence-collect --provider fetch`,
and passes the generated
`automation/reports/llm-auto-review-queue/external-scout.json` artifact into
`llm-auto-review-queue --external-proposals`. The workflow may commit only
queue report artifacts and must not edit public content or production state.

`llm-editor` is the second live LLM worker wrapper. It reads one selected LLM Scout opportunity, combines it with deterministic Editor context, sends a JSON-only planning request through `llm_adapter`, and writes:

- `automation/reports/llm-editor-brief-<topic_id>-request.json`
- `automation/reports/llm-editor-brief-<topic_id>-result.json`
- `automation/reports/llm-editor-brief-<topic_id>.md`

It must not generate final public page copy, patch specs, backlog entries, manifests, content edits, PRs, or production state. It is planning context only until deterministic review and owner approval.

The Editor schema may include `exact_replacements`, but only as draft proposal data. Each item must be target-only, include literal `exact_old` and `exact_new` strings, and set `owner_approval_required: true`. The deterministic Editor context exposes limited raw target-page snippets under `current_page_snapshot.source_snippets` so `exact_old` can be copied literally; this includes common guide-page snippets and home-hub hero/header snippets. The LLM Editor wrapper blocks any exact replacement whose `exact_old` does not match the current target HTML exactly once. These candidates do not approve copy, create Patch Specs, edit files, or skip the later `propose -> approval -> apply-preview -> apply-approved -> strict QA` flow.

`llm-reviewer` is the third live LLM worker wrapper. It reads one LLM Editor planning brief, sends a JSON-only review-gate request through `llm_adapter`, and writes:

- `automation/reports/llm-reviewer-gate-<topic_id>-request.json`
- `automation/reports/llm-reviewer-gate-<topic_id>-result.json`
- `automation/reports/llm-reviewer-gate-<topic_id>.md`

It checks duplicate intent, cluster role fit, canonical claims, template safety, draft exact replacement safety, owner questions, and readiness. It must not generate final public page copy, patch specs, backlog entries, manifests, content edits, PRs, or production state. High-risk cornerstone/home pages cannot receive a final content approval from this worker alone; owner approval remains required. If Editor `exact_replacements` are present, Reviewer must keep owner approval required and cannot advance them directly to `apply-preview`.

`llm-worker-chain` runs the no-write live LLM sequence in one command:

1. `llm-scout`
2. `llm-editor`
3. `llm-reviewer`

After the owner records `approved_for_chain`, use:

```bash
python3 automation/pipeline.py llm-worker-chain --from-decision automation/reports/llm-topic-decision-<topic_id>.json --provider openai --json
```

This creates replay Scout artifacts from the saved decision snapshot instead of rerunning live Scout. The handoff blocks unless the decision artifact is `approved_for_chain`, and it still does not approve public copy, patch specs, backlog mutation, manifests, PRs, or deployment.

It writes:

- `automation/reports/llm-worker-chain-<topic_id>.json`
- `automation/reports/llm-worker-chain-<topic_id>.md`

The chain summary references each stage's request/result/markdown artifacts. If any stage fails or is blocked, the chain writes a blocked summary and stops before later stages. Live Scout handoffs advance only `ready_for_chain` opportunities: `update_existing`, `create_new`, or `consolidate` with non-low priority. Monitor-only, reject, or low-priority selected topics are blocked before Editor/Reviewer. It must not generate final public page copy, patch specs, backlog entries, manifests, content edits, PRs, or production state.

The GitHub Actions wrapper `.github/workflows/llm-worker-chain.yml` runs pending owner-approved handoffs by manual dispatch, after path-limited LLM worker infrastructure pushes, or after committed `llm-topic-decision-*.json` pushes. Decision-triggered runs use `llm-run-approved-handoffs` so they only process committed `approved_for_chain` decision artifacts and skip current completed chain summaries. It is intentionally not scheduled because the workflow uploads artifacts without committing generated reports, so a weekly run could repeatedly process the same approved decision. Manual dispatch can replay one approved `decision_path` directly. It uploads artifacts only; it must not commit generated reports or mutate content.

`llm-review-latest` is a read-only operator view over the latest local `llm-worker-chain-<topic_id>.json` summary. It extracts the Reviewer gate result, owner questions, blocking issues, required checks, and next step without calling an LLM provider.

`llm-intake-latest` is the no-write bridge from LLM owner review to the existing controlled intake/run-plan flow. It reads the latest or specified `llm-worker-chain-<topic_id>.json`, writes:

- `automation/reports/llm-intake-<topic_id>.json`
- `automation/reports/llm-intake-<topic_id>.md`

When owner approval is required, the intake artifact stays `approval_required` until rerun with `--approved-by <name>`. If owner questions are present, `--note` is also required. If the Reviewer used `blocking_issues` for owner-confirmation items, `--resolve-reviewer-blockers` can downgrade them to intake warnings only when `--approved-by` and `--note` are both present. This approval is intake-only: it allows the existing run-plan/proposal flow, but it does not approve public copy, patch specs, backlog mutation, manifest creation, PR creation, deployment, or production publishing. Draft `exact_replacements` may be carried into intake for later run-plan/proposal handling, but they remain proposal-only until the exact public diff is shown and approved.

An approved LLM intake can be passed to the existing run-plan command with:

```bash
python3 automation/pipeline.py worker-run-plan --intake automation/reports/llm-intake-<topic_id>.json --json
python3 automation/pipeline.py worker-run-plan --intake automation/reports/llm-intake-<topic_id>.json --basename llm-worker-run-plan-<topic_id> --json
```

This still does not edit public content, backlog files, manifests, PRs, or production state.

## Shared Inputs

Every worker must treat these files as source-of-truth context:

- `AGENTS.md`
- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/seo_llm_optimization.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`
- `automation/memory/entities.json`
- `automation/memory/release_checklist.md`

Analytics-aware workers may also use:

- `content/gsc/latest-gsc-agent-signals.json`
- `content/bing/latest-bing-agent-signals.json`
- GA4 / LLM referral reports when supplied by a human operator

Existing run-state workers must use:

- `automation/manifests/<run_id>.json`
- `automation/reports/<run_id>.*.md`

## Shared Guardrails

All workers must follow these rules:

- No production publishing.
- No direct content edits unless the worker is a later approved apply worker.
- Generic content application is limited to `safe_exact_replace`: exact
  owner-approved `exact_old` -> `exact_new` snippets in one non-generated HTML
  file. Workers must not treat summaries, desired-after notes, or LLM prose as
  applyable content.
- If a future worker proposes exact public copy, it may pass exact
  `exact_old` and `exact_new` strings into Patch Spec v1. That still creates
  only a proposal; owner approval is required before `apply-approved`.
- LLM-originated `exact_old` values must be copied from deterministic
  `current_page_snapshot.source_snippets` or otherwise match the current target
  HTML exactly once; nonliteral or ambiguous candidates are blocked before
  intake.
- Approved intake/run-plan artifacts may carry exact snippets as
  `plan.exact_replacements`. This is a handoff format, not content approval.
- No live LLM provider calls unless they go through the fail-closed adapter and have explicit configuration.
- No new page unless the page has a distinct user job and a clear cluster route.
- No generated research branch edits through generated HTML; use JSON source + generator.
- Research proposals must not imply that Field Research is required before UST/T10; after Peace Shield/Urgent Rescue, treat the path as a goal-based decision between shortest practical UST/T10 progression and the badge-heavy Siege to Seize/Field Research deep-combat route.
- No updates to archived Reddit/news experiments unless explicitly requested.
- No contradiction of canonical claims.
- No keyword-stuffing or thin intent pages.
- No generic AI-guide prose that restates the topic without concrete player utility.
- No mass-produced trust/freshness boilerplate; trust context should be page-specific when possible.
- No template drift from existing page families.
- No autonomous edits to cornerstone pages without human approval.
- No accidental snippet or AI-search exclusion on public guide pages.
- No `FAQPage` schema unless the FAQ is visible, useful, and specific to the page.
- No sitemap `lastmod` churn for cosmetic-only changes.

Future LLM-assisted workers must preserve public guide eligibility for search and answer features:

- crawlable HTML
- indexable page
- snippet-eligible first-screen answer
- visible textual answer
- descriptive internal links
- structured data that matches visible content

Future LLM-assisted workers must also prove human utility before any content proposal:

- identify the exact player problem
- compare against the existing page or cluster owner
- explain why the proposal is not a duplicate or thin variation
- name the concrete value added: cost, timing, UI path, route, threshold, mistake, exception, or decision rule
- list any claims that need human confirmation before publication
- avoid broad language like “ultimate”, “comprehensive”, “game changer”, or “maximize” unless the supporting page context makes the claim specific and defensible

## Scout Contract

### Current Worker

The first no-write implementation lives at:

```bash
python3 automation/workers/scout.py --json
```

It reads `content/gsc/latest-gsc-agent-signals.json` by default and can also read Bing signals with `--signals content/bing/latest-bing-agent-signals.json`. It writes:

- `automation/reports/scout-topic-proposals.json`
- `automation/reports/scout-topic-proposals.md`

This worker does not mutate content, manifests, or `topic_backlog.csv`.

### Job

Find candidate topics, updates, gaps, and optimization opportunities.

Scout answers:

- What opportunity exists?
- Which existing page or cluster owns it?
- Is it an update, new page, consolidation, or no-op?
- What evidence supports it?
- What risks or conflicts exist?

Scout must not write page copy or patch specs.

### Inputs

Required:

- site memory files
- `content_index.json`
- `topic_backlog.csv`

Use when available:

- `content/gsc/latest-gsc-agent-signals.json`
- `content/bing/latest-bing-agent-signals.json`
- current sitemap/search-index state
- human-supplied notes or screenshots

### Output

Scout outputs a list of `topic_proposal` records.

Required fields:

```json
{
  "topic_id": "stable-kebab-id",
  "title": "Human-readable topic title",
  "cluster": "Research",
  "recommended_action": "update_existing",
  "archetype_suggestion": "support-guide",
  "target_page_or_slug": "example.html",
  "source_type": "analytics",
  "source_reference": "GSC: query family or supplied evidence",
  "confidence": "medium",
  "priority": "high",
  "risk_level": "medium",
  "evidence": [
    "Specific query/page signal, user note, or content gap"
  ],
  "site_fit": {
    "primary_user_job": "Exact user problem this would solve",
    "cluster_owner": "Existing hub/support/atlas owner",
    "expected_internal_route": ["index.html", "cluster-hub.html", "target.html"],
    "archetype_reason": "Why this page family fits"
  },
  "human_utility": {
    "player_problem": "The real player question or pain point",
    "existing_page_compared": "The current page or cluster this was checked against",
    "new_value_added": ["Exact utility this proposal adds beyond rewording"],
    "why_not_duplicate": "Why this should be an update/new page instead of no-op",
    "evidence_basis": ["GSC signal, supplied source, in-game observation, or site memory basis"],
    "claims_needing_human_confirmation": ["Claims that should not be published without owner review"]
  },
  "constraints": [
    "Canonical claims or template constraints that matter"
  ],
  "reject_if": [
    "Conditions that should block the topic"
  ]
}
```

### Required Classifications

`recommended_action` must be one of:

- `update_existing`
- `create_new`
- `consolidate`
- `monitor`
- `reject`

`source_type` must be one of:

- `analytics`
- `research`
- `product`
- `human_request`
- `technical_audit`

### Scout Acceptance Criteria

A Scout proposal is acceptable only if it:

- maps to a real cluster or proposes a clear cluster owner
- identifies the smallest correct archetype
- explains why the page would help players
- explains the concrete utility added beyond generic rewording
- identifies at least one internal route
- identifies canonical or cannibalization risks
- can be reviewed without opening external context first

## Editor Contract

### Current Worker

The first no-write implementation lives at:

```bash
python3 automation/workers/editor.py --topic-id <topic_id> --json
```

It reads `automation/reports/scout-topic-proposals.json` by default and writes:

- `automation/reports/editor-brief-<topic_id>.json`
- `automation/reports/editor-brief-<topic_id>.md`

This worker does not mutate content, manifests, or `topic_backlog.csv`.

### Job

Turn an approved topic or run manifest into a content/edit brief that fits the current site.

Editor answers:

- What is the page's primary job?
- What exact first-screen answer should the page give?
- What existing template/archetype should it follow?
- Which internal links and cluster routes are required?
- Which claims and terminology must be protected?

Editor must not directly edit production pages in the first worker MVP.

### Inputs

Required:

- one approved `topic_proposal` or backlog item
- run manifest
- target page or closest archetype example
- site memory files
- relevant cluster hub
- one adjacent same-cluster page when role separation matters

### Output

Editor outputs an `editor_brief` artifact.

Required fields:

```json
{
  "run_id": "2026-05-01-example",
  "target_page_or_slug": "example.html",
  "page_role": "support-guide",
  "primary_query_family": "last z example query",
  "primary_user_job": "What the visitor needs to do or decide",
  "first_screen_answer": "Concise answer-first guidance",
  "template_reference": "closest-existing-template.html",
  "required_sections": [
    "Section names or content blocks that should exist"
  ],
  "internal_links": {
    "upstream": ["cluster-hub.html"],
    "downstream": ["exact-support-page.html"],
    "lateral": ["related-page.html"]
  },
  "protected_claims": [
    "canonical_claim_id"
  ],
  "do_not_change": [
    "Scope, template, or cluster boundaries that must stay stable"
  ],
  "acceptance_checks": [
    "python3 scripts/prepublish_check.py",
    "python3 automation/pipeline.py checks --strict --manifest <run_id>"
  ]
}
```

### Editor Acceptance Criteria

An Editor brief is acceptable only if it:

- preserves the chosen archetype
- includes an answer-first first-screen plan
- routes the page into its cluster
- protects canonical claims
- avoids duplicate intent
- identifies the exact files that must be read before any patch plan

## Reviewer Contract

### Current Worker

The first no-write implementation lives at:

```bash
python3 automation/workers/reviewer.py --topic-id <topic_id> --json
```

It reads `automation/reports/editor-brief-<topic_id>.json` by default, checks the related Scout proposal from `automation/reports/scout-topic-proposals.json`, and writes:

- `automation/reports/worker-review-<topic_id>.json`
- `automation/reports/worker-review-<topic_id>.md`

This worker does not mutate content, manifests, or `topic_backlog.csv`.

### Job

Review Scout proposals, Editor briefs, and future patch specs for site fit, risk, and readiness.

Reviewer answers:

- Does this match the site mission?
- Does it fit an existing cluster and page role?
- Does it risk cannibalization or duplicate intent?
- Does it contradict canonical claims?
- Does it preserve templates and navigation?
- Is it safe to proceed to proposal, approval, or apply?

Reviewer must not rewrite the brief into a different content plan without flagging the reason.

### Inputs

Required:

- Scout proposal or Editor brief
- run manifest
- canonical claims
- content index
- relevant cluster pages
- deterministic check results when available

### Output

Reviewer outputs a `worker_review` record.

Required fields:

```json
{
  "verdict": "needs_human_review",
  "risk_level": "medium",
  "approved_next_stage": "brief",
  "blocking_issues": [
    {
      "severity": "high",
      "issue": "Specific conflict or missing requirement",
      "required_fix": "Concrete correction"
    }
  ],
  "warnings": [
    "Non-blocking issue to keep visible"
  ],
  "required_context_before_edit": [
    "specific-file.html",
    "automation/memory/canonical_claims.json"
  ],
  "required_checks": [
    "python3 scripts/prepublish_check.py",
    "python3 automation/pipeline.py checks --strict --manifest <run_id>"
  ],
  "human_approval_required": true
}
```

### Reviewer Verdicts

`verdict` must be one of:

- `pass`
- `needs_human_review`
- `revise`
- `reject`

`approved_next_stage` must be one of:

- `none`
- `plan`
- `brief`
- `patch_plan`
- `proposal`
- `approval`
- `apply_preview`

## Human Gate

Human approval is required before:

- creating a new indexable page
- changing a cornerstone guide
- changing canonical claims
- applying any patch spec to content
- opening a PR
- merging or deploying

The system may prepare artifacts before approval. It must not publish autonomously.

## Current Implementation Milestone

The current implementation is deterministic and no-write:

1. `Scout` reads `content/gsc/latest-gsc-agent-signals.json` by default, or Bing agent signals when explicitly passed with `--signals`.
2. `Scout` produces `topic_proposal` records into review artifacts.
3. `llm-scout` can review deterministic GSC/Bing proposals through the fail-closed LLM adapter and produce JSON/markdown opportunity review artifacts.
4. `llm-candidate-refresh` can run LLM Scout plus topic discovery in one scheduled no-write candidate generation step.
5. `llm-topic-discovery` converts selected and monitored LLM Scout opportunities into backlog-shaped owner-review proposals.
6. `llm-topic-decision` records whether each discovered topic is `approved_for_chain`, `monitor`, or `rejected`.
7. `llm-editor` can turn one selected LLM Scout opportunity into a no-copy planning brief through the fail-closed LLM adapter.
8. `llm-reviewer` can gate one LLM Editor planning brief for duplicate intent, cluster fit, canonical claims, template safety, owner questions, and readiness.
9. `llm-worker-chain` can run the live no-write LLM Scout -> Editor -> Reviewer sequence and produce one compact owner-review summary.
10. `Editor` turns one proposal into an `editor_brief` artifact.
11. `Reviewer` gates the brief for site fit, risk, context, canonical claims, and next-stage readiness.
11. Operators decide which reviewed proposals become backlog items or patch-plan work.
12. An approved run-plan may create a `planned` manifest through the manifest writer.

This keeps discovery useful without letting analytics noise become content churn.
