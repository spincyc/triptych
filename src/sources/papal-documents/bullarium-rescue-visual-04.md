# Bullarium rescue visual review — batch 04

Layout review completed 2026-10-26: **33 documents, 69 of 69 pages individually inspected; 33 PASS, 0 CHANGES_REQUIRED.** Every assigned individual page was opened through `view_image` at original full-page resolution. No prior reviews were reused.

Every PDF SHA-256 measurement and `pdfinfo` page count matched its assignment before, after and at the final reconciliation. The viewed raster hashes remained unchanged. The actual-view ledger was saved after every document, with an intermediate checkpoint for the eight-page document.

No clipping, overlapping columns, introduced missing rendered text or glyphs, unreadable title/body boundary, unreadable source/rights apparatus, conspicuously flattened table, modern digitizer banner, substantial foreign-language section under an inaccurate compact language label, or terminal furniture-only page was observed. Retained uncorrected OCR includes garbled words, literal squares, fragmented words and historical running furniture; these remain source-quality qualifications. Literal black squares visible in the volume 02, 04, 05, 06, 09, 11, 13, 16, 19, 21, 22 and 24 documents have corresponding square characters in the generated body TeX, recorded separately in the scratch evidence.

This PASS records visual layout only. It does not establish source collation, authentication, completeness beyond declared witness bounds, doctrinal or juridical verification, or publication approval. No source, PDF or raster was edited or regenerated.

## Source gate

The assignment pins withdrawal SHA-256 `a3e66221ed8afbd73c6cfab3e41d7d2be8ef7dce597a1bf2d41773b8a1faacbc`. Every per-document gate check and the final reconciliation measured `aa7bf4c374674f5b53846a203f76812bb4e07fdfe8a3cf924d21918146125c79` (revision `2026-10-26T16:11:07Z`). The difference from dispatch was reported to the coordinator. Each assigned exact `(id, language, pdf_sha256)` tuple was checked against every `supersessions[].prior` and `affected_units[].withdrawn_documents[]` record before its document was opened, and again at the final reconciliation: zero exact matches. The changed global gate hash therefore blocks no assigned PDF in this batch.

The actual-view ledger, per-document before/after measurements, gate checks, final gate snapshot, literal-glyph evidence, receipt-file hashes and final reconciliation are retained in `.scratch/bullarium_visual_review/rescue/batch-04/review/`.

## Receipt namespaces

Each document retains its assigned frozen receipt namespace. Both frozen receipt files were measured and matched the assigned hashes.

| Reference | Assigned receipt SHA-256 |
| --- | --- |
| A | `b8256dabaaeed467420920684323695182b61247530edbff7b9e1371ae92fc71` |
| B | `7db0034ada22d4dac66a12e91490a960e026d79540857026067ab0a72325b5eb` |

## Exact coverage

| Document ID | Receipt | PDF SHA-256, before = after | All individually inspected pages | Disposition |
| --- | --- | --- | --- | --- |
| `bullarium.volume-02.unit-0026` | A | `f3fc8f30eee8a1c9a31e58f8fadfb8f9eb046d60cb24cf092cff3ed92841d327` | 1, 2 | PASS |
| `bullarium.volume-02.unit-0136` | A | `4bfdb97b89780d3345cd0702a062e527f40eac9adf6f386d5b6dced502ccb1bf` | 1 | PASS |
| `bullarium.volume-02.unit-0273` | A | `bd745b14b0e1c241673c04e5bf5d86ea990a58ff5b2817d39fe0fd47c85318bd` | 1, 2 | PASS |
| `bullarium.volume-03.unit-0197.part-01` | A | `57a6b2489c22b4e09a0bd4b6494b6a21d260418bebf1ce31611536b1f2c67e3c` | 1 | PASS |
| `bullarium.volume-04.unit-0018` | A | `cc627e9590e16211deb871683ed7a8df3b898ed409e1ea51faa5fbef65a753f9` | 1, 2, 3 | PASS |
| `bullarium.volume-04.unit-0078` | A | `474ae8e26fa00f93c0148c958c9f903e19cddeead39cdd3c746e670806ac5a25` | 1, 2 | PASS |
| `bullarium.volume-04.unit-0134` | A | `b83503c2421ed28a2464169d78ed10bb28e452b0355bf459ffef20aea9a911e0` | 1 | PASS |
| `bullarium.volume-04.unit-0199` | A | `7b74f12ad3e7267af5367e76f134e452eb02a7e980ff30fb04c9eb33303078e0` | 1, 2, 3, 4, 5, 6, 7, 8 | PASS |
| `bullarium.volume-05.unit-0102` | A | `e68e5acb3f0b4ac2151644cb018ee77bfac3f848d2363028793ff6ef4d603296` | 1 | PASS |
| `bullarium.volume-06.unit-0089` | A | `32b30f37063d5e61b5efe5fdd305817219129716e1a3c080e8cff560c1d6c9e0` | 1, 2 | PASS |
| `bullarium.volume-08.unit-0093` | A | `ca08787eaf3ba735cc2810465b0e196eaf9f89b14377c9726271e315ebab1700` | 1, 2 | PASS |
| `bullarium.volume-09.unit-0137` | A | `f865a671c891d50fe4f207183fd9b880a09f91c6775b456e402290139e29b081` | 1, 2, 3 | PASS |
| `bullarium.volume-10.unit-0126` | A | `dd93591fd7c43309d81771cd3b58b04c2ed27c791fc4e3ae52e8b7fac04732a6` | 1 | PASS |
| `bullarium.volume-11.unit-0013` | A | `0ed9013c97f50a5d898345ee7cde3195c2e154b0c5023588dca7bfda233b1078` | 1, 2 | PASS |
| `bullarium.volume-13.unit-0006` | A | `98c047397c8bc3bbff3c6fe9a13b917631ecfdd0635af0aff549c27970759b1a` | 1, 2 | PASS |
| `bullarium.volume-13.unit-0131` | A | `9a4113ee65648a557c7d49c48495c748c0033b680e78e4ea3b3ade8953959f96` | 1 | PASS |
| `bullarium.volume-14.unit-0002` | A | `38b1891a8c97cb66fce3c233ea21a12549996527315d2d02743b66a9340e888f` | 1, 2 | PASS |
| `bullarium.volume-14.unit-0047` | A | `1d33f95081e822c3750ac730246bb6f7eeeb24b6b4df97ddf13096f664ce83d8` | 1, 2, 3, 4 | PASS |
| `bullarium.volume-15.unit-0096` | A | `a441b05fd8b2501704bd658cf9077484ba742654f760ea42959dc78d2a682dd3` | 1, 2 | PASS |
| `bullarium.volume-15.unit-0257` | A | `7560b743b077ab230fedc8e0d9ae3be915b046d6dd48d1d66f0d50e365cf4917` | 1, 2, 3 | PASS |
| `bullarium.volume-15.unit-0281` | A | `a4d98930fa6b95b205bbb314a6c7568bf1d189d80c3a0cd74fd943cb377746d3` | 1 | PASS |
| `bullarium.volume-16.unit-0093` | A | `0be622d47469cebdfd384050c59c9e9ab8170ffe314191714c29f2875579a681` | 1, 2 | PASS |
| `bullarium.volume-16.unit-0243` | A | `ec9c7ea5c255cda02fc54141f53e7357a56d93f5446495c01cf709b6bf1cddb9` | 1, 2 | PASS |
| `bullarium.volume-17.unit-0195` | A | `5fdf72e31a6b585032c3cfa038b31198c30e889ffe34e4f11b6121b007ba8cd6` | 1, 2 | PASS |
| `bullarium.volume-18.unit-0042` | A | `7b0fcc15e6f2729ef68535b77545b612b3a46fdee6048674278f188fe24729c5` | 1 | PASS |
| `bullarium.volume-19.unit-0049` | A | `4d518258dc8b7d9919a5423876f0dc2e52d7fd8dffb1541e8b7101c7b46b1849` | 1, 2 | PASS |
| `bullarium.volume-21.unit-0003` | A | `dbccae80d2d462c574dbcced5abd9fd981e33da9120329a806252dc286f9cc80` | 1, 2 | PASS |
| `bullarium.volume-21.unit-0164` | A | `089122c1d1120c454d2f1c4e5b56e6686840bef654fa405a87a7a0ec9533bdfe` | 1, 2, 3 | PASS |
| `bullarium.volume-21.unit-0203` | A | `5429aada86536797895916b271b708df9399c37ea05f802e5dab67f3675eb195` | 1, 2 | PASS |
| `bullarium.volume-22.unit-0133` | A | `622d97ab339dd96be7d2435d873de64dd2881f0512f4803e400fe9a3a09f0164` | 1, 2 | PASS |
| `bullarium.volume-22.unit-0212` | A | `71debb14311e52b68323b356d44dd4dbf11dd8f407efdf56b18de60fa9653ae8` | 1 | PASS |
| `bullarium.volume-23.unit-0062.fragment` | B | `18780114d1057d3dbcd718cd16a4e18c94c22cf7e867b7de09bf7eda14a87b74` | 1, 2 | PASS |
| `bullarium.volume-24.unit-0033` | A | `3f7209f18ff3cf7807763d01ec1c44ad9bb42c9102590a3d95a23983cc6fb7c9` | 1, 2 | PASS |

## Material qualifications

- `bullarium.volume-02.unit-0026`: Page 2 is sparse and contains a tall stack of short retained OCR fragments, followed by genuine historical dating clauses before readable source/rights apparatus; source-quality and composition qualification, without clipping or overlap.
- `bullarium.volume-02.unit-0273`: Page 2 is sparse but retains the concluding historical clause, subscription and dating before readable source/rights apparatus; qualified composition limit. Black squares on pages 1-2 are literal retained body-TeX characters, not introduced missing glyphs.
- `bullarium.volume-04.unit-0018`: Page 3 is sparse but retains the concluding historical prose and dating clauses before readable source/rights apparatus; qualified composition limit. Retained OCR damage and running furniture remain visible.
- `bullarium.volume-04.unit-0199`: Page 8 is very sparse but retains genuine historical dating clauses before readable source/rights apparatus; qualified composition limit. Retained uncollated OCR contains literal squares, garbled words and running furniture throughout.
- `bullarium.volume-06.unit-0089`: Page 2 is very sparse but retains the historical annulo Piscatoris dating clause and date before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-13.unit-0006`: Page 2 is sparse but retains the historical concluding prohibition and dating clauses before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-14.unit-0047`: Page 4 is sparse but retains historical concluding prose and the Placet motu proprio subscription before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-15.unit-0096`: Page 2 is sparse but retains historical closing prose, dating clauses and two historical notes before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-16.unit-0243`: Page 2 is very sparse but retains the historical concluding clause and dating before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-21.unit-0164`: Page 3 is sparse but retains genuine historical concluding prose and dating clauses before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-21.unit-0203`: Page 2 is sparse but retains genuine historical concluding prose, notes and dating clauses before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-23.unit-0062.fragment`: The fragment designation is visible in the title, and its terminal missing-content notice and rights apparatus are readable; the declared historical omission remains a source-boundary qualification.

No unresolved layout blocker was found.
