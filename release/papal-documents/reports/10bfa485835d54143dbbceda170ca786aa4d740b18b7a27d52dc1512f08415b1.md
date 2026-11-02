# Independent baseline continuation review 03

Packet: `.scratch/encyclical-ready-package/baseline-review-packets/03.json`.
Canonical report destination: `src/sources/papal-documents/encyclicals-baseline-continuation-03.md`.
Review date: 2026-10-30. Scope: 7 exact baseline PDFs, 39 pages.

Outcome: **4 PASS (29 pages), 3 CHANGES_REQUIRED (10 pages)**. All 39 pages were freshly inspected both on the existing contact sheets and as original-size full-page rasters. No prior review inspection was inherited and no pages were reused.

The three blocking readers have pervasive OCR word-boundary damage. Auspicato concessum additionally runs a historical citation into a body paragraph. These usability failures remain blocking even though every PDF passes the independent complete-body source-fidelity check.

## Identity and verification

All packet PDF hashes and actual `pdfinfo` page counts match. The exact receipt hash, frozen-manifest hash, source payload hash, segment hash where present, source-controller record hashes and retained controller payload hashes match. Receipt rows and frozen source rows match the packet exactly; segment identities, input hashes and physical LF ranges match. The pinned raster-run manifest matches; each document cache identifies the exact PDF/page count, and every listed page, thumbnail and contact-sheet file matches its cache hash and size. The common brief hash also matches.

Receipt for all seven: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Frozen manifest: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.
Raster-run manifest: `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`.
Render revision: `2026-10-30T02:56:48Z`.

Read-only `pdfinfo`, `pdffonts` and raw text extraction succeeded for each PDF. The metadata identifies the corresponding title, issuer and text language, with US Letter pages; all listed fonts are embedded. The repository's `pdf_body_fidelity` function was independently rerun against the exact selected local source text, using LF-based segment ranges where required and `PYTHONDONTWRITEBYTECODE=1`. All seven pass `pdf-raw-source-aware-line-hyphen-nfkc-v3`, with the source beginning on page 1 and ending on the actual final page. Raw-source character counts can differ from the frozen normalized block text's count because selected LF joins preserve different whitespace; normalized whole-body equality and source-bearing page extent pass.

Local verification evidence is in the assigned scratch directory: `pin-results.json`, `fidelity-results.json`, `0`–`6` source/PDF boundary extracts, PDF metadata and font listings. These are review aids, not additional historical witnesses.

## Actual page coverage and findings

All contact images used `contact-sheets/sheet-001.png` under the exact packet `raster_dir`. Every numbered full-size page image under each `raster_dir/pages/` was opened at original size: `page-01.png`–`page-16.png` for Divini illius Magistri and `page-1.png` through the final numbered page for the other six. This includes every first, final, note-bearing, dense, sparse and suspicious page.

### 1. Divini illius Magistri — PASS

ID: `papal.pius-xi.hf-p-xi-enc-31121929-divini-illius-magistri`; language `en`; 16 pages.

PDF SHA-256: `0df2f8c73d3af10f3ca271355f436dc16b16005898c410466bdee5e8eb2266ba`.
Source SHA-256: `8d44b2c03213449a25f5e4af3b4b5daed51dffb24ee9bf9f1dd63b3e61f8cafa`.

PDF: `.scratch/encyclical-classic/readers-fixed/1929-12-31-papal-pius-xi-hf-p-xi-enc-31121929-divini-illius-magistri-a6878805-en/1929-12-31-papal-pius-xi-hf-p-xi-enc-31121929-divini-illius-magistri-a6878805-en.pdf`.
Rasters: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1929-12-31-papal-pius-xi-hf-p-xi-enc-31121929-divini-illius-magistri-a6878805-en/1929-12-31-papal-pius-xi-hf-p-xi-enc-31121929-divini-illius-magistri-a6878805-en`.

Fresh contact-sheet inspection: pages 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16. Fresh original-size inspection: pages 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16.

- **qualification**, pages 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16: Readable retained OCR with damaged words, internal source hyphenation and note markers. Page 1 retains Hts Hottness Pore and the missing drop-cap in EPRESENTATIVE; page 2 retains the damaged section heading. Notes remain separate paragraph blocks in original source-page order, sometimes interrupting a sentence; their corrupted original markers are not a reliable corrected reference system. No note is run into a body paragraph in the inspected rendering.
- **qualification**, pages 16: Source-bearing final page retains the closing exhortation, blessing, dated Pius PP. XI subscription and terminal historical references before the compact source/rights apparatus. The unused right column is acceptable.

### 2. Cum illud — PASS

ID: `acta.aas.009.ii.archive.aas.009.ii.l025727`; language `la`; 6 pages.

PDF SHA-256: `1da6d62ad7caf3ec2eeca597eb8248146e931b131230248d0849b1e1f747cdf7`.
Source SHA-256: `3e09a2381a05e7b67a5a8115e58fea16beff9131bf15275387ebb526184f81a8`.

PDF: `.scratch/encyclical-classic/readers-fixed/1742-12-14-acta-aas-009-ii-archive-aas-009-ii-l025727-96567a7c-la/1742-12-14-acta-aas-009-ii-archive-aas-009-ii-l025727-96567a7c-la.pdf`.
Rasters: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1742-12-14-acta-aas-009-ii-archive-aas-009-ii-l025727-96567a7c-la/1742-12-14-acta-aas-009-ii-archive-aas-009-ii-l025727-96567a7c-la`.

Fresh contact-sheet inspection: pages 1, 2, 3, 4, 5, 6. Fresh original-size inspection: pages 1, 2, 3, 4, 5, 6.

- **qualification**, pages 1, 2, 3, 4, 5, 6: Historical OCR includes occasional anomalous glyphs and retained internal hyphenation, but continuous prose and paragraph/section order remain readable. The quoted 1721 curial letter and signatures on page 3 remain within the selected source context; they are not newly inferred document boundaries.
- **qualification**, pages 6: The full final dating clause through Pontificatus Nostri anno tertio is present, followed on the same source-bearing page by compact source/rights apparatus.

### 3. Auspicato concessum — CHANGES_REQUIRED

ID: `acta.ass.015.ass-015-act-004`; language `la`; 5 pages.

PDF SHA-256: `2622003bf3779fb4350c18e27c17a0d00e36946cce7573a02c916f82db87087f`.
Source SHA-256: `ce7f8fbb6a92dd17066c6343b60deb8936d228c487e61c1eabf3b660327dd3ab`.

PDF: `.scratch/encyclical-classic/readers-fixed/1882-09-17-acta-ass-015-ass-015-act-004-9fbe6ed8-la/1882-09-17-acta-ass-015-ass-015-act-004-9fbe6ed8-la.pdf`.
Rasters: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1882-09-17-acta-ass-015-ass-015-act-004-9fbe6ed8-la/1882-09-17-acta-ass-015-ass-015-act-004-9fbe6ed8-la`.

Fresh contact-sheet inspection: pages 1, 2, 3, 4, 5. Fresh original-size inspection: pages 1, 2, 3, 4, 5.

- **blocking**, pages 1, 2, 3, 4, 5: Pervasive OCR whitespace destroys word boundaries: long letter-spaced runs mix with missing spaces between words. This materially impairs continuous reading at full size, rather than constituting occasional historical spelling damage. Page 1 mixes long spaced-letter sequences with joined multiword streams; the same pervasive pattern continues on page 4. Faithful reproduction of these bytes does not satisfy reading usability.
- **blocking**, pages 2: The historical citation fi) Act. I V , 12. is fused into a body paragraph: the left-column prose ending Atqui istud plane nsuveniebat sub runs directly into the citation before the paragraph break. The corresponding selected-source line 86 and generated body.tex line 96 confirm that this note has no separate paragraph block. Restore a source-grounded note/body partition before approval.
- **qualification**, pages 5: The benediction, Datum Romae dating clause and LEO PP. XIII ending survive on the final page; the failure concerns readability and note separation, not an observed lost ending or apparatus-only page.

### 4. Adiutricem populi christiani — PASS

ID: `acta.ass.028.ass-028-l05003`; language `la`; 4 pages.

PDF SHA-256: `0196f0f15cffeb576e48dbd1eacc660efafa99955fb96d80c6d056f302069e00`.
Source SHA-256: `9d724e374e7e18e9100778a8714c07cb4f9124039cbd3718543d2d907f25aac4`.

PDF: `.scratch/encyclical-classic/readers-fixed/1895-09-05-acta-ass-028-ass-028-l05003-7d922a59-la/1895-09-05-acta-ass-028-ass-028-l05003-7d922a59-la.pdf`.
Rasters: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1895-09-05-acta-ass-028-ass-028-l05003-7d922a59-la/1895-09-05-acta-ass-028-ass-028-l05003-7d922a59-la`.

Fresh contact-sheet inspection: pages 1, 2, 3, 4. Fresh original-size inspection: pages 1, 2, 3, 4.

- **qualification**, pages 1, 2, 3, 4: Retained OCR has scattered spaced words, broken hyphenation and damaged citation glyphs (including Greek-looking words in notes). These are local source limitations; the Latin prose and distinct note paragraphs remain readable. Notes occur in original source-page sequence, occasionally between parts of a continuing sentence, and remain in separate blocks.
- **qualification**, pages 4: Final blessing, September 5 dating and LEO PP. XIII subscription precede the terminal apparatus; the final page is source-bearing.

### 5. Epistola ad Ordinarios Imperii austriaci — CHANGES_REQUIRED

ID: `acta.ass.023.ass-023-011`; language `la`; 3 pages.

PDF SHA-256: `0e01598aa24f19613cd7f7f1a8c4466fbe3f3f95abe29a7d896cd2725660697b`.
Source SHA-256: `2ed2fb06999a29e2791c1f8f58acf69590b4a12449217d5b6b3debfb7dd2355b`.

PDF: `.scratch/encyclical-classic/readers-fixed/1891-03-03-acta-ass-023-ass-023-011-627ed544-la/1891-03-03-acta-ass-023-ass-023-011-627ed544-la.pdf`.
Rasters: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1891-03-03-acta-ass-023-ass-023-011-627ed544-la/1891-03-03-acta-ass-023-ass-023-011-627ed544-la`.

Fresh contact-sheet inspection: pages 1, 2, 3. Fresh original-size inspection: pages 1, 2, 3.

- **blocking**, pages 1, 2, 3: Most running prose is rendered as mixtures of separated letters and joined words, with spaces no longer indicating lexical boundaries. Page 1 In ipso supremi Pontificatus and page 2 the long opening continuation demonstrate the pervasive pattern; page 3 remains affected through the closing. This is a material reading-usability failure at full size despite source fidelity.
- **qualification**, pages 3: The final benediction, March 3 dating and LEO PP. XIII subscription are retained before the source/rights apparatus. No ending loss or blank/apparatus-only terminal page was observed.

### 6. Paterna Caritas — PASS

ID: `papal.leo-xiii.hf-l-xiii-enc-25071888-paterna-caritas`; language `la`; 3 pages.

PDF SHA-256: `76ec96e41d2c073610f23738ba76bc4f87d503af84ddb39b4037a369af441409`.
Source SHA-256: `231d82f6f5b57b9222450fa42ef73fd60ccbd48b657f2c1da838d7777754d628`.

PDF: `.scratch/encyclical-classic/readers-fixed/1888-07-25-papal-leo-xiii-hf-l-xiii-enc-25071888-paterna-caritas-6232edc0-la/1888-07-25-papal-leo-xiii-hf-l-xiii-enc-25071888-paterna-caritas-6232edc0-la.pdf`.
Rasters: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1888-07-25-papal-leo-xiii-hf-l-xiii-enc-25071888-paterna-caritas-6232edc0-la/1888-07-25-papal-leo-xiii-hf-l-xiii-enc-25071888-paterna-caritas-6232edc0-la`.

Fresh contact-sheet inspection: pages 1, 2, 3. Fresh original-size inspection: pages 1, 2, 3.

- **qualification**, pages 1, 2, 3: Clear normal two-column Latin reading order, legible justified lines and compact identification. Occasional inherited transcription spellings remain source limitations; no material clipping, overlap, note fusion or unusable word spacing was found.
- **qualification**, pages 3: The unused right column accompanies substantial genuine concluding source paragraphs, the full July 25 dating and LEO PP. XIII subscription, then compact source/rights apparatus. This is a source-bearing final page, not an apparatus-only page.

### 7. LITTERAE SSmi. D. N. Leonis Xlii ad Emum. Gibbons Archiepiscopum Baltimorae aliosque Ordinarios foederatarum Americae Civitatum, ut eisdem significaret quanta affectus fuerit laetitia ex litteris ab eisdem sibi conscriptis. — CHANGES_REQUIRED

ID: `acta.ass.034.ass-034-l025156`; language `la`; 2 pages.

PDF SHA-256: `b209cb80acef27024ea7cf099fca379bc8a64801b5b5d3b271de6d14573db359`.
Source SHA-256: `817d63a71b9ee1a6f3ef8155b871fe5105eb668c6c521c3ab73eafa21f240749`.

PDF: `.scratch/encyclical-classic/readers-fixed/1902-04-15-acta-ass-034-ass-034-l025156-d6553788-la/1902-04-15-acta-ass-034-ass-034-l025156-d6553788-la.pdf`.
Rasters: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1902-04-15-acta-ass-034-ass-034-l025156-d6553788-la/1902-04-15-acta-ass-034-ass-034-l025156-d6553788-la`.

Fresh contact-sheet inspection: pages 1, 2. Fresh original-size inspection: pages 1, 2.

- **blocking**, pages 1, 2: Extensive letter-spaced OCR streams combine adjacent words while splitting their letters; both pages require reconstruction of word boundaries to read ordinary prose. Page 1 beginning In amplissimo Pontificum Romanorum and page 2 rectam puerorum institutionem are representative. The defect persists at full size and blocks acceptance even though all source characters are retained.
- **qualification**, pages 2: April 15 dating and LEO P. XIII subscription remain before the terminal source apparatus. The apparatus continues from the left-column foot to the top of the right column; it does not create a separate apparatus-only page.

## Shared observations and limits

The classic roman type, two-column direction, compact identification and final rights colophons are coherent. No clipped text, overlapping columns, detached title-only page, apparatus-only page, blank page or visually lost selected ending was observed. Page and column breaks sometimes divide source sentences and source hyphenated words; this alone is not a failure. The three word-boundary failures are distinct from those ordinary breaks.

PASS is bounded visual usability of the exact reviewed source edition, not word-level correction, original-print collation, translation validation or independent rights clearance. This review compares opening/closing boundaries with the selected retained text, not facsimiles of the historical printings; an error or omission already in a selected source is outside that comparison. No claim of whole-source textual collation, historical pagination verification or reliable reconstruction of damaged note markers is made. The input receipt's historical evidence claims were not inherited as this reviewer's own inspection.

The failed readers require a separately recorded, source-grounded derivative or partition that repairs their demonstrated defects, followed by fresh hash-bound review. This review did not edit sources, PDFs, receipts, shared rasters, caches, installed output or canonical records. Only the assigned scratch directory was written; no rendering, rerastering, installation, Git mutation or delegation occurred.
