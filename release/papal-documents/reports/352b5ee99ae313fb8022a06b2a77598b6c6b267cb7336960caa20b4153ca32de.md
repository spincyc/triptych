# Independent baseline continuation review 07

Cold review of the six exact PDFs in `.scratch/encyclical-ready-package/baseline-review-packets/07.json`. Result: **5 PASS (19 pages), 1 CHANGES_REQUIRED (13 pages)**. Actual fresh coverage is **32/32 pages** in contact sheets and **32/32 full-resolution page views**. No previous checkpoint coverage was inherited. No page is accepted merely because its raster exists.

## Identity and verification

- Packet SHA256: `799a717c726994820ad9a8e7b53e0d008dd9c7f0f96777a031666117c06ed717`.
- Canonical report destination: `src/sources/papal-documents/encyclicals-baseline-continuation-07.md`; this lane writes only its assigned scratch.
- Exact receipt: `.scratch/encyclical-classic/readers-fixed/receipt.json`; SHA256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
- Frozen input manifest SHA256: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.
- Raster manifest SHA256: `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`.
- All **145/145** recorded checks pass in `verification.json`: PDF, receipt, common brief, frozen manifest, source artifact/payload and segment-manifest hashes; exact receipt rows; PDF page counts; raster-manifest hash; each raster cache PDF/page pin; every listed raster/contact-sheet/thumbnail file hash.
- `pdfinfo` reads all six PDFs as unencrypted PDF 1.7, US Letter, with correct displayed title/author/language metadata and the 2026-10-30T02:56:48Z render revision (shown locally as Oct 29 21:56:48 CDT). `pdffonts` lists all fonts as embedded, subset and Unicode mapped. `pdftotext -raw` succeeds for all six. Each PDF is below the repository size-review thresholds.
- Source openings/endings were read from the exact pinned payloads. For archival volume selections, one-based physical **LF** ranges from the receipt were used, retaining form-feed characters inside lines. `boundaries.json` records this bounded check. Displayed final Benedictions, subscriptions and terminal source notes match the inspected selection endings; no loss at an outer boundary was observed.

## Page evidence and dispositions

| Reader | Language | Pages inspected in contact sheet | Full-resolution pages | Disposition |
| --- | --- | --- | --- | --- |
| The Study of Holy Scripture | en | 1–13 | 1–13 | CHANGES_REQUIRED |
| Ad diem illum | en | 1–7 | 1–7 | PASS |
| Nobilissima Gallorum gens | la | 1–4 | 1–4 | PASS |
| Maximam Gravissimamque — historical abridged English translation | en | 1–4 | 1–4 | PASS |
| Christi nomen | la | 1–2 | 1–2 | PASS |
| Superiore Anno | la | 1–2 | 1–2 | PASS |

### 1. The Study of Holy Scripture — CHANGES_REQUIRED

- ID: `papal.leo-xiii.hf-l-xiii-enc-18111893-providentissimus-deus` (en).
- PDF: `.scratch/encyclical-classic/readers-fixed/1893-11-18-papal-leo-xiii-hf-l-xiii-enc-18111893-providentissimus-deus-ec8dd363-en/1893-11-18-papal-leo-xiii-hf-l-xiii-enc-18111893-providentissimus-deus-ec8dd363-en.pdf`.
- PDF SHA256: `234ef12d1b952160ae9fdd46d18f7dc528f369d3c9ede414133eaa6ef5eb15c2`; exact page count: 13.
- Source payload SHA256: `ed8e5a405701a51eec9124f0e63a4db7740ded35545fe5d99874ac9581541879`.
- Existing contact sheet: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1893-11-18-papal-leo-xiii-hf-l-xiii-enc-18111893-providentissimus-deus-ec8dd363-en/1893-11-18-papal-leo-xiii-hf-l-xiii-enc-18111893-providentissimus-deus-ec8dd363-en/contact-sheets/sheet-001.png`.
- Actual contact-sheet pages: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13. Actual full-resolution views: the same complete page list in the packet raster directory’s `pages/`.
- **blocking**, pages 5, 6, 7, 8, 9, 11, 12: Material inherited OCR unreadability. Page 5 upper-right, after “this knowledge, falsely”, contains several nonsensical lines in the sentence about ancient and true science; page 6 lower-right, from the sentence about interpretation of the Scriptures through the private student, is heavily corrupted; page 7 top-left opening and the lines before “Church; on the other” lose coherent words over multiple lines; page 8 left upper-middle passage after “the excellent work which Catholics” and lower-right passage about the Church contain garbled clauses; page 9 top-left opening and its next paragraph contain unreadable stretches; page 11 left lower-third from “It follows” through the Fathers contains extensive nonsense strings; page 12 right lower-third concluding exhortation/quotation contains repeated junk sequences and black-square glyphs. These are substantive reading losses rather than ordinary recoverable misspellings. The stated uncorrected-OCR limitation and mechanical fidelity do not establish readable publication bytes. Hold these bytes for source-level repair/replacement and fresh review.
- **qualification**, pages 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13: Historical references occur as separately indented blocks at retained source-page transitions, sometimes before an interrupted body sentence resumes. Their position alone is not a note/body fusion finding; no source-order correction is inferred by this review. Additional literal OCR errors, retained running headings/folios and junk characters remain, including isolated damaged spans on pages 1–2 and the quotation at the top of page 13.
- **qualification**, pages 13: Sparse final page is source-bearing: the ending Apostolic Benediction and source notes [1]–[17] precede the compact ruled project apparatus. It is not an apparatus-only page.
- Geometry: normal left-column then right-column continuation; no observed clipping, overlap, cropped title, lost source ending or apparatus-only terminal page. Body/colophon scale and separation remain legible. The disposition does not certify the correctness of source words.

### 2. Ad diem illum — PASS

- ID: `papal.pius-x.hf-p-x-enc-02021904-ad-diem-illum-laetissimum.acqr-1904-english` (en).
- PDF: `.scratch/encyclical-classic/readers-fixed/1904-02-02-papal-pius-x-hf-p-x-enc-02021904-ad-diem-illum-laetissimum-acqr-1904-english-b844e449-en/1904-02-02-papal-pius-x-hf-p-x-enc-02021904-ad-diem-illum-laetissimum-acqr-1904-english-b844e449-en.pdf`.
- PDF SHA256: `a4bc762ec724560dcb8f6d128dcb6235e5f05a26aae94dafc524a286ce2a2238`; exact page count: 7.
- Source payload SHA256: `0dc48b0fe2f9867355c1f886a0aa337e6ae4030a0901595f13ce26de32e3536e`.
- Existing contact sheet: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1904-02-02-papal-pius-x-hf-p-x-enc-02021904-ad-diem-illum-laetissimum-acqr-1904-english-b844e449-en/1904-02-02-papal-pius-x-hf-p-x-enc-02021904-ad-diem-illum-laetissimum-acqr-1904-english-b844e449-en/contact-sheets/sheet-001.png`.
- Actual contact-sheet pages: 1, 2, 3, 4, 5, 6, 7. Actual full-resolution views: the same complete page list in the packet raster directory’s `pages/`.
- **qualification**, pages 1, 2, 3, 4, 5, 6, 7: Literal historical OCR punctuation, broken words and note-marker recognition errors remain, but the body remains readable. Historical reference notes are distinct indented blocks, including blocks that intervene at retained source-page breaks; no fused note/body paragraph was observed.
- **qualification**, pages 6, 7: Jubilee conditions and faculties remain as substantive source text. Final page retains the closing Benediction, date, Pius X signature, and the final historical note rendered literally as “1* Offl. Immac. Cone.” before the ruled project colophon; the source-bound note is present despite its OCR marker.
- Geometry: normal left-column then right-column continuation; no observed clipping, overlap, cropped title, lost source ending or apparatus-only terminal page. Body/colophon scale and separation remain legible. The disposition does not certify the correctness of source words.

### 3. Nobilissima Gallorum gens — PASS

- ID: `acta.ass.016.ass-016-act-006` (la).
- PDF: `.scratch/encyclical-classic/readers-fixed/1884-02-08-acta-ass-016-ass-016-act-006-2b186389-la/1884-02-08-acta-ass-016-ass-016-act-006-2b186389-la.pdf`.
- PDF SHA256: `8d1e260b1e0d842b362ef7416dce7a29e934114ac865db971263e8734cc5ab78`; exact page count: 4.
- Source payload SHA256: `83bd7db6c3f5d5bb95ad0e942b948ed5d72c7d0aecd7d0992064d82b962bcc24`.
- Existing contact sheet: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1884-02-08-acta-ass-016-ass-016-act-006-2b186389-la/1884-02-08-acta-ass-016-ass-016-act-006-2b186389-la/contact-sheets/sheet-001.png`.
- Actual contact-sheet pages: 1, 2, 3, 4. Actual full-resolution views: the same complete page list in the packet raster directory’s `pages/`.
- **qualification**, pages 1, 2, 3, 4: Retained archival OCR includes internal hyphen/space breaks, widely letter-spaced source words, and recognition errors. The type remains legible and the surrounding body can be followed. This is not a corrected Latin edition; in particular the damaged biblical wording in page 4 left column remains uncollated. No paragraph-scale unreadability or geometric interference comparable to the held English reader was found.
- **qualification**, pages 4: Final page retains substantial source body in the left column and the Benediction, dating clause and Leo XIII subscription in the right before the ruled project apparatus. No source-ending loss was observed at the pinned selection boundary.
- Geometry: normal left-column then right-column continuation; no observed clipping, overlap, cropped title, lost source ending or apparatus-only terminal page. Body/colophon scale and separation remain legible. The disposition does not certify the correctness of source words.

### 4. Maximam Gravissimamque — historical abridged English translation — PASS

- ID: `papal.pius-xi.hf-p-xi-enc-18011924-maximam-gravissimamque` (en).
- PDF: `.scratch/encyclical-classic/readers-fixed/1924-01-18-papal-pius-xi-hf-p-xi-enc-18011924-maximam-gravissimamque-b67da687-en/1924-01-18-papal-pius-xi-hf-p-xi-enc-18011924-maximam-gravissimamque-b67da687-en.pdf`.
- PDF SHA256: `05f8930e86da8c2fbc7fb606e7e102e5a6c4d733c029a2f965a5733db36a6f48`; exact page count: 4.
- Source payload SHA256: `7019568db20715af4e9d5a686f1b122af5e466d78744d07e6c6af26b4c9392d8`.
- Existing contact sheet: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1924-01-18-papal-pius-xi-hf-p-xi-enc-18011924-maximam-gravissimamque-b67da687-en/1924-01-18-papal-pius-xi-hf-p-xi-enc-18011924-maximam-gravissimamque-b67da687-en/contact-sheets/sheet-001.png`.
- Actual contact-sheet pages: 1, 2, 3, 4. Actual full-resolution views: the same complete page list in the packet raster directory’s `pages/`.
- **qualification**, pages 1, 2, 3, 4: Visible title explicitly identifies the historical abridged English translation. Source line-break artifacts, stray punctuation/underscores, broken words and OCR reference errors remain readable source limitations. The long title remains inside the page and does not clip. The omitted diocesan-association regulations are disclosed as the historical translator’s omission.
- **qualification**, pages 4: Final source text includes the Apostolic Blessing, complete displayed dating paragraph and PIUS XI subscription, followed by compact ruled project apparatus on the same page.
- Geometry: normal left-column then right-column continuation; no observed clipping, overlap, cropped title, lost source ending or apparatus-only terminal page. Body/colophon scale and separation remain legible. The disposition does not certify the correctness of source words.

### 5. Christi nomen — PASS

- ID: `acta.ass.027.ass-027-l15151` (la).
- PDF: `.scratch/encyclical-classic/readers-fixed/1894-12-24-acta-ass-027-ass-027-l15151-4689516c-la/1894-12-24-acta-ass-027-ass-027-l15151-4689516c-la.pdf`.
- PDF SHA256: `929ee068915f8eef5978a39b966fa38a685be3bef6f962426947127be0da1766`; exact page count: 2.
- Source payload SHA256: `76fd18c3621cc707adc62b79835f68c979493efd988d9e4a6916a3b16d17ae6f`.
- Existing contact sheet: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1894-12-24-acta-ass-027-ass-027-l15151-4689516c-la/1894-12-24-acta-ass-027-ass-027-l15151-4689516c-la/contact-sheets/sheet-001.png`.
- Actual contact-sheet pages: 1, 2. Actual full-resolution views: the same complete page list in the packet raster directory’s `pages/`.
- **qualification**, pages 1, 2: Retained OCR letter-spacing and broken words remain visible but readable. The second page has a deliberately empty right column, while the left contains substantial concluding source prose, Benediction, dating clause and Leo XIII subscription before the ruled colophon. It is source-bearing rather than apparatus-only.
- Geometry: normal left-column then right-column continuation; no observed clipping, overlap, cropped title, lost source ending or apparatus-only terminal page. Body/colophon scale and separation remain legible. The disposition does not certify the correctness of source words.

### 6. Superiore Anno — PASS

- ID: `papal.leo-xiii.hf-l-xiii-enc-30081884-superiore-anno` (la).
- PDF: `.scratch/encyclical-classic/readers-fixed/1884-08-30-papal-leo-xiii-hf-l-xiii-enc-30081884-superiore-anno-ada7c15c-la/1884-08-30-papal-leo-xiii-hf-l-xiii-enc-30081884-superiore-anno-ada7c15c-la.pdf`.
- PDF SHA256: `d5d48377d4a2c00521856261f0edf523d2678e0729ceb01e4d12602fdf629e63`; exact page count: 2.
- Source payload SHA256: `e59c71084162dd123e16b325713bcb977a4ca3c644714eb324a241f1c91441dd`.
- Existing contact sheet: `.scratch/encyclical-classic/visual-fixed/.scratch/encyclical-classic/readers-fixed/1884-08-30-papal-leo-xiii-hf-l-xiii-enc-30081884-superiore-anno-ada7c15c-la/1884-08-30-papal-leo-xiii-hf-l-xiii-enc-30081884-superiore-anno-ada7c15c-la/contact-sheets/sheet-001.png`.
- Actual contact-sheet pages: 1, 2. Actual full-resolution views: the same complete page list in the packet raster directory’s `pages/`.
- **qualification**, pages 2: Final page has an empty right column, while the left carries substantial source prose, Benediction, dating clause and Leo XIII subscription before the ruled colophon. The literal Roman-numeral source-date error MDCCCCLXXXIV is retained alongside the compact identification date 1884-08-30; this review does not certify the source wording or correct it.
- Geometry: normal left-column then right-column continuation; no observed clipping, overlap, cropped title, lost source ending or apparatus-only terminal page. Body/colophon scale and separation remain legible. The disposition does not certify the correctness of source words.

## Limits

- Fresh visual review of the exact assigned PDF bytes using existing packet rasters; every page was inspected in the contact sheet and at full resolution. No inherited page coverage or raster-reuse proof is claimed.
- Boundary checks compare retained source opening/ending with displayed opening/ending; no whole-source print-image collation, translation verification, new rights determination, or independent rerun of the receipt’s text-fidelity algorithm was performed.
- pdfinfo, pdffonts and successful pdftotext reads were checked. This is not a separate exhaustive PDF syntax/accessibility audit. No rerender, reraster, canonical/shared/cache modification, installation or Git mutation was performed.

The sole blocking disposition is the substantial unreadability of the pinned English Providentissimus Deus source reader. Its separate note paragraphs are not asserted to be fused. The five PASS dispositions are qualified layout/readability judgments on the disclosed historical sources, not source-collation or publication-authority decisions.
