# Missals: what to acquire, in what order, and what may be printed

An acquisition audit of the Roman Missal and the Latin uses in communion with
Rome, made on 2026-08-01. Thirty-one books and fourteen acts were identified,
their rights settled or explicitly left open, and a retrieval route recorded for
each. Nothing was acquired.

**Seven corrections are recorded, and three of them are to this audit's own
rows.** That is the most useful thing in the file and §3 is about it.

**This document owns no rules.** `time-machine.md` Rule 1 settles that the
station is the act, and the narrow `printed` exception where a surviving book
declares itself one; `recensions.md` settles the departure model; `sources.md`
settles retrieval, aliases and rights. Those govern. This document
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
instrument as `act_citation = "not-found"`. `act-histories.md` §7.2 kept the node
anyway — a flagged gap a reader can see, rather than a node never drawn — and
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

`time-machine.md` Rule 1 rules that the station is the act and a printing is a
witness. Acquisition needs one more cut, because "witness" flattens two very
different things:

| | what it is | in the record |
| --- | --- | --- |
| **Act** | the instrument: a bull, a decree, an order of a general chapter | a station |
| **Typical edition** | the book an act declared `typica` | a witness, the strongest |
| **Printing** | a commercial edition conformed to a typical one, a lay translation, a critical edition | a witness, weaker |

Every book row in the audit carries `station = false`, and the derived count
`books_that_are_stations = 0` is an assertion under test rather than a tally.
Every book here is held as a witness to an act located elsewhere, so none of
them is a station; a row that ever set it true would have to be a `printed`
station under Rule 1's exception, meeting all four of its conditions, and the
count going non-zero is the prompt to check that it does.

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

### And then the audit made the same mistake three times

The first draft of this file recorded the Lyon missal as `not-located` — *the one
use in the group with no located witness at all* — and the 1500 Cisneros
Mozarabic editio princeps as *not located*, and the Braga promulgating instrument
as `unrecorded`.

All three were wrong. **The Lyon missal is at the Bibliothèque nationale de
France** (1503, 452 views; 1530, 430 views), **so is the Cisneros** (992 views),
all three public domain by Gallica's own records [verified]. And the **Braga
instruments are printed inside the book the row already linked to**: a bull of
Pius XI of 8 December 1924 and a Congregation of Rites decree of 9 December 1924,
both legible in the OCR text layer of the very item the row called whole and
fetchable [verified].

The searches underneath the negatives were honest and remain true. **What failed
was the verdict field.** `retrievable = "not-located"` is a claim about the
world; the evidence supporting it was a claim about one repository.

That is exactly the fault this same document records against the act history in
§1 — `not-found` reading as a claim about the tree when the search behind it
covered seven text layers. **The audit diagnosed the defect in another lane's
record and then committed it three times in its own, in the same sitting.** The
Braga case is the worst: nothing external was needed, because the instrument was
inside a document the row itself described as already fetched. It wrote
`unrecorded` about the contents of a book it had not opened, while linking to it.

Worse still, the file contained its own remedy and did not apply it. The
Carthusian row says in terms that when the Internet Archive returns nothing the
next attempt should be a French library — and the Lyon row, two entries later,
recorded a negative without trying one.

> **The rule this yields.** A `not-located` verdict must name **the repositories
> searched**, not only the aliases. An alias list without a host list is half a
> bound, and half a bound reads as a whole one.

## 4. The orders legislate for themselves; the diocesan uses do not

The exempting clause of *Quo primum* creates the parallel line, and the existing
act history draws that fork and then records that it holds no witness for any of
them, calling the branch *honestly empty*.

The audit's structural surprise is that filling it is **easier** than the Roman
line, not harder — but the first version of this section overstated it, and the
correction is the more interesting half.

**What was written first:** *these lines have their own promulgating acts, and
those acts are not papal — they are decrees of a general chapter and orders of a
master general, a prior general or an abbot.*

**That is true of the orders and false of the diocesan uses**, and the
counter-example was in the same group. The Braga missal of 1924 was approved by a
**bull of Pius XI** and declared typical by a decree of the **Sacred Congregation
of Rites** — signed by **Cardinal Vico and Alexander Verde, the same two men who
signed the Roman typical edition's decree of 25 July 1920**. This audit read both
decrees at the bytes. One congregation, one pair of officials, declaring typical
editions for the Roman line and for a diocesan use four years apart.

So the corrected statement is two-part:

| | who declares the typical edition |
| --- | --- |
| **The orders** | themselves — a general chapter decree or a superior's order, very often printed **on the title page** in the *iussu editum* clause |
| **The diocesan uses** | **Rome**, through the same congregation and sometimes the same officials as the Roman line |

(Sarum is neither: having no modern typical edition at all, it is a different
situation again, not a counter-example.)

The generalisation was drawn from three order missals and written as though it
held for a group that also contains Braga, Lyon, Sarum, the Ambrosian and the
Mozarabic. It is the ordinary shape of the error this project exists to catch: a
claim true of what had been read, stated as true of the class, fluent enough that
nothing in the sentence signals the jump.

The three **order** instruments, read at the bytes, which remain correct: [verified]

- **Carthusian 1679** — *ex ordinatione capituli Generalis. Anno Domini
  M.D.CLXXVII. Celebrati sub R. P. D. Innocentio le Masson Priore Cartusiae ac
  totius eiusdem ordinis generali*
- **Carmelite 1621** — *Capituli Generalis decreto … Et reverendissimi prioris
  generalis magistri Sebastiani Fantoni Romani iussu*
- **Dominican 1604** — *Sub r.mo P.F. Hieronymo Xavierre … totius praefati
  Ordinis Generali magistro recognitum & emendatum, & auctoritate Apostolica
  approbatum & confirmatum*

A datable, attributable, citable station, obtained from a catalogue field.

One further result worth naming: the **Carmelite** claim to the rite of the Holy
Sepulchre is not a modern gloss. The 1574 title page reads *…de Monte Carmelo, ad
normam, et consuetudinem Hierosolymitanae Ecclesiae* [verified].

## 5. Rights: two thirds readable, fewer than half printable

Twenty-three of thirty-one books are retrievable whole; fourteen may be published
from. The gap is almost entirely the twentieth century. (That first figure rose
from 22 during the audit — not because anything was published, but because two
`not-located` verdicts were wrong. See §3.)

**The frame this audit began with was wrong in two places, and both came in with
the brief rather than from a source.** A dedicated rights pass could source
neither half of "post-1929 works of the Holy See are protected in the US;
pre-1929 printings are generally clear":

- **The line is before 1931, not before 1930.** Cornell's chart, current as of
  1 January 2026, gives for works first published abroad: *Before 1931 | None |
  In the public domain* [verified]. Nothing in the audit turned on the year —
  the latest row claiming the rule is a 1924 printing — but the frame was
  stating a rule it had not checked, which is the same defect whether or not it
  bites. It also means **this file goes stale every January**.
- **1929 is not a US watershed for the Holy See; 1935 is.** US Copyright Office
  Circular 38a lists the Holy See's US copyright relations in full, earliest
  *Berne (Paris) Sept. 12, 1935*, with no bilateral date and no WTO entry
  [verified]. No Copyright Office, court, or published analysis making
  11 February 1929 a boundary could be found. The date is real in Vatican law —
  the Lateran Pacts, cited in Law CXCVII art. 1 — and its migration into a US
  copyright rule is **unrecorded**.

The replacement reasons are stronger than the ones they displace, which is why
the churn was worth it:

- **The altar book's own printed claim**, on the leaf after the title page of
  the 2002 typical edition [verified]:

  > *« Copyright » apud Administrationem Patrimonii Sedis Apostolicae in
  > Civitate Vaticana / Venditio operis fit cura Librariae Editricis Vaticanae*

  Note what this actually says. The holder of record is **APSA** — the
  Administration of the Patrimony of the Apostolic See — with **LEV as sales
  agent only**, not as owner. That sits awkwardly beside the Secretariat of
  State decree of 31 May 2005 vesting in LEV *every moral copyright and all the
  exclusive financial rights … over all the deeds and documents through which
  the Supreme Pontiff exercises his own Magisterium* [sourced]. Nothing located
  reconciles them; recorded as an open tension.
- **Vatican Law N. CXCVII (2017), art. 2**, which extends copyright to *the
  texts of the laws and official acts published, in whatever form, by the Holy
  See*, with a seventy-year term under art. 5 [sourced]. This is the opposite of
  the US government-edicts rule, and it is why "it is an official act, therefore
  free" fails here.
- **URAA restoration**, 17 U.S.C. §104A, effective 1 January 1996 for Berne
  members, running generally 95 years from publication [sourced]. This is the
  mechanism that actually protects twentieth-century Holy See printings in the
  US.

A rights position resting on a book's own claim is better evidence than one
resting on a treaty date nobody could cite.

### The cleanest case in the file runs the other way: Milan

The Archdiocese of Milan publishes **the whole of the 2024 second edition of the
Ambrosian Missal** as twelve free PDFs, introduced *Riportiamo qui i files PDF
per la consultazione, lo studio e la preghiera personale*. Four were probed here
and all return HTTP 200 [verified]. And the same page carries an explicit
reservation [verified]:

> *Tutti i diritti d'autore … sono riservati all'editore ITL - Impresa
> Tecnoeditoriale Lombarda srl a socio unico (© 2024). È vietata l'utilizzazione,
> la riproduzione, l'elaborazione, la diffusione e la stampa anche parziale senza
> autorizzazione scritta dell'editore, essendo consentita esclusivamente la
> consultazione on-line per uso personale e senza finalità di lucro*

**Free to read in full; explicitly not free to republish** — even partial
printing forbidden without written permission. This is the cleanest illustration
in the audit that `retrievable = whole` and `may_publish_text = no` are **not in
tension**. A project that collapsed the two would either wrongly refuse to read
this book or wrongly reprint it.

Note also that the publisher is a diocesan company, not LEV: the Ambrosian books
are not Holy See imprints and their rights do not follow the Roman rows.

**Retrieval and publication are separate acts** and the audit keeps them apart
throughout, as `sources.md` requires. A book may be `retrievable = "whole"` and
`may_publish_text = "no"`, and several are. Acquiring the 1970 typical edition's
identity and route is correct; printing a line of it is not.

Three rights positions were left explicitly open rather than resolved:

- **The CMAA 1962 facsimile — now answerable.** Four things were established.
  The **hosting page carries no rights notice at all**: 54,516 bytes fetched and
  searched for `copyright`, `©`, `creative commons`, `public domain` and `all
  rights` — every one returns **zero** [verified]. The **facsimile itself carries
  no copyright notice**, across all 54,807 extracted lines [sourced]. The **CC
  BY-NC-ND was applied by a private individual** — uploader
  `m.kusnjacic@gmail.com`, in a personal collection, describing the book as taken
  from a Croatian website — while the same item credits the CMAA as *creator*
  [verified]. And **at least nine Internet Archive items of this book contradict
  each other**: two CC BY-NC-ND, two CC public-domain mark, five no licence,
  including the one that is explicitly the CMAA file re-uploaded [sourced].

  Under *Bridgeman* there is no new copyright in the scan for anyone to license,
  and the Internet Archive states it *does not make guarantees as to the
  copyright status of items on archive.org* [sourced]. So `unresolved` on the
  artifact **stands and is correct** — it records the absence of affirmative
  permission — but the open question about the licence can be **closed with a
  reason**: it is an assertion by someone who is neither rights holder nor
  scanner, over bytes carrying no new copyright, hosted by a body that publishes
  no notice. It confers nothing.
- **The 1942 Benziger** carries its own US copyright line and no renewal search
  is recorded.
- **The 1936 Premonstratensian** has Internet Archive metadata with no publisher,
  no date field and no copyright statement [verified] — nothing established in
  either direction, which is a different thing from being free.

### `absent: icel` is right, and its stated reason is not quite

`the-shape.md` §4 gives `absent: icel` as its example of an absence carrying a
reason: *a postconciliar text nobody may publish*. **That reason is too strong as
stated**, and an absence must carry a true reason or it is doing the same job as
a silence.

ICEL's own published policy contains a standing conditional permission: approved,
recognised and promulgated ICEL texts *may be reproduced in a non-commercial site
… on the global computer network commonly known as the Internet without obtaining
written or oral permission*, subject to five conditions — no access fee, the
acknowledgment on first and last pages, texts followed exactly, and ICEL
reserving the right to terminate [sourced]. The USCCB points the other way:
*with the exception of … single daily collects from the Roman Missal, no
permission will be given for the publication of liturgical texts on the Internet
at this time* [sourced].

So the position is **a conflict between two bodies**, not a prohibition. The
operational answer is unchanged — a conditional permission with five conditions
and a termination clause is not a basis for a library to print from, and the
USCCB directly contradicts it — but the recorded reason should be *the two bodies
that would have to agree do not*, rather than *nobody may*.

> **Check before acting.** Another lane was working this exact ground
> concurrently on 2026-08-01, with uncommitted records for ICEL publication
> policies and WIPO Berne contracting parties. That work is not cited here
> because it was not committed, and this audit does not adopt another lane's
> uncommitted files. Reconcile before either is relied on.

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
5. **The first use — now Braga, revised during the audit.** It is the only row in
   the file where **both the book and its promulgating acts are in hand and
   publishable**: a whole 1924 typical edition, pre-1931 and therefore printable,
   plus a bull and a Congregation decree now read at the bytes. A complete
   station-plus-witness pair for a non-Roman use is exactly what the empty branch
   needs, and nothing else here offers one. Sarum remains the best *critical*
   text; the **Ambrosian**, raised to top priority among the uses, is the largest
   rite and the only living one readable in full today.
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
4. **The count is reported, not verified.** A research pass reports **23** sui
   iuris Churches in five traditions — Alexandrian, Armenian, Byzantine, East
   Syriac, West Syriac — and notes the figure is sometimes given as 24 depending
   on whether the Latin Church is counted, with the canonical enumeration resting
   on the *Annuario Pontificio*, which was not reached [reported]. Recorded as a
   lead. **Not to be printed as settled.**

Starting points for the separate track, all reported and none verified: the
promulgating authority is a single body, the **Dicastery for the Eastern
Churches** (*Praedicate Evangelium* arts. 82–87), whose own page cites **CCEO
can. 657** to the effect that all liturgical texts to be published are submitted
to its *recognitio* or approval. The book names differ by tradition — Hieratikon,
Sluzhebnik, Euchologion (Byzantine); Taksa for the Holy Qurbana (East Syriac);
Qurbono (West Syriac and Maronite); Patarag (Armenian); Qeddase (Alexandrian) —
which is the first reason a missal-shaped search fails. **No individual Church's
official service book was verified as available online.**

The right first deliverable is not an inventory but a single sourced page fixing
the list of Churches, the principal eucharistic book in each tradition, and the
promulgating authority — and only then a search. **Do not extend the audit file
to cover them.** A Roman-shaped row about an Eastern book is a reference that will
resolve successfully and wrongly.
