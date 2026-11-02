# Baseline continuation 15 — cold visual review

Reviewed packet: `.scratch/encyclical-ready-package/baseline-review-packets/15.json`.
Canonical report destination: `src/sources/papal-documents/encyclicals-baseline-continuation-15.md`.

**Result: 7 PASS (29 pages), 1 CHANGES_REQUIRED (10 pages). All 8 PDFs / 39 pages were freshly inspected on their existing contact sheets; 26 pages were also opened at the original full raster resolution. No inherited inspection or acceptance is claimed.**

## Scope and verification

The applicable workspace/repository instructions, personal guidance, `guidance/papal-documents.md`, the PDF requirements in `guidance/repository.md`, the common review brief and `tmt.json` were read. Only this lane’s scratch directory was written. No shared raster/cache, PDF, source, manifest, release or tracked file was changed.

All 289 pin/count/size/equality checks passed: exact PDF hashes and `pdfinfo` page counts; receipt hashes and exact receipt-row bindings; source payload hashes; segment-manifest hashes where present; frozen-manifest hashes and exact source rows; all source-controller record hashes and available payload hashes; raster-manifest hashes; raster-cache PDF/page bindings; and every cached page, contact-sheet and thumbnail hash/size. The restricted parent artifacts have no packet payload paths; only their pinned controller records were verified. The check ledger is `.scratch/encyclical-baseline-continuation-15/pin-checks.json` (SHA-256 `c9a2ce0cba0f9878d5a1fbfdc769257894d691c81dbe57712afb6f400bebac8c`).

Shared exact pins:

- Receipt: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
- Frozen manifest: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.
- Raster manifest: `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`.
- Common brief: `ba9dcb643e6a8110382ac1080ff8f70d51b3ebca892d2efca45bd91bec0f6913`.
- Render revision: `2026-10-30T02:56:48Z`.

`pdfinfo`, `pdffonts` and `pdftotext` opened all eight PDFs successfully. The PDFs are unencrypted Letter pages, with embedded, subsetted Unicode Latin Modern fonts. Metadata identifies each work/issuer/language. This was not a separate low-level PDF structural validator run. Source opening/ending windows were read from the retained payloads using literal LF indexing for physical ranges and compared with the PDF openings/closings. This establishes no observed ending loss within the selected source, not full-work collation.

## Exact PDFs and fresh inspection coverage

| ID / language | Pages | Contact-sheet pages actually viewed | Full-size pages actually viewed | Status |
| --- | ---: | --- | --- | --- |
| `acta.ass.032.ass-032-l07351` / fr | 10 | 1–10 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 | CHANGES_REQUIRED |
| `papal.pius-xi.hf-p-xi-enc-19260228-rerum-ecclesiae` / la | 8 | 1–8 | 1, 8 | PASS |
| `papal.pius-x.hf-p-x-enc-11061905-il-fermo-proposito` / la | 6 | 1–6 | 1, 6 | PASS |
| `papal.pius-xi.hf-p-xi-enc-19280908-rerum-orientalium` / la | 5 | 1–5 | 1, 5 | PASS |
| `acta.ass.007.ass-007-act-015` / la | 3 | 1–3 | 1, 2, 3 | PASS |
| `gregory-xvi-acta.volume-01.line-00002526` / mul | 3 | 1–3 | 1, 2, 3 | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-14` / la | 3 | 1–3 | 1, 2, 3 | PASS |
| `papal.benedict-xv.hf-ben-xv-enc-01121918-quod-iam-diu` / la | 1 | 1 | 1 | PASS |

Each contact sheet is `contact-sheets/sheet-001.png` in that document’s exact packet `raster_dir`; full-size views used its existing `pages/page-N.png` files (two-digit N for the ten-page French reader). Every first/final page and every note-bearing, sparse or otherwise suspicious page was opened full size. The remaining ordinary interior pages were inspected on the contact sheets. No previous reviewer’s page claims or verdicts were counted.

## Document findings and source pins

### Depuis le jour

**CHANGES_REQUIRED** — `acta.ass.032.ass-032-l07351` (fr), 10 page(s).

- PDF SHA-256: `121d3af19d1fe96a277cfef59aa9295f675d86b81bd4c7f1e49710374c05e137`.
- Source payload SHA-256: `c2a09d45aed9009c095cfb732c38a125326abfd7577ad6ebe04bafba37efcfc4`.
- Segment-manifest SHA-256: `f9daa589e0b0e9dd58d526576ae5e278dc0fcca8487f82cb1a52a7012ec67001`.

PDF: `.scratch/encyclical-classic/readers-fixed/1899-09-08-acta-ass-032-ass-032-l07351-44547493-fr/1899-09-08-acta-ass-032-ass-032-l07351-44547493-fr.pdf`.

**Blocking finding, pp5–6:** Historical reference notes are fused into source-body paragraphs. On p5 left, the paragraph ending in “se corn-” continues directly into “Ci) 18 Nov. 1893.” and the Genus interpretandi note before body continuation “pose” in the right column. On p6 left, “aux droits” runs directly into “(1) O Timothee, depositum custodi…” and the Zelus animarum note; on p6 right, “son Père,” runs directly into “(1) Importabilis siquidem…” and the Divinum quippe note. The generated body confirms that each note set shares its preceding body paragraph without a separating paragraph boundary. These are substantive reading-order/usability failures despite exact retention of OCR words. Partition the identified notes into source-grounded separate blocks, preserve the literal wording and source order, then rebuild and review the changed PDF.

The earlier reference sets on pp1–4 and separate blocks on pp7–9 are distinguished from the blocking fused sets on pp5–6. Separate source-note paragraphs can interrupt body sentences under the governing profile; that fact alone was not classified as fusion. The French body is ragged right as required for non-English/non-Latin text. Numerous retained OCR hyphen/space and glyph errors remain visible. P10 retains the closing blessing, 8 September 1899 dating, LEO PP. XIII subscription and final II Cor. V, 20 note before its colophon.

### Rerum Ecclesiae

**PASS** — `papal.pius-xi.hf-p-xi-enc-19260228-rerum-ecclesiae` (la), 8 page(s).

- PDF SHA-256: `e393fe956bfcca86db94152df150cfe385253803fe66548a51070baae3f8532a`.
- Source payload SHA-256: `482bb54a7c78229761d28e72ecadeacb6c96b6d89e4f5d3a67885e7a29719184`.

PDF: `.scratch/encyclical-classic/readers-fixed/1926-02-28-papal-pius-xi-hf-p-xi-enc-19260228-rerum-ecclesiae-d7eee9bb-la/1926-02-28-papal-pius-xi-hf-p-xi-enc-19260228-rerum-ecclesiae-d7eee9bb-la.pdf`.

The final page retains the 28 February 1926 dating, PIUS PP. XI subscription and all twenty numbered reference-note blocks. Notes remain individually addressable and separate from the project colophon. The web transcription contains literal spelling/space anomalies; visual acceptance does not certify them.

### Il Fermo Proposito

**PASS** — `papal.pius-x.hf-p-x-enc-11061905-il-fermo-proposito` (la), 6 page(s).

- PDF SHA-256: `8b6037d77e5de8881491b371783638a30b656099ebcb7bfeb1f2e42abcf8f081`.
- Source payload SHA-256: `9d47c227ccdaf9a12da32072f09125825f5b373c24875c4d4027bbf6f1c43b24`.

PDF: `.scratch/encyclical-classic/readers-fixed/1905-06-11-papal-pius-x-hf-p-x-enc-11061905-il-fermo-proposito-15fdd030-la/1905-06-11-papal-pius-x-hf-p-x-enc-11061905-il-fermo-proposito-15fdd030-la.pdf`.

The final page retains the 11 June 1905 Pentecost dating and PIUS PP. X subscription. The colophon explicitly identifies this as a historical Latin translation of the Italian act. Literal retained anomalies, including the separated “commodu m” on p6, remain readable but are not corrected or certified by this review.

### Rerum Orientalium

**PASS** — `papal.pius-xi.hf-p-xi-enc-19280908-rerum-orientalium` (la), 5 page(s).

- PDF SHA-256: `1e15491449f095820c43957d52430725ecd38a0e49bb9e32411e4284787e119f`.
- Source payload SHA-256: `59210881c709f110b971aaf8c01210d51a72c7777f81efcd7b80d3e4ff59f914`.

PDF: `.scratch/encyclical-classic/readers-fixed/1928-09-08-papal-pius-xi-hf-p-xi-enc-19280908-rerum-orientalium-a3774d84-la/1928-09-08-papal-pius-xi-hf-p-xi-enc-19280908-rerum-orientalium-a3774d84-la.pdf`.

The final page retains the 8 September 1928 dating, PIUS PP. XI subscription and seven separate reference-note blocks. No note/body fusion or loss of terminal notes was observed. The web transcription remains uncollated.

### Vix dum a Nobis

**PASS** — `acta.ass.007.ass-007-act-015` (la), 3 page(s).

- PDF SHA-256: `4eb9c5a044c870e45f7526dac7f69bc6e8b8b9ae43ba64b26a90bf03a25892c1`.
- Source payload SHA-256: `5b64eabc613113dd83fb03b0798d99c1644d274f3a8d6482cdd97b803624f03d`.
- Segment-manifest SHA-256: `074e9c70454eed6524e3376ac8432b58d1777f8d7bfbdcf4aeb24633cf3b7968`.

PDF: `.scratch/encyclical-classic/readers-fixed/1874-03-07-acta-ass-007-ass-007-act-015-6cbf9cd3-la/1874-03-07-acta-ass-007-ass-007-act-015-6cbf9cd3-la.pdf`.

Notes on pp1–3 are separate paragraphs, although their retained source order can interrupt a sentence; generated paragraph boundaries corroborate the visual separation. The Psalm, Motivorum Expos., S. Thom./S. Anselm. and terminal reference sets were inspected. Spaced letters, hard word divisions and OCR note-marker anomalies are conspicuous but the source paragraphs and references remain readable. The 7 March 1874 dating and PIUS PP. IX subscription are present.

### Ad universos subditos ditionis Pontificiae cum gratiarum actione erga augustum Austriae imperatorem Franciscum I. .pro praestito. auxilio ?.

**PASS** — `gregory-xvi-acta.volume-01.line-00002526` (mul), 3 page(s).

- PDF SHA-256: `c75b1ef2315582220c765f97752d64c24a0ca3026ba9e37114af88ecd0aa8ce4`.
- Source payload SHA-256: `cdd5664e1012a3cec8d36ccb9c3921e61ee2ddbfc15158fe6cbf290ef907f619`.
- Segment-manifest SHA-256: `302624a689aab10fda4b879604aaecc0f819dfa2874752b6f79a579af0d9d62a`.

PDF: `.scratch/encyclical-classic/readers-fixed/1831-04-05-gregory-xvi-acta-volume-01-line-00002526-bbccadba-mul/1831-04-05-gregory-xvi-acta-volume-01-line-00002526-bbccadba-mul.pdf`.

The witness has a Latin title/protocol and dating with an Italian body, correctly identified as multilingual. P1 retains its own “2 Ex Bullario Romano.” citation as a separate paragraph, not fused into body text. The very long retained title leaves “?.” alone on its last title line; this is awkward but does not conceal identification or clip text. Rough OCR includes stray bars, punctuation and damaged words on pp1–2; despite that friction the body remains followable. P3 is sparse but contains the genuine concluding blessing and Latin 5 April 1831 dating before compact source/rights apparatus; it is source-bearing and is not an apparatus-only page.

### Ubi Urbaniano — ad episcopos Poloniae et Russiae

**PASS** — `pius-ix-acta.volume-03.line-00021313.part-14` (la), 3 page(s).

- PDF SHA-256: `3e7c9ec37c4a76f376da79055557954064b96700a68c6b356a18faa57fa525a5`.
- Source payload SHA-256: `3a788e20d82b5eb754d99242edaf43006aa915d8ebdfd9e1a62e73a1804e19f8`.
- Segment-manifest SHA-256: `ab023b32302c366cd6050e6ef1a5acd870970df0fa93603571eb722985ceffc7`.

PDF: `.scratch/encyclical-classic/readers-fixed/1864-07-30-pius-ix-acta-volume-03-line-00021313-part-14-ba2be848-la/1864-07-30-pius-ix-acta-volume-03-line-00021313-part-14-ba2be848-la.pdf`.

The Sapientia reference on p2 and Romans reference on p3 are separate note paragraphs. P3 separates the Romans note even where the original OCR source breaks a body word across that block; this preserves an identifiable source-note block and is qualified rather than treated as fusion. Retained OCR errors, including “Us Urbaniano” in the opening body, remain visible. P3 retains the 30 July 1864 dating and nineteenth-pontificate-year line; the source has no further subscription within the selected ending. The colophon starts at the lower left and has a short continuation at the upper right on that same source-bearing page, with no clipping or extra page.

### Quod Iam Diu

**PASS** — `papal.benedict-xv.hf-ben-xv-enc-01121918-quod-iam-diu` (la), 1 page(s).

- PDF SHA-256: `1db701fa8f02c777f3049019c5536145506f873e36448359887ae50a2be09447`.
- Source payload SHA-256: `bca1346ff2970f388fa3f3d5420719e7da9781e16417e0f699ce239a3d9e7a51`.

PDF: `.scratch/encyclical-classic/readers-fixed/1918-12-01-papal-benedict-xv-hf-ben-xv-enc-01121918-quod-iam-diu-068b3abc-la/1918-12-01-papal-benedict-xv-hf-ben-xv-enc-01121918-quod-iam-diu-068b3abc-la.pdf`.

The single page retains the full visible close, 1 December 1918 dating and BENEDICTUS PP. XV subscription, followed by a compact separated colophon. The right column is shorter than the left; it contains genuine source text and does not create an apparatus-only page.

## Overall layout disposition and limits

The readers use the requested restrained classic two-column design. Column sequence, title/issuer/date/language identification, text margins and line spacing were visually coherent. No significant clipping, overlap, collision, concealed heading, empty source-ending page or project-apparatus-only page was observed. The genuine sparse ending in the Gregory XVI reader is explicitly qualified above. Latin justification and the ragged-right French/multilingual settings remained readable. Historical OCR word divisions and note markers were not silently corrected.

The blocking decision is confined to the paragraph-level source-note fusion actually confirmed on Depuis le jour pp5–6. Separate source-note blocks elsewhere are permitted by the papal profile and were not failed merely because source order places them between body fragments. The French reader’s exact bytes must not be installed as PASS evidence without resolving those fused sets and reviewing the replacement bytes.

Cold visual/layout review of the exact packet bytes; no whole-source verbal or facsimile collation, new rights determination, translation certification, source correction, rebuild, raster generation, installation or installed-mirror comparison. Previously recorded inspections were not reused. Restricted parent payloads were not acquired; their pinned controller records, and all available tracked payloads, were verified.
