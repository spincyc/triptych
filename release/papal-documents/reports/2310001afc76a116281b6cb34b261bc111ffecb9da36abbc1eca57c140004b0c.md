# Acta visual layout review — batch 001

Reviewed on 2026-10-26 UTC; narrow adjudication revised on 2026-10-26 UTC. **38 PDFs, 69 pages individually inspected; 37 PASS, 1 CHANGES_REQUIRED.** No prior Acta page review was reused. Pascendi requires correction for two confirmed publisher running heads on page 19 of the exact frozen PDF.

The scope is `.scratch/acta_visual_review/batch-001/assignment.json`, frozen receipt SHA-256 `3d1d2c53a1be2d8407d36292652f1e87bd6510182d69db50ab22473d25f50a07`. Every assigned full-page raster was opened individually through `view_image` at original raster size. Inspection covered title and issuer/language identification, both columns, visible source headings, closings and historical notes, source notice and final rights colophon. Checks included clipping, collision, reading order, missing glyphs, isolated headings and source-free terminal pages.

All 38 frozen PDF hashes and all 69 assigned raster hashes matched the assignment before and after inspection. The actual frozen receipt hash also matched. Exact paths and hashes are recorded in `.scratch/acta_visual_review/batch-001/hashes-before.json`, `hashes-after.json`, `receipt-check.json` and `inspection-log.json`; the normalized outcome is `result.json` in that directory. `checkpoint.json` preserves the earlier actual 66-page checkpoint; the final inspection log records all 69 pages.

This is visual layout inspection. Source OCR remains uncollated, including malformed words, letter spacing, inline reference fragments and unusual printed symbols. It does not establish source-image fidelity, historical authenticity, rights clearance, installation or publication. The source notices state the derivative and collation limits; their readable presence does not independently validate their claims.

## Revision history and required correction

The original completion of 38 PASS and 0 CHANGES_REQUIRED is superseded only for `acta.ass.040.ass-040-l022854` (`la`, 21 pages), frozen PDF SHA-256 `98588238b36fc2e2016fd5b635444750a5bd71199a10a7a1d8c9c0eaa3c8c009`. Page 19 contains two pure publisher running heads `4 Litterae Encyclicae`: the lower left-column head splits `Censo-` / `res e religiosorum familiis` (source LF 24857); the right-column foot head follows genuine historical citations before `adsciscantur` continues on page 20 (source LF 24934). Exclude only those two publisher heads. The historical citations, opening genre heading and source-bearing page 21 subscription remain qualified source content.

This corrects the original page 19 OCR-furniture qualification using the coordinator's independent original-page calibration at `.scratch/acta_visual_coordinator/runninghead-calibration-coordinator/result.json`, SHA-256 `c6db5bc7ccb5a349e1ff1cfa38d7cb92144672e648bdee4350a5d0acf8aa5ad7`; the source owner confirmed the two pure publisher lines. The exact page raster is `.scratch/acta_visual_review/rasters-01/.scratch/acta_visual_review/frozen/pdfs/1907-09-08-acta-ass-040-ass-040-l022854-2cfa979b-la/pages/page-19.png`, SHA-256 `a40de1dfebb06db32510b779abff85eb6a1d1e7bebbdc2fa50105a7b9396eb5d`. Its calibration proof is copied byte-identically to `.scratch/acta_visual_review/batch-001/review-revision-001-calibration.json`. This adjudication revision claims no additional page view and preserves all 69 recorded individual views and every other observation.

Byte-identical originals are archived under `.scratch/acta_visual_review/batch-001/review-revision-001-before/`, including the original report (SHA-256 `697cfa7a98d87d415b03447d45d7d1c73e156b9fbd1f7db0907c8fcd06125de9`), result (`91642d51a7d36a78c0aaf2c1177c77402c0153a2304576f40c1ffd8a490f88bc`), inspection log (`c077d2fd3c5dea07298d432bd4e7214f3c4833c687fe7e78b7f4400da7f2d5a3`), before/after hash evidence and original completion pins in `validation.json` (`d4b41efebe7937c31b68fd12360c54fcfbf2cad48ceffc20ab50d010874f1b33`). The archive manifest, `review-revision-001.json`, fresh unchanged-byte checks in `revision-hashes.json`, and current `validation.json` / `completion.json` preserve the evidence chain. Replacement PDF bytes require a separate exact-hash review.

## Qualified findings

- `acta.ass.007.ass-007-act-011`, page 3: a sparse close retains the final source dating words, chancery subscriptions and register wording before the notices. PASS qualified. Its source notice explicitly distinguishes an adjacent, separately signed publication certificate excluded from this papal body; this review does not independently establish that source boundary.
- `acta.ass.040.ass-040-l022854`, page 21: the very sparse final page retains the historical Pius X subscription before source and rights notices. Its source-bearing signature qualification remains valid. Pages 1–20 retain extensive OCR spacing and genuine inline reference fragments; the two confirmed publisher heads on page 19 are the separate CHANGES_REQUIRED finding described below.
- `acta.aas.009.i.archive.aas.009.i.l008870`, page 2, and `acta.aas.019.aas-019-l03633`, page 2: each very sparse final page retains a historical Cardinal Gasparri subscription before the notices. PASS qualified as source-bearing closing spills; no repair is requested solely for sparseness.
- `acta.ass.038.ass-038-l014560`, page 1: Italian identifies the main letter; its historical Latin synopsis remains visible above the Italian recipient heading. Retained malformed words and punctuation remain qualified OCR.
- `acta.aas.020.aas-020-l12426`, page 1: the source title includes punctuation and digit debris, and separator-like marks appear before the closing. They remain visible and uncorrected. Their source-image meaning is outside this layout review; no physical collision or clipping was observed.

## Exact PDF coverage

The inspected-page arrays below give every actual PDF page. All reuse arrays are empty. Detailed page-specific observations follow in assignment order.

| ID | Language | Exact PDF SHA-256 | Pages | Individually inspected pages | Status |
| --- | --- | --- | ---: | --- | --- |
| `acta.ass.009.ass-009-act-031` | `la` | `9f18d8ee750ddab30af6844f9c41f230948f4a63101a6ef3f5b5c39f1dfa3547` | 1 | `[1]` | PASS |
| `acta.ass.001.ass-001-quamvis-urbs` | `la` | `eca3908c8f66e76fff5a0d34cf430911e0058b2c9938d99496c7e579d6204f9b` | 1 | `[1]` | PASS |
| `acta.ass.007.ass-007-act-011` | `la` | `883729637f4a328f017bca273e2743fdce0dc4f80b0afbd44e93262129e40517` | 3 | `[1,2,3]` | PASS |
| `acta.ass.015.ass-015-act-007` | `la` | `430c4085f9732a1a58c24b9fae191c8bcb345db5f992daaca45dd704d6ae6451` | 2 | `[1,2]` | PASS |
| `acta.ass.027.ass-027-l00233` | `la` | `37fc24617bb4546b44a42a87ba0f47bb6bbc6fd6fc002916cd7f1ed829c579a9` | 1 | `[1]` | PASS |
| `acta.ass.032.ass-032-l10116` | `la` | `a0ed4c9b282e429d92c0a8a8742d194a5e46d0e43422ca9bc27157bed2533c55` | 2 | `[1,2]` | PASS |
| `acta.ass.036.ass-036-l000316` | `la` | `373a70424ef9d620abd8cfa229a2839284d3cee5ee8c02bb061ca846388c58f9` | 1 | `[1]` | PASS |
| `acta.ass.039.ass-039-l022410` | `la` | `9bb4721c0929876390676ae08726ad465284dcdbaf43f517cb3718bfd421fc54` | 1 | `[1]` | PASS |
| `acta.ass.040.ass-040-l022854` | `la` | `98588238b36fc2e2016fd5b635444750a5bd71199a10a7a1d8c9c0eaa3c8c009` | 21 | `[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]` | CHANGES_REQUIRED |
| `acta.aas.009.i.archive.aas.009.i.l008870` | `la` | `6a2d3fba94f5a64ece8460b01a9ae0df5d9a1b282597e9af205d049fc966fe74` | 2 | `[1,2]` | PASS |
| `acta.aas.010.archive.aas.010.l012855` | `la` | `5e6063267b3e0fd14988a6552fdae6ab8169a3394fc410bfa09d954d37b9aacf` | 1 | `[1]` | PASS |
| `acta.aas.011.archive.aas.011.l011544` | `la` | `f3a50f00f3f0037bd28cdaf5873ede28f8ea4a580e1136a42a44a3763f272b9c` | 1 | `[1]` | PASS |
| `acta.aas.012.archive.aas.012.l023533` | `la` | `c85c113117674fc6eaaad3e5a87af26bf7a33456e1773c77251871d9261c2a97` | 2 | `[1,2]` | PASS |
| `acta.aas.012.archive.aas.012.l023789` | `la` | `c0f2c5aa8976e2b5a7d9d1a9fc769f225d212021e36b3c654a87ff2df743b006` | 1 | `[1]` | PASS |
| `acta.aas.014.archive.aas.014.l027029` | `la` | `c366359e64722c8fe4ef822fc97efea4c14f6e8c2e8bc2b34cb5dcbc4405127b` | 1 | `[1]` | PASS |
| `acta.aas.016.aas-016-l15188` | `la` | `d736d5d59d02f31ddbe8b03eed132b6160c3eb9f4460093d1af0448eff6d7a34` | 1 | `[1]` | PASS |
| `acta.aas.019.aas-019-l03633` | `la` | `0042f5c137adb68e966b83b321f5c11252d46d43ad13dbe1701edcf61e36abd4` | 2 | `[1,2]` | PASS |
| `acta.aas.001.archive.aas.001.006` | `la` | `1b7b545dee9326285842079a3cec165be0cf8be40608cebdfb7738fd987ce10f` | 1 | `[1]` | PASS |
| `acta.aas.001.archive.aas.001.056` | `la` | `6ca5ab446010c6ce2bfd7420e5fb23f8c37128acb3e95a4d6b33120de6c0501f` | 2 | `[1,2]` | PASS |
| `acta.aas.001.archive.aas.001.073` | `la` | `7e1562f4d458f9aea9871cf3c0fae5064737dce0a307a0bd03afc1e0653c3333` | 1 | `[1]` | PASS |
| `acta.aas.002.archive.aas.002.044` | `la` | `12ce9501ea05773f296f19adfd820980a9951ebab9b9c1638cce41c7cf29b73a` | 1 | `[1]` | PASS |
| `acta.aas.003.archive.aas.003.005` | `la` | `7ef14a2ab4754566d447a394e0797d03a1b3b8834ed26d08307d218c39d3b0bb` | 1 | `[1]` | PASS |
| `acta.aas.003.archive.aas.003.076` | `la` | `501d0b910badfa8aee4775e557bca37cfc8ef1fcc500151243f7b34543fb6c09` | 1 | `[1]` | PASS |
| `acta.aas.004.archive.aas.004.002` | `la` | `d7758b62be90e8531f4ab595f851c5c7ede9c6648ce555e95e8735f33a811690` | 2 | `[1,2]` | PASS |
| `acta.aas.004.archive.aas.004.048` | `la` | `3552b92ef650f70700b50263dde0ad6978e21a9f0b5f1967b9cce269acb271c8` | 1 | `[1]` | PASS |
| `acta.aas.005.archive.aas.005.061` | `la` | `650e0c05834186c1cf62c320a5cdd0fa3f693115e3ac4a603276e3b0cdc6e73e` | 1 | `[1]` | PASS |
| `acta.aas.007.archive.aas.007.022` | `la` | `6b68c9601018c7c6a1914b6f4256ee1d7001738d017e9b2e88f8ba8597077423` | 1 | `[1]` | PASS |
| `acta.aas.008.archive.aas.008.040` | `la` | `b3576eb20319af5f242627867b5cb3f47dacbdd3141c349b091730104d922d28` | 1 | `[1]` | PASS |
| `acta.aas.009.i.archive.aas.009.i.l015763` | `la` | `5792bd8da47d7abbef24b5e7e034289d5c4945f4c845c5d0e980e695a2e7c0ef` | 1 | `[1]` | PASS |
| `acta.aas.014.archive.aas.014.l000030` | `la` | `503937a915355d16c8ba04bb8817926ab5eb0fbdb3cb5e1530810a359d51e3fe` | 1 | `[1]` | PASS |
| `acta.aas.015.archive.aas.015.l019108` | `la` | `b42fd851d88b9b9d2bf9bcabe9fac0a0941b88d7d460e4a84c5066772f811a48` | 1 | `[1]` | PASS |
| `acta.aas.016.aas-016-l08900` | `la` | `5b319811fcff32e762f5a820b4ae0596a6585072be46700fc3b25b65ee9b30c9` | 2 | `[1,2]` | PASS |
| `acta.aas.018.aas-018-l15527` | `la` | `6ff6cbb856239f839e4d94c07a9372fba2d1f9523d865bd6745247dde982f915` | 1 | `[1]` | PASS |
| `acta.aas.019.aas-019-l11956` | `la` | `2cf5001cbfb4b03cf63ae8662a5f3bdb506a1cf4c3b77ad5111df2966c1f9ce6` | 1 | `[1]` | PASS |
| `acta.aas.020.aas-020-l12426` | `la` | `4084dd172be6fa9b91d421f7fdf3e02d653c7a3927971c170c6eea19b78d481d` | 1 | `[1]` | PASS |
| `acta.aas.021.aas-021-l26082` | `la` | `785028bd46f0bdbc4451ace050911acbdc278234fafe2306f03b16b20c4ea5a2` | 1 | `[1]` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l10078` | `la` | `02a0d107aa79a10d9b3c7da279aabcf20de662646ea6d6368a3718fed9b77f0c` | 2 | `[1,2]` | PASS |
| `acta.ass.038.ass-038-l014560` | `it` | `4f095a46450f34428607552469e3a0e42b27db94c938331ee6f9cff619a9f22b` | 1 | `[1]` | PASS |

## Page observations

### acta.ass.009.ass-009-act-031 (la) — PASS

- Page 1: Compact title and Pius VI / 1778-03-17 / Latin line fit above the historical brief heading and Pius VI identification. Entire letter, source date and Philippus Bonamicius subscription precede readable Source notice and rights colophon in the left column. The later ASS 9 (1876) publication basis is explicit; retained source letter spacing is qualified OCR, with no clipping or overlap seen.

### acta.ass.001.ass-001-quamvis-urbs (la) — PASS

- Page 1: Compact title and Pius IX / date / Latin line fit above the papal identification. Two distinct columns reach the dated closing, cardinal subscription and retained seal notation, followed by readable Source notice and rights colophon. Retained asterisk, malformed seal string and word breaks are qualified OCR; no missing-glyph boxes seen.

### acta.ass.007.ass-007-act-011 (la) — PASS

- Page 1: Compact title and Pius IX / date / Latin line fit. The apostolic-letter heading, papal identification and dense two-column body remain readable; retained inline source-reference digits, quotation fragments and broken words remain qualified OCR.
- Page 2: Dense continuation, historical editor note and start of the closing date remain inside separated columns with clear margins; no collision, clipping or missing-glyph boxes seen.
- Page 3: Sparse source-bearing close: final dating words, chancery subscriptions and register wording precede readable Source notice and rights colophon. PASS qualified for sparseness. The notice explicitly distinguishes a separately signed adjacent publication certificate retained in the parent witness and excluded from this papal body; this review does not independently establish that source boundary.

### acta.ass.015.ass-015-act-007 (la) — PASS

- Page 1: Long single-line title and Leo XIII / date / Latin line fit within the page. Historical letter heading, dense body and source-reference strings remain inside separated columns; pervasive letter spacing, caret and broken words are retained OCR limitations.
- Page 2: Substantial concluding text and source dating clauses remain readable in the left column before the Source notice and rights colophon. No clipping, overlap or source-free terminal page seen.

### acta.ass.027.ass-027-l00233 (la) — PASS

- Page 1: Compact title and Leo XIII / date / Latin line fit above the source letter heading. Body reaches the dated closing and Leo XIII subscription before the Source notice in the left column; rights colophon continues at the top right. Retained OCR letter spacing and broken words remain qualified; no clipping or collision seen.

### acta.ass.032.ass-032-l10116 (la) — PASS

- Page 1: Compact title and Leo XIII / date / Latin line fit. The historical constitution heading and papal identification are visible above dense body/provisions. Both columns and inline source references remain clear; retained bullet and word breaks are qualified OCR.
- Page 2: Substantive provisions and conclusion reach the dated closing, cardinal/chancery subscriptions and register notation in the right column. Source notice and rights colophon remain readable below; no clipping, collision or source-free ending seen.

### acta.ass.036.ass-036-l000316 (la) — PASS

- Page 1: Two-line title and Pius X / date / Latin line fit above the historical letter heading. Both columns remain distinct through source date, Pius X signature and recipient line, followed by readable Source notice and rights colophon. Retained caret and broken words are qualified OCR; no title-only page or missing-glyph box seen.

### acta.ass.039.ass-039-l022410 (la) — PASS

- Page 1: Two-line spaced-capital title and Pius X / date / Latin line fit. Body, dated closing and cardinal subscription stay in the left column; Source notice continues into the top right before the rights colophon. Retained OCR spacing and hyphens remain source features; no clipping, overlap or isolated heading seen.

### acta.ass.040.ass-040-l022854 (la) — CHANGES_REQUIRED

- Page 1: Four-line title and Pius X / date / Latin line fit above the retained encyclical heading and papal identification. Pascendi incipit and extensive historical editor note remain inside separated columns. Retained OCR letter spacing, reference strings and broken words are qualified source limitations.
- Page 2: Dense Latin continuation and inline source references stay within clear columns and margins; no clipping, collision or missing-glyph boxes seen.
- Page 3: Dense continuation remains readable in both columns; source OCR spacing and broken words remain qualified, with no physical layout obstruction seen.
- Page 4: Dense body and inline references remain within two clear columns; retained source spacing and word breaks cause no clipping or collision.
- Page 5: Full Latin columns have clear margins and gutter; no missing-glyph boxes, overlap or isolated headings seen.
- Page 6: Dense continuation and source-reference strings remain readable. Literal bullets/caret and unusual spacing in the right column are retained OCR features, with no physical layout obstruction seen.
- Page 7: Dense Latin continuation and retained source spacing/reference fragments remain within clear columns and margins; no clipping, collision, missing-glyph boxes or isolated heading seen.
- Page 8: Dense Latin continuation and retained source spacing/reference fragments remain within clear columns and margins; no clipping, collision, missing-glyph boxes or isolated heading seen.
- Page 9: Dense Latin continuation and retained source spacing/reference fragments remain within clear columns and margins; no clipping, collision, missing-glyph boxes or isolated heading seen.
- Page 10: Full columns and inline source-reference blocks remain clear and within margins; no clipping or overlap seen.
- Page 11: Dense body and inline references remain inside separated columns with readable line spacing; retained OCR spacing is qualified.
- Page 12: Full columns remain distinct. Literal bullets and malformed source-reference fragment near upper left are retained OCR, with no missing-glyph boxes, collision or clipping seen.
- Page 13: Dense Latin continuation and source references remain readable inside two distinct columns with clear margins; retained source letter spacing and word breaks are qualified, with no clipping, collision or missing-glyph boxes seen.
- Page 14: Dense Latin continuation and source references remain readable inside two distinct columns with clear margins; retained source letter spacing and word breaks are qualified, with no clipping, collision or missing-glyph boxes seen.
- Page 15: Dense Latin continuation and source references remain readable inside two distinct columns with clear margins; retained source letter spacing and word breaks are qualified, with no clipping, collision or missing-glyph boxes seen.
- Page 16: Dense body, retained source references and numbered provisions remain inside distinct columns with clear margins; no clipping, overlap, missing-glyph boxes or isolated heading seen.
- Page 17: Dense body, retained source references and numbered provisions remain inside distinct columns with clear margins; no clipping, overlap, missing-glyph boxes or isolated heading seen.
- Page 18: Dense body, retained source references and numbered provisions remain inside distinct columns with clear margins; no clipping, overlap, missing-glyph boxes or isolated heading seen.
- Page 19: CHANGES_REQUIRED for two pure publisher running heads '4 Litterae Encyclicae' intruding into the source text. The lower left-column head splits Censo- / res e religiosorum familiis (source LF 24857); the right-column foot head follows genuine historical citations before the page 20 continuation adsciscantur (source LF 24934). Exclude only these publisher heads; retain the historical citations and opening genre heading. Dense provisions and references otherwise remain within clear columns; retained bullets remain qualified OCR. This supersedes the original furniture qualification on the coordinator's independent original-page calibration, proof .scratch/acta_visual_coordinator/runninghead-calibration-coordinator/result.json SHA-256 c6db5bc7ccb5a349e1ff1cfa38d7cb92144672e648bdee4350a5d0acf8aa5ad7. This revision claims no additional page view.
- Page 20: Substantive conclusion and source dating clause remain readable in the right column after the final provisions; no clipped closing or overlap seen.
- Page 21: Very sparse terminal page retains the historical Pius X subscription before the readable Source notice and rights colophon. PASS qualified as a source-bearing signature spill; it is not an apparatus-only page.

### acta.aas.009.i.archive.aas.009.i.l008870 (la) — PASS

- Page 1: Two-line title and Benedict XV / date / Latin line fit above the apostolic-letter heading and papal identification. Both dense columns remain readable through the closing date, with retained OCR hyphenation qualified.
- Page 2: Very sparse final page retains the historical Cardinal Gasparri subscription before the readable Source notice and rights colophon. PASS qualified as a source-bearing subscription spill; no source-free ending or clipping seen.

### acta.aas.010.archive.aas.010.l012855 (la) — PASS

- Page 1: Four-line title and Benedict XV / date / Latin line fit above the numbered source heading and papal identification. Both columns remain distinct through closing date and Cardinal Gasparri subscription, with readable Source notice and rights colophon below right. Pervasive OCR spacing and asterisk remain qualified source features.

### acta.aas.011.archive.aas.011.l011544 (la) — PASS

- Page 1: Five-line title and Benedict XV / date / Latin line fit above the numbered historical heading. Two columns carry the letter through source date and Benedict XV subscription to readable Source notice and rights colophon. Source spelling/diacritics and pervasive letter spacing remain qualified OCR; no clipping or collision seen.

### acta.aas.012.archive.aas.012.l023533 (la) — PASS

- Page 1: Four-line title and Benedict XV / date / Latin line fit above the apostolic-letter heading and papal identification. Dense columns and retained source word breaks remain readable, with no clipping or overlap.
- Page 2: Substantial conclusion, source date and Cardinal Gasparri subscription precede readable Source notice and rights colophon in the left column. OCR spacing remains qualified; no source-free terminal page seen.

### acta.aas.012.archive.aas.012.l023789 (la) — PASS

- Page 1: Three-line spaced-capital title and Benedict XV / date / Latin line fit above numbered source heading and papal identification. Full body, dated closing, Cardinal Gasparri subscription, Source notice and rights colophon remain readable in the left column. Retained OCR letter spacing and word breaks cause no clipping or collision.

### acta.aas.014.archive.aas.014.l027029 (la) — PASS

- Page 1: Single-line title and Pius XI / date / Latin line fit above apostolic-letter heading and papal identification. Body reaches dated closing and Cardinal Gasparri subscription before Source notice in the left column; rights colophon is readable at top right. Retained OCR spacing remains qualified; no clipping or overlap seen.

### acta.aas.016.aas-016-l15188 (la) — PASS

- Page 1: Five-line title and Pius XI / date / Latin line fit above the historical letter heading. Both columns remain distinct through the dated closing and Pius XI subscription, with readable Source notice and rights colophon below right. Source OCR spacing, malformed words and numeral forms remain qualified.

### acta.aas.019.aas-019-l03633 (la) — PASS

- Page 1: Four-line spaced-capital title and Pius XI / date / Latin line fit above the numbered historical heading and papal identification. Dense columns reach the source date at bottom right; retained caret and letter spacing remain qualified, with no clipping or collision.
- Page 2: Very sparse terminal page retains the historical Cardinal Gasparri subscription before readable Source notice and rights colophon. PASS qualified as a source-bearing subscription spill; source-free apparatus is not its only content.

### acta.aas.001.archive.aas.001.006 (la) — PASS

- Page 1: Two-line title and Pius X / Latin line fit. Complete letter, source dating and Pius X subscription precede readable Source notice and rights colophon in the left column; note identifies AAS 1 (1909) separately from the visible 1908 source date. Source OCR spelling, broken words and spaced numerals remain qualified; no clipping or overlap seen.

### acta.aas.001.archive.aas.001.056 (la) — PASS

- Page 1: Three-line title and Pius X / Latin line fit above the historical letter heading. Dense two-column body remains readable through its continuation; retained OCR word breaks and spaced numerals remain qualified, with no clipping or collision.
- Page 2: Substantial continuation, source date and Pius X subscription precede readable Source notice and rights colophon in the left column. No source-free ending, overlap or missing-glyph boxes seen.

### acta.aas.001.archive.aas.001.073 (la) — PASS

- Page 1: Four-line title and Pius X / Latin line fit above the historical heading and papal identification. Full left column flows into the substantive conclusion, date and Cardinal Merry del Val subscription at right, followed by readable Source notice and rights colophon. Retained percent-like mark, numeral spacing and word breaks remain qualified OCR.

### acta.aas.002.archive.aas.002.044 (la) — PASS

- Page 1: Three-line title and Pius X / Latin line fit above the historical heading and papal identification. Two columns reach source date and Cardinal Merry del Val subscription before readable Source notice and rights colophon at right. Pound-sign/digit-like subscription marks and letter spacing are retained OCR features; no missing-glyph boxes or clipping seen.

### acta.aas.003.archive.aas.003.005 (la) — PASS

- Page 1: Four-line title and Pius X / Latin line fit above the complete historical letter. Source date and Pius X subscription precede readable Source notice and rights colophon in the left column. Source-title diacritics, apostrophe and word breaks remain qualified OCR; no collision or clipping seen.

### acta.aas.003.archive.aas.003.076 (la) — PASS

- Page 1: Three-line title and Pius X / Latin line fit above the historical heading and papal identification. Full left column flows clearly into the conclusion, date and Cardinal Merry del Val subscription at top right, followed by readable Source notice and rights colophon. Retained source word breaks and accent are qualified OCR; no layout obstruction seen.

### acta.aas.004.archive.aas.004.002 (la) — PASS

- Page 1: Three-line title and Pius X / Latin line fit above historical letter heading. Dense two-column body remains readable; retained bullet, asterisk, malformed word and word breaks are qualified OCR.
- Page 2: Substantive continuation and conclusion reach the source date and Pius X subscription in the right column before readable Source notice and rights colophon. The visible source date and AAS 4 (1912) publication reference remain distinct; no clipping, collision or furniture-only ending seen.

### acta.aas.004.archive.aas.004.048 (la) — PASS

- Page 1: Five-line title and Pius X / Latin line fit above historical letter heading. Complete body, dated closing and Pius X subscription precede readable Source notice and rights colophon in the left column. Retained source numeral spacing and word breaks are qualified OCR; no clipping or isolated heading seen.

### acta.aas.005.archive.aas.005.061 (la) — PASS

- Page 1: Three-line title and Pius X / Latin line fit. Complete letter, source date and Pius X subscription precede readable Source notice in the left column; rights colophon is readable at top right. Source-heading 'DF' and pervasive letter spacing are retained OCR limitations; no clipping or overlap seen.

### acta.aas.007.archive.aas.007.022 (la) — PASS

- Page 1: Three-line title and Benedict XV / Latin line fit above the complete historical letter. Source date and Benedict XV subscription precede readable Source notice and rights colophon in the left column. Source-title diacritic/spacing and broken words remain qualified OCR; no layout obstruction seen.

### acta.aas.008.archive.aas.008.040 (la) — PASS

- Page 1: Five-line title and Benedict XV / Latin line fit above the source letter heading. Body reaches date and Benedict XV subscription before the Source notice in the left column; rights colophon is readable at top right. Retained source spacing, punctuation and word breaks cause no clipping or collision.

### acta.aas.009.i.archive.aas.009.i.l015763 (la) — PASS

- Page 1: Four-line title and Benedict XV / Latin line fit above numbered epistle heading. Two-column letter reaches source date and Benedict XV subscription before readable Source notice and rights colophon at right. Malformed source-title spelling and broken words remain qualified OCR; no clipping or overlap seen.

### acta.aas.014.archive.aas.014.l000030 (la) — PASS

- Page 1: Three-line title and Benedict XV / Latin line fit above apostolic-letter heading and papal identification. Two columns remain readable through the source date and Cardinal Gasparri subscription, with Source notice and rights colophon below right. Literal title caret, malformed source-year numeral and letter spacing remain qualified OCR; the AAS 14 (1922) publication reference remains explicit.

### acta.aas.015.archive.aas.015.l019108 (la) — PASS

- Page 1: Two-line title and Pius XI / Latin line fit above historical constitution heading and papal identification. Full left column flows to the source date, cardinal/protonotary subscriptions and register wording at top right, followed by readable Source notice and rights colophon. Retained pound-sign/digit-like seal string and source spelling/spacing remain qualified OCR; no layout obstruction seen.

### acta.aas.016.aas-016-l08900 (la) — PASS

- Page 1: Two-line title and Pius XI / Latin line fit above the constitution heading and papal identification. Both dense columns remain distinct through body continuation; retained OCR spacing and broken words remain qualified.
- Page 2: Substantial closing clauses, source date, cardinal/protonotary subscriptions and seal/register wording precede readable Source notice and rights colophon in the left column. Copyright-like source mark and malformed words remain qualified OCR; no clipping, overlap or source-free ending seen.

### acta.aas.018.aas-018-l15527 (la) — PASS

- Page 1: Four-line title and Pius XI / Latin line fit above the apostolic-letter heading and papal identification. The full left column ends with source date and Cardinal Gasparri subscription; Source notice and rights colophon are readable at top right. Malformed heading spelling and OCR word spacing remain qualified; no physical obstruction seen.

### acta.aas.019.aas-019-l11956 (la) — PASS

- Page 1: Four-line spaced-capital title and Pius XI / Latin line fit above epistle heading and papal identification. Full left column continues into the source date and Pius XI subscription at top right, followed by readable Source notice and rights colophon. Retained source bullet, spaced numerals and word breaks remain qualified OCR; no clipping or collision.

### acta.aas.020.aas-020-l12426 (la) — PASS

- Page 1: Six-line title and Pius XI / Latin line fit above the historical heading and papal identification. Both columns remain readable through dated closing and Pius XI subscription before Source notice and rights colophon at right. Source-heading punctuation/digit debris and horizontal separator-like marks before the closing are retained OCR limitations; no physical overlap, clipping or missing-glyph boxes seen.

### acta.aas.021.aas-021-l26082 (la) — PASS

- Page 1: Three-line title and Pius XI / Latin line fit above constitution heading and papal identification. Both columns remain readable through source date, cardinal/protonotary subscriptions and seal/register wording, followed by Source notice and rights colophon. Source-title spelling, caret/asterisk and seal-like marks remain qualified OCR; no clipping or collision seen.

### acta.aas.022.issues-01-12.aas-022-l10078 (la) — PASS

- Page 1: Two-line title and Pius XI / Latin line fit above constitution heading and papal identification. Dense body and quoted historical text remain within clear columns and margins; retained source hyphenation and spelling remain qualified.
- Page 2: Substantial continuation and source date flow from the full left column to the top right; cardinal/protonotary subscriptions and seal/register lines precede readable Source notice and rights colophon. Retained pound-sign/letter-like seal string remains qualified OCR; no clipping, collision or apparatus-only ending seen.

### acta.ass.038.ass-038-l014560 (it) — PASS

- Page 1: Four-line title and Pius X / Italian line fit above the historical Latin synopsis and Italian recipient heading. Main letter is visibly Italian and reaches the source date and Pius X subscription before readable Source notice and rights colophon in the left column. Latin synopsis is retained historical heading, and malformed words, inverted-question-like mark and punctuation remain qualified OCR. No clipping or collision seen.

No PDF, raster, source text, source metadata or typesetting tool was changed by this review. Replacement bytes require a separate review against their exact hashes.
