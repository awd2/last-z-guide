# LLM Candidate Refresh - 2026-05-10T09:57:25Z

## Overview

- State: `candidate_refresh_ready`
- Provider: `openai`
- Source proposals: 8
- Candidate topics: 2
- Monitor topics: 6
- Topic discovery: `automation/reports/llm-candidate-refresh-live/llm-candidate-refresh-topic-discovery.md`
- Allows content edit: `false`
- Allows backlog mutation: `false`
- Allows manifest mutation: `false`
- Allows PR/deploy: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Source Signals

- content/gsc/latest-gsc-agent-signals.json
- content/bing/latest-bing-agent-signals.json

## Candidate Topics

- index-bing-opportunity
- research-gsc-opportunity

## Monitor Topics

- codes-gsc-opportunity
- alliance-duel-gsc-opportunity
- vehicle-modification-cost-gsc-opportunity
- heroes-gsc-opportunity
- hq-gsc-opportunity
- power-guide-gsc-opportunity

## Stages

### llm_scout

- State: `completed`
- Return code: `0`
- Request: `automation/reports/llm-candidate-refresh-live/llm-candidate-refresh-scout-request.json`
- Result: `automation/reports/llm-candidate-refresh-live/llm-candidate-refresh-scout-result.json`
- Markdown: `automation/reports/llm-candidate-refresh-live/llm-candidate-refresh-scout.md`

### llm_topic_discovery

- State: `topic_discovery_ready`
- Return code: `0`
- Request: ``
- Result: `automation/reports/llm-candidate-refresh-live/llm-candidate-refresh-topic-discovery.json`
- Markdown: `automation/reports/llm-candidate-refresh-live/llm-candidate-refresh-topic-discovery.md`

## Next Actions

- Review `automation/reports/llm-candidate-refresh-live/llm-candidate-refresh-topic-discovery.md` before approving any topic.
- Record owner decisions with `python3 automation/pipeline.py llm-topic-decision --topic-id <topic_id> --state monitor|approved_for_chain|rejected --decided-by <name> --json`.
- Only `approved_for_chain` topics may move to the no-write llm-worker-chain stage.
- Public content edits still require exact proposed text, explicit owner approval, apply-preview, apply-approved, and strict QA.
