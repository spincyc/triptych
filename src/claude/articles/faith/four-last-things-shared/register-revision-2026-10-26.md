# The Four Last Things (Claude): register revision, 26–27 October 2026

On 26 October 2026 the maintainer asked that the drafting guidance of
21 October in `guidance/editorial.md` be applied to the four Claude essays:
"Speaking from within the tradition" and "Say what the texts say, plainly",
with its rule "Plain is not flat". The rewrite of 16 October
(`rewrite-review.md`) was written before that guidance existed. This file
holds the decisions that apply to the whole series and the artifacts that
were accepted. Each essay's own account is in its
`research/revision-2026-10-26.md`, with a short entry in its
`research/scope.md`.

## Correction of 27 October 2026

During the work of 26 October the host switched the coordinating session and
some of its workers from the Claude model to kimi-k3. The switch was announced
inside those sessions but was not acted on. In this series that model gave the
round-1 verdict on the Judgment repairs, made both Judgment visual reviews and
the Judgment print-only space reservation, and wrote the round-1 verdict of
the Death visual review after the Claude model had inspected the pages. It
also drafted the first version of this record, a section of the Judgment
record and the Judgment contribution line. It built and converted the Judgment
essay, installed the four PDFs, and refreshed the inventory, catalogue and
release bindings. The records then credited all of it to the Claude model. On
27 October fresh Claude workers did each of its reviews again. A fresh Claude
worker, given the text with the reservation removed (its brief said that one
had been removed), re-derived the same reservation. The Claude coordinating
session rewrote the records. The substituted model's mechanical steps were
superseded by the Claude rebuilds and refreshes of 26 and 27 October, as the
sections below and the Judgment and Death records describe. The four
`generation-metadata.tex` files list only Claude work, by exact model
identifier.

An independent Claude audit on 28 October confirmed this account from the
session logs, rebuilt the four PDFs and converted the four web editions again
byte for byte, and corrected statements in this record, in the Judgment and
Death records and in `PROJECT-WORK.md`. It also found that the Death and
Heaven worker contribution lines credit the worker with "its repairs after
review", though the round-1 repairs (Death DEA-006 and DEA-007, Heaven
HEA-005) were made by the coordinating session. Both sessions ran on the
Claude model; the lines are left as they are so that the installed PDFs keep
their reviewed bytes.

## What the revision changes

Only the essays' own prose in the body sections. The block and inline
quotations, the `\latin` spans, the endnotes and their attachment points, the
headings, the appendices ("Teaching and Its Grades"; "Scope, Method, and
Qualifications"; the references), `main.tex` and the source bindings are as
they were at the revision's starting commit, `c7dfb84c7`, which already
carried the two-column layout revision of 26 October. A conservation check
compares each essay with the revision's starting commit, `c7dfb84c7`; it
compares quotations as text with whitespace normalized, and it passed with no
problems on every round for all four essays. The web edition repairs of 27
October (below) changed each `main.tex`, which now calls the title-page macro
without a print-edition condition, and removed the `\emph` around four
`\latin` spans in Heaven. Run again after them, the check reports `main.tex`
as changed in each essay and nothing else.

The revision withdrew no claim, qualification, attribution, date, locus or
grade. Some repair sentences say in the essay's own words a connection that
the earlier text left implicit. The cold reviews checked each of them. One of
them, in Judgment, gave the Lyons profession of 1274, the emperor's profession
of faith received at the council, a higher degree than it has; it was
corrected on 27 October.

Extent, by the checker's count of body prose (headings, endnotes and
print-only adjustments excluded):

| Essay | Words before | Words after | Ratio |
| --- | ---: | ---: | ---: |
| I Death | 10,825 | 9,798 | 0.905 |
| II Judgment | 11,582 | 10,421 | 0.8998 |
| III Hell | 13,606 | 12,599 | 0.926 |
| IV Heaven | 10,126 | 9,285 | 0.917 |

What was cut is what the guidance names: maxims and restatements that close a
paragraph or repeat the quotation just read; claims that a text holds or
settles everything; denials of positions nobody holds; emphatic fragments and
other stress devices; repeated connecting formulas; and a few places where
the essay's own inference was put in a source's mouth. Where a cut left a gap,
the essay now gives the plain reason why one source bears on the next. The
arguments, the concrete scenes and the conclusions stay.

## Cold register and fidelity reviews

Each essay went to a fresh reviewer with no inherited conversation, and every
repair went back to review until a round passed with no findings.

- **I Death.** Round 0 required changes: one blocking finding and four
  advisory ones (closers that restated, with a shared closing cadence; a claim
  that the liturgical year follows the order of the meditation; no plain
  explanation of Ignatius's "do not hinder me from living"; the lost judgment
  that it is right both to fear death and to hope through it; an "it says"
  that gave the *Imitation* the essay's own word). Round 1 found a new
  blocking defect in a repair sentence ("formed before the last hour or not at
  all", which goes beyond *Imitation* I.23.4 and contradicts the good thief
  later in the section) and one advisory (a sentence about the essay itself,
  and the Preface credited with the essay's reading). Round 2 passed.
- **II Judgment.** Round 0 required changes: one blocking finding (a sentence
  implying that only two magisterial acts define the immediacy of retribution
  after death, which Florence's *Laetentur caeli* also defines) and five
  advisory ones. The round-1 recheck was repeated on 27 October against the
  sources: Denzinger in the bound edition, *Spe salvi* 44 and 47, Catechism
  1032, and the retained de Sales and *Summa* texts. It accepted the five
  advisory repairs and found that the blocking repair now called the Lyons
  profession of 1274 a definition, which it is not (finding JUD-007). The
  repair gave both acts the verb "taught", and a looser phrase in section 1
  that implied the same was corrected with it. Round 2 passed.
- **III Hell.** Round 0 passed with two advisories (bare "the same"
  connectives; a closing sentence promising more perseverance than the
  Ignatian colloquy gives). Both were repaired, and the round-1 recheck passed.
- **IV Heaven.** Round 0 required changes: one blocking finding (restating
  closers in four places, the final paragraph among them) and three advisory
  ones. Round 1 accepted the repairs and raised one advisory (Thomas's
  two-premise argument in section 10 restated as if it had one premise).
  Round 2 passed.

## Every-page visual reviews

- **I Death.** Round 0 required changes: the English *Proficiscere* ended as
  a two-line stub beside an empty column, and a prayer from the Baltimore
  *Manual* split three lines to six across the columns. A column break
  between the Latin and English *Proficiscere* and a space reservation before
  the prayer, both print-only, fixed them without changing a word. The round-1
  verdict was written by the substituted model, so on 27 October a fresh
  reviewer inspected every page of the published PDF again and found no
  defect.
- **II Judgment.** On 27 October a fresh reviewer began from the revised text
  with the earlier print-only reservation removed. It found the de Sales
  quotation in "The Books Were Opened" split across a page turn, restored a
  print-only `\Needspace` reservation identical to the earlier one, and
  passed that build, which was byte-identical to the PDF published on
  26 October. After the JUD-007 repair, a further every-page review of the
  new build passed with three advisories accepted: a long Aquinas quotation
  breaking 17 lines to 2 across a page turn; a hyphenated *Dies irae* verse
  line that wraps the same way in the predecessor; and a one-word last line
  where the section 1 paragraph reflowed.
- **III Hell.** Round 0 required changes: the closing prayer of Alphonsus
  ended as a two-line stub beside an empty column. A print-only page break
  now divides the prayer evenly across the columns, and round 1 passed. One
  advisory is accepted: a hyphenated verse line of the *Dies irae*
  translation, the same in the published predecessor.
- **IV Heaven.** Passed with no findings.

Four print-only adjustments were made in all: two in Death and one each in
Judgment and Hell. None changes a word, and none reaches the web editions.

## Web edition repairs, 27 October 2026

A review of the regenerated Judgment web edition found that it had no
epigraph. None of the four web editions had carried one since the rewrite of
16 October, before this revision: each `main.tex` called
`\FourLastThingsTitlePage`, which sets the epigraph on the title page, only in
the print edition. The macro in `format.tex` now chooses its own branch. The
print branch is the title page as before, with the page-anchor and
roman-numbering settings moved inside it. The web branch sets the epigraph
and its source, as the title page prints them, as a quotation, which the
converter places after the contents; it sets no title or subtitle, because
the web edition takes those from the PDF metadata. Each `main.tex` now calls
the macro directly.

A review of all four web editions then found a second defect in Heaven
alone, also present since 16 October. The four Latin lemmas in "The Vision of
God" that open the gloss on *Benedictus Deus* were italic in the PDF and plain
in the web edition: the source wrapped `\latin` in `\emph`, and the converter
drops italics nested inside italics. They are now written with `\latin`
alone, which sets the same italic in the PDF. A search of the four essays'
sources found no other italics nested in this way.

The print pages are unchanged: apart from the revision line on the last page,
every page of each rebuilt PDF matches its predecessor when rasterized.

## Accepted artifacts

| Essay | Pages | PDF SHA-256 | Web edition SHA-256 |
| --- | ---: | --- | --- |
| I Death | 23 | `321c4346c435299ab6376ce68c1a91fa34face004d903fdcc485c2b6c00d3b3c` | `4a3e7cd75a9c61081a15eb3505f268d2a655b4bf56879a98aa9cef107496a617` |
| II Judgment | 25 | `6ec2bf6a465cecec3800baa2ac2ef59d6b616383d94952e551b875cae4f36555` | `fedbaef01297c60c2cab44d57037476ab1c0904221e31ee4cf2b4dec6865d04a` |
| III Hell | 30 | `3bcfa196950617c075073adc31e904c9298047ca48b1979eed34d3cccd9960f5` | `53596d14d153c2bf0043758e19f1fe45ce4c1b5abe2fb0a5e26dc94dbe9dc38b` |
| IV Heaven | 22 | `53f57926044cfefef5f41dc0de2f1e858d28ae14545f9070c65a2a2e25f6f252` | `185560890437b62851f7aef26bcb39dd594370f936e9c4d5001de398c40632f0` |

Every build exits 0 with settled references, no overfull boxes and no
undefined references; the underfull-box notices that remain are those of the
unrevised builds and show nothing on the page. The generation-metadata and
anchor gates pass on each PDF. Each `generation-metadata.tex` lists the
contributions to this revision by exact model identifier, exposed reasoning
effort, dispatch tier and client version. All four revision timestamps are
2026-10-27T16:55:31Z, for the web repairs; Judgment's wording repair had
first advanced its timestamp to 2026-10-27T15:50:30Z. Apart from the revision
line, each PDF matches page for page the one published on 26 October, except
that Judgment matches the reviewed build of its repaired wording. The web
editions are fresh conversions of the final sources and pass the converter's
gates. Each was reviewed against its PDF on 27 October, and each
`web-edition.toml` carries `reviewed = "2026-10-27"`. `PROJECT-WORK.md`
gives the hashes published on 26 October.

## Publication

`PROJECT-WORK.md` records the deployment of 26 October and its live check. The
correction of 27 October is recorded there as pending until it is deployed and
verified.
