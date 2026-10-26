# Vatican mechanical reading editions: visual review batch 12

Reviewed 2026-10-26: **25 PDFs, 71 physical pages personally inspected; 22 PASS, 3 CHANGES_REQUIRED**. Each assigned page was opened individually with `view_image` at original detail from its full-page 2200-pixel review raster. No contact sheet, extraction, or hash enumeration was counted as visual inspection. **No prior review was reused (0 pages).**

Frozen receipt SHA-256: `08f5638fcea515986bf2c20efee50d0a6835280b6ea9959c95604b13a1a2b596`.

The exact frozen PDF hashes (25/25) and raster hashes (71/71) were independently recomputed and matched the assignment. Supplied `pdffonts` rows show embedded/subset/Unicode fonts throughout and no font flags; this report does not claim a fresh `pdffonts` invocation. Every `special_pages` list was empty; all closing and final pages were nevertheless explicitly inspected. Review covered visible glyph/font integrity, clipping, overlap, column/gutter continuation, heading and page breaks, terminal spills, source/revision notices, and final-page rights colophons.

## Changes required: original rejected hashes

### Tametsi Futura Prospicientibus — physical page 6

- Work: `papal.leo-xiii.hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus`.
- PDF SHA-256: `17a448c30b7ef4d4a1704d10d8cc5993af04329cc7d2ae0ddda47461766b9270`.
- Exact assigned raster: `.scratch/vatican_visual_review/rasters-01/.scratch/vatican_visual_review/frozen/pdfs/1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-la/pages/page-6.png`.
- Finding: Sparse terminal spill: p.6 contains only two lines completing the final blessing, two-line dating clause and one-line papal subscription before source/revision apparatus and rights colophon; right column and most of page are empty. Keep closing with preceding text and remove avoidable sixth-page spill.

### Quum, arcano — physical page 2

- Work: `papal.pius-x.hf-p-x-apl-19040211-quum-arcano`.
- PDF SHA-256: `b0340799ac5971be1cadf7a993958d6db09730d8866143d75abde7956ab31090`.
- Exact assigned raster: `.scratch/vatican_visual_review/rasters-01/.scratch/vatican_visual_review/frozen/pdfs/1904-02-11-papal-pius-x-hf-p-x-apl-19040211-quum-arcano-395c6b30-la/pages/page-2.png`.
- Finding: A standalone comma is rendered as its own paragraph between the final cardinal subscription (Pro-Datarius.) and the Source notice. Resolve against approved source and exclude wrapper punctuation if extraneous; the isolated mark is visibly anomalous.

### Tribus Circiter — physical page 3

- Work: `papal.pius-x.hf-p-x-enc-05041906-tribus-circiter`.
- PDF SHA-256: `4c08a8aed416e0504c3cb36a4da02858c7c8bbcf64df094672fabbae6194e6da`.
- Exact assigned raster: `.scratch/vatican_visual_review/rasters-01/.scratch/vatican_visual_review/frozen/pdfs/1906-04-05-papal-pius-x-hf-p-x-enc-05041906-tribus-circiter-ff59a7f6-la/pages/page-3.png`.
- Finding: Sparse terminal spill: p.3 isolates only the one-line papal subscription PIUS PP. X followed by source/revision notice and rights colophon. The dating clause ends p.2; keep subscription with closing and eliminate avoidable third-page spill.

These findings retain their rejected hash history. Any replacement requires a separate exact-hash review; these decisions do not transfer to rebuilt PDFs.

## Per-PDF coverage and disposition

### 1. Address Multiplices inter

- Work: `papal.pius-ix.allocutio-multiplices-inter-25-septembris-1865`.
- PDF SHA-256: `ecd90c016b78ac444f3d34baa1fc3ac6603b617b36420eea0b8438ae51c3987b`.
- Physical pages personally inspected: 1, 2. Prior review reused: none.
- Status: **PASS**.
- Observation: Both pages clear; full closing paragraph and source/revision notice remain legible at foot of left column on p.2; compact rights colophon starts right column. No overlap or clipping.

### 2. Romanos Pontifices

- Work: `papal.leo-xiii.hf-l-xiii-apc-18810513-romanos-pontifices`.
- PDF SHA-256: `b92be30591d2b35347dee8394bc4ffcc63296ef4fb0a23fa60f0e7e0b288cb14`.
- Physical pages personally inspected: 1, 2, 3, 4, 5, 6, 7, 8, 9. Prior review reused: none.
- Status: **PASS**.
- Observation: Nine pages show continuous readable columns and intact numbered source notes. P.9 is a sparse but substantive continuation of note 49 and notes 50–53, followed by source/revision notice and rights colophon; no apparatus-only extra page, clipping, or overlap.

### 3. Eximiam praeclarorum

- Work: `papal.leo-xiii.hf-l-xiii-apl-18891109-eximiam-praeclarorum`.
- PDF SHA-256: `d8d84470610ffc9bfe1325b6c299c38ab9764ed1d76664ffd37f2b7100174a23`.
- Physical pages personally inspected: 1, 2, 3. Prior review reused: none.
- Status: **PASS**.
- Observation: Clear headings and three-page column continuation. P.3 dating clause, cardinal subscription, explicit historical abbreviated-closing/transcription notice, revision, and rights colophon are legible without collision.

### 4. Non maius

- Work: `papal.leo-xiii.hf-l-xiii-apl-18950615-non-maius`.
- PDF SHA-256: `3f00b8c140b5b748a7af974602193049e1aed674df439b70d0bca9f98d3d360c`.
- Physical pages personally inspected: 1, 2, 3, 4. Prior review reused: none.
- Status: **PASS**.
- Observation: Four pages clear, including p.4 full-length closing left column, dating clause MDCCCXCI, accented cardinal subscription, source/revision notice, and colophon. Displayed 1891-06-15 agrees with visible closing; no spill page.

### 5. Fidentem piumque animum

- Work: `papal.leo-xiii.hf-l-xiii-enc-20091896-fidentem-piumque-animum`.
- PDF SHA-256: `5631505493db4c9f871bc9b9a48420e51f368645f4d03468db2d16eb457d3ebe`.
- Physical pages personally inspected: 1, 2, 3. Prior review reused: none.
- Status: **PASS**.
- Observation: Three pages clear; dense original opening identification remains readable. P.3 final blessing, dating clause, papal subscription, source/revision notice and colophon fit in right column with no collision.

### 6. Officiorum ac munerum

- Work: `papal.leo-xiii.hf-l-xiii-apc-18970125-officiorum-ac-munerum`.
- PDF SHA-256: `54578739b7341d3f3685fb5745c0467d95eef803faea53fc378087ed97bdb19c`.
- Physical pages personally inspected: 1, 2, 3, 4, 5. Prior review reused: none.
- Status: **PASS**.
- Observation: Five pages clear; title, chapter headings and source numbering remain readable across columns. P.5 dating clause and both subscriptions end left column; source/revision notice and rights colophon start right column without overlap or extra page.

### 7. Tametsi Futura Prospicientibus

- Work: `papal.leo-xiii.hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus`.
- PDF SHA-256: `17a448c30b7ef4d4a1704d10d8cc5993af04329cc7d2ae0ddda47461766b9270`.
- Physical pages personally inspected: 1, 2, 3, 4, 5, 6. Prior review reused: none.
- Status: **CHANGES_REQUIRED**.
- Observation: All six pages inspected. Glyphs, margins, column continuation and apparatus are clear, but p.6 isolates a five-line closing tail with apparatus on a mostly empty page; pagination change required.

### 8. Vigilantiae studiique

- Work: `papal.leo-xiii.hf-l-xiii-apl-19021030-vigilantiae-studiique`.
- PDF SHA-256: `f12664dc24f6694443649e2b65ffa552fa7ddb1364cd3fda186262074c3c7f26`.
- Physical pages personally inspected: 1, 2. Prior review reused: none.
- Status: **PASS**.
- Observation: Both pages clear; quoted passage and normal column continuation readable. Dating clause, papal signature, source/revision notice and rights colophon all fit p.2.

### 9. Litteras ante annos

- Work: `papal.leo-xiii.hf-l-xiii-motu-proprio-19021125-litteras-ante-annos`.
- PDF SHA-256: `3752d1591454e9b7a70bc1bb550c03c6707f24ba086f8f68ab0417b154a96d42`.
- Physical pages personally inspected: 1. Prior review reused: none.
- Status: **PASS**.
- Observation: Single-page act clear. Closing and signature fit left column; source notice continues from its final two left-column lines into right column, with revision and compact rights colophon, without collision.

### 10. E Supremi

- Work: `papal.pius-x.hf-p-x-enc-04101903-e-supremi`.
- PDF SHA-256: `f1d9a1c76151a8aa2adfa651e3edf95dee0fdc00a10da526af97f5c133826747`.
- Physical pages personally inspected: 1, 2, 3, 4, 5. Prior review reused: none.
- Status: **PASS**.
- Observation: Five pages clear; dense prose and note-call glyphs remain readable. Final blessing/date/signature on p.4; p.5 carries substantial notes 16–49 followed by legible source/revision notice and rights colophon, without overflow.

### 11. Quum, arcano

- Work: `papal.pius-x.hf-p-x-apl-19040211-quum-arcano`.
- PDF SHA-256: `b0340799ac5971be1cadf7a993958d6db09730d8866143d75abde7956ab31090`.
- Physical pages personally inspected: 1, 2. Prior review reused: none.
- Status: **CHANGES_REQUIRED**.
- Observation: Both pages clear typographically; p.2 dating/subscription and apparatus readable. A standalone comma paragraph after Pro-Datarius. and before Source is visibly anomalous and requires source-owner disposition.

### 12. Tribus Circiter

- Work: `papal.pius-x.hf-p-x-enc-05041906-tribus-circiter`.
- PDF SHA-256: `4c08a8aed416e0504c3cb36a4da02858c7c8bbcf64df094672fabbae6194e6da`.
- Physical pages personally inspected: 1, 2, 3. Prior review reused: none.
- Status: **CHANGES_REQUIRED**.
- Observation: All three pages inspected; clear glyphs, columns and source notice. P.3 isolates papal subscription alone before apparatus, separated from p.2 dating clause; closing pagination requires correction.

### 13. Propositum urgentes

- Work: `papal.pius-x.hf-p-x-motu-proprio-19060805-propositum-urgentes`.
- PDF SHA-256: `3600d127c7e20060bfd7b343fe528eab2288985a3c09bf6e68143b683ff2df4f`.
- Physical pages personally inspected: 1. Prior review reused: none.
- Status: **PASS**.
- Observation: One page clear; final word continues into right column before intact dating clause/signature. Source/revision notice and rights colophon are legible and separated.

### 14. Ea semper fuit

- Work: `papal.pius-x.hf-p-x-apl-19070614-ea-semper-fuit`.
- PDF SHA-256: `82d47867f1b227ead1a006cd6d056a9d9676041bfc0ec1bb583d451f58bd4298`.
- Physical pages personally inspected: 1, 2, 3, 4. Prior review reused: none.
- Status: **PASS**.
- Observation: Four pages clear; chapter/article numbering readable and continuation intact. P.4 has substantial final legal formulae, dating clause and cardinal subscriptions before source/revision notice and colophon; no clipping.

### 15. Decessor Noster

- Work: `papal.pius-x.hf-p-x-apl-19091209-decessor-noster`.
- PDF SHA-256: `451aff8a0b22fe19f8f66a6625c314f5d1f362efd36a6e908a5c13442badec70`.
- Physical pages personally inspected: 1. Prior review reused: none.
- Status: **PASS**.
- Observation: Single page clear; dating clause, cardinal subscription and later presentation note remain legible in right column above source/revision notice and colophon.

### 16. Quo uberiores

- Work: `papal.pius-x.hf-p-x-apl-19110408-quo-uberiores`.
- PDF SHA-256: `135a3ebc541a8bd1c8b873d79e69c3ac4e3786c1d5e32d91b0e83c3a82476a66`.
- Physical pages personally inspected: 1. Prior review reused: none.
- Status: **PASS**.
- Observation: Single page clear; dating clause crosses column break in normal order with subscription at top right, followed by legible source/revision notice and colophon.

### 17. Abhinc duos annos

- Work: `papal.pius-x.hf-p-x-motu-proprio-19131023-abhinc-duos-annos`.
- PDF SHA-256: `7db6371ef1329f6a3b8f2a310ca22d9d26ed4c28c16daffbbe8f36bbeb3921ef`.
- Physical pages personally inspected: 1, 2. Prior review reused: none.
- Status: **PASS**.
- Observation: Both pages clear; Roman-numbered provisions and closing readable. P.2 carries substantive remaining provisions plus intact dating clause/signature, source/revision notice and colophon.

### 18. Alloquentes Proxime

- Work: `papal.benedict-xv.hf-ben-xv-motu-proprio-19170325-alloquentes-proxime`.
- PDF SHA-256: `7fc4c183a235873d269b3e7507bdf5a87d1a036310d63ed610f17c56f918fa60`.
- Physical pages personally inspected: 1. Prior review reused: none.
- Status: **PASS**.
- Observation: Single page clear; five provisions, dating clause and signature legible. Source notice continues across column break; revision and colophon fit top right without clipping.

### 19. Nobis supremum

- Work: `papal.benedict-xv.hf-ben-xv-apl-19191119-nobis-supremum`.
- PDF SHA-256: `083d3d78d2e7c6b5afb61ceb6fe2a3a470eff873f8a316e749fa1f15fa6c9d0e`.
- Physical pages personally inspected: 1. Prior review reused: none.
- Status: **PASS**.
- Observation: Single page clear; date and cardinal subscription legible. Source notice continues in right column before revision and rights colophon; no overlap.

### 20. Cum in honorem

- Work: `papal.benedict-xv.hf-ben-xv-apl-19200915-cum-in-honorem`.
- PDF SHA-256: `a2e92c710fb11c28a5826205dcfa01ffd91e6be79361f1bade8ac8b56eeef29b`.
- Physical pages personally inspected: 1, 2. Prior review reused: none.
- Status: **PASS**.
- Observation: Both pages clear; p.2 is sparse but retains eleven lines of substantive final proviso, dating clause and subscription together, then source/revision notice and colophon. No isolated signature or clipping.

### 21. Quae catholico

- Work: `papal.pius-xi.hf-p-xi-apl-19230419-quae-catholico`.
- PDF SHA-256: `6866a6816a9d245d293ebfb9d6c50f5366f17f5abb0c5cc00255ed3fbfff5dad`.
- Physical pages personally inspected: 1. Prior review reused: none.
- Status: **PASS**.
- Observation: One page clear; closing word continues right column before intact dating clause and cardinal subscription. Source/revision notice and colophon remain legible.

### 22. Motu Proprio Orbem catholicum

- Work: `papal.pius-xi.hf-p-xi-motu-proprio-19230629-orbem-catholicum`.
- PDF SHA-256: `059eb0d72931e0dcd80e8be25029e3ca249d9a828c0afb7faa5ee2a2833282b5`.
- Physical pages personally inspected: 1. Prior review reused: none.
- Status: **PASS**.
- Observation: One-page act clear, with long title fitting comfortably. Final proviso, dating clause, signature, source/revision notice and rights colophon all fit in right column above footer.

### 23. Rite Expiatis

- Work: `papal.pius-xi.hf-p-xi-enc-19260430-rite-expiatis`.
- PDF SHA-256: `3f447ebe8446820793993078d1652d989d4206b287dec2373044c0d374e94b6a`.
- Physical pages personally inspected: 1, 2, 3, 4, 5, 6, 7, 8, 9. Prior review reused: none.
- Status: **PASS**.
- Observation: Nine pages clear with continuous readable columns and note calls. Closing blessing/date/signature on p.8; p.9 carries notes 27–35 and readable source/revision notice and colophon. No isolated closing subscription or apparatus-only extra page.

### 24. Monasterii Sanctae Mariae

- Work: `papal.pius-xi.hf-p-xi-apl-19280918-monasterii-sanctae`.
- PDF SHA-256: `72670aad2bbe6d64e6a9bb0651f60cb2124223b479eae03f2689f72d40231c01`.
- Physical pages personally inspected: 1. Prior review reused: none.
- Status: **PASS**.
- Observation: One page clear. Visible title/date agree with signature XVIII Septembris MDCCCCXXVIII. Expanded conflict-of-index/source-identity notice and archive URL wrap within right-column margins; revision and colophon legible.

### 25. Ad animorum bonum

- Work: `papal.pius-xi.hf-p-xi-apl-19290330-ad-animorum`.
- PDF SHA-256: `71853f22d65f6c0dd736bf39baf03e85351d08503cd920140d485afcd8f7108c`.
- Physical pages personally inspected: 1. Prior review reused: none.
- Status: **PASS**.
- Observation: One page clear; accented heading glyph and complete dating clause/cardinal signature readable. Source notice continues across column break; revision and rights colophon fit top right.

## Limits

This is visual review of the frozen, source-approved mechanical reading editions. It is not independent rights adjudication, historical word-level collation, or approval of installation or publication. No new title/date discrepancy was established; the displayed Non maius date matches its visible 1891 closing, and Monasterii Sanctae Mariae visibly preserves its reviewed 1928 date and expanded index-conflict notice. Source-boundary punctuation in Quum, arcano remains a finding for the source owner, rather than permission to silently alter papal wording. No PDF, source artifact, generator, manifest, or publication destination was changed by this review.
