# Gregory XVI Acta visual review 04 — batch gregory-0003, lane 4 (re-issue)

**Re-issue.** This report supersedes the first issue (SHA-256 `71a02bf28917dc2826bc6eeb9f2f589a0e1163a55fac6f353c09c6854b074f35`). It applies the coordinator's ruling on edition notes in Gregory readers:

- **Non-blocking:** the edition's own notes set as separate blocks where the source page breaks, even when a body sentence or hyphenated word resumes after them.
- **Blocking:** note text sharing a printed line with body words, or note lines interleaved line by line with body lines.
- **Blocking for Gregory readers:** a folio number or running head left in the body.

All three pages of `line-00018174` were re-opened at full size for this re-issue. No other page needed re-opening. The first-issue page ledger is kept as `observations-initial.jsonl`.

**Result: 43 PASS, 1 CHANGES_REQUIRED** of 44 assigned PDFs; 65 pages, every one individually opened full size; zero reused pages. All documents come from Gregory XVI Acta volume 3 (1841-03-23 to 1842-01-07). No assigned document carried a prior finding.

CHANGES_REQUIRED:

- `gregory-xvi-acta.volume-03.line-00020298.part-04` (*Perlatum ad Nos est*, 1841-07-17, 5 pages), blocking on pages 1, 3 and 4. The edition's page furniture is left in the body:
  - Folio "147" shares a line with body words on page 1, left column ("147 frater, ut clero ...").
  - Folio "149" sits inside the word "vige-/sima" on page 3, right column.
  - The volume running head "ACTA GREGORII PP. XVI." interrupts a body sentence on page 4, right column ("scissionis," / "nisi Michaelem").

  Its edition notes (note 1 and the footnote blocks on pages 1–5) are set as separate blocks at source page breaks. Under the ruling they are now non-blocking qualifications.

Changed from the first issue:

- `gregory-xvi-acta.volume-03.line-00018174` (*Ex literis*, 1841-05-04, 3 pages) is now **PASS with qualifications**. The re-check found no printed line that mixes note and body words, and no line-by-line interleaving.
  - The Italian Propaganda letter, printed as the act's note 2, is set as separate blocks at source page breaks.
  - The Latin body block ends "in Do-" on page 1 and resumes as its own block "mino commendamus" on page 2.
  - Note 2 resumes as its own block "tico modo" after the papal Datum Romae clause.
  - A display qualification remains: the title-line language label ends "printed as note2", with no space before the 2.

## Scope and method

The scope was lane 4 of batch `gregory-0003`, the assignment at `.scratch/claude-review/gregory-0003/lane-04/assignment.json`, SHA-256 `3c5bc95b76f9e5230ceb0b19e76c00addf638439e821ea0a570cafb6712f9e37`. Each page PNG produced by the repository `pdf-review` tool was opened individually at full size with the Read tool, one image per page, with no contact sheets and no re-rasterization. Each page's displayed title, responsible issuer, date and language were compared with the frozen metadata. Each page was also checked for:

- heading and two-column flow, gutters and margins
- glyphs, including clipping, overlap and tofu
- natural source closing and terminal apparatus
- modern digitizer signatures
- running heads or folios fused into body sentences
- marginal or foot notes fused into body sentences
- raw placeholders

No digitizer signature (for example "Digitized by Google"), raw `None` placeholder, clipping, overlap or missing-glyph block was found on any page. Every final page carries a genuine source closing (dating clause or the allocution's closing invocation), not just project apparatus.

Standing coordinator rulings applied as non-blocking qualifications:

- `line-00020184` (consistorial allocution) displays the volume running-title issuer "ACTA GREGORII PP. XVI.".
- `line-00017391` displays the OCR-damaged running-title issuer "ACTA GREGORIT PP. XVI.".
- `line-00024652.part-01` displays "GREGORIUS PP. XVI. :" with a stray OCR colon.
- `line-00018575` and `line-00021663` display "GREGORIUS PP. XVI" without a final period.
- `line-00024500` is in Italian. Its issuer line is the letter's own OCR-damaged Italian superscription ("... successore dis. Pietro, @ mandata"). This matches the frozen metadata and is disclosed in the apparatus.

All of these match the frozen metadata and identify Gregory XVI.

Four documents leave a column partly empty before the next paragraph starts on the following page: `line-00076989` p. 1, `line-00024287` p. 1, `line-00025194` p. 2 and `line-00027004` p. 1. Nothing is clipped or overlapping. These are recorded as non-blocking whitespace qualifications.

## Evidence verification

Before and after inspection, every assigned PDF, the receipt, the frozen manifest, the raster-run record and every page PNG was rehashed: 112 files in all. Every digest matched its assignment pin both times, and the before and after records are identical.

| Evidence | Path | SHA-256 | Verification |
| --- | --- | --- | --- |
| Render receipt | `.scratch/typeset_pipeline/claude/gregory-0003/receipt.json` | `577919974e1a28297556b1831218679f679e3d9ca177dfdb0e06dd61d494cdd0` | Before and after |
| Frozen manifest | `.scratch/typeset_pipeline/claude/gregory-0003/frozen-manifest.json` | `a6a2848a84eff686f984d05e2707ab592b0119dd621858fdd034a0b38dca65d0` | Before and after |
| Raster run | `.scratch/claude-review/rasters-gregory-0003/review-run.json` | `d604d73b069c67a6adfc51aa429515f56b8d1f225b32cfda61a4b4adefc4f6ec` | Before and after |
| Verification before | `.scratch/claude-review/gregory-0003/lane-04/verification-before.json` | `e29018ade77ae5c3d4c35be2e4242f820a344d68f75b7db8ab6ce05772db2c41` | all_match = true |
| Verification after | `.scratch/claude-review/gregory-0003/lane-04/verification-after.json` | `e29018ade77ae5c3d4c35be2e4242f820a344d68f75b7db8ab6ce05772db2c41` | all_match = true; identical digests |
| Observation ledger (re-issue) | `.scratch/claude-review/gregory-0003/lane-04/observations.jsonl` | `0de63d8389fc4065352700e7b7e7973fdbfede59ca7c409fc4e9a8b93d12924d` | 65 unique page observations |
| Observation ledger (first issue) | `.scratch/claude-review/gregory-0003/lane-04/observations-initial.jsonl` | `57d74461ee8de5b6018b8d93914558a9cd0895d5ce80eea90336c8c9ffe3ce4a` | Preserved |

## PDF outcomes

| Source ID | Date | Language | Issuer line | Pages | Pages inspected | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gregory-xvi-acta.volume-03.line-00016578` | 1841-03-23 | `la` | GREGORIUS PP. XVI. | 2 | 1, 2 | `768152ec4c7efc914c20ef322ce25b6ac4c2ed90f446e73447c9f04e3b082907` | PASS |
| `gregory-xvi-acta.volume-03.line-00016831` | 1841-03-26 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `4db22f1061621b963256cb74e13a966e2cedda5054cffc7afee6e831d221afb3` | PASS |
| `gregory-xvi-acta.volume-03.line-00017212` | 1841-04-05 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `05f2a89ee0a5678aea4d0a05a36ff966a3b78020f953158b9209cadb77c63171` | PASS |
| `gregory-xvi-acta.volume-03.line-00017269` | 1841-04-07 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `513d534df930b6e18a027e0cd6f1504c1487f93e767017429f6ea4e26e2b7959` | PASS |
| `gregory-xvi-acta.volume-03.line-00017391` | 1841-04-07 | `la` | ACTA GREGORIT PP. XVI. | 1 | 1 | `947d60d865702a0381822ae11c57b3226616534fd86410635bda06f7bf0990ea` | PASS |
| `gregory-xvi-acta.volume-03.line-00017480` | 1841-04-19 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `03569fbbd216cc7ae685584527c3ff36ce96a8ca2c49390c26fe35e43ca08962` | PASS |
| `gregory-xvi-acta.volume-03.line-00017542` | 1841-04-30 | `la` | GREGORIUS PP. XVI. | 3 | 1, 2, 3 | `a0f30cae67a22d74f3e647526ec98bb413ce51910e31360b1955a7379c0ea014` | PASS |
| `gregory-xvi-acta.volume-03.line-00017863` | 1841-04-30 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `b77a3c48c741ad107a2bc6f3ba35ab742a911e6f41f57717e9eee1337409c296` | PASS |
| `gregory-xvi-acta.volume-03.line-00076989` | 1841-04-30 | `la` | GREGORIUS PP. XVI. | 2 | 1, 2 | `28310ff2f984d108e6200261cbf562b20c5e77ee321b4cf53d33877fca7bf635` | PASS |
| `gregory-xvi-acta.volume-03.line-00018174` | 1841-05-04 | `mul` | GREGORIUS PP. XVI. | 3 | 1, 2, 3 | `34c175dbf568e29ef74e27b9d403edb10a3cf515f6882e3ec953daf5106d7b58` | PASS |
| `gregory-xvi-acta.volume-03.line-00018412` | 1841-05-04 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `519c45dfb78d0a847e72acf4ec551e7d92c035d7195966640e638c78aee4ac0f` | PASS |
| `gregory-xvi-acta.volume-03.line-00018502` | 1841-05-10 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `eed1fb163508a38a69e561d48463dd54c94f1d7964ded6bf08320128909a450b` | PASS |
| `gregory-xvi-acta.volume-03.line-00018575` | 1841-05-17 | `la` | GREGORIUS PP. XVI | 1 | 1 | `ed3121a0c5ed51e718bbb2ca4ac2cc008ff93693a77532e6dbb76eaf5e03c021` | PASS |
| `gregory-xvi-acta.volume-03.line-00018658` | 1841-05-18 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `8c0402d66f5767f569889a9a0470617dee263567900c79cf424eb90e0106d046` | PASS |
| `gregory-xvi-acta.volume-03.line-00018746.part-01` | 1841-05-19 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `8b6d8abb11a00e119a6d9e0153a2fffa43412a784b703c5d56f98cf5be7db74b` | PASS |
| `gregory-xvi-acta.volume-03.line-00018746.part-02` | 1841-05-21 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `37fd2e3a116ae382aa776354b64f2020ce544934f4708ae6586d082a705640c7` | PASS |
| `gregory-xvi-acta.volume-03.line-00018930` | 1841-05-21 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `fabc91515c53289cbe5bf531fd1ad2533107940c796c677d84a2c34267a66ffb` | PASS |
| `gregory-xvi-acta.volume-03.line-00019224` | 1841-06-08 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `94391521d4fe13befa6f590f1bb67f005e79b6124aab25560d92660fd5dd737b` | PASS |
| `gregory-xvi-acta.volume-03.line-00019332` | 1841-06-08 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `7161f3c388aac8bf5a1abba8dfe862c8ab20f420d135a33c699ebd9574ee01c9` | PASS |
| `gregory-xvi-acta.volume-03.line-00019431` | 1841-06-11 | `la` | GREGORIUS PP. XVI. | 2 | 1, 2 | `d89956ea80e286b28630dff857932d2b6cce3b700d823689aebb38875f7d6ea6` | PASS |
| `gregory-xvi-acta.volume-03.line-00019630.part-01` | 1841-06-18 | `la` | GREGORIUS PP. XVI. | 2 | 1, 2 | `108e3b1b95eb2bfef2da3ce3b45924521bea5fcf9aeb11b2d7edac3943e49b6b` | PASS |
| `gregory-xvi-acta.volume-03.line-00020068` | 1841-07-06 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `33984cccfa3be70fb26d13f47bb365b8f5d97ec7e4c7f673ca8f275e0cf016c2` | PASS |
| `gregory-xvi-acta.volume-03.line-00020184` | 1841-07-12 | `la` | ACTA GREGORII PP. XVI. | 1 | 1 | `9112d9cf26b388f99ee434def98fde5cc9e5f28ced2c9c91c1ef2ffcf45bf60a` | PASS |
| `gregory-xvi-acta.volume-03.line-00020298.part-01` | 1841-07-13 | `la` | GREGORIUS PP. XVI. | 2 | 1, 2 | `00b59c63150389e6ee3027bb1a0b5480c67c257952bc313bdd04f989696febc4` | PASS |
| `gregory-xvi-acta.volume-03.line-00020298.part-02` | 1841-07-15 | `la` | GREGORIUS EPISCOPUS | 3 | 1, 2, 3 | `dfd20ded56d548903d0b9d9c05b86a9843354f4b20cf4a196d98993d5648b080` | PASS |
| `gregory-xvi-acta.volume-03.line-00020298.part-03` | 1841-07-16 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `0689d3171ff33bc7aacae0b8c88505753a5eb123e98d7efec776302b6d445254` | PASS |
| `gregory-xvi-acta.volume-03.line-00020298.part-04` | 1841-07-17 | `la` | GREGORIUS PP. XVI. | 5 | 1, 2, 3, 4, 5 | `7a999f1967a075fbbf0863405a8d164ccec6a9636acf4f3778922b9c0d66abd7` | CHANGES_REQUIRED |
| `gregory-xvi-acta.volume-03.line-00021663` | 1841-07-27 | `la` | GREGORIUS PP. XVI | 1 | 1 | `af6e73273e58d53ced0a7584d84b853a0fc2f0d811be826d95a88805b051c2ff` | PASS |
| `gregory-xvi-acta.volume-03.line-00024436` | 1841-08-19 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `0b8fd26c8440c447a3afd7b8b62b0c515f1ae6058fcb1d87657de6a91ac885c6` | PASS |
| `gregory-xvi-acta.volume-03.line-00024287` | 1841-08-22 | `la` | GREGORIUS PP. XVI. | 2 | 1, 2 | `7db82ea1115611457edfcbc995f91c757076bf94ac382c0d340bba142d10f902` | PASS |
| `gregory-xvi-acta.volume-03.line-00024500` | 1841-08-29 | `it` | Questa lettera del Pontefice Massimo di Roma, successore dis. Pietro, @ mandata | 1 | 1 | `4afef28c064c31d748051441a79c16518537d1b9b32a7a2745e00ee552ffc483` | PASS |
| `gregory-xvi-acta.volume-03.line-00024551` | 1841-09-10 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `c51cfa867e49ab944120a9b60a47d6f852475e41b81b02324aeb3f69c0384fe5` | PASS |
| `gregory-xvi-acta.volume-03.line-00024652.part-01` | 1841-09-17 | `la` | GREGORIUS PP. XVI. : | 1 | 1 | `d13cb57561635fa47d549d44c7c93088be8a7ec194a17564ec867580fc817020` | PASS |
| `gregory-xvi-acta.volume-03.line-00024905` | 1841-09-24 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `178a1ce9f768be12051e03ad4ca1644bfed40d5ab0f539e1ec7989847d201cfb` | PASS |
| `gregory-xvi-acta.volume-03.line-00025003` | 1841-09-24 | `la` | GREGORIUS PP. XVI. | 2 | 1, 2 | `2f324b5d6cc79b0a2e6901d0a6a37ad3aa38c217fae5156ca2823ef1e8c90ffc` | PASS |
| `gregory-xvi-acta.volume-03.line-00025194` | 1841-10-01 | `la` | GREGORIUS EPISCOPUS | 3 | 1, 2, 3 | `0cf13ba9db9aeb95149502dc027b9171c89b6f3354b997ba3d0a0a1d1d3a778b` | PASS |
| `gregory-xvi-acta.volume-03.line-00025470` | 1841-10-16 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `44a231b7199c736d8afca6ff8e08a10b3510464c7287b0a0220eb4c3073a09be` | PASS |
| `gregory-xvi-acta.volume-03.line-00025543` | 1841-10-31 | `la` | GREGORIUS PP. XVI. | 2 | 1, 2 | `05ab27c1ebdbd75af1a6f12caef2d24260fca5a1439925525d314b73a187b2e2` | PASS |
| `gregory-xvi-acta.volume-03.line-00025806` | 1841-11-12 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `528a2f5befdb236dd0f861551fe4438e73057b11feae840a6402baa0e32c9a5e` | PASS |
| `gregory-xvi-acta.volume-03.line-00025868` | 1841-11-22 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `67352796ab7284c8202d85be1d12a6c2eaea40685ccccd6420935a934bf26a6f` | PASS |
| `gregory-xvi-acta.volume-03.line-00026718` | 1841-12-17 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `97dfa2fe1ae3313c8721b70378cb733548c6186ce63a5007679b174d0392857e` | PASS |
| `gregory-xvi-acta.volume-03.line-00026803.part-02` | 1841-12-23 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `3ae05ecdf57675bca90ba252e83ec3ae5901f84394895d4a46924bc8a697e11a` | PASS |
| `gregory-xvi-acta.volume-03.line-00026941` | 1842-01-03 | `la` | GREGORIUS PP. XVI. | 1 | 1 | `780da2da28319f4c79e43c3bfc4039b747c8537d1d2947c25853674f67a7caeb` | PASS |
| `gregory-xvi-acta.volume-03.line-00027004` | 1842-01-07 | `la` | GREGORIUS PP. XVI. | 2 | 1, 2 | `f9a47d44c3f01adc0ab2ff3665535cc79e54d84233f04b868592147d3c267589` | PASS |

## Per-document page findings and PNG hashes

### `gregory-xvi-acta.volume-03.line-00016578` — PASS

*In supremo episcopatus culmine — De custodia Terrae Sanctae et vicariatibus Syriae et Aegypti* · GREGORIUS PP. XVI. · 1841-03-23 · Latin · motu-proprio

- Page 1 (`4c9084f4043bc74c441a92e8e2fe928512e3d364b41b7f0897983e4fb043bc99`): **PASS**. Title, GREGORIUS PP. XVI., 1841-03-23, Latin match metadata; two columns clean; no furniture or digitizer marks.
- Page 2 (`c86e5035d31e13a06533ee69f43ea9813fb3e878d9cd008a21658da6b7d9d786`): **PASS**. Body continues to Datum Romae dating clause; Source and rights apparatus follow body on same page; columns and margins clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00016831` — PASS

*Cum Nobis nihil potius — Congregatio Presbyterorum Adoratorum Sanctissimi Cordis Iesu Tolosana commendatur* · GREGORIUS PP. XVI. · 1841-03-26 · Latin · apostolic-letter

- Page 1 (`77d8b724ca15b2dcd60e6681a8887832ce7d7eec605024733418010fdfaeaed0`): **PASS**. Title/issuer/date/Latin match; two columns; Datum Romae closing then Source/rights apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00017212` — PASS

*Quaecumque illa sint — Ferdinando regi utriusque Siciliae de nato filio* · GREGORIUS PP. XVI. · 1841-04-05 · Latin · papal-letter

- Page 1 (`cf8a86ab721f96cee18c28f841d750e96b20b08456ffabec577635c84756f16e`): **PASS**. Title/issuer/date/Latin match; short letter set in left column only, ends with Datum Romae and apparatus; right column empty (sparse but source-bearing); clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00017269` — PASS

*Magna cum animi voluptate — Nicolao Russiarum imperatori de catholicis libere religionem profitendi* · GREGORIUS PP. XVI. · 1841-04-07 · Latin · papal-letter

- Page 1 (`b8bc9de5d79d76b0f0c0a308a39f1b1e5a0376ddbbd1932c7089801641d909fb`): **PASS**. Title/issuer/date/Latin match; two columns; Datum Romae closing then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00017391` — PASS

*Memores officii — Marcello Gutkowski episcopo Podlachiensi de sede abdicanda* · ACTA GREGORIT PP. XVI. · 1841-04-07 · Latin · papal-letter

- Page 1 (`729deb1921b4f444d4c58a2cd53f8c8b957a29c9a2d71abf354301ea17c1fcb9`): **PASS**. Issuer line reads ACTA GREGORIT PP. XVI. (volume running-title attribution, OCR-damaged) matching frozen metadata: non-blocking qualification; date/Latin match; two columns; Datum Romae closing carries into right column then apparatus; clean.
  - Qualification (non-blocking): issuer displayed as running-title attribution ACTA GREGORIT PP. XVI., matching frozen metadata and identifying Gregory XVI.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00017480` — PASS

*Ad regiam tuam maiestatem — Carolo Alberto Sardiniae regi de nuntio Thoma Paschali* · GREGORIUS PP. XVI. · 1841-04-19 · Latin · papal-letter

- Page 1 (`3d5f12221c5a6237b87a6ae69ee9600b427f80e97c288ec937c280239c716edc`): **PASS**. Title/issuer/date/Latin match; short letter in left column with Datum Romae closing and apparatus; literal OCR stray bar after omnino is source OCR; clean layout.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00017542` — PASS

*Quas vestro et communi — Praesulibus Hungariae de matrimoniis mixtis* · GREGORIUS PP. XVI. · 1841-04-30 · Latin · papal-letter

- Page 1 (`fa72a269008c2405ea6bfb006fde464871c3aec1dcf46450aaa34d86e9ca94de`): **PASS**. Title/issuer/date/Latin match; address, salutation and body in two columns; clean.
- Page 2 (`f57679b3d89bc5d1369397c7491baa5d5d1c14a97564844cf3805d00f4eb2008`): **PASS**. Body continues in two columns including quoted Pius VI responsio; no furniture fused; clean.
- Page 3 (`f49e699d7b6fe35124018d574d278edc3801c0b8dab0e2ba5460f71d70659213`): **PASS**. Body conclusion, Datum Romae dating clause, then apparatus; sparse but source-bearing final page.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00017863` — PASS

*Universi dominici gregis salus — Iosepho Rosati delegatus apostolicus apud rempublicam Haitarum* · GREGORIUS PP. XVI. · 1841-04-30 · Latin · apostolic-letter

- Page 1 (`19c8592fb204c845bdf6ef2613b6c650f2dcc8c4a4460da0725813a444e288f0`): **PASS**. Title/issuer/date/Latin match; two columns; Datum Romae clause continues to right column then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00076989` — PASS

*Quantum christianae reipublicae intersit — Francisco IV Mutinae duci de foro ecclesiastico et de beneficiorum administratione* · GREGORIUS PP. XVI. · 1841-04-30 · Latin · papal-letter

- Page 1 (`e649756ce676db8f5ec8e99d886c1c73ffa9dbfe1fbd6c85fc3d94bcd41255d4`): **PASS**. Title (three lines)/issuer/date/Latin match; two columns; right column ends about two-thirds down before the final paragraph moves to page 2 (non-blocking whitespace, no clipping or overlap); clean.
  - Qualification (non-blocking): page 1 right column leaves lower third blank before final paragraph continues on page 2.
- Page 2 (`4073bd72b2cacc73ccab5b9aad789754b104d926a7a87ebebbc067b9bcebbfcc`): **PASS**. Final blessing paragraph and Datum Romae dating clause, then apparatus with disclosed literal etc. abbreviation note; source-bearing final page.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00018174` — PASS

*Ex literis — Dionysio Augusto archiepiscopo Parisiensi de nova societate pro missionibus Europaeis* · GREGORIUS PP. XVI. · 1841-05-04 · Multilingual · papal-letter

- Page 1 (`293767bebbdedbf262969b0be476b8ad8c8a2624b43870143c41b44efc5e2e07`): **PASS**. Re-opened after coordinator ruling. Title/issuer/date match; multilingual label. Latin body paragraph ends at the source page break with 'etiam atque etiam in Do-'; note 2 (Italian Propaganda letter) then begins as its own separate block(s) ('2 Litterae cardinalis Franzonii ...', 'Al? Ilo Sig. Mons. Augé ...', 'Sonosi quasi ...') and runs through the right column. No printed line mixes note and body words.
  - Qualification (non-blocking, coordinator edition-note ruling): page 1, left column lower half to right column: edition note 2 (Italian Propaganda letter) set as separate blocks at the source page break, in source order; Latin body word 'Do-/mino' resumes in its own block on page 2.
  - Qualification (non-blocking, display): title-line language label reads '... Italian Propaganda letter printed as note2' (no space before 2).
- Page 2 (`6aeb12ab0af3a8aa93b0753e02a6582d3365f3903b669b9281829d9760c39b97`): **PASS**. Re-opened after coordinator ruling. Left column: note block ends 'nel migliore e pil auten-'; Latin body resumes as its own block 'mino commendamus ...' through the Datum Romae dating clause; note resumes as its own block 'tico modo, quali le risoluzioni ...' and continues through the right column. Block-level switches at source page breaks only; no line-by-line interleaving.
  - Qualification (non-blocking, coordinator edition-note ruling): page 2, left column: body block (with Datum Romae clause) sits between note-2 blocks at the source page break ('auten-' / 'tico modo'); separate blocks in source order.
- Page 3 (`00e0ce70db0941427159e18457fe4b8fc54bf468c026dc517ee3b3e4710cc57d`): **PASS**. Re-opened after coordinator ruling. Tail of note 2 ending 'E qui con sentimenti di sincera distintissima stima....' as its own block, then apparatus disclosing the non-papal annex note; papal dating clause is on page 2. No layout defect.
  - Qualification (non-blocking, coordinator edition-note ruling): page 3: final page carries the remaining separate note-2 block after the papal dating clause, as the edition's own note in source order; apparatus discloses it.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00018412` — PASS

*Omnium saluti paterna charitate intenti — Altare privilegiatum societatis S. Mariae in Monterone* · GREGORIUS PP. XVI. · 1841-05-04 · Latin · apostolic-letter

- Page 1 (`261750bfd7f84ce7fc8ce8ddb994568461f4eb37d0915228b80d7d6845d1da54`): **PASS**. Title/issuer/date/Latin match; short act in left column with clauses, Datum Romae and apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00018502` — PASS

*Maxime Nobis cordi est — Petro imperatori Brasiliae de internuntio Ambrosio Campodonico* · GREGORIUS PP. XVI. · 1841-05-10 · Latin · papal-letter

- Page 1 (`3ff4e4f4bc308eac2be5fcc0f2e113ce38f53f3862c5143c83694f7de4849a5e`): **PASS**. Title/issuer/date/Latin match; letter in left column with Datum Romae closing; Source note in left column, rights line flows to top of right column; single-page, no clipping.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00018575` — PASS

*Nullis explicari verbis — Mariae Portugalliae reginae de legato vicecomite De Carreira* · GREGORIUS PP. XVI · 1841-05-17 · Latin · papal-letter

- Page 1 (`7a18cc59b81b1b136fc506419385e7087917bd3cff46d21c5fd599e27b943d36`): **PASS**. Title/issuer GREGORIUS PP. XVI (no final period, matches metadata)/date/Latin match; Datum Romae closing; Source apparatus breaks across columns into right column; no clipping.
  - Qualification (non-blocking): issuer spelled GREGORIUS PP. XVI without final period, matching frozen metadata.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00018658` — PASS

*Cum Romano Pontifici nihil gratius — Sodalitas Angelorum Friburgi in archisodalitatem erigitur* · GREGORIUS PP. XVI. · 1841-05-18 · Latin · apostolic-letter

- Page 1 (`750d2ed0b189fb9109ae47172adbc316f80fdf6311c689facdc4e791dd72b4dc`): **PASS**. Title/issuer/date/Latin match; two columns; non obstantibus clause and Datum Romae closing then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00018746.part-01` — PASS

*Inter praecipuas curas — Lucae et Marco e comitibus Passi de instituto Sanctae Dorotheae* · GREGORIUS PP. XVI. · 1841-05-19 · Latin · papal-letter

- Page 1 (`cfde441de78986eeb58ff0be98c08d711a15c47a2f7ab862ddb70b33572f206a`): **PASS**. Title/issuer/date/Latin match; two columns; Datum Romae closing then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00018746.part-02` — PASS

*Postquam inscrutabili — Theresiae Verzeri de confraternitate Sacri Cordis Iesu erigenda* · GREGORIUS PP. XVI. · 1841-05-21 · Latin · indult

- Page 1 (`7140a3e08b18c0a0e2d7f7148aa606de436baf4edfdb439ba0038786d81d8ac7`): **PASS**. Title/issuer/date/Latin match; left column carries full act; dating clause ends at top of right column ('primo.') followed by apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00018930` — PASS

*Romano certe decet Pontifici — Indulgentiae instituti Filiarum Sacri Cordis Iesu in Gallia Cisalpina* · GREGORIUS PP. XVI. · 1841-05-21 · Latin · indult

- Page 1 (`cc428ef80fb991eb18e03f4f763f2e11570fe6fd0de2913bbcbdd97d7fe07dad`): **PASS**. Title/issuer/date/Latin match; left column act with Datum Romae closing and Source note; revision/rights lines continue at top of right column; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00019224` — PASS

*Piorum hominum societates — Sodalitas S. Mariae in Monterone in archisodalitatem erigitur* · GREGORIUS PP. XVI. · 1841-06-08 · Latin · apostolic-letter

- Page 1 (`51b6a1049e0aba06334973b0150bddaa2300476d2da09454a47d71bd6fe11597`): **PASS**. Title/issuer/date/Latin match; two columns; non obstantibus clause and Datum Romae closing then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00019332` — PASS

*Romani Pontifices provido sane consilio — Insignia canonicorum cathedralis Papiensis* · GREGORIUS PP. XVI. · 1841-06-08 · Latin · indult

- Page 1 (`889f7e48014144dfce19f7bfd3df2bffc8973680b531221927c9a0126014c118`): **PASS**. Title/issuer/date/Latin match; two columns; non obstantibus clause and Datum Romae closing then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00019431` — PASS

*Cum, divino edocente Spiritu — Institutum Filiarum Sacri Cordis Iesu Bergomi approbatur* · GREGORIUS PP. XVI. · 1841-06-11 · Latin · apostolic-letter

- Page 1 (`4f4da74f9d3546df42554f25851110069b658770be8f79ce06390e6d9c9bc34e`): **PASS**. Title/issuer/date/Latin match; dense two-column body; no furniture or digitizer marks; clean.
- Page 2 (`0e900c8e96c574449146ce84ee373d95b8177eb9c96d9fd92d9a3ae0211c8dc3`): **PASS**. Body conclusion, non obstantibus clause, Datum Romae dating clause, then apparatus in left column; source-bearing final page.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00019630.part-01` — PASS

*Romanum certe decet Pontificem — Translatio cathedralis Lincensis ad ecclesiam Sancti Ignatii confirmatur* · GREGORIUS PP. XVI. · 1841-06-18 · Latin · apostolic-letter

- Page 1 (`768c1ba33f10b550b6495725dd4098b13f6d188363240215c3a9ba16f2f57da2`): **PASS**. Title/issuer/date/Latin match; two full columns; body through non obstantibus clause; Datum Romae begins at foot of right column; clean.
- Page 2 (`9e8e0a61dc6ac0c9acb608c9edcd3d97016e7cd2620db8ca1c284baff71b2b18`): **PASS**. Sparse final page holds the remainder of the genuine Datum Romae dating clause followed by apparatus; source-bearing.
  - Qualification (non-blocking): sparse final page carries only the tail of the dating clause plus apparatus; genuine source closing present.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00020068` — PASS

*Cum in vinea Domini — Institutum congregationis Oratorii Sancti Philippi Nerii Leonensis in Mechoacan confirmatur* · GREGORIUS PP. XVI. · 1841-07-06 · Latin · apostolic-letter

- Page 1 (`c95e5752a829f3bc7f76deae48b718493313955feb2ed164536f86f066d1fd02`): **PASS**. Title/issuer/date/Latin match; two columns; Datum Romae apud s. Mariam Maiorem closing then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00020184` — PASS

*Maximi sane momenti — Allocutio de Silvestro Belli cardinali declarando* · ACTA GREGORII PP. XVI. · 1841-07-12 · Latin · consistorial-allocution

- Page 1 (`3a330f762e133e7d1f6ae871b11a01da6056f04a22bb5a0f85948b1506f1c3fa`): **PASS**. Consistorial allocution; issuer line ACTA GREGORII PP. XVI. from volume running title matches metadata (standing ruling: non-blocking qualification); date/Latin match; two columns ending with invocation and Amen; apparatus discloses no dating clause, date from excluded caption.
  - Qualification (non-blocking): issuer displayed as running-title attribution ACTA GREGORII PP. XVI. per standing allocution ruling, matching frozen metadata.
  - Qualification (non-blocking): allocution has no dating clause; apparatus discloses date taken from excluded edition caption.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00020298.part-01` — PASS

*De spirituali christifidelium bono — Canonicatus presbyteralis in collegiata oppidi Rotella erigitur* · GREGORIUS PP. XVI. · 1841-07-13 · Latin · apostolic-letter

- Page 1 (`5000a6b8da2662b01a9e2b07d062b5f6db4869f9b335d967ad418edb2260e5da`): **PASS**. Title/issuer/date/Latin match; two full columns of body; clean.
- Page 2 (`42fd941871a895a0eb4c73386510d676e9498857544c26f0209be27bf1f2074a`): **PASS**. Body conclusion, non obstantibus clause, Datum Romae apud sanctam Mariam Maiorem dating clause continuing to top of right column, then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00020298.part-02` — PASS

*Inter apostolicae qua tenemur sollicitudinis munia — Translatio sedis cathedralis Casertanae ad Casertam Novam* · GREGORIUS EPISCOPUS · 1841-07-15 · Latin · bull

- Page 1 (`3a0dc6cb478239ddb0145c3587d85cc9fe558cfacb5d9e5d4b0af8ccb6f34b6f`): **PASS**. Bull; title/issuer GREGORIUS EPISCOPUS/date/Latin match; servus servorum Dei intitulation; two full columns; clean.
- Page 2 (`2bf3aa865121bb3012353fccb6359ad17943b58bcb6c5fa5f6cd0f4cd2d94ed6`): **PASS**. Body continues in two full columns; literal OCR stray hyphen line '- curam' disclosed in apparatus; no furniture; clean.
- Page 3 (`b4806c6389e601269d1313245c3401871cb5908cd9882e2ef4c45544fb812324`): **PASS**. Executor clause, Nulli ergo sanction, Datum Romae apud s. Mariam Maiorem dating clause, then apparatus disclosing literal etc. and stray hyphen; source-bearing final page.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00020298.part-03` — PASS

*Universi dominici gregis salus — Provincia Texensis in vicariatum apostolicum erigitur* · GREGORIUS PP. XVI. · 1841-07-16 · Latin · motu-proprio

- Page 1 (`a59e983e778bf26c76aa799a81b2cc69836887b9abbb7c80fb96284fbd92f66d`): **PASS**. Motu proprio; title/issuer/date/Latin match; Datum Romae clause continues to top of right column then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00020298.part-04` — CHANGES_REQUIRED

*Perlatum ad Nos est — Michaeli Lewicki archiepiscopo Leopoliensi Rutheni ritus de primatu et ritibus* · GREGORIUS PP. XVI. · 1841-07-17 · Latin · papal-letter

- Page 1 (`f4d434e80098648447f397955e8f90d7822bee14734e713aee1304a7ef20c055`): **CHANGES_REQUIRED**. Title/issuer/date/Latin match. Edition folio '147' left inside the body: printed on the same line as body words ('ven.' / '147 frater, ut clero tuarum ...'). Note 1 begins as its own block after 'ipsis ingruentium pe-' at the source page break and runs through the right column.
  - BLOCKING: page 1, left column upper third: source folio '147' left in the body, sharing a line with body words ('147 frater, ut clero ...').
  - Qualification (non-blocking, coordinator edition-note ruling): page 1, left column lower half to right column: edition note 1 set as separate blocks at the source page break ('pe-' / 'riculorum' resumes on page 2).
- Page 2 (`41e8ead0bbb0f6f91c568023d68c2659d1e331ca7d646c633d4748c6678b31ac`): **PASS**. Note 1 and body alternate only as separate blocks at source page breaks ('in Russiae' / 'riculorum initiis'; 'insuper ad-' / 'imperio et Pius VII'); right column continues the quoted 1802 Propaganda decree inside note 1. No folio or running head on this page; no line mixes note and body words.
  - Qualification (non-blocking, coordinator edition-note ruling): page 2: note-1 blocks and body blocks alternate at source page breaks in source order.
- Page 3 (`af284c733ba4e4cee36c9afa6c7acbae2521eea24c7a6e80d8c78eee87f740b6`): **CHANGES_REQUIRED**. Left column: note 1 concludes 'Concordiam »,' then body resumes 'notasti, plures ...' as its own block. Right column: edition folio '149' left as a stranded line inside the body word 'vige-/sima'.
  - BLOCKING: page 3, right column middle: source folio '149' left inside the body, splitting the word 'vige-/sima'.
  - Qualification (non-blocking, coordinator edition-note ruling): page 3, left column upper half: end of note 1 as a separate block before body resumes at 'notasti'.
- Page 4 (`e7d74c7e9ccd5d6dea2014e91fbd644f90dbfb2e31eb4af5152554f9fb0331a0`): **CHANGES_REQUIRED**. Right column: volume running head 'ACTA GREGORII PP. XVI.' left as a line inside a body sentence ('scissionis,' / 'nisi Michaelem Caerularium'). Left column: footnotes 1-3 set as separate blocks between 'speciatim vero catechismum' and 'non lingua solummodo'.
  - BLOCKING: page 4, right column middle: volume running head 'ACTA GREGORII PP. XVI.' left inside the body sentence ('scissionis,' / 'nisi Michaelem').
  - Qualification (non-blocking, coordinator edition-note ruling): page 4, left column upper half: footnotes 1-3 set as separate blocks at the source page break.
- Page 5 (`c4ee43f25588bb1688859a1301a2fe9af83dd4bc16b0d717ff7df8dc461a6f18`): **PASS**. Left column: note block (notes 1-4, '>', '(c)', '7 Sess.') set separately between 'quam nisi' and 'quisque integram'; body concludes; right column Datum Romae dating clause, footnotes 1-3, apparatus disclosing fused edition note1. No folio or running head on this page.
  - Qualification (non-blocking, coordinator edition-note ruling): page 5, left column upper half: footnote block set separately at the source page break between 'quam nisi' and 'quisque integram'.
  - Qualification: apparatus discloses edition note1 as retained printed apparatus.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00021663` — PASS

*Apostolicae providentiae ac benignitatis — Insignia canonicorum basilicae Sancti Laurentii Florentiae* · GREGORIUS PP. XVI · 1841-07-27 · Latin · indult

- Page 1 (`4ed712783c2702077df3d4f3ea07058404beaf3a599ab81dc5aa30e1e4eddc06`): **PASS**. Title/issuer GREGORIUS PP. XVI (no final period, matches metadata)/date/Latin match; two columns; Datum Romae closing then apparatus; clean.
  - Qualification (non-blocking): issuer spelled GREGORIUS PP. XVI without final period, matching frozen metadata.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00024436` — PASS

*Perspecta Nobis religio — Ferdinando Austriae imperatori de dispensatione matrimonii Victoris Emmanuelis et Adelaidis* · GREGORIUS PP. XVI. · 1841-08-19 · Latin · papal-letter

- Page 1 (`04fc4fadba99f0b4feec5760a64b5a30912146a8c44df25dfc06b79d9c96f9e4`): **PASS**. Title/issuer/date/Latin match; short letter in left column with address, salutation, body, Datum Romae closing and apparatus; right column empty; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00024287` — PASS

*Dudum Nos sollicitos habent — Henrico episcopo Heliopolitano, vicario apostolico Gibraltariae, de aedituis* · GREGORIUS PP. XVI. · 1841-08-22 · Latin · papal-letter

- Page 1 (`9b20c6e5c432ca1a1544495b4b6b63806c2fc7c7e607c081d5c4f956cf36b976`): **PASS**. Title/issuer/date/Latin match; two columns; right column stops about 55% down after 'fruantur.' and the next paragraph begins on page 2 (non-blocking whitespace, no clipping or overlap).
  - Qualification (non-blocking): page 1 right column leaves lower half blank before the 'Denique' paragraph continues on page 2.
- Page 2 (`1973cdd79f3bb182f362575c69d03bff115b0b0b5f86bb68b14b0d8832852296`): **PASS**. Final paragraph, Datum Romae dating clause and apparatus in left column; source-bearing final page.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00024500` — PASS

*E lungo tempo che il tuo popolo — Desgiamaccio Ubie signore del Tigre in Abissinia* · Questa lettera del Pontefice Massimo di Roma, successore dis. Pietro, @ mandata · 1841-08-29 · Italian · papal-letter

- Page 1 (`0153b0b67b402d7c38b9b29e8596d66a252ff69e7bf6d8a7184ef2d91c41e760`): **PASS**. Italian letter; title/date match; language line reads Italian, matching assignment language it. Issuer line is the letter's own OCR-damaged Italian superscription ('Questa lettera del Pontefice Massimo di Roma, successore dis. Pietro, @ mandata'), matching frozen metadata and disclosed in apparatus; left column only, Dato in Roma dating clause then apparatus; clean.
  - Qualification (non-blocking): issuer displayed as OCR-damaged Italian superscription naming the Roman Pontiff (stray '@', 'dis.'), matching frozen metadata; apparatus discloses absence of GREGORIUS PP. XVI. intitulation and Italian text language.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00024551` — PASS

*Universi dominici gregis salus — Vicariatus apostolicus Siamensis in Orientalem et Occidentalem dividitur* · GREGORIUS PP. XVI. · 1841-09-10 · Latin · apostolic-letter

- Page 1 (`6c4eed04531cb07f8d928bb62b65636eed69b4592fa4c19cd6bdb7f99a9292bc`): **PASS**. Title/issuer/date/Latin match; two columns; literal 'Haec volumus etc.' disclosed; Datum Romae clause then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00024652.part-01` — PASS

*Quamvis per similes apostolicas litteras — Iacobo Leonardo Perocheau de coadiutore vicarii apostolici Coreae eligendo* · GREGORIUS PP. XVI. : · 1841-09-17 · Latin · apostolic-letter

- Page 1 (`858ff614b78ccb976ac8e4176383de223e938049d64a9a8a863b2199068e4a4a`): **PASS**. Title/date/Latin match; issuer line 'GREGORIUS PP. XVI. :' with stray OCR colon, matching frozen metadata; two columns; literal 'Volumus tamen etc.' disclosed; Datum Romae clause then apparatus; clean.
  - Qualification (non-blocking): issuer displayed with stray OCR colon 'GREGORIUS PP. XVI. :', matching frozen metadata and identifying Gregory XVI.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00024905` — PASS

*Ad apostolicae dignitatis atque auctoritatis fastigium — Ecclesia cathedralis Reatina in basilicam minorem erigitur* · GREGORIUS PP. XVI. · 1841-09-24 · Latin · apostolic-letter

- Page 1 (`9688d3a8f4120852a3bf96f36a4092b262487b56277ba7233271cce338d4c928`): **PASS**. Title/issuer/date/Latin match; two columns; non obstantibus clause and Datum Romae closing then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00025003` — PASS

*Cum de universi dominici gregis salute — De Canonicissis Lateranensibus monasterii Iesu et Mariae Neapoli* · GREGORIUS PP. XVI. · 1841-09-24 · Latin · apostolic-letter

- Page 1 (`08a8b746b6cfc7613a2079977b5899060a67e32280e457c3594159108d8418ec`): **PASS**. Title/issuer/date/Latin match; two full columns; clean.
- Page 2 (`deac58aec3862fb15b1221df88e38e670f7f460e0bc4c9451176588a91be3942`): **PASS**. Body conclusion, non obstantibus clause, Datum Romae dating clause and apparatus in left column; source-bearing final page.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00025194` — PASS

*Mysticam Petri naviculam — Episcopatus Cameracensis in archiepiscopatum erigitur cum suffraganea Atrebatensi* · GREGORIUS EPISCOPUS · 1841-10-01 · Latin · bull

- Page 1 (`f428521c615de6089fdfd153b88f9f2b5f4d3e9bff2028f7b0adca7e1a403638`): **PASS**. Bull; title/issuer GREGORIUS EPISCOPUS/date/Latin match; servus servorum Dei intitulation; two full columns; clean.
- Page 2 (`1b07af9d9b2519d240dedbbb8a66dd012060190e779289dcbfe6406770a32061`): **PASS**. Body continues in two columns; right column ends about 55% down at 'ostensae.' with literal OCR stray hyphen '-ubique' (disclosed); Nulli ergo sanction continues on page 3 (non-blocking whitespace, no clipping).
  - Qualification (non-blocking): page 2 right column leaves lower half blank before the 'Nulli ergo' paragraph on page 3.
- Page 3 (`6d80de571da03090e95a6093bf71a039f740c26554dd9de4ac5b3bc7b5cc3e81`): **PASS**. Nulli ergo sanction, Datum Romae de speciali mandato dating clause, then apparatus disclosing stray hyphen; source-bearing final page.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00025470` — PASS

*Literae, quae datae a te — I. Collin de Plancy de reditu ad fidem catholicam* · GREGORIUS PP. XVI. · 1841-10-16 · Latin · papal-letter

- Page 1 (`a4dac631fb8750e017afc7ac7a63119ef54b833be93c39764fae2f92583d5d81`): **PASS**. Title/issuer/date/Latin match; letter in left column with address, salutation, body, Datum Romae clause and apparatus; right column empty; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00025543` — PASS

*Cum hominum mentes animique — De equestri ordine Auratae Militiae* · GREGORIUS PP. XVI. · 1841-10-31 · Latin · apostolic-letter

- Page 1 (`0a9185283e5775300de92d5b311b9cb0a8b15f45ad3fde325b5f9b316dc35ca6`): **PASS**. Title/issuer/date/Latin match; two full columns; clean.
- Page 2 (`ce425ba107ce44a4d2c1f62f0f97d5d0b081ca428e8ee6d8b8f7615d6cd1fa22`): **PASS**. Body conclusion, non obstantibus clause, Datum Romae dating clause in right column, then apparatus; source-bearing final page.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00025806` — PASS

*Nihil profecto tristius — Leopoldo archiduci Austriae, magno duci Etruriae, de morte filiae* · GREGORIUS PP. XVI. · 1841-11-12 · Latin · papal-letter

- Page 1 (`1c93fc74a410fb4a9bae170029242408e68ab401c39857c2f05f77d1f2871a71`): **PASS**. Title/issuer/date/Latin match; letter in left column with Datum Romae closing and apparatus; right column empty; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00025868` — PASS

*Redditae Nobis sunt regiae maiestatis tuae literae — Friderico Guilelmo Borussiae regi de ministro de Buch* · GREGORIUS PP. XVI. · 1841-11-22 · Latin · papal-letter

- Page 1 (`9fbfe2112d04b97a2fd8a3e528dd73988ea38012b1db8f8ec106570b7a5985f8`): **PASS**. Title/issuer/date/Latin match; letter in left column with Datum Romae closing and apparatus; right column empty; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00026718` — PASS

*Inter multiplices gravissimasque apostolatus Nostri curas — Provincia occidentalis Canadae superioris in episcopatum erigitur* · GREGORIUS PP. XVI. · 1841-12-17 · Latin · apostolic-letter

- Page 1 (`f30e0da3f545505ebaeb12e02f224cf68fe3020b1d9a98ccaec97cab8381fc31`): **PASS**. Title (three lines)/issuer/date/Latin match; two columns; Non obstantibus clause, Datum Romae clause at top of right column, then apparatus; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00026803.part-02` — PASS

*Cum aliquandiu abfuissemus ab Urbe — Nicolao I Russiarum imperatori de nuptiis filii Alexandri* · GREGORIUS PP. XVI. · 1841-12-23 · Latin · papal-letter

- Page 1 (`1c07d6cde57cb0144bb6eb9467fb9837407315125a6e46fb2010bdf7d8abe0da`): **PASS**. Title/issuer/date/Latin match; letter in left column with Datum Romae closing and apparatus; right column empty; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00026941` — PASS

*Quo magis, pro paterno — Ludovico Bavariae regi de morte reginae viduae* · GREGORIUS PP. XVI. · 1842-01-03 · Latin · papal-letter

- Page 1 (`12cdce43483c83d0c967ff26c37f78aff9b444297e183b6c07dccb29429cf1b0`): **PASS**. Title/issuer/date/Latin match; letter in left column with Datum Romae closing and apparatus; right column empty; clean.
- Prior finding: none assigned.

### `gregory-xvi-acta.volume-03.line-00027004` — PASS

*Apostolicae huius Sedis benignitas — Oppidum Monte San Giovanni in civitatem erigitur* · GREGORIUS PP. XVI. · 1842-01-07 · Latin · apostolic-letter

- Page 1 (`057e3c5c48f36484bfade247ececb93653aa8fe7dca3c4cd289e525ff22448a2`): **PASS**. Title/issuer/date/Latin match; two columns; right column ends about 60% down after 'attentari.' and the non obstantibus paragraph continues on page 2 (non-blocking whitespace, no clipping).
  - Qualification (non-blocking): page 1 right column leaves lower part blank before the 'Non obstantibus' paragraph on page 2.
- Page 2 (`ec36dc270b74265fccdbee12cea422553ddd8813087c7e18d15d873abbd5ba6d`): **PASS**. Non obstantibus clause, Datum Romae dating clause and apparatus in left column; source-bearing final page.
- Prior finding: none assigned.

## Limitations

- The texts are literal, uncorrected, uncollated historical OCR rendered as a mechanical two-column source edition. Wording, odd spellings and OCR corruption were not judged or repaired.
- This was a layout and page-furniture review only. No word-level collation against the printed source was performed.
- No historical authentication or date reconstruction was performed. This report makes no claim of publication, installation or deployment.
- Source admission and successful rendering are upstream facts, not findings of this lane.
