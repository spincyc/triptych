# Production manifest: 1962 altar-server guides

Audit date: 2026-07-23 (America/Chicago).

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
| `01-low-mass` | `2026-07-24T03:20:06Z` | 33 | 0 | 203,660 | `25e61efa29745f5e69ac24ddcabc94bcba3ba4424a61261c71dbb7089473335b` | installed evaluation snapshot; not release-authorized |
| `01-low-mass-trainer-manual` | `2026-07-24T03:20:06Z` | 33 | 0 | 219,207 | `c507df839af9b96ee273e0d4317a54109779d8bd155b955298c2f6d1ef207c56` | installed evaluation snapshot; not release-authorized |
| `01-low-mass-flash-cards` | `2026-07-23T21:26:03Z` | 6 | 22 | 73,254 | `d361503e0bd46c873d07411ce3cce2fe184fb690bb3c7cb66aaa48e45ab7dc35` | installed evaluation snapshot; not release-authorized |
| `02-missa-cantata` | `2026-07-23T02:31:26Z` | 29 | 0 | 668,985 | `09c14200921ff31fe72aff9ee7de20370241f104de3d59c00c641fadd71eeaff` | unchanged; installed exact match |
| `02-missa-cantata-cue-cards` | `2026-07-23T02:31:26Z` | 12 | 36 | 474,866 | `29dcbd0390872b3474f26b5096907730bb856ddfb360dbd1f5cb3a43b0a488b2` | unchanged; installed exact match |
| `03-solemn-mass` | `2026-07-23T02:31:26Z` | 31 | 0 | 681,161 | `c00ddb2319aa14b703c24655f28d36de4e36434e6c98fde651d65c1e65e4ec63` | unchanged; installed exact match |
| `03-solemn-mass-cue-cards` | `2026-07-23T02:31:26Z` | 12 | 36 | 479,127 | `725b02f8f11dbcc2dd350c95cea8ea82a2626f48d7249efd07786886fb26fed7` | unchanged; installed exact match |

The current source set is 156 pages: 126 guide or manual pages and 30 card
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
  `pdfinfo` confirms page counts of 33/33/6/29/12/31/12 and 612 by 792 point
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

## Every-page screen review

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

- the child and trainer share the same 33-page order and main-lane source;
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
