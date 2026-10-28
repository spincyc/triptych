# Acta visual layout review — batch 007

Reviewed on 2026-10-26 UTC. **40 PDFs, 69 pages individually inspected; 40 PASS, 0 CHANGES_REQUIRED.** No prior Acta page review was reused. No layout blocker was observed in the assigned frozen bytes.

The scope is `.scratch/acta_visual_review/batch-007/assignment.json`, frozen receipt SHA-256 `3d1d2c53a1be2d8407d36292652f1e87bd6510182d69db50ab22473d25f50a07`. Every assigned full-page raster was opened individually through `view_image` at original raster size. Inspection covered title and issuer/language identification, both columns, visible source headings, closings and historical notes, source notice and final rights colophon; checks included clipping, collision, reading order, missing glyphs, isolated headings and source-free terminal pages. Saved completed views were preserved across capacity recovery before inspection continued through the remaining pages.

All 40 frozen PDF hashes and all 69 assigned raster hashes matched the assignment before and after inspection. The actual frozen receipt hash also matched. Exact paths and hashes are recorded in `.scratch/acta_visual_review/batch-007/hashes-before.json`, `hashes-after.json`, `receipt-check.json` and `inspection-log.json`; the normalized outcome is `result.json` in that directory.

This is visual layout inspection. Source OCR remains uncollated, including malformed words, letter spacing, inline reference fragments and unusual printed symbols. It does not establish source-image fidelity, historical authenticity, rights clearance, installation or publication. The source notices state the derivative and collation limits; their readable presence does not independently validate their claims.

## Qualified findings

- `acta.ass.040.ass-040-l012123`, page 1: the Latin-labelled main papal act includes a substantial Italian historical note signed Cardinal Merry del Val. PASS with this language qualification; the Latin label should not be read as describing every retained historical note.
- `acta.aas.016.aas-016-l09817`, page 2: the selected papal letter ends with its dated subscription after mentioning an attached law. This bounded visual inspection does not establish the scope or presence of that separate annex; no omission is asserted from these pages.
- `acta.aas.009.i.archive.aas.009.i.l013555`, page 2: a very sparse final page retains the historical Cardinal Gasparri subscription before the source notice and rights colophon. PASS qualified as a source-bearing closing spill; no repair is requested solely for sparseness.
- `acta.aas.012.archive.aas.012.l016158`, pages 11–12: particularly garbled OCR fragments remain visible near source reference groups. These are retained source limitations; the columns show no clipping, collision or missing-glyph boxes.

## Exact PDF coverage

The inspected-page arrays below give every actual PDF page. All reuse arrays are empty. Detailed page-specific observations follow in assignment order.

| ID | Language | Exact PDF SHA-256 | Pages | Individually inspected pages | Status |
| --- | --- | --- | ---: | --- | --- |
| `acta.ass.003.ass-003-apostolici-nostri` | `la` | `c56205ad72b412ed542ee529fc77025d2dd6f49f7e03631d56aa88c277762fb9` | 1 | `[1]` | PASS |
| `acta.ass.007.ass-007-act-017` | `la` | `cbe7d0982d179ea1a74ed66e76d376c56ba5ff48fb54bdb3a558ae15dcdebce9` | 3 | `[1,2,3]` | PASS |
| `acta.ass.011.ass-011-act-006` | `la` | `5e2b469f572e80f7b5c5561663e256525ff3efd91175108687ad1258d0b87486` | 1 | `[1]` | PASS |
| `acta.ass.017.ass-017-act-001` | `la` | `afde480ebcab7b0df0456c4f009be5b129f1662c09998fd9a3b31113a34e775b` | 2 | `[1,2]` | PASS |
| `acta.ass.028.ass-028-l00045` | `la` | `f4e7c127adbc601c5ed39c37a4b02051604ca6f4b1da93458019e8c1e86ffa38` | 1 | `[1]` | PASS |
| `acta.ass.033.ass-033-l07481` | `it` | `79bf4b733c479ccc8ecb7609b230d1e3e6795c3151fbd0687da79586c7b601e7` | 2 | `[1,2]` | PASS |
| `acta.ass.036.ass-036-l007763` | `la` | `cf21240a63046565bef7e6b10888a0f130882f5f3105453c0fbf0c2745499a2d` | 1 | `[1]` | PASS |
| `acta.ass.039.ass-039-l000792` | `la` | `5fea329d66bd668615c679bdc94008382078cc99077dcdfa3ecadbdfc7a0cda8` | 1 | `[1]` | PASS |
| `acta.ass.040.ass-040-l007377` | `la` | `7af76e9677efec38dcd02293ad14c056372ad91fdadb3423a6a9561fd0fd11cf` | 4 | `[1,2,3,4]` | PASS |
| `acta.ass.040.ass-040-l012123` | `la` | `e46ceefb6dc792081029028b6de68f09102050ba607a65e2deae76f7a732e689` | 1 | `[1]` | PASS |
| `acta.aas.009.i.archive.aas.009.i.l000030` | `la` | `025183790d578ca71dbc7037f5fadb472d42f9f9c9a108f32a61cdf52e30b2f8` | 1 | `[1]` | PASS |
| `acta.aas.010.archive.aas.010.l013291` | `it` | `43566702bfff07d091393abe629a17df2a253bd9b31ecdc3db0e18cfbee43ee8` | 1 | `[1]` | PASS |
| `acta.aas.009.i.archive.aas.009.i.l017737` | `la` | `8dbbd7ce7e4c55310f81652e77c3278c8ea4e3c351d4ef0b56b2a8d2bd946ff6` | 1 | `[1]` | PASS |
| `acta.aas.011.archive.aas.011.l014474` | `la` | `85108b1143815d929be04e53ab32eff368726b471f66dc3e7c994ababd9b75db` | 1 | `[1]` | PASS |
| `acta.aas.012.archive.aas.012.l016158` | `la` | `0f16c1272f804651921a3ffe77e4f9e302b4d3fe278b4a86234261ed5ace89f1` | 13 | `[1,2,3,4,5,6,7,8,9,10,11,12,13]` | PASS |
| `acta.aas.013.archive.aas.013.l000230` | `la` | `6c8cad7bf4282305bbe83973b1717e0521e3db6dfd76622f6abf254a17333a2e` | 1 | `[1]` | PASS |
| `acta.aas.014.archive.aas.014.l001367` | `la` | `a72d31b8e9b3afc05a4e60f17cbd2d02eae343eec26d4f5928888da65d23e27c` | 1 | `[1]` | PASS |
| `acta.aas.015.archive.aas.015.l001125` | `la` | `68897e63322a22efdf40635d4140656a151ce4dda3986745753b3e6e01b6a9bd` | 1 | `[1]` | PASS |
| `acta.aas.016.aas-016-l09817` | `la` | `194e0d73f3972efe19942173cab132c4969b59ec2884784068f6ef1aa47188b3` | 2 | `[1,2]` | PASS |
| `acta.aas.016.aas-016-l19183` | `la` | `17f7cb561944546a306d876833efe64f76641dee9f2ae4db0d6f59ba31428bc4` | 1 | `[1]` | PASS |
| `acta.aas.018.aas-018-l15835` | `la` | `27eb01ea64ce4a0bd2bdfabdb6e0d4624bcd5adefc5ea30ac4148d4de69005e4` | 1 | `[1]` | PASS |
| `acta.aas.020.aas-020-l13717` | `la` | `700769a7f9eb2ad9ec042049f7f333cebdf402c8ee0f4eb44a71d8e8a457dd77` | 1 | `[1]` | PASS |
| `acta.aas.021.aas-021-l26451` | `la` | `f2dbd3dd7dfec1a0d322fa411f816c1ef5c74d744df34b7611d06fdce86571c7` | 1 | `[1]` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l13545` | `la` | `212003dae8fd6e828f5f4c2f1e7594939bacc3fb97e4b027b27f4402d7db9ed3` | 2 | `[1,2]` | PASS |
| `acta.aas.001.archive.aas.001.010` | `la` | `4a8a9afb4d10755818df02a44e70c2083b959eaa47f89015b21103b548f7b69e` | 1 | `[1]` | PASS |
| `acta.aas.001.archive.aas.001.081` | `la` | `e1a01106c8b5b2cb270a490e15b7c6dd542e60d231f06f1bff26839536a3b21e` | 2 | `[1,2]` | PASS |
| `acta.aas.001.archive.aas.001.082` | `la` | `872bdf36b1c0677e83a0f0bc30876d85967979cd508ecfd97e9a7894b9a73bd1` | 1 | `[1]` | PASS |
| `acta.aas.002.archive.aas.002.053` | `la` | `ae044d0bfc07dce5c2f1ea5a0c7b050050023097ec83186cc5884bb48f24b2da` | 1 | `[1]` | PASS |
| `acta.aas.003.archive.aas.003.011` | `la` | `09b2c68037d105a54358c0bbaaad10a26c1c1d553e022a19d765a7ab44e5e73d` | 1 | `[1]` | PASS |
| `acta.aas.003.archive.aas.003.083` | `la` | `56ce7d152e6b0763550ed11631005a49a957e1a86d15bb83047956b87f8437bd` | 1 | `[1]` | PASS |
| `acta.aas.004.archive.aas.004.022` | `la` | `638288c4b26d7f4677fac484183eb4a2328f8a3adbc4a14ed73cb4975475a906` | 2 | `[1,2]` | PASS |
| `acta.aas.004.archive.aas.004.056` | `la` | `ae6bb617a10f2a035d1d39fc8135d0273df6e836858a119843f2b724c3f69876` | 1 | `[1]` | PASS |
| `acta.aas.006.archive.aas.006.006` | `la` | `18a016e852ae7c4e73412dc71099c0f097b646e317aa757aeae220ef4cca6f41` | 1 | `[1]` | PASS |
| `acta.aas.007.archive.aas.007.035` | `la` | `ea3b54e0cc356276cba9a03976c8038a82e29e0abb2cecccbd9e45a76593c5ac` | 1 | `[1]` | PASS |
| `acta.aas.009.i.archive.aas.009.i.l013555` | `la` | `01651cbc87555e86894a522ca9de409fc955edf11b82a8cfb674bdb397ef0428` | 2 | `[1,2]` | PASS |
| `acta.aas.012.archive.aas.012.l008747` | `la` | `b3c28b0a2ac92dddf08aba303f806378bd5f181c20a7bb44cfe66bb2ebd27ba8` | 4 | `[1,2,3,4]` | PASS |
| `acta.aas.013.archive.aas.013.l010453` | `la` | `bcba4844b8a7e05d985dfedc8a8a9868230a0b8ad6cf4f31526903828e4e6398` | 2 | `[1,2]` | PASS |
| `acta.aas.015.archive.aas.015.l021281` | `la` | `d98249ccf3f07948a8924476cad90c70859aafad997dc5c4f4a39f00e5052a4d` | 1 | `[1]` | PASS |
| `acta.aas.019.aas-019-l05435` | `la` | `dea48ecce01d301f1d92387311b4b405d2ccf69b7fa9818c39eef011bd1b7e05` | 2 | `[1,2]` | PASS |
| `acta.aas.019.aas-019-l13198` | `la` | `e7008628e313cab733e0468b55537cc1ce3f1dd7069b1c4aefc514891f679996` | 1 | `[1]` | PASS |

## Page observations

### acta.ass.003.ass-003-apostolici-nostri (la) — PASS

- p1: Compact title and Pius IX/date/Latin line remain clear of both columns. Papal dating/subscription and the historical retraction note precede readable project source notice and rights colophon in the right column. Retained OCR joins, carets and spaced digits are qualified source features.

### acta.ass.007.ass-007-act-017 (la) — PASS

- p1: Title, Pius IX/date/Latin identification and historical apostolic-letter heading are clear; preserved spaced-letter OCR remains readable within columns.
- p2: Dense two-column continuation keeps margins and gutter clear, with no isolated heading or missing-glyph box observed.
- p3: Substantive closing clauses, historical note, dating and subscriptions precede readable source notice/rights in right column; source notice explicitly retains the 1873 act dating against surrounding ASS 7 (1872) attribution.

### acta.ass.011.ass-011-act-006 (la) — PASS

- p1: Title and Leo XIII/date/Latin line agree with visible issuer heading; source close/date/subscription sit above source notice, which continues cleanly at top of right column before rights. Retained quote/OCR anomalies are qualified.

### acta.ass.017.ass-017-act-001 (la) — PASS

- p1: Title and Leo XIII/date/Latin line remain distinct from retained encyclical heading and two-column body; spaced source capitals stay within columns.
- p2: Substantial closing paragraphs/date and Leo XIII signature precede readable source notice and rights in left column; no furniture-only ending.

### acta.ass.028.ass-028-l00045 (la) — PASS

- p1: Compact title/Leo XIII/date/Latin line and retained letter heading agree visibly. Spaced-letter OCR stays within columns; dating and Leo XIII signature precede readable source notice and rights in right column.

### acta.ass.033.ass-033-l07481 (it) — PASS

- p1: Italian identification matches main Italian letter following retained Latin editorial heading; title and Leo XIII/date line fit clearly above columns. Source OCR spacing remains.
- p2: Substantial Italian conclusion, date and Leo XIII signature remain in left column; source notice continues at top of right column before readable rights.

### acta.ass.036.ass-036-l007763 (la) — PASS

- p1: Two-line title and Leo XIII/date/Latin line fit above source text. Entire source, closing/date and cardinal subscription, source notice and rights fit left column with ample white space.

### acta.ass.039.ass-039-l000792 (la) — PASS

- p1: Three-line mixed-case title and Pius X/date/Latin line fit above source heading. Source close/date and Pius X subscription precede readable source notice/rights in left column. The 1904 act date and ASS 39 (1906) source year are retained explicitly; OCR spelling remains qualified.

### acta.ass.040.ass-040-l007377 (la) — PASS

- p1: Two-line title and Pius X/date/Latin identification fit above retained beatification heading; spaced source letters remain inside columns.
- pp2–3: Dense continuation preserves separated columns and clear margins despite pervasive spaced-letter OCR.
- p4: Sparse final page retains substantive conclusion, dating and cardinal subscription above readable source notice/rights; no furniture-only ending.

### acta.ass.040.ass-040-l012123 (la) — PASS

- p1: Three-line title and Pius X/date/Latin identification fit clearly. Extended Italian historical note signed Cardinal Merry del Val occupies much of left column within Latin papal text; language label describes the main act and needs this qualification. Papal date/signature and source notice/rights fit right column; retained spaced OCR and dot remain qualified.

### acta.aas.009.i.archive.aas.009.i.l000030 (la) — PASS

- p1: Two-line title and Benedict XV/date/Latin line fit; historical letter heading and issuer agree visibly. Source close/date and cardinal subscription precede readable notice/rights in right column, with clear gutter and margins.

### acta.aas.010.archive.aas.010.l013291 (it) — PASS

- p1: Six-line Latin synopsis title fits above Benedict XV/date/Italian line; main body is Italian with retained Latin editorial heading. Dating and Benedict XV signature precede readable source notice/rights in right column; no visible attribution conflict.

### acta.aas.009.i.archive.aas.009.i.l017737 (la) — PASS

- p1: Four-line title and Benedict XV/date/Latin identification fit; complete source text/date and cardinal subscription precede readable notice/rights in left column, leaving clear white space.

### acta.aas.011.archive.aas.011.l014474 (la) — PASS

- p1: Four-line synopsis title and Benedict XV/date/Latin line remain clear of source heading/body. Pervasive spaced-letter OCR stays within columns; dating, papal signature, notice and rights fit right column.

### acta.aas.012.archive.aas.012.l016158 (la) — PASS

- p1: Four-line synopsis and Benedict XV/date/Latin line fit above historical encyclical heading; incipit Spiritus Paraclitus and issuer are visible without collision.
- pp2–10: Dense Latin body and numerous retained inline references remain inside separated columns; literal backslashes, dots, carets and broken words remain qualified OCR features.
- pp11–12: Garbled retained fragments are especially conspicuous near p11 right-column lower references and p12 reference groups; no clipping, collision or missing-glyph box observed.
- p13: Substantive concluding paragraphs/date and Benedict XV subscription precede readable project source notice and rights in right column; no sparse/furniture-only ending.

### acta.aas.013.archive.aas.013.l000230 (la) — PASS

- p1: Three-line title and Benedict XV/date/Latin line fit; source epistle heading is followed by complete body/date and papal signature in left column, then readable source notice/rights. Retained spaced-letter OCR remains qualified.

### acta.aas.014.archive.aas.014.l001367 (la) — PASS

- p1: Four-line title and Benedict XV/date/Latin line remain clear of source epistle heading/body. Dating and Benedict XV signature precede readable notice/rights in right column; 1921 act date is distinct from AAS 14 (1922) source year.

### acta.aas.015.archive.aas.015.l001125 (la) — PASS

- p1: Four-line title and Pius XI/date/Latin line fit above source heading; source dates and cardinal subscription are intact above notice, which continues cleanly at top of right column before rights. Spaced OCR remains qualified.

### acta.aas.016.aas-016-l09817 (la) — PASS

- p1: Three-line title and Pius XI/date/Latin line fit; source heading/body continue through two separated columns with retained OCR spacing and dot.
- p2: Substantial conclusion/date and Pius XI subscription precede readable source notice/rights in left column. The letter mentions an attached law; this bounded visual review does not establish inclusion of that separate annex beyond the selected papal letter.

### acta.aas.016.aas-016-l19183 (la) — PASS

- p1: Four-line title preserves malformed AI)/THEQDOSTENSEM source spelling; Pius XI/date/Latin line stays clear of body. Source dot/backslash and spaced letters remain qualified; close/date, Pius XI signature, notice and rights fit right column.

### acta.aas.018.aas-018-l15835 (la) — PASS

- p1: Two-line title and Pius XI/date/Latin line fit above source numbered heading/body. Clear two-column flow reaches dating/cardinal subscription and readable notice/rights in right column.

### acta.aas.020.aas-020-l13717 (la) — PASS

- p1: Three-line title includes retained HI heading debris, also visible above source heading; Pius XI/date/Latin line and columns remain clear. Dating and cardinal subscription precede readable source notice/rights in right column.

### acta.aas.021.aas-021-l26451 (la) — PASS

- p1: Three-line title and Pius XI/date/Latin identification fit above numbered source heading; source closing/date and cardinal subscription lead to readable notice/rights at top of right column. Retained OCR asterisks and spacing remain qualified.

### acta.aas.022.issues-01-12.aas-022-l13545 (la) — PASS

- p1: Three-line beatification title and Pius XI/date/Latin line fit; source heading and dense body preserve clear columns. Retained OCR such as RENUNTIANTUR remains qualified.
- p2: Substantive concluding provisions/date and Cardinal Pacelli subscription precede readable source notice/rights in right column; source notice explicitly identifies bounded earlier-1930 fascicle selection.

### acta.aas.001.archive.aas.001.010 (la) — PASS

- p1: Three-line title retains CONDECORATÜR OCR; Pius X/Latin line agrees with visible issuer. Source dated subscription and cardinal signature precede clear source notice/rights in right column; absent compact date follows undated assignment metadata.

### acta.aas.001.archive.aas.001.081 (la) — PASS

- p1: Three-line title and Pius X/Latin identification fit above source heading; dense body/references preserve clear columns despite retained brackets, quotation anomalies and broken words.
- p2: Substantive conclusion/date and Pius X subscription precede readable source notice/rights in left column; no furniture-only ending. Source notice lists printed pages 761, 763; no facsimile completeness inference made from those labels.

### acta.aas.001.archive.aas.001.082 (la) — PASS

- Page 1: The two-line spaced-capital title and Pius X / Latin label fit above the source heading. The complete body, dated closing of 17 September 1909, Cardinal Merry del Val subscription, Source notice and rights text remain readable in the columns; no clipping, overlap or missing-glyph boxes seen.

### acta.aas.002.archive.aas.002.053 (la) — PASS

- Page 1: The two-line title and Pius X / Latin label fit. The letter, closing dated 9 May 1910 and Pius X signature precede the readable Source notice and rights text in the left column. Retained soft-hyphen / OCR word breaks are source limitations; no layout obstruction seen.

### acta.aas.003.archive.aas.003.011 (la) — PASS

- Page 1: The two-line title and Pius X / Latin label fit above the complete letter. The closing dated 14 November 1910, Pius X signature, AAS 3 (1911) source reference and rights notice remain readable in the left column. No clipping, overlap, detached heading or furniture-only ending seen.

### acta.aas.003.archive.aas.003.083 (la) — PASS

- Page 1: The three-line title and Pius X / Latin label fit. Both columns remain distinct through the closing date, Cardinal Merry del Val subscription, Source notice and rights colophon in the right column. Retained hyphenation, asterisk and caret OCR forms are visible source limitations; no clipping or collision seen.

### acta.aas.004.archive.aas.004.022 (la) — PASS

- Page 1: The four-line title and Pius X / Latin label fit above the source heading and full columns. French devotional names and quotations within the Latin act remain readable; retained broken words are qualified OCR.
- Page 2: The numbered provisions continue through the substantive conclusion, dated closing and Cardinal Merry del Val subscription. Source notice and rights colophon fit in the right column; no isolated heading, clipping, collision or apparatus-only terminal page seen.

### acta.aas.004.archive.aas.004.056 (la) — PASS

- Page 1: The three-line title and Pius X / Latin label fit. The letter flows clearly through both columns to the dated closing and Pius X signature; Source notice and rights colophon remain readable below in the right column. Retained word-break hyphens and a caret are qualified OCR; no clipping or collision seen.

### acta.aas.006.archive.aas.006.006 (la) — PASS

- Page 1: The five-line title and Pius X / Latin label fit above the source heading and letter. Closing date, Pius X signature, Source notice and rights colophon remain readable in the left column. Odd source-title spelling, punctuation and diacritics are retained OCR; no missing-glyph boxes or title-only page seen.

### acta.aas.007.archive.aas.007.035 (la) — PASS

- Page 1: The six-line title and Benedict XV / Latin label fit above the complete letter. The dated closing, Benedict XV signature, Source notice and rights colophon remain readable in the left column. Retained title spelling and broken words are qualified OCR; the ample whitespace causes no detached heading or furniture-only ending.

### acta.aas.009.i.archive.aas.009.i.l013555 (la) — PASS

- Page 1: The three-line title and Benedict XV / Latin label fit above the source heading and complete two-column body. Retained broken words, spaced numerals and separator-like OCR debris remain legible source limitations. Closing date remains in the right column without clipping or overlap.
- Page 2: Very sparse closing spill: the historical Cardinal Gasparri subscription is the first line, followed by the readable Source notice and rights colophon. PASS qualified because the terminal page retains a source subscription; it is not a source-free or apparatus-only ending.

### acta.aas.012.archive.aas.012.l008747 (la) — PASS

- Page 1: The four-line title and Benedict XV / Latin label fit above the encyclical heading and visible papal identification. The two columns and inline source references remain distinct; malformed breaks and reference digits are qualified OCR.
- Page 2: Dense continuation remains within clear columns and margins. Source-reference strings, quotation fragments and broken words are retained OCR; no physical overlap, clipping or missing-glyph boxes seen.
- Page 3: Dense continuation and inline references remain legible in the intended columns. Carets, slashes, parentheses and broken words are source limitations; no detached heading or page-layout obstruction seen.
- Page 4: Substantive conclusion, dated closing, Benedict XV subscription and final source references remain in the left column. Source notice starts below and continues at the top of the right column before the readable rights colophon. No source-free terminal page seen.

### acta.aas.013.archive.aas.013.l010453 (la) — PASS

- Page 1: The three-line title and Benedict XV / Latin label fit. The historical constitution heading and papal identification are visible; two dense columns remain clear despite pervasive source OCR letter spacing, title spelling and an embedded volume/page line.
- Page 2: Substantive closing clauses, source date, cardinal and protonotary subscriptions, seal/register wording precede the readable Source notice and rights colophon in the left column. Retained copyright-like and bullet/caret OCR marks are source features; no clipping or furniture-only ending seen.

### acta.aas.015.archive.aas.015.l021281 (la) — PASS

- Page 1: The four-line spaced-capital title and Pius XI / Latin label fit above the source heading and papal identification. Body continues from the full left column into the dated closing and Cardinal Gasparri subscription at the top right, followed by readable Source notice and rights colophon. Spaced OCR words, numerals and a caret remain qualified; no clipping or collision seen.

### acta.aas.019.aas-019-l05435 (la) — PASS

- Page 1: The two-line title and Pius XI / Latin label fit above the numbered historical heading and papal identification. Dense two-column body has clear margins and gutter; retained spaced words and word-break hyphens are source limitations.
- Page 2: Substantive closing, source date, cardinal/protonotary subscriptions and seal/register lines precede the Source notice and rights colophon. Pound-sign/digit-like OCR forms and source spacing remain visible and uncorrected. No source-free ending, clipping or overlap seen; provenance notice explicitly retains the no-facsimile-collation limit.

### acta.aas.019.aas-019-l13198 (la) — PASS

- Page 1: The three-line title and Pius XI / Latin label fit above the source heading and visible papal identification. The full left column reaches the dated closing and Cardinal Gasparri subscription, then the Source notice continues from its bottom into the right column before the readable rights colophon. Retained numeral/letter spacing is qualified OCR; no clipping, overlap or furniture-only page seen.

No PDF, raster, source text, source metadata or typesetting tool was changed by this review. Replacement bytes require a separate review against their exact hashes.
