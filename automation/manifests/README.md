# Run Manifests

This directory defines the state format for future automation runs.

The goal is simple: every non-trivial automation run should leave behind an explicit artifact that says:

- what the run was trying to do
- what inputs it used
- what stage it reached
- what files it changed
- what checks passed or failed
- what a reviewer should look at next

This is the first step toward durable orchestration. It avoids “hidden state in the model”.

## Why manifests exist

Without a manifest, future Scout / Editor / Reviewer flows will have to infer state from:

- repo diffs
- chat history
- loose notes

That is fragile.

With a manifest, a run becomes an explicit object with:

- identity
- status
- risk
- outputs
- QA results

## Current MVP lifecycle

The current automation MVP uses this concrete lifecycle:

- `planned`
- `reviewed`
- `draft_brief_ready`
- `patch_plan_ready`

`patch_plan_ready` is the current stop point. It means the run has a
proposal-only patch plan and now needs human review before any site files are
edited.

Future lifecycle stages may add names such as `drafted`, `qa_passed`,
`ready_for_approval`, `approved`, and `released`, but those are not implemented
states yet.

## Required top-level fields

- `run_id`
  - stable identifier for the run

- `created_at`
  - ISO timestamp

- `run_type`
  - examples:
    - `topic_scan`
    - `update_existing`
    - `new_page`
    - `cluster_pass`

- `status`
  - current lifecycle stage

- `risk_level`
  - `low`, `medium`, or `high`

- `summary`
  - one short explanation of the run

- `inputs`
  - what pages/topics/sources triggered the run

- `plan`
  - what the run intends to create or update

- `artifacts`
  - reports, briefs, or generated files produced by the run

- `changed_files`
  - explicit file list if the run edits the repo

- `checks`
  - deterministic QA results

- `review`
  - reviewer verdict, open questions, and next action

## Usage rule

The orchestrator should treat the manifest as the single run record.

That means:
- update the manifest as the run progresses
- do not hide critical decisions only in logs or prose
- keep the final reviewer summary in the manifest even if a PR body also exists

## Scope for MVP

For the first MVP:
- manifests can be created manually or by simple helper scripts
- one JSON example is enough to lock the schema shape
- no database or external state store is needed

The only goal right now is to establish a durable, explicit state format.
