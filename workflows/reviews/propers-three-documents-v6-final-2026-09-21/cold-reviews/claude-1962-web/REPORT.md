# Claude 1962 canonical web artifact: final cold review

## Verdict

**PASS — corrected build, tracked canonical artifact, fresh regeneration, and
receipt are exact-byte identical.**

The exact expected corrected Markdown is reproducible at SHA-256
`d9009d445a8e438ffe603e4dd063535f5795db790cb2b7ca6688b5ed6c3df830`.
The fresh isolated regeneration, existing `build/web` artifact, and tracked
canonical `web/` artifact all have that hash; both byte comparisons return
zero, and `research/web-artifact.json` records the same digest. All three
Markdown copies use the semantic `<br>` title break and contain zero trailing
spaces or tabs.

## Corrected-artifact review

Everything below passes for the exact installed `d9009d...` artifact.

- **Source graph and rite isolation:** all three component phases pass. The
  canonical research graph contains 15 files: the research entrypoint, its
  leaf formatting/metadata/chronology files, nine research sections, and the
  two common formatting inputs. It contains no postconciliar path, concise
  component, homily component, `synthesis.tex`, or `homily.tex`.
- **Single web owner:** the only source leaf and web Markdown matching this
  identity are the canonical unsuffixed leaf. There is no `-synthesis` or
  `-homily` web leaf.
- **Title and hierarchy:** the site renderer produces one `h1`, 57 headings,
  and zero heading-level jumps. The subtitle paragraph contains a real `<br>`.
- **Contents and navigation:** `[TOC]` renders as a ten-link Contents block;
  every fragment target exists. The page retains the primary navigation and
  `Library › 1962 Missal` breadcrumb.
- **Tables:** three tables render with 11 scoped column headers. They are clear
  at desktop width and become internal horizontal scroll regions at the mobile
  breakpoint without widening the document.
- **Four senses:** the three interpretive readings render as three semantic
  definition lists, each with exactly `Literal`, `Allegorical`, `Moral`, and
  `Anagogical` in that order.
- **Chronology:** the live chronology record and generated annotations are
  current. Content preflight reports seven scriptural elements, seven Date
  cells, seven generated annotations, 14 corpus assertions in the record and
  15 in the complete live projection. The rendered chronology has 16 rows
  including its header and the Gospel event row, and preserves the profile
  comparison for Matthew.
- **Browser review:** the exact corrected Markdown was rendered through the
  repository's `public-alpha` renderer and inspected in Chromium at 1440×1000
  and 393×852. The top, Contents, hierarchy, definition lists, inventory table,
  and chronology table are legible and coherent. Focus screenshots hide
  unrelated sibling nodes only to place deep sections in the viewport; their
  section markup and production CSS are unchanged.
- **Converter regression tests:** 69 web-conversion tests, 26 schema-2
  component tests, and 16 propers-format tests pass.

## Browser evidence

- `screenshots/claude-tlm-web--top--1440x1000.png`
- `screenshots/claude-tlm-web--top--393x852.png`
- `screenshots/claude-tlm-web--inventory-focus--393x852.png`
- `screenshots/claude-tlm-web--four-senses-focus--1440x1000.png`
- `screenshots/claude-tlm-web--four-senses-focus--393x852.png`
- `screenshots/claude-tlm-web--chronology-focus--1440x1000.png`
- `screenshots/claude-tlm-web--chronology-focus--393x852.png`

No tracked file was edited by this review. The checkout already contained
uncommitted work; this review wrote only beneath
`.scratch/claude-tlm-web-review-final/`.
