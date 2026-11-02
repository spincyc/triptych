# Bullarium Romanum reading-order visual review: batch bullarium-ro-0003, lane 07

**24 PASS, 1 CHANGES_REQUIRED** of 25 assigned PDFs; 46 pages individually opened at full raster size with the Read tool, zero reused. The only blocking document is `bullarium.volume-11.unit-0086.reading-order` (Paul V, *Confirmatio ... monachorum sancti Basilii*), page 1, column 2: a printed page-foot note is fused with the body at one page break in both directions (note continuation run into the § 5 body paragraph, and the § 5 body continuation run into the following note paragraph). No marginal-summary fusion was found. Scope: lane 07 of review batch `bullarium-ro-0003`, coordinate-reconstructed readers from the whole-volume reading-order derivative of the Turin Bullarium Romanum, volume XI (1867 printing, artifact `reading-order-e3cb674fd723`); acts printed under Clement VIII, Leo XI and Paul V.

## Scope and method

Every assigned page PNG produced by the repository `pdf-review` run (1700x2200 rasters) was opened as its own full-size image before its observation was recorded. No contact sheet, thumbnail, rerasterization, source acquisition, word-level collation, text correction or date reconstruction was performed. One JSON observation per page is in the lane ledger `observations.jsonl`.

Each page was checked for title line, responsible issuer, Latin label and omission of the unresolved act date against the frozen metadata; headings, two-column flow, gutters, margins, glyphs, clipping and overlap; natural source closing; modern digitizer signatures; raw placeholders; and, per the series addendum, (a) marginal summaries as separate TAB-led blocks, (b) page-foot notes as separate blocks, (c) natural two-column order, (d) running heads, folios and signature marks left inline, (e) fragment presentation and (f) non-word OCR noise.

Mechanical support (read-only, lane-local scripts `mech.py`, `mech2.py`): each selection was split into paragraphs from the reading-order derivative `hybrid.txt` at the frozen manifest's line ranges, and the generated body TeX was split the same way. The selections contain **140 TAB-led marginal paragraphs**; no derivative paragraph and no body-TeX paragraph mixes TAB-led and plain lines. Note probes found **69 printed-note blocks** set as their own paragraphs (several holding two notes, which is acceptable), one of which also carries body text, plus one note continuation inside a body paragraph (both unit-0086). The extracted first-page heading of every PDF equals the frozen title, issuer and "· Latin". No `Missing character` entry occurs in any lane PDF log; no `Google`/`Digitized` variant and no bare `None` occurs in any lane body TeX. These checks support, but do not replace, the visual review.

## Evidence verification

All assigned PDF, receipt, frozen-manifest and raster-run digests and every page PNG digest (74 files) were computed before and after inspection; all matched the assignment pins both times, and the two verification records are byte-identical. PDF page counts (pdfinfo) equal the assigned counts.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt `.scratch/typeset_pipeline/claude/bullarium-ro-0003/receipt.json` | `4630fab56b8bbfa1f62db653aba468655fe661502c4d542023eee3dcad929b3e` | Before and after |
| Frozen manifest `.scratch/typeset_pipeline/claude/bullarium-ro-0003/frozen-manifest.json` | `5ae108677f3bc8075c77de79fb694c8871fc01898aa3af28b575fddffe6f9294` | Before and after |
| Raster run `.scratch/claude-review/rasters-bullarium-ro-0003/review-run.json` | `6849911614a92c10885f9d9977d01a37f5ad78137723500b4ad9d831eaf671ef` | Before and after |
| Lane assignment | `6ba1db7c94dacc56f626dd125592fa6e6b24198e0cf6c05aca6f62b3685b9182` | Scope binding, unchanged |
| `verification-before.json` | `5691065ea5bcb1022ddba19fe766c94b7604efb23e3da1dfb38e1fcd2eb0bf8b` | All match |
| `verification-after.json` | `5691065ea5bcb1022ddba19fe766c94b7604efb23e3da1dfb38e1fcd2eb0bf8b` | All match; identical to before |
| `observations.jsonl` | `341119e4683d4f8e67a33bcf4f5f249e0445e194e52cd76dd05215ba5c15729f` | 46 unique page observations |
| `mech.json` / `mech2.json` | `85d72435f5a2ac385d157d39679b968694a2590ad2690e0e2ec37edeed9b9f05` / `9fbd1eada4399d4537cdfd6d45a615807efc0cbe9562cbdd7b174dfdf6813b0e` | Body-TeX and derivative paragraph roles |

## PDF outcomes

All documents display "Latin", omit the unresolved act date, and show the title and issuer strings exactly as frozen in the metadata (literal OCR forms such as `Clemens Papa Vili`, `perpetuata`, and the full address/protocol issuer lines of units 0069, 0087 and 0091 are matching qualifications that name the pope). No prior finding is recorded for any assigned document. No digitizer footer, tofu, clipping, overlap, collapsed table or raw placeholder was seen. Every document ends on a page carrying genuine source closing (dating clause, often followed by the printing's own notes) before the project apparatus.

| Document | Pages | PDF SHA-256 | Marginal blocks | Note blocks | Status |
| --- | ---: | --- | ---: | ---: | --- |
| `bullarium.volume-11.unit-0049.reading-order` | 3 | `ebb98072245173ddc29256fe13c4d343d25a81189160a8d9738fee525c086456` | 14 | 3 | PASS |
| `bullarium.volume-11.unit-0050.reading-order` | 2 | `2b411649a67bdc946aa8058d42f6b54f7a9c767c82e5df9016fce1961a69d69a` | 8 | 3 | PASS |
| `bullarium.volume-11.unit-0051.reading-order` | 2 | `7b8bee40d97a2ac5e1f152a049f9da6f5e0c9bb486d6d05364c7ff1208b03f08` | 6 | 6 | PASS |
| `bullarium.volume-11.unit-0052.reading-order` | 1 | `94964c80a68403e717cbcfbca15c65be456f327097baef2f1a493630e79648ad` | 4 | 1 | PASS |
| `bullarium.volume-11.unit-0053.reading-order` | 1 | `323daf2ab1b64a63c9f8291bf9c7ee60711cee3adbb3309bd91de3b5a6cae023` | 3 | 1 | PASS |
| `bullarium.volume-11.unit-0054.reading-order` | 1 | `914209e7a6c1e97e6f23463d5a6e88fb51d5e6d3a61f49a6455eaf3f8ac0ee65` | 3 | 1 | PASS |
| `bullarium.volume-11.unit-0055.reading-order` | 1 | `0b9575cd5b1d0b21207928563666756b981231254e03808b3421c90db24849f5` | 2 | 1 | PASS |
| `bullarium.volume-11.unit-0057.reading-order` | 3 | `a60b5ae90d687c0382b50c24d387a345699b686f0e111777246fd1601cd2b026` | 10 | 3 | PASS |
| `bullarium.volume-11.unit-0060.reading-order` | 2 | `ffe0caeb4254fed88cead1fc583700e172fc92053497f79c5ed1f51bd26c17fe` | 7 | 2 | PASS |
| `bullarium.volume-11.unit-0065.reading-order` | 3 | `75140d601b7f65090038888c34c233cd681a41f94d5054f3fd23b62c203f8ff5` | 11 | 5 | PASS |
| `bullarium.volume-11.unit-0067.reading-order` | 2 | `96d2b69374b5f963c3022a3424502265b0cbf2c185f9f86b3b2c3354cf27802c` | 9 | 1 | PASS |
| `bullarium.volume-11.unit-0069.reading-order` | 2 | `db1162dbb5866484f8e44d3317465c423529feb9952ad32a045c609523ac3c9a` | 3 | 2 | PASS |
| `bullarium.volume-11.unit-0071.reading-order` | 1 | `d6ab3184e08758cfa33d9b038b1dda03c8e0aaa4ebc134ba84b389fe65363909` | 2 | 1 | PASS |
| `bullarium.volume-11.unit-0072.reading-order` | 2 | `c42f003cf83c11c2bee43ef4f90d5180fd0ec75e6a06ae6035afccc9e7ab3944` | 4 | 2 | PASS |
| `bullarium.volume-11.unit-0080.reading-order` | 1 | `5f0409e0ec2beeadfb60f2befeeb2536ef74fc73dba7a9494dc2ffd9e9686f4e` | 2 | 1 | PASS |
| `bullarium.volume-11.unit-0086.reading-order` | 3 | `a599aa1201d16b7681d6f37546d2f809ecae6efa6e9aee355f029d59b9ea3eb4` | 12 | 8 | CHANGES_REQUIRED |
| `bullarium.volume-11.unit-0087.reading-order` | 2 | `b43e1f3309684e262c948ea62f90ce537aec62b74e4256c1bc53f7781ca10663` | 3 | 4 | PASS |
| `bullarium.volume-11.unit-0091.reading-order` | 2 | `9f9e6988c2a042ded55b85d3e4b6137672ef2cb3267f898eba32ac247da6042f` | 6 | 3 | PASS |
| `bullarium.volume-11.unit-0104.reading-order` | 2 | `df4b57be7f960dbaf69edeb73ffe9b86e425b35de0440fa524ec5aaf957ec32f` | 5 | 3 | PASS |
| `bullarium.volume-11.unit-0110.reading-order` | 1 | `9c7641a2ac710e6fd6afe5cf1cb3de378753a0bd6ce134e727e176ec862899bf` | 4 | 4 | PASS |
| `bullarium.volume-11.unit-0111.reading-order` | 2 | `1075dc248ef6050e19e89a2f0bf2f320c034f78a3883baad3f4c90ee3fbcda15` | 3 | 2 | PASS |
| `bullarium.volume-11.unit-0113.reading-order` | 2 | `efe76b4b70990702f4e8e48176aaecd5932fcf748f2e22b638935cea39bd80ec` | 8 | 4 | PASS |
| `bullarium.volume-11.unit-0116.reading-order` | 2 | `c866e55f4451fe258d529c97df810e0a66a2ff2267bd0f20195c0830cef05b34` | 4 | 3 | PASS |
| `bullarium.volume-11.unit-0118.reading-order` | 2 | `303cfceb0394cbe3a8fd4e541bae5ca7bade33765f5979f9881fba58231c8a19` | 4 | 4 | PASS |
| `bullarium.volume-11.unit-0120.reading-order` | 1 | `39b88206c4da1e75917982db6165b61ac127c19bdcec7b514560861614208e71` | 3 | 1 | PASS |

Marginal-block counts are TAB-led derivative paragraphs inside each selection, including TAB-set exordium labels (e.g. `Eioraium.`, `iciordium.`, `Bioniiam.`) and pure OCR-debris blocks; a block that continues across a PDF page break is counted once.

## Blocking finding

- `bullarium.volume-11.unit-0086.reading-order` (Paul V, *Confirmalio rethiclionis monachorum sancii Basila in imam Conrirpgafionem ...*), page 1, column 2, at the printed page break inside § 5 (derivative artifact reading-order-e3cb674fd723, `hybrid.txt`):
  1. The continuation of the page-foot note begun as `ì Praedicta omnia liabeiilur in Const. cix ipsius` (line 41657, set as its own block in column 1) — `Gregoiii XIII quae legitur in Buìl. toni, viii jiag. 307 (p,. T ).` (lines 41720-41721) — is run into the § 5 body paragraph directly after `... qui Theodorus divina favente clementi^ plu-` (derivative paragraph 41709-41721; same paragraph, no break; confirmed in the generated body TeX). BLOCKING under addendum (b).
  2. The following note paragraph `2 Edil. Main. leg. separareuUir ; al videlur mensa conventualis soparanda : de liis \ide prae- cil. Const. § 1 4 et IC), ih. pag. SOOctseq. (n. t).` carries the body continuation `res separaliones fecit , faclasque eliam iuxta sibi tributam facullatem revidil.` (lines 41730-41731, completing `plu-`/`res`) in the same paragraph (derivative paragraph 41727-41731). BLOCKING under addendum (b).

  Note `1 Eugenii IV habetur ...` (41723-41725) between them is correctly its own block. Pages 2 and 3 of this document are clean; the document status is CHANGES_REQUIRED.

## Items recorded for the coordinator (not counted as fusions)

- **Unsure, addendum (f):** unit-0086 p1 § 1, the word-like token `vili` inside the non-word run `fé- ,. . . . . „ ● r> vili licis` (line 41630); unit-0118 p1 § 2, the token `"éÌìa?us°` at the end of the body line `senalus elaliorum praedicto-` before `rum expoctamus` (line 52879). In both places the neighbouring marginal block is rendered as its own block; whether the token is reverse-page show-through or a marginal glyph group was not determined.
- **Selection gaps holding note text:** unit-0065 excludes lines 30779-30780 (`i Viderelur legenduni potius formam in iliis tradilam (r. t).`) and unit-0118 excludes lines 52890-52895 (`i Quiiique post dies confirmata fuit facullas ... in Romana Curia.`). Both appear to annotate a neighbouring act; ownership was not determined here. unit-0116 includes `1 Die 21 innrlii Paulus Papa privilegia ...` (line 52555), which appears keyed to the dating clause's note mark; the next act's `2 Ex Regest.` (line 52559) is excluded.
- unit-0111 ranges 51356 and 51358 overlap unit-0110's range 51353-51360; both lines are blank in the derivative, so no content is duplicated.

## Addendum checks

- **(a) Marginal fusion: none.** 140 TAB-led marginal blocks seen, each rendered as its own short paragraph; some are pure OCR debris (`•> i`, `^`, `.`, `ai""""`). Blocks placed between hyphen halves or a little early/late (qualifications): unit-0055 (`incum-`/`bat`), unit-0072 p2 (`pos-`/`sessioiiem`, debris `^`), unit-0110 (`Hie-`/`l'osolymilani`), and mid-sentence placements in units 0052, 0054, 0060, 0067 and 0071.
- **(b) Notes:** 69 note blocks at page or column breaks or after the dating clause, including note-only blocks holding two notes (units 0069, 0113, 0120) and the two-block note in unit-0065 continuing across a column. Two fusion loci, both unit-0086 p1 (above).
- **(c) Column order:** natural on every page. Several body paragraphs are split in two at a non-word OCR noise line (units 0050, 0065, 0086, 0104, 0113, 0118, 0120); derivative paragraphing, no marginal or note text involved.
- **(d) Inline furniture (qualifications):** running heads on most multi-page readers (e.g. `An. C. IfiOi 166 BULLARIUM ROMANUM An. C. 1604`), including inside the printed source heading in units 0051 and 0087 and inside hyphen halves in units 0057 p3 (`quibuscu-`/`que.`) and 0067 p2 (`consli-`/`lulionibus`); signature marks inline in body at unit-0069 p1 (`ad do-`/`cendum`: `Bidl. Rom. - Voi. XI. 29`) and unit-0057 p2 (own line), and appended to note blocks in units 0051, 0060, 0087, 0091 and 0116.
- **(e) Fragments:** none assigned; all are `printed-act`.
- **(f) Non-word noise:** short specks and reverse-page show-through inside body lines in most readers (e.g. unit-0049 `ma- p ,■ ■ ,\--,,' ■ i , !● ture`); literal OCR noise with the nearby marginal block complete, except the two unsure tokens listed above.

## Limitations

Literal, uncorrected, uncollated historical OCR rendered as a mechanical two-column source edition. This is a layout review only: no word-level collation, source-boundary audit beyond the noted selection gaps, historical authentication, rights review, publication or installation claim. Literal OCR corruption, odd spellings and conflicting literal dates (e.g. unit-0120 `die xxiv aprilis MDCvi` / `Pat. die 21 aprilis 1607`) are limitations, not defects; no date was inferred or repaired. Automated printed-page labels remain unverified, as the apparatus states.

## Page ledger

| Document | Page | PNG SHA-256 | Status | Observation |
| --- | ---: | --- | --- | --- |
| `bullarium.volume-11.unit-0049.reading-order` | 1 | `7b82e4e1681dfa31d0832893b1785df51531168c412e63dabab698a8aa27c39c` | PASS | Title, issuer, Latin match; heading `CCCLXVII.`; 5 marginals separate; notes `1 Congregationem ...`, `i Islae lilerae ...`, `2 Aptius ...` own blocks at break; running head inline col 2 (qualification). |
| `bullarium.volume-11.unit-0049.reading-order` | 2 | `ce014b646009df498bbdd86980056909374be9d18203eff692098efbfb24fe3d` | PASS | Marginals separate (one continues from p1); running head `An. C. 1604 vili PP. 167` inline col 2; debris block `•> i`; §§ 5-13 in order. |
| `bullarium.volume-11.unit-0049.reading-order` | 3 | `6fa0824a4c07eca68a025d802245d12c5b5af89ea4e77f1fbc5bd56978db7e9f` | PASS | Sparse final page: `Datum Romae ... anno xiii.` / `Dai. die 22 decembris ItìOi ...` then apparatus. |
| `bullarium.volume-11.unit-0050.reading-order` | 1 | `7845df5e4209ecf5935029335e24b1122a75ac09809fde92286f936d8e566eea` | PASS | Title, issuer, Latin match; 7 marginals separate; note `i Ex Regest. ...` own block at col-1 break; running head inline (qualification). |
| `bullarium.volume-11.unit-0050.reading-order` | 2 | `3f737967143389f2b1e64447820aa375de0df0bb8d531b4309bdc2fb565c871a` | PASS | Marginal `Derogai cm-`, § 7, `Datum Romae ...` / `Uat. die 3 ianuarii )605 ...`, notes `1 Lnonee ...`, `i Has literas ...` own blocks, apparatus. |
| `bullarium.volume-11.unit-0051.reading-order` | 1 | `8847ec6d2f6fd67d136982020ec9f7805fac7617e2f873ab8d6bd0a948e30bae` | PASS | Title, issuer, Latin match; running head inside source heading (qualification); 4 marginals separate; six notes own blocks, signature mark `Bull. Hom. - Voi. XI. n` appended to a note. |
| `bullarium.volume-11.unit-0051.reading-order` | 2 | `fd6f2430afdcbc39012de87713db11925869b35e0fc96b22bbe3464d45842dbe` | PASS | Marginals `ciauspiae.`, `Contraria Iti-` separate; `Dalum Romae ... anno xiii.` / `Dal. die 15 ianiiarii 1C05 ...`, apparatus. |
| `bullarium.volume-11.unit-0052.reading-order` | 1 | `b8fde90d839165cd46dcc207ed6741079d633aed1c53469bd4c0cde5102a6654` | PASS | Single page. Title, issuer, Latin match; 4 marginals separate; note own block; running head inline after debris `S`; closing `Defluii! Roniae ...` / `Dal. die 26 ianuarii 1605 ...`. |
| `bullarium.volume-11.unit-0053.reading-order` | 1 | `1339b1be81093f6905a4a43d9c3004dca330a4e4974a2240de7e82c6c5f772ae` | PASS | Single page. Title, issuer, Latin match; 3 marginals separate; closing then note `1 Ex ({egesl. ...` own block; apparatus. |
| `bullarium.volume-11.unit-0054.reading-order` | 1 | `7161b74230942108dba536c5d06a8a4e9bb8d5e9ae1836941607e225424acfd7` | PASS | Single page. Title, issuer, Latin match; marginals separate; note own block at break; running head inline; closing `Dalum Romae ... anno xiii.` / `Dal' die et anno ...`. |
| `bullarium.volume-11.unit-0055.reading-order` | 1 | `06864e859ae879f78d91e102592b42ae533f30a18a245366b6bc1dce808f78f3` | PASS | Single page. Title, issuer, Latin match; marginal between `incum-`/`bat` (qualification); closing then note own block; apparatus. |
| `bullarium.volume-11.unit-0057.reading-order` | 1 | `04b3a8ed67604bdc6d1af840cebf7212287a1bb8a501664d408842c285441a41` | PASS | Title, issuer, Latin match; 3 marginals separate; note `1 la Bullario ...` own block at break; running head inline; § 2-3 OCR specks (addendum f). |
| `bullarium.volume-11.unit-0057.reading-order` | 2 | `ac0729d06b996bf043d85af51c9826e0b4c5370d20207c38d877479a3136e5d6` | PASS | 6 marginals separate; notes `1 Etiam hoc Pii V ...`, `1 llas quoque ...` own blocks; running head and signature mark `Uull. HoìH. - lui. A7. 23` inline (qualifications). |
| `bullarium.volume-11.unit-0057.reading-order` | 3 | `38bb024d8d9e0f20eebb410cd1e0a7d89366c092c27c65fe259415131c1e7fa2` | PASS | Running head between `quibuscu-`/`que.` (qualification); marginal separate; closing `Dalum Romae ... anno xiii.` / `Dal. die i fobruarii 1605 ...`. |
| `bullarium.volume-11.unit-0060.reading-order` | 1 | `f5529ad908a25f02b5378a1c92ada425ad37588df3e3bcd0e71eaeb7fe2a4574` | PASS | Title, issuer `Leo Papa XI, ...`, Latin match; heading `II.`; marginals separate; note own block; ten one-character debris lines then running head (qualification). |
| `bullarium.volume-11.unit-0060.reading-order` | 2 | `a8c85bfde803299a9d7ec2839c19c897e46c4ca4fcc7165d64068e57d50a2198` | PASS | Note `1 Vide Const. xxvii ...` own block with signature mark appended; running head inline; marginals separate; closing `Datum Romae ... anno i.` / `Dut. die 16 aprilis 1605 ...`. |
| `bullarium.volume-11.unit-0065.reading-order` | 1 | `5448360d4eba9d2f6dee942205cff65d256cddff05934bba50813fd128d281d4` | PASS | Title, issuer `Paulus episcopus servus servorum Dei , ...`, Latin match; marginals separate; note `2 Collegii ...` and its continuation as note-only blocks; running head inline. |
| `bullarium.volume-11.unit-0065.reading-order` | 2 | `847c13e1598e1437a52515b27977db1a825d092811973f8f32d1d72039cced11` | PASS | Four notes own blocks at two column breaks; two running heads inline; marginals separate; §§ 4-5 split at noise lines. |
| `bullarium.volume-11.unit-0065.reading-order` | 3 | `cf4e8a7f8c42fec82ebe91a1ffaf5070bf834660f030d852ce730a021ec971a8` | PASS | Marginal `FiJe» Iran- iomptorum.` separate; § 10; sanction; closing `Dalum Romae ... anno i.` / `Dal. die 1 iulii 1605 ...`. |
| `bullarium.volume-11.unit-0067.reading-order` | 1 | `61d818e19f46464704dba7d87e3fbc507e59c02eab1dbf3f8ee370dd651218df` | PASS | Title (extracted text equals metadata), issuer, Latin match; note own block; running head inline; 7 marginals separate (two mid-sentence in § 4: qualification). |
| `bullarium.volume-11.unit-0067.reading-order` | 2 | `0e8c4dd348e53bff7b2c7d86e2f2f784627c824deefae24dad47a80261ed091a` | PASS | Running head between `consli-`/`lulionibus` (qualification); marginal separate; closing `Dalum Romae ... anno i.` / `Dal. die 20 augusti 1605 ...`. |
| `bullarium.volume-11.unit-0069.reading-order` | 1 | `597020021b7b02a8926cc4224f7cc88184037a8219591346baf858da9047ef7d` | PASS | Title, full protocol issuer, Latin match; note own block; running head inline; signature mark `Bidl. Rom. - Voi. XI. 29` inside body between `ad do-`/`cendum` (qualification). |
| `bullarium.volume-11.unit-0069.reading-order` | 2 | `fc837be4fc666b7f9716728d7fa9ac01826afcd96e6232a3e4bc39efb6015f27` | PASS | Two notes in one note-only block; running head inline; marginal separate; closing `Datum Romae ... anno i.` / `Dal. die 10 septembris 1605 ...`. |
| `bullarium.volume-11.unit-0071.reading-order` | 1 | `a5e5587e12f8ea165e168615178e246640c568a60143cb7c57f47c8ccae4fc0c` | PASS | Single page. Title, issuer, Latin match; marginals separate (one mid-sentence); closing then note own block; apparatus. |
| `bullarium.volume-11.unit-0072.reading-order` | 1 | `047396a32084b94565f9d31cc47507557c19a05d57a7be0c486a3de1162f5121` | PASS | Title, issuer, Latin match; note own block at col-1 break; two running heads inline; marginals separate. |
| `bullarium.volume-11.unit-0072.reading-order` | 2 | `88740c1765fd110c300b7c0d4c8a3c43c92c24d0dd7247c224babb9683a87c3d` | PASS | Debris block `^` between `pos-`/`sessioiiem`; marginal separate; closing `Dalum Romac ... anno i.` / `Dal. die 17 septembris 1C05 ...`, note own block. |
| `bullarium.volume-11.unit-0080.reading-order` | 1 | `e40a4b8503428cc5c49cab5b2d03ac1198cd93cf5de041322bed79fbd72c6ce0` | PASS | Single page. Title, issuer, Latin match; marginals separate; closing `Dalum Romae ... anno i.` / `Dal. die £3 decembris 1605 ...`, note own block; apparatus col 2. |
| `bullarium.volume-11.unit-0086.reading-order` | 1 | `949ba1b5f55c6705738d06ec56a45cb0dd1bce7300d8b031995d03be354ac0a7` | CHANGES_REQUIRED | Col 2 § 5: note continuation `Gregoiii XIII quae legitur ... (p,. T ).` inside the body paragraph after `plu-`, and body `res separaliones fecit ... revidil.` inside note `2 Edil. Main. ...` (BLOCKING, addendum b). Title, issuer, Latin match; marginals separate; unsure token `vili` in § 1 noise. |
| `bullarium.volume-11.unit-0086.reading-order` | 2 | `43f569cfa8d30e2f68545abda04a270fb205e864b34c39a6aaa23e5be8c1a55c` | PASS | Notes `3 Conslit. ...`, `4 Clomenlis ...`, `1 Non male ...` own blocks; running head inline; 5 marginals separate; §§ 7-11 in order. |
| `bullarium.volume-11.unit-0086.reading-order` | 3 | `b68c4005510ed9cf1486121e58e72545e16636df35017eaf324e96a376f6c93e` | PASS | Sparse final page: `Datum Romae ... anno u.` / `Dal. die 17 mailii 1606 ...`, note `1 Decst hic ...` own block, apparatus. |
| `bullarium.volume-11.unit-0087.reading-order` | 1 | `78ca799fd5744ebeebc2f77fb59e0dee00ac95c9147176f5e1894f972d273af9` | PASS | Title, full protocol issuer, Latin match; running head inside source heading (qualification); marginals separate; four notes own blocks, signature mark appended to one. |
| `bullarium.volume-11.unit-0087.reading-order` | 2 | `53f5f195d94438537dc0851c3a985ccdfda591071b720c376301b0c95d09477c` | PASS | Running head at top; § 4; closing `Dalum Romae ... anno i.` / `Dat. die 1 aprilis 1G06 ...`; apparatus. |
| `bullarium.volume-11.unit-0091.reading-order` | 1 | `99c18d40d528b4dd6f25145a56dceeae324e817630de57576a6dcdfd40f4c71f` | PASS | Title, full protocol issuer, Latin match; marginals separate; three notes own blocks, signature mark appended to one; running head inline. |
| `bullarium.volume-11.unit-0091.reading-order` | 2 | `6e5ffb65908ccddaaeb16270469260e1d8d5818b282ed7d561f4267ef057a801` | PASS | Marginals separate; §§ 5-6; closing `Datura Romae ... anno i.` / `Dat. die 13 maii 1606 ...`. |
| `bullarium.volume-11.unit-0104.reading-order` | 1 | `b0ff4bf9cd86897c3408bc2ec3bd3dd895118a895185c5f040ad6754b5b60959` | PASS | Title, issuer, Latin match; marginals separate (debris `.` block); three notes own blocks; running head inline. |
| `bullarium.volume-11.unit-0104.reading-order` | 2 | `53ee1c5a94fdf602a3c12fe8b7e1b2cc84179f7109e31781695c4b17cf0b67e4` | PASS | Sparse final page: `Dalum Romae ... anno ii.` / `Dat. die 18 seplembris -1606 ...`, apparatus. |
| `bullarium.volume-11.unit-0110.reading-order` | 1 | `a32f2c198d4decd9252980f9e83ebc290d6d26a20fed75161bd8b1f811899ec1` | PASS | Single page. Title, issuer, Latin match; note own block; running head inline; marginal between `Hie-`/`l'osolymilani` (qualification); closing then three notes own blocks. |
| `bullarium.volume-11.unit-0111.reading-order` | 1 | `d8a2113556e4c498bbc6ab304e72d8f18c6aee7034f88429b5ebea58940beb25` | PASS | Title, issuer, Latin match; marginals separate; note own block; running head inline; §§ 1-4 in order. |
| `bullarium.volume-11.unit-0111.reading-order` | 2 | `608da4bec474e984ddbf83cf42939c11d2bfcac0c93cc14e7b6b9483411f4b61` | PASS | Sparse final page: `Datum Romae ... anno ii.` / `Dal. die i5 dicembris 1606 ...`, note `1 Sic legil ...` own block, apparatus. |
| `bullarium.volume-11.unit-0113.reading-order` | 1 | `9ed48343bfa492eebb2e91fc3e72b60f5a03c871baa5366cf8b3f0d3ccd124cb` | PASS | Title, issuer, Latin match; marginals separate; three note blocks at break between `peleren-`/`lui'` (non-blocking); running head inline. |
| `bullarium.volume-11.unit-0113.reading-order` | 2 | `ea1ef39b47c66b65bb9ee65fbe6a292a4801f0408811b26172c35f516cd626a6` | PASS | 5 marginals separate; note `1 Breve isliusmodi ...` own block; running head inline; closing `Dalum Romae ... anno ir.` / `Dal. die 6 fibruarii 1607 ...`. |
| `bullarium.volume-11.unit-0116.reading-order` | 1 | `fc7833860151fb887251454c29f5386b8fd802e2db21d584d9cb78839dc72404` | PASS | Title, issuer, Latin match; 4 marginals separate; note own block; running head inline; dating clause at col-2 foot. |
| `bullarium.volume-11.unit-0116.reading-order` | 2 | `04f2c8fba73e44c43f7a753f0d05892299cbcd55db472e4bbf984c32ab1f9388` | PASS | Sparse final page: `Itat. die 9 martii 1607 ...`, notes `1 Edit. Rom. ...` (signature mark appended) and `1 Die 21 innrlii ...` own blocks, apparatus. |
| `bullarium.volume-11.unit-0118.reading-order` | 1 | `1d093d8d14de199dc473b3f9a4bf866f24e1901ee84513c815f754e10dcd567b` | PASS | Title, issuer, Latin match; marginals separate; notes own blocks; running head inline; unsure token `"éÌìa?us°` in § 2 body line. |
| `bullarium.volume-11.unit-0118.reading-order` | 2 | `623ebb63dce044f15e73933c4f46a8bafbe773aa4e4982a2c8caa6202d93ae7f` | PASS | Marginal separate; § 4; notes `1 Perperam ...`, `2 Ada ...` own blocks; running head before closing `Dalum Romae ... anno ii.` / `Dal. die i aprilis 1(507 ...`. |
| `bullarium.volume-11.unit-0120.reading-order` | 1 | `cba5fa0edfcbdaf58bb38900f7863ea0a2abd3a66f875f37378165b80ba821d7` | PASS | Single page. Title, issuer, Latin match; marginals separate; two notes in one note-only block; running head inline; closing `Dadim liomae ... anno ii.` / `Pat. die 21 aprilis 1607 ...`. |
