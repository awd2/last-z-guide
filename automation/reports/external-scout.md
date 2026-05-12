# External Scout - 2026-05-12T19:22:15Z

## Outcome

- State: `source_approval_needed`
- Registry: `automation/memory/source_registry.json`
- Included sources: `0`
- Candidate proposals: `0`
- Proposed sources awaiting owner review: `10`
- Allows content edit: `false`
- Allows backlog mutation: `false`
- Allows manifest mutation: `false`
- Allows PR/deploy: `false`
- Safety: no content, backlog, manifest, PR, or production files were modified.

## Source Review Queue

### official-google-play

- Name: Last Z: Survival Shooter on Google Play
- Base URL: `https://play.google.com`
- Trust level: `high`
- Notes: Official app-store listing. Good for official description, developer identity, app availability, update cadence, and broad feature framing; not enough for detailed mechanics or costs.

### official-apple-app-store

- Name: Last Z: Survival Shooter on Apple App Store
- Base URL: `https://apps.apple.com`
- Trust level: `high`
- Notes: Official iOS listing. Useful for official metadata, version/update context, app category, and broad game framing; not enough for detailed mechanics or costs.

### official-functap-store

- Name: FunTap Last Z store and Gift Center
- Base URL: `https://www.last-z.com`
- Trust level: `high`
- Notes: Official-looking Last Z service domain used for Gift Center and store flow validation. Use only to verify official redeem/store routing, not game mechanics.

### stresswar-lastz-reference

- Name: StressWar Last Z reference pages
- Base URL: `https://lastz.stresswar.com`
- Trust level: `medium`
- Notes: Previously used as a research-reference source. Keep proposed until the owner explicitly approves it for automated external discovery.

### fandom-last-z-wiki

- Name: Last Z: Survival Shooter Wiki on Fandom
- Base URL: `https://last-z-survival-shooter.fandom.com`
- Trust level: `medium`
- Notes: Community wiki. Useful for entity/topic discovery and rough cross-checking. Public claims must be verified elsewhere because wiki pages can be incomplete, outdated, or user-edited.

### lastzwiki-reference

- Name: LastZWiki.com reference pages
- Base URL: `https://lastzwiki.com`
- Trust level: `medium`
- Notes: Unofficial reference/wiki-style site. Useful for topic and entity discovery; every mechanic/cost claim needs independent verification.

### last-z-wiki-reference

- Name: last-z.wiki reference pages
- Base URL: `https://www.last-z.wiki`
- Trust level: `medium`
- Notes: Unofficial wiki/reference site with apparent data-oriented pages. Use as a discovery and second-source candidate only; verify exact mechanics before public copy.

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

- None

## Next Actions

- Approve or reject proposed sources before using them in scheduled discovery.
- Add explicit topic_seeds or approved search tooling before expecting external topic candidates.
- Pass this JSON to llm-scout with --external-proposals when candidate_proposals are ready.
- Public content edits still require exact proposed text, owner approval, apply-preview, apply-approved, and strict QA.
