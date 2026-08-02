# Act histories: the Latin missal as a history of acts

A liturgical history rendered as a Git repository, where the shape of the graph
is the finding.

**Part one** is the report on a tracer through Holy Week, 1570 to 1962, built on
2026-07-31: what it proved, what it broke, and what it cost. **Part two**, from
section 11, is the wider slice built on 2026-08-01 -- 1484 to 2023, seventeen
lines, the uses and the order rites beside the Roman one -- and the amendments it
required to the rule part one is built on. Part one is not edited to match it.

**Part one owns no rules; part two owns three.** `time-machine.md` settles the
rest — no station without an act, parallel stays parallel, the diff is the
acceptance test — and part two settles, on the maintainer's ruling of
2026-08-01, the `promulgated`/`printed` station vocabulary (§11), what an edge
must declare it rests on (§12), and the date-prefixed path convention (§13).

**One of those amends a rule this document does not own, and the tension is on
the record rather than resolved here.** `time-machine.md` Rule 1 is *no station
without an act*, and §11 admits a printing as a station where no act has been
located. The reason behind Rule 1 is unchanged and §11 restates it; what changed
is that refusing a surviving book was found to be its own kind of silence.
`time-machine.md` is not this lane's surface and is not edited from here, so it
still states the unamended rule. Whoever reconciles them should read §11 first.

`recensions.md` settles the departure model, a base and its departures with
identity writing no row, and that model is untouched by anything in part two.
Those two propose; this one measures. Everything below was built and run, and
where a ruling left a question open under test, the result is here rather than
in the document that asked it.

## Evidence conventions

- **[verified]** — measured during this tracer against tracked artifacts or by
  running the tool. Reproducible.
- **[sourced]** — read out of an external document, cited by artifact and line.
- **[inferred]** — reasoned from the above, flagged wherever it matters.

## What was built

| | |
| --- | --- |
| source encoding | `src/sources/inventories/roman-holy-week-acts-v1.toml` |
| generator | `tools/act-history` (`check`, `graph`, `structure`, `plate`, `commonality`, `emit`) |
| generated repository | `build/act-history/roman-holy-week`, untracked |
| corpus read | seven Internet Archive OCR text layers at `~/git/lt-hist` |
| size | 12 acts, 2 lines, 9 witnesses, 4 masses, 38 base units, 42 departures |

The generated repository is a build artifact, like a PDF. Regenerating it
rewrites every hash and that is expected. The record is the source encoding.

---

## 1. Applying Rule 1: which of these nodes is a station?

`time-machine.md` Rule 1 — no station without an act — was applied node by node.
The tracer began keyed on books, as the brief framed it, and was re-keyed on
acts. **The rule pruned the brief's own line, and that is the tracer's first
finding rather than a shortfall.**

| Candidate node | Act found? | Verdict |
| --- | --- | --- |
| 1570 Missal | *Quo primum tempore*, Pius V, 14 July 1570, printed in the front matter of two witnesses | **station** |
| 1604 Missal | *Cum sanctissimum*, Clement VIII, 7 July 1604, dateline read | **station** |
| — | *Si quid est*, Urban VIII, 2 September 1634, dateline read | **station** the brief did not list |
| **1862 Pustet** | **none. Its title page says *CUM APPROBATIONE SACRORUM RITUUM CONGREGATIONIS* — leave to print. The two decrees in its front matter are of 1862 and concern a Mass of the Japanese Martyrs and one of Bl. John Leonardi *pro aliquibus locis*, neither in this slice** | **witness, not a station** |
| 1920 Missal | *Decretum approbationis editionis typicae Vaticanae*, in the book | **station** |
| 1955 reform | *Maxima redemptionis*, S.R.C., 16 November 1955, AAS 47 (1955) 838-841 | **station** |
| — | *Rubricarum instructum* 25 July 1960 and the S.R.C. decree of 26 July 1960, both printed entire in the 1962 witness | **two stations** the brief did not list |
| **1962 Missal** | **none in this corpus: 136,068 lines hold three occurrences of `DECRETUM`, all belonging to the 1960 documents. Named *Novo rubricarum corpore* from `time-machine.md` §4, not read. See §7.2** | **station, instrument not read** |
| **1806 English** | **none. No approbation, imprimatur, *permissu*, licence or Vicars Apostolic anywhere in the book** | **witness, not a station** |
| **1843 English** | **none about the rite. Its title page carries a US copyright registration and a treatise by a bishop; neither changes the missal** | **witness, not a station** |

Four of the brief's seven nodes are not stations. Two stations the brief did not
name are, and were found only because the rule forced the question. The Latin
line the brief drew — 1570 → 1604 → 1862 → 1920 → 1962 — has one false edge in
it, and the English line does not exist in this encoding at all.

**Independently corroborated.** `time-machine.md` §4, deriving a coarse view from
a different property entirely — whether an act produced a new typical edition —
arrives at a skeleton of 1570, 1604, **1634**, 1884, 1920, 1962 and later. It
includes the 1634 revision this tracer had to add, and excludes 1862, which this
tracer had to remove. Two routes to the same set is worth more than either.

Section 6 measures what the rule buys against the OCR. It is worth a great deal.

---

## 2. The DAG, and every edge with its source

```
                    quo-primum-1570  (root)
                    ├── quo-primum-exemption-1570        [line: exempt-uses]
                    └── cum-sanctissimum-1604
                        └── si-quid-est-1634
                            └── divino-afflatu-1911
                                └── abhinc-duos-annos-1913
                                    └── editio-typica-1920   (via unrepresented: typica 1900)
                                        ├── de-rubricis-simpliciorem-1955
                                        │   └── rubricarum-instructum-1960
                                        │       └── codex-rubricarum-1960 ──┐
                                        └── maxima-redemptionis-1955 ───────┤
                                                                            └── editio-typica-1962
```

Two branches, one merge, one root per line, and one edge marked as crossing a
station the record does not hold.

| Edge | Basis, and where it was read |
| --- | --- |
| — → `quo-primum-1570` | Root. What precedes it — the pre-Tridentine curial missal, the 1474 Milan printing — is a live question and **no edge is drawn into it**. A root means "the record starts here". |
| `quo-primum-1570` → `quo-primum-exemption-1570` | Same instrument, same day. Drawn as its own station because it is what makes the other uses a line rather than an absence. [sourced: pustet-1862 OCR 189-198, 231] |
| `quo-primum-1570` → `cum-sanctissimum-1604` | The bull's own account of what it revises: *tum in primis fel. rec. Pius Papa Quintus Missale Romanum ex Decreto Sac. Concilii Tridentini ad veterem, et emendatiorem normam restitui, Romaeque imprimi curavit*. [sourced: pustet-1862 OCR 286-406] |
| `cum-sanctissimum-1604` → `si-quid-est-1634` | The bull names both predecessors and says it follows in their steps: *Pius V. et Clemens VIII. diligentissime recognosci atque instaurari curaverunt; Nos quoque eorum vestigiis inhaerentes*. [sourced: pustet-1862 OCR 409-447] |
| `si-quid-est-1634` → `divino-afflatu-1911` | The 1920 decree of approbation names the two norms its edition was made to. [sourced: missale-romanum-1920 OCR 18-19] |
| `divino-afflatu-1911` → `abhinc-duos-annos-1913` | Named beside it in the same clause, and later. [sourced: missale-romanum-1920 OCR 19-20] |
| `abhinc-duos-annos-1913` → `editio-typica-1920` | The decree of approbation, subscribed *Die 25 Julii 1920*, A. Card. Vico prefect, Alexander Verde secretary. **Marked `via_unrepresented`**: the decree says the text was drawn *ex altera typica anni 1900*, an edition not in this corpus. The edge means "descends from", not "immediately follows". [sourced: missale-romanum-1920 OCR 7-64] |
| `editio-typica-1920` → `de-rubricis-simpliciorem-1955` | It simplifies the rubrics of the books that edition carried. [sourced: named and dated in *Rubricarum instructum*, benziger-1962 OCR 1131-1134, 1171-1173] |
| `editio-typica-1920` → `maxima-redemptionis-1955` | The state the decree reformed is the one that edition carried. [sourced: AAS 47 (1955) 838-841, aas-47-1955 OCR 51717-51940] |
| `de-rubricis-simpliciorem-1955` → `rubricarum-instructum-1960` | **An act that says what it supersedes has drawn its own edge**: *Pariter vigere cessat Decretum generale S. R. C. diei 23 Martii anni 1955 De rubricis ad simpliciorem formam redigendis, in hac nova rubricarum redactione assumptum*. [sourced: benziger-1962 OCR 1171-1173] |
| `rubricarum-instructum-1960` → `codex-rubricarum-1960` | The decree recites the act it executes, by title and date. [sourced: benziger-1962 OCR 1235-1254] |
| `maxima-redemptionis-1955` + `codex-rubricarum-1960` → `editio-typica-1962` | **The one merge.** Reception shown from both sides — see section 5. The node's own instrument was **not found**; see section 7. |

### Edges deliberately left undrawn

- **1862 Pustet → 1920.** Chronologically adjacent, and false. The 1862 is a
  commercial Ratisbon printing whose title page says *CUM APPROBATIONE SACRORUM
  RITUUM CONGREGATIONIS* — leave to print — and whose latest named authority is
  Urban VIII [verified]. The 1920 decree names its own parent and it is the 1900
  typical edition [sourced]. A generator that chains versions by date would have
  drawn this edge and asserted that the Roman Holy Week descends through a German
  publisher.
- **1806 and 1843 English → any Latin edition.** Neither book names a Latin
  exemplar. A search of both for an approbation, imprimatur, *permissu*,
  licence, or the Vicars Apostolic returns nothing [verified]. They are attached
  as witnesses on a **date bound only**, labelled `attests_kind = "date-bound"`,
  and that weakness is on the record rather than hidden behind a confident edge.
  The repository's own family ledger had already found the same thing of the
  1861 Cummiskey: *the book states no Latin exemplar, and its formularies were
  matched to the 1962 Missal by collation, not by a stated descent*.
- **A pre-1955 line continuing beside 1962.** The brief expected this branch —
  the emacs/xemacs case. No act permitting it was found in this corpus, and none
  is asserted from memory, so **it is not drawn**. The absence is a statement
  about this search, not about history.

---

## 3. The pruning, stated plainly

**The English line does not survive Rule 1.** A lay translation is not an act.
Nothing in the 1806 or the 1843 changes the missal, and no decree, edict or
approbation for either was found. The 1843's title page carries a US copyright
registration — *Entered according to the Act of Congress, in the year 1843, by
EUGENE CUMMISKEY* [sourced] — which is an act, dated, by a named party, in a
named jurisdiction, and is not an act about the rite. So the English books are
witnesses, and **the parallel English line the brief asked for does not exist in
this encoding.**

That is not a gap to be filled later by finding a better source. It is the rule
saying that a translation is evidence about a state, not a state of its own. The
convergence the brief expected from the English side — each lay missal taking
from a Latin edition — survives as a witness attachment, and a weak one: both
books are attached on a date bound, because neither names an exemplar.

**The 1862 Pustet is not a station either**, for the reason in §1.

That leaves the exemption clause of *Quo primum* as the tracer's only genuine
parallel line, and it is a good one: the constitution excepts uses whose
institution the Apostolic See approved or whose custom had run above two hundred
years, and says of them *praefatam celebrandi constitutionem, vel consuetudinem
nequaquam auferimus* [sourced: pustet-1862 OCR 189-198, 231]. Those uses kept
their own Holy Week and never rejoined. **This corpus holds no witness for any
of them**, so the branch is a root and nothing more.

An empty branch that is honestly empty is worth having. The fork is in the
record because an act put it there, and its emptiness measures what the corpus
holds rather than what happened.

---

## 4. The four storage decisions, settled against real diffs

`time-machine.md` Rule 6 fixes the acceptance test and names the four things
that decide it. This section reports what each was set to and what it measured.
The full station diff that tests all four at once is §4.6.

### 4.1 Granularity: one file per addressable unit

`holy-week/<mass>/<slot>.txt`, plus `mass.txt` and `order.txt` per mass. Forty-
eight files at the tip [verified]. The alternative measurements:

| Encoding | What the 1955 reform's diff would look like |
| --- | --- |
| one file per missal | one file, wholly rewritten |
| one file per mass | four files, each wholly rewritten |
| **one file per unit** | **36 files, 31 of them changing by exactly two lines** [verified] |
| one file per line of text | thousands of files; git copes, a reader does not |

The unit — one proper, one rubric, one antiphon — is where the acts actually
bite, so it is where the file boundary goes.

### 4.2 Path is liturgical identity, never page order

`holy-week/sabbato-sancto/prophetia-04.txt` is the same object in 1634 and in
1955. Nothing in a path is a page, a leaf, a line range or an ordinal position
in the printed book. Order lives in a separate `order.txt`, so a reordering is
one file's diff rather than a cascade of renames.

This is the defect `time-machine.md` Rule 6 names in the earlier corpus, and it
was confirmed on the way past: that corpus's `source_lines: 50001-70000` windows
mean any insertion shifts every offset below it.

### 4.3 Deterministic serialisation

Sorted iteration everywhere, one fixed author identity, timestamps derived from
act dates alone, trees built with `mktree` from a sorted flat path map rather
than through an index. Measured: two successive `emit` runs produce byte-
identical commit hashes, `c3b024c4…` both times [verified].

### 4.4 Semantic line breaks, applied by the generator

Break points set at full stop, colon and semicolon, and **not at commas**: Latin
orations are comma-dense, and breaking there puts three words on a line and
loses the clause as the unit a reader compares. Rule 6 requires the rule be
mechanical; it is applied by `tools/act-history` at emit time and the source
stores text unwrapped, so there is nothing for a later hand to re-wrap.

```
Omnipotens sempiterne Deus, qui etiam judaicam perfidiam a tua misericordia non repellis:
exaudi preces nostras, quas pro illius populi obcaecatione deferimus;
ut, agnita veritatis tuae luce, quae Christus est, a suis tenebris eruantur.
Per eundem Dominum.
```

### 4.5 The one that was free: git carries `reslotted` natively

`reslotted` is the hard departure kind — the same words in a different slot,
invisible to any matcher keyed on `(mass, proper-name)`. Under this encoding
git's own rename detection finds it without being told [verified]:

```
$ git show -M --format='' 291c0d3 -- holy-week/sabbato-sancto/postcommunio-seu-oratio.txt
diff --git a/holy-week/sabbato-sancto/vesperae-oratio.txt b/holy-week/sabbato-sancto/postcommunio-seu-oratio.txt
similarity index 89%
rename from holy-week/sabbato-sancto/vesperae-oratio.txt
rename to holy-week/sabbato-sancto/postcommunio-seu-oratio.txt
@@ -1,4 +1,4 @@
-Oratio
+Postcommunio seu Oratio
 Spiritum nobis, Domine, tuae caritatis infunde
```

`git log --follow` walks through it to the unit's introduction in 1634
[verified]. The whole 1955 station, with rename detection on:

```
 rename holy-week/dominica-in-palmis/{evangelium-ante-benedictionem.txt => evangelium-post-distributionem.txt} (100%)
 delete mode 100644 holy-week/dominica-in-palmis/graduale-collegerunt.txt
 delete mode 100644 holy-week/dominica-in-palmis/praefatio.txt
 delete mode 100644 holy-week/dominica-in-palmis/sanctus.txt
 ... eight more deletions
 rename holy-week/sabbato-sancto/{prophetia-01.txt => lectio-01.txt} (72%)
 rename holy-week/sabbato-sancto/{prophetia-04.txt => lectio-02.txt} (73%)
 rename holy-week/sabbato-sancto/{prophetia-11.txt => lectio-04.txt} (68%)
 rename holy-week/sabbato-sancto/{vesperae-oratio.txt => postcommunio-seu-oratio.txt} (89%)
 delete mode 100644 holy-week/sabbato-sancto/prophetia-02.txt
 ... seven more suppressed prophecies
```

And the mass header carries `renamed` and `moved` as two legible lines:

```
-title: Sabbato Sancto
+title: Sabbato Sancto: De Vigilia paschali
 day: Saturday of Holy Week
-hour: in the morning, after None
+hour: circa mediam noctem inter sabbatum sanctum et dominicam Resurrectionis
```

**How free is free? Measured across four flag settings** [verified, git 2.55],
counting renames detected in the 1955 station:

| invocation | renames found |
| --- | ---: |
| `git show` (no flags at all) | **6** |
| `git show -M` | 6 |
| `git show -M --find-copies-harder` | 6 |
| `git show -M20% --find-copies-harder` | 6 |

**No flags are needed.** `diff.renames` has defaulted to true since git 2.9, so
a reader who clones this repository and types `git show` gets the reslotted
prayer as a rename without knowing that rename detection exists. Neither
`--find-copies-harder` nor a threshold as low as 20 per cent finds one more.

**Where it fails, and it matters.** When an act both moves a unit and rewrites
it, similarity collapses and git shows a delete beside an unrelated create. Two
cases here: the third Vigil lesson, which is Isaiah 4 with verse 1 dropped, and
the Holy Saturday canticle antiphon, which moves from Magnificat to Benedictus
with new words. Nothing in the table above recovers either — the files are three
lines long, so there is not enough text left to match on.

So the answer to `time-machine.md` §7's open question is **yes, with one
boundary**. The viewer needs no machinery for `reslotted` where the words are
unchanged, which is six of eight cases here. `reslotted` must nonetheless stay a
first-class departure kind in the source, because the two it misses are exactly
the cases where a reader most needs telling that the words did not appear from
nowhere.

### 4.6 The acceptance test: a real station, in full

`git show` on `maxima-redemptionis-1955`, unedited except for eliding
twenty-three further file lines of the same shape:

```
commit 6890a1f
Author: Roman Holy Week tracer
Date:   11955-11-16

    Maxima redemptionis restores the order of Holy Week

    The largest set of departures in this slice.

    Act: Decree Maxima redemptionis nostrae mysteria
    Act-date: 1955-11-16
    Authority: Pius XII, through the Sacred Congregation of Rites
    Line: typica
    Citation: Sacred Congregation of Rites, Maxima redemptionis nostrae mysteria,
      16 November 1955, in Acta Apostolicae Sedis 47 (1955), with the Instruction.
    Descends-from: editio-typica-1920
    Effect-established: yes
    Departures: absent 20, moved 3, renamed 3, replaced 2, reslotted 8
    Timestamp-shift: +10000 years; git refuses a pre-1970 date

 acts/maxima-redemptionis-1955.txt                        | 28 ++++++++++
 witnesses/aas-47-1955.txt                                | 14 ++++++
 ...ionem.txt => evangelium-post-distributionem.txt}      |  0
 holy-week/dominica-in-palmis/graduale-collegerunt.txt    |  2 --
 holy-week/dominica-in-palmis/lectio-exodi.txt            |  2 --
 holy-week/dominica-in-palmis/mass.txt                    |  4 +-
 holy-week/dominica-in-palmis/praefatio.txt               |  2 --
 holy-week/dominica-in-palmis/sanctus.txt                 |  2 --
 holy-week/sabbato-sancto/{prophetia-01.txt => lectio-01.txt}                  |  2 +-
 holy-week/sabbato-sancto/{vesperae-oratio.txt => postcommunio-seu-oratio.txt} |  2 +-
 holy-week/sabbato-sancto/mass.txt                        |  4 +-
 holy-week/sabbato-sancto/order.txt                       | 23 +++++-----
 ... 26 more file lines
 38 files changed, 65 insertions(+), 83 deletions(-)
```

Read it as a reader would. An act, dated, with its instrument and its citation
in the header. The blessing of palms loses its lesson, its gradual, its preface,
its Sanctus and five blessing prayers — one deleted file each. The Gospel of the
blessing moves after the distribution as a hundred-per-cent rename. The first
prophecy becomes the first lesson, and the Vespers prayer becomes the
Postcommunion, both as renames carrying their words.

**The measured shape of it** [verified]. Of the 38 files, two are the station's
own record — the act and the witness it was read in — leaving 36 files of
liturgy, 23 insertions and 83 deletions. Their size distribution:

| changed lines in the file | files |
| ---: | ---: |
| 0 (a pure rename) | 1 |
| 2 | 31 |
| 4 | 2 |
| 13 | 1 |
| 23 | 1 |

**Thirty-one of thirty-six files change by exactly two lines**, because a unit
file is a name and an incipit and a suppressed unit takes both with it. The two
four-line files are mass headers, changing title and hour. Not one unit file is
a wall.

**The outlier is real and is the cost of a deliberate choice.** The 23-line file
is `sabbato-sancto/order.txt`, which absorbs the whole reordering of Holy
Saturday — eight prophecies gone, four renamed to lessons — in one hunk. Keeping
order in its own file is what stops a reordering cascading into renames of every
unit below it (§4.2); the price is that the reordering lands in one place and
looks big there. That is the right trade and it should be stated rather than
averaged away: the largest hunk in the station is 25 lines and every one of them
is in that file.

That is the acceptance test passing at four liturgies, which is where it is
cheap to fail.

---

## 5. Divergence, convergence, parallelism, and the empty station

**Divergence** — `maxima-redemptionis-1955` carries 34 of the 42 departures. The
blessing of palms loses its collect, its lesson, its gradual, its preface, its
Sanctus and five of six blessing prayers; the twelve prophecies of Holy Saturday
become four lessons; the Vigil moves from Saturday morning to midnight
[verified against both sides].

**Convergence** — the single merge, and it is drawn because the reception is
shown to the letter and not inferred from the fact that both acts precede it:

- section 9 of *Maxima redemptionis*, fixing the Vigil at midnight, is printed in
  the 1962 witness as the same sentence: the Acta at `aas-47-1955` OCR
  51915-51921, the book at `benziger-iuxta-typicam-1962` OCR 40203-40212. The
  two were compared token by token [verified], and the comparison is worth
  reporting exactly, because it turned into the tracer's own sharpest measurement
  of the OCR hazard — see the note below.
- the Code of Rubrics is printed entire in the same book's front matter from
  line 1276, with its promulgating decree above it at 1235-1272, and its
  renaming of the Introit is then carried into the Palm Sunday propers at 35155
  [sourced].

**The note, and it is the tracer in miniature.** That comparison was first
written up here as "word for word", which is what it looks like to a reader and
is not what the bytes say. Normalised to letters and spaces and compared as
token sequences, the two OCR renderings of one sentence agree on **75.7 per
cent** of tokens [verified]:

```
AAS  : solemnis paschalis vigilia celebranda est hora competenti ea scili cet quae permittat ...
1962 : h solemnis vigilia paachalis cclebranda est hora competenti ea scilicet quee permittat ...
```

`celebranda`/`cclebranda`, `quae`/`quee`, `vigiliae`/`vigilite`, `scilicet`
split across a line break in one scan and not the other. Every one of those is a
scanner. One is not: the Acta read *Solemnis paschalis vigilia* and the book
*Solemnis Vigilia paschalis*, a word order difference that could be the decree,
could be the book, and **cannot be told apart from the other seven without page
images**.

So the single strongest piece of evidence in this tracer — an act and a book
agreeing to the letter — degrades to three-quarters agreement the moment it is
measured through two scans. The reception is not in doubt; no reading of these
divergences makes the book print a different rule. But if a quarter of the
tokens move on the sentence chosen *because* it is identical, nothing about a
diff of two OCR texts should be trusted where an act does not stand behind it.

`act-history check` enforces the reception rule: **an act with more than one
parent that carries no `reception_basis` is rejected.** A merge asserts a
synthesis, so it must cite one.

The three-way merge itself refuses to guess. Where two parents leave the same
unit in two different states, the tool raises rather than preferring a side,
because silently preferring one is how a synthesis nobody performed gets drawn.

**Parallelism** — `exempt-uses` forks at 1570 and never rejoins. No act in the
encoding may name parents on two different lines, so the tool cannot draw a
merge across them even by mistake.

**The empty station** — `divino-afflatu-1911` and `abhinc-duos-annos-1913` each
commit exactly one file, their own act record:

```
$ git show --stat c3b9a15
c3b9a15 11911-11-01 Divino afflatu orders the new arrangement of the Psalter
 acts/divino-afflatu-1911.txt | 30 ++++++++++++++++++++++++++++++
```

A history keyed on diffs would have dropped both. A history keyed on acts keeps
them, and the empty commit is the record saying that an authority acted and this
slice did not move.

There is a sharper version of the same point. *Maxima redemptionis* §6 legislates
the hour of the Palm Sunday blessing: *fiunt mane, hora consueta; in choro autem
post Tertiam* [sourced: aas-47-1955 OCR 51902-51903]. That is exactly the hour
the pre-1955 books already kept. **A decree explicitly legislated a thing and
changed nothing, so it writes no row** — identity writing no row, arriving from
an act rather than from a comparison.

### Departure kinds actually needed

All seven of `recensions.md` §3 were exercised [verified]:

| kind | count | hardest instance |
| --- | ---: | --- |
| `absent` | 20 | eight of twelve prophecies suppressed |
| `added` | 1 | the numbered titles over the solemn prayers |
| `moved` | 3 | the Vigil from Saturday morning to midnight |
| `renamed` | 5 | *Feria VI in Parasceve* → *in Passione et Morte Domini* |
| `replaced` | 2 | Isaiah 4,1-6 → 4,2-6, verse 1 dropped |
| `reslotted` | 8 | *Spiritum nobis* — the case this whole apparatus exists for |
| `unrecorded` | 3 | the Good Friday prayer for the Jews |

**`reslotted` needed to be split from `replaced`.** The Isaiah lesson both moves
and changes, and it is recorded as two rows because they are two different
claims — one about where it stands, one about what it says. Collapsing them
would make a reader unable to tell which was established.

**`unrecorded` needed a stronger implementation than "resolves to nothing".**
`recensions.md` Rule 3 says it must never silently fall back to the base, and a
first implementation that simply skipped the row did exactly that: the 1962
commit would have carried `perfidis` forward, which is false to the witness. The
tool now **removes the unit from the liturgy and writes a marker** under
`unestablished/` saying the state is not known and why. Carrying the inherited
text forward would have been the stronger claim, made for free.

---

## 6. What the OCR does to a diff, measured

Every reading in the tracer is `ocr-only`. Not one was collated against a page
image, and the file says so in its own `evidence` block.

**The calibration this repository already owns.** On 2026-07-31 it collated 99
orations taken from an OCR text layer of an 1861 printing against the page
images of that same printing and corrected 38 of them — `Lard` for `Lord`,
`tliese` for `these`, a comma where the page prints a full stop [verified from
`roman-1962-proper-translations-v1.toml`]. That sample was biased toward the
loci most likely to be wrong, so 38 per cent is an upper bound, not an estimate.

**The measurement made here.** Lines matching each unit label, inside the Holy
Week slice of three witnesses [verified]:

| label | 1862 Pustet | 1920 typica | 1962 Benziger |
| --- | ---: | ---: | ---: |
| `Prophetia` | 8 | 15 | 0 |
| `Postcommunio` | 3 | 8 | 6 |
| `Introitus` | 0 | 5 | 0 |
| `Oratio` | 37 | 52 | 32 |
| `Antiphona` | 16 | 25 | 50 |

**The first two columns are two witnesses of the same state.** No act stands
between them in this record. Both books print twelve prophecies — confirmed by
reading every heading with its biblical citation and incipit, one by one, in
both [verified]. A strict search for the label returns 8 lines in the 1862 and
15 in the 1920, and of the 1862's 8 only six are headings: its OCR renders the
rest as `lYophetia priina`, `IVophcfia secunda`, `Prophotia qunrta`,
`Prophet.ia dedma`, `Prophctia undeciina`. The `Postcommunio` count differs by
a factor of nearly three, and the 1862 scan loses the word `Introitus` entirely.

Every one of those differences is a scanner. A generator that built its unit
inventory by matching labels in OCR would report the 1862 book as having lost
seven prophecies and five postcommunions between 1862 and 1920, and would date
the loss to a printing.

**And the failures are not random.** They concentrate on the chanted and
ceremonial units, which is exactly where the 1955 reform acted:

- The Palm Sunday Introit's own words, *Domine, ne longe facias*, return nothing
  in the 1862 and 1920 scans and are found at line 35161 in the 1962 scan
  [verified]. Both older books print the Introit; both set it with chant
  notation, and the text layer does not carry it.
- *Vere dignum* returns 0 in the 1862 and 1920 scans and 16 in the 1962
  [verified].
- The *Improperia* incipit *Popule meus* returns nothing in any of the three
  within Holy Week [verified].

So a diff built on these text layers would be blindest precisely where the
change was largest. Three of the tracer's own units carry a label and citation
read from the page and **no incipit**, because the words were not in the scan;
that is a different claim from a unit nobody looked for, and the encoding keeps
them apart.

**What the act rule buys.** None of the above can become a commit, because a
commit is an act. The OCR's disagreements live at the witness level, where they
belong. One example is in the data: the two pre-1955 witnesses print different
rubrics at the Good Friday prayer for the Jews — the 1920 has the long form, the
1862 only *Non respondetur Amen, sed statim dicitur* — and with no act between
them, that is recorded as a disagreement between witnesses and generates no
station.

**What a diff between two OCR texts is worth.** As evidence about the books,
nothing on its own. It is worth something when an act stands behind it, and it
is worth something as a **negative bound** on a whole-file search: a word absent
from every line of a scan may still be printed in the book, but a word present
was read by something. Every "not in the witness" basis in the encoding is a
whole-file search, stated as such, and correctable.

---

## 7. What broke

### 7.1 The tracer misidentified its own principal witness, and the rule caught it

The corpus records its 1962 text as *Missale Romanum 1962*, and the encoding
recorded it that way until its front matter was read. It is not the Vatican
typical edition. Its title page says **EDITIO IUXTA TYPICAM**, its publisher is
Benziger Brothers of New York, and its authority page is a diocesan imprimatur:
Francis Cardinal Spellman, under canon 1390, approving this first edition *iuxta
typicam* and citing the Congregation of Rites' declaration of 21 October 1961
that the Benziger Missal agrees with the typical edition [sourced].

This is the 1862 Pustet case a century later, and the tracer walked straight
into it. It was caught because the act rule forces the question *which act does
this book attest* to be answered in writing, for every witness.

### 7.2 The merge has no citable act, and the node stands anyway

The 1962 scan contains **no** decree approbating a 1962 typical edition, no *Quo
primum*, and only three occurrences of the word `DECRETUM` in 136,068 lines, all
belonging to the 1960 documents [verified].

So `editio-typica-1962` fails the rule that every station cites its instrument.
It is kept, flagged `act_citation = "not-found"`, with a required note saying
so, and `act-history check` refuses that value without the note. The reasoning:
an edition certainly was promulgated — both parent acts order their content into
the typical editions of the Missal, and a book exists that carries both — but
the instrument was not found here and is not asserted from memory. Dropping the
node would leave the two reforms on branches that never join, which is false in
the other direction. **A reader can see a flagged gap; a reader cannot see a
node that was never drawn.**

**Since first drawing it, the instrument has acquired a name from elsewhere.**
`time-machine.md` §4 records, from separate research, that the 1962 decree is
*Novo rubricarum corpore* and that **it is not in AAS 54** [sourced] — which
explains why searching an AAS volume and a missal scan for it returned nothing.
The station now names it. It is **not** promoted: no text of it has been read
here, `act_citation` stays `not-found`, and it stays there until someone reads
the decree rather than a report of one. Naming a document and reading it are
different acts, and the encoding keeps them apart.

> ### CORRECTION, 2026-08-01: the decree was in the repository the whole time
>
> The paragraph above is left standing because it records what the tracer knew.
> It is now wrong, and the way it was wrong is worth more than the finding.
>
> The missal acquisition audit read the decree at page 2 of the Vatican typical
> edition — in the CMAA facsimile **this repository already had registered**,
> whose SHA-256 the audit recomputed and matched. It begins *Novo rubricarum
> corpore, a Summo Pontifice Ioanne XXIII, Motu proprio « Rubricarum instructum »
> diei 23 iulii anno 1960 approbato posteroque die a Sacra Rituum Congregatione
> promulgato…*, declares the edition typical in terms — *hinc est quod praesens
> Vaticana Missalis romani editio uti « typica » declaratur* — and is dated
> *Romae, ex aedibus Sacrae Rituum Congregationis, die 23 iunii 1962*, subscribed
> by Cardinal Larraona and Enrico Dante [verified].
>
> Worse: a passage record asserting exactly this, `states = [… "verified"]`,
> `verified_on = "2026-07-25"`, existed **six days before this tracer ran**.
>
> The tracer was not careless. It searched its own corpus, and its 1962 witness
> is the Benziger printing, which carries a New York imprimatur and no Vatican
> decree. *Only three occurrences of `DECRETUM` in 136,068 lines* is a true
> statement about that scan. The error was recording a corpus result in a field
> that reads as a claim about the repository — and §1 of `the-shape.md` is
> precisely about references that resolve successfully and wrongly.
>
> `act_citation` is now `cited-externally`; `date_note` no longer calls the day
> conventional, because the day is printed in the dateline. The corpus and its
> negative result are unchanged.
>
> **The lesson is not "search harder".** It is that a tracer bounded to a corpus
> must say so in the field it writes, not only in the prose beside it. A reader
> of `act_citation = "not-found"` cannot see that "not found" meant "not in
> these seven text layers".

### 7.3 A famous change has no instrument, and therefore no station

Between the pre-1955 witnesses and the 1962 witness, the Good Friday prayer for
the Jews changes in three ways: *Oremus et pro perfidis Judaeis* becomes *Oremus
et pro Iudaeis*; *qui etiam judaicam perfidiam a tua misericordia non repellis*
becomes *qui Iudaeos etiam a tua misericordia non repellis*; and the rubric
forbidding the kneeling is gone, replaced by *Oremus. Flectamus genua. Levate.*
A whole-file search of the 1962 scan for `perfid` returns nothing [verified].

The change is commonly attributed to John XXIII in 1959. **No instrument for it
was found in this corpus, so no station carries it**, and all three units are
recorded `unrecorded` — removed from the liturgy at that point, with a marker
saying the state is not established. The rule bit hard on a change everyone
knows, and that is the rule working.

### 7.4 The encoding the brief asked for cannot be derived from these scans

Section 6 is the measurement. Addressing text by what it is requires the unit
labels and the unit texts, and these text layers carry neither reliably, with
the failures concentrated on the ceremonial units. **The re-encoding has to be
read off page images.** The tracer's 38 units took a working day of targeted
searching across three scans to establish at the level of "label and citation
read, words sometimes not"; the four Holy Week liturgies hold on the order of
170 propers in this repository's own 1962 index.

### 7.5 The scan is not the book

Lines 134 to 780 of the 1962 text layer are not the missal. They are polemical
matter from a body calling itself The Fatima Movement, inserted ahead of the
title page at line 816 [sourced]. **A generator that slices by line window and
calls the result the book would publish that material as the Missale Romanum.**

### 7.6 Two stations have no Holy Week at all

`quo-primum-1570` and `cum-sanctissimum-1604` commit their act records and no
liturgy. Every unit enters at `si-quid-est-1634`, because the earliest witness
read for any unit is the 1862 Pustet and the latest act it attests is Urban
VIII's revision. The two 1570 and 1604 scans are two-column and their OCR
interleaves the columns, so Holy Week is locatable in them and not readable unit
by unit.

The history shows what was read, not what existed, and it shows it by being
visibly empty at the top.

---

## 8. Commit dates: keep the ten-thousand-year shift

The corpus this drew on shifts commit dates 10,000 years forward, so every
commit reads year 11570. That looked like a defect worth removing. It is not,
and the reason is measurable [verified, git 2.55]:

- `git commit` and `git commit-tree` **refuse** a pre-1970 date outright:
  `fatal: invalid date format: 1570-07-14T12:00:00+0000`, and the same for a raw
  negative epoch.
- Writing the object directly with `git hash-object --literally` succeeds, and
  the result is broken: `git fsck --strict` reports
  `badDate: invalid author/committer line`, and `%ad`, `%ai` and `%at` all print
  **empty** under every date format.

So a true 1570 date cannot be stored in a way any tool will display. Given a
shift is forced, 10,000 years is the right one: a shift small enough to look
plausible would be read as a real date, and 11570 cannot be mistaken for
anything. The true date is carried in the tree, in the commit subject line, and
in an `Act-date` trailer, so nothing depends on reading the stamp.

Recorded here rather than left to be re-derived, since it looks wrong and is
right.

---

## 9. Where the encoding lives, and why not beside the calendars

`src/sources/inventories/roman-holy-week-acts-v1.toml`, which is not where a
recension belongs. The constraints, each verified:

- `check-calendar-masses` reads every `.yaml` under `src/sources/calendars` as a
  mass index, and `scripts/_calendars.py` makes an unrecognised schema in a
  calendar directory a **hard failure** by design.
- `source-library validate` rejects any file under `src/sources` outside its own
  schema, **except** `.md` and `.toml` under `inventories/`.
- A new calendar directory would also be discovered by `calendar-days`,
  `calendar-rubrics`, the census, the harvest corpus and the browser's missal
  control, none of which a tracer is ready to answer to.

`source-library validate` and `source-inventory check` both pass with the file
in place [verified]. When the shape is settled, its home is a calendar-scoped
companion schema registered in `COMPANION_SCHEMAS`, which is the extension point
`scripts/_calendars.py` documents for exactly this.

**No canonical source manifests were created.** Adding one blocks
`source-family-migration refresh` and requires every family with canonical IDs
to be re-reviewed. A tracer should not levy that. The editions are identified in
the encoding by human-readable citation and artifact line number, and
canonicalising them is the next step, not this one.

---

## 10. What this proved, and what to do next

**The shape works.** Twelve acts, two lines that never rejoin, one merge that
cites its reception, one edge that admits it crosses an unrepresented station,
three units whose state is honestly unknown, and diffs a reader can read. All
seven departure kinds were needed. Git's rename detection carries the hard one
for free.

**The blocker is not the model. It is the evidence.** These OCR text layers
cannot support the unit-level encoding the model requires, and the tracer's own
measurements say so quantitatively rather than as an impression.

So, in order:

1. **Read Holy Week off page images**, for the 1920 and one pre-1955 witness at
   minimum. The tracer's `read_from` field is already there to be upgraded from
   `ocr-only` to `page-image`, and `check` already refuses a `page-image` claim
   without a collation date.
2. ~~**Find or refuse the 1962 promulgating decree.**~~ **DONE, 2026-08-01, and
   it was never missing.** It stands at page 2 of the Vatican typical edition,
   in a facsimile this repository already held, and a passage record had already
   asserted it six days before this tracer ran. See the correction box in §7.2.
   The replacement task is narrower and harder: **make a corpus-bounded negative
   look like one in the field that records it**, so that `not-found` cannot again
   be read as a claim about the tree.
3. **Settle the pre-1955 branch question.** Either an act permitting the older
   Holy Week's continued use is citable, in which case the branch is drawn, or
   it is not, in which case the current silence is correct and should be
   recorded as a settled negative rather than an open one.
4. **Then move the encoding beside the calendars**, as a companion schema, and
   only then widen past Holy Week.

Not, in any order: enlarging the corpus, adding more editions, or drawing more
edges. The tracer's finding is that the edges are the expensive part and the
scans are the weak part, and neither gets better by adding books.

---

# Part two: the wider slice, 1484 to 2023

Written 2026-08-01, on top of everything above. Part one is a report on twelve
acts of one week and is left exactly as it stood; nothing in it is edited to
match what follows, because a report that quietly grows to fit a later finding
stops being evidence of what was known when.

The wider slice is `src/sources/inventories/latin-missal-acts-v1.toml`. It
**extends** the Holy Week file rather than copying it, and adds fifty-nine
stations on seventeen lines: the Tridentine acts that stand before Quo primum,
the Roman line down to the emended reprint of 2008, the acts governing which
missal may be used, the Ordinary of the Mass as base units, and fifteen lines
for the uses and the order rites.

| | |
| --- | --- |
| stations | 59 — 33 promulgated, 26 printed |
| lines | 17, of which 15 begin at a root |
| edges | act-states-it 23, use-continuity 12, line-order 8, book-states-it 2 |
| witnesses | 41 |
| base units | 53 — the 38 of Holy Week and 16 of the Ordo Missae, less one |
| repositories searched | Internet Archive, Bavarian State Library; Gallica unreachable |

## 11. The rule is amended, and the amendment is narrow

**A printing may be a station.** §1 of part one says the station is the act and
never the book, and gives the reason: two printings of one prayer differ
constantly with no act behind the difference, so a history keyed on books
publishes scanner artefacts as liturgical change. That reason is unchanged and
this document still holds it. What the unamended rule could not do is carry a
missal for which no act has been located, and before Trent that is most of them.
Refusing them is not neutrality — it is a record silent about books that exist.

The amendment is owned by `time-machine.md` Rule 1, which states it and its four
conditions; this document keeps the vocabulary and what the tracer measured
under it. The two agree as written, which is exactly when a second copy is
cheapest to remove — if they ever differ, Rule 1 governs.

So every station declares which kind it is, and these are the settled words:

| `station_kind` | what it says |
| --- | --- |
| `promulgated` | an act stands behind it and its instrument is cited |
| `printed` | a missal survives and **no act is claimed** |

Four things keep the exception narrow, and `act-history check` enforces all
four:

- A `printed` station **may not name an instrument**. If an act was located, the
  station is promulgated.
- Its `act_citation` must be `none-claimed`, a value only it may use.
  **`none-claimed` is not `not-found`**: not-found means an instrument is
  believed to exist and nobody has read it, and the 1971 emended reprint is
  exactly that; none-claimed means no instrument is asserted at all.
- It must name the `printing` it stands on, and that must be a declared witness.
- It must say in `distinct_edition_basis` why it is a **distinct edition** and
  not a reprint or a rescan of one already carried. Two Internet Archive items
  of one printing are one witness and one station; four such mirrors are
  recorded on their witness rows in the wider slice rather than given stations.

**It reads as the weaker claim everywhere, including where it is cheapest to
hide it.** The commit subject begins `[printed]`, because the subject is the
only part of a commit `git log --oneline` and a GitHub commit list show, and a
weaker station that reads identically to a stronger one in the one view
everybody uses is a claim laundered by a renderer. The body then carries five
lines saying what is not being asserted.

**The two cases part one caught would still be caught.** The 1862 Pustet and the
1962 Benziger are printings *conformed to a typical edition* — an act stands
behind each — so they remain witnesses and are not eligible to be stations at
all. The amendment reaches only books for which nothing was found.

## 12. Every edge declares what it rests on

The danger the old rule guarded against has moved from the stations to the
edges, and is guarded there. A chain of printings ordered by date is not a chain
of descent, so `parent_kind` is required on every edge and is ordered by
strength:

| `parent_kind` | what the edge asserts |
| --- | --- |
| `act-states-it` | an instrument's text draws the edge — its own, or a later act reciting both in order |
| `book-states-it` | a title page or colophon names what the book follows |
| `attributed` | a scholarly attribution, cited to its source; never a bare inference |
| `use-continuity` | two **printings** declare the same use and this is their order. **It does not assert that the later was set from the earlier.** Requires `use_declared` |
| `line-order` | two **acts** stand on one line in this order and nothing in either names the other |

**Where descent is unknown the station is a root, and many roots is the honest
shape.** Fifteen of the seventeen lines begin at one. A single trunk joining the
pre-Tridentine printings would read better and would be a fabrication.

Two edges are worth reading as specimens. `quo-primum-1570` **is no longer a
root**: the bull's own opening recites the Tridentine decree committing the
missal to the Pope, so an `act-states-it` edge runs from Session XXV of 1563 —
and part one's root basis is kept and printed under *why this was formerly a
root*, not deleted. And the 1561 Venice printing on the pre-Tridentine line was
printed by Giovanni Varisco, **the same man who printed the 1570 Venice
edition** — a fact recorded on the witness row and drawn as no edge at all,
because nothing about the Tridentine missal descends through a Venetian press.

## 13. Paths sort in the order the thing has

`acts/` and `witnesses/` are directories a reader browses on GitHub, and a
listing of a history that reads alphabetically hides the one property a history
has. Every per-act and per-witness path takes its date as a prefix:

```
acts/1562-09-17-tridentinum-sessio-xxii.txt
acts/1570-07-14-quo-primum.txt
witnesses/1862-pustet.txt
witnesses/1970-missale-romanum-typica.txt
```

This is the convention `guidance/sources.md` settles for scripture — lowercase
paths, the ordering fact as a zero-padded prefix — keyed on date instead of canon
position. Three boundaries, and they are the whole of it:

1. **The prefix is derived**, in one function, from the date already in the
   record, and is never typed beside it. Two copies of one fact are a prediction
   that they will differ.
2. **A path is not an identity.** The eight witness ids inherited from part one
   are not renamed: several are also edition ids under `src/sources/works`, and
   re-keying a record so a listing sorts would break that alignment to fix a
   filename. Their paths are prefixed all the same, because the prefix comes
   from `printed` and not from the id. New ids in the wider slice do lead with
   their year, and `sorted_name` is idempotent, so nothing is prefixed twice.
3. **No date is invented so that a name will sort.** `date` is written to the
   precision the record has — `1497` for a book dated only by its year, `1971`
   for a reprint whose leaf gives no month — and `date_precision` is **derived**
   from it, with `check` refusing a stated precision that disagrees. Twenty-nine
   stations carry year-only dates and not one has a fabricated day.

The derived fragment names are published on the map spine as `station_path` and
`state_path`, so the page reads a name rather than building one.

## 14. Commonality, computed, and the two ways to read it wrong

This is the reason the Git shape earns its keep. *What did Sarum and Rome share
before they diverged* is not a question anyone should answer by writing a table
— a hand-written table beside a derived one is a second source of truth, and
this project has already been bitten by exactly that. It is a merge-base query.

`act-history commonality [LINE LINE]` answers it, and **proves its own answer**:
the shared base is derived from the act graph, `git merge-base --all` is then run
on the emitted repository, and the verb *raises* if the two disagree rather than
reporting. The same derivation is written to the map spine as `commonality`.

Two halves, and they must not be run together:

**The shared base is about ACTS.** Measured [verified]:

```
$ act-history commonality --source ...latin-missal-acts-v1.toml typica usus-antiquior
typica / usus-antiquior
  shared base : editio-typica-1962
  units       : 27 identical, 3 differing, 0 only in typica, 11 only in usus-antiquior

$ act-history commonality --source ...latin-missal-acts-v1.toml sarum typica
sarum / typica
  shared base : NONE: no act stands behind both
```

The first is a real answer: the two lines part at the 1962 typical edition, and
eleven units of the Ordinary stand on the older line and not on the newer, with
three more differing — the whole postconciliar divergence this slice carries,
computed rather than asserted. The second is **also** a real answer. Sarum and
Rome share no act in this record because none was located, and the graph says so
by drawing no edge.

**The divergence is about TEXT**, and here the reading runs the other way. Two
lines with no shared act may still hold the same prayer, and agreement without an
edge is the most interesting thing this shape can show: inheritance older than
anything the record carries. **The wider slice cannot show it yet.** No unit of
any use has been read, so every use line's tree is empty and the verb reports
zero units in common with everything — a statement about what has been
transcribed and about nothing else. A reader who took it for a statement about
the rites would have it exactly backwards, and the slice says so in its own
`commonality_reading` block.

## 15. What the wider pull measured

**A count is not a corpus.** `title:(missale) AND year:[1450 TO 1570]` returns
215 Internet Archive items [verified]. A large share are single-leaf photographs
of *one* manuscript, catalogued one folio to an item; another large share are
EEBO microfilm reels. One of those reels is in the slice and carries its own
measurement: 415 images, **127,736 bytes of text layer** — about 300 bytes a
page, against ten times that for the fresh scans beside it.

**A negative belongs to a repository and to a spelling.** The missal acquisition
audit recorded that no Carthusian missal is on the Internet Archive under
`cartusiense`, `cartusiensis`, `cartusianum` or `chartreux`. True, and too
strong: `carthusiense`, the same word with an h, returns a whole 1620 printing
[verified]. The audit had written that lesson two paragraphs earlier — about a
different catalogue. **An alias set must be applied to every repository
searched, not to the one where it was discovered.**

**A whole-file search is a search for a typesetting decision unless it is
normalised.** The 1970 typical edition prints `Oráte, fratres`; a literal search
for `Orate, fratres` returns zero and the prayer is on the page. Every negative
in the wider slice was run through a normalisation that strips diacritics, folds
the ae and oe ligatures and lowercases. **Any negative in this project taken
with a literal search should be re-run before it is believed.**

**And a hit is not the unit.** Two searches in the wider slice returned exactly
one hit that was not the thing looked for, and both are recorded on their rows:
`iudica me deus et discerne` is in the 1970 book as an *entrance antiphon* for a
Sunday, not as the psalm at the foot of the altar; `suscipe sancte pater` is
there in the *Exsultet*, not as the Offertory prayer. A count-only search would
have reported both units as surviving. This is §1 of `the-shape.md` in its
smallest form.

**The drop capital is where OCR damage falls, and it is the worst place for it.**
The Ordo Missae is set in large type with rubricated initials, and the scanner
loses them: `"Pv eus, qui humanae` is *Deus*, `a&te, fratres` is *Orate*, `1n
principio` is *In principio*, `T av&bo` is *Lavabo*. An incipit is by definition
the first words of a prayer, so damage concentrated on initials is damage aimed
at exactly the thing an incipit is. The wider slice reproduces them as the scan
gives them, because correcting them would hide the measurement.

**Rights decide what may be copied, and a departure need not copy anything.**
The 1970 typical edition may be read here and may not be published. Every one of
the twelve departures recorded against it is therefore an *absence established
by search* or a slot whose new words are **withheld** — and `withheld` is a
first-class field, printed in the tree as `[incipit withheld: ...]`, because a
prayer whose words were never read and a prayer whose words may not be printed
must not render alike.

## 16. What is still open

1. **No unit of any use is read.** Fifteen lines carry stations, witnesses and
   descent, and no liturgy. Until that changes, `commonality` can report acts
   between rites and cannot report text. The first use to read is **Braga**: it
   is the only one where the book and both its promulgating instruments are in
   hand and publishable.
2. **Gallica was unreachable from this run**, and four rows the acquisition
   audit verified there the same day are carried as `[recorded]`. The Lyonnais
   line rests entirely on that, and is carried rather than dropped because
   dropping a use on a network failure is the error that audit had already
   corrected once.
3. **The reading vocabulary has no value for a born-digital delivery.** Summorum
   Pontificum and Traditionis custodes were fetched from vatican.va and their
   SHA-256 matched the artifacts this repository registered a week earlier,
   exactly — a stronger reading than any OCR in either slice — and both had to
   record `ocr-only`, because `page-image | ocr-only | not-read` has no better
   term. Flagged rather than fixed: adding a value changes a vocabulary two
   files share.
4. **The Munda cor meum is `unrecorded` and should not stay so.** The 1962
   witness prints it as a cross-reference at the place it was read, so its words
   were never read there, and it cannot be compared with the 1970 text that
   plainly survives. The fix is to read it where the book actually prints it.
5. **Part one's item 4 still stands**: move the encoding beside the calendars as
   a companion schema. It is now more work and more overdue.

And part one's closing warning is **withdrawn in one respect and upheld in the
other**. It said: *not, in any order: enlarging the corpus, adding more editions,
or drawing more edges.* The corpus was enlarged and the edges were drawn, on the
maintainer's ruling, and the warning was right about which half is expensive:
the books were cheap and the edges cost the whole of the work. Every one of the
fifty-nine stations took a search; every one of the thirty-three edges took a
sentence somebody had written down, and where no such sentence existed the
station is a root.

---

## 17. The printed map's source, and the step this machine cannot run

Built 2026-08-01 and extended 2026-08-02 with the apparatus and the monochrome
grammar, on `time-machine.md` §9. That section settled the route and this records
only what was built to it and what it does not do.

**`tools/act-history plate` writes the plate's DOT, and nothing else.**

```
tools/act-history plate --source src/sources/inventories/latin-missal-acts-v1.toml \
    --out build/act-history/plate
```

writes `build/act-history/plate/<slice>.dot` — untracked, like the generated
repository, because it is derived from the inventory in one pass. It runs on all
three slices. [verified]

**It is a verb and not a tool, because Rule 5 says so.** The interactive map,
the git repository and the plate come off one generator. A second program
reading the same inventory would be a restatement, and this repository's
standing finding is that restatements drift.

### What is in the file

`octi` reads a DOT whose nodes carry `pos="x,y"` as plain Cartesian doubles, so
an abstract graph needs no geography [sourced, §9].

- **x is the date, y is the tradition lane.** Both are written into `pos`.
- **A node is a station.** It carries `date` at the record's own precision with
  `date_precision` beside it, `approximate="~"` where that precision is not a
  day, `line`, `lane`, `station_kind`, `act_citation`, `title`, `authority`,
  `instrument`, its line's `texture`, `grey` and `color`, and a `role` of `root`,
  `through` or `interchange`, plus `terminus="true"` where nothing descends
  from it.
- **An edge is a descent**, written `parent -- child`, undirected. It carries
  `line` — always the child's line — `descent`, which is the `parent_kind` an
  edge already declares it rests on, the band's `texture`, `dasharray`, `grey`
  and `color`, the `strength` and `penwidth` that width channel gives that
  `descent`, and `fork="true"` where it crosses from one line to another.
  Stemmatology draws descent without arrowheads for the same reason this does:
  the direction is read off the axis.
- **The graph itself carries the apparatus**, in nine attributes, and the header
  carries the same nine blocks, the lane register with each line's texture and
  grey, and the counts — so the file says what it is without a second document.

**An edge takes the line of the station it arrives at.** That is what makes the
Rule 2 grammar fall out rather than be drawn: a fork is the one place a line
touches another line's station, an interchange is a station two edges of one
line arrive at — a documented reception, and `check` refuses one that cites
nothing — and every other crossing on the plate is two lines that meet nowhere.
`latin-missal` has 59 stations on 17 lines, 45 edges, 15 roots, 17 termini, two
forks, one interchange and five lines that are a single station and nothing
more. [verified]

### The one choice §9 said must be made explicitly

Strict octilinearity and strictly time-proportional edge length cannot both
hold, and no published diagram is both. **This picks monotone over
proportional.** Between consecutive distinct dates the abscissa advances by four
units a year, clamped to `[25, 400]`; lanes are 100 apart. So the widest gap on
the plate is sixteen times the narrowest and not thirty-eight thousand times it,
which is what makes §3's requirement — four centuries and four years must both
read — a property of the file rather than a hope about the renderer. `octi` will
move everything; what the positions usefully tell it is the order.

The lane order is **derived and not the `lines` table's order**, which is an
editorial arrangement Rule 3 will not let decide a drawing: roots enter in the
order they enter the record, and a line born at a fork follows the line it was
born from.

### The apparatus, and where every line of it comes from

§9 lists what the ICS chronostratigraphic chart carries **on the plate**, and the
DOT now carries the same nine blocks — in the graph's own attributes, where the
labelling pass will read them off the graph it is labelling, and in the header,
where a person reading the file reads them. Every number in them is a count of
what the file itself carries, because a legend typed beside the emitter drifts
from it the first time a texture moves.

| block | what it says | read from |
| --- | --- | --- |
| `edition` | the release, the slice, its `recorded_on`, the schema | `release/public-alpha.json` and the slice's own header |
| `provenance` | the record type, the vocabulary, every file read, each file's SHA-256, the counts, and what each class of record was read from | the loaded slice |
| `exceptions` | printed stations, not-found instruments, roots, edges resting on order alone, descents through unrepresented acts, OCR-only and unread records, withheld text, unestablished effects | counted, and printed only where there are any |
| `epistemic` | `~`, defined: the record holds only the year or the month | `date_precision`, and the mark rides on the station in `approximate` |
| `legend` | station roles, terminus, station kinds, forks, and why descent has no arrowhead | counted off the graph |
| `grammar` | the monochrome key, below | the texture table |
| `url` | the interactive twin, and why the pin is not in it | the page that is actually there, and the origin |
| `cite` | the "To cite:" line, and the refusal of Priestley's refusal | the release and the slice |
| `unmarked` | what this sheet does **not** mark | §9's own list of what nobody automates |

**The edition stamp is the release's and never the build machine's.** Nothing in
the emitter reads a clock: a build timestamp would put a different byte in the
artifact every run and destroy the reproducibility Rule 5 asks for. `release_id`
is read from the release record and `recorded_on` from the slice; a slice that
declares no `recorded_on` — `code-of-canon-law` is one — **says so** rather than
being given a date. [verified]

**The version-pinned URL is two things, because a one-edition site cannot be
one.** §9 wants a URL pinned to a version; the published site serves whatever
was published last, so the URL names the twin and the **pin is the SHA-256 of
every file the slice was read from**, which `sha256sum` checks against the files
named. That is a stronger pin than a URL would have been: it names the bytes.
The origin is not typed here — it is read from the tool that publishes to it,
which is why `act-history` now declares `public-alpha` in its `requires`.

### Byte-identical, and nothing here reads a clock

Two runs produce identical bytes, and so do runs under a changed `TZ`, `LANG`,
`LC_ALL` and several `PYTHONHASHSEED` values including `random`. The abscissa is
integer arithmetic throughout for that reason, and the apparatus reads two files
and a release id rather than a date. [verified, and asserted in
`tests/tools/act-history.test`]

### The monochrome grammar separates eighteen, and six by dash alone

§9 measured TfL's black-and-white plate: **constant band width** for every line
so weight stays free for another dimension, differentiation by the band's
**internal texture** plus **three grey values**, 22 services with no colour at
all. This copies that and states its ceiling rather than implying one.

- **Six textures × three greys = eighteen lines separated.** `latin-missal` has
  seventeen, so no two lines on it are drawn alike. [verified]
- **The dash channel alone separates six**, and it is the channel that survives
  a photocopy. The greys carry the rest of the way and want the sheet printed
  rather than copied. A grammar claiming to separate seventeen by dashes would
  separate six.
- **Past eighteen the pairs repeat, and the file names which lines share one.**
  It does not claim a distinction it does not draw.
- **The key is on the lane, not the name.** The texture turns over fastest, so
  two lines sharing one stand at least six lanes apart — and lanes are adjacent
  exactly where the traditions were drawn adjacent, which is where a reader has
  to tell two bands apart while following one across a crossing. [verified in
  the test]

**Width is the second channel, and it is the one §9's constant band leaves
free.** The band says which line; the width says what the descent rests on:
`stated` where an instrument or the book itself draws the edge, `attributed`
where a cited scholar does, `sequence` where nothing does and two acts merely
stand in this order. **Three tiers over five declared `parent_kind` values**,
because five widths inside one band are not tellable apart and the exact kind
stays on the edge in `descent`.

That split is deliberate. Priestley put uncertainty in the dash channel because
he had one line per item; here the dash channel is spent on identity, so the
uncertainty grammar moved to width. One channel for *which*, one for *how well
attested*, and neither reading the other's mark.

### What this machine did not do

**`octi` is not installed here, and this repository neither ships nor vendors
it.** So the SVG was not produced and no step silently pretended to. To render:

```
octi < build/act-history/plate/latin-missal.dot | transitmap > latin-missal.svg
```

LOOM, GPL-3.0, <https://github.com/ad-freiburg/loom>. That `octi` accepts the
DOT is §9's finding [sourced]; the exact flag set of that pipeline is **not
[verified] here**, because nothing here could run it. The same command is in
every emitted file's header, from one string in the tool, so there is no second
copy to drift.

### What remains of the printed map, and why none of it is the generator's alone

Three things remain, and the sheet **says so on itself**, under `unmarked`. A
reader is told what this drawing does not mark rather than left to assume it
does — which is §9's status disclaimer, discharged by naming the three.

1. **Labelling.** §9 found that labelling, not layout, is where automation still
   fails, and that neither `octi` nor TikZ will do it. The nodes carry
   everything a label must say and nothing places one. This is the next unit and
   the largest, and it is the one of the three that is squarely the generator's.
2. **The mark for a crossing that is not an interchange.** §6 records that no
   published metro map has a grammar separating "these lines meet" from "these
   lines merely cross", and §9 measured that the same interchange drawn as a dot
   rather than as a long link *changed which transfers passengers made*. The DOT
   distinguishes the two structurally; drawing them apart means **inventing
   notation**, and §9 is explicit that invented notation must be defined in a
   legend and **not claimed as conventional**. That is a human ruling, not a
   generator's, and nothing here invents one on its own authority.
3. **Sheet size.** §9's measurement puts 40 nodes on A3, 100 on A2 and 200 on
   A1, with 15–25 per cent reserved for the key, so `latin-missal` at 59 is an
   A2 sheet. Which sheet to print is a layout decision; the plate states the
   measurement and sets nothing.

### One more restatement, found while landing this

This document's own "What was built" table, at the top, carries a hand-typed
`size` row — *12 acts, 2 lines, N witnesses…* — beside a `check` that computes
exactly those numbers, with nothing comparing the two. A concurrent lane added a
witness and the row went stale the moment it landed; it has been corrected here,
**by hand, which is the defect repeating rather than being fixed.** It is the
same shape as the lookup table this repository already had to delete: a
hand-typed restatement sitting beside a derived value with no check between
them. The general fix — the row read out of `check --json`, or a test that
compares the two — is not attempted in this unit, and this note exists so the
next one does not think the digit was the problem.

## 18. Whether these repositories may be published: the decision record

Measured 2026-08-02. `guidance/sources.md:389` forbids a dedicated data
repository "until measured source size or rights constraints justify the
contribution and distribution cost", and until this measurement no one had
measured either. The record is
**`src/sources/inventories/act-history-repository-publication-v1.toml`**, and
it is the file to read before anything is published. This section records that
it exists and what it decided; it does not restate it, because a restatement
beside a record is a prediction that the two will disagree.

**It authorizes nothing.** No repository was created, no remote configured and
nothing pushed to write it. Registering a repository is the maintainer's act.

Four things in it change what this document says elsewhere.

1. **Size justifies nothing, and measuring it argues the other way.** The three
   emitted repositories pack to 42 KB, 136 KB and 175 KB. The tracked browser
   data this repository already serves for the same three slices is 211 KB,
   503 KB and 3.0 MB. The emitted repository is the *smaller* artifact in every
   case. §9's "1.3 MB" was `du -sh` over 148 loose objects — a measurement of
   filesystem block rounding, not of the artifact, which is 78,602 content
   bytes. [verified]
2. **The justification that survives is consumability, and the claim it rests on
   had to be corrected before it could be used.** A bare repository's files
   *can* be committed into this one, and `git log` inside that directory *does*
   work — until someone clones. In a clone, `refs/` is absent because git does
   not track empty directories, discovery fails, and `git log` silently answers
   with *this* repository's history instead. `mkdir refs` repairs it completely.
   The in-tree route is therefore either refused by git (a non-bare repository
   becomes a gitlink) or silently wrong for every reader who clones. [verified]
3. **`withheld` survives into the commit objects — and nothing enforces it.**
   237 of 237 post-1929 canon blobs across all 47 commits carry the
   `[text withheld: …]` banner and none carries words. But `check` has no guard
   against a row carrying both `withheld` and `text`: a probe adding one such
   line passed `check` with zero problems and emitted the protected words into a
   commit object *underneath the banner saying they were not there*. The
   `interpretations` table has that guard; `units` and `departures` do not.
   [verified]
4. **§8 kept the ten-thousand-year shift on a hazard analysis that was half
   written down.** A fresh emit passes `git fsck --strict`. Run `git gc` — which
   writes a commit-graph by default — and `fsck --strict` exits 16 and reports
   every commit, because the commit-graph stores a date in 34 bits and the
   shifted stamps are eighteen times too large. It is not cosmetic:
   `rev-list --date-order` then puts a 1570 commit ahead of a 1962 one.
   `gc.writeCommitGraph=false` leaves it clean locally, and what a hosting
   service does is recorded as an open question rather than guessed. [verified]

**The decision, per slice.** `roman-holy-week` may be published, private or
public, once three written conditions are met; it carries no withheld row at
all, so the missing guard is not load-bearing for it. `latin-missal` and
`code-of-canon-law` may not be published in *any* visibility until the guard
lands — 2 rows and 174 rows respectively rest on a withholding the tool does not
enforce, and a git history is the one artifact here from which a mistake cannot
be withdrawn.

**Private answers three of the four hazards and not the fourth.** Consumability,
date presentation and replaceability are all satisfied by a private repository
plus a written authority. Rights are not: `guidance/sources.md:382-384` draws
its line at whether restricted bytes *entered* Git and a build product, and a
private repository is Git and an emitted repository is a build product. Privacy
changes who can read a leak, not whether it happened.

The conditions, the open questions and the corrections are in the record. The
one that reaches beyond it: a published derived repository needs its own written
authority in `PROJECT-WORK.md` saying it is a build output replaced in full,
because every correction to it is a force-push — one word changed in one act
rewrote 10 of 12 commit ids, and renaming the source inventory rewrote all 12,
since every commit's README names the file it was built from. [verified]
