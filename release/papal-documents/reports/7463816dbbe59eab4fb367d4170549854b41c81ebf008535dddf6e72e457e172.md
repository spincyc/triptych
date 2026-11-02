# Pius IX Acta visual review — pius-0001 lane 03

17 PASS, 2 CHANGES_REQUIRED: 19 assigned Pius IX Acta reader PDFs, 63 pages, each page PNG individually opened at full size; zero reused pages. Two documents keep a source folio or signature line inside the body, which is blocking in this boundary-reviewed series.

## Scope and method

Lane 03 of batch `pius-0001` (assignment schema `triptych-claude-visual-assignment/v1`). Every assigned page raster, produced by the repository `pdf-review` tool, was opened one image per page with the Read tool at full size (1700x2200 originals). No contact sheet, thumbnail or new raster pass was used. Per-page observations were appended to the lane ledger `observations.jsonl` as they were made. `pdftotext` output of the assigned PDFs was used only as a locating aid for candidate furniture lines; every finding was confirmed on the page image.

Each page was checked for title line, responsible issuer, date and language against the frozen metadata; headings, two-column flow, gutters, margins and glyphs; natural source closing; modern digitizer signatures; running heads, folio numbers and signatures in the body; marginal summaries or notes fused into body text; and raw placeholders. No document carried a `prior_finding`.

Standing rulings applied: Pius IX Acta readers whose issuer line is the volume title "PII IX PONTIFICIS MAXIMI ACTA" matching the metadata take it as a recorded attribution context (non-blocking qualification, recorded for 17 documents); OCR-damaged issuer spellings that match the metadata are qualifications; edition notes set as separate blocks at source page breaks are non-blocking; a folio number or running head left inside the body is blocking.

No modern digitizer signature, raw `None` placeholder, tofu glyph, clipping, column overlap, collapsed table, stranded heading, fused marginal summary or note interleaved into body lines was found. Every final page carries genuine source closing (dating clause, subscriptions or the natural end of an allocution) before the compact source/rights colophon.

## Evidence verification

All digests below were computed before inspection (`verification-before.json`) and again after (`verification-after.json`); every one matched its assignment pin both times (85 files: receipt, manifest, raster run, 19 PDFs, 63 PNGs). The two verification files are byte-identical.

| Evidence | Path | SHA-256 | Verification |
| --- | --- | --- | --- |
| receipt | `.scratch/typeset_pipeline/claude/pius-0001/receipt.json` | `720d0acae7c1f32315fd11d968d13eaa0510b72ea25906a6916054bd2ada2d73` | Before and after: match |
| manifest | `.scratch/typeset_pipeline/claude/pius-0001/frozen-manifest.json` | `583691e3d8941ca1c9a3a3f27f4cc57747afcfb3b3817776aad37a103df9d736` | Before and after: match |
| raster run | `.scratch/claude-review/rasters-pius-0001/review-run.json` | `5718cc943c5d94fdf4a333529ce03aa4e55089d3d90a4801f03abb5e9597e7c6` | Before and after: match |
| Lane assignment | `.scratch/claude-review/pius-0001/lane-03/assignment.json` | `55e339c5ff8e883c4ddf32784c5fac049138b61814172a324d1f5b539a125548` | Unchanged before and after |
| Verification before | `.scratch/claude-review/pius-0001/lane-03/verification-before.json` | `3a5295881dd9f6997768627f5a25948bd36d3e2d111d48881f93f3760a1b6934` | All 85 match |
| Verification after | `.scratch/claude-review/pius-0001/lane-03/verification-after.json` | `3a5295881dd9f6997768627f5a25948bd36d3e2d111d48881f93f3760a1b6934` | All 85 match; identical to before |
| Inspection ledger | `.scratch/claude-review/pius-0001/lane-03/observations.jsonl` | `eb38eee7a847c8d5a552a89b4e911a55e602ba15b7cea58df6fc29611364703e` | 63 unique page observations |

## PDF outcomes

| Source ID | Date | Language | Pages | Pages inspected | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| `pius-ix-acta.volume-01.line-00009581.part-04` | 1851-06-10 | `la` | 2 | 1, 2 | `ced166a9d43752f41aa70d63dab2fdc37ae9ca94288eb1f5105cf65933f7197b` | PASS |
| `pius-ix-acta.volume-01.line-00009581.part-05` | 1851-08-22 | `la` | 3 | 1, 2, 3 | `1837c55d03f4223e8778ecee3f520ab3cbc9d72d66d2b01e319e2126bb346e37` | PASS |
| `pius-ix-acta.volume-01.line-00010548` | 1851-09-05 | `la` | 3 | 1, 2, 3 | `6408cc855cffb04cf8bc1a3f551a760e5802ad66a4df9983c167584d37224b27` | PASS |
| `pius-ix-acta.volume-01.line-00010887` | 1851-09-05 | `la` | 11 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 | `db9b8d1f66d9f81a506856aff623acb22a16c91841c342d92ead11d4082febe7` | CHANGES_REQUIRED |
| `pius-ix-acta.volume-01.line-00012382` | 1851-11-21 | `la` | 2 | 1, 2 | `1da668af07d44d7c6b21cdaaa215b476f891fd7b2bb25e61309f6a82171b9c09` | PASS |
| `pius-ix-acta.volume-01.line-00012583.part-01` | 1851-11-21 | `la` | 2 | 1, 2 | `86a59e7df8e3b7df77f476d3fbfe53e2f35fadb7c21fb066f458436ccc9011a6` | PASS |
| `pius-ix-acta.volume-02.line-00030138.part-02` | 1852-03-08 | `la` | 6 | 1, 2, 3, 4, 5, 6 | `a5aa0da6ac2739ef429aed7392b53db304cdad58fabb86563b2219c877314cda` | PASS |
| `pius-ix-acta.volume-01.line-00012583.part-02` | 1852-03-25 | `la` | 3 | 1, 2, 3 | `9dbb0bdeeee1348b0283f41ddf758901d24db0eef8c3f0f2ab9a6c9cfde8ee03` | PASS |
| `pius-ix-acta.volume-01.line-00012583.part-03` | 1852-05-17 | `la` | 2 | 1, 2 | `5f7e9355611a67b19c2e342bf17c6991905de234977177c9cb2f2cbb0994aac4` | PASS |
| `pius-ix-acta.volume-01.line-00012583.part-04` | 1852-05-18 | `la` | 2 | 1, 2 | `fae0b311267a1f7912912d70f86f5d3a2f9a885484572193d279c7e9d3fe2d90` | PASS |
| `pius-ix-acta.volume-01.line-00013456` | 1852-08-26 | `la` | 3 | 1, 2, 3 | `9cca7d54f7738cd3df5e2d36e7b46e623b284aed758ac47bc18a9d23926dfbe4` | PASS |
| `pius-ix-acta.volume-02.line-00000208.part-05` | 1852-09-19 | `it` | 3 | 1, 2, 3 | `5609db3bc8bdce50f8e3c0bdea5012753e509b7e23b3790f9d17b6b383186234` | PASS |
| `pius-ix-acta.volume-01.line-00013832.part-01` | 1852-09-27 | `la` | 4 | 1, 2, 3, 4 | `18a75bafc640da885d943be94aaf3e488e966d30267cc59f48b9123fa6316f20` | PASS |
| `pius-ix-acta.volume-01.line-00013832.part-02` | 1852-10-01 | `la` | 3 | 1, 2, 3 | `c7e30ad0389241668f1938e7e413683f313159e70a0c3ce78887a1b59dc445ec` | PASS |
| `pius-ix-acta.volume-01.line-00013832.part-03` | 1852-10-01 | `la` | 2 | 1, 2 | `5afbc1a8e9d94c19b120809173da608dc6150fe206843f4e9b70e3aa789c1845` | PASS |
| `pius-ix-acta.volume-01.line-00013832.part-04` | 1853-02-09 | `la` | 2 | 1, 2 | `a6e8e3d40be7cb3ca18d39c2e42a485d1a74ec5caade2a007d7bcfd6af81c7d6` | PASS |
| `pius-ix-acta.volume-01.line-00014984` | 1853-03-04 | `la` | 3 | 1, 2, 3 | `bd4bd2311b9c1ecd646c3a393bf452ab7b5b7b806432f20958c3fd9d400b5baf` | PASS |
| `pius-ix-acta.volume-01.line-00015347.part-01` | 1853-03-07 | `la` | 4 | 1, 2, 3, 4 | `7741181e4050b28f7367d3295fabab729458dc92690b389cde36107c699e78e5` | CHANGES_REQUIRED |
| `pius-ix-acta.volume-01.line-00015347.part-02` | 1853-03-21 | `la` | 3 | 1, 2, 3 | `42beb9fda8d41cea25aac11d9df28167c81ee46e6539b665e914b3be995933d3` | PASS |

## Blocking findings

### `pius-ix-acta.volume-01.line-00010887` — Ad vicariam aeterni Pastoris — confirmatio conventionis cum Hispaniarum regina

- ' and 'nÍum in se recipiet' (splitting the word Gubernium), at roughly the lower middle of the left column after 'Hujusmiodi reditus nullam prorsus dedustioteui / patientur, neque ob sumptus Bullarum'. In this boundary-reviewed Pius IX series a folio number or signature left inside the body is BLOCKING. Rest of page (Arts. 31-35) is literal heavy OCR damage only.
- Page 8, left column, Art. 31 body: standalone source folio/signature number '22' left inside the body between 'quos Guber- 
- ' and 'nÍum in se recipiet' (mid-word); boundary-reviewed series furniture omission violated (BLOCKING).

### `pius-ix-acta.volume-01.line-00015347.part-01` — Cum placuerit — allocutio in consistorio secreto 7 martii 1853

-  
- ' marks are OCR noise.
- Page 3, right column, Morlot paragraph: standalone source folio/signature line '436 uat' left inside the body mid-sentence between '... ac pari' and 'in hanc Apostolieam Sedem'; boundary-reviewed series furniture omission violated (BLOCKING).

Both lines are print furniture (page number with signature or fragment) that the source note says is omitted; they need removal at the reading-selection/derivative level and a fresh render and visual review of the affected PDFs.

## Per-document observations

### `pius-ix-acta.volume-01.line-00009581.part-04` — PASS

Title "Multiplices inter — damnatio operis F. de Paula G. Vigil"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1851-06-10; Latin; type `apostolic-letter`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title, volume-title issuer (PII IX PONTIFICIS MAXIMI ACTA, recorded attribution context), 1851-06-10 and Latin match metadata; AD PERPETVAM REI MEMORIAM heading; clean two-column flow, gutter and margins; literal OCR marks ($o$ &c, stray bars) only; no running head, folio, digitizer signature or fused summary.
- Page 2 (PASS): Body concludes in left column with dating clause (Datum Romae ... die X Junii Anno MDCCCLI ... Anno V) and subscription A. CARD. LAMBRVSCHINI, then compact source and rights colophon; sparse final page carries genuine source closing; no clipping or furniture.

### `pius-ix-acta.volume-01.line-00009581.part-05` — PASS

Title "Ad Apostolicae Sedis fastigium — damnatio operum I. N. Nuytz"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1851-08-22; Latin; type `apostolic-letter`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1851-08-22 and Latin match metadata; AD PERPETVAM REI MEMORIAN heading (OCR); two columns flow normally; inline scriptural citation (ad Gal. 1) and Sess. 24 citation are source wording; literal OCR damage only; no furniture, folio, digitizer signature or fused summary.
- Page 2 (PASS): Continuous two-column body with source citations (S. Bern. Ep. 190; S. Felix III dist. 83) inline as printed; dating clause begins at foot of right column; no clipping, overlap, running head or folio.
- Page 3 (PASS): Sparse final page: dating clause conclusion (Anno Sexto.) and subscription A. CARD. LAMBRVSCHINI are genuine source closing, followed by compact source/rights colophon.

### `pius-ix-acta.volume-01.line-00010548` — PASS

Title "Quibus luctuosissimis — allocutio in consistorio secreto 5 septembris 1851"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1851-09-05; Latin; type `consistorial-allocution`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title wraps cleanly over two lines; volume-title issuer (recorded attribution context), 1851-09-05 and Latin match; source caption HABITA IN CONSISTORIO SECRETO DIE V SEPTEMBRIS and VENERABILES FRATRES address present; two-column flow normal; source-page-break line restarts (e.g. irrr / tas.) are literal OCR, not furniture; no folio, running head or digitizer signature.
- Page 2 (PASS): Continuous two-column allocution body; literal OCR damage only (punctuation noise); no clipping, overlap, fused summary, folio or running head.
- Page 3 (PASS): Allocution concludes naturally in right column (... splendidioribus triumphis exornet et augeat.) followed by compact source/rights colophon; no subscription expected for an allocution; no furniture.

### `pius-ix-acta.volume-01.line-00010887` — CHANGES_REQUIRED

Title "Ad vicariam aeterni Pastoris — confirmatio conventionis cum Hispaniarum regina"; issuer line "PIVS EPISCOPVS SERVVS SERVORVM DEI"; 1851-09-05; Latin; type `bull`. Prior finding: none.

- Qualification: Issuer line PIVS EPISCOPVS SERVVS SERVORVM DEI is the bull protocol and matches frozen metadata (qualification).
- Page 1 (PASS): Title wraps over two lines; issuer line PIVS EPISCOPVS SERVVS SERVORVM DEI matches frozen metadata and is the bull's own protocol (identifies the pope; qualification); 1851-09-05 and Latin match; protocol and AD PERPETVAM REI MEMORIAM headings; clean two-column flow; no folio, running head or digitizer signature.
- Page 2 (PASS): Continuous bull narratio in two columns; literal OCR damage only; no clipping, overlap, fused summary or furniture.
- Page 3 (PASS): Convention heading block (CONVENTIO / INTER SANCTISSIMVM DOMINVM PIVM IX ... / IN NOMINE SANCTISSIMAE ET INDIVIDVAE TRINITATIS) set as separate lines; articles and diocese lists flow normally; OCR article numbers (Art. J, Art. 4, Art. 9) are literal OCR; no furniture.
- Page 4 (PASS): Convention articles 6-12 with diocese lists and numbered items 1-5 as separate lines; literal OCR garbling (e.g. forwya, Exewsado, stray bars) only; no table collapse, clipping, running head or folio.
- Page 5 (PASS): Articles 13-18 continue in two columns; mojibake-like OCR sequence (a-grave euro) renders as real glyphs, not tofu; literal OCR only; no furniture or fused notes.
- Page 6 (PASS): Articles 18-24 continue with numbered collegiate items; literal OCR damage only; no clipping, overlap, running head, folio or digitizer signature.
- Page 7 (PASS): Articles 24-31 in two columns with revenue list beginning; literal OCR damage only (e.g. &nem, swfÉcienti); no clipping, running head, folio or digitizer signature.
- Page 8 (CHANGES_REQUIRED): Left column: a standalone folio/signature line '22' sits inside the Art. 31 body between 'quos Guber- 
- Page 9 (PASS): Articles 35-40 continue; numbered fund items (1, 9, J, A as literal OCR) set as separate lines; literal OCR marks (^, stray bars) only; no folio, running head or fused notes found.
- Page 10 (PASS): Articles 40-46, convention dating clause (Datum Matriti die decimasexta Martii ...) and plenipotentiary subscriptions with Loco Sigilli, then papal ratification clause; inline Art. 43-45 run-ons and stray bars are literal OCR; no folio, running head or fused note.
- Page 11 (PASS): Bull concludes with derogation clauses, sanction (Nulli ergo ...), dating clause (Datum Romae ... Nonis Septembris ... Anno Sexto) and subscriptions (Pro-Datarius, A. CARD. LAMBRVSCHINIVS, Visa de Curia D. Bavri) as genuine source closing, followed by compact source/rights colophon.

### `pius-ix-acta.volume-01.line-00012382` — PASS

Title "Exultavit cor Nostrum — de fructibus iubilaei"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1851-11-21; Latin; type `encyclical`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Historical footnote set as its own block at a source page break (non-blocking).
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1851-11-21 and Latin match; address and salutation headings set separately; two-column flow normal; note marker (1) in body; '24que' at foot of left column is an OCR-damaged word fused within the token, not a standalone folio; no running head, digitizer signature or fused summary.
- Page 2 (PASS): Historical footnote '(1) Matth. 7, 8.' set as its own separate block at the source page break inside 'pe- / trem' (non-blocking per standing ruling); closing blessing and dating clause (Datum Romae ... die XXI Novembris ... Anno Sexto) followed by compact source/rights colophon.

### `pius-ix-acta.volume-01.line-00012583.part-01` — PASS

Title "Ex aliis Nostris — de facultatibus pro iubilaeo"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1851-11-21; Latin; type `encyclical`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1851-11-21 and Latin match; address/salutation headings separate; two-column flow normal; right column has severe literal OCR garbling (e.g. Apostolie36, 3baolveve, '8 jure', '2 pecesto') fused inside words/sentences as OCR, not standalone folio or running-head lines; no digitizer signature or fused summary.
- Page 2 (PASS): Body concludes with derogations, blessing and dating clause (Datum Romae ... die XXI Novembris anno MDCCCLI ... Anno Sexto) followed by compact source/rights colophon; no clipping or furniture.

### `pius-ix-acta.volume-02.line-00030138.part-02` — PASS

Title "Inter cetera — nova paroeciarum constitutio in civitate Senogalliensi"; issuer line "PIVS EPISCOPYS SERVTS SBBVORVM DEI"; 1852-03-08; Latin; type `bull`. Prior finding: none.

- Qualification: Issuer line PIVS EPISCOPYS SERVTS SBBVORVM DEI is OCR-damaged but matches frozen metadata and identifies the pope (qualification).
- Page 1 (PASS): Title wraps over two lines; issuer line PIVS EPISCOPYS SERVTS SBBVORVM DEI is OCR-damaged but matches frozen metadata and identifies the pope (qualification); 1852-03-08 and Latin match; protocol lines and AD PERPETVAM REI MEMORIAM separate; literal OCR not-sign hyphenation marks render as glyphs, not tofu; clean two-column flow; no furniture.
- Page 2 (PASS): Continuous bull body with parish boundary descriptions; inline OCR noise (e.g. 'erigi 1 volumus', 'quae 1 viergit') is fused OCR, not standalone folio lines; no clipping, running head or digitizer signature.
- Page 3 (PASS): Continuous body; literal OCR damage (asterisks, carets) only; no folio, running head, fused summary or overlap.
- Page 4 (PASS): Continuous parish-boundary and endowment provisions in two columns; literal OCR damage only; no folio, running head, fused summary or clipping.
- Page 5 (PASS): Continuous body through derogation clauses; literal OCR damage only; no furniture or overlap.
- Page 6 (PASS): Bull concludes with derogations, transumpt clause, sanction (Nulli ergo ...), dating clause (Datum Romae ... Anno Incarnationis Dominicae ... Quinquagesimo Primo, Octavo Idus Martii; Pontificatus Nostri Anno Sexto) and Loco Plumbi as genuine source closing; incarnation-style year is source wording, not a defect (no date inferred); compact source/rights colophon flows into right column.

### `pius-ix-acta.volume-01.line-00012583.part-02` — PASS

Title "Nemo certe ignorat — ad archiepiscopos et episcopos Hiberniae"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1852-03-25; Latin; type `encyclical`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Historical notes set as their own blocks at source page breaks (non-blocking).
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1852-03-25 and Latin match; address/salutation headings separate; historical notes '(1) Concik Lateranen. 1V, cap. 9.' (left column) and '(2) S. Gregor. M. in Ezechid. ...' (right column) each set as their own separate block at source page breaks (non-blocking per standing ruling); heavy literal OCR damage only; no running head, folio or digitizer signature.
- Page 2 (PASS): Continuous two-column body including quoted letter with literal guillemet line-markers as printed; no clipping, fused notes, running head or folio.
- Page 3 (PASS): Body concludes with blessing and dating clause (Datum Romae ... die XXV martii Anno MDCCCLII ... Anno Sexto) followed by compact source/rights colophon; genuine source closing on sparse final page.

### `pius-ix-acta.volume-01.line-00012583.part-03` — PASS

Title "Probe noscitis — ad archiepiscopos et episcopos Hispaniae"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1852-05-17; Latin; type `encyclical`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1852-05-17 and Latin match; address/salutation headings separate; clean two-column flow; 'statuta 3« sancita' is fused OCR damage, not a standalone folio; no running head, digitizer signature or fused summary.
- Page 2 (PASS): Body concludes with blessing and dating clause (Datum Romae ... die XVII Maii Anno MDCCCLII ... Anno Sexto) then compact source/rights colophon; no clipping or furniture.

### `pius-ix-acta.volume-01.line-00012583.part-04` — PASS

Title "Cum primis Ecclesiae temporibus — beatificatio Ioannis de Britto"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1852-05-18; Latin; type `apostolic-letter`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1852-05-18 and Latin match; AD PERPETVAM REI MEMORIAM heading (OCR-damaged); clean two-column flow; literal OCR damage only; no running head, folio, digitizer signature or fused summary.
- Page 2 (PASS): Body concludes with grant clauses, dating clause (Datum Romae ... die Decima Octava Maii ... Pontificatus Nostri anno Sexto) and subscription ':. 4. CARD. LAMBRVSCHINIVS' (OCR for A. CARD.) as genuine source closing, followed by compact source/rights colophon; no furniture.

### `pius-ix-acta.volume-01.line-00013456` — PASS

Title "Inter omnia — indultum aggregandi ecclesias almae domui Lauretanae"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1852-08-26; Latin; type `bull`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title wraps over two lines; volume-title issuer (recorded attribution context), 1852-08-26 and Latin match; AD PERPETVAM REI MEMORIAM heading; clean two-column flow; literal OCR damage only; no running head, folio, digitizer signature or fused summary.
- Page 2 (PASS): Continuous body with indulgence grants; literal OCR damage (stray colons, bars, $) only; no folio, running head, overlap or fused notes.
- Page 3 (PASS): Body concludes with sanction, dating clause (Datum Romae ... Anno Incarnationis ... quinquagesimo secundo, Septimo Kalendas Septembris; Pontificatus ... Anno Septimo) and chancery subscriptions (L. C., Abbreviator, Rescribendarius, Plumbator, Scriptor, Loco Plumbi) with OCR noise, as genuine source closing; compact source/rights colophon follows.

### `pius-ix-acta.volume-02.line-00000208.part-05` — PASS

Title "La lettera che V. M. Ci ha fatto tenere — a Vittorio Emanuele II sul matrimonio civile"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1852-09-19; Italian; type `letter`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Qualification: Italian letter closes with a one-line Latin dating formula (Datum Castri Gandulphi ...); recorded as qualification.
- Page 1 (PASS): Title wraps over two lines; volume-title issuer (recorded attribution context), 1852-09-19 and Italian match; letter begins directly (no address heading in source); two-column flow normal; short OCR-noisy line '; ; sapui «odservarne ...' is a source-line restart within the body, not furniture; no folio, running head or digitizer signature.
- Page 2 (PASS): Continuous Italian letter body; literal OCR damage (& for a/e, Ia for la, 8. Sede) only; no clipping, overlap, running head or folio.
- Page 3 (PASS): Letter concludes with blessing and Latin dating clause 'Datum Castri Gandulphi die 19 septembris 1852.' (one-line Latin chancery formula within an Italian letter; recorded as qualification, not a multilingual annex) followed by compact source/rights colophon; genuine source closing.

### `pius-ix-acta.volume-01.line-00013832.part-01` — PASS

Title "Acerbissimum vobiscum — allocutio in consistorio secreto 27 septembris 1852"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1852-09-27; Latin; type `consistorial-allocution`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title wraps over two lines; volume-title issuer (recorded attribution context), 1852-09-27 and Latin match; OCR-damaged source caption (MABITA IN LONSISTORIO ... MDCGCLII) and VENERABILES FRATRES address set separately; two-column flow normal; no running head, folio or digitizer signature.
- Page 2 (PASS): Continuous allocution body; OCR-garbled years ('18935') are fused literal OCR, not standalone furniture; no clipping, overlap or fused summary.
- Page 3 (PASS): Continuous body; literal OCR damage only; no folio, running head or fused notes.
- Page 4 (PASS): Allocution concludes naturally ('... et exormetur trismphis.') with literal OCR garble (SIUAMONIOHUBE); compact source/rights colophon follows in right column; no subscription expected for an allocution; no furniture.

### `pius-ix-acta.volume-01.line-00013832.part-02` — PASS

Title "Quod, iuxta effatum Salvatoris — beatificatio Ioannis Grande"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1852-10-01; Latin; type `apostolic-letter`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1852-10-01 and Latin match; AD PERPETVAM REI MEMORIAM heading; clean two-column flow; literal OCR damage only; no running head, folio, digitizer signature or fused summary.
- Page 2 (PASS): Continuous body; 'experimentp 931, quid ille' is an inline OCR misreading inside the sentence (context reads as a garbled word, not a separate folio line) and is recorded as literal OCR; no standalone folio or running head, clipping or overlap.
- Page 3 (PASS): Body concludes with transumpt clause, dating clause (Datum Romae ... sub Annulo Piscatoris die Prima Octobris ... Anno Septimo) and subscription A. CARD. LAMBRVSCHINI as genuine source closing, followed by compact source/rights colophon.

### `pius-ix-acta.volume-01.line-00013832.part-03` — PASS

Title "Ad excitandum in animis — beatificatio Pauli a Cruce"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1852-10-01; Latin; type `apostolic-letter`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1852-10-01 and Latin match; AD FVTVRAM REI MEMORIAM heading; clean two-column flow; literal OCR damage only; no running head, folio, digitizer signature or fused summary.
- Page 2 (PASS): Body concludes with dating clause (Datum Romae ... sub [Annulo] Piscatoris die Prima Octobris ... anno Septimo) and run-in subscription 'E. A. CARD. LAMBRVSGHINI' (OCR) as genuine source closing; compact source/rights colophon splits across columns without clipping; no furniture.

### `pius-ix-acta.volume-01.line-00013832.part-04` — PASS

Title "Quamvis peculiares facultates — de privilegiis protonotariorum apostolicorum"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1853-02-09; Latin; type `apostolic-letter`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Qualification: A lone stray OCR bar sits on its own line in the right column of page 1; literal OCR mark, not furniture (qualification).
- Page 1 (PASS): Title wraps over two lines; volume-title issuer (recorded attribution context), 1853-02-09 and Latin match; AD PERPETVAM REI MEMORIAM heading; clean two-column flow; right column has a lone stray OCR bar '
- Page 2 (PASS): Body concludes with derogations, dating clause (Datum Romae ... sub annulo Piscatoris die IX Februarii Anni MDCCCLIII ... Anno VII) and subscription A. CARD. LAMBRVSCHINI as genuine source closing, followed by compact source/rights colophon.

### `pius-ix-acta.volume-01.line-00014984` — PASS

Title "Ex qua die — restitutio hierarchiae episcopalis in Hollandia"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1853-03-04; Latin; type `apostolic-letter`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1853-03-04 and Latin match; AD PERPETVAM REI MEMORIAM heading; clean two-column flow; literal OCR damage only; no running head, folio, digitizer signature or fused summary.
- Page 2 (PASS): Continuous body establishing sees; OCR-damaged roman years (wpccccxxxx, wDccxxxxi) are literal OCR inside sentences, not furniture; no clipping, overlap, folio or running head.
- Page 3 (PASS): Body concludes with derogations, transumpt clause, dating clause (Datum Romae ... die quarta Martii An. MDCCCLIII ... Anno Septimo) and subscription A. CARD. LAMBRVYSCHINI (OCR) as genuine source closing, followed by compact source/rights colophon.

### `pius-ix-acta.volume-01.line-00015347.part-01` — CHANGES_REQUIRED

Title "Cum placuerit — allocutio in consistorio secreto 7 martii 1853"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1853-03-07; Latin; type `consistorial-allocution`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1853-03-07 and Latin match; OCR-damaged source caption (RABITA JN CONSISTORIO SECRETO DIE VI! MARTII ANNO MDCCCLIII) and VENERABILES FRATRES set separately; clean two-column flow; no running head, folio, digitizer signature or fused summary.
- Page 2 (PASS): Continuous allocution body (Holland hierarchy, Costa Rica convention); literal OCR damage only; no clipping, overlap, folio or running head.
- Page 3 (CHANGES_REQUIRED): Right column, Morlot paragraph: a standalone source folio/signature line '436 uat' is set as its own line inside the sentence between 'Turonen-813, qui insigni religionis et pietatis studio, ac pari' and 'in hanc Apostolieam Sedem fide et observantia spectatus'. In this boundary-reviewed Pius IX series a folio number or running head left inside the body is BLOCKING. Rest of page (cardinals' elogia) is literal OCR only; stray '
- Page 4 (PASS): Allocution concludes with cardinal-creation formula (Quid Vobis Videtur?; Auctoritate Omnipotentis Dei ... declaramus; name lists) and 'In Nomine Patris ... Amen.' as genuine source closing (OCR cross marks render as glyphs); compact source/rights colophon follows; no furniture.

### `pius-ix-acta.volume-01.line-00015347.part-02` — PASS

Title "Inter multiplices — ad cardinales et episcopos Galliae"; issuer line "PII IX PONTIFICIS MAXIMI ACTA"; 1853-03-21; Latin; type `encyclical`. Prior finding: none.

- Qualification: issuer taken from the Acta volume title (recorded attribution context), matching metadata.
- Historical notes set as their own blocks at source page breaks on pages 1-3, including inside sentences (non-blocking per standing ruling).
- Page 1 (PASS): Title, volume-title issuer (recorded attribution context), 1853-03-21 and Latin match; address and salutation headings separate; historical notes '(1) Epist. Il ad Timoth. ...' (left column) and '/ (1) S. Cyprian. Epist. 45 ... (2) Concil. Ephes. ... (3) S. Irenaeus ...' (right column) each set as their own separate blocks at source page breaks (non-blocking per standing ruling); no running head, folio or digitizer signature.
- Page 2 (PASS): Continuous body with heavy literal OCR garbling at top of left column; historical note '(4) S. August. ... (2) Lit. Synodic. ...' set as its own separate block at the source page break before 'quo paf est obsequio' (non-blocking); no folio, running head, clipping or fused notes.
- Page 3 (PASS): Body concludes with blessing; historical note '(1) S. Cyprian. de unit. Eccles.' set as its own separate block at a source page break inside the closing sentence (non-blocking); dating clause (Datum Romae ... die XXI Martii Anno MDCCCLIII ... Anno Septimo) as genuine source closing, followed by compact source/rights colophon.

## Page raster digests

| Source ID | Page | PNG SHA-256 |
| --- | --- | --- |
| `pius-ix-acta.volume-01.line-00009581.part-04` | 1 | `6b54505de3f53ce2821ef7bbd2f96c0a43ae3e076efccfdc4a0b4e343efd7287` |
| `pius-ix-acta.volume-01.line-00009581.part-04` | 2 | `c9a2157da79ba13ae6f779c19c658b215695f7500bfbc56b4379464856ed9ea8` |
| `pius-ix-acta.volume-01.line-00009581.part-05` | 1 | `a25b20064098c1aa4f50347a688bee5a14f8c4aa2ce16fdd89a1d80c04682a97` |
| `pius-ix-acta.volume-01.line-00009581.part-05` | 2 | `cf37feae4ee605aa7775b21699a7599ebef1fa49b2d17aec773deed1d2468d46` |
| `pius-ix-acta.volume-01.line-00009581.part-05` | 3 | `c057c156512358b186333afbb74874a910624572a933339cbd7d5fddbd6956b7` |
| `pius-ix-acta.volume-01.line-00010548` | 1 | `a069a579afc352bf704ba4be36c49fc5476d13d7fd31b2d2b4def30511dbbc9a` |
| `pius-ix-acta.volume-01.line-00010548` | 2 | `a62f36f304da92637354f26b4a75c277fe94501378d72dbb44148d313c358982` |
| `pius-ix-acta.volume-01.line-00010548` | 3 | `0d2df326e97a26f0e007d6e9aec57feb0daebd9253bade3bf956241eb6a0c7c3` |
| `pius-ix-acta.volume-01.line-00010887` | 1 | `ecc44a28f0ec4ad59e19f3d4784b813d63ed4c1c9ab4bf203e3202c6e0aaef4c` |
| `pius-ix-acta.volume-01.line-00010887` | 2 | `5e1c980095ff0b40b7573abf0551048a675e210047dd43ca5f7a28438f3105a9` |
| `pius-ix-acta.volume-01.line-00010887` | 3 | `dce49d1c65a3bd9ca16579d3950122c76320ea4b09b13c8f6da9d358cad5e014` |
| `pius-ix-acta.volume-01.line-00010887` | 4 | `bf0f1041b10c2683f4978feae885234e1ded4928a6cd9b96dc6caba8e17adfd4` |
| `pius-ix-acta.volume-01.line-00010887` | 5 | `184e7e612529c6b116fa0962d2bc8af3e372b8c0a9e34762ff6f06900937316d` |
| `pius-ix-acta.volume-01.line-00010887` | 6 | `a734b0fe5ed87c0de1d542bdabfbb534e2dc3df2c7556e190ffbfa1071a4d55d` |
| `pius-ix-acta.volume-01.line-00010887` | 7 | `d746eee2f8951f5de1594971d5a29ee682396236391d61ade4db4e734fda16fd` |
| `pius-ix-acta.volume-01.line-00010887` | 8 | `26ffc2b9f40706c46249d1450d3cdb230c8ce02dcc141755cd91b4c148309a0d` |
| `pius-ix-acta.volume-01.line-00010887` | 9 | `a3289a4b230680fb33e49daa6e2bdcf69352005d12415d7ddaf7c5f38ecfacc8` |
| `pius-ix-acta.volume-01.line-00010887` | 10 | `b6da024f692870143e28b1dc4d315d9893242d8c0d95888fc38abaee063b16ac` |
| `pius-ix-acta.volume-01.line-00010887` | 11 | `706283d2befd0c976577a35f06b49ca722700822fd316fad13d417b6a6757fde` |
| `pius-ix-acta.volume-01.line-00012382` | 1 | `5342302572cc67958eb452a1f036f0ea46c62c04557ddb62ce2f353de23b40dd` |
| `pius-ix-acta.volume-01.line-00012382` | 2 | `27475f6e5efd29a0fda4d75fded32e95314fa5b830cf4ce9e847061d6f381724` |
| `pius-ix-acta.volume-01.line-00012583.part-01` | 1 | `76b5e2b378646917f3088ed70377d1a1725fa772f060eaeb13bec1305507cf5b` |
| `pius-ix-acta.volume-01.line-00012583.part-01` | 2 | `bdc87ba54069ac520c17dc603fca54cdc22c89f8fd9d45bc44f752df649c45a0` |
| `pius-ix-acta.volume-02.line-00030138.part-02` | 1 | `b68913fbb1dea114e4faff63d96e25006d9f342136218d2eb14da54e5ecdd5da` |
| `pius-ix-acta.volume-02.line-00030138.part-02` | 2 | `38ead52e819b88558477604642222b4d905aa4e838767d32b916cdc8d6916cab` |
| `pius-ix-acta.volume-02.line-00030138.part-02` | 3 | `f777f3dd04b0e37ff1026ffad5863f68b14766204ab0364fdbc5e7641e20226d` |
| `pius-ix-acta.volume-02.line-00030138.part-02` | 4 | `9cb75cdd244042bbb079567b711684924debb641224b44c7aebeb7647c246235` |
| `pius-ix-acta.volume-02.line-00030138.part-02` | 5 | `273139e74ad5802efd0c362065c952989ffbaa64b05b74b4a5a780d8c752a83e` |
| `pius-ix-acta.volume-02.line-00030138.part-02` | 6 | `bba684ca256b6cecc99be6c7c61442f9c668ce20bcc321f2dbf0c1d2e056c7fc` |
| `pius-ix-acta.volume-01.line-00012583.part-02` | 1 | `d9378533905afa11f86aa2f7d50e7cade2b44b511abfa05f6364922f24eb1477` |
| `pius-ix-acta.volume-01.line-00012583.part-02` | 2 | `381bd45bf2588287f3d14c122567592229f6c516b006cb75f99a5c16e3cd1b25` |
| `pius-ix-acta.volume-01.line-00012583.part-02` | 3 | `daf99852a04777f18bee74ccf8a6ad873e7dfb92a617dd4fa9827c97ca1f223c` |
| `pius-ix-acta.volume-01.line-00012583.part-03` | 1 | `e99ae74b3714d50bceacc1bd0648fd1ee1250286b5efd477ed11f3620d2dbe37` |
| `pius-ix-acta.volume-01.line-00012583.part-03` | 2 | `8863ff428562b62e4f8686b48a13e3048bdbba2c36ba5d2c33ab3248abdda032` |
| `pius-ix-acta.volume-01.line-00012583.part-04` | 1 | `d9c323f54576aaf2a3bc69d0183e0c5a3515d883b1da5615ba637454f1c0aea4` |
| `pius-ix-acta.volume-01.line-00012583.part-04` | 2 | `8ca82c2b7d9c1d8da2b0327a756683b83c63e30a22497fc7e0893bdee06aca89` |
| `pius-ix-acta.volume-01.line-00013456` | 1 | `92b472e1de966e08fe42406529bc97841a49f6defb7237ae046a2918ce7c1254` |
| `pius-ix-acta.volume-01.line-00013456` | 2 | `0dac39771bda8f70b97b429da02355c69dbb580de220ab55f100b1dc3741c87e` |
| `pius-ix-acta.volume-01.line-00013456` | 3 | `04821f87f329ad1670deb048d54e74d2bd9f91e53147f2d1981785da615d1358` |
| `pius-ix-acta.volume-02.line-00000208.part-05` | 1 | `0ac67f694f68f64c76ffad8a6bb6d9c691dbf540f3089aaddacac3d43abb0836` |
| `pius-ix-acta.volume-02.line-00000208.part-05` | 2 | `d68add977de2044226af95057d9a76e1ae4f7def93333d659a34d5a9a5cb94d4` |
| `pius-ix-acta.volume-02.line-00000208.part-05` | 3 | `f188310e73ee79618aba6efe466c5a23e8aa66536d3e9c53c3af27407d85000b` |
| `pius-ix-acta.volume-01.line-00013832.part-01` | 1 | `2e801a510677f978b6dd83c4a6cd42b38cc3d071edc55b363c4d64ab615d5733` |
| `pius-ix-acta.volume-01.line-00013832.part-01` | 2 | `5294e3f113379cb3e36f872d793f60dbf6a476a37968f08ea350edfef665ff7b` |
| `pius-ix-acta.volume-01.line-00013832.part-01` | 3 | `6530fdf176c36a27ad418e63aa667e27d03184968146dd1bfd19e2c46229e340` |
| `pius-ix-acta.volume-01.line-00013832.part-01` | 4 | `ca790174b3a7d2e54d54eeb52e577e4eaa4d66973c2065380642edfefd406114` |
| `pius-ix-acta.volume-01.line-00013832.part-02` | 1 | `367f44c734789df8592e8758615ad5a48f13543b58871074e68f8e4856887ae2` |
| `pius-ix-acta.volume-01.line-00013832.part-02` | 2 | `9e98734b3b9cc48fd365f877aaf016ddfbb3a15e77bfeccfab2b07180f1b1a78` |
| `pius-ix-acta.volume-01.line-00013832.part-02` | 3 | `f8dbd96ff2adbb0ee296778aa1e598904821f00d35f013936cb35f0a1c3f066f` |
| `pius-ix-acta.volume-01.line-00013832.part-03` | 1 | `dc8f06abafdd158bcdf031b7c85743fd453e0291b26d0db5599af978d8f4ce8c` |
| `pius-ix-acta.volume-01.line-00013832.part-03` | 2 | `25f3d23dcd24a13d0d10116a41908c350abd07b0e5fb3786fad4a39b79efd830` |
| `pius-ix-acta.volume-01.line-00013832.part-04` | 1 | `17e3944a61caeb2135b4d80f624f71542ed9f64bfc311eb5a92ceb70761ab0d2` |
| `pius-ix-acta.volume-01.line-00013832.part-04` | 2 | `b1cb8c0757a8a54d6108a547f912805a52900faf06e577bd1cf1e4d490704813` |
| `pius-ix-acta.volume-01.line-00014984` | 1 | `b5dc9fe8ab7cb888ddf1eda1f2b91476cf4bed6f2af07804ff4a6f005d7bea02` |
| `pius-ix-acta.volume-01.line-00014984` | 2 | `a13791fd2d96a8c7b8408f8e81326b833a4981968de9ed965ba1a2a0bdf24a80` |
| `pius-ix-acta.volume-01.line-00014984` | 3 | `669a2b5b33c94c990a32890bfa80927d1c12d6909e719bededd771f9070bbf24` |
| `pius-ix-acta.volume-01.line-00015347.part-01` | 1 | `76c98858ff8064f2ebb144e1901a445479a9c54d4195086888987758465a6d62` |
| `pius-ix-acta.volume-01.line-00015347.part-01` | 2 | `ae8e699767199af6eae4b41e928f7a8beabe7bd7d6cbaa45e29d71d13a87249e` |
| `pius-ix-acta.volume-01.line-00015347.part-01` | 3 | `5df4f688de2b5a192972a30db6689b4881d803fea6bb620d50803e2b493c4556` |
| `pius-ix-acta.volume-01.line-00015347.part-01` | 4 | `0b3535b87147fc4d87cf140f7a121ed25ed168d1c8aa051785b1b9beaf4d6972` |
| `pius-ix-acta.volume-01.line-00015347.part-02` | 1 | `ad464069c081cd810227c336418a2b292d2c43cbf3ab02cde7434b70546ced87` |
| `pius-ix-acta.volume-01.line-00015347.part-02` | 2 | `d258b677715f82d9342368b02e772f2f52fb908c582796815bdb7018b0434307` |
| `pius-ix-acta.volume-01.line-00015347.part-02` | 3 | `c973a426f1b4662c9d70c2fff1dd63e2e329ff6d88a4ea599997784a5777d25a` |

## Limitations

- Literal, uncorrected, uncollated historical OCR; wording, spelling and OCR damage not judged or repaired.
- Layout review only; no word-level collation, historical authentication, publication or installation claim.
- The OCR text streams are reconstructions; rendered pages do not establish the glyphs or pagination of the 1854/1858 printing. Disclosed or OCR-damaged dates were not inferred or repaired.
- Upstream source admission, rendering and source-fidelity checks are not independent findings of this lane. This report does not authorize installation and does not claim installation, deployment, publication or historical authentication.
