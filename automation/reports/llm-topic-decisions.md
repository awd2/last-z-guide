# LLM Topic Decisions - 2026-05-05T19:52:52Z

## Overview

- Decisions: 4
- Counts by state: `{"approved_for_chain": 1, "monitor": 3}`
- Topics currently allowed for worker chain: 1
- Topics currently allowed for content edit: 0
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Allowed Worker Chain Topics

- hq-gsc-opportunity

## Decisions

### heroes-gsc-opportunity

- Decision: `monitor`
- Target: `heroes.html`
- Cluster: `Heroes`
- Priority: `high`
- Risk: `high`
- Allows worker chain: `false`
- Allows content edit: `false`
- Artifact: `automation/reports/llm-topic-decision-heroes-gsc-opportunity.json`

Decision note:

Owner scope review plus live LLM Scout: heroes.html is a plausible cornerstone opportunity, but current evidence is thinner than stronger GSC/Bing opportunities and the page already has strong Season 4/faction first-screen coverage. Keep in monitoring until a specific hero, faction, or season query pattern becomes persistent.

Next actions:

- Keep this topic out of content intake for now.
- Reconsider only after materially new GSC/Bing/query evidence or an explicit owner request.
- Do not create public content edits from this topic decision.

### hq-gsc-opportunity

- Decision: `approved_for_chain`
- Target: `hq.html`
- Cluster: `Progression`
- Priority: `low`
- Risk: ``
- Allows worker chain: `true`
- Allows content edit: `false`
- Artifact: `automation/reports/llm-topic-decision-hq-gsc-opportunity.json`

Decision note:

Owner approved this topic for one no-write LLM worker-chain replay only. This does not approve public content edits, patch specs, PRs, or deployment.

Next actions:

- Run the no-write LLM worker chain from this saved decision: python3 automation/pipeline.py llm-worker-chain --from-decision automation/reports/llm-topic-decision-hq-gsc-opportunity.json --provider openai --json
- Review the generated LLM Reviewer gate before any intake, run-plan, or public content proposal.
- Public content still requires exact text/spec proposal, explicit owner approval, and strict checks.

### index-bing-opportunity

- Decision: `monitor`
- Target: `index.html`
- Cluster: `Home`
- Priority: `low`
- Risk: ``
- Allows worker chain: `false`
- Allows content edit: `false`
- Artifact: `automation/reports/llm-topic-decision-index-bing-opportunity.json`

Decision note:

Owner scope review plus live LLM Scout: index.html already works as a broad home-hub with clear routing into progression, research, heroes, events, PvP, and economy. Bing signal is useful, but query data is still broad/sparse and live Scout placed this topic in monitoring. Keep out of content intake until repeated Bing/GSC evidence shows a stable navigation-query pattern or homepage underperformance relative to other hubs.

Next actions:

- Keep this topic out of content intake for now.
- Reconsider only after materially new GSC/Bing/query evidence or an explicit owner request.
- Do not create public content edits from this topic decision.

### research-gsc-opportunity

- Decision: `monitor`
- Target: `research.html`
- Cluster: `Research`
- Priority: `high`
- Risk: `high`
- Allows worker chain: `false`
- Allows content edit: `false`
- Artifact: `automation/reports/llm-topic-decision-research-gsc-opportunity.json`

Decision note:

Owner scope review: current research.html already satisfies the broad GSC opportunity. Keep this topic out of content intake unless materially new query evidence points to a narrow, concrete improvement.

Next actions:

- Keep this topic out of content intake for now.
- Reconsider only after materially new GSC/Bing/query evidence or an explicit owner request.
- Do not create public content edits from this topic decision.
