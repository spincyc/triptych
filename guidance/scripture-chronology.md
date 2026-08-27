# Scripture chronology: when the text was written, and when what it tells of happened

This contract governs the Scripture chronology corpus under
`src/sources/chronology/`: what it holds, what a query returns, what may be
authored into it, and what a consumer is forbidden to do when it says nothing.
It supplements `guidance/sources.md`, which owns source identity and
provenance, and `guidance/versification.md`, which owns how a citation reaches
a locus at all. It replaces neither.

## Evidence conventions

**[verified]** — read in this repository's tracked data or derived from it by a
command recorded here. **[sourced]** — read in an inspected external source
whose record is in the source library. Everything else is a proposal.

---

## 1. The problem

A publication that wants to say when something happened has, until now, had to
find out. Each one separately. The repository has three hundred documents and
no place where a biblical date lives, so every document that needed one
researched it, and nothing compared the answers.

That is `the-shape.md` §2 exactly — *two copies of a fact are a prediction that
they will differ* — and this project has already paid the prediction once, in
the neighbouring case. `guidance/sources.md` records it: *De Genesi ad
litteram* carries **no date field at all** in its work record, its Migne
edition carries `date = "1841"`, and the catena renders the work at 415 from
`text_date` in `src/sources/commentary/fragment-loci.yaml`, restated once per
fragment. One work, two dates, in two subsystems, with nothing reconciling
them. **[verified]**

Biblical dates are the same shape of fact with more consumers and worse
failure. A date is a well-formed integer, so a wrong one reads exactly like a
right one, which is `the-shape.md` §1 in its most silent form. And the wrong
answer is not merely a wrong year: it is usually a wrong *question*. Ask when
Psalm 21 belongs and there are at least three defensible answers — when David
composed it, what occasion he composed it on, and the Passion the Church reads
in it — and a corpus with one `date:` field per verse forces the first
consumer to choose one and every later consumer to inherit the choice without
seeing it.

So the corpus does not hold dates. It holds **typed temporal assertions**, and
a locus resolves to as many of them as are true of it.

---

## 2. Where chronology sits

```text
edition / citation
    ↓   guidance/versification.md
citation + versification/projection machinery
    ↓
resolved Scripture locus, in a NAMED system
    ↓   this document
SCRIPTURE CHRONOLOGY CORPUS
    ↓
zero or more typed temporal assertions
    ↓
propers, Catena, studies, web, PDF, whatever comes next
```

Chronology is **downstream of locus resolution and upstream of document
synthesis**. It is not part of a Bible edition, it is not part of a projection,
and it is not part of any publication.

The seam is deliberate in both directions:

- **Downstream of resolution**, because a chronology that had to parse
  citations would be a second citation parser, and this repository already has
  the one it needs. A consumer resolves its citation the way it already does
  and asks about the locus it arrives at.
- **Upstream of synthesis**, because a chronology embedded in a proper is a
  chronology only that proper can read.

`scripts/_chronology.py` is the whole seam. Nothing else reads
`src/sources/chronology/`.

---

## 3. What a chronology key is

```text
system + book token + chapter + verse
```

spelled exactly as `scripts/_projection.py` spells a locus: `Ps.50.3`,
`Matt.27.35`, `3Kings.6.1`. The book tokens are the canon's own, from
`scripts/_canon.py`, which reads them from the canonical edition's tracked book
index — 73 books, 1 334 chapters, 35 809 verses. **[verified]**

The **preferred shared system** is `vulgate`: the same `_projection.CANONICAL`
every tracked projection projects into, because it is the system both tracked
calendars cite in and the system the canonical edition witnesses.
`_chronology.PREFERRED_SYSTEM` names it once and is checked against
`_projection.CANONICAL` at load.

Preferred is not sole. The systems a scope may name are read from the modules
that **own** them — `_projection` owns the canonical name, `_psalms` owns
`hebrew`, `_deuterocanon` owns `greek` and `world-english-catholic` — rather
than restated here, because a list beside theirs is how lists stop agreeing.
They already had: `_commentary.NUMBERING_SYSTEMS` names `septuagint`,
`nova-vulgata` and `nab`, for which no concordance exists, and omits
`world-english-catholic`, for which one does. Chronology admits only names with
machinery behind them, and the check is **(system, book)**: `hebrew` is a
psalter numbering and may not name Matthew.

### 3.0 One fact, one place — and the gate that enforces it

**Where a safe correspondence exists, chronology is authored once at the
preferred locus and reached from elsewhere through the concordance.** Hebrew
Psalm 51 is Vulgate Psalm 50; there is one Miserere and it is dated once.

This is a **load-time gate, not a convention**: a scope naming another system
whose locus the concordance carries safely to the Vulgate is refused. So a
native scope is admissible *precisely when sharing is impossible*, and where
sharing is possible it is mandatory.

**The gate holds over the whole scope, not over its first locus.** It walks every
locus the system's witness prints inside the span. A gate that probed
`span.first` proved something about `span.first`, and admitted any span whose
opening happened to refuse — which is what it did until 2026-08-27, when the cold
audit of `2330d63a5` found it. Where a span's loci do not behave alike, the span
is refused and the author splits it.

**And what it refuses is a duplicated fact, not a safe correspondence.** The two
are not the same thing, and they come apart at exactly one locus in this
repository. The concordance carries greek Ecclus 36:16 safely to vulgate Ecclus
36:18; the fact authored natively there is the date of the *Greek translation*,
which the Vulgate unit does not hold and could not, because it dates the Hebrew
original and the Latin version. Safe correspondence says the two loci carry
corresponding text. It does not say that every fact about one is a fact about the
other.

So the gate asks which kind of other system it is looking at, of the module that
owns the name. A **psalter numbering** — `hebrew`, owned by `_psalms` — is one
psalter under two numbers: §8, one psalm with one chronology, so a native scope
there is the same fact twice whatever value it carries, and two *different* dates
for one psalm is the worse failure rather than the lesser. A **witness to another
text** — `greek` and `world-english-catholic`, owned by `_deuterocanon` — is
§3.2's "two texts, not two numberings", and native authorship there is refused
only where it would restate a claim the preferred locus already holds.

### 3.0.1 A mapping refusal is not a chronology refusal

The corpus used to return a concordance refusal as its own answer. Those are
two questions:

```text
may this locus be asserted equivalent to that one?     mapping status
does this locus have chronology at all?                chronology status
```

They are **separate axes** and an `Answer` carries both. A textually distinct
text can be dated and unmappable at once, and the standing case is the Greek
Ecclesiasticus: 1 355 of its 1 356 printed loci refuse the Vulgate because there
are two texts and not two numberings, and Gigot dates the Greek translation to "not
long after" 132 B.C. in its own right. Both are true. Before the correction the
second was unreachable, and the corpus knew it — `composition.book-of-ecclesiasticus`
carried a note warning that three dates in that article "must not be conflated",
written by an author with nowhere to put the second one.

There is still deliberately **no reverse projection**: `_projection` runs
canonical → edition, and inventing the inverse would manufacture a plausible
locus at exactly the places where the true answer is that two traditions carry
different text. Native chronology is not a reverse projection; it is a fact
authored at the locus it is true of.

### 3.1 Why there is no translation-specific chronology

Because chronology is not a fact about a translation. When Matthew was written
is the same fact whether it is read in the Douay, the Knox or the King James,
and three copies of it would be three chances to drift. `the-shape.md` §3:
reference, do not copy.

The tracked editions differ in *numbering*, and that difference is already
solved, once, by the projection layer. A chronology keyed to canonical loci and
reached through that layer needs no per-edition data at all — and the size of
the thing that would otherwise be duplicated is worth stating: seven editions ×
35 809 verses.

### 3.2 Why there is no universal verse space

`guidance/versification.md` §4 settles this and this document does not
re-argue it: **a single universal verse space cannot exist, because the
disagreement is about how much text there is.** Sirach settles it — 48 of its
51 chapters differ in verse count between the tracked Douay and the tracked
King James Apocrypha, because the Latin carries expansions the Greek does not.
**[verified]** There are two texts, not two numberings.

A chronology key that resolved anyway would be the defect this apparatus exists
to catch, in its purest form: a query that succeeds, returns a well-formed
date, and has answered about different text than the caller asked about. So the
concordance goes on refusing, and says which of the two kinds of refusal it is.

What changed on 2026-08-27 is what that refusal *means*. It is reported on the
mapping axis and it no longer suppresses the answer: where the corpus holds
chronology authored natively at the asked locus, the query returns it **and**
the refusal. Refusing to equate two texts is not a reason to say the second one
is undated.

**Both axes answer, always, and the chronology axis only ever speaks chronology.**
The first correction separated the axes for the locus that *has* chronology and
left the locus that has none still answering `textually-distinct` to the question
"is this dated?" — a mapping word standing in the chronology axis, on ten native
loci with no route to anything else. A native locus whose mapping refuses now
reaches an authored gap row scoped in its own system, and otherwise the honest
default of §9. Two consequences bind:

- **a native scope is bounded by its own witness, not by the canon.** `EsthGr` is
  a book the Greek witness prints and `scripts/_canon.py` has no row for, and
  while scopes were checked against the canon no locus in it could be given any
  status at all;
- **a mapping word is never a chronology status.** `not-alignable` and
  `textually-distinct` belong to the mapping axis. They may appear in `gaps.yaml`
  only where an author is recording what the concordance says, never as an answer
  to whether a locus is dated.

And a successful mapping does not erase a native fact either: where a locus both
corresponds safely and carries chronology authored in its own system, the query
returns both.

---

## 4. The profile

A date in this corpus is a date **under a profile**. The profile is the policy;
the assertions are the facts; each fact names the profile it was authored
under. `src/sources/chronology/profiles.yaml` holds them.

There is one: **`catholic-traditional-v1`**.

### 4.1 What it asserts, and what it does not

It asserts the chronology a traditional Catholic apparatus states about
Scripture. It does **not** assert that every traditional calculation has been
dogmatically defined; the Church has defined very few of them, and a profile
that implied otherwise would be making a claim about the Magisterium in order
to make a claim about a year.

It is **not** normalised to modern archaeological, Egyptological,
Assyriological or critical-historical chronology, and a divergence between this
profile and modern scholarship is **a profile boundary, not an error in
either**. Where the two diverge the corpus keeps the traditional figure and
says, in the assertion's own note, that it is a traditional figure. A modern
chronology, if ever wanted, is a **separate profile with its own id** — never a
silent correction of this one, and never an edit of an existing assertion.

The id ends in a version because **a change of authority policy is a new
profile, not an edit**.

### 4.2 The authority hierarchy

Read in order. A lower rank is consulted only where every higher rank is
silent, and a higher rank never yields to a lower one because the lower one is
more precise. **Precision is not authority** — the date model keeps `precision`
apart from the claim's `basis` and its sources for the same reason.

| Rank | Authority | What this repository holds |
| --- | --- | --- |
| 1 | Scripture's own chronological and relational statements | `src/sources/bibles/` |
| 2 | Roman liturgical witnesses, where they make a chronological claim | `src/sources/calendars/` |
| 3 | The received Catholic biblical apparatus, edition-identified | Haydock's Douay-Rheims commentary |
| 4 | Patristic and early ecclesiastical chronological testimony | Eusebius, Jerome |
| 5 | Traditional Catholic commentators and chronologists | Cornelius a Lapide |
| 6 | Later traditional Catholic reference works | The 1907–1914 Catholic Encyclopedia |
| 7 | Project derivation from the above | a claim carrying a `derivation`, with its rule and inputs |

Rank 2 is silent far more often than it speaks. **A feast's date is not a
chronological claim.** The Roman books keep the Annunciation on 25 March; they
do not thereby assert the year, and reading a calendar as a chronology would
manufacture dates out of a liturgical arrangement.

### 4.3 What is not an authority

Three, named because they are the ones that would otherwise arrive silently.

- **Ussher.** May be cited as comparison, and may be *reported* where a ranked
  Catholic source itself prints his figures — Haydock does, and that printing
  is Haydock's testimony, recorded as such. Ussher is never the source of
  record, and **no assertion may name him alone**.
- **Modern critical chronology.** Not consulted, not used to adjust a
  traditional date, not treated as a correction. See §4.1.
- **Any model's unsourced recollection.** Never an authority at any rank. A
  date nobody read is `research-pending`, which is a status this corpus can
  hold — and the reason it can hold one is precisely so that this rule can be
  obeyed without leaving a hole.

### 4.4 When sources disagree

**Preserve the disagreement.** Every sourced claim is kept with its own
provenance and a disposition:

| Disposition | Meaning |
| --- | --- |
| `preferred` | the claim the profile displays first; needs a strictly higher authority rank than every alternate, or an explicit note saying what settles it |
| `alternate` | a sourced claim not displayed first, kept queryable with its provenance |
| `disputed` | a sourced claim in unsettled disagreement; **no claim on that subject is preferred while any is disputed** |

The loader enforces all three: more than one `preferred` under one profile is a
load error, `preferred` beside `disputed` is a load error, and two claims with
neither is a load error, because silence about which is which is the thing that
later reads as a decision nobody made.

Forbidden: numeric confidence, model scores, and harmonising two claims into a
third nobody asserted.

---

## 5. The eight relations

The vocabulary is closed. `_chronology.RELATIONS` holds it and an unrecognised
relation is a load error.

| Relation | What it answers |
| --- | --- |
| `composition` | when the text was written |
| `narrated-event` | when the event the passage narrates happened |
| `utterance` | when the words the passage quotes were spoken |
| `historical-setting` | the occasion tradition associates with the text |
| `superscription-setting` | the setting the biblical title itself asserts |
| `retrospective-event` | an earlier event the passage explicitly recalls |
| `prophecy-given` | when the oracle was uttered |
| `prophetic-referent` | the later event tradition reads it as prophesying |

The distinctions are the point of the corpus, so they are stated as
prohibitions:

- **`prophetic-referent` is not `narrated-event`.** Psalm 21 is not a report of
  the Passion. A corpus that could not say so would have David narrating
  Calvary as history, and the resulting page would be fluent, confident and
  false.
- **`composition` is not `historical-setting`.** When a text was written and
  what occasion it is about are different events, frequently centuries apart.
- **`superscription-setting` is not `composition`.** A title is *evidence*
  about a setting. It is not proof of a year, and it settles no editorial
  question about authorship.
- **`utterance` is not the quoting passage's `narrated-event`.** When the
  Gospel reports Our Lord quoting Psalm 21, the psalm's utterance and the
  Gospel's narrated event are two assertions on one locus, not one.
- **`retrospective-event` is not `narrated-event`.** A passage that recalls the
  Exodus does not narrate it.

Additional relations may be added when research proves one semantically
necessary. Synonyms may not.

---

## 6. Events, held once

An **event** is a reusable temporal subject: an id, a title, an optional
parent, and zero or more dated claims (§6.1).
`src/sources/chronology/events.yaml`.

```yaml
- id: life-of-christ.crucifixion
  title: The Crucifixion of Our Lord
  parent: life-of-christ.passion
  dates:
    - profile: catholic-traditional-v1
      disposition: preferred
      date: {precision: year, from: {year: 33, era: ad}}
      sources: [passage....]
```

*(The shape is real; the year is an illustration and asserts nothing.)*

**An event is dated once and bound from every locus that needs it.** If the
four Gospels narrate the Crucifixion, there is one Crucifixion event and four
sets of bindings — not four dates. A **binding carries no date at all**, and the
loader refuses one that tries to, because that is the exact door through which
parallel passages acquire parallel dates that then drift. This is
`the-shape.md` §2 applied to the one fact this corpus exists to hold once.

The same event is bound from an Old Testament prophetic locus under
`prophetic-referent`, without anything implying that the psalm was composed on
Good Friday.

Events may nest (`parent`), for grouping only. The loader refuses a dangling
parent and refuses a cycle. Do not grow an ontology ahead of a consumer that
needs one.

### 6.1 A subject may be named without being dated

**An event may hold zero claims.** Naming a subject and dating it are two acts,
and requiring the second of every event meant the only claim on a subject could
not be withdrawn without deleting the subject — which cannot be done at all
where bindings name it and other claims are measured from it. The live cases
are `israel.monarchy.saul-accession`, whose one claim was a modern
reconstruction §4.3 excludes, and
`israel.exile.ezechiel.death-of-the-prophets-wife`, whose one claim encoded
containment as an offset (§10.0); both claims are withdrawn and both subjects
stand.

Such an event **asserts nothing and returns nothing**. Omit `dates`; an empty
list is refused, here as everywhere. A binding may name it — `bindings.yaml`
asks only that the event is declared — and a `relative` date may be measured
from it, because an anchor is checked for existence and never computed with
(§10.0). A binding to it therefore contributes no assertion, so the loci it
reaches keep whatever else reaches them and nothing moves in coverage: the
accession verses answer `composition-only` from their book's composition unit.
**[verified]** `validate` remarks on such an event exactly as it does on any
event no binding reaches (§16) — a remark, and not an error.

**A composition unit still requires a claim**, and the loader refuses one
without. A unit exists only to carry a composition date over an extent, so a
dateless unit would be a scope asserting nothing about the text it names.

**This is not `research-pending`.** That is a status a *locus* has when no
ranked source has been inspected for it (§9); a claimless event is a *subject*
this corpus holds and dates nowhere. One corpus carries both at once, and a
consumer meets them differently — the subject as silence, the locus as a word
on the verse.

---

## 7. Composition, and how it inherits

A **composition unit** is a textual unit with its own writing chronology and an
explicit extent. `src/sources/chronology/composition.yaml`. A scope may be a
whole book, a chapter, a run of chapters, or a verse range.

A unit reaches **every verse inside its scope**, so a book-level claim needs no
row per verse: one unit for the Gospel of St Matthew covers 1 071 verses
without 1 071 rows. **[verified]** That is `the-shape.md` §3 — reference, do
not copy — and it is also the only way this corpus stays reviewable.

**The narrowest unit covering a verse wins.** Two units of *equal* width over
one verse is a **load error, not a tie**: nothing here may pick between them,
because choosing the first, or the most recently edited, would be a date
resolving successfully and wrongly with no signal at all. The author says which
unit owns the text.

**Inheritance must be semantically honest.** It exists because a book written
once was written once — not to make a coverage number look better. Two
consequences, both binding:

- **An anthology gets no single date.** The Psalter in particular is not one
  book written at one time, and giving it one composition unit in order to
  reach every verse would be exactly the abuse this paragraph forbids. §8.
- A composite work whose tradition distinguishes its parts gets units at the
  size tradition distinguishes, not at the size that is convenient.

A query reports whether an assertion reached the locus **directly or by
inheritance**, so a consumer can tell a statement about this verse from a
statement about its book.

---

## 8. The Psalter

The psalter is the case every simplification breaks on, and four separate
things are load-bearing here.

**Traditional authorship or attribution ALONE never establishes a
`historical-setting`.** That a psalm is "of David" — or that a ranked source
says David wrote it — supports authorship, and it may support a `composition`
claim to the degree an inspected source actually dates or bounds the writing.
It does not establish the occasion the psalm was written on, or the event it is
historically about. A `historical-setting` needs a source that actually
identifies an occasion, or an explicit deterministic derivation from evidence
that does.

The rule had been applied in both directions at once. Ps 88 refused an
authorship-derived setting and said so in its own note — "this corpus does not
convert an authorship claim into an occasion" — while Ps 21 carried one whose
note conceded the title "names no occasion" and then took the occasion to be
"the reign of David itself", which is the attribution restated. Ps 21's was
withdrawn on 2026-08-27. Removing a `historical-setting` does not disturb a
`prophetic-referent` over the same psalm: they are different relations, and Ps
21 keeps the Passion referent it was authored for.

**It is an anthology.** It has no single composition date and this corpus will
not give it one. Composition units are authored per psalm, or per group where
tradition groups them, and psalms nobody has researched stay
`research-pending` — which is the honest report and is not a defect.

**Its numbering is already solved and must not be re-solved.** The Miserere is
Psalm 50 in the Vulgate system and Psalm 51 in the Hebrew, and it is **one
psalm with one chronology**. Chronology is authored at `Ps.50` and a query in
Hebrew numbering reaches it through `_psalms.convert_point`, which the psalm
concordance drives. Authoring both would produce two chronologies for one
psalm, and `scripts/_psalms.py` opens by recording what happened the last time
this fact was restated: the copies *"disagreed, and gave Hebrew 10 and 115 the
last verse of the Vulgate psalm hosting them rather than their own."*
**[verified]**

**A title is evidence, not a date.** A biblical superscription is recorded as
`superscription-setting` — what the title itself asserts — and never promoted
to `composition` because it is available. Where tradition reads a further
occasion into a psalm, that is `historical-setting`; where the Church reads the
psalm of Christ, that is `prophetic-referent`. One psalm can carry all four
kinds at once, which is the whole reason the model is many-valued.

---

## 9. Statuses: what a locus has when it has no date

**Absence is data and must have somewhere to live**, or it will be filled —
`the-shape.md` §4. Every locus of the **Vulgate/Clementine primary universe**
reaches exactly one status, and the coverage report refuses to load if the
statuses do not account for all 35 809 of them. That universe is named, not
assumed: it is not the whole of Scripture this layer can address (§9.3).

**Chronology status answers whether a substantive assertion APPLIES, not how it
arrived.** A scoped assertion true of every verse in its scope is true of each
of them; that it was authored at the scope rather than at the verse is
provenance, it rides on every returned assertion as `inherited`, and it decides
nothing. Before 2026-08-27 `dated` was defined as "at least one **direct**
substantive assertion", which said two wrong things: a whole-book
`prophecy-given` over Ezechiel left 271 verses looking undated though the oracle
applies to every one of them, and a directly authored composition unit alone
would have reported event chronology nobody had researched.

| Status | Meaning | Authored? |
| --- | --- | --- |
| `dated` | at least one substantive (non-composition) assertion applies, direct or inherited | earned |
| `composition-only` | a composition assertion applies and no substantive one does, at any scope | earned |
| `research-pending` | nothing has been inspected for it yet | the default |
| `undated-in-tradition` | ranked sources inspected; tradition dates nothing | `gaps.yaml` |
| `not-alignable` | the locus cannot be safely addressed from the asking system | `gaps.yaml`, or returned live by the concordance |
| `textually-distinct` | another tradition carries different text, not a renumbering | `gaps.yaml`, or returned live |

The last two are **mapping** answers, and where they arrive live they belong to
the mapping axis (§3.0.1), not to the chronology axis. Do not read
`not-alignable` as "undated", and do not read `research-pending` as "the
projection refused".

`composition-only` was called `inherited` until 2026-08-27 — a directness word
doing a scope job, and the same word the per-assertion provenance flag uses.
Coverage reports the provenance split (`substantive_by_provenance`: direct-only,
inherited-only, both) beside the statuses rather than inside them.

`research-pending` is **the honest default and is not authored**. A corpus that
had to write a row for every unresearched verse would be 35 809 rows asserting
nothing, and the rows would then be mistaken for coverage.

These words are deliberately **not** `_projection`'s (`absent`, `unrecorded`,
`displaced`, `split`, `merge`, `renumber`). Those say things about where *text*
is. A verse can be present, aligned and perfectly addressable and still have no
date, and a word that meant both would hide one of them.

### 9.1 A headline percentage is forbidden

`coverage` reports every category and no single number. "100% covered" is true
of a corpus that has researched nothing, if the thing being counted is keys in
a file. A consumer that wants a headline builds it from the categories, in
sight of them.

### 9.3 The universe is named, not assumed

Coverage is reported over three dimensions, because one number over an
unexamined universe is how a corpus claims completeness it has not got.

1. **The Vulgate/Clementine primary universe** — 35 809 loci. Complete
   accounting: every one reaches exactly one chronology status.
2. **Additional native loci per named system** — loci a system prints that the
   concordance refuses to carry to the preferred system, and which are
   therefore additional text rather than the same text renumbered. An alternate
   numbering of a safely corresponding locus is **not** new Scripture and is
   not counted. Neither is a locus already counted under another system: the
   World English Catholic edition re-divides the Greek, and 2 088 of the 2 094
   loci it prints reach it, so counting those again would count one text twice.
3. **Cross-system mapping status** — safely shared, textually-distinct,
   not-alignable — reported as its own axis, never as a chronology status.

At the time of writing the corrected universe is 35 809 + 1 356 (`greek`) + 6
(`world-english-catholic`) + 0 (`hebrew`, whose psalter is wholly shared) =
**37 171**. A system this repository can name but cannot enumerate is reported
as `enumerable: false` and is a reason the coverage requirement stays open, not
a thing to leave out quietly.

### 9.2 `research-pending` is empty in the primary universe, and what that does and does not mean

Every locus of the **Vulgate/Clementine primary universe** reaches a
substantive assertion, a composition assertion, or an authored gap row.
**[verified]** No verse of it is `research-pending`.

That is a statement about that universe and no other. It must never be reported
as "the Bible is dated" or "Scripture chronology is complete": 1 362 native
loci sit outside it — 1 356 `greek` and 6 `world-english-catholic`, counted
from the verses those witnesses actually print — and seven of them answer
`research-pending` on the chronology axis, beside a mapping refusal on the
mapping axis. The figures were 1 400 and ten until 2026-08-27, when
`_system_loci` stopped filling each chapter from its first printed verse to its
last; three of the ten were invented verse numbers and were never text.

That is a real result and a small one. It means a ranked source was inspected
for every verse and its answer recorded — including where the answer was that
tradition dates nothing, which is most of `undated-in-tradition`'s share. It
does **not** mean the chronology is finished, and it must never be reported as
"the Bible is dated". Two thirds of the canon is `inherited` — a book-level
composition claim reaching its verses — and a book whose composition tradition
declines to date has no chronology of its own at all.

While the corpus was incomplete, the presence of `research-pending` was itself
the guard: a coverage number could not run ahead of the research, because the
unresearched share was printed beside it. That guard is now gone, and the job
falls to two others, both in `tools/tests/test_chronology.py`:

- **every gap row names a source record.** A row that names none is the exact
  shape a fabricated coverage number would take — a verse leaves
  `research-pending` for an authored status and no other way, so an unsourced
  row is coverage asserted on nobody's authority.
- **no status reaches a verse unless an author asserted it**, checked against
  `AUTHORED_STATUSES`, which `_chronology` names once so the loader and the
  test cannot drift apart.

A lane that closes the last of a book's gaps should expect to add to those
guards rather than to delete them.

---

## 10. Dates

A date is structured. A display string is carried beside it and is **never the
machine truth**.

```yaml
basis: >-
  The Catholic Encyclopedia's article on the book states it, and refuses to
  settle between this and the later date it also reports.
sources: [artifact.catholic-encyclopedia.volume-10.new-york-1911....]
date:
  precision: interval
  from: {year: 40, era: ad}
  to:   {year: 45, era: ad}
  label: "between A.D. 40 and 45"
```

*(Structure, not assertion.)*

| Precision | Endpoints |
| --- | --- |
| `day` | one point, with month and day |
| `month-day` | month and day, **year unknown** |
| `year` | one point, exact |
| `approximate-year` | one point, the source's own "about" |
| `range` | the subject **spans** from..to |
| `interval` | the subject **falls somewhere within** from..to |
| `relative` | an **offset**: N units after/before a named anchor event |
| `duration` | a **length**: the subject lasted N units, measured from nothing |

`range` and `interval` are different claims and the corpus keeps them apart: a
Gospel written over five years and a Gospel written at an unknown point in a
five-year window are not the same statement.

### 10.0 A duration is not a relative offset

`relative` says **when** relative to something else. `duration` says **how
long**. "He judged Israel eighteen years" states no point in time and no
anchor; reading it as an offset would put the judgeship eighteen years after
whatever the anchor happened to be. One value meaning both would be a date that
resolves successfully and wrongly.

The distinction is **structural, not conventional**:

- a `duration` may not carry a `relative` anchor, and may not carry endpoints;
- a `relative` must name an anchor that exists, dated or not (§6.1);
- a duration's units are whole and positive — zero is refused, because a span
  of no length is how "the source says nothing about how long" would look if it
  were written down, and that is silence, with `undated-in-tradition` and a gap
  row of its own;
- a duration may say what it sits **within**, validated as a real event, and
  `Date.anchor` deliberately does not return it. **Containment is not offset.**

```yaml
date:
  precision: duration
  duration:
    years: 18
    statement: "And he judged Israel eighteen years"
    within: israel.judges.period
  label: "eighteen years"
```

Before 2026-08-27 the corpus had only `relative`, and 47 claims were using it
for lengths — the whole Judges family among them, each anchored on
`israel.judges.period` as though counted from its start. Nothing computed with
them, which is the only reason no wrong date had yet been produced.

### 10.2 An interval lands on the endpoint its source names

A source that states an interval states what it runs to. Attach it there, and
nowhere else — not to a neighbouring event whose own figure happens to compute,
and not to the endpoint a section heading names when the arithmetic inside the
section names a different one.

The instance is the cold audit's one critical finding. The Catholic
Encyclopedia's Flood-to-Abraham table totals 367 / 1017 / 1147 under a row it
labels *"Hence, number of years from Flood to Call of Abraham"*, and reaches
those totals from the row above by *"Add for age of Abraham at time of his call:
75"*. The section's heading says "birth"; the arithmetic says "call". The corpus
carried all three on the birth, overstating every one by exactly seventy-five
years, and read perfectly.

**Arithmetic consistency is not an anchor.** The check that catches this is to
compute the interval against what the anchor already holds and see which event it
lands on: the Deluge is held at A.M. 1656, and 1656 + 292 is the traditional year
of Abraham's birth while 1656 + 367 is his call. Where a corpus holds both events
and an interval between them — here Genesis 12:4's seventy-five years — the two
stored statements must be capable of being true together, and these were not.

**`precision` is separate from authority.** Approximate means the *date* is
approximate. It is not a judgement about the source, and a rank-3 source's
"about A.D. 42" outranks a rank-6 source's exact year.

`basis` is a required line of **prose beside every claim, saying what grounds
it** — which work, what it states, and the decisive phrase. It is the same
pairing the source library already enforces on a work record, whose message says
it best: *composed requires composed_basis: say what dates the writing, and
never the printing.* And it is held to the same standard
`src/sources/commentary/work-extents.yaml` states: **a basis that merely
restates this repository's own prose is not a basis.** It is not an enum, and it
is not a confidence.

A claim must also name at least one **source record** — the loader refuses one
that does not, because a date with nothing behind it cannot be checked and is
indistinguishable from an invented one. Records are named by their
source-library id, or, where Scripture is its own witness, as
`bible:<edition>:<locus>`. The audit refuses an id this repository does not
hold.

A claim carrying a **`derivation`** is a derived claim; there is no second word
saying so, because two ways of saying it is one way of disagreeing. A derivation
must name its `rule` and its `inputs`, each input being an event or composition
unit this corpus holds, and is visibly derived wherever it is displayed. A
derivation never overwrites a sourced assertion.

### 10.1 Eras

`bc`, `ad`, `am`.

- **There is no year zero**, in either Christian era, and the loader refuses
  one. An interval computed across a year zero is wrong by one and reads
  perfectly.
- **A year is never negative.** B.C. is an era, not a sign.
- **Anno Mundi is a third axis and is not converted.** Traditional sources
  print A.M. figures — Haydock prints Usher's, giving the first captivity under
  Joakim as A.M. 3398 **[sourced]** — and this corpus records them in the era
  they were printed in. Converting would require fixing an epoch; traditional
  sources use several; no ranked source in this repository has been inspected
  *asserting* one. A conversion is therefore a derivation and needs its own
  rule, inputs and epoch before it may exist. A range may not run between A.M.
  and the Christian era, and the loader refuses one.
- Month and day are validated against the month's real length; `calendar` is
  recorded where it matters and is not defaulted.

---

## 11. Provenance

Chronology is factual corpus data and is source-first. `guidance/sources.md`
governs source identity; nothing here restates it.

Every substantive assertion names source-library records — a passage record and
its exact locus wherever one exists, else an edition or work record. Keep three
things apart, always:

```text
the source says X
the project derives Y from X          a derivation, with its rule and inputs
the profile prefers Y                 disposition: preferred
```

Do not put a raw search result in the corpus as evidence. Do not name a source
loosely: work, edition, artifact and inspected locus are four things and
`sources.md` says so. Do not invent a citation.

Where a source is not lawfully redistributable, store what the source-library
policy allows and keep enough provenance to re-check the claim. The Haydock
commentary is the live instance: `storage = "remote"`, no bytes retained, and
thirteen passage records that name the artifact hash and the exact PDF page
read. **[verified]** That is sufficient provenance and is the pattern.

---

## 12. What a query returns

```python
from _chronology import chronology
answer = chronology("Ps.21.19")
```

An **`Answer`** — the resolved locus, an ordered tuple of assertions, a status
and a note — or an **`Unresolved`**, which is returned, never raised, so a
caller can print the reason.

Each assertion carries its relation, the event or unit it belongs to, that
subject's title, the claim (date, disposition, sources, note), whether it was
`inherited`, and the authored scope it reached the locus from.

Ordering is stable and defined: relation in the order of §5, then disposition
(`preferred`, `alternate`, `disputed`), then subject id, then the date's
rendering. A diff of two queries is a diff of the answers, not of the sorting.

**The query never picks.** Where a subject carries alternatives, every
alternative is returned. `the-shape.md` §5: a tool that always answers is a
tool that lies when it does not know, and silently choosing between two
traditional dates is that lie with better manners.

---

## 13. The generated view

`src/sources/chronology/coverage.tsv` is **derived, tracked, and gated**. It is
not the source of truth; `tools/tpt scripture-chronology check` fails when it
differs from a fresh derivation, exactly as the bible indexes are gated.

It is **run-compressed**: one row per maximal run of consecutive verses that
answer identically. That is the same choice `versification.md` §4 makes for the
psalm concordance — *the psalm table covers 2 528 verses in 220 rows, because a
segment is the natural unit* **[verified]** — and for the same two reasons. A
run is what a reviewer can actually read, and a verse-by-verse file would be an
order of magnitude larger while hiding the structure that makes an error
visible.

A consumer wanting true per-verse rows gets them from `--expand`, which writes
to `build/` and is never tracked.

---

## 14. The consumer contract

**A publication or proper that needs biblical chronology MUST read this corpus.
It MUST NOT independently infer, research, harmonize, or assign a replacement
biblical date.**

If the corpus returns no substantive assertion, or a typed unresolved state,
the consumer **preserves that state or omits the date** according to its own
profile. It does not invent one. It does not fall back to a model's
recollection. It does not quietly use a date it found elsewhere.

This is not a style preference. A consumer that re-derives is a second source
of truth for a fact that has one, and every such pair in this repository's
history has already diverged.

Consumers should carry the stable chronology ids — event id, unit id, profile,
relation — in their research or audit payload, so prose can be regenerated
without re-researching the fact.

**Propers are not wired to chronology yet, and this document does not wire
them.** That is a separate bounded lane. The rule above binds it when it comes.

---

## 15. Adding or correcting chronology

1. **Find the reusable subject first.** One researched event bound from fifty
   loci beats fifty researched verse dates, and one composition unit inherited
   by a thousand verses beats a thousand rows. If what you are about to author
   is already an event, bind to it.
2. **Read a ranked source and quote it.** §4.2. Register what you read under
   `guidance/sources.md` — work, edition, artifact, passage — before the claim
   names it.
3. **Choose the relation deliberately.** §5. If two of them apply, author two
   assertions; that is what the model is for.
4. **Author the date structurally**, with the source's own words in `label`
   and its own hedges preserved. Do not resolve an ambiguity the source left.
5. **If a source disagrees with one already held, add it** with a disposition.
   Do not overwrite, and do not harmonize.
6. **If nothing dates it, author nothing.** `research-pending` is correct. Only
   author a `gaps.yaml` row when the status is *known* to be something else.
7. **Run the checks** (§16), and rebuild the generated view in the same commit.

Never fabricate to close a gap. Never promote a superscription to a composition
date because the composition date is missing. Never let a book-level date be
authored solely to move a coverage number.

### 15.1 The ways this corpus has actually been got wrong

Not hypotheticals. Each of these passed a lane's own review, loaded clean,
audited clean, and was caught only when a second reader went back to the
source. Check for them by name.

1. **A quotation from memory.** A note quoted Genesis 18:10 as "at this set
   time I will return to thee". The tracked Douay reads "I will return and come
   to thee at this time" — the remembered string is the Authorised Version's.
   The claim was true; the evidence for it was not. **Read every verse you
   quote out of the tracked text**, and never from recollection, however
   familiar. `.scratch`-style helpers exist for this; `_bible` is the source.

2. **A relative anchor that exists but is the wrong one.** Jacob's twenty years
   of service were anchored on the birth of Joseph, which Genesis places
   *fourteen years into* the term. The loader cannot catch this: it checks that
   the anchor exists, not that the interval is measured from it. **Say what is
   measured, from what, and check the text puts the anchor at the interval's
   start.**

3. **A figure the source reports rather than asserts.** Both books of Esdras
   were dated to 300 B.C. on a clause reading "as most critics think". §4.3
   excludes exactly that, and the same lane had correctly refused a different
   figure on the same ground an hour earlier. **A year inside "most critics
   hold", "some writers say", or a named third party's voice is that party's
   claim, not the source's** — and under this profile usually not a claim at
   all. The units were withdrawn and the books now carry typed silence.

4. **A claim about a source with no retained retrieval.** A gap row asserted
   that four encyclopedia articles "carry no chronological statement of any
   kind". Nothing of those four was retained, so the claim could not be
   checked — and when it finally was, it was false for two of them: "Adam"
   quotes the years of Genesis 5 and "Sara" gives three ages. **Register and
   retain what you read before you characterise it**, including when what you
   are recording is a silence.

5. **A refusal that goes stale in the same wave.** A binding refused to name an
   event "because this corpus holds no event for that episode" while a parallel
   lane was authoring precisely that event; two psalms with one superscription
   ended up with two answers. **When lanes run in parallel, re-read the merged
   corpus before trusting any refusal whose ground is "the corpus does not hold
   it".**

6. **A duration encoded as an offset.** Forty-seven claims used `relative` —
   "N units after an anchor" — to say "lasted N units". Nothing computed with
   them, which is the only reason no wrong date had been produced yet. The two
   are now different precisions and the loader keeps them apart structurally
   (§10.0).

7. **Authorship promoted to a historical occasion.** Ps 21 carried a
   `historical-setting` inferred from "of David" plus the years David reigned,
   while Ps 88 had refused exactly that inference. §8 now states the rule once
   and both stand under it.

8. **Directness confused with applicability.** `dated` required a *direct*
   assertion, so 271 verses of Ezechiel reached by a whole-book
   `prophecy-given` looked undated though the oracle applies to every one of
   them. Status now asks what applies; `inherited` is provenance and decides
   nothing (§9).

9. **A textually distinct locus treated as chronologically nonexistent because
   the projection refused.** The Greek Ecclesiasticus had a date in an
   inspected source and no way to hold it. Mapping status and chronology status
   are separate axes (§3.0.1).

10. **A refusal produced by taking the wrong route, then enshrined in a test.**
    The World English Catholic edition is two hops from the Vulgate; chronology
    asked for a direct row, the direct index is empty, and all 2 094 of the loci
    it prints came back `textually-distinct`. A test asserted that refusal as
    correct. 730 of those loci are the Vulgate's own text, and under the
    corrected coverage rules every one of the 2 094 would have been counted as
    new Scripture.
    **A refusal is evidence about a route until you have checked the route.**

11. **A key stated twice in one mapping.** An edit applied by string
    replacement left a second `sources:` in one claim and a second `label:` in
    two `date:` mappings. Every duplicated pair was identical, so no answer
    moved, and `validate`, the coverage rebuild and 92 tests all passed over a
    corpus that is not valid YAML.
    **The loader now refuses a repeated key by file, line and name (§16).**

---

## 16. Commands and checks

| Command | Question |
| --- | --- |
| `tools/tpt scripture-chronology validate` | is the authored corpus well-formed and internally consistent? |
| `tools/tpt scripture-chronology query <locus>` | what does the corpus say about this verse? |
| `tools/tpt scripture-chronology coverage` | what is covered, by category? |
| `tools/tpt scripture-chronology build` | rewrite the generated view |
| `tools/tpt scripture-chronology check` | is the generated view current? |

`make check-scripture-chronology` runs `validate` and `check`, and is part of
`make check`. The focused tests are `tools/tests/test_chronology.py`.

The loader refuses a mapping key stated twice, at any depth, before it reads
anything in the file as a fact, and names the file, the line and the key.
PyYAML keeps the last of a repeated key silently, so a corpus invalid under
YAML 1.2 loaded clean and every gate behind the loader called it healthy: that
is how three duplicated keys survived a `validate`, a coverage rebuild and the
whole test suite in August 2026.

Because chronology reads `_canon`, `_psalms` and `_deuterocanon`, a change to
the canonical edition's book index, the psalm concordance or the deuterocanon
concordance can change chronology's answers. Run the chronology check after
touching any of them.

---

## 17. What this corpus is not

- Not a general chronology of the world. It dates Scripture and what Scripture
  tells of.
- Not the composition date of an *edition*. `guidance/sources.md` owns that
  distinction and states it: a work's date is when it was written, an
  edition's is when it was printed, and **a composition date is never inferred
  from a printing date.**
- Not a claim of doctrinal certainty. §4.1.
- Not a modern chronology, and not a place to smuggle one in. §4.1.
- Not complete. It says which parts are not.
