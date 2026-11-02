# Rerum novarum native-spacing cold review

## Decision and exact scope

**PASS — 2026-10-30.** Independently inspected all fourteen pages of `acta.ass.023.ass-023-014` (Latin), with no reused-page claims. The reviewed reader is `Litterae encyclicae de conditione opificum`, Leo XIII, 1891-05-15. No clipping, overlap, missing source ending, mixed-column order or project-apparatus-only final page was found. Its final page retains source body, dating, subscription and the last historical note before the project apparatus.

| Exact object | SHA-256 |
| --- | --- |
| Reviewed fourteen-page PDF | `1c306f4964425d5875d7f0646727221105968d435ce87a79e9e94ee4791ce92f` |
| Frozen render receipt | `fad59fc2e38b0633525475ca5eab9ef9fa32c70530cb4916e7b757e982ec6e51` |
| Correction/frozen input manifest | `f163d82fd21226a18141e7918581d9fce91c480613316a0995373a074f333f7b` |
| Final source artifact | `0dbbf1e2ae2b41b9ac8c5526f310b670a97fc303bee6ebf175ae1c5dfe92d399` |

The PDF and receipt are the frozen candidate beneath `.scratch/spacing-feasibility/reader-final-reviewed/`; the input is `.scratch/spacing-feasibility/correction-manifest.json`. All fourteen full-size existing reader rasters were opened individually, in addition to the contact sheet. Every page-raster and contact-sheet hash matches its review cache, whose run binds this exact PDF. All embedded Latin Modern subsets have ToUnicode mappings. The receipt reports no layout warnings; an independent complete-body extraction check passes with 305 additional physical-line hyphens and source-bearing first and final pages.

## Source transformation audit

The native PDF hash is `db86af2e261f732f9b958dd0f7dd5e34739b5c0939d4dd8580339af642e3fa89`. A new read-only extraction of native artifact pages 641–670 with `pdftotext -raw -enc UTF-8 -eol unix` reproduces the registered native-raw artifact `fa68451630f74ac4c43d2e15eb0097b0107e38da3a165311eb64841643cb8efc` byte for byte. The parent historical-text artifact is independently hash-checked as `2ed2fb06999a29e2791c1f8f58acf69590b4a12449217d5b6b3debfb7dd2355b`.

The registered recipe is `rerum-novarum-native-spacing-recipe-dc192a445cd4/recipe.json`; its exact hash is `dc192a445cd4c632bb44ee64ae10fbfd3101ed043fca80ca30caf6be9d68b6df`. An independent reconstruction, separate from the helper, confirms that all 1,178 selected nonblank parent LF lines have exactly one matching native line on their explicitly assigned page after removing whitespace. No native line is reused. The independently rebuilt line map exactly equals registered mapping `8dbd09359aaf474df16ca95ef1c8d0d1ef03c2d1d6756ad2a3850f920b2016b4`.

The output is exactly the registered spacing derivative `e1de8d5325c3d76a8b7826d8ca0ecde983ef6849c3a8be8691efab7b90828dcf`. All 60,256 selected parent non-whitespace characters and their order remain unchanged. Parent LF order and existing blank records are retained within the declared selections. This Rerum recipe has no retained-line whitelist and uses no zero-match exception.

The nine detected native content-stream order differences are exactly the explicitly disposed pages **647, 648, 651, 653, 654, 656, 662, 664 and 670**. Each was independently inspected as an existing full-size native raster. Each has one body column and physically separate page-foot historical notes; no marginal text/body fusion or misplaced physical note was observed. Native bbox evidence confirms clear body-to-note gaps of 13.352–25.328 points on those pages. The projection takes only each uniquely matched line's whitespace and leaves the parent source-line sequence intact; it does not adopt the raw stream's footnote-before-body ordering.

## Final LF-only note stage

Spec `rerum-novarum-native-spacing-note-spec-4f634dc56410/spec.json` is hash-checked as `4f634dc56410769347bd259fb3b2f4fe07972f2a311e2212a82a3aadba5fdd8c`. Replaying `tools/papal-source-notes` over the exact spacing derivative reproduces the final source hash above and its 1,274 LF records. Removing LF bytes leaves the entire input and output byte sequences equal. This stage inserts only empty LF records around source LF 1014–1016, corresponding to original parent LF 26225–26227.

Native page 664 visibly places those three citations below the final body line. Final reader page 11 now renders their source text as a separate paragraph block between the unchanged adjacent body passages. Other historical notes remain in their parent source-page sequence and separate blocks; no new note anchor or lexical reading is inferred. Reader pages 3–7, 9–11, 13 and 14 received particular attention at note transitions and the terminal subscription.

## Helper review and reproducibility qualification

Reviewed native-spacing helper SHA-256: `b67f55a5075a11a43f23766d477b32c5209a1144262790476e31c4fde2362b49`. Its optional retained-line API requires unique explicit source LF/page/hash/reason records, permits only zero-match lines, preserves their original bytes and labels that origin in its map. A whitelist entry cannot waive another unmatched line, a duplicate native match, a unique available native match, a blank line or an unselected line. Missing defaults remain strict; stream-order review coverage must equal the detected exception pages. All sixteen native-spacing tests pass independently.

Reviewed source-notes helper SHA-256: `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57`. All sixteen source-note tests pass independently. The Rerum spec uses the ordinary LF-range path, with no inline boundary options. Both current helpers reproduce the frozen Rerum outputs exactly, including the original registered mapping.

The immutable recipe and artifact transformation descriptions identify earlier helper hashes (`c3f13e34101ea360aa9dafb3e6d92723c001ce4286bf32ef03e837597b68e41c` and `92a17c5a5de809b2261f14979ef4d71444dae20e490bbfe5617e5fd7bec003c4`). Exact historical snapshots were located in the producer archives, independently hash-checked, and loaded read-only. They also reproduce the frozen spacing output, complete mapping and final LF-only note output byte for byte. This audit therefore establishes both exact-pinned-helper replay and compatible-successor replay, without asserting the historical and current helper files are identical. Source and PDF pins remain unchanged.

## Limits

This PASS covers exact-byte source preservation, the declared spacing/note transformation, bounded native reconstruction geometry and every page of this one final reading PDF. It does **not** certify lexical OCR accuracy, authenticate every citation, collate an original-print facsimile, prove historical discovery completeness or approve another reader. Literal OCR glyph errors, parent hard-line hyphens and source-page interruptions remain. No alternate Latin, English translation or model-generated source wording was used. The cold review made no tracked edits, rerender, installation or release mutation.
