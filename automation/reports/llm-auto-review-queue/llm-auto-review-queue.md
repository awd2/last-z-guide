# LLM Auto Review Queue - 2026-05-16T19:02:32Z

## Outcome

- State: `completed_with_failures`
- Provider: `openai`
- Candidate topics: `1`
- Queued topics: `1`
- Completed items: `0`
- Failed items: `1`
- Skipped existing: `0`
- Stale existing reruns: `0`
- Required chain contract: `2` `exact-editor-proposals-v2`
- Deferred by limit: `0`
- Candidate refresh: `automation/reports/llm-auto-review-queue/llm-auto-review-candidate-refresh.md`
- Topic discovery: `automation/reports/llm-auto-review-queue/llm-auto-review-topic-discovery.md`
- Allows content edit: `false`
- Allows backlog mutation: `false`
- Allows manifest mutation: `false`
- Allows PR/deploy: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Errors

- LLM Editor stage failed; Reviewer was not run.

## Review Queue

### external-gift-center-official-flow-validation

- Status: `failed`
- Score: `91`
- Target: `gift-center-uid.html`
- Cluster: `Economy`
- Priority: `high`
- Risk: `medium`
- Verdict: `None`
- Owner approval required: `none`
- Chain: `automation/reports/llm-auto-review-queue/llm-worker-chain-external-gift-center-official-flow-validation.md`
- Existing chain rerun: `false`

Score reasons:

- priority:high=45
- confidence:high=20
- risk:medium=8
- action:update_existing=8
- candidate_status=10

## Next Actions

- Review queue_items and open the referenced chain markdown for the best candidate.
- Approve only final public content diffs, not this queue artifact.
- If a queue item is worth drafting, move it through llm-intake-latest and the existing run-plan/proposal lifecycle.
