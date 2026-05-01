# Last Z Guides

Static guide site for `lastzguides.com`.

## Project Instructions

Root [AGENTS.md](/Users/oleg/Projects/claude-playground/AGENTS.md) is the main repo-level instruction file for this project.

Use it as the default operating manual for both:

- agent-style workflows
- ordinary chat requests about this repository

It does not override platform or developer instructions, but it is the default local source for:

- project rules
- file-reading flow
- cluster roles
- canonical content constraints
- SEO / LLM optimization rules
- safe editing and publishing behavior

## Local workflow

The publish flow stays the same:

1. Edit pages locally in VS Code.
2. Run the local checks when needed.
3. Commit and `Sync Changes`.

## Local automation

These scripts are meant to be run locally before publishing. I will also use them automatically during larger edit passes.

### One-command check

```bash
python3 scripts/prepublish_check.py
```

What it does:

- checks that `sitemap.xml` and `search-index.json` match the current HTML pages
- audits HTML pages for common issues like missing metadata, broken markers, broken `<title>` content, canonical mismatches, and likely duplicate paragraphs

### Auto-fix indexing files

```bash
python3 scripts/prepublish_check.py --fix
```

What `--fix` does:

- syncs `dateModified` / `article:modified_time` from real file mtimes
- injects or refreshes sitewide `Organization` JSON-LD
- syncs verification blocks across content pages
- rebuilds `sitemap.xml`
- rebuilds `search-index.json` while preserving existing titles, categories, descriptions, and keywords when they already exist

### Individual scripts

```bash
python3 scripts/audit_site.py
python3 scripts/check_site_indexing.py
python3 scripts/check_site_indexing.py --fix
python3 scripts/sync_structured_data.py
python3 scripts/sync_verification_blocks.py
```

## Automation MVP

The repo now also contains a separate `automation/` layer for a controlled editorial automation MVP.

This is **not** an autonomous publishing system. It is a draft-first planning and review foundation:

- explicit site memory
- structured backlog
- deterministic QA helpers
- run manifests
- human-readable review bundles
- editor briefs
- proposal approval records
- no-write apply previews
- controlled apply results
- closeout reports

Root `README.md` only gives the short project-level view.
Use [automation/README.md](/Users/oleg/Projects/claude-playground/automation/README.md) as the full operator reference for:

- CLI commands
- lifecycle states
- manifests and report artifacts
- baseline vs strict automation checks

Most useful entrypoints:

```bash
python3 automation/pipeline.py checks
python3 automation/pipeline.py checks --strict
python3 automation/pipeline.py status
python3 automation/pipeline.py list
python3 automation/pipeline.py backlog-sync
python3 automation/pipeline.py open-topic <topic_id>
python3 automation/pipeline.py open-run <run_id>
python3 automation/pipeline.py recent-runs
python3 automation/pipeline.py propose <run_id>
python3 automation/pipeline.py approval <run_id> --state approved --all --dry-run
python3 automation/pipeline.py apply-preview <run_id>
python3 automation/pipeline.py apply-approved <run_id>
python3 automation/pipeline.py close-run <run_id>
```

`checks` includes:

- content index memory sync
- orphan / weak-cluster coverage
- cluster-link expectations
- site structure consistency for shared navigation, guide template signals, and generated research branch boundaries
- SEO/LLM alignment warnings
- basic cannibalization warnings

`checks --strict` turns weak-cluster and SEO/LLM warnings into a failing gate. Site structure issues are always hard failures.

Automation artifacts live in:

- `automation/manifests/<run_id>.json`
- `automation/reports/<run_id>.md`
- `automation/reports/<run_id>.brief.md`
- `automation/reports/<run_id>.patch.md`
- `automation/reports/<run_id>.proposed.md`
- `automation/reports/<run_id>.apply-preview.md`
- `automation/reports/<run_id>.apply-result.md`
- `automation/reports/<run_id>.closed.md`

## Notes

- No CI or deploy changes are required.
- The scripts are local safety rails, not a new publishing system.
- `search-index.json` can still be edited manually when you want custom wording or keywords.

## LLM referral observability

The site tracks a lightweight `llm_referral_session` event when a visit appears to come from:

- `utm_source=chatgpt.com`
- `chatgpt.com`
- `perplexity.ai`
- `copilot.microsoft.com`
- `bing.com`
- `grok.com`
- `x.com`

Suggested GA4 views:

- segment or exploration filtered to `event_name = llm_referral_session`
- breakdown by the event parameter `llm_source`
- breakdown by the event parameter `llm_channel`
- landing pages filtered by the event parameter `landing_page`
- optional secondary breakdown by `referrer_host`

Suggested GA4 setup:

- register `llm_source`, `llm_source_type`, `llm_channel`, `landing_page`, and `referrer_host` as event-scoped custom dimensions
- build an exploration filtered to `event_name = llm_referral_session`
- compare `chatgpt`, `perplexity`, `copilot`, `bing`, and `grok` over time
- use `llm_channel` to separate true LLM traffic from Bing/search-surface traffic

Local reporting helper:

```bash
python3 automation/reports/llm_referral_report.py path/to/ga4-llm-referrals.csv --output automation/reports/llm-referrals.md
```

The helper expects a GA4 CSV export with dimensions such as `llm_source`, `llm_channel`, `landing_page`, and `referrer_host`, plus metrics such as `sessions`, `event_count`, or `total_users`. It does not call GA4 directly.

This is meant to answer:

- which pages get LLM referrals
- whether ChatGPT/Perplexity/Copilot traffic is growing
- whether LLM traffic behaves differently from standard search traffic

## llms.txt

The root `llms.txt` file is an optional discovery aid. It is not a substitute for crawlability, structured data, or page quality.
