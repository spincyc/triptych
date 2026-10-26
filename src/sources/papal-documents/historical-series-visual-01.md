# Historical papal series: first Continuatio layout review

Reviewed on 2026-10-26. The historical-series reviewer inspected every full-page
raster of the three exact PDFs below, using one `tools/pdf-review` invocation.
This is a visual review of the mechanical two-column editions, not complete
facsimile collation, historical authentication, or publication approval.

The frozen typesetting receipt is
`.scratch/typeset_pipeline/continuatio-0001/receipt.json`, SHA-256
`f16afc1c51f2342468d99e9badedb37384688e4c8dd0fee5e1133cec6c8a15ce`.
Its input manifest SHA-256 is
`21d10c03da097ddc781330435aa07f30a825ed0fa793a2320311729b98099cc6`.
The independent mechanical receipt audit also passed source, TeX, PDF, support,
font and text-fidelity checks. Each row retains revision
`2026-10-26T12:15:11Z`.

| Exact witness | PDF SHA-256 | Pages inspected | Layout result |
| --- | --- | --- | --- |
| `bullarium-continuatio.volume-04.line-00142853.part-02` | `e200fc462eabe5ce0d7f1858ce81ae682790955a1349108f0651fa6116d3b212` | 1–4, individually | PASS with source qualifications |
| `bullarium-continuatio.volume-04.line-00144009.part-01` | `e74b0f5e2755786f5723c158c69426061dfff59c1b9636b2c0246016e821c9b8` | 1–2, individually | PASS with source qualifications |
| `bullarium-continuatio.volume-04.line-00145044.part-01` | `59890d5d913713ddd297dd234c49d211c4f95817ae8341d4e5cd247ce0647b69` | 1, individually | PASS with source qualifications |

The first witness has a readable two-line title above two columns, consistent
column widths, clear folios, and no physical clipping, overlap, missing visible
glyphs or blank inserted page. Its fourth page ends naturally in the left
column, followed by compact source and rights notes. Historical marginal
summaries occur as separate source blocks among the body paragraphs. The
reader notice records the disagreement between its marginal date and final
dating clause; the normalized date remains absent.

The second witness has a readable two-line title and date, continuous two-column
body on page 1, and a short natural final page. The complete source/rights notice
is legible on page 2. Its historical synopsis, marginal date, source running
matter and literal OCR spelling and line-end hyphens remain visible. No clipping
or overlap was observed.

The third witness fits on one page. The title and issuer are readable, the two
columns have a clear gutter, and the ending, detached own marginal summary,
source notice and rights colophon all fit without collision. The notice clearly
qualifies the retained detached summaries. No clipping or overlap was observed.

All three remain uncorrected and uncollated OCR witnesses. Broken words,
historical marginal blocks, source running titles/page numbers and OCR errors
are source limitations, not certified editorial readings. Sparse final-page
space is the natural ending of these separate acts. This review does not assert
that the entire historical collection is reconstructed or that the source text
has been authenticated.

A separate targeted native-layout recheck confirmed the distinction between
these retained marginal blocks and inline body-word fusion. Its exact receipt
SHA-256 is `fce0b5f7372ed7d3377b1b277758355d193714a2d44d3f0a75a69ed186934a88`.
For CCCXXXI, CCCXXXII and CCCXXXIV respectively it identified 422/130/58
nonempty body LF lines and 62/12/14 own-margin LF lines: none shares a selected
source LF or native XML LINE, and no selected body WORD lies in its page's
own-margin band. The recheck uses the whole 609,730-token TXT/XML equality and
exact 25,627-token tail map. It handles each leaf's actual coordinate shift and
confirms body, incorporated decree, subscriptions and dating continuity. Its
complete factual findings are embedded in the durable JSON audit; it is still
not a complete print-glyph collation. The frozen packet and PDFs did not change.

The raster run is retained under
`.scratch/historical_series/visual/continuatio-0001/`; its `review-run.json` and
the per-PDF `review-cache.json` files pin every page raster and the renderer
fingerprint. The durable JSON audit records their exact SHA-256 values.
