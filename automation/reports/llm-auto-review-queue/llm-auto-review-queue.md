# LLM Auto Review Queue - 2026-05-12T18:35:58Z

## Outcome

- State: `queue_ready`
- Provider: `openai`
- Candidate topics: `1`
- Queued topics: `1`
- Completed items: `1`
- Failed items: `0`
- Skipped existing: `0`
- Deferred by limit: `0`
- Candidate refresh: `automation/reports/llm-auto-review-queue/llm-auto-review-candidate-refresh.md`
- Topic discovery: `automation/reports/llm-auto-review-queue/llm-auto-review-topic-discovery.md`
- Allows content edit: `false`
- Allows backlog mutation: `false`
- Allows manifest mutation: `false`
- Allows PR/deploy: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Review Queue

### index-gsc-opportunity

- Status: `completed`
- Score: `83`
- Target: `index.html`
- Cluster: `Home`
- Priority: `high`
- Risk: `high`
- Verdict: `needs_human_review`
- Owner approval required: `true`
- Chain: `automation/reports/llm-auto-review-queue/llm-worker-chain-index-gsc-opportunity.md`

Score reasons:

- priority:high=45
- confidence:high=20
- risk:high=0
- action:update_existing=8
- candidate_status=10

## Next Actions

- Review queue_items and open the referenced chain markdown for the best candidate.
- Approve only final public content diffs, not this queue artifact.
- If a queue item is worth drafting, move it through llm-intake-latest and the existing run-plan/proposal lifecycle.
