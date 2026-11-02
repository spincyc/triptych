# Historical English reading editions: visual review 4

Reviewed on 2026-10-26. **PASS for visual layout: eight PDFs, all 53 pages.**

The reviewed editions identify Leo XIII as author and the 1903 Benziger
English edition as their historical source. The assignment identifies their
common transcription artifact as
`artifact.papal-collections.leo-xiii-great-encyclical-letters.1903-benziger-english.ws-reading-text-fc16a357`,
with SHA-256
`fc16a357008f7f2e1b0f331dceecc6ae76138b370a19665208fb064677cf6573`.
These are mechanical source reading editions, with no AI translation.

## Extent and method

Each physical page listed below was opened individually with `view_image` at
original raster detail. The repository's `tools/pdf-review`, with two workers,
produced the full-page rasters at a maximum dimension of 2200 pixels.
Contact sheets were not used as a substitute for individual page inspection.
Review covered column flow, margins, clipping, missing-glyph boxes, overlap,
heading placement, source notes, density, and final-page source and rights
notices. The visual review did not perform full word collation against page
images of the historical edition.

The assignment's PDF hashes were checked independently before rendering and
again after inspection. `pdfinfo` page counts, raster counts, and the
PDF-review receipt matched the assignment for all eight PDFs. The assignment
also reports zero compilation warnings and passing whole-body mechanical text
fidelity; those supplied results are distinct from this visual inspection.

The input root was `.scratch/typeset_pipeline/english-final/`; each PDF is at
`<stem>/<stem>.pdf`. Review rasters and the helper's receipt are under
`.scratch/english_visual_4/rasters/`.

## Exact reviewed bytes

| Work | PDF stem | Physical pages individually inspected | PDF SHA-256 | Result |
| --- | --- | --- | --- | --- |
| *Immortale Dei* | `1885-11-01-papal-leo-xiii-hf-l-xiii-enc-01111885-immortale-dei-ce994b60-en` | 1–10, 10 pages | `a6da164c52312e926e8de11fedbd58a88c9f78d9f5b1be34af58497692e1360d` | PASS |
| *Libertas* | `1888-06-20-papal-leo-xiii-hf-l-xiii-enc-20061888-libertas-38226778-en` | 1–10, 10 pages | `936e272112c4eb22e90a8de7b4701511851c4ee38f8900333d57ae638615c2bc` | PASS |
| *Arcanum* | `1880-02-10-papal-leo-xiii-hf-l-xiii-enc-10021880-arcanum-75869473-en` | 1–9, 9 pages | `d5ba69ba1450026408f57fc8d548ec4cea498136b32c22d8a24eadbc465bae5d` | PASS |
| *Exeunte Iam Anno* | `1888-12-25-papal-leo-xiii-hf-l-xiii-enc-25121888-exeunte-iam-anno-5d01d084-en` | 1–6, 6 pages | `77f78f6e3847e25f6240a24fb9634129b53dca3d5da0468fb28ee388be31fea2` | PASS |
| *Apostolicae Curae* | `1896-09-13-papal-leo-xiii-litterae-apostolicae-apostolicae-curae-13-septembris-1896-3faf90d2-en` | 1–6, 6 pages | `1f82f3dd3b4e709db06f70f6d224bd4c8250141ad8e7adfe31a0a514e0e38aec` | PASS |
| *Quod Apostolici Muneris* | `1878-12-28-papal-leo-xiii-hf-l-xiii-enc-28121878-quod-apostolici-muneris-e71ca4ec-en` | 1–5, 5 pages | `dbe57f618f34fdbc982c7a3d4358b69d21a057e23271f53ff7e75ef6169ac5a9` | PASS |
| Letter to the Archbishop of Paris | `1900-12-23-papal-historical-leo-xiii-paris-archbishop-letter-1900-12-23-260d4c26-en` | 1–4, 4 pages | `f008fd0a7a2618f97235c24d1cc3d463307c360a63dcc4aaa1e3c5b2e4be54b1` | PASS |
| *Vigilantiae Studiique* | `1902-10-30-papal-leo-xiii-hf-l-xiii-apl-19021030-vigilantiae-studiique-74bd6ebe-en` | 1–3, 3 pages | `ac814015782b0ad86c0c07f5ea4ff5030060a585928e3367d7db5ab1833da051` | PASS |

## Page findings

All page spans in this table describe pages inspected individually. No page
showed clipped text, overlapping text, a visibly missing renderer glyph, or a
heading stranded from its following text. Body type is dense but readable,
with clear separation between the two columns and ordinary left-column then
right-column continuation. Partial final pages retain that normal flow.

| Work and exact pages | Findings |
| --- | --- |
| *Immortale Dei*, p. 1 | Compact title and clear author, act date, and language precede the source text. The columns begin below the identification without collision. |
| *Immortale Dei*, pp. 2–8 | Continuous, readable columns with intact outer and lower margins. The anomalous `v/rites` on p. 7 is visible transcription wording, not clipping. |
| *Immortale Dei*, pp. 9–10 | The body ends on p. 9; historical note [1] begins there and notes [2]–[26] continue on p. 10. The final page carries substantial historical source notes, followed by a compact, legible source notice and rights colophon. It is not a project-apparatus-only spill. |
| *Libertas*, p. 1 | Clear title and edition identification; source title and dating line wrap legibly within the left column. |
| *Libertas*, pp. 2–9 | Both columns remain readable and within their margins; quotations and note references cause no collisions. |
| *Libertas*, p. 10 | Closing body, historical notes [1]–[7], and source notice occupy the left column. The short common rights colophon continues at the top of the right column on the same physical page. It is readable and unclipped, without another page. |
| *Arcanum*, p. 1 | Title and identifying line are clear; source text starts promptly below them. |
| *Arcanum*, pp. 2–7 | Readable continuous body columns, including inline references. |
| *Arcanum*, p. 8 | The closing paragraph begins on the last line of the right column and continues on p. 9. This isolated paragraph-opening line is a minor typographic observation; it does not obscure text or reading order. |
| *Arcanum*, p. 9 | Closing body and historical notes [1]–[24] fit with the source notice and common colophon in the left column. No apparatus-only page follows. |
| *Exeunte Iam Anno*, p. 1 | Long title fits without clipping; the dated source heading wraps legibly. |
| *Exeunte Iam Anno*, pp. 2–4 | Dense but readable text, clear gutters, and intact lower margins. |
| *Exeunte Iam Anno*, pp. 5–6 | Closing body and notes [1]–[8] are on p. 5; notes [9]–[25] continue on p. 6. The compact notices follow those historical notes on p. 6. The final page is source-note continuation, not a notice-only spill. |
| *Apostolicae Curae*, p. 1 | Clear compact identification and readable columns. Retained source corruption is conspicuous, including mojibake in the right column. |
| *Apostolicae Curae*, pp. 2–5 | Column flow and margins are sound. Frequent retained split words, stray symbols, and mojibake affect textual smoothness. The historical translators' note on p. 3 remains visibly bounded by its source brackets, although it interrupts a sentence as the retained transcription does. |
| *Apostolicae Curae*, p. 6 | Closing clauses, historical notes [1]–[3], source notice, and colophon share the final page and remain readable. |
| *Quod Apostolici Muneris*, p. 1 | Title fits on one line; compact identification and source dating line remain distinct from the body. |
| *Quod Apostolici Muneris*, pp. 2–3 | Columns are legible and flow normally without collisions. |
| *Quod Apostolici Muneris*, pp. 4–5 | Closing body and notes [1]–[7] occupy p. 4; notes [8]–[19] continue on p. 5 with the compact notices. The sparsity on p. 5 is a short historical-note continuation, not a project-apparatus-only page. |
| Paris letter, p. 1 | Title, date, and language fit clearly. Source section headings `ORIGIN AND OBJECT` and `SERVICES TO CIVIL SOCIETY` remain with following text. Retained OCR and split words are visible. |
| Paris letter, pp. 2–3 | Continuous readable columns. Occasional corrupt or internally split words are visible source-quality limitations. |
| Paris letter, p. 4 | Several closing body paragraphs and both compact notices share the final page. No text is clipped and no notice-only page follows. |
| *Vigilantiae Studiique*, p. 1 | Long title fits within the page; source heading wraps across two lines. Columns are clear. Source OCR includes a visible malformed word near the opening and retained internal splits. |
| *Vigilantiae Studiique*, p. 2 | Column margins and readable type remain intact. A retained split of `questions` into separate paragraph fragments is conspicuous in the right column; this is source segmentation, not lost or overprinted type. |
| *Vigilantiae Studiique*, p. 3 | Closing source paragraphs and both compact notices fit in the left column. Internal word splits remain visible; the final page is not apparatus-only. |

## Source-quality boundary and disposition

The final source notices identify a historical English web transcription,
unidentified individual translator, residual OCR errors, and outstanding full
image collation. Those notices are legible in all eight PDFs. In particular,
the anomalous punctuation and `â€` sequences observed in *Apostolicae Curae*
also occur in its retained body TeX, so they are not evidence of a PDF font
failure. Split words are also conspicuous in the Paris letter and
*Vigilantiae Studiique*. This review preserves those limitations and does not
silently correct the source or promote the transcription to image-collated
status.

No visual-layout change is required for these exact bytes. The minor paragraph
opening on *Arcanum* p. 8 is nonblocking. The source-quality observations remain
bounded transcription qualifications, and the PASS does not establish textual
accuracy against historical page images. No PDF, transcription, or generator
was changed during this review.
