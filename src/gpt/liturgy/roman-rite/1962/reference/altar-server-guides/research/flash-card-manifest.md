# Flash-card manifest

This manifest defines the paired-publication card contract. Each full training
guide owns the printing, actor and form, branch, and safety key and points to
the paired catalog row. A full guide renders no card faces. Its companion is a
card-face-only mechanical rendering from the same shared data and must be used
with that key.

All card pages are US-letter portrait, printed at actual size, two-sided, with
long-edge binding. Each face uses a two-column by three-row grid, so one duplex
sheet produces six cards. Each front/back sheet pair stays in generated order.
Back sheets reverse left and right positions in all three rows so the two sides
align after the long-edge turn. Cutting borders are the card borders; there are
no filler cards or blank backs.

## Owned card families

| Stable card range | Owner source | Front | Back | Rendered by |
| --- | --- | --- | --- | --- |
| R01--R07, R08A--R08C, R09--R22 | `shared/response-reference.tex`, governed by the response inventory and pronunciation audit | Rendered ID at upper left, `Cue` at upper right, and the complete spoken cue or complete verse used for practice | Rendered ID at upper left, `Answer` at upper right, canonical response, learner syllables and stress, sound line, concise meaning, bank or chunk ID, and any necessary condition | All three cards-only companions; the paired full guides supply the keys and catalog pointers but render no faces |
| MC-A01--MC-A12 | `shared/missa-cantata-action-cards.tex`, governed by the ceremonial inventory | Form, role or roles, concrete cue, and direct practice question | Direct action sequence and branch; supporting MC IDs appear only in the small trainer-reference footer | Missa Cantata cards-only companion |
| SO-A01--SO-A12 | `shared/solemn-action-cards.tex`, governed by the ceremonial inventory | Form, role or roles, concrete cue, and direct practice question | Direct action sequence and branch; supporting SO IDs appear only in the small trainer-reference footer | Solemn Mass cards-only companion |

The R range contains twenty-four integrated response cards: one for A1--A7,
three stable study chunks for A8, and one for A9--A22. It replaces the former
separate C cue deck and P pronunciation-and-meaning deck as a physical product.
The C and P designations remain historical layout and audit evidence; retiring
them from selection does not erase the checked response, cue, normalization,
pronunciation, meaning, or source records they drew from.

Each companion adds a compact form marker to the visible ID: for example,
`R09 · LOW`, `R09 · MC`, or `R09 · SOLEMN`. The stable underlying ID remains
R09. This marker prevents independently cut form-specific decks from being
silently mixed. Action IDs already carry their form marker.

## Integrated response-card contract

The R-card front and back are one audited physical pair. The front gives the
entire response-triggering formula or verse selected for practice, not an
isolated final word, ellipsis, or direction to supply the missing cue orally.
Where the appointed Epistle or Gospel ending varies, use a complete
facsimile-checked practice ending and identify it as an example rather than as
the universal proper text. The selected form's actor and mode rule remains in
the paired full guide's card key; a condition that changes whether the answer
is made remains on the affected face.

The back consolidates the canonical answer with its learner syllables and
stress, consistent English-like sound line, and concise meaning. Received
Latin, displayed normalization, pronunciation analysis, respelling, and
project-written meaning remain distinct data layers with their existing
owners. Combining those layers on one face creates no new received text and
does not make the card layout an independent pronunciation or translation
source. A competent human listener remains necessary for pronunciation
mastery.

Each face puts only the rendered ID at upper left and `Cue` or `Answer` at
upper right. It does not print the generic word `Card`, a repeated `Voice`
field, or a repeated recall slogan.

## Lesson-group order and duplex map

Response cards follow the six learning groups rather than numerical order:

1. R09, R13, R15.
2. R16, R17, R19, R20, R21.
3. R01, R06, R10, R11, R12.
4. R02, R03, R04, R05.
5. R07, R08A, R08B, R08C, R18.
6. R14, R22.

The required row-wise duplex order is:

| Sheet pair | Front grid | Mirrored back grid |
| --- | --- | --- |
| Response 1 | R09 R13 / R15 R16 / R17 R19 | R13 R09 / R16 R15 / R19 R17 |
| Response 2 | R20 R21 / R01 R06 / R10 R11 | R21 R20 / R06 R01 / R11 R10 |
| Response 3 | R12 R02 / R03 R04 / R05 R07 | R02 R12 / R04 R03 / R07 R05 |
| Response 4 | R08A R08B / R08C R18 / R14 R22 | R08B R08A / R18 R08C / R22 R14 |
| Missa Cantata 1 | MC-A01 MC-A02 / MC-A03 MC-A04 / MC-A05 MC-A06 | MC-A02 MC-A01 / MC-A04 MC-A03 / MC-A06 MC-A05 |
| Missa Cantata 2 | MC-A07 MC-A08 / MC-A09 MC-A10 / MC-A11 MC-A12 | MC-A08 MC-A07 / MC-A10 MC-A09 / MC-A12 MC-A11 |
| Solemn 1 | SO-A01 SO-A02 / SO-A03 SO-A04 / SO-A05 SO-A06 | SO-A02 SO-A01 / SO-A04 SO-A03 / SO-A06 SO-A05 |
| Solemn 2 | SO-A07 SO-A08 / SO-A09 SO-A10 / SO-A11 SO-A12 | SO-A08 SO-A07 / SO-A10 SO-A09 / SO-A12 SO-A11 |

## Odd-start companion map

The first integrated-response front is physical PDF page 1 and its mirrored
back is page 2. The twenty-four six-up response cards occupy four consecutive
duplex sheet pairs. In each sung-form companion, the twelve action cards begin
on the next odd page and occupy two further duplex sheet pairs. No cover,
instruction, actor key, lesson, parity leaf, or terminal apparatus precedes or
interrupts the faces. The compact required revision and rights notice stays
below the cut grid on the final back and adds no page.

The final builds verify the following physical ranges:

| Companion | Response faces | Action faces |
| --- | --- | --- |
| Low Mass | physical pages 1--8 | none |
| Missa Cantata | physical pages 1--8 | physical pages 9--12 |
| Solemn Mass | physical pages 1--8 | physical pages 9--12 |

Production review confirmed physical parity, page extent, form markers, row
mirroring, cut-border alignment, full-size legibility, and installed-artifact
identity. Exact hashes, sizes, and review results are recorded in the
production manifest.

## Action-card boundaries

The Missa Cantata action deck covers the MC entrance-to-exit chain, Gospel
candles, four incense visits, the concurrent Offertory and Lavabo routes,
torches, voice tracks, the 1962 Communion checkpoint, missed-cue recovery, the
proper-text Gospel genuflection, the alternate lesson route, the
procession-linked *Benedicamus* branch, and the third-Christmas Last-Gospel
omission. Cards MC-A09--MC-A12 supply the last four of those checks.

The Solemn Mass action deck covers complete role chains, the Gospel group, the
boat and thurible lifecycles, concurrent Offertory and Lavabo routes, torches
and elevations, terminal-day and reservation branches, the seven-scene
rehearsal, the pre-Mass branch call, the acolytes' pax-to-reset chain, and a
partner handoff, recovery, and safe-finish drill. Cards SO-A09--SO-A12 supply
the last four of those checks. Action cards summarize the numbered chronology;
they do not create an independent ceremonial route.

This manifest preserves the existing source and audit distinctions while
changing the physical selection and composition contract. Exact rebuilt page
counts, completed alignment results, PDF identities, and release status remain
production-record facts recorded in `production-manifest.md`.
