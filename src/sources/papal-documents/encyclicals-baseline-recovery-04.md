# Independent cold review — baseline recovery 04

Complete packet: 2 PDFs, 15 of 15 pages freshly inspected. Result: Libertas PASS (10 pages); Rosary CHANGES_REQUIRED (5 pages). No page inspection or acceptance is inherited from earlier contexts.

## Libertas — PASS

- Identity: `papal.leo-xiii.hf-l-xiii-enc-20061888-libertas`, Latin, 10 pages.
- Exact reviewed PDF SHA-256: `3d9d9acfcfa2b45a351a34363475fffe503c6872971cee8d59657756a27a7b7d`.
- Fresh contact-sheet inspection: pages 1–10; fresh full-size raster inspection: pages 1–10. Reused pages: none.
- Restrained title/pope/date/language identification is clear. Both columns remain legible, justified and in normal reading order. The all-capital historical protocol uses restrained ragged-right lines. No meaningful clipping, overlap, stretched heading, orphan/widow or note-legibility defect was seen.
- Page 10 retains substantive body, blessing, dating clause and `LEO PP. XIII` before the small ruled terminal source/rights apparatus; it is source-bearing, not apparatus-only. Pinned source literal-LF lines 81 and 83 correspond to body.tex lines 129–133: the date ends with `\par` and the subscription is its own ragged-right paragraph. The source opens at LF line 1 with the historical encyclical protocol. Inline references remain readable; no fused historical note block was observed.
- The two recorded underfull-box warnings concern the opening protocol paragraphs; fresh page 1 inspection found no material spacing or containment defect.

## Epistola encyclica de Rosario mariali — CHANGES_REQUIRED

- Identity: `acta.ass.025.ass-025-007`, Latin, 5 pages.
- Exact reviewed PDF SHA-256: `265c82ab5015fa8fa61aae050a58726a17eb95aa2e5bb2fdb01c81f21b807a45`.
- Fresh contact-sheet inspection: pages 1–5; fresh full-size raster inspection: pages 1–5. Reused pages: none. No replacement PDF was inspected.
- Identification and columns are clear, text is contained, and no clipping or overlap was seen. The source retains numerous internal OCR word divisions. Page 1 right column visibly prints a literal backslash-n; source LF5765 and body.tex79 (`\textbackslash{}n`) prove that this is retained source content. This is an OCR qualification, independent of the blocking note-layout finding.
- Blocking historical-note fusion: on page 2 left, the text ending `dulcissimum, in` continues directly into the S. Th./Hebr. note group. Source LF5815–5817 maps to body.tex129–131, with no `\par` before the notes and only body.tex132 after them. On page 2 right, `lumine contingat` continues into Hebr./Ioann. notes: source LF5857–5859, body.tex171–173, with only body.tex174 ending the paragraph. Both full-size loci visibly run notes into body text.
- The same confirmed defect occurs on page 3 right after `Quis ergo`: source LF5940–5943, body.tex255–258, followed by `\par` at259; and on page 4 left after `referentes`: source LF5983–5984, body.tex298–299, followed by `\par` at300. These are attached note paragraphs, not findings based solely on an interrupted sentence.
- Separate notes also occur and are not classified as fusion: page 3 Iac. note (source LF5901; TeX214–217), page 4 Ex sacr. liturg. (LF6029; TeX344–347), and page 5 Psalm note (LF6071; TeX387–390) each have explicit paragraph boundaries before and after. Their positions interrupt `au-/tem`, `valde/tribuimus`, and `Omnibus/autem` respectively, which alone does not fail the clarified criterion.
- The sparse page 5 is source-bearing: substantial closing, blessing, dating clause, `LEO PP. XIII`, and a final Ecclesiasticus note precede compact ruled apparatus. The subscription ends at TeX415, and the final note occupies TeX417–418, corresponding to source LF6097. The source opens with the historical protocol at LF5693 and stray retained `i` at5694. The final page does not fail merely for its blank right column.

## Verification and limits

`pin-verification.json` records successful programmatic checks for both documents: exact PDF hashes and actual pdfinfo page counts; receipt, frozen-manifest, source, body.tex, segment where applicable, and pinset hashes; exact sidecar receipt/frozen rows; every source-controller record and available tracked payload; original packet hashes; raster-run identity and renderer agreement; and all 32 listed contact/page/thumbnail hashes and sizes. Restricted upstream payloads were not available for independent hashing. Physical source line numbers count literal LF only; form-feed adds no line. Both PDFs report four embedded, subset Latin Modern fonts with Unicode mappings. Receipt source-fidelity results pass for the exact PDFs; that recorded mechanical check was verified as pinned evidence, not independently rerun. Libertas has two recorded underfull warnings, assessed visually on page 1; the Rosary receipt has none.

This is layout review of exact retained bytes, not full historical source collation, certification of wording/translation accuracy, rights clearance, or original-print facsimile fidelity. Libertas is an uncollated normalized web transcription; the Rosary text is a Vatican OCR reconstruction of the identified ASS25 witness. No prior checkpoint review was inherited. No rendering, rasterization, installation, source change, or tracked-file/Git mutation was performed. Detailed actual observations and source/TeX note contexts are retained in this lane's scratch evidence.

Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Canonical report target: `src/sources/papal-documents/encyclicals-baseline-recovery-04.md`.
