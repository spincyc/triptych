# Web Editions

This policy governs every provider branch. Its deterministic half is
implemented by `tools/tpt check-web-edition` and the per-leaf record
`web-edition.toml`; the evaluative half is provider work that this profile
defines.

## What a web edition is

A web edition is a generated, reviewed reading version of one eligible
publication, offered for readers who cannot use a print-shaped PDF. The
LaTeX under `src/<provider>/<leaf>/` remains the one authoritative source.
A web edition is derived from it and never hand-authored beside it: there is
no second editable copy of a publication's text, and a divergence between
the two is a defect in the web edition, not a variant reading.

`guidance/repository.md` governs ownership, paths, and the colophon;
`guidance/editorial.md` governs content quality. A web edition weakens
neither.

## Pipeline

Three tiers, in order:

1. **generate** — a converter reads `src/<provider>/<leaf>/*.tex` and writes
   `build/web/<provider>/<leaf>.md` under the ignored build tree;
2. **review** — a person or provider reads the generated file against the
   installed PDF and installs the accepted result as tracked
   `web/<provider>/<leaf>.md`; and
3. **install** — the site renders only tracked `web/`.

Only tier two is a publication decision. Generated output is a reproducible
intermediate and is never edited in place to become the tracked file
without review. An ineligible publication has no tier-one output.

## Eligibility

Every publishable leaf declares its own eligibility in `web-edition.toml`
beside `main.tex`. `make check-web-editions` validates the declaration
mechanically: a missing record is an error, so a new publication cannot
default to eligible by silence.

- **eligible** — the document's meaning survives reflow. No declared
  blocking construct, and none found by the scanner in the leaf or in the
  shared trees it inputs.
- **conditional** — renderable only once a named obstacle is solved
  (wide matrices, diagrams, paired-column bilingual text, gated answers,
  write-in forms). The record names the obstacle; it does not promise a
  solution.
- **ineligible** — the page itself carries the meaning (duplex cards,
  page-matched courses, print artifacts). These publications remain
  PDF-only without prejudice: ineligibility is a statement about layout,
  not about quality, importance, or release status.

Declaring `eligible` against a document that uses a blocking construct is a
gate failure, not a judgment call. Reclassify the leaf or remove the
construct.

## Rights and provenance

A web edition reproduces the document's rights colophon
(`\TriptychRightsNotice` in `src/common/preamble.tex`) and its
reader-facing revision timestamp in readable form on the page a reader
actually reaches. Model identity, qualifiers, effort, agent/runtime details,
and contribution history remain only in tracked audit records. A web edition
that drops the timestamp or rights colophon is not publishable. The colophon rule in
`guidance/repository.md` binds every rendering of a publication, not only
the PDF.

## Fidelity

A web edition never introduces content absent from the PDF, and never
silently omits content present in it. Permitted differences are layout
adaptations only: reflow, single-column collapse, table linearization,
substitution of a described equivalent for a purely decorative rule or
frame. Any material omission — a dropped appendix, matrix, diagram, or
apparatus — is declared in the record's rationale and visibly in the web
edition itself. An undeclared omission is a defect.

The converter's job is to make omission impossible to miss, because the
reader deletes silently and exits zero. Known deletions, all now handled
in `scripts/web-shim.tex` or `tools/tpt web-edition`: a `\multicolumn`
cell loses its contents; a `>{...\arraybackslash}` column prefix
swallows the token opening every cell in that column, so dates and book
numbers vanish from a citation; `\cmidrule` leaks its span into the
following row; `\endnote` disappears with its citations; an `enumitem`
option list takes every `\item` label with it; a comment between a
`\newenvironment`'s groups hides the definition from the audit. When you
meet a new one, add the audit that catches it, not just the fix. A macro
the shim does not define and the audit does not know stops the
conversion by design — extend the shim rather than dropping the leaf.

## Componentized proper guides

When a proper profile authorizes `proper-components.toml`, the canonical
research mode is the publication represented on the web. The converter reads
the canonical entrypoint and every `research` component. The `-synthesis` PDF
is a bounded mechanical companion and receives no separate web leaf; canonical
HTML is its accessible superset. This is not an `ineligible` classification
and must not be represented by a fabricated blocking construct.

Component boundaries become semantic headings, stable element keys become
durable anchors, and relation evidence classes remain readable text rather
than styling alone. Component-scoped references accompany exactly the
components that use them. Preflight rejects a component included in one mode
when it depends on a component omitted from that mode.
