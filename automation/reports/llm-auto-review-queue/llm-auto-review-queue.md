# LLM Auto Review Queue - 2026-05-16T17:32:20Z

## Outcome

- State: `queue_ready`
- Provider: `openai`
- Candidate topics: `2`
- Queued topics: `1`
- Completed items: `1`
- Failed items: `0`
- Skipped existing: `1`
- Deferred by limit: `0`
- Candidate refresh: `automation/reports/llm-auto-review-queue/llm-auto-review-candidate-refresh.md`
- Topic discovery: `automation/reports/llm-auto-review-queue/llm-auto-review-topic-discovery.md`
- Allows content edit: `false`
- Allows backlog mutation: `false`
- Allows manifest mutation: `false`
- Allows PR/deploy: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Review Queue

### external-research-costs-external-cross-check

- Status: `completed`
- Score: `83`
- Target: `research-costs.html`
- Cluster: `Research`
- Priority: `high`
- Risk: `high`
- Verdict: `needs_human_review`
- Owner approval required: `true`
- Chain: `automation/reports/llm-auto-review-queue/llm-worker-chain-external-research-costs-external-cross-check.md`

Score reasons:

- priority:high=45
- confidence:high=20
- risk:high=0
- action:update_existing=8
- candidate_status=10

## Skipped Topics

- `external-hq-and-progression-reference-cross-check`: `skipped_existing_chain`, score `83`, existing `automation/reports/llm-auto-review-queue/llm-worker-chain-external-hq-and-progression-reference-cross-check.json`

## Next Actions

- Review queue_items and open the referenced chain markdown for the best candidate.
- Approve only final public content diffs, not this queue artifact.
- If a queue item is worth drafting, move it through llm-intake-latest and the existing run-plan/proposal lifecycle.
