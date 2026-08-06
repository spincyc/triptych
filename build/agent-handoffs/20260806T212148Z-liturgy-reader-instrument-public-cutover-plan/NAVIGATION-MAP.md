# Liturgical Instrument cutover navigation map

## Scope

This is a read-only inventory at
`7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`. No link is changed by planning.
The preferred same-path cutover intentionally makes external navigation edits
unnecessary.

## Repository-owned links into canonical readers

| Owner | Current destination | Classification | Later cutover edit |
| --- | --- | --- | --- |
| `README.md` | `liturgy/day.html`, `liturgy/` | already canonical | none |
| `docs/the-mass.md` | `../liturgy/` | already canonical Propers entrance | none |
| `library/liturgy.md` | `../liturgy/` | already canonical Propers entrance | none |
| `src/web/browser/history/index.html` | `../liturgy/day.html`, `../liturgy/` | already canonical | none |
| `src/web/browser/sources/index.html` | `../liturgy/day.html`, `../liturgy/` | already canonical | none |
| `src/web/browser/texts/index.html` | `../liturgy/day.html`, `../liturgy/` | already canonical | none |
| `src/web/browser/catena/index.html` | `../liturgy/` | already canonical Propers entrance | none |
| `src/web/browser/law/index.html` | `../liturgy/` | already canonical Propers entrance | none |
| `src/web/browser/scripture/index.html` | `../liturgy/` | already canonical Propers entrance | none |
| `src/web/browser/scripture/track.html` | `../liturgy/` | already canonical Propers entrance | none |

`tools/public-alpha` resolves Markdown links naming the `liturgy` entrance to
`liturgy/index.html`. Standalone browser pages keep authored relative links.
`/liturgy/` and `/liturgy/index.html` currently return HTTP 200 with identical
bytes rather than redirecting. The explicit canonical spelling for the plan is
`/liturgy/index.html`; the directory form remains a host alias.

No repository-owned navigation link to `day-reader.html` or
`propers-reader.html` was found. No public navigation path therefore needs a
route change, and any proposed mechanism that required broad href edits would
be rejected as too invasive.

## Links inside the current canonical readers

| Source | Current links | Cutover consequence |
| --- | --- | --- |
| `src/web/browser/liturgy/day.html` footer | Propers `index.html`, Law, Texts | removed if candidate DOM is copied unchanged |
| `src/web/browser/liturgy/index.html` footer | Day `day.html`, Scripture, History, Texts, Sources, Law | removed if candidate DOM is copied unchanged |

The accepted Instrument masthead links to Triptych Home. In the built site,
`reader-instrument.css` hides the generated header, footer, release banner, and
breadcrumb around an Instrument. Thus “all external links already use canonical
URLs” does not prove navigation parity: direct Day↔Propers and contextual exits
would change from one link to a two-step trip through Home.

The plan recommends one quiet counterpart entrance link plus contextual links
inside Details, but the exact presentation is an independent-review decision.
It must not restore the generic site header, add a new dashboard row, or alter
the four primary action model. Until resolved, this is a cutover blocker rather
than an unrecorded navigation deletion.

## Candidate and oracle surfaces

- `day-reader.html` and `propers-reader.html` remain unlinked compatibility and
  parity surfaces for the initial acceptance window. They must become
  source-declared noindex and must not advertise themselves as canonical.
- `reader-visual-reset-day.html` and `reader-visual-reset-propers.html` remain
  unlinked, statically noindex, unchanged visual oracles.
- No cleanup, redirect, deletion, or repurposing of these routes belongs to the
  initial cutover.

## Later label-only possibilities

The homepage/catalog descriptions may eventually be updated to describe the
accepted reader’s Read/Missal/Browse interaction more precisely, but their
current hrefs are correct and a label refresh is deliberately postponed until
after independent public-cutover acceptance. It is not a cutover prerequisite.
