# Apply Preview: 2026-04-22-season-alias-clarification

## Overview

- Summary: Update the existing page `start.html` for the `Seasons` cluster using the `support-guide` archetype.
- Status before preview: `approved_for_apply`
- Target: `start.html`
- Approved specs: 1
- Generated at: `2026-04-30T18:38:06Z`

## Safety Rule

- This report is preview-only.
- It does not modify site content.
- It only renders operations with `approval_state=approved`.
- Generated research pages must still be edited through JSON source files and regenerated.

## Source Files

- start.html

## `start.html`

### first_screen_update

- Target output: `start.html`
- Source type: `html_file`
- Generated page: `false`
- Approval state: `approved`
- Preview action: `replace_first_screen_answer`
- Generator command: `None`

Warnings:
- None

Preview patch:
```diff
# Quick Answer callout
- Only the existing Core rule callout appears in `.qa-callouts`.
+ <p class="qa-callout qa-callout--note">
    <span class="qa-icon" aria-hidden="true">i</span>
    <span class="qa-callout-text"><strong>Season naming note:</strong> on newer servers, Season 2 is Winter. Older guides may call Season 2 Desert, but Desert was canceled or skipped for current servers, so follow Winter naming when planning your early timeline.</span>
</p>
```

Validation:
- python3 automation/run_checks.py
- python3 scripts/prepublish_check.py --fix
- python3 scripts/prepublish_check.py
- python3 automation/checks/changed_pages_report.py --manifest <run_id>
- python3 automation/pipeline.py checks

