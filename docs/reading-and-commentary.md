# Reading and commentary: two editorial undertakings

Two pieces of work in this repository are not data entry. Both had to decide
something before they could record anything, and in both cases the decision is
more interesting than the result.

The first is **an abridged reading plan** — a route through the Bible that tells
salvation history as a continuous story, at three depths, in 357 sittings. The
hard part was not choosing passages. It was choosing them *lawfully*: every
published narrative reading plan worth consulting is a copyrighted compilation,
and the obvious way to build one — read four of them and take the union — is the
one way you may not.

The second is **a commentary harvest** — an attempt to find out which pre-1900
commentaries actually treat each passage the missals cite. It consulted a model,
which is not a reproducible act, so the tooling was built to never call one. It
records what a model said, with the model's name and the date, and then measures
how often three separate askings agreed. The measurement came back with an
uncomfortable and useful answer, and the answer is why nothing from the harvest
has been promoted into the source library yet.

This document explains what each undertaking decided and why. The headings alone
give the shape; the prose under each gives the detail. Every number in it was
recomputed from the repository's own tracked files — where a figure disagreed
with what the files claim about themselves, the measurement is given and the
disagreement said out loud. The recompute commands, the invariants, and the
failure modes are in
[`guidance/reading-plan-for-agents.md`](../guidance/reading-plan-for-agents.md).

---

## Part one — the narrative spine

### What the plan is

`src/sources/reading-plans/narrative-spine.yaml` holds 357 readings in 12
periods, running from creation to the end of Acts and closing on Apocalypse
21:1–22:5. It touches 454 chapters in 31 of the canon's 73 books.

It is a *route*, not a text. The file carries references — book, chapter, verse
— and nothing else that a reader would call scripture. That matters for rights,
and it matters for the architecture: the browser fetches the same chapter
fragments the propers browser uses, and the reading plan just tells it which
ones and in what order.

### Three tiers that nest, so a shorter pass is not a different plan

| Tier | Readings | Verses | Share of the Bible |
| --- | --- | --- | --- |
| Overview | 36 | 1,210 | 3.4% |
| Narrative | 111 | 3,675 | 10.3% |
| Year | 357 | 13,867 | 38.7% |

The tiers are cumulative. Each reading records the tier at which it *first*
appears, and reading a tier means taking that tier and every tier above it. So
36 readings enter at overview, 75 more at narrative (111 total), 246 more at
year (357 total). No reading appears twice, and — checked directly — no verse in
the whole plan is covered by two readings.

The design consequence is the point. A reader who does the overview and then
wants more does not re-read; the narrative tier fills the gaps *between* the
overview readings rather than restating them. The three tiers are three
resolutions of one route, not three plans.

### Where the selection came from: overlap measured, not lists transcribed

Four widely used narrative schemes were consulted: Ascension's Great Adventure
Bible Timeline, Zondervan's *The Story*, Tyndale's narrative arrangement, and
BibleProject's reading plans. None of their chapter lists, sequences, divisions
into readings, titles, notes, or commentary was copied.

What was taken is the *overlap* — the set of chapters that all four independently
land on. The file records that overlap as 334 chapters, about 30.7% of the Bible
by verse, and calls it the consensus narrative spine.

The distinction is load-bearing, and it is worth being precise about it. A
curated reading plan is a compilation: the selection and arrangement are the
creative act, and they are protected even though every individual verse
reference in them is a bare fact. So you may not take one scheme's list. But
"these four schemes all include Genesis 22" is a fact *about* those schemes, not
an expression *of* any of them — the way a survey reporting that four
dictionaries all define a word the same way is not a copy of any dictionary. The
overlap is discovered by measurement, and measurements are facts.

Two disciplines keep that distinction real rather than rhetorical. First, the
overlap only established *which chapters* carry the story; the division of those
chapters into 357 readings, their ordering, and every reading title and note
were done afterwards, without any scheme in view. Second, the plan's own content
diverges from the spine in both directions — it holds back three chapters of the
spine (Esdras 2, Nehemias 3, Nehemias 7, all registers) and adds a great deal
the spine does not contain. If the output were a transcription, it would not do
either.

One caveat, stated because the document is supposed to be checkable: the 334-
chapter overlap is an editorial measurement made against four external works.
It is not reproducible from anything in this repository, and it is the only
figure in this document that is not.

### The rights episode, which is worth telling honestly

The file was first drafted using Ascension's twelve period names verbatim — Early
World, Desert Wanderings, Royal Kingdom, Divided Kingdom, Return, Messianic
Fulfilment, The Church, and five that are plain historical terms anyway.

The reasoning at the time was not unreasonable. Dividing sacred history into
named periods is a *system*, and systems are not copyrightable; each label on its
own is a short descriptive phrase, and short phrases generally are not either.
But the set of twelve taken together was recognisably that scheme's — that is
exactly what makes a compilation protectable — and Ascension's terms ask that
their material not be reproduced or altered. The right answer was not to argue
the point.

So the labels were replaced with the periodization ordinary in biblical
scholarship, which any scheme arrives at independently: Primeval History, The
Wilderness, The United Monarchy, The Divided Monarchy, Return and Restoration,
The Life of Christ, The Apostolic Church.

The detail that makes this a design story rather than a compliance story: the
period *keys* did not change, and no reading moved. `early-world` is still
`early-world`; only its label reads "Primeval History". The keys had been made
stable and opaque for precisely this reason — so that a display string could be
replaced without touching a single reference. The rewrite was one column of one
file.

And the file says all of this, in its own `precedents` block, in the repository,
permanently. An abridgement that quietly fixed its own rights problem would have
left no way for a later reader to know a problem had existed.

### What it leaves out, stated in full — because the usual account is false

Abridged Bibles are routinely defended with the claim that they cut the boring
parts: the genealogies, the census lists, the sacrificial law. This is measured
here, and it is not true.

All figures are verse counts from the Douay-Rheims (Challoner) text indexed in
this repository, whose 73 books hold 35,804 verses.

Every genealogy and register the plan drops — Genesis 5, 10, 22:20–24, 25:12–18
and 36; Exodus 6:14–30; Esdras 2; Nehemias 3 and 7 — comes to **309 verses, 0.9%
of the Bible**. Add the whole of Leviticus, Exodus 25–31 and 35–40, Numbers 1–9
and 26–30, and Deuteronomy 12–26, and you add **2,217 verses, 6.2%**. Cut all of
it and you have removed about seven per cent. You are at 93% of the Bible, not
at a third of it.

The reduction comes from somewhere else entirely: three whole classes of book
that are not narrative, together 15,519 verses, **43.3% of the Bible**.

| Not read at any tier | Verses | Share (73-book canon) |
| --- | --- | --- |
| The prophets (incl. Lamentations, Baruch, Daniel) | 5,875 | 16.4% |
| The wisdom and poetical books | 6,881 | 19.2% |
| The epistles (all twenty-one, and Hebrews) | 2,763 | 7.7% |

A few things about that table.

**The denominator is doing visible work.** The figures usually quoted for these
classes — around 19.8% for the prophets, 14.4% for wisdom and poetry, 8.1% for
the epistles — are computed on a 66-book canon. Drop the deuterocanon and the
denominator shrinks, so the prophets' share rises; but Wisdom and Ecclesiasticus
are themselves wisdom books, so *that* class moves the other way and its
Catholic share is higher, not lower. The two figures are not in conflict and
neither is wrong. They are answers to different questions, and an abridgement
that quotes whichever is more flattering without saying which canon it counted
is doing something dishonest with arithmetic that looks like precision.

**What survives is small and should be described as small.** Of the prophets:
fifteen passages in thirteen readings, plus the narrative chapters of Daniel. Of
the psalms: sixteen of a hundred and fifty, each one because a narrative moment
demands it. Of the epistles: nothing. The plan follows the Church's expansion
through Acts and stops. That is the largest gap in its New Testament coverage,
and no narrative plan can close it, because the epistles are not narrative. The
file's own summary is the right one: *a reader who finishes this plan has not
read the prophets*.

**This is written down because concealment is the thing that gets punished.**
Every abridged Bible that hid its cost has been attacked for hiding it, and
rightly. The defensible claim is narrow and the file makes only that one: a
reader who wants the Bible should read the Bible; what this offers is the story
in order, at three depths, with the seams visible.

### The constraint the Church already set

The Old Testament lessons of the Easter Vigil are the oldest surviving
abridgement of salvation history in Catholic use. They are treated here as a
constraint rather than a model: all of them are read, at the extent the Missal
appoints, and each carries a note at its reading saying so.

Verified against the file, all eight ranges are present at exactly those extents
— Genesis 1:1–2:2, Genesis 22:1–18, Exodus 14:15–15:1, Isaias 54:5–14, Isaias
55:1–11, Baruch 3:9–15 with 3:32–4:4, and Ezechiel 36:16–28. (Seven lessons,
eight ranges: the Baruch lesson skips a stretch, so it is two ranges in one
reading.) Three of them fall at the overview tier, which is to say a reader who
does only the 36-sitting pass still gets creation, the binding of Isaac, and the
crossing of the sea at the Missal's own boundaries.

### Precedents that are free to use

Where the modern schemes could only be measured, two Catholic works could be
drawn on directly, because both are out of copyright:

- **Friedrich Justus Knecht, *A Practical Commentary on Holy Scripture* (1910)** —
  its selection of Old Testament narratives for continuous reading stands behind
  the shape of the first six periods.
- **Ignaz Schuster, *Bible History*** (*Handbuch zur biblischen Geschichte*), in
  its nineteenth-century English editions — its two-testament arrangement, and
  its insistence that the deuterocanonical histories carry the period between
  the Testaments, stand behind the Maccabean period here.

That the reusable precedents are a century old and the unusable ones are recent
is not a coincidence, and it is not really a constraint either. Knecht and
Schuster were solving the same problem for the same Church.

### Numbering, which is where a plan like this usually goes quietly wrong

Chapter and verse are Vulgate throughout, and every endpoint is validated against
the actual printed verse text of the tracked Challoner edition — not against a
chapter-length table. A reading that names a verse the edition does not print is
a reading that addresses nothing, and the validator refuses it.

Two consequences the file handles explicitly rather than hoping nobody notices:

- **The psalms are Vulgate-numbered.** The shepherd psalm is 22, not 23. All
  sixteen psalm readings carry a note giving the Hebrew equivalent, and the
  numbering conversion happens in the tooling, so no numbering logic ever
  reaches the browser.
- **Book names are modern.** Douay's 1–4 Kings appear as 1–2 Samuel and 1–2
  Kings; the Douay titles are given in the period summaries and at the first
  reading of each affected book. Tobias, Judith, Esther and Ecclesiasticus are
  divided differently in the Vulgate than in the Greek behind most modern
  versions, and the readings concerned say so rather than leaving a reader to
  discover it by landing in the wrong place.

---

## Part two — the commentary harvest

### The thing it deliberately does not do

`tools/harvest` never calls a model.

That is the whole design, and it is worth understanding why a tool built to
process model output would refuse to produce any. A model consulted twice does
not answer twice the same. If the tool called out, then the tool's output would
depend on when you ran it, and every downstream artifact would inherit that
irreproducibility with no marker on it.

So the nondeterminism is pushed out of the tool and into a tracked file, where it
is visible. The harvester:

- **plans** — emits a worklist of loci still short of their target run count;
- **records** — ingests one run's results into a dated ledger, validated, with
  the model's identity and an `--audited-on` date stored beside what it said;
- **promotes** — collates the ledger into a discovery index, deriving each
  work's confidence from *agreement across runs*, never from a score the model
  supplied.

Everything the tool itself does is deterministic. The judgement stays in the
ledger with its provenance attached, and a run can be re-read, re-counted, or
thrown out years later because you can see whose answer it was.

The output is also narrower than it sounds. The harvest produces an
**acquisition list** — which works to go and obtain — not commentary text and not
a citation. Nothing enters the source library on a harvest alone.

### One more design decision that pays for itself

A query covers at most one chapter. Isaias 63:16–64:7 is two loci, not one.

Grouping across chapters would silently drop any work that comments on only one
of them, and "silently" is the operative word: the result would look like a
complete answer. Splitting costs more queries and loses nothing. The 1,296
verse-range references the missals cite collapse to 491 chapter-bounded loci.

### The measurement, which is the actual result

Three independent passes over all 491 loci, all by `claude-opus-5`, all dated
2026-07-31, produced **15,803 attributions** (5,927 + 4,963 + 4,913). Across them
sit 6,511 distinct (locus, author) pairs and 10,293 distinct (locus, author,
title) triples.

Corroboration — appearing in at least two of the three passes:

| Matched on | Corroborated | Total | Rate |
| --- | --- | --- | --- |
| Author | 5,095 | 6,511 | **78.3%** |
| Author **and** title | 3,635 | 10,293 | **35.3%** |

A 43-point gap.

And it is not noise. Measure the same two rates on each *pair* of passes and the
gap is 41.0, 41.0 and 44.3 points. Going from two passes to three moved the
absolute rates around and left the gap almost exactly where it was. A gap that
survives changing the number of observations is a property of the thing being
measured.

### What the gap actually means

It means **the research is sound and the identity matching is the weak link**.

Ask three times who wrote on a passage and roughly four in five answers agree.
Ask what the commentary is *called* and only about one in three agree — because
the same work has many names. Jerome's commentary on Jeremias appeared under
five spellings: *In Hieremiam libri VI*, *Commentarii in Hieremiam*, *Commentarii
in Ieremiam*, *In Hieremiam prophetam libri VI*, *Commentariorum in Hieremiam
libri VI*. Origen on Matthew appeared under three. Of the corroborated (locus,
author) pairs, **54.9% carry more than one title spelling** across the passes.

The contrast between two authors makes the mechanism vivid. Nicholas of Lyra
drew 1,470 attributions under exactly **one** title — he wrote one *Postilla* over
the whole Bible and there is nothing to disagree about. Denis the Carthusian drew
1,470 attributions under **92** titles, because he wrote per-book *enarrationes*,
so a pass may name the whole (*Enarrationes in omnes libros sacrae Scripturae*)
or the part (*Enarratio in librum primum Paralipomenon*) and both are correct.
Across the three passes: 79 distinct authors, 718 distinct title spellings.

So the variance is not mostly error. Part of it is genuine bibliographic
ambiguity — Latin titles with no standard form, and works that legitimately have
a whole-and-part relationship. That is a *cataloguing* problem, and it wants a
work-identity registry, not more passes.

### Why extent gating is the whole game

The failure a lead list like this invites is confident nonsense: naming a great
commentator on a passage his commentary does not reach. A reader clicks through,
finds nothing, and reasonably stops trusting the rest.

The three passes handled this well, and — more to the point — they handled it
*the same way*, independently, which is the only evidence that means anything.
The tracked ledger shows:

| Work | Real extent | What the passes did |
| --- | --- | --- |
| Aquinas, *Postilla super Psalmos* | stops at Psalm 54 | cited on exactly the 45 harvested psalm loci at or below 54 — all of them — and on none of the 78 above it |
| Jerome on Jeremias | breaks off around chapter 32 | cited on Jeremias 1, 17, 20, 23, 29, 31 — never on 33 or 38, the two harvested loci above the break |
| Origen on Matthew | survives only from 13:36 | cited on Matthew 13–28 and never on 1–11, though eleven such loci were harvested |
| Gregory the Great, *Homiliae in Hiezechihelem* | covers only chapters 1–4 and 40 | of eight harvested Ezechiel loci, cited on chapter 2 alone |
| Cornelius a Lapide | wrote on nearly all of scripture, but never on Job or the Psalms | **zero** of the 89 Job attributions and **zero** of the 4,399 Psalms attributions, while appearing across 58 other books |

The Lapide row is the strongest of the five. He is the most reflexively cited
Catholic commentator there is; the passes cite him constantly; and across 4,399
chances on the Psalms not one pass reached for him. That is a negative held
consistently under heavy pressure to get it wrong.

### Agreement on a negative

One locus came back empty from all three passes, and only one: **4 Esdras 2**.

It is in the harvest because both missals cite it: the Introit of Tuesday within
the Octave of Pentecost, *Accipite jucunditatem gloriae vestrae*, at 4 Esdras
2:36–37. (The same book is the traditional source of the Requiem's *Requiem
aeternam*, at 2:34–35, though that mass is not yet among the transcribed
propers here.) And 4 Esdras is not among the 73 books of the canon this library
holds — it appears nowhere in the Douay book index. It is liturgically present
and canonically absent, and pre-1900 commentators overwhelmingly did not write
on it.

Three passes, three empty lists, no hedging and no plausible-sounding filler.
Returning nothing is the hardest thing to get from a model and the most
informative thing to get from one, and here it is the correct answer.

### Why nothing has been promoted

`src/sources/commentary/passage-commentary-index.yaml` is still an empty stub:
`passages: []`. Running the promotion now would write 9,034 work entries across
497 passages — and a large share of those entries would be the same work counted
twice under two titles, each fragment carrying a confidence of 0.33 or 0.67
instead of the 1.0 the work actually earned.

You can watch it happen in the collation output as it stands: **Denis the
Carthusian occupies four of the top fifteen slots**, as four different titles of
what is substantially one commentary. Splitting a work in two does not merely
duplicate a row; it demotes both halves below works that are genuinely less
attested, which corrupts the ranking that the acquisition list exists to
provide.

Open tasks, in the order they need doing:

1. **Build a work-identity registry.** Reconcile harvested candidates to the
   `work.*` identities `tools/source-library` already uses, so a harvested
   candidate can become a vault record without a second identity
   reconciliation. The harvester already supports `work_id` and an `aliases`
   field, and already collapses aliases onto a canonical key — the alias table
   is simply empty. Nothing else in the chain needs to change.
2. **Resolve whole-versus-part titling** for the authors whose works are
   per-book. This is a cataloguing decision, not a data problem: pick the rule,
   then apply it as aliases.
3. **Reconcile the two locus granularities in the ledger.** Three early pilot
   runs used verse-range keys (`Psalms 24:1-24:3`); the three full passes use
   chapter keys (`Psalms 24`). They do not collide, so promotion currently emits
   497 passages where 491 were harvested, with seven of them carrying pilot data
   at a finer grain.
4. **Then promote**, with a confidence floor, and review candidates into the
   vault under `guidance/sources.md` — the way a source family's presence is
   promoted to `reviewed`.

### What this is, plainly

Model-generated leads requiring collation. Not citations, not evidence, not
scholarship. The value is that 491 loci now have a ranked list of plausible
pre-1900 commentators with a measured agreement figure attached to each, so that
a human deciding what to acquire starts from an ordered list instead of a blank
page — and knows, per entry, whether three independent askings agreed or only
one did.

The single most useful thing the harvest produced is not the list. It is the
78.3%/35.3% split, which says where to spend the next effort: not on more passes,
but on knowing what the works are called.

---

## What the two have in common

Both undertakings had to record something inconvenient about themselves in the
artifact, permanently.

The reading plan records that it once used period labels it had no right to, and
what it does not read, in verse counts, on the correct denominator. The harvest
records the model that produced each run and the date, and a corroboration rate
that is bad enough to block the next step.

Neither disclosure was required by anything. Both are load-bearing anyway,
because the alternative in each case is an artifact that looks finished and
cannot be checked — and an abridgement nobody can audit is exactly the thing
readers have learned to distrust.

---

*Sources: `src/sources/reading-plans/narrative-spine.yaml`,
`src/sources/commentary/harvest-ledger.yaml`,
`src/sources/commentary/README.md`, `tools/reading-plan`, `tools/harvest`.
Verification commands, invariants and failure modes:
[`guidance/reading-plan-for-agents.md`](../guidance/reading-plan-for-agents.md).*
