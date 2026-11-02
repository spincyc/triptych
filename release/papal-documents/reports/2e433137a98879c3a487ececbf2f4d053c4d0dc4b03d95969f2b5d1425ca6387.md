# Encoding-repaired historical English PDF visual review, group 3

Review date: 2026-10-26. **PASS for the visual layout of all three exact PDFs
below, covering all 20 physical pages.** Every page was opened individually
with `view_image` at the PDF-review helper's original 2200-pixel maximum
dimension. Each document's contact sheet was also inspected. Contact sheets
did not substitute for individual page inspection.

This review covers the source-body-changed reading editions of *Vigesimo
quinto anno*, *Longinqua*, and the letter to the Archbishop of Paris. The
identified English witness is the 1903 Benziger collection. These are
provider-neutral mechanical source editions, with Leo XIII named as issuer,
English identified, and compact source, revision, transcription-limit, and
rights apparatus following the source body.

## Exact reviewed artifacts

The assigned typesetting receipt is
`.scratch/typeset_pipeline/english-encoding-final/receipt.json`, SHA-256
`6c6f508f3bc1859b33cf2c2501a301428ef3bc7d4cbce2b7efd784de08a2e634`.
Its hash was recomputed directly and matched the assignment. Each PDF below
was independently hashed and matched both its assigned SHA-256 and the
shared raster run's source hash and page count.

The coordinator prepared the read-only rasters centrally through
`tools/pdf-review --jobs 2` under
`.scratch/english_encoding_review/rasters/`. Its `review-run.json` has SHA-256
`3fd9dd903de55b542b52d7e44a27ee238559f39913277ad56c3c121f99f60e30`.
No rasters were regenerated during this review.

Each PDF path is `<receipt-directory>/<stem>/<stem>.pdf`. Each raster folder
is `<rasters-root>/<review-run entry.output>`.

| Work and PDF stem | Exact PDF SHA-256 | Pages individually opened | Disposition |
| --- | --- | --- | --- |
| Vigesimo quinto anno — `1902-03-19-papal-leo-xiii-hf-l-xiii-apl-19020319-vigesimo-quinto-anno-08f56845-en` | `a314c75c1fd217fae659bf239dbc4f2c0d70525fde0d3559aa17f7cea8385a49` | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | PASS |
| Longinqua — `1895-01-06-papal-leo-xiii-hf-l-xiii-enc-06011895-longinqua-dbf1a172-en` | `888aa6cbd92e822aaddae88042781e421c4fb149a6a7b086256cbe41a4f797c0` | 1, 2, 3, 4, 5, 6 | PASS |
| Letter to the Archbishop of Paris — `1900-12-23-papal-historical-leo-xiii-paris-archbishop-letter-1900-12-23-260d4c26-en` | `24d3426b5fb9b7f90df54af1298752ccf18245060e4e37513c1754aa8da42555` | 1, 2, 3, 4 | PASS |

All three use source artifact
`artifact.papal-collections.leo-xiii-great-encyclical-letters.1903-benziger-english.ws-encoding-repaired-ed8e5a40`,
whose assigned source SHA-256 is
`ed8e5a405701a51eec9124f0e63a4db7740ded35545fe5d99874ac9581541879`.
The shared repair campaign is limited to 205 source-backed character-encoding
spans. It does not establish lexical correction or print collation.

## Individual page findings

The page numbers below are physical PDF pages. All listed pages had clear
margins and page numbers, readable type, and normal sequential left-column
then right-column flow. No clipping, overlap, missing-glyph substitution, or
detached heading requiring a layout correction was observed.

| Work | Page | Finding |
| --- | --- | --- |
| Vigesimo | 1 | Title, issuer, date, and language are clear. Source heading and opening follow immediately; the left-to-right continuation is intact. OCR word damage and inherited spaced hyphens remain visible. |
| Vigesimo | 2 | Both columns continue normally. Stray punctuation and an embedded St John citation remain visible within the retained transcription. |
| Vigesimo | 3 | Dense but readable continuous body; the column and page continuations are intact. Inherited broken words and paragraph interruptions remain visible. |
| Vigesimo | 4 | Clear body boundaries and margins; no overflow. OCR word damage and internal word splits remain visible. |
| Vigesimo | 5 | Normal two-column continuation without clipping or collision. Several retained malformed words and separated word fragments remain visible. |
| Vigesimo | 6 | Dense body and embedded citation fit within the columns. Retained OCR substitutions and punctuation noise remain visible. |
| Vigesimo | 7 | Body continues correctly between columns and onto page 8. Retained carets and word-recognition noise remain visible. |
| Vigesimo | 8 | Both columns remain readable and unclipped. Retained malformed words and punctuation remain visible. |
| Vigesimo | 9 | Normal page flow. The right column visibly retains running-head/page debris, `REVIEW OF HIS PONTIFICATE. 57\f`, and a filled black square after “immediate contact”. Direct inspection of the generated body TeX confirms a literal U+25A0 square at that locus; it is source content rendered as supplied, not a font replacement glyph. |
| Vigesimo | 10 | Closing prayer and blessing, then historical note [1], appear above the source notice. The notice declares 9 repaired spans (8 intact reversals and 1 partial marker repair), residual OCR word/source-date errors, outstanding full print collation, and revision `2026-10-26T05:10:28Z`. The compact rights colophon is readable and separate. This sparse final page contains substantive source text and is not an apparatus-only or rights-only spill. |
| Longinqua | 1 | Title, issuer, date, and language are clear. The retained source title and dated heading remain together with the opening; normal continuation between columns. |
| Longinqua | 2 | Readable dense body and clear margins. Retained OCR substitutions, carets, and spaced hyphens remain visible. |
| Longinqua | 3 | Normal body continuation. Malformed words and historical citation markers remain visible without font or layout failure. |
| Longinqua | 4 | Embedded historical citation lines at the upper left and prose in both columns fit within the margins. No heading split or clipping; OCR noise remains. |
| Longinqua | 5 | Both columns continue correctly. An embedded Arcanum citation line and recognition errors remain within the retained prose. |
| Longinqua | 6 | The final left column contains substantial closing source prose, an embedded citation, and the Apostolic Benediction before the source notice. The notice declares 5 repaired spans (5 intact reversals, no partial marker repairs), residual errors and outstanding collation, and revision `2026-10-26T05:10:28Z`. Rights text is readable and does not collide with the body or page number. The right column is empty; there is no separate notice-only page. |
| Paris letter | 1 | Title, issuer, date, language, and source heading are clear. “ORIGIN AND OBJECT.” and “SERVICES TO CIVIL SOCIETY.” each stay with the beginning of their following prose. Retained OCR punctuation and word damage remain visible. |
| Paris letter | 2 | Normal full-page continuation between columns; no clipping or detached heading. Recognition errors remain visible in the source prose. |
| Paris letter | 3 | Continuous dense body with clear margins, intact column order, and no heading split or overlap. |
| Paris letter | 4 | Closing paragraphs and Apostolic Benediction precede the source notice. The notice declares 1 repaired span (1 intact reversal, no partial marker repairs), residual errors and outstanding collation, and revision `2026-10-26T05:10:28Z`. Source and rights text are readable and separate. This sparse final left column retains substantive source text; it is not an apparatus-only or rights-only spill. |

Vigesimo's individual rasters were `pages/page-01.png` through
`pages/page-10.png`; Longinqua's were `pages/page-1.png` through
`pages/page-6.png`; the Paris letter's were `pages/page-1.png` through
`pages/page-4.png`. Each document's `contact-sheets/sheet-001.png` was opened.
The scratch receipt at `.scratch/english_encoding_review/lane-3/receipt.json`
records every actual page opening, the corresponding raster paths, exact
hash checks, and these dispositions.

## Review limits

The PASS is a judgment about visual usability of these exact rendered bytes.
The editions visibly retain substantial OCR word errors, punctuation noise,
word fragments, and embedded citation/running-head debris. The new encoding
repairs preserve that recognition noise rather than rewriting the wording.
Their notices accurately disclose residual OCR word and source-date errors
and the outstanding full print collation. The filled square on Vigesimo page
9 is included in that source-quality qualification.

This review did not collate any complete text against the historical print,
verify the English translation, settle source dates, or rerun mechanical
body-text fidelity, PDF font, or metadata checks. The assignment receipt
records separate passing body-text-fidelity checks. No PDF, source payload,
manifest, or prior review report was edited. There is no visual-layout
blocker within this assignment.
