# Independent refinement review: packet 30a

**PASS: two Latin PDFs, ten reader pages independently inspected.** Review scope is the exact finalized `notes10` replacements assigned by packet 30a, not earlier producer PDFs. No material source-boundary, fidelity, or layout blocker was found.

| Document | Exact PDF SHA-256 | Pages individually inspected | Status |
| --- | --- | --- | --- |
| `acta.ass.010.ass-010-act-011` — Inscrutabili Dei consilio | `50ebecd17d34c38a11548fe7a6a337681709122cfaac83b81eae93478d4ac325` | 1, 2, 3, 4, 5 | PASS |
| `acta.ass.037.ass-037-l023300` — Acerbo nimis, source title “L I T T E R A E E N C Y C L I C A E” | `d3f29d0a3f5d763c508bd3a518f470eb11129c0ef5b5c063dded4d535006bf18` | 1, 2, 3, 4, 5 | PASS |

The exact PDF paths are those under `.scratch/encyclical-notes-10-late/final-readers-02/` pinned in `.scratch/encyclical-refinement-package/packets/30a.json`. Both actual page counts are five. The shared receipt `.scratch/encyclical-notes-10-late/final-readers-02/receipt.json` has SHA-256 `28005d63d94eac18dbb80967f62b74655355b7ae60fd7a82d2fe1645fe399627`. The frozen manifest has SHA-256 `0bdf8490c7fbf11c9396a272f49c5d072c04e643fcdc89c437a9129f5c945c66`.

## Independent visual findings

I opened both pinned reader contact sheets, then every reader raster individually using its original resolution. All ten pages received fresh inspection; no prior visual coverage, producer acceptance, or reused page proof supplies this review. The pinned raster files were checked against their hashes and sizes without rerunning `pdf-review` or changing its output.

Identification, issuer, date and Latin language are clear on both first pages. Two-column flow, paragraph indentation, headings, note paragraphs, page numbers and terminal apparatus remain legible. I found no clipping, overlap, missing-glyph box, or material spacing problem. Source wording begins promptly after identification. The source/rights notice is visibly separated by a short rule and includes the transcription limitation and project-license boundary.

Inscrutabili's repaired Marcellinum note is a separate paragraph in page 3's right column; the Ad Goloss. note is separate in page 4's left column. The surrounding body resumes in its retained order. Its sparse page 5 retains the closing blessing, dating clause, pontificate statement and `LEO PP. XIII.` subscription before the compact apparatus. This source-bearing final page passes with a sparseness qualification.

Acerbo's Ephesians/Trent note group is a separate block at the top of page 3's right column. The source's `conside-` / `ranti` division remains around the historical note position; it has not been silently repaired or moved. On page 5, the Exodus/Peter note group is separate below the dating and `PIUS PP. X` subscription and above project apparatus. The final page is source-bearing. Other literal OCR divisions and character debris remain visible, as disclosed; this review does not authorize changing them.

## Source and native-boundary evidence

I checked exact source payloads, complete equality of each packet `source_row` with its matching frozen-manifest row, the segment controllers and metadata, and all retained artifact/spec/review payload and record pins. The current helper pins, assembly-spec pin, proposed-row pin, receipt, source-selection manifest, native parents and raster evidence pins also matched. The verification records 112 pin comparisons, including repeated shared evidence.

Both exact `tools/papal-source-notes check --spec … --out … --json` commands exited 0 with `status: pass`, preserving selected non-LF bytes and source order. A separate direct comparison of the original selected LF ranges with the derivative after removing only LF bytes also matched. The selected non-LF hashes are `2611148f92ff73999edbec1824b73351140025ae2db4496f19493766ebf8ae90` for Inscrutabili and `87244c5efc06db65791773c72977d10c4da4a33216baf627b892947ba16e6181` for Acerbo.

I read the source LF contexts and derivative empty-LF boundaries around all four repaired groups: Inscrutabili parent LF 22247 and 22290; Acerbo parent LF 23551–23553 and 23780–23781. I also inspected the selected source beginnings and endings. Substantive address/protocol, closing, subscriptions and the selected historical notes remain accounted for.

The composite native excerpt PDF has SHA-256 `e1e68152959a7e8279af2ad25d6dfcf2be9d72df01ad3ec4fa1624c314619969`. I independently opened its correct four page rasters individually at original resolution:

| Reader | Parent PDF pages | Excerpt pages | Finding |
| --- | --- | --- | --- |
| Inscrutabili | 589, 590 | 4, 5 | Smaller page-foot notes are distinct from the preceding body and agree with the selected LF boundaries. |
| Acerbo | 619, 625 | 1, 2 | Ephesians/Trent notes are below the body; Exodus/Peter notes are below the subscription. Both groups agree with the selected LF boundaries. |

For each of the four mappings I reran `pdftotext -raw` on the exact parent and excerpt page and compared full output bytes. I also reran `-bbox-layout`, serialized the parsed page element with the exact ElementTree method in `NATIVE_PROOF_METHOD.md`, and compared bytes and packet hashes. All four raw-text and geometry proofs passed; the listed lower-page note line boxes are present. Composite excerpt page 3 is the wrong-page diagnostic and was excluded from acceptance evidence.

## Mechanical verification and limits

Using the pinned current `scripts/_typeset_papal.py`, independent `validate_document` and `pdf_body_fidelity` calls passed for both readers, with source coverage on pages 1–5. The source-aware fidelity check recorded 114 permitted layout hyphens for Inscrutabili and 104 for Acerbo. Cache-disabled `tools/source-library validate` exited 0. Imports and validation ran with `PYTHONDONTWRITEBYTECODE=1` and `TRIPTYCH_LIBRARY_CACHE=0`.

`pdfinfo` and `pdffonts` exited 0. Both PDFs are unencrypted letter-size PDF 1.7 files, with the expected source title, author and Latin subject. Creation and modification times equal the pinned render revision `2026-10-30T12:46:54Z`. All four Latin Modern font subsets in each PDF are embedded and have Unicode maps. Files are 45,698 and 48,307 bytes. The actual compile logs contain the disclosed underfull boxes and five-page output, with no fatal error, undefined-reference or overfull-box finding; full-page inspection found no corresponding material layout defect.

This is bounded source-boundary, mechanical-fidelity and PDF-presentation acceptance. Native witnesses are Vatican OCR reconstructions. The review does not establish whole-source lexical collation, original-print glyph identity, translation accuracy, new rights clearance, historical intake/identity approval, installation or deployment. No separate source-intake gate is closed by this PDF PASS.

The review output is confined to `.scratch/encyclical-refinement-package/cold-review-30a/`. Root owns copying these report bytes to `src/sources/papal-documents/encyclicals-refinement-cold-30a.md` and any integration. No tracked source, producer file, PDF, shared raster/cache, manifest or release record was edited by this review.
