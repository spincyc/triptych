# Vatican mechanical editions — visual review batch 04

Review date: 2026-10-26. Overall disposition: **CHANGES_REQUIRED**.

Personally inspected all **71 physical pages in 24 PDFs**, opening every assigned 2200-pixel page raster individually at original detail. No pages were reused. Twenty-two PDFs pass visual review; two require changes under the exact rejected hashes below. The review checked visible glyphs, clipping/overlap, column and gutter flow, headings and page breaks, terminal spills, and final source/revision/rights apparatus. No supplied special-page or font flags were present.

Frozen receipt SHA-256: `08f5638fcea515986bf2c20efee50d0a6835280b6ea9959c95604b13a1a2b596`.

All 24 frozen PDF hashes and all 71 raster hashes were independently checked against the assignment and matched. `pdfinfo` read all PDFs and confirmed their assigned page counts. Fresh `pdffonts` outputs match the assignment: TeX Gyre Pagella Regular and Bold are embedded, subset, and Unicode mapped throughout. No visible missing glyphs, clipping, overlap, or gutter intrusion was observed.

This is a visual review of source-approved mechanical editions. It does not establish independent historical collation or rights clearance. Installation and publication remain outside this review. `qpdf` was unavailable; broader PDF structure and source-fidelity gates belong to the coordinating build lane. Changed PDF hashes require assigned re-review; rejected hash history below remains part of this record.

## Findings

1. **CHANGES_REQUIRED — display-title-misspelling.** `papal.leo-xiii.hf-l-xiii-apc-18830530-misericors-dei-filius`, physical p. 1, PDF SHA-256 `8d63ea15a7773ec471615b2726be81d26f209e1857b182ca58fe4a8aa7182d48`. Project title reads “Misericords Dei Filius” (extra d); retained source heading and incipit read “Misericors Dei Filius”.

   Raster: `.scratch/vatican_visual_review/rasters-01/.scratch/vatican_visual_review/frozen/pdfs/1883-05-30-papal-leo-xiii-hf-l-xiii-apc-18830530-misericors-dei-filius-d46134f6-la/pages/page-1.png` (SHA-256 `f383141f617a6b67bd68d1227729c90a153cb6230ee5dbe9406f5177c13d32f7`).

2. **Nonblocking observation — apparatus-spacing.** `papal.pius-x.hf-p-x-apl-19081016-satis-constat`, physical p. 1, PDF SHA-256 `4368e873f023ccabde3ea2bceb581cb98b16ed31461831bd681b3daf98dd3a5f`. Project source note joins words/numbers: “AASvolumeIV”, “dates1909”, “AASvolume1”, “pages202–203”. Meaning remains readable; spacing polish recommended.

   Raster: `.scratch/vatican_visual_review/rasters-01/.scratch/vatican_visual_review/frozen/pdfs/1908-10-16-papal-pius-x-hf-p-x-apl-19081016-satis-constat-245639ef-la/pages/page-1.png` (SHA-256 `ef748821452ccf53de461aa8d976b386c388abc1044e76f6d044920c102c7b3d`).

3. **CHANGES_REQUIRED — orphan-rubric-heading.** `papal.pius-x.hf-p-x-apc-19111101-divino-afflatu`, physical p. 6, PDF SHA-256 `8de4026f110948e8b9e4cd80f077fa662d2e6927a5ea5d4563f3cfd91fbb4008`. Right-column final line “In Dominica IV Quadragesimae:” is stranded at the foot of p. 6; its antiphon starts p. 7. Keep the rubric heading with its text.

   Raster: `.scratch/vatican_visual_review/rasters-01/.scratch/vatican_visual_review/frozen/pdfs/1911-11-01-papal-pius-x-hf-p-x-apc-19111101-divino-afflatu-c1af6fc7-la/pages/page-6.png` (SHA-256 `fd90c15db40dc18d44591a0d9075ae2fa7bb040ecf19a8e0af5de1cbcc689b97`).

4. **Nonblocking observation — sparse-terminal-spill.** `papal.pius-x.hf-p-x-apc-19111101-divino-afflatu`, physical p. 7, PDF SHA-256 `8de4026f110948e8b9e4cd80f077fa662d2e6927a5ea5d4563f3cfd91fbb4008`. Only seven source lines plus apparatus occupy the upper left of final p. 7. Investigate compact closing fit alongside the orphan-heading repair.

   Raster: `.scratch/vatican_visual_review/rasters-01/.scratch/vatican_visual_review/frozen/pdfs/1911-11-01-papal-pius-x-hf-p-x-apc-19111101-divino-afflatu-c1af6fc7-la/pages/page-7.png` (SHA-256 `c1bf036f5a8c2e4d61c5599882cb4da41ed0c9c0c90a7107f05283296e9b3589`).

## Exact PDF coverage and disposition

All page ranges below were personally inspected in full. PASS applies only to the named bytes.

### 01. Tuas libenter

- Identity: `papal.pius-ix.epistola-tuas-libenter-21-decembris-1863`.
- PDF SHA-256: `a784c62b4adba6181b6f40509898ec258198b3ecf498963daacbb146a3ae4b76`.
- Individually inspected physical pages: 1–3 (3 total); reused pages: none.
- Disposition: **PASS**.

Clear compact identification; clean Latin glyphs and uninterrupted two-column flow across pp. 1–3. Dating clause, signature, source/revision and rights colophon fit on p. 3.

### 02. Non sine gravissimo

- Identity: `papal.pius-ix.litterae-apostolicae-non-sine-gravissimo-24-februarii-1870`.
- PDF SHA-256: `10628c0ef47c582d9590e2580938b3d2ae14aaf325818d23b9ad1bb64d8ceaf9`.
- Individually inspected physical pages: 1–2 (2 total); reused pages: none.
- Disposition: **PASS**.

Long opening title wraps cleanly within the left column; pp. 1–2 preserve clear gutter and margins. Closing signature and complete compact apparatus fit p. 2.

### 03. Grande Munus

- Identity: `papal.leo-xiii.hf-l-xiii-enc-30091880-grande-munus`.
- PDF SHA-256: `9b1d169512c8a2dfed80b1848bced73ecae38aae67569e4fd3ca88fe768515f2`.
- Individually inspected physical pages: 1–4 (4 total); reused pages: none.
- Disposition: **PASS**.

Four pages have readable Latin glyphs, clean wrap of the long opening identification, and orderly column/page transitions. Final page carries substantial source ending, signature, source/revision and rights colophon in the left column without spill.

### 04. Sancta Dei Civitas

- Identity: `papal.leo-xiii.hf-l-xiii-enc-03121880-sancta-dei-civitas`.
- PDF SHA-256: `bdc2181c3cd4a1b8df22ec28d5a10760e12a2094d98c38f7f07d56dc7754aff9`.
- Individually inspected physical pages: 1–3 (3 total); reused pages: none.
- Disposition: **PASS**.

Long opening headings remain inside the column; clean Latin glyphs and continuous reading flow on pp. 1–3. Final date/signature and compact source/revision/rights apparatus are clear on p. 3.

### 05. Misericords Dei Filius

- Identity: `papal.leo-xiii.hf-l-xiii-apc-18830530-misericors-dei-filius`.
- PDF SHA-256: `8d63ea15a7773ec471615b2726be81d26f209e1857b182ca58fe4a8aa7182d48`.
- Individually inspected physical pages: 1–4 (4 total); reused pages: none.
- Disposition: **CHANGES_REQUIRED**.

p. 1 project heading misspells the incipit as “Misericords Dei Filius”; source heading/body read “Misericors Dei Filius”. Layout itself is clean on pp. 1–4, including section signs/Roman numerals, headings and final dated signature/source/revision/rights apparatus.

### 06. Sapienter olim

- Identity: `papal.leo-xiii.hf-l-xiii-apl-18911130-sapienter-olim`.
- PDF SHA-256: `573daedbbd12667c45e26c94918dadacdf975a99f6cbe6548c9e246d255c1be5`.
- Individually inspected physical pages: 1–2 (2 total); reused pages: none.
- Disposition: **PASS**.

Two pages show clear glyphs, wrapped heading and clean column transitions. Final page has substantial source text and complete date/signature plus source/revision/rights colophon without an isolated apparatus page.

### 07. Alumnis Seminarii Vaticani

- Identity: `papal.leo-xiii.hf-l-xiii-motu-proprio-18920725-alumnis-seminarii`.
- PDF SHA-256: `15ad2bfcedf2695a2cfa257db9f9b996f8af5372d456cb18d955b1885a4b887e`.
- Individually inspected physical pages: 1 (1 total); reused pages: none.
- Disposition: **PASS**.

Single-page two-column edition has clear opening identification and source ending/signature; terminal source/revision and rights colophon fit beneath the right-column ending with generous clearance.

### 08. Apostolicae curae

- Identity: `papal.leo-xiii.litterae-apostolicae-apostolicae-curae-13-septembris-1896`.
- PDF SHA-256: `057286ee4ec06b55370d6e497b15d6ba0a3d8e75606cca20bd808269ecf02087`.
- Individually inspected physical pages: 1–5 (5 total); reused pages: none.
- Disposition: **PASS**.

All five pages have clear Latin glyphs and stable two-column flow; headings, quotations and page transitions remain unobstructed. Final dating clause and source/revision/rights apparatus fit in p. 5 right column.

### 09. Paternae

- Identity: `papal.leo-xiii.hf-l-xiii-enc-18091899-paternae`.
- PDF SHA-256: `044ba71c5c404e803d7d74075f793d51672e00cae7cca6c76415222f709c1961`.
- Individually inspected physical pages: 1–2 (2 total); reused pages: none.
- Disposition: **PASS**.

Clear compact identification and clean two-page Latin flow; final date/signature and complete source/revision/rights apparatus fit in p. 2 right column.

### 10. Apostolicae Sedi

- Identity: `papal.pius-x.hf-p-x-motu-proprio-19050508-apostolicae-sedi`.
- PDF SHA-256: `734a133fcca33a37a658a4e58f8640b622701e8485210bae30bb04f07784e9e2`.
- Individually inspected physical pages: 1 (1 total); reused pages: none.
- Disposition: **PASS**.

Single-page edition maintains clear title, long opening heading and readable Latin glyphs. Final source/revision and rights colophon fit below the signature in the right column.

### 11. Gravissimo Officii Munere

- Identity: `papal.pius-x.hf-p-x-enc-10081906-gravissimo-officii-munere`.
- PDF SHA-256: `568c20784fc2d34f8dfc7873c126de344585f9c6d96a83162aaefa18b8e87a16`.
- Individually inspected physical pages: 1–2 (2 total); reused pages: none.
- Disposition: **PASS**.

Two-page source text and headings are legible and within margins. On p. 2 the source/revision note ends at left-column foot and the two-line rights colophon continues at right-column top; it remains on the same final page, without a sparse additional page.

### 12. Satis constat

- Identity: `papal.pius-x.hf-p-x-apl-19081016-satis-constat`.
- PDF SHA-256: `4368e873f023ccabde3ea2bceb581cb98b16ed31461831bd681b3daf98dd3a5f`.
- Individually inspected physical pages: 1 (1 total); reused pages: none.
- Disposition: **PASS**.

Single-page source text, date/signature and terminal colophon are clear and unobstructed. Minor apparatus typography: p. 1 source note joins words/numbers (“AASvolumeIV”, “dates1909”, “AASvolume1”, “pages202–203”); readable but spacing should be polished.

### 13. Nobis exponendum

- Identity: `papal.pius-x.hf-p-x-apl-19100621-nobis-exponendum`.
- PDF SHA-256: `d2bcb315c0832083ae36460255044743dd0940ba2bb5b2f47f4fb1d465e7b1c6`.
- Individually inspected physical pages: 1 (1 total); reused pages: none.
- Disposition: **PASS**.

Single-page edition fits entirely in the left column; headings, date/signature and compact source/revision/rights apparatus remain clear within margins, with no additional terminal page.

### 14. Divino afflatu

- Identity: `papal.pius-x.hf-p-x-apc-19111101-divino-afflatu`.
- PDF SHA-256: `8de4026f110948e8b9e4cd80f077fa662d2e6927a5ea5d4563f3cfd91fbb4008`.
- Individually inspected physical pages: 1–7 (7 total); reused pages: none.
- Disposition: **CHANGES_REQUIRED**.

p. 6 right-column foot strands rubric heading “In Dominica IV Quadragesimae:” from its antiphon on p. 7. Final p. 7 has seven source lines plus source/revision/rights apparatus in the upper left; investigate compact closing fit. All seven pages otherwise show clear glyphs, note numbers and two-column flow.

### 15. Ex quo Ecclesia

- Identity: `papal.benedict-xv.hf-ben-xv-apl-19200523-ex-quo-ecclesia`.
- PDF SHA-256: `296ca60275e8c7a02c7f706fa0445fd00c2b1d3c5fc194c8dd517f5a3ced7b1f`.
- Individually inspected physical pages: 1–3 (3 total); reused pages: none.
- Disposition: **PASS**.

All three pages have clear Latin glyphs and stable column/page transitions. Long opening heading wraps cleanly; final date/signature and source/revision/rights apparatus fit in p. 3 right column.

### 16. Spiritus Paraclitus

- Identity: `papal.benedict-xv.hf-ben-xv-enc-15091920-spiritus-paraclitus`.
- PDF SHA-256: `c1cb1bf6833780cf480acf7e3b525ae9c74334f2ee63eb4e2b8eb066b50c4b2b`.
- Individually inspected physical pages: 1–14 (14 total); reused pages: none.
- Disposition: **PASS**.

All 14 pages personally inspected. Long Latin quotations, parenthetical note markers and notes 1–144 remain legible; no glyph loss, clipping, overlap or gutter intrusion observed. Source ending/date/signature on p. 13 flows into historical endnotes; p. 14 ends with complete source/revision/rights apparatus in the right column.

### 17. Quod nobis

- Identity: `papal.benedict-xv.hf-ben-xv-apl-19200925-quod-nobis`.
- PDF SHA-256: `f4bdfab3b5cc3b31b594d5e91e0a354871bd03475dcc413d9640ddb694757bb3`.
- Individually inspected physical pages: 1 (1 total); reused pages: none.
- Disposition: **PASS**.

Clear one-page Latin edition, including long opening heading and final date/signature. Source/revision and rights colophon fit in the right column without clipping or overlap.

### 18. Unigenitus Dei on the criteria for the formation of clergy

- Identity: `papal.pius-xi.hf-p-xi-apl-19240319-unigenitus-dei`.
- PDF SHA-256: `8d61ed4da34e8ec4728e07b67b1858ae9aa244d467186bdece4f85c8585798b2`.
- Individually inspected physical pages: 1–6 (6 total); reused pages: none.
- Disposition: **PASS**.

All six pages personally inspected. Very long project title stays inside the page margins; body quotations, bracketed notes, paragraph breaks and endnotes remain legible. Final date/signature and complete source/revision/rights apparatus fit p. 6 without extra terminal page.

### 19. Apostolici officii

- Identity: `papal.pius-xi.hf-p-xi-apc-19280119-apostolici-officii`.
- PDF SHA-256: `7d30857327588bdf1798cb72ca3077effa650e99be47169bdca18749253352a6`.
- Individually inspected physical pages: 1 (1 total); reused pages: none.
- Disposition: **PASS**.

Single-page edition has clear accented name glyphs, clean wrapped headings, full signature block and terminal source/revision/rights apparatus in the right column.

### 20. Quum ex Apostolico

- Identity: `papal.pius-xi.hf-p-xi-apl-19280718-quum-ex`.
- PDF SHA-256: `34f80c8d7c56e5010a8a3630f679e73de95bbc341c2d4ba05ecbe4a12dfd597e`.
- Individually inspected physical pages: 1 (1 total); reused pages: none.
- Disposition: **PASS**.

Single-page edition keeps source/date/signature and source/revision note in the left column; the two-line rights colophon continues at right-column top on the same page. No clipping, overlap or additional terminal page.

### 21. Ea, quae catholicae

- Identity: `papal.pius-xi.hf-p-xi-apl-19290221-ea-quae`.
- PDF SHA-256: `b114bcb8fdabc20503083f6159e9a2ad60cc41e1f3a1baa367ae811e8f2b924b`.
- Individually inspected physical pages: 1 (1 total); reused pages: none.
- Disposition: **PASS**.

Single-page edition has clean Latin text and opening heading wraps; closing dating clause continues into right column before signature and complete source/revision/rights apparatus.

### 22. Cum ex apostolico

- Identity: `papal.pius-xi.hf-p-xi-apl-19290606-cum-ex`.
- PDF SHA-256: `04dc9ed1889c40c36cdca9ab1f44bd576f13e9cd1f0770b419c36bfff226d172`.
- Individually inspected physical pages: 1 (1 total); reused pages: none.
- Disposition: **PASS**.

Single-page source and terminal apparatus fit in the left column; title, date/signature, source/revision and rights colophon are clear with no spill or overlap.

### 23. Ardenti amore

- Identity: `papal.pius-xi.hf-p-xi-apl-19290616-ardenti-amore`.
- PDF SHA-256: `69363654e8fae226863f25751d4a17cd0ba010c41891a36f13998f003bd32130`.
- Individually inspected physical pages: 1–3 (3 total); reused pages: none.
- Disposition: **PASS**.

Three pages retain clear Latin and accented-name glyphs, opening heading wraps and normal two-column/page flow. Final page contains substantial closing source text with date/signature and complete compact source/revision/rights apparatus.

### 24. Mites corde

- Identity: `papal.pius-xi.hf-p-xi-apl-19290623-mites-corde`.
- PDF SHA-256: `fc195bb3a34d3df8b6c22c61f87f195b3780d26734306f7773cbf4d38c1dd529`.
- Individually inspected physical pages: 1–2 (2 total); reused pages: none.
- Disposition: **PASS**.

Two pages retain clean heading/body glyphs and normal reading flow. Final date, two-line signature and complete source/revision/rights colophon fit in p. 2 right column with clearance.
