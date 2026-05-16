# External Search Collect - 2026-05-16T17:27:14Z

## Outcome

- State: `search_collected`
- Provider: `openai`
- Evidence Refresh: `automation/reports/llm-auto-review-queue/external-evidence-refresh.json`
- Search tasks: `6`
- Searched: `6`
- Failed: `0`
- Candidate proposals: `9`
- Allows content edit: `false`
- Allows backlog mutation: `false`
- Allows manifest mutation: `false`
- Allows PR/deploy: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Candidate Proposals

### external-search-lastzwiki-reference-heroes-last-z-wiki-tier-list-stats-complet-1

- Title: External search opportunity: Heroes - Last Z Wiki | Tier List, Stats & Complete Character Guide 2026
- Action: `update_existing`
- Target: `heroes.html`
- Cluster: `Heroes`
- Score: `82`
- Source: `External search: site:lastzwiki.com/en Last Z guide heroes research`
- URL: `https://lastzwiki.com/en/heroes.html`
- Mapping: `content_index_token_match`
- Public claim ready: `false`

### external-search-lastzwiki-reference-laboratory-badges-in-last-z-complete-resea-2

- Title: External search opportunity: Laboratory Badges in Last Z - Complete Research Guide | Last Z Wiki
- Action: `update_existing`
- Target: `heroes.html`
- Cluster: `Heroes`
- Score: `82`
- Source: `External search: site:lastzwiki.com/en Last Z guide heroes research`
- URL: `https://lastzwiki.com/en/laboratory.html`
- Mapping: `content_index_token_match`
- Public claim ready: `false`

### external-search-lastzwiki-reference-beginner-s-guide-last-z-wiki-how-to-start--3

- Title: External search opportunity: Beginner's Guide - Last Z Wiki | How to Start & Essential Tips 2026
- Action: `monitor`
- Target: `start.html`
- Cluster: `Progression`
- Score: `54`
- Source: `External search: site:lastzwiki.com/en Last Z guide heroes research`
- URL: `https://lastzwiki.com/en/beginner-guide.html`
- Mapping: `content_index_token_match`
- Public claim ready: `false`

### external-search-lastz-fandom-reference-full-preparedness-last-z-survival-shooter--4

- Title: External search opportunity: Full Preparedness | Last Z: Survival Shooter Wiki | Fandom
- Action: `update_existing`
- Target: `events.html`
- Cluster: `Events`
- Score: `82`
- Source: `External search: site:lastz.fandom.com Last Z heroes research events`
- URL: `https://lastz.fandom.com/wiki/Full_Preparedness`
- Mapping: `content_index_token_match`
- Public claim ready: `false`

### external-search-lastz-fandom-reference-heroes-last-z-survival-shooter-wiki-fandom-5

- Title: External search opportunity: Heroes | Last Z: Survival Shooter Wiki | Fandom
- Action: `update_existing`
- Target: `research.html`
- Cluster: `Research`
- Score: `82`
- Source: `External search: site:lastz.fandom.com Last Z heroes research events`
- URL: `https://lastz.fandom.com/wiki/Heroes`
- Mapping: `content_index_token_match`
- Public claim ready: `false`

### external-search-lastz-fandom-reference-event-center-last-z-survival-shooter-wiki--6

- Title: External search opportunity: Event Center | Last Z: Survival Shooter Wiki | Fandom
- Action: `update_existing`
- Target: `events.html`
- Cluster: `Events`
- Score: `82`
- Source: `External search: site:lastz.fandom.com Last Z heroes research events`
- URL: `https://lastz.fandom.com/wiki/Event_Center`
- Mapping: `content_index_token_match`
- Public claim ready: `false`

### external-search-mmediamreza-last-z-reference-shooter-camp-guide-last-z-survival-shooter-7

- Title: External search opportunity: Shooter Camp Guide - | Last Z: Survival Shooter
- Action: `create_new`
- Target: `about.html`
- Cluster: `Site`
- Score: `82`
- Source: `External search: site:mmediamreza.com Last Z Survival Shooter`
- URL: `https://mmediamreza.com/shooter-camp-guide`
- Mapping: `content_index_token_match`
- Public claim ready: `false`

### external-search-mmediamreza-last-z-reference-assaulter-camp-guide-train-faster-gain-pow-8

- Title: External search opportunity: Assaulter Camp Guide - Train Faster & Gain Power - | Last Z: Survival Shooter
- Action: `create_new`
- Target: `power-guide.html`
- Cluster: `Progression`
- Score: `82`
- Source: `External search: site:mmediamreza.com Last Z Survival Shooter`
- URL: `https://mmediamreza.com/en/assaulter-camp-training-guide`
- Mapping: `content_index_token_match`
- Public claim ready: `false`

### external-search-mmediamreza-last-z-reference-last-z-laboratory-guide-tech-research-lab--9

- Title: External search opportunity: Last Z Laboratory Guide: Tech Research & Lab No. 2 Unlocking - | Last Z: Survival Shooter
- Action: `create_new`
- Target: `tech.html`
- Cluster: `Research`
- Score: `82`
- Source: `External search: site:mmediamreza.com Last Z Survival Shooter`
- URL: `https://mmediamreza.com/laboratory`
- Mapping: `content_index_token_match`
- Public claim ready: `false`

## Search Records

### lastzwiki-reference-query-1

- Status: `searched`
- Source: `lastzwiki-reference`
- Query: site:lastzwiki.com/en Last Z guide heroes research
- Results: `3`

### last-z-wiki-reference-query-1

- Status: `searched`
- Source: `last-z-wiki-reference`
- Query: site:last-z.wiki Last Z heroes events research cost
- Results: `0`

### lastz-command-center-one-query-1

- Status: `searched`
- Source: `lastz-command-center-one`
- Query: site:lastz-command-center-one.vercel.app Last Z
- Results: `0`

### lastz-fandom-reference-query-1

- Status: `searched`
- Source: `lastz-fandom-reference`
- Query: site:lastz.fandom.com Last Z heroes research events
- Results: `3`

### packsify-last-z-gear-guide-query-1

- Status: `searched`
- Source: `packsify-last-z-gear-guide`
- Query: site:packsify.com/blogs/last-z-gear-guide-how-to-use-and-upgrade-equipment Last Z gear guide
- Results: `0`

### mmediamreza-last-z-reference-query-1

- Status: `searched`
- Source: `mmediamreza-last-z-reference`
- Query: site:mmediamreza.com Last Z Survival Shooter
- Results: `3`

## Next Actions

- Feed candidate_proposals into LLM Scout as external proposal inputs.
- Treat search results as discovery evidence only, not proof.
- Validate any public claim against canonical memory, a second reliable source, or explicit owner confirmation.
- Public content still requires exact proposed text, owner approval, apply-preview, apply-approved, and strict QA.
