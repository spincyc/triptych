# The catena: presenting commentary beside the passage it comments on

A design study for a page that walks the Bible chapter by chapter, shows the
chapter's text in a translation the reader chooses, and beneath it shows every
commentary fragment this project holds on that chapter, in chronological order.

The name is descriptive. A *catena* is the genre — a chain of excerpted comment
running beside the text — and this is not a reproduction of Aquinas's
*Catena Aurea*, which is one particular thirteenth-century catena on the four
gospels and a work this project may later carry as a source. Where the two could
be confused, the work wins the name and the page takes another.

**Nothing here has been built.** The commentary texts do not exist in this
repository and are not expected to until a later acquisition round. This study
exists so that the addressing, granularity and storage decisions are settled
*before* acquisition, because they are the decisions that are expensive to
revisit once several thousand fragments have landed under the wrong key.

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

L1 exists and is large: **497 rows, 61 books, 341 distinct works, 86 authors**
[verified].

L3 also exists, which an earlier draft of this study got wrong and is worth
correcting in place rather than quietly. No field anywhere in
`src/sources/commentary/` can hold the text of a fragment — that much is right
[verified], and it is by design, because the harvest produces an acquisition
list. But the **source library's `passage` record has held third-party prose all
along**: `text`, `transcription_segments`, `physical_line_ranges`, `artifact_id`,
`artifact_sha256`, `states`, `context`, `verified_on`. There are **1,227 such
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

**The index already carries two granularities, and they disagree** [verified].
Of its 497 rows, 490 are chapter-keyed and 7 are verse-or-range-keyed survivors
of the early pilot runs — `Luke 21:25-21:33`, `Romans 13:11-13:14`,
`Psalms 24:1-24:3`, `Psalms 24:3`, `Psalms 24:4`, `Psalms 84:8`, `Psalms 84:13`,
all of them First Sunday of Advent propers. The arithmetic reconciles: 491
harvested chapter loci, less `4 Esdras 2` which all three passes correctly
returned empty, gives 490.

They are not duplicates. `Psalms 24:4` carries 19 works of which **7 appear on no
chapter row**; `Romans 13:11-13:14` carries 22 of which **13** do not;
`Luke 21:25-21:33` carries 27 of which **14** do not [verified]. So the index
answers the same question two ways and the answers differ. A consumer keyed on
chapters loses those works silently; a consumer keyed on the pilot loci sees a
different corpus for the same text. Both look complete.

`docs/reading-and-commentary.md` listed four things that had to happen before
promotion, in order, and the third was *"reconcile the two locus granularities
the ledger carries […] so promotion would currently emit 497 passages where 491
were harvested."* Promotion ran anyway. This is TASK-101 and it blocks the
catena, whose entire promise is *every* commentary on this chapter.

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

Of the 300 groups in `work-aliases.yaml`, exactly two have a canonical title
naming fewer books than the group spans [verified]:

```
Thomas Aquinas       => Super Epistolam ad Romanos lectura     spans 10 books
Theophylact of Ohrid => Expositio in epistulam ad Romanos       spans 10 books
```

Both groupings are *correct* — each author really did comment across the Pauline
corpus as one work. The name chosen for the group says Romans. Downstream, the
index carries **148 rows whose recorded title names a book other than the
passage's, 61 of them at confidence 1.0** [verified] — all three independent runs
agreed, which does not make it right, because they share the bias.

This was anticipated. The same four-item list in `docs/reading-and-commentary.md`
names it: *"settle whether a per-book commentary is named by the whole or by the
part, which is a cataloguing decision rather than a data problem."* It is the one
item still open, and it is TASK-100.

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

### Three prerequisites the survey turned up

- **No structure file enumerates the canon** [verified]. Every existing coverage
  is citation-driven — the bible index covers what the calendars cite, the
  propers structure covers the propers, the readings structure covers 454
  chapters in 31 books. A catena over *every* chapter needs a whole-canon
  enumeration. The material is there — `book-index.tsv` gives 73 books and 1,334
  chapters, and chapter fragments exist on disk for all of them — but no tool
  writes it.
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

In order. The first three are open tasks and the acquisition round should not
start ahead of them.

1. **TASK-101** — one locus granularity in the index, the other derived.
   Acquiring against an index that answers two ways files the corpus two ways.
2. **TASK-100** — canonical titles that cover their works' extent. The
   acquisition list is keyed by work identity; a work named after one tenth of
   itself will be acquired as one tenth of itself.
3. **TASK-95** — the projection consumed by something. The catena is the natural
   consumer, and a projection nothing has exercised is a projection nobody knows
   is right.
4. A licence survey of the candidate text sources, with the licence established
   by fetching the licence, not by reputation.
5. The scripture edge of Rule 10, with a validator, before the first fragment is
   written — not after several thousand. Not a schema: the container exists.
6. `work_id` reconciled between the harvest's leads and the source library's work
   records, without which Rule 8 cannot be checked at all.

## 9. Prior art

Deferred: a survey of CTS/CITE canonical URNs, Biblindex, existing digital
catenae, and the bulk availability and licensing of the patristic text corpora is
in progress and will be folded in here. It is expected to bear chiefly on §2
(addressing) and §6 (licence), and may replace the addressing scheme proposed
here with a standard one, which would be a better outcome than keeping ours.
