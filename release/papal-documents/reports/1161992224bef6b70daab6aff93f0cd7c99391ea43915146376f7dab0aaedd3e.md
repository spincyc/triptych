# Independent cold review 35 — Sancta Dei civitas

**Source-order disposition: PASS. Four-page PDF disposition: PASS.** These are separate judgments, supported by independent native-image/geometry review and every-page reader review respectively. No material source-order or rendering blocker was found within this packet's bounded scope.

Only the current Latin reader for `acta.ass.013.ass-013-act-006` was reviewed. Earlier Sancta intermediates and the already-cleared Ubi/Litteras readers are excluded.

| Exact input | SHA-256 / extent |
| --- | --- |
| Current reader PDF | `84b257b54d9bd60b480420a2de91eb7f0bac671beddf7665f626c4051f1fab2c` — 4 pages, 41,739 bytes |
| Current complete selected source | `d85f33f3fdd01425f34066f2e3ce1cf68ef175dab51c55ae867a905db1075d5e` — 17,834 bytes, physical LF rows 1–304 |
| Render receipt | `422d075bb37c5d21f55a3c4c7d48be9c3f522b5fbef3a85ea27f093c0ddad449` |
| Frozen manifest | `4da26875c4a497d32470cc197e6df2ba88b5ac7803af833009534555ab9926c5` |
| LF partition spec | `a90c26f72c8a2dae0eda7ca01263a303c4739a171a83a270de028c992e664bd7` |
| Retained LF intermediate | `f1534dd74c508578b768004f97918249b69457b7d789587c10364b54335fe40a` |
| Source-order spec | `08fa6bbd1f67efcadaeb13e7e441dfc3864002422c65a367a6b99ca4a8194218` |
| Native note geometry | `2e1c0994a13f9a874600670658da4bf1c39adab62496935956785409f000dd3f` |

The PDF is the packet's `sancta-final-readers/1880-12-03-acta-ass-013-ass-013-act-006-6ac2d4e6-la/1880-12-03-acta-ass-013-ass-013-act-006-6ac2d4e6-la.pdf` under `.scratch/encyclical-notes-09-early/`. The canonical report destination is `src/sources/papal-documents/encyclicals-refinement-cold-35.md`; this reviewer wrote only its exclusive scratch copy.

## Independent source-order judgment

I opened the retained native contact sheet and native actual pages 241, 242 and 248 individually at original raster resolution, using excerpt pages 1, 2 and 8. Native page 242 visibly contains **three notes in the left column and two in the right column**. Its complete left column precedes its complete right column. The current reader's page 1 presents that order as five distinct note paragraphs: left Rom., Luc., I Cor.; then right Matth./Luc. and Act. Literal damaged labels `1`, apostrophe, `s`, `*`, `8` remain literal; no replacement label or inferred anchor is introduced.

I independently extracted native242 WORD geometry from the exact parent PDF. All 25 selected WORD values and boxes equal the pinned geometry. Every box lies wholly to one side of x=200pt. Left xmax=155.775266pt and right xmin=236.68pt leave an empty **80.904734pt gutter**, so none of these words joins the columns. Native WORD strings in the declared column order equal the unchanged output slice strings with only ASCII spaces ignored.

The eight source slices cover every byte of LF-intermediate rows 89–94 exactly once, without overlap or gap. Their output order is `left-marker1`, `left-note1`, `left-note2`, `left-marker3`, `left-note3`, `right-note4`, `right-marker5`, `right-note5`. The byte-48 cuts on LF90 and LF91 follow existing ASCII spaces and immediately precede literal right-column `*` and `8`. All bytes outside this group, including every BODY LF record and the terminal LF, remain unchanged and ordered. The retained review's body hash `36a0b8282ce5c97d4009259abbf941b27b80658fdc6256e21d4d76a4814acd79` also matches its LF-row-join serialization, which excludes the final LF; exact terminal-LF preservation was checked separately through complete prefix/output/suffix equality.

The earlier Isaias note at historical LF9230–9231 is separately partitioned by the LF stage. Native241 shows it at the page foot; reader page 1 shows its own paragraph between the preceding body and the following continuation. Direct inspection of the generated body TeX confirms `\par` boundaries around this note, all five native242 notes, and the resumed body. This is source-page note placement, with no fusion into the adjacent body paragraph.

Both read-only stages were independently replayed with the pinned current tools: `tools/papal-source-notes check --spec <a90c-spec> --out <retained-f153-text> --json`, then `tools/papal-source-order check --spec <08fa-spec> --out <current-d85-text> --json`. Both returned `pass`. LF-stage selected non-LF bytes equal the historical selection exactly. Source-order acceptance additionally rests on the native image and geometry judgment above; it is not inferred from these replay or fidelity results.

## Four-page PDF judgment

I opened the current reader contact sheet and **each page 1, 2, 3 and 4 individually at original resolution**. No pages or prior visual acceptance were reused.

| Reader pages | Finding |
| --- | --- |
| 1 | Title, pope, date and Latin label are clear; protocol/address remains present. Initial Isaias and all five reordered notes form distinct paragraphs. Columns and page foot are clear. |
| 2–3 | Normal left-column then right-column continuation, consistent margins and leading; no observed clipping, overlap, lost rendered glyph, or collision with page numbers. Literal OCR/interletter spacing and word damage remain conspicuous but legible as disclosed source defects. |
| 4 | Sparse, source-bearing final page: substantial concluding body, blessing, dating clause and `LEO PP. XIII` precede the rule and terminal apparatus. The source statement, reconstruction limits, revision and rights colophon are legible. This is not an apparatus-only final page. |

Native248 independently confirms the reviewed closing boundary through `LEO PP. XIII`; the following separate material does not enter the current selected body. This bounded check does not claim lexical collation of that page or the whole act.

## Mechanical evidence and limits

`verification.json` records 93 distinct exact hash/size checks, including packet brief and assembly inputs, source/segment/artifact controllers, current helper pins, producer evidence pins, native parent/excerpt pins, and every listed reader/native output and cache raster. All nine artifact metadata records and the segment metadata equal their packet snapshots. The full source row equals the frozen manifest, source-selection manifest and proposed-current row. Receipt/frozen schemas, generator version 2, revision `2026-10-30T14:35:12Z`, PDF/source identities and page count agree. Cache files, renderer fingerprint/inputs and review-run associations were checked without changing them or rerasterizing.

The complete native `-layout` extraction reproduces `32b54fe751219089e3823e66538321bed1dc30daee67d3b8cc62841735a044aa`; historical text equals the declared extraction LF44–23195 derivative. All eight selected historical LF ranges occur on their assigned actual native pages 241–248. For every parent/excerpt page pair, I independently compared complete `pdftotext -raw` bytes and `ElementTree.tostring(page)` bbox serialization as specified by `NATIVE_PROOF_METHOD.md`; all pinned hashes and byte equalities match.

Using the pinned current `_typeset_papal.py`, uncached `validate_document` succeeded and independent `pdf_body_fidelity` returned `pass`: 4 source-bearing pages, 17,800 source characters, 12,519 normalized characters and 12 permitted layout hyphens. `pdfinfo` reports the correct title/author/Latin subject, four unencrypted Letter pages and revision-derived creation/modification dates. All four Latin Modern fonts are embedded, subset and Unicode-mapped. The retained compile log contains no fatal, undefined-reference, overfull, underfull, missing-character or LaTeX warning findings.

All Python imports and helper executions used `PYTHONDONTWRITEBYTECODE=1` and `TRIPTYCH_LIBRARY_CACHE=0`. Only reviewer scratch was written. No source words were changed or guessed, and no canonical files, producer outputs, PDF bytes, shared cache, install/release records or Git state were changed by this lane. This acceptance covers the declared source-order repair and these exact four rendered pages. It does **not** certify whole-source lexical accuracy, translation, original-print facsimile identity/collation, new rights or intake approval, installation, publication or deployment. Native evidence is the identified archival OCR reconstruction.
