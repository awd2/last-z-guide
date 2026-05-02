# SEO / LLM Optimization Playbook

This is the canonical optimization playbook for `lastzguides.com`.

Use it together with:

- `automation/memory/site_style_guide.md`
- `automation/memory/page_archetypes.md`
- `automation/memory/canonical_claims.json`
- `automation/memory/content_index.json`

The goal is not “SEO hacks” or a fake “LLM voice”.
The goal is:

- strong query-to-page match
- clear first-screen answers
- consistent cluster architecture
- crawlable internal routing
- pages that are easy for both search engines and answer engines to understand and cite

## Optimization Priorities

Always optimize in this order:

1. intent match
2. page role clarity
3. first-screen answer quality
4. title / H1 / meta alignment
5. cluster integration and internal links
6. structured data and indexing hygiene

Do not optimize in this order:

- raw keyword repetition
- FAQ inflation
- “AI-friendly” filler
- duplicative page creation for every phrase variation

## Query Strategy

Every page should have:

- one primary query family
- a small set of secondary variations
- one clear dominant user job

Examples:

- `codes.html`
  - primary family: `last z redeem codes`
  - secondary: `gift center`, `gift center login`, `uid`, `code redemption`
- `gift-center-uid.html`
  - primary family: `last z gift center login`
  - secondary: `uid`, `copy id`, `how to redeem on phone`
- `redeem-code-not-working.html`
  - primary family: `last z code not working`
  - secondary: `gift center error`, `wrong uid`, `rewards not showing`

Rules:

- the primary query family must match the page’s real role
- secondary terms should support the page, not redefine it
- do not split one intent into multiple thin pages unless the user job is genuinely different

## Keyword and Entity Rules

Use:

- exact game entities
- canonical event names
- stable branch names
- common community aliases when real confusion exists

Do not:

- stuff repeated keywords into paragraphs
- force phrase variants into every heading
- mix old and new naming without clarification

If community naming changed:

- use the current canonical term first
- add the old or alternate name only where it reduces confusion

## Title / H1 / Meta Rules

`title`, `H1`, and `meta description` must work as one system.

### Title

The title should:

- lead with the real page intent
- use the canonical entity name
- stay specific and click-worthy without hype
- match the page’s actual answer

Use:

- `Entity + action/outcome`
- `Entity + exact problem`
- `Entity + comparison / guide type`

Avoid:

- vague titles
- title/H1 mismatch
- broad titles on narrow pages
- narrow titles on broad hub pages

### H1

The H1 should:

- match the same intent as the title
- be readable on-page
- avoid being meaningfully different from the title unless there is a good reason

### Meta Description

The meta description should:

- reflect the actual first-screen answer
- include the primary decision or utility of the page
- support click-through, not just keyword presence

It should not:

- promise things the page does not deliver
- read like a keyword list

## First-Screen Answer Rules

The first screen is critical for both SEO and LLM retrieval/citation.

Every important page should quickly establish:

- what the page solves
- the main recommendation or answer
- why the answer is trustworthy or operationally useful

Preferred first-screen structure:

1. clear H1
2. short trust/freshness signal where appropriate
3. `guide-verified` or equivalent context block when trust matters
4. `Quick Answer` or equivalent direct answer
5. immediate route to the next relevant action/page

The first screen should not:

- spend space on lore or generic background
- hide the recommendation below long intros
- bury the decision rule in prose

## First-Screen Exception Policy

Not every page needs the exact same chrome.

Required principle:

- every important indexable page should expose a strong early answer signal

But that signal can take different shapes by archetype:

- `support-guide`, `cost-page`, `atlas-page`
  - should usually have `guide-verified`, `Quick Answer`, or an equally explicit first-screen answer block
- `cornerstone-guide`
  - should usually have a strong opening recommendation and may also use `guide-verified` / `Quick Answer`
- `comparison-guide`
  - may use a strong opening comparison summary instead of a standard `Quick Answer` block
- `event-guide`
  - may use a short operational opener if that fits the page better than a formal `Quick Answer`
- `site-page` and clearly non-indexable/internal pages
  - should not be forced into answer-first content templates

Deterministic SEO/LLM checks should be interpreted with this rule in mind:

- warnings are a review prompt, not an instruction to force every page into one template
- the goal is early clarity and retrieval quality, not visual uniformity

## Section Design Rules

Optimize sections for retrieval and scanning:

- use descriptive H2/H3 headings
- keep paragraphs short
- prefer lists, tables, checkpoints, and compact callouts when the topic is operational
- make important comparisons explicit

For utility pages, prefer:

- step order
- thresholds
- unlock chains
- stop points
- cost totals

This improves:

- human comprehension
- snippet quality
- answer-engine extraction

## Internal Linking and Cluster Architecture

Internal links are part of optimization, not optional polish.

Every meaningful page should sit inside a visible cluster.

Minimum expectations:

- support pages link back to the correct hub
- hubs route to the right support pages
- atlas pages route to exact detail pages
- neighboring intents connect laterally where useful

Examples:

- `codes.html` -> `gift-center-uid.html` and `redeem-code-not-working.html`
- `gift-center-uid.html` -> `codes.html` and `redeem-code-not-working.html`
- `research.html` -> `research-costs.html`
- `research-costs.html` -> exact branch pages

Do not create isolated pages that depend only on search engines to be found.

## Cannibalization Rules

Before creating a new page, check:

- does a current winner already satisfy this intent
- is the real problem a snippet/title mismatch rather than missing content
- should this be a section on an existing page instead of a new URL

Create a new page only when:

- the user job is meaningfully different
- the page archetype is different
- the page can hold a distinct query family without blurring another winner

Warning signs of bad cannibalization:

- two pages targeting the same “how to” question with minor wording differences
- a support page trying to become a hub
- an atlas page trying to become the canonical detailed guide
- a new page whose real fix should have been a snippet/title/first-screen update to an existing winner

## Structured Data Rules

Structured data should explain the real page, not decorate it.

Use schema only when it genuinely matches the page type and visible content.

Good fit:

- `Article`
- `FAQPage` only when the FAQ is real, useful, and visible
- sitewide `Organization`

Do not:

- force FAQ schema onto thin or decorative FAQ blocks
- add structured data that implies content the page does not actually contain
- assume schema alone will improve ranking

## AI Search / Answer Feature Eligibility

AI search visibility starts with ordinary search eligibility.

Important indexable pages should remain:

- crawlable
- indexable
- eligible for snippets
- available as visible textual content, not only image or script-rendered content
- internally linked from relevant pages
- backed by structured data that matches visible page content

Do not add special “AI schema”, `llms.txt`, hidden summaries, or machine-only content.

For Google AI features, there is no separate optimization layer beyond search fundamentals. The practical rule for this site is:

- make the page useful enough for a player
- make the answer easy to extract and cite
- keep the content eligible for normal snippets unless there is a deliberate privacy or policy reason not to

## Crawler and Snippet Controls

Crawler and snippet controls are part of SEO / LLM visibility.

For indexable guide pages:

- do not add `noindex`
- do not add `nosnippet`
- do not add `max-snippet:0`
- do not wrap the first-screen answer, `qa-lede`, `guide-verified`, `data-lede`, or main recommendation in `data-nosnippet`
- do not block search or answer-engine crawlers in `robots.txt`

Current crawler policy:

- allow search crawlers to access public guide pages
- allow `OAI-SearchBot` so pages can be linked and surfaced in ChatGPT search features
- treat training crawlers such as `GPTBot` as a separate policy decision from search visibility

Archived or internal experiments may use `noindex`, but they must stay out of editorial routing and LLM automation.

## Trust / Who / How / Why Signals

Every future content change should preserve or improve trust signals.

The page should make clear:

- who is responsible for the guide: `Last Z Guides`
- why the page exists: to solve a real player job, not to target a phrase
- how the answer was produced when that matters:
  - game observation
  - canonical site memory
  - generated JSON data for research branch pages
  - GSC/Bing evidence for optimization work

Do not fake freshness. Update dates and sitemap `lastmod` should reflect meaningful content, structured data, or internal-link changes.

## Search Index / Sitemap Rules

After meaningful content or structure changes:

- ensure `sitemap.xml` is in sync
- ensure `search-index.json` is in sync
- update sitemap `lastmod` only for meaningful page changes, not cosmetic churn
- preserve custom titles/descriptions/keywords where they are intentionally better than auto-derived defaults

If a page is important and newly added to a cluster:

- make sure it is crawlable through internal links
- do not rely on sitemap submission alone

## LLM / Answer Engine Rules

Treat answer engines as systems that reward:

- explicit answers
- stable terminology
- structured comparisons
- entity clarity
- clean page roles
- visible related-page routing

Pages are more citation-friendly when they:

- answer the core question in the first screen
- use consistent wording for the same mechanic across the site
- avoid contradiction with neighboring pages
- provide crisp lists, tables, thresholds, and decisions

Do not write a separate “AI voice”.
Write a clear operational page that is easy to quote accurately.

## Update Rules

When updating an existing page for optimization:

- preserve the page’s core role
- improve query match before expanding scope
- fix title/meta/first-screen alignment before adding more sections
- improve cluster routing before creating a new URL

For high-performing pages, prefer:

- snippet and first-screen sharpening
- better internal links
- cleaner exact-answer formatting

Over:

- large rewrites without evidence

## Release Expectations

A change is not “SEO optimized” unless it also:

- respects canonical claims
- keeps cluster roles clean
- passes indexing and metadata checks
- improves or preserves first-screen answer quality
- avoids creating low-value or overlapping pages
