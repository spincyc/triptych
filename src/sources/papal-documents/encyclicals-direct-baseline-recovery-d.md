# Direct baseline recovery review D

2026-10-30. Independent cold review of exactly two Latin readers and nine reader pages. Canonical integration target: `src/sources/papal-documents/encyclicals-direct-baseline-recovery-d.md`. The actual immutable report is delivered from the isolated scratch lane; the coordinator owns canonical integration.

## Scope and result

**PASS: both exact packet editions**, subject to the explicit selected-witness limitations below. These are normalized Vatican web transcriptions, not the archival/note-repaired readers of the same works. Neither shared incipits nor prior review coverage were used as acceptance evidence. All nine reader pages were opened individually at their original raster dimensions; no inherited page inspection or contact-sheet-only review is counted. No blocking source-ending loss, note/body fusion, clipping, overflow, missing glyph or material whitespace unreadability was found.

Each reader visibly states: “Uncollated normalized web transcription; source wording and numbering retained apart from the explicitly recorded corrections and apparatus exclusions.” That scope controls the judgment. This review does not silently replace the selected web witness with AAS wording, salutations, subscriptions, punctuation or page-foot citation style. The existing affirmative historical distribution basis and exact exclusions were inspected as repository evidence; no new legal assessment is claimed.

## Exact identity and checks

Packet SHA-256: `c13eb42b6f645fd2a2a16afe35d2cfc134a6d39900d8d9b9547d1969fffe7da7`.

Shared frozen manifest: `.scratch/encyclical-classic/readers-fixed/frozen-manifest.json`, SHA-256 `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`. Shared receipt: `.scratch/encyclical-classic/readers-fixed/receipt.json`, SHA-256 `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`. Raster run manifest: `.scratch/encyclical-classic/visual-fixed/review-run.json`, SHA-256 `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`. Render revision: `2026-10-30T02:56:48Z`.

For each (id, language), exactly one complete matching frozen-manifest source row equals packet `source_row`, and exactly one complete receipt document equals packet `receipt_row`; all fields were compared, not a subset of pins. PDF, normalized payload, all four source-controller record pins, declared tracked payloads, raster-run identity, and every existing cache-manifest file hash and size match the packet. There are no segment selections or segment-manifest pins for either input.

Fresh checks called `validate_document(row, Path.cwd())` then `pdf_body_fidelity(Path(pdf), validated, pages)` from `scripts/_typeset_papal.py` with `PYTHONDONTWRITEBYTECODE=1`. Both independently returned the exact receipt fidelity object under `pdf-raw-source-aware-line-hyphen-nfkc-v3`, covering every source character through the final page. Unicode compatibility/whitespace normalization and source-aware line hyphens are the declared allowances; this is not a correctness check of source Latin.

`/usr/bin/pdfinfo`, `/usr/bin/pdffonts`, and complete `/usr/bin/pdftotext -layout` plus `-raw` checks exited 0 for both PDFs. Both are unencrypted letter-size PDF 1.7, zero rotation, with correct title, Benedict XV author and Latin subject; no JavaScript, forms or suspicious structure was reported. Creation/modification metadata convert to the pinned UTC revision. All four font subsets in each PDF are embedded CID Type 0C Latin Modern Roman with Unicode mappings. The title uses LMRoman17; body LMRoman10; terminal apparatus LMRoman8 regular/bold. Layout and raw extraction, cross-checked against the full-page views, preserve left column then right column and normal page progression.

The entire final `.log` and both `.pass-1.txt` / `.pass-2.txt` files were scanned for fatal errors, undefined references, missing characters, overflow and warnings. All six report completed output. First-pass page-label/reference rerun notices settle on pass 2. Praeclara has no final warning. In Hac has only the three underfull source-title lines listed below; no fatal, undefined, missing-character or overfull diagnostic was found. No recompilation was performed.

## In Hac Tanta — PASS

- Identity: `papal.benedict-xv.hf-ben-xv-enc-14051919-in-hac-tanta` / `la`.
- PDF: `.scratch/encyclical-classic/readers-fixed/1919-05-14-papal-benedict-xv-hf-ben-xv-enc-14051919-in-hac-tanta-cefcb450-la/1919-05-14-papal-benedict-xv-hf-ben-xv-enc-14051919-in-hac-tanta-cefcb450-la.pdf`.
- PDF SHA-256: `46d57e1a3022c68eec58d55992c8a858596b30e85bf051016fbe12669e7945ca`; 5 pages; 46385 bytes.
- Source: `src/sources/works/papal-documents/1919-05-14-papal-benedict-xv-hf-ben-xv-enc-14051919-in-hac-tanta-cefcb450/editions/2026-10-26-vatican-la/artifacts/latin-text-3f3e6239ce31/text.txt`, SHA-256 `3f3e6239ce31dbcdf7040f90ad8cb44b5cf289c1a887e7afdf784aae2962986f`.
- Artifact: `artifact.papal.benedict-xv.hf-ben-xv-enc-14051919-in-hac-tanta.2026-10-26-vatican-la.latin-text-3f3e6239ce31`.
- Official web delivery: https://www.vatican.va/content/benedict-xv/la/encyclicals/documents/hf_ben-xv_enc_14051919_in-hac-tanta.html.

Fresh fidelity: 24311 source characters; 21005 normalized characters; 159 layout hyphens; source begins on page 1 and ends on page 5.

| Controller record | Record SHA-256 | Recorded parent/payload SHA-256 |
| --- | --- | --- |
| `src/sources/works/papal-documents/1919-05-14-papal-benedict-xv-hf-ben-xv-enc-14051919-in-hac-tanta-cefcb450/editions/2026-10-26-vatican-la/artifacts/latin-text-3f3e6239ce31/artifact.toml` | `8beea48a78533466466c29c5a6a33f227675a6697fd0b39dbf36fbb383f12cd9` | `3f3e6239ce31dbcdf7040f90ad8cb44b5cf289c1a887e7afdf784aae2962986f` |
| `src/sources/works/papal-documents/1919-05-14-papal-benedict-xv-hf-ben-xv-enc-14051919-in-hac-tanta-cefcb450/editions/2026-10-26-vatican-la/artifacts/html/artifact.toml` | `d2081df7cf79f9dcd0bb94e20e72fcd6e877f68a9d07178250fccfcbe925e2cd` | `799660f680ce25250dc33c35cfe9acbbdf678232ae9dc6854fed80f98ea18612` |

| Reader page individually viewed | Observation |
| --- | --- |
| 1 | Compact identification and long source title are legible. The complete web salutation and opening begin on this page; no title-only page or clipping. The left-column ending appa- continues as rari in the right column. Retained source forms include de vinctam and the stray closing guillemet after acerbissimi. |
| 2 | Both columns read continuously. Page 1 ends maris and page 2 begins vias within the same sentence. Distinct indented paragraphs and [3]–[7] remain visible. Scattered web forms include quis/non, quant am, voluntat em, mandaci tum and poce puli; these do not create sustained unreadable body spacing. |
| 3 | Page 2 ends obedivit and page 3 begins its closing guillemet, completing that quotation. Notes [8]–[15] remain body anchors, with their text preserved in the final list. Retained localized forms include f amiliaritati, clerici catus, commence daret, noce stro and dispensatoci rem. No separate note has entered the body. |
| 4 | Page 3 ends Domi- and page 4 begins no, preserving Domino across the page break. Quotations and [16]–[19] are legible; the split volunt at um and ornee nipotens are retained web-source defects. Columns, margins and page number are clear, without overlap or repeated letter-by-letter spacing. |
| 5 | Page 4 ends le- and page 5 begins gatis. The three historical grants I–III, dating clause, BENEDICTUS PP. XV, and complete retained [1]–[23] reference list precede the ruled project apparatus. Column 1 ends utrius- and column 2 begins que. The source anchor mismatch described below is present; the page is fully source-bearing and not an apparatus-only tail. |

Findings:

- **low; page(s) 1, 2, 3, 4, 5** — Non-blocking selected-witness limitation: the exact uncollated web source retains localized spelling, quote and word-division defects, including de vinctam (p1), quis/non / quant am / poce puli (p2), noce stro / dispensatoci rem (p3), ornee nipotens (p4), and vestror um (p5). Full-size review found no sustained unreadable spacing, body/note fusion or missing rendering glyph. Corrections would require a separately identified derivative and fresh byte-bound review.
- **low; page(s) 5** — Non-blocking selected-witness reference-number anomaly: the Clement quotation uses body anchor [23] while its terminal reference is [22], and the final Boniface quotation uses [24] while its terminal reference is [23]. All 23 historical reference texts are present. Native AAS 220 and 221 identify the corresponding S. CLEM. ROM. and Ep. L references. The complete normalized source contains the same mismatch, and the reader expressly retains source numbering; this is not loss of a final note during typesetting.
- **low; page(s) 1** — Three final-pass underfull hbox diagnostics (badness 1596, 2903, 1412) concern the long source-title paragraph. Full-size inspection found the title readable and within both margins; no overflow or layout blocker remains.

Exact existing full-page raster hashes (all independently verified before viewing):

| Page | SHA-256 |
| --- | --- |
| pages/page-1.png | `42dc1160b64d6fa4b26dc26839d23ca4d161b15ada00ed2f138813a4cadc5f8b` |
| pages/page-2.png | `3e5f8cfd42e9c2f36d6ba1d5ed0eb42b440b42ffe3658eaa17729ffef24aa473` |
| pages/page-3.png | `e95a406a299bbe84942840aefabe88c646c1bfa7d56a89c98b7b43debd00e61c` |
| pages/page-4.png | `11666e15ef5d7f08bce682deb843ee8f36946f3e8b5d9523d972d838732317d6` |
| pages/page-5.png | `a77b30cdf6cb21433160689ca307992ca894603848b7d71b1c774a191de30b95` |

Build diagnostic file pins:

| File suffix | SHA-256 |
| --- | --- |
| .log / log | `ba1cef0e4879edd4f82f379f13d507e6d51f0956f9e64d4d67acb86c70e5090b` |
| .txt / pass-1.txt | `f1e3e7540d2c0a2918f419d56626d5a29aa58abcd0fc3f38daf49977e351158d` |
| .txt / pass-2.txt | `e4f24db718504fe778d390fef5fad3253fad30d64f2528a45726f02a697a7ec8` |

## In Praeclara Summorum — PASS

- Identity: `papal.benedict-xv.hf-ben-xv-enc-30041921-in-praeclara-summorum` / `la`.
- PDF: `.scratch/encyclical-classic/readers-fixed/1921-04-30-papal-benedict-xv-hf-ben-xv-enc-30041921-in-praeclara-summorum-05d26bb3-la/1921-04-30-papal-benedict-xv-hf-ben-xv-enc-30041921-in-praeclara-summorum-05d26bb3-la.pdf`.
- PDF SHA-256: `55de28632623853421c49359e1a175a75b9e0517b7ec1b6b8856b36eda82e3ad`; 4 pages; 38110 bytes.
- Source: `src/sources/works/papal-documents/1921-04-30-papal-benedict-xv-hf-ben-xv-enc-30041921-in-praeclara-summorum-05d26bb3/editions/2026-10-26-vatican-la/artifacts/latin-text-4954c60b5940/text.txt`, SHA-256 `4954c60b5940706adb895abd27fa3df5e2b5338e62160d6514121c37e0e4430c`.
- Artifact: `artifact.papal.benedict-xv.hf-ben-xv-enc-30041921-in-praeclara-summorum.2026-10-26-vatican-la.latin-text-4954c60b5940`.
- Official web delivery: https://www.vatican.va/content/benedict-xv/la/encyclicals/documents/hf_ben-xv_enc_30041921_in-praeclara-summorum.html.

Fresh fidelity: 15585 source characters; 13388 normalized characters; 71 layout hyphens; source begins on page 1 and ends on page 4.

| Controller record | Record SHA-256 | Recorded parent/payload SHA-256 |
| --- | --- | --- |
| `src/sources/works/papal-documents/1921-04-30-papal-benedict-xv-hf-ben-xv-enc-30041921-in-praeclara-summorum-05d26bb3/editions/2026-10-26-vatican-la/artifacts/latin-text-4954c60b5940/artifact.toml` | `04d7c6bc2c048545e4476ea1dc681d55d2b986d33f517fc862e26505c895bea5` | `4954c60b5940706adb895abd27fa3df5e2b5338e62160d6514121c37e0e4430c` |
| `src/sources/works/papal-documents/1921-04-30-papal-benedict-xv-hf-ben-xv-enc-30041921-in-praeclara-summorum-05d26bb3/editions/2026-10-26-vatican-la/artifacts/html/artifact.toml` | `4901b407253968ca3c7f208533aa978e8ff97a6c981a1e3c9010e0b0a054f75a` | `8e96c8ba6486498cfb19d3b815eac4de40aad3a806a5f522f7ccae2f13aa9054` |

| Reader page individually viewed | Observation |
| --- | --- |
| 1 | Title, Benedict XV, date and Latin are clear. The selected web heading and VENERABILES FRATRES salutation are retained. The left column ends poeticam lauream de and the right starts salutaris lavacri fonte. Source forms such as num quam and sedi simul remain localized. No clipping or column collision. |
| 2 | Page 1 ends universitatem and page 2 begins quoquo eius partes; the body continues normally. Anchors [1]–[7] are visible and their references remain separate in the terminal list. Forms such as gioria, Römern, falli neseium and dediti s simuim are literal source limitations, not missing glyphs or a note/body merge. |
| 3 | Page 2 ends quam and page 3 begins pius filius. The [8]–[9] anchors and final blessing are present. The columns continue vic- / tor within the Christus phrase. Retained tiusque and vemovere are localized transcription errors; there is no sustained nonsensical or fused body passage. |
| 4 | Sparse final left column contains the genuine Datum clause, BENEDICTUS PP. XV, and all nine historical references before the short ruled source/rights notice. The right column is empty. The final source text is substantive historical closing and notes, so sparseness alone is acceptable. |

Findings:

- **low; page(s) 1, 2, 3** — Non-blocking selected-witness limitation: localized source transcription errors remain, including num quam and sedi simul (p1), Römern / falli neseium / dediti s simuim (p2), and tiusque / vemovere (p3). The rendered pages are legible and faithful to the pinned normalized web source. No sustained nonsensical body, material whitespace unreadability, note/body fusion or missing rendering glyph was found.
- **low; page(s) 4** — Acceptable source-bearing sparse final page: genuine dating clause, signature and nine historical references remain before project apparatus. The empty right column is not a source-ending or completeness failure.

Exact existing full-page raster hashes (all independently verified before viewing):

| Page | SHA-256 |
| --- | --- |
| pages/page-1.png | `17ae48b1391dd70a0179c8a5309b2ab7a240f2798c637ee1e6619c8e3d5ee518` |
| pages/page-2.png | `61c51dc8dc81ae6a09d29368825ca8676136e6e697ade2af45c0a0506d5230a0` |
| pages/page-3.png | `d20f26888afd541b365064584ac6ad1570f71602713025ee4d0bd34ecda04296` |
| pages/page-4.png | `53e95e8786995e950fe4f3506d8b037e8d3c68feed48d70e5560ade6fb06b288` |

Build diagnostic file pins:

| File suffix | SHA-256 |
| --- | --- |
| .log / log | `3a501ffce55594ed837398835276a99053a62db9d8b18a0fd1e35d34eb8c7c58` |
| .txt / pass-1.txt | `fde962183bf511c4d3976db15605e7c309c89865501565f643be6773be37e182` |
| .txt / pass-2.txt | `9d2995be3cc3f615a98fe3bd40eb21d6cf463975362a999673d5775aaf86c499` |

## Native extent, endings and note ownership

Both complete native volumes were hashed against their controlling native artifact manifests and matching `publication-approvals.json` historical-witness pins **before** extracting pages or text. Whole-volume `pdftotext -layout` outputs were written only under this lane. Page numbers below are 1-based artifact pages; the AAS act bounds correspond to the nominal printed bounds 209–221 and 209–217. OCR headers/page digits contain errors and are not treated as independent dating evidence.

| Native complete PDF | Whole SHA-256 | Bytes / artifact pages | Controller record SHA-256 | Individually viewed native pages |
| --- | --- | --- | --- | --- |
| `.scratch/papal_early_review/AAS-11-1919-ocr.pdf` | `6d5c93f73af4538f8023be5447c046a5f4c3f97397c90fcda387026bfac446ad` | 2358367 / 536 | `afe9790c4801b87a49f720a646c732425a9d361c2c61b391bd8d2c0463558f50` | 209, 211–217, 219–221 |
| `.scratch/papal_early_review/AAS-13-1921-ocr.pdf` | `f3bb05e86347a392ba44e9c92bcda9663e82b79e9c72676b57a5ad7b11e93a03` | 2731780 / 631 | `c539ff6c2579ee00190185584a98f8fa292acf932cb764058e832d068276d00a` | 209, 212–214, 217 |

The controlling records are under `src/sources/works/holy-see/acta-apostolicae-sedis/editions/1919-acta-aas-011/artifacts/vatican-pdf-6d5c93f7/artifact.toml` and the corresponding `1921-acta-aas-013/artifacts/vatican-pdf-f3bb05e8/artifact.toml`. The retained source URLs and exact exclusions agree with the selected text identities. In Hac’s excluded modern web bibliography mislabels the historical volume as AAS X (1918); the selected reader cites AAS XI (1919), matching the approval record and the bounded act closing.

Native bounded PDFs were extracted with `/usr/bin/pdfseparate -f P -l P` into `native-pages/`, then rendered only by `tools/pdf-review --output .scratch/direct-baseline-recovery/child-d/native-rasters --cache .scratch/direct-baseline-recovery/child-d/native-cache --jobs 1` with those extracted PDF arguments. Helper exit 0; its durable command output is `native-raster-command.txt`. No shared output/cache or raw parallel raster command was used. Native views were single full-page images; all 16 selected native pages were individually opened. They are OCR reconstructions, so image-level claims about the original printing remain outside scope.

For **In Hac**, native 209 gives the act title/address, opening and II Cor. reference. Native 211–217 supply the Colossians, Willibald, Boniface-letter and patristic notes corresponding to reader [2]–[18]; 219 has Othlono, 220 has Boniface XXXIX/Ibid./Clement, and 221 has Ep. L. These are historical internal references, not the excluded modern bibliography. All are represented in the reader’s retained final list. The original native page-foot presentation and the web’s terminal reference list differ openly.

Both-side checks resolve concrete interruption ownership: native 212 ends the body at ut narrantem se- and 213 begins quamur eiusdem aetatis scriptorem before its own page-foot notes; the reader’s p2 retains that continuous body. Native 213 ends the paragraph at continuatam., then three distinct notes; 214 starts Nam et ipsi Romani Pontifices. Reader p2 retains a paragraph boundary before Nam et ipsi and keeps those references in the terminal list. Native 216 ends body ceteris etiam, then its two notes; 217 starts omnibus, quos per Evangelium genuisset and finishes that paragraph at videretur., followed by Ita enim. Reader p3 retains the complete continuous sentence and boundary before Ita enim, without inserted note text. Native 220 ends the body lead-in Atque utinam ... in terris:, then three references; 221 starts quantoscunque ... non cesso, followed by the distinct Huius interea paragraph, grants I–III, actual date clause and subscription. Reader p5 retains all of those elements. The final Ep. L note is genuine; the [24]/[23] mismatch is selected-source numbering, not a dropped note.

For **Praeclara**, native 209 identifies the act/addressees and opening; the selected web salutation differs from the native dilecti filii form, which is an edition difference within the disclosed scope. Native 212 has Mon. III,4 / Mon. III,3,16 / Conv. II,9; 213 has Mon. III,3 / Epist. VIII; 214 has Mon. III,16 / S. Leo / Mon. III,3; 217 has Epist. X, §15. These account for all nine retained terminal references. Native 212 ends quibus Chri-, then notes; 213 resumes stum interfuisse ... and completes the passage through degustavit before the distinct Ecclesiae vero paragraph. Reader p2 retains Christum and the complete surrounding passage, then its Ecclesiae vero paragraph; reference text is separate on p4. Native 213 ends Romano Pontifici non, then notes; 214 begins subiaceat ... ordinetur and completes Optima ... uberrimos before At in Summos Pontifices. Reader p2 retains both the continuous quotation and the later At in Summos paragraph boundary. Native 217 and reader pp3–4 retain the final blessing, real date/subscription, and last historical note. None of these native note interruptions supplies evidence of body/note fusion in these selected readers.

## Limits and disposition

- Normalized Vatican web wording and reference numbering are intentionally retained. This PASS covers faithful, legible rendering of that exact selected uncollated witness; it does not certify a corrected Latin text, the AAS paragraphing, or original-print glyphs.
- The official AAS -ocr.pdf is an OCR reconstruction, not an original-print facsimile. Native visual checks are bounded to the explicitly listed pages and establish extent, note ownership and examined boundaries, not full lexical collation.
- Restricted HTML parent payload bytes were not independently opened; their controlling artifact records and exact recorded hashes were checked. The normalized tracked payloads, complete reader PDFs and native comparison volumes were hashed directly.
- No build, source repair, canonical record, installation, release change, Git mutation or external publication was performed. Existing reader rasters were read-only; new native extracts and review artifacts are confined to this lane.

PASS applies only to the exact `(id, language, PDF SHA-256)` tuples above. Every reader page is freshly inspected; reused pages and reuse proofs are empty. There are no blocking findings, pending tools, lost operations or live child processes. No generic ZIP handoff was created because this delegated task explicitly uses an isolated scratch report/result lane; its coordinator owns integration and acceptance.
