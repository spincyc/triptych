# Research scope: Twenty-fourth and Last Sunday after Pentecost (1962), 22 November 2026

Research stage, iteration 0, of `proper-study` v19 run `11c5af05fe374203`,
16 November 2026. Provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/68-twenty-fourth-after-pentecost`.
This record holds the bounded reception sweep, the checked loci and witness
roles, the textual difficulties on which the interpretations turn, material
disagreements, negative searches, unresolved leads, rights and the evidence
bounds. `research/context.md` settles what is studied; `propers/verified.md`
holds the collated Latin and the English routes; `research/interpretations.md`
holds the readings. This is an independent production: no other provider's
leaf, review or release record for this identity was opened. This provider's
resumed Sixth Sunday leaf (`67`) shares this formulary's five chants; its
research records were used only to locate held loci for those chants, and every
locus relied on below was read afresh in this stage in the bytes named. Nothing
of that leaf's conclusions is adopted.

**Iteration 1 (16 November 2026).** This record was revised by the research
stage, iteration 1, answering the research review (RES-001 to RES-003, and the
advisory RES-004). Changed: section 2.4 (the English display now follows the
1962 profile: Douay for the lessons and wherever the chant is the Vulgate
verse); sections 4, 5 and 6 (Sicard's *Mitrale* VIII.23 and VIII.25 read and
registered; Durandus VI.142's words attributed to Sicard VIII.25, which he
reproduces; Rupert cited only for what he writes); section 9 (the Gospel now
has a narrated-event row, added by this stage to the shared chronology corpus;
the Psalm occasion rows' bound stated); sections 10, 11 and 13.2.

## 1. Publication mode and identity

- **Mode.** Not reference-only: research/context.md, *Publication mode*,
  verified against `guidance/liturgy/propers-production-plan.md` (no line
  `Authorized reference-only …` names this provider and identity). The ordinary
  appointed-text mode applies. Every element's Latin and English has a lawful
  route (section 2), so the expected completeness is `complete`.
- **Identity, occurrence and inventory.** research/context.md was read whole
  and its findings checked where this stage re-read the same pages: the
  printed heading, rank, marginal numbers 1769-1778 and boundaries on PDF
  503-505 (200 and 400 dpi, re-rendered by this stage from the re-hashed
  facsimile); the ten-element inventory, the oration conclusions and the
  wording against the Clementine (propers/verified.md). No contextual error was
  found. One item the context left for research is closed: the 1862 Gospel
  citation, which the text layer reads *c. 21.*, is *c. 24.* on the page image.
- **Dated witnesses.** The two dated Ordo responses that research/context.md
  reads for 22 November 2026 were re-hashed in the resolve-context scratch
  area, matched, and read again by this stage (FSSP: *Dimanche 22 novembre —
  24e et dernier dimanche avant la Pentecôte (2ème classe, Vert)*; ICRSP:
  *XXVIᵉ et Dernier Dimanche après la Pentecôte (5ᵉ de nov.)*, II classe, green,
  Gloria, Credo, Trinity Preface, *Messe propre (Dicit Dominus) du dernier
  Dimanche après la Pentecôte*, no memorial). This stage registered both as
  dated institutional witnesses, without retained bytes:
  `passage.fssp-france.ordo-du-mois.web-2026-11-16.2026-11-22` and
  `passage.icrsp-france.ordo.web-2026-11-16.2026-11-22`, with their editions and
  restricted artifacts (`…html-4c47a491`, `…html-d2d89328`). They corroborate
  the occurrence; the printed rubrics control it.
- **Precedence tool.** `tools/tpt calendar-rubrics day --calendar roman-1962
  --date 2026-11-22 --json`, which refused during the resolve-context stage, was
  run by this stage on 2026-11-16 once the workspace's generated rubrics product
  was present. It agrees with the printed rubrics research/context.md read:
  winner `last-sunday-after-pentecost`, II class (RG 12; RG 91 row 15),
  `settled`; St Cecilia (III class, RG 91 row 24) `omitted` (RG 111; RGMR 434 b);
  one oration in low and sung non-conventual Masses. It is a finding aid; the
  printed rubrics control.

## 2. Text control, rights and English

### 2.1 Latin

`propers/verified.md` gives all ten elements as printed on 1962 printed
pp. 422-424 (PDF 503-505), read on page images. The study's Latin follows that
page.

### 2.2 Publication basis

Every word of the ten elements stands in Pustet 1862, *Dominica XXIV. et
ultima post Pentecosten*, printed pp. 359-360 (PDF 445-446), read on its page
images. The Latin travels on 17 U.S.C. 103(b) with that witness under
`src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`. The
differences are orthography, pointing, capitalisation, one conclusion cue and
citation form (propers/verified.md). The 1862 is the formulary's own printing
under its own heading, not a borrowing from the Twenty-third Sunday.

### 2.3 The chant forms and the lessons' departures: search for an origin

The chants depart from the Clementine at the Introit (a cento of Jer
29:11-14), the Gradual (*Liberásti … et eos, qui nos odérunt … in sǽcula*), the
Alleluia and Offertory (*oratiónem meam*) and the Communion (*Amen dico vobis,
quidquid … et fiet vobis*); the Epistle opens *Fratres: Non cessámus* and reads
*voluntátis Dei*; the Gospel opens with the liturgical *In illo témpore: Dixit
Iesus discípulis suis*.

- The Pustet 1862 page images carry every one of these forms word for word.
  They are not 1962 novelties.
- Read in this stage: Augustine's lemma of Ps 43:8-9 in *En. in Ps.* 43.8-9
  (tracked Latin, part 5, line 35) reads *Salvos enim fecisti nos ex
  affligentibus nos, et eos qui oderunt nos confudisti* and *confitebimur in
  saecula*: his Latin psalter shares the Gradual's *et eos qui … oderunt* and
  *in saecula*, against the Clementine *odientes nos* and *in saeculum*, and
  reads *Salvos … fecisti* where the Gradual reads *Liberásti*. Hilary's lemma
  of Ps 129:2 in *Tract. in Ps.* 129 (PL 9 OCR, line 57624) reads *Domine
  exaudi vocem meam*, the Clementine form, not the chant's *oratiónem meam*.
  Jerome's lemma of Jer 29:11-14 (PL 24 col. 893) is the Vulgate's, with *ut
  dem vobis finem et patientiam* and *et ibitis*, which the antiphon lacks.
  These are textual observations, not derivations.
- No psalter, antiphonary or Old Latin (Vetus Latina) witness was searched for
  any chant form or for the Epistle's *Dei*. The forms' origin is
  **unresolved**; no study may assert one.

Per the three-document profile, compilation history is recorded only where a
fact changes a claim. The facts that do are in section 6: medieval commentators
whose Sunday shares this Epistle but not this Gospel or these chants; Durandus's
report that *in quibusdam ecclesiis* this Gospel was read on that Sunday; the
explanation Sicard gives, and Durandus repeats, for a Sunday without proper
chants; and Fromage's claim about when the Matthean Gospel came to close the
year, which this stage did not verify and which no study may repeat as fact.

### 2.4 English: what exists, and the recommended display

- **Lasance 1945**, printed pp. 736-740, prints English for every element of
  this formulary, rendering the Missal's chant forms, the Epistle's *voluntátis
  Dei* and both lessons' liturgical openings; its Gospel is the Douay lightly
  revised. Public domain in the United States by non-renewal on the
  repository's record (`src/sources/inventories/lasance-new-roman-missal-rights-v1.toml`);
  these pages stand in the body of the book, outside the excluded appendix and
  insert. Read on page images in this stage (propers/verified.md, *English*).
- **Douay-Rheims (Challoner)** carries the bodies of the Epistle and Gospel
  (not their liturgical openings, nor *Dei*) and Ps 84:2; not the Introit
  antiphon, the Gradual, the Alleluia and Offertory or the Communion.
- **Guéranger's *Liturgical Year*, English vol. 11** (Dublin 1883; the
  continuation, by Lucien Fromage), pp. 503-514, prints the formulary in Latin
  and English with commentary; its Alleluia English reads "hear my prayer". It
  is a second public-domain route, not recommended over Lasance.
- **Cummiskey 1861** (`passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.post-pentecosten-ultima`),
  named in research/context.md, was not opened in this stage; it is not
  needed, since Lasance carries every element.

Recommended display (revised in iteration 1 to follow
`guidance/liturgy/roman-1962-propers.md`, *English*, which assigns the
scriptural elements to the Douay-Rheims (Challoner), "the English of the
Vulgate the missal prints", and the orations to a public-domain hand missal
cited by formulary):

- **Epistle (Col 1:9-14) and Gospel (Mt 24:15-35).** The Douay-Rheims
  (Challoner), attributed, for the body of each lesson. The Missal's
  liturgical openings are disclosed as Missal forms, not blended into the
  Douay: the Epistle's *Fratres: Non cessámus* stands where the Vulgate (and
  the Douay, "Therefore we also, from the day that we heard it, cease not")
  opens *Ideo et nos ex qua die audivimus, non cessamus*; the Gospel's *In illo
  témpore: Dixit Iesus discípulis suis: Cum vidéritis* stands for *Cum ergo
  videritis* (Douay "When therefore you shall see"). The Missal's *voluntátis
  Dei* is the Douay's "his will" (*voluntatis ejus*); a study that gives the
  Missal's reading says it is the Missal's, and may give Lasance's "the will
  of God" and his openings ("Brethren"; "At that time, Jesus said to His
  disciples") as Lasance's rendering of the Missal's words. Lasance's lesson
  English is not the display text: his Gospel is the Douay with light
  revisions (propers/verified.md).
- **Introit verse (Ps 84:2).** The Douay: the Missal's verse is the Vulgate's.
- **Chants whose Latin is not the Vulgate verse.** The Introit antiphon (a
  cento of Jer 29:11-12, 14 with words left out), the Gradual (*Liberásti … et
  eos, qui nos odérunt, confudísti … in sǽcula*), the Alleluia and Offertory
  (*oratiónem meam* for *vocem meam*) and the Communion (*Amen dico vobis,
  quidquid … et fiet vobis* for *Propterea dico vobis, omnia quaecumque … et
  evenient vobis*). The Douay renders the Vulgate verse and so cannot give
  these words without composing; for these chants alone Lasance's English is
  given, attributed, with this reason stated, and the Douay source verse is set
  beside it (Jer 29:11-12, 14; Ps 43:8-9; Ps 129:1-2; Mk 11:24, all in
  propers/verified.md, *Douay-Rheims (Challoner)*).
- **Orations.** Lasance, cited by formulary (*Twenty-fourth and Last Sunday
  after Pentecost*).

Nothing is composed.

## 3. Search method

- `tools/tpt commentary-work-index formulary --calendar roman-1962 --mass
  last-sunday-after-pentecost` (2026-11-16): 40 loci compared on their
  elements, **0 listed, 0 structural**. The same query for `pentecost-23`,
  which shares the five chants, also lists 0. No liturgical commentator in
  `src/sources/commentary/formulary-loci.yaml` matches either Mass. Section 6
  records the commentators found outside the index.
- `tools/tpt commentary-work-index discover --max-results 0` for each distinct
  appointed passage, Psalms in Vulgate numbering (2026-11-16): Jer 29:11-14,
  10 works; Ps 84:2, 18; Col 1:9-14, 12; Ps 43:8-9, 15; Ps 129:1-2, 14; Mt
  24:15-35, 16; Mk 11:24, 11. *None registered* is an absence from the
  library's joins, not proof that no copy exists. Section 3.1 gives, for every
  work reported *held* or *held-in-container*, whether its held artifact reaches
  the passage and what was done there.
- Second searches beyond the index, made because the index lists no holding of
  the Gospel's parallels or of the Fathers' question-books: Gregory the Great,
  *Homiliae in Evangelia* I (on Lk 21:25-33, the Gospel's Lukan parallel), found
  by searching the held complete text for *ficulneam* and *Coelum et terra
  transibunt*; Augustine, *Quaestiones Evangeliorum* I.37-39 and 42 (on Mt 24:20,
  23-27, 32 and 28), found in the held Latin text by *aquilae* and the
  question list; Bede, *In Marci evangelium expositio* on Mk 13:14-31 (the
  Gospel's Marcan parallel), found in the held Latin text by *abominationem*,
  *ficu* and *Coelum et terra*.
- Liturgical commentators beyond the index: the tracked text layers of Rupert
  (PL 170), Durandus (1612 *tomus secundus*), Sicard (PL 213), Honorius
  (PL 172) and Guéranger's English vols. 11-12 and French vol. 11, and Schuster
  (*Sacramentary* vol. V English OCR), were searched by the Gospel's, Epistle's
  and Collect's key words (*abominatio*, *Non cessamus*, *Excita*,
  *abomination of desolation*) and by the headings for a twenty-fourth or last
  Sunday. Results in section 6. A literal miss over these OCRs supports no
  claim of absence beyond the words searched.
- Remote whole files fetched on 2026-11-16 and matched to their registered
  SHA-256 before reading: Pustet 1862 (102,880,787 bytes), Lasance 1945
  (75,268,976), PL 26 (63,426,233), PL 24 (67,109,688), and the restricted
  Corpus Thomisticum responses `ccl.html` (140,991, Aquinas on Colossians) and
  `cps41.html` (286,376, Aquinas on Pss 41-50). The 1962 facsimile fetched by
  the resolve-context stage was re-hashed and matched. Tracked artifacts read
  were re-hashed: the Augustine, Gregory, Aquinas (Venice), PL 107 and
  Clementine files against their recorded SHA-256 in full; the NPNF I.10 and
  I.13, PL 9, Bede, Sicard, Durandus, Rupert, Guéranger, Pustet-text and
  Lasance-text files by the first twelve to sixteen hex digits of the
  recomputed digest, which matched the hash in each artifact identifier.
  Pages relied on were read on rendered images where section 5 says so; text
  layers otherwise.

### 3.1 Every held work the index lists, passage by passage

"Reaches" means that a held artifact of the work, or of the container the
index names, actually carries the appointed passage. Works the index reports
as *none registered* are listed in section 10.

| Passage | Work (index title) | Held artifact reaches the passage? | Opened, and result |
| --- | --- | --- | --- |
| Mt 24:15-35 | Chrysostom, *Hom. in Mt.* (NPNF I.10; Greek PG 57 OCR held) | Yes, the English (NPNF I.10). The PG 57 OCR holds the first homilies, not 75-77 | Read: Hom. 75.2 on v. 15 (lines 41905-41923), 76 on vv. 16-31 (lines 42301-42640), 77.1 on vv. 32-35 (lines 42824-42930) |
| Mt 24:15-35 | Jerome, *In Matthaeum* IV (PL 26 container) | Yes | Read on page images, cols. 177-181 (PDF 96-98, 200-dpi column crops) |
| Mt 24:15-35 | Hilary, *In Matthaeum* (PL 9 container) | Yes | Read in the tracked OCR, cc. 25.2-26.4, lines 83380-83660 (cols. 1053-1058); no page image |
| Mt 24:15-35 | Aquinas, *Super Mt.* (Venice t. 3) | Yes | Read in the OCR, c. 24, lines 39330-39500 (vv. 15-21), 39849-39900 (vv. 23-28), 39985-40000 (v. 30) |
| Mt 24:15-35 | Rabanus, *In Matthaeum* (PL 107 container) | Held; the tracked OCR, badly damaged in the region of Mt 24, does not locate the passage by any lemma searched (*desolationis*, *abomin*, *fulgur*, *aquil*, *Porphyr*) | Not opened on page images: a compiler whose Matthew commentary transmits Jerome; Jerome was read at the passage on page images. A lead |
| Mt 24:15-35 | Origen, *Comm. in Mt.* | No: the held English (ANF 9) is the surviving Greek books, which end before Mt 24; the Latin *series*, which reaches Mt 24, is not held | — |
| Mt 24:15-35 | Cornelius a Lapide (1908 English vol. 3, Mt 22-28 and Mk) | Yes | Not opened: an ecclesiastical writer at a passage read in four Fathers and a Doctor; a lead |
| Mt 24:15-35 | Aquinas, *Catena aurea* (index joins four held Catenae by title) | The held *Catena in Matthaeum* (English) | Not opened: a catena is a lead to its sources, and its principal sources here (Chrysostom, Jerome, Hilary, Augustine) were read in their own texts |
| Mt 24:15-35 | Hugh of Saint-Cher | No: the held responses are his postilla on Pss 83, 94 and 117 | — |
| Mt 24:15-35 (parallel Lk 21:25-33; beyond index) | Gregory, *Hom. in Ev.* I | Yes, the held complete Latin text (Wikisource extraction) | Read: the homily whole, lines 12-20 |
| Mt 24:20, 23-28, 32 (beyond index) | Augustine, *Quaest. Ev.* I.37-39, 42 | Yes (tracked Latin) | Read: lines 42-44, 47 |
| Mk 13:14-31 (parallel; beyond index) | Bede, *In Marc.* IV | Yes (tracked Latin) | Read: lines 390-391, 400-401 |
| Col 1:9-14 | Chrysostom, *Hom. in Col.* 2 (NPNF I.13; held fragments `…2.col-1.9-12`, `…2.col-1.13-14`) | Yes | Read in the NPNF I.13 text, lines 23769-24002, the two admitted passages' whole extent |
| Col 1:9-14 | Aquinas, Pauline lectures (index joins by title) | The registered Corpus Thomisticum *Super Col.* (`…ccl-html-d055308f`) | Read: c. 1 l. 2 (end) and l. 3, [87848], in the fetched response |
| Col 1:9-14 | Theodoret, *Interpretatio* (PG 82 container) | Yes, in the remote PG 82 OCR | Not opened: an ecclesiastical writer at a passage read in a Father and a Doctor; a lead |
| Col 1:9-14 | Theophylact (PG 124 container; listed twice) | Yes, in the remote PG 124 OCR | Not opened; a lead, as Theodoret |
| Col 1:9-14 | Cornelius a Lapide | No: the held Pauline volumes are 1 Cor and 2 Cor-Gal | — |
| Col 1:9-14 | Hugh of Saint-Cher | No | — |
| Jer 29:11-14 | Jerome, *In Hieremiam* V (PL 24 container) | Yes | Read on page images, PDF p. 451, cols. 893-894 (200-dpi crops) |
| Jer 29:11-14 | Cornelius a Lapide; Hugh of Saint-Cher | No | — |
| Ps 84:2 | Augustine, *En. in Ps.* 84 | Yes (tracked Latin, part 9; NPNF I.8; PL 37 container) | Read in Latin: 84.1-5, part 9 lines 75-79 |
| Ps 84:2 | Cassiodorus (PL 70); Bellarmine; Theodoret (PG 80); Athanasius (PG 27) | Held as the index states | Not opened: Augustine was read at the verse and no reading turns on more; leads |
| Ps 84:2 | Aquinas, *Postilla super Psalmos* | No: the lectures end at Ps 54 | — |
| Ps 84:2 | Hugh of Saint-Cher; Cornelius a Lapide | No | — |
| Ps 43:8-9 | Augustine, *En. in Ps.* 43 | Yes (tracked Latin, part 5) | Read in Latin: 43.6-10, part 5 line 35 |
| Ps 43:8-9 | Aquinas, *Super Ps.* 43 (Corpus Thomisticum `cps41`) | Yes | Read: nn. 3-4 [87223-87224] |
| Ps 43:8-9 | Chrysostom, *Expositio in Ps.* (PG 55 OCR) | Yes, remote | Not opened in this stage; a lead |
| Ps 43:8-9 | Cassiodorus; Bellarmine; Theodoret; Ambrose (PL 14, restricted) | Held | Not opened; leads |
| Ps 43:8-9 | Hugh of Saint-Cher | No | — |
| Ps 129:1-2 | Hilary, *Tract. in Ps.* 129 (PL 9) | Yes | Read in the tracked OCR, 129.1-3, lines 57585-57626 (col. 718) |
| Ps 129:1-2 | Augustine, *En. in Ps.* 129 | Yes (NPNF I.8, abridged English; PL 37 container) | Read in English: 129.1-3, NPNF I.8 lines 62171-62240 (section 3, on v. 4, runs to line 62249, reread at source registration); the Latin was not read |
| Ps 129:1-2 | Chrysostom (PG 55); Cassiodorus; Bellarmine; Theodoret | Held | Not opened; leads |
| Ps 129:1-2 | Hugh of Saint-Cher | No | — |
| Mk 11:24 | Bede, *In Marc.* III | Yes (tracked Latin) | Read: on 11:22-25, lines 338-339 |
| Mk 11:24 | Augustine, *De consensu* (NPNF I.6) | Yes | Not opened: it harmonizes the narrative order of the fig-tree episode; no reading uses the order |
| Mk 11:24 | Aquinas, *Catena aurea in Marcum*; Cornelius a Lapide vol. 3 | Yes | Not opened: a catena, and an ecclesiastical writer at a verse read in Bede; leads |
| Mk 11:24 | Hugh of Saint-Cher | No | — |

## 4. Passage-by-passage reception matrix

Psalms in Vulgate numbering (Hebrew in parentheses). "Read" means the locus
and the surrounding argument were read in the named bytes; it does not mean
the whole work was examined.

| Passage and proper | Direct ancient exegesis checked | Medieval, Doctoral and later saintly reception checked | Corpora and languages searched | How a retained witness is used | Material negative results |
| --- | --- | --- | --- | --- | --- |
| Jer 29:11-12, 14 — Introit antiphon | Jerome, *In Hieremiam* V on 29:10-14, PL 24 cols. 893-894 (Latin, page image): read | Sicard, *Mitrale* VIII.23 and VIII.25, and Rupert XII.23 on the antiphon as a chant; Durandus VI.142 reproduces Sicard VIII.25 (section 6) | PL 24 scan; discover list; commentators' OCR | Direct exegesis: future things known to God alone; prayer commanded though God could fulfil without it (Mt 7:7); anagogy of return to *locum nostrum Ecclesiam* | Theodoret *In Ieremiam*, Rabanus, Albert, Aquinas, Lyra, Denis not registered; no Greek witness held at this chapter |
| Ps 84:2 (85:2) — Introit verse | Augustine, *En. in Ps.* 84.1-5 (Latin): read | — | Tracked Latin part 9 | Direct exegesis: the past tense prophesies what is certain with God; the captivity turned away is the captivity of sin (Rom 7:23-25), freed by remission | Athanasius, Cassiodorus, Bellarmine, Theodoret held and not opened |
| Col 1:9-14 — Epistle | Chrysostom, *Hom. in Col.* 2 on 1:9-14 (NPNF I.13): read | Aquinas, *Super Col.* c. 1 l. 3 (Corpus Thomisticum): read; Sicard VIII.24 and Durandus VI.141 (section 6) | NPNF I.13; Corpus Thomisticum; commentators' OCR | Direct exegesis: *ut impleamini* as gentle reproof; knowledge joined to conduct; *patience* to those without, *longsuffering* to one another; the double gift of making worthy and giving; *lot* as free gift; *translated*; prayer as *ascensus mentis*, not bending God | Theodoret, Theophylact held and not opened; Ambrosiaster, Lombard, Rabanus *In epistolas*, Lapide on Col not held |
| Ps 43:8-9 (44:8-9) — Gradual | Augustine, *En. in Ps.* 43.6-10 (Latin): read | Aquinas, *Super Ps.* 43 nn. 3-4: read; Sicard VIII.23 and VIII.25 and Rupert XII.23 on the Gradual; Durandus VI.142 copies Sicard (section 6) | Tracked Latin part 5; Corpus Thomisticum | Direct exegesis: the past tense *quia tam certum est quasi factum sit*; future tenses mixed in; deliverance *vel in praesenti … vel in futuro* (Aquinas) | Chrysostom PG 55, Ambrose, Cassiodorus, Bellarmine held and not opened |
| Ps 129:1-2 (130:1-2) — Alleluia and Offertory | Hilary, *Tract. in Ps.* 129.1-3 (PL 9 OCR): read; Augustine, *En. in Ps.* 129.1-3 (NPNF I.8 English): read | Sicard VIII.23 and VIII.25 and Rupert XII.23 on the Offertory; Durandus VI.142 copies Sicard (section 6) | PL 9 OCR; NPNF I.8 | Direct exegesis: the cry from the depth of human calamity and from the heart's secret; God hears by nature, faith asks to be heard (Hilary); this mortal life is our deep (Augustine) | Chrysostom PG 55, Cassiodorus, Bellarmine held and not opened |
| Mt 24:15-35 — Gospel | Chrysostom, *Hom. in Mt.* 75.2, 76, 77.1 (NPNF I.10): read; Jerome, *In Mt.* IV, cols. 177-181 (page images): read; Hilary, *In Mt.* 25.2-26.4 (PL 9 OCR): read; Augustine, *Quaest. Ev.* I.37-39, 42 (Latin): read | Aquinas, *Super Mt.* c. 24 (Venice OCR): read; Bede on the Marcan parallel (below); Durandus VI.141 and Fromage (section 6) | NPNF I.10; PL 26 scan; PL 9 OCR; Latin *Quaest. Ev.*; Venice t. 3 OCR | Direct exegesis of every part of the pericope: the abomination; the flight; the shortened days; false christs; lightning; body and eagles; signs; the sign of the Son of Man; the gathering; the fig tree; *generatio haec*; heaven and earth | Origen's Latin series not held; Rabanus not located in the OCR; Paschasius, Albert, Theophylact *in Mt.*, Lyra, Denis, Walafrid not registered |
| Lk 21:25-33 and Mk 13:14-31 — parallels of the Gospel (not appointed) | Gregory, *Hom. in Ev.* I (Latin): read; Bede, *In Marc.* IV on Mk 13:14-31 (Latin): read | — | Held Latin texts | Analogue: Gregory on the fig tree, the summer, and words that pass yet stand; Bede on Pella, the fig as the Synagogue restored, and the heaven that passes | Bede's comment on Mk 13:14 and on the fig tree's *sub exemplo arboris* is Jerome's, *In Mt.* IV cols. 177, 180, word for word (section 5) |
| Mk 11:24 — Communion | Bede, *In Marc.* III on 11:22-25 (Latin): read | Sicard VIII.23 and VIII.25 and Rupert XII.23 on the Communion, with different readings; Durandus VI.142 copies Sicard (section 6) | Bede Latin text | Direct exegesis: *notanda distinctio deprecantium*: faith working through love moves spiritual mountains; the imperfect surely obtain forgiveness if they forgive | Jerome *Tract. in Marc.* not registered |
| Collect *Excita … voluntates* | — (composed text) | Fromage, vol. 11 p. 503 (introductory note only) | Commentator texts searched by incipit; no exposition found | Studied as a composed text (section 7.6) | No commentary on the Collect located in Rupert, Sicard, Durandus, Honorius |
| Secret *Propitius esto* | — | Fromage, vol. 11 p. 513 (note only) | As above | Studied as a composed text | No commentary located |
| Postcommunion *Concede … vitiosum* | — | Fromage, vol. 11 p. 513 (note only) | As above | Studied as a composed text | No commentary located |

**Corpus status of the matrix's witnesses** (source registration, 16 November
2026; `research/source-dispositions.toml` holds one row per bound use). Every
witness in the matrix is bound in `research/source-bindings.toml`; none rests
on a bibliography entry. Catena fragments (L3) now stand for Augustine on the
Gospel, *Quaest. Ev.* I.37 (Mt 24:20), I.38 (24:23-27), I.39 (24:32) and I.42
(24:28), for Augustine on the Introit verse, *En. in Ps.* 84.3 and 84.4 (Ps
84:2) and 84.5 (Ps 84:3-4), for Augustine on the Gradual, *En. in Ps.* 43.8
and 43.9 (Ps 43:8, 9), all admitted in this stage, and for Chrysostom on the
Epistle, *Hom. in Col.* 2 (Col 1:9-12, 13-14), admitted earlier. Every other
commentary witness is an acquired, inspected holding (L2) with a deferred row
naming what admission still needs: Chrysostom on Mt 24 (no translator credit
on the CCEL edition, Greek not held); Jerome on Mt 24 (no page of PL 26 cols.
177-181 retained, no transcription); Hilary on Mt 24 and Ps 129 (uncorrected
OCR; no work record for the *In Matthaeum*); Aquinas on Mt 24 (OCR; his reports
of Jerome and Augustine inside the lecture), on Colossians and on Ps 43
(restricted Corpus Thomisticum witnesses only); Gregory on Lk 21 and Bede on Mk
11 and 13 (no passage records; Bede's Jerome to be bounded; the Bede work
record's locus grammar); Jerome on Jer 29 (pages retained, no transcription or
work record); Augustine on Ps 129 (abridged English only); and the four
liturgical commentators (OCR, no harvest alias groups).

## 5. Witness register

Standing is from `src/sources/inventories/author-standing-v1.toml`. "Role" is
this study's use. Every locus below was read by this stage in the bytes named.

| Witness | Standing | Work and locus | Bytes read | Role | What the witness says that the study may use |
| --- | --- | --- | --- | --- | --- |
| John Chrysostom | father | *Hom. in Mt.* 75.2 (on 24:15) | NPNF I.10 CCEL text, lines 41905-41923 | direct exegesis | By *abomination* he means *"the statue of him who then took the city"*, placed in the temple; *"in order that they might learn that these things will be while some of them are alive"*. |
| John Chrysostom | father | *Hom. in Mt.* 76.1-4 (on 24:16-31) | NPNF I.10, lines 42301-42640 | direct exegesis | Vv. 16-22 concern the Jews' calamity under Vespasian; the apostles *"were not to keep the Sabbath day, neither to be there"*; read Josephus; the elect are *"the believers that were shut up in the midst of them"*, for whose sake the war was shortened; *"If, saith He, the war of the Romans … had prevailed further, all the Jews had perished"*. V. 23: *"the word, 'then,' relates not to the connection in order of time"*: passing over *"all the intermediate time from the taking of Jerusalem unto the preludes of the consummation"*; the false christs and signs are Antichrist's (2 Thess 2:9); *Go not forth … enter not*. The lightning: his coming *"needs not a herald"* but shows itself everywhere at once; the eagles are *"the multitude of the angels, of the martyrs, of all the saints"*. Vv. 29-31: the sun *"darkened, not destroyed, but overcome by the light of His presence"*; the sign is *"the cross being brighter than the sun"*; the tribes mourn on seeing him whom they pierced; *"He puts the mournful things first, and then the good things, that in this way also He may comfort"*; *"no longer on the cross, but 'in the clouds of Heaven'"*; angels gather the risen; trumpets *"for arousing, for gladness"*; 76.4: *"Woe is me for that fearful day!"* … *"the time is short, and the labor small"*. |
| John Chrysostom | father | *Hom. in Mt.* 77.1 (on 24:32-36) | NPNF I.10, lines 42824-42930 | direct exegesis | The fig tree shows the interval is not great, and also *"a spiritual summer, and a calm … (after the present tempest) for the righteous; but to the sinners … winter after summer"*; it confirms the saying *"as assuredly thus to come to pass. For as this of the fig tree is of necessity, so that too"*, as with the grain of wheat (Jn 12:24; 1 Cor 15:36). *This generation*: *"not of the generation then living, but of that of the believers"* (Ps 23:6); *"over this generation shall nothing prevail"*. Heaven and earth: *"it were more easy for these firm, fixed, and immoveable bodies to be blotted out, than for ought of my words to fall to the ground"*; *"let him test His sayings, and when he hath found them true … from what is past, let him believe also the things to come"*; *"the church is of more honor than Heaven and earth"*. |
| Jerome | father | *Commentariorum in Matthaeum* IV on 24:15-36 | PL 26 (Paris 1845) scan, cols. 177-181, PDF pp. 96-98, page images (200-dpi column crops) | direct exegesis | V. 15: *"Quando ad intelligentiam provocamur, mysticum monstratur esse quod dictum est"*; Dan 9:27; 2 Thess 2:4; *"Potest autem simpliciter aut de Antichristo accipi, aut de imagine Caesaris, quam Pilatus posuit in templo; aut de Hadriani equestri statua"*; abomination = idol, *desolationis* because set in the desolate temple. V. 16: *"Abominatio desolationis intelligi potest, et omne dogma perversum"*: standing in the holy place, *"hoc est, in Ecclesia"*, we must flee from Judaea to the mountains, *"dimissa occidente littera et Judaica pravitate, appropinquare montibus aeternis"* (Ps 75:5), stay on the roof where the devil's fiery darts cannot reach, not go down *"de domo conversationis pristinae"*. He notes Porphyry's attack and Eusebius's reply. V. 19: woe to souls that have not brought their offspring to the perfect man; or literally in Antichrist's persecution or the Roman captivity. V. 20: if of the captivity of Jerusalem under Titus and Vespasian, they pray against winter's cold and the sabbath law; *"Si autem de consummatione mundi intelligitur, hoc praecipit, ut non refrigescat fides nostra et in Christum charitas, neque ut otiosi in opere Dei torpeamus virtutum sabbato."* V. 22: the days shortened *"non mensura, sed numero"*, *"ne temporum mora, fides concutiatur credentium"*. V. 23: of false messiahs in the Roman siege, *"Sed melius de consummatione mundi intelligitur"*. V. 24: the place *"Tripliciter … disserendus"*: the Roman siege, the consummation, or heretics' war on the Church. Vv. 25-26: the desert of philosophers' dogma and the chambers of heretics. V. 27: Christ's faith shines in the Catholic churches from East to West; the second coming *"non in humilitate ut prius, sed in gloria"*: *"Stultum est itaque eum in parvo loco vel abscondito quaerere, qui totius mundi lumen sit."* V. 28: eagles sense a carcass across seas; *"quanto magis nos … debet festinare ad eum, cujus fulgur exit ab Oriente"*; *"Possumus autem corpus, id est, πτῶμα, quod significantius Latine dicitur cadaver, ab eo quod per mortem cadat, passionem Christi intelligere, ad quam provocamur; ut ubicumque in Scripturis legitur, congregemur, et per illam venire possimus ad Verbum Dei"* (Ps 21:17; Is 53:7); *"Aquilae autem appellantur sancti, quibus innovata est juventus ut aquilae"* (Ps 102:5), who take wings (Is 40:31) *"ut ad Christi veniant passionem"*. V. 29: not a diminution of light but *"quod ad comparationem verae lucis omnia visui tenebrosa sint"*; the powers are the multitudes of angels. V. 30: the sign *"aut crucis … ut videant … Judaei quem compunxerunt; aut vexillum victoriae triumphantis"*; those mourn *"qui municipatum non habuere in coelis, sed scripti sunt in terra"*. V. 31: the trumpet of 1 Cor 15 and 1 Thess 4. Vv. 32-33: *"Sub exemplo arboris, docuit consummationis adventum"*: when you see these things, *"nolite putare jam adesse consummationem mundi, sed quasi prooemia et praecursores quosdam venire"*. V. 34: *generatio* is *"aut omne genus hominum … aut specialiter Judaeorum"*. V. 35: *"Coelum et terra transibunt immutatione, non abolitione sui"* (col. 181). V. 36: against Arius and Eunomius, the Son is not ignorant of the day. |
| Hilary of Poitiers | father | *Commentarius in Matthaeum* 25.2-26.4 (on 24:4-36) | PL 9 tracked OCR, lines 83380-83660 (cols. 1053-1058); no page image | direct exegesis | 25.2: the gospel preached, then Jerusalem's end: *"fame, bello, captivitate consumpta est"*. 25.3: *"Antichristus cur abominatio desolationis"*: of Antichrist's times; abomination because he claims God's honour, of desolation because he will lay waste the earth with wars; received by the Jews, he will stand in the place of sanctification. 25.4: Judaea is to be left lest contagion of believing Antichrist reach the faithful. 25.5: the housetop precept *"secundum humanam intelligentiam rationem dicti factique non recipit"*: the roof is the house's summit and perfection; he who stands *"in corporis sui perfectione … regeneratione novus, spiritu celsus"* must not go down *"in humiliora rerum saecularium cupiditate"*; the man in the field must not go back to old cares nor take again the tunic of former sins. 25.6: *"absit … ut quidquam sit, quod homini nisi sua culpa malum fiat"*: the pregnant are souls heavy with sins, the nursing souls still fed on milk who *"nec peccata effugerint, nec cibum veri panis acceperint"*. 25.7: pray that flight be not in winter or sabbath, *"ne aut in peccatorum frigore, aut in otio bonorum operum reperiamur"*. 25.8: *"Sanctos de volatu spiritalis corporis aquilas nuncupavit: quorum, congregantibus angelis, conventum futurum in loco passionis ostendit. Et digne illic claritatis adventus exspectabitur, ubi nobis gloriam aeternitatis passione corporeae humilitatis operatus est."* 26.1: the signs show *"gloriam adventus sui et claritatis reditum"*; *"Sic erit de grano sinapis arbor ingens … sic ex humilitate mortis Dei gloria"*; *"scire nos voluit tempus nostrae redemptionis, quo ex corruptione corporum in honorem spiritalis substantiae transferemur"*. 26.2: the fig's branch *"antichristus esse intelligitur"*, whose leafing is the green of exulting sins, summer the heat of eternal fire. 26.3: heaven and earth, *"de nihilo"*, *"habeant id in se necessitatis ut non sint"*; his words, *"ex aeternitate deducta, id in se contineant virtutis ut maneant"*. 26.4: the day is hidden *"ut … incerti tamen metu semper nos sollicitos detineret"*. |
| Augustine | father | *Quaestiones Evangeliorum* I.37-39, 42 (on Mt 24:20, 23-27, 32, 28) | Latin text (Migne via Corpus Corporum/Wikisource, tracked), lines 42-44, 47 | direct exegesis | I.37: winter or sabbath, *"ne impedimento aliquo detineamini"*; *"Vel aliud, ne in tristitia aut laetitia rerum temporalium quis inveniatur a die illa."* I.38: east and west *"totum orbem"*, the Church spread through the world; *"Convenienter enim Ecclesiam nunc fulgur nominavit"*; *here* and *there* are schisms holding a part of the earth; *desert* and *chambers* the hidden conventicles of heretics. I.39: *"arborem fici genus humanum intellige"*; the tender branch is when the sons of men *"per fidem Christi ad spirituales fructus profecerint"*. I.42: *"Ubi fuerit corpus, illo congregabuntur aquilae; id est in coelum, quo hinc secum levavit corpus in homine suscepto: quod etiam cadaver ideo appellatum est, quia moriturus haec loquebatur. Illo congregabuntur aquilae, dictum est de spiritualibus, qui ejus passionem humilitatemque imitando, tanquam de ejus corpore saturantur."* |
| Augustine | father | *En. in Ps.* 84.1-5 (on Ps 84:2) | Latin text (Migne via Corpus Corporum/Wikisource, tracked part 9), lines 75-79 | direct exegesis | 84.3: the prophet *"utitur verbis quasi jam praeteriti temporis … quia apud Deum et quod futurum est, jam factum est"*, as in Ps 21:17-19. 84.4: *Avertisti captivitatem Jacob*: all who imitate Abraham's faith belong to Jacob; the captivity is Rom 7:23 (*"captivum me ducentem in lege peccati"*); it is said to Christ; *"non liberando nos a Barbaris … sed liberando nos ab operibus malis, a peccatis nostris, per quae nobis satanas dominabatur"*. 84.5: *"iniquitas tenebat captivum, remissa iniquitate liberaris. Confitere ergo te esse in captivitate, ut dignus sis liberari"*. |
| Augustine | father | *En. in Ps.* 43.6-10 (on Ps 43:8-9) | Latin text (Wikisource ed. Migne, tracked part 5), line 35 | direct exegesis | His lemma: *"Salvos enim fecisti nos ex affligentibus nos … et eos qui oderunt nos confudisti"*; 43.8: *"Et hoc figura praeteriti de futuro dicitur: sed ideo tanquam praeteritum dicitur, quia tam certum est quasi factum sit"*, as with Ps 21; *"Da prophetam cui tam certum sit futurum quam tibi praeteritum"*. 43.9: *"Videte quemadmodum miscet etiam verba futuri temporis"*: we shall be praised and confess *"Quia ex omnibus affligentibus nos eruisti nos, quia regnum perpetuum dabis nobis"*. 43.10: the present time of the persecuted Christians, *"Quare nos ista omnia medio tempore pati voluit?"* |
| Augustine | father | *En. in Ps.* 129.1-3 (on Ps 129:1-2) | NPNF I.8 CCEL text, lines 62171-62240 (section 3 ends at line 62249): abridged English (editorial ellipses); the Latin was not read | direct exegesis; quotations are of the condensed English | Jonah cried from the deep; *"this mortal life is our deep"*; *"they are very deep in the deep, who do not even cry from the deep"*; the sinner cries *"Because He who came to absolve from sins, gave hope even to the sinner down in the deep"*; *"there is propitiation with Thee"*: the innocent blood *"redeemed all captives from the hand of the enemy"*. |
| Hilary of Poitiers | father | *Tractatus in Ps.* 129.1-3 | PL 9 tracked OCR, lines 57585-57626 (col. 718) | direct exegesis | *"statue illum de profundo humanarum calamitatum aestu precantem"*; *"non labiis, sed secreto … cordis orare"* (Mt 6:6); the cry fits ignorance, suffering or prayer; God is everywhere and hears, *"sed orandus a nobis est"*: *"Naturae suae est ut audiat; sed fidei nostrae est ut precemur audiri"*. His lemma reads *vocem meam*. |
| Jerome | father | *In Hieremiam* V on 29:10-14 | PL 24 (Paris 1865) scan, cols. 893-894, PDF p. 451, page image (200-dpi crops) | direct exegesis | *"Se dicit nosse quid cogitet, illos autem cum suis prophetis … ignorare. Futurorum igitur scientia soli Deo competit"*; on *ut dem vobis finem et patientiam* (words the antiphon omits): *"finem captivitatis, et patientiam laborum praesentium, sive spem futurorum"*; *"Certe absque invocatione et oratione captivorum, poterat implere Dominus quod promiserat; sed hortatur eos ad preces, ut quod promissum est, mereantur accipere"*, with Mt 7:7; *"Secundum anagogen, tamdiu in saeculi hujus confusione versamur, quamdiu requiem septenarii numeri mereamur accipere, et accepta poenitentia, Deus impleat quod promisit, et reducamur ad locum nostrum Ecclesiam"*; col. 894: *"et invocabimus eum, et revertemur in Ecclesiam, et orabimus, et exaudiemur"*; others read the seventy years as Ps 89:10, *"nunc enim in umbra nos omnia et in imagine possidere"*. |
| John Chrysostom | father | *Hom. in Col.* 2 on 1:9-14 | NPNF I.13 CCEL text, lines 23769-24002 (the admitted passages `…2.col-1.9-12` and `…2.col-1.13-14`) | direct exegesis | *"that ye may be filled"* is a gentle hint they have not reached the end, *"not, 'that ye may receive,' for they had received"*; *"with faith he always couples conduct"*; *"he that knows without doing, is even in the way to punishment"*; *strengthened* refers to trials and persecutions; *"longsuffering towards one another, patience towards those without"*; giving thanks *"with joy"* is not from fear; *"He hath not only given, but also made us strong to receive"*: the honour is twofold; *lot*: *"by his own achievements no one obtains the kingdom … the whole is of His free gift"* (Lk 17:10); *in light*: *"both the future and the present light"*. V. 13: *"The whole is of Him"*; *"power"* of darkness, *"for it had great power over us"*; *"delivered … showing our great misery"*; *translated* *"so that it is both of us and of Him"*; *"to the same honor with Him"*; *"had we not been forgiven our sins, we should not have been 'translated'"*. |
| Thomas Aquinas | doctor | *Super Col.* c. 1 l. 3 [87848] | Corpus Thomisticum response `ccl.html` (registered, restricted; fetched 2026-11-16, hash matched) | direct exegesis | Prayer's three conditions, timely, continual, manifold; *"Oratio est ascensus mentis in Deum. Postulatio est rerum petitio"*; we premise devotion *"non ut eum flectamus, sed ut nos erigamus in eum"*. Paul asks knowledge of truth, working of virtue and endurance of evils; *"Qui ergo peccat, non cognoscit voluntatem Dei"*; *"ad virtutem non sufficit scire vel velle, nisi immobiliter operetur"*; patience against the difficulty of adversities, *longanimitas* against the delay of the reward (Hab 2:3); *cum gaudio* against bearing them with sadness. *Qui dignos nos fecit* excludes merit before grace; the saints' portion is God himself (Ps 15:5); *sors* because not by our choice (Jn 15:16). *Potestas tenebrarum*: *"sive Daemonum, sive peccatorum"*, with Is 49:25 *captivitas a forti tollitur*; *transtulit*: *"ut essemus regnum Dei … Et hoc fit quando liberamur a peccato … Vel ad litteram, ut consequeremur vitam aeternam"*; redemption by Christ as man, remission as God. He reports the *Glossa*, Augustine and Gregory by name on *sapientia*, *intellectus* and *dilectio*. |
| Thomas Aquinas | doctor | *Super Psalmos* 43 nn. 3-4 [87223-87224] | Corpus Thomisticum response `cps41.html` (registered, restricted; fetched 2026-11-16, hash matched) | direct exegesis | *Salvasti … ex affligentibus nos*: *"vel in praesenti: quia etsi corporaliter nobis noceant, spiritualiter tamen nocere non possunt; vel in futuro"*; the saints are afflicted bodily, and spiritually *"quando peccant illi qui habitant apud eos"*; *tota die* is eternity; praise *"non est in seipsis, sed in Deo"*. |
| Thomas Aquinas | doctor | *Super Evangelium Matthaei* c. 24 on vv. 15-30 | Venice 1745 tomus 3 OCR, lines 39330-39500, 39849-39900, 39985-40000 (printed pp. 306-310) | supporting (literal sense; reports Jerome and Augustine) | Abomination: the Roman army, or idols: Pilate's eagle brought into the temple, which the Jews called an abomination, or Hadrian's idol; *qui legit intelligat* because Dan 9 speaks of Christ's passion; the believers withdrew to Agrippa's realm; housetop and field: all a man has he gives for his life; *"Orate … quia in talibus ad Deum solum est recurrendum"* (Hos 6:1). Vv. 23-26: *"Secundum Hieronymum, potest retorqueri ad tempus ante destructionem; sed melius est ut retorqueatur ad finem"*; or *"secundum Augustinum"*, true doctrine is everywhere and public. V. 28: the coming will be manifest; *cadaver* signifies the passion, *"quia tunc veniet Christus ostendens signa passionis"*; eagles are the saints (Is 40:31), *"Sic, ut dicit Hieronymus, ubicumque sit memoria Christi passionis, viri sancti debent congregari per jugem memoriam passionis ejus"* (Heb 10:32): his report of Jerome, in his own words. V. 30: the sign of victory, or of the cross, *"ad ostendendum quod tota ista gloria est per passionem ejus"*; *"signum crucis erit clarius quam sol"*. |
| Gregory the Great | father | *Homiliae in Evangelia* I (on Lk 21:25-33, the Gospel's Lukan parallel) | Held complete Latin text (Wikisource extraction), lines 12-20 | analogue (parallel of Mt 24:29-35) | 1: *"senescentem mundum quae mala sequantur denuntiat, ut nos ab ejus amore compescat"*; *"sequentium rerum certitudo est praeteritarum exhibitio"*. 2: the powers of heaven are the angelic orders who will exact *"quod nos modo invisibilis conditor aequanimiter portat"*; *"In potestate et majestate visuri sunt quem in humilitate positum audire noluerunt"*. 3: *levate capita*: *"exhilarate corda"*; *"Qui ergo Deum diligunt ex mundi fine gaudere atque hilarescere jubentur"*; *"Quid est vita mortalis, nisi via?"*; the fig: *"sicut ex fructu arborum vicina aestas cognoscitur, ita ex ruina mundi prope esse agnoscitur regnum Dei … fructus mundi ruina est. Ad hoc enim crescit, ut cadat"*; *"Bene autem regnum Dei aestati comparatur, quia tunc moeroris nostri nubila transeunt"*. 4: nothing more durable than heaven and earth, nothing passes faster than a word; *"sine mutabilitate manentes sententias exprimit meus sermo qui transit"*. 5: the world in its old age; *"Nolite ergo … diligere quem videtis diu stare non posse"* (1 Jn 2:15). |
| Bede | father | *In Marci evangelium expositio* IV on Mk 13:14-31 (the Gospel's Marcan parallel) | Latin text (Migne PL 92 via Wikisource, tracked), lines 390-391, 400-401 | analogue; transmitter of Jerome | **Whose words.** On Mk 13:14 (*"Quando autem ad intelligentiam provocamur … idolum positum sit"*) and on the fig tree (*"Sub exemplo arboris … prope sit et in januis"*) and *generatio* (*"aut omne hominum significat genus, aut specialiter Judaeorum"*), he gives Jerome's words (*In Mt.* IV, cols. 177, 180) without naming him; those are Jerome's and are cited as Jerome's. Not found in Jerome's chapter: the literal fulfilment, *"ut ecclesiastica narrat Historia"*, that the Christians of the province withdrew to Pella beyond the Jordan; the spiritual flight, when heresies and crimes reign among the consecrated, *"tanto altius virtutum culmen debemus ascendere"*; the roof as one who *"excedens animo carnalia … spiritualiter vivit"* and the house as the flesh (2 Cor 5:1); the fig as the Synagogue, sterile now, which will bear fruit when the fullness of the gentiles enters (Rom 11:25-26; Job 14:7-9); the heaven that passes as the airy heaven of the flood (2 Pet 3:5-7), heaven and earth passing *"per eam, quam nunc habent imaginem … attamen per essentiam sine fine subsistunt"* (1 Cor 7:31; Apoc 21:1; Ps 101:27). No source of these was searched beyond Jerome's chapter; nothing more is claimed for them. |
| Bede | father | *In Marci evangelium expositio* III on Mk 11:22-25 | Same text, lines 338-339 | direct exegesis | On v. 23 he answers pagans who say Christians never moved mountains: not all deeds are written, and a mountain could be moved if need required, as by the prayers of Gregory of Neocaesarea; the mountain is also the devil, cast out of hearts by preachers. On v. 25: *"Notanda distinctio deprecantium. Qui perfectam habet fidem, quae per dilectionem operatur, ille orando, vel etiam jubendo, potest montes transferre spiritales"*, as Paul with Elymas and the Pythoness; those not yet perfect *"postulent sibi peccata dimitti … et absque dubio impetrabunt quod petunt, si tamen in se peccantibus aliis primo ipsi dimittunt"*. |
| Sicard of Cremona | ecclesiastical-writer | *Mitrale* VIII.23, VIII.24, VIII.25 | PL 213 tracked OCR: VIII.23 lines 29951-29975 (left column); VIII.24 lines 29976-29996 (left column); VIII.25 lines 29998-30015 (left column) continued at lines 29951-29980 (right column). The two columns of each line belong to different chapters | liturgical commentary (VIII.23 and VIII.25 the chants; VIII.24 the Epistle) | Section 6. VIII.23 and VIII.25 read in iteration 1. |
| William Durandus | ecclesiastical-writer | *Rationale* VI.141-142 | 1612 Lyon *tomus secundus* OCR, lines 17445-17527 (printed pp. 412-414) | transmitter of Sicard (VI.141 of VIII.24, VI.142 of VIII.25); witness only to the reading of Mt 24 in some churches | Section 6. |
| Rupert of Deutz | ecclesiastical-writer | *De divinis officiis* XII.23 | PL 170 OCR, lines 23697-23776 (cols. 329-330) | liturgical commentary (chants only) | Section 6. |
| Prosper Guéranger (series), Lucien Fromage (continuator) | servant-of-god; ecclesiastical-writer | *The Liturgical Year*, English vol. 11, *The Twenty-fourth and Last Sunday after Pentecost*, pp. 501-514 | Tracked text layer, lines 29991-30758 (research cited lines 29991-30710, which end at the Secret; the chapter's Communion, the note on the Postcommunion and the Postcommunion follow to line 30758, reread at source registration) | liturgical commentary; context (English printing) | Section 6. The volume is the continuation; any words used are Fromage's and cited as the continuation's. |

Witnesses read for occurrence and chronology (not reception): the two dated
Ordo entries (section 1) and the chronology sources named in section 9.

## 6. Liturgical commentators

The `formulary` query lists none for this Mass or for `pentecost-23`. Five
commentators' loci were read outside the index (Sicard's VIII.23 and VIII.25
in iteration 1); each is identified by elements, never by Sunday number. Rupert, Durandus, Sicard and Fromage are
ecclesiastical writers: each may be cited for what he says of an element his
Mass shares with this one, and may support a reading; he does not carry one.

| Commentator, heading | Elements shared with this formulary | Elements that differ | What he says of the shared elements | Use |
| --- | --- | --- | --- | --- |
| Sicard of Cremona, *Mitrale* VIII.23, *Dominica vicesima tertia post Pentecosten* (PL 213 OCR lines 29951-29975, left column; read in iteration 1) | Introit *Dicit Dominus: Ego cogito cogitationes pacis … et reducam captivitatem vestram de cunctis locis*, Gradual *Liberasti*, Offertory *De profundis*, Communion *Amen dico vobis* | The tribute Gospel (*si liceat censum dari Caesari*, Mt 22:17); the Epistle he quotes, *Corpus humilitatis nostrae configurabit corpori claritatis suae* (Phil 3:21) | The people pressed to pay tribute to Caesar figures the time when Antichrist will bring all to his service; *"quoniam tunc temporis Israelis reliquiae salvabuntur"*, the Lord announces it in the Introit, *"qui respondent in graduali: Liberasti nos, et in offerenda: De profundis. Quos denuo Dominus in communione certificat de salute dicens: Amen dico vobis"*. | Witness to the four chants read as one dialogue of the Lord and Israel's saved remnant at the end, the Communion as the Lord's assurance; supporting only; never cited for a link between the chants and this formulary's Epistle or Gospel. |
| Sicard of Cremona, *Mitrale* VIII.24, *Dominica vicesima quarta post Pentecosten* (PL 213 OCR lines 29976-29996, left column) | Epistle Col 1:9 (*"Non cessamus pro vobis orantes"*) | Gospel of the ruler's daughter and the woman with the issue of blood (Mt 9:18-26); no proper chants | The ruler's daughter is the Synagogue, the woman the Church of the gentiles; when the fullness of the gentiles has entered, Israel will be saved; *"Quae ut impleantur orat in epistola Paulus"*. The Sunday *"proprium cantuale non habet officium, vel quia vexabitur Ecclesia persecutionibus Antichristi, et ideo sua continet organa; vel quia praecedens officium huic evangelio rectissime coaptatur; vel quia haec Dominica saepius abundat"*. | Witness to the Epistle read as Paul's prayer for Israel's final salvation; supporting only, and only for the Epistle; never cited for a link between the Epistle and this formulary's Gospel. His explanation of the borrowed chants concerns his own Sunday. |
| Sicard of Cremona, *Mitrale* VIII.25, *Dominica vicesima quinta post Pentecosten* (PL 213 OCR lines 29998-30015, left column, continued at lines 29951-29980, right column; read in iteration 1) | Introit (*Reducam captivitatem vestram de cunctis locis*), Gradual *Liberasti*, Offertory *De profundis*, Communion *Amen dico vobis* | Lesson Jer 23 (*Ecce dies veniunt*, vv. 5-8); Gospel of the five loaves (Jn 6) | *"Huic quoque lectioni praecedens cantuale concordat officium"*: the lesson's return *de cunctis terris* answers the Introit's *de cunctis locis*; *"Soluti ergo illi, qui nunc tenentur captivitate, in graduali: Liberasti, gratiarum referunt actionem, et in offerenda: De profundis, ad hoc porrigunt orationem; qui suae petitionis, in communione: Amen dico vobis, recipiunt certificationem"*. Then: *"in hac ultima Dominica caeteras concludente recte ponitur officium, quod ad utramque Domini pertinere possit adventum"*, Jer 23:5 (*Ecce dies veniunt*) being the first coming and 23:6 (*In diebus illis salvabitur Juda*) the second; the five loaves, given after five thousand years; five Sundays to Christmas. | Witness to the chants read as the freed remnant's thanksgiving, supplication and assurance, and to the last Sunday's office as belonging to both comings; supporting only; his Mass's lesson and Gospel are not this formulary's. **Whose words.** His Gradual clause rewords Rupert XII.23 (*"Soluti ergo illi, qui nunc tenentur, captivitate animarum, clamabunt alta devotione gratiarum actionem, quam sequens innuit graduale"*); the Offertory as prayer and the Communion as the assurance (*certificatio*) of their petition are his, and differ from Rupert's Joseph (below). Durandus VI.142 reproduces this chapter. |
| William Durandus, *Rationale* VI.141, *De Dominica vigesimaquarta post Pentecosten* (1612 OCR lines 17445-17478, printed pp. 412-413) | Epistle Col 1:9 (*"Non cessamus … orantes pro vobis"*); the Gospel *Cum videritis abominationem* (Mt 24), which he says *"In quibusdam tamen ecclesiis dicitur hac die"* | His principal Gospel is Mt 9:18 (*"incipit in quibusdam Ecclesiis"*); no proper chants | Allegory of the ruler (Moses, prophets, apostles, prelates) praying for the Synagogue, *"sicut etiam orat Apostolus in epistola huius dominicae"*. His account of why the Sunday lacks proper chants repeats Sicard's word for word (Antichrist's persecution, *sua continet organa*; the preceding office fits the Gospel; the Sunday often superabounds). | Durandus attests that some churches read this Gospel on that Sunday in his day; that is all he supplies on the Gospel. The explanation of the chants is Sicard's, transmitted, and is cited as Sicard's. Supporting only. |
| William Durandus, *Rationale* VI.142, *De xxv dominica post Pente.* (same OCR, lines 17482-17527, printed pp. 413-414) | Introit *Dicit Dominus … reducam captivitatem vestram de cunctis locis*, Gradual *Liberasti*, Offertory *De profundis*, Communion *Amen dico* | Lesson Jer 23 (*Ecce dies veniunt*) in some churches; Gospel of the five loaves, which he calls the refreshment Joseph gave his brothers | The chants agree with the lesson's return *de cunctis terris*: the freed give thanks in *Liberasti*, still pray in *De profundis*, receive *sanctificationem* in the Communion; the last Sunday's office for both comings; five Sundays to Christmas. | **Whose words.** All of this reproduces Sicard VIII.25 almost word for word (*"Soluti ergo illi, qui nunc tenentur in captivitate"*; *recipiunt sanctificationem* for Sicard's *certificationem*), as VI.141 repeats VIII.24; it is cited as Sicard's, never as Durandus's or Rupert's. His Gospel clause on Joseph's refreshment of his brothers is not in VIII.25; it is the figure Rupert XII.23 gives, and Durandus's immediate source for it is not established. Supporting only. |
| Rupert of Deutz, *De divinis officiis* XII.23, *De Dominica vicesima tertia post Pentecosten* (PL 170 OCR lines 23697-23776, cols. 329-330) | Introit *Dicit Dominus*, Gradual *Liberasti*, Offertory *De profundis*, Communion *Amen dico vobis, quidquid* | Lesson Jer 23:5-8 and Gospel of the five loaves (Jn 6); no Epistle of Paul, Collect, Alleluia, Secret or Postcommunion named; his book has no chapter for a twenty-fourth Sunday (XII.24 is on the summer night lessons) | In the year's last office the Church gives thanks for the future salvation of Israel's remnant; the Introit's *cogitationes pacis* promise the banquet of grace with his brethren according to the flesh, prefigured in Joseph; freed *"captivitate animarum"*, they give thanks in the Gradual; in the Offertory they say to the true Joseph *Obsecramus ut obliviscaris sceleris fratrum* (Gen 50:17); the Communion is Joseph's answer (Gen 50:19-21). | Witness to the four chants read as one sequence; supporting only; never cited for a link between the chants and this formulary's Epistle or Gospel. **What is his.** The Gradual's thanksgiving of the remnant freed from the captivity of souls, in his own sentence (which Sicard VIII.25 later rewords); the Offertory as the brothers' plea to Joseph (Gen 50:17) and the Communion as Joseph's answer (Gen 50:19-21). Sicard's reading of the Communion as the assurance given to their petition is not Rupert's and is never put in his mouth. |
| Lucien Fromage, *The Liturgical Year*, English vol. 11, *The Twenty-fourth and Last Sunday after Pentecost*, pp. 501-514 (tracked text layer lines 29991-30758) | All ten elements, the chants as the Twenty-third Sunday's | — | P. 501-503: the Mass of the twenty-third Sunday *"was regarded, by our fore-fathers, as really the last of the Cycle"* (citing Rupert); *"It is only since a few centuries that … she closes the Cycle with the prophetic description of the dread Coming"*, St Matthew's after St Luke's in Advent. P. 504-506: the Epistle is *"Thanksgiving, and Prayer"*; *"The just man cannot possibly remain stationary … he must either descend or ascend"* (Ps 83:6). P. 509-512: a prayer on the coming: the elect *"whose youth, like that of the eagle, has been so often renewed by their receiving thy precious Blood"*, flying to *"the sacred prey of thy divine Body"*; the trumpet as summons *"to the Pasch … for all, and for ever"*. P. 513: the Secret asks God *"at the approach of the Last Judgment"* to turn all hearts; the Postcommunion asks the Sacrament to cure *"whatsoever there may remain faulty in our souls, at this close of the Year"*. | A modern ecclesiastical writer's reception of the whole formulary; supporting only. His Eucharistic eagles are his own and may be cited as his. His statement about when the Gospel came to this Sunday was not verified in this stage and is not to be asserted by any study; Durandus (above) shows the Gospel already read on this Sunday in some churches. |

Searched with no exposition found: *abominatio* and *Non cessamus* in Rupert's
*De divinis officiis* (the one hit for *abominatio desolationis*, line 43958,
is in another work of the volume on Dan 9, not on this Gospel or Sunday);
*Excita* and the other orations' incipits in Rupert, Sicard, Durandus and
Honorius; the Gospel and the headings for a twenty-fourth or last Sunday in
Honorius's *Gemma animae* (PL 172 OCR), in Schuster's *Sacramentary* vol. V
English OCR, and in Guéranger's English vol. 12. The French vol. 11
(*Le Temps après la Pentecôte* II) carries the same chapter (lines 34760,
36012) and was not read beyond its heading.

## 7. The consequential textual difficulties

The test of the three-document profile: the appointed words that raise the
question, what each principal witness infers, and what changes if the answer
is accepted.

### 7.1 Gospel: *Cum vidéritis abominatiónem desolatiónis … tunc qui in Iudǽa sunt, fúgiant ad montes* (24:15-20)

**The words.** A sign named from Daniel, then commands to flee from Judaea,
not to come down from the roof or turn back from the field, with woe to the
pregnant and nursing and prayer against winter or sabbath. Read on the last
Sunday of the year by people who will never be in Judaea, the commands raise
the question: to whom, and about what, is this said?

**The witnesses.**
- **Chrysostom** (*Hom.* 75.2, 76.1-2): of the Roman war; the abomination is the
  conqueror's statue in the temple; the discourse is *"addressed to the Jews"*,
  since the apostles would not keep the sabbath nor be there; the elect are the
  believers shut up in the city; the commands are literal. Only at v. 23 does
  *then* leap to the consummation.
- **Hilary** (25.3-7): of Antichrist; and the housetop precept *"secundum
  humanam intelligentiam rationem … non recipit"*: a man on the roof cannot
  leave without coming down. So the words are read of the person: the roof is
  the perfection of the regenerated, who must not descend to the cupidity of
  worldly things; the field-worker must not take back the tunic of old sins;
  the pregnant are souls heavy with sin; winter and sabbath are *"in peccatorum
  frigore, aut in otio bonorum operum"*.
- **Jerome** (cols. 177-178): first the literal options (Antichrist, Caesar's
  image set up by Pilate, Hadrian's statue; the siege under Titus and
  Vespasian), then *"et omne dogma perversum"* standing in the Church: flee to
  the eternal mountains, leaving the killing letter; stay on the roof beyond the
  devil's darts; do not go down to the house of former conversation; if of the
  consummation, *"ut non refrigescat fides nostra et in Christum charitas, neque
  ut otiosi in opere Dei torpeamus virtutum sabbato"*.
- **Augustine** (*Quaest. Ev.* I.37): winter and sabbath are any impediment; or
  *"ne in tristitia aut laetitia rerum temporalium quis inveniatur a die illa"*.
- **Aquinas** and **Bede** take the literal sense of the Roman war (Aquinas:
  Pilate's eagle, Hadrian's idol, Agrippa's mountains; Bede: Pella) and Bede a
  spiritual one like Jerome's.

**What changes.** Chrysostom's answer makes vv. 15-22 history fulfilled in
A.D. 70 (a date this record does not supply; section 9), and their use on this
Sunday a proof from fulfilled prophecy (77.1: *"from what is past, let him
believe also the things to come"*). Hilary's and Jerome's make the commands a
present rule of life for whoever hears them: not to go back down to what one
has left. The disagreement is real and survives: Chrysostom insists on the
historical referent where Hilary says the literal precept is unreasonable.
Reading 2 is built on Hilary and Jerome and keeps Chrysostom's literal sense
beside it.

### 7.2 Gospel: *Ubicúmque fúerit corpus, illic congregabúntur et áquilæ* (24:28)

**The words.** A proverb of carrion birds and a carcass, between the lightning
of the coming (v. 27) and the cosmic signs (v. 29). What is the body, and who
are the eagles?

**The witnesses.**
- **Jerome**: *corpus* is πτῶμα, *cadaver*, *"ab eo quod per mortem cadat"*: the
  passion of Christ, to which we are summoned, so that *"ubicumque in Scripturis
  legitur, congregemur"*; the eagles are the saints renewed like the eagle (Ps
  102:5), who take wings *"ut ad Christi veniant passionem"*.
- **Hilary** (25.8): the eagles are the saints, named from the flight of the
  spiritual body; the angels gather them *"in loco passionis"*; *"digne illic
  claritatis adventus exspectabitur, ubi nobis gloriam aeternitatis passione
  corporeae humilitatis operatus est"*.
- **Augustine** (*Quaest. Ev.* I.42): the body is the risen body he took up to
  heaven, called *cadaver* because he spoke as one about to die; the eagles are
  the spiritual who, imitating his passion and humility, *"tanquam de ejus
  corpore saturantur"*.
- **Chrysostom** (76.3): the eagles are *"the multitude of the angels, of the
  martyrs, of all the saints"*; the place is wherever he appears.
- **Aquinas** (c. 24): Christ will come showing the signs of the passion; he
  reports Jerome: wherever the memory of the passion is, the saints gather.
- **Fromage** (ecclesiastical writer): the eagles fly to *"the sacred prey of
  thy divine Body"*, their youth renewed *"by their receiving thy precious
  Blood"*.

**What changes.** All the Fathers read the body as Christ's and the eagles as
the saints (Chrysostom adds the angels); they differ on where the gathering
is: in the passion as read and remembered (Jerome), at the place of the
passion where the glory will return (Hilary), in heaven where the risen body
is (Augustine). Accepted, the verse makes the end a gathering to the crucified
and risen Christ rather than a scattering. No Father here names the Eucharist;
Augustine's *saturantur* and Jerome's *congregemur* are the nearest words, and
the Eucharistic reading is Fromage's and the editor's. Reading 1 is built on
this.

### 7.3 Gospel: *non præteríbit generátio hæc, donec ómnia hæc fiant* (24:34-35)

**The words.** The Lord says this generation will not pass until all these
things happen, then that heaven and earth will pass and his words will not.
Taken of the generation then living, the saying seems to promise the end
within their lifetime.

**The witnesses.**
- **Chrysostom** (77.1): *all these things* include Jerusalem's fall and
  everything until the coming; *this generation* is *"that of the believers"*,
  which nothing will overcome; heaven and earth are named to show his power and
  that *"the church is of more honor than Heaven and earth"*.
- **Jerome** (col. 180): *generatio* is *"aut omne genus hominum … aut
  specialiter Judaeorum"*; heaven and earth pass *"immutatione, non abolitione
  sui"*. Bede repeats the first and expands the second (section 5).
- **Hilary** (26.3): *generationem nostram* cannot pass until all runs its
  course; heaven and earth, made from nothing, carry in themselves the
  necessity of not being; his words, from eternity, the power to remain.
- **Gregory** (*Hom.* 1.4, on the Lukan parallel): nothing in nature is more
  durable than heaven and earth and nothing passes faster than a word; his
  word, which passes, utters sentences that remain without change.

**What changes.** None of the witnesses reads the saying as a date. Chrysostom
and Jerome make *generation* a kind or a lineage that lasts (the faithful, the
human race, the Jews); Hilary and Gregory make the contrast between heaven and
earth and the word the guarantee. Reading 3 is built on this: the certainty of
the promise rests on the speaker, not on a calendar.

### 7.4 The tenses: *avertísti*, *Liberásti*, *erípuit … tránstulit*, against *redúcam*, *accipiétis*

**The words.** The Introit verse (*avertísti captivitátem*), the Gradual
(*Liberásti nos … confudísti*) and the Epistle (*erípuit … et tránstulit*) speak
of deliverance as done; the Introit antiphon (*invocábitis … exáudiam …
redúcam*), the Gradual's verse (*laudábimur … confitébimur*), the Gospel and the
Communion (*accipiétis … fiet*) speak in futures.

**The witnesses.** **Augustine** on Ps 84:2: the prophet uses past tenses
*"quia apud Deum et quod futurum est, jam factum est"*; on Ps 43:8: *"tanquam
praeteritum dicitur, quia tam certum est quasi factum sit"*, and the psalm
*"miscet etiam verba futuri temporis"*. **Aquinas** on Ps 43:8: *vel in
praesenti … vel in futuro*; on Col 1:13: translated *"quando liberamur a
peccato … Vel ad litteram, ut consequeremur vitam aeternam"*. **Chrysostom** on
Col 1:12: Paul names the things already given *"for these are the causes of
the other"*, and *"that which hath already come to pass gains belief"*.
**Gregory**: *"sequentium rerum certitudo est praeteritarum exhibitio"*.

**What changes.** The witnesses agree that the past tenses state something
already given (deliverance from sin, a translation already begun) and
something certain though unseen; they differ in weight: Augustine on the
certainty of what God has decided, Chrysostom and Gregory on the evidence of
what has already happened, Aquinas on the two times. Readings 1 and 3 use this
differently (section 8.4).

### 7.5 Communion: *quidquid orántes pétitis, crédite quia accipiétis, et fiet vobis*

**The words.** An unlimited promise to prayer, with the one condition of
believing that it is received.

**The witnesses.** **Bede** (Mk 11:25): *"Notanda distinctio deprecantium"*:
the perfect, whose faith works through love, move spiritual mountains; those
not yet perfect surely obtain the forgiveness they ask, if they forgive.
**Hilary** (Ps 129): *"Naturae suae est ut audiat; sed fidei nostrae est ut
precemur audiri."* **Jerome** (Jer 29:12): God could fulfil without the
captives' prayer, *"sed hortatur eos ad preces, ut quod promissum est, mereantur
accipere"*. **Aquinas** (Col 1:9): prayer is the ascent of the mind, made
*"non ut eum flectamus, sed ut nos erigamus in eum"*.

**What changes.** Each answer locates the promise's condition in the one who
prays and not in what is asked: love and forgiveness (Bede), faith's office
(Hilary), the merit of receiving what is promised (Jerome), the mind raised to
God (Aquinas). A study must not present the promise as unconditioned, and
must not credit Hilary, Jerome or Aquinas with commenting on Mk 11:24; the join
of their words to the Communion is the editor's.

### 7.6 The orations

No exposition of the three orations was located beyond Fromage's one-line
notes (sections 4, 6). They are read as composed texts:

- **Collect.** *Excita … tuórum fidélium voluntátes: ut, divíni óperis fructum
  propénsius exsequéntes; pietátis tuæ remédia maióra percípiant*: God is asked
  to stir up the wills of the faithful, so that, pursuing the fruit of the
  divine work more readily, they receive greater remedies of his kindness. Its
  *fructum* stands beside the Epistle's *in omni ópere bono fructificántes* and
  its *voluntátes* beside *agnitióne voluntátis Dei*: verbal relations observed
  by the editor. Chrysostom's *"with faith he always couples conduct"* and
  Aquinas's *"ad virtutem non sufficit scire vel velle, nisi immobiliter
  operetur"* are comments on Col 1:9-10, not on the Collect.
- **Secret.** *ómnium nostrum ad te corda convérte; ut, a terrénis
  cupiditátibus liberáti, ad cæléstia desidéria transeámus*: a petition that
  hearts be turned and pass over from earthly to heavenly desires. Hilary's
  roof (25.5, not to go down *"in humiliora rerum saecularium cupiditate"*) and
  Gregory's *"Nolite … diligere quem videtis diu stare non posse"* stand beside
  it only as the editor sets them.
- **Postcommunion.** *quidquid in nostra mente vitiósum est, ipsórum
  medicatiónis dono curétur*: healing of what is faulty in the mind by the
  sacraments received. Its *mente* and *vitiósum* stand beside Hilary's souls
  heavy with sin (25.6) and Augustine's captivity of sin (Ps 84) only as
  editorial synthesis.

## 8. Material disagreements and differences

### 8.1 The referent of vv. 15-22

Chrysostom: the Roman war, literally, addressed to the Jews; Hilary:
Antichrist, with the precepts read of the soul because the letter is
unreasonable; Jerome: several literal referents and a spiritual one, without
choosing; Aquinas and Bede: the Roman war literally, Bede adding the spiritual.
A real disagreement on method between Chrysostom and Hilary. Readings must not
smooth it.

### 8.2 The body and the gathering (v. 28)

Passion remembered and read (Jerome), place of the passion (Hilary), heaven
where the risen body is (Augustine), wherever he appears, with angels among the
eagles (Chrysostom). Complementary identifications with a real difference of
place; section 7.2.

### 8.3 *This generation* and the passing of heaven and earth (vv. 34-35)

The faithful (Chrysostom), the human race or the Jews (Jerome, Bede), *our
generation* (Hilary). Heaven and earth pass by change, not abolition (Jerome,
Bede), against Hilary's emphasis that, made from nothing, they carry the
necessity of not being; Gregory's contrast of durability and the passing word.
Differences of emphasis, not of doctrine.

### 8.4 The fig tree (vv. 32-33)

The signs as preludes, the end not yet (Jerome, Bede); the interval not great
and a spiritual summer for the just, winter for sinners, and a pledge of
certainty from nature's necessity (Chrysostom); the human race, whose tender
branch is progress in faith (Augustine); Antichrist, whose leafing is the green
of exulting sins (Hilary); the world's fruit is its ruin, the kingdom the
summer (Gregory); the Synagogue that will bear fruit (Bede). Here the
witnesses genuinely diverge, and Hilary's Antichrist-branch reverses the
others' signs of hope. A study using the fig must name which reading it takes.

### 8.5 The past tenses

Section 7.4: Augustine's certainty of the decreed future against Chrysostom's
and Gregory's evidence from the past; Aquinas's two times.

## 9. Chronology: the generated record inspected

`tools/tpt proper-chronology record --provider claude --document
liturgy/roman-rite/1962/propers/temporal/68-twenty-fourth-after-pentecost
--write` and `annotations … --presentation orientation-v3 --write` were run on
2026-11-16; they wrote `research/chronology.toml`,
`research/chronology-annotations.tex` and `research/chronology-table.tex`. In
iteration 1 they were run again after this stage added the Gospel's event to
the shared corpus (below), and `--check` reports both current. The
orientation rows, inspected against passage scope, subject and relation:

| Row | Passage | Generated context and date | Inspection |
| --- | --- | --- | --- |
| Gradual | Ps. 43:8-9 (Vg.; Heb. 44) | Composition: the Psalms of the Sons of Korah; c. 740-536 B.C. (Korahite collection estimate) | The Vulgate title (*In finem, filiis Core, ad intellectum*) is Korahite. Source read: Catholic Encyclopedia, "Psalms" (tracked article text `…newadvent-12533a-cb9d9a25-article-text`, line 176): *"these psalms seem to have been composed between the days of Isaias and the return from exile"*. A collection estimate, not an occasion. The separate historical-setting row reads *Occasion date unresolved*: it reports that the chronology corpus holds no occasion for this psalm. The held commentaries on Ps 43 (section 10) were not searched for a received historical occasion, so the row does not show that tradition names none. |
| Introit | Ps. 84:2 (Vg.; Heb. 85) | Same Korahite estimate | Augustine's Latin title reads *In finem, filiis Core, Psalmus* (part 9, line 76). As above: the occasion row reports the corpus's absence; the held commentaries on Ps 84 were not searched for an occasion. Augustine (84.4), the one commentator read here, reads *avertisti captivitatem Jacob* of the captivity of sin, not of a dated return. |
| Alleluia; Offertory | Ps. 129:1-2 (Vg.; Heb. 130) | Composition: David after his sin (proposed); c. 1048-1015 B.C. (traditional Jerusalem chronology) | The source is Haydock's note on Ps 129:1, printed p. 790, reporting Berthier: *"David might compose it after his sin"*; the passage record (`…psalm-129-possible-davidic-composition`, verified 2026-11-05 on the page image) was read; the page itself was not re-rendered here. The biblical title (*Canticum graduum*) is anonymous. The row labels the attribution *(proposed)* and the date as the regnal frame with its qualification; the corpus note says the frame *"does not assign this psalm a year"*. The concise table prints a regnal range beside a proposed occasion of an anonymous psalm; the record keeps the qualification. Flagged for review (section 11). |
| Introit | Jer. 29:11-12, 14 | Composition: letter to the exiles, Jerusalem to Babylon; after the deportation of c. 598-597 B.C. | From Jer 29:1-3 (Douay) and the Catholic Encyclopedia's "Jeremias". Correct scope: the letter is the setting of the antiphon's words. The record also carries a final-formation claim for the book. |
| Gospel | Matt. 24:15-35 | Narrated event: Jesus foretells Jerusalem's ruin and His coming; Mount Olivet by narrative continuity; A.D. 29 (derived; Maas's chronology). Composition: Matthew; Semitic original associated with Palestine; proposals span c. A.D. 38-68 | Iteration 0 found **no narrated event** here, a gap in the shared corpus. Iteration 1 supplied it (section 9.1): Maas (tracked article text `…newadvent-08377a-f81e2c23-article-text`, lines 131-134, compared with printed p. 381) closes the Tuesday of the last week, the day of the fig-tree instruction the Communion row already dates: *"Jesus ended this day by uttering the prophecies concerning the destruction of Jerusalem, His second coming, and the future judgement"*; Douay Mt 24:3 seats the discourse on Mount Olivet, spoken to the disciples privately. Inspected: the event row's subject is the speaking of the discourse; its scope (Mt 24:3-35) contains the whole appointed passage, so the row prints the passage's own reference with no split; the relation is `narrated-event`, the same relation and derivation as the Communion's fig-tree row (one harmony's chronology, derived from Maas's A.U.C. 782 = A.D. 29 calibration and labelled so); the place is qualified *by narrative continuity*, since only v. 3 names Olivet. The composition row is unchanged and kept apart. The prophecy's referents (A.D. 70; the coming and the judgement) are not dates of the passage: no prophetic-referent binding was made, and none reaches this page. |
| Communion | Mark 11:24 | Narrated event: Jesus teaches faith and prayer; Bethany to Jerusalem, before the Passion; A.D. 29 (derived; Maas's chronology). Composition: Mark; Rome traditionally; proposals span A.D. 38-70 | Maas, line 134: *"On Tuesday the wonder of the disciples at the sudden withering of the fig tree provokes their Master's instruction on the efficacy of faith"*. Correct scope; the event row and composition row are kept apart. |
| Epistle | Col. 1:9-14 | Composition: Colossians; Rome traditionally; addressed to Colossae; proposals span A.D. 61-63 | Catholic Encyclopedia, "Epistle to the Colossians" (`…newadvent-04131b-08367306-article-text`, line 3): *"some time between A.D. 61 and 63"*, in Paul's first Roman captivity; and the "St. Paul" table, 61. Writer's place (Rome) and recipients' (Colossae) are distinct in the row. |

The four Catholic Encyclopedia article texts quoted above are bound as context
(`research/source-bindings.toml` 40-43) and were reread at those lines by source
registration. The Haydock note and the "Jeremias" article (a remote delivery)
are cited by the chronology record, which seals them; neither was reread by
source registration, and neither is bound here.

The generated table imports each row once, groups the Gospel's event and
composition rows (`row-cd9d06ad7f8b3c92`, `row-52f2107c2407274c`) and the
Communion's (`row-abcb772de81468ec`, `row-f28db60616916496`), and notes *Vg.*
and *Heb.* once. The Gospel's former composition-only row
(`row-9348c0895cf392cb`) and its unresolved event row
(`row-1b1b32c8447e41df`) no longer exist. Psalm numbering agrees with
the Missal's printed citations (*Ps. 43*, *Ps. 84*, *Ps. 129*). No date reaches
the page from anywhere but this record.

### 9.1 The Gospel's event, added to the shared corpus (iteration 1)

Made under `guidance/scripture-chronology.md` (sections 5, 6, 14.1 and 15),
following the pattern of the Communion's fig-tree event and of the Mt 25:1-13
orientation context added by the Thirty-second Sunday research. Every change
is under `src/sources/` and is listed in the stage result for commit.

- **Source.** Maas's Holy Week paragraph was reread whole in the tracked
  article text (lines 131-134; SHA-256 recomputed and matched) and compared
  with printed p. 381, right column, in Internet Archive's page image of the
  scanned volume the registered facsimile reproduces (leaf n432; not
  hash-matched to the registered PDF). The printed sentence ends *"the future
  judgment; these predictions are interrupted by the parable of the ten
  virgins, and of the talents"*; the text differs only in spelling and that
  phrase. Registered as
  `passage.catholic-encyclopedia.volume-8.new-york-1910.maas-ninth-journey-olivet-prophecies`.
- **Event.** `life-of-christ.prophecies-on-mount-olivet`, *Jesus foretells the
  destruction of Jerusalem, His second coming and the judgement*; one
  `catholic-traditional-v1` claim, A.D. 29, `basis_class = "derived"`,
  derived exactly as the fig-tree instruction of the same day is (Maas's
  Ninth Journey, A.U.C. 782, with his express A.U.C. 782 = A.D. 29
  equivalence; input `chronology.maas-auc-782-ad-29-calibration`), with the
  orientation qualification *Maas's chronology*. "Tuesday" stays in the basis;
  Maas names no date of the month. The marriage-feast event's note had said
  that the prophecies of that evening need their own subject rather than a
  silent reuse; this is that subject.
- **Binding.** `narrated-event`, Mt 24:3-35. Verse 3 seats Jesus on Olivet; v.
  35 ends the prophecy with the passing of heaven and earth. Verses 1-2 (the
  prophecy spoken on leaving the Temple) are outside, since Olivet is not
  their place. Verses 24:36-25:46 continue the same discourse by Maas's account
  and Matthew 26:1; they are not bound here, because widening the binding
  changes other appointed passages' generated chronology (another production's
  Gospel acclamation from Mt 24:42, 44, and Mt 25:1-13), which is a separate
  reviewed act. The binding note says so.
- **Place and description.** A `settings` entry gives the event's place,
  *Mount Olivet by narrative continuity* (Douay Mt 24:3, 24:35); a `contexts`
  entry for Mt 24:3-35 gives the date-free description, worded as the Mt
  25:1-13 entry is, for any projection in which the event goes undated.
- **No referent dates.** The destruction of Jerusalem
  (`apostolic-age.destruction-of-jerusalem`) and the coming are what the
  discourse prophesies; the Fathers dispute which verses speak of which
  (section 8.1), and no `prophetic-referent` binding was made.
- **Regenerated and checked.** `tools/tpt scripture-chronology validate`,
  `build` (coverage: `Matt.24.3-35` now `dated`) and `check`;
  `scripts/build_profile_contract_manifest.py` (the corpus's cold-review
  manifest gains the new claim and binding; `--check` current); the leaf's
  record and annotations (`--check` current). The chronology tests that
  exercise these files pass except failures that fail identically on the
  committed corpus without this change (stage result).
- **Seal.** The chronology record cites the event's sources (the Maas article
  text, both Maas passage records, Douay Mt 24:3 and 26:1), and the
  computation opens `events.yaml`, `bindings.yaml` and `orientation.yaml`; the
  engine seals all of these. They are provider-neutral, not same-family
  evidence, and need no entry in `research/review-dependencies.toml`. The
  printed page compared is bound as context (`research/source-bindings.toml`,
  last binding).

## 10. Negative results and unresolved leads

- **Not registered** (discover's *none registered*), by passage. Mt 24:15-35:
  Nicholas of Lyra, Paschasius Radbertus, Albert the Great, Denis the
  Carthusian (two titles), Theophylact *in Mt.*, Walafrid (*Glossa*). Col
  1:9-14: Lyra, Peter Lombard, Denis (two), Rabanus *In epistolas*. Jer
  29:11-14: Lyra, Rabanus, Theodoret *In Ieremiam*, Albert, Denis (two), Aquinas
  *In Ieremiam*. Ps 84:2: Denis (two), Lombard, Jerome *Tractatus* and
  *Commentarioli*, Lyra, Albert, Bede (two entries), Walafrid. Ps 43:8-9: Lyra,
  Lombard, Denis (two), Albert, Jerome *Commentarioli*, Walafrid. Ps 129:1-2:
  Lyra, Lombard, Denis (two), Albert, Jerome *Commentarioli*, Walafrid. Mk
  11:24: Albert, Denis, Lyra, Theophylact *in Marc.*, Jerome *Tract. in Marc.*,
  Walafrid.
- **Held and not opened** (leads, section 3.1): Cornelius a Lapide (Mt 24,
  Mk 11); Rabanus *In Mt.* (Mt 24; OCR does not locate it); *Catena aurea in
  Mt.* and *in Mc.*; Theodoret and Theophylact on Colossians; Cassiodorus,
  Bellarmine, Theodoret, Athanasius on Ps 84; Chrysostom (PG 55), Ambrose,
  Cassiodorus, Bellarmine, Theodoret on Ps 43; Chrysostom (PG 55),
  Cassiodorus, Bellarmine, Theodoret on Ps 129. None of these was searched for
  a received historical occasion of Ps 43 or Ps 84 (for instance, a particular
  return read into *avertisti captivitatem Jacob*); the unresolved occasion
  rows (section 9) report the chronology corpus's absence, not a search of the
  tradition; Augustine, *De consensu*;
  Augustine, *De civitate Dei* XX (on Antichrist and the end; held, not
  searched in this stage); Schuster's *Sacramentary* on the chants.
- **Not held as text, or not reaching the passage**: Origen's Latin
  *Commentariorum series* on Mt 24; Aquinas on the Psalms beyond Ps 54; Hugh of
  Saint-Cher on any of these passages.
- **Chant forms**: no psalter, antiphonary or Old Latin witness searched for
  any chant form or the Epistle's *Dei* (section 2.3).
- **No Greek witness** was read on Mt 24 or Col 1 in Greek: the English NPNF
  translations of Chrysostom were read; his Greek on these homilies is not held
  in a reached artifact.
- **Fromage's history claim** (section 6) not verified.

## 11. Shared-record defects observed (reported, not repaired)

Iteration 0 changed no shared record except the two dated Ordo registrations
it was assigned (section 1). Iteration 1 changed the shared chronology corpus
and registered one Maas passage record, for the Gospel's event (section 9.1).

- **Chronology corpus, Mt 24.** Reported in iteration 0 (no event binding or
  orientation context covered Mt 24:15-35); **repaired in iteration 1** by this
  stage under the research assignment (section 9.1). Left for the corpus
  owner: whether to widen the binding over Mt 24:36-25:46, the rest of the same
  discourse, which would change other productions' generated chronology. Any
  other production whose appointed loci fall in Mt 24:3-35 must regenerate its
  chronology record and table against the changed corpus.
- **Chronology corpus, Ps 129.** The orientation date prints David's regnal
  range beside a *proposed* Davidic occasion for an anonymous psalm. The record
  keeps *(proposed)* and the qualification; whether a regnal range should print
  for a modal proposal is the corpus owner's judgement under
  `guidance/scripture-chronology.md` (owner: `src/sources/chronology/orientation.yaml`).
- **Latin ledger.** No row covers this formulary's five chants or two lessons
  (nos. 1769, 1771-1775, 1777), nor the same chants under `pentecost-23`.
  propers/verified.md is their page-image collation. Owner:
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml`.
- **Formulary loci.** `src/sources/commentary/formulary-loci.yaml` has no locus
  for Sicard VIII.23-25, Durandus VI.141-142, Rupert XII.23 or Fromage vol. 11
  pp. 501-514, though all are held and read here; `formulary` therefore lists
  no commentator for this Mass or `pentecost-23`.
- **Commentary index joins.** `discover` does not reach Gregory's *Hom. in
  Ev.* I (Lk 21 parallel), Augustine's *Quaest. Ev.* I.37-42 or Bede on Mk 13
  for this Gospel; they were found by literal search (section 3).
- **Precedence tool.** `tools/tpt calendar-rubrics day` depends on a generated
  browser-data product; it refused during the resolve-context stage while the
  product was being rebuilt and ran in this stage after it returned (section 1).

## 12. Evidence bounds

- The 1962 and 1862 Latin and the Lasance English were read on page images;
  the Fathers were read as section 5 states, many in uncorrected OCR (Hilary
  PL 9, Aquinas Venice t. 3, Sicard, Durandus, Rupert) or in transcriptions not
  collated with a page image (Augustine's Latin, Gregory, Bede), and Augustine
  on Ps 129 and Chrysostom on Matthew and Colossians in English translation
  only. A quotation from an OCR layer is the editor's reading of a damaged
  layer, normalised in spelling; a study quoting it should say so or prefer
  paraphrase.
- The NPNF I.8 Augustine on the Psalms is abridged; quotations from it are of
  the condensed English, not Augustine's continuous words.
- Nothing here establishes the history of this formulary's assembly; sections
  2.3 and 6 record only the facts that bound claims.
- The sweep is bounded by the library's holdings and the searches named; it is
  not a survey of all reception.

## 13. Handoff to source registration

Every source read or used, with its binding in `research/source-bindings.toml`;
receipts are in this run's scratch area (named in the stage result's notes).

- Bound and already registered: the 1962 facsimile; the 1962 orations passage;
  Pustet 1862 facsimile and text layer; Lasance facsimile and text layer; the
  Clementine and Douay verse texts and the psalm concordance; NPNF I.10
  (Chrysostom on Matthew); NPNF I.13 with the two admitted Chrysostom passages
  on Col 1:9-14; PL 26 PDF (Jerome on Mt); PL 9 OCR (Hilary on Mt and Ps 129);
  PL 24 PDF (Jerome on Jer); Augustine's *Quaest. Ev.* Latin, *En. in Ps.*
  Latin parts 5 and 9 and NPNF I.8; Gregory's *Hom. in Ev.* Latin; Bede's *In
  Marc.* Latin; Aquinas, *Super Col.* (`ccl.html`), *Super Ps.* (`cps41.html`)
  and *Super Mt.* (Venice t. 3 OCR); Sicard (PL 213 OCR), Durandus (1612 OCR),
  Rupert (PL 170 OCR); Guéranger/Fromage English vol. 11; the two dated Ordo
  passages registered in this stage.
- Commentary candidates for `research/source-dispositions.toml`: Jerome *In
  Mt.* IV on Mt 24:15-36; Hilary *In Mt.* 25.2-26.4 on Mt 24:4-36; Chrysostom
  *Hom. in Mt.* 75.2-77.1 on Mt 24:15-36; Augustine *Quaest. Ev.* I.37-39, 42 on
  Mt 24:20, 23-28, 32; Aquinas *Super Mt.* c. 24 on Mt 24:15-30; Gregory *Hom.
  in Ev.* I on Lk 21:25-33 (an analogue; its Scripture is Luke); Bede *In
  Marc.* IV on Mk 13:14-31 (analogue; much of it Jerome's) and III on Mk
  11:22-25; Chrysostom *Hom. in Col.* 2 (already admitted passages); Aquinas
  *Super Col.* c. 1 l. 3 on Col 1:9-14; Jerome *In Hier.* V on Jer 29:10-14;
  Augustine *En. in Ps.* 84.1-5 and 43.6-10 (Latin) and 129.1-3 (English);
  Aquinas *Super Ps.* 43 nn. 3-4; Hilary *Tract. in Ps.* 129.1-3; the
  liturgical commentators (Sicard VIII.24; Durandus VI.141-142; Rupert XII.23;
  Fromage vol. 11 pp. 501-514) as liturgical commentary.

### 13.1 Source registration (iteration 0), 16 November 2026

- **Receipts.** Every retrieval receipt named in the research result was
  re-hashed against its registered record and matched in SHA-256 and byte
  length: the 1962 facsimile (82,815,941 bytes), Pustet 1862 (102,880,787),
  Lasance 1945 (75,268,976), PL 26 (63,426,233), PL 24 (67,109,688), the
  restricted Corpus Thomisticum responses `ccl.html` (140,991) and `cps41.html`
  (286,376), and the two dated Ordo responses (165,243 and 110,049). Every
  tracked artifact bound here was re-hashed in full and matched. No inspection
  is claimed from a receipt: each row of `research/source-dispositions.toml`
  says who read the locus, and the tracked loci were reread in this stage.
- **Registrations.** The source library already held every work, edition and
  artifact research read; aliases and container holdings were checked through
  `discover` and the containment joins, and no duplicate identity was created.
  New records: nine verified passages of Augustine (below). The Augustinus.it
  chronology table (`artifact.augustinus-it.enarrationes-chronology.2026-10-23-web-state.whole-html-a2938c5d`)
  was reacquired whole, matched its registered SHA-256, and was read only to
  date those passages; it stays remote (unresolved redistribution basis).
- **Bindings.** The Bede binding's lines now stand in its context (the work
  record's locus grammar, `III.Mc.10.42-45`, admits no loci for them); the
  Sicard binding's range was corrected to the chapter's own left-column lines,
  29976-29996; and five context bindings were added (the four Catholic
  Encyclopedia article texts read for section 9, and the Augustinus.it table).
- **Admitted to the Catena** (passage record verified and canonical edge in
  `src/sources/commentary/fragment-loci.yaml`):
  `passage.augustine.quaestiones-euangeliorum.latin-migne-corpus-corporum-wikisource-web-2026-09-05.1-37`,
  `…1-38`, `…1-39`, `…1-42` (Mt 24:20; 24:23-27; 24:32; 24:28; dated by the
  work record, c. 399-400);
  `passage.augustine.enarrationes-in-psalmos.latin-migne-corpus-corporum-wikisource-web-2026-09-05.84-3`,
  `…84-4`, `…84-5` (Ps 84:2; 84:2; 84:3-4; composition date recorded as not
  established, Zarb's "post. 410" having no closing year);
  `passage.augustine.enarrationes-in-psalmos.2026-10-23-latin-migne-wikisource.43.8`,
  `…43.9` (Ps 43:8; 43:9; dated 412 from Zarb's Lent 412). The two existing
  Chrysostom passages on Col 1:9-12 and 1:13-14 are admitted rows as before.
- **Deferred** (key, missing criteria): `chrysostom-hom-mt-75-2-matt-24-15`,
  `chrysostom-hom-mt-76-matt-24-16-31` and `chrysostom-hom-mt-77-1-matt-24-32-36`
  (edition-translator-credit, passage-record, original-language-text,
  natural-excerpt-boundary); `jerome-in-mt-iv-matt-24-15-36` (retained-page-image,
  verified-transcription, passage-record, natural-excerpt-boundary);
  `hilary-in-mt-25-2-26-4-matt-24-4-36` (page-image-collation,
  retained-page-image, verified-transcription, work-record, passage-record,
  natural-excerpt-boundary); `hilary-tract-ps-129-1-3-ps-129-1-2`
  (page-image-collation, retained-page-image, verified-transcription,
  passage-record, natural-excerpt-boundary); `aquinas-super-mt-24-matt-24-15-30`
  (page-image-collation, passage-record, natural-excerpt-boundary,
  quoted-text-attribution); `gregory-hom-ev-1-luke-21-25-33` (passage-record,
  page-image-collation, natural-excerpt-boundary); `bede-in-marc-iii-mark-11-22-25`
  and `bede-in-marc-iv-mark-13-14-31` (passage-record, quoted-text-attribution,
  work-locus-grammar); `aquinas-super-col-1-l-3-col-1-9-14`
  (publishable-controller, passage-record, quoted-text-attribution);
  `jerome-in-hier-v-jer-29-10-14` (verified-transcription, passage-record,
  work-record); `augustine-en-ps-43-6-7-10-context` (passage-record);
  `augustine-en-ps-129-1-3-npnf-ps-129-1-4` (unabridged-text,
  edition-translator-credit, original-language-text, passage-record);
  `aquinas-super-ps-43-3-4-ps-43-7-9` (publishable-controller, passage-record);
  and the liturgical commentators `sicard-mitrale-viii-24-col-1-9`,
  `durandus-rationale-vi-141-col-1-9`,
  `durandus-rationale-vi-142-dicit-dominus-chants`,
  `rupert-de-div-off-xii-23-dicit-dominus-chants` and
  `fromage-liturgical-year-xi-last-sunday` (page-image-collation,
  passage-record, harvest-alias-group, with natural-excerpt-boundary or
  quoted-text-attribution as each row states). No row is rejected.
- **Retention.** No new bytes were retained. The remote scans stay remote
  under their existing records (whole files of 63-103 MB, two of them of
  unresolved rights); page extracts would need a separately preserved offline
  pack, which this stage did not make. Jerome on Jer 29 is already retained as
  page extracts (PL 24 PDF 451-452); no page of PL 26 cols. 177-181 or of
  Pustet 1862 PDF 445-446 is retained.
- **Corrections to this record.** The Sicard and Fromage line ranges in
  sections 5 and 6 and the end of Augustine's section 3 on Ps 129 were
  corrected after rereading; the Fromage chapter runs to line 30758.

### 13.2 Research (iteration 1), 16 November 2026: for source registration

- **Sicard, *Mitrale* VIII.23 and VIII.25.** Read in the tracked PL 213 OCR
  (`artifact.sicard-of-cremona.mitrale.latin-migne-pl-213.ia-djvu-ocr-ea9fd813`,
  SHA-256 recomputed and matched) at the column extents in section 5. The
  Sicard binding now carries both chapters beside VIII.24, and
  `research/source-dispositions.toml` has a deferred row for each
  (`sicard-mitrale-viii-23-dicit-dominus-chants`,
  `sicard-mitrale-viii-25-dicit-dominus-chants`), liturgical commentary,
  supporting only, with the Scripture each cites. No passage record was made:
  the columns interleave chapters line by line, and the OCR is uncorrected.
- **Durandus VI.142 and Rupert XII.23.** Reread against Sicard. The Durandus
  binding's VI.142 extent is corrected to the whole chapter (lines
  17482-17527); its context and disposition row now attribute its words on
  the chants to Sicard VIII.25. The Rupert context and row now name what
  Rupert writes.
- **Maas.** The new passage record
  `passage.catholic-encyclopedia.volume-8.new-york-1910.maas-ninth-journey-olivet-prophecies`
  (tracked article text, lines 131-134) is cited by the chronology corpus and
  sealed through the chronology record; the Maas article-text binding's
  context was updated. Printed p. 381 was compared in Internet Archive's page
  image (`https://archive.org/download/catholicencyclop0008unse_u7y2/page/n432_w1600.jpg`,
  fetched 2026-11-16, 1,459,495 bytes, SHA-256 in the stage result); it is
  bound last, as context, to the segment
  `segment.catholic-encyclopedia.volume-8.new-york-1910.jesus-christ-a-j-maas`,
  without retained bytes and without a hash match to the registered PDF.
- **Digests.** `binding_sha256` for the changed bindings (34, 35, 36, 41) and
  the new one (45) were recomputed with `scripts/_proper_study.py
  binding-digests`; `proper-study source-dispositions --mode source` exits 0.


### 13.3 Source registration (iteration 2), 16 November 2026

- **Research's changes reread.** The tracked OCR of Sicard (PL 213), Durandus
  (1612) and Rupert (PL 170) and the Maas article text were re-hashed in full
  and matched their artifact records. Sicard VIII.23 (lines 29951-29975, left
  column) and VIII.25 (lines 29998-30015, left, continued at 29951-29980,
  right, to *mentio continetur*), Durandus VI.142 (lines 17482-17527) and
  Rupert's Gradual sentence (lines 23738-23740) were reread at those extents
  and agree with the bindings, rows and sections 4-6. The new Maas passage
  record agrees with lines 131-134 of the article text it names. The research
  receipt for Internet Archive leaf n432 was re-hashed and matched the
  SHA-256 and byte count research recorded.
- **Printed p. 381 on the registered facsimile.** The complete registered
  facsimile of volume 8
  (`artifact.catholic-encyclopedia.volume-8.new-york-1910.ia-facsimile-pdf-ac62a7ca`)
  was acquired from its registered route, 135,877,116 bytes, and matched its
  SHA-256. PDF p. 433 is headed printed p. 381, and its right column carries
  the sentence section 9.1 quotes, ending *"the future judgment; these
  predictions are interrupted by the parable of the ten virgins, and of the
  talents"*. Binding 45 now records that check, and its row carries the
  recomputed digest. No bytes are retained; the artifact stays remote under its
  record.
- **Registrations.** No new work, edition, artifact or passage identity was
  needed: research registered the one new passage (Maas), which is chronology
  evidence, not commentary, and has no Catena edge. No row changed its
  disposition. The leaf has 45 bindings and 59 rows: 12 admitted, 22 deferred,
  25 not-commentary, none rejected.
- **Advisory on the Psalm occasions.** Research answered it in sections 9 and
  10: the occasion rows report the chronology corpus's absence, and the held
  Psalm commentaries were not searched for an occasion. This stage searched
  them no further.
