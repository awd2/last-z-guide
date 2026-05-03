# Gift Center / Codes Trust Block Proposal

Scope:

- `codes.html`
- `gift-center-uid.html`
- `redeem-code-not-working.html`

Purpose:

- Replace generic trust/disclaimer wording with page-specific review basis.
- Preserve the fixed Gift Center cluster roles:
  - `codes.html` = codes hub
  - `gift-center-uid.html` = setup
  - `redeem-code-not-working.html` = troubleshooting
- Keep canonical redemption claims consistent:
  - redeem through the official Gift Center website, not inside the game client
  - UID path: Avatar -> Settings -> Copy ID
  - rewards are delivered through mailbox

## Proposed Copy

### codes.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for code availability and Gift Center flow:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> official Gift Center redemption behavior, UID requirements, mailbox reward delivery, and the linked setup and troubleshooting guides.</li>
                <li><strong>Changes to watch:</strong> code expiry, already-used status, campaign availability, reward contents, and temporary Gift Center outages can change faster than normal guide mechanics.</li>
            </ul>
        </section>

        <section class="disclaimer">
            <p>This page is for finding current Last Z codes and redeeming them through the official Gift Center. Always paste your UID directly from the game, check the live Gift Center response, and confirm rewards in your in-game mailbox.</p>
        </section>
```

### gift-center-uid.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for UID setup and Gift Center login flow:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> the official Gift Center flow, the in-game UID path (Avatar -> Settings -> Copy ID), mobile browser redemption, mailbox delivery, and the related codes and troubleshooting pages.</li>
                <li><strong>Changes to watch:</strong> Gift Center page availability, login labels, UID copy path, browser behavior, and mailbox timing may shift after game or web updates.</li>
            </ul>
        </section>

        <section class="disclaimer">
            <p>Use this setup guide before redeeming Last Z codes. Copy your UID from the game instead of typing it manually, redeem through the official Gift Center, and check your mailbox after a successful submission.</p>
        </section>
```

### redeem-code-not-working.html

```html
        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for code troubleshooting and Gift Center errors:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> common failed-redemption causes, wrong UID entry, expired or already-used codes, official Gift Center behavior, mailbox delays, and the linked setup and codes pages.</li>
                <li><strong>Changes to watch:</strong> error wording, code status, account or server eligibility, reward delays, and temporary Gift Center outages can change without notice.</li>
            </ul>
        </section>

        <section class="disclaimer">
            <p>Use this checklist before retrying a failed Last Z code. Verify the official Gift Center is loading, copy your UID directly from the game, match the code text exactly, and allow for mailbox delay after a successful redemption.</p>
        </section>
```

## Not Included

- `news-preview.html` remains excluded from modernization and user-facing optimization.
- No changes are proposed for generated research branch pages in this batch.
- No changes are proposed to navigation, sitemap, schema, or page roles.

## Implementation Path After Approval

1. Update `scripts/sync_verification_blocks.py` with these three page-specific block rules.
2. Regenerate/repair page blocks with `python3 scripts/sync_verification_blocks.py`.
3. Run:
   - `python3 scripts/prepublish_check.py --fix`
   - `python3 scripts/prepublish_check.py`
   - `python3 automation/pipeline.py checks`
   - `python3 automation/pipeline.py checks --strict`
   - `python3 automation/pipeline.py content-voice --top 40`
4. Review the exact diff before commit.
