# Independent cold review 49 — Inter praecipuas

**Bounded SOURCE SPACING/NOTES: PASS. Exact five-page reader PDF: PASS.** No material blocker found. This is independent review of the exact replacement bytes below; producer observations and previous visual reviews were not reused as acceptance.

| Identity | Exact value |
| --- | --- |
| Document / language | `acta.ass.009.ass-009-act-035` / `la` |
| Act | Gregory XVI, *Inter praecipuas*, 1844-05-08 |
| Packet 49 SHA-256 | `7cca7992a2c2680eb89d6bbdb6076e5c0c569e7a03acb54aad828ba0135ca197` |
| Reviewed PDF SHA-256 | `29da4b5f459b2879feb528aad505462794c3a80c774e43c34eedd6cbe2a21e9c` |
| Actual PDF extent / size | 5 pages / 48,108 bytes |
| Selected source SHA-256 | `85105d054e156fab4f5e1913e15886656fbbfc19f792dd4134d60680bc78d584` |
| Receipt SHA-256 | `4788f6923ae13d3a80f1d02ce6730e76dc2e648c11054f8110b3b7c796825ad3` |
| Frozen manifest SHA-256 | `e337d3e02f7ada434b39c90c3f886a2304024c5353523453b0f8d698e77dc40b` |
| Render revision | `2026-10-30T17:40:07Z` |

The canonical report destination is `src/sources/papal-documents/encyclicals-refinement-cold-49.md`; this reviewer has not written it. Review artifacts remain solely in `.scratch/encyclical-refinement-package/cold-review-49/` for coordinator admission and copying.

## Independent byte and source checks

The packet brief, current helper pins, selected source, full frozen row, segment controller, artifact metadata and payloads, recipe, note spec, source-specific preparation code, maps, author handoff and its final producer erratum, receipt, PDF, and listed review inputs passed 119 exact pin checks. The segment and artifact metadata were parsed independently and compared in full with the packet. The selected source row equals the matching frozen-manifest row in full. Receipt source/PDF hashes, extent and manifest pin agree. All 38 listed reader/native output rasters and the corresponding 38 cache files passed independent size and SHA-256 checks; cache identity and renderer fingerprint agree. These checks establish raster identity, without importing visual acceptance.

The complete 690-page native parent is SHA-256 `a849b1d96a2ec47f4d8286f565c8040f0e48e3b34f8e5df7e42d4e0b7d33ea05`; the 13-page excerpt is `4a19151bd71a0a5697b2972cc1cc36cabce038db53f382c5551c6207f0610055`. For each parent page 644–656 and excerpt page 1–13, this reviewer independently replayed complete `pdftotext -raw -enc UTF-8` stdout and `-bbox-layout` page serialization exactly as `NATIVE_PROOF_METHOD.md` specifies. Every raw-text and default `ElementTree.tostring(page)` hash matched both the parent/excerpt bytes and packet. A fresh complete parent-page-644–656 bbox extraction also exactly reproduced retained bbox SHA-256 `9567a67dc499ad1a2befa6e9a5cc92d23494847d95810417979a31a1985c5b3c`.

The source-specific preparation code was read and executed into this reviewer's scratch. Its artifact declares MIT under repository `LICENSE`; the current helpers are MIT project software, distinct from the historical source wording. Exact-yMin grouping, xMin ordering and the 2.2pt gap threshold reproduced both native line witness `93809ebe57edb09e8c8e55dd0d98e87630779d47e4aa60199d2b3ef771949b86` and WORD map `cd56064d1258c256c9e016c1cedfc60b5c6c1f870d0d82032626de023a41d485`. All 5,910 native WORD values and coordinates were independently accounted for once. Maximum joined gap is 1.814670pt; minimum separated gap is 2.535390pt. No below-threshold joined pair contains a multi-character WORD. Actual native pages show single body columns and separately positioned page-foot notes, supporting the distinction between letter runs and word spaces.

The page-654 claim in earlier producer review `d2e412da3c3d…` that `edoceanturquod` was one fused WORD is explicitly superseded by final producer review SHA-256 `7a009d1b6e111759fa103164855332bb4b02e944eae672ad96629b8263b8943a`. Independent geometry confirms separate `edoceantur` and `quod` WORDs at yMin45.897000, with xMax296.521430 and xMin307.161950: a 10.640520pt gap. Their space is correctly present in the source and reader page 4. The superseded assertion has not been inherited.

Current `papal-source-notes` check and scratch derivation both reproduce `41c8cb04aeb865dfaa1def992d77a9f4e1df1cd7ec011add2e59d182a1f77f50`. Current `papal-native-spacing` check and scratch derivation both reproduce the selected source `85105d054e15…`. Independent replay also reproduces the exact 466-entry projection map `7ea7960a131ead1c5d930c2a09061acd1c73a152ca0af4f3f47c0548f48f2c75`. There are 445 unique native LF matches, with no native line identity reused, no substantive unmatched LF, no stream-order difference and no unstated exception. All 515 physical LF records, blank-line positions, per-line nonwhitespace and whole nonwhitespace order remain unchanged by spacing restoration.

The 21 explicitly retained numeral-only LF records are 91, 102, 105, 109, 117, 120, 127, 129, 131, 156, 158, 170, 177, 179, 182, 197, 210, 224, 227, 238 and 271. Each retains exact original bytes and its declared repeated native match count. None is assigned a native occurrence identity. They are the complete exception set.

All eight historical note groups match complete, distinct source paragraphs after whitespace restoration. Their native regions were directly inspected in the full-resolution source rasters; reader paragraph boundaries were checked visually and against the exact source blocks.

| Historical source LF group | Native page | Reader page(s) | Actual disposition |
| --- | --- | --- | --- |
| 24361–24363 | 644 | 1 | Jerome reference, separate paragraph; body resumes separately |
| 24401–24404 | 645 | 1 | Two references, one source-note paragraph |
| 24438–24458 | 646 | 2 | Eight references, separate from preceding and following body |
| 24495–24504 | 647 | 2 | Note paragraph crosses columns; body resumes after its end |
| 24541–24548 | 648 | 2 | Separate reference paragraph before body continuation |
| 24574–24595 | 649 | 3 | Long note including Italian quotation, distinct from body |
| 24628–24634 | 650 | 3 | Previous note's continuation remains its own paragraph at source interruption |
| 24782–24783 | 654 | 5 | Leonis XII reference is separate between body `ad-` and `ducere` |

Fresh current whole-library validation ran with `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0`: exit 0, `source-library valid: artifact=11108 corpus=5 edition=14304 passage=9532 segment=10882 work=10944 bindings=4398`. No historical sibling error was imported. All actual source replays and Python source-library loads used both flags. Initial CLI help-only probes omitted them and did not invoke the source-library loader; their imports may have refreshed Python bytecode outside this reviewer's scratch. That possible bytecode write was not measured or reversed. The source-library cache was not used or restored.

## Fresh every-page reader decision

The exact native contact sheet and all 13 full native page rasters 644–656 were opened and inspected afresh. This covers protocol, body/letter-run geometry, all note regions, page-654 word spacing and the closing/appendix boundary. The exact reader contact sheet and all five full reader page rasters were likewise opened and inspected afresh. Every image used its original MIME, `view_image(detail="original")` and automatic image display detail, one image per call. The 20 actual views, exact raster hashes and contemporaneous dispositions are recorded in `actual-views.json`; no previously inspected page was reused.

| Reader page | Decision and direct observation |
| --- | --- |
| 1 | PASS. Clear title, pope, date and Latin identification; substantive addressee/protocol retained. Readable two-column order. First two note groups are distinct indented paragraphs. No clipping, overlap or glyph loss observed. |
| 2 | PASS. Dense but readable columns; note groups 3–5 remain distinct. The four-reference group crosses the column boundary normally, ending before the next indented body paragraph. |
| 3 | PASS. Large note with Italian quotation and separate continuation block remain distinct from resumed body. Literal OCR `1916`, hard hyphens and reference marks remain disclosed. No note/body paragraph fusion observed. |
| 4 | PASS. Full body in both columns, normal reading order, correctly separated `edoceantur quod`; no new false WORD join or residual pervasive interletter spacing observed. |
| 5 | PASS. Final historical note has its own paragraph. Substantial source body continues through paragraphs 14–16, dating and `GREGORIUS PP. XVI`. Readable source apparatus and rights colophon share the same page in the upper right column. It is source-bearing, with no apparatus-only final page. |

The native page-656 subscription ends before the unrelated `APPENDIX`; the latter is excluded from the selected source and reader. The opening protocol and closing agree with the exact selected source. Notes remain at their native source-page interruptions, including the interrupted word around the final note; that literal historical extraction order has not been silently rearranged.

Independent `validate_document` and current `pdf_body_fidelity` replay passed: 23,948 source characters, 20,134 normalized source characters, 115 permitted layout hyphens, and source coverage on reader pages 1–5. `pdfinfo` confirms five unencrypted Letter pages, expected title/author/Latin subject and creation/modification time matching the tracked render revision. All four Latin Modern fonts are embedded subsets with Unicode maps. The actual retained final compile log contains no fatal, undefined-reference, overflow or warning matches. PDF size is below both publication-size review triggers.

## Review limits and delivery

PASS is bounded to these exact bytes, mechanical whitespace restoration, explicit LF note boundaries, native OCR geometry and fresh visual usability of every reader page. Vatican native pages are archival OCR reconstructions, not original-print facsimiles. Literal OCR spelling, hard hyphens, markers and source interruption order remain; no whole-source lexical collation, original-print image identity, translation accuracy, new rights clearance or broader intake approval is asserted. The existing declared United States historical-text distribution basis and license boundary were checked for consistency; this review does not expand them.

All deliberate review writes remain in this reviewer's scratch; the initial help-probe bytecode uncertainty is disclosed above. No source, canonical report, producer artifact, manifest, installed PDF or Git state was edited, and no delegation occurred. Coordinator admission, canonical copying and any installation remain outside this reviewer's lane. `verification.json`, `source-audit.json`, `actual-views.json`, helper outputs and `reviews.json` retain the reproducible review evidence. No unresolved material source/layout finding remains within this assigned scope.
