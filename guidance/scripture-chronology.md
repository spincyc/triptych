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

The system is `vulgate`: the same `_projection.CANONICAL` every tracked
projection projects into, because it is the system both tracked calendars cite
in and the system the canonical edition witnesses. `_chronology.CANONICAL_SYSTEM`
names it once and is checked against `_projection.CANONICAL` at load.

**Chronology is authored in exactly one system.** A locus in another system
reaches the corpus through a concordance that already exists — `_psalms` for
the psalter's vulgate/hebrew numbering, `_deuterocanon` for the arrangements of
Esther, Sirach and Daniel — and a refusal there is returned as a refusal here.
There is deliberately **no reverse projection**: `_projection` runs canonical →
edition, and inventing the inverse would manufacture a plausible locus at
exactly the places where the true answer is that two traditions carry different
text.

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
date, and has answered about different text than the caller asked about. So
where the concordance refuses, chronology refuses, and says which of the two
kinds of refusal it is (§9).

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
parent, and one or more dated claims. `src/sources/chronology/events.yaml`.

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

The psalter is the case every simplification breaks on, and three separate
things are load-bearing here.

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
`the-shape.md` §4. Every locus in the corpus's address space reaches exactly
one status, and the coverage report refuses to load if the statuses do not
account for all 35 809 verses.

| Status | Meaning | Authored? |
| --- | --- | --- |
| `dated` | at least one direct substantive assertion | earned |
| `inherited` | covered only by an inherited composition assertion | earned |
| `research-pending` | nothing has been inspected for it yet | the default |
| `undated-in-tradition` | ranked sources inspected; tradition dates nothing | `gaps.yaml` |
| `not-alignable` | the locus cannot be safely addressed from the asking system | `gaps.yaml`, or returned live by the concordance |
| `textually-distinct` | another tradition carries different text, not a renumbering | `gaps.yaml`, or returned live |

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
| `relative` | no absolute endpoints; a stated interval from another event |

`range` and `interval` are different claims and the corpus keeps them apart: a
Gospel written over five years and a Gospel written at an unknown point in a
five-year window are not the same statement.

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
