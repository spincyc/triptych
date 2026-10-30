# Baseline recovery 12: fresh bounded cold PDF review

Completed subset: 3/3 PDFs, 9/9 pages. This report covers only the documents listed below.

Reviewed on 2026-10-30. Every reported page was freshly inspected in its existing contact sheet and full-size raster. No page inspection or acceptance was inherited from a checkpoint. No raster generation, source correction, installation or publication was performed.

The packet/common brief, complete hashed pinset sidecars, source controller records and available payloads, exact PDF/body TeX/source/segment/receipt/frozen-manifest pins, and all seven raster artifacts per document were checked programmatically. Receipt rows equal their pinsets; frozen source rows equal their pinsets. Raster cache and review-run rows bind the same PDF hashes and page counts. pdfinfo confirms three pages, unencrypted Letter PDFs (612 × 792 points); All listed fonts are embedded subsets with Unicode maps; pdffonts output and metadata are retained in the lane evidence. Receipt fidelity status is pass with no warnings; this is verified receipt evidence, not a newly rerun whole-source collation. Details: verification.json.

Source positions below count literal LF bytes; form feeds are not extra lines. Restricted parent payloads without supplied paths were not inspected or rehashed; their pinned artifact records were hashed. Layout acceptance does not certify OCR wording, translations, historical completeness or rights. No web/facsimile collation or legal reassessment was performed.

## acta.ass.029.ass-029-l08038 (la) — PASS

Title: Fidentem piumque animum
PDF: `.scratch/encyclical-classic/readers-fixed/1896-09-20-acta-ass-029-ass-029-l08038-3f3ff98b-la/1896-09-20-acta-ass-029-ass-029-l08038-3f3ff98b-la.pdf`
SHA-256: `69311cc7109f09f16995c9cbc115fe148c7975cb4a07e47b468a0f7c7584139c`; pages: 3.
Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Fresh individually inspected pages: [1, 2, 3]; full-size views: [1, 2, 3]. Reused pages: none.

The compact title identifies Leo XIII, date and Latin. Both columns follow ordinary left-column then right-column order, with clear gutter, consistent baselines and contained justified text. The all-capital source identification and historical subscription remain visible.
All three pages were viewed in contact sheet sheet-001.png and opened at full size because each contains retained notes. Notes visibly start as separate indented paragraphs. The last page retains substantial historical body text, dating clause, LEO PP. XIII. and final Acts note; the compact smaller project colophon follows a rule on that same page. No apparatus-only page or problematic heading split was found.

- qualification, page(s) [1, 2, 3]: Retained OCR includes intraword spaces, divided-word spacing and a damaged citation label (page 2: “De (tssumpt”). Glyphs and separate note blocks remain legible; no material layout unreadability, clipping or overlap observed.

Boundary/source evidence:
- Source LF 8113–8116, 8156–8159, 8199–8202, 8244 and 8285 are the five retained note blocks. In body.tex these are lines 90–93, 134–137, 178–181, 224 and 265, delimited respectively by explicit \par at 88/94, 132/138, 176/182, 222/225 and 263/266.
- Rendered page 1 ends with the Matthew/Apologeticum note; page 2 contains the Litt. apost. note and De (tssumpt)/Hebrews/Colossians/Romans note; page 3 has Sap. XV and Acts notes. Interruptions after “placuit”, “inde simul”, “pretium” and “de qua” match the separate source-order paragraphs, not fused body/note text.
- The source ending at LF 8278–8279 (Datum…anno…1896), LF 8281 (LEO PP. XIII.) and LF 8285 (Acts note) matches body.tex 258–266 and the final rendered column.

Limitations: Cold review of these exact three rendered pages and bounded source/TeX loci only; no full-work textual or facsimile collation. Two restricted ancestor payloads have no supplied local payload path; their exact artifact records were checked.

## acta.ass.039.ass-039-l004849 (la) — CHANGES_REQUIRED

Title: LITTERAE ENCYCLICAE S S . D. N. Pii d. pr. PP. X, quibus consociatio " Mariavitarum „ seu sacerdotum mysticorum reprobatur ac supprimitur.
PDF: `.scratch/encyclical-classic/readers-fixed/1906-04-05-acta-ass-039-ass-039-l004849-795c5f58-la/1906-04-05-acta-ass-039-ass-039-l004849-795c5f58-la.pdf`
SHA-256: `80a4e7b0d642093ddf5c22666adfdd05482918b913386d301669d7e985ea81a9`; pages: 3.
Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Fresh individually inspected pages: [1, 2, 3]; full-size views: [1, 2, 3]. Reused pages: none.

All three pages were freshly inspected in sheet-001.png and at full size. The long source-derived title wraps safely across three lines and identifies Pius X, date and Latin. The all-capital address stays with the opening. Two-column body text is contained and legible, with no clipping or overlap observed.
Page 2 has one confirmed fused note and one genuinely separate note. The latter interrupts the divided word Mariavitarum, but is a separate visible paragraph with explicit TeX boundaries and is not itself a fusion failure. Page 3 retains the ending and signature, followed by the smaller project apparatus under a rule.

- blocking, page(s) [2]: Left column: historical Ezechiel/Die20 note runs directly into the quotation after “clare nobis patuit,” with no paragraph boundary before it. Exact pinned source LF4953–4955 and body.tex119–121 confirm fusion; body.tex has only the trailing \par at122. A separate note paragraph is required before acceptance.
- minor, page(s) [2]: Historical running-page marker “l32” is retained as its own visible paragraph after the fused note (source LF4957; body.tex124), contrary to the terminal apparatus statement that running heads are omitted.
- qualification, page(s) [3]: Final page is sparse with empty right column, but retains substantial concluding historical body, the dated subscription and PIUS PP. X before the compact colophon; it is source-bearing.

Boundary/source evidence:
- Rendered page2 left: after “clare nobis patuit,” the note begins inline as “(1) Ezechiel, xni, 6, 7. (2) Die 20 Febr. an. curr.”. Pinned body.tex119 is the body line,120–121 are notes,122 is \par; no \par precedes120. Literal source LF4953 is body and4954–4955 are the adjacent notes with no blank LF between.
- Rendered page2 right: note “(1) Cfr. Acta S. Sedis, vol.21, pag.321.” between Ma- and riavitarum. Source LF5028 is “quo Ma-”,5029–5030 blank,5031 note,5032 form-feed running head omitted by segment,5033–5034 blank,5035 resumes “riavitarum”. Body.tex194 ends Ma-,195 \par,197 note,198 \par,200 resumes riavitarum. This separate block is acceptable under the clarified note criterion.
- Final source LF5059–5060 (Datum…5 April1906…third pontifical year) and5062 (PIUS PP.X) match body.tex224–229 and rendered page3.

Limitations: Cold visual review and bounded source/TeX checks only; no whole-work textual or facsimile collation. Two restricted ancestor payloads lack supplied local paths; their pinned artifact records were checked. The identified fusion blocks acceptance of these PDF bytes; repair and fresh byte-bound review belong to the coordinator.

## papal.leo-xiii.hf-l-xiii-enc-03031891-in-ipso (la) — PASS

Title: In Ipso
PDF: `.scratch/encyclical-classic/readers-fixed/1891-03-03-papal-leo-xiii-hf-l-xiii-enc-03031891-in-ipso-baf35a16-la/1891-03-03-papal-leo-xiii-hf-l-xiii-enc-03031891-in-ipso-baf35a16-la.pdf`
SHA-256: `00d9ac45cb865455ae47c5597564b689dd3d1fcaa6d0c3d2820e3531f653ea1d`; pages: 3.
Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Fresh individually inspected pages: [1, 2, 3]; full-size views: [1, 2, 3]. Reused pages: none.

All three pages were freshly viewed in sheet-001.png and at full size. Compact identification names Leo XIII, date and Latin; the historical EPISTOLA / IN IPSO heading and recipient description precede the source body. Two-column reading order, gutter, justification, margins and baselines are consistent, with no clipping, overlap, dangling heading or observed material unreadability.
The unnumbered historical paragraphs and final subscription are preserved. No historical note blocks appear in these three rendered pages or the bounded source/body checks. The final page has a short continuation paragraph, blessing, date and signature, then a ruled, smaller terminal source/rights colophon.

- qualification, page(s) [3]: Sparse final page with empty right column retains the conclusion, Apostolic blessing, dating clause and LEO PP.XIII before the colophon. It is source-bearing and acceptable under the sparse-page criterion.
- qualification, page(s) [1, 2]: A few retained transcription intraword spaces remain visible (for example t am and ad u n um). Body remains readable; this review does not certify the transcription wording.

Boundary/source evidence:
- Opening source literal LF1–7 has EPISTOLA, IN IPSO, Sanctissimi D.N.LeonisXIII and the recipient description; body.tex9 onward retains these, including separate ragged-right all-capital headings. Rendered page1 shows this same order.
- Source LF17 is the concluding Haec igitur paragraph, LF19 the Interim blessing, LF21 the Datum dating clause, and LF23 LEO PP.XIII. Body.tex33/34,36/37,39/40 and42/43 retain the corresponding text and explicit paragraph endings. Rendered page3 shows the ending before project apparatus.

Limitations: Bounded visual and opening/ending source/TeX review only; no whole-work textual, historical-image or facsimile collation. One restricted HTML ancestor has no supplied local payload path; its exact artifact record was checked.
