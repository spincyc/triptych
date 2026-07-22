# Production manifest: 1962 altar-server guides

Audit date: 2026-07-22. The full-guide revision timestamp is
`2026-07-22T19:25:31Z`; the card-companion revision timestamp is
`2026-07-22T20:28:22Z`.

## Exact reviewed builds

All six publications were built as US-letter portrait PDFs with pdfTeX
1.40.29 from TeX Live 2026. The build ran all required passes and validated
both canonical and inherited generation metadata.

| Publication | Pages | Cards in this copy | Bytes | SHA-256 |
| --- | ---: | ---: | ---: | --- |
| 01-low-mass | 31 | 48 | 666,459 | `cb3a45e5bec74fe4fbb90cf8006adbe8849cf85d17cfe0de9ce987e0fb0a9cc1` |
| 01-low-mass-cue-cards | 16 | 48 | 400,342 | `6d8475a9d511db10dd469e8a5d79f80cd2d3a4f7687630ac5665541fe8fcd7e8` |
| 02-missa-cantata | 49 | 60 | 742,298 | `20db8f6ba874e5eeda54ebf2fce5f8d64ac8832b7a0b396d229bda240ca757e4` |
| 02-missa-cantata-cue-cards | 20 | 60 | 405,776 | `e547b22c0eab9f4899a708564e2d8c55781e6e71cd1e6aa403bc105e9cbd5eea` |
| 03-solemn-mass | 51 | 60 | 753,282 | `8ac222949e9a17c3f818f0b55479ee97d85472a3957413398fa790b792e7d40d` |
| 03-solemn-mass-cue-cards | 20 | 60 | 401,530 | `796a3ff499b7c425e771bbea384c08d87bf6d3c97b472bec967c139794fde011` |

One complete selection from the three guide families contains 168 card
copies derived from 72 distinct owner cards: 24 cue-to-response, 24
Latin-to-pronunciation-and-meaning, twelve Missa-Cantata action, and twelve
Solemn-Mass action cards. The six PDFs render that selection twice—once in
the full guides and once in their print-only companions—for 336 card copies
across 56 duplex sheet pairs.

## Family and learner navigation

Every full guide opens with a family start sheet that says what to teach first,
how to practise a short lesson, and exactly which numbered pages to print.
The Low-Mass leaf routes a learner through six small word-only lessons and
contains no ceremonial direction. Each sung full-guide leaf puts the child's
scene map and individual role sheets before the complete numbered chronology,
which is retained as the coach's reference. Contents entries lead directly to
each role, and the start sheet explains where a role-only print selection ends.

The response course keeps cue, canonical answer, child-readable sound line,
meaning, speaker rule, and adult-check IPA distinct. Its course order moves
from five vowel anchors through six short lessons and then consolidates the
same learned answers in Mass order.

Each card companion deliberately omits the cover, contents, lessons, role
packets, card key, and terminal reference page. It contains only the complete
detachable C, P, and, where applicable, action decks. A family uses the key in
the matching full guide for speaker rules and printing instructions, then
prints the companion without selecting page ranges.

## Technical checks

- All six build logs are free of fatal errors, undefined references, LaTeX
  or package warnings, overfull boxes, and underfull boxes.
- `qpdf --check` reports no syntax or stream-encoding errors in any PDF.
- `pdfinfo` confirms 31/16/49/20/51/20 pages and 612 by 792 pt US-letter
  geometry.
- Each full-guide PDF catalog retains its page-label map, so the advertised
  numbered ranges resolve to the corresponding physical card pages in
  label-aware PDF print dialogs. Companion page numbers are their physical
  page numbers.
- Every listed font is embedded and subset. The TIPA fonts used for broad IPA
  are embedded.
- Layout-preserving text extraction succeeds for all six publications.
  Family start headings, form-specific C03 text, terminal action-card IDs,
  and the final revision timestamps remain extractable. IPA glyphs were also
  inspected in the rendered response bank at full size.

## Every-page and card review

The review tool rastered all 187 pages from the exact final PDFs. Every page
was inspected in complete-document contact sheets for page order, density,
navigation, monochrome legibility, split action units, clipping, accidental
blanks, and writable space. Family start sheets, the revised Solemn-Mass role
run, form-specific C03 cards, dense chronology pages, pronunciation cards,
both action decks, and each card-key-to-first-front transition were
additionally inspected at full size. A second targeted review confirmed the
final fixes to the indivisible response lessons, Missa Cantata section 6.8,
the Solemn-Mass practice-stage break, and each companion's final back and
rights notice. No clipping, collision, unsafe diagram, accidental blank,
broken sequence, orphan heading, or colophon overflow was found.

All card faces stay inside their cut borders. Actual-size printing is US-
letter portrait, two-sided, flipped on the long edge. Six cards fit on each
face in two columns by three rows; there are no filler cards or blank backs.
The measured duplex audit checked all 28 design pairs in the full guides and
their 28 duplicate renderings in the companions:

| Publication | Numbered card pages | Physical card pages | Page before first front | Duplex pairs | Result |
| --- | --- | --- | --- | ---: | --- |
| 01-low-mass | 13--20 and 21--28 | 15--22 and 23--30 | 14 | 8 | every first front odd; mirrored order passed; six borders aligned; no blank backs |
| 01-low-mass-cue-cards | 1--8 and 9--16 | 1--8 and 9--16 | none; starts with a front | 8 | every first front odd; mirrored order passed; six borders aligned; no blank backs |
| 02-missa-cantata | 27--34, 35--42, and 43--46 | 29--36, 37--44, and 45--48 | 28 | 10 | every first front odd; mirrored order passed; six borders aligned; no blank backs |
| 02-missa-cantata-cue-cards | 1--8, 9--16, and 17--20 | 1--8, 9--16, and 17--20 | none; starts with a front | 10 | every first front odd; mirrored order passed; six borders aligned; no blank backs |
| 03-solemn-mass | 29--36, 37--44, and 45--48 | 31--38, 39--46, and 47--50 | 30 | 10 | every first front odd; mirrored order passed; six borders aligned; no blank backs |
| 03-solemn-mass-cue-cards | 1--8, 9--16, and 17--20 | 1--8, 9--16, and 17--20 | none; starts with a front | 10 | every first front odd; mirrored order passed; six borders aligned; no blank backs |

Every advertised range begins on an odd numbered page and excludes its
instruction page, so a range-only print job begins with a front. In each
complete PDF, the first physical pages of the C, P, and applicable action
decks are respectively 15/23, 29/37/45, and 31/39/47; all are odd. The exact
build needed no inserted blank parity leaf: the shared key finishes on
physical page 14, 28, or 30. The source still checks the physical shipout
counter and will insert a visibly labeled leaf if later layout changes make
one necessary.

The companions begin their C decks on physical page 1 and their P decks on
page 9; the sung companions begin their action decks on page 17. Thus every
companion opens with a front, every subsequent deck also begins on an odd
page, and every PDF ends with its corresponding back. There is no cover,
instruction, parity, or terminal-reference page to interfere with duplex
printing whether the companion is printed by itself or reached through the
family's catalog row.

Every card header was also checked by text extraction and full-size visual
review. The stable ID is at upper left and `Cue` or `Answer` is at upper
right; no card face contains a redundant `Card` or `Voice` label or the
retired memorization slogan. All fixed cue texts are complete. C03 and C16B,
whose appointed Epistle or Gospel ending varies by day, direct the trainer to
read the complete final sentence or verse from that day's Missal.

For every pair, source enumeration required the back grid to be the row-wise
horizontal mirror `2 1 / 4 3 / 6 5` of the front. Coordinate-aware extraction
confirmed six `Cue` headers on each front, six `Answer` headers on each back,
48 unique card IDs in each Low-Mass rendering, and 60 in each sung rendering.
Measurement of the final review rasters found the same four vertical boundary
coordinates `111, 609, 626, 1124` and the same six horizontal boundary
coordinates `109, 539, 555, 984, 1001, 1430` pixels on both faces of all 56
rendered pairs: a front/back border delta of zero pixels at the review
resolution.

After page furniture and the final companion colophon were excluded, text
extraction from every companion card page matched the corresponding
full-guide card page. The comparison covered all 56 companion pages. This
establishes card-text equivalence while allowing normal font-subsetting and
raster-hinting differences between separately built PDFs.

The complete three-guide card run now uses 28 duplex sheets instead of the
superseded four-up arrangement's 37. That saves nine physical sheets and 18
printed card sides while increasing each complete sheet face from four cards
to six.

The complete guides still total 131 PDF pages instead of the superseded
38/60/62-page layout's 160, a reduction of 29 pages without reducing the card
inventory or removing the complete ceremonial chronologies. The standalone
companions add 56 installed pages, but a family printing only cards now opens
a 16-, 20-, or 20-page file containing no non-card leaf.

## Installed identity

The reviewed files are installed at:

- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/01-low-mass.pdf`
- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/01-low-mass-cue-cards.pdf`
- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata.pdf`
- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards.pdf`
- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass.pdf`
- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards.pdf`

Each installed file is byte-for-byte identical to its reviewed build and has
the SHA-256 recorded above.

## Release state

Technical completion and installation do not authorize public distribution.
All six entries remain `hold` in `release/public-alpha.json`, with null
approval. Each companion inherits the same release boundary as its matching
full guide. The recorded gates are work-specific rights review, a
distribution basis for incorporated liturgical text, independent
server-guide review, and renewed authorization of the exact PDF snapshot.
The independent review must include liturgical and ceremonial accuracy,
Ecclesiastical-Latin pronunciation, age-appropriate pedagogy, rights, and
ecclesiastical suitability.

The public-alpha policy check therefore fails closed on the changed hashes of
`README.md`, `LIBRARY.md`, and `library/traditional-latin-mass.md`. The earlier
authorization and its approved site-source hashes were deliberately left
unchanged; clearing that failure requires the recorded renewed-snapshot gate,
not a mechanical hash update.
