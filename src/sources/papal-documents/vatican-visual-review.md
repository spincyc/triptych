# Vatican Latin PDF visual review

Review date: 26 October 2026. The current reviewed selection contains **392 PDFs / 1,127 physical pages: all 392 PASS**, with no pending pages or required changes. Its coverage comprises 990 fresh individual page inspections and 137 exact prior PNG reuses. The collector independently validated every current PDF, receipt and report hash, the exact page partitions and all reused-page proofs.

The frozen initial receipt is `08f5638fcea515986bf2c20efee50d0a6835280b6ea9959c95604b13a1a2b596`.

**All 392 PDFs and 1,140 physical pages are covered:** 1,065 pages were newly inspected individually at readable original detail, and 75 pages reuse exact PNG bytes from earlier individually inspected pages. The initial result is **353 PASS and 39 CHANGES_REQUIRED**. These decisions apply only to the exact initial hashes.

The structured [visual audit](vatican-visual-review.json) binds every document to its PDF hash, physical page extent, explicit individual/reused page numbers and hash-pinned report. Each reuse proof records equal current/prior PNG digests, the prior PDF, and the prior report digest. Compilation and text-fidelity checks are separate from this visual approval.

The 16 bounded batches used one shared four-worker `tools/pdf-review` raster run. Every new page was opened individually with `view_image`; contact sheets did not count as inspection. Checks covered visible glyphs and accents, clipping and collisions, column flow, heading breaks, closing clauses, source notices, revision lines and rights colophons. All fonts were embedded with Unicode mappings.

All Greek and combining-mark priority cases passed, including Vianney’s three declared overlines on physical pages 4, 7 and 8. All eleven corrected null-date title lines and all sixteen automatic closing repairs were individually inspected. The initial review identified several remaining protocol-only spills; the later correction build resolved these. Complete substantive paragraphs and substantial historical-note endings remain accepted despite unused space.

## Batch evidence

| Batch | PDFs | Physical pages | Report |
| --- | --- | --- | --- |
| 01 | 31 | 78 | [vatican-visual-01.md](vatican-visual-01.md) |
| 02 | 23 | 71 | [vatican-visual-02.md](vatican-visual-02.md) |
| 03 | 23 | 71 | [vatican-visual-03.md](vatican-visual-03.md) |
| 04 | 24 | 71 | [vatican-visual-04.md](vatican-visual-04.md) |
| 05 | 24 | 71 | [vatican-visual-05.md](vatican-visual-05.md) |
| 06 | 24 | 71 | [vatican-visual-06.md](vatican-visual-06.md) |
| 07 | 24 | 71 | [vatican-visual-07.md](vatican-visual-07.md) |
| 08 | 24 | 71 | [vatican-visual-08.md](vatican-visual-08.md) |
| 09 | 25 | 71 | [vatican-visual-09.md](vatican-visual-09.md) |
| 10 | 25 | 71 | [vatican-visual-10.md](vatican-visual-10.md) |
| 11 | 24 | 71 | [vatican-visual-11.md](vatican-visual-11.md) |
| 12 | 25 | 71 | [vatican-visual-12.md](vatican-visual-12.md) |
| 13 | 24 | 70 | [vatican-visual-13.md](vatican-visual-13.md) |
| 14 | 24 | 71 | [vatican-visual-14.md](vatican-visual-14.md) |
| 15 | 24 | 70 | [vatican-visual-15.md](vatican-visual-15.md) |
| 16 | 24 | 70 | [vatican-visual-16.md](vatican-visual-16.md) |

## Corrections and limits

A separate 58-row correction build addresses the approved layout, source-boundary and display-metadata findings. Its exact receipt is `0a3cba767175a1675173fd0271262e44fa3546272910c04c11f8012acb92529f`. All 200 physical pages were covered in reports 17–19; 57 corrected PDFs passed immediately. Mens Nostra required one further isolated heading repair, accepted after all eight replacement pages were freshly inspected in report 20. Its final receipt is `9b28f5dc1ed0cce3858aa2dc9bcb4b01d15671df29d5830c320b5133739f097b`; exact PDF SHA-256 is `710fac0836118e1f851509f306f763411aa5d0ac60718ac938aa639933f5b8d4`.

The final corrected selection contains 58 PDFs / 201 pages, with 139 fresh individual inspections and 62 exact prior PNG reuses. Initial and rejected seven-page Mens Nostra bytes remain frozen. All 59 superseded rendered snapshots retain their review evidence and findings in history and are excluded from current approval.

| Replacement batch | PDFs | Physical pages | New individual views | Exact PNG reuses | Report |
| --- | ---: | ---: | ---: | ---: | --- |
| 17 | 19 | 66 | 58 | 8 | [vatican-visual-17.md](vatican-visual-17.md) |
| 18 | 19 | 67 | 35 | 32 | [vatican-visual-18.md](vatican-visual-18.md) |
| 19 | 20 | 67 | 45 | 22 | [vatican-visual-19.md](vatican-visual-19.md) |
| 20, replaces Mens Nostra in batch 17 | 1 | 8 | 8 | 0 | [vatican-visual-20.md](vatican-visual-20.md) |

This review establishes visible usability of the declared corpus witnesses. It does not establish word-for-word agreement with historical printings, comprehensive OCR accuracy, a new historical conclusion or a theological argument. Retained source anomalies and qualified omissions are recorded in the reports and source metadata rather than silently emended.
