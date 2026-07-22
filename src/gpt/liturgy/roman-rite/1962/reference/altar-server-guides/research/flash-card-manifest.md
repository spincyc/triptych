# Flash-card manifest

All card pages are US-letter portrait, printed at actual size, two-sided, with
long-edge binding. Each face uses a two-column by three-row grid, so one duplex
sheet produces six cards. Each front/back sheet pair stays in generated order.
Back sheets reverse left and right positions in all three rows so the two sides
align after the long-edge turn. Cutting borders are the card borders; there
are no filler cards or blank backs.

| Card range | Owner source | Front | Back | Selected by |
| --- | --- | --- | --- | --- |
| C01--C13, C14A--C14C, C15, C16A--C16B, C17, C18A--C18B, C19--C20 | shared/response-reference.tex | Stable ID at upper left, Cue at upper right, and every fixed formula or verse in full; variable-reading cards require the trainer to read the complete appointed ending | Stable ID at upper left, Answer at upper right, canonical response, learner sound line, bank ID, and any condition needed to prevent a false response | All three full guides and all three cue-card companions |
| P01--P07, P08A--P08C, P09--P22 | shared/response-reference.tex | Stable ID at upper left, Cue at upper right, canonical Latin, and bank ID | Stable ID at upper left, Answer at upper right, syllables and stress, English-like sound line, short meaning, and bank ID | All three full guides and all three cue-card companions |
| MC-A01--MC-A12 | shared/missa-cantata-action-cards.tex | Form, role, cue, or branch question | Role, linked MC action IDs, action sequence, branch, and next state | Missa Cantata full guide and companion |
| SO-A01--SO-A12 | shared/solemn-action-cards.tex | Form, role, cue, or branch question | Role, linked SO action IDs, action sequence, branch, and next state | Solemn Mass full guide and companion |

There are 72 distinct cards in the owner sources: 24 cue-to-response cards,
24 Latin-to-pronunciation-and-meaning cards, twelve Missa-Cantata action
cards, and twelve Solemn-Mass action cards. A Low-Mass copy selects 48 cards
on eight duplex sheets. Each sung guide selects 60 cards on ten duplex sheets.
Across one copy of each form's card selection, a complete print run is
therefore 28 duplex sheets, nine fewer than the superseded four-up
arrangement's 37 sheets. The three companions reproduce those same 28 pairs;
they add no distinct card or sheet design.

## Odd-start print ranges

Each full guide gives one shared printing and actor key, followed by all
selected decks consecutively. Every deck has an even page count. The first
front begins on an odd physical page and each later deck also begins on an odd
page without another instruction leaf. Every advertised range ends on an even
back page and excludes the shared key. A range-only job and a whole-guide job
therefore both begin each deck with its front.

Each cards-only companion is a mechanically composed parallel rendering from
the same source, not a self-contained trainer. It omits the cover and key,
begins with the C front on physical page 1, and must be used with the matching
full guide's printing and actor key. Because every selected deck has an even
page count, later fronts begin on physical pages 9 and, in the sung companions,
17 without a parity leaf. The required revision and rights notice is below the
final back's cut grid and adds no page.

The source checks the physical shipout counter immediately before the first
deck and inserts a visibly labeled parity leaf only when needed. In the exact
reviewed builds, the shared key itself ends on an even physical page, so no
extra parity leaf was generated.

| Guide and deck | Advertised numbered pages | Physical PDF pages | Page immediately before first deck |
| --- | --- | --- | --- |
| Low Mass C | 13--20 | 15--22 | physical 14, shared card key |
| Low Mass P | 21--28 | 23--30 | none; follows the even C back |
| Missa Cantata C | 27--34 | 29--36 | physical 28, shared card key |
| Missa Cantata P | 35--42 | 37--44 | none; follows the even C back |
| Missa Cantata action | 43--46 | 45--48 | none; follows the even P back |
| Solemn Mass C | 29--36 | 31--38 | physical 30, shared card key |
| Solemn Mass P | 37--44 | 39--46 | none; follows the even C back |
| Solemn Mass action | 45--48 | 47--50 | none; follows the even P back |
| Low Mass companion C | 1--8 | 1--8 | document begins with the front |
| Low Mass companion P | 9--16 | 9--16 | none; follows the even C back |
| Missa Cantata companion C | 1--8 | 1--8 | document begins with the front |
| Missa Cantata companion P | 9--16 | 9--16 | none; follows the even C back |
| Missa Cantata companion action | 17--20 | 17--20 | none; follows the even P back |
| Solemn Mass companion C | 1--8 | 1--8 | document begins with the front |
| Solemn Mass companion P | 9--16 | 9--16 | none; follows the even C back |
| Solemn Mass companion action | 17--20 | 17--20 | none; follows the even P back |

Physical parity was checked after the exact final build; logical numbering
was not used as a substitute for that check. Every first deck page is odd in
both numbering systems, and every subsequent front is on an odd physical
page.

## Response and pronunciation decks

The C deck renders from the same A1--A22 response bank used by the lessons,
Mass-order consolidation, pronunciation entries, and memorization drills. The
form-specific actor and mode rule appears once in the full guide's shared key
immediately before the decks; each companion relies on that paired key, and
individual faces do not repeat a Voice field. Conditions
that change whether an answer is made remain on the affected face, so the
cards do not turn a choir, public, or sacred-minister response into an
automatic lay-server response.

Every fixed C cue is complete. C02 prints four complete fixed Amen formulas;
C03 prints both dismissals and John 1:14 in full; C05--C07 print the complete
Psalm verses; C10 prints the celebrant's complete Confiteor; C11--C13 print
the complete preceding exchange or study chunk; C15 prints the full practice
pattern; and C16A spells out complete Gospel-title announcements. C03 and
C16B cannot print a universal proper-reading ending, so they require the
trainer to read the complete final sentence or verse from that day's Missal.
The former composite cards are retired. C14A--C14C, C16A--C16B, and
C18A--C18B each train one response point; C20 uses A22 directly.

The P deck renders P01--P07, the three A8 study parts P08A--P08C, and
P09--P22. The front asks the learner to read canonical Latin and name its bank
ID. The back supplies learner syllables and stress, an English-like sound
line, a short meaning, and the bank ID. Broad IPA and the form-specific actor
rule remain in the A-bank and shared card key rather than being repeated on
the face. P08A--P08C remain one response, A8.

## Action decks

The Missa Cantata deck covers the MC entrance-to-exit chain, Gospel candles,
four incense visits, the concurrent Offertory and Lavabo routes, torches,
voice tracks, the 1962 Communion checkpoint, missed-cue recovery, the proper-
text Gospel genuflection, the alternate lesson route, the procession-linked
*Benedicamus* branch, and the third-Christmas Last-Gospel omission. Cards
MC-A09--MC-A12 supply the last four of those checks.

The Solemn deck covers complete role chains, the Gospel group, the boat and
thurible lifecycles, concurrent Offertory and Lavabo routes, torches and
elevations, terminal-day and reservation branches, the seven-scene rehearsal,
the pre-Mass branch call, the acolytes' pax-to-reset chain, and a partner
handoff/recovery/safe-finish drill. Cards SO-A09--SO-A12 supply the last four
of those checks. Action cards summarize the numbered chronology; they do not
create an independent ceremonial route.

## Audited duplex map

The following is the generated order. Each back is the row-wise horizontal
mirror of its front.

| Sheet pair | Front grid | Mirrored back grid |
| --- | --- | --- |
| Response 1 | C01 C02 / C03 C04 / C05 C06 | C02 C01 / C04 C03 / C06 C05 |
| Response 2 | C07 C08 / C09 C10 / C11 C12 | C08 C07 / C10 C09 / C12 C11 |
| Response 3 | C13 C14A / C14B C14C / C15 C16A | C14A C13 / C14C C14B / C16A C15 |
| Response 4 | C16B C17 / C18A C18B / C19 C20 | C17 C16B / C18B C18A / C20 C19 |
| Pronunciation 1 | P01 P02 / P03 P04 / P05 P06 | P02 P01 / P04 P03 / P06 P05 |
| Pronunciation 2 | P07 P08A / P08B P08C / P09 P10 | P08A P07 / P08C P08B / P10 P09 |
| Pronunciation 3 | P11 P12 / P13 P14 / P15 P16 | P12 P11 / P14 P13 / P16 P15 |
| Pronunciation 4 | P17 P18 / P19 P20 / P21 P22 | P18 P17 / P20 P19 / P22 P21 |
| Missa Cantata 1 | MC-A01 MC-A02 / MC-A03 MC-A04 / MC-A05 MC-A06 | MC-A02 MC-A01 / MC-A04 MC-A03 / MC-A06 MC-A05 |
| Missa Cantata 2 | MC-A07 MC-A08 / MC-A09 MC-A10 / MC-A11 MC-A12 | MC-A08 MC-A07 / MC-A10 MC-A09 / MC-A12 MC-A11 |
| Solemn 1 | SO-A01 SO-A02 / SO-A03 SO-A04 / SO-A05 SO-A06 | SO-A02 SO-A01 / SO-A04 SO-A03 / SO-A06 SO-A05 |
| Solemn 2 | SO-A07 SO-A08 / SO-A09 SO-A10 / SO-A11 SO-A12 | SO-A08 SO-A07 / SO-A10 SO-A09 / SO-A12 SO-A11 |

Source-level enumeration accounts for all 24 C, 24 P, 12 MC, and 12 SO
front/back IDs exactly once, and every back order matches the map. The final
production audit records the rendered border measurements, page ranges, and
all 56 selected sheet-pair renderings across the six PDFs in
`production-manifest.md`.
