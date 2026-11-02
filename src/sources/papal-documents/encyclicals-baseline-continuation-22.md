# Independent baseline continuation review 22

Result: 3 PASS readers (10 pages); 1 CHANGES_REQUIRED reader (6 pages). All 4 assigned PDFs and all 16 pages were freshly inspected. No prior checkpoint or inherited inspection contributes coverage.

## Scope and exact identities

Assigned packet: `.scratch/encyclical-ready-package/baseline-review-packets/22.json`.
Canonical report destination: `src/sources/papal-documents/encyclicals-baseline-continuation-22.md`.
Review used only the packet's existing `raster_dir` page images and contact sheets. No rerasterization, rerendering, canonical edits, installation, cache mutation, or Git mutation occurred.

| Reader | Language | Pages | Exact PDF SHA-256 | Status |
| --- | --- | ---: | --- | --- |
| `acta.ass.039.ass-039-l000032` (Pius X, 1906-02-11) | la | 6 | `1404d2efe1b133054d1daeaaa89ce10467a1f8c2a7afcad0884a29cc79f17df3` | CHANGES_REQUIRED |
| `papal.leo-xiii.hf-l-xiii-enc-22081886-quod-multum` | la | 5 | `1d9fe030b9741829b35f65d451dc1596860f61c24fec7bff4e061b03b39825d1` | PASS |
| `papal.leo-xiii.hf-l-xiii-enc-16071892-quarto-abeunte-saeculo` | la | 3 | `8d8d0ad75878b5f5e32785eb0f5eb0c26f73a7de7f8c20dff364a55c02dd2c95` | PASS |
| `papal.leo-xiii.hf-l-xiii-enc-18091899-paternae` | la | 2 | `feb6df3c2b8f5d723debc264989ef11d65fd02f1934e0981027d2c21e6b2785a` | PASS |

## Verified pins and structural checks

All 95 identity/hash/page checks passed. Recomputed each exact PDF hash and independently obtained each page count using `pdfinfo`. Verified the common brief, frozen manifest, receipt, raster manifest, source payloads, segment manifest where applicable, every supplied source-controller record and available controller payload, and every page/contact/thumbnail raster listed in each `review-cache.json`. Receipt document rows and frozen source rows exactly equal the packet rows; the raster manifest/cache rows match the assigned PDF hashes and page counts.

Shared receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Frozen-manifest SHA-256: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.
Raster-manifest SHA-256: `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`.
Render revision: `2026-10-30T02:56:48Z`.

| Reader | Exact source payload SHA-256 |
| --- | --- |
| Pius X | `036e2b7e75b6d396ae9ef1aef98669749cbac3c5b0db08305510ffb04046dfc6` |
| Quod Multum | `81dab58b9a61ce2df6312fd092604b1f63bf9611e7b638724dbb79fc5743fea2` |
| Quarto Abeunte Saeculo | `8da45e9f3658956aaa329815f2c61de92c137a7caf6916310e3cff3e8439c792` |
| Paternae | `bd7e7b77175ef5a60607b5d70cf606770ee1863da9409e3621857e25c1ed5cde` |

Pius X selected-segment manifest SHA-256: `cfb035e625c9f1eff7000a3d3fd4418a05e79ff36afad7946b90f5eb8af1c487`.

`pdfinfo`, `pdffonts`, and `pdftotext -layout` succeeded for all four PDFs. All fonts reported by `pdffonts` are embedded Latin Modern subsets with Unicode maps. The PDFs are unencrypted, have no page rotation, and show the expected title/author/language metadata; creation/modification times correspond to the pinned render revision. These checks are not a dedicated PDF conformance audit; `qpdf` was unavailable on PATH. No installed mirror was in scope.

## Actual visual coverage

Each reader's `contact-sheets/sheet-001.png` was freshly opened. Every listed page was also separately opened from `pages/page-N.png` at original raster resolution:

| Reader | Contact-sheet pages inspected | Full-resolution pages inspected | Reused pages |
| --- | --- | --- | --- |
| Pius X | 1, 2, 3, 4, 5, 6 | 1, 2, 3, 4, 5, 6 | none |
| Quod Multum | 1, 2, 3, 4, 5 | 1, 2, 3, 4, 5 | none |
| Quarto Abeunte Saeculo | 1, 2, 3 | 1, 2, 3 | none |
| Paternae | 1, 2 | 1, 2 | none |

The full-resolution inspection covered title and identification, normal left-column/right-column continuation, justified body spacing, column separation, paragraph and heading breaks, notes, page margins, source endings, and the smaller ruled terminal apparatus. Beginning and ending wording were checked against the tracked selected source text. No clipping, collision, blank page, or page containing only project apparatus was observed.

## Reader findings

### Pius X — CHANGES_REQUIRED

**Blocking, page 5, right column:** the historical reference `(ij Rom. XIII, 12.` is fused into the body paragraph ending `... estis in Gallia;`. It appears on the same composed line immediately after the body semicolon. The following `(2) Act. v, 41.` reference is separately indented, so the first note's membership is visually ambiguous. In the pinned whole-volume source payload, physical LF line 466 contains the body ending and line 467 contains the first reference without an intervening blank line; line 468 is blank before the next reference on line 469. Mechanical retention of these bytes does not excuse note/body fusion. Preserve the historical wording/order and give the first reference a distinct source-note block before accepting new PDF bytes.

Pages 2 and 3 contain other historical reference blocks, which remain visually separate from the body. Source letter spacing and retained word divisions are conspicuous throughout this OCR-derived reader, including its long title and split source words; they slow reading but did not make the inspected text meaningfully unreadable at full resolution. This is not an OCR correction or word-level accuracy certification.

Page 6 is sparse and source-bearing: it retains substantive closing prose, the apostolic blessing, the Rome dating clause, and `PIUS PP. X` before the ruled source/rights colophon. Sparseness is not an additional failure. The exact reviewed PDF remains held for the page-5 note defect.

### Quod Multum — PASS

All five pages are legible and maintain clear two-column continuation. The final page retains substantive body and blessing, the dating clause, and `LEO PP. XIII`; its apparatus continues from the lower left into the upper right column. That continuation is readable, and the page is not apparatus-only. No blocking geometry or source-ending defect was observed.

### Quarto Abeunte Saeculo — PASS

All three pages are legible, with clear column order, title identification and section openings. The final page's single occupied column retains substantive concluding text, blessing, the dating clause, and `LEO PP. XIII` before compact apparatus. Its empty right column does not make it an apparatus-only page. No blocking geometry or source-ending defect was observed.

### Paternae — PASS

Both pages are legible, with normal two-column continuation and clear identification. Page 2 retains substantive concluding body, blessing, the dating clause, and `LEO PP. XIII`; the terminal source/rights colophon follows within the right column without overlap. No blocking geometry or source-ending defect was observed.

## Limits

This is a byte-bound presentation review of the assigned mechanical readers, using the provided rasters and tracked source boundaries. It does not establish facsimile fidelity, whole-work textual collation, historical authenticity, translation accuracy, completeness of discovery, or an independent legal/rights determination. The three web-derived readers explicitly remain uncollated normalized transcriptions. The Pius X reader retains its disclosed OCR limitations. Existing receipt text-fidelity results were verified as pinned receipt data; a new whole-source text-fidelity comparison was not run. No source text was fetched from the network. Only actual fresh page inspection is claimed, and no raster-reuse credit or prior reviewer coverage is claimed.
