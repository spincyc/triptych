# Independent cold review: Tametsi futura, packet 47

**Bounded SOURCE SPACING/NOTES: PASS. Final reader PDF: PASS, 6/6 pages.** No material blocker was found within this review's scope. These are separate decisions; neither grants original-print identity, lexical collation, translation certification, new rights clearance, installation or deployment approval. Root retains admission and canonical-copy ownership.

The reviewed work is Leo XIII's *Tametsi futura*, Latin, dated 1900-11-01, `acta.ass.033.ass-033-l10742`. This review concerns only the final packet bytes and uses fresh visual inspection throughout. Earlier provisional PDFs and producer visual acceptance were not reused.

| Exact input | SHA-256 |
| --- | --- |
| Packet 47 | `50312d7d3e1ad2364b2582e8a3c7cf05800ead338c5d4b15fa53987a96325531` |
| Final PDF, 53,351 bytes, 6 pages | `43ff816d916e563e7f48644f04506287e671fc3f60d4722b9b4dee9edcab283a` |
| Receipt | `92a63c2a59020f28d96234e880d4f76dabba8050c9ce5778658870413f6d1fd8` |
| Frozen manifest and selection manifest | `bd28407724f8140f058b558d673c3758f17d1038ac3c9eebd199280e620196e4` |
| Final selected source | `e5a5c6eeaa42b649c730cc234a4672ec13f44ec01716daa6033bf4796ba95e20` |
| Native whitespace derivative | `b76bbdd32d7a6d80d8d4fcb39760a77638085cd34508fb84764d3ca3802ad052` |
| Current native-spacing recipe | `a6b92043f80f0915d2d6dcb71ef8fc4fd3333ca2d931b79bb2d16c906c195020` |
| Note partition spec | `f5376de822a9427c7c941a6a37cb8cabe405419bfa3d72bccb1b55e34323f7c1` |
| Native geometry proof | `e4102267832a2594077bf5cf18a07585834f3ed71a2424d166198bc8113f09a6` |
| Whole native OCR PDF | `18fd550d59a2de5ac9f7e283c407c43ee5d1f004032b9109c4cdc733fcb021d6` |
| 13-page native excerpt | `1ca5e7998416c6a9a8052b713fa137fa019879db274546cb19c6831d2e0fe366` |

The packet's full `source_row` equals the matching frozen-manifest row, including controller, ranges, correction evidence, rights declarations and revision `2026-10-30T17:27:42Z`. The segment and artifact TOML metadata equal their packet copies. Every declared retained payload and current helper pin checked; restricted parent records were checked as metadata and the scratch native PDF as exact evidence. Schema and source-graph validity were checked by the current uncached whole-library validator.

## Bounded source spacing and notes

The source controller is `segment.acta-papal-archives.ass.033.ass-033-l10742.tametsi-finish-e4102267832a`, with final source LF range 1–562. The exact prior historical selection comprises 13 declared ranges from parent LF 10736–11276. Its non-whitespace stream remains unchanged through whitespace projection and note partition: 25,116 characters, UTF-8 non-whitespace SHA-256 `2d332286377bcaf11159b7526f200c0e290b43a2ada38854187fbd19e23c9d95`.

I independently reran `pdftotext -raw -enc UTF-8` and `-bbox-layout -enc UTF-8` over each whole-parent page 273–285 and excerpt page 1–13. Complete raw stdout and default `ElementTree.tostring(page)` bytes matched each corresponding packet hash and each other, following `NATIVE_PROOF_METHOD.md`. The complete 13-page raw and bbox outputs also equal the retained native raw and bbox artifacts. The bbox payload hash is `1b8d9a198a3cc069e51680d97f9137e2ca855f0483d7d5f9eed8c0a3b789accb`.

All 506 nonblank selected LF records have one same-page raw match and one geometry match. I reconstructed the geometry groups from exact equal line `yMin` values and complete unchanged WORDs sorted by `xMin`, then independently compared line ordinals, every WORD value hash, box and ordinal with the retained proof. All 5,240 selected WORDs occur once. The current helper replay reproduces the retained 506-entry line map exactly, including its recovered whitespace hashes. There are no literal-parent retention exceptions. Source-specific native word and letter gaps remain those of this OCR reconstruction; no lexical inference was introduced.

I ran the current native-spacing recipe into owned scratch and compared its output byte-for-byte with the retained whitespace derivative, then ran the exact note spec into owned scratch and compared it with the final source. Both registered read-only `check` invocations also pass. Notes add exactly 22 LF bytes; selected non-LF bytes and order remain unchanged at that stage. The current helper paths and SHA-256 values are:

| Helper | SHA-256 |
| --- | --- |
| `scripts/_papal_native_spacing.py` | `7c7393f6b366bc986e7d106d217a769fabba5a48edd645a7bd02b463eb64d82c` |
| `scripts/_papal_source_notes.py` | `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57` |
| `scripts/_papal_source_order.py` (pin checked; no order repair applied) | `f0a3014db485ee25ffa7df013c81e600f8e4f9eccff76b5ac7daecbc1d6a9c86` |
| `scripts/_typeset_papal.py` | `1c14411ed430d51605af66a37ddcb6d758d0eb67c9e8d56a1d4d875e9a0ba146` |

I freshly opened the native contact sheet and **every native page 273–285 individually at original raster resolution**. Each has one body column. The 11 note groups are vertically ordered page-foot citations, with no second note column or interleaved ownership. I inspected their internal citation order directly, separately from the fidelity checks. The raw extraction stream differences on 278, 280 and 285 move footnote records relative to body; the retained parent LF order follows the visible body-then-note geometry. On 285 the final note physically follows the subscription. That disposition is accepted for this bounded repair.

| Native artifact page | Spaced-source note LF | Final note LF | Final PDF page | Direct note disposition |
| --- | --- | --- | --- | --- |
| 274 | 82–83 | 83–84 | 1 | Two citation rows, (1), (2) |
| 275 | 124–126 | 127–129 | 2 | Three rows, (1), (2), (3) |
| 276 | 166–168 | 171–173 | 2 | Three rows, (1), (2), (3) |
| 277 | 208–211 | 215–218 | 3 | Four rows, (1), (2), (3), (4) |
| 278 | 253 | 262 | 3 | Single Augustine citation; literal `ti)` marker |
| 279 | 293–295 | 304–306 | 4 | Three rows, (1), (2), (3) |
| 280 | 337 | 350 | 4 | Single John citation |
| 281 | 378–379 | 393–394 | 4 | Two rows, (1), (2) |
| 282 | 419–421 | 436–438 | 5 | Three rows, (1), (2), (3) |
| 283 | 462–463 | 481–482 | 5 | John then Mark, (1), (2) |
| 285 | 540 | 561 | 6 | Final John citation after subscription |

Each final group has an actual empty LF before and after; the rendered reader has corresponding paragraph separation on both sides. At the native 280 break, the following body paragraph starts at the top of the next reader column. Historical page-foot placement sometimes interrupts a word split at the source page break, such as `or-` / `dine` around the native 278 note on reader page 3; this retained source order is explicit and legible.

## Final PDF

I freshly opened the final contact sheet and **all six actual reader pages individually at original raster resolution**, with no reused pages or prior visual-review proofs.

| Reader pages | Findings |
| --- | --- |
| 1 | Clear title, issuer, date and Latin identification; protocol/address and first source-note paragraph remain readable. |
| 2–5 | Normal left-column then right-column continuation; all source-note groups above remain separate paragraphs with their literal citation order. No observed clipping, overlap, missing glyphs or unreadable spacing. |
| 6 | Substantive source continues through the closing blessing, `Datum Romae` dating clause, `LEO PP. XIII.` subscription and final citation. Smaller ruled source apparatus and the rights colophon remain readable on that physical final page. |

`pdfinfo` confirms six unencrypted letter-size pages and appropriate title/subject/author metadata. Both PDF dates correspond to the pinned UTC render revision. `pdffonts` confirms all four Latin Modern subsets embedded with Unicode mappings. The final compile log reports six output pages and has no warning, overflow, undefined-reference, fatal-error or error matches; the pinned receipt also has no compile warnings.

Using the pinned current `_typeset_papal.py`, I independently ran `validate_document(source_row, root=repo)` followed by `pdf_body_fidelity(pdf, validated, 6)`. The result is `pass`, method `pdf-raw-source-aware-line-hyphen-nfkc-v3`, 25,116 normalized source characters, 124 permitted layout hyphens, with source text on reader pages 1–6. This does not replace the visual judgment above.

## Qualifications and retained predecessors

Literal OCR spelling, punctuation, some native word gaps and original hard-line hyphens remain visible, including inline hyphens after reflow. Native body starts encoded only through indentation remain continuous where the inherited selected LF text lacks a paragraph boundary. This review accepts the declared whitespace and note repair; it does not certify full body paragraph restoration. The native PDF is an archival OCR reconstruction, and its displayed pagination is not original-print evidence. For example, artifact ordinal 283 displays a page number resembling 285. No original-print image or whole-source lexical collation was performed.

The actual installed predecessor remains identified separately: source `0bf4c816a025b28cf31636812e0a2bf93729edf32823a74844f33ea857d3af6f`, PDF `61d42a7909e2e256982ac7ba4c5f3d9c702058d0f346bd9b8a57e8a24d05b1ea`, recorded installed review `PASS`. The failed notes07 candidate is source `33587b49539cd3fa0e7593215f8afb78f27843447e527febf2fe586cf426a3fd`, PDF `a6fd3d9394083bbff6ef6976a898bf33997f2ca4f89c0925fb620bcdbfb7eab0`, recorded review `CHANGES_REQUIRED` for inherited interletter spacing. Both source/PDF pairs and prior receipt records remain present with their exact hashes. The frozen manifest explicitly distinguishes their supersessions. This review changes neither prior status nor bytes.

Current uncached `tools/source-library validate` exited 0: artifact=11108, corpus=5, edition=14304, passage=9532, segment=10882, work=10944, bindings=4398. No historical unrelated Provid review error was carried forward. Every Python import and source-library invocation used `PYTHONDONTWRITEBYTECODE=1 TRIPTYCH_LIBRARY_CACHE=0`; no shared cache was touched.

The check record is `.scratch/encyclical-refinement-package/cold-review-47/verification.json`, with actual observations in `view-log.json`. All review-created files remain under that exclusive scratch directory. Source artifacts, producer files, shared caches, release records, installed PDFs, canonical report target and Git state were left unchanged by this reviewer. The target for root's exact report-byte copy is `src/sources/papal-documents/encyclicals-refinement-cold-47.md`.
