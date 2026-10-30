# Independent repair acceptance: packet 23-a

2026-10-30. **PASS: 4 PDFs, 25 reader pages.** Every reader page was viewed in the packet contact overview and individually at full raster resolution. No page was reused from an earlier acceptance event. No blocking clipping, overflow, overlap, fused note/body paragraph, sustained unreadability or apparatus-only terminal page was found.

Packet: `.scratch/encyclical-ready-package/review-packets/23-a.json`.
Packet SHA-256: `2fb2fe691b3ecda4637bbe8f4ab335dc79b8b6d9c2c85c2cac27a0a05f463aca`.
Canonical destination for these exact report bytes: `src/sources/papal-documents/encyclicals-repair-cold-23-a.md`.

## Exact reviewed readers

| Source ID / title | PDF SHA-256 | Pages actually viewed, contact and full-size | Receipt SHA-256 |
| --- | --- | --- | --- |
| `acta.ass.026.ass-026-l10652` — Providentissimus Deus | `13cf93fed9659e2bdeb8514dd8d868ac46c307bceea3e3c1ce25b28c4ca03778` | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 | `94f4e23cc45e17bbd04b87b559d037be21c047586042f6ae1fe69c92a70c7dc6` |
| `acta.ass.029.ass-029-l25864` — Divinum illud munus | `9a202664b57c62c67ed7d5db89383d8814c95854891ef02af3dbe96baf589171` | 1, 2, 3, 4, 5, 6, 7 | `048b5919f8a6df92243c67c7bb204c3bba9a3fa539489bf9d40fe4e85b0f5644` |
| `acta.ass.026.ass-026-l05089` — Constanti Hungarorum | `1a7d7b11cd6f92d913a201aac8a9a7ee111d6e2d01a56510fb8aeef35312e6a9` | 1, 2, 3, 4 | `ca164d3c04886c0b42693befed248e1b308132af382ab91f337c8cd07384e2d9` |
| `acta.ass.026.ass-026-l07664` — Laetitiae sanctae | `03a1f05213713fd2c64ec5ac0bcf1141998600882019fac1f72fe20a434d9f9f` | 1, 2, 3 | `94f4e23cc45e17bbd04b87b559d037be21c047586042f6ae1fe69c92a70c7dc6` |

The actual page counts are 11, 7, 4 and 3. All PDF, receipt, frozen-manifest, selected source-text, segment-manifest, controller-record and available payload hashes match the packet. Each complete frozen source row matches by object equality; no fields were omitted from that comparison. Receipt source/artifact/segment/range/revision/PDF bindings also match. `verification.json` retains the exact rows, paths and per-file pins.

## Reader findings

**Providentissimus Deus — PASS.** The opening protocol and identification are clear. The short retained letter-spaced phrase and displaced k on page 1 remain conspicuous but bounded; the surrounding text is usable and the terminal source note describes this defect. Historical notes start their own indented paragraph blocks, including the five newly partitioned groups. Page 11 retains the continuing source body, blessing, date, LEO PP. XIII subscription and final Psalm note before the ruled apparatus; it is source-bearing.

**Divinum illud munus — PASS.** All 15 historical note groups form separate blocks at their source-page breaks. Retained malformed reference markers, superscript fragments, citation punctuation and the short stray glyph cluster remain visible, but do not fuse a note into body or cause sustained unreadability. Page 7 retains the conclusion, date, LEO PAPA XIII and final Psalm note. Apparatus begins at bottom left and continues at top right in normal column order on this same source-bearing page.

**Constanti Hungarorum — PASS.** All three historical citation groups are separate blocks on reader pages 1, 2 and 4. The damaged incipit and scattered source letter spacing remain usable. Page 4 preserves the literal 11 Septembris closing and LEO PP. XIII; its terminal note explicitly distinguishes the 2 September identification from that OCR discrepancy. Apparatus continues from bottom left to top right on the same source-bearing page.

**Laetitiae sanctae — PASS.** The compact 0.65-inch margin composition remains readable in two columns with a clear gutter. Historical citation notes are separate blocks on pages 2 and 3. Scattered native letter spacing, OCR punctuation and hard-line fragments remain literal and disclosed. Page 3 retains blessing, dating and LEO PP. XIII before the ruled apparatus and rights colophon.

All four readers identify Leo XIII, the selected date and Latin unambiguously. The normal left-column-to-right-column order, gutter, paragraph indentation and baseline spacing remain usable. Terminal notices are smaller but legible, and do not overlap source text. `pdfinfo` parses every file without a suspect/encryption indication; title, author and subject match the reader and frozen row. PDF timestamps agree with the frozen render revisions. `pdffonts` reports all four Latin Modern font resources per reader as embedded, subset and Unicode-mapped. The PDFs are 38–84 kB, below the repository size-review triggers.

## Independent replay and native evidence

The registered commands were replayed with outputs only under `.scratch/cold-repairs-23a/`. Four native-spacing recipes and three LF-only note specifications reproduced their expected hashes. The exact historical b67 helper (`b67f55a5075a11a43f23766d477b32c5209a1144262790476e31c4fde2362b49`) was separately imported from its canonical archived artifact and replayed. Its outputs, complete line maps and stream-order dispositions are identical to the current 7c helper on all four assigned recipes. The historical helper pin was preserved; current-code compatibility was not treated as permission to repin it. The registered note helper hashes to `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57`.

| Reader | Matched native LF lines | Retained old LF exceptions | Raw-stream difference pages whose visual order was checked | Final selected source SHA-256 |
| --- | --- | --- | --- | --- |
| Providentissimus Deus | 940 | 10678, 10679 | 279, 289, 292 | `b4df8a1914cdba51537b2f3607ff4f42680e063d8128a238e68d2d86f2cbb205` |
| Divinum illud munus | 583 | 26024, 26025, 26065, 26066, 26242, 26243, 26324, 26325, 26369, 26370, 26413, 26414 | 651, 656, 657 | `21f6dafef3648aa4b08b13a0af06aaa0f01d3790d8791c28495db7f882e8a395` |
| Constanti Hungarorum | 297 | None | 130, 131 | `5cdf0bbdb77ddd84d421f85682f36307f9ae1744dbd89b5c2696112b1bd878c8` |
| Laetitiae sanctae | 266 | None | 193 | `fb187da8b18b2ab865b235a32e6327196743a2f54ebcb4f0d5b4bb3a83a1c95e` |

All four registered spacing maps match the independently replayed maps, including Divinum’s map `cef68e87ff77cde70bf48ff0961049e65a1143d01b374863a2478a96fb7b71fb`, resolved from its source review. Whole native PDF hashes match the source pins: ASS26 `02f81d1d13781d2f7d27d4aa327d7ec83bbe5ea8ec22f785eda20dd4ce777446` and ASS29 `0972de3da0abf6bf1b37c5eb2da66bba6e11d8b231ec65df32cc826458514b27`. Fresh whole-PDF raw extraction, bounded afterwards to each registered native-page interval, equals each tracked native-raw payload byte for byte. Each viewed excerpt PDF matches its cache hash; its page text and bounding-box geometry equal the exact parent-PDF page interval. Every native and reader cache file hash was checked.

Native contact inspection covered ASS26 physical artifact pages 269–292, 129–136 and 193–199, and ASS29 pages 644–658 (54 native pages). Full-size native inspection was limited to these actual pages:

- Providentissimus Deus: 269, 270, 271, 272, 273, 279, 283, 289, 292.
- Divinum illud munus: 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658.
- Constanti Hungarorum: 129, 130, 131, 135, 136.
- Laetitiae sanctae: 193, 196, 197, 199.

These are physical artifact page numbers established from the recipes and parent/excerpt comparison, not inferred from contact-sheet ordinals or printed OCR folios. The changed note groups appear as page-foot citations separate from the single native body column. Stream-inversion pages support keeping prior layout order. The bounded Providentissimus exception shows the small k at auctore; its old-LF displacement is retained and disclosed. Divinum’s six superscript/note exception pairs are bounded by exact old-line hashes. Constanti’s native page 136 and Laetitiae’s page 199 place the subscription before a visibly unrelated next act; the selected readers stop at their own subscriptions.

The source-aware PDF fidelity check was independently rerun over the complete selected bodies. All four pass with source-bearing first and last pages. Results exactly match the frozen receipts, including 261, 143, 93 and 65 permitted layout hyphens respectively; original source hyphens are still accounted for.

One nonblocking audit-record defect was noticed: Constanti’s registered geometry review/recipe contains a copied sentence about Annum sacrum native page 651. This sentence does not describe Constanti. Independent inspection above establishes the actual Constanti geometry and all three note boundaries; the irrelevant sentence did not affect the selected bytes or this acceptance.

## Limits and disposition

This is an independent reader-usability, source-boundary, transformation and OCR-PDF-geometry acceptance of the exact bytes above. Native pages are Vatican OCR text reconstructions. No original-print image collation, lexical OCR correction, translation-equivalence judgment, whole-book completeness claim or independent rights certification was performed. Existing rights statements were checked for rendered separation and identity only. `qpdf` is unavailable; structural examination used Poppler parsing/extraction and embedded-font reports. No PDFs were rerendered or installed, and no tracked source, canonical report, shared cache, release file or Git state was changed in this lane.

Durable scratch evidence: `verification.json`, `page-observations.jsonl`, `native-observations.jsonl`, the exact replay outputs and extraction/geometry checks under `.scratch/cold-repairs-23a/`. Root may copy this report unchanged to the canonical destination and bind its SHA-256.
