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
commentaries actually treat each passage the missals cite. Consulting a model is
not a reproducible act, so exactly one verb of the tool does it, and what that
verb produces lands in a tracked ledger stamped with the model that answered and
the date. Three separate askings are then measured against each other. The
measurement came back with an uncomfortable and useful answer — the passes agreed
on *who* wrote on a passage far more often than on *what the work was called* —
and that answer blocked promotion until a derived table of work identities closed
the gap. Promotion ran on 2026-07-31. The discovery index now holds 497 passages
and 7,297 work entries, under no confidence floor, and over a locus-granularity
mismatch that is still unsettled.

This document explains what each undertaking decided and why. Every number in it
was recomputed from the repository's own tracked files — where a figure disagreed
with what the files claim about themselves, the measurement is given and the
disagreement said out loud. The recompute commands, the invariants, and the
failure modes are in
[`guidance/reading-plan-for-agents.md`](https://github.com/spincyc/triptych/blob/main/guidance/reading-plan-for-agents.md).

**[The Story of Salvation](../scripture/)** — the plan itself, in three
lengths, with the translation of your choosing.

---

## Part one — The Story of Salvation, the reading plan

### What the plan is

`src/sources/reading-plans/narrative-spine.yaml` holds 357 readings in 12
periods, running from creation to the end of Acts and closing on Apocalypse
21:1–22:5. It touches 454 chapters in 31 of the canon's 73 books.

It is a *route*, not a text. The file carries references — book, chapter, verse
— and nothing else that a reader would call scripture. The words come from
whichever tracked translation the reader chooses.

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

### The harvester calls a model in exactly one verb

A model consulted twice does not answer twice the same. If that were spread
through the tool, every downstream artifact would inherit the irreproducibility
with no marker on it.

So it is confined to one verb, and what that verb hears goes into a tracked file
where it is visible. The harvester:

- **plans** — emits a worklist of loci still short of their target run count;
- **asks** — the only verb that reaches outside this machine: the `claude` CLI,
  once per passage per run, three runs by default, with no tools, no session on
  disk and this repository's own customization switched off, each answer
  validated against a schema derived from what `record` accepts. It writes
  results files and records nothing;
- **records** — ingests one run's results into a dated ledger, validated, with
  the model's identity and the date stored beside what it said;
- **aliases** — derives the work-identity table from the alias claims the runs
  themselves made;
- **promotes** — collates the ledger into a discovery index, deriving each
  work's confidence from *agreement across runs*, never from a score the model
  supplied.

Until 2026-07-31 there was no `ask` and the harvest was run by hand outside the
tool. That was not free: the model identity and date the ledger carried were
whatever an operator typed. `ask` takes both from the answer instead. `--model
opus` is a request and an alias; what gets recorded is read from the `model` that
each assistant message declares. The first implementation read it from the
response's `modelUsage` tally and was wrong — an opus query bills
`claude-haiku-4-5` alongside `claude-opus-5`, because the CLI uses a helper
model, so the tally cannot say which of them wrote the answer. Where the
assistant messages disagree, the run stops rather than picking one.

Two smaller things `ask` was built to say out loud. The ledger keys a run by a
digest of its content, so two runs that answered identically are one run there —
the same guard that makes re-recording a file a no-op, but silently it would
leave an operator believing three runs of corroboration landed where one did, and
confidence is appearances over runs; so it is reported as `identical_runs`. And
running with the repository's customization switched off is load-bearing: the
first probe without it inherited this repository's own `CLAUDE.md` and hooks and
answered about a hook instead of about the Psalms.

Everything else the tool does is deterministic. The judgement stays in the
ledger with its provenance attached, and a run can be re-read, re-counted, or
thrown out years later because you can see whose answer it was.

The output is also narrower than it sounds. The harvest produces an
**acquisition list** — which works to go and obtain — not commentary text and not
a citation. Nothing enters the source library on a harvest alone.

### A query never spans two chapters

Isaias 63:16–64:7 is two loci, not one.

Grouping across chapters would silently drop any work that comments on only one
of them, and "silently" is the operative word: the result would look like a
complete answer. Splitting costs more queries and loses nothing. The 1,600
verse-range references the two missals cite collapse to 525 chapter-bounded loci.
The three passes ran over 491 of them: the corpus has grown since they were
asked, and 34 loci have never been asked about at all.

### The measurement, which is the actual result

Three independent passes over all 491 loci, all by `claude-opus-5`, all dated
2026-07-31, produced **15,803 attributions** (5,927 + 4,963 + 4,913). Across them
sit 6,511 distinct (locus, author) pairs and 10,293 distinct (locus, author,
title) triples. Titles are compared case-insensitively throughout this section,
as the tooling compares them; compared byte-for-byte the triples come to 10,619.

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

### The registry was built, and the gap closed

`src/sources/commentary/work-aliases.yaml` holds **300 groups over 2,862 title
spellings**, covering 77 authors. It is derived, not hand-typed: `groups` is the
connected components of the "these names are the same work" graph that the runs
themselves asserted, per author, regenerated whole and validated on load. It is
stamped `derived_on: 2026-07-31` and carries a digest of the alias claims it was
built from, so recording a run that asserts a new alias ages the table and
`promote` refuses until the new grouping has been looked at.

Collapsing titles through it, on the same three passes:

| Matched on | Corroborated | Total | Rate |
| --- | --- | --- | --- |
| Author | 5,095 | 6,511 | 78.3% |
| Author **and** title, as written | 3,635 | 10,293 | 35.3% |
| Author **and** work, through the table | 5,060 | 7,156 | **70.7%** |

The 42.9-point gap becomes 7.5. Corroborated (locus, author) pairs carrying more
than one name for the work fall from 54.9% to 11.8%; 718 title spellings resolve
to 283 works. Where the passes agree on the author, they now agree on the work
**98.2%** of the time. The document's own reading of the gap — that the research
was sound and the identity matching was the weak link — is what the fix confirms:
nothing was asked again, and 1,425 more (locus, work) claims came out corroborated.

One thing the table records because it could not be derived. Blind title
normalisation was rejected, and the reason is in the file's `review` block: Peter
Lombard's *Magna Glossatura* names both his Psalms gloss and his *Collectanea* on
Paul, and two of the three runs offered it as an alias of each, so normalising
would have merged two works into one. No corroboration threshold catches that —
both runs were right about the name and wrong about what it picks out.

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
| Cornelius a Lapide | wrote on nearly all of scripture, but never on Job or the Psalms | **zero** of the 89 Job attributions and **zero** of the 4,399 Psalms attributions, while appearing across 59 other books |

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

### What was promoted, and what is still open

Promotion ran on **2026-07-31**, once the alias table existed.
`src/sources/commentary/passage-commentary-index.yaml` holds **497 passages and
7,297 work entries**, naming 341 distinct works by 86 authors, stamped
`updated: 2026-07-31` and `harvest_runs: 6`. The 6 counts the ledger's runs; no
passage was seen by more than three, and every entry accordingly reads `runs: 3`.

**No confidence floor was applied.** The index records `min_confidence: 0.0`, and
confidence is appearances over runs:

| Confidence | Entries | Share |
| --- | --- | --- |
| 1.0 — all three passes | 3,631 | 49.8% |
| 0.6667 — two of three | 1,499 | 20.5% |
| 0.3333 — one of three | 2,167 | 29.7% |

So very nearly three in ten entries rest on a single asking, and they sit in the
file beside the ones that three askings agreed on, distinguished only by the
number.

**The work-identity split is reduced, not gone.** Denis the Carthusian takes two
of the collation's top fifteen slots — the 2nd and the 11th — and the index
carries four Denis titles in all. The table gathers 304 of his per-book names
under *Enarrationes in universam Bibliam* (495 passages, confidence 1.00) but
keeps *Enarrationes in omnes libros sacrae Scripturae* (326 passages, 0.67)
separate, because no run asserted the two whole-Bible names of each other. The
whole-versus-part question is settled for the parts and open for the wholes.
(This section used to say Denis held four of the top fifteen. That figure is not
reproducible and is not restated: `promote`'s identity map was first-hit rather
than a union at the time, so the ranking depended on the order the ledger was
walked.)

**The granularity mismatch is real and unresolved.** 490 of the index's keys are
chapters; 7 are verse ranges, left by the three pilot runs of 2026-07-30, which
keyed verse ranges where the three full passes key chapters. The two key spaces
disagree about the same text:

| Verse-range key | Works | Chapter row | Works | On the range but not the chapter |
| --- | --- | --- | --- | --- |
| Luke 21:25-21:33 | 27 | Luke 21 | 16 | 14 |
| Romans 13:11-13:14 | 22 | Romans 13 | 15 | 13 |
| Psalms 24:1-24:3 | 22 | Psalms 24 | 18 | 10 |
| Psalms 24:3 | 17 | Psalms 24 | 18 | 5 |
| Psalms 24:4 | 19 | Psalms 24 | 18 | 7 |
| Psalms 84:8 | 17 | Psalms 84 | 15 | 8 |
| Psalms 84:13 | 17 | Psalms 84 | 15 | 8 |

Reconciling the two granularities was named here as something that had to happen
before promotion. It did not happen, and promotion ran anyway. The commit that
promoted records the identity fix as what unblocked it and says nothing about the
granularity; this document does not know why it ran, and will not guess.

Two smaller facts about the shape of the file. 490 chapter rows, not 491, because
4 Esdras 2 came back empty from all three passes and `promote` writes no row for
a passage with no works. And the corpus has outgrown the harvest since: it now
resolves to 525 chapter loci, of which 491 have been asked about.

### What this is, plainly

Model-generated leads requiring collation. Not citations, not evidence, not
scholarship. The value is that 497 passages now carry a ranked list of plausible
pre-1900 commentators with a measured agreement figure attached to each, so that
a human deciding what to acquire starts from an ordered list instead of a blank
page — and knows, per entry, whether three independent askings agreed or only
one did. Nearly three in ten entries are the one-did case.

The most useful thing the harvest produced is not the list. It is the 78.3%/35.3%
split, which said where to spend the next effort: not on more passes, but on
knowing what the works are called. That effort was spent, and it moved the title
figure to 70.7% without asking anything again.

---

## What the two have in common

Both undertakings had to record something inconvenient about themselves in the
artifact, permanently.

The reading plan records that it once used period labels it had no right to, and
what it does not read, in verse counts, on the correct denominator. The harvest
records the model that produced each run and the date, a corroboration rate that
was bad enough to block the next step until a derived table lifted it, and the
precondition that was still unmet when the next step was taken anyway.

Neither disclosure was required by anything. Both are load-bearing anyway,
because the alternative in each case is an artifact that looks finished and
cannot be checked — and an abridgement nobody can audit is exactly the thing
readers have learned to distrust.

---

*Sources: `src/sources/reading-plans/narrative-spine.yaml`,
`src/sources/commentary/harvest-ledger.yaml`,
`src/sources/commentary/work-aliases.yaml`,
`src/sources/commentary/passage-commentary-index.yaml`,
`src/sources/commentary/mass-commentary-corpus.yaml`,
`src/sources/commentary/README.md`, `tools/reading-plan`, `tools/harvest`.
Verification commands, invariants and failure modes:
[`guidance/reading-plan-for-agents.md`](https://github.com/spincyc/triptych/blob/main/guidance/reading-plan-for-agents.md).*
