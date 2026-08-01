# Missals: what to acquire, in what order, and what may be printed

An acquisition audit of the Roman Missal and the Latin uses in communion with
Rome, made on 2026-08-01. Thirty-one books and twelve acts were identified,
their rights settled or explicitly left open, and a retrieval route recorded for
each. Nothing was acquired.

**This document owns no rules.** `act-histories.md` settles that the station is
the act and never the book; `recensions.md` settles the departure model;
`sources.md` settles retrieval, aliases and rights. Those govern. This document
reports what applying them to the missals actually found, and where it found
this repository disagreeing with itself.

The record is `src/sources/inventories/missal-acquisition-audit-v1.toml`. Where
this page and that file differ, the file is right: its counts are derived from
its own tables and this page's are transcribed.

## Evidence conventions

- **[verified]** — read on 2026-08-01 from bytes fetched during the audit: an
  exact PDF, an exact OCR text layer, or a catalogue API queried by URL.
- **[sourced]** — read from an external document cited by URL.
- **[recorded]** — taken from a record already in this repository, cited by path.

Identification never passed through a model. Candidates came from the Internet
Archive advanced-search API and were confirmed against the metadata API, both by
`curl`; where identity mattered, the book's own text layer or PDF was fetched
whole and its title page and colophon read locally. That is what caught the
misidentification in §3.

---

## 1. The finding that cost something: the 1962 decree was never missing

`roman-holy-week-acts-v1.toml` recorded the 1962 typical edition's promulgating
instrument as `act_citation = "not-found"`. `act-histories.md` §7.2 called it
*the tracer's least comfortable result and the one most worth arguing with*, and
§10 set *find or refuse the 1962 promulgating decree* as the second next step.

It is at page 2 of the Vatican typical edition, in the CMAA facsimile **this
repository already had registered**. The audit fetched those 82.8 MB, recomputed
the SHA-256 against the registered value, and read the page [verified]:

> DECRETUM
>
> *Novo rubricarum corpore, a Summo Pontifice Ioanne XXIII, Motu proprio
> « Rubricarum instructum » diei 23 iulii anno 1960 approbato posteroque die a
> Sacra Rituum Congregatione promulgato, vix fieri non potuit quin eadem Sacra
> Rituum Congregatio novam Missalis romani editionem, ad dictum rubricarum
> codicem plane accommodatam, pararet.*
>
> … *hinc est quod praesens Vaticana Missalis romani editio uti « typica »
> declaratur* …
>
> *Romae, ex aedibus Sacrae Rituum Congregationis, die 23 iunii 1962.*
> A. M. Card. Larraona, Praefectus — Henricus Dante, a secretis.

So the incipit *Novo rubricarum corpore* — which `time-machine.md` carried only
from a report, and which `act-histories.md` expressly declined to promote because
naming a document and reading it are different acts — has now been read.

And it was already asserted here. A passage record
`…vatican-typica-1962.decretum-sacrae-rituum-congregationis-1962` states
`verified`, `verified_on = "2026-07-25"` — **six days before the tracer ran**
[recorded].

**Why this happened, which matters more than the decree.** The tracer was not
careless. Its corpus is seven OCR text layers, and its 1962 witness is the
*Benziger* printing, which carries a New York imprimatur and no Vatican decree.
"Only three occurrences of `DECRETUM` in 136,068 lines" is a true statement about
that scan. What was false was writing a corpus-bounded result into a field that
reads as a claim about the repository.

> A bounded negative must look bounded **in the field that records it**, not only
> in the prose beside it. `not-found` cannot carry "not in these seven text
> layers" — and a reader will not supply the qualifier.

This is `the-shape.md` §1 and §2 at once: a reference that resolved successfully
and wrongly, and two copies of one fact in one tree that nothing compared. Both
records have been corrected in place, and the correction box in `act-histories.md`
§7.2 keeps the original reasoning visible rather than erasing it.

## 2. Typical edition, printing, act: a three-way distinction, not two

`act-histories.md` rules that the station is the act and a printing is a witness.
Acquisition needs one more cut, because "witness" flattens two very different
things:

| | what it is | in the record |
| --- | --- | --- |
| **Act** | the instrument: a bull, a decree, an order of a general chapter | a station |
| **Typical edition** | the book an act declared `typica` | a witness, the strongest |
| **Printing** | a commercial edition conformed to a typical one, a lay translation, a critical edition | a witness, weaker |

Every book row in the audit carries `station = false`, and the derived count
`books_that_are_stations = 0` is an assertion under test rather than a tally: if
a later edit ever sets it true, the rule breaks visibly.

The distinction has teeth. Two books in this repository have already been
mistaken for stations — the 1862 Pustet and the 1962 Benziger — and the audit
adds independent corroboration for the first. The 1894 Pustet's approval leaf,
read whole [verified], has the Bishop of Ratisbon reciting that Pustet is the
Apostolic See's and the Congregation of Rites' printer, that a censor examined
the edition, and that the Congregation declared it *plane concordare cum editione
typica ab eadem S. Congregatione publicata*. A printing certified to **conform**
to a typical edition is as clear a statement of witness status as exists.

## 3. Resolve aliases first, or record an absence that is not one

Two rows carry the whole argument.

**The Carthusian missal.** Searching the Internet Archive under `cartusiense`,
`cartusiensis`, `cartusianum` and `chartreux` returns no Carthusian missal
[verified]. Stopping there records the book as unavailable. It is not: four whole
digitisations exist across two libraries, reached by two moves — spelling the
word **both** ways, because `cartusiense` and `carthusiense` return different
result sets, and searching the **French vernacular** *missel chartreux*, which is
the query that actually surfaced the 1517 and 1679 printings.

**The 1570 Missal that is not the 1570 Missal.** A catalogue record gives the
publisher as *apud Ioannem Variscum, & haeredes Bartholomaei Faletti, & socios*
and **no place**. That consortium is the one associated with the Rome first
edition, so a lane stopping at the catalogue records the editio princeps. The
whole text layer was fetched and the colophon read [verified]:

```
YENE TIUS / zipud 3oannem Aarifcum et heredes /
Bartho iFaletti Socios. / zinno $omint. / z MODLSESX.
```

*Venetiis* — Venice, not Rome. A genuine 1570 witness; not the book the station
names. The difference cost one whole-file retrieval and would otherwise have
been invisible.

The audit therefore records, per book, both `aliases_tried` and
`aliases_that_hit`, and — where it matters — `aliases_that_failed`. Some of the
failures are the useful part: `missale dominicanum` returns zero and
`praedicatorum` returns the order's missals; `missale salisbury` returns zero
because the vernacular place name is not in those titles; `norbertine missal`
returns zero.

## 4. The uses have their own acts, and they are cheaper to cite than Rome's

The exempting clause of *Quo primum* creates the parallel line, and the existing
act history draws that fork and then records that it holds no witness for any of
them, calling the branch *honestly empty*.

The audit's structural surprise is that filling it is **easier** than the Roman
line, not harder. These lines are governed by decrees of a general chapter and
orders of a master general, prior general or abbot — and the instrument is very
often printed **on the title page**, in the *iussu editum* clause, so a catalogue
record carries it. Three read without opening a book [verified]:

- **Carthusian 1679** — *ex ordinatione capituli Generalis. Anno Domini
  M.D.CLXXVII. Celebrati sub R. P. D. Innocentio le Masson Priore Cartusiae ac
  totius eiusdem ordinis generali*
- **Carmelite 1621** — *Capituli Generalis decreto … Et reverendissimi prioris
  generalis magistri Sebastiani Fantoni Romani iussu*
- **Dominican 1604** — *Sub r.mo P.F. Hieronymo Xavierre … totius praefati
  Ordinis Generali magistro recognitum & emendatum, & auctoritate Apostolica
  approbatum & confirmatum*

A datable, attributable, citable station, obtained from a catalogue field.

Two further results worth naming. The **Carmelite** claim to the rite of the Holy
Sepulchre is not a modern gloss: the 1574 title page reads *…de Monte Carmelo, ad
normam, et consuetudinem Hierosolymitanae Ecclesiae* [verified]. And the
**Lyonnais** use is the one member of the group with no located witness at all —
seven alias forms, all zero [verified] — which is a bounded negative and a
specific next step, since the Carthusian result proves French libraries hold what
the Internet Archive does not.

## 5. Rights: two thirds readable, fewer than half printable

Twenty-two of thirty-one books are retrievable whole; fourteen may be published
from. The gap is almost entirely the twentieth century, and the rule dividing
them is the 1929 line.

The strongest rights evidence in the audit is not an argument about treaties. It
is the book's own claim, on the leaf after the title page of the 2002 typical
edition [verified]:

> *« Copyright » apud Administrationem Patrimonii Sedis Apostolicae in Civitate
> Vaticana / Venditio operis fit cura Librariae Editricis Vaticanae*

The Holy See asserting copyright in the altar book, in the altar book. That
settles every postconciliar row as **cite-only** without further reasoning.

**Retrieval and publication are separate acts** and the audit keeps them apart
throughout, as `sources.md` requires. A book may be `retrievable = "whole"` and
`may_publish_text = "no"`, and several are. Acquiring the 1970 typical edition's
identity and route is correct; printing a line of it is not.

Three rights positions were left explicitly open rather than resolved:

- **The CMAA 1962 facsimile.** Three hosts serve byte-identical copies —
  82,815,941 bytes each, the first matching the registered SHA-256 [verified] —
  and they carry three different rights labels, one of them a CC BY-NC-ND applied
  at an Internet Archive item. An uploader-applied licence is an assertion by
  whoever filled in the field, not a grant; and no licence on a scan can enlarge
  what may be done with the Holy See's text inside it. The recommendation is that
  `unresolved` **stands**, and that the open question be answered *the licence
  confers nothing* rather than left open.
- **The 1942 Benziger** carries its own US copyright line and no renewal search
  is recorded.
- **The 1936 Premonstratensian** has Internet Archive metadata with no publisher,
  no date field and no copyright statement [verified] — nothing established in
  either direction, which is a different thing from being free.

### A rights conclusion that must not travel

The sibling corpus at `~/git/lt-hist`, which supplied the OCR the act history
reads, imported the 1970 Missal, the 1998 ICEL Sacramentary, the 2002 typical
edition and the 2011 English Roman Missal *under the project public-domain
assumption* — while recording in the same table that *ICEL lists the underlying
Roman Missal translation as copyrighted* [sourced].

That assumption is the opposite of this project's, which marks postconciliar
English `absent: icel` and registers the 2002 artifact `storage = restricted`.
The door between the two repositories is already open — seven text layers have
come through it. **Any future reuse of lt-hist material must re-derive rights
rather than inherit them.**

## 6. What to acquire, in order

Ordered by what each acquisition *settles*, not by chronology and not by what is
easiest to download. Prefer closing a gap the record already admits over opening
a new area; prefer a publishable witness where two would settle the same
question; and do not acquire a book to answer a question no record is asking.
`act-histories.md` ends by warning against enlarging the corpus, and that warning
is still in force — which is why this list is short.

1. **The 1956 *Ordo Hebdomadae Sanctae instauratus*.** The 1955 reform carries 34
   of 42 departures in the existing history, read entirely from the AAS decree
   and missal OCR, never from the reformed rite's own book. Access-restricted at
   the only host found, so the task is finding an open copy. Cite-only.
2. **The 1900 typical edition.** The single `via_unrepresented` edge in the whole
   graph — the one place the record admits crossing a station it does not hold.
   Pre-1930, so publishable, and the 1920 decree naming it as parent has been
   read [verified].
3. **The 1884 instrument, via the 1889 Desclée printing.** Not a scan
   acquisition but a *reading*: the book is already whole and fetchable and its
   title page names Leo XIII's authority. Cheapest gap-closure in the file.
4. **The 1975 *editio typica altera*.** The only postconciliar typical edition
   with no whole witness anywhere — what exists is the Ordo Missae alone, three
   orders of magnitude too small. A 1970-to-2002 diff that skips it will
   misattribute 1975's changes to 2002.
5. **The first use — Braga or Sarum.** Braga 1924 is whole, publishable and
   twentieth-century; Sarum has two whole publishable scholarly editions, one a
   critical edition from three manuscripts. Either converts the empty branch into
   a real one.
6. **The Rome 1570 editio princeps, or an explicit refusal.** The 1570 station
   hangs on a witness this repository's own record calls unchecked, and two
   passes have now failed to find the Rome printing.

**Deliberately not on the list**, because an order that does not say what it
refuses is a wish list: the 1474 Milan missal and the curial missal (the project
takes no position on the pre-Tridentine question); the 1634 edition (two passes
failed in the *same* repository — the next attempt is a different library, which
is research, not acquisition); the 1970, 2002 and 2011 books (identified,
cite-only, nothing gained by holding bytes that may not be printed); and every
modern order missal, whose early printings are whole and publishable while the
modern ones have no established rights basis.

## 7. Traps a later lane will otherwise walk into

- **A partial scan that looks whole.** Dickinson's Sarum missal was published in
  fascicles 1861–1883. One Internet Archive copy has 830 images and another 353
  [verified/reported]; a third is labelled *Part I – Temporale* only [verified].
  Check *which* fascicles a scan holds. This is the Psalm 27 failure waiting in a
  new place.
- **The scan is not the book.** The project's 1962 Benziger text layer carries
  polemical matter inserted ahead of the title page, and the item's uploader
  field confirms the source [verified]. A generator slicing by line window will
  publish it as the Missale Romanum.
- **OCR that is too damaged to search.** The 1894 Pustet returns two lines for a
  whole-file search on `typic` [verified]. Under `act-histories.md` §6 that is a
  negative bound and nothing more.
- **A "1971" nobody listed.** The 2002 edition's printing-history leaf reads
  *Editio typica 1970 / Reimpressio emendata 1971 / Editio typica secunda 1975 /
  Editio typica tertia 2002* [verified]. There is a 1971 emended reprint, exactly
  parallel to the 2008 one this repository already models. A postconciliar
  recension omitting it would be silently wrong about 1971–1975.

## 8. Scope is wider than the brief, and the evidence for that was accidental

Two rows nobody asked for:

- **The Glagolitic Roman Missal** — *Missale Romanum Slavonico idiomate*,
  Vatican Polyglot Press, 1893, in Old Church Slavonic, title set in Glagolitic
  characters [verified]. The Roman rite, officially, in another language and
  another script. Whole and publishable.
- **A Chinese Roman Missal of 1670**, indexed as *Missale Romanum Sinice* in the
  Usuarium database [verified].

Neither is a use exempted by *Quo primum* and neither is a lay translation. Both
are official Roman-rite altar books that a search for Latin titles will never
return — which is direct evidence that "all missals for all churches in communion
with Rome" has members this project has not yet named. **Usuarium**
(`https://usuarium.elte.hu/`, live [verified]) is the right instrument for
finding them, because it is organised by *use*, which no scan repository is.

## 9. The Eastern Catholic books: flagged, not attempted

Deliberately out of scope, and the audit records *why* rather than leaving a
silence someone will fill:

1. **The book is not a missal.** The Eucharistic liturgy in these Churches is not
   carried by one altar book analogous to the Missale Romanum, and the vocabulary
   differs by tradition. A row keyed on `missal` finds nothing and records an
   absence that is an artefact of the query.
2. **The act model differs.** A Roman typical edition is declared *typica* by a
   Roman congregation; Eastern books are promulgated through patriarchal or
   synodal authority together with the Holy See. This audit established **nothing**
   about how those instruments are shaped, dated or published, so applying the
   Roman act vocabulary to them would be an assertion, not a finding.
3. **The languages are not Latin**, and this project's raw-line search is literal.
4. **The count of sui iuris Churches is not stated here**, because it was not
   sourced in this pass. `unrecorded` is the point.

The right first deliverable is not an inventory but a single sourced page fixing
the list of Churches, the principal eucharistic book in each tradition, and the
promulgating authority — and only then a search. **Do not extend the audit file
to cover them.** A Roman-shaped row about an Eastern book is a reference that will
resolve successfully and wrongly.
