# External Scout - 2026-05-14T10:35:57Z

## Outcome

- State: `external_scout_ready`
- Registry: `automation/memory/source_registry.json`
- Included sources: `11`
- Candidate proposals: `10`
- Source query tasks: `10`
- Proposed sources awaiting owner review: `3`
- Allows content edit: `false`
- Allows backlog mutation: `false`
- Allows manifest mutation: `false`
- Allows PR/deploy: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Source Review Queue

### lastzsurvivalshooter-guides

- Name: LastZSurvivalShooter.com player guides
- Base URL: `https://lastzsurvivalshooter.com`
- Trust level: `low`
- Notes: Unofficial player-guide site. Useful for seeing what players write guides about, but not trusted enough for mechanic claims without stronger verification.

### gamestratwiki-last-z-guides

- Name: GameStratWiki Last Z guides
- Base URL: `https://www.gamestratwiki.com`
- Trust level: `low`
- Notes: General guide site. Useful for topic discovery and SERP landscape only; claims need stronger cross-validation.

### earnne-last-z-codes

- Name: Earnne Last Z codes tracker
- Base URL: `https://earnne.com`
- Trust level: `low`
- Notes: Codes tracker. Potentially useful for discovering code-related search competition, but redemption-flow claims may conflict with this site's canonical Gift Center guidance.

## Candidate Proposals

### external-gift-center-official-flow-validation

- Title: External source opportunity: official Gift Center and store flow validation
- Source: `official-functap-store: https://www.last-z.com`
- Decision hint: `update_existing`
- Target: `gift-center-uid.html`
- Priority: `high`
- Risk: `medium`
- Cross-validation: `owner_approved_source_needs_live_check`

Evidence:

- Official service domain is the strongest source for Gift Center routing and redeem/store flow validation.
- External source URL recorded for later manual verification.

Claims to verify:

- gift-center-only-redeem-flow
- uid-required-for-gift-center

### external-hq-and-progression-reference-cross-check

- Title: External source opportunity: HQ and progression requirement cross-check
- Source: `lastzwiki-reference: https://lastzwiki.com`
- Decision hint: `update_existing`
- Target: `hq.html`
- Priority: `high`
- Risk: `high`
- Cross-validation: `needs_second_source_or_owner_check`

Evidence:

- Owner-approved wiki/reference source can reveal HQ and progression planning gaps.
- External source URL recorded for later manual verification.

Claims to verify:

- hq_requirements
- hq_resource_costs
- hq31_35_progression

### external-research-costs-external-cross-check

- Title: External source opportunity: research cost and branch coverage cross-check
- Source: `stresswar-lastz-reference: https://lastz.stresswar.com`
- Decision hint: `update_existing`
- Target: `research-costs.html`
- Priority: `high`
- Risk: `high`
- Cross-validation: `needs_second_source_or_data_file_check`

Evidence:

- Owner-approved research reference source can reveal branch coverage gaps and cost/name drift.
- External source URL recorded for later manual verification.

Claims to verify:

- research_branch_costs
- research_branch_unlocks
- t10_path_order

### external-gear-guide-cross-check

- Title: External source opportunity: gear guide coverage cross-check
- Source: `packsify-last-z-gear-guide: https://www.packsify.com`
- Decision hint: `update_existing`
- Target: `gear.html`
- Priority: `high`
- Risk: `medium`
- Cross-validation: `needs_second_source`

Evidence:

- Owner-approved gear guide can reveal equipment topics or terminology to cross-check.
- External source URL recorded for later manual verification.

Claims to verify:

- gear_upgrade_order
- equipment_terms
- gear_materials

### external-calculator-and-tool-gap-review

- Title: External source opportunity: calculator and planning-tool gap review
- Source: `lastz-command-center-one: https://lastz-command-center-one.vercel.app`
- Decision hint: `monitor`
- Target: `index.html`
- Priority: `medium`
- Risk: `medium`
- Cross-validation: `needs_owner_product_decision`

Evidence:

- Owner-approved community tool may reveal calculator-style jobs not covered by static guides.
- External source URL recorded for later manual verification.

Claims to verify:

- tool_gap
- calculator_player_job

### external-events-and-season-source-cross-check

- Title: External source opportunity: event and season coverage cross-check
- Source: `last-z-wiki-reference: https://www.last-z.wiki`
- Decision hint: `update_existing`
- Target: `events.html`
- Priority: `medium`
- Risk: `high`
- Cross-validation: `needs_second_source`

Evidence:

- Reference pages may surface event or season naming differences that need validation against canonical site memory.
- External source URL recorded for later manual verification.

Claims to verify:

- event_names
- event_rotation
- season_2_winter_vs_desert

### external-general-guide-gap-cross-check

- Title: External source opportunity: general guide gap cross-check
- Source: `mmediamreza-last-z-reference: https://mmediamreza.com`
- Decision hint: `monitor`
- Target: `index.html`
- Priority: `medium`
- Risk: `medium`
- Cross-validation: `needs_source_triage`

Evidence:

- Owner-approved medium-trust source can be used to discover guide topics that need mapping to existing clusters.
- External source URL recorded for later manual verification.

Claims to verify:

- new_topic_fit
- duplicate_intent_risk

### external-hero-and-event-entity-cross-check

- Title: External source opportunity: Fandom entity and event cross-check
- Source: `lastz-fandom-reference: https://lastz.fandom.com`
- Decision hint: `update_existing`
- Target: `heroes.html`
- Priority: `medium`
- Risk: `high`
- Cross-validation: `needs_second_source`

Evidence:

- Owner-approved Fandom source can surface alternate naming or missing entities for review.
- External source URL recorded for later manual verification.

Claims to verify:

- entity_aliases
- hero_names
- event_names

### external-hero-entity-coverage-cross-check

- Title: External source opportunity: hero roster and entity coverage cross-check
- Source: `fandom-last-z-wiki: https://last-z-survival-shooter.fandom.com`
- Decision hint: `update_existing`
- Target: `heroes.html`
- Priority: `medium`
- Risk: `high`
- Cross-validation: `needs_second_source`

Evidence:

- Community wiki can surface hero/entity names that need comparison against entities.json and current hero pages.
- External source URL recorded for later manual verification.

Claims to verify:

- hero_entity_names
- season_hero_mapping
- hero_tier_claims

### external-official-store-metadata-cross-check

- Title: External source opportunity: official app metadata and update-cadence cross-check
- Source: `official-google-play: https://play.google.com`
- Decision hint: `monitor`
- Target: `about.html`
- Priority: `medium`
- Risk: `medium`
- Cross-validation: `needs_second_source`

Evidence:

- Official store listings can validate app identity, broad feature framing, and update cadence but not detailed mechanics.
- External source URL recorded for later manual verification.

Claims to verify:

- official_app_identity
- store_listing_metadata

## Source Query Tasks

- `official-google-play-query-1` (high): site:play.google.com/store/apps/details Last Z Survival Shooter
- `official-apple-app-store-query-1` (high): site:apps.apple.com Last Z Survival Shooter
- `official-functap-store-query-1` (high): site:last-z.com giftCenter Last Z
- `fandom-last-z-wiki-query-1` (medium): site:last-z-survival-shooter.fandom.com Last Z heroes research events
- `lastzwiki-reference-query-1` (high): site:lastzwiki.com/en Last Z guide heroes research
- `last-z-wiki-reference-query-1` (medium): site:last-z.wiki Last Z heroes events research cost
- `lastz-command-center-one-query-1` (high): site:lastz-command-center-one.vercel.app Last Z
- `lastz-fandom-reference-query-1` (high): site:lastz.fandom.com Last Z heroes research events
- `packsify-last-z-gear-guide-query-1` (medium): site:packsify.com/blogs/last-z-gear-guide-how-to-use-and-upgrade-equipment Last Z gear guide
- `mmediamreza-last-z-reference-query-1` (medium): site:mmediamreza.com Last Z Survival Shooter

## Next Actions

- Approve or reject proposed sources before using them in scheduled discovery.
- Run approved source_query_tasks through a future search worker before converting them into public-facing claims.
- Pass this JSON to llm-scout with --external-proposals when candidate_proposals are ready.
- Public content edits still require exact proposed text, owner approval, apply-preview, apply-approved, and strict QA.
