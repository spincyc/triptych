# Pius IX Acta visual review — pius-0001 lane 04

CHANGES_REQUIRED: 20 assigned PDFs, 65 pages individually opened at full size; 19 PASS, 1 CHANGES_REQUIRED. All inspections are new; zero reused pages. Scope is exactly the assignment of batch `pius-0001`, lane 4 (newly admitted Pius IX Acta readers, volumes I and II).

## Scope and method

Each assigned page PNG (produced by the repository `pdf-review` tool; not re-rasterized) was opened individually with the Read tool at full size; no contact sheet or thumbnail was used. Title, responsible issuer, date and language line were compared with the frozen metadata; headings, two-column flow, gutters, margins, glyphs, natural closing, historical notes, and terminal source/rights apparatus were inspected. Where a page showed a stray line, the corresponding raw OCR line, the segment's `physical_line_ranges` and the volume line-map were consulted read-only to decide whether it was page furniture.

No visible clipping, overlap, tofu/missing glyphs, collapsed tables, stranded headings, modern digitizer signature (e.g. "Digitized by Google"), journal running head, raw placeholder such as `None`, or fused marginal summary was found. Every final page carries genuine source closing (dating clause, subscriptions, or the act's own final sentence for allocutions/homilies without a dating clause) before the compact colophon.

## Evidence verification

All assigned PDFs, the receipt, the frozen manifest, the raster-run record and every page PNG were hashed before and after inspection (88 files); all matched their assignment pins both times and the before/after digests are identical.

| Evidence | Path | SHA-256 | Verification |
| --- | --- | --- | --- |
| receipt | `.scratch/typeset_pipeline/claude/pius-0001/receipt.json` | `720d0acae7c1f32315fd11d968d13eaa0510b72ea25906a6916054bd2ada2d73` | Before and after |
| manifest | `.scratch/typeset_pipeline/claude/pius-0001/frozen-manifest.json` | `583691e3d8941ca1c9a3a3f27f4cc57747afcfb3b3817776aad37a103df9d736` | Before and after |
| raster_run | `.scratch/claude-review/rasters-pius-0001/review-run.json` | `5718cc943c5d94fdf4a333529ce03aa4e55089d3d90a4801f03abb5e9597e7c6` | Before and after |
| Lane assignment | `.scratch/claude-review/pius-0001/lane-04/assignment.json` | `3792006e170deb3096b7a84f052cd3d43a1dc82d68697761db1ec06a7681e500` | Scope binding |
| Before verification | `verification-before.json` | `aa7198c44ab575a6014a30f10e075ec82ab4980d6d0c3824fbd51e85a9100576` | all_match = True |
| After verification | `verification-after.json` | `bcab0baeb08d7bde5b1e4e4a11ea564c4d37271478bf604f5c23dc7acdefdbae` | all_match = True; identical to before |
| Inspection ledger | `observations.jsonl` | `21a208fe6ee36a7ef4ea334981ad61502e1619b9f2cdf4c416e3b2853334d571` | 65 unique page observations |

## PDF outcomes

| Source ID | Date metadata | Language | Pages | Pages inspected | PDF SHA-256 | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| `pius-ix-acta.volume-01.line-00016170` | 1853-05-15 | `la` | 5 | 1, 2, 3, 4, 5 | `012cae387ae910170c7e3cfa743d56b65564684f4f72e16f4598f7059e5d3a47` | PASS |
| `pius-ix-acta.volume-01.line-00016746` | 1853-06-13 | `la` | 3 | 1, 2, 3 | `9d44408ac8298cd1d41b11494155d0e25f489d6a78e0271d53b6130fb8a9e48f` | CHANGES_REQUIRED |
| `pius-ix-acta.volume-01.line-00017084.part-01` | 1853-06-28 | `la` | 6 | 1, 2, 3, 4, 5, 6 | `1b9b7c7099bc716e57e0b9c684c7b8540eca47c1fa2ebc99e2eb40806cd219e3` | PASS |
| `pius-ix-acta.volume-01.line-00017084.part-02` | 1853-07-01 | `la` | 2 | 1, 2 | `1b4ad61534094e79b083d992dd0c2ec8170ca76063c847a088c2176069772c48` | PASS |
| `pius-ix-acta.volume-01.line-00017084.part-03` | 1853-07-05 | `la` | 2 | 1, 2 | `87a82a169cfc9b7b2a52307623963d3c7c76dfe38090c52981ffe5224e2204f4` | PASS |
| `pius-ix-acta.volume-01.line-00018312` | 1853-08-03 | `la` | 5 | 1, 2, 3, 4, 5 | `4d6e38f8a55a46b6f916ec503166e9ee70002da594b07822e7c3db5c93af8f7e` | PASS |
| `pius-ix-acta.volume-01.line-00018400.part-02` | 1853-09-01 | `la` | 3 | 1, 2, 3 | `f085baf9c6450cad95f5e69957a50f7049fad32ff62d3a48dd8e528766290d3f` | PASS |
| `pius-ix-acta.volume-01.line-00019284` | 1853-10-03 | `la` | 5 | 1, 2, 3, 4, 5 | `d8677e748f89e710ea5d30f508aae8de501fd816d41bb8281678c9cd536b4607` | PASS |
| `pius-ix-acta.volume-01.line-00020042.part-01` | 1853-12-19 | `la` | 3 | 1, 2, 3 | `1a70de99d358a6560bfa4d657e38c15c58634fbb7c2874fdae7d13bfbefb75f9` | PASS |
| `pius-ix-acta.volume-01.line-00023322.part-04` | 1854-01-09 | `la` | 2 | 1, 2 | `3d160c9ad563138edb06c4f4d9f0f445bceafffe53d95568c881887163965435` | PASS |
| `pius-ix-acta.volume-01.line-00020042.part-02` | 1854-02-02 | `la` | 6 | 1, 2, 3, 4, 5, 6 | `16b952d4be6445afba2c347fddedcfa3759f9d9c427d69dc0c65e8a8f7b02a7a` | PASS |
| `pius-ix-acta.volume-01.line-00020042.part-03` | 1854-03-20 | `la` | 2 | 1, 2 | `67fa5b8917e1009bfb04cd0e3b6b9f75e8c8351fc791544763f2294161bc5edf` | PASS |
| `pius-ix-acta.volume-01.line-00020042.part-04` | 1854-08-01 | `la` | 2 | 1, 2 | `ba7b0e562307613a78c7c3496582f698ea6e40b62a74390bfe2307a6c54c90f8` | PASS |
| `pius-ix-acta.volume-01.line-00021573` | 1854-12-01 | `la` | 1 | 1 | `19623651dc0fedd6b76a7977d7c471d891ab8dced587e16a27c6d84372b47197` | PASS |
| `pius-ix-acta.volume-01.line-00021682` | 1854-12-08 | `la` | 7 | 1, 2, 3, 4, 5, 6, 7 | `5944fe22d35fedb3a99e0ce89c81b5183a46e6f5774fa5c9fa481ecb9c883cb5` | PASS |
| `pius-ix-acta.volume-01.line-00022532` | 1854-12-09 | `la` | 4 | 1, 2, 3, 4 | `1ecef557bd6d01bd89ae3a1f8f462dce8ef6b9a66fba8eceabc307b0eb71ef8a` | PASS |
| `pius-ix-acta.volume-01.line-00022956` | 1854-12-10 | `la` | 2 | 1, 2 | `0f37f1dd94971351e9c946a5c3c4c6e7c0be4436b43dfdeea710aef14f9f2bc1` | PASS |
| `pius-ix-acta.volume-02.line-00000208.part-01` | 1855-01-02 | `la` | 1 | 1 | `7a0e57aaa215b144648d0910430db24b147aefbf3ee8d2e4a359c8b09b938059` | PASS |
| `pius-ix-acta.volume-02.line-00000208.part-02` | 1855-01-22 | `la` | 2 | 1, 2 | `c25107e872d79f917f2158a6dde98529ad6fe38c23bf6ae06d5a879d279c983e` | PASS |
| `pius-ix-acta.volume-02.line-00025929` | 1855-07-26 | `la` | 2 | 1, 2 | `27865011e817a7d9c0a120c2b6db6f46bf5fa03e2727aa51ab5a6e5d4d92516f` | PASS |

## Blocking finding

- `pius-ix-acta.volume-01.line-00016746` (Decet Romanum Pontificem, 1853-06-13), page 3, left column, paragraph 15 (Nonobstantibus clause): the standalone line `omo A nm` is set between `...specifica et individua mentio , seu` and `quaeyis alia expressio ad id servanda foret`, interrupting the sentence. It is raw OCR line 17041, in the page-foot zone of source page 471 immediately before the excluded folio line 17047 (`412`, i.e. 472) and the line-map page start 17047; it is not body text or a historical note (likely a damaged signature/scan mark). Under the standing ruling, page furniture left inside the body of these boundary-reviewed series is BLOCKING. Remedy: exclude line 17041 from the selection (e.g. end the range at 17040) and rerender.

## Per-document findings


### `pius-ix-acta.volume-01.line-00016170` — Totius Dominici gregis — confirmatio conventionis cum republica Costaricensi

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). Qualification: p.3 right column, Art. 17 ends with literal OCR token '54' (raw OCR line 16521, mid-page; the excluded folio is line 16509 '458'); recorded as literal OCR, not identified furniture. Dating-clause month OCR-garbled (disclosed in source review). prior_finding: none.

- p.1: Title, issuer PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1853-05-15, Latin match metadata; two columns clean; address, proem and convention heading; paragraph split at source page break mid-word (non-mini-/mum) is plain continuation without furniture.
- p.2: Art. 1-10 continue in two clean columns; literal OCR noise only; no running head, folio or digitizer line.
- p.3: Art. 10-22; right col Art. 17 ends with literal OCR token '54' (raw OCR line 16521, mid-page, not the excluded folio 458 at line 16509) - recorded as literal OCR token, not identified furniture; no clipping.
- p.4: Art. 22-28, convention subscriptions (Actum Romae die 7 Octobris 1852, Antonelli, Lorenzana), confirmation and clauses; columns clean.
- p.5: Sanctio, Datum Romae dating clause (OCR-garbled month, disclosed), datary/secretary subscriptions, Visa, Loco Plumbi, then compact Source/rights colophon; genuine source closing on final page; ', 2 1' is OCR noise inside the subscription block.

### `pius-ix-acta.volume-01.line-00016746` — Decet Romanum Pontificem — suppressio collegii Xystini ad Scalas Sanctas

**CHANGES_REQUIRED.** Page 3, left column, paragraph 15 (Nonobstantibus): page-foot non-body line 'omo A nm' (raw OCR line 17041, foot of source p. 471, possibly a damaged signature/scan mark) stands as its own line inside the sentence '...mentio , seu / omo A nm / quaeyis alia expressio...'; page furniture interrupting a body sentence is blocking in this boundary-reviewed series. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1853-06-13, Latin match; address and numbered paragraphs in clean two columns; source paragraph numbering literal (OCR '9.', '1.').
- p.2: Paragraphs 9-13 continue cleanly; no furniture, clipping or overlap.
- p.3: Left column: standalone line 'omo A nm' set between '...individua mentio , seu' and 'quaeyis alia expressio' mid-sentence; raw OCR line 17041 lies in the page-foot zone of source page 471 immediately before folio line 17047 ('412' = 472) and is not body text or a historical note. Otherwise para 14-16, sanctio, Datum Romae Idibus Junii 1853 dating clause, subscriptions, Loco Plumbi and colophon are fine.

### `pius-ix-acta.volume-01.line-00017084.part-01` — Cum Romani Pontifices — institutio Seminarii Pii

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). Qualification: p.3 standalone OCR mark '21: à' between a paragraph end and the TITVLVS II heading (raw line 17406, mid-page, interrupts no sentence). prior_finding: none.

- p.1: Title Cum Romani Pontifices, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1853-06-28, Latin match; address and proem in clean two columns.
- p.2: Proem continues; TITVLVS I heading set as own block; stray OCR 'DE.' ends a paragraph inline (literal OCR); no furniture or clipping.
- p.3: Titles I-III; standalone '21: à' between paragraph end and TITVLVS II heading (raw line 17406, mid-page, not page-edge furniture, not interrupting a sentence) recorded as literal OCR noise; headings not stranded.
- p.4: Titles IV-VI with numbered exam items; columns, gutter and headings clean.
- p.5: Title VI end and Title VII De gradvvm; clean flow; no running head or folio.
- p.6: Clauses, sanctio, Datum Romae quarto Kalendas Julii 1853 dating clause, Pro-Datarius/Lambruschini subscriptions, Visa, Loco Plumbi, Cugnonius, then colophon; genuine source closing on final page.

### `pius-ix-acta.volume-01.line-00017084.part-02` — Rerum omnium — beatificatio Germanae Cousin

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title Rerum omnium, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1853-07-01, Latin match; AD FVTVRAM REI MEMORIAM and narrative in clean two columns.
- p.2: Narrative, grant and clauses; Datum Romae sub Annulo Piscatoris die Prima Julii 1853 dating clause; Lambruschini and Brancaleoni subscriptions; colophon; genuine source closing.

### `pius-ix-acta.volume-01.line-00017084.part-03` — Quae duo ad sacrum ministerium — beatificatio Andreae Bobola

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title Quae duo ad sacrum ministerium, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1853-07-05, Latin match; address and narrative in clean two columns; no furniture.
- p.2: Narrative and grant, clauses; Datum Romae apud Sanctam Mariam Majorem die Quinta Julii 1853 dating clause; Lambruschini/Brancaleoni subscriptions; colophon; genuine source closing.

### `pius-ix-acta.volume-01.line-00018312` — In celsissima Petri Sede — confirmatio conventionis cum republica Guatimalensi

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title In celsissima Petri Sede, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1853-08-03, Latin match; proem, CONVENTIO heading block and Art. 1-2 clean.
- p.2: Art. 2-8 (literal OCR numbering 'Art. À..', 'Art. 4' before 'Art. 3'); clean columns; no furniture.
- p.3: Art. 9-18; clean two-column flow; no running head, folio or digitizer line.
- p.4: Art. 19-29, Actum Romae 7 Oct 1852, plenipotentiary subscriptions with Loco Sigilli, confirmation begins; clean.
- p.5: Clauses, sanctio, Datum Romae apud S. Mariam Majorem Tertio Nonas Augusti 1853 dating clause, subscriptions, Loco Plumbi, Cugnonius; colophon; genuine source closing; page-break split 'fue-/t' carries no furniture.

### `pius-ix-acta.volume-01.line-00018400.part-02` — Senogalliae urbis — institutio gymnasii Senogalliensis

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title Senogalliae urbis, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1853-09-01, Latin match; proem and foundation clauses clean in two columns.
- p.2: Commission to the Society of Jesus, library grant; inline OCR noise ('. "CH') only; no furniture.
- p.3: Decernentes, Non obstantibus, sanctio, Datum Romae Kalendis Septembris 1853 dating clause, Pro-Datarius/Lambruschini, Visa, Loco Plumbi, Cugnonius; colophon; genuine source closing.

### `pius-ix-acta.volume-01.line-00019284` — Ad piam doctamque — ratio studiorum seminarii Romani

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). Qualification: dating-clause year numeral OCR-garbled; source year headings ('ANNO PRIMO' etc.) sometimes run into following lines by OCR joins. prior_finding: none.

- p.1: Title Ad piam doctamque, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1853-10-03, Latin match; proem; source curriculum headings (DE PHILOSOPHIAE CVRSV, ANNO PRIMO etc.) set as own lines; literal OCR noise ('2008') only.
- p.2: Legal faculties, Hebrew/Greek, professors; source year headings 'ANNO PRIMO'/'ANNO SECVNDO' run into a list paragraph by the OCR line joins (source headings, not furniture; non-blocking); columns clean.
- p.3: Academici, De annuis experimentis, De gradvvm collatione (heading run into following sentence, non-blocking), In Philosophia, In Sacra Theologia; clean.
- p.4: Gradus in legalibus, De bibliotheca, Ordinationes peculiares, De religionis officiis; clean two columns; no furniture.
- p.5: De anno scholastico, decree clauses, Non obstantibus, Datum Romae sub Annulo Piscatoris die III Octobris (year numeral OCR-garbled 'wpcccuut', disclosed limitation), A. CARD. LAMBRVSCHINI subscription; colophon; genuine source closing. A few one-line paragraphs at left-column top reflect OCR line breaks.

### `pius-ix-acta.volume-01.line-00020042.part-01` — In apostolicae Sedis fastigio — allocutio in consistorio secreto 19 decembris 1853

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title In apostolicae Sedis fastigio allocutio 19 decembris 1853, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1853-12-19, Latin match; source caption 'HABITA IN CONSISTORIO SECRETO DIE XIX DECEMBRIS MDCCCLII!' (literal OCR year) and VENERABILES FRATRES address; clean columns.
- p.2: Guatimala convention, Freiburg conflict, East Indies schism; clean two columns; no furniture.
- p.3: Haiti mission, Sardinia negotiations, closing exhortation 'securitatis portum attingat.' (allocution has no dating clause; caption carries date); inline OCR noise '^ ., 5... 2' at raw line 20331 is mid-page, not furniture; colophon after genuine body close.

### `pius-ix-acta.volume-01.line-00023322.part-04` — Antequam ad Nos pervenirent — ad Hermannum archiepiscopum Friburgensem

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title Antequam ad Nos pervenirent, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1854-01-09, Latin match; address VENERABILI FRATRI HERMANNO... and salutation set as own lines; body clean; right column ends 'quo-' with some unused space at foot before the source-page-break paragraph moves to p.2 (non-blocking layout qualification; no clipping).
- p.2: Sparse final page with genuine source closing: end of benediction and Datum Romae apud S. Petrum die 9 Januarii 1854 dating clause, then colophon; not project-notice-only.

### `pius-ix-acta.volume-01.line-00020042.part-02` — Neminem vestrum latet — ad Armenios catholicos provinciae Constantinopolitanae

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). Historical notes set as separate blocks at source page breaks (non-blocking per standing ruling). prior_finding: none.

- p.1: Title Neminem vestrum latet, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1854-02-02, Latin match; address and salutation blocks; historical note '(1) Lit. Apost. Pii VIII...' set as its own block at the source page break (non-blocking).
- p.2: Body continues cleanly in two columns; no notes, furniture or clipping.
- p.3: Notes '(1) Matth. 12 25. (2) Gal. 5 15.' and '(1) Petr. Epist. 1, cap. 5. v. 2, 3.' each set as separate blocks at source page breaks (the latter mid-word 'nsu-/jora'); permitted by ruling, non-blocking.
- p.4: Notes '(1) Conc. Trid. Sess. XITI...' and '(4) S. Gregor. Homil. IX in Evang.' as separate blocks at page breaks (non-blocking); body clean.
- p.5: Notes (1)-(4) (Literae ad Orientales, S. Ambros., Concilium Ephes., S. Irenaeus) set as a separate block at the page break; body clean.
- p.6: Closing exhortation and benediction, Datum Romae apud S. Petrum die 2 Februarii 1854 dating clause, then colophon; sparse final page with genuine source closing.

### `pius-ix-acta.volume-01.line-00020042.part-03` — Optime noscitis — ad archiepiscopos et episcopos Hiberniae

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). Qualification: dating clause literally reads 'die 20 Mai- 1li Agno 1954' (source review records the leaf image as 20 Martii 1854); not repaired. Historical notes set as separate blocks at source page breaks (non-blocking per standing ruling). prior_finding: none.

- p.1: Title Optime noscitis, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1854-03-20, Latin match; address and salutation; stray OCR line 'b' before incipit (literal OCR, not furniture); clean columns.
- p.2: Notes '(1) Hieronym. Epist. 16. (3) Concil. Trideat...' and '(1) I. Petri cap. 4, v. 11.' set as separate blocks at source page breaks (non-blocking); benediction, dating clause literally OCR-garbled 'die 20 Mai- 1li Agno 1954' (source-review records leaf image as 20 Martii 1854; limitation, not repaired); colophon; genuine source closing.

### `pius-ix-acta.volume-01.line-00020042.part-04` — Apostolicae Nostrae caritatis — de precibus et iubilaeo

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). Historical notes set as separate blocks at source page breaks (non-blocking per standing ruling). prior_finding: none.

- p.1: Title Apostolicae Nostrae caritatis, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1854-08-01, Latin match; OCR-damaged address caption and salutation as own lines; note '(1) S. Joan. Chrysost. Homil. 15...' set as separate block at the page break (non-blocking).
- p.2: Jubilee grant, exhortation, benediction; Datum Romae apud S. Petrum die 1 Augusti 1854 dating clause; colophon; genuine source closing.

### `pius-ix-acta.volume-01.line-00021573` — Inter graves multiplicesque angustias — allocutio in consistorio secreto 1 decembris 1854

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Single page: title Inter graves allocutio 1 decembris 1854, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1854-12-01, Latin match; OCR-damaged source caption, VENERABILES FRATRES, body, 'HABITIS OMNIBVS SVFFRAGIIS PONTIFEX HAEC ADIECIT' section heading and closing address, then colophon; genuine source content with closing on the page.

### `pius-ix-acta.volume-01.line-00021682` — Ineffabilis Deus — de dogmatica definitione Immaculatae Conceptionis

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). Qualification: p.2 right column standalone OCR token 'x' between 'edita in' and 'favorem sententiae' (raw line 21942, mid-page, not a folio/running head). Historical notes set as separate blocks at source page breaks (non-blocking per standing ruling). prior_finding: none.

- p.1: Title Ineffabilis Deus, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1854-12-08, Latin match; AD PERPETVAM REI MEMORIAM; clean two columns.
- p.2: Note '(1) Alexandgsr VII. Const. Sollicituado...' as separate block at the page break (non-blocking); quoted constitution; standalone OCR token 'x' between 'edita in' and 'favorem sententiae' (raw line 21942, mid-page, not a folio/running head; recorded as literal OCR noise, non-blocking).
- p.3: Quoted Alexander VII decree, Fathers' testimony; clean columns, no furniture.
- p.4: Patristic types and titles; clean two-column flow.
- p.5: Effata, liturgy, petitions, Congregation; clean.
- p.6: Consistory, definition formula, anathema, exhortation; clean.
- p.7: Promulgation, sanctio, Datum Romae VI Idus Decembris MDCCCLIV dating clause (no subscriptions follow in the source OCR before the next act's folio and caption), colophon; genuine source closing.

### `pius-ix-acta.volume-01.line-00022532` — Singulari quadam — allocutio in consistorio secreto 9 decembris 1854

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title Singulari quadam allocutio 9 decembris 1854, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1854-12-09, Latin match; source caption and VENEBABILES FRATRES address; clean columns.
- p.2: Rationalism and salvation passages; clean two-column flow; no furniture.
- p.3: Clergy, seminaries, Immaculate Conception; trailing OCR mark '| ij' at paragraph end (literal OCR, not furniture); clean.
- p.4: Closing benediction ending 'per omnem .83e—/tersitatem. |' (OCR-damaged 'aeternitatem'; allocution has no dating clause), then colophon; sparse final page with genuine source closing.

### `pius-ix-acta.volume-01.line-00022956` — Quanta animi iucunditate — homilia in consecratione basilicae Ostiensis

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title Quanta animi iucunditate homilia, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1854-12-10, Latin match; source caption HABITA DIE X. DECEMBRIS MDCCCLIV and address; inline OCR noise ('HORE i EE MM', 'im') at paragraph ends, not furniture; clean columns.
- p.2: Closing period ending 'aeternae vitae efficiantur heredes.' (homily has no dating clause), then colophon; sparse final page with genuine source closing.

### `pius-ix-acta.volume-02.line-00000208.part-01` — Fidelis domus Domini — de indulgentiarum concessione Secretariae Brevium reservata

**PASS.** No blocking finding. Issuer line PIUS PAPA IX. is the act's own protocol and matches metadata. prior_finding: none.

- p.1: Single page: title Fidelis domus Domini, issuer PIUS PAPA IX. (matches metadata; protocol line in source), 1855-01-02, Latin; motu proprio body; literal OCR line-break sign '¬' renders as a visible glyph (no tofu); Datum Romae sub annulo Piscatoris die 2 Ianuarii MDCCCLV dating clause; colophon names volume II 1858; genuine source closing.

### `pius-ix-acta.volume-02.line-00000208.part-02` — Probe memineritis — allocutio in consistorio secreto 22 ianuarii 1855

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title Probe memineritis allocutio 22 ianuarii 1855, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1855-01-22, Latin match; source caption lines and TBNERABILES FRATRES address; literal OCR '¬' line-break signs render visibly; clean two columns.
- p.2: Closing petition ending 'reducere velit.' (allocution, no dating clause), then colophon (volume II, 1858); sparse final page with genuine source closing.

### `pius-ix-acta.volume-02.line-00025929` — Cum saepe — allocutio in consistorio secreto 26 iulii 1855

**PASS.** No blocking finding. Issuer line 'PII IX PONTIFICIS MAXIMI ACTA' from volume title matches metadata (non-blocking attribution qualification). prior_finding: none.

- p.1: Title Cum saepe allocutio 26 iulii 1855, PII IX PONTIFICIS MAXIMI ACTA (volume-title attribution), 1855-07-26, Latin match; OCR-damaged caption and address; '●' glyph after 'edita' is a literal OCR character rendered (no tofu); clean columns.
- p.2: Closing prayer ending 'vehementer gloriantur.' (allocution, no dating clause), then colophon; genuine source closing.

## Page raster hashes

| Source ID | Page | PNG SHA-256 |
| --- | --- | --- |
| `pius-ix-acta.volume-01.line-00016170` | 1 | `463ad82e511db9bafcbecfdeea67d577e6dfd7598976ba9581e3ae88b6395177` |
| `pius-ix-acta.volume-01.line-00016170` | 2 | `62017f7d310f86cdb0191484c536690bd0a66dea2a0af17b2f127a5b285436f5` |
| `pius-ix-acta.volume-01.line-00016170` | 3 | `470ecfde38b6d3e49aa6b418b6782e18a6c9089f394005c5421985b9c418cef7` |
| `pius-ix-acta.volume-01.line-00016170` | 4 | `1a3eaadd4eb83a33010388a5dcb0c1d7c7b9a16a17923be21b7c2ad34bdf7abd` |
| `pius-ix-acta.volume-01.line-00016170` | 5 | `16cf0a8691c70b338bb90225e15b84b8b29aa2ea9d39fcb05100e247c7db60d2` |
| `pius-ix-acta.volume-01.line-00016746` | 1 | `efa4742a563e3b5d25034816c73ad37d8f4d9bd94b6367c45b2fa23ae4cfaa4b` |
| `pius-ix-acta.volume-01.line-00016746` | 2 | `57bf3801b8139214a52380932da4b6e8650271ec65c44f96d766a9ae96c13dbc` |
| `pius-ix-acta.volume-01.line-00016746` | 3 | `32f415799c700af72b49616fbdab8df75b9ffd03d30c8fb7a8a0d9882b1bfaaa` |
| `pius-ix-acta.volume-01.line-00017084.part-01` | 1 | `29915ae240b80a6840dbaf2e9ec70dd5e905c5df432795199ca67def91ff5744` |
| `pius-ix-acta.volume-01.line-00017084.part-01` | 2 | `756a9fc2ac29dfc06516101f7c242c1d813c6f82f3954a66233cdb33011feb14` |
| `pius-ix-acta.volume-01.line-00017084.part-01` | 3 | `041ae3dd1e3ba978386bce3e63cfcd430703ba756924cc93fff1bc7bb3c6dcf4` |
| `pius-ix-acta.volume-01.line-00017084.part-01` | 4 | `a69dde52955cf0b218bf107778e8e33a13ac0ad63caf1626fd5b341157fcc85e` |
| `pius-ix-acta.volume-01.line-00017084.part-01` | 5 | `0692f4f1857a9d9583fc1a775f0cc9d7abbbde09406262053bd9cb231ea2b630` |
| `pius-ix-acta.volume-01.line-00017084.part-01` | 6 | `e3cb585a4ab2944e52d257f0b4dbe008e3fb2d8d1d3e9c605806b2b8d91ce968` |
| `pius-ix-acta.volume-01.line-00017084.part-02` | 1 | `027719339229c9bcf492853daea8a9da01543654a7a51ffbef1b345a2a8066f1` |
| `pius-ix-acta.volume-01.line-00017084.part-02` | 2 | `42dae3739ae31caa076f18ba4a2e2152e75b22cdd57ee39a044af0801cba5675` |
| `pius-ix-acta.volume-01.line-00017084.part-03` | 1 | `d89f8f689df7d452d8f12441db330f3f48928bc80dd1dbb6a02e622f41e9a08b` |
| `pius-ix-acta.volume-01.line-00017084.part-03` | 2 | `49fbb9d2e2b7fe58cab1dd85a8d73435ee2382bbaf91a0304b219fca4bea635f` |
| `pius-ix-acta.volume-01.line-00018312` | 1 | `ab47e9460b385cb3aeee79f30e59c093afa8ab8f62f90cac0228ce04ebeabe03` |
| `pius-ix-acta.volume-01.line-00018312` | 2 | `933beff1a946a0af59012e1acf842cac80aff43cd295212dcdf93ef33943785d` |
| `pius-ix-acta.volume-01.line-00018312` | 3 | `fe4e95b874d7160c96180e17b7c9af2cebd74b8581056aab1f05f834fa082779` |
| `pius-ix-acta.volume-01.line-00018312` | 4 | `4d44da489b4f2dba1b021b054c86ed7fcb9b084d84f89a9ea48b9e9ef6bebe3c` |
| `pius-ix-acta.volume-01.line-00018312` | 5 | `c587612ff4a60122d110d5e0c9f4f95915ca9419c3bb6c85168edd6f5158964f` |
| `pius-ix-acta.volume-01.line-00018400.part-02` | 1 | `b8c3b2e9e6d4abf001768007bb3c443ae95f6ed24cf579c1443c3725758beb02` |
| `pius-ix-acta.volume-01.line-00018400.part-02` | 2 | `d75127b65fcaea1757db78be73caa4d0490c35855b6595d1b2924ecfd05a8236` |
| `pius-ix-acta.volume-01.line-00018400.part-02` | 3 | `e8b52c569f0a82c7904f429ebbe63e89b55c7a3f12d93c819c7998fd520319d6` |
| `pius-ix-acta.volume-01.line-00019284` | 1 | `be6b8ce7d4882e017bb159ea53eaf0bd820004473ad73e5cc81f95ed63cae76d` |
| `pius-ix-acta.volume-01.line-00019284` | 2 | `a5580eda14a96ea47b55a0cc57dd4907fd45a034a75a98d27cfee3b61507962e` |
| `pius-ix-acta.volume-01.line-00019284` | 3 | `4bf253d8df93196c98e014de0f3429d40fc81f721a50473e157982b7d53c41f5` |
| `pius-ix-acta.volume-01.line-00019284` | 4 | `0733fe93b8221b070adb3bde1ead5a739fc58b0d85aa357e7551fd31c73f512e` |
| `pius-ix-acta.volume-01.line-00019284` | 5 | `8f04d79c5bb89e2a8916616901487f0c8c04065b853b68b6241ebb4a9c7c7107` |
| `pius-ix-acta.volume-01.line-00020042.part-01` | 1 | `5006e1f67afc5bbf46420d7cd8d7823b3e7e203ec4e40cdadf8468a4f0c86623` |
| `pius-ix-acta.volume-01.line-00020042.part-01` | 2 | `f393be38d3e513ea448a402e700166fcebf3eeb76a248adfd7ebce6ac0427268` |
| `pius-ix-acta.volume-01.line-00020042.part-01` | 3 | `56bd872fd86620b9c0f0de1040e9f2412e0688b3fd81a56a59c5193055faa5df` |
| `pius-ix-acta.volume-01.line-00023322.part-04` | 1 | `5524908a496f8e7993bdea0d0a361a989cd9b21445f2e19eb4b00e00e8b1ba04` |
| `pius-ix-acta.volume-01.line-00023322.part-04` | 2 | `a766d662513107fbe5bdaf8652aa6e1f8e936afb7b012672fbd418016e596d86` |
| `pius-ix-acta.volume-01.line-00020042.part-02` | 1 | `9ba95dcf269138f2439b30abde40445effea1e09c399a5a34cae7497b0ae4006` |
| `pius-ix-acta.volume-01.line-00020042.part-02` | 2 | `28e35a42ab0470c952072f9b2dac1696d213dedadf0b692eafc904546993e668` |
| `pius-ix-acta.volume-01.line-00020042.part-02` | 3 | `3a51e64e9477d45a25155f09f9dc6452ca3eb5cfa7be91e244eebeecc4aa66a4` |
| `pius-ix-acta.volume-01.line-00020042.part-02` | 4 | `542c18b735fda9cde61eee56e79ad9fcecfef3b6714b2a6982130eec8aa9245c` |
| `pius-ix-acta.volume-01.line-00020042.part-02` | 5 | `696013824cf473035b0c1fed88ca998404286002c25b7e891118d0810a49dd57` |
| `pius-ix-acta.volume-01.line-00020042.part-02` | 6 | `044df87537740f385d0c39df39f0171b15a8a6933458f59802016ae164d7a263` |
| `pius-ix-acta.volume-01.line-00020042.part-03` | 1 | `6ba8adbe929348a0420b266418ec2ac502d6b68296bd1938e2fa305a3327a433` |
| `pius-ix-acta.volume-01.line-00020042.part-03` | 2 | `97b0317e79a690319653a24a4152b4611d3f25fe3c095e2fd0e08c055dec8ab8` |
| `pius-ix-acta.volume-01.line-00020042.part-04` | 1 | `0492cda63583b2bd840ddfd8334a936ff8052e00b1e8408d33e339fd3776cabc` |
| `pius-ix-acta.volume-01.line-00020042.part-04` | 2 | `c35c1027e97cce08285ddea641c78765338cdcf3abb26d0eb915cd22282ccc36` |
| `pius-ix-acta.volume-01.line-00021573` | 1 | `019793f8ab318375fc4f1375620096192b1c640aaec6267020e79dfbc1434066` |
| `pius-ix-acta.volume-01.line-00021682` | 1 | `dc7dc23ddf8f66d72e26bb0326899519b4faf0533793e1cdcc8c90eb0cd0ddcf` |
| `pius-ix-acta.volume-01.line-00021682` | 2 | `6d3fdf85cedd969d85b574328b67ebcfd025d5e4ab44003fedb7952f2b7922c7` |
| `pius-ix-acta.volume-01.line-00021682` | 3 | `d9cb4aa8fff8b523f932767c7256ca6d0e47acad1fa1870e190638e3b1de7391` |
| `pius-ix-acta.volume-01.line-00021682` | 4 | `031f381285d2dcec88b75d409945e8bba14dadb811a66472ba9ed63e4ce8334f` |
| `pius-ix-acta.volume-01.line-00021682` | 5 | `33510f01cbd482e1e7aa2b564ada29d0dcd9c0702a923b69acb525d3cc5b9430` |
| `pius-ix-acta.volume-01.line-00021682` | 6 | `0d67bca1b3a11fd9e0faea74b8363dd11af1e2f8bed243cfd5646b30efae54a9` |
| `pius-ix-acta.volume-01.line-00021682` | 7 | `28040b59ff1d2b6d54f78eb2abf03fdee792c9fd9bbdca5ef68a6daa1b8876e0` |
| `pius-ix-acta.volume-01.line-00022532` | 1 | `d0a212c50cb12cdfbdd08395775ace13a3cd82ffd67bff3881d6144ebf9e3892` |
| `pius-ix-acta.volume-01.line-00022532` | 2 | `55b9bb4320782a011d49a6693fb467552658663068d8d502b07738b36423cd32` |
| `pius-ix-acta.volume-01.line-00022532` | 3 | `b9a9e5329886a49fe450643504dc36b4bf79af48b5f419c84f0ea14c9526f567` |
| `pius-ix-acta.volume-01.line-00022532` | 4 | `268c8bddef026dedfc5b8fa2c7e306d0a521b0b77a008b4040f06eb5739ede6d` |
| `pius-ix-acta.volume-01.line-00022956` | 1 | `a969d9b45544949030d17182525747b91398ab5b5d1b7492f1181d5c21eba27c` |
| `pius-ix-acta.volume-01.line-00022956` | 2 | `67c020030f45e5cf350d748c5863a0c6c6b33d9d55062b85d569ea0063ee42a6` |
| `pius-ix-acta.volume-02.line-00000208.part-01` | 1 | `b2313987f0576c0c3cfc122201ccefeea4070a31c33ae55085a6b41f80795524` |
| `pius-ix-acta.volume-02.line-00000208.part-02` | 1 | `bd3534f6e64162a4bd54dc94f122f8b449fe354473a0d27935bcb3984d7b2806` |
| `pius-ix-acta.volume-02.line-00000208.part-02` | 2 | `ec804aea6b491d10023b4f3a358e65777b5d4feefb971a05325a21aea47ef20f` |
| `pius-ix-acta.volume-02.line-00025929` | 1 | `2f16a5e37f6aeea8467ae7a6d6b67d15ad211fb723f58ff5c470d6f27c2666c6` |
| `pius-ix-acta.volume-02.line-00025929` | 2 | `2292e095125940c66ae39e4fa8039a696d4641fcf4320e6c033d1666d1dd7f9b` |

## Limitations

- Uncorrected, uncollated historical OCR; literal OCR corruption, odd spellings and stray OCR marks are limitations, not defects.
- Layout/visual review of the supplied rasters only; no word-level collation, historical authentication, publication, installation or deployment claim.
- Issuer attribution from the volume title is a recorded attribution context, accepted as a non-blocking qualification under the standing coordinator ruling.
- Dates were not inferred or repaired; OCR-garbled dating clauses are disclosed limitations.
- No prior findings were assigned to any document in this lane.
