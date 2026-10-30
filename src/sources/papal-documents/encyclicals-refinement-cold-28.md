# Independent cold review: finalized encyclical refinements, packet 28

Result: PASS for both assigned Latin PDFs, 8 of 8 reader pages inspected individually at full resolution. No material source-partition or layout blocker was found. This is independent review of the exact finalized packet bytes; producer acceptance and earlier PDF inspections were not reused.

| Document | PDF SHA-256 | Bytes | Pages individually inspected | Result |
| --- | --- | ---: | --- | --- |
| `acta.ass.025.ass-025-007`, *Epistola encyclica de Rosario mariali* | `3958cda4310ec831519f2397d5c270625d9104e078bd818ca0d7d01a67696c6c` | 47321 | 1, 2, 3, 4, 5 | PASS |
| `acta.ass.006.ass-006-act-011`, *Ubi Nos* | `bac451cad42c35f6a934b3fb7a061a2ac8a8d8c147fba0b95453e265ba31182b` | 38037 | 1, 2, 3 | PASS |

## Exact inputs and independent checks

All 106 unique packet file pins checked against existing bytes matched their SHA-256 and, where specified, size. This includes the current helper code, brief, assembly specification, source-selection manifest, segment controllers, source artifact records and payloads, specifications, producer evidence, native parents/excerpts, reader/native review runs, cache receipts, contact sheets, full-page images and thumbnails. The two retained source-partition review payloads and their helper/CLI hashes were checked separately against their artifact records. No changed or missing input was found.

The source rows equal their respective frozen-manifest rows and the matching combined source-selection-manifest rows in full, including Ubi Nos's `compact_layout: true`. Receipt schema, source/segment/PDF identities, page counts, render revisions and frozen-manifest pins agree. `validate_document(source_row, root=repo)` independently passed for each current source, including the selected artifact, segment schema/ranges and edition identity checks. Current whole-library `tools/source-library validate` returned exit 0: artifact=10880, corpus=5, edition=14277, passage=9140, segment=10870, work=10925, bindings=4398. Its actual invocation used `TRIPTYCH_LIBRARY_CACHE=0 PYTHONDONTWRITEBYTECODE=1`.

| Document | Selected source SHA-256 | Receipt SHA-256 | Frozen manifest SHA-256 |
| --- | --- | --- | --- |
| Rosario | `5d8e0a4e4618bc8c0a399f31f24ecf139f656ab7f2e2d8da5be360417d064a4c` | `6e0e3507bf47c915e2a3b2c0d58e0545c4e952d52723c377ce92bcfb25e7bec7` | `23079f54b84d69fc4ed453d84e204c881e0193ff3df6547133982a418428e7e2` |
| Ubi Nos | `32ae8d62360d0e1aaff37690389cb3b6a4e3cd2fe523e7fda754bd081574fc38` | `d828f82f2408244d2b7cd32e0a2852bcd6d85e4639ba6b16ea89a8ec02ecfa48` | `7c608ddbdec186a72365a4924b92a1be6d0ffddf92236ab1600c4c1c243c7817` |

Both exact read-only `tools/papal-source-notes check --spec <retained-spec> --out <canonical-selected-text> --json` replays returned exit 0 and `status: pass`, preserving every selected non-LF byte and its order. Rosario's specification is `note-spec-rosario-1e81250af05a/spec.json` under its ASS 25 edition, SHA-256 `1e81250af05a73aa36b56041c8498112105f4561a4a862aef756b6b2b2c72419`; Ubi Nos's is `note-spec-ubi-nos-61b694a3b7fb/spec.json` under its ASS 6 edition, SHA-256 `61b694a3b7fbafc482869a969100b30771877a0821dfa3f10a065b20f5798c33`. These are the exact specification paths recorded in packet 28 and `verification.json`. The output extents are 413 LF lines/22947 bytes and 270 LF lines/15331 bytes respectively. The pinned helper is `scripts/_papal_source_notes.py`, SHA-256 `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57`.

Using pinned `scripts/_typeset_papal.py`, SHA-256 `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146`, independent `pdf_body_fidelity` returned `pass` with method `pdf-raw-source-aware-line-hyphen-nfkc-v3`. Rosario has 19095 normalized source characters and 100 permitted layout hyphens; Ubi Nos has 12918 and 52. Source body coverage begins on page 1 and ends on the actual final page in both PDFs. Actual `pdfinfo` page counts are 5 and 3. Both PDFs parse without encryption or suspect flags, identify the correct title, pope and Latin language, and carry creation/modification dates matching their pinned UTC revisions, `2026-10-30T14:00:37Z` and `2026-10-30T14:15:40Z`. All four fonts per PDF are embedded, subset Latin Modern fonts with Unicode maps. Existing compilation logs contain no fatal/error, undefined-reference, overfull/underfull or warning lines.

## Native source inspection and partition judgment

The full native parents were independently hashed: Rosario `bebce8f35cead87a8dca23f31645396b5e4aa943abccd126ac9421d972ca9dd8`, 767 pages; Ubi Nos `7e480931ad07d3a53db391d2c26a69a256ca106719d0e7a6220415d3123eecca`, 776 pages. Full `pdftotext -layout -enc UTF-8 -eol unix` extraction hashes and the declared historical-line projections also reproduce the packet's parent text hashes exactly.

All 17 excerpt mappings were independently replayed: Rosario native parent pages 139–148 map to excerpt pages 1–10, and Ubi Nos pages 257–263 to excerpt pages 1–7. Complete raw UTF-8 stdout bytes and default `ElementTree.tostring` serialization of the first parsed bbox-layout page element agree between each parent/excerpt pair and reproduce every packet hash. Default namespace, ASCII character-reference and tail serialization follows `NATIVE_PROOF_METHOD.md` exactly. This establishes excerpt mapping for the identified archival OCR reconstruction.

I opened both native contact sheets and every native excerpt page individually at full resolution: Rosario 139, 140, 141, 142, 143, 144, 145, 146, 147, 148; Ubi Nos 257, 258, 259, 260, 261, 262, 263. These are actual current inspection views, not inherited producer inspection. All image calls used existing rasters, `view_image(detail="original")`, original MIME and `detail="auto"`, one image per call. No replacement rasters or crops were generated.

Rosario's parent LF groups 5816–5817, 5858–5859, 5941–5943 and 5984–5987 correspond to smaller page-foot citations on native pages 141, 142, 144 and 145. The unchanged source start at LF5693 includes the EPISTOLA title and literal isolated `i`; the selected terminal LF6097 includes the final historical citation after the dating and LEO PP. XIII subscription. I inspected those anchors, their immediately adjacent source lines and rendered TeX paragraph delimiters. The four repaired groups have explicit `\par` boundaries; the pre-existing blank within LF5984–5987 keeps the first citation separate from the second citation and retained Acta footer. No note is fused into adjacent body paragraphs. Native pages 143, 146 and 147 also confirm the already-separated notes remain at their source-page breaks. The inherited interruption `au-` / citation / `tem` is literal source order.

Ubi Nos's parent LF10203–10204 group follows body ending `tenere` on native page 257; LF10284–10285 follows `Italorum` on native page 259. Both now have explicit TeX paragraph boundaries before and after the group, matching reader pages 1 and 2. Existing Act. 4, Ep. 8/Ep. 12, Ep. 42 and terminal citation paragraphs stay separate. Native pages 261–263 confirm the inherited `glorioso-` / note / `rum` and `con-` / note / `sensione` interruptions; they are retained source order, not newly fused notes.

The Ubi Nos selection begins at parent LF10174, EPISTOLA ENCYCLICA, and includes the complete addressed-recipient lines LF10176–10178, PIUS PP. IX protocol, salutation and body. Its unchanged selected extent excludes the preceding genitive publisher supertitle at LF10166–10172 and the Acta footer LF10205. The terminal dating, PIUS PP. IX subscription and source notes through LF10440 are retained; the next act starts outside the selection at LF10441. This PASS is for that identified bounded selection and its note partition, not a new claim to reproduce every item of source publishing furniture.

## Reader page observations

Both reader contact sheets and all eight full-page images were inspected afresh. Two-column flow, heading/paragraph spacing, note legibility, clipping, glyph completeness, overlap, closing and terminal apparatus were assessed directly.

- Rosario page 1: restrained identification, pope/date/language and source opening are clear; columns and baselines remain legible. The literal isolated `i`, source divisions and literal `\n` are inherited OCR content, also visible in the native reconstruction.
- Rosario page 2: the two repaired native p141/p142 citation blocks are distinct indented paragraphs; unchanged body continuations follow in source order.
- Rosario page 3: the existing p143 citation and repaired p144 three-citation group are separate from body. The historical interrupted word remains recognizable in its literal order.
- Rosario page 4: the first p145 citation is separated from preceding body; its second citation, Acta footer and numeral `10` retain their separate source block. The existing liturgical citation also remains a separate paragraph.
- Rosario page 5: substantial source prose, the Psalm citation, closing exhortation, dating, LEO PP. XIII and final source citation precede the readable source notice and rights colophon. The empty right column is a qualified source-bearing ending, with no apparatus-only page.
- Ubi Nos page 1: compact identification, EPISTOLA, substantive address, PIUS PP. IX and salutation are readable. Has litteras/Epist. 243 is a separate paragraph after `tenere`; the existing Act. 4 citation is also separate.
- Ubi Nos page 2: S. Bern./Eiusmodi is separate after `Italorum`; the later source note between `glorioso-` and `rum` remains its own paragraph. Compact composition is legible without clipping or overlap.
- Ubi Nos page 3: the note between `con-` and `sensione` is separate. Closing body, benediction, dating, PIUS PP. IX and terminal citations are retained above clear apparatus and rights text. Substantial source text occupies this final page.

No material unreadability, missing rendered glyph, overlap, clipped baseline, incorrect column sequence, note fusion, lost closing or apparatus-only spill was observed.

## Limits and disposition

PASS covers the exact two finalized PDFs, all eight reader pages and the bounded source/geometry checks stated above. Reused visual pages: none. Reuse proofs: none. Cache reuse supplies raster bytes only and was not treated as visual acceptance. Source inspection covered the stated native excerpt pages and selected LF anchors, not a whole-volume lexical collation. Native Vatican OCR PDFs are text reconstructions; no original-print glyph/image identity, lexical correction, translation accuracy, new rights clearance, source-intake admission, installation or deployment is certified. Existing historical hyphens, OCR defects and source furniture remain disclosed limitations. Any separately owned intake or rights gate remains separate.

All review writes are under `.scratch/encyclical-refinement-package/cold-review-28/`. Final machine evidence is in `verification.json`, including actual command results, hashes, mapping proofs and inspection extent. `reviews.json` names this report's intended canonical copy at `src/sources/papal-documents/encyclicals-refinement-cold-28.md`; that target was not written by this reviewer.
