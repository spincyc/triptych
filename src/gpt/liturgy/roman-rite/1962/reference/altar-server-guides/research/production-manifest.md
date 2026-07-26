# Production manifest: 1962 altar-server guides

Audit date: 2026-07-24 (America/Chicago).

This record distinguishes the immutable six-PDF predecessor snapshot from the
seven publications now installed. The redesigned Low-Mass child booklet, new
trainer manual, and new flash cards are installed evaluation publications.
Their installation was expressly authorized after the pending actual-size,
physical-duplex, photocopy, paired-use, independent, rights, and
ecclesiastical-review gates were disclosed. That evaluation override records
installation only: it neither completes those gates nor release-authorizes the
three PDFs. The four sung PDFs remain byte-for-byte identical to their
installed and authorized artifacts.

## Historical reviewed predecessor snapshot

The following six PDFs carry revision timestamp `2026-07-23T02:31:26Z`. They
formed the installed predecessor set under
`doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/`. The four sung
PDFs remain installed unchanged. The two Low-Mass predecessor PDFs have been
superseded by the current installed evaluation trio.

| Installed publication | Pages | Physical cards | Bytes | SHA-256 |
| --- | ---: | ---: | ---: | --- |
| `01-low-mass` | 15 | 0 | 571,087 | `bfed57816157141c676b6bf8e460e13d53696a14dc76d159a5c9b7cf5df35009` |
| `01-low-mass-cue-cards` | 8 | 24 | 430,042 | `2ee877985ecaa737ee62a3d8cfe2c87858c2a7526b626fbcc28eefe4dbcfb12e` |
| `02-missa-cantata` | 29 | 0 | 668,985 | `09c14200921ff31fe72aff9ee7de20370241f104de3d59c00c641fadd71eeaff` |
| `02-missa-cantata-cue-cards` | 12 | 36 | 474,866 | `29dcbd0390872b3474f26b5096907730bb856ddfb360dbd1f5cb3a43b0a488b2` |
| `03-solemn-mass` | 31 | 0 | 681,161 | `c00ddb2319aa14b703c24655f28d36de4e36434e6c98fde651d65c1e65e4ec63` |
| `03-solemn-mass-cue-cards` | 12 | 36 | 479,127 | `725b02f8f11dbcc2dd350c95cea8ea82a2626f48d7249efd07786886fb26fed7` |

The predecessor identities, page extents, and byte counts were rechecked on
2026-07-23. The six exact hashes received the recorded 23 July exact-byte
authorization. That authorization remains a historical fact about only those
immutable bytes; it neither approves the changed Low-Mass PDF nor creates
approval for the new trainer-manual or flash-card identities.

The earlier production review for this snapshot established clean logs,
valid PDF structure, embedded fonts, successful text extraction, every-page
screen review, and correct six-up card pairing. Those results remain
historical evidence for the exact PDFs named above. They are not reused as
verification of the redesigned Low-Mass publications.

## Current installed evaluation set

The Low-Mass child and trainer timestamps identify their final shared ceremony
state. The flash-card timestamp is independent and also inherits the trainer
provenance. A final shared-response-source cleanup changed only a hidden
Low-Mass full-guide instruction branch; rebuilding all seven publications
reproduced the exact flash-card and four sung-form hashes below.

| Source publication | Revision UTC | Pages | Physical cards | Bytes | SHA-256 | State |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `01-low-mass` | `2026-07-26T10:27:32Z` | 30 | 0 | 222,382 | `820b5aef1d1c39aa498955d87a9911c1a6f51f3d5db43611963340cc2e2914d4` | installed action-first evaluation snapshot; not release-authorized |
| `01-low-mass-trainer-manual` | `2026-07-26T10:27:32Z` | 30 | 0 | 238,060 | `5899cb40a25802c047cdae1593154f884cd1e0f521f10cf2f727ccce70bbc64a` | installed page-aligned evaluation snapshot; not release-authorized |
| `01-low-mass-flash-cards` | `2026-07-23T21:26:03Z` | 6 | 22 | 73,254 | `d361503e0bd46c873d07411ce3cce2fe184fb690bb3c7cb66aaa48e45ab7dc35` | installed evaluation snapshot; not release-authorized |
| `02-missa-cantata` | `2026-07-23T02:31:26Z` | 29 | 0 | 668,985 | `09c14200921ff31fe72aff9ee7de20370241f104de3d59c00c641fadd71eeaff` | unchanged; installed exact match |
| `02-missa-cantata-cue-cards` | `2026-07-23T02:31:26Z` | 12 | 36 | 474,866 | `29dcbd0390872b3474f26b5096907730bb856ddfb360dbd1f5cb3a43b0a488b2` | unchanged; installed exact match |
| `03-solemn-mass` | `2026-07-23T02:31:26Z` | 31 | 0 | 681,161 | `c00ddb2319aa14b703c24655f28d36de4e36434e6c98fde651d65c1e65e4ec63` | unchanged; installed exact match |
| `03-solemn-mass-cue-cards` | `2026-07-23T02:31:26Z` | 12 | 36 | 479,127 | `725b02f8f11dbcc2dd350c95cea8ea82a2626f48d7249efd07786886fb26fed7` | unchanged; installed exact match |

The current source set is 150 pages: 120 guide or manual pages and 30 card
pages. It contains 94 physical cards: 22 Low-Mass cards, 36 Missa-Cantata
cards, and 36 Solemn-Mass cards. It has 70 distinct card IDs: 22 LM-F
selections, 24 shared R responses, 12 MC actions, and 12 SO actions. The shared
R deck is physically repeated in both sung companions.

## Build and mechanical validation

- pdfTeX 1.40.29 from TeX Live 2026 rebuilt all seven publications for enough
  passes after the final shared-source cleanup. The child and trainer hashes
  include the closed actor-label correction; the flash-card and four sung-form
  PDFs reproduced their prior exact hashes.
- The repository metadata checker validates all 106 canonical and 6 inherited
  generation records, and validates each of the seven PDFs against its
  declared metadata.
- All seven logs contain no fatal error, undefined reference, LaTeX or package
  warning, overfull box, underfull box, or unresolved rerun notice.
- `qpdf --check` reports no syntax or stream-encoding error in any PDF.
  `pdfinfo` confirms page counts of 30/30/6/29/12/31/12 and 612 by 792 point
  US-letter geometry.
- Every listed font is embedded and subsetted and has a ToUnicode map. UTF-8
  text extraction succeeds in all three Low-Mass PDFs with no replacement
  character and no observed fallback family.
- The four sung PDFs reproduce the exact reviewed and installed hashes above.
  The redesign therefore changed no sung-form rendered byte.

### Production font audit

pdfLaTeX embeds Type 1 conversions of Atkinson Hyperlegible Next 2.001:
Regular, Bold, Regular Italic, and Bold Italic as used. Atkinson Hyperlegible
Mono 2.001 Regular appears only in compact terminal file-name references.
The flash cards use Next Regular and Bold plus that terminal Mono face.

| Embedded source face | Exact local PFB SHA-256 |
| --- | --- |
| Next Regular | `43d2d95d68a308408ec90ab677a43b5bb5fa9e91f400891c7ebddb88a09f1761` |
| Next Bold | `195de55190dc80712bea9b280c0bfd47dc582e089e9600cc4623241ce1d9c65a` |
| Next Regular Italic | `68c28967f1976e113ea4543760caea83b0e6c5a3fc81202026d8aaa0b0bb8a2e` |
| Next Bold Italic | `3cff85588da7a6bcefd8c192cd11f54cce412bfb3db43a7920d26f874abd9bc2` |
| Mono Regular | `881e8e34751cbf5d807c7b4bd222f4671a9508a43d45d9a99429b93d533bf462` |

Technical embedding, used-glyph coverage, and fallback checks pass. Rights
evidence is recorded without silent reconciliation: the current Braille
Institute and Google Fonts distribution identifies SIL Open Font License 1.1,
while the installed 2.001 font's own name-table notice permits free commercial
and noncommercial use without derivatives or alteration and its OS/2 metadata
permits editable embedding. The PDFs embed subsetted font programs; that
technical observation does not reconcile the license evidence or characterize
subsetting as a permitted alteration. The TeX support package retains its
separate LaTeX Project Public License.

## Low-Mass flash-card audit

Text extraction finds exactly 22 `PRIEST` front headers and 22 `BOTH` back
headers. It finds no pronunciation, meaning, action, score, mastery, or
servers'-Confiteor teaching block. The source and raster review confirm the
fixed 11.5-point body, full cue or selected exemplar, bold complete response,
consistent three-zone header, and two unbordered final positions.

| Sheet pair / physical pages | Front grid | Mirrored back grid |
| --- | --- | --- |
| 1 / 1--2 | 01 02 / 03 04 / 05 06 / 07 08 | 02 01 / 04 03 / 06 05 / 08 07 |
| 2 / 3--4 | 09 10 / 11 12 / 13 14 / 15 16 | 10 09 / 12 11 / 14 13 / 16 15 |
| 3 / 5--6 | 17 18 / 19 20 / 21 22 / unused unused | 18 17 / 20 19 / 22 21 / unused unused |

Thus Low-Mass fronts are pages 1, 3, and 5; backs are pages 2, 4, and 6.
Each odd front begins a self-contained long-edge duplex pair. The Missa
Cantata and Solemn Mass companions retain their previously reviewed fronts on
pages 1, 3, 5, 7, 9, and 11 and mirrored backs on pages 2, 4, 6, 8, 10, and
12.

## Historical 2026-07-24 every-page screen review

The bounded repository review tool rastered all 72 pages in the Low-Mass
evaluation trio.
Complete-document contact sheets were checked for order, density, navigation,
monochrome hierarchy, clipping, accidental blanks, card pairing, and terminal
fit. Every unchanged child and trainer page was exact-raster compared with its
previously inspected full-size image. The seven changed pages in each book
(2, 15, 20, 21, 27, 28, and 33) were then inspected individually at full
size. All six unchanged flash-card pages had already received individual
full-size inspection and were rechecked as a complete deck.

The final audit changed the page-28 actor label from `First and Second` to the
closed label `Both` and otherwise advanced only the page-33 generation
timestamp. Pages 28 and 33 in both books were re-inspected at full size after
that rebuild; text extraction confirms `BOTH`, and neither page reflowed or
clipped.

The final screen review found no clipping, collision, broken sequence,
accidental blank, split unit, or terminal overflow. In particular:

- the child and trainer shared the same 33-page order and main-lane source;
- the Lavabo and ablution figures stand on the named second step and remain on
  the stated side of the altar edge;
- the Communion scene prints the complete `PRIEST` label, distinguishes the
  plate bearer from the kneeling First Acolyte, and names the nave-facing
  picture-left orientation exception;
- the altar, three levels, Missal states, standing figures, and kneeling
  figures remain visually distinct; and
- all card text and borders remain within their intended cells, with the last
  two positions wholly blank and unbordered.

Screen review does not substitute for the pending physical tests.

## Installed evaluation override and pending review

After the following outstanding gates were disclosed, the maintainer expressly
authorized installation of the exact three Low-Mass snapshots as an installed
evaluation set. Before any release decision, or any representation
that physical or independent review is complete, they still require:

- actual-size reader testing of the 11.5-point flash-card body with children
  in the intended age range;
- a physical long-edge duplex overlay or cut-and-turn test of every card cell;
- black-and-white photocopy review for hierarchy, clipping, and cut safety;
- paired child-and-parent use testing of the child booklet and page-matched
  trainer rail; and
- independent liturgical, ceremonial, Latin-pronunciation, pedagogical,
  rights, and ecclesiastical-suitability review.

The exact three Low-Mass PDFs listed in the current table have been copied into
their mirrored `doc/` paths. Installation and catalog visibility do not grant
distribution clearance. No current Low-Mass snapshot has received a new
exact-byte authorization; the historical exception remains limited to the six
predecessor hashes listed first.

## Uninstalled corrected source candidates

On 2026-07-24 the current source produced the following review-only
candidates. They remain under `build/`; they have not been copied to `doc/`,
installed, cataloged as replacements, or exact-byte authorized. The installed
identities remain the hashes in the current installed evaluation table above.

| Source publication | Revision UTC | Pages | Bytes | SHA-256 | State |
| --- | --- | ---: | ---: | --- | --- |
| `01-low-mass` | `2026-07-24T16:29:47Z` | 33 | 226,102 | `265768f40697564282b16794f404c7918b149910578e063604b0114cdf40b4a8` | uninstalled review candidate |
| `01-low-mass-trainer-manual` | `2026-07-24T16:29:47Z` | 33 | 240,886 | `5d93d21b684806b2fbc4c3c6a638bee5f8608df5f8d2c067605f6202e63cadce` | uninstalled review candidate |
| `02-missa-cantata-cue-cards` | `2026-07-24T16:06:15Z` | 12 | 474,936 | `85e652e540494f59b7bccd7717ff11069925f4b9f7f9e90be042b751ddde381b` | uninstalled review candidate |
| `03-solemn-mass` | `2026-07-24T16:06:15Z` | 31 | 681,159 | `efb37f8356c6695c5a4a89e8ba9a37dc5bbd22ca6bfb6c5d4d0ec0c7fc3d25ab` | uninstalled review candidate |
| `03-solemn-mass-cue-cards` | `2026-07-24T16:06:15Z` | 12 | 479,186 | `60af9f4f83b9d8508fc5dd29b363682dbf23fda63ca38764726901d2b3ae58c9` | uninstalled review candidate |

The Low-Mass pair refines the shared monochrome vector illustration system:
altar and three-step architecture, standing and kneeling figures, facing
direction, role and object labels, Missal and service-object drawings, and
movement-path hierarchy. It also corrects the selected two-acolyte teaching
model in words and pictures. First moves the Missal from Epistle to Gospel for
the Gospel and continuously handles the Communion plate. After the final wine
and water, each server returns his own cruet; First then returns the
priest-cleared plate and reaches his normal place before Second returns the
Missal from Gospel to Epistle. The priest's paten and chalice remain distinct
from the Communion plate: the priest reassembles, veils, centers, and
ultimately carries his chalice, using the loose veil kept at his declared
altar resting place. Neither server transfers the chalice or its veil in this
selected model.

The final illustration audit separates the waiting Communion plate from the
Gospel-side Missal, places Second at the Gospel-side foot while First returns
the plate, keeps all three level markers visible in the completed
post-ablution scene, and clears the prepared-chalice callout from the
Last-Gospel role labels. The child and trainer continue to share one main-lane
source and page order.

The official 1962 Missal controls the celebrant's ablutions, prepared chalice,
Communion-plate clearance, unnamed post-ablution minister, and chalice
recession. O'Connell 1943, pp. 170--174, supplies the selected asymmetric
Missal allocation and First's continuous plate assignment; Carmody 1961,
p. 87 and pp. 91--94, confirms that the purified plate is removed after the
second wine and water and before the Missal is replaced. O'Connell's
additional First-carried veil, his older second Communion Confiteor, and
Fortescue's contrary post-Communion book allocation are recorded but not
silently imported. This is a documented teaching-model synthesis, not a claim
that the manuals prescribe one universal assignment.

The three sung-form candidates make layout-only corrections discovered during
the required full-series visual review. The Solemn guide now keeps the
complete `Present; do not push` movement unit on one page. Both sung
companions use the established dense answer layout for R08B, preserving all
verbal fields while restoring a safe inset for its continuation note. Their
page counts, card selections, odd-front parity, mirrored backs, and grid
geometry remain unchanged.

pdfTeX 1.40.29 rebuilt all seven publications after the final shared-source
edits. The Low-Mass flash cards and Missa Cantata full guide reproduced their
exact installed hashes. The repository metadata checker accepts all canonical
and inherited records; all seven logs are free of fatal errors, undefined
controls, warnings, overfull or underfull boxes, and rerun notices; and
`qpdf --check` accepts all seven PDFs. All seven remain 612-by-792-point
letter-size PDFs. Every font is embedded and subsetted with a ToUnicode map,
UTF-8 text extraction has no replacement character, and Ghostscript ink
coverage reports zero cyan, magenta, or yellow on every page.

The bounded repository review tool rastered complete exact baselines for all
seven publications. Final full-size rasters made with its recorded renderer
were then compared byte-for-byte with those tool-owned page caches. The first
comparison isolated Low-Mass pages 28, 29, 32, and 33; Solemn pages 5, 6, and
31; and each corrected sung companion's pages 8 and 12. After the final
Communion-branch audit, both Low-Mass books were rebuilt and fully rastered
again. A second byte-for-byte comparison against their immediately preceding
inspected candidates isolated pages 27, 28, and 33; every other page retained
its exact inspected raster. Complete-document contact sheets and the changed
pages were checked for order, density, navigation, monochrome hierarchy,
clipping, accidental blanks, split action units, card pairing, cut safety,
and terminal fit. The substantive corrected pages 27--29 and 32 in both
Low-Mass books, Solemn pages 5--6, and both sung companions' page 8 passed
individual full-size inspection; the remaining changed terminal pages carry
only their new generation timestamp and also fit. The unchanged Low-Mass
flash cards and Missa Cantata full guide retain their exact reviewed hashes.
Screen review found no remaining collision, clipping, broken sequence,
accidental blank, split unit, unsafe diagram ambiguity, cut-border incursion,
or terminal overflow.

Screen review does not substitute for the pending actual-size, physical
duplex, photocopy, paired-use, independent, rights, or
ecclesiastical-suitability gates.

## 2026-07-25 Low-Mass corrective installation

The child booklet and trainer manual were rebuilt from the corrected
two-acolyte source and installed as the exact 30-page evaluation snapshots in
the current table. The installed pair now assigns the Epistle-to-Gospel Missal
move to First and the Gospel-to-Epistle return to Second in both words and
pictures. Every diagram contains at most the two declared acolyte figures;
where the celebrant is needed as a cue or handoff partner, his distinct
chasuble silhouette and `PRIEST` capsule remain explicit.

Three short sequences now share sheets without reducing any established
teaching type size: Confiteor parts 2 and 3 on page 10, the normal-place move
and Kyrie on page 13, and the Gospel responses and post-Gospel branches on
page 16. The pair therefore falls from 33 to 30 pages. The child and trainer
retain the same physical page boundaries and identical main-lane order; every
trainer rail still names the matching child page.

pdfTeX 1.40.29 rebuilt both publications for two passes with the temporary
Atkinson package tree used only for this run. Both final logs contain no fatal
error, undefined reference, LaTeX or package warning, overfull or underfull
box, or unresolved rerun notice. The bounded repository review tool rastered
all 60 final pages. Complete contact sheets were checked for order, density,
split units, clipping, collisions, actor count, Missal ownership and route,
and terminal fit; the three consolidated pages and the Missal-move page were
also checked at full size. No orphaned continuation, accidental blank, third
acolyte, clipped label, or unsafe Missal-route ambiguity remains.

Ghostscript decoded both complete PDFs through its null-page device without
error, and `pdfinfo` accepts their structures. They remain 612-by-792-point
US-letter documents; all fonts are embedded, subsetted, and carry ToUnicode
maps; UTF-8 text extraction contains no replacement character; and
Ghostscript reports zero cyan, magenta, or yellow ink on every page. `qpdf`
was not available in this build environment, so no new `qpdf --check` result
is claimed for these exact bytes. This corrective installation does not
satisfy the pending physical, intended-reader, independent, rights-review, or
ecclesiastical-suitability gates and does not release-authorize either exact
snapshot.

## 2026-07-26 action-first reconciliation

The two retained Low-Mass revisions were reconciled into the installed
30-page pair. The child publication is now an action-first field guide; the
trainer remains physically page-aligned while reserving meanings, correction
points, and adult preparation notes for its trainer rail. The pair also makes
the selected two-acolyte model and local choices explicit, separates the two
ablution moments, and keeps the Communion-plate return ahead of the Missal
return.

The complete seven-publication family rebuilt with the declared Arch
dependencies. The five non-Low-Mass outputs reproduced the source candidates
or installed identities already recorded above. The repository review tool
rastered every page of all seven PDFs. Complete contact sheets for the
60-page Low-Mass pair and the retained exact review records for the other
five publications show no clipping, collision, accidental blank, broken
sequence, or role ambiguity. Both installed Low-Mass PDFs remain on hold for
renewed exact-snapshot authorization; this reconciliation adds no physical,
intended-reader, independent, rights, or ecclesiastical approval.
