# LLM Candidate Refresh - 2026-05-18T19:47:18Z

## Overview

- State: `blocked`
- Provider: `openai`
- Source proposals: 8
- Candidate topics: 0
- Monitor topics: 0
- Topic discovery: ``
- Allows content edit: `false`
- Allows backlog mutation: `false`
- Allows manifest mutation: `false`
- Allows PR/deploy: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Source Signals

- content/gsc/latest-gsc-agent-signals.json
- content/bing/latest-bing-agent-signals.json

## Errors

- Selected topic `external-hq-and-progression-reference-cross-check` has monitor/reject decision `monitor`; move it to rejected_or_monitor.

## Stages

### llm_scout

- State: `blocked`
- Return code: `1`
- Request: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-request.json`
- Result: `automation/reports/llm-auto-review-queue/llm-auto-review-scout-result.json`
- Markdown: `automation/reports/llm-auto-review-queue/llm-auto-review-scout.md`

## Next Actions

- Review the Scout errors before rerunning discovery.
- Record owner decisions with `python3 automation/pipeline.py llm-topic-decision --topic-id <topic_id> --state monitor|approved_for_chain|rejected --decided-by <name> --json`.
- Only `approved_for_chain` topics may move to the no-write llm-worker-chain stage.
- Public content edits still require exact proposed text, explicit owner approval, apply-preview, apply-approved, and strict QA.
