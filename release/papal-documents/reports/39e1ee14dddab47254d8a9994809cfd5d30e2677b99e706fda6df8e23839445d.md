# Baseline recovery 06: independent cold PDF review

Coverage: 2/2 PDFs and 15/15 pages completed. This is the final packet report.

Reviewed on feature/encyclicals. Every coverage claim below is a fresh image inspection in this recovery; no checkpoint inspection or raster-review acceptance is inherited. All reused_pages and reuse_proofs are empty.

Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Frozen manifest SHA-256: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.
Raster run manifest SHA-256: `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`.
Render revision: `2026-10-30T02:56:48Z`.

Programmatic verification checked PDF bytes and pdfinfo page counts; exact receipt and frozen-source rows against their hashed sidecars; source, source-controller record/payload, selection and generated body.tex hashes; raster-run identity and every cache-listed contact, thumbnail and page file hash/size. The retained receipt reports source-aware PDF text fidelity PASS for both assigned PDFs; that existing mechanical result is distinguished from this visual review. Verification evidence: `pin-verification.json` in the review scratch directory. No sources, PDFs, shared caches or canonical files were changed.

Image method: existing bounded contact sheets plus the full-size page views listed below. Some full-size views use deterministic full-pixel JPEG95 proxies of the existing PNGs, with 4:4:4 sampling and unchanged dimensions; source and proxy hashes are recorded in `proxy-pins.json`. No PDF was rerendered or rerasterized.

## Studiorum Ducem — historical abridged English translation

`papal.pius-xi.hf-p-xi-enc-19230629-studiorum-ducem` · English · **CHANGES_REQUIRED** · 9 pages.

PDF: `.scratch/encyclical-classic/readers-fixed/1923-06-29-papal-pius-xi-hf-p-xi-enc-19230629-studiorum-ducem-8016f6c5-en/1923-06-29-papal-pius-xi-hf-p-xi-enc-19230629-studiorum-ducem-8016f6c5-en.pdf`
PDF SHA-256: `28e6fdef87c12eb38d48aea40dbb9ac1c156216c210941f5754c952f5ae71130`
Source SHA-256: `7019568db20715af4e9d5a686f1b122af5e466d78744d07e6c6af26b4c9392d8`
Selection manifest SHA-256: `c3c8d81491fc5c18a56cfab7d5618f05824011023cabb24f5dbad61500a66c24`
Generated body.tex SHA-256: `07d781b9f9afffd788bc3a21df125f638dfdd9600c195eb3f4a6e6443eff924e`
Source pinset SHA-256: `4508b3802436e6330eb1cb827d6d8a6d54a9ae2dd848826a29558b9d2943bf6a`

Fresh contact-sheet inspection: pages 1–9 on sheet-001.png. Fresh full-size inspection: all pages 1–9; p1–5 and p9 original PNGs, p6–8 native full-pixel JPEG95 proxies. No reused review coverage.

The restrained title identifies pope, date, language and historical abridgment clearly. Two columns run in normal order; the justified text stays within the page with no observed clipping, overlap or heading collision. Full-size views showed legible type and inline references. pdfinfo identifies a 9-page Letter PDF with the expected title/author and tracked revision instant; pdffonts lists embedded/subset Latin Modern fonts.

Blocking readability finding: p3 right column inserts “Fa” between “Ecu-” and “menical”; p4 right column inserts the standalone strings “PS.”, “SS ee eee”, “Se ee a” between “remote from” and “it”; p5 left column inserts “br aaa” and vertical-bar/punctuation lines between “St.” and “Thomas”. These are visible nonsensical body-sized blocks. Source-backed exclusion or repair needs to dispose of them before this reader is accepted. Exact literal-LF source and generated-TeX evidence is saved in doc-01-locus-evidence.json and doc-01-boundary-evidence.json. Source LF4196–4205 and TeX LF306–312 establish the first locus; source LF4339–4354 and TeX LF441–453 the second; source LF4431–4447 and TeX LF530–543 the third. Explicit \par before and after each block establishes separation, so this finding is OCR-noise/readability, not note fusion.

Other disclosed OCR breaks remain visible throughout, including split words and stray glyphs on p6–8. The surrounding prose remains readable; no claim of corrected wording or full collation is made.

Page 9 is sparse but retains substantial concluding source text, the blessing, the dated Roman subscription and PIUS XI; the compact source/rights colophon follows a short rule. It is not apparatus-only. The first/last source boundaries match the selected ENCYCLICAL OF PIUS XI heading and PIUS XI closing; the colophon discloses the historical translator’s omission of the appended prayer.

## Exeunte Iam Anno

`papal.leo-xiii.hf-l-xiii-enc-25121888-exeunte-iam-anno` · Latin · **PASS** · 6 pages.

PDF: `.scratch/encyclical-classic/readers-fixed/1888-12-25-papal-leo-xiii-hf-l-xiii-enc-25121888-exeunte-iam-anno-5d01d084-la/1888-12-25-papal-leo-xiii-hf-l-xiii-enc-25121888-exeunte-iam-anno-5d01d084-la.pdf`
PDF SHA-256: `9432cf54deb25b60c25059b8f2650b239ddf74409be6dfccf7ec13cf7e22e165`
Source SHA-256: `ac0a432c506421b9cd346ee32f1eb809b7c5d0765c38512e30c747684bf6fce1`
Generated body.tex SHA-256: `193c6482237f65ea1b174b05aed92a315878f4d3277391ab124c1da73b69feec`
Source pinset SHA-256: `744435ed1dd644854c7d28ed4926e6b3e4319b3d1186d61a2cf5374fad1bdddc`

Fresh contact-sheet inspection: pages 1–6 on sheet-001.png. Fresh full-size inspection: all pages 1–6 through native full-pixel JPEG95 proxies. No reused review coverage.

The restrained title and compact identification clearly state Leo XIII, 1888-12-25 and Latin. The EPISTOLA / EXEUNTE IAM ANNO source heading is retained flush left. All six pages are readable, with standard left-column then right-column order, indented paragraphs, justified Latin and contained inline references. Dense p2–5 have no observed clipping, collision, materially stretched source heading, separate-note fusion or conspicuous OCR-noise block. Minor retained web-transcription spacing irregularities are not a claim of corrected wording.

Page 6 is sparse but source-bearing: final body continuation, Augustine citation, apostolic blessing, dated Roman closing and LEO PP. XIII appear before the compact source/rights colophon. The short rule and smaller apparatus are legible; this is not an apparatus-only page. The pinned source starts with EPISTOLA / EXEUNTE IAM ANNO / Sanctissimi D. N. Leonis XIII (literal LF1–7) and ends with the dating clause and LEO PP. XIII (LF29–31); generated body.tex retains the closing at LF51–55 with explicit paragraph boundaries. Boundary snippets are saved in doc-02-boundary-evidence.json.

pdfinfo confirms six Letter pages, the expected title/author/language subject and tracked revision instant. pdffonts lists embedded/subset Latin Modern fonts. This PASS covers layout/readability and the checked opening/closing, while retaining the disclosed uncollated normalized web-transcription limit.

Limits: this is a layout/readability and bounded source-boundary review, not whole-source collation, a new translation assessment, or a new rights determination. Historical OCR spelling and broken words are disclosed and were judged independently from clipping, overlap, separate source-note paragraphs and material noise. A retained note interrupting a word is not called fusion without rendered and exact source/TeX boundary evidence. No installation or publication is authorized by this report.
