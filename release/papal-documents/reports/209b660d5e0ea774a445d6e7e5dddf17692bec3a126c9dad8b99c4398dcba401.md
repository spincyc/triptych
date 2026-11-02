# Bullarium Romanum vol. VII reading-order visual review 02 (batch bullarium-ro-0002)

**25 PASS, 2 CHANGES_REQUIRED** of 27 assigned PDFs; 60 pages individually opened at full raster size with the Read tool, zero reused. Both CHANGES_REQUIRED findings are printed page-foot notes emitted inside a body paragraph (addendum (b)); no marginal-summary fusion was found. Scope: lane 02 of review batch `bullarium-ro-0002`, coordinate-reconstructed (whole-volume reading-order derivative `reading-order-c906c8a9a6ff`) readers of the Turin 1862 Bullarium Romanum, volume VII (Pius IV and Pius V acts). Review date 2026-10-28.

## Scope and method

Each assigned PNG produced by the repository `pdf-review` run was opened as its own full-size image (1700x2200 raster) with the Read tool before its observation was recorded; no contact sheet, thumbnail, new rasterization, source acquisition, word-level collation, text correction or date reconstruction was performed. One JSON observation per page was appended to the lane ledger `observations.jsonl` after viewing.

Each page was checked for the displayed title, responsible issuer, Latin label and omission of the unresolved act date against the frozen metadata; headings, two-column flow, gutter, margins, glyphs, clipping and overlap; natural source closing; modern digitizer signatures; raw placeholders; and, per the Bullarium reading-order addendum, (a) marginal summaries as separate TAB-led blocks never fused into a body sentence or hyphen-split word, (b) page-foot footnotes as separate blocks at the page break, (c) natural two-column order, (d) inline running heads/folios/signature marks and misplaced but separate marginal blocks, (e) fragment presentation. No assigned document is a fragment (all `extent_kind` = `printed-act`), so (e) does not apply. No document carries a `prior_finding`.

Mechanical support (read-only, lane-local scripts `mech.py`, `fn.py`, `fn2.py`): each document's selection was split into paragraphs from the reading-order derivative `hybrid.txt` at the manifest line ranges. It contains **292 TAB-led marginal paragraphs**; no source paragraph mixes TAB-led and body lines (0 mixed paragraphs). 12 marginal blocks sit between the halves of a hyphenated body word (separate blocks; addendum (d) placement qualifications). At least 52 running-head, folio or signature-mark lines are inline (qualifications). Every lane PDF log has 0 `Missing character` entries; no `Google`/`Digitized` string or bare `None` occurs in any lane body TeX; every receipt `text_fidelity` status is `pass` with no warnings. The note scans located the two in-paragraph notes confirmed visually. This support does not replace the visual review.

Note blocks seen: 24 printed page-foot notes, 22 set as separate blocks (unit 0055 carries two notes in one note block, not mixed with body) and 2 fused into body paragraphs (units 0040 and 0081). Marginal blocks: 292 TAB-led blocks, every one emitted as its own paragraph; fusion count 0.

## Evidence verification

All assigned PDF, receipt, frozen-manifest and raster-run digests, and every assigned page PNG digest, were computed before and after inspection and matched the assignment pins both times (90 files; the before and after verification records are byte-identical).

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt `.scratch/typeset_pipeline/claude/bullarium-ro-0002/receipt.json` | `6abaf3f0a23aecea64d5a76485c69926ade5926fd2b88a89840f787ded6bc46a` | Before and after |
| Frozen manifest `.scratch/typeset_pipeline/claude/bullarium-ro-0002/frozen-manifest.json` | `ce384dfe75cde78b6427f00c878a870507a47e1a9422408dbfa0bfefb0d7b11a` | Before and after |
| Raster run `.scratch/claude-review/rasters-bullarium-ro-0002/review-run.json` | `d91c149a7573666400708bd0104faa48443b257929563ed9769ee787ec4f7a20` | Before and after |
| Lane assignment | `04b4381e9b45eb24ec7b5ae45cd38a4fb3f0b9d42b334b11551541274bf0ca1e` | Scope binding, unchanged |
| Before verification record | `c5ec64d4bb710a26216300367bd0e547d02e952ac41c9e9f61d6534a5f091207` | PASS |
| After verification record | `c5ec64d4bb710a26216300367bd0e547d02e952ac41c9e9f61d6534a5f091207` | PASS; identical digests |
| Inspection ledger `observations.jsonl` | `b13001f62ee7ebb28dec536f3053d3a056e25cb82b7959995fb8b35d0117fb29` | 60 unique page observations |
| Mechanical extraction `mech.json` | `37cce134459168ac6e3e6e23e194b97b8277236dcdcfe2c267fbc715c15f61bb` | Marginal/note/running-head scan |
| Note scans `footnotes.json` / `footnotes-broad.json` | `f39b6e64efb4742506ac926c3c42adeee1f06aaf95352ba5c1ec560d8cac56e2` / `c4d5d8d25b1df9cc0a1254635023469f46d7e11b86361782ae9b90f5985f47db` | Note paragraph membership |

## PDF outcomes

All documents display "Latin" and omit the unresolved act date. Issuer lines reproduce the printing's OCR protocol formula as frozen; OCR-damaged spellings that still identify the pope are qualifications.

| Document | Pages | PDF SHA-256 | Marginal blocks | Status |
| --- | ---: | --- | ---: | --- |
| `bullarium.volume-07.unit-0038.part-02.reading-order` | 3 | `e67eba449d7fea67ecc5674e609e105b72281508b6d541cac23e3e4734bc4168` | 16 | PASS |
| `bullarium.volume-07.unit-0040.reading-order` | 4 | `e676e48c2c6e4c959de5a7f3dbda89653a39d12443dd3a0f2b7f89f95d49b609` | 19 | CHANGES_REQUIRED |
| `bullarium.volume-07.unit-0041.reading-order` | 2 | `e916509882449b769a67c0660f1887c3a3f9e5ab650bd3575264f3ff5896c99e` | 8 | PASS |
| `bullarium.volume-07.unit-0042.reading-order` | 3 | `b0091f9e29396f91c44d646c0952ace0df3487b53989edf8d9da16331d894edc` | 13 | PASS |
| `bullarium.volume-07.unit-0043.reading-order` | 2 | `313e53e8ea2d06a63173d21ee67bf4ed0ec6c113813195da9596417c40c4c078` | 6 | PASS |
| `bullarium.volume-07.unit-0045.reading-order` | 3 | `86963d0cc4dac15f42ef01c5bc55b156e573786c730122b724893448f149c8b9` | 2 | PASS |
| `bullarium.volume-07.unit-0046.reading-order` | 2 | `e7ac94868a846f1b47040bb369b643d937dfb25616a609688327ea0cdfb3b690` | 8 | PASS |
| `bullarium.volume-07.unit-0049.part-02.reading-order` | 1 | `8de88861e51c2884450e00507a672525c561842f2591f43c312a37c67448bee7` | 4 | PASS |
| `bullarium.volume-07.unit-0052.reading-order` | 3 | `ce30c7c3f730192b6fc2e1478be931c29c043be5dec9f02fd1eb1fe9b8e5030c` | 10 | PASS |
| `bullarium.volume-07.unit-0053.reading-order` | 8 | `46bd13ec746e5783fb0e6302ed3192b87ed344de4f46e394754f6b1a39427304` | 86 | PASS |
| `bullarium.volume-07.unit-0055.reading-order` | 2 | `37170491154916412e2f6d591173aa87c291bcf77e6f30167d56a8f5261bb0f1` | 8 | PASS |
| `bullarium.volume-07.unit-0059.reading-order` | 2 | `2dcfc21a002b4fb1f318de82082c9bb6b21ef252b3f243f9045051b169975f5a` | 10 | PASS |
| `bullarium.volume-07.unit-0063.reading-order` | 2 | `1cfbe0bdf662b88ddd48d05ec8e25f67b8c071571d3984fca17d573da2ad82e8` | 4 | PASS |
| `bullarium.volume-07.unit-0067.reading-order` | 2 | `8775aa112ab13a7c94c665e04f9884c69645e9be4902678f1bb70485459c5383` | 8 | PASS |
| `bullarium.volume-07.unit-0080.reading-order` | 2 | `51e55a0992caf8d4f7a75df387e63ed5710a6a594f213457a5c66bdd21f58430` | 11 | PASS |
| `bullarium.volume-07.unit-0081.reading-order` | 2 | `a55ba18eb44e38200b51ed19fff36e22e725ade590f2e8d049c27c6a263c72cb` | 6 | CHANGES_REQUIRED |
| `bullarium.volume-07.unit-0091.reading-order` | 2 | `98674319f4c4ada37af4998227f6a7494f9b4e208ba68d05e5cbb032d8590c6e` | 11 | PASS |
| `bullarium.volume-07.unit-0094.part-02.reading-order` | 2 | `91afc863bf3f037747d4068955e8fc335ed2b13cf85fe162a3c4a8a5c3741276` | 8 | PASS |
| `bullarium.volume-07.unit-0094.part-03.reading-order` | 1 | `4cd2d12a89c12794f5710bd4e4a8bea4738180a8dc2a491f368b0b75ca8a94f0` | 3 | PASS |
| `bullarium.volume-07.unit-0098.reading-order` | 3 | `8f828d9888cd31b3c8493b27b0e9159c208c0250dfe9f65a89e587a7d3348d88` | 11 | PASS |
| `bullarium.volume-07.unit-0100.part-01.reading-order` | 2 | `2e8d2e900aff3bf656909dc9881e4f94a4c1c30629ee1795592aaea0651433ed` | 6 | PASS |
| `bullarium.volume-07.unit-0100.part-02.reading-order` | 1 | `acb43003208b27c3dfc86b49e93ba3e6995fa2fe9b53f465ab20da4643a10d2e` | 7 | PASS |
| `bullarium.volume-07.unit-0100.part-03.reading-order` | 1 | `796beb46849e10cfea6480fe39fe09f2bba7dfa087169b8f6cd912bae88f75c8` | 6 | PASS |
| `bullarium.volume-07.unit-0101.part-01.reading-order` | 1 | `8d651dfdafda207b7763ac5d31b3ab18b916e1458a12c1ac940c02bed8917337` | 3 | PASS |
| `bullarium.volume-07.unit-0101.part-02.reading-order` | 1 | `e67a6749a676c6665be439bb238ccea3a05f6ae4a9a99529dfc4f25beb8022e5` | 9 | PASS |
| `bullarium.volume-07.unit-0104.reading-order` | 1 | `c771a575e07b4803bd142e1bde652eaf6fb53541a719f22e3e376830a98ce6c7` | 4 | PASS |
| `bullarium.volume-07.unit-0108.reading-order` | 2 | `372571bfd7b272d929794479c5cf682e62814ebe72718e39af38c3a5ad88c46b` | 5 | PASS |

## Findings requiring changes

- `bullarium.volume-07.unit-0040.reading-order`: BLOCKING footnote fusion (page 1, left column, end of §1): the printed page-foot note `t De materia liebraeorum vide in constit. iv Palili IV, Cum nimis, tom. vi, pag. 498.` is emitted inside the §1 body paragraph immediately after the hyphen-split body word `scien-` (same paragraph, no break). Reading-order derivative lines 20513-20515 form one paragraph; the body resumes `tia, ac de apostolicae potestatis...` after the running head `An. e. 1865 168 BULtAUTUM nOMANUM An. C. 1869`.
- `bullarium.volume-07.unit-0081.reading-order`: BLOCKING footnote fusion (page 1, left column, §3): the printed page-foot note `i Ex Regest. in Arcliiv. Valic. — Huiusmotli refoimalionem vide siipra in conslilulione xxxi, Hoiiianum decet, pag. 97.` is emitted inside the §3 body paragraph immediately after the hyphen-split body word `quo-` (same paragraph, no break). Reading-order derivative lines 46451-46459 form one paragraph (body TeX: note line precedes the paragraph's `\par`); the body resumes `quam, quavis auctoritate...` after the running head `An C. IbCb 372 EULLARIUM ROMANO! An. e, 1505`.

Remedy direction (not performed): emit the note at the page break as its own block, splitting it from the body paragraph, then re-render and re-review every page of the affected PDF.

## Per-document observations

### `bullarium.volume-07.unit-0038.part-02.reading-order` — PASS

Lines [[19786, 20263]]; 16 marginal blocks.

- Page 1 (PASS; PNG `30c83ce061ab1b85bd59da01dda648beab015a0ba853d8dca8fca2c3c8b97ba7`): Title/issuer line 'Pius episcopns servus servorum Del, ad perpetuam rei memoriam. · Latin' matches metadata; no date shown. Two columns read naturally. Marginal blocks 'Eiordium.', 'Eiempiioaiu- risdictioiie or- dinariornmi.', 'FaeuUa. reU- ...' are separate short paragraphs. Qualification: running head 'An, C. 1S62 162 BULLARIUM ROMANUM An. C. 1862' inline between 'nulUsque terminis' and 'comprehensa' (left col) and 'Ad. C. 1S62 Plus rv PP. i63 An. e. 1562' (right col). Footnotes '1 Ad hoc vide ...' and '1 Illosque, Cherub. (r. t.).' set as own blocks at page break. No clipping/tofu.
- Page 2 (PASS; PNG `50d039d5013df6034f9aa968263124be338eb0cd49714d4dd8d722090816a71e`): Continuous two-column body §3-§9; marginal blocks (PriTilegium dispODendi..., Presbyi. miiii..., jiiuies ob inob-..., Eiempuo co-..., Pensione! su-..., induig. pien..., indaij. «tiam...) separate. Qualification: running head 'An. C. Ib62 ^Q^ BULLARIUM ROMANUM An. C. 1862' at top of right column preceded by stray OCR marks. Literal OCR garbage marks only.
- Page 3 (PASS; PNG `450039d7fa089a5fc2f8e7995d6b08cbdf7ca5d760ad6b650351dc3938cbea39`): §10-§14 and dating clause 'Datum Romae apud S. Marcum ... nonis iu- lii, pontificatus nostri anno iii.' as natural source closing, then Source/rights apparatus. Footnote '1 Fervcnlinri, Cherub. (r. t.)' own block; running head 'An. C. 1562 PIUS IV PP. 165 An. e. Ib62' inline (qualification). Marginal 'ciausuiae de- rogaloriao.' placed between 'recorda-' and 'tionis' as its own block (hyphen-split placement qualification). No overlap or clipping.

### `bullarium.volume-07.unit-0040.reading-order` — CHANGES_REQUIRED

Lines [[20455, 20928]]; 19 marginal blocks.

- Page 1 (CHANGES_REQUIRED; PNG `1e12d59faabf52806a10e9a191e2dcbf042bda243b0d0b277a248b0200597e22`): Title/issuer (Pius Papa IV universis et singnlis ... custodire. · Latin) match metadata; no date. Constitution number 'LVII.' and repeated heading/address in body. Marginal blocks (pauiusivmoi-..., hìc modo Pon-..., siibiiia usque..., '"um chrisua- ,erseniur.) separate. Running head 'An. e. 1865 168 BULtAUTUM nOMANUM An. C. 1869' inline (qualification). Footnote fused into §1 paragraph (blocking).
  - Finding: BLOCKING footnote fusion: page 1, left column, foot of §1 paragraph: the printed page-foot note 't De materia liebraeorum vide in constit. iv Palili IV, Cum nimis, tom. vi, pag. 498.' runs on inside the §1 body paragraph directly after the hyphen-split word 'scien-' (same paragraph, no break; source derivative lines 20513-20515 in one paragraph); the body resumes 'tia, ac de apostolicae...' after the running head.
- Page 2 (PASS; PNG `39d00e736f3e52916d279a25114d02767975196e1c71213b97e4521c1d713cfd`): §3-§11 continuous; marginal blocks separate (pignora posi..., siamu Crbn..., Domini domo- rum..., Qui slabìlia..., Delifla..., Querelans..., Praesmptio..., Apoibocas...). Footnote 'ì Concurrcnti, Cherub. (r. t.).' own block; running head 'Ah. C. I56'2 PIOS IV PP- 169 An. e. IB62' and signature 'Bull. Rom. Yoì. YIl. 22' inline (qualifications). '§ 5 ... almae Urbis / » ° ..... praetatae' line break is literal OCR noise. No clipping.
- Page 3 (PASS; PNG `274ebd4d46026139b301942ff866e1c891b0bd3870cfc5df3f2281499b159bf3`): §12-§15 continuous; running heads 'An, C. 1862 170 BULLARIUM ROMANUM An. G. 1S62' and '1S62 Plus IV PP. 171 An. C. 1862' / 'An. C.' inline (qualifications). Marginal blocks separate (libri non prò-..., CtertiuDi Ir rllui., Eieculorum..., ClausulflS it' rogaloriae.); marginal fragment 'i' between 'su-' and 'per' (hyphen-split placement qualification). Right column ends short before page break; no overlap.
- Page 4 (PASS; PNG `9318cc3e87d0373ecb28a879cb83f3963a23d3f9a29e7c4322916ca4f85ce279`): Sparse final page carries genuine source closing: dating clause 'Datum Romae apud Sanctum Petrum, sub annulo Piscatoi is, die xxvn februarii ... anno iii.' and publication note 'iJiit. die 27 IVli. 156-2, luinlif .iniici ni.' before Source/rights apparatus. Not apparatus-only.

### `bullarium.volume-07.unit-0041.reading-order` — PASS

Lines [[20930, 21121]]; 8 marginal blocks.

- Page 1 (PASS; PNG `245197587aefa17f7d7302b6464a30fb202c92620ed50daee7389a2c1e4c76a2`): Title and issuer 'Plus episcopus servus servorum Dei, ad perpeluam rei meoijTiam. ^ · Latin' match metadata (OCR-damaged issuer; qualification); no date. 'LVIII.' number and heading. Marginal blocks separate (Cauia buius prohibiiionu., • rrobibnio de..., Conlraveuien- lium poenae., lobibilio con-..., Lioentia au-..., Inssio publi- undi., Fides tran- lumptoram.). Running head 'i An. C. 1S62 172 BULLARint r.OMANTM An. C. 1S62' inline between 'dictumque' and 'genus' (qualification). Two columns natural; no clipping.
- Page 2 (PASS; PNG `6194cdb56bbf6122361612bb9c235ebc43a4e8afe84880b3d9c104d2da2b7944`): §6 end, marginal 'De.osaiiocon-', §7, 'Nulli ergo e(c.', dating clause 'Datum Romae apud Sanctum Petrum ... pridie nonas martii, pontificatus nostri anno iii.' and publication note 'Ua(. die G martii 1562, pontif. anno hi.' as genuine source closing, then Source/rights apparatus. Single-column sparse final page acceptable.

### `bullarium.volume-07.unit-0042.reading-order` — PASS

Lines [[21123, 21505]]; 13 marginal blocks.

- Page 1 (PASS; PNG `8e65e5e22f03e5fe87151532e9977ee0cba6ac635152d7f1e1b877cca73202cb`): Title (multi-line OCR title) and issuer 'Pius Papa IV, moto proprio, etc. · Latin' match metadata; no date. 'LIX.' heading. Marginal blocks separate (caos, conni-..., Advocalii) causaruni..., DopuUIio et faciilutes...). Footnote '1 InjlitLitionem iiuius monasterii ... pag. 742.' set as own block at page break after 'Conver-', followed by stray '|' and running head 'As. C. )b62 HUS IV PP. 173 An. C. 1862'; body resumes 'tilarum de Urbe' (note block between hyphen halves at the page break: acceptable). Running head 'An. C.1862 174. BULLARlIIM ROMANUM An. C. i862' inline in right column (qualification).
- Page 2 (PASS; PNG `6fa1c718b1c584bc39157259b29d9674269678f665ad17b7c639c96e7de7dcad`): §2-§10 continuous two columns; marginal blocks separate (Facuitaiinhi- bendi..., semeniiM..., Inobeillenlcs coerceailli, <^«'«" neces- «aria faciendi;, Causas reai-..., Cau^ae alibi..., ciausui» prie-, Decretum ir-, uauiuiae je-). Running head 'An. C. (S62 Plus IV PP. 175 An. e. 1S62' inline between 'cum' and 'inde secutis' (qualification). No clipping or tofu.
- Page 3 (PASS; PNG `18ee259fa60d1c45643145f589983ecf8f4b43f1c234156e1a96b6ff0bbdaa06`): §11, marginal 'soia sijnatur»', §12, footnote '1 Exemptionibtis, Clierub. (r. t.).' as own block at page break followed by running head 'An. C. 1B62 176 BULLAmiJM ROMANUM An. C. 1S62' (qualification) between 'tam in iudicio' and 'quam extra'; closing 'Placel, mota proprio. I.', 'Datuiii Ixoiiiae apud Sanctum Pelriim, deciniosexto kalendas aprilis, anno in.' and 'Hai. die 17 martii 156;2, ponlif. anno in.' as genuine source closing; Source/rights apparatus continues into the right column.

### `bullarium.volume-07.unit-0043.reading-order` — PASS

Lines [[21507, 21699]]; 6 marginal blocks.

- Page 1 (PASS; PNG `08caab14ef77684acd47f9e940579a96860021f16c5e3a5060b2106ed09f2a0f`): Title and issuer 'Pius Papa 17 , ad futuram rei memoriam. · Latin' match metadata (OCR-damaged regnal numeral; qualification); no date. 'LX.' heading, marginal blocks separate (Eiordiam., Po Diificescon-..., scd hic Pou-..., Ei iiaac non aiias iudiciri). Footnote '1 Haec bulla in Mainardi ... (r. t.).' set as own block at page break, then running head 'An. C. i86? Pirs IV PP 177 An. C. 1S62' (qualification). Stray '* .' inside §2 is literal OCR mark. Natural column flow.
- Page 2 (PASS; PNG `d2ea29c4a4a738e9f3702ef5226bdcc07576623da09a0f33c846f565bd0ee424`): §3 end, §4 with marginal 'Coutrariisde- rogai;' as separate block; signature mark 'BuU. Rom. Voi. VII. 23' inline between 'dero-' and 'gatum' (non-blocking qualification per addendum (d)). §5, dating clause 'Datum Romae apud Sanctum Pelrum, sub annulo Piscatoris, die prima aprilis ... anno in.' and 'Uat. die 1 aprilis 1562, pontif. anno ni.' as genuine source closing, then apparatus.

### `bullarium.volume-07.unit-0045.reading-order` — PASS

Lines [[22074, 22567]]; 2 marginal blocks.

- Page 1 (PASS; PNG `0a67d4b2efc570a9d7e2e1f0d4414f97942ff8e53c774794ba8d2c0aa0d9a4be`): Title (Tara merccduninotariormn ... iudicis Burgi.) and issuer 'Pius Papa IV, motu proprio, etc. · Latin' match metadata; no date. 'LXII.' heading, marginal 'Nolani prae- liane lavam, ei labeMam affi- lam leneaiu m loco pubiico.' separate; motu proprio body, 'Placet. Motu proprio. I.', then tariff entries each as own paragraph. Running head 'An. C. 1862 PIUS IV PP. 181 An. e. 1B62' inline between tariff entries (qualification). Some tariff entries run together in source OCR (e.g. 'b. 37 1/2- Pro monitorio'), literal OCR. No collapsed table or clipping.
- Page 2 (PASS; PNG `06baa0ea16a456c779ad848096dcaf166ed26be21303433f32e0735d2b44bf93`): Tariff entries continue in two natural columns; running head 'Ad. C. 1S62 182 BULLARIUM nOMANUM An. C. 1S62' inline between 'extractus facti cum' and 'lineis et iuxta' (qualification). No overlap or tofu.
- Page 3 (PASS; PNG `e9cf0e6b82f5390202cb977d09e6f7cf3f3660dd149f49ff71e5393caa111f95`): Tariff entries conclude with 'Eadem taxa prseinserta servetur...', 'In aliis vero mere civilibus...' and 'In omnibus casibus praedictis ... gratis.' (natural end of the printed tax schedule) before Source/rights apparatus; running heads 'An. C. 1562 PIUS rv pp. i83 Ali. e. 1862' and 'An.C. 1862 18i BULLARirM R0MANU5I An. C. 1862' inline (qualifications). Source-bearing final page.

### `bullarium.volume-07.unit-0046.reading-order` — PASS

Lines [[22569, 22817]]; 8 marginal blocks.

- Page 1 (PASS; PNG `13336f8b6a9889caad13c1c74b2e03ae0b1a7069af06f518120689d3a55d18f5`): Title (', Privilegia, gratias ... pro- midganda 1.') and issuer 'Pius Papa IV, ad perpetuam rei memoriam. · Latin' match metadata; no date. 'LXIII.' heading, marginal blocks separate (Eioréiao., Aiiqni onun-..., oeciaraiion.» uQdbutfacuT, J ", I, consuiuiio- nes...). Marginal fragment 'I' between 'tribu^le-' and 'ctorum' (hyphen-split placement qualification). Footnote '1 Ex Bull. Can. Later., lom. i, pag. 136.' own block at page break, then running head 'An. C. 1562 PIUS rv PP. 185 Ka. C. 1862' (qualification).
- Page 2 (PASS; PNG `c9b2ff13aff24b81892e1b01902be89644693b390e0d0d7b0015cdd204c2571b`): Marginal 'Omnia prae* dìvU coDtlrnint' separate; §2 continuous; signature mark 'Bull. Rum. Voi. MI. 24' and running head 'An. e. Ib62 186 BULLARIUM ROMANUM An. C. 1S62' inline (qualifications). Dating clause 'Datum Romae apud Sanctum Petrum, sub annulo Piscatoris, die iv aprilis, mdlxii ... anno iii.' and 'Dal. die i apiilis 1502, poiilif. anno ni.' as genuine closing, then apparatus.

### `bullarium.volume-07.unit-0049.part-02.reading-order` — PASS

Lines [[24437, 24542]]; 4 marginal blocks.

- Page 1 (PASS; PNG `66ec4d00e43d80fc7e9ff4d045382c5bdbefba0842a8aa32de6bb0d5113776a0`): Title 'Sequi tur dedaratio superius editae constitutioìiis.' and issuer 'Pins Papa IV, ad futuram rei memoriam. · Latin' match metadata (OCR-damaged issuer; qualification); no date. Marginal blocks separate (Enunciai su- perioreslileras., ordinaiiisdat..., ^„,5 ... panasPoulilei., comraria loiiu). §1-§4 continuous, running head 'An. C. 186-2 200 BULLARIUM ROMANUM An. C. 1862' inline (qualification). Dating clause 'Datum Romae apud Sanctum Pelrum ... die vigesima octava iunii ... anno quarto.' as source closing, then apparatus. Single page, no clipping.

### `bullarium.volume-07.unit-0052.reading-order` — PASS

Lines [[25972, 26374]]; 10 marginal blocks.

- Page 1 (PASS; PNG `ec8d7a5946a148bd80d68b1b33ca57715dad708af2a87afe6858f5371ce505f9`): Title (Loca pia et confraternitates ... in eortim membra recipere.) and issuer 'Pius episcopus servus servorum Dei, ad perpetuam rei memoriam. · Latin' match metadata; no date. 'LXX.' heading, marginal blocks separate (Prooemium., Miiiisiri ec- siiiuiarum ... nariorura 1.). Footnote '1 Multae lites ortae fuerunl iiiter iilos el loco- rum ordiDarios.' own block at page break, then running head 'Ali. C. 1jG-2 212 BULLARIl'M ROMAN L'JI An. e. 1S62' (qualification). Natural column order.
- Page 2 (PASS; PNG `a4e6f58502bd322a3436773f7d487cfebf97ca1524f7ba6f3bc84a5854e1bf9d`): Stray marginal mark '•' separate between 'ec-' and 'clesiarum' (hyphen placement qualification). Marginal 'Ideo !'u.iiuv\ ...' separate. Printed marginal summary split into two separate blocks around body: 'El revocai Ilo- ... società-' after 'audeant', then 'tes, sire illas in eorum mem- bra ... chialium.' between 'instan-' and 'tiani' (separate blocks, hyphen-split placement qualification; no fusion). Running head 'An. C. 1!J6-2 PII'S IV PP. 213 An. C. Ib62' inline (qualification); marginal 'coniravenien- lium poenae.' separate.
- Page 3 (PASS; PNG `bdc9f5bf2c98da4df82fce9fd93fbce37785134f8ffffa7c97b607d8e166c97b`): §3 end, marginals 'Dooreium ir-', 'e ausui» Je-...', 'sanciio poe- nalis,' separate; running head 'An. e. 1562 21-4 BULLARIUM R0M.4.NUM An. C. 1S62' inline (qualification). §6 sanction, dating clause 'Datura Romae apud Sanctum Pelrum ... idibus iunii, pontificatus nostri anno ni.' and 'Ddt. die 13 iunii 1562, poiitif. anno ni.' as genuine closing; apparatus in right column.

### `bullarium.volume-07.unit-0053.reading-order` — PASS

Lines [[26376, 27771]]; 86 marginal blocks.

- Page 1 (PASS; PNG `6a4097b09e45c41a4cfa815c2a9860b4c7949c6403dfcc84e427e1e5387ec655`): Title (Reformatio iribunalinm ... Came- rati Apostolicae.) and issuer 'Pius episcopus servus servoram Dei, ad perpetuam rei memoriam. · Latin' match metadata; no date. 'LXXI.' heading. Marginal blocks separate (Poiuifei re-..., Nnncaiiorum..., Super sporlii- lis..., Et in crimi- nalibus..., In civilibui commissariis,, Merceda iu- dicum...). Footnote '1 Vide supra pp. 193, 203 et 207.' own block at page break, then running head 'An. C. 1S62 Plus VI pp. 215 An. C. 1562' (qualification). Natural column order.
- Page 2 (PASS; PNG `c262292beec288d2358561340af43992f4d734121db9f5fcc8b021ffbc4d915c`): §6-§20 in two columns; many short marginal blocks each separate (Sportulis ca-..., Tempore re-..., Tata prò si- bilo iudicum,, riniiiijiiioiie..., observaiuia bul. Paulilll 1,, Dcciaraiioiie..., >;uu;i,,i.bus, Eipciiiiionc..., caroerum li-..., Mediconim..., confes,..., fìsco ciiando..., Advocatis..., lu.iicis de Sa-...). Footnote '1 Lib. I, cap. 46.' own block followed by running head 'An. e. 1S62 216 BULLARltfM ROMANl'M An. C. 1S62' (qualification); footnote '1 Vide lom. vi, pag. 384.' own block at foot of right column. No clipping.
- Page 3 (PASS; PNG `d47a323200c8ce024dc19f0d9ea08285ec9593b7566bff785768f5aa32be584b`): Opens with running head 'An. C. Ib62 PUS l\ pp. 217 An. e. ISf,'^' (qualification) then body continuation; signature 'Bull. Rom. Voi. VII. 28' and running head 'An. e. 1S62 218 BULLARIUM ROMANUil An. e. IS62' inline (qualifications). Marginal blocks separate (Nulni ioni..., hiiisque cuslo-..., ludìctim dictne..., Cinici Ili Ri- pae..., Itidicis Bur^'i..., (',nn<erTalo-..., conscrvaio- rum..., Emaoidina-..., Fide eis dan-, ofQcìo co- rumdcDi,, Mandaiorum excculione,). §21-§31 natural order.
- Page 4 (PASS; PNG `57d1ad3b233f5212db6c765bdb5772818e5ac09fd902c36573718b4f1983fde1`): §31 end through §39; marginal blocks separate (Mneisirorum..., Eor.jmdem, siibningisiro-, Magisiiorum, Advocatipau-, Profuraioiis pati^erum lìùu,, Pioruraioria...). Marginal 'Advor-aii n- scalis oflìcio,' placed as own block between 'tangenti-' and 'bus' (hyphen-split placement qualification). Running head 'An. C. Ib62 Pirs IV PP. 2i9 .\n. C. 18G2' at foot of left column (qualification).
- Page 5 (PASS; PNG `be894d8d1c0f4a0562af2432b8065fdb845242fce6ad09e8e68d8d02943df9be`): §40-§52; marginal blocks separate (riscm ..., ei de o\rn-..., Ciiaiioncsque..., Capturaranoii..., Appeiiei..., Siipersesso- rias..., Reniissoriae fisco..., Lilerae prò capiendis..., Dilationes reis..., Coniposiiiones..., Absolulorum cauliones..., Fiscus quando appellai...). At the §41 page break: running head 'An. C. IjG^ 220 BULLARIUM ROIIANUM Ali. C. 1SG2' (qualification), marginal 'libus insiigaio- ... lineai prò se;' as own block between 'insti-' and 'gator', and the body line 'gator adei'it , sive apertus sive secretus ,' set as its own short paragraph before 'ipsas fccerit' (source derivative paragraphing; no marginal/body fusion; noted qualification). Running head 'An. C. Ib62 Plus IV PP. 221 An. e. IS62' inline (qualification).
- Page 6 (PASS; PNG `7cdc01038b2a41f14998699382141220de9df80e48119853a4522b97fdfa93a2`): §53-§66 continuous; marginal blocks separate (Fiscus ime- resse..., Fiscusubique, Fisci fieui-..., pioiiibiiioque..., Fisci Capilo-, poenarum in-..., lasa » imiii., ornda noia-..., sabsiuuii..., acius probi-..., Recisua nen-..., Taxa prò co-..., Nolarioruai Capilolii..., TaiB eonim- dem., Prolonotarii...). Running head 'An. C. 1S62 222 BULLARIUM ROHaNUM An. e. ib62' inline between 'merce-' and 'dum' (qualification).
- Page 7 (PASS; PNG `9e084fda677a94dcc9a71c1393fc155675a252f321667705fbf719e931fc9264`): §67-§79 continuous; marginal blocks separate (Exlractuum laxalio., Noiariomm eniumd..., Rognusadre- Libino., piurium noia-..., El procuia-, consuiumar lium..., liirìsdiolìo., ÌSoiaiioriim arlis lai:), Assessornm- que eorumdeiD-, ludicis Turris Nooae..., PJoUriorum psiuE taia., Cursorum Pa- pae..., Mandatario-...). Running head 'An. C. I!i62 PIUS IV PP. 223 An. e. iS62' inline between 'ta-' and 'xam' (qualification).
- Page 8 (PASS; PNG `7dc7a8c2a5c935157ec3b2f61678627f7342ad18f36dc9802ce4bc98f7d24d92`): §79 end through §84, sanction 'Nulli ergo ... Si quis autem etc.', dating clause 'Datum Roniae apud Sanctum Petrum ... secun- do kalendas iulii, pontificatus nostri an- no IH.', subscription '•f- Ego Plus, catholicae Ecclesiae episco- pus.', 'Seqmmtur Cardinalium siibscriptiones et publicatio.' and 'Dal. die 30iunii 1562, poiilif. anno in.' as genuine source closing, then apparatus. Running head 'An. C. Ib62 224 BT'LLARIUM ROMANl'M An. e. 1862' inline (qualification); marginal blocks separate (B^iigeiii..., Eoriimdem potest.is..., Poenarum indiclio..., A pauperibus..., ciausuiae ile- rogaloriae., Sanclio poe-).

### `bullarium.volume-07.unit-0055.reading-order` — PASS

Lines [[28285, 28550]]; 8 marginal blocks.

- Page 1 (PASS; PNG `1aee73482ab55515d6b2647b62feaf4b27a69254bdf1934cdad4e356089feb21`): Title (Revocalio privilegionmi ... matrimonialibus, eie.) and issuer 'Pius episcopus servus servorum Dei, ad perpetuam rei memoriam. · Latin' match metadata; no date. 'LXXIV,' heading, marginal blocks separate (Eiordium., nic Pomifei el al»..., Quibas eo- riim..., Hic ideo Pon-...). Footnotes '1 Ila lume lociim siipplemus: ... (n. T.). 9 Legimus : ... (r. t.).' set as one note block at the page break (two notes in one note paragraph, not mixed with body), then running head 'An. C. 1362 PlfS IV PP. 229 An. e. 15G2' (qualification). Stray marginal mark '■' between 'con-' and 'suevit' (hyphen placement qualification).
- Page 2 (PASS; PNG `ac29b784b6e3a733720961ed7e9d099936937decd615a1f244a3fc0a80b0bb76`): §3 end through §6; running head 'An. C. If)62 230 BDLLARIUM ROMANUM An. C. Ib62' inline between 'ite-' and 'ratis' (qualification); marginal blocks separate (Prohibiiìo eis de celerò ..., Coniraiiorum ilcrogaliO', Fues j.mHa ...). 'Nulli ergo etc. Si quis autem etc.', dating clause 'Dntum Romae apud Sanctum Marcum ... xiii kalendas octobris, pontificatus nostri an- no III.' and 'Dut. (Ile 19 seplembris 1502, poni. an. ili.' as genuine closing; apparatus follows.

### `bullarium.volume-07.unit-0059.reading-order` — PASS

Lines [[30073, 30288]]; 10 marginal blocks.

- Page 1 (PASS; PNG `d410df94d0d3d9b2a920e68173ba78391579a94b73df14b69e31f112135b04d3`): Title (Revocatio exemptioniim ... dnode- cini filiorum.) and issuer 'Plus Papa IV, mota proprio, etc. · Latin' match metadata (OCR-damaged issuer; qualification); no date. 'LXXIX.' heading. Marginal 'Causa con- slilatioDis.' as own block between 'rationabili-' and 'bus' (hyphen-split placement qualification); other marginals separate (ReTocalio e- xemption..., Declaraiio circa exemplioncs...); stray marks '\', '1', '|' as separate blocks. Running head 'An. C. 1862 Plus IV PP. 243 Ati. e. 1562' inline (qualification).
- Page 2 (PASS; PNG `a793c072b303ada6efff35aeae2f2739b1c59e35175249048f6bbe203df15577`): §2 end through §6; marginal blocks separate (ncrreuim ir-, Eiecuiorum..., cbusuia.d»..., soi» signatura..., riique cxcm- pium probci.). Running head 'An. C. Ib62 24-4 BULLAUIUM ROMANUM An. C. 1563' inline (qualification). Ends with 'Placet, motu proprio. I.' (source motu proprio signature) before apparatus, which continues into the right column. Source-bearing final page.

### `bullarium.volume-07.unit-0063.reading-order` — PASS

Lines [[31180, 31308]]; 4 marginal blocks.

- Page 1 (PASS; PNG `521c1bea1fb9fb08fd7704e3d77847215f55e987471781a45e2ac0dcc4539e35`): Title (Praefìnilio emolumentonimmagifttris ... persolvendorum 1.) and issuer 'Plus Papa IV, ad perpetuam rei memoriam. · Latin' match metadata (OCR-damaged issuer; qualification); no date. 'LXXXIIl.' heading; marginal blocks separate (^.n» ... lam., Eh soiTcnj», snon...o"nl'g"l buiusce..., oiisianiiaioUii.). Footnote '1 Es Regest. in Archiv. Yalic.' own block at page break after 'hae-', then running head 'An. C. 1E)63 252 BULLARIUM ROMANUM An. C. iS63' (qualification), body resumes 'redes'. §1-§4 natural order.
- Page 2 (PASS; PNG `f28f161440b453d1e626e8ba2dc80ac068b4c7b3f1a3cc2647405f8c7ca92e99`): Sparse final page carries genuine source closing: dating clause 'Dalum Romae apud Sanctum Pelrum, sub annulo Piscatoris, die decima maii , millesimoquingentesimosexagesimotertio, pontificatus nostri anno quarto.' and 'Dal. die 10 maii 1563, ponlif. anno iv.' before Source/rights apparatus. Not apparatus-only.

### `bullarium.volume-07.unit-0067.reading-order` — PASS

Lines [[32803, 33033]]; 8 marginal blocks.

- Page 1 (PASS; PNG `1b538cea87f669f9828998551107049ff92d99cf4167d29e82fa70ce7f4a2fdb`): Title (Caupones et albergatores ... in eo- rum ingressu.) and issuer 'Pius Papa IV, motu proprio, etc. · Latin' match metadata; no date. 'LXXXVIII.' heading; marginal blocks separate (^-...CODStltutlOIlli., Hospues Vt-..., connrmaiio..., FacuHascon- dendi ..., Decreium ir-). At the §1 page break after 'sin-': running head 'An. C. Ib65 26H BULLARIUM ROMANUM An. C. 1K63' and marginal 'sabiraciis , ei eìs anlea ... liScavcriul.' as own blocks before 'gulis' (hyphen-split placement qualification). Marginal 'FacuHascon-...' between 'or-' and 'dinationes' (placement qualification). Stray OCR mark runs inside §1 body lines ('.. , . ^. iti- 1 ^ ' j j,^i', '., l ' r r _ i') are illegible native-word noise, recorded as qualification (no legible marginal summary wording fused).
- Page 2 (PASS; PNG `3e3011d8d56b02e96345a8f2f25011d13ac8d518dce956c57877bbc01705b4f7`): §4 end to §6; marginal blocks separate (cian«uiaede-..., chusuiamm...); 'Fiat ut petitur. I.' source signature; partial running head '267 An. C. IbGi' inline between 'confirma-' and 'tione' (qualification). Dating clause 'Datuni Romae apud S. Petrum, quarto idus novembris, anno quarto.' and 'Dai. die 10 novembris 1563, punlif. anno iv.' as genuine closing; apparatus follows.

### `bullarium.volume-07.unit-0080.reading-order` — PASS

Lines [[46155, 46393]]; 11 marginal blocks.

- Page 1 (PASS; PNG `f50b74f5cd34b83ab253175f220de68d682ed2a2de9375c771b445134409913b`): Title (Nuncii apostolici ... conferendas.) and issuer 'Pius episcopus servus servorum Dei, ad futuram rei memoriam. · Latin' match metadata; no date. 'CXI.' heading; marginal blocks separate (l'ronMHium., Causa isiius, inhìbeiur nun- riis ... ei- pressis.). Running head 'An. C. lb6S 370 BULLARIUM ROMANUM An. C. 186b' inline between 'cupidita-' and 'tem' (qualification). Stray OCR marks inside §2 body lines ('i-i- , 111 ...', '1 1 1-1 .' 1-1,') are illegible native-word noise (qualification). Two columns natural.
- Page 2 (PASS; PNG `eb202c3d520636d1c47fbf69c2da62faf9b9dcd1ddf64e81da8d600321f4694a`): §2 end to §7; stray marginal marks '.' and '1' as own blocks (the '1' between 'pro-' and 'cessu': hyphen placement qualification), 'i' before running head 'An. C. 1363 PIL'S IV PP, 371 An. C. lb6S' (qualification); marginal 'Aposlol. porre- clae ... dieiues.' placed between 'convin-' and 'cendum' (placement qualification); other marginals separate (Laarac prin-..., Docretum ir- lilans., Forma el ef-..., Cidusulie J6- rogaloritie., Sandio poe' nalis.). Dating clause '... xv ka- lcndas iunii, pontificatus nostri anno vi.', subscription '-J- Ego Pus calbolicae Ecclesiae epi- ^copus.', 'Seqtnoititr Canlinalium subscriplionex et publicutio.', 'Uat. die 18 maii 1565, jiontif. anno vi.' as genuine closing; apparatus follows.

### `bullarium.volume-07.unit-0081.reading-order` — CHANGES_REQUIRED

Lines [[46395, 46533]]; 6 marginal blocks.

- Page 1 (CHANGES_REQUIRED; PNG `134dceda56d50bf6d72a22350289961a2d089f65b32dd64b34a123cf5251b60c`): Title (De computorum exhibilione ... praecesserunt *.) and issuer 'Pius Papa IV, mota proprio, etc. · Latin' match metadata (OCR-damaged formula; qualification); no date. 'CXII.' heading; marginal blocks separate (c.^usae huiusre..., oecurai quo-..., sì- ii.bei .a-, Do ri'ji'^iraii-..., Derogaiio con-, soiapraoseii- lenci,). Running head 'An C. IbCb 372 EULLARIUM ROMANO! An. e, 1505' inline (qualification). Footnote fused into §3 body paragraph (blocking).
  - Finding: BLOCKING footnote fusion: page 1, left column, §3 paragraph: the printed page-foot note 'i Ex Regest. in Arcliiv. Valic. — Huiusmotli refoimalionem vide siipra in conslilulione xxxi, Hoiiianum decet, pag. 97.' runs on inside the §3 body paragraph directly after the hyphen-split word 'quo-' (same paragraph, no break; source derivative lines 46451-46459 one paragraph; body TeX line 82 before \par); body resumes 'quam, quavis auctoritate...' after the running head.
- Page 2 (PASS; PNG `f2967f4cdba403f6d1c84bedbdff2010182b3829636c87b13f6014c83e6fd3e0`): Sparse final page carries §6 body and genuine source closing 'Placet, molu proprio. I.' and 'Dal. die 20 mnii 15G5, puiilif. anno vi.' before Source/rights apparatus. Not apparatus-only.

### `bullarium.volume-07.unit-0091.reading-order` — PASS

Lines [[54886, 55088]]; 11 marginal blocks.

- Page 1 (PASS; PNG `f6821cec0247ef7d0818d1c900bcf4863f602ed3e01046f2e44fd0b9f4272046`): Title (Confmnatio constHutionis ... deferre debent.) and issuer 'Pius episcopiis servus servorum Dei, ad perpetuam rei memoriam. · Latin' match metadata; no date. 'X.' heading; marginal blocks separate (Eiordium, Pauius iv e-..., jiic Pomifei ... approbat;, Signum defe- rendum..., Hoc pubiicari..., Obs«rTanliam..., Contraiiii dr • rogai.). Footnote '1 Omiltiuir lonor isliusconstitulionis, quaeha- betur tom. vi, pag'. 498.' own block at page break, then stray 'I' and running head 'An. C. IS66 Plus V PP. 439 An. e. 1S66' (qualification); body resumes 'illa concerniint'. Stray marks '«' and ''' as own blocks.
- Page 2 (PASS; PNG `a0ec864497986f33958333ecf51270d106f69ceb00869262b1bcf9cdd6582d7c`): §6 end, running head 'An. C. ISG6 440 BULLARIUM ROJIANUM An. C. 1K66' inline (qualification), marginals 'Forma pultl catioiiìs.' and 'Fides Iran- aumptoium' separate, §7-§8, 'Nulli ergo etc. .', dating clause 'Datum Romao apud Sanctum Pel rum ... xin ka- iendasmaii, pontificatus nostri anno i.' and 'Dal. die IO aprilis 1566, poiitif. mino i.' as genuine closing; apparatus follows.

### `bullarium.volume-07.unit-0094.part-02.reading-order` — PASS

Lines [[57033, 57212]]; 8 marginal blocks.

- Page 1 (PASS; PNG `97540a96c967c21a08f4b2f262ee7144903d77114e21fb17251eb44e3cc07fa5`): Title 'Serjuiiiir ampiiaiio pocnanim coìtlra fauforcs bannUorum.' and issuer 'Pius episcopus servus servorum Dei, ad perpetuam rei memoriam. · Latin' match metadata; no date. Marginal blocks separate (Exnrdiuni., Causa luiiiis ' oiislitulionis, Ampiiauop»-..., niini.im in fu-, Deriariii.i quo-..., cliusui,..., ciausuUe de-). Running head 'An. C. 1866 PIUS V PP. -iS? An. C. IBSfi' and signature 'Bull. Rom. Voi. VII. 58' inline (qualifications). Two columns natural.
- Page 2 (PASS; PNG `5b198b3c06757d137a7e906d700f4ebe849ee1af40cf669c5a09621efa104a9f`): Marginal 'iransumpio-' separate, §6 ending 'Nulli ergo etc.', running head 'u.c. \m -458 BULLARIUM ROMANUM An. C. 1K86' inline (qualification), dating clause 'Datimi Roniae apud Sancluni Pelruni ... xvin ka- lendas septembris, ponlificatus nostri an- no primo.' as genuine source closing before apparatus. Sparse but source-bearing.

### `bullarium.volume-07.unit-0094.part-03.reading-order` — PASS

Lines [[57214, 57300], [57319, 57319]]; 3 marginal blocks.

- Page 1 (PASS; PNG `d5ca75f7b4173aa4d1621a9e24af0c4a6e6a65b0e7ebfd173ddcb14854d69e32`): Title 'Seqidtur mandatmn qmlannis dictam buUain publicandi.' and issuer 'Fius Papa T, ad perpetnam rei memariam. · Latin' match metadata (OCR-damaged issuer; qualification); no date. Marginal blocks separate (praeccpium pubiicaudi ... fhiviìs., contmenien-, Eiempiorum fide»). §1-§3, dating clause 'Datum Romae apud Sanctum Marcuni, sub annulo Piscatoris, die quarta septem- bris ... pontificatus nostri anno i.' as genuine closing, followed by the printing's own note '1 Legimus seu (n. t.).' as a separate block (discontiguous selected line 57319, disclosed in source note), then apparatus. Single page, no clipping.

### `bullarium.volume-07.unit-0098.reading-order` — PASS

Lines [[58546, 58941]]; 11 marginal blocks.

- Page 1 (PASS; PNG `5d2fa45254b1fb6b9b0d2daaf852a01746ad88dca29c925e38dfe6d7cdb9cdd6`): Title (Excmftioncs Ordinmn Mendicanthmi ... miUtcs *.) and issuer 'Pius Papa V, ad perpetuam rei memoriam. · Latin' match metadata; no date. 'XIX.' heading; marginal blocks separate (Eiordium., EiPiniiiioncs Ordìnutii ..., Exeiiiplio ali onere ...). Footnote '1 Aliam exeniplionem generalem ... pag. 21.' own block at page break after 'quolidie', then running head 'An. e. \m fius V PP. 409 An. C. 1S6' (qualification); running head 'Àn. C. I!$66 470 BULLARIUM ROMANUM An. C. 1S66' inline in right column (qualification).
- Page 2 (PASS; PNG `123fbd5107e2a1f57e3a5e17d7cb914ddbe16f836999e94eb5aae7ad05eaf958`): §3-§8; marginal blocks separate (Redditus eo- rum ..., Repetitìo ex- emplìonum., coniravenien..., Decreium ir- riunì. ,, Eiccuioiiim denutalioel ...). Marginal 's,.i Mcndiran- ... Canierac' placed between 'Ca-' and 'merae' (hyphen-split placement qualification); stray 'I' between 'sta-' and 'tus' (placement qualification). Running head 'An. C. Ib66 Plus V PP. 471 An. e. 1S66' inline (qualification).
- Page 3 (PASS; PNG `bae01e6dcc9bfae98b79e917027fbc7dcb2531d1fe0b3a1f37d6e42ca74e7220`): §8 end, marginal 'ciausuiae de-' separate, §9; running head 'Ali. C. 1S66 472 BlJLLAniUM ROMANUM An. e. tB66' inline between 'aposto-' and 'lica' (qualification). Dating clause 'Datum Romae apud S. Marcum , sub annulo Piscatoris die xxix iulii mdlxvi , pontificatus nostri anno i.' and 'Dut. die 29 iulii 1566, poiilif. anno i.' as genuine closing; apparatus follows.

### `bullarium.volume-07.unit-0100.part-01.reading-order` — PASS

Lines [[59410, 59543]]; 6 marginal blocks.

- Page 1 (PASS; PNG `552cc48f8eaddcab5362ee8c530d0538fc9555a61a6eb6c0a3b8b8b45725d8f5`): Title (Declarationes concìlii Tridentini ... celerò contrahenda 1.) and issuer 'Sanctissimns in Christo pater et dominns noster dominus Pius divina providentia Papa V= · Latin' match metadata; no date. 'XXIII.' heading; marginal blocks separate (Diibium circa S.sèssTjn'..., ouijium circ»..., oeciaratiu pn nii..., Ueiiaratio pn-..., Dcircmm u). 'Placet, pnblicetur et describatur. M.' and publication record 'Leda et publicata ... millesimo quin-'; the printing's two footnotes '1 Huius concilii contìrmalio ... coeperit.' and '1 Clienib. addit ... (h. t.).' set as separate blocks at the page break, then running head 'Ad. C. IS66 Plus V PP. 477 An. C. ib66' (qualification); continuation 'gentesimo' follows on page 2 (note blocks at a mid-word page break: acceptable). Stray '1 '■ <' block.
- Page 2 (PASS; PNG `56a137f60c4cfd5c4a1099e6f57b7c969e9ac46ab2891c8ecccfb5dfd9722368`): Sparse final page carries genuine source closing: end of publication record 'gentesimo sexagesimosexlo, dieveio Mar- tis, vigesima mensis augusti ... anno i.', subscription 'A. Lomellinus, custos.' and 'Pubi, ilii^ 20 augusti 1566, poulif. niino r.' before Source/rights apparatus. Not apparatus-only.

### `bullarium.volume-07.unit-0100.part-02.reading-order` — PASS

Lines [[59545, 59671]]; 7 marginal blocks.

- Page 1 (PASS; PNG `414aefc20849e9c8331ba1c58decc9c308206c3614fab8ab71edab375410f210`): Title 'Sequitur alia declaratio circa impedimeuta cognalioìm spiriluuUs.' and issuer 'Pius episcopas servus servorum Dei, ad pcrpetuam rei memoriam. · Latin' match metadata (OCR-damaged issuer; qualification); no date. Marginal blocks separate (Exordiini)., Dubiuni se- cundum..., Declaratio e- iuedeiii diibii., oecreium n- riUiis., cuusuiae de-..., ...caiidi, qU38 niox seqmtur.). Dating clause 'DaUim Romae apud Saiicluni Pelrum ... quarto kalendas decembris, ponlilicatus noslri anno i.', 'Visum de Curia, lacobus Barengus.', 'PuMicaii..' and publication record with running head 'An. C. i866 -478 BULLA.RIUM ROMANUM An. e. 1B66' inline between 'loan-' and 'nem' (qualification), 'Steplianvis de Olea, matiisler ciii'soruni.' as genuine closing; apparatus follows.

### `bullarium.volume-07.unit-0100.part-03.reading-order` — PASS

Lines [[59672, 59777]]; 6 marginal blocks.

- Page 1 (PASS; PNG `5c3b0bd100e422af06f059c61a34797d3168b6b59bc9127ec0eabfce0aeebb32`): Title 'Sequitur alia dedaraiio circa inipnlimen- lìim olpitildlis et furnìcationis.' and issuer 'Pias episcopus servus servorum Dei, ad perpetuimi rei memoriam. · Latin' match metadata (OCR-damaged issuer; qualification); no date. Marginal blocks separate (Enordium., DubiumspcuL- ..., ', . . I', Deciarai.o ,-- lusdem dui.i,., Decronim ir- riUns., Forma pubii- ...). 'Nulli ergo de.', dating clause 'Datnm Homae apud Sancì um Petrum ... quarto kalendas decembris , ponlincatus nostri anno i.', 'PuMicaiiu' publication record, 'Steplianiis de Ulea, magisler rursoium.' and 'Uni. liii- i28 MOV. 15GG, imnlif ;iiiiio i.' as genuine closing; apparatus follows. No running head in this unit.

### `bullarium.volume-07.unit-0101.part-01.reading-order` — PASS

Lines [[59779, 59884]]; 3 marginal blocks.

- Page 1 (PASS; PNG `d0a6bf060d3c2c1d26f99068489583e28dff0a5e9e89b02b3e60d515a52df2f6`): Title (Fiimilìdrcs mnclae Ronunutc Ecclcsiae ... praejinitur I.) and issuer 'Sanctisslmus'in Chrlsto pater et dominus noster dominus Pias divina providentia Papa V, · Latin' match metadata (OCR-damaged formula; qualification); no date. 'XXIV.' heading, then the printing's page-foot note 'l llaec siipeiidia ... ibidem, pag. !(17.' set as its own block at the page break after the printed title, followed by running head 'An. C. 1S66 ' Plus V PP. 479 4d. C. 1S66' (qualification) and the issuer formula. Marginal blocks separate (Causa buiut, Prohibiiio fp- cardinalibus vei eorum haeredi-, dTogaiio.). §1-§2 and closing 'Apud Sanclum Marcum. in consislorio habilo die Veneris , sexta septembris , millesimo qningenlesimo sexagesimosexto.' as genuine source closing; apparatus follows. Single page.

### `bullarium.volume-07.unit-0101.part-02.reading-order` — PASS

Lines [[59885, 60023]]; 9 marginal blocks.

- Page 1 (PASS; PNG `e775eb6c8cc326f68f565935a8a7eb7fc96727bcedd4d2cd4083f299f998f8c1`): Title 'Sequitur alia in praedictis constihUio.' and issuer 'Plus Papa V, motu proprio, etc. · Latin' match metadata (OCR-damaged issuer; qualification); no date. Marginal blocks separate (Familiaresnon ..., Servelur bul- la Psuli 111. ..., Regalia non pelantur ..., Camera prn au- ..., Creditores po- slea ..., Successive prò vesliariis;, Mcrcenarii ..., Eiecuior bui- ..., coniranaioi-). Running head 'An C IS66 480 BULLARIUM ROMANUM Au. C 1B66' inline between 'valilura' and 'conslilutione' (qualification). §1-§8 and 'Placet, molli proprio. M.' as source closing; apparatus follows. Single page.

### `bullarium.volume-07.unit-0104.reading-order` — PASS

Lines [[60410, 60504]]; 4 marginal blocks.

- Page 1 (PASS; PNG `16a5cb16b3a5363b9b80653f65c1a5e55e52f57ab8e3240b622cb0dfe3f5c9ea`): Title (lurisdictio vicarii Papae ... in Urbe 1 .) and issuer 'Pius Papa V, niotn proprio, etc. · Latin' match metadata (OCR-damaged formula; qualification); no date. 'XXVII.' heading; marginal blocks separate (causa huius ..., lurisdiciio »i- carii ..., Sola signaiu- ra sufficit., cuusuiaede-). Footnote '1 De hac iurisdictione adnotstiones vide in con- stit. xvii Pauli HI, Licei, tom. vi, pag. 2!i7.' own block at page break after 'aliis', then running head 'An. C. 1S66 484. BULLARIUM ROMANUM An. e 1866' (qualification). 'Placet, molu proprio. M.', dating clause 'Dalum Romae apud S. Marcum, pridie idus septembris, anno i.' and 'Diit. ilie 12 sept. 156t>, puiilil. anno i.' as genuine closing; apparatus follows.

### `bullarium.volume-07.unit-0108.reading-order` — PASS

Lines [[62729, 62869]]; 5 marginal blocks.

- Page 1 (PASS; PNG `3051a3e2a0ed8e18c6c91023aa977fabc4ac3834a070d5822f4f4247b0bdaa5a`): Title (Mitigaiio consti tutionis PiilV, ... cautione 1.) and issuer 'Pius Papa V, motu proprio, etc. · Latin' match metadata; no date. 'XXXV.' heading; marginal blocks separate (Fius IV posi aiioB ..., me amen. ..., confessis la- ..., Decretuni ir rìtans.). Footnote '1 Ista Pii IV constilulio l\iv, Elsi ciincta, est supra, pag. 186.' own block at page break after 'respe-', then running head 'Ad. e. 1866 504 BULLARIUM nOMANUM An. C. 1S66' (qualification); body resumes 'ctive'. Stray OCR mark runs in §1/§2 lines are illegible noise (qualification).
- Page 2 (PASS; PNG `bb1a002d5e95273bc7eff8de4b3545a8eb861912a8322d8546e2bcbc6e153748`): Sparse final page: marginal 'ciausuiae Je- rogaioiiae soiii sifiiaiu- TA SUtìcit.' separate, §6 body 'Volumus autcm ... praesentetur.' and source signature 'Placet, molu proprio. M.' before Source/rights apparatus. Source-bearing, not apparatus-only.

## Limitations

- Literal, uncorrected, uncollated historical OCR; wording, OCR corruption and stray OCR marks were not judged or repaired.
- Layout and structure review only; no word-level collation, historical authentication, date reconstruction, publication or installation claim.
- Inline running heads, folios and printer signature marks are recorded as non-blocking qualifications per the series addendum (d).
- Act date unresolved in the frozen metadata; omitted from the title line as allowed.
- Final-page check: every last page carries genuine source text or closing (dating clause, subscriptions, `Placet` signature, publication record or the source's own notes) before the project source/rights colophon; none is apparatus-only.
- Separately set historical notes placed at a page break that falls mid-sentence or mid-word are recorded as acceptable.
