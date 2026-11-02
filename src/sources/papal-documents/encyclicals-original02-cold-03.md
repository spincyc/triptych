# Original02 cold visual review 03

Fresh review of packet `original02-cold-03`: **4 PASS; 2 CHANGES_REQUIRED**.
All **31/31 pages** were inspected individually in the six existing contact
sheets and then opened at the original full raster resolution. No previous
review coverage or acceptance was inherited. `reused_pages` and `reuse_proofs`
are empty for every document.

This report is intended for the exact canonical destination
`src/sources/papal-documents/encyclicals-original02-cold-03.md`. It concerns the
six original PDFs below, not any later repair or replacement.

## Reviewed bytes and coverage

| Document ID | Language | PDF SHA-256 | Pages viewed in contacts and full size | Status |
| --- | --- | --- | --- | --- |
| `papal.leo-xiii.hf-l-xiii-enc-04081879-aeterni-patris` | en | `94df7779351ec47c78f285e0369fb59acdba185f3feb7d464ce0ad4e0c91da6a` | 1–10 | PASS |
| `acta.ass.024.ass-024-010` | fr | `3703528ef99b8a590e1a8b956f6e104e62bdeaa5ef1c185534beeced805514da` | 1–7 | CHANGES_REQUIRED |
| `papal.leo-xiii.hf-l-xiii-enc-29061881-diuturnum` | la | `414d8c96f8120d4448ceb969e195ecc12e2e03ba663a1899f9499ea9a42c188c` | 1–6 | PASS |
| `papal.leo-xiii.hf-l-xiii-enc-25071898-caritatis-studium` | la | `9c62c30e23fb8a565f446e5ba36b6b5cc7330ec41ce3042a9936e873da012824` | 1–4 | PASS |
| `pius-ix-acta.volume-01.line-00020042.part-03` | la | `9565b8effb408f850e44cefbe522135998f4243af44975390d596e141138222a` | 1–3 | CHANGES_REQUIRED |
| `acta.aas.010.archive.aas.010.l019820` | la | `ba07f0b6999eeea1ac6becac59478e44960bdbe8b1c867d2b1465d61e0401bd8` | 1 | PASS |

The packet's `pdf_path` and `raster_dir` govern every row. Contact inspection
used each directory's `contact-sheets/sheet-001.png`; full-size inspection used
every file in its `pages/` directory. The English reader names pages
`page-01.png` through `page-10.png`; the other readers use unpadded numbers.
The rasters were opened with original image detail. No raster was regenerated.

## Identity and mechanical verification

The working branch was `feature/encyclicals`. The exact packet
`.scratch/encyclical-ready-package/original02-review-packets/03.json` has SHA-256
`4ab74bf4151af4ff841ef24470db2fbdbd52d42108f61dce9acdaa56de01d8d4`.
Its clarified common brief matches
`c2eb89fab157c4df4b19f3c670871f27730012a4eeb95f695b6fc656bc1bc7d7`.

All six PDFs match their packet digests and `pdfinfo` page counts. All six
receipt rows and frozen source rows equal the packet's exact embedded rows.
The common frozen receipt is
`.scratch/encyclical-classic/readers-fixed/receipt.json`, SHA-256
`3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e`.
The frozen input manifest is
`.scratch/encyclical-classic/readers-fixed/frozen-manifest.json`, SHA-256
`13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342`.
The render revision is `2026-10-30T02:56:48Z`.

| Document, in packet order | Controlling text SHA-256 |
| --- | --- |
| Aeterni Patris, English | `fc16a357008f7f2e1b0f331dceecc6ae76138b370a19665208fb064677cf6573` |
| ASS 24 French reader | `040fa780d381758f432e740ecfe4cee01143cc43aceb357677177ec4458a5215` |
| Diuturnum | `f8b51aa20600211649af746845c879a95548097cf2b2781f907493242f608789` |
| Caritatis Studium | `5446e438a3cfb3e603785e94f08fe4c1ea4f7c40ddc5bddc868bc2d86a54ee00` |
| Pius IX, Optime noscitis | `898bc939f063a4b1e2cc87b5bba06d51fccbf14ff329c4bf7c8261b60b595205` |
| AAS 10 peace-prayer act | `7f9a8862646fd073b6ceb69c66eee6fc5ba69f375dcd03a8b2c3828825eacf20` |

All available segment manifests, every packet-pinned source-controller record,
and every available controller payload match their declared hashes. The two
normalized Latin web transcriptions have no separate segment pin in the
packet; their artifact/controller pins were checked instead.

The shared raster manifest
`.scratch/encyclical-classic/visual-fixed/review-run.json` matches
`ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02`.
Each per-document cache binds the correct PDF hash and page count, and its
renderer fingerprint matches the run fingerprint
`cb6bc6758b165c50bba7f68d7b5e1df5cc66fa3e0aad97361992b67d97cea2ba`.
All 68 listed contact-sheet, full-page, and thumbnail files match their cache
digests. There were 123 successful hash comparisons in total, including the
common brief and repeated document-level receipt/manifest checks.

`pdfinfo`, `pdffonts`, and `pdftotext -raw -enc UTF-8` completed successfully
for all six PDFs. The PDFs are unencrypted Letter-size PDF 1.7 documents;
all reported fonts are embedded, subsetted Latin Modern fonts with Unicode
maps. Titles, author fields, language subjects, and modification timestamps
agree with the packet identities and render revision. Extracted text was used
to check reading sequence and identify source-ending loci, not as a substitute
for page inspection. The receipt's fidelity PASS results were checked as
pinned receipt data; the generator's complete fidelity algorithm was not rerun.

## Findings

### Aeterni Patris, English — PASS

Pages 1–10 were viewed in contacts and at full size. The compact identification
leads directly into the English source. The justified two-column pages retain
a clear gutter, consistent baselines, readable references, and ordinary
left-column-then-right-column progression. No clipping, overlap, materially
stretched heading, or disruptive heading split was found.

Page 9 retains the concluding blessing followed by the historical references.
Page 10 is very sparse but contains actual source notes [48]–[50] before the
compact source/rights apparatus. Those notes match source LF 293–297 and
generated body.tex 258–265. It is a source-bearing final page, not a page made
solely of project notices. This specific sparseness qualification accompanies
the PASS.

### ASS 24 French reader — CHANGES_REQUIRED

Pages 1–7 were viewed in contacts and at full size. The ragged-right French
columns, long identification, opening, closing blessing, dated subscription,
and final source/rights apparatus remain contained and readable. OCR noise,
retained line hyphens, and occasional corrupt tokens are visible; the text has
not been certified or silently repaired by this review.

**Blocking note/body fusion, page 6.** At the bottom of the left column, the
body ending `au Saint-Siège de s'occuper.` is immediately followed on the same
rendered line by `(1) Aliquando...`. The Latin historical note then continues
into the top of the right column. It is attached to the French body paragraph.

The generated file is
`.scratch/encyclical-classic/readers-fixed/1892-02-16-acta-ass-024-ass-024-010-9592f812-fr/1892-02-16-acta-ass-024-ass-024-010-9592f812-fr.body.tex`.
Line 443 contains the French body ending; line 444 begins the note, which
continues through line 451. There is no blank paragraph or `\par` before the
note. Line 452 supplies only its trailing `\par`. The controlling
`historical.txt` named by the packet likewise has the body ending at **LF
20392**, the note at **LF 20393–20400**, and a blank at LF 20401. Coordinates
here count U+000A only; form-feed characters do not add line numbers.

This finding satisfies both the rendered and exact boundary tests. It is
different from the separate historical-note blocks on pages 2–5, whose
generated boundaries include explicit `\par` pairs: 101/104, 194/205,
253/256, 297/306, and 352/355. Those source-order note blocks may interrupt
sentences or divided words without constituting fusion. A preserved note
requires a separate paragraph boundary before installation; any changed PDF
needs its own review.

### Diuturnum — PASS

Pages 1–6 were viewed in contacts and at full size. The long initial source
protocol is flush left and stays inside its column. Justified Latin text,
citations, page transitions, and the gutter remain legible and consistent.
The final page contains the concluding source blessing and dating clause,
matching the ending of the controlling transcription, before the restrained
terminal apparatus. No material layout defect or apparatus-only page was found.

### Caritatis Studium — PASS

Pages 1–4 were viewed in contacts and at full size. Title, source heading,
Latin body, embedded citations, and paragraph transitions are legible. Page 4
continues the body in the left column and ends in the right column with the
blessing, dating clause, and `LEO XIII`, matching source LF 33–37. The source
notice and rights colophon fit below that ending. No material clipping,
overlap, reading-order defect, or isolated apparatus page was found.

### Pius IX, Optime noscitis — CHANGES_REQUIRED

Pages 1–3 were viewed in contacts and at full size. The two-column geometry,
gutter, notes, and colophon are contained. Both historical note groups on
page 2 are separate paragraphs: generated body.tex boundaries 144/148 and
214/217. Their interruption of source text is not a fusion finding. Page 3
is sparse but retains the historical closing and dating text; its sparseness
alone is not a defect.

**Blocking OCR unreadability, especially pages 2–3.** The reader contains
substantial lexical corruption, rather than merely a few uncertain spellings.
At page 2 lower right the closing blessing includes `Vo& cáritatis 4estem`
and `ex ástimo corde depremptam`; page 3 opens with `JÁratséR, Cunetisque`.
The dating then reads `-Detum ... Mai-lli Agno 1954`, despite the title's
1854 identity. Earlier page-2 text also includes such sequences as
`una-nHni` and `disciplingsm`. These passages require the reader to reconstruct
words and the closing formula, and materially impair use as a reading edition.

The closing corruption is present in the pinned OCR payload, LF 21305–21324,
and in generated body.tex 219–239; the worst closing tokens occur at
231–238. It is not caused by clipping or failed glyph rasterization.
The disclosed uncorrected-OCR status and mechanical fidelity do not cure this
reading-usability failure. Any remedy must preserve source evidence and use
the repository's source-correction/derivative process; this review makes no
proposed word substitutions or historical-date correction.

### AAS 10 peace-prayer act — PASS

Page 1 was viewed in its contact sheet and at full size. The long uppercase
title wraps over several lines but remains within the page. Issuer, date,
and Latin identification are clear. The actual source follows in two columns,
continues in normal reading order, and ends with the historical dating and
`BENEDICTUS P P . XV`, matching source LF 19876–19882. The compact source and
rights notices fit beneath the ending. No clipped lines, overlaps, or material
readability defect was found.

## Scope and limits

This is fresh byte-bound visual acceptance evidence for the listed PDFs.
It does not certify translation accuracy, doctrinal interpretation, rights,
the accuracy of historical source wording, or complete image collation.
Opening/ending and note-boundary comparisons used the packet-pinned local
text and generated body.tex. Restricted ancestor payloads without local paths
were not retrieved; their packet-pinned controller records were hashed.
No original-print facsimiles or external websites were consulted. No separate
qpdf structural validation was performed; the basic PDF inspection commands
listed above succeeded.

Only `.scratch/encyclical-original02-cold-03/` was written. Supplemental
`verification.json`, `source-boundaries.json`, extracted raw text, and an
incremental `checkpoint.json` retain the detailed mechanical and coverage
evidence there. No tracked source, canonical report, shared raster/cache,
manifest, PDF, release, or Git state was modified. No installation, rerender,
rerasterization, or delegation was performed. The two blockers were sent to
the coordinator before final report delivery.
