# E supremi Latin — independent cold acceptance review

PASS for `acta.ass.036.ass-036-l004837` / `la`, all five pages of the exact candidate PDF. This source-readonly review independently inspected the actual native witness pages and reader pages and replayed the acceptance checks. It does not depend on producer visual conclusions. No blocking finding remains within this document's review scope.

Reviewed 2026-10-30. Intended canonical report target: `src/sources/papal-documents/encyclicals-notes05-cold-e-supremi-la.md`. This scratch report does not write that target. Only `.scratch/notes05-cold-recovery/e-supremi-la/` was written; no source, helper, inventory, release, install, shared manifest or Git changes were made. No delegated work or live process remains.

## Exact reviewed bytes

| Item | Path / SHA-256 |
| --- | --- |
| Scope | `.scratch/notes05-cold-recovery/scope-pins.json` — `01c23a6fc4456089f7bd00f5956c937963d32914b7aa4b4dd5ca0fdce49128d6` |
| Producer manifest | `.scratch/encyclical-notes-05-finish/manifest.json` — `ca12f96e8dbec6dc938a69d1b92c02b469c70b7225e4d810c719beacd8fcf488` |
| Frozen manifest | `.scratch/encyclical-notes-05-finish/render/frozen-manifest.json` — `ca12f96e8dbec6dc938a69d1b92c02b469c70b7225e4d810c719beacd8fcf488` |
| Receipt | `.scratch/encyclical-notes-05-finish/render/receipt.json` — `fce1af199380be667fbc94f0cecedc094f27f2c211098fc36ee193096d639302` |
| Reader | `.scratch/encyclical-notes-05-finish/render/1903-10-04-acta-ass-036-ass-036-l004837-19df11d9-la/1903-10-04-acta-ass-036-ass-036-l004837-19df11d9-la.pdf` — `1c71e4dc9485e07d5c5e78f9fdde4fef46b5784c7d3580715998702240bb81ec`; 50,627 bytes, five pages |
| Source derivative | `src/sources/works/holy-see/acta-sanctae-sedis/editions/1903-acta-ass-036/artifacts/note-blocks-e-supremi-la-33101aa16b39/text.txt` — `33101aa16b39c37fc278d4ffebc89f50799e5a10b86934bfdc7aa7d62af0b412` |
| Partition spec | `src/sources/works/holy-see/acta-sanctae-sedis/editions/1903-acta-ass-036/artifacts/note-spec-e-supremi-la-3762e762458a/spec.json` — `3762e762458abd7f4433ccc541268db991153291153e6fea133758398a4910e7` |
| Parent | `src/sources/works/holy-see/acta-sanctae-sedis/editions/1903-acta-ass-036/artifacts/acta-historical-text-2e2ac41b/historical.txt` — `2e2ac41b82e92ef6a68a6bd1d4c768933ebadf42a8c74f3103755ac13fd762cb` |
| Native full witness | `.scratch/papal_pius_x_review/ASS-36-1903-4-ocr.pdf` — `4d5577b47b26023818a4219fc9e089c3425a066056638aa2c16013990fd87d27` |
| Native excerpt | `.scratch/encyclical-notes-05/acta.ass.036.ass-036-l004837.native.pdf` — `e1b46e4dd031a23b08db782948c9e5d26d86680c4e412bd6e8ce457ec94ffbdc`; excerpt pages 1–11 map to native artifact pages 129–139 |
| Replay helper | `scripts/_papal_source_notes.py` — `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57` |
| Renderer | `scripts/_typeset_papal.py` — `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146` |
| Raster run | `.scratch/notes05-cold-recovery/e-supremi-la/rasters/review-run.json` — `5fc9566c62fc4e0bd45008a037aa08a5339fef0c82e0864e28c68816c97229d8` |

The exact controller is `segment.acta-papal-archives.ass.036.ass-036-l004837.note-blocks-33101aa16b39`, owning `artifact.acta-papal-archives.ass.036.historical-text-2e2ac41b.note-blocks-e-supremi-la-33101aa16b39`. The current source/spec payloads, adjacent artifact records and segment match all five scope path/hash pins. Manifest and frozen manifest bytes are identical. The complete document rows are equal, including correction evidence; segment/artifact IDs, hashes, paths, language, edition, selected ranges, rights basis and receipt pins agree. The supersession preserves the prior raw parent and segment. The older installed typography is outside this candidate's approval; this review authorizes only the reader hash above.

Complete manifest document keyset: `artifact_id, correction_evidence, date, document_type, edition_id, id, language, physical_line_ranges, pope, revision, rights_basis, rights_notice, rights_status, segment_id, segment_path, sha256, source_note, source_url, text_path, title, work_id`.

Complete receipt document keyset: `artifact_id, body_tex, changed, id, language, pages, pdf, pdf_sha256, physical_line_ranges, render_revision, segment_id, source_sha256, status, stem, tex, text_fidelity, warnings`.

## Source extent and native evidence

I individually viewed the full `tools/pdf-review` page rasters for native artifact pages **129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139**, each via `view_image(detail="original")`, one image per call. These are page-layout observations of the identified Vatican OCR delivery; the source is an OCR reconstruction. There is no original-print or lexical collation claim.

Native129 shows the title, addressees, `PIUS PP. x`, salutation and `E supremi apostolatus cathedra` opening. The original selection starts at parent LF4831, retaining all of that source text. The excluded LF4857–4858 are the issue/footer and next running head. The eleven complete selected page pieces retain the prior selection's body, notes, blessing, actual dating clause and subscription without new exclusions. Native139 ends with the blessing, `Datum Romae apud S. Petrum, die iv octobris MCMIII`, `PIUS PP. X` and six final notes; LF5281 `(6) Dan. m , 39.` is the exact selected end. The following Italian version begins outside the bound. No neighboring act, running head, issue footer or modern wrapper has entered the selection.

Every listed note range is geometrically a page-foot group in the actual native page viewed. Reader inspection and a separate exact-block check establish both paragraph boundaries for all ten groups:

| Native artifact page | Parent physical LF | Reader location | Before / after note paragraph |
| --- | --- | --- | --- |
| 130 | 4897–4899 | 1 right | `verum conscii` / `Nobis infirmitatis` |
| 131 | 4937–4941 | 2 left | `furore religionis` / `pietas ubique` |
| 132 | 4979–4985 | 2 right | `moeror, quum` / literal `îiomines videant` |
| 133 | 5023–5027 | 3 left, top | `Chrysostomus: Spes` / `tua Ecclesia` |
| 134 | 5067–5069 | 3 left, bottom | `formetur Chri-` / `stus in vobis` at 3 right, top |
| 135 | 5106–5111 | 3 right | `aut semirationalismi` / `errores invehere` |
| 136 | 5150–5154 | 4 left | `maior sit ignorantia,` / `ibi etiam latius` |
| 137 | 5191–5197 | 4 right | `sed voluntati.` / `Attamen, Venerabiles Fratres` |
| 138 | 5237–5238 | 5 left | `obtentis, optimates` / `ac locupletes` |
| 139 | 5276–5281 | 5 right | `PIUS PP. X` / end of source, rule and project apparatus |

Each group exactly matches one whole source paragraph. The boundaries preserve source order even when notes interrupt a sentence or split `Chri-` / `stus`; the notes do not fuse with either body side. Literal reference marks and source word divisions remain unaltered.

## Every reader page inspected

I individually viewed **1, 2, 3, 4, 5**, in full-page rasters, at original detail. No pages were inherited, reused, skipped or accepted from a contact sheet. The title, issuer, date and Latin language identification are legible; the source protocol and opening remain present. Both columns continue in normal reading order. No clipping, overlap, missing-glyph boxes, body-note fusion or materially unreadable sustained OCR run was found. The sparse right side on page5 contains genuine source dating, subscription and notes before the terminal source/rights colophon; no apparatus-only page is introduced. The terminal colophon discloses OCR, exact LF partition, retained notes, excluded furniture and the absence of image collation.

Non-blocking source qualifications: literal OCR has damaged words/glyphs and number forms, including `rag ¿tus`, `îiomines`, `M e s`, malformed note numerals and an isolated `3` near `Dei (5)` on page5. Spaced source word fragments and hyphens remain visible. The surrounding Latin is readable; these are retained source limitations, not newly corrected readings. The long reproduced title is restrained within its area. The only compile diagnostic is one underfull box in the source all-capitals protocol; it produces no visible clipping or overlap.

Reader raster hashes:

- Page 1: `d299083911055d65f6b0d23304642737101bef3d80d52164d9895ce281b55160`
- Page 2: `b5efa89494c9cb342ee42957973b1efd2db45e122e62412da4049b21780b2e50`
- Page 3: `9f3e2e411432d7a58da1ff89d348a8de12fff648ddc1e8878da64bf76df7a015`
- Page 4: `b31721998606eb9058142f8e7cb320a07903c6cfe29816390fd7352f961701f3`
- Page 5: `4b953cc6cc334c7597368c19cf9c2590dd04dc141615a31353f55c2952636229`

Native raster hashes (artifact page / excerpt page):

- 129 / 1: `9cb4f0cc45c4a8ef5c6fe68f2a975d1a4428f78611d8a63c45174f77eca4a8a8`
- 130 / 2: `e30d233bf250810aee2f4da872eb9ecc3424a3b92d1e9528d0238ea129285db8`
- 131 / 3: `b7a969938564c6a338384013fc790828a53d26c3904f390a2acffb14fdba00d3`
- 132 / 4: `e22c9f60e3b511f73f6e34318bdf261971c4dd339e7005852dc63e3670e3cea2`
- 133 / 5: `ff46908cc7d1561aab1e80069d135d74fcba59ed57b81e20065aeaa9387af2e1`
- 134 / 6: `dfba225c869a5bedc3b3a6b8e05998b454c44eb59ea694276d27cb068fa705b3`
- 135 / 7: `e3bb8f679266bd36502db0d8cefa06eb2969b1f0e496758bc6db3f404571579c`
- 136 / 8: `7ca0a11d32ae29f95a8c3de274a8c88abb2e016ea4d83489f71295b8467105b7`
- 137 / 9: `f18e90cf1a6eb9bfbd57745dc5b3352ce55a82535d0267e31bf3443a31df7174`
- 138 / 10: `2ae63c737de13ed21bca9445709fdb2aca3d4da2144bab23da1a3f30d010bb9d`
- 139 / 11: `5363b8089012a912b5444adb8b369e5bde4f896e19d797313c4a802deebde1da`

## Independent mechanical checks

Every Python/repository-tool invocation used `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0`. All following checks passed with exit0 or equivalent successful direct API return:

- `tools/papal-source-notes check --spec src/sources/works/holy-see/acta-sanctae-sedis/editions/1903-acta-ass-036/artifacts/note-spec-e-supremi-la-3762e762458a/spec.json --out src/sources/works/holy-see/acta-sanctae-sedis/editions/1903-acta-ass-036/artifacts/note-blocks-e-supremi-la-33101aa16b39/text.txt --json`: ten groups, 23,704 bytes, 470 physical lines, exact expected output hash; selected non-LF bytes and source order preserved. Independent removal of only LF bytes from the original selected pieces and derivative also gives equality, SHA-256 `39ca3f08f6a1b6d98372f0745deb008aebdfe336836a7a54d00312ea57a2ce36`.
- Direct tracked `_typeset_papal.read_manifest` and `_typeset_papal.pdf_body_fidelity` over the exact reader: `pdf-raw-source-aware-line-hyphen-nfkc-v3`, pass; 23,669 source characters, 19,551 normalized characters, 86 permitted physical layout hyphens, source pages1–5 of5. The independently obtained result equals the frozen receipt's complete fidelity object. The validated document has27 paragraph blocks.
- Whole-library uncached `tools/source-library validate`: `source-library valid: artifact=10885 corpus=5 edition=14277 passage=9140 segment=10871 work=10925 bindings=4398`. Exit0. No graph validation qualification remains in this lane.
- `pdfinfo`: five unencrypted letter pages, no JavaScript or form, author Pius X, subject Latin source edition, revision timestamps equivalent to `2026-10-30T11:44:50Z`.
- `pdffonts`: all four Latin Modern subsets embedded, with Unicode maps. Existing XeLaTeX log has no fatal, undefined-reference, overfull-box or missing-character diagnostics; one underfull box as qualified above.
- Fresh `tools/pdf-review` render run completed successfully for both the five-page candidate and eleven-page native excerpt, with output and cache wholly under this lane's scratch directory.

Evidence files alongside this report: `pins.json`, `mechanical.json`, `note-boundaries.json`, `final-checks.json`, `observations.txt`, `source-library.txt`, `pdfinfo.txt`, `pdffonts.txt`, `tex-log-check.txt` and `rasters/review-run.json` with page rasters. The existing repository helpers were reused, never copied. These checks did not rerender or install a reader and did not create a new handoff package or ZIP. This is the completed bounded review response; the coordinator owns promotion and release disposition.

Review JSON row keyset is exactly `findings, history, id, individually_inspected_pages, language, limitations, page_rasters, pages, pdf_sha256, raster_run_sha256, receipt_sha256, report, report_sha256, reuse_proofs, reused_pages, status`. No remaining handles or required source corrections.
