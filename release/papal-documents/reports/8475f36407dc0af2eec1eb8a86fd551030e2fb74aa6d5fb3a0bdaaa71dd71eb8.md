# Continuatio provider-mark corrections visual review 02 — Pius VIII lane (re-issue)

**Re-issued result.** 3 of 31 assigned PDFs are CHANGES_REQUIRED and 28 PASS. All 54 pages were individually opened at full size in the original pass (51 page-level PASS, 3 page-level CHANGES_REQUIRED after re-issue). No page was reused. Lane 2 of batch `continuatio-marks-0001`: provider-mark-omitted v2 corrections of previously rejected Bullarii Romani continuatio tome XVIII readers.

## What changed in this re-issue and why

The first issue of this report (sha256 `5e12a0340fb316d26f24c625f67a1082b9e118b23708fb14b58013fc2b484082`) returned 29 CHANGES_REQUIRED / 2 PASS documents (41 / 13 pages), because it treated historical running heads and printer signatures interrupting a body sentence as blocking. On the coordinator's ruling, this lane is re-issued under the established standard for the continuation series, under which the 397 installed continuation readers were reviewed (`src/sources/papal-documents/historical-series-visual-16.md`: the retained uncorrected, uncollated OCR qualification "covers historical spellings, abbreviations, running-head and rule fragments; it does not cover modern digitizer marks retained in the body").

- Now non-blocking qualifications: historical running heads and folios (`Pius PP. Octavus` + folio, `Bullarium Romanum` + folio), printer/volume signatures (`Bull. Rom. Tom. XVIII.`), including those set mid-sentence or inside a hyphen split, and the extra paragraph break left at a removal seam.
- Still blocking: any remaining modern provider mark, marginal-summary labels or dates fused into body sentences, and displaced notes set mid-sentence.
- No page was re-opened. The original full-size observations are the evidence, and every original locus is kept below and labelled `QUALIFICATION`. `observations.jsonl` keeps its 54 original lines and adds 54 `reissue` lines, without deleting anything. No recognizable marginal-summary label or date fused into a body sentence, and no displaced note set mid-sentence, was recorded on any page. The garbled marginal lines on `line-00017980` page 1 (`Pmea^aa / «b*di«n4* / mira.`) are set as separate lines inside the running-head block, not fused into the sentence, and are treated like the series' other literal marginal-summary OCR fragments. Inline OCR noise is a literal-OCR limitation.

## Prior-finding disposition

Every document's `prior_finding` named a modern Google digitizer footer. The classified locus is no longer visible in any of the 31 readers, and the text around each removal seam keeps its words in natural order. In three readers, however, a second damaged provider signature remains, so the prior defect is not fully absent there. These are the only blocking findings:

- `bullarium-continuatio.volume-18.line-00018126.provider-marks-omitted-v2` p1: BLOCKING: Residual damaged modern provider mark: page 1, column 1, bottom, standalone line '■zed by Gooalc' (truncated 'Digitized by Google') between 'ox quo profer' and the running head. Prior provider-mark defect ('Digitizad by Googie') is NOT fully absent: the classified locus may be gone but a second damaged signature remains.
- `bullarium-continuatio.volume-18.line-00019150.provider-marks-omitted-v2` p4: BLOCKING: Residual damaged modern provider mark: page 4, column 2, middle, standalone line '■ " ii:i<:cd by Cooglf' (damaged 'Digitized by Google'). Prior provider-mark defect ('Digitizcc' by Coogie') is NOT fully absent: a second damaged signature remains.
- `bullarium-continuatio.volume-18.line-00022349.provider-marks-omitted-v2` p2: BLOCKING: Residual damaged modern provider mark: page 2, column 1, middle, standalone line 'by Cixylc' (damaged tail of 'Digitized by Google') immediately after the dating clause. Prior provider-mark defect ('Diqitized by Gooqle') is NOT fully absent: a damaged signature fragment remains.

As a cross-check, the extracted text of every PDF was searched for `Digit`, `Goog`, `Coog`, `ogle` and stray `by` fragments. It found exactly these three, plus only the project source note and Italian `coogregazione` OCR words.

## Scope and method

Each PNG in `page_rasters` was opened as its own full-size image with the Read tool (1700x2200 originals). No contact sheet, re-rasterization, source acquisition, text correction, word-level collation or date reconstruction was performed. Title line, literal issuer, language label and date treatment were compared with the frozen metadata. Every act date is unresolved in the metadata and is correctly omitted from the title line; the literal dating clauses remain in the body. No clipping, overlap, missing glyph, collapsed table, raw `None` placeholder or apparatus-only final page was found. Every final page carries a genuine source dating clause, plus subscriptions or appended decree notes where printed, before the project source/rights apparatus.

## Evidence verification

All 88 digests (31 PDFs, 54 PNGs, receipt, manifest, raster run) matched their assignment pins before and after inspection, and the before/after records are identical. The re-issue changed classification only, not inputs.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| receipt `.scratch/typeset_pipeline/claude/continuatio-marks-0001/receipt.json` | `baa1f5617d5758fca7659cac83c33b17e1ca7c6d59997befb4a24d3dc200916a` | Before and after |
| manifest `.scratch/typeset_pipeline/claude/continuatio-marks-0001/frozen-manifest.json` | `fe821f047335393afda93cb86c97d10d51cf41d2730b3670e520a20d94457f3f` | Before and after |
| raster_run `.scratch/claude-review/rasters-continuatio-marks-0001/review-run.json` | `664e1f7bef4a6a5d605e2b681e37b72281a51f3dde85e7330a90ea166d6e63e6` | Before and after |
| Lane assignment | `8076bad55291cf7ceb7ff53bdddd1a753a87d173aa2b37dc98787b173c587733` | Scope binding |
| Before verification record | `99afa878a06278994b721ccfba64f96a87c9abb93caa4693d1659725d8c5f962` | PASS (88/88) |
| After verification record | `99afa878a06278994b721ccfba64f96a87c9abb93caa4693d1659725d8c5f962` | PASS (88/88), identical |
| Inspection ledger with re-issue lines | `1406b959f1e1cf05c5a93c2071bb58a335bcdcca0164dd4bb5334ec4f04548c5` | 54 original + 54 reissue lines |

## PDF outcomes (re-issued)

| Source ID | Language | Pages | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- |
| `bullarium-continuatio.volume-18.line-00015238.part-01.provider-marks-omitted-v2` | `la` | 1 | `aaaa4b2b5fbaaa2eb223f9737483b99c4f3d9713c277c46fa20d19f7cd0ed970` | PASS |
| `bullarium-continuatio.volume-18.line-00015238.part-02.provider-marks-omitted-v2` | `la` | 1 | `3488944add4b0048077175e3915dadd4c95edb93f8518b343ae4b760e595b9fb` | PASS |
| `bullarium-continuatio.volume-18.line-00015470.provider-marks-omitted-v2` | `la` | 2 | `0d075f8eee1a29c48bf456a913f42a26e8aee59df921eb8a94b5326c91639266` | PASS |
| `bullarium-continuatio.volume-18.line-00015849.provider-marks-omitted-v2` | `la` | 2 | `abd461d72e5d989a73cc087c3edf7b2e682ca158faba3d615e22569448e90950` | PASS |
| `bullarium-continuatio.volume-18.line-00016096.part-01.provider-marks-omitted-v2` | `la` | 1 | `60564ae20beabff8acc61653cdffd01e82b0b2ff7058e5b4f55cf46236ce3c6a` | PASS |
| `bullarium-continuatio.volume-18.line-00016498.provider-marks-omitted-v2` | `la` | 2 | `5d796a43afefdf8d9861351d917e98a8ec00bddcfb74664eee329d3d44be0011` | PASS |
| `bullarium-continuatio.volume-18.line-00016916.part-01.provider-marks-omitted-v2` | `la` | 2 | `b8cb76ff398ceb8ffa7d072a55734326ddf1c501960205957a11ce7116e8b7b1` | PASS |
| `bullarium-continuatio.volume-18.line-00017193.provider-marks-omitted-v2` | `la` | 2 | `1733bb3e80e5ca96e4826412f87c05eee9a5b7a4a4998c83e1f834892901cb95` | PASS |
| `bullarium-continuatio.volume-18.line-00017494.part-02.provider-marks-omitted-v2` | `la` | 1 | `022f733e157df01a76d7094c4ae727cfb9d12df8903c2b11fbff469ec4ed014b` | PASS |
| `bullarium-continuatio.volume-18.line-00017701.provider-marks-omitted-v2` | `la` | 1 | `b025252ccc7b08991ef204252ff5bc4d07ce72adfa072006baa282d2e3613a53` | PASS |
| `bullarium-continuatio.volume-18.line-00017862.provider-marks-omitted-v2` | `la` | 1 | `615bfc1bee9a5a85859e7a9bfe81b3274b0da63e19bd8185e0e4ace7750489cb` | PASS |
| `bullarium-continuatio.volume-18.line-00017980.provider-marks-omitted-v2` | `la` | 2 | `25fedde943b323b74adf387a2e5437c445884a00f2ec44e3e53cdcc72201cdc3` | PASS |
| `bullarium-continuatio.volume-18.line-00018126.provider-marks-omitted-v2` | `la` | 2 | `5f789f6ec5b331195cb3eaf0adebf0fde7446ba25e046e27603ac32c4d5b8c42` | CHANGES_REQUIRED (residual provider mark) |
| `bullarium-continuatio.volume-18.line-00018492.provider-marks-omitted-v2` | `la` | 1 | `62525252d41203ac2420c31be3a3690c07cabf5987826c6499a50f28f9d155df` | PASS |
| `bullarium-continuatio.volume-18.line-00018761.provider-marks-omitted-v2` | `la` | 2 | `739f25f48f5a9a1f3af3816f721fb07d5506a8d98c7bb5b74a5bec701b41f493` | PASS |
| `bullarium-continuatio.volume-18.line-00019150.provider-marks-omitted-v2` | `it` | 5 | `92115eb3fc09900df02591d835896398191b0dd1a74deb2864e28f6d601de62b` | CHANGES_REQUIRED (residual provider mark) |
| `bullarium-continuatio.volume-18.line-00019727.discovery-01.provider-marks-omitted-v2` | `la` | 2 | `537da121cc86c4d08f15563af61d3503d78105fe684d0700e72afd0ccb4bf030` | PASS |
| `bullarium-continuatio.volume-18.line-00020089.discovery-01.provider-marks-omitted-v2` | `la` | 1 | `0b15d122872ff6a86d5a8c52a5104c155a49e310e1d5a5f8aabe6368d41b5e6c` | PASS |
| `bullarium-continuatio.volume-18.line-00020473.provider-marks-omitted-v2` | `la` | 1 | `0d22f1eb6aea6e2ff43e6bce4615df288e564b0080d62e5d6480cfba6392ba84` | PASS |
| `bullarium-continuatio.volume-18.line-00020888.provider-marks-omitted-v2` | `mul` | 5 | `8f148bae66fb6a046dee0405a3ec03e2a4a2417fa4859077f82e7ff2556b8a7e` | PASS |
| `bullarium-continuatio.volume-18.line-00021533.discovery-01.provider-marks-omitted-v2` | `la` | 2 | `272a7af958cfe514e3ab66feefa3e3d57a04ac2325681530d2bf7e3f0938f277` | PASS |
| `bullarium-continuatio.volume-18.line-00021533.discovery-03.provider-marks-omitted-v2` | `la` | 1 | `26248287e9ad6d1d348d4310fc113abe6557096e9dd7648f8753f619bac18005` | PASS |
| `bullarium-continuatio.volume-18.line-00021533.discovery-04.provider-marks-omitted-v2` | `la` | 2 | `c1703ff61ec7a2f3729f108dcb74ee1231bec81514fe7d38c12b22b99cc595c2` | PASS |
| `bullarium-continuatio.volume-18.line-00022349.provider-marks-omitted-v2` | `la` | 2 | `e36d418e52d102a9e397298de5f1ea9a0c899f160758be17bbf3b6d828492993` | CHANGES_REQUIRED (residual provider mark) |
| `bullarium-continuatio.volume-18.line-00022620.provider-marks-omitted-v2` | `la` | 1 | `976dd195f0edfb6eac956a7b8faeeb67c3b396d8d47d95391c34ec1e3c935fd0` | PASS |
| `bullarium-continuatio.volume-18.line-00022878.part-01.provider-marks-omitted-v2` | `la` | 2 | `8a6ef021b68f84800689badd84348baf727932a2b6f3d873bb46ee5eb3076667` | PASS |
| `bullarium-continuatio.volume-18.line-00023244.provider-marks-omitted-v2` | `la` | 1 | `16efb7ce9f6963e55eaa4d4643ad4db42889d6fdee89f9694e66a489d98c8f32` | PASS |
| `bullarium-continuatio.volume-18.line-00023326.provider-marks-omitted-v2` | `la` | 2 | `6b70cd14c67671c4ef2902655ff8880282d45879a534a6e7bfc62178e9025c41` | PASS |
| `bullarium-continuatio.volume-18.line-00023558.part-01.provider-marks-omitted-v2` | `la` | 1 | `e56c018b56e606e1525a661e83db65c510547cad26e6490ec2c28847565d211a` | PASS |
| `bullarium-continuatio.volume-18.line-00024403.part-01.provider-marks-omitted-v2` | `la` | 1 | `24bac09af083cbb973abde20cc42183bf7663c9608bd43726ba6a240444842c4` | PASS |
| `bullarium-continuatio.volume-18.line-00024403.part-02.provider-marks-omitted-v2` | `la` | 2 | `624308d059d7a72a4002354ebed25acd654f49c58d75576a251e11b55fbb03ee` | PASS |

## Per-document findings and qualifications (all original loci retained)

### `bullarium-continuatio.volume-18.line-00015238.part-01.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googie') is absent: no provider mark on page 1; text around the removed locus reads in order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pius PP. OotavUsJ' with folio '89' at page 1, column 1, lower third, interrupts the body sentence 'de venerabilium fratrum Nostrorum S. Romanae Ecclesiae | eardiDtUuai' (cardinalium) in section 2.

### `bullarium-continuatio.volume-18.line-00015238.part-02.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Coogle') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running-head furniture '23 / l / 90 / Bullarium Romanum' at page 1, column 2, top, interrupts the body sentence 'apostolica auctoritate tenore prae- | wDtiuiD misencordiler' (praesentium misericorditer) in section 2.

### `bullarium-continuatio.volume-18.line-00015470.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googie') is absent: no provider mark on page 1.
- p2: Prior provider-mark defect is absent on page 2.

### `bullarium-continuatio.volume-18.line-00015849.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('DIgitized by Googie') is absent: no provider mark on page 1; column 2 paragraph break inside 'per- | functus' (likely the omitted-mark seam) keeps natural word order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pius PP. OctaTus' with folio '93' at page 1, column 1, middle, interrupts the body sentence 'Is nobilissimo | genere ortus'.
- p2: Prior provider-mark defect is absent on page 2.

### `bullarium-continuatio.volume-18.line-00016096.part-01.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Dlgitizcd by Googli') is absent: no provider mark on page 1; column 1 paragraph break after 'seu «b& ^ | priorissa' keeps natural order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pius PP. Octavus' with folio '95' at page 1, column 1, bottom, interrupts the body word 'ope- | ribu3' (operibus) in section 2.

### `bullarium-continuatio.volume-18.line-00016498.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googie') is absent: no provider mark on page 1; column 1 paragraph break inside 'qua- | tuor' keeps natural order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume signature furniture 'BuU. Rom. Tom. XVIU.' at page 1, column 1, bottom, interrupts the body sentence 'Supjdieiter ergo a Nobis | ... ipsi sodalitatis moderatores petiere' in section 2.
- p2: Prior provider-mark defect is absent on page 2; column 1 paragraph break inside 'appro- | bationem' keeps natural order.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Volume running head '25 / i / 9H / Bullariiim Konianum' at page 2, column 1, top, interrupts the body sentence 'ut quolibet aooo per mensem ab ecclesia | possint abesse'.

### `bullarium-continuatio.volume-18.line-00016916.part-01.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googie') is absent: no provider mark on page 1; column 1 paragraph break inside 'prae- | terea' keeps natural order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pins PP Octavus' with folio '101' at page 1, column 2, lower middle, interrupts the body word 'apo- | rtolioi aiiiUtores' (apostolici auditores) in section 3.
- p2: Prior provider-mark defect is absent on page 2.

### `bullarium-continuatio.volume-18.line-00017193.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('DIgitized by Googie') is absent: no provider mark on page 1.
- p2: Prior provider-mark defect is absent on page 2.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pilis PP. OcUirus' with folio '105' and 'I' at page 2, column 1, top, interrupts the body word 'assi- | •Uat' (assistat) in section 3.

### `bullarium-continuatio.volume-18.line-00017494.part-02.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googli') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pios PP, OcUtO»' with folio fragment 'm' at page 1, column 1, middle, interrupts the body sentence 'benedictam, tenore | pnieMabttffl' (tenore praesentium) in section 2.

### `bullarium-continuatio.volume-18.line-00017701.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitiz<^ ts^Googlc') is absent: no provider mark on page 1; column 2 paragraph break inside 'qua- | vis' keeps natural order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head '2T / 106 / Bullarium Romanum' at page 1, column 1, lower third, interrupts the body sentence 'laneam byemej | vero oostftte' (hyeme ... aestate vero) in section 3.

### `bullarium-continuatio.volume-18.line-00017862.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googie') is absent: no provider mark on page 1; column 1 paragraph break after 'poeniteotiarum | relaxationes' keeps natural order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pins PP. Octavus' with folio '107' at page 1, column 2, lower middle, interrupts the dating clause 'Datum Rmnae apu(l sanctam Mariam | Majorem aub aonulo ...'.

### `bullarium-continuatio.volume-18.line-00017980.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Go;,gIe') is absent: no provider mark on page 1; column 1 paragraph break inside 'absolven- | tes' keeps natural order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Marginal/running-head furniture 'Pmea^aa / «b*di«n4* / mira. / 108 / BuUarium Romanum' at page 1, column 2, bottom, interrupts the body word 'ef- | focti}' (effectui) in section 3.
- p2: Prior provider-mark defect is absent on page 2.

### `bullarium-continuatio.volume-18.line-00018126.provider-marks-omitted-v2` — CHANGES_REQUIRED

Prior defect: NOT fully absent: a residual damaged signature remains.

- p1: BLOCKING: Residual damaged modern provider mark: page 1, column 1, bottom, standalone line '■zed by Gooalc' (truncated 'Digitized by Google') between 'ox quo profer' and the running head. Prior provider-mark defect ('Digitizad by Googie') is NOT fully absent: the classified locus may be gone but a second damaged signature remains.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head "I' Pim SP. Octavus" with folio '109' at page 1, column 1, bottom, interrupts the body word 'profer | cto' (profecto) in section 2.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Column 2 paragraph break inside 'tum io | temporalibiis' keeps natural order (nonblocking).
- p2: No provider mark on page 2.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Volume signature furniture 'BttU. Rom Tom. XVIIJ.' at page 2, column 1, top, interrupts the body word 'il- | i lis' (illis) carried from page 1 column 2 in section 3.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Volume running head '28 / 110 / BuHarium Aomanum' at page 2, column 1, bottom, interrupts the body word 'fu- | turum' in section 4.

### `bullarium-continuatio.volume-18.line-00018492.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('DIgitized by Googie') is absent: no provider mark on page 1.

### `bullarium-continuatio.volume-18.line-00018761.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googie') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume signature furniture 'Bull. Ilom.Tom, XV W.' at page 1, column 1, middle, interrupts the body word 'ex- | terior' in section 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head '29 / 114 / Bullarium Romanum' at page 1, column 2, middle, interrupts the body word 'ba- | beant' (habeant) in section 1.
- p2: Prior provider-mark defect is absent on page 2.

### `bullarium-continuatio.volume-18.line-00019150.provider-marks-omitted-v2` — CHANGES_REQUIRED

Prior defect: NOT fully absent: a residual damaged signature remains.

- p1: Prior provider-mark defect ('Digitizcc' by Coogie') is absent from page 1 (see page 4 for a remaining damaged signature).
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Ci / 116 / BuUarium Romanum' at page 1, column 1, middle, interrupts the body word 'pro- | cedenti' (procedenti) in section 1.
- p2: No provider mark on page 2.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pius PPi Octavas / «17' at page 2, column 1, middle, interrupts the body word 'camcrlen- | e ooi|i' (camerlengo) in section 1.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Volume signature furniture 'BuU. Htm. Tom. XVW.' at page 2, column 2, upper third, interrupts the body sentence '... Nostro predecessore I^oone XII. | per organo dul reverendissimo ...' in section 2.
- p3: No provider mark on page 3.
- p3: QUALIFICATION (non-blocking under continuation-series standard): Volume running head '118 / Bullarium Romanum' at page 3, column 1, top, interrupts the body word 'regol&i | menti' (regolamenti) in section 4.
- p3: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'I Pius PP. Ocuvus / f/lty' at page 3, column 2, lower third, interrupts the body sentence 'Ciascuno dei sc^getU, ^ebe so- | m> eet ...' in section 8.
- p4: BLOCKING: Residual damaged modern provider mark: page 4, column 2, middle, standalone line '■ " ii:i<:cd by Cooglf' (damaged 'Digitized by Google'). Prior provider-mark defect ('Digitizcc' by Coogie') is NOT fully absent: a second damaged signature remains.
- p4: QUALIFICATION (non-blocking under continuation-series standard): Volume running head '"»20 / fiuikrium Romanum' immediately after that mark, page 4, column 2, middle, interrupts the body sentence 'fuHa quale | perallro in ordiao ...' in section 11.
- p5: No provider mark on page 5.

### `bullarium-continuatio.volume-18.line-00019727.discovery-01.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googie') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pilis PP. Oclaviis' with folio '121' at page 1, column 1, upper third, interrupts the body sentence 'postulatioaibui oADueodo» | iui iiieiropoliliinnrut» ...' in section 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume signature furniture 'BuU. Rom Tom. XV///.' at page 1, column 2, middle, interrupts the body word 'm igislra- | tuum' (magistratuum) in section 5.
- p2: No provider mark on page 2.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Volume running head '31 / l / 122 BulJarium nomaiium' at page 2, column 1, middle, interrupts the body sentence 'eligimus, ac deputamus vc-pl"«ri^" ** | ncnihilcm fratrem' (venerabilem fratrem) in section 8.

### `bullarium-continuatio.volume-18.line-00020089.discovery-01.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googie') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'i / Pius PP. Oclavus . ^25' at page 1, column 1, middle, interrupts the body word 'procuran- | dam' in section 1.

### `bullarium-continuatio.volume-18.line-00020473.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digilizectby Googicj') is absent: no provider mark on page 1; column 1 paragraph break inside 'fralrix | bus' (title synopsis) keeps natural order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head "Pius PP. Octavus ' / .125" at page 1, column 1, lower third, interrupts the body word 'ciargi- | mur' (elargimur) in section 2.

### `bullarium-continuatio.volume-18.line-00020888.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digilized by Cooglc') is absent: no provider mark on page 1 (the 'coogregazione' strings are literal OCR of Italian 'congregazione', not provider marks).
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head '128 / Ballarium Romanum' at page 1, column 2, middle, interrupts the Italian body sentence 'e tra queili. «kvnanon | etier presenli duo guardiani' in section 5.
- p2: No provider mark on page 2.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pius PP. Oclavus / 129' at page 2, column 2, upper third, interrupts the Italian body word 'sopra.ros- | «ervanza' (osservanza) in section 12.
- p3: No provider mark on page 3.
- p3: QUALIFICATION (non-blocking under continuation-series standard): Volume signature furniture 'BuU. Rom.Tom. XV IU.' at page 3, column 1, upper third, interrupts the Italian body sentence 'osservisi oeU' | avvenire nel modo' in section 16.
- p4: No provider mark on page 4.
- p5: No provider mark on page 5.
- p5: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Bultarium Bomanuin' at page 5, column 1, middle, interrupts the Latin body word 'qui spe- | ...' (spectant) in section 30.

### `bullarium-continuatio.volume-18.line-00021533.discovery-01.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googl') is absent: no provider mark on page 1; column 1 paragraph break inside 'exi- " - . | tu- litis' keeps natural order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head "■ ' Pius PP. Octavus / ■133" at page 1, column 1, bottom, interrupts the body sentence 'ut salvo cujuscumquo | jure' in section 1.
- p2: No provider mark on page 2.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Volume signature furniture 'BuH Rom. fom. IT///.' at page 2, column 1, top, interrupts the body sentence 'vel specialibus | constitutionibus et ordinationibus' in section 4.

### `bullarium-continuatio.volume-18.line-00021533.discovery-03.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digilizcc by Googie') is absent: no provider mark on page 1; column 1 paragraph break after 'apostolorum ejus , | auctoritate' keeps natural order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pius PP. Octavus : / 135 / *' at page 1, column 1, bottom, interrupts the body sentence 'auctoritate apostolica tenore | praeienUum (praesentium) perpetuo communicamus' in section 2.

### `bullarium-continuatio.volume-18.line-00021533.discovery-04.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Google') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Biillariuni RonianuQi / irX)' at page 1, column 1, middle, interrupts the body word 'profestus ha- | b(Mur»' (habeatur) in section 2.
- p2: No provider mark on page 2.

### `bullarium-continuatio.volume-18.line-00022349.provider-marks-omitted-v2` — CHANGES_REQUIRED

Prior defect: NOT fully absent: a residual damaged signature remains.

- p1: Prior provider-mark defect ('Diqitized by Gooqle') is absent from page 1 (see page 2 for a remaining damaged signature fragment).
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pius PP. Octarus / 157' at page 1, column 1, middle, interrupts the body sentence 'coronae aliquid | fulgoris' in section 1.
- p2: BLOCKING: Residual damaged modern provider mark: page 2, column 1, middle, standalone line 'by Cixylc' (damaged tail of 'Digitized by Google') immediately after the dating clause. Prior provider-mark defect ('Diqitized by Gooqle') is NOT fully absent: a damaged signature fragment remains.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Running furniture 'BuU. Kam. Tom. XYIU. / S5 / 138 / Baliarium Romanum' follows at the boundary between the dating clause and the appended office/decree notes (nonblocking position; recorded with the mark).

### `bullarium-continuatio.volume-18.line-00022620.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Coogie') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'I^ius l^P. Octavhfi \ / 159' at page 1, column 2, top, interrupts the body sentence 'ut no- V - V. \ | vt crectk) alteri cap|>cUsniae loci' in section 2.

### `bullarium-continuatio.volume-18.line-00022878.part-01.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digilized by Coogie') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pius PP. Octavus / 141' at page 1, column 1, lower third, interrupts the body word 'pcrloi-btillo* | nes' (perturbationes) in section 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume signature furniture 'BvU. Rom.Tom. XV/JL' fused at page 1, column 2, bottom, into the body word 'qui- | que' (quique) in section 2.
- p2: No provider mark on page 2.

### `bullarium-continuatio.volume-18.line-00023244.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ("' by Coogle") is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head '/ / Pius PP. Ocutus 143' at page 1, column 1, bottom, interrupts the body sentence 'ab hac luce | nigraveriot (migraverint)' in section 1.

### `bullarium-continuatio.volume-18.line-00023326.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by GuogI') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Dcrofttk) / llr«ri»run / 144' at page 1, column 2, bottom, interrupts the body sentence 'empbyteulious fuodua | ... cum adjieiis rebus' in section 3 (continues on page 2 after a further 'Bullarlum Romanum' head).
- p2: No provider mark on page 2.
- p2: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Bullarlum Romanum' at page 2, column 1, top, interrupts the same body sentence 'fuodua | cum adjieiis rebus ...' carried from page 1.

### `bullarium-continuatio.volume-18.line-00023558.part-01.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Di>j\\...') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Pilis n*. Octavus / 145' at page 1, column 1, middle, interrupts the body word 'Alhoaa*» | nuo' (Ulyssiponensis nuntio) in section 2.

### `bullarium-continuatio.volume-18.line-00024403.part-01.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitized by Googie') is absent: no provider mark on page 1.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head 'Plus PP. Octavus / 151' at page 1, column 2, top, interrupts the body word 'com- | miUeodo' (committendo) in section 2.

### `bullarium-continuatio.volume-18.line-00024403.part-02.provider-marks-omitted-v2` — PASS

Prior defect: the classified provider footer is absent and no provider mark remains.

- p1: Prior provider-mark defect ('Digitizod by Googlc') is absent: no provider mark on page 1; column 1 paragraph breaks ('fungeris , | facultatibus') keep natural order.
- p1: QUALIFICATION (non-blocking under continuation-series standard): Volume running head '152 / Bullarlum Romanum' at page 1, column 2, middle, interrupts the body sentence 'sanes ac suppleas , | ac quamcamque proviociam ...' in section 2.
- p2: No provider mark on page 2.

## Individual page evidence

| Source ID | Page | PNG SHA-256 | Original status | Re-issued status | Observation |
| --- | --- | --- | --- | --- | --- |
| `bullarium-continuatio.volume-18.line-00015238.part-01.provider-marks-omitted-v2` | 1 | `7e9117efdbae63dc30f581d79ac8d7edf1840f837fab98bb0be1f1e36a475a52` | CHANGES_REQUIRED | PASS | Title, literal issuer 'Pius pp. vm.', Latin label and omitted date agree with metadata. Two clean columns, margins and gutter sound. Dating clause 'Datum Romae ... pontificatus Nostri anno primo' then source/rights apparatus in column 2. No provider mark visible. |
| `bullarium-continuatio.volume-18.line-00015238.part-02.provider-marks-omitted-v2` | 1 | `00f91723852e879921019dbc069b6b78d965b7cbab4c92064831d4203c4f1d64` | CHANGES_REQUIRED | PASS | Title, literal issuer 'Pius PP. vm.', Latin label and omitted date agree. Two columns, sound margins. Dating clause and apparatus close column 2. Literal OCR noise ('t«or eoa.', black square) retained. No provider mark visible. |
| `bullarium-continuatio.volume-18.line-00015470.provider-marks-omitted-v2` | 1 | `a87186575e9371d25a7f36ab6777be8911defa96e11ff8576314c07bfc379d81` | PASS | PASS | Title, literal issuer 'Pius PP. Vlll.', Latin label and omitted date agree. Two columns, sound gutter/margins. Column 1 lower: paragraph break inside 'fra- / tris' (likely the omitted-mark seam); words continue in natural order. Column 2 ends with section 3, OCR fragments 'D«r*f4lto / ilrartoraa' and running head 'Pius PP. Octayus' at a sentence boundary (after 'quibuscumque.'), nonblocking. Literal OCR noise retained. |
| `bullarium-continuatio.volume-18.line-00015470.provider-marks-omitted-v2` | 2 | `8b2a2c26b67afb0cb5e056a969a98cc9a135c145719d3ac1f3ad8e9f8c7cbae2` | PASS | PASS | Folio '91' then 'Praesentibus perpetuis futuris temporibus valituris.' and dating clause 'Datum Romae ... secunda martii ... anno primo', then source/rights apparatus. Sparse final page with genuine source closing; not apparatus-only. |
| `bullarium-continuatio.volume-18.line-00015849.provider-marks-omitted-v2` | 1 | `2e655872d8b1c04333487c9a6aa16133cba3870561c388be5f20c8000d99a8c0` | CHANGES_REQUIRED | PASS | Title (allocution synopsis), literal issuer 'Pius PP. OctaTus', Latin label and omitted date agree. Two columns, sound margins/gutter. Literal OCR noise and black square retained. |
| `bullarium-continuatio.volume-18.line-00015849.provider-marks-omitted-v2` | 2 | `b82a22d431adbe410076e065e1a95bc6f59d7190444a21fc32b1a04f9f9c2a03` | PASS | PASS | Continues the cardinal list, closing formula 'In nomine Patris et Filii et Spiritus 1^ sancti Amen.' then source/rights apparatus in column 1. Sparse final page with genuine source closing. |
| `bullarium-continuatio.volume-18.line-00016096.part-01.provider-marks-omitted-v2` | 1 | `b95fd06927c8f9a246e41ecc99292030385ac3d297032f73d56d87367a91d31f` | CHANGES_REQUIRED | PASS | Title, literal issuer 'Pius PP, rm. »', Latin label and omitted date agree. Two columns, sound margins. Column 2 holds section 3, dating clause 'Datum Romae ... vicesima tertia martii ... anno primo' (with OCR fragment 'raricrM') and apparatus. |
| `bullarium-continuatio.volume-18.line-00016498.provider-marks-omitted-v2` | 1 | `8b3946770ece6246adba1c2310232e8f61ececf5d1d2095496faee59f29fc871` | CHANGES_REQUIRED | PASS | Title, literal issuer 'Pius PP. vm.', Latin label and omitted date agree. Dense two columns, sound gutter and margins. Literal OCR noise retained. |
| `bullarium-continuatio.volume-18.line-00016498.provider-marks-omitted-v2` | 2 | `24846ed4029fc5a44ac282be370b0448112efc610cde5a9f5d97dabbf69bf61a` | CHANGES_REQUIRED | PASS | Sections 5-6, dating clause 'Datum Romae ... trigesima martii ... anno primo' and apparatus in column 2. No clipping or overlap. |
| `bullarium-continuatio.volume-18.line-00016916.part-01.provider-marks-omitted-v2` | 1 | `35cf6c48b02172fe7c9434bd70fcc4630ba9e7594261872a9e35f595f50bb92f` | CHANGES_REQUIRED | PASS | Five-line OCR title, literal issuer '. ; . Phu PP. VIU. i . .', Latin label and omitted date agree. Two columns, sound gutter and margins. Literal OCR fragments ('cubjuu»m.', 'ust.') retained in section 3. |
| `bullarium-continuatio.volume-18.line-00016916.part-01.provider-marks-omitted-v2` | 2 | `7ad50fbfc1a7db0195f897d270f82257189431bb52e2edf485bad0d6915d9a7a` | PASS | PASS | End of section 4, dating clause 'Datum Romae ... secunda aprilis ... anno secundo' and apparatus in column 1. Sparse final page with genuine closing. |
| `bullarium-continuatio.volume-18.line-00017193.provider-marks-omitted-v2` | 1 | `b1d90626a927301a858bc53687acfbeaf61fbd0f35be861f3371ea2819f33165` | PASS | PASS | Title, issuer 'Pius PP. VIII.', Latin label and omitted date agree. Two columns, sound margins. Several OCR line-break paragraph splits ('locum, / quae', 'gloria, / animeruiii', 'utilius / exercere', 'decreta, / reformandi', 'intuitu, / ac.') keep natural word order. Section 2 opening retains garbled OCR fragments. No running head on this page. |
| `bullarium-continuatio.volume-18.line-00017193.provider-marks-omitted-v2` | 2 | `628a91c51ebd09f07fb29fa703de868849be93ad3aaab3910899c2a9534eb29e` | CHANGES_REQUIRED | PASS | Section 4, dating clause 'Datum Romae ... sexta aprilis ... anno secundo' and apparatus in column 1. |
| `bullarium-continuatio.volume-18.line-00017494.part-02.provider-marks-omitted-v2` | 1 | `b9c8d575a5a63b0cea5098413d6ce818abe13b81e115672fee98e6ecd217c75d` | CHANGES_REQUIRED | PASS | Title, literal issuer 'Pius PP. VIII. n:.; .', Latin label and omitted date agree. Two columns; heavy OCR noise lines and black squares near the opening are literal. Dating clause 'Datum Romae apud sanctam ... Majorem ... anno secundo' and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00017701.provider-marks-omitted-v2` | 1 | `36b3906928d1f84e12942d8e971c7189c857543dded7fcdb0be421ebd28faf47` | CHANGES_REQUIRED | PASS | Title, literal issuer 'Pius PP. ViU.', Latin label and omitted date agree. Two columns, sound margins. Dating clause 'Datum Romae ... vicesima quinta maii ... anno secundo' and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00017862.provider-marks-omitted-v2` | 1 | `cda86eb434a4affe98549e9767dad63c5842624f32b4f68aeeaee97c664ede47` | CHANGES_REQUIRED | PASS | Four-line OCR title, issuer 'Pius PP. VIII.', Latin label and omitted date agree. Two columns, sound margins. Dating clause (vicesima quinta maii, anno secundo) and apparatus close column 2. |
| `bullarium-continuatio.volume-18.line-00017980.provider-marks-omitted-v2` | 1 | `e6dd7191daf005fa4cce159e828269bcb34d016d8e1ce441c744ee4afbaf42da` | CHANGES_REQUIRED | PASS | Two-line OCR title (begins mid-synopsis 'superiorum majorum ...'), issuer 'Pius PP. VIII.', Latin label and omitted date agree with frozen metadata. Two columns, sound gutter and margins. |
| `bullarium-continuatio.volume-18.line-00017980.provider-marks-omitted-v2` | 2 | `65ee8bd2f8a782d70dd04aea6c788f0fe8af6fb7159cc1e288e4c817a7f4bd93` | PASS | PASS | Sections 4-6 with several OCR line-break paragraph splits ('fo- / it', 'spe- / ctat*', 'comlituliooi- / pmititoeei', 'ju- / ramento', 'publici / subscriptis') that keep natural word order; dating clause 'Delum Romae ... vicesima octava maii ... anno aecundo' and apparatus in column 1. No running head on this page. |
| `bullarium-continuatio.volume-18.line-00018126.provider-marks-omitted-v2` | 1 | `f49eb100f71145728b3bd210350c924e1edd789c37ef2a3a1fe0fa559ef67651` | CHANGES_REQUIRED | CHANGES_REQUIRED | Three-line OCR title, literal issuer 'Pius PP. YUI.', Latin label and omitted date agree. Two dense columns, sound gutter and margins. |
| `bullarium-continuatio.volume-18.line-00018126.provider-marks-omitted-v2` | 2 | `fdb0980755823aeeb9b001d2cb485987e3a94c95783122b5d2c7ac7c58a8d3b4` | CHANGES_REQUIRED | PASS | Sections 3-6, dating clause 'Datum Romae apud sanctam Mariam Majorem ... anno secundo' and apparatus in column 2. Column 2 paragraph breaks 'privile- / glis' and 'ut / praefertur' keep natural order. |
| `bullarium-continuatio.volume-18.line-00018492.provider-marks-omitted-v2` | 1 | `4ecfa92619ba6252c28e7c18309a6ae21130c8363157b94a0cfa8ac7abc5074a` | PASS | PASS | Four-line title, literal issuer 'Pius pp. vm.', Latin label and omitted date agree. Running head 'Pius PP. Octavus' (column 1 end) and folio '111' (column 2 top) sit at a sentence boundary between 'quibuscumque.' and the dating clause; nonblocking. Dating clause 'Datum Roina^ ... quinta junii ... anno se- / CDOdO.' and apparatus in column 2. Literal OCR fragments ('n«roc«ti«', '***^**') retained. |
| `bullarium-continuatio.volume-18.line-00018761.provider-marks-omitted-v2` | 1 | `ae01f8d14b7386a4de2889f94c8847e108a3f06b14264fe648b9571384b361cc` | CHANGES_REQUIRED | PASS | Two-line OCR title, issuer 'Pius pp. VIII.', Latin label and omitted date agree. Two columns, sound margins. Column 1 opening retains garbled OCR lines ('c«rain tiape» ~ . ®') with paragraph splits that keep order. |
| `bullarium-continuatio.volume-18.line-00018761.provider-marks-omitted-v2` | 2 | `272dd23c3e51f031155a43bd283917b7d7484b702d3db0820f41244ad70172cc` | PASS | PASS | Sections 2-3 continue cleanly; dating clause 'Datum Hornae apud sanctam Mariam Majorem ... sexta julii ... anno secundo' and apparatus in column 2. No running head on this page. |
| `bullarium-continuatio.volume-18.line-00019150.provider-marks-omitted-v2` | 1 | `eebecc073a90e94890664dab29e8b57d852f65b07ce7dc9581e20a23e1492056` | CHANGES_REQUIRED | PASS | Two-line OCR title, issuer 'Pius PP. VIII.', Italian label (motu proprio, Italian body) and omitted date agree. Two dense columns, sound margins. Column 2 paragraph break 'molo-proprio / dei 12 agosto' keeps natural order. |
| `bullarium-continuatio.volume-18.line-00019150.provider-marks-omitted-v2` | 2 | `c0aff903892fa3d58a393f055f23c2d49a0fbd7cf807b2ea08cad7fe1a8b772a` | CHANGES_REQUIRED | PASS | Italian body continues in two columns; section 3-4 headings with literal roman-numeral markers. Literal OCR noise and black squares retained. |
| `bullarium-continuatio.volume-18.line-00019150.provider-marks-omitted-v2` | 3 | `df538874bec047f1c977acb7dc7560d14c4d89b124e11fbbfee07d21d76e05d8` | CHANGES_REQUIRED | PASS | Sections 4-8 continue; several OCR line-break paragraph splits keep natural word order. |
| `bullarium-continuatio.volume-18.line-00019150.provider-marks-omitted-v2` | 4 | `cca119a172f42edde90e3e8bbb0e0e3597ed04908bcb5a448d7836443c7c8a31` | CHANGES_REQUIRED | CHANGES_REQUIRED | Sections 9-13 in two columns; column 1 stray 'ip» I / vni.' OCR furniture between sections; literal OCR noise retained. |
| `bullarium-continuatio.volume-18.line-00019150.provider-marks-omitted-v2` | 5 | `5978f62415aa2ab64935ca327b06ec92518ee940f214ca11535a194a64605bc5` | PASS | PASS | End of section 13 and derogation clause, natural closing 'Dato dal Nostro palazzo apostolico Quirinale questo di 23 luglio ... pontificato anno secoado.' and subscription 'Pios PP. Vlii.', then source/rights apparatus in column 2. Genuine closing on final page. |
| `bullarium-continuatio.volume-18.line-00019727.discovery-01.provider-marks-omitted-v2` | 1 | `5a428349e811fb72acf0d76ab94bfa57963c7152cbe03e961c3c7a954e53defb` | CHANGES_REQUIRED | PASS | Two-line OCR title, literal issuer 'Pilis PP. Oclaviis', Latin label and omitted date agree (bull form 'Servus servorum Dei'). Two columns, sound margins. Several OCR paragraph splits keep natural order. |
| `bullarium-continuatio.volume-18.line-00019727.discovery-01.provider-marks-omitted-v2` | 2 | `a50adfc288f60079eeb985d404d7f5e04c8d4f147b4d446d3f52ad14b3b30758` | CHANGES_REQUIRED | PASS | Parish list, sections 8-11, sanction clause 'Nulli ergo omnino hominum ...', dating clause 'Datum Romae apud sanctam Mariam Majorem ... sexto kalendas augusti ... anno secundo' and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00020089.discovery-01.provider-marks-omitted-v2` | 1 | `6d480b39f703165a3ddef333fb600a9254fbef73c5dd9aaa9342b8a54df0f667` | CHANGES_REQUIRED | PASS | Three-line OCR title, issuer 'Pius PP. VIII.', Latin label and omitted date agree. Two columns, sound margins. Dating clause 'Datum Romae apud sanctam Mariam Majorem ... prima augusti ... anno secundo' and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00020473.provider-marks-omitted-v2` | 1 | `781d9f8bb735c381521e88b60d8651c3e30377651596a2017b410c4f884964e3` | CHANGES_REQUIRED | PASS | Three-line OCR title, literal issuer 'Pius PP., VIU.', Latin label and omitted date agree. Two columns, sound margins. Dating clause 'Datum Rboue apud sanctam Mariam Majorem ... prima augusti ... anno sectindo' and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00020888.provider-marks-omitted-v2` | 1 | `a02adf7f7263e0809a255561acee4f372074d73e7709d411b167c2e709d423dc` | CHANGES_REQUIRED | PASS | Two-line OCR title, literal issuer 'Pius pp. vin.', 'Latin and Italian' label (mul) and omitted date agree: Latin brief with inserted Italian statutes in source order. Two columns, sound margins. Literal OCR noise and roman-numeral chapter markers retained. |
| `bullarium-continuatio.volume-18.line-00020888.provider-marks-omitted-v2` | 2 | `bf380e15ee704cd57043ee561c60442f3493faa5f396b54a06c6691ce9d316f5` | CHANGES_REQUIRED | PASS | Italian statutes sections 7-15 continue in two columns; several OCR paragraph splits keep natural order. |
| `bullarium-continuatio.volume-18.line-00020888.provider-marks-omitted-v2` | 3 | `e3c6e34495d9c63187736508c89baa3c43665497d6ab92f1419e531985f8d569` | CHANGES_REQUIRED | PASS | Italian statutes sections 16-22. Column 2 running head '33 / 150 / Bullarium Romanum' plus garbled lines sits at a section boundary before 'xvu.' (nonblocking). Several OCR paragraph splits keep natural order. |
| `bullarium-continuatio.volume-18.line-00020888.provider-marks-omitted-v2` | 4 | `e398e7fc245b0883bb06b0488dfdf23978753a47014b8320bd66fa313f84688f` | PASS | PASS | Statutes sections 23-27, roll of officers, then Latin resumes (sections 28-29). Running head 'Pius PP. Octavus / 131' with garbled lines in column 1 sits at a section boundary before 'XXII.' (nonblocking). Literal OCR noise retained. |
| `bullarium-continuatio.volume-18.line-00020888.provider-marks-omitted-v2` | 5 | `1d0a394af385b625698bb2894c0f18eee60315895f7d1f2fde13e164e0c09f11` | CHANGES_REQUIRED | PASS | Sections 30-33, dating clause 'Datum Romae apud sanctam Mariam Majorem ... vicesima quarta mensis augusti ... anno secundo' and apparatus (which discloses the incorporated Italian statutes) in column 2. |
| `bullarium-continuatio.volume-18.line-00021533.discovery-01.provider-marks-omitted-v2` | 1 | `879b45ebf10213b236af2edc4411d21dcdcc626f8c0271f6540e085c807703d0` | CHANGES_REQUIRED | PASS | Three-line OCR title, literal issuer 'Pios PP. VIII,', Latin label and omitted date agree. Two columns, sound margins. Column 2 paragraph breaks ('G- / lium', 'valo- / rnn') keep natural order. |
| `bullarium-continuatio.volume-18.line-00021533.discovery-01.provider-marks-omitted-v2` | 2 | `86cb531ab7acd7710031caedb8dc47412bfb2502a01f1995a174a7652465d671` | CHANGES_REQUIRED | PASS | Section 4 end, dating clause 'Datum Romae apud sanctam Mariam Majorem ... decima tertia augusti ... anno secundo' and apparatus in column 1. Sparse final page with genuine closing. |
| `bullarium-continuatio.volume-18.line-00021533.discovery-03.provider-marks-omitted-v2` | 1 | `50bdbc158e35110070f3ccd5bd8201745c8e6a069270260ee860a9cc3decc557` | CHANGES_REQUIRED | PASS | Three-line title, literal issuer 'Pius PP. YIU.', Latin label and omitted date agree. Historical date note 'D»C Si« 17 aon"i 183S mao M.' retained literally. Dating clause 'Datum Romae ... decima septima augusti ... anno secundo' and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00021533.discovery-04.provider-marks-omitted-v2` | 1 | `19aea86c1a78a9beaf739ffe49968775c8d13756bd886cdc89b2497c695e4606` | CHANGES_REQUIRED | PASS | Two-line OCR title, issuer 'Pius PP. VIII.', Latin label and omitted date agree. Two columns, sound margins; column 2 ends mid-sentence and continues on page 2. |
| `bullarium-continuatio.volume-18.line-00021533.discovery-04.provider-marks-omitted-v2` | 2 | `f886b716b40b83d96bf7bc512280ba46cafac57bd575af19fb5041ec558b2cb7` | PASS | PASS | End of section 3, section 4, dating clause 'Datum Romae apud sanctam Mariam Majorem ... vicesima augusti ... anno secundo' and apparatus in column 1. Sparse final page with genuine closing. |
| `bullarium-continuatio.volume-18.line-00022349.provider-marks-omitted-v2` | 1 | `c28e46a38e96df9c6e9a47b1783fc319a1a0e15b7e4395586888fc37f7f63a82` | CHANGES_REQUIRED | PASS | Two-line OCR title, issuer 'Pius PP. VIII.', Latin label and omitted date agree. Two columns, sound margins. Column 2 paragraph splits ('intarpielatiooi- / bus', 'ek<fer i / cernimus') keep natural order. |
| `bullarium-continuatio.volume-18.line-00022349.provider-marks-omitted-v2` | 2 | `ffa7d0628ad6f6e696350ddf8e1ceb86a693365dc0b401afc224d33bd2ae22a5` | CHANGES_REQUIRED | CHANGES_REQUIRED | Sections 4-6, dating clause 'Datum Romae ... vicesima augusti ... anno secundo', then appended historical office lessons and Sacred Rites decree with subscriptions ('C. M. episcopus Praenest. ...', 'Loco Sigilli', 'J. G. Falati S. R. C. secretarius') and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00022620.provider-marks-omitted-v2` | 1 | `b19fe1698c6166271388fb85f4e9f4f1be04fd5f7bc9be0c0b6db77146e4a9af` | CHANGES_REQUIRED | PASS | Three-line title, literal issuer 'Pius pp. vni.', Latin label and omitted date agree. Two columns, sound margins. Column 1 paragraph break 'No* .4 / bis petiit' keeps natural order. Dating clause 'Datum Romae ... trigesima prima augusti ... anno secundo' and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00022878.part-01.provider-marks-omitted-v2` | 1 | `4249a69066f5ba17754741b4423847b045a18e886a58c50132f24858d0fd9eef` | CHANGES_REQUIRED | PASS | Four-line OCR title, literal issuer 'Pius PP. vm.', Latin label and omitted date agree. Two dense columns, sound margins. |
| `bullarium-continuatio.volume-18.line-00022878.part-01.provider-marks-omitted-v2` | 2 | `5eb904ce8f424273261cd65a04cdf11578ac45b117929b929463895484b3c17f` | PASS | PASS | End of section 2, sections 3-4, dating clause 'Datum Romae ... decima septima septembris ... anno secundo' (with OCR split 'octin- / i genlosimo') and apparatus in column 1. Paragraph break 'literas firmas, / et elTicaccs' keeps natural order. Sparse final page with genuine closing. |
| `bullarium-continuatio.volume-18.line-00023244.provider-marks-omitted-v2` | 1 | `8ec2319718aa826d0c315e025bcb77929df95846f3f290d6ebc03e8ba7a2374d` | CHANGES_REQUIRED | PASS | Four-line title, issuer 'Pius PP. VIII.', Latin label and omitted date agree. Two columns, sound margins. Dating clause 'Datum Romae ... vicesima quarta Septembris ... anno secundo' and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00023326.provider-marks-omitted-v2` | 1 | `f58231173b8dcfc6245bd8616ca78243045185cbc346f9a33cab66ea1d0ad0dc` | CHANGES_REQUIRED | PASS | Two-line OCR title (begins 'st emphyteuticandi'), literal issuer 'Piui PP. VUI.', Latin label and omitted date agree. Two columns, sound margins. Column 1 paragraph splits ('possidere / in majori', 'Porta / germani', 'peculiari / beneficentia') keep natural order. |
| `bullarium-continuatio.volume-18.line-00023326.provider-marks-omitted-v2` | 2 | `38ea29f7a632f8bb58ed578815b7509a0caec94ab0df963bbc0c9c9c4fa68cdb` | CHANGES_REQUIRED | PASS | End of section 3, dating clause 'Datum Romae ... vicesima quarta septembris ... anno secundo' and apparatus in column 1. Sparse final page with genuine closing. |
| `bullarium-continuatio.volume-18.line-00023558.part-01.provider-marks-omitted-v2` | 1 | `af545f2c13bad2ad6f121e88bf48bab3b0aded98aa5658585b1a639c6a881884` | CHANGES_REQUIRED | PASS | Two-line OCR title, literal issuer 'Pius PP. VUI.', Latin label and omitted date agree. Two columns, sound margins. Column 2 paragraph splits ('Bene- / JrlrtJrii', 'divi- / sione', 'consueiudinibus, / oieterisque') keep natural order. Dating clause 'Datum Romae ... vicesima octava Septembris ... anno secundo' and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00024403.part-01.provider-marks-omitted-v2` | 1 | `5d0ca3b8f32e274754fff6329d7e257a80e7aec2be985780b446567bf10060c7` | CHANGES_REQUIRED | PASS | Four-line OCR title, literal issuer 'Pius PP. VIU.', Latin label and omitted date agree. Two columns, sound margins. Dating clause 'Datum Romae ... vicesima tertia novembris ... anno seenndo' and apparatus in column 2. |
| `bullarium-continuatio.volume-18.line-00024403.part-02.provider-marks-omitted-v2` | 1 | `d93d6c4409c81a51e1464d11d250a4291dc780feebfdbd9806330e981cd3b7c9` | CHANGES_REQUIRED | PASS | Four-line OCR title, literal issuer 'Pius PP. VUI.', Latin label and omitted date agree. Two dense columns, sound margins. |
| `bullarium-continuatio.volume-18.line-00024403.part-02.provider-marks-omitted-v2` | 2 | `c3a89b1b3740a8becb06fd2adec85085ff5c5bd587e2c33dcdec0e50deadfc3f` | PASS | PASS | End of section 2, sections 3-4, dating clause 'Datam Romae apud sanctam Mariam / Majorem ... vicesima sexta novembris ... anno secundo' and apparatus in column 1. Sparse final page with genuine closing. |

## Limitations

- Text is literal, uncorrected and uncollated historical OCR. Historical spellings, abbreviations, OCR corruption, black squares, running heads, folios, printer signatures and rule fragments are retained as qualifications under the continuation-series standard, including where they interrupt a sentence.
- Removal-seam paragraph breaks left by omitting modern digitizer marks are qualifications, not defects.
- Layout and visual review only: no word-level collation against the 1856 printing, no historical authentication, and no claim of publication, installation or deployment.
- Act dates remain unresolved in the frozen metadata; no date was inferred or repaired.
- The re-issue reclassified the original observations without re-opening pages.
