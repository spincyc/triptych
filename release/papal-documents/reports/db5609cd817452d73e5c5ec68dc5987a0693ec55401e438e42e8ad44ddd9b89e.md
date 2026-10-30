# Original02 cold review 04, subset-03

Fresh independent visual review of the exact frozen PDF below. No prior inspection or acceptance is inherited. Disposition: **PASS**.

| Identity | Value |
| --- | --- |
| ID | `acta.ass.007.ass-007-act-010` |
| Language | `la` |
| Title | Cum illud semper |
| PDF | `.scratch/encyclical-classic/readers-fixed/1742-12-14-acta-ass-007-ass-007-act-010-0980167b-la/1742-12-14-acta-ass-007-ass-007-act-010-0980167b-la.pdf` |
| PDF SHA-256 | `c26fe2f2bb04e04fdb56ea1cdc918914562e0cc15147a4afa648fddaac97b194` |
| Pages | 5 |
| Actual contact-sheet pages | 1, 2, 3, 4, 5 |
| Actual full-size pages | 1, 2, 3, 4, 5 |
| Individually inspected pages | 1, 2, 3, 4, 5 |
| Reused pages/proofs | None |
| Receipt SHA-256 | `3d675f5fd22af20a3661feebf3c247fd11071df1d3e66c6c2e684764bff8de1e` |
| Frozen manifest SHA-256 | `13e7c7109ce155a4acba1af8df2fe82119e9315e73fcdb41a025e46a59171342` |
| Source SHA-256 | `5b64eabc613113dd83fb03b0798d99c1644d274f3a8d6482cdd97b803624f03d` |
| Segment manifest SHA-256 | `d025afabf7aef8db080a799b31da2ac2b1452c6d28b77679abdbe42f7ced5074` |
| Raster manifest SHA-256 | `ef71348cafc32523cc57fd1052598e3850b3fff4c8dba4d51588bfa1e182cc02` |
| Render revision | `2026-10-30T02:56:48Z` |
| Canonical report destination | `src/sources/papal-documents/encyclicals-original02-cold-04-subset-03.md` |

All supplied PDF, receipt, frozen manifest, source payload, segment (where present), source-controller records and retained payload pins matched exact bytes. The receipt document row and frozen source row matched the packet exactly. `pdfinfo` confirmed the page count, Letter pages, declared identity/language, no encryption and no suspect flag; `pdffonts` reported embedded, subset, Unicode-mapped Latin Modern fonts. Every listed contact sheet, full page and thumbnail matched its retained cache hash/size, and the raster run/cache matched the PDF hash/page count. Evidence is in `pin-verification.json`, `02-pdfinfo.txt`, `02-pdffonts.txt` and `02-pdftext.txt` in the review scratch directory. These pin checks do not establish historical accuracy.

## Observations and bounded source checks

All five pages were freshly inspected in the existing contact sheet and at full native raster size. The compact Cum illud semper/Benedict XIV/date/Latin identity and retained capital address are legible. Dense justified columns, source section numbers and Roman-numbered instructions remain contained with no observed clipping, overlap, isolated heading or obstructive orphan/widow. Literal OCR word divisions and letter spacing remain visible but do not prevent continuous reading.

The historical note beginning 1 Hic obiter nota starts near the bottom of page4 right column and continues on page5. Its end, quod tamen non habet, is followed by a clear new paragraph regendae ecclesiae magis idoneam. Exact LF source lines16578–16605 distinguish the interrupted body, note and body continuation: source16579–16580 are blank before the note; source16603 is excluded running-head furniture and source16604 is blank before continuation. Generated body.tex358 ends the earlier body with \par; note begins360–361 and ends381 with \par382; continuation starts384 and ends393 with \par. This is the permitted separate source-order historical-note interruption, not fusion.

Bounded opening/ending checks used the packet’s exact LF ranges, splitting on LF rather than treating formfeed as another line break. Source16231 begins PATRIARCHIS, PRIMATIBUS, ARCHIEPISCOPIS ET EPISCOPIS, followed by the protocol and incipit visible on page1. Source16605–16613 and body384–393 preserve the resumed body, blessing and Datum Romae/apud S.Mariam Maiorem/die xiv.Dec.MDCCXLII/Pont.Nostri annoIII ending visible on page5.

The final page is sparse in its right column but contains a substantial historical note continuation, resumed historical body, blessing and dating in its left column above the restrained source/rights apparatus. It is source-bearing; no page is project-apparatus-only.

## Findings

No blocking visual defect observed.

## Limits

This accepts layout of the exact five-page OCR reader with its historical-note and literal OCR qualifications. It does not certify every word, historical date, original-print typography or rights basis. No complete historical-print collation, translation review or reference reconstruction was performed.

No new raster/render, source/controller/cache/canonical/installed/release/Git write, network research or installation was performed. The PDF is untagged; accessibility remediation is outside this visual brief.
