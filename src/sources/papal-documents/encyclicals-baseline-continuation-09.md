# Independent baseline continuation review 09

Outcome: 4 PASS readers (16 pages); 4 CHANGES_REQUIRED readers (24 pages). Fresh inspection covers all 8 assigned PDFs and all 40 pages on existing contact sheets and at full page resolution. No earlier inspection is inherited.

Packet: `.scratch/encyclical-ready-package/baseline-review-packets/09.json` (SHA-256 `19c311aa72b68de3756f3447b1d4175316655fb50dc50b0f615f4b3c579b29cf`). Canonical report destination: `src/sources/papal-documents/encyclicals-baseline-continuation-09.md`.

All 161 hash checks passed: exact PDFs, receipts, source payloads, selected segment manifests where present, source-controller records and available tracked payloads, frozen input manifest, raster manifest, and every existing page/contact/thumbnail listed in the raster caches. PDF page counts match both packet and raster metadata. Each packet source row matches the frozen manifest, and every receipt row matches the pinned receipt. The common brief hash also matches. Restricted ancestor payloads with null paths were not reacquired; their controller records were hash checked.

Independently replayed the repository `pdf_body_fidelity` check against each exact selected source (physical LF ranges interpreted using LF, not formfeed as a line delimiter). All 8 checks pass with source beginning on p. 1 and ending on each PDF’s actual final page. `pdfinfo` reads each PDF and confirms its page count; `pdffonts` shows all used fonts embedded and subsetted. These mechanical successes do not override the visual failures below.

Receipt SHA-256: `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e` (all assigned documents). Frozen manifest SHA-256: `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`. Raster manifest SHA-256: `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`. Render revision: `2026-10-30T02:56:48Z`.

## Exact inspected set

| Document | Language | Pages viewed on contact sheet and full size | Status | PDF SHA-256 |
| --- | --- | --- | --- | --- |
| acta.aas.002.archive.aas.002.049 | it | 1–11 | CHANGES_REQUIRED | `01645bbcbbfc51aaa849c48a20fab8dda2dccb7ea0f569a434dd7b68b489a229` |
| acta.ass.036.ass-036-l017876 | la | 1–7 | CHANGES_REQUIRED | `5444ebec688b52a73920564e421a58df736fa53996bb7110212bd799129f1701` |
| papal.benedict-xv.hf-ben-xv-enc-05101920-principi-apostolorum-petro | la | 1–6 | PASS | `9a88d59b1838d39dee45fb0450bb2c2298deecb0657450791b37f1fbf2a984f0` |
| papal.leo-xiii.hf-l-xiii-enc-28121878-quod-apostolici-muneris | en | 1–5 | PASS | `d9f0de74ef61c615054de306049d79ed23b0c9b53b1724eb8b47dab18f5b457e` |
| pius-ix-acta.volume-03.line-00021313.part-07 | la | 1–4 | CHANGES_REQUIRED | `5a7665f29589ecc55df50e359e54925722def25a124c64648ecaf10670d1c7d0` |
| papal.leo-xiii.hf-l-xiii-enc-25051899-annum-sacrum | la | 1–3 | PASS | `85714b7ec2342dd473fab6bf20dbd6e0c447f54f9f6085d5b5fe5a3e98f2b0ad` |
| acta.ass.033.ass-033-l02448 | la | 1–2 | CHANGES_REQUIRED | `e408bf6445b3a35f8281afd367739082f9d65fce327c3555b42253cb5aaa896c` |
| papal.pius-x.hf-p-x-enc-10081906-gravissimo-officii-munere | la | 1–2 | PASS | `8cec78ee2cf0630d9cf6725bb2ca84bc32dd99b193df488649ad8f3db13042c5` |

Each document’s `contact-sheets/sheet-001.png` and every `pages/page-*.png` in its exact packet `raster_dir` were freshly opened. Full-size inspection therefore includes every first, final, crowded, sparse and note-bearing page, not just a sample. The 11-page reader uses zero-padded page names; the others use unpadded names.

## Findings and source endings

### 1. Editae saepe

`acta.aas.002.archive.aas.002.049` · it · 11 pages · CHANGES_REQUIRED.

PDF: `.scratch/encyclical-classic/readers-fixed/1910-05-26-acta-aas-002-archive-aas-002-049-a22eff63-it/1910-05-26-acta-aas-002-archive-aas-002-049-a22eff63-it.pdf`. Source SHA-256: `270bc227b469bacbef2b3fcab827d06d946aa2e657987593f82081e5c07bdaad`.

- **Blocking, pages 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11:** Pervasive OCR intra-word spacing, broken word divisions and intrusive symbols materially impair continuous Italian reading. For example, p. 1 repeatedly sets words as separated letters and splits 'P r o v v i d e' at the bottom left before 'n z a' at the top right. Similar damage continues through p. 11. Faithful reproduction does not make this a usable classic reading edition; hold until an explicitly registered source-grounded spacing/word correction or better witness is available.
- **Blocking, pages 10:** Historical note/body fusion in the left column: the source sentence ending 'sebbene d’indole mite e soave.' runs directly into '1 Conc. Prov. V, Pars II. 2 MATTH, XXV…' on the same composed paragraph. The retained body.tex places the note list before the paragraph's terminating \par (lines 1016–1027 in the reviewed generated body). Restore an explicit, evidence-bounded note block while preserving source wording/order.

Final p. 11 retains the conclusion, 26 May 1910 dating, PIO PP. X subscription and final Bulla Unigenitus historical note. No source ending loss, clipping or overlap found. Many historical notes are separate blocks; the confirmed fusion finding is specifically p. 10.

### 2. LITTERAE ENCYCLICAE SS.mi D. N. Pii PP. X Iubilaeum extraordinarium orbi catholico indicentis, occa- sione quinquagesimi anniversarii a dogmatica definitione Immaculatae B. M. V. Conceptionis.

`acta.ass.036.ass-036-l017876` · la · 7 pages · CHANGES_REQUIRED.

PDF: `.scratch/encyclical-classic/readers-fixed/undated-acta-ass-036-ass-036-l017876-c6f5dc0f-la/undated-acta-ass-036-ass-036-l017876-c6f5dc0f-la.pdf`. Source SHA-256: `2e2ac41b82e92ef6a68a6bd1d4c768933ebadf42a8c74f3103755ac13fd762cb`.

- **Blocking, pages 2, 4, 5, 7:** Historical notes run into source prose or subscription. On p. 2 right, 'Natus est vobis hodie' continues inline into '(1) Ioann… (2) Rom…' before 'Salvator' resumes below; on p. 4 left the word 'Deipa-' is followed inline by the Matthew/John note list; on p. 5 left 'Et in utero habens,' continues into '(1) Grad. Miss…'; p. 7 sets the historical references inline after PIUS PP. X. Generated body.tex confirms missing paragraph boundaries before these lists. Separate the historical note blocks using exact source evidence.

Sparse p. 7 genuinely carries PIUS PP. X and historical references, so sparseness alone is acceptable. The 1904 dating appears on p. 6; the selected record's unresolved title date is omitted. OCR hard-line hyphens and occasional damaged forms remain source limitations. No ending loss, clipping or overlap found.

### 3. Principi Apostolorum Petro

`papal.benedict-xv.hf-ben-xv-enc-05101920-principi-apostolorum-petro` · la · 6 pages · PASS.

PDF: `.scratch/encyclical-classic/readers-fixed/1920-10-05-papal-benedict-xv-hf-ben-xv-enc-05101920-principi-apostolorum-petro-8f85232c-la/1920-10-05-papal-benedict-xv-hf-ben-xv-enc-05101920-principi-apostolorum-petro-8f85232c-la.pdf`. Source SHA-256: `e860ebdbb47a620c42901bab00515e9d332af335037355f4c6cf2154a784ccbc`.

Page 6 retains the blessing, 5 October 1920 dating, BENEDICTUS PP. XV and all 44 individually addressable historical endnotes. Minor retained transcription defects (including 'ben edictionem' and a 461 numeral in note 21) do not prevent reading. Terminal source/rights apparatus is compact. No blocking layout defect found.

### 4. Socialism, Communism, Nihilism

`papal.leo-xiii.hf-l-xiii-enc-28121878-quod-apostolici-muneris` · en · 5 pages · PASS.

PDF: `.scratch/encyclical-classic/readers-fixed/1878-12-28-papal-leo-xiii-hf-l-xiii-enc-28121878-quod-apostolici-muneris-e71ca4ec-en/1878-12-28-papal-leo-xiii-hf-l-xiii-enc-28121878-quod-apostolici-muneris-e71ca4ec-en.pdf`. Source SHA-256: `fc16a357008f7f2e1b0f331dceecc6ae76138b370a19665208fb064677cf6573`.

Page 5 contains substantial concluding prose and blessing plus all 19 separate addressable notes. The selected historical translation ends there; no extra subscription or dating is invented. Its right-column terminal apparatus shares this source-bearing page. Occasional source OCR defects such as 'wdth' remain legible. No blocking layout defect found.

### 5. Quanto conficiamur moerore — ad cardinales et episcopos Italiae

`pius-ix-acta.volume-03.line-00021313.part-07` · la · 4 pages · CHANGES_REQUIRED.

PDF: `.scratch/encyclical-classic/readers-fixed/1863-08-10-pius-ix-acta-volume-03-line-00021313-part-07-f5779e0c-la/1863-08-10-pius-ix-acta-volume-03-line-00021313-part-07-f5779e0c-la.pdf`. Source SHA-256: `3a788e20d82b5eb754d99242edaf43006aa915d8ebdfd9e1a62e73a1804e19f8`.

- **Blocking, pages 1, 2, 3, 4:** The retained OCR is materially unreliable as readable Latin, beyond occasional disclosed spelling errors. The opening contains 'bd had 3L'; p. 1 right contains 'EY DXX iie XU es D ost Lupus' and other nonlinguistic debris; p. 2 has garbled date references and 'io gp d T RU n'; p. 3 includes 'Optime: autern :noseitis' amid pervasive substitutions/punctuation intrusions; p. 4 retains corrupt word forms throughout. A source-grounded corrected derivative or better witness is needed before reader acceptance. No silent emendation is implied.

Page 4 retains the blessing and complete 10 August 1863 dating and eighteenth pontificate-year passage, followed by compact apparatus. No ending loss, clipping or overlap found. References are generally separate blocks; the provisional p. 2 fusion lead was rejected after checking paragraph boundaries and is not a finding.

### 6. Annum Sacrum

`papal.leo-xiii.hf-l-xiii-enc-25051899-annum-sacrum` · la · 3 pages · PASS.

PDF: `.scratch/encyclical-classic/readers-fixed/1899-05-25-papal-leo-xiii-hf-l-xiii-enc-25051899-annum-sacrum-6c3608f3-la/1899-05-25-papal-leo-xiii-hf-l-xiii-enc-25051899-annum-sacrum-6c3608f3-la.pdf`. Source SHA-256: `aa488348d28fe96c791579d6efdff0f93b4c5b617af6564d4ad1a7a1d4c96234`.

Page 3 retains substantial concluding prose, blessing, 25 May 1899 dating and LEO PP. XIII before compact apparatus. Its empty right column does not create an apparatus-only final page. No clipping, overlap, note fusion or other blocking layout defect found.

### 7. Omnibus compertum

`acta.ass.033.ass-033-l02448` · la · 2 pages · CHANGES_REQUIRED.

PDF: `.scratch/encyclical-classic/readers-fixed/1900-07-21-acta-ass-033-ass-033-l02448-d412de05-la/1900-07-21-acta-ass-033-ass-033-l02448-d412de05-la.pdf`. Source SHA-256: `0bf4c816a025b28cf31636812e0a2bf93729edf32823a74844f33ea857d3af6f`.

- **Blocking, pages 1, 2:** Repeated intra-word spacing and broken source word groups materially interrupt the short reader's prose. Page 1 rubric breaks 'P a t r i a r' / 'c h a m', and the lower-right body breaks 'c o m m e n d a v i m u' / 's'; p. 2 includes split 'm a i o- r' / 'e m' and 'R o m a' / 'e'. This is less severe than Editae saepe, but reconstructing word groups recurs across both pages. Hold for an explicitly registered source-evidenced spacing repair; fidelity alone is insufficient.

The second page is genuinely source-bearing: blessing, XXI Iulii MDCCCC dating, pontificate XXIII and LEO PP. XIII all remain. No ending loss, clipping, overlap or note fusion found. Sparseness itself is acceptable.

### 8. Gravissimo Officii Munere

`papal.pius-x.hf-p-x-enc-10081906-gravissimo-officii-munere` · la · 2 pages · PASS.

PDF: `.scratch/encyclical-classic/readers-fixed/1906-08-10-papal-pius-x-hf-p-x-enc-10081906-gravissimo-officii-munere-22797b1b-la/1906-08-10-papal-pius-x-hf-p-x-enc-10081906-gravissimo-officii-munere-22797b1b-la.pdf`. Source SHA-256: `3b48f4cb53ddf955f00d23cbc9c14a65c798755251dca2edfaacd8499edd3bb9`.

Page 2 retains substantial body across both columns, blessing, 10 August MCMVI dating and PIUS PP. X before compact apparatus. No note fusion, clipping, overlap or blocking layout defect found. The recorded underfull heading warning has no material visual effect.

## Review limits and evidence

This is a fresh visual/usability and exact-input review of the packet bytes. It does not certify whole-source verbal or facsimile collation, translation accuracy, legal rights, original historical pagination, or the correctness of residual source OCR. The source records and their affirmative distribution states were inspected as pinned inputs; no new rights research was performed. No PDF was recompiled, rerastered, installed or edited. Existing source/receipt/raster files and shared caches were read only.

The geometry review found readable title/body separation, normal left-column then right-column flow, adequate margins and compact terminal apparatus; no clipping, overlap, missing glyph box, or apparatus-only final page was found. Punctuation and word errors explicitly identified above are source-stream usability failures, not claims of missing PDF glyphs.

Lane-local supporting files: `.scratch/encyclical-baseline-continuation-09/pin-verification.json`, `fidelity-font-verification.json`, `observations.json`, and per-document extracted text, selected-source, pdfinfo and pdffonts snapshots. The selected-source snapshots use exact LF range semantics; they are review aids, not new source derivatives.
