# LLM Candidate Refresh - 2026-05-18T18:58:28Z

## Overview

- State: `candidate_refresh_ready`
- Provider: `openai`
- Source proposals: 8
- Candidate topics: 0
- Monitor topics: 7
- Topic discovery: `automation/reports/llm-auto-review-queue/llm-auto-review-topic-discovery.md`
- Allows content edit: `false`
- Allows backlog mutation: `false`
- Allows manifest mutation: `false`
- Allows PR/deploy: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Source Signals

- content/gsc/latest-gsc-agent-signals.json
- content/bing/latest-bing-agent-signals.json

## Monitor Topics

- codes-gsc-opportunity
- alliance-duel-gsc-opportunity
- external-gift-center-official-flow-validation
- external-hq-and-progression-reference-cross-check
- external-research-costs-external-cross-check
- external-search-lastz-fandom-reference-full-preparedness-last-z-survival-shooter--4
- external-search-lastz-fandom-reference-heroes-last-z-survival-shooter-wiki-fandom-5

## Stages

### llm_scout

- State: `completed`
- Return code: `0`
- Request: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`
- Markdown: `automation/reports/llm-auto-review-queue/llm-auto-review-scout.md`

### llm_topic_discovery

- State: `topic_discovery_ready`
- Return code: `0`
- Request: ``
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-topic-discovery.json`
- Markdown: `automation/reports/llm-auto-review-queue/llm-auto-review-topic-discovery.md`

## Next Actions

- Review `automation/reports/llm-auto-review-queue/llm-auto-review-topic-discovery.md` before approving any topic.
- Record owner decisions with `python3 automation/pipeline.py llm-topic-decision --topic-id <topic_id> --state monitor|approved_for_chain|rejected --decided-by <name> --json`.
- Only `approved_for_chain` topics may move to the no-write llm-worker-chain stage.
- Public content edits still require exact proposed text, explicit owner approval, apply-preview, apply-approved, and strict QA.
