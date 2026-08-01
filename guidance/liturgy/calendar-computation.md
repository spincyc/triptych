# Roman Calendar Computation

This file owns the recurring calendar arithmetic used across the liturgy collections: the movable anchors, the Sunday and weekday Lectionary cycles, postconciliar Ordinary Time numbering, and the 1962 Epiphany-and-Pentecost Sunday mechanism. Under the one-authoritative-source rule in [repository rules](../repository.md), every other profile, registry, publication, and tracked record references these rules rather than restating them; a rule that changes changes here first.

It is not a genre profile. [Roman calendar references](roman-calendar-references.md) governs published calendar histories and inventories; [the 1962 proper-guide profile](roman-1962-propers.md), [the 1962 assembly profile](roman-1962-assembly.md), [the postconciliar proper-guide profile](postconciliar-propers.md), and [the postconciliar proper registry](postconciliar-propers-registry.md) govern their own documents. Each must agree with this file, and a published calendar reference that disagrees is corrected here or there, never left divergent.

Computation is a finding aid, never an authority. The competent General, territorial, diocesan, religious, parish, and church calendar, the approved books, and the competent annual Ordo control an actual celebration. Compute, then verify against a dated official witness, record both in the tracked instance record, and fail closed on disagreement: state the divergence and resolve nothing by preference. Never publish a computed date as its own occurrence witness, and never compute a territorial transfer — Epiphany, Ascension, and the Body and Blood of Christ move only by the competent authority's actual decision.

## Fixed anchors

- The liturgical year turns at the **First Sunday of Advent**. The Universal Norms nowhere say so in one sentence; the boundary is compounded from no. 40, where Advent "begins with Evening Prayer I of the Sunday falling on or closest to 30 November," and no. 44, where Ordinary Time "ends before Evening Prayer I of the First Sunday of Advent." The General Introduction to the Lectionary states it directly at its note to no. 66.2: each cycle "begins with the First Week of Advent, which falls in the preceding year of the civil calendar." That Sunday is the fourth before December 25 and falls November 27 through December 3; the two formulations agree in every year from 1900 to 2100. Every cycle, count, and year label below turns on it, not on January 1.
- Universal Norms 6 permanently assigns four Sundays: the Sunday within the Octave of Christmas to the Holy Family, the Sunday after January 6 to the Baptism of the Lord, the Sunday after Pentecost to the Most Holy Trinity, and the last Sunday in Ordinary Time to Christ the King. Universal Norms 7 assigns the Epiphany, the Ascension, and the Body and Blood of Christ to a Sunday only where they are not observed as holy days of obligation — a decision of the competent authority, never a computation.
- **Easter** is the Sunday after the first ecclesiastical full moon falling on or after March 21, by the Gregorian computus. Do not approximate it, and do not carry an astronomical full moon into the ecclesiastical rule.
- Derive the remaining movable anchors from Easter by fixed offsets in days:

| Day | Offset from Easter | Note |
| --- | ---: | --- |
| Septuagesima | −63 | Sunday; 1962 only |
| Ash Wednesday | −46 | Wednesday |
| Ascension, Thursday form | +39 | The fortieth day of Easter |
| Ascension, transferred Sunday form | +42 | Only where the competent authority actually transfers it |
| Pentecost | +49 | Sunday |
| Trinity Sunday | +56 | Sunday after Pentecost |
| Body and Blood of Christ, Thursday form | +60 | Thursday after Trinity |
| Body and Blood of Christ, transferred Sunday form | +63 | Only where the competent authority actually transfers it, as in the United States |

Worked anchors, checked against the Gregorian computus:

| Civil year | Easter | Ash Wednesday | Septuagesima | Pentecost | Trinity | First Sunday of Advent | Sunday before Advent |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 2024 | March 31 | February 14 | January 28 | May 19 | May 26 | December 1 | November 24 |
| 2025 | April 20 | March 5 | February 16 | June 8 | June 15 | November 30 | November 23 |
| 2026 | April 5 | February 18 | February 1 | May 24 | May 31 | November 29 | November 22 |
| 2027 | March 28 | February 10 | January 24 | May 16 | May 23 | November 28 | November 21 |
| 2028 | April 16 | March 1 | February 13 | June 4 | June 11 | December 3 | November 26 |

## Ember Days, Litanies and the Sacred Heart

These belong to the 1962 calendar, and they get their own tables here because the table of movable anchors above is the wrong shape for most of them. That table is offsets from Easter, and three of these days have no such offset: the Ember Days of Advent follow the Third Sunday of Advent, which is fixed by the Advent boundary; the Ember Days of September follow the third Sunday of September; and the greater Litanies keep a civil date. The interval from Easter to Advent is not constant, so an Easter offset for the Advent Ember Days cannot be written at all, and one written anyway would be arithmetic that only looked like a rule. State each day on the anchor its own source names, and derive nothing further.

### The four Ember weeks

The 1960 code names the Ember Days in four places and never dates them: general rubric 24 b makes the Ember ferias of Advent, of Lent and of September second-class ferias, rubric 109 d makes the September commemoration privileged, and rubrics 127–128 except the September days from green. The Ember Days of Pentecost are named in none of those lists because rubric 66 has already made every day within that octave first class. The tracked rubric registry carries the same rows at `src/sources/calendars/roman-1962/rubrics.yaml` lines 98–99 and 756.

The date rule is not in the code but in the Missal's own front matter, in the note *De anno et eius partibus*. The repository's tracked 1962 calendar reference quotes it at `src/claude/liturgy/roman-rite/1962/reference/liturgical-calendar/sections/30-vigils-octaves-ember-rogation.tex` lines 121–133: "Quatuor Tempora celebrantur quarta et sexta feria ac sabbato post tertiam dominicam Adventus, post primam dominicam Quadragesimae, post dominicam Pentecostes, post dominicam tertiam septembris" — the Ember Days are celebrated on the Wednesday, Friday and Saturday after the Third Sunday of Advent, after the First Sunday of Lent, after Pentecost Sunday, and after the third Sunday of September. The same four positions are given at `src/gpt/liturgy/roman-rite/1962/reference/liturgical-calendar/sections/40-temporale.tex` line 66, which agrees on Advent, Lent and Pentecost and diverges on September; that divergence is recorded below.

One sentence dates all four weeks, and it dates each of them the same way: three fixed offsets from a Sunday, with only the Sunday changing. Write it that way and nothing is restated — the offsets are one row of arithmetic used four times, and no week carries a private copy of them:

| Ember week | The Sunday it follows | Wednesday | Friday | Saturday | Class |
| --- | --- | ---: | ---: | ---: | ---: |
| Advent | Third Sunday of Advent (First Sunday of Advent +14) | +3 | +5 | +6 | II |
| Lent | First Sunday of Lent (Easter −42) | +3 | +5 | +6 | II |
| Pentecost | Pentecost Sunday (Easter +49) | +3 | +5 | +6 | I |
| September | third Sunday of September (September 15–21) | +3 | +5 | +6 | II |

Two of the four anchors are Easter-based, so for those two the row reduces to offsets from Easter — the Lenten Ember Days to Easter −39, −37 and −36, those of Pentecost to Easter +52, +54 and +55. Those reductions are derived from this table and are deliberately not copied into the table of movable anchors above, because a second written copy is what drifts. The Advent and September weeks reduce to no offset from Easter at all, which is the whole reason this section exists.

"The third Sunday of September" is reckoned by general rubric 19, which fixes the first Sunday of a month as the one occurring first in it, that is falling from the first to the seventh day, and repeats the rule for September expressly; it is quoted at `src/claude/liturgy/roman-rite/1962/reference/liturgical-calendar/sections/20-temporal-cycle.tex` lines 150–153. The third Sunday of September therefore falls September 15 through 21 in every year, and the Ember Wednesday September 18 through 24 — the window that reference states independently at line 142 of its Ember section, and which the computus reproduces.

Computed across 2020–2120: Advent Ember Wednesday falls December 14–20, Friday December 16–22, Saturday December 17–23; September Ember Wednesday falls September 18–24, Friday September 20–26, Saturday September 21–27.

**The September divergence, recorded and not resolved by preference.** `40-temporale.tex` line 66 dates the September Ember week from September 14. That is the pre-1955 wording, *post Festum Exaltationis sanctae Crucis*, and the 1962 wording *post dominicam tertiam septembris* is not equivalent to it: the older rule keys the week to a fixed date and puts the Ember Wednesday as early as September 15, the newer keys it to a Sunday. The two disagree in 44 of the 101 years from 2020 to 2120. The rules above follow the 1962 wording because that is the wording of the typical edition this calendar is of, quoted in Latin from the Missal's own front matter with the pre-1955 comparison witness named — a resolution by the governing text, not a choice between two equal readings. The limit is real and is recorded at `src/claude/liturgy/roman-rite/1962/reference/liturgical-calendar/research/calendar-inventory.md` lines 145–147: the change is corroborated as a change by two independent 1960-code books, but the act that made it is not identified and the *Variationes in Calendario* do not mention the Ember Days. `40-temporale.tex` line 66 states the superseded rule and is to be corrected there, under the standing rule that a published calendar reference which disagrees is corrected here or there and never left divergent.

### The Litanies and the Sacred Heart

General rubrics 80 and 87 assign the two Litany observances, and rubrics 81 and 88 confine both to the Mass, nothing being done about either in the Office. They are quoted at `30-vigils-octaves-ember-rogation.tex` lines 148–194. One Mass formulary serves both, *in Litaniis maioribus et minoribus*.

| Observance | Rule | Locus | Window, 2020–2120 |
| --- | --- | --- | --- |
| Greater Litanies | April 25; if Easter Sunday or Easter Monday falls on it, the following Tuesday | general rubric 80 | April 25, and Easter +2 in a transferred year |
| Lesser Litanies, the Rogation days | Monday, Tuesday and Wednesday before the Ascension: Easter +36, +37, +38 | general rubric 87 | April 30 – May 31, May 1 – June 1, May 2 – June 2 |
| Most Sacred Heart of Jesus | Easter +68, the Friday after the second Sunday after Pentecost | 1962 Missal, temporal cycle | June 1 – July 2 |

The transfer of the greater Litanies is computable because rubric 80 states its own condition and its own replacement day, unlike a territorial transfer. It occurs twice in the span, in 2038 and 2095, and in both the replacement day is Easter +2, the Tuesday in the octave of Easter; both are years in which April 25 is Easter Sunday or Easter Monday.

The Rogation days carry a discretion that is not computable and must never be inferred. Rubric 87 gives local Ordinaries the faculty of transferring them "to three other continuous days more suitable according to the diversity, custom or necessity of their regions." That is a genuine transfer of a temporal observance by local authority, and it stands with the territorial transfers of Universal Norms 7: state the universal assignment, and never compute an actual one. Where the Ascension itself is kept on a day other than Easter +39, the Rogation days are not recomputed here either.

The Sacred Heart offset is attested twice and the two agree: `40-temporale.tex` line 42 gives Easter +68 with the gloss "Friday after the second Sunday after Pentecost", and `calendar-inventory.md` line 167 gives +68 as a first-class feast. The gloss and the offset are the same day in every year of the span, Pentecost being Easter +49 and the second Sunday after it Easter +63.

### Two 1962 feasts assigned to a Sunday

General rubric 17 assigns four celebrations to a Sunday outright, and two of them have no ordinal position in the temporal cycle to be reached by, so they need a rule here of their own. Both are quoted from the Missal's own front matter at `src/claude/liturgy/roman-rite/1962/reference/assembling-the-mass/sections/10-the-day.tex` lines 65–80, and named in the calendar reference at `src/claude/liturgy/roman-rite/1962/reference/liturgical-calendar/sections/60-sanctoral.tex` lines 17 and 20.

| Celebration | Rule | Locus | Window, 2020–2120 |
| --- | --- | --- | --- |
| D. N. Iesu Christi Regis | The last Sunday of October | general rubric 17 d | October 25–31, always a Sunday |
| Sanctissimi Nominis Iesu | The Sunday falling January 2–5; where no Sunday falls in that span, January 2 | general rubric 17 a | January 2–5 |

The Holy Name is the only rule in this file whose result is not always the same weekday, and that is the rule and not a defect: in 43 of the 101 years from 2020 to 2120 no Sunday falls between January 2 and January 5, and in those years the feast is kept on January 2 whatever day that is. A rule stated as "the Sunday after the Circumcision" would be wrong in exactly those 43 years.

### The three postconciliar movables

The Universal Norms fix no dates; these three are assigned in the Missal's own temporal cycle, and the repository's tracked postconciliar calendar reference carries all three at `src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/reference/liturgical-calendar/sections/50-movable.tex` lines 56, 63 and 65, corroborated at that publication's `research/calendar-inventory.md` lines 66, 70 and 71.

| Celebration | Rule | Latin | Window, 2020–2120 |
| --- | --- | --- | --- |
| Most Sacred Heart of Jesus | Easter +68 | *Feria VI post dominicam secundam post Pentecosten* | June 1 – July 2, always a Friday |
| Immaculate Heart of the Blessed Virgin Mary | Easter +69 | *Sabbato post dominicam secundam post Pentecosten* | June 2 – July 3, always a Saturday |
| Blessed Virgin Mary, Mother of the Church | Easter +50 | The Monday after Pentecost | May 14 – June 14, always a Monday |

The Sacred Heart carries the same Easter +68 in both calendars, and the two rows are stated separately rather than shared. They are different books assigning the same day, and a single row would make one calendar's rule depend on the other's, so that correcting either would silently move both.

## Sunday Lectionary cycle A, B, C

The three-year cycle and its determination are fixed by the General Introduction to the Lectionary at no. 66.2 and its note: "The letter C designates a year whose number is divisible into three equal parts… Obviously each cycle runs in accord with the plan of the liturgical year, that is, it begins with the First Week of Advent, which falls in the preceding year of the civil calendar."

Let `Y` be the civil year in which the liturgical year **ends** — the year of its January through November, which is the year the Introduction numbers, not the year of its Advent. Then:

`Y mod 3 = 1` is Year A; `Y mod 3 = 2` is Year B; `Y mod 3 = 0` is Year C.

Equivalently, the cycle beginning at the First Sunday of Advent of civil year `y` is fixed by `(y + 1) mod 3`. The cycle changes at that Sunday and nowhere else, so one civil year normally carries the end of one cycle and the beginning of the next. Record both the letter and the exact interval it governs. The Introduction's own worked series — 1980 Year C, 1981 Year A, 1982 Year B, 1983 Year C — satisfies the same arithmetic.

| Liturgical year | Interval | `Y` | `Y mod 3` | Sunday cycle |
| --- | --- | ---: | ---: | --- |
| Advent 2023 – November 2024 | 2023-12-03 – 2024-11-30 | 2024 | 2 | B |
| Advent 2024 – November 2025 | 2024-12-01 – 2025-11-29 | 2025 | 0 | C |
| Advent 2025 – November 2026 | 2025-11-30 – 2026-11-28 | 2026 | 1 | A |
| Advent 2026 – November 2027 | 2026-11-29 – 2027-11-27 | 2027 | 2 | B |

Never infer the letter from civil-year parity, from the weekday cycle, from a January date, or from a neighbouring document. A celebration whose readings are not cycle-governed records `not applicable`, not a letter.

## Weekday Lectionary cycle I and II

The General Introduction to the Lectionary at no. 69.4 fixes it: "For the thirty-four weeks of Ordinary Time, the gospel readings are arranged in a single cycle, repeated each year. But the first reading is arranged in a two-year cycle and is thus read every other year. Year I is used during odd-numbered years; Year II, during even-numbered years." Its independence is equally express at no. 65: "neither series… depends on the other. The Order of Readings for Sundays and the solemnities of the Lord extends over three years; for weekdays, over two. Thus each runs its course independently of the other."

The weekday cycle is therefore keyed to the parity of the same `Y`: odd is Cycle I, even is Cycle II. It turns at the First Sunday of Advent together with the Sunday cycle and is otherwise **independent of it**.

The two cycles have periods 3 and 2, so their pairing repeats only every six years and neither ever determines the other. Year A falls with Cycle II in the year ending 2026 and with Cycle I in the year ending 2029:

| `Y` | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sunday | B | C | A | B | C | A | B | C | A |
| Weekday | II | I | II | I | II | I | II | I | II |

Never derive `I` or `II` from a Sunday letter, never carry a Sunday letter onto a weekday, and never assign a weekday cycle to a Sunday celebration. The weekday cycle governs the Ordinary Time ferial course alone: under the same Introduction at nos. 69.2 and 69.3, Lent has its own principles and the weekdays of Advent, Christmas Time, and Easter Time repeat the same readings each year. A weekday use of a Sunday or week formulary is a separate liturgical instance with its own independently resolved weekday Lectionary path.

## Postconciliar Ordinary Time numbering

Universal Norms 43 states that "thirty-three or thirty-four weeks remain in the yearly cycle," and Universal Norms 44 fixes the boundaries: Ordinary Time "begins on Monday after the Sunday following 6 January and continues until Tuesday before Ash Wednesday inclusive. It begins again on Monday after Pentecost and ends before Evening Prayer I of the First Sunday of Advent." The Missal and Lectionary nevertheless supply thirty-four formularies and thirty-four weekday weeks, so one week's material goes unused in a thirty-three-week year.

The rule for the unused week is not in the Norms but in the General Introduction to the Lectionary at nos. 103 and 104.3. No. 103 names the displacements: "some Sundays either belong to another season (the Sunday on which the feast of the Baptism of the Lord falls and Pentecost) or else are impeded by a solemnity that coincides with Sunday (for example, Holy Trinity or Christ the King)." No. 104.3 governs the resumption: "When there are thirty-four Sundays in Ordinary Time, the week to be used is the one that immediately follows the last week used before Lent. When there are thirty-three Sundays in Ordinary Time, the first week that would have been used after Pentecost is omitted, in order to reserve for the end of the year the eschatological texts that are assigned to the last two weeks." Its notes give the worked cases: six weeks before Lent puts the seventh week on the Monday after Pentecost, while five weeks before Lent puts the seventh week there and drops the sixth. Cite that locus, not the Norms, for the omission.

Ordinary Time weeks are Sunday-first and anchored at **both** ends, and the rule below is the same rule stated as arithmetic. Do not count forward from one anchor alone.

1. **Week I** is the week in which the Baptism of the Lord falls. Under the Introduction at no. 104.1 the Baptism "replaces the first Sunday in Ordinary Time," whose readings therefore begin on the Monday after the Sunday following January 6; and "when the feast of the Baptism of the Lord is celebrated on Monday because Epiphany has been celebrated on the Sunday, the readings of the First Week begin on Tuesday." Week I therefore never has a numbered Sunday, and there is no First Sunday in Ordinary Time.
2. Under no. 104.2 the Sunday after the Baptism is the Second Sunday and the rest are numbered consecutively to the Sunday before Lent, the week containing Ash Wednesday being "suspended after the Tuesday readings." Call that last pre-Lenten week `L`.
3. **Week XXXIV** is the week whose Sunday is Our Lord Jesus Christ, King of the Universe — the Sunday before the First Sunday of Advent — and it ends on the Saturday before Advent.
4. Ordinary Time resumes on the Monday after Pentecost. The **resumed week** `R` is the week whose Sunday is Pentecost, so that its weekdays are the first to resume:

   `R = 34 − (Sunday before Advent − Pentecost) ÷ 7 weeks`

5. `R = L + 1` gives thirty-four weeks and no omission. `R = L + 2` gives thirty-three: week `L + 1` **never occurs**. Its Missal formulary, its weekday Lectionary passages, and its numbered Sunday are omitted, not transferred, anticipated, or folded into an adjacent week, so that the final eschatological weeks keep their place. Record any permission actually used to join omitted weekday passages; do not assume one.
6. Solemnities occupy the Sunday of a numbered week without erasing it. The Sunday of week `R` is Pentecost; of `R + 1`, the Most Holy Trinity; of `R + 2`, the Most Holy Body and Blood of Christ where the competent authority transfers it to Sunday, and otherwise the numbered Ordinary Time Sunday; of week XXXIV, Christ the King. The weekdays of those weeks keep their numbers and their ferial Lectionary.

| Civil year | Baptism | `L` | Pentecost | `R` | Weeks | Omitted week | First numbered Sunday after Pentecost, U.S. |
| ---: | --- | ---: | --- | ---: | ---: | ---: | --- |
| 2024 | January 8 (Monday) | 6 | May 19 | 7 | 34 | none | June 9, week X |
| 2025 | January 12 | 8 | June 8 | 10 | 33 | 9 | June 29, week XIII |
| 2026 | January 11 | 6 | May 24 | 8 | 33 | 7 | June 14, week XI |
| 2027 | January 10 | 5 | May 16 | 7 | 33 | 6 | June 6, week X |
| 2028 | January 9 | 8 | June 4 | 9 | 34 | none | June 25, week XII |

The 2026 line is corroborated by the edition's own tracked occurrence record, which resolves Trinity to the Ninth and the Body and Blood of Christ to the Tenth Sunday's date and the Eleventh Sunday to 2026-06-14, and by the United States Conference's published calendar for that year.

### Identity mapping

For `PC-S26` through `PC-S57` the Ordinary Time Sunday number and the shared formulary owner are computable and independently checkable:

`Ordinary Time Sunday = parent number − 24`, and the owner directory is `temporal/shared/ordinary-time/weeks/NN` with `NN` that Sunday number written in two digits.

`PC-S58`, `PC-S59`, and `PC-S60` are Solemnities of the Lord with their own formularies and owners; they consume no `weeks/NN` directory. Weeks 01 and 34 have no numbered Sunday consumer. The parallel Lectionary-number check, target counts, keys, and slugs remain in [the postconciliar proper registry](postconciliar-propers-registry.md).

An identity whose week is omitted in a given year, or whose Sunday is replaced by a higher celebration, keeps its permanent identity and its source work. Absence in one civil year is an occurrence result, never a target disposition and never a renumbering.

## 1962 Sunday computation

The 1962 temporal Sundays are likewise anchored at both ends of the after-Pentecost run.

- **Sundays after Epiphany** run from the Sunday following January 6 to the Sunday before Septuagesima. Their count `E` ranges from one to six. The first always occurs and carries the Feast of the Holy Family, because January 7 through 13 always contains exactly one Sunday.
- **Sundays after Pentecost** run from Trinity Sunday, which is the first, to the Sunday before the First Sunday of Advent, which is the last. Their count `P` ranges from twenty-three to twenty-eight by computation; the rubric quoted below enumerates only the twenty-five through twenty-eight cases expressly.
- The Missal prints twenty-four formularies after Pentecost, and the **last Sunday after Pentecost always uses the twenty-fourth formulary**. Where `P` exceeds twenty-four, `P − 24` formularies of the unused Sundays after Epiphany are resumed between the twenty-third and that last Sunday, as the Missal directs.
- Because `P − 24` never exceeds four, only the Third through Sixth Sundays after Epiphany are ever resumed. These are the `46R` through `49R` catalog identities in the 1962 proper-guide profile, each a separately sourced variant that joins the Epiphany orations, Epistle, and Gospel to the chants appointed for resumed use.
- The 1960 general rubrics enumerate the arrangement directly: with twenty-five Sundays the twenty-fourth place takes the Sixth after Epiphany; with twenty-six, the Fifth then the Sixth; with twenty-seven, the Fourth, Fifth, and Sixth; with twenty-eight, the Third through the Sixth. The formulary numbered twenty-fourth after Pentecost is always kept for the last place, and any Mass for which no place is found is omitted. The resumed Masses are therefore taken from the highest unused ordinal downward, and it is the lowest unused ordinal that is dropped.
- This enumeration is a **nominal fixed-slot map**. Resolve it before occurrence: n. 18 states which inscribed formulary the twenty-fourth, twenty-fifth, twenty-sixth, and twenty-seventh Sunday *will be*. A feast that wins occurrence in one of those slots displaces that slot's nominal Sunday under nn. 14 and 16; it does not compress the later resumed formularies into earlier available Sundays. Thus in 2008 the nominal map is Third, Fourth, Fifth, Sixth after Epiphany on October 26, November 2, 9, and 16. Christ the King displaces the Third on October 26, and the Lateran dedication displaces the Fifth on November 9; the Fourth and Sixth remain in their own slots. The 1962 Missal's alphabetical index expressly places the Lateran dedication under *Festa Domini*, resolving its line-14 precedence over a II-class Sunday.
- Keep computation and occurrence as separate recorded layers: `slot`, `nominal_formulary`, `winner`, `displaced`, `commemorated`, and `verification`. A nominal result is not a dated occurrence witness. Apply the competent universal and proper calendar after the slot map, preserve unresolved local overlays, and do not claim dated-Ordo verification unless a competent dated Ordo was actually checked.
- Over 1900–2100 the surplus `(6 − E) − (P − 24)` is always zero or one, which is why at most one unused formulary is ever dropped, and why the resumable set is exactly the Third through Sixth. Read the rubric in the identified 1962 Missal or the Latin *Rubricae generales* and cite that locus in the leaf; the English witness used here is a specialist transcription, not an official edition, and it carries at least one demonstrable error elsewhere in the same text.
- The code and Missal do not expressly legislate the `P = 23` shortfall. Fail closed rather than choosing between the Twenty-third and the Twenty-fourth-and-last formularies without a competent dated Ordo.

| Civil year | `E` | `P` | Unused after Epiphany | Resumption slots |
| ---: | ---: | ---: | ---: | ---: |
| 2024 | 3 | 27 | 3 | 3 |
| 2025 | 5 | 24 | 1 | 0 |
| 2026 | 3 | 26 | 3 | 2 |
| 2027 | 2 | 27 | 4 | 3 |
| 2028 | 5 | 25 | 1 | 1 |

The 1962 system has no Lectionary cycle: formulary and readings are appointed together and repeat annually. Never import an A/B/C or I/II label into a 1962 record, and never project a postconciliar week number, season boundary, or Ordinary Time term onto the 1962 calendar or the reverse.

## Recording and gates

Every dated instance record states the computed anchors it used, the dated official witness that confirmed them, the resolved Sunday cycle with its exact interval, the independently resolved weekday cycle where applicable, and any unresolved territorial or proper-calendar overlay. Before publishing a dated occurrence, verify that:

- the liturgical-year boundary, not a civil-year boundary, fixed the cycle letter, and the weekday numeral was resolved independently;
- the Ordinary Time week number agrees with both anchors and any omitted week is recorded as omitted rather than shifted;
- a territorial transfer is carried by an actual competent decision, not by arithmetic;
- the computed result agrees with the competent calendar or Ordo, or the disagreement is recorded and publication fails closed; and
- no other guidance file, registry, or publication restates these rules in a form that can drift from this one;
- any feast collision was applied after, and without rewriting, the nominal fixed-slot map;
- a `P = 23` year or unresolved proper-calendar overlay failed closed rather than receiving an inferred winner; and
- a Rogation day was published on its universal assignment only, with any actual transfer under general rubric 87 carried by the Ordinary's decision rather than by arithmetic.

## Sources and open points

These rules were checked on 25 July 2026 against the bishops' approved English [Universal Norms on the Liturgical Year and the Calendar](https://www.liturgyoffice.org.uk/Resources/GIRM/Documents/GNLY.pdf), especially nos. 6, 7, 37, 38, 40, 43, and 44; the approved [General Introduction to the Lectionary](https://www.liturgyoffice.org.uk/Resources/GIRM/Documents/Lectionary.pdf), especially nos. 65, 66, 67, 69, 103, and 104 with their notes; the Holy See's [General Instruction of the Roman Missal](https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20030317_ordinamento-messale_en.html); and Paul VI's [*Mysterii Paschalis*](https://www.vatican.va/content/paul-vi/la/motu_proprio/documents/hf_p-vi_motu-proprio_19690214_mysterii-paschalis.html). Every worked table was recomputed from the Gregorian computus and cross-checked against the United States Conference's published annual calendars, the Bishops' Conference of England and Wales [table of movable feasts](https://www.liturgyoffice.org.uk/Calendar/Info/moveable.shtml), and the repository's own tracked calendar references and dated occurrence records. The 1962 arrangement was checked against *Rubricae generales* n. 18 in the [1962 typical Missal](https://media.churchmusicassociation.org/pdf/missale62.pdf) and in [*Acta Apostolicae Sedis* 52 (1960)](https://www.vatican.va/archive/aas/documents/AAS-52-1960-ocr.pdf), pp. 599–600; the Missal's corrected `XXVII` controls over the Acta's facial `XVII` misprint.

The Ember Days, the two Litanies and the Sacred Heart were established on 31 July 2026 from the repository's own tracked 1962 calendar references rather than from any general knowledge of the liturgical year: the Missal's front-matter note *De anno et eius partibus* and general rubrics 19, 24 b, 80 and 87 as quoted in `src/claude/liturgy/roman-rite/1962/reference/liturgical-calendar/sections/30-vigils-octaves-ember-rogation.tex` and `.../20-temporal-cycle.tex`, the offsets tabulated in `.../research/calendar-inventory.md`, and the temporal table at `src/gpt/liturgy/roman-rite/1962/reference/liturgical-calendar/sections/40-temporale.tex`. Every window above was recomputed from the Gregorian computus across 2020–2120 before being written down.

Record these limits in any leaf that relies on them. Two open points belong to the section just cited: the act that moved the September Ember week from the Exaltation of the Holy Cross to the third Sunday of September is not identified in any witness tracked here, so that rule rests on the 1962 typical edition's wording alone; and a transfer of the Rogation days under general rubric 87 is a local decision that is never computed, so a published Rogation date is the universal assignment and nothing more. No official ecclesiastical statement of the Easter computus was located; the rule above follows the [United States Naval Observatory](https://aa.usno.navy.mil/faq/easter) account of the ecclesiastical equinox and tabular full moon, which is authoritative for the computation but not a Church text. No quotable locus was found for the universal Thursday placement of the Body and Blood of Christ, which comes from the General Roman Calendar itself rather than from an article of the Norms. The 1962 occurrence layer uses general rubrics nn. 14, 16, 17(d), and the table at n. 91; the typical Missal's final alphabetical index expressly includes *Dedicatio Archibasilicae Ssmi Salvatoris, 9 novembris* under *Festa Domini*. The `P = 23` disposition remains unresolved because neither identified normative locus expressly provides for the shortfall.
