# LLM Topic Decision - research-gsc-opportunity

## Decision

- State: `decision_recorded`
- Decision: `approved_for_chain`
- Decided by: `oleg`
- Source discovery: `automation/reports/llm-candidate-refresh-live/llm-candidate-refresh-topic-discovery.json`
- Source decision: ``
- Allows worker chain: `true`
- Allows content edit: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

Decision note:

Owner approved no-write LLM worker chain for research opportunity only.

## Topic Snapshot

- Title: GSC opportunity review: Last Z Research Guide — Best Research Order, Peace Shield, and T10 Path
- Target: `research.html`
- Cluster: `Research`
- Action: `update_existing`
- Priority: `high`
- Risk: `high`
- Status at discovery: `candidate`

Rationale:

research.html shows meaningful impressions but middling CTR, plus a rising research priority query. This suggests the page likely needs clearer positioning of order, scope, and progression value rather than new content.

## Next Actions

- Run the no-write LLM worker chain from this saved decision: python3 automation/pipeline.py llm-worker-chain --from-decision automation/reports/llm-topic-decision-research-gsc-opportunity.json --provider openai --json
- Review the generated LLM Reviewer gate before any intake, run-plan, or public content proposal.
- Public content still requires exact text/spec proposal, explicit owner approval, and strict checks.
