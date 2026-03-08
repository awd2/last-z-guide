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

- rebuilds `sitemap.xml`
- rebuilds `search-index.json` while preserving existing titles, categories, descriptions, and keywords when they already exist

### Individual scripts

```bash
python3 scripts/audit_site.py
python3 scripts/check_site_indexing.py
python3 scripts/check_site_indexing.py --fix
```

## Notes

- No CI or deploy changes are required.
- The scripts are local safety rails, not a new publishing system.
- `search-index.json` can still be edited manually when you want custom wording or keywords.
