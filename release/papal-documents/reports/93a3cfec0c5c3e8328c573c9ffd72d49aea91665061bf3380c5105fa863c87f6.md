# Pius IX Acta visual review 07 — pius-0001 lane 07

Result: 17 PASS, 2 CHANGES_REQUIRED of 19 assigned Latin readers from *Pii IX Pontificis Maximi Acta*, pars prima, volume III; 64 pages, every page individually opened full size with the Read tool. Zero pages reused. No document carried a `prior_finding`.

## Scope and method

Each assigned page PNG produced by the repository's `pdf-review` raster run was opened one image per page; no contact sheet, thumbnail or new rasterization was used. The displayed title, responsible issuer, act date and language were compared with the frozen metadata. Headings, two-column flow, gutters, margins and glyphs were inspected, as were the natural source closing (dating clause, subscriptions, historical notes) and the terminal source/rights colophon. No clipping, overlap, missing or tofu glyphs, collapsed tables, modern digitizer signatures, running heads, raw `None` placeholders or fused marginal summaries were found.

Two visual suspicions (isolated short lines interrupting a sentence) were checked against the frozen manifest's `physical_line_ranges` and the canonical OCR artifact named by the manifest. A mechanical scan of every line of eight characters or fewer inside the selected bounds of all nineteen documents was then run. It found no further furniture candidates beyond the two findings below. Lane helper scripts are in this lane directory.

## Standing-ruling qualifications (non-blocking)

- Six allocutions and one homily display the issuer `PII IX. — PONTIFICIS MAXIMI ACTA`, taken from the volume title as a recorded attribution context, matching frozen metadata: `line-00015219.part-01`, `line-00016060.part-01`, `line-00016705`, `line-00016779`, `line-00016877.part-01`, `line-00016966`, `line-00017185.part-01`.
- OCR-damaged issuer spellings that match metadata and still identify the pope (`SERYORUM`, `SERVORYM`, `SENVONVM`) are qualifications.
- Historical footnotes set as their own blocks at source page breaks (including mid-word, e.g. `come- / derit`, `ie- / gitimae`) in `line-00016060.part-01`, `line-00016060.part-02`, `line-00016966`, `line-00017185.part-01`, `line-00017185.part-03` are non-blocking.
- `line-00011044.part-05` and `line-00011044.part-07` print the edition's own abridgement `Non obstantibus etc. sequuntur clausulae, prout in praecedenti`; this is source wording.
- `line-00017185.part-03` page 2: the right column ends about 45% down the page at `officii ve-`, continuing at page 3 top. Reading order is intact; recorded as a cosmetic layout qualification.
- Sparse final pages in this lane all carry genuine source closing (dating clause, subscription or the speech's own close) before the colophon.

## Blocking findings

- `pius-ix-acta.volume-03.line-00015219.part-02` page 1, right column: page-foot furniture fragment 'uma -.' (OCR LF15455, inside selected bound [15420,15457], immediately before excluded folio line LF15458 '408') is set as its own body paragraph in the right column, splitting the word 'inci- / pientibus « Inscrutabili »' (after '... die 23 Maii anno 1622 datis et inci'). Page-foot signature/furniture left inside the body is blocking in the boundary-reviewed Pius IX series.
- `pius-ix-acta.volume-03.line-00017185.part-01` page 1, right column: page-foot furniture fragment 'qs' (OCR LF17259, inside selected bound [17225,17261], immediately before excluded folio line LF17262 '438') is set as its own body paragraph in the right column, interrupting the sentence '... potestatem ct ius divinae originis / qs / audacissime denegare non metuant.' Page-foot signature/furniture left inside the body is blocking in the boundary-reviewed Pius IX series.

Both fragments lie inside the recorded selection bounds as the last OCR line before an excluded folio number. They are page-foot furniture (signature residue) that the source selections otherwise omit, as with `P`, `27` and `X` elsewhere in this volume. Under the standing ruling for the boundary-reviewed Pius IX series, they block those readers. Remedy belongs upstream: trim the bound or record the line as omitted furniture, then rerender and re-review.

## Evidence verification

All assigned PDFs, the receipt, the frozen manifest, the raster-run record and all 64 page PNGs (86 files) were hashed before and after inspection; every digest matched its assignment pin both times (`verification-before.json`, `verification-after.json`, identical).

| Evidence | Path | SHA-256 | Verification |
| --- | --- | --- | --- |
| Render receipt | `.scratch/typeset_pipeline/claude/pius-0001/receipt.json` | `720d0acae7c1f32315fd11d968d13eaa0510b72ea25906a6916054bd2ada2d73` | Before and after |
| Frozen manifest | `.scratch/typeset_pipeline/claude/pius-0001/frozen-manifest.json` | `583691e3d8941ca1c9a3a3f27f4cc57747afcfb3b3817776aad37a103df9d736` | Before and after |
| Raster run | `.scratch/claude-review/rasters-pius-0001/review-run.json` | `5718cc943c5d94fdf4a333529ce03aa4e55089d3d90a4801f03abb5e9597e7c6` | Before and after |
| Lane assignment | `.scratch/claude-review/pius-0001/lane-07/assignment.json` | `a2dded57e206573eadd12ed3dea7218e877f14bacf62d040e0efbaab6e5e129b` | Scope binding |
| Observation ledger | `.scratch/claude-review/pius-0001/lane-07/observations.jsonl` | `008dd2e00dd2fae4459a3fd99de4c5f9f4bd51833cabef7aed94a4ca13a227a6` | 64 unique page records |
| Before verification | `.scratch/claude-review/pius-0001/lane-07/verification-before.json` | `76210e3b98823dd2c9021d5c1b983da23f00be24cb478c1fbeab3f0ba8e2136d` | All match |
| After verification | `.scratch/claude-review/pius-0001/lane-07/verification-after.json` | `76210e3b98823dd2c9021d5c1b983da23f00be24cb478c1fbeab3f0ba8e2136d` | All match; identical |

## PDF outcomes

| Source ID | Date | Lang | Pages | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- |
| `pius-ix-acta.volume-03.line-00008746.part-05` | 1861-07-09 | `la` | 3 | `dbad35b65d5957cdd5741c223e1eaaa935afa35a39a344300a32e756ecb4520a` | PASS |
| `pius-ix-acta.volume-03.line-00008746.part-06` | 1861-09-26 | `la` | 6 | `e70af6747c1c21fd951ff0db6bbf4a277c6dba29148f533676a6561814ffac5e` | PASS |
| `pius-ix-acta.volume-03.line-00011044.part-02` | 1861-10-03 | `la` | 6 | `e196ab64044f3a3a172b9097779a9d4923e7bcd7b6d6d5553e5f904fccf7e04e` | PASS |
| `pius-ix-acta.volume-03.line-00011044.part-03` | 1861-10-03 | `la` | 6 | `7bba326adda65793d0a2bc7a60e0cd4fba596279d915ca58c5b140a7d438475c` | PASS |
| `pius-ix-acta.volume-03.line-00011044.part-04` | 1861-10-03 | `la` | 6 | `34f852f941b5effa9a6316513c39c19c83dd74e020f34d962964cbdafeb04925` | PASS |
| `pius-ix-acta.volume-03.line-00011044.part-05` | 1861-10-03 | `la` | 5 | `c44999c12b62ee4e80c3593aeb4a8e3ec1951352058773314d0a26854d645776` | PASS |
| `pius-ix-acta.volume-03.line-00011044.part-07` | 1861-10-07 | `la` | 5 | `e6b743ce688a953a4bdbbc9b64ebe8531f2a8c6fed629fca6e60651d01de447c` | PASS |
| `pius-ix-acta.volume-03.line-00015219.part-01` | 1861-12-23 | `la` | 2 | `05cc838a74108124ea8b4eef0e51c878a3f97165f59ffba72eac5da407d648a8` | PASS |
| `pius-ix-acta.volume-03.line-00015219.part-02` | 1862-01-06 | `la` | 5 | `ace2c727a4f366443887d933b4aaae416311d2ab55c154b608175a775fb5b6f0` | CHANGES_REQUIRED |
| `pius-ix-acta.volume-03.line-00015219.part-03` | 1862-02-07 | `la` | 2 | `738175b3566b58b53de1ccfe467d87f1422695b755ea653d5c6d33841c04f8fa` | PASS |
| `pius-ix-acta.volume-03.line-00016060.part-01` | 1862-04-07 | `la` | 1 | `677bf610a227958b955ae375fe012fc5c7c923a02077f0198f3d7d986abc68da` | PASS |
| `pius-ix-acta.volume-03.line-00016060.part-02` | 1862-04-08 | `la` | 4 | `9875e02692ce9a64a064c4d565b6228e9931e7a440deda95f696d6b8aa4630da` | PASS |
| `pius-ix-acta.volume-03.line-00016705` | 1862-05-22 | `la` | 1 | `296c25b232a0c7554555d4a642bc04310ddff7481ea104878792288c3a8b9b80` | PASS |
| `pius-ix-acta.volume-03.line-00016779` | 1862-05-24 | `la` | 1 | `97c9053adbf70442ed67bada6db4d6173e3817581076f43b212039d00aedd920` | PASS |
| `pius-ix-acta.volume-03.line-00016877.part-01` | 1862-06-06 | `la` | 1 | `e2cdfc9e1cf0792ca9ce67b6aba467ebd3cc0a137761889e24573fd9e7f83e0d` | PASS |
| `pius-ix-acta.volume-03.line-00016966` | 1862-06-08 | `la` | 2 | `75877127a66ed301018d9c174e6f0f421450c705ae97fc94c1c688d12f5fe7b9` | PASS |
| `pius-ix-acta.volume-03.line-00017185.part-01` | 1862-06-09 | `la` | 4 | `b89f5260263b288c856cd49f48e9374a4c2218385f20305b46bb5c1d5b354e62` | CHANGES_REQUIRED |
| `pius-ix-acta.volume-03.line-00017185.part-02` | 1862-06-10 | `la` | 1 | `d3e05e17f7f1a5a70546c64e5957ddec9498790699c7f3968b4a92a624c03e52` | PASS |
| `pius-ix-acta.volume-03.line-00017185.part-03` | 1862-07-03 | `la` | 3 | `67f28860be3771f2fa6492b879492ab164dcbb52481b3df447192d1bf35d7319` | PASS |

## Per-document page record

### `pius-ix-acta.volume-03.line-00008746.part-05` — PASS

De tuendo colendoque agro — beatificatio Ioannis Leonardi · PIVS PP. IX. · 1861-07-09 · apostolic-letter. PDF `.scratch/typeset_pipeline/claude/pius-0001/1861-07-09-pius-ix-acta-volume-03-line-00008746-part-05-fb0d89eb-la/1861-07-09-pius-ix-acta-volume-03-line-00008746-part-05-fb0d89eb-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `40e3e40fba50a89fcc44b7b59ac01824af49f7f4da610e47de34d4030f3ad7c1` | PASS | Title, issuer PIVS PP. IX., 1861-07-09, Latin match metadata; protocol PIVS PP. IX. / AD PERPETUAM REI MEMORIAL; clean two-column body, no furniture or digitizer marks. |
| 2 | `668624f654664f37e080882040b51fc049a8bc36d9daaad830a715b82fee9d05` | PASS | Two-column body continues cleanly; dating clause Datum Romae ... die IX Iulii MDCCCLXI Pontificatus Nostri anno XVI closes right column. |
| 3 | `d64604a35b8b595baa63a09adcc4cb647333c45dcfba45c570e167ea8c088af9` | PASS | Final page carries the historical subscription (Pro Domino Card. ... / Io: B. Brancaleoni Castellani Substitutus, OCR-damaged) before source and rights colophon; genuine source closing. |

### `pius-ix-acta.volume-03.line-00008746.part-06` — PASS

In celsissima — erectio episcopatus Victoriensis · PIUS EPISCOPUS SERVUS SERYORUM DEI · 1861-09-26 · bull. PDF `.scratch/typeset_pipeline/claude/pius-0001/1861-09-26-pius-ix-acta-volume-03-line-00008746-part-06-441e96ed-la/1861-09-26-pius-ix-acta-volume-03-line-00008746-part-06-441e96ed-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `b0acb3bd4d54505031decb52a27b133449796027947d9cbe4cd3abc01fb5ae01` | PASS | Title, issuer PIUS EPISCOPUS SERVUS SERYORUM DEI (OCR-damaged, matches metadata), 1861-09-26, Latin match; protocol lines then two-column body; no furniture. |
| 2 | `b25bc894cd8a8e9a6c5f41a6f47c9543d214028a178115d60f91aa9bc46990b4` | PASS | Two-column body continuous; stray literal OCR '\|' after evehimus is OCR noise, not furniture; no clipping. |
| 3 | `d63811434834a1c5f1c79dc06cce5b6df2e3f893922c2cf5555ff48c88c4d9df` | PASS | Two-column body continuous; clean gutters and margins. |
| 4 | `dd7d0c661b3c30585c19b9295e914a38b64a9c54f09b776fa2de4564950a612f` | PASS | Two-column body continuous; no running heads or folio numbers in body. |
| 5 | `b47956004270c34a66f5dc44a24a91d90e20031a555bd3cd95603626da232faa` | PASS | Two-column body with derogation clauses; clean layout. |
| 6 | `674f86b4b4c55fbf9c4d4be039ca955fd970e23d05904efd56b7665e59aa428d` | PASS | Sanctio (Nulli ergo ...) and dating clause Datum Romae ... sexto Kalendas octobris ... anno sexto decimo, then source and rights colophon; genuine source closing. |

### `pius-ix-acta.volume-03.line-00011044.part-02` — PASS

Vix a primis — erectio sedis Capitis Haitani · PIVS EPISCOPVS SERVVS SERVORVM DEI · 1861-10-03 · bull. PDF `.scratch/typeset_pipeline/claude/pius-0001/1861-10-03-pius-ix-acta-volume-03-line-00011044-part-02-c38ad627-la/1861-10-03-pius-ix-acta-volume-03-line-00011044-part-02-c38ad627-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `508d02f1bd6b2eb29d7be36c3ff9690b32213d7e877e122f85a2b9d9e69af33d` | PASS | Title, issuer PIVS EPISCOPVS SERVVS SERVORVM DEI, 1861-10-03, Latin match; protocol lines and two-column body; source-page-break paragraph splits (plentes / Litterae favent) are non-blocking; no furniture. |
| 2 | `8351bcabfc8ea0cf58ea230d759d12666833e010ce0685b8e52cba7a87846514` | PASS | Two-column body continuous; clean gutter and margins. |
| 3 | `0c995bed181cfe84a77daaa8d933a3ca92880a2b01885b1dff3628df34730b4e` | PASS | Two-column body continuous; literal OCR marks only. |
| 4 | `afb58a8a2eebfe3c78407c88e6d681b867facf6d19a3ae274516646d731bea0a` | PASS | Two-column body continuous; no running heads or folios. |
| 5 | `43c8eba9747291815ab7e87e985260fcc98b123009f03e7cb36ae7d9459c18e4` | PASS | Derogation clauses, executor mandate, sanctio begin; mid-sentence block split before Cardinalium at a source page break, non-blocking. |
| 6 | `5c2cec4001ee183f5d393fdf3580946b13b8a89852e4177a41b95a9e775087af` | PASS | Sanctio end and dating clause Datum Romae ... quinto nonas octobris ... anno sexto decimo, then source/rights colophon; genuine closing. |

### `pius-ix-acta.volume-03.line-00011044.part-03` — PASS

Christianae religionis — erectio episcopatus Cayesensis · PIVS EPISCOPVS SERVUS SERVORYM DEI · 1861-10-03 · bull. PDF `.scratch/typeset_pipeline/claude/pius-0001/1861-10-03-pius-ix-acta-volume-03-line-00011044-part-03-40f3ebea-la/1861-10-03-pius-ix-acta-volume-03-line-00011044-part-03-40f3ebea-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `8ee7a094b1bf67616fed4bee7ef0b2b4644ddbddf5ee697e80bd6d06ff8423fd` | PASS | Title, issuer PIVS EPISCOPVS SERVUS SERVORYM DEI (OCR-damaged, matches metadata), 1861-10-03, Latin match; protocol and two-column body; OCR has many truncated line-initial/final letters from the scan (literal OCR limitation, not layout). |
| 2 | `c3854e473269db36fe7bc44ebc3a874b4559c3131f0d070d692f4b36f4de7870` | PASS | Two-column body continuous; OCR letter loss at line edges is literal OCR; no furniture. |
| 3 | `00878d56008464a1628f29c5c901eaae6711652d01362d290b0acb7dc7e93b80` | PASS | Two-column body continuous; stray OCR '\|' and digit noise only; no folios or running heads. |
| 4 | `262a342a22c3dd3e73ab7f1ef02951766d184844c5b219efbe90f0c41b25c615` | PASS | Two-column body continuous; clean gutter and margins. |
| 5 | `caa944509fec940c3fb7455b34e86c756e9e2d5284fe3002bb575f82bef3f14d` | PASS | Derogations, executor mandate, Volumus clauses, sanctio begins; clean layout. |
| 6 | `d4ccb2d6b8ed6ab8c8a56a8734c40c6683f53844127bbba040dd9103e345abc5` | PASS | Sanctio end and dating clause Datum Romae ... quinto nonas octobris ... sextodecimo, then source/rights colophon; genuine closing. |

### `pius-ix-acta.volume-03.line-00011044.part-04` — PASS

Catholicae Romanae Ecclesiae — erectio sedis Portus Principis · PIUS EPISCOPUS SERVUS SERVORUM DEI · 1861-10-03 · bull. PDF `.scratch/typeset_pipeline/claude/pius-0001/1861-10-03-pius-ix-acta-volume-03-line-00011044-part-04-73afa13b-la/1861-10-03-pius-ix-acta-volume-03-line-00011044-part-04-73afa13b-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `a586920e7044c18024cb1debfdf6bd892459d9fa4071750a95eb43781356de3f` | PASS | Title, issuer PIUS EPISCOPUS SERVUS SERVORUM DEI, 1861-10-03, Latin match; protocol and two-column body; parish list set inline as source; no furniture. |
| 2 | `e45247444d3d7b63517c3288cbd39fb90b926da91a170ae54b666b90d6abc484` | PASS | Two-column body continuous; literal OCR noise only (stray '\|', digit). |
| 3 | `ebc52d07a35fd52fbc7bd9e5c87b4f5f6c7ed0496ed94a5f6714bd0b2d75d3e8` | PASS | Two-column body continuous; no folios or running heads. |
| 4 | `270c9f8cffecb02047e77a5a5de54de3e38547d2c2f63d277b91c93629cde0d7` | PASS | Two-column body continuous; clean gutter and margins. |
| 5 | `f8b785ec2be64a0f729d052b1caf18d7b49b374b79740f172fc183dadef5aeb5` | PASS | Dotation, taxa, derogations and executor mandate; clean layout. |
| 6 | `f295a8323eb4bd9fca9c853225a2e811d379621bc0548a8325257df3ccc1ca6d` | PASS | Non obstantibus, Volumus clauses, sanctio, dating clause Datum Romae ... quinto nonas octobris ... sexto decimo in right column, then source/rights colophon; genuine closing. |

### `pius-ix-acta.volume-03.line-00011044.part-05` — PASS

Proprium fuit semper — erectio sedis Portus Pacis · PIUS EPISCOPUS. SERVUS SERVORUM DEI · 1861-10-03 · bull. PDF `.scratch/typeset_pipeline/claude/pius-0001/1861-10-03-pius-ix-acta-volume-03-line-00011044-part-05-a2e9cb38-la/1861-10-03-pius-ix-acta-volume-03-line-00011044-part-05-a2e9cb38-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `bd18098410c0e68edc6906fa693eab27194e754c3667fdd0b1a424bd9208e56b` | PASS | Title, issuer PIUS EPISCOPUS. SERVUS SERVORUM DEI, 1861-10-03, Latin match; protocol and two-column body; no furniture. |
| 2 | `031a83dae68fd39df8e1fc74e772ec57d38ea86bac3042f5a284b14844d3b620` | PASS | Two-column body continuous; clean gutter and margins. |
| 3 | `9528cb24106bf680244aadad5a76abfa5ee1411b70eef9b06899360b7a06c58e` | PASS | Two-column body continuous; no folios or running heads. |
| 4 | `2d068336f86eaf41605cc5f6e870f54394a8ac048d7024f95da0ce25e0b194da` | PASS | Two-column body continuous; short block splits in right column at source page/line breaks (dioecesanum ... / etiam noviter ...) are non-blocking. |
| 5 | `0c67bcc99ecea201893dae64a1eeca6fa03667dfdb3d38d827ff6a575225fbed` | PASS | Derogations, executor mandate, the edition's own abridgement 'Non obstantibus etc. sequuntur clausulae, prout in praecedenti' (source wording, qualification), dating clause Datum Romae ... quinto nonas octobris ... sexto decimo, then source/rights colophon; genuine closing. |

### `pius-ix-acta.volume-03.line-00011044.part-07` — PASS

In procuranda — erectio sedis Puniensis · PIVS EPISCOPVS SERVUS SENVONVM DEI · 1861-10-07 · bull. PDF `.scratch/typeset_pipeline/claude/pius-0001/1861-10-07-pius-ix-acta-volume-03-line-00011044-part-07-8226bf9d-la/1861-10-07-pius-ix-acta-volume-03-line-00011044-part-07-8226bf9d-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `2afb1abb4edaf38fce6df45350bf74e3de15016ef9146b9a13e98f9fc6aefe9d` | PASS | Title, issuer PIVS EPISCOPVS SERVUS SENVONVM DEI (OCR-damaged, matches metadata), 1861-10-07, Latin match; protocol and two-column body; no furniture. |
| 2 | `891042a3c431021f99decc8d1dddc06670fde4169cbe97c8b14aa58b2ba07847` | PASS | Two-column body continuous; stray OCR '\|' and '$' only; clean gutter. |
| 3 | `27bbc5b8250ecd2bce2ff87e0f2ab21798bd026516209f66070bf6ca2192fbe7` | PASS | Two-column body continuous; no folios or running heads. |
| 4 | `a396779a4b6b969c8d7df319d1d25f59919373773806cfafecb11658963e51d0` | PASS | Two-column body continuous; literal OCR '©' glyph in right column renders (OCR noise); no clipping. |
| 5 | `395d5922c9ec831a4f15cb91da8297132207acdf2152d299136b2e252678d14a` | PASS | Executor clause, edition abridgement 'Non obstantibus etc. sequuntur clausulae, prout in praecedenti' (source wording), dating clause Datum Romae ... nonis octobris ... anno sexto decimo, then source/rights colophon on same page; genuine closing. |

### `pius-ix-acta.volume-03.line-00015219.part-01` — PASS

Inter plurima — allocutio in consistorio secreto 23 decembris 1861 · PII IX. — PONTIFICIS MAXIMI ACTA · 1861-12-23 · consistorial-allocution. PDF `.scratch/typeset_pipeline/claude/pius-0001/1861-12-23-pius-ix-acta-volume-03-line-00015219-part-01-a61652d4-la/1861-12-23-pius-ix-acta-volume-03-line-00015219-part-01-a61652d4-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `52cb2545b1b7e0f28f6e8b3ff84352b27da7fd10d184c5eb7200a5dc30539f24` | PASS | Title (wraps to two lines), volume-title issuer, 1861-12-23, Latin match; dated caption HABITA IN CONSISTORIO SECRETO ... retained as source dating; address, allocution and set-apart narrative rubrics (Hic Cardinalis Patrizi ...) flow in two columns; no furniture. Findings: Issuer line 'PII IX. — PONTIFICIS MAXIMI ACTA' is the volume-title attribution context matching frozen metadata (non-blocking qualification). |
| 2 | `91cd5b7e2faf295caf43d1c0a8ebdf3d177ab54dae7420917a1db11a7f5005c6` | PASS | Final rubric and closing speech, then subscription PIUS PP. IX. (printed before folio 402 in the source OCR, within selected bounds) and source/rights colophon; genuine source closing. |

### `pius-ix-acta.volume-03.line-00015219.part-02` — CHANGES_REQUIRED

Romani Pontifices — congregatio de Propaganda Fide pro negotiis ritus orientalis · PIVS PP. IX. · 1862-01-06 · apostolic-letter. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-01-06-pius-ix-acta-volume-03-line-00015219-part-02-f06285a3-la/1862-01-06-pius-ix-acta-volume-03-line-00015219-part-02-f06285a3-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `1041fcb801484c5de80c398411d04d844a291f75f6a8c5df4f7f3da0649cf828` | CHANGES_REQUIRED | Title (two lines), issuer PIVS PP. IX., 1862-01-06, Latin match; protocol and two-column body otherwise clean; stray page-foot furniture line 'uma -.' interrupts a body word in right column lower third. Findings: BLOCKING: page-foot furniture fragment 'uma -.' (OCR LF15455, inside selected bound [15420,15457], immediately before excluded folio line LF15458 '408') is set as its own body paragraph in the right column, splitting the word 'inci- / pientibus « Inscrutabili »' (after '... die 23 Maii anno 1622 datis et inci'). Page-foot signature/furniture left inside the body is blocking in the boundary-reviewed Pius IX series. |
| 2 | `bc08d409a8526476af87ea677636d86fac0d3977b06c18204609cca99b880ba1` | PASS | Two-column body continuous; no folios, running heads or signatures visible. |
| 3 | `c3575c21658fd41c3295d26cd1771155934b3e07ad5c3d1a6fae5df975428d00` | PASS | Two-column body continuous; clean gutter and margins. |
| 4 | `e9173e4b5ef1aac2a633da96b9b3a0fc4841c46581ce809efbb85292a406a827` | PASS | Two-column body with consultor list, decree and non obstantibus; stray OCR '\|' only. |
| 5 | `6255d846129a591c28f1801de215954d1e8e121533bf747376e9bec6d8e2275e` | PASS | Derogation close, dating clause Datum Romae ... sub Annulo Piscatoris die sexta mensis Ianuarii ... (OCR-damaged), Pontificatus anno decimosexto, subscription G. B. Canp. Praxerti (OCR-damaged), then source/rights colophon; genuine closing. |

### `pius-ix-acta.volume-03.line-00015219.part-03` — PASS

Ad universalis Ecclesiae — de votis simplicibus ante sollemnia · PIUS PAPA IX. · 1862-02-07 · apostolic-letter. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-02-07-pius-ix-acta-volume-03-line-00015219-part-03-215b4e53-la/1862-02-07-pius-ix-acta-volume-03-line-00015219-part-03-215b4e53-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `2419925e17700c5a797724e4c60c942e86258963311c07ded49e5d0dbfd43992` | PASS | Title, issuer PIUS PAPA IX., 1862-02-07, Latin match; protocol and two-column body including quoted decree; source-page-break block splits non-blocking; no furniture. |
| 2 | `226eaf234a978fe2e0349973426af95dfa60591f35b012eaaef3735f1c1f6e71` | PASS | Close, dating clause Datum Romae ... sub annulo Piscatoris die VII Februarii MDCCCLXII ... anno decimo sexto, subscription B. CARD. BARBERINUS., then source/rights colophon; genuine closing. |

### `pius-ix-acta.volume-03.line-00016060.part-01` — PASS

Si semper — allocutio in consistorio secreto 7 aprilis 1862 · PII IX. — PONTIFICIS MAXIMI ACTA · 1862-04-07 · consistorial-allocution. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-04-07-pius-ix-acta-volume-03-line-00016060-part-01-13a853e1-la/1862-04-07-pius-ix-acta-volume-03-line-00016060-part-01-13a853e1-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `7a52dc6c573e8547649659898e66d28f38cf35f8fcc8f51d505d657e67a8158b` | PASS | Single page: title, volume-title issuer, 1862-04-07, Latin match; dated caption (OCR-damaged BABITA ... SECETO) and address, allocution with rubrics, closing speech ending 'cu- rabimus. ;' (source has no subscription; next OCR line is folio and next act), then source/rights colophon in right column; genuine closing. Findings: Issuer line 'PII IX. — PONTIFICIS MAXIMI ACTA' is the volume-title attribution context matching frozen metadata (non-blocking qualification). Historical footnote '(1) S. Leo serm. in fest. S. Laurentii' set as its own separate block at the source page break between 'prodigia accurato' and 'examine perpensa' (non-blocking under standing ruling). |

### `pius-ix-acta.volume-03.line-00016060.part-02` — PASS

Amantissimus humani generis — ad episcopos ritus orientalis · PIVS PAPA IX. · 1862-04-08 · encyclical. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-04-08-pius-ix-acta-volume-03-line-00016060-part-02-b254be95-la/1862-04-08-pius-ix-acta-volume-03-line-00016060-part-02-b254be95-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `ab3133015858c52335ad33f0399686b4758ed7f5536ab0bb429e1f36d12ef5d5` | PASS | Title, issuer PIVS PAPA IX., 1862-04-08, Latin match; protocol lines and two-column body with literal line-initial guillemets of source quotations; no running heads, folios or digitizer marks. Findings: Historical footnote blocks (1)-(5) left column and (1)-(13) right column are set as separate blocks at source page breaks (the right-column block splits 'come- / derit' mid-word); non-blocking under standing ruling; OCR-damaged note numbers (&), 19), a, are literal. |
| 2 | `75cfc7c78e896aa64b680ee73faaad1e391e17c3e31593c7b30a0315d45d582b` | PASS | Two-column body continuous; stray OCR 'PRA' inside a sentence is OCR noise, not identifiable furniture. Findings: Footnote blocks (1)-(b) left column and (1) right column set as separate blocks at source page breaks; non-blocking. |
| 3 | `589724b0ff62aa7dd7cc0872d44edd55ab4a82fc5c0187276519933eac331336` | PASS | Two-column body continuous; stray OCR marks (È, \, ') only; clean gutter and margins. |
| 4 | `3d4f52b37c764f874b6305c9d8f0b3aace7c81fb798c835cd8ad539555c27271` | PASS | Close with apostolic blessing, dating clause Datum Romae apud S. Petrum die 8 Aprilis anno 1862 / Pontificatus Nostri Anno decimosexto, then source/rights colophon; genuine closing. |

### `pius-ix-acta.volume-03.line-00016705` — PASS

Quanto studio — allocutio in consistorio semipublico 22 maii 1862 · PII IX. — PONTIFICIS MAXIMI ACTA · 1862-05-22 · consistorial-allocution. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-05-22-pius-ix-acta-volume-03-line-00016705-34e170af-la/1862-05-22-pius-ix-acta-volume-03-line-00016705-34e170af-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `5c3ced24739db545f93bcc1ef950c34b3f690e852ab38911496ff72da21e9ec3` | PASS | Single page: title (two lines), volume-title issuer, 1862-05-22, Latin match; dated caption (OCR-damaged SHMIPUBLICO ... MAIL / MDCCCLAII) and address, allocution, rubric and closing speech ending 'beneplacitum.', then source/rights colophon in right column; no furniture. Findings: Issuer line 'PII IX. — PONTIFICIS MAXIMI ACTA' is the volume-title attribution context matching frozen metadata (non-blocking qualification). |

### `pius-ix-acta.volume-03.line-00016779` — PASS

Cum eximias — allocutio in consistorio semipublico 24 maii 1862 · PII IX. — PONTIFICIS MAXIMI ACTA · 1862-05-24 · consistorial-allocution. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-05-24-pius-ix-acta-volume-03-line-00016779-1fd0a10d-la/1862-05-24-pius-ix-acta-volume-03-line-00016779-1fd0a10d-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `251aa16991cb3f6e8995a9e5789caf95bbdffd4c034c0b98a3e28768906804d0` | PASS | Single page: title, volume-title issuer, 1862-05-24, Latin match; dated caption and address (stray OCR backslash and drop-cap debris), allocution, rubric and closing speech ending 'utilitatem,' as the source OCR ends before the next act's folio; source/rights colophon in right column; no furniture. Findings: Issuer line 'PII IX. — PONTIFICIS MAXIMI ACTA' is the volume-title attribution context matching frozen metadata (non-blocking qualification). |

### `pius-ix-acta.volume-03.line-00016877.part-01` — PASS

Mirabile quoddam — allocutio in sacello Xystino 6 iunii 1862 · PII IX. — PONTIFICIS MAXIMI ACTA · 1862-06-06 · allocution. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-06-06-pius-ix-acta-volume-03-line-00016877-part-01-53253977-la/1862-06-06-pius-ix-acta-volume-03-line-00016877-part-01-53253977-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `a5d89c87f0989cac016fc470c0cd32599c1222e520ed922b3e8b1473838c3499` | PASS | Single page: title, volume-title issuer, 1862-06-06, Latin match; dated caption HABITA IN XYSTINO SACELLO DIE 6 1unn 1862 (OCR-damaged), address DILECTI FILII, allocution ending 'preces effuderint.', then source/rights colophon in right column; no furniture. Findings: Issuer line 'PII IX. — PONTIFICIS MAXIMI ACTA' is the volume-title attribution context matching frozen metadata (non-blocking qualification). |

### `pius-ix-acta.volume-03.line-00016966` — PASS

Exultat cor Nostrum — homilia in canonizatione martyrum Iaponensium · PII IX. — PONTIFICIS MAXIMI ACTA · 1862-06-08 · homily. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-06-08-pius-ix-acta-volume-03-line-00016966-5896e9d8-la/1862-06-08-pius-ix-acta-volume-03-line-00016966-5896e9d8-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `4e3109596f548e4604e1f8cc0749e9d0b99c4848c602463ddfce465a60023bf7` | PASS | Title (two lines), volume-title issuer, 1862-06-08, Latin match; dated caption HABITA IN SOLEMNI CANONIZATIONE ... MDCCCLXII retained; two-column homily body; no running heads or folios. Findings: Issuer line 'PII IX. — PONTIFICIS MAXIMI ACTA' is the volume-title attribution context matching frozen metadata (non-blocking qualification). Historical footnote blocks ((1) left; (1)(2), (1)-(3) right) set as separate blocks at source page breaks; non-blocking. |
| 2 | `2ee00a382a90640f397bb61277789133c6d0f9735afef6d6a5cd928d1f48596b` | PASS | Homily continues to the closing prayer ending 'honor et gloria.', then source/rights colophon in right column; genuine closing. Findings: Footnote blocks (1)(2) and (1) set as separate blocks at source page breaks; non-blocking. |

### `pius-ix-acta.volume-03.line-00017185.part-01` — CHANGES_REQUIRED

Maxima quidem laetitia — allocutio in consistorio 9 iunii 1862 · PII IX. — PONTIFICIS MAXIMI ACTA · 1862-06-09 · consistorial-allocution. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-06-09-pius-ix-acta-volume-03-line-00017185-part-01-0615c83e-la/1862-06-09-pius-ix-acta-volume-03-line-00017185-part-01-0615c83e-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `5d80647cc0d67b3274d5fc20f37eaa30d8d641b643e5fafa1a68d021d9c2be2d` | CHANGES_REQUIRED | Title, volume-title issuer, 1862-06-09, Latin match; dated caption (OCR-damaged IVNLE MDCCCLIII) and address; two-column body otherwise clean; stray 'qs' block mid-sentence in right column upper third. Findings: Issuer line 'PII IX. — PONTIFICIS MAXIMI ACTA' is the volume-title attribution context matching frozen metadata (non-blocking qualification). BLOCKING: page-foot furniture fragment 'qs' (OCR LF17259, inside selected bound [17225,17261], immediately before excluded folio line LF17262 '438') is set as its own body paragraph in the right column, interrupting the sentence '... potestatem ct ius divinae originis / qs / audacissime denegare non metuant.' Page-foot signature/furniture left inside the body is blocking in the boundary-reviewed Pius IX series. |
| 2 | `d575b4d8ef3851c5bb0d00ea8b8be29c80ef1c2af0bdb76ecd3276a9ab1813ec` | PASS | Two-column body continuous; no folios or running heads. Findings: Historical footnote '(1) Ad Rom. c: 8. v. 13.' set as its own block at the source page break inside 'ie- / gitimae'; non-blocking under standing ruling. |
| 3 | `d82866a49608172c27105cf8453c70198cfd18c9f554f640210dbe77dce7e87b` | PASS | Two-column body continuous; literal guillemet quotation markers; clean layout. Findings: Historical footnote '(1) Epist. VII ad Episc. per Ital. ...' set as its own block at the source page break between 'sal' and 'terrae'; non-blocking. |
| 4 | `2578d85efc2198017bf20b1cc34066b6b570f68f4d432924e461dff55ec93b59` | PASS | Allocution closes with apostolic blessing '... vehementer laetamur.' (no printed subscription), then source/rights colophon; genuine source closing. |

### `pius-ix-acta.volume-03.line-00017185.part-02` — PASS

Pontificiae Nostrae largitatis — facultas benedicendi episcopis canonizationi adstantibus · PIUS PAPA IX. · 1862-06-10 · apostolic-letter. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-06-10-pius-ix-acta-volume-03-line-00017185-part-02-58d04e9e-la/1862-06-10-pius-ix-acta-volume-03-line-00017185-part-02-58d04e9e-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `1a0b149c1bf9fe2ec8f975e69295417026b2cdf27527268baa6cd48f2e9ba51f` | PASS | Single page: title (two lines), issuer PIUS PAPA IX., 1862-06-10, Latin match; protocol PIUS PAPA IX., brief body, dating clause Datum Romae ... die X Junii MDCCCLXII ... anno XVI, subscription B. Carp. BarseRINUS. (OCR-damaged), then source/rights colophon with its retained-apparatus wording; genuine closing; single-column final layout normal. |

### `pius-ix-acta.volume-03.line-00017185.part-03` — PASS

Quo graviora — ad episcopos Lusitaniae · PIVS PAPA IX. · 1862-07-03 · letter. PDF `.scratch/typeset_pipeline/claude/pius-0001/1862-07-03-pius-ix-acta-volume-03-line-00017185-part-03-82cc4f8f-la/1862-07-03-pius-ix-acta-volume-03-line-00017185-part-03-82cc4f8f-la.pdf`. No prior finding.

| Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- |
| 1 | `5ff6045796dbb0b98ce5d52790b435753b66bdc115462eecda2e36c8cfaa2c87` | PASS | Title, issuer PIVS PAPA IX., 1862-07-03, Latin match; address block (OCR-damaged) and protocol PIVS PAPA IX., two-column body; no running heads, folios or digitizer marks. |
| 2 | `cbe47c4eed2357b4fab0412911681cc8eed8ed42cebca0b25ea2712f91d747cd` | PASS | Two-column body continuous with literal guillemet quotation markers. Findings: Non-blocking layout qualification: right column stops about 45% down the page at 'officii ve-' and the text continues at the top of page 3 left column ('sti munera'); reading order is intact and nothing is clipped or overlapped. Footnotes '(1) Jerem. Thr. IV v. &' and '(1) Ezech. c. XXXIV v. 4.' set as separate blocks at source page breaks; non-blocking. |
| 3 | `a803cef998add6069fd26328002b06dd58fbed6b648bffb5de9f61b7d8be593b` | PASS | Body ends with apostolic blessing, dating clause Datum Romae apud $. Petrum die 3 Iulii anno 1862 \| Pontificatus Nostri anno decimoseptimo (literal OCR), then source/rights colophon; genuine closing. |

## Limitations

- Uncorrected, uncollated historical OCR; literal OCR corruption, odd spellings and damaged issuer/protocol spellings are limitations, not defects.
- Layout review only of the hash-pinned page rasters; no word-level collation, image collation, historical authentication, date reconstruction, publication, installation or deployment claim.
- Canonical source admission, rights clearance and source-fidelity rendering are upstream evidence, not findings of this lane. This report does not authorize installation.
