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

If the worker review requires human approval, intake remains `approval_required` until rerun with `--approved-by <name>`.

The current no-write run-plan proposal step is:

```bash
python3 automation/workers/intake_to_run.py --topic-id <topic_id> --json
```

It reads `automation/reports/worker-intake-<topic_id>.json` and writes:

- `automation/reports/worker-run-plan-<topic_id>.json`
- `automation/reports/worker-run-plan-<topic_id>.md`

It only produces a `proposed_manifest` when the intake state is `approved_for_intake`; otherwise it emits a blocked artifact.

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
- GA4 / LLM referral reports when supplied by a human operator

Existing run-state workers must use:

- `automation/manifests/<run_id>.json`
- `automation/reports/<run_id>.*.md`

## Shared Guardrails

All workers must follow these rules:

- No production publishing.
- No direct content edits unless the worker is a later approved apply worker.
- No new page unless the page has a distinct user job and a clear cluster route.
- No generated research branch edits through generated HTML; use JSON source + generator.
- No updates to archived Reddit/news experiments unless explicitly requested.
- No contradiction of canonical claims.
- No keyword-stuffing or thin intent pages.
- No template drift from existing page families.
- No autonomous edits to cornerstone pages without human approval.

## Scout Contract

### Current Worker

The first no-write implementation lives at:

```bash
python3 automation/workers/scout.py --json
```

It reads `content/gsc/latest-gsc-agent-signals.json` by default and writes:

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

1. `Scout` reads `content/gsc/latest-gsc-agent-signals.json`.
2. `Scout` produces `topic_proposal` records into review artifacts.
3. `Editor` turns one proposal into an `editor_brief` artifact.
4. `Reviewer` gates the brief for site fit, risk, context, canonical claims, and next-stage readiness.
5. Operators decide which reviewed proposals become backlog items or patch-plan work.

This keeps discovery useful without letting analytics noise become content churn.
