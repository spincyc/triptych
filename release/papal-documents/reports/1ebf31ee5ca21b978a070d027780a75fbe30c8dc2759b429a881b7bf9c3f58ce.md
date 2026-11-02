# Independent cold review 41: Arcanum, Latin

**SOURCE ORDER: PASS. PDF: PASS — one PDF, all nine reader pages freshly inspected.** The eight native page-foot note groups now follow complete left-column flow and then complete right-column flow. Each historical note starts a separate paragraph and its continuation stays with that note. The bounded blockers in cold review 34a are closed only for the exact replacement source and PDF below.

| Exact reviewed item | Value |
| --- | --- |
| Document | `acta.ass.012.ass-012-act-007`, Latin, *Arcanum divinae sapientiae*, Leo XIII, 1880-02-10 |
| Packet SHA-256 | `699b88bf39a70ea9f98e7cb61e9ea2b6a12d0ab33593b0c45350e7d0d6adc451` |
| PDF SHA-256 | `cc29fe74d31e4f8116edb2d4cb616a8b0951d4150c88b99b61f3ce67e0ee139a` |
| PDF bytes / actual pages | 71,309 / 9 |
| Selected source SHA-256 | `d28389997f6af7045924b64ab085b6e58ec7df1622060fb7675fa9909a5d484d` |
| Receipt SHA-256 | `ccfa1eab9f165422207f2b97f9a2c2b0461a7314686bd63ede420ffa4f3ac4ef` |
| Frozen manifest SHA-256 | `99d3be4108d414e4aee3b10bdc87b57c28d2ab4245f869a9fd50ab11b293351a` |
| Source-order spec SHA-256 | `ea99e02112eafae37747ae7f5a7f4197c89f813b77e8d48e453eac6079e26711` |
| Native geometry SHA-256 | `9a0a51a96db3c2b8f8dcd87776bfc4ddf882724182acc451e27a03a47b31fce3` |
| Source byte-proof SHA-256 | `29f08070f94aa56b6d1ed270288331c4c0c6d2d38d6c0c716d8d3db01d7c59fd` |
| Canonical report destination | `src/sources/papal-documents/encyclicals-refinement-cold-41.md` — left unwritten for coordinator integration |

The PDF is `.scratch/arcanum-note-order-fix/readers/1880-02-10-acta-ass-012-ass-012-act-007-59a1708c-la/1880-02-10-acta-ass-012-ass-012-act-007-59a1708c-la.pdf`. This reviewer opened the packet's reader contact sheet and every individual reader raster, pages **1–9**, at original raster resolution. All eight native excerpts, parent pages **387, 388, 389, 390, 391, 392, 393, 398**, were opened as full-page original-resolution rasters and again as reviewer-created JPEG quality-95 note-region crops. No prior visual inspection or page acceptance was reused. Cache reuse identifies raster bytes; it is not reused visual judgment.

## SOURCE ORDER verdict: PASS

The native evidence is an archival OCR reconstruction, not an original-print facsimile. Within that witness, the two note columns are geometrically disjoint and their numbered starts and continuations support the repaired order. The judgments below are fresh source-geometry judgments, separate from helper success and producer assertions.

| Native page | WORDs / byte slices | Source-order and paragraph judgment | Reader page |
| --- | --- | --- | --- |
| 387 | 33 / 4 | Left notes (1), (2), then right damaged `(S)` and (4); all four are separate paragraphs. The damaged label and `Arnot).` remain literal. | 2 |
| 388 | 53 / 6 | Left notes (1), (2), damaged `is)`, then right (4), (5). The right third row `form. matr.` continues note (5)'s `re-`; it is in the same paragraph. | 2 |
| 389 | 72 / 8 | Left notes (1)–(4) precede right (5)–(8), each separately indented. Notes remain between source body ending `Do-` and continuation `mini (.1)`. | 3 |
| 390 | 89 / 13 | Left (1)–(6), including note (6)'s `Ad-` / `monere`, precede right (7)–(9). Note (7)'s `cognât,` / `spirti.` stays together; note (8)'s second citation and note (9)'s second row also stay in their owning paragraphs. | 3 |
| 391 | 45 / 6 | Note (1)'s `Capp. 5` continues directly to `et 6 de eo aut duxit in matr.`. Note (2) begins at bottom left and continues into top right with `matr. Trid. sess. X X X I V` and `re-` / `form. matr.` in one paragraph. Note (3) starts separately. | 4 |
| 392 | 24 / 4 | Left (1), (2) precede right (3), (4), with four separate paragraphs. | 4 |
| 393 | 123 / 18 | Complete left notes (1)–(7), including multirow (5) and (6), precede complete right (8)–(15). Note (10)'s `Pest. 1 8 3 5 .` remains its continuation. Reader notes (1)–(9) finish the left column; note (10) begins the right column. The literal spaced final period wraps to the next line without changing note ownership. | 5 |
| 398 | 164 / 16 | All eight left rows form the long note (1), ending `22 Sept. 1 8 5 2 .`. Right notes (2)–(5) follow, with the multirow continuations of (3) and (5) preserved. Note (1) is complete at reader page 7 bottom; the remaining notes start page 8. | 7–8 |

Native column splits are x=210, 230, 210, 228, 210, 220, 210 and 220 pt respectively. The measured empty gutters are 80.529930, 21.858588, 52.252110, 13.056223, 14.153659, 66.037041, 12.117888 and 11.169510 pt. Every selected WORD box lies wholly in its assigned column. `verification.json` records independent equality of all 603 exact WORD values and boxes, and coordinate-derived complete left-then-right order. Native row reconstruction used a 3 pt y band for small superscript offsets, below the roughly 10 pt row separation, then ascending x within each row; it did not trust the fragmented, interleaved XML line traversal as reading order.

The spec's 75 UTF-8 byte slices exhaust every affected source-note row exactly once and every slice is emitted exactly once. Independently reconstructing the declared permutation and LF paragraphs reproduces the complete replacement source byte for byte. Independently comparing every selected non-note LF row at its actual output offset and all nine pinned unchanged prefix/intergroup/suffix regions proves their bytes and order unchanged. Their combined SHA-256 is `679de67126e3e3615d796fdb724970aa3c57bbc3e3e3b4280d0a254aadd438f7`. **Global non-LF order equality is false**, as required by a note-column permutation; no global word-order preservation claim is made.

Direct current body-TeX inspection corroborates the visual paragraphs: native 390 note (6), lines 324–325, has no intervening `\par`; note (7), lines 328–329, likewise stays together. Native 391 note (1), lines 381–382, and cross-column note (2), lines 385–387, each end in their own `\par` before the following note. Native 398 note (1), lines 737–744, stays one paragraph before the boundary at line 745. The whole retained body TeX also equals the current pinned generator's `render_body(validated)` output.

Cold review 34a's page-391 misattachment and page-390 interrupted continuations are therefore resolved for source `d28389997f6a…` and PDF `cc29fe74d31e…`. The old source `fd4fbfc32f74ef62b13b24d533120d495c404cd2405dec588f63092541993872`, old PDF `c158cde1e0458c59f65ff7a40ff8e207f9dfa410b19720682a958e99cc9f3d29`, and old 34a report/decision remain immutable **CHANGES_REQUIRED** records. This review neither edits nor retroactively accepts them.

## PDF verdict: PASS

- **Page 1:** compact identification names the incipit, Leo XIII, date and Latin. Protocol, address and salutation remain present. The all-capital source blocks, first historical note and body are legible. Two columns read normally with clear gutter and margins.
- **Page 2:** both repaired native 387/388 note groups are visibly separate, individually indented note paragraphs. Literal damaged markers, spacing and hyphens remain; no collision or clipping occurs.
- **Page 3:** repaired native 389/390 notes read in source column order. The original body interruptions around `Do-` / `mini (.1)` and `securitatem` / `personarum` remain bounded by separate notes. These historical page-break interruptions are disclosed source structure, not fused paragraphs.
- **Page 4:** native 391's note ownership is readable, including the bottom-left to top-right continuation of note (2); native 392 has four distinct notes. Body resumes after the note group as a separate paragraph.
- **Page 5:** all fifteen native 393 notes are separately addressable and their multirow citations stay together through the reader's left-to-right column transition. The original damaged strings and spaced digits remain visible. A lone wrapped period in note (10) is a minor consequence of literal source spacing and does not impair note ownership or cause overlap.
- **Page 6:** body columns, paragraph flow, margins and folio are legible; no new glyph loss, clipping or overlap observed.
- **Page 7:** the entire long native 398 note (1) occupies a single paragraph at the right-column bottom. Its rows no longer alternate with right-column notes.
- **Page 8:** native 398 notes (2)–(5) begin the left column as separate complete paragraphs before the source body resumes `sunt una consistere.`. Body and note text remain distinguishable and legible.
- **Page 9:** freshly inspected source-bearing final page retains the closing exhortation, blessing, `Datum Romae` clause dated 10 February 1880, pontificate year and `LEO PP. X I I I .` subscription before the short rule. Selected-source LF 847–857 independently account for the prayer, blessing, date and subscription. The smaller source apparatus and rights colophon remain legible below the subscription, with no dedicated apparatus-only page or overlap.

Literal OCR defects, original word-break hyphens and interletter spacing remain throughout. This mechanical reader is usable within that disclosed transcription limit; it is not a corrected Latin edition.

## Independent verification and scope

`verification.json` retains 163 successful file-pin checks, including the full parent, all eight exact excerpts, brief, current helpers, source controller, retained artifact records/payloads, spec/geometry/byte-proof/review, producer evidence, PDF/receipt/frozen manifest, review-run and cache receipts, and every listed output/cache raster. Full `source_row` equality with the matching frozen row and TOML equality with all packet controller/artifact metadata pass. Producer PASS evidence was checked as provenance, not adopted as this acceptance.

The full native parent SHA-256 is `017009649925ced58e3f51a80eac34dc0f858a8e4b06e6992bf6e663e56b8993`. For each of all eight parent pages against excerpt page 1, this reviewer freshly ran complete `pdftotext -raw -enc UTF-8` and `-bbox-layout` extraction. Complete raw stdout bytes and default-ElementTree-serialized page bytes were equal between parent and subset and matched both packet hashes, exactly following `NATIVE_PROOF_METHOD.md`. Complete bbox-output hashes and selected WORD geometry also match the retained geometry artifact.

Read-only exact replays of `tools/papal-source-order check` and the prior `tools/papal-source-notes check` pass. Current source-order helper path `scripts/_papal_source_order.py` has SHA-256 `f0a3014db485ee25ffa7df013c81e600f8e4f9eccff76b5ac7daecbc1d6a9c86`. The current pinned typesetter `scripts/_typeset_papal.py`, SHA-256 `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146`, independently passes `validate_document` and `pdf_body_fidelity`: `pdf-raw-source-aware-line-hyphen-nfkc-v3`, 46,830 source characters, 38,386 normalized characters, 206 allowed physical-line layout hyphens, source-bearing pages 1–9.

Current whole-library validation was run uncached with `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0` and exited 0: artifact=11052, corpus=5, edition=14304, passage=9532, segment=10874, work=10944, bindings=4398. Both environment variables were set before every Python import and source-library invocation in this lane. No shared cache was used, refilled, removed or restored.

`pdfinfo` parses nine unencrypted letter-sized pages with correct title, author, Latin subject and revision-derived creation/modification time; no suspect marker, form or JavaScript. All four Latin Modern fonts are embedded subsets with Unicode mapping. The final compile log contains no fatal, missing-character, overfull/underfull, undefined-reference or LaTeX/package warning. PDF size is below both repository investigation thresholds. `qpdf` is unavailable on PATH and at the personal executable fallback; no qpdf structural result is claimed.

All native rasters are 1550 × 2200 pixels for 419.55 × 595.55 pt pages. The eight fresh note crops preserve pixel scale and are JPEG quality 95, written only in this review's scratch. `crop-geometry.json` records their exact source paths, point and pixel rectangles, MIME and quality. Native source/cache bytes were unchanged. Reader and native images were transferred one per call using original image detail and automatic display detail.

This is bounded independent source-order and every-page PDF acceptance of the stated bytes. It does not establish whole-source lexical collation, original-print image identity, translation accuracy, a new historical identity/intake or rights determination, installation or deployment. Only `.scratch/encyclical-refinement-package/cold-review-41/` was written. Canonical report copying and admission remain the coordinator's work.
