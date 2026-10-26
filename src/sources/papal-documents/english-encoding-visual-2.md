# English encoding repair: visual review, partition 2

Reviewed on 2026-10-26. **PASS for visual layout of the three exact PDFs below.**
All 21 physical pages were opened individually through `view_image` at the
original 1700 × 2200 full-page raster size. Each document's contact sheet was
also opened. No page was accepted from a contact sheet alone. The shared
rasters were prepared centrally with `tools/pdf-review --jobs 2`; this review
did not rerender or change any PDF, source payload, manifest, or prior report.

| Source edition | Physical pages individually opened | Exact reviewed PDF SHA-256 |
| --- | --- | --- |
| *The Study of Holy Scripture* — Providentissimus Deus | 1–12 | `c355929180726b087bdf98a4ca19ad0eef52240dcb488acf0af0b2a5147e7a67` |
| *Anglican Orders* — Apostolicae Curae | 1–6 | `6dab69f7f5bd684fa2d196a6ec69d609d13114b6a9029a689778b70865a1f44c` |
| *Letter to the Superiors of Religious Orders and Institutes in France* | 1–3 | `d2bbe84b121c28222d576c83b093fb6c4cd5d38f77fbe799e2f2ca761c50c91a` |

## Identity and coverage

The pinned build receipt is
`.scratch/typeset_pipeline/english-encoding-final/receipt.json`, SHA-256
`6c6f508f3bc1859b33cf2c2501a301428ef3bc7d4cbce2b7efd784de08a2e634`.
Its bytes and all three PDF hashes were independently checked with
`sha256sum` and matched both the assignment and the corresponding central
`review-run.json` entries. The assignment is
`.scratch/english_encoding_review/lane-2-assignment.json`, SHA-256
`d8c6db41c7a2b26703d18a955cefaa4ebf2fc792a95977897f9cec2791d8c139`.

The raster record is
`.scratch/english_encoding_review/rasters/review-run.json`, SHA-256
`3fd9dd903de55b542b52d7e44a27ee238559f39913277ad56c3c121f99f60e30`.
The renderer fingerprint is
`cb6bc6758b165c50bba7f68d7b5e1df5cc66fa3e0aad97361992b67d97cea2ba`.
For each assigned entry, the raster directory is the raster root joined to
that entry's `output`. The following exact page files were opened there:

| Document | Individual files under `pages/` | Additional image opened |
| --- | --- | --- |
| Providentissimus Deus | `page-01.png`, `page-02.png`, `page-03.png`, `page-04.png`, `page-05.png`, `page-06.png`, `page-07.png`, `page-08.png`, `page-09.png`, `page-10.png`, `page-11.png`, `page-12.png` | `contact-sheets/sheet-001.png` |
| Apostolicae Curae | `page-1.png`, `page-2.png`, `page-3.png`, `page-4.png`, `page-5.png`, `page-6.png` | `contact-sheets/sheet-001.png` |
| French religious superiors letter | `page-1.png`, `page-2.png`, `page-3.png` | `contact-sheets/sheet-001.png` |

## Page findings

The two columns follow normal left-column-to-right-column order, continuing
onto the next physical page. Text remains inside the margins and clear of the
gutter. No clipping, overlapping text, or isolated title/heading caused by a
layout break was observed. The visible squares described below are literal
source characters, not evidence of a missing-font substitution.

| Document | Physical page | Disposition and observation |
| --- | --- | --- |
| Providentissimus Deus | 1 | **PASS.** Compact title/date/language identification, retained historical heading and opening paragraph are visible. Both columns fit. Residual word damage and stray caret-like source markers remain. |
| Providentissimus Deus | 2 | **PASS.** Both columns continue normally and remain unclipped. Embedded references and malformed OCR passages interrupt the prose within the retained source. |
| Providentissimus Deus | 3 | **PASS.** Continuation begins with `themselves`; references in the first column and the second-column historical survey fit without collision. |
| Providentissimus Deus | 4 | **PASS.** Column/page flow is clear. The right column retains an old `THE STUDY OF HOLY SCRIPTURE.` running head, the source numeral `282`, and isolated source symbols inside the body. These are source contamination, not a new page heading. |
| Providentissimus Deus | 5 | **PASS.** Dense text stays within both columns. A visibly garbled passage in the middle of the left column remains inherited OCR damage. |
| Providentissimus Deus | 6 | **PASS.** Both columns fit. Old source page numerals `286` and `287`, repeated running heads, and malformed text remain in the prose stream. The filled square in the left-column symbol cluster is present literally in the retained source at physical line 1491. |
| Providentissimus Deus | 7 | **PASS.** Left-to-right continuation and lower page edges are clear. Substantial word/symbol corruption remains near the top and middle of the right column. |
| Providentissimus Deus | 8 | **PASS.** Both columns fit with a clear gutter. Several left-column passages contain inherited malformed words and symbols; right-column text continues without clipping. |
| Providentissimus Deus | 9 | **PASS.** Continuous columns and inline references remain readable as set. The page has no heading or apparatus break needing repair. |
| Providentissimus Deus | 10 | **PASS.** The text continues across the columns and onto page 11. Malformed source passages remain near the lower left and upper right; no character is visibly cut off by the layout. |
| Providentissimus Deus | 11 | **PASS.** The source's concluding benediction is visible in the right column, followed by retained references [1]–[4]. The damaged closing prose includes literal filled squares also present in source lines 1591 and 1593. |
| Providentissimus Deus | 12 | **PASS.** Retained references [5]–[17], the source/repair qualification, visible revision and compact rights colophon all fit in the left column. The right column is empty. This is a sparse notes-and-apparatus final page, not a rights-only spill. |
| Apostolicae Curae | 1 | **PASS.** `Anglican Orders`, pope/date/language identification, historical heading, and opening body are clear. The `æ` characters in the historical title render legibly. |
| Apostolicae Curae | 2 | **PASS.** Both columns fit and continue correctly. Backslashes and malformed letter groups near the lower right are inherited transcription characters. |
| Apostolicae Curae | 3 | **PASS.** The historical translators' note about `Feria V.` remains visible in the right-column prose stream. It and the surrounding body fit without collision or clipping. |
| Apostolicae Curae | 4 | **PASS.** Dense text, quotation marks and dashes remain clear; there is no column or page-boundary defect. |
| Apostolicae Curae | 5 | **PASS.** The paragraph beginning `Wherefore` continues from the bottom of the left column to the top of the right. The final paragraph continues onto page 6 without dropped text at the visible boundary. |
| Apostolicae Curae | 6 | **PASS.** Closing legal paragraphs end with `these presents`, followed by references [1]–[3]. The source/repair qualification, revision and complete rights colophon fit together in the left column; no extra notice page exists. |
| French religious superiors letter | 1 | **PASS.** The long title wraps onto two centered lines within the margins; identification stays attached. The retained `II. Letter...` heading and opening `At all times...` paragraph are visible. |
| French religious superiors letter | 2 | **PASS.** Columns and page continuation are clear. The inline `Acts V. 41.` source reference remains visible in the left column. |
| French religious superiors letter | 3 | **PASS.** Body text proceeds into the right-column closing blessing and ends with `true to Us in the Lord.` The source/repair qualification, revision and rights colophon follow legibly in that column without splitting or spill. |

The beginnings and endings above were also checked against the generated
`.body.tex` files named in the assignment. The full-body text-fidelity checks
are separate receipt facts; their recorded status is `pass` for all three
documents, using `pdf-raw-whitespace-soft-hyphen-nfkc-v2`. This visual review
does not claim to have independently replayed that comparison.

## Source quality and review boundary

All three selections use artifact
`artifact.papal-collections.leo-xiii-great-encyclical-letters.1903-benziger-english.ws-encoding-repaired-ed8e5a40`.
The retained payload was independently hashed as
`ed8e5a405701a51eec9124f0e63a4db7740ded35545fe5d99874ac9581541879`.
Its [artifact record](../works/papal-collections/leo-xiii-great-encyclical-letters/editions/1903-benziger-english/artifacts/ws-encoding-repaired-ed8e5a40/artifact.toml)
declares exactly 205 encoding-only repairs across the container: 193 intact
Windows-1252 display/UTF-8 reversals and 12 partial marker repairs,
corroborated against independent OCR of the same 1903 Benziger printing.
That record preserves ASCII characters, whitespace, physical lines and source
dates and excludes lexical rewriting, dehyphenation and full print collation.
Those corroboration facts are attributed to the retained audit and artifact
record; this page review did not repeat the OCR research.

The visible final source notes accurately disclose the limited repair extent:
53 spans for Providentissimus Deus (50 intact reversals and 3 partial marker
repairs), 14 intact reversals for Apostolicae Curae, and 2 intact reversals for
the French superiors letter. All three display revision
`2026-10-26T05:10:28Z` and state that OCR word and source-date errors remain
uncorrected and full print collation is outstanding. The common rights notice
is readable, complete, and on the same final physical page as substantive
source content or retained historical references.

Providentissimus Deus in particular still contains severe word-level
corruption, stray symbols, OCR hyphenation, old running heads and page numerals,
and source references embedded in sentences. Literal filled squares in the
rendering were confirmed in the exact retained payload, including lines
1491, 1591 and 1593. Apostolicae Curae and the French letter also retain OCR
letter substitutions and intrusive note markers. These findings preclude
calling the editions clean transcriptions or image-collated texts. A visual
layout pass does not close those source-quality limitations.

There are no unresolved layout blockers for the three exact reviewed PDFs.
This report grants no whole-print textual verification, independent rights
reassessment, installation, publication, or deployment status. The prior
English review reports are preserved and concern their own earlier PDF hashes.
The detailed machine-readable coverage receipt is
`.scratch/english_encoding_review/lane-2/receipt.json`.
