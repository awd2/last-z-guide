# Site Style Guide

This is the canonical editorial style guide for `lastzguides.com`.

## Product Positioning

`lastzguides.com` is a practical Last Z guide site, not a general gaming blog.

The site should feel:
- direct
- useful
- operational
- exact-answer-first
- consistent across clusters

It should not feel:
- fluffy
- generic
- over-written
- stuffed for SEO
- inconsistent from page to page

## Tone

Use:
- clear, practical language
- confident recommendations when the evidence is strong
- explicit tradeoffs when the answer depends on player stage
- short paragraphs and tight sectioning

Avoid:
- hype language
- motivational filler
- fake neutrality when there is a better option
- hedging every sentence

## Core Writing Rules

1. **Answer first**
- Every important page should tell the user the main answer near the top.
- The user should not need to scroll through backstory to understand the recommendation.

2. **One page, one primary job**
- A page can support neighboring intents, but it must have one dominant user job.

3. **Prefer exact utility over generic explanation**
- If a page can offer a number, threshold, route, unlock chain, or decision rule, do that.

4. **Keep terminology canonical**
- Reuse the same game terms, event names, and branch names consistently.
- If the game/community naming changes, add a clarification block instead of silently mixing terms.

5. **Use the site’s existing content graph**
- New content must fit into an existing cluster or intentionally create a new one.
- Add related links and hub/support bridges as part of the change, not as an afterthought.

6. **Add real human utility**
- Every new or revised guide section should add at least one concrete player-useful element:
  - an exact number, threshold, cost, timing, UI path, unlock route, decision rule, exception, or common mistake
  - a practical scenario that helps a player decide what to do next
  - a comparison that changes the decision, not just wording that sounds complete
- If a paragraph can be moved to another generic mobile strategy site without changing anything, rewrite it or remove it.

## First-Screen Rules

Every important page should have:
- a strong `title`
- a clear `H1`
- a short `guide-meta` or equivalent freshness/trust signal where appropriate
- a `guide-verified` or equivalent trust block when relevant
- a `Quick Answer` or first-screen answer block for exact-intent pages

The first screen should answer:
- what this page is about
- what the main takeaway is
- why the user should trust the page

## Page-Family Notes

### Cornerstone guides
- Start with the main recommendation, not with lore.
- Route to narrower winners quickly.

### Support guides
- Solve one problem.
- Use setup/troubleshooting splits where useful.

### Cost pages / research trees / planners
- Answer first.
- Keep numbers scannable.
- Favor tables, tree views, checkpoints, and compact summaries.
- Do not bury totals and unlock requirements in prose.

### Atlas pages
- Help users choose the correct detailed page.
- Compare entities/pages at a glance.
- Do not become overloaded encyclopedias.

## SEO / LLM Search Rules

Treat “SEO and LLM search optimization” as:
- helpful content
- clear structure
- explicit entity naming
- exact answers
- crawlable internal links
- accurate titles/meta
- structured data that matches the real page content

Do not:
- write for “AI style” as a separate voice
- pad pages with empty FAQ sections
- create thin pages just to target a phrase
- force schema where it does not match the real page

For detailed rules, use:

- `automation/memory/seo_llm_optimization.md`

That file is the canonical playbook for:

- query family selection
- title / H1 / meta alignment
- first-screen answer fit
- internal-link / cluster routing
- cannibalization avoidance
- structured data fit
- answer-engine / citation friendliness

## Forbidden Patterns

Do not publish:
- pages that duplicate an existing winner with slightly different wording
- contradictory claims against canonical site knowledge
- vague intros that delay the answer
- copy that reads like generic gaming filler
- smooth but low-utility “AI-ish” paragraphs that restate the topic without helping a player decide
- mass-produced trust or freshness boilerplate that is identical across many pages without page-specific evidence
- broad claims like “ultimate”, “game changer”, “maximize your”, or “best possible” unless the page immediately proves them with specific context
- fake “updated” claims without real content changes
- speculative event timing or mechanic claims without confidence

## Anti-AI-Slop / Human Voice Rules

The risk is not AI assistance by itself. The risk is publishing content that looks mass-produced, generic, or low-originality.

For all future user-visible content:

- write like an experienced player explaining the shortest useful path, not like a generic guide generator
- prefer short operational sentences over polished filler
- replace vague value words with the actual value: badges saved, timing gained, risk avoided, unlock reached, or mistake prevented
- make trust blocks page-specific when possible; do not repeat the same “verified by in-game data and community validation” line everywhere
- do not pad pages with generic setup paragraphs, generic conclusions, or repeated definitions
- keep first-screen answers direct, but make the supporting copy specific to the page’s real job

For LLM-assisted drafts, the draft is not acceptable unless it explains:

- the player problem it solves
- the existing page or cluster it fits
- what new utility it adds beyond rewording
- which claims need human confirmation before publication

## Update Rules

When updating an existing page:
- preserve the page’s primary job
- improve query match, clarity, links, or factual coverage
- do not rewrite a stable winner unless the current version is clearly underperforming or wrong

## Internal Linking Rules

Every meaningful content change should consider:
- upstream hub link
- downstream support link
- one lateral link if there is a neighboring intent

Examples:
- hub → setup
- setup → troubleshooting
- atlas → exact tree page
- cornerstone guide → cost page

## Seasonal / Ambiguity Rule

When community naming or season naming changed:
- state the current interpretation clearly
- mention older naming if confusion is common
- do not mix old and new naming without a clarification note

## Preferred Output Shape

For change planning, the system should prefer:
- smallest useful edit
- strongest intent match
- minimal content duplication
- visible integration into the site graph
