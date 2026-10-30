# Independent classic encyclical visual and source-repair review — packet 19

Outcome: **PASS for all 5 exact PDFs, 19 pages.** Every page was inspected both on the helper-generated contact sheet and separately at full resolution. No page review was reused. This accepts the inspected layout and the bounded repair invariants below; it does not certify historical wording, OCR accuracy, translation, rights, or whole-source completeness.

The five PDF SHA-256 values, page counts, and two receipt SHA-256 values match packet 19. Each helper raster cache identifies those same PDF bytes; all 43 listed page, thumbnail, and contact-sheet file hashes were checked. The lane did not regenerate rasters or alter a PDF, retained source, manifest, release, or tracked file. Its durable outputs are confined to `.scratch/encyclical-page-review-19/`.

## Exact reviewed artifacts and actual coverage

| Title | Language | PDF pages | Contact-inspected pages | Separately opened full-size pages | PDF SHA-256 |
| --- | --- | ---: | --- | --- | --- |
| Spesse volte | it | 4 | 1, 2, 3, 4 | 1, 2, 3, 4 | `a0dba0fee44e79bc0836f27bde1f488c30bdef0a6b29fe5f7bfe2b8856b4251e` |
| Saepenumero | la | 5 | 1, 2, 3, 4, 5 | 1, 2, 3, 4, 5 | `eeb24e5c08f8bb15469d60d03d97390f20aada9864a2e8f9118200f595518573` |
| Diuturni temporis | la | 2 | 1, 2 | 1, 2 | `7610dd2732c557e4c49063abaa6de232247503925c3acfd1505a7ac62701d046` |
| Respicientes ea omnia | la | 5 | 1, 2, 3, 4, 5 | 1, 2, 3, 4, 5 | `d41c0a4c00042619528b9aa67836e6b4a63e41b17ef213b8216af5994ae31b71` |
| Epistola encyclica de patrocinio S. Iosephi (Quamquam pluries) | la | 3 | 1, 2, 3 | 1, 2, 3 | `e470b6eefdb82041a8483a6de03b6de4ac23f54f3f67bb745dbac54dea080d37` |

Spesse volte, Saepenumero, and Diuturni temporis use receipt `.scratch/encyclical-spacing-02/readers/receipt.json`, SHA-256 `526b128f0787ea2694f84a3cb782920bbb9a084bb153c87ae020410076f04149`.

Respicientes and Quamquam use receipt `.scratch/encyclical-geometry-margins/simple-readers/receipt.json`, SHA-256 `824d24cdc7affde12ac8b1357b18d697f248ae3fc196d223008f00018b737e5e`.

The canonical destination for these exact report bytes is `src/sources/papal-documents/encyclicals-classic-visual-19.md`. The coordinator owns that copy and any installation.

## Visual findings

All five readers identify issuer, date, title, and language before the source text. The two-column order is clear, with adequate gutters and margins, regular leading, and legible paragraph indents. Latin is justified; Italian retains its intended ragged-right composition. Titles and source headings are not isolated from their text. No clipping, column collision, overlap, materially unreadable spacing, or apparatus-only page was observed. The short rule, smaller type, and Source label separate the terminal project apparatus from the historical text. Literal hard-line hyphens, OCR glyph errors, and source-spaced letters or numerals remain conspicuous qualifications.

### Spesse volte — PASS

ID: `acta.ass.031.ass-031-l05065`.

All four pages are legible. The native spacing projection preserves visible source hyphen-plus-space fragments, including mid-line broken words, rather than silently reconstructing words. Page 4 retains the source blessing, 5 August 1898 dating, and LEO PP. XIII subscription before the ruled apparatus. The apparatus correctly identifies the following Latin witness as a language version of the same act. No historical note block occurs in this bounded constituent.

PDF: `.scratch/encyclical-spacing-02/readers/1898-08-05-acta-ass-031-ass-031-l05065-80790b50-it/1898-08-05-acta-ass-031-ass-031-l05065-80790b50-it.pdf`.

### Saepenumero — PASS

ID: `acta.ass.031.ass-031-l05416`.

The Versio Latina heading remains explicit. Literal hard-line hyphens and OCR fragments reduce reading comfort but do not create unreadable spacing. Page 5 is very sparse, with source continuation of the blessing, the dated closing, and LEO PAPA XIII subscription above the apparatus. It therefore has genuine source-bearing coverage. No historical note block occurs in this bounded constituent.

PDF: `.scratch/encyclical-spacing-02/readers/1898-08-05-acta-ass-031-ass-031-l05416-2f53cac9-la/1898-08-05-acta-ass-031-ass-031-l05416-2f53cac9-la.pdf`.

### Diuturni temporis — PASS

ID: `acta.ass.031.ass-031-l05804`.

The citation pair on reader page 1 and the short `(i) vii, li.` note on reader page 2 remain distinct indented historical blocks at their source-page-break positions. They interrupt continuing source sentences but are not fused into body paragraphs. Page 2 retains source body, blessing, 5 September 1898 dating, and subscription before the project apparatus. The receipt records one `Underfull \hbox (badness 1502) in paragraph at lines 13--27`; both pages and that opening paragraph were inspected full size, with no material spacing defect. This warning is visually disposed, not suppressed or represented as absent.

PDF: `.scratch/encyclical-spacing-02/readers/1898-09-05-acta-ass-031-ass-031-l05804-45da69ef-la/1898-09-05-acta-ass-031-ass-031-l05804-45da69ef-la.pdf`.

### Respicientes ea omnia — PASS

ID: `acta.ass.006.ass-006-act-006`.

Seven historical note groups remain separate indented blocks on reader pages 1, 3, 4, and 5. The historical editor's note on reader page 1 is separate from both interrupted body continuations. Its retained Redactoris ephemeridum wording and the explicit final source note distinguish it from papal authorship. Source-spaced numerals and OCR errors remain literal and legible. Page 5 retains substantive continuation, blessing, dating, PIUS PP. IX subscription, and the final historical citation before the project apparatus.

PDF: `.scratch/encyclical-geometry-margins/simple-readers/1870-11-01-acta-ass-006-ass-006-act-006-e04f0918-la/1870-11-01-acta-ass-006-ass-006-act-006-e04f0918-la.pdf`.

### Quamquam pluries — PASS

ID: `acta.ass.022.ass-022-003`.

The source title, date, and issuer remain clear. Near the end of reader page 1's left column the inherited source-page `con-` / `stantesque` division remains visible with a paragraph start; the excluded printer line is not interleaved. Page 3 retains substantial ending text, blessing, Roman-numeral date, and source subscription before the ruled apparatus. Source-spaced title letters and subscription numerals remain literal. No substantive historical note was removed by the inspected footer repair.

PDF: `.scratch/encyclical-geometry-margins/simple-readers/1889-08-15-acta-ass-022-ass-022-003-96238909-la/1889-08-15-acta-ass-022-ass-022-003-96238909-la.pdf`.

## Independent repair-method checks

These checks concern declared transformations over retained evidence. They are not a lexical collation or a claim that the Vatican OCR reproduces the original printing accurately.

### Native whitespace projection

For each of the three ASS 31 recipes, the parent, native raw, recipe, review, and complete line-map artifact hashes were checked. The current segment input pins and PDF receipt source hashes agree with the resulting artifact. Fresh `pdftotext -raw -enc UTF-8 -eol unix` extraction of the pinned native PDF page range equals each retained native raw artifact byte for byte.

An independent replay, without calling the projection helper, checked every selected nonblank source LF line for one unique same-page native raw line with the identical non-whitespace character sequence, preserved source line order and blank lines, substituted only the witnessed whitespace, and obtained the exact retained output bytes. Every row of each retained line map also independently matched its source/native line ordinals, line digests, and character count.

| Reader | Uniquely matched nonblank lines | Preserved non-whitespace characters | Output source SHA-256 | Recipe SHA-256 |
| --- | ---: | ---: | --- | --- |
| Spesse volte | 327 | 16881 | `dabaa680a417719522cc436ea2896f439ebe7554a760550507ceb07febc3df72` | `95b0469083714c0d3f851895df29d74e47e24a17ce82b188699a69ceb6288b45` |
| Saepenumero | 362 | 18523 | `4d9027d4c7526380ea59be5431c2ae40008ac3bfba7ba3de283945b3c95bdf68` | `42ec90ba53f1ddff178c92a24d1392d04f63bac7b6709cc8809f144bc8c39aef` |
| Diuturni temporis | 99 | 4893 | `8a446bb3909ffc387dca60392d9bd1ff8563675d67c941848f4bb362b767e118` | `df5e47d99b5ca02d054163255d315d9501c447d1d40a7a54f06a34e599bdd20b` |

All three current `tools/papal-native-spacing --check --json` replays pass. Their recipes identify original helper SHA-256 `c3f13e34101ea360aa9dafb3e6d92723c001ce4286bf32ef03e837597b68e41c`, while the current compatible helper has a later hash. The exact original implementation is retained at `src/sources/works/holy-see/acta-sanctae-sedis/editions/1890-acta-ass-023/artifacts/native-spacing-helper-c3f13e34101e/helper.py`. Its pinned hash was independently verified and its original replay returned exact output and line-map bytes for all three recipes. The historical/current helper difference is therefore resolved evidence, not an unreported failed pin.

Diuturni native stream-order differences are exactly pages 146 and 148. Inspection confirms that page 146's second heading line physically belongs below its first heading line, and page 148's note physically belongs at page foot. The projection retains the parent source order and does not adopt the raw stream's heading or note displacement. Native pages 147 and 148 confirm the historical citation-note membership and separation seen in the final reader.

### Respicientes LF-only note partitions

`tools/papal-source-notes check --spec ... --out ... --json` passes for retained spec SHA-256 `1077f202f2ec40acf0b936d5f584497766d989fd29c5526d54f671d979a0ae3e` and output SHA-256 `32d50100759b4f049394641479ad07dce3440858cf260ee43230f6648f06e011`. The parent hash is `6f710d76d851369aa5ea49b7fefa65c2279ee93cf1c54f3555e5365f4fbb628a`.

An independent check selected the exact parent ranges and removed only LF bytes for comparison. All other bytes and their order are equal; the resulting non-LF SHA-256 is `e88fb89aacbf07e80a996b920f3b32e23bc7089e46577a958b267e31a7f377e6`. The seven note ranges are physical LF 5348; 5386–5388; 5508; 5548; 5628; 5668; and 5703. Native source pages 136, 137, 140, 141, 143, 144, and 145 were opened full size to check their page-foot membership, including the explicit historical editor attribution on page 137. No note was removed, reordered, rewritten, or assigned an invented anchor.

### Quamquam printer-footer exclusion

The exact parent hash is `5f0e20783cd07f688f4350856fa7cbd858954a5d0a33895e8b22b53cb8aacfe0`. Independent replay of parent physical LF ranges `[[2439,2478],[2481,2520],[2522,2561],[2563,2602],[2604,2627]]`, joined by the declared LF separators, returns the exact output SHA-256 `facb122cf837ad6960a4e2bdd17c40cad75a24a35d2026006c5366ecda1f985c` bound by the receipt.

Relative to the predecessor's retained ranges, the only removed source line is physical LF 2479: the separately positioned small printer/fascicle line beneath the native page 65 body. Native pages 65 and 66 were opened full size; page 65 ends its substantive text with `con-`, page 66 continues `stantesque`, and the excluded line is visually distinct publishing furniture. The dated closing and subscription remain visible in the final reader. This is a bounded furniture exclusion, not correction of source words.

## Native evidence and other checks

The native parent PDFs were verified at SHA-256 `4c1f67a32e35808f32bcee788ff380bd8bafc954e854a441be99be58dc1a9eb9` (ASS 31), `7e480931ad07d3a53db391d2c26a69a256ca106719d0e7a6220415d3123eecca` (ASS 6), and `4b4d61704f24df83e706494d81c7c0cfb554ca06f80755bc083fa26a3e9204ec` (ASS 22). The existing review excerpts have identical per-page `pdftotext -bbox` sequences to their pinned parent page ranges. Their cache PDF hashes and every listed raster hash were checked without rerendering.

Native source pages actually opened full size in this lane were ASS 31 pages 129, 137, 146, 147, 148, and 149; ASS 6 pages 136, 137, 140, 141, 143, 144, and 145; and ASS 22 pages 65 and 66. These 15 native page views are additional to the 19 final-reader full-size views. The lane does not claim to have visually inspected any other native source page.

`pdfinfo`, `pdffonts`, and raw text extraction succeeded for all five final PDFs. Titles, authors, language subjects, page counts, and revision-derived creation/modification timestamps agree with their identification and receipts. All enumerated fonts are embedded, subsetted, and have Unicode maps. PDF information reports no encryption, JavaScript, forms, or suspect structure. The receipts' source-fidelity checks report PASS; this lane did not rerun the generator's full PDF/source fidelity algorithm. `qpdf` was unavailable, so no `qpdf --check` result is claimed.

Machine-readable evidence is retained beside this report in `reviews.json`, `verification.json`, `preflight.json`, `observations.json`, `source-replays.json`, `native-evidence.json`, and `pdf-structure-metadata.json`. The bounded local audit script is `audit.py`.

## Limits

All 19 final-reader pages were actually inspected at both contact and full-page scale. No earlier PDF version is accepted by this report, and no review page or proof is reused. Native evidence is the Vatican archival OCR reconstruction, not original-print facsimile evidence. No word reconstruction, lexical correction, translation equivalence review, whole-source collation, independent rights determination, or source-library evidence-state promotion was performed. No AI translation was created. There are no unresolved layout or repair-invariant blockers in this packet; source OCR and literal hard-line hyphen limitations remain visible and disclosed.
