# Bullarium Romanum vol. IV reading-order visual review 02 — lane 02

CHANGES_REQUIRED: 36 assigned PDFs, 67 pages individually opened at full raster size; 26 PASS, 10 CHANGES_REQUIRED. Zero reused pages. Marginal summaries seen as separate TAB-led blocks: 241; marginal-summary fusion into a body line or hyphen-split word: **none found**. The 10 CHANGES_REQUIRED readers all carry a different, page-foot defect: a historical footnote run into the body paragraph (usually inside a hyphen-split word) without a paragraph break.

## Scope and method

Lane `bullarium-ro-v04` / `lane-02`, assignment schema `triptych-claude-visual-assignment/v1`, assignment SHA-256 `dd706958646d604a4b01d1c1a205382a7f6ef24aa714a652b5b2bb29ec03846c`. These are the first coordinate-reconstructed readers of the Turin 1859 Bullarium Romanum vol. IV, from the whole-volume reading-order derivative `artifact.bullarium-romanum.volume-04.1859-turin-latin.reading-order-497a692a65d1` (hybrid.txt SHA-256 `497a692a65d1dfe838c88ebf7a748585889d2c3b9ba80be7e2cc38189b26982d`).

Every page PNG listed in `assignment.json` was opened individually with the Read tool (one image per call, 1700x2200 raster), and its observation was appended to `observations.jsonl` before later pages were opened. No new rasterization, contact sheet, source repair or text correction was done. On each page I checked title, issuer, language and the absence of a date against the frozen metadata; two-column order; marginal summaries; headings; glyphs; running heads, folios and signature marks; natural closing; and fragment notices. To confirm what I saw, read-only lane helpers listed the TAB-led marginal blocks of each unit's LF range and looked up word-map roles and bounding boxes (`.../replay/changed-word-map.jsonl.gz`, SHA-256 `710b55343b3aa8ed96c067898dd756a445b8fa6a0aba8d092c373a8ff10c4c82`, identical to the validation record's pin) for suspicious lines.

Standards applied, as instructed for this series: marginal-summary fusion is BLOCKING; running heads, folios and printer signature marks left inline are NON-BLOCKING qualifications and are recorded; marginal blocks that are separate but misplaced are qualifications, with their locus noted; fragments must show the fragment title and a clear missing-content notice. Historical notes that are not separately set (brief: "Separately set historical notes are acceptable") were treated as blocking. The coordinator may rule otherwise (see Findings).

## Evidence verification

All assigned PDFs, every page PNG, the receipt, the frozen manifest and the raster-run file were hashed before inspection (`verification-before.json`) and again after (`verification-after.json`). All 106 digests matched their assignment pins both times, and the before and after hashes are identical.

| Evidence | Path | SHA-256 | Verification |
| --- | --- | --- | --- |
| receipt | `.scratch/typeset_pipeline/claude/bullarium-ro-v04/receipt.json` | `c4b889a739db113dc22902e16a9b3756fff816d2fa9853a4e28e6aeffa166b1e` | Before and after: match |
| manifest | `.scratch/typeset_pipeline/claude/bullarium-ro-v04/frozen-manifest.json` | `8943af0675c465f58d2a8ce8885eabfe26e44c867cd0440d5580268933291a40` | Before and after: match |
| raster_run | `.scratch/claude-review/rasters-bullarium-ro-v04/review-run.json` | `ebefec8b707cfc0c378149b41b959340b0627fe316929c3552b898d3ffc1356a` | Before and after: match |
| verification-before.json | lane | `ecd358cba8f38357eac3f769f6121bbd67d9e56740975132f13493d6e2ed63a7` | all_match = True |
| verification-after.json | lane | `ecd358cba8f38357eac3f769f6121bbd67d9e56740975132f13493d6e2ed63a7` | all_match = True |
| observations.jsonl | lane | `03ba006ab8d3bc712ad837954806b1b776fac48277c5d3241700600ad4b75e7e` | 67 unique page observations |

## PDF outcomes

| Source ID | Pages | Marginal blocks | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- |
| `unit-0133.reading-order` | 2 | 7 | `a9809780f0bec3fd7bd15398b348b975102744f2a90de37d584b8d44c6d0d1e6` | PASS |
| `unit-0134.reading-order` | 1 | 2 | `2c8ab583c02325472ea5d15a35020defa50808685141081593af0e74d27fbea9` | PASS |
| `unit-0140.reading-order` | 3 | 9 | `02b8469c7b2b1e3ec722c0aa26ae119641c54d59d0061f179a2dc1705229ce63` | PASS |
| `unit-0144.reading-order` | 3 | 10 | `02204873dd156b721e7662577c3d3d638c09e07fd03fdbf936c27eb625f4964c` | CHANGES_REQUIRED |
| `unit-0147.reading-order` | 1 | 2 | `87b5383ad774ad746a6e4499cae8469717fc5a3fedfada482d010b9462d9b0c0` | PASS |
| `unit-0150.reading-order` | 1 | 3 | `ba6be29c38461ec2f822d395221af7867c47dbe68bba68b7b6347bf0f8afe706` | PASS |
| `unit-0151.reading-order` | 2 | 14 | `a5e4126e65b5bf9bde93328482e0064f5b819fef61612be5c005dd5413057807` | CHANGES_REQUIRED |
| `unit-0152.reading-order` | 1 | 4 | `6d73f440003f334b6c04995302dd7fdaa5037be3bda5b3f6567ca4c20ce453d4` | PASS |
| `unit-0158.reading-order` | 1 | 4 | `fcdf6a0f93f029730fc40276155b8e25c7ba424237f94fe75e26de650043f190` | PASS |
| `unit-0159.reading-order` | 1 | 5 | `125564753d92ebdc5cc67a542d26de3ead9263cc3235f5ba690c87ded15c74dd` | CHANGES_REQUIRED |
| `unit-0162.reading-order` | 2 | 7 | `c345fe6866544b312b904c7a3aa9cc0ce3331954b09b6a087b7e257f9a198d9a` | PASS |
| `unit-0165.reading-order` | 2 | 4 | `2939a1a1d9267f82141b9f8298f9e12f499a1af5ee1af0688bf0d8f5b94554e1` | PASS |
| `unit-0167.reading-order` | 2 | 5 | `a0fc0d624af29bcee2b2f40714285fe8bef0e94238b2ccf534dadc96109a0f07` | CHANGES_REQUIRED |
| `unit-0171.reading-order` | 2 | 6 | `f9d054f61a492d891b0aab9abd16f94341fe8240e45962653eda326c05c47043` | CHANGES_REQUIRED |
| `unit-0172.reading-order` | 2 | 5 | `54be91fe7651cc37734f443d1a41138ac4498587e53460df88b069c0dac6564d` | CHANGES_REQUIRED |
| `unit-0174.reading-order` | 1 | 3 | `1a09342795ea1a709bf5191fdb3e2f73c9fc2a8d9cc2c72b735f0fe8ab5fbab2` | PASS |
| `unit-0177.reading-order` | 2 | 9 | `74dfd6fcaebe9c340837d9c4b4072cafd0125ebe9eec1387781418a91de364c2` | PASS |
| `unit-0178.reading-order` | 2 | 6 | `24d2ea335b7a68e8a6ddca5d714f6e1b7335c9df23424f7f4128fa80c5e173b6` | PASS |
| `unit-0185.reading-order` | 4 | 14 | `81c819d781245232459aa3ef9d18d90df3d49158089a09a8c953d43f1a6ae196` | CHANGES_REQUIRED |
| `unit-0186.reading-order` | 2 | 10 | `655fbcefc09f2ed474d4c28b4279c65d2541c851be82990c765310c9582fe6c1` | PASS |
| `unit-0194.part-01.reading-order` | 2 | 9 | `4d6d316a335436f2ed7aac984bf753a55dcc60c9da05c9b38baf9f9ea813753f` | PASS |
| `unit-0197.reading-order` | 1 | 7 | `d9357be14994fd6f0fcb5d3e8e3bd327c6cbdcfda5cdd8f63b9522ba9ef5b80c` | PASS |
| `unit-0198.reading-order` | 2 | 7 | `c16199ebadf397b036deae03648e5f2acdc2d647453d8ca7596151649c6fec0e` | PASS |
| `unit-0200.reading-order` | 2 | 5 | `b7659164cf83231c1eb942ecc30f378e9862a324f0ced834f26878427fb3337b` | PASS |
| `unit-0213.reading-order` | 3 | 11 | `4f49bb44960453f441567e53a598321f5a415cf1dd8c9c00d149be0ebce5bf78` | PASS |
| `unit-0215.reading-order` | 2 | 7 | `7b8ce9f0240421ce21687b54d1697b076a0800c4578d78b217b64ed77c8e15ba` | PASS |
| `unit-0217.reading-order` | 2 | 6 | `0963280d032b3eb2ebcdbf6d52f761cb4c0450d756e8b34c7c9dc34ae3e5445a` | PASS |
| `unit-0218.part-01.reading-order` | 1 | 3 | `4b93a42a6d999f3a6f8a9e0150b6c4f25dcc85e8af8f9fa111479249e5726020` | PASS |
| `unit-0030.reading-order.fragment` | 4 | 26 | `79bb4ced4e255812023f77cd2020636cd17a454efe0fa7c863ed8859424b9f8d` | PASS |
| `unit-0040.reading-order.fragment` | 2 | 5 | `04cf7709e0c067dcdf0e597ab7cd33d336362f849811bd8aef12b7d7ac5f325d` | CHANGES_REQUIRED |
| `unit-0110.reading-order.fragment` | 1 | 3 | `691a54e5434926bf3fd13272e90c913f1e6d110479f5959b5a441d7f08e79190` | PASS |
| `unit-0160.reading-order.fragment` | 2 | 6 | `31dce1900ffe2a7df9764a58a74f7ea8cda5c82468c7e766265fec9e199fb420` | PASS |
| `unit-0173.reading-order.fragment` | 2 | 2 | `893fd55bb7edc96025a721dc6cdf7c3e0f8ec54273b8ca6e1a5473f2c4d43ce2` | PASS |
| `unit-0181.part-01.reading-order.fragment` | 1 | 5 | `27b5e0ff2df2efef030b99dfc45ee440bd66b5db85e1e2aa11427be5eaeddcb9` | CHANGES_REQUIRED |
| `unit-0206.reading-order.fragment` | 1 | 2 | `4e1c98fb3a1ab2add3d3610225db57b1664a7d554d0de80ffe837511a800ea8f` | PASS |
| `unit-0211.reading-order.fragment` | 2 | 8 | `ac67eeac7421f50a39536805bfeb36e7404eb8bc11fe3d8939feeb868dc16b01` | CHANGES_REQUIRED |
| **Total** | **67** | **241** | | **26 PASS / 10 CHANGES_REQUIRED** |

## Blocking findings

No marginal summary is fused into a body line or a hyphen-split word anywhere in the lane. Every blocking finding has the same cause. A page-foot historical note (the source's own `(1) Ex Regest. ...` style note) is emitted in the same paragraph as the body text that precedes it, so the note's wording reads as part of a body sentence, usually inside a word split by a hyphen at the page boundary. The word map gives these note words the `body-left`/`body-right` role, and no paragraph break separates them from the body. Running heads at the same boundaries do get their own paragraph, which is why those are only qualifications.

- `unit-0144.reading-order` p.1: BLOCKING (historical footnote fused into body): right column, §1 paragraph ends '...caslrum Imiusmodi insultare, capere, ipsum fun- (t) Ex Regest. Vatic.' - the page-foot note is run into the body paragraph inside the hyphen-split word 'fun-[ditus]' (derivative LF 64484-64485 with no paragraph break); the body resumes 'diliis tleslriiere' after the running head. Not a marginal summary; a footnote not separately set.
- `unit-0151.reading-order` p.1: BLOCKING (historical footnote fused into body): left column end of §1 reads '... celebralioni di- (I) Aliorum Ordinum prolectores maiores bis facultates non habenl. Has ergo ponerc satis esse arbitratiis sum, ut caeteris Regularibus usui esse possint. C.lieritbiH.' before the body resumes 'vinonim varani' at top of right column: the page-foot note is run into the body paragraph inside hyphen-split 'di-/vinonim' (derivative LF 67671-67672, no paragraph break).
- `unit-0159.reading-order` p.1: BLOCKING (historical footnote fused into body): left column §1 reads '... aut alias ipsorum gubernationi commit- (1) Ex Regest. in Arcliiv. Vatic. (2) Forsan leg. cupidilatis.' then signature 'Bull. Rnm. Voi. lY. 73' then 'iiintur, luiiusmodi provisiones' - the page-foot notes are run into the body paragraph inside hyphen-split 'commit-/[tu]iintur' (derivative LF 69592-69593, no paragraph break).
- `unit-0167.reading-order` p.1: BLOCKING (historical footnote fused into body): left column §1 reads '... nul- lum sen nullam ex prioralibus, praece- (1) Ex Regesl. in Arcbiv. Vatic.' then 'ptorils scii doniibiis ...' - the page-foot note is run into the body paragraph inside hyphen-split 'praece-/ptorils' (derivative LF 70894-70895, no paragraph break).
- `unit-0171.reading-order` p.1: BLOCKING (historical footnote fused into body): left column §1 reads '... ac iidem canonici ad divinum Officium suflìcien- (I) Ex Regesl. in Archiv. Vatic.' then running head, then 'les aul disposili' - the page-foot note is run into the body paragraph inside hyphen-split 'suflìcien-/les' (derivative LF 71347-71348, no paragraph break).
- `unit-0171.reading-order` p.2: BLOCKING (historical footnote fused into body): left column §4 reads '... vel aliis beneficiis ecclesiaslicis in illis par- (I) Arrendure, arrenlare, ad censum ponere, ad censum annuum vel ad emphyleusim praediura locare (Ducange).' then running head, then 'libus generales' - note run into body inside hyphen-split 'par-/libus' (derivative LF 71464-71465).
- `unit-0172.reading-order` p.1: BLOCKING (historical footnote fused into body): left column §1 ends '... olim in ecclesia Sancii Lanreniii ad San- (I) Ex Regpst. in Arcliiv. Valir.' and the body resumes 'eia Sanclorum' after the running head at the top of the right column - the note is run into the body paragraph inside hyphen-split 'San-/[ct]eia' (derivative LF 71595-71596, no paragraph break).
- `unit-0185.reading-order` p.1: BLOCKING (historical footnote fused into body): left column §1 reads '... et eadem Ecclesia in diclis provin- (I) Ex Regest. Vatic.' then 'ciis in spiriliialibus' - note run into the body paragraph inside hyphen-split 'provin-/ciis' (derivative LF 76158-76159).
- `unit-0185.reading-order` p.1: BLOCKING (historical footnote fused into body): right column inserted letter reads '... ausus temerarios reprimil, illi- (1) Deest aliquìd, foisaii adminislralortm , vel alìud simile.' then running head, then 'citos nioliis' - note run into body inside hyphen-split 'illi-/citos' (derivative LF 76219-76220).
- `unit-0040.reading-order.fragment` p.1: BLOCKING (historical footnote fused into body): left column §1 ends '... quod non- nullae persOHae se conlia sanciam ca- (1) Ex Regest. in Archiv. Vatic. (1) Forsan leiitiilUmihus.' and the body resumes 'iholicam Ecclesiam' after the running head and a marginal - notes run into the body paragraph inside hyphen-split 'ca-/[t]holicam' (derivative LF 16019-16020).
- `unit-0040.reading-order.fragment` p.1: BLOCKING (historical footnote fused into body): right column §2 reads '... el talia nefanda credenlibus nul- (l) Deest aiiquid, forsan n rentiam. ctnera- lionem, etc.' then marginal, then 'lum per se' - note run into body inside hyphen-split 'nul-/lum' (derivative LF 16080-16081).
- `unit-0181.part-01.reading-order.fragment` p.1: BLOCKING (historical footnotes fused into body): left column §4 reads '... ac lolius cleri Brunswi- (1) Leg. Romanorum. (2) Caetera legtintur in Conslil. xLviii Honorii III, lom. ni, par. i, pag. 37'» el. seq. (3) OmitliUir nanatio huius Conslil. Ca- roli IV, ([uia per extensum poiiitur hic in Glie. censis , llildeiiseineiisi.s, ...' - the three page-foot notes are run into the body paragraph inside hyphen-split 'Brunswi-/censis' (derivative LF 74180-74181).
- `unit-0211.reading-order.fragment` p.1: BLOCKING (historical footnote fused into body): left column §2 reads '... vesligiis inliaerenies, auctori- (I) Ex Regest. in Archiv. Vatic. Consule Ray- naldum, ann. l'»25.' then running head, then 'tntc apostolica' - note run into body inside hyphen-split 'auctori-/[ta]tntc' (derivative LF 87538-87539).

Suggested remedy (for the tool owner, not done here): emit page-foot note rows as their own block before the next running head, as running heads already are, then re-render and review again. The prior reviewed extents are not affected.

## Per-document findings

### `unit-0133.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0133-reading-order-bf6d617a-la/undated-bullarium-volume-04-unit-0133-reading-order-bf6d617a-la.pdf` (SHA-256 `a9809780f0bec3fd7bd15398b348b975102744f2a90de37d584b8d44c6d0d1e6`, 2 pages). Title `Reformaiio  laxarum  Curiae  civitalis  Be-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 7; none fused.

- p.1 — PASS — PNG `e7dc3ba827098878ac77bcc16748e69c287878211a0b86a4efe2ed4515f73e8e`. Title/issuer/Latin match metadata, no date shown. Two columns read naturally. 7 marginal summaries (Eiordium.; Abusus non-...; laias iuqne...; salaria notariis...; Pro scriptione in protocolla.; Pro iibbrevii tura.; Executio Imi eonstilutioni!) each a separate short block before the section it annotates. No marginal fusion. No digitizer signature.
  - Qualification: printer signature/folio mark 'Bull. Rota. Voi IV. 65' inline in right column between '...et futuri in' and 'eonini sidariis' (non-blocking, series standard).
  - Qualification: source footnote '(1) Ex Regest. in Archiv. Vatic. / An C. )35S...' set as its own block mid left column between 'usque ad' and 'deceni' (printed page-foot note at leaf boundary; separate, not fused).
  - Qualification: stray body-column OCR line 'I . I ,' between 'prò in-' and 'slriimenlis' (word-map role body-right, bbox x1694-1988 inside body column; interlinear OCR noise, not marginal text).
- p.2 — PASS — PNG `da4d810ce29fd74938316e0839780aa103f6eab3cd661462fe533c3fdf397379`. Sparse final page: body ends 'nostri anno tertio.' then dating line 'Dal. die 6 februarii 1355, poni, anno ni.' followed by Source and license notes. Genuine source closing present.

### `unit-0134.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0134-reading-order-57ae4a99-la/undated-bullarium-volume-04-unit-0134-reading-order-57ae4a99-la.pdf` (SHA-256 `2c8ab583c02325472ea5d15a35020defa50808685141081593af0e74d27fbea9`, 1 pages). Title `Extensio  constitutionis  contra  occupantes`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 2; none fused.

- p.1 — PASS — PNG `e2cbed832b8a3b57f9da6aacd7e4a34f4e6ee3c5f0ad9dab00e62f39ce92c6aa`. Title/issuer/Latin match metadata; no date. Single page carries body, closing 'Datum Avenione undecime kalendas iunii...' and 'Dat. die 22 mali 1355', then Source and license notes. 2 marginal summaries ('Eiicniio [u qua ID rubrl<i>.' before the extension clause; 'ciiasuia»;' before 'Nulli ergo') as separate blocks. No fusion.
  - Qualification: source footnote '(IJ Ex Regest. in Archiv. Vatic.' and running head 'Ad, C. «33» mi BIIII.I.AHIUM HOMAM'M Ali. C. 13SS' set as separate blocks mid left column between 'nos' and 'ciipienles' (non-blocking running head).
  - Qualification: stray in-column OCR glyphs ', • n • i • •' (word-map role body-left, interlinear) after 'im-' before 'pugnatores'; OCR noise, not marginal text.

### `unit-0140.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0140-reading-order-297abc0e-la/undated-bullarium-volume-04-unit-0140-reading-order-297abc0e-la.pdf` (SHA-256 `02b8469c7b2b1e3ec722c0aa26ae119641c54d59d0061f179a2dc1705229ce63`, 3 pages). Title `lieatum  Elzeariiim  de  Sabrano  in  Gallia`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 9; none fused.

- p.1 — PASS — PNG `b6f499515717644da090cf244aa6751bb80ff595fac0fef3ab1e118973333b1e`. Title/issuer/Latin match; no date. Two columns natural. Marginal blocks 'ProoBmiuni.', 'Quae Urbanum c'e7n3n?B.ìiV- ...', 'SoDouiiae El- recl'nsentm' each separate and placed before their sections. No fusion, no digitizer signature.
  - Qualification: footnote '(1) Ex Regest. in Archiv. Vatic.' and running head 'An. C. 1371 >"^>0 BULLARIUM nOMANUM An. C. 1571' as separate blocks in left column between 'sanctos suos per' and 'pxoinplaris' (non-blocking).
  - Limitation: OCR-damaged body word '"''' ^ec' after hyphen 'dile-' (body-left role, literal OCR).
- p.2 — PASS — PNG `803014e7e523f99f5e51b84806053f31cabf1bed6bd2f86620ab12f243124030`. Two columns read naturally. Marginal blocks 'MiracuU.', 'b;inas rlisadnun erari BialuerHi', 'f-"" «epul-...', ''•""" L prò hi« l Gr«- jorius.' separate; three placed before their § numbers. No fusion.
  - Qualification (misplaced but separate marginal): block 'f-"" «epul- viiilai- m'J'^c )ncesfiit ...itìa«.' stands as its own paragraph at top of right column between '(pinque eliam, ut ad Ecclesiam' and 'fralrum Minoriim', i.e. interrupting the §4 sentence at its line anchor; not fused into any line.
  - Qualification: running head 'Al). C. 1571 r.KEGOKlUS XI PP. OÓ1 An. C 1571' inline in left column between 'operaque sa-' and 'lulìi'ia' (non-blocking).
  - Qualification: running head 'An C. 1371 oTt"! BiHJ.Aiuuiti HOMANUM An. e. 1371' inline in right column between 'exhibilione' and 'colenda' (non-blocking).
- p.3 — PASS — PNG `2a3e0e2870d53170558be40f29df5b5250db0f24a75eae7aa8de52730b291754`. Sparse final page with body §6-§7, marginals 'Tesiimsnium bano rei.' and 'cidusnia»' as separate blocks, closing 'Dalum Avenione, nonis ianuarii...' and 'Dal. die 5 ianuarii 1371, poni, anno i.', then Source/license notes.

### `unit-0144.reading-order` — CHANGES_REQUIRED

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0144-reading-order-f887a950-la/undated-bullarium-volume-04-unit-0144-reading-order-f887a950-la.pdf` (SHA-256 `02204873dd156b721e7662577c3d3d638c09e07fd03fdbf936c27eb625f4964c`, 3 pages). Title `Damnatio  quorunuìam  slalulorttm  hi  regno`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 10; none fused.

- p.1 — CHANGES_REQUIRED — PNG `0bcad8cce4be71411b131c50642a284c5a4e6c7dc3cb3127e15ff98af6e2b82e`. Title/issuer/Latin match; no date. Two columns natural. Marginals ',', 'Primamstam- """■', 'Alterum (ulum.', 'Terlium sltlu-' separate blocks; no marginal fusion.
  - BLOCKING (historical footnote fused into body): right column, §1 paragraph ends '...caslrum Imiusmodi insultare, capere, ipsum fun- (t) Ex Regest. Vatic.' - the page-foot note is run into the body paragraph inside the hyphen-split word 'fun-[ditus]' (derivative LF 64484-64485 with no paragraph break); the body resumes 'diliis tleslriiere' after the running head. Not a marginal summary; a footnote not separately set.
  - Qualification: running head 'An. C. 1573 GHKGORKIS XI l>P r537 An.r:. 1372' inline in left column before 'diliis' (non-blocking).
  - Qualification: signature mark 'Bull. Rom. Yol. IV. G8' and footnote '(I) Forsan elicere.' as separate blocks in right column after '§ 3. Aliquaiido vero cum praelati sive' (non-blocking).
  - Qualification (misplaced but separate marginal): 'Terlium sltlu-' block sits between '§ 3. Aliquaiido vero cum praelati sive' and 'aliae personae', interrupting the §3 sentence.
- p.2 — PASS — PNG `b2095b0030e1fd1f35386081688553de0490b61ae012173a8a6c2dc7478fe8c2`. Two columns natural. Marginal blocks 'Ei Ti horum ...', 'soni» ecclesia-...', 'SpiriiuHies|.(i- n»c conica in- obeaicnies.' separate; no marginal fusion.
  - Qualification: running head 'Ali. C. 1372 338 UDL1.AHILJ1 IIOMAM'M An. e. 1372' inline in left column between '§ 5 ... in quibus eiiis laiidibus' and '(Icserviiur' (non-blocking).
  - Qualification (misplaced but separate marginal): continuation 'soni» ecclesia- lai l'oniifei.' of the marginal 'Ei Ti horum slitluloni ... per-' sits after that running head, interrupting the §5 sentence.
  - Qualification: footnotes '(i) Leg. f. praedam. (4) Forsan grarius.' and '()) farcire, forsan ... Gallice saisir.' and running head 'An. C 1372 GiiEr.onii 5 XI l'P. o59 An. C 1372' set as separate blocks in right column mid §6 (non-blocking).
- p.3 — PASS — PNG `292bcba4498160b8d75816f3a2db43a52c739b92897a0e0fe0bfe1d9d610f464`. Marginals 'Exiensio hu- Mismn I pnfiia-', 'obsuniiiimde- "?«■»', 'ciau,' separate before §7-§9. Closing 'Datum Avenione, iionis febrnarii...' and 'Dal. die 5 l'ebruarii 1372'. Source note continues into right column; license note present.
  - Limitation: in-column OCR damage '^gudgijipg gpy jjgpj' (§7) and 'jjjg pj' after 'indulgen-' (§8), word-map role body-left at line starts; literal OCR, not marginal text.

### `unit-0147.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0147-reading-order-0656acb5-la/undated-bullarium-volume-04-unit-0147-reading-order-0656acb5-la.pdf` (SHA-256 `87b5383ad774ad746a6e4499cae8469717fc5a3fedfada482d010b9462d9b0c0`, 1 pages). Title `Saraceni  ad  chrislianam  fdem  conversi  et`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 2; none fused.

- p.1 — PASS — PNG `ea51095dc3e1e7f7c3a4844ea43ea79b67825ddcfeac1323e046c090423db1b6`. Title/issuer 'Gregorias Papa XI, inquisitoribns haereticae pravitatis.'/Latin match; no date. Marginal 'Sancuo (Je qua' before §2. Closing 'Dal. apud Villamnovam ...' and 'Dal. die 3 augusti 1372'. Source note flows into right column. Two marginal blocks; no fusion.
  - Qualification (misplaced but separate marginal): block 'Q'i"i rM-.im (j°'„'^j j^^"/, "'' stands as its own paragraph between '§ I. ... quidam de sa-' and 'racenica impielale', i.e. inside the hyphen-split word 'sa-/racenica' at its line anchor; not fused into a line.

### `unit-0150.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0150-reading-order-56240287-la/undated-bullarium-volume-04-unit-0150-reading-order-56240287-la.pdf` (SHA-256 `ba6be29c38461ec2f822d395221af7867c47dbe68bba68b7b6347bf0f8afe706`, 1 pages). Title `Exemptio  Ordinis  fratrum  lì.  Muriae  de`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 3; none fused.

- p.1 — PASS — PNG `b48bbf6ded26cb0a97a8524bec6fdd51e8154dd834a6b227609146a3c8f61876`. Title/issuer (long address to B. Mariae de Mercede)/Latin match; no date. Two columns natural. Marginals 'Oiusae exera- ptiODÌK coore- dendae.' before §1 and 'Eiempn '*""""' before §2 separate. Closing 'Dalum Avenione xvi kalendas iunii...' and 'Dal. die il mail 1373'. 3 marginal blocks; no fusion.
  - Qualification: signature mark 'Uidl. Rom. Voi. IV. 71' inline in left column between 'Hierosolymitani,' and 'de Calatiava' (non-blocking).
  - Qualification (misplaced but separate marginal): '.t^i*<"«' block sits between '... irrilas et iuanes. Nulli' and 'ergo omnino liominiim', interrupting the closing sentence.

### `unit-0151.reading-order` — CHANGES_REQUIRED

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0151-reading-order-5fbbc400-la/undated-bullarium-volume-04-unit-0151-reading-order-5fbbc400-la.pdf` (SHA-256 `a5e4126e65b5bf9bde93328482e0064f5b819fef61612be5c005dd5413057807`, 2 pages). Title `Dedaratio  el  limilalio  anctorUatis  et  fa-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 14; none fused.

- p.1 — CHANGES_REQUIRED — PNG `51827577b71af0b31f16cd2adb7410f9a62235755ffa77ae61f5107b0bea89d0`. Title/issuer/Latin match; no date. Marginals 'ProcemiuM.', 'Reguiarium Or- dimim emo-', 'E' pi-ie^^ipue...', 'i reguU r, ul J'," ...', '"''^ >"" *""« pulcsUlein 111- rmumeoendcii', 'iniiriiirihir muial-erte ...' separate blocks; no marginal fusion.
  - BLOCKING (historical footnote fused into body): left column end of §1 reads '... celebralioni di- (I) Aliorum Ordinum prolectores maiores bis facultates non habenl. Has ergo ponerc satis esse arbitratiis sum, ut caeteris Regularibus usui esse possint. C.lieritbiH.' before the body resumes 'vinonim varani' at top of right column: the page-foot note is run into the body paragraph inside hyphen-split 'di-/vinonim' (derivative LF 67671-67672, no paragraph break).
  - Qualification (misplaced but separate marginals): '"• Orilo a Eoclssia J^' between 'pauper-' and 'talem' (inside hyphen-split word, as its own block); '"""" ".■""""•" rt's ouunuil.' between 'Iidem' and 'I ' _ fratres'.
  - Qualification: running head 'Ari. c. 17)7:, f;iti;(.(jim s \i l'I'. of)ó An. C. (575' inline in right column before marginal 'iniiriiirihir ...' (non-blocking).
  - Limitation: interlinear body-column OCR noise ('<T. ,■ • • '^ lA • i-. 1 • I • 1- L' after 'mulliplicibns'; '|j|.Qj.„,.,,„),|g^'; '" ' 1- • ■') with body roles, not marginal text.
- p.2 — PASS — PNG `45519aa692046414573402634f1b2ce9906b084fd31f9f5bb7d1fb31b36ed39a`. Two columns natural. Marginals 'r.rii.iaips Or- (finis insliiiiere ...11 (teponere:', 'Cu-mquam ad c'ara™ p"omo- v€ie, ei piomo- lum revnciiie:', 'n- loro mn-', 'Dehnqi.pnies fò'iv'ere.'eir"', 'Qaa r uiiiendi pocna fralre.s qiiidqua', '.\dhorta ipgos pio' each separate before its section. Closing 'Datimi apud Pontem Sorgiae...' and 'Dal. die 27 mail 1373'; source/license notes.

### `unit-0152.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0152-reading-order-ff7e276f-la/undated-bullarium-volume-04-unit-0152-reading-order-ff7e276f-la.pdf` (SHA-256 `6d73f440003f334b6c04995302dd7fdaa5037be3bda5b3f6567ca4c20ce453d4`, 1 pages). Title `Quod  officiale^  Status  Ecclesiastici  nemi-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 4; none fused.

- p.1 — PASS — PNG `be3e93f558cd4c8b1d0720f81ea5a1926d6303ab885bdeb61640be6176bd6537`. Title/issuer/Latin match; no date. Marginals 'Exordiiim.', 'oi.si.mi """"', 'Pocnae '°""""' separate before their sections. Closing 'Daliim apud Poiitem Sorgiae...' and 'Dal. die 15 iunii 1373'. 4 marginal blocks; no fusion.
  - Qualification (misplaced but separate marginal): 'Consiiiuiiofde nua in rubricnl.' sits between '§ f. ... vicariis guberiialoribiis' and '. *^ . i> noslris', interrupting the §1 sentence.

### `unit-0158.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0158-reading-order-680a2f89-la/undated-bullarium-volume-04-unit-0158-reading-order-680a2f89-la.pdf` (SHA-256 `fcdf6a0f93f029730fc40276155b8e25c7ba424237f94fe75e26de650043f190`, 1 pages). Title `Clerici  illegilimi  non  admiUantur  ad  ca-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 4; none fused.

- p.1 — PASS — PNG `10eaa5d52ead4bff9cecb113768eb1974b6ad9a7bf4f9e6a6d609ab5fa94ae20`. Title/issuer/Latin match; no date. Two columns natural. Marginals 'AsacriscHTc n"e^l'legu'imi"e'c- ...', 'PioLìlìiio de "i"""" """■■', '.ciomi" "" """', 'Ffroptiii prò ai'U obliiienli-' separate blocks before their sections. Closing 'Nulli ergo, etc.', 'Dalum Avenione, terlìo idus aovembris...', 'Dal. die 11 novembris 1374'. 4 marginal blocks; no fusion.
  - Qualification: running head 'An. C. 1571 GREfiORl S XI PI'. 577 An. C. 137«' inline in left column between §1 and §2 (non-blocking; falls at a paragraph boundary).

### `unit-0159.reading-order` — CHANGES_REQUIRED

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0159-reading-order-7ef37165-la/undated-bullarium-volume-04-unit-0159-reading-order-7ef37165-la.pdf` (SHA-256 `125564753d92ebdc5cc67a542d26de3ead9263cc3235f5ba690c87ded15c74dd`, 1 pages). Title `Cantra  praelatos  et  alias  dantes  munera`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 5; none fused.

- p.1 — CHANGES_REQUIRED — PNG `8f87505040ea312c595fa844a6cc6aaa5081a8bd9935666d30eec01c88adafb3`. Title/issuer/Latin match; no date. Two columns natural. Marginals 'CupiJìtdlis r^ dix prava.', 'ProinMiio «ife- ...', 'inobedieniium ""°^°'', 'CspuHicaiione ...', 'u.usuiae' each separate before its section; no marginal fusion. Closing 'Datimi Avcnionc, spxIo kalcMidas no- vembris...' and 'Dal. die 27 octobris 1375'.
  - BLOCKING (historical footnote fused into body): left column §1 reads '... aut alias ipsorum gubernationi commit- (1) Ex Regest. in Arcliiv. Vatic. (2) Forsan leg. cupidilatis.' then signature 'Bull. Rnm. Voi. lY. 73' then 'iiintur, luiiusmodi provisiones' - the page-foot notes are run into the body paragraph inside hyphen-split 'commit-/[tu]iintur' (derivative LF 69592-69593, no paragraph break).
  - Qualification: signature mark 'Bull. Rnm. Voi. lY. 73' inline in left column (non-blocking).
  - Qualification: running head 'An. f: 137K ^iTS Buu.AnirM ROMAMIM An. C. I37S' inline in right column between '... voluntatem et' and '(Iccri'titm' (non-blocking).

### `unit-0162.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0162-reading-order-909fb97f-la/undated-bullarium-volume-04-unit-0162-reading-order-909fb97f-la.pdf` (SHA-256 `c345fe6866544b312b904c7a3aa9cc0ce3331954b09b6a087b7e257f9a198d9a`, 2 pages). Title `furisdivtio  camerarii  Sanriae  Homanae`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 7; none fused.

- p.1 — PASS — PNG `7d5e4eea9de5e86f374b0ada7ad3d67a03cc0be62de4daeb9be19adf9e191d54`. Title/issuer 'Urbanns episcopas servas servorum Dei, venera»'/Latin match; no date. Two columns natural. Marginals 'cusie huius fooslilulioiiis.', 'Facullas carne- rarii fproul in rubrieay.', 'de pia- r idendi:', 'iud,cibu,-i|iir inliihendi ro- pnllionem ...' are separate blocks before their sections.
  - Qualification: thin interlinear OCR glyph strings with body-left roles inside hyphen-split words: 'Came- r ' ì ■ ■■ 1 / ram' (§1; word-map x390-887, same baseline as marginal 'fooslilulioiiis.', which ends at x390) and 'spccia- "^ , ...,'. lem' (§2, beside marginal 'Facullas carne- rarii'). They contain no summary wording and lie inside the body column; recorded as OCR noise, not marginal-summary fusion, but noted for the coordinator.
  - Qualification: footnote '(1) Ad liane lurisdiclionem vide btdlas ... pag. 820.' set as its own block in left column between 'Camerae cura' and 'commissa' (separate, non-blocking).
  - Qualification: running head 'An. <".. iri7'.t •)^- Itili Alili M uoM.viNiMi An. C. I08O' inline in right column between '... sine strepitu et' and 'ligiir:)' (non-blocking).
  - Limitation: heavily OCR-damaged §4 opening ('<l»! cailSIS IpSIS [lO.sl ...', ', ... ' .'') with body roles.
- p.2 — PASS — PNG `89fd4f24feac59b69be25f3a161c13fa44b51a17a9be18d2f71aef3bff42a706`. Marginals 'Obstantium de- rogaiio', 'i,;,i.o'Ii^I.'iun, ^,'1 ...', 'coucessionem tempore d.ilae lonsinuiionis ... p^^- filili.' separate before §5-§7. Closing 'Datum Romae apud S. Pelrum, vi idiis septembris...' and literal 'Dal. die 8 septembris 1319' (literal source date, not judged). 7 marginal blocks in unit; no fusion.
  - Limitation: in-column OCR noise in §5 and §7 ('^' ^'"•'*', 'i-- ,•, ,■ -i j .1', ', . '., , • I-', '.'.,-' ' .'.,..').

### `unit-0165.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0165-reading-order-7a1b7ee8-la/undated-bullarium-volume-04-unit-0165-reading-order-7a1b7ee8-la.pdf` (SHA-256 `2939a1a1d9267f82141b9f8298f9e12f499a1af5ee1af0688bf0d8f5b94554e1`, 2 pages). Title `Confoederaliones  cwn  haerelicis  quncumque`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 4; none fused.

- p.1 — PASS — PNG `e5ac6961cd1b870bf95e6b6d92ea12a957d1d9d8923ab4a5817ff4aabcf5ac7f`. Title/issuer 'Urbanas episcopus servus servorum Dei,'/Latin match; no date. Two columns natural. Marginals 'Eiordium.', 'venreiUumei Romlrrum fff- deia ...', 'iiuiu.modi f.L deia nulla du- ciaiai. ...' separate and before their sections. No marginal fusion.
  - Qualification (misplaced but separate marginal): 'Ea observari """"" °""""°' sits between '... nulliiis esse' and 'decernimns (irmilalis' in the right column, interrupting the §2 sentence.
  - Qualification: running head 'An. C 1382 CRBANUS VI l>P. u8o An.C. 138-2' inline in right column between 'quomo-' and '(lolibet' (inside a hyphen split; non-blocking).
  - Qualification: footnote '(1) Ex Collectione Acloium Rimer.' set as its own block in left column between 'illiciiae et' and 'ipso iure' (separate, non-blocking).
  - Limitation: thin interlinear body-column OCR noise '. p I . r I „' and damaged word ''"•^''^'^' in §2 (body roles).
- p.2 — PASS — PNG `f1d2c5c71490ddf1d35de06560b3ccd9784dfcd574611b462120aa72f76ccbfb`. Sparse final page: §5 'Nulli prgo ...', closing 'Daliim Romae apud Sanctnni Pelrum ...' and 'Dat. die 30 niarlii 138'2', then Source/license notes. Genuine source closing.

### `unit-0167.reading-order` — CHANGES_REQUIRED

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0167-reading-order-81ccb0b8-la/undated-bullarium-volume-04-unit-0167-reading-order-81ccb0b8-la.pdf` (SHA-256 `a0fc0d624af29bcee2b2f40714285fe8bef0e94238b2ccf534dadc96109a0f07`, 2 pages). Title `Quod  fialres  hospitalis  Sancii  Ioannis  Mie-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 5; none fused.

- p.1 — CHANGES_REQUIRED — PNG `ed1a47b34927cba4c87c389d39747e46f71c9e605ae5d75d69566398a562b302`. Title/issuer 'Urbanns episcopos'/Latin match; no date. Two columns natural. Marginals 'Ambiiio in ec- tenibile viiium.', 'Causae eden- nae huius eoa- siiiuiioiiis.', 'Prohihet fra- l'nrrliu5'''e'ir ''' Online obu-', 'Poenae ino- ...', 'Praeccpion i:\- fullalcni ...' separate and before their sections; no marginal fusion.
  - BLOCKING (historical footnote fused into body): left column §1 reads '... nul- lum sen nullam ex prioralibus, praece- (1) Ex Regesl. in Arcbiv. Vatic.' then 'ptorils scii doniibiis ...' - the page-foot note is run into the body paragraph inside hyphen-split 'praece-/ptorils' (derivative LF 70894-70895, no paragraph break).
  - Qualification: running head 'An C 1585 588 U( i.l.AKlL.il uuM AM>M An. C i585' inline in right column between 'singoli' and 'singulas' (non-blocking).
  - Limitation: in-column OCR noise '. . ^ . . .' after 'lios-' (body role).
- p.2 — PASS — PNG `61c8362f67465d300427cc26b9d2afa47ef3b12a4fecfa508a6a6c898e44c860`. Sparse final page: end of §6, closing 'Dalum apud Monlera Flasconem ...' and 'Dal. die 15 septembris 1383', then Source/license notes.

### `unit-0171.reading-order` — CHANGES_REQUIRED

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0171-reading-order-d7c6bcc0-la/undated-bullarium-volume-04-unit-0171-reading-order-d7c6bcc0-la.pdf` (SHA-256 `f9d054f61a492d891b0aab9abd16f94341fe8240e45962653eda326c05c47043`, 2 pages). Title `Fralribus  Ordinis  Servorum  Sanclae  Ma`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 6; none fused.

- p.1 — CHANGES_REQUIRED — PNG `ee787448fd3f2a8d41f919cf515faad7db17936f58e779d757bc2716a359b968`. Title/issuer 'Urbanus episcopus servus servorum Dei , vene-'/Latin match; no date. Two columns natural. Marginals 'eio', 'caus "**""', 'EociesiaS.Mar- celli, in qi' ca- noniri jesHiani ...', 'Daia e\e(iufn- ili fiicull,.< la- cobo epi^c. Are- ...', 'oijsiani """"' separate before their sections; no marginal fusion.
  - BLOCKING (historical footnote fused into body): left column §1 reads '... ac iidem canonici ad divinum Officium suflìcien- (I) Ex Regesl. in Archiv. Vatic.' then running head, then 'les aul disposili' - the page-foot note is run into the body paragraph inside hyphen-split 'suflìcien-/les' (derivative LF 71347-71348, no paragraph break).
  - Qualification: running head 'An. C. n8'l URBANtJS VI PP. m\ An. C. tSS't' inline in left column (non-blocking).
  - Limitation: in-column OCR noise '• ,■ ,■ ^' e ■ ]■' after 'Iralrum in dieta' (§2) and ',. . , ' r' after 'aposlo-' (§3), body roles.
- p.2 — CHANGES_REQUIRED — PNG `f5a79b88a5e5e85849c607e6e88967241cf1bcd71ed0d10bc492da279ba9728a`. Marginal 'Alieno caulum.' separate before §5. Closing 'Dalum Roniae apud Sancliim Petrum, septimo idus decembris...' and 'Dal. die 7 decembris 1384'; source/license notes.
  - BLOCKING (historical footnote fused into body): left column §4 reads '... vel aliis beneficiis ecclesiaslicis in illis par- (I) Arrendure, arrenlare, ad censum ponere, ad censum annuum vel ad emphyleusim praediura locare (Ducange).' then running head, then 'libus generales' - note run into body inside hyphen-split 'par-/libus' (derivative LF 71464-71465).
  - Qualification: running head 'Ali. C. 1384 f>92 BIILI.AIIIUM llovuMiM An. C 1585' inline (non-blocking).

### `unit-0172.reading-order` — CHANGES_REQUIRED

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0172-reading-order-1c4335b9-la/undated-bullarium-volume-04-unit-0172-reading-order-1c4335b9-la.pdf` (SHA-256 `54be91fe7651cc37734f443d1a41138ac4498587e53460df88b069c0dac6564d`, 2 pages). Title `Sanclorum  Pelri  et  Patili  apostolorum  irò-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 5; none fused.

- p.1 — CHANGES_REQUIRED — PNG `7c43ca0887be8b824c095fed5e0c5d8571afa3974afc006200a3cd796c18b240`. Title/issuer 'Urbanus episcopas'/Latin match; no date. Two columns natural. Marginals 'Excidumi', 'H" roiiquùe uiide sumplae.' separate before their sections.
  - BLOCKING (historical footnote fused into body): left column §1 ends '... olim in ecclesia Sancii Lanreniii ad San- (I) Ex Regpst. in Arcliiv. Valir.' and the body resumes 'eia Sanclorum' after the running head at the top of the right column - the note is run into the body paragraph inside hyphen-split 'San-/[ct]eia' (derivative LF 71595-71596, no paragraph break).
  - Qualification (misplaced but separate marginal): 'Eas. earumque leremes quibus subiecU poenis.' stands as its own block between 'fidelium re-' and 'condi, perpeluis', i.e. inside hyphen-split 're-/condi'.
  - Qualification: running head 'Ali. c. nsb URBANDS VI l'P. r;9"> Aii. C \7a:>' at top of right column and signature 'Bull. fiom. Vul. IV. :ó' inline in right column (non-blocking).
  - Limitation: in-column OCR noise '_^ V , . . ' ,' and '..^ I . n -. 1- •' (body roles).
- p.2 — PASS — PNG `f3507c01e73cf065afb34a870baa6421138085716f981627e78173c4b5eb7010`. Marginals 'temporsles.' before §2 and 'chii-uiae' before §3 separate. Closing 'Datiim apiul Montem Flasconem, quinto kalendas augusti...' and 'Dat. die 28 iulii 138ìi'; source/license notes.
  - Qualification: running head 'Ali. C. ir>8S fifli BIIMAIIIUM An. C. t38!>' inline between 'prorsus red-' and '(laiiliir indigni' (inside a hyphen split; non-blocking).

### `unit-0174.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0174-reading-order-c60f9cc1-la/undated-bullarium-volume-04-unit-0174-reading-order-c60f9cc1-la.pdf` (SHA-256 `1a09342795ea1a709bf5191fdb3e2f73c9fc2a8d9cc2c72b735f0fe8ab5fbab2`, 1 pages). Title `Causaruni  Curiae  Capiloliitae  cognilionem`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 3; none fused.

- p.1 — PASS — PNG `0259152017dde228a0a90731eb99376cb95e2c6121d32a027a1f2ed93576f9f4`. Title/issuer/Latin match; no date. Two columns natural. Marginals 'j.J^^JJ^ ippella ''' cur ia Capi' ilatuti.', 'consiiiuiiofde quain ru lira .', 'euumi.»' separate before §1-§3. Closing 'Daliim lioniae apiid Saiiclum Peiruin ...' and 'l);it. (Ile 28 iiovembris 1380' with source/license notes. 3 marginal blocks; no fusion.
  - Qualification: footnote '(1) Ex Regest. in Archiv. Vatic.' and running head 'An. C. 1583 l'RitAMS VI l'I'. 597 An. e 1588' set as separate blocks in left column between 'a cuius quidem iudicis' and 'seiileiilìis' (non-blocking).

### `unit-0177.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0177-reading-order-04015c29-la/undated-bullarium-volume-04-unit-0177-reading-order-04015c29-la.pdf` (SHA-256 `74dfd6fcaebe9c340837d9c4b4072cafd0125ebe9eec1387781418a91de364c2`, 2 pages). Title `In^lilulio  festiritalìs  Visilationis  lì.  Marine`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 9; none fused.

- p.1 — PASS — PNG `4ea26d20997b6d3e082ed0a26bd892a9bb244e88cc32fb351b1390bdb7bd5447`. Title/issuer 'Bonifacius episcopus servas servorum Dei,'/Latin match; no date. Two columns natural. Marginals 'Proffimiuoi.', 'eìhs Luniinias s^J^'f,""" °', 'sequumuriu»- riae «ncomia.' separate before their sections. No marginal fused into a body line.
  - Qualification (misplaced but separate marginals): 'incarnaiionis mj^ienam.' stands as its own block between 'eam a morlis ne-' and 'xil)us liberaret' (inside hyphen-split 'ne-/xil)us'); 'Yirgitiis Miri» elosuim.' between 'clemens' and 'Verbi aelerni', interrupting the proem sentence.
  - Qualification: running head 'Ali. C. I?i89 ROMPACI is IX i>p. 603 .\n. C. 1589' inline in right column between 'Magnificat anima' and 'ine;i Duiiiiiiiini' (non-blocking).
  - Limitation: in-column OCR noise '. j I ■ li • 1-' after 'pra-' and '.... . '. *^ I -Il I •' after 'hu-' (body roles).
- p.2 — PASS — PNG `52fef200b9aae2896985bbb3ea5ac840d98e665c6226a6cdf6e696d5c04148d6`. Two columns natural. Marginals 'Festuni Visila- itnnlsahCrbaQO iiishtulum', 'ofEuo ei mi!. pr-iesenlibusin- duUentias con-', 'Hìs fìrmalìs, ad liuiusmodi festi public:itìo- nem ...' separate before their sections. Closing 'Dalum Romae apud S. Pelrum, qumlo idus novembris ...' and 'Dal. die 0 novembris 1380'; source/license notes. 9 marginal blocks in unit; no fusion.
  - Qualification (misplaced but separate marginal): 'cum duplici of- òcìavà."'' stands as its own block between 'per orbem universum' and 'solemnilrr celebrai eliir', interrupting the §3 sentence.
  - Qualification: running head 'An. C. 1389 60i BULLARIL'M UOMANUM Ali. ('.. 1590' inline in right column between 'vesperorum,' and 'luissae' (non-blocking).

### `unit-0178.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0178-reading-order-28b6df6b-la/undated-bullarium-volume-04-unit-0178-reading-order-28b6df6b-la.pdf` (SHA-256 `24d2ea335b7a68e8a6ddca5d714f6e1b7335c9df23424f7f4128fa80c5e173b6`, 2 pages). Title `Camerae  Aposlolicae  bona  delinentes  seu`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 6; none fused.

- p.1 — PASS — PNG `2e94d38530d9d86ba9e5174788329ac0d45c7d95f0d4c2595225cb4e84214823`. Title/issuer 'Bonifacins episcopas servas servoroin Dei, ad fataram rei memoriam.'/Latin match; no date. Two columns natural. Marginals 'Humauam cu- Sibù'ffeTe'^en,- pe...', 'Bona Camcrae occupala eidera refulm lubei.', ''^''p''. ExcoQ ...- tionis,', 'P"Bnase,!iiera ai) non rcTelan- ie=, ...' separate; no fusion.
  - Qualification: footnote '(I) Ex Regesl. in Archiv. Vatic.' and running head 'An C. 1590 HOMI ACM S l\ l'I', 60d A II. C 1500' set as separate blocks in left column between 'subse' and 'cula poena' (non-blocking).
  - Qualification (misplaced but separate marginal): 'ei pnTjiionis ^'^^ ,^'^' ""^l "of"" poeDU.' sits between '... oblinenda: si' and 'vero laicales', interrupting the §3 sentence.
  - Limitation: in-column OCR noise ''- ■ ' • .' after 'ti-' (§2) and ''^ . . ' -,' after '§ 4. Caelerum, ne praeseutes lilerae' (body roles).
- p.2 — PASS — PNG `86de35a8c72327eb6adf75be9d159d0df90fdb1475642784d6754397b10054a4`. Marginal 'Pubiicn pn- mandai.' separate before §5. Closing 'Datiiin Hoiiiac a|iii(J Sanclum Pelruiii ...' and 'Hai. die 18 septeinbris 1390'; source/license notes. 6 marginal blocks in unit; no fusion.
  - Qualification: running head 'An, C. 1590 606 BULLA II IH IIO.MANUM Ali. C. 1.5'Jl' inline between §5 and §6 (paragraph boundary; non-blocking).

### `unit-0185.reading-order` — CHANGES_REQUIRED

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0185-reading-order-a167b7c2-la/undated-bullarium-volume-04-unit-0185-reading-order-a167b7c2-la.pdf` (SHA-256 `81c819d781245232459aa3ef9d18d90df3d49158089a09a8c953d43f1a6ae196`, 4 pages). Title `Confinnado  stalulorum  et  oidiiuUionum`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 14; none fused.

- p.1 — CHANGES_REQUIRED — PNG `0242479566fb5907bc2c9e24333085dffff189f444b3c00d31200bd05823da05`. Title/issuer 'Bonifaclus episcopas, servus servorum Dei,'/Latin match; no date. Two columns natural. Marginals '!', 'AniivKim «er- 3'i"i„s...', 'Bnnifani i.is-' separate before their sections; no marginal fused into a body line.
  - BLOCKING (historical footnote fused into body): left column §1 reads '... et eadem Ecclesia in diclis provin- (I) Ex Regest. Vatic.' then 'ciis in spiriliialibus' - note run into the body paragraph inside hyphen-split 'provin-/ciis' (derivative LF 76158-76159).
  - BLOCKING (historical footnote fused into body): right column inserted letter reads '... ausus temerarios reprimil, illi- (1) Deest aliquìd, foisaii adminislralortm , vel alìud simile.' then running head, then 'citos nioliis' - note run into body inside hyphen-split 'illi-/citos' (derivative LF 76219-76220).
  - Qualification (misplaced but separate marginal): 'campanue « rom'i'ùm"' stands between 'claruit devotionis integritas,' and 'splenduit reverentiae plenitudo', interrupting the sentence.
  - Qualification: running head 'Ali. C. l'iOO 050 BlLI-AKIl !>1 lluMANUM An. e. l'iOO' inline in right column (non-blocking).
- p.2 — PASS — PNG `96c44435d631a13d115686abf246fba86359759ba0d8ad0bfa9d29016c10d903`. Two columns read naturally; no marginal fused into a body line.
  - Qualification (misplaced but separate marginals, all as own blocks at their line anchors inside the inserted letter's run-on paragraphs): 'De forma iu- d.eiorum.' between 'super' and 'eodcm'; 'De appeiiaiio-' inside hyphen-split 'Or-/dinamus'; 'l'ignora non i,,,,,, 1,^5' inside hyphen-split 'Prae-/lerea'; 'i>e deposuo compositionum.' between 'appellalione' and 'pendente'; 'De cusiodibu»' between 'maleficium' and 'exlilil'; stray marginal '-' between 'Ad' and 'haec'.
  - Qualification: running head 'BONIFACICS IX l'P. fi-'l An C. l'iOO' inline in right column inside hyphen-split 'accu-/sali' (non-blocking).
  - Limitation: in-column OCR noise '' , ■• ■• .• •,' after 'redo-' (body role).
- p.3 — PASS — PNG `10adaa72ea9bcc807223a5791678f3d0a16526f39176ecc4dda8822a182b5654`. Marginal 'De minoribus ,lòn"«'('imm'e'n"- ""*' separate before its paragraph. Inserted letter closes 'Dalum Anagniae, quarto kal. oclobris ...', then 'Nulli ergo omnino ... intVingere, eie.' No marginal fusion.
  - Qualification (misplaced but separate marginals): 'AppelIanUs uou molestao-' inside hyphen-split 'ilislri-/cliiis'; 'D« TMiisiau- sarum mode- randis expeii- *'••' inside hyphen-split 'om-/„jn,ojie'; 'i"obedieiiies buie eonslitu- iionianaibema- ...' between 'omupm' and '. , . procpssum'.
  - Qualification: running head 'An. C 1400 G32 BUIIAIUIIM IlOMANdH An. C. l'iOO' inline in left column between 'liberalioni.s,' and 'absolulionis' (non-blocking).
  - Limitation: in-column OCR noise '. . , i- • ■ •.• *' after 'pro-'.
- p.4 — PASS — PNG `5ec14d80c85f053f6fcd1fafdbea574e79fcfc91637df3c094b702a7320574de`. Sparse final page: running head, genuine dating clause 'Datum Romae apiid S. Pelrum , se- ciindo idus iiinii, pontificaliis nnslii anno undecimo.' and 'Dal. die 1^2 ìunìi 1400', then Source/license notes. Source-bearing closing present. 14 marginal blocks in unit.
  - Qualification: final page opens with running head 'An. C. eoo BONIFACl js IX pp. 635 Ali. e. HOO' (non-blocking) before the act's own dating clause.

### `unit-0186.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0186-reading-order-d44a9cbe-la/undated-bullarium-volume-04-unit-0186-reading-order-d44a9cbe-la.pdf` (SHA-256 `655fbcefc09f2ed474d4c28b4279c65d2541c851be82990c765310c9582fe6c1`, 2 pages). Title `Ecclesia  S.  Michaelis  in  Monte  Gargano`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 10; none fused.

- p.1 — PASS — PNG `bb0ca914f80e8ecb76cd64721409daddc2197ccaeab8f2f363288965126426d7`. Title/issuer/Latin match; no date. Two columns natural. Marginals 'Siponuna Ec- p'(,*ii,"„'."„rrBe "^ "«' before §2 and 'lerra praecii- icm erViur'r' at column foot are separate blocks; no fusion.
  - Qualification: footnote '(1) Ex Ughell., Ital. Sac, tom. vn.', signature 'Bull. Rom. Voi. IV. 80' and marginal 'infein sipon- lime rivilatii mun.' set as separate blocks in left column between '§ i. Cum ilaque, sicut ipsa veritas et' and 'facli evidenlia' (non-blocking / misplaced-but-separate).
  - Qualification (misplaced but separate marginals): 'Eccie, iS. Mi- ri llon- J, u,'r' between 'monlis vertice' and 'supremo'; 'Te"" Montìs li inco- 1,3^ caVienTquo foetnindarebui.' between 'sexus' and 'desfunt'.
  - Qualification: running head 'An. C. l/iOO 05-4 BllM.AimiM nOMANtJM An. e. l/lOO' inline in right column between 'honoribo§' and '(lecoraveial' (non-blocking).
  - Limitation: in-column OCR noise ', , ,. •!' after 'metropolitana'.
- p.2 — PASS — PNG `8af6537c8c61c2649a3194ea791d1fe74e42bc9026966246b3787a6d568df6b4`. Two columns natural. Marginal 'De rcdailibus aicliii'piepifico- pì II capiiuli.' before §3. Closing 'Diiliim Roma»! a|)ii(l Sanctuin Peliiiin ...' and 'Dal. die 5 ilecenil)ns 1 400'; source/license notes. 10 marginal blocks in unit; none fused into a body line.
  - Qualification (misplaced but separate marginals): 'Eiciesia veio raiiiedrricm è" nieiropoiii.' inside hyphen-split 'lempo-/ribus'; 'Arrhiepisropus Siponlirius el Gaigankus ap-' between 'Perìeluo per' and ', ' ,■ L- praespoles'; 'Capilull assl- gnalki.' between 'ìnletidìmus' and 'removere'; 'ibilanliuni (te ojalio.' between 'non' and 'obslanlibus'.
  - Qualification: running head 'e. l'iOO BUiMFAtI 633 Ari. C. I')05' inline in right column between 'statuti ,' and 'coiifiimalioilis' (non-blocking).

### `unit-0194.part-01.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0194-part-01-reading-order-eb6d2cb6-la/undated-bullarium-volume-04-unit-0194-part-01-reading-order-eb6d2cb6-la.pdf` (SHA-256 `4d6d316a335436f2ed7aac984bf753a55dcc60c9da05c9b38baf9f9ea813753f`, 2 pages). Title `Confirmatio  fralrum  Eremitaruin  S.  Hie-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 9; none fused.

- p.1 — PASS — PNG `a950cfb0fa0f6761b50244b28ace091891d92b0045a88733edbcf7f5a124978c`. Title/issuer 'Gregorius episcopus servus servorum Del, ...'/Latin match; no date. Two columns natural. Marginals 'E.oriium.', 'pmh,, >h \n- "tiis"hù"us con- ...', 'omcessaabco- ...', 'Laeris vero eód"mn"en'con"- ... Gregotm;', 'AequisitHque usque adhuc bo- na foniirmai.' separate before their sections; no fusion.
  - Qualification (misplaced but separate marginal): 'Nova peiiiioqni, Ji* 'f'j'j*,,^"""' stands between '§ 5. Quare iidem Carolus el fratres.' and 'iu liumililatis spirila', interrupting §5.
  - Qualification: footnote '(i) Diclim, per singulos dies, quotidie.' set as its own block between 'venire el' and 'ipsorum habiluni' (separate, non-blocking).
  - Qualification: running head 'An. C. t/iiN 65i laii-i.Aimni ROMAMIM An. C. 1415' inline in right column between 'assumpli,' and 'ne i|)si' (non-blocking).
  - Limitation: in-column OCR noise '" _' and '. . ' '' (body roles).
- p.2 — PASS — PNG `6b696e61fd3712c56edd2f9469a34c59a3cd9dd76e515c52d97e1fdafe4e733c`. Marginals 'AUae eis con- fìrmatae domiis.' and 'obsiamium de- ""^"""' separate before §6/§7. Closing 'Dalum in castro Monlisflorum ...' and 'Dal. die 8 iulii 1415', then source note '(1) Deest conslitutione.' and Source/license notes. 9 marginal blocks in unit; no fusion.
  - Qualification (misplaced but separate marginal): '.^liosrecipien- di, coeraeie- rjimq„e haben- •" ...' stands between 'vel eos illa alias iusto' and 'titillo contingel', interrupting §6.
  - Limitation: §6 opening split by an OCR-noise line '■ , I ... cu|)imiis' (body role).

### `unit-0197.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0197-reading-order-1dd67005-la/undated-bullarium-volume-04-unit-0197-reading-order-1dd67005-la.pdf` (SHA-256 `d9357be14994fd6f0fcb5d3e8e3bd327c6cbdcfda5cdd8f63b9522ba9ef5b80c`, 1 pages). Title `Cantra  impedientes  execulionem  literarwn`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 7; none fused.

- p.1 — PASS — PNG `ca810218c9e8497ead843aa0e7aad435f2a94d9a74b7c19fe8fff0e35280b643`. Title/issuer 'Martinus episcopus servus servorum Dei, ad fatnram rei memoriam.'/Latin match; no date. Two columns natural. Marginals 'i'rr.tpmmm.', 'U"»et,prrii tr- h^i.i vi coii- ,.e,5io.', 'Qu^e mai in- i^ ' " rm .', ''»»"' conees- ^'inem revocai Maruoos.', 'Sentenliasqno e contrario latas irriiat', 'Secusque a- gentes debitifl roercet poenis.' separate before their sections. Closing 'Dalnm Conslantiae ...' and 'Dal. die 30 aprilis 14i8'. 7 marginal blocks; no fusion.
  - Qualification (misplaced but separate marginal): 'I.ilPrJ»qiie »- pneinlii^as libe- ro vult execu- Ijnni manditri:' stands after the running head between 'tenore praesenlium,' and 'hoc sacro Conslaniìense', interrupting §3.
  - Qualification: running head 'An. r. |/||S 678 BIII.I.AIIK M HO.MANIIM Am C l'ilR' inline in right column (non-blocking).
  - Limitation: in-column OCR noise '.,:■-. .... . . '' (§1) and '"^ 11- 1 I ■ .•' after 'ca-' (§3), body roles.

### `unit-0198.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0198-reading-order-46b940e6-la/undated-bullarium-volume-04-unit-0198-reading-order-46b940e6-la.pdf` (SHA-256 `c16199ebadf397b036deae03648e5f2acdc2d647453d8ca7596151649c6fec0e`, 2 pages). Title `Ordinis  Mendicanlium  professoribus  qui-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 7; none fused.

- p.1 — PASS — PNG `90c88409ed753e2d9862a157cd5de4a167288bc1caa164d19f0671eb43d9129e`. Title/issuer 'Martlnus episcopus servus servorum Dei, ad perpetuam rei memoriam.'/Latin match; no date. Two columns natural. Marginals 'ordir ^^"_|^"' nd iilios Ordim 5, C.itlu- ...', ''■■-', 'Quenique "' Ordine, ili DOTani e sii professioii slare pracrìpil', '"""" ad suam gionem vu ,e-', 'Hunrvei sinim a ",'[ posl$run "<' separate before §1-§5; no fusion.
  - Qualification: footnote '(t) Ex Regesl. in Arctiiv. Vatic.' set as its own block inside the SUMMARIUM between '... vull remeare.' and '— 5. llunc vero' (separate, non-blocking).
  - Qualification: running head 'MARTINCS V Pl>, 079 An. C. 1418' inline in right column between 'admilti' and 'aiit lecipi' (non-blocking).
- p.2 — PASS — PNG `a306a2fc48d75b209cc432393fd78434d99941adbf414b5cdbc0a96d29c6ee11`. Marginals 'oimamibus de- "^"' and 'ciausuiae.' separate before §6/§7. Closing 'Dalum Gebennis, quarto kalendas au- gusti, anno primo.' and 'Dal. die 29 iulii 1418'; source/license notes. 7 marginal blocks in unit.

### `unit-0200.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0200-reading-order-386e0f2b-la/undated-bullarium-volume-04-unit-0200-reading-order-386e0f2b-la.pdf` (SHA-256 `b7659164cf83231c1eb942ecc30f378e9862a324f0ced834f26878427fb3337b`, 2 pages). Title `//t  officio  provincialalus  non  possutit  fratres`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 5; none fused.

- p.1 — PASS — PNG `ce0f403e8e3de177654dc2328acc5c74385a200b787be7e151f928923ad14fe8`. Title/issuer 'Martinas episcopus'/Latin match; no date. Two columns natural. Marginals 'Ordinis e I cohiberp:', 'Consiii i,'!.-^^^ ',', 'HrovinrUlos ultin lemiiiium nuuiiie vei.i.', 'l'iiori gene- eìs'pcnMndi 'a- dimii ...', 'chusuKie.' separate before §1-§5. 5 marginal blocks; no fusion.
  - Qualification: footnote '(1) Edidit Empolus in Bullar. Ordinis huiiis.' and signature 'Bull. Kom. Voi. IV. 87' set as separate blocks in left column between 'gloriae el ambilionis' and '(ludi, el sua serie' (non-blocking).
  - Qualification: running head 'An. C. mS fi90 BUI-LAnilM noMANHM An. C. 1420' inline in right column between 'a fine' and 'li'i'inìni' (non-blocking).
  - Limitation: in-column OCR noise '^|,pj,^ ^^^^' (§3), ',.:;,|,' (§4), ',.^.;||' (§5).
- p.2 — PASS — PNG `512b537545d3989ac7105c13362bc1a63b9bf49df941f5a30ce591c41ed5307f`. Final page: source dating line, then project Source and license notes.
  - Qualification: sparse final page carrying only the source's dating line 'D;it. die 17 oclobris 1418, poni, anno i.' before the Source/license notes; this is a genuine source closing line, so not a notice-only page.

### `unit-0213.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0213-reading-order-b3a86695-la/undated-bullarium-volume-04-unit-0213-reading-order-b3a86695-la.pdf` (SHA-256 `4f49bb44960453f441567e53a598321f5a415cf1dd8c9c00d149be0ebce5bf78`, 3 pages). Title `Inililulio  Sludn  generalis  in  oppido  Lo-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 11; none fused.

- p.1 — PASS — PNG `34899e52d3b9da6d33bf0c6b67e57d1af610131a16049a27462bf2c3e24c85d9`. Title/issuer 'Martinus episcopus servus servorum Dei,'/Latin match; no date. Two columns read naturally. Marginal 'Ducis Braban- i;ie pelilio prò' separate before §1. No marginal fusion.
  - Qualification: running head 'An. C. \llìi 721 BIII.I.AIIUIU ito.MAiNiiM An. G. IWS' inline in right column inside hyphen-split 'confoveiidum-/que' (non-blocking).
- p.2 — PASS — PNG `36d1498fc6309eb7b6558c48f7f513f150f556bfa369ae0fcde5fd67fc89384b`. Two columns natural. Marginals 'Daeis Braban- tiae pelitioni addila nonnulla de rectoris ...', 'a.- dy.iorum ...', 'Marimus sm- ^3ii,...', 'srliolarihiis e» leriinim ... elarfi tur.', 'Licentiali ubi- qae decere pos- sunl.', 'Scbolastico da- ta facallasquas- cumque cogno- scendi causas ...' each separate before its section; no fusion.
  - Qualification (misplaced but separate marginals): 'Dnmam apiam ad hoc «ligil fnm rohu! om- nihns opporto-' near top of left column; stray marginal 'I' after 'prò buiusmodi Studio' at foot of left column (as own block).
  - Qualification: running head 'An. C- Id-ib MVnTINUS V l'P. ilo C. IW:»' inline in right column between 'qualibel,' and 'praeteiquam' (non-blocking).
  - Limitation: in-column OCR noise ', .*^ S- I I' (§3), ', i it • ' • * i' and ', . -ii . » • • -i-i qua„, j„' (§4), 'nigutjg \\\\f^' (body roles).
- p.3 — PASS — PNG `81638d34b7062391481115c82fb9cc5914b9a68824596044c107e76433eb0929`. Marginal 'Ob&lantium de- rosatio.' separate before §11. Closing 'Nulli ergo ...', 'Daturn Romae apiid Ss. Apostolos quinto idus decembris ...' and 'Dal. die 9 decembris 1420'; source/license notes. 11 marginal blocks in unit; no fusion.
  - Qualification (misplaced but separate marginal): 'sis infra an- n slelerinl, lìtleras ir-' stands between §11 and §12 as its own block (a marginal continuation for the §12 summary).

### `unit-0215.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0215-reading-order-e0248faf-la/undated-bullarium-volume-04-unit-0215-reading-order-e0248faf-la.pdf` (SHA-256 `7b8ce9f0240421ce21687b54d1697b076a0800c4578d78b217b64ed77c8e15ba`, 2 pages). Title `Proliibido  Iraliendi  personas  ecclestanlicas`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 7; none fused.

- p.1 — PASS — PNG `83f4edbdde26cffb78dce6d59dd4b847cfbbed9c97bedab76d075d3b5095d29d`. Title/issuer 'Martinus episcopus servus servorum Dei, ad perpetuam rei memoriam.'/Latin match; no date. Two columns natural. Marginals 'Exoniium.', 'AiiiiBus non- mlieriii suiioi- los dolci, lum fx parie .u,li- .uni,', 'imn ex pane °^].",'^...', 'Su b iiocuisiU- qu.' hi,- <.x|„«. 'iiusiS ... Telai:' separate before their sections. No marginal fusion.
  - Qualification: running head 'An. C. 1/1-28 MARTrNI 729 An. C nm' inline in right column inside hyphen-split 'vilipen-/dium' (non-blocking).
  - Limitation: §1 split into a new paragraph by an OCR-noise line start '1 • f lomporalibus' and in-column '(●ramenlorum' (body roles).
- p.2 — PASS — PNG `a85df6dd81753a8c1ec717af226b5430eb533ba0afa9e8093ce3bf2793986c4c`. Marginals 'Laicosque oflì- ciales compii- cesqoe tatìa at-' before §4 and 'El corilra eos- dem asi man-' before §5 separate. Closing 'fiatum Romae apud Sanclos Aposlo- los, kalend. februarii ...' and 'Dal. die 1 februarii 1428'; source/license notes. 7 marginal blocks in unit; no marginal fusion.
  - Qualification: printer signature mark 'Bidl. Rom. Vul. IV. 'Ò'I' run inline at the end of the §4 line '... personas, posl-' (non-blocking per series standard).
  - Qualification (misplaced but separate marginal): 'lenUntei ei- conimiiD'c lIoDÌ addjcil :' stands as its own block inside hyphen-split 'posl-/(|iiam'.

### `unit-0217.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0217-reading-order-e6865382-la/undated-bullarium-volume-04-unit-0217-reading-order-e6865382-la.pdf` (SHA-256 `0963280d032b3eb2ebcdbf6d52f761cb4c0450d756e8b34c7c9dc34ae3e5445a`, 2 pages). Title `Quod  festivilas  Sanclissiiììi  Corporis  Chrhli`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 6; none fused.

- p.1 — PASS — PNG `30c6ca9ea1e771a320707dcb41f149509e6feb905d838391408b315cd8a407bc`. Title/issuer 'Martinus episcopas servus servoram Dei, ad futaram rei memoriam.'/Latin match; no date. Two columns natural. Marginals 'Hoc festam ab Orbano IV in- gtitutum, non-' and 'Huiusmodi ìd- pi"ia",*"iliarii,trs'' separate before §1/§2. No marginal fused into a body line.
  - Qualification: footnote '(t) De instilutione huius festivilalis ... voi. ni, pag. 703.' set as its own block in left column after '... corroboralionem et' (separate, non-blocking).
  - Qualification (misplaced but separate marginal): 'nuiiii concei-' (continuation of the 'Hoc festam ab Orbano IV in- gtitutum, non-' summary) sits after that footnote, before 'exallalionem'.
  - Qualification: running head 'An. C. [liiO lù'ì ItLU.I.AItlDM IlOMANUM Al). C. l'ióO' inline in right column between 'possint prò' and 'conservandis' (non-blocking).
- p.2 — PASS — PNG `2e3ec9b132bc4646b2054da7dc4ea0b92bd93b714ba316c36357a754ef479d1a`. Marginals 'Fesiutnhof in iBcis iilleriiiclo Fupposiiis quo- raodo rci^brin-' and 'rr,n.?iimpiis ...' separate before §3/§5. Closing 'Datimi Romae apnd Sanctos Aposlolos ...' and 'Dui. die 26 niaii 1429'; Source note in left column, license line in right column. 6 marginal blocks in unit; no fusion.
  - Qualification (misplaced but separate marginal): 'nmc Bum™ h™'prà"("""r '« iHiiiiitan' stands between '§ 4. El iiisuper uiiiversos paliiarclias,' and 'arcliiepiscopos', interrupting §4.
  - Limitation: in-column OCR noise '• - • . •. . ■.• ■' (§3) and 'I ' et . . . ^' (§4), body roles.

### `unit-0218.part-01.reading-order` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0218-part-01-reading-order-d850ade4-la/undated-bullarium-volume-04-unit-0218-part-01-reading-order-d850ade4-la.pdf` (SHA-256 `4b93a42a6d999f3a6f8a9e0150b6c4f25dcc85e8af8f9fa111479249e5726020`, 1 pages). Title `Cum  generale  capiliilum  Fratrum  Mi-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 3; none fused.

- p.1 — PASS — PNG `0cb6df45a4925afb0d2ab86f75787b6974b215cb1d781374eda7904e7df86493`. Title/issuer 'Martinus episcopus servus servornm Dei, dilecto'/Latin match; no date. Two columns natural. Marginal 'Cardiudlem S. PetrU(jvi,icaia 'eDMaiir"ra°e- sidtm facit.' separate before the narrative. Closing 'Daluni Romae apnd Sanclos Aposlo- los, oclavo idus innii ...' and 'Dal. die 6 iunii 1430'; source/license notes. 3 marginal blocks; no marginal fusion.
  - Qualification (misplaced but separate marginal): the summary is split by the running head - 'Oppnr dal f«c' before §1 and its continuation 'tuli fxlii' after the running head 'An C. l'iJO 7.>ì lUII.AIIIIIM An. C. 1430' (non-blocking), each a separate block.
  - Limitation: OCR-damaged body words 'no"""' "'' and 'P*^""""^^' at line starts in the first paragraph (word-map body-left, x314+, i.e. 'Mi-/norum' and 'proximo'; adjacent marginal 'Cardiudlem S. PetrU(jvi,icaia ...' ends at x314 and is emitted separately) plus interlinear noise '• ■ • . . 4 • • ■ 1'.

### `unit-0030.reading-order.fragment` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0030-reading-order-fragment-8166b662-la/undated-bullarium-volume-04-unit-0030-reading-order-fragment-8166b662-la.pdf` (SHA-256 `79bb4ced4e255812023f77cd2020636cd17a454efe0fa7c863ed8859424b9f8d`, 4 pages). Title `Fragment: Hospitale  Sancii  Spiritus  in  Saxia  de`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 26; none fused.

- p.1 — PASS — PNG `024cd79c55880d2933999c1174a8fc29e8680694f6de56e343a0dc0c1888ce6b`. Fragment title 'Fragment: Hospitale Sancii Spiritus in Saxia de' and issuer 'Nicolans episcopas servns servorum Dei, dilectis'/Latin match; no date. Source's own omission note '( Omitlilur residuum huius prommii, quia est idem cum procemio bullae Innoc. Ili)' visible in body. Two columns natural. Marginals 'Eiordinm', 'In Urbe e territorio', 'In regno Siti-' separate before their sections; no fusion.
  - Qualification: footnote '(1) De institutione hospitalis vide Innoc. Ili, ...' set as its own block after the SUMMARIUM (separate).
  - Qualification (misplaced but separate marginal): 'Hospiiale bo 5Uh A pa- Irocini ptum' and its continuation 'corum ad illud pertinentium.' (top of right column) are separate blocks; the latter sits after the sentence it annotates.
  - Qualification: running head 'An C \W\ 108 BUILAUIUM UUMANUM An. C. 1291' inline in right column between 'omnibus' and '|jeriineii(iis' (non-blocking); stray marginal mark ''' between 'Asculi,' and 'domos'.
- p.2 — PASS — PNG `c25de4a2037d3d2b6cd61de000a06f2c516b8c2adf5fb1da4b2d96ffede22722`. Two columns natural. Place-name marginals 'In Campania.', 'in thuìcu', 'i„p,„imonin', 'In . Marchia An-', 'in patnar. haiu q». eicn', 'in Burgundi»', 'inLoiiiarinfia.', 'In regno Ale- iianniae.' each separate before its section; no fusion.
  - Qualification: footnote '(1) Ànnelum, alnelum, iocus ubi crescunt alni (Ducangei.' set as its own block in left column between 'quicquid' and 'iuris habelis' (separate).
  - Qualification: running head 'Ali. 0 1201 IV i>i>. ll)!t' inline in right column between 'obli' and 'iielis' (non-blocking).
- p.3 — PASS — PNG `1890b6a65440f1815ff61647a9a37e4d6d8bb1f3ab51775649ec963fa772ebdd`. Two columns natural. Province marginals 'In AngI,;', 'III prOTiDcis ^arbonen.', 'in proTinci» Bitnrie«n.', 'In proTinc ArfìaUn-', 'Io proTÉneia Viennen.', '1= provinci, Tarracon«Die.', 'iD proTiDcia Toietan.', 'Munu* cieri- ...', 'vicmm «i -re- admini^rano"!' qu» sacramcn-', 'Ho.-piiaie s Spirilus in Mon „;pessuiaiioho ...' each separate before its section; no fusion.
  - Qualification: running head 'An. <", noi ' '^ RCILARITM nOMA>r.ii An C. 1291' inline in left column inside §15 between 'Hospitale S. Spiritus de' and 'Sulmaco' (non-blocking).
  - Limitation: in-column OCR noise in §23 ('ho - , "-' „ . • -li', 'r * . * . ...').
- p.4 — PASS — PNG `96fbfc36b823f150a9e7e952fcd2532c02aa30e10f0d3a512906764dfc6a6d95`. Source's own omission note '(Besiduum omi7<i7«r, quia est idem ac in Conslit. Innocenlii HI ...)', marginals 'Pai» >ihscr\-' and 'Calli. I ub^cii- plionec' as separate blocks, papal and cardinal subscriptions, dating 'Datuin apud llrbem Yelerem ...' and 'Dat. die '21 iunii 1291'; Source note continues into right column, license line present. 26 marginal blocks in unit; no fusion.
  - Qualification: running head 'An, C. 1591 MCOl.AUS Ili An. C. U9J' inline in left column between 'bo. meni.' and 'Sleplian.' (non-blocking).
  - Qualification (apparatus): the missing-content notice 'Fragment witness: part of the act is absent from this printing.' is clear, but its locus references ('X12259', 'synopsis12261–12266', 'proem12320–12322', 'residue12767–12769', ... 'end12807') are typeset without a space between label and number and are raw-OCR physical line numbers (ocr-ea5a1bbf8d4f: line 12259 = 'X.', 12807 = the dating line), not the 'reading-order LF lines 12414-12985' named two sentences earlier; the numbering basis is not labeled.

### `unit-0040.reading-order.fragment` — CHANGES_REQUIRED

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0040-reading-order-fragment-a9fa94a6-la/undated-bullarium-volume-04-unit-0040-reading-order-fragment-a9fa94a6-la.pdf` (SHA-256 `04cf7709e0c067dcdf0e597ab7cd33d336362f849811bd8aef12b7d7ac5f325d`, 2 pages). Title `Fragment: Noram  haeresim  in  administratione  sacra-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 5; none fused.

- p.1 — CHANGES_REQUIRED — PNG `586a2affe8cd8dbc2d96f493fb34b4846c143f76a2b1db4954007e275daaf25a`. Fragment title 'Fragment: Noram haeresim in administratione sacra-' and issuer 'Bonifacius episcopus servas servornm Dei, ad perpetnam rei memoriam.'/Latin match; no date. Two columns natural. Marginals 'KfciMias i-a- |,^...', 'ludiciaria »«> ...', 'Hu,u> j.cii- haereiici jam- °"' separate. No marginal fused into a body line.
  - BLOCKING (historical footnote fused into body): left column §1 ends '... quod non- nullae persOHae se conlia sanciam ca- (1) Ex Regest. in Archiv. Vatic. (1) Forsan leiitiilUmihus.' and the body resumes 'iholicam Ecclesiam' after the running head and a marginal - notes run into the body paragraph inside hyphen-split 'ca-/[t]holicam' (derivative LF 16019-16020).
  - BLOCKING (historical footnote fused into body): right column §2 reads '... el talia nefanda credenlibus nul- (l) Deest aiiquid, forsan n rentiam. ctnera- lionem, etc.' then marginal, then 'lum per se' - note run into body inside hyphen-split 'nul-/lum' (derivative LF 16080-16081).
  - Qualification: running head 'An. C. 19% BOMFACIDS Vili PI' li^Ji Ah. C. 1597' inline in left column (non-blocking).
  - Qualification (misplaced but separate marginals): 'Nula '<>"» iraecìiiuafnar- rintur oopiu.' between the running head and 'iholicam'; 'Inqiiiiiloram (tcullt CDQlri • aidem eli. procedendi.' inside hyphen-split 'nul-/lum'.
- p.2 — PASS — PNG `f75b0ce320deafe772d98e78f129869b5dfcca5eab25a056f8588ad600ee4085`. Sparse final page: dating 'Dalum Anagniae, kalendis augusti ...' and 'Dal. die 1 augusti 1296', then Source/license notes with missing-content notice. 5 marginal blocks in unit.
  - Qualification (apparatus): missing-content notice 'Fragment witness: part of the act is absent from this printing.' is clear; its loci 'LF 15884–15888' and 'LF 15845–15846' fall outside the reader's stated reading-order range 15957-16113 (raw-OCR numbering, unlabeled).

### `unit-0110.reading-order.fragment` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0110-reading-order-fragment-0bac7cb0-la/undated-bullarium-volume-04-unit-0110-reading-order-fragment-0bac7cb0-la.pdf` (SHA-256 `691a54e5434926bf3fd13272e90c913f1e6d110479f5959b5a441d7f08e79190`, 1 pages). Title `Fragment: Duin solicilae consideralionis`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 3; none fused.

- p.1 — PASS — PNG `d6f38727384d1ac4a1c13290ff11add4667d1033f9b0a5bc04aaa4f9ddb65b9d`. Single page. Fragment title 'Fragment: Duin solicilae consideralionis' and issuer 'Benedictus episcopus'/Latin match; no date. Body is single short section; closing 'Datum Avenione ...' and 'Dal. die 22 seplembris 1339', source note '(I) Ex Regest. Valic, ...', Source note in left column, license line in right column. 3 marginal blocks; no fusion.
  - Qualification (apparatus): missing-content notice 'Fragment witness: part of the act is absent from this printing.' is clear and the source's own '( Caelera proul in conslitu liane xxviii Ioannis XXI ...)' is visible; locus labels run together with raw-OCR numbers ('XIV54829', 'synopsis54831–54832', 'nextXV54890') outside the stated reading-order range 54990-55045.
  - Qualification: stray marginal marks 'f', 'i» ^"' and ''' as own blocks.

### `unit-0160.reading-order.fragment` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0160-reading-order-fragment-2d24971a-la/undated-bullarium-volume-04-unit-0160-reading-order-fragment-2d24971a-la.pdf` (SHA-256 `31dce1900ffe2a7df9764a58a74f7ea8cda5c82468c7e766265fec9e199fb420`, 2 pages). Title `Fragment: Quod  in  Ecclesia  S.  Ambrosii  ad  Nemm`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 6; none fused.

- p.1 — PASS — PNG `a0a8d0ec4d3103b5c3c4bec068e00814d60a7a2048c0353ac100cdd5ef9339a6`. Fragment title 'Fragment: Quod in Ecclesia S. Ambrosii ad Nemm' and long issuer/address/Latin match; no date. Two columns natural. Marginals 'rrairun. ei«i- còr"'pr7"ói'i'u- ... vitae eondnutt- none;', 'O"™ ...^^s', 'Re^uins .mn- j", "', '„lefw', 'Ai beniRci, ?rc!esi.ist. [<T(ì-' separate before their sections; no fusion. Source's four-dot gap 'bcnefieiuni.... animaium' visible in §9.
  - Qualification: running head 'Ali. C. 1575 GUEGoniiis \i l'I'. 579 An. C. IÓ76' inline in right column between 'El intra' and 'locuni' (non-blocking).
  - Qualification (misplaced but separate marginal): stray mark ''' between 'aposiolicnni convcnit' and 'praebere consensum' as its own block.
  - Limitation: in-column OCR noise ''I . ■ ■ I luincupaliir' (§1).
- p.2 — PASS — PNG `3dae5412da7cdd46d7e341db6347b23f4d7e495eed184de4c75b6d63001d4010`. Sparse final page: end of §9, closing 'Dal. Avenione in kal. decembris ...' and dating line, then Source/license notes. 6 marginal blocks in unit; no fusion.
  - Qualification (apparatus): missing-content notice is clear; its loci 'LF 69497–69498' and 'LF 69509–69511' are raw-OCR line numbers outside the stated reading-order range 69685-69849 (basis unlabeled).
  - Limitation: literal OCR year 'Dal. die 29 novembris 1875' (source date not judged).

### `unit-0173.reading-order.fragment` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0173-reading-order-fragment-fc7fc208-la/undated-bullarium-volume-04-unit-0173-reading-order-fragment-fc7fc208-la.pdf` (SHA-256 `893fd55bb7edc96025a721dc6cdf7c3e0f8ec54273b8ca6e1a5473f2c4d43ce2`, 2 pages). Title `Fragment: Haereticis,  schismaticis  aliisque  a  sacro-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 2; none fused.

- p.1 — PASS — PNG `ff09f27bcd001800d83dac70a7dff1a7cfa03a733db9f015f0d388c64fedcdc9`. Fragment title 'Fragment: Haereticis, schismaticis aliisque a sacro-' and issuer 'Urbanus episcopus servus servorum Dei , ad perpetaam rei memoriam.'/Latin match; no date. Two columns natural. Marginal 'e eniiHen- pi'ofessio- praescrì-' separate before §2. No fusion.
  - Qualification: footnote '(1) Ex Regesl. in Archiv. Valle.' set as its own block in left column between '... ostenrlere , per' and 'quas salubriter' (separate, non-blocking).
  - Qualification: running head 'An. C. 1585 UilBA>US VI l'J>. 595 An. C. 1585' inline in right column inside hyphen-split 'liomi-/iiem' (non-blocking).
- p.2 — PASS — PNG `b1309b762993680e8ed9ed8baf9afbfd86b993462059bd1bbd46c8568768f042`. Two columns natural. Closing '^ 13. Nulli ergo ...', 'Daliim apud Montem Flasconem ...' and 'Dal. die 1 augusti 1385'; source/license notes. 2 marginal blocks in unit; no fusion.
  - Qualification: footnote '(1) Addendum (orsan: nmlieres, nec una nuilier simul habere permitlilur pltires.' and running head 'Ali. C. ió8y J>!)^J IIIIIJ.AKIUM UOMAINUU Ari. C. I38a' set as separate blocks in left column between '... secundas el terlias' and 'el deiiiceps' (non-blocking).
  - Qualification (misplaced but separate marginal): 'ei.us' stands as its own block inside hyphen-split 'anathe-/malizaluin'.
  - Qualification (apparatus): missing-content notice clear; loci 'LF 71519–71520', 'LF 71515', 'LF 71595–71599' are raw-OCR numbers outside the stated reading-order range 71726-72006 (unlabeled basis).

### `unit-0181.part-01.reading-order.fragment` — CHANGES_REQUIRED

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0181-part-01-reading-order-fragment-812e5432-la/undated-bullarium-volume-04-unit-0181-part-01-reading-order-fragment-812e5432-la.pdf` (SHA-256 `27b5e0ff2df2efef030b99dfc45ee440bd66b5db85e1e2aa11427be5eaeddcb9`, 1 pages). Title `Fragment: Confìrmalii)  fon'>lilutio)tum  a  Fiidcricu  Se-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 5; none fused.

- p.1 — CHANGES_REQUIRED — PNG `14369fe8882f21e6eedd1bd80cd3b9f6afc1597e5ba9bcb92e019468859e46c6`. Single page. Fragment title 'Fragment: Confìrmalii) fon'>lilutio)tum a Fiidcricu Se-' and long issuer address/Latin match; no date. Two columns natural. Marginals 'Eiordium', 'Consiituiiones a Friderko II laias coiiiirma- viiHoiioriusiii. '', 'Inilium *'■- tUtiODÌS.', 'causae hanim naodarum.', 'EirumJemde- ,|„„iio' separate before their sections; no marginal fusion. Closing 'Datnm Roinae, 6 kal. iunii ...' and 'Dal. die 27 mali 1391'; source/license notes.
  - BLOCKING (historical footnotes fused into body): left column §4 reads '... ac lolius cleri Brunswi- (1) Leg. Romanorum. (2) Caetera legtintur in Conslil. xLviii Honorii III, lom. ni, par. i, pag. 37'» el. seq. (3) OmitliUir nanatio huius Conslil. Ca- roli IV, ([uia per extensum poiiitur hic in Glie. censis , llildeiiseineiisi.s, ...' - the three page-foot notes are run into the body paragraph inside hyphen-split 'Brunswi-/censis' (derivative LF 74180-74181).
  - Qualification (apparatus): missing-content notice clear; loci ('VI73687', 'synopsis73690–73693', 'body73709–73797', 'references73718/73736', 'begins73804') are run together and are raw-OCR numbers outside the stated range 74111-74229.
  - Limitation: in-column OCR noise '„ ò ii i-' i- r („p^' (§2) and 'jjjg nupcr 1110' (§4).

### `unit-0206.reading-order.fragment` — PASS

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0206-reading-order-fragment-89984e1a-la/undated-bullarium-volume-04-unit-0206-reading-order-fragment-89984e1a-la.pdf` (SHA-256 `4e1c98fb3a1ab2add3d3610225db57b1664a7d554d0de80ffe837511a800ea8f`, 1 pages). Title `Fragment: Privileyiuin  exemplionis  monacar  uni  S.  Be-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 2; none fused.

- p.1 — PASS — PNG `4f99160e5925350559a5dbfa9e59767554d14aed9d794ede8943036bb922589d`. Single page. Fragment title 'Fragment: Privileyiuin exemplionis monacar uni S. Be-' and long issuer address/Latin match; no date. Two columns natural. Marginals 'Exompiio (de qii» 111 rubricu).' before §2 and 'Obsl.iii rogatio' before §3 separate. Closing 'Dalum Romae apiid S. Mariani Maio- rem ...' and 'Dal. die 23 seplenibris 1424'. 2 marginal blocks; no fusion.
  - Qualification: running head 'Ali. C. l'ii'l 708 BIU-AUIUM UOMANUM' inline in left column between proem and §1 (paragraph boundary; non-blocking).
  - Qualification (apparatus): missing-content notice clear and the source's own note '(1) Omiltitur haer, narrativa, quia eadem est in Constit. i.xxiii Honorii III ...' is set as a separate closing note; loci 'LF 85424–85425' and 'LF 85471–85473' are raw-OCR numbers outside the stated range 85871-85962 (unlabeled basis).
  - Limitation: in-column OCR noise '||„|^,|.„„^' (§2).

### `unit-0211.reading-order.fragment` — CHANGES_REQUIRED

PDF `.scratch/typeset_pipeline/claude/bullarium-ro-v04/undated-bullarium-volume-04-unit-0211-reading-order-fragment-ebbe544b-la/undated-bullarium-volume-04-unit-0211-reading-order-fragment-ebbe544b-la.pdf` (SHA-256 `ac67eeac7421f50a39536805bfeb36e7404eb8bc11fe3d8939feeb868dc16b01`, 2 pages). Title `Fragment: Cuntra  cmenies,  rapienles  xeu  alias  quo-`; issuer as printed; `la`; date unknown and correctly omitted. `prior_finding`: none. Marginal blocks in the derivative: 8; none fused.

- p.1 — CHANGES_REQUIRED — PNG `6c3e9f8c558aea027acd5f343262d69f93b2f24322a0219bb719cdf816b29c54`. Fragment title 'Fragment: Cuntra cmenies, rapienles xeu alias quo-' and issuer 'Martinos episcopas servas servorum Dei ,'/Latin match; no date. Two columns natural. Source's own reference '(proul in praecedenli Constil., § 1 )' visible. Marginals 'E.ordiun..', 'causae eden- „'5^ ...', 'chrisiunoss,!- je"|,",„'s ...', 'Banc ' public.ii' separate; no marginal fusion.
  - BLOCKING (historical footnote fused into body): left column §2 reads '... vesligiis inliaerenies, auctori- (I) Ex Regest. in Archiv. Vatic. Consule Ray- naldum, ann. l'»25.' then running head, then 'tntc apostolica' - note run into body inside hyphen-split 'auctori-/[ta]tntc' (derivative LF 87538-87539).
  - Qualification: running head 'An. C. l'l2o MAIITINDS 721 An. C. 1425' inline in left column and signature 'Bull. Rom. Voi. IV. 91' inline in right column between 'in locis' and 'singulis' (non-blocking).
  - Qualification (misplaced but separate marginals): stray 'I' blocks inside §1 ('aliis'/'illis') and §2 ('incidere'/'slaiuerunl'); '""' inside the title rubric.
- p.2 — PASS — PNG `cfcfd6d02a453130308dc855f8cd5280768045c579157c2c7582699ad3984c33`. Sparse final page: end of §4 'eamdem noverint se ligalos.', 'Nulli ergo omnino etc.', 'Datum Romae, apud Sanctos Apostolos tertio nonas iunii, anno octavo.', 'Dat. die annoque eodem.', then Source/license notes. 8 marginal blocks in unit.
  - Qualification (apparatus): missing-content notice clear; loci run together with raw-OCR numbers ('XVII87013', 'section1 stops87050', 'cross-reference87051') outside the stated range 87465-87624 (unlabeled basis).

## Cross-cutting qualifications (non-blocking)

- Running heads (`An. C. ... BULLARIUM ROMANUM ...`) and printer signature marks (`Bull. Rom. Vol. IV. NN`) stay inline at page boundaries, often between the halves of a hyphen-split word. The series standard makes this non-blocking; each locus is recorded per page. One signature mark (`unit-0215` p.2, `posl- Bidl. Rom. Vul. IV. 'Ò'I`) runs on at the end of a body line instead of starting its own block.
- Separate marginal blocks that interrupt a sentence, or sit inside a hyphen split, are emitted at their own line anchors. They are qualifications, and each locus is recorded.
- Interlinear OCR glyph noise (bullets, `■`, stray letters) sits inside body columns with body roles. In `unit-0162` p.1, two such strings lie on the same baseline as an adjacent marginal block and fall inside a hyphen split (`Came- r ' ì ■ ■■ 1 / ram`; `spccia- "^ , ...,'. / lem`). They contain no summary wording, so they are recorded as OCR noise rather than marginal fusion. They are worth a glance from the tool owner.
- Fragment readers (`unit-0030`, `0040`, `0110`, `0160`, `0173`, `0181.part-01`, `0206`, `0211`) all show a `Fragment:` title and the clear notice 'Fragment witness: part of the act is absent from this printing.', followed by a description of what is missing. In every one, though, the locus numbers in that description are raw-OCR physical line numbers (e.g. `unit-0030`: OCR line 12259 = `X.`), not the reading-order 'LF lines' range given two sentences earlier, and the basis is not labeled. Several are also run together with their labels (`X12259`, `synopsis12261–12266`, `nextXV54890`). This is non-blocking but misleading apparatus.
- Several readers have sparse final pages. Each carries a genuine source dating line before the project notices (e.g. `unit-0200` p.2: `D;it. die 17 oclobris 1418`). None is a notice-only page. No modern digitizer signature, `None` placeholder, clipping, overlap or tofu glyph was seen.

## Limitations

- Literal, uncorrected, uncollated historical OCR; odd spellings, OCR noise and literal source dates are limitations, not defects.
- Layout review of the reviewed PDF bytes only; no word-level collation, image-level collation against the 1859 facsimile, historical authentication, publication, installation or deployment claim.
- Marginal-block count and fusion checks were cross-checked mechanically against the reading-order derivative (TAB-led blocks) and its word map (roles, coordinates); the derivative is evidence, not an independent finding of this lane.

This report does not authorize installation and makes no claim of installation, deployment, historical authentication or publication.
