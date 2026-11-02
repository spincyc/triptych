# Historical English encoding repairs: visual review 4

Reviewed on 2026-10-26. **PASS for visual layout: three PDFs, all 20 physical pages.** No blocking visual finding.

## Exact scope and method

This report reviews the encoding-repaired mechanical English source reading editions of *Divinum illud munus*, *Mirae caritatis*, and *Tametsi futura prospicientibus*. It supplements, and does not replace, the earlier `english-visual-4.md` report for different PDF bytes and a different selection.

The controlling assignment is `.scratch/english_encoding_review/lane-4-assignment.json`. The input receipt is `.scratch/typeset_pipeline/english-encoding-final/receipt.json`, independently hashed as:

`6c6f508f3bc1859b33cf2c2501a301428ef3bc7d4cbce2b7efd784de08a2e634`

Every assigned PDF was independently hashed before inspection and matched both its assignment and its entry in `.scratch/english_encoding_review/rasters/review-run.json`. The coordinator generated the rasters centrally through `tools/pdf-review` with two workers. This lane did not render, alter, or duplicate them. Its recorded renderer maximum full-page dimension is 2200 pixels.

All 20 physical pages were opened individually with `view_image` at original raster detail. Each of the three `contact-sheets/sheet-001.png` files was also opened. Contact sheets supported the overall pagination check and did not substitute for individual inspection. Review covered sequential left-column/right-column/page flow, title and body boundaries, clipping, overlap, visible glyph failures, heading placement, density, final source/revision/rights notices, and sparse spill pages.

The receipt reports passing mechanical text fidelity for all three PDFs and no compilation warnings. Those supplied results are distinct from this visual inspection; this lane did not rerun compilation, font/metadata checks, or a whole-body comparison. Targeted retained body-TeX checks were used only to identify conspicuous source residue and the first/last body boundaries.

## Exact reviewed bytes and coverage

All input PDFs are beneath `.scratch/typeset_pipeline/english-encoding-final/`, at `<stem>/<stem>.pdf`.

| Work | PDF stem | Individually opened physical pages | PDF SHA-256 | Result |
| --- | --- | --- | --- | --- |
| *Divinum illud munus* — The Holy Spirit | `1897-05-09-papal-leo-xiii-hf-l-xiii-enc-09051897-divinum-illud-munus-7370b2e4-en` | 1, 2, 3, 4, 5, 6, 7 | `fcbe69a6cc130687516201db16d9c02f9131cf1e17d54cc3b95e55356bfe543b` | PASS |
| *Mirae caritatis* — The Most Holy Eucharist | `1902-05-28-papal-leo-xiii-hf-l-xiii-enc-28051902-mirae-caritatis-95ca27b6-en` | 1, 2, 3, 4, 5, 6, 7 | `4a0dc8eb574cc54a566ffbf1d3a4e433c72862a8988f6c83b53689afdea5fe82` | PASS |
| *Tametsi futura prospicientibus* — Christ Our Redeemer | `1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-en` | 1, 2, 3, 4, 5, 6 | `ead52013c51ac33349c208d57856ce844361ecaaadde98c49a38248995ba4493` | PASS |

For each stem, the exact full-page files opened are
`.scratch/english_encoding_review/rasters/.scratch/typeset_pipeline/english-encoding-final/<stem>/<stem>/pages/page-N.png`,
with `N` individually enumerated in the table. The contact sheet opened for each has the same parent and `contact-sheets/sheet-001.png`. The scratch receipt at `.scratch/english_encoding_review/lane-4/receipt.json` enumerates each opened image separately.

## Individual page findings

No page showed clipped or overlapping text, a lost outer/lower margin, an evident missing renderer glyph, or a heading stranded from its following text. Body type is dense but readable and the gutter remains clear. The following observations record every physical page.

| Work and page | Finding |
| --- | --- |
| *Divinum*, 1 | Compact title, Leo XIII, catalog date 1897-05-09, and English identification fit cleanly. Source begins with its own title/date and “That divine office”; its May 4 date remains visible. Left-column “looking” continues as “forward” at the right-column top; the page ends “absolutely”, continued on p. 2. |
| *Divinum*, 2 | The “refused” continuation is intact. Left-column “likeness we can” continues as “find in creatures”. “THE HOLY GHOST AND THE INCARNATION” remains with its body; source-note lines interrupt the following sentence but remain legible. |
| *Divinum*, 3 | Continues “Son of / man” from p. 2. Both church/souls section headings have following body text. The left-column doctrine sentence continues “committed to them” at the right top; “rivers of” continues on p. 4. |
| *Divinum*, 4 | “living water” starts the page as expected. Notes and body fit within both columns; the right column starts a new paragraph. The conspicuous in-body OCR residue “IHE EOLY SPmiT.” also occurs in body TeX and remains visible, without a glyph-rendering failure. |
| *Divinum*, 5 | Continuous body and source-note lines fit cleanly. Left-column “Old” continues “Testa- ment” at the right top; “penetrate” continues on p. 6. Em dashes render visibly. |
| *Divinum*, 6 | “into the interior” continues p. 5. Left-column ending/source-note residue precedes the right-column “of the Holy Ghost” continuation. The retained “438 THE HOLY ^SPIRIT.” line is also present in body TeX, not a new running footer or clipping. The final sentence continues onto p. 7. |
| *Divinum*, 7 | Substantial concluding body, Apostolic Benediction, source notes [1]–[4], source statement, revision and common rights colophon all fit in the left column. The unused right column is ordinary final-page whitespace, not a notice-only spill. The source statement legibly discloses 16 encoding-only spans, remaining OCR/source-date errors, outstanding full print collation, and the May 4/May 9 conflict. |
| *Mirae*, 1 | Title, author, date and language are distinct; the source heading retains the readable Miræ ligature and opens “To examine”. Both columns fit; the left ends a paragraph before “Accordingly” on the right. “in the” continues as “Eucharist” on p. 2. |
| *Mirae*, 2 | Dense continuous body remains readable. “or again” at left bottom continues “the same as that” at right top; the page ends “the former is”, continued on p. 3. No margin loss. |
| *Mirae*, 3 | “changed into our substance” continues the preceding page. Left-column “there” continues “exist public and notable records” at right top. Notes and body stay within bounds. Existing OCR forms such as “w^ar” and “ferv^or” are visible source defects. |
| *Mirae*, 4 | “expecta- tions” continues p. 3. Left-column “into the” continues “world” at the right top. Source-note interruptions and residual OCR (“2oled”, for example) remain readable; no collisions occur. |
| *Mirae*, 5 | “and charity” continues p. 4. Left-column “derive” continues “their origin” at the right top. Quotations, notes and clear em dashes fit; the final quotation continues on p. 6. |
| *Mirae*, 6 | “eat under the sacramental veils” completes the quotation from p. 5. Left-column “desire” continues “utterly to banish God” at right top. The page ends “by day and night,”, continued on p. 7. No clipping. |
| *Mirae*, 7 | Closing body fills the left column and continues “shine / forth” into the right. Apostolic Benediction, notes [1]–[10], source statement, revision and rights colophon share the page. The source statement legibly identifies 12 encoding-only spans and the residual OCR/full-collation limitations. No additional apparatus page. |
| *Tametsi*, 1 | Compact title/author/date/language are clear; source opens with its own title/date and “The outlook”. Left-column “indeed,” continues “daily practice” at right top. “clearly and” continues on p. 2. Text stays within bounds. |
| *Tametsi*, 2 | “distinctly prefigured” continues p. 1. Left-column “life-blood of” continues “nations” at right top. The solid square before “Luke i. 33.” is literal U+25A0 `■`, also present in body TeX. Its declared partial-marker repair is recorded at container line 2943 in `encoding-audit-63e640f6/encoding-investigation.json`, with exact independent OCR context. It remains OCR note-marker noise, not a missing-glyph box. The page ends “By this”, continued on p. 3. |
| *Tametsi*, 3 | “we ought to understand” follows p. 2. Notes remain legible; both columns flow normally. Right-column body ends “appointed and”, continued on p. 4. Existing split words remain visible. |
| *Tametsi*, 4 | “provided” continues p. 3. Left-column “understanding” continues “as well as over the will” at right top. No heading or text collision. Retained OCR, including “baimer” near the right-column end, is a transcription limitation. |
| *Tametsi*, 5 | “fight” continues p. 4. Left-column “such” continues “important matters” at right top. Source-note lines and body remain within margins; “Him who is” continues on p. 6. |
| *Tametsi*, 6 | “the way, the truth, and the life” continues p. 5. Substantial closing body fills the left column; its last sentence ends with the single-line “Apostolic Bene- diction.” at the right top. This short column continuation is nonblocking. The final source note, source statement, revision and rights colophon follow clearly on the same page. The source statement legibly identifies 12 encoding-only spans (11 intact reversals and one partial marker repair), residual OCR and outstanding full collation. No notice-only spill. |

## Disposition and evidence boundary

The assignment identifies the common repaired source artifact as
`artifact.papal-collections.leo-xiii-great-encyclical-letters.1903-benziger-english.ws-encoding-repaired-ed8e5a40`,
with source SHA-256
`ed8e5a405701a51eec9124f0e63a4db7740ded35545fe5d99874ac9581541879`.
The repository's recorded 205 adopted changes across 11 selections are encoding-only symbol repairs corroborated against independent OCR of the same 1903 printing. This lane reviewed the visual outputs of its assigned three selections; it did not independently recollate all 205 repairs or the printed pages.

Residual OCR word errors, split words, note-marker corruption, in-body page-header residue, and the disclosed *Divinum* date discrepancy remain. Their presence does not establish a PDF renderer failure. The compact final notices accurately retain the historical English web-transcription status, unidentified individual translator, separate historical-wording rights basis, and outstanding full print-collation limit. This PASS establishes basic visual usability of the exact PDF bytes above; it does not establish word-level accuracy against the historical printing.

No PDF, source, manifest, generator, earlier report, or shared raster was changed. No commit or push was made. No visual-layout change is required within this lane's scope.
