# Research scope: First Sunday of Advent (1962)

Research record for `liturgy/roman-rite/1962/propers/temporal/01-first-sunday-of-advent`,
written on 25 November 2026 in the research stage (iteration 0) of
proper-study run `77c1ca91ef2d5e93`. It holds the findings; the readings are
in research/interpretations.md, the verified text in propers/verified.md, the
machine pulls in propers/retrieved.txt, the library bindings in
research/source-bindings.toml and the chronology in research/chronology.toml.

Revised on 25 November 2026 in the research stage (iteration 1) of the same
run, after the research review. Gregory's first homily is read and cited as
its six sections (sections 4, 5, 7.1, 8.1, 8.4, 11-13); Augustine's and
Ambrose's identifications of sun, moon and stars are each recorded at their
own loci, and the difference between them is stated (sections 4, 7.1, 8.2);
Chrysostom on Rom 13:12 is restated (section 4). Source registration
(iteration 1) then corrected the shared Gregory passage record and recorded
the outcome (sections 11, 13.2).

## 1. Publication mode and identity

Ordinary schema-2 appointed-text mode, not reference-only: no reference-only
authorization names this provider and identity (research/context.md,
*Publication mode*). The appointed text is complete for all ten elements
(propers/verified.md). The formulary is *Dominica prima Adventus*, I classis,
Missale Romanum 1962, printed pp. 1-2, marginal nos. 1-10, on Sunday
29 November 2026; nothing is commemorated. research/context.md was read whole
and its identity, occurrence, rubrics and inventory were checked against the
page images (section 2.1); one point is corrected and one sharpened below.

**Corrections to research/context.md**, made in that record in this stage
for (a) and (c) and recorded here. (a) It recorded that the 1862 text
layer's Communion citation reads *Ps. 81* and leaves the image to research:
the 1862 page image (PDF p. 89, printed p. 3) reads *Ps. 84*; the layer
misreads. (b) Its *Lawful study-text routes* leave open whether the five chants
and the Gospel have a public-domain antecedent with the same words: the 1862
page images were read and they do, word for word (propers/verified.md, *The
publication basis of the Latin*). (c) It left open whether Lasance prints
English for the chants and lessons: it does, for all ten elements, Douay-based
(section 2.4). Everything else in it stands as written; its station
(*Statio ad S. Mariam maiorem*) is the 1962 heading, and the older station
tradition is a separate fact (section 8.4).

## 2. Text control, rights and English

### 2.1 The 1962 page images

PDF pp. 82-84 read whole at 200 dpi; PDF pp. 82-83 in 400-dpi crops of all six
column sections; the head of PDF p. 84 in a 200-dpi crop. Every element's
words, accents, citations, conclusions and rubrics are in propers/verified.md.
Points of form the study must keep: the Gospel's *veniéntem in nube*
(singular; Gregory's text reads *in nubibus*, section 8.3); the Epistle's
*Abiciámus* and its end at v. 14a; the Gradual's *notas fac mihi* beside the
Introit verse's *demónstra mihi*; the Communion without *Etenim*; the Collect
addressed to the Son (*Qui vivis et regnas cum Deo Patre*).

### 2.2 Publication basis

Pustet 1862, printed pp. 1-3 (PDF pp. 87-89 of the registered scan, fetched
whole on 2026-11-25 and hash-matched), read on page images: every element in
the same words as the 1962, with orthographic, pointing and cue differences
only. The repository's 17 U.S.C. 103(b) holding
(`src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`)
therefore admits the Latin of all ten elements. The Latin ledger has rows only
for the three orations and the Epistle (section 11).

### 2.3 What the chant forms are, and what is not established

The Missal's chant wording differs from the Clementine at five places
(propers/verified.md, table). Two have a checked parallel in a Father's
psalter:

- Augustine's Latin of Ps 24 in his *Enarratio* (augustinus.it
  `esposizione_salmo_026_testo.htm`, read whole) has *Etenim universi qui te
  exspectant non confundentur* and *Vias tuas, Domine, notas fac mihi*: the
  Introit's and Gradual's *qui te exspectant* and the Gradual's *notas fac*.
  It also has *Ad te, Domine, levavi*, with the vocative the chant lacks.
- Augustine's Latin of Ps 84:13 (*Enarratio* 84.15, tracked Wikisource part 9,
  line 89) reads *Etenim Dominus dabit suavitatem*, not *benignitatem*.

Aquinas's psalter in *Super Psalmos* 24 reads the Clementine's *qui sustinent
te* and *demonstra*. These are textual observations about which Latin psalters
share the chant's words. No Roman Psalter witness was read, and no claim is
made that the chants were taken from any of these psalters (section 10).

### 2.4 English: what exists, and the recommended display

- **Lasance 1945**, printed pp. 103-106, prints English for every element,
  read on page images (propers/verified.md, *English*). Its chant and lesson
  English follows the Douay, with the liturgical openings and with "For"
  dropped from the Communion; it renders neither the Gradual's *notas fac* nor
  its added *Dómine*. Public domain in the United States by non-renewal on the
  repository's record
  (`src/sources/inventories/lasance-new-roman-missal-rights-v1.toml`).
- **Douay-Rheims (Challoner)** carries the bodies of the Epistle and Gospel,
  the Alleluia and the Introit verse exactly; the Introit and Offertory
  antiphon with an "O Lord" the Missal lacks and "wait on" for *sustinent*;
  not the Gradual's verse; the Communion with a "For" the Missal lacks.
- **Cummiskey 1861** (named in research/context.md) was not opened: Lasance
  carries every element.
- The English overlay's `project-created` Epistle row is excluded (research/
  context.md); nothing here uses it.

Recommended display (propers/verified.md, *Recommended display*): the Douay
for every scriptural element, its differences from the Missal's form stated
where they occur; for the Communion, Lasance's line, which is the Douay
without "For", attributed, with the Douay verse beside it; for the Gradual's
verse, the Latin with the statement that it reads *notas fac* ("make known")
where the Douay renders *demonstra*; Lasance for the three orations, cited by
formulary. Nothing is composed.

## 3. Search method

- `tools/commentary-work-index discover`, uncapped, for Ps 24:1-4, Ps 84:8,
  Ps 84:13, Rom 13:11-14 and Lk 21:25-33, and `formulary --calendar roman-1962
  --mass advent-1`, run on 2026-11-25. The formulary query compared 40 loci and
  listed none: the commentator index has no entry for this Mass, so the
  liturgical commentators were found by direct search of the held Latin
  texts (section 6).
- Every source read is a library artifact or passage, re-hashed and matched
  before its locus was read, or a fetch of a registered remote or restricted
  artifact matched to its registered SHA-256, or (two files) a new fetch
  handed to source registration (section 13).
- Biblical contexts read whole in the Douay and Clementine: Ps 24; Ps 84;
  Rom 12:1-13:14; Lk 21:5-38, with Mt 24:3-35 and Mk 13:3-37 for the
  synoptic place of the discourse.

### 3.1 Holdings the discover runs reported, and what was done with them

| Passage | Held and read | Held and not read (lead) | Reported as not registered |
| --- | --- | --- | --- |
| Lk 21:25-33 | Gregory, *Hom. in Ev.* 1; Ambrose, *Expos. in Luc.* X.36-45; Bede, *In Luc.* VI; Cyril of Alexandria, *Comm. in Luc.* sermon 139; Augustine, Ep. 199; Chrysostom, *Hom. in Mt.* 77 (parallel) | Catena aurea in Lucam on 21:28; Jerome, *In Mt.* IV on 24:34-35 (PL 26 facsimile only); Augustine, *De civ.* XX; Leo (only the Breviary lesson read); Hugh of St Cher (restricted); Cornelius a Lapide | Bonaventure, Theophylact, Albert, Lyra, Denis, Ephrem, Origen |
| Ps 24:1-4 | Augustine, *En. in Ps.* 24 (Latin, English NPNF); Aquinas, *Super Ps.* 24 nn. 1-4; Bellarmine, *Explanatio* 24 vv. 1-5 | Cassiodorus; Theodoret (remote); Athanasius; Basil; Hilary; Ambrose | Lombard, Denis, Lyra, Jerome, Albert, Bede, Walafrid |
| Ps 84:8, 13 | Augustine, *En. in Ps.* 84.1, 9, 15; Bellarmine 84 vv. 8, 13 and the psalm's title | Cassiodorus; Theodoret | as for Ps 24; Aquinas's *Super Psalmos* does not reach Ps 84 |
| Rom 13:11-14 | Chrysostom, *Hom. in Rom.* 24; Aquinas, *Super Rom.* 13 l. 3; Augustine, *Conf.* VIII.5.12 and VIII.12.28-29 | Cornelius a Lapide | Origen, Lombard, Lyra, Cyril, Denis, Rabanus, Theodoret |

## 4. Passage-by-passage reception matrix

Roles: **D** direct exegesis of the appointed words; **L** liturgical
commentator on this Mass's element; **C** context or doctrinal illumination.
"Read" means this stage read the locus in the bytes bound.

| Element and passage | Witness, locus | Role | What the witness actually says (checked) |
| --- | --- | --- | --- |
| Introit, Offertory: Ps 24:1-3 | Augustine, *En. in Ps.* 24.1-3 | D | Christ speaks in the person of the Church; the soul lifted *desiderio spiritali, quae carnalibus desideriis conculcabatur in terra*; the enemies are hidden suggestions. |
| | Aquinas, *Super Ps.* 24 nn. 1-2 | D | Prayer is prepared by lifting the mind (Damascene: *oratio est ascensus intellectus in Deum*; Lam 3:41) and by trust; those who wait (*sustinent*) are those who await him *cum longanimitate* (Hab 2:3). |
| | Bellarmine, *Explanatio* 24 expl. 1-3 | D | The soul torn from earthly affections is lifted to God; "none of them that wait on thee shall be confounded" rests on the examples of the ancestors and God's promises. |
| | Rupert, *De div. off.* III.2 | L | The Introit's trust, the Gradual and the Alleluia ask that God show the freed soul his ways (his Mass, section 6). |
| | Sicard, *Mitrale* V (first Sunday) | L | Introit is the voice of mankind returning to its heavenly country; *Ad te levavi* now, as once it lifted its hands to idols; Gradual and Offertory repeat the Introit *ut qui stat, videat ne cadat*. Largely Rupert's words (section 8.5). |
| | Durandus, *Rationale* VI (first Sunday) | L | *per adventum Domini in carnem spes maxime elevatur*; the cantor raises his voice from low to high, *quod proprium est excitantis*, which the Epistle's *Hora est* also marks; the Introit sung in the person of the old man, or of John the Baptist. |
| | Schuster, *Sacramentary* I, pp. 321-322 | L | The Introit voices humanity "cast down, yet full of hope"; the Offertory shows the reason of the choice: "He who with watchful trust waits upon the Lord shall never be confounded" (his paraphrase). |
| Introit verse, Gradual verse: Ps 24:4 | Augustine, *En. in Ps.* 24.4 | D | The ways are narrow paths; asks to be shown them. |
| | Aquinas, *Super Ps.* 24 n. 4 | D | *Viae domini … sunt praecepta … Per has enim vias venit dominus ad nos*; the paths are the counsels. |
| | Bellarmine 24 expl. 4 | D | The ways are God's law; he asks to be taught "not speculatively, but practically", for grace that moves the will. |
| | Durandus | L | Christ coming shows his ways (Isa 2:3); the Epistle shows which ways. |
| Gradual respond: Ps 24:3 | Schuster p. 322 | L | The Gradual follows "an old liturgical rule" in taking the Introit's psalm (his statement; not checked further). |
| Alleluia: Ps 84:8 | Augustine, *En. in Ps.* 84.9 | D | *Hoc est quod cantavimus*; *salutare tuum, Christum tuum … Dedit enim nobis Christum, sed hominem: quem nobis dedit hominem, eum ipsum nobis daturus est Deum*; *Jam quidem sumus, sed per fidem … nondum sumus in re*. |
| | Bellarmine 84 expl. 7 | D | He now asks for the coming of the Saviour: "grant us thy salvation. Send us your Son for a Savior". |
| | Durandus | L | *Ostende nobis faciem tuam*: *Da nobis cognitionem tuam*. |
| | Sicard; Rupert | L | The Alleluia asks mercy because salvation *non est volentis … sed Dei miserentis* (Sicard). |
| | Schuster p. 322 | L | The Father's "pity and his salvation — which is Jesus Incarnate". |
| Communion: Ps 84:13 | Augustine, *En. in Ps.* 84.15 | D | Reads *dabit suavitatem*: God gives the sweetness of justice, so that our earth, confessing, yields good works; God's rain on the seed of the word. |
| | Bellarmine 84 expl. 12 | D | "For the Lord will give goodness": he will send his Holy Spirit, who will overshadow a virgin, "and thus our land, which was never ploughed nor sown … will yield her fruit". |
| | Rupert, *De div. off.* III.2 | L | *terra nostra, id est, uterus Virginis concipiens, dedit fructum suum, Deum et hominem proferens*. |
| | Sicard | L | *terra nostra, id est beata virgo concipiens dabit fructum suum, scilicet Deum et hominem* (Rupert's reading reproduced). |
| | Durandus | L | *benignitatem, id est affectum bonum: et terra nostra, scilicet caro, dabit fructum suum, id est bona opera*. |
| | Schuster p. 323 | L | The Eucharist a pledge of his goodness; hearts "rendered arid and sterile by sin" now bring forth fruit. |
| Epistle: Rom 13:11 | Chrysostom, *Hom. in Rom.* 24 (on v. 11) | D | Resurrection and judgment are nearer each day; as runners near the goal rouse themselves, so should we. |
| | Aquinas, *Super Rom.* 13 l. 3 | D | The sleep is of sin (Eph 5:14) or negligence; *propior … salus* is eternal life, near in time and by disposition; *secundum quod Ecclesia haec verba adventus tempore legit*, the words refer to the salvation of Christ's first coming, the Apostle speaking *ex persona omnium fidelium qui fuerunt ab initio mundi* (Isa 56:1). |
| | Augustine, *Conf.* VIII.5.12 | C | The sleep image: *conatibus expergisci volentium … "modo," "ecce modo," "sine paululum"*; *surge qui dormis*; who would free him *nisi gratia tua*. |
| | Durandus; Sicard; Rupert | L | The Introit's rising voice and the Epistle's *Hora est* (Durandus); the Epistle shows the ways to walk and not to walk (Rupert, Sicard). |
| Rom 13:12 | Chrysostom (on v. 12) | D | Neighbours rouse each other when the swallow sings; the arms of light; the one armed with the arms of light goes out "as the bridegroom goes forth with joyous looks from his chamber", "at once soldier and bridegroom". |
| | Aquinas l. 3 | D | Three nights: this life's ignorance, sin, and the time before the Incarnation; *nox praecessit* fits each; *dies appropinquavit*, by the Apostle's intention the day of glory, can also be the time of grace that draws near *per fidem et devotionem* (Phil 4:5). |
| | Durandus | L | *factus est dies, quando natus est Sol*. |
| Rom 13:13-14 | Chrysostom (on vv. 13-14) | D | Not prohibition of drink but of excess; Christ put on "all round" as a garment and dwelling within. |
| | Augustine, *Conf.* VIII.12.28-29 | C | Under a fig tree; *tolle lege*; reads Rom 13:13-14 and *luce securitatis infusa cordi meo*. Conversion narrative, not exegesis of the verse. |
| | Schuster pp. 321-322 | L | "the Church rouses us at last from sleep by those inspired words of the Apostle which once wrought the conversion of Augustine"; Christ as "a secret and supernatural garment of the soul". |
| | Durandus | L | *induamus nos in similitudine Christi … Filius Dei factus est homo, ut homo fieret filius Dei*. |
| Gospel: Lk 21:25-26 | Gregory, *Hom. in Ev.* 1.1-2 | D | The world is aging; some signs already seen, others feared; earthquakes heard of from other parts of the world; fiery battle lines seen in the sky before Italy fell; *virtutes caelorum* are the angelic orders. |
| | Ambrose, *Expos. in Luc.* X.36-40 | D | Figurative. The sun is Christ, *sol ille coelestis*, who *mea fide vel minuitur, vel augetur*: when many fall from religion, bright faith is darkened by the cloud of faithlessness (X.37). The moon is the Church, which cannot borrow light from Christ's rays when the vices of the flesh stand in the way; in persecutions love of this life shuts out God's light (X.37). The falling stars are *illi … resurrectionis gloria iam micantes*, the patriarchs and prophets, who *excident … hominibus* if the bitterness of persecution grows strong: *sic enim probantur boni, sic produntur infirmi* (X.38). Perhaps (*Fortasse*), as the awaited coming is a presence that happens in each one who receives Christ with all his affections, the heavenly powers are moved by an increase of grace (X.39-40). |
| | Augustine, Ep. 199.34, 39-40 | D | The eclipse at the crucifixion was greater than any later sign; the signs are better understood in the Church (199.39). *Ecclesia est enim sol et luna et stellae* (Cant 6:9); when sun, moon and stars fail, *Ecclesia non apparebit*, as persecutors rage; the falling stars are *multi, qui gratia fulgere videbantur*, who *persequentibus cedent et cadent*, and even the strongest faithful will be troubled (199.39). *Pressura gentium*, the nations on the left (199.40). |
| | Cyril of Alexandria, *Comm. in Luc.*, sermon 139 | D | After the siege (vv. 20-24) "He transfers His words … to the time of the consummation"; creation begins to be changed; fear itself will destroy many. |
| | Cyril of Jerusalem, *Cat.* 15.3 | D | The heavens rolled up to be raised "more beautiful"; converts from the Manichees are not to think "that this sun which shall be darkened is Christ". (On the synoptic parallel and Isa 34:4.) |
| | Bede, *In Luc.* VI on v. 25 | D | The PL 92 optical text is barely legible here: Joel 2:31; the distress of nations tied to Antichrist's time. Limit recorded (section 12). |
| Lk 21:27 | Gregory 1.2 | D | *In potestate et majestate visuri sunt quem in humilitate positum audire noluerunt*. |
| | Gregory 1.6 | D | The coming judge: if he so shook the earth through a wind, what will he do *cum per semetipsum venerit*? (Hebr 10:31; Ps 49:3; Zeph 1:14-16; Hag 2:22.) Present terrors are *sequentis irae praecones*, as unlike the last tribulation as the herald is unlike the judge; *Adventum namque aeterni judicis tanto securiores quandoque videbitis, quanto nunc districtionem illius timendo praevenitis*. |
| | Ambrose X.41-42 | D | The clouds are prophets and saints; he came *in nube levi incarnatus ex Virgine* (Isa 19:1). |
| | Augustine, Ep. 199.41 | D | *in nube* can mean the Church, or his own body as at the Ascension (Acts 1:11); he will not decide. |
| | Cyril of Alexandria | D | He will come "not secretly nor obscurely, but as God and Lord" and renew creation. |
| | Schuster p. 322 | L | The Church joins the second coming *in gloria majestatis suae* with the first *in humilitate passionis*. |
| Lk 21:28 | Gregory 1.3 | D | *levate capita, id est exhilarate corda … dum finitur mundus, cui amici non estis* (Jas 4:4). |
| | Bede on v. 28 | — | Copies Gregory 1.3 word for word; Gregory's words, not Bede's (section 8.5). |
| | Cyril of Alexandria | D | Redemption is the resurrection: the body puts on incorruption (2 Pet 3:10-12; Lk 21:36). |
| Lk 21:29-31 | Gregory 1.3 | D | The fig tree's fruit: *fructus mundi ruina est … Ad hoc crescit ut cadat*; the summer is the kingdom, when the clouds of mourning pass. |
| | Ambrose X.44-45 | D | Double figure: the fruit of faith (the Jews' confession; the summer of resurrection) or the leaves of the man of iniquity. |
| | Chrysostom, *Hom. in Mt.* 77 | D (parallel) | The fig tree shows the interval is short and the event certain as nature's course; a spiritual summer for the righteous, winter for sinners. |
| | Augustine, Ep. 199.42 | D | When the Son of man is seen, the kingdom is not yet, but near. |
| Lk 21:32 | Chrysostom, *Hom. in Mt.* 77 | D (parallel) | "Speaking not of the generation then living, but of that of the believers" (Ps 23:6): the generation of the faithful outlasts every trial. |
| | Bede on v. 32 | D | *Generationem autem aut omne hominum genus dicit, aut specialiter Judaeorum*; the *Amen* as Christ's oath. The *generatio* sentence is commonly Jerome's; not checked in Jerome (section 10). The *Amen* sentences are Augustine's, *In Ioh. tr.* 41.3-4 (section 8.5). |
| Lk 21:33 | Gregory 1.4 | D | Heaven and earth the most durable things, words the most fleeting; yet his words abide. |
| | Bede on v. 33 | D | The heaven that passes is the aerial heaven (2 Pet 3), renewed rather than destroyed. |
| | Cyril of Jerusalem 15.3 | D (parallel) | "the creatures are not as precious as the Master's words". |
| Whole discourse | Augustine, Ep. 199.1-3, 25-27, 45, 52-54 | D | Three comings in the discourse (Jerusalem; daily in the Church; at the end); Luke separates the city (vv. 20-24) from the last coming; perhaps all refers to the daily coming except what is plainly the last; of three views on the time, he who says "sooner" *optabilius loquitur, sed periculose fallitur*; *in quo enim quemque invenerit suus novissimus dies, in hoc eum comprehendet mundi novissimus dies*. |
| | Leo, Breviary lesson 4 (Sermon on the December fast) | C | Teaches from Lk 21:34 that the day is near though the hour is unknown. Read only as the Breviary prints it. |
| Collect | Schuster p. 321 | L | "we ask our Lord to come to our aid and to save us by his power from the dangers to which we are exposed through our sins". |
| | Rupert; Sicard; Durandus | L | The orations *manifeste … ad primum Domini respiciunt adventum* (Rupert); Sicard *Orationes manifeste primum adventum respiciunt*; Durandus adds *et possunt etiam adaptari congrue ad secundum*. None quotes an incipit (section 6). |
| Secret | Schuster p. 322 | L | The Roman epiclesis idea: the sacrifice's virtue purifies "that we may worthily receive him who is its Author". |
| Postcommunion | Schuster p. 323 | L | "inspired by Psalm xlvii" (Ps 47:10, *Suscepimus, Deus, misericordiam tuam in medio templi tui*; Douay "We have received thy mercy, O God, in the midst of thy temple"); preparation "for the approaching feast of our common ransom". |
| Two comings (Ps 84, Gospel, Postcommunion) | Cyril of Jerusalem, *Cat.* 15.1-2, 15.4 | C | "We preach not one advent only of Christ, but a second also"; the first "unobserved, like rain on a fleece"; as to the time "let no one be curious", nor "supinely slumber". |
| | Bernard, *In Adventu* 3.4, 4.1, 5.1 | C | Three comings (to men, into men, against men); the two advents as the Bridegroom's arms; the middle advent "the way … by which we must travel from the first to the last". |
| | Augustine, *En. in Ps.* 24.10 (v. 10, not appointed) | C | *universae viae Domini, duo adventus Filii Dei, unus miserantis, alter iudicantis*. |

## 5. Witness register

Standing from `src/sources/inventories/author-standing-v1.toml`.

| Witness | Standing | Role here | Locus read | State |
| --- | --- | --- | --- | --- |
| Augustine | father | direct; carrier | Ep. 199 (whole; augustinus.it restricted copy matched); *En. in Ps.* 24 (Latin, new fetch; English NPNF); *En. in Ps.* 84.1, 9, 15; *Conf.* VIII.5.12, 12.28-29 (new fetch) | inspected |
| Gregory the Great | father | direct; carrier | *Hom. in Ev.* 1.1-6 (section 6 printed inline after section 5 in the tracked text) and its inscription | inspected |
| Ambrose | father | direct; carrier | *Expos. in Luc.* X.2, 36-45 | inspected |
| John Chrysostom | father | direct; carrier | *Hom. in Rom.* 24 on 13:11-14; *Hom. in Mt.* 77 on 24:32-35 | inspected |
| Cyril of Alexandria | father | direct; carrier | *Comm. in Luc.*, sermon 139 (on 21:5-36); sermon 140 opening (21:37-38) | inspected |
| Cyril of Jerusalem | father | direct (parallel); carrier | *Cat.* 15.1-4, 15.22 | inspected |
| Bede | father | direct, with copied matter | *In Luc.* VI on 21:25 (OCR), 28-33 (checked text) | inspected |
| Leo the Great | father | context | Breviary lesson 4 only | inspected (lesson) |
| Thomas Aquinas | doctor | direct; carrier | *Super Rom.* 13 l. 3; *Super Ps.* 24 nn. 1-4 | inspected |
| Robert Bellarmine | doctor | direct; carrier | *Explanatio* 24 expl. 1-5; 84 title, expl. 7, 12 | inspected |
| Bernard of Clairvaux | no row in the standing file (section 11) | context; may not carry until a row exists | *In Adventu* 3.4, 4.1, 5.1 (checked English) | inspected |
| Ildefonso Schuster | blessed | liturgical commentator | *Sacramentary* I, pp. 320-323 (pp. 321-323 on page images) | inspected |
| William Durandus | ecclesiastical writer | liturgical commentator | *Rationale* VI, first Sunday of Advent (1612 Lyon OCR) | inspected |
| Sicard of Cremona | ecclesiastical writer (standing file) | liturgical commentator | *Mitrale* V, first Sunday (PL 213 OCR) | inspected |
| Rupert of Deutz | ecclesiastical writer (standing file) | liturgical commentator | *De div. off.* III.2 (PL 170 OCR) | inspected |

## 6. Liturgical commentators

No locus row for this Mass exists in `src/sources/commentary/formulary-loci.yaml`
(section 3). Each Mass below was identified by its elements, read in the
commentator's own text.

| Commentator, heading | Elements matching the 1962 | Elements differing | Use permitted |
| --- | --- | --- | --- |
| Rupert of Deutz, *De divinis officiis* III, cap. 2, *De prima Dominica adventus Domini* (PL 170, Migne OCR) | Introit *Ad te levavi* with *Vias tuas … demonstra*; Gradual (*in graduali*); Alleluia; Epistle *Scientes quia hora est*; Offertory *Ad te levavi*; Communion *Dominus dabit benignitatem* | Gospel: Mt 21:1-9, the ass and its colt, which he makes the key to the whole office; Offertory adds the verse *Dirige me in veritate tua*; station *ad Sanctum Petrum*. The Collect, Secret and Postcommunion are named only as *collecta*, *super oblata*, *ad complendam*, without incipits, so their identity with the 1962 orations is not established. | Introit, Gradual, Alleluia, Epistle, Offertory antiphon, Communion; never the Gospel connection. |
| Sicard of Cremona, *Mitrale* V, the first Sunday of Advent (PL 213, Migne OCR, the column under the running head *205*) | Introit, verse *demonstra*; Epistle; Alleluia *Ostende*; Gradual *Universi*; Offertory *Ad te levavi*; Communion *Dominus dabit* | Gospel Mt 21 (*Cum appropinquasset … solvere asinam*); Offertory verse *Dirige me*; station *ad sanctum Petrum*; orations unnamed. | As for Rupert; Sicard reproduces much of Rupert (section 8.5). |
| William Durandus, *Rationale divinorum officiorum* VI, the first Sunday of Advent (Lyon 1612, tomus secundus, OCR) | Introit *Ad te levavi* with *Vias tuas … demonstra*; Epistle Rom 13; Gradual *Universi*; Alleluia *Ostende*; Offertory *Ad te levavi*; Communion *Dominus dabit benignitatem*; and, *in nonnullis Ecclesiis*, the Gospel *Erunt signa* (Lk 21) | In other churches Mt 21 or Mk 1; orations unnamed | All the shared elements, the Gospel included where he speaks of the churches that read *Erunt signa*; he himself joins that Gospel to the Epistle: *Cui adaptatur epistola, ubi dicitur: propior est nostra salus*. |
| Bl. Ildefonso Schuster, *The Sacramentary* I (London 1924), "First Sunday of Advent", pp. 320-323 | All ten, named or cited: Introit Ps 24; Collect; Epistle Rom 13:11-14; Gradual Ps 24; Alleluia Ps 84; Gospel Lk 21:25-33; Offertory Ps 24; Secret; Communion Ps 84; Postcommunion | none | Every element. |
| Honorius, *Gemma animae* (PL 172 OCR) | — | A search for *Ad te levavi* found only the Lenten Tract (III Lent); no Advent chapter located | none (negative, section 10) |
| Amalarius (PL 105 OCR) | — | no hit for *Ad te levavi* in the held OCR | none (negative) |

Schuster's two historical claims about the station and about Gregory's
homily, and his "earthquake", are disputed by the checked texts (section 8.4).

## 7. Consequential textual difficulties

Each is a place where the appointed words force a question, the principal
witnesses answer it differently, and the answer changes the reading.

**7.1 Literal signs or figures of the Church (Lk 21:25-26).** Words: *Erunt
signa in sole, et luna, et stellis … virtutes cælorum movebuntur.* Gregory
takes the signs as coming portents, some already seen, and reads them as the
aging world's last blows meant to wean love from it (1.1, 1.5); the present
terrors are heralds of the judge's wrath (1.6). Cyril of Alexandria and Cyril
of Jerusalem take them of creation's change at the end, the second warning
against identifying the darkened sun with Christ. Ambrose and Augustine both
read the signs of the Church under persecution, but they assign the figures
differently. Ambrose: the sun is Christ, whose light *mea fide vel minuitur,
vel augetur*, darkened when many fall from religion; the moon is the Church,
which cannot borrow his light when the vices of the flesh obstruct it; the
stars are the patriarchs and prophets, already shining with resurrection
glory, lost to men when persecution grows harsh (X.37-38). Augustine: the
Church is sun, moon and stars (Cant 6:9), and when they fail the Church will
not appear; the stars that fall are the many who seemed to shine with grace
and give way to persecutors (Ep. 199.39). Augustine also refuses to make
present calamities a proof of nearness (199.36-37, 52-54). What changes: on
Gregory's reading the hearer is told to look at the world's ruin and rejoice;
on Augustine's and Ambrose's he is told the signs run through the Church's
age of persecution, in which many fall from the faith, and on Augustine's
that to date the end from them is a danger. Whether the darkened sun is Christ
(Ambrose) or the Church (Augustine), and whether the fallen stars are the
patriarchs and prophets lost to men (Ambrose) or the apparently shining who
give way (Augustine), is a difference the study must keep (section 8.2).

**7.2 "This generation" (Lk 21:32).** Words: *non præteribit generatio hæc,
donec ómnia fiant*. Chrysostom (on the parallel Mt 24:34) reads the generation
of believers; Bede gives the whole human race or the Jewish people. None of
the witnesses read takes it of Jesus' contemporaries as a dated term. What
changes: the verse stops being a chronological claim and becomes a promise of
the Church's endurance (Chrysostom) or of the race's survival to the end.

**7.3 The Gospel's opening (Lk 21:24-25).** The Missal's *In illo témpore:
Dixit Iesus discípulis suis: Erunt signa* drops the Vulgate's *Et*, which ties
v. 25 to the fall of Jerusalem (vv. 20-24). This is a textual observation about
the lesson's boundary; it supports no claim about why the lesson begins there.
Augustine (Ep. 199.27) and Cyril of Alexandria (sermon 139) both distinguish
the city's fall from what follows, so a study that reads vv. 25-33 of the end
has them, not the boundary, as its warrant; Augustine still allows part of the
discourse to be the daily coming in the Church (199.45).

**7.4 "Nearer than when we believed" (Rom 13:11) and "the kingdom is near"
(Lk 21:31).** Chrysostom takes nearness in time: every day brings resurrection
and judgment closer. Aquinas gives nearness in time and by disposition, and
adds that as the Church reads the words in Advent they speak of the first
coming, in the person of all the faithful since the world began. Augustine
holds the time unknown and the desire right either way (199.1). Durandus joins
the Gospel's *prope est regnum Dei* with the Epistle's *propior est nostra
salus*. What changes: whether the Sunday's urgency is a calendar (soon), a
condition (prepared), or a season of the Church's memory of the first coming.

**7.5 "Our earth shall yield her fruit" (Ps 84:13).** Rupert, Sicard and
Bellarmine read the earth as the Virgin and the fruit as Christ. Augustine
reads the confession of the sinner and the good works God's sweetness makes
grow; Durandus the flesh yielding good works; Schuster hearts made fruitful by
the Eucharist. This is a real disagreement over what the Communion sings:
the Incarnation, or the grace that makes us fruitful. The two can be held
together only as different senses, and the study must say which witness gives
which.

**7.6 "In a cloud" (Lk 21:27).** Ambrose: the cloud of the flesh, *nube levi*
(Isa 19:1), and the clouds of prophets and saints. Augustine: the Church, or
his body as at the Ascension, undecided. Gregory: power and majesty against
the humility once refused. The Missal's singular *nube* agrees with the
Clementine; Gregory's lesson text reads *in nubibus*.

## 8. Material disagreements

**8.1 Present calamity as sign.** Gregory reads his own city's calamities —
fiery battle lines seen in the sky before Italy fell (1.1), and the sudden
storm *nudius tertius* (1.5) — as the end's approach, and calls such terrors
*sequentis irae praecones*, heralds of the wrath to come, as unlike the last
tribulation as a herald is unlike the judge (1.6). Augustine, answering
Hesychius, says that such evils are common to every age and that to say
"sooner" is to speak desirably but err dangerously (Ep. 199.36-37, 54). Both are kept; neither is smoothed
into the other.

**8.2 The sun, the moon and the stars.** Augustine and Ambrose differ on
two identifications. On the sun: for Ambrose the sun is Christ, *sol ille
coelestis*, whose light grows or wanes in the believer's faith (X.37); for
Augustine the Church is sun, moon and stars together, *Ecclesia est enim sol
et luna et stellae* (Cant 6:9), so that when they fail *Ecclesia non
apparebit* (Ep. 199.39). On the stars: for Ambrose the stars that fall are
the patriarchs and prophets, already shining with resurrection glory, who
*excident … hominibus* when persecution grows harsh (X.38); for Augustine they
are *multi, qui gratia fulgere videbantur*, who yield to persecutors and fall
(199.39). They agree that the Church is figured among the lights (for
Ambrose the moon; for Augustine all three) and that the signs are read of the
Church in persecution, in which many fall from the faith (Ambrose: *plurimis … a
religione deficientibus*; Augustine: *multi … cedent et cadent*) and the good
are proved (Ambrose: *sic enim probantur boni, sic produntur infirmi*). A
study must give each identification to its own author and may credit both
only with the shared reading. Ambrose's figure (the sun is Christ, dimmed by
faithlessness) and Cyril of Jerusalem's warning (the darkened sun is not
Christ) address different errors: Ambrose speaks of Christ's light in the
believer; Cyril refutes Manichaean worship of the sun. Complementary, not a
dispute, but a study must not cite Cyril against Ambrose or vice versa without
saying so.

**8.3 Which coming.** Augustine and Bernard admit a coming between the two;
Cyril of Jerusalem names two; Aquinas lets the Church's Advent reading of Rom
13 point to the first; Gregory and the two Cyrils read the Gospel of the last.
These are complementary emphases. Gregory's text of v. 27 reads *in nubibus*;
the Missal *in nube*.

**8.4 Station, occasion and Schuster's account.** The 1962 station is St Mary
Major (printed heading). Gregory's homily, as the edition read prints it, is
*Habita ad populum in basilica sancti Petri apostoli, Dominica secunda
Adventus Domini*, with the lesson Lk 21:25-32. Rupert and Sicard place the
first Sunday's station at St Peter's. Schuster says "several of the ancient
manuscripts" place the homily at St Mary Major and that Gregory preached it
there; this stage read no such manuscript witness. Schuster also calls the
calamity "an earthquake which only three days before had destroyed churches
and houses". Gregory's account of that event runs through two sections. In
1.5: *Nudius tertius, fratres, agnovistis quod subito turbine annosa arbusta
eruta, destructae domus, atque Ecclesiae a fundamentis eversae sunt.* In 1.6:
*invisibilis judex venti tenuissimi spiritum movit, unius procellam nubis
excitavit, et terram subruit, casura tot aedificiorum fundamenta concussit*,
and again *Ecce, ut praediximus, aerem movit, et terra non subsistit*. Gregory
describes a whirlwind sent by the judge that shook the ground and threw down
buildings, and he does not call it an earthquake. The agent in both sections
is wind and cloud (*turbo*, *venti … spiritum*, *procellam nubis*, *aerem
movit*); the ground's shaking is what the wind did. The one *terrae motus* in
the homily is in 1.1, where earthquakes that overthrow cities are reported
*ex aliis mundi partibus*, from elsewhere, as one of the Gospel's signs. So
Schuster's "earthquake" is his reading of the event, close to 1.6's words
but not Gregory's name for it. The study may cite Gregory for what he says of
Lk 21 and must not narrate the Sunday on which he preached it; Schuster is not
to be cited for the station of the homily or for an earthquake, and Gregory's
event, if mentioned, is a whirlwind that shook the ground.

**8.5 Whose words are whose.** Bede's comment on Lk 21:28 is Gregory's 1.3
copied; credit Gregory. So is his comment on vv. 29-31 (the fig tree's fruit,
*fructus mundi ruina est*), Gregory 1.3 again. Bede's sentences on v. 32 that
call *Amen* the Lord's oath, left untranslated by Greek and Latin, follow
Augustine, *In Ioh. tr.* 41.3-4 on Jn 8:34 (checked in the NPNF English by
source registration); credit Augustine. Bede's *generatio* sentence is likely
Jerome's and is cited, if at all, as Bede's text with that limit. Sicard reproduces Rupert's
first-Sunday chapter in substance and much wording (the ass, *Ascensorem
suscipe regem*, *offensus eques suum velit mutare vehiculum*, the Virgin
earth); Durandus follows Sicard on the orations (*Orationes … primum adventum
respiciunt*) and adds the clause on the second coming. Cite the earliest
checked author for each sentence, and the later one only for what he adds.
The Schuster sentence on the Offertory ("He who with watchful trust waits upon
the Lord …") is his paraphrase, not a translation of the Missal.

## 9. Chronology: the generated record inspected

`tools/tpt proper-chronology record --provider claude --document
liturgy/roman-rite/1962/propers/temporal/01-first-sunday-of-advent --write`
and `annotations … --presentation orientation-v3 --write` were run on
2026-11-25, after the corpus change in 9.1; they wrote
`research/chronology.toml`, `research/chronology-annotations.tex` and
`research/chronology-table.tex`. Rows inspected:

| Rows | Passage | Generated context and date | Inspection |
| --- | --- | --- | --- |
| Introit, Offertory, Gradual (three groups of three rows) | Ps 24:1-4 (Vg.; Heb. 25) | Traditional attribution: David's reign, c. 1055-1015 B.C. (Corbett, usual chronology); historical setting: occasion date unresolved; composition: before c. 165 B.C. | The Vulgate title *In finem. Psalmus David* is a Davidic attribution, which the row labels as attribution, not composition. The commentators read (Augustine, Aquinas, Bellarmine) name no historical occasion; Bellarmine's title is "A Prayer for Grace, Mercy, and Protection Against Our Enemies". The occasion row truly reports the corpus's absence. The composition boundary is the corpus's (USCCB Psalms introduction) and is generic. The generator prints the same Ps 24 answers once per element; that is its v3 grouping, not an error of scope. |
| Alleluia, Communion | Ps 84:8, 84:13 (Vg.; Heb. 85) | Composition: Psalms of the Sons of Korah, c. 740-536 B.C. (Korahite collection estimate); occasion unresolved | Catholic Encyclopedia, "Psalms" (tracked article text, line 176): "between the days of Isaias and the return from exile". A collection estimate. Augustine and Bellarmine read v. 2's *captivitatem Jacob* of the captivity of sin and the coming of Christ, not of a dated return; no occasion is supplied. |
| Gospel | Lk 21:25-33 | Narrated event: Jesus foretells Jerusalem's fall and His coming; Jerusalem, by the Temple in Luke's narrative; Mount Olivet in Matthew and Mark; c. A.D. 29 (derived; Maas's chronology). Composition: Luke; disputed, c. A.D. 70 or before the end of Paul's Roman imprisonment | Before 9.1 the Gospel was composition-only. The event row is the speaking of the discourse, dated through Maas (Catholic Encyclopedia VIII, "Jesus Christ", tracked article text lines 131-134, reread): the Ninth Journey "February, A.U.C. 782- Passover, 782 (Cf. Luke 17-22 …)", and "Jesus ended this day by uttering the prophecies concerning the destruction of Jerusalem, His second coming, and the future judgement". The composition rows: Catholic Encyclopedia, "The New Testament" (tracked, line 33): "About the year 70"; the Biblical Commission's 1912 response (corpus-held). Kept apart from the event. |
| Epistle | Rom 13:11-14 | Composition: Romans; proposals span A.D. 57-58 | Catholic Encyclopedia, "St. Paul" (line 45): "(Romans), 57"; "Epistle to the Ephesians" (line 69): "the Epistle to the Romans (58)". |

No date reaches the study's page 2 from anywhere but this record. The
prophecy's referents (the fall of Jerusalem in A.D. 70; the coming) are not
dates of the passage and no prophetic-referent binding exists.

### 9.1 The Gospel's event, added to the shared corpus

Made under `guidance/scripture-chronology.md` sections 6, 14 and 15, following
the corpus's own pattern for `life-of-christ.closing-charge-to-watch` (Mark
13:33-37), which holds a part of the same discourse as its own subject with a
date derived from `life-of-christ.prophecies-on-mount-olivet`. Changes, all
under `src/sources/chronology/`:

- **Why a new subject and not a binding to the Olivet event.** That event is
  the right occurrence (Maas makes the three synoptic discourses one Tuesday
  speech), but its `settings` place, *Mount Olivet by narrative continuity*,
  is Matthew's and Mark's, and a setting attaches to a subject, not to a
  binding (`scripts/_proper_chronology.py`, the orientation row builder).
  Binding Luke to it would print Olivet beside Lk 21:25-33, which Luke does not
  say: he opens the discourse with talk of the Temple (21:5), names no
  departure, and closes with Jesus teaching in the Temple by day and lodging
  on Olivet by night (21:37-38). Correcting the Olivet setting instead would
  alter the generated chronology of the Twenty-fourth Sunday after Pentecost
  leaf, a reviewed record outside this stage.
- **Event** `life-of-christ.prophecies-in-the-temple-lucan-account`, *Jesus
  foretells the fall of Jerusalem and the coming of the Son of Man, as Luke
  places the discourse*; one `catholic-traditional-v1` claim, `derived`,
  c. A.D. 29 (`approximate-year`), derivation input
  `life-of-christ.prophecies-on-mount-olivet`, qualification *Maas's
  chronology*; sources Luke 21:5, 7, 36-38 and the two Maas passage records
  already registered.
- **Binding** `narrated-event`, Luke 21:5-36: the whole speech, from the
  remark about the Temple to the charge to watch and pray. Verses 1-4 (the
  widow) and 37-38 (Luke's summary) are outside. No other leaf's chronology
  record outside this one reaches Luke 21 (searched; the other provider's
  leaf for this identity was not opened, by instruction, and is not known).
- **Setting**, `narrated-event`: *Jerusalem, by the Temple in Luke's
  narrative; Mount Olivet in Matthew and Mark*, sources Lk 21:5, 21:37, Mt
  24:3, Mk 13:3. The place in Luke is by narrative continuity; the two places
  are not harmonized.
- **Checks.** `tools/tpt scripture-chronology validate` (valid: 296 events,
  399 bindings), `build` (coverage: `Luke.21.5-36` now `dated`; `Luke.21.1-4`
  and `37-38` unchanged, composition-only) and `check` (current). The leaf's
  record and annotations were written after the change.
  `scripts/build_profile_contract_manifest.py --check` already failed on the
  base before this change (575 tracked lines against 578 derived); it was not
  regenerated here, so as not to fold unrelated drift into this change
  (section 11).

## 10. Negative results and unresolved leads

- **Cassiodorus**, *Expositio Psalmorum* 24 and 84: held, not read. A lead;
  an ecclesiastical writer in any case.
- **Catena aurea in Lucam** on 21:25-33: held (21:28 passage), not read; its
  Gregory is read directly.
- **Jerome**, *In Mt.* IV on 24:34-35: held only as PL 26 facsimile pages; not
  read. Bede's *generatio* sentence is therefore not credited to Jerome.
- **Augustine, *De civitate Dei* XX** on the signs: held; not read.
- **Leo**, Sermon on the December fast: only the Breviary's lesson read.
- **Roman Psalter**: no witness read; the textual source of the chants'
  *qui te exspectant*, *notas fac*, *Ad te levavi* without *Domine*, the
  Gradual's added *Domine* and *Dominus dabit* without *Etenim* is not
  established. Only Augustine's psalter was compared (section 2.3).
- **Guéranger**, *The Liturgical Year*, Advent volume: not held (the library
  holds English vols. 10-15). Lead for a later production.
- **Alphonsus Liguori** (Sunday sermons) and **Anthony of Padua**: no held
  text for this Sunday located; not searched further.
- **Honorius**, *Gemma animae*, and **Amalarius**: searches of the held OCR
  for *Ad te levavi* found no Advent chapter (section 6). OCR-limited; not a
  finding that they have none.
- **Theophylact, Bonaventure, Albert, Lyra, Denis, Origen, Ephrem** on Lk 21:
  not registered (discover). Not acquired.
- **Gutenberg Confessions (Pusey English)**: two fetches returned a
  maintenance page (HTTP 503). The Latin was read (section 13), and source
  registration then read Pilkington's English of VIII.5.12 and VIII.12.28-29 in
  the tracked NPNF I.1 text, the library's lawful English of the work.
- **Bede on v. 25-27**: the PL 92 optical text is too damaged to quote; only
  its sense is recorded.

## 11. Shared-record defects (reported, not repaired)

- **Latin ledger** (`src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml`):
  no rows for the Introit, Gradual, Alleluia, Gospel, Offertory or Communion of
  `advent-1`, though the 1862 pages carry the same words (section 2.2). Owner:
  the ledger.
- **Author standing** (`src/sources/inventories/author-standing-v1.toml`): no
  row for Bernard of Clairvaux, a canonized saint and Doctor. Until one exists
  he cannot be a declared carrying author. Owner: the inventory.
- **Commentator index** (`src/sources/commentary/formulary-loci.yaml`): no
  locus for this Mass; Rupert III.2, Sicard's *Mitrale* V chapter and
  Durandus VI's first-Sunday chapter (section 6) are candidates. Owner: the
  index.
- **Chronology review manifest**
  (`src/sources/chronology/profile-contract-rereview-manifest.tsv`) is stale
  against a fresh derivation on the base commit, before this stage's change.
  Owner: the chronology corpus.
- **Olivet setting**: `life-of-christ.prophecies-on-mount-olivet` carries a
  Matthean place; the corpus owner may decide whether Luke's account should in
  future be merged under a place-neutral setting (section 9.1).
- **Gregory's passage record**
  (`passage.gregory-the-great.homiliae-in-evangelia.wikisource-web-2026-09-17.1.1-5-luke-21`):
  its `locus` read `1.1-5` and its context "§§1–5" and "the five paragraphs",
  though its own transcription segment for physical line 19 holds section 6
  entire (*6. Sed considerandum nobis est …* to *… timendo praevenitis*).
  Repaired by source registration (iteration 1); see section 13.2.
- `tools/tpt calendar-rubrics day` refused during the browser-products build
  (research/context.md); not rerun.

## 12. Evidence bounds

- Latin: verified on page images (1962, 1862). English: Lasance on page
  images; Douay from tracked verse texts.
- Patristic and medieval texts were read in the editions bound, many in
  optical text (Rupert, Sicard, Durandus, Bede PL 92); where OCR is damaged
  the sense, not the words, is recorded. Durandus, Rupert and Sicard are cited
  by book and chapter with the OCR's location; their printed columns were not
  read on images.
- Schuster p. 320 was read only in the OCR text; pp. 321-323 on the page images
  of the registered Internet Archive scan.
- Gregory's homily is cited by the numbering of the edition read, sections
  1-6: sections 1-5 begin physical lines 15-19 of the extracted text, and
  section 6 is printed inline on line 19 after section 5; line 20 is the
  extractor's source note. Augustine's Letter 199 is cited by its own section
  numbers in the augustinus.it text.
- Aquinas's *Super Psalmos* and *Super Romanos* are restricted remote
  artifacts, read in copies matched to their registered hashes.
- Cyril of Jerusalem and Chrysostom on Matthew comment on the synoptic
  parallels, not on Luke's words; they are parallel witnesses.
- Nothing here establishes why the compilers chose these texts or set them
  together; every whole-Mass reading is editorial synthesis.

## 13. Handoff to source registration

Every binding in research/source-bindings.toml is a registered record. Two
texts were read in new fetches that are not yet registered; their bytes and
receipts are held in this run's scratch area (the result's `notes` give the
locations):

| Source | URL | Retrieved | Bytes | SHA-256 | Locus read | Rights note |
| --- | --- | --- | --- | --- | --- | --- |
| Augustine, *Enarrationes in Psalmos* 24, Latin, augustinus.it | <https://www.augustinus.it/latino/esposizioni_salmi/esposizione_salmo_026_testo.htm> | 2026-11-25 | 9,900 | `614fe7034fe6ce563753ba42ddaf5e7d1fe1651160320a64788287fa92efdf1a` | §§ 1-5, 10, 21; psalter readings | Same site and terms as the registered restricted augustinus.it artifacts (Ep. 199; Ps 85); register restricted unless shown otherwise. The page's numbering is offset (026 = Ps 24). |
| Augustine, *Confessiones* VIII, Latin, The Latin Library | <https://www.thelatinlibrary.com/augustine/conf8.shtml> | 2026-11-25 | 39,278 | `be90ce92453e55099573c1fdd6a885d93407d54bc616e51ff39f39477de6f416` | VIII.5.12; VIII.12.28-29 | Ancient text; site edition unidentified; the registered CSEL 33 facsimile (`…1896-knoll-csel-33.ia-facsimile-pdf-aabe4272`) is the lawful edition to collate against. |
| Augustine, Ep. 199, augustinus.it | already registered (`artifact.augustine.epistula-199.2026-11-23-augustinus-it.letter-199-5b570f96`) | 2026-11-25 | 88,756 | matched | §§ 1-3, 25-27, 34-45, 52-54 | restricted |

Registered remote artifacts fetched whole and matched (no new registration
needed): the 1962 facsimile, Pustet 1862 (102,880,787 bytes), Lasance 1945
(75,268,976), Aquinas *Super Psalmos* 21-30 and *Super Romanos* 12-16,
Schuster vol. I in both the Isidore OCR-only PDF (10,988,816) and the Internet
Archive scan (149,350,698, SHA-256 `13aa55ad…a3299`). The Gutenberg fetch
returned a maintenance page and is not a source.

Every checked witness for `research/source-dispositions.toml`, with the
Scripture each actually expounds (native locus first):

- Gregory, *Hom. in Ev.* 1 — Lk 21:25-33 (his lesson 25-32; he treats v. 33).
- Ambrose, *Expos. in Luc.* X.36-45 — Lk 21:25-31; X.2 — Ps 109 (context).
- Augustine, Ep. 199 — Lk 21 and parallels, Dan 9, Acts 1:7; 199.39-41 on Lk
  21:25-27.
- Augustine, *En. in Ps.* 24 — Ps 24:1-4 (and v. 10 for context); *En. in Ps.*
  84.9 — Ps 84:8; 84.15 — Ps 84:13 (his text *suavitatem*).
- Augustine, *Conf.* VIII.12.29 — Rom 13:13-14 (narrative reception, not
  exegesis); VIII.5.12 — Eph 5:14 echo (context for Rom 13:11).
- Bede, *In Luc.* VI — Lk 21:25-33 (vv. 28-31 copied from Gregory).
- Cyril of Alexandria, *Comm. in Luc.* sermon 139 — Lk 21:5-36.
- Cyril of Jerusalem, *Cat.* 15.3 — Mt 24:29, 35 and Isa 34:4 (parallel);
  15.1-2, 4 — two comings (context).
- Chrysostom, *Hom. in Mt.* 77 — Mt 24:32-35 (parallel to Lk 21:29-33);
  *Hom. in Rom.* 24 — Rom 13:11-14.
- Aquinas, *Super Rom.* 13 l. 3 — Rom 13:11-14; *Super Ps.* 24 nn. 1-4 —
  Ps 24:1-4.
- Bellarmine, *Explanatio* 24 expl. 1-5 — Ps 24:1-5; 84 expl. 7 — Ps 84:8;
  expl. 12 — Ps 84:13.
- Bernard, *In Adventu* 3.4, 4.1, 5.1 — no single passage (context).
- Leo, Breviary lesson 4 — Lk 21:34 (context, Office use).
- Rupert III.2, Sicard *Mitrale* V, Durandus VI, Schuster I pp. 320-323 —
  liturgical commentary on the Mass's elements (section 6).

### 13.1 Registration outcome (source registration, iteration 0)

Both new fetches were refetched on 2026-11-25 and were byte-identical to the
research receipts (SHA-256 and byte size matched). They are registered as
remote, unresolved-rights artifacts, since neither page carries a licence:

- `artifact.augustine.enarrationes-in-psalmos.latin-augustinus-it-web-2026-09-05.augustinus-it-ps024-614fe703`,
  filed under the existing augustinus.it edition like its Ps 85 page
  (remote, as that edition's other pages are), the complete Enarratio in
  Psalmum 24, sections 1-22.
- `edition.augustine-of-hippo.confessiones.the-latin-library-web-2026-11-25`
  (crediting James J. O'Donnell's edition) and its artifact
  `artifact.augustine-of-hippo.confessiones.the-latin-library-web-2026-11-25.book-8-html-be90ce92`,
  Book VIII complete (8.1.1-8.12.30).

Admitted to the Catena (verified passages with canonical edges): Augustine,
*En. in Ps.* 84.1 and 84.9 (Ps 84:8) and 84.15 (Ps 84:13), in the tracked
Latin, with Coxe's English of 84.9 and 84.15 (NPNF I.8, Psalm LXXXV §6 from
ver. 7 and §12) as excerpt English versions. Already admitted and confirmed
here: Gregory's Homily I (the passage whose ID reads 1.1-5, which holds
sections 1-6; section 13.2); Ambrose X.44-45; Bede on vv. 28-33 (now crediting
Gregory and Augustine in their edges); Chrysostom on Rom 13:11-14; Augustine's
English on Ps 24:1-5, 10; Bellarmine on Ps 24:1-5, 84:8, 84:13. The English
of Augustine on Ps 24 is admitted; his Latin of it, held only remotely, is
not. Every binding's disposition, with what deferred witnesses still lack, is
in research/source-dispositions.toml.

### 13.2 Registration outcome (source registration, iteration 1)

No new source was read in a fetch after iteration 0, and nothing new was
registered. Every tracked artifact the bindings reach (37) was re-hashed and
matched its registered SHA-256 and byte size; the remote and restricted ones
were not refetched, since no binding to them changed.

Gregory's Homily I was reread at physical lines 10-20 of the tracked text
(`gregory-whole.txt`, SHA-256 `dc25dd69…618d`, 629,050 bytes, matched). Line 19
holds section 5 and then section 6 inline (*6. Sed considerandum nobis est …*
to *… timendo praevenitis*); line 20 is the extractor's source note. The shared
records were corrected to that count:

- the passage
  `passage.gregory-the-great.homiliae-in-evangelia.wikisource-web-2026-09-17.1.1-5-luke-21`
  now has locus `1.1-6` and a context naming six sections, with a dated note
  of the correction. Its text, segments, line range and verification date are
  unchanged, and its ID keeps its original form, because a stable ID is not
  re-keyed to a corrected label. This leaf is the record's only bound
  consumer (`tools/source-library uses`); bindings 13-14 are unaffected in
  meaning, binding 14's locus is now `1.1-6`, and its fingerprint and digest
  are re-pinned;
- its Catena edge's basis in `src/sources/commentary/fragment-loci.yaml` names
  six sections, and the two English-version bases there now read "§§2–6" (Bute)
  and "§§1–6" (Oxford Catena Aurea);
- the same English-version wording was corrected in the two English excerpts'
  own records (the Bute *advent-opening* and Oxford *gregory-on-luke-21-28*
  passages and segments) and in their own Catena rows. No publication binds
  those four records.
