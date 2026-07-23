# Production manifest: 1962 altar-server guides

Audit date: 2026-07-22 (America/Chicago). All six publications carry the
revision timestamp `2026-07-23T02:31:26Z`.

## Exact reviewed and installed builds

All six publications were built as US-letter portrait PDFs with pdfTeX
1.40.29 from TeX Live 2026. The installed files are byte-for-byte identical to
the reviewed builds.

| Publication | Pages | Physical cards | Bytes | SHA-256 |
| --- | ---: | ---: | ---: | --- |
| 01-low-mass | 15 | 0 | 571,087 | `bfed57816157141c676b6bf8e460e13d53696a14dc76d159a5c9b7cf5df35009` |
| 01-low-mass-cue-cards | 8 | 24 | 430,042 | `2ee877985ecaa737ee62a3d8cfe2c87858c2a7526b626fbcc28eefe4dbcfb12e` |
| 02-missa-cantata | 29 | 0 | 668,985 | `09c14200921ff31fe72aff9ee7de20370241f104de3d59c00c641fadd71eeaff` |
| 02-missa-cantata-cue-cards | 12 | 36 | 474,866 | `29dcbd0390872b3474f26b5096907730bb856ddfb360dbd1f5cb3a43b0a488b2` |
| 03-solemn-mass | 31 | 0 | 681,161 | `c00ddb2319aa14b703c24655f28d36de4e36434e6c98fde651d65c1e65e4ec63` |
| 03-solemn-mass-cue-cards | 12 | 36 | 479,127 | `725b02f8f11dbcc2dd350c95cea8ea82a2626f48d7249efd07786886fb26fed7` |

The installed set is 107 pages: 75 pages of full guides and 32 pages of card
companions. The superseded paired set was 187 pages (131 guide pages and 56
companion pages), so the revision removes 80 pages, or 42.8 percent, without
removing a response, lesson, role sheet, ceremonial chronology, action card,
or audit apparatus.

The current card selection has 48 distinct owner cards: twenty-four shared
response cards, twelve Missa-Cantata action cards, and twelve Solemn-Mass
action cards. Because the shared response deck is rendered once for each
form, the three companions contain 96 physical cards in all: 72 response-card
copies and 24 action cards.

## Reader navigation and content boundary

Each full guide begins with a trainer-and-server start sheet. The Low-Mass
guide routes the learner through six short word-only lessons and contains no
ceremonial directions. Each sung guide puts an overview and individual role
sheets before the complete chronology, so a server may learn one assignment
without first reading the trainer's full sequence.

The full guide owns the actor, mode, printing, branch, safety, and consolidated
pronunciation keys. It points to the paired catalog row but does not repeat its
cards-only companion.
The companions contain only detachable card faces and a compact revision and
rights notice below the final cut grid.

The integrated R deck keeps the complete practice cue on the front. The back
places the canonical answer, learner stress line, sound line, concise meaning,
and audit ID together. R15 and R17 use complete, labeled, facsimile-checked
examples from the Fifth Sunday after Pentecost rather than an isolated final
word or an ellipsis. The actor and spoken-or-sung rule appears once in the full
guide instead of being repeated on every card.

## Technical checks

- All required build passes completed, and canonical and inherited generation
  metadata validated.
- The six current logs contain no fatal error, undefined reference, LaTeX or
  package warning, overfull box, or underfull box.
- `qpdf --check` reports no syntax or stream-encoding error in any installed
  PDF.
- `pdfinfo` confirms 15/8/29/12/31/12 pages and 612 by 792 pt US-letter
  geometry.
- Every listed font is embedded and subset, including the TIPA fonts used for
  broad IPA.
- Text extraction succeeds in all six PDFs. It finds no obsolete
  reader-role label, and no card retains the removed `Card`,
  `Voice`, or recall-slogan labels.
- Build and installed copies compare byte-for-byte; the exact installed
  identities are recorded above.

## Every-page and card review

The review tool rastered all 107 pages from the exact final PDFs. Every page
was inspected in complete-document contact sheets for order, density,
navigation, monochrome legibility, clipping, accidental blanks, split units,
and terminal-page fit. Dense guide pages, the three final pages, every card
sheet, and the response and action transitions received additional full-size
inspection. The final review found no clipping, collision, unsafe diagram,
accidental blank, broken sequence, orphan heading, or colophon overflow.

All card faces remain inside their cut borders. Print at actual size on US
letter, portrait, two-sided, flipped on the long edge. Six cards fit on each
face in two columns by three rows, and every back reverses the left-right order
of all three rows. The inspected front/back pairs have coincident borders and
no filler card or blank back.

| Companion | Response fronts | Response backs | Action fronts | Action backs | Duplex pairs |
| --- | --- | --- | --- | --- | ---: |
| 01-low-mass-cue-cards | 1, 3, 5, 7 | 2, 4, 6, 8 | none | none | 4 |
| 02-missa-cantata-cue-cards | 1, 3, 5, 7 | 2, 4, 6, 8 | 9, 11 | 10, 12 | 6 |
| 03-solemn-mass-cue-cards | 1, 3, 5, 7 | 2, 4, 6, 8 | 9, 11 | 10, 12 | 6 |

Thus every companion begins with a front on odd physical page 1. Each sung
action deck also begins with a front on odd physical page 9. The arrangement
is correct whether a companion is printed alone or opened from the same
catalog row as its full guide.

The response run has exactly twenty-four `Cue` faces and twenty-four matched
`Answer` faces per companion. Each sung companion adds twelve action cues and
twelve matched answers. Every stable ID appears once on a front and its
mirrored back. Full-size inspection confirmed that the longest response backs,
including R08A--R08C and R18, remain legible and inside their borders.

## Installed identity

The reviewed files are installed at:

- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/01-low-mass.pdf`
- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/01-low-mass-cue-cards.pdf`
- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata.pdf`
- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/02-missa-cantata-cue-cards.pdf`
- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass.pdf`
- `doc/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/03-solemn-mass-cue-cards.pdf`

## Release state

Technical completion and installation do not authorize public distribution.
At this production record's 22 July cutoff, all six entries remained `hold` in
`release/public-alpha.json`, with null approval, and each companion inherited
the same release boundary as its matching full guide. Independent liturgical
and ceremonial accuracy, Ecclesiastical-Latin pronunciation, age-appropriate
pedagogy, rights, and ecclesiastical-suitability review remain outstanding.

At that cutoff the public-alpha policy therefore failed closed for the
unapproved revision and the earlier authorization and approved site-source
hashes were unchanged. The separate 23 July 2026 exact-byte exception now
binds all six exact PDF hashes and the current recognized site inputs. It
release-clears only those immutable bytes and supplies no missing rights
analysis, review, or ecclesiastical approval.
