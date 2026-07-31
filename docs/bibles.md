# Bibles: their canons, their editions, and why citing them consistently is hard

This repository resolves scripture citations — the readings and antiphons of two
Roman calendars — against tracked Bible editions, and renders the words. That
sounds like a lookup. It is not, and this document explains why.

The short form: **a citation is a three-part address of which only two parts are
ever written down.** A reference gives you a book name and a chapter-and-verse
locus. It does not give you the numbering system its author was using, and
several incompatible systems are in circulation, all of them legitimate. When
the missing third part is guessed wrong, the lookup usually still succeeds —
because the target edition happens to print *something* at those numbers — and
returns the wrong words under a correct-looking reference. Nothing counts that
as a failure.

Everything below is checkable against files in this repository. The headings are
written to carry the argument on their own; the detail sits underneath each one.

---

## A citation is a three-part address, and only two parts are ever written down

Write out `Isaiah 9:5` and you have named a book and a locus. You have not named
the numbering system, and for Isaiah 9 there are two in common use that differ by
one verse. In the numbering the postconciliar Lectionary uses, `Isaiah 9:5` is
*For a CHILD IS BORN to us*. In the numbering the Vulgate uses, `Isaiah 9:5` is
*every violent taking of spoils, with tumult, and garment mingled with blood*.

Both are real verses. Both are in Isaiah 9. A resolver handed the citation and
the Douay-Rheims returns the garments rolled in blood, reports success, and moves
on.

The third element is unwritten because for most of the Bible it does not matter.
`John 3:16` is `John 3:16` everywhere. It is precisely the fact that the guess is
*usually* right that makes it dangerous when it is wrong: there is no habit of
checking, and no signal when the check would have failed.

---

## The editions here belong to three different canons, and the differences are structural

Six editions are indexed in this repository. Their book counts are not variations
on a theme; they are different answers to what the Bible contains, and in three
cases the same text is filed under a different book.

| Edition | Books | Chapters | Verses | Numbering | Psalter |
|---|---|---|---|---|---|
| Douay-Rheims (Challoner), Gutenberg 1581 | 73 | 1334 | 35,804 | Vulgate | Gallican |
| Douay-Rheims American 1899 (eBible engDRA) | 73 | 1334 | 35,811 | Vulgate | Gallican |
| Clementine Vulgate (eBible latVUC, Latin) | 73 | 1334 | 35,809 | Vulgate | Gallican |
| World English Bible, Catholic Edition | 73 | 1328 | 35,379 | Hebrew | Masoretic |
| King James with Apocrypha (1769 text) | 80 | 1362 | 36,822 | Hebrew | Masoretic |
| Revised Version with Apocrypha (1895) | 80 | 1362 | 36,836 | Hebrew | Masoretic |

A seventh edition, the Knox translation, is registered but is licensed rather
than public domain; it is discussed under rights below.

The Catholic canon fixed at Trent is 73 books. The King James and the Revised
Version print 80. The extra seven are not seven extra Catholic books.

### The King James Apocrypha is not the Catholic deuterocanon

The King James prints fourteen books in a section of their own between the
Testaments. Of those fourteen:

- **Seven are Catholic deuterocanonical books** — Tobit, Judith, Wisdom,
  Ecclesiasticus, Baruch (with the Epistle of Jeremias as its sixth chapter), and
  1 and 2 Maccabees. These are inside the Old Testament proper in a Catholic
  Bible.
- **Four are Catholic canonical *matter* printed as separate books** — the Greek
  additions to Esther and the three Greek additions to Daniel. A Catholic Bible
  has these too; it just does not have them as books.
- **Three are in no Catholic canon at all** — 1 Esdras, 2 Esdras, and the Prayer
  of Manasses. Trent did not receive them. The Clementine Vulgate prints 3 and
  4 Esdras and the Prayer of Manasses in an appendix *after* the New Testament,
  outside the canon, and the electronic Clementine tracked here does not carry
  that appendix at all.

So the King James canon is larger *and* differently shaped, and the naming makes
it worse. In this library the Douay-Rheims's "1 Esdras" is Ezra and its
"2 Esdras" is Nehemiah — token `1Esd`, `2Esd`. The King James's *1 Esdras* is the
Greek Esdras, a different book entirely, token `1Esdras`. Two books, near-identical
names, and one is not a translation of the other: Greek Esdras reorders its
material and contains the Tale of the Three Guardsmen, which has no counterpart
in Ezra-Nehemiah. Book identity has to be resolved per edition. There is no
shared alias table that could be right for both.

### Esther's Greek additions are integrated in one canon and a separate book in the other

The Greek Esther is about half again as long as the Hebrew. The Vulgate keeps the
whole of it, arranging the six additions as chapters 10:4 through 16:24 —
appended after the Hebrew narrative rather than in their narrative places. The
Douay-Rheims and the Clementine therefore print **Esther in sixteen chapters**.

The King James prints **Esther in ten chapters** and puts the additions in the
Apocrypha as *The Rest of the Chapters of the Book of Esther Which are Found
Neither in the Hebrew, nor in the Chaldee* — seven chapters, 105 verses, token
`EsthGr`. Critically, that separate book **keeps the Vulgate's own numbers**,
10:4 through 16:24. So a 1962 Missal citation of `Esther 13:9` addresses `EsthGr`
13:9 in the King James and resolves, verse for verse, with no arithmetic. The
Revised Version does the same.

The World English Bible Catholic Edition does neither. It translates Esther whole
from the Greek and merges the additions into the Hebrew chapter numbering as
extensions of 1:1, 3:13, 4:17, 8:12 and 10:3. Its Esther has ten chapters, and
the Vulgate's Esther 11-16 **do not exist in it at all**. The 1962 Missal's
`Esther 13:9-11` and `Esther 14:12-13` find no chapter there and are reported
unresolved — which is the correct outcome, and a visible one.

Three editions, three incompatible arrangements of the same text, and only one of
them can be reached by Vulgate numbers.

### Daniel's Greek additions become three separate books, and only two of them line up

The Vulgate's Daniel has fourteen chapters. Chapter 3 runs to verse 100, because
the Prayer of Azarias and the Canticle of the Three Children sit inside it as
3:24-90. Chapters 13 and 14 are Susanna, and Bel and the Dragon.

The King James's Daniel has twelve chapters, its chapter 3 ends at verse 30, and
the additions are three separate books in the Apocrypha: *The Song of the Three
Holy Children* (68 verses), *The History of Susanna* (64), *Bel and the Dragon*
(42).

Two of the three are nearly clean relabellings. The third is not, and the seams
are instructive:

- **Susanna** is Vulgate Daniel 13 — but Daniel 13 has **65** verses and Susanna
  has **64**. The Vulgate's Daniel 13:65, *And king Astyages was gathered to his
  fathers*, is the King James's **Bel 1:1**. The book boundary is in a different
  place.
- **Bel and the Dragon** therefore runs one ahead of Vulgate Daniel 14 all the way
  down: Bel 1:2 is Daniel 14:1, Bel 1:41 is Daniel 14:40. And the Vulgate's
  Daniel 14:42 — *Then the king said: Let all the inhabitants of the whole earth
  fear the God of Daniel* — has no King James counterpart at all.
- **The Song of the Three** does not relabel. Its 68 verses stand against the
  Vulgate's Daniel 3:24-90, which is 67 verses, so at least one verse boundary
  falls somewhere different inside the block. The King James edition record here
  states exactly where it is known to break — Vulgate Daniel 3:52 is its verse 29
  but Vulgate 3:89 is its verse 67, not 66 — and **refuses to assert a
  correspondence** rather than pick an offset. The Vulgate loci that overlap the
  King James's own Aramaic chapter 3 are withheld in that edition's alias table,
  so `Daniel 3:29` in a Vulgate-numbered calendar refuses instead of quietly
  returning Nabuchodonosor's decree, which is what the King James really prints
  at those numbers.

The World English Bible Catholic Edition keeps the Vulgate's fourteen chapters
but divides the additions as the Greek does — 97 verses in chapter 3 against 100,
64 in chapter 13 against 65 — and its Daniel 14 is the Bel arrangement, one verse
ahead of the Vulgate's throughout. That last shift is not recorded in that
edition's alias table. It is not currently a defect only because no tracked
calendar cites Daniel 13 or 14.

---

## The psalms are numbered twice over, and the two offsets are independent

Two entirely separate things shift psalm verse numbers, and they compose. Get
either one wrong and you land on real text a verse or two from the words meant.

### First offset: the Septuagint and the Hebrew join and split psalms differently

The Greek Septuagint, and the Latin Vulgate after it, treat four places in the
psalter differently from the Hebrew. The result is that from Psalm 9 to Psalm 147
the two systems mostly run one apart, and realign only at the end:

| Vulgate | Hebrew | |
|---|---|---|
| 9 | 9 + 10 | one Greek psalm becomes two Hebrew ones; Vulgate 9:22-39 is Hebrew 10:1-18 |
| 10-112 | 11-113 | Hebrew number is one higher |
| 113 | 114 + 115 | Vulgate 113:1-8 is Hebrew 114; 113:9-26 is Hebrew 115 |
| 114 + 115 | 116 | two Vulgate psalms are one Hebrew one |
| 116-145 | 117-146 | Hebrew number is one higher |
| 146 + 147 | 147 | two Vulgate psalms are one Hebrew one |
| 148-150 | 148-150 | the joins and splits cancel exactly |

The consequence is not subtle. The Advent introit *Ad te levavi* is **Psalm 24**
in the 1962 Missal and **Psalm 25** in the postconciliar one. Douay-Rheims Psalm
25 is *Judge me, O Lord* — a different psalm about a different thing. The
*Miserere* is Psalm 50 in the 1962 books and Psalm 51 in the postconciliar ones.

This library's authority for the correspondence is a tracked, verse-level
concordance — `psalm-numbering.tsv`, an artifact of the Douay-Rheims edition —
which maps all **2,528 verses** of the psalter in **219 rows**, one row per run
of verses both systems number without interruption. It is data, not a remembered
rule, and `scripts/_psalms.py` reads it and validates it on load: both sides of
every row must be the same length, and each system must cover all 150 psalms
with no gap and no overlap. The module deliberately holds no table of its own.
The reason is recorded in its docstring — when the correspondence was restated
in several places, the copies disagreed.

### Second offset: whether a psalm's title counts as verse 1

Most psalms open with an inscription — *Unto the end, a psalm for David*. The
Hebrew numbers it, and so do the Vulgate, the Nova Vulgata and the New American
Bible. The English convention of the King James, the Revised Version and most
modern English versions prints it as an unnumbered heading.

So an English Bible's verse numbers run **one lower** than the Hebrew numbering
through the body of the psalm. The concordance records an inscription for **67**
psalms; for four of them — Vulgate 50, 51, 53 and 59 — the inscription is two
verses long, so the offset there is **two**.

Both offsets apply at once. The *Miserere*:

- 1962 Missal / Vulgate: **Psalm 50:3**
- Hebrew numbering: **Psalm 51:3**
- What the King James prints: **Psalm 51:1**, *Have mercy upon me, O God*

This is why the edition registry carries `psalm_titles` alongside `numbering`. An
edition can agree with a calendar on which psalm is meant and still be two verses
out on which words.

### Fifteen psalms where neither rule holds, and the tool refuses rather than guessing

For fifteen psalms the two conventions divide the *body* differently as well, not
just the head, so an offset taken at verse 1 stops being right further down. The
concordance flags them (`english_offset_uniform: no`): Hebrew 2, 4, 20, 29, 43,
44, 53, 56, 72, 100, 109, 126, 136, 146 and 150.

For those, `_psalms.english_verse` returns no number and a reason. So does an
endpoint that lands on the inscription itself, which an English Bible has no
number for at all. Run the index against the World English Bible and you get, in
full:

```
Psalm 100:1-2, 3, 5: English Bibles divide Psalm 100 differently from the
  Hebrew numbering, and no verse-for-verse correspondence is recorded for it
Psalm 102:1: Hebrew Psalm 102:1 is the inscription, which English Bibles
  print unnumbered
```

Neither is a bug. Both are the design working: a refusal that explains itself.

---

## Chapter divisions move outside the psalter too

The psalter is the famous case. It is not the only one. The Nova Vulgata — the
Latin edition the postconciliar Lectionary is keyed to — divides several prophets
differently from the Vulgate, and the two calendars this repository tracks cite in
those different systems.

The tracked Douay-Rheims, Clementine, King James, Revised Version and World
English editions all agree with each other on these loci and all differ from the
Nova Vulgata. That is not an accident. The modern verse divisions were made in
Latin Bibles — Santes Pagnino's Old Testament of 1527/28 and Robert Estienne's,
whose 1555 Latin Vulgate was the first Bible to print verse numbers in the
running text — and the English Bibles inherited them. The King James is a witness
to the Hebrew *text* and to the English *versification* at the same time, and the
English versification here is the Latin one.

| Locus | Nova Vulgata | Every edition tracked here |
|---|---|---|
| Joel | 4 chapters | 3 chapters |
| Malachi | 3 chapters | 4 chapters |
| Isaiah 8 | ends at v. 23 | ends at v. 22 |
| Isaiah 64 | 11 verses | 12 verses |
| Micah 4 | ends at v. 14 | ends at v. 13 |

Worked out with the actual words:

- **Joel.** Nova Vulgata Joel 3 is Vulgate Joel 2:28-32; Nova Vulgata Joel 4 is
  Vulgate Joel 3. The Pentecost reading cited `Joel 3:1-5` means *I will pour out
  my spirit upon all flesh*. Douay-Rheims Joel 3:1-2 is *I will gather together
  all nations and will bring them down into the valley of Josaphat*.
- **Malachi**, in the other direction. Nova Vulgata 3:19-24 is Vulgate 4:1-6. A
  citation of `Malachi 3:19-20a` means *the day shall come kindled as a furnace*,
  which the Vulgate prints as 4:1.
- **Isaiah 9.** Nova Vulgata 8:23 is Vulgate 9:1, and the rest of chapter 9 runs
  one verse ahead. `Isaiah 9:5` means the Child born to us; the Vulgate prints
  that as 9:6, and prints the garments rolled in blood at 9:5.
- **Isaiah 64**, again in the other direction. Nova Vulgata 63:19b is Vulgate
  64:1, so the rest of chapter 64 runs one verse *behind*. The Advent reading
  `Isaiah 63:16b-17, 19b; 64:2-7` is Vulgate `Isaiah 63:16b-17; 64:1, 3-8`.
- **Micah 5.** Nova Vulgata 4:14 is Vulgate 5:1. The Christmas prophecy
  `Micah 5:1-4a` — *And thou Bethlehem Ephrata* — is Vulgate `Micah 5:2-5a`.
  Douay-Rheims Micah 5:1 is *Now shalt thou be laid waste, O daughter of the
  robber*.

These five books are recorded in the postconciliar calendar under
`citation_divergences`, citation by citation, with the resolution written out even
where nothing moves — because inside a divergent book, silence is not evidence
that anyone checked. `index-bible` validates those entries against the citations
the calendar actually makes before it indexes anything, and a citation reaching a
divergent locus with no resolution recorded is **refused**, not resolved.

---

## Two printings of the same Vulgate disagree with each other

It would be convenient if "the Vulgate" were one thing. It is not, and the
disagreements are inside this library, not out at the edges of scholarship.

Comparing the Challoner Douay-Rheims against the Clementine Latin, chapter by
chapter: **1,334 chapters in common, 17 of which have different verse sets.**
Both editions declare `numbering: vulgate` and `psalter: gallican`.

| Book/chapter | Douay-Rheims | Clementine |
|---|---|---|
| 1 Thessalonians 4 | 1-17 | 1-18 |
| 2 Thessalonians 2 | 1-16 | 1-17 |
| 2 Kings 13 | 1-38 | 1-39 |
| Amos 9 | 1-14 | 1-15 |
| Ecclesiasticus 29 | 1-34 | 1-35 |
| Isaiah 45 | 1-26 | 1-25 |
| Isaiah 46 | 1-12 | 1-13 |
| Judith 4 | 1-16 | 1-17 |
| Psalm 15 | 1-11 | 1-10 |
| Psalm 19 | 1-9 | 1-10 |
| Psalm 28 | 1-10 | 1-11 |
| Psalm 42 | 1-6 | 1-5 |
| Psalm 115 | **10-19** | **1-10** |
| Psalm 125 | 1-7 | 1-6 |
| Psalm 135 | 1-27 | 1-26 |
| Psalm 147 | **12-20** | **1-9** |
| Psalm 150 | 1-5 | 1-6 |

Most of these are one edition merging two verses that the other keeps apart.
1 Thessalonians 4 is the clean example: the Douay's 4:17 is *Wherefore, comfort ye
one another with these words*, and the Clementine's 4:18 is *Itaque consolamini
invicem in verbis istis*. Same sentence, different number, same nominal
numbering system.

This is why the correction cannot live in the calendar. A calendar entry saying
"1 Thessalonians 4:18 means 4:17" would be right for the Douay and wrong for the
Clementine. **It is a fact about an edition**, and it belongs in that edition's
own `verse-aliases` table. The Douay's has seven rows, each recording a verse
number the edition gives no text of and the verse its words stand in. The
Clementine's has none at all — its file is a header line and nothing else.

Psalm 115 and Psalm 147 are a different animal. Where the Vulgate splits a Hebrew
psalm, the second half **keeps its pre-split numbering**: Vulgate Psalm 115 is
printed as verses 10-19, not 1-10, because those verses were Hebrew 116:10-19
before the split. The Challoner Douay-Rheims prints it that way. The Clementine
and the American 1899 Douay-Rheims restart both psalms at verse 1. Three editions,
two conventions, no declaration distinguishing them.

The third electronic Douay-Rheims makes the point again from another angle. The
American 1899 text differs from the Challoner text in only nine chapters: two are
those restarted psalms, and the other seven are verse divisions the Challoner
e-text runs together and this one keeps apart — Genesis 5:32, 2 Kings 13:39,
Psalm 28:11, Psalm 150:6, Amos 9:15, John 11:57, 2 Corinthians 1:24. Same
translation, same 73 books, same 1,334 chapters, seven extra verse numbers.

---

## The failure that matters is a citation that resolves *successfully and wrongly*

Here is the whole reason this document exists.

Run the index against the Douay-Rheims today and it reports **949 of 950**
postconciliar references and **777 of 778** 1962 references resolved — 99.9% on
both. The single failure in each is `4 Esdras 2:36-37`, a book no Vulgate edition
here carries.

That number is not a measure of correctness. It is a measure of *how many
citations produced text*. The calendar's own `open_collation_items` records that
an audit of every non-psalm citation against the tracked Douay text found **a
further 23 that still resolve to the wrong verses** — in Exodus 22, Hosea 2 and 6,
Esther 4, Wisdom 6 and 11, Sirach 3, 27 and 35, Mark 9, John 6 and Acts 14. Every
one of them is inside the 99.9%.

The two named at the top of this document were of exactly that kind before they
were found:

- `Joel 3:1-5` returned *the valley of Josaphat* instead of *I will pour out my
  spirit*.
- `Isaiah 9:5` returned *garment mingled with blood* instead of *For a CHILD IS
  BORN to us*.

Neither appeared in any error count. Both resolved.

### Why that is worse than a miss

A miss is a question. A wrong hit is an answer.

A missing passage announces itself. It shows up in a tally, it is one line in a
report, someone looks at it and either fixes it or records why it cannot be
fixed. It has a natural constituency: the number is visible and it is uncomfortable.

A wrong hit has none of that. It is a well-formed reference, resolving to real
scripture, printed in the right place on the page, in the right book, in the right
chapter. Everything about it looks like success. It will pass every automated
check the system has, because the system's checks are all shaped like "did this
resolve?". The only thing that catches it is a human who knows the passage and
reads the page — which means the defect's lifetime is bounded by nothing at all,
and the more citations the system carries the less likely that human is to look at
this one.

Worse, a defect of this kind can be **harmless in one edition and destructive in
another**, which is how it survives review. Three of the four Douay-Rheims
citations that run past the end of a chapter lose no text, because the verse the
Vulgate merged them into carries the words. The same defect against the Clementine
loses the passage entirely.

### One is still shipping

The Clementine index in this repository currently contains this line:

```yaml
  Psalm 115:10, 15, 16-17, 18-19: in atriis domus Domini, in medio tui, Jerusalem.
```

The Douay-Rheims index, for the identical key, contains the antiphon: *I have
believed, therefore have I spoken...*

A four-part responsorial psalm has become one clause, and the wrong clause. Two
defects combined. The psalm concordance renumbers Hebrew 116 into Vulgate 115
using the numbering the Douay prints, where Vulgate 115 runs verses 10-19; the
Clementine prints the same psalm as verses 1-10. Verses 15-19 fall past the
Clementine's chapter end and are silently discarded, leaving verse 10 — which in
the Clementine is the psalm's *last* verse, *in atriis domus Domini*, not its
first.

The concordance is not wrong. Published Vulgate versification data numbers Psalm
115 to verse 19, as the concordance does. The Clementine is the edition that
departs, and there is nowhere to record that it departs.

### The silent clamp

`index-bible` derives a chapter's bounds from the verses the edition actually
prints, and then truncates a request to fit:

```python
for verse in range(low, min(high, bound) + 1):
```

So `1 Thessalonians 4:13-18` against the Douay-Rheims, whose chapter 4 ends at
17, returns verses 13 through 17 and reports no problem. Three citations are
handled this way in the Douay-Rheims today — `1 Thessalonians 4:13-18`,
`Acts 7:55-60` and `Mark 4:35-41` — and all three happen to lose no words,
because the verse the Vulgate merged them into carries them. The same clamp
against the Clementine's psalms destroys the passage.

The design study `guidance/versification.md` names removing this clamp as the
second item of work, and the shape of the replacement matters: the error message
has to name the cited verse, the edition's last verse, **and the edition**,
because `1 Thessalonians 4:18` is an error against the Douay and correct against
the Clementine.

---

## The same citation string can be valid in two systems and mean unrelated text

Everything above is about numbers being one or two apart. This one is about
seventy, and it is in the library.

Codex Sangermanensis I, copied in 822, lost a leaf of 4 Ezra, and almost every
later Latin manuscript descends from it. Around seventy verses were therefore
absent from the Western tradition until Robert Bensly recovered them from an
Amiens manuscript in 1875. The restored block was numbered 7:36-105, and what had
previously been 7:36-70 became 7:106-140.

The King James Apocrypha, transcribed from the standardized 1769 text, lacks the
block: its 2 Esdras 7 has **70** verses, and 7:36 reads *Then said I, Abraham
prayed first for the Sodomites*. The Revised Version's 1895 Apocrypha has it: its
2 Esdras 7 has **140** verses, its 7:36 reads *And the pit of torment shall
appear*, and the King James's 7:36 is its **7:106**.

Same citation string. Same book. Same nominal canon. Two editions in this
repository, seventy verses apart, both correct for their own text. Nothing about
`2 Esdras 7:36` warns you which one you are talking about.

The general lesson: a system identifier has to be specific enough to distinguish
two states of the same tradition. "Vulgate" is not specific enough where the
Douay and the Clementine disagree; "Greek" is not specific enough where Rahlfs and
Ziegler disagree about the order of Sirach 30-36.

---

## Some books are not renumbered, they are different texts

There is a hard floor to what any numbering scheme can fix. Compare the tracked
Douay-Rheims, Englished from the Latin, against the tracked King James Apocrypha,
Englished from the Greek:

| Book | Douay-Rheims | King James | Chapters differing |
|---|---|---|---|
| Ecclesiasticus (Sirach) | 1,591 verses | 1,393 | **48 of 51** |
| Tobit | 298 | 244 | 13 of 14 |
| Judith | 345 | 339 | 14 of 16 |
| Wisdom | 439 | 436 | 7 of 19 |
| Baruch | 213 | 213 | 2 of 6 |

Sirach settles the question. The Latin carries expansions the Greek does not,
scattered through nearly every chapter. There is no numbering of "Sirach" that
these two editions are numbering differently; **there are two texts**. For a
Latin expansion there is simply no Greek verse to name, and the honest record is
"absent", not a number. The publishers of the standard mapping datasets say the
same thing and decline these books outright, for the same reason.

Baruch is the miniature version. Both editions have 213 verses, so the totals
agree; but the King James joins at 3:34 what the Vulgate divides, so its chapter 3
ends at 37 where the Vulgate's ends at 38. The Vulgate's *Afterwards he was seen
upon earth, and conversed with men* is Baruch 3:38 in the Douay and 3:37 in the
King James, and a citation of `Baruch 3:38` falls past the end of the chapter
there and refuses.

And Sirach shows why per-chapter offsets are not enough either. Against the
tracked Douay, the US Lectionary's `Sirach 3:2` is Douay 3:3 (+1), its `3:17` is
Douay 3:19 (+2), its `27:30` is Douay 27:33 (+3), and its `28:1` is Douay 28:1
(0). The offset changes three times inside one chapter and resets at the chapter
boundary. Only a segment-level table can carry that.

---

## Rights decide where a text may live, not only whether it may be read

Public domain by age is the ordinary basis here, and for most of the library it
is uncomplicated: the Douay-Rheims Challoner revision dates to 1749-1752, the
Clementine Vulgate to 1592.

Two of them are not uncomplicated, and in the same way. The King James Version and
the Revised Version are public domain in the United States and everywhere else
**except the United Kingdom**, where the Crown holds a perpetual right in the
Authorized Version and its revisions by letters patent. Those patents have no
expiry, and printing the text in the UK or importing printed copies into it is
reserved to the Crown's patentees — Cambridge University Press, Oxford University
Press and Collins. The decree has no effect outside the UK.

The repository does not paper over that. Every artifact under both editions
records `rights_status = "public-domain"` with `rights_jurisdiction = "United
States"`, and the `rights_basis` field names the United Kingdom exception in prose
rather than claiming the text is free everywhere.

The Knox translation is the case where rights change the architecture. It is
copyright Westminster Diocese, licensed for use but not for redistribution. So:

- its artifacts are retrieved by `tools/knox-bible`, which **refuses any
  destination inside this repository**;
- its index is written outside the repository too, reached with
  `mass-propers --bible-root <path>`;
- it is registered with `publishable: false`, and the public manifest is generated
  from that flag rather than from a directory listing, so the public site cannot
  offer it even if its files were somehow present in the tree.

A licensed text stays fully usable locally and can never be committed or served.
That is the point of building the distinction into the tool rather than into a
convention.

Two smaller distinctions worth keeping straight. Permission to *use* a text is not
permission to *republish* it. And an ecclesiastical imprimatur is not a copyright
licence — it attests that a work is free of doctrinal error and says nothing about
who may copy it.

Finally, not everything in the source library is scripture. The psalm concordance,
the book indexes and the verse-alias tables are Triptych-created reference tables
recording the identity and numbering of public-domain books. They carry no
third-party text, they are recorded as `project-created`, and the project claims
no exclusive right in the underlying facts.

---

## What is settled here, and what is not

**Settled and working.**

- Psalm numbering converts through one tracked, validated, verse-level
  concordance. Nothing restates it.
- Every edition declares its `numbering`, its `psalter` and its `psalm_titles`,
  and `mass-propers` refuses to resolve across a mismatch rather than rendering
  something plausible.
- Book identity is read from each edition's own book index, never from a shared
  table.
- Where a correspondence is not known, the resolver refuses and carries the reason
  through to the output, so a page can explain itself.
- Divergence declarations are validated against the citations actually made, and
  a declaration that has stopped applying fails the build. So does a psalm-bounds
  exception that has stopped being needed. Neither can quietly outlive the defect
  it was written for.
- Rights are enforced by generation, not by filtering.

**Not settled.**

- The clamp is still there. Three Douay-Rheims citations and more Clementine ones
  are silently truncated.
- Around 23 postconciliar citations are known to resolve to the wrong verses and
  are recorded as such in the calendar's `open_collation_items`. They are not
  fixed, because fixing one requires deciding *which system it speaks* — and the
  answer varies slot by slot. Several John 6 antiphons are already Vulgate-numbered
  and correct while the John 6 readings beside them in the same Mass are not.
- Eleven psalm antiphons in the postconciliar calendar carry Vulgate numbers
  inside a file that declares Hebrew numbering. They are listed under
  `psalm_numbering_exceptions` so the psalter-bounds gate can stay shut over the
  rest of the calendar. The calendar names the work of deciding each one — against
  its printed incipit, per slot, whether the number moves or the declaration
  does — as TASK-32.
- No edition here witnesses the Nova Vulgata, so there is nothing to compile a
  concordance from. The five diverging books are handled by hand-recorded
  citation-by-citation resolutions.
- The Clementine declares no per-book chapter or verse counts, so its book index
  cannot be checked against its own text. The six editions carry four different
  book-index header lines between them, and no schema governs any of them.
- The Clementine's `verse-aliases` file is empty, so its thirteen unexplained
  differences from the Douay have nowhere to be recorded.

The full design study — how this problem is solved elsewhere, what this library
can and cannot derive from what it already tracks, and a proposed data model with
gates — is `guidance/versification.md`. Nothing in it has been built.

The through-line of all of it: **a refusal that explains itself is a correct
result.** A plausible wrong answer is not.
