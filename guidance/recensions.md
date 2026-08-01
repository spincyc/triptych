# Recensions: one rite, held in more than one state

A design study for carrying more than one state of the same rite — the Roman
Missal as it stood before the Holy Week reform of 1955, and the 1962 typical
edition as a revision applied on top of it — without holding two copies of the
great majority they share.

**The base is the pre-1955 book.** That is the maintainer's ruling of
2026-07-31, and it is the direction the rite actually ran: the older book is not
a variant of the newer one, and deriving an ancestor from its descendant would
invert the history the whole apparatus exists to keep straight. A third state —
the reformed Holy Week of 1956 to 1960 — then sits between them rather than
having to be squeezed alongside.

The base is chosen on that ground and on no other. It is a claim about which
book came first, not about which is better, and this document takes no position
on the second question — see `editorial.md`, "No side in what is described".

**This was written before anything was built, and section 8 now records what
was.** The mechanism, a first recension, and its checks landed on 2026-08-01;
sections 1 to 7 are left as they were written, because a design study that is
quietly edited to match what got built stops being evidence of anything.
Section 8 is where the differences between the plan and the thing are recorded,
including the two places the plan was wrong.

## Evidence conventions

- **[verified]** — measured during this study against tracked artifacts.
- **[sourced]** — reported from an external document, cited.
- **[inferred]** — reasoned from the above. Flagged wherever it matters.

---

## 1. This is already a defect, not only a feature

The repository is **already collating a 1962 book against a pre-1955 witness and
recording the differences as errors.**

The English orations are read against the 1861 Cummiskey printing, which is a
pre-reform book. On 2026-07-31 two entries in
`roman-1962-proper-translations-v1.toml` recorded prayers as *absent from the
witness* when the witness prints them [verified]. The Easter Vigil's
postcommunion was one:

> it is printed on p. 329 as the Vespers prayer *Spiritum*, because the pre-1955
> Holy Saturday Mass **has no postcommunion**.

Nothing was wrong with the witness or the transcription. A matcher keyed on
`(mass, proper-name)` asks a pre-reform book for a slot the reform created, gets
nothing, and writes down an absence. Four further `untranslated` rows are now
flagged *untested* rather than settled, precisely because two rows with identical
wording fell the moment anyone looked [verified].

So the pivot is not a feature request that can wait. It is the missing
distinction that turns a good witness into a generator of phantom absences.

> **Rule 1.** A witness is matched against the recension it belongs to. Where the
> two differ in structure and not merely in wording, an absence in one is not
> evidence about the other.

---

## 2. The mechanics are already free; the duplication is the whole problem

`scripts/_calendars.partition` discovers calendars by walking
`src/sources/calendars/` and dispatching on each file's **declared schema**,
filtering by directory name only when one calendar is asked for [verified]. Nothing
is fixed at two. A third directory would be found by `calendar-days`,
`calendar-spine`, `calendar-rubrics`, the census, the harvest corpus and the
browser's missal control without any of them being told.

What is not free is the data. This section used to carry its own count of
`roman-1962/propers.yaml` — 460 masses and 1,378 propers, marked [verified] —
and both figures have since drifted well past a rounding error; the derived
census in `guidance/propers-for-agents.md` reports the current ones and is the
only place they are stated. **The ratio below has not been re-derived against
them, and the Passiontide subset it rests on was never reproducible from the
figures printed beside it**, so treat the percentage as an order of magnitude
and re-derive before quoting it. That this section restated a census at all is
the defect §2 of `the-shape.md` describes, committed by the document arguing
against it.

**The "tenth of the book" figure below was never reproducible and is now
withdrawn; section 8.1 carries what was measured in its place.** It is left
standing here, struck, because the instruction to re-derive it is the reason
anyone did.

~~**A pre-1955 recension departs in something on the order of a tenth of the
book.**~~ Copying every proper to change that tenth leaves the rest duplicated,
and this repository's
standing rule exists because copies drift: on one day it found three disagreeing
copies of one census, an edition string written out four times, a README
restating its own table differently, and a release manifest attesting a hash that
had never matched any committed file [verified]. A second full calendar would be
the largest such copy in the tree.

> **Rule 2.** A recension is stored as its **departures from a base**, never as a
> second copy of the base.

### The text we hold was read from the newer book, and that does not have to move

Making the pre-1955 book the base raises an obvious objection: every proper now
in the tree was transcribed from the 1962 typical edition and collated
against it, and relabelling them as though they had been read from a pre-reform
printing would be a false provenance claim — the exact defect class this
repository spends its effort catching.

The objection dissolves once **attestation is separated from residence**. A text
lives once, in the base. What witnesses attest it is a separate fact, recorded
per witness, and one text may be attested by many books — which is the ordinary
case, since the whole point is that most of the missal did not change.

So a proper in the base carries the witnesses that have actually been read for
it, and today most of them will say *1962 typical edition, collated* and nothing
else. **That is a true statement, not a false one.** It says the text stands in
the base because the rite had it before 1955, and that the only printing anyone
here has checked it against is the 1962 one.

Three consequences make this the practical shape as well as the honest one:

- **The base can be declared now, with nothing transcribed.** Populating it is
  not a precondition; it is the work.
- **Transcribing a pre-1955 witness ADDS attestation** where the text agrees and
  **creates a departure** where it does not. Neither rewrites what is there.
- **A reader can always be told what was checked.** "Attested in both printings"
  and "attested only in the 1962 printing" are different claims, and a page that
  cannot tell them apart is claiming the stronger one for free.

> **Rule 2a.** A text resides in the base. Its witnesses are recorded per
> witness, and a text attested by only one printing says so. No transcription is
> ever re-attributed to a book nobody read it from.

---

## 3. The shape is one this repository already chose once

`guidance/versification.md` §8.0 settles the projection: a set of rules rather
than a set of verses, where the default rule is identity and **writes no row**,
so the size of the projection measures how far an edition sits from the canon
rather than how large the edition is.

A recension is the same instrument pointed at a calendar. It declares its base
and records only where it departs, so the shared year has exactly one home and
the diff *is* the document — the departures alone instead of the whole book, and
no possibility of the shared remainder disagreeing with itself.

The vocabulary a departure needs is wider than the projection's, because a
calendar can differ in ways a numbering cannot:

| Kind | What it says |
| --- | --- |
| `absent` | the base has this mass or proper; this recension does not |
| `added` | this recension has one the base does not |
| `replaced` | both have it and the text differs |
| `renamed` | the same formulary under another name or key |
| `moved` | the same liturgy on another day, or at another hour |
| `reslotted` | the same words in a different slot — the *Spiritum* case |
| `unrecorded` | known to differ, correspondence not established |

`reslotted` is the one this study exists to name. It is what generated the false
absences, and it is invisible to any matcher keyed on `(mass, proper-name)`
because both sides genuinely hold the words.

> **Rule 3.** A departure that cannot be established is recorded as
> `unrecorded` and resolves to nothing. It is never guessed, and it never
> silently falls back to the base.

---

## 4. Three things harder than the propers

The overlay is the easy part. These are not, and a plan that ignores them will
produce a recension that is right about words and wrong about the Mass.

**The rubrics differ, not only the texts.** The 1962 book follows the 1960
*Codex rubricarum*; a pre-1955 recension answers to the rubrics that preceded
Pius XII's reform. `rubrics.yaml` encodes precedence, and the fifteen solved
cases now genuinely enforce themselves against the browser's model — so a second
rubrics source needs its own solved cases, not a copy of the 1962 ones.

**The placements differ.** The reform moved the Easter Vigil from Saturday
morning to the night [sourced]. `calendar-days` computes placements from the
rules, so this is arithmetic and not text: a recension that overlays only
formularies would put the right words on the wrong day.

**The scope claim needs settling.** `roman-1962/propers.yaml` states in its own
conventions that *"the invariant Ordinary is out of scope; prefaces are not
recorded"* [verified]. The 1955 pivot reaches ceremonies — processions, the
blessing of fire, the order of the prophecies — more than it reaches orations.
A recension must say how far it claims to go, because a reader will otherwise
read silence as sameness.

> **Rule 4.** A recension declares its extent. Where it is silent, it is silent
> *because it has not been established*, and the page says so rather than
> serving the base as though it had been checked.

---

## 5. Naming, which is not cosmetic

"1955" names the reform, not the book, and the reform is a boundary rather than
an edition: the decree *Maxima Redemptionis* was promulgated in November 1955
and took effect in 1956 [sourced]. There are at least three states — the
pre-reform books, the 1956–1960 reformed Holy Week, and the 1962 typical edition
that carries the reform with further changes — and a two-way flag will be wrong
the first time someone asks about the middle one.

> **Rule 5.** A recension is named for the book it transcribes and dated by its
> own printing, exactly as the existing calendars are. It states which reform it
> stands before or after in prose, not in its identifier.

---

## 6. What must be true before any data moves

0. **Per-witness attestation on every proper, before anything is renamed.** This
   is Rule 2a and it comes first, because it is what lets the base be declared
   without moving a single transcription. Until a proper can say which printings
   have been read for it, declaring the pre-1955 book the base would make the
   tree assert a provenance nobody established.
1. The departure vocabulary of §3, with a validator, before the first row is
   written — the lesson `catena.md` records from the same position.
2. A check that fails when a recension's base does not exist, and when a
   departure names a mass or proper the base does not hold. A row pointing at
   nothing is the same defect as a citation that resolves wrongly.
3. `calendar-days` able to compute placements per recension, or an explicit
   statement that it cannot yet and that placements are the base's.
4. The witness question settled: `roman-1962-proper-translations-v1.toml` should
   record which recension each witness belongs to, so the matcher of Rule 1 has
   something to read. This is what makes the 1861 Cummiskey usable instead of
   misleading, and it is worth doing **before** more collation is done against
   it.

## 7. Landing it

The Triduum is both the part that is wanted and the part already producing wrong
results, and under a projection the rest of the year expresses no departure —
which is to say, no rows at all. So the first recension can be four liturgies
wide and still be correct about everything else, because it says nothing about
everything else.

---

## 8. What was built, and where this document was wrong

Landed 2026-08-01. Sections 1 to 7 above are the plan as written; this section
is the thing as built, and it exists separately so that the two can be compared
rather than merged.

### 8.1 The measurements this document asked for

Section 2 told a reader to treat its own ratio as an order of magnitude and
re-derive it. Re-derived, against the tracked files [verified]:

| Measure | Value |
| --- | ---: |
| `roman-1962` masses / propers | 490 / 2,312 |
| `roman-pre-1955` rows (departures stated) | 5 |
| Departures as a share of the base's masses | **1.02 %** |
| Masses the recension serves | 491 |
| — stated by the recension | 1 |
| — inherited, stamped `text_from: roman-1962` | 490 |
| Dates in 2026 resolving to a mass | 316 of 365 |

**The old figure was not merely stale, it was measuring the wrong thing.** "A
tenth of the book" is a claim about how far the two states of the rite stand
apart. 1.02 % is a claim about how much of that distance anyone here has
*established*. The projection is small because the evidence is thin, not because
the books are close, and a reader who reads 1.02 % as agreement has made exactly
the mistake Rule 4 exists to prevent.

What can be measured about the distance itself is narrower and comes from
`roman-holy-week-acts-v1.toml`, which models 38 units of the four liturgies
[verified]:

| At the 1955 reform | Units |
| --- | ---: |
| `absent` — in the pre-1955 book, gone after | **20** |
| `reslotted` | 8 |
| `renamed` | 3 |
| `moved` | 3 |
| `replaced` | 2 |
| Departures recorded at the 1962 edition against that state | 4 (1 `added`, 3 `unrecorded`) |

**Twenty of thirty-eight modelled units — 53 % — do not survive the reform.**

### 8.2 The direction, which this settles

That table is the concrete argument for the ruling in this document's second
paragraph, and it is worth stating as an argument rather than a preference.

If the pre-1955 state were expressed as departures *from* 1962, those twenty
units would each be an `added` row. A recension whose departures are
overwhelmingly additions is not a recension: it is a base wearing the wrong
label, and the file would be reconstructing the older book by undoing the newer
one — a reference that resolves successfully and wrongly, in the one file
written to prevent that.

**One caution, and it is the largest open item.** The act history reads the
post-reform state entirely from a **1962** printing, because the reformed rite's
own book — the *Ordo Hebdomadae Sanctae instauratus* of 1956 — is
`access-restricted-item` at both Internet Archive copies and carries
`may_publish_text = no` [verified, `missal-acquisition-audit-v1.toml`]. So the
figures above measure **pre-1955 against 1962**, and attribute the difference to
the 1955 act on the strength of the decree's own words. Whether the 1956–1960
book differs from the 1962 one in these liturgies is **unrecorded**. Section 5
predicted exactly this hazard; it has arrived.

### 8.3 Where the plan was wrong

**Section 6 item 3 was too optimistic about `calendar-days`.** The claim in
section 2 that "nothing is fixed at two" was true of `partition` and false of
the tools: `calendar-days.BUILDERS`, `calendar-spine.SOURCES` and
`commentary-work-index.DEFAULT_CALENDARS` are closed two-element sets, so a
third calendar directory was *discovered* by four tools and *refused* by three.
A recension now inherits its base's year builder through `temporal_base`, which
is item 3's second option — placements are the base's — made explicit rather
than assumed. This is correct for the date and says nothing about the hour, and
the pre-1955 Easter Vigil is a difference of hour.

**One departure kind per row was not enough.** The Triduum is where one liturgy
departs several ways at once: the pre-1955 Holy Saturday service is `moved` to
another hour, `renamed`, `replaced` in most of its lessons and `reslotted` in
its Postcommunion and its following office, all at the same time. A schema
admitting one kind per row would have forced the file to choose which of those to
record and drop the rest. The primary `departure` is what the machinery acts on;
`also` carries the others, each with its own basis, each checked against the same
closed vocabulary.

### 8.4 What was deliberately not done

**Residence was not flipped.** The base is still where the text lives, and the
text lives in `roman-1962`. Section 6 item 0 is the reason and it is unmet: no
proper in this repository yet records which printings have been read for it, so
moving 2,312 transcriptions under a 1920 heading would assert a provenance
nobody established. The two relations are therefore carried as two fields that
must never be collapsed — `text_from`, which says where text was transcribed in
this repository, and `stands_before`, which says which act the recension stands
before and is the only place descent is claimed.

**No text was transcribed, and the reason is measurable.** The pre-1955
witnesses this project holds are read only through OCR text layers. On
2026-07-31 this repository collated 99 orations taken from the OCR of a single
printing against that printing's page images and corrected **38** of them
[verified]. Landing OCR as payload would put a known 38-in-99 error rate into a
file a page reads from.

**No `rubrics.yaml` was written, and this is why the missal selector does not
yet offer the recension.** The 1962 precedence table answers to the 1960 *Codex
rubricarum*; the pre-1955 calendar answers to the general rubrics that preceded
both the 1955 simplification and the 1960 code. Those must be sourced. Obtaining
them by subtracting 1962 from itself would produce a precedence table that
resolves cleanly and decides days wrongly, which is worse than having none. The
browser discovers missals from `structure/rubrics/index.json`, so a calendar with
no rubrics source is not offered — the dropdown is downstream of the sourcing,
which is the right way round.

> **Rule 6.** A recension is offered to a reader only where it can be served.
> The absence of a rubrics source is not a gap to be filled from the base; it is
> the reason the calendar is not yet in the selector.

---

## 9. One derivation, and the tool that was not using it

Added 2026-08-01, after section 8, in the same spirit: what section 8 recorded as
built turned out to be built in four places out of five.

### 9.1 The shape, stated once

A recension calendar is a `propers.yaml` like any other, distinguished by two
header fields and by the fact that its `masses` are **departures** rather than
entries. `text_from` names the calendar it inherits from; `stands_before` names
the act it stands before. Every row states one primary `departure` from the
closed vocabulary of §3, may carry further kinds under `also`, and must state a
`basis`.

Everything downstream then reads **one function**:

```
_calendars.load_document(root, calendar, effective=True)
```

which returns the base with the departures applied, every entry stamped with how
the recension reached it. `effective=False` returns the file as written, and is
what a census counts — because the size of a recension is the size of its diff.

| Reader | What it takes | Whether it knows what a recension is |
| --- | --- | ---: |
| `check-calendar-masses` | the file as written, plus `recension_problems` | yes, and only to refuse a bad row |
| `mass-propers` | `load_document` | no |
| `calendar-days` | `load_document`, plus `temporal_base` for the year builder | only for the builder |
| `calendar-rubrics` | `load_document` | no |
| `assembly-model.js` | the emitted year file and rubrics file | **no, and it never will** |

The last row is the one that matters. `assembly-model.js` takes a date, a
calendar year file and a rubrics file, asserts no rule of its own, and is run
both by the page and by `calendar-rubrics check` against the solved cases. It
cannot learn a second way to resolve a day, because it is downstream of the
derivation and not a party to it. A recension reaches the browser as a calendar
like any other or it does not reach it at all.

### 9.2 Where it was not true, and how that was found

`calendar-rubrics` parsed `propers.yaml` itself, with `yaml.safe_load`, in
`load_masses` and `all_formularies` [verified]. For the two non-recension
calendars that route and `load_document` return the same object, which is why
nothing caught it.

For a recension they differ by the whole book. `roman-pre-1955` states six rows
and serves 490 masses, so rubrics read the short way would have classified **six
days and been silent about four hundred and eighty-four**, while the browser
served all of them — a second way to resolve a day, disagreeing with the first,
in the layer that decides which day wins. Both functions now go through
`load_document`, and `tools/tests/test_recensions.py` holds the seam with three
cases, one of which asserts that a calendar which is nobody's recension is read
exactly as before.

> **Rule 7.** Every tool that serves or checks a day reads the calendar through
> the one derivation. A tool that parses `propers.yaml` itself is correct for
> every calendar that is not a recension, and that is precisely why the defect
> survives review.

### 9.3 The measurements, re-derived

Section 8.1's figures moved, and are restated rather than edited, because two of
them moved for reasons worth reading [verified, 2026-08-01]:

| Measure | 8.1 | now |
| --- | ---: | ---: |
| `roman-1962` masses | 490 | 490 |
| `roman-pre-1955` departure rows | 5 | **6** |
| Departures as a share of the base's masses | 1.02 % | **1.22 %** |
| Masses the recension serves | 491 | **490** |
| — stated by the recension | 1 | 1 |
| — inherited from the base | 490 | 489 |
| Dates in 2026 resolving to a mass | 316 of 365 | 316 of 365 |
| — reaching a formulary with real text | not measured | **235** |
| — reaching only placeholder formularies | not measured | 81 |

**The 81 are the base's, not the recension's.** 167 of the base's 490 masses
carry a single `Placeholder` proper — mostly third-class saints whose Masses come
from the Commune and have not been written out — and the recension inherits every
one of them. Nothing a recension does can improve that number, and it is recorded
here so that `316 dates resolve` is not read as `316 dates can be served`.

**The served count fell while the departure count rose**, and that pairing is the
projection working. The sixth row is an `absent`, so it removes a mass rather
than adding one: the recension now states more and serves less. A projection
whose row count and whose output count moved together would not be a projection.

The six rows carry six further kinds under `also`, so **twelve departure claims
in six rows** — three `moved`, one `renamed`, one `added` and one `absent` as
primaries, and two `reslotted`, two `renamed`, one `replaced` and one
`unrecorded` beneath them.

### 9.4 The direction, verified rather than assumed

Section 8.2 argued the direction from a table. Re-derived at the unit level from
`roman-holy-week-acts-v1.toml` [verified]:

| | Units |
| --- | ---: |
| Modelled in the pre-1955 state | **38** |
| Gone at the 1955 reform (`absent`) | 20 |
| Surviving into the reformed books | 18 |
| Appearing only at 1962 (`added`) | 1 |
| **Post-reform side, total** | **19** |

**The pre-1955 Triduum is exactly twice the size of what follows it, 38 units
against 19, and the ledger runs 20 losses to 1 gain.** Per liturgy: Palm Sunday
18 units to 7, Holy Saturday 16 to 7, Good Friday 3 to 4, Holy Thursday 1 to 1.

So expressing the pre-1955 state as departures *from* 1962 would make **20 of 21
unit-level rows `added`** — 95 %. That is not a recension of 1962; it is the
older book retyped under a heading that denies it. The maintainer's ruling and
the arithmetic agree, and the arithmetic is now the reason.

### 9.5 An open question closing the right way

The recension refused to write `absent` for the Chrism Mass, although a separate
Chrism Mass being a creation of the 1955 Order is widely understood, because
nothing in this repository established it. On 2026-08-01 both pre-1955 witnesses
were fetched whole and read: each prints exactly one `Introitus` between the Holy
Thursday and Good Friday headings, neither prints `Chrismatis` anywhere in Holy
Week, and the 1920 book prints its own rubric *Triduo sequenti prohibentur omnes
Missae privatae* immediately before the day [verified]. The row is now `absent`
with that reading as its basis.

**It was right for the same reason it had been left open.** The question stood
for one day and cost one fetch, and the answer that arrived was the one everybody
expected — which is exactly the case where writing it down early is cheapest and
most corrosive, because nothing afterwards records that it was never checked.
What the delay bought is a basis that cites two books instead of a consensus.

The same fetch produced a second finding the recension had no reason to expect:
the two pre-1955 witnesses **disagree** about *De hora celebrandi Missam*, the
1920 typical edition allowing Mass `ab aurora usque ad meridiem` and the 1942
Benziger `ab una hora ante auroram usque ad unam horam post meridiem`
[verified]. The Easter Vigil row argues from that rubric. Its conclusion stands
— one hour after noon is still not the night — and its reasoning is now narrowed
to the printing that carries it. §5 said `pre-1955` names a boundary and not an
edition; this is the first time that has cost something.

### 9.6 The rubrics, and what the books said about them

Section 8.4 said the pre-1955 rubrics `must be sourced` and left it there. They
were looked for, and the result is a finding rather than a search report:
**the pre-1955 Missal declines the question in its own general rubrics.** Before
title I it prints *Missa quotidie dicitur secundum Ordinem Officii*, and title VI
prints *In dicendis Missis servetur Ordo Breviarii de Translatione Festorum
Duplicium* — both verified in both witnesses.

The Mass follows the order of the Office; when a feast is impeded, the Breviary
governs. So a pre-1955 `rubrics.yaml` **cannot be built from a missal witness**,
and missals are the only pre-1955 witnesses this repository holds. The 1962
calendar's rubrics source could be built from a missal only because the 1960 code
is reprinted at the front of the 1962 typical edition; before 1960 there was no
such code to reprint.

This is not a gap a closer reading would close, and it sharpens Rule 6 rather
than weakening it: the missing book is now named, and
`src/sources/inventories/pre-1955-rubrics-sources-v1.toml` records the reading,
the two witnesses at their sha256, the rights on each, and what is wanted in the
order that settles the most. Its headline count is
`rubrics_sources_this_record_makes_writable = 0`, written as a number so that it
cannot be read past.

### 9.7 The rule was then found, and the blocker moved

§9.6 asked whether the pre-1955 order is printed anywhere as a numbered table.
It was looked for, and the answer arrived the same day.

**The rule is in the *Acta Apostolicae Sedis* of 1911, and it may be published.**
It is Titulus II, *De Festorum praestantia*, of the rubrics issued under *Divino
afflatu*, at AAS 3 (1911) 641–642 — fetched from vatican.va and read here
[verified, sha256 `590a78b6…`]. That is a stronger position than the calendar
beside it holds: the 1962 rubrics rest on the 1960 code, which is
`holy-see-post-1929` and cite-only, and this one is pre-1931 and publishable.

**And it is not a table.** It is five criteria, taken in order until one
separates two days:

> *Ut recte dignoscatur quale ex pluribus Officiis sit praestantius … sequentes
> praestantiae characteres considerandi sunt:* (a) *Ritus altior*, unless a
> Sunday, a feria, a privileged octave or any octave day occurs; (b) *Ratio
> Primarii aut Secundarii*; (c) *Dignitas Personalis*, in a stated order of
> Persons; (d) *Sollemnitas externa*; (e) *Proprietas Festorum* — which n. 2
> applies **in occurrence and translation only, and not in concurrence**.

The 1960 code replaced this with twenty-eight numbered rows whose numbers later
rubrics cite as addresses, and that is the shape the tooling models:
`check_precedence` requires `rows` numbering 1..N, `check_bases` requires each
competing basis to name one, and `assembly-model.js` picks the winner with
`if (one.row < best.row)` — a comparison of one integer.

**There is no honest mapping, and the reason is (e).** A row number is one order
for all questions. Criterion (e) makes the same two days rank differently in
occurrence than in concurrence, so no single number can carry the pre-1955
answer. Flattening the five criteria into a linear table would produce a file
that validates, resolves every day, and decides some of them wrongly.

> **Rule 8.** Where a recension's rule has a different *shape* from the base's,
> the schema is extended before the source is written. A rule bent to fit an
> existing schema resolves cleanly and answers wrongly, and nothing downstream
> can tell that it was bent.

So Rule 6 holds with a sharper reason. **The calendar is not offered because the
tool cannot yet state its rule, not because nobody has found the book.** Sourcing
is finished; `src/sources/inventories/pre-1955-rubrics-sources-v1.toml` records
seven located sources with rights, two witnesses read at the bytes, five
repositories and the aliases each was searched under — including Google Books,
which was quota-blocked on every query and is recorded as *not reached* rather
than as a negative. Its headline count,
`rubrics_sources_this_record_makes_writable`, is **0**, and it did not move when
the search succeeded. That is the most useful number in the file.

What would have to change, in order, is: `check_precedence`, to admit an ordered
criteria list as a second kind of precedence; `check_bases`, whose competing
bases name a row; and the winner comparison in `assembly-model.js`. That is a
design change and should be argued before it is written, which is why it is
recorded here and not attempted.
