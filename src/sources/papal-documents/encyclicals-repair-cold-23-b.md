# Independent repair acceptance: packet 23-b

Reviewed 2026-10-30. Result: **4 PASS, 24 reader pages, no blockers**.
Every actual reader page was inspected individually at the existing raster's original resolution and in its contact overview. No pages or prior author PASS decisions were reused. The report's canonical destination is `src/sources/papal-documents/encyclicals-repair-cold-23-b.md`.

This is independent reader usability and bounded source-boundary/repair acceptance. It does not certify lexical OCR accuracy, original-print glyphs, translation equivalence, rights, whole-volume completeness or exhaustive discovery. The native Vatican PDFs are OCR reconstructions. Their images establish the inspected reconstruction geometry, not original-print facsimile collation.

## Exact reader pins and coverage

### `acta.aas.018.aas-018-l06278` (la) — PASS

PDF: `1dec676b7156442427f2a87844acf5b5a401f7d1b8947ca9e333b7329031db86`. Actual pages: 9; contact overview and individual full-size inspection: 1, 2, 3, 4, 5, 6, 7, 8, 9.

Receipt: `4454ea328b884a827e03e14581afc289db1110222a4e0baee89cd01a91ae50f6`. Frozen manifest: `ba24b3e9b660927e6bbfe85aa4e8bdbc910caa790ee5faaec27e977297e27f95`. Source payload: `92195a739059200e7596d81b233810be05248944fab52dd4880b963dc5284c17`.

Long literal OCR title remains readable; wide gutter and unclipped columns. Citation notes on pages 2–8 are distinct indented paragraph blocks at historical source breaks, sometimes interrupting a divided body word. Inherited internal hyphens, scattered letterspacing and OCR glyphs reduce polish but no sustained unreadability. Page 9 sparse yet contains blessing, dated clause and PIUS PP. XI subscription above ruled apparatus.

### `acta.aas.006.archive.aas.006.053` (it) — PASS

PDF: `9518b69b215ed3114cfff232af5d237c005aaaab97907229bba26974028a5dde`. Actual pages: 7; contact overview and individual full-size inspection: 1, 2, 3, 4, 5, 6, 7.

Receipt: `1605bbe0138ca0f719c6696a4039b12fa18ef89cef6eeffc4db752096f0cecef`. Frozen manifest: `da4d599533113646545b2835de7cbca9cc8aff14c94ce154e2b1ca95e99df27d`. Source payload: `29ba2464005ce41c9eca081201cc5f64d8a5ac546856eed9ed016d541fa70792`.

Ragged-right Italian columns remain legible and ordered. All note groups appear as distinct short line/paragraph blocks, including page 3 top and page 7 top and above subscription; source hard-line divisions and OCR punctuation are retained. No clipping, overlap or sustained spacing defect. Final page retains substantive ending, blessing, dated clause, final citation note and BENEDICTUS PP. XV subscription above rule and compact apparatus.

### `acta.ass.034.ass-034-l025902` (la) — PASS

PDF: `23703acb1b4938e0a3c51bfc8641fb605a621b2753eec8657d43b0a5715a3d8a`. Actual pages: 6; contact overview and individual full-size inspection: 1, 2, 3, 4, 5, 6.

Receipt: `144477ea1b59b430fcc5c0c7b461fe9037315d66cdb31dcccc383936162301a3`. Frozen manifest: `5cffa2c4368535582dba77766cfca518d9a6d15a7e17b284d7c04db3d87aa0c1`. Source payload: `6655dba354966b066d2ef52ce413e7328eadddfe030b03a17d66cfaf7b83a95c`.

Latin two-column text remains readable. Note sets on pages 1–5 have separate indented starts and ends; final page retains source exhortation, blessing, date and LEO PP. XIII subscription before ruled apparatus which continues in right column. Some literal internal hard-line hyphens and isolated native letterspaced words remain, without sustained unreadability.

### `acta.ass.034.ass-034-l012846` (la) — PASS

PDF: `ef5b60185786fb97439ea286994d7f4120fc80a0fb3a6e2714842e3e1251999f`. Actual pages: 2; contact overview and individual full-size inspection: 1, 2.

Receipt: `5d74d051a6b699831b8b682d7bc8a0fbe67a1fd45a956e94d6221e722df342e9`. Frozen manifest: `08f531b9393e5282448df3e0094190c6a7c59736d002bf74a3dce889a47d76bf`. Source payload: `5ebd4c3f12542382676aeb8e85b7dbec106ff44b9a809766c1a0f01ab3fbdf21`.

Both note groups distinct (page 1 right below seminary paragraph; page 2 after closing). Preserved letterspaced unum and fragmented lines remain readable. Page 2 sparse but has continued body, blessing, dated clause and final historical notes above project apparatus. No separate subscription appears. Clear gutter, no clipping or overlap.

## Source and transformation checks

All four PDFs, receipts, frozen manifests, source payloads and segment manifests match the packet hashes. Each entire frozen document row equals its packet source row. Every available controller/recipe record and tracked payload pin matches. Raster PDF/page-count bindings and every cached file hash match. `pdfinfo` reads all four PDFs with the expected page counts and issuer/language/title metadata; all listed Latin Modern fonts are embedded, subsetted and Unicode-mapped. No PDF exceeds 75 KiB per page or 1 MiB. Qpdf is unavailable; no qpdf structural check is claimed.

The read-only source validation and whole-body PDF fidelity function were rerun against the exact selected source row. All four pass `pdf-raw-source-aware-line-hyphen-nfkc-v3`, allowing whitespace, Unicode compatibility and source-aware line-ending discretionary hyphens. Source first/last pages are respectively 1/9, 1/7, 1/6 and 1/2. This is mechanical fidelity, not lexical collation.

The LF-only note derivations reproduce all four retained payloads exactly: 14 Rite expiatis groups, 14 Italian Ad beatissimi groups, 11 Eucharistia groups and 2 Bohemiae groups. Inspection of the helper confirms explicit hash/range selection and insertion of empty LF records, with no semantic note detector or lexical normalization. The current notes helper hash is `a0b31d45f498bec3a12a29cdff28da38f3e01cc02c50e5de8a9a65e4a82a9d57`. Italian also replays identically through the canonical historical notes helper `92a17c5a5de809b2261f14979ef4d71444dae20e490bbfe5617e5fd7bec003c4`.

Current native helper `7c7393f6b366bc986e7d106d217a769fabba5a48edd645a7bd02b463eb64d82c` reproduces both legacy recipes' exact output bytes and complete registered line maps: Eucharistia 535 unique matched lines, 26,617 non-whitespace characters, only stream-order difference page 650; Bohemiae 110 unique matched lines, 5,081 characters, no stream difference. Those recipes retain their historical helper pin `8163acf4cc10c54c974690bc8f87f21f302b52ccde2d2124eacaa5e83d9249ea`; this audit executed the compatible current helper and does not claim to have executed that historical implementation. The inspected current method permits only exact same-page non-whitespace matches, preserves selected order and requires the explicit stream-order disposition. Both native raw extractions were independently re-extracted from the hash-matched whole source PDF and match their registered hashes exactly.

## Native loci inspected

All 55 bounded native excerpt pages were inspected in contact overviews. The following 48 native physical PDF pages were also opened individually at original raster resolution; these are source PDF page addresses, not contact-sheet ordinal labels.

| Reader | Full-size native physical PDF pages | Checked loci |
| --- | --- | --- |
| Rite expiatis | 153, 154, 157–166, 171–175 | Every one of 14 note groups; selector LF 6306; opening and ending boundaries |
| Ad beatissimi, Italian | 585–590, 592–599 | Every one of 14 note groups; protocol, dated ending and subscription |
| Eucharistia | 641–654 | Every spacing page and all 11 page-foot note groups; stream difference 650; terminal boundary |
| Bohemiae | 321–323 | Every spacing page and both note groups; terminal boundary |

Source PDF hashes: AAS 18 `6d501f9ad97d4dc9a7581e83c6f057fe4e74ec7b0fc55e4530a4da4c66a77c7a`; AAS 6 `b655eb5e24d52cfabc538f3da1e3e19d7056fe9dc1fcb67189a3b1bea5c8831f`; ASS 34 `64a68e6efcbf01054672a6bccb274a8ce1dcce4241149ce342d4d478c6786ea8`. Bounded excerpt hashes, their exact original page ranges, source-range/excerpt text agreement, raster hashes and native raw checks are recorded in `native-evidence-verification.json`.

All 41 repaired note groups occupy separate smaller page-foot blocks in the native reconstruction, without body/note column interleaving or marginal summaries. The explicit note bounds match the native page-addressed text: LF-partition-only witnesses against native layout extraction, and spacing witnesses against native raw extraction. Italian native page 593 has a raw/layout punctuation-order difference inside its note group (stray dots around note marker 2). The retained layout extraction matches the registered bounds; the LF repair retains that exact sequence and never adopts raw-stream order. This is inherited OCR evidence, not a note/body fusion.

Rite expiatis source LF 6306 is the lower publisher line `Aera., vol. XVIII, n. 5. - 3-5-926.` with its page numeral. Native page 153 places it below the continuing body; native page 154 resumes that body. The explicit selector removes this furniture, preserving the substantive continuation. At native page 175 the selected blessing, dating clause and PIUS PP. XI subscription precede a different apostolic epistle, which does not enter the reader.

Eucharistia native page 650 physically places its sole historical citation below the body although the raw stream emits it earlier. The approved LF order and explicit page-650 disposition keep that note after the page-650 body and before the continuing page-651 body. Bohemiae native page 323 ends after its dated clause and final historical notes; it supplies no separate subscription. Each reader's final page is source-bearing.

## Qualifications and evidence

Retained hard-line word fragments, scattered letterspaced words, reference marks and OCR glyph errors remain visible. They impair polish but do not create sustained unreadability in these four readers. Historical notes use distinct paragraph starts in retained source order, so a note may interrupt a source sentence or divided word. No fused note/body paragraph, clipping, overflow, column overlap or project-apparatus-only terminal page was found. No wording correction is proposed by this acceptance.

Audit files under `.scratch/cold-repairs-23b/`: `reviews.json`, `verification.json`, incremental `page-observations.json`, `replay-verification.json`, `native-evidence-verification.json`, `note-loci-verification.json`, `fidelity-verification.json`, read-only metadata/font outputs and independently replayed scratch derivatives. No tracked source, PDF, manifest, cache or release was changed, and no raster was regenerated.
