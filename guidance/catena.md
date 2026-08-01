# The catena: presenting commentary beside the passage it comments on

A design study for a page that walks the Bible chapter by chapter, shows the
chapter's text in a translation the reader chooses, and beneath it shows every
commentary fragment this project holds on that chapter, in chronological order.

The name is descriptive. A *catena* is the genre — a chain of excerpted comment
running beside the text — and this is not a reproduction of Aquinas's
*Catena Aurea*, which is one particular thirteenth-century catena on the four
gospels and a work this project may later carry as a source. Where the two could
be confused, the work wins the name and the page takes another.

This began as a design study written before anything was built, so that the
addressing, granularity and storage decisions would be settled *before*
acquisition — those being the decisions that are expensive to revisit once
several thousand fragments have landed under the wrong key. That worked, and the
study has since been overtaken by its own subject: the page is live at `/catena/`,
the edge exists, and a Genesis pilot has put 44 fragments through the whole
apparatus, 23 English and 21 Latin, over six solved chapters. Where the study first got a figure or a rule wrong, the correction is
made **in place and marked**, because a design document that quietly agrees with
whatever was built is no longer evidence of anything.

## Evidence conventions

- **[verified]** — measured during this study against this repository's tracked
  artifacts. Reproducible.
- **[sourced]** — reported from an external document, cited, read but not
  independently re-derived.
- **[inferred]** — reasoned from the above. Flagged wherever it matters.

---

## 1. Three layers, and the rule that keeps them apart

The single most important thing this design has to prevent is a lead being
displayed as though it were a text. Three distinct things get confused under the
word "commentary", and the page must render exactly one of them.

| Layer | The claim it makes | Where it lives today | What backs it |
| --- | --- | --- | --- |
| **L1 attribution** | *Chrysostom commented here* | `src/sources/commentary/passage-commentary-index.yaml` | agreement across independent model runs |
| **L2 holding** | *we possess this work, in this edition, under this licence* | the source library | an artifact on disk |
| **L3 fragment** | *these words, by this author, on this locus* | the source library's `passage` records | the text itself |

L1 exists and is large: **562 rows, 61 books, 579 distinct works, 184 authors**,
across 9,083 entries, from 13 harvest runs [verified 2026-08-01]. Re-derive it
from `passage-commentary-index.yaml` rather than quoting this line; it moves
with every run.

L3 also exists, which an earlier draft of this study got wrong and is worth
correcting in place rather than quietly. No field anywhere in
`src/sources/commentary/` can hold the text of a fragment — that much is right
[verified], and it is by design, because the harvest produces an acquisition
list. But the **source library's `passage` record has held third-party prose all
along**: `text`, `transcription_segments`, `physical_line_ranges`, `artifact_id`,
`artifact_sha256`, `states`, `context`, `verified_on`. There are **1,274 such
records**, and four of them are already patristic commentary [verified] — among
them Augustine on John 20:8 and three homilies of Chrysostom on John, each
carrying its text, its transcription segments, a `states` list running
`cataloged → acquired → inspected → verified`, and a verification date. Fifteen
volumes of Schaff's *Nicene and Post-Nicene Fathers* are tracked works.

So the catena does not need a fragment container invented for it. It needs the
container it already has to be pointed at scripture, which is §7.

The gap between L1 and L3 is not a matter of degree. `docs/reading-and-commentary.md`
already states what L1 is: *"The harvest produces an **acquisition list** — which
works to go and obtain — not commentary text and not a citation."* Waiting for L1
to grow will never produce L3. Only acquisition will.

> **Rule 1.** The catena renders L3 and only L3. A chapter with no fragments
> shows no fragments.

L1 may be shown, but only in its own right and under its own label — *works we
believe comment here and have not yet acquired* — never interleaved with
fragments and never carrying the visual weight of one. A row reading
"John Chrysostom — *Homiliae in epistulam i ad Corinthios* (confidence 0.67)"
with no text beneath it is a research note. Rendered in a chain of real excerpts
it reads as a commentary the reader failed to load.

The corollary is worth stating because it saves later work:

> **Rule 2.** Once a work's fragments are held for a locus, that work's L1
> confidence is irrelevant *for presence* at that locus.

We do not need three model runs to agree that Chrysostom commented on
1 Corinthians 1 when his text on 1 Corinthians 1 is on disk. The confidence
figure is a property of the acquisition list and it must not follow the fragment
onto the page, where it would invite a reader to discount a text that is simply
present.

---

## 2. The anchor is canonical; the display is projected

A fragment comments on a locus. Which numbering is that locus in?

Chrysostom comments on a Greek text; Cornelius a Lapide on the Vulgate; the
reader may be looking at the Douay-Rheims or the King James. These disagree about
verse numbers throughout and about chapter numbers across the Psalter. A fragment
stored against "Psalm 9:22" with no numbering declared is anchored to nothing,
and will resolve — successfully and wrongly — against whichever edition the page
happens to render.

The apparatus for this already exists. `guidance/versification.md` §8.0 settles
the projection: a set of rules, not a set of verses, where identity writes no row
and each row maps a canonical citation to a locus in an edition's own numbering.
`scripts/_projection.py` derives it. Current sizes: Clementine Vulgate 16 rules,
Douay-Rheims 23, King James 4,313 [verified].

> **Rule 3.** Every fragment anchors to a **canonical** locus — Vulgate
> numbering, the `CANONICAL` constant the projection projects into. The reader's
> chosen edition is reached through that edition's projection, at render time.
> A fragment is never stored twice for two editions.

This makes the catena the first real consumer of the projection, which until now
nothing has consumed. That is a point in the design's favour: it turns an
apparatus built on principle into one under load.

It also inherits the projection's refusals, and must honour them rather than
route around them. Sixteen psalms are flagged `english_offset_uniform: no` —
their verse numbers correspond while their body boundaries do not — and the
projection deliberately declines to say where the boundary moves, because no
source this project can reach models it.

> **Rule 4.** Where the projection refuses, the page refuses. It shows the
> fragment against its canonical address and states that the boundary in the
> selected edition is not established. It does not fall back to the same verse
> number, which is precisely the wrong answer dressed as the right one.

---

## 3. Granularity: store the extent, derive the chapter

The page is chapter-shaped. That is a fact about the page and it must not become
a fact about the storage.

**Settled by TASK-101; recorded here because the reasoning outlived the defect.**
The index once carried two granularities that disagreed: of 497 rows, 490 were
chapter-keyed and 7 were verse-or-range survivors of the early pilot runs, all of
them First Sunday of Advent propers. They were not duplicates — `Luke 21:25-21:33`
carried 27 works of which 14 appeared on no chapter row — so the index answered
the same question two ways and the answers differed, both looking complete.

It now holds **490 chapter rows and 7,203 work entries** [verified], and the fold
lost nothing: 7,203 = 7,203, with all 42 works that had sat only on a pilot row
now on their chapter rows.

The ruling corrected a misreading of this very document, which is worth keeping.
Rule 5 below says *store the natural extent* — but Rule 5 governs **fragments**,
and §3 draws that line itself: fragments are not asked for, they are held. The
discovery index is **L1**, an acquisition list built from asking, and its natural
extent *is* the chapter, because "which works comment on Luke 21" is the whole of
what was asked and answered. A verse-range key asserted something the harvest
never learned — that those works address verses 25–33 specifically — which is
this repository's named worst failure wearing a finer address.

So: the index stores the chapter and derives everything finer. Fragments store
their extent. The two layers take opposite defaults, for the same reason.

> **Rule 5.** A fragment is stored at its **natural extent** — the range the
> commentator actually addressed — and the chapter view is **derived**. One
> stored granularity, one derived table, and no hand-keyed restatement beside
> it.

Extent is not a formality. `docs/reading-and-commentary.md` measures why: works
have real limits — Aquinas's *Postilla super Psalmos* stops at Psalm 54, Origen
on Matthew survives only from 13:36 — and the value of the corpus is that it
respects them.

A separate rule already governs the harvest: *"a query never spans two
chapters"*, because grouping across a chapter boundary would silently drop a work
commenting on only one side. That is a rule about **asking**. Fragments are not
asked for; they are held, and a homily on Isaias 63:16–64:7 genuinely spans the
boundary.

> **Rule 6.** A fragment may declare an extent spanning chapters. It then appears
> under every chapter it touches, once, with its full extent shown. It is never
> split at the boundary, because splitting would attribute to one chapter words
> written about another.

---

## 4. Chronological order needs a stated rule, not a sort

"In chronological order" is underdetermined, and each ambiguity has a wrong
answer that looks right.

- **By what date?** Author death year is what the corpus already carries
  [verified] and is the conventional ordering. Composition date would be better
  and is unknown for most of the corpus.
- **Pseudonymous works.** A text circulating as Dionysius the Areopagite is not
  first-century. It orders by the date of the *text*, not of the claimed author,
  and the page says whose text it actually is. Getting this wrong would place a
  sixth-century work at the head of the chain, which is not a rendering error but
  a historical claim.
- **Ties and unknowns.** Same year, and no year, both need a deterministic
  secondary key or the page reorders itself between builds for no reason.

> **Rule 7.** Order by the date of the text. Where a work's attribution is
> disputed, the page carries the dispute rather than resolving it silently.

---

## 5. The label is rendered, so the label must not lie

A catena prints, above each fragment, the author and the title of the work it
came from. That is the first time this project will have rendered a work title
beside a passage, and it converts a currently invisible defect into a visible
one.

**Settled by TASK-100.** This study first reported *two* groups whose canonical
title named fewer books than the group spans — Aquinas and Theophylact, both
labelled *ad Romanos*, against 148 index rows naming the wrong book, 61 at
confidence 1.0. Both figures were low. The check written to enforce Rule 8 found
**four** groups, and the true count of mislabelled rows was **151**, of which 57
sat at confidence 1.0 — all three independent runs agreeing, which does not make
it right, because they share the bias. It is now 0.

    Thomas Aquinas       => Super Epistolas S. Pauli lectura
    Theophylact of Ohrid => In omnes D. Pauli apostoli epistolas enarrationes
    Theophylact of Ohrid => Commentarius in epistulas catholicas
    Albert the Great     => Commentarii in duodecim prophetas minores

The groupings were correct throughout; only the names were wrong, which is why
this was a cataloguing decision and not a data problem — as the four-item list in
`docs/reading-and-commentary.md` predicted when it asked whether a per-book
commentary is named by the whole or by the part.

Two lessons the correction leaves behind. A hand-written detector reported the
smaller number because it recognised only the Latin book-names it had been given;
the landed check derives its vocabulary from the ledger instead — a word counts as
a book name only if every attributed title carrying it landed on one book, at
least two authors use it, and at least three distinct titles do. That yields 45
words and correctly refuses genre words: *explanatio* heads 418 psalm attributions
and still fails, because it also heads titles on the Apocalypse and on John. And
the check is **sound where incomplete**: an unproved word is never read as a book
name, so it under-reports rather than inventing. One of the four was found by
measurement rather than by the check, which is what that trade-off costs.

> **Rule 8.** No fragment renders until its work's canonical title covers the
> work's actual extent. The check is cheap: a group's canonical title must not
> name a book that the group's titles do not all share.

---

## 6. Licence is a property of the fragment, not of the author

Nothing about a father being dead for sixteen centuries makes a text of him free
to republish. The Greek may be public domain while a modern critical edition of
it is not, and a modern translation of it is a new copyrightable work with its
own term.

This project has already paid for learning that lesson once: the Knox bible is
in copyright under US renewals R525394 and R646862 until 2039 and 2043
respectively, and the guard that keeps it off the site is that its retrieval tool
refuses any destination inside the repository.

> **Rule 9.** A fragment record names the **edition** it was taken from, and the
> licence is carried by that edition, exactly as bible editions carry theirs. The
> page filters on it. An unlicensed fragment is not hidden at render time; it
> never enters the published artifact.

The consequence for acquisition is that the licence column decides the corpus.
A source that cannot be redistributed is worth much less here than one that can,
whatever its scholarly superiority — and that ranking should drive the
acquisition round, not be discovered during it.

---

## 7. The missing edge, which is the only new thing

A `passage` record already carries the text, the provenance, the rights and the
review state. What it does not carry is **what scripture the text is about**.

Look at the `locus` on the Augustine record [verified]:

```
locus = "Augustine, In Iohannis Evangelium Tractatus CXX.9"
```

That is an address in the *commentary's* own work — tractate 120, section 9 —
not in scripture. `context` says what the passage is about, in prose. So nothing
can answer *"every passage record commenting on Genesis 1"*, and that question is
the entire machinery of a catena.

> **Rule 10.** The new thing is one typed, validated edge from a fragment to a
> **canonical scripture extent**. Not a prose field, not a free-text list. It
> carries the extent in `CANONICAL` numbering (Rule 3) at the fragment's natural
> reach (Rule 5).

Everything else the earlier draft proposed as a schema is already provided:

| Need | Already provided by |
| --- | --- |
| the text | `passage.text`, `passage.transcription_segments` |
| the locator | `passage.locus`, `physical_line_ranges`, `artifact_page_ranges` |
| the edition, and so the licence | `passage.edition_id` → `artifact.toml`'s `rights_status`, `rights_basis`, `rights_jurisdiction` |
| language | `edition.language` |
| provenance and review state | `states`, `verified_on`, `artifact_sha256` |
| **the scripture it comments on** | **nothing — Rule 10** |

One point from the earlier draft survives unchanged and matters: a translation is
**not** a field on a fragment. It is a separate fragment of the same work in
another language, with its own edition and its own licence — which is exactly
what lets a father's Greek be publishable while a modern English rendering of him
is not. The source library already models this, because an edition carries the
language and the artifact carries the rights.

### The axis the reader chooses along is not the language code

Settled 2026-08-01, on the maintainer's direction that the commentary control
should read *original / English* rather than *la / grc / en*.

The language code is a true fact about an edition and a **misleading one about
the claim**. Three editions of Basil's *Hexaemeron* stand in this corpus:
Severian's neighbour in the original Greek, Eustathius's fifth-century Latin
version of Basil made for the deaconess Syncletica, and Blomfield Jackson's
1895 English. On a language axis the middle one prints "Latin" —
indistinguishably from Ambrose writing Latin himself. A reader asking for the
father's own words would be handed a translation with nothing on the page
saying so, which is [the shape](the-shape.md) §1 in the selector.

> **Rule 11.** A fragment declares whether it carries the author's **own
> language** or a **translation** of it, and the control runs along that axis.
> The declaration is derived, never typed: `original` where the edition's
> language is one the work was written in, `translation` otherwise.

Three consequences worth stating, because each was a decision:

- **The derivation is cross-checked against a second, independent signal.** An
  edition that translates names translators; an edition in the author's own
  language does not. `catena check` refuses a fragment whose two signals
  disagree, because either alone reads perfectly when it is wrong. It has teeth
  in both directions: a translation naming nobody is one this page would publish
  as the author's own words, and an original naming translators is either
  mislabelled or a version nobody has declared.
- **Two ISO code spaces meet at that comparison.** Work records name a language
  in 639-2/B (`lat`), edition records in 639-1 (`la`). Compared raw, Migne's
  Latin of a Latin father is a *translation* of him — a well-formed answer,
  reached correctly, and wrong. Both sides fold through one closed table first,
  and a code the table does not know is an error rather than a guess: an
  unfoldable code compares unequal to everything, so dropping it would make
  every edition of that work read as a translation.
- **The original is one offer and translations are one per language.** A reader
  asking for the author's own words is asking a single question, so a chapter
  holding Ambrose's Latin beside Severian's Greek offers *the author's own
  language* once. Translations are offered by the language they translate into,
  because English and Latin are different offers.

Where a chapter holds nothing in the chosen voice the page says so and names
what it does hold, exactly as it already did for a language. Genesis 1 is the
worked case: 107 fragments, 84 in their authors' own language, 14 in English
translation and 9 in Latin translation [verified 2026-08-01].

### Three prerequisites the survey turned up

- ~~**No structure file enumerates the canon.**~~ **Done.** It was true when
  written: every coverage was citation-driven — the bible index covers what the
  calendars cite, the propers structure covers the propers, the readings
  structure covers 454 chapters in 31 books — and a catena over *every* chapter
  needs a whole-canon enumeration that no tool wrote. `scripts/_catena.py canon`
  now prints it and `structure` writes it, so
  `src/web/data/structure/catena/index.json` carries all 73 books with their
  chapter counts, tokens and paths [verified]. The prerequisite is recorded
  rather than deleted because it is why the enumeration is derived in one place
  instead of typed into the browser.
- **`work_id` is null on every entry** of both the discovery index and the mass
  corpus [verified], so no harvested lead links to a source-library work record;
  deduplication falls back to the string `"author | title"`. The commentary
  README says this reconciliation should exist. It has not been done, and Rule 8
  depends on it.
- **Editing an existing `artifact.toml` cascades a review obligation.** Its
  fingerprint feeds every segment, passage and corpus above it, and 101 tracked
  binding files carry pins. This is deliberate policy, not a bug. New records are
  cheap; edits to old ones are not.

### And the page is largely already written

`src/web/browser/shared/browser-core.js` already provides the chapter cache, the
translation selector, `renderLocus`, `renderCitation`, `recastLoci` — which
prints *"…in this edition's vulgate numbering"* rather than leaving a reader to
doubt — a render token that discards an overtaken selection, and four named
failure renderings. The proven way to feed new data through it is the adapter in
`plan-model.js`, which rewraps a reading as a citation-shaped object so the shared
renderer serves it unchanged. A catena needs that adapter, not a front end.

Two constraints from that file's own header bind the catena and rule out the
obvious shortcut:

> file counts must be **additive, never multiplicative** — adding a translation
> adds that translation's fragments and changes nothing else;
>
> the join belongs **at read time** in the browser: do not turn this into static
> pages, do not inline verse text into the structure files, and do not build a
> per-pair cache on disk.

A catena that pre-rendered chapter × translation × fragment-set would break both.

---

## 8. What must be true before acquisition begins

Most of this list is now discharged. It is kept in order, with what settled each,
because a checklist that only ever grows teaches nothing.

1. ~~**TASK-101** — one locus granularity.~~ **Done.** The index stores the
   chapter and derives everything finer; see §3.
2. ~~**TASK-100** — canonical titles that cover their works' extent.~~ **Done.**
   Four groups renamed, 151 mislabelled rows to 0; see §5.
3. ~~**TASK-95** — the projection consumed by something.~~ **Done.** One parser
   for `verse-aliases.tsv` instead of two, and an edition that will not project
   now fails the build rather than resolving quietly.
4. ~~A licence survey of the candidate text sources.~~ **Done, and it is the
   hardest finding of the pilot.** The first pass covered ten target works on
   Genesis and found two with a public-domain English text. The survey has since
   been widened to all **66 distinct works** the index names on Genesis, from
   1,746 alias queries over 327 catalogue candidates: **34** carry an affirmative
   public rights basis, **57** have reachable text at the upper bound, four have
   candidates but no text layer, and five have no candidate at all [verified,
   `genesis-availability-survey.yaml`]. The finding survived the widening — the
   English translations that exist are 20th- and 21st-century, the earliest
   expiring 2052. This is not a gap more effort closes.

   **It survived a third widening, 2026-08-01, run against the twelve works
   actually held rather than against the acquisition list.** Four reach English
   and all four already did — Basil in NPNF 2-8, Gregory of Nyssa in NPNF 2-5,
   Augustine's *City of God* in Dods, Luther in Lenker. **Eight reach none, and
   the lane authorised to acquire English landed zero**, because for six of the
   eight the only English is in copyright and for two — Angelomus of Luxeuil and
   Remigius of Auxerre — no English translation of any date could be found at
   all. Four of the negatives were settled against the actual tables of contents
   of the series that would have carried them, volume by volume, rather than
   inferred: the *Hexameron* is not in NPNF 2-10, the *Hebrew Questions* are not
   in NPNF 2-6, *De Genesi ad litteram* is in none of Dods's fifteen volumes,
   and Giles's twelve-volume Bede translates the *historical* works only, by its
   own title page.

   Two public-domain partials were found and deliberately not landed: Jerome's
   own preface to the *Hebrew Questions*, which stands among the Prefaces in
   NPNF 2-6 and answers no chapter of Genesis, and an English of Severian's
   first homily made from Bareille's 1865 **French** rather than from the Greek
   — a translation of a translation, which is a third claim again and would have
   to be rendered as one.

   All of it lives in `src/sources/commentary/translation-absences.yaml`, one
   row per work per language, and the check has teeth in both directions: a work
   standing in the catena with no English and no row saying why is a build
   failure, and so is a row claiming a work reaches no English while the library
   holds an English edition of it. The page prints the reason where the reader
   meets the gap, which is the point — an unexplained absence is what invites
   somebody to fill it, and the way this project would fill it is a fluent
   English of a Latin father made here.
5. ~~The scripture edge of Rule 10, with a validator.~~ **Done.** It lives in
   `src/sources/commentary/fragment-loci.yaml`, *beside* the passage records
   rather than inside them, because a field added to a passage would move its
   `source_fingerprint` and hand a review obligation to every pinned binding
   above it.
6. **`work_id` reconciled** between the harvest's leads and the source library's
   work records. Still open, and now the only item ahead of acquisition.

Two things the pilot added to this list that the study did not anticipate:

7. **Retrieval must not route source text through a model.** Demonstrated, not
   feared: asked for a verbatim text, one route returned Basil exactly and, from
   the same host under the same instruction, a **paraphrase** of Gregory of
   Nyssa. See `guidance/sources.md`.
8. **The unencumbered Latin is OCR wreckage and the clean Latin is encumbered.**
   Migne PL 34's Internet Archive text layer corrupts roughly one word in eight.
   For every work reachable only in Latin the cost is transcription, not download — which
   is a different project from acquisition and should be planned as one.

## 9. Prior art

Deferred: a survey of CTS/CITE canonical URNs, Biblindex, existing digital
catenae, and the bulk availability and licensing of the patristic text corpora is
in progress and will be folded in here. It is expected to bear chiefly on §2
(addressing) and §6 (licence), and may replace the addressing scheme proposed
here with a standard one, which would be a better outcome than keeping ours.

---

## 10. Coverage: what is held, against what the work reaches

Everything above governs a fragment that exists. Nothing above governs the
fragment that does not, and that is where the apparatus had a hole.

The hole was found by eye rather than by a check. Augustine reaches Genesis 3
and stops, which a reader noticed on the page and no gate had anything to say
about. `catena check` reported 1,351 fragments and reported nothing whatever
about where they are not: the harvest names works, acquisition lands what is
reachable, and the two were never subtracted. *De Genesi ad litteram* holding
12 fragments over Genesis 1–3 is that work being finished. *De civitate Dei*
holding 3 over Genesis 1–2 is acquisition stopping, and the two were
indistinguishable from anything the repository recorded.

They are indistinguishable *in principle*, not for want of effort. The index
and the fragments together cannot say how far a work goes; only the work can.
So the extent is stored, once, per work and book, with its basis — the
author's preface, the printing's own headings, or a second work written to
supply what the first left undone — exactly as `composed` carries
`composed_basis`.

> **Rule 12.** A work's extent is recorded where it can be sourced, and the
> coverage check subtracts it. Where it is not recorded the difference between
> named and held is reported as **unexamined**, never as a gap. "We have not
> established where this work ends" and "this work is missing" are different
> claims and the record must be able to say which it is making.

Four readings, and they must not collapse into one number:

| Reading | What it means | What to do |
| --- | --- | --- |
| `complete` | the extent is recorded and held entire | nothing |
| `gap` | chapters unheld inside a **continuous** work's extent | acquire |
| `not-established` | chapters unheld inside a **selective** work's extent | read the printing before calling it anything |
| `unexamined` | no extent recorded | establish the extent, and only then ask |

Two consequences worth stating because both were decided against the obvious
alternative.

The extent lives *beside* the work record and not on it, in
`src/sources/commentary/work-extents.yaml`. This is not tidiness. `work.toml`
has a closed field set, and opening it moves that record's
`source_fingerprint` and every fingerprint descending from it — measured at 53
reviewed bindings across 17 tracked files for one Augustine record alone. §7
already states the policy; `fragment-loci.yaml` already obeys it. The cost is
that a work's prose `description` may also state its reach, and the guard
against those two drifting is not discipline but a check: a recorded extent
that a held fragment of the same work already reaches past is a hard failure,
because either the extent is short or the fragment is misplaced and the
subtraction reports a clean corpus either way.

And a gap never fails the build. An unacquired work is not a defect, and a
`check` that stayed red until someone had gone and got the rest of *De
civitate Dei* is a `check` nobody could ship. What fails is the extent record
being unusable. What *prints*, on every run, is the count — because the whole
reason a work sat held on a sliver of itself was that every gate passed and
none of them said anything about absence. `guidance/the-shape.md` §4: absence
is data, and it has to have somewhere to live.

`commentary-work-index coverage` is the verb; `make check-commentary-coverage`
is the one line it prints into the build.
