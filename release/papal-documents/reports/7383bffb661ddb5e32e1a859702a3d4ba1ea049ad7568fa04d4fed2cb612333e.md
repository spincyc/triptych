# Historical English PDF visual review, group 3

Review date: 2026-10-26. This record covers eight mechanically typeset English
source editions from the 1903 Benziger collection, totaling 53 pages. Every
page listed below was opened individually at the PDF-review tool's full
2200-pixel raster size and visually inspected. Contact sheets were not used
as a substitute for page inspection.

Final disposition: **PASS for all eight editions**, using the seven current
hashes in the identifier-continuity table and the final Officiorum hash
recorded below. The two rejected Officiorum iterations remain in this record
as review history.

The initial reviewed PDFs were below
`.scratch/typeset_pipeline/english-final/`. Each table stem identifies the
relative PDF path `<stem>/<stem>.pdf`. The review rasters were generated with
`tools/pdf-review --output .scratch/english_visual_3/rasters --jobs 2`, passing
the eight assigned PDF paths. The tool's `review-run.json` independently
recorded the same eight PDF hashes and page counts. Each PDF's SHA-256 was
also recomputed directly before review and matched the assignment receipt.

| Work | PDF stem | SHA-256 | Extent inspected | Initial result |
| --- | --- | --- | --- | --- |
| Providentissimus Deus | `1893-11-18-papal-leo-xiii-hf-l-xiii-enc-18111893-providentissimus-deus-ec8dd363-en` | `9dc276c46d3b363ff52942fa20d1b3eb3e9ac09e7b2457bf03389ad03aaf1c22` | All 12 pages, 1–12 | PASS |
| Sapientiae Christianae | `1890-01-10-papal-leo-xiii-hf-l-xiii-enc-10011890-sapientiae-christianae-e74b25b5-en` | `b8307b4a23bd0ea04721b2d69e1a96f6786835b9dee4d74831cca8b933867320` | All 10 pages, 1–10 | PASS |
| Humanum genus | `1884-04-20-papal-leo-xiii-hf-l-xiii-enc-18840420-humanum-genus-1c6966f6-en` | `17492ce51265ed22fef786ced00ed1305c0f6baf9dfe444c79046d6d5ab34586` | All 8 pages, 1–8 | PASS |
| Au milieu des sollicitudes | `1892-02-16-papal-leo-xiii-hf-l-xiii-enc-16021892-au-milieu-des-sollicitudes-c9538ed1-en` | `e6af7aaf2933e147a4fafec4b77bce217a55e953a9ffa72805bc00659e3fdb0f` | All 6 pages, 1–6 | PASS |
| Tametsi futura prospicientibus | `1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-en` | `32b8bc752ab169850adba40799ae43605c00ba1344eb9169721fc138dc8ed9b8` | All 6 pages, 1–6 | PASS |
| Officiorum ac munerum | `1897-01-25-papal-leo-xiii-hf-l-xiii-apc-18970125-officiorum-ac-munerum-5f33d1e2-en` | `dab783c86db09ea7eb5c76613f9755b9c8880ed4e4fb2f35749007a626e3a712` | All 5 pages, 1–5 | CHANGES_REQUIRED |
| Quarto abeunte saeculo | `1892-07-16-papal-leo-xiii-hf-l-xiii-enc-16071892-quarto-abeunte-saeculo-ca29ac08-en` | `5bf8a7ca62316c6fad4906d065344013fe684c03c6bd8c7b6ce477219476a54b` | All 3 pages, 1–3 | PASS |
| Letter to the superiors of religious orders and institutes in France | `1901-06-29-papal-historical-leo-xiii-french-religious-superiors-letter-1901-06-29-8d4968a4-en` | `093b2b7e36731fab14b9ec4db9b8d07bb2ccdf00310e4fd15e7b1ca61b7e9f13` | All 3 pages, 1–3 | PASS |

## Identifier continuity for the seven unchanged layouts

After initial visual review, the typesetting owner repaired the English
PDFs' deterministic trailer identifiers, which had inherited one common
container-based value. A final identity check detected the changed hashes.
The review was carried forward only after an independent exact-byte replay:
each pre-change file was hashed and matched against its individually reviewed
hash above; each current file was hashed against the replacement receipt;
and each file was required to contain exactly one `/ID` array within its last
2048 bytes. Replacing only the two 32-hex-digit identifiers with equal-width
zero identifiers made the complete old and new PDF byte streams identical.
No page stream, font, date, cross-reference entry, or other PDF byte was
excluded from the equality comparison.

The replay passed for all seven rows below. Their original full-page visual
reviews therefore cover the current display bytes without a second visual
inspection. Page counts and review extents remain those in the initial table.
The common normalized digest in each row is SHA-256 of both equal byte
streams after that precise replacement. The detailed replay receipt is
`.scratch/english_visual_3/identifier-equivalence-replay.json`.

| Work | Current PDF SHA-256 — PASS | Common identifier-normalized SHA-256 |
| --- | --- | --- |
| Providentissimus Deus | `187f337dce7f957833e8e07beb805af29c1dbea5884071f1e29e6d238f0d94c9` | `cde329f6479f6862ad497a4e338150659ad28ae24e0a287589129ff3c773b187` |
| Sapientiae Christianae | `fe725ab48bf831b5ad814bc84d81bdcfe6cb54c0a47d8e4ca3f837830bbe67a6` | `9f19db2593ec8a57664162e710dd7713505827561733d3f7c0d6586c0fe62d6c` |
| Humanum genus | `cc6cf4369a67a1e2aeb1b899c7818d329bd6aee34cb75889f173faca8816e5cf` | `262e90f60014bfd8cb10de0140a483f5c4793cf6903ec4b32a7a3dac689619ef` |
| Au milieu des sollicitudes | `04368480d58f19a3306955e1b38268682810f7780fb956e406b81ce22c2e68f9` | `dca5ce6be2a9bbefde0ccf25855a6821d4495e35db254a27ac5adbeac2e12156` |
| Tametsi futura prospicientibus | `bb2517e7ea051b7df4540503314984e7ca5841b68fba3455c968a6b3665645f0` | `a4936c83bd9ef677a9ec9f7431bb1f3e6d250fd432c5b1b18ee082ed649129d1` |
| Quarto abeunte saeculo | `c63ec554fe988bec1a012e2fc806cda2ec9ecaee58032ffcaa438339644d1528` | `50e92a90cab241bd9b2a4c821151ad5a52d9e4aa85b0744f0f41606c532dd13c` |
| French superiors letter | `9a5410548a9e00966b9aff3e97944ecb27b2f49e3988f0f9e2892ecb9fec8f9d` | `fce4c9a37a7fa5db9b1cbbd5949c72deb19ed22f75e7be3e701a430c2972cafc` |

## Required correction

**Officiorum ac munerum, page 4:** the left column ends with the complete
heading chain “ARTICLE II.”, “Of the Censorship of Books.”, “CHAPTER I.”,
and “Of the Prelates entrusted with the Censorship of Books.” Its first
numbered paragraph, 30, begins at the top of the right column. Keep the
heading chain with the beginning of that paragraph. This finding concerns
column composition, and does not call for changing the retained wording.

The typesetting owner confirmed the finding. The original Officiorum bytes
above remain CHANGES_REQUIRED; the final correction below supersedes them.

### First Officiorum correction: CHANGES_REQUIRED

The replacement PDF with SHA-256
`72d800eb2fd6fee691d904f99170dd17f9c0e72431c87e441760af01b39a8ce6`
retains five pages. All five were individually opened and inspected after
generation through `tools/pdf-review` into
`.scratch/english_visual_3/rasters-revised-officiorum/`. Its hash was
recomputed directly and matches the raster receipt.

Page 4 now keeps the entire Article II / Chapter I heading chain with
paragraph 30 in the right column. The changed flow creates a different
heading split on page 5: “CHAPTER V.” and most of its subtitle end the left
column, while the subtitle's final word, “Decrees.”, stands alone at the top
of the right column before paragraph 47. Keep this entire heading and
subtitle with the paragraph's start. No other layout defect was observed in
the replacement; its final-page source and rights notice remains intact.

### Final Officiorum correction: PASS

The final replacement PDF has SHA-256
`d00cc902c119265005658cdf6c13b1868a5f8e06085834ac170fa914416cece6`
and five pages. Its exact bytes were hashed directly and matched the
PDF-review receipt. All five final pages, 1–5, were individually opened at
full raster size after generation through `tools/pdf-review` into
`.scratch/english_visual_3/rasters-final-officiorum/`.

Page 4 now places the complete Article II / Chapter I heading chain at the
top of the right column followed immediately by paragraph 30. Page 5 places
Chapter V and its complete subtitle together at the top of the right column
followed immediately by paragraph 47. The other article and chapter headings
remain attached to their text. The sequential column flow, all page margins,
and the final-page source and rights notice pass; no further clipping,
overlap, missing-glyph boxes, heading split, or apparatus-only spill was
observed. This final hash supersedes both rejected Officiorum hashes above.

## Page findings and limits

- All eight initial PDFs have genuine sequential columns, consistent readable
  type, ample margins, and unclipped page numbers. No overlap, clipped body
  text, missing-glyph boxes, or collision between body text and terminal
  notices was observed on any page. Officiorum's page-4 heading chain is the
  sole composition defect identified.
- Each final page includes the source identification, transcription limit,
  revision, and compact rights colophon with source content or historical
  notes on the same physical page: Providentissimus 12; Sapientiae 10;
  Humanum 8; Au milieu 6; Tametsi 6; Officiorum 5; Quarto 3; French
  superiors letter 3. No PDF ends with a project-apparatus-only or rights-only
  spill page. Providentissimus page 12 carries historical endnotes [5]–[17]
  above the notice; Sapientiae page 10 carries the ending and historical
  endnotes, including the long note 32 continuing normally between columns.
- Providentissimus visibly retains substantial source-transcription damage,
  particularly on pages 5–8 and 10–11: garbled word sequences, stray
  punctuation/carets, and disrupted historical citation lines. Pages 4 and 6
  also contain inherited running-head and source-page-number debris inside
  the text. These reduce the usefulness of those passages as readable source
  wording. They are not clipping or font-rendering failures. The final-page
  notice expressly declares residual OCR errors and outstanding full image
  collation; the layout PASS must not be cited as a clean-transcription or
  source-verification judgment.
- Tametsi and the French superiors letter also visibly retain OCR punctuation,
  broken words, and citation lines within prose. Their terminal notices make
  the same transcription limitation explicit. No source wording was silently
  corrected during this review.
- Quarto page 1 displays the catalog date 1892-07-16 in the identification and
  the source transcription's 1902 date in its retained heading. The terminal
  notice on page 3 explicitly states this discrepancy. The two dates were
  not harmonized, and their declared disagreement is not a layout failure.

This was visual review of the rendered editions. It did not collate wording
against the historical page images, verify a translation, resolve source
dates, or repeat the separate mechanical body-text-fidelity check. All PASS
results are limited to the exact hashes and page extents recorded above.
