# Independent cold review: packet 50 — Latin Editae saepe

**SOURCE SPACING: PASS. SOURCE NOTES: PASS. PDF: PASS (10/10 fresh pages).** No material source-spacing, note-partition, fidelity or layout blocker was found within this bounded review. Source admission, canonical copying, installation and publication remain the coordinator's decisions. English and Italian Editae editions are outside this review.

Reviewed on 2026-10-30. Document `acta.aas.002.archive.aas.002.048`, Latin, Pius X, 1910-05-26. Packet SHA-256: `2b6793f5e72e74f7955f67dbb7c0c5ad521bd7934c1e42e46c9915250462c046`; brief SHA-256: `6a1aa4da7df4b21b53617a1065405644d5f3ae08fccb0e02adbbb3fbe08d221d`.

## Exact reviewed inputs

| Input | SHA-256 |
| --- | --- |
| Ten-page reader PDF | `5035b5162de126cd7ca1036b7b6da0de13475a618bcd704bd7076a6913b9310a` |
| Reader receipt | `a2ee275ce92e2b203a6cb7947791f1e1b7d97d40a1433a713309de5a9cdb8b8e` |
| Frozen and source-selection manifests | `3d76a2359226e54ad1c577ac80c49f227684f39c94122d198393f04ba406cb9d` |
| Selected source text, physical LF 1–1231, 51,372 bytes | `0d59d43d582b1c2630784de1b45d184db34eb9513a05f92949c9d460a38d0811` |
| Segment controller | `2784520418ba74fbacfa5052ac64d6a1c6eb2dfec655cae483df24c30585885e` |
| Spacing recipe | `82945a6bfaf83ec98280638babe90d99024a5125402903f2a881099345f1b5ac` |
| Spacing line map | `0efd6bc01bc9390b9fd6492d64f10b8aa4cfa7702ebf86feca7e9ab763429395` |
| Spacing derivative | `4feabb339f68e410d61cccefd89e20e80387ffa26f22edceab8ccefe05a2b220` |
| Note-partition specification | `44f1e5fc47860db8a209698bf7abc3b62cfffc776c11dbc89b520f2e45916f0f` |
| Native WORD-line text | `b6b6babb43f326e6987758b053462c07af9f7b2f30cdb9f2eb26ceba7535ad06` |
| Native WORD map | `11e5d120720be8742ec5863c5aa9939a842e709dc53c5782180634e553f5f256` |
| Native bbox artifact | `ea5147bc07a0b26dde714cd8bb16e61d4aef8632a7f590db54fea5efe053b503` |
| Full native parent PDF | `e1d32b09f7d61312089738aacb8ca4fb15e940a5bf93948278a67b09cf145b24` |
| Native 24-page excerpt | `91af54f52983c6859466ded4670e7ee6a6f84c465cf866fd2c068712f96fe8a0` |

The PDF is `.scratch/inter-editae-native-finish/editae/readers/1910-05-26-acta-aas-002-archive-aas-002-048-518c037a-la/1910-05-26-acta-aas-002-archive-aas-002-048-518c037a-la.pdf`. Its receipt and frozen manifest are in that `readers/` directory. The selected artifact is `artifact.acta-papal-archives.aas.002.editae-latin-native-finish-notes-0d59d43d582b`, controlled by `segment.acta-papal-archives.aas.002.archive.aas.002.048.editae-latin-native-finish-0d59d43d582b`. The selected source row equals the matching frozen-manifest row in full, with render revision `2026-10-30T17:44:06Z`. Segment and artifact TOML metadata also equal their packet snapshots. All 126 recorded file pins passed; both complete raster cache objects and their materialized outputs were independently checked. Renderer fingerprints and cache keys were recomputed.

## Bounded source spacing decision

The controlling witness is a Vatican archival OCR/text reconstruction of AAS 2 (1910), native artifact pages 357–380. I independently replayed every parent-page/subset-page raw-text and bbox mapping using `NATIVE_PROOF_METHOD.md`: complete `pdftotext -raw` stdout, and the first XML `page` serialized with default `ElementTree.tostring`. All 24 pairs equal each other and the packet's exact hashes. Fresh parent bbox pages also equal the retained bbox pages.

Before replay I read the retained source-specific MIT geometry implementation. Its path is `src/sources/works/holy-see/acta-apostolicae-sedis/editions/volume-2-1910/artifacts/editae-latin-native-finish-geometry-code-b687a14e7bc7/replay.py`, SHA-256 `b687a14e7bc75a271847491cbbb9824ef42c24697f855b112de745df1ce00a0a`. Running it into reviewer-owned scratch reproduced both complete WORD text and WORD map byte for byte. All **14,597 native WORD objects occur exactly once**, with unchanged values. Independently comparing original and mapped WORD-value/coordinate multisets also passed.

The grouping uses native LINE yMin within 3 points, separates fragments below 4 points high from normal lines, sorts WORDs by x within a row, and joins only adjacent single-character WORD values with gaps below 2 points and an alphanumeric participant. Complete WORDs stay separated. The actual replay made 7,538 such joins, maximum joined gap 1.96733 points, and yielded 1,013 native lines. The full-page views below show why separating the small marker rows from body and citation rows matters. This is source geometry evidence, not a lexical correction rule.

Independent recipe replay and a separate per-source-LF match-count/identity audit established:

| Disposition | Count |
| --- | ---: |
| Uniquely corresponding source LF lines receiving native whitespace | 831 |
| Explicit `preserve_original` LF lines | 153 |
| Of those, marker/numeral-only records | 151 |
| Of those, duplicate citation records | 2 |
| Preserved records with exact native match count 2 | 136 |
| Preserved records with exact native match count 1 | 17 |
| Reused native line identities | 0 |
| Undisposed or substantively unmatched selected source LF lines | 0 |
| Native stream-order difference pages | 0 |

The two duplicate citation records are original physical LF **15896 and 15902**, native page **368**, both `Conc. Prov. V, Pars. I.` with exact native match count 2. They remain literal without claiming unique native identity. Numeral strings likewise do not establish marker identity, even for the 17 with one textual match. These are valid explicit exceptions, not missing substantive text. No zero-exception requirement was imposed.

All **39,475 original non-whitespace characters and their order** agree across the selected raw source ranges, spacing derivative and final note derivative. Literal hard hyphens and inherited OCR readings remain. No source words or new note anchors were supplied.

## Bounded source notes decision

The note helper replay passes exactly: 83 groups, 1,231 final physical LF lines, with every non-LF input byte and source order preserved. I independently checked each of the 83 specified note groups against a complete separate final source paragraph. The transformation adds 166 LF bytes to the 1,065-line spacing input.

Fresh source inspection comprised both native contact sheets (overview of all 24 pages), full individual pages **357, 365, 368, 372 and 380**, and individual bounded note regions on **358–364, 366–367, 369–371 and 373–379**. Thus every native note region was actually inspected, including the absence of page-foot notes on 364. Reviewer-created JPEG95 crops retain their exact source raster hashes, dimensions and crop rectangles in `native-note-crops.json`; source rasters were unchanged. Each image was opened alone with original resolution and automatic display detail.

| Native artifact page | Historical notes |
| --- | --- |
| 357–364 | 3, 6, 2, 2, 4, 2, 2, 0 |
| 365–372 | 8, 1, 3, 7, 1, 5, 5, 4 |
| 373–380 | 3, 7, 4, 4, 5, 3, 1, 1 |

The native notes are visibly separate from body text and retain their preceding source order. I specifically checked the repeated citations on 368, the damaged 1/2/5/1 note-label sequence on 372, the starred IOAN. label on 377, and the final Unigenitus note on 380. Their literal labels and readings are retained. In the reader, source-page notes can interrupt a continuing body paragraph and can cross a column boundary; they remain distinct paragraphs. No note/body fusion was found.

## Independent PDF decision

The reader contact sheet and **every individual page 1–10** were freshly opened at full raster resolution. There is no inherited visual acceptance: `reused_pages: []`, `reuse_proofs: []`.

The restrained title, issuer, act date and Latin identification are clear. Two-column order, paragraph starts, source note separation, margins and page feet are usable throughout. No clipping, overlap or visible glyph loss was found. Page 4's eighth note continues at the top of the next column as its own paragraph. Short uppercase citations sometimes use the documented flush-left treatment.

The only compile warning is the recorded underfull hbox, badness **1009**, on page 1. I judged the actual page: some loose word spacing remains, but the paragraph is legible and has no clipping or overlap. Source hard hyphens and OCR marker interruptions remain visible as disclosed source limitations.

Page **10 is source-bearing**: it retains the closing blessing, `Datum Romae` dating clause, `PIVS PP. X` subscription and final `Bulla « Unigenitus »` historical note before the source apparatus and compact rights colophon. Its sparse single-column ending is acceptable; there is no apparatus-only spill page.

Independent `validate_document` followed by `pdf_body_fidelity` from the pinned current typesetter passes: **10 pages**, 39,475 normalized source characters, **202 permitted layout hyphens**, source first/last pages **1/10**. Original source hyphens were not globally discarded. `pdfinfo` confirms the title, Latin subject, Pius X author, revision-bound dates, unencrypted letter-size PDF 1.7, **73,188 bytes**. All four fonts are embedded, subset and Unicode-mapped Latin Modern fonts. The compile log contains no fatal, undefined-reference or missing-character warning.

Current helper pins were checked without making code archives:

| Repository helper | SHA-256 |
| --- | --- |
| `scripts/_papal_native_spacing.py` | `7c7393f6b366bc986e7d106d217a769fabba5a48edd645a7bd02b463eb64d82c` |
| `scripts/_papal_source_notes.py` | `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57` |
| `scripts/_typeset_papal.py` | `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146` |
| `scripts/_papal_source_order.py` (pin checked; not used) | `f0a3014db485ee25ffa7df013c81e600f8e4f9eccff76b5ac7daecbc1d6a9c86` |

Read-only CLI checks of the exact spacing recipe and note specification both returned exit **0**, status **pass**. A fresh current whole-library command, `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0 tools/source-library validate`, returned exit **0**: `artifact=11108 corpus=5 edition=14304 passage=9532 segment=10882 work=10944 bindings=4398`.

## Limits and ownership

This accepts the bounded mechanical whitespace/note operation and the exact rendered PDF. It does not establish original-print glyph identity, whole-source lexical collation, translation accuracy, new rights clearance, broader historical-source admission, installation or deployment. Original OCR spelling, hard hyphens, marker interruptions and damaged note labels remain explicitly disclosed. Producer review was treated as evidence to check, not reused acceptance.

Procedural limitation: three initial help-only tool invocations omitted the bytecode/cache environment guards. No source-library load is known from them, but implicit bytecode writing cannot be excluded. No shared cache was repaired, removed or restored. Every substantive Python import, source replay and validation used both guards; the final whole-library result is uncached.

Only `.scratch/encyclical-refinement-package/cold-review-50/` was intentionally written. `verification.json` records exact pins, source dispositions, native maps, CLI receipts and validation; `inspection-log.json` records the actual views and page decisions. The target `src/sources/papal-documents/encyclicals-refinement-cold-50.md` remains unwritten by this reviewer.
