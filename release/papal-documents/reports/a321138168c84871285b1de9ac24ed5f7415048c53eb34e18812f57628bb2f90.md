# Fresh bounded encyclical review — baseline recovery 11

Completed subset: 3/3 PDFs; 9/9 pages. Packet complete.

Scope: independent cold visual review of the exact assigned generated PDFs, using existing repository-helper contacts and native page rasters. Every completed PDF was inspected freshly; no prior checkpoint coverage, reused pages, or reuse proofs are claimed. No rendering, source editing, installation, Git mutation, or delegation was performed.

Pins: verification.json records PDF, receipt, frozen manifest, source payload, source/controller records, segment, body.tex, compact packet pinset, original packet, raster manifest and every cache-listed raster hash; all 42 checks per assigned document passed. PDF page counts were checked using pdfinfo. Receipt fidelity and warnings were read; fonts and metadata were inspected through pdffonts/pdfinfo. Every listed font is embedded with a Unicode map. Receipt-relative body.tex paths were resolved against the receipt directory. Literal LF alone determines source/body line numbers.

## acta.aas.013.archive.aas.013.l013842 — CHANGES_REQUIRED

Title: AD PATRIARCHAS, PRIMATES, ARCHIEPISCOPOS, EPISCOPOS ALIOSQUE LOCORUM ORDINARIOS, PACEM ET COMMUNIONEM CUM APOSTOLICA SEDE HABENTES I DE DCC NATALI SANCTI DOMINICI CELEBRANDO.
PDF SHA-256: `3a86dc554ce7b0eb3691b6bad725ff324b66403ad7819ad2bbdbe2982ae3d471`; language `la`; 3 pages.
Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Fresh contact-sheet pages: 1, 2, 3; native full-size pages: 1, 2, 3.
Contact: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/undated-acta-aas-013-archive-aas-013-l013842-b2029fae-la/undated-acta-aas-013-archive-aas-013-l013842-b2029fae-la/contact-sheets/sheet-001.png`.
Full-size rasters: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/undated-acta-aas-013-archive-aas-013-l013842-b2029fae-la/undated-acta-aas-013-archive-aas-013-l013842-b2029fae-la/pages/page-N.png` for N in the full-size list.

- Page 1: identification and both columns fit; long all-capital title remains readable. Body starts directly after identification. Three historical reference notes are visibly fused at the confirmed right-column locus below the Dominicus paragraph.
- Page 2: left-to-right column flow and justified text stay within margins; split source words and OCR letter spacing remain visible, with no clipping or overlap.
- Page 3: historical conclusion, dating clause and BENEDICTUS subscription precede a compact rule-separated source/rights colophon in the right column. This is a source-bearing final page, not an apparatus-only page.
- The receipt has three underfull-box warnings, concentrated at initial paragraph LF 9–13; fresh full-size inspection shows contained identification and heading text without an overflow.
- Pinned source LF 13842–13846 and body.tex LF 9–13 match the viewed opening; source LF 14093–14098 and body.tex LF 259–265 match the blessing, dating clause and literal OCR subscription `BENEDICTUS PP. XT` at the viewed ending. The literal XT was not silently corrected.
- blocking (pages 1): Historical reference notes are fused to the body paragraph in the right column: rendered `convertisset. 1 Eccli. L, t. 2 Matth. XXVIII, Í9. 3 Marc. XVI, 15.` Source literal-LF 13904 is `nem convertisset.` and LF 13905–13910 carry the three reference notes. Pinned body.tex LF 71–77 retains these lines continuously, without an explicit paragraph boundary before the first note; the first following \par is LF 78. The rendered locus and exact TeX boundary jointly establish fusion, rather than merely a separate historical note interrupting a sentence.

Limits: Historical OCR word divisions, letter-spaced words and anomalous punctuation remain visible; these source-derived characters were not silently corrected or fully collated. No full-volume facsimile collation or independent historical rights adjudication was performed.

## acta.ass.006.ass-006-act-008 — CHANGES_REQUIRED

Title: Nullis certe verbis
PDF SHA-256: `4de22148736e7d1f7b85c9ed945cbb5c24dce79839d28c947db45c9e8ea5961d`; language `la`; 3 pages.
Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Fresh contact-sheet pages: 1, 2, 3; native full-size pages: 1, 2, 3.
Contact: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1860-01-19-acta-ass-006-ass-006-act-008-c1c9bcc5-la/1860-01-19-acta-ass-006-ass-006-act-008-c1c9bcc5-la/contact-sheets/sheet-001.png`.
Full-size rasters: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1860-01-19-acta-ass-006-ass-006-act-008-c1c9bcc5-la/1860-01-19-acta-ass-006-ass-006-act-008-c1c9bcc5-la/pages/page-N.png` for N in the full-size list.

- Page 1: compact title, Pius IX, act date and language are clear. All-capital source protocol, body and columns are contained with no overlap or clipping. Repeated source word fusions and large inter-word gaps disrupt the intended justified classic reading texture.
- Page 2: column flow is physically contained. Long fused OCR tokens are visible in both columns, including the exact source/TeX examples cited in the blocking finding.
- Page 3: real historical prayer, blessing and dating clause end with `Anno Deci- moquarto.` before a source note below the rule. Rights continuation occupies the top of the right column on this same source-bearing page. The page is not project-apparatus-only.
- Receipt fidelity passes for the pinned bytes. Its 41 underfull-box warnings match the broad visible spacing concern; no overflow or glyph collision was observed.
- Pinned source LF 1–5 and body.tex LF 9–13 match the viewed opening; source LF 342–347 and body.tex LF 350–356 match the historical closing/dating clause at the viewed ending.
- blocking (pages 1, 2, 3): Dense OCR word fusion materially impairs reading across all three pages and contributes to conspicuous justification gaps. Confirmed examples visible at full size: page 1 `VenerabilesFratres` and `nostraereligionisiustitiaeque` (source LF 13, 48; body.tex LF 21, 56); page 2 `LitterisprimamsuamEpistolamante` and `Ecclesiaenominerogavimus,utetiam` (source LF 209, 220; body.tex LF 217, 228); page 3 `mantissimanostrumomniumestma-` (source LF 318; body.tex LF 326). These are retained source-byte word fusions, not a claim that the TeX generator invented words or that a separate note interruption is fusion. Mechanical text fidelity does not resolve their visual readability impact.

Limits: No correction, reordering or spacing repair was attempted. The declared source derivative and selected body were checked at cited loci; the historical printing was not fully collated.

## acta.ass.025.ass-025-017 — PASS

Title: Epistola de Collegiis Clericorum in Indiis orientalibus
PDF SHA-256: `8a3757e9c23e751ef86db2fb82cd11589d924f15299ba4206840acfb7e346913`; language `la`; 3 pages.
Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Fresh contact-sheet pages: 1, 2, 3; native full-size pages: 1, 2, 3.
Contact: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1893-06-24-acta-ass-025-ass-025-017-94d3ad68-la/1893-06-24-acta-ass-025-ass-025-017-94d3ad68-la/contact-sheets/sheet-001.png`.
Full-size rasters: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1893-06-24-acta-ass-025-ass-025-017-94d3ad68-la/1893-06-24-acta-ass-025-ass-025-017-94d3ad68-la/pages/page-N.png` for N in the full-size list.

- Page 1: compact title, Leo XIII, date and Latin identification are readable. The retained source heading and incipit lead directly into the text. Columns are readable, with no clipping, overlap or materially disruptive justification gaps.
- Page 2: both dense columns were opened at native page size. Source paragraphs, historical line-division hyphens and left-to-right flow are contained. The continuation into the last page is a divided source word (`bene-` / `volentiae`), preserved without an inserted historical note.
- Page 3: six lines of historical closing/dating/subscription remain at the upper left, followed by a short rule and compact apparatus. The final paragraph and signature are separated; no apparatus-only terminal page is present.
- Pinned source LF 28707–28711 and body.tex LF 9–13 match the viewed source opening. Source LF 28886–28891 and body.tex LF 190–197 match the viewed ending. Receipt fidelity passes, with no layout warnings recorded.
- qualification (pages 3): The final page is sparse but preserves the actual historical conclusion, act dating clause and LEO PP. XIII subscription before compact source/rights apparatus. The conclusion corresponds to source literal-LF 28886–28891 and body.tex LF 190–197. It is source-bearing and qualifies under the stated sparse-final-page rule.

Limits: Literal source OCR word divisions, scattered spacing and punctuation anomalies remain; visual acceptance does not certify the reconstructed wording. No whole-volume facsimile collation, independent rights determination or installation check was performed.

## Review boundary

This review establishes visual acceptance or rejection only for the pinned bytes and actual pages listed. It does not establish word-level or facsimile collation, source completeness outside the declared selection, translation accuracy, a new rights determination, installation identity, or deployment. Source OCR wording remains a disclosed historical derivative; material presentation problems are reported independently of mechanical fidelity.
