# Baseline continuation visual review 08

Fresh cold review of packet `baseline-continuation-08`: **8 PDFs, 40/40 pages inspected; 6 PASS and 2 CHANGES_REQUIRED**. Every assigned page was viewed on its existing contact sheet and opened at full resolution. No prior inspection claim was inherited.

The blocking findings are note fusion in **Inscrutabili Dei consilio**, pages 3–4, and **Paternae providaeque**, page 2. These PDFs pass mechanical fidelity, but that does not resolve their reading defects. No clipping, overlap, lost column, apparatus-only final page, or ending lost from the pinned source selection was found in this packet.

## Identity and verification

- Packet: `.scratch/encyclical-ready-package/baseline-review-packets/08.json`.
- Canonical report destination supplied by the packet: `src/sources/papal-documents/encyclicals-baseline-continuation-08.md`.
- Receipt SHA-256 for all eight documents: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
- Frozen manifest SHA-256: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.
- Render revision: `2026-10-30T02:56:48Z`.
- Fresh verification completed with **163 matching SHA-256 checks**: PDF files, receipt, frozen manifest, common brief, selected source payloads, segment manifests where present, all supplied source-controller record/payload pins, raster-run manifest, every cache-pinned contact sheet/page/thumbnail, and prior-reference identity pins. Prior-reference contents were not used as inspection evidence.
- Packet source rows match the frozen manifest; receipt rows match the exact receipt. `pdfinfo` page counts match packet, receipt, raster manifest, and raster cache. The existing raster cache binds every page to the reviewed PDF hash.
- The repository's read-only `validate_document` and `pdf_body_fidelity` helpers were rerun on the selected source rows and exact PDFs with `PYTHONDONTWRITEBYTECODE=1`. All eight fidelity results match their receipt, including source presence on first and final pages. Extracted beginnings/endings were compared with the first/final page images.
- `pdfinfo`, `pdftotext`, and `pdffonts` succeeded for all eight PDFs. All listed Latin Modern fonts are embedded, subsetted, and have Unicode maps. Metadata identifies the expected title and language; PDF creation and modification dates match the tracked revision. All PDFs are US Letter, PDF 1.7. `qpdf` is unavailable, so no independent `qpdf --check` was run.

Task-local verification details, selected source snapshots, text extractions, and font listings are retained beside this report in `.scratch/encyclical-baseline-continuation-08/`. Only that scratch directory was written. There was no rerasterization, render, shared-cache write, canonical edit, installation, or Git operation.

## Exact reviewed PDFs and actual coverage

All contact sheets are `contact-sheets/sheet-001.png` under each document's exact packet `raster_dir`. All full-size images are the existing `pages/page-*.png` files under that same directory.

| Document ID / title | Language | Pages | Contact-sheet pages viewed | Full-resolution pages viewed | Status | PDF SHA-256 |
| --- | --- | ---: | --- | --- | --- | --- |
| `papal.pius-xi.hf-p-xi-enc-19221223-ubi-arcano-dei-consilio` — Ubi Arcano Dei Consilio | en | 13 | 1–13 | 1–13 | PASS | `e70d0e5d0478f70202a5fb1f5be88197d1c35075058efe95b2c79e5fd84ade69` |
| `papal.pius-xi.hf-p-xi-enc-18111926-iniquis-afflictisque` — Iniquis Afflictisque | en | 7 | 1–7 | 1–7 | PASS | `d058c2be8009350ea007df765c81e32787fbf406093f821170527a1b74381d8a` |
| `acta.ass.010.ass-010-act-011` — Inscrutabili Dei consilio | la | 5 | 1–5 | 1–5 | CHANGES_REQUIRED | `5c052b96088731122941f23dd7843b614e94a6a819faef7319ece511c442b50b` |
| `acta.ass.018.ass-018-009` — Litterae ad Archiepiscopos et Episcopos Borussiae | la | 4 | 1–4 | 1–4 | PASS | `d9e0c08179bd40d588108fbefbbe0bfd9cac81cf41934dea6f6966fcac5f7880` |
| `pius-ix-acta.volume-03.line-00000167.part-03` — Amantissimi Redemptoris — de missa pro populo | la | 4 | 1–4 | 1–4 | PASS | `bb4b5e23e50231b3dab6e589c7daea2c8d8497baba30f5a9fe743f18b1223519` |
| `papal.leo-xiii.hf-l-xiii-enc-25051899-annum-sacrum` — On the Consecration of Mankind to the Sacred Heart of Jesus | en | 3 | 1–3 | 1–3 | PASS | `5a84f7fc929cc963265c7667607d7713c3eaceb9f29d2ab4a3b61ece66538754` |
| `acta.ass.032.ass-032-l08224` — Paternae providaeque | la | 2 | 1–2 | 1–2 | CHANGES_REQUIRED | `d7e2ebeefa4940c3f8258f06d16b3a0b52898e0f08bc8f35847cd9f67fab63a4` |
| `papal.pius-ix.epistola-encyclica-ubi-prima-11-martii-1871` — Letter Ubi Prima | la | 2 | 1–2 | 1–2 | PASS | `c1ca7b01723948ca8a6b7ea74395c7140c834eca4c84ea87abef9b80c237a874` |

## Blocking findings

1. **Inscrutabili Dei consilio, page 3, right column near the top:** the historical reference `[I) E p . 138. a l i a s 5. ad Marcellinum u. 15.` runs into the body paragraph after `concordia` and before `firmior in dies`. It is composed as part of the preceding body block, interrupting the sentence rather than remaining an addressable note block. The selected source snapshot has no paragraph boundary before the reference (snapshot lines 208–209). Separate the historical note without changing its words, preserve the continuing sentence/source order, then rebuild and review the replacement bytes.

2. **Inscrutabili Dei consilio, page 4, left column in the upper quarter:** `(1) Ad Goloss. 2, 8.` is fused into the body paragraph after `At vero` and before `postquam`. It begins on the same composed line as the body and its continuation occupies the next line. The source snapshot likewise places it inside the preceding body block (lines 251–252). This is a second note-separation defect, not merely a retained misspelling.

3. **Paternae providaeque, page 2, right column after the closing:** the notes `(1) I Petr. V, 7.` through `(5) I Thess. V, 12-13.` run directly after `LEO PP. XIII.` in the same dating/signature paragraph. There is no standalone historical-note block, and the five references wrap as continuous protocol text. The selected source snapshot contains the signature and notes in one paragraph (lines 158–165). Preserve the signature and every note, give the note set its own source-grounded block, then rebuild and review the replacement bytes.

These findings were reported to the coordinator during review. The byte-faithful source/PDF comparison passes for each affected PDF; **neither affected PDF is accepted for installation**.

## Per-document findings and qualifications

- **Ubi Arcano Dei Consilio — PASS.** The title, pope/date/language, two-column order, margins, leading, and page feet are clear throughout all 13 pages. The source's OCR retains broken words, intrusive marks, and paragraph breaks, including `did|not` on page 1 and an intrusive bar within the broken `restoration` on page 13. These cause local reading friction, but the surrounding prose remains decipherable; no passage was judged meaningfully unreadable. This assessment is visual judgment as well as fidelity checking. Page 13 contains substantial historical text, the dating clause, and `PIUS XI.`; the smaller source notice continues into the right column without creating another page.

- **Iniquis Afflictisque — PASS.** All seven pages have clean column geometry and legible body type. Retained OCR includes split words, isolated punctuation, broken source paragraphs, and the stray `PP a a a` line on page 4. These are visible source-quality qualifications and do not hide a sentence or produce an unreadable passage. The page 7 blessing, dating clause, and `PIUS XI.` are present before the clearly separated terminal apparatus. No historical note was found fused into the prose.

- **Inscrutabili Dei consilio — CHANGES_REQUIRED.** The page 2 `(1) rrov. 14, 34.` reference is a distinct block, but the references on pages 3–4 fail the note-separation requirement described above. OCR corruption in the address and letter-spaced/broken words is retained and visible; layout review does not establish correct Latin. Page 5 is sparse but contains the historical closing blessing, dating clause, pontificate year, and `LEO PP. XIII.`. Its sparse layout is acceptable in itself; it is not an apparatus-only page. No clipping or ending loss was found.

- **Litterae ad Archiepiscopos et Episcopos Borussiae — PASS.** Every page is legible with clear column separation. On page 2 the Ignatius reference is its own block between the source's broken `mysterio-` / `rum`; on page 3 the Romans reference is its own block between `impen-` / `dentibus`. The interruptions follow literal source order and do not fuse notes into the body block. The typography does not falsely turn these into new semantic headings or invented footnotes. Page 4 retains the closing blessing, dating clause, pontificate year, and signature before the compact source/rights notice.

- **Amantissimi Redemptoris — de missa pro populo — PASS.** The note blocks on pages 1–2 remain visually separate from their surrounding prose. The text is legible despite retained OCR misspellings in the opening address, broken words, and occasional intrusive bars on page 3. There is no sustained unreadability, overlap, or column collision. Page 4 retains the substantive closing and the `Datum Romae...` / pontificate-year ending exactly represented by the pinned selection. Its short single-column remainder includes genuine historical text; the large blank remainder is not itself a defect.

- **On the Consecration of Mankind to the Sacred Heart of Jesus — PASS.** All three pages have orderly and readable columns. The long title fits without clipping. The body reference markers remain readable; all twelve historical endnotes are individually visible on page 3, distinct from the final blessing and the ruled-off project apparatus. The pinned selection ends with note 12; this review found no loss from that ending and does not infer an additional signature or dating clause absent from the selected text. The source note's residual-OCR and outstanding-image-collation limits remain applicable.

- **Paternae providaeque — CHANGES_REQUIRED.** Both pages are legible and geometrically clean. The historical blessing, dating clause, signature, and all five references are present on page 2, but their fused presentation fails the source-note requirement. No text ending is missing from the pinned selection.

- **Letter Ubi Prima — PASS.** Both pages have clear headings, identification, body flow, and margins. Inline patristic references remain understandable as part of the source prose. The second page retains the final blessing, dating clause, pontificate year, and `PIUS PP. IX`; the smaller source/rights notice is distinctly separated below. No note fusion or meaningful unreadability was found.

## Limits

This review covers the exact packet PDFs, their byte-bound existing rasters, and the pinned mechanically selected source text. It does not claim whole-source image collation, translation verification, independent rights adjudication, or recovery of words from historical printing. The source notes identify uncorrected OCR/transcription limits. Restricted upstream payloads were not reacquired; their supplied controller-record pins were checked. No replacement PDF bytes are covered by these statuses. Repaired readers require new fidelity, pin, and full-page visual review.
