# The Mass and its propers

Most of a Mass never changes: the same Kyrie, the same Creed, the same Canon,
every day of every year. That invariant part is the **Ordinary**. Woven through
it are about ten short texts that change with the day — a different opening
chant, a different prayer, a different pair of readings — and those are the
**propers**. Knowing what Mass is being said on a given day means knowing which
propers are appointed for it.

Two books of propers are in use. The **1962 Roman Missal** is the last edition
before the Second Vatican Council; the **postconciliar Missal** (here the
*editio typica tertia* of 2008) replaced it. They share a rite, a language, and
a great many actual texts, but they cut the year differently, name the slots
differently, and read scripture on entirely different schedules. This repository
models both, side by side, and refuses to harmonize them where they genuinely
differ.

Every count below is derived from the repository's own files by
`tools/tpt mass-propers census`, and lands in one table under
[What is actually here](#what-is-actually-here). That command is the only thing
that writes the table, and the prose around it states no figure the table does
not. It had to become one derived table because it was three typed ones: this
page, [`guidance/propers-for-agents.md`](https://github.com/spincyc/triptych/blob/main/guidance/propers-for-agents.md)
and the calendars' own README each carried a retyped copy of the same census,
and all three disagreed.

**[Browse the propers](../liturgy/)** — every Mass of both calendars, with each
appointed passage rendered in the translation you choose.

---

## Part one — the two books

### The concrete case: the First Sunday of Advent

The day opens the liturgical year in both books, and both books open it with the
same chant.

In the 1962 Missal it is *Dominica Prima Adventus*. Its first proper is the
**Introit**, the chant sung as the priest approaches the altar; its incipit —
the first words, which is how a chant is identified — is **Ad te levavi**, built
out of Psalm 24, verses 1 to 3, with verse 4 as its psalm verse. In the
Douay-Rheims that this repository has indexed, those verses read:

> To thee, O Lord, have I lifted up my soul. In thee, O my God, I put my trust;
> let me not be ashamed. Neither let my enemies laugh at me: for none of them
> that wait on thee shall be confounded.

The whole 1962 Mass of that day has ten propers:

| Slot | Kind | Content |
| --- | --- | --- |
| Introit | scripture | *Ad te levavi* — Psalm 24:1-3, 24:4 |
| Collect | composed | *Excita, quaesumus* |
| Epistle | scripture | Romans 13:11-14 |
| Gradual | scripture | *Universi, qui te exspectant* — Psalm 24:3, 24:4 |
| Alleluia | scripture | *Ostende nobis* — Psalm 84:8 |
| Gospel | scripture | Luke 21:25-33 |
| Offertory | scripture | *Ad te levavi* — Psalm 24:1-3 |
| Secret | composed | *Haec sacra nos* |
| Communion | scripture | *Dominus dabit benignitatem* — Psalm 84:13 |
| Postcommunion | composed | *Suscipiamus, Domine* |

The postconciliar Mass of the same Sunday also has ten, with the same three
chants under the same incipits:

| Slot | Kind | Content |
| --- | --- | --- |
| Entrance Antiphon | scripture | *Ad te levavi* — Psalm 25:1-3 |
| Collect | composed | *Da, quaesumus, omnipotens Deus* |
| First Reading | scripture | A: Isaiah 2:1-5 · B: Isaiah 63:16b-17, 19b; 64:2-7 · C: Jeremiah 33:14-16 |
| Responsorial Psalm | scripture | A: Psalm 122 · B: Psalm 80 · C: Psalm 25 |
| Second Reading | scripture | A: Romans 13:11-14 · B: 1 Corinthians 1:3-9 · C: 1 Thessalonians 3:12-4:2 |
| Gospel Acclamation | scripture | *Ostende nobis, Domine* — Psalm 85:8 |
| Gospel | scripture | A: Matthew 24:37-44 · B: Mark 13:33-37 · C: Luke 21:25-28, 34-36 |
| Prayer over the Offerings | composed | *Suscipe, quaesumus, Domine* |
| Communion Antiphon | scripture | *Dominus dabit benignitatem* — Psalm 85:13 |
| Prayer after Communion | composed | *Prosint nobis* |

Four things in that pair are each a subject below.

1. **Psalm 24 and Psalm 25 are the same psalm.** So are 84 and 85. The two books
   number the psalter differently — see [Two numberings](#two-numberings).
2. **The 1962 Epistle is Romans 13:11-14; so is the postconciliar Second
   Reading, but only in Year A.** The postconciliar readings rotate on a
   three-year cycle — see [One cycle against three](#one-cycle-against-three).
3. **The Collects are different prayers.** Chants often survived the reform
   unchanged; orations were frequently rewritten or replaced.
4. **The Douay text above is the psalm, not the antiphon.** The Introit's actual
   sung words are a lightly adapted form of those verses, and this repository
   does not carry them. It records what a chant is *made of*, not what it says.

### Chants, orations, readings

The Ordinary is out of scope here entirely: the calendar indexes record no part
of it, and record no prefaces either. An index of what varies has nothing to say
about what does not.

What varies falls into three kinds:

- **Chants** — Introit, Gradual, Alleluia, Tract, Offertory, Communion; in the
  postconciliar books, the Entrance and Communion Antiphons and the Responsorial
  Psalm and Gospel Acclamation. Almost all are scripture, usually a psalm, cut to
  a few verses.
- **Readings** — Epistle and Gospel in 1962; First Reading, Second Reading and
  Gospel in the postconciliar books — scripture outright.
- **Orations** — Collect, Secret, Postcommunion (1962); Collect, Prayer over the
  Offerings, Prayer after Communion (postconciliar). These are *composed* Latin
  prayers. They quote scripture only incidentally and are not built from it.

Only scripture-bearing propers contribute anything to a passage-keyed index; the
orations contribute nothing, because their words are their own. Set the
placeholders aside and rather more than half of what remains carries scripture
in either book; the census below counts both.

Propers are also not a fixed template. The repository stores each Mass's propers
**in the order the edition appoints them**, so Tracts, Sequences, the palm-rite
antiphons, the Improperia, the Exsultet, the Holy Saturday prophecies and the
litanies appear only where they are actually appointed, and a ten-row Sunday
template is never imposed on a day that does not have ten rows. Each file uses
scores of distinct slot names — the census below counts them — and many occur
exactly once: *First Antiphon at the Imposition of Ashes*, *Exsultet
(Praeconium paschale)*, *Improperia*, *Washing of Feet, Antiphon 4*, *Chant at
the Place of Reposition*.

### The temporal cycle and the sanctoral cycle

Every Roman missal is organized around two overlapping cycles. The **temporal**
cycle (the *Proprium de Tempore*) follows the life of Christ through the
seasons: Advent, Christmas, Lent, Easter, and the long stretch after Pentecost.
Its days are movable, because they hang off Easter, which moves. The
**sanctoral** cycle (the *Proprium Sanctorum*) is a fixed-date list of feasts of
the Lord, of Our Lady, and of the saints: 25 December, 25 March, 29 June, and so
on through the year.

The two run simultaneously, which is why a single calendar date can carry more
than one candidate celebration. 26 December is both the second day within the
Octave of the Nativity (temporal) and the feast of Saint Stephen (sanctoral).
Which wins is a question of **precedence**, settled by rank and by rubric, and
it is a separate question from which formularies exist.

This repository classifies every celebration by `kind` — `seasonal`,
`christological`, `marian`, or `sanctoral` — and the classification follows the
*edition's own printed title*, not a modern judgement. The 1962 books title
2 February and 25 March as feasts of Our Lady (*In Purificatione*, *Annuntiatio
Beatae Mariae Virginis*) while the postconciliar books title them as feasts of
the Lord, and the repository reproduces that disagreement rather than resolving
it.

### Where the two books diverge

| Aspect | 1962 | postconciliar |
| --- | --- | --- |
| Season before Lent | **Septuagesima, Sexagesima, Quinquagesima** — a three-week pre-Lenten season | does not exist |
| Long summer/autumn stretch | Sundays after Pentecost, in a single run | Ordinary Time, numbered weeks I–XXXIV, interrupted by Lent and Easter |
| Sunday readings | one fixed set, repeated every year | a **three-year cycle**, Years A, B and C |
| Weekday readings | one fixed set | a **two-year cycle**, Years I and II, independent of the Sunday cycle |
| Readings per Sunday Mass | Epistle and Gospel | First Reading, Responsorial Psalm, Second Reading, Gospel |
| Psalm numbering | Vulgate throughout | mixed — see below |

Septuagesima is the cleanest case of a season existing in one book and not the
other. In the 1962 data it is a season in its own right holding three Masses; in
the postconciliar data there is no such season and no such key.

The postconciliar Ordinary Time has its own arithmetic quirk: there is no
**First** Sunday in Ordinary Time at all. Week I is the week in which the
Baptism of the Lord falls, and the Baptism replaces that Sunday, so the numbered
Sundays run from the Second to the Thirty-fourth. The repository's data agrees:
its Ordinary Time Masses are keyed `ot-2` through `ot-33`, thirty-two of them,
with the Thirty-fourth Sunday carried separately as Christ the King.

### One cycle against three

The single largest structural difference is the Lectionary. The 1962 system
appoints formulary and readings together: the First Sunday of Advent has *one*
Epistle and *one* Gospel, the same every year, forever. The postconciliar system
separates them — a Sunday has one set of chants and orations but three sets of
readings, and which set is used depends on whether the liturgical year is Year
A, B or C.

The letter is fixed by the civil year in which the liturgical year *ends*, not
the year it begins. Call that year `Y`; then `Y mod 3 = 1` is Year A, `2` is
Year B, `0` is Year C, and the cycle turns at the First Sunday of Advent and
nowhere else. Weekdays in Ordinary Time run a separate two-year cycle, Year I in
odd years and Year II in even ones, which is *independent*: with periods 3 and
2 the pairing repeats only every six years, and neither letter can ever be
derived from the other.

In the repository's data the propers that carry a `cycles` mapping are the
Gospels, the Second and First Readings, the Responsorial Psalms and the Gospel
Acclamations, plus a handful of Holy Week items; the census below counts them.
Every one of them is postconciliar. No 1962 proper carries a cycle, and none
ever should.

### The calendar arithmetic, and its hard limit

[`guidance/liturgy/calendar-computation.md`](https://github.com/spincyc/triptych/blob/main/guidance/liturgy/calendar-computation.md)
is the single authoritative statement of the arithmetic. Nothing else in the
repository may restate it; everything else references it.

**Easter** is the Sunday after the first ecclesiastical full moon falling on or
after 21 March, by the Gregorian computus — the tabular ecclesiastical rule, not
an astronomical full moon. Every other movable day is a fixed offset in days
from Easter:

| Day | Offset |
| --- | ---: |
| Septuagesima (1962 only) | −63 |
| Ash Wednesday | −46 |
| Ascension, Thursday form | +39 |
| Ascension, transferred Sunday form | +42 |
| Pentecost | +49 |
| Trinity Sunday | +56 |
| Corpus Christi, Thursday form | +60 |
| Corpus Christi, transferred Sunday form | +63 |

The liturgical year itself turns at the First Sunday of Advent, the fourth
Sunday before 25 December, which falls between 27 November and 3 December.

And then the constraint that governs all of it:

> **Computation is a finding aid, never an authority.**

The competent General, territorial, diocesan, religious, parish and church
calendar, the approved books, and the competent annual Ordo control what is
actually celebrated. The rule here is: compute, then verify against a dated
official witness, record both, and **fail closed on disagreement** — state the
divergence and resolve nothing by preference. A computed date is never published
as its own occurrence witness.

The sharpest form of this is the **territorial transfer**. Epiphany, the
Ascension, and the Body and Blood of Christ are moved to a Sunday in some places
and not in others, and that is a decision of the competent authority, not
derivable from any calendar arithmetic whatsoever. The offsets table gives both
the Thursday and the transferred Sunday form of Ascension and Corpus Christi
precisely because no formula can choose between them.

Two smaller cases are recorded as deliberately unresolved rather than guessed: a
1962 year with only twenty-three Sundays after Pentecost (neither identified
normative text provides for the shortfall), and any proper-calendar overlay that
has not actually been checked.

### Two numberings

The Latin psalter is numbered two ways, and over most of its length the Vulgate
number runs one behind the Hebrew one: Vulgate 24 is Hebrew 25, Vulgate 84 is
Hebrew 85, Vulgate 118 is Hebrew 119. That is why the 1962 Introit cites
Psalm 24 and the postconciliar Entrance Antiphon cites Psalm 25 for the same
words. The correspondence is not a formula — six psalms divide between the two
systems — so the repository converts through a tracked verse-level concordance
built from the Challoner edition, and never from a typed table.

Each calendar file declares its own numbering. `roman-1962` declares `vulgate`
and means it throughout. `postconciliar` declares `hebrew` — and here the books
themselves are not consistent. The file's own recovered `citation_convention`
states the rule:

> Lectionary readings and antiphons preserve the numbering in the controlling
> missal

Which is to say: a postconciliar antiphon reproduces the number printed in the
*Missal*, and a responsorial psalm or acclamation takes the number printed in the
*Lectionary*, and those are not always the same system. The Twenty-third Sunday
in Ordinary Time shows it inside a single Mass: its Entrance Antiphon is cited
`Psalm 118:137, 124` and its Year C Gospel Acclamation `Psalm 119:135`. Both are
the psalm *Beati immaculati*. One is numbered Vulgate, the other Hebrew.

---

## Part two — what this repository holds

### How a calendar file is shaped

One file holds each calendar, under a header that declares the controlling
edition, the ordering rule, the psalm numbering, the citation convention, and
the verification state. Each Mass carries a stable key, the edition's own
catalog name, its identity in the registry that numbers it, and its propers in
the order the edition appoints them.

Every proper declares whether its text is scripture, composed, or both, and the
rest of its shape follows: a scripture proper carries the passages it is built
from and no text, a composed proper carries the Latin text and no passages, and
the validator refuses either one carrying the other. A proper whose content
varies by Lectionary year carries the A, B and C forms separately. A celebration
with several complete formularies — the Nativity's four Masses, the Ember
Saturdays the Missal prints in a longer and a shorter form — carries each
formulary whole.

References are stored as structured extents rather than as strings to be
re-parsed: one or more contiguous ranges under a canonical book name, with the
edition's own printed display string kept beside them and never treated as
authoritative. The encoding carries what liturgical books actually print — a
selection within a chapter, a range crossing a chapter boundary as the Passions
do, a chant cited whole by chapter, a printed part-verse letter — and the
encoder refuses a citation it cannot encode without guessing rather than writing
a wrong range.

### What is actually here

The seasonal sections carry real propers. **Most of the rest is a name, not a
formulary**: a mass that holds nothing but a placeholder establishes that the
mass exists and where it falls, and records nothing of what is said at it.
Coverage is wide and shallow by design, and a reader who sees a Mass listed
should not infer that its texts are here.

The table below is derived, not typed. `tools/tpt mass-propers census --write`
rewrites it in place, `make check-propers-census` fails when it has drifted from
the calendars, and nothing else on this page states a figure it gives.

<!-- census:begin — derived; edit nothing between these markers -->

| Calendar | Section | Masses | Propers | Masses holding only placeholders |
| --- | --- | ---: | ---: | ---: |
| roman-pre-1955 | seasonal | 6 | 6 | 6 |
| roman-1962 | seasonal | 128 | 1138 | 5 |
| roman-1962 | christological | 8 | 12 | 7 |
| roman-1962 | marian | 18 | 74 | 4 |
| roman-1962 | sanctoral | 307 | 981 | 121 |
| roman-1962 | common | 30 | 152 | 0 |
| postconciliar | seasonal | 67 | 832 | 2 |
| postconciliar | christological | 7 | 23 | 3 |
| postconciliar | marian | 14 | 52 | 4 |
| postconciliar | sanctoral | 181 | 606 | 44 |

| Calendar | Rank | Entries | Celebrations |
| --- | --- | ---: | ---: |
| roman-pre-1955 | (no rank) | 6 | 6 |
| roman-1962 | (no rank) | 93 | 93 |
| roman-1962 | Comm. | 104 | 104 |
| roman-1962 | I | 37 | 37 |
| roman-1962 | II | 46 | 47 |
| roman-1962 | III | 211 | 211 |
| postconciliar | (no rank) | 64 | 64 |
| postconciliar | All Souls commemoration | 1 | 1 |
| postconciliar | Feast | 24 | 24 |
| postconciliar | Memorial | 69 | 69 |
| postconciliar | Optional memorial | 82 | 82 |
| postconciliar | Optional memorials | 18 | 38 |
| postconciliar | Solemnity | 11 | 11 |

| Measure | roman-pre-1955 | roman-1962 | postconciliar |
| --- | ---: | ---: | ---: |
| Masses | 6 | 491 | 269 |
| Propers | 6 | 2357 | 1513 |
| — named `Placeholder` | 6 | 139 | 55 |
| — inside a `forms` block | 0 | 130 | 140 |
| — carrying a `cycles` mapping | 0 | 0 | 253 |
| Masses holding only placeholders | 6 | 137 | 53 |
| Masses taking a formulary from another entry | 0 | 56 | 0 |
| Propers taking their text from another entry | 0 | 53 | 0 |
| Propers that are not placeholders | 0 | 2218 | 1458 |
| — of those, scripture-bearing | 0 | 1827 | 1185 |
| Encoded passages | 0 | 2129 | 1721 |
| Distinct books cited | 0 | 55 | 63 |
| Distinct slot names | 1 | 119 | 89 |

Counted from `src/sources/calendars/*/propers.yaml` and written here by
`tools/mass-propers census --write`, which is the only thing that writes the
block above; `make check-propers-census` refuses a copy that has drifted. What
each row counts, because two honest counts of “propers” differ by hundreds
when they key differently: a **mass** is one entry under `sections[*].masses`.
A **proper** is one entry in a mass's `propers`, or in the `propers` of one of
its `forms`; a proper carrying `cycles` counts once, not three times.
Placeholders are **inside** the proper and mass totals, and are also given
their own rows. A mass **holds only placeholders** when every proper it holds,
those inside `forms` included, is named `Placeholder` — keying on the mass's
own `propers` alone undercounts, because it misses the masses whose
placeholders sit inside a `forms` block. **Scripture-bearing** means a
`source` of `scripture` or `mixed`, or a `cycles` entry that is. **Encoded
passages** and **distinct books** are `tools/citations check`'s own counts,
one passage per encoded citation entry and books counted distinct within a
file. **Distinct slot names** counts distinct proper `name` values, with
`Placeholder` among them. The two **taking** rows count the entries that name
where their text is printed instead of printing it — a feria taking the
preceding Sunday, a saint taking a Mass of the Common. Such an entry holds few
propers or none, so it lowers the proper count while raising what the calendar
can actually show: every row above counts what a file **carries**, and these
two count what it **appoints** from elsewhere. Neither is a placeholder.

The rank rows count **entries**, and a calendar's rank rows sum to its
`Masses` above. `(no rank)` is a row and not an omission: the temporal cycle
prints no rank at all, so unranked entries are a large group in both indexes,
and a table that dropped them would invite the ranks it does show to be read
as the whole book. **Celebrations** counts what those entries name. One entry
can print more than one celebration — a pair of optional memorials falling on
the same day, or the Greater Litanies kept with Saint Mark — and the index
records the join only in the entry's `name`, joined with `;`, so that is where
it is read from; the plural rank word marks some such entries and not others,
and it never says how many. Where the two columns differ the index is keeping
more celebrations than it holds entries: reading the entry count as a count of
celebrations understates the calendar, and folding the celebrations into the
entry count would break the sum against `Masses`, so both are given and
neither replaces the other. A **rank** is reproduced exactly as the file
prints it. `Optional memorial` and `Optional memorials` are two rows because
they are two different words in the index, and the two Missals' rank
vocabularies are not one scale — no row of this table is comparable across
calendars, which is why rank is tabulated down the page and not across it.
This table answers what an index is scoped to; it does not answer which
entries are Sundays, because no entry states that and it is not derived here.

<!-- census:end -->

### The 1962 temporal expansion, and what it deliberately omits

The 1962 seasonal section began as 59 Masses — the Sunday run plus the Triduum
and Palm Sunday. Its largest single expansion added 63 temporal days, and the
three Christmas octave placeholders came with it; a few more entries have landed
since, and the census above holds the current figure. The 63 cover the days the
Missal keeps and the file did not — the Ember Days of all four seasons, Ash
Wednesday and the days after it, the ferias of Lent and Passiontide and of Holy
Week to Wednesday, the Chrism Mass, the Easter and Whitsun octaves, the Rogation
Mass, the Vigil and feast of the Ascension, the Vigil of Pentecost, the Mass of
the First Sunday after Pentecost, Corpus Christi, and the Sacred Heart.

Every one of those 63 entries carries **only its scripture-bearing propers**, and
says so in its own notes:

> Only the scripture-bearing propers are recorded; the day's orations and other
> composed chants are appointed but not yet transcribed.

This is a deliberate refusal. The orations of those days exist and are appointed;
they were not transcribed because they were not read. The alternative would have
been to generate plausible Latin, and a plausible wrong oration is worse than an
absent one.

Identity, rank and the printed scripture references were read from an **OCR text
layer** of the CMAA 1962 facsimile, not from the facsimile images. Confidence in
each day's identity and rank is high; confidence in each citation is only as
high as an unproofed scan allows; nothing has been visually collated.

### Eleven antiphons that fell between the numberings

Eleven antiphons carried the Missal's printed Vulgate number inside a file
declaring Hebrew numbering. Because Hebrew 118 ends at verse 29, `Psalm 118:137`
is not a resolvable verse at all under the file's own declaration — and for a
long time nothing noticed, because the psalter bounds check held verse ceilings
only for the six psalms that split between the systems. The eleven are:

| Mass | Slot | Incipit | Cited |
| --- | --- | --- | --- |
| ascension (Vigil Mass) | Entrance Antiphon | *Regna terrae cantate Deo* | Psalm 67:33, 35 |
| ot-6 | Communion Antiphon | *Manducaverunt, et saturati sunt nimis* | Psalm 77:29-30 |
| ot-8 | Entrance Antiphon | *Factus est Dominus protector meus* | Psalm 17:19-20 |
| ot-9 | Entrance Antiphon | *Respice in me, et miserere mei* | Psalm 24:16, 18 |
| ot-22 | Communion Antiphon | *Quam magna multitudo dulcedinis tuae* | Psalm 30:20 |
| ot-23 | Entrance Antiphon | *Iustus es, Domine* | Psalm 118:137, 124 |
| ot-26 | Communion Antiphon | *Memento verbi tui servo tuo* | Psalm 118:49-50 |
| ot-29 | Communion Antiphon | *Ecce oculi Domini super timentes eum* | Psalm 32:18-19 |
| ot-31 | Communion Antiphon | *Notas mihi fecisti vias vitae* | Psalm 15:11 |
| ot-33 | Communion Antiphon | *Mihi autem adhaerere Deo bonum est* | Psalm 72:28 |
| christ-the-king | Communion Antiphon | *Sedebit Dominus Rex in aeternum* | Psalm 28:10-11 |

**Current state.** Each proper may now declare its own numbering rather than
being forced into its calendar's, and all eleven carry that declaration; the
validation path has not caught up, so all eleven still report as out of bounds
and are set aside through a listed exceptions ledger. That ledger is
self-cleaning in both directions: an out-of-bounds psalm at an *unlisted* locus
still fails the build, so a new leak cannot hide behind the known ones, and a
listed locus that has *stopped* breaching also fails, so an entry cannot outlive
the defect that earned it. Correcting the eleven — deciding, per slot, whether
the number moves or the declaration does — is tracked as TASK-32.

Two other references cannot resolve for reasons upstream of any of this:
`4 Esdras 2:36-37` is not among the Douay-Rheims' 73 books, and
`Malachi 3:19-20a` is Hebrew numbering where the Vulgate prints Malachi 4:1-6.
Only psalms are converted between systems today.

### Divergences outside the psalter, recorded by hand

Only the psalter has a concordance; nothing else converts. The postconciliar
Lectionary cites the Nova Vulgata, no witness of that versification is tracked
here, and every bible in this library follows the Vulgate division. Where the
two divide a book
differently — Joel, Malachi, and single chapters of Isaiah and Micah — the
reference does not fail. It **resolves, to different words**: `Joel 3:1-5`
returned the valley of Josaphat instead of the outpoured spirit, in Latin and
English alike, and appeared in no error count.

So a calendar records the correspondence by hand, citation by citation, in a
`citation_divergences` list. A correspondence that holds unchanged is written out
anyway rather than omitted, on the principle that inside a divergent locus,
silence is not evidence that anyone checked. A citation reaching a divergent
locus with no correspondence recorded is refused — left out of every index and
reported unresolved — because a missing passage is a question and a plausible
wrong one is an answer.

### Three days that fell between two records

29, 30 and 31 December 1962 — the fifth, sixth and seventh days within the
Octave of the Nativity — sat in the date-ordered list of celebrations and in no
section of the propers file at all. They are there now, as placeholders, and
every celebration the date list carries must now have a Mass, filed under the
kind that list assigns it, or the build fails.

Closing the gap meant settling how they classify, and the answer was in the
edition's own punctuation. Within an octave:

- a **colon** introduces the day's own principal celebration — *"Second day
  within the octave: S. Stephani Protomartyris"* is Saint Stephen's feast, set
  within the octave, and classifies **sanctoral**;
- a **semicolon** introduces a mere commemoration — *"Fifth day within the
  octave; comm. S. Thomae Episcopi et Martyris"* is the octave day itself, and
  classifies **seasonal**.

So in the 1962 data, 26–28 December are filed sanctoral and 29–31 December
seasonal.

The formulary those three days actually use is still absent. It is one of three
the Missal carries that this file does not — the others being *D. N. Iesu Christi
Regis* and *Sanctissimi Nominis Iesu*.

### Everything here is an unverified lead

A calendar index is a **planning and cross-reference spine, not a source of
record**. It carries no artifact hash and proves nothing on its own; a
publication still binds the edition and artifact that control each text through
its own `research/source-bindings.toml`.

Both files say so in their `verification` header. The 1962 file states three
tiers of confidence; the postconciliar file states two. Every citation and every
text is an unverified lead until collated against the controlling edition, and
each file tracks its known problems in `open_collation_items` rather than
silently harmonizing them away. The instruction is explicit: fix a divergence by
collation, not by making the file falsely uniform. `open_collation_items` in
both files ends with the line *all entries in this file are placeholders pending
source-backed completion*.

---

## Open questions

Each of these is recorded in the repository as unresolved, not silently decided.

| Question | Where it lives |
| --- | --- |
| Whether the eleven antiphons should move their numbers or keep their per-slot declaration | TASK-32; the `psalm_numbering_exceptions` ledger |
| Whether Ascension, Corpus Christi, the Sacred Heart and the Chrism Mass belong under `seasonal` (where the Missal prints them) or `christological` (what they are by kind) | 1962 `open_collation_items` |
| A registry scheme for 1962 ferias, which have no printed identifier | 1962 `open_collation_items` |
| How 1962 commemorations should be modelled — the 104 are now dated entries of rank `Comm.`, but a commemoration's own three orations still have nowhere to live | 1962 `open_collation_items` |
| Which numbering system each of a further 23 non-psalm postconciliar citations actually speaks, before any of them is corrected | postconciliar `open_collation_items` |
| Whether proper prefaces and the *Oratio super populum* belong in this index at all | postconciliar `open_collation_items` |
| The 1962 twenty-three-Sunday shortfall after Pentecost | `guidance/liturgy/calendar-computation.md` |

---

## Where to look next

| For | Read |
| --- | --- |
| The schema and how to read an index | [`src/sources/calendars/README.md`](https://github.com/spincyc/triptych/blob/main/src/sources/calendars/README.md) |
| The calendar arithmetic, authoritatively | [`guidance/liturgy/calendar-computation.md`](https://github.com/spincyc/triptych/blob/main/guidance/liturgy/calendar-computation.md) |
| What is outstanding, and what each open item is blocked on | [`guidance/propers-for-agents.md`](https://github.com/spincyc/triptych/blob/main/guidance/propers-for-agents.md) |
| The source contract for calendars | [`guidance/sources.md`](https://github.com/spincyc/triptych/blob/main/guidance/sources.md) |
| Working here as an agent | [`guidance/propers-for-agents.md`](https://github.com/spincyc/triptych/blob/main/guidance/propers-for-agents.md) |

To read a Mass:

    tools/tpt mass-propers show --calendar roman-1962 --mass advent-1 --bible douay-rheims
    tools/tpt mass-propers list --calendar postconciliar
