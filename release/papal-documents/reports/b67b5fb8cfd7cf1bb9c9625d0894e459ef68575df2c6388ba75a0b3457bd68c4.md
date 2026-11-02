# Baseline continuation 14 — cold visual review

Disposition: 6 PASS documents (26 pages); 2 CHANGES_REQUIRED documents (13 pages). All 8 assigned PDFs and all 39 pages were freshly inspected in their existing contact sheets. Thirty-one pages were additionally opened at the helper’s full-page resolution. Every first/final page and every identified sparse, suspicious or historical-note-bearing page received a full-size view.

Packet: `.scratch/encyclical-ready-package/baseline-review-packets/14.json`; SHA256 `6e8c50d45d1792d44a3a60f315a68d41e90a395ab67ab2a3a72fc4d08a559c3b`. Canonical report target: `src/sources/papal-documents/encyclicals-baseline-continuation-14.md`. Common brief SHA256 `ba9dcb643e6a8110382ac1080ff8f70d51b3ebca892d2efca45bd91bec0f6913`.

Identity checks: 205/205 passed. Checked exact PDF/source/receipt/frozen-manifest/segment/controller/raster-manifest hashes where supplied; complete receipt-row equality; complete frozen source-row equality; independent PDF page counts; raster-cache PDF/page identity; and every pinned contact/page/thumbnail file hash. Prior checkpoint references were hashed for identity only; no inspection or acceptance was inherited. Evidence: `.scratch/encyclical-baseline-continuation-14/identity-check.json`, SHA256 `013d88e4279963adf9e5e280434a3f2d5545446dcda920d16dd26c1c57c2b0a6`.

The packet’s existing raster directories were used as supplied. No PDF was rerendered or rasterized; no shared cache, source, manifest, release, installed PDF or Git state was changed. Source bounds were interpreted as LF-delimited physical lines, including retained form-feed characters. The actual selected starts and endings were compared with the first/final page views and extracted PDF text; no source-ending loss was observed.

The classic two-column flow, compact identification, justified body text, headings, margins, column gutters, page numbers, notes and terminal colophon were checked. No clipping, overlap, unusable line spacing or apparatus-only final page was found. Both-sided historical-note paragraphs can interrupt a sentence or word and remain acceptable; only a genuinely missing paragraph boundary is called a fusion below.

| Document | Pages | Full-size pages | Disposition |
| --- | ---: | --- | --- |
| acta.ass.020.ass-020-014 (la) | 10 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | CHANGES_REQUIRED |
| papal.pius-xi.hf-p-xi-enc-11121925-quas-primas (la) | 8 | 1, 7, 8 | PASS |
| papal.pius-x.hf-p-x-enc-04101903-e-supremi.acqr-1904-english (en) | 6 | 1, 2, 3, 4, 5, 6 | PASS |
| papal.pius-xi.hf-p-xi-enc-19280106-mortalium-animos (la) | 5 | 1, 5 | PASS |
| acta.ass.006.ass-006-act-011 (la) | 3 | 1, 2, 3 | CHANGES_REQUIRED |
| acta.ass.039.ass-039-l014773 (la) | 3 | 1, 2, 3 | PASS |
| pius-ix-acta.volume-03.line-00021313.part-08 (la) | 3 | 1, 2, 3 | PASS |
| acta.ass.006.ass-006-act-007 (la) | 1 | 1 | PASS |

## 1. Litterae encyclicae de libertate humana

`acta.ass.020.ass-020-014` · `la` · CHANGES_REQUIRED.

PDF `.scratch/encyclical-classic/readers-fixed/1888-06-20-acta-ass-020-ass-020-014-22cdfa56-la/1888-06-20-acta-ass-020-ass-020-014-22cdfa56-la.pdf`; SHA256 `6ee96db9f2543e0916de6a30919dee6e86efe049d67e9b530f120b90946c35b8`; 10 pages.

Source `src/sources/works/holy-see/acta-sanctae-sedis/editions/1887-acta-ass-020/artifacts/acta-historical-text-c3d47678/historical.txt`; SHA256 `c3d4767811d43be6597af243328f5a23229f3e271c4bdcf3543c462d2e7e2140`. Receipt `.scratch/encyclical-classic/readers-fixed/receipt.json`; SHA256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

Freshly viewed contact pages: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10. Fresh full-size pages: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10. Existing raster directory: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1888-06-20-acta-ass-020-ass-020-014-22cdfa56-la/1888-06-20-acta-ass-020-ass-020-014-22cdfa56-la`.

Pages 2, 4, 6 and 8 contain historical notes interrupting body sentences or words, but exact generated TeX gives those note groups their own paragraphs with boundaries on both sides. Those interruptions are accepted. The page 9 note listed as a blocker lacks the preceding boundary. Paragraph/body geometry is legible throughout; retained OCR blemishes and source hyphens remain. Page 10 retains the final dating clause and LEO PP. XIII before compact apparatus.

Blocking finding — pages 9: Historical note is fused into the body paragraph at the top of the left column. Generated body.tex lines 733–734 run “recte (1). Verumtamen in eiusmodi rerum adiunctis, si communis” directly into “(1) August, de lib. arò. lib. 1, cap. 6, n. 14.”; there is no preceding \par or blank paragraph boundary. A \par follows at line 735. Exact source LF 24258–24259 likewise has no blank separation before the note. This is a true one-sided note boundary, distinct from the acceptable both-sided note blocks elsewhere in this PDF.

## 2. Quas Primas

`papal.pius-xi.hf-p-xi-enc-11121925-quas-primas` · `la` · PASS.

PDF `.scratch/encyclical-classic/readers-fixed/1925-12-11-papal-pius-xi-hf-p-xi-enc-11121925-quas-primas-01f6711d-la/1925-12-11-papal-pius-xi-hf-p-xi-enc-11121925-quas-primas-01f6711d-la.pdf`; SHA256 `4ef2265110cf198924bd37f50b61f2d984269c986bdd29e182e1c5e1229a47b1`; 8 pages.

Source `src/sources/works/pius-xi/quas-primas/editions/2026-10-26-vatican-la/artifacts/latin-text-549b7a6e70f9/text.txt`; SHA256 `549b7a6e70f9f799e74781980f2586a06a1f75d9553c82d1cccd2e7c3914b31d`. Receipt `.scratch/encyclical-classic/readers-fixed/receipt.json`; SHA256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

Freshly viewed contact pages: 1, 2, 3, 4, 5, 6, 7, 8. Fresh full-size pages: 1, 7, 8. Existing raster directory: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1925-12-11-papal-pius-xi-hf-p-xi-enc-11121925-quas-primas-01f6711d-la/1925-12-11-papal-pius-xi-hf-p-xi-enc-11121925-quas-primas-01f6711d-la`.

The sparse final page 8 contains genuine historical notes 31–36, ending Rom., VI, 13.; the act closes with its dating clause and PIUS PP. XI on page 7. Notes 1–30 continue in the right column of page 7. These are addressable source notes, so the final page is source-bearing. No clipping, overlap or materially unreadable composition found.

## 3. E Supremi

`papal.pius-x.hf-p-x-enc-04101903-e-supremi.acqr-1904-english` · `en` · PASS.

PDF `.scratch/encyclical-classic/readers-fixed/1903-10-04-papal-pius-x-hf-p-x-enc-04101903-e-supremi-acqr-1904-english-b257356e-en/1903-10-04-papal-pius-x-hf-p-x-enc-04101903-e-supremi-acqr-1904-english-b257356e-en.pdf`; SHA256 `907f7dc0215b103b08d2e2afcbf3456de6812145de59f9d8a08ef99183944c73`; 6 pages.

Source `src/sources/works/journals/american-catholic-quarterly-review/editions/1904-volume-29/artifacts/english-reading-0dc48b0fe2f9/text.txt`; SHA256 `0dc48b0fe2f9867355c1f886a0aa337e6ae4030a0901595f13ce26de32e3536e`. Receipt `.scratch/encyclical-classic/readers-fixed/receipt.json`; SHA256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

Freshly viewed contact pages: 1, 2, 3, 4, 5, 6. Fresh full-size pages: 1, 2, 3, 4, 5, 6. Existing raster directory: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1903-10-04-papal-pius-x-hf-p-x-enc-04101903-e-supremi-acqr-1904-english-b257356e-en/1903-10-04-papal-pius-x-hf-p-x-enc-04101903-e-supremi-acqr-1904-english-b257356e-en`.

Sparse final page 6 retains the historical dating clause and Pius X. subscription, followed by compact source/rights apparatus. The visibly retained printed line transposition and OCR word divisions are disclosed in that apparatus; the review does not correct them. The black square beside WORK FOR THE LAITY on page 5 is literal source U+25A0 at source LF 75 and is explicitly rendered with the symbol fallback in body.tex line 166; it is not a missing-glyph box. Headings have following text and remain legible. No geometry blocker found.

## 4. Mortalium Animos

`papal.pius-xi.hf-p-xi-enc-19280106-mortalium-animos` · `la` · PASS.

PDF `.scratch/encyclical-classic/readers-fixed/1928-01-06-papal-pius-xi-hf-p-xi-enc-19280106-mortalium-animos-84c4d016-la/1928-01-06-papal-pius-xi-hf-p-xi-enc-19280106-mortalium-animos-84c4d016-la.pdf`; SHA256 `95448f0c78c706af07eab53efcc122635a8075bd66a692433bd8c8b1bffbd115`; 5 pages.

Source `src/sources/works/papal-documents/1928-01-06-papal-pius-xi-hf-p-xi-enc-19280106-mortalium-animos-84c4d016/editions/2026-10-26-vatican-la/artifacts/latin-text-74ed5b789c36/text.txt`; SHA256 `74ed5b789c36ea605e8e87ccb894da6b29c122be5e2ba759e4d4944b4836b436`. Receipt `.scratch/encyclical-classic/readers-fixed/receipt.json`; SHA256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

Freshly viewed contact pages: 1, 2, 3, 4, 5. Fresh full-size pages: 1, 5. Existing raster directory: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1928-01-06-papal-pius-xi-hf-p-xi-enc-19280106-mortalium-animos-84c4d016-la/1928-01-06-papal-pius-xi-hf-p-xi-enc-19280106-mortalium-animos-84c4d016-la`.

The act closes on page 5 with its dating clause and PIUS PP. XI, followed by separately addressable historical notes 1–30 flowing across the columns. Final source/rights apparatus is compact on the same source-bearing page. No clipping, overlap, suspicious heading split or materially unreadable composition found.

## 5. Ubi Nos

`acta.ass.006.ass-006-act-011` · `la` · CHANGES_REQUIRED.

PDF `.scratch/encyclical-classic/readers-fixed/1871-05-15-acta-ass-006-ass-006-act-011-0f97c911-la/1871-05-15-acta-ass-006-ass-006-act-011-0f97c911-la.pdf`; SHA256 `6a813d5aa891b75bc334192d8d994636e933c0b5493be641ebc97af3c665f7ba`; 3 pages.

Source `src/sources/works/holy-see/acta-sanctae-sedis/editions/volume-6-1870-1871/artifacts/acta-historical-text-6f710d76/historical.txt`; SHA256 `6f710d76d851369aa5ea49b7fefa65c2279ee93cf1c54f3555e5365f4fbb628a`. Receipt `.scratch/encyclical-classic/readers-fixed/receipt.json`; SHA256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

Freshly viewed contact pages: 1, 2, 3. Fresh full-size pages: 1, 2, 3. Existing raster directory: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1871-05-15-acta-ass-006-ass-006-act-011-0f97c911-la/1871-05-15-acta-ass-006-ass-006-act-011-0f97c911-la`.

The page 1 Act. 4, 32 note and page 3 references interrupt words or sentences but have explicit TeX paragraph boundaries on both sides and are accepted. They are not the one-sided note groups listed as blockers. Page 3 retains dating, PIUS PP. IX and terminal source references before compact apparatus. No clipping or source-ending loss observed.

Blocking finding — pages 1, 2: Historical note groups join the preceding body paragraph. Page 1 left column: body.tex lines 40–42 append “(1) Has litteras encyclicas…” and “— (2) Epist. 243.” directly to “Iniquitas enim viam suam tenere”; the first following \par is line 43, with no \par before the note. Exact source LF 10202–10204 agrees. Page 2 left column: body.tex lines 121–123 append “(1) S. Bern. ep. 238 et 130…” through “habes infra pag. 264 et seqq.” directly to “maxima Italorum”; the first following \par is line 124. Exact source LF 10283–10285 agrees. Both note groups need explicit separation on the body side before acceptance.

## 6. EPISTOLA                ENCYCLICA S S . D. N. Pii Div. Prov. PP. X ad Archiepiscopos et Episco- pos Galliae, ubi, consociationibus cultualibus ex lege Gal- lica constituendis improbatis, iidem incitantur disponendo instruendoque religioso cultui ( i ) .

`acta.ass.039.ass-039-l014773` · `la` · PASS.

PDF `.scratch/encyclical-classic/readers-fixed/undated-acta-ass-039-ass-039-l014773-7b752472-la/undated-acta-ass-039-ass-039-l014773-7b752472-la.pdf`; SHA256 `5086f7eb272a8c06643995c3b431a406dde850c0d73df558848aa8f2754949f3`; 3 pages.

Source `src/sources/works/holy-see/acta-sanctae-sedis/editions/1906-acta-ass-039/artifacts/acta-historical-text-036e2b7e/historical.txt`; SHA256 `036e2b7e75b6d396ae9ef1aef98669749cbac3c5b0db08305510ffb04046dfc6`. Receipt `.scratch/encyclical-classic/readers-fixed/receipt.json`; SHA256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

Freshly viewed contact pages: 1, 2, 3. Fresh full-size pages: 1, 2, 3. Existing raster directory: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/undated-acta-ass-039-ass-039-l014773-7b752472-la/undated-acta-ass-039-ass-039-l014773-7b752472-la`.

Latin main text and the historical French episcopal response/legal quotations remain in the recorded order; the terminal note identifies their multilingual extent. Exact TeX confirms both-sided paragraph boundaries around the French note blocks and the short Haec referuntur note. Their interruption of body sentences/words is accepted under the profile; earlier suspicion based on interruption alone is withdrawn. OCR letterspacing/source hyphens remain, but the words and geometry are readable. Page 3 retains final dating and PIUS PP. X. The rights colophon continues at the top of the right column on that same source-bearing page.

## 7. Incredibili — ad episcopos Neogranatenses

`pius-ix-acta.volume-03.line-00021313.part-08` · `la` · PASS.

PDF `.scratch/encyclical-classic/readers-fixed/1863-09-17-pius-ix-acta-volume-03-line-00021313-part-08-7b974059-la/1863-09-17-pius-ix-acta-volume-03-line-00021313-part-08-7b974059-la.pdf`; SHA256 `37741657ea7fe67743ea0d5f09edcac993c8179c8c0fd0398f7b62b69d40e6d3`; 3 pages.

Source `src/sources/works/papal-collections/pii-ix-acta-pars-prima-volume-3/editions/1864-rome-ia-mul/artifacts/ocr-3a788e20d82b/ocr.txt`; SHA256 `3a788e20d82b5eb754d99242edaf43006aa915d8ebdfd9e1a62e73a1804e19f8`. Receipt `.scratch/encyclical-classic/readers-fixed/receipt.json`; SHA256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

Freshly viewed contact pages: 1, 2, 3. Fresh full-size pages: 1, 2, 3. Existing raster directory: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1863-09-17-pius-ix-acta-volume-03-line-00021313-part-08-7b974059-la/1863-09-17-pius-ix-acta-volume-03-line-00021313-part-08-7b974059-la`.

The short references on page 2 are separate paragraphs with explicit \par on both sides (body.tex 146/149 and 183/186); their interruption of abro-/gamus and praemu-/nire is accepted. Sparse final page 3 retains a genuine historical dating clause, including literal OCR year 4863, before compact apparatus. The title metadata identifies 1863-09-17; this review does not silently correct the body. No clipping, overlap or meaningful unreadability found.

## 8. Qui nuper

`acta.ass.006.ass-006-act-007` · `la` · PASS.

PDF `.scratch/encyclical-classic/readers-fixed/1859-06-18-acta-ass-006-ass-006-act-007-a91724cb-la/1859-06-18-acta-ass-006-ass-006-act-007-a91724cb-la.pdf`; SHA256 `00c509a3e31d3e34a850ec6033e6df481a43ce8c18344b2444a7efc0281d390b`; 1 pages.

Source `src/sources/works/holy-see/acta-sanctae-sedis/editions/volume-6-1870-1871/artifacts/acta-historical-text-381e6e11/historical.txt`; SHA256 `381e6e11f80a958fe6480ae7815679df9fb916c4a138b19328c32cc367543e89`. Receipt `.scratch/encyclical-classic/readers-fixed/receipt.json`; SHA256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

Freshly viewed contact pages: 1. Fresh full-size pages: 1. Existing raster directory: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1859-06-18-acta-ass-006-ass-006-act-007-a91724cb-la/1859-06-18-acta-ass-006-ass-006-act-007-a91724cb-la`.

The single page retains the opening protocol, source body and final dating clause through Pontificatus Nostri Anno Decimo-quarto. The body continues left column to right column normally, and compact source/rights apparatus remains beneath the historical ending. Local OCR spacing defects such as quaeramus.AtquehacoccasioneVos are visible and were checked against the pinned source; they do not create sustained unreadable passage geometry. No clipped or overlapping text found.

## Limits

Visual layout/usability review and boundary checks only. No whole-source word-for-word collation, original-print facsimile verification, translation review or renewed rights assessment is claimed. Existing receipt text-fidelity PASS is a pinned build fact, not this reviewer’s independent full-text collation. No installed/public artifact was changed.

The earlier visual suspicions concerning both-sided blocks in Libertas, Ubi Nos and ASS 39 were checked against exact generated paragraph boundaries and withdrawn where those boundaries exist. The final findings above preserve only the two documents with demonstrably missing pre-note boundaries. No earlier checkpoint is counted as visual coverage.
