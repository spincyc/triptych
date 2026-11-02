# Independent baseline continuation review 12

Outcome: **4 PASS (29 pages); 2 CHANGES_REQUIRED (5 pages)**. All six assigned PDFs and all 34 pages were freshly inspected. Augustissimae contains historical notes fused into body text. Exultavit remains blocked for materially garbled OCR; its initial note-fusion finding has been withdrawn after a bounded factual reconsideration. No review pages were inherited from prior checkpoints.

## Scope and method

Active branch: `feature/encyclicals`. Packet: `.scratch/encyclical-ready-package/baseline-review-packets/12.json` (SHA256 `be9935f6c78dab6c54d1af05a9e99bf11ca2d7840df741ff42643cc8c51e6420`). Common brief SHA256: `ba9dcb643e6a8110382ac1080ff8f70d51b3ebca892d2efca45bd91bec0f6913` (matched). The exact existing packet `raster_dir` was used for every reader; no PDF, raster, cache, source, canonical report, or Git data was changed.

Every existing `contact-sheets/sheet-001.png` was opened and all assigned pages were visually inspected there. Fourteen full-resolution rasters were additionally opened at their original 1700 × 2200 size: first/final pages of every PDF, Ubi Arcano page 10, and Augustissimae page 2. Actual full-resolution coverage is listed below. No raster reuse is claimed.

All six PDF SHA256 values, `pdfinfo` page counts, exact receipt rows, source payload hashes, available segment-manifest hashes, frozen-manifest hashes, source-controller record hashes and retained payload hashes, raster-manifest hashes, and all cached raster-file hashes matched the packet. Receipt SHA256 for all six readers: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`. Frozen manifest SHA256: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.

`pdfinfo`, `pdffonts`, and `pdftotext -layout` parsed every PDF successfully. All listed fonts are embedded/subset with Unicode maps; all are Latin Modern. PDF metadata titles and authors identify the assigned documents, and modification times correspond to the pinned render revision `2026-10-30T02:56:48Z`. The PDFs are untagged. Source beginnings and endings were read against the exact retained text; disjoint selections used literal LF line ranges, not generic Unicode line splitting. The receipt fidelity PASS states were verified as receipt data, not promoted to an independent full-text collation.

## Byte-bound coverage

| Document | Pages freshly inspected on contact sheet | Full-resolution pages | Status | PDF SHA256 |
| --- | --- | --- | --- | --- |
| Ubi Arcano Dei Consilio (`papal.pius-xi.hf-p-xi-enc-19221223-ubi-arcano-dei-consilio`) | 1–11 | 1, 10, 11 | PASS | `de9998bf86c4b7d86e37eff67f9b39a4cec051cd129a4b0b739c18cdeb4ab9c8` |
| Officio Sanctissimo (`papal.leo-xiii.hf-l-xiii-enc-22121887-officio-sanctissimo`) | 1–7 | 1, 7 | PASS | `f4e6344e2481742ccc112321df85c4003336801715d32dccb07533aa785228f2` |
| Mirae Caritatis (`papal.leo-xiii.hf-l-xiii-enc-28051902-mirae-caritatis`) | 1–6 | 1, 6 | PASS | `631fd0a1deaa781d4df2fac5b8e4211f2fd20b26c6caaeeb420b686f3cccc6a2` |
| Vehementer Nos (`papal.pius-x.hf-p-x-enc-11021906-vehementer-nos`) | 1–5 | 1, 5 | PASS | `ca8a7b527d45169fbcf2bf37516e70848ee235aa7e5fb5ba9bfd4bf8b83a07fa` |
| Augustissimae Virginis Mariae (`acta.ass.030.ass-030-l05020`) | 1–3 | 1, 2, 3 | CHANGES_REQUIRED | `9dba055833715cfa5012a3eeda528e79228460c1ceb44e883d4e626d5b878182` |
| Exultavit cor Nostrum — de fructibus iubilaei (`pius-ix-acta.volume-01.line-00012382`) | 1–2 | 1, 2 | CHANGES_REQUIRED | `023e6f08a35b31610a398d101332a9ec8fa409166f1fdef375c28f8af83e78ee` |

## Findings

### Ubi Arcano Dei Consilio — PASS

Pages 1–11 were inspected freshly on the contact sheet; pages 1, 10 and 11 were opened full size. Compact identification precedes the source protocol. The dense two-column body has clear gutters and margins, regular justified line spacing and no visible clipping, overlap, stranded headings, or disruptive widow/orphan behavior. Page 10 retains the dating clause, `PIUS PP. XI.`, and source notes (1)–(40). Page 11 continues the historical notes (41)–(59), ending `(59) Luc. II, 14`, before compact source/rights apparatus. Its empty right column is a source-bearing final-page qualification, not an apparatus-only page. Notes remain individually distinguishable and readable.

### Officio Sanctissimo — PASS

Pages 1–7 were inspected freshly on the contact sheet; pages 1 and 7 were opened full size. Identification, source address, body paragraphs and inline citations remain legible within clear two-column geometry. No visible clipping, overlap, isolated heading, or apparatus-only page was found. The final page retains the blessing, the 22 December 1887 dating clause, and `LEO PP. XIII` above the compact colophon, matching the selected source ending.

### Mirae Caritatis — PASS

Pages 1–6 were inspected freshly on the contact sheet; pages 1 and 6 were opened full size. The source headings begin cleanly after identification; ordinary Latin text is consistently set and the columns remain separated. No visible geometry defect or disruptive page break was found. The final page retains the closing blessing, the 28 May 1902 dating clause, and `LEO PP. XIII` before terminal apparatus, matching the selected source ending. The shorter right column remains substantially source-bearing.

### Vehementer Nos — PASS

Pages 1–5 were inspected freshly on the contact sheet; pages 1 and 5 were opened full size, including the crowded first-page protocol. Its long capitalized address remains within the column and readable. Body and inline citations are legible; no clipping, overlap or disruptive heading/page break was found. The final page retains the 11 February 1906 dating clause and `PIUS PP. X` above the source/rights block, matching the selected source ending.

### Augustissimae Virginis Mariae — CHANGES_REQUIRED

All three pages were inspected on the contact sheet and opened full size. Geometric margins, glyph visibility and the final dating/signature are intact, but historical notes are fused into body sentences on every page:

- Page 1 right: `legibus confirmatae, suis distinctae` is interrupted by `(1) Eccli. XXIV. 23. (2) Ps. II. 2. (3) Apolog. c. XXXIX.` before the body resumes `signis, privilegiis donatae`.
- Page 2 left: numbered citation notes interrupt the sentence beginning `militiae precantis, a ... Dominico Patre`. Page 2 right places `(1) De orat. domin. (2) Conc. Trid. sess. xxv.` inside the surrounding body/quotation sequence.
- Page 3 left: `(1) S. Th. 2a. 2ae ? q. LXXXIII, a. iv. (2) Ib.` interrupts the body after `reversurum`. Page 3 right inserts the numbered historical notes between `nunquam conticescant; et` and `per varias terrarum orbis regiones`.

These are substantive reading-order defects, not merely uncorrected spellings. The historical notes need separate visible blocks in an evidence-bound derivative, with all source words and sequence retained. Pervasive literal internal spacing (such as `q u a n t u m`) and midword hyphens also burden reading; the glyphs themselves are legible. The selected source ends with the blessing, the September 1897 dating clause and `LEO P P . XIII.`, all visible on page 3. No lost selected-source ending or apparatus-only page was found. That does not cure the note fusion.

### Exultavit cor Nostrum — de fructibus iubilaei — CHANGES_REQUIRED

Both pages were inspected on the contact sheet and opened full size. In a bounded factual reconsideration, page 2 was reopened at full resolution and the exact generated body fragment was checked. Lines 143 and 146 of the pinned batch body TeX contain explicit `\par` boundaries around line 145, `(1) Matth. 7, 8.`. Page 2 visibly places that note on its own line between body passages ending `quemque Ecclesiae suae pe-` and resuming `trem constituit`. This is a separately partitioned historical note retained at a source-page interruption, not same-paragraph fusion. The initial note-fusion finding is withdrawn; no note-layout repair is required on that evidence. The unchanged PDF and receipt hashes were reverified. The initial report and review JSON are retained byte-for-byte as `report.superseded-initial.md` and `reviews.superseded-initial.json` in this lane's scratch directory.

The independent source-OCR finding remains: the OCR materially garbles continuous prose, beyond a few unfamiliar historical spellings. Examples visible in the exact PDF and retained payload include page 1 incipit `E.uwit cor Nostrum`; page 1 right `24que hane Ápostolicam Sedem bel- Inm;teterriteumocontra`; and page 2 left `Hhaqne ... Unbe Mostra pwbdicas preces`, `Ibawibulum`, `8t`, and `offeran&`. Clear glyph rendering does not make those passages reliably readable. The uncorrected-OCR disclosure is accurate but does not resolve the meaningful readability defect. An evidenced source repair and a new byte-bound review are required; otherwise retain a held state. No conjectural corrections are proposed here.

No clipping or overlap was seen. The final right column retains the blessing and the 21 November 1851 dating clause ending `Pontificatus Nostri Ànno Sexto.`, as in the exact selected source; it is followed by compact project apparatus. No selected-source ending loss or apparatus-only final page was found.

## Limits

This is a fresh visual/layout review of the exact packet bytes, with hash and boundary checks. It does not certify historical wording, rights, translation accuracy, original printing pagination, or completeness beyond the selected retained payload. No native facsimile was consulted and no whole-source word-by-word collation was performed. Ordinary middle pages of the four web transcriptions were inspected at contact-sheet scale; their full-resolution views are limited to the pages listed in the table. All pages with separate historical notes in this packet, including all pages of the two oldest OCR readers, were opened full size. No installed-mirror comparison, build-log review, rerender, reraster, installation or canonical mutation was performed. The blocked exact hashes require repair/supersession before installation; these results do not approve later bytes.
