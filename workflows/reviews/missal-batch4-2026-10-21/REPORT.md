# Missal timeline: fourth parallel batch, 21 October 2026

**Integrated after independent cold review; published to `main` under the
maintainer's 21 October authorization.** Implementation `1bc263922` deployed
through Pages run `39661330623`, and nine changed or core live routes matched
the local build byte for byte. This batch executes plan rows 1–5 of
the continuation plan: route coverage, the Eastern census and local
reception, dossier gaps, originals and acts, and the permission census. The
all-rite project remains in progress. No whole-book text, generated-history
change or reader acceptance is claimed.

## Method

Eight research lanes ran in parallel, each in its own worktree. Every one of
the 174 routes and 36 pre-existing dossiers had exactly one owning lane. Each
lane wrote a dated receipt in
`src/sources/inventories/eucharistic-research-reviews/` and committed locally.
An independent cold reviewer, distinct from the lane author and the
coordinator, then re-opened the cited sources. Reviewers could only narrow,
correct or remove claims. Each receipt carries its reviewer's
`independent_review` envelope and verdict hash. The coordinator merged route
rows by owner, refreshed the audit snapshot, and confirmed with the
reconciliation, source-library and focused-test gates after each lane.

## Results

| Lane | Stages added | Transitions | Gap dispositions | Routes newly with stages | Review |
| --- | --- | --- | --- | --- | --- |
| french-a | 12 documented | – | 11 narrowed, 22 searched | 11 | 12 corrections; two same-copy duplicates merged |
| french-b | 28 documented, 6 provisional | – | 13 narrowed, 21 searched | 13 | 17 corrections; three duplicates removed |
| eastern-census | – | – | 11 searched, 1 not attempted | – | 12 corrections; four "narrowed" claims reverted |
| eastern-gaps | 16 documented; 1 upgraded | 8 documented, 2 provisional | 25 narrowed, 18 searched, 12 not attempted | – | Vienna 1904 stage removed; three change units withdrawn |
| western-gaps | 18 documented | 11 documented | 29 narrowed, 22 searched, 8 not attempted | – | 14 corrections; a closed gap reopened |
| western-regional | 8 documented, 2 provisional | 5 documented | 12 narrowed, 20 searched, 6 not attempted | – | 15 corrections; one misread change removed |
| originals | 10 documented | 4 documented | 11 narrowed, 19 searched, 4 not attempted | 2 | 18 corrections, nothing removed |
| permissions | 1 documented | – | 2 narrowed, 3 searched | – | 28 corrections; 70 permission findings accepted |

| Measure | Before (`5f2e74718`) | After |
| --- | --- | --- |
| Dossiers / traditions | 36 / 156 | 39 / 202 |
| Stages (documented / provisional) | 295 (284 / 11) | 396 (378 / 18) |
| Transitions | 77 | 107 |
| Declared gaps | 203 | 251 |
| Routes with selected stages | 98 | 124 |
| Routes without any mapped stage | 76 | 45 |
| Eastern / Western candidates | 446 / 1,457 | 451 / 1,498 |
| Text coverage | 279 not transcribed, 16 partial | 377 not transcribed, 19 partial |
| Complete whole books | 0 | 0 |

Highlights:

- **French dioceses.** 24 French dioceses now have dated book states, from
  bishops' mandates, colophons, primary acts or exact-locus diocesan
  bibliographies. Every source basis is labelled.
- **Rome.** An inspected Rome Typographia Vaticana 1635 printing carries the
  brief *Si quid est* of 2 September 1634. It now witnesses the Urbanian
  stage.
- **Iberia.** The historic Zaragoza and Valencia uses now have documented
  stages, with calendar transitions.
- **Eastern dossiers.** Gains include Rome 1548 Ge'ez, the Brightman Armenian
  manuscripts, Univ 1740, Supraśl 1758, Pochaiv 1788, the Blaj line,
  Maronite 2005, and transitions for Chaldean 2014–2020 and West Syriac
  1843–1922.
- **Permission census.** The new register holds 70 findings. 21 were read in
  the issuing instrument, 36 rest on official decree summaries with protocol
  numbers, and 13 are official retrospectives or reproduced instruments.
  This falls short of the requested 30 original-instrument findings.

## Corrections to earlier records

- **Braga rights record.** `missale-bracarense-rights-v1.toml` had reported
  St Therese, St John Bosco and the 1929 Sacred Heart Mass absent from the
  scanned 1924 Braga missal, and dated the Queenship leaf 1955. All four
  claims were OCR-probe artifacts. The page images show the formularies, and
  a Queenship approbation of 15 March 1956. The record is corrected in
  place, and its rights holding is unchanged.
- **Coptic 1898 lead.** The Coptic receipt points to HathiTrust
  `oxu1.308011427` as a route to the 1898 Catholic book. It is the 1902
  Orthodox Euchologion.
- **Urmia 1890.** The title photograph matches the Anglican mission
  edition. The Bedjan attribution is not disproved.

## Limits and access

- **Access refusals.** Gallica, HathiTrust and several catalogues refused
  automated access with HTTP 403 or bot challenges. Google Books served
  CAPTCHAs. archive.org, BVMM and USUARIUM timed out for much of the day. No
  challenge was solved or bypassed. Each affected gap records the refusal
  rather than an absence.
- **Acquisitions.** All new acquisitions (about 2,800 receipt entries) are
  hash-recorded and remain outside the repository. Their retention is
  deferred to the maintainer.
- **What is not claimed.** No body text was collated, and no transition
  grants Git ancestry or text inheritance. Most French stages state their
  source basis, and many rest on scholarship rather than inspected leaves.

## Remaining work raised by this batch

- **French dioceses.** 22 routes have searches only. Retry Gallica,
  archive.org and BVMM when they allow access, along with Dubarat's chapter
  xvi for Dax, Auch and Bayonne, and the Mazarine 1162 B copy.
- **Rome and Iberia.** A 1634-dated Rome issue; the Tarragona 1499 copy at
  BVPB; Urgell; the identity of Zaragoza H-1-152.
- **German propers.** Approval stages for the other dioceses confirmed by
  Prot. 697/75. Settle the Speyer 2069/71 date clash and the Speyer stage's
  Lectionary claim.
- **Small record follow-ups:**
  - Valencia candidate certainty fields underclaim.
  - The OSA post-conciliar candidate's title needs requalifying.
  - The Dominican 1550→1604 edge duplicates the new chain.
  - A cross-reference for the joint 1971 Cistercian/OCSO reply.
- **Permission census.** Further original instruments: the Chinese indults,
  Divine Worship 2015, and the Lyon 1864 brief.
- **Whole books, textual ancestry and reader acceptance** remain as recorded
  in [the batch 3 report](../missal-batch3-2026-10-20/REPORT.md#remaining-work).
