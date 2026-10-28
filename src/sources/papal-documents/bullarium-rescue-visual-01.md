# Bullarium rescue visual review — batch 01

Layout review completed 2026-10-26: **32 documents, 69 of 69 pages individually inspected; 32 PASS, 0 CHANGES_REQUIRED.** Every assigned page was opened through `view_image` at original full-page resolution. No prior page reviews were reused.

All PDF SHA-256 measurements and `pdfinfo` page counts matched their assignments before and after inspection. The assigned rasters remained hash-identical through the final check. The actual-view ledger was saved after each document, with intermediate checkpoints for the ten-page fragment.

No clipping, column overlap, introduced missing text or glyphs, unreadable title/body boundary, unreadable source/rights apparatus, flattened table, modern digitizer banner, or terminal furniture-only page was observed. The French bibliographic quotations in `bullarium.volume-22.unit-0186` are explicitly identified in its language line and terminal apparatus. Retained OCR damage, literal source squares, garbled words, marginal fragments and historical running furniture remain source-quality qualifications. The three black squares on page 1 of `bullarium.volume-02.unit-0255` were confirmed as literal characters in the generated body TeX.

This PASS records visual layout only. It does not establish source collation, authentication, completeness beyond declared witness bounds, doctrinal or juridical verification, or publication approval. No source, PDF, or raster was edited or regenerated.

## Source gate

The assignment pins withdrawal SHA-256 `a3e66221ed8afbd73c6cfab3e41d7d2be8ef7dce597a1bf2d41773b8a1faacbc`. Before and after this review the current withdrawal record measured `aa7bf4c374674f5b53846a203f76812bb4e07fdfe8a3cf924d21918146125c79` (revision `2026-10-26T16:11:07Z`), unchanged during the review. The difference from dispatch was reported to the coordinator. None of the 32 assigned IDs appears among current affected-unit IDs or supersession prior IDs. The final explicit comparison of each exact `(id, language, pdf_sha256)` tuple against every `supersessions[].prior` and every `affected_units[].withdrawn_documents[]` record returned zero matches. The global hash difference therefore blocks no assigned PDF in this batch.

Both measured gate snapshots, hash/page-count checks, the exact-tuple nonmembership check, and the actual-view ledger are retained in `.scratch/bullarium_visual_review/rescue/batch-01/review/`.

## Receipt namespaces

Each row preserves its assigned frozen receipt namespace; a combined-corpus receipt was not substituted.

| Reference | Assigned receipt SHA-256 |
| --- | --- |
| A | `b8256dabaaeed467420920684323695182b61247530edbff7b9e1371ae92fc71` |
| B | `7db0034ada22d4dac66a12e91490a960e026d79540857026067ab0a72325b5eb` |

## Exact coverage

| Document ID | Receipt | PDF SHA-256, before = after | All individually inspected pages | Disposition |
| --- | --- | --- | --- | --- |
| `bullarium.volume-02.unit-0057` | A | `b1d7bca3e3bba5a10a1e164d563b23ea83c303e411084a9d7b664c3d59665c4d` | 1 | PASS |
| `bullarium.volume-02.unit-0255` | A | `3e0c72b01ef0b8e84b2a2737b0504fc11c6a39c7f9f007d31952347a684cd011` | 1, 2 | PASS |
| `bullarium.volume-03.unit-0108` | A | `82f9279d5d16ac60bd0c43d971dc6462d176fb0b61f34ddbf5b712d3cd99c47c` | 1 | PASS |
| `bullarium.volume-04.unit-0023` | A | `8f7c579b6bef92253872bf159d6b82bfcaa2f61106f142ba2bba6bc07eb34f6e` | 1, 2 | PASS |
| `bullarium.volume-04.unit-0123.fragment` | B | `37f16c4a3edf04d18c060189e0f28c594ab63ef12396bac33fcde576539149a2` | 1 | PASS |
| `bullarium.volume-05.unit-0024.part-01` | A | `5885138cf108b26690445d260a73f64e1df4f0cff5afd252585a278b5e616475` | 1 | PASS |
| `bullarium.volume-05.unit-0057` | A | `c023d6240cfe837cbb718dcdefcbe1308b3de7498847f0c651b9a995cc8d43d4` | 1, 2, 3 | PASS |
| `bullarium.volume-05.unit-0100` | A | `2decfe725de1c9cba74ba6c90735533a7d2a2c187fc5d71131c3058ef8529575` | 1, 2 | PASS |
| `bullarium.volume-08.unit-0011` | A | `acc14e3a6da8da7c23d61177e9447929f349de9762b08794daa857b92f7e64ce` | 1, 2 | PASS |
| `bullarium.volume-09.unit-0003.fragment` | B | `dbc1ea6ff5c6797bed59de91ab4a42ba62c3981b7fd7c4bf21f5bf63abc95b95` | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | PASS |
| `bullarium.volume-10.unit-0007` | A | `88ba2fb140afc175a69b91c7d6a3c8e6979770950156c2e74fd7d366b55ddcdb` | 1 | PASS |
| `bullarium.volume-10.unit-0201.part-01` | A | `2ba59f0a3de81df86c8f0b14b330c7296cca6fee02dff39571aaa1f5301aea6c` | 1, 2 | PASS |
| `bullarium.volume-11.unit-0082` | A | `8a9b993f13f2255086688821904a0b61cd81ee2a39b0f40013e27d63dd8c5fc3` | 1, 2, 3 | PASS |
| `bullarium.volume-12.unit-0160` | A | `6fedad747a97fc409e205c52a4073ea5db8095d3aa7925f73d5d47cbb4151d38` | 1 | PASS |
| `bullarium.volume-12.unit-0192` | A | `bbd6492c526fc872c6c3e1f21609aed541a98850aae05f100b15ee2eb89e0455` | 1, 2 | PASS |
| `bullarium.volume-13.unit-0245` | A | `2255e5a1f462c92f667714696f98a23808e1baac76f27ff68bd1a242717cada1` | 1, 2 | PASS |
| `bullarium.volume-15.unit-0061` | A | `671eea67e8b1b0e511c3ce561b8bcfb24616a7d4452c6f901784a668ad3f8d80` | 1, 2 | PASS |
| `bullarium.volume-15.unit-0194` | A | `17cc7150d14f09c210f1c11c628fe34f6b3d9dfe1d52de38f90b411aefbb66cb` | 1 | PASS |
| `bullarium.volume-16.unit-0025` | A | `e9817ca117d325103b8f5a4d8a18f2c3a5a3bd887662f0edb074c2ef7aff99a5` | 1, 2 | PASS |
| `bullarium.volume-16.unit-0233` | A | `972cae49a50168236a8fdda80919da076d3017d8f4754f332e6da2338c4c99e0` | 1, 2 | PASS |
| `bullarium.volume-16.unit-0279` | A | `3a167b29b9d39edef7c8218dedc9314bd44fcdda301507e91255e0c2eef5298e` | 1 | PASS |
| `bullarium.volume-17.unit-0142` | A | `e9ccab678d03a02659be95dae974a2238e69fa0e62015346fc0da3f020ee3fee` | 1, 2 | PASS |
| `bullarium.volume-18.unit-0096` | A | `1eeb608b4dfc94f9ccaeb774108b09d2e8fd9a4f15f651a4491bb9df5cf5b93b` | 1, 2, 3, 4 | PASS |
| `bullarium.volume-19.unit-0046` | A | `e05d0915af98e2f66796ea88211f36b40ea8f5524a1e4bd45702818bdb15e2b7` | 1, 2 | PASS |
| `bullarium.volume-19.unit-0115` | A | `38fb6f39b94ea11e69f8d0066d3095ef3797da179378faa5bd819bbd98544d0c` | 1, 2, 3 | PASS |
| `bullarium.volume-20.unit-0155` | A | `a71440bf38abc22dc02a28e939843ae486475bee7e7454b30de5113d1b43e64d` | 1, 2 | PASS |
| `bullarium.volume-21.unit-0201` | A | `5dcc8d5a132fa548cc7fe041d537a460b19a3b9d93b591c7b752b862cbcaefec` | 1, 2 | PASS |
| `bullarium.volume-22.unit-0120` | A | `d646a770cca6b3f55f89d04df7f53ee53e601ad6f51d3e95adb8cdbd289ff5a0` | 1, 2 | PASS |
| `bullarium.volume-22.unit-0186` | A | `fc0a1d468bd4224b1610be5b4e5b3a1f5fda79b3908eca394d7d160e642a4885` | 1 | PASS |
| `bullarium.volume-23.unit-0052` | A | `01d0f89d13b9eb66a7e10b0f92f9d591eb0201a5fa7a14c374f04a2075c5c209` | 1, 2 | PASS |
| `bullarium.volume-23.unit-0058` | A | `4fb630ea7021996da54bd48c16e98fdd15bd7c3e560424f4175d48c3f9f4461a` | 1, 2, 3 | PASS |
| `bullarium.volume-24.unit-0022` | A | `95a3fb362f32e4a68c89a5a4d18066ead78adce0f298f6735a51082b111bf979` | 1, 2 | PASS |

## Material qualifications

- `bullarium.volume-02.unit-0255`: p. 2 is sparse but begins with genuine historical dating clauses before the readable source/rights apparatus; qualified composition limit. Page 1 black squares are literal in the retained body TeX, not introduced missing glyphs.
- `bullarium.volume-04.unit-0023`: p. 2 is sparse but retains the end of the historical sentence and actual dating clauses before the source/rights apparatus; qualified composition limit. Running-head furniture also remains in the uncollated OCR.
- `bullarium.volume-05.unit-0100`: p. 2 is sparse but retains the concluding historical sentence and papal subscription before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-09.unit-0003.fragment`: p. 7 left column contains a conspicuous run of very short retained OCR fragments (from lil through SIXTUS), producing a tall narrow stack and interrupting the prose; source-quality qualification, without clipping or column overlap. p. 10 is sparse but retains genuine historical dating and papal subscription before readable fragment/source/rights apparatus; qualified composition limit.
- `bullarium.volume-10.unit-0201.part-01`: p. 2 is sparse but retains genuine historical dating clauses before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-17.unit-0142`: p. 2 is sparse but retains the end of the historical clause, dating and source note before readable source/rights apparatus; qualified composition limit.
- `bullarium.volume-18.unit-0096`: p. 4 is sparse but retains the concluding historical clause, dating, signature and registration line before readable source/rights apparatus; qualified composition limit.

No unresolved layout blocker was found.
