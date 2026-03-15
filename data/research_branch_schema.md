# Research Branch Data Schema

This directory stores source data for generated research branch cost pages.

Each branch file is a JSON object with these top-level fields:

- `page`
  - `slug`: output filename without `.html`
  - `title`: HTML `<title>`
  - `meta_description`: meta description and social description
  - `keywords`: meta keywords
  - `h1`: main page heading
  - `headline`: Article schema headline
  - `guide_meta`: short visible meta line under the H1
  - `updated_iso`: `YYYY-MM-DD` for visible date and schema
  - `updated_human`: visible date string

- `guide_verified`
  - short trust / answer-first sentence below the header

- `data_lede`
  - short explanation of what the page helps the player plan

- `quick_answer`
  - `lede`: short direct answer
  - `items`: array of `{ "title", "detail" }`
  - `callout`: optional short highlighted note

- `summary`
  - `title`
  - `body`
  - `bullets`: array of `{ "label", "value" }`

- `tree`
  - `title`
  - `lede`
  - `rows`: ordered array of node-id arrays for layout
  - generator can render connectors from explicit parent links when node data includes `parents`

- `nodes`
  - each node contains:
    - `id`
    - `col` (optional): explicit zero-based column within its row when the visual position should differ from array order
    - `name`
    - `mobile_name` (optional): shorter mobile tree label
    - `levels`: visible level label, for example `Lv. 1-5`
    - `mobile_levels` (optional): shorter mobile level label, for example `1-5`
    - `total_badges`: total badge cost for that node
    - `parents` (optional): array of parent node ids used to render exact tree connectors
    - `type`: `regular`, `highlight`, or `reward`

- `table`
  - `title`
  - `intro`

- `checkpoints`
  - `title`
  - `items`: array of `{ "title", "badges", "text" }`

- `requirements` (optional)
  - `title`
  - `intro`
  - `bullets`: array of strings
  - `followup`: optional HTML string

- `next_steps`
  - `title`
  - `paragraphs`: array of HTML strings

- `faq`
  - array of `{ "question", "answer" }`

- `related_guides`
  - array of `{ "href", "label" }`

Notes:

- `nodes[].total_badges` is the source of truth for the branch page and tree overview.
- `levels` is kept as a visible label so pages can stay aligned with in-game naming even when costs are discussed at the node-total level.
- When `nodes[].parents` is present, the generator uses an SVG connector layer instead of the generic row-wide CSS connectors.
- Generator output is committed as static HTML, then synced through the normal `prepublish_check --fix` workflow.
