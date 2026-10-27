# Research scope and evidence record

Run `427e2f58bb897a16`, stage research, iteration 0, provider claude, date
2026-11-01 (the feast *In Festo Omnium Sanctorum*, I classis, with the
commemoration of the Twenty-third Sunday after Pentecost). This record states
what was read, how, and to what depth; the reception found for every appointed
passage; the witnesses and their standing; the difficulties and disagreements
preserved; the negative searches; the chronology inspection; the rights basis;
and the reports owed to the owners of shared records. It holds the evidence
behind `propers/verified.md` and `research/interpretations.md`. It contains no
study prose. It was revised in iterations 1 and 2 of the same stage
(2026-10-26). Iteration 2 restated the Preface question and the last Gospel
from registered sources only (§6 items 7-8, §7, §11), withdrew the dated web
witnesses as evidence, and declared the Lasance oration records in
`research/review-dependencies.toml`. Iteration 3 (2026-10-26)
corrected a false negative on the Lesson: Victorinus of Pettau's commentary in
the tracked ANF VII text does comment on Apoc 7 (§3.3). The proportionate
second search that followed read three Augustine loci, Bellarmine on two
psalms, Cyprian, and the anonymous *Expositio in Apocalypsim* of PL 35 (§3.3,
§4, §5.1, §6 item 1, §7, §10 items 5 and 12, §11).

Standing terms used below are those of
`src/sources/inventories/author-standing-v1.toml`: father, doctor, saint,
blessed, servant-of-god, ecclesiastical-writer. Where a row is missing, that is
said. A witness's standing governs who may carry an interpretation; every
witness may still be evidence of reception.

## 1. What was read, and how

**The appointed text.** The formulary (printed pp. 702–703, artifact pp.
783–784, nos. 3974–3983) and the commemorated Sunday's three orations (printed
pp. 416–417, artifact pp. 497–498, nos. 1720, 1726, 1728) were read on 200-dpi
page images and again on 400-dpi quarter crops of the controlling CMAA
facsimile (hash matched before use), rendered as transient rasters that are
not kept with the records. Every word, accent and cue in `propers/verified.md` comes from
those images. The facsimile's embedded text layer was pulled (`pdftotext
-layout`) and is kept in `propers/retrieved.txt` as a finding aid with its
misreadings listed; it supplied no reading.

**The collation witnesses.** The Mame 1922 checked artifacts
(`…all-saints-four-propers-la-checked-82edd79a`,
`…all-saints-scriptural-propers-la-checked-415a1d46`) and the two project
editorial projections (2026-10-20 `adfda498`; 2026-10-25 `f645e8ee`) were read
in full and compared element by element against the 1962 readings: result in
`propers/verified.md` (word-for-word agreement apart from *i/j* orthography,
accents, and the Postcommunion conclusion cue). The Clementine verse artifacts
for Psalms, Wisdom, Matthew and Apocalypse were read for the cited verses.

**The reception sweep.** For each appointed passage the registered library was
searched first (`tools/tpt source-library discover --passage …` and the
formulary-level `commentary-work-index`); every held candidate was opened and
read at the passage, on the artifact's own text layer with line numbers kept.
Readings are recorded below with artifact identity and line loci. Nothing was
read from the GPT leaf for this identity, its review records, or any
postconciliar record. No web fetch was made in iterations 0-2 of this stage:
everything they read is a registered artifact whose source fingerprint was
taken with `tools/tpt source-library fingerprint` on 2026-10-26; each full
fingerprint is recorded on its binding in `research/source-bindings.toml`.
Iteration 3 made one fetch, of a registered artifact's own bytes (below).

**The iteration-1 repair (2026-10-26).** The repair of this stage read three
further things at their loci. (1) The 1570 Venice Missal's own All Saints
Offertory (text artifact `563f4dd2`, physical lines 71705–71709), with the
later Missal printings held as text layers (1604, 1862, 1889), to fix the
history of the antiphon's wording (§3.7, §5.3). (2) The tracked Pustet 1862
page extract `pentecost-23-prayer-pages-7e6ef53b` (parent PDF pp. 443–444 =
printed pp. 357–358), rendered at 150 dpi and in 300-dpi crops, for the
commemoration's three orations (§9; `propers/verified.md`). (3) The verse
numbers of the NPNF and Bellarmine English for Ps 33, converted to the
Vulgate's (§3.4, §6.9).

**Sources read by the resolve-context stage (registered 2026-10-26).** The
dated web witnesses and Murphy's 1960 rubrics commentary that the
resolve-context stage read were registered by the source-registration stage
(iteration 2) after it re-hashed the receipts and read each bound locus in
those bytes; they are bound as context only (bindings 35-41) and carry
nothing (§7, §11).

**The iteration-3 repair (2026-10-26).** The repair read
Victorinus of Pettau's commentary on Apoc 7 in the tracked ANF VII text
(artifact `ccel-text-b69327af`), which iteration 0 had wrongly reported as
outside the holdings, and ran the proportionate second search for an
eligible witness on Apoc 7 who agrees with Bede (§3.3, §7). Literal searches
of the registered library's text layers for the Lesson's wording located,
and the repair then read at the passage, Augustine's Letter XCIII §30, *De
doctrina christiana* III.35.50–51 and Sermon LXI (NPNF I.1, I.2 and I.6),
Bellarmine on Ps 86 and 121, and Cyprian's *Ad Fortunatum* §11 (ANF V). It
made one fetch: the registered remote scan of PL 35
(`internet-archive-google-pdf-b3ff8a95`), retrieved on 2026-10-26 from the
artifact record's `source_url`
(https://archive.org/download/patrologiaecurs143migngoog/patrologiaecurs143migngoog.pdf).
Its SHA-256 (`b3ff8a95023613d6dd6d3953ed7203946aeb95fd8ab819547f693083a07fa902`)
and size (62,548,064 bytes) matched the artifact record before any page was
rendered. PDF pp. 557 and 562–563 were read on page images rendered at 150 to
300 dpi, which are transient and not kept with the records. The Internet
Archive's OCR of the item
(https://archive.org/download/patrologiaecurs143migngoog/patrologiaecurs143migngoog_djvu.txt,
4,425,263 bytes, SHA-256
`54f87784316947fa7c237fa9d3816cd1640bb8b087cd23966e68b2986c02ec56`, retrieved
2026-10-26) served only to find the pages; no wording rests on it. The
fingerprints of the new and changed bindings (14, 17, 19, 42–46) were taken
on 2026-10-26.

**The third pass of the source-registration stage (iteration 3, 2026-10-26).**
The pass registered the two PL 35 retrievals named above: the OCR finding aid
as the tracked artifact `…1845-paris.ia-djvu-text-54f87784` (its byte size and
SHA-1 equal the Internet Archive item's own file listing), and the four pages
read as evidence (parent PDF pp. 557, 558, 562, 563) as the tracked facsimile
excerpt `…1845-paris.columns-2415-2418-and-2425-2428-facsimile-772856db`,
each extracted page's embedded image checked byte for byte against the
registered scan. Binding 46 now binds the excerpt, so the checked pages are
openable without the network; the whole scan stays remote for its measured
size (62,548,064 bytes). The OCR layer is bound as a finding aid (binding 47).
The fingerprints of the other iteration-3 bindings were re-taken, unchanged.

**Whole-context reading.** Apocalypse 7 was read whole in Bede's chapter VII
(his *Explanatio Apocalypsis*, the principal held commentary on the Lesson),
and in iteration 3 in Victorinus of Pettau's chapter 7 comments (vv. 2 and 9
only) and the anonymous PL 35 *Expositio*'s comment on the chapter;
Psalms 32 and 33 whole in Augustine's *Enarrationes* (English NPNF text) with
Bellarmine and Basil and Aquinas at the appointed verses; Matthew 5:1–12 with
its frame (Mt 4:23–5:2, 5:13–16) in Chrysostom's Homily 15, Augustine's *De
sermone Domini in monte* I, Hilary chapter IV, and Aquinas's *Super Matthaeum*
cap. 5; Matthew 11:25–30 in Chrysostom's Homily 38 and Augustine's Sermon XIX
(Benedictine LXIX); Wisdom 2:21–3:9 against the Clementine text (no mapped
commentary exists; §3.7).

## 2. Literary context of each appointed passage

- **Ps 32:1 (Heb./Eng. 33:1) — Introit verse.** Vulgate Psalm 32, the only
  psalm of the first book whose Hebrew carries no superscription; the
  Clementine prints `Psalmus David` inside v. 1, which the Missal's citation
  `Ps. 32, 1` does not read. The psalm is a hymn of praise: rejoice in the
  Lord (v. 1), praise on the cithara (vv. 2–3), the word and works of the Lord
  (vv. 4–9), the counsel of the Lord against the counsels of nations
  (vv. 10–12, with *Beata gens cuius est Dominus Deus eius* at v. 12), and the
  Lord's regard for those who fear Him (vv. 18–22). The feast's antiphon is
  not the psalm: *Gaudeamus omnes in Domino…* is an ecclesiastical
  composition, printed without a citation (on its origin see §3.1, Schuster
  and Durandus).
- **Apoc 7:2–12 — Lesson.** The chapter stands between the sixth and seventh
  seals: the four angels holding the winds (v. 1), the angel from the east
  with the seal of the living God (vv. 2–3, echoing Ezechiel 9's mark on the
  forehead), the numbered sealing of 144,000 from the tribes (vv. 4–8, Dan
  omitted, Manasses added), then the vision that answers it: the great
  uncounted multitude from all nations before the throne and the Lamb, in
  white robes with palms, crying *Salus Deo nostro* (vv. 9–12). The Missal
  reads vv. 2–12 and stops before the elder's question and answer
  (vv. 13–17: *hi sunt qui venerunt de tribulatione magna… laverunt stolas
  suas in sanguine Agni*), which the feast's office uses elsewhere. The
  liturgical incipit *In diebus illis: Ecce ego Ioannes vidi…* replaces the
  Clementine's *Et vidi alterum angelum…*.
- **Ps 33:10–11 (Heb. 34:10–11; Eng. 34:9–10) — Gradual.** Vulgate Psalm 33,
  an alphabetical psalm whose inscription (*Davidi, cum immutavit vultum suum
  coram Achimelech…*, so the registered Clementine) is its v. 1 in the
  Clementine count, as it is in the Hebrew. The Missal's `Ps. 33, 10 et 11`
  is therefore Douay 33:10–11 and Hebrew 34:10–11; English Bibles that follow
  the Hebrew psalter but leave the inscription unnumbered call the same verses
  34:9–10. The appointed words sit in the
  psalm's second movement: the angel of the Lord encamps around those who
  fear Him (v. 8), *Gustate et videte quoniam suavis est Dominus* (v. 9),
  *Timete Dominum omnes sancti eius* (v. 10), *Divites eguerunt et
  esurierunt; inquirentes autem Dominum non minuentur omni bono* (v. 11). The
  Gradual reads v. 10 in the older Roman psalter wording (*quoniam nihil
  deest timentibus eum*) and v. 11b only (*non deficient omni bono*), leaving
  *Divites eguerunt* unsaid — a selection with exegetical weight (§5.2).
- **Mt 11:28 — Alleluia verse.** The close of the Lord's turn from the
  woes on the lake towns to thanksgiving (11:25–27, *I confess to Thee,
  Father… Thou hast hid these things from the wise and prudent and hast
  revealed them to little ones*) and before the sabbath controversies of
  chapter 12. Verse 28 is the invitation (*Come to me, all you that labour
  and are burdened, and I will refresh you*), continued in vv. 29–30 (the
  easy yoke, the light burden) which the verse of the Mass does not read but
  every commentator below reads with it.
- **Mt 5:1–12 — Gospel.** The opening of the Sermon on the Mount: the ascent,
  the sitting, the opening of the mouth (5:1–2), the eight beatitudes
  (5:3–10) and their direct application to the hearers (5:11–12). The Missal
  ends at 12a, before *Sic enim persecuti sunt prophetas*. The frame matters
  for the reception: the mountain against Sinai, the beatitudes against the
  decalogue (so the commentators, §3.6).
- **Wis 3:1–3 — Offertory, adapted.** The Book of Wisdom's answer to the
  impious speech of 1:16–2:20 (*Let us oppress the poor just man… let us
  condemn him to a most shameful death*): the souls of the just are in the
  hand of God (3:1), they seemed to die in the eyes of the unwise but are in
  peace (3:2–3), their hope is full of immortality (3:4), and *in the time of
  their visitation they shall shine* (3:7). The antiphon selects 3:1 and the
  frame of 3:2–3, omits *autem*, reads *tanget* for *tangent* and *tormentum
  malitiae* where the Clementine reads *tormentum mortis*, and adds
  *alleluia*. It is the received liturgical form, not the verse (collation in
  `propers/verified.md`; its history in §3.7).
- **Mt 5:8–10 — Communion.** The sixth, seventh and eighth beatitudes,
  re-read from the Gospel just proclaimed: the clean of heart see God, the
  peacemakers are called sons of God, the persecuted for justice possess the
  kingdom. Word-for-word the Gospel's own words (§3.6 for the reception).
- **The three orations of the feast and the three of the Sunday** are composed
  texts, not Scripture; their reception is in §3.9–3.10.

## 3. Reception matrix

### 3.1 Liturgical commentators

The shared index `src/sources/commentary/formulary-loci.yaml` lists no
liturgical commentator for this formulary
(`tools/tpt commentary-work-index formulary --calendar roman-1962 --mass
omnium-sanctorum`: 40 loci compared, none listed — the negative is reported
in §10). The sweep therefore went directly to the registered commentators.

- **Ildefonso Schuster (blessed), *The Sacramentary*, vol. 5** (English,
  Burns Oates & Washbourne, 1930), the All Saints chapter, printed pp.
  208–212: OCR artifact `…ia-volume-5-ocr-65192aa1` (SHA-256 `65192aa1…9a11`),
  physical lines 13898–14128; the registered chapter PDF
  `…all-saints-research-chapter-volume-5-d55b5905` carries the page images
  (parent PDF pp. 228–232) but was not inspected by this research and is not
  bound; every Schuster claim below rests on the bound OCR. Read: the collective feast of martyrs in
  fourth-century Syria; the Byzantine Sunday after Pentecost; the Würzburg
  Comes's short-lived *Dominica in natale Sanctorum*; Boniface IV's Pantheon
  dedication (13 May) and Gregory III's oratory; the November date under
  Gregory IV with Louis the Pious; Sixtus IV's octave. Element by element:
  the Introit *Gaudeamus* was originally St Agatha's (5 February); the
  Collect already stands in the Gelasian for a collective feast of Apostles
  in the octave of Ss Peter and Paul; the Lesson is "significant of the
  origin of the feast" and is the Pantheon dedication's own lesson (his
  citation "Apocalypse, viii, 2–12" is a misprint for vii — §6); the sealing
  with the Tau of Ezechiel, *signa Tau super frontem virorum gementium*; the
  Gradual *Timete Dominum* is also St Cyriacus's (8 August); the Alleluia
  verse "prepares" the Gospel as the Lord's invitation to those faint beneath
  the cross; the Gospel "can be no other" than the Beatitudes, "the decalogue
  of happiness"; the Offertory reads the martyrs' deaths as life in God's
  hand, the persecutor believing their lives are in his; the Secret and
  Postcommunion are quoted and glossed (*fideles populi* as the people
  journeying toward eternity in the light of faith); the medieval
  sacramentaries' proper Preface (*Vere dignum… ut cum exsultantibus sanctis
  in caelestis regni cubilibus gaudia nostra subiungas*) is quoted as
  history — it is **not** the 1962 appointment, and the studies must not
  present it as such; the Damasus inscription from the Cemetery of Callixtus
  closes the chapter.
- **Prosper Guéranger's *Liturgical Year*, continued by Lucien Fromage**,
  French Oudin edition, vol. 15 (the November volume), *La Toussaint*, *A la
  Messe*: artifact `…french-oudin-1909-volume-15.ia-djvu-text-6301674b`,
  physical lines 7891–8546. Per decision D7 of the edition's record this
  volume is Fromage's continuation; the standing row `lucien-fromage` is
  ecclesiastical-writer, and the row `prosper-gueranger` is servant-of-god.
  Read element by element: the Introit recalls the Assumption's and the feast
  completes Mary's triumph; the Collect reads the Church on earth as exiled
  sinners who hope in the multiplied intercessors; the Lesson is a "second
  census" after the emperor's first at the Nativity (citing Gregory's
  homily for the Christmas midnight lesson), the enrolment in the book of
  life against the beast's mark; the Gradual's fear is filial, not servile,
  the trembling of the angelic Powers (citing the Mass Preface's own words);
  the Alleluia verse is the homeland's echo in exile; the Gospel sets the
  mountain of the beatitudes against Sinai's threats, the beatitudes as the
  portrait of the Son of Man and the Church's only ideal; the Offertory has
  the beatitudes raising man above torments and death, which consummates the
  just man's peace; the Secret glorifies God, honours the saints, and wins
  the supreme goodness; the Communion repeats the Gospel's last three
  beatitudes joined to the Sacrament; the Postcommunion prays perpetual
  veneration and protection.
- **William Durandus (ecclesiastical-writer), *Rationale divinorum
  officiorum* VII.34, *De festo omnium Sanctorum***: artifact
  `…1568-durandus-and-beleth-composite.ia-djvu-ocr-2bd5ccb5`, physical lines
  67273–67482 (printed pp. 798–799 of the composite). Read whole: the
  Pantheon built for Cybele and all the gods; Boniface IV obtains it from
  Phocas and dedicates it *quarto Idus Maii* to Blessed Mary and all martyrs
  (*festum beatae Mariae ad martyres*), no feasts of confessors yet
  existing; Gregory IV transfers the feast to the Kalends of November so
  that, the harvest gathered, provisions for the crowds are easier; the feast
  extended to Trinity, angels, confessors and all the elect; **four causes**
  of the institution (the temple's dedication; the supplying of omitted
  saints' feasts; the expiation of negligence in feasts kept — quoting the
  sermon read that day, *Decretum est ut die ista omnium Sanctorum memoria
  habeatur…*; and the easier gaining of petitions, quoting the Collect's
  *multiplicatis intercessionibus largiaris* — note the variant
  *intercessionibus* against the 1962 *intercessoribus*, §6); the day's fast;
  the office's ninefold order (Trinity, B. Mary, angels, prophets, apostles,
  martyrs, confessors, virgins, all together) with the descending rank of
  readers; and his own Mass assignment — Epistle *Ecce ego Ioan.* (his
  chaptering "Apoc. v"), Alleluia *O quam gloriosum* (Apoc. vii), Gospel
  *Videns Iesus turbas* (Mt v), vigil Epistle and Luke vi — which differs
  from the 1962 assignment in the Alleluia and shows the formulary's
  stability only in the Gospel. Durandus also (VII.47, *De virginibus*, line
  69660) assigns *Gaudeamus omnes in Domino* to St Agatha, matching
  Schuster's note on the Introit's origin.
- **John Beleth (ecclesiastical-writer), *Summa de ecclesiasticis officiis***:
  artifact `…latin-migne-pl-202.ia-djvu-ocr-22b781bf` (SHA-256 `22b781bf…`),
  cap. CLVIII *De festo Omnium Sanctorum* at physical line 10894 (PL 202
  col. 160) and cap. CXXVII *De festo B. Mariae ad Martyres* at line 9179
  (Pantheon, Boniface IV and Phocas, and the November transfer because May
  lacks provisions). Read: Beleth gives the office's variety following the
  variety of the saints (Trinity, B. Mary, angels, prophets, apostles,
  martyrs, confessors, virgins, all saints) and the reading-order hierarchy;
  he does not gloss this Mass's elements. **Attribution caution found while
  reading:** the *Wis 3:1* quotation in the same volume at lines 80754–80756
  is inside Peter of Celle's *Tractatus de disciplina claustrali* (its title
  at lines 79890–79912, col. 1097; running heads *PETRI CELLENSIS* and *TRACT.
  DE DISCIPLINA CLAUSTRALI* throughout), not Beleth's; any use must credit
  Peter of Celle (no standing row; ecclesiastical-writer by genre), not
  Beleth (§3.7).
- **Negative within the commentators.** Honorius Augustodunensis, Sicard of
  Cremona, Rupert of Deutz, Amalarius, Berno and Bernold have standing rows
  but no registered All Saints chapter was located in held texts this stage;
  they are unopened leads (§7).

### 3.2 Ps 32:1 — Introit verse

- **Augustine (father), *Enarrationes in Psalmos*, Ps 32 (Vulgate; the NPNF
  numbers it "Psalm XXXIII")**: artifact
  `…enarrationes-in-psalmos.english-npnf8-ccel-web-2026-09-05.ccel-npnf108-text-d6841950`
  (SHA-256 `d6841950…`), physical lines 7871–8011. At v. 1 (lines
  7873–7876): "Rejoice in the Lord, O ye righteous: rejoice, O ye righteous,
  not in yourselves" — the joy is in the Lord, not in one's own justice; and
  "praise is comely to the upright," the upright being those who submit to
  the Lord. At v. 12: the "blessed nation whose God is the Lord" is the one
  nation belonging to the heavenly city.
- **Robert Bellarmine (doctor), *Commentary on the Book of Psalms*, Ps 32
  (his numbering XXXII)**: artifact `…historical-text-357551e1` (SHA-256
  `357551e1…`), head of the psalm at physical line 1131. Read: v. 1's
  rejoicing includes praising with joy; the just are the upright of heart;
  v. 2's ten-stringed instrument is the decalogue observed in conduct.
- **Coverage note.** Cassiodorus's *Expositio Psalmorum* is held only for
  Psalms 39, 70, 85, 97 and 101 — Ps 32 is not held (§7). Theodoret (PG 80)
  is a remote-only lead, not fetched (§7). Aquinas's *Super Psalmos* (Parma
  vol. 14 OCR) was searched; its Ps 32 lectio was located but not read at the
  verse, Ps 33 being the appointed psalm (§7, proportionate). Athanasius's
  *Expositiones in Psalmos* (PG 27, tracked) was not opened (§7).

### 3.3 Apoc 7:2–12 — Lesson

- **Bede (father), *Explanatio Apocalypsis*, on chapter VII** (the whole
  chapter, vv. 1–17): artifact
  `…explanatio-apocalypsis.1878-marshall-parker.whole-text-layer-f4e3b01e`
  (SHA-256 `9417c4a1…`), chapter VII spanning physical lines 1705–2085, read
  whole; the registered passage records cover vv. 4, 9, 10, 11, 12 and 14
  (`…1-7-4`, `…1-7-9`, `…1-7-10`, `…1-7-11`, `…1-7-12`, `…1-7-14`). Reading:
  v. 1's four angels are the four kingdoms (Assyrian, Persian, Greek,
  Roman); the angel ascending from the east (v. 2) is the Lord incarnate,
  bearing the sign of the cross to seal foreheads; the seal (v. 3) is the
  faith of the cross marked on the saints' faces. At v. 4 the definite
  number signifies the whole Church's perfection — from the patriarchs on,
  by nature or by imitation of faith (Gal 3:29), twelve times twelve times a
  thousand, the cube of ten. Verses 5–8 receive a tribe-by-tribe name
  interpretation (Judah, *confession*, first; Benjamin, *son of the right
  hand*, last; Dan omitted). At v. 9 Bede first reads the great multitude
  as those who overcome the last persecution (physical lines 1977–1986),
  and then gives, as an alternative ("may also be thus understood"), the
  Gentiles saved after the tribes of Israel; the robes
  are baptism, the palms the triumph of the cross; v. 10's loud voice is
  unceasing praise; at v. 11 the angels represent the persons of the great
  multitude itself; v. 12 is sevenfold praise; and at v. 14 (registered,
  just past the Missal's end) those washed in the Lamb's blood are **not the
  martyrs alone but the whole Church**. At v. 4 the number already signifies
  "the innumerable multitude of the whole Church" (line 1763). Read together,
  these give the line this study draws from Bede — definite number and
  uncounted crowd are one Church; the formulation is the study's synthesis of
  his v. 4 and his alternative v. 9 reading, not a sentence of his — and it
  is the strongest held answer to the
  formulary's central difficulty (§5.1).
- **Victorinus of Pettau (no standing row), *Commentary on the Apocalypse of
  the Blessed John*, from the seventh chapter** (read in iteration 3): ANF VII
  artifact `…volume-7.ccel-web-2026-10-19.ccel-text-b69327af` (fingerprint
  `f3e73dde…`), the commentary headed at physical line 32802 and its chapter 7
  section at line 33565. He comments only on v. 2 (lines 33567–33618) and v. 9
  (lines 33620–33625). Reading: the angel ascending from the east is **Elias**,
  "the precursor of the times of Antichrist", sent (Mal 4:5–6) "to recall the
  Jews to the faith of the people that succeed them"; "the number of those
  that shall believe, of the Jews and of the nations, is a great multitude
  which no man was able to number"; the Church's prayers are received
  against wrath, and seven archangels smite the kingdom of Antichrist; the
  trumpets and phials tell the same events twice, for "Nor must we look for
  order in the Apocalypse". At v. 9 the multitude "out of every tribe" shows
  "the number of the elect out of all believers, who, being cleansed by
  baptism in the blood of the Lamb, have made their robes white, keeping the
  grace which they have received." He names the 144,000 only on 12:6 (lines
  33964–33974): "in the last times a hundred and forty-four thousands of men
  should believe on the preaching of Elias". **Agreement with Bede:** the
  crowd is the elect drawn from all believers, Jews and nations, and the
  white robes are baptism in the Lamb's blood. **Disagreement:** the angel is
  Elias, not the Lord incarnate; the setting is the last persecution and the
  recall of the Jews; and the 144,000 are the believers at Elias's preaching
  in the last times, not the perfection of the whole Church. **Recension
  caution:** the editor's elucidations (lines 34467–34545) report that "the
  manuscripts must have been much corrupted", that the mention of Genseric
  "proves the subsequent interpolation of his works", that the text may be
  "full of the corrections of some pious disciple of St. Augustine who lived
  much later", and that the author's identity is uncertain; elucidation 9
  sets his chapter 4 use of Dan (Gen 49:16) against Rev 7:5–8, where Dan is
  omitted. The recension behind the English is not established in the
  registered records. Binding 42; deferred (research/source-dispositions.toml).
- **Augustine (father), three brief loci on the Lesson** (read in iteration
  3; none is a commentary on the Apocalypse):
  - *De doctrina christiana* III.35.50–51, the fifth rule of Tichonius (NPNF
    I.2 artifact `…series-1-volume-2.ccel-web-2026-09-17.ccel-text-5c973fed`,
    lines 48865–48909): "twelve into twelve gives one hundred and
    forty-four, which last number is used in the Apocalypse to signify the
    whole body of the saints" (NPNF's note gives Rev 7:4), a number that "has
    not reference to times, but to men". It stands in his account of
    Tyconius's rule, and the text does not separate Tyconius's application
    from Augustine's own. Binding 44.
  - Letter XCIII to Vincentius §30 (NPNF I.1 artifact
    `…series-1-volume-1.ccel-web-2026-10-13.ccel-text-21000696`, lines
    36927–36944): the same Church is few beside the wicked and many in
    herself, and "in the Apocalypse, many thousands 'which no man can
    number,' from every tribe and tongue, are seen clothed in white robes,
    and with palms of victory". Binding 43.
  - Sermon LXI (Benedictine CXI) on Lk 13:21 and 23 (NPNF I.6 artifact
    `ce371798`, lines 43160–43275; the passage at 43193–43212): the few who
    are saved are themselves the many, few beside the lost and many in the
    society of the angels; the Apocalypse's great multitude "coming with
    white robes and palms. This is the mass of the saints." Binding 17.
  Together these make Augustine a second father who agrees with Bede on the
  Lesson's own question: the number signifies the whole body of the saints,
  and the uncounted crowd is the one Church. They are short applications,
  not an exposition of the chapter, and say nothing of the angel from the
  east or of the seal.
- **Robert Bellarmine (doctor), *Commentary on the Psalms*, on Ps 86:2 and
  121:2** (read in iteration 3; artifact `357551e1`, lines 3069 and 4543):
  the twelve tribes' names on the gates of the new Jerusalem signify "that
  the first members of the Church came from the children of Israel… then
  came the fullness of the gentiles", as the Apocalypse first names twelve
  thousand from each tribe "and then follows 'a great multitude; which no
  man could number, of all nations…'"; and the heavenly country is "a
  kingdom by reason of the multitude and the variety of its inhabitants"
  (Apoc 7:9). Analogue reception that seconds Bede's alternative reading of
  v. 9 (Israel first, then the Gentiles). Binding 19.
- **Cyprian (no standing row), *Exhortation to Martyrdom, addressed to
  Fortunatus*, §11** (read in iteration 3; ANF V artifact
  `…volume-5.ccel-web-2026-10-13.ccel-text-a02b61c3`, lines 50321–50342):
  quoting Apoc 7:9–10 and 13–15, he says that "the Christian martyrs cannot
  be numbered" and that "the crowd of martyrs cannot be numbered". A third
  reading of the crowd, as the martyrs, which Bede at v. 14 and the PL 35
  *Expositio* both reject for the whole Church. Binding 45.
- **Anonymous, *Expositio in Apocalypsim*, printed in PL 35's appendix to
  Augustine's works (no standing)** (read in iteration 3 on page images of
  the PL 35 scan `b3ff8a95`, §1): the editors' *Admonitio* (PDF p. 557, cols.
  2415–2416) says the exposition is for the most part stitched together
  (*consarcinata*) from the words of Victorinus, Primasius and Bede, that
  some wished it received as Tyconius's, and that the Louvain theologians
  judged it annotations collected by someone and later put in homily form;
  it names no Caesarius. Homily VI's comment on Apoc 7 (cols. 2426–2427 =
  PDF pp. 562–563) and its recapitulation (col. 2428 = PDF p. 563): the
  144,000 is the whole Church (*tota Ecclesia intelligitur*), and in the
  uncounted multitude *Ecclesia eadem significata est*, from every tribe
  because all nations are grafted into the root by believing; *in stolis
  donum Spiritus sancti intelligitur*; the angels round the throne are the
  Church; the angel ascending from the east is the Church, *ascendens ab
  ortu solis, id est a passione vel resurrectione Domini*; and *Laverunt
  stolas* is said *de tota Ecclesia… non de martyribus tantum*, *quod utique
  per Baptismi sacramentum impletur*. It agrees with Bede on the number, the
  crowd and the robes, but it is an anonymous compilation that, by its
  editors' account, draws on Bede himself; it is reception without standing,
  not an independent witness. Binding 46.
- **Held but not usable, recorded:** Andrew of Caesarea is cataloged-only;
  Cornelius a Lapide and Hugh of St Cher are held in works that do not cover
  this passage; Ambrose Autpert, Beatus, Denis, Rupert, Bruno of Segni,
  Haimo, Primasius, Richard of St Victor — no holdings (`discover` output of
  iteration 0, not kept). Iteration 0 also recorded Victorinus as held in a
  container whose extent does not reach Rev 7. That was false: `discover`
  reported Apoc 7 outside his extent because the containment inventory maps
  his constituent only to Rev 1, 5 and 19 (§10.12), and the artifact was not
  opened at chapter 7 until iteration 3. No Caesarius of Arles text is
  registered (§7).
- **Registration gap, reported:** Bede's passage records cover vv. 4, 9, 10,
  11, 12, 14 but not vv. 2–3 (the angel from the east and the sealing),
  which the Lesson reads and this stage read in the whole text layer. A
  candidate for the registration handoff (§10).

### 3.4 Ps 33:10–11 — Gradual

- **Augustine (father), *Enarrationes*, Ps 33 (Vulgate; NPNF "Psalm
  XXXIV")**: same artifact, physical lines 8012–8624, read whole. The NPNF
  English numbers the verses from the Hebrew-based English psalter, which
  leaves the inscription unnumbered, so its "(ver. 9)", "(ver. 10)" and
  "(ver. 11)" are Vulgate 33:10, 33:11 and 33:12. The Gradual's Vulgate
  vv. 10–11 are NPNF ver. 9–10, at lines 8237–8287. The inscription's David
  "changing his
  countenance before Abimelech" (NPNF's spelling; the Clementine reads
  *Achimelech*) is Christ changing His countenance in the
  priesthood, sent away from the kingdom of the Jews, coming to the Gentiles;
  the "drum" of the title is the flesh of Christ crucified; "carried in His
  own hands" is *This is My Body*. At Vulgate vv. 10–11 (NPNF ver. 9–10): "O
  fear the Lord, all ye His
  saints, for there is no want to them that fear Him" — Augustine faces the
  scandal directly: the wicked rich die in plenty while the seeking poor
  hunger; the resolution is spiritual. On v. 10 (NPNF ver. 9, §13) he
  calls the fearful not to defraud for fear of hunger ("The Lord fed thee
  despising Him, and will He desert thee fearing Him?"). The Living Bread
  (Jn 6) is his answer to the clause "The rich do lack and suffer hunger"
  (v. 11a, *Divites eguerunt*, which the Gradual omits; NPNF §14, lines
  8273–8283), so it must be presented as his comment on the psalm's
  omitted half-verse. On the said v. 11b, "they that seek the Lord shall
  not want any good thing", the good is spiritual riches — justice, truth,
  charity, faith, endurance — and he cites "blessed are they which do
  hunger and thirst after righteousness" (Mt 5:6, the Gospel's own fourth
  beatitude) inside the same section. Context only, outside the Gradual: at Vulgate v. 12 (NPNF
  ver. 11, from line 8289; Clementine *Venite, filii; audite me*), "Come, ye
  children, hearken unto me: I will teach you the fear of the Lord", Augustine
  hears Christ Himself speaking. The Mass does not say this verse, and no
  reading in this study rests on it.
- **Basil (father), *Homily on Psalm 33*** (Vulgate 33; the volume numbers
  it 32 by the Hebrew): PG 29, full-text-layer artifact `…1860-paris.
  full-text-layer-2898b217` (SHA-256 `2898b217…`), the homily's section on
  vv. 10–11 at physical lines 40778–40889 (cols. 365–368), read on the Latin
  column (the artifact's own note records the Greek column as corrupt in
  this layer). At v. 10: unless fear instructs our life, holiness cannot be
  established in the body; fear is to be nailed into the flesh (Ps 118:120);
  he who fears has no lack, being kept from every unseemly act — perfect,
  wanting nothing of the goods of human nature; perfect fear sins nothing.
  At v. 11: *Divites eguerunt* may be Israel (whose is the adoption, Rom
  9:4), made poor by sin, suffering the famine of hearing the word (Amos
  8:11); the Gentiles seeking the Lord are not diminished from any good; the
  perfect good is God Himself; Paul sought the Lord and lacked no good
  despite scourgings and shipwreck (2 Cor 11:25).
- **Bellarmine (doctor), *Commentary*, Ps 33 (his XXXIII)**: same artifact,
  head at physical line 1179. His English counts *I will bless the Lord at all
  times* as v. 1, which is the Vulgate's v. 2, so in this psalm each of his
  verse numbers is one lower than the Vulgate's: his v. 9 (line 1201) is
  Vulgate v. 10 and his v. 10 (line 1203) is Vulgate v. 11. (In Ps 32, which
  has no separately numbered inscription, his numbers agree with the
  Vulgate's.) Read: the psalm is alphabetical; the fear of Vulgate v. 10 (his
  v. 9) is the **filial** fear proper
  to saints and the perfect — the perfect lover fears offending; "no want"
  in the higher sense means feeling no want, since the friend of God
  possesses everything, and in the lower sense God supplies temporal
  necessities; at Vulgate v. 11 (his v. 10) the rich are reduced to want while seekers of the
  Lord want no good because they cling to the Supreme Good.
- **Thomas Aquinas (doctor), *Super Psalmos*, on Ps 33:9–11** (Vulgate
  numbering): Parma vol. 14 OCR artifact `…opera-omnia-volume-14.1863-parma.
  ia-complete-ocr-02c6dc25` (SHA-256 `31b59669…`), physical lines
  42579–42664. Read: at *Gustate et videte* the experience of God's goodness
  is "tasting" because God is not far off but within (Jer 14); at v. 10
  *Timete Dominum omnes sancti eius* — no one is holy without fear, which is
  needed not only by those ascending to holiness but by those remaining in
  it (Eccl 27), fear being the bridle of pride; *non est inopia timentibus
  eum* is expounded of spiritual goods (the fear of the Lord is the
  treasure, Isa 33) and of bodily goods, since the God-fearing is content
  with what he has (Phil 4). Aquinas then puts **Augustine's objection**
  (from *De sermone Domini in monte*): the Apostle says "unto this hour we
  hunger and thirst and are naked" (1 Cor 4) — how then no want? — and
  answers: God is nourisher and physician, and as a physician withdraws
  food from the sick for their health, so God sometimes sends want,
  sometimes wealth. At v. 11 the *Divites* are those who give their souls to
  riches — rich in worldly things, poor in spiritual (Apoc 3, Laodicea).
- **Coverage:** Cassiodorus's held psalms do not include 33; Theodoret
  remote-only; Athanasius unread (§7).

### 3.5 Mt 11:28 — Alleluia verse

- **John Chrysostom (father), *Homily 38 on Matthew***: NPNF I.10 artifact
  `…series-1-volume-10.ccel-web-2026-09-17.ccel-text-adb8f1c9` (SHA-256
  `adb8f1c9…`), homily at physical lines 23727–24161, the verse at
  23880–23958. Read: "Come unto me, all ye that labour" — all who are in
  anxiety, sorrows and sins; not "I will save you only," but "I will place
  you in all security"; the yoke is easy if one is lowly and meek; rest is
  given to souls even here; sin's burden is the heavy one (Ps 37; the
  "talent of lead" of Zacharias); virtue gives wings.
- **Augustine (father), Sermon XIX (Benedictine LXIX), on Mt 11:28**: NPNF
  I.6 artifact `…series-1-volume-6.ccel-web-2026-09-17.ccel-text-ce371798`
  (SHA-256 `ce371798…`), physical lines 30137–30246. Read: "Come unto Me,
  all ye that labour" — that ye may labour no more; take the yoke, learn
  meekness and lowliness; the foundation of humility is dug deep for the
  building whose top reaches the Vision of God; we cannot flee from God, who
  is everywhere, so we fly to His presence.
- **Gregory the Great (father), *Moralia in Iob***: complete-text
  artifact `…complete-text-d9f9ed86` (SHA-256 `f86bcd2a…`); the phrase
  *Venite ad me omnes qui laboratis* is indexed at physical lines 1126,
  25115, 29352, 32511, 33807, 47672. These are phrase occurrences inside
  other expositions; they were indexed, not read in context this stage, and
  are registered as indexed reception, not as an exposition of the verse
  (§7).

### 3.6 Mt 5:1–12 — Gospel

- **Augustine (father), *De sermone Domini in monte* I.1–5**: NPNF I.6
  artifact, physical lines 585–1188, read. The sermon is the perfect
  standard of the Christian life; the mountain is the greater precepts of
  righteousness, the same God giving the lesser by fear and the greater by
  love; the poor in spirit are the humble and God-fearing (the fear of the
  Lord the beginning of wisdom; pride the beginning of sin); the beatitudes
  are a seven-stage ascent mapped to the seven gifts of Isa 11
  (fear→piety→knowledge→fortitude→counsel→understanding→wisdom); the eighth
  returns to the starting-point (circumcision on the eighth day, the
  resurrection on the eighth day, Pentecost as 7×7+1) and is perfection; the
  rewards are one kingdom variously named, promised and in part fulfilled in
  this life (in the apostles), perfected after; "falsely and for my sake"
  excludes heretics and schismatics; the reward in heaven is the spiritual
  firmament.
- **John Chrysostom (father), *Homily 15 on Matthew***: NPNF I.10 artifact,
  physical lines 8742–9261, read. The withdrawal to the mountain is not for
  display; He teaches even in silence by His works ("opened His mouth");
  through the disciples He addresses all; the poor in spirit are the humble
  and contrite by choice, awe-struck (Isa 66:2); humility is the foundation
  as pride is the root of all evil (the devil, Adam); the beatitudes are
  blessings, not commandments; mourning is for sins, one's own and others'
  (Moses, Paul, David); the meek inherit the earth — a sensible prize
  mingled with the spiritual; hunger for righteousness against
  covetousness; the merciful obtain a mercy far exceeding; the pure in
  heart see God as far as is possible for man; peacemakers do the work of
  the Only-Begotten; persecution for righteousness' sake; the rewards all
  shadow the one Kingdom; the beatitudes are a golden chain, each virtue
  linked to the next; the prophets' fellowship; "ye are the salt of the
  earth" — for the whole world.
- **Hilary (father), *In Matthaeum*, caput IV**: PL 9 artifact
  `…1844-paris.ia-djvu-text-db389fea` (SHA-256 `1ffb9ec5…`), physical lines
  ~73730–73862 (cols. 934–935), read. Christ on the mountain, in the height
  of paternal majesty, sets the precepts of the heavenly life; the poor in
  spirit possess the kingdom through humility; the meek inherit the earth —
  which Hilary reads as the body the Lord assumed as His habitation (Christ
  dwells in us by meekness, and we are clothed with His glorified body);
  the mourners weep for old sins; the hungry are the saints' eagerness for
  teaching, filled with perfect goods in heaven; the merciful obtain mercy;
  the pure in heart see God — nothing polluted meets the divine brightness,
  and only the perfected in spirit, changed into immortality, see; the
  peacemakers receive the adoption's reward, one Father; the persecuted are
  the perfect in affection; a copious reward in heaven is reserved for the
  confessors and martyrs of the heavenly justice.
- **Thomas Aquinas (doctor), *Super Matthaeum*, cap. 5**: Venice 1745 tomus
  3 OCR artifact `…veneta-bettinelli-1745.ia-djvu-ocr-10aa155e` (SHA-256
  `9fcd4856…`; source fingerprint
  `sha256:9fcd48561f23ea12b2a7271b5cbcdeaee88f85652a5194fe6756bfb2b4aa558f`),
  physical lines 9400–9659
  and 10393–10462, read. He follows Augustine: in this sermon is the whole
  perfection of life; four false opinions of beatitude are reproved and
  ordered (exterior wealth; the satisfaction of appetite; the active
  virtues; the contemplative life as attainable in via) — the active
  virtues are ways, not beatitude itself; beatitude is finally the vision of
  God with love's delight; each beatitude is merit and reward; the rewards
  are perfect in patria, inchoate in via (*regnum Dei intra vos est*); the
  gifts-mapping is Augustine's; the eighth beatitude is the perfection of
  all the preceding (the furnace proves the just, Eccli 27:5); persecution
  does not make blessed, but its cause does (*propter iustitiam*, citing
  Chrysostom against those who suffered *pro fide* from pagans); at *Beati
  estis…* three sustainables are named: contumely in words, injuries in
  deeds, detractions in absence; Jerome via the gloss: where Christ is the
  cause, malediction is to be welcomed (1 Pet 4:14).
- **Rabanus Maurus (saint), *Expositio in Matthaeum*, on Mt 5**: PL 107
  artifact `…1864-paris.ia-djvu-text-5b8a4b8b` (source fingerprint
  `sha256:f46dd80fe29ddd52cbaf7d81009b328bf011400b6917c0473b5f04f9bb443bae`),
  read at physical lines 92120–92145 and
  93900–93960. Rabanus compiles: at 5:11–12 he quotes Augustine's *De
  sermone Domini* explicitly (the inline attribution "(Aug.)" is printed),
  and in the Lord's Prayer section he maps the seven petitions onto the
  beatitudes with the gifts (*timor Dei, quo beati sunt pauperes spiritu…*).
  He is a derivative but saintly witness to the Augustinian reading.
- **Held, not read:** Jerome's *In Matthaeum* on Mt 5 (PL 26, cols. ~32–38)
  is held only as column facsimiles of later chapters and a remote whole PDF
  — no tracked text; the facsimiles do not cover cap. 5. Recorded as an
  unopened lead with a proportionate-search note (§7).

### 3.7 Wis 3:1–3 — Offertory

`tools/tpt source-library discover --passage "Wisdom 3:1-3"` returns no
mapped commentary; none is held. The reception found is **patristic and
liturgical use of the verse**, which is itself the evidence for this
adapted antiphon:

- **John Chrysostom (father), *Homily 28 on Matthew*** (on the Gadarene
  demoniacs): NPNF I.10 artifact, physical lines ~17896–18119. Arguing that
  the souls of the dead cannot wander the earth, he quotes "the souls of the
  righteous are in the hand of God" (Wis 3:1) at line 18097. A direct
  patristic reception of the antiphon's first clause.
- **Gregory the Great (father), *Moralia***: complete-text artifact,
  Book XII, chapter v, paragraph 6, on Job 14:8–9 (the lemma at physical
  lines 19542–19543): Wis 3:2 is quoted at line 19554 of the righteous man
  whose stock dies in the dust, his body bereft of life amid the
  persecutors. Further indexed occurrences stand at 38149, 19694 and
  following.
- **Augustine (father), *Enarrationes in Psalmos*, Ps 118 Vulgate (NPNF
  "Psalm CXIX", section *Nun*)**: NPNF VIII artifact, comment 108 on
  ver. 109, physical lines 58646–58658. On "My soul is alway in Thy hand"
  he notes that some copies read "in my hand" but most "in Thy hand", which
  he calls easy, "For 'the souls of the righteous are in God's hand'"
  (line 58648; NPNF's note [5293] gives Wisd. iii. 1). The NPNF English
  here is abridged (an editorial ellipsis at line 58654).
- **Peter of Celle, *Tractatus de disciplina claustrali*** (printed in the
  PL 202 volume artifact `…latin-migne-pl-202.ia-djvu-ocr-22b781bf`, lines
  80751–80756; §3.1 for the attribution): the monk commends his spirit to
  God (Ps 30:6) so that the torment of malice may not touch him, "quia
  Justorum animae in manu Dei sunt, et non tanget illos tormentum malitiae
  (Sap. iii, 1)", as the OCR layer reads. This is a non-Missal witness to
  the *tanget* and *malitiae* wording. It does not date this feast's
  Offertory.
- **Alphonsus Liguori (no standing row, §10), *Apparecchio alla morte***: cites the
  verse (artifact `d25bba22`); later saintly reception, indexed.
- **The 1570 Missal (Venice), read at the locus in the iteration-1 repair.**
  In the text artifact `…venice-1570.missale-romanum-1570-text-563f4dd2`
  the All Saints Mass opens at physical line 71573 (*In festo omnium
  Sanctorum*); after the Gospel and the cue *Credo* the feast's Offertory
  stands at lines 71705–71709: *Iustorum anime in manu dei sunt: et non
  tanget illos tormentum mortis: visi sunt oculis insipientium mori, illi
  autem sunt in pace.* The 1570 feast therefore reads **tormentum mortis,
  with no alleluia**: the same selection from 3:1–3 as the 1962 antiphon
  and the same *tanget* (without *autem* after *Iustorum*), but the
  Clementine's *mortis*. The two other lines the index reported belong to
  other Masses and are not this feast's text: line 62448 is the Communion
  of Ss Marcellinus, Peter and Erasmus (2 June; the Mass opens at line
  62382), and lines 68676–68680 are the Gradual of Ss Felix and Adauctus
  (30 August; the Mass opens at line 68657). Both read *tormentum
  malitiae*, without alleluia, so the *malitiae* wording was current in
  1570 in martyrs' Masses while the All Saints Offertory still read
  *mortis*.
- **Later Missal printings, read on their text layers only (no page images
  read).** The 1604 Vatican typical edition (text artifact
  `…vatican-typica-1604.missale-romanum-1604-text-6d12feef`, two-column OCR
  interleaved, lines 53517–53525), the Pustet 1862 Ratisbon text layer
  (`…pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`, lines
  77748–77753, about printed p. 570) and the Desclée Tournai 1889 OCR
  (`…1889-tournai-desclee-leo-xiii-recognitum.ia-djvu-ocr-715f57fd`, lines
  77695–77699) all print the feast's Offertory with *tormentum malitiae*
  and **no alleluia**. Guéranger-Fromage 1909 (vol. 15, line 8434 onward,
  printed p. 99) gives the same form. The Mame 1922 (checked artifact
  `415a1d46`) is the earliest held witness with both *malitiae* and the
  closing *alleluia*, as in 1962.
- **What this establishes, and what it does not.** On the held witnesses,
  *mortis* gave way to *malitiae* in this feast's Offertory between the 1570
  and the 1604 printings; the 1604, 1862 and 1889 readings rest on OCR text
  layers, not on page images. The *alleluia* is absent from every held
  witness through 1909 and present in the Mame 1922, an edition printed
  *iuxta typicam* (by its registered title, presumably the 1920 typical
  edition, which was not read). When and by which act it entered is
  **unresolved**:
  no 1920 typical edition, no other printing between 1909 and 1922, and no
  decree on the point is held and read (the registered 1920 typica text
  record is remote and was not read). The study states the change; it does
  not date it more closely.
- **The Clementine** (verse artifact `…verse-text-25-wisdom-bfeace21`, line
  43): *Justorum autem animæ in manu Dei sunt, et non tangent illos
  tormentum mortis.* Against Wis 3:1–3 the 1962 antiphon omits *autem*,
  reads *tanget* for *tangent* and *malitiae* for *mortis*, omits 3:2b–3a
  (*et æstimata est afflictio exitus illorum, et quod a nobis est iter
  exterminium*), and adds *alleluia*; the collation is in
  `propers/verified.md` and the difference is weighed in §5.3.

### 3.8 Mt 5:8–10 — Communion

The Communion re-reads the Gospel's sixth, seventh and eighth beatitudes;
its reception is the Gospel's (§3.6), with each witness's treatment of the
three verses: Augustine (the pure heart's vision as the reward's core; the
peacemakers' sonship; the eighth as the return to the first, enclosing the
octave), Chrysostom (peacemakers doing the Only-Begotten's work; persecution
for righteousness), Hilary (only the perfected see God; the confessors' and
martyrs' copious reward), Aquinas (the eighth beatitude as the perfection of
all; vision of God as beatitude itself). Schuster and the continuation read
the placement itself: the Church receives in the Sacrament the three
beatitudes she has just heard — purity, peace, persecution — "the three
last beatitudes" (Guéranger-Fromage); the Communion is "from the Gospel"
(Schuster).

### 3.9 The feast's orations — composed texts

Collect, Secret and Postcommunion have no biblical source. Reception found:
Schuster places the Collect in the Gelasian for a collective Apostles' feast
(§3.1) and glosses the Secret (*pro cunctorum tibi grata sint honore
iustorum*) and Postcommunion (*fideles populi* as the journeying people of
faith); Durandus quotes the Collect's petition (*multiplicatis
intercessionibus*, §6) as the feast's fourth cause — the easier gaining of
petitions because "it is impossible that the multitude should not be
heard"; the continuation reads the Collect as the exiled sinners' hope in
multiplied intercessors and the Postcommunion as perpetual veneration and
protection. The Introit antiphon *Gaudeamus omnes in Domino* is likewise a
composition: originally St Agatha's (Durandus VII.47; Schuster), extended
by the feast.

### 3.10 The commemoration's orations — composed texts

*Absolve, quaesumus* (Collect), *Pro nostrae servitutis augmento* (Secret),
*Quaesumus, omnipotens Deus* (Postcommunion) are the Twenty-third Sunday's
own; they enter this Mass only as the privileged commemoration. No
commentary reception was swept for them this stage (the plan does not open
the commemorated Sunday); their textual basis is settled
(`propers/verified.md`). Their thematic bearing — pardon of guilt, increase
of servitude's offering, protection from human perils — is used only where
an interpretation notes the juxtaposition, and is marked as editorial
observation there.

## 4. Witness register

| Witness | Work read | Standing (author-standing-v1.toml) | Role this stage |
|---|---|---|---|
| Augustine | *Enarrationes* on Ps 32, 33; *De sermone Domini in monte* I; Sermon XIX; on Apoc 7: *De doctrina christiana* III.35, Letter XCIII §30, Sermon LXI | father | reception, carrying-eligible |
| Bede | *Explanatio Apocalypsis* on Apoc 7 | father | reception, carrying-eligible |
| Basil of Caesarea | *Homily on Ps 33* | father | reception, carrying-eligible |
| Hilary of Poitiers | *In Matthaeum* cap. IV | father | reception, carrying-eligible |
| John Chrysostom | *Homilies on Matthew* 15, 28, 38 | father | reception, carrying-eligible |
| Gregory the Great | *Moralia* (indexed occurrences; Book XII, chapter v, paragraph 6 read) | father | indexed reception |
| Thomas Aquinas | *Super Matthaeum* cap. 5; *Super Psalmos* on Ps 33 | doctor | reception, carrying-eligible |
| Robert Bellarmine | *Commentary on Psalms* 32, 33; 86 and 121 (Apoc 7 analogue) | doctor | reception, carrying-eligible |
| Rabanus Maurus | *Expositio in Matthaeum* on Mt 5 | saint (per 2004 Martyrology; maintainer-settled 2026-09-23) | derivative reception |
| Alphonsus Liguori | *Apparecchio alla morte* (indexed) | **no standing row** — §10 | indexed reception, lead |
| Ildefonso Schuster | *The Sacramentary* V, All Saints chapter | blessed | liturgical commentary, second-author-eligible |
| Prosper Guéranger / Lucien Fromage | *Liturgical Year*, French vol. 15, La Toussaint | servant-of-god / ecclesiastical-writer (continuation per decision D7) | liturgical commentary, never carrying |
| William Durandus | *Rationale* VII.34 (and VII.47) | ecclesiastical-writer | liturgical commentary, never carrying |
| John Beleth | *Summa* capp. CXXVII, CLVIII | ecclesiastical-writer | liturgical commentary, never carrying |
| Peter of Celle | *Tractatus de disciplina claustrali* (printed in the PL 202 volume), Wis 3:1 quotation | no row; ecclesiastical-writer by genre | phrase reception, attribution caution |
| Jerome | *In Matthaeum* cap. 5 | father | held as facsimiles/remote PDF only — unopened lead |
| Cassiodorus | *Expositio Psalmorum* | ecclesiastical-writer | held psalms exclude 32/33 — negative |
| Theodoret | *In Psalmos* (PG 80) | ecclesiastical-writer | remote-only — unopened lead |
| Athanasius | *Expositiones in Psalmos* (PG 27) | no row | tracked, unread — unopened lead |
| Bernard of Clairvaux | (All Saints sermons are a known lead) | **no standing row** — §10 | not registered for this feast |
| Victorinus of Pettau | *Commentary on the Apocalypse* (ANF VII): chapter 7 on vv. 2 and 9, 12:6, elucidations | **no standing row** — §10 | developed reception on the Lesson, never carrying; recension caution (§3.3) |
| Cyprian of Carthage | *Exhortation to Martyrdom, to Fortunatus* §11 (Apoc 7:9–15 quoted) | **no standing row** — §10 | rival reception (the crowd as the martyrs), never carrying |
| Anonymous (printed in PL 35 among Augustine's spuria) | *Expositio in Apocalypsim*, Admonitio cols. 2415–2416, Homily VI cols. 2426–2428 | no row; anonymous compilation | dependent reception agreeing with Bede, never carrying |
| Patrick L. Murphy | *The New Rubrics of the Roman Breviary and Missal* (1960), printed pp. 93, 192–193 | no row; modern rubrical commentator, not a Scripture witness | rubrical context only (binding 41), not citable |

Missing standing rows for Bernard, Victorinus, Cyprian, Gregory of Nyssa,
Alphonsus Liguori, Athanasius and Peter of Celle are reported in §10;
Victorinus and Cyprian are now read witnesses on the Lesson (§3.3). The
registry gives Gregory the Great the one standing *father*. Per the carrying
rule, no witness without a row carries
an interpretation in `research/interpretations.md`.

## 5. Passage-level difficulty tests

### 5.1 The definite number and the uncounted crowd (Apoc 7:4 against 7:9)

The Lesson counts exactly 144,000 sealed from the tribes, then shows a
multitude *quam dinumerare nemo poterat*. Read flatly, the vision either
contradicts itself or restricts salvation to a numbered Israel. Bede's
chapter VII is the principal held resolution: the definite number signifies the whole
Church's perfection (twelve times twelve times a thousand, the cube of
ten), drawn from the patriarchs by nature or by imitation of faith (Gal
3:29). At v. 9 Bede first reads the uncounted multitude as those who
overcome the last persecution, and only then offers, as an alternative
("may also be thus understood"), the Gentiles joined to the Church after
Israel. "One body seen in two aspects" is this study's synthesis of the v. 4
reading with that alternative, not Bede's own settled formula; at v. 14 Bede extends the white
robes beyond martyrs to the whole Church washed in the Lamb's blood. The
continuation reads the same verses as the "second census": the enrolled
against the marked of the beast, the enrolment in the book of life. The two
readings differ (ecclesial totality against eschatological enrolment) and
are preserved (§6).

The patristic witnesses read in iteration 3 (§3.3) divide on the same words.
Augustine agrees with Bede on both halves: 144 "is used in the Apocalypse to
signify the whole body of the saints" (*De doctrina christiana* III.35.51,
in his account of Tyconius's rule), and the uncounted crowd in white robes
is the one Church, few beside the lost and many in herself, "the mass of
the saints" (Letter XCIII §30; Sermon LXI). Bellarmine on Ps 86:2 gives
Bede's alternative order, the tribes first and then the nations. The
anonymous PL 35 *Expositio* takes Bede's side throughout (*tota Ecclesia*;
the robes washed by the whole Church in baptism, not by martyrs only), but
it draws on Bede and cannot count as an independent witness. Victorinus,
the oldest Latin commentary held, answers differently. He agrees that the
crowd is the elect from all believers, of the Jews and of the nations, made
white in baptism (7:2, 7:9). But he makes the angel from the east Elias,
sets the vision in the last persecution under Antichrist, and, at 12:6,
takes the 144,000 as those who believe at Elias's preaching in the last
times: a particular eschatological company, not the whole Church's
perfection. Cyprian reads the crowd as the innumerable martyrs, the reading
that Bede (v. 14) and the *Expositio* reject. What these answers change: on
Bede's and Augustine's reading the number and the crowd are one Church,
which is what makes the Lesson the feast's own; on Victorinus's the number
is a part (those who believe at Elias's preaching in the last times) and
the crowd the whole; on Cyprian's the crowd is the martyrs, and the feast's extension to
all the saints would need another ground. The record keeps all four
answers. An interpretation that cannot say who the 144,000 are, or that
silently drops the number for the crowd, fails this test.

### 5.2 "Nihil deest timentibus eum" against the hungering saints (Ps 33:10–11; Mt 5:6)

The Gradual promises no want to those who fear the Lord; experience shows
the wicked rich in plenty (Augustine's scandal, En. Ps 33) and the apostles
themselves hungering and naked (1 Cor 4, Aquinas's objection, raised from
Augustine's *De sermone Domini*). The held answers agree in shape and
differ in accent: Augustine — the want is spiritual; the rich lack the
Living Bread (his comment on the omitted *Divites eguerunt*, §3.4), and the hunger that is blessed is hunger for righteousness
(Mt 5:6, the Gospel's own verse, cited inside the psalm's exposition);
Aquinas — God is nourisher and physician and sometimes sends want for
health; Bellarmine — in the higher sense the God-fearing *feel* no want,
owning everything in friendship with God; in the lower, God supplies;
Basil — the fear that is nailed into the flesh lacks nothing because it
sins nothing, and the *Divites* may be Israel itself, starved of the word
(Amos 8:11), while Paul, seeking the Lord, lacked no good under scourgings
and shipwreck. The Missal's own selection sharpens the difficulty by
cutting *Divites eguerunt* (v. 11a): the verse about the rich is left
unsaid, and the Gradual states the promise without its foil. An
interpretation that reads *nihil deest* as a promise of temporal comfort
fails; one that cannot say why the Mass omits v. 11a has not read the
formulary.

### 5.3 "They seemed to die" — the Offertory's adapted Wisdom (Wis 3:1–3)

The antiphon says the just, who *seemed to die in the sight of the unwise*,
are in peace — and the Missal changes the Clementine's *tormentum mortis*
to *tormentum malitiae* and appends *alleluia*. The difficulties: (1) the
textual one — the received liturgical form is not the verse, and a study
that quotes the Clementine as the Offertory misquotes the Mass
(`propers/verified.md` carries the collation); (2) the theological one —
the verse in context answers the impious who "condemn the just man to a
shameful death" (Wis 2:20), so the antiphon sang over the offering names
the martyr's death as non-death; Chrysostom (Hom. 28) uses Wis 3:1 against
the wandering of dead souls — the dead just are in God's hand, not abroad;
Schuster reads the persecutor's error (he believes the martyrs' lives in
his hands; they are in God's). The *malitiae*/*mortis* variant has a
witnessed history (§3.7): the 1570 Missal's own All Saints Offertory still
reads *tormentum mortis* without alleluia; the held printings from 1604 to
1889 (text layers) read *malitiae* without alleluia, the wording the 1570
already used in martyrs' Masses; the Mame 1922 is the first held witness
with the closing *alleluia*. When the alleluia entered is unresolved. No
resolution of the variant itself is imposed (§6).

### 5.4 Present kingdom, future reward (Mt 5:3, 10 against 5:4–9; Ps 33)

The first and eighth beatitudes say *ipsorum **est** regnum caelorum*;
the six between say *shall be* comforted, filled, shown mercy, shall see
God. Augustine: one kingdom, variously named, begun in this life (in the
apostles), perfected after; the eighth beatitude returns to the first —
perfection enclosing the octave. Aquinas: the rewards are inchoate in via
(*regnum Dei intra vos est*), consummate in patria; beatitude itself is the
vision of God with love's delight. Chrysostom: sensible and spiritual
prizes are mingled — the meek inherit the earth now. Hilary: only the
perfected, changed into immortality, see God. On a feast that celebrates
the saints already reigning, the present tense does the work; an
interpretation that postpones everything to the last day, or that collapses
the future tenses into mere present devotion, fails the text.

## 6. Material disagreements preserved

1. **The sealed number, the crowd and the angel (§5.1):** (a) The number:
   Bede (the whole Church's perfection), with Augustine (*De doctrina
   christiana* III.35.51: the whole body of the saints) and the anonymous PL
   35 *Expositio* (*tota Ecclesia*), against Victorinus (on 12:6, those who
   believe at Elias's preaching in the last times) and the continuation's
   eschatological enrolment ("second census"). (b) The crowd: Bede's first
   reading (the victors over the last persecution) and his alternative (the
   Gentiles gathered after Israel, with Bellarmine on Ps 86:2); Augustine and
   the *Expositio* (the one Church); Victorinus (the believers of the Jews
   and of the nations, and at v. 9 the elect from all believers); against
   Cyprian (the innumerable martyrs), whose reading Bede at v. 14 and the
   *Expositio* reject. (c) The angel ascending from the east: Bede, the Lord
   incarnate; Victorinus, Elias the precursor; the *Expositio*, the Church
   rising from the Lord's passion or resurrection.
2. **"Divites eguerunt" (Ps 33:11a):** Basil's Israel reading against
   Augustine's spiritual-rich reading against Bellarmine's two-sense
   reconciliation; and the Missal's omission of the half-verse against all
   three expositions, which presume it.
3. **Offertory wording:** the 1962 *tormentum malitiae* against the
   Clementine's *tormentum mortis*, which the 1570 Missal's own All Saints
   Offertory still reads (§3.7); *malitiae* is held for this feast from the
   1604 printing (text layer) and in 1570 only in martyrs' Masses; the
   selection and the added *alleluia* (first held in the Mame 1922; entry
   unresolved) are recorded, not harmonized.
4. **The Collect's petition word:** the 1962 *multiplicatis
   intercessoribus* against Durandus's quotation *multiplicatis
   intercessionibus* (VII.34) — a medieval reading of the same prayer.
5. **Schuster's citation:** his "Apocalypse, viii, 2–12" for the Lesson is a
   misprint or slip for vii; recorded so the study cites Apoc 7:2–12.
6. **The feast's early date:** Durandus has the Pantheon dedicated *quarto
   Idus Maii* and Gregory IV's transfer to the Kalends of November "so
   that provisions may be found more abundantly after the harvest"; Beleth
   has the same transfer rationale (May lacks provisions); Schuster dates
   the November choice under Gregory IV (827–844) with Louis the Pious and
   marks the initiative uncertain. The traditional date of the Pantheon
   dedication is 13 May; Durandus's *quarto Idus* (12 May) is kept as his.
7. **The Preface (rubrical, not textual):** the registered rules read both
   ways (RGMR, printed p. XXXIV = facsimile PDF p. 32, read on the page
   image in iteration 2). RGMR 482 gives the Mass's proper Preface, failing
   that the Preface *de Tempore*, otherwise the common; RGMR 483 forbids a
   commemoration to induce a proper Preface; RGMR 494 b gives the Trinity
   Preface *tamquam de Tempore in dominicis Adventus, et in omnibus
   dominicis II classis, extra tempus natalicium et paschale*; RGMR 498
   gives the common Preface *in Missis quae praefatione propria carent, nec
   sumere debent praefationem de Tempore*. The question is whether 494 b
   attaches the Trinity Preface to the Sunday (so that a feast without a
   proper Preface said on it takes the Trinity Preface) or only to the
   Sunday's own Mass (so that the feast takes the common Preface). The
   wording of the other seasonal rules does not decide it: most name the
   Masses of a period (484 b, 486 b, 487 b, 489 b, 490 b, 493 b), while 485 b names days (*diebus a 7 ad 13
   ianuarii*) and 494 b names Sundays. The Missal's Vigil of the Nativity
   rubric (printed p. 16 = PDF p. 97: *Praefatio communis; sed, si venerit
   in dominica, dicitur de Ss.ma Trinitate*) gives the Trinity Preface to a
   Mass that is not the Sunday's when it falls on an Advent Sunday; it can
   be read as an instance of the general rule or as an exception the
   general rule needed. The repository test asserts the common Preface
   without citing an authority. Open; owners notified (§10). The medieval
   sacramentaries' proper Preface quoted by Schuster is history, not
   appointment.
8. **The last Gospel:** RGMR 509 (printed p. XXXV = PDF p. 33, read on the
   page image in iteration 2) appoints *initium Evangelii secundum Ioannem*
   regularly *in quavis Missa*; its one exception is Palm Sunday Masses not
   preceded by the blessing and procession of palms, and none of the RGMR
   510 omission cases (a-f) applies. The last Gospel is Jn 1:1–14. This is
   settled from the registered RGMR loci alone. A contrary line in a dated
   web Ordo (research/context.md, *Dated witnesses*; registered as context
   only, binding 35) was withdrawn as evidence in iteration 2, and the
   studies neither cite nor present it.
9. **Numbering hazards (recorded so citations stay honest):** the NPNF
   titles Augustine's exposition of Vulgate Ps 32 "Psalm XXXIII" and of
   Vulgate Ps 33 "Psalm XXXIV"; Bellarmine numbers Vulgate 32 as XXXII and
   33 as XXXIII. The Clementine, the Douay and the Hebrew all count Ps 33's
   inscription as v. 1, so the Missal's `Ps. 33, 10 et 11` = Douay 33:10–11
   = Hebrew 34:10–11; English Bibles that follow the Hebrew but leave the
   inscription unnumbered call them 34:9–10. The NPNF English of Augustine
   uses that English verse count, so its "(ver. 9)–(ver. 11)" are Vulgate
   33:10–12; Bellarmine's English counts Ps 33:2 as v. 1, so his vv. 9–10
   are Vulgate 33:10–11. In Ps 32 (no separately numbered inscription) both
   agree with the Vulgate verse numbers. The Missal's
   `Ps. 32, 1` excludes the inscription the Clementine prints inside the
   verse. Every citation in the studies must carry its numbering's basis.
10. **Rabanus derivative:** his Mt 5 matter quotes Augustine (printed
    "(Aug.)"); he witnesses the Augustinian reading's transmission, not an
    independent exegesis.

## 7. Negative searches, unopened leads and bounds

- `commentary-work-index formulary` for `omnium-sanctorum`: 40 loci
  compared, no liturgical commentator listed, although Schuster vol. 5 and
  the Guéranger-Fromage vol. 15 chapters are registered artifacts — the
  index is incomplete (§10).
- `discover` for Wisdom 3:1–3: no mapped commentary at all. Reception was
  reconstructed from phrase reception (§3.7).
- `discover` for Apoc 7:2–12 (iteration 0): Bede is the only mapped
  commentary it reports. It places Victorinus (ANF VII) outside his held
  extent because the containment inventory maps his constituent only to Rev
  1, 5 and 19; the artifact itself comments on 7:2 and 7:9, and the
  negative iteration 0 recorded was false (corrected in iteration 3: §3.3,
  §10.12). Andrew of Caesarea cataloged-only; Cornelius a Lapide and Hugh
  of St Cher held in non-covering works; Ambrose Autpert, Beatus, Denis,
  Rupert, Bruno of Segni, Haimo, Primasius, Richard of St Victor: no
  holdings.
- **Second search for an eligible witness on Apoc 7 who agrees with Bede
  (iteration 3).** Result: Augustine (father) agrees on the number and the
  crowd in three brief loci, and Bellarmine (doctor) agrees with Bede's
  alternative reading of v. 9 on Ps 86:2 (§3.3). No further eligible
  commentary on the chapter is held. The review's lead, Caesarius of Arles'
  Apocalypse homilies printed among Augustine's spuria in PL 35, was
  followed to the registered PL 35 scan: the work printed there is the
  anonymous *Expositio in Apocalypsim* (col. 2417 in the volume's Elenchus),
  and the print's own *Admonitio* names Victorinus, Primasius, Bede and
  Tyconius but no Caesarius. No registered source states an attribution to
  Caesarius, and the library holds no work of Caesarius of Arles and no
  standing row for him (§10.5). The *Expositio* was read on page images and
  agrees with Bede (§3.3), but as an anonymous compilation that draws on
  Bede it can neither carry nor count as independent. Tyconius and
  Primasius have no holdings; Tyconius's number rule reaches the library
  only in Augustine's account of it (*De doctrina christiana* III.35). The
  same search found Cyprian's martyrs reading of the crowd, preserved as a
  rival (§6 item 1). Literal searches of the text layers for the Lesson's
  wording are finding aids only; a commentary on Apoc 7 held only as an
  image scan without a text layer, or in a constituent no inventory maps,
  would not have been reached.
- Cassiodorus, *Expositio Psalmorum*: held for Ps 39, 70, 85, 97, 101 only
  (Monumenta artifacts); Ps 32 and 33 not held.
- Jerome, *In Matthaeum* cap. 5 (PL 26, cols. ~32–38): no tracked text; the
  held column facsimiles cover later chapters; a remote whole-volume PDF is
  registered. Not fetched: the Gospel already carries four fathers/doctors
  read at the verse plus a saintly compiler; fetching a remote scan for a
  fifth carrying-eligible reading was not proportionate this iteration. If
  review requires Jerome, the artifact record's `source_url` is the lead.
- Theodoret, *In Psalmos* (PG 80): remote-only; not fetched, same
  proportionality (Ps 33 already carries Basil, Augustine, Bellarmine,
  Aquinas). An ecclesiastical-writer; he could not carry.
- Athanasius, *Expositiones in Psalmos* (PG 27): tracked, not opened;
  unopened lead for Ps 32:1.
- Gregory of Nyssa, *De beatitudinibus*: no holdings (discover negative);
  no standing row either (§10).
- Bernard of Clairvaux's All Saints sermons (Sermones de omnibus sanctis):
  a known lead, not held. Iteration 3 checked the library's Bernard
  holdings: the registered works are his letters, *De consideratione*, *De
  diligendo Deo*, the *Homiliae super Missus est*, the *Sermones in festo
  sancti Michaelis*, the *Sermones in psalmum XC Qui habitat* and the
  *Sermones super Cantica canticorum*; none is an All Saints sermon, and no
  Patrologia Latina volume of his works (PL 182–185) is registered. No
  passage or artifact is registered for the All Saints sermons, and there
  is no standing row (§10). Not used.
- Gregory the Great, *Homiliae in Evangelia*: the homily collection is held
  (wikisource whole text, PL 76 facsimiles, checked snippets); no homily
  covers Mt 5:1–12 or Mt 11:28 (his Mt homilies treat other pericopes); his
  *Moralia* occurrences of Mt 11:28 are indexed phrase reception, not an
  exposition of the verse. His Christmas homily (Hom. viii) is cited by the
  continuation for the "first census" — indexed, not read at the verse.
- Peter Chrysologus (PL 52, line 24879 "in manu Dei sunt"): context not
  checked; indexed lead only.
- The 1570 Missal: the feast's own Offertory (lines 71705–71709) was read
  in the iteration-1 repair and reads *tormentum mortis* without alleluia
  (§3.7); lines 62448 and 68676–68680, which the index reported, are the
  Communion of Ss Marcellinus, Peter and Erasmus and the Gradual of Ss Felix
  and Adauctus, not this feast's text. The 1604, 1862 and 1889 printings were
  read on text layers only, not on page images. The date at which the
  *alleluia* entered (after 1909, by the Mame 1922) is unresolved: no 1920
  typical edition is held in readable form. The 1962–Mame collation controls
  the text.
- Honorius, Sicard, Rupert, Amalarius, Berno, Bernold: standing rows exist;
  no registered All Saints chapter located in held texts; unopened leads.
- The Lasance scriptural-English artifact (`ff92e98e`) is registered but has
  no translations-inventory row; it is a lead for English display, disclosed
  as such in `propers/verified.md`.
- Not searched this stage: post-1962 literature, modern commentaries, and
  any source outside the registered library, except two groups read by the
  resolve-context stage, which carry nothing. Research iteration 2 withdrew
  every reliance on them; the source-registration stage (iteration 2)
  registered both as restricted records with no bytes retained and bound
  them as context only (bindings 35-41), and the studies may not cite them.
  (a) The dated web witnesses (research/context.md, *Dated witnesses*): the
  ICRSP Ordo and Mass-text page, the FSSP France Ordo du mois, the FSSPX
  Ordo day page and texts endpoint, and Missale Meum, each a dated edition
  of 2026-10-26 with its artifact and 1 November passage (bindings 35-40).
  The Divinum Officium request returned an access-block page with no
  content; nothing from it was read and it is not registered. (b) Patrick L.
  Murphy, *The New Rubrics of the Roman Breviary and Missal: Translation and
  Commentary* (Sydney, Catholic Press Newspaper Co., 1960), registered as
  `work.patrick-l-murphy.new-rubrics-of-the-roman-breviary-and-missal` with
  the scan PDF of its posthumous re-publication (111 pages, 9,458,756 bytes,
  SHA-256 `a519a5cf0204bf6a9ebbeb41e743ade3bcc89c7b93462855bb10794d1df69a7d`,
  served at two public URLs recorded on the artifact) and passages at printed
  p. 93 and pp. 192-193 (binding 41). The commentary on the Preface restates
  RGMR 482-483 and adds only "In practice the Ordo will indicate the preface
  for each day"; the commentary on the last Gospel restates RGMR 509. It
  does not treat a feast said on a Sunday, so it does not settle the
  Preface. It is in copyright (Australian, 1960; editor d. 2007) and is
  context, not evidence.
- **Registered rubrical sources searched for the Preface (iteration 2).**
  None settles the case of a first-class feast without a proper Preface
  said on a II-class Sunday:
  - the RGMR of the 1962 typical edition,
    `passage.catholic-church.missale-romanum.vatican-typica-1962.rubricae-generales-missalis`
    (nn. 424-432 and 466-510, verified) and the bound facsimile at PDF pp.
    32-33, read in iteration 2: the rule itself, which reads both ways
    (§6 item 7);
  - the same code as promulgated in AAS 52 (1960),
    `segment.catholic-church.rubricae-breviarii-et-missalis-romani.latin-aas-52-1960.aas-52-1960-pages-597-740`:
    the same text as the Missal's RGMR, so it adds no rule; not re-read;
  - Fortescue, *Ceremonies of the Roman Rite Described*: the twelfth
    revised edition of 1962 is a catalog-only remote record (no text held);
    the seventh revised edition of 1943 is held with passages but is before
    the 1960 code and cannot speak to RGMR 494 b;
  - the registered dated Ordo editions: ICRSP France (web states of 17 and
    22 September 2026) and FSSP France (web states of 17 September to 19
    October 2026) carry no passage for 1 November. The FSSPX Ordo edition
    "web 2026-10-25" for 1 November 2026, added by another lane's commit
    `9ff79af29`, was not opened by this research under the independence
    boundary (§11); a dated usage witness would be evidence of practice, not
    a rubrical authority, in any case;
  - `src/sources/commentary/formulary-loci.yaml`: no liturgical commentator
    locus for this formulary (above).

## 8. Chronology

### 8.1 What the gate requires

The stage generated `research/chronology.toml` and
`research/chronology-annotations.tex` (both rewritten by `tools/tpt
proper-chronology` on 2026-10-26) from `src/sources/chronology/`
and the locus resolution. The gate's needs: every directly appointed
passage carries a chronology orientation; disputed dates keep their ranges;
no date is asserted beyond the sources.

### 8.2 Each generated row: passage scope, subject, and a sourced phrase

The distinct said passages (canonical then verse order): Ps 32:1 (verse,
without inscription); Ps 33:10 + 11b; Wis 3:1–3 (selected and adapted); Mt
5:1–12a; Mt 5:8–10 (re-read as the Communion); Mt 11:28; Apoc 7:2–12. The
generated rows, inspected one by one:

- **Ps 32 — attribution** (row groups `introit` + `gradual`'s psalm family
  is 33; this row is the Introit's): traditional attribution to David
  (1055–1015 BC) disputed — the Hebrew has no superscription; the
  Clementine's *Psalmus David* is the LXX tradition. Sourced phrase: the
  chronology sources' own label for the Davidic attribution claim.
- **Ps 32 — historical setting**: research-pending; occasion unresolved.
  The annotation carries the "Date unresolved" orientation rather than an
  invented one.
- **Ps 32/33 — composition**: preferred before c. 165 BC (the Psalter's
  collection bound); no precision asserted.
- **Ps 33 — superscription setting**: preferred — David's flight to Achis of
  Geth (1 Kings 21), A.M. 2944 in the Ussher-style reckoning the sources
  carry; the Missal reads vv. 10–11, far from the inscription, and the
  setting is the psalm's own tradition.
- **Ps 33 — composition**: before 165 BC, as Ps 32.
- **Wis 3 — composition**: disputed between Ptolemy IV (221–204 BC) and
  Ptolemy VII (145–117 BC); the range is kept, no point estimate.
- **Mt 5:1–12 — narrated event**: research-pending, "Date unresolved"; the
  place is "a mountain" per 5:1 (the traditional identification near
  Capernaum is later devotion, not asserted).
- **Mt 11:28, Mt 5:1–12, Mt 5:8–10 — Matthew's composition**: six disputed
  dates carried (38–45 … 50 and onward ranges), grouped as one orientation
  row across `alleluia`, `gospel`, `communion`.
- **Apoc 7 — composition**: disputed 81–96 against c. 90–100; kept open.

### 8.3 Over-wide ranges, expected and flagged

The locus resolution (`tools/tpt proper-chronology loci`) inherits the
calendar record's ranges: Gradual `Ps 33:10–11` where the said text is
10 + 11b; Gospel `Mt 5:1–12` where the said text ends at 12a; Offertory
`Wis 3:1–3` where the antiphon selects and adapts. The generated
annotations therefore orient whole ranges, which is safe for chronology
(no range adds a date claim the said text lacks) but is reported for the
owners of `propers.yaml` and the locus tool (§10). Two orientation rows
group several elements behind one passage family (the Introit/Gradual
psalm-attribution family and the Matthew composition row across
alleluia/gospel/communion): allowed by the orientation grammar, and the
concise-study printer must not render them as if each element had an
independent date claim.

### 8.4 Composite-element check

No composite-element row was found carrying a date beside a constituent
passage row in violation of the gate's rule; the shared rows above are
composition families, which the orientation grammar permits.

### 8.5 Controlling sources inspected

`research/chronology.toml` was generated from the chronology corpus under
`src/sources/chronology/`, whose claim records cite the following library
sources; the controlling claims of this leaf rest on them, and each was
inspected at its passage in the iteration-1 repair (2026-10-26). The
generated file carries the exact labels.

- **Catholic Encyclopedia, Jacquier, "Gospel of St. Matthew"** (artifact
  `…volume-10.new-york-1911.newadvent-10057a-e7b6ccef`) and **Durand, "The
  New Testament"** (`…volume-14.new-york-1912.newadvent-14530a-0a19aa2c`):
  the disputed composition ranges of Matthew carried for the Alleluia,
  Gospel and Communion; traditional and critical ranges are kept distinct.
- **Gigot, "Book of Wisdom"** (`…volume-15.new-york-1912.newadvent-15666a-
  999fbc07`): the composition dispute between the reigns of Ptolemy IV and
  Ptolemy VII, for the Offertory.
- **Van den Biesen, "Apocalypse"** (`…volume-1.new-york-1907.newadvent-
  01594b-7f47696f`): "the reign of Domitian … A.D. 81-96" against "from the
  year 90 to 100", for the Lesson.
- **Corbett, "David"** (article text `…volume-4.new-york-1908.newadvent-
  04642b-f1c0bed3`; passage `corbett-david-usual-chronology`): David's
  reign in the usual chronology, 1055–1015 B.C., for the traditional
  attribution of Ps 32 and Ps 33.
- **Haydock, 1 Kings 21 (Achis of Geth)** (passage
  `…2014-loreto-feeney-memorial.first-kings-21-achis-geth-chronology`):
  Haydock's margin reports the Ussher reckoning, A.M. 2944 (A.C. 1060, as
  marked at 1 Kings 20), for David's flight to Achis — the setting the Ps 33
  superscription names. Haydock reports Ussher's chronology; the date is
  Ussher's reckoning, not an independent dating.
- **Haydock, Psalm 70** (passage `…psalm-70-captivities-usher-chronology`):
  Haydock's report of Ussher's dates for the captivities, cited beside the
  1 Kings 21 passage as the Ussher reckoning's attribution; it does not
  itself date the Achis episode.
- **NABRE, Introduction to the Psalms** (passage
  `…new-american-bible-revised-edition.english-usccb-web-2026-07-28.psalms-
  introduction`): the composition boundary of the Psalter, which reaches
  the Introit verse and the Gradual as the generated label "before the
  Maccabean period, around 165 B.C.; no individual psalm can be dated
  securely". The NABRE introduction's prose is summarized in that label,
  not reproduced (§9).

## 9. Rights

- **1962 facsimile (CMAA scan):** read on page images for control only; no
  page image, layout, accent scheme, rubric or marginal number is
  reproduced in any publication. The Latin travels on 17 U.S.C. 103(b) plus
  the public-domain witnesses, per
  `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`.
- **Mame 1922** (Tours): public domain in the United States (pre-1931
  foreign publication, the `guidance/missals.md` §5 line applied as of
  2026-10-26); the four own bodies and six scriptural bodies stand in its
  checked artifacts, collated word-for-word with the 1962 page.
- **Pustet 1862** (Ratisbon): public domain. The tracked page extract
  `…pustet-ratisbon-1862.pentecost-23-prayer-pages-7e6ef53b` (parent PDF
  pp. 443–444 = printed pp. 357–358) was read on its page images in the
  iteration-1 repair: it prints the commemoration's three orations — the
  Collect *Absolve, quaesumus* on printed p. 357, the Secret *Pro nostrae
  servitutis augmento* and the Postcommunion *Quaesumus, omnipotens Deus*
  on printed p. 358 — in the words of the 1962 page, with shorter
  conclusion cues (`propers/verified.md`).
- **Lasance 1945** (Benziger revised): English public domain by nonrenewal
  (`lasance-new-roman-missal-rights-v1.toml`); orations confirmed in
  `roman-1962-proper-translations-v1.toml`; scriptural English a registered
  lead without an inventory row (disclosed).
- **Douay-Rheims (Challoner):** public domain; registered edition and verse
  artifacts; carries English only where it carries the Missal's form.
- **Reception witnesses:** NPNF volumes (1886–1890, public domain); CCEL
  text derivatives; PG 29 (1860), PL 9 (1844), PL 107 (1864), PL 202 —
  public-domain scans; Bede, Marshall 1878 (public domain); Bellarmine in
  O'Sullivan's nineteenth-century English (public domain); Aquinas Venice
  1745 and Parma 1863 scans (public domain); Durandus 1568 composite scan
  (public domain); Schuster vol. 5, London 1930 (public domain on the same
  pre-1931 line); Guéranger-Fromage French vol. 15, Paris 1909 (public
  domain). Quotation from every witness is limited, attributed, and made
  for study; the studies quote rather than reproduce.
- **Registered context, no bytes retained:** the dated web witnesses
  (ICRSP, FSSP France, FSSPX, Missale Meum; rights unresolved, modern
  institutional or private pages without a redistribution grant) and
  Murphy's 1960 commentary (restricted: in copyright in Australia and,
  under 17 U.S.C. 104A, in the United States). Identity and factual-locus
  records only; nothing from them is quoted or used as a reading.
- **Project artifacts** (editorial projections): CC BY 4.0 project records,
  internal conveniences, never a publication source.
- **Restricted, never reproduced:** ICEL, Knox, Jerusalem, RSV, NRSV,
  NABRE, Grail. No restricted text is quoted or used as a reading. The one
  exception to "never used" is the NABRE Psalms introduction, which the
  chronology corpus cites for the Psalter's composition boundary; its prose
  reaches the Introit and Gradual chronology claims only as a summarizing
  label (§8.5), not as quotation; the vatican.va OCR reconstruction habits noted in F01 are not in
  play here.

## 10. Shared records: reports for their owners

This stage owns no shared record. The following are reported, not repaired.

1. **`tools/tests/test_ordinary_appointments.py`** (fixture
   `allSaintsSunday1962`, date 2026-11-01) asserts `praefatio-communis` with
   the comment "494 b) reaches the Mass of the Sunday, not a feast said on
   one." It cites no authority. The registered rules read both ways, and
   the Missal's own Vigil of the Nativity direction (*si venerit in
   dominica, dicitur de Ss.ma Trinitate*) supports the Trinity reading by
   analogy (§6 item 7). The rule is unsettled in the registered sources
   (§7, *Registered rubrical sources searched*). The test's owner should
   either cite an authority for its reading or mark the assertion disputed.
2. **`src/sources/calendars/roman-1962/propers.yaml`, mass
   `omnium-sanctorum`:** (a) no Preface case for the Sunday occurrence,
   while `pentecost-23` carries `ordinary_appointments.preface: trinitate`;
   (b) the six scriptural elements carry ranges only, so `mass-propers
   show` labels them "Missal wording not established" although the Mame
   received-form passages were registered on 2026-10-25; (c) the Gradual
   (`Ps 33:10-11`), Gospel (`Mt 5:1-12`) and Offertory (`Wis 3:1-3`) ranges
   are wider than the said text, so Douay reconstructions include words the
   Mass does not read (the Gradual's *The rich have wanted…*, the Gospel's
   *So persecuted they the prophets…*, the Offertory's omitted clauses).
3. **`tools/tpt proper-chronology loci`:** inherits the same over-wide
   ranges (§8.3).
4. **`src/sources/commentary/formulary-loci.yaml`:** no commentator locus
   for this formulary, although registered All Saints chapters exist
   (Schuster vol. 5, read on its bound OCR artifact `65192aa1`, with the
   registered chapter page-image artifact `d55b5905` not inspected by this
   research; Guéranger-Fromage vol. 15 artifact
   `6301674b`; Durandus VII.34 in artifact `2bd5ccb5`; Beleth cap. CLVIII in
   artifact `22b781bf`). The index's owner may want rows.
5. **`src/sources/inventories/author-standing-v1.toml`:** no rows for
   Bernard of Clairvaux (whose All Saints sermons are a standing lead),
   Victorinus of Pettau, Cyprian, or Gregory of Nyssa (whose *De
   beatitudinibus* is a natural Gospel witness with no holdings). None was
   needed as a carrier this stage; if review or authoring wants them, the
   rows must exist first. The source-registration stage (iteration 1) also
   found no rows for Alphonsus Liguori (`make check-sources` lists him among
   lane authors with no row), Athanasius, or Peter of Celle; §4 had given the
   first two standings the registry does not hold. Iteration 3 read
   Victorinus of Pettau and Cyprian as witnesses on the Lesson (§3.3); both
   remain without rows and cannot carry, and rows would let review weigh
   them. There is also no row for Caesarius of Arles, whose name the review
   attached to the PL 35 *Expositio in Apocalypsim* (§7).
6. **Bede, *Explanatio Apocalypsis* passage records:** vv. 4, 9, 10, 11, 12
   and 14 are registered, but vv. 2–3 (the angel from the east; the
   sealing) — which the Lesson reads — have no passage records. The whole
   text layer carries them (this stage read them there); a registration
   handoff candidate.
7. **`src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml`:**
   no `omnium-sanctorum` rows for the six scriptural bodies;
   `propers/verified.md` carries the collation and basis (103(b) + Mame
   1922) until the ledger's owner adds rows.
8. **Lasance scriptural English:** artifact `ff92e98e` exists and is
   checked, but `roman-1962-proper-translations-v1.toml` has no row for it;
   English display treats it as a lead until the inventory's owner rules.
9. **`src/sources/inventories/source-containment-v1.toml`, container
   `…latin-migne-pl-202.ia-djvu-ocr-22b781bf`:** it lists only Beleth's
   *Summa* and records as unresolved whether the volume prints other works.
   The volume prints Peter of Celle's *Tractatus de disciplina claustrali*
   (title at physical lines 79890–79912, col. 1097; §3.1, §3.7), so a
   holdings sweep through the container cannot reach his work.
   `author-standing-v1.toml` has no row for Peter of Celle either. Reported
   by the source-registration stage (iteration 1); the inventory's owner may
   want a constituent row, entered from the volume's own contents.
10. **`src/sources/inventories/author-standing-v1.toml`:** after the
    source-registration stage (iteration 2) registered
    `work.patrick-l-murphy.new-rubrics-of-the-roman-breviary-and-missal`
    as a `liturgical-commentary`, `make check-sources` lists it among
    liturgical commentaries with no standing row. It carries nothing here
    (context only, binding 41); the inventory's owner may want a row before
    any study relies on it.
11. **`work.fsspx.ordo`:** the shared work record lists `languages =
    ["en"]`, but the day page and texts endpoint registered on 2026-10-26
    (`edition.fsspx.ordo.web-2026-10-26`) are in French. Not changed here
    because another lane created the record; its owner may want to add
    `fr`.
12. **`src/sources/inventories/source-containment-v1.toml`, container
    `work.ante-nicene-fathers.volume-7`:** the Victorinus constituent's
    `scripture` list is Rev 1:1, 1:4–7, 5:1–9 and 19:11, the portions the
    2026-10-20 audit inspected, and its `unresolved` note leaves the rest
    unassigned. `discover` therefore reports Apoc 7 outside his extent,
    although the same artifact (`ccel-text-b69327af`) prints comments
    headed "from the seventh chapter" on 7:2 and 7:9 (lines 33565–33625)
    and comments on most other chapters (chapter headings at lines 33024
    to 34337, including 12:6 on the 144,000 at lines 33964–33974). This
    false negative led iteration 0 to record Victorinus as unusable for
    the Lesson. The inventory's owner may want to extend the constituent's
    extent from the commentary's own chapter headings. The anonymous
    *Expositio in Apocalypsim* in PL 35 (col. 2417 in the volume's
    Elenchus) also has no work or constituent record, so no holdings sweep
    can reach it either.
13. **Bede, chapter VII, and the PL 35 *Expositio*:** the Lesson's
    registered commentary passages are Bede's six alone. Victorinus's
    comments on 7:2 and 7:9 and the *Expositio*'s Homily VI on Apoc 7 are
    deferred candidates with their missing criteria in
    `research/source-dispositions.toml` (bindings 42 and 46): a registration
    handoff, not a repair this stage makes.

## 11. Evidence bounds

- **Settled:** the appointed text (all fourteen elements) word-for-word
  against the 1962 page; the publication basis of every Latin body; the
  commemoration's composition and order; the colour, Gloria, Credo; the
  last Gospel (Jn 1:1–14, RGMR 509–510, from the registered loci alone); the
  reception of every appointed passage in at least one father or doctor
  read at the verse (Wisdom 3 via patristic phrase reception, no mapped
  commentary existing); for the Lesson, two fathers who read the number and
  the crowd as the whole Church (Bede on the chapter; Augustine in three
  brief loci), a doctor's analogue (Bellarmine), and the dissent of
  Victorinus and Cyprian (§3.3, §5.1); the chronology orientation of every
  said passage.
- **Open:** the Preface (Trinity n. 1082 against common n. 1086). The
  research searched the registered rubrical sources named in §7 and found
  no settling authority. **Fixed rule for authoring (element 11):** name
  the slot as unsettled; name both candidates, the Trinity Preface (n. 1082)
  and the common Preface (n. 1086), each with its RGMR basis (482 and
  494 b for the Trinity reading, with the Vigil of the Nativity rubric as an
  analogy only; 482, 483 and 498 for the common reading); assert neither as
  this Mass's appointment; reproduce neither text; build no interpretation
  on either Preface's wording; and cite no Ordo, web calendar or
  repository test as evidence for either.
- **What the studies may cite for the occurrence, the Preface and the last
  Gospel:** only the registered records of the 1962 typical edition — the
  bound facsimile (binding 1: the formulary, the commemorated Sunday's
  orations, RGMR nn. 482–499 and 507–510, and the Vigil of the Nativity
  rubric) and the registered passages `…rubricae-generales-missalis`,
  `…praefationes` and `…praefationes-sine-cantu`. The dated web witnesses
  and Murphy's commentary (§7) are registered and bound as context only
  (bindings 35-41) and may not be cited, quoted or described as evidence.
- **Not attempted:** Jerome's Mt 5 (remote lead), Theodoret and Athanasius
  on the psalms, Gregory of Nyssa, Bernard's All Saints sermons (not held;
  §7), any natural-excerpt transcription of Victorinus or of the PL 35
  *Expositio* (deferred, §10.13), the
  medieval liturgical commentators beyond Durandus and Beleth, any
  post-1962 literature, and the commemorated Sunday's own reception (out of
  scope per the production plan). Each is a named lead with its artifact
  or index locus above.
- **Independence:** the GPT leaf for this identity, its review records and
  its PDF/web editions were not opened; the Claude F01 records were used as
  shape models only. Shared library records (including those added by
  another lane's commit `9ff79af29`) were used only after independent
  verification of identity and content at the loci cited.
