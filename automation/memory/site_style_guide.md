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
- fake “updated” claims without real content changes
- speculative event timing or mechanic claims without confidence

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
