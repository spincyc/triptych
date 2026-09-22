# Research scope — Eighteenth Sunday after Pentecost (1962 Roman Rite)

The audit record for the canonical leaf
`liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost`. It holds
the checked sources and loci, the passage-by-passage reception matrix, the material
disagreements preserved, the negative results, the chronology audit, the rights
boundary, and the evidence bounds that later stages must respect. It is not study
prose and carries no reader-facing argument; the proposed readings are in
`research/interpretations.md`, the text control in `propers/verified.md`.

Resolved for the `proper-study` v6 production of the Claude 1962 leaf, run
`71b6f89518984232`, seeded at commit `fa5355745b5e973584f047a7f59a20ad22676d64`.
**Re-entered on 2026-09-22 after research review.** The re-entry swept the
repository's own registered holdings before recording any witness as unreached —
Jerome at PL 26, Hilary's CSEL 22 *Tractatus*, Cassiodorus on all three appointed
psalms, and the registered gregorien.info report of the Sextuplex — registered
what the library did not yet hold, and resolved both of Wilson's Gelasian
cross-references and both dated occurrence witnesses. Sections 2.1, 2.3, 3.2–3.9,
4.1–4.3, 5.1, 5.2, 6, 7.2, 8.1, 9.1 and 10 carry the result.

**Re-entered a second time on 2026-09-22**, after a second research review found
that the first re-entry had still swept by work record and not by artifact
coverage. `tools/commentary-work-index discover` was run for **every** appointed
locus — Ps 95:8, Ps 101:16, Ps 121:1, Ps 121:7, Mt 9:1, 1 Cor 1:4, Ex 24:4 and
Sir 36:18 — and for each lead it returned, the registered collected-volume and
whole-volume artifacts were checked for the work before anything was recorded as
unreached. That reached Chrysostom and Theodoret on Ps 121 in Greek, Theodoret and
Athanasius on Pss 95 and 101, Theodoret on 1 Cor 1:4–8, Bellarmine on all three
psalms, Augustine's own Latin in PL 37 (including Ps 121, which no tracked Latin
carries), Aquinas's lectura on Mt 9:1–8, Cornelius a Lapide on Ex 24:4–8, and — as
documented reception of the compilation, not as exegesis — Rupert of Deutz and
Guéranger on this Sunday's Mass. The new § 2.7, § 3.11, § 4.6 and § 4.7, and the
rewritten §§ 3.2–3.8, 4.1–4.5, 5.2, 6.3 and 10, carry the result.
`ARGS.research_handoff` is `none`; no handoff dossier was supplied. Nothing below
is taken from the other provider's leaves, from any postconciliar record, or from
this provider's neighbouring Sundays, except where a neighbouring Sunday's printed
text on the same page is itself the evidence and is named as such.

## Contents

1. [The formulary and the facts the research rests on](#1-the-formulary-and-the-facts-the-research-rests-on)
2. [How the formulary was assembled: evidence that its parts travelled separately](#2-how-the-formulary-was-assembled-evidence-that-its-parts-travelled-separately)
3. [Passage-by-passage reception matrix](#3-passage-by-passage-reception-matrix)
4. [Material disagreements preserved](#4-material-disagreements-preserved)
5. [Negative results and unreached corpora](#5-negative-results-and-unreached-corpora)
6. [Witness register](#6-witness-register)
7. [Scriptural chronology audit](#7-scriptural-chronology-audit)
8. [Calendar, rubrics and occurrence: what this stage re-checked](#8-calendar-rubrics-and-occurrence-what-this-stage-re-checked)
9. [Rights, quotation and publication bounds](#9-rights-quotation-and-publication-bounds)
10. [Evidence bounds and open items for later stages](#10-evidence-bounds-and-open-items-for-later-stages)

---

## 1. The formulary and the facts the research rests on

Ten elements, no option, no alternative, no substitute, one oration of each kind.
Printed pp. 410–411 of the 1962 typical edition, marginal nos. 1669–1678, all
collated word for word at the pages' native 500 ppi. `propers/verified.md` is the
control; this record does not repeat the Latin.

| Key | Element | Direct biblical locus | Character |
| --- | --- | --- | --- |
| `introit` | *Da pacem, Dómine* + Ps 121:1 | Ecclus 36:18; Ps 121:1 | Antiphon **not** a quotation of its cited verse; psalm verse verbatim |
| `collect` | *Dírigat corda nostra* | — | Composed oration |
| `epistle` | 1 Cor 1:4–8 | 1 Cor 1:4–8 | Verbatim, with the liturgical address |
| `gradual` | Ps 121:1 + 7 | Ps 121:1, 7 | Verbatim |
| `alleluia` | Ps 101:16 | Ps 101:16 | Verbatim less the opening connective |
| `gospel` | Mt 9:1–8 | Mt 9:1–8 | Verbatim, with the liturgical opening |
| `offertory` | *Sanctificávit Móyses* | cited Ex 24:4–5 | **A compilation**, not a quotation |
| `secret` | *Deus, qui nos, per huius sacrifícii* | — | Composed oration |
| `communion` | Ps 95:8–9 | Ps 95:8–9 | One word divergent (`in aula sancta`) |
| `postcommunion` | *Grátias tibi reférimus* | — | Composed oration |

### 1.1 Threads inside the appointed text

These are textual observations, each verifiable by reading the ten elements
together. They are not claims about a compiler.

- **Peace.** `Da pacem` (Introit), `Fiat pax in virtúte tua` (Gradual verse). Two
  of the ten elements ask for peace in their first words.
- **The house and its courts.** `in domum Dómini íbimus` (Introit verse and
  Gradual respond, the same verse appointed twice), `introíte in átria eius …
  in aula sancta eius` (Communion), `abundántia in túrribus tuis` (Gradual verse).
- **The altar and the sacrifice.** `Sanctificávit Móyses altáre` and `fecit
  sacrifícium vespertínum` (Offertory), `huius sacrifícii veneránda commércia`
  (Secret), `Tóllite hóstias` (Communion), `sacro múnere vegetáti`
  (Postcommunion).
- **What we cannot do.** `tibi sine te placére non póssumus` (Collect); the
  paralytic who is carried, laid down, and told to rise (Gospel); `grátia Dei,
  quæ data est vobis` and `nihil vobis desit in ulla grátia` (Epistle).
- **Thanksgiving at both ends.** `Grátias ago Deo meo semper pro vobis`
  (Epistle, the lection's first clause) and `Grátias tibi reférimus`
  (Postcommunion, the formulary's last prayer).
- **Waiting and the day.** `sustinéntibus te` (Introit), `exspectántibus
  revelatiónem … in die advéntus Dómini nostri Iesu Christi` (Epistle).
- **The nations.** `Timébunt gentes nomen tuum, Dómine, et omnes reges terræ`
  (Alleluia) — the only element that looks outward.

### 1.2 Threads in the unsung context of the appointed verses

Read in the complete biblical context, as the profile requires, three of the
psalms carry a frame the antiphon does not print. These are facts about the
psalms, recorded here because §3's exegesis turns on them.

- **Ps 95** is titled, in the Clementine, *Canticum ipsi David, quando domus
  ædificabatur post captivitatem* — "when the house was being built after the
  captivity". The Communion's two clauses are vv. 8b–9a of that psalm.
- **Ps 101** is titled *Oratio pauperis, cum anxius fuerit, et in conspectu
  Domini effuderit precem suam*. The Alleluia verse (v. 16) stands immediately
  after *Tu exsurgens misereberis Sion* (v. 14) and immediately before *quia
  ædificavit Dominus Sion, et videbitur in gloria sua* (v. 17).
- **Ps 121** is titled *Canticum graduum* and is one of the Songs of Ascents
  (Ps 119–133 in the Vulgate's numbering, Ps 120–134 in the Hebrew). The
  Gradual's respond and verse are vv. 1 and 7 of that ascent song; v. 9, which
  neither element prints, reads *Propter domum Domini Dei nostri, quæsivi bona
  tibi.*
- **1 Cor 1:4–8** is the thanksgiving of a letter whose next paragraph
  (vv. 10–13) is about schisms at Corinth. The lection stops one verse before
  *Fidelis Deus* (v. 9) and four before *Obsecro autem vos, fratres*.
- **Mt 9:1–8** follows the Gadarene demoniacs (Mt 8:28–34) and is followed by the
  call of Matthew (9:9). The Gospel's `civitátem suam` is the point at issue
  between the witnesses in §4.1.

### 1.3 Threads that are not in the appointed text

Recorded so that a later stage does not import them:

- **No Tract and no Sequence.** The Missal prints neither; the Alleluia stands
  alone between Epistle and Gospel.
- **No proper preface of its own.** The Trinity Preface is appointed by rubric
  (printed direction after the Secret; RGMR 494 b), not chosen.
- **No second oration, no blessing, no *Oratio super populum*, no proper
  *Communicantes* or *Hanc igitur*.**
- **The word *paralyticus* occurs nowhere but the Gospel**, and *peccatum* /
  *peccata* nowhere but the Gospel. Forgiveness is named once in the formulary.

---

## 2. How the formulary was assembled: evidence that its parts travelled separately

That a Mass formulary is a liturgical compilation is settled once in the
three-document profile, `guidance/liturgy/propers-three-documents.md`, under
*The formulary is a compilation*, and is not re-derived here. What follows is recorded because it is a **specific
fact that changes a claim**: in the oldest Roman books this project holds, the
chants of this Sunday and the orations of this Sunday do not stand at the same
Sunday, and the orations stand at no Sunday at all.

### 2.1 The orations in the Old Gelasian

**Read on the page image of Wilson 1894, printed p. 232** (Internet Archive item
`LiberSacramentorumRomanaeEcclesiae`, leaf n324, 3407 × 5528 px, SHA-256
`4da337e05b14beed287181c66c743e104fb5ac2dfa9f06f019c8dbaa1aada354`; the leaf index
runs 92 ahead of the printed page, as the registered leaf-322 artifact records),
and in the registered optical layer
`artifact.catholic-church.sacramentarium-gelasianum-vetus.wilson-1894.ia-djvu-ocr-gelasiansacrame00wilsgoog`
(SHA-256 matched on fetch) at its physical lines 21548–21580.

Book III, section **XIV**, headed `ITEM ALIA MISSA` — **with no Sunday number** —
carries, in this order:

- Collect: *Dirigat corda nostra, Domine, quaesumus, tua miserationis operatio,
  quia tibi sine te placere non possumus.* (marginal sigla `R. S. Gerb. 186.
  Pam. 412. Men. 182.`)
- a **second** Collect: *Tuis, Domine, quaesumus, adesto supplicibus; et inter
  mundanae pravitatis insidias fragilitatem nostram sempiterna pietate
  prosequere.*
- Secreta: *Deus qui nos per huius sacrificii veneranda commercia unius
  summaeque divinitatis participes effecisti, praesta, quaesumus, ut sicut tuam
  cognoscimus veritatem, sic eam dignis moribus et mentibus assequamur.*
  (`R. S. Gerb. 186. Pam. 412. Men. 182. I. lix supra.`)
- Postcommun.: *Gratias tibi referimus, Domine, sacro munere vegetati, tuam
  misericordiam deprecantes, ut dignos eius nos participatione perficias.*
  (`R. S. Gerb. 186. Pam. 412. Men. 183. I. xciii supra.`)

Wilson's footnote to the section: *"This Missa is assigned by R. S. Gerb. to the
twenty-second Sunday after Pentecost: see the Missa for that Sunday in Men., and
that for the nineteenth Sunday in Pam."* The section immediately following, XV,
opens *Omnipotens et misericors Deus, universa nobis adversantia propitiatus
exclude* — the 1962's **Nineteenth** Sunday Collect; the section immediately
preceding carries *Da, quaesumus, Domine, populo tuo diabolica vitare contagia,
et te solum Dominum puro corde sectari* and *Maiestatem tuam, Domine, suppliciter
deprecamur* — the 1962's **Seventeenth** Sunday Collect and Secret, whose Missa
Wilson's footnote assigns *"to the twenty-first Sunday after Pentecost … see the
Missa for the eighteenth Sunday in Pam."*

Four variants in Wilson's apparatus bear directly on the 1962's own wording:

1. `efficis` (the 1962's reading) is the reading of R, S, Gerbert, Pamelius and
   Ménard; Wilson prints `effecisti` from V.
2. `dignis moribus et mentibus` is the reading of V here, R, S and Gerbert;
   Pamelius and Ménard read `mentibus ac moribus`; **V at Book I § lix omits
   `et mentibus`** — that is, reads `dignis moribus assequamur`, which is the
   1962's own reading.
3. `cognoscimus` (the 1962's reading) is V, R, S, Gerbert and Pamelius; Ménard
   reads `ut et tuam cognoscamus … et eam`; V at I. lix has `cognovimus`.
4. `eius nos` is V and S; `nos eius` (the 1962's order) is Gerbert, Pamelius and
   Ménard; R omits `nos`.

**Both cross-references in Wilson's margin at III. xiv resolve in the same optical
layer, and this stage resolved them.** The whole layer was re-fetched on
2026-09-22 and its SHA-256 recomputed and matched (`039123ca…684d84`, 1,098,845
bytes) before anything was read in it.

- **`I. xciii supra`, the Postcommunion.** *Gratias tibi referimus, Domine, sacro
  munere vegetati* stands a second time in Book I, at physical lines 15341–15344,
  as the Postcommun. of the Mass **`Orationes et preces in Dedicatione loci ubi
  prius fuit synagoga`** — the dedication of a place that had been a synagogue —
  with the marginal cross-reference `III. xiv` beside it. **The section number is
  settled, and by the edition's own table of contents rather than by the running
  heads.** The contents list at physical line 640 reads `xcili. Orat et Preces in
  Dedicatione lod ubi prius fuit Synagoga 141` — the scan's `xcili` and `lod` for
  *xciii* and *loci* — and the next entry, at line 642, `xciv. Orat et Preces in
  Dedicatione Fontis 149`; § xciv's own heading, `Orationes et preces in
  Dedicatione Fontis`, stands at line 15372, *after* the Postcommunion. So the
  Postcommunion is in § **xciii**, as Wilson's cross-reference at line 21582
  (`I. xciii`) says. The running heads are what misled: the head above printed
  p. 142 (line 15317) and the head above printed p. 143 (line 15381) **both** read
  `I. xciv.` — the scan prints `I.xdv.` for both — because this edition's
  compositor heads a page with the section it runs into. The page images of pp. 141–143 were not opened; nothing here needs
  them.
- **`I. lix supra`, the Secret.** *Deus, qui nos per huius sacrificii veneranda
  commercia* stands a second time in Book I, at physical lines 12585–12598, under
  the rubric `Secreta.` and carrying the marginal cross-reference `III. xiv`. The
  scan reads `Deus, qui nos per huiiis sacrificii veneranda commerda … unius
  summae* divinitatis partidpes efiecisti, praesta, quaesumus, ut sicut tuam
  cognovimus veritatem sic eam dignis moribus assequamur. Per.` — four OCR
  corruptions (`huiiis`, `commerda`, `partidpes`, `efiecisti`) and a stray
  asterisk, which is why a literal search on the ordinary spellings misses it
  (§ 5.1.6). **What it settles is textual, not bibliographic**: V at I. lix reads
  `cognovimus` and `dignis moribus` *without* `et mentibus`, exactly as Wilson's
  apparatus at III. xiv reports and exactly as the 1962 prints; the manuscript
  text, not the apparatus alone, now carries the 1962's own readings (§ 3.9).

### 2.2 The orations in the Gregorian Sacramentary

**Read on the page image of Wilson 1915, printed p. 175** (rendered at 300 dpi from
the tracked artifact
`artifact.catholic-church.sacramentarium-gregorianum-hadrianum.wilson-1915.ia-pdf-96fd93c7`,
SHA-256 `96fd93c73f8c9df47b6911981155b8b02cf2f2183ca6e87baad15128682d8681`,
PDF p. 233 of 432).

Section **CXXXVII**, headed `DOMINICA .XVIIII. POST PENTECOSTEN`, carries the same
three prayers in the same order — Collect *Dirigat corda nostra*, Super oblata
*Deus qui nos per huius sacrificii ueneranda commertia … unius summeque diuinitatis
participes efficis … dignis mentibus et moribus adsequamur*, Ad complendum
*Gratias tibi referimus domine sacro munere uegetati* — with the folio note
`[fo. 169v` inside the Collect. Wilson's apparatus records `cognoscimus
cognouimus O`. Section CXXXVI (`DOMINICA .XVIII.`) carries the 1962's Seventeenth
Sunday orations; section CXXXVIII (`DOMINICA .XX.`) carries the 1962's Nineteenth.

**So in the Hadrianum the whole oration-set of the 1962's Eighteenth Sunday stands
at the Nineteenth, and the run is displaced by one place across three consecutive
Sundays.**

### 2.3 The chants in the Hadrianum's cues

**Read on the page image of Wilson 1915, printed p. 174** (PDF p. 232). The chant
cues are printed as lettered footnotes attached to the section headings. Footnote
`b`, attached to section **CXXXV, `DOMINICA .XVII. POST PENTECOSTEN`**, reads:

> *Ant.* Da pacem domine. *Resp.* Letatus sum. *Off.* Sanctificauit moyses.
> Com. Tollite hostias. [(*All.* Qui?) posuit.]

That is this Sunday's Introit, Gradual, Offertory and Communion, as a set, in
liturgical order — attached to the **Seventeenth** Sunday, two places before the
Sunday whose orations they now share. Footnote `a` on the same page, attached to
CXXXIIII (`DOMINICA .XVI.`), reads *Ant.* Iustus es domine, *Resp.* Unam petii a
domino, *Off.* Oraui deum meum, Com. Uouete et reddite — the 1962's Seventeenth
Sunday Introit, Offertory and Communion, with a different Gradual. Footnote `a`
on p. 175, attached to CXXXVI (`DOMINICA .XVIII.`), reads *Ant.* Salus populi,
*Resp.* Dirigatur oratio me(a), *Off.* Si ambulauero, Com. Tu mandasti — the
1962's Nineteenth Sunday Introit and Gradual.

Two further facts about that cue:

- **The Alleluia is not this Sunday's.** Wilson prints it in brackets and with a
  query, `[(All. Qui?) posuit.]`. If the reading is *Qui posuit*, the verse is
  Vulgate Ps 147:3, *Qui posuit fines tuos pacem, et adipe frumenti satiat te*
  (checked in the tracked Clementine; the Vulgate's Ps 147 is vv. 12–20 of the
  Hebrew Ps 147, per the tracked psalm-numbering concordance). The 1962's
  Alleluia is Ps 101:16, *Timébunt gentes*. **Wilson's own brackets mark the cue
  as an addition and his query marks the reading as uncertain**; nothing here
  rests on the identification, and no manuscript was consulted.
- **The cues are not the sacramentary's own text.** They are marginal or added
  matter that Wilson prints as footnotes; this stage read them as Wilson prints
  them and made no judgment about the hand or the date that supplied them.

**A second, independent witness to the same chant-set, and it reports what Wilson
could only query.** The source library registers the gregorien.info chant database at
`edition.gregorien-info.gregorien-info-chant-database.web-2026-09-05`, whose
pages carry that database's reading of the six manuscripts Hesbert collated in
the *Antiphonale Missarum Sextuplex* — Monza (M), Rheinau (R), Mont-Blandin (B),
Compiègne (C), Corbie (K), Senlis (S). Two of its pages are registered artifacts
and both were re-fetched on 2026-09-22 and matched byte for byte
(`…calendar-ams-day-819-684af370`, `684af370…0224f7`, 7,190 bytes;
`…chant-8121-gradual-timebunt-gentes-72145226`, `72145226…10d6e0`, 20,959 bytes).
The database's AMS-calendar day for **Dominica XVIII post Pentecosten** is
day 823, which is *not* registered; it was read live on 2026-09-22, response
SHA-256 `43acf9bd8a7bd40d…` (full digest in § 6.2), and its neighbours 818 and
820–825 with it. What day 823 prints is this formulary's chant-set entire:

| AMS row | Chant | Books |
| --- | --- | --- |
| Introitus | *Da pacem Domine sustinentibus* | R B K |
| Graduale | *Convertere Domine…et deprecare* | M |
| Graduale | *Laetatus sum in his* | R B K S |
| Graduale | *Quis sicut Dominus Deus noster* | B |
| Versus alleluiaticus | *Laudate dominum quoniam benignus* | R |
| Versus alleluiaticus | *Qui posuit fines* | S |
| Offertorium | *Sanctificavit Moyses altare* | R B K S |
| Communio | *Tollite hostias et introite* | R B K S |

Three things follow, and each is bounded by what this evidence is.

1. **Wilson's queried Alleluia is confirmed as a reading.** His bracketed
   `[(All. Qui?) posuit.]` at the Hadrianum's Seventeenth-Sunday cue is, in this
   database's report of the Sextuplex, the Senlis alleluia *Qui posuit fines* at
   the Eighteenth Sunday. The identification § 2.3 refused to rest on is now
   reported independently; it is still a database's reading of a manuscript, not
   a collation of one.
2. **The 1962's Alleluia is not the early one.** No Sextuplex book gives
   *Timebunt gentes* as this Sunday's alleluia in that report; the two alleluia
   verses are *Laudate dominum quoniam benignus* (R) and *Qui posuit fines* (S).
   *Timebunt gentes* is there a **Gradual**, and the registered chant page for it
   carries the database's whole Hesbert citation line — *Antiphonale missarum
   sextuplex*, HESBERT, René-Jean, 1985, `nr.00 R; nr.26 M B C K S; nr.187 B;
   nr.188 K S; nr.189a B; nr.198 R B` — whose days that page names as Dominica V
   ante Nativitatem Domini, Dominica III post Epiphaniam, and the Fifteenth,
   Sixteenth, Seventeenth and Twenty-third Sundays after Pentecost. So the text
   the 1962 sings as an Alleluia is an old Roman chant, attested in all six
   books, that travelled as a Gradual and at other Sundays.
3. **The AMS numbering and the Hadrianum's do not line up.** Day 819, *Dominica
   XVII post Pentecosten*, carries *Iustus es Domine*, *Unam petii a Domino*,
   *Oravi Deum meum* and *Vovete et reddite* — the cue Wilson prints at the
   Hadrianum's section CXXXIIII, `DOMINICA .XVI.` (footnote `a`, p. 174). The
   chant-set of this Sunday therefore stands one place later in the Sextuplex
   books than in the Hadrianum's added cues, and at the Sunday number the 1962
   itself uses.

**What this does not establish.** Nothing here was read in a manuscript or in
Hesbert's printed collation; every siglum above is the gregorien.info database's
own report, which its registered artifact records call "an unverified lead until
collated against the manuscript or against Hesbert's printed *Antiphonale
Missarum Sextuplex*". Day 823 is besides an unregistered delivery. The bound is
recorded again at § 5.2 and § 10.5.

### 2.4 The Veronense: a clean negative

The registered optical layer
`artifact.catholic-church.sacramentarium-veronense.feltoe-1896.ia-djvu-ocr-sacramentariumle00cath`
(SHA-256 `7e7e82fe4e8990ec557a914b6ec768c99e174623f8acba606654280845cad21b`,
matched on fetch) was searched, by a diacritic- and case-insensitive literal
search over the whole file with `i/j` and `u/v` normalised, for `dirigat corda
nostra`, `sine te placere non possumus`, `ueneranda commercia`, `gratias tibi
referimus` and `sacro munere uegetati`. **None of this formulary's three orations
is in it.** `gratias tibi referimus` returns ten hits, every one of them a
different prayer (*Gratias tibi referimus Dne qui nos a temporalibus facis
respirare pressuris*; *… qui nos et caelestis participatione sacramenti*; and
eight more), and `sacro munere uegetati` returns none.

The negative is bounded by
`corpus.catholic-church.ancient-sacramentaries-2026-08-01`, whose own record says
what it does not hold: no eighth-century Gelasian, no Ambrosian book, no
Gregorian supplement beyond Wilson, no medieval diocesan sacramentary. The
Veronense is besides fragmentary. A prayer absent from it may still be ancient.

### 2.5 What this evidence supports, and what it does not

- It supports, as documented fact: this oration-set is **pre-Gregorian**, since it
  stands complete in the Old Gelasian; it circulated there **without a Sunday
  number**, in a run of *aliae missae*; the printed editions of the Gelasian
  assign that Mass to the twenty-second Sunday (Rheinau, St Gall, Gerbert) or the
  nineteenth (Pamelius); the Hadrianum numbers it the nineteenth; the 1962 numbers
  it the eighteenth. **Four different Sunday numbers for one set of prayers.**
- It supports, as documented fact: the chant-set travels as a unit too, and in the
  Hadrianum's cues that unit is attached to a *different* Sunday from the orations,
  with a different Alleluia. The gregorien.info report of the Sextuplex agrees that
  it is a unit and places it at the **Eighteenth** Sunday — the 1962's own number —
  in four of the six books, again with a different Alleluia (§ 2.3). So the chant
  Sunday and the oration Sunday do not coincide in either early witness, and they
  do not disagree in the same direction.
- **It does not support any claim about who joined them, when, or why**, and no
  such claim is made here or is to be made downstream. The 1962 pairing is a fact
  about the 1962 book; the joining of chant-set to oration-set is what the editor
  of a study reads, and `research/interpretations.md` labels every cross-element
  connection as editorial synthesis for that reason.
- Neither does it license reading the Gelasian's *second* Collect, its variant
  `effecisti`, or its `et mentibus` into the 1962 text. `propers/verified.md`
  controls what the 1962 prints.

### 2.6 Continuity from 1862 to 1962

The 1862 Pustet prints this formulary complete, in the same order, at its pp.
350–351, with the pre-1960 additional orations beside it. Every 1962 word stands
there. The collation is in `propers/verified.md`; the one real spelling difference
is `expectántibus` (1862) for `exspectántibus` (1962).

### 2.7 Where the Gospel stood: Rupert of Deutz's books

§§ 2.1–2.3 place the oration-set and the chant-set; this section places the
Gospel, which neither sacramentary nor gradual carries. **Read on the page images**
of Migne, PL 170, cols. 325–328 (Internet Archive `patrologiaecursu0170mign`,
leaves n168 and n169, unregistered, digests in § 6.3), located in the tracked
optical layer `artifact.rupert-of-deutz.de-divinis-officiis.latin-migne-pl-170.ia-djvu-ocr-2e2ca850`
(SHA-256 recomputed and matched, `2e2ca850…ed376`) at physical lines 23431–23519.

Rupert, *De divinis officiis* XII, **caput XVIII**, headed *Dominica decima octava
post Pentecosten* (col. 326), expounds a Mass whose chants and Epistle are this
formulary's — Introit *Da pacem*, Epistle *Gratias ago Deo meo pro vobis* (1 Cor 1),
Gradual verse *Fiat pax in virtute tua*, Offertory *Sanctificavit Moses* **with its
verse** *Videns Moses, procidens adoravit, dicens: Obsecro, Domine, dimitte peccata
populi tui, et dixit ad eum Dominus: Faciam secundum verbum tuum*, and Communion
*Tollite hostias* — but whose **Gospel is another**: *juxta Evangelium ejusdem
officii, sint sicut Scribae et Pharisaei, qui sederunt super cathedram Mosi (Matth.
xxiii)*. **Caput XIX**, *Dominica decima nona post Pentecosten* (cols. 326–327),
opens *In evangelio Dominicae nonae decimae ait Dominus paralytico: Confide, fili,
remittuntur tibi peccata tua (Matth. ix)*, and pairs the paralytic with the Epistle
of Eph 4 (*renovatur spiritu mentis suae … Qui furabatur, jam non furetur*) and the
chants *Salus populi*, *Elevatio manuum mearum* (the Gradual's verse), *Si
ambulavero* and *Tu mandasti* — which is the chant-set, and the Epistle, that the
1962 appoints at its **Nineteenth** Sunday (`src/sources/calendars/roman-1962/propers.yaml`,
`pentecost-19`, read for this comparison and already declared in
`research/review-dependencies.toml`).

What this adds to § 2.5, as documented fact and within its bound:

- In the books Rupert expounds, the paralytic of Mt 9 stood **one Sunday later**
  than in the 1962, with the Nineteenth's chants and Epistle, and this Sunday's
  chants and Epistle stood with the Gospel of the chair of Moses. So the Gospel,
  like the orations and the chants, travelled separately from the rest of the
  formulary.
- **The Offertory once had verses**, and the first of them is Moses' intercession
  for the people's sin, *Obsecro, Domine, dimitte peccata populi tui*, which Rupert
  sets beside the golden calf and *Dimitte me, ut irascatur furor meus* (he cites
  *Exod. xxxii*; the verse's own scriptural sources were not traced here). Guéranger prints both ancient verses in full (vol. XI, printed pp. 407–408;
  § 3.11). The 1962 prints the antiphon alone.
- Guéranger (vol. XI, printed pp. 393–394) records that this Sunday follows the
  September Ember days, that medieval liturgists discussed its having replaced the
  *Dominica vacat* after ordinations, and that 1 Cor 1 interrupts the run of
  Ephesians epistles; and (p. 402) that the Gospel was once the chair of Moses,
  citing Rupert. **His translation dates that usage to "the thirteenth century"**;
  Rupert's own text gives no date, the dating is Guéranger's or his translator's,
  and nothing here rests on it.
- **It does not establish** when, where or by whom the Gospel was moved, and no
  such claim is made. Rupert is one witness to one set of books; no lectionary,
  comes or evangeliary was opened.

---

## 3. Passage-by-passage reception matrix

One row per distinct appointed passage or composed proper, as the profile requires.
`Direct` means exegesis of this passage in a work of the named author, read at the
locus given. `Through the Catena` means the passage was read in Aquinas's
*Catena aurea*, at its own verified locus, as Aquinas reports it, and **not** at
the named Father's own locus; those are attributions the study must either verify
at PL or attribute through the Catena. **After the re-entry sweep of § 5.2 only
one attribution in this matrix is still of that kind**, Hilary on the Gospel
(reported by the Catena on vv. 1–2 and by Aquinas's lectura on v. 8);
Jerome, who was, is now read at PL 26 and the two places where the Catena departs
from him are recorded at § 3.5. Corpora searched are named in §5.

### 3.1 Introit antiphon — Ecclus 36:18 (no. 1669)

- **Direct ancient exegesis checked: none located.** See §5.1.
- **Later reception checked: none located** in a readable text. The repository's
  own passage→work index maps Sirach 36 to Rabanus Maurus (*Commentaria in
  Ecclesiasticum*), Walafrid Strabo (*Glossa ordinaria*), Hugh of Saint-Cher,
  Nicholas of Lyra, Denis the Carthusian and Cornelius a Lapide, all at chapter
  granularity and all as leads (`discover --passage "Sir 36:18"`, re-run on
  2026-09-22, returns exactly these six). None has a registered route: the library
  holds a Lapide for the Pentateuch and the Pauline epistles only, Hugh for three
  single psalm chapters, and no record for the other four; no registered Migne
  volume prints any of them. None was reached in text.
- **Textual state** (`propers/verified.md`): the antiphon is not the Clementine's
  wording and not the Greek's. This is the element with the least reception and
  the most textual divergence, and the study must say so rather than fill it.

### 3.2 Introit psalm verse and Gradual respond — Ps 121:1 (nos. 1669, 1672)

- **Direct: Augustine**, *Enarrationes in Psalmos* 121 § 2. The Psalm is a Song of
  degrees, "for these degrees are not of descent, but of ascent"; the city longed
  for is "the eternal Jerusalem, where are our fellow citizens, the Angels: we
  are wanderers on earth from these our fellow citizens"; and the joy of v. 1 is
  joy at the *companions* — "we find companions in this pilgrimage, who have
  already seen this city herself; who summon us to run towards her. At these he
  also rejoices, who says, I rejoiced in them who said to me, We will go into the
  house of the Lord." Read in the NPNF1-8 English at
  `https://www.newadvent.org/fathers/1801122.htm` (leaf SHA-256 in §6.3).
  - **Augustine's own Latin, read on the page images of PL 37** (the registered
    whole-volume facsimile, PDF p. 302 = cols. 1617–1618, where the heading *IN
    PSALMUM CXXI ENARRATIO. SERMO AD PLEBEM* stands at col. 1618, and PDF p. 303 =
    cols. 1619–1620, § 2; binding in `research/source-bindings.toml`). The English
    above is faithful to it: *quia non sunt gradus isti descendentium, sed
    ascendentium … Sed est in coelo aeterna Jerusalem, ubi sunt cives nostri
    Angeli: ab ipsis civibus nostris peregrinamur in terra … Invenimus autem et
    socios in ista peregrinatione, qui jam viderunt ipsam civitatem, et invitant nos
    ut curramus ad illam. Ad hos gaudet iste qui et dicit, Jucundatus sum in his qui
    dixerunt mihi, In domum Domini ibimus.* **His lemma is not the Missal's.**
    Augustine reads *Jucundatus sum in his qui dixerunt mihi* — "in those who said
    to me", persons — where the Missal and the Clementine read *Laetatus sum in his,
    quae dicta sunt mihi*, "in the things that were said". His reading of the verse
    as joy at the *companions* rests on that lemma, and he presses it: *Jucundatus
    sum in Prophetis, jucundatus sum in Apostolis. Omnes enim isti dixerunt nobis,
    In domum Domini ibimus.* A study that attaches his reading to the Missal's words
    must say that his psalter read them otherwise. (Hilary's lemma, below, is the
    Missal's.) At § 3 his lemma is *in atriis Jerusalem*; Migne's footnote records
    *in atriis tuis* in two manuscripts only.
- **Direct: Cassiodorus**, *Expositio psalmorum*, in Ps. CXXI, host sectio 6, read
  in the registered Latin (binding in `research/source-bindings.toml`). The cause
  of the joy is named and then raised: *Decora nimis et salutaris causa laetitiae
  … Sed ne more humanitatis mediocre gaudium fuisse sentires, de quo perfecto
  bono laetari se profiteatur ostendit, quia in domum Domini iturum se esse
  testatur. O digna exsultatio illuc ire contendere, unde nunquam aliquis velit
  exire!* Who said it is answered too — *Scilicet Spiritus sanctus, qui cordi eius
  tacita voce loquebatur … non aure, sed mente, non sermone, sed divino
  inspiramine* — and the house is *domus desiderabilis, domus de vivis lapidibus
  fabricata*, with Ps 26:4 attached. At sectio 2 he places the psalm in the
  ascent: *Audivimus gradum, intelligamus ad altiora conscensum … Ecce iam
  sublevatur propheta tertio gradu.*
- **Direct: Hilary of Poitiers**, *Tractatus super Psalmos*, in Ps. CXXI §§ 1–5,
  read in the registered CSEL 22 (Zingerle 1891) optical layer, where the whole
  *tractatus in psalmum CXXI* runs from physical line 29495 to 30011 and the
  *tractatus in psalmum CXXII* begins at 30012. The five sections read here are
  the tractatus's whole exposition of v. 1: the psalm heading stands at 29495, § 1
  opens at 29501, and § 6 — which turns to v. 2 — at 29680, so §§ 1–5 are physical
  lines 29501–29679. He opens from the hearer, not the text: *Qui spe caelestis
  desiderii detinetur, nihil obscuritatis in psalmo habebit*, because a man who
  remembers that he is *coheredem* and *futurumque incolam ciuitatis caelestis
  uiuis lapidibus extructae* will *proclamabit necesse est exemplo prophetae:
  Laetatus sum in his, quae dicta sunt mihi.* § 2 identifies the house from
  Ps 131:13–14 and refuses the earthly city: *non utique, ut diximus, hanc
  terrenam et caducam et poenas impietatis suae luentem, sed illam liberam et
  caelestem Hierusalem, quia eadem et Sion est.*
  § 3 reads *stantes erant pedes nostri* of the custodes *quibus datae sunt
  claues domus huius*, with Mt 16:19 and Is 52:7, and names the builders of the
  living stones — *a Moyse in lege, a prophetis in passionibus suis, a domino in
  corpore, ab apostolis in martyriis, a sancto spiritu in uirtutibus. hi
  aedificatores, haec aedificia, haec ciuitas.*
  - **§ 4** (physical lines 29623–29659) explains the *ut* of *aedificatur ut
    ciuitas*, and it is the reason the earthly city is refused rather than a
    second refusal of it: *Hierusalem, quae aedificatur ut ciuitas. non ciuitas,
    sed ut ciuitas: quia illa terrena ciuitatis aedificatio et templi extructio
    et tabernaculi institutio speciem illius aeternae et caelestis ciuitatis
    praefigurabat.* Because the building runs to the end of the age, the psalm
    gives it no date: *ideo aedificari eam sine temporis definitione significat.*
  - **§ 5** (physical lines 29660–29679) gives the reason for the psalm's plural
    *ibimus*: *quia unum ecclesiae corpus est, non quadam corporum confusione
    permixtum neque singulis in indiscretum aceruum et informem cumulum unitis,
    sed per fidei unitatem, per caritatis societatem, per operum uoluntatisque
    concordiam, per sacramenti unum in omnibus donum, unum omnes sumus* — with
    1 Cor 1:10 and Acts 4:32 attached, and the conclusion *tunc erimus ciuitas
    dei, tunc sancta Hierusalem, quia Hierusalem aedificatur ut ciuitas, cuius
    participatio est in idipsum.* `research/interpretations.md` § 1.2 rests on
    these two sections; they are recorded here so that every Hilary claim it
    makes has a matrix row and a stated locus behind it.
  - The 1 Cor 1:10 in § 5 is from the **same letter** as this Sunday's Epistle
    and from a verse the lection stops short of. Hilary is not commenting on the
    Epistle and this record does not treat him as doing so; the coincidence is
    recorded and nothing is built on it.
  - **How the Hilary Latin is quoted.** The CSEL 22 optical layer is badly
    damaged on several pages of this tractatus (lines 29660–29665 read `Sfd
    (|ui;i unum ecclesiie c(ir|tus est …`). Every Hilary quotation in §§ 3.2 and
    3.3 was therefore checked on the page images of the same Internet Archive item
    — leaves n599–n602 = CSEL 22 pp. 570–573 and n607–n608 = pp. 578–579,
    unregistered, digests in § 6.3 — and **the images, not the layer, control the
    wording**. Three readings an earlier draft reconstructed from the layer were
    wrong and are corrected above: *quia eadem et Sion est* (§ 2, p. 571), *quae
    aedificatur ut ciuitas* (§ 4, p. 572) and *quia Hierusalem aedificatur* (§ 5,
    p. 573). The edition's ligatures *æ* and *œ* are written out; nothing else is
    normalised.
- **Direct, in Greek: John Chrysostom**, *Expositio in Psalmum CXXI*, read in the
  registered whole-volume layer of PG 55 and on its page images, **cols. 347–351**
  (heading `ΕΙΣ ΤΟΝ ΡΚΑ' ΨΑΛΜΟΝ` at col. 347; binding in
  `research/source-bindings.toml`). He reads v. 1 of the exiles, *ἀπὸ τῆς
  αἰχμαλωσίας ἐγένοντο βελτίους* — "from the captivity they became better" — and
  of their longing for *τὸν εὐκτήριον οἶκον καὶ τὴν πόλιν*, the house of prayer and
  the city; and he turns it at once on his hearers: call men to the hippodrome and
  many run together, *ἂν δὲ ἐπὶ τὸν εὐκτήριον οἶκον, ὀλίγοι οἱ μὴ ὀκνοῦντες* — call
  them to the house of prayer and few are not sluggish, so that Christians show
  themselves slower than the Jews. At v. 3 the city built *as* a city is the city
  the returning exiles found in ruins, *τῶν πύργων καταβεβλημένων, τῶν τειχῶν
  ἐῤῥιμμένων* (col. 348).
- **Direct, in Greek: Theodoret**, *Interpretatio in Psalmos*, in Ps. CXXI, PG 80,
  **cols. 1879–1882**, read on the page images of the registered facsimile (PDF pp.
  996–997). The psalm is sung by those who have *already* received the good news
  of the return: *Εὐσεβείας αὕτη φωνή· γάννυνται γὰρ καὶ χαίρουσιν, οὐχ ὡς τὰς
  οἰκίας ἀποληψόμενοι, ἀλλ' ὡς τὸν θεῖον οἶκον ὀψόμενοι* — "this is the voice of
  piety: they rejoice not as men about to recover their houses but as men about to
  see the divine house." V. 3 is the deserted city that will flourish again and
  recover its walls; v. 4 the tribes reunited after the return.
- **Direct, later: Robert Bellarmine**, *Explanatio in Psalmos*, Ps 121, in the
  tracked O'Sullivan English (physical line 4541; binding in
  `research/source-bindings.toml`). He gives **both** readings and ranks them.
  First the history: "Such is the language of God's people, expressive of their
  joy on hearing the welcome news of their return to their country … we shall
  return to our country, where we shall get to see mount Sion and the site of the
  house of the Lord." Then: "Christ, however, was the bearer of a far and away more
  happy message," with Jn 14:2. At v. 2 (line 4543) he asks how Christians can say
  *our feet were standing in thy courts* and answers from paradise before the
  fall, "that we may understand that the Psalm treats of the celestial, and not the
  earthly Jerusalem." The 1866 English is abridged by its translator and is quoted
  as printed; the Latin was not opened.
- **Where the witnesses stand to one another, and it is a real disagreement.**
  Augustine, Hilary and Cassiodorus read the house as the heavenly city built of
  living stones — Cassiodorus and Hilary through the psalm's title and the ascent,
  Augustine through the *companions* his lemma gives him — and Hilary refuses the
  earthly city in terms. **Chrysostom and Theodoret read the psalm of the earthly
  city rebuilt after the captivity, and of nothing else**; neither offers an
  allegory of the Church or of heaven at this psalm. Bellarmine holds both, the
  history first and the heavenly sense as the higher. § 4.6 preserves the
  disagreement.
- **Appointed twice**, as Introit verse and as Gradual respond; inventoried once
  in `research/chronology.toml`, which lists `Ps.121.1` under both elements.

### 3.3 Gradual verse — Ps 121:7 (no. 1672)

- **Direct: Augustine**, *Enarr. in Ps.* 121 § 12, on *Fiat pax in virtute tua*:
  "O Jerusalem, O city, who art being built as a city, whose partaking is in The
  Same: Peace be in your strength: peace be in your love; for your strength is
  your love," with the *Song of Songs* 8:6 proof, "Love is strong as death," and
  the consequence, "since this love slays what we have been, that we may be what
  we were not; love creates a sort of death in us." In § 13, on the next verse,
  Augustine turns the same peace against those "who seeking their own glory, say,
  Peace be with you: and have not the peace which they preach to the people. For
  if they had peace, they would not tear asunder unity."
  - **The English abridges § 12, and the Latin expounds the towers.** The NPNF
    text (CCEL NPNF1-8 line 60439 and the New Advent page alike) closes § 12 with
    "Love is strong as death..." — an editorial ellipsis. Migne's print, read on the
    page image of PL 37, PDF p. 307 = col. 1628, continues past it: *Si ergo
    valida est, fortis est et magnae virtutis, et ipsa est virtus, et per ipsam
    reguntur infirmi a firmis, terra a coelo, populi a sedibus; ideo, Fiat pax in
    virtute tua, fiat pax in dilectione tua. Et per istam virtutem, per istam
    dilectionem, per istam pacem, fiat abundantia in turribus tuis: id est, in
    excelsis tuis. Pauci enim sedebunt in judicio; sed multi ad dexteram positi
    facient populum civitatis illius. Multi enim pertinebunt ad singulos quosque
    excelsos, a quibus recipiantur in tabernacula aeterna; et erit abundantia in
    turribus ejus.* So Augustine **does** read the towers: they are the city's
    *excelsi*, the few who will sit in judgment, to whom the many at the right hand
    belong and by whom they are received into the eternal tabernacles (Lk 16:9).
    An earlier draft of this record, reading the English only, said Augustine was
    no witness on the towers; that is withdrawn.
- **Direct: Cassiodorus**, in Ps. CXXI, host sectio 12, on the same verse, and he
  answers the same question Augustine does in almost the same terms: *Virtus
  quippe ipsius pax sine dubitatione sanctorum est, quae vocatur et charitas; de
  qua scriptum est: Deus charitas est … Per hanc enim fiunt unum, per hanc templum
  merentur esse Creatoris.* On the second clause he divides: *Sed hic per turres
  aliquid significantius videtur expressum, ut hanc abundantiam non aequalem
  omnibus, sed intelligeres esse potiorem. Turres enim sunt quae obiectu et
  altitudine sua civitates defendunt … Unde non improbe martyres significatos
  advertimus, qui oppositione corporis sui, civitatem Dei pia confessione
  defendunt.*
- **Direct: Hilary**, in Ps. CXXI §§ 13–14, on the same verse in the fuller Greek
  form his text carries, *fiat pax in uirtute tua, et abundantia in turribus
  grauibus tuis*, read on the page images of CSEL 22 pp. 578–579 (leaves n607 and
  n608), where the section figures **13.** and **14.** are legible, and located in
  the registered layer at physical lines 29911–29962 (the layer prints the first
  marker as `1 3.`; Zingerle's apparatus interrupts the body at 29940–29950, and
  § 15, on v. 8, begins at 29963). His *virtus* is not charity but the strength
  peace itself confers: *pax atque uirtus domus huius conexa sunt sibi. posse enim aliquid nisi
  ex pace non poterit … perfecta uero uirtus eorum tantum est, qui congregantur
  in idipsum*, and again *pax enim ecclesiae et unitas uirtutem nobis
  firmitatemque praestat*, with Phil 4:7. His towers are not the martyrs but the
  city's principes: *grauia pro firmis et inmobilibus* in scriptural usage, so the
  abundance is *eorum tantum fidelium et sanctorum uirorum, qui ceterae ciuitatis
  huius aedificationi tamquam turrium firmitate praestiterint.*
- **Direct, in Greek: Chrysostom**, *Expositio in Ps. CXXI*, PG 55, **col. 350**
  (read on the page image, leaf n340). *Γενέσθω δὴ εἰρήνη ἐν τῇ δυνάμει σου … Τί
  ἐστιν, Ἐν τῇ δυνάμει σου; Ἐν τῇ ὑποστάσει σου, ἐν τοῖς οἰκοῦσί σε, ἐν τῇ εὐθηνίᾳ
  σου. Ἐπειδὴ γὰρ φθοροποιὸν ὁ πόλεμος, καὶ τοῦτο αὐτὴν ἀπώλεσεν, ἐπεύχεται αὐτῇ
  εἰρήνην* — the city's "strength" is its substance, its inhabitants, its plenty;
  "since war is destructive, and this is what destroyed her, he prays peace for
  her." Peace and plenty go together: *Τί γὰρ ὄφελος εἰρήνης, ὅταν πενίᾳ, καὶ
  πτωχείᾳ, καὶ λιμῷ συζῶσι; τί δὲ ὄφελος εὐθηνίας, ὅταν πόλεμος ἐπίκειται;* The
  towers are given no figure; for the first clause he cites one version's *Ἐν τῷ
  προτειχίσματί σου* and another's *Ἐν τῷ περιβόλῳ σου* — the outwork, the circuit
  wall — and for the second *Ἐν τοῖς βασιλείοις σου*, "in thy palaces".
- **Direct, in Greek: Theodoret**, PG 80, **col. 1881** (page image, PDF p. 997).
  After Symmachus's *Εἴη εἰρήνη ἐν τῷ περιβόλῳ σου, ἡσυχία ἐν τοῖς βασιλείοις σου*:
  *Ἐπεύχεται δὲ αὐτῇ ὁ θεῖος Δαβὶδ τὰ ἀγαθά, ὥστε καὶ τοὺς περιβόλους, καὶ τὰ
  βασίλεια, καὶ τὰς ἐν αὐτῇ οἰκίας, πάσης ἀπολαύειν εἰρήνης* — David prays that the
  walls, the palaces and the houses of the city may enjoy all peace.
- **Direct, later: Bellarmine**, Ps 121 v. 7 (tracked English, line 4553): "may
  your walk [so the transcription, for *walls*] be always secure and fortified,
  thereby ensuring perfect peace and quiet to all who dwell within them; 'and
  abundance in thy towers;' no lack of meat or drink in your public buildings and
  private houses." Of the heavenly Jerusalem the prayer is only "the pious
  affection we cherish for the blessings of the Jerusalem above," since there can
  be no want there.
- **A material difference, preserved, and now with six readers.** On *virtus*:
  charity for Augustine and Cassiodorus; the firmness that the Church's peace and
  unity confer for Hilary, who makes *virtus* and *pax* condition each other; the
  city's substance, people and plenty for Chrysostom; its walls for Theodoret and,
  in the literal sense, Bellarmine. On the towers: the martyrs (Cassiodorus); the
  steadfast among the faithful (Hilary); the *excelsi* who sit in judgment and
  receive the many (Augustine, in the Latin); the city's real towers and buildings
  (Chrysostom, Theodoret, Bellarmine's literal sense). The three Latin readings are
  allegories of the same clause and neither refutes another, but they are not one
  reading; the two Greek readings are not allegories at all (§ 4.6). The study
  must not report any two of them as one.
- **Note for the study.** The polemical edge of Augustine's §§ 12–13 is
  anti-Donatist. It is Augustine's setting, not this Sunday's, and must not become
  the frame of a Mass commentary.

### 3.4 Alleluia — Ps 101:16 (no. 1673)

- **Direct: Augustine**, *Enarr. in Ps.* 101, **sermo I**, § 16 (the first of his
  two discourses on this psalm, which runs to v. 20; sermo II begins there): "Now
  that You have pitied Sion,
  now that Your servants have taken pleasure in her stones, by acknowledging the
  foundation of the Apostles and Prophets; now that they have pitied her dust …
  hence preaching has increased among the heathen: let the heathen fear Your
  Name, let another wall approach also from the heathen, let the Corner Stone be
  recognised, let the two who come from different regions, but who no longer
  differ in belief, meet in close union." § 17, on v. 17, adds "For the Lord shall
  build up Sion. This work is going on now. O you living stones, run to the work
  of building, not to ruin."
- **Direct: Cassiodorus**, in Ps. CI, host sectio 22, on the appointed verse
  itself, read in the artifact this repository already tracks (no network
  required): *(Vers. 16.) Et timebunt gentes nomen tuum, Domine, et omnes reges
  terrae gloriam tuam. Haec contra saeculi istius superstitiones nefarias
  depromuntur: quia tunc non timebatur verus Dominus, quando mundus devotus idolis
  serviebat; postquam vero adventus eius salutaris infulsit, gentes conversae sunt
  per timorem.* The kings are read morally — *qui corpora sua divinis regulis
  infrenantes, sui imperatores esse (Domino praestante) valuerunt* — and the
  believing kings are identified with the *lapides* of v. 15, which sectio 21
  glosses *Isti lapides, id est Christianos, qui divina firmitate viguerunt*. At
  sectio 23, on v. 17, the building is named: *quoniam omnes gentes ideo timebunt
  Dominum … quia aedificata est Sion, hoc est mater Ecclesia, de vivis lapidibus
  fabricata, in qua Domini cultura usque ad finem mundi sine intermissione
  proficiet.*
- **Five direct witnesses agree on the structure of the verse** — the fear of the
  nations follows from the building of Sion, and Sion is the Church — and differ
  in emphasis: Augustine's is the second wall coming from the heathen to meet the
  Corner Stone; Cassiodorus's the conversion of the nations out of idolatry and the
  self-rule of the kings; the PG 27 expositions' the calling of the nations joined
  to the stones of the former people; Bellarmine's the conversion of nations and
  kings while the new Sion is building. **Theodoret agrees on the fulfilment and
  differs on the letter**: he gives the verse a first, historical sense (the
  return) that the others do not give it, and then denies that the history
  fulfilled it. Bellarmine, conversely, names the historical reading only to refuse
  it. All five are direct exegesis of v. 16 at its own locus.
- **Augustine's own Latin, tracked in this checkout, was read at the same two
  sections** (`…wikisource-part-11-latin-text/enarrationes-part-11.txt`, bound in
  `research/source-bindings.toml`): *IN PSALMUM CI* opens the file, § 16 stands at
  its line 20 — *«vers.» 16. … Et timebunt Gentes nomen tuum, Domine, et omnes
  reges terrae gloriam tuam* — and § 17 at line 21, *Quoniam aedificabit Dominus
  Sion … Et videbitur in gloria sua.* It agrees with the English at every clause
  quoted above, and it settles the numbering caution below from the Latin side.
- **The same two sections in Migne's own print and in a third delivery.** PL 37,
  PDF p. 145 = col. 1304, read on the page image: *16. [vers. 16.] Quid igitur
  sequitur? Et timebunt Gentes nomen tuum, Domine, et omnes reges terrae gloriam
  tuam. Jam quoniam misertus es Sion … hinc praedicatio crevit in Gentibus: timeant
  nomen tuum Gentes … veniat et alius paries de Gentibus, agnoscatur lapis
  angularis (Ephes. II, 20), ibi haereant duo de diverso venientes, sed jam non
  adversa sentientes*, and § 17 *Quoniam aedificabit Dominus Sion. Hoc agitur nunc.
  Eia lapides vivi in structuram currite, non in ruinam.* The registered
  augustinus.it page for sermo I (re-fetched, digest matched, § 6.3) agrees word
  for word apart from its *i* for *j*. The three Latin witnesses and the two
  English ones agree at every clause this row quotes.
- **Direct, in Greek: Theodoret**, in Ps. CI, PG 80, **cols. 1679–1680** (page
  image, PDF p. 890). He reads v. 16 first of the return — the neighbours who had
  seen Israel's calamities would see the return and the rebuilding and marvel at
  God's power — and then says in terms that this was not its fulfilment: *Τοῦτο δὲ
  κυρίως καὶ ἀληθῶς μετὰ τὴν τοῦ Θεοῦ καὶ Σωτῆρος ἡμῶν ἐνανθρώπησιν γέγονε* — "this
  happened properly and truly after the incarnation of our God and Saviour," for
  after the return the neighbours marvelled and made war instead of believing; here
  the word foretells the conversion of all the nations and their kings, part of
  which we see accomplished and part we hope for (Heb 2:8, Phil 2:10). **So at
  Ps 101 Theodoret, the Antiochene who reads Ps 121 of the rebuilt city alone,
  reads the Alleluia verse of Christ.**
- **Direct, in Greek: the *Expositiones in Psalmos* printed under Athanasius's
  name**, PG 27, **col. 429** (page image, leaf n221): *Εἰκότως μεταξὺ τοῦ
  εὐδοκῆσαι τοὺς λίθους τοῦ προτέρου λαοῦ τῶν ἐθνῶν ἐπισυνάπτει τὴν κλῆσιν* — "fittingly,
  between the good pleasure in the stones of the former people, he joins on the
  calling of the nations"; the kings are the kingdoms, *οὐ γάρ ἐστι βασιλεία οὐδὲ
  ἔθνος ὃ μὴ προσκυνεῖ τὴν δόξαν Κυρίου*; and at v. 17 Sion is *τὴν Ἐκκλησίαν*. The
  attribution is Migne's and is reported as his.
- **Direct, later: Bellarmine**, Ps 101, in the tracked English, where the
  paragraph on *Timebunt gentes* is numbered **15** (line 3597), one behind the
  Vulgate as in NPNF: "When the new Sion shall be in progress of building, the
  gentiles will be converted, and 'shall fear' with a holy fear and pious
  veneration, 'thy name, O Lord,' Jesus Christ." At the paragraph numbered 18 (line
  3603) he refuses the historical reading outright: the Holy Ghost added *Let these
  things be written unto another generation* "for fear the Jews may suppose that
  this prophecy applied to themselves, and take it as in reference to the
  termination of the captivity of Babylon, and the building of Jerusalem."
- **Numbering caution.** The NPNF marginal verse numbers in this psalm run **one
  behind** the Vulgate and the Douay: what NPNF cites as Psalm 101:15 is Vulgate
  101:16. The section numbers (§ 16, § 17) are the reliable locus, and the tracked
  Latin confirms it: it prints *vers. 16* against its own § 16, where the CCEL
  NPNF1-8 text prints *(ver. 16)* against its § 17. Cassiodorus's delivery carries
  Migne's own marginal numerals, which agree with the Vulgate.

### 3.5 Gospel — Mt 9:1–8 (no. 1674)

- **Direct: John Chrysostom**, *Homiliae in Matthaeum* 29 (NPNF1-10). The city is
  Capernaum; this paralytic is not the paralytic of John 5; "Seeing, it is said,
  their faith; that is, the faith of them that had let the man down … Or rather,
  in this case the sick man too had part in the faith; for he would not have
  suffered himself to be let down, unless he had believed." Christ "healed first
  that which is invisible, the soul, by forgiving his sins," and proves the
  greater, unseen work by the lesser, visible one: "by how much a soul is better
  than a body, by so much is the doing away sins a greater work than this." The
  reading of their thoughts is a second sign of divinity: "But that it belongs to
  God only to know men's secrets, hear what says the prophet …". And "He said not, I forgive you your sins, but,
  your sins be forgiven you: upon their constraining, He discloses His authority
  more clearly." Of the crowd's *glorificavérunt Deum, qui dedit potestátem talem
  homínibus*: "But nevertheless they still creep upon the earth. … But He did not
  rebuke them, but proceeds by His works to arouse them, and exalt their thoughts.
  Since for the time it was no small thing for Him to be thought greater than all
  men, as having come from God. For had they well established these things in
  their own minds, going on orderly they would have known, that He was even the
  Son of God. But they did not retain these things clearly, wherefore neither
  were they able to approach Him."
- **Direct: Augustine**, *De consensu evangelistarum* II. xxv. 57–58 (NPNF1-6).
  On *fili* against Luke's *homo*: "For these sins were [thus said to be] forgiven
  to the 'man,' inasmuch as the very fact that he was a man would make it
  impossible for him to say, 'I have not sinned;' and at the same time, that mode
  of address served to indicate that He who forgave sins to man was Himself God."
  (NPNF prints double quotation marks round *man* and *I have not sinned*, given
  here as single marks inside the quotation.) The
  bracketed words are the NPNF translator's supplement and are kept here. On
  *civitátem suam*, at length: Galilee may be called Christ's city as the whole
  Roman world is called a Roman state, and Capernaum "held a position of such
  eminence in Galilee that it was reckoned to be a kind of metropolis"; failing
  that, Matthew may simply have passed over what happened between the arrival and
  Capernaum.
- **Direct: Jerome**, *Commentariorum in Matthaeum libri IV*, lib. I, at Mt 9:1–8,
  read on the page images of **PL 26, columns 53–56** — artifact PDF pp. 32–33 of
  `artifact.jacques-paul-migne.patrologia-latina-volume-26.paris-1845.internet-archive-google-pdf-0d889bd6`,
  inside the registered segment `…pl26-columns-15-218`, rendered at 200 dpi. The
  scan carries no text layer; every reading below was taken off the image.
  - On the city and the faith (col. 54): *Civitatem ejus non aliam intelligimus
    quam Nazareth, unde et Nazaræus appellatus est. Obtulerunt autem ei, ut supra
    diximus, secundum paralyticum jacentem in lectulo, quia ipse ingredi non
    valebat. Videns autem Jesus non ejus fidem qui offerebatur, sed eorum qui
    offerebant, dixit paralytico: Confide, fili, remittuntur tibi peccata tua.*
  - On *fili* (col. 55): *O mira humilitas, despectum et debilem, totisque
    membrorum compagibus dissolutum, filium vocat, quem sacerdotes non
    dignabantur attingere. Aut certe ideo filium, quia dimittuntur ei peccata
    sua.* Then, **and this is where the tropology actually stands**: *Juxta
    tropologiam interdum anima jacens in corpore suo, totis membrorum virtutibus
    dissolutis, a perfecto doctore offertur curanda Domino, quæ si misericordia
    ejus sanata fuerit, tantum roboris accipit, ut portet statim lectulum suum.*
  - On vv. 3–4 (col. 55): *Sed Dominus videns cogitationes eorum, ostendit se
    Deum, qui possit cordis occulta cognoscere, et quodammodo tacens loquitur:
    Eadem majestate et potentia qua cogitationes vestras intueor, possum et
    hominibus peccata dimittere. Ex vobis intelligite quid paralyticus
    consequatur.*
  - On vv. 5–6 (col. 55): *Inter dicere, et facere, multa distantia est. Utrum
    sint paralytico peccata dimissa, solus noverat, qui dimittebat … Fit igitur
    carnale signum, ut probetur spirituale … Et datur nobis intelligentia,
    propter peccata plerasque [Al. plerisque] evenire corporum debilitates. Et
    idcirco forsan dimittuntur prius peccata tua [Al. tacet tua], ut causis
    debilitatis ablatis, sanitas restituatur.*
  - On vv. 7–8 (cols. 55–56), and this is the **whole** of what he says there:
    *Et anima paralytica si surrexerit, si pristinum robur recuperaverit, portat
    lectum suum in quo jacebat antea dissoluta, et portat illum in domum virtutum
    suarum.* He then passes straight to v. 9. **Jerome offers no comment of any
    kind on *qui dedit potestatem talem hominibus*** — see § 4.3.
- **What reading Jerome at his own locus corrects in the Catena.** Two things.
  (a) The Catena's Jerome lemma is a **splice**: it runs *O mira humilitas …
  attingere* (Jerome on vv. 1–2) straight into *ubi datur nobis intelligentia,
  propter peccata plerasque evenire corporum debilitates* (Jerome on vv. 5–6),
  which stands three lemmata later in the commentary and under different verses.
  (b) The Catena's tropological sentence *unusquisque enim aeger petendae salutis
  precatores debet adhibere* is **not** in PL 26 at this place; what Jerome's own
  *juxta tropologiam* says is the sentence about the soul offered by a *perfectus
  doctor*, quoted above. The Catena's wording differs in detail elsewhere too
  (*forsitan prius dimittuntur peccata* against Migne's *forsan dimittuntur prius
  peccata tua*). Anything the study takes from Jerome must be taken from PL 26,
  not from the Catena.
- **Through the Catena** (Aquinas, *Catena in Matthaeum* cap. 9 lect. 1, read in
  the Latin at `corpusthomisticum.org/cmt05.html`, whole-file SHA-256 recorded in
  §6):
  - **Hilary** — *a Iudaea repudiatus in civitatem suam revertitur. Dei civitas
    fidelium plebs est: in hanc ergo introivit per navim, idest Ecclesiam, vectus*;
    and *In paralytico autem gentium universitas offertur medenda … huic
    remittuntur animae peccata, quae lex laxare non poterat: fides enim sola
    iustificat.*
  - **Rabanus** — *Surgere autem est animam a carnalibus desideriis abstrahere;
    lectum tollere est carnem a terrenis desideriis ad voluptatem spiritus
    attollere; domum ire est ad Paradisum redire.*
  - The Catena also carries "Ioannes episcopus" (*Quantum valet apud Deum fides
    propria, apud quem sic valuit aliena …*) and the *Glossa* on whether
    *ut sciatis* is Christ's words or the Evangelist's.
- **Direct, later, a Doctor: Thomas Aquinas**, *Super Evangelium S. Matthaei
  lectura*, caput IX, on Mt 9:1–8, **read on the page images** of the registered
  Venice 1745 facsimile, *Opera*, tomus III, printed pp. 120–122 = PDF pp. 138–140
  at native 600 ppi, and located in the tracked optical layer at physical lines
  16227–16540 (bindings for both in `research/source-bindings.toml`). The earlier
  statement of this record that the library holds Aquinas "not for the Matthew
  lectura" was false: the volume's own work record says it holds his lectures on
  Matthew and John. This is the eighteenth-century vulgate text of a *reportatio*,
  not the Leonine or Marietti text. What he says, verse by verse:
  - v. 1 (p. 121): *Haec navicula significat crucem, vel Ecclesiam. Et venit in
    civitatem suam, scilicet in civitatem gentium, quae sibi datae sunt*, with
    Ps 2:8. Then the harmony question, answered twice: *quaedam erat civitas
    Christi ratione nativitatis; et haec erat Bethlehem: quaedam ratione
    educationis; et haec erat Nazareth: quaedam ratione conversationis, et
    operationis miraculorum; et sic Capharnaum*; and Augustine's metropolis, or
    else that the Evangelists pass something over, *quod videlicet transivit per
    Nazareth, et venit in Capharnaum* (§ 4.1).
  - v. 2: *Iste paralyticus significat peccatorem in peccato iacentem … Illi autem
    qui portant eum, sunt illi qui suis monitionibus portant eum ad Deum*; and on
    *videns fidem illorum*, *Curat aliquando Dominus aliquem propter fidem suam:
    aliquando propter preces suas, et aliorum* (§ 4.2). Sins are forgiven first
    *quia peccatum erat causa aegritudinis … Unde fecit Deus sicut bonus medicus,
    qui causam curat.*
  - vv. 3–4: the scribes *videbant hominem, et non videbant Deum*; Christ confutes
    them *sua cognitione, verbo, et facto*, for *sicut soli Deo pertinet dimittere
    peccata, sic cognoscere secreta cordis.*
  - v. 6 (p. 122), *Filius hominis … in terra*, against Nestorius and Photinus;
    and then the objection this record had found in no witness: ***Videtur quod
    per hoc non ostendatur, quia etiam ipsi Apostoli habebant potestatem. Sed
    dicendum, quod ipsi habebant per viam administrationis, non auctoritatis*** —
    the Apostles too had the power to forgive sins, by way of ministry and not of
    authority. § 4.3 turns on it.
  - v. 6, the tropology: *Similiter peccatori in peccato iacenti dicitur, Surge,
    a peccato per contritionem; tolle lectum, per satisfactionem … et vade in
    domum tuam, in domum aeternitatis, vel in conscientiam propriam.*
  - v. 8: *Videntes autem turbae, non scribae … timuerunt … glorificaverunt Deum:
    quia omnia in Deum retulerunt*; and on *hominibus* he reports Hilary: *Qui
    dedit talem potestatem hominibus, ut fiant filii Dei*, with Jn 1:12. That is a
    second Hilary attribution through Aquinas, and a reading of v. 8 that is not
    the ministerial one.
- **Later and Doctoral reception: what the index returns and what the library
  holds.** The Rabanus lemma above is the Catena's report and not Rabanus at his
  own locus. `tools/commentary-work-index discover --passage "Mt 9:1"`, run again
  on 2026-09-22, returns nineteen rows, all matched at chapter granularity, on
  Matthew 9 and not on the verses. With the registration state of each, found by
  work record **and** by the registered collected and whole volumes:
  - **Read**: Jerome, *Commentariorum in Matthaeum* (PL 26); Chrysostom, *Homiliae
    in Matthaeum*; Thomas Aquinas, *Super Evangelium S. Matthaei lectura* (Venice
    1745, above).
  - **Read through an unregistered delivery**: Thomas Aquinas, *Catena aurea in
    quatuor Evangelia* — the library holds the *Catena* only *in Lucam*; the
    *Catena in Matthaeum* was read on Corpus Thomisticum (§ 6.3).
  - **No registered route**: Hilary, *Commentarius in Matthaeum* (the library holds
    his *Tractatus super Psalmos* only, and no PL 9); Rabanus Maurus, *Commentariorum
    in Matthaeum libri VIII*; Albert the Great, *Super Matthaeum*; Chromatius,
    *Tractatus in Matthaeum*; Paschasius Radbertus, *Expositio in Matheo* (two
    rows); Theophylact, *Enarratio in Evangelium Matthaei* (the library holds his
    John only); Bruno of Segni, *Commentaria in Matthaeum*; Walafrid Strabo,
    *Glossa ordinaria*; Nicholas of Lyra; Denis the Carthusian (two rows); Juan
    Maldonado; Hugh of Saint-Cher (the library holds three single psalm chapters
    of his *Postilla*, restricted, and no Gospel); Cornelius a Lapide,
    *Commentaria in Scripturam Sacram* (the library holds his Pentateuch and his
    Pauline epistles, and no Gospel). None of the registered Migne volumes — PL 24,
    26, 30, 37, 56, 70, 78, 92, 105, 170; PG 27, 29, 55, 57, 80, 82 — contains any
    of these works on Matthew (PG 57 carries Chrysostom's own Greek homilies, § 6.3).
  - **So the later reception of the Gospel is no longer a negative.** It has one
    Doctor read at his own locus. Beyond him it is bounded by the registered
    library and that index, and by nothing wider; no external delivery of an
    unregistered lead was tried (§ 5.2).
- **Not reached:** Hilary's *Commentarius in Matthaeum* VIII at its own locus. He
  is the one Father of the four whose Gospel reading is still reported by another
  — by the *Catena* on vv. 1–2, and now also by Aquinas's lectura on v. 8. See
  § 5.2.

### 3.6 Epistle — 1 Cor 1:4–8 (no. 1671)

- **Direct: John Chrysostom**, *Homiliae in epistulam i ad Corinthios* 2
  (NPNF1-12), on vv. 4–8 clause by clause:
  - v. 4, *For the grace of God*: "Do you see how from every quarter he draws
    topics for correcting them? For where grace is, works are not; where works, it
    is no more grace. If therefore it be grace, why are you high-minded? Whence
    is it that you are puffed up?"
  - v. 5, *in all utterance and all knowledge*: "Word [or utterance,] not such as
    the heathen, but that of God … You, says he, are not such as these, but
    competent both to understand and to speak." (The bracketed gloss is the NPNF
    translator's and is kept.)
  - v. 6, *Even as the testimony of Christ was confirmed in you*: "Under the
    color of praises and thanksgiving he touches them sharply … If therefore you
    were established by signs and grace, why do you waver?"
  - v. 7, *waiting for the revelation*: "he terrifies them by mention of the
    fearful judgment-seat, and thus implying that not only the beginnings must be
    good, but the end also … Revelation is his word; implying that although He be
    not seen, yet He is, and is present even now, and then shall appear.
    Therefore there is need of patience."
  - v. 8, *who shall also confirm you unto the end*: "he is also covertly
    accusing them: for, to say, He shall confirm, and the word unreprovable marks
    them out as still wavering, and liable to reproof."
  - and on the proem as a whole: "consider how he always fastens them as with
    nails to the Name of Christ … in order that by incessant application of that
    glorious Name he may foment their inflammation, and purge out the corruption
    of the disease."
- The disease is the party-spirit of vv. 10–13, which the lection stops short of.
  Chrysostom's reading of vv. 4–8 is governed by it throughout, and a study that
  drops the schism drops his argument.
- **Direct, in Greek: Theodoret**, *Interpretatio in I Cor.* 1:4–8, read in the
  registered whole-volume layer of PG 82 (physical lines 16583–16773) and on the
  page images of **cols. 229–232** (leaves n131–n132; binding in
  `research/source-bindings.toml`). The earlier statement of this record that
  Theodoret is held "for the Psalms and Galatians only" was false: PG 82 carries
  his commentary on the whole Pauline corpus, and its registered layer is the
  route. What he says:
  - v. 4 (col. 229): *Μέλλων κατηγορεῖν προθεραπεύει τὴν ἀκοήν, ὥστε δεκτὴν
    γενέσθαι τὴν ἰατρείαν. Ἔχει δὲ καὶ τὸ ἀψευδὲς τὰ εἰρημένα· ἐπὶ γὰρ ταῖς
    δοθείσαις αὐτοῖς εὐχαρίστησε τῷ Θεῷ δωρεαῖς* — "being about to accuse, he first
    tends their hearing, so that the cure may be received. Yet what is said is also
    free of falsehood, for he gave thanks to God for gifts they had been given."
  - vv. 5–6: the riches are *εἴδη τῶν τοῦ Πνεύματος χαρισμάτων* (1 Cor 12:8); he
    sets the Lord's name in continually, *διδάσκων ὡς οὐχ ἑτέρωθεν ὀνομάζεσθαι
    χρή, ἀλλ' ἐκ τοῦ τὴν σωτηρίαν παρεσχηκότος* — teaching that they must be named
    from no one but him who gave salvation; the confirmation of the testimony is
    the working of signs.
  - v. 8 (col. 232): *Καὶ τὸ βέβαιον αὐτοῖς ἐπηύξατο, καὶ τὸ ἄμωμον. Τὸ εἰπεῖν
    ἀνεγκλήτους, ἔδειξε τέως ὄντας ἐγκλήμασιν ὑπευθύνους* — "saying *blameless*
    showed them as for the present liable to charges." After v. 9 he says, in a
    sentence read in the layer only (lines 16787–16789), that having smoothed their
    hearing with praises and blessings Paul now begins the accusation.
- **Direct, later, a Doctor: Thomas Aquinas**, *Super I ad Corinthios*, cap. 1
  lect. 1, in the part the work record says survives from Thomas's own hand, read
  on the registered Corpus Thomisticum page (re-fetched 2026-09-22, digest matched;
  `storage = "restricted"`, so quoted only in short phrases; binding in
  `research/source-bindings.toml`). Paul gives thanks first *ut correctionem
  suorum defectuum tolerabilius ferant*; the riches of utterance and knowledge are
  *referendum … ad eos qui erant in Ecclesia perfectiores*, in whom the lesser
  also possess them through the charity that joins (with Augustine on John); and
  at v. 8 *sine crimine* is *id est, sine peccato mortali* — a promise of
  perseverance, not a covert rebuke.
- **Later reception, read at its own locus: Cornelius a Lapide**,
  *Commentaria in omnes D. Pauli epistolas* (Antwerp 1614), on 1 Cor 1:4–8 verse
  by verse, in the optical layer this repository tracks (physical lines
  40030–40130; binding in `research/source-bindings.toml`). He glosses the
  lection clause by clause and shortly: *in gratia Dei* is *propter gratiam Dei*;
  *in omni verbo et scientia* is *praedicationis Evangelii* and *spiritali eius
  intelligentia*, summed as *q.d. Gratias ago Deo, quod vobis copiosam per me et
  Apollo exhibuerit praedicationem et doctrinam Evangelii, eiusque sensum et
  intelligentiam*; *sicut testimonium Christi confirmatum est in vobis* is read
  of the two things named, *quibus, ceu testimoniis duobus, Christiana fides
  fundata et firmata est in vobis*; *expectantibus revelationem* is *in secundo
  illius adventu, quando omnium gratiarum copiam et consummationem in gloria
  caelesti a Christo accipietis*; and *in die adventus* is an ellipsis,
  *supplendum enim est, ut sitis et appareatis sine crimine*.
- **Where a Lapide stands against Chrysostom, and it is at the Epistle's last
  verse.** Chrysostom reads *qui et confirmabit vos … sine crimine* as covert
  accusation — the words "mark them out as still wavering, and liable to
  reproof." A Lapide reads the same clause as addressed to a church most of whose
  members were sound: *loquitur Apostolus toti Ecclesiae, in qua plerique erant
  sancti et inculpati, etiamsi pauci aliqui schismata sererent* — those few being
  the ones the next verse rebukes — and he divides the promise itself — *quantum est
  ex parte sua, id est, gratiam dabit quae vos confirmare possit; et actu
  confirmabit, si eam recipere, ea uti, et vos confirmare in Christi fide et
  charitate velitis.* **The two are not reconcilable by emphasis alone**: for
  Chrysostom the praise of vv. 4–8 is strategy against the whole body, for a
  Lapide it is true of the body and the rebuke begins only at v. 10. A study may
  use either; it may not report them as one. This is a seventeenth-century Jesuit
  exegete and not a Father, and the record labels it so.
- **How that Latin is quoted, and its limit.** The layer is uncorrected optical
  recognition of a black-letter printing with long *s*: it prints *fanái* for
  *sancti*, *teflimonium* for *testimonium*, *przdicationem* for
  *praedicationem*, *czlefti* for *caelesti*. The Latin above is therefore given
  in ordinary orthography, which is an editorial normalisation of a damaged
  layer and **not** a transcription of what the 1614 page prints; the page images
  of the registered facsimile were not opened. No claim here turns on a letter,
  and where the layer is damaged past confident reading the sense is given in
  English instead of being emended into Latin.
- **What the index returns for the Epistle, and what the library holds.**
  `tools/commentary-work-index discover --passage "1 Cor 1:4"` returns fourteen
  rows, all at chapter granularity. **Read**: Chrysostom (*Hom. in 1 Cor.* 2, on a
  public delivery; § 6.3); Theodoret (PG 82, above); Thomas Aquinas, *Super
  Epistolas S. Pauli lectura* (Corpus Thomisticum, above); Cornelius a Lapide
  (*Commentaria in Scripturam Sacram* in the index; the registered Pauline
  volume, above). **No registered route**: Origen, *Fragmenta* (the library holds
  *Contra Celsum*, *De principiis* and the *Selecta in Psalmos*); Theophylact, two
  rows (John only is held); Peter Lombard, *Collectanea* (the *Sententiae* only);
  Rabanus Maurus, *Enarrationes in epistolas*; Hugh of Saint-Cher; Nicholas of
  Lyra; Denis the Carthusian, two rows; Willem Hessels van Est. None of these is
  printed in a registered Migne volume. The later reception of the Epistle is
  therefore four witnesses read at their loci, bounded beyond them by the
  registered library and that index.
- **Where the four stand at v. 8, and it is a real division.** Chrysostom and
  Theodoret read *confirmabit … sine crimine* as showing the Corinthians still
  liable to reproof — for both the praise of vv. 4–7 is the physician's
  preparation for the cure, though Theodoret insists it is also true. Aquinas and a
  Lapide read v. 8 as a promise to a body most of which was sound — *sine peccato
  mortali* (Aquinas), *toti Ecclesiae, in qua plerique erant sancti et inculpati*
  (a Lapide) — and Aquinas refers the riches to the more perfect in whom the rest
  share by charity. Theodoret and Aquinas agree that the thanksgiving is meant to
  make the correction bearable. § 4.7 records the division.

### 3.7 Offertory — the antiphon cited to Ex 24:4–5 (no. 1675)

- **Direct patristic exegesis of Ex 24:4–5: none located at its own locus.**
  `tools/commentary-work-index discover --passage "Ex 24:4"` returns sixteen rows:
  Augustine, *Quaestiones in Heptateuchum*; Cornelius a Lapide; Gregory of Nyssa,
  *De vita Moysis*; Isidore, *Quaestiones in Vetus Testamentum*; Nicholas of Lyra;
  Rabanus Maurus, *Commentaria in Exodum*; Theodoret, *Quaestiones in
  Octateuchum*; Bede, *De tabernaculo* (two rows); Cyril of Alexandria, *Glaphyra
  in Pentateuchum*; Denis the Carthusian (two rows); Hugh of Saint-Cher; Ephrem,
  *Commentary on Exodus*; Procopius of Gaza, *Commentarii in Octateuchum*; Rupert
  of Deutz, *De sancta Trinitate*. Two have registered routes and both were
  opened:
  - **Theodoret**, *Quaestiones in Exodum*, in the registered PG 80 facsimile,
    read on the page images of **cols. 277–280** (PDF pp. 147–148): *interrogatio*
    59 is on Ex 23:31 and *interrogatio* 60 on the tabernacle of Ex 25. **He asks
    no question on Ex 24.** A clean negative, bounded by this work.
  - **Cornelius a Lapide**, *Commentaria in Pentateuchum*, below.
  - **No registered route**: Augustine's *Quaestiones in Heptateuchum* (the
    library holds none of the *Quaestiones*); Gregory of Nyssa's *De vita Moysis*
    (the library holds *De hominis opificio* and the *Oratio catechetica*);
    Isidore; Rabanus; Bede's *De tabernaculo* (the library holds his Luke and
    Genesis commentaries, and PL 92, which carries neither); Cyril's *Glaphyra*
    (his John and Luke only); Ephrem; Procopius; Rupert's *De sancta Trinitate*
    (PL 170, which is registered, carries his *De divinis officiis* and not the
    *De Trinitate*); Lyra, Denis, Hugh.
- **Later reception at the Offertory's own locus: Cornelius a Lapide**,
  *Commentaria in Pentateuchum* (1700 folio), on Ex 24:4–8, in the registered
  optical layer (fetched 2026-09-22, digest matched; physical lines 79138–79245;
  binding in `research/source-bindings.toml`). **The layer is uncorrected
  recognition of a long-*s* folio and no page image was opened**, so what follows
  is given in normalised orthography and is a reading of the layer, not of the
  page. At v. 4 the twelve *tituli* are twelve rude stones set up *ut sacrificia
  haec, quibus foedus inter Deum et populum sanciebatur, a duodecim tribubus offerri
  significaret*, and *aliqui probabiliter putant* the altar itself was built of
  them (Abulensis, Cajetan). At v. 5 the *iuvenes* who offered are, with the
  Chaldee, the firstborn, *hi enim in lege naturae erant sacerdotes*, before the
  Aaronic priesthood; he reports Augustine (*quaest.* in Leviticus) as taking them
  for the sons of Aaron. At vv. 6–8 the covenant sealed in blood is the type of
  the new: *Simili modo Christus Dominus novum foedus et testamentum sancivit se
  ipso, et sanguine suo quasi victima … idque expressit in institutione
  Eucharistiae, dicens:* — the words of institution follow, which the layer
  garbles past reading and which are therefore not transcribed here — and he draws
  from it *contra Sacramentarios validum pro veritate corporis Christi …
  argumentum*: if the old covenant was sanctioned with true blood, so was the new. **This is a seventeenth-century Jesuit and not a Father**, and
  he comments on Ex 24, not on the Offertory, whose compiled wording (§ 5.1.4)
  none of this addresses. It is nonetheless the first witness this record has at
  the cited verses themselves, and it joins the altar of v. 4 to the covenant
  blood of v. 8 and to the Eucharist, as Chrysostom on Heb 9 joins that blood to
  the remission of sins.
- **Adjacent direct exegesis, read at its own locus: John Chrysostom**,
  *Homiliae in epistulam ad Hebraeos* 16 (NPNF1-14), on Heb 9:18–22, which
  narrates the same Sinai sacrifice from Ex 24:6–8: "Tell me then why is the book
  of the testament sprinkled, and also the people, except on account of the
  precious blood, figured from the first? … With this blood not Moses but Christ
  sprinkled us, through the word which was spoken; This is the blood of the New
  Testament, for the remission of sins … there indeed the body was cleansed
  outwardly, for the purifying was bodily; but here, since the purifying is
  spiritual, it enters into the soul, and cleanses it, not being simply sprinkled
  over, but gushing forth in our souls." He also notes the qualification in
  *almost all things are by the law purged with blood*: "Because those [ordinances]
  were not a perfect purification, nor a perfect remission, but half-complete and
  in a very small degree."
- **This is exegesis of Hebrews' account of the covenant sacrifice, not of Ex 24:4–5,
  and the matrix labels it so.** It is the nearest direct witness located to what
  the Offertory narrates. Its value for this formulary is that it connects Moses'
  covenant sacrifice to the *remission of sins* — which is the Gospel's own
  subject — in a checked Father at his own locus.
- **Documented reception of the compilation.** Rupert of Deutz expounds this
  Offertory, with the verse the 1962 no longer prints (*Videns Moses, procidens
  adoravit … dimitte peccata populi tui*), as the pastor's model of intercession,
  and Guéranger prints both ancient verses; § 2.7 and § 3.11. That is how the chant
  was read in the Mass, not what a Father said of Exodus.
- **Textual state:** the antiphon is a compilation; see `propers/verified.md`,
  *The Offertory's wording*. Its four non-Exodus-24:4–5 clauses were located by
  literal search of the whole tracked Clementine, and the Greek was checked.

### 3.8 Communion — Ps 95:8–9 (no. 1677)

- **Direct: Augustine**, *Enarr. in Ps.* 95 §§ 9–10, on exactly the two clauses
  the antiphon takes:
  - v. 8, *Tollite hostias, et introite in atria eius*: "Confession is a present
    unto God. O heathen, if you will enter into His courts, enter not empty. Bring
    presents. What presents shall we bring with us? The sacrifice of God is a
    troubled spirit: a broken and a contrite heart, O God, shall not Thou despise.
    Enter with an humble heart into the house of God, and you have entered with a
    present. But if you are proud, you enter empty … Rejoice, because you have
    entered into the courts; rejoice, because you are being built into the temple
    of God. For those who enter are themselves built up, they themselves are the
    house of God."
  - v. 9, *adorate Dominum in aula sancta eius*: "O worship the Lord in His holy
    court: in the Catholic Church; this is His holy court. Let no man say, Lo,
    here is Christ, or there."
  - The whole exposition is governed by the psalm's title, which Augustine takes
    as its key: "While the house was being built, after the captivity … men were
    held captive under the devil, and served devils; but they were redeemed from
    captivity … He poured forth His Blood, and bought the whole world."
  - **Augustine's own Latin was read at the same two sections**, in the file this
    checkout tracks (`…wikisource-part-10-latin-text/enarrationes-part-10.txt`,
    bound in `research/source-bindings.toml`): *IN PSALMUM XCV* at its line 108,
    § 9 at line 119 — *«Tollite hostias, et introite in atria ejus.» … Confessio
    hostia est Deo … Cum humili corde intra in domum Dei, et cum hostia intrasti.
    Si autem superbus es, inanis intras* — and § 10 at line 120, *«Adorate
    Dominum in atrio sancto ejus:» in catholica Ecclesia; hoc est atrium sanctum
    ejus.* **His lemma at v. 9 is *in atrio sancto ejus*, not *in aula sancta***,
    which is a second witness on the psalter question § 5.1.7 had left standing on
    Cassiodorus alone.
  - **And in Migne's own print**, PL 37, PDF p. 110 = cols. 1233–1234, read on the
    page image: § 9 *[vers. 8.] Afferte Domino gloriam nomini ejus. Tollite hostias,
    et introite in atria ejus … Confessio hostia est Deo … Cum humili corde intra in
    domum Dei, et cum hostia intrasti. Si autem superbus es, inanis intras*; § 10
    *[vers. 9, 10.] Adorate Dominum in atrio sancto ejus: in catholica Ecclesia; hoc
    est atrium sanctum ejus*, and at the head of col. 1234 *in atrio sancto adoro
    Deum meum*. The tracked transcription is faithful to Migne at every clause this
    row quotes.
- **Direct: Cassiodorus**, in Ps. XCV, host sectiones 13 and 14, on exactly the
  same two clauses, read in the registered Latin:
  - v. 8, *Tollite hostias, et introite in atria eius*: *Hostias non victimas
    pecudum dicit, sed conscientiae pura libamina, unde non sanguis currat, sed
    piae lacrymae defluant. Istae sunt hostiae quas in quinquagesimo psalmo dixit:
    Cor contritum et humiliatum Deus non spernit.* And on the order of the two
    imperatives, which Augustine does not press: *Sed considera quia prius posuit,
    tollite, et sic introite: quia qui tales hostias non portant, in atria Domini
    non iudicantur intrare.* Then the plural: *Non est autem otiose suscipiendum,
    quod plurali numero posuit atria. Atria enim Domini sunt apostoli vel
    prophetae, per quos fidelis populus intrat ad Dominum.*
  - v. 9, *adorate Dominum in atrio sancto eius*: *Nec vacat quod in anteriore
    versu atria posuit; hic vero singulariter atrium dicit, quia ex illis atriis,
    id est, patriarchis, apostolis et prophetis in istud atrium catholicae
    duntaxat Ecclesiae pervenitur, ubi eius potentia maiestatis adoratur.*
  - On the title, which he too takes as the key, and which he reads on two levels
    at once (sectio 2): *Quantum ad litteram pertinet, tempus illud significatur
    in titulo cum a Zorobabel filio Salathiel post captivitatem templum
    Ierosolymitanum constat esse reparatum … Destructa domus aedificatur, quando
    anima post captivitatem peccati ad intelligentiam veritatis coeperit (Domino
    praestante) remeare. Domus enim ista, id est universalis Ecclesia, in qua
    Christus inhabitat, vivis lapidibus semper exstruitur.*
- **Direct, in Greek: Theodoret**, in Ps. XCV, PG 80, **cols. 1647–1648** (page
  image, PDF p. 872). His lemma is *Ἄρατε θυσίας, καὶ εἰσπορεύεσθε εἰς τὰς αὐλὰς
  αὐτοῦ. Προσκυνήσατε τῷ Κυρίῳ ἐν αὐλῇ ἁγίᾳ αὐτοῦ*, and he reads it of the
  Church's sacrifice: *Θυσίας λέγει τὰς λογικάς, ἃς ὁρῶμεν διηνεκῶς ὑπὸ τῶν ἱερέων
  προσφερομένας καὶ ἱερουργουμένας. Καὶ τῶν αὐλῶν δὲ τὸ πλῆθος τὰς ἐκκλησίας
  δηλοῖ* — "he means the rational sacrifices which we see continually offered and
  sacrificed by the priests; and the plurality of the courts signifies the
  churches." The command is not to the Jews, *ἀλλὰ ταῖς πατριαῖς τῶν ἐθνῶν, αἳ τὰς
  τῆς καινῆς διαθήκης θυσίας ἐν ταῖς ἐκκλησίαις προσφέρουσι*, with Mal 1:10–11.
- **Direct, in Greek: the *Expositiones in Psalmos* printed under Athanasius's
  name**, PG 27, **cols. 415–416** (page image, leaf n214). The title is read of
  the Church founded through the whole world after the release from spiritual
  captivity; and at vv. 7–9, *Πατριὰς καλεῖ τοὺς τῶν Ἐκκλησιῶν ἡγουμένους, ἱερέας
  φημὶ καὶ προέδρους … καὶ θυσίας αὐτῷ ἀναφέρειν νοητάς· ἀναφέρειν δὲ ἐν ταῖς θείαις
  αὐτοῦ αὐλαῖς, δηλαδὴ ταῖς ἐκκλησίαις* — the "families" are the leaders of the
  churches, "priests, I mean, and presidents", who offer him spiritual sacrifices
  in his divine courts, that is, the churches.
- **Direct, later: Bellarmine**, Ps 95 v. 8 (tracked English, line 3431): the
  verse alludes to the Jews' offering of victims when they went up to the temple;
  for the gentiles invited to the Church the sacrifices are "those spiritual
  sacrifices of which St. Peter speaks … the sacrifices of a contrite heart,
  confession of sins, prayer, fasting, alms, and the like. This may also apply to
  the Eucharistic sacrifice, that took the place of all the Jewish sacrifices,
  according to the prophecy of Malachy, and which is offered … to God, by the
  converted gentiles, through the hands of the priests of the New Testament." His
  v. 9 paragraph in this abridged English does not expound the court.
- **Where the five stand.** All five read the courts of the Church. They divide on
  what the *hostiae* are: a contrite and humble heart for Augustine and
  Cassiodorus, with no word of an altar; the rational sacrifices the priests offer
  continually in the churches for Theodoret, and spiritual sacrifices offered by
  the churches' priests and presidents in the PG 27 expositions; both, in that
  order, for Bellarmine, who names the Eucharist in the second place. And they
  divide on the courts: Augustine reads the holy court simply as the Catholic
  Church; Cassiodorus makes the plural *atria* of v. 8 the apostles and prophets
  and the singular *atrium* of v. 9 the Church arrived at; Theodoret makes the
  plural the many churches. These are real differences of exegesis inside an
  agreement about the psalm, and the study may use any without implying the
  others. **The sacerdotal reading of *Tollite hostias* is now a checked reading of
  two Greek witnesses and a Doctor**, and the study may say so at this verse.
- **Note for the study.** Augustine's §§ 10–11 are heavily anti-Donatist ("they
  are very ungrateful for their price … who say that the price is so small that it
  bought the Africans only"). Same caution as § 3.3.

### 3.9 Collect, Secret and Postcommunion (nos. 1670, 1676, 1678)

- **Direct patristic exegesis: none, and none is to be expected.** These are
  composed Roman orations, not scriptural texts, and no Father comments on them.
  Their documented reception is their **transmission**, recorded in § 2: the Old
  Gelasian at III. xiv, the Hadrianum at CXXXVII, and the variant readings of the
  printed editions.
- **What the transmission shows about the wording itself.** The 1962's `efficis`,
  `cognoscimus`, `nos eius` and `dignis moribus` (without *et mentibus*) each
  match a reading Wilson's apparatus records in one or more witnesses; none is a
  1962 innovation. **For `dignis moribus` this no longer rests on the apparatus
  alone.** The Gelasian's own Book I § lix now stands located in the registered
  optical layer at physical lines 12585–12598 (§ 2.1), and the printed text there
  reads *ut sicut tuam cognovimus veritatem sic eam dignis moribus assequamur* —
  the manuscript text itself, not Wilson's note about it.
- The Secret's *uníus summæ divinitátis partícipes* and the appointed Trinity
  Preface stand together on the printed page. That they do is a fact;
  what to make of it is the editor's, and `research/interpretations.md` says so.

### 3.10 The Trinity Preface (appointed by rubric)

- Appointed by the printed direction after the Secret and by RGMR 494 b; text at
  printed p. 293, no. 1082. Not a proper of this formulary, not reproduced, and
  not given a reception sweep here.

### 3.11 Documented reception of the compilation: the liturgical commentators

**This section is not exegesis of the passages, and nothing in it may be cited as
the Fathers'.** It records what two named liturgical commentators say of this
Sunday's Mass as their books gave it — the kind of witness the three-document
contract names as documented reception of the compilation. Their Mass is not in
every part the 1962's (§ 2.7), and each reading below is attributed to its author.

- **Rupert of Deutz**, *De divinis officiis* XII.18–19, PL 170, cols. 326–327,
  read on the page images (§ 2.7 gives the identification and § 6.3 the digests).
  He reads the whole Eighteenth-Sunday Mass as addressed to *eidem, qui vocatus
  est superius, id est praelatus est domui Christi, et curam animarum suscepit*:
  - the Offertory: *Sint sicut ipse Moses, de cujus exemplo, quod ecclesiastici
    sequi debeant rectores, longa et valida declamatio est in offerenda:
    Sanctificavit Moses, et versibus ejus* — the rectors must seek *non tam
    praeesse … quam prodesse*, *ut portare possint peccata populi, et a subditis
    suis avertere iram Dei. Bene ergo cum hoc evangelio positum est in offerenda
    exemplum Mosi* — the Gospel meant being the chair of Moses;
  - the Introit: *Da pacem … id est eorum quos nobis commisisti, peccata dimitte.
    Pax enim Dei, peccatorum remissio est*;
  - the Epistle: *Talibus in praesenti lectione epistolae dicit Apostolus: Gratias
    ago Deo meo pro vobis*;
  - the Gradual verse: *Fiat pax in virtute tua, id est remissio peccatorum in
    Spiritu sancto tuo*;
  - the Communion: *Tollite hostias … videlicet quia vestrum officium est: ut pro
    subditis interveniatis exemplo Mosi, in conspectu Domini stantes in
    confractione cordis* (Ps 105:23).
  At the Nineteenth Sunday, where his books put this Gospel, he reads the bearers
  of the paralytic as the prelates: *ipsorum est offerre paralyticum in lecto
  jacentem, id est orare pro his quorum peccata animas … detinent, et ita pro eis
  intervenire, ut videns Dominus fidem illorum, dicat: Confide, fili*; and the
  Introit *Salus populi* as Christ's own testimony *quod … curatione paralytici
  comprobatur, videlicet quia potestatem haberet in terra dimittendi peccata*.
  **Rupert therefore reads peace as the remission of sins and the Mass as the
  office of those who intercede for the people's sins** — but his Mass paired that
  Offertory with another Gospel, and the forgiveness he reads into its chants is
  the pastor's intercession, not the power of absolution.
- **Prosper Guéranger**, *The Liturgical Year*, Time after Pentecost vol. II
  (series vol. XI), English 1909, printed pp. 393–409, in the tracked facsimile,
  checked on the page images (§ 6.3). He reads the Epistle's gifts of the Ember
  ordinations — *the powers conferred by the imposition of the bishop's hands on
  the ministers of the Church are the most marvellous gift that is known on earth*
  (p. 394) — the Introit's prophets as *the pastors, whom the Church sends* (pp. 394–
  395), and the Gradual's house as heaven and also *the temple in which we are now
  assembled, and into which we are introduced by … His priests* (p. 401). He
  reports Rupert's other Gospel and its harmony with the Moses Offertory (pp.
  402–403), and then reads the present Gospel of the same pastors: *the faithful …
  are now invited to meditate upon the prerogative which these same men have of
  forgiving sins and healing souls* (p. 403; the book italicises *forgiving sins*,
  which this quotation cannot show), with the power of the keys and the
  sacrament of Penance (pp. 403–404). He also reads the paralytic as the human
  race, carried to the Church by the apostles' faith (p. 405). The Offertory's
  Moses is *the type of those faithful prophets mentioned in the Introit … the
  model of those true leaders of God's people, who devote themselves in order to
  procure mercy and peace for those whom they guide* (p. 406).
- **What this changes.** The ministerial and priestly sense of this Sunday's Mass
  is no longer only the editor's: it is **documented reception** — Rupert's
  (intercession) and Guéranger's (the power of forgiving sins), each commenting on
  the Mass and not on Matthew. It is still not a Father's reading of Mt 9:8 (§ 4.3),
  and the study must say whose it is.

---

## 4. Material disagreements preserved

### 4.1 Which city? Chrysostom, Jerome, Augustine

Chrysostom (*Hom. in Matth.* 29): "By His own city here he means Capernaum. For
that which gave Him birth was Bethlehem; that which brought Him up, Nazareth;
that which had Him continually inhabiting it, Capernaum."

Jerome (*Comm. in Matth.* I, PL 26, col. 54, read at his own locus this round):
*Civitatem ejus non aliam intelligimus quam Nazareth, unde et Nazaræus appellatus
est.* He gives no reason and offers no alternative.

Augustine (*De cons. evang.* II. xxv. 58) holds the difficulty open and offers two
solutions rather than one: Galilee as a whole may be called Christ's city, and
Capernaum was its metropolis; or Matthew may have passed over the interval in
silence. He explicitly says the question "would be more difficult to solve if
Matthew mentioned Nazareth by name."

Aquinas (*Super Matth.* IX, Venice 1745, p. 121) does harmonise it, and in two
ways: Christ had three cities — Bethlehem *ratione nativitatis*, Nazareth *ratione
educationis*, Capernaum *ratione conversationis, et operationis miraculorum* — so
*civitatem suam* is rightly said of Capernaum; or, with Augustine, Capernaum was
Galilee's metropolis; or the Evangelists pass over a journey *per Nazareth* to
Capernaum. Before any of that he reads the words allegorically: *in civitatem
gentium, quae sibi datae sunt* (Ps 2:8), with the boat as the cross or the Church.

**This is a real disagreement among the Fathers and it is not harmonised here**;
Aquinas's harmony is his, and a study that uses it must say so. It matters for the
study because Hilary's reading — *Dei civitas fidelium plebs est* — depends on
leaving the identification open, and Aquinas's allegory (*civitas gentium*) is a
second reading of the same kind, at his own locus.

### 4.2 Whose faith? Jerome against Chrysostom

Jerome (*Comm. in Matth.* I, PL 26, col. 54, at his own locus), of *videns Iesus
fidem illorum*: *Videns autem Jesus non ejus fidem qui offerebatur, sed eorum qui
offerebant* — not the faith of the man who was offered, but of those who offered
him. He has already given the reason a sentence earlier, and it is physical rather
than theological: *quia ipse ingredi non valebat*.

Chrysostom (*Hom. in Matth.* 29) states the same starting point and then refuses
it: "Seeing, it is said, their faith; that is, the faith of them that had let the
man down … **Or rather, in this case the sick man too had part in the faith; for
he would not have suffered himself to be let down, unless he had believed.**"

Aquinas (*Super Matth.* IX, p. 121) takes neither side outright: *Curat aliquando
Dominus aliquem propter fidem suam: aliquando propter preces suas, et aliorum* —
sometimes for the sick man's own faith, sometimes for his prayers and those of
others — and he reads the bearers tropologically as *illi qui suis monitionibus
portant eum ad Deum*. Rupert, commenting on the Mass (§ 3.11), reads the bearers as
the prelates who offer the sinner by prayer; that is liturgical reception, not
exegesis, and it sides with Jerome's *fides offerentium*.

**This disagreement is load-bearing** for any reading of the formulary that turns
on the Collect's *tibi sine te placére non póssumus*, and it is preserved in
`research/interpretations.md` § 3 rather than smoothed.

### 4.3 The power to forgive given "to men": what each checked witness says

Chrysostom is emphatic that *qui dedit potestátem talem homínibus* records an
**inadequate** confession: "they still creep upon the earth … had they well
established these things in their own minds, going on orderly they would have
known that He was even the Son of God. But they did not retain these things
clearly."

**No Father checked here draws the ministerial reading from v. 8.** Jerome, read
whole at his own locus in PL 26, cols. 55–56, comments on vv. 7–8 in a single
sentence about the risen soul carrying its bed, and goes straight to v. 9.
Augustine at *De cons. evang.* II. xxv does not reach the verse. Hilary, as Aquinas
reports him on v. 8, reads *hominibus* of the power *ut fiant filii Dei* (Jn 1:12)
— adoption, not absolution. That negative stands.

**But the question is no longer answered by the Fathers alone**, and three
witnesses checked on the second re-entry each bear on it at a different place:

- **Aquinas, at v. 6, at his own locus** (*Super Matth.* IX, Venice 1745, p. 122):
  *Videtur quod per hoc non ostendatur, quia etiam ipsi Apostoli habebant
  potestatem. Sed dicendum, quod ipsi habebant per viam administrationis, non
  auctoritatis.* He raises the Apostles' power to forgive sins as an objection to
  the verse's proof of Christ's divinity, and answers that they have it by way of
  ministry, not of authority. **This is a Doctor connecting Mt 9:6 with the
  Apostles' power to forgive**, at the verse *authority-on-earth* already turns on
  (`research/interpretations.md` § 4.3); it is not a reading of v. 8, and it is
  made to protect the proof of divinity, not to found the ministry.
- **Rupert of Deutz, on the Mass** (§ 3.11): peace is *peccatorum remissio*, the
  Offertory's Moses is the pastor who intercedes for the people's sins, and the
  prelates offer the paralytic by prayer. Liturgical reception, not exegesis; and
  in his books this Offertory stood with another Gospel (§ 2.7).
- **Guéranger, on the Mass** (§ 3.11): the present Gospel invites the faithful *to
  meditate upon the prerogative which these same men* — the Church's pastors —
  *have of forgiving sins*, with the keys and Penance. A nineteenth-century
  liturgical commentator on the Tridentine Mass.

So the ministerial sense has a documented home: at v. 6 in Aquinas, as ministry
beneath Christ's authority, and in the liturgical commentators' reading of this
Mass. It has none in a Father at v. 8. The study may use it with those
attributions; it may not put it in Chrysostom's, Jerome's, Augustine's or Hilary's
mouth, and it must not present Rupert's reading as the 1962 Mass's own, since his
Mass had another Gospel.

### 4.4 Is the paralytic an individual or the Gentiles? Hilary against the literal readers

Hilary (through the Catena): *In paralytico autem gentium universitas offertur
medenda* — in the paralytic the whole body of the Gentiles is offered for healing;
and *fides enim sola iustificat*, which in his context means that the law could not
loose what faith looses.

Chrysostom, Augustine and Jerome all read the episode as an episode, and Jerome
gives the tropological application to the **individual soul**, in his own words
at PL 26, col. 55: *Juxta tropologiam interdum anima jacens in corpore suo, totis
membrorum virtutibus dissolutis, a perfecto doctore offertur curanda Domino, quæ
si misericordia ejus sanata fuerit, tantum roboris accipit, ut portet statim
lectulum suum.* The soul is **offered to the Lord for healing by a perfect
teacher**, and receives its strength afterwards.

**The word *precatores* is not Jerome's here.** *Unusquisque enim aeger petendae
salutis precatores debet adhibere* — "every sick man must employ intercessors" —
is the **Catena aurea's** wording, and § 3.5(b) records that it is not in PL 26 at
this pericope; § 10.1 says the same. An earlier draft of this record and of
`research/interpretations.md` § 3.2 attributed it to Jerome, and both now correct
it. Anything the study takes from Jerome's tropology must be the *perfectus
doctor* sentence; *precatores* may be cited only as the Catena's, and only with
that said.

Hilary's is a different order of reading, not a contradiction; the study must
present it as the allegorical sense and not as what the others say.

### 4.5 A disagreement that the evidence does **not** support

No disagreement was located among the checked witnesses about the meaning of
*Da pacem* — the only witness to it is Rupert, commenting on the Mass, who reads it
as *peccata dimitte* (§ 3.11) — about the Offertory's compilation, or about the
Collect's *sine te placere non possumus*. Where § 3.1 has no witness and § 3.7 has
only a later exegete at Ex 24 and a liturgical commentator on the chant, the study
must not manufacture a dispute to fill the space.

### 4.6 Is Ps 121 of the city rebuilt or of the heavenly city? The Greeks against the Latins

Chrysostom (PG 55, cols. 347–351) and Theodoret (PG 80, cols. 1879–1882) read the
psalm of the Introit verse and both Gradual verses **wholly of the earthly
Jerusalem rebuilt after the Babylonian captivity**: the exiles' joy at the news of
the return and at seeing the house of God again (v. 1), the city lying in ruins,
its towers thrown down and its walls cast down, to be built again (v. 3), the
tribes reunited (v. 4), peace prayed for walls, palaces and houses after the war
that destroyed them (v. 7). Neither offers an allegory of the Church or of heaven
at this psalm; Chrysostom's turn to his hearers is moral — Christians are slower
to the house of prayer than the returning Jews were.

Hilary (CSEL 22, p. 571) refuses exactly that reading: *non utique … hanc terrenam
et caducam … sed illam liberam et caelestem Hierusalem*. Augustine and Cassiodorus
read the city as the heavenly Jerusalem and the Church built of living stones, and
Augustine's lemma (*Jucundatus sum in his qui dixerunt mihi*, PL 37 col. 1619)
turns the verse to the companions who summon the singer.

Bellarmine holds both: the literal sense is the exiles' joy at the return, and the
psalm "treats of the celestial, and not the earthly Jerusalem" in the sense he
thinks the Holy Spirit chiefly intended.

**This is a material disagreement about what the psalm is about, and it is
preserved.** § 10.2's earlier sentence that the checked witnesses read the psalms
"of it and not of a place" is withdrawn: for Ps 121 two Greek Fathers read it of a
place and of nothing else. The study may take the Latin reading as its own
allegorical sense; it may not say the Fathers agree on it, and a literal sense
that ignores the return from exile ignores the only reading the Greek witnesses
give. At Ps 101:16 the division is narrower — Theodoret gives the verse a first,
historical sense and then says it was fulfilled properly only after the
Incarnation (§ 3.4) — and at Ps 95:8–9 there is none: Theodoret reads the courts as
the churches.

### 4.7 Is the praise of 1 Cor 1:4–8 true, and does v. 8 accuse? Four readers in two pairs

Chrysostom: the praise is strategy and v. 8's *unreprovable* "marks them out as
still wavering, and liable to reproof." Theodoret (PG 82, cols. 229–232): Paul
"first tends their hearing, so that the cure may be received," **and** what he says
is true, for he thanks God for gifts really given; and *ἀνεγκλήτους* "showed them
as for the present liable to charges." Aquinas (*Super I Cor.* 1 lect. 1): the
thanks are given *ut correctionem suorum defectuum tolerabilius ferant*, but the
riches belong to the more perfect and are shared by charity, and *sine crimine* is
*sine peccato mortali* — a promise. A Lapide: the Apostle speaks *toti Ecclesiae,
in qua plerique erant sancti et inculpati*, and the rebuke begins at v. 10.

So on v. 8 Chrysostom and Theodoret stand against Aquinas and a Lapide; on the
purpose of the thanksgiving Theodoret and Aquinas agree that it prepares a
correction, and Theodoret alone insists in terms that it is also true. The
division at v. 8 is real and the study may not report the four as one.

---

## 5. Negative results and unreached corpora

### 5.1 Searched and not found

Each of the following was a real search, and each negative is bounded by the
corpus named. A negative here means the search did not find it, not that it does
not exist.

1. **Direct patristic exegesis of Ecclus 36:18.** Searched: the repository's
   passage→work index for Sirach 36 (which returns only medieval and later Latin
   commentators, at chapter granularity); the New Advent Fathers collection by
   direct retrieval of the works this formulary's other elements led to. No
   ancient exegesis of the verse was located, and no reachable text of Rabanus
   Maurus's *Commentaria in Ecclesiasticum* or of the *Glossa ordinaria* on
   Ecclesiasticus was found. **Recorded as a negative; the study says so.**
2. **`Da pacem` as a scriptural phrase.** A literal, diacritic-insensitive search
   of the **whole** tracked Clementine Vulgate
   (`src/sources/bibles/clementine-vulgate/chapters`, 73 books) for `da pacem`
   and `da pacem domine` returns **zero** occurrences. The antiphon's opening
   words are in no verse of that edition.
3. **`preces servi tui` as a scriptural phrase.** Same search: **zero**
   occurrences in the Clementine. `plebis tuae Israel` returns exactly one,
   Luke 2:32. `populi tui Israel` returns nine, of which 3 Kings 8:30 and
   2 Par 6:21 are Solomon's dedication prayer and are the nearest shape.
4. **The Offertory's clauses in Ex 24.** `sanctificavit altare` returns zero in
   the whole Clementine; `sacrificium vespertinum` returns three (Ps 140:2,
   1 Esd 9:4, 4 Kings 16:15), none in Exodus; `in odorem suavitatis` returns ten,
   the nearest being Ex 29:41; `in conspectu filiorum Israel` returns five,
   including Ex 24:17. The Greek was checked at Ex 24:4, 5 and 17 in the CATSS
   morphological Septuagint and supplies none of them.
5. **The orations in the Veronense.** § 2.4. Zero, by literal search of the whole
   registered optical layer.
6. **A second occurrence of the Secret in the Gelasian — searched, then found.**
   The earlier literal search of the registered optical layer on `summaeque
   diuinitatis`, `diuinitatis participes` and `ueneranda commercia` returned, of
   those three strings, only the Book III occurrence of the Secret, at physical
   line 21570, **and** — this record previously missed it — one further hit for
   `ueneranda commercia` at physical line **11487**, in the Exsultet, where the
   layer reads *istius mystica et veneranda commercia !* (line 11485, which an
   earlier draft of this record gave, reads *resurrectionis vexilla® suscepit\**
   and carries no occurrence). That is the correct statement of what those three probes return.
   **The Book I occurrence has now been located**, at physical lines 12585–12598,
   and § 2.1 records what it reads. It was invisible to those probes because the
   scan prints `commerda` for *commercia*, `partidpes` for *participes*,
   `efiecisti` for *effecisti* and `summae*` for *summaeque*; a probe on `dignis
   moribus`, the very reading Wilson's apparatus assigns to V at I. lix, finds it
   at once — and returns **exactly one hit in the whole layer, physical line
   12598**, the Book I occurrence. **It does not return the Book III occurrence,
   and cannot**: physical line 21574 reads `w/n». Jjgjjg moribus et mentibus *
   assequamur. Per. y`, the scan printing `Jjgjjg` for *dignis*. A probe on
   `moribus et mentibus` does return that line, and is how it was located. The
   receipt is corrected here because the earlier draft reported two hits; the
   conclusion it was offered for is unchanged, and the correction is an instance
   of this paragraph's own general lesson rather than an exception to it. The
   page image of Book I was still not opened, and nothing here needs it.
   **The general lesson is recorded rather than the particular fix:** a literal
   probe over an OCR layer tests the scanner's spelling, not the book's, and a
   negative from one is only as wide as the strings tried.
7. **A Roman Psalter witness** for the Communion's `in aula sancta eius`. None was
   reached. Two candidate web deliveries returned 404 or nothing. The reading is
   attested in 1862 and 1962; its psalter is unresolved. **Three data now stand
   against *aula*, one carried from the previous round and two added here.**

   - **Cassiodorus**, expounding the verse in the sixth century, lemmatises it
     *Adorate Dominum in atrio sancto eius* and builds his whole exposition on
     *atrium* standing against the plural *atria* of v. 8 (§ 3.8), so the psalter
     he read did not have *aula* there.
   - **Augustine's own Latin has the same lemma**, and this no longer rests on
     one witness. The tracked Migne Latin of the *Enarrationes* reads, at *in
     Psalmum XCV* § 10, *«Adorate Dominum in atrio sancto ejus:» in catholica
     Ecclesia; hoc est atrium sanctum ejus* — and again inside the exposition,
     *in atrio sancto adoro Deum meum* (§ 3.8). **This no longer rests on the web
     transcription**: Migne's own print, PL 37 col. 1233, read on the page image on
     the second re-entry, has the same lemma, *Adorate Dominum in atrio sancto
     ejus* (§ 3.8). Augustine and Cassiodorus, who
     divide over what the court *is*, agree without qualification about what the
     verse *says*.
   - **Migne's own print of Cassiodorus was opened this round and carries the
     same lemma.** The registered optical layer of PL 70 reads, at physical line
     52417 (between the layer's column markers 679 at line 52369 and 682 at
     52540), `323 Vers. 9. Adorate Dominum in atrto $ancl0` continuing at 52418
     `ejus; commoveatur a facie eju$ univer$a terra.` — that is, *Adorate Dominum
     in atrio sancto ejus*, with the scanner's damage left visible. The
     *atria*/*atrium* distinction the exposition builds on is legible in the same
     run, at 52413 (*Atria enim Domini sunt apostoli vel prophetae*) and at
     52443–52444 (*… atrium dicit, quia ex illis atriis, id est, patriarchis,
     apostolis et prophetis in istud atrium catholicae …*). **So the *atrio*
     reading is not an artefact of the Corpus Corporum transcription: Migne's own
     printing has it.** This is an optical layer and not a facsimile, no page
     image was opened, and nothing here is offered as Migne's letterform (§ 6.3).

   - **The Greek reads *αὐλή*, and the Latin translation Migne prints beside
     Theodoret reads *aula*.**
     Theodoret's lemma at Ps 95:9 (PG 80, col. 1648, page image) is *Προσκυνήσατε
     τῷ Κυρίῳ ἐν αὐλῇ ἁγίᾳ αὐτοῦ*, with the plural at v. 8 *εἰς τὰς αὐλάς*; the PG 27
     expositions paraphrase the same *αὐλαί*; and the Latin translation Migne prints
     facing Theodoret renders the lemma *Adorate Dominum in aula sancta ejus* (col.
     1647, page image). That the Greek behind both Latin readings is *αὐλή*, and
     that a Latin translator of Theodoret chose *aula* for it, are data,
     recorded; neither identifies the Missal's psalter.

   **What this does and does not settle.** It settles that both Latin expositors
   this study reads at this verse — Augustine in the fifth century and Cassiodorus
   in the sixth — had *atrio* in front of them, and that the
   Corpus Corporum files are faithful to Migne at this lemma. It does **not**
   identify the Missal's *aula sancta* with any psalter: no Roman Psalter, no
   Gallican or *iuxta Hebraeos* witness and no critical edition was opened, the
   chant's own transmission was not traced behind 1862, and *aula* remains a
   reading this record can place in the Missal and nowhere else.
8. **Cantus Index** for the chants of this formulary. Its full-text search
   requires JavaScript and returned no usable result to a plain HTTP client. No
   chant record for *Da pacem Domine*, *Laetatus sum*, *Sanctificavit Moyses* or
   *Tollite hostias* was retrieved from it, and none is cited from it. **A
   different database did serve**, and this round used it: gregorien.info, which
   the source library already registers and which § 2.3 now reports. The negative
   above is therefore about Cantus Index and nothing more.

### 5.2 Not reached, named so that a later run can take them up

**How this section is now kept.** Before anything is recorded here as unreached,
the repository's own registered holdings are swept for it with
`tools/source-library` and `tools/commentary-work-index`, and a registered route
is tried before an external delivery. That discipline was not applied in the first
pass of this stage and four witnesses were recorded as out of reach that the
repository already registered; the entries below say, per witness, which route was
tried and what it gave.

**The same sweep was then run a second time, over the witnesses the study
actually uses, and that is how § 6.3 came to be rewritten.** The first
application of the rule asked only *whether the library holds what this record
called unreached*. It did not ask the other question — *does the library hold
what this record is already quoting?* — and the answer was yes for five of the
eight deliveries § 6.3 had listed as unregistered. Claiming the discipline while
sweeping only half the ground is the defect this paragraph exists to prevent, and
it survived one round.

**It survived a second round too, in a third form, and the second re-entry
corrected it.** Both earlier sweeps asked the library by *work record*: does it
register this author's commentary on this book? That misses every text the
library holds inside a collected or whole volume registered under another work —
Chrysostom's Ps 121 inside a PG 55 record described by his Ps 117, Theodoret's 1
Corinthians inside a PG 82 record named for Galatians, Aquinas's Matthew inside a
Venice *Opera* volume, Augustine's Ps 121 inside PL 37. And the index was queried
for five loci only (Sirach 36, Exodus 24, Ps 121:1, Mt 9:1, 1 Cor 1:4), and the
Ps 121:1 list was then presented as covering all three psalms. **The rule as now
kept**: `tools/commentary-work-index discover` is run for every appointed locus —
on 2026-09-22 for Ps 95:8, Ps 101:16, Ps 121:1, Ps 121:7, Mt 9:1, 1 Cor 1:4, Ex 24:4
and Sir 36:18 — and for each lead it returns, the registered work records **and**
the registered collected and whole volumes (the Migne volumes PL 24, 26, 30, 37,
56, 70, 78, 92, 105, 170 and PG 27, 29, 55, 57, 80, 82, and the *Opera* volumes) are
checked for the text before it is called unreached. The lists below are what the
index returned for the locus each names, and nothing is carried from one locus to
another. § 6.3 names, per reception witness, which registered route was tried and
what it gave, and every registered route deliberately not used, with its reason.

**Reached on the first re-entry, and no longer negatives.** Each is now in § 3 and bound in
`research/source-bindings.toml`.

- **Jerome, *Commentariorum in Matthaeum libri IV*, lib. I**, at Mt 9:1–8. The
  four external deliveries the first pass tried — Documenta Catholica Omnia,
  Latin Wikisource, IntraText, Corpus Corporum — still do not serve it, and that
  was never the route: the library registers
  `segment.jerome.commentariorum-in-evangelium-matthaei.vallarsi-migne-pl26-1845.pl26-columns-15-218`
  over the Migne PL 26 scan
  `artifact.jacques-paul-migne.patrologia-latina-volume-26.paris-1845.internet-archive-google-pdf-0d889bd6`,
  at artifact PDF pp. 13–116. The 63,426,233-byte scan was fetched, its SHA-256
  recomputed and matched (`0d889bd6…0245e4`), and Mt 9:1–8 read on the page images
  of PDF pp. 32–33 = PL 26, cols. 53–56. § 3.5 carries the readings.
- **Cassiodorus, *Expositio psalmorum*** on Pss 95, 101 and 121. Ps 101 needed no
  network at all: the whole exposition is a **tracked** file in this checkout,
  `…/monumenta-ps101-apparatus-latin-text/cassiodorus-ps101-latin.txt`, and the
  Alleluia verse stands at its sectio 22. Pss 95 and 121 were not held; both were
  fetched from the host the registered edition names, by the addressing rule that
  edition's record states, and are now registered under
  `edition.cassiodorus.expositio-psalmorum.latin-corpus-corporum-monumenta-web-2026-09-22`
  with their Latin retained. § 3.2, § 3.3, § 3.4 and § 3.8 carry the readings.
- **Hilary of Poitiers, *Tractatus super Psalmos*** at Ps 121. The library
  registers
  `artifact.hilary-of-poitiers.tractatus-super-psalmos.csel-22-zingerle-1891.ia-djvu-ocr-shilariiepiscopi22hilauoft`,
  and `tools/commentary-work-index discover` returns it for this psalm. The
  2,729,218-byte OCR layer was fetched, its SHA-256 recomputed and matched
  (`6b39d974…14a7fa`), and the *tractatus in psalmum CXXI* read whole at its
  physical lines 29495–30011, the next tractatus beginning at 30012. § 3.2 and
  § 3.3 carry the readings.
- **The Sextuplex, through the registered gregorien.info database.** See below.

**Reached on the second re-entry, by artifact coverage, and no longer negatives.**
Each is now in § 3 (or § 2.7 and § 3.11) and bound in
`research/source-bindings.toml`; § 6.3 gives the identities and digests.

- **Chrysostom**, *Expositio in Ps. CXXI*, in the registered whole-volume PG 55
  layer, cols. 347–351 (§ 3.2, § 3.3, § 4.6).
- **Theodoret**, *Interpretatio in Psalmos* on Pss 95, 101 and 121, and his
  *Quaestiones in Exodum* (a negative at Ex 24), in the registered PG 80
  facsimile (§§ 3.2–3.4, 3.7, 3.8); and his *Interpretatio in I Cor.* in the
  registered PG 82 layer (§ 3.6, § 4.7).
- **The *Expositiones in Psalmos* printed under Athanasius's name**, PG 27, on
  Pss 95 and 101 (§ 3.4, § 3.8).
- **Bellarmine**, *Explanatio in Psalmos*, on Pss 95, 101 and 121, in the tracked
  English (§§ 3.2–3.4, 3.8).
- **Augustine's own Latin in PL 37** on Pss 95, 101 and 121, and the augustinus.it
  delivery of Ps 101 sermo I (§§ 3.2–3.4, 3.8).
- **Aquinas**, *Super Matthaeum* on Mt 9:1–8, in the tracked Venice 1745 layer and
  its registered facsimile (§ 3.5, §§ 4.1–4.3); and *Super I ad Corinthios* on
  1 Cor 1:4–8, in the registered Corpus Thomisticum page (§ 3.6, § 4.7).
- **Cornelius a Lapide**, *Commentaria in Pentateuchum*, on Ex 24:4–8 (§ 3.7).
- **Rupert of Deutz**, *De divinis officiis* XII.18–19, and **Guéranger**, *The
  Liturgical Year* vol. XI, as documented reception of the compilation (§ 2.7,
  § 3.11).

**Still not reached, and why.**

- **Hilary of Poitiers, *Commentarius in Matthaeum* VIII** (PL 9, SC 254). No
  registered route exists: the library holds Hilary's *Tractatus super Psalmos*
  and not his Matthew commentary, and PL 9 is not among its Migne volumes. The
  same four external deliveries were tried again and none served it. His readings
  in § 3.5 remain reported ones — the Catena's on vv. 1–2 and Aquinas's lectura on
  v. 8 — and he is the **only** Father of the Gospel's four in that position.
- **Hesbert, *Antiphonale Missarum Sextuplex*** itself, the printed collation.
  Not held by this repository and not reached; no scan of it was located on a
  public route. **What the repository does hold, and what this record previously
  overlooked, is the gregorien.info chant database's report of the same six
  books**, registered at
  `edition.gregorien-info.gregorien-info-chant-database.web-2026-09-05`. Two of
  its pages are registered artifacts and were re-read and digest-matched this
  round; the Sunday's own calendar day, 823, is an unregistered delivery of the
  same host and was read live. § 2.3 records what they give, including the six
  AMS numbers on the *Timebunt gentes* chant page and the whole chant-set of this
  Sunday with its manuscript sigla. **The printed Hesbert is still what would
  settle it**: everything in § 2.3 from that host is one database's reading, not a
  collation, and § 10.5 keeps the bound.
- **The psalm leads, locus by locus, as the index returns them.** Every row
  matched at chapter granularity.
  - **Ps 95:8** (thirteen rows). *Read*: Augustine; Cassiodorus; Bellarmine;
    Theodoret; Athanasius (PG 27). *No registered route*: Denis the Carthusian;
    Hugh of Saint-Cher (three single psalm chapters are held — 83, 94, 117 — not
    95); Nicholas of Lyra; Peter Lombard, *Commentarium in Psalmos* (the
    *Sententiae* only); Albert the Great; Jerome, *Commentarioli in Psalmos*;
    Euthymius Zigabenus; Walafrid Strabo, *Glossa ordinaria*.
  - **Ps 101:16** (twenty rows). *Read*: Augustine; Cassiodorus; Bellarmine;
    Theodoret; Athanasius (PG 27). *No registered route*: Nicholas of Lyra; Peter
    Lombard; Albert the Great; Bruno the Carthusian; Denis the Carthusian (two
    rows); Hugh of Saint-Cher; Jerome, *Commentarioli in Psalmos* and *Tractatus
    in Psalmos*; Prosper of Aquitaine, *Expositio Psalmorum C–CL*; Alcuin,
    *Expositio in psalmos poenitentiales* (the library holds only his
    *Interrogationes in Genesim*); Arnobius the Younger; Gregory the Great,
    *Expositio in septem psalmos paenitentiales* (the library holds his Gospel and
    Ezekiel homilies, the *Regula pastoralis*, and PL 78, which carries the
    Gregorian liturgical books and not this work); Euthymius; Richard Rolle.
  - **Ps 121:1 and Ps 121:7** (seventeen rows each, the same seventeen). *Read*:
    Augustine; Cassiodorus; Hilary; Chrysostom (PG 55); Bellarmine; Theodoret.
    *No registered route*: Nicholas of Lyra; Peter Lombard; Denis the Carthusian
    (two rows); Hugh of Saint-Cher; Albert the Great; Bruno the Carthusian;
    Euthymius; Jerome, *Commentarioli*; Prosper; Walafrid Strabo.
  - None of the unreached works is printed in a registered Migne volume. **Jerome's
    two psalm works** are the one case worth a sentence: the index's
    *Commentarioli* and *Tractatus* are not in PL 26, which the library registers
    for Jerome on Matthew; whether PL 26 prints any other psalm work under his name
    was not checked, and nothing here rests on one.
  - The psalms now have six direct witnesses on Ps 121, five on Ps 101 and five on
    Ps 95, in Latin and Greek, and they disagree materially about Ps 121 (§ 4.6);
    that is enough for § 3 and it is not a patristic consensus (§ 10.2).
- **Augustine, *Quaestiones in Heptateuchum***, **Cyril of Alexandria, *Glaphyra***,
  and the other Ex 24:4 leads listed in § 3.7. Not registered, not reached.
  Theodoret's *Quaestiones in Exodum*, which is registered, asks no question on
  Ex 24 (§ 3.7). The Offertory's cited verses now have one later witness at their
  own locus, Cornelius a Lapide, and no patristic one.
- **The later and Doctoral reception of the two large lections.** § 3.5 and § 3.6
  now carry, row by row, what the index returns for Mt 9:1 (nineteen rows) and
  1 Cor 1:4 (fourteen rows) and the registration state of each, found by work
  record and by collected and whole volume. **Read**: for the Gospel, Aquinas's
  lectura (and the *Catena aurea* through an unregistered delivery); for the
  Epistle, Theodoret, Aquinas and a Lapide. **Unreached, with no registered
  route**: for the Gospel, Hilary's *Commentarius*, Rabanus, Albert, Chromatius,
  Paschasius, Theophylact, Bruno of Segni, the *Glossa*, Lyra, Denis, Maldonado,
  Hugh, and a Lapide on the Gospels; for the Epistle, Origen, Theophylact, Peter
  Lombard, Rabanus, Hugh, Lyra, Denis and Estius. The corpora searched are the
  registered source library, its collected volumes and the repository's
  passage→work index, and nothing wider; no external delivery of any unregistered
  lead was tried.
- **The Ordines and the medieval liturgical commentators.** **Rupert of Deutz was
  opened on the second re-entry** and is in § 2.7 and § 3.11, with Guéranger. The
  earlier rationale for leaving him unopened — that nothing in § 3 or § 4 turned on
  him — was wrong: he expounds this Sunday's Mass, records a different Gospel for
  it, and bears on §§ 4.3 and 4.5 and on what `research/interpretations.md` may say
  no witness supports. Of the others: **Amalarius** is registered in the tracked
  PL 105 layer; a search of it for this Mass's chant and Gospel incipits (*Da
  pacem*, *Sanctificavit*, *Tollite hostias*, *paralytic-*) returns one hit, at
  physical line 17725, which is a pastoral rule on giving the sacraments to the
  dying on the faith of their friends, citing the paralytic in Luke's form (*Homo,
  dimittuntur tibi peccata*); it is not a comment on this Mass, its author inside
  the volume was not identified, and nothing is built on it. **PL 78**, registered
  with a tracked layer, carries Ménard's edition of the Gregorian sacramentary; the
  layer prints this formulary's three orations at physical lines 14353–14360 under
  a heading it renders `HEBDOMADA XXU POST PENTECOSTEN`, immediately before
  `HEBDOMADA XX` — apparently the Nineteenth, which would agree with the Hadrianum
  (§ 2.2) — with Ménard's variant *ut et tuam cognoscamus veritatem, et eam dignis
  mentibus ac moribus*. That was read in the layer only, the heading is damaged,
  no page image was opened, and nothing in § 2 rests on it; it is recorded as a
  lead. **Durandus and Honorius** have no registered route and were not reached.

### 5.3 The gallery and the proposal quota

The three-document contract that governs this run adopts the restored four-page
concise opening **without** reinstating the older schema-1 mandatory cultural
gallery or exploratory-proposal quota. No `Notable-and-quotable audit` and no
`Interpretive-proposal audit` is therefore recorded, and **no cultural afterlife
was verified to the standard those sections require.** Candidate phrases were
noticed in passing — *Surge, tolle lectum tuum* has an English idiomatic life, and
the Gradual's psalm has a famous anthem tradition — and none was checked at a
primary source. Nothing downstream may treat either as established, and a later
run that reinstates the gallery starts that work from zero.

---

## 6. Witness register

Every source this stage actually opened, with what was read and how its identity
was fixed. Registered bindings are in `research/source-bindings.toml`; the
records here that have no binding are cited in `References` in the ordinary way.

### 6.1 Liturgical text control

| Witness | Identity | What was read |
| --- | --- | --- |
| 1962 typica | `artifact.…vatican-typica-1962.cmaa-facsimile-pdf`, SHA-256 `648fdb8f…d3518a`, 82,815,941 bytes, fetched and matched 2026-09-22 | printed pp. 410–411 (PDF 491–492) at 200, 400 and native 500 ppi; the text layer of the same two pages for `propers/retrieved.txt` |
| 1962 orations passage | `passage.…vatican-typica-1962.temporal-pentecost-18-orations` | its four recorded loci, re-read on the page images |
| Benziger 1962 | `artifact.…benziger-iuxta-typicam-1962.ia-djvu-ocr`, SHA-256 `2a2da44d…4585ce`, matched | whole-file text layer at lines 61206–61352; page images of leaves n480 and n481 (its printed pp. 404–405), 800 × 1158 px, SHA-256 `0d4b2b05…d3cf` and `68609629…184f`, **unregistered, not retained** |
| 1862 Pustet, text | `artifact.…pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`, SHA-256 recomputed and matched | physical lines 51669–51811 |
| 1862 Pustet, images | Internet Archive `bub_gb_E7sPAAAAIAAJ` leaves n435, n436 = printed pp. 350, 351, 2500 × 4097 px each, SHA-256 `dd53758e…0bc13` and `5dfc6948…5804e`, **unregistered, not retained** | the whole formulary, column by column |
| Clementine Vulgate | `edition.catholic-church.vulgata-clementina.ebible-latvuc`, tracked chapter files | Ex 24; Pss 95, 101, 121, 140, 147; Ecclus 36; Mt 9; 1 Cor 1; and a literal search of all 73 books |
| Douay–Rheims (Challoner) | `edition.…challoner-gutenberg-1581`, tracked verse-text artifacts | Ex 24:1–8; Pss 95, 101:14–18, 121; Ecclus 36; Mt 9:1–13; 1 Cor 1:1–13 |
| Psalm-numbering concordance | `…challoner-gutenberg-1581/artifacts/psalm-numbering-ee3c7757/`, SHA-256 `53576188…5b721` | rows for Vulgate 95, 101, 121, 147 |
| Cummiskey 1861 | `passage.…philadelphia-1861.post-pentecosten-18` over `…temporal-orations-en` | the three oration rows, in the tracked payload only |

### 6.2 Transmission

| Witness | Identity | What was read |
| --- | --- | --- |
| Old Gelasian, text | `artifact.…sacramentarium-gelasianum-vetus.wilson-1894.ia-djvu-ocr-gelasiansacrame00wilsgoog`, SHA-256 `039123ca…684d84`, matched on fetch | lines 21548–21580 (Bk III xiii–xv); lines 15300–15360, carrying the Postcommunion of Bk I **§ xciii** at 15341–15344 — § xciii, not § xciv, on the contents entry at line 640 and Wilson's own marginal `I. xciii` at 21582, the twin `I. xciv` running heads at 15317 and 15381 being what misled (§ 2.1); lines 12585–12598, the Secret of Bk I **§ lix**, on which §§ 2.1, 3.9 and 10.6 rest; whole-file literal searches |
| Old Gelasian, images | Internet Archive `LiberSacramentorumRomanaeEcclesiae` leaves n324, n325 = printed pp. 232, 233, 3407 × ~5520 px, SHA-256 `4da337e0…a354` and `14291a2c…585c`, **unregistered, not retained** | p. 232 whole, both columns; p. 233 top, to fix the section boundary |
| Hadrianum | `artifact.…sacramentarium-gregorianum-hadrianum.wilson-1915.ia-pdf-96fd93c7`, tracked payload, SHA-256 `96fd93c7…8681` | printed pp. 174–175 (PDF 232–233) rendered at 300 dpi; whole-file text extract for location |
| Veronense | `artifact.…sacramentarium-veronense.feltoe-1896.ia-djvu-ocr-sacramentariumle00cath`, SHA-256 `7e7e82fe…cad21b`, matched on fetch | whole-file literal searches only |
| Sacramentary corpus boundary | `corpus.catholic-church.ancient-sacramentaries-2026-08-01` | its own declared limits, quoted in § 2.4 |
| gregorien.info, Gradual *Timebunt gentes* | `artifact.gregorien-info.gregorien-info-chant-database.web-2026-09-05.chant-8121-gradual-timebunt-gentes-72145226`, SHA-256 `72145226…10d6e0`, 20,959 bytes, re-fetched and matched 2026-09-22 | the whole rendered record: piece text, the AMS calendar block and the Hesbert citation line with its six numbers |
| gregorien.info, AMS day 819 | `artifact.…web-2026-09-05.calendar-ams-day-819-684af370`, SHA-256 `684af370…0224f7`, 7,190 bytes, re-fetched and matched 2026-09-22 | the whole day: *Dominica XVII post Pentecosten*, ten chant rows with sigla |

**Unregistered gregorien.info deliveries**, read live on 2026-09-22 at
`https://gregorien.info/calendar/id/2/<day>/en`, retained nowhere, digests given
so that a later run can register them. Day 823 is the one § 2.3 depends on.

| Day | Heading | Response SHA-256 |
| --- | --- | --- |
| 818 | Dedicatio S Michaelis | `e37cac12806a96b89bf61267e6bd59dba84dbe95c319b5684efef60c6b1644de` |
| 820 | Feria IV Quatuor Temporum Septembri | `a0db65a8867547d78dfa9b4112726fbbd827c1297d0fed30bf5ed6aa9d1374fc` |
| 821 | Feria VI Quatuor Temporum Septembri | `846fd1a26a71b392ed74edda24bd30568b9e665f64bbc23a094b595c1d085232` |
| 822 | Sabbato Quatuor Temporum septembris | `d64acbb7674658d2a90a0041583f1c8ca8f5699aa54c04b14addbb6f097ab0d7` |
| **823** | **Dominica XVIII post Pentecosten** | `43acf9bd8a7bd40d43827f1a0d5a65455e47f765aae71883eb10934060ac23d9` |
| 824 | Dominica XIX post Pentecosten | `380afd456ec4612fa8ebc77d1d10634560cc5a9a9112f255711e1751ddf483a9` |
| 825 | Dominica XX post Pentecosten | `825b777f5e5ed1bc7854b7a3d93f05620d86aae92f533561559b0ae783c7239d` |

### 6.3 Reception

**Registered, bound, and read at the locus this round.** These four were reached
through the source library, not through a public delivery, and each has a binding
in `research/source-bindings.toml`.

| Witness | Identity | What was read |
| --- | --- | --- |
| Jerome, *Comm. in Matth.* I, at Mt 9:1–8 | `segment.jerome.commentariorum-in-evangelium-matthaei.vallarsi-migne-pl26-1845.pl26-columns-15-218` over `artifact.jacques-paul-migne.patrologia-latina-volume-26.paris-1845.internet-archive-google-pdf-0d889bd6`, SHA-256 `0d889bd6…0245e4`, 63,426,233 bytes, fetched and matched 2026-09-22 | PL 26, cols. 53–56 = artifact PDF pp. 32–33, rendered at 200 dpi; PDF pp. 13–14 read first to fix the column-to-page rule (p. 13 = cols. 15–16), which the segment's own bounds then confirm. **The scan has no text layer**: `pdftotext` over pp. 13–116 returns 104 bytes, so every reading is off the image |
| Hilary, *Tractatus super Psalmos*, in Ps. CXXI | `artifact.hilary-of-poitiers.tractatus-super-psalmos.csel-22-zingerle-1891.ia-djvu-ocr-shilariiepiscopi22hilauoft`, SHA-256 `6b39d974…14a7fa`, 2,729,218 bytes, fetched and matched 2026-09-22; registered `indexable = false` | physical lines 29495–30011, the whole tractatus; the running heads inside that span print CSEL 22 pp. 570, 571, 574, 575, 578 and 580, so it runs from p. 570 into p. 580 |
| Cassiodorus, *Expositio psalmorum*, in Ps. CI | `artifact.cassiodorus.expositio-psalmorum.latin-corpus-corporum-monumenta-web-2026-09-05.monumenta-ps101-apparatus-latin-text`, **tracked in this checkout**, SHA-256 `bed53e26…c45ff` | the whole exposition, 38 sectiones; sectiones 21–23 for the Alleluia verse and its frame |
| Cassiodorus, in Ps. XCV and in Ps. CXXI | `artifact.…latin-corpus-corporum-monumenta-web-2026-09-22.monumenta-ps95-apparatus-latin-text` (SHA-256 `06e1919c…94b0a`) and `…monumenta-ps121-apparatus-latin-text` (SHA-256 `38f93abc…4bb92`), both **registered and retained by this stage** from the exact deliveries `21640d6c…3df8a` and `f95cb469…193eca` | both expositions whole, 21 and 16 sectiones; Ps 95 sectiones 1–2, 13, 14 and Ps 121 sectiones 2, 6, 12 |

The derivation that produced the two new Latin files was **checked before it was
used**: run over the re-fetched Ps 101 delivery (which itself returned the
registered digest `ac7c0acd…618855`), it reproduced the already-tracked Ps 101
Latin byte for byte. That is why the Ps 95 and Ps 121 files can be trusted to
stand in the same relation to their sources as the tracked one does to its.

**Two defects in the library, found while binding and reported rather than
fixed.** `work.cassiodorus.expositio-psalmorum` declares `locus_pattern =
'(?:16|24|64|88)\.…'` — four psalm numbers — while the library registers
artifacts of that work for Psalms 39, 70, 85, 95, 97, 101 and 121. A locus for any
of those is rejected by `source-library validate`, which is why the three
Cassiodorus bindings here carry no `loci` array and name their sectiones in
`context` instead. Widening the pattern would move the work record's fingerprint
and with it every Cassiodorus binding in every leaf, which is a repository-wide
review obligation and not this leaf's to trigger.

The same defect stands in a second work record, found on the sweep below:
`work.cornelius-a-lapide.commentaria-in-omnes-divi-pauli-epistolas` declares
`locus_pattern = '(?:prooemium|epistola-ad-galatas-argumentum)'` — two named loci
an earlier leaf happened to need — while the library tracks the optical layer of
the whole Pauline commentary. A scriptural locus in that work is rejected, so the
a Lapide binding here also carries no `loci` array and names its physical lines in
`context`. Reported on the same footing and for the same reason.

**Registered routes found by the second sweep of the library, and what each
gave.** The first pass of this stage swept the library only for the witnesses it
had recorded as unreached, and then printed the eight deliveries below under a
heading saying the library registered none of them. It registers five of them,
or an equivalent route to the same text, and § 5.2 says why that gap in the
sweep matters. Each row below was opened this round; each is bound in
`research/source-bindings.toml`.

| Witness | Registered route | What it gave |
| --- | --- | --- |
| Augustine, *Enarr. in Ps.* 95, 101 and 121 | `artifact.augustine.enarrationes-in-psalmos.english-npnf8-ccel-web-2026-09-05.ccel-npnf108-text-d6841950`, **tracked in this checkout**, SHA-256 `d6841950…0020e9`, 5,029,159 bytes, 81,685 lines | The complete CCEL NPNF1-8 English, needing no network, covering all three expositions. Psalm XCVI § 9 at line 48059 and § 10 at 48078, § 11 opening at 48086; Psalm CII § 16 at 50512 and § 17 at 50522; Psalm CXXII, opening at 60234, §§ 2 and 3 at 60246 and 60259 and §§ 12 and 13 at 60439 and 60456. **Every sentence §§ 3.2, 3.3, 3.4 and 3.8 quote stands here at the same section.** Two differences of delivery, not of sense: this 1888 text keeps its own century's second person (*if ye will enter*, *thou hast entered*), and the NPNF editors' abridgments print as four-dot ellipses inside the exposition |
| Augustine, *Enarr. in Ps.* 101, the delivery quoted | `artifact.augustine.enarrationes-in-psalmos.english-npnf-new-advent-web-2026-09-05.newadvent-1801102-adb31091`, SHA-256 `adb31091…4e57a` | **The registered record's `source_url` and digest are exactly the URL and digest this record's own table gave for it as an unregistered delivery.** It is registered `storage = "remote"`, `rights_status = "unresolved"`, bytes not retained, because the host states a revision of its own inside the text. It is now bound; § 3.4's quotations are from it, and the tracked CCEL and Latin routes above and below are the offline reader's way to the same sections |
| Augustine's own Latin, Pss 95 and 101 | `…latin-migne-corpus-corporum-wikisource-web-2026-09-05.wikisource-part-10-latin-text` and `…-part-11-latin-text`, both **tracked in this checkout** | *IN PSALMUM XCV* § 9 and § 10, and *IN PSALMUM CI* § 16 and § 17, at the exact loci §§ 3.4 and 3.8 had cited in NPNF English only. **Augustine's lemma at Ps 95:9 is *in atrio sancto ejus***, which is the second witness § 5.1.7 needed. Ps 121 has **no** tracked Latin here: the registered parts of this edition run 31–40, 61–66, 80–89, 90–100 and 101–110 |
| Chrysostom, *Hom. in Matth.* 29 | `segment.john-chrysostom.homiliae-in-matthaeum.ccel-web-2026-09-17.complete-homilies` over the **tracked** `artifact.nicene-and-post-nicene-fathers.series-1-volume-10.ccel-web-2026-09-17.ccel-text-adb8f1c9` | The segment bounds all ninety homilies at lines 614–49168; Homily XXIX stands at 18438–18793, headed *Matt. IX. 1, 2*, Homily XXX opening at 18794. Every sentence §§ 3.5, 4.1, 4.2 and 4.3 quote stands there, with one difference of delivery: *He said not, I forgive **thee thy** sins, but, **thy** sins be forgiven **thee*** against the New Advent page's *you your … your … you* |
| Augustine, *De cons. evang.* II. xxv | `segment.augustine.de-consensu-evangelistarum.ccel-web-2026-09-17.complete-work` over the **tracked** `artifact.nicene-and-post-nicene-fathers.series-1-volume-6.ccel-web-2026-09-17.ccel-text-ce371798` | The segment bounds the whole treatise at lines 6929–22951; the *Chapter XXV* heading stands at 12672, § 57 at 12679–12698, § 58 at 12700–12791 and § 59, which leaves the pericope, at 12793. Both sentences § 3.5 and § 4.1 quote stand there word for word, the translator's brackets in *[thus said to be]* included; *a kind of metropolis* at 12747 and *would be more difficult to solve if Matthew mentioned Nazareth by name* at 12729 |
| Cassiodorus, in Pss XCV, CI and CXXI, **as Migne printed him** | `artifact.jacques-paul-migne.patrologia-latina-volume-70.paris-1865.ia-djvu-ocr-patrologiaecurs27goog`, SHA-256 `d777c4c6…63a2e`, 5,244,841 bytes, fetched and matched 2026-09-22, `storage = "remote"` so nothing retained | **This is the row that changes what this record may say about Migne.** Read at five places, each given here in normalised orthography because the layer is damaged, and each with the physical line at which a reader may check the damage: *Vers. 9. Adorate Dominum in atrio sancto ejus* (52417, printed `Adorate Dominum in atrto $ancl0`, between the column markers 679 and 682); *Vers. 8. Afferte Domino gloriam nomini ejus; tollite hostias, et introite in atria ejus* (52502, re-read on the layer re-fetched and matched on 2026-09-22; an earlier draft gave 52499, which reads `dati $unt? et non e$t inventu$ qni daret honorem Deo^`) with *Atria enim Domini sunt apostoli vel prophetae* (52413); *Vers. 16. Et timebunt gentes nomen tuum, Domine* (55123); *Laetatus sum in his … in domum Domini ibimus. Decora nimis et salutaris causa laetitiae* (69957–69959); *Vers. 7. Fiat pax in virtute tua, et abundantia in turribus tuis* … *Virtus quippe ipsius pax sine dubitatione sanctorum est, quae vocatur et charitas* (70260–70262, 70284–70287). **At all five the Corpus Corporum transcription agrees with Migne**, which is what the record needed. The layer is uncorrected optical recognition and does not print the printed reading order — the Ps 95 v. 9 lemma stands *before* the v. 8 lemma — so it confirms and locates, and no letterform claim is made from it |
| Cornelius a Lapide on 1 Cor 1:4–8 | `artifact.cornelius-a-lapide.commentaria-in-omnes-divi-pauli-epistolas.antwerp-1614.ia-djvu-text-197365b2`, **tracked**, 3,103,885 bytes | The verse-by-verse exposition at lines 40030–40130 (the layer prints each page twice; the same exposition stands again at 40466–40560). It gives § 3.6 the later reception that row had none of, and one real difference from Chrysostom at v. 8 |

**Registered routes opened on the second re-entry, by artifact coverage.** Every
one was registered before this run; every one had been recorded by an earlier pass
of this stage as unreached, or not named at all. Each is bound in
`research/source-bindings.toml`.

| Witness | Registered route | What was read, and how |
| --- | --- | --- |
| Chrysostom, *Expositio in Ps. CXXI* | `artifact.john-chrysostom.expositio-in-psalmos.migne-pg-55-paris.ia-djvu-ocr-d9b83186`, 9,609,040 bytes, SHA-256 `d9b83186…3781b4`, fetched and matched 2026-09-22, `storage = "remote"` | Physical lines 45635–46230 (heading at 45635, v. 7 at 45881–45890, Ps 122 at 46231). Columns and every Greek word quoted re-read on the page images, leaves n339 (cols. 347–348), n340 (cols. 349–350) and n343 (col. 351) |
| Theodoret, *Interpretatio in Psalmos* and *Quaestiones in Exodum* | `artifact.theodoret-of-cyrus.interpretatio-in-psalmos.migne-pg80-paris-1860.wikimedia-pdf-72ee8714`, 129,500,554 bytes, SHA-256 `72ee8714…bcdd8`, fetched and matched 2026-09-22, `remote` | PDF pp. 872 (cols. 1647–1648, Ps 95:7–9), 890 (cols. 1679–1680, Ps 101:14–16), 996–997 (cols. 1879–1882, Ps 121), 147–148 (cols. 277–280, *interr.* 59–60 on Exodus), rendered at 200 dpi; the PDF's text layer located the pages and was never quoted |
| Theodoret, *Interpretatio in I Cor.* | `artifact.theodoret-of-cyrus.interpretatio-epistolae-ad-galatas.1864-migne-pg82-paris.ia-djvu-ocr-db2067fd`, 8,475,812 bytes, SHA-256 `db2067fd…8f2ad`, fetched and matched 2026-09-22, `remote` | Physical lines 16372 (heading of the 1 Corinthians commentary), 16583–16789 (vv. 4–9); columns 229–232 read on the page images, leaves n131–n132 |
| *Expositiones in Psalmos* under Athanasius's name | `artifact.athanasius-of-alexandria.expositiones-in-psalmos.migne-pg-27-paris.ia-djvu-ocr-969a381f`, 6,205,972 bytes, SHA-256 `969a381f…f4269`, fetched and matched 2026-09-22, `remote` | The layer's recognition of these columns is too poor to search; located by arithmetic from the registered leaf n213 (cols. 413–414) and read on the page images, leaves n214 (cols. 415–416, Ps 95) and n221 (cols. 429–430, Ps 101:16–17) |
| Bellarmine, *Explanatio in Psalmos* | `artifact.robert-bellarmine.commentary-on-the-book-of-psalms.2026-09-05-osullivan-ecatholic2000.historical-text-357551e1`, **tracked**, SHA-256 `357551e1…51bc2` recomputed and matched | Pss 95 (lines 3413–3439), 101 (3565–3622) and 121 (4535–4556), whole. O'Sullivan's 1866 English, which its translator abridged |
| Augustine, *Enarr. in Ps.*, Migne's print | `artifact.jacques-paul-migne.patrologia-latina-volume-37.paris-1845.internet-archive-google-pdf-afe6878f`, 48,479,761 bytes, SHA-256 `afe6878f…97bb4`, fetched and matched 2026-09-22, `remote` | No text layer. PDF pp. 110 (cols. 1233–1234, Ps 95 §§ 9–10), 145 (cols. 1303–1304, Ps 101 sermo I §§ 16–17), 302–303 (cols. 1617–1620, Ps 121 heading and § 2), 307 (cols. 1627–1628, Ps 121 § 12), found by the column arithmetic the registered records fix and read at 250 dpi. **It is the only registered route to Augustine's Latin on Ps 121**, and it corrects the English twice (§ 3.2 lemma, § 3.3 towers) |
| Augustine, *Enarr. in Ps.* 101 sermo I, augustinus.it | `artifact.augustine.enarrationes-in-psalmos.latin-augustinus-it-web-2026-09-05.augustinus-it-ps101-i-9c30d781`, re-fetched 2026-09-22 and matched (`9c30d781…cd05d`), `remote`, rights unresolved | §§ 16–17 in locally parsed text; agrees with PL 37 and the tracked Latin; quoted nowhere |
| Aquinas, *Super Matthaeum* | `artifact.thomas-aquinas.opera-editio-altera-veneta-tomus-3.venice-bettinelli-1745.ia-djvu-ocr-10aa155e`, **tracked**, SHA-256 `10aa155e…63efee` matched; and its facsimile `…internet-archive-google-pdf-adb333e0`, 56,148,876 bytes, SHA-256 `adb333e0…785de8`, fetched and matched 2026-09-22, `remote` | Layer lines 16227–16540 to locate; printed pp. 120–122 = PDF pp. 138–140 read at native 600 ppi for every word quoted |
| Aquinas, *Super I ad Corinthios* | `artifact.thomas-aquinas.super-i-ad-corinthios.latin-corpusthomisticum-web-2026-07-26.c1c-html-8be5b71c`, re-fetched 2026-09-22 and matched (`8be5b71c…a8c7c`), `restricted` | Cap. 1 lect. 1 on vv. 4–8 in locally parsed text; quoted only in short phrases |
| Cornelius a Lapide, *Commentaria in Pentateuchum* | `artifact.cornelius-a-lapide.commentaria-in-pentateuchum.antwerp-1700.ia-djvu-ocr-d1f91f40`, 7,195,178 bytes, SHA-256 `d1f91f40…dac470`, fetched and matched 2026-09-22, `remote` | Lines 79014–79245, Ex 24:4–8. **Layer only; no page image opened**, so § 3.7 normalises and says so, and transcribes nothing the layer garbles |
| Rupert of Deutz, *De divinis officiis* XII.18–19 | `artifact.rupert-of-deutz.de-divinis-officiis.latin-migne-pl-170.ia-djvu-ocr-2e2ca850`, **tracked**, SHA-256 `2e2ca850…ed376` matched | Lines 23431–23519 to locate; every word quoted read on the page images, leaves n168 (cols. 325–326) and n169 (cols. 327–328), as the artifact's own note requires |
| Guéranger, *The Liturgical Year* XI | `artifact.prosper-gueranger.the-liturgical-year.english-duffy-1900-volume-11.ia-pdf-95ba98e2`, **tracked**, SHA-256 `95ba98e2…92690` matched | The chapter on this Sunday, printed pp. 393–409 = PDF pp. 414–430, in the text layer; every sentence quoted checked on the rendered pages (PDF pp. 414, 415, 422, 423, 424, 426, 427) |

**Unregistered page images read on the second re-entry**, fetched on 2026-09-22
from `https://archive.org/download/<item>/page/n<leaf>.jpg`, retained nowhere,
digests given so that a later run can register them.

| Item, leaf | What it carries | Size | SHA-256 |
| --- | --- | --- | --- |
| `patrologiae_cursus_completus_gr_vol_055`, n339 | PG 55 cols. 347–348, Greek, Ps 121 heading and vv. 1–4 | 2010 × 3135 | `90bafddf142001b157e8aba8c0649fdd8280531375502733deaab44ae51b692e` |
| same, n340 | PG 55 cols. 349–350, Greek, vv. 4–9 | 2010 × 3135 | `340ce98710ec280ca597917f643ada633202f7ed551d98bb20da24f5629ae646` |
| same, n343 | PG 55 col. 351, end of the exposition | 2044 × 3138 | `2f6e5a67df125496c8ed732faea6189c2dd71f1a24c9dddef9199320bbda2e7c` |
| `patrologiae_cursus_completus_gr_vol_082`, n131 | PG 82 cols. 229–230, 1 Cor 1:1–6 | 1984 × 3229 | `62b972cfc7c000f203e57a23a6e6c282b45783c7441022c6b5d6c3a3549d5139` |
| same, n132 | PG 82 cols. 231–232, 1 Cor 1:6–9 | 1962 × 3210 | `cd16fc3ba6ba8606aedd4f2306ca95cff16508da3be58c103f4e0cd718019340` |
| `patrologiae_cursus_completus_gr_vol_027`, n214 | PG 27 cols. 415–416, Ps 95 | 4174 × 6451 | `1eacb3f9d67a96bf54a5bdbc109427b092311f5000fd7ef5f59d9063dc947492` |
| same, n221 | PG 27 cols. 429–430, Ps 101:16–18 | 4174 × 6451 | `e7eb2007fd551c645505dc82f49873a0b669ad584bba0c1613d82d34c78e513b` |
| `patrologiaecursu0170mign`, n168 | PL 170 cols. 325–326, *De div. off.* XII.18 | 2253 × 3584 | `0c20d000ed8796aafd43c6ce691bea17ff8bacae04428378f4c92ab55dc1b45d` |
| same, n169 | PL 170 cols. 327–328, XII.19 | 2253 × 3584 | `9089571fd01c08d43d349eb9c9022bae30a1858a832eb9038decb6a87fbb91e9` |
| `shilariiepiscopi22hilauoft`, n599 | CSEL 22 p. 570, Hilary in Ps. CXXI § 1 | 2216 × 3736 | `b79995ce0ece9cb92f5da6127f2276b7f90c5d851f287b7b402424647118be31` |
| same, n600 | p. 571, §§ 1–3 | 2216 × 3736 | `bdb6cec06a268caf84b59daf4a4dcb7b8cadbd60e06ab887508ccf36ec63971c` |
| same, n601 | p. 572, §§ 3–4 | 2216 × 3736 | `2ef5450fa5655d9607c75df48913cc69764ccab2ca61dfcd9845d29a946241a7` |
| same, n602 | p. 573, §§ 4–6 | 2216 × 3736 | `b7915a7a1bf3564ab2b54478ccf34d5740dd7b48a20d5787c5e534973040579d` |
| same, n607 | p. 578, §§ 13–14 | 2216 × 3736 | `94d7edda601da9587dde3477c103804bca9cca0a10b0232fbcdd77fb489b5c19` |
| same, n608 | p. 579, §§ 14–15 | 2216 × 3736 | `763890005df1fc5dfa3a9013926e9682b114ebec9168394007909aa55f2569c5` |

**Registered routes that exist and were deliberately not used, with the reason.**

| Route | Why not |
| --- | --- |
| `artifact.cassiodorus.expositio-psalmorum.latin-adriaen-ccsl98-turnhout-1958.azbyka-google-scan-pdf-c72410b0` — Adriaen's CCSL 98, Pss 71–150, 18,569,885 bytes, 721 pages | Registered `storage = "restricted"`, `rights_status = "restricted"`: its record says in terms that public delivery of the scan establishes access for bounded verification and not permission, and retains no bytes. It is a route to take when a claim needs the critical text, and **this record makes no claim about Adriaen** — the only Cassiodorus question it had open was what *Migne* printed, which PL 70 now answers. A later run that wants the critical lemma at Ps 95:9 should open exactly this artifact |
| `artifact.nicene-and-post-nicene-fathers.series-1-volume-12.new-york-1889.ia-facsimile-pdf-40c052fb` — NPNF1-12, 40,960,735 bytes | The registered route to Chrysostom on 1 Corinthians is a **facsimile page-image PDF with no registered text layer**, held `storage = "remote"` and not retained, of the same 1888 translation the delivery read at § 3.6 carries. Opening it would confirm the printing, not the locus, and nothing § 3.6 states turns on a letterform; the witness stands at `inspected` either way. A later run wanting `verified` for Chrysostom on 1 Cor starts here |
| `artifact.nicene-and-post-nicene-fathers.series-1-volume-14.new-york-1889.ia-facsimile-pdf-a09a5d18` — NPNF1-14, 55,590,001 bytes, 580 PDF pages | The same, for Chrysostom's *Hom. in Heb.* 16 at § 3.7. The registered work record describes this volume by its homilies on John and says nothing about its Hebrews content, so which printed pages carry Homily 16 is **not established from the library** and was not established by opening the file |
| `artifact.augustine.enarrationes-in-psalmos.latin-augustinus-it-web-2026-09-05.augustinus-it-ps101-ii-71f61f8e` — augustinus.it, Ps 101 sermo II | Re-fetched and matched (`71f61f8e…875fd`), and **not bound, because it does not carry the Alleluia verse**: sermo II begins at v. 20. Its record's note says the reverse — that sermo II covers vv. 13–29 and sermo I does not reach v. 16 — which the two Latin deliveries and PL 37 all contradict. Reported to the record's owner; not edited here |
| `artifact.robert-bellarmine.commentary-on-the-book-of-psalms.osullivan-duffy-1866.commons-ia-facsimile-78b290d4` — the 1866 English facsimile, 56,448,883 bytes | The record of the transcription read above says the facsimile controls quotation. It was not opened: the Bellarmine quotations in § 3 are short, are given as the transcription prints them, and carry the one transcription error found (*walk* for *walls*) marked as such; no claim turns on a letterform. A later run quoting Bellarmine for publication should collate against this facsimile, or better against the Latin, which the library does not register |
| `artifact.john-chrysostom.homiliae-in-matthaeum.migne-pg-57-paris.ia-djvu-ocr-1b95176e` — Chrysostom's Greek *Hom. in Matth.*, **tracked** | Chrysostom on the Gospel is read in the registered CCEL English at his own locus (below), and every claim §§ 3.5 and 4.1–4.3 make from him is a claim about his argument, not his Greek wording. The Greek would confirm the translation, not the locus. A study that quotes a Greek word of Homily 29 should open it |
| `artifact.theodoret-of-cyrus.interpretatio-epistolae-ad-galatas.1864-migne-pg82-paris.wikimedia-pdf-7d6dd76e` — PG 82 facsimile, 112,586,234 bytes | The same columns were read on the Internet Archive page images of the same printing (above); a second facsimile of them would add nothing |
| `artifact.jacques-paul-migne.patrologia-latina-volume-78.latin-migne-pl-78.ia-djvu-ocr-301707e7` — PL 78, Ménard's Gregorian sacramentary, **tracked layer** | Read in the layer only, as a lead (§ 5.2); no page image was fetched, because § 2 rests on Wilson's Hadrianum and the gregorien.info report of the Sextuplex and this later printed edition would add a third placement without changing either |

**Read on public deliveries, with the registration state of each now stated.**
Each is cited in `References` in the ordinary way. **Every response digest below
was recomputed on 2026-09-22 by re-fetching the page, and all eight matched**, so
the loci are reproducible. The last column says what the library holds for that
text, which is the column the first pass of this stage did not have.

| Witness | Delivery | Response SHA-256 | Extent read | Registration state |
| --- | --- | --- | --- | --- |
| Chrysostom, *Hom. in Matth.* 29 (NPNF1-10) | `https://www.newadvent.org/fathers/200129.htm` | `829801882887301353ea51022e3a3c58ca12274616f0c68521ba5a8873d7b99d` | whole homily | This delivery is unregistered; **the text is registered** and tracked, through the CCEL segment above, which was read and agrees |
| Chrysostom, *Hom. in 1 Cor.* 2 (NPNF1-12) | `https://www.newadvent.org/fathers/220102.htm` | `66bffe297c6a95cbc8e224e1faa835fcbc0a221ca676c8d2b49d3ee4577b5858` | §§ 1–7, on vv. 4–8 | Unregistered; the library's route to this text is the NPNF1-12 facsimile above, deliberately not used |
| Chrysostom, *Hom. in Heb.* 16 (NPNF1-14) | `https://www.newadvent.org/fathers/240216.htm` | `89e7ae8b625f5ac454ccbfbf01073427ee1a81f9cb0d67f0b8ded7e3534362b5` | §§ 3–5, on Heb 9:18–22 | Unregistered; the library's route is the NPNF1-14 facsimile above, deliberately not used |
| Augustine, *Enarr. in Ps.* 95 (NPNF1-8) | `https://www.newadvent.org/fathers/1801096.htm` | `ade5c0bebf1daf4126aeedd6343b191d88eb264bb5f834addc8bb08b7a9d7fb5` | §§ 2, 5, 8–11 | This page is unregistered; **the text is registered three times over** — the tracked CCEL NPNF1-8 English, the tracked Corpus Corporum Latin, and Migne's PL 37 facsimile — and all three were read |
| Augustine, *Enarr. in Ps.* 101 (NPNF1-8) | `https://www.newadvent.org/fathers/1801102.htm` | `adb31091e2f92062d89831f7b914aef93045e7dbb0f800a63a91e6b2f444e57a` | §§ 15–19 | **This exact page is a registered artifact** and is now bound; the same text is also tracked in the CCEL English and in Migne's Latin |
| Augustine, *Enarr. in Ps.* 121 (NPNF1-8) | `https://www.newadvent.org/fathers/1801122.htm` | `b2f96cc93e40f2b151cb4548254b4d482b2f38b0c6bb1a5b29df222581719f31` | §§ 2, 12, 13 | This page is unregistered; **the English is registered** and tracked in the CCEL NPNF1-8, which was read. No Latin of Ps 121 is *tracked*, but Migne's Latin is **registered** in the PL 37 facsimile and was read on its page images on the second re-entry (above) |
| Augustine, *De cons. evang.* II. xxiii–xxvi (NPNF1-6) | `https://www.newadvent.org/fathers/1602223.htm` … `1602226.htm` | chapter 25's page: `519be078c5b269538fabd580a8a1cf2faa229cf37da80afcbf5af85ab2c6193a` | chapter 25 in full; 23, 24 and 26 read for the boundary | These pages are unregistered; **the text is registered** and tracked, through the CCEL segment above, which was read and agrees |
| Aquinas, *Catena in Matthaeum* capp. 5–9 | `https://www.corpusthomisticum.org/cmt05.html` | `55b3379759bb33c2b9b918b8fc13d6a6a29e1aacd782ad0e457e306f0fd4ac32` | cap. 9 lect. 1 | **Genuinely unregistered, and the only one of the eight that is.** The library holds `work.thomas-aquinas.catena-aurea-in-lucam` and no state of the *Catena in Matthaeum* at all. This is the delivery §§ 3.5, 4.4 and 10.1 attribute Hilary and Rabanus through, and the reason those attributions are labelled *through the Catena* |

**Every reception witness stands at `inspected`, not `verified`.** Each was read
at the locus stated, in the language stated; none was collated against a critical
edition. The New Advent pages carry the NPNF English, which for Augustine on the
Psalms is an abridging translation with its own ellipses — one of which, at Ps 121
§ 12, hides Augustine's reading of the towers (§ 3.3) — and which those pages
additionally modernise: the second person of the 1888 printing is *ye* and *thou*
where they print *you*, as the CCEL rows above show for Augustine on Pss 95 and
121 and for Chrysostom on Matthew. Where this record quotes them it quotes the
delivery it read, and the tracked text's wording is recorded beside it rather than
harmonised away. The Latin and Greek witnesses carry their own limits and each is
stated where it is used: the PL 26 and PL 37 scans are page images with no text
layer and were read by eye; **the CSEL 22 layer is damaged in the body text of
this tractatus as well as in the apparatus**, so every Hilary quotation was taken
from the page images (§ 3.2), not the layer; the PL 70 layer misreads the very
lemma it confirms, so it locates and confirms and is never quoted as a letterform;
the PG 27, PG 55, PG 80, PG 82, PL 170 and Venice 1745 quotations were read on page
images, the layers serving only to locate; the a Lapide layers (Pauline and
Pentateuch) were read as layers only and their Latin is normalised; and the Corpus
Corporum Cassiodorus files are a transcription of a transcription of Migne —
**which PL 70 has shown to be faithful at every lemma this study uses**, so the
earlier bound, that they could settle nothing about what Migne printed, is
withdrawn as to Migne and kept as to Adriaen, whose critical text nobody here has
opened.

**What was checked, quotation by quotation, and what was not.** Every quotation
added on the second re-entry was taken from the page image or file its row names.
Of the quotations carried from earlier passes, those the second review named were
re-read against their cited pages and corrected; the rest stand on the first
re-entry's check and were not re-read a third time. The corrections: Hilary's *quia eadem et
Sion est*, *quae aedificatur* and *quia Hierusalem aedificatur*, from the page
images (the layer-based reconstructions were wrong); Chrysostom's "But that it
belongs to God only to know men's secrets …" (§ 3.5), where an earlier draft
printed "for it belongs …" as if it were the homily's; and "those [ordinances]"
(§ 3.7), where an earlier draft dropped the translator's brackets. Omissions inside
a quotation carry an ellipsis; `[thus said to be]`, `[or utterance,]` and
`[ordinances]` are the NPNF translator's brackets and are kept; *color* and
*labors* stand as NPNF prints them; emphasis is never added inside a quotation.
**Three classes of quotation are not transcriptions of a page, and each is
declared where it occurs**: the Latin from the two a Lapide optical layers (§ 3.6,
§ 3.7), given in normalised orthography; the Bellarmine English, quoted from a
web transcription whose facsimile was not opened (§ 3.2–3.4, 3.8); and the
Latin from Migne's editions and CSEL, where the ligatures *æ* and *œ* are written
out and *&* is written *et*.

### 6.4 Chronology

| Witness | Identity | What was read |
| --- | --- | --- |
| Catholic Encyclopedia, *Ecclesiasticus* | `artifact.catholic-encyclopedia.volume-5.…05263a-c3fe190d-article-text`, tracked | the authorship and date sections, for "between 190 and 170 B.C." and the alternate "about 280 B.C." |
| CE, *Epistles to the Corinthians* | `…volume-4.…04364a-2b6b401d-article-text`, tracked | "sent it by Titus about Easter A.D. 57" |
| CE, *St. Paul* | `…volume-11.…11567b-bff0dda8-article-text`, tracked | Prat's chronological table, "(1 and 2 Corinthians; Galatians), 56" |
| CE, *Gospel of St. Matthew* | `…volume-10.…10057a-e7b6ccef-article-text`, tracked | all five of its date positions: 38–45, 40–42, 40–45, 60–68, 64–67 |
| CE, *The New Testament* | `…volume-14.…14530a-0a19aa2c-article-text`, tracked | "about the year 50" |
| CE, *Temple of Jerusalem* | `…volume-14.…14499a-82b12b6e-article-text`, tracked | "Zorobabel raised it again from its ruins (537 B.C.)" |
| CE, *General Chronology* | `…volume-3.…03738a-5eb03e5b-article-text`, tracked | "the year of Rome 750 which he styles 3 B.C." |
| CE, *Biblical Chronology* | `…volume-3.…03731a-f5f96f04-article-text`, tracked | "we should be taken to 6 or 7 B.C. as the year of the Nativity" |
| NABRE, Psalms introduction | `passage.…english-usccb-web-2026-07-28.psalms-introduction`; payload not retained, so the live page was read 2026-09-22, response SHA-256 `fd3b94eed66c235f7ecb9c0d667d2cb804c4b5ff2382d88cbfc0b41f53532f86` | "there is no sure way of dating any Psalm … but not as late as the Maccabean period (ca. 165)"; also its own note that the Greek Psalter's numbering is usually one behind the Hebrew |

### 6.5 Greek

| Witness | Identity | What was read |
| --- | --- | --- |
| CATSS morphological Septuagint | `artifact.catss.lxxm-morphology.unicode-fddec9b.github-archive-fddec9b-74c72484`, SHA-256 `74c72484…4d8891`, matched on fetch; registered `storage = "restricted"`, so **retained only in the run's scratch and not installed** | `02.Exod.txt` at Ex 24:4, 5, 6, 17; `34.Sirach.txt` at Sir 36:12–22 |

---

## 7. Scriptural chronology audit

### 7.1 Generation

`research/chronology.toml` and `research/chronology-annotations.tex` were written
by `tools/tpt proper-chronology record --write` and `… annotations --write`, under
the default profile `catholic-comprehensive-v1`, for document
`liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost`, provider
`claude`. **Neither file is hand-edited, and no biblical date in any output may
come from anywhere else.** No non-default profile comparison is declared, so there
is no `research/chronology-profile-comparisons.toml`.

`tools/tpt proper-chronology loci` resolves every appointed locus: Introit,
Epistle, Gradual, Alleluia and Gospel return `composition-only`; Offertory
(Ex 24:4–5) and Communion (Ps 95:8–9) return `dated`; Collect, Secret and
Postcommunion cite no Scripture. The distinct directly appointed passages are
**Ex 24:4–5, Ps 95:8–9, Ps 101:16, Ps 121:1, Ps 121:7, Ecclus 36:18, Mt 9:1–8 and
1 Cor 1:4–8**; Ps 121:1 is appointed twice, by the Introit verse and by the Gradual
respond, and is inventoried once.

### 7.2 What the record asserts, element by element

| Element | Publication status | What the one displayable cell says |
| --- | --- | --- |
| `introit` | `nonuniform` | **No date may be printed.** Its two loci have chronology, but no one assertion covers both, so an element-wide cell would be a locus-specific claim wearing an element's name. |
| `epistle` | `composition-only` | Composition, disputed: A.D. 56; A.D. 57 |
| `gradual` | `composition-only` | Composition: before c. 165 B.C. |
| `alleluia` | `composition-only` | Composition: before c. 165 B.C. |
| `gospel` | `composition-only` | Event: **no narrated-event date in the corpus**; Composition, disputed: c. A.D. 38–45; c. A.D. 40–42; A.D. 40–45; c. A.D. 60–68; c. A.D. 64–67; c. A.D. 50 |
| `offertory` | `dated` | Event: "rising in the morning" (a relative, not a calendar, date) |
| `communion` | `dated` | Superscription setting: B.C. 537; Composition: before c. 165 B.C.; Prophetic referent, disputed: B.C. 3; c. B.C. 7 |
| `collect`, `secret`, `postcommunion` | *(empty)* | cite no Scripture |

The status column is `research/chronology.toml`'s own `publication_status` field,
transcribed. Only the Offertory and the Communion carry `dated`; the four elements
whose Scripture has a composition answer but no narrated-event date carry
`composition-only`, which is exactly what § 7.1 and § 7.4.2 say in words.

### 7.3 Inspection of the controlling chronology source owners

Every source the record cites was opened at the locus that produces its claim, in
this stage. The eight Catholic Encyclopedia articles are held as tracked
`-article-text` payloads and were read there; the NABRE Psalms introduction has no
retained payload and was read live. § 6.4 gives the loci. Nothing in the record
was accepted on the corpus's word alone.

Two things the inspection settles, and a study must not soften:

- **The Gospel's six composition labels are not six opinions of six scholars.**
  Five of them come from one article, which presents them as the range of
  positions — Theophylact and Euthymius (8 years after the Ascension), a tradition
  of the Apostles' separation (40–42), "Catholic critics, in general" (40–45),
  Eusebius's later departure (60–68), and Irenaeus (64–67) — and itself says of
  Irenaeus that "this text presents difficulties of interpretation which render
  its meaning uncertain." The sixth, "about the year 50," is a different article's
  own judgment.
- **The Communion's two Nativity dates are not a dating of the psalm.** They are a
  `prophetic-referent` relation inherited at the psalm level from a group of
  psalms (Ps 67, 95, 96, 97), and the disagreement is between two encyclopedia
  articles about the year of the Nativity, not about Ps 95.

### 7.4 Limits the page-2 dossier must preserve

1. **The Introit has no date cell.** It is `nonuniform`, and the concise study must
   print the corpus's absence rather than borrow the Gradual's psalm boundary or
   the Ecclesiasticus interval. The cause is structural: the antiphon is cited to
   Ecclesiasticus and the verse to a psalm, and they have different answers.
2. **The Gospel has no narrated-event date.** The corpus answers `composition-only`
   for Mt 9:1–8 and returns no event date for the healing at Capernaum. The dossier
   must say that the corpus does not date the episode, and must keep composition
   and event visibly distinct, as the profile requires — the absence is the answer,
   not a gap to fill from the life-of-Christ literature.
3. **The Offertory's "date" is a relative one.** `rising in the morning` is what
   Ex 24:4 says, carried as a `narrated-event` relation of
   `israel.wilderness.covenant-at-sinai` with `precision = "relative"`. It is not
   a year and must not be printed as one, and no Exodus date may be supplied from
   elsewhere to make it look like one.
4. **The psalms carry a boundary, not a date.** `before c. 165 B.C.` is the
   Psalter-wide latest-composition boundary, inherited at book scope, and the
   NABRE introduction behind it says in terms that "there is no sure way of dating
   any Psalm." Three elements — Gradual, Alleluia, Communion — carry the same
   boundary for that reason, and the dossier must not present it as three separate
   findings.
5. **Ps 95's 537 B.C. is a superscription setting, not a composition date.** It
   comes from the psalm's own title (*quando domus ædificabatur post captivitatem*)
   and the encyclopedia's date for Zorobabel's raising of the Temple. It sits in the
   same cell as a composition boundary of *before c. 165 B.C.*, and the two are not
   in conflict only because they answer different questions.
6. **The Epistle's two years are two Catholic authorities disagreeing** — Prat's
   table in *St. Paul* against the *Epistles to the Corinthians* article — and both
   must be named.

### 7.5 Controlling chronology evidence in the research seal

The chronology record's sources are eight Catholic Encyclopedia article artifacts,
one NABRE passage, and two Douay–Rheims verse citations (`bible:douay-rheims:Ex.24.3`
and `Ex.24.4`). All of them live under `src/sources/`. The engine seals the
chronology computation code and the identity registry separately, as computation
inputs; they are not source owners and are not declared as such. The Catholic
Encyclopedia and NABRE records are reached through registered binding ancestry and
are bound in `research/source-bindings.toml`.

---

## 8. Calendar, rubrics and occurrence: what this stage re-checked

`research/context.md` resolved the celebration, and this stage's business with it
was to verify it from evidence and correct any error. **One characterisation is
corrected and no substantive claim was falsified.** Everything below was re-read
here, on the page images or in the tracked payloads, and agrees with what that
record states:

- the printed heading `DOMINICA / DECIMA OCTAVA / post Pentecosten` and the rank
  `II classis`;
- the formulary boundary — that it opens after no. 1668, the Postcommunion of
  *Sabbato Quatuor Temporum septembris*, and closes before no. 1679, the Introit
  of the Nineteenth Sunday — and the marginal span 1669–1678;
- the running heads of pp. 410 and 411, and the fact that the head of p. 411 names
  the Nineteenth Sunday over a column that is almost entirely the Eighteenth's;
- **the clipping of the marginal numbers in the right column of p. 410**, which
  this stage re-verified on a strip cropped at that margin at native 500 ppi, and
  the consequence that 1671–1674 are fixed by continuity;
- the abbreviation of the chant rubrics (`Ant. ad Introitum`, `Ant. ad
  Offertorium`, `Ant. ad Communionem` here; `Antiphona ad Introitum` in full for
  the next formulary at no. 1679) as a setting variable and not a different rubric;
- the three textual divergences from the Clementine that record names — the
  Introit's, the Alleluia's and the Communion's — each of which this stage
  confirmed and, for the Introit and the Offertory, carried further (§ 5.1);
- the 1862 antecedent at pp. 350–351, including `Prophetae` capitalised, `Israel`
  without diaeresis, `Exodi 24` without verse numbers and `Per Dominum.`
  throughout, all four re-read on the page images;
- the presence of exactly four `publication_status = "permitted"` rows for this
  Mass in the Latin provenance ledger, for Collect, Offertory, Secret and
  Postcommunion.

**The one correction.** `research/context.md` says the clipped marginal numbers
"run off the fore-edge" of printed p. 410. They do not: p. 410 prints its folio
number at the far left of its running head and p. 411 prints its own at the far
right, so 410 is a verso and its **outer** margin is the left-hand one — which is
intact and carries 1666–1670 legibly. The loss is at the right-hand margin, which
on a verso is the gutter, and the same gutter margin is captured on p. 411, where
1675–1678 print legibly at that page's left edge. The loss is therefore a property
of this one page's reproduction, not a systematic fore-edge loss.
`propers/verified.md` carries the corrected account. **Nothing that record
concludes from the clipping changes**: the numbers still cannot be read whole and
are still fixed by continuity.

One refinement, which corrects nothing: `research/context.md` says of the
Offertory that `in conspectu filiorum Israel` stands "in neither verse" of
Ex 24:4–5, which is true; this stage adds that it stands three verses later, at
Ex 24:17, in both the Latin and the Greek.

Two of that record's statements are **not** re-checked here and are carried on its
authority, because nothing this stage or the study needs depends on them: RG 91's
precedence table, and the stale `source_url` of the Internet Archive `sp07`
facsimile artifact. The rubrical points this stage did re-read — that this is a
second-class Sunday with one oration, that a third-class feast is omitted
outright, and that the Trinity Preface is appointed rather than chosen — it read
in the printed formulary itself (the rank under the heading, the single `Oratio`,
the printed `Præfatio de Ssma Trinitate.`), not in the front matter.

### 8.1 The dated occurrence witnesses are now registered, bound, and bounded

`research/context.md` read two dated annual Ordos for 27 September 2026 live, kept
no bytes, registered nothing, and recorded two response digests so that this stage
could register them if it relied on them. It does rely on them — the study will
print this civil date and cite both Ordos — so this stage registered them, and
found something about them on the way that has to be said plainly.

**What was registered.** Both pages were re-fetched on 2026-09-22, the dated
entries for 27 September read in locally parsed response text, and a dated
edition, artifact and passage written for each:

| Witness | Records |
| --- | --- |
| FSSP France, *Ordo du mois*, <https://www.fssp.fr/ordo-du-mois/> | `edition.fssp-france.ordo-du-mois.web-2026-09-22`, `artifact.….html-0fe38941` (SHA-256 `0fe38941…d203a`, 169,631 bytes, 352 lines), `passage.….2026-09-27` |
| ICRSP France, *Ordo*, <https://icrspfrance.fr/ordo.php> | `edition.icrsp-france.ordo.web-2026-09-22`, `artifact.….html-2233cf19` (SHA-256 `2233cf19…8564d`, 111,681 bytes, 1,679 lines), `passage.….2026-09-27` |

Both passages are bound in `research/source-bindings.toml`, so the evidence for
the date is now inside the research seal and reviewable with the leaf.

**What the registration is worth, and what it is not.** Neither delivery is
byte-stable, and this stage measured that rather than assuming it. Two responses
taken minutes apart on the same day differ:

- the FSSP page by 57,725 bytes and by one byte of length (169,631 against
  169,630), the divergence starting at offset 67,090 in a per-response WordPress
  token `/*wp_block_styles_on_demand_placeholder:<hex>*/` whose differing width
  shifts everything after it;
- the ICRSP page by 110 bytes, all inside a per-response Content-Security-Policy
  `nonce="…"` on its first inline script at offset 1,941.

**So the two digests `research/context.md` recorded on 2026-09-22 can never be
re-obtained, and neither can the ones registered here.** A digest on these pages
identifies one response; it is not a value a reader can reach for. That is part of
why the registered `web-2026-09-17` artifacts' digests no longer reproduce — the
rest is ordinary change, since those responses were also 169,614 and 112,647 bytes
against today's 169,631 and 111,681, so the content moved as well as the token. Each artifact record says so
in its own words, and each is `storage = "restricted"`, so no bytes are retained
and an offline reader has the dated identity and the factual passage, not the
page.

**What the occurrence claim rests on, in order.** (1) The computation, which is a
finding aid: `tools/calendar-days` prints on its own output that every date there
is derived from arithmetic, that the competent calendar, books and annual Ordo
control an actual celebration, and to "never cite this file as an occurrence
witness". (2) The printed rank, rubrics and formulary boundary in the 1962 typical
edition, which this stage read on the page images (above) and which are the
controlling evidence for what the Mass *is*. (3) These two dated institute Ordos,
as corroboration that the date carries this formulary, at second class, in green —
which both do, the ICRSP entry naming the Mass by its Introit incipit, *Da pacem*.
Both are institute calendars, not the universal one: the optional or particular
solemnity of St Thérèse each prints, and the ICRSP *Oratio pro Papa*, belong to
them and are not imported, since a second-class Sunday admits no added oration.
The FSSP page's duplicate *Dimanche 27 septembre* row, headed *de la férie (4ème
classe, Vert)*, was re-read on the live page this round and is still there; it is
an error in that witness and is recorded in the passage record rather than
smoothed.

**The bound a downstream document must keep.** A dated Ordo entry may be cited for
27 September 2026, and both passages above are what it cites. It may not be cited
as though a reader could verify it by re-fetching, and no claim about the
universal calendar may rest on either institute's own observances.

---

## 9. Rights, quotation and publication bounds

- **Latin of the ten proper elements**: publishable on 17 U.S.C. 103(b) with the
  tracked 1862 Pustet as public-domain antecedent; every element's wording stands
  there (`propers/verified.md`). The rubric line *Præfatio de Ss͞ma Trinitate* and
  the Missal's rubrical front matter are 1962 matter: cited, not reproduced.
- **English Scripture**: Douay–Rheims (Challoner), public domain, canonical verses
  only, and never composed to fill the five places where it cannot carry the
  Missal's form.
- **English orations**: 1861 Cummiskey, public domain, registered passage
  `passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.post-pentecosten-18`
  over the **tracked** artifact `…temporal-orations-en` (SHA-256 `c79e9500…1bae0`),
  at its payload lines 164–166, which carry the Collect, Secret and Postcommunion
  and nothing else of this Mass. **One same-family record says otherwise and has
  to be answered.** See § 9.1.
- **Trinity Preface**: no Latin antecedent and no registered historical English was
  established here. Cite it; do not reproduce it until one is.
- **Patristic and medieval texts**: the NPNF volumes and Wilson's and Feltoe's
  editions are public domain; the New Advent and Corpus Thomisticum deliveries
  carry the host's presentation over public-domain underlying texts. The Marietti
  Latin of the *Catena aurea* served by Corpus Thomisticum is a modern edition of
  uncertain status: quote it briefly, as any modern edition, or quote the NPNF
  English of the Fathers it excerpts instead.
- **Restricted**: the CATSS morphological Septuagint is registered
  `storage = "restricted"`; its bytes are held only in the run's scratch, must not
  enter Git, and its readings are reported here rather than reproduced at length.
  The NABRE Psalms introduction is protected prose: summarized and quoted only in
  the one short clause § 7.4 needs.
- **Unregistered page images** — the 1862 leaves n435/n436, the Benziger leaves
  n480/n481, the Gelasian leaves n324/n325 — are retained nowhere. Their
  identities and digests are in § 6 so that a later run can register them.
- No liturgical text is composed, translated or paraphrased by this record.
  English renderings of Latin in `research/interpretations.md` are descriptions of
  arguments for research use; a quotation meant for publication must be taken from
  an identified translation or left in the original.
- **The new Cassiodorus records.** The two Latin files this stage registered
  (§ 6.3) are `rights_status = "public-domain"` on their own basis — a faithful
  transcription of a sixth-century text out of a Migne printing of 1844–1866,
  with every element authored by the host removed by the stated transformation.
  The exact HTML deliveries they came from are `remote` and `unresolved`, because
  monumenta.ch states no terms at all and silence is not a grant. Quote the Latin;
  do not reproduce the host's page.
- **The witnesses added on the second re-entry.** Migne's PG 27, 55, 80, 82 and
  PL 37, 170, the Venice 1745 Aquinas, the 1700 a Lapide and Guéranger's 1909
  English are public-domain printings, and O'Sullivan's 1866 Bellarmine is public
  domain; quote them as their records allow. The Internet Archive page images read
  beside them are unregistered and retained nowhere. The Corpus Thomisticum page
  of Aquinas on 1 Corinthians is `restricted` (a modern delivery of uncertain
  status) and is quoted only in short phrases; the augustinus.it page is `remote`
  with rights unresolved and is quoted nowhere.
- **The two dated Ordos** (§ 8.1) are `restricted`: institutional authored text
  with no affirmative grant. Cite the dated entry as a fact; reproduce no wording.

### 9.1 A same-family record that says this Mass has no publishable English

`src/sources/inventories/roman-1962-proper-translations-v1.toml` is the roman-1962
calendar's English-translation overlay. It carries **four** `[[untranslated]]`
rows for `mass = "pentecost-18"`, `form_id = "main"`, `cycle = "all"`, `lang =
"en"`, `extent = "body"` — Collect, Secret, Postcommunion and Offertory. Each
reads `availability = "unavailable"` with `reason = { kind = "rights-withheld",
source_id = "edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861",
surfaces = ["site-display", "corpus-data", "public-git", "command-line",
"download"] }`, and each carries the same note:

> A historical English lead was formerly stored here, but no exact tracked
> publication artifact and passage binding establishes text that may be served.
> The wording is quarantined until that binding exists.

`research/context.md` cites exactly these rows when it states this Mass's English
position. The file is now declared in `research/review-dependencies.toml` so that
it is sealed with the leaf and a reviewer can check what follows.

**What follows, row by row.** The quarantine is conditional on its own face, and
the condition names two things: a tracked publication artifact and a passage
binding.

- **Collect, Secret, Postcommunion — the condition is met, and the rows are
  stale.** The artifact
  `artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.temporal-orations-en`
  is `storage = "tracked"`, `rights_status = "public-domain"`, SHA-256
  `c79e9500…1bae0`; the passage `…post-pentecosten-18` controls it at
  `physical_line_ranges = [[164, 166]]` and its context names those three orations
  under the 1861 printing's heading `XVIII. SUNDAY AFTER PENTECOST` at printed
  pp. 444–445. This stage read those three lines in the tracked payload. The
  overlay's own stated condition for lifting the quarantine is therefore satisfied
  for these three propers, and the rows are out of date rather than governing.
- **Offertory — the condition is not met, and the row stands.** No tracked English
  of the Offertory antiphon exists: the Cummiskey passage covers the three
  orations and no chant. Nothing in this leaf publishes an English Offertory, so
  nothing here is changed by it, but the row is not stale and must not be reported
  as if it were.

**What this stage does about it.** Nothing to that file. It is another owner's
record, it governs the calendar data and the browser surfaces it names, and a
research stage of one leaf does not edit a repository-wide overlay to suit itself.
The staleness of the three oration rows is reported here for its owner. **The
English route of this study does not change**: the three orations are published
from the registered Cummiskey passage on the public-domain basis above, which is
the basis the overlay's own condition asks for; no English Offertory is published;
and no English is composed or paraphrased anywhere.

---

## 10. Evidence bounds and open items for later stages

1. **One Father of the Gospel's four is still the Catena's, and it is Hilary.**
   Jerome was read whole at his own locus this round, on the page images of PL 26,
   cols. 53–56 (§ 3.5), and everything the study takes from him must come from
   there and not from the Catena, whose Jerome lemma splices two loci and carries
   a tropological sentence the commentary does not have at that place. Hilary's
   *Commentarius in Matthaeum* has no registered route and was not reached;
   attribute him through Aquinas — the *Catena aurea* on vv. 1–2, the lectura on
   v. 8 — or leave him out. Do not present him as read.
2. **The psalms now have five or six direct witnesses each, in Latin and Greek,
   and on Ps 121 they disagree about what the psalm is about.** Ps 121:1 and 121:7:
   Augustine, Cassiodorus, Hilary, Chrysostom, Theodoret, Bellarmine. Ps 101:16:
   Augustine, Cassiodorus, Theodoret, the PG 27 expositions under Athanasius's name,
   Bellarmine. Ps 95:8–9: the same five. What the study may say:
   - **Ps 121 is not read "of the Church and not of a place" by the Fathers.** The
     Latins (Augustine, Hilary, Cassiodorus) read it of the heavenly city built of
     living stones, and Hilary refuses the earthly one; the Greeks (Chrysostom,
     Theodoret) read it of the earthly Jerusalem rebuilt after the captivity and of
     nothing else; Bellarmine gives both, the history first (§ 4.6). An earlier
     draft's sentence that the witnesses agree the psalms are "read of it and not
     of a place" is withdrawn.
   - On Ps 121:7 the *virtus* and the *turres* are read five different ways
     (§ 3.3), and Augustine, in the Latin the English abridges, does read the
     towers.
   - On Ps 101:16 all five read the fear of the nations as following from the
     building of Sion, the Church; Theodoret alone first gives the verse a
     historical sense and then denies that it was fulfilled in it (§ 3.4).
   - On Ps 95:8–9 all five read the courts of the Church; they divide on the
     *hostiae* — a contrite heart (Augustine, Cassiodorus), the sacrifices the
     priests offer in the churches (Theodoret, PG 27), both (Bellarmine) — and on
     the courts (§ 3.8).
   - **Augustine's lemma at Ps 121:1 is not the Missal's** (*Jucundatus sum in his
     qui dixerunt mihi*); his reading of the verse must be attached to it with that
     said (§ 3.2).
   Report every agreement as an agreement of named witnesses, never as "the
   Fathers".
3. **The Introit antiphon has no reception at all** (Ecclus 36:18; § 3.1). **The
   Offertory's cited verses have one later exegete at their own locus** —
   Cornelius a Lapide on Ex 24:4–8, who joins the altar and the covenant blood to
   the Eucharist (§ 3.7) — and no Father; the nearest patristic witness remains
   Chrysostom on Hebrews 9, which is exegesis of Hebrews. The Offertory **as a
   chant** has documented liturgical reception in Rupert and Guéranger (§ 3.11),
   which is reception of the compilation and not exegesis. Say each for what it
   is.
4. **The Offertory's and the Introit's textual sources are unidentified.** What is
   established is negative and exact (§ 5.1). Neither an Old Latin exemplar nor a
   Greek reading was found that accounts for them, and no claim about a compiler's
   source may be made.
5. **The chant-set now has two independent attestations, and neither is a
   manuscript.** § 2.3 rests on (a) Wilson's printed cues in the Hadrianum, with
   his own brackets and query, and (b) the gregorien.info database's report of the
   six Sextuplex books, which gives this Sunday's whole chant-set at AMS *Dominica
   XVIII post Pentecosten* with sigla, confirms Wilson's queried *Qui posuit* as
   the Senlis alleluia, and shows that the 1962's *Timebunt gentes* stands in
   those books as a Gradual at other Sundays. **The second is a database's
   reading, which its own registered record calls an unverified lead**, and the
   day page carrying the chant-set is an unregistered delivery. No manuscript and
   no critical collation was consulted. A study may now say that the set is
   attested as a set at this Sunday in the earliest graduals *as this database
   reports them*; it may not say Hesbert prints it, because Hesbert was not
   opened.
6. **The Gelasian's Book I occurrences are both located** (§ 2.1): the Secret at
   physical lines 12585–12598 in Book I § lix, the Postcommunion at 15341–15344 in
   Book I § xciii, with the section number settled from the edition's own table of
   contents at line 640. No page image of Book I was opened, and none is needed
   for anything this record states.
7. **The Cummiskey English was read in the tracked payload only**, not against the
   1861 scan.
8. **Chronology gaps belong to the chronology owner.** Three would change this
   leaf's page 2 if answered: a narrated-event relation for Mt 9:1–8; a composition
   or attribution answer for Ps 121 and Ps 101 beyond the Psalter-wide boundary;
   and a date for the Sinai covenant that is a date rather than "rising in the
   morning". The leaf's chronology files must be regenerated if any is answered.
9. **No cultural-afterlife or exploratory-proposal audit exists** (§ 5.3), because
   this contract does not require one. Nothing downstream may assume either.
10. **A dated Ordo entry is citable for 27 September 2026 and is not
    re-verifiable.** Both witnesses are now registered, bound and sealed (§ 8.1),
    and both deliveries are measurably not byte-stable, so their digests identify
    single responses. Cite the passages; do not tell a reader they can re-fetch
    them; and take nothing about the universal calendar from either institute's
    own observances.
11. **Four `rights-withheld` rows in the roman-1962 translations overlay name this
    Mass** (§ 9.1). Three are stale on the overlay's own condition and one, the
    Offertory, is not. Nothing downstream may publish an English Offertory.
12. **The registered library was swept three times, and only the third swept it by
    artifact coverage.** The first sweep asked which of the *unreached* leads the
    library held; the second, which of the witnesses the study *already quotes* it
    held (five of eight); both asked by work record. The third, on the second
    re-entry, ran the index for every appointed locus and checked the registered
    collected and whole volumes for every lead, and reached eleven registered
    routes the first two had missed (§ 5.2, § 6.3). **Quotation wording**: the New
    Advent deliveries modernise the 1888 second person and the NPNF English of
    Augustine abridges (§ 6.3); a study that wants an offline-checkable quotation
    should take the CCEL wording, and a study that quotes Augustine's Latin should
    take PL 37. **The one genuinely unregistered delivery** among the reception
    witnesses is the *Catena aurea in Matthaeum*, which is exactly the witness
    §§ 3.5, 4.4 and 10.1 attribute Hilary and Rabanus through; Aquinas's lectura
    now reports Hilary on v. 8 as well.
13. **Both lections now have later reception at their own loci.** The Epistle has
    Theodoret, Aquinas and a Lapide beside Chrysostom, and they divide two against
    two on whether v. 8 accuses (§ 4.7). The Gospel has Aquinas's lectura, which
    among other things raises the Apostles' power to forgive sins at v. 6 and
    answers *per viam administrationis, non auctoritatis* (§ 4.3). Beyond those,
    each lection's later reception is bounded by the registered library, its
    collected volumes and the passage→work index, and by nothing wider (§ 3.5,
    § 3.6, § 5.2).
14. **What a research PASS covers**: study drafting from this bounded evidence. It
    is not a claim to have searched every witness; § 5.2 names, locus by locus,
    what the index returns and what was not reached, and § 6.3 names, for each
    witness reached, which registered route served and which registered routes
    were deliberately not used.
15. **The ministerial and priestly sense has a documented home, and it is not a
    Father's.** At Mt 9:6 in Aquinas (ministry beneath Christ's authority); at
    Ps 95:8 in Theodoret, the PG 27 expositions and Bellarmine (sacrifice offered
    by priests in the churches — a reading of the Communion's verse, not of the
    Gospel); and in the liturgical commentators on this Mass, Rupert (intercession)
    and Guéranger (the power of forgiving sins) (§ 3.11). No Father reads Mt 9:8 of
    it (§ 4.3). The study may use it with those attributions and no others, and
    must not present Rupert's Mass as the 1962's: his paired this Offertory with
    the Gospel of the chair of Moses (§ 2.7).
