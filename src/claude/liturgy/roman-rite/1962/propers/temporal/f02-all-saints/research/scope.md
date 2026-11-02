# Research scope: the Mass of All Saints, 1 November 2026

Research stage, iteration 3, of proper-study run `450355254538c1ba`.
Identity `liturgy/roman-rite/1962/propers/temporal/f02-all-saints`, provider
`claude`. Iteration 0 (27 October 2026) rebuilt the research from the sources:
nothing was taken over from earlier research records. The research handoff
(`workflows/reviews/claude-1962-f02-revision-2026-10-27/HANDOFF.md`) was used
only as a list of leads, and each lead used below was checked in the source it
names. Iteration 1 answers the research review recorded in
`evaluations/blocking-findings-v1.toml` (RES-001 to RES-010): it adds the
passage-by-passage reception matrix (3.0), the searches actually made and
their results, the witnesses those searches found, the liturgical
commentators' element comparisons, the planned place phrases of the
chronology rows (8.6) and the governing edition's closest Preface direction
(3.11). Nothing in iteration 0 that the review did not touch was re-derived.

Iteration 2 answers RES-011 to RES-013 of the same record, and the advisory
RES-014. The literal searches of iterations 0 and 1 took a query's spaces
literally, line by line, and the Internet Archive text layers separate many
words with two spaces or break a phrase across lines, so those searches
undercounted and returned false negatives. Iteration 2 replayed every recorded
multi-word query with whitespace-tolerant matching and records both counts
(method below); read at the line every hit it added that is not a missal or a
Bible; read Rabanus Maurus on Mt 5:1-12 and Mt 11:28 and Hilary, *In
Matthaeum* XI n. 15, which iteration 1 had recorded as not found, with their
page images (3.6, 3.7); added Augustine's sermons, Gregory's *Moralia* I and
Aquinas's I-II q. 107 a. 4 on Mt 11:28 (3.6), with the disagreement they
show (6.8), and Bruno of Würzburg on Ps 32:1 (3.2); entered the Gregorian
Sacramentary and Antiphonary printed in PL 78, and the eleventh-century
sacramentary of Monte Suavicino and the Fonte Avellana chant excerpts printed
in PL 151, into the history of the Collect, the Secret and the Offertory (3.1,
3.3, 3.8, 3.9); redated the
witness formerly cited as "Rome 1920" (3.8); and corrected the loci of
Augustine's *De sermone Domini* (3.7). Everything else stands as iteration 1
left it.

Iteration 3 answers RES-015 of the same record, and the advisories RES-016 and
RES-017. It read the prayer of all the apostles from which the Collect is
adapted in the Leonine Sacramentary (Feltoe 1896, image-read) and in the
Gelasian Sacramentary (Wilson 1894, OCR checked on the page images of the
remote scan), searched the whole library for the Collect and read every hit
at the line (3.1), and restates *intercessoribus* and *intercessionibus* as
two variants with the witnesses of each, without assigning a direction that
no checked witness establishes (3.3). The hit that iteration 2's review took
for the Mozarabic missal is the Monte Suavicino sacramentary again, printed in
an appendix to Migne's Mozarabic volume (3.1). It read Jerome on Mt 11:28 on
the page image of the remote PL 26 scan and found there the source of
Rabanus's unlabelled comment (3.6), and it describes Rabanus's source labels
as they are printed (3.7). Everything else stands as iteration 2 left it.

## 1. Publication mode and boundary

- **Mode: `complete`.** research/context.md records that no reference-only
  authorization exists; the manifest declares
  `appointed_text_completeness = "complete"`. The full Latin and English of
  every element are recorded in propers/verified.md with their publication
  basis (section 9).
- **The object studied** is the Mass said on Sunday 1 November 2026: the
  feast's ten texts (printed pp. 702-703, nos. 3974-3983) with the three orations
  of the Twenty-third Sunday after Pentecost (pp. 416-417, nos. 1720, 1726,
  1728) commemorated after the feast's Collect, Secret and Postcommunion, and a
  Preface that the rubrics read here leave between two candidates
  (propers/verified.md, element 11; section 3.11).
- **Psalm numbering.** Psalms are cited in the Missal's Vulgate numbering, with
  the Hebrew in parentheses: Ps 32:1 (33:1), Ps 33:10-11 (34:10-11; English
  Bibles that follow the Hebrew verse count print 34:9-10). Augustine's
  *Enarrationes* is cited in the Latin of the Migne text, which keeps the
  Vulgate number (Ps 32, enarrationes 1 and 2; Ps 33, sermo 2; Ps 87).
  Bellarmine's English numbers the verses without the title: his 9-10 are
  Vulgate 33:10-11, and his v. 1 of Ps 32 is Vulgate 32:1. NPNF's Augustine is
  not used for the Psalms here. Vulgate 33:12, *Venite, filii*, is not said.
- **Method.** Text control was read on page images (propers/verified.md). Each
  reception witness below was read at the locus given, in the artifact named,
  in the state stated. "Image-read" means the words quoted were read on a page
  image; "text-read" means on a text layer or transcription only; "OCR" means
  an uncorrected optical text layer, whose spelling is normalized in the
  quotations here.

## 2. Text control and its corrections

- The 1962 facsimile, Mame 1922 and Pustet 1862 were read on page images;
  propers/verified.md records every form and every collation.
- Corrections made to research/context.md from that reading: the Introit reads
  *solemnitáte* (one *l*); the Gospel closes *gaudéte et exsultáte, quóniam*
  (no capital, no comma); the Communion has a colon, not a semicolon, after
  *vidébunt*; Mame 1922's pages are printed pp. 748-750 (parent PDF pp.
  862-864); the 1570 Offertory stands at physical lines 71698-71701 of the 1570
  text layer; the Mame derivative of the six scriptural elements is described
  correctly (next item).
- **The Mame derivative of the scriptural elements does not keep Mame's
  forms.** `…1922-tours-mame-editio-quarta-iuxta-typicam.all-saints-scriptural-propers-la-checked-415a1d46`
  is described as image-checked Mame text with accents removed. Against the
  Mame page images it reads *milia* where Mame prints *míllia*, *quoadusque*
  where Mame misprints *quoasdúsque*, *Beniamin* where Mame prints *Bénjamin*,
  *Sancti ejus* where Mame prints *sancti ejus*, and the 1962 pointing in the
  Lesson, Gradual and Gospel. Its words agree with both printings, so no
  publication basis depends on it, but it is not a transcription of Mame. The
  basis rests on the Mame page images themselves. Reported for the source owner
  (section 10).
- The four-oration derivative `…all-saints-four-propers-la-checked-82edd79a`
  agrees with the Mame page images (*justi*, *justórum*, *solemnitate*, *Per
  Dominum*).

## 3. Reception

Three search methods were used, and every result below names its method.

- **Index.** `tools/commentary-work-index discover` was run, uncapped, for each
  appointed passage (Ps 32:1, Apoc 7:2-12, Ps 33:10-11, Mt 11:28, Mt 5:1-12,
  Wis 3:1-3, Mt 5:8-10), and `formulary` for `omnium-sanctorum` and
  `pentecost-23`. Its results are recorded below, candidate by candidate, in
  the matrix (3.0); the raw outputs are run receipts, not tracked records.
- **Literal text search.** Case-insensitive search over the tracked text
  artifacts under `src/sources/works` (and, for Wis 3, `src/sources/bibles`),
  with the terms given in each block of the matrix. Iterations 0 and 1 matched
  each query against single lines with its spaces taken literally (`rg`, and
  `tools/source-library search`, whose `raw-line-literal-casefold-v1` mode
  behaves the same way). The Internet Archive djvu text layers separate many
  words with two spaces (about two lines in five in the 1568 Durandus, and
  many in the PL volumes, Bonaventure vol. 6, the Parma Aquinas, Legg's Sarum
  and Guéranger vol. 15) and break phrases across lines, so those searches
  missed hits; they did not fail because of the long *s*, as iteration 1
  said. Iteration 2 replayed every multi-word query recorded below over the
  whole text of each file, with each space matched as any run of whitespace
  including a line break. Each block gives the counts as files/hits, literal
  then tolerant, and disposes of every hit the tolerant search added that is
  not a missal, a lectionary or a Bible. This search reaches tracked text
  layers only. Remote and restricted artifacts and page images are not
  searched by it, and OCR misreadings can still hide a hit: Bonaventure's
  lemma on Wis 3:1 is recognized as *lustorum* and was found only through the
  catalogue (3.0, Wis 3:1-3), and the 1568 Durandus prints *sanctorum* with a
  long *s* and a *ct* ligature that its OCR reads as *fandorum* (3.1).
- **Catalogue.** The holdings `discover` reports for each candidate, the
  registered work and containment records, and, for Wisdom, a listing of the
  work directories whose names mention Wisdom.

Holdings were used as finding aids, and every locus relied on was read. "Held,
not read" below names a held direct witness this stage did not read, with the
reason; "not held" means no library record, fragment edge, identity row or
containment entry joins the work (the index's own definition, which is not
proof that no copy exists); "searched, not found" names a search that was made
and its terms.

### 3.0 Reception matrix, passage by passage

Roles use the letters of research/interpretations.md: A
`sealed-number-uncounted-crowd`, B `beatitudes-way-of-the-saints`, C
`no-want-just-in-gods-hand`. "Carries" is said only of an author with a
standing row; an author without one "supports". "Illuminates" marks a use of
the verse that sheds light on it without expounding it, and which no reading
rests on.

#### Ps 32:1, *Exsultáte, iusti, in Dómino: rectos decet collaudátio*

- **Proper using it:** the Introit's psalm verse. The antiphon itself is not
  scriptural.
- **Direct ancient exegesis checked:** Augustine, *Enarr. in Ps.* 32, both
  enarrations on v. 1 (Migne Latin, wikisource part 4, physical lines 26 and
  28; text-read); Basil, *Homilia in Psalmum XXXII* n. 1 (PG 29 text layer
  `full-text-layer-2898b217`, lines 39150-39241, Greek and Latin columns; OCR,
  the facsimile not re-read for this homily). Section 3.2 gives what each
  infers.
- **Medieval, Doctoral and later reception checked:** Aquinas, *In Psalmos
  Davidis* 32 (Parma vol. 14, lines 41482-41591; OCR); Bellarmine (O'Sullivan's
  English, line 1137; text-read); Fromage on the Introit (Guéranger vol. 15,
  lines 7891-7903; OCR, French); St Bruno of Würzburg, *Expositio Psalmorum*
  on Ps 32:1 (PL 142, lines 11631-11651; OCR), whose extracts are marked by
  source siglum: under C, which the volume uses for Cassiodorus, the prophet
  warns Christians not to exult "in terrenis delectationibus … sed in
  Domino", and "Rectos decet collaudatio, non hereticos pravos decet, sed
  rectos … Collaudatio vero multorum ore una laudatio est, propter unitatem
  Ecclesiae".
- **Searched.** Index: `discover` (19 candidates). Literal, Latin and English
  (files/hits, literal then whitespace-tolerant): `rectos decet` 8/28 and
  18/82; `Exsultate,? justi` 4/7 and 11/72; `Exultate,? justi` 2/2 and 9/18;
  `Exsultate,? iusti` 1/1 and 1/1; `praise becometh the upright` 7/11 and
  11/23. Besides the expositors above, the hits of the literal search are
  uses, read at the line and not used: a commentary on the Song of Songs
  printed in PL 202 (John Beleth artifact `ia-djvu-ocr-22b781bf`, lines
  85788-85799: joy is vain "nisi quae fundatur in Domino", quoting *rectos
  decet collaudatio*); a sermon for St Narcissus printed in PL 142 (Berno
  artifact `ia-djvu-ocr-991758f7`, lines 50214-50215, *collaudatio*); the
  Sarum Missal (Legg 1916), as the Introit verse of All Saints (line 28084)
  and in a Communion of the common of many martyrs (line 30165), both with
  *collaudacio*; missals and Bibles; and Ps 31:11 (*Laetamini in Domino et exsultate,
  justi*) in PL 183 and PL 78, a different verse.
- **Added by the tolerant replay, read at the line.** Missals and chant books
  (Pustet 1862, Tournai 1889, the Mozarabic missal, Dickinson's and Legg's
  Sarum, the Gilbertine rite, the lay missals of 1806 and 1843, the 1549
  Prayer Book comparison, Lasance) and the Douay Bible, not further read. The
  Gregorian Antiphonary printed in PL 78 (`ia-djvu-ocr-301707e7`): the All
  Saints Introit verse *Exsultate justi in Domino, rectos decet collaudatio*
  (line 61962) and its vigil (61953), and the same psalm in other Masses
  (59795, 59883, 61097, the last a Communion *Gaudete justi … rectos decet*):
  liturgical witnesses, entered in 3.1. Guéranger vol. 15: the Introit verse
  of the Mass Fromage comments (7927-7928, already read) and the Communion of
  the Mass of the Holy Relics on 5 November (17908). Berno, PL 142 line
  90938: the Romans sing *Gaudete, justi* where "nos canimus: Exsultate,
  justi", a note on chant usage, not used. Uses, not used: St Bonaventure, *In
  II Sent.* (Quaracchi vol. 2, line 1883: "quia soli recti experiuntur, ideo
  rectos decet collaudatio"); Schuster vol. 3 (1927, line 20031, the verse as
  an alleluia verse of another Mass) and vol. 5 (line 13709, the vigil's
  Introit verse); Aquinas's *Summa* in the English Dominican translation, I-II
  (line 9611, and the same line in the raw text, 9639) and II-II (line 73023,
  and 73053), each reporting a gloss on Ps 32:1 ("That man has an upright
  heart, who wills what God wills"; "The upright are those who direct their
  heart according to the will of God"), the sense Augustine gives (3.2); the
  index of Wilson's Gregorian Sacramentary (line 19411). Ps 31:11, a different
  verse: Guéranger vol. 15 (6707, 7811) and vol. 13 (line 25901), the Parma
  Aquinas (41038) and PL 78 (60790). One expositor, read and entered below: St Bruno of Würzburg,
  *Expositio Psalmorum* on Ps 32:1, printed in PL 142 (Berno artifact, lines
  11631-11651; OCR), found through the PL 142 hits.
- **Roles.** Augustine carries C (the just exult not in themselves but in the
  Lord) and supports B (the upright are those who direct the heart by God's
  will, consoled in their frailty). Basil carries C (exult because you have such a Lord, not because of
  prosperity) and supports B (the rare joy given us is a small taste that
  reminds us of the unbroken joy of the just). Aquinas supports C (exult in
  the Lord, not in the world; *collaudatio* is praise in all things, in
  prosperity and adversity) and A (*Item unanimiter*). Bellarmine supports C.
  Fromage supports A (the angels' joy at the filling of their choirs). Bruno
  of Würzburg (no standing row), reporting Cassiodorus (ecclesiastical
  writer), supports C (exult in the Lord, not in earthly delights) and A (one
  praise from many mouths, for the unity of the Church).
- **Psalter form.** Augustine's psalter reads *Rectos decet laudatio* in both
  enarrations, where the Missal prints *collaudátio*. Basil's Latin lemma reads
  *collaudatio* (the Greek, αἴνεσις), and his exposition says *laudatio*.
  Aquinas reads *collaudatio* and draws an inference from the prefix (praise
  "de omnibus … non in aliquibus tantum", and "unanimiter"). Bellarmine's
  English reads "praise becometh the upright". The Clementine, the Sarum
  Missal, the PL 202 commentary and Fromage read *collaudatio*.
- **Negatives.** Held, not read: Cassiodorus (his tracked artifacts reach other
  psalms only; the whole work is held only in the remote PL 70, not fetched);
  Theodoret (remote PG 80 only, not fetched); Athanasius (remote PG 27 OCR,
  whose tracked artifacts reach Ps 83 and 94 only); Hugh of Saint-Cher
  (restricted). Not held: Nicholas of Lyra, Peter Lombard, Albert, Bruno the
  Carthusian, Denis the Carthusian (two index rows), Jerome (*Commentarioli*;
  *Tractatus*), Arnobius the Younger, Euthymius, Richard Rolle. Augustine's
  comment on Ps 32:12 ("one nation of the heavenly city") is on a verse the Mass
  does not say and is not used.

#### Apoc 7:2-12, the Lesson

- **Proper using it:** the Lesson, in the place of the Epistle.
- **Direct ancient exegesis checked:** Victorinus on 7:2-9 and 12:6 (ANF VII;
  text-read, recension uncertain); Bede on 7:1-4 and 7:9-12 (Marshall 1878,
  image-read; passage records 7:4, 7:9, 7:10, 7:11, 7:12); the anonymous PL 35
  *Expositio*, hom. 6 (image-read); Cyprian, *Ad Fortunatum* 11, who quotes
  7:9-15 and draws a conclusion from it (ANF V, lines 50324-50342); Augustine,
  Sermon LXI, who quotes 7:9 and draws a conclusion from it (NPNF I.6, lines
  43174-43216). Augustine, *Enchiridion* 29, Gregory, *Hom. in Ev.* 34 n. 11,
  and Aquinas, *ST* I q. 23 a. 7 give the doctrine of the number without
  commenting on the chapter (3.3). Section 3.4 gives what each infers.
- **Medieval and later reception checked:** Bernard, sermo 5 n. 2 (on 7:14,
  outside the Lesson); Sicard of Cremona, *Mitrale* IX c. 49 (the Lesson's
  fitness for the feast, beside the Gospel's); Durandus, Fromage and Schuster,
  who name or comment on the Lesson as an element (3.1).
- **Searched.** Index: `discover` (19 rows, with duplicates). Literal, Latin
  and English (files/hits, literal then whitespace-tolerant): `dinumerare
  nemo` 4/4 and 10/10; `quam dinumerare` 6/7 and 11/12; `which no man could
  number` 5/6 and 10/11; `which no man can number` 2/2 and 3/3; `numerum
  signatorum` 2/2 and 5/5; `numero signatorum` 1/1 and 1/1. The tolerant
  replay added missals (the Mozarabic missals of 1755 and 1862, Pustet 1862,
  Dickinson's Sarum, the lay missals of 1806 and 1843, Lasance), two Prayer
  Books (1662 annexed book, 1816) and three hits read at the line and not
  used: Guéranger vol. 15, line 6347 (a chant text of the feast's office);
  Aquinas, *In Ioannem* c. 21, in the Venice 1745 tom. 3 OCR
  (`ia-djvu-ocr-10aa155e`, line 109822), quoting 7:9 beside the draught of
  fishes, a use; and *Macmillan's Magazine* vol. 9 (line 6706), a literary
  allusion. Beyond the witnesses read, the hits of the literal search are missals and Bibles, a
  quotation of 7:9 in a compilation printed in PL 105 (Amalarius artifact
  `ia-djvu-ocr-f6438466`, line 52696), Blunt's *Annotated Book of Common
  Prayer* (line 31480), NPNF I.1, and two uses in Bellarmine's Psalms (lines
  3069 and 4543), none read beyond the line. `numero signatorum` found Sicard.
  For liturgical commentators beyond `formulary`, see 3.1.
- **Roles.** Bede carries A. Augustine carries A (Sermon LXI's use of 7:9;
  *Ench.* 29). Victorinus and Cyprian (no row) support A; Cyprian also stands
  with Schuster on the question of ease (5.1, 6.2). The PL 35 *Expositio*
  supports A. Gregory and Aquinas support A. Bernard (no row) supports A and B.
  Sicard (ecclesiastical writer) supports A and B: he joins the Lesson's number
  to the Gospel's. Schuster (blessed) supports A, as the other side of
  disagreement 6.2.
- **Negatives.** Not held: Primasius, Ambrose Autpert, Beatus of Liébana,
  Haimo (or Haymo) of Halberstadt (two index rows), Rupert of Deutz's
  commentary (two rows), Richard of Saint-Victor (three rows), Bruno of Segni,
  Nicholas of Lyra, Denis the Carthusian (two rows). Andrew of Caesarea is
  catalogued only, with no edition or artifact. Hugh of Saint-Cher is held only
  in restricted artifacts, not read. Cornelius a Lapide is reported "held"
  through title joins to his Pauline and Pentateuch commentaries, which do not
  reach the Apocalypse: not held for this passage. Caesarius of Arles: no
  separately held Apocalypse homilies (3.4).

#### Ps 33:10-11, the Gradual

- **Proper using it:** the Gradual (respond v. 10; verse v. 11b).
- **Direct ancient exegesis checked:** Augustine, *Enarr. in Ps.* 33 s. 2 nn.
  11-15, 19 (text-read); Basil, *Hom. in Ps.* 33 nn. 6-7 (Latin column
  image-read).
- **Medieval, Doctoral and later reception checked:** Aquinas, *Super Ps.* 33
  nn. 10-11 (OCR); Bellarmine (text-read, abridged); Bernard, sermo 5 n. 3, on
  the verse as sung in the night office of the feast (image-read; RES-010,
  3.5).
- **Searched.** Index: `discover` (15 candidates). Literal: `non deficient omni
  bono` (Latin) and `not be deprived of any good|shall not want for any
  good|shall not be diminished of any good|shall not want any good` (English):
  besides missals and Bibles, one use in PL 202 (line 66678) and Bellarmine's
  and NPNF's Psalms. The chant form of the Gradual was also read in the Sarum
  Missal's common of many martyrs (3.5). Counts (files/hits, literal then
  whitespace-tolerant): `non deficient omni bono` 4/5 and 10/16; the English
  alternation 5/8 and 6/12. The tolerant replay added missals and chant books
  (Tournai 1889, Pustet 1862, Dickinson's and Legg's Sarum, the Gilbertine
  rite, the 1843 lay missal) and PL 78, line 61296, a Gradual of another Mass
  in the Gregorian Antiphonary. Reading that Antiphonary's All Saints Mass
  (3.1) found its Gradual *Timete Dominum … non deficient omni bono* (lines
  61963-61966, OCR *deiicient*).
- **Roles.** Basil, Augustine, Aquinas and Bellarmine carry C. Bernard (no row)
  supports A and C, as reception of the verse the Gradual shares, not as a
  comment on the Mass Gradual.
- **Negatives.** Held, not read: Cassiodorus (remote PL 70 only), Theodoret
  (remote PG 80 only), Athanasius (remote PG 27 OCR; tracked artifacts reach Ps
  83 and 94 only), Hugh of Saint-Cher (restricted). Not held: Denis the
  Carthusian, Nicholas of Lyra, Peter Lombard, Albert, Jerome's
  *Commentarioli*, Euthymius, the *Glossa ordinaria*.

#### Mt 11:28, the Alleluia verse

- **Proper using it:** the Alleluia's verse.
- **Direct ancient exegesis checked:** Chrysostom, *Hom. in Matt.* 38.3 (NPNF
  I.10; text-read); Hilary, *In Matthaeum* XI n. 15 (PL 9 col. 984, image-read);
  Augustine, Sermons XIX and XX [LXIX and LXX Ben.], both on the verse (NPNF
  I.6; text-read), with his use of it in Sermon XXI [LXXI Ben.] n. 11; Jerome,
  *In Matthaeum* II on 11:28 (PL 26 col. 75, image-read on the remote scan,
  iteration 3; the page is retained as a tracked excerpt). Section 3.6 gives
  what each infers.
- **Medieval and later reception checked:** Rabanus Maurus, *Expositio in
  Matthaeum* IV on 11:28 (PL 107 col. 916, image-read); Gregory the Great,
  *Moralia* I, on Job 1:3, who uses the verse with an inference (Library of
  Fathers text; text-read); Aquinas, *ST* I-II q. 107 a. 4, *sed contra*,
  reporting Hilary (English Dominican translation; text-read).
- **Searched.** Index: `discover` (19 candidates). Literal, Latin and English
  (files/hits, literal then whitespace-tolerant): `qui laboratis et onerati`
  11/13 and 15/24; `qui laboratis, et onerati` 2/2 and 3/5; `labour, and are
  burdened` 0/0 and 2/2; `labor and are burdened` 3/3 and 4/4; `labour and are
  heavy laden` 9/25 and 13/33; `labor and are heavy laden` 5/8 and 7/11. In
  PL 107, `qui laboratis` 0 and 1 (line 101134, Rabanus's lemma) and `onerati
  estis` 0 and 0 (the OCR reads *onerali esiis*); in PL 9, `qui laboratis` 0
  and 1 (line 48137, a use). Iteration 1's statements that Hilary and Rabanus
  were "searched, not found" were false negatives of the single-spaced
  search; both comments are present and were read (3.6). The verse is quoted
  throughout the library, and every hit of either search outside missals and
  Bibles was read at the line in iteration 2. Read and entered: Augustine's
  Sermons XIX-XXI (NPNF I.6, lines 30141-30160, 30299-30389, 30706-30708);
  Gregory, *Moralia* I (line 1126); Aquinas, I-II q. 107 a. 4 (pg17897 line
  49940, and the same line in the raw text, 49968). Uses, read at the line and
  not used: Augustine, *Enarrationes* (Latin, wikisource parts 4, 7 and 10;
  English, NPNF I.8, lines 5168, 40188, 56204); Gregory, *Moralia* elsewhere
  (lines 6627, 25115, 29352, 32511, 33807, 47672); Bede, *In principium
  Genesis* (line 162); Ambrose, *Hexameron* (line 105); Rabanus on Esther
  (line 25); Honorius (lines 27477, 30082); Chrysologus (13938, 38157); PL 30
  (71681); PL 202 (42275, 55052, 73741); PL 9 (48137, Hilary elsewhere in the
  volume); Bonaventure vol. 6 (lines 28567, 49347, 54895, 64065, 93376,
  93475); Irenaeus reporting a Gnostic exegesis (ANF I, line 32201, and the
  1887 OCR, 41720); ANF V and VII (16459, 36881); NPNF I.1 (9444, 23239,
  29044), I.2 (47354), I.5 (19762), I.6 elsewhere (44933, 51872-51873), I.7
  (8050, 13190, 14406), I.10 (Chrysostom, Hom. 69, line 39018, besides Hom.
  38 at 23882 and 23948), I.12 (27650), I.13 (31586), II.7 (5473, 39388),
  II.8 (22831) and II.10 (19802, 33677, 42363); the lay missals and the Douay
  Bible. Iteration 3 fetched the remote PL 26 scan, which has no tracked
  text layer, and read Jerome's comment on 11:28-29 on its page image (PDF
  p. 45, col. 75); the source-registration stage retained that page as the
  tracked excerpt `…patrologia-latina-volume-26.paris-1845.columns-75-76-facsimile-b432adc8`.
- **Roles.** Chrysostom carries B and supports A ("not this or that person, but
  all") and C (rest given here). Hilary carries B (the yoke taken is his
  commandments, and he is approached by the sacrament of the cross, being
  meek and humble). Augustine carries B (learn of me that I am meek and lowly:
  begin from the foundation of humility) and supports C (the labour is mortal
  frailty, and rest is promised). Jerome (father), Rabanus (saint) and Gregory
  support B; their reading of the burden as the Law's yoke stands with
  Hilary's in the disagreement of 6.8. Rabanus's comment is Jerome's, taken
  over nearly word for word (3.6), so the two are one reading and not two
  witnesses to it.
- **Negatives.** Held, not read: Gregory, *Homiliae in Evangelia* (held; not read for this verse);
  Aquinas, *Super Matthaeum* on Mt 11 (held in the Venice volume read for Mt 5;
  this stage did not extend to Mt 11); Hugh of Saint-Cher (restricted). The
  *Catena aurea* is held only for Luke (restricted): not held for Matthew.
  Cornelius a Lapide: title joins only, not held for Matthew. Not held:
  Nicholas of Lyra, Paschasius Radbertus, Albert, Chromatius, Denis the
  Carthusian (two rows), Juan Maldonado, Theophylact, Bruno of Segni, the
  *Glossa ordinaria*.

#### Mt 5:1-12a, the Gospel

- **Proper using it:** the Gospel (vv. 1-12a); its vv. 8-10 are the Communion
  (next block).
- **Direct ancient exegesis checked:** Augustine, *De sermone Domini in monte*
  I.3.10-I.4.12; Chrysostom, *Hom. in Matt.* 15; Hilary, *In Matthaeum* IV nn.
  1-9.
- **Medieval, Doctoral and later reception checked:** Aquinas, *Super
  Matthaeum* c. 5 (Venice 1745 image-read; Corpus Thomisticum text-read);
  Rabanus Maurus, *Expositio in Matthaeum* II on 5:1-12 and on the Lord's
  Prayer (PL 107 cols. about 794-798 and 821-822; image-read at the loci
  quoted, OCR elsewhere); Bernard, *In festo omnium Sanctorum* sermo 1; Sicard, *Mitrale* IX c. 49 (the
  Gospel "de numero beatitudinum"); Fromage, who joins the Offertory to the
  beatitudes (3.8); Schuster on the Gospel (3.1).
- **Searched.** Index: `discover` (21 candidates). Literal, in Rabanus Maurus
  (PL 107 OCR), files/hits literal then whitespace-tolerant: `pauperes
  spiritu` 0 and 1 (line 93920, the Lord's Prayer passage); `mundo corde` 0
  and 1 (91859, his lemma of 5:8); `ascendit in montem` 0 and 1 (107010, Lk
  9:28 quoted at the Transfiguration, not Mt 5:1). Iteration 1 recorded the
  three zero counts as "not found"; they were false negatives of the
  single-spaced search, and the commentary on 5:1-12 stands at about lines
  91690-92200 (3.7). Augustine's *Quaestiones evangeliorum* (tracked PL 35
  text): its hits on these verses are incidental quotations; no question on
  Mt 5:1-12 was found.
- **Roles.** Augustine, Chrysostom, Aquinas, Hilary and Rabanus (saint) carry
  B. Bernard (no row), Sicard, Fromage and Schuster support B.
- **Negatives.** Held, not read: Jerome (PL 26 tracked excerpts do not reach Mt
  5; the remote volume, fetched in iteration 3 for Mt 11:28, was not read at
  Mt 5); Augustine, *De consensu evangelistarum*
  (NPNF I.6, held; not read); Hugh of Saint-Cher (restricted). The *Catena
  aurea* (Luke only, restricted) and
  Cornelius a Lapide (title joins only) are not held for Matthew. Not held:
  Gregory of Nyssa, *De beatitudinibus*; Chromatius; Paschasius Radbertus;
  Albert; Nicholas of Lyra; Denis the Carthusian; Juan Maldonado; Theophylact;
  Euthymius; the *Glossa ordinaria*.

#### Wis 3:1-3 as adapted, the Offertory

- **Proper using it:** the Offertory antiphon, which omits 3:2b-3a and reads
  *malítiæ* for the Vulgate's *mortis*.
- **Direct exegesis checked:** St Bonaventure, *Commentarius in librum
  Sapientiae* c. 3 vv. 1-3 (Quaracchi *Opera omnia* vol. 6, 1893, tracked OCR
  `ia-djvu-ocr-e7f54e11`, lines 22902-23082; OCR), a direct commentary that
  reports the *Glossa* and Rabanus at the verse; St Augustine, *Enarr. in Ps.*
  87 n. 5, which glosses Wis 3:1 itself (wikisource part 9, line 134;
  text-read). Section 3.8 gives what each infers.
- **Later saintly reception checked:** St Alphonsus Liguori, *Preparation for
  Death*, Ninth Consideration (Duffy 1843, OCR lines 5480-5686, printed pp.
  117-122), built on Wis 3:1-3.
- **Liturgical commentators:** Fromage on the Offertory (Guéranger vol. 15,
  lines 8427-8442); Schuster (3.1).
- **Illuminating uses, read at their loci:** Chrysostom, *Hom. in Matt.* 28
  n. 3 (NPNF I.10, lines 18096-18100; the Greek in PG 57 OCR, line 39312);
  Gregory, *Moralia* XII n. 6 (Library of Fathers text, lines 19547-19557);
  Bernard, *In transitu S. Malachiae* sermo 2 n. 5 (PL 183 OCR, line 43611).
- **Searched.** Index: `discover`, "no mapped commentaries yet". Literal, Latin:
  `animae in manu Dei`, `animæ in manu Dei`, `Justorum animae`, `Justorum
  animæ`, `visi sunt oculis insipientium`, `illi autem sunt in pace`,
  `tormentum malitiae`, `in manu Dei sunt`, `in pace sunt`; English: `souls of
  the just are in the hand`, `souls of the just are in the hands`, `souls of
  the righteous are in the hand`, `seemed to die`, `torment of death shall not
  touch`, `torment of malice`; Greek: `ψυχαὶ ἐν χειρὶ θεοῦ`, `ἔδοξαν ἐν
  ὀφθαλμοῖς ἀφρόνων`, `ἐν ὀφθαλμοῖς ἀφρόνων` (the last two, no hits);
  citation forms: `Sap.? ?III,? ?[123]`, `Sap.? ?3,? ?[123]`, `Wisd?.? ?iii.?
  ?[123]`, `Wisdom iii.? ?[123]`. Catalogue: the work directories naming Wisdom
  (Bonaventure's commentary found; the other is a papal document). In the
  Sarum Missal the term `tormentum` was searched and its hits read (3.8).
- **Counts** (files/hits, literal then whitespace-tolerant): `animae in manu
  Dei` 4/4 and 10/29; `animæ in manu Dei` 0 and 0; `Justorum animae` 7/7 and
  12/26; `Justorum animæ` 0 and 0; `visi sunt oculis insipientium` 2/2 and
  9/32; `illi autem sunt in pace` 3/5 and 11/48; `tormentum malitiae` 2/2 and
  8/26; `in manu Dei sunt` 8/9 and 20/78; `in pace sunt` 4/4 and 9/10; `souls
  of the just are in the hand` 4/10 and 7/23; `souls of the just are in the
  hands` 1/4 and 2/5; `souls of the righteous are in the hand` 1/1 and 4/7;
  `seemed to die` 7/18 and 10/31; `torment of death shall not touch` 1/2 and
  4/8; `torment of malice` 3/3 and 3/3; the Greek, 1/1 and 1/1, then 0 and 0
  twice; the citation forms 1/1 and 1/1, 0 and 2/2, 7/12 and 9/14, 0 and 1/1.
- **Added by the tolerant replay, read at the line.** Liturgical witnesses,
  entered in 3.8: the Gregorian Antiphonary and the Office book (*Liber
  responsalis*) printed in PL 78 (lines 60300-60302, 60310, 60791-60793,
  60865-60867, 61117, 61121, 72590, 72714-72715, 72812-72814, 75043-75044);
  the Fonte Avellana chant excerpts printed in PL 151 (Bernold artifact
  `ia-djvu-ocr-f7de4b32`, lines 70850-70852, 70875-70877, 73693-73694); the
  Würzburg *Comes* in Morin's edition (line 4179: CXC, "in nat. scorum", the
  lesson *Iustorum autem animae in manu dei sunt*), a lectionary. A use
  entered in 3.8: Aquinas, *In Ps.* 17 (Parma vol. 14, line 31719), who quotes
  Wis 3:1 with *tormentum malitiae*. Bonaventure vol. 6 beyond his commentary
  on c. 3 (which the replay also finds at 22967 and 23075): his *Comm. in
  Eccles.* c. 9 (line 14698) and his commentary on Wisdom at 1:15 (21599,
  quoting 3:1 with *tormentum mortis*) and at 4:17 (24628), the editors' note
  on the *Glossa* (23160, already read), a sermon or collation on the peace of
  the blessed (104341) and a note (70246): uses, not used. Schuster vol. 3
  (1927): the Gradual of another Mass from Wis 3:1-3, "the torment of death"
  (22068-22071), a lesson Wis 3:1-8 (23103) and an Offertory "the torment of
  malice" (26784-26786), sanctoral Masses, not used. Guéranger vol. 15, lines
  8440-8442 (Fromage's Offertory, already read). Brightman's *English Rite*:
  a lectionary table (19843) and Lk 11:21 (59166, a coincidence). Phrase
  coincidences or other verses: PL 78, line 66219 (Lk 11:21); PL 107, line
  87794; the *Supplementum* to the *Summa* (lines 6266, 6336, Wis 3:15); NPNF
  II.7 and II.10 footnotes (Wis 3:15 and 3:13); Shakespeare's works (10699)
  and Schmidt's *Shakespeare-Lexicon* (10674, 87684). Missals and Bibles (the
  Ambrosian missal of 1640, the Mozarabic books, Venice 1570, Tournai 1889,
  Pustet 1862, Dickinson's and Legg's Sarum, the Gilbertine rite, the lay
  missals, Lasance, Férotin's *Liber Mozarabicus sacramentorum*, Douay), not
  further read.
- **Other hits, read at the line and not used:** Augustine, *Enarr. in Ps.*
  118 (NPNF I.8, line 58648); John Damascene, *De fide orthodoxa* IV.15 and
  IV.27 (NPNF II.9, lines 37119 and 38687); the *Apostolic Constitutions* VI
  and VIII (ANF VII, lines 43883 and 47319); Aquinas, *De malo* q. 16 (line
  73); Peter of Celle in PL 202 (3.8, the wording's history); the Pseudo-Jerome
  *Comes* in PL 30 (line 41012: the lesson Wis 3:1 listed for SS Marcellinus
  and Peter). Phrase coincidences that are not uses of the verse: Augustine's
  *Quaestiones evangeliorum* and *De Genesi ad litteram* XII, Jerome on Daniel,
  Chrysologus, Honorius and Rupert.
- **Roles.** Augustine carries C (in God's hand: dwelling in the help of the
  Most High). Bonaventure (no standing row) supports C and B: in God's hand
  is under his protection, and the peace of the just is "nunc in spe, tandem in
  re". Alphonsus (no standing row) supports C and B. Fromage supports B.
  Schuster supports C. Chrysostom, Gregory and Bernard illuminate.
- **Negatives.** No other direct commentary on Wisdom is registered in the
  library (catalogue). The index maps no commentator to the passage, although
  Bonaventure's commentary is registered and contained in vol. 6 (section 10).
  The *Glossa* and Rabanus Maurus on Wisdom are read only as Bonaventure
  reports them; neither is registered for Wisdom.

#### Mt 5:8-10, the Communion, nested in the Gospel

- **Proper using it:** the Communion antiphon; the same verses stand in the
  Gospel.
- **Checked:** Fromage on the Communion (3.10); the Gospel's witnesses on vv.
  8-10 (Augustine I.3.10 and I.4.12; Bernard sermo 1 nn. 13-15; Hilary IV
  nn. 7-9; Aquinas; Rabanus on 5:8), who comment on the verses as part of the Gospel, not on the
  antiphon.
- **Searched.** Index: `discover` for Mt 5:8-10, whose candidates are those of
  Mt 5:1-12. No separate literal search was made.
- **Roles.** Fromage supports B; the Gospel's carriers carry B on these verses.
- **Negatives.** As for Mt 5:1-12. No witness read comments on the antiphon as
  such except Fromage.

### 3.1 Liturgical commentators and the feast

- **`formulary`, negative.** For both formularies: 40 loci compared, 0 listed,
  0 structural. No liturgical commentator is mapped to this Mass in
  `src/sources/commentary/formulary-loci.yaml`.
- **Search beyond `formulary`.** The tracked OCR of the liturgical
  commentators held in the library was searched for
  `omnium\s+sanctorum|festivitate\s+omnium|festo\s+omnium` (case-insensitive).
  Iteration 1 applied the pattern line by line, so a phrase broken across two
  lines was missed; iteration 2 applied it to the whole text of each file.
  Lines matched by iteration 1, then matches over the whole text: Amalarius
  (PL 105) 3 and 4; Rupert of Deutz, *De divinis officiis* (PL 170) 8 and 9;
  Bernold's *Micrologus* (PL 151, the whole volume) 19 and 25; Berno of
  Reichenau (PL 142, the whole volume) 16 and 17; Honorius, *Gemma animae*
  (PL 172) 12 and 15; Sicard, *Mitrale* (PL 213) 7 and 7; John Beleth (PL 202)
  16 and 19; Durandus with Beleth (1568) 1 and 1. Every match was read at the
  line. In the 1568 printing the cause of the low count is the OCR's reading
  of *sanctorum*, printed with a long *s* and a *ct* ligature, as *fandorum*,
  *Sandorum* or *fantorum*; the pattern `omnium\s+\S*an\S{0,3}orum` finds 15
  matches there, all read at the line: Durandus's chapter VII c. 34 (heading
  at 67273, the office at 67361), Beleth's c. 158 *De festo omnium sanctorum*
  (83349, below), and incidental hits (lists of fasts and chapters, a gloss on
  Ps 109:3, a prayer at Prime, the commemoration of the dead, the Assumption;
  lines 39444, 40808, 47832, 64567, 64871, 67468, 82932, 84546, with
  *angelorum* and *annorum* at 65685, 71633, 81721 and 83222). Found and read:
  Sicard and Honorius (below), with Durandus, Beleth, Schuster and Fromage.
  Among the added whole-text matches, PL 202 line 10899 is Beleth's c. 158
  (below), and PL 151 line 66275 is the Mass of the feast in the sacramentary
  printed there (below). The other matches in Amalarius, Rupert, Bernold and
  Berno are incidental (a vestment rule "in festo Omnium Sanctorum", Rupert
  line 101500; Odilo's decree for the commemoration of the dead, PL 142 line
  83529; charters, laws, prayers and editors' notes) and none treats the
  feast's Mass.
- **Element comparisons.** For each liturgical commentator, his heading and
  the elements he names, against the 1962 formulary:
  - **Durandus, *Rationale* VII c. 34, *De festo omnium Sanctorum*** (1568
    composite printing with Beleth, IA OCR
    `…1568-durandus-and-beleth-composite.ia-djvu-ocr-2bd5ccb5`, physical lines
    67273-67395, printed p. 799; OCR). Matches: the Epistle *Ecce ego Ioannes*
    (the 1962 Lesson; the OCR's chapter numeral is garbled), the Gospel
    *Videns Iesus turbas* (Mt 5), and the Collect, which he quotes. Differs: the
    Collect's word, *multiplicatis intercessionibus largiaris* (line 67349)
    where the 1962 Collect reads *multiplicatis intercessoribus* (printed p.
    702, no. 3975, image-read); his reading is the one Ménard's Gregorian
    codex and the eleventh-century sacramentary of Monte Suavicino give, and
    not the one of the Leonine and Gelasian prayer from which the Collect is
    adapted (below; the witnesses of each reading are listed in 3.3); the
    Alleluia *O quam gloriosum* where 1962 has
    *Veníte ad me*; his vigil Mass (Epistle *Ecce ego Ioannes*, Gospel Lk 6),
    which has no 1962 counterpart. Not named: Introit, Gradual, Offertory,
    Secret, Communion, Postcommunion. Office: nine responsories from the
    Trinity down to all the saints together, and the chapter *Vidi turbam*
    (Apoc 7). History: the Pantheon given by Phocas to Boniface and dedicated
    to Mary and all the martyrs, with *Terribilis est locus iste*, "quod tantum
    in dedicatione Ecclesiae solet dici"; Gregory IV's transfer to the Kalends
    of November, so that food would be found after the harvest. Four causes:
    the dedication; the supplying of omitted feasts (the second, not the only,
    cause); the expiation of negligences; and easier impetration, "quia
    impossibile est multitudinem non exaudiri".
  - **John Beleth, *Summa de ecclesiasticis officiis* c. 127, *De festo
    beatae Mariae ad martyres*** (same file, lines 81693-81725; OCR). History
    only: the Pantheon, Boniface IV, Gregory IV's transfer, and the feast of
    the Trinity, the angels and all the saints. He names no element of the
    Mass, so no comparison can be made. His c. 158, *De festo Omnium
    Sanctorum* (PL 202, `ia-djvu-ocr-22b781bf`, lines 10894-10924; OCR; the
    same chapter in the 1568 composite at line 83349), found by the
    whole-text replay: the feast keeps a fast "institutionis", not to be moved
    for St Quentin; the office varies "prout habetur varietas sanctorum", its
    nine antiphons, lessons and responsories running from the Trinity through
    Mary, the angels, prophets, apostles, martyrs, confessors and virgins to
    all the saints; the lessons are read in descending order of persons, from
    the bishop to the boys. He names no element of the Mass.
  - **Bl. Ildefonso Schuster, *The Sacramentary* V, heading "November 1. Feast
    of All Saints"** (English, 1930, printed pp. 208-212; retained chapter
    derivative `…all-saints-research-chapter-volume-5-d55b5905`, p. 210
    image-read; the chapter text-read whole in the volume's OCR, physical lines
    13898-14140). Matches: Introit *Gaudeamus*, the Collect, the Lesson Apoc 7
    (which he cites as "Apocalypse, viii, 2-12", a misprint for vii), the
    Gradual *Timete*, the Alleluia verse, the Gospel of the beatitudes, the
    Offertory, the Secret, the Communion and the Postcommunion. Differs: the
    Preface, for he gives the medieval proper Preface (*ut cum exsultantibus
    sanctis … gaudia nostra subiungas*), which is not a 1962 text. His notes:
    the Introit came from St Agatha (5 February); the Collect is Gelasian, for
    a collective feast of the Apostles in the octave of SS Peter and Paul; the
    Lesson is the Pantheon dedication's (13 May); the Gradual is St
    Cyriacus's (8 August); the Offertory St Hippolytus's (13 August). On the
    Lesson he writes: "It is not then so hard to be saved, as St John writes
    that he could not count the number of the elect", and makes the Tau of Ez
    9:4 the seal, with 2 Cor 1:7 (glory in proportion to a share in the
    Passion). On the Gospel: "those who have least according to the world
    receive a larger share of the heavenly gift". On the Offertory: the
    persecutor thinks the martyrs' lives are in his hands, but they are in
    God's. History: a collective feast of martyrs in fourth-century Syria;
    Boniface IV's Pantheon (13 May); Gregory III's oratory at St Peter's; the
    move to 1 November under Gregory IV (827-844), the initiative uncertain.
  - **Lucien Fromage, in Guéranger, *L'Année liturgique*, heading "A LA
    MESSE"** for 1 November (French, vol. 15, 1909, IA text
    `…french-oudin-1909-volume-15.ia-djvu-text-6301674b`, lines 7847-8536;
    OCR). Matches: Introit *Gaudeamus* with *rectos decet collaudatio*; the
    Collect with *multiplicatis intercessoribus* (lines 7961-7971); the Lesson
    Apoc 7, *Ecce ego Joannes*; the Gradual *Timete*; the Alleluia *Venite ad
    me*; the Gospel, ending *copiosa est in coelis* (12a); the Secret; the
    Communion; the Postcommunion (lines 8530-8536). Differs: the Offertory,
    printed *tormentum malitiae* without *alleluia* (lines 8437-8442), where
    1962 adds it. Not printed: a Preface. His comments, French, no English
    quoted from them: on the Introit (lines 7891-7903), the antiphon recalls the
    Assumption's, and "Joie parmi les Anges, qui voient se combler les vides de
    leurs chœurs"; on the Collect (7948-7955), "tant d'intercesseurs … Si la
    prière d'un habitant du ciel est puissante, que n'obtiendra pas le ciel
    tout entier?"; on the Offertory (8427-8432), "Les Béatitudes évangéliques
    élèvent l'homme au-dessus des tourments, au-dessus même de la mort, qui
    n'ébranle pas la paix des justes, mais la consomme. C'est ce que chante
    l'Offertoire"; on the Communion (8479-8484), "Echo de la lecture
    évangélique, l'Antienne de Communion, ne pouvant énumérer à nouveau la
    série entière des Béatitudes, rappelle les trois dernières, et, ce faisant,
    les rapproche toutes avec raison du Sacrement divin où elles
    s'alimentent."
  - **Sicard of Cremona, *Mitrale* IX c. 49, *In festivitate omnium
    Sanctorum*** (PL 213, IA OCR
    `…sicard-of-cremona.mitrale.latin-migne-pl-213.ia-djvu-ocr-ea9fd813`, lines
    31497-31517; OCR; standing ecclesiastical-writer). Matches: the epistle "de
    numero signatorum" (Apoc 7) and the gospel "de numero beatitudinum" (Mt
    5): "Huic festo bene congruit epistola de numero signatorum, et evangelium
    de numero beatitudinum". Not named: the other elements. Also the fast,
    which is not to be moved, and the office's responsories in the order
    Trinity, Mary, angels, prophets, apostles, martyrs, confessors, virgins,
    all the blessed together. His c. 24 (lines 30792-30807) gives the history
    (the Pantheon, Boniface, and a transfer to the Kalends of November that
    the OCR assigns to "Gregorius septimus", where Durandus and Schuster say
    Gregory IV); his c. 50 (lines 31545-31555) sets the vigil as affliction,
    the feast as exultation and the next day as prayer.
  - **Honorius Augustodunensis, *Gemma animae* III cc. 161 and 168** (PL 172,
    IA OCR `…gemma-animae.1895-garnier-migne-pl-172.ia-djvu-ocr-2ebfcb5f`,
    lines about 54195-54294; OCR; standing ecclesiastical-writer). History
    only: the Pantheon given to Mary *ad martyres*, with *Terribilis* sung at
    the dedication, and the feast instituted by Gregory (*junior*) where it had
    been Boniface's. He names no element of the 1962 Mass.
- **A medieval Mass for comparison (not a commentator).** The Sarum Missal
  (Legg, Oxford 1916, IA OCR
  `…missale-ad-usum-sarum.1916-oxford-clarendon-legg.ia-djvu-ocr-68839565`,
  lines 28071-28138, printed pp. 341-342; OCR), *In die omnium Sanctorum*.
  Matches: Introit *Gaudeamus* with the verse *Exultate iusti … rectos decet
  coll[audacio]*; the Collect, with *multiplicatis intercessoribus* (line
  28106), as in 1962 and against Durandus; the Lesson Apoc 7 *Ecce ego
  iohannes*; the Gradual *Timete dominum*; the Gospel *Uidens turbas*; the
  Secret and the Postcommunion. Differs: the Alleluia *Iudicabunt sancti*, the
  sequence *Christo inclito*, the Offertory *Mirabilis deus* and the Communion
  *Gaudete iusti*.
- **Two further Mass books for comparison (not commentators), found by the
  whole-text replay.** Neither was in iteration 1's reading.
  - **The Gregorian Sacramentary in Ménard's edition**, reprinted in PL 78
    (`…patrologia-latina-volume-78.latin-migne-pl-78.ia-djvu-ocr-301707e7`,
    lines 11147-11178; OCR). The Mass stands as "EODEM DIE. NATALIS OMNIUM
    SANCTORUM", after St Caesarius (1 November). Collect: "Omnipotens
    sempiterne Deus, qui nos omnium sanctorum merita sub una tribuisti
    celebritate venerari, quaesumus ut desideratam nobis tuae propitiationis
    abundantiam, multiplicatis intercessionibus, largiaris" (11149-11153);
    Secret (*Super oblata*) *Munera tibi, Domine*, with *honore sanctorum*
    where 1962 has *honore iustorum* (11155-11158); a proper Preface, "ut cum
    exsultantibus sanctis in coelestis regni cubilibus gaudia nostra
    subjungas" (11160-11165), the medieval Preface Schuster gives; an episcopal
    blessing (11195-11201); a Postcommunion (*Ad complendum*) *Sanctorum
    omnium gloriosa confessio* (11203-11206), not the 1962 text, and after it,
    as *Alia*, *Da, quaesumus, Domine, fidelibus populis omnium sanctorum
    semper veneratione laetari*, the 1962 Postcommunion (11208-11209). The Maurist
    editors' note (11172-11178) answers Pamelius, who said the day's office
    was in all the manuscripts: it is wanting in the Queen of Sweden's codex,
    in two others Ménard indicates, and in the Roman calendar. Ménard's own
    note (lines 52226-52229): the first oration reads *multiplicatis
    intercessionibus*; "licet in Missali Romano legatur, intercessoribus,
    prior tamen lectio non est contemnenda". The Gregorian Antiphonary
    printed in the same volume (the editors' preface, lines 487-489: the
    chants "quae in Missis canenda sunt"; lines 61952-61968; OCR) gives the
    vigil (*Judicant sancti gentes*) and "In die ad Missam": the Introit
    *Gaudeamus omnes in Domino* with the psalm verse "Exsultate justi in
    Domino, rectos decet collaudatio"; the Gradual *Timete Dominum … non
    deficient omni bono*; the Alleluia *Justi epulentur*; the Offertory *Deus
    in sanctis suis* (the incipit as the OCR gives it); the Communion
    *Gaudete, justi, in Domino*. Against 1962, the two books together match
    in the Introit, the Collect (in its *intercessionibus* reading), the
    Gradual, the Secret (but for *sanctorum*) and the second Postcommunion;
    they differ in the Alleluia, the Offertory, the Communion, the first
    Postcommunion and the Preface.
  - **The *Sacramentarium vetus* printed in PL 151** (the eleventh-century
    sacramentary of the hermits of Holy Trinity on Monte Suavicino, edited by
    Mittarelli and Costadoni, *Annales Camaldulenses* II, 1756, as the
    *Monitum* at lines 63740-63784 says; the volume's OCR
    `…micrologus-de-ecclesiasticis-observationibus.latin-migne-pl-151.ia-djvu-ocr-f7de4b32`,
    lines 66273-66289; OCR). "IN FESTIVITATE OMNIUM SANCTORUM": the Collect
    with *multiplicatis intercessionibus largiaris*; the Secret with *honore
    justorum*, as in 1962; the Postcommunion *Da, quaesumus, Domine, fidelibus
    populis omnium semper sanctorum veneratione laetari, et eorum perpetua
    supplicatione muniri*, as in 1962. It gives no chants for the day.
    The same sacramentary, with the same *Monitum* (Mittarelli and
    Costadoni, *Annales Camaldulenses* II, Venice 1756, appendix p. 597), is
    printed again in an appendix to Migne's *Liturgia Mozarabica* I (PL 85,
    Paris 1862; text layer
    `…missale-mixtum-mozarabicum.paris-migne-1862.liturgia-mozarabica-1862-text-769ccd75`,
    the *Monitum* at lines 97865-97873, the heading "Vetus sacramentarium
    nunc primum editum ex codice membranaceo saeculi XI" at 98106-98108;
    OCR). Its Mass "(20) IN FESTIVITATE OMNIUM SANCTORUM" (lines
    100412-100428) has the same Collect, "qui nos omnium sanctorum tuorum
    merita sub una tribuisti celebritate venerari, quaesumus, ut
    desideratam nobis tuae propitiationis abundantiam multiplicatis
    intercessionibus largiaris" (100414-100418), the same Secret and the
    same Postcommunion. It is a second printing of the Monte Suavicino book
    and not a witness of the Mozarabic rite. A whitespace-tolerant search of
    the volume for the Collect's words (`sub\s+una\s+trib`,
    `propitia[ct]ionis\s+abund` and an OCR-tolerant form of *tribuisti
    celebritate*) finds it at this place only; the Missale mixtum's own Mass
    of the feast was not read.
- **The prayer the Collect adapts, in the two oldest sacramentaries held
  (not commentators).** Schuster says the Collect is Gelasian and was
  written for a collective feast of the Apostles (above). Both books give it
  as a prayer of all the apostles, *omnium apostolorum*, where the feast's
  Collect has *omnium sanctorum*. Neither has a Mass of All Saints.
  - **The Leonine (Verona) Sacramentary**, Feltoe's edition (Cambridge
    1896; the tracked scan
    `…sacramentarium-veronense.feltoe-1896.internet-archive-pdf-3b991b13`,
    printed p. 46, lines 18-21, PDF p. 70; image-read). Under *Mense Iunio*
    (the running head of p. 45), in the series that begins "XV. IN N̄
    APOSTOLORUM PETRI ET PAULI" (p. 36), formulary "XXI. Item alia", second
    prayer: "Omp semp Ds qui nos omnium apostolorum merita sub una
    tribuisti celebritate venerari quaesumus ut celerem tuae propitiationis
    abundantiam multiplicatis intercessoribus largiaris per." Feltoe's notes
    on the page record no variant at this prayer; Muratori's page number 341
    stands in his margin.
  - **The Gelasian Sacramentary**, Wilson's edition of Vat. Reg. lat. 316
    (Oxford 1894; the tracked OCR
    `…sacramentarium-gelasianum-vetus.wilson-1894.historical-book-ocr-e4500b54`,
    lines 18076-18104, with the notes at 18124-18145; checked on the page
    images of the remote scan `…wilson-1894.internet-archive-pdf-006a38a3`,
    PDF pp. 276-277, printed pp. 183-184, fetched whole and matched to its
    registered SHA-256; the two pages are retained as the tracked page
    extraction `…wilson-1894.pages-183-184-facsimile-7f5cc922`). Book II, section xxxiii, *Orationes ad Vesperum*,
    which follows the Masses of SS Peter and Paul (II.xxxi, *In natali
    apostolorum Petri et Pauli*, iii Kal. Iul., and the Mass of St Paul in
    II.xxxii) and precedes II.xxxiv, *Item de vigilia omnium apostolorum*.
    Its fifth prayer: "Omnipotens sempiterne Deus, qui nos omnium
    apostolorum merita sub una tribuisti celebritate venerari, quaesumus ut
    celeriter nobis tuae propitiationis abundantiam multiplicatis
    intercessoribus largiaris. Per." (p. 183), with "Leon. 341" in the
    margin. The apparatus (p. 184): "celerem Leon.; desideratam S² Gerb.; V.
    S¹ as text", and "multiplicas V."; none at *intercessoribus*. Wilson's
    note on the series says this prayer is in S. and Gerbert "the last of
    the aliae Orationes for the festival", and his note on II.xxxiv that the
    Natale omnium apostolorum "does not appear as a Festival in the other
    Sacramentaries here cited". The section is not an octave: Schuster's
    "octave of SS Peter and Paul" is his, not Wilson's heading.
  What these two books show is the wording of the apostles' prayer. They do
  not show when, where or by whom it was adapted to all the saints. The
  feast's *desideratam* for *celerem* or *celeriter* is the reading Wilson
  reports from a later hand of the St Gall book and from Gerbert.
- **Other Mass books with the Collect, found by a whole-library search
  (not commentators).** Iteration 3 searched every tracked text file under
  `src/sources` for `sub\s+una\s+tribuisti` (11 files) and for
  `multiplicat\w*[\s-]+[il]n?ter[\s-]*ces` (10 files), whitespace-tolerant
  and across line breaks, and read each hit at the line:
  - the Gilbertine Missal (Woolley, vol. 2, 1922,
    `…gilbertine-rite.woolley-1921-1922.volume-2-ocr-ce518b29`, lines
    14950-14957, printed p. 197, *In die omnium sanctorum*, fo. 122; OCR):
    "qui nos omnium sanctorum merita … desideratam nobis tue propiciationis
    abundantiam multiplicatis intercessoribus largiaris";
  - Dickinson's Sarum Missal (Burntisland 1861-1883,
    `…1861-1883-burntisland-dickinson.ia-djvu-ocr-685c74b2`, lines about
    81708-81716; OCR): *multiplicatis intercessoribus*; its second hit, line
    112666, is the index of collects;
  - Brightman, *The English Rite* II (London 1915,
    `…english-rite.london-rivingtons-1915-volume-2.ia-djvu-text-englishrite0002febr-f01e2067`,
    lines 19661-19676, printed p. 632; OCR), printing the Sarum Collect as
    the source of the Prayer Book's: *multiplicatis intercessoribus*, with
    "(Leon. 341)";
  - the Roman Missal: Venice 1570 (text layer, lines 71592-71599; the OCR
    reads *íntercefTozibus*), Pustet 1862 (lines about 77622-77632, and the
    Octave at about 77860-77872) and Tournai 1889 (lines about 77577-77585,
    and the Octave at about 77795-77804), all *omnium Sanctorum tuorum …
    desideratam … multiplicatis intercessoribus*; Mame 1922 and the 1962
    typical edition on their page images (propers/verified.md);
  - Fromage (above), and this repository's editorial projection and
    calendar data, which reproduce the 1962 text and are not witnesses;
  - Sicard of Cremona's PL 213, line 52838: *multiplicatis intercessoribus*
    in a letter of Innocent III printed in the *Historia Albigensium* of the
    same volume, a phrase coincidence and not the Collect.
  The 1604 typical edition's text layer is too corrupt at the feast (lines
  53418-53429) to read the word. Wilson's Gregorian Sacramentary (the
  Hadrianum, HBS 1915,
  `…sacramentarium-gregorianum-hadrianum.wilson-1915.pdf-text-layout-6ca97fd7`)
  has no Mass of All Saints: neither search finds the Collect in it, and its
  *omnium sanctorum* hits, read at the line, are a votive Mass named in the
  introduction (line 1698), the Canon's list of saints (2301), texts of
  other days (12640, 15992) and the index (19085, 19197). The Ménard
  Gregorian, the Monte Suavicino book and the 1568 Durandus, whose text
  layers break the words, were found by iteration 2's searches (above); the
  Feltoe edition's optical text layers are remote only, were not searched,
  and the prayer was read on the images of the tracked scan.

### 3.2 Introit: the antiphon and Ps 32:1

- **The antiphon** is not scriptural. Schuster (3.1) gives its earlier use;
  Fromage (3.1) comments on its words: the feast follows the Assumption, and
  the angels rejoice to see the gaps in their choirs filled.
- **Ps 32:1** was read in its context (Ps 32 whole, Douay and Clementine). Four
  direct expositions of the verse were read:
  - **St Augustine, *Enarr. in Ps.* 32, enarratio 1** (wikisource part 4,
    physical line 26; text-read): "Exsultate justi in Domino: exsultate justi,
    non in vobis, non enim hoc tutum est; sed in Domino. Rectos decet laudatio:
    ipsi laudant Dominum, qui se subdunt Domino; aliter enim distorti et pravi
    sunt." The inference: the ground of the just's joy is outside themselves,
    and only the subject can praise.
  - **Augustine, enarratio 2, sermo 1** (line 28; text-read): "Exsultate
    fideles in Domino, quia justus ex fide vivit. Rectos decet laudatio.
    Discite gratias agere Deo et in prosperitatibus, et in tribulationibus";
    "Qui sunt recti? Qui dirigunt cor secundum voluntatem Dei; et si eos
    perturbat humana fragilitas, divina consolatur aequitas". The inference:
    the just are the faithful; the upright are those who set their heart by
    God's will and give thanks in every lot.
  - **St Basil, *Homilia in Psalmum XXXII* n. 1** (PG 29 text layer, lines
    39150-39241, the Latin column with the Greek beside it; OCR, normalized).
    The Latin lemma reads *recto decet collaudatio* (Greek τοῖς εὐθέσι πρέπει
    αἴνεσις). "Exsultate itaque, justi, in Domino; non cum res domi vobis
    prospere succedunt, non cum bona fuerit corporis habitudo … sed quod
    Dominum habetis"; the joy that God sometimes, rarely, lets fall on us is a
    small taste that reminds us of what we lack, but "justo perpetua est divina
    ac caelestis laetitia, quod semel in ipso inhabitat Spiritus" (Gal 5:22);
    the Lord is the place of the just, and the just man becomes a place for the
    Lord; "Quemadmodum pes obtortus calceo recto non adaptatur; ita neque
    distortis cordibus laudatio Dei convenit". The inference: the joy commanded
    rests on possessing the Lord, not on fortune, and is unbroken in the just.
  - **St Thomas Aquinas, *In Psalmos Davidis* 32** (Parma vol. 14, lines
    41482-41591; OCR, normalized). The psalm is "de dignitate justorum";
    "Justi, quia justificati estis, exultate in Domino, non in mundo … non enim
    est justus qui non gaudet in justitia". Why *justi* and not *omnes*?
    "Rectos decet collaudatio": a thing is right by conforming to its rule, and
    the rule of the human will is the divine will, so those who will not
    conform their will to God's "non possunt bene collaudare Deum"; those who
    conform "gaudent in prosperis et adversis; et ideo dicit Collaudatio, quia
    de omnibus laudant, non in aliquibus tantum. Item unanimiter", with Ecclus
    15:9, "Non est speciosa laus in ore peccatoris". The inference: the prefix
    *col-* means praise in every lot and praise in concord.
  - **St Robert Bellarmine** (O'Sullivan's English, line 1137; text-read):
    the rejoicing asked for includes praising God with great affection, inward
    and outward; "praise becometh the upright" is a special invitation to the
    just, with whom God is always pleased; the crooked offend him rather than
    praise him.
  - **St Bruno of Würzburg, *Expositio Psalmorum*** (PL 142, Berno artifact
    `ia-djvu-ocr-991758f7`, lines 11631-11651; OCR), an extract under the
    siglum the volume uses for Cassiodorus: not to exult "in terrenis
    delectationibus … sed in Domino"; *collaudatio* is fitting not for
    heretics but for the upright, and "Collaudatio vero multorum ore una
    laudatio est, propter unitatem Ecclesiae". Found by the iteration-2
    replay (3.0).
- **How the readings use them.** Reading C's Introit rests on Augustine and
  Basil (joy in the Lord possessed, not in prosperity); Reading B's on Basil's
  taste of the unbroken joy of the just and Augustine's upright who set the
  heart by God's will; Reading A's on Fromage's comment on the antiphon, with
  Aquinas's *unanimiter* as an editorial join (research/interpretations.md).
- **Psalter form.** Augustine's psalter reads *laudatio*, the Missal
  *collaudátio*; the forms of the other witnesses are given in 3.0.
- **Held, not read**: Cassiodorus, Theodoret, Athanasius and Hugh of
  Saint-Cher, with the reasons in 3.0. Augustine's comment on Ps 32:12 ("the
  one nation of the heavenly city"), which the handoff reports, is on a verse
  the Mass does not say and was not used.

### 3.3 The orations: intercession, veneration and the number of the elect

- **Collect, *multiplicatis intercessoribus*.** The witnesses read give the
  word in two forms (each read in full in 3.1):
  - *intercessoribus* ("intercessors"): the Leonine Sacramentary's prayer of
    all the apostles (Feltoe p. 46, image-read) and the Gelasian's (Wilson
    p. 183, image-read; his apparatus records no variant at the word); and,
    for the feast, the Gilbertine Missal, the Sarum Missal (Legg; Dickinson;
    Brightman's citation of it), and the Roman Missal from the Venice 1570
    printing to 1962 (1570, Pustet 1862 and Tournai 1889 on text layers;
    Mame 1922 and 1962 on page images). Fromage comments on this form.
  - *intercessionibus* ("intercessions"): for the feast, the Gregorian
    Sacramentary in Ménard's codex (PL 78), the eleventh-century
    sacramentary of Monte Suavicino (printed twice by Migne, in PL 151 and in
    the appendix to PL 85), and Durandus's *Rationale*, which quotes the
    Collect of his Mass in this form.
  These are two readings of the same prayer. No checked witness says which
  came first, or when either entered the books of any rite, and the ages of
  the witnesses do not settle it: the Leonine and Gelasian books give the
  apostles' prayer, not the feast's adaptation of it. Ménard says only that
  his codex reads *intercessionibus* in the first oration: "Hoc loco licet
  in Missali Romano legatur, intercessoribus, prior tamen lectio non est
  contemnenda" (PL 78 lines 52226-52229). His "prior lectio" is the reading
  he has just named first, his codex's; he says it is not to be despised,
  not that it is older. Durandus's word is therefore not a slip, and it is
  not the 1962 Collect's. His use here is limited to what he says of the
  petition both forms share: it rests on many interceding, "impossibile est
  multitudinem non exaudiri". The Secret shows a like variant: *honore
  sanctorum* in Ménard's Gregorian Sacramentary, *honore iustorum* in the
  Monte Suavicino book and 1962 (3.9). Fromage (3.1) on the 1962 form: so
  many intercessors, the whole of heaven. St Bernard, *In festo omnium Sanctorum*
  sermo 2 n. 1 (PL 183 col. 463, image-read): "cum eorum intercessione juvetur
  infirmitas nostra"; the ladder by which the whole choir of saints ascended,
  and "implorandis eorum suffragiis".
- **Postcommunion, *veneratione laetari*.** The text stands in Ménard's
  Gregorian Sacramentary as the second Postcommunion (*Alia*) and in the PL 151
  sacramentary as the only one (3.1). Bernard, sermo 5 n. 5 (PL 183 cols.
  477-478, OCR, with the opening checked on the image of col. 477): "Ad quid
  ergo sanctis laus nostra? … honorum nostrorum sancti non egent … quod eorum
  memoriam veneramur, nostra interest, non ipsorum"; the memory kindles a
  threefold desire, first for their company, "in omnium denique colligi et
  collaetari communione sanctorum".
- **The number of the elect** (the Lesson's counted 144,000 and uncounted
  multitude). Doctrine of the number, not commentary on Apoc 7:
  - St Augustine, *Enchiridion* 29 (NPNF I.3, New Advent page fetched whole
    and matched to the registered
    `…english-npnf1-3-new-advent-web-2026-09-05.newadvent-1302-bed70924`,
    SHA-256 `bed70924…2aa2`, 266,881 bytes, 2026-10-27; text-read): restored
    mankind fills "the gap which the rebellion and fall of the devils had left
    in the company of the angels", and the city "shall perhaps reign over even
    a more abundant population. We do not know the number either of the saints
    or of the devils; … But the number of the citizens … is present to the
    thoughts of the great Creator".
  - St Gregory the Great, *Homiliae in Evangelia* 34 n. 11 (on Lk 15:1-10;
    tracked Wikisource Latin
    `…homiliae-in-evangelia.wikisource-web-2026-09-17.complete-extracted-text-dc25dd69`,
    physical line 456; text-read): "superna illa civitas ex angelis et
    hominibus constat, ad quam tantum credimus humanum genus ascendere, quantos
    illic contigit electos angelos remansisse" (Deut 32:8); the different ways
    of life of the elect are allotted to the nine orders.
  - St Thomas Aquinas, *ST* I q. 23 a. 7 (English Dominican translation, read
    first at New Advent, page 1023.htm fetched whole 2026-10-27T20:44:55Z,
    78,621 bytes, SHA-256 `b203a0a3…98b0`, since registered as
    `…2026-10-27-english-dominicans-newadvent-prima-q23.prima-q23-delivery-b203a0a3`;
    then confirmed word for word in the registered Gutenberg text of the same
    translation,
    `…summa-theologiae.2006-english-dominicans-gutenberg-prima.pg17611-body-9c99a67a`,
    physical lines 12507-12603; text-read): the number of the
    predestined is certain to God; of the three opinions (as many men as angels
    fell; as many as remained; as many as were created) "it is, however, better
    to say that, 'to God alone is known the number for whom is reserved
    eternal happiness'", quoting the Missal's Secret *pro vivis et defunctis*.
    That Secret, *Deus, cui soli cognitus est numerus electorum in superna
    felicitate locandus*, stands in the 1962 *Orationes diversae*, oratio 35,
    printed p. [115], no. 5086 (PDF 923, image-read). It is not said on 1
    November.
  - Augustine's and Cyprian's direct uses of Apoc 7:9 belong to the Lesson
    (3.4).
- **Commemoration orations.** No commentator on the Twenty-third Sunday's
  orations was read; `formulary` lists none (3.1). Their words are recorded
  with their Pustet collation in propers/verified.md.

### 3.4 Lesson: Apoc 7:2-12

Read in context: Apoc 1:9-11, 4-5, 6:9-17, 7:1-17, 14:1-5 (Douay and
Clementine). Apoc 1:9-11 sets the visions: John "was in the island, which is
called Patmos, for the word of God, and for the testimony of Jesus", and is
told to write what he sees and send it to the seven churches in Asia (8.6).

- **St Victorinus of Pettau, *Commentary on the Apocalypse*** (ANF VII,
  `ccel-text-b69327af`, lines 33565-33625, and on 12:6 lines 33964-33974;
  text-read). 7:2: the angel from the east is Elias, precursor "of the times of
  Antichrist, for the restoration and establishment of the churches from the
  great and intolerable persecution" (33568-33570); "the number of those that
  shall believe, of the Jews and of the nations, is a great multitude which no
  man was able to number" (33575-33577). 7:9: "the number of the elect out of
  all believers", cleansed by baptism (33620-33625). 12:6: the 144,000 who
  believe at Elias's preaching in the last times. His remark that order is not
  to be sought in the Apocalypse (33604-33613) concerns the trumpets and the
  phials; it is not about the sealing. The editor's elucidations (lines
  34525-34539) warn of interpolation and a corrupt manuscript tradition: the
  recension is uncertain.
- **St Bede, *Explanatio Apocalypsis*** (Marshall's English, 1878, whole scan
  `…1878-marshall-parker.whole-scan-65cb5fc5`, PDF pp. 56-58 = printed pp.
  44-46 for 7:1-4 and PDF pp. 64-65 = printed pp. 52-53 for 7:9-12, image-read
  at 110 dpi; registered passages `…1-7-4`, `…1-7-9`, `…1-7-10`, `…1-7-11`,
  `…1-7-12`). 7:1: four angels as the four kingdoms or four winds. 7:2: "The
  Lord incarnate, Who is the Angel of the great counsel … has visited us, 'the
  day-spring from on high,' bearing the ensign of the cross, with which to seal
  His own in their foreheads." 7:3: the seal of faith on the foreheads; the
  cross. 7:4: the number signifies the innumerable multitude of the whole
  Church. 7:9: first, those who overcome the last persecution; as an
  alternative, the Gentiles joined to the Church. 7:10: "They proclaim with a
  loud voice, that is, with great devotion, an unceasing praise, that on the
  throne, namely, in the Church, there reign the Father and the Son; the Holy
  Spirit, nevertheless, reigning together with them", with Jn 17:3 for the
  one God understood in the two names. 7:11: the angels may stand for the
  multitude, or be the angels themselves. 7:12: "The Church offers the
  sevenfold praise of excellence unto the Lord, and in each of its members
  confesses to have received this from Him." The inference of 7:10 and 7:12:
  the multitude's cry is the Church's praise, given to the Trinity reigning in
  the Church, and every member confesses that what is praised was received.
- **Anonymous *Expositio in Apocalypsim*, in the appendix to Augustine** (PL
  35, 1845, artifact
  `…patrologia-latina-volume-35.1845-paris.internet-archive-google-pdf-b3ff8a95`,
  fetched whole and matched, 62,548,064 bytes; PDF p. 562 = cols. 2425-2426,
  image-read). Homilia VI begins at col. 2425: "Alterum angelum eamdem
  Ecclesiam catholicam intelligit: ab ortu solis, a passione et resurrectione
  Domini"; at col. 2426, "Centum quadraginta quatuor millia, omnis omnino
  Ecclesia est". The work is spurious under Augustine and was not used as his;
  its usual attribution (to Caesarius of Arles) is not established by anything
  read here.
- **St Cyprian, *Ad Fortunatum* (Exhortation to Martyrdom) 11** (ANF V,
  `ccel-text-a02b61c3`, lines 50324-50342; text-read). The ancient examples
  "may be numbered", but "the Christian martyrs cannot be numbered, as the
  Apocalypse testifies", and he quotes Apoc 7:9-15. From the quotation he
  concludes (50339-50342): "But if the assembly of the Christian martyrs is
  shown and proved to be so great, let no one think it a hard or a difficult
  thing to become a martyr, when he sees that the crowd of martyrs cannot be
  numbered." The inference runs from the uncounted multitude to the ease of
  martyrdom; it is limited to martyrdom.
- **St Augustine, Sermon LXI** (NPNF I.6, `ccel-text-ce371798`, lines
  43174-43216; text-read). On Lk 13:23-24, "Are there few that be saved? Strive
  to enter by the strait gate": the Lord "confirmed what He heard", and "few
  then are saved in comparison of the many that shall perish. For these same
  'few' will constitute in themselves a great mass", the wheat the Winnower
  lays up in the garner; "So large a mass is to come out of this floor, as to
  fill the garner of heaven". Then: "the 'few' are themselves the 'many;'
  'few' in comparison of the lost, 'many in the society of the Angels.'
  Hearken, dearly Beloved. The Apocalypse hath this written; 'After this I
  beheld of all languages, and nations, and tribes, a great multitude, which no
  man can number, coming with white robes and palms.' This is the mass of the
  saints"; the floor, fanned and separated from the ungodly and false
  Christians, leaves "the purified mass, standing at the Right Hand", about to
  reign with Christ. The inference: Apoc 7:9 shows that the few who pass the
  narrow gate are many in themselves; the "mass of the saints" is the
  winnowed grain, and the image and the phrase go together.
- **St Bernard, sermo 5 n. 2** (PL 183 col. 476, image-read): the second kind
  of saints are those who "venerunt ex magna tribulatione et dealbaverunt
  stolas suas in sanguine Agni" (Apoc 7:14, outside the Lesson); the third,
  still fighting, are holy "juxta solam adhuc praedestinationem. Latet ergo
  hujusmodi sanctitas penes Deum".
- **Sicard** (3.1): the Lesson "de numero signatorum" fits the feast, with the
  Gospel "de numero beatitudinum".
- **Schuster** (3.1) on the Lesson.
- **Caesarius of Arles** (handoff STU-001). No holding of Caesarius's
  Apocalypse homilies under his name was found in the library or the discover
  output; the PL 35 *Expositio* is the text sometimes given to him and is
  recorded above as anonymous. Negative for a separately held Caesarius.
- The negatives for this passage are in 3.0.

### 3.5 Gradual: Ps 33:10-11

Read in context: Ps 33 whole (title: David before Achimelech; v. 8 the angel of
the Lord; v. 12 *Venite, filii*, not said).

- **St Augustine, *Enarr. in Ps.* 33, sermo 2 nn. 11-15 and 19** (Migne Latin,
  `…latin-migne-corpus-corporum-wikisource-web-2026-09-05.wikisource-part-4-latin-text`,
  physical line 34; text-read). n. 14 on v. 10: *Timete Dominum, omnes sancti
  ejus, quoniam nihil deest timentibus eum*: Augustine's psalter reads *nihil
  deest* here as the Gradual does. On v. 11 it reads *Divites eguerunt et
  esurierunt, inquirentes autem Dominum non minuentur omni bono*: "Si ad
  litteram accipias, videtur te fallere"; n. 15, the goods are spiritual ("in
  bonis spiritualibus"), the rich lack the bread "Ego sum panis vivus", with Mt
  5:6. That comment is on the half-verse the Gradual omits. n. 11 (on v. 8, not
  said): the angel of the Lord is Christ, *magni consilii Angelus*. n. 19:
  peace sought here and perfected at the end ("ex parte hic … ex toto illic"),
  on v. 15, which the Mass does not say.
- **St Basil, *Homilia in Psalmum XXXIII* nn. 6-7** (PG 29, 1860, facsimile
  `…patrologia-graeca-volume-29.1860-paris.commons-pdf-53d21baf`, fetched whole
  2026-10-27 and matched, 95,465,952 bytes; PDF pp. 591-592 = cols. 366C-367C,
  the Latin column image-read at 300 dpi; tracked text layer
  `full-text-layer-2898b217`, lines 40776-40870). On v. 10: unless fear trains
  our life, holiness in the body cannot be achieved (Ps 118:120, "Confige
  timore tuo carnes meas"); "Timenti itaque non est inopia; hoc est, qui per
  timorem ab omni indecora et absurda actione arcetur, ei nihil deest ad
  quamlibet virtutem, sed perfectus est, nullo bono humanae naturae convenienti
  destitutus"; whoever despises one commandment is imperfect in that. On v. 11:
  the word teaches contempt of bodily riches; or the rich are Israel (Rom
  9:4-5), who, having killed the Bread of life, suffer the famine of hearing
  the word; those from the nations who seek the Lord "non minuentur omni bono.
  Perfectum omnino bonum Deus ipse est, quo non minuentur quotquot exquirunt
  ipsum". The goods are not bodily: else the apostles, who sought the Lord and
  lacked bodily goods, would make Scripture false; "Paulus utique et
  inquirebat Dominum, et nihil ei defuit bonorum", though scourged, stoned and
  shipwrecked. The preceding lines (on v. 9, not said) join *Gustate* to Mt
  5:6.
- **St Thomas Aquinas, *Super Psalmos* 33 nn. 10-11** (Parma vol. 14, 1863,
  `…opera-omnia-volume-14.1863-parma.ia-complete-ocr-02c6dc25`, lines
  42600-42670, printed pp. 206-207; text-read). n. 10: "Timete … sancti, quia
  nullus potest esse sanctus nisi sit timens"; fear is needed by those who
  remain in holiness. *Non est inopia* (his psalter) expounded three ways:
  spiritually (the treasure of Isa 33:6), of bodily want (the content man,
  Phil 4), and "Item Deus quaerentibus se subvenit in necessitate". He raises
  the objection of 1 Cor 4:11 (the apostles hungered) and answers that God, as
  a physician, withholds. n. 11: *Divites eguerunt* read spiritually (Apoc
  3:17).
- **St Robert Bellarmine, *Commentary on the Psalms*** (O'Sullivan's English,
  `…historical-text-357551e1`, lines 1201 and 1203; text-read): to feel no
  want "is the essence of perfection"; a humbler sense of temporal supply is
  kept; "as they cling to the Supreme Good, they possess all that is good". He
  says nothing of the vision of God or of the Communion.
- **St Bernard, sermo 5 n. 3** (PL 183 cols. 476-477, image-read at col. 477):
  "Cantavimus sanctis hac nocte, dicentes: Timete Dominum, omnes sancti ejus;
  sed non istis", that is, not to the saints in glory, who no longer fear;
  "merito his dicatur … Tota interim beatitudo nostra est timere Deum"; "Nostra
  ergo felicitas, nostra interim festivitas, in timore Dei: nam illorum magis
  in exsultatione et laude versatur." *Hac nocte*: Bernard speaks of the verse
  as sung in the night office of the feast, not of the Mass Gradual. He is
  cited as reception of the verse the Gradual shares, and he does not say to
  whom the Mass Gradual is addressed.
- **Schuster** (3.1) gives only the Gradual's earlier use.
- **The psalter form.** No psalter read carries the whole Gradual: Augustine
  agrees at v. 10 (*nihil deest*) and not at v. 11 (*non minuentur*); Basil's
  Latin translator, Aquinas and the Clementine read *non est inopia* and *non
  minuentur*. The chant form itself is older than the printings read: the
  Sarum Missal's common of many martyrs (Legg pp. 366-367, OCR) has an Introit
  *Timete dominum … nichil deest timentibus eum … non deficient omni bono*
  (lines 29775-29777) and a Gradual *Timete dominum … quoniam nichil deest
  timentibus eum. V. Inquirentes autem dominum non deficient omni bono* (lines
  29903-29905), the 1962 respond and verse. The psalter from which *non
  deficient* comes is still unidentified.

### 3.6 Alleluia: Mt 11:28

Read in context: Mt 11:20-30.

- **St John Chrysostom, *Hom. in Matt.* 38.3** (NPNF I.10,
  `ccel-text-adb8f1c9`, lines 23880-23960; text-read). The invitation is "not
  this or that person, but all that are in anxiety, in sorrows, in sins";
  meekness and lowliness are "the mother of all strictness of life. Wherefore
  also, when beginning those divine laws, with this He began", that is, with
  the Beatitudes; "Even before the things to come, He gives thee here thy
  recompense"; "Come, ye that labor and are heavy laden" implies "that sin too
  hath labor, and a burden".
- **St Hilary of Poitiers, *In Matthaeum* XI n. 15** (PL 9, IA text
  `ia-djvu-text-db389fea`, lines 77911-77919; image-read on the remote scan
  of the volume, PDF p. 506 = cols. 983-984, col. 984). Under the edition's
  summary heading "Jugum Christi unde suave": "Legis deinde difficultatibus
  laborantes, et peccatis saeculi oneratos ad se advocat: dempturumque se
  laborem onusque
  promittit, si modo ejus jugum tollant, mandatorum scilicet suorum praecepta
  suscipiant, eumque sacramento crucis adeant: quia corde humilis et mitis
  sit". The inference: the labour is the Law's difficulty and the burden the
  world's sins; the yoke taken is his commandments, and he is approached by
  the sacrament of the cross.
- **St Augustine, Sermons XIX and XX [LXIX and LXX Ben.]**, both on Mt 11:28
  (NPNF I.6, `ccel-text-ce371798`; text-read; the heading of Sermon XIX
  prints "Matt. xix. 28" for xi). Sermon XIX n. 1 (lines 30144-30160): "For
  why do we labour all, except that we are mortal men, frail creatures and
  infirm, bearing about vessels of clay"; "What then does He mean by, 'Come
  unto Me, all ye that labour,' but that ye may labour no more?"; n. 2
  (30162-30169): "learn of Me … 'that I am meek and lowly in heart.' Thou
  wishest to be great, begin from the least … first think of the foundation
  of humility". Sermon XX (lines 30299-30389): the yoke is easy to those who
  love; the inner man, "placed no longer under the Law but under Grace, and
  freed from the burdens of numberless observances which were indeed a heavy
  yoke", bears every outward trouble lightly through the joy within
  (30382-30389). In Sermon XXI [LXXI Ben.] n. 11 he uses the verse: the Jews
  were "full of and laden with sins … Laden! with what, but with the burdens
  of sins and transgressions of the Law?" (30706-30708). The inference: the
  labour is the common lot of frail mortals, and the rest promised begins
  with humility as a foundation.
- **Rabanus Maurus, *Expositio in Matthaeum* IV** (PL 107, IA text
  `ia-djvu-text-5b8a4b8b`, lines 101134-101141; image-read on the remote scan
  of the volume, PDF p. 462, col. 916). "Gravia onera esse peccati et
  Zacharias propheta testatur, dicens iniquitatem sedere super talentum
  plumbi (Zach. V): Et Psalmista complorat: Iniquitates meae aggravatae sunt
  super me (Psal. XXXVII). Vel certe eos qui jugo legis gravissimo
  premebantur ad Evangelii invitat gratiam." The comment on 11:27 just before
  it is taken from Hilary. The inference: the burden is sin, or else the
  Law's yoke, from which the call is to grace. On the page the comment
  carries no source label of its own (the tracked excerpt, col. 916). It is
  Jerome's comment on the verse, taken over nearly word for word (next
  entry), and a sentence of the comment on 11:27 before it, on Eunomius, is
  Jerome's too (Rabanus reads *jactans* where Jerome has *vendicans*).
- **St Jerome, *In Matthaeum* II, on Mt 11:28-29** (PL 26, Paris 1845; the
  remote scan `…patrologia-latina-volume-26.paris-1845.internet-archive-google-pdf-0d889bd6`,
  fetched whole and matched to its registered SHA-256, PDF p. 45, col. 75;
  image-read; no tracked text layer; the page is retained as the tracked
  excerpt `…paris-1845.columns-75-76-facsimile-b432adc8`). "Gravia onera esse peccati, et
  Zacharias propheta testatur, dicens, iniquitatem sedere super talentum
  plumbi (Zach. v). Et Psalmista complorat: Iniquitates meae aggravatae sunt
  super me (Psal. xxxvii, 6). Vel certe eos qui gravissimo Legis jugo
  premebantur, ad Evangelii invitat gratiam." Rabanus differs only in the
  order *jugo legis gravissimo*. The inference recorded for Rabanus above is
  Jerome's first: the burden is sin, or else the Law's yoke, from which the call is
  to the Gospel's grace; he gives both and does not choose.
- **St Gregory the Great, *Moralia* I n. 24, on Job 1:3** (Library of Fathers
  English, `…moralia-in-iob.2026-10-12-library-of-fathers-lectionarycentral.complete-text-d9f9ed86`,
  lines 1121-1130; text-read). Those of Judaea "were weighed down with the
  heavy yoke of the Law, because they were burthened with the ordinances of
  the external letter", and to them the verse is spoken; rest "is promised to
  those that labour well". A use with an inference, not a commentary.
- **St Thomas Aquinas, *ST* I-II q. 107 a. 4, *sed contra*** (English
  Dominican translation, Gutenberg
  `…2006-english-dominicans-gutenberg-prima-secundae.pg17897-body-6d5b93fb`,
  lines 49939-49945; text-read): the New Law is a lighter burden than the Old,
  because of the verse "expounded by Hilary thus: 'He calls to Himself all
  those that labor under the difficulty of observing the Law, and are
  burdened with the sins of this world'", with "My yoke is sweet". Aquinas
  reports Hilary's sentence and makes it the ground of a comparison of the
  two Laws.
- **Schuster** (3.1): the verse prepares for the Gospel.
- **Bound.** The held, unread and searched witnesses are in 3.0.

### 3.7 Gospel: Mt 5:1-12a

Read in context: Mt 4:23-5:16.

- **St Augustine, *De sermone Domini in monte* I.3.10-I.4.12** (NPNF I.6,
  `ccel-text-ce371798`, lines 932-1074: I.3.10 at 932-990, chapter IV and
  I.4.11 at 1002-1039, I.4.12 at 1041-1074; text-read). I.3.10: the
  beatitudes in order from humility, as seven stages (949-979); "The eighth,
  as it were, returns to the starting-point, because it shows and commends
  what is complete and perfect" (979-981), so that the kingdom of heaven is
  named in the first and the eighth. I.4.11: the seven stages matched to the
  seven gifts of Isa 11:2-3, in reverse order, beginning from the fear of
  God. I.4.12: the one reward variously named; "This eighth sentence, which
  goes back to the starting-point, and makes manifest the perfect man"
  (1069-1071), with the eighth day of circumcision and of the resurrection.
  Iteration 1 placed the starting-point sentence in I.4.12; the words quoted
  above stand in I.3.10, and I.4.12 repeats the thought. Of the
  promises (lines 1064-1068): "And those promises can indeed be fulfilled in
  this life, as we believe them to have been fulfilled in the case of the
  apostles. For that all-embracing change into the angelic form, which is
  promised after this life, cannot be explained in any words."
- **St John Chrysostom, *Hom. in Matt.* 15** (NPNF I.10, lines 8742-9127;
  text-read). The mourners are comforted "both here and there" (8928); the
  ladder of the beatitudes (8988-8995); on the peacemakers and the persecuted
  (9103-9127).
- **St Hilary of Poitiers, *In Matthaeum* IV nn. 1-9** (PL 9, IA text
  `ia-djvu-text-db389fea`, lines about 73730-73870, cols. about 933-935;
  text-read). n. 1: "in paternae scilicet majestatis positus celsitudine,
  caelestis vitae praecepta constituit. Non enim aeternitatis instituta, nisi
  in aeternitate positus, tradidisset"; n. 3: the earth the meek inherit is
  Christ's assumed body, "claritate clarificati ejus corporis vestiemur"; nn.
  4-5: consolation and satiety "in caelo"; n. 7 (col. 935): "Non enim nisi
  spiritu perfecti, et immortalitate immutati … hoc quod in Deo est immortale
  cernemus"; n. 9: the persecuted as "gloriosi promissorum Dei martyres".
- **St Thomas Aquinas, *Super Matthaeum* c. 5 lect. 2** (Corpus Thomisticum,
  `…1951-turin-corpusthomisticum-web-2026-10-26.cma0500-a73c7d72`, paragraph
  [87340] and following, fetched whole and matched; and the Venice printing of
  1745, tom. 3,
  `…opera-editio-altera-veneta-tomus-3.venice-bettinelli-1745.internet-archive-google-pdf-adb333e0`,
  fetched whole and matched, 56,148,876 bytes: PDF p. 85 = printed p. 67 col.
  a, and PDF p. 90 = printed p. 72, image-read). The rewards are given in the
  way (*in via*) as a beginning (*inchoationem*) and in the homeland (*in
  patria*) perfectly (p. 67); peace "hic inchoatur" (p. 72, on 5:9); the eight
  rewards are "unum praemium" under different names; on the eighth he reports
  Chrysostom: "Non dicit a paganis" (p. 72), that is, persecution suffered for
  justice and not only from pagans. The Leonine text at Corpus Thomisticum
  (`…1969-leonine-corpusthomisticum-web-2026-10-26.cma0510-86c3a4eb`, paragraph
  [87564], fetched whole and matched; text-read) gives the same report on 5:10
  and adds that the kingdom is promised to the poor in hope and to the martyrs
  in fact. The Venice printing prints no lecture
  number near the locus; the lecture number is Corpus Thomisticum's.
- **St Bernard, *In festo omnium Sanctorum* sermo 1, on Mt 5:1-12** (PL 183
  cols. 453-462). n. 9 (col. 457, OCR): a lesser kingdom given "velut in
  arrham", with 1 Tim 4:8; n. 13 (col. 461, image-read): "Videbunt quidem in
  fine facie ad faciem; videbunt etiam nunc, sed per speculum in aenigmate";
  n. 14 (col. 461, image-read): in the first three the soul is reconciled to
  itself, in the next two to its neighbour, in the sixth to God, in the
  seventh it reconciles others; n. 15 (col. 462, image-read): "octava
  beatitudo, martyrum est praerogativa"; the same promise is made to the poor
  and to the martyrs "quia vere martyrii genus paupertas voluntaria est …
  paupertate quidem emitur, sed in passione pro Christo absque omni dilatione
  percipitur".
- **Rabanus Maurus, *Expositio in Matthaeum* II, on Mt 5:1-12** (PL 107, IA
  text `ia-djvu-text-5b8a4b8b`, lines about 91700-92080, cols. about
  794-798; OCR, with the loci below image-read on the remote scan, PDF pp.
  402-403 = cols. 796-797). A compilation that names its sources in
  parenthetical labels set in the running text, such as "(Hieron.)",
  "(Aug.)" and "(MAURUS.)" for his own words (the tracked excerpt, col. 795
  and following); not every comment carries one. The poor in
  spirit are the humble and those fearing God, and "Initium autem sapientiae
  timor Domini", against pride, the beginning of every sin (lines
  91773-91783, from Augustine). On 5:8, after Augustine, in his own words
  (labelled "(MAURUS.)", lines 91869-91872, col. 796, image-read): "Dominum enim mundi
  corde vident hic in aenigmate per gratiam, in futuro autem facie ad faciem"
  (1 Cor 13:12). On 5:9-10 (lines 92066-92077; OCR, badly garbled, given in
  paraphrase) he takes over Augustine's sentence that these promises can be
  fulfilled in this life, as in the apostles, and that the eighth goes back
  to the start, with the eighth day of circumcision and of the resurrection.
  On the Lord's Prayer (lines 93916-93937, col. about 822; image-read on PDF
  p. 415) he repeats Augustine's matching of the seven petitions to the
  seven beatitudes and gifts (*De sermone Domini* II.11.38): "Si enim timor
  Dei est, quo beati sunt pauperes spiritu … petamus ut sanctificetur in
  hominibus nomen Dei, timore casto permanente in saeculum saeculi". The
  inference is Augustine's: the rewards are begun here, by grace and in a
  mirror, and completed hereafter.
- **Sicard** (3.1): the Gospel "de numero beatitudinum" fits the feast with the
  Lesson "de numero signatorum".
- **Bound.** Gregory of Nyssa, *De beatitudinibus*: no holding. The other held,
  unread and searched witnesses are in 3.0.

### 3.8 Offertory: Wis 3:1-3 as adapted

Read in context: Wis 2:21-3:9 (Douay and Clementine). Wis 2:21 (Douay) says of
the wicked that "their own malice blinded them"; this is an editorial
observation on the context, not a source for the antiphon's *malitiae*. The
antiphon omits 3:2b-3a (*et æstimata est afflictio exitus illorum: et quod a
nobis est iter, exterminium*), the unwise men's judgement of the departure.

The search that was made, and what it found, is in 3.0 (Wis 3:1-3). The index
maps no commentary to the passage; literal search and the catalogue found one
direct commentary on Wisdom, one patristic gloss of the verse, one saintly
exposition built on it, and several uses.

- **St Bonaventure, *Commentarius in librum Sapientiae* c. 3** (Quaracchi
  *Opera omnia* vol. 6, 1893, tracked OCR
  `…bonaventure.opera-omnia-quaracchi.1893-volume-6.ia-djvu-ocr-e7f54e11`,
  lines 22902-23082, printed pp. 125-126, the page header "126" at line 23034;
  OCR, normalized; the lemma *Iustorum* is recognized as *lustorum*). He
  divides 3:1-3 as the just's deliverance from eternal damnation, from the evil
  of temporal death and from present tribulation. On v. 1 the souls are "id est
  Martyrum, secundum Glossam; quod etiam verum est de aliis iustis, sed
  Martyres dicuntur specialiter iusti"; "animae; non dicit corpora", for the
  body is given into the hands of the wicked (Job 9:24); "in manu Dei sunt, id
  est in protectione, et ideo sunt securae", with Ps 90:1 and Jn 10:28; the
  *tormentum mortis* is eternal death, "ut dicit Glossa", "quia illa est vera
  mors; temporalis autem est quasi umbra mortis; est enim quidam transitus ad
  vitam" (Jn 5:24). On v. 2 the unbelievers judge the death of the saints to be
  eternal, "cum tamen transeant ad vitam meliorem", with Augustine (*De civ.
  Dei* XIII.4) that death has become the instrument by which one passes to
  life; to the eyes of the wise they seem to be born, "propter quod obitus
  Sanctorum vocatur natale". On the omitted 3:2b-3a he reports the *Glossa*:
  the unwise "palmam martyrii afflictionem putant et exterminium". On *illi
  autem sunt in pace*: "Glossa: Perpetuae quietis, nunc in spe, tandem in re",
  with Apoc 14:13 and Isa 32:17, "Terminus enim iustorum est pax". The
  inference: the verse is said first of the martyrs and truly of all the just;
  God's hand is his protection of the soul; the death the just escape is
  eternal death, and the peace they have is had now in hope and at last in
  fact. The *Glossa* and Rabanus Maurus are read here only as he reports them;
  the editors' note gives the interlinear gloss on *mortis* as "perpetuae
  mortis" under Rabanus's name. Bonaventure has no standing row: he supports.
- **St Augustine, *Enarr. in Ps.* 87 n. 5** (Migne Latin,
  `…latin-migne-corpus-corporum-wikisource-web-2026-09-05.wikisource-part-9-latin-text`,
  physical line 134; text-read). On Ps 87:6, *et ipsi expulsi sunt de manu
  tua*: the words are not to be referred to the dead sleeping in the
  sepulchre, "cum sint in eis justi …; de his tamen dictum est, Justorum animae
  in manu Dei sunt (Sap. III, 1), hoc est, habitant in adjutorio Altissimi, et
  in protectione Dei coeli commorantur (Psal. XC, 1). Sed illi expulsi sunt de
  manu Dei, qui Dominum Christum de manu ejus expulsum esse crediderunt". The
  inference: to be in God's hand is to dwell under his help and protection, and
  it is said of the just dead before their resurrection; those who thought
  Christ cast out of God's hand are the ones cast out. Augustine and
  Bonaventure gloss *in manu Dei* the same way, by Ps 90:1.
- **St Alphonsus Liguori, *Preparation for Death*, Ninth Consideration**
  (Duffy, Dublin 1843, tracked OCR
  `…alphonsus-liguori.apparecchio-alla-morte.duffy-1843.historical-ocr-d25bba22`,
  lines 5480-5686, printed pp. 117-122; OCR). The consideration is headed by Wis
  3:1-3 quoted with the same omission as the antiphon: "In the sight of the
  unwise they seemed to die;....but they are in peace" (lines 5483-5485; the
  omission is his, and nothing read says he took it from the Offertory). First
  point (5491-5608): "If God holds fast in his hands the souls of the just, who
  can snatch them from him?"; hell tempts the saints at the hour of death, but
  God multiplies his help where the danger is greater, and the guardian angel,
  St Michael, the divine Mother and Christ come to the dying. Second point
  (5655-5686): "In the eyes of the unwise the servants of God appear to die, as
  worldlings do, in sorrow and with reluctance", but God gives them foretastes
  of Paradise, and "the saints … begin to feel that peace which they shall
  afterwards fully enjoy in Heaven. To the saints death is not a punishment,
  but a reward." The inference: the verse is said of the death of every just
  soul, and its peace begins before death. Alphonsus has no standing row: he
  supports and does not carry.
- **How Alphonsus differs from Schuster.** Schuster (3.1) reads the antiphon of
  the martyrs and their persecutor, who thinks their lives are in his hands.
  Alphonsus reads it of the ordinary death of every just soul, whose enemy is
  the devil's last temptation, and places the beginning of the peace before
  death. Bonaventure holds both: the martyrs first, and "verum … de aliis
  iustis". What the difference changes: on Schuster's reading the Offertory
  names the martyrs among the saints of the feast; on Alphonsus's it names
  every saint's death, and with Bonaventure's "nunc in spe, tandem in re" it
  bears on Reading B's peace begun here and finished there (5.5).
- **Liturgical commentators.** Fromage (3.1, lines 8427-8442): the Beatitudes
  raise man above torments and above death itself, "qui n'ébranle pas la paix
  des justes, mais la consomme. C'est ce que chante l'Offertoire". He joins
  the antiphon to the Gospel just read. Schuster: the martyrs and the
  persecutor (3.1).
- **Illuminating uses, read at their loci** (none expounds the verse, and no
  reading rests on them):
  - St John Chrysostom, *Hom. in Matt.* 28 n. 3 (NPNF I.10,
    `ccel-text-adb8f1c9`, lines 18096-18100; text-read): a soul torn from the
    body cannot wander here, "For 'the souls of the righteous are in the hand
    of God;' and if of the righteous, then those children's souls also"; the
    souls of sinners too are straightway led away. He uses the verse for the
    state of souls after death.
  - St Gregory the Great, *Moralia* XII n. 6 (Library of Fathers text,
    `complete-text-d9f9ed86`, lines 19547-19557; text-read): the stock of the
    righteous dies in the dust "in that amidst the hands of the persecutors his
    body is bereft of life; for according to the words of Wisdom, In the sight
    of the unwise they seemed to die, and their departure is taken for misery
    [Wisd. 3, 2]". He applies the verse to the martyr's body, and he quotes
    3:2b, which the antiphon omits.
  - St Bernard, *In transitu S. Malachiae* sermo 2 n. 5 (PL 183 OCR,
    `ia-djvu-text-44995734`, line 43611): "Nimirum visus est oculis
    insipientium mori, ille autem est in pace", of Malachy, now "concivis
    sanctorum et domesticus Dei".
- **The wording's history** (text layers of registered printings, OCR only,
  except Mame read on images):
  - Venice 1570 (`…venice-1570.missale-romanum-1570-text-563f4dd2`, lines
    71698-71701): *tormentum mortis*, no *alleluia*;
  - Rome 1604 (`…vatican-typica-1604.missale-romanum-1604-text-6d12feef`,
    lines 53515-53525): *malitiae*, no *alleluia*;
  - Ratisbon 1862 (`…pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`,
    lines about 77748-77753) and Tournai 1889
    (`…1889-tournai-desclee-leo-xiii-recognitum.ia-djvu-ocr-715f57fd`):
    *malitiae*, no *alleluia*;
  - Fromage, 1909 (lines 8437-8442): *malitiae*, no *alleluia*;
  - the scanned printing registered under the 1920 typical edition
    (`…vatican-typica-1920.missale-romanum-1920-text-aa646196`, fetched whole
    and matched, 2,918,085 bytes, lines 95336-95341): *malitiae* and
    *alleluja*. Iteration 1 dated this witness 1920. Its own artifact and
    edition records say otherwise: the body of the scanned book is a printing
    of 1951-1954 (the Assumption Mass *Signum magnum* of 1950 is in it, with
    the octave abolished in 1955), and its appendix is of 1970 or later. It
    is a late printing of the 1920 text, and it cannot date a 1920 reading;
  - Tours 1922 (Mame, image-read), a printing *iuxta typicam* of the 1920
    edition: *malitiae* and *allelúja*.
  - **Chant books before the printed Missals.** The Gregorian Antiphonary in
    PL 78 (OCR) gives the chant *Justorum animae in manu Dei sunt, et non
    tanget illos tormentum malitiae. Visi sunt oculis insipientium mori, illi
    autem sunt in pace* as a Communion (lines 60300-60302, 60791-60793; the
    incipit at 61121), as a Gradual with the verse *Visi sunt oculis* (60310,
    60865-60867, 61118), and in the Responsale as a Lauds antiphon (72714-72715)
    and a responsory verse (72589-72590), all with *malitiae*. One antiphon in
    the Responsale reads *tormentum mortis. In pace sunt ea quae possident,
    allel.* (72812-72814). The excerpts from the Fonte Avellana liturgical
    codices printed in PL 151 (OCR) have the chant with *malitiae* as a
    Gradual followed by *Alleluia* (70850-70853) and as a Communion (70875-70877,
    73693-73694). Aquinas, *In Ps.* 17, quotes the verse with *malitiae*
    (Parma vol. 14, line 31719, which the OCR reads *lormentum maliiiae*; a
    use). None is the All Saints Offertory, which these
    books do not give.
  - **The form *malitiae* is older than the 1570 printing.** The Sarum Missal
    (Legg 1916, OCR), *In natali plurimorum martyrum*, has the chant as an
    alternative Gradual, *Iustorum anime in manu dei sunt et non tanget illos
    tormentum malicie. V. Uisi sunt oculis insipiencium mori illi autem sunt
    in pace* (lines 29907-29909), and as a Communion, with *alleluia* only in
    paschal time (lines 30178-30182); both have the antiphon's omission. Its
    lesson from Wisdom (*Sap. iii. 1-8*, lines 29793-29796) reads *tormentum
    mortis*. Peter of Celle, printed in PL 202 (the John Beleth artifact
    `ia-djvu-ocr-22b781bf`; OCR), quotes the verse both ways: *malitiae* at
    lines 51129-51133 (the OCR reads *talitie*, corrected by the next line,
    "Tormentum malitiae est passio carnis, elatio cordis, tentatio hostis")
    and at 80754-80756, and *mortis* at 69179-69181. So the chant read
    *malitiae* where the Bible read *mortis*, and the 1570 printing's *mortis*
    is the departure, not the 1604 printing's *malitiae*. The printings read do
    not show why 1570 differs. Peter of Celle's gloss on *tormentum malitiae*
    is a use, not a comment on the Offertory.
  - The *alleluia* is absent from the Tournai printing of 1889 and from
    Fromage's 1909 text, and present in the Mame printing of 1922, which is
    conformed to the 1920 typical edition. The earliest dated witness read
    that has it is therefore 1922. The 1920 typical edition itself was not
    read (the only scan held is the late printing above), so this research
    does not show that the *alleluia* entered with it. No act or decree for it
    was read. RGMR 478 (research/context.md) governs its use in 1962.
- The 1570 and 1604 Gospels read *maledixerint vobis homines*; 1889 and later
  omit *homines*. Text layers only.

### 3.9 Secret, Postcommunion and the commemoration's orations

- Schuster (3.1) translates the Secret and Postcommunion and says nothing
  further on them; Bernard (3.3) on veneration. The Secret's *pro cunctorum …
  honore iustorum* has no commentator read. Ménard's Gregorian Sacramentary
  reads *honore sanctorum*; the PL 151 sacramentary reads *honore justorum*,
  as 1962 does (3.1). The Postcommunion stands in both (3.3).
- The three Sunday orations: no commentator read; their Pustet collation is
  in propers/verified.md.

### 3.10 Communion: Mt 5:8-10

- Fromage (3.1) gives the one reason read for the choice of three beatitudes.
- Augustine I.3.10 (the eighth returns to the starting-point, commending what
  is complete and perfect, a thought I.4.12 repeats), Rabanus on 5:8 (God
  seen "hic in aenigmate per gratiam, in futuro autem facie ad faciem"), Bernard sermo 1 nn. 13-15 (seeing now in a mirror; the
  reconciliations; the eighth as the martyrs' prerogative) and Hilary IV nn.
  7-9 read the three verses as part of the Gospel (3.7); none of them comments on the
  Communion antiphon as such.

### 3.11 Preface

The 1962 rubrics read (RGMR 482, 483, 494 b, 498) and the dated ordos are in
research/context.md. This iteration adds the governing edition's closest
direction and the contrast in wording among the Preface rubrics.

- **The Missal's own closest direction.** In the Vigil of the Nativity, printed
  p. 16 (PDF 97), after the Secret no. 105, the 1962 Missal directs:
  "Praefatio communis; sed, si venerit in dominica, dicitur de Ss.ma
  Trinitate." (page image read; the facsimile's text layer, extracted for this
  run from `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`,
  line 5653). The Vigil is a first-class Mass that is not the Sunday's own. A
  search of the same text layer for `venerit in dominica` and for `Praefatio
  communis` (nine hits, each read) found no other Preface direction that
  depends on the Mass falling on a Sunday. The other hits are the common
  Preface's own headings, directions for a Sunday's Mass resumed on weekdays
  (after the Epiphany; the First Sunday after Pentecost), and directions for
  other Masses (Corpus Christi; the vigils of SS Peter and Paul and of the
  Assumption), none of them conditioned on a Sunday.
- **The contrast in wording among the Preface rubrics** (RGMR, printed p.
  XXXIV, PDF 32, read on the text layer, lines 1820-1842). The seasonal
  Prefaces are given *tamquam de Tempore* to other Masses in express words:
  486 b (Lent), 489 b (Easter) and 493 b (Pentecost), "in ceteris Missis quae
  celebrantur eodem tempore, et praefatione propria carent"; 487 b (Passiontide)
  and 490 b (Ascension), "in omnibus Missis … quae praefatione propria carent".
  494 b says only "tamquam de Tempore in dominicis Adventus, et in omnibus
  dominicis II classis, extra tempus natalicium et paschale". It does not say
  "in Missis quae … praefatione propria carent".
- **Two inferences from the p. 16 direction.**
  1. *As an application of 482 and 494 b.* A Mass without its own Preface said
     on a Sunday takes the Preface *de Tempore* of that Sunday (482, *qua
     deficiente, dicitur praefatio de Tempore*), which is the Trinity (494 b).
     The direction then states what the general rubrics already give, and the
     same reasoning gives the Trinity Preface to All Saints on a Sunday:
     candidate 1.
  2. *As a special exception.* The seasonal rubrics extend their Prefaces to
     other Masses in words that 494 b lacks; 494 b assigns the Trinity Preface
     to Sundays, not to other Masses said on them; and the Missal printed the
     Vigil's case expressly because the general rubrics did not reach it.
     Without such a direction a feast that takes the Sunday keeps the common
     Preface (483, 498): candidate 2.
  - An observation of this record, not a rubric: the Vigil can meet only the
    Fourth Sunday of Advent, which 494 b names in its own clause (*in dominicis
    Adventus*). The Twenty-third Sunday after Pentecost falls under the other
    clause (*in omnibus dominicis II classis*). The analogy reaches All Saints
    only if both clauses work the same way.
- **The ICRSP Ordo** for 1 November 2026 directs the Trinity Preface
  (research/context.md). That is one institute's direction, not a rubric of the
  Missal; the FSSPX texts and day page name no Preface.
- **Disposition: unresolved; both candidates kept.** The p. 16 direction
  supports either inference, and nothing read decides between them.
  propers/verified.md element 11 records both candidates with this evidence.
  Searched, not found: no registered rubrical commentary read treats a
  first-class feast that takes a second-class Sunday. Murphy 1960 was not
  re-read and is not relied on.

## 4. Witness register

Standing is the `standing` value of
`src/sources/inventories/author-standing-v1.toml` where a row exists; "no row"
means the author has no standing row and cannot carry a reading.

| Author | Work, locus | Standing | Use | State |
|---|---|---|---|---|
| Augustine of Hippo | *De serm. Dom.* I.3.10-I.4.12; *Enarr. in Ps.* 32 (en. 1; en. 2 s. 1, on v. 1), 33 s. 2 nn. 11-15, 19, 87 n. 5; *Ench.* 29; Sermon LXI; Sermons XIX-XX [LXIX-LXX Ben.] on Mt 11:28, and XXI [LXXI] n. 11 | father | carries A (Sermon LXI, *Ench.* 29), B (with Sermons XIX-XX), C (Ps 32, 33, 87); supports C (Sermon XIX) | text-read |
| John Chrysostom | *Hom. in Matt.* 15; 38.3; 28 n. 3 | father | carries B; supports A, C; illuminates the Offertory (28 n. 3) | text-read |
| Hilary of Poitiers | *In Matt.* IV nn. 1-9; XI n. 15 | father | carries B | text-read (OCR); image-read (XI n. 15, col. 984) |
| Thomas Aquinas | *Super Matt.* 5 lect. 2; *In Ps.* 32 and 33 nn. 10-11; *ST* I q. 23 a. 7; I-II q. 107 a. 4 (reporting Hilary) | doctor | carries B, C; supports A | image-read (Venice); text-read; OCR (Parma) |
| Basil of Caesarea | *Hom. in Ps.* 32 n. 1; 33 nn. 6-7 | father | carries C; supports B | OCR (Ps 32); image-read, Latin column (Ps 33) |
| Robert Bellarmine | *In Ps.* 32:1; 33:10-11 | doctor | carries C | text-read (abridged English) |
| Bede | *Explanatio Apocalypsis* on 7:1-12 | father | carries A | image-read |
| Gregory the Great | *Hom. in Ev.* 34 n. 11; *Moralia* I n. 24 (Mt 11:28), XII n. 6 | father | supports A, B (*Moralia* I); illuminates the Offertory (*Moralia* XII) | text-read |
| Rabanus Maurus | *Expositio in Matt.* II on 5:1-12 and on the Lord's Prayer; IV on 11:28 (Jerome's comment taken over) | saint | carries B | image-read at the loci quoted (cols. 796, about 822, 916); OCR elsewhere |
| Jerome | *In Matt.* II on 11:28-29 | father | supports B (the source of Rabanus's comment, 3.6) | image-read (PL 26 col. 75) |
| Cyprian | *Ad Fortunatum* 11 | no row | supports A; with Schuster in 6.2 | text-read |
| Victorinus of Pettau | *In Apoc.* on 7:2-9, 12:6 | no row | supports A | text-read (recension uncertain) |
| Bernard of Clairvaux | *In festo omnium Sanctorum* sermones 1, 2, 5; *In transitu S. Malachiae* s. 2 n. 5 | no row | supports A, B, C; illuminates the Offertory (Malachy) | image-read at the loci marked; OCR |
| Bonaventure | *Comm. in Sap.* c. 3 vv. 1-3 | no row | supports B, C | OCR |
| Alphonsus Liguori | *Preparation for Death*, Ninth Consideration | no row | supports B, C | OCR (English, 1843) |
| Anonymous (PL 35 appendix) | *Expositio in Apoc.* hom. 6 | not an author row | supports A | image-read |
| Alfredo Ildefonso Schuster | *Sacramentary* V pp. 208-212 | blessed | element notes; supports A (6.2), C (Offertory) | image-read p. 210 |
| William Durandus | *Rationale* VII.34 | ecclesiastical-writer | history of the feast; the Collect (limited, 3.3) | text-read (OCR) |
| John Beleth | *Summa* c. 127 | ecclesiastical-writer | history of the feast | text-read (OCR) |
| Sicard of Cremona | *Mitrale* IX cc. 24, 49, 50 | ecclesiastical-writer | supports A, B (Lesson and Gospel joined) | text-read (OCR) |
| Honorius Augustodunensis | *Gemma animae* III cc. 161, 168 | ecclesiastical-writer | history of the feast | text-read (OCR) |
| Lucien Fromage | in Guéranger vol. 15 | ecclesiastical-writer | supports A (Introit), B (Offertory, Communion) | text-read (OCR) |
| Peter of Celle | uses of Wis 3:1 in PL 202 | no row | the Offertory's wording history only | text-read (OCR) |
| Bruno of Würzburg | *Expositio Psalmorum* on Ps 32:1 (PL 142) | no row | supports A, C (reporting Cassiodorus) | text-read (OCR) |
| Gregorian Sacramentary and Antiphonary (Ménard), PL 78; *Sacramentarium vetus* of Monte Suavicino, PL 151 and the PL 85 appendix | the Mass of All Saints; the chant *Justorum animae* | not author rows | the Collect's and Secret's readings (3.3, 3.9); the Offertory's wording history (3.8) | text-read (OCR) |
| Leonine Sacramentary (Feltoe 1896); Gelasian Sacramentary (Wilson 1894) | the prayer of all the apostles (Feltoe p. 46; Wilson II.xxxiii, p. 183) | not author rows | the wording of the prayer the Collect adapts (3.1, 3.3) | image-read (Feltoe); OCR checked on the page images (Wilson) |
| Gilbertine Missal (Woolley); Sarum Missal (Dickinson); Brightman, *English Rite* II | the Collect of the feast | not author rows | witnesses of *intercessoribus* (3.1, 3.3) | text-read (OCR) |

Bernard, Victorinus, Cyprian, Bonaventure, Alphonsus, Peter of Celle and Bruno
of Würzburg have no standing row, so they support and do not carry. The readings' letters are
research/interpretations.md's: A `sealed-number-uncounted-crowd`, B
`beatitudes-way-of-the-saints`, C `no-want-just-in-gods-hand`.

## 5. Passage-level difficulty tests

### 5.1 The counted and the uncounted (Apoc 7:4 and 7:9)

The words: *audívi númerum signatórum, centum quadragínta quátuor mília* and
*turbam magnam, quam dinumeráre nemo póterat*. Are these two companies or
one? Victorinus: the 144,000 are those who believe at Elias's preaching (12:6),
and the believers of Jews and nations are the multitude; two groups, one
Church at the end. Bede: the number signifies the innumerable multitude of the
whole Church (7:4), and the multitude of 7:9 is first the victors of the last
persecution, then the Gentiles. The PL 35 *Expositio*: "omnis omnino Ecclesia
est". What changes: on Bede's and the *Expositio*'s answer the Lesson shows one
people twice, under a number and beyond number; on Victorinus's, two moments
of salvation history. Neither makes the number countable to us. Augustine
(*Ench.* 29) and Aquinas (*ST* I q. 23 a. 7, with the Missal's Secret) say the
number is known to God; Augustine and Gregory differ on what it completes
(6.1).

A second question rests on the same words: what does the uncounted multitude
show about how many are saved? Two answers were read. Cyprian (*Ad Fortunatum*
11) concludes from 7:9 that no one should think martyrdom hard, "when he sees
that the crowd of martyrs cannot be numbered"; Schuster concludes that "It is
not then so hard to be saved". Augustine (Sermon LXI) reads the same verse
against Lk 13:23-24: the saved are few in comparison of the lost and many in
themselves, "This is the mass of the saints", and the narrow gate still stands.
What changes: on Cyprian's and Schuster's answer the Lesson encourages by its
number; on Augustine's it consoles without relaxing the narrow gate (6.2).

### 5.2 Present or future: the rewards of the beatitudes (Mt 5:3-12a)

The words: *ipsórum est regnum* (vv. 3, 10), future tenses between, and
*merces vestra copiósa est in cælis* (v. 12a). Augustine (I.4.12): "And those
promises can indeed be fulfilled in this life, as we believe them to have been
fulfilled in the case of the apostles. For that all-embracing change into the
angelic form, which is promised after this life, cannot be explained in any
words." Chrysostom (Hom. 15): the mourners are comforted "both here and
there"; and (Hom. 38) "even before the things to come, He gives thee here thy
recompense". Aquinas: rewards begun in the way, perfected in the homeland.
Bernard: a lesser kingdom given as a pledge; vision now in a mirror, then face
to face. Rabanus, in his own words on 5:8: the pure in heart see God "hic in
aenigmate per gratiam, in futuro autem facie ad faciem", and he takes over
Augustine's sentence on the promises fulfilled in this life. Hilary: the rewards belong to heaven, to those changed by immortality
("nisi spiritu perfecti, et immortalitate immutati"). What changes: on the
first group the Gospel describes a life the saints already lived; on Hilary's,
it describes the state they now enjoy. Augustine's second sentence keeps a
consummation after this life that is beyond words, so his difference from
Hilary is one of emphasis (6.3). No witness read holds that the first and
eighth rewards are present and the six between future; that observation, if a
study makes it, is its own.

### 5.3 "Nothing is lacking" (Ps 33:10-11 in the Gradual)

The words: *nihil deest timéntibus eum* and *non defícient omni bono*. Is the
want bodily or spiritual? Augustine: taken literally the verse seems to
deceive; the goods are spiritual (on the half-verse not said). Basil: the
fearer lacks nothing toward any virtue; God is the perfect good; the apostles
lacked bodily goods, so the goods cannot be bodily. Aquinas: spiritually, and
of bodily want (contentment), and God helps those who seek him in necessity;
the apostles' hunger is answered by the physician's withholding. Bellarmine:
perfection is to feel no want, and a humbler temporal sense stands. What
changes: on Basil's and Augustine's reading the Gradual promises the saints
God himself; on Aquinas's and Bellarmine's it also promises providence in
need. Bernard, on the verse as sung in the night office of the feast, raises a
different question: to whom is *Timete* said? Not to the saints in glory, who
no longer fear, but to us. He does not comment on the Mass Gradual.

### 5.4 Why the Communion repeats three beatitudes (Mt 5:8-10)

Fromage: the antiphon cannot list the whole series again, so it recalls the
last three and brings all of them to the Sacrament in which they are
nourished. No other witness read comments on the antiphon. Bernard's
reconciliations (sixth to God, seventh to others) and his eighth as the
martyrs' prerogative give the three verses a sequence of their own; joining
that sequence to the Communion is editorial.

### 5.5 "They seemed to die" (Wis 3:1-3 in the Offertory)

The words: *Iustórum ánimæ in manu Dei sunt*, *non tanget illos torméntum
malítiæ*, *visi sunt óculis insipiéntium mori: illi autem sunt in pace*, with
3:2b-3a omitted and *malitiae* for *mortis*.

- *Whose souls?* Schuster: the martyrs. Bonaventure: the martyrs, after the
  *Glossa*, "quod etiam verum est de aliis iustis". Alphonsus: every just
  soul. Augustine: the just among the dead.
- *What is God's hand?* Augustine and Bonaventure: his help and protection (Ps
  90:1); Bonaventure adds Jn 10:28, and Alphonsus "who can snatch them from
  him?"
- *What torment does not touch them?* Bonaventure (on *mortis*, after the
  *Glossa*): eternal death, temporal death being "quasi umbra mortis". The
  antiphon's *malitiae* is not commented on by any witness read except Peter of
  Celle's use (the torment of malice as passion of the flesh, pride of heart
  and temptation of the enemy), which is not on the Offertory.
- *When is the peace?* Bonaventure, after the *Glossa*: "nunc in spe, tandem
  in re". Alphonsus: begun before death and fully enjoyed in heaven. Fromage:
  death does not shake the peace of the just but consummates it.
- What changes: on Schuster's reading the antiphon names the martyrs; on
  Bonaventure's and Alphonsus's it names every saint, and its peace is begun in
  this life (Reading B) as well as secured in God's hand (Reading C).
- What the omission changes: the antiphon drops the unwise men's judgement
  (*afflictio … exterminium*) and keeps only their appearance and the truth.
  Gregory quotes the omitted 3:2b; Bonaventure expounds it as the unbelievers'
  reckoning; Alphonsus quotes the verses with the same omission. That is a
  textual observation, not evidence of a source.

## 6. Material disagreements

1. **What the number completes.** Augustine (*Ench.* 29): men fill the place of
   the fallen angels, perhaps exceeding it. Gregory (*Hom.* 34.11): as many men
   ascend as elect angels remained. Aquinas: better to say the number is known
   to God alone. Real disagreement; Aquinas does not decide between the first
   two but sets both aside.
2. **Whether the Lesson's multitude shows that salvation is easily reached.**
   On one side, Cyprian (*Ad Fortunatum* 11): martyrdom is not hard, because
   the martyrs cannot be numbered; his conclusion is limited to martyrdom, and
   it is the ancient precedent read for Schuster's. Schuster: "It is not then
   so hard to be saved, as St John writes that he could not count the number
   of the elect." On the other, Augustine (Sermon LXI): the saved are few in
   comparison of the lost and many in themselves, "many in the society of the
   Angels", as Apoc 7:9 shows, and the narrow gate of Lk 13:24 still stands.
   What each changes: Cyprian and Schuster make the multitude an argument from
   number to ease; Augustine makes it a consolation that leaves the effort of
   the narrow gate in place. Augustine also says the saved are many, so he is
   not simply against Schuster on number; he differs on what follows from it.
   Schuster attributes the counting to John, where the text says *nemo*. The
   study must not say the saved are uncountable in God's sight.
3. **The rewards of the beatitudes.** Augustine, Chrysostom, Aquinas,
   Bernard and Rabanus place them in this life as begun or as pledge; Hilary reads them of
   the immortal state. Augustine qualifies his own emphasis: "that
   all-embracing change into the angelic form, which is promised after this
   life, cannot be explained in any words" (I.4.12). A difference of emphasis
   that changes the reading of the Gospel (5.2).
4. **The goods of Ps 33:11.** Basil excludes bodily goods by the apostles'
   example; Aquinas admits them and answers the same objection otherwise;
   Bellarmine keeps a temporal sense; Augustine says the literal sense seems
   to deceive (5.3).
5. **The 144,000.** Victorinus: believers at Elias's preaching; Bede and the
   PL 35 *Expositio*: the whole Church (5.1).
6. **The angel of 7:2.** Victorinus: Elias. Bede: Christ, the Angel of great
   counsel. PL 35: the Catholic Church. Augustine applies *magni consilii
   Angelus* to the angel of Ps 33:8, which the Mass does not say.
7. **Whose souls are in God's hand (Wis 3:1).** Schuster: the martyrs, against
   their persecutor. Alphonsus: every just soul at death. Bonaventure: the
   martyrs specially and all the just truly. A difference of extent that
   changes what the Offertory says of the saints of the feast (5.5).
8. **What burden the Alleluia's call lifts (Mt 11:28).** Chrysostom: sins,
   anxieties and sorrows, so "not this or that person, but all". Hilary: the
   Law's difficulties and the sins of the world, with the yoke of Christ's
   commandments taken through the sacrament of the cross. Rabanus: sin, with
   Zach 5 and Ps 37, or else the Law's heavy yoke, from which the call is to
   the Gospel's grace, which is Jerome's comment taken over (3.6). Gregory
   (*Moralia* I): the heavy yoke of the Law, the
   ordinances of the external letter. Augustine: in Sermon XIX the common
   labour of frail mortals, "bearing about vessels of clay"; in Sermon XX the
   burdens of numberless observances; in Sermon XXI the burdens of sins and
   transgressions of the Law. Aquinas reports Hilary's reading and draws from
   it that the New Law is lighter than the Old. A difference of extent: on
   Chrysostom's reading and Augustine's in Sermon XIX the call reaches every
   burdened human being; on Hilary's, Jerome's and Rabanus's second reading and Gregory's
   it is first a call out of the Law into the Gospel. What it changes: whether
   the Alleluia, sung on the feast, speaks to the common burden of frailty and
   sin or recalls the passage from the Law to grace. Every witness read joins
   the rest to the yoke of meekness and humility of 11:29, which is the use
   Reading B makes of the verse (3.6).

## 7. Negative results and searches bounded

The matrix (3.0) gives, passage by passage, the held witnesses not read with
the reason, the works not held, and the searches made with their terms. The
results that bear most on the study:

- **How the searches were made.** Iteration 1's literal phrase searches matched
  single-spaced text line by line. Many tracked Internet Archive text layers
  put two spaces between words on many lines, and a phrase broken across two
  lines is missed by a line search. Iteration 2 replayed every literal query
  over the whole text of each tracked file with any run of whitespace between
  words, read every added hit outside missals and Bibles at the line, and
  corrected each negative that the replay overturned (3.0). Counts are given
  literal first, then whitespace-tolerant.
- `formulary`: no liturgical commentator for `omnium-sanctorum` or
  `pentecost-23`. A search of the held liturgical commentators beyond
  `formulary` found Sicard and Honorius in iteration 1, and Beleth's c. 158
  and the PL 151 sacramentary's Mass in iteration 2; the other hits in
  Amalarius, Rupert, Bernold and Berno do not treat the feast's Mass. The
  replay also found the Gregorian Sacramentary and Antiphonary in PL 78 (3.1).
- Ps 32:1: Augustine, Basil, Aquinas and Bellarmine read (3.2). Held, not
  read: Cassiodorus, Theodoret, Athanasius (remote or partial holdings) and Hugh
  of Saint-Cher (restricted).
- Apoc 7: Primasius, Ambrose Autpert, Beatus, Haymo, Rupert, Richard of
  Saint-Victor and Bruno of Segni are mapped by the index but not held.
  Caesarius of Arles: no separately held Apocalypse homilies (3.4).
- Mt 11:28: iteration 1's "searched, not found" for Hilary and Rabanus was
  wrong; both comments are held and were read on the page images (3.6).
  Iteration 3 read Jerome on the verse on the page image of the remote PL 26
  scan and found Rabanus's comment there (3.6). Gregory's *Homiliae in
  Evangelia* and Aquinas's *Super Matthaeum* on Mt 11 are held but not read;
  the *Catena aurea* is not held for Matthew.
- Mt 5:1-12: iteration 1's "searched, not found" for Rabanus was wrong; his
  commentary was read (3.7). Jerome and Augustine's *De consensu* are held but
  not read; Gregory of Nyssa, Chromatius and Paschasius are not held.
- Wis 3:1-3: the index maps no commentary. Literal search and the catalogue
  found Bonaventure's commentary (the only registered commentary on Wisdom),
  Augustine's gloss, Alphonsus's consideration and the uses in 3.8. The
  *Glossa* and Rabanus on Wisdom are not registered and are known here only
  through Bonaventure. Greek search terms found nothing.
- The Offertory's wording: *malitiae* is older than 1570 (the Gregorian
  Antiphonary in PL 78, the Fonte Avellana codices in PL 151, Sarum, Peter of
  Celle). The *alleluia* is first found in the Mame printing of 1922; the
  scan registered under the 1920 typical edition is a printing of 1951-1954
  (body) and 1970 or later (appendix), so the 1920 typical edition itself was
  not read. No act or decree was read for the *alleluia* (3.8).
- The Preface: the governing edition's closest direction (p. 16) was found and
  admits both inferences; no registered rubrical commentary was found that
  treats a first-class feast taking a second-class Sunday; Murphy 1960 was not
  re-read and is not relied on (3.11).
- No dated web witness is relied on beyond research/context.md's record; none
  is registered as a dated passage here.

## 8. Chronology

`research/chronology.toml` and `research/chronology-annotations.tex` were
generated with `tools/tpt proper-chronology` (record, then annotations with
`--presentation orientation-v2 --write`); both commands exited 0 in iteration 0
and were not regenerated, because no appointed range changed.

### 8.1 Rows and their passages

- Introit, Ps 32:1; Gradual, Ps 33:10-11: traditional attribution to David,
  reign 1055-1015 B.C. "in the usual chronology" (Catholic Encyclopedia vol. 4,
  "David", passage `…volume-4.new-york-1908.corbett-david-usual-chronology`,
  read); composition of the Psalter before c. 165 B.C., no individual psalm
  securely dated (NABRE Psalms introduction, passage
  `…new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-introduction`,
  read). Ps 32's occasion: unresolved; the corpus supplies none.
- Gradual, Ps 33: superscription setting, David's flight to Achis, king of
  Geth, A.M. 2944 (Haydock's 1 Kings 21 note, passage
  `…first-kings-21-achis-geth-chronology`; the attribution of the marginal
  chronology to Ussher rests on the Ps 70 note, passage
  `…psalm-70-captivities-usher-chronology`; both read). The psalm's title
  names Achimelech, 1 Kings 21 Achis; the row's subject is the event the title
  names, which the corpus identifies with 1 Kings 21.
- Lesson, Apoc 7:2-12: composition disputed, the reign of Domitian, A.D. 81-96
  (Catholic Encyclopedia vol. 1, "Apocalypse", 01594b) and c. A.D. 90-100
  (vol. 14, 14530a). The row is labelled "Revelation 7:2-12" by the generator.
- Alleluia, Gospel and Communion share one Matthew composition row with six
  disputed dates (Catholic Encyclopedia vol. 10, 10057a; vol. 14). The Gospel's
  event row reads "Date unresolved": the corpus has no date for the Sermon on
  the Mount.
- Offertory, Wis 3:1-3: two disputed lower bounds, in or after Ptolemy IV
  Philopator (221-204 B.C.) or Ptolemy VII Physcon (145-117 B.C.) (Catholic
  Encyclopedia vol. 15, "Wisdom", 15666a).

### 8.2 Partial verses and adaptations not reflected in the rows

- The Gospel row reads Mt 5:1-12 and reaches 5:12 whole; the Mass ends at 12a.
  The range comes from `propers.yaml` (section 10).
- The Offertory row reaches Wis 3:1-3 whole; the antiphon omits 3:2b-3a.
- The Gradual's composite form (5.3) is not a chronology question; its verses
  are Ps 33:10-11.
- No row is printed for the Introit antiphon, which is not scriptural.

### 8.3 Nesting and duplication

The Communion (Mt 5:8-10) lies inside the Gospel (5:1-12a). The orientation-v2
rows merge the Alleluia, Gospel and Communion into one Matthew composition row,
so no identical date is repeated beside a constituent passage.

### 8.4 Event and composition kept apart

Psalms: attribution, superscription setting and composition are separate rows;
the era of David is not given as the date of an event. The Gospel's event is
unresolved and its composition disputed. The Apocalypse and Wisdom have
composition rows only; the corpus dates no event in Apoc 7.

### 8.5 For the authors

The concise page 2 and the study's terminal appendix
(`sections/80-date-location.tex`) print these rows. Where the passage column
says "Revelation", the documents' own citations say "Apoc"; the label comes
from the generator, not this leaf.

### 8.6 Planned occurrence and place phrases

One phrase for each orientation-v2 row, in the row order of
research/chronology-annotations.tex. The writer's place, the event's place and
an unknown place are kept distinct; "place unknown" is written wherever the
sources name none.

| Row | Subject | Planned phrase | Source |
|---|---|---|---|
| `row-e88e943a6faaa20b` | Psalms, traditional attribution: David's reign | "Traditionally ascribed to David; place of composition unknown." | Catholic Encyclopedia vol. 4, "David" (8.1); no source read names where any psalm was written |
| `row-bbfc04633a7fe6e8` | Ps 32, historical setting | "No occasion is named; place unknown." | Ps 32:1, whose Vulgate title reads only *Psalmus David* (Douay "A psalm for David"; Aquinas's psalter adds *In finem*, and he notes "Titulus non est novus", Parma vol. 14 line 41544); the Hebrew psalm has no title |
| `row-fb6656afd6f4b4f0` | Psalms, composition | "Composed before c. 165 B.C.; place unknown." | NABRE Psalms introduction (8.1) |
| `row-d7a171509b4d3dc5` | Ps 33, superscription setting | "The title's occasion: David feigning madness before the king at Geth (called Achimelech in the title, Achis in 1 Kings 21:10-15)." This is the event's place, not the writer's. | Ps 33:1 (Vulgate title); 1 Kgs 21:10-15 (Douay and Clementine, read); Haydock's note (8.1) |
| `row-ca811ebc12efaaee` | The Apocalypse, composition | "The visions were seen on Patmos (Apoc 1:9)." Where the book was written down is not stated in the text and is given only by tradition. | Apoc 1:9-11, read in context (3.4); Catholic Encyclopedia vol. 1, "Apocalypse", 01594b, line 33: "the visions he is about to narrate were seen by him whilst in Patmos" |
| `row-43dce930fad06090` | The Book of Wisdom, composition | "Written in Alexandria by an unknown Alexandrian Jew (by inference from internal evidence and the Alexandrian canon)." | Catholic Encyclopedia vol. 15, "Wisdom", 15666a, line 27: "as it was composed in Alexandria"; the author "unknown" |
| `row-c1e1f88c6b954af2` | Mt 5:1-12, event | "On a mountain in Galilee, not named (Mt 4:23-5:1)." | Mt 4:23-25 (Jesus "went about all Galilee"; crowds from Galilee, Decapolis, Jerusalem, Judea and beyond the Jordan) and 5:1, "he went up into a mountain", read in context (3.7) |
| `row-8b85083df79d6e95` | Gospel of Matthew, composition | "Place of writing unknown; Eusebius reports that Matthew wrote it when he left Palestine." | Catholic Encyclopedia vol. 10, "Gospel of St. Matthew", 10057a, line 201 |

- **The Alleluia's setting**, which has no row of its own: Mt 11:28 is said
  after the upbraiding of Corozain, Bethsaida and Capharnaum (Mt 11:20-24,
  read in context, 3.6); the place where the words were spoken is not named.
  If a study mentions it, the phrase is "place not named".
- The Gradual phrase keeps Achimelech, the psalm's title, beside Achis, the
  king of 1 Kings 21, as 8.1 does.

## 9. Rights

- **Latin.** On the 17 U.S.C. 103(b) holding of
  `missale-romanum-1962-facsimile-rights-v1.toml`, each element's words stand
  in a public-domain printing collated with the 1962 page: the feast's ten in
  Mame 1922, the three Sunday orations in Pustet 1862 (propers/verified.md, The
  publication basis of the Latin). The Preface is not printed.
- **English.** Douay-Rheims (Challoner), public domain. Lasance 1945, public
  domain in the United States by nonrenewal
  (`lasance-new-roman-missal-rights-v1.toml`); its excluded lettered ranges are
  not touched.
- **Reception quotations** are short and from public-domain editions: PL 9, 35,
  78, 107, 142, 151, 183, 202, 213, 172; PG 29; Parma 1863; Venice 1745; Quaracchi 1893; ANF and
  NPNF; Marshall 1878; Duffy 1843; Legg 1916; Schuster 1930 (registered
  public-domain); Durandus 1568; Guéranger 1909. The New Advent *Summa* and
  *Enchiridion* pages carry the older public-domain translations; the
  registered Enchiridion artifact's rights are recorded as unresolved and it is
  cited, not retained. The Wikisource Gregory is CC-BY-SA 3.0 as a
  transcription; its Latin is ancient. The *Moralia* is quoted in the Library
  of the Fathers translation (Oxford, 1844), read in a dated web text layer.

## 10. Shared records: defects reported for their owners

- `src/sources/calendars/roman-1962/propers.yaml`, `omnium-sanctorum`: Gospel
  encoded Mt 5:1-12 (the Mass ends at 12a); Offertory Wis 3:1-3 entire (3:2b-3a
  omitted); no Preface case.
- The chronology generator labels the Lesson "Revelation".
- `tools/tests/test_ordinary_appointments.py` (`allSaintsSunday1962`, lines
  261-269) asserts the common Preface, which the rubrics do not settle; the
  same test asserts the Trinity Preface for the Christmas Vigil on a Sunday from
  p. 16, whose reach to All Saints is the open question (3.11).
- `roman-1962-proper-latin-provenance-v1.toml` has no rows for the six
  scriptural elements; `roman-1962-proper-translations-v1.toml` has none for the
  scriptural elements; `formulary-loci.yaml` is empty for both formularies.
- `author-standing-v1.toml` has no rows for Bernard (a Doctor), Cyprian,
  Victorinus, Alphonsus Liguori (a Doctor), Bonaventure (a Doctor) or Peter of
  Celle, so canonized saints and Doctors cannot carry a reading here.
- `passage-commentary-index.yaml` has no mapping for Wis 3:1-3, although
  Bonaventure's commentary (registered, contained in Quaracchi vol. 6) and
  Alphonsus's Ninth Consideration (registered, and already indexed for other
  passages) treat it.
- The Quaracchi vol. 6 OCR reads the lemma of Wis 3:1 as *lustorum*, which
  defeats literal search.
- The PL 202 text layer is filed under John Beleth's work, but the uses of Wis
  3:1 read here are Peter of Celle's, printed in the same volume.
- Several works' locus grammars cannot express the loci read: Honorius's
  *Gemma animae* admits book IV only (III cc. 161 and 168 were read), and
  Fromage's volume admits printed pages only; research/source-bindings.toml
  gives those loci by physical line in its contexts.
- `tools/commentary-work-index discover` reports Cornelius a Lapide as held for
  the Apocalypse and Matthew through title joins to commentaries that do not
  cover them, and lists some works under duplicate rows (Haimo and Haymo;
  Richard of Saint-Victor three times; Rupert of Deutz twice; Denis the
  Carthusian twice).
- `source-containment-v1.toml`, Victorinus constituent: bounds his extent at
  Rev 1, 5 and 19, but the ANF text comments on chapters 7 and 12.
- Bede's *Explanatio*: no passage records for Apoc 7:1-3.
- The PL 35 *Expositio* and its possible Caesarian attribution are not
  represented in the library.
- The Mame derivative `…all-saints-scriptural-propers-la-checked-415a1d46`
  does not reproduce Mame's orthography (section 2).
- `work.fsspx.ordo` declares English; the responses are French.
- St Bernard's *In festo omnium Sanctorum* sermons (PL 183) and the New Advent
  page of *ST* I q. 23 read here were unregistered when iteration 0 read them;
  the source-registration stage has since registered them
  (`work.jacques-paul-migne.patrologia-latina-volume-183` with its remote scan,
  tracked optical text and tracked excerpt of cols. 453-481;
  `segment.bernard-of-clairvaux.sermones-in-festo-omnium-sanctorum.1854-migne-pl183.cols-453-481`;
  and `edition.thomas-aquinas.summa-theologiae.2026-10-27-english-dominicans-newadvent-prima-q23`),
  and research/source-bindings.toml binds them. No English translation of
  Bernard's sermons is registered or was sought. The PG 29 facsimile is
  registered as a remote artifact; the copy read here matched it.
- Registering those records stales the pinned `canonical_catalog_snapshot` in
  `src/sources/inventories/source-family-migration-v1.toml`, as any new source
  record does; the ledger's owner refreshes it.
- Iteration 1's added reading needed no new registration: every source it
  read, searched or used to locate a passage was already registered and is
  bound. Two library gaps remain for its new loci: no work record exists for
  Bernard's sermons *In transitu S. Malachiae* (PL 183) or for Peter of Celle's
  writings (PL 202), and the library holds no Latin of Cyprian's *Ad
  Fortunatum*, Augustine's *De sermone Domini* or Sermon LXI [CXI], Victorinus,
  or Gregory's *Moralia*, so those loci stay English-only. The text layer of
  the 1962 facsimile searched at line 5653 (3.11) is a local extraction from
  the registered remote facsimile and is not registered; the claim rests on the
  page image of the bound facsimile, and whether a derivative may be retained
  is for the facsimile's rights record to settle.
- Iteration 2 (the search replay) found these defects in shared records:
  - `tools/source-library` text search matches a phrase literally within one
    line. It has no whitespace-tolerant or whole-text mode and gives no
    warning, so on Internet Archive text layers that double-space words, or
    where a phrase breaks across lines, a phrase search returns false
    negatives. The artifact records of PL 9, PL 78, PL 107 and PL 151 do not
    warn of the double spacing, and none gives loci for the works read here
    (Hilary XI n. 15 at col. 984; Rabanus on Mt 5 and 11:28; the Gregorian
    Sacramentary's All Saints Mass and Ménard's note; the Antiphonary; the
    Monte Suavicino sacramentary and the Fonte Avellana excerpts).
  - The PL 151 text layer is filed under Bernold's *Micrologus*, but the
    sacramentary and liturgical excerpts read here, printed in the same volume,
    are not Bernold's; the PL 142 text layer is filed under Berno of
    Reichenau, but Bruno of Würzburg's *Expositio Psalmorum* is printed in it.
    Neither has a work record of its own.
  - `author-standing-v1.toml` has no row for St Bruno of Würzburg.
  - `proper-components.toml` of this document (owned by the assembly stage)
    says in its lane comment that Rabanus Maurus "is cited as a compiler of
    Augustine" and carries no reading, and the lane
    `beatitudes-way-of-the-saints` does not list him in `carrying_authors`.
    He has the standing `saint`, and this research records him as carrying
    Reading B (section 4; research/interpretations.md).
  - `research/source-dispositions.toml` is the source-registration stage's
    record. The source-registration stage of iteration 2 reconciled it: it
    disposes of the sources this iteration added (Rabanus on Mt 5 and 11:28,
    Hilary XI n. 15, Augustine's Sermons XIX-XXI, Gregory's *Moralia* I,
    Aquinas's I-II q. 107, the PL 78 Sacramentary, Antiphonary and Ménard's
    note, the PL 151 sacramentary and excerpts, Bruno of Würzburg, Aquinas's
    *In Ps.* 17), corrects iteration 1's rows for the 1920 witness and the
    *De sermone Domini* locus, and replaces the negative-search rows for
    Rabanus. Every new commentary locus is deferred, not admitted: none has a
    passage record, and the OCR-only loci have no checked Latin.
  - The page images of PL 107 cols. 795-798, 821-822 and 915-918 and of PL 9
    cols. 983-984 are now retained as tracked facsimile excerpts of the
    registered remote scans (research/source-bindings.toml). The remote
    artifact records of PL 107 and PL 9 do not yet point to them.
  - Rabanus's comment on Mt 11:28 (PL 107 about col. 916) carries no source
    label. Iteration 3 found its source: it is Jerome's comment on the verse
    (*In Matthaeum* II, PL 26 col. 75), taken over nearly word for word (3.6).
    The library holds no text layer of PL 26 and no passage record for the
    locus; the segment `pl26-columns-15-218` of Jerome's commentary bounds
    the work in the scan, and the page read (cols. 75-76) is now retained as a
    tracked excerpt (below).
  - The study's section on the Lord's Prayer and the beatitudes (study-owned)
    quotes Rabanus at PL 107 lines 93919-93920; that passage is Augustine's
    *De sermone Domini* II.11.38 taken over by Rabanus (3.7).
- Iteration 3 (the Collect's two readings and Jerome) found these defects in
  shared records:
  - The PL 85 text layer `…liturgia-mozarabica-1862-text-769ccd75` is filed
    under the *Missale mixtum*, but lines about 97865-100430 are the Monte
    Suavicino *Vetus sacramentarium* printed in an appendix of the volume (the
    same book as in PL 151). Its artifact record does not say so, and a hit
    there reads as a Mozarabic witness, as it did in iteration 2's review.
  - Feltoe's 1896 Leonine Sacramentary has only remote optical text layers
    (`ia-djvu-ocr-sacramentariuml00feltgoog`, `ia-djvu-ocr-sacramentariumle00cath`),
    so no search of tracked text reaches it.
  - Wilson's 1894 Gelasian Sacramentary is registered as two editions under
    two works, `work.catholic-church.sacramentarium-gelasianum-vetus`
    (edition `wilson-1894`, whose artifacts are read here) and
    `work.anonymous.gelasian-sacramentary` (edition `wilson-clarendon-1894`),
    whose artifact records refer to each other; whether the two works should
    be one is for the library's owner. The remote PDF's
    `rights_status` is `unresolved` for its digitiser matter; the two
    printed pages read here (183-184) are now retained as a page extraction
    (below), as other printed pages of the same scan already are.
  - The 1604 typical edition's text layer is unreadable at the feast (lines
    53418-53429).
- The source-registration stage of iteration 3 found every source read in
  iteration 3 already registered, and checked the fetched PL 26 and Wilson
  1894 copies against their registered SHA-256 and byte sizes. It retained
  the pages read as tracked mechanical page extractions:
  `…patrologia-latina-volume-26.paris-1845.columns-75-76-facsimile-b432adc8`
  (PDF p. 45) and
  `…sacramentarium-gelasianum-vetus.wilson-1894.pages-183-184-facsimile-7f5cc922`
  (PDF pp. 276-277), and bound them. It corrected the record of the PL 107
  excerpt, which had called the source labels marginal. Defects in shared
  records:
  - The remote artifact records of PL 26 and of Wilson 1894 do not name the
    new excerpts in their notes; the Wilson record's access limitation lists
    only the excerpts retained before.
  - The record of the PL 107 excerpt `…columns-869-874-facsimile-9d084bb1`,
    made for another document, also speaks of "marginal source sigla"; its
    pages were not read here.
  - Jerome's *In Matthaeum* has no registered English edition and no row in
    `translation-absences.yaml`, and no passage record for the comment on
    Mt 11:28-29, so it is deferred (research/source-dispositions.toml).

## 11. Bounds of this research

- Reception was read at the loci named and no further. The searches are the
  ones the matrix records (3.0); no whole-corpus sweep of the Fathers on any
  passage is claimed, and literal search reaches tracked text layers only.
- OCR-read loci (Hilary, Rabanus, Durandus, Beleth, Fromage, Sicard,
  Honorius, Bonaventure, Alphonsus, Peter of Celle, Bruno of Würzburg, the
  Sarum Missal, the PL 78 Sacramentary and Antiphonary, the PL 151
  sacramentary and excerpts, parts of Bernard, Aquinas and Basil on the
  Psalms) were not collated against page images except where stated. Hilary
  XI n. 15 and Rabanus at cols. 796, about 822 and 916 were read on the
  images, which are retained as tracked facsimile excerpts. Jerome at PL 26
  col. 75, the Leonine prayer (Feltoe) and the Gelasian prayer (Wilson) were
  read on page images; the PL 26 and Wilson scans were fetched for the
  reading, and the pages read are retained as tracked excerpts of them
  (Feltoe's scan is tracked whole).
- The Collect's history rests on the witnesses listed in 3.3. No study of the
  Collect's adaptation from the apostles' prayer was read, and no witness
  read dates either reading of *intercessoribus* and *intercessionibus*.
- The whitespace-tolerant replay (iteration 2) covered the research's own
  queries over tracked text files; it did not add new queries beyond those
  recorded in 3.0 and 3.1, and remote artifacts were searched only where
  stated.
- Victorinus's ANF text is a recension of uncertain integrity.
- Bellarmine is read in an expressly abridged English; Alphonsus in an 1843
  English translation.
- The Offertory's history rests on text layers of five printings (one of them
  the 1951-1954 printing of the 1920 text, with an appendix of 1970 or
  later), the Mame 1922 page, the Sarum Missal, Peter of Celle, the
  Gregorian Antiphonary in PL 78 and the PL 151 excerpts. The 1920 typical
  edition itself, any printing between 1909 and 1922, and any document of the
  Roman congregations were not read, so the *alleluia*'s entry is bounded
  only between 1889/1909 and 1922.
- No Greek original was collated for Basil or Chrysostom; Basil was read in
  Migne's Latin (on Ps 32 n. 1, in the OCR of both columns), Chrysostom in
  NPNF.
