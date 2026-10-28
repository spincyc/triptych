# Bullarium Romanum reading-order visual review: batch bullarium-ro-0004, lane 01

**5 PASS, 0 CHANGES_REQUIRED** of 5 assigned PDFs; 17 pages individually opened at full raster size with the Read tool, zero reused. Every prior blocking locus named in the five `prior_finding` fields is now absent: each printed page-foot note, including note text continued across a page break, is its own block at the page break and separate from every body paragraph, and the unit-0030 title is now the act's heading. No marginal summary is fused into a body sentence or hyphen-split word. Scope: lane 01 of review batch `bullarium-ro-0004`, replacement `reading-order-v2` readers from the coordinate reading-order derivatives of the Naples Bullarium Romanum, volume VIII (1883 printing, artifact `reading-order-0173ea662340`, unit 0176) and the Turin Bullarium Romanum, volume XI (1867 printing, artifact `reading-order-1cd45c76492d`, units 0030, 0037, 0038 and 0086).

## Scope and method

Every assigned page PNG from the repository `pdf-review` run (1700x2200 rasters) was opened as its own full-size image before its observation was recorded in the lane ledger `observations.jsonl` (one line per page). No contact sheet, thumbnail, rerasterization, source acquisition, word-level collation, text correction or date reconstruction was performed.

Each page was checked against the frozen metadata for title line, responsible issuer, Latin label and omission of the unresolved act date; for headings, two-column flow, gutters, margins, glyphs, clipping and overlap; for natural source closing; for modern digitizer signatures and raw placeholders; and, per the series addendum, for (a) marginal summaries as separate TAB-led blocks, (b) page-foot notes as separate blocks, (c) natural two-column order, (d) running heads, folios and signature marks left inline, (e) fragment presentation and (f) non-word OCR noise. Each prior locus was checked twice: visually on the page, and in the reading-order derivative at the cited LF lines.

## Mechanical support

Read-only lane scripts split each selection of the derivative at its manifest line ranges (`mech.py`, `notes.py`). The lane holds **54 TAB-led marginal blocks**; 0 paragraphs mix TAB-led and body lines. Eight marginal blocks fall between the halves of a hyphen-split body word, as separate blocks (qualification under addendum (d)). The note probe found **69 printed-note blocks**, each opening its own paragraph; no editor tag of the `(R. T.)` kind and no note-start line occurs inside a body-opening paragraph. These counts match the pages as viewed. No PDF log has a `Missing character` or `Overfull` entry; no body TeX contains `Google`/`Digitized` variants or a bare `None`; the render receipt records `compiled`, text fidelity `pass` and no warnings for all five.

For the unit-0086 `UNSURE` item, `rows.py` printed the volume XI geometry recipe rows (`reading-order-recipe-072bfb851865/recipe.json.gz`, SHA-256 `072bfb8518656c6fcd94ea408d459357b3881de18925d584ce19acccf7715c9c`) beside the derivative lines they produced; its output is retained as `recipe-rows.txt`. Row WORD counts match the derivative lines one for one. The rows only show the coordinate role the recipe gave each WORD. They do not collate any wording.

## Evidence verification

All assigned PDF, receipt, frozen-manifest and raster-run digests, and every page PNG digest (25 files in all), were computed before and after inspection. All matched the assignment pins both times, and the two verification records are byte-identical. PDF page counts (`pdfinfo`) equal the assigned counts.

| Evidence | SHA-256 | Verification |
| --- | --- | --- |
| Render receipt `.scratch/typeset_pipeline/claude/bullarium-ro-0004/receipt.json` | `546498b74188c8848122afd5bd187a35afc82def83211f82456d8210ea651ca5` | Before and after |
| Frozen manifest `.scratch/typeset_pipeline/claude/bullarium-ro-0004/frozen-manifest.json` | `04806aa99394dba0611989b5a13b8bfcdb220d8ee3af17b934b5ab287d46de03` | Before and after |
| Raster run `.scratch/claude-review/rasters-bullarium-ro-0004/review-run.json` | `1e6784e3ebeb0a99e0100139413b0e5bdaf83b9987b788781f9531bcaa422e13` | Before and after |
| Lane assignment | `784aba90908f095a9eed1a9d30edfb029d48b03bfe298efd304c8807d22840f8` | Scope binding, unchanged |
| `verification-before.json` | `9f4f69635962cac5af09735e6cec20fd7e80cf3192aa44954329b93ab95e1edc` | All match |
| `verification-after.json` | `9f4f69635962cac5af09735e6cec20fd7e80cf3192aa44954329b93ab95e1edc` | All match; identical to before |
| `observations.jsonl` | `fe816141dd682856f4e893517c09c9a521e5692c6365c6c93eb8409659e5704b` | 17 unique page observations |
| `mech.json` / `notes.json` | `fd18d805c54cd4192020ad5da19b1e36182057564a4b615b81e38f68a77aa1a4` / `2fb81e29c99cdaeda4237fd583b9581dc84617e4d7f92c9f44ae566366ffb52b` | Marginal and note block extraction |
| Derivatives `hybrid.txt` (vol. VIII / vol. XI) | `0173ea6623401c08fb8b03623f03015ac60164c370b3e05047daf4df2ef77872` / `1cd45c76492d54bef7ae10aee49de76ba90c917302361317d2d977515f2e6823` | Equal to the manifest's `sha256` |

## PDF outcomes

All documents display "Latin", omit the unresolved act date, and show the frozen title and issuer strings exactly (whitespace collapsed). Literal OCR issuer forms `Sìxtas Papa T, ad fatnram rei memoriam.`, `Clemens Papa Vili.` and `Clemens Papa Vili,` match the metadata and still identify the issuing pope; they are qualifications. No digitizer footer, tofu, clipping, overlap, collapsed table or raw placeholder was seen. Every document ends on a page that carries source text and its natural ending (dating clause, and for three of them a historical note) before the project apparatus. No final page holds only the colophon.

| Document | Pages | PDF SHA-256 | Marginal blocks | Note blocks | Status |
| --- | ---: | --- | ---: | ---: | --- |
| `bullarium.volume-08.unit-0176.reading-order-v2` | 2 | `81bf6d439059d29b636a22470cd38b05861d6c111250a0db5f0f2a2c13b3936e` | 7 | 2 | PASS |
| `bullarium.volume-11.unit-0030.reading-order-v2` | 5 | `78c2318c4991c0291b5b28f20428ce144a2249a6d9d21ab28fdee3c132a633aa` | 17 | 35 | PASS |
| `bullarium.volume-11.unit-0037.reading-order-v2` | 3 | `beb1c07cfa53e369240e3ce98ff4da5de7bbfade1ac749de625bbbe7d483ae20` | 7 | 11 | PASS |
| `bullarium.volume-11.unit-0038.reading-order-v2` | 4 | `491690c8d22e06ae8f47c4b63875f12220491845a4c57392639776599f4d38ab` | 11 | 12 | PASS |
| `bullarium.volume-11.unit-0086.reading-order-v2` | 3 | `415257729bbdcc10e586a5564917588d91a431f8220650e011b72a78483d9710` | 12 | 9 | PASS |

## Prior findings: confirmation per locus

- `unit-0176` (prior: note run into § 4 at p. 2). **Fixed.** § 4 ends `aliteriudicandietin-` (LF 79615). The note `■ Haec moderatio est fortasse extensa etiam ad provinciam Dalmatiae et luslinopolilanam.` (LF 79617-79618) is now its own block. The running head `1. e. 1580 SIXTI'S V pp. r.S.T An C. 1586` (LF 79621) is a separate block, and the body resumes `terprelandi facultale` (LF 79623) in its own paragraph (p. 2, left col).
- `unit-0030` (prior: three note fusions and a marginal-fragment title). **All fixed.**
  - Note `1 Bull. Ord. cil. legit de Clavasio (R. t.).` is its own block (LF 16802; p. 2, left col).
  - The body continuation `annexo- rum respeclive etiam quinquaginta* duca- ...` now continues the body paragraph at the top of p. 2 (LF 16738-16771). Note `3 Edil. Mail). ... siciit paulo post (R. T.).` (LF 16807-16809) is pure note text.
  - The note 3 tail `de qua unione vide supra Conslit. cccxxvil eiusdem Clem. Vili pag. 30 (r. t.).` is its own note block (LF 16962-16963; p. 3, left col). It follows its head `3 Nescio annon ...` and comes after the body ends `simul vel successive (eliam in`. The note is now split into two note blocks, a qualification.
  - The displayed title is the act heading `Suppressio nonnullarum ecclesiarum , ca- pcllarum ci prioratuum dticatux Sa- haudiac et principalus Pedcmonlium, el upplìcatio ac unio ipsorum mililiae Ss. Mauritìi et Lazari '.`. `Ordiiies Alili ; lilaros prò de- '` now appears only as a marginal block.
- `unit-0037` (prior: note 2 continuation inside the body). **Fixed.** The body reads `episcopi JIer])ipo- / lensis coUationi` contiguously (LF 20017-20018; p. 1, right col). The continuation `len. ecdesiarum praedictarum; ... (R. t.).` is its own block at the page break (LF 20066-20068; p. 2, left col).
- `unit-0038` (prior: note 1 continuation inside § 5). **Fixed.** § 5 reads `defuncla- / rum, applicavit` contiguously (LF 20678-20679; p. 3, right col). The continuation `una Cìemeiitis Vili Conslitutio ... (R. t.).` is its own block (LF 20738-20740; p. 4, left col).
- `unit-0086` (prior: two note fusions, an `UNSURE` token and inline heads). **Fixed and resolved.**
  - § 5 reads `clementi^ plu- / res separaliones fecit , faclasque eliam iuxta sibi tributam facullatem revidil.` in one body paragraph (LF 41717-41719; p. 1, right col).
  - The note continuation `Gregoiii XIII quae legitur in Buìl. toni, viii jiag. 307 (p,. T ).` (LF 41775-41776) and note `2 Edil. Main. leg. separareuUir ; ... (n. t).` (LF 41782-41784) are separate note blocks with no body words (p. 2, left col).
  - The `UNSURE` token `vili` (LF 41629) is resolved under (f) as body-column OCR noise, not a marginal word. The recipe classes the nine-WORD run `,. . . . . „ • r> vili` as `R` (body-right) on leaf 332 row 82, together with `licis recordalionis Gregorius Papa XIII,`. In XML order those WORDs precede the margin WORDs of the same OCR line. The § 1 margin-right block holds exactly its eight WORDs, `Aniiiuiuiera l""iis relidiiinis recensei ronti. ffxaconsllliitio- ne(;reBoni.\iii laudatam.`, ends with a full stop, and is rendered as its own block. Leaf 332 records no inseparable WORD. Its glyph origin (speck or reverse-page show-through) is not established, but it does not affect the status.
  - The running heads remain inline, which is non-blocking under (d).

## Addendum checks

- (a) Marginal summaries: 54 separate TAB-led blocks and no fusions. Eight blocks sit between the halves of a hyphen-split body word; these are qualifications:
  - `unit-0176`: `•` between `le-`/`neatur;` (LF 79642).
  - `unit-0030`: `Bcneiìcu ec- clesiaslica hic espr»»*»,` between `me-`/`rito` (LF 16704). `•` between `Car-`/`pes,` (16722). `cumprimum quoniodolibet >^<-a\eriat,` between `as-`/`serii,` (16773). `Kt benttGcia in ecclesiis ...` between `supplica-`/`tionibus` (16931). `Eiiamsireser-` between `disposi-`/`tioni` (16995). `'•' m^i'ii^s pratMliridtì an- ...` between `in-`/`stilulas,` (17048).
  - `unit-0038`: `Addii.s am- plissiniis facul- tatìbus.` between `obli-`/`galos` (20496).
- (b) Page-foot notes: 69 separate note blocks and no note run into a body, synopsis or protocol paragraph. Continued notes are separate blocks at the next page break: `unit-0037` `len. ecdesiarum ...`, `unit-0038` `una Cìemeiitis ...` and `unit-0086` `Gregoiii XIII ...`. The `unit-0030` note 4 (`Id. omittit partic. ...`) flows from the left into the right column inside its own note block, which is column flow and not a fusion. Two qualifications are unchanged from the prior review. Note-to-note merges remain in `unit-0037` (`1 Turbatissime ...` with `"2 l'aiticulani ...`) and `unit-0038` (`1 Vide super hoc ...` with `'i Praedicla duo ...`). The `unit-0030` note 3 is split into a head block and a tail block.
- (c) Two-column order is natural on all 17 pages. Body halves split at page breaks resume after the notes and running head: `Iler-`/`bipolensis`, `l'ru-`/`elibus`, `iudi-`/`cium`, `ge-`/`neiali`.
- (d) Inline running heads are non-blocking: `unit-0176` 2, `unit-0030` 5, `unit-0037` 3, `unit-0038` 5, `unit-0086` 2. One printer signature, `Bull. Hom. — Voi. A7. 15`, is set as its own block in `unit-0037` on p. 3. Stray one-glyph blocks `i` (p. 3) and `|` (p. 4) sit at page breaks in `unit-0030`.
- (e) No fragments are assigned. All five have extent `printed-act`, and each shows its heading, protocol and closing.
- (f) The non-word noise runs inside body lines are listed per page in the ledger. Examples are `^ „ . °`, `■ ■ ... -i'.*`, `. , •. 1- • • 1 . ...`, `1 • ■. j> •. 11 •`, `• i' T-.1 •!• • -1`, `,., ,. r> , rr,i i •` and `T^ i ■• . ,. . ,.`. They are non-blocking because the nearby marginal summaries are their own blocks. The `unit-0086` § 6 marginal `nicmodoPon- lifcx conlirraal eiusraoji sepa-` ends on a hyphen. It holds all five margin-right WORDs of its recipe block (leaf 333). The run `,., ,. r> , rr,i i •` is classed body-right on the row of `lilati`, level with the marginal's second row and not below `sepa-`. The marginal's missing tail has no native OCR WORD, which is a literal OCR limitation and not a fusion.

## Per-document findings and qualifications

- `bullarium.volume-08.unit-0176.reading-order-v2` — **PASS.** Prior locus fixed (above). Qualifications:
  - Issuer `Sìxtas Papa T, ad fatnram rei memoriam.`, as in the metadata.
  - A one-glyph marginal `•` between `le-`/`neatur`.
  - `■•` after `Italiam` in § 4 is a non-word mark, plausibly the note reference.
  - The closing `Dat. die 29 marti! 1586, ponliC. anno i.` is literal.
- `bullarium.volume-11.unit-0030.reading-order-v2` — **PASS.** The prior loci and the title are fixed (above). Qualifications:
  - Six marginal placements between hyphen halves.
  - Note 3 split into head and tail blocks.
  - Stray `i` and `|` blocks.
  - Five inline running heads.
- `bullarium.volume-11.unit-0037.reading-order-v2` — **PASS.** Prior locus fixed. Qualifications:
  - The note-to-note merge on p. 2.
  - The signature block on p. 3.
  - The literal `Dat. die 31 iulii 1601`, which is not repaired.
- `bullarium.volume-11.unit-0038.reading-order-v2` — **PASS.** Prior locus fixed. Qualifications:
  - The note-to-note merge on p. 4.
  - One marginal between hyphen halves.
  - The selection includes the separately listed dating note at LF 20853-20859, which is rendered as its own block after the dating clause.
- `bullarium.volume-11.unit-0086.reading-order-v2` — **PASS.** Prior loci fixed and `vili` resolved (above). Qualifications:
  - The `sepa-` marginal tail is absent from the OCR.
  - On p. 2, the body line `§ 8. Sicoue wcr quoscumoue iudices et` and a noise-only line `. . * '. ^. „` are set as short separate paragraphs. This is a layout qualification with no marginal words.

## Individual page evidence

| Document | Page | Page PNG SHA-256 | Observation |
| --- | ---: | --- | --- |
| `unit-0176` | 1 | `1b71f86dc8fb539269466bd8e8bd8324fe3be89917473865858b7c71bbb9c014` | Title, issuer, Latin, date omitted. The marginals `Eiordiam`, `P'"' ▼ au ...`, `Enmque sup- ...` and `Hic Poniifex ...` are separate. Note `1 De hoc Ordine ...` is its own block, then inline head `An. C. 1586 fi^-^ RrLLARimi ROMANUM ...`. Noise `^ „ . °` appears in § 2. |
| `unit-0176` | 2 | `ef3a1ce66ae88cedb7f355ab0f1cf04c524b2848c37b19dedab1ba10aebc455a` | Prior locus fixed: note `■ Haec moderatio ...` and the running head are each separate blocks. The marginals `ri.n(ni»ede- -iioriM.`, `•` and `Ttin.ampio- ...` are separate. The closing `Datum Romae ... anno i.` and `Dat. die 29 marti! 1586 ...` precede the apparatus. |
| `unit-0030` | 1 | `52cfe564001ac5103f0e36a55f7b44c4fbf211dabf490d2e976b5b5f34c1422e` | The title is now the act heading. Four marginal blocks are separate, two of them between hyphen halves. Notes `1 Ex Regest. ...`, `1 Nempe: ...` and `2 Bullarium Ord. ...` are separate, then head `1601 CLEMENS Vili PP. 83 ...`. The right col ends in body text. |
| `unit-0030` | 2 | `d9dc4668d02df060fd6996fc187d2b61dacb8410c7ed3afddd79bd33eb1824f4` | `annexo- rum respeclive ...` is body text. Notes 1-9 and 1-5 are separate blocks, with note `1 Bull. Ord. cil. ...` and note `3 Edil. Mail). ...` both clean. Then head `An.n. 160i 8i BULLARIUM ...`. The marginals are separate. |
| `unit-0030` | 3 | `74e1b43cc34995383f267d62a99c0f57f780bf7797b2a9f22629770322525ca6` | The note 3 head and its tail `de qua unione ...` are separate note blocks after the body ends `(eliam in`. Six marginals are separate. A stray `i` block is followed by heads 85 and 86. |
| `unit-0030` | 4 | `8a335b42bb7c41c8c7634cf219085d4df4927af111f0fd8a8d0ace1b67c3b3ef` | The marginals `Clausure.`, `i^ep"iai ««•` and `ira^f"»^' """` are separate. Notes 1-3 are separate, then a stray `|` and head `An.C 1604 CLEMENS Vili PP. 87 ...`. The body resumes `cium evocetur`. |
| `unit-0030` | 5 | `d19a2cdf257617f32d1be0658a16af57a6a09feff8b3e211462cfafeae108ad5` | Marginal `ciausnue pne- nales.`, § 7, and the dating `Daluni Romac ... anno xiii.` and `Dal. die 15 iunii 1604 ...`. Three note blocks follow, then the apparatus. |
| `unit-0037` | 1 | `929719fc41d06ff914e5b9543bb6dd82ea4d22799bd58f13ee942cae374f0a9c` | Title, issuer, Latin and address. Two marginals are separate. Notes 1, `ì`, 2 open the right col, then head `An. e. ItiOi CLEMENS Vili PP. Ili ...`. `JIer])ipo- / lensis` is contiguous. |
| `unit-0037` | 2 | `1514ae402f394c03322ad246e10a0ea9feacdeaadbd236b56e2a71694959c011` | The continuation `len. ecdesiarum ...` is its own block. The notes are separate, with the 1+2 merge as a qualification. Heads 112 and 113 are inline. Three marginals are separate. Noise runs appear in the § 1 and § 2 lines. |
| `unit-0037` | 3 | `c7d0aa747512ad34a5cb6790ae9538d4ab6f31cfc27f27765273b7770294aaca` | Two marginals are separate. The signature `Bull. Hom. — Voi. A7. 15` is its own block. The closing `Palum Romac ... anno xiii.` and `Dat. die 31 iulii 1601 ...` precede the apparatus. |
| `unit-0038` | 1 | `04309ebfa2a8afa085dddcbbdc9c6e26c1a3e7b45248e1d877eda441e365264a` | Title, issuer and Latin. Marginals `Pliilippus n ob ratioaes ...` and `Coiiccsserai Cleiucus.` are separate. Notes 1 and 2 are separate, then head `An. C. 1601 Il-i nULLARlUM ...`. |
| `unit-0038` | 2 | `cecbda585524e8eff131bac2259515553b79143fe5e7d4d647372830afd85779` | Four notes are separate, then head 115. Three marginals are separate, one of them between `obli-`/`galos`. Noise runs appear in § 3 and in the right col. Head 116 is inline. |
| `unit-0038` | 3 | `af7c280cdd0b040a71afedf2f9d0c0da4ae648f36dda61a26f45694a4aacc6e5` | § 5 is contiguous at `defuncla- rum`. The note head `1 Sub liac dalà ...` is its own block before head 117. Four marginals are separate. |
| `unit-0038` | 4 | `34f2eb64eb5df09be8872c39457a0e75d6e28f633634aebaeeb5cddf3ef2aef4` | The continuation `una Cìemeiitis Vili ...` is its own block. The notes are separate, with the 1+2 merge as a qualification. Head 118 is inline. Marginals `ciausuiae.` and `Derogatio coi-` are separate. The closing `Datum Romae ... anno xiii'.` and `Dal. die 4 aiigust. 1604 ...` are followed by dating note `1 Edit. Muin. ...`, then the apparatus. |
| `unit-0086` | 1 | `fcc309224c6cf682cafaeac31bf2bdc272bc2673676440dd7ae196ec3fbc0ae8` | Title, issuer and Latin. Seven marginals are separate. `vili` is body noise per the recipe roles. § 5 `plu- res separaliones ...` is contiguous. Notes 1 and `ì Praedicta ...` are separate, then head 295. |
| `unit-0086` | 2 | `bceae6bedc24a023d4e039628d6676bd6864f91aca7e09e832c77dafdb3285ec` | The continuation `Gregoiii XIII ...` and note `2 Edil. Main. ...` are separate blocks with no body words. Head 296 is inline. Five marginals are separate. § 8 is split into short paragraphs with a noise-only line. |
| `unit-0086` | 3 | `c956ed017149647617f5faeae513d17056673e0a1803687e1dbf0bc21257c619` | A sparse source-bearing final page: `Datum Romae ... anno u.`, `Dal. die 17 mailii 1606 ...` and note `1 Decst hic ...`, then the apparatus. |

## Limitations

These are literal, uncorrected, uncollated historical OCR reading editions in a mechanical two-column layout. This was a layout review only. It does not collate words against the printing or a facsimile, authenticate historical wording, adjudicate rights or provenance, or normalize dates. Literal OCR dates such as `Dat. die 31 iulii 1601` and `Dat. die 29 marti! 1586` are recorded as they stand.

The recipe-row check above only decided whether a token was classed as body or marginal text. It is not collation, and it does not establish a glyph's printed origin. Garbled words and speck strings are literal source OCR. PASS covers only the hash-bound visual review recorded here and the pinned PDF bytes. It makes no publication, installation or deployment claim.
