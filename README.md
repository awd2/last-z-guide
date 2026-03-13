# Last Z Guides

Static guide site for `lastzguides.com`.

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

This is meant to answer:

- which pages get LLM referrals
- whether ChatGPT/Perplexity/Copilot traffic is growing
- whether LLM traffic behaves differently from standard search traffic

## llms.txt

The root `llms.txt` file is an optional discovery aid. It is not a substitute for crawlability, structured data, or page quality.
