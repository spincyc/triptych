# Pius IX Acta visual review — pius-0001 lane 01

CHANGES_REQUIRED: 24 assigned PDFs, 65 pages individually opened at full size; 23 PASS, 1 CHANGES_REQUIRED. All pages are new inspections; zero reused pages. Scope is lane 01 of batch `pius-0001`: newly admitted Pius IX readers from *Pii IX Pontificis Maximi Acta*, pars prima, volume I (Rome 1854; Latin) and *Atti del sommo Pontefice Pio IX*, parte seconda, volume I (Rome 1857; Italian).

## Scope and method

Each page PNG from the repository's `pdf-review` raster run (as pinned in the assignment) was opened individually at full size with the Read tool; no contact sheet, thumbnail or re-rasterization was used. Per page, the title line, responsible issuer, date and language were compared with the frozen metadata, and headings, two-column flow, gutters, margins, glyphs, note placement, folio/running-head/signature furniture, modern digitizer signatures, raw placeholders and the natural source closing were checked. Text extraction (`pdftotext`) and the source OCR, line map and pinned OCR-layout XML were consulted only to locate and identify suspected furniture after visual inspection; they did not substitute for viewing any page.

Standing rulings applied: an issuer line `PII IX PONTIFICIS MAXIMI ACTA` taken from the volume title and matching the metadata is a non-blocking qualification; OCR-damaged issuer spellings matching the metadata (`pivs PP. IX.`) are qualifications; notes set as their own block at a source page break are non-blocking; in these boundary-reviewed series a folio number, running head or gathering signature left inside the body is BLOCKING.

## Evidence verification

All assigned PDFs, the receipt, the frozen manifest, the raster-run record and every page PNG were hashed before and after inspection; every digest matched its assignment pin both times (92 files; before and after records identical).

| Evidence | Path | SHA-256 | Verification |
| --- | --- | --- | --- |
| Render receipt | `.scratch/typeset_pipeline/claude/pius-0001/receipt.json` | `720d0acae7c1f32315fd11d968d13eaa0510b72ea25906a6916054bd2ada2d73` | Before and after |
| Frozen manifest | `.scratch/typeset_pipeline/claude/pius-0001/frozen-manifest.json` | `583691e3d8941ca1c9a3a3f27f4cc57747afcfb3b3817776aad37a103df9d736` | Before and after |
| Raster run | `.scratch/claude-review/rasters-pius-0001/review-run.json` | `5718cc943c5d94fdf4a333529ce03aa4e55089d3d90a4801f03abb5e9597e7c6` | Before and after |
| Lane assignment | `.scratch/claude-review/pius-0001/lane-01/assignment.json` | `9b4cf451b69ac76262de203708524f84ad8e00e8f0fbb984233198d90d710860` | Scope binding |
| Inspection ledger | `.scratch/claude-review/pius-0001/lane-01/observations.jsonl` | `7371341766780debdf8969e5e960fbd75b46a6192ef93e023a2f86a6880ace00` | 65 unique page observations |
| Before verification | `.scratch/claude-review/pius-0001/lane-01/verification-before.json` | `14b67347c3615e9b3acfb1ca5b86125d1c8ad185455476e636b3f91dcffea5b3` | all_match True |
| After verification | `.scratch/claude-review/pius-0001/lane-01/verification-after.json` | `14b67347c3615e9b3acfb1ca5b86125d1c8ad185455476e636b3f91dcffea5b3` | all_match True; identical input hashes |

## PDF outcomes

| Source ID | Date | Language | Pages | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- |
| `pius-ix-acta.pars-02-volume-01.line-00000154` | 1846-07-16 | `it` (Italian) | 1 | `ae0098b33000924a9ce5b8c3219fc17546137e1a4c989f11e6effd9dd556a6c2` | PASS |
| `pius-ix-acta.volume-01.line-00000166` | 1846-07-27 | `la` (Latin) | 1 | `945833669cc02c8b4f6eca00e2f90620753d40b04d320237fd1c44fb8a9c457c` | PASS |
| `pius-ix-acta.volume-01.line-00000248` | 1846-11-09 | `la` (Latin) | 6 | `6c62369fbf6ec1ced6d318e647c5cedc3b786f57da2c109cffcc564b382540d6` | PASS |
| `pius-ix-acta.volume-01.line-00001024` | 1846-11-20 | `la` (Latin) | 2 | `b9ec19c1717e52138d33d6f35b1f04ac1e676e887d496d84c60b9fe6d3302745` | PASS |
| `pius-ix-acta.volume-01.line-00001267.part-01` | 1847-03-25 | `la` (Latin) | 2 | `c17ef9a7c9d883ee6c1cff0180a1d68359e7e66b8281372f12b28c059a04e948` | PASS |
| `pius-ix-acta.volume-01.line-00023100` | 1847-06-01 | `la` (Latin) | 2 | `9a17ee30708466456cd196192ef4e6eace53c1e3c90e704e6ae30ded31756565` | PASS |
| `pius-ix-acta.volume-01.line-00001267.part-02` | 1847-06-11 | `la` (Latin) | 2 | `7cfe4ca9e771aee83436369a66792056998a6f6453a23a34b90d7b4f127a4e27` | PASS |
| `pius-ix-acta.pars-02-volume-01.line-00002039.part-01` | 1847-06-12 | `it` (Italian) | 4 | `c98d01767b080e89e8fd460221e59f5a355f69f64ad867dbf06e3ebd87d47b7a` | PASS |
| `pius-ix-acta.volume-01.line-00001650` | 1847-06-17 | `la` (Latin) | 1 | `85c6d028c5b04485a7f979612f60fa352e8ce8902a2e95dc8c907cbb7d1761bf` | PASS |
| `pius-ix-acta.volume-01.line-00001756.part-01` | 1847-06-17 | `la` (Latin) | 3 | `57bb2abe51bacc2082ba79423cfd37c0e534a7ea418e6ae74a159e1f69e38b7d` | PASS |
| `pius-ix-acta.volume-01.line-00001756.part-02` | 1847-06-17 | `la` (Latin) | 1 | `2b228aebed067ea63e5b0685b68524585f58e6ffb8a06082ccfa496c48741aa8` | PASS |
| `pius-ix-acta.volume-01.line-00002099.part-01` | 1847-06-21 | `la` (Latin) | 1 | `fd0a401c4b636757cc034bb96d8e73c4bd0b7c476a2d9c35e5504d499192b6cf` | PASS |
| `pius-ix-acta.volume-01.line-00002099.part-02` | 1847-07-23 | `la` (Latin) | 2 | `014a4f905bd7fd8e587ce8a3767ac5e1ad3e570394565ff89323a5635caca334` | PASS |
| `pius-ix-acta.pars-02-volume-01.line-00004832.part-01` | 1847-10-01 | `it` (Italian) | 6 | `5802f82a312215f8db22b6ac4cddee0b61e028cc8374fc74e4c77e103c728183` | PASS |
| `pius-ix-acta.volume-01.line-00002336` | 1847-10-04 | `la` (Latin) | 2 | `deaa8e0f40bb6e22ca7d32d3d136b69e4d3804d84ede6f2feb39802a013f964d` | PASS |
| `pius-ix-acta.pars-02-volume-01.line-00004832.part-03` | 1847-10-14 | `it` (Italian) | 5 | `a6b3c9027fed8ef554254435d3fbdb2308faf190b36cb80bf713e841c170f580` | PASS |
| `pius-ix-acta.volume-01.line-00002530` | 1847-12-17 | `la` (Latin) | 3 | `5c170595a157d2c2e79b9a1cca9be4b084e55daa6245be54a6f43d368ddfecd2` | PASS |
| `pius-ix-acta.volume-01.line-00002818.part-01` | 1848-01-06 | `la` (Latin) | 5 | `b4f498a8d9fcd1cce2b415f509673415ccdbaef8fbca2187eb1dfea86e19df29` | CHANGES_REQUIRED |
| `pius-ix-acta.volume-01.line-00023322.part-01` | 1848-01-17 | `la` (Latin) | 1 | `2676dab35c3b5d7ea4c673dba795abab1247e66812d5a1685d60685c04053115` | PASS |
| `pius-ix-acta.pars-02-volume-01.line-00008741.part-04` | 1848-03-14 | `it` (Italian) | 5 | `a8b8439d5df069258140c898d4c700810c33b722c0766c187175b4308506fc5c` | PASS |
| `pius-ix-acta.volume-01.line-00002818.part-02` | 1848-04-29 | `la` (Latin) | 3 | `c0aac3c3f2ba715aa3e5d20d14bdc47a46616e68d97b3c332e491a503ff6c68e` | PASS |
| `pius-ix-acta.volume-01.line-00002818.part-03` | 1848-06-02 | `la` (Latin) | 2 | `abc0e6b7c6cdb054edb3fe661603e3b5057462399e796e2502ed6572ec979ddb` | PASS |
| `pius-ix-acta.pars-02-volume-01.line-00008741.part-05` | 1848-06-03 | `it` (Italian) | 3 | `683055e20241d3f508d3f773eb0ed4a9ddeacbd771fa85e16f20e2ba9dcbb607` | PASS |
| `pius-ix-acta.volume-01.line-00003708` | 1848-07-03 | `la` (Latin) | 2 | `4dc1414f03f32bf8ba7b074d95202f76ec5cbf0d8c3bff56d848fd163f851899` | PASS |

## Blocking finding

- `pius-ix-acta.volume-01.line-00002818.part-01` (*In suprema Petri Apostoli Sede — litterae ad Orientales*), page 4: BLOCKING: gathering-signature furniture left inside the body. Page 4, left column, lower half: a standalone line 'ri' (source OCR LF3261, printed at the foot of source page 89, bottom-centre at x1963-2008/y4341-4415 of 3289x5286, the same position as the signature '6' on leaf 79 sixteen leaves earlier) sits between the note block '(2) Ex Eusebio ... Lib. IV. Cap. 23.' and the body continuation 'mus, nihil Nobis antiquius esse', interrupting the sentence 'testamur et confirma-/mus'. The source note says gathering signatures are omitted, but LF3261 is not among this selection's omitted loci (it omits folio '90' at LF3264 only).

No modern digitizer signature, running head, folio number, raw `None` placeholder, clipping, overlap, tofu glyph, collapsed table or fused/interleaved note was found on any other page. No document carried a `prior_finding`.

## Per-document findings and qualifications

### `pius-ix-acta.pars-02-volume-01.line-00000154` — PASS

*Pio IX ai suoi fedelissimi sudditi: amnistia per i delitti politici, 16 luglio 1846*; issuer `PIUS PP. IX.`; 1846-07-16; Italian; proclamation. Prior finding: none.

- p1 PASS (`b698258242a8bf466a8ecaca028af951a565bdd9e2633ee3522ab1592c3220cb`): Title, PIUS PP. IX., 1846-07-16, Italian match metadata. Two columns clean; ends with Datum Romae dating clause and PIUS PP. IX. subscription, then project source/rights notes. No digitizer footer, running head or folio in body.

### `pius-ix-acta.volume-01.line-00000166` — PASS

*Amplissimum consessum vestrum — allocutio in consistorio secreto 27 iulii 1846*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1846-07-27; Latin; consistorial-allocution. Prior finding: none.

- p1 PASS (`dab8df58f5376995e275d72e6dbdd0f52be5a0cf43a6b632c78289ac87843eee`): Title, date 1846-07-27, Latin match. Caption HABITA IN CONSISTORIO..., VENERABILES FRATRES, body in two columns ending 'esse velit ac salutares.' followed by project notes. No furniture in body. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.

### `pius-ix-acta.volume-01.line-00000248` — PASS

*Qui pluribus — epistola encyclica de erroribus aetatis*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1846-11-09; Latin; encyclical. Prior finding: none.

- p1 PASS (`73e5a1cfc1b6210d08047feb55b34c3467cfef0bac22ee9f92942e77658dbfe2`): Title, date 1846-11-09, Latin match. Address, salutation, body in two columns; note (4) Apocalyps. set as its own block at the source page break in right column. No digitizer footer or running head. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata. Non-blocking qualification: isolated literal OCR token '1' on its own line between the address and VENERRABILES FRATRES (source OCR LF255, a 7x17px speck on source page 4, not the folio; page label for that leaf is 4); literal OCR noise, not a folio or running head.
- p2 PASS (`25e51849be010baacd59a10e3210a2a5fd503a999453eb951052f036da3a8294`): Two-column body; source notes (1)-(3) and (1)-(6) set as separate blocks at source page breaks, not fused. No furniture.
- p3 PASS (`52625c8e14017c2486f3c587ee3dd953653b6e72ebb3cec02d0b41ad4d78fb4c`): Two-column body; notes (1)-(4) and (4)/(2) set as separate blocks at page breaks. No folio, running head or digitizer line.
- p4 PASS (`19f11a2596c8bc2161f4445d7d890ad96d94911763c79568393145abcafaa1a6`): Two-column body; notes (1) Ex Symbolo, (4) S. Leo, (1)/(3), (4)/(2)/(3) set as separate blocks at page breaks; literal OCR stray marks ('|', 'ET') only. No furniture.
- p5 PASS (`8498cfe2e8365a48bfedd5825ecc6bf9f6d17f2572fb47d7a3f0a49768811000`): Two-column body; notes (1) Ad Hebr., (1) Concil. Trid. set separately at page breaks. Clean.
- p6 PASS (`7f7751f19cde2b34eec7b641ee69b3b42667f37721d836babad57cfef80c02ef`): Body ends with Apostolic benediction and Datum Romae ... IX Novembris MDCCCXLVI dating clause, then project source/rights notes; notes set separately. Natural source closing.

### `pius-ix-acta.volume-01.line-00001024` — PASS

*Arcano divinae Providentiae — iubilaeum universale ad implorandum divinum auxilium*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1846-11-20; Latin; apostolic-letter. Prior finding: none.

- p1 PASS (`fb40ae476f3da29a7450772301d57531c7edbc6f82b8c9d2f08ea533a39880f5`): Title, date 1846-11-20, Latin match. Address, salutation and body in clean two columns; no running head, folio or digitizer footer. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`e3a485bcd318663a14741b0d3b99370dae12ff1f80fdf84857af77de55a05324`): Body ends with Datum Romae ... sub annulo piscatoris die XX mensis novembris MDCCCXLVI clause and subscription 'A. CARD. LANBAUSCHIAA' (literal OCR, a stray comma line above it), then project notes. Natural closing.

### `pius-ix-acta.volume-01.line-00001267.part-01` — PASS

*Praedecessores Nostros — pro regno Hiberniae*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1847-03-25; Latin; encyclical. Prior finding: none.

- p1 PASS (`7caf188ff462bf70f8d3ea3f53e67bbddcf9047691bf1ba4d39014c74993814e`): Title, date 1847-03-25, Latin match. Address, caption 'Ad implorandum pro regno Hiberniae Divinum Auxilium.', protocol and body in two columns; notes as separate blocks. No furniture. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata. Non-blocking: source note (1) Apud Eusebium breaks mid-word ('Dio-' / 'nysii') and its continuation is set as its own block at the next source page break; not fused into body lines.
- p2 PASS (`694ef4cc6b0abb605183febb94ecf1e34b8fb692b161fe027cca2a49937a8ed5`): Body ends with Apostolic benediction and Datum Romae ... die XXV Martii Anno MDCCCXLVII ... Anno Primo, then project notes. Notes separately set; literal per-line guillemets are source quotation marks. Non-blocking: note (2) Edit. Balutii continuation ('» lia nummorum ...') set as its own block at the following page break.

### `pius-ix-acta.volume-01.line-00023100` — PASS

*Quum illud plurimi — de utensilibus sacris cardinalium et episcoporum*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1847-06-01; Latin; apostolic-letter. Prior finding: none.

- p1 PASS (`5fa66c8f1e2b78642addf4836cb77c7e60af86ba5d1bb2852d9e8a547547db7a`): Title, date 1847-06-01, Latin match. AD PERPETVAM REI MEMORIAM then two-column body with heavy literal OCR corruption (limitation). No running head, folio or digitizer line. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`ed41096c3b3560809da6a5ebd1139368659378b4baabbe35fb9325dd2a2f3c0c`): Body ends with Datum Romae ... sub Annulo Piscatoris die 1 Junii MDCCCXLVII clause and subscription '... A. CARD. LAMBRVSCHINI / A BREVIBVS APOSTOLICIS.' (stray OCR 'mE'), then project notes. Natural closing.

### `pius-ix-acta.volume-01.line-00001267.part-02` — PASS

*Cum, veluti probe noscitis — allocutio in consistorio secreto 11 iunii 1847*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1847-06-11; Latin; consistorial-allocution. Prior finding: none.

- p1 PASS (`c41fbf99e03e01caca7719b5c031728d9a5893ecd61ba9e7fb3c559412b8675a`): Title, date 1847-06-11, Latin match. Literal OCR-damaged caption 'WAEITA 1* CON-ISToR;IO sECRETO ...' and VESERABILES FRATRES (limitation). Two-column body clean; no furniture. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`4c4c5a2f210193e9d14fb392dd2c65eb90c0d9b8fdb7f756ca2d30bd8b6b7c28`): Body concludes with 'Quid Vobis videtur ?', creation formula, names of cardinals and closing 'In Nomine Patris ... Amen.' (literal OCR), then project notes, all in left column. Natural source closing.

### `pius-ix-acta.pars-02-volume-01.line-00002039.part-01` — PASS

*Motu proprio sul Consiglio de’ Ministri, 12 giugno 1847*; issuer `pivs PP. IX.`; 1847-06-12; Italian; motu-proprio. Prior finding: none.

- p1 PASS (`7dffa6da3346d224ac978bed5799c19a958bab87e1ff5daa7b1f09ba271b9761`): Title 'Motu proprio sul Consiglio de' Ministri, 12 giugno 1847', date 1847-06-12, Italian match. Opening protocol, CAPO I headings and numbered paragraphs flow in two columns; no furniture. Qualification: issuer line 'pivs PP. IX.' is an OCR-damaged spelling that matches the frozen metadata and identifies the pope.
- p2 PASS (`704f6c23a42de1890a4ce0bd218bc04bc77fc04042b65d8f0876dfabb1a60164`): Two-column body with CAPO II heading and numbered items; no running head, folio or digitizer line.
- p3 PASS (`a0c78833a2167d8658c306a5035b245aacdb4ef0c091dc6e577b5007e8f6faf8`): Two-column body; CAPO IV/V headings (literal OCR 'GAPO LV.') kept with following paragraphs; no furniture.
- p4 PASS (`a87627c086d847bacbfdcb66e9c6d1a7fe3e60bd2bf40fad4e2da61b1a88b000`): Final articles, derogation clause, literal dating clause and subscription 'pivs PP. IX. MED' at top of right column, then project notes. Natural source closing. Disclosed limitation: dating clause and subscription carry OCR show-through noise ('Dato dal nostro palazzo apostolico al Ouivinale i112) giugno® 1847 ... pivs PP. IX. MED'), disclosed in the project source note; not a layout defect.

### `pius-ix-acta.volume-01.line-00001650` — PASS

*Romanis Pontificibus — de equestris ordinis Piani constitutione*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1847-06-17; Latin; apostolic-letter. Prior finding: none.

- p1 PASS (`7f7dd75bbe94abb8a43dd90bdca9c9b2788af82b828f15c35f89bcb71c765b8a`): Title, date 1847-06-17, Latin match. AD PERPETVAM REI MEMORIAM, body in two columns ending with Datum ... die XVII Iunii MDCCCXLVII clause and subscription ALOISIVS CARD. LAMBRVSCHINI / A BREVIBVS APOSTOLICIS, then project notes. Single page, natural closing, no furniture. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.

### `pius-ix-acta.volume-01.line-00001756.part-01` — PASS

*Ubi primum — ad supremos moderatores ordinum regularium*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1847-06-17; Latin; encyclical. Prior finding: none.

- p1 PASS (`679012709947d93bdaa7743714d43121369cb1d4b3b87cd2b2264072fdac7ce4`): Title, date 1847-06-17, Latin match. Address and salutation then two-column body; no furniture or digitizer line. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`aa2dd557233a3ec5d606cf4089ef494fde60f021203cf7253f238cdc5dca5588`): Two-column body continues cleanly; no running head, folio or fused note.
- p3 PASS (`aaab980e6c4a77299a222ac0597e623bc7b4e70fefcf3547052e84ab42200564`): Body ends with Apostolic benediction and Datum Romae ... die XVII Junii Anno MDCCCXLVII clause, then project notes, in left column. Natural source closing.

### `pius-ix-acta.volume-01.line-00001756.part-02` — PASS

*Cum hisce Litteris — ad locorum ordinarios encyclicam de regularibus mittens*; issuer `PIVS PAPA IX.`; 1847-06-17; Latin; letter. Prior finding: none.

- p1 PASS (`b3f3de30001557a7f24757e6196002e6d46abc5066aa67d8f5e704554f99ded8`): Title, date 1847-06-17, Latin match. Protocol PIVS PAPA IX., salutation and body; ends with Datum Romae ... die XVII Junii (literal OCR 'Ànno TUUM') ... Anno Primo, then project notes (license line flows to right column). Natural source closing; no furniture. Qualification: issuer line 'PIVS PAPA IX.' matches the frozen metadata and identifies the pope (source protocol issuer).

### `pius-ix-acta.volume-01.line-00002099.part-01` — PASS

*Apostolico moderamini — de cubiculariis in ordinem Pianum adlegendis*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1847-06-21; Latin; apostolic-letter. Prior finding: none.

- p1 PASS (`dcfe45f75b11aadfde8858ea012a2118cc4c3348864414bc8e32bddde2d95340`): Title, date 1847-06-21, Latin match. AD PERPETVAM REI MEMORIAM, body, Datum ... die XX1 Junii MDCCCXL VII ... Anno Becundo (literal OCR) and subscription ALOISIVS CARD. LAMBRVSCHINI / A BREYIBVS APOSTOLICIS, then project notes. Single-column fill on one page; natural closing. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.

### `pius-ix-acta.volume-01.line-00002099.part-02` — PASS

*Nulla celebrior — de patriarchatu Hierosolymitano*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1847-07-23; Latin; apostolic-letter. Prior finding: none.

- p1 PASS (`ed76185a3728249f30de008ae6c24ff85f519d05c388da16d892bb13767824a8`): Title, date 1847-07-23, Latin match. AD PERPETVAM REI MEMORIAM and two-column body; no running head, folio or digitizer line. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`b2f5ffc61066af872d90007cc560b7e269e6780256da584c91f39d8a7ef62817`): Body ends with Datum Romae ... die XXIII mensis Julii MDCGCXLVIL ... Anno Secundo and subscription PRO DOMINO CARD. LAMBRUSCHINI A. Picchionm Substitutus, then project notes. Natural closing.

### `pius-ix-acta.pars-02-volume-01.line-00004832.part-01` — PASS

*Motu proprio sulla organizzazione del consiglio e senato di Roma e sue attribuzioni, 1 ottobre 1847*; issuer `PIVS PP. IX.`; 1847-10-01; Italian; motu-proprio. Prior finding: none.

- p1 PASS (`1725ccaa5ac8c4f4d186837112642887374e89e6e390b9f868dbb3cc39f8aac8`): Title, date 1847-10-01, Italian match. Protocol PIUS PAPA IX MOTU-PROPRIO, preamble, Disposizioni Preliminari, TITOLO 1 and numbered articles in two columns. No running head, folio (source folios 125-144 omitted) or digitizer line. Qualification: issuer line 'PIVS PP. IX.' matches the frozen metadata and identifies the pope.
- p2 PASS (`e1b09df48b9d71428d8030b34897cbbecbe9be482d962aa022940666bd2c5a10`): Two-column articles 12-31 with TITOLO heading; literal OCR marks only; no furniture.
- p3 PASS (`209fe094ebda522b949d73ec403e1e6cbab43ea6a323ed7e9bc2ee9efba51c9a`): Two-column articles 31-47 with TITOLO IIL heading; no furniture.
- p4 PASS (`b5bedbc05cab9a0613d8a77d493caf4081fd07c0e051712d06c802d0d8260a24`): Articles 47-58 with § subheadings in two columns; no running head or folio. Disclosed limitation: OCR-garbled section headings '61' and '6.1L.' (source §. I. / §. II., OCR LF5313 and LF5321) plus 'th,' and 'phe' stand as separate heading lines; the volume folios here are 125-144, so these are not folios; disclosed in the project source note.
- p5 PASS (`6c6005976a8736f4312b8d46020cd959cd0c78d396a2eb1f0bb67026c0364c77`): Articles 58-70 with § subheadings in two columns; literal OCR stray tokens ('49 I]', '18. Do', '9)') are body OCR noise, not folio numbers (folios 125-144). No furniture.
- p6 PASS (`5a36171b170b0a24045f751531cb37e73e93a1e69ff6c6ccde7ec4d689336b61`): Final articles, Disposizioni Transitorie, derogation clause, dating clause 'Dato dal nostro palazzo apostolico al Quirinale il di primo ottobre 1847 ...' and subscription PIVS PP. IX., then project notes. Natural source closing.

### `pius-ix-acta.volume-01.line-00002336` — PASS

*Quisque vestrum — allocutio in consistorio secreto 4 octobris 1847*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1847-10-04; Latin; consistorial-allocution. Prior finding: none.

- p1 PASS (`40731e9132a695df8c953798529258126a9451fb0050e4c800a99de953e89e7d`): Title (wraps with '1847' on second line), date 1847-10-04, Latin match. Caption HABITA IN CONSISTORIO..., VENERABILES FRATRES, body in two columns; notes (1)/(2) set as separate block at page break. No furniture. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`9688b2b33e475566cc02c24eb2f20fc68e3cd5af3c40cb293272b5864699ef28`): Body ends with 'Quid Vobis videtur?', creation of Valerga as Latin Patriarch and 'In nomine Patris ... Amen.' (literal OCR), then project notes split across columns. Note (1) S. Leo Ibidem set separately. Natural closing.

### `pius-ix-acta.pars-02-volume-01.line-00004832.part-03` — PASS

*Motu proprio sulla Consulta di Stato, 14 ottobre 1847*; issuer `PIVS PP. IX.`; 1847-10-14; Italian; motu-proprio. Prior finding: none.

- p1 PASS (`52339e762f45ed94659c17a1af0148930b6d2b4b3d839ddf2861c0dff37511e3`): Title, date 1847-10-14, Italian match. Protocol 'PIUS PP. IX. MOTY-PROPRIO Sulla' Consulta di Stato', preamble, TITOLO PRIMO/SECONDO and Art. 1-13 in two columns. No furniture. Qualification: issuer line 'PIVS PP. IX.' matches the frozen metadata and identifies the pope.
- p2 PASS (`a05ebccd40d962485d874ced2ebc82fa0e5702fef9a15476bce0c16157b37a00`): Art. 14-31 with TITOLO TERZO/QUARTO/QUINTO headings in two columns; no running head, folio or digitizer line.
- p3 PASS (`19e60107419b315c501cc1f51cd17f838e427c6f4154267dcc5c0d8c8fc0feaf`): Art. 31-54 with TITOLO SESTO in two columns; literal OCR noise only (e.g. 'cit', 'of'); no furniture.
- p4 PASS (`747bae369f39afbd44433de9b34bb8e9b600fa2cb892bb8c09dedc82239b3183`): Art. 54-76 with TITOLO SETTIMO/OTTAYO/NONO and start of derogation clause; no furniture.
- p5 PASS (`16606296c04aebfdf6df29432948f4891fce740448815becf549a534dffe71c5`): Derogation clause, dating clause 'Dato dal Nostro Palazzo Apostolico, al Quivinale il di 14 ottobre 1847, anno secondo ...' and subscription PIVS PP. IX., then project notes. Natural source closing.

### `pius-ix-acta.volume-01.line-00002530` — PASS

*Ubi primum — allocutio in consistorio secreto 17 decembris 1847*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1847-12-17; Latin; consistorial-allocution. Prior finding: none.

- p1 PASS (`00951525d8ce05df4d0a7e1986e1a4bb333f6d27e38d6a7df08b95e7420a4ee9`): Title, date 1847-12-17, Latin match. Caption (literal OCR 'BMABITÀ IN CONSISTORIO SECRETO DIE XVII DECEMBRIS ...'), VENERABILES FRATRES, two-column body; no furniture. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`cc97d17bdc82e5073ed5c2429b3a7183742d880531adf4d1da9c9ef447d903d6`): Two-column body; note (1) S. Iren. contra haereses set as separate block at page break. No running head, folio or digitizer line.
- p3 PASS (`8623231461fb8cda0dae1c06ae16ec2e2f08190a06903dc44388ab1446fa5a79`): Allocution's own closing ('... unum ovile et unus pastor.') followed by project notes in left column; allocutions of this series carry no dating clause. Natural source closing.

### `pius-ix-acta.volume-01.line-00002818.part-01` — CHANGES_REQUIRED

*In suprema Petri Apostoli Sede — litterae ad Orientales*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1848-01-06; Latin; apostolic-letter. Prior finding: none.

- p1 PASS (`c8aaa264736359e91d80925561c7fd60167485f53c328f98d3ebbce1507965db`): Title, date 1848-01-06, Latin match. Address '» AD ORIENTALES' and two-column body; no running head, folio or digitizer line. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`0570899007dc8fff53188a6517ba7c1a1ea1a729f78d648d3343f738e33ad3b9`): Two-column body; note (1) Extant Tom. IV. Bullarii set as separate block at the source page break. No furniture.
- p3 PASS (`7009c29d2dad505ec076ce69d984f903863dc4e311dc34ff0d26bcb2ed4a21e4`): Two-column body; notes (1)-(3), (1)-(2), (1)-(2) set as separate blocks at page breaks, not fused. No furniture.
- p4 CHANGES_REQUIRED (`c13a0a657830dc566488cfff1f92204cf2020a2da39f923731b6269900ed4d30`): Two-column body with notes (4) Tom. IF. Concilior. and (1)/(2) set as separate blocks; body ends with the Apostolic benediction 'impertimur.' Otherwise clean. BLOCKING: gathering-signature furniture left inside the body. Page 4, left column, lower half: a standalone line 'ri' (source OCR LF3261, printed at the foot of source page 89, bottom-centre at x1963-2008/y4341-4415 of 3289x5286, the same position as the signature '6' on leaf 79 sixteen leaves earlier) sits between the note block '(2) Ex Eusebio ... Lib. IV. Cap. 23.' and the body continuation 'mus, nihil Nobis antiquius esse', interrupting the sentence 'testamur et confirma-/mus'. The source note says gathering signatures are omitted, but LF3261 is not among this selection's omitted loci (it omits folio '90' at LF3264 only).
- p5 PASS (`825227809744effed54961184b0e2a8cfd9469895077312cb8308ef17b612951`): Natural source closing; not a notices-only page. Sparse final page: carries the genuine dating clause 'Datum Romae ... die VI Januarii Anno MDCCCXLVWHI. Pontificatus Nosti Anno Secundo. | B. od' (literal OCR, trailing stray marks) before project notes; qualification only.

### `pius-ix-acta.volume-01.line-00023322.part-01` — PASS

*Non dubitamus profecto — allocutio in consistorio secreto 17 ianuarii 1848*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1848-01-17; Latin; consistorial-allocution. Prior finding: none.

- p1 PASS (`bec19663079031c7b0d5b1eaa5a22b765f4e623627b6f4bd3b44a54d744abccd`): Title, date 1848-01-17, Latin match. Caption HABITA IN CONSISTORIO ..., body, 'Quid Vobis videtur ?', creation of Carolus Vizzardelli, in-pectore reservation and 'In Nomine Patis ... Ámen. ?' then project notes. Natural closing. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata. Non-blocking qualification: isolated non-lexical OCR mark '4$ 74v' on its own line between VENERABILES FRATRES and the body (source OCR LF23332; tiny 20-33px-high glyphs mid-page under the caption on source page 643, folio separately omitted at LF23359); not a folio, running head, signature or digitizer line; literal OCR noise.

### `pius-ix-acta.pars-02-volume-01.line-00008741.part-04` — PASS

*Statuto fondamentale pel governo temporale degli Stati di Santa Chiesa, 14 marzo 1848*; issuer `PIVS PP. IX.`; 1848-03-14; Italian; fundamental-statute. Prior finding: none.

- p1 PASS (`9ea7fa99044cbcdf6224196217d06c85f003d8a66c51e6490a8f500428af9fe6`): Title, date 1848-03-14, Italian match. Heading STATUTO FONDAMENTALE..., protocol PIVS PAPA: IX, preamble, DISPOSIZIONI GENERALI, Art. 1-6 in two columns; no furniture. Qualification: issuer line 'PIVS PP. IX.' matches the frozen metadata and identifies the pope.
- p2 PASS (`52470670ee4e02f1da0c6d49af0aeae60d55988eb11d108438119cf0f8eba101`): Art. 6-23 with section heading in two columns; literal OCR noise only; no running head, folio or digitizer line.
- p3 PASS (`2c6119ef91662b0993875fe762c54f9528af0eb8ab7feb3a7e811da28a5b1911`): Art. 23-42 with ATTRIBUZIONI DEI DUE CONSIGLI heading; no furniture. Non-blocking qualification: literal OCR scan noise at body line ends, Art. 31 left column: '~ sistlog', '« Gat' and 'di 918' (source OCR LF9421 tokens at x1288-1406 of a 1559px page, 4-13px high, mid-page on source page 230); not a folio (230), running head, signature or digitizer line; uncorrected OCR limitation.
- p4 PASS (`38570a261fbe64ee401a297348e2c39552dfbdc11bc201c3be4883cd8dca6217`): Art. 42-59 with DEL SACRO CONCISTORO, DE' MINISTRI, DEL TEMPO DELLA SEDE VACANTE headings; no furniture.
- p5 PASS (`7653359ef393e59ae8059f10e69a021a7f3f7427dd31bee7e02a4c01df7e44fa`): Art. 59-69, transitional provisions, final clause, dating clause 'Datum Romae apud S. Mariam Majorem die 14 Martii 1848 ...' and subscription PIVS PP. IX., then project notes. Natural closing.

### `pius-ix-acta.volume-01.line-00002818.part-02` — PASS

*Non semel — allocutio in consistorio secreto 29 aprilis 1848*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1848-04-29; Latin; consistorial-allocution. Prior finding: none.

- p1 PASS (`3c7d986cea843197ed97bbc23dcf8615477d4c9df665d45dd83d171750e9265c`): Title, date 1848-04-29, Latin match. Caption HABITA IN CONSISTORIO SECRETO DIE XXIX APRILIS ..., VENERABILES FRATRES, body in two columns; note (1) In Consistor. Allocut. set as separate block at page break. No furniture. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`62d2889ebefacba5edf98cd582b462883a9be0b4e3255d663252ab23d3efa093`): Two-column body; right column ends 'lace- rantur....' (source's own ellipsis, literal) before the closing paragraph. No running head, folio or digitizer line.
- p3 PASS (`9d85cad7f2f2ad17df12dff25b21c7fd51fb67b0f7e4c59fd4989213658e16be`): Closing paragraph 'Haec Vobis ... studia revocare dignetur.' then project notes; allocutions of this series carry no dating clause. Natural source closing.

### `pius-ix-acta.volume-01.line-00002818.part-03` — PASS

*In Sess. X Concilii Lateranensis V — ad praepositos censurae librorum in ditione pontificia*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1848-06-02; Latin; letter. Prior finding: none.

- p1 PASS (`31a51ab8e38146b0831647fb8c787eb5ab96f9f4afbc9b64b7e4a0b28011197e`): Title, date 1848-06-02, Latin match. Address VENERABILIBVS FRATRIBVS ..., salutation, body in two columns; note (4) In Const. Dominici gregis set as separate block at page break. No furniture. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`70e91f1a2bf8245f5a2a377ca8423c6343b06624ecb65882e7bca919771064ca`): Closing paragraph with Apostolic benediction and dating clause 'Datum Romae apud S. Mariam Majorem die II Junii Anno MDCCCXLVIII ...', then project notes. Natural source closing.

### `pius-ix-acta.pars-02-volume-01.line-00008741.part-05` — PASS

*Motu proprio sulla legge repressiva della stampa, 3 giugno 1848*; issuer `PIVS PP. IX.`; 1848-06-03; Italian; motu-proprio. Prior finding: none.

- p1 PASS (`8cb1eeeae42fc2dd558f9be05a664fa5ba743e8c79b187f0891621b1f81c8696`): Title, date 1848-06-03, Italian match. Protocol PIVS PP. 1X MOTV=PROPRIO SULLA LEGGE REPRESSIVA DELLA STAMPA, preamble, TITOLO I-II and articles 1-10 in two columns; no furniture. Qualification: issuer line 'PIVS PP. IX.' matches the frozen metadata and identifies the pope.
- p2 PASS (`473a13451f55a5a5ceafdb9d82d0741a5cbb8f34abd1cd1f3072c4b5e39e3f37`): Articles 11-25 with TITOLO III heading in two columns; no running head, folio or digitizer line.
- p3 PASS (`d06fd47663183ddb70af4b2658e52bdb379f3a8c0f0542d0fc91f8e50d7ed8c2`): Articles 26-32, TITOLO IV, dating clause 'Datum Romae apud S. Mariam Majorem die 3 Junii 1848 ...' and subscription PIVS PP. IX., then project notes continuing in right column. Natural closing.

### `pius-ix-acta.volume-01.line-00003708` — PASS

*Probe noscitis — allocutio in consistorio secreto 3 iulii 1848*; issuer `PII IX PONTIFICIS MAXIMI ACTA`; 1848-07-03; Latin; consistorial-allocution. Prior finding: none.

- p1 PASS (`5aaacab94b0c2607e3dfe64731dce50ec72169bd7b0c228e6c5000698d830aa5`): Title, date 1848-07-03, Latin match. Caption (literal OCR 'HABITA IN CONSISTORIO SECRETO DIE 13] 1VLU] ANNI NDCCCXLYUI.'), VENERABILES FRATRES, two-column body; no furniture. Non-blocking qualification: issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title, matches metadata.
- p2 PASS (`e84c24da56d8ceb3353a2b587ccae396166cd114db79f580c8eb78d9711c0f62`): Two-column body ends '... praesidium est collocatum.' then project notes; allocutions of this series carry no dating clause. Natural closing; no running head, folio or digitizer line.

## Limitations

- Literal, uncorrected, uncollated historical OCR; OCR corruption, odd spellings and stray marks are recorded as limitations, not repaired.
- Layout and boundary review of the rendered pages only; no word-level collation against the printed source.
- No historical authentication, publication, installation or deployment claim.
- A single short standalone OCR line was judged against the pinned layout XML geometry and the selection's omitted-loci list; isolated mid-page specks (`1` in Qui pluribus, `4$ 74v` in Non dubitamus) and scan-noise tokens were treated as literal OCR, not furniture.
- Canonical source admission and the upstream render are not independent findings of this lane. This report does not authorize installation.

