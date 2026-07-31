# Versification: resolving a citation against an edition that divides the text differently

A design study for the class of defect where a scripture citation **resolves
successfully and wrongly** — where the resolver returns real text under a
correct-looking reference and nothing counts it as a failure.

It surveys how the problem is solved elsewhere, establishes by measurement what
this repository can and cannot derive from the editions it already tracks, and
proposes a data model, a resolution contract, and a set of gates.

Nothing here has been built. Where it says "must", it states a requirement on
the implementation, not current behaviour.

## Evidence conventions

- **[verified]** — measured during this study, either against this
  repository's tracked artifacts or by fetching an external file and inspecting
  its bytes. Reproducible.
- **[sourced]** — reported from an external document, cited with a URL, read
  but not independently re-derived.
- **[inferred]** — reasoned from the above. Flagged wherever it matters.

---

## 1. The failure, stated precisely

A citation is a triple: a **book name**, a **locus** (chapter, verse, sometimes
a part-verse letter), and — almost always unwritten — the **numbering system**
the citing authority used. The resolver receives the first two and guesses the
third. When the guess is wrong and the target edition happens to print
something at those numbers, wrong words are returned in silence.

### 1.1 What is shipping wrong today

**[verified]** `src/sources/bibles/clementine-vulgate/index.yaml` contains:

```yaml
  Psalm 115:10, 15, 16-17, 18-19: in atriis domus Domini, in medio tui, Jerusalem.
```

A four-part responsorial psalm rendered as one verse, and the wrong one. Two
defects combined:

1. The psalm concordance renumbers Hebrew 116 into Vulgate 115 using the
   numbering the **Douay-Rheims** prints, where Vulgate Psalm 115 runs verses
   **10-19**. The tracked **Clementine Vulgate** prints it as verses **1-10**.
   Both editions declare `numbering: vulgate`, `psalter: gallican`.
2. Verses 15-19 fall past the Clementine's chapter end and are silently
   clamped away, leaving verse 10 — which in the Clementine is the *last* verse
   of the psalm (*in atriis domus Domini*), not the first (*Credidi, propter
   quod locutus sum*).

**[verified]** by diffing the two editions' `verse-text-*` artifacts:

| Psalm | Douay-Rheims prints | Clementine prints |
|---|---|---|
| 115 | verses 10-19 | verses 1-10 |
| 147 | verses 12-20 | verses 1-9 |

`scripts/_psalms.py` treats
`.../challoner-gutenberg-1581/artifacts/psalm-numbering-*/psalm-numbering.tsv`
as describing **the Vulgate system**. It describes **one edition's printing of
it**. That confusion — between a numbering system and an edition's witness of
it — is the root of everything in this document.

### 1.2 The scale of divergence inside the tracked library

**[verified]** comparing per-chapter verse sets across the tracked editions:

| Pair | Shared chapters | Chapters whose verse sets differ | Books in only one |
|---|---|---|---|
| Douay-Rheims vs Clementine | 1334 | **17** | none |
| Douay-Rheims vs King James | 1326 | **298** | Vulgate side: Daniel 13-14, Esther 11-16. KJV side: 1Esdras, 2Esdras, Bel, EsthGr, PrMan, SgThree, Sus |
| Clementine vs King James | 1326 | **291** | as above |

Seventeen disagreements between **two witnesses of the same Vulgate**. Four are
covered by a row in the Douay's `verse-aliases` artifact; thirteen are not:

| Book/chapter | Douay | Clementine |
|---|---|---|
| 1 Thessalonians 4 | 1-17 | 1-18 |
| 2 Thessalonians 2 | 1-16 | 1-17 |
| Ecclesiasticus 29 | 1-34 | 1-35 |
| Isaiah 45 | 1-26 | 1-25 |
| Isaiah 46 | 1-12 | 1-13 |
| Judith 4 | 1-16 | 1-17 |
| Psalm 15 | 1-11 | 1-10 |
| Psalm 19 | 1-9 | 1-10 |
| Psalm 42 | 1-6 | 1-5 |
| Psalm 115 | 10-19 | 1-10 |
| Psalm 125 | 1-7 | 1-6 |
| Psalm 135 | 1-27 | 1-26 |
| Psalm 147 | 12-20 | 1-9 |

**[verified]** The Clementine's `verse-aliases.tsv` is a header and nothing
else, and carries two columns where the Douay's and the King James's carry four
(`kind`, `note`). The three `book-index.tsv` artifacts carry three different
column sets — the Douay has `chapters`/`verses`/`note`, the Clementine has
neither, the King James adds `kjv_title`. **No schema governs either artifact
and no gate validates their contents.** The Douay's declared per-book counts do
agree with its verse text (73 books, 35 804 verses, zero mismatches)
**[verified]** — but that is luck, not enforcement, and the Clementine cannot
be checked at all because it declares no counts.

### 1.3 The silent clamp

`tools/index-bible`, in `Bible.span`, derives a chapter's bounds from the
verses the edition prints and truncates the request to fit:

```python
for verse in range(low, min(high, bound) + 1):
```

**[verified]** by replaying every calendar citation against each edition:

| Edition | Citations naming a verse past a chapter end |
|---|---|
| Douay-Rheims | 4 — `1 Thessalonians 4:13-18`, `Acts 7:55-60`, `Malachi 3:19-20a`, `Mark 4:35-41` |
| Clementine | 17 — the above less 1 Thessalonians, plus every Psalm 115, 147 and 15 citation |

Three of the Douay's four lose no text, because the verse the Vulgate merged
them into carries the words. The Clementine's psalm cases lose the passage and
keep a wrong fragment. **A defect harmless in one edition and destructive in
another is exactly the kind that survives review.**

### 1.4 The unwritten third element

**[verified]** The postconciliar calendar declares `psalm_numbering: hebrew`
for the whole file *and* `citation_convention: Lectionary readings and antiphons
preserve the numbering in the controlling missal`. Those contradict each other,
and the file proves it — eleven antiphons carry Vulgate psalm numbers, already
recorded under `psalm_numbering_exceptions`.

The same split runs through the New Testament, inside a single chapter. Each
antiphon's printed Latin incipit matched against the tracked Clementine text
**[verified]**:

| Cited as | Incipit | Clementine verse carrying those words | System spoken |
|---|---|---|---|
| John 6:35 | *Ego sum panis vitae* | 6:35 | agrees in both |
| John 6:51 | *Panis, quem ego dedero* | 6:52 | Greek |
| John 6:51-52 | *Ego sum panis vivus* | 6:51-52 | **Vulgate** |
| John 6:55 | *Qui manducat meam carnem* | 6:55 | **Vulgate** |
| John 6:56 | *Qui manducat meam carnem et bibit meum sanguinem* | 6:57 — or 6:55 | Greek, probably; see below |
| John 6:57 | *Qui manducat meam carnem* | 6:57 | **Vulgate** |
| John 6:58 | *Sicut misit me vivens Pater* | 6:58 | **Vulgate** |
| John 6:63c | *Verba tua, Domine, Spiritus et vita sunt* | 6:64c | Greek |
| John 6:68c | *verba vitae aeternae habes* | 6:69c | Greek |

The cause is structural: the Vulgate splits Greek John 6:51 into 6:51 (*Ego sum
panis vivus, qui de cælo descendi*) and 6:52 (*Si quis manducaverit ex hoc
pane...*), so from 6:52 the Vulgate runs one ahead **[verified]**. Antiphons
that kept the Missal's Latin numbering are correct as printed; readings and
Gospel acclamations taken from the Lectionary are not. They sit in the same
Mass.

`John 6:56` shows the limit of automatic disambiguation: Clementine 6:55 and
6:57 **both** open *Qui manducat meam carnem et bibit meum sanguinem* and
differ only in the second half. The incipit cannot decide, and a resolver must
say so rather than pick.

---

## 2. Three problems, currently conflated

| # | Question | Derivable? | Where it lives now |
|---|---|---|---|
| 1 | **Inventory** — which loci does this edition print? | Yes, fully, from tracked verse text | Recomputed at runtime in `Bible.__init__`; never asserted, never tracked |
| 2 | **Alignment** — which locus in system Y carries the words system X numbers thus? | Partly; see §5-6 | `scripts/_psalms.py` (psalter only); `verse-aliases` (scattered loci); `citation_divergences` (four books) |
| 3 | **Attribution** — which system is *this citation* written in? | **No.** An editorial fact about the citing document, varying slot by slot | One file-level `psalm_numbering` key plus a growing exception list |

The most consequential blur is `citation_divergences`, which records a
**resolved target reference** rather than the citation's **source system**:

```yaml
    "Isaiah 8:23-9:3": "Isaiah 9:1-4"
```

That answer is correct for Vulgate-numbered editions and must be rewritten for
any other. It also cannot express the case where two editions in the *same*
nominal system need different answers — not hypothetical:
`1 Thessalonians 4:18` needs `4:17` for the Douay and `4:18` for the Clementine
**[verified]**. The calendar is being asked to know things about editions,
which is not its business.

---

## 3. Prior art

### 3.0 Where the divisions came from, and why that matters here

The divisions were not designed. They accreted, in a particular order, and the
order explains which divergences exist.

**Verses are older than chapters, in the Hebrew.** The Masoretic *pesuqim*,
delimited by *sof pasuq* (׃), are attested in the manuscript tradition by at
least the tenth century **[sourced]**. They were delimited and counted, never
numbered. Every later Old Testament versification "correspond[s] predominantly
with the existing Hebrew sentence breaks."

**Chapters: Langton, with a serious caveat.** The conventional attribution is
to Stephen Langton (c. 1150-1228) at Paris, c. 1203-1205. But the attribution
itself traces to **Nicholas Trevet's *Annales regum Angliae*, fourteenth
century** — roughly a century after the fact, not a contemporary witness
**[sourced]**. Paul Saenger identified St Albans manuscripts, now at Corpus
Christi College Cambridge, datable to **c. 1180** and already carrying the
modern divisions in the margin in a hand contemporary with the text; Langton's
own writings use them only sporadically. Saenger's conclusion is that the
system is English in origin and older than Langton's Paris teaching
**[sourced]**:

- Paul Saenger, "The British Isles and the Origin of the Modern Mode of
  Biblical Citation," *Syntagma* 1 (2005): 77-123 —
  <https://dialnet.unirioja.es/servlet/articulo?codigo=1165926>
- Paul Saenger, "The Twelfth-Century Reception of Oriental Languages and the
  Graphic *Mise en page* of Latin Vulgate Bibles Copied in England," in Poleg
  and Light (eds.), *Form and Function in the Late Medieval Bible* (Brill,
  2013)
- J. H. A. van Banning, "Reflections upon the Chapter Divisions of Stephan
  Langton," in *Method in Unit Delimitation* (Brill, 2007), 141-161

Hugh of Saint-Cher is sometimes credited, but his concordance of the 1230s
*presupposes* a division rather than creating one; his plausible role is
dissemination. **Lanfranc: no supporting source was found for this attribution
at all, and it should be treated as an error unless someone can produce one.**

**Verses, printed: Pagnino then Estienne** **[sourced]**. Santes Pagnino's
*Veteris et Novi Testamenti nova translatio* (Lyon, 1527/1528 — the sources
disagree, probably a 1527 title page with a 1528 colophon) divided the Old
Testament, and **that division became standard**. Robert Estienne's 1551 Geneva
Greek New Testament carried the first numbered New Testament verses, in the
margins; his **1555 Latin Vulgate was the first Bible to print verse numbers in
the running text**. The Sixto-Clementine Vulgate of 1592 adopted Estienne's
1551 enumeration, which is why the Clementine numbering is the Catholic
baseline this repository's two Vulgate editions inherit.

**The consequence that governs §5.** Estienne made his divisions in a *Latin*
Bible. English Bibles inherited them. That is why the tracked King James, a
Masoretic-*text* witness, is an English-*versification* witness and sits with
the Vulgate at Joel, Malachi, Isaiah 8/9, Micah 5, Exodus 21 and Hosea 1.

**The psalter's two independent offsets.** The chapter correspondence is the
familiar one **[sourced]**, confirmed against the Nova Vulgata's own printed
headings (`PSALMUS 10 (Vg 9, 22-39)`):

| Hebrew | Greek/Vulgate | |
|---|---|---|
| 9-10 | 9 | one psalm in Greek; MT 10 = Vg 9:22-39 |
| 114+115 | 113 | |
| 116 | 114 + 115 | MT 116:1-9 = Vg 114; 116:10-19 = Vg 115 |
| 147 | 146 + 147 | MT 147:1-11 = Vg 146; 147:12-20 = Vg 147 |

148-150 realign because the two joins and the two splits cancel exactly.
**Superimposed on this is a second, independent offset**: the Hebrew, the
Vulgate, the Nova Vulgata and the NAB count a psalm's superscription as verse 1
(or 1-2 where it is long); most traditional English versions leave it
unnumbered. The NABRE Psalms introduction states it plainly **[sourced]** —
"many of the traditional English translations are often a verse number behind
the Hebrew because they do not count the superscriptions as a verse" — and it
affects some 62 psalms by up to two verses. `scripts/_psalms.py` already models
both offsets separately, which is correct and should be preserved through any
generalization.

### 3.1 Family A — whole-verse renumbering against a single base

**Paratext / UBS / SIL `.vrs` files.** Six built-in schemes, with numeric ids
**[sourced]**, from `VersificationType` in SIL's `machine.py` and the identical
switch in libpalaso's `Versification.cs`:

| id | name | file |
|---|---|---|
| 1 | Original | `org.vrs` |
| 2 | Septuagint | `lxx.vrs` |
| 3 | Vulgate | `vul.vrs` |
| 4 | English | `eng.vrs` |
| 5 | Russian Protestant | `rsc.vrs` |
| 6 | Russian Orthodox | `rso.vrs` |

- <https://github.com/sillsdev/machine.py/blob/main/machine/scripture/verse_ref.py>
- <https://github.com/sillsdev/libpalaso/blob/master/SIL.Scripture/Versification.cs>
- <https://github.com/sillsdev/libpalaso/tree/master/SIL.Scripture/Resources>

A custom versification is not a seventh id: it is `Unknown` plus a **delta over
a named base** **[sourced]**. Line types are `#` comment, `BOOK C:V C:V …`
verse counts (chapter numbers explicit, so a custom file may be sparse, with a
literal `END` token truncating a book), `BOOK A:B = BOOK C:D` mapping,
`&…` one-to-many mapping, `-BOOK C:V` excluded verse, `*BOOK C:V,seg,…` verse
segments, and a `#!` forward-compatibility escape that a pre-7.3 parser reads
as a comment.

Every scheme maps to `org`; there is no direct `eng`↔`lxx` mapping, so
cross-scheme resolution is always a two-hop round trip **[sourced]**.

The format's own limit is written into `eng.vrs` as disabled lines
**[sourced]**:

```
# NUM 26:1a = NUM 25:19b  # no support for splits yet
```

**The `.vrs` mapping format cannot express a mid-verse split.**

**Copenhagen Alliance JSON** is the same model in JSON, and is the artefact
worth actually using — <https://github.com/Copenhagen-Alliance/versification-specification>.
Six properties: `basedOn`, `maxVerses`, `mappedVerses`, `excludedVerses`,
`mergedVerses`, `partialVerses`. Its schema `$id` is
`https://burrito.bible/schema/ingredients/versification.schema.json`, so this
is also Scripture Burrito's canon-constraints ingredient.

UBS's own sibling repo is candid about quality **[sourced]**,
<https://github.com/ubsicap/versification_json>:

> Historically, the mapping section has not been validated. (It would be quite
> hard to do this.) The current JSON examples include cases of mapping from
> verses that do not exist … This is not ideal, but the solution is not obvious.

**`vref.txt`** is the flattened consumer form: **41 899 lines**, `org`
versification, 89 books **[sourced]**, at
<https://github.com/BibleNLP/ebible/blob/main/metadata/vref.txt>. Three cell
states — text, blank (absent), `<range>` (merged into an earlier line). Merges
record the fact but not the split point; reordering is not representable at
all. `biblelib` demonstrates the right relationship: a `vref` is a **derived
artefact** of a scheme, regenerated and asserted byte-identical by a test
**[sourced]**, <https://github.com/Clear-Bible/Biblelib>. That is the pattern
§7.1 adopts.

### 3.2 Family B — conditional, subverse-addressable transformation

**STEPBible TVTMS** — *Translators Versification Traditions with Methodology
for Standardisation*, Tyndale House Cambridge, **CC BY 4.0** **[sourced]**:
<https://github.com/STEPBible/STEPBible-Data/tree/master/Versification>.
One file, ~5.8 MB, 29 896 lines, in two datasets: a **condensed** section of
429 human-readable records and an **expanded** section of **24 922** machine
rows with columns `SourceType | SourceRef | StandardRef | Action | NoteMarker |
Reversification Note | Versification Note | Ancient Versions | Tests`.

Three things it has that Family A does not:

1. **Subverse addressing**, three interchangeable spellings — `Gen.6:1.2`,
   `Gen.6:1b`, `Gen.6:1!b` — with the invariant that **subverse 0 is the text
   present in all Bibles**, additions being 1..n. That makes a split
   addressable without renumbering anything downstream.
2. **A relation vocabulary** — `OneToOne`, `SubdividedVerse`, `MergedVerse`,
   `LongVerse`, `LongVerseElsewhere`, `StartDifferent`, `PassageMoved`,
   `TextMayBeMissing`, `Colophon`, `PassageMissing` — and three distinct senses
   of *Absent*: `Absent [=Ref]` (text is elsewhere), `Absent [Ref]` (an empty
   numbered slot exists), bare `Absent` (the source simply lacks it).
3. **Test-gated rules.** A row applies only if its `Tests` hold
   (`Gen.32:33=Last`), which is how an unknown text's versification is
   *inferred* rather than declared.

It also states where mapping should stop **[sourced]**:

> Occasionally it is better to leave versification uncorrected, as with ESV
> Rev.12.17. The difference is equivalent to moving the verse division by a few
> words, and a correction will merely add confusion.

The Copenhagen repo's `versification-sniffing/rules/*.json` is TVTMS's
condensed section compiled to JSON — the one artefact living in both families.

### 3.3 Family C — a pivot edition (SWORD / CrossWire `av11n`)

Eighteen registered schemes **[sourced]** — `KJV`, `Leningrad`, `MT`, `KJVA`,
`NRSV`, `NRSVA`, `Synodal`, `SynodalProt`, `Vulg`, `German`, `Luther`,
`Catholic`, `Catholic2`, `LXX`, `Orthodox`, `Calvin`, `DarbyFr`, `Segond` —
from `registerVersificationSystem()` in
<https://crosswire.org/svn/sword/trunk/src/mgr/versificationmgr.cpp>. A scheme
is two `sbook[]` arrays plus a flat verses-per-chapter array in
`include/canon_*.h`.

**The pivot is KJVA, not KJV**, in both engines. Two incompatible mapping
implementations exist from unshared data: SWORD's compact binary
`unsigned char[7|8]` tables covering **6 of 18** schemes, and JSword's
`.properties` files covering **12 of 18** **[sourced]**,
<https://github.com/crosswire/jsword/tree/master/src/main/resources/org/crosswire/jsword/versification/>.
Neither is a superset of the other, and **LXX and Orthodox have no mapping in
either**.

Three findings from this family bear directly on the proposal:

- **The C++ format cannot express "absent."** No rule means identity mapping,
  silently. This is the project's own defect, implemented as a data format.
- JSword's `!a`/`!b` part markers exist **solely** to make the KJVA pivot
  round-trippable through a merge; without them A→KJVA→B smears one verse into
  a range **[sourced]**.
- **The pivot is documented-by-data as insufficient for the deuterocanon.**
  JSword's `Catholic2.properties` carries `Esth.15.1-Esth.15.3=?` — three
  verses with no KJVA counterpart at all — alongside `Dan.14.43=?BelThenKingSaid`
  and `Dan.3.34-Dan.3.100=?SongOfThreeChildren`, while SWORD's `mappings_vulg[]`
  has **zero rules for Tobit, Judith, Esther, Sirach or Baruch** **[sourced]**.

Also worth quoting, because it is the distinction the whole design turns on —
`canon_vulg.h`'s own header note **[sourced]**:

> this is not based on any single edition of the Vulgate, but on myriad
> editions on the Vulgate and translations of the Vulgate … As such, it is
> probable that every Bible will contain some empty verses (and most will have
> empty books). This versification system is explicitly NOT intended for the
> Nova Vulgata.

**A scheme is a superset, not a description of any real edition.** That is
precisely the §1.1 confusion, named by the people who built the thing.

And the design decision that produced the situation, from the CrossWire wiki
**[sourced]**, <https://wiki.crosswire.org/Alternate_Versification>:

> Without this identification, the versification system will default to "KJV"
> for backward compatibility.

> The final step (in >1.6.0) will be to allow mappings between versification
> schemes …

Mapping was deferred, not designed in. Sixteen years later six of eighteen
schemes have it.

### 3.4 Family D — digital-library citation infrastructure

**CTS / CITE.** The URN grammar is
`urn:cts:CTSNAMESPACE:TEXTGROUP.WORK.VERSION.EXEMPLAR:PASSAGE`, mapping to FRBR
work / expression / item with no manifestation level **[sourced]**,
<https://cite-architecture.github.io/ctsurn_spec/>.

Its founding assumption is exactly the failure case **[sourced]**:

> The passage component is a hierarchy of one or more levels expressing a
> logical citation scheme **applying to all versions of a text**.

CTS asserts that the citation scheme belongs to the notional work and that
every version is addressable by it. Cross-version alignment is out of scope:
the seven requests never take two version URNs, and the five-code error table
has "syntactically valid URN refers in invalid value" with no "here is where it
is instead" **[sourced]**, <https://cite-architecture.github.io/cts_spec/>.

**DTS 1.0** (2026-02-13) is closer — <https://dtsapi.org/specifications/> — and
its `citationTrees` array with `citeStructure`/`citeType` is the right
vocabulary. Its own Josephus example is structurally the Vulgate/Masoretic
case: *"the same stretch of text can be identified as 7.8.6-7.9.2 or as
7.320-402"*. But DTS models **many schemes over one document**; this project
needs **one citation across many documents**. It gives a place to declare the
trees and no operation to convert between them.

**Failure behaviour** is the borrowable part. MyCapytain, the CTS reference
implementation, distinguishes four failure modes where a naive resolver has one
**[sourced]**,
<https://github.com/Capitains/MyCapytain/blob/master/MyCapytain/errors.py>:
`InvalidURN` (malformed), `UnknownObjectError` (names nothing),
`CitationDepthError` (*"the depth of a requested citation is deeper than the
citation scheme of the text"*), `RefsDeclError` (shaped right, resolves to
nothing). DTS mandates 404 for a `ref` absent from the tree.

**OSIS** is the only specification found that treats overlapping citation
systems as a first-class encoding problem **[sourced]**, OSIS 2.1.1 User
Manual, <https://www.crosswire.org/osis/>. `osisRef` is
`[WORK.SUBWORK:]BOOK[.CHAP[.VERSE]][!extension][@grain]`, versification reached
indirectly through the work's `<refSystem>`, with reserved names including
`Vugl` *(sic)*, `LXX`, `MT`, `Synodal`. Two rules are directly reusable:

> It is highly undesirable to call these separate versification schemes,
> because they differ so slightly; because the differences can be mechanically
> resolved; and because there is considerable overhead to maintaining and
> mapping among versification schemes.

> Such subdivisions are not standard across different translations, so
> applications must be prepared to discard them when trying to locate a
> referenced location in a different edition.

The first is an argument for **edition departure tables rather than a new
system per edition** — which §7.3 adopts. The second is a free, correct,
non-obvious rule for the project's 118 part-verse citations **[verified]**:
strip everything after the part letter before cross-edition matching.

**Applied to the Bible, CTS is a shell.** `urn:cts:greekLit:tlg0527` is the Old
Testament textgroup, and its Genesis directory holds exactly one text — a
modern public-domain English translation, filed under a Septuagint author code
**[sourced]**. No Vulgate was found under `canonical-latinLit`. The interop
payoff is zero.

### 3.5 Also relevant

- **USFM 3.1** distinguishes `\ca`/`\va` (*alternate* chapter/verse — a
  semantic claim that the text carries two versification traditions) from
  `\cp`/`\vp` (*published* — presentational only) **[sourced]**,
  <https://docs.usfm.bible/usfm/3.1/cv/va.html>. Both editions in this library
  are derived from eBible USFM, so this distinction governs what the upstream
  artifacts can even tell us. Verse bridges (`\v 1-2`) are defined not in prose
  but by pattern in the USX RelaxNG schema, which also admits `,` for disjoint
  sets and forbids a chapter in `number` while allowing one in `altnumber`.
- **`bible-passage-reference-parser`** is the only reference parser found with
  versification awareness, offering `vulgate` and `nab` among its systems — but
  it is aware for *validation*, not *mapping* **[sourced]**,
  <https://github.com/openbibleinfo/Bible-Passage-Reference-Parser>.
  `curiousdannii/reversify` is its scheme-changing plugin.
- **Dead ends, recorded so nobody re-chases them** **[sourced]**: openscriptures
  has no versification dataset; `scrollmapper/bible_databases` has no
  versification model at all and its flat schema implies all 140 translations
  share one numbering; there is no `bibleref` URI scheme at IETF or
  microformats; Scripture Burrito has **no** versification property (its
  `numbering_system` is Unicode CLDR digit shapes).

### 3.6 The organizing claim

**Families A and B are incompatible, and the choice between them is the design
decision.** Family A models versification as whole-verse renumbering against
one base and says in its own source comments that it cannot represent splits.
Family B models it as conditional, subverse-addressable transformation among
~40 traditions with an explicit vocabulary for merge, split, move, duplicate
and absent. Family C shows what happens when you pick a pivot *edition* rather
than a base *scheme*: the deuterocanon breaks, because the pivot has no address
for text it does not contain. Family D contributes no mapping at all, but
contributes the two best rules in this document: **alignment belongs in a third
resource**, and **failures must be typed**.

---

## 4. Is there a canonical intermediate?

### Verdict

**No single canonical verse space, and not pairwise mappings between editions
either. The right structure is a small named set of *systems*, a segment-level
concordance between chosen *pairs* of systems, and a per-edition record of
where an edition departs from the system it declares.** Three claims:

**(a) A single universal verse space cannot exist, because the disagreement is
about how much text there is.** Sirach settles it. **[verified]** Comparing the
tracked Douay (Englished from the Latin) against the tracked King James
Apocrypha (Englished from the Greek), **48 of Sirach's 51 chapters differ in
verse count**; only 6, 14 and 18 agree. The Latin carries expansions the Greek
does not, scattered through every chapter. There is no numbering of "Sirach"
that both editions are numbering differently; there are two texts.

The people who publish the mapping data say the same thing in the same words
**[verified]** — the Copenhagen `standard-mappings/README.md`:

> **No mapping is done from Vulgate to Septuagint for TOB, JDT, or SIR since
> they follow a different Vorlage than the Septuagint text.**

**(b) Pairwise mappings between *editions* would be quadratic and would repeat
work.** Four editions is six pairs; most pairs differ for the *same* reason,
and recording that reason six times guarantees drift. The project has already
been bitten: `scripts/_psalms.py` opens by noting that the restated copies
"disagreed, and gave Hebrew 10 and 115 the last verse of the Vulgate psalm
hosting them rather than their own."

**(c) Therefore systems as the unit of alignment, editions as witnesses.** A
system is an abstract addressing scheme; alignment rows join two systems; an
edition declares which system addresses it and carries a table of its own
departures. This is what `_psalms.py` already does for the psalter, minus the
§1.1 confusion.

### The rule that makes it safe: mappings do not compose

If the concordance holds `vulgate ↔ org` and `org ↔ nova-vulgata`, it must
**not** silently chain them. Each mapping is lossy at every split and merge,
and composing two lossy maps yields a plausible wrong answer with no signal.
A composed route may be used only where the implementation can prove both hops
are one-to-one across the *specific* segment; otherwise it refuses and asks for
a direct row.

This is the discipline pivot designs get wrong, and JSword's `!a`/`!b` markers
exist precisely because CrossWire hit it **[sourced]**.

### Why segments, not verses

The psalm table covers 2 528 verses in 220 rows, because a *segment* — a
maximal run both systems number without interruption — is the natural unit.
Verse enumeration would be 12× the data and would hide the structure a reviewer
needs to see. Both external families agree; keep segments.

---

## 5. The finding that scopes the project

**No edition this repository tracks witnesses the numbering its principal
calendar cites in.** **[verified]**:

| Locus | Nova Vulgata / Masoretic | Douay | Clementine | King James |
|---|---|---|---|---|
| Joel | 4 chapters | 3 | 3 | 3 |
| Malachi | 3 chapters | 4 | 4 | 4 |
| Isaiah 8 | ends at v. 23 | 22 | 22 | 22 |
| Micah 4 | ends at v. 14 | 13 | 13 | 13 |
| Exodus 21 | ends at v. 37 | 36 | 36 | 36 |
| Hosea 1 | 9 verses | 11 | 11 | 11 |

The King James is a Masoretic-**text** witness but an English-**versification**
witness: it inherits the Vulgate's boundaries at precisely these loci, because
Estienne made his verse divisions in a Latin Bible. Adding it adds no witness
of Hebrew or Nova Vulgata numbering.

The comment in `tools/index-bible` is therefore right and should stay — "this
library tracks no witness of the Nova Vulgata. There is nothing here to compile
a concordance from." What changes is the shape of the recorded fact, and the
fact that **the numbers can be acquired even though the text cannot** (§6).

### Why the Lectionary's numbering is not the Nova Vulgata's — and is allowed not to be

This is the authoritative explanation of the whole postconciliar mess, and it
should be recorded because a future session will otherwise re-derive it.
*Liturgiam authenticam* (Congregation for Divine Worship, 7 May 2001) §37
**[sourced]**,
<https://www.vatican.va/roman_curia/congregations/ccdds/documents/rc_con_ccdds_doc_20010507_liturgiam-authenticam_en.html>:

> … the *Nova Vulgata Editio* is the point of reference as regards the
> delineation of the canonical text. Thus, in the translation of the
> deuterocanonical books and wherever else there may exist varying manuscript
> traditions, the liturgical translation must be prepared in accordance with
> the same manuscript tradition that the *Nova Vulgata* has followed. If a
> previously prepared translation reflects a choice that departs from that
> which is found in the *Nova Vulgata Editio* as regards the underlying textual
> tradition, the order of verses, or similar factors, the discrepancy needs to
> be remedied … **In preparing new translations, it would be helpful, though
> not obligatory, that the numbering of the verses also follow that of the same
> text as closely as possible.**

**Textual tradition and verse order are binding; verse numbering is explicitly
not.** So the *Ordo Lectionum Missae* cites in Nova Vulgata numbering while the
US *Lectionary for Mass* cites in NAB numbering, both legitimately, and the two
citations of one pericope differ. The postconciliar file in this repository
therefore contains citations in **at least three** systems — the Missal's
Vulgate numbers in antiphons, Nova Vulgata numbers, and NAB numbers — and no
file-level declaration can be true of all of them. §8.4 follows from this
paragraph.

### What the Nova Vulgata actually does, book by book

**[sourced]**, verified against <https://www.vatican.va/archive/bible/nova_vulgata/>:

| Book | Nova Vulgata | Consequence for this project |
|---|---|---|
| Psalms | **Hebrew numbering**, Vulgate number in parentheses (`PSALMUS 11 (10)`) | the calendar's `psalm_numbering: hebrew` is right for responsorial psalms |
| Joel | 4 chapters | as already recorded |
| Malachi | 3 chapters, ch. 3 to v. 24 | as already recorded |
| Isaiah | ch. 8 to v. 23; ch. 64 has 11 verses | as already recorded |
| Micah | ch. 4 to v. 14 | as already recorded |
| Hosea | ch. 1 has 9 verses — **NV agrees with the NAB here; it is the English/Vulgate tradition that departs** | explains the +2 verified in §6.1 |
| Wisdom | **drops** the Old Latin plus at 6:1, so ch. 6 has 25 verses against the Clementine's 27 | explains the +1 verified in §6.1 |
| Wisdom 17 | 20 verses against the Greek/NABRE's 21 | **NV and NAB disagree**; a Wisdom 17 citation needs its system named |
| **Sirach** | **keeps the long Latin versification** — ch. 1 has 40 verses, ch. 3 has 34, as the Vulgate does | see §7.3; this materially changes the Sirach diagnosis |
| Psalm 151, Prayer of Manasses, 3-4 Esdras | **absent** — the NV appendix carries only Tridentine decrees | nothing to map |

The Nova Vulgata's *Praenotanda* explains the Sirach decision: the commission
took the Latin version "quasi normam" because no surviving Greek, Hebrew or
Syriac witness descends directly from the original **[sourced]**.

### How far automatic derivation gets

**[verified]** aligning Douay and King James verse text by normalized
sequence similarity, per chapter:

| Chapter | True relation | Recovered? |
|---|---|---|
| Mark 9 | KJV = Douay + 1 throughout | Yes — 47 of 49 verses agree on offset +1, no low-confidence rows |
| Acts 14 | offset 0 to v. 17, +1 from v. 18 | Yes — the seam is found (6 rows at 0, 20 at +1) |
| Sirach 3 | Latin expansions, offset drifts −1 to −3 | **Partly** — 11 of 34 verses low-confidence |
| Hosea 2 | offset 0; both follow the Vulgate division | Yes, and correctly — the Lectionary's +2 is a *third* system neither witnesses |

Alignment is reliable where two editions render the same underlying text and
unreliable exactly where the traditions carry different text. That is the shape
of a **candidate generator**, not an oracle. **Derive the obligation, record
the answer, validate the pairing.**

---

## 6. What acquisition actually buys — measured

The published Family A data is not a general solution, but it is a specific and
large one, and it can be checked against the tracked editions before it is
trusted. I fetched `vul.json`, `lxx.json`, `org.json` and `eng.json` from
Copenhagen's `standard-mappings/` and measured them **[verified]**.

### 6.1 It covers most of the unsolved cases, and agrees with independent derivation

`vul.json` holds 475 `mappedVerses` rows mapping Vulgate → `org`. Against the
project's open list:

| Open case | `vul.json` row | Agrees with my independent check of the tracked text? |
|---|---|---|
| Joel | `JOL 2:28-32 → JOL 3:1-5`, `JOL 3:1-21 → JOL 4:1-21` | yes — identical to the hand-written `citation_divergences` |
| Malachi | `MAL 4:1-6 → MAL 3:19-24` | yes, identical |
| Isaiah 9 | `ISA 9:1 → ISA 8:23`, `ISA 9:2-21 → ISA 9:1-20` | yes, identical |
| Isaiah 64 | `ISA 64:1 → ISA 63:19`, `ISA 64:2-12 → ISA 64:1-11` | yes, identical |
| Micah 5 | `MIC 5:1 → MIC 4:14` | yes, identical |
| **Exodus 22** | `EXO 22:1 → EXO 21:37` | **yes** — matches the +1 shift I verified |
| **Hosea 2** | `HOS 2:1-22 → HOS 2:3-24` | **yes** — the +2 shift I verified |
| **Wisdom 6** | `WIS 6:2-21 → WIS 6:1-20` | **yes** — the +1 shift I verified |
| **Mark 9** | `MRK 8:39 → MRK 9:1`, `MRK 9:1-49 → MRK 9:2-50` | **yes** — the −1 shift I verified |
| **John 6** | `JHN 6:51 → 6:51`, `JHN 6:52 → 6:51`, `JHN 6:53-72 → 6:52-71` | **yes** — the merge I verified |
| **Acts 14** | `ACT 14:6 → 14:7`, `ACT 14:7-27 → 14:8-28` | **yes** |
| **Acts 7:60** (clamped) | `ACT 7:55 → 7:56`, `ACT 7:56-59 → 7:57-60` | resolves the clamp |
| **Mark 4:41** (clamped) | `MRK 4:40 → MRK 4:41` | resolves the clamp |
| Daniel additions | 22 rows, e.g. `DAG 3:24-52 → S3Y 1:1-29` | book-level routing, as the KJV index already does |
| **Sirach** | **0 rows** | not covered |
| **Esther** | **0 rows** | not covered |
| Tobit, Judith | 0 rows | not covered |
| 1 Thessalonians 4 | 0 rows | not covered |

Two independent derivations — mine from the tracked text, theirs from the
manuscript tradition — agree on every case both cover. That is the strongest
confirmation available without a Nova Vulgata witness.

### 6.2 It describes the Clementine almost exactly, which sizes the departure table

**[verified]** comparing `vul.json`'s `maxVerses` against each edition's actual
printed chapters:

| Edition | Chapters agreeing | Differing | Uncovered |
|---|---|---|---|
| Clementine Vulgate | **1311** | **7** | 16 |
| Douay-Rheims | 1298 | 20 | 16 |

The Clementine's seven departures are `2 Corinthians 1`, `3 John 1`,
`Daniel 14`, `Genesis 5`, `John 11`, `Psalm 115`, `Psalm 147`. **That is the
edition's entire departure table, derived, seven rows.**

And it settles a decision that would otherwise be taste: **`vul.json` numbers
Psalm 115 to verse 19 and Psalm 147 to verse 20** — the Douay's convention, the
one `psalm-numbering.tsv` already records. So the psalm concordance describes
the `vulgate` *system* correctly, and the **Clementine is the edition that
departs**. §1.1 is a missing departure table, not a wrong concordance.

### 6.3 It is not clean, which is why load-time validation is not optional

**[verified]** parsing all 475 `vul.json` rows: **one malformed row**,
`DAG 3:52-23 → S3Y 1:30-31`, whose left range ends before it begins. Also
**[verified]** `lxx.json`'s `partialVerses` carries values like `['-', 'a ']`
with a trailing space. And `vul.json` sets `excludedVerses` and
`partialVerses` to empty, so it **cannot express text the Vulgate has and the
original does not** — the exact thing Sirach needs.

Combined with UBS's own admission that the mapping sections were never
validated **[sourced]**, the rule is: **ingest, validate against the tracked
inventories, and refuse to load on any failure.** The 1298/1311 agreement
figures above *are* that validation, run once by hand.

### 6.4 Rights — a decision required before ingest

**[verified]** by fetching `LICENSE.md`:

| Source | Data licence | Compatible with this project's CC BY 4.0 content grant? |
|---|---|---|
| Copenhagen Alliance mappings | **CC BY-SA 4.0** | **ShareAlike** — a derived tracked artifact carries a copyleft obligation the project's plain CC BY 4.0 does not |
| STEPBible TVTMS | **CC BY 4.0** **[sourced]** | yes |

This is a real constraint, not a formality. The project's `LICENSE` places
project-created content under CC BY 4.0 and `guidance/sources.md` requires the
rights basis to be recorded per artifact. Three honest options, in order of
preference:

1. **Prefer TVTMS as the source of record** (CC BY 4.0), and use Copenhagen's
   `vul.json` as an independent cross-check that is measured but not
   redistributed. This is the recommendation.
2. Track the Copenhagen-derived table as a separately-licensed artifact with
   its own CC BY-SA notice, as `THIRD_PARTY.md` already does for other
   material.
3. Treat the numbering correspondences as uncopyrightable facts. Defensible,
   but it is an argument rather than a record, and this project's house style
   is to record rather than argue.

Whichever is chosen, record it. Do not ingest first and decide later.

---

## 7. The hard cases

For each: does a numeric mapping suffice, or is the difference structural?

### 7.1 Esther

**[verified]** in the tracked editions:

| Edition | Chapters | Chapter 10 | Additions |
|---|---|---|---|
| Douay-Rheims | 1-16 | 13 verses | integrated as 10:4-16:24 |
| Clementine | 1-16 | 13 verses | integrated as 10:4-16:24 |
| King James | 1-10 | 3 verses | separate book `EsthGr`, chapters 10-16, **carrying the Vulgate's own numbers** |

**Structural.** Three things differ at once: number of books, number of
chapters, and — at the seam — the number of verses inside a shared chapter
number. No verse map expresses "this text is in a different book here."
Neither `vul.json` nor `lxx.json` has a single Esther row **[verified]**;
JSword's `Catholic2.properties` needs an unmappable `Esth.15.1-Esth.15.3=?`
**[sourced]**.

The live citation makes the point. **[verified]** The postconciliar entrance
antiphon for the Twenty-seventh Sunday in Ordinary Time, incipit *In voluntate
tua, Domine*, is cited `Esther 4:17`. Clementine Esther **13:9** reads *Domine,
Domine rex omnipotens, in ditione enim tua cuncta sunt posita, et non est qui
possit tuæ resistere voluntati*. The Douay's own Esther 4:17 reads *So Mardochai
went, and did all that Esther had commanded him* — a real verse, entirely the
wrong words, returned today without complaint.

The citation is also **ambiguous in its own system**. The standard concordance
between the letter numbering and the Vulgate's, from NRSVA editorial footnotes
**[sourced]**:

| Addition | Letters | Vulgate | Narrative position |
|---|---|---|---|
| A | A 1-17 | 11:2-12 + 12:1-6 | before 1:1 |
| B | B 1-7 | 13:1-7 | after 3:13 |
| C | C 1-30 | 13:8-18 + 14:1-19 | after 4:17 |
| D | D 1-16 | 15:1-16 | replaces Hebrew 5:1-2 |
| E | E 1-24 | 16:1-24 | after 8:12 |
| F | F 1-11 | 10:4-13 + 11:1 | after 10:3 |

Addition C — which is what the antiphon quotes — spans **two Vulgate chapters
and two distinct prayers**, Mordecai's (13:8-18) and Esther's (14:1-19). The
Nova Vulgata addresses them as lettered sub-verses hanging off 4:17, so a bare
`Esther 4:17` names neither. Only the incipit settles it, and *In voluntate
tua* is Mordecai's. **Requires a human decision**; refuse until it gets one.

Two parser requirements for the Nova Vulgata's sub-verse letters **[sourced,
and flagged by the researcher as needing confirmation against the printed
edition]**: the sequence **skips `j`** (…17i, 17k…), and it **doubles past
`z`** (8:12a-12cc). Note also that the Vulgate's *numeric* order is not the
*narrative* order — F precedes A in the appendix — so book-level redirection
must not assume that ascending Vulgate numbers mean ascending narrative
position.

The King James's handling is the model: the additions are a distinct book token
carrying *the Vulgate's* numbers, so a Vulgate citation of Esther 13:9 routes
to `EsthGr 13:9` by **book-level redirection**, with no arithmetic.

### 7.2 Daniel

**[verified]**:

| Edition | Daniel | ch. 3 | ch. 4 | Additions |
|---|---|---|---|---|
| Douay / Clementine | 1-14 | 100 verses | 34 verses | integrated (3:24-90, 13, 14) |
| King James | 1-12 | 30 verses | 37 verses | separate `SgThree` (68 vv.), `Sus` (64), `Bel` (42) |

**Mixed**, and instructive because it needs both mechanisms at once.

- **Susanna and Bel are pure chapter relabelling** — Daniel 13 ↔ `Sus` 1-64,
  Daniel 14 ↔ `Bel` 1-42, verse for verse **[verified]** from the tracked verse
  counts. A numeric map expresses these completely.
- **The Song of the Three does not relabel.** `SgThree` runs 1-68 against
  Vulgate Daniel 3:24-90, which is 67 verses. **[sourced]** the endpoints are
  offset differently — NRSV Prayer of Azariah v. 1 = Nova Vulgata Daniel 3:24
  (+23) while v. 68 = Daniel 3:90 (+22) — so at least one verse boundary
  differs somewhere inside the block, and the exact split point was not
  established. **Sixty-eight verses onto sixty-seven needs an alignment table,
  not a formula.** The tracked King James book index says exactly this and
  refuses rather than asserting an offset — the right call, implemented by the
  existing `not-in-this-edition` alias rows.

Useful for the Song of the Three when someone does compile it: the Nova Vulgata
prints the Aramaic verse number alongside its own, so NV 3:91 carries a
secondary `24` marking MT 3:24 **[sourced]**. That is a published crib for the
seam at the far end of the block.

Note also **Daniel 4: 34 verses in the Latin against 37 in the King James**
**[verified]** — not an addition but the chapter 3/4 boundary, which the
Aramaic and the Greek place differently. **Both mechanisms are required in one
book.**

### 7.3 Sirach

The messiest, and the one that decides the architecture.

**[verified]** 48 of 51 chapters differ in verse count between the tracked
Latin and Greek witnesses. Spot checks against the postconciliar citations:

| US Lectionary (NAB) cites | Text meant | Vulgate/Douay locus | Offset |
|---|---|---|---|
| Sirach 3:2 | *God hath made the father honourable to the children* | 3:3 | +1 |
| Sirach 3:17 | *My son, go on with thy business in meekness* | 3:19 | +2 |
| Sirach 27:30 | *Malice and wrath, even these are abominations* | 27:33 | +3 |
| Sirach 28:1 | *He that seeketh to revenge himself* | 28:1 | 0 |

**The offset changes three times inside chapter 3 and resets at the chapter
boundary.** A per-chapter offset is provably insufficient; only segment-level
rows can carry it.

And there are **three arrangements in play**, not two. **[verified]** King
James Sirach 35:12 reads *Do not think to corrupt with gifts; for such he will
not receive*, which is Douay 35:14 — offset +2. The postconciliar
`Sirach 35:12-14, 16-18` means *The Lord is a God of justice, who knows no
favourites… the prayer of the lowly pierces the clouds*, which is **neither**.

The three, correctly named:

| Arrangement | Followed by | Character |
|---|---|---|
| **Long Latin** | Vulgate, Douay, **and the Nova Vulgata** (§5) | Gr II expansions throughout; ch. 1 has 40 verses |
| **Corrected Greek** | Ziegler, NRSV, and the tracked King James | 30 verses in ch. 1; chapter order as the Hebrew/Latin/Syriac have it |
| **NAB** | the US *Lectionary for Mass* | Greek text, its own verse numbers |

**This corrects a natural but wrong diagnosis.** Because the Nova Vulgata keeps
the *long Latin* Sirach, the postconciliar Sirach problem is **not**
Vulgate-versus-Nova-Vulgata at all — those two agree. It is **NAB versus
everything else**, which is exactly what *Liturgiam authenticam* §37 permits.
The concrete case **[sourced]**: the Holy Family first reading is
`Sir 3:2-6, 12-14` in the US Lectionary and `Sir 3:3-7, 14-17a` in the *Ordo
Lectionum Missae*. The +1 at the head of chapter 3 in that pair is exactly the
offset verified above against the tracked Douay.

**The displacement is an acquisition hazard rather than a present bug.**
Every extant Greek manuscript of Sirach reverses the order of **30:25-33:13a**
and **33:13b-36:16a** — a transposed leaf in the archetype. The correct order
survives in the Hebrew, the Old Latin/Vulgate and the Syriac. Ziegler restored
it; Rahlfs numbers the Greek in manuscript sequence, so the two blocks **swap
their number ranges**, shifting chapter numbers by ±3 in opposite directions
**[sourced]**, NETS introduction to Sirach (Benjamin G. Wright),
<https://ccat.sas.upenn.edu/nets/edition/30-sirach-nets.pdf>.

**[verified]** the tracked King James Apocrypha is in the **corrected** order:
its 33:16 reads *I awaked up last of all, as one that gathereth after the
grapegatherers*, matching Douay 33:16, and its 30:25 matches NETS 30:25. So
**the displacement does not affect any edition this repository holds** — but it
would affect a Rahlfs-derived `lxx` scheme, in which that same sentence is
numbered **30:25**. Acquiring an LXX scheme without checking which Sirach order
it follows would silently corrupt Sirach 30-36. Add it to the ingest gate.

**Verdict: segment-level numeric mapping is sufficient in *form*, must be
compiled per system pair, and will be largely `absent` rows in both
directions.** Both published datasets decline Sirach outright, for the reason
quoted in §4(a). This is where the project is on its own.

### 7.4 3 and 4 Esdras

**[verified]** The postconciliar calendar cites `4 Esdras 2:36-37` (entrance
antiphon *Accipite iucunditatem gloriae vestrae*). Neither Vulgate edition
carries it — the Clementine prints 3-4 Esdras in an appendix the tracked
artifact does not include — so it appears today as `no book named '4 Esdras' in
this edition`. **This is correct behaviour.**

The incoming King James supplies it: token `2Esdras`, chapters 1-16, with
`4 Esdras` registered as an alternate name, and 2:36 reading *Flee the shadow
of this world, receive the joyfulness of your glory* **[verified]**.

**Structural at the naming level** — once the book is identified the verse
numbers agree. The King James book index documents the trap: Douay "1 Esdras"
is Ezra (`1Esd`) while KJV "1 Esdras" is the Greek Esdras (`1Esdras`). **Book
identity must be resolved per edition, never through a shared alias table.**
`load_books` already does this; add a gate that no alias is claimed by two
tokens. Note also that Greek Esdras is not a renaming of Ezra: it reorders its
material and contains the Tale of the Three Guardsmen at 3:1-4:42, which has no
counterpart in Ezra-Nehemiah at all **[sourced]**.

**And 4 Ezra supplies the precedent case for a hazard nothing else in this
document covers: the same citation string valid in two schemes, with no
textual overlap.** Codex Sangermanensis I (822) lost a leaf, and almost every
later Latin manuscript descends from it, so roughly seventy verses were absent
from the Western tradition until Bensly recovered them from the Amiens
manuscript in 1875 **[sourced]**, *The Missing Fragment of the Latin
Translation of the Fourth Book of Ezra* (Cambridge, 1875). The restored block
became **7:36-105**, and what had been numbered 7:36-70 became **7:106-140**.
A citation of `4 Ezra 7:40` means entirely different text before and after
1875, at a flat offset of +70.

The lesson generalizes past this book: **a system identifier must be specific
enough to distinguish two states of the same tradition.** `vulgate` is not
sufficient where the Douay and the Clementine disagree (§7.7); nor is a bare
`greek` where Rahlfs and Ziegler disagree (§7.3). Where an edition date or
recension is what actually decides, the system name must carry it.

### 7.5 Prayer of Manasses

**[verified]** Present only in the King James (`PrMan`, 15 verses); absent from
both Vulgate editions; cited by neither calendar. No mapping required; a
book-presence declaration suffices.

### 7.6 Psalm 151

**[verified]** Absent from all three tracked editions — each carries exactly
150 psalms — and **[sourced]** absent from the Nova Vulgata, whose psalter also
ends at 150. Nothing to map and nothing to acquire unless a calendar cites it;
refusal by book identity already works.

Worth recording so nobody later treats it as a numbering problem: the Greek
Psalm 151 is itself a **conflation of two distinct Hebrew compositions**, 151A
and 151B, both preserved in 11QPsa **[sourced]**. Its LXX superscription marks
it *ἔξωθεν τοῦ ἀριθμοῦ*, "outside the number" — the tradition's own statement
that it is not part of the numbered sequence.

### 7.7 Verses one edition merges and another splits

The case a chapter-offset model cannot represent, occurring *within* the
Vulgate tradition.

**[verified]** 1 Thessalonians 4. The Douay ends at verse 17, the Clementine at
18. Douay 4:17 (*Wherefore, comfort ye one another with these words*) is
Clementine 4:18 (*Itaque consolamini invicem in verbis istis*), and the offset
begins at 4:14. Two witnesses of the same Vulgate, differing by a merge. No
published dataset covers it **[verified]** — `vul.json` has zero `1TH` rows and
its `maxVerses` gives 18, i.e. the Clementine.

**[verified]** Hosea 6 defeats verse granularity entirely. The Vulgate's 6:3
carries *both* Masoretic 6:2 (*He will revive us after two days*) and Masoretic
6:3 (*We shall know, and we shall follow on*). The two re-align at 6:4. So the
Lectionary's `Hosea 6:3-6` corresponds to no whole number of Vulgate verses:
the smallest containing range is 6:3-6, which **over-includes half a verse**.

Three honest responses, chosen per case rather than silently:

| Response | When | What the consumer sees |
|---|---|---|
| Exact | segments align | the passage |
| Superset, declared | a cited boundary falls mid-verse | the passage plus a note naming the over-inclusion |
| Refuse | no correspondence recorded, or the citation is ambiguous | no text, and the reason |

TVTMS's subverse convention is the right vocabulary if this is ever recorded
precisely: **subverse 0 is the text present in all traditions**, additions being
1..n, so a split is addressable without renumbering downstream **[sourced]**.
The calendar already carries part-verse letters on **118 citations**
**[verified]**, which is enough to write a superset note; it is not enough, and
should not be used, to cut a verse.

### 7.8 Roll-up: which divergences a numeric map can express

| Case | Numeric map sufficient? | Mechanism needed |
|---|---|---|
| Hebrew ↔ Vulgate psalm numbers | **Yes** | piecewise psalm map + per-psalm superscription offset — already built |
| Nova Vulgata vs Vulgate: Joel, Malachi, Isaiah, Micah, Hosea, Exodus | **Yes** | segment rows; acquirable (§6.1) |
| John 6, Mark 9, Acts 14, Acts 7, Mark 4 | **Yes** | segment rows with one split/merge; acquirable |
| Susanna ↔ Daniel 13, Bel ↔ Daniel 14 | **Yes** | pure chapter relabelling |
| Song of the Three ↔ Daniel 3:24-90 | **Almost** | 68 onto 67 — explicit alignment table, no formula |
| Wisdom, Sirach chapter-internal Latin pluses | **No** | different amount of text; segment rows plus `absent-*` |
| Sirach 30-36 displacement | **No** | different text order; block swap, and only if a Rahlfs-derived scheme is ingested |
| Esther additions | **No** | different text, different order, three addressing schemes; book-level redirection |
| 1/2/3/4 Esdras | **No** | book-identity resolution per edition |
| 4 Ezra 7:36-105 | **Yes, but** | flat +70, and the same citation string is valid in both schemes — an edition discriminator is mandatory |
| Prayer of Manasses, Psalm 151 | **No** | presence and placement, not numbering |
| Douay vs Clementine merges (1 Thess 4, Hosea 6) | **Partly** | edition departure rows; mid-verse cases refuse or declare a superset |

---

## 8. Proposal

Four artifacts and six gates. Each is derived from tracked data or validated
against it on load; none is a hand-typed table that nothing checks.

### 8.1 `verse-inventory.tsv` — per edition, fully derived

One row per chapter, generated from the same `verse-text-*` artifacts the index
is built from, written beside them, tracked.

```
token	chapter	first_verse	last_verse	verse_count	gaps
Ps	115	10	19	10
Ps	147	12	20	9
1Thess	4	1	17	17
```

- **Derived** by a `build` verb, as the chapter fragments already are.
- **Checked** by the existing `check` verb, failing on stale, missing or
  orphaned rows exactly as fragments do.
- Replaces the runtime `self.chapters` computation, so a chapter's ceiling
  becomes **a tracked fact a diff shows** rather than an inference nothing
  records.

This alone would have surfaced the Psalm 115 conflict as a two-line diff. It is
also the pattern `biblelib` uses for `vref` files — generate, commit, assert
byte-identity in a test **[sourced]**.

It further lets `book-index.tsv` be validated: `chapters` and `verses` must
equal the inventory's totals. Give the book index a declared schema, make the
editions' columns agree, and gate them.

### 8.2 `numbering-concordance.tsv` — per system pair

The generalization of `psalm-numbering.tsv`, keyed by **system**, not edition.
Header carries `left_system` and `right_system` once.

```
book	left_chapter	left_verses	right_chapter	right_verses	relation	note
Joel	3	1-5	2	28-32	one-to-one
Malachi	3	19-24	4	1-6	one-to-one
Isaiah	8	23	9	1	one-to-one
Hosea	2	1-22	2	3-24	one-to-one
John	6	51	6	51-52	split-right
Hosea	6	2-3	6	3	merged-right	the Vulgate carries both in one verse
Sirach	3	19	—	—	absent-right	no Vulgate counterpart
Sirach	30-36	—	—	—	not-recorded	arrangements differ; see §7.3
```

| Relation | Meaning | Resolution behaviour |
|---|---|---|
| `one-to-one` | equal-length runs, verse for verse | convert |
| `split-right` / `split-left` | one verse becomes several | convert a whole-verse citation; note the widening |
| `merged-right` / `merged-left` | several become one | convert to the containing verse and **declare the superset** |
| `absent-right` / `absent-left` | text present in one tradition only | **refuse**, with the reason |
| `not-recorded` | known to diverge here; no correspondence established | **refuse**, with the reason |

`not-recorded` is the load-bearing addition, and the thing SWORD's binary
format provably cannot say. It differs from *no row* (unknown — also a refusal,
but a silent gap) because it is a positive, reviewable statement that someone
looked and found no clean correspondence. `_psalms.py` already has the idea as
`english_offset_uniform: no`, and the King James `verse-aliases` as
`numbering-not-recorded`; make it first-class.

**Validation on load** — refuse to load the table, rather than converting
anything, if:

1. a `one-to-one` row's two sides differ in length;
2. rows for a book overlap or leave a gap in either system's extents;
3. a `split`/`merged` row's counterpart is not the stated cardinality;
4. an `absent-*` row has a non-empty counterpart;
5. any range ends before it begins, or names a chapter outside the system's
   extents;
6. a book appears in the table but in neither system's extents.

Rule 5 is not theoretical. **[verified]** the published `vul.json` contains
`DAG 3:52-23`.

### 8.3 System extents

Gap and overlap checks need per-system chapter lengths. For systems the library
witnesses, that comes from an edition's inventory. For systems it does not
(`nova-vulgata`, `nab-lectionary`), extents must be acquired as a **scheme
file** — a book/chapter/verse-count table and nothing else, carrying no
scripture text and so raising no textual-rights question. Copenhagen's
`maxVerses` is exactly this shape and is measured against the tracked editions
in §6.2.

An edition declares `numbering: <system>` and records its departures in its own
`verse-aliases`. **[verified]** the Clementine's departure table is seven rows;
the Douay's is twenty. Following OSIS's advice **[sourced]**, these are
departures, **not** new systems — the differences are slight, mechanically
resolvable, and inventing a system per edition would multiply the maintenance
surface for nothing.

### 8.4 Citations declare a system, not a target

Replace `citation_divergences`' resolved targets with a per-citation system
declaration, the file-level `psalm_numbering` becoming a **default** rather
than a claim:

```yaml
- book: Esther
  ranges:
  - begin: {chapter: 4, verse: 17}
    end: {chapter: 4, verse: 17}
  ref: Esther 4:17
  numbering: nova-vulgata      # new
```

Why this shape:

- **One declaration serves every edition.** The 1 Thessalonians case, where the
  Douay and Clementine need different targets, stops being expressible in the
  calendar — as it should be, being a fact about editions.
- **It is what a human actually knows.** The John 6 audit produces "this
  antiphon speaks Vulgate, that reading speaks Greek", not a target reference.
- **It is checkable.** A citation declaring `vulgate` whose locus lies outside
  the `vulgate` extents is a contradiction the loader catches. A resolved
  target can be checked against nothing but the one edition it was written for.
- **It shrinks the hand-written surface** from *editions × citations* answers
  to *citations* one-word declarations plus one concordance per pair.

Keep the existing `Divergences` upkeep discipline verbatim: a declaration for a
citation the calendar no longer makes must fail the build, and a declared
divergence nothing cites must fail too. That machinery has already caught real
drift.

### 8.5 Resolution and the refusal contract

```
citation (book, ranges, system)
  → book identity, per edition, from the edition's own book index
      ↳ no such book, or a redirect (Esther additions → EsthGr)  → route or refuse
  → strip part-verse letters before cross-edition matching        [OSIS rule]
  → system == edition's system?
      no → concordance lookup, direct pair only (no composition unless proved)
             ↳ no row                    → REFUSE "no correspondence recorded"
             ↳ not-recorded / absent-*   → REFUSE with the recorded reason
             ↳ merged                    → convert, attach a superset note
  → edition departure table (verse-aliases)
      ↳ merged-verse        → follow
      ↳ not-in-this-edition → REFUSE
  → inventory bounds check
      ↳ verse < first or verse > last → REFUSE, naming both ceilings
  → fetch text
```

Non-negotiable rules:

1. **Never clamp.** Remove `min(high, bound)`. A range naming a verse past the
   chapter's end is an error unless an alias resolves it. The message must name
   the cited verse, the edition's last verse, **and the edition** — because
   `1 Thessalonians 4:18` is an error against the Douay and correct against the
   Clementine, and a message that omits the edition sends someone to the wrong
   file.
2. **Never compose mappings** unless both hops are proved one-to-one across the
   segment in question.
3. **Refuse on ambiguity, including ambiguity inside one system.**
   `Esther 4:17` in Nova Vulgata numbering names two distinct prayers.
4. **A superset is not a hit.** Return it with a machine-readable note, never
   as an exact match.
5. **Type the failures.** Following MyCapytain **[sourced]**, distinguish at
   minimum: *unparseable reference*; *book not in this edition*; *locus outside
   this edition's chapter*; *no correspondence recorded between the two
   systems*; *correspondence exists but is inexact*; *citation ambiguous in its
   own system*. These mean different things to whoever fixes them, and
   collapsing them into one `unresolved` string costs real time.
6. **Refusals are data.** Carry the reason through to
   `<out>/propers/<calendar>.json`'s `unresolved`, as `mass-propers` already
   does, so a page explains itself.

### 8.6 Gates

| Gate | Fails when |
|---|---|
| inventory staleness | a tracked `verse-inventory.tsv` row differs from a fresh derivation, is missing, or is orphaned |
| book-index schema | the editions' book indexes disagree on columns, a declared count differs from the inventory, or an alias is claimed by two tokens |
| concordance integrity | any of the six load-time checks in §8.2 |
| ingest validation | an acquired scheme's `maxVerses` disagrees with a tracked edition's inventory outside that edition's declared departure table |
| divergence-register upkeep | a cross-edition verse-set difference has no explaining row, **or** an explaining row whose difference no longer exists |
| refusal-register upkeep | a recorded refusal that has stopped being needed (the existing `psalm_numbering_exceptions` self-cleaning behaviour, generalized) |

The fifth would have caught §1.1 the day the Clementine was added: the derived
diff produces the obligation and the build stays red until someone explains it.

### 8.7 Tooling

Per `tmt.json` and the repository's tool-making rule, this extends existing
tools rather than adding a program:

- `index-bible inventory` — new verb; writes and checks `verse-inventory.tsv`.
- `index-bible divergences` — new verb; emits the cross-edition candidate diff
  the upkeep gate consumes.
- `scripts/_versification.py` — generalizes `scripts/_psalms.py`; the psalm
  module becomes a thin caller so the psalter keeps its verified behaviour.
- `citations check` — extended to validate per-citation `numbering`.

Do not scaffold a new registry tool until two derivations recur; `tmt note` the
candidates as they appear.

---

## 9. Acquire, derive, decide

### 9.1 Acquire (numbering data, not text)

| Item | Buys | Rights |
|---|---|---|
| A Vulgate↔`org` mapping — TVTMS preferred, Copenhagen `vul.json` measured in §6 | 13 of the open cases, including Exodus 22, Hosea 2, Wisdom 6, Mark 9, John 6, Acts 14, and two of the clamps | TVTMS CC BY 4.0; Copenhagen CC BY-SA 4.0 — see §6.4 |
| `org` / `lxx` extents | system bounds for gap and overlap checks | as above |
| Nova Vulgata extents | the one system with no witness and no full published mapping. Note it agrees with the Vulgate on Sirach and with the NAB on Hosea and Wisdom 6 (§5) | numbering only |
| NAB / US Lectionary extents | *Liturgiam authenticam* §37 makes the Lectionary's numbering free to differ, and it does — Sirach throughout, Wisdom 17 | numbering only |

**Validate on ingest against the tracked inventories before trusting anything.**
§6.2's 1311/1318 and 1298/1318 figures are that validation performed once; make
it a gate.

**Two specific ingest checks that a generic gate would miss:**

1. **Which Sirach order does an acquired `lxx` scheme follow?** Rahlfs's
   displaced order and Ziegler's corrected order differ by a ±3-chapter block
   swap across 30:25-36:16 (§7.3). Test it on one verse — `Sirach 33:16` should
   be the gleaner-after-the-grape-pickers, as it is in every tracked edition
   **[verified]**. If it is not, the scheme is Rahlfs-ordered and Sirach 30-36
   must be rejected rather than mapped.
2. **Does the scheme claim to describe an edition or to superset several?**
   SWORD's `Vulg` header says outright that it supersets "myriad editions"
   and expects empty verses **[sourced]**. A superset scheme is fine as a
   *system* definition and wrong as an *inventory*; never let one populate the
   other.

### 9.2 Derive from what is tracked

| Derivation | Output |
|---|---|
| Per-edition inventory | every chapter's first/last verse, all editions, complete |
| Cross-edition verse-set diff | 17 Douay/Clementine rows, 298 Douay/King James rows — the obligation list |
| Text alignment on the diffed chapters | candidate offsets; reliable in the protocanon, unreliable in the deuterocanon (§5) |
| Departure tables | 7 rows for the Clementine, 20 for the Douay, against `vul` (§6.2) |
| Book-level structural routing | already present in the King James book index; generalize the relation |
| Incipit matching for antiphons | narrows which system an antiphon speaks; does not always settle it |

### 9.3 Requires a human decision

1. **Which system each ambiguous citation speaks** — the John 6 group, the
   eleven psalm antiphons, the Sirach and Wisdom group. Per slot, against the
   printed incipit and where necessary the full antiphon text.
2. **Whether an antiphon's number moves or the calendar's declaration moves** —
   already scoped as TASK-32; this proposal does not pre-empt it.
3. **Esther 4:17** — Mordecai's prayer or Esther's.
4. **Every deuterocanonical `absent-*` row.** Deciding a Vulgate verse has no
   Greek counterpart is a textual judgement, not a diff.
5. **Whether a superset is acceptable** for each mid-verse boundary.
6. **The rights basis for the acquired mapping** (§6.4).

§6.2 removes one item that would otherwise be here: which printing of the
Vulgate psalter is normative. The published `vul` system numbers Psalm 115 to
19 and 147 to 20, matching `psalm-numbering.tsv`, so the Clementine is the
departing edition.

---

## 10. Work estimate

In dependency order. "Sessions" means focused working sessions.

| # | Work | Size | Blocked by |
|---|---|---|---|
| 1 | `verse-inventory` artifact, build + check verbs, book-index schema unification and gate | 1-2 | nothing |
| 2 | Remove the clamp; refuse with an edition-naming message; typed failures; add the missing alias rows for the 4 Douay clamps and the 13 unrecorded Douay/Clementine differences | 1 | 1 |
| 3 | Cross-edition divergence register and upkeep gate (17 rows; the 298 King James rows as a second pass) | 1-2 | 1 |
| 4 | `_versification.py`: system model, concordance loader, six integrity checks, refusal vocabulary; `_psalms.py` reduced to a caller | 2-3 | nothing |
| 5 | Settle the rights basis and ingest the Vulgate↔`org` mapping with the §8.6 ingest gate | **1-2**, was estimated at 3-5 before §6 measured the data | 4 |
| 6 | Per-citation `numbering` declaration; migrate the four existing `citation_divergences` books | 1-2 | 4, 5 |
| 7 | Settle the ~23 known wrong resolutions and the 11 psalm antiphons, per slot, against incipits | **2-4, mostly judgement** | 5, 6 |
| 8 | Nova Vulgata and NAB extents; Sirach, Wisdom 17 and Esther concordance rows | **3-6, partly open-ended** | 5 |

Items 1-4 are mechanical, independent of any acquisition, and convert silent
wrongness into loud refusal — already most of the value. Item 5 is materially
cheaper than it looked before §6: the data exists, matches independent
derivation on every case both cover, and validates at 99.5% against the
Clementine. Item 8 has no firm bottom; the right discipline is to record
`not-recorded` rows and move on rather than chase completeness.

Two scoping notes that came out of the research and cut item 8 down:

- **Sirach needs a NAB↔Latin mapping only, not a Nova-Vulgata↔Latin one.** The
  Nova Vulgata keeps the long Latin versification (§5), so a citation carrying
  *Ordo Lectionum* numbering resolves against the tracked Vulgate editions with
  no mapping at all. Only the US Lectionary's NAB numbers need one. The first
  useful move is therefore to establish, per Sirach citation, which of the two
  it is — which is §9.3 item 1, not a concordance task.
- **Esther needs no arithmetic once the book is identified.** The King James
  already carries the additions under `EsthGr` with the Vulgate's own numbers
  **[verified]**, so a Vulgate-numbered citation routes by book redirection.
  What is missing is the Nova-Vulgata-to-Vulgate direction — the letter table
  in §7.1 — and that is six rows, not a concordance.

---

## 11. What indexing cannot solve

1. **Sirach, Esther and Daniel are different texts in the two traditions, not
   different numberings of one text.** For a Latin expansion there is no Greek
   verse to name. **[verified]** 48 of Sirach's 51 chapters; and the publishers
   of the mapping data decline these books for exactly this reason (§4a).
2. **Mid-verse boundaries.** Where one edition's verse spans parts of two of
   another's, no verse-granular map is exact. Superset-with-a-note or refusal;
   never a silent exact-looking answer.
3. **Citations whose system cannot be determined.** `John 6:56` with the incipit
   *Qui manducat meam carnem et bibit meum sanguinem* matches two Clementine
   verses. The machine cannot choose. Neither should it.
4. **The Mass chants.** Already documented in `src/sources/bibles/README.md`:
   the 1962 chant texts predate the Gallican psalter and frequently disagree
   with it — *protéctor salutárium* against the Clementine's *protector
   salvationum*. No versification work touches this; it needs a corpus of the
   sung text.
5. **Text the library does not hold.** Psalm 151 is in no tracked edition
   **[verified]**. Refusal by book identity is the whole answer.
6. **The divergence is not a defect anyone intends to fix.** *Liturgiam
   authenticam* §37 binds a liturgical translation to the Nova Vulgata's
   textual tradition and verse *order* while making the verse *numbering*
   "helpful, though not obligatory" **[sourced]**. New approved translations
   are therefore free to renumber, and some will. The resolver must treat a
   citation's numbering system as **permanently variable input**, not as a
   temporary inconsistency awaiting cleanup. That is the strongest argument for
   §8.4: attribution belongs on the citation, because it will keep changing.

The through-line: **a refusal that explains itself is a correct result.** The
existing design already believes this — `unresolved` in the structure files,
the `not-in-this-edition` alias kind, `english_verse` returning a reason rather
than a number. This proposal extends that belief to the rest of the Bible.

---

## 12. Checklist for the implementer

- [ ] `verse-inventory.tsv` derived, tracked, and staleness-gated per edition.
- [ ] `book-index.tsv` given one schema across editions; counts gated against
      the inventory; no alias claimed by two tokens.
- [ ] `min(high, bound)` removed from `Bible.span`; out-of-range refuses with a
      message naming the cited verse, the edition's ceiling, and the edition.
- [ ] Failure taxonomy typed, not a single string (§8.5 rule 5).
- [ ] Cross-edition divergence register derived; every difference either
      explained by an alias row or failing the build; explanations that stop
      applying also fail.
- [ ] `numbering-concordance.tsv` loaded through all six integrity checks;
      `not-recorded` and `absent-*` implemented as refusals, not gaps.
- [ ] Mapping composition forbidden by default.
- [ ] Part-verse letters stripped before cross-edition matching.
- [ ] Acquired scheme validated against tracked inventories on ingest; Sirach
      order and superset-versus-inventory checked (§9.1); rights basis recorded
      in `THIRD_PARTY.md` before ingest, not after.
- [ ] System names specific enough to distinguish two states of one tradition
      (§7.4) — not a bare `vulgate` or `greek`.
- [ ] Per-citation `numbering` declaration added; `citation_divergences`
      migrated; the upkeep gates kept.
- [ ] `scripts/_psalms.py` reduced to a caller of the general module, with its
      existing behaviour unchanged and still tested.
