# Research scope: resumed Fifth Sunday after the Epiphany (1962), 8 November 2026

Research stage, iteration 0, of `proper-study` v17 run `eb621aedbeee828e`,
5 November 2026. Provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/66-resumed-fifth-after-epiphany`.
This record holds the bounded reception sweep, the checked loci and witness
roles, the textual difficulties on which the interpretations turn, material
disagreements, negative searches, unresolved leads, rights and the evidence
bounds. `research/context.md` settles what is studied; `propers/verified.md`
holds the collated Latin and the English routes; `research/interpretations.md`
holds the readings. This is an independent production: no other provider's
leaf, review or reader link for this identity was opened.

**Iteration 1 (5 November 2026).** The research review of this run found that
held witnesses had been recorded as not held (RES-001), that held liturgical
commentators had been recorded as absent (RES-002), that section 3 claimed a
reading of every held work it had not made (RES-003), and that the dated Ordos
the context record relies on were unregistered (RES-004). This revision
answers each: sections 1, 2.3, 2.4, 3, 4, 5, 6, 7, 8.1, 9, 10, 11, 12 and 13.3
are corrected, and every witness read in this iteration is bound in
`research/source-bindings.toml`. Statements withdrawn are named where they
stood.

## 1. Publication mode and identity

**Appointed-text completeness: `complete`.** No reference-only authorization
exists for this provider and identity (research/context.md, *Publication
mode*). The study can reproduce all ten elements in Latin, because every word
of each stands in the public-domain Pustet 1862 printing read on its page
images (propers/verified.md, *The publication basis of the Latin*), and can
quote public-domain English for every element (section 2.4). No rights limit
forces `rights-limited`.

Identity, occurrence and inventory are as `research/context.md` records them;
this stage re-read the formulary itself on the 1962 page images (PDF 501-502)
and the Epiphany-season Secret and Postcommunion (PDF 129) and found the
inventory, loci, boundaries and conclusion cues as recorded. Three statements
of the context record are completed or corrected here from evidence:

- *"the relation of Lasance's supplementary Masses to the resumed Sundays is
  unestablished"*: established. Lasance 1945, printed pp. 744-747, is
  *Supplementary Mass No. 2. Mass of the Fifth Sunday after Epiphany*, with the
  rubric *If there are twenty-six Sundays after Pentecost, this is said on the
  twenty-fourth …*, and prints this formulary whole, with the *Dicit Dominus*
  chants (propers/verified.md, *English*).
- the context record repeats the overlay's description of the Secret's page as
  *"that book's 'Supplementary Mass No. 3'"*. Printed p. 746 carries the
  running head *SUPPLEMENTARY MASS No. 2*; No. 3 (the Fourth Sunday after the
  Epiphany) begins on p. 747. The locus is right and the label is wrong.
- *"The registered 1862 scan … was not fetched in this stage"*: it was fetched
  whole in this stage and matched its registered hash, and the five pages
  carrying this formulary's words were read on their images.

The Trinity Preface (printed p. 293, no. 1082) and the *Ordo Missae* numbers
cited in the context record were not re-read in this stage; the study needs
only the appointment of the Trinity Preface, which the printed direction after
no. 1756 (read) and RGMR 494 b (read by the context stage) establish.

The two dated Ordos the context stage read (FSSP France, ICRSP France) are the
dated official witnesses of the occurrence chain that `research/context.md`
adopts, and both stay in it. Iteration 1 re-hashed both retained responses
(FSSP 165,240 bytes, `446c71a4…1608`; ICRSP 110,141 bytes, `2827905d…a5a8`;
both matched), read the 8 November 2026 entries in locally parsed response
text, registered each as a dated edition with a passage, and bound both with
role `context`:
`passage.fssp-france.ordo-du-mois.web-2026-11-05.2026-11-08` (*5e dimanche
après l'Épiphanie (transféré)*, second class, green) and
`passage.icrsp-france.ordo.web-2026-11-05.2026-11-08` (*XXIVᵉ Dimanche après la
Pentecôte (3ᵉ de nov., 5ᵉ après l'Épiph.)*, second class, green, no memorial,
*Messe propre (Dicit Dominus)*, Trinity Preface). The library's earlier
registration of the FSSP November section (`web-2026-10-26`) was inspected and
not reused: it was registered for its 1 November entry and its bytes are not
those the context stage read. The books settle the day; the Ordos corroborate
it. The iteration-0 statement that neither Ordo is relied on, registered or
bound is withdrawn.

## 2. Text control, rights and English

### 2.1 Latin

`propers/verified.md` gives all ten elements as printed on 1962 printed
pp. 420-421 (PDF 501-502), read at 200 dpi whole and in 400-dpi crops of every
column section, with the Epiphany-season printing compared at the
Postcommunion's conclusion. The study's Latin follows the resumed printing
(nos. 1749-1758): Collect with written-out conclusion; Secret and
Postcommunion with *Per Dóminum.*

### 2.2 Publication basis

Every word of the ten elements stands in Pustet 1862 on its page images:
orations and lessons at printed pp. 42-44 (*Dominica V. post Epiphaniam*),
chants at pp. 357-358 (*Dominica XXIII. post Pentecosten*), with the rubric
for the resumed Sundays at pp. 358-359. The Latin travels on 17 U.S.C. 103(b)
with that witness under the repository's holding in
`src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`. The
1962 facsimile's own `rights_status = "unresolved"` is untouched and is not the
basis.

### 2.3 The chant forms and the Communion: search for an origin

The context record asked whether a textual source can be identified for the
Introit's Jeremiah cento, the Gradual's *Liberásti nos … in sǽcula*, the
*oratiónem meam* of the Alleluia and Offertory, and the Communion's *Amen dico
vobis, quidquid … fiet vobis*. Result:

- The Pustet 1862 page images carry every one of these forms word for word
  (propers/verified.md). They are therefore not 1962 novelties.
- The Communion's two divergent edges are the words of Mk 11:23 (*Amen dico
  vobis*, *fiet ei*) joined to the body of 11:24. This is a textual
  observation about Mark's own adjacent verse.
- Bl. Ildefonso Schuster, *The Sacramentary* III (1927 English), p. 188 (OCR
  lines 11733-11735), says of the Communion: *"The Communion is drawn from
  St Mark (xi, 24), but it must be out of its proper place. The Gregorian
  Antiphonary has the first verse of Psalm cxxix"*. The sentence is a
  compilation-history claim this stage could not test: no antiphonary or Old
  Latin witness was searched. It is recorded and not used.
- No Old Latin (Vetus Latina), Roman Psalter or antiphonary witness was
  searched for any chant form. The forms' origin is **unresolved**; no study
  may assert one.
- One datum found in iteration 1, recorded and not extended: the psalm text
  that Ambrose expounds at Ps 43:8 reads *Liberasti enim nos ex affligentibus
  nos* (PL 14 col. 1154, page image), and so does the lemma of Cassiodorus
  (PL 70 OCR, with a manuscript variant *de*), where the Clementine Vulgate
  reads *Salvasti enim nos de affligentibus nos*. The Gradual's *Liberásti …
  ex* therefore stands in the Latin psalm text two Latin Fathers expounded.
  Which psalter that is, and how the chant came to it, were not examined; the
  study may state the agreement and no more.

Per the three-document profile, the compilation history is recorded only
where a fact changes a claim. The facts that do: the 1862 and 1962 rubrics
assign the *Dicit Dominus* chants to the resumed Sundays (research/context.md;
propers/verified.md), so a commentator who expounds the chants under
*Dominica XXIII* is commenting on this formulary's chants (section 6).

### 2.4 English: what exists, and the recommended display

- **Douay-Rheims (Challoner)** carries the bodies of the Epistle and Gospel and
  Ps 84:2. It does not carry the Missal's form of the Introit antiphon, the
  Gradual, the Alleluia and Offertory (*orationem meam*), the Communion, or the
  liturgical openings and close of the lessons (propers/verified.md).
- **Lasance 1945, Supplementary Mass No. 2** (pp. 744-747) prints English for
  every element of this formulary, rendering the Missal's chant forms. It is
  public domain in the United States by non-renewal on the repository's record
  (`src/sources/inventories/lasance-new-roman-missal-rights-v1.toml`). The
  supplementary Masses stand in the body of the book, outside the excluded
  appendix and insert that record names.
- **Orations**: Lasance 1945 through the overlay rows (Collect p. 196, Secret
  p. 746, Postcommunion p. 198), read on page images in this stage. The p. 198
  Postcommunion English carries *in these mysteries*; the resumed printing at
  pp. 746-747 omits the phrase. The p. 198 rendering is the fuller one.
- **Guéranger, *The Liturgical Year*, English volume 11 (Dublin 1883,
  Shepherd's translation)**, pp. 524-528, also prints this exact resumed
  formulary in Latin and English (read in its tracked text layer in iteration
  1, not on page images). It is a second public-domain English printing of the
  chant forms; it does not change the recommendation below, and any wording
  taken from it must first be read on its page images.

Recommendation to the author, for review to confirm: give the Douay for the
Epistle and Gospel bodies; for each chant, give Lasance's hand-missal English
of the chant, attributed as such (it is the English of a registered
public-domain witness that prints this formulary, not a translation made for
the study), and where the Douay's canonical verse is cited beside it, say that
the Missal's form differs. The 1962 profile's rule that scriptural elements
take the Douay was written for chants the Douay can carry; for these five the
alternative its own text gives is *"say so and give the Latin … with a
description"*, and a quoted public-domain English of the actual sung form is
the more truthful of the two lawful courses. Under either course nothing is
composed. The Cummiskey 1861 route named in the context record was not read on
page images in this stage and is not recommended.

## 3. Search method

- `tools/commentary-work-index formulary --calendar roman-1962 --mass
  resumed-epiphany-5`: 40 loci compared on their elements, **0 listed, 0
  structural** (2026-11-05). No liturgical commentator in
  `src/sources/commentary/formulary-loci.yaml` matches this Mass. Section 6
  records the commentators found outside the index.
- `tools/commentary-work-index discover --max-results 0` for each distinct
  appointed passage, Psalms in Vulgate numbering, run in iteration 0 and again
  in iteration 1 (2026-11-05; the counts reproduce: Jer 29:11-14, 10 works;
  Ps 84:2, 23; Col 3:12-17, 15; Ps 43:8-9, 17; Ps 129:1-2, 17; Mt 13:24-30,
  21; Mk 11:24, 13). *None registered* is an absence from the library's joins,
  not proof that no copy exists. Section 3.1 gives, for every work reported
  *held* or *held-in-container*, whether its held artifact reaches the
  appointed passage and what was done there. The iteration-0 sentence that
  every such work was opened at the passage was not true and is withdrawn.
- Liturgical commentators beyond the index: the tracked text of every held
  liturgical commentator (Durandus 1568 and 1612, Rupert PL 170, Honorius
  PL 172, Sicard PL 213, Schuster III and V, Guéranger English and French
  volumes) was searched in iteration 0 by literal incipit with
  whitespace-tolerant `grep`. Those searches missed Rupert (the OCR reads
  *cogilationes*), Durandus (the 1612 OCR reads *cogiro co» gitationes* and
  long-s forms) and Guéranger's volume 11, all of which carry this Mass's
  chants. Iteration 1 searched again by heading (*vicesima tertia*, *xxiij*,
  *Twenty-third Sunday*, *Fifth Sunday after the Epiphany*) and by OCR-tolerant
  forms, and read the loci found (section 6). A literal miss over these OCRs
  supports no claim of absence.
- Remote whole files fetched and matched to their registered SHA-256 and byte
  length before reading. Iteration 0: the 1962 CMAA facsimile, Pustet 1862,
  Lasance 1945, PL 26, PL 24. Iteration 1: PL 9 (80,742,141 bytes), PL 107
  (60,617,436), PL 70 OCR (5,244,841), PG 55 OCR (9,609,040), PG 27 OCR
  (6,205,972), PG 82 OCR (8,475,812), PG 124 OCR (3,544,388), the restricted
  Ambrose PL 14 facsimile (54,628,386) and the restricted Corpus Thomisticum
  Super Psalmos 41-50 response (286,376). One new response was acquired and
  registered: the Corpus Thomisticum *Super Colossenses* (`ccl.html`, 140,991
  bytes). Pages relied on were read on rendered images where the binding says
  so; OCR layers otherwise.

### 3.1 Every held work the index lists, passage by passage

"Reaches" means that a held artifact of the work, or of the container the
index names, actually carries the appointed passage. Works the index reports
as *none registered* are not repeated here.

| Passage | Work (index title) | Held artifact reaches the passage? | Opened, and result |
| --- | --- | --- | --- |
| Jer 29:11-14 | Cornelius a Lapide | No: joined by title to his Pauline commentary (Antwerp 1614, which stops at Galatians) and his Pentateuch | — |
| Jer 29:11-14 | Jerome, *In Hieremiam* (PL 24 container) | Yes | Read on page images (section 5) |
| Jer 29:11-14 | Hugh of Saint-Cher | No: the three held responses are his postilla on Pss 83, 94 and 117 | — |
| Ps 84:2 | Augustine, *En. in Ps.* | Yes (NPNF I.8; Latin in the Corpus Corporum part 9) | English read; Latin not collated |
| Ps 84:2 | Cassiodorus (PL 70 container) | Yes, in the remote PL 70 OCR | Read in iteration 1 (OCR) |
| Ps 84:2 | Bellarmine | Yes | Read |
| Ps 84:2 | Theodoret, *In Psalmos* (PG 80 container) | Yes, in a remote 129.5 MB facsimile without text layer | Not read: Athanasius was read as the Greek witness at this verse instead, and the facsimile's size against one verse was judged disproportionate |
| Ps 84:2 | Hugh of Saint-Cher | No (Pss 83, 94, 117 only) | — |
| Ps 84:2 | Athanasius (attrib.), *Expositiones* (PG 27) | Yes, in the remote OCR | Read in iteration 1 (Greek OCR) |
| Ps 84:2 | Bernard, *Sermones de Adventu* (PL 183 container) | Not established: the container's reach in Scripture is not stated, and a literal search of the tracked PL 183 OCR for the verse's words found nothing | Not read beyond that search |
| Ps 84:2 | Cornelius a Lapide | No (as above) | — |
| Ps 84:2 | Aquinas, *Super Psalmos* | No: the lectures end at Ps 54 | — |
| Col 3:12-17 | Cornelius a Lapide (Antwerp 1614 OCR) | No: the held volume stops at Galatians (its artifact record) | — |
| Col 3:12-17 | Chrysostom, *Hom. in Col.* | Yes | Read (NPNF I.13) |
| Col 3:12-17 | Theodoret, *In xiv epistulas* (PG 82 container) | Yes, in the remote PG 82 OCR | Read in iteration 1 (Greek OCR) |
| Col 3:12-17 | Aquinas, Pauline lectures (Dessain 1857) | Only at 3:15b-17: the OCR and its facsimile derivative pass from printed p. 439 to p. 442 | Read at 3:15b-17; the second search (Corpus Thomisticum *Super Col.*, registered in iteration 1) reached 3:12-15a and was read |
| Col 3:12-17 | Hugh of Saint-Cher | No (Pss 83, 94, 117 only) | — |
| Col 3:12-17 | Theophylact (PG 124 container) | Yes, in the remote PG 124 OCR | Read in iteration 1 (Latin column) |
| Col 3:12-17 | Ambrosiaster | No: the one held artifact is his commentary on 1 Corinthians | — |
| Ps 43:8-9 | Augustine, *En. in Ps.* | Yes (NPNF I.8; Latin in the Wikisource part 5) | English read; Latin not collated |
| Ps 43:8-9 | Cassiodorus (PL 70) | Yes | Read in iteration 1 (OCR) |
| Ps 43:8-9 | Bellarmine | Yes | Read |
| Ps 43:8-9 | Theodoret (PG 80) | Yes, in the remote facsimile without text layer | Not read: four further witnesses at this verse were read in iteration 1, Chrysostom's Greek among them, and the facsimile was judged disproportionate; a lead |
| Ps 43:8-9 | Aquinas, *Super Psalmos* (Corpus Thomisticum; Parma vol. 14) | Yes | Read in iteration 1 (both) |
| Ps 43:8-9 | Hugh of Saint-Cher | No | — |
| Ps 43:8-9 | Chrysostom, *Expositio in Psalmos* (PG 55) | Yes, in the remote OCR | Read in iteration 1 (Greek OCR) |
| Ps 43:8-9 | Ambrose, *Explanatio XII Psalmorum* (PL 14 facsimile, restricted) | Yes | Read in iteration 1 on the page image |
| Ps 129:1-2 | Augustine, *En. in Ps.* (NPNF; PL 37 container) | Yes | English read (abridged); PL 37 not opened |
| Ps 129:1-2 | Cassiodorus (PL 70) | Yes | Preface read in iteration 1 (OCR); the verse comment not read |
| Ps 129:1-2 | Hilary, *Tractatus super Psalmos* (PL 9) | Yes | Read in iteration 1 on page images (sections 1-3) |
| Ps 129:1-2 | Chrysostom (PG 55) | Yes | Read in iteration 1 (Greek OCR) |
| Ps 129:1-2 | Bellarmine | Yes | Read |
| Ps 129:1-2 | Theodoret (PG 80) | Yes, remote facsimile | Not read; a lead |
| Ps 129:1-2 | Hugh of Saint-Cher | No | — |
| Mt 13:24-30 | Cornelius a Lapide | No | — |
| Mt 13:24-30 | Gregory, *Homiliae in Evangelia* | No: none of the forty homilies expounds this parable (the held complete text has no *zizani-*) | — |
| Mt 13:24-30 | Hilary, *In Matthaeum* (PL 9) | Yes | Read in iteration 1 on the page image: he declines to expound the parables the Lord explained (13.1) |
| Mt 13:24-30 | Jerome, *In Matthaeum* (PL 26) | Yes | Read on page images |
| Mt 13:24-30 | Chrysostom, *Hom. in Mt.* | Yes (NPNF I.10; the held Greek PG 57 layer stops at homily 44) | English read |
| Mt 13:24-30 | Origen, *Comm. in Mt.* | No: the tracked text is Book XIII (from Mt 17:10); the ANF 9 container has no artifact | — |
| Mt 13:24-30 | Rabanus, *In Matthaeum* (PL 107) | Yes | Read in iteration 1 on page images (book IV) |
| Mt 13:24-30 | Aquinas, *Catena aurea* (index joins *in Lucam* only) | No: the held responses are Luke 4-8 and 14-18 | — |
| Mt 13:24-30 | Aquinas, *Super Mt.* (Venice t. 3) | Yes | Read (OCR) |
| Mt 13:24-30 | Hugh of Saint-Cher | No | — |
| Mt 13:24-30 | Augustine, *Quaest. Ev.* | Yes | Read (Latin) |
| Mk 11:24 | Bede, *In Marc.* | Yes (the Latin text; the PL 92 container excerpt does not) | Read |
| Mk 11:24 | Cornelius a Lapide | No | — |
| Mk 11:24 | Hugh of Saint-Cher | No | — |
| Mk 11:24 | Aquinas, *Catena aurea* | No (Luke only) | — |
| Mk 11:24 | Augustine, *De consensu* (NPNF I.6) | Yes, at II.68 | Opened in iteration 1: it settles only the order of the fig-tree narrative and does not expound the saying |

Beyond the index, iteration 1 also read Augustine's *Sermo* 73 and *Ep.* 93
(NPNF I.6 and I.1), which the index does not join to these passages, and the
liturgical commentators of section 6.

## 4. Passage-by-passage reception matrix

Psalms in Vulgate numbering (Hebrew in parentheses). "Read" means the locus
and the surrounding argument were read in the named bytes; it does not mean
the whole work was examined.

| Passage and proper | Direct ancient exegesis checked | Medieval, Doctoral and later saintly reception checked | Corpora and languages searched | How a retained witness is used | Material negative results |
| --- | --- | --- | --- | --- | --- |
| Jer 29:11-12, 14 — Introit antiphon | Jerome, *In Hieremiam* V, on 29:4-14, PL 24 cols. 891-894 (Latin, page images): read | Liturgical commentators on the antiphon as a chant: Rupert XII.23, Durandus VI.140, Sicard VI.23, Schuster, Fromage quoting Rupert (section 6) | PL 24 scan and OCR; discover list; commentators' OCR and text layers | Direct exegesis: the exiles' prayer, God's foreknowledge, anagogy of return to the Church; commentators: Israel's final return, the Joseph typology, affliction ordered to reconciliation (Durandus) | Theodoret *In Ieremiam*, Rabanus, Albert, Aquinas, Lyra, Denis not registered; Hugh of Saint-Cher held only on other psalms; no Greek witness held at this chapter |
| Ps 84:2 (85:2) — Introit verse | Augustine, *En. in Ps.* 84.1-4 (NPNF I.8, English): read; Athanasius (attrib.), *Expositio in Ps.* 84, hypothesis and v. 2 (PG 27, Greek OCR): read | Bellarmine, *Explanatio in Ps.* 84, v. 2 (O'Sullivan English): read; Cassiodorus, *Expositio* 84, vv. 1-2 (PL 70 OCR): read; Honorius, *Speculum Ecclesiae* sermon headed *Dominica tercia* (PL 172 OCR) on Ps 84:9: read as context | NPNF I.8; PG 27 OCR; Bellarmine; PL 70 OCR; PL 172 OCR | Direct exegesis: captivity of Jacob as captivity of sin turned away by Christ (Augustine, Athanasius with Lk 4:18-21, Cassiodorus); perfect tense of prophetic certainty (Augustine, Cassiodorus); return from Babylon and salvation of the world both prophesied (Athanasius) | Theodoret PG 80 (facsimile without text layer) not read; Augustine's Latin held, not collated; Bernard not established at this verse |
| Col 3:12-17 — Epistle | Chrysostom, *Hom. in Col.* 8 (on 3:12-15) and 9 (on 3:16-17) (NPNF I.13, English): read; Theodoret, *In Col.* 3:12-17 (PG 82, Greek OCR): read | Aquinas, *Super Col.* c. 3 lect. 3: on 3:12-17 in the Corpus Thomisticum response (read in iteration 1) and on 3:15b-17 in the Dessain 1857 OCR; Theophylact on 3:13-16 (PG 124, Latin column): read | NPNF I.13; PG 82 and PG 124 OCR; Corpus Thomisticum; Dessain OCR | Direct exegesis: forbearance and forgiveness on Christ's pattern; peace as umpire (Greek: Chrysostom, Theodoret, Theophylact) / joy that follows peace (Latin *exsultet*: Aquinas); the word dwelling richly; songs of the heart, not the mouth only | Ambrosiaster, Lombard, Haimo, Estius not held at Col; the held Cornelius a Lapide volume stops at Galatians |
| Ps 43:8-9 (44:8-9) — Gradual | Augustine, *En. in Ps.* 43.1-8 (NPNF I.8): read; Chrysostom, *Expositio in Ps.* 43 §6 on vv. 5-9 (PG 55, Greek OCR): read; Ambrose, *Enarratio in Ps.* 43.20-22 (PL 14 col. 1154, page image): read | Aquinas, *Super Ps.* 43 nn. 1-4 (Corpus Thomisticum; Parma vol. 14): read; Cassiodorus, *Expositio* 43, vv. 7-9 (PL 70 OCR): read; Bellarmine, *Explanatio in Ps.* 43: read; Schuster, *Sacramentary* III p. 187: read; Rupert, Durandus, Sicard on the Gradual as a chant (section 6) | NPNF I.8; PG 55 OCR; PL 14 facsimile; Corpus Thomisticum; PL 70 OCR; Bellarmine; Schuster | Direct exegesis: voice of the martyrs; the tense of *Liberasti* read as the certain future (Augustine, Cassiodorus, Ambrose at the resurrection), as remembered deliverance (Bellarmine), as present pledges of providence (Chrysostom), or as present and future both (Aquinas); the saints afflicted spiritually by the sins of those who dwell among them (Aquinas) | Theodoret PG 80 not read; Augustine's Latin held (Wikisource part 5), not collated |
| Ps 129:1-2 (130:1-2) — Alleluia and Offertory | Augustine, *En. in Ps.* 129.1-3 (NPNF I.8, abridged): read; Hilary, *Tract. in Ps.* 129, sections 1-3 (PL 9 cols. 717-720, page images): read; Chrysostom, *Expositio in Ps.* 129 §1 (PG 55, Greek OCR): read | Bellarmine, *Explanatio in Ps.* 129, vv. 1-5: read; Cassiodorus, *Expositio* 129, preface (PL 70 OCR): read; Schuster III pp. 187-188: read; Rupert and Durandus on the Offertory as the brothers' plea (section 6) | NPNF I.8; PL 9 scan; PG 55 OCR; Bellarmine; PL 70 OCR; Schuster | Direct exegesis: this mortal life as the deep; the sinner's cry; the cry from the secret of the heart and not the lips (Hilary, Chrysostom); God hears by nature, faith asks to be heard (Hilary); our part supplied first, then *exaudi* (Chrysostom); propitiation (v. 4, context) as sacrifice | Theodoret PG 80 not read; Cassiodorus's comment on the verses not read; Prosper not registered |
| Mt 13:24-30 — Gospel | Chrysostom, *Hom. in Mt.* 46.1 (NPNF I.10): read; Jerome, *In Mt.* II on 13:24-30 and 13:36-43, PL 26 cols. 89-90, 93-94 (page images): read; Augustine, *Sermo* 73 (NPNF I.6): read; Augustine, *Quaest. Ev.* I.10 (Latin): read; Augustine, *En. in Ps.* 42.2-4 and 64.15-16 (NPNF I.8): read; Augustine, *Ep.* 93 §§10, 15-17, 31-36 (NPNF I.1): read; Hilary, *In Mt.* 13.1 (PL 9 col. 993, page image): read | Rabanus, *In Mt.* IV on 13:24-30 (PL 107 cols. 947-948, page images): read; Aquinas, *Super Mt.* c. 13 on vv. 24-30 (Venice 1745 tomus 3 OCR, pp. 183-185): read; Aquinas, *ST* II-II q. 10 a. 8 ad 1, q. 11 a. 3 ad 3, q. 64 a. 2 ad 1 (English Dominican translation): read; Honorius, *Speculum Ecclesiae*, sermon headed *Dominica tercia* (PL 172 OCR): read | NPNF I.10, I.6, I.8, I.1; PL 26 and PL 9 scans; Latin *Quaest. Ev.*; PL 107 scan; Venice t. 3 OCR; *ST* II-II | Direct exegesis of the parable and of its Lord's explanation; Augustine's own sermon on it; doctrinal reception of *ne forte … eradicetis*; the moral application to bearing injuries and to one's own field (Rabanus) | Hilary declines to expound the parable (13.1); Origen *Comm. in Mt.* X not held; Gregory has no homily on it; Augustine *Contra ep. Parmeniani* III.2 not held: Aquinas's citation of it is a lead only |
| Mk 11:24 — Communion | Bede, *In Marc.* III on 11:22-25 (Latin, PL 92 via Wikisource): read; Chrysostom, *Hom. in Mt.* 67.1-2 on the parallel Mt 21:18-22 (NPNF I.10): read as parallel | Schuster III p. 188 on the Communion: read; Rupert and Durandus on the Communion as Joseph's answer (section 6) | Bede Latin text; NPNF I.10 and I.6; Schuster | Direct exegesis (Bede) of prayer joined to forgiveness; analogue (Chrysostom) on confidence in prayer | Augustine *De consensu* II.68 opened: it harmonizes the narrative order only; Jerome *Tract. in Marc.* not registered |
| Collect *Familiam tuam* | — (composed text) | Schuster on the *Dicit Dominus* Mass does not treat this Collect (his 23rd Sunday has *Absolve*) | Commentator texts searched by incipit; no hit | Verbal echoes only, studied as such (section 7.8) | No commentary on this Collect located in the held commentators |
| Secret *Hostias tibi … placationis* | — | — | Incipit search; no hit | Verbal relation to Ps 129:4 *propitiatio* and Augustine's reading of it (section 7.8) recorded as editorial | No commentary located |
| Postcommunion *Quaesumus … pignus* | — | — | Incipit search; no hit | Studied as a composed text (pledge and effect) | No commentary located |

## 5. Witness register

Standing is from `src/sources/inventories/author-standing-v1.toml`. "Role"
is this study's use. Every locus below was read by this stage in the bytes
named.

| Witness | Standing | Work and locus | Bytes read | Role | What the witness says that the study may use |
| --- | --- | --- | --- | --- | --- |
| John Chrysostom | father | *Hom. in Mt.* 46.1 (on Mt 13:24-30) | NPNF I.10, CCEL text, lines 27066-27201 | direct exegesis | Tares are *"the societies of the heretics"*, sown beside the truth and like wheat; *"while men slept"* warns rulers and subjects; continual watchfulness is possible for *"our moral faculty"*; the servants are brought in *"that He may pronounce it wrong to slay them"*; two reasons: *"If ye are to take up arms, and to kill the heretics, many of the saints also must needs be overthrown with them; or that of the very tares it is likely that many may change and become wheat"*; *"He doth not therefore forbid our checking heretics, and stopping their mouths … but our killing and slaying them."* |
| John Chrysostom | father | *Hom. in Mt.* 67.1-2 (on Mt 21:18-22) | NPNF I.10, lines 37939-37995 | analogue (parallel of Mk 11:22-24) | The fig tree withered *"that He might train them to feel confidence"*; *"many more things shall ye do, being confident in faith and prayer."* |
| John Chrysostom | father | *Hom. in Col.* 8 (on Col 3:12-15) and 9 (on 3:16-17) | NPNF I.13, CCEL text, lines 26655-26775 and 27136-27215, 27347-27380 | direct exegesis | *"Complaint"* makes the offence a petty thing, but *"even as Christ"* obliges forgiveness of great wrongs; love is *"the bond"*, the girding ropes of a ship; the peace of God as umpire between two thoughts, revenge and endurance, giving the prize to endurance *"by persuading him that God is Peace, that He hath made peace with us"*; the word dwelling *"richly"*; Scripture in the home; doing all *"in the Name"*. Chrysostom's Greek reads *brabeuetō* ("let it be umpire") where the Vulgate and the Missal read *exsúltet*. |
| Jerome | father | *Commentariorum in Matthaeum* II, on 13:24-30 and 13:36-43 | PL 26 (Paris 1845) scan, PDF p. 52 (cols. 89-90) and p. 54 (cols. 93-94), page images | direct exegesis | At 13:24-30 he defers: the parable's explanation is given later, *"Non ergo debemus praepropero intelligendi desiderio ante ejus notitiam quaerere, quam a Domino disseratur."* At 13:36-43: *"Homines qui dormiunt, magistros Ecclesiarum intellige"*; *"non dormiat, qui Ecclesiae praepositus est, ne per illius negligentiam inimicus homo superseminet zizania, hoc est, haereticorum dogmata"*; *ne forte … eradicetis*: *"datur locus poenitentiae, et monemur ne cito amputemus fratrem: quia fieri potest, ut ille qui hodie noxio depravatus est dogmate, cras resipiscat"*; he names the difficulty, *Sinite utraque crescere* against *Auferte malum de medio vestrum*, and answers from the plant: wheat and *lolium*, while still in the blade, are nearly indistinguishable; *"ne ubi quid ambiguum est, cito sententiam proferamus; sed Deo judicii terminum reservemus"*, so that God casts out *"non suspicionem criminis, sed manifestum reatum"*. |
| Jerome | father | *In Hieremiam* V, on 29:5-9 and 29:10-14 | PL 24 (Paris 1865) scan, PDF pp. 450-451 (cols. 891-894), page images | direct exegesis | On 29:7, tropologically: *"Quaeramus quoque pacem Ecclesiae … orare praecepit pro inimicis nostris … ut non simus nostra tantum salute contenti, sed inimicorum quoque quaeramus salutem."* On 29:11: God alone knows what he thinks, *"Futurorum igitur scientia soli Deo competit"*; *finem et patientiam* = *"finem captivitatis, et patientiam laborum praesentium, sive spem futurorum"*. On 29:12: *"Certe absque invocatione et oratione captivorum, poterat implere Dominus quod promiserat; sed hortatur eos ad preces, ut quod promissum est, mereantur accipere."* On 29:13 he cites Mt 7:7. Anagogically: *"quamdiu in saeculi hujus confusione versamur … et accepta poenitentia, Deus impleat quod promisit, et reducamur ad locum nostrum Ecclesiam"*; some read the seventy years as the span of a life (Ps 89:10). |
| Augustine | father | *Quaestiones Evangeliorum* I.10 (on Mt 13:25-30) | Latin text (Migne via Corpus Corporum/Wikisource), line 15 | direct exegesis | *"Omnis immunditia in segete, zizania dicuntur."* The tares are separated first because *"tribulatione praecedente separabuntur impii a piis"*, the work of good angels, since *"officia vindictae possunt implere boni bono animo"*. |
| Augustine | father | *En. in Ps.* 42.2-4 (NPNF heading Psalm XLIII) | NPNF I.8, CCEL, lines 14562-14640 | doctrinal illumination of Mt 13:30 (direct exegesis of Ps 42) | In pilgrimage *"I am to live together with the 'tares' even to the time of the 'harvest'"*; *"a certain distinction without separation … the tares however being still tares, and the corn still corn"*; patience needed *"to endure, until the harvest"*. Ps 42 is the psalm of the prayers at the foot of the altar of this Mass. |
| Augustine | father | *En. in Ps.* 43.1-8 (NPNF heading Psalm XLIV) | NPNF I.8, lines 14847-15000 | direct exegesis | The psalm is *"the voice of the Martyrs"* (Rom 8:36 quotes v. 22); v. 8 *"Thou hast saved us"* is *"spoken of the future under the figure of the past … as certain as if it were past"*; v. 9 *"Observe how he intermingles words expressive of a future time"*; then *"what is our state at present? 'But now Thou hast cast us off'"*. |
| Augustine | father | *En. in Ps.* 64.15-16 (NPNF heading Psalm LXV) | NPNF I.8, lines 28068-28115 | doctrinal illumination of Mt 13:24-30 | Tares are *"false Christians, having like leaf, but not like fruit"*, *"darnel … wild oats"*; *"The wheat is not choked by the tares, nay, through endurance of the tares the fruit of the wheat is increased."* |
| Augustine | father | *En. in Ps.* 84.1-4 (NPNF heading Psalm LXXXV) | NPNF I.8, lines 41518-41600 | direct exegesis | *"Thou hast turned away the captivity of Jacob"* is said to Christ: *"not by setting us free from the barbarians … but by setting us free from bad works, from our sins"*; the past tense is prophecy, and the psalmist prays v. 5 *"because they are not yet done"*. |
| Augustine | father | *En. in Ps.* 129.1-3 (NPNF heading Psalm CXXX; abridged) | NPNF I.8, lines 62171-62240 | direct exegesis | *"This mortal life is our deep"*; Jonah's prayer from the deep; those deepest *"do not even cry from the deep"*; v. 4 *"propitiation"* is *"sacrifice … offered for us"*. |
| Bede | father | *In Marci evangelium expositio* III, on 11:22-25 | Latin text (Migne PL 92 via Wikisource), lines 338-339 | direct exegesis | *"Notanda distinctio deprecantium"*: the perfect in faith move spiritual mountains; those not yet perfect *"postulent sibi peccata dimitti … et absque dubio impetrabunt quod petunt, si tamen in se peccantibus aliis primo ipsi dimittunt."* |
| Thomas Aquinas | doctor | *Super Evangelium Matthaei*, c. 13 on vv. 24-30 | Venice 1745 tomus 3 OCR, lines 23995-24275 (printed pp. 183-185) | direct exegesis | Tares are *"filii nequam … specialiter haeretici"*, like wheat; the enemy *"occultum se reddidit"*; the servants' zeal is praised as *ex iussu domini*; four reasons the wicked are not uprooted: the good are exercised by them (1 Cor 11:19), the wicked may become good *"ut Paulus"*, some seem wicked and are not (*"Nolite ante tempus iudicare"*), and a powerful man drags many with him; he states the objection from *Auferte malum* and reports Chrysostom (*"loquitur de occisione"*) and Augustine's change of mind. Augustine's reading of *cum crevisset herba* of the wheat's growth in discernment (1 Cor 2:15) is reported by Aquinas; the Augustinian locus was not found. |
| Thomas Aquinas | doctor | *Summa theologiae* II-II q. 10 a. 8 ad 1; q. 11 a. 3 obj. 3 and ad 3; q. 64 a. 2 ad 1 | English Dominican translation (Gutenberg), lines 5160-5228, 5880-5935, 28535-28585 | doctrinal reception | The parable read through *ne forte*: the prohibition holds *"when the cockle cannot be plucked up without plucking up the wheat"*, citing Chrysostom and Augustine, *Contra Ep. Parmen.* iii.2. Aquinas draws from this a conclusion on the coercion and death of heretics (q. 11 a. 3). See section 8.1. |
| Thomas Aquinas | doctor | *Super Col.* c. 3 lect. 3, on 3:15b-17 | Dessain 1857 vol. 2 OCR, lines 46776-46880 | direct exegesis | *Verbum Christi … habitet … abundanter*: wisdom's origin is the word of Christ; three uses, *"instructionis, devotionis et directionis"*; psalms, hymns and songs *"in cordibus, et non in labiis tantum"*; *"Sunt autem cantica ecclesiae cordis principaliter, sed oris sunt ut excitetur canticum cordis, et pro simplicibus et rudibus"*; *Omne quodcumque facitis* binds *"habitu"*, not every act *"actu"*. |
| Robert Bellarmine | doctor | *Explanatio in Psalmos*: Ps 43 (paragraphs 1, 7-8); Ps 84 (v. 2); Ps 129 (vv. 1-5) | O'Sullivan English, lines 1603-1640, 2987-2995, 4679-4690 | direct exegesis | Ps 43 spoken *"in the person of the Church, or the martyrs of both Testaments"*; vv. 8-9 acknowledge that safety *"is not owing to my own strength"* and that the people *"whenever they shall be delivered … will thank God"*. Ps 84:2: God's eternal decree to bless the land and end the captivity, *"thoroughly accomplished in the resurrection only"*; *Jacob* is *"the whole human race"*. Ps 129: *"two depths, the depth of misery and the depth of his heart"*; v. 5 cites Deut 4:29, *"if thou seek him with all thy heart"*. |
| Augustine | father | *Sermo* 73 (NPNF Sermon XXIII [LXXIII Ben.]), on Mt 13:24-30, sections 1-4 | NPNF I.6, CCEL text, lines 32064-32218 | direct exegesis (iteration 1) | The tares are evil Christians, the same as the wayside, stony and thorny ground of the sower; to the zealous servants: *"be quiet, it is not the time of harvest. That time will come, may it only find you wheat!"*, *"In the field they may be with you, but they will not be so in the barn"*; to the tares: *"amend yourselves before the harvest come"*, *"they who to-day are tares, may to-morrow be wheat"*; to the wheat: *"The angels will come who can make the separation, and who cannot make mistakes"*; *Let both grow* because *"ye are such as may be deceived"*; *"We are but men, the reapers are the angels"*; *"even in these high seats there is both wheat, and tares, and among the laity"*; *"Let the good tolerate the bad; let the bad change themselves, and imitate the good."* |
| Augustine | father | *Ep.* 93 to Vincentius, sections 1, 10, 15-17, 31-36 | NPNF I.1, CCEL text, lines 36024-37100 | doctrinal reception; the coercion question (iteration 1) | §17: *"originally my opinion was, that no one should be coerced into the unity of Christ, that we must act only by words, fight only by arguments, and prevail by force of reason, lest we should have those whom we knew as avowed heretics feigning themselves to be Catholics"*; the opinion was overcome *"not by the words of those who controverted it, but by the conclusive instances"*, his own town first. §10: the penalties, *"such as exile and fines"*, are *"moderate severity, or rather clemency"*, aimed *"rather that you should be admonished to depart from evil, than that you should be punished for a crime"*, set against the death appointed for pagan sacrifice. §§15, 31, 33-34: the Church grows among the tares until the harvest, *"correcting as many as she can, and bearing with those whom she cannot correct"*, and looks for the visible separation *"only on the sea-shore, i.e. at the end of the world"*. §36: Cyprian censured those who would separate themselves, *"assuming to themselves that which the Lord did not concede even to apostles,--namely, the gathering of the tares before the harvest"*. See section 8.1. |
| Hilary of Poitiers | father | *Tractatus in Ps.* 129, sections 1-3 | PL 9 (Paris 1844) scan, cols. 717-720, PDF pp. 375-376, page images | direct exegesis (iteration 1) | §1: God's judgments are inscrutable (Rom 11:33). §2: the prophet cries *"ex interno cordis sui secreto"*; *"existima illum non labiis, sed secreto, ut jussum est, cordis orare"* (Mt 6:6); the cry fits *"aut ignorationi, aut passioni, aut orationi"*; because he cries from the depths he says with confidence *exaudi*. §3: God is everywhere and hears, *"sed orandus a nobis est, ut secundum precem nostram adsit"*; *"Naturae suae est ut audiat; sed fidei nostrae est ut precemur audiri"*; faith asks that he *"qui per naturam suam audit, per orantis precem dignetur audire"*. |
| Hilary of Poitiers | father | *Commentarius in Matthaeum* 13.1 | PL 9 scan, col. 993, PDF p. 511, page image | negative (iteration 1) | *"De parabolis autem jam a Domino absolutis loqui otiosum est"*; the Maurist note (c) names the sower and the tares among them. Hilary does not expound this Gospel. |
| John Chrysostom | father | *Expositio in Ps.* 43, §6 on vv. 5-9 | PG 55 OCR (Greek), lines 20880-20990; no page image | direct exegesis (iteration 1) | At v. 7, fighting the devil: trust not in my arms, my strength or my righteousness, but in God's mercy (Dan 9:18). At v. 8: *"Why speak of the old things?"* we ourselves have many pledges of his providence and can count trophies; *put to shame* means rescued with the shame of the attackers. At v. 9: *all the day* is the whole life; we glory not only when God helps but also when he forsakes (Gal 6:14). |
| John Chrysostom | father | *Expositio in Ps.* 129, §1 on vv. 1-2 | PG 55 OCR (Greek), lines 49325-49440; no page image | direct exegesis (iteration 1) | *Out of the depths*: not simply from mouth and tongue, for words pour out while the mind wanders, but from the deepest heart and the foundations of the mind; such prayer, rooted like a tree, stands against the devil, while prayer from the lips cannot rise to God; in prayer seek not only to receive but to make the soul better; two lessons: *"it is not possible simply to obtain from God unless our part be supplied"*, so he says first *I cried* and then *Hear*; and intent prayer full of compunction has great power to persuade God. |
| Ambrose | doctor | *Enarratio in Ps.* 43, sections 20-22 | PL 14 facsimile (restricted), col. 1154, PDF p. 96, page image | direct exegesis (iteration 1) | Lemma *Liberasti enim nos ex affligentibus nos*. God frees us by the arrows he shoots from heaven into the interior of our earth; the hostile powers are confounded, or the wisdom of the flesh blushes at its crimes; the wicked are confounded here, *"sed multo amplius confundentur; cum viderint sanctos Domini resurgentes"* (Jn 5:28-29); the saint *"non in hac vita, sed in Deo laudabitur"*. |
| Athanasius (attrib.) | no row in author-standing-v1.toml | *Expositio in Ps.* 84, hypothesis and v. 2 | PG 27 OCR (Greek), lines 28660-28800; no page image | supporting (iteration 1) | The psalm shows the calling of the gentiles and then the Jewish people confessing after it; at v. 2, preaching first to the Jews he redeemed many from the spiritual captivity, as the Saviour showed in Isaiah's words, *release to captives* (Lk 4:18-21); he ended our slavery to idols and demons and loosed the chains of sins; both the return from Babylon and the salvation of the world are prophesied. |
| Theodoret of Cyrus | ecclesiastical-writer | *Interpretatio in Col.* 3:12-17 | PG 82 OCR (Greek), lines 47120-47215; no page image | supporting (iteration 1) | Forgive one another, imitating the Master who forgave so many sins; love as the tie-beams of a building; one body: do not divide it, and if tried by another's offence keep peace in the heart as umpire of the contest; continual meditation on the oracles (Deut 6:7); *in your hearts*, *"not with the mouth only"*. His text reads *the peace of God* and *brabeuetō*. |
| Theophylact of Ohrid | ecclesiastical-writer | *In Col.* 3:13-16 | PG 124 OCR (Latin column), lines 103300-103560, cols. 1261-1264 | supporting (iteration 1) | *Et pax Dei palmam ferat*: two thoughts contend, to revenge and to long-suffering; the peace of God as just arbiter gives the palm to long-suffering; the word dwells abundantly when we are rich in the knowledge of the Scriptures. Follows Chrysostom. |
| Cassiodorus | ecclesiastical-writer | *Expositio Psalmorum* 43 vv. 7-9; 84 vv. 1-2; 129, preface | PL 70 OCR, lines 24590-24660, 46770-46840, 72423-72520; no page image | supporting (iteration 1) | Ps 43:8 (lemma *Liberasti enim nos ex affligentibus nos*): *"Confidentia fidei futura pro praeteritis dicunt"*; the saints are freed at the second coming from the spirits who afflict them, which cannot come about generally in this age. Ps 84:2: *"tanquam de praeterito laetus exsultat"*; the captivity of sin, when the world served idols. Ps 129: since no one in a frail body escapes sin, *"Una est ergo securitas in hoc saeculo viventi, jugiter piis precibus inclinari"*. |
| Thomas Aquinas | doctor | *Super Psalmos* 43, nn. 1-4 | Corpus Thomisticum response `cps41.html` (registered, hash matched); Parma 1863 vol. 14 OCR, lines 50488-50720, pp. 515-516 | direct exegesis (iteration 1) | n. 1: the sons of Core are the sons of Christ's passion, properly the martyrs. n. 3: *Salvasti … vel in praesenti … vel in futuro*; *"Sancti dupliciter affliguntur … quandoque affliguntur spiritualiter, quando peccant illi qui habitant apud eos. Et ab his afflictionibus liberantur a Deo"*. n. 4: *tota die* is eternity. |
| Thomas Aquinas | doctor | *Super Col.* c. 3 lect. 3 on 3:12-15a | Corpus Thomisticum response `ccl.html`, paragraph [87858] (registered in iteration 1) | direct exegesis (iteration 1) | *Supportantes invicem*: though one does not himself leave justice, *"aliorum mores sunt ei importabiles"* (2 Pet 2:8, Lot); *donantes*: one forgives when he holds no rancour and procures no evil, *"Sed quando necessitas puniendi est, tunc puniendus est"*; *sicut et Dominus donavit vobis* with Mt 18:32; *pax Christi* is the peace Christ made between God and man; *"Exultet, quia charitatis effectus est gaudium, quod sequitur ex pace"*. |
| Rabanus Maurus | saint | *Commentaria in Matthaeum* IV, on 13:24-30 | PL 107 (Paris 1864) scan, cols. 947-948, PDF p. 478, page images | direct exegesis, moral (iteration 1) | The good seed is sown by one *"qui in corpore suo semen bonae voluntatis ad bonorum operum studet perducere fructum"*; the sleepers warn us *"Ne dum somno inertiae torpemus, fructum laboris nostri perdamus"*; the householder did not burn with anger nor seek quick revenge, *"ita et nos cum aliquam laesionem ab inimicis nostris acceperimus, non statim ad vindictam prorumpere, sed magis ad virtutem patientiae recurrere debemus"*; *"Aequanimiter ergo debemus sufferre malos propter bonos"*; *Sinite* builds longanimity to the end of life (Mt 24:13); at the harvest he who bore patiently repays by justice, *"ut in patiendo justitiam meditemur, et in judicando patientiam habere non negligamus"*; then, from Augustine, the bundles are the sects, and many first tares afterwards become wheat. |
| Sicard of Cremona | ecclesiastical-writer | *Mitrale* VI.23, *Dominica vicesima tertia post Pentecosten* | PL 213 OCR, lines 29945-29990 | liturgical commentary (chants only) | The Introit announces the salvation of *"Israelis reliquiae"* at the end; they answer in the Gradual *Liberasti* with thanksgiving, offer prayer in the Offertory *De profundis*, and *"in communione: Amen dico vobis, recipiunt certificationem"*. In VI.24 he notes that the 24th Sunday *"proprium cantuale non"* has (OCR breaks), i.e. repeats the 23rd's chants. His 23rd Sunday has Phil 3 and the Gospel of the tribute money: evidence for the four chants only (section 6). |
| Ildefonso Schuster | blessed | *The Sacramentary* III (1927 English), 23rd and 24th Sundays after Pentecost, pp. 186-190 | IA OCR, lines 11586-11830 | liturgical commentary (chants only) and rubric | Introit: *"At length we hear the divine answer to our humble supplications of last Sunday"*; *"derived from Jeremias, but with certain textual alterations"*; the Lord *"chastises because he loves"*. Gradual *"well adapted to the celebration of the victories of the martyrs"*. Alleluia: God drawn the more powerfully *"as our misery is greater"*. Offertory: gifts *"accompanied by the incense of humility"*. Communion: Augustine on the conditions of prayer (no locus given). Pp. 189-190: the chants of the last Sunday *"are regularly repeated on each of these supplementary Sunday synaxes"*. His 23rd Sunday has the Collect *Absolve*, Phil 3:17-4:3 and Mt 9:18-26 (section 6). |
| Honorius Augustodunensis | ecclesiastical-writer | *Speculum Ecclesiae*, sermon headed *Dominica tercia* | PL 172 OCR, lines 70286-70395 (registered by source registration as the *Speculum Ecclesiae*'s own segment of that layer, section 13) | reception (supporting only) | Opens on Ps 84:9 (*Loquetur Dominus pacem in plebem suam*) and expounds the tares: the servants are *"praelati Ecclesiae qui cupiunt malos a bonis segregare"*; the Lord forbids it *"ne forte simul reprobentur electi"*; the mixture is willed *"ut boni per malos exerceantur et pro patientia habundantius remunerari mereantur"*, with the series Abel/Cain, Joseph/brothers, David/Saul. The sermon's Sunday is not identified from the OCR's running heads (*Dominica III in Quadrages.*); it is not used as evidence for any Mass. |

## 6. Liturgical commentators

The `formulary` query lists none. Five were found outside the index; each is
identified by elements, never by Sunday number. Standing is from
`src/sources/inventories/author-standing-v1.toml`: Sicard, Rupert, Durandus
and Lucien Fromage are ecclesiastical writers, Schuster is Blessed. An
ecclesiastical writer may be cited for what he says of the elements his Mass
shares with this one, and may support a reading; he does not carry one.

| Commentator, heading | Elements shared with this formulary | Elements that differ | What he says of the shared elements | Use |
| --- | --- | --- | --- | --- |
| Rupert of Deutz, *De divinis officiis* XII.23, *De Dominica vicesima tertia post Pentecosten* (PL 170 cols. 329-330, OCR lines 23697-23778; read in iteration 1) | Introit *Dicit Dominus*, Gradual *Liberasti*, Offertory *De profundis*, Communion *Amen dico vobis* | Lesson Jer 23:5-8 (*Ecce dies veniunt*) before the Gospel of the five loaves (Jn 6); no Collect, Alleluia, Secret or Postcommunion named | In this last office of the year the Church gives thanks for the future salvation of Israel's remnant (1 Tim 2:1; Rom 9:27). The Introit's *cogitationes pacis* are the promise of the banquet of grace with his brethren according to the flesh, prefigured in Joseph, who received the brothers who had sold him; freed from the captivity of souls, they give thanks in the Gradual; in the Offertory they say to the true Joseph *Obsecramus ut obliviscaris sceleris fratrum* (Gen 50:17); the Communion is his answer, *Nolite timere … Deus vertit illud in bonum* (Gen 50:19-21). | Principal witness, with Sicard, to the four chants as one sequence; ecclesiastical writer, supporting only; never cited for a link between the chants and the tares. |
| William Durandus, *Rationale* VI.140 *De xxiij Dominica post Pentec.*, with VI.141-142 (1612 Lyon tomus secundus OCR, lines 17384-17535, printed pp. 412-413; read in iteration 1) | Introit, Gradual, Offertory, Communion | Epistle Phil 3 (*Fratres imitatores*), Gospel of the tribute money (*Abeuntes*, in some churches); Alleluia *Qui sanat contritos corde* in some churches; VI.141 says the twenty-fourth Sunday has no chant office of its own; VI.142 sets the same chants before Jer 23 and the Gospel of the five loaves | The last three Sundays share one office, in which the Church shows the wedding garment of charity by praying for the conversion of the Jews at the end, signified in Joseph. Introit: their conversion and the Lord's promise, *quia ad hoc tendunt mala quae vobis infero: ut reconciliem vos mihi*. Gradual: David's thanks for deliverance from spiritual and bodily captivity; its verse promises the praise of good works. Offertory: they ask pardon as Joseph's brothers did. Communion: Joseph, that is Christ, answers *Nolite timere*, *quia liberalis est Dominus, et cito dimittit*. | Second witness to the sequence; ecclesiastical writer, supporting only. |
| Sicard of Cremona, *Mitrale* VI.23, *Dominica vicesima tertia post Pentecosten* (PL 213 OCR) | Introit, Gradual, Offertory, Communion | Epistle Phil 3 (*Corpus humilitatis nostrae configurabit*), Gospel of the tribute money; no Collect named | Section 5. | As Rupert. Never cited for a connection between the chants and the tares. |
| Ildefonso Schuster, *Sacramentary* III, *Twenty-third Sunday after Pentecost* | Introit, Gradual, Alleluia, Offertory, Communion | Collect *Absolve*, Epistle Phil 3:17-4:3, Gospel Mt 9:18-26, Secret, Postcommunion | Section 5. | Supporting witness for the chants; may carry with a Father or saint (Blessed). Pp. 189-190 state the resumed-Sunday arrangement. |
| Lucien Fromage, *The Liturgical Year* (Guéranger's series, English volume 11, Dublin 1883), *Twenty-third Sunday after Pentecost* pp. 486-490; *Twenty-fourth and Last Sunday* pp. 501-502; *The Fifth Sunday after the Epiphany* pp. 524-528 (text layer; read in iteration 1) | At pp. 486-490 the five chants; at pp. 524-528 the whole formulary | At pp. 486-490 the 23rd Sunday's Collect, Epistle and Gospel, and the ancient Epistle Jer 23 and Gospel Jn 6 he reports | He reports that the Gospel was once the five loaves and the Epistle Jer 23, *"equally applicable to the conversion of the Jews"*, and quotes Rupert XII.23 at length for the chants. At pp. 501-502 he states that the intervening Sundays are taken from those after the Epiphany, the Introit, Gradual, Offertory and Communion being repeated from the twenty-third, and that with twenty-six Sundays the Fifth after the Epiphany becomes the twenty-fourth. At pp. 524-528 he prints this formulary without commentary, with the Magnificat antiphon *Colligite primum zizania*. | A witness to the reception of Rupert's reading and to the resumed-Sunday rule; ecclesiastical writer; adds no exegesis of his own here. |

The 1568 Durandus composite's table of contents (OCR lines 765-772) lists the
same chapters, VI.140-142, at printed pp. 278-279; its text was not read, the
1612 printing being read instead. Searched with no commentary found:
Honorius's *Gemma animae* (the hit is in the *Speculum Ecclesiae*, section 5);
the three orations' incipits in every commentator's text (iteration 0, literal
search, bounded as above). Rupert's PL 170 OCR also has one hit for *Dicit Dominus, ego cogito
cogitationes pacis* at line 49970 that is not Rupert: the *Chronicon S.
Laurentii Leodiensis* printed in the same volume tells that Bruno of Toul (Leo
IX) heard angels sing these words; Durandus VI.140 repeats the story. It
supports no claim.

The iteration-0 statements that Rupert's only hit was the chronicle, that the
1612 Durandus *tomus secundus* might not contain book VI (it opens with *LIBER
SEXTVS*), and that the held Guéranger volumes contain neither the Sundays after
Pentecost nor the Fifth Sunday after the Epiphany are withdrawn.

## 7. The consequential textual difficulties

The test of the three-document profile: the appointed words that raise the
question, what each principal witness infers, and what changes if the answer
is accepted.

### 7.1 Gospel: *Sínite útraque créscere* against discipline

**Words.** *Vis, imus, et collígimus ea? Et ait: Non: ne forte colligéntes
zizánia, eradicétis simul cum eis et tríticum. Sínite útraque créscere usque
ad messem.* Against it stands the Apostle's *Auferte malum ex vobis ipsis*
(1 Cor 5:13), which Jerome and Aquinas both name.

**Inferences.**
- Jerome: the reason is in the plant. Wheat and *lolium* look alike *quamdiu
  herba est*; so where a case is ambiguous judgment is reserved to God, who at
  the end removes *manifestum reatum*, not suspicion. *Ne forte* gives *locus
  poenitentiae*: the one corrupted today may defend the truth tomorrow.
  Expulsion of the manifest is not excluded.
- Chrysostom: the prohibition concerns killing. Bloodshed would kill saints
  with heretics, and tares may become wheat. Restraint — silencing,
  dispersing assemblies — is not forbidden.
- Aquinas (*Super Mt.*): four reasons, of which the second (*qui modo malus
  est, postea bonus fit, ut Paulus*) agrees with Chrysostom and Jerome, the
  third (*Nolite ante tempus iudicare*) with Jerome's ambiguity; the
  prohibition holds *si non possit sine periculo*. In *ST* II-II he makes *ne
  forte* the condition of the whole command (section 8.1).
- Augustine, *Sermo* 73 (his own sermon on this Gospel, read in iteration 1):
  the servants are refused *"For ye are such as may be deceived"*; the reapers
  are angels *"who cannot make mistakes"*; *"they who to-day are tares, may
  to-morrow be wheat"*; wheat and tares stand in the clergy's seats and among
  the laity alike; *"Let the good tolerate the bad; let the bad change
  themselves"*. With *En. in Ps.* 42 and 64: the present is *"distinction
  without separation"*, and enduring the tares increases the wheat's fruit.
  His *Ep.* 93 shows what he later held about coercion (section 8.1); the
  sermon itself names no penalty.
- Rabanus (iteration 1, moral sense): the householder's patience toward the
  enemy is the pattern for bearing injuries without revenge; *"Aequanimiter
  ergo debemus sufferre malos propter bonos"*, lest retaliation give the good
  occasion of scandal; *Sinite* asks longanimity to the end of life.
- Hilary (*In Mt.* 13.1) declines to expound a parable the Lord explained, as
  Jerome defers at 13:24-30.

**What changes.** If Jerome's answer is accepted, the parable governs
judgment under uncertainty and the patience it commands is a patience of
judgment; if Chrysostom's, it governs the use of force; Aquinas's reading
makes it a rule of prudence about harm to the good. Augustine's own sermon
gives Jerome's ground (the servants may be deceived; only the angels cannot
err) and Chrysostom's (the tare may become wheat) together, and adds the
charge to the bad to change; Rabanus turns the command into the moral rule of
bearing personal injury. All agree that the command's ground is the wheat and
the possibility of conversion, not indifference to the tares. This is the
difficulty on which interpretation 1 turns.

### 7.2 Gospel: *Cum autem dormírent hómines*

**Words.** The enemy sows *while men slept*; the parable assigns no fault and
the Lord's explanation (13:37-39) does not gloss the sleepers.

**Inferences.** Jerome (13:36-43): the sleepers are *magistri Ecclesiarum*,
and the warning is to those set over the Church. Chrysostom: the warning is
to rulers *"and not the rulers only, but the subjects too"*; natural sleep is
unavoidable, moral sleep is not, hence *"continual watchfulness"*.

Rabanus (iteration 1) applies it to each person: *"Ne dum somno inertiae
torpemus, fructum laboris nostri perdamus"*, the good seed being sown by one
who in his own body strives to bring good will to good works.

**What changes.** The detail the Lord leaves unexplained becomes, in these
witnesses, a charge of vigilance; Jerome confines it to pastors, Chrysostom
extends it to every hearer, and Rabanus reads the field as each person's own.
Interpretation 3 turns on that extension.

### 7.3 Gospel: *the field is the world* (13:38) and *out of his kingdom* (13:41)

The Lord's explanation, read in the Douay and Clementine (Mt 13:36-43) though
not appointed, says *the field is the world* and that the angels gather *out
of his kingdom all scandals*. The held witnesses place the tares inside the
Church: heretics (Chrysostom, Jerome, Aquinas), false Christians (Augustine,
*En. in Ps.* 64.15). Aquinas: *seminantur in agro, ideo in hoc mundo*, yet the
enemy sows *in medio tritici, et fidelis populi*. The study must not make the
field simply "the Church" against the Lord's gloss, nor simply "the world"
against the Fathers' application. Augustine holds both in *Ep.* 93 §31: the
Church the Son of man sowed grows among the tares, *"For the field is the
world, and the harvest is the end of time"*; *Sermo* 73 §1 has the Lord's own
gloss, *"His field the whole world"*, with *"evil Christians among the good"*.
His argument from *de regno eius* in *Contra ep. Parmeniani* is not held
(section 10).

### 7.4 Introit: the cento and what it leaves out

**Words.** The antiphon keeps *cógito cogitatiónes pacis, et non
afflictiónis*, *invocábitis me, et ego exáudiam vos*, *redúcam captivitátem
vestram de cunctis locis*; it drops God's *scio* and *ait Dominus*, puts
*Dicit Dóminus* first, and omits *ut dem vobis finem et patientiam*, *et
ibitis … et orabitis me*, v. 13 (*seek … with all your heart*), and the
gathering *de universis gentibus*.

**Inferences.** Jerome reads the omitted words as the hinge: God *could* have
restored the exiles without their prayer, but commands it *ut quod promissum
est, mereantur accipere*; *finem et patientiam* is the end of captivity and
endurance meanwhile. His anagogy places the reader in the *confusio* of this
age awaiting the return *ad locum nostrum Ecclesiam*. Schuster reads the
antiphon as God's answer and a promise of the Redeemer. Durandus reads *non
afflictionis* of the purpose of affliction: *ad hoc tendunt mala quae vobis
infero: ut reconciliem vos mihi*. On the same question asked of the
Offertory's psalm, Hilary answers that God hears by nature but faith asks to
be heard (*Naturae suae est ut audiat; sed fidei nostrae est ut precemur
audiri*), and Chrysostom that one cannot simply obtain from God unless one's
own part is supplied first (section 5).

**What changes.** With Jerome, the antiphon's *invocábitis me* is a command
to pray inside a promise already made, which is the question the Communion
answers; Hilary and Chrysostom, commenting on the psalm the Mass sings twice,
give the same answer from God's side and from the petitioner's. The study may observe the omission as a textual fact; it may not say
the compilers omitted the words for a purpose.

### 7.5 Gradual: *Liberásti* — memory or prophecy?

**Words.** Perfect tenses, *Liberásti … confudísti*, cut from a psalm whose
next verse turns: *But now thou hast cast us off* (Ps 43:10-26, read whole).

**Inferences.** Augustine: the perfect is prophecy *"as certain as if it were
past"*; the psalm then states the present, and the whole is the martyrs'
voice. Cassiodorus agrees (*futura pro praeteritis*: the saints freed at the
second coming), and Ambrose places the full confusion of the enemies at the
resurrection. Bellarmine: the verses acknowledge past deliveries, so that the
people will thank God whenever delivered; the complaint follows; martyrs of
both Testaments. Chrysostom: why speak of the forefathers? we ourselves hold
*pledges* of providence now, and glory in God even when he forsakes us.
Aquinas: *vel in praesenti … vel in futuro*, and the saints are afflicted not
only in body but *spiritualiter, quando peccant illi qui habitant apud eos*.
Schuster: the Gradual fits the martyrs' victories.

**What changes.** Augustine, Cassiodorus and Ambrose make the Gradual a
confession of a deliverance not yet seen; Bellarmine a memory that grounds
trust; Chrysostom a present experience; Aquinas allows both present and
future. The Gradual stops before the lament either way; the study may say
what it keeps and what follows it in the psalm, and must give more than one
reading of the tense.

### 7.6 Epistle: *pax Christi exsúltet*

**Words.** The Missal and Vulgate read *exsúltet* (rejoice); the Greek that
Chrysostom expounds reads *brabeuetō*, "let it act as umpire".

**Inferences.** Chrysostom builds the moral argument on the umpire: two
thoughts wrestle, and peace gives the prize to endurance; Theodoret and
Theophylact (iteration 1) read the same word the same way. Aquinas, read in
iteration 1 in the Corpus Thomisticum text after the Dessain OCR was found to
lack the passage, expounds the Latin: peace springs from charity, *"Exultet,
quia charitatis effectus est gaudium, quod sequitur ex pace"*, and the peace
is Christ's, made between God and man.

**What changes.** The Greek reading makes peace the judge of an inner
contest; the Latin makes joy the fruit of peace. A study that quotes
Chrysostom must say that he reads a different word than the Mass sings, and
must not attribute *exultation* to him or *umpire* to the Latin; Aquinas may
be cited for what the Mass sings.

### 7.7 Communion: prayer that receives

**Words.** *quidquid orántes pétitis, crédite quia accipiétis, et fiet vobis*,
appointed without Mk 11:25, which joins prayer to forgiveness.

**Inferences.** Bede reads vv. 22-25 together and makes forgiveness the
condition for the not-yet-perfect: they will obtain *si tamen in se peccantibus
aliis primo ipsi dimittunt*. Chrysostom (Mt 21 parallel) makes the fig tree a
lesson in confidence in prayer. Schuster appeals to Augustine on the
conditions of prayer without a locus (not used).

**What changes.** With Bede, the Communion's unconditional sound carries the
condition the Mass's Epistle states (*donántes vobismetípsis … sicut et
Dóminus donávit vobis*). The connection between Bede's condition and the
Epistle is the editor's; Bede states only his half.

### 7.8 The orations

No witness held comments on these three orations. What the texts say, from
their own words:

- **Collect.** God is asked to guard *Famíliam tuam* with *contínua pietáte*;
  the reason is that the family *in sola spe grátiæ cæléstis innítitur*, leans
  on the hope of heavenly grace alone; the petition is protection, *tua semper
  protectióne muniátur*. The same incipit opens the Twenty-first Sunday's
  Collect with another petition (research/context.md); the study must quote
  this one whole.
- **Secret.** *Hóstias … placatiónis*, "offerings of propitiation"; two
  petitions: absolution of sins, and *nutántia corda tu dírigas*, that God
  direct wavering hearts. *Placatio* and Ps 129:4 *propitiatio* are different
  words; any link the study draws between the Secret and Augustine's reading of
  Ps 129:4 as sacrifice is editorial synthesis.
- **Postcommunion.** The Mass gives a *pignus*, pledge, of a salvation whose
  *efféctus* is still asked for. The distinction pledge/effect is the
  oration's own.

## 8. Material disagreements and differences

### 8.1 Coercion: Chrysostom, Augustine's own change of mind, and Aquinas

The disagreement is stated from each author's own locus.

- **Chrysostom** (*Hom. in Mt.* 46.1) reads *ne forte* as forbidding the
  killing of heretics and allowing lesser restraint: stopping their mouths,
  taking away their freedom of speech, breaking up their assemblies.
- **Augustine**, *Ep.* 93 to Vincentius (read in iteration 1). He says that
  his own first opinion was *"that no one should be coerced into the unity of
  Christ, that we must act only by words, fight only by arguments, and prevail
  by force of reason, lest we should have those whom we knew as avowed heretics
  feigning themselves to be Catholics"*, and that it was overcome by examples,
  his own town first, brought to unity *"by fear of the imperial edicts"*
  (§17). The coercion he came to accept is the imperial laws' penalties,
  *"such as exile and fines"*, which he calls *"moderate severity, or rather
  clemency"*, aimed at admonition rather than punishment, and which he sets
  beside the death that imperial law appoints for pagan sacrifice (§10). What
  the parable forbids, in this letter, is separation before the harvest: the
  Church grows among the tares until the end, *"correcting as many as she can,
  and bearing with those whom she cannot correct"*, and looks for the visible
  separation only at the end (§§31-34); the Donatists claimed what the Lord did
  not concede even to apostles, *"the gathering of the tares before the
  harvest"* (§36). The letter does not argue from the parable to the penalties;
  it argues for them from their effects. *Sermo* 73 names no penalty.
- **Aquinas.** In *Super Mt.* c. 13 he holds the prohibition *si non possit
  sine periculo* and reports both Chrysostom and Augustine's change of mind. In
  *ST* II-II q. 10 a. 8 ad 1 and q. 11 a. 3 ad 3, citing Augustine's *Ep.* 93
  and *Contra Ep. Parmen.* iii.2 (not held), he makes *ne forte* the condition
  of the whole command, and in q. 11 a. 3 he concludes to the death of
  convicted heretics who persist after admonition. That conclusion is Aquinas's own. Augustine's letter, as
  read here, accepts fines and exile for correction and does not ask for death;
  it must not be cited for Aquinas's conclusion.

This is a real disagreement within the tradition about the parable's reach,
and the study must keep it as one. Two cautions bind the authors. First, the
parable's literal sense, as the held witnesses state it, is patience grounded
in the wheat and in conversion; Augustine's acceptance of correction by law and
Aquinas's penal conclusion are doctrinal receptions of the conditional *ne
forte*, not the parable's own teaching. Second, the Church's later teaching on
religious liberty (the Second Vatican Council's declaration *Dignitatis
humanae*, 1965) is a doctrinal development that this research did not read; a
study that reproduces Aquinas's conclusion must either leave it as Aquinas's
historical position or treat the development from a source actually read. The
recommended course is the first, with the disagreement stated plainly and
claim-locally, each position under its own author's name.

### 8.2 *Liberásti*: Augustine and Bellarmine

Section 7.5. Complementary emphases (prophetic certainty: Augustine,
Cassiodorus, Ambrose; remembered deliverance: Bellarmine; present pledges:
Chrysostom; both: Aquinas), not a doctrinal conflict.

### 8.3 The sleepers: Jerome and Chrysostom

Section 7.2. Jerome restricts the warning to pastors; Chrysostom extends it to
all; Rabanus to each person's own field. Complementary.

### 8.4 Greek and Latin at Col 3:15

Section 7.6. A difference of text, not of doctrine: the Greek witnesses
(Chrysostom, Theodoret, Theophylact) read *brabeuetō* of an umpire; the Latin
(Aquinas) reads *exsultet* of the joy that follows peace.

### 8.5 What the tares are

Heretics (Chrysostom, Jerome, Aquinas *specialiter*), all wicked children
(Aquinas's wider class), all uncleanness in the crop (Augustine, *Quaest.
Ev.*), false Christians like in leaf (Augustine, *En. in Ps.* 64), evil
Christians in the clergy and the laity alike (Augustine, *Sermo* 73). The
witnesses agree that the tares resemble wheat and grow in the same field; they
differ in how narrowly they name them.

## 9. Chronology: the generated record inspected

`research/chronology.toml`, `research/chronology-annotations.tex` and
`research/chronology-table.tex` were generated on 2026-11-05 with `tools/tpt
proper-chronology record --write` and `annotations --presentation
orientation-v3 --write` (default profile `catholic-comprehensive-v1`). Every
element's status is `composition-only`; the orations carry no Scripture. Rows
and their scope, inspected:

| Passage (element) | Context printed | Date printed | Inspection |
| --- | --- | --- | --- |
| Ps 43:8-9 (Gradual) | Historical setting: occasion date unresolved; composition: the Psalms of the Sons of Korah | Between the days of Isaias and the return from exile | Title *for the sons of Core* (Douay Ps 43:1) read; the Catholic Encyclopedia *Psalms* article (tracked article text) names the Korahite group. No occasion is supplied; Bellarmine's mention of Antiochus and the Roman persecutions is exegesis, not a dated occasion. Unresolved occasion correctly preserved. |
| Ps 84:2 (Introit verse) | as above | as above | Title read (Douay Ps 84:1). No occasion supplied; correct. The verse's *captivity* is not dated by the record, and the study must not date it. |
| Ps 129:1-2 (Alleluia; Offertory) | Composition: Psalms | Before c. 165 B.C. (critical boundary) | No attribution in the title (*Canticum graduum*, not appointed). The record holds only the critical latest-composition boundary; no traditional date is available; correct. |
| Jer 29:11-12, 14 (Introit) | Composition: Jeremias's letter to the exiles after Jechonias's deportation; Jerusalem to Babylon. Final formation: the received book after enlargement | After Jechonias and the deportees had departed from Jerusalem; after the first authentic recension | Douay Jer 29:1-3 read: the letter is sent *after that Jechonias … were departed*, by Elasa and Gamarias, from Jerusalem to Babylon. Jerome (col. 892) places it *in principio Sedeciae regis*; the record gives no absolute year and the study must not add one. |
| Mt 13:24-30 (Gospel) | Narrated event: Jesus tells the parable … beside the sea; composition: Matthew | Date unresolved; composition disputed: six ranges | Mt 13:1-3, 24, 34, 36 read: the parables are spoken to the crowds from the boat by the sea, and he then goes into the house. The setting description is supported; the parable's fictional field is not dated. |
| Mk 11:24 (Communion) | Composition: Mark; Rome traditionally | Disputed: six ranges | The saying's narrative setting (the morning after the cleansing of the Temple, on the way into Jerusalem, Mk 11:12-21) has no event row; the record is composition-only, which is honest. |
| Col 3:12-17 (Epistle) | Composition: Colossians; Rome traditionally; addressed to Colossae | Disputed: A.D. 61; A.D. 61-63 | The Catholic Encyclopedia *Colossians* and *St. Paul* articles (tracked article texts) read at the captivity-epistle and chronology passages. |

No date reaches the study except through these generated records. No
`research/chronology-profile-comparisons.toml` is declared.

**An open alternative for the Gradual's psalm, not in the generated record.**
The controlling Catholic Encyclopedia *Psalms* article (its tracked article
text, line 218) reports that Delitzsch and Perowne, *"on historical grounds"*,
admit Ps xliv (Hebrew; the Gradual's Ps 43 in Vulgate numbering) to be
Machabean, says that *"There are no certain proofs that these or any psalms
are Machabean"*, and reports that the Biblical Commission (1 May 1910) will
not allow that the Psalter contains many Machabean psalms. Bellarmine's
mention of Antiochus at Ps 43 is exegesis, and no witness read dates the
psalm's occasion. The generated row names the Korahite group, not the psalm,
as its dated subject, so it prints no false passage date; but the open
alternative its own source reports is absent from it. It is not admitted to
the shared chronology corpus by this stage, because that corpus is shared data
under this run's research seal and its owner must decide under
`guidance/scripture-chronology.md` whether a reported critical opinion that
its source calls unproved is an alternative to carry. It is reported in
section 11. The study must not date Ps 43 to the Maccabean period, and may
say only that the controlling source reports the opinion and calls it
unproved.

## 10. Negative results and unresolved leads

Iteration 1 withdraws the iteration-0 entries that recorded held witnesses as
not held or not located: Augustine's *Sermo* 73 and *Ep.* 93 (held in NPNF
I.6 and I.1), Hilary's *Tract. in Ps.* 129 (PL 9 from line 57478), Rabanus on
Mt 13 (PL 107), Cassiodorus and Chrysostom on the appointed psalms (remote
layers), and the liturgical commentators of section 6. All were read.

- **Not held:** Augustine, *Contra epistulam Parmeniani* (cited by Aquinas;
  lead); Origen, *Comm. in Mt.* X (the tracked English text is Book XIII);
  Theodoret on Jeremias; the Greek of Chrysostom's *Hom. in Mt.* 46 and 67
  (the library's PG 57 layer carries homilies 1-44 only; the NPNF English is
  the read witness); Paschasius Radbertus, Chromatius, Bruno of Segni,
  Lombard, Lyra, Albert, Denis, Euthymius, Walafrid, Haimo, Estius (not
  registered); Hugh of Saint-Cher at any appointed passage (held only at Pss
  83, 94 and 117).
- **Held and not read, with the reason:** Theodoret, *In Psalmos* (PG 80) on
  Pss 43, 84 and 129, held only as a 129.5 MB facsimile without a text layer;
  Athanasius was read at Ps 84 and Chrysostom at Pss 43 and 129 as the Greek
  witnesses; a lead. Cassiodorus's comment on Ps 129:1-2 itself (his preface
  was read). Augustine's Latin of Pss 42, 43, 64 and 84 (held; the English was
  read, not collated). The 1568 Durandus (the 1612 printing was read).
  Bernard's Advent sermons at Ps 84:2 (the container's reach is not stated; a
  literal search of its OCR found nothing).
- **Negative on opening:** Augustine, *De consensu* II.68 does not expound Mk
  11:24; Gregory's *Homiliae in Evangelia* has no homily on the tares; Hilary
  declines to expound the parable (*In Mt.* 13.1).
- **Unresolved textual history:** the origin of the chant forms (section 2.3),
  with the one datum that Ambrose's and Cassiodorus's psalm text reads
  *Liberasti … ex affligentibus*.

## 11. Shared-record defects observed (reported, not repaired)

1. `src/sources/inventories/roman-1962-proper-translations-v1.toml`, Secret
   row for `mass = "epiphany-5"`: the witness note calls Lasance p. 746
   *Supplementary Mass No. 3*; the page belongs to *Supplementary Mass No. 2*
   (the resumed Fifth Sunday).
2. `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml`,
   Collect row for `epiphany-5`: *"1862 sets a colon after innititur"* follows
   the text layer; the 1862 page image prints a comma.
3. The same ledger has no rows for this formulary's five chants
   (`pentecost-23`) or its two lessons, and none for the resumed printing
   nos. 1749-1758 (already reported by the context stage).
4. `src/sources/calendars/roman-1962/propers.yaml` resolves this Mass's
   Postcommunion through `epiphany-5` with the expanded conclusion; the resumed
   printing prints *Per Dominum.* (already reported by the context stage).
5. `src/sources/commentary/formulary-loci.yaml` has no locus for Sicard,
   *Mitrale* VI.23, or Schuster, *Sacramentary* III, 23rd Sunday, both of which
   expound the *Dicit Dominus* chants by name; nor (found in iteration 1) for
   Rupert, *De divinis officiis* XII.23 (PL 170 cols. 329-330), Durandus,
   *Rationale* VI.140-142 (1612 tomus secundus pp. 412-413; 1568 pp. 278-279),
   or Fromage, *The Liturgical Year* vol. 11 pp. 486-490 (English) and its
   French equivalent, all of which name the *Dicit Dominus* chants. Each shares
   the four chants and differs in the lessons (section 6). Reported to the
   owner of that file.
6. The Lasance passage
   `passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.publish-phase4-en31-epiphany-5--main--secret--all--1`
   carries the same *Supplementary Mass No. 3* label in its `locus`.
7. `work.bede.in-marci-evangelium-expositio` declares a `locus_pattern` that
   admits only *Mc.10.32-45*, so a binding cannot name the Mk 11:22-25 locus read
   here; the binding states it in its context instead.
8. The PL 172 OCR is filed as an artifact of *Gemma animae*; the sermon read
   here belongs to the *Speculum Ecclesiae* printed in the same volume, which had
   no work record. Resolved by source registration (section 13): the work, its
   1895 edition and a whole-work segment of the same layer are registered, and
   the binding names the segment.
9. The shared Scripture chronology corpus carries no row for the Maccabean
   dating of Ps 43 (Hebrew 44) that the controlling Catholic Encyclopedia
   *Psalms* article reports and calls unproved (section 9). Reported to its
   owner for a disposition under `guidance/scripture-chronology.md`; not
   changed here.
10. Theodoret's commentary on Colossians and Theophylact's on the Pauline
    epistles have no work records of their own: the PG 82 and PG 124 layers that
    carry them are filed as artifacts of Theodoret's Galatians commentary and
    Theophylact's John commentary. The bindings name those artifacts and state
    the locus in their context.
11. `src/sources/inventories/author-standing-v1.toml` has no row for
    Athanasius of Alexandria, whose attributed Psalm expositions are read at
    Ps 84 (section 5); he is used as a supporting witness only.

## 12. Evidence bounds

The sweep is bounded by the library's holdings, by section 3.1, and by the
searches named. English translations (NPNF, O'Sullivan, Dominican *Summa*)
were the read witnesses for Chrysostom's homilies, Augustine's sermons, letter
and Psalm expositions, Bellarmine and the *Summa*; their originals were not
collated. OCR texts (Aquinas Venice, Dessain and Parma, Sicard, Schuster,
Honorius, Rupert, Durandus, Cassiodorus, Theophylact) and the Guéranger text
layer were read as text layers, not on page images; Chrysostom on the Psalms,
Athanasius and Theodoret were read in uncorrected Greek OCR, with no column
figure claimed. The Corpus Thomisticum responses were read in locally parsed
text. The Latin of Jerome, Hilary, Rabanus and Ambrose was read on page
images. No claim is made to have
found all witnesses; a later sweep should begin with the leads in section 10.

## 13. Source registration and reusable-source dispositions

Source-registration stage, iterations 0 and 1, of the same run, 5 November
2026. `research/source-dispositions.toml` gives every binding of
`research/source-bindings.toml` at least one row, pinned to the binding's
digest and the source's fingerprint. Iteration 0 wrote 46 rows over the first
36 bindings. Iteration 1, after research iteration 1, re-pinned the rows of
the two changed bindings (22, whose Homily 9 loci were extended, and 36, whose
role became reception), added a row for Rupert's chant commentary on binding
36, and gave bindings 37-55 their rows: 74 rows over 55 bindings, of which 3
are `admitted`, 40 `deferred`, 2 `rejected` and 29 `not-commentary`. The
research stage's results were re-read against its retrieval receipts and the
library's records; nothing below rests on a receipt alone.

### 13.1 Receipts re-verified

The five remote whole files the research and context stages fetched were
re-hashed on 2026-11-05 and each matched its registered SHA-256 and byte
length: the 1962 CMAA facsimile (82,815,941 bytes), Pustet 1862
(102,880,787), Lasance 1945 (75,268,976), PL 26 (63,426,233) and PL 24
(67,109,688). The tracked text artifacts bound here are hash-checked by
`tools/source-library validate`.

Iteration 1 re-hashed every remote or restricted whole file that research
iteration 1 read, and each matched its registered SHA-256 and `byte_size`:
PL 9 PDF (80,742,141 bytes), PL 107 PDF (60,617,436), the restricted PL 14
facsimile of Ambrose (54,628,386), the PG 55 (9,609,040), PG 27 (6,205,972),
PG 82 (8,475,812) and PG 124 (3,544,388) text layers, the PL 70 text layer
(5,244,841), the Corpus Thomisticum responses for *Super Psalmos* 41-50
(286,376) and *Super Colossenses* (140,991), and the two Ordo responses of
2026-11-05 (FSSP 165,240; ICRSP 110,141).

### 13.2 Registered by this stage

- **Honorius, *Speculum Ecclesiae*.** A work record
  (`work.honorius-augustodunensis.speculum-ecclesiae`), its 1895 Garnier PL 172
  edition, and a whole-work segment of the PL 172 text layer already held under
  *Gemma animae* (physical lines 63969-86480, from the heading at col. 807 to
  the closing rubric before the *Elucidarium* at col. 1109). The containment
  inventory enters *Gemma animae* as container-shaped by that segment. Binding 35
  now names the segment; the lines read (70286-70395) were re-read.
- **Augustine, *Quaestiones Evangeliorum* I.10.** A verified passage holding the
  whole answer, copied mechanically from the bound Latin text (line 15, without
  the numeral and Migne's bracketed reference), with its canonical edge Mt
  13:25-30 in `src/sources/commentary/fragment-loci.yaml` and an English
  `not-surveyed` row in `translation-absences.yaml`. Admitted.

Registered by research iteration 1 and reviewed by registration iteration 1:
the FSSP *Ordo du mois* and ICRSP *Ordo* editions of 2026-11-05 with their
restricted response artifacts and their 8 November passages, and
`work.thomas-aquinas.super-colossenses` with its Corpus Thomisticum edition and
restricted response. Their bytes were re-hashed (13.1). The aliases were
checked: the dated Ordo editions follow the existing series of web states, and
the *Super Colossenses* work joins the harvest's *Super Epistolas S. Pauli
lectura* lead by title in `commentary-work-index discover` at Col 3:12-17,
beside the Dessain volume II collection that also prints the lectures (13.6
item 4). Iteration 1 registered nothing new: no witness bound in research
iteration 1 meets the Catena's admission criteria (each row below says which
are missing), and no excerpt was made to fill a gap.

### 13.3 The checked-witness matrix, by registration

Psalms in Vulgate numbering. "Binding" is the one-based index in
`research/source-bindings.toml`.

| Witness and locus read | Binding | Canonical extent of the row | Disposition | What admission still needs |
| --- | --- | --- | --- | --- |
| Chrysostom, *Hom. in Col.* 8 | 22 | Col 3:12-15 | admitted (existing verified passage and edge) | — |
| Chrysostom, *Hom. in Col.* 9 | 22 | Col 3:16-17 | admitted (existing verified passage and edge) | — |
| Augustine, *Quaest. Ev.* I.10 | 26 | Mt 13:25-30 | admitted (registered here) | — |
| Chrysostom, *Hom. in Mt.* 46.1 | 21 | Mt 13:24-30 | deferred | translator credit on the constituent edition; passage; Greek not held |
| Chrysostom, *Hom. in Mt.* 67.1-2 (analogue) | 21 | Mt 21:18-22 | deferred | the same |
| Jerome, *In Mt.* II, col. 89 | 23 | Mt 13:24-30 | deferred | retained page; checked transcription; passage |
| Jerome, *In Mt.* II, cols. 93-94 | 23 | Mt 13:36-43 | deferred | the same |
| Jerome, *In Hier.* V, cols. 891-892 | 24 | Jer 29:4-7 | deferred | the same |
| Jerome, *In Hier.* V, cols. 893-894 | 24 | Jer 29:10-14 | deferred | checked transcription; passage (the page is already retained) |
| Augustine, *En. in Ps.* 42, 43, 64, 84, 129 (NPNF I.8) | 27 | Ps 42:1-3; 43:1-10; 64:12-13; 84:1-5; 129:1-4 | deferred, one row each | unabridged text; the Latin; passages; for 43 and 84 the boundary of the chant's comment |
| Aquinas, *Super Mt.* c. 13 | 28 | Mt 13:24-30 | deferred | page-image collation; passage |
| Aquinas, *ST* II-II (three articles) | 29 | Mt 13:29-30 | deferred | the Latin; passage; excerpt boundaries; a harvest alias group |
| Aquinas, *Super Col.* c. 3 lect. 3 | 30 | Col 3:15-17 | deferred | page-image collation; passage |
| Bellarmine, *Explanatio* on Pss 43, 84, 129 | 31 | Ps 43:2 and 43:8-9; 84:2-3; 129:1-5 | deferred, one row each | unabridged text; the Latin; page-image collation; passages |
| Bede, *In Marc.* III | 32 | Mk 11:22-25 | deferred | a locus grammar on the work record; page-image collation; passage |
| Sicard, *Mitrale* VI.23-24 | 33 | the chants: Jer 29:11-12, 14; Ps 43:8-9; Ps 129:1-2; Mk 11:24 | deferred | page-image collation; passage; a harvest alias group |
| Schuster, *Sacramentary* III | 34 | the same | deferred | the Italian original; page-image collation; passage; a harvest alias group |
| Honorius, *Speculum Ecclesiae*, *Dominica tercia* | 35 | Mt 13:24-30; Ps 84:9 | deferred | page-image collation; passage; a harvest alias group |
| Rupert, *De div. off.* XII.23 | 36 | the verses quoted: Jer 29:11; Ps 43:8; Ps 129:1; Mk 11:24 | deferred | the reach of each chant comment; page-image collation; passage; a harvest alias group |
| Augustine, *Sermo* 73 (NPNF I.6) | 37 | Mt 13:24-30; 13:37-39 | deferred | a work, edition and segment record; a harvest alias group; passage |
| Augustine, *De consensu* II.68 | 37 | candidate Mk 11:24 | rejected | it argues the order of Mt 21 and Mk 11 and does not expound the verse |
| Augustine, Ep. 93, sections 15 and 31-36 | 38 | Mt 13:24-30; 13:38-39 (applied) | deferred | a work record; a harvest alias group; excerpt boundary; passage |
| Hilary, *Tract. in Ps.* 129.1-3 | 39 | Ps 129:1-2 | deferred | retained page; checked transcription; passage |
| Hilary, *In Mt.* 13.1 | 39 | candidate Mt 13:24-30 | rejected | he declines to expound the parables the Lord resolved |
| Durandus, *Rationale* VI.140-142 | 41 | the verses quoted: Jer 29:11, 14; Ps 43:8-9; Ps 129:1; Mk 11:24 | deferred | page-image collation; passage; a harvest alias group |
| Fromage (*Liturgical Year* 11), pp. 486-489 | 42 | the verses Rupert quotes | deferred | the comment is Rupert's, quoted in Shepherd's English from the French; the originals; page-image collation; passage |
| Chrysostom, *Exp. in Ps.* 43 section 6 and 129 section 1 (PG 55) | 43 | Ps 43:5-9; 129:1-2 | deferred, one row each | a tracked controller; page-image collation; passages |
| Athanasius (as printed), *Exp. in Ps.* 84 (PG 27) | 44 | Ps 84:1-3 | deferred | a tracked controller; page-image collation; review of the ascription; passage |
| Cassiodorus, *Exp. Ps.* 43, 84, 129 (PL 70) | 45 | Ps 43:7-9; 84:1-2; 129:1 | deferred, one row each | a tracked controller; page-image collation; passages |
| Ambrose, *In Ps.* 43.20-22 (PL 14) | 46 | Ps 43:8-9 | deferred | a publishable witness (only a restricted facsimile is held); checked transcription; passage |
| Aquinas, *Super Ps.* 43 nn. 1-4, Corpus Thomisticum | 47 | Ps 43:1-9 | deferred | a publishable controller; passage |
| Aquinas, *Super Ps.* 43 nn. 1-4, Parma 1863 OCR | 48 | Ps 43:1-9 | deferred | page-image collation; passage |
| Aquinas, *Super Col.* c. 3 lect. 3, Corpus Thomisticum | 49 | Col 3:12-17 | deferred | a publishable controller (no public-domain witness of 3:12-15a is held); passage |
| Rabanus, *In Mt.* IV (PL 107 cols. 947-948) | 50 | Mt 13:24-30 | deferred | retained page; checked transcription; passage |
| Theodoret, *In Col.* (PG 82) | 52 | Col 3:13-16 | deferred | a work record; a tracked controller; page-image collation; passage |
| Theophylact, *In Col.* (PG 124 Latin column) | 53 | Col 3:13-16 | deferred | a work record; translator credit; the Greek; a tracked controller; page-image collation; passage |

Every other binding is `not-commentary`: the 1962 and 1862 Missals and the
1862 text layer, the Lasance missal, its text layer and its three overlay
passages, the Douay-Rheims and Clementine texts, the psalm concordance, the
PL 24, PL 9 and PL 107 OCR layers used to locate Jerome, Hilary and Rabanus,
the chronicle sighting in the PL 170 volume, the sections of Ep. 93 on
coercion (a letter's argument, used for section 8.1), the rubrical statements
and the printed formulary in *The Liturgical Year* vol. 11, and the two dated
Ordo passages for 8 November 2026.

Searched and not bound: the literal incipit searches of section 3 over the
held Durandus, Guéranger, *Gemma animae*, Hilary (PL 9) and Rabanus (PL 107)
text layers were whitespace-tolerant `grep`, not the repository's canonical
search modes, so no negative-search binding records them. Their misses are
bounded in sections 3 and 10 and support no claim of absence.
(Research iteration 1: those misses were false negatives for Durandus,
Guéranger volume 11, Hilary and Rabanus, as they were for Rupert. Each of
these is now read and bound, and registration iteration 1 gave each its
disposition rows above; see sections 3, 5 and 6.)

### 13.4 Holdings this stage corrected or added to the record

- Migne's Latin of Augustine's *Enarrationes* is held for Psalms 41-50
  (`artifact.augustine.enarrationes-in-psalmos.2026-10-23-latin-migne-wikisource.wikisource-part-5-latin`),
  61-70 and 81-90 (the 2026-09-05 Corpus Corporum parts 7 and 9). It covers
  Pss 42, 43, 64 and 84 and was not read; Ps 129 is not held in Latin. Section 4's
  statement that Augustine's Latin of Ps 43 is not tracked is corrected there.
- The Greek of Chrysostom's *Hom. in Mt.* 46 and 67 is not held: the library's
  PG 57 layer carries homilies 1-44 only. Section 10 is corrected.
- Jerome's PL 24 cols. 893-896 are already retained offline as
  `artifact.jacques-paul-migne.patrologia-latina-volume-24.paris-1865.jeremias-29-columns-893-896-20261102`,
  and the Pustet 1862 pages of this formulary as
  `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.resumed-epiphany-5-evidence-pages-20261102`.

### 13.5 Retention

The remote whole files stay remote under their existing records (size; the
1962 facsimile's and the Lasance PDF's artifact rights are recorded as
unresolved). The pages read on the PL 26 scan (PDF 52 and 54) and on the PL 24
scan (PDF 450) were extracted and checked, but are not entered: the offline
delivery index admits only paths in the Git index, and this stage runs no Git
command. Those rows therefore name `retained-page-image` as a missing
criterion. No Lasance page was retained: its artifact rights are unresolved and
the delivery is encrypted against page merging.

In iteration 1 the same holds for the pages read on the PL 9 and PL 107 scans
(Hilary, cols. 717-720 and 993; Rabanus, cols. 947-948): they are not retained,
and their rows name `retained-page-image`. The PG 55, PG 27, PG 82, PG 124 and
PL 70 text layers stay remote under their existing records, the PL 70 layer's
own rights being unresolved. The Ambrose facsimile and the two Corpus
Thomisticum responses are restricted and keep no bytes in the library; their
rows name `publishable-controller`.

### 13.6 Defects for other owners found at registration (not repaired)

1. `edition.john-chrysostom.homiliae-in-matthaeum.ccel-web-2026-09-17` names no
   translator, though the volume's constituent title (lines 149-155) credits
   Prevost's translation revised by Riddle. The Catena refuses a translation
   fragment from it; adding the credit moves the fingerprints that other
   leaves' reviewed bindings pin, so it needs its owner's review.
2. No tracked, checked transcription carries the English of Lasance's
   *Supplementary Mass No. 2* chants (printed pp. 744-747). Section 2.4
   recommends quoting that English; the author stage has only the remote page
   images, so the wording it quotes must be read on them and recorded as such,
   or a checked transcription registered first.
3. The defects already listed in section 11 stand: items 1-7 and 9-11 are
   unrepaired, item 8 is resolved above.
4. Found in iteration 1: `src/sources/inventories/source-containment-v1.toml`
   enters the Dessain volume II collection
   (`work.thomas-aquinas.in-omnes-pauli-epistolas-commentaria`) with only 2
   Corinthians and Ephesians as constituents, so `discover` at Col 3 reports
   the passage outside it, although binding 30 reads the Colossians lectures in
   that volume's OCR and `work.thomas-aquinas.super-colossenses` now exists. The
   inventory's rule admits a constituent only from the container's own records
   or a segment pointing into it; the container's records do not name
   Colossians, and a segment would need the lectures' bounds in the OCR, which
   this stage did not establish. Reported to the inventory's owner.
5. Found in iteration 1: `src/sources/commentary/work-aliases.yaml`, which the
   harvest derives, has no group for Augustine's sermons or letters, for
   Aquinas's *Summa*, or for the liturgical commentators Rupert (*De divinis
   officiis*), Durandus, Sicard, Schuster and Honorius. A Catena row must name
   a group, so none of these witnesses can be admitted until one exists. This
   is the harvest owner's; this stage writes no alias.
