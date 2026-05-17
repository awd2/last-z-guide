# External Evidence Refresh - 2026-05-17T09:36:03Z

## Outcome

- State: `evidence_queue_ready`
- External Scout: `automation/reports/llm-auto-review-queue/external-scout.json`
- Source query tasks: `6`
- URL evidence leads: `11`
- Claim review groups: `22`
- Allows content edit: `false`
- Allows backlog mutation: `false`
- Allows manifest mutation: `false`
- Allows PR/deploy: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Source Query Tasks

- `lastzwiki-reference-query-1` (high): site:lastzwiki.com/en Last Z guide heroes research
- `last-z-wiki-reference-query-1` (medium): site:last-z.wiki Last Z heroes events research cost
- `lastz-command-center-one-query-1` (high): site:lastz-command-center-one.vercel.app Last Z
- `lastz-fandom-reference-query-1` (high): site:lastz.fandom.com Last Z heroes research events
- `packsify-last-z-gear-guide-query-1` (medium): site:packsify.com/blogs/last-z-gear-guide-how-to-use-and-upgrade-equipment Last Z gear guide
- `mmediamreza-last-z-reference-query-1` (medium): site:mmediamreza.com Last Z Survival Shooter

## URL Evidence Leads

### url-external-gift-center-official-flow-validation-1

- Topic: `external-gift-center-official-flow-validation`
- Source: `official-functap-store: https://last-z.com`
- Target: `gift-center-uid.html`
- URL: `https://last-z.com/giftCenter/#/login`
- Cross-validation: `owner_approved_source_needs_live_check`
- Public claim ready: `false`

Claims to verify:
- gift-center-only-redeem-flow
- uid-required-for-gift-center

### url-external-gift-center-official-flow-validation-2

- Topic: `external-gift-center-official-flow-validation`
- Source: `official-functap-store: https://last-z.com`
- Target: `gift-center-uid.html`
- URL: `https://store.last-z.com/#/order`
- Cross-validation: `owner_approved_source_needs_live_check`
- Public claim ready: `false`

Claims to verify:
- gift-center-only-redeem-flow
- uid-required-for-gift-center

### url-external-hq-and-progression-reference-cross-check-1

- Topic: `external-hq-and-progression-reference-cross-check`
- Source: `lastzwiki-reference: https://lastzwiki.com`
- Target: `hq.html`
- URL: `https://lastzwiki.com`
- Cross-validation: `needs_second_source_or_owner_check`
- Public claim ready: `false`

Claims to verify:
- hq_requirements
- hq_resource_costs
- hq31_35_progression

### url-external-research-costs-external-cross-check-1

- Topic: `external-research-costs-external-cross-check`
- Source: `stresswar-lastz-reference: https://lastz.stresswar.com`
- Target: `research-costs.html`
- URL: `https://lastz.stresswar.com/research`
- Cross-validation: `needs_second_source_or_data_file_check`
- Public claim ready: `false`

Claims to verify:
- research_branch_costs
- research_branch_unlocks
- t10_path_order

### url-external-gear-guide-cross-check-1

- Topic: `external-gear-guide-cross-check`
- Source: `packsify-last-z-gear-guide: https://www.packsify.com`
- Target: `gear.html`
- URL: `https://www.packsify.com/blogs/last-z-gear-guide-how-to-use-and-upgrade-equipment`
- Cross-validation: `needs_second_source`
- Public claim ready: `false`

Claims to verify:
- gear_upgrade_order
- equipment_terms
- gear_materials

### url-external-calculator-and-tool-gap-review-1

- Topic: `external-calculator-and-tool-gap-review`
- Source: `lastz-command-center-one: https://lastz-command-center-one.vercel.app`
- Target: `index.html`
- URL: `https://lastz-command-center-one.vercel.app`
- Cross-validation: `needs_owner_product_decision`
- Public claim ready: `false`

Claims to verify:
- tool_gap
- calculator_player_job

### url-external-events-and-season-source-cross-check-1

- Topic: `external-events-and-season-source-cross-check`
- Source: `last-z-wiki-reference: https://www.last-z.wiki`
- Target: `events.html`
- URL: `https://www.last-z.wiki`
- Cross-validation: `needs_second_source`
- Public claim ready: `false`

Claims to verify:
- event_names
- event_rotation
- season_2_winter_vs_desert

### url-external-general-guide-gap-cross-check-1

- Topic: `external-general-guide-gap-cross-check`
- Source: `mmediamreza-last-z-reference: https://mmediamreza.com`
- Target: `index.html`
- URL: `https://mmediamreza.com/en/lastz-news/last_z_survival_shooter_gift_codes_april_2026_always_updated/2026-04-24-19`
- Cross-validation: `needs_source_triage`
- Public claim ready: `false`

Claims to verify:
- new_topic_fit
- duplicate_intent_risk

### url-external-hero-and-event-entity-cross-check-1

- Topic: `external-hero-and-event-entity-cross-check`
- Source: `lastz-fandom-reference: https://lastz.fandom.com`
- Target: `heroes.html`
- URL: `https://lastz.fandom.com/wiki/Event_Center`
- Cross-validation: `needs_second_source`
- Public claim ready: `false`

Claims to verify:
- entity_aliases
- hero_names
- event_names

### url-external-official-ios-store-metadata-cross-check-1

- Topic: `external-official-ios-store-metadata-cross-check`
- Source: `official-apple-app-store: https://apps.apple.com`
- Target: `about.html`
- URL: `https://apps.apple.com/us/app/last-z-survival-shooter/id6503272652`
- Cross-validation: `needs_second_source`
- Public claim ready: `false`

Claims to verify:
- official_app_identity
- store_listing_metadata

### url-external-official-store-metadata-cross-check-1

- Topic: `external-official-store-metadata-cross-check`
- Source: `official-google-play: https://play.google.com`
- Target: `about.html`
- URL: `https://play.google.com/store/apps/details?id=com.readygo.barrel.gp`
- Cross-validation: `needs_second_source`
- Public claim ready: `false`

Claims to verify:
- official_app_identity
- store_listing_metadata

## Claim Review Queue

- `calculator_player_job`: needs_cross_validation; sources=1; public_claim_ready=false
- `duplicate_intent_risk`: needs_cross_validation; sources=1; public_claim_ready=false
- `entity_aliases`: needs_cross_validation; sources=1; public_claim_ready=false
- `equipment_terms`: needs_cross_validation; sources=1; public_claim_ready=false
- `event_names`: has_multiple_source_leads_needs_human_validation; sources=2; public_claim_ready=false
- `event_rotation`: needs_cross_validation; sources=1; public_claim_ready=false
- `gear_materials`: needs_cross_validation; sources=1; public_claim_ready=false
- `gear_upgrade_order`: needs_cross_validation; sources=1; public_claim_ready=false
- `gift-center-only-redeem-flow`: has_multiple_source_leads_needs_human_validation; sources=1; public_claim_ready=false
- `hero_names`: needs_cross_validation; sources=1; public_claim_ready=false
- `hq31_35_progression`: needs_cross_validation; sources=1; public_claim_ready=false
- `hq_requirements`: needs_cross_validation; sources=1; public_claim_ready=false
- `hq_resource_costs`: needs_cross_validation; sources=1; public_claim_ready=false
- `new_topic_fit`: needs_cross_validation; sources=1; public_claim_ready=false
- `official_app_identity`: has_multiple_source_leads_needs_human_validation; sources=2; public_claim_ready=false
- `research_branch_costs`: needs_cross_validation; sources=1; public_claim_ready=false
- `research_branch_unlocks`: needs_cross_validation; sources=1; public_claim_ready=false
- `season_2_winter_vs_desert`: needs_cross_validation; sources=1; public_claim_ready=false
- `store_listing_metadata`: has_multiple_source_leads_needs_human_validation; sources=2; public_claim_ready=false
- `t10_path_order`: needs_cross_validation; sources=1; public_claim_ready=false
- `tool_gap`: needs_cross_validation; sources=1; public_claim_ready=false
- `uid-required-for-gift-center`: has_multiple_source_leads_needs_human_validation; sources=1; public_claim_ready=false

## Next Actions

- Run a future approved search/fetch provider over source_query_tasks and url_evidence_leads.
- Treat collected external evidence as discovery context only until canonical memory and cross-source validation are complete.
- Do not use any single external source as proof for public mechanic, cost, reward, season, or event claims.
- Route verified opportunities back through LLM Scout, Editor, Reviewer, owner approval, proposal, apply-preview, apply-approved, and strict QA.
