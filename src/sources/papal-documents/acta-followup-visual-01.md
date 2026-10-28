# Acta follow-up visual review 01: furniture-removal confirmation lane

**Result: PASS.** All 9 assigned Acta readers (43 pages) were opened one page at a time at full size. There are 0 blocking findings, and no page was reused. Each document had a prior CHANGES_REQUIRED finding for a journal running head or publisher line that interrupted body text. That defect is gone from every reader.

## Scope and method

Batch `acta-followup`, lane 01, schema `triptych-claude-visual-assignment/v1`. I opened every page PNG with the Read tool, one image per page at the rasters' original 1700x2200 size. I did not use contact sheets, re-rasterize, correct text or reconstruct dates. For each page I compared the title line, responsible issuer, date (or its omission when unknown) and Latin label with the frozen metadata. I also checked headings, two-column flow, gutters, margins, glyphs, closing and terminal apparatus, and looked for running heads, digitizer signatures, fused marginal summaries and raw placeholders. A mechanical `pdftotext` of each PDF was used only to search for leftover furniture strings. For the prior-finding loci and the anomalies I noted, I compared those lines with the canonical source text named in the frozen manifest.

## Evidence verification

Before and after inspection, I hashed every assigned PDF, the receipt, the frozen manifest, the raster-run record and every page PNG. All 55 digests matched the assignment pins on both passes.

| Evidence | Path | SHA-256 | Verification |
| --- | --- | --- | --- |
| Render receipt | `.scratch/typeset_pipeline/claude/acta-followup-0001/receipt.json` | `fd74d4c738f6435617eb0f128e444e94f5880978ee75d059d9944a4535dd082f` | Before and after |
| Frozen manifest | `.scratch/typeset_pipeline/claude/acta-followup-0001/frozen-manifest.json` | `6bd9958ce888adea5e16d1ef856b3e3cd326c3dc6ae0518f8700495509b8cc50` | Before and after |
| Raster run | `.scratch/claude-review/rasters-acta-followup-0001/review-run.json` | `ee22b538a102b31506c591e3c8a8fc10f494f404c7fb4ac453851e4dd72ea22a` | Before and after |
| Lane assignment | `.scratch/claude-review/acta-followup/lane-01/assignment.json` | `478216dee246878b46d1c245786c0eee6b9aafb3a0a80b38d43874e0d22ec50b` | Scope binding |
| Observation ledger | `.scratch/claude-review/acta-followup/lane-01/observations.jsonl` | `a44f7c3232b6970a1cbd3da2c92352f4b5b25a449a6962f7dbeaaaea09f0000f` | 43 unique page observations |
| Before verification | `.scratch/claude-review/acta-followup/lane-01/verification-before.json` | `61bd27947c97aa2edbf6b215d06e67fb66c7395f1ac06a6d0e0bf8c32102f26d` | all_match true |
| After verification | `.scratch/claude-review/acta-followup/lane-01/verification-after.json` | `f786106ecfabc354c9135dc25efe87dfdf742aed70aac53a08c80728aa7112df` | all_match true; identical digests |

## PDF outcomes

| Source ID | Date metadata | Language | Pages | PDF SHA-256 | Prior defect | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| `acta.aas.018.aas-018-l06278` | 1926-04-30 | `la` | 9 | `63a3d5b93ddccd9e8c6fe78aebe66751c8b827e4273c717fc8bcc6bc357e76d5` | Absent | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 1929-12-31 | `la` | 15 | `183f490592ea3554696a27db4e3784f3e1fee320a887b62c9806e30726543dde` | Absent | PASS |
| `acta.aas.005.archive.aas.005.047` | Unresolved; omitted from title | `la` | 2 | `0c16237b275110aa1eda34bf77f81e5c5bdd8f79265e600b23dfbd18416c1bff` | Absent | PASS |
| `acta.aas.012.archive.aas.012.l021627` | Unresolved; omitted from title | `la` | 8 | `b7cb3c9aeed78417f705f01b4b4f1803a272320f9db3608adb2d576e604f5fc3` | Absent | PASS |
| `acta.aas.021.aas-021-l04078` | Unresolved; omitted from title | `la` | 1 | `5d67fa1d070b8ea81566eafdd31e98e01b96a056568351eb936c48f8d51300e8` | Absent | PASS |
| `acta.aas.021.aas-021-l22883` | Unresolved; omitted from title | `la` | 2 | `e3f6b8dc7a2db1bd279e0d44a09aab989a858e3613a4fe46d55e6a856e355b41` | Absent | PASS |
| `acta.aas.022.issues-01-12.aas-022-l04984` | Unresolved; omitted from title | `la` | 2 | `9a4fda7cb363c790aac928e6762775a3cd4917b13d05bb58cf60f1f571942667` | Absent | PASS |
| `acta.aas.022.issues-01-12.aas-022-l06420` | Unresolved; omitted from title | `la` | 1 | `81d49a711728e442cac692a7dda2e45247be62c81257df0ad828c699471f608d` | Absent | PASS |
| `acta.ass.029.ass-029-l20563` | Unresolved; omitted from title | `la` | 3 | `c7ae18f17ab811c4baee5c5abd644500b33e1f4d60a4b19b8bc41d5d9962c39d` | Absent | PASS |

## Per-document findings

### acta.aas.018.aas-018-l06278

Pius XI, encyclical, Latin. Prior finding: Prior PDF 8480684ef282 was CHANGES_REQUIRED (report src/sources/papal-documents/acta-replacement-visual-017.md, page 1): Aera.,vol.XVIII,n.5.-3-5-926.11 interrupts recentiorum/errorum.

Prior defect absent. Page 1 reads `recentiorum errorum fautoribus` continuously; the `Aera.,vol.XVIII,n.5.-3-5-926.11` running head no longer appears on any page. Source page-foot note groups are set as separate paragraphs at source page breaks. Page 9 carries the genuine closing (dating clause of 30 April 1926 and `PIUS PP. XI`).

### acta.aas.022.issues-01-12.aas-022-l01896

Pius XI, encyclical, Latin. Prior finding: Prior PDF ffedd6ceced7 was CHANGES_REQUIRED (report src/sources/papal-documents/acta-replacement-visual-011.md, page 8): Acte Apostolicae Sedis - Commentarium Officiale follows genuine ProvXXII15 citation before continued body; preserve citation and paragraph boundary.

Prior defect absent. On page 8, column 2 keeps the genuine citation `vel i Prov., XXII, 15.` and the paragraph break, then continues the body (`repudiatis maiorum praeceptorum ...`). No `Acta Apostolicae Sedis - Commentarium Officiale` line appears anywhere in the PDF. Page 15 carries the genuine closing (31 December 1929 dating clause, `PIUS PP. XI` and final notes).

### acta.aas.005.archive.aas.005.047

Pius X, motu-proprio, Latin. Prior finding: Prior PDF 12c5753d2131 was CHANGES_REQUIRED (report src/sources/papal-documents/acta-replacement-visual-017.md, page 1): ACTA,rol.V,n.16.—28-10-913.32 interrupts mystica Christi/Sponsa.

Prior defect absent. Page 1 reads `quod mystica Christi Sponsa, ad suam declarandam` continuously; no `ACTA, vol. V, n. 16` running head. Page 2 carries the genuine closing (dating clause and `PIUS PP. X.`).

### acta.aas.012.archive.aas.012.l021627

Benedict XV, bull, Latin. Prior finding: Prior PDF e3c9d62b9bb1 was CHANGES_REQUIRED (report src/sources/papal-documents/acta-replacement-visual-017.md, page 4): ACTA.vol.XII,n.12.—2-11-920.36 interrupts Puellae/visionibus.

Prior defect absent. Page 4, column 2 reads `praesertim de Puellae visionibus et revelationibus` continuously; no `ACTA. vol. XII, n. 12` running head. Two non-blocking notes. (1) Page 4, column 1: a paragraph opens `m Puellae usque ad finem processus`. Source physical line 21909 holds a lone `m` right after the excluded running head `Acta Benedicti PP. XV`, which is probably a garbled page numeral. It begins a paragraph and does not sit inside a sentence, so it is treated as literal unresolved OCR. (2) Page 8 opens with a lone `.`, which is the period of the letter-spaced `P O M P I L J .` wrapped from page 7. The cardinals' subscriptions, protonotaries and registration close the act on page 8.

### acta.aas.021.aas-021-l04078

Pius XI, apostolic-constitution, Latin. Prior finding: Prior PDF f0cb9513d6c7 was CHANGES_REQUIRED (report src/sources/papal-documents/acta-replacement-visual-017.md, page 1): ACTA. vol.XXI,n.3.-6-3-929 interrupts honorifico/concathedrali titulo.

Prior defect absent. The single page reads `ecclesia ipsa honorifico concathedrali titulo in posterum fruatur` continuously; no `ACTA. vol. XXI, n. 3` running head. The genuine closing (dating clause, subscriptions, Loco Plumbi, registration) is present.

### acta.aas.021.aas-021-l22883

Pius XI, apostolic-constitution, Latin. Prior finding: Prior PDF 66c035b3ebc7 was CHANGES_REQUIRED (report src/sources/papal-documents/acta-replacement-visual-017.md, page 1): ACTA, rol. XXI, n.13. —1-10-929.39 interrupts ado-/lescentibus.

Prior defect absent. Page 1 reads `cum teneris ado- leseentibus potissimum` with no running head between the word halves; the hyphen-space is the literal source hyphenation. Page 2 carries the genuine closing (15 August dating clause, subscriptions, registration).

### acta.aas.022.issues-01-12.aas-022-l04984

Pius XI, apostolic-constitution, Latin. Prior finding: Prior PDF 3e82f7dcac34 was CHANGES_REQUIRED (report src/sources/papal-documents/acta-replacement-visual-015.md, page 1): Agta,rol.XXII,n.3.—3-3-930.9 interrupts meri-/diem Vallar fluminis.

Prior defect absent. Page 1 reads `quae exstat ad meri- diem Vallar fluminis`; the `Agta, rol. XXII, n. 3` running head and the publisher line between those rows are gone. Page 2 carries the genuine closing. The stray `;` after `Si quis autem` is on the source line itself and is literal OCR, not a defect.

### acta.aas.022.issues-01-12.aas-022-l06420

Pius XI, motu-proprio, Latin. Prior finding: Prior PDF 5418fb7ccffa was CHANGES_REQUIRED (report src/sources/papal-documents/acta-replacement-visual-016.md, page 1): AeTA,vol.XXII,n.4.—7-4-930.11 interrupts com-/memoratae Commissionis; retain genuine opening ACTA genre heading.

Prior defect absent. The single page reads `rationesque cum com- memoratae Commissionis` continuously; no `AeTA, vol. XXII, n. 4` running head. The genuine opening `ACTA` genre heading is kept, as required. The genuine closing (dating clause and `PIUS PP. XI`) is present.

### acta.ass.029.ass-029-l20563

Leo XIII, apostolic-letter, Latin. Prior finding: Prior PDF 1144037ae5dd was CHANGES_REQUIRED (report src/sources/papal-documents/acta-replacement-visual-017.md, page 1): Ada,Tom.XXIX.rase.CCCXLV.33 interrupts assignata in/perpetuum scutatorum. Source owner must preserve the surrounding in/perpetuum words.

Prior defect absent. Page 1 reads `assignata in perpetuum scutatorum summa quadringentorum` continuously, so the surrounding in/perpetuum words are preserved; no `Acta, Tom. XXIX, Fasc. CCCXLV` running head. Page 3 carries the genuine closing. The colophon discloses the conflicting date and leaves it unknown; this is a limitation, not a defect.

## Page raster digests

| Source ID | Page | PNG SHA-256 | Status |
| --- | --- | --- | --- |
| `acta.aas.018.aas-018-l06278` | 1 | `1bf21c501f5c61374e8e32ef79cb2f3d3b52f90d99080bb46612c779a17063cb` | PASS |
| `acta.aas.018.aas-018-l06278` | 2 | `9384f63511d1a988ae223cf7029b91a7d91e0b9f09aabdb0c6037c0b1fec8ac1` | PASS |
| `acta.aas.018.aas-018-l06278` | 3 | `4bca5a5e33d7c13ceab98bd4f9d1446b7c95a589973705bc17f1ad0d14a43e2c` | PASS |
| `acta.aas.018.aas-018-l06278` | 4 | `6e62e958e06719e0adae69621c9c67f92fcb2a415ed03dc3d5921e6b55bc17ab` | PASS |
| `acta.aas.018.aas-018-l06278` | 5 | `d0a79c26ddd4bcc99e1f94a699841f9e7efd03bd257caa137cd83d8aa5288f7c` | PASS |
| `acta.aas.018.aas-018-l06278` | 6 | `2c498568d784612200e0b055fa0523b5f8ce3e7f1865741d7e141b38e69693f3` | PASS |
| `acta.aas.018.aas-018-l06278` | 7 | `3724a3384fafcc9393a95bb15a2c2179695e0653ac185cceb2f9141991c48c42` | PASS |
| `acta.aas.018.aas-018-l06278` | 8 | `d2922df728666d4eb436a2e5aa32f5a8bd28c2ae3e9183ea7fba1cc1ba266552` | PASS |
| `acta.aas.018.aas-018-l06278` | 9 | `407ad9dab2180f36243f5d838e1a6c893dc1cf3b7c9e1d3c26e9f2ce2b066f2d` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 1 | `63e801c5325e18beb9a3ab60ef82e2b2349f7ec4811c78fd2a68a07090da8942` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 2 | `6cb22a912b6acc69e3af83466ea247985ee406de7008a3126ef943d6efd870e1` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 3 | `811a9070bd153b64ebccb1ce5da072d4ce57218a5b55d6e55aa7b276253b3fcb` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 4 | `883c5c25d75bbbde3c16cc7dd6dce5fc71151b494e51c45bdd639912c2326ed1` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 5 | `e252f187d6639b4730912941850ec09db18c55b6da83d785382576df341e6ff1` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 6 | `b2a0b2c9c00f1d31d9d1ea62ab02f588c095c2fee7c80a60951e3ad7d8905f6a` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 7 | `7f89951cde4593ab67196c398989f77474ea2f8af98058ad89921b7ae39b0ecf` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 8 | `7b47c190de3693b4399926c5d44c720f12b0df313a204fcad3767e39db9716df` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 9 | `22e9c52682e57e34be124f31081b49ada124c18dd4fcc4c8936c9e3a8fa39fcc` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 10 | `88bdcc3fee56a833cf3216c7b232a3a6c43fc1a2867014a11366f18412395c48` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 11 | `59e8ad44f36ee4ba972dec68c7c888deb7bd6ce47b51964fe6f0d734d082ed01` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 12 | `d2e711a84016ad81ec968b9bd0ed7714bfe92600c8be506479fe5aba1d21838c` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 13 | `65e5bb1699c7e64f3e1b10315248969d826c7aa2e8fe28842675954f5a379b0f` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 14 | `ae232cc0874d9d981657a6eb757308038cd1ab06338eb1dbe13b2a9bdc4daa91` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l01896` | 15 | `5179e1f06f1262cddd95ef22e91fe94008dc6ad090a4466418bc6c0e56286ebf` | PASS |
| `acta.aas.005.archive.aas.005.047` | 1 | `6973d79c1f03035ae80b2a0edb7af6cb0c147d5cab79214f57ff83d2504dd5d9` | PASS |
| `acta.aas.005.archive.aas.005.047` | 2 | `294c851c1ae7862a24085d37fb446d981ab9e2ca789ab406ca45994ec9979a5d` | PASS |
| `acta.aas.012.archive.aas.012.l021627` | 1 | `ed6761c1225cf207792a4e292c1fdbc7ad347f0ebf212774428d8672e7d120df` | PASS |
| `acta.aas.012.archive.aas.012.l021627` | 2 | `cd96b455930d3b4dcedec42b5a0679ac63fde33c268f3cd4682521d608eb9e97` | PASS |
| `acta.aas.012.archive.aas.012.l021627` | 3 | `964593595a02b686efc0b6aa9a19a03e29dde881f715ae7ebe563ba5b56f2e5d` | PASS |
| `acta.aas.012.archive.aas.012.l021627` | 4 | `f79607ae0be30511c636b44137190430c3d65005d0599542f78502fabcbb02bb` | PASS |
| `acta.aas.012.archive.aas.012.l021627` | 5 | `d55ab78d1a5a099ec95ba9dbb430f7b3ed695ae21b3c1934bed5406d69ea3cc7` | PASS |
| `acta.aas.012.archive.aas.012.l021627` | 6 | `7feb95f1363c2264a826fe210f52f6151d84833f154af80dc3323eabc5772030` | PASS |
| `acta.aas.012.archive.aas.012.l021627` | 7 | `1b11a5c9be5869e2a7c5de45150f40a36f3bc6eda820d0d6a5e5f6a47f963f7d` | PASS |
| `acta.aas.012.archive.aas.012.l021627` | 8 | `a0fbb49ce34962fb0e0b71bc91d150484e1097c11b20c538046bb9c47e85ef30` | PASS |
| `acta.aas.021.aas-021-l04078` | 1 | `d17cbb8dd9859c21d9cea2513500f07a9c71623cbd917f37f6e4fb764d13548e` | PASS |
| `acta.aas.021.aas-021-l22883` | 1 | `c29c1597b57184fcec405644ddbb83f220d3633e9a523180940b84a5d71fec75` | PASS |
| `acta.aas.021.aas-021-l22883` | 2 | `2c995021bd8a907504dbd849b4c30ce4ffb915e4559b2e60c2b8259cc57816b3` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l04984` | 1 | `6e0aac3e523072f827d8936ff4b33c9cb5450791ae408ee0e1c62eae8652cf8f` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l04984` | 2 | `07f20d68299fab87084065c1dc8843021bf12a99b146ca3790528956bbf83306` | PASS |
| `acta.aas.022.issues-01-12.aas-022-l06420` | 1 | `3459ddb6bef190379d75236096987349c97be20f8f75027f56b47e862208d34a` | PASS |
| `acta.ass.029.ass-029-l20563` | 1 | `3a4f1676ae8e97330aabcc35bbe613cc6d945df4d513a7b757a78361ddaa1510` | PASS |
| `acta.ass.029.ass-029-l20563` | 2 | `73c09e6884d755f583b91195f8361ee7ecb63bf74be891009a3a266d739c0e47` | PASS |
| `acta.ass.029.ass-029-l20563` | 3 | `17764481275e1b91ea9b85bdb9ba4aa9e6de2b24f0e41e4c823705c5e91bbd06` | PASS |

## Limitations

- The text is uncorrected, uncollated historical OCR. Letter-spacing, odd spellings, stray sign glyphs (for example `$8`, `)$!` and `●`) and the literal leftovers noted above are limitations, not defects.
- This is a layout review only. No word-level collation, facsimile comparison, historical authentication or date reconstruction was performed. Conflicting dates disclosed in the colophon stay unresolved.
- This report does not authorize or claim installation, publication or deployment.
