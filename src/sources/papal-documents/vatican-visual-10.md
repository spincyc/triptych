# Vatican source-edition visual review — batch 10

Review date: 2026-10-26. Frozen receipt SHA-256: `08f5638fcea515986bf2c20efee50d0a6835280b6ea9959c95604b13a1a2b596`.

All 25 assigned PDFs and all 71 physical pages were newly inspected by opening each full-size 2200-pixel raster with `view_image` at original detail. Reused pages: **0**. Result: **23 PASS; 2 CHANGES_REQUIRED**. The exact frozen PDF and raster hashes were rechecked after inspection: 25 PDFs and 71 rasters matched the assignment without mismatch.

The review covered visible glyphs and font consistency, clipping and overlap, column/gutter flow, heading and page-break behavior, sparse endings, and each final source/revision notice and compact rights colophon. Supplied `pdffonts` outputs show embedded, subset, Unicode TeX Gyre Pagella regular and bold in every PDF. Every assigned `special_pages` and `font_flags` list was empty; all closing pages nevertheless received individual inspection.

This is a visual review of the source-approved frozen renderings, not source collation or renewed rights clearance. The supplied text-fidelity checks were not substituted for visual inspection. No PDF, source, manifest or generator was changed; nothing was installed or published. No replacement is approved by this initial record. Rejected hashes below remain part of the review history.

## Required corrections

- **Praeclara gratulationis**, `papal.leo-xiii.hf-l-xiii-apl-18940620-praeclara-gratulationis`, SHA-256 `03bd8ef95e757e9969f7752c8da180ef711d7c5b36501ae93a2d49b7ee96f0e9`, physical pp. 5–6: Signature-only terminal spill: p.5 ends with date; LEO PP. XIII alone moves to p.6 above source/revision and rights apparatus. Keep closing signature with dating clause or adjust pagination. Evidence: `.scratch/vatican_visual_review/rasters-01/.scratch/vatican_visual_review/frozen/pdfs/1894-06-20-papal-leo-xiii-hf-l-xiii-apl-18940620-praeclara-gratulationis-83f27738-la/pages/page-6.png`.
- **Humani Generis Redemptionem**, `papal.benedict-xv.hf-ben-xv-enc-15061917-humani-generis-redemptionem`, SHA-256 `dc8d3a62c0376d1da1e8b28915c43bd99f722dce55c3e9d1feed62253364a5b6`, physical pp. 4–5: Dating clause split across pages: p.4 ends after Pontificatus, p.5 starts with isolated Nostri tertio. before BENEDICTUS PP. XV and historical endnotes. Keep date intact with subscription. Evidence: `.scratch/vatican_visual_review/rasters-01/.scratch/vatican_visual_review/frozen/pdfs/1917-06-15-papal-benedict-xv-hf-ben-xv-enc-15061917-humani-generis-redemptionem-ac6fb370-la/pages/page-5.png`.

Both findings were sent to the catalogue coordinator and typesetting lane with exact hashes and raster loci. Their replacement review remains pending.

## Per-PDF coverage and disposition

### 1. Libertas

- Document ID: `papal.leo-xiii.hf-l-xiii-enc-20061888-libertas`.
- PDF SHA-256: `099b189ee436207746b39bf7d4250110bcce2d70876baa31c94da58196b6a410`.
- Newly inspected physical pages: **1–10** (10/10); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Dense, readable two-column body through p.9; p.10 is sparse but retains closing blessing, date and signature with source/revision and compact rights colophon together. No clipping, overlap, missing glyphs or gutter collision seen.

### 2. Pastoralis vigilantiae

- Document ID: `papal.leo-xiii.hf-l-xiii-enc-18910625-pastoralis`.
- PDF SHA-256: `11ae7806b092c39b4a2196b85ad15a543ad82dff8f015d6ce2cac1901a17742e`.
- Newly inspected physical pages: **1–3** (3/3); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Header and body hierarchy are clear; p.3 retains substantial closing text, date and signature in the left column followed by readable source/revision and rights apparatus. No clipping, overlap or glyph defects seen.

### 3. Praeclara gratulationis

- Document ID: `papal.leo-xiii.hf-l-xiii-apl-18940620-praeclara-gratulationis`.
- PDF SHA-256: `03bd8ef95e757e9969f7752c8da180ef711d7c5b36501ae93a2d49b7ee96f0e9`.
- Newly inspected physical pages: **1–6** (6/6); reused pages: **none**.
- Disposition: **CHANGES_REQUIRED**.
- Observation: CHANGES_REQUIRED: p.5 ends with the dating clause, while p.6 starts with the isolated signature LEO PP. XIII followed only by source/revision and rights apparatus. This creates an excessively sparse terminal spill and separates the signature from its date. Body glyphs and columns otherwise read clearly on pp.1–5.

### 4. Orientalium dignitas Ecclesiarum

- Document ID: `papal.leo-xiii.hf-l-xiii-apl-18941130-orientalium-dignitas`.
- PDF SHA-256: `d4bcb2cef53c63dfd2471c7e608cce7167c1032e2f9d788f8056a691e386faba`.
- Newly inspected physical pages: **1–4** (4/4); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Long title remains within margins; Roman-numbered provisions flow legibly across pp.2–3. The final page keeps the concluding provision and date with readable source/revision and rights apparatus. No clipping, overlap or missing glyphs seen.

### 5. Quum nonnullorum

- Document ID: `papal.leo-xiii.hf-l-xiii-motu-proprio-18980720-quum-nonnullorum`.
- PDF SHA-256: `6e9eb25e27e071562929efbd6f2e610de03dfde613b160caa7b2ff5563aa30cd`.
- Newly inspected physical pages: **1** (1/1); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Single-page two-column edition has clear title and source heading; closing date/signature and complete source/revision and rights colophon fit naturally in the right column. No clipping, overlap or missing glyphs seen.

### 6. Conditae a Christo

- Document ID: `papal.leo-xiii.hf-l-xiii-apc-19001208-conditae-a-christo`.
- PDF SHA-256: `64ac896bfb34d1492b45538ac1442aae2b0cda0f6315c4addc0b027d0cfd5e96`.
- Newly inspected physical pages: **1–3** (3/3); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Roman-numbered provisions have clear paragraph separation; p.3 keeps both cardinal subscriptions below the dating clause and the compact source/revision and rights apparatus in the right column. No clipping, overlap or missing glyphs seen.

### 7. Ad pastoralem

- Document ID: `papal.leo-xiii.hf-l-xiii-motu-proprio-19020405-ad-pastoralem`.
- PDF SHA-256: `03da1da44048903f1df2f21b648bd581420c4ad769886eb5f9be9d10ad28fcbe`.
- Newly inspected physical pages: **1–2** (2/2); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Dense unnumbered body flows in normal column order; p.2 keeps the date and papal signature above source/revision and rights apparatus in the right column without an extra spill. No clipping, overlap or missing glyphs seen.

### 8. Non mediocri

- Document ID: `papal.leo-xiii.hf-l-xiii-apl-19020730-non-mediocri`.
- PDF SHA-256: `15acae748a95452b2d06609aacba290661704aa595c2efea457f58c37ac32c15`.
- Newly inspected physical pages: **1–2** (2/2); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Clear two-column text with stable gutter; p.2 has a full left column and retains concluding formula/date plus readable source/revision and rights apparatus in the right column. No clipping, overlap or missing glyphs seen.

### 9. Quae Nostra

- Document ID: `papal.pius-x.hf-p-x-apl-19040303-quae-nostra`.
- PDF SHA-256: `b7428e24e63a447dcad5c12e5617a5e41f1e3373ec91ec232414f467fe38f245`.
- Newly inspected physical pages: **1–4** (4/4); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Roman-numbered provisions and historical note (1) are readable; p.4 retains closing date/subscription and note, with source apparatus continuing from the bottom of the left column into the top right, ending in revision and rights colophon. Normal column order is clear; no clipping, overlap or missing glyphs seen.

### 10. Inter multiplices curas

- Document ID: `papal.pius-x.hf-p-x-motu-proprio-19050221-inter-multiplices-curas`.
- PDF SHA-256: `c544905d7bdeb173747d09c20572aaad37d16f06b30f47c3e5ade5540dbbebd6`.
- Newly inspected physical pages: **1–8** (8/8); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Numbered paragraphs 1–81 and Roman/lettered division headings remain legible and with following text; p.8 retains substantial concluding provisions with date/signature and compact source/revision and rights colophon. No clipping, overlap or missing glyphs seen.

### 11. De Sacris Congregationibus

- Document ID: `papal.pius-x.hf-p-x-motu-proprio-19060526-sacrae-congregationi`.
- PDF SHA-256: `9e56540a7cfa55b01e28078de5581800119c60fc85654472904e5981f164bd57`.
- Newly inspected physical pages: **1** (1/1); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Single page keeps the body/date/signature in the left column and source/revision and rights apparatus at the top right. Long uppercase source heading fits; explanatory bibliographic note remains readable. No clipping, overlap or missing glyphs seen.

### 12. Sodalitium

- Document ID: `papal.pius-x.hf-p-x-apl-19090824-sodalitium`.
- PDF SHA-256: `8199c775fb23ebff4e23f19858f129280a29eeaf141af8766a57df9c39b46a8e`.
- Newly inspected physical pages: **1** (1/1); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Long uppercase source heading wraps within the left column; final date and cardinal subscription fit above readable source/revision and rights colophon in the right column. No clipping, overlap or missing glyphs seen.

### 13. Septimo iam

- Document ID: `papal.pius-x.hf-p-x-apl-19090709-septimo-iam`.
- PDF SHA-256: `768ac2f463a706f70e61082e1f60a73127610c28c68eea27445f56838fc13ccf`.
- Newly inspected physical pages: **1–5** (5/5); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Roman-numbered provisions and bracketed references remain readable across all columns. Final p.5 preserves date/signature, the full visible note series [1]–[23], source/revision notice and compact rights colophon without extra page spill; source URL wraps within margins. No clipping, overlap or missing glyphs seen.

### 14. In hac Beatissimi Petri

- Document ID: `papal.pius-x.hf-p-x-motu-proprio-19100503-in-hac`.
- PDF SHA-256: `0ddf2ca0697533bfa74b8139a9a0f6a353a3043369a2cd0216622e130786745b`.
- Newly inspected physical pages: **1–2** (2/2); reused pages: **none**.
- Disposition: **PASS**.
- Observation: The heading and dense first-page body read clearly; p.2 contains a substantial closing paragraph followed by date/cardinal subscription and complete source/revision and rights apparatus. No clipping, overlap or missing glyphs seen.

### 15. Seraphici Patriarchae

- Document ID: `papal.pius-x.hf-p-x-apl-19100815-seraphici`.
- PDF SHA-256: `bcd2e45586c6ebff51b349d5c377e7807dd8193cb151d2611312e3923f7ca13a`.
- Newly inspected physical pages: **1–3** (3/3); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Roman-numbered provisions read clearly on p.2; p.3 retains multiple closing paragraphs with date/signature and compact source/revision and rights colophon. No isolated terminal signature, clipping, overlap or missing glyphs seen.

### 16. Fuldensem

- Document ID: `papal.pius-x.hf-p-x-apl-19100902-fuldensem`.
- PDF SHA-256: `2e5be4a91dbe2712f54333d91a8664ed0ff99bf7ddca2734ef2a15294ad7f086`.
- Newly inspected physical pages: **1** (1/1); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Short single-page text remains in the left column with the source heading, closing date/cardinal subscription, source/revision and rights colophon all fitting before the footer. The unused right column is consistent with the short text. No clipping, overlap or missing glyphs seen.

### 17. In praecipuis

- Document ID: `papal.pius-x.hf-p-x-apc-19130628-in-praecipuis`.
- PDF SHA-256: `a2b74c501a7857b225bcd0eab08d063d9ddcbd94564123089082a70aff512ece`.
- Newly inspected physical pages: **1–2** (2/2); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Roman-numbered provisions flow legibly onto p.2, which retains substantial concluding body and date before the source/revision and rights colophon. No clipping, overlap or missing glyphs seen.

### 18. Quandoquidem in iis

- Document ID: `papal.benedict-xv.hf-ben-xv-motu-proprio-19150916-quandoquidem-in-iis`.
- PDF SHA-256: `ccab56960ff9a8473b714fc0dc80e71e2ef221671598d453c69e965488430f5a`.
- Newly inspected physical pages: **1** (1/1); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Short single-page edition fits source heading, complete body, date/signature and source/revision and rights colophon in the left column, with an unused right column. No clipping, overlap or missing glyphs seen.

### 19. Humani Generis Redemptionem

- Document ID: `papal.benedict-xv.hf-ben-xv-enc-15061917-humani-generis-redemptionem`.
- PDF SHA-256: `dc8d3a62c0376d1da1e8b28915c43bd99f722dce55c3e9d1feed62253364a5b6`.
- Newly inspected physical pages: **1–5** (5/5); reused pages: **none**.
- Disposition: **CHANGES_REQUIRED**.
- Observation: CHANGES_REQUIRED: the dating clause is split after Pontificatus at the foot of p.4; p.5 opens with the isolated continuation Nostri tertio. and the papal signature before endnotes. Keep the date intact with its subscription. Endnotes [1]–[39], source/revision and compact rights colophon are readable on p.5; body glyphs and columns are clear throughout.

### 20. Inter potiores

- Document ID: `papal.benedict-xv.hf-ben-xv-apl-19191110-inter-potiores`.
- PDF SHA-256: `483684271687ca5aa84614e9ede11b38129d49c4b6d3d034b7b4f86f62b6f3e5`.
- Newly inspected physical pages: **1** (1/1); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Long uppercase source heading wraps cleanly; p.1 retains concluding formula/date/cardinal subscription and source/revision and rights colophon in the right column. No clipping, overlap or missing glyphs seen.

### 21. Inter Suebiae

- Document ID: `papal.benedict-xv.hf-ben-xv-apl-19200614-inter-suebiae`.
- PDF SHA-256: `8d97be70ba7e01cd03bc37696c523cfd4be6dcedb68a72ca0ac002a950bfb72c`.
- Newly inspected physical pages: **1–2** (2/2); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Body and long source heading are clear; p.2 keeps final provisions with date/cardinal subscription and source/revision and rights apparatus together in the left column. No clipping, overlap or missing glyphs seen.

### 22. Romanorum Pontificum

- Document ID: `papal.pius-xi.hf-p-xi-apl-19230413-romanorum-pontificum`.
- PDF SHA-256: `31ec39a2c2c1ff37400bb0577d6b962539c9161e03e1556e085112bb973d240c`.
- Newly inspected physical pages: **1** (1/1); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Single-page edition flows into the right column, where closing formula/date/cardinal subscription and source/revision and rights apparatus remain readable within margins. No clipping, overlap or missing glyphs seen.

### 23. Motu Proprio Post datam

- Document ID: `papal.pius-xi.hf-p-xi-motu-proprio-19230420-post-datam`.
- PDF SHA-256: `d391f81556cad638f7f4a03bd9ae7787c8fee582fba33889c38de125e44afae1`.
- Newly inspected physical pages: **1** (1/1); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Short single-page edition keeps heading, body, complete date/signature and source/revision and rights apparatus in the left column. No clipping, overlap or missing glyphs seen; literal irregular word spacing in the uncollated text is outside this visual review's source-collation scope.

### 24. Sagiensis dioecesis

- Document ID: `papal.pius-xi.hf-p-xi-apl-19280829-sagiensis-dioecesis`.
- PDF SHA-256: `c2d540b51d8296f248e861dee57683a24dc3d826ce6643ad1079f87d6dfa4562`.
- Newly inspected physical pages: **1** (1/1); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Single-page body flows cleanly into the right column, keeping date/cardinal subscription with source/revision and rights apparatus. Long uppercase source heading fits within margins. No clipping, overlap or missing glyphs seen; literal irregular spacing in source words is outside this visual review's source-collation scope.

### 25. Cum vicarius apostolicus

- Document ID: `papal.pius-xi.hf-p-xi-apl-19290318-cum-vicarius`.
- PDF SHA-256: `f752254a6df06d0b1e8a4145b47ea3cb72969076bc8dceb346e68a64628bf694`.
- Newly inspected physical pages: **1** (1/1); reused pages: **none**.
- Disposition: **PASS**.
- Observation: Single-page edition keeps the complete source body/date/cardinal subscription in the left column. Source apparatus continues at the top right and ends with readable revision and rights colophon; no apparatus-only extra page, clipping, overlap or missing glyphs seen.

The scratch result records each physical page and its exact raster SHA-256. Passing observations apply only to the hashes recorded here; any changed PDF requires an explicitly assigned replacement review.
