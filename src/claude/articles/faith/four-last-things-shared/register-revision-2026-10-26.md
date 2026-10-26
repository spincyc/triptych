# The Four Last Things (Claude): register revision, 26 October 2026

This record covers the prose register revision of the four Claude essays under
the maintainer's request of 26 October 2026, which applied the 21 October
guidance in `guidance/editorial.md` ("Speaking from within the tradition" and
"Say what the texts say, plainly", including "Plain is not flat"). The 16
October rewrite (`rewrite-review.md`) predates that guidance. Each leaf's
`research/revision-2026-10-26.md` and `research/scope.md` hold its own record;
this file records the series-level decisions and the accepted artifacts.

## Scope and boundaries

The revision changes the essays' own prose in the body sections and nothing
else. Quotations (block, inline and `\latin` spans), endnote bodies and their
attachments, headings, the appendices ("Teaching and Its Grades"; "Scope,
Method, and Qualifications"; the references), `main.tex` and the source
bindings are byte-identical to the 16 October text. A mechanical conservation
check comparing each leaf against the revision's starting commit passed with
no problems on every round, for all four essays. No claim, qualification,
attribution, date, locus or grade was added, withdrawn or restated at a
different degree.

Extent stays within roughly 90–100% of the starting text by the checker's
count (body prose, excluding headings, endnotes and print-only adjustments):

| Essay | Words before | Words after | Ratio |
| --- | ---: | ---: | ---: |
| I Death | 10,825 | 9,798 | 0.905 |
| II Judgment | 11,582 | 10,424 | 0.900 |
| III Hell | 13,606 | 12,599 | 0.926 |
| IV Heaven | 10,126 | 9,285 | 0.917 |

The defects removed were the ones the guidance names: paragraph-closing maxims
and restatements of the quotation just read; claims that a text contains or
governs everything; denials of positions nobody holds; emphatic fragments and
stress devices; repeated connective formulas; and a few places where the
essay's own inference had been put in a source's mouth. Where a cut left a
gap, the plain reason one source bears on the next was written in its place,
in the essay's own voice. "Plain is not flat" governed: the essays' arguments,
concrete scenes and conclusions were kept.

## Reviews

Each essay received an independent cold register and fidelity review by a
fresh reviewer with no inherited conversation, followed by rechecks of every
repair until the review passed with no findings:

- **I Death:** round 0 CHANGES_REQUIRED (1 blocking, 4 advisory: restating
  closers and a shared closing cadence; a claim that the liturgical year
  follows the meditation's order; a missing plain explanation of Ignatius's
  "do not hinder me from living"; the dropped judgement that it is right to
  fear death and right to hope through it; an "it says" crediting the
  *Imitation* with the essay's own word). Round 1 found one new blocking
  fidelity defect in a repair sentence ("formed before the last hour or not
  at all", beyond *Imitation* I.23.4 and contrary to the good thief later in
  the section) and one advisory (a sentence about the essay itself; the
  Preface credited with the essay's own reading). Round 2 passed with no
  findings.
- **II Judgment:** round 0 CHANGES_REQUIRED (1 blocking: a sentence implying
  only two magisterial acts define the immediacy of the particular judgment,
  against Florence's *Laetentur caeli*; 5 advisory). Round 1 passed with no findings; every repair was verified against the sources (the Lyons II profession and *Benedictus Deus* as quoted, *Spe salvi* 44 at its published text, de Sales's words, and the essay's own grading appendix).
- **III Hell:** round 0 passed with two advisories (bare "the same"
  connectives; a closing sentence promising perseverance beyond the Ignatian
  colloquy), both repaired; the round-1 recheck passed with no findings.
- **IV Heaven:** round 0 CHANGES_REQUIRED (1 blocking: restatement closers in
  four places including the final paragraph; 3 advisory). Round 1 accepted
  the repairs and raised one advisory (Thomas's two-premise argument in §10
  restated on one premise). Round 2 passed with no findings.

Each essay's PDF then received an independent every-page visual review:

- **I Death:** round 0 CHANGES_REQUIRED (the English *Proficiscere* ending as
  a two-line stub beside an empty column; a Baltimore *Manual* prayer split
  three lines to six across columns). Two print-only adjustments — a column
  break between the Latin and English *Proficiscere* and a space reservation
  before the prayer — resolved both without changing a word; round 1 passed.
- **II Judgment:** round 0 passed with one advisory (the nine-line de Sales
  quotation in "The Books Were Opened" split three lines to six across a page
  turn). A print-only space reservation keeps the quotation whole on one page
  without changing a word; round 1 passed. The revision timestamp was then
  advanced for the changed render source, which changed only the revision
  line on the final page; the text layers and page rasters were compared to
  confirm it.
- **III Hell:** round 0 CHANGES_REQUIRED (the closing Alphonsus prayer ending
  as a two-line stub beside an empty column). A print-only page break now
  divides the prayer evenly across the columns; round 1 passed. One accepted
  advisory remains: a hyphenated verse line of the *Dies irae* translation,
  identical in the published predecessor.
- **IV Heaven:** passed with no findings.

Reviewers verified repairs against the sources themselves (the *Imitation*,
the *Confessions*, the *Summa*, *Spe salvi*, the conciliar acts as quoted),
not against the authors' accounts.

## Accepted artifacts

| Essay | Pages | PDF SHA-256 | Web edition SHA-256 |
| --- | ---: | --- | --- |
| I Death | 23 | `c0ce7de359ea8da84599bd1dcdbf883457ad3d99a9acb89c720313eb7bd196e6` | `ec286b99658a6655361473e1dd7df5a67b7bc6698ae177ed9b787e8f65e662a5` |
| II Judgment | 25 | `07227cae27258bcaf5af90fe188a93d373ed32e03a35026040a467dcf52f7731` | `3205e299a9d0e273b5fee55aad7a4379f53fa07657aae34697d829ce07d5a139` |
| III Hell | 30 | `e4f164a8b5122cfad75bb2efce11b8263efa3148c6065ab12f04372b7794507d` | `0a1e6a02902c72d22b9eb93c70a4cb489963f991d38a28e73339a33cd0fabb40` |
| IV Heaven | 22 | `1c2fb4e8e6a664609b3b31afb61e239d2c3d2edd6a54384a6614d8913714effa` | `b39647741705b34a55bd564f869c74d20e26cfa622e76cf02dfde72a9299864b` |

Every build exits 0 with settled references and no overfull boxes or
undefined references; residual underfull-box diagnostics match the unrevised
builds and show no visual defect. The generation-metadata and anchor gates
pass on every PDF. Each leaf's `generation-metadata.tex` carries the 26
October revision timestamp and a contribution record naming the model, host
and dispatch terms; each `web-edition.toml` carries `reviewed = "2026-10-26"`.
The web editions are fresh conversions of the final sources, checked against
the converter's own gates; the print-only layout adjustments do not appear in
them.

## Publication

The four PDFs and web editions in the table above are installed. The
deployment to `main` and its live verification are recorded in
`PROJECT-WORK.md`.
