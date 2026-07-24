# Flash-card manifest

This manifest owns the physical-card selection and pairing audit for the 1962
altar-server series. The Low-Mass redesign and the two sung-form companions
have intentionally different contracts. A card layout does not own the
received Latin, pronunciation, meaning, or ceremonial action it renders.

## Publication families and historical boundary

| Card publication | Current selection | Layout |
| --- | --- | --- |
| `01-low-mass-flash-cards` | Twenty-two Low-Mass verbal cue-to-response pairs; no action cards | Eight-up, two columns by four rows, three long-edge duplex sheets |
| `02-missa-cantata-cue-cards` | Twenty-four integrated R response cards followed by twelve MC action cards | Six-up, two columns by three rows, six long-edge duplex sheets |
| `03-solemn-mass-cue-cards` | Twenty-four integrated R response cards followed by twelve SO action cards | Six-up, two columns by three rows, six long-edge duplex sheets |

The redesigned Low-Mass publication replaces the source identity and product
label `01-low-mass-cue-cards`. That earlier companion selected the same
twenty-four-card R response deck used by the sung forms and produced an
eight-page, six-up PDF. Its source, production, installed-hash, and
exact-snapshot records remain historical evidence about that immutable
artifact. They do not control or release the new twenty-two-card deck.

The Missa Cantata and Solemn Mass selections and publication names are
unchanged. Their installed production results remain historical evidence for
those exact bytes. The current sources use the established dense answer layout
for R08B so that its continuation note remains safely inside the cut border;
the resulting companions are separate uninstalled candidates.

## Owned card families

| Stable audit range | Owner source | Front data | Back data | Rendered by |
| --- | --- | --- | --- | --- |
| LM-F01--LM-F22; visible numbers `01`--`22` | Physical selection in `01-low-mass-flash-cards/main.tex`, reconciled below with `response-inventory.md`; canonical answers imported from `shared/response-reference.tex` | Visible number, `PRIEST`, `LOW MASS`, stage, and one complete cue or checked exemplar | Same number, `BOTH`, `LOW MASS`, same stage, and the complete canonical response in bold | Low Mass flash-card companion only |
| R01--R07, R08A--R08C, R09--R22 | `shared/response-reference.tex`, governed by the response inventory and pronunciation audit | Rendered R ID, form marker, `Cue`, and complete practice cue | Rendered R ID, form marker, `Answer`, canonical response, learner line, sound line, meaning, bank/chunk ID, and necessary condition | Missa Cantata and Solemn Mass cue-card companions |
| MC-A01--MC-A12 | `shared/missa-cantata-action-cards.tex`, governed by the ceremonial inventory | Form, role or roles, concrete cue, and direct practice question | Direct action sequence and branch; supporting MC IDs only in the trainer-reference footer | Missa Cantata cue-card companion |
| SO-A01--SO-A12 | `shared/solemn-action-cards.tex`, governed by the ceremonial inventory | Form, role or roles, concrete cue, and direct practice question | Direct action sequence and branch; supporting SO IDs only in the trainer-reference footer | Solemn Mass cue-card companion |

LM-F is an audit namespace. The Low-Mass face prints only its two-digit number
because the surrounding header already supplies `LOW MASS`. The publication
ID plus visible number uniquely identifies the physical pair.

## Low-Mass content contract

Every Low-Mass card contains exactly one priest cue and the response that Both
acolytes give. The front uses the full fixed formula where possible. When a
proper reading varies, it uses one complete, facsimile-checked exemplar and
the books explain that it is an exemplar rather than the universal text. A
response class that recurs has one selected cue rather than duplicate cards.

| Audit / visible ID | Stage | Response bank | Front cue |
| --- | --- | --- | --- |
| LM-F01 / 01 | `FOOT/ALTAR` | A1 | *Introibo ad altare Dei.* |
| LM-F02 / 02 | `FOOT/ALTAR` | A2 | Complete *Iudica me, Deus … erue me* verse |
| LM-F03 / 03 | `FOOT/ALTAR` | A3 | Complete *Emitte lucem tuam … tabernacula tua* verse |
| LM-F04 / 04 | `FOOT/ALTAR` | A4 | Complete *Confitebor tibi … conturbas me* verse |
| LM-F05 / 05 | `FOOT/ALTAR` | A5 | *Gloria Patri, et Filio, et Spiritui Sancto.* |
| LM-F06 / 06 | `FOOT/ALTAR` | A6 | *Adiutorium nostrum in nomine Domini.* |
| LM-F07 / 07 | `FOOT/ALTAR` | A7 | Complete final *Ideo precor … Dominum Deum nostrum* sentence of the priest's *Confiteor* |
| LM-F08 / 08 | `FOOT/ALTAR` | A9 | First *Misereatur vestri … vitam aeternam* occurrence |
| LM-F09 / 09 | `FOOT/ALTAR` | A10 | *Deus, tu conversus vivificabis nos.* |
| LM-F10 / 10 | `FOOT/ALTAR` | A11 | *Ostende nobis, Domine, misericordiam tuam.* |
| LM-F11 / 11 | `FOOT/ALTAR` | A12 | *Domine, exaudi orationem meam.* |
| LM-F12 / 12 | `FOOT/ALTAR` | A13 | *Dominus vobiscum.* |
| LM-F13 / 13 | `READINGS` | A14 | *Kyrie, eleison.* |
| LM-F14 / 14 | `READINGS` | A14 | *Christe, eleison.* |
| LM-F15 / 15 | `READINGS` | A15 | Complete final sentence of the Fifth Sunday after Pentecost Epistle |
| LM-F16 / 16 | `READINGS` | A16 | *Sequentia sancti Evangelii secundum Matthaeum.* |
| LM-F17 / 17 | `READINGS` | A17 | Complete final verse of the Fifth Sunday after Pentecost Gospel |
| LM-F18 / 18 | `OFFERTORY` | A18 | Complete *Orate, fratres … Deum Patrem omnipotentem* formula |
| LM-F19 / 19 | `CANON` | A19 | *Sursum corda.* |
| LM-F20 / 20 | `CANON` | A20 | *Gratias agamus Domino Deo nostro.* |
| LM-F21 / 21 | `COMMUNION` | A21 | *Et ne nos inducas in tentationem.* |
| LM-F22 / 22 | `ENDING` | A22 | *Ite, missa est, alleluia, alleluia.* |

LM-F08 is the selected exemplar for the repeated A9 *Amen* class; LM-F12 for
the repeated A13 class; and LM-F15 for the A15 *Deo gratias* class. LM-F13 and
LM-F14 are the two priest-to-server pair types within the one audited A14
ninefold pattern.

A8 is intentionally absent. Its complete servers' *Confiteor* is taught in a
three-page phrase ladder in the child booklet and page-matched trainer manual.
Compressing it onto one eight-up card would violate the complete-response and
fixed-type contracts; splitting it into detached physical fragments would
violate the one-cue/one-response contract.

Every Low-Mass back imports only the canonical answer. The deck prints no
learner syllables, sound line, IPA, meaning, action, exercise, score, mastery
field, or self-certification. All backs say `BOTH`; `FIRST` and `SECOND` are
reserved for a future card only if its response is genuinely assigned that
way.

## Low-Mass face and print contract

All pages are US-letter portrait, black ink on white paper, printed two-sided
at actual size and flipped on the long edge. Each face uses a two-column by
four-row grid. Body type is fixed at 11.5-point Atkinson Hyperlegible Next
2.001 and may not shrink. Cues are regular, responses bold, and both are
top-aligned.

The three header zones are:

- front: left `NUMBER · PRIEST`, center `LOW MASS`, right `STAGE`;
- back: left `NUMBER · BOTH`, center `LOW MASS`, right the same `STAGE`.

No actor field is repeated in the body. Card borders are the cut borders.
Print hints remain outside the card borders. The inherited revision and
rights notice occupies unused space below the final back grid and may not
create a page or enter a cut card.

### Low-Mass duplex map

| Sheet pair / physical pages | Front grid, top to bottom | Mirrored back grid, top to bottom |
| --- | --- | --- |
| 1 / 1--2 | 01 02 / 03 04 / 05 06 / 07 08 | 02 01 / 04 03 / 06 05 / 08 07 |
| 2 / 3--4 | 09 10 / 11 12 / 13 14 / 15 16 | 10 09 / 12 11 / 14 13 / 16 15 |
| 3 / 5--6 | 17 18 / 19 20 / 21 22 / unused unused | 18 17 / 20 19 / 22 21 / unused unused |

The two final unused front cells and their corresponding back cells have no
border, label, filler message, crop box, or decorative mark. The first front
is physical PDF page 1; each later sheet front is likewise odd. There is no
cover, contents, instruction, actor key, lesson, assessment, parity leaf, or
terminal-reference page.

## Unchanged sung-form contract

The sung response cards remain in six learning groups:

1. R09, R13, R15.
2. R16, R17, R19, R20, R21.
3. R01, R06, R10, R11, R12.
4. R02, R03, R04, R05.
5. R07, R08A, R08B, R08C, R18.
6. R14, R22.

Their row-wise six-up duplex order remains:

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

The response run occupies physical pages 1--8 in each sung companion. The
action deck begins on page 9 and ends on page 12. The first response front and
each later sheet front remain on an odd physical page. Their full-guide actor,
branch, safety, lesson, and use keys remain unchanged.

The MC and SO action decks continue to summarize their numbered
chronologies; they do not create independent ceremonial routes.

## Verification state

The Low-Mass source map accounts for twenty-two fronts, twenty-two mirrored
backs, six populated positions on the final sheet, and two wholly unused
positions. The current installed evaluation companion has six US-letter pages.
Automated and screen checks confirm the 22/22 content count, odd-front parity,
mirrored electronic grid, fixed font identity and size, extracted text,
consistent headers, cell containment, and blank unbordered final positions.
Those results and the exact PDF hash are recorded in
`production-manifest.md`.

Actual-size reader legibility, physical long-edge duplex overlay or equivalent
cut-and-turn alignment, and black-and-white photocopy and cut-safety tests
remain pending. After those limits were disclosed, the maintainer expressly
authorized installation of the exact companion for evaluation.
Installation does not complete the pending checks, and the companion is not
release-authorized.

The production manifest's earlier six-up R-deck and action-deck results remain
historical evidence for their named PDFs. They must not be silently reused as
verification of the redesigned Low-Mass companion or the corrected sung-form
card candidates.

The current uninstalled sung-form companions retain the same twelve-page
front/back maps, card selections, form markers, and mirrored grid geometry.
Rendered review confirms that the denser R08B answer preserves every verbal
field while restoring a safe inset for the continuation note on page 8. The
electronic pairing, border alignment, and full-size screen checks pass; the
physical actual-size, duplex, photocopy, and cut tests remain pending.
