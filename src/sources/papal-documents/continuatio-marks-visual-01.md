# Continuatio provider-mark corrections visual review 01

**Re-issue with re-verification.** CHANGES_REQUIRED overall: 28 assigned PDFs, 55 pages individually opened at full size in the original pass, 21 pages re-opened at full size during re-verification; final 0 PASS, 28 CHANGES_REQUIRED. Zero reused pages. This report covers only lane 01 of batch `continuatio-marks-0001` (Bullarii Romani continuatio, tomes XIV and XVIII).

Status history: first issue 2 PASS / 26 CHANGES_REQUIRED (running heads treated as blocking); re-issue 15 PASS / 13 CHANGES_REQUIRED (continuation-series standard); this re-verification 0 PASS / 28 CHANGES_REQUIRED (fused marginal-summary labels found by full-size re-viewing). Every earlier finding is kept below.

## Re-issue: what changed and why

The first issue of this report (SHA-256 `2217f43697c55d7549f1880a7204c17f02d384912116ab96d2aa209650e0a75f`; result `4cf1e4261a2b9ac268b0ceefed4e6ce50200cf67d4af9e77558f1e48c8d8ca14`) rated 26 documents CHANGES_REQUIRED, chiefly because historical running heads and printer signatures interrupted body sentences at the former page-foot joins. The coordinator ruled that this lane must apply the established continuation-series standard under which the 397 installed continuation readers were reviewed (`historical-series-visual-16.md`: the uncorrected-OCR qualification "covers historical spellings, abbreviations, running-head and rule fragments; it does not cover modern digitizer marks retained in the body").

Under that standard: historical running heads, folios, `Bullarium Romanum` + page number, `Pius PP. ...` heads and printer signatures (`Bull. Rom. Tom. ...`) are non-blocking qualifications even mid-sentence or inside a hyphen split. Remaining modern provider marks, marginal-summary labels or dates fused into body sentences, and displaced notes set mid-sentence remain blocking.

No page was re-opened. The first-pass page observations stand as evidence; every original locus is kept below, reclassified. While reclassifying, the marginal-label category needed a closer reading of the evidence: several documents carry recognizable marginal-summary labels (Derogatio contrariorum, Expositio, Tenor concessionis, Nomina eminentissimorum, Clausula irritans, dated expedition notes) fused inside body sentences or split words. The first pass had grouped these with the running-head breaks or left them unrecorded. They are now listed as blocking. For documents 1-8, whose page images were no longer in the reviewer's working context, a `pdftotext` scan for recognizable marginal-label words was used. It found only labels at paragraph starts. The observation ledger keeps the first-issue lines and appends one note plus one `reissue` line per page.

Classification line used: a fused fragment is blocking when it is recognizable as a marginal-summary label or date; isolated, unidentifiable glyph fragments (for example `Tn»r «n».`, `tnor «●.`, `bolfo Somp*`) are recorded as OCR-noise qualifications. Some of these may be garbled labels of the same kind (for example a "Tenor" label); they are listed by locus so the coordinator can tighten the line if wanted.

## Re-verification (coordinator follow-up)

The coordinator asked that every currently PASS page of readers 1-8 (whose marginal-label classification had rested on a text scan) be re-opened with Read at full size and judged by the same visual rule as readers 9-27, and that three fragments flagged as possibly garbled labels be looked at again. Rule applied: a fragment recognizably of the Tenor / Expositio / Proemium / Derogatio / Clausula (irritans) marginal-summary type, fused inside a body sentence or split word, is BLOCKING. Each re-view is a `reverify: true` line in `observations.jsonl`.

Results:

- Readers 1-8, all 11 PASS pages re-opened: each of the six previously PASS readers has at least one page carrying a fused marginal label, so all six (`line-00045176.part-04`, `line-00049746`, `line-00049754.part-03`, `line-00052913.part-03`, `line-00053407.part-02`, `line-00059193`) are now CHANGES_REQUIRED. The text scan had missed these because the fused labels are garbled (for example `Dcm^atio eoo- / ●tMioram.`, `Drroptisom / irarioruu`, `n*r|»g»t;«rTO`).
- The three named fragments are Tenor labels and are blocking: `Tn»r «n».` inside `fra-ter` (line-00007598), `tnor ««●.` inside `exponen[ti]bus` (line-00009091.part-01) and `Tm»r «m.` mid-sentence (line-00013651.part-02). Re-opening those pages also exposed missed Expositio/Proemium labels (`KipMiu»`, `Promiim`).
- Because the re-verification showed that the first pass had under-recorded garbled labels, the remaining PASS readers among 9-27 were checked against the same rule: `line-00005460`, `line-00009091.part-03`, `line-00010152` and `line-00010476.part-03` page 2 were re-opened at full size; `line-00010476.part-03` page 1, `line-00012995` and `line-00013651.part-01` were judged from full-size images still in this session. All carry a fused label of the listed types and are now CHANGES_REQUIRED.
- Confidence: findings marked "judgment: probable" or "judgment: structural" rest on label shape and formula position rather than a fully legible label (`line-00052913.part-03` p2, `line-00059193` p1, `line-00010152` p2, `line-00010476.part-03` p2, `line-00012995` p2, `line-00013651.part-01` p1-2). They are recorded as blocking because these readers are headed for installation; the coordinator may override them individually.
- Systemic observation: in this source every act prints marginal summaries beside its numbered paragraphs, and the extraction interleaves those labels into body text throughout. All 28 readers in this lane are affected. The defect is likely shared by other continuation readers built by the same extractor, including installed ones; that question is outside this lane and is reported, not assessed.

## Scope and method

Every assigned document is a `provider-marks-omitted-v2` source correction superseding a reader previously rejected for a modern provider signature. For each document the review checked whether any provider mark remains and whether the text at the former page-foot join reads in natural order. Each page PNG produced by the repository `pdf-review` tool was opened individually with the Read tool at full raster size (1700x2200); no contact sheet, re-rasterization, word-level collation or text repair was performed. Supplementary `pdftotext` scans were used only to locate candidate provider-mark and marginal-label strings. Title, issuer, date omission and language label were compared with the frozen metadata; columns, gutters, margins, glyphs, natural closing and terminal apparatus were inspected.

This report does not authorize installation or claim that installation, deployment, historical authentication or publication has occurred.

## Evidence verification

All assigned PDFs, the render receipt, the frozen manifest, the raster run record and all 55 page PNGs were hashed before and after inspection; every digest matched its assignment pin both times.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt `.scratch/typeset_pipeline/claude/continuatio-marks-0001/receipt.json` | `baa1f5617d5758fca7659cac83c33b17e1ca7c6d59997befb4a24d3dc200916a` | Before and after |
| Frozen manifest `.scratch/typeset_pipeline/claude/continuatio-marks-0001/frozen-manifest.json` | `fe821f047335393afda93cb86c97d10d51cf41d2730b3670e520a20d94457f3f` | Before and after |
| Raster run `.scratch/claude-review/rasters-continuatio-marks-0001/review-run.json` | `664e1f7bef4a6a5d605e2b681e37b72281a51f3dde85e7330a90ea166d6e63e6` | Before and after |
| Lane assignment | `3d098c59416ae3542ee80859d7c4a05679448693dde41f0ed444f7b474f8fb91` | Scope binding |
| Before verification record | `7dded05d369c9a7a98d3f6377cc2fac012f0532509346f71d0fbbfd71b923cfb` | PASS (86/86 match) |
| After verification record | `07ef64f78259d4ceb21996fce5588f017470a30c8ac05455f0a5e048a7e1fd42` | PASS (86/86 match; identical digests) |
| Observation ledger | `1ad73542b498cd136c71d1371cb7681ea20dadcd69e3c141b3162f31032ff094` | 55 first-issue + 1 note + 55 reissue + 25 reverify lines |

## PDF outcomes

| Source ID | Date metadata | Language | Pages | PDF SHA-256 | Provider mark | First issue | Re-issue | Final |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `bullarium-continuatio.volume-18.line-00002188.part-02.provider-marks-omitted-v2` | 1829-04-07 | `la` | 3 | `2a67fbd848fdb9360f7d11083aa4e64a7125f3d3f2a6a112fa3b42433ed9765e` | Residual damaged mark | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00045176.part-04.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `44718bf03c0b0b5e247707b96c681ae5b14ec1c234c025dd745950807caa4cb3` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00049746.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 1 | `1889bfe638a63e545a50480bf582b5626cfae511076ad0d0c8227dff65360571` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00049754.part-03.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 1 | `564912b1fd0ca96d550241962e45fd99f422a455331cad396184ffd39c08f1b1` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00050183.part-01.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `cf7541bce8352ddb783e9fba53aa48e90082038bc9ad7ea126349eb57047abe3` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00050617.part-01.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 3 | `60587fee7a54700eec53a144ed0020998ffca18656296a86ab045c569e902d33` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00052913.part-03.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 3 | `d52bfe8911f6ac5071a8609611eaf84ac6741e1d28583bf1e0bf78514585067e` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00053407.part-02.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `b1d81c6cc081201ddeb90cde67ec5741aa2de79d2409af22699477c823c94912` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00059193.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `25cdb869e6cf4e288404d6baf8873478a99f6c5832edd6e1a1837feb3e1cdfdd` | Absent | PASS | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00059362.part-03.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `f7c7b0e5ef0eb3f1d4b2452fbfceff2e75d86338b50c5b32c1574609364afa61` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00078623.part-02.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 1 | `c36c84e40cda355b1c0622466c44add3a66e3f770c4eec4e5a4ea9d20770e694` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00080476.part-02.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `eb861141e992bac18a53d876fce28f51aba2f6060cf0a9290b7edd3cd6581c06` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00080476.part-03.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 1 | `31c8e4dc246e74f88c67fc8437774e29095216127fe807a474e984dffe8f41ca` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00080476.part-04.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `00170aaab53c25ba725cfd8eecc062bee348059a09dc852eb92ba539a2298e62` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00005460.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 1 | `b499bf1296694bd2174f06bbaa50a41b0e8fcd6b2798dec8e9d057cf1eafea41` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00007598.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `c89531b2e28a00d4820481f1bf9d095f687be1c9dc7efd7f61af6df010598a12` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00009091.part-01.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 1 | `72a8d1f2834c51e49f293f961eed90e49b6d9d914656d22daa170058529e6a85` | Absent | PASS | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00009091.part-03.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `b49a1bb2cc40ddacfcdb17099612ab69897052ddc783e8e1de2c5ccfc473c8ca` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00010152.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 3 | `8f67c14f9a1499af743a5c08d638f8fa04655ca35f68c8406f784b9cafe26650` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00010476.part-03.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `cb4e9ebb2d5822f7954bfdcc6e965543f897311577a72647e5f6ed30fd97fef9` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00011084.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 1 | `53ec2e6cedee2ef09965f988d36b5bb8d8c8c70760cc7fcbad700f6ccf8ff2c4` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00012995.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 4 | `621044b699d520f7db6cc9e08ebe8aa6e777866ba7b856c4061b8523ba336e37` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00013651.part-01.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `ce13eae4e503b870a3154cd7d7088b557ff020aabb31d59bc12f9fae168825e5` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00013651.part-02.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `8910eda5dd64a684427aa22165fcb20f8d41ab4e5ffaf3d43f85a60c39c56f22` | Absent | CHANGES_REQUIRED | PASS | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00014020.part-03.provider-marks-omitted-v2` | Unresolved; omitted from title | `it` | 3 | `dacaf5db3c0a7e5852cc270b70307d63e2ee0cabbd27268f172c65d9a4ff95e5` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00014591.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `e9245153becc084b74b306a6f7aa9a10a51541678b10eb19551bc7bed993bb55` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00014946.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 1 | `27a0e29d8ff244488c449689d9288e26bca8f7bf055ac3f9681ca72e8c46a807` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00015042.provider-marks-omitted-v2` | Unresolved; omitted from title | `la` | 2 | `45266030cf7a32cb0c809518b677207ade58639cfa4098ebe9dfa88744c071a7` | Absent | CHANGES_REQUIRED | CHANGES_REQUIRED | CHANGES_REQUIRED |

## Per-document findings

### `bullarium-continuatio.volume-18.line-00002188.part-02.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: NOT fully absent - damaged digitizer residue 'Digilizcxj i';' remains on page 1, column 2.
- Blocking: Remaining modern provider mark: damaged digitizer residue 'Digilizcxj i';' on its own line, page 1, column 2, lower-middle, followed by '\' and 'Pius PP.' running-head furniture, between 'praeeminentia' and 'gaudere debeas' (§5). Prior provider-mark defect not fully absent.
- Non-blocking: Page 2: Running head '4 / Bullarium Romanum / •m' splits 'thesaura- | rk) gonorali' (column 2, middle, §8); 'Octavus 5' residue before §7 (column 1).

### `bullarium-continuatio.volume-14.line-00045176.part-04.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label (Derogatio contrariorum) 'Dcm^atio eoo-' / second line '●tMioram.' fused inside 'felrìs re- | ... cordationis' (page 1, column 2, middle, §4).
- Non-blocking: Page 1: Running head '43* / 340 / Bullarfum Romanum' interrupts 'hujus | tantum' (column 1, lower, §2); unidentified fragments 'Tiu>|', '«ioni*' inside 'soffra- ganeura' and 'qui- bus' (column 1, §2) and 'hu, et dmre', 't*un ufi lan*.' inside 'prae- sentes' and 'effi- caces' (column 2, §3).

### `bullarium-continuatio.volume-14.line-00049746.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label (Derogatio contrariorum) 'Drroptisom' / second line 'irarioruu' fused inside 'constitu- ... tionibus' (page 1, column 1, foot, §3).
- Blocking: Fragment 'iionu' (second line of the marginal label 'Tnioroomoi' at §2) fused inside 'exponcn- ... tes' (column 1, lower-middle, §2).
- Non-blocking: Page 1: Running head '335 / Pius PP. Septimu»' splits 'supplica- | ri fecerunt' (column 1, middle, §2); marginal date '18. julii 1817 / ioo X Vili.' at the synopsis head.

### `bullarium-continuatio.volume-14.line-00049754.part-03.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label (Derogatio contrariorum) 'n*r|»g»t;«rTO' / 'l'*rw>rum-' fused inside the §5 sentence 'quatenus ... opus sit, quihusvis coostitulionibus ... et ordinationibus' (page 1, column 2, middle).
- Blocking: Probable Clausula-irritans label fragment ',ura irriltu>>' fused inside 'nul- | ... lo unquam' (column 2, upper, §4).
- Non-blocking: Page 1: Running head '562 / Bulìarium Romamira' (column 2, §6); signature 'Bull. Rorn. Tom. XIV I. 106.' (column 1, §2); 'Proemio»' label at §1 start (boundary); unidentified fragments 'liooT*.****4*', '««m i', ',toDI*'.

### `bullarium-continuatio.volume-14.line-00050183.part-01.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label fragments 'Nomina rmi- nenliuimo-' and 'uenliMimo- . , . r» i-' (Nomina eminentissimorum) fused into the formula 'Auctoritate omnipotentis Dei, ... [beato]rum apostolorum' (page 2, single column, middle).
- Non-blocking: Page 1: Running head 'Pius PP. Septimus 363' splits 'in li- | teras' (column 2, middle).
- Non-blocking: Page 2: Printer's signature '...Bull. Iiom. / Tom. XIV. F. 106.' interrupts 'presby* | teros cardinales' (page 2, middle).

### `bullarium-continuatio.volume-14.line-00050617.part-01.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Displaced historical footnote '(4) Kp. ad Pulcher. Aug. xlix. <2 ) i\ahum± 3. 2.' set mid-sentence between 'ut nonni -' and 'si ex longa' (page 1, column 2, middle).
- Non-blocking: Page 1: Running head 'BuIlarium Romanum / 3C(>' interrupts 'religio, et | pietas' (column 1, lower).
- Non-blocking: Page 2: Running head 'Bullariura Ròraanum / 3SS' splits 'dioece- | sihus' (column 2, lower, Art. XI).
- Non-blocking: Page 3: Running head 'Pius PP. Septìmus 3GJT' interrupts 'lollendo , | ac conventione' (column 2, top, §6).

### `bullarium-continuatio.volume-14.line-00052913.part-03.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Three-line marginal-label block 'cjmwia rob-' / ',,u ,l J*0»' / 'Um' at the §7 Decernentes clause: its continuation lines split 'eas- | dem' and 'vali- | das' (page 2, column 2, lower-middle). Same structure as the Clausula/Decretum-irritans blocks blocked in line-00053407.part-02 and line-00009091.part-03; text of this block itself is not legible (judgment: structural).
- Non-blocking: Page 1: Labels '»ro«BÌB«.' (§1), '*tpa»iiio p„' (§2, Expositio-type) and 'p notanti*' (§4) at paragraph starts; their unrecognizable continuation glyphs '«■■».' and 'dS^ur.1™ ^ »' sit inside §2 and §4 sentences (column 1 and 2); running head '385 / Pius PP. Septirans' at the §3/§4 boundary.
- Non-blocking: Page 2: Signature/running head 'Bull. J torri. Tom. XI V. F. 108. / Ài / 58G / Bullarium Romannm' splits 'auctorita- | te' (column 2, top); label 'A»piiiodo' at §3 start; fragment 'u.rwii . «' inside §3 sentence.

### `bullarium-continuatio.volume-14.line-00053407.part-02.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Three-line marginal-label block '■cimmsU iub-' / 'itu, et de<x-' / 'A»m iriiufl*' (Clausula / decretum irritans type) at §3: continuation lines split 'praesen* | ... tes' and 'effi- | ... Caces' (page 2, column 1, upper-middle).
- Non-blocking: Page 1: Signature/running heads at page-break joins (column 1 lower, column 2 middle); synopsis-head marginal date '26 icptambm / *nno xvui.'; unidentified fragments ''^a*as su^ pluni)»o', 'ine^bmioaù', 'n rwpteti*.»', 'atoemnrM' inside §1-2 sentences.
- Non-blocking: Page 2: Label '●JOwwùo «r.»' at §4 start with fragment 'totiofuw.' inside 'apostolici[s ...]' (column 1, middle).

### `bullarium-continuatio.volume-14.line-00059193.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Tenor-type marginal label 'Tnircm»' at §2 with continuation '22*.*°"°""' splitting 'tuis- | ... <luc' (tuisque) (page 1, column 1, lower-middle). Same 'T-n-r' label shape as the Tenor labels in line-00007598, line-00009091.part-01 and line-00013651.part-02 (judgment: probable).
- Non-blocking: Page 1: Running head 'Pius PP. Septimus 43?' and label 'lata, et decre- tili» irtiliM.' (decretum irritans) between §3 and §4 at a paragraph boundary; label 'i»cc ti o pM' at the §4/§5 sentence boundary; synopsis-head marginal date '31 nor«nbt«« 1817 XV1U.'.

### `bullarium-continuatio.volume-14.line-00059362.part-03.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label (Derogatio contrariorum) second line 'trarionum.' fused inside 'felicis re- | ... cordationis' at the start of §5 (page 2, column 1, lower-middle).
- Non-blocking: Page 1: Running head 'U% / ●Pilla PP. Septimus'' interrupts 'susientandara | ti suppeditandnm' (column 1, lower, §2); signature 'Bull. Rum. Tom. XIV F. 108-' (column 2, lower, §2); marginal date '1817>' / 'in*00* xv,1,' within the historical synopsis heading (not a body sentence); unidentified fragment 'T#a<w' inside 'exponen- tes' (column 2, foot).
- Non-blocking: Page 2: Running head 'lBnl D6* / Bullarium Romanutn' splits 'pie- | narios' (column 1, lower-middle, §4).

### `bullarium-continuatio.volume-14.line-00078623.part-02.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal date/expedition notes 'Dal. £» / 19 dccrmbrù 1817 / ●uno XVIJL / Expdiitiò'pre cuoi.' fused into 'infra indui- | gcre' (page 1, column 1, lower, §1).
- Blocking: Marginal label second line 'iranornm.' (contrariorum) fused inside 'felici» re - | ... cordationis' (column 2, §3).
- Non-blocking: Page 1: Running head '378 / Bullarium Romanurn' at the same §1 join.

### `bullarium-continuatio.volume-14.line-00080476.part-02.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label second line 'tn.rioru«i.' (Derogatio contrariorum) fused mid-sentence between 'Non obstantibus qoibusvis' and 'etiam in synodalibus' (page 2, upper-middle, §6).
- Non-blocking: Page 1: Signature and running head 'tir//. Rom. Tom. XIV . F. 4H / Septimus' split 'diver- | sitate' (column 1, lower, §2); running head '594, Bullarium Komanum' splits 'Eugu- | bino' (column 2, lower, §4); marginal date lines at the synopsis head; unidentified fragments 'Wrwi,MI', 'Uu et aecre-' (column 2).

### `bullarium-continuatio.volume-14.line-00080476.part-03.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label 'Tcnor conce*,' (Tenor concessionis) fused inside 'prae- | fatos' (page 1, column 1, lower, §2).
- Non-blocking: Page 1: Running head ': Piu* PP, SeptiniiM ;S95' splits 'interdi- | oli' (column 1, §2); marginal date 'anno xviu.' within the synopsis heading; fragment 'irafiutHtB.' beside 'COllSt'ltU- ... tionlbus' after the Derogatio label (column 2, §3).

### `bullarium-continuatio.volume-14.line-00080476.part-04.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label 'Dr»«..;ocW' (Derogatio, as at the corresponding §-start in sibling acts) fused inside '.constitu ... tiopibus' (page 2, single column, middle, §6).
- Non-blocking: Page 1: Running head '73* / ● 596 / Buliarium Romanum' interrupts the quoted rescript (column 1, lower, §2); unidentified fragments 'apoiioi»*».' inside 'referen- | te' and 'pn.0 ci.c- r.' inside 'spe- | cialibus' (column 2).

### `bullarium-continuatio.volume-18.line-00005460.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Tenor-type marginal label 'venor eo^' fused inside 'animoM- | ... rum profectum' (animarum) at §2 'Nos igitur, ne quid de animarum profectum' (page 1, column 1, lower-middle). Missed as unidentified in the first pass.
- Non-blocking: Page 1: Running head '24 / fiullarium R«manum' (column 1, §2); fragment 'p„.' inside 'di- | lectus' (§1).

### `bullarium-continuatio.volume-18.line-00007598.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Tenor-type marginal label 'Tn»r «n».' fused inside 'fra- | ... ter' (page 1, column 1, foot, §2).
- Blocking: Expositio-type label 'KipMiu»' fused mid-sentence 'haud ita KipMiu» pridem curasti' (page 1, column 1, top, §1); same label as 'KipiMiuo' blocked in line-00015042. Missed in the first pass.
- Non-blocking: Page 1: Running head '10 / 58 / finilarlam Rotnanum' (column 1 foot); fragment 'u«<a. «t' inside 'man- | damus' (column 2, §3).

### `bullarium-continuatio.volume-18.line-00009091.part-01.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Tenor-type marginal label 'tnor ««●.' fused inside 'exponens | ... libus' (page 1, column 1, lower, §3).
- Non-blocking: Page 1: Fragment 'g»p* 4 iu, pr*.' inside the §2 sentence; running head '1 / Builariaoi Romanum' at the §4/dating boundary.

### `bullarium-continuatio.volume-18.line-00009091.part-03.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Clausula/decretum-irritans label fragment 'lu* irriun*.' fused mid-sentence 'efficaces existere, lu* irriun*. ac fore' (page 2, column 1, lower-middle, §5).
- Non-blocking: Page 1: Probable Proemium label fragment 'p,e«a»iim' inside §1 'voti» ... eo libentius' (borderline); running head 'Pius PP. Octavus' / «49'; signature 'BuU. Rotn. Tom. XYI//.' at §3/§4; fragments 'FTioirr', 'mwimi».', 'Bueotes'.
- Non-blocking: Page 2: Running head '13 / 60 / Bullarium Romanum / ^ clM 60' (column 1, §5); fragments 'iUJs', 'r. apecUt»'.

### `bullarium-continuatio.volume-18.line-00010152.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Clausula-type marginal label 'ciiuiuUia.' fused mid-sentence 'Decernentes quoque easdem ciiuiuUia. praesentes' with continuation 'MfiBoi**' inside 'validus ... et efficaces' (page 2, column 2, middle, §6) (judgment: probable Clausula).
- Non-blocking: Page 1: Running head 'i / Pius PP* Octavus / 55' (column 1, §1); label '«»»● diMr **®*I“®' at a §-start with continuation 'bolfo Somp*' inside 'coeno- | bium' (unrecognizable); fragment 'Dwurniar' inside §2.
- Non-blocking: Page 2: Running head '56 / Bullariam Romanum' (column 1, §3); fragment 'tMisViiurT*' inside 'unaqua- | que'; label 'usIwMfM' at §7 start.

### `bullarium-continuatio.volume-18.line-00010476.part-03.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Probable Derogatio-type marginal label '»«r«raiio' fused mid-sentence 'Non obstantibus Nostra , ot »«r«raiio cancellariae apostolicae regula' (page 2, single column, top, §4) (judgment: probable).
- Non-blocking: Page 1: Two-glyph fragment '*■' inside 'omnipotentis Dei' (§3).

### `bullarium-continuatio.volume-18.line-00011084.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label fragment 'E>p<iiuiopr«-' (Expositio) fused into 'Nobis curavit ... dileclus filius' (page 1, column 1, §1).
- Blocking: Four non-running-head marginal lines 'T«Mr «OAMI- ●Mi- / De re (Illo welrerleran.' together with running head 'Pius PP. Octavas / 61' interrupt 'supplici cum prece | a Nobis petiiU' (column 1, middle, §1).

### `bullarium-continuatio.volume-18.line-00012995.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Distributio-type marginal label 'Di*iriktu«' fused mid-sentence 'quinque nosocomiorum Di*iriktu« modo dictorum' (page 2, column 2, lower, §6) (judgment: probable).
- Non-blocking: Page 1: Running head '19 / 74 / Bullarkim Romanum' interrupts 'di&ndi.at* * | ●que' (column 1, lower, §1); unidentified fragments 'quikuiei«gi»^' inside 'consti- tuta', 'n«i ● u».'.
- Non-blocking: Page 2: Running head 'Pius PP. OctaTus / 75'; fragments '■●lowfniiolf^', 'y rn rtn fuiu', 'Dilati.', 'c«««r*', ''^***'*^"""'.
- Non-blocking: Page 3: Running head '^G / Bullarium Romanum' at the §6/§7 boundary; unidentified fragment 'mmr^iVsr ... niMrarnnMr*'.
- Non-blocking: Page 4: Running head 'PIns PP. Octavus / 77' splits 'quae« | sUonet' (column 1, §9).

### `bullarium-continuatio.volume-18.line-00013651.part-01.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Proemium-type marginal label 'prtTcmOi*' (first line 'i»eprMiiaD- j. |,') fused inside 'La- | ... tio' at §1 (page 1, column 1, top) (judgment: probable, cf. 'Promiim' in line-00013651.part-02).
- Blocking: Derogatio-contrariorum-type label 'Bafr,ou«' / '«Miiriortua' fused inside 'man- | ... damus' and 'Beoe- | ... [dicti]' at §6 Non obstantibus (page 2, single column, middle) (judgment: probable).
- Non-blocking: Page 1: Running head 'Pius PP. Octavus / 79'; fragments 'iidMiiadinsf', 'piUdrMMii', '«ontiTep.', '*'●● *"'**●'.
- Non-blocking: Page 2: Fragment '^ — ■' inside 'perpen- | sis' (§5).

### `bullarium-continuatio.volume-18.line-00013651.part-02.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Tenor-type marginal label 'Tm»r «m.' fused mid-sentence 'qui pubblicao Tm»r «m. charilalis instituta' (page 1, column 1, lower, §2).
- Blocking: Proemium label 'Promiim' fused mid-sentence 'eropportunum sane atqua Promiim perutile' (page 1, column 1, top, §1). Missed in the first pass.
- Non-blocking: Page 1: Running head '80 / Bnllarram Romanum' at the column break (§2); fragments ''^*"""', 'salu-**”*^**'.

### `bullarium-continuatio.volume-18.line-00014020.part-03.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label 'Clia»u4,« MldUna , ●! IrritutM.' (Clausula ... irritans) fused into 'in virlii dol- | la semplicc Nostra soUoscnziooe' (page 2, column 2, lower-middle, §19).
- Non-blocking: Page 1: Running head 'i / t / Pius PP. Octavus / 8 ^' splits 'qual- | cuiiu' (column 2, lower, §8); unidentified fragments '?iVhuj»Vi-', 'Rteapu', '4’^'.
- Non-blocking: Page 2: Running head 'S4 / Bullarlum Romanum' at the same join.

### `bullarium-continuatio.volume-18.line-00014591.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label fragment 'EipoMitt' (Expositio) fused mid-sentence 'nuper fuit EipoMitt nomipe carissimi' (page 1, column 1, §1).
- Non-blocking: Page 1: Running head 'Pius PP. OclaTua / 85' splits 'ab | eo depultiKlis' (column 2, §1).
- Non-blocking: Page 2: Printer's signature 'BvH. Rovt. Tom. IVI/I.' interrupts 'debere, Ii | ac irritum' (middle, §3).

### `bullarium-continuatio.volume-18.line-00014946.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label 'Eipcsitiop».' (Expositio) fused inside 'Valen- ... tiae' (page 1, column 1, §1).
- Blocking: Marginal-summary label 'D 'raciiio ijgQyi. / caiilr«iiorua . .' (Derogatio contrariorum) fused inside 'aposloli- | ... ets literis' (column 2, §3).
- Non-blocking: Page 1: Running head 'Pius PP. Octavus / 87' interrupts 'indulgentia | ac venia' (column 1, §1).

### `bullarium-continuatio.volume-18.line-00015042.provider-marks-omitted-v2` - CHANGES_REQUIRED

- Prior provider-mark defect: absent - no 'Digitized by Google'-type mark or damaged variant visible on any page.
- Blocking: Marginal-summary label fragment 'KipiMiuo' (Expositio, same formula position as in line-00014591) fused mid-sentence 'nuper est KipiMiuo nomine' (page 1, column 1, §1).
- Non-blocking: Page 1: Running head '88 / BullaiHum Romanum' splits 'ucclc- | ftiasticis' (column 2, §3).

## First-issue findings retained

Each first-issue page finding, verbatim, with its re-issue status.

| Source ID | Page | First-issue finding | Final status |
| --- | --- | --- | --- |
| `bullarium-continuatio.volume-18.line-00002188.part-02.provider-marks-omitted-v2` | 1 | Residual damaged modern provider mark: page 1, column 2, lower-middle, standalone line 'Digilizcxj i';' followed by '\' and 'Pius PP.' running-head furniture, interrupting the body sentence 'praeeminentia / gaudere debeas' in §5. Prior provider-mark defect is not fully absent. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00002188.part-02.provider-marks-omitted-v2` | 2 | Volume running head '4 / Bullarium Romanum / •m' at page 2, column 2, middle, interrupts the body word 'thesaura- / rk) gonorali' (thesaurario generali) in §8. | qualification on this page |
| `bullarium-continuatio.volume-14.line-00045176.part-04.provider-marks-omitted-v2` | 1 | Volume running head/page furniture '43* / 340 / Bullarfum Romanum' at page 1, column 1, lower, interrupts the body sentence 'si qua» forte incurrerint hujus / tantum rei grafia absolventes' (§2). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00049746.provider-marks-omitted-v2` | 1 | Running head '335 / Pius PP. Septimu»' at page 1, column 1, middle, splits the word 'supplica- / ri fecerunt' in §2. No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00049754.part-03.provider-marks-omitted-v2` | 1 | Running head '562 / Bulìarium Romamira' at page 1, column 2, middle, interrupts the sanctio sentence 'eique ausu 40 / temerario cóntraire' (§6). | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00049754.part-03.provider-marks-omitted-v2` | 1 | Printer's signature 'Bull. Rorn. Tom. XIV I. 106.' fused at end of column 1 §2 sentence before 'u visum fuit' (page 1, column 1, middle). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00050183.part-01.provider-marks-omitted-v2` | 1 | Running head 'Pius PP. Septimus 363' at page 1, column 2, middle, splits 'in li- / teras' mid-sentence. No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-14.line-00050183.part-01.provider-marks-omitted-v2` | 2 | Printer's signature '...Jr™ tcros cardinale* Bull. Iiom. / Tom. XIV. F. 106.' at page 2, single column, middle, interrupts 'S.R. E. presby* / teros cardinales'. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00050183.part-01.provider-marks-omitted-v2` | 2 | Marginal fragments 'Nomina rmi- nenliuimo-' and 'uenliMimo- . , . r» i-' interleaved into 'Auctoritate omnipotentis Dei, ... [beato]rum apostolorum' (page 2, middle). | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00050617.part-01.provider-marks-omitted-v2` | 1 | Running head 'BuIlarium Romanum / 3C(>' at page 1, column 1, lower, interrupts 'christiauissimi religio, et / pietas'. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00050617.part-01.provider-marks-omitted-v2` | 1 | Historical footnote '(4) Kp. ad Pulcher. Aug. xlix. <2 ) i\ahum± 3. 2.' set mid-sentence at page 1, column 2, middle, between 'ut nonni -' and 'si ex longa'. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00050617.part-01.provider-marks-omitted-v2` | 2 | Running head 'Bullariura Ròraanum / 3SS' at page 2, column 2, lower, splits 'iis dioece- / sihus unicntnr' (Art. XI). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-14.line-00050617.part-01.provider-marks-omitted-v2` | 3 | Running head 'Pius PP. Septìmus 3GJT' at page 3, column 2, top, interrupts '... quaesito non lollendo , / ac conventione die! xv.' (§6). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-14.line-00052913.part-03.provider-marks-omitted-v2` | 2 | Printer's signature and running head 'Bull. J torri. Tom. XI V. F. 108. / Ài / 58G / Bullarium Romannm' at page 2, column 2, top, split 'auctorita- / te apostolica' (§6). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00053407.part-02.provider-marks-omitted-v2` | 1 | Printer's signature and running head 'Bull. llcm. Tom. F. XIV. 106 / Septimus 38T' at page 1, column 1, lower, split 'protrahe- / re' (§1). | qualification on this page |
| `bullarium-continuatio.volume-14.line-00053407.part-02.provider-marks-omitted-v2` | 1 | Running head '49* / Bullarium Romammt / 3SS' at page 1, column 2, middle, interrupts 'omnia bona, reddilus, ac / proventus' (§2). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-14.line-00059362.part-03.provider-marks-omitted-v2` | 1 | Running head 'U% / ●Pilla PP. Septimus'' at page 1, column 1, lower, interrupts 'necessarium ad vitam susientandara / ti suppeditandnm est' (§2). | qualification on this page |
| `bullarium-continuatio.volume-14.line-00059362.part-03.provider-marks-omitted-v2` | 1 | Printer's signature 'Bull. Rum. Tom. XIV F. 108-' fused at page 1, column 2, lower, inside 'et Bull. ... / unam cantatam' (§2). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-14.line-00059362.part-03.provider-marks-omitted-v2` | 2 | Running head 'lBnl D6* / Bullarium Romanutn' at page 2, column 1, lower-middle, splits 'suosque pie- / narios' (§4). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00078623.part-02.provider-marks-omitted-v2` | 1 | Marginal date/expedition notes and running head 'Dal. £» / 19 dccrmbrù 1817 / ●uno XVIJL / Expdiitiò'pre cuoi. / 378 / Bullarium Romanurn' at page 1, column 1, lower, split 'infra indui- / gcre de benignitate' (§1). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00080476.part-02.provider-marks-omitted-v2` | 1 | Printer's signature and running head 'tir//. Rom. Tom. XIV . F. 4H / Septimus' at page 1, column 1, lower, split 'regiminis diver- / sitate' (§2). | qualification on this page |
| `bullarium-continuatio.volume-14.line-00080476.part-02.provider-marks-omitted-v2` | 1 | Running head '594, Bullarium Komanum' at page 1, column 2, lower, splits 'episcopo Eugu- / bino solvere' (§4). No modern provider mark (prior 'jOOgle' literal) remains. | qualification on this page |
| `bullarium-continuatio.volume-14.line-00080476.part-03.provider-marks-omitted-v2` | 1 | Running head ': Piu* PP, SeptiniiM ;S95' at page 1, column 1, lower-middle, splits 'interdi- / oli' (interdicti) in §2. No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-14.line-00080476.part-04.provider-marks-omitted-v2` | 1 | Running head '73* / ● 596 / Buliarium Romanum' at page 1, column 1, lower, interrupts the quoted rescript 'precibus « oratorum sequentem in modum / « rescripsit' (§2). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-18.line-00005460.provider-marks-omitted-v2` | 1 | Running head '24 / fiullarium R«manum' at page 1, column 1, lower-middle, interrupts 'religionis, pietalisqoe **"^*"'*' / augmenlum deficiat' (§2). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00007598.provider-marks-omitted-v2` | 1 | Running head '10 / 58 / finilarlam Rotnanum' at page 1, column 1, bottom, splits 'quum- / que anituadverleris' across the column break (§2). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00009091.part-03.provider-marks-omitted-v2` | 1 | Running head 'Pius PP. Octavus' / «49' at page 1, column 1, middle, interrupts 'aliorumque ofiicialium / numero, eorumque' (§2). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-18.line-00009091.part-03.provider-marks-omitted-v2` | 2 | Running head '13 / 60 / Bullarium Romanum / ^ clM 60' at page 2, column 1, middle, splits 'integros effe- / ... Tliria ct oblinere' (§5). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00010152.provider-marks-omitted-v2` | 1 | Running head 'i / Pius PP* Octavus / 55' at page 1, column 1, lower, interrupts 'non «dhuc ad finem omoinQ / perductam' (§1). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-18.line-00010152.provider-marks-omitted-v2` | 2 | Running head '56 / Bullariam Romanum' at page 2, column 1, lower, splits 'io unaqua- tMisViiurT*' / que harum' (§3). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00010476.part-03.provider-marks-omitted-v2` | 1 | Running head '15 / 58 / Bullarium Romanum' at page 1, column 1, middle, interrupts 'atque in earum pia do- / ITIO vetutfls ac viduas excipere' (§2). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-18.line-00011084.provider-marks-omitted-v2` | 1 | Running head and marginal summary 'Pius PP. Octavas / 61 / T«Mr «OAMI- ●Mi- / De re (Illo welrerleran.' at page 1, column 1, middle, interrupt 'Hinc supplici cum prece / a Nobis petiiU' (§1). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00012995.provider-marks-omitted-v2` | 1 | Running head '19 / 74 / Bullarkim Romanum' at page 1, column 1, lower, interrupts 'ea latius di&ndi.at* * / ●que m aliag quoque civitates propagari' (§1). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-18.line-00012995.provider-marks-omitted-v2` | 2 | Running head 'Pius PP. OctaTus / 75' at page 2, column 1, lower-middle, splits 'oculos auffiuraque / coDTertimus' (§4). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00012995.provider-marks-omitted-v2` | 4 | Running head 'PIns PP. Octavus / 77' at page 4, column 1, upper-middle, splits 'Si quae exorientur quae« / sUonet' (quaestiones) in §9. No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-18.line-00013651.part-01.provider-marks-omitted-v2` | 1 | Running head 'Pius PP. Octavus / 79' at page 1, column 2, lower, splits 'mensae episcopali certo io- / cumb^rot' (§4). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00013651.part-02.provider-marks-omitted-v2` | 1 | Running head '80 / Bnllarram Romanum' at page 1, column 1 foot / column 2 top, interrupts 'poenis quovis / modo' (§2). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00014020.part-03.provider-marks-omitted-v2` | 1 | Running head 'i / t / Pius PP. Octavus / 8 ^' at page 1, column 2, lower, splits 'ed essendo qual- / cuiiu det giudici' (§8). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-18.line-00014020.part-03.provider-marks-omitted-v2` | 2 | Marginal fragment and running head 'Clia»u4,« MldUna , ●! IrritutM. / S4 / Bullarlum Romanum' at page 2, column 2, lower-middle, interrupt 'in virlii dol- / la semplicc Nostra soUoscnziooe' (§19). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00014591.provider-marks-omitted-v2` | 1 | Running head 'Pius PP. OclaTua / 85' at page 1, column 2, lower-middle, splits 'sive aliis ab / eo depultiKlis' (§1). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00014591.provider-marks-omitted-v2` | 2 | Printer's signature 'BvH. Rovt. Tom. IVI/I.' at page 2, single column, middle, interrupts 'definiri debere, Ii / ac irritum el inane' (§3). No modern provider mark remains. | qualification on this page |
| `bullarium-continuatio.volume-18.line-00014946.provider-marks-omitted-v2` | 1 | Running head 'Pius PP. Octavus / 87' at page 1, column 1, lower-middle, interrupts 'cx Nostra indulgentia / ac venia' (§1). No modern provider mark remains. | page CHANGES_REQUIRED |
| `bullarium-continuatio.volume-18.line-00015042.provider-marks-omitted-v2` | 1 | Running head '88 / BullaiHum Romanum' at page 1, column 2, middle, splits 'in legitimis ucclc- / ftiasticis tribunalibuf' (§3). No modern provider mark remains. | page CHANGES_REQUIRED |

## Qualifications

- Sparse final pages all carry genuine source dating clauses (and in one case a subscription) before the project apparatus; none is apparatus-only.
- The Italian chirograph `bullarium-continuatio.volume-18.line-00014020.part-03.provider-marks-omitted-v2` is labelled Italian, matching its `it` metadata.
- Title lines and issuer headers reproduce literal OCR noise from the frozen metadata; they match it and are limitations, not defects. Marginal dates within the historical synopsis heading (not a body sentence) are qualified.

## Limitations

- Uncorrected, uncollated historical OCR; literal spellings, abbreviations, title/issuer noise and unidentified short glyph fragments are retained and not judged.
- Historical running heads, folios, 'Bullarium Romanum' + page number, 'Pius PP.' heads and printer signatures are retained as qualified OCR furniture, including where they fall mid-sentence or inside a hyphen split (continuation-series standard).
- Layout and visual review only; no word-level collation, historical authentication, publication, installation or deployment claim.
- Act date unresolved in frozen metadata for all but one document; no date was inferred or repaired.

## Individual page evidence

| Source ID | Page | PNG SHA-256 | Final status | Observation (re-verification where present, else first pass) |
| --- | --- | --- | --- | --- |
| `bullarium-continuatio.volume-18.line-00002188.part-02.provider-marks-omitted-v2` | 1 | `dcd93efdb5528333d77cccf5dca358c4e4fe1f075bc161be0e69f7ffc1193378` | CHANGES_REQUIRED | Title, Pius PP. VIII., 1829-04-07, Latin match metadata. Two columns clean. Column 2 retains damaged digitizer residue 'Digilizcxj i';' plus '\' and 'Pius PP.' between 'praeeminentia' and 'gaudere debeas'. |
| `bullarium-continuatio.volume-18.line-00002188.part-02.provider-marks-omitted-v2` | 2 | `383f4cec2cc75eb61c78687f9caff0cf1456670d4eea84a44dbca0a01f249125` | PASS | Two columns, no clipping. Column 1 'Octavus 5' running-head residue sits at a paragraph boundary before §7 (nonblocking). Column 2 'Bullarium Romanum' head interrupts a word mid-sentence. No provider mark. |
| `bullarium-continuatio.volume-18.line-00002188.part-02.provider-marks-omitted-v2` | 3 | `d88ef75c1f610b62d84af87f4489ff6dd2341bd9deaba045303333a98360f9fa` | PASS | Single-column continuation through §§10-12 and dating clause 'Datum Romae ... anno primo', then source/rights apparatus. Natural source closing; no provider mark. |
| `bullarium-continuatio.volume-14.line-00045176.part-04.provider-marks-omitted-v2` | 1 | `03d489a9d1e900205f45d1102ff325e3d1a740fc6570de28b5eca8cfc7486dca` | CHANGES_REQUIRED | Re-viewed at full size. Title, Pius PP. VII., Latin match. Derogatio label fused mid-word in column 2. No provider mark. |
| `bullarium-continuatio.volume-14.line-00045176.part-04.provider-marks-omitted-v2` | 2 | `e8afe9d24a7cb65fb33c71d12153a041799959980bfcc9ae1d56fac780903bca` | PASS | Re-viewed. End of derogation clause and dating 'Datum Komae ... anno decimo octavo' then apparatus. No marginal label or provider mark. |
| `bullarium-continuatio.volume-14.line-00049746.provider-marks-omitted-v2` | 1 | `0997321a2eb981c17f32b143a7aee7eb654600fe99019254e59bbc7502e61495` | CHANGES_REQUIRED | Re-viewed at full size. Title, Pius PP. VII., Latin match. Marginal labels fused into body words in §§2-3. No provider mark. |
| `bullarium-continuatio.volume-14.line-00049754.part-03.provider-marks-omitted-v2` | 1 | `613bdbb01218d3400781bd4a7a69283f6b9b3e02509cc2723a1ea0058bc35422` | CHANGES_REQUIRED | Re-opened at full size. Title, issuer, Latin match. Derogatio label clearly fused mid-sentence in §5. No provider mark. |
| `bullarium-continuatio.volume-14.line-00050183.part-01.provider-marks-omitted-v2` | 1 | `501a3130946da60c79010fe3bff781b488a4d7b8951fffd50913fde17764ea45` | PASS | Title, Pius PP. VII., no date, Latin match. Two clean columns of allocution. No digitizer mark; running head interrupts body word. |
| `bullarium-continuatio.volume-14.line-00050183.part-01.provider-marks-omitted-v2` | 2 | `032cf94f907fc2d5a6a8f8e27ef3d1e9c6d509809051ae9109d0e442a7ba4e8f` | CHANGES_REQUIRED | Single-column ending with creation formula and 'In Nomine Patris ... Amen.' then apparatus; genuine closing. No digitizer mark; signature/margin furniture interleaved. |
| `bullarium-continuatio.volume-14.line-00050617.part-01.provider-marks-omitted-v2` | 1 | `c9ac7221095acf8ee1ac8c2e403a9c8222c15d2e3778ef04b331277bf250b8b9` | CHANGES_REQUIRED | Title, 'Pius episcopus Servus Servorum Dei', no date, Latin match. Two clean columns. No modern provider mark. |
| `bullarium-continuatio.volume-14.line-00050617.part-01.provider-marks-omitted-v2` | 2 | `a0fee6805354bfb24c9c2f1f1b3ab2a2dcc4d583d76b1bc0f311157aefcb262d` | PASS | Concordat articles I-XIII in two clean columns. Stray '36/' page number atop column 2 and 'Pius PP. Septimi»' before ARTICULUS I fall at heading boundaries (nonblocking). No digitizer mark. |
| `bullarium-continuatio.volume-14.line-00050617.part-01.provider-marks-omitted-v2` | 3 | `4a7d343f771b34278a858e0962b8afdb767dd6df0ca845f13346badd932ac5da` | PASS | Art. XIV, Actum clause, signatures, §§3-7, sanctio and dating clause 'Datum ... anno decimo oclavo' then apparatus. Natural closing; no digitizer mark. |
| `bullarium-continuatio.volume-14.line-00052913.part-03.provider-marks-omitted-v2` | 1 | `bb5601ac8c029440dfde856d4bbbe1e50f55d39db9658f2e89cc40b8690588db` | PASS | Re-opened. Page alone carries no recognizable fused label; continuation glyphs recorded as qualifications. |
| `bullarium-continuatio.volume-14.line-00052913.part-03.provider-marks-omitted-v2` | 2 | `15c4a9962cf1f5723b9ccd6dc65218ceac83b9176c2ed60d9109a6f34f4de5e2` | CHANGES_REQUIRED | Re-opened at full size. Marginal block splits two body words in §7. |
| `bullarium-continuatio.volume-14.line-00052913.part-03.provider-marks-omitted-v2` | 3 | `5a2cbc4defcd146f3e237767c3ae690ba6641771fc548e3c1177f7db15ff6297` | PASS | Re-opened. Dating clause and apparatus only; nothing fused. |
| `bullarium-continuatio.volume-14.line-00053407.part-02.provider-marks-omitted-v2` | 1 | `df8b69523b19a14cc3f5dd1114d007b7bceb13c7c7b7d16a796a4ee929967ff7` | PASS | Re-opened. No recognizable label text fused; fragments recorded as OCR-noise qualifications. |
| `bullarium-continuatio.volume-14.line-00053407.part-02.provider-marks-omitted-v2` | 2 | `5006317433d71e38aad9f87e531c8b2ffdaf709e14fd9f348cce03d2aa92cf7d` | CHANGES_REQUIRED | Re-opened at full size. Recognizable 'de[cretum] irri[tans]' label continuation splits body words. |
| `bullarium-continuatio.volume-14.line-00059193.provider-marks-omitted-v2` | 1 | `2bd0c6000935a3cfd951535fee8c382faeb9738f43aa69cc005cdd25bbe89bc6` | CHANGES_REQUIRED | Re-opened at full size. Tenor-type label block splits 'tuisque'. |
| `bullarium-continuatio.volume-14.line-00059193.provider-marks-omitted-v2` | 2 | `270b2776a5de82174bed21ed8a2ed549795168949a56a4a2951ad07d4acaf281` | PASS | Re-opened. End of sanctio and dating clause then apparatus; nothing fused. |
| `bullarium-continuatio.volume-14.line-00059362.part-03.provider-marks-omitted-v2` | 1 | `9dc93b1a72ae6296450b31197a8a330f78cf2d22c47bbf255cfeeeccf2e078a1` | PASS | Title, 'Pius PP, VIL', no date, Latin match. Two clean columns. No digitizer mark; running-head and signature furniture interrupt body sentences. |
| `bullarium-continuatio.volume-14.line-00059362.part-03.provider-marks-omitted-v2` | 2 | `bf917ce9d1bd131a6b560f9df15c94f438b10559ad4d551fecaf522765f53bfd` | CHANGES_REQUIRED | §§3-5 and dating clause 'Datomi noiuae ... anno decimo octavo' then apparatus continuing into column 2. Natural closing; running head splits a body word. |
| `bullarium-continuatio.volume-14.line-00078623.part-02.provider-marks-omitted-v2` | 1 | `143bd2e3274080034b38bc2cfece88544ec57abaf99c9b5de8ad704ebcf2ed04` | CHANGES_REQUIRED | Title, 'pìus pp. vn.', no date, Latin match. Two columns; dating clause 'Datemi ltoniac ... anno de- cimo orlavo' then apparatus. Genuine closing; no digitizer mark; furniture interrupts a body word. |
| `bullarium-continuatio.volume-14.line-00080476.part-02.provider-marks-omitted-v2` | 1 | `aaf8084703f7b3fbcead977e2118255516cb208e0a2ef15fa234c7846745757e` | PASS | Title, 'Pius episcopus Scrvus servorum Dei', no date, Latin match. Two clean columns. No digitizer residue; two page-break joins carry running-head/signature furniture inside words. |
| `bullarium-continuatio.volume-14.line-00080476.part-02.provider-marks-omitted-v2` | 2 | `d9050ff452fccb58800bc1d169c3dd9a7b413bb5439a9fcc72062e06d9ef6783` | CHANGES_REQUIRED | Single-column ending: §§5-7, sanctio and dating clause 'Datum Ro- mae ... anno decimo octavo' then apparatus. Genuine closing; no provider mark. |
| `bullarium-continuatio.volume-14.line-00080476.part-03.provider-marks-omitted-v2` | 1 | `48dd1e2b858613ae7c5a859f99bdc22fa2781d60177d4a2699f96de98443cba3` | CHANGES_REQUIRED | Title, Pius PP. VII., no date, Latin match. Two columns; dating clause 'Dalum Romae ... anno decimo octavo' then apparatus. Genuine closing; no digitizer mark; running head splits a body word. |
| `bullarium-continuatio.volume-14.line-00080476.part-04.provider-marks-omitted-v2` | 1 | `d67b6b5080616737fa3d4aaf6a5e4d09396c3c47b845ae7c10a0f555dce9cfa2` | PASS | Title, 'Pius PP. vn.', no date, Latin match. Two clean columns with quoted rescripts. No digitizer mark; running head interrupts a body sentence. |
| `bullarium-continuatio.volume-14.line-00080476.part-04.provider-marks-omitted-v2` | 2 | `92b57bead209357b0264a5fbaaca352d7e240b3965bf9f1c31343cec9d373dc6` | CHANGES_REQUIRED | Single-column §§5-6 and dating clause 'liatum Roma* ... anno decimo octavo' then apparatus. Genuine closing; no provider mark. |
| `bullarium-continuatio.volume-18.line-00005460.provider-marks-omitted-v2` | 1 | `1f0cc520518ee27fd5b96644a50f683dc1b65206e7332d6a5e434473730f8527` | CHANGES_REQUIRED | Re-opened at full size during re-verification of the Tenor pattern. |
| `bullarium-continuatio.volume-18.line-00007598.provider-marks-omitted-v2` | 1 | `92e89fd318534dbe06b2b7562de1f5f419687af9e9fd6ca8c3b7c72ae263a967` | CHANGES_REQUIRED | Re-opened at full size for the named fragment. |
| `bullarium-continuatio.volume-18.line-00007598.provider-marks-omitted-v2` | 2 | `8d7bfeaa2d1cfe79d23f9c850f04e8a32426dfa4883c53eb69eb057d3c163552` | PASS | Single-column end of §3, §4 and dating clause 'Datum Romae ... anno primo' then apparatus. Genuine closing; no provider mark. |
| `bullarium-continuatio.volume-18.line-00009091.part-01.provider-marks-omitted-v2` | 1 | `72a24aa389ba0821d3e2b873a0e21acba90b9b084cec59713919bc2889cfe200` | CHANGES_REQUIRED | Re-opened at full size for the named fragment. |
| `bullarium-continuatio.volume-18.line-00009091.part-03.provider-marks-omitted-v2` | 1 | `fc60d0e3a48e5205b999bb1508497ce762c391fa7e31de04ecc23e2ccbb7e530` | PASS | Re-opened at full size. |
| `bullarium-continuatio.volume-18.line-00009091.part-03.provider-marks-omitted-v2` | 2 | `3e97a3bb8abe276e7d2c256a5cdf4892301fea2d60612839756fc2cd23aee79f` | CHANGES_REQUIRED | Re-opened at full size. |
| `bullarium-continuatio.volume-18.line-00010152.provider-marks-omitted-v2` | 1 | `0cd198daea99311fb48e7323dbc0e1eeed00da89c057954977cfc8014825900a` | PASS | Re-opened at full size. |
| `bullarium-continuatio.volume-18.line-00010152.provider-marks-omitted-v2` | 2 | `fc4faa0d1d73f7831a743327f4a616f2833e77a59b6d5bddb6c52a2e0ed99c70` | CHANGES_REQUIRED | Re-opened at full size. |
| `bullarium-continuatio.volume-18.line-00010152.provider-marks-omitted-v2` | 3 | `1710dd3b38ca1ea4f5fb62d3014a79365cec911b9887ffa14f42fca58e093a44` | PASS | Re-opened. End of dating clause and apparatus. |
| `bullarium-continuatio.volume-18.line-00010476.part-03.provider-marks-omitted-v2` | 1 | `e4bf0b1354d69f4ebf6fb3bbc1d96b1fa0aa68b84fda400125bade26eacdbe11` | PASS | Viewed at full size earlier this session (image in context); no label text fused. |
| `bullarium-continuatio.volume-18.line-00010476.part-03.provider-marks-omitted-v2` | 2 | `b8915f5312d113717d95fa4a8d858678c3c6ea3a5c92adfba760af07a5c6886a` | CHANGES_REQUIRED | Re-opened at full size. |
| `bullarium-continuatio.volume-18.line-00011084.provider-marks-omitted-v2` | 1 | `389b4240764b7643aad34c5fe582228f908cdfc2bf9a6ed159ddf84dcfce54a1` | CHANGES_REQUIRED | Title, 'Pius PP.. VIII.', no date, Latin match. Two columns; dating clause 'Datum Romae ... anno primo' then apparatus. Genuine closing; furniture interrupts a body sentence. |
| `bullarium-continuatio.volume-18.line-00012995.provider-marks-omitted-v2` | 1 | `f6c1e97ae17d38f6f8186cc5893cd51f51304c9d0bf6e89525ef431914af60b0` | PASS | Title 'Ordinatio nosocomiorum urbis. mi. su', issuer ', » Pius PP. VIII. *', no date, Latin match frozen metadata (literal OCR noise). Two clean columns. No digitizer mark; running head interrupts a body sentence. |
| `bullarium-continuatio.volume-18.line-00012995.provider-marks-omitted-v2` | 2 | `7c46dd0270e04925053e07cb21a5a4915e456567955bdf37c0a6a1941d6b363d` | CHANGES_REQUIRED | Viewed at full size earlier this session (image in context). |
| `bullarium-continuatio.volume-18.line-00012995.provider-marks-omitted-v2` | 3 | `82c9854750ce027113d9ff6b4669530783eb19544da19e6ecbc76090dbaf489b` | PASS | §§6-9 in two clean columns. '^G / Bullarium Romanum' running head in column 1 falls between §6 ('constiluorunt.') and §7, a paragraph boundary (nonblocking). No modern provider mark. |
| `bullarium-continuatio.volume-18.line-00012995.provider-marks-omitted-v2` | 4 | `c763fd10ffd4085b486d41cdeb9cee689219c3397275ba8ec17cd5efc8c569ec` | PASS | End of §9, §10, derogation and dating clause 'Datum Romae ... anno primo' then apparatus (rights line in column 2). Genuine closing; running head splits a body word. |
| `bullarium-continuatio.volume-18.line-00013651.part-01.provider-marks-omitted-v2` | 1 | `5533033875ec26c007d988c022343dd4510c770360bd5a0fa0c82be1bb41cfeb` | CHANGES_REQUIRED | Viewed at full size earlier this session (image in context). |
| `bullarium-continuatio.volume-18.line-00013651.part-01.provider-marks-omitted-v2` | 2 | `d667cf210ac9586c8690fbd407d14bb8498073d2b1a5379835eacfe0b72f8371` | CHANGES_REQUIRED | Viewed at full size earlier this session (image in context). |
| `bullarium-continuatio.volume-18.line-00013651.part-02.provider-marks-omitted-v2` | 1 | `9a7ac7668e9a0f72e5fc4c340772420ca7f57d70cf89315b1f554245974fc233` | CHANGES_REQUIRED | Re-opened at full size for the named fragment. |
| `bullarium-continuatio.volume-18.line-00013651.part-02.provider-marks-omitted-v2` | 2 | `9ad9bcf61ea156ac8ea23eb7f734485d3c3d5fad2585f4b44ecce7661b81edc4` | PASS | Sparse final page: dating clause 'Datum Romae ... anno primo' then apparatus. Genuine source closing; no provider mark. |
| `bullarium-continuatio.volume-18.line-00014020.part-03.provider-marks-omitted-v2` | 1 | `6ef4a31eb5e48b7b1dbede570af8e14a661b6f4a8bf41f4fa12bdee9db0fdc9e` | PASS | Title, 'Pius pp. vin.', no date, Italian label matches language 'it'. Two clean columns of Italian chirograph. No digitizer mark; running head splits a body word. |
| `bullarium-continuatio.volume-18.line-00014020.part-03.provider-marks-omitted-v2` | 2 | `cbad221cdd06b64c00c185ec8085a2bfd76cb8c3bf837b0b60276ecced120424` | CHANGES_REQUIRED | Articles IV-XII, §§10-19 in two columns; roman-numeral article heads are source structure. No digitizer mark; furniture interrupts a body sentence. |
| `bullarium-continuatio.volume-18.line-00014020.part-03.provider-marks-omitted-v2` | 3 | `bf79fe7cbab3a405e33a35ceac0da14fb2aba4de641f5bf6175036cc17a12e6a` | PASS | Sparse final page: dating clause 'Dal Nostro palazzo apostolico Vati- cano ... 1830 ... anno primo' and subscription 'Pius FP, Ul,' then apparatus disclosing Italian chirograph. Genuine closing; no provider mark. |
| `bullarium-continuatio.volume-18.line-00014591.provider-marks-omitted-v2` | 1 | `a005f5243f48cd56a491e6f65199c34c98516cf8ea14a1d21c6ad75f0c110ec3` | CHANGES_REQUIRED | Title, 'Pios PP. VUl.', no date, Latin match (OCR title noise literal). Two clean columns. No digitizer mark; running head interrupts a body sentence. |
| `bullarium-continuatio.volume-18.line-00014591.provider-marks-omitted-v2` | 2 | `d1bdbc7d072247fde039f9b54bc13023591a28eb872648d3a5c42408ce3f1ecc` | PASS | End of §2, §§3-4 and dating clause 'Dstum Romae ... anno primo' then apparatus. Genuine closing; signature interrupts a body sentence. |
| `bullarium-continuatio.volume-18.line-00014946.provider-marks-omitted-v2` | 1 | `431db62ca7b6e620a5864f09050995b653ce21150490e681bb4ffb7e80b14470` | CHANGES_REQUIRED | Title, Pius PP. VIII., no date, Latin match (OCR title noise literal). Two columns; dating clause 'Datum Romae ... anno primo' then apparatus. Genuine closing; running head interrupts a body sentence. |
| `bullarium-continuatio.volume-18.line-00015042.provider-marks-omitted-v2` | 1 | `21b9764b09f282aef6fa6b4c1826d5531501eacb302e5fe6b7e64feeea15c9b1` | CHANGES_REQUIRED | Title, 'Pius PP. Octavus', no date, Latin match (OCR title noise literal). Two clean columns. No digitizer mark; running head splits a body word. |
| `bullarium-continuatio.volume-18.line-00015042.provider-marks-omitted-v2` | 2 | `5f0056bb9abaad41000dbb7b2a9d8fdff3234560b83c91506d0c9f22ab97636e` | PASS | Single-column §§4-5 and dating clause 'Datum Romae ... anno primo' then apparatus disclosing issuer from running title. Genuine closing; no provider mark. |
