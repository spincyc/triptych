# Pius IX Acta visual review — batch pius-0001, lane 08

CHANGES_REQUIRED: 22 assigned PDFs, 65 pages individually opened at full size; 21 PASS, 1 CHANGES_REQUIRED. All inspections are new; zero reused pages. All documents come from *Pii IX Pontificis Maximi Acta*, pars prima, volume III (Rome, 1864).

## Blocking finding

- `pius-ix-acta.volume-03.line-00021313.part-01` (*Omnibus notum*, consistorial allocution, 1863-03-16), page 1, right column, about two-thirds of the way down: a stray source gathering-signature/folio numeral **`36`** is set as its own body line. It splits the word *ma-/gis* ("…permanens quotidie ma- | 36 | gis vigeat, et efilorescat…"). The container OCR (`ocr-3a788e20d82b`, lines 21414-21421) has `36` and the folio `560` at this source page break. The selection range `[21384, 21418]` ends at line 21418, so it keeps line 21416 (`36`) while the next range starts at 21420 and omits the folio. The source review records such furniture as omitted. Under the standing ruling for boundary-reviewed Pius IX series, a folio or running-head numeral left in the body is BLOCKING.

## Scope and method

Each assigned page PNG, produced earlier by the repository `pdf-review` tool, was opened one image per page at full size (1700×2200) with the Read tool. No contact sheet, thumbnail, re-rasterization, source edit or text correction was used. Extracted PDF text (`pdftotext -layout`, kept in the lane directory) and the container OCR were consulted only to locate and confirm visual observations. The checks covered: the displayed title, responsible issuer, date and language label against the frozen metadata; headings, two-column flow, gutters, margins and glyphs; natural source closing; modern provider signatures; running heads and folio/signature furniture; fused marginal summaries or notes; and raw placeholders.

No visible clipping, overlap, tofu or missing-glyph blocks, collapsed tables, stranded headings, modern digitizer signatures (no "Digitized by Google" or variant), raw `None` placeholders, or apparatus-only final pages were found. Every final page carries genuine source closing (dating clause, subscriptions or the source's own notes) before the compact Source/rights apparatus.

## Evidence verification

Every assigned PDF, the receipt, the frozen manifest, the raster-run record and all 65 page PNGs were hashed before and after inspection. All 90 digests matched the assignment pins both times.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt (`.scratch/typeset_pipeline/claude/pius-0001/receipt.json`) | `720d0acae7c1f32315fd11d968d13eaa0510b72ea25906a6916054bd2ada2d73` | Before and after |
| Frozen manifest (`.scratch/typeset_pipeline/claude/pius-0001/frozen-manifest.json`) | `583691e3d8941ca1c9a3a3f27f4cc57747afcfb3b3817776aad37a103df9d736` | Before and after |
| Raster run (`.scratch/claude-review/rasters-pius-0001/review-run.json`) | `5718cc943c5d94fdf4a333529ce03aa4e55089d3d90a4801f03abb5e9597e7c6` | Before and after |
| Lane assignment | `ab67b2857281fd4caac9cc481f521174b92306b376b66be52dde0fda4a5ccb7c` | Scope binding |
| Observation ledger (65 unique page records) | `eb9d02ee48add481528d6e8920928b8bf96a73237153e2d64623b5bd7fb51c99` | Final |
| Before verification record | `70abe4823925f6436e1cb3406c46699a41ebe9102cea2f5a49dc72602be63c36` | all_match true |
| After verification record | `6624ae64923f40270404cc53ab2a2bbbedefdec0f1b06d7d329944243a182be8` | all_match true; identical input hashes |

## PDF outcomes

| Document | Lang | Date | Pages | PDF SHA-256 | Status |
| --- | --- | --- | --- | --- | --- |
| `pius-ix-acta.volume-03.line-00017185.part-04` | la | 1862-07-10 | 9 | `0640a89f8e96ddba30ff29c0c51e5cc69566255833d9b39b631b915f0f8340d2` | PASS |
| `pius-ix-acta.volume-03.line-00017185.part-05` | la | 1862-07-10 | 5 | `7032a844a8ebb01fb5277cdceb0ee1234e83f5ac1613a198529571d6e2339db3` | PASS |
| `pius-ix-acta.volume-03.line-00017185.part-06` | la | 1862-07-10 | 4 | `a24b3fbef2b64d3638b953b3d05d07212d575de0fe1c8204f3940cbaf13caaf7` | PASS |
| `pius-ix-acta.volume-03.line-00017185.part-07` | la | 1862-10-18 | 1 | `79b131f62cfcb61042519dc687832cec40a3d6033b38b36937da00a2aee08e64` | PASS |
| `pius-ix-acta.volume-03.line-00017185.part-08` | la | 1862-12-01 | 5 | `fb31c38def7cc6b3f3a77c1f2e85c4f39b9f5cdeee0cd95292bd96e754a1938b` | PASS |
| `pius-ix-acta.volume-03.line-00017185.part-09` | la | 1862-12-11 | 3 | `b157d5bb183dfd12f67dffec31b3360150843b28bcff51b827bbd7361b643411` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-01` | la | 1863-03-16 | 2 | `da70b3b5789beb821b2bf983adf33bc657f062c17a483541be0ce3b47c05587d` | CHANGES_REQUIRED |
| `pius-ix-acta.volume-03.line-00021313.part-02` | it | 1863-04-22 | 3 | `c08fa8c7dd4cc0b24c632eb52befdc0b54ac0c6ba350940d84bb0583e8a86a03` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-05` | la | 1863-06-01 | 2 | `b2e5192c524ed152c261302380ada281f99504d9b7151ef39bf3712e68b5688d` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-06` | la | 1863-06-15 | 1 | `fab62380ab881572c1e27033e5ac334345d1b6384c0281d42aa356e7b9ac4310` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-07` | la | 1863-08-10 | 4 | `776ce3d877e01724e7c3b62d4828a1eec019ab8f814ef35076a3cf2b4ade11d2` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-08` | la | 1863-09-17 | 2 | `a8197aae31a134f5a645271368593e55a170322917a0a852d58571a7e58ec983` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-09` | la | 1863-09-25 | 1 | `b92221c79a730788dff48b12a3cda3af071c29627ad03aede70d26c7cc0543a3` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-10` | la | 1863-11-30 | 2 | `4f61d556762d80c1eb419ba3ecdbf12677053650d74e2de8409988500b74e47d` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-11` | la | 1863-12-21 | 3 | `14de2232958765c169d37836be9cea2cbacac5223ab33e65f6006fb785c0019a` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-12` | la | 1864-03-17 | 2 | `1723b3f2486d8481cc3dc66ec8af290f41dfde0e1fd038e122ceb1656de04212` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-13` | la | 1864-07-14 | 2 | `597f34647924900e46efbfb9bbaf66d8fcc585f2a2c7b53e91663a619ef29265` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-14` | la | 1864-07-30 | 3 | `0a68b11162b09679b42f83434fea1e33c4d630ebce1663929e782eba35627952` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-15` | la | 1864-08-02 | 3 | `e55f3386ff59d39c012b965954291af0efba2b8fc854e2e885bcd742d763f1cb` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-16` | la | 1864-08-18 | 2 | `85ca40665c6bcad9ef705fe34bf4ca3c28f8f902d494c43e1d97d829d333f46d` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-17` | la | 1864-08-19 | 2 | `f12498da873d29fb46906dfef52c4411bde2ebf765828e0484ecabbc9f0a35d9` | PASS |
| `pius-ix-acta.volume-03.line-00021313.part-18` | la | 1864-12-08 | 4 | `42432ae24f0848bcec1b6dab73a5d7703b443b100ba5c6e598a1bb1c6e7013cb` | PASS |

## Per-document findings

### `pius-ix-acta.volume-03.line-00017185.part-04` — PASS

*Canonizatio martyrum Iaponensium Ordinis S. Francisci (bulla)*; issuer `PIVS EPISCOPVS BERVUS SERVORUM DEI`; 1862-07-10; bull; language `la`. Prior finding: none.

- p1 PASS — PNG `e5e5a509bc910b598026313584ae02632f208854f1259d07f306e55e4bab92b0` — Title, issuer (frozen OCR spelling BERVUS), 1862-07-10, Latin match metadata; protocol and sections 1-5 flow in two balanced columns; no clipping, overlap or furniture.
- p2 PASS — PNG `76b20455ba43034e3d9490cd12f9e44f8bc6de5dfa51a47ccbbf7a3c4d8280d9` — Sections 5-10 continue in normal two-column order; source page-break paragraph restarts only; no folio, running head or digitizer line.
- p3 PASS — PNG `733da82f828adb6986378811cb7df2e0045edcb292ff39d540d33cd2552fdb8f` — Sections 11-18 clean two-column flow; stray OCR bar marks are literal; no furniture.
- p4 PASS — PNG `a7010e60af7094a8ddb8abdc4d3cdf595825ffa9e2badcfc062286d9eec208b7` — Sections 18-26 clean; no clipping, overlap, running head or fused marginal.
- p5 PASS — PNG `2c99fff59b0068710de75131a0ad10e091c7bae01de7a287f0ea7fb1e5c9ffed` — Sections 27-34 clean two-column flow; literal OCR section-sign damage only.
- p6 PASS — PNG `6fa09a5e94a54dc8ba4d0b87c1f14d64ebe208df1b40b79e8bb47a9eee3aa137` — Sections 34-39 clean; no furniture or glyph faults.
- p7 PASS — PNG `cfedd3478ca7562c80fefd473f2c703330adfcae0022118c958c35fc67f68757` — Sections 39-45 including canonization formula; clean flow.
- p8 PASS — PNG `64659041664e594d78e19ef04571cfc60e3326e34bf5e02ee75bd3fe4d9bdc86` — Sections 45-48, dating clause (VI Idus Julias, anno XVII), papal and cardinal subscriptions with literal OCR cross marks; no furniture.
- p9 PASS — PNG `625fef496df89886a62823d2826d87d73a6de2b093d3e2a51070d4fb8974238f` — Final page: remaining cardinal subscriptions, datary/plumbum/registration lines (genuine source closing), then compact Source and rights apparatus; not apparatus-only.

### `pius-ix-acta.volume-03.line-00017185.part-05` — PASS

*Canonizatio martyrum Iaponensium e Societate Iesu (bulla)*; issuer `PIVS EPISCOPVS SERVUS SERVORVM DEI`; 1862-07-10; bull; language `la`. Prior finding: none.

- p1 PASS — PNG `c6b6cc8ed1e9f749b31b726424096b984eb719e307724e52f43f52b992ea737c` — Title, issuer PIVS EPISCOPVS SERVUS SERVORVM DEI, 1862-07-10, Latin match metadata; protocol and sections 1-5 in clean two-column flow.
- p2 PASS — PNG `c404192b3730cfd1cb16fe582b3e90a8b189eed79bcc20c45263ace8d2e33880` — Sections 5-9 continue cleanly; no furniture, clipping or overlap.
- p3 PASS — PNG `d4e07e4605d42430aa9c7a128ebc98ef41cfed55710a212dc4bbec2ae5d105c0` — Sections 10-15 clean two-column flow; literal OCR only.
- p4 PASS — PNG `257300aae622b2aa7e995a8e6f9aa7b55f9a4ab06fd9ecc971a965e1cc6b9a88` — Sections 15-20 including canonization formula; stray OCR letter E at a source line break is literal; no running head or folio.
- p5 PASS — PNG `dfb35662fd38a95677b18b93e9bc16bb373a3b7d49388f107bb19883638b104a` — Final page: sanctio, dating clause (VI Idus Julias MDCCCLXII, anno XVII), papal subscription and note on following subscriptions (genuine source closing), then Source/rights apparatus.

### `pius-ix-acta.volume-03.line-00017185.part-06` — PASS

*In Dei proximique amore — canonizatio Michaelis de Sanctis (bulla)*; issuer `PIUS EPISCOPUS SERVVS SERVORYM DEI`; 1862-07-10; bull; language `la`. Prior finding: none.

- p1 PASS — PNG `1883f070ad85c93e042067df1632a3adc236f0cdfd6f8db68549c77794a56da6` — Title (two-line wrap, clean), issuer PIUS EPISCOPUS SERVVS SERVORYM DEI, 1862-07-10, Latin match metadata; protocol and sections 1-9 flow cleanly.
- p2 PASS — PNG `eb54a1351bff84af8790126cd0dd930c8fac60b5161048b420262ecfe843b89c` — Sections 5-11 clean two-column flow; no furniture or glyph faults.
- p3 PASS — PNG `379010cc4fb32ee746b0ceef961aa4162f84422c84f832617c44b25619b69648` — Sections 11-14 clean; source page-break paragraph restarts only; no running head or folio.
- p4 PASS — PNG `fd9ae2ec66fbbc1e513b3b369581dbdbeede73d348d0b93e0e73e7ddc73db1a9` — Sections 14-16, sanctio, dating clause (VI Idus Julias MDCCCLXII, anno XVII), papal subscription and source note on following subscriptions, then Source/rights apparatus in right column.

### `pius-ix-acta.volume-03.line-00017185.part-07` — PASS

*Gravissimas inter ac multiplices — ad archiepiscopum Neo-Eboracensem*; issuer `PIVS PP. IX.`; 1862-10-18; letter; language `la`. Prior finding: none.

- p1 PASS — PNG `70d9ab1281a8bef86caa85c388ac77b5d039431ac6e8c7861802b9bed7eef0e8` — Single page: title (two-line), issuer PIVS PP. IX., 1862-10-18, Latin match; protocol, body, dating clause (die 18 Octobris 1862, anno XVII), then Source/rights apparatus; clean two-column flow, no furniture.

### `pius-ix-acta.volume-03.line-00017185.part-08` — PASS

*Senogalliensis civitatis ac dioecesis — de rebus Senogalliensibus (bulla)*; issuer `PIVS EPISCOPVS SERYUS SERVORUM DEI`; 1862-12-01; bull; language `la`. Prior finding: none.

- p1 PASS — PNG `69ff2a730bebb51f2602659646435547ce75e6f8ea314e9155b730387a1e9e0a` — Title (two-line), issuer PIVS EPISCOPVS SERYUS SERVORUM DEI (OCR spelling matches metadata), 1862-12-01, Latin; protocol and body in clean two columns.
- p2 PASS — PNG `367b59d03b36fdbde7110f067ff6550dd4112444faf617a889e182036fe8a12c` — Body continues in clean two-column flow; source page-break paragraph restarts only; no folio, running head or digitizer line.
- p3 PASS — PNG `78aed6e563a88b2185cef31e285a64a1898bbe963b534cde273034f8ed799381` — Body continues; clean columns, no furniture or glyph faults.
- p4 PASS — PNG `f7cc552b804b93228ef7d72b42946d2ffbe85ad1fd951af324bae6b000e61338` — Body and derogation clauses continue; clean flow; no running head or folio.
- p5 PASS — PNG `b368071be9fcac02cfdedb2577dc7c3325d0082fd8262031eb3f62a72b8ead0d` — Final page: derogation end, sanctio, dating clause (Kalendis decembris 1862, anno XVII), datary/plumbum/registration subscriptions (genuine source closing), then Source/rights apparatus.

### `pius-ix-acta.volume-03.line-00017185.part-09` — PASS

*Gravissimas inter — ad archiepiscopum Monacensem de Frohschammeri erroribus*; issuer `PIUS PP. IX.`; 1862-12-11; letter; language `la`. Prior finding: none.

- p1 PASS — PNG `6fcf44bdf99ce0fa0492a65df8f8d3d3082bb464d85502848bdd84b875a344ee` — Title (two-line), issuer PIUS PP. IX., 1862-12-11, Latin match; protocol and body in clean two columns; no furniture.
- p2 PASS — PNG `3ae8fd9d1900665fc502d6dfbc916cb3fc1d4c9b3e72db70dbf906798a64e5c4` — Historical footnotes set as their own separate blocks at source page breaks (left column after 'multi-' and after 'oh-'; right column after 'principiis,'), not fused into body lines: non-blocking per standing ruling. No running head, folio or digitizer line.
- p3 PASS — PNG `ea1d016b29200a84d7c4467829540cac6abb057bba7441a013fc03757d1c6dee` — Body to close, dating clause (die 11 Decembris 1862, anno XVII), then Source/rights apparatus in right column; clean flow.

Recorded findings and qualifications:
- p2: Non-blocking: historical footnote blocks at source page breaks (left col: '(1) Col. 1. 26.' between 'multi-' and 'fariam'; '(à) Heb. v. 19.'-'(4)' between 'oh-' and 'voluta'; right col: patristic note block between 'principiis,' and 'seu methodo').

### `pius-ix-acta.volume-03.line-00021313.part-01` — CHANGES_REQUIRED

*Omnibus notum — allocutio in consistorio secreto 16 martii 1863*; issuer `PII IX. — PONTIFICIS MAXIMI ACTA`; 1863-03-16; consistorial-allocution; language `la`. Prior finding: none.

- p1 CHANGES_REQUIRED — PNG `cad329fc8565e1ec3ba158b6e1c3f404595717675bde692b363c08e7fc13f891` — Title, 1863-03-16 and Latin match; issuer line 'PII IX. — PONTIFICIS MAXIMI ACTA' is the volume-title attribution context matching metadata (non-blocking qualification). BLOCKING: a stray source folio/gathering-signature numeral '36' is set as its own body line in the right column, splitting the word 'ma-/gis' (…quotidie ma- | 36 | gis vigeat…).
- p2 PASS — PNG `5f3af565cbef8e1d7d330b172ac70cc0616585bc912385d6f8204e551b7e4d5c` — Body continues to cardinal creation formula and Trinitarian closing (genuine source closing), then Source/rights apparatus in right column; no furniture on this page.

Recorded findings and qualifications:
- p1: BLOCKING: source folio/signature furniture '36' left inside the body — page 1, right column, about two-thirds down, between 'permanens quotidie ma-' and 'gis vigeat, et efilorescat', splitting the word 'magis'.
- p1: Non-blocking qualification: issuer taken from volume title 'PII IX. — PONTIFICIS MAXIMI ACTA' (matches frozen metadata).

### `pius-ix-acta.volume-03.line-00021313.part-02` — PASS

*Non deve meravigliare — all'imperatore di Russia*; issuer `Pius Papa IX.`; 1863-04-22; letter; language `it`. Prior finding: none.

- p1 PASS — PNG `49642fbf20c07d4960a11eed90288168f86668802aa5e4d885071044534acea5` — Title, issuer Pius Papa IX., 1863-04-22, Italian label match metadata (it); address and body in clean two columns; no furniture.
- p2 PASS — PNG `391f489320843d8e0965d5032f2c711513f8f221d9a987c6d22c6de9ec7b92ff` — Body continues; clean flow; no running head, folio or digitizer line.
- p3 PASS — PNG `e80296f803727fb503604e442c39b0399ad2b5b8de9076150383d99a8ede02fe` — Body to close, dating clause (22 Aprile 1863) and signature Pius Papa IX. (genuine source closing), then Source/rights apparatus.

### `pius-ix-acta.volume-03.line-00021313.part-05` — PASS

*In gravissimis Nostris acerbitatibus — ad episcopum Tridentinum*; issuer `| PIVS PAPA IX.`; 1863-06-01; letter; language `la`. Prior finding: none.

- p1 PASS — PNG `c0f6f938211afe74006772573d9c042e8c2f44774b537b8009a4485d562506c7` — Title (two-line), 1863-06-01, Latin match; issuer line '| PIVS PAPA IX.' carries a stray OCR bar that matches frozen metadata (non-blocking qualification). Protocol and body in clean two columns; right column ends about 40% short of the foot before the closing moves to page 2 (unbalanced break; reading order intact, no text lost, non-blocking).
- p2 PASS — PNG `1b46399dcaf160a6611be52a0ae6c212eae1c0031a43c70048693a33f248a136` — Final page: end of body, dating clause (die 1 mensis Iunii 1863, anno XVII) as genuine source closing, then Source/rights apparatus.

Recorded findings and qualifications:
- p1: Non-blocking qualification: issuer line '| PIVS PAPA IX.' with stray OCR bar, matching metadata.
- p1: Non-blocking layout note: right column of page 1 ends early (after 'quam ex intimo corde profectam'), continuation on page 2; reading order intact.

### `pius-ix-acta.volume-03.line-00021313.part-06` — PASS

*Qua singulari prorsus laetitia — ad episcopum Tridentinum*; issuer `PIVS PP. IX.`; 1863-06-15; letter; language `la`. Prior finding: none.

- p1 PASS — PNG `0870686cd96918ae0ff6e924e4a7d00b80269a7566b3d460ee71b35aa7188d90` — Single page: title, issuer PIVS PP. IX., 1863-06-15, Latin match; protocol, body, dating clause (die 15 Junii 1863, anno XVII); Source/rights apparatus begins at foot of left column and continues at top of right column in normal order.

### `pius-ix-acta.volume-03.line-00021313.part-07` — PASS

*Quanto conficiamur moerore — ad cardinales et episcopos Italiae*; issuer `| PIUS PAPA IX.`; 1863-08-10; encyclical; language `la`. Prior finding: none.

- p1 PASS — PNG `e9a19d4ba94ea99ce539112af3998f2dcebd4a9453e73f6982e61026e5fe8df9` — Title, 1863-08-10, Latin match; issuer '| PIUS PAPA IX.' with stray OCR bar matches metadata (non-blocking). Address, garbled OCR line 'bd had 3L', body. Right column: historical note '1 8. Leo Epist 15...' set as its own block at the source page break inside 'patran-/tur' (non-blocking); later a separate note block '...(MS. Leo Serm. 82...' and a stray OCR line '"quo'. Raw OCR noise ('Mi (EC uy de p . BOX PO') from the source's note-separator line runs on after 'religionis,' at the end of a body line; checked against container OCR line 23365: separate noise line in source, no note wording or furniture numeral fused. Literal OCR corruption, not a blocking defect. No folio or running head.
- p2 PASS — PNG `c3986718c348ed7c34c1c2c0da57a332be6fa4274e4541f7c5761ba29bde1c67` — Body continues in clean two columns. Historical notes set as separate blocks at source page breaks (left column: '(1) Alocst. 90...' block after 'fuimu (1)'; '(1) Concil. Oecum...' at foot; right column: '(1) Luc...'-'(6)' block). Raw OCR noise from the note-separator line ("'::! p ebd io gp d T RU n ; i duc", container OCR lines 23406-23407) runs on at the end of the body line 'fuimu (1).'; it is noise with no note wording, folio or running head, so it counts as literal OCR corruption. A stray 'o 0 i' line also stands on its own.
- p3 PASS — PNG `46942909a1819b130427f40d4a748831c05bf85a1a970067e98dda73337d9e3c` — Body continues; separate note blocks '(1) Matth...' and '(1) S. Gregor...' at source page breaks; no furniture, clipping or overlap.
- p4 PASS — PNG `8721d34f6c96f8561633be6385351ce8a1c8a9bc7e3064676d103d4d7462de79` — Body to close; note block '(1) S. Leo Epist. 107...' set separately at source page break; dating clause (die 10 Augusti 1863, anno decimoctavo) runs into right column, followed by Source/rights apparatus.

Recorded findings and qualifications:
- p1: Non-blocking qualification: issuer line '| PIUS PAPA IX.' with stray OCR bar, matching metadata.
- p1: Non-blocking: historical note blocks set separately at source page breaks (p1 right column after 'patran-' and after 'religionis,').
- p1: Limitation: raw OCR noise strings at note boundaries ('bd had 3L', 'Mi (EC uy de p . BOX PO', '"quo') retained literally.
- p2: Non-blocking: historical note blocks set separately at source page breaks.
- p2: Limitation: raw OCR noise at note boundaries retained literally (p2 left column after 'fuimu (1).'; 'o 0 i').

### `pius-ix-acta.volume-03.line-00021313.part-08` — PASS

*Incredibili — ad episcopos Neogranatenses*; issuer `PIUS PAPA IX.`; 1863-09-17; encyclical; language `la`. Prior finding: none.

- p1 PASS — PNG `7125401ae7ee7bc7604fa287ad9242b9d92eaf5f05a3dcc32a0a5339e8e16e7d` — Title, issuer PIUS PAPA IX., 1863-09-17, Latin match; address, protocol and body in clean two columns; no furniture.
- p2 PASS — PNG `5025dc03dafc9bb4ecd22843bb4dc64a9128d5defbde6e1bcf8e3817ac3a41b1` — Body continues. Notes '(1) Isaias c. 58 v. I.' and '(1) Sap. 8.' set as separate blocks at source page breaks (non-blocking). Dating clause (die 17 Septembris anno 4863 [literal OCR], anno decimo octavo), then Source/rights apparatus.

Recorded findings and qualifications:
- p2: Non-blocking: historical note blocks '(1) Isaias...' and '(1) Sap. 8.' set separately at source page breaks (left column).

### `pius-ix-acta.volume-03.line-00021313.part-09` — PASS

*Quod iampridem — de Immaculata Conceptione (breve)*; issuer `PIUS PAPA IX. -`; 1863-09-25; apostolic-letter; language `la`. Prior finding: none.

- p1 PASS — PNG `4517b9931abfc12fac400112e8ef460f9daca99592fc6b60c910095c7680f6f9` — Single page: title, 1863-09-25, Latin match; issuer 'PIUS PAPA IX. -' with stray OCR dash matches metadata (non-blocking). Body, dating clause sub Anulo Piscatoris (die XXV Septembris MDCCCLXIII, anno XVIII), subscription N. CARD. PARACCIANI CLARELLI, then Source/rights apparatus.

Recorded findings and qualifications:
- p1: Non-blocking qualification: issuer line 'PIUS PAPA IX. -' with stray OCR dash, matching metadata.

### `pius-ix-acta.volume-03.line-00021313.part-10` — PASS

*Etsi maximo — ad episcopum Popayanensem*; issuer `PIUS PP. IX.`; 1863-11-30; letter; language `la`. Prior finding: none.

- p1 PASS — PNG `452876f06e11462b34b35b8039f6ce34ddc8779e3dd1254d2fb2a8ac2404f3e1` — Title, issuer PIUS PP. IX., 1863-11-30, Latin match; protocol and body in two columns; right column ends about a quarter short of the foot before the closing moves to page 2 (unbalanced break, reading order intact, non-blocking). No furniture.
- p2 PASS — PNG `7b7aa6b8a9f95d01de7cbb26afd26936bd9e574f263a1175b70bbe189d187d78` — Final page: end of body, dating clause (die 30 Novembris 1863, anno XVIII) as genuine source closing, then Source/rights apparatus.

Recorded findings and qualifications:
- p1: Non-blocking layout note: right column of page 1 ends early (after 'Apostolicam Benedictionem'), continuation on page 2; reading order intact.

### `pius-ix-acta.volume-03.line-00021313.part-11` — PASS

*Tuas libenter — ad archiepiscopum Monacensem*; issuer `PIUS PAPA IX.`; 1863-12-21; letter; language `la`. Prior finding: none.

- p1 PASS — PNG `de8e00085de42f1952d9518c7e1b4f12a1b8aa4248feded1b128065c2c0495af` — Title, issuer PIUS PAPA IX., 1863-12-21, Latin match; address, protocol and body in clean two columns; no furniture.
- p2 PASS — PNG `5a0428621fa638d226c9bdc4205168561af12dd02e78361601c0cb3951ff2a86` — Body continues in clean two columns; no furniture, clipping or overlap.
- p3 PASS — PNG `06226814d50b1dbfedea5eff8cb6ec410eb70863884de01c2414d9c5fb930dd6` — Body to close, dating clause (die 21 Decembris 1863, anno XVIII; literal OCR 'Z Pontiieatus'), then Source/rights apparatus.

### `pius-ix-acta.volume-03.line-00021313.part-12` — PASS

*Non mediocri — ad cardinalem de Bonald de liturgia Lugdunensi*; issuer `PIUS PP. IX.`; 1864-03-17; letter; language `la`. Prior finding: none.

- p1 PASS — PNG `c2e1056009249c9ccb71a03a1191915b69a7f17a361ebb69ac2fe66539cb0e4e` — Title, issuer PIUS PP. IX., 1864-03-17, Latin match; address (OCR-damaged), protocol and body in clean two columns; no furniture.
- p2 PASS — PNG `9ea339302607c2701f3a48b0b6a7f75febb15b0ac24d68c559007d0ffcf39954` — Final page: end of body, dating clause (die 17 Martii 1864, anno XVIII) as genuine source closing, then Source/rights apparatus.

### `pius-ix-acta.volume-03.line-00021313.part-13` — PASS

*Quum non sine maxima — ad archiepiscopum Friburgensem*; issuer `PIVS PP. IX.`; 1864-07-14; letter; language `la`. Prior finding: none.

- p1 PASS — PNG `326e7b5f1fced9641ab13c8e86f82fbce14ed4841a60663fe828805734182c32` — Title, issuer PIVS PP. IX., 1864-07-14, Latin match; address, protocol with stray OCR initial lines 'I' and 'P' (literal drop-cap remnants), body in clean two columns; no furniture.
- p2 PASS — PNG `3051bb88af5c99a6d79c3b723fd654897f1175b8fe282ab585e0d3737dfdb6a8` — Body to close, dating clause (die 14 Iulii 1864, anno XIX), then Source/rights apparatus in right column; clean flow.

### `pius-ix-acta.volume-03.line-00021313.part-14` — PASS

*Ubi Urbaniano — ad episcopos Poloniae et Russiae*; issuer `PIVS PP. IX.`; 1864-07-30; encyclical; language `la`. Prior finding: none.

- p1 PASS — PNG `41e371f584e9d6c61bb53c3b4cfd4fbd2711b17f96ccdd24fdec28c17cd20ad5` — Title, issuer PIVS PP. IX., 1864-07-30, Latin match; address, protocol and body in clean two columns; no furniture.
- p2 PASS — PNG `f4efe36267b690817bc7beae8edda1ce0633b01635361f40e17023398caa2571` — Body continues; notes '(* Sap. c. 6...' and '(*) Rom. c. 8. v. 18.' set as separate blocks at source page breaks (non-blocking); no furniture.
- p3 PASS — PNG `41a1f8258bb6cec85bfbdb315394bc08082a3de70eedb7ea6c6dc1a910b67180` — Final page: end of body, dating clause (ex Arce Gandulphi die 30 Iulii 1864, anno XIX) as genuine source closing, then Source/rights apparatus.

Recorded findings and qualifications:
- p2: Non-blocking: historical note blocks '(* Sap. c. 6...' and '(*) Rom. c. 8. v. 18.' set separately at source page breaks (right column).

### `pius-ix-acta.volume-03.line-00021313.part-15` — PASS

*Qui contra Ecclesiam — beatificatio Petri Canisii*; issuer `PIUS PP. IX.`; 1864-08-02; apostolic-letter; language `la`. Prior finding: none.

- p1 PASS — PNG `21c105eff42aff2a1f7aa0dee0af41ed58e6f82f109774bc4fcc3ae4f771ab1f` — Title, issuer PIUS PP. IX., 1864-08-02, Latin match; protocol and body in clean two columns; no furniture.
- p2 PASS — PNG `86d980c8590f9b6033abb2711724c7e34af1c78b2e82439c12fd377b7f7adae7` — Body continues; source page-break paragraph restarts only (one short restart line 'Sanctis Carolo Borromeo...'); no folio, running head or fused note.
- p3 PASS — PNG `aa91cc521f18b4eeca1fd40c9ffcd7878d440c7f4187365a5ac73d411f0f10b0` — Final page: end of body, dating clause sub Anulo Piscatoris (die II Augusti MDCCCLXIV, anno XIX) and subscription N. CARD. PARAGCIANI CLARELLI (genuine source closing), then Source/rights apparatus.

### `pius-ix-acta.volume-03.line-00021313.part-16` — PASS

*Maximae quidem — ad episcopos Bavariae*; issuer `PIVS PAPA IX.`; 1864-08-18; letter; language `la`. Prior finding: none.

- p1 PASS — PNG `048540e87d0b09d5940c533667877304e92844283fd9072b5dee7d723f732766` — Title, issuer PIVS PAPA IX., 1864-08-18, Latin match; address, protocol and body in clean two columns; no furniture.
- p2 PASS — PNG `8991cf7f9f6b5e49d5a8991682632b5b14d05f915e95cfe5c03655ebb89aad2f` — Body to close, dating clause (ex Arce Gandulphi die 18 augusti 1864, anno XIX), then Source/rights apparatus in right column; clean flow.

### `pius-ix-acta.volume-03.line-00021313.part-17` — PASS

*Auctor nostrae fidei — beatificatio Margaritae Mariae Alacoque*; issuer `PIVS PP. IX.`; 1864-08-19; apostolic-letter; language `la`. Prior finding: none.

- p1 PASS — PNG `13104242a7bef8c9d9f5076078235c90cae7d1854c4907eaaf51a994372e91a4` — Title, issuer PIVS PP. IX., 1864-08-19, Latin match; protocol and body in clean two columns; no furniture.
- p2 PASS — PNG `eef50b2d25036072d5e48019f86b7c26be499d8936761e5a2a6d41b6915bb520` — Body to close, dating clause sub Anulo Piscatoris (die XIX Augusti MDCCCLXIV, anno XIX), subscription N. CARD. PARACCIANI CLARELLI, then Source/rights apparatus in right column.

### `pius-ix-acta.volume-03.line-00021313.part-18` — PASS

*Quanta cura — de praecipuis erroribus aetatis*; issuer `PIUS PP. IX.`; 1864-12-08; encyclical; language `la`. Prior finding: none.

- p1 PASS — PNG `3c156f1166871e60aa3293f65da2397e8ab4f678d2181516c6b6bd04f44069bb` — Title, issuer PIUS PP. IX., 1864-12-08, Latin match; address, protocol and body in clean two columns; source page-break paragraph restarts only; no furniture.
- p2 PASS — PNG `84789f6d09f21c0cb9f5f1cdbafcab4596a72bf4b95f064e6c182c787ff932af` — Body continues; historical note blocks ('(1) Gregor. XVI...(2) Eadem', '(1)S. Aug....(2) S. Leo', '(1) Epist. ad Card. De la Rochefeucault') set separately at source page breaks (non-blocking); no folio or running head.
- p3 PASS — PNG `21fd9d568f3ffc858cd6246aebd5dcd3dc16bbfe3ad4d690fbd5a2d352408644` — Body continues; note blocks set separately at source page breaks (left: '(1) Clement. XII...« Quo' with its OCR tail '- graviora a. c' as its own line, container OCR 26321-26325, folio 693 correctly omitted; right: '(1) S. Ignatius...(2) Psal. 143.' and '(1) S. Caelest...(2) S. Innocent...'). No folio or running head; no note text fused into body lines.
- p4 PASS — PNG `44976a39659da3c5146ad8f5b69f3cf02f42015ae6dc1087447a8e62ef921d7e` — Note continuation block ('Carthag.', 'spud Coust. pag. 891.', '(3) S. Leo...(&) Pius VII...') at page head as its own block, then body to close; note '(1) S. Cyprian.' separate; dating clause (die VIII Decembris 1864, anno XIX) and final note '(1) S. Bernard...' (genuine source closing), then Source/rights apparatus.

Recorded findings and qualifications:
- p2: Non-blocking: historical note blocks set separately at source page breaks (left column twice, right column once).
- p3: Non-blocking: historical note blocks set separately at source page breaks, including the separate note-tail line '- graviora a. c' (p3 left column).
- p4: Non-blocking: historical note blocks set separately (p4 left column head; right column twice).

## Qualifications (non-blocking)

- Issuer from the volume title: 21313.part-01 displays `PII IX. — PONTIFICIS MAXIMI ACTA`, which matches the frozen metadata. Under the standing ruling this is a recorded attribution-context qualification. It does not block, although that document is blocked for the separate furniture defect.
- Stray OCR marks in issuer lines that match the metadata: `| PIVS PAPA IX.` (21313.part-05), `| PIUS PAPA IX.` (21313.part-07), `PIUS PAPA IX. -` (21313.part-09). OCR-damaged protocol spellings such as `BERVUS` (17185.part-04), `SERVVS SERVORYM` (17185.part-06) and `SERYUS` (17185.part-08) likewise match the metadata.
- Historical notes are set as their own blocks at source page breaks, including mid-sentence or mid-word breaks: in the 1862-12-11 letter to the Archbishop of Munich (17185.part-09), *Quanto conficiamur*, *Incredibili*, *Ubi Urbaniano* and *Quanta cura*. No note text is fused into a body line.
- Two pages have short columns before a page break (21313.part-05 p1 right column; 21313.part-10 p1 right column). Reading order is intact and no text is lost.

## Limitations

- This is literal, uncorrected, uncollated historical OCR. OCR corruption, odd spellings and literal year errors (for example "4863" in *Incredibili*) are retained and not judged. No date was inferred or repaired.
- This is a layout review only. It makes no word-level collation, historical-authentication, publication, installation or deployment claim. The source admission and render receipts are upstream evidence, not findings of this lane.
- The raw OCR noise at note boundaries in *Quanto conficiamur* was compared against the container OCR and judged to be noise rather than fused note wording or furniture. A character-geometry pass could refine that judgment.
