# Bibles for agents

Operating rules for anything that touches a scripture citation, a Bible edition,
or a numbering system in this repository. Companion prose for humans is
`docs/bibles.md`; the design study is `guidance/versification.md`.

The governing fact: **a citation carries a book and a locus but not the numbering
system it was written in.** Guess wrong and the lookup usually still succeeds,
returning real text at the cited numbers. That is the defect class this whole
apparatus exists to catch, and no resolution count will show it to you.

---

## Do not assume

- **Do not assume a chapter starts at verse 1.** Douay-Rheims Psalm 115 runs
  10-19; Psalm 147 runs 12-20. Read both bounds from the text.
- **Do not assume two editions in the same nominal system agree.** The Douay and
  the Clementine both declare `numbering: vulgate`, `psalter: gallican`, and
  differ in 17 of 1,334 shared chapters.
- **Do not assume `numbering` identifies the text.** Latin psalters agree on
  numbers and differ in wording. Gallican Psalm 22 opens *Dominus regit me*; the
  Nova Vulgata reads *Dominus pascit me*. `psalter` is the discriminator.
- **Do not assume `numbering: hebrew` means the printed verse numbers are the
  Hebrew ones.** `psalm_titles: unnumbered` shifts the body of 67 psalms by one
  or two. Both keys are required to address an edition.
- **Do not assume the Mass chants match any tracked psalter.** The 1962 chant
  texts predate the Gallican psalter and frequently disagree with it — the sixth
  Sunday after Pentecost sings *protector salutarium* where the Clementine reads
  *protector salvationum*. No indexed psalter resolves a chant incipit reliably.
- **Do not assume book names are stable across editions.** Douay "1 Esdras" is
  Ezra (`1Esd`); King James "1 Esdras" is Greek Esdras (`1Esdras`). Douay 1-2
  Kings are modern 1-2 Samuel; Douay 3-4 Kings are modern 1-2 Kings.
- **Do not assume the King James is a Hebrew-versification witness.** Its text is
  Masoretic; its chapter and verse divisions are Estienne's Latin ones. It agrees
  with the Vulgate at Joel, Malachi, Isaiah 8/9 and 63/64, and Micah 4/5.
- **Do not assume any tracked edition witnesses the Nova Vulgata.** None does.
  There is nothing here to compile a concordance from.
- **Do not assume an offset generalizes.** Sirach's offset against the tracked
  Douay changes three times inside chapter 3 and resets at the chapter boundary.
- **Do not restate a numbering correspondence in code or prose.** Read it from
  the tracked concordance. Restated copies have already disagreed here; the
  reason is recorded in `scripts/_psalms.py`'s docstring.
- **Do not expect the concordance to tell you how a psalm divides.** A row is a
  correspondence between two runs of verses and both runs must be the same
  length, so one verse answering to two has no representation in the table at
  all, and `_concordance` refuses any row that tries. The concordance can say
  *that* a psalm's body divides differently — that is what
  `english_offset_uniform: no` means — and never *how*. To learn how, read the
  two editions' printed verses; nothing else will tell you.
- **Do not treat a resolution rate as a correctness rate.** The Douay-Rheims
  reported 99.9% on both calendars through the whole period in which two dozen
  postconciliar citations were returning the wrong verses. The rate did not move
  when they were corrected, because they had never been counted as failures.

## Invariants that hold

- One tracked psalm concordance is the sole authority for Vulgate/Hebrew/English
  psalm numbering:
  `src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/psalm-numbering-*/psalm-numbering.tsv`
  (219 rows, all 2,528 psalter verses). `scripts/_psalms.py` holds no table of
  its own and validates the file on load — equal-length sides, all 150 psalms,
  no gap, no overlap. It raises `PsalterUnavailable` rather than converting from
  a bad table.
- `tools/index-bible`'s `EDITIONS` dict is the edition registry. `numbering`,
  `psalter`, `psalm_titles`, `rights`, `publishable` and the artifact path all
  live there.
- Book identity is read per edition from that edition's `book-index.tsv`. Modern
  names are claimed first, so an alternate spelling can never steal a name a
  modern name owns.
- `Bible.verse` consults the edition's `verse-aliases.tsv` **first**, and its
  answer is final — including a recorded refusal (`resolves_to` empty). An
  edition can print real text at numbers a citation does not mean.
- `<out>/bibles.json` is generated from `publishable: true`, and the public-alpha
  deploy copies fragments driven by that manifest, not by a directory listing. A
  non-publishable edition cannot reach the site even if its fragments exist.
- `Divergences` fails the build on a resolution for a reference no longer cited,
  one landing in another book, one addressing no text in an edition holding that
  book, or a declared chapter nothing reaches.
- `check-calendar-masses`'s `psalm_numbering_exceptions` ledger is self-cleaning
  in both directions: an unlisted psalm-bounds breach fails, and a listed locus
  that has stopped breaching fails.
- Psalms are excluded from `citation_divergences` by construction — a second
  mechanism could only contradict the concordance.
- Structure files resolve every citation in **both** numbering systems, so no
  numbering logic ships to the browser.
- Rights on the psalm concordance, book indexes and alias tables are
  `project-created`: numbering facts, no third-party text.

## What fails silently

Ranked by how much damage it does before anyone notices.

1. **Numbering-system mismatch inside a chapter.** `Isaiah 9:5` against a
   Vulgate-numbered edition returns *garment mingled with blood*, not *For a
   CHILD IS BORN to us*. `Joel 3:1-5` returned *the valley of Josaphat*, not *I
   will pour out my spirit*. Both resolved. Both counted as successes. Twelve
   books now carry `citation_divergences` rows; what is left after them is in
   Open work below, and in the postconciliar calendar's `open_collation_items`.
2. **The departing edition, now refusing rather than lying.** The Clementine
   e-text numbers Psalm 115 to 10 and Psalm 147 to 9, where the concordance and
   published Vulgate data run them to 19 and 20. Until the clamp was removed this
   silently served `Psalm 115:10, 15, 16-17, 18-19` as one clause — a four-part
   responsorial psalm reduced to the last words of the wrong end. It now refuses,
   which is why the Clementine reports 12 unresolved against 3 for the Douay.
   **A higher unresolved count is the honest number, not the worse one.** There
   is still no departure table to record the divergence in.
3. **Unrecorded edition divergences.** Most of the 17 Douay/Clementine chapter
   differences have no explaining alias row. The Clementine's
   `verse-aliases.tsv` is a header line and nothing else.
4. **Unrecorded cross-edition shifts nothing currently cites.** The World English
   Bible Catholic Edition's Daniel 14 is one verse ahead of the Vulgate's
   throughout (its 14:1 is Vulgate 13:65); no alias row records it. It is inert
   only because no tracked calendar cites Daniel 13 or 14. Do not add such a
   citation without adding the rows.
5. **Unvalidated book indexes.** Six editions carry four different header lines.
   The Clementine declares no `chapters`/`verses` columns at all, so its book
   index cannot be checked against its own text. No schema governs any of them
   and no gate validates them; the five that do declare counts happen to agree,
   by luck rather than enforcement.
6. **The same citation string valid in two systems.** King James `2 Esdras 7:36`
   and Revised Version `2 Esdras 7:36` are unrelated text, 70 verses apart —
   the 1875 Bensly restoration. A bare system name is not a sufficient
   discriminator where two states of one tradition exist.

## Ownership — change the right file

| Fact | Owner | Never put it |
|---|---|---|
| Psalm number, verse and split correspondence | `psalm-numbering.tsv` (Douay artifact), read by `scripts/_psalms.py` | in a tool, a calendar, or a second table |
| Which system an edition is addressed in | `EDITIONS` in `tools/index-bible` (`numbering`, `psalter`, `psalm_titles`) | in the calendar |
| A verse this edition merged, or does not carry under that book | that edition's `verse-aliases.tsv` | in the calendar — the Douay and Clementine need different answers for 1 Thess 4 |
| Book names, tokens, aliases, per-book counts | that edition's `book-index.tsv` | in a shared alias table |
| Which target a calendar's citation means in a divergent book | that calendar's `citation_divergences` | in a tool |
| Psalm loci a calendar's own declaration cannot hold | that calendar's `psalm_numbering_exceptions` | anywhere permanent — the ledger is temporary and self-cleaning |
| Rights basis, jurisdiction, transformation | the artifact's `artifact.toml`; edition-level facts in `edition.toml` | in prose elsewhere |
| Whether a text may be served publicly | `publishable` in `EDITIONS`, via `index-bible manifest` | in a page filter |

Extend existing tools; do not add a program. `guidance/versification.md` §8.7
names the intended verbs (`index-bible inventory`, `index-bible divergences`,
`scripts/_versification.py`).

## Commands to check a claim

Run from the repository root. `$DR` and `$CV` below stand for the artifact
directories:

```sh
DR=src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts
CV=src/sources/works/catholic-church/vulgata-clementina/editions/ebible-latvuc/artifacts
KJ=src/sources/works/church-of-england/king-james-version/editions/ebible-engkjv/artifacts
```

**What does this edition actually print at a locus?**

```sh
awk -F'\t' '$1=="Is" && $2==9 && $3==6 {print $4}' $DR/verse-text-*/*.tsv
# -> For a CHILD IS BORN to us, and a son is given to us...
```

**Where does a chapter begin and end here?** — the question the clamp hides.

```sh
awk -F'\t' '$1=="1Thess" && $2==4 {n++; if(!lo||$3<lo)lo=$3; if($3>hi)hi=$3} \
  END{print lo"-"hi" ("n" verses)"}' $DR/verse-text-*/*.tsv   # -> 1-17 (17 verses)
awk -F'\t' '$1=="1Thess" && $2==4 {n++; if(!lo||$3<lo)lo=$3; if($3>hi)hi=$3} \
  END{print lo"-"hi" ("n" verses)"}' $CV/verse-text-*/*.tsv   # -> 1-18 (18 verses)
```

**What is the psalm correspondence for a given psalm?**

```sh
awk -F'\t' 'NR==1 || $1==115' $DR/psalm-numbering-*/psalm-numbering.tsv
# vulgate 115 verses 10-19 = hebrew 116:10-19 = english 116:10-19
```

**Convert, or find out why it refuses.** Never reimplement this arithmetic.

```sh
python3 -c "import sys; sys.path.insert(0,'scripts'); import _psalms
print(_psalms.convert_point(115, 10, 'vulgate', 'hebrew'))   # (116, 10, 'vulgate 115:10 is hebrew 116:10')
print(_psalms.psalm_extent(115, 'vulgate'))                  # (10, 19)
print(_psalms.english_verse(51, 3))                          # (1, '')  -- the Miserere
print(_psalms.validate_psalm(118, 137, 'hebrew'))            # 'Psalm 118:137 exceeds hebrew Psalm 118...'
"
```

**Is the index current, and what refuses?**

```sh
python3 tools/index-bible check --bible douay-rheims
python3 tools/index-bible check --bible world-english-bible-catholic --verbose
```

`check` is the default verb; a bare invocation reports drift rather than
rewriting a tracked file. Measured 31 July 2026: douay-rheims 3 unresolved,
douay-rheims-american-1899 8, clementine-vulgate 12,
world-english-bible-catholic 78, king-james-version 74, revised-version-1895 79.
These rose when the clamp came out. A citation that used to be truncated into a
neighbouring verse and counted as a success now refuses and is counted as one of
these.

**Does the alias table already explain a difference?**

```sh
cat $DR/verse-aliases-*/verse-aliases.tsv   # 7 merged-verse rows
cat $CV/verse-aliases-*/verse-aliases.tsv   # header only
cat $KJ/verse-aliases-*/verse-aliases.tsv   # 317 renumbered rows derived from the
                                            # deuterocanon concordance, plus 1594
                                            # numbering-not-recorded refusals
```

**Diff two editions' verse sets** — the derivation the repository does not yet
track. Adapt from `guidance/versification.md` §9.2; current results are
Douay/Clementine 17 differing chapters of 1,334 shared, Douay/King James 298 of
1,326 (plus 7 books only in the King James), King James/Revised Version 32 of
1,362.

**Parse a citation** — `tools/citations` owns what a reference string means.
Never write a second parser.

```sh
python3 tools/tpt citations parse "Baruch 3:9-15, 32-4:4"
python3 tools/tpt citations check --root src/sources/calendars
python3 tools/tpt check-calendar-masses
```

**Read the edition record before asserting anything about an edition.** Each
`edition.toml`'s `notes` field carries the measured divergences — canon shape,
which books follow the Greek division, which loci are withheld and why. They are
long because they were derived, not remembered.

## Canon shape — the facts, per edition

- Catholic canon: **73 books**. King James and Revised Version: **80**.
- The King James Apocrypha is **not** the Catholic deuterocanon. Its fourteen
  books are 7 deuterocanonical + 4 addition-books + **3 that no Catholic canon
  has**: `1Esdras`, `2Esdras`, `PrMan`.
- **Esther.** Douay/Clementine: 16 chapters, additions integrated as 10:4-16:24.
  King James and Revised Version: Esther 1-10 plus separate `EsthGr` carrying
  **the Vulgate's own numbers** 10:4-16:24 — so `Esther 13:9` routes by book
  redirection with no arithmetic. World English Catholic: 10 chapters, additions
  merged into the Hebrew numbering; Vulgate Esther 11-16 do not exist and those
  citations refuse.
- **Daniel.** Douay/Clementine: 14 chapters, ch. 3 to verse 100. King James and
  Revised Version: 12 chapters, ch. 3 to verse 30, plus `SgThree` (68 verses),
  `Sus` (64), `Bel` (42). Susanna is Vulgate Daniel 13:1-64 — but Daniel 13 has
  **65** verses and its 13:65 is `Bel` 1:1, so `Bel` runs one ahead of Vulgate
  Daniel 14 throughout and Vulgate 14:42 has no counterpart. `SgThree`'s 68
  verses against Vulgate 3:24-90's 67 need an alignment table, not a formula;
  no correspondence is asserted, and Vulgate Daniel 3:24-30 is withheld.
- **Greek-division books.** Tobit, Judith and Ecclesiasticus follow the Greek in
  the King James, Revised Version and World English Catholic: 244 / 339 / 1393
  (KJV) against the Douay's 298 / 345 / 1591. 48 of Sirach's 51 chapters differ.
  These are **different texts, not different numberings** — record `absent`, not
  a number.
- **Baruch.** Same 213 verses everywhere, different division: the King James joins
  at 3:34, so its chapter 3 ends at 37 and `Baruch 3:38` refuses there.
- **Revised Version omissions.** The revisers dropped verses the Vulgate and the
  Authorized Version carry — Matthew 17:21, 18:11, 23:14; Mark 7:16, 9:44, 9:46,
  11:26, 15:28; Luke 17:36, 23:17; John 5:4; Acts 8:37, 15:34, 24:7, 28:29;
  Romans 16:24; and 23 loci of Ecclesiasticus. Those numbers carry no text, so a
  citation of them refuses for want of the verse and a range crossing one refuses
  with it. This produces **gaps inside a chapter**: RV Acts 8 runs 1-40 with 39
  verses.

## Numbering — the facts

- Chapter correspondence, Vulgate to Hebrew: 1-8 identical; Vg 9 = Heb 9 + 10;
  Vg 10-112 = Heb +1; Vg 113 = Heb 114 + 115; Vg 114 + 115 = Heb 116;
  Vg 116-145 = Heb +1; Vg 146 + 147 = Heb 147; 148-150 identical.
- **Second, independent offset:** the Hebrew, Vulgate, Nova Vulgata and NAB count
  a psalm's inscription as verse 1; the English convention leaves it unnumbered.
  67 psalms carry an inscription row; the offset is one verse for 63 and **two**
  for four (Vulgate 50, 51, 53, 59). Both offsets apply at once: the *Miserere*
  is Vulgate 50:3 = Hebrew 51:3 = King James 51:1.
- **16 psalms divide their bodies differently as well** and are flagged
  `english_offset_uniform: no` — Hebrew 2, 4, 13, 20, 29, 43, 44, 53, 56, 72,
  100, 109, 126, 136, 146, 150. `english_verse` refuses for these. Do not apply
  the head-of-psalm offset. **These sixteen are externally corroborated and the
  list is complete.** Three independent detectors built only from outside data —
  SWORD `vm_vulg` verse counts against the Douay, TVTMS `SubdividedVerse` and
  `MergedPrevVerse` rows in its Latin column, and TVTMS Latin title treatment
  against the Douay's recorded offset — union to exactly these sixteen, no more
  and no less, and an independent word-overlap alignment against an external
  King James recovered the same sixteen and nothing else. TVTMS also reproduces
  the 2026-07-30 Psalm 12 correction verbatim, split and merge included.

- **Do not confuse a wrong verse number with a displaced verse boundary.** They
  are different defects of different severity, and the second is not what
  `english_offset_uniform` means. In the sixteen above the offset lands on
  *entirely different text*. In a larger set — an audit of 31 July 2026 proposed
  38, and hand-verified 7 of them — the verse count is equal, the offset is
  uniform, the verse *number* is right, and only the boundary is displaced by a
  clause: the King James Psalm 130:5 runs "I wait for the LORD, my soul doth
  wait" where the Douay's 129:4 already carries "my soul hath relied on his
  word". A reader lands within a verse of the passage rather than on a different
  passage. No external standard models this: TVTMS's `StartDifferent` relation
  exists for exactly it and is used three times in the whole file and never in
  the Psalms, Copenhagen's `partialVerses` has one Psalms entry, and SWORD has
  no subverse concept at all. So an external witness settles the sixteen and
  cannot settle the thirty-eight. Do not fold the second class into the first by
  flagging it `no`: that would take `english_verse` from refusing 16 of 150
  psalms to refusing 54, on a basis no standard supports, to describe a smaller
  error.
- **Beyond the psalter** (Nova Vulgata against every edition tracked here): Joel 4
  chapters vs 3; Malachi 3 vs 4; Isaiah 8 to v. 23 vs v. 22; Isaiah 64 with 11
  verses vs 12; Micah 4 to v. 14 vs v. 13. Resolutions:
  NV Joel 3 = Vg 2:28-32, NV Joel 4 = Vg 3; NV Mal 3:19-24 = Vg 4:1-6;
  NV Isa 8:23 = Vg 9:1; NV Isa 63:19b = Vg 64:1; NV Mic 4:14 = Vg 5:1.
- These five books are recorded citation-by-citation in the postconciliar
  calendar. A correspondence that holds unchanged is written out anyway: inside a
  divergent locus, silence is not evidence that anyone checked.

## Rights

- `public-domain` — tracked here, servable. Douay-Rheims Challoner (1749-1752),
  Clementine (1592), World English Catholic (public-domain dedication).
- **King James and Revised Version: jurisdictional.** Public domain in the US and
  everywhere outside the United Kingdom; inside the UK the Crown's perpetual
  letters patent still run and printing or importing printed copies is reserved
  to Cambridge, Oxford and Collins. Every artifact records
  `rights_jurisdiction = "United States"` and names the exception in
  `rights_basis`. Do not simplify this to "public domain".
- **`licensed` — Knox. Under copyright in the United States until 2039 at the
  earliest; the US renewals were found and are recorded below.** Do not re-run
  this research. On 31 July 2026 the question was asked whether a translation
  whose author died in 1957 could already be public domain, and it was settled
  from the primary record rather than by reasoning:

  | Work | Original | Renewal | Claimant | US copyright until |
  |---|---|---|---|---|
  | New Testament | A184908, 25 Oct 1944 | **R525394**, 13 Mar 1972 | Sheed & Ward, Inc. | 31 Dec 2039 |
  | Old Testament vol. 1, Genesis–Esther | A29371, 5 Nov 1948 | **R646862**, 5 Nov 1976 | Sheed, Andrews and McMeel | 31 Dec 2043 |

  Both are printed in the *Catalog of Copyright Entries* — the first at 3rd
  series vol. 26 part 1 no. 1 p. 1728, the second at vol. 30 part 1 no. 2
  p. 3284 — and each was confirmed in two independent renderings of that record.
  This is positive evidence of renewal, not an absence of evidence.

  Three consequences. **Sheed & Ward published it in New York**, so it is
  probably a United States work and the URAA analysis that would apply to a
  purely British work does not govern; it does not matter, because the renewals
  make the term 95 years from publication either way. **The territoriality
  argument does not rescue it**: it is public domain in life+50 countries such
  as Canada and New Zealand, and enters the public domain in the United Kingdom,
  the EU and Australia on 1 January 2028, but this project publishes from the
  United States, where it is protected for another thirteen years. That is the
  mirror image of the King James position above, and the reason the same
  jurisdiction note cannot do the same work here. **Two items were not found
  renewed** — Old Testament vol. 2 (1950) and *The Psalms: A New Translation*
  (1947) — but that is an absence of evidence in a corpus where simultaneity of
  publication was not established, so it settles nothing and must not be acted
  on.

- © Westminster Diocese, not redistributable.
  `tools/knox-bible` refuses any destination inside this repository; its index
  goes outside too via `mass-propers --bible-root <path>`; `publishable: false`
  keeps it out of the public artifact. Never commit its artifacts, never add it
  to a tracked bible root.
- Permission to *use* is not permission to *republish*. An imprimatur is not a
  copyright licence.
- Reference tables the project derived — psalm concordance, book indexes, alias
  tables — are `project-created` and carry no third-party text.
- Record the rights basis **before** ingesting external data, not after. Note for
  any future versification acquisition: STEPBible TVTMS is CC BY 4.0; the
  Copenhagen Alliance mappings are CC BY-**SA** 4.0, which is a copyleft
  obligation this project's CC BY 4.0 grant does not carry.

## The access boundary — what actually blocks each one

Searched 30 July 2026 and **not obtained: RNJB, NRSV, NABRE.** The reasons are
not the same, and only one of them is now a hard stop.

- **api.bible's terms forbid populating a local database**, whatever licence the
  text carries and whatever the project is willing to spend. That is a contract
  term, not a budget question, and it does not move.
- **`bible.usccb.org` blocks automated requests**, which is an obstacle rather
  than a prohibition. A licensed electronic edition obtained another way would
  answer it.
- **The Jerusalem Bible family is Darton, Longman and Todd copyright.** Reading
  it is a purchase; republishing it needs a licence. Those are two different
  permissions and obtaining the first grants nothing of the second.

The rule that once forbade proposing a paid source was withdrawn on 31 July 2026
(see `PROJECT-WORK.md`). Where one of these would settle a question, say what it
would cost and what it would answer.

Two consequences worth stating, because a later reader will otherwise re-derive
them:

- **The NABRE is the only English bible whose versification matches the
  postconciliar citations.** Not having it means nothing tracked here witnesses
  that numbering in English, which is why the postconciliar seam is settled
  citation-by-citation against the printed Douay instead of from a concordance.
- **The NRSV would not have helped.** It fails the same citations the Douay
  does; it is textually wrong for this project, not merely unobtainable.

## When you find a divergence

1. Establish which side is the departure by measuring both editions' printed
   verses. Do not assume the concordance is wrong.
2. Decide whether it is a fact about an **edition** (→ that edition's
   `verse-aliases.tsv`) or about a **citation** (→ that calendar's
   `citation_divergences`). If two editions in the same nominal system would need
   different answers, it is an edition fact.
3. If no correspondence can be established, record the refusal rather than an
   offset. `not-in-this-edition` and `numbering-not-recorded` already exist as
   alias kinds and are the right answer.
4. Never return a plausible wrong verse. A refusal carrying its reason through to
   `unresolved` is a correct result; a superset is not a hit and must be declared
   as one if it is ever returned.
5. Rebuild and re-check the affected indexes; do not hand-edit `index.yaml` or a
   chapter fragment.

## Open work — do not report as done

Measured 31 July 2026. Re-measure before quoting any figure here.

- **The Douay and the Clementine still disagree in 17 of their 1,334 shared
  chapters, and most of it is unrecorded.** Three carry an explaining
  `merged-verse` row in the Douay's alias table (2 Kings 13, Psalm 28, Amos 9)
  and two more are the psalm splits the concordance owns (Psalms 115 and 147).
  The rest have no row anywhere, and the Clementine's `verse-aliases.tsv` is
  still a header line and nothing else.
- **1 Thessalonians 4 and 2 Thessalonians 2 are the two that break live
  citations.** The Douay e-text joins verses the Clementine prints separately, so
  those chapter tails stand one number low: `1 Thessalonians 4:13-18` goes
  unresolved and `2 Thessalonians 2:14` and `2:16-3:5` resolve to the wrong
  verses, in the tracked Douay and in the Catholic Public Domain Version alike.
  This is an edition fact, not a numbering divergence — the remedy is
  `merged-verse` rows in each edition's own alias artifact.
- **Sirach and John 6 mix two numbering systems inside one calendar.** Settling
  the postconciliar citations showed that Sirach 15:16-21, 24:1-4 and 27:5-8 are
  in the Vulgate's own numbering and needed no correction, while others in the
  same file are not. Those loci are therefore `unrecorded` for a Greek-numbered
  edition and cannot be served by one ruling while the mixture stands.
  Normalizing them onto one system would return about twenty references to the
  English indexes.
- **Two beatitude citations cannot be told apart.** The `ot-4` Communion Antiphon
  cites Matthew 5:3-4 and the Easter Vigil canticle Matthew 5:5-6, where the
  Vulgate and the Nova Vulgata exchange the meek and those who mourn. Both
  resolve to real beatitudes either way and the recorded incipit is too short to
  say which was meant. Settle against the printed antiphon, not by reasoning.
- **10 psalms, 19 loci, carry Vulgate numbers in a Hebrew-declared file.** Listed
  under the postconciliar calendar's `psalm_numbering_exceptions`, which is
  self-cleaning in both directions and is meant to empty.
- **No `verse-inventory` artifact, no book-index schema, no cross-edition
  divergence register.** All three are proposed and unbuilt in
  `guidance/versification.md` §8. The fourth item that section proposes — a
  concordance beyond the psalter — now exists for Esther, Sirach and Daniel as
  the Douay's `deuterocanon-numbering` artifact, read by
  `scripts/_deuterocanon.py`.

Settled, so that a later reader does not re-open them: the clamp is gone from
`Bible.span`, which now looks up every verse a range names and refuses rather
than truncating, and consults the alias table before deciding a chapter is
absent. `citation_divergences` has grown from four books to twelve.
