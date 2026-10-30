# Independent baseline continuation review 16

Review date: 2026-10-30. Scope: the exact seven Latin PDFs in baseline-continuation packet 16. Outcome: **4 PASS (21 pages), 3 CHANGES_REQUIRED (15 pages)**. Fresh inspection covers all **36/36 pages**, first on the seven supplied contact sheets and then every page at full resolution (1700 × 2200 supplied rasters). No prior checkpoint inspection or acceptance was inherited.

## Byte identity and checks

Packet: `.scratch/encyclical-ready-package/baseline-review-packets/16.json`, SHA256 `fe3040395a3bc4c1ca7147957fb3da6499719778e9b414e130645893cfdb77aa`. The common-brief SHA256 matches the packet. Canonical report destination: `src/sources/papal-documents/encyclicals-baseline-continuation-16.md`.

Every PDF hash and `pdfinfo` page count matches the packet. The common receipt SHA256 is `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`; each packet receipt row matches the actual receipt. All 62 checked PDF/receipt/source/segment/frozen-manifest/controller/raster-manifest pin occurrences match. Every controller payload available as a tracked file was rehashed; restricted parent payloads with null paths were not acquired or inspected. All 79 raster-cache file hashes and sizes match, and each cache names the exact assigned PDF hash and page count. Detailed path/hash checks remain in `verification.json` in this lane scratch.

`pdfinfo`, `pdffonts`, and `pdftotext -raw` succeeded for each PDF. Metadata titles/authors match their packet identities; modification time corresponds to render revision 2026-10-30T02:56:48Z. All are Letter, PDF 1.7. Every listed font is embedded, subsetted and has Unicode mapping; no missing-glyph rendering was observed. `qpdf` is unavailable, so no independent qpdf structural check was run. PDF structure evidence is limited to successful Poppler parsing and all-page rendering supplied by the packet. No build, rerender, reraster, install, shared-cache or Git mutation was performed.

## Exact reviewed artifacts

| Document | Pages | Status | PDF SHA256 |
| --- | ---: | --- | --- |
| `papal.leo-xiii.hf-l-xiii-enc-01111885-immortale-dei` | 10 | PASS | `8b25675f0c347dcb86a920f314d0fbd7646bafb4b619d574bbf46f941d991b61` |
| `acta.aas.011.archive.aas.011.l008779` | 7 | CHANGES_REQUIRED | `3e98c102d9e7e2a3c899980f84dd22fecbf62767be0309a9e84d0a568a2c0c3f` |
| `acta.ass.014.ass-014-act-001` | 6 | CHANGES_REQUIRED | `8eb70ad23342aecadd133a0140016285f604af295d840fed54821280ab91d615` |
| `papal.benedict-xv.hf-ben-xv-enc-15061917-humani-generis-redemptionem` | 5 | PASS | `6f255c4d401e5c1ad82bf5a5146ea8bd49c26080315f0b31364b07fe7b8d1132` |
| `papal.leo-xiii.hf-l-xiii-enc-01051896-insignes` | 4 | PASS | `58d2e3442669296bc231437da839371090e3e146160a6f098f7ee29bc5ac3497` |
| `acta.aas.011.archive.aas.011.l018487` | 2 | CHANGES_REQUIRED | `62d41d26b0278d9e76348ef7c95844eaabb9057e035652206f1e221ecfeba17c` |
| `papal.benedict-xv.hf-ben-xv-enc-24111919-paterno-iam-diu` | 2 | PASS | `e9e7478f27297091ab1ec95160658c17c5cbd33af10f9f6c0d6f081855fece56` |

## Actual inspection and findings

For every row below, `contact-sheets/sheet-001.png` and the full-size `pages/page-N.png` images under that document’s exact packet `raster_dir` were opened. Immortale Dei uses zero-padded page-01.png through page-10.png. Every page listed is an actual fresh view. Two-column progression, identification, paragraph/heading breaks, justification, note legibility, margins, ending and apparatus were inspected. No clipping, overlap, missing glyph or project-apparatus-only page was found. The blocking note fusions and OCR unreadability are listed explicitly below.

### papal.leo-xiii.hf-l-xiii-enc-01111885-immortale-dei

**PASS**. PDF: `.scratch/encyclical-classic/readers-fixed/1885-11-01-papal-leo-xiii-hf-l-xiii-enc-01111885-immortale-dei-ce994b60-la/1885-11-01-papal-leo-xiii-hf-l-xiii-enc-01111885-immortale-dei-ce994b60-la.pdf`. Actual contact pages: 1–10. Actual full-resolution pages: 1–10. Receipt SHA256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

- QUALIFICATION, page(s) 10: Sparse final page retains the historical dating clause (1 November 1885) and LEO PP. XIII before the compact project apparatus. It is source-bearing and passes.

### acta.aas.011.archive.aas.011.l008779

**CHANGES_REQUIRED**. PDF: `.scratch/encyclical-classic/readers-fixed/undated-acta-aas-011-archive-aas-011-l008779-d06149c5-la/undated-acta-aas-011-archive-aas-011-l008779-d06149c5-la.pdf`. Actual contact pages: 1–7. Actual full-resolution pages: 1–7. Receipt SHA256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

- BLOCKER, page(s) 1, 2, 3, 4, 5, 6, 7: Pervasive retained OCR character spacing splits words into isolated letters and tiny groups throughout the source body, including the dating clause on p7. Full-resolution reading requires reconstruction of words; this is meaningful unreadability despite mechanical source fidelity.
- BLOCKER, page(s) 1, 2, 3: Historical references run into body paragraphs: p1 left column joins the body ending iucunda directly to 1 II, Cor., xi, 28., then resumes scilicet; p2 left joins commisit. to 1 Coloss., III, U. 2 Vita S. Bonifacii..., and p3 left appends 1 Vita S. Bonifacii... 2 Ibid... 3 Ep... to the preceding body paragraph. Note sets need separately identified source blocks; typography/fidelity disclosure does not cure fusion.
- QUALIFICATION, page(s) 7: The sparse final page preserves the historical dating clause, BENEDICTUS PP. XV and terminal source reference 1 Ep. L. (al. XLIX). No source-ending loss or apparatus-only terminal page was found.

### acta.ass.014.ass-014-act-001

**CHANGES_REQUIRED**. PDF: `.scratch/encyclical-classic/readers-fixed/1881-06-29-acta-ass-014-ass-014-act-001-37124c84-la/1881-06-29-acta-ass-014-ass-014-act-001-37124c84-la.pdf`. Actual contact pages: 1–6. Actual full-resolution pages: 1–6. Receipt SHA256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

- BLOCKER, page(s) 4: Historical notes fuse into body text in both columns. Left column reads ...patramus, im- (1) Sap. VI, 4, 5, 6, 8. (2) Rum. X, 12. (3) Ad Tit. III, 1. (4) I Timoth II, 1 3. before the body resumes mo omnium.... Right column reads quantum in (1) Legat pro Christian. (2) Apolog. n. 35 (3) Apolog. n. 37. before resumed auctoritate.... The note sets interrupt body words/sentences without their own block.
- QUALIFICATION, page(s) 1, 2, 3, 4, 5, 6: Retained OCR has frequent literal word-break hyphens/spaces and sporadic garbled tokens; p1 contains a particularly garbled source heading (J IE? _tr JtLi IX! I l i). The modern identification remains clear. These are uncollated source limitations, not missing glyphs; no silent textual correction is requested.
- QUALIFICATION, page(s) 6: Final page retains the closing blessing, historical dating, LEO P P . X I I I . and final Psal./Isai. source notes before the apparatus. Source ending is present.

### papal.benedict-xv.hf-ben-xv-enc-15061917-humani-generis-redemptionem

**PASS**. PDF: `.scratch/encyclical-classic/readers-fixed/1917-06-15-papal-benedict-xv-hf-ben-xv-enc-15061917-humani-generis-redemptionem-ac6fb370-la/1917-06-15-papal-benedict-xv-hf-ben-xv-enc-15061917-humani-generis-redemptionem-ac6fb370-la.pdf`. Actual contact pages: 1–5. Actual full-resolution pages: 1–5. Receipt SHA256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

- QUALIFICATION, page(s) 4, 5: Historical dating and BENEDICTUS PP. XV appear at the end of p4. Page 5 retains addressable historical reference notes [1]–[39] as separate entries, followed by project apparatus. Its open right column is acceptable because the page carries real source notes.

### papal.leo-xiii.hf-l-xiii-enc-01051896-insignes

**PASS**. PDF: `.scratch/encyclical-classic/readers-fixed/1896-05-01-papal-leo-xiii-hf-l-xiii-enc-01051896-insignes-32162ac4-la/1896-05-01-papal-leo-xiii-hf-l-xiii-enc-01051896-insignes-32162ac4-la.pdf`. Actual contact pages: 1–4. Actual full-resolution pages: 1–4. Receipt SHA256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

- QUALIFICATION, page(s) 4: The final source paragraphs, dating clause and LEO PP. XIII remain on p4. The compact project source note begins beneath its rule in the left column and continues at the top of the right column on the same page; no source or apparatus clipping was found.

### acta.aas.011.archive.aas.011.l018487

**CHANGES_REQUIRED**. PDF: `.scratch/encyclical-classic/readers-fixed/1919-11-24-acta-aas-011-archive-aas-011-l018487-b8b25bc8-la/1919-11-24-acta-aas-011-archive-aas-011-l018487-b8b25bc8-la.pdf`. Actual contact pages: 1–2. Actual full-resolution pages: 1–2. Receipt SHA256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

- BLOCKER, page(s) 1, 2: Pervasive retained OCR character spacing fragments source words into isolated letters and tiny groups across both pages, including the body, dating and subscription. Full-resolution reading is severely impeded and fails reader usability despite mechanical fidelity.
- QUALIFICATION, page(s) 1, 2: The long all-capital title fits and is identifiable, with retained OCR PAME in the display title. Page 2 preserves the historical dating and BENEDICTUS PP. XV; project rights text continues into the right column on that same page. No source-ending loss or apparatus-only terminal page was found.

### papal.benedict-xv.hf-ben-xv-enc-24111919-paterno-iam-diu

**PASS**. PDF: `.scratch/encyclical-classic/readers-fixed/1919-11-24-papal-benedict-xv-hf-ben-xv-enc-24111919-paterno-iam-diu-1bed8491-la/1919-11-24-papal-benedict-xv-hf-ben-xv-enc-24111919-paterno-iam-diu-1bed8491-la.pdf`. Actual contact pages: 1–2. Actual full-resolution pages: 1–2. Receipt SHA256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.

- QUALIFICATION, page(s) 2: Sparse p2 retains the end of the historical blessing, the 24 November 1919 dating clause and BENEDICTUS PP. XV above the apparatus. It is source-bearing and passes.

## Boundaries and limitations

Canonical source payloads were hashed and their opening/ending bounds were read; archive selections used the packet’s exact 1-based physical LF ranges (splitting only on LF, preserving form-feed semantics). Those starts/ends were compared with the rendered beginnings/endings and extracted PDF text. The visible source subscriptions and final notes are present in every assigned PDF. This was a boundary check, not complete verbal collation of any historical printing.

The receipt’s source-fidelity PASS is an existing mechanical result, not a new textual or rights certification by this reviewer. No original facsimile, restricted parent artifact, translation accuracy, doctrinal interpretation or rights determination was independently reviewed. Existing OCR and web transcription limitations remain. Recommendations to separate source notes or repair spacing require a new traceable derivative and a new PDF review; they do not authorize rewriting the pinned source bytes.

PASS is limited to the exact hashes above and the full page extent actually viewed. Three blocked readers must remain uninstalled pending repair and fresh review. The four passing readers have no visual blocker within this scope.
