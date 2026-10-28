# Historical series visual review 34 — Bullarii Romani Continuatio finite lane

Review date: 2026-10-28. Batch `continuatio-0016`, lane 34. Result: **11 PASS; 40 CHANGES_REQUIRED** of 51 assigned PDFs. All 68 of 68 page rasters were individually opened at full size (41 pages carry a blocking finding). No pages were reused and no inspection proofs were borrowed.

## Scope and method

The assigned set is exactly the 51 PDFs in `.scratch/historical_series_visual/lane-34/assignment.json`: 21 pages from *Bullarii Romani continuatio* tome VI (Pius VI) and 47 pages from tome XV (Pius VII). Each queued PNG from the completed central raster run was opened as its own full-size image (1700×2200, displayed at original resolution scaled to the viewer) with the Read tool, one image per page. No contact sheet, thumbnail, cache hit, new raster pass, source acquisition, marker scan, word-level collation, text correction or date reconstruction was used or performed.

For each page the displayed title, responsible issuer, the omission of the unresolved act date, and the language label were compared with the frozen `metadata` in `page-queue.json`. Headings, two-column flow, gutter, margins, glyphs, tables, natural source closing, historical notes and terminal source/rights apparatus were inspected. No visible clipping, overlap, missing-glyph/tofu blocks, flattened table, stranded heading, raw `None` placeholder, colophon-only final page, or recognizable modern digitizer signature ("Digitized by Google" or damaged variants) was found on any page.

The blocking class in this lane is **inline marginal-summary fusion**: OCR of the printed marginal captions (Prooemium, Expositio precum, Tenor concessionis, Clausulae, Derogatio contrariorum, marginal dating and `Anno XIX/XX/XXI` labels) inserted inside body sentences or inside hyphen-split body words. Separately retained marginal blocks standing between paragraphs or at a paragraph start, and historical running heads/page numbers, are recorded as nonblocking qualifications. One document also carries a blocking responsible-issuer identification defect.

This review does not authorize installation and makes no claim that installation, deployment, publication or historical authentication has occurred. No source, metadata, PDF, raster or shared file was modified.

## Evidence verification

All 51 assigned PDF digests, the render receipt, frozen manifest, canonical source admission receipt, visual admission manifest, all 68 page PNGs and the final raster-run file (124 files) were hashed before inspection and again after; every digest matched its assignment/queue pin both times and the two records are identical.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Canonical source admission receipt (`clean-332-reviews.json`) | `735468568f2e0f2fc48c16ef5d3911ba2acba8e0949ddf38002c8e95dca727c3` | Before and after |
| Frozen source/render manifest | `7947f97884e262de16de0cb5787c18365cf02b110538d04e5c34c2bdb3e19ce3` | Before and after |
| Successful render receipt | `33d9110cc7f2426684d1ebe5fabd4ebbd2f03e3168ab6ad05568c672f0f83f9d` | Before and after |
| Visual admission manifest | `d0570dac93fdfaa654bf6b8170c8817fc04ba5ecc39d6fdd58b2e6bbd3e76f61` | Before and after |
| Final shared raster run (`rasters-continuatio-0016/review-run.json`) | `32603817dd58b4fa4929b3eb8f7bfb06c9ee76d1f44d133fb2912d4a6e15f8ab` | Before and after |
| Lane assignment | `f79ef9d141ae020d10d711518e874cfbf4928f99dc06a6e11bb36e35f786ed5e` | Exact scope binding |
| Exact page queue | `bc88e434e7cbc00f80de220e5b60b265ec0bdb875d73eb5f2464d6ced659b635` | Exact raster binding |
| Individual inspection ledger (`observations.jsonl`) | `d46ac7fc24de220d9b2ae72fbde08c391a0977bd8506a51e9e6170878670774a` | 68 unique observations |
| Before verification record | `5e5a6c9de12111d8b3c5d67ab71f81eb67a053ffcd11f17ce4f2f1f64a1fafb9` | PASS |
| After verification record | `5e5a6c9de12111d8b3c5d67ab71f81eb67a053ffcd11f17ce4f2f1f64a1fafb9` | PASS; identical hashes |

## PDF outcomes

Every act date is unresolved in the frozen metadata and is correctly omitted from the title line. The receipt and manifest above bind every PDF below.

| Source ID | Language | Page count | Pages inspected | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- |
| `bullarium-continuatio.volume-06.line-00103790.part-01` | `la` | 1 | 1 | `29ee4ee5103efd552d277c0092d5fe83ff0af7a6b795a3a98a0e949cf8ac9b7a` | PASS |
| `bullarium-continuatio.volume-06.line-00103790.part-03` | `la` | 2 | 1, 2 | `a7e0e70a22b7f466a00c555e082a878572db893a32753140948dc2adc93a72eb` | PASS |
| `bullarium-continuatio.volume-06.line-00103790.part-04` | `la` | 2 | 1, 2 | `511433fe2327b9996f5b950d80b093ca5769ad6d61d2f25c7026f18d3364b203` | PASS |
| `bullarium-continuatio.volume-06.line-00103790.part-05` | `la` | 2 | 1, 2 | `4a3ab8def17e5a3ac03ffd3dc49098cf390c43f93c59eef28ef9eda37e418ddc` | PASS |
| `bullarium-continuatio.volume-06.line-00105289` | `la` | 3 | 1, 2, 3 | `61d3deed466112bfdfd5b632f4a15d13794e6dfcd47213bdd6b953cf0f9e1563` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-06.line-00106172` | `la` | 3 | 1, 2, 3 | `6d1e4f06e719cdd6f8f2db574ccfe1a14637644f7b26f1dd2671047f44c5a8e5` | PASS |
| `bullarium-continuatio.volume-06.line-00106661.part-01` | `la` | 2 | 1, 2 | `8099cb663e1176904b4a8949f40f1d74165cfbbfc625dc26b4e44567aafa0b6b` | PASS |
| `bullarium-continuatio.volume-06.line-00107940.part-01` | `la` | 1 | 1 | `e08639e8eabe3798a7f22e38662bf3bb848eeb2b95a386836ccb21a7f3c39375` | PASS |
| `bullarium-continuatio.volume-06.line-00107940.part-02` | `it` | 5 | 1, 2, 3, 4, 5 | `bf6480442f3592b531cf91376f9e56a0490300cae715f40464f4d1362b1069c2` | PASS |
| `bullarium-continuatio.volume-15.line-00010973` | `la` | 1 | 1 | `3e8718f933b0b4e0a77350d298aaa308d22e4880b956b4d0778dd6aec3e9b197` | PASS |
| `bullarium-continuatio.volume-15.line-00011979.part-02` | `la` | 1 | 1 | `76a8c95c5212a93a216d3f79539947d299378cc2e4e492c95f70fe76c700e608` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00014845` | `it` | 1 | 1 | `521de54a3325ef6343098511db617b9cb6f748926b2d17eaa5e7c9456ed1b0c4` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00020175` | `la` | 2 | 1, 2 | `d77e355717857d90d5389aa0a5f143f220009b0ca711f81c1ec9456fbf65d212` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00020320.part-02` | `la` | 1 | 1 | `e0ae27b6714d327ad94bdcc96f9512d4e7dd7149f7857d917d0b14c5fd1cc29f` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00020320.part-03` | `la` | 1 | 1 | `4d1b6a7fee10b94a79e6e338a7f8283f1953b5b4bdcd4c367476d62255c2ff39` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00020666` | `la` | 1 | 1 | `8dd2b04e6737fd36b050d4a1bb73505a6981afbf7a8310a4d4f7b49334ac4a71` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00020760` | `la` | 1 | 1 | `4a849ca4e678ff5b7f0e0fbcb40cd7550d9fbce2dc015c274cc5958c46c10b02` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00020888` | `la` | 1 | 1 | `86963c2f0fb6be68efa19f9f5c66d5776ec0130a904487d14f576617413ed205` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00021431` | `la` | 1 | 1 | `f1bbe7a7d9a5c5fd045dc31957326c0211685472e09662c9686bb1d3e143d2a3` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00022610` | `la` | 1 | 1 | `cdac78a87a9ba2d15c2b7e41fafc7cbd25b45a3f7ce4100fb06faa924d60e41d` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00022854.part-01` | `la` | 1 | 1 | `8faeb217ee56c623102313137c70e83fae6985a6c16c69e112cd2ce117c4e997` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00022854.part-02` | `la` | 1 | 1 | `8ace26ecd6cc527ca0dd5de97e4ce140fd859681be50141c5721f36f697a8e25` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00023187.part-01` | `la` | 1 | 1 | `381e7305770b53a7440f3e92eccd31eff0f419684568fc28fea23223c3f43d88` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00023187.part-02` | `la` | 1 | 1 | `f3f750952c0f94bf98c824c9eb6d7e3e4d21a1b49d3f42dde4ab51daa33e4f94` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00024897.part-02` | `la` | 1 | 1 | `ddbbf46fb3c8cf15b2916ba62caf669492a550082726c6e6886464e34ac43de8` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00026610` | `la` | 1 | 1 | `4899a0993837c4e296d34a9bcf365e48ce542ba721727eb5755afb2992e9ce8d` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00026701` | `la` | 1 | 1 | `c6b44001fe9dea42bcf983a4f63bc2e236515426d6588ded3b422f2a1216b46a` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00030230` | `la` | 1 | 1 | `ccc2cb9c7fe4d4ab1b84d95fa790c9f0b26f60b4d1509f8cb8b19e443159739c` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00035412` | `la` | 1 | 1 | `c5b96e16aa9bcf1cfddc46f27d50712c583c1d6393d1f7e104014b8a7dcb7ef9` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00036542.part-01` | `la` | 1 | 1 | `1b6c307a5b177c6e89d98d04a03f8e397cd01f8c4851ed18672050498fd316a0` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00036542.part-02` | `la` | 1 | 1 | `ec69a94af63c3c1b28713748cb69b765736d1067ec3237a001dac1b45963ac9d` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00037369` | `la` | 1 | 1 | `1931a2f0da01f731f5b0897874ccdf6814543f7093862d4796733fdb85022a3c` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00037789` | `la` | 2 | 1, 2 | `e71eddd382a8d9272bcfe72d1c1cd675a08531d2e054e04c0c5f97899cfdd370` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00038131` | `la` | 1 | 1 | `43c27416585d74d0d8fe5fa4c3aec8fd7bdbcd8dca2966ea2c5262814eb553c3` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00038687` | `la` | 1 | 1 | `32447dcfbe69eea22e8a08b4d110ffad18dd5218a76a21e920cb2b69c12f250f` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00039134.part-02` | `la` | 2 | 1, 2 | `28b9041c18f489ff1f66d0925d355b767c9b3addbb2f6eb7b0915f800f774142` | PASS |
| `bullarium-continuatio.volume-15.line-00039947` | `la` | 1 | 1 | `e1383e5217fd7c969f2f1eda9c2636683ecaa5ca6af875a1cc548e980779cb89` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00040070` | `la` | 3 | 1, 2, 3 | `9b1d0b403e69494129923ec1708d78a88f850cf29a8e6003988f76fdd3ba4743` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00040917` | `la` | 1 | 1 | `730c6dfdd9f7d69ed25ac59c8637d2e9a4403dd0aef8f3d9b8cbb7bc02b74f67` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00041050` | `la` | 1 | 1 | `a83db947791dd64cba4b36d6d3e2d52615b3fa092a2d041abe710e6fe7b6bb95` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00041109` | `la` | 1 | 1 | `3a85358779ec31041d876b930d3b4acb09bfd5122d17db14c77cd46720a7ed1a` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00041224.part-02` | `la` | 1 | 1 | `0c006e518f8c39d0c6b8d479666288a35982308fc0d502580c86f9eef173f34e` | PASS |
| `bullarium-continuatio.volume-15.line-00042121` | `la` | 1 | 1 | `b5aff9e9873d9e56251dc27df8924617e194a81646e6f7f71a8d4f7b54893d97` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00042432.part-02` | `la` | 1 | 1 | `aceacd6afb93527b371d21f6d2f1e27e677e33ec2d2dbd9572f59222f17c154e` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00042432.part-04` | `la` | 1 | 1 | `e4a7cffe58adf56a060947552b8caeb84959440c04be1eb879d632bc7006a89c` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00042432.part-05` | `la` | 1 | 1 | `bb30b9a17899f0b9d0cd1b1495224368f1fec444548cf319bc9a669683c84ad0` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00045937` | `la` | 1 | 1 | `e004349b4ba70ec24ee61f96f59d1b3fb18d4a06844b85e5fb92cfeb37d65e54` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00046365.part-01` | `la` | 1 | 1 | `054001c165514a486f6bee07e65afcc99b4576b6435510670153c1d337134c78` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00046365.part-02` | `la` | 1 | 1 | `6844f65b63858511ab65be2480eb5122066b81f6b065f577bce9cf6de20f1ef9` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00047648` | `la` | 1 | 1 | `277ec7fb0da43c788136193dd4ff0881835ef9c996514df6a641ea1c605474b4` | CHANGES_REQUIRED |
| `bullarium-continuatio.volume-15.line-00047758.part-01` | `la` | 1 | 1 | `545f468845fdff0a0507f825ec2be2e536b7801cb60874e4ba09bbb7fbd00b3d` | CHANGES_REQUIRED |

## Blocking findings per document

### `bullarium-continuatio.volume-06.line-00105289` — CHANGES_REQUIRED

- metadata-issuer-clarity: page 1, compact identification line below the title displays the responsible issuer as 'Pius PP. v E "T'; the corrupted regnal designation does not unambiguously identify the responsible pope (the body's own running head reads 'Pius PP. Sextus'). Source-owner metadata reconciliation required without altering the literal body wording.

### `bullarium-continuatio.volume-15.line-00011979.part-02` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, upper, §. 1 'In summo aposlolatus apice , Proeniiu» meritis licet imparibus' — marginal 'Prooemium' label inserted mid-sentence between 'apice' and 'meritis'.
- Inline marginal-summary fusion: page 1, left column, top synopsis 'Concessio mozzettac violacea© cum ca- i8i8 pytio' and 'eccle- / Aawxix. 8jae parochialis' — marginal date '1818' and 'Anno XIX' fragments inserted inside the hyphen-split words 'ca-putio' and 'eccle-siae'.
- Inline marginal-summary fusion: page 1, left column, §. 2 'Expositum siquidem Nobis nu- / PWcwbT tU° Dom*ne * qu°d tu' — marginal 'Expositio precum' residue fused inside the body sentence after 'nu-'.

### `bullarium-continuatio.volume-15.line-00014845` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, middle, §. 2 'Volendo , e decreUndo , che / inuro» «i tni- it presente Nostro moto - proprio' — unidentified marginal fragment inserted mid-sentence between 'che' and 'it presente'.
- Inline marginal residue fusion: page 1, left column, upper, §. 1 'La varia zione della durata r*«m , «i della rinomata fiera' — marginal residue inserted mid-sentence between 'durata' and 'della'.

### `bullarium-continuatio.volume-15.line-00020175` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, top synopsis 'per viati- »«« xix cum' and 'Eu- ** jg* charistiae' — marginal 'Anno XIX' and residue inserted inside the hyphen-split words 'viati-cum' and 'Eu-charistiae'.
- Inline marginal-summary fusion: page 1, right column, upper-middle, 'Decernentes ipsas praesentes / wiwn** iit literas firmas , validas , et efficaces exi- Uo* stere' — marginal 'Clausulae' residue inserted mid-sentence and inside 'exi-stere'.
- Inline marginal-summary fusion: page 1, right column, middle, 'Non obstantibus apostolicis , ac uwfJnui*0"* in universalibus' — marginal 'Derogatio contrariorum' residue inserted mid-sentence.

### `bullarium-continuatio.volume-15.line-00020320.part-02` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, lower, §. 3 'Nos igitur exponentium votis T,n„r con. benigne annuere' — marginal 'Tenor concessionis' label inserted mid-sentence.
- Inline marginal residue fusion: page 1, left column, lower, §. 3 'eosque, ac singu- ccs'u,°1' lares' — marginal fragment inserted inside the hyphen-split word 'singu-lares'.
- Inline marginal-summary fusion: page 1, right column, middle, §. 4 'Non obstantibus fel: rcc; Benedicti D-r«*.u«, pp. XIV.' — marginal 'Derogatio' residue inserted between 'Benedicti' and 'pp. XIV.'.
- Inline marginal-summary fusion: page 1, left column, synopsis 'pro canonicis eccle- 151» siae' — marginal fragment inside the hyphen-split word 'eccle-siae'.

### `bullarium-continuatio.volume-15.line-00020320.part-03` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, right column, upper-middle, §. 4 'Benedicti pp. XIV. praedecessoris Nostri su- eootrwioru» per divisione' — marginal 'contrariorum' (Derogatio contrariorum) inserted inside the hyphen-split word 'su-per'.

### `bullarium-continuatio.volume-15.line-00020666` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'numerum adolescen- anao xix. tiura choraliuin' — marginal 'Anno XIX' inserted inside the hyphen-split word 'adolescen-tium'.
- Inline marginal-summary fusion: page 1, left column, middle, §. 3 'Non obstantibus constitutioni- D*roff«ij» bus.' — marginal 'Derogatio' residue inserted inside the hyphen-split word 'constitutioni-bus'.
- Inline marginal residue fusion: page 1, left column, §. 2 'susceptum per dictos cwMoiu*. canonicos' — marginal fragment inserted mid-sentence.

### `bullarium-continuatio.volume-15.line-00020760` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'et invoca- i*» tione' and 'Servitori **"* in civitate' — fragments inserted inside the hyphen-split word 'invoca-tione' and mid-phrase.
- Inline marginal-summary fusion: page 1, right column, upper, §. 3 'Decernentes easdem praesentes ercinm irri- literas semper urinas validas , et enicaces Uo*' existere' — marginal 'Clausula irritans' residue inserted mid-sentence between 'praesentes' and 'literas'.
- Inline marginal-summary fusion: page 1, right column, upper-middle, §. 4 'constitutionibus, emiranwum. et ordinationibus' — marginal 'contrariorum' residue inserted mid-sentence.

### `bullarium-continuatio.volume-15.line-00020888` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'in basilicam minorem cum ,nno X1X' omnibus privilegiis' and 'san- «● cti' — marginal 'Anno XIX' inserted mid-sentence and residue inside the hyphen-split word 'san-cti'.
- Inline marginal residue fusion: page 1, left column, §. 3 'attentis desuper or- r*-or «or- dinarii' and 'ipsum ex- "*MuauK ponentem' — marginal fragments inserted inside the hyphen-split words 'or-dinarii' and 'ex-ponentem'.
- Inline marginal-summary fusion: page 1, right column, middle, §. 5 'Non obstantibos, quatenus opus / coniranorun sit' — marginal 'contrariorum' inserted mid-sentence between 'opus' and 'sit'.

### `bullarium-continuatio.volume-15.line-00021431` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, foot, §. 3 'Non obstantibus felicis recorda- ®«i»r»oni®i. t ion is Benedicti' — marginal 'Derogatio contrariorum' residue inserted inside the hyphen-split word 'recorda-tionis'.

### `bullarium-continuatio.volume-15.line-00022610` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'favore cano- jjjyj, nicorum capituli ecclesiae cathedralis 18,8 Rossanensis' — marginal fragment and marginal year '1818' inserted inside 'cano-nicorum' and mid-phrase.
- Inline marginal-summary fusion: page 1, left column, lower, §. 3 'Non obstantibus felicis rccor- coairaxionuB' dationis' — marginal 'contrariorum' residue inserted inside the hyphen-split word 'rccor-dationis'.

### `bullarium-continuatio.volume-15.line-00022854.part-01` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'princi- iiMioLrii palium' and 'oppido- wmlTxix rum' — marginal fragments (including 'Anno XIX') inside the hyphen-split words 'princi-palium' and 'oppido-rum'.
- Inline marginal-summary fusion: page 1, left column, §, 1 'in forma bre- Mw?onl»! C0D* v*9 li teras' — marginal residue inside 'bre-vis literas'; §. 2 'supplicationibus Tmr «<w- inclinali' — marginal 'Tenor' residue inserted mid-sentence.
- Inline marginal-summary fusion: page 1, right column, §. 3 'brevis literis diei decimae aprilis, qui- CMlU,rioruB1 busad' — marginal 'contrariorum' inside the hyphen-split word 'qui-bus'.

### `bullarium-continuatio.volume-15.line-00022854.part-02` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, §. 1 'Exponi Nobis nuper fecerunt Eipoiiuo prfr- dilecti filii' — marginal 'Expositio precum' inserted mid-sentence.
- Inline marginal-summary fusion: page 1, left column, §. 2 'Nos igitur dictos exponentes nnTrth w"' ®Pec*a*'^us gratiis' — marginal 'Tenor' residue inside 'specialibus'.
- Inline marginal-summary fusion: page 1, right column, §. 3 'Benedicli pp. XIV. praedecesso- tfWioro"- ris Nostri' — marginal 'contrariorum' inside the hyphen-split word 'praedecesso-ris'.

### `bullarium-continuatio.volume-15.line-00023187.part-01` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'ex praescri- n D'^hr(# pto' and 'monte Car- """ melo' — fragments inside the hyphen-split words 'praescri-pto' and 'Car-melo'.
- Inline marginal-summary fusion: page 1, left column, §. 1 'Exponi Nobis nuper fecerunt pMCTSpo*IUtf dilecti filii' — marginal 'Expositio' residue inserted mid-sentence; §. 2 'exponentes ape- tenor pon- / . ... * n 1 ● ceitiosli. / cialibus' — marginal 'Tenor concessionis' inside 'spe-cialibus'.
- Inline marginal-summary fusion: page 1, right column, top, 'Non obstantibus omnibus , et / conturionuD. singulis illis' — marginal 'contrariorum' inserted mid-sentence.

### `bullarium-continuatio.volume-15.line-00023187.part-02` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'puellarum sancti Vincent» uno xix. a pau|0' — marginal 'Anno XIX' inserted inside the name phrase 'Vincentii a Paulo'.
- Inline marginal-summary fusion: page 1, left column, §. 1 'Nobis gravissimi mo- / nor couceiiio- menti' — marginal 'Tenor concessionis' residue inside 'mo-menti'; §. 2 'Decernentes praesentes literas, cnn.ui. ««- et in eis' — marginal residue mid-sentence.
- Inline marginal-summary fusion: page 1, right column, §. 3 'et COBU,ri<>ruin* ordinationibus' and §. 4 'hominum Ii- s*n«u<» por- ceat' — marginal 'contrariorum'/'Sanctio poenalis' residue mid-sentence and inside 'li-ceat'.

### `bullarium-continuatio.volume-15.line-00024897.part-02` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'favore hebdomadario- 15 'li8wbri* n,m ec<^es>ae collcgiatae de Mcsagnc uid« xix.' — marginal date '15 decembris 1818 anno XIX' residue fused inside the synopsis words.
- Inline marginal residue fusion: page 1, left column, §. 3 'Nos attentis etiam desuper ve- mmIobu. c#** ncrabilis' — marginal fragment inside the hyphen-split word 've-nerabilis'.
- Inline marginal-summary fusion: page 1, left column, §. 4 'Non obstantibus costilutionibus , c «ir/nSniX et ordinationibus' — marginal 'contrariorum' residue inserted mid-sentence.

### `bullarium-continuatio.volume-15.line-00026610` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'pro verificatio- a, ne inventionis' and 'sacri cor- 9 poris' — marginal fragments inside the hyphen-split words 'verificatio-ne' and 'cor-poris'.
- Inline marginal-summary fusion: page 1, left column, §. 1 'JosephiMa- niiwdu» riac' — marginal fragment inside the name 'Josephi Ma-riae'; §. 2 'de fraterni- *mH' talum' — fragment inside 'fraterni-talum'; §. 3 'curis cer- n« tiores' — fragment inside 'cer-tiores'.

### `bullarium-continuatio.volume-15.line-00026701` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, §. 1 'In summo apostolatus apice , rrwwdBtt. ycel imparibus' — marginal 'Prooemium' residue inserted mid-sentence (replacing/merging into 'meritis licet').
- Inline marginal residue fusion: page 1, left column, §. 2 'in nova Mn" francia' — fragment mid-phrase; §. 3 'constitutio- JSSS.-0*' nibus' — marginal 'Derogatio' residue inside the hyphen-split word 'constitutio-nibus'.
- Inline marginal-summary fusion: page 1, left column, synopsis 'pro- tono xix. vincia' — marginal 'Anno XIX' inside the hyphen-split word 'pro-vincia'.

### `bullarium-continuatio.volume-15.line-00030230` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'vulgo bugia , d«i. 1« et gestandi', 'cappam , et 16 collare' and 'fasciolam ●nB0 *ix ejusdem' — marginal date '16 februarii 1819 anno XIX' fragments inserted mid-sentence.
- Inline marginal-summary fusion: page 1, left column, §. 2 'dilecti filii t»«- moderni' and §. 3 'speciali- cwwTui ^ 61,01'*8» et favor*bus' — marginal 'Expositio'/'Tenor concessionis' residue mid-sentence and inside 'speciali-bus'.
- Inline marginal-summary fusion: page 1, right column, §. 4 'Non obstantibus constitutionibus, (Miwmga et ordinationibus' — marginal 'Derogatio' residue mid-sentence.

### `bullarium-continuatio.volume-15.line-00035412` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'cardinalis Ridol- auLVxx. phi Austriac' — marginal 'Anno XX' residue inserted inside the hyphen-split name 'Ridol-phi'.

### `bullarium-continuatio.volume-15.line-00036542.part-01` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, §. 1 'Ex parte venerabilis fratris precum, Raymundi archiepiscopi' — marginal 'Expositio precum' fragment inserted mid-sentence.
- Inline marginal residue fusion: page 1, left column, §. 2 'sup- pumc^Tw£ plicantibus' and 'archicpUcopo gregiuoflit. 0t clero' — fragments inside the hyphen-split word 'sup-plicantibus' and mid-phrase.
- Inline marginal-summary fusion: page 1, right column, §. 4 'nec non di- / * , . ● coD(r«rlDruati / ctae met ropohtanae' — marginal 'contrariorum' residue splitting the word 'di-ctae'.

### `bullarium-continuatio.volume-15.line-00036542.part-02` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, §. 3 'Nomdbstantibus constitutionibus, «oni^rCruoQ0 et ordinationibus' — marginal 'contrariorum' residue inserted mid-sentence.
- Inline marginal residue fusion: page 1, left column, foot, 'Mariam Ma- / ji jorenvstib annuio piscatoris' — marginal fragment inside the hyphen-split word 'Ma-jorem'; also 'desi- 1 derant' inside 'desi-derant'.

### `bullarium-continuatio.volume-15.line-00037369` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'supra moz- uajil' zettam' and 'ecclesiae ab^'xx. aacramentalis' — marginal date/'Anno XX' fragments inside the hyphen-split word 'moz-zettam' and mid-phrase.
- Inline marginal-summary fusion: page 1, left column, §. 2 'specialibus gra- T«»r tiis' and 'et a ce'*l<",u quibusvis' — marginal 'Tenor concessionis' residue inside 'gra-tiis' and mid-sentence.
- Inline marginal-summary fusion: page 1, left column, §. 3 'omnibus, et sin- Dero«r«iio mjjg j||,v qUae ... con- CMirar torno' — marginal 'Derogatio contrariorum' residue inside 'sin-gulis' and 'con-cessa'.

### `bullarium-continuatio.volume-15.line-00037789` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, §. 1 'sub plum- buj«» 1*° lileras', 'octobris ®' r*"® anno' and 'sexto iiiiaircducUo- praevia' — marginal fragments inside 'plum-bo' and mid-sentence.
- Inline marginal-summary fusion: page 1, left column, §. 1 'opportune*, ttfc Cbinmtv- de proluendam' and §. 2 'deque apo- cjuu> prw- stolicae ... in dicu* d»uiMH |jac dumtaiat' — marginal residue inside the hyphen-split word 'apo-stolicae' and mid-sentence.
- Inline marginal-summary fusion: page 2, left column, §. 5 'Non obstantibus constitutioni* trinorum bus' — marginal 'Derogatio contrariorum' fragment ('trinorum') inserted inside the hyphen-split word 'constitutioni-bus'.
- Inline marginal-summary fusion: page 2, left column, §. 6 'quod ipsius Detcripuo ecclesiae' — marginal 'Descriptio' label inserted mid-sentence.
- Inline marginal-summary fusion: page 2, left column, §. 7 'Nulli ergo omnino hominum sanctio poe- liceat' — marginal 'Sanctio poenalis' inserted mid-sentence.

### `bullarium-continuatio.volume-15.line-00038131` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'plenariae , assc- An»oxx. quendae' — marginal 'Anno XX' inserted inside the hyphen-split word 'asse-quendae'.
- Inline marginal-summary fusion: page 1, left column, §. 1 'fidelium re~ TnwrcoMN* tigionetn' and 'salutem' coe- °n<' restibus' — marginal 'Tenor concessionis' residue inside 're-ligionem' and 'coe-lestibus'.
- Inline marginal residue fusion: page 1, left column, §. 2 'ut si pro conaniMM impetratione , ... admissio- a^Thib^i. ne' — fragments mid-sentence and inside 'admissio-ne'.

### `bullarium-continuatio.volume-15.line-00038687` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'de jure pa- Anno'xx» tronatu' — marginal 'Anno XX' inserted inside the hyphen-split word 'pa-tronatu'.
- Inline marginal-summary fusion: page 1, left column, §. 2 'Nos igitur dictum exponoulem ! «oIr^.eo'l specialibus' — marginal 'Tenor concessionis' residue inserted mid-sentence.
- Inline marginal-summary fusion: page 1, right column, §. 3 'Benedicli Derog»u» pp. XI V' and 'divisiuT «««o.riornw. ne materiarum' — marginal 'Derogatio contrariorum' inserted mid-name and inside 'divisio-ne'.

### `bullarium-continuatio.volume-15.line-00039947` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'ia p»« ci vitale Caesenae' and 'dolatione «c «te-3 11 Ttno** rura' — marginal date/'Anno XX' fragments inserted inside 'ci-vitate' and mid-phrase.
- Inline marginal-summary fusion: page 1, left column, §. 2 'Licet post Nostrum io hanc si a«u« «●£●»- Sedom regressum' — marginal residue inserted mid-sentence.
- Inline marginal-summary fusion: page 1, right column, §. 4 'Decernentes has praesentes li- / erelui *',r£ lGrm fi™*»*» validas' — marginal 'Clausulae' residue inside the hyphen-split word 'li-teras'; §. 5 'constitutioni- i / imiorum , et onlinationibus' — marginal 'contrariorum' inside 'constitutioni-bus'.

### `bullarium-continuatio.volume-15.line-00040070` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'Catnbcriensi, ea- D»t u, rumque' — marginal date fragment inside the hyphen-split word 'ea-rumque'.
- Inline marginal-summary fusion: page 1, left column, §. 2 'Statirn ac per politicas convcn- Expetit* tiones' — marginal 'Expositio' label inside the hyphen-split word 'conven-tiones'.
- Inline marginal residue fusion: page 1, left column, §. 1 'non exiguam ***●*'«● tenet partem' and §. 3 'propositis oJuio»u.8°^ praesertim' — marginal fragments inserted mid-sentence.

### `bullarium-continuatio.volume-15.line-00040917` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'capituli genera- » «jptt lis' and 'superiorum ordinis Anno xx Carmelitarum' — marginal date/'Anno XX' fragments inside the hyphen-split word 'genera-lis' and mid-phrase.
- Inline marginal-summary fusion: page 1, right column, §. 4 'efficaces exislero , tn* utium. et fore' — marginal 'Clausulae' residue inserted mid-sentence between 'existere' and 'et fore'.

### `bullarium-continuatio.volume-15.line-00041050` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'in consistorio secreto diei «u»o81 ii XXV'1 septerobfis mdcccxix' — marginal date/'Anno XX' residue inserted mid-phrase between 'diei' and the date.

### `bullarium-continuatio.volume-15.line-00041109` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'eccle- 1W» siae' and 'Ascia- MIM> no' — marginal fragments inside the hyphen-split words 'eccle-siae' and 'Ascia-no'.
- Inline marginal-summary fusion: page 1, left column, §. 1 'apice , Pwmiwa meritis licet' — marginal 'Prooemium' inserted mid-sentence.
- Inline marginal-summary fusion: page 1, left column, §. 3 'exponentes Tenor cob- spccialibus' and 'prosequi e"*k,mk- volentes' — marginal 'Tenor concessionis' inside 'spe-cialibus' and mid-sentence.

### `bullarium-continuatio.volume-15.line-00042121` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'sedes irmnuta- / *nno XX 7 r , ● * ,● ● ●« l / tae tucrunt' — marginal 'Anno XX' residue splitting the hyphen-split word 'immuta-tae'.
- Inline marginal-summary fusion: page 1, left column, §. 3 'exponentem , meew?M»ii ac s'nSu^ares personas' — marginal 'Tenor' residue inserted mid-sentence.
- Inline marginal-summary fusion: page 1, right column, §. 4 'li- cumuli »n- teras' and 'inte- UjSi- gros' — marginal 'Clausulae' residue inside 'li-teras' and 'inte-gros'; §. 5 'quatenus opus sit, Der<*»ti® fel. rec.' — marginal 'Derogatio' inserted mid-sentence.

### `bullarium-continuatio.volume-15.line-00042432.part-02` — CHANGES_REQUIRED

- Inline marginal residue fusion: page 1, left column, synopsis 'pro ar- d«l sia chiepiscopo' — marginal date fragment inside the hyphen-split word 'ar-chiepiscopo'.
- Inline marginal-summary fusion: page 1, left column, §. 1 'praedeces- Pro**®» sores' — marginal 'Prooemium' inside 'praedeces-sores'; §. 3 'magnifi- T— m , / centiam' and 'clariori e**»**"1» virtutum' — marginal 'Tenor' residue inside 'magnifi-centiam' and mid-sentence.
- Inline marginal-summary fusion: page 1, right column, 'Decernentes praesentes literas / i*«a. et< firmasq validas, et efficaces existerc ct / tSB IftllJus p * / .fore' — marginal 'Clausulae' residue splitting 'existere et fore'.

### `bullarium-continuatio.volume-15.line-00042432.part-04` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'eirphi- am* xx. tcuticandi' — marginal 'Anno XX' inside the hyphen-split word 'emphy-teuticandi'.
- Inline marginal residue fusion: page 1, left column, §. 1 'praefectorum jniMMiUi». congregationis' and 'sancti Jo- co» n.wfco» annis' — marginal fragments mid-phrase and inside 'Jo-annis'.
- Inline marginal-summary fusion: page 1, left column, §. 2 'fra- Te> ter', 'prae- piT^o fo- sentes' and 'inter- <u Mamuaiw dicti' — marginal 'Tenor' residue inside 'fra-ter', 'prae-sentes' and 'inter-dicti'; right column §. 3 'prae- tr.n«ni». decessorum' — marginal 'contrariorum' inside 'prae-decessorum'.

### `bullarium-continuatio.volume-15.line-00042432.part-05` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'et par- * 'SS™ t*3 lerrae' and 'aposto- *«« xx, lico' — marginal date/'Anno XX' residue inside the hyphen-split words 'par-tis' and 'aposto-lico'.
- Inline marginal residue fusion: page 1, left column, §. 2 'dioecesis in / «>«u»e « di- America' and 'rela- MMuUiriUoau tum' — marginal fragments mid-phrase and inside 'rela-tum'.
- Inline marginal-summary fusion: page 1, right column, §. 4 'constitutionibus, et d***»*»* «●» ordinationibus' and 'dictae U,,l*ru"' Quebecensis' — marginal 'Derogatio contrariorum' residue inserted mid-sentence.

### `bullarium-continuatio.volume-15.line-00045937` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, §. 1 'religio- cMcciiionii./ nem' — marginal 'Tenor concessionis' residue inside the hyphen-split word 'religio-nem' ('■«utr.ft tenor' precedes at the paragraph start).
- Inline marginal-summary fusion: page 1, left column, §. 2 'non etarferhlbMi' obstantibus' and 'Praesentibus d* perpetuis' — marginal 'Derogatio contrariorum' residue inserted inside 'non obstantibus' and mid-sentence.

### `bullarium-continuatio.volume-15.line-00046365.part-01` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'de K w*11 tempore' and 'pro incolis ci- ●«mo xx vitalia' — marginal date/'Anno XX' residue inside the hyphen-split word 'ci-vitatis'.
- Inline marginal residue fusion: page 1, left column, §. 2 'hisce cau- o* sis adducti' — fragment inside 'cau-sis'.
- Inline marginal-summary fusion: page 1, right column, §. 3 'severioris quadrage-Con4JUo#) | si malis' and 'ne- eU ve' — marginal 'Conditio' residue inside 'quadrage-simalis' and 'ne-ve'.

### `bullarium-continuatio.volume-15.line-00046365.part-02` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, §. 1 'Expositum Nobis nuper fuit, nui» cw-quod in' and 'non mo- / rtoniiii i . . / dico' — marginal 'Expositio precum' residue mid-sentence and inside the hyphen-split word 'mo-dico'.
- Inline marginal-summary fusion: page 1, left column, §. 2 'quae hinc Teeor eoo* oriri possent' and 'prae- a ** dictos' — marginal 'Tenor concessionis' residue mid-sentence and inside 'prae-dictos'.
- Inline marginal-summary fusion: page 1, right column, §. 3 'quadrage- c*«Nti»*<ij*. simalis' — marginal 'Conditio' residue inside 'quadrage-simalis'.

### `bullarium-continuatio.volume-15.line-00047648` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, synopsis 'destina- * tac' and 'in civi— *»»● ixi. tate' — marginal 'Anno XXI' residue inside the hyphen-split words 'destina-tae' and 'civi-tate'.
- Inline marginal-summary fusion: page 1, left column, §. 1 'parochus Sx^oHtio Pre- administrator' — marginal 'Expositio' inserted mid-sentence; §. 2 'exponen- Tmer cob tem' and 'praesen- ecMionit. ^eg j|oslrac Iaerae' — marginal 'Tenor concessionis' inside 'exponen-tem' and 'praesen-tes'.
- Inline marginal-summary fusion: page 1, left column foot to right column top, §. 3 'constitutioni- D*r°r*',o / . 3 ,.l . . . conlnriorucB / ; bus' — marginal 'Derogatio contrariorum' inside 'constitutioni-bus'.

### `bullarium-continuatio.volume-15.line-00047758.part-01` — CHANGES_REQUIRED

- Inline marginal-summary fusion: page 1, left column, §. 1 'in Chri- Ktpotuio 8l° filii' — marginal 'Expositio' residue inside the hyphen-split word 'Chri-sto'.
- Inline marginal residue fusion: page 1, left column, §. 2 'votis bc- *' nigne' and 'supra v&- Mem' — fragments inside 'be-nigne' and 've-stem'.
- Inline marginal-summary fusion: page 1, left column, §. 3 'Non obstantibus constitutionibus . , jjgg» apostolicis' — marginal 'Derogatio' residue inserted mid-sentence.

Each fused locus requires a source-owner boundary correction through a separately identified replayable derivative, then a new frozen render and fresh page review. Word-level body content was not altered or judged.

## Qualifications and nonblocking observations

- Historical running heads and page numbers printed inline within a body paragraph (e.g. `582 Bullarium` in `bullarium-continuatio.volume-06.line-00103790.part-05` page 2; `592 Bullarium` in `bullarium-continuatio.volume-06.line-00106172` page 3; `Boil. Rorn. "Porn. FI.` in `bullarium-continuatio.volume-06.line-00106661.part-01` page 1; `299 |` in `bullarium-continuatio.volume-06.line-00107940.part-01`; `Bull Rom. Tom. FI.` in `bullarium-continuatio.volume-06.line-00107940.part-02` page 2; `BuU. Ilum. Tom. XV.` in `bullarium-continuatio.volume-15.line-00038687`; `24?` in `bullarium-continuatio.volume-15.line-00040070` page 2) are recorded as retained historical furniture, not modern provider marks or marginal summaries.
- Literal issuer forms matching metadata and still intelligible are nonblocking: `Tijus PP. VI.`, `Pius PP. VM.`, `Pius pp. vn.`, `Pius PP. VU.`, `Pius PP. VH.`, `Pius PP VII.`, `Pius PP, VII.`, `Pius P?. VII.`, `Pids PP VII.`, `: Fius PP. VII.`, `! Pius pp. vn.`, `I Pius PP. VII.`, `Pius episcopus Servus senorum Dei`, and `Pius PP. Septimus 251` (stray page number). By contrast `Pius PP. v E "T` in `bullarium-continuatio.volume-06.line-00105289` loses the regnal designation and is a blocking issuer-clarity finding.
- `bullarium-continuatio.volume-06.line-00107940.part-02` (5 pages) and `bullarium-continuatio.volume-15.line-00014845` are Italian acts with Latin protocol/rubrics, labelled and disclosed accordingly.
- Sparse final pages of `bullarium-continuatio.volume-06.line-00103790.part-03`, `...part-04`, `...part-05`, `bullarium-continuatio.volume-06.line-00105289`, `bullarium-continuatio.volume-06.line-00106661.part-01`, `bullarium-continuatio.volume-06.line-00107940.part-02`, `bullarium-continuatio.volume-15.line-00020175`, `bullarium-continuatio.volume-15.line-00037789`, `bullarium-continuatio.volume-15.line-00039134.part-02` and `bullarium-continuatio.volume-15.line-00040070` carry genuine source text and natural dating before the apparatus; none is a colophon-only page.
- PASS documents in tome VI retain separate marginal caption blocks between paragraphs without inline body fusion. `bullarium-continuatio.volume-15.line-00039134.part-02` page 1 and `bullarium-continuatio.volume-15.line-00040070` pages 2-3 contain heavily corrupted body OCR runs that cannot be positively identified as marginal labels; these are recorded as literal OCR corruption (and `line-00040070` is CHANGES_REQUIRED on page 1 only).

## Individual page evidence

| Source ID | Page | PNG SHA-256 | Status | Observation |
| --- | --- | --- | --- | --- |
| `bullarium-continuatio.volume-06.line-00103790.part-01` | 1 | `0cbf99ff2861d367a2e9fdb710f41df8b81f43c48f6bba3b10159e5ed1c4eb15` | PASS | Two-line title, Pius PP. VI. and Latin match; unresolved date omitted. Literal body heading 'CDI.' and synopsis retained. Separate marginal/running blocks ('Dat. die 16. novembris 1783', 'Amno YIL', 'Pius PP. Sextus:') sit between paragraphs, not fused into a body line. Natural 19 November dating closes column 2 before source/rights apparatus. No clipping or glyph blocks. |
| `bullarium-continuatio.volume-06.line-00103790.part-03` | 1 | `4d19d0c2b71aaa36df8b03bc43132dff2188741f3b7d78370d75ce25c5a67c08` | PASS | Two-line title, Pius Episcopus and Latin match. Dense two-column body; retained 'Bullarium Romanum' running head and marginal captions ('Concessinuls Ienor.', 'Leges, et con- diliunes...', 'Clausula &u- blata...') appear as separate blocks, not fused into a body line. Literal OCR oddity 'DENIED:' in column 2 retained as uncorrected OCR. Margins/gutter clear. |
| `bullarium-continuatio.volume-06.line-00103790.part-03` | 2 | `e2a100684b9a40fe325ea28fd337ee5c537e3833de28bda168539aa488e08571` | PASS | Single-column continuation with retained marginal caption and 'Pius PP. Sextus' running head as separate blocks, non obstante clause and natural dating (19 November, pontificate year 8) before source/rights apparatus. Source-bearing final page; unused right column acceptable. |
| `bullarium-continuatio.volume-06.line-00103790.part-04` | 1 | `d70bcfc09e9ec3083d4ab137d0ce8678a64698eb88d43bb5e3067f2ec240256e` | PASS | Two-line title, Pius episcopus and Latin match; unknown date omitted. Synopsis, protocol and two-column body readable. Retained marginal captions and running furniture ('GCceca', 'Dat die af! uovembris 1589 Anno VIII.', 'Clausula salu- fares', 'Bullarium', '58o') stand as separate blocks; literal OCR marginal year not corrected. No clipping, overlap or glyph blocks. |
| `bullarium-continuatio.volume-06.line-00103790.part-04` | 2 | `24d908aacf8ba55074a27dcdb96e59c31d6ad161fdf1ea662c239e3fb1eb347f` | PASS | Single-column continuation with separate 'Romanum' running-head block, non obstante and sanctio clauses, and natural 'decimo kalendas decembris ... anno octavo' dating before source/rights apparatus. Source-bearing final page; unused right column acceptable. |
| `bullarium-continuatio.volume-06.line-00103790.part-05` | 1 | `8cb19b8ae32bdebb4af6208a8c96ba36d2fa0f5c60ecfd558aa4c4fa33817507` | PASS | Two-line title, Pius PP. VI. and Latin match. Literal heading 'CDVTI.', synopsis and two-column body readable; page number '581' and marginal captions ('Consuliur a- lumnis...', 'Clausula. sa. hluta...', 'Deragatio con Lrariorum,') retained as separate blocks. Literal OCR noise ('& n ERR', 'ADtOEen s') retained. No clipping or overlap. |
| `bullarium-continuatio.volume-06.line-00103790.part-05` | 2 | `c09a6b7691fcb33a6d4a65734ae4a8a232244391df786d8320cd2c181b5d7bd1` | PASS | Separate marginal blocks ('Dat. die 6 decembris / 1782 Auuo VIIE.', Clement XIV disposition note) precede the body continuation. Nonblocking qualification: historical page number/running head '582 Bullarium' is printed inline at the start of the continuation paragraph between 'de-' (p1) and 'rogatoriarum'; recorded as retained historical furniture, not a marginal summary or modern provider mark. Natural 29 November dating closes before source/rights apparatus. |
| `bullarium-continuatio.volume-06.line-00105289` | 1 | `2c7779ca749bd497eed7ab6bda69c80a0035b65e018ed078a04c455c7f99316a` | CHANGES_REQUIRED | Two-line title and Latin label match; unknown date omitted. Displayed issuer 'Pius PP. v E "T' matches metadata literally but is not an intelligible responsible-person identification. Body protocol, synopsis and two-column text readable; marginal/running blocks ('Prosmium', 'Tenor peecum...', 'Pius PP. Sextus', 'Bull. Rom. Tom. FI.', '585') stand separately. No clipping or overlap. |
| `bullarium-continuatio.volume-06.line-00105289` | 2 | `b220e40607d7235da79b0bc3ea58b3560444b9511f8bce3bd2ecfff1ba8fcc91` | PASS | Dense two-column continuation inside margins and gutter. Retained marginal captions ('Dddd', 'Tenor conces gionis', 'ClausnIs sala lares...', 'Derozatio con- irariorum.', '586') and running head 'H / Ballarium. Ronianum' are separate blocks, not fused into body lines. Non obstante clause flows into dating at foot of column 2. |
| `bullarium-continuatio.volume-06.line-00105289` | 3 | `ec7dcbb3afef1d130beea522db029bfd01375123b2f36e63335f92a66d02074c` | PASS | Sparse source-bearing final page: dating clause completes ('cima decembris ... anno octavo.') before the source/rights apparatus, which discloses rough OCR. Not a project-colophon-only page. |
| `bullarium-continuatio.volume-06.line-00106172` | 1 | `cde630bdabd59db9be50425628623e039baee2717a1726d9de58b624746e7865` | PASS | Two-line title, Pius episcopus and Latin match; unknown date omitted. Synopsis, protocol and two-column body readable. Retained marginal blocks ('Taxe desert- ptio...', 'Dat. die 16. decembris 1782 Auno VIIL', 'Procmnium', 'Batio exponi...', '59o', 'Bullarium. Romanum') stand as separate paragraphs between body segments, not fused into body lines. No clipping, overlap or glyph blocks. |
| `bullarium-continuatio.volume-06.line-00106172` | 2 | `ddae9442d182b734b0d65a229324ce666f338683f7654c74c1771c776ca408f0` | PASS | Dense two-column continuation within margins and gutter. Marginal caption 'Collatio pen- sionis...', running head 'Pius PP. Sextas' and page number '501' are separate blocks. Literal OCR fragments and short split paragraphs retained; no overlap or missing glyphs. |
| `bullarium-continuatio.volume-06.line-00106172` | 3 | `4d34e9b25978b457fddb5c783c422e870628d89558fc7e74567024aff3673250` | PASS | Final page carries substantive body, decrees and natural dating ('de- cimo-septimo kalendas jaunsrii ... anno octavo') before source/rights apparatus in column 2. Separate marginal captions retained. Nonblocking qualification: historical page number/running head '592 Bullarium' is printed inline at the start of the column-1 paragraph between 'festivis' and 'diebus'; recorded as retained historical furniture, not a modern provider mark or marginal summary. |
| `bullarium-continuatio.volume-06.line-00106661.part-01` | 1 | `3ab6e1445f4a6f66eca4cf05859bf1cbf2c33cee94350d62fdafa309c5ab4507` | PASS | Two-line title, Pius episcopus and Latin match; unknown date omitted. Synopsis, protocol and two-column body readable. Marginal blocks ('Sanctio posna-', 'Jat. die 10 deoerhrid 11782 Anno VIII.', 'Proemium.', 'Expesitio pre- cum.', 'Pius PP. Sextus', 'Tenor conees- 51o&g13.', '595') stand separately. Nonblocking qualification: running head 'Boil. Rorn. "Porn. FI.' is printed inline in column 2 between 'con-' and 'sensum'; recorded as retained historical furniture. No clipping or overlap. |
| `bullarium-continuatio.volume-06.line-00106661.part-01` | 2 | `19e8166d3cac6b6fda935a0b1758f93ffe0d1962afa82b546d99fd4e5cc10a23` | PASS | Single-column continuation: decree, non obstante, sanctio and natural dating ('tertio decimo kalendas ja- nuarii, pontificatus Nostri auno octavo') before source/rights apparatus. Source-bearing final page; unused right column acceptable. |
| `bullarium-continuatio.volume-06.line-00107940.part-01` | 1 | `fee95bf999777b0bd2ae899095ab58a85b5b73d8b07b98cbc06852958e7f6a38` | PASS | Two-line title, Pius PP. VI. and Latin match; unknown date omitted. Complete short brief in column 1 with synopsis, address, grant and natural dating ('die xxv. Ja- nuarii MDCCLXXXTIL ... anno octavo') before source/rights apparatus; right column empty after natural end. Nonblocking: historical page number '299 \|' printed inline at start of a body paragraph between 'monialium' and 'ordinis'. No clipping or glyph blocks. |
| `bullarium-continuatio.volume-06.line-00107940.part-02` | 1 | `a25e16d3e6bc8e948ffc900a453fe8694aa963d2bd613f4d43586c9c73bb4857` | PASS | Two-line title and label 'Italiano (protocollo e rubriche latini)' match the it metadata and the source note's Latin protocol/rubrics disclosure; unknown date omitted. Displayed issuer 'Tijus PP. VI.' is the literal metadata and remains recognizable with regnal number intact (nonblocking literal OCR). Latin rubric and motu proprio heading, Italian body in two columns; 'Bullarium. Romanum' running head separate. No clipping or overlap. |
| `bullarium-continuatio.volume-06.line-00107940.part-02` | 2 | `4e033105a9daac0ac6354f49d963ebfae18e5aa8b3827d7b4bea0509564528c1` | PASS | Dense two-column Italian continuation within margins/gutter. Latin marginal rubric, garbled marginal line 'CI eium LA re fumafein...' and 'Pius PP. Sextus 601' are separate blocks. Nonblocking qualification: running head 'Bull Rom. Tom. FI.' printed inline at end of a column-2 sentence between 'delle' and 'teoute'; recorded as retained historical furniture. |
| `bullarium-continuatio.volume-06.line-00107940.part-02` | 3 | `37ff1025617f37e3fe656d0b6854cd1f20988dad18d806153d396686384cc552` | PASS | Two-column continuation with Latin marginal rubrics ('Declarationes gpoeiales.', 'De jure re- stringendi...', 'Quid deficien...', 'Monitum ad...', 'Quod pacta...') and running heads ('602 Bullarium', 'Romanum', 'Pius PP. Sextus') as separate blocks. Literal OCR noise retained. No clipping, overlap or glyph blocks. |
| `bullarium-continuatio.volume-06.line-00107940.part-02` | 4 | `18af6af6b83802c6ccd73082237bc8a5a7d278bfa5cdede4fbb98826e1cfc912` | PASS | Two-column continuation of sections 8-11; running head 'Bull. Rora. T'om. FI.' and closing marginal rubrics ('Fffiilz', 'Do jure pricu hs...', 'Clausulie salu- lar&e...', 'Tat. die 4. februarii 1783 [Anno VII', 'Prosmium. -') stand as separate blocks. Literal marginal date retained without inference. No clipping or overlap. |
| `bullarium-continuatio.volume-06.line-00107940.part-02` | 5 | `94b60b8dff87a953a3c4f0455944f02a8d9738f30736279f6c70645490cabd94` | PASS | Sparse source-bearing final page: marginal 'Expositio pre- £u.' and page number '604' precede the derogation and natural Italian dating 'Dato dal Nostro palazzo apostolico Vaticano questo di 25. gennaro 1783.' before source/rights apparatus disclosing Italian motu proprio with Latin protocol. Not a colophon-only page. |
| `bullarium-continuatio.volume-15.line-00010973` | 1 | `1803da19dd7b2176b152b9033ece2f98f87382d6548fb0ca9442e5c4514ea524` | PASS | One-line title, displayed issuer 'Pius Papa VII.' and Latin match metadata; unknown date omitted. Heading DCCLXXXVIII, synopsis, address and complete letter in column 1; literal bullet/punctuation OCR noise lines ('knnu XIX ● . . . .', '.● 1 . ●; y ...') rendered as visible glyphs, not tofu. Natural dating '... pontificatus No- stri anno decimo nono.' opens column 2 before source/rights apparatus. |
| `bullarium-continuatio.volume-15.line-00011979.part-02` | 1 | `ea641803ae29d66c8ba655141d532b23feb44ab2717b0207fb29f29fa569e71e` | CHANGES_REQUIRED | One-line title and Latin match; unknown date omitted. Displayed issuer 'Pius PP. VM.' is the literal metadata (single-glyph OCR variant of the regnal numeral; name intact; nonblocking). Two-column layout, margins and gutter clean; black-square/bullet OCR glyphs render as glyphs, not tofu. Natural dating '... anno decimo nono.' precedes source/rights apparatus in column 2. Marginal labels are fused into body sentences/words (see findings). |
| `bullarium-continuatio.volume-15.line-00014845` | 1 | `231ce7de6e3f43c0bc74bdbc2eb9c598dfccd47ee8c601f734134b4fb77e9a04` | CHANGES_REQUIRED | One-line Latin rubric title, displayed issuer 'Pius pp. vn.' (literal metadata; recognizable OCR of VII) and Italian label match; unknown date omitted. Leading marginal date fragments ('oti 4»', 'Aa» XIX.') sit at synopsis start/separate blocks (acceptable). Natural closing 'Dato dal Nostro pa- lazzo apostolico Quirinale questo dl 22 luglio 1818.' and 'Pius PP. VII.' in column 2 before apparatus. No clipping, overlap or tofu; marginal residue fused into body sentences (see findings). |
| `bullarium-continuatio.volume-15.line-00020175` | 1 | `96960b9af3a1459ea89957d4b6f2204595781465b9d5af7ec7cd64bf979e862c` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCV, synopsis, address and two-column body; margins/gutter clean, black-square glyphs render, no clipping or tofu. Body continues to page 2 dating. Marginal labels/residue fused into body words and sentences (see findings). |
| `bullarium-continuatio.volume-15.line-00020175` | 2 | `469e0c36290cffce2889eae84d94f40cd948699045ae82ca8378d615605d12ad` | PASS | Sparse source-bearing final page: genuine dating clause 'Datum Romae apud s. Mariam Ma- jorem ... die vicesima quarta julii MDCCCXVI11 pontificatus No- stri anno dicimo nono.' precedes source/rights apparatus. Literal date OCR not normalized. Not a colophon-only page. |
| `bullarium-continuatio.volume-15.line-00020320.part-02` | 1 | `f5ea63e8ac22d09233c44653da21946b75b96d58b1d9f9782f2b9a9b61e91787` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCVU., synopsis, protocol and two-column body; natural dating '... anno de- cimo nono.' in column 2 before apparatus. Margins/gutter clean; no clipping or tofu. Marginal labels fused into body (see findings); 'Fipotitip S- 2.' sits at a paragraph start. |
| `bullarium-continuatio.volume-15.line-00020320.part-03` | 1 | `3d4ea55db27e36379a0d43618610de5685a3f01197043cd379813c604f004a71` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Synopsis, protocol and §§ 1-4 in two clean columns; natural dating '... pontificatus Nostri anno decimo nono.' before source/rights apparatus. No clipping or tofu; one inline marginal fusion (see finding). |
| `bullarium-continuatio.volume-15.line-00020666` | 1 | `efd85cd02fb7e94f95184ec591d3019e6bcbbe0253b314ceb5fa75534982528d` | CHANGES_REQUIRED | Two-line title and Latin match; displayed issuer 'Pius PP. VU.' is literal metadata (single-glyph OCR of VII; nonblocking). Unknown date omitted. Two-column brief with natural dating '... anno de- cimo nono.' and apparatus in column 2; separate marginal block 'eonlrirlorum. .. . .r ...' also retained. No clipping or tofu; inline fusions as listed. |
| `bullarium-continuatio.volume-15.line-00020760` | 1 | `f974c77eeec936fa25c8940ecf2fa51da08489cd6caa5cf60a401d19c883ca2a` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Two-column body; natural dating '... anno decimo nono.' then source/rights apparatus in column 2. No clipping or tofu. Separate marginal blocks in the synopsis are acceptable; inline fusions listed in findings. |
| `bullarium-continuatio.volume-15.line-00020888` | 1 | `430111aaa4dac926c0ac5d7faf5f8d42ad2400678161e65a5c1933fb876a28c0` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCXI, synopsis, protocol and two-column body; natural dating '... anno decimo nono.' then apparatus in column 2. Margins/gutter clean, no clipping or tofu; inline marginal fusions listed. |
| `bullarium-continuatio.volume-15.line-00021431` | 1 | `57b35a5c75741f914438f406fa558c887f6b91d1e2654ff4b2dd41dad4855fc0` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCXIV, synopsis, address and brief in two columns; natural dating '... anno decimo nono.' then source/rights apparatus. Margins/gutter clean; no clipping or tofu. One inline marginal fusion (see finding). |
| `bullarium-continuatio.volume-15.line-00022610` | 1 | `3c030ec50bacfaea1d37313cbadcf4a8020b30d6d26a53894afbb0fea16d2332` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCXX, address, salutation and two-column body; natural dating '... anno decimo nono.' then apparatus. 'Deropuo' at a paragraph start is acceptable placement. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00022854.part-01` | 1 | `98dcf3c4edcd365922e62f6ed758da615136d3d77630ac8971e0d2000a4f53a6` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCXXII, synopsis, address and two-column body; natural dating '... anno decimo nono.' then apparatus. Margins/gutter clean; no clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00022854.part-02` | 1 | `6b476b469c3c001833a7f20c7bec321a769e6e5bed1ad7a33140e2fde99c1646` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCXXIIU., synopsis, address and two-column body; running head 'Butt. Rom. Tom. XV.' inline at foot of column 1 and separate marginal date blocks ('17 travnuiiris ISIS', '●txuo XIX') retained. Natural dating '... anno decimo nono.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00023187.part-01` | 1 | `539a5dd17ae9b6aac34d669a2c24eb1d0386079b913f26eff64f92a78363a091` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCXXV., protocol, two-column body with page number '131' and running head 'Pius PP. Septimus' as separate blocks; natural dating '... anno de- cimo nono.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00023187.part-02` | 1 | `d54320d6ce64b31a74c78f4b52c4539b79315cf614e7c51df3b12450a5e32972` | CHANGES_REQUIRED | Two-line title, Pius episcopus and Latin match metadata; unknown date omitted. Heading DCCCGXXYI., protocol 'Pius episcopus Servus servorum Dei', two-column body and natural dating '... quinto kalendas decembris ... anno decimo nono.' before apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00024897.part-02` | 1 | `4f535a826b1a2a6a60c4eccf333004c7edfaa865b5df75855359ff34e19b0a5a` | CHANGES_REQUIRED | One-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCXXX1, protocol, two-column body; 'Proemian' and '^Eipoduopr*-' at paragraph starts are acceptable placements. Natural dating '... anno decimo nono.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00026610` | 1 | `072dc1f6b8a8cca56e31c36405029c7ad24eacd53b1762ad943c764c3a13d299` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading dccc xxxv., synopsis, address and two-column brief; natural dating '... anno decimo nono.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00026701` | 1 | `2d7c9c0b6c1a08cc3e93c3f7f5735ae2047c69cecda6a79303df721bc0997ff9` | CHANGES_REQUIRED | One-line title and Latin match; displayed issuer 'Pius PP VII.' is literal metadata (missing period; nonblocking). Unknown date omitted. Separate marginal date lines ('n.i. di*', '12 Jinnarti - . r r n ,') retained. Natural dating '... anno de- cimo nono.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00030230` | 1 | `57b3c9ab64f49250d6ed80f1235afe0eb8998f1db9f07b834f5a893f02861590` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading IDCCCXLV, protocol and dense two-column body; natural dating '... anno decimo nono.' then apparatus at foot of column 2, all within margins. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00035412` | 1 | `2cfb14442ae2fe3ae8ac9df8aecaea556e720e76c183743a28f8d7f3bef08875` | CHANGES_REQUIRED | One-line title, displayed issuer 'Pius PP. Septimus' and Latin match; unknown date omitted. Consistorial allocution DCCCLXII in column 1 with 'Quid vobis videtur ?' and creation formula; closing 'In Nomine Patris ... Sancti Arnen.' in column 2 before apparatus (natural source closing). Literal OCR noise ('ijjt', '>36', 'tjg') retained. No clipping or tofu; one inline fusion in synopsis. |
| `bullarium-continuatio.volume-15.line-00036542.part-01` | 1 | `5dd48233846a7e1fdebeef26ece92e6d697ba38b30b1224864532ef1d5ca5edc` | CHANGES_REQUIRED | Two-line title and Latin match; displayed issuer 'Pius PP. vn.' literal metadata (recognizable OCR of VII). Unknown date omitted. Heading DCCCLXVIII, synopsis, protocol, inserted decree dated 'Die 15 maii 1819', two-column body and natural dating '... anno vi- c esimo.' before apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00036542.part-02` | 1 | `f3c268dc4516313d1a02bd0148dd81ab6496e6f41fa6de4ee626fc5540824e32` | CHANGES_REQUIRED | One-line title and Latin match; displayed issuer 'Pius PP. VU.' literal metadata (single-glyph OCR of VII). Unknown date omitted. Heading DCCCLX1X., protocol, brief in column 1; natural dating '... pontificatus Nostri anno vi- \|( ceaimo.' tops column 2 before apparatus. Synopsis/paragraph-start marginal fragments ('m j'obh', 'Imoxx.', 'Expowuopn-') sit at line starts. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00037369` | 1 | `ce6ceceecb5968b59fa7f20a8474f5003e00392f089ac976b9551cba97789dd8` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Short brief DCCCLXXV in column 1 with natural dating '... pontificatus No- stri anno vicesimo.' followed by source/rights apparatus in the same column; right column intentionally empty. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00037789` | 1 | `673aae5dadd34627dd9e5ee20badef037cd5cdeaf19ab0d1f08ebc37ed22aae7` | CHANGES_REQUIRED | One-line title and Latin match; displayed issuer 'Pius episcopus Servus senorum Dei' is literal metadata with intelligible issuer. Unknown date omitted; marginal 'D«t dia 18 julU 1819 / Anno XX' stands as separate blocks. Dense two-column bull; separate marginal block 'Deputilio exe- ...' and running head '232 / Pius PP. Septimus' retained. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00037789` | 2 | `8ecb88dce99c37889de84d39a2ca5c6ce6491a0404ff11172f5c66cfe5baef47` | CHANGES_REQUIRED | Single-column continuation page: clauses, sanctio and natural dating 'Datum Romae ... quinto decimo talendas angu- sti, pontificatus Nostri anuo vicesimo.' before source/rights apparatus (source-bearing final page; unused right column acceptable). No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00038131` | 1 | `3412df327a5fad44b25c0045c1d43a645ae7681e3d5f4334c8fc259979c2bf36` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCLXXX., address, salutation, §§ 1-2 and dating start in column 1; dating completes '... anno vi- cesimo. / ,' at top of column 2 before apparatus. Separate OCR-noise lines retained as visible glyphs. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00038687` | 1 | `dadcb3604bb02f57506747992790e1f639a829601cda5b86e74e4b007cfe4642` | CHANGES_REQUIRED | Two-line title, displayed issuer 'Pius PP. VII' and Latin match; unknown date omitted. Heading DCCCLXXXIV, address, two-column body; running head 'BuU. Ilum. Tom. XV.' printed inside 'excommunicatio-nis' (historical furniture). Natural dating '... anno vicesimo.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00039134.part-02` | 1 | `d5489130f278e184ccb2fa4f418fa874b904cb7b08a51decddb26679d9ab9145` | PASS | Two-line title, displayed issuer 'Pius PP. Septimus' and Latin match; unknown date omitted. Heavily corrupted literal OCR synopsis/address/salutation lines ('ConuBUCioitio ...', 'Ri!inrlrt...', 'ui «*»● W I ●«') retained as visible glyphs. Long letter flows across two columns; running head 'Bullarium Romanum' and page number '242' stand as separate blocks. Garbled body runs (e.g. ',or4m9l's', 'di™ neor urn regem') cannot be positively identified as marginal labels and are recorded as literal OCR corruption. No clipping, overlap or tofu. |
| `bullarium-continuatio.volume-15.line-00039134.part-02` | 2 | `e15dc2ba3c8f001fb5fa3668c8d62fd47e6943f413b278c8b55bdba577146cc0` | PASS | Single-column continuation completing the letter: natural closing 'Datum Romae, apud sanctam Mariam Majorem ... pontificatus Nostri anno vicesimo.' before source/rights apparatus. Source-bearing final page; unused right column acceptable. No clipping, tofu or recognizable marginal fusion. |
| `bullarium-continuatio.volume-15.line-00039947` | 1 | `d713df9e416530b39f136cc30902db754a5cde0fcc11698a00997840da1b3375` | CHANGES_REQUIRED | One-line title and Latin match; displayed issuer ': Fius PP. VII.' is literal metadata (leading colon and F-for-P OCR; regnal number intact, nonblocking). Unknown date omitted. Two-column body with running head 'BuHarium Romanum' and page number '62' as separate blocks; natural dating '... Nostri an- no vicesimo.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00040070` | 1 | `b92b0dea63c551f64b9feaafe0231f1389e74719b414832095de775e2d859f4f` | CHANGES_REQUIRED | Two-line title, displayed issuer '! Pius pp. vn.' (literal metadata; recognizable OCR of Pius VII) and Latin match; unknown date omitted. Heading DOCCXC., synopsis, address and dense two-column body; running head 'MmiI / Pius PP. Septimns' as separate blocks. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00040070` | 2 | `87f1c679c503cd68d4b9ae64f9e7820dd1dd499777328af04c4ff7b8d285c855` | PASS | Dense two-column continuation inside margins. Historical page number '24?' splits 'superio-ribus' and separate blocks 'Tenor coarta lieni».', 'Bullali uni Romanum', 'm' sit between paragraphs (retained historical furniture/marginal blocks, not inline fusion). Heavily corrupted OCR runs (e.g. 'ConsUqtiqDsi diqpeeK', 'No^trq,,^ epo^tQr licae') are not positively identifiable as marginal labels and are recorded as literal OCR corruption. No clipping or tofu. |
| `bullarium-continuatio.volume-15.line-00040070` | 3 | `f5d634b6f9a3e50981226d2be359239b0ae0ff777e57c878a14e4cb1ff17d2cf` | PASS | Final page (single column): continuation, §. 6 clausulae and §. 7 derogation, natural dating 'Datum Romae ... die vice- sima Septembris ... pontificatus Nostri anno vicesimo. /' then separately retained marginal blocks ('ClaaiuU >o< hiat, , «I de- cretum irri- tant', 'D*roga:tocoB- trarlanim') before source/rights apparatus. Source-bearing, not colophon-only. Corrupted derogation words ('general'busriyel SP®"', 'derogato-r riaijijm Rogatori is') read as literal OCR corruption of the body, not positively identifiable marginal labels. No clipping or tofu. |
| `bullarium-continuatio.volume-15.line-00040917` | 1 | `b38e611f1c9a5a71552dcff8fb3dab236479759f405af7fa3fe94e139ba266aa` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCXCIII., protocol, two-column body; 'a«uo coo ce»- S- 1-' at paragraph start (acceptable). Natural dating '... pontificatus Nostri an- no vicesimo.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00041050` | 1 | `e1ba8fda5ed8b61d7007f3d858b85944fc0c11001ec5187429ebb486b1376163` | CHANGES_REQUIRED | Two-line title and Latin match; displayed issuer 'Pius PP. Septimus 251' is literal metadata carrying a stray historical page number, issuer still intelligible (nonblocking qualification). Unknown date omitted. Complete consistorial allocution DCCCXCIV in column 1 ending 'In nomine Patris, et Filii, et Spiritus Sancti. Arnen.' followed by apparatus; right column empty after natural end. No clipping or tofu; one synopsis fusion. |
| `bullarium-continuatio.volume-15.line-00041109` | 1 | `0fb83e538fea05e2f56952014cbdadf17a74166b057cff0b799fabe746143cc0` | CHANGES_REQUIRED | Two-line title, displayed issuer 'Pius PP, VII.' (literal comma; nonblocking) and Latin match; unknown date omitted. Heading DCCCXCV., two-column body; natural dating '... anno vicesimo.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00041224.part-02` | 1 | `201412cd9a84452b899d2ca567607cf26b0be629ae8a7042b2a372bb8c093b64` | PASS | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading DCCCXCVH., synopsis, address and §§ 1-3 flow cleanly across two columns; natural dating '... anno vicesimo.' then apparatus. Isolated literal glyph noise ('\|', '\\', '●' in 'synoda- ● libus', single 'D' at the start of 'D tate') is not a recognizable marginal label; no inline marginal-summary fusion identified. No clipping or tofu. |
| `bullarium-continuatio.volume-15.line-00042121` | 1 | `aa737b1eadc1c011bd551e7a9fa81141ad57014af02f7a591f2583a20f97df89` | CHANGES_REQUIRED | Two-line title and Latin match; displayed issuer 'Pius PP. VH.' literal metadata (single-glyph OCR of VII; nonblocking). Unknown date omitted. Heading DCCCIC., protocol, two-column body; natural dating '... anno vicesimo.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00042432.part-02` | 1 | `920d0cf90b6d634e72c3e30096ba4fc6aa81a8c71aff91572e67786a8ac9b6b0` | CHANGES_REQUIRED | One-line title and Latin match; displayed issuer 'I Pius PP. VII.' is literal metadata with stray leading 'I' (issuer intelligible; nonblocking). Unknown date omitted. Heading CMI, protocol, two-column body; page number '263' and running head 'Pius PP. Septimus' as separate blocks; natural dating '... anno vicesimo.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00042432.part-04` | 1 | `4b6ee9575ffedf982791c9ff99d91dc1c3fa7ae1273f7f00533c404555ced612` | CHANGES_REQUIRED | Two-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading CM11I., protocol, two-column body; natural dating '... pontificatus Nostri anno vicesimo.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00042432.part-05` | 1 | `8c956524aacfe722c9fa727ab825ae19134af6b3f175ac8fb112916084e1cb29` | CHANGES_REQUIRED | One-line title and Latin match; displayed issuer 'Pius pp. vn.' literal metadata (recognizable OCR of VII). Unknown date omitted. Heading CM1V., protocol, two-column body; running head 'Bul. Bom. T. XV.' inline at foot of column 1 (historical furniture). Natural dating '... anno vi- cesimo.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00045937` | 1 | `ed87cd142af5ab13def78733430461c76dcd1ce673974f60b1c588921ce5627d` | CHANGES_REQUIRED | One-line title, Pius PP. VII. and Latin match; unknown date omitted. Short brief CMVI in column 1 with natural dating '... pontificatus Nostri anno vicesimo.' followed by apparatus; right column empty after natural end. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00046365.part-01` | 1 | `4eec9e1fe9602ae8aa4680c41d13e7ef5a5b196995cfeeb38b74c6a6d22ed1c6` | CHANGES_REQUIRED | One-line title and Latin match; displayed issuer 'Pius P?. VII.' literal metadata (question-mark OCR glyph; issuer intelligible, nonblocking). Unknown date omitted. Heading CMX., address, two-column body with running head 'JBuU. Rom. Tom. XV.' at a paragraph end; natural dating '... anno vicesimo.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00046365.part-02` | 1 | `36c5ef7761788e9f6a5102a8170cf62c360ef61bb7eba4867afd3ce184b8349c` | CHANGES_REQUIRED | One-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading CHXI., address, two-column body; natural dating '... pontificatus Nostri anno vicesimo.' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00047648` | 1 | `e941a824b971f41765f5f6e2f671180a99ad32266dc82359be6bb7d47b8d2f9c` | CHANGES_REQUIRED | Two-line title and Latin match; displayed issuer 'Pids PP VII.' literal metadata (OCR of Pius; regnal number intact; nonblocking). Unknown date omitted. Heading CMXVII., address, two-column body; natural dating '... anno vicesimo primo. ● .' then apparatus. No clipping or tofu; inline fusions listed. |
| `bullarium-continuatio.volume-15.line-00047758.part-01` | 1 | `6a31d10c5f0d3a3fcf1e053093685233e3c58f75fe9b9e891ebb8e5c7ff84985` | CHANGES_REQUIRED | One-line title, Pius PP. VII. and Latin match; unknown date omitted. Heading CM XVIII, protocol, two-column body; natural dating '... pontificatus Nostri aoim \\iccsimo primo.' then apparatus. No clipping or tofu; inline fusions listed. |

## Limitations

These are literal uncorrected, uncollated historical OCR reading editions. This is a layout review only: it does not collate words against an original printing or facsimile, authenticate historical wording, establish juridical interpretation, independently adjudicate provenance or rights, or normalize historical dates; unresolved dates were not inferred. Odd issuer spellings and character noise remain as disclosed limitations unless they defeat responsible-issuer identification. Upstream canonical admission, zero-marker scan and source-fidelity/font checks were accepted within the assigned contract. PASS and CHANGES_REQUIRED concern only the hash-bound visual review extent stated here and make no publication or installation claim.
