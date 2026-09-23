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
  web-active input closure. A construct confined to the true/print arm of an
  explicit `\\ifdefined\\TriptychPrintEdition ... \\else ... \\fi` branch does
  not enter that closure; the always-included source must provide its complete
  textual equivalent, and the normal fidelity review must verify it.
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
following row, including from inside a leaf's own row macro, where the
postconciliar `\dossierevent` put "2-4" before every narrated event and
dossier note, so the audit now refuses a span pandoc kept without
attributes; a starred row end, `\\*[-0.06em]` in the postconciliar
`\unitphase`, set its length before the next row's first cell, and a
body row ending `\\*` set its star there; pandoc takes the number
opening a cell, or following a command in running text, as an argument of
many commands it otherwise ignores -- `\RaggedRight`, `\centering`,
`\noindent`, `\relax`, `\normalfont`, `\ttfamily`, `\newpage`, `\endfoot`
and more -- so the parish ledgers, the institute timelines, the assembling
reference, both 1962 calendars and the la Salette and Guadalupe acts lost
dates, years and ranks: a column prefix now keeps only the declarations
pandoc renders (weight, shape, size) and `\raggedright`, at any brace
depth; row-level page and spacing commands are closed with an empty group;
the rest are closed where a number or a macro parameter follows; and the
row-opening audit, reading the body as assembled before the converter
rewrites any of it, refuses an edition in which any source table cell's
opening is missing from the output's cells, so neither a variant nobody has
met yet nor the converter's own rewriting can lose one silently; pandoc
drops `\textemdash` and `\textendash` with the number after them, so they
are set as the characters, the space after them read as TeX reads it and
never across a blank line, which once joined two paragraphs; a longtable declaring `\endfirsthead` and
`\endhead` published its header twice, the continuation head as the first
body row, so only the first head is kept, each longtable read alone and in
either order of its heads, and the audit refuses a first body row that
repeats its header; a `\multicolumn` span lost the face its own spec
declares until that face was carried into it; `\cline` leaked its span as
`\cmidrule` did; a column prefix broken by a paragraph break, `\raggedright` after
`\bfseries` or a blank line after `\endfoot`, set each cell as an empty
bold paragraph with its text unbolded after it and forced the table into
HTML, so the converter's table filter now restores the cell as TeX sets
it, leaves a collapsed `\multicolumn` span its own face, split or not,
because a span replaces its column's prefix, writes bold inside bold once,
and the audit
refuses empty or nested bold; `\endnote` disappears with its citations; an `enumitem`
option list takes every `\item` label with it; a comment between a
`\newenvironment`'s groups hides the definition from the audit; an
edition conditional written inline, `\ifdefined\TriptychSynthesisEdition
… \else … \fi{}`, was spliced with the newlines that surrounded it and
so cut its sentence in two at a paragraph break, which the paragraph
audit now catches by its shape; a macro whose text opens with a
bracket, `\notread{…}` setting the unappointed half of a verse, was read by
pandoc as the optional argument of the `\nopagebreak` ending the quotation
environment before it and deleted with it, so every such macro now reaches
pandoc behind an empty group and the audit requires each call's words in
the output; and pandoc cannot expand the `\if\relax\detokenize{#n}\relax`
test with which `\propertitle` omits an empty field, so every proper title
block lost its second and third lines while their words still stood in the
opening prose. The shim now sets each field as a line of its own, and the
audit requires the non-empty fields of every title macro as consecutive
blocks in source order. When you meet a new one, add the audit
that catches it, not just the fix. A macro the shim does not define and
the audit does not know stops the conversion by design — extend the shim
rather than dropping the leaf.

Two handlings are deliberate rather than repaired, and a reviewer meets
the decision here rather than the bare defect. A `\multicolumn` span
keeps its contents but not its span, because neither Markdown nor the
site's renderer has a cell span. In the dossier of the shared proper
format — `\dossierprose` and `\dossierevent` in a `dossiertable`, in a
leaf declaring `format_contract = "propers-format-v1"` — each note is set
as a paragraph directly beneath the row it annotates, and the table
resumes after it under its own header row, as a longtable repeats its
header on each page. The maintainer decided this on 2026-09-23: written
into the first cell of a padded row, those notes stood in the table's
narrowest column, and the Eighteenth Sunday's dossier ran about 8,900 px
tall at 1280 px wide, against about 3,900 px lifted out. Everywhere else,
including a leaf that defines its own dossier, a full-width note is still
written into the row's first cell and the row is padded with empty cells
to the table's width, readable but under a column header that does not
govern it. And a `<` inside quoted matter is
written `\<`, which the site's Python-Markdown does not consume, so the
backslash reaches the reader; the escape set the converter emits is
pandoc's, and narrowing it to the site's is a change to every tracked
edition that carries one.

The site presents a dossier's tables without clipping any column, as the
maintainer also decided on 2026-09-23: an ordinary four-column table at desktop
widths, and at the stylesheet's 760px breakpoint each row set as two lines of
two, unit and citation over location and date, beneath a header block of the
same shape. `release/public-alpha/assets/site.css` finds the dossier by its
section heading's id, `sec:date-location` or the plain heading's slug
`scriptural-date-and-location`, and `tools/tests/test_public_alpha.py` holds
every edition to those ids, so a converter change to that heading moves the
stylesheet with it.

## Componentized proper guides

When a proper profile authorizes `proper-components.toml`, the canonical
research mode is the publication represented on the web. The converter reads
the canonical entrypoint and every `research` component. The `-synthesis` PDF
is a bounded mechanical companion and receives no separate web leaf; canonical
HTML is its accessible superset. This is not an `ineligible` classification
and must not be represented by a fabricated blocking construct.

Under [the schema-2 contract](liturgy/propers-three-documents.md), the
canonical research study remains the sole web owner. Its `-synthesis` and
`-homily` PDFs contain separately authored concise and spoken presentations
within that same source leaf and have no separate web declarations. The
canonical HTML supplies their research and citations, not a claim that it
reproduces their distinct prose verbatim. The reader catalog links all three
PDFs alongside the canonical web edition.

Component boundaries become semantic headings, stable element keys become
durable anchors, and relation evidence classes remain readable text rather
than styling alone. Component-scoped references accompany exactly the
components that use them. Preflight rejects a component included in one mode
when it depends on a component omitted from that mode.

For a current schema-2 proper, conversion assembles exactly the same recursive,
literal source graph accepted by the component checker. A source present only
in TeX's recorder or only in the converter is an error. Generated Markdown uses
semantic `<br>` elements where a hard break is needed and contains no trailing
spaces or tabs.

For schema 2, author one explicit `\label{proper-<element-key>}` at each
appointed text or its rights-safe locator. Put it immediately after a heading
that names only that element, or immediately before the element's paragraph
when a heading groups several texts. Optional alternatives have their own
declared keys and targets. The converter verifies exact coverage and unique
source and rendered targets; it does not infer a liturgical role from a Bible
reference or a combined heading. Label placement remains a source-review
judgment. A missing or misplaced source label belongs to the study author;
loss of a correctly placed label in conversion belongs to the converter.
