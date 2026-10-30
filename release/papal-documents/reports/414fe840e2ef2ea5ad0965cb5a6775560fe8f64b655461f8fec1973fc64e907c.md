# Independent baseline continuation 10: exact-byte page review

Reviewed 2026-10-30. Fresh coverage: 7 PDFs, 35 of 35 pages on the exact existing contact sheets, plus 27 full-resolution page views. Result: 4 PASS PDFs (26 pages) and 3 CHANGES_REQUIRED PDFs (9 pages). Every listed page was personally inspected in this lane; prior checkpoints supplied no inspection credit.

Packet: `.scratch/encyclical-ready-package/baseline-review-packets/10.json`; SHA256 `2d74b4df8e206bb0c4e4e8161e096ff8f1ebfd606dcfdd9180080edb3fe0d417`.
Canonical report destination: `src/sources/papal-documents/encyclicals-baseline-continuation-10.md`. This file is the report to copy byte-for-byte; no canonical destination was written in this lane.

## Verification and method

- Read the applicable personal guidance, repository AGENTS.md, papal-document profile, PDF build/review requirements, external-review handoff requirements and common brief. The bounded lane only produces its report and review rows; package assembly belongs to the coordinator.
- Recomputed each PDF SHA256 and used pdfinfo to verify every page count. Recomputed the exact receipt SHA256 and matched every packet receipt_row with the receipt document identified by id/language. Matched every source_row with the frozen manifest row.
- Recomputed all packet-local source text, segment manifest, frozen manifest, source-controller record and local controller payload pins. Five controller payload references are nonlocal (remote/restricted) and were not downloaded. No local pin mismatch was found.
- Verified the common brief hash, raster-manifest hash, every per-document cache PDF/page pin, and SHA256/size of every cache-listed contact sheet, full-page raster and thumbnail. Existing rasters were read only; this is fresh inspection of those images, not inherited review or a raster-reuse claim.
- Opened sheet-001.png in each packet raster_dir at original resolution and inspected every numbered page. Full-page images opened at their original 1700×2200 resolution are listed per document. Full-size coverage includes every first/final page and the note-bearing, sparse, garbled or otherwise suspicious pages.
- Poppler pdfinfo, pdffonts and pdftotext successfully parsed all seven files. All are unencrypted Letter-size PDF 1.7, with no JavaScript or reported Suspects. All fonts are embedded, subsetted and Unicode-mapped; Latin Modern is used throughout, with the English Christ Our Redeemer also using FreeSerif. No separate object-level structural validator was run.
- Checked pdftotext bounding boxes on every page; no text lay outside the normal page margins (the check used x=45–568pt and y=25–778pt bounds). Visual inspection found no clipping, overlap, column collision, missing page content, bad heading split or project-apparatus-only page. Two columns continue in normal left-to-right reading order.
- Compared retained-source first/last excerpts with extracted PDF text and the rendered boundaries, using physical LF lines (formfeeds are not counted as line breaks). No renderer-created beginning or ending loss was found. The receipt records source-aware text-fidelity PASS for every PDF; that is recorded evidence, not a fresh full-source collation.

Receipt: `.scratch/encyclical-classic/readers-fixed/receipt.json`; SHA256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
Frozen manifest SHA256: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`. Raster manifest SHA256: `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`.

## Document results

### 1. The Christian Constitution of States — PASS

Identity: `papal.leo-xiii.hf-l-xiii-enc-01111885-immortale-dei` / `en`. Pages: **11**. PDF SHA256: `c073739c95433e9ac27acb654e2e02264946799da653046f7e2a34c12fc70f54`.
PDF: `.scratch/encyclical-classic/readers-fixed/1885-11-01-papal-leo-xiii-hf-l-xiii-enc-01111885-immortale-dei-ce994b60-en/1885-11-01-papal-leo-xiii-hf-l-xiii-enc-01111885-immortale-dei-ce994b60-en.pdf`.
Actual contact-sheet pages: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11. Actual full-resolution pages: 1, 10, 11.
Raster evidence: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1885-11-01-papal-leo-xiii-hf-l-xiii-enc-01111885-immortale-dei-ce994b60-en/1885-11-01-papal-leo-xiii-hf-l-xiii-enc-01111885-immortale-dei-ce994b60-en/contact-sheets/sheet-001.png` and `pages/page-*.png`.
Retained source SHA256: `fc16a357008f7f2e1b0f331dceecc6ae76138b370a19665208fb064677cf6573`. Segment manifest SHA256: `42143773d485cce2582a73dab76e71ee8fd31293974485410a37e78700cc949f`.

- **QUALIFICATION**, page(s) 11: The sparse last page is source-bearing: historical notes [4]–[26], including substantive note [22], precede the compact project source/rights colophon. Historical endnotes begin on p10 and remain distinct, legible paragraphs.

Pages 2–9 were inspected at contact-sheet scale only; no suspicious geometry or actual note block there required a full-size view. First-page identification and p10–11 endnote/ending behavior were checked full size.

### 2. Christ Our Redeemer — PASS

Identity: `papal.leo-xiii.hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus` / `en`. Pages: **7**. PDF SHA256: `b583be861a06b88b37f176147aea9c513158d8004504d8d2743c7db11ab87d3d`.
PDF: `.scratch/encyclical-classic/readers-fixed/1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-en/1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-en.pdf`.
Actual contact-sheet pages: 1, 2, 3, 4, 5, 6, 7. Actual full-resolution pages: 1, 2, 3, 4, 5, 6, 7.
Raster evidence: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-en/1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-en/contact-sheets/sheet-001.png` and `pages/page-*.png`.
Retained source SHA256: `ed8e5a405701a51eec9124f0e63a4db7740ded35545fe5d99874ac9581541879`. Segment manifest SHA256: `7c356dd2d65ee0281e4c6b8fdf727658e684efbb061d7f5a815e54e36904b8d1`.

- **QUALIFICATION**, page(s) 1, 2, 3, 4, 5, 6, 7: Disclosed OCR word errors, literal broken-word hyphens and malformed reference marks remain visible (including backslash/caret-like forms and Ufe/Hfe forms). The English prose remains readable at full resolution. Citation blocks are distinct from body paragraphs, although source-order note insertion sometimes interrupts a sentence.
- **QUALIFICATION**, page(s) 7: The sparse last page retains the final invocation, Apostolic Blessing and historical John xii. 32 citation before the colophon; it is not apparatus-only.

### 3. Tametsi Futura Prospicientibus — PASS

Identity: `papal.leo-xiii.hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus` / `la`. Pages: **6**. PDF SHA256: `31f289d11b681f6bc62b8eb365971ca001b2df4d8c93d6412b95c7a039b8ea38`.
PDF: `.scratch/encyclical-classic/readers-fixed/1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-la/1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-la.pdf`.
Actual contact-sheet pages: 1, 2, 3, 4, 5, 6. Actual full-resolution pages: 1, 2, 3, 4, 5, 6.
Raster evidence: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-la/1900-11-01-papal-leo-xiii-hf-l-xiii-enc-01111900-tametsi-futura-prospicientibus-56340f3f-la/contact-sheets/sheet-001.png` and `pages/page-*.png`.
Retained source SHA256: `ddf59fbe77b760a61333334736f94fe444d073d7b17229fc35719afb4ae9f109`. Segment manifest SHA256: `not applicable (whole retained text artifact)`.

- **QUALIFICATION**, page(s) 6: The sparse last page retains the historical blessing, dating clause (1 November 1900) and LEO XIII subscription before the compact colophon. It is source-bearing.

### 4. Singulari quadam — CHANGES_REQUIRED

Identity: `acta.aas.004.archive.aas.004.066` / `la`. Pages: **3**. PDF SHA256: `ad34164692a5ba36b4095d7c2d929422925e0833909422db636997255c9a4d46`.
PDF: `.scratch/encyclical-classic/readers-fixed/1912-09-24-acta-aas-004-archive-aas-004-066-298ae7d8-la/1912-09-24-acta-aas-004-archive-aas-004-066-298ae7d8-la.pdf`.
Actual contact-sheet pages: 1, 2, 3. Actual full-resolution pages: 1, 2, 3.
Raster evidence: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1912-09-24-acta-aas-004-archive-aas-004-066-298ae7d8-la/1912-09-24-acta-aas-004-archive-aas-004-066-298ae7d8-la/contact-sheets/sheet-001.png` and `pages/page-*.png`.
Retained source SHA256: `e0104108dc7b3434b7a3b7ab4a312dd657d0c0ea67ddf4a2249f54030e0a4312`. Segment manifest SHA256: `d8e0ac17740eb5255218b8158a90f9681650e8bb5c6a4413a409e0562291c020`.

- **BLOCKING**, page(s) 1, 2, 3: Pervasive source OCR character-level spaces fragment words across both columns and line endings. Word spaces cannot be reliably distinguished from intraword spaces; ordinary continuous reading is materially impaired. Literal fidelity and the disclosure do not establish an acceptable reading layout.
- **QUALIFICATION**, page(s) 2, 3: The p2 historical citation is its own paragraph block; the closing blessing and 24 September 1912 dating clause remain on p3. The pinned source selection ends at the dating clause and does not contain a separate papal name subscription.

### 5. Inter graves ac multiplices curas — CHANGES_REQUIRED

Identity: `acta.ass.026.ass-026-l25716` / `la`. Pages: **3**. PDF SHA256: `30e9c9210b30e60c33d0f0ac42f02984e28c4a6e96500e40f5d6f45e97b52839`.
PDF: `.scratch/encyclical-classic/readers-fixed/1894-05-01-acta-ass-026-ass-026-l25716-cc623bdc-la/1894-05-01-acta-ass-026-ass-026-l25716-cc623bdc-la.pdf`.
Actual contact-sheet pages: 1, 2, 3. Actual full-resolution pages: 1, 2, 3.
Raster evidence: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1894-05-01-acta-ass-026-ass-026-l25716-cc623bdc-la/1894-05-01-acta-ass-026-ass-026-l25716-cc623bdc-la/contact-sheets/sheet-001.png` and `pages/page-*.png`.
Retained source SHA256: `15a33cfd01401e070c0b912e4154be4f7d163d6730ac8f1cd64ed6096d756d3d`. Segment manifest SHA256: `2b8424578324afc5b1bedc358f90a31c903610ed7f7123e18248e41aac159af3`.

- **BLOCKING**, page(s) 1, 2, 3: Pervasive source OCR character-level spaces and midword line boundaries make the Latin body materially difficult to read throughout both columns; justified spacing further obscures word boundaries.
- **BLOCKING**, page(s) 3: The terminal historical note is fused into the papal subscription in the right column: LEO P P . XIII. (1) Act. 26, 18. Existing body TeX has both in one paragraph. The source LF selection retains the citation on a separate physical line, but the rendered reader does not give it a separate block.

The raw-source ending and existing generated body TeX confirm the fused note: the final paragraph contains both the subscription and citation. A separately evidenced source/paragraph repair and fresh hash-bound review are required before this exact reader can pass.

### 6. Nemo certe ignorat — ad archiepiscopos et episcopos Hiberniae — CHANGES_REQUIRED

Identity: `pius-ix-acta.volume-01.line-00012583.part-02` / `la`. Pages: **3**. PDF SHA256: `f3f94b0859775852908d8ae4db029c022c312687fbf61387042c68644ef48ef0`.
PDF: `.scratch/encyclical-classic/readers-fixed/1852-03-25-pius-ix-acta-volume-01-line-00012583-part-02-5b12159e-la/1852-03-25-pius-ix-acta-volume-01-line-00012583-part-02-5b12159e-la.pdf`.
Actual contact-sheet pages: 1, 2, 3. Actual full-resolution pages: 1, 2, 3.
Raster evidence: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1852-03-25-pius-ix-acta-volume-01-line-00012583-part-02-5b12159e-la/1852-03-25-pius-ix-acta-volume-01-line-00012583-part-02-5b12159e-la/contact-sheets/sheet-001.png` and `pages/page-*.png`.
Retained source SHA256: `898bc939f063a4b1e2cc87b5bba06d51fccbf14ff329c4bf7c8261b60b595205`. Segment manifest SHA256: `5192482f91be6abb2b75e1b39123e491627b87f82341388d1493ca2537d0934f`.

- **BLOCKING**, page(s) 1: A long OCR-corrupted passage, covering the Gregory quotation and the following exhortation across the lower left and upper right columns, is materially unreadable in places. Examples include Quensebrenvos Nosteume, No-SW condis adfectu Von allequimur, and in ostibolicae Eeolosee/de-cteina. This is source OCR corruption, not small type or clipping; literal retention does not cure the reading defect.
- **QUALIFICATION**, page(s) 1, 3: The historical citations on p1 are distinct blocks. The final page retains the concluding body, blessing and 25 March 1852 dating clause. The project rights line continues at the top of its right column on that same source-bearing page.

The issuer banner and PDF Author metadata retain the literal collection form PII IX PONTIFICIS MAXIMI ACTA. Pius IX is identifiable; this is a metadata qualification, not a claim that this lane normalized that field.

### 7. Praedecessores Nostros — pro regno Hiberniae — PASS

Identity: `pius-ix-acta.volume-01.line-00001267.part-01` / `la`. Pages: **2**. PDF SHA256: `077909227dedaea334ab3eae0ba2cefc7c4c1d6c7ac80cb92b46862bb92d4b3f`.
PDF: `.scratch/encyclical-classic/readers-fixed/1847-03-25-pius-ix-acta-volume-01-line-00001267-part-01-d2bdb167-la/1847-03-25-pius-ix-acta-volume-01-line-00001267-part-01-d2bdb167-la.pdf`.
Actual contact-sheet pages: 1, 2. Actual full-resolution pages: 1, 2.
Raster evidence: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1847-03-25-pius-ix-acta-volume-01-line-00001267-part-01-d2bdb167-la/1847-03-25-pius-ix-acta-volume-01-line-00001267-part-01-d2bdb167-la/contact-sheets/sheet-001.png` and `pages/page-*.png`.
Retained source SHA256: `898bc939f063a4b1e2cc87b5bba06d51fccbf14ff329c4bf7c8261b60b595205`. Segment manifest SHA256: `8db964ea305a0ebb74e5af7baa2d2ea35bd5165bab1445ca867a87e9014fe7b0`.

- **QUALIFICATION**, page(s) 1, 2: Long historical notes continue in source page order as separate paragraph blocks, sometimes interrupting midword body continuations. Existing body TeX confirms their separation; apparent fusion at contact-sheet scale was ruled out. Residual OCR errors remain, including the initial |) Nostros form.
- **QUALIFICATION**, page(s) 2: The final page retains historical note continuations, the concluding blessing and the 25 March 1847 dating clause through Nostri Anno Primo before the compact colophon.

The issuer banner and PDF Author metadata retain the literal collection form PII IX PONTIFICIS MAXIMI ACTA. Pius IX is identifiable; this is a metadata qualification, not a claim that this lane normalized that field.

## Acceptance limits and disposition

- Fresh visual review of the exact packet bytes and source-boundary excerpts only; no whole-source or facsimile collation, translation verification, or independent rights adjudication.
- Mechanical text-fidelity PASS is the pinned receipt result; no fresh whole-document fidelity algorithm was run. PDF first/last source wording was compared with the retained source selection.
- Remote/restricted parent payloads without packet-local payload paths were not acquired; their local controller records were hash-verified.
- No rerender, reraster, cache mutation, installation, canonical edit or Git mutation was performed. No inherited visual coverage or page reuse is claimed.

Hold the three CHANGES_REQUIRED readers. Their source fidelity receipts remain valid records of literal preservation, but cannot override the actual readability and note-separation findings. The four PASS statuses accept the inspected typography and stated source limitations only. None certifies historical accuracy or promotes the source to image-collated status.
