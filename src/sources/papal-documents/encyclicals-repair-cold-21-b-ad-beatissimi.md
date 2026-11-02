# Independent cold review: Ad beatissimi, Spanish

**PASS — 8 of 8 reader pages freshly inspected; no blocking finding.** All 15 native excerpt pages and all 14 historical note loci were also freshly inspected. Producer PASS and older checkpoint observations were not adopted.

Exact review identity:

| Item | Pin |
| --- | --- |
| Document | `acta.aas.006.archive.aas.006.055` · `es` · 1914-11-01 |
| Packet SHA-256 | `ffb8e480001485511b84a158ff6672605f60e13b035efa4573dd208247e7ae95` |
| Reader PDF SHA-256 | `31d41384a012164499a97c52faf90060cd1066103ec6588d510a40f5873a2ed7` |
| Receipt SHA-256 | `1605bbe0138ca0f719c6696a4039b12fa18ef89cef6eeffc4db752096f0cecef` |
| Frozen manifest SHA-256 | `da4d599533113646545b2835de7cbca9cc8aff14c94ce154e2b1ca95e99df27d` |
| Selected source SHA-256 | `9d57573c0c78118304bec963a7f37a9f51a66b76f93e71de07feedba9f001633` |
| Current segment manifest SHA-256 | `f551b29c06b344bc4b3b932de38fd55fe3120ef63ada36b600565046c35b4464` |
| Render revision | `2026-10-30T05:31:36Z` |

Reader: `.scratch/encyclical-notes-01/readers/1914-11-01-acta-aas-006-archive-aas-006-055-14e15da7-es/1914-11-01-acta-aas-006-archive-aas-006-055-14e15da7-es.pdf`. Receipt: `.scratch/encyclical-notes-01/readers/receipt.json`. Canonical report destination: `src/sources/papal-documents/encyclicals-repair-cold-21-b-ad-beatissimi.md`. The PDF is 56,468 bytes, eight unencrypted US Letter pages, with matching title/Spanish subject/Benedict XV metadata. Its four font subsets are embedded and have Unicode mappings. Build logs contain no checked layout, glyph, or undefined-reference warnings.

Fresh mechanical verification completed 79 hash checks. Every packet PDF, receipt, frozen manifest, complete frozen source row, source selection proposal, parent packet, segment, source controller record and retained payload matches. The receipt input-manifest pin and source/PDF/revision/page facts match the packet. The complete frozen row was compared as an object, including rights and limitations. All checks and exact paths are retained in `verification.json`, `frozen-source-row.json` and `receipt-row.json` in this review’s scratch directory.

The parent Vatican OCR PDF SHA-256 is `b655eb5e24d52cfabc538f3da1e3e19d7056fe9dc1fcb67189a3b1bea5c8831f`. Its fresh complete `pdftotext -layout -enc UTF-8 -eol unix` extraction reproduces `04755d3ed4f0ee6a201de4120afcf5f87107f107f1a70da6d5dc10a527728f3e`; the registered full-volume historical derivative reproduces `fb3b4bd1a8d41392dc06fc705d97bac09d7aee15780990391456a948f9ea3c67`. The native excerpt `.scratch/encyclical-notes-01/native-es.pdf`, SHA-256 `6cb557b0d68533bc59e8e00e707acf9fcd678a1662bbb0b53d3962a65c2f2801`, is 15 pages. Every excerpt page’s text and bounding-box XML exactly matches the corresponding parent artifact page 615–629. The archived-PDF segment and source evidence independently identify those bounds. This establishes excerpt correspondence to the OCR reconstruction, not original-print image collation.

The exact registered specification `ad-beatissimi-es-note-spec-685b7841df3d/spec.json` hashes to `685b7841df3d79de77b18a282a05af77428a75a3fd0647e333ddc87b05dac1f0`. I replayed both archived helper `source-notes-helper-92a17c5a5de8/helper.py` (SHA-256 `92a17c5a5de809b2261f14979ef4d71444dae20e490bbfe5617e5fd7bec003c4`) and current `scripts/_papal_source_notes.py` (SHA-256 `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57`). Both produced the selected source’s exact 40,027 bytes and 716 LF records. All selected non-LF bytes and source order are preserved; their digest is `b77f0c0f7187558f88578987d03d648905b9c5a787ad44bb441b8a65d1077d6a`. All imports/replays set `PYTHONDONTWRITEBYTECODE=1`, and outputs remained in this scratch. The helper software is MIT-licensed; it does not inherit the historical wording’s recorded US public-domain rights basis.

The predecessor selection’s full disjoint LF extent is retained exactly. The body begins at the historical address, LF25476, and ends with the subscription, LF26164. The excluded Roman series ordinal, 16 intervening running-head/issue-footer/reconstruction-furniture records, and the following page header were checked as furniture against native pages. No substantive neighboring act was selected. This is an LF-only note partition: there is no source-order or character-geometry map to replay.

The independent complete source/PDF comparison passed `pdf-raw-source-aware-line-hyphen-nfkc-v3`: 39,430 source characters, 30,741 normalized characters, zero added layout hyphens, source beginning on reader page 1 and ending on page 8. Its result exactly matches the receipt. The generated body TeX also matches a fresh render byte for byte; SHA-256 `39afe53802d37255741821e10bc6d7f24d8a152f357b0802902cff74f0f1803a`.

The shared review-run SHA-256 `0a4c8712774dd80811f96f57003c1a182836120302ef147385cbeb66240e2a0f` matches `raster-operation.json`; its exact source/PDF/page-count/output row matches the packet. Every listed reader/native cache image hash and size, full-page count, cache key, renderer fingerprint and renderer/font binary pin was freshly verified. Renderer fingerprint: `cb6bc6758b165c50bba7f68d7b5e1df5cc66fa3e0aad97361992b67d97cea2ba`. The native cache’s index row matches its excerpt and 15-page bounds. No shared job was rerun; no raster reuse is claimed as inherited inspection. No crops or proxies were needed.

Actual visual coverage was the reader contact sheet and individual full-size views of pages **1–8**, followed by the native contact sheet and individual views of excerpt pages **1–15** (parent artifact pages **615–629**). Per-page observations were written before moving to the next image batch. `visual-coverage.json` binds every inspected image to its verified hash; `visual-observations.md` contains the fresh observations.

| Reader pages | Fresh observation |
| --- | --- |
| 1 | Restrained title and clear pope/date/language identification; complete historical address. Note groups 1–2 are separate paragraphs. The original escu-/chen interruption is preserved. |
| 2 | Dense, legible two-column body; groups 3–4 remain separate and complete. No clipping, collision or displaced heading. |
| 3 | Groups 5–6 remain independent between divina en / su origen and odio / porque. Column order and text spacing are readable. |
| 4 | Continuous two-column body with group 7 as its own paragraph before hombre. No overlap or cutoff. |
| 5 | Groups 8–9 preserve the source breaks at firmeza / de que and Dios y de la / Iglesia. Both columns remain legible. |
| 6 | Groups 10–11 remain separate at fé / integra and sean / fundadas. Latin quotations and Spanish body fit cleanly. |
| 7 | Group 12 separately interrupts auto-/ridaci; group 13 preserves all four references before lejos. The source OCR spelling remains literal. |
| 8 | Genuine historical closing prayer, blessing, full dating clause, Isai. note and BENEDICTUS PP. XV subscription. Sparse left column is source-bearing; compact apparatus/rights follow a short rule. |

Every note locus below was checked in the native page-foot geometry, the rendered reader, the source selection and generated body TeX. Each has blank-LF separation and explicit `\par` before and after. The native pages are single-column and do not interleave note columns or marginal summaries. Native artifact 621 has no page-foot group.

| Group | Native artifact page | Original source LF | Reader page | Body TeX note lines; following `\par` |
| --- | --- | --- | --- | --- |
| 1 | 615 | 25512–25517 | 1 | 48–53; 54 |
| 2 | 616 | 25560–25563 | 1 | 97–100; 101 |
| 3 | 617 | 25605–25610 | 2 | 145–150; 151 |
| 4 | 618 | 25653–25665 | 2 | 193–205; 206 |
| 5 | 619 | 25708–25713 | 3 | 251–256; 257 |
| 6 | 620 | 25756–25761 | 3 | 301–306; 307 |
| 7 | 622 | 25851–25852 | 4 | 392–393; 394 |
| 8 | 623 | 25896–25903 | 5 | 439–446; 447 |
| 9 | 624 | 25946–25947 | 5 | 491–492; 493 |
| 10 | 625 | 25989–25990 | 6 | 536–537; 538 |
| 11 | 626 | 26033–26036 | 6 | 581–584; 585 |
| 12 | 627 | 26079–26079 | 7 | 628–628; 629 |
| 13 | 628 | 26121–26128 | 7 | 673–680; 681 |
| 14 | 629 | 26161–26162 | 8 | 714–715; 716 |

Qualifications: literal source word divisions, stray symbols and bounded OCR defects remain visible. They do not create sustained unreadability in the inspected pages. The note groups intentionally retain original page-break positions, including interruptions of sentences or divided words; the explicit paragraph boundaries distinguish those from fusion. The final page is sparse but retains substantial historical ending material, rather than project apparatus alone.

This acceptance covers the exact selected OCR-derived reader, mechanical fidelity, source-order note boundaries and visible layout. It does not certify translation accuracy, lexical correctness, original-print collation, work-wide textual completeness beyond the declared selection, or legal rights analysis. Rights facts were checked for exact recorded identity and clear separation of historical source wording from MIT helper software; no new rights opinion is asserted. No source, PDF, shared cache, release, tracked report or Git state was changed by this lane.

Durable scratch evidence: `verification.json`, `source-replay-evidence.json`, both replay command receipts and output texts, `native-parent-correspondence.json`, `selection-boundaries.json`, `excluded-furniture.json`, `cache-verification.json`, `raster-run-evidence.json`, `source-pdf-fidelity.json`, `note-boundary-evidence.json`, `visual-coverage.json`, `visual-observations.md`, `pdfinfo.txt`, `pdffonts.txt`, and the scoped `verify.py` script. The complete restricted extraction remains transient in this scratch only. Canonical copying, installation and integration belong to the coordinator.
