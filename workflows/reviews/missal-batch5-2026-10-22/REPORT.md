# Missal timeline: fifth parallel batch, 22 October 2026

**Integrated after independent cold review and collation.** This batch
continues plan rows 1–5 of the continuation plan: route coverage, the
Eastern census, dossier gaps, originals and acts, and the permission
census. It also starts row 6 with bounded native-text constituents. The
maintainer asked for all possible parallel work in sub-agents, a cold review
after each phase, and, on 22 October, a coherent stop with the work plan
persisted and the result pushed to `main`. The all-rite project remains in
progress. No complete whole book, text ancestry or reader acceptance is
claimed.

## Method

- Twelve lanes ran in parallel, each in its own worktree from `a17f42c7e`:
  eight research lanes and four text lanes.
- Every route row and every dossier had exactly one owning research lane.
- Text lanes could change only the text fields of the stages they bound.
  Shared dossiers were merged field by field at integration.
- Every research lane passed an independent cold reviewer, who could only
  narrow, correct or remove claims. Each receipt in
  `src/sources/inventories/eucharistic-research-reviews/*-batch5-2026-10-22.json`
  carries its reviewer's `independent_review` envelope.
- The text lanes worked in two steps:
  - The transcriber built the facsimile, the reading, the passages and the
    extent census, but activated nothing.
  - A distinct collator then re-read every line on the page images,
    corrected the text, wrote the collation receipt and activated the
    binding.
- After each lane, the coordinator re-ran the reconciliation,
  source-library and focused-test gates.

## Results

| Lane | Stages added (doc / prov) | Transitions | Gaps | Review |
| --- | --- | --- | --- | --- |
| french-a | 11 / 15 | – | 22 named gaps added, 6 narrowed | 12 corrections; a duplicate Auxerre candidate folded into USUARIUM 6927 |
| french-b | 15 / 4; Rieux and Vannes upgraded | – | 5 added, 27 narrowed | 10 corrections; Noyon 1631, Tarentaise and Tours 1492–93 made provisional; the Rennes transition removed (it named no change) |
| south | 4 / 0 (Tarragona 1499, Urgell 1509 and 1535–36, Ambrosian 1609) | 1 (Veronica removed 1475→1609) | 11 narrowed | 9 corrections; three Ambrosian 2026 changes held in a gap (unverified pre-press PDF) |
| central-north | 28 / 2 (21 Prot. 697/75 approvals, Speyer and Cologne approvals, Halberstadt) | 4 existing gain calendar loci | 3 added, 13 narrowed | 10 corrections; Prague 1845 made provisional |
| orders | 1 / 1 (Dominican 1985 Proprium; Carthusian [1496]) | +2, −1 duplicate | 7 narrowed | 18 corrections |
| eastern-census | – | – | 2 named gaps (Albanian, Macedonian) | 16 corrections |
| eastern-gaps | 6 / 0; Slavonic-Roman 1893 upgraded | 7 | 21 narrowed | 53 corrections; the mixed EAP 1677 Armenian copy detached from the 1677 stage |
| permissions | – | – | – | 12 corrections, including the Ex pastorali munere date |

| Measure | Before (`a17f42c7e`) | After |
| --- | --- | --- |
| Dossiers / traditions | 39 / 202 | 39 / 259 |
| Stages (documented / provisional) | 396 (378 / 18) | 483 (446 / 37) |
| Transitions | 107 | 116 |
| Declared gaps | 251 | 283 |
| Routes with selected stages | 124 | 141 |
| Routes without any mapped stage | 45 | 18 |
| Eastern / Western candidates | 451 / 1,498 | 455 / 1,517 |
| Checked native text books | 11 | 20 |
| Stages bound to native text | 7 | 13 |
| Text coverage | 377 not transcribed, 19 partial | 462 not transcribed, 21 partial |
| Complete whole books | 0 | 0 |

**Native texts (plan row 6).** Nine complete declared constituents were
added. Each is bound as partial text, as an isolated-root text version:

- **Mozarabic.** The Ordo core, from "Deinde dicat presbiter" through the
  Liberati, in Toledo 1500, Rome 1755 and Rome 1804, with 20 units each.
  Each book's text is the second member of its stage's `text_bindings`,
  after the bread blessing.
- **Roman.** The Canon Missae in Rome 1604 (Clementine) and Rome 1635
  (Urbanian, carrying *Si quid est* of 2 September 1634), with 17 units
  each, on the 1570 paths.
  - Cum sanctissimum's dating clause, 7 July 1604, is legible on the image.
  - Image-confirmed changes: in 1570→1604, N. becomes N. et N., Amen is
    added after the Communicantes and the Hanc igitur, and Haec
    quotiescumque is now said secretly. In 1604→1634, the only change is
    "Iungit manus, et caput inclinat".
- **Dominican.** The Canon in Venice 1550, Venice 1553 (the Salamanca 1551
  reform), Rome 1603 and Rome 1604 (Xavierre), with 14, 14, 15 and 15 units.
  The concluding Per omnia is printed only in the notated Cantus solemnis,
  so it is excluded. Two new BSB edition records were added.

The new tracked facsimiles are 13 files, 55.8 MB in total. The largest is
12.3 MB. The rights basis is US public domain by publication date.

**Permission census (plan row 5).** The register now holds 148 findings, 147
of them active. Findings read in the issuing instrument went from 21 to
**40**, 35 of them without caveat, against the requested 30. The batch adds
the following instruments: the Chinese indults of 1615 and 1673, the
Glagolitic instruments of 1631–1909, Zaire 1988 (which supersedes its
summary finding), Ambrosian, Braga, Udine and India instruments, and the
2022 licences for the 1962 Missal.

## Corrections to earlier records

- **Rome 1570 Canon reading (already published).** It departs from its
  retained images:
  - it reads "Et quotquot" where the print has "Ut quotquot";
  - the doxology order is wrong;
  - the Amen after the Memento of the dead is missing;
  - "surgit et ostendit" is missing its "et";
  - the closing "Iungit manus" is missing;
  - printed capitals are not kept.

  The 1570 stage now carries a limitation saying so. Two 1570→1604 changes
  that rested on the misreading were removed. A re-collation is in
  progress; see the work plan, row 6.
- **Ex pastorali munere (1754).** Its date and sanction clause had been read
  from the next constitution in the Bullarium. It now has 25 August
  (VIII Kal. Sept.).
- **Dominican transitions.** The duplicate 1550→1604 shortcut is removed,
  and the chain 1550→1553→1603→1604 carries the evidence.
- **Re-datings.** The OSA early print is re-dated to 1491 from its colophon.
  The Carthusian 1496 print is undated, so its stage is provisional.
- **Speyer.** The date clash is two acts: the common calendar of
  21 September 1972, and the diocesan calendars of 41 sees confirmed on
  15 November 1972.

## Limits and access

- **Refused or unavailable access.**
  - Gallica, HathiTrust, BNE, CCPB and the Vatican catalogues returned
    HTTP 403.
  - BVPB returned HTTP 429 throughout.
  - Google Books quotas, ISTC and COBISS bot challenges blocked access.
  - BVMM and USUARIUM were intermittent.
  - No challenge was solved or bypassed. Each affected gap records the
    refusal.
- **Acquisitions.** Thousands of hash-recorded acquisitions remain in
  scratch only. Their retention is deferred to the maintainer.
- **Not integrated.** Two text efforts stopped at the maintainer's wrap-up
  and were not integrated; see the work plan, row 6.

## Work plan for the remaining work

Rows 1–5 can run in parallel. Rows 6, 7 and 8 must run in that order.

| # | Workstream | Open requirement | State after batch 5 | Remaining work |
| --- | --- | --- | --- | --- |
| 1 | Close route coverage | historical-catalogue | 141 routes have selected stages; 18 have no stage; 30 have no researched sequence; 3 have related evidence only | Originals refused by Gallica: Mirepoix 1753, Sarlat 1777, Vannes 1535. Original leaves for Tarragona and Urgell (BVPB). The Sainte-Geneviève copy of Tours c.1492; the Noyon 1631 title leaf; Tarentaise BnF B-1484; the Bayonne originals; Mazarine 1162 B; Huesca 1488. New routes for the Roman returns at Saint-Brieuc, Quimper and Nantes, and for the Paris-missal adopters Orange, Dol and Digne. Map Grenoble's use of the Vienne provincial missal. |
| 2 | Eastern census and local adoption | historical-catalogue | The census is bounded to the official list of 15 Nov 2016; Albanian and Macedonian have named gaps | A 2026 Annuario Pontificio enumeration; the Albanian and Macedonian books; the original 1968 Lungro decree; reception at Piana and in the Greek exarchate; dated Hungarian use |
| 3 | Close dossier gaps | full-research | 283 gaps; this batch narrowed 86, searched 103 without change and left 89 not attempted | A printed copy of the Ambrosian 2026 missal; the Maronite 1908 state; pp. 7–19 of the EAP 1677 copy; collation of Urmia 1906 against Rome 1767; the Speyer 2023 Lectionary; the identity of the Prague 1845 book; the decree texts for the 21 sees; the Cologne Gross collect of 19 Dec 2002; a lower date bound for the Carthusian print; OCSO after 1995 |
| 4 | Acquire originals and decrees | full-research | A Rome issue dated 1634 is still not found | The Lyon brief of 1864; the 2015 Divine Worship decree; a Bullarium copy for Ex pastorali munere; the *Decreta authentica* (1892 against 1893); AAS 1 (1909), p. 577 |
| 5 | Permission census | full-research | Target met: 40 findings read in the instrument, 35 without caveat | Widening: Lyon 1864, Divine Worship 2015, the Chinese indult of 1949, and the Farnés 1993, Lugano 1976 and Spanish Ordo 1992 instruments; a rule for overlapping finding pairs |
| 6 | Complete book texts | witnesses-and-texts | 20 checked constituents; 0 complete books | **Greek Chrysostom anaphora** (1738, 1754, 1873): the lane's work is on local branch `batch5/text-greek` (`9dfdf469d`), and a partial WIP collation is at `beba6c641`. 1754 and 1873 are fully collated; 1738 pp. 40–41 and the declarations of the 1873 editorial supplies remain. **Rome 1570 re-collation**: WIP `c5ea1849b` on `batch5/text-roman-1570`, with a draft of lines 1–64 in that lane's scratch; p. 286, the rebuild and an independent collation remain. Then further Order-of-Mass and Canon constituents per tradition. Decision B governs closure. |
| 7 | Text ancestry and Git history | git-history | Contiguous evidenced chains now exist; no new parent edges yet | Parentage receipts and parented `text_versions`: Mozarabic Ordo 1500→1755→1804; Roman 1570→1604→1634, after the 1570 re-collation; Dominican 1550→1553→1603→1604; Greek, after collation. Then verify the corpus diffs. |
| 8 | Reader and print acceptance | map | Not run on the batch-4 or batch-5 data | Interactive, accessibility and print review of the expanded data; a spoken screen-reader test; production-sheet and physical-print proof; the maintainer's verdict |
| 9 | Integrate and close | execution-through-completion | Batch 5 integrated | The retention decision for the scratch acquisitions; ledger closure; workspace cleanup, which must not happen before the retention decision |

Decisions only the maintainer can make:

| | Decision | State |
| --- | --- | --- |
| A | Push target | Pushes to `main` are authorized one request at a time; this batch was authorized on 22 October |
| B | How much text counts as "complete" for witnesses-and-texts | Open. The text lanes produce bounded constituents, which count under any definition. |
| C | Retention of the scratch acquisitions | Open. `wt tidy` and `wt sweep` must not run until it is decided. |
| D | Smaller choices raised by the cold reviews | Open. Whether single Analecta hymnica sequence witnesses suffice for documented stages (five accepted). Whether to keep both Veronica edges. Whether Bayonne 1836 is a stage or a reprint. Whether to retitle `german-diocesan-uses`. Whether Maronite 1908 is a distinct state. |
