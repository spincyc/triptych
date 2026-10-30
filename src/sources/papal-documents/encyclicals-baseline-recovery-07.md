# Baseline recovery 07 — cold PDF review

Complete packet: 2 of 2 documents completed; all 15 pages freshly inspected in contact sheets and at full size. Both documents PASS for layout with the qualifications below.

Review scope: classic two-column mechanical historical source editions. Existing repository-generated rasters were freshly viewed; no inherited inspection, reused pages or reuse proofs. No PDF, source, canonical report, shared cache, installed output or Git state was changed.

## Iucunda Sane — Latin — PASS

- Identity: `papal.pius-x.hf-p-x-enc-12031904-iucunda-sane`.
- PDF SHA-256: `58718f37b2a9b437182e43630689bdf34c32d37d96a1f728e40fb1637a919e91`; actual page count: 8.
- Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
- Actual fresh contact-sheet views: pages 1–8, sheet-001. Actual original/full-size views: pages 1–8.

All eight pages have legible, contained two-column text in normal order, consistent justified line spacing and clear margins/gutter. Source protocol and citations are readable; no material clipping, overlap, heading split, orphan heading or source-note fusion was observed. Page-specific observations are saved in doc-01-review.json.

Page 8 is sparse but source-bearing: the blessing, dating clause and `PIUS PP. X` subscription precede the compact source/rights apparatus. The terminal apparatus does not create a project-only page. Beginning and ending were checked against the pinned source (literal-LF lines 1, 3, 5, 7, 85, 87, 89) and body.tex (including LF135–142). TeX has explicit paragraph ends after the final blessing and dating clause. Parenthetical references are integrated in the retained web source; no separate page-foot note was identified. Page 1's `Venerabiles Frodres` matches source LF7 and body.tex LF18 and is recorded as retained transcription wording.

The exact PDF, receipt, frozen manifest, source, body.tex, sidecar pinset, source-controller records/payloads and raster manifest/cache images were verified programmatically. The sidecar source and receipt rows equal their frozen records. pdfinfo confirms eight pages; all four listed Latin Modern font subsets are embedded with Unicode maps. Exact checks and image hashes are retained in pin-verification.json; PDF metadata/font output is retained alongside it.

Limits: this is a layout review of an uncollated normalized web transcription, not whole-source/facsimile collation, translation validation or a new rights decision. Source identity/disclosed limits and the receipt's fidelity pass were checked as retained pinned evidence; no full-body fidelity replay or rebuild was performed.

## Catholicity in the United States (Longinqua) — English — PASS

- Identity: `papal.leo-xiii.hf-l-xiii-enc-06011895-longinqua`.
- PDF SHA-256: `496097463da71bf8b67a56d62d0b40c4b138c6feffe869ca9ee7906662deb312`; actual page count: 7.
- Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
- Actual fresh contact-sheet views: pages 1–7, sheet-001. Actual full-size views: pages 1–7, including all apparent note-bearing pages 4–6.

The title, issuer/date/language and source opening are clear. Both columns have readable justified lines, ordinary paragraph indentation, a clear gutter and contained page numbers. No material clipping, overlap, orphan heading or source-note fusion was observed. Page 7 is sparse but contains the historical Apostolic Benediction paragraph above compact terminal source/rights apparatus; it is not apparatus-only.

The historical citations on page 4 (source literal-LF 1763, 1765, 1767; TeX LF72, 75, 78), page 5 (source LF1783; TeX LF102) and page 6 (source LF1797; TeX LF123) are visibly distinct paragraphs. Exact generated TeX has explicit paragraph boundaries before/after each: LF70/73, 73/76, 76/79, 100/103 and 121/124 respectively. Source notes have blank-line boundaries. The page 5 reference `' Encyc. Arcanum.` interrupts the body sentence between `by` and `nature`; this source-order interruption is disclosed here and is not a fusion finding. Page 6's `Ep. Cognita Nobis...` reference is separate from the following retained `1 "Praeclara," has...` body paragraph. Exact contexts are retained in doc-02-note-boundaries.json.

The source's OCR defects remain conspicuous: broken-word forms and localized corrupt tokens such as `pubHc`, `3'ou`, `ApostoUc` on page 3 and `unitj?` with a caret on page 4. They reduce textual quality; no continuous passage was judged materially unreadable in this bounded review. Acceptance does not correct them or certify their wording. Source paragraph breaks within divided words/sentences also remain, including `apos`/`tolic` on page 3.

The exact source segment is literal-LF 1721–1805. Opening title/date/body boundaries (LF1721/1723/1725) and the closing blessing (source LF1805; TeX LF135 followed by LF136 paragraph end) match the viewed boundaries. Segment identity, artifact and ranges were verified against its pinned TOML. All PDF/receipt/frozen/source/body/sidecar/controller/segment/raster pins passed; 15 cached image hashes were checked. pdfinfo confirms seven pages and correct identification; all four Latin Modern font subsets are embedded with Unicode maps.

Limits: historical English web transcription of the 1903 Benziger edition, individual translator unidentified, encoding-only repair as disclosed, with full print collation outstanding. OCR word and source-date errors remain uncorrected. This is a layout review, not full-source/facsimile collation, translation validation, note-anchor reconstruction or a new rights decision. The pinned receipt's fidelity pass was verified as retained evidence; no independent full-body fidelity replay was performed.

## Exact common and source pins

- Frozen manifest SHA-256: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.
- Raster review-run manifest SHA-256: `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`.
- Render revision: `2026-10-30T02:56:48Z` for both PDFs.
- Iucunda Sane source SHA-256: `ccfec5275c88a2120242dddf1157822618781133bf996de390b78cfc76afb7ba`; body.tex SHA-256: `99e64690db0fe4a7588c7feb1bf39d93bdf7a7a3dba988c8437af799f35e87f4`; source pinset SHA-256: `81d37a0641057abddad3b26ef8ed01439826e2a0643359f88ea3479bd86c92f3`.
- Longinqua source SHA-256: `ed8e5a405701a51eec9124f0e63a4db7740ded35545fe5d99874ac9581541879`; body.tex SHA-256: `d578e2959832b21e8965347dc7c8988f234a28c78197eff59c438274b2437bb7`; source pinset SHA-256: `000fc095ac143068a726590f06cb64c3198c3bdbd0bcb21bde447b0e95625224`; segment manifest SHA-256: `624da64d4e38c6f1baf8a108d00f7d7f65d85e8be13c280f78211450548be9a0`.

Only the assigned scratch directory was written. All observations are fresh; reused_pages and reuse_proofs are empty for both documents. No old checkpoint inspection or acceptance was inherited. No blockers or live tool handles remain.
