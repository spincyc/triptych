# Research scope — `PC-S01-B`, First Sunday of Advent, Year B

Research stage of `proper-study` v20, run `99f04ef5cf9b711b`, iteration 0,
26 November 2026, at commit `cbccbfcb3be4896c95225d8cd281e2b0684a12e9`. This
record states what the research stage read, where, in what form, and what it
did not read. The second research iteration (the same day) repaired the
research review's findings: it traced Bede's comments on Mark 13:32–33 to
Jerome on Matthew 24 (sections 3.1 and 7), corrected the psalm-to-reading row
of `propers/verified.md` (section 3.3), regenerated the chronology record
(section 8.1) and brought the context's registration notes and the official
bindings up to date. Text control is in [`../propers/verified.md`](../propers/verified.md)
and the [owner](../../shared/formularies/pc-s01-first-sunday-of-advent/propers/verified.md);
the identity and inventory in [`../instance/manifest.md`](../instance/manifest.md);
interpretation reasoning in [`interpretations.md`](interpretations.md); source
use in [`source-bindings.toml`](source-bindings.toml).

No other leaf is evidence here. The other provider's leaf for this identity,
its release and production records, and every 1962 record (including both
providers' 1962 First Sunday of Advent leaves and production records) were not
opened. Some library records consulted below were registered on 22–24 November
2026 by other productions; they were used as provider-neutral library records,
and every witness this record relies on was read by this stage in the bytes
named.

## 1. How far this sweep goes, and what was re-verified

- **Context.** `research/context.md` was read whole. Its downloads were
  re-hashed before use and all matched (`propers/verified.md`, first table).
  Its two citation questions are settled in `propers/verified.md` findings 1
  and 2; its owner questions in owner findings 5–8; its ritual-book lead under
  Branches in `propers/verified.md`. No contextual error was found. One
  precision is added: the context's description of the readings page (the
  mountains' quaking standing once) is now explained by the NABRE note on
  Isaiah 64:2 (`propers/verified.md` finding 1).
- **Finding aids.** `tools/tpt commentary-work-index discover` was run
  uncapped for every appointed passage (Isaiah 63:16–17; Isaiah 64:1–8 in
  Vulgate numbering; Psalm 79:2–19; 1 Corinthians 1:3–9; Psalm 84:8; Mark
  13:33–37; Psalm 24:1–3; Psalm 84:13). `tools/tpt commentary-work-index
  formulary --calendar postconciliar --mass advent-1` compared 40 loci on the
  formulary's elements and listed none and no structural match: no liturgical
  commentator held in the index comments on this Mass as a whole (section 3.9).
  Discover's results are finding aids; every witness relied on was then read at
  its locus.
- **Reading languages.** Jerome on Isaiah and Aquinas on Isaiah and 1
  Corinthians were read in Latin (Jerome on page images of Migne; Aquinas in the
  Corpus Thomisticum electronic text); Jerome on Matthew 24:36–43 in Latin on
  page images of Migne PL 26 (iteration 1; bound both to the volume and to the
  library's segment for Jerome's commentary); Bede on Mark and Gregory's homilies in
  tracked electronic Latin; Augustine's letter 199 in the augustinus.it Latin;
  Augustine on Psalm 84 (85) in tracked Latin and English, on Psalms 24 (25)
  and 79 (80) in tracked English; Chrysostom, Cyril of Jerusalem, Bellarmine
  and the *Catena aurea* on Mark in tracked English. English words are the
  translators', and section 3 says so wherever a translation is quoted.

## 2. Biblical contexts read

| Passage | Context read | Edition and form |
| --- | --- | --- |
| Isaiah 63:16b–17, 19b; 64:2b–7 | Isaiah 63:15–64:12 (Douay numbering); *Nova Vulgata* 63:15–65:5 | Douay–Rheims (Challoner) and Clementine (tracked verse files); *Nova Vulgata* web state of 26 November 2026; NABRE Isaiah 64 with notes (for the note on 64:2 only) |
| Psalm 80 (79) | Whole psalm | Douay–Rheims, Clementine (context stage), *Nova Vulgata*; King James Version vv. 14–17 for the Hebrew-based rendering of v. 16 |
| 1 Corinthians 1:3–9 | 1:1–10 | Douay–Rheims; Clementine (context stage) |
| Psalm 85 (84):8 and 13 | Whole psalm | *Nova Vulgata*; Douay–Rheims and Clementine at vv. 1, 8 and 13 (context stage) |
| Mark 13:33–37 | 13:28–37, with 13:1–4 for the setting through the chronology sources | Douay–Rheims; Clementine (context stage) |
| Psalm 25 (24):1–3 | Whole psalm | *Nova Vulgata*; Douay–Rheims and Clementine at vv. 1–4 (context stage) |

What the contexts settle for the readings:

- **Isaiah 63:7–64:11** is one community lament: it recalls the Exodus
  mercies (63:7–14), asks God to look down (63:15), confesses him Father where
  Abraham and Israel do not know the people (63:16), asks why he let them stray
  and harden (63:17), laments the trampled sanctuary (63:18–19a), cries for him
  to rend the heavens and come down (63:19b), remembers what he did when he
  came down before (64:1–3), confesses that he meets the one who does justice,
  that his anger and their sin go together, that their justice is a soiled rag
  and that no one calls on his name (64:4–6), and ends the reading at the
  potter and the clay (64:7). The reading omits the trampled sanctuary
  (63:18–19a) and the burning brushwood (64:1), and stops before the plea not to
  be angry and the ruined cities (64:8–11). Its whole movement is petition
  grounded in fatherhood and confession, with no answer within the passage.
- **Psalm 80** is a community lament built on a refrain (vv. 4, 8, 20) and the
  figure of the vine brought out of Egypt (vv. 9–17). The appointed strophes
  give the address to the Shepherd enthroned on the cherubim, the plea to stir
  up his might and come, the plea to look down and visit the vine, the prayer
  for the man of his right hand, the son of man, and the vow not to turn away.
  The vine's history and ruin (vv. 9–14) are not sung.
- **1 Corinthians 1:3–9** is Paul's greeting and thanksgiving before the
  rebuke of divisions that begins at v. 10. Its verbs of gift run in the past
  and present (given, enriched, confirmed); its future belongs to God's action
  (he will confirm you to the end) and the day of the Lord.
- **Mark 13:33–37** closes the discourse that begins when Jesus leaves the
  Temple and is questioned privately by four disciples on the Mount of Olives
  (13:1–4). V. 32 (no one knows the day or hour, not the angels nor the Son,
  but the Father) stands just before the reading and is not read; the reading
  begins with its consequence. Chapter 14 turns to the Passover two days later.
- **The antiphons and the acclamation** come from two laments (Psalm 25 is an
  acrostic plea for guidance and forgiveness; Psalm 85 a prayer for restored
  favour whose second half hears God speak peace).

## 3. Reception matrix

Witness roles: **carries** (a Father or saint whose reasoning at the locus
carries a reading of `interpretations.md`), **supports** (an ecclesiastical
writer or a compiled or translated witness that adds to a reading without
carrying it), **context**, **negative** (searched, nothing relevant found),
**not opened** (with reason). Standing is that of
`src/sources/inventories/author-standing-v1.toml`: Augustine, Jerome, Gregory
the Great, Bede, John Chrysostom and Cyril of Jerusalem are Fathers; Thomas
Aquinas and Robert Bellarmine are Doctors; Cassiodorus, Cornelius a Lapide and
Theophylact are ecclesiastical writers (Theophylact by the maintainer's
settlement recorded in his row).

### 3.1 Gospel — Mark 13:33–37

| Witness | Locus and form read | What it says at the locus | Role |
| --- | --- | --- | --- |
| Jerome, *Commentarii in Matthaeum* IV | On Matthew 24:36 and 24:42–43, Migne PL 26 (Paris, 1845) cols. 181–182 (Vallarsi 200–201), read on the page image of PDF p. 98 rendered from the registered Internet Archive PDF, fetched whole on 26 November 2026 and matched to its registered hash (iteration 1) | On 24:36 (col. 181): some Latin copies add *neque Filius*, which the Greek copies of Origen and Pierius lack, but since some read it, it must be discussed. *Gaudent Arius et Eunomius, quasi ignorantia magistri, gloria discipulorum sit*: the Word made all times, the day of judgment among them, so he cannot be ignorant of a part when he knows the whole; the treasures of wisdom are *hidden* in him (Col 2:3); after the resurrection he answered *Non est vestrum scire tempora* (Acts 1:7), showing that he knows *sed non expediat nosse apostolis, ut semper incerti de adventu Judicis, sic quotidie vivant, quasi die alia judicandi sint*; in the Father he includes the Son. On 24:42–43 (col. 182): *Perspicue ostendit quare supra dixerit: De die autem illa… nemo scit… quod non expediat scire apostolis, ut pendulae exspectationis incerto semper eum credant esse venturum, quem ignorant quando venturus sit. Et non dixit, quia nescimus qua hora venturus sit Dominus; sed nescitis*; the householder's example then shows more plainly why he keeps the day of the consummation silent | carries Reading 2 (parallel Gospel: Jerome comments on Matthew 24; Bede transmits the two comments on Mark 13:32–33) |
| Bede, *In Marci evangelium expositio* | On Mark 13:32–37, tracked Latin (Wikisource transcription from Migne; the transcription's own section marks only), physical lines 402–405, the lemmata *De die autem illo*, *Videte, vigilate*, *Vigilate ergo*, *Quod autem vobis dico* | **Transmitted, not his own.** His comment on 13:32 (line 402) is Jerome's on Matthew 24:36 nearly word for word (Bede omits Jerome's remark on *neque Filius*, which Mark reads, and has *die illa* where the Migne Jerome has *die alia*); his comment on 13:33–34 (line 403), the day withheld *ut pendulae exspectationis incerto…* and the remark that he said not *we* but *you* do not know, is Jerome's on Matthew 24:42–43. On the man gone abroad (line 404) the identification with Christ ascended is also Gregory's (Hom. 9.1), and the sentence *Carnis enim locus proprie terra est…* is Gregory's; the triad *Vigilat qui…* (line 405) is Gregory's (Hom. 13.3). **His own, as far as checked:** Christ left the Church in bodily presence and never without the protection of his divine presence, abiding with it to the consummation; he gave his servants power over every work by giving them the grace of the Holy Spirit to serve in good works; the porter is the order of pastors and spiritual rulers, charged with the care of the Church entrusted to them (line 404). On 13:37: not only the apostles and their successors, the rulers of the Church, but all are commanded to watch, to guard the doors of their hearts lest the old enemy break in by evil suggestion; each must take care lest the Lord find him sleeping, for each will give account to God for himself (line 405), with Rom 13:11 and 1 Cor 15:34 | carries Reading 2 for Mark 13:34–37 (his own allotment of the watch); transmitter only for 13:32–33 |
| Gregory the Great, *Homiliae in Evangelia* | Hom. 13 (Luke 12:35–40) §§1–6 read whole, tracked Latin (Wikisource); Hom. 9 (Matthew 25:14–30) §1 for the sentence Bede borrows | Hom. 13: the Lord went to the wedding when he ascended and returns when he is shown to us in judgment (§2); he comes in judgment and knocks when sickness signals death; the one who is secure in hope and work opens at once (§3); the *vigilat qui…* triad, verbatim the source of Bede's (§3); the watches are childhood, youth and old age, so that no one should despair (§5); the last hour is hidden so that it may always be suspected and we be ready for it without interruption (§6). Hom. 9 (Matthew 25:14–30): *Carnis enim locus proprius terra est…*, the sentence on Christ's journey abroad that Bede reuses | carries Reading 2 (parallel Gospel: Gregory comments on Luke 12, not on Mark 13) |
| Augustine, *Epistula* 199 (to Hesychius) | 199.1.2–1.3 (nn. 2–3), augustinus.it Latin, fetched whole and matched to its registered hash | Ignorance of the times differs from a corrupt life; Paul would not have the Thessalonians believe rumours that the day was near, nor say with the bad servant *my master delays*. Whatever day finds each one as his last finds him so in the last day of the world, for as each dies in that day, so will he be judged in that day. On Mark 13:35–37 he asks to whom *all* is said: to the elect who belong to the body of Christ, the Church, those then present, those after them, us and those after us until his last coming; the day will not find all alive, so the command belongs to all because the day comes to each when he leaves this life such as he will be judged; therefore every Christian must watch | carries Reading 2 |
| John Chrysostom, Homily 77 on Matthew | §§2–3 on Matthew 24:42–44, tracked English (CCEL, NPNF 1.10, physical lines 43022–43050) | The translator's English: he said not *I know not* but *ye know not*; he does not tell them in order that they may watch and be always ready and continually in virtuous action; if men knew when they were to die they would strive only at that hour | carries Reading 2 (parallel Gospel, Matthew 24) |
| Thomas Aquinas, *Catena aurea in Marcum* | Mark 13:32–37, tracked English (Oxford 1842, Dalgairns), passage record verified 2026-11-24 | Compiles Theophylact (the hour hidden because if we knew it we would stay in wickedness to the end; *not I know not but ye know not*; the four watches as old age, youth, the age of reason and childhood), Hilary (*De Trinitate* IX: the Son's not knowing is an economy of silence, not ignorance), Pseudo-Jerome, Bede (the man abroad), Gregory (attributed "Hom. in Evan. 9" for the journey sentence and, with no new heading, for the servants' power, the porter and the doors of the heart, which the tracked Gregory does not contain: a search of the whole *Homiliae in Evangelia* Latin for *janitor*, *januas cordium* and *ordini pastorum* returned nothing, so those sentences are Bede's), and Augustine *Ep.* 199.3. The *Catena* does not excerpt Bede's comments on 13:32–33, the ones taken from Jerome | supports Reading 2 (a compilation; each excerpt is credited to its own author) |
| Theophylact, *Enarratio in Evangelium Marci* | Through the *Catena* only | As above | supports (ecclesiastical writer) |
| Cornelius a Lapide, *Commentaria in quatuor Evangelia* | Held: the tracked English OCR (Mossman, 1908), volume 3 (Matthew 22–28 and Mark 1–16), artifact `…1908-grant-mossman.volume-3-ocr-b001cf78`, which `discover` reports as containing the passage; its Mark chapter XIII (physical lines 21731–21760) read at iteration 2 | Lapide comments on Mark 13 only at vv. 6 and 11; there is nothing on 13:33–37. The chapter's printed argument (its opening summary) mentions the watch "when he cometh to each one, particularly by death", but that is the edition's summary, not a comment, and is not relied on. The same volume holds his commentary on the Matthew 24 parallel (chapter XXIV from physical line 2920), which was not read | ecclesiastical writer, support only; nothing used |
| Albert the Great, Hugh of Saint-Cher, Nicholas of Lyra, Denis the Carthusian | discover lists them; they are not held at this locus or not held at all | — | not opened (no held text at the locus) |

**Difficulty.** The reading begins after v. 32. Its two hard points are why the
hour is hidden and to whom *what I say to you I say to all* is said, when most
who hear it die before the end. Jerome and Chrysostom, both on Matthew 24,
answer the first: it is hidden for our good, so that readiness is continuous
(Jerome: *ut pendulae exspectationis incerto semper eum credant esse
venturum*), and the Lord said *you* do not know, not *we* do not know, so that
the ignorance is the disciples' and not his. Chrysostom makes the same remark
in his own homily on Matthew 24:42 (*He said not, "I know not," but, "ye know
not"*). Bede carries Jerome's two comments over to Mark 13:32–33 without
naming him; they are cited as Jerome's, with Bede as the one who applied them
to Mark. Augustine answers
the second: *all* is the whole Church through time, and the day of each one's
death is, for him, the form in which the last day comes. Gregory joins the two
(the knock at sickness; the hour hidden so that it is always suspected).
Augustine's answer moves the command from the end of history into each life;
Bede's own comment on 13:34–37 keeps it at the Lord's return and distributes
it by office (porter, servants, all). The two are compatible and do not say
the same thing.

### 3.2 Second reading — 1 Corinthians 1:3–9

| Witness | Locus and form read | What it says | Role |
| --- | --- | --- | --- |
| John Chrysostom, Homily 2 on 1 Corinthians | §§4–8 on 1:7–9, tracked English (CCEL, NPNF 1.12, physical lines 727–851; registered at source registration as the verified passage `…ccel-web-2026-09-28.2.1cor-1.7-9`); the New Advent page was also fetched (state differs from the earlier registered one; the state read is now registered) and agrees | The translator's English: on 1:7, why are you troubled that Christ has not come? the Day is at the doors; *revelation* means that he is present now though not seen, and will appear; there is need of patience. On 1:8, *will confirm* and *unreprovable* mark them as still wavering. On 1:9, God is faithful, i.e. true; what he has promised he will perform; he has called them to fellowship with the only-begotten; Paul puts this early lest after the rebukes they despair; unbelief comes not from him who calls but from those who start away | carries Readings 2 and 3 |
| Thomas Aquinas, *Super I ad Corinthios* | c. 1, lect. 1 (no. [86234] of the Corpus Thomisticum text), Latin, fetched whole and matched to its registered hash | The present gifts are of grace; the future good is awaited: Christ's revelation, which makes men blessed in reality, and those who wait for it are blessed in hope (Is 30:18). The waiting is not vain: Christ *confirmabit* in the grace received *usque in finem*, scilicet *vitae vestrae*; not that they be without sin (1 Jn 1:8) but *sine crimine*, without mortal sin, *quia qui sine crimine invenitur in die mortis, sine crimine perveniet ad diem iudicii* (Eccles 11:3). The ground is *Deus fidelis*: God would not seem faithful if he called us to his Son's fellowship and denied us, as far as lies in him, the means to reach it. That fellowship is had *in praesenti per similitudinem gratiae* (1 Jn 1:7) and *in futuro per participationem gloriae* (Rom 8:17) | carries Readings 2 and 3 |
| Cornelius a Lapide | 1 Cor 1:5 and 1:7, held tracked fragments (`…commentaria-in-omnes-divi-pauli-epistolas.1908-grant-cobb.1cor-1-5`, `…1cor-1-7`) | Listed by discover; not read at this stage | lead (not read) |
| Theodoret, Theophylact, Peter Lombard, Rabanus, Origen fragments, Denis, Lyra, Hugh | discover | Theodoret and Theophylact are held only inside containers whose extent does not include 1 Corinthians at a read locus | not opened |

**Difficulty.** Paul thanks God that the Corinthians lack no gift, and the
letter goes on to rebuke them as carnal. Chrysostom faces it directly: either
they became remiss after receiving the gifts, or the praise is said of the
part for the whole, and the praise belongs to God's grace, not to them; *will
confirm* and *unreprovable* already imply that they waver. Aquinas assigns the
perfection to the Church as a body (Augustine on John: what another has in the
unity you have). Both make the thanksgiving rest on God's fidelity, not on the
Corinthians' state.

### 3.3 First reading — Isaiah 63:16b–17, 19b; 64:2b–7

| Witness | Locus and form read | What it says | Role |
| --- | --- | --- | --- |
| Jerome, *Commentarii in Isaiam* XVII | Migne PL 24 (Paris, 1865) cols. 641–650, on 63:15–64:8 (Vulgate numbering), read on page images rendered from the Internet Archive PDF (PDF pp. 325–329), fetched whole and matched to its registered hash; the tracked OCR was too poor to read | The whole chapter is the prayer of a people mixed of just and sinners (col. 643). On 63:17: the lemma gives the verse from the Hebrew and from the Septuagint, and both of Jerome's Latin renderings read *convertere propter servos tuos*, the Septuagint adding *ut modicum possideamus montis sancti tui* (col. 642). Not that God is the cause of error and hardness, but that his patience, waiting for our salvation and not at once correcting sinners, seems a cause; Pharaoh, Romans 9, the physician who hides the knife (cols. 643–644). He reads the petition two ways: *Convertere, ait, Domine, sive converte nos propter servos tuos*, "turn, Lord, or turn us"; the second he develops with the Septuagint's clause, *Sive converte nos, ut, juxta Septuaginta, paululum possideamus montis sancti tui*, so that, having a part, we may come to its fullness and contemplate the glory of the Only-begotten, full of grace and truth (cols. 643–644; re-read on the page image at iteration 2). On 64:1 (Hebrew 63:19b): *Utinam disrumperes caelos, et descenderes; et qui semper promitteris, tu aliquando promissa compleres*; this was said before the Saviour came and took our nature from the Virgin's womb (col. 645); the mountains are adverse powers. On 64:3 (Hebrew 64:2): *Pulchreque juxta Hebraicum, quasi exauditi essent…* after the prayer *Utinam disrumperes… descenderes* they say *Descendisti*, the Word made flesh, Emmanuel (col. 646). On 64:4: Paul (1 Cor 2:9) gives the sense of this verse from the authentic books, not from apocrypha (cols. 646–647). On 64:5 (Hebrew 64:4): *Ordo praeposterus. Non quia tu iratus es, nos peccavimus; sed quia nos peccavimus, tu iratus es*; and according to the Hebrew, we who were always in sins shall be saved by your mercy alone (col. 647). On 64:7–8: no one calls on your name; God having turned his face away, we shall say *Ostende faciem tuam, et salvi erimus* (Ps 79:4), that we may be servants not of sin but his (col. 649); if we consider our merits we must despair; if your clemency, we dare to pray, for you are our Father; though we are clay, and the vessel may not answer the potter, knowing we are sons we dare to say *Ne irascaris, Domine, satis* (cols. 648–650) | carries Readings 1 and 3 |
| Thomas Aquinas, *Expositio super Isaiam ad litteram* | c. 63 end ([85023]) and c. 64 ([85024]), Corpus Thomisticum Latin, fetched whole and matched to its registered hash | On 63:17: *fecisti* errare, *permittendo, non immittens gratiam, et non corrigens*; *indurasti, permisisti* (Rom 9). On 63:17b, the petition for mercy: *convertere, de ira ad misericordiam, propter servos, patres nostros*, with Psalm 89:13 *convertere, domine, usquequo…* and Lamentations 5:21 *converte nos, domine et convertemur* adduced together ([85023]). On 64:1 *dirumperes*: figurative, as to one dwelling above the heavens, *vel exinanires temetipsum, despiciens majestatem, et carnem assumeres* (Ps 143:5). On *Descendisti*: three readings: *ad judicandum nos: praeteritum pro futuro*; *vel in uterum virginis*; *vel melius, secundum litteralem sensum*, a proof from the past: if you came down now, these things would happen as they did when you came down to free your people from Egypt (Exod; Ps 17:10). On 64:5 *occurristi laetanti*: in help, while he was still asking or coming to you; *mystice Simeoni* (Luke 2). *Ecce tu iratus, et peccavimus: praeposterus ordo: ideo iratus, quia peccavimus: et tamen salvabimur, tua misericordia*. On 64:8: *pater noster es tu*, clay in the potter's hand (Jer 18; Job 10) | carries Readings 1 and 3 |
| Cyril of Alexandria, Theodoret, Albert, Hugh, Lyra, Denis, Lapide | discover | Cyril of Alexandria and Theodoret on Isaiah are not held; Hugh is held only as restricted whole-Bible artifacts, not read; Lapide on Isaiah is not held | not opened |

**Jerome's polemical passage.** At cols. 644 and 647 Jerome applies the trampled
sanctuary (63:18, omitted from the reading) and the soiled justice of 64:5 to
the Jewish people after the Passion in terms of permanent curse and of the
law's ceremonies. Those sentences rest on omitted verses or on a reading the
studies do not need; they are not used, and no reading of `interpretations.md`
relies on them (section 7).

**Difficulty.** Two textual hard points bear on meaning. (1) **The answered
cry.** After *Utinam dirumperes caelos et descenderes* (63:19b), the *Ordo*'s
Latin goes on with *Descendisti* (64:2b). Jerome hears the prayer answered in
the Incarnation; Aquinas gives three readings and prefers, as the literal
sense, the memory of the Exodus descent, with the Incarnation and the judgment
as further readings. In the United States text *Descendisti* is not heard
(`propers/verified.md` finding 1), so the answer Jerome hears is present in
the Latin edition's reading and absent from the English proclamation. (2)
**Hardening and the order of sin and anger** (63:17; 64:4 Hebrew). Both
Jerome and Aquinas refuse to make God the author of the people's straying
(patience that seems a cause; permission, withholding of grace), and both call
the order *you were angry, and we sinned* inverted (*praeposterus*): the anger
follows the sin. These hard words are in the Latin (*errare nos fecisti*;
*ecce tu iratus es, et peccavimus*) and the Douay ("made us to err"). The
United States text the assembly hears differs at both points (readings page,
state `7e0b44c0…`, read again at iteration 1): at 63:17 it asks why God *lets*
the people wander, a permissive rendering, and at 64:4 it states God's anger
and the people's sinfulness side by side, both in the present, where the
*Nova Vulgata* has *peccavimus*, "we sinned", after the anger. The
permissive rendering already takes the line of Aquinas's *permittendo*, so a
study should not describe to hearers words they do not hear; it can still
teach the difficulty Jerome and Aquinas address, saying that it stands in the
Latin.

**Psalm and reading: two petitions to turn, joined by the witnesses**
(iterations 1–2). *The texts.* The refrain (Psalm 80 (79):4, *Deus, converte
nos*) asks God to turn his people; in the Hebrew-based Latin, Isaiah 63:17b
(*Convertere propter servos tuos*) asks God himself to turn, that is, to
return. The appointed psalm has Isaiah's imperative at v. 15 (*Deus virtutum,
convertere*), not in its refrain; in the United States psalm that imperative
is rendered adverbially and the verb is not heard. *The witnesses.* Neither
witness read here keeps the two petitions apart. Jerome, on 63:17 itself,
reads *Convertere, ait, Domine, sive converte nos propter servos tuos*: "turn,
Lord" or "turn us". He develops the second reading with the Septuagint's
added clause (*Sive converte nos, ut, juxta Septuaginta, paululum possideamus
montis sancti tui*), and carries it to the contemplation of the glory of the
Only-begotten (PL 24 cols. 643–644, page image). His lemma (col. 642) renders
both the Hebrew and the Septuagint with *convertere*, so the "turn us" is his
reading of the petition, not a different verb in either text. Jerome also
ties the refrain to the reading by quoting it, through the hidden face: on Isaiah
64:7 (Vulgate; Lectionary 64:6) he answers God's turning away of his face with
Psalm 79:4, *Ostende faciem tuam, et salvi erimus* (cols. 648–649, page
image). Aquinas, commenting on the Vulgate, glosses Isaiah's *convertere* as *de
ira ad misericordiam* and adduces, under that one petition for mercy, Psalm
89:13 *convertere, domine* and Lamentations 5:21 *converte nos, domine et
convertemur* together ([85023]); on 64:6–7 he reads the hidden face as God's
mercy withheld ([85024]). Neither quotes the refrain at 63:17. A study may
therefore say that Jerome reads Isaiah's *convertere* also as *converte
nos*, the refrain's own words, and that Aquinas sets God's turning and his turning of us side
by side; it must not say that the Hebrew, the *Nova Vulgata* or the United
States reading has "turn us" at 63:17. The Greek of the Septuagint was not
read; the record rests on Jerome's Latin of it. `propers/verified.md`
(Relationship classes) records the correction.

### 3.4 Responsorial psalm — Psalm 80 (79)

| Witness | Locus and form read | What it says | Role |
| --- | --- | --- | --- |
| Augustine, *Enarrationes in Psalmos* 79 | §§1–3, 9, 11, tracked English (Oxford translation in NPNF 1.8, CCEL, physical lines 39604–39989); the translation is abridged where it prints "…" | §1: the song is of the Advent of the Lord and of his vineyard; it confesses Christ and the vineyard, head and body. §2: He is invoked to come, expected until he come, longed for until he come; *stir up thy power and come*, read of the Crucified who rises in power. §3: *O God, convert us*: we were turned away, and unless you convert us we shall not be converted; *illumine thy face*: he placed before it a cloud of flesh. §9: *perfect this vineyard… and upon the Son of man*, Christ, the foundation (1 Cor 3:11). §11: *thou wilt quicken us*, we who were dead loving earth; *thy name we will invoke*, that is, we will love thee | carries Readings 1 and 3 |
| Robert Bellarmine, *Explanatio in Psalmos* 79 | Explanations 1–3 and 14–18, tracked English (O'Sullivan), passage records verified | Expl. 3: God does not look on us because we turn away; we cannot turn to him without his aid, so the prophet asks for both. Expl. 14–15: *turn again… visit this vineyard*, a prayer that foretells Christ's coming; *and upon the Son of man*: "all agree that this passage refers literally to Christ". Expl. 17: the man of the right hand is Christ | carries Readings 1 and 3 |
| Cassiodorus, Theodoret, Athanasius, Albert, Hugh, Jerome (*Commentarioli*, *Tractatus*), Lombard, Lyra, Denis | discover | Cassiodorus is held in many artifacts but no locus for Psalm 79 was read at this stage; Theodoret and Athanasius in Greek containers not read | not opened (Cassiodorus a named gap, section 10) |

**Difficulty.** V. 16b: the *Nova Vulgata*, the Clementine and the
Douay–Rheims have *son of man* at v. 16 as at v. 18; the King James Version,
from the Hebrew, has *branch* at v. 16 (`propers/verified.md` finding 2). The
United States text names the son of man in the second strophe. Augustine and
Bellarmine read the son of man as Christ; Bellarmine says the agreement is
general. Because the Hebrew of v. 16b was not read, the studies say only that
the Latin tradition and the United States text have *son of man* there and
that a Hebrew-based version has *branch*.

### 3.5 Alleluia verse and Communion antiphon — Psalm 85 (84):8 and 13

| Witness | Locus and form read | What it says | Role |
| --- | --- | --- | --- |
| Augustine, *Enarrationes in Psalmos* 84 | Latin 84.9 and 84.15, tracked (Wikisource from Migne), passage records verified; English §§6 and 12 of the Oxford translation (physical lines 41616–41672, 41844–41871) | On v. 8: *Hoc est quod cantavimus* (this is what we sang); *salutare tuum, Christum tuum*; the one to whom God shows his mercy cannot be proud, for he is persuaded that whatever good he has he has only from God. On v. 13 (his psalter: *Etenim Dominus dabit suavitatem*): truth springs from the earth when the sinner confesses; justification is given from heaven; *Tua ergo peccata potes habere; fructum bonum non habebis, nisi ille dederit cui confiteris*; God gives the sweetness of doing justice so that justice delights where iniquity delighted; the preacher sows, but unless God rains, the land gives no fruit | carries Reading 3 (and Reading 1 on v. 8) |
| Robert Bellarmine, *Explanatio in Psalmos* 84 | Explanations 7 and 12 (with 10–11 for context), tracked English, passage records verified | Expl. 7: *show us thy mercy… grant us thy salvation*: send us your Son for a Saviour; he reports Augustine's moral reading. Expl. 12: the land never ploughed nor sown yields its fruit: the Spirit overshadows the Virgin; Christ is the flower of the field | carries Reading 1 |
| Cassiodorus, Theodoret, Athanasius, Jerome (*Tractatus*), Bede (*In Psalmorum librum*), Lapide, Aquinas (*Super Psalmos* stops before Ps 84), Strabo, Lombard, Lyra, Denis, Albert, Hugh | discover | Not read at this stage | not opened |

Augustine's *Hoc est quod cantavimus* shows that v. 8 was sung in his church
before he preached on it; it says nothing about the Roman Alleluia verse.

### 3.6 Entrance antiphon — Psalm 25 (24):1–3, adapted

| Witness | Locus and form read | What it says | Role |
| --- | --- | --- | --- |
| Augustine, *Enarrationes in Psalmos* 24 | §§1–5, tracked English (NPNF 1.8, physical lines 6850–6883; passage records `…first-thirty.24.1-2`, `…24.3`, `…24.4` and `…24.5` verified) | Christ speaks in the person of the Church, the Christian people turned to God; the soul trodden down by carnal longing is lifted with spiritual longing; trusting in himself he fell, trusting in God he will not be ashamed; on v. 5, dismissed from Paradise he cannot return unless God meets the wanderer | carries Reading 2 (support) and Reading 3 |
| Robert Bellarmine, *Explanatio in Psalmos* 24 | Explanations 1–3, tracked English, verified | To wait on the Lord is to expect him in the certain hope of help; those who wait were never disappointed | supports |

The antiphon's *qui te exspectant* is not the *Nova Vulgata*'s or the
Clementine's wording (owner finding 5); the studies should not present the
waiting of the antiphon as the psalm's Latin.

### 3.7 The orations, the Preface and the blessing

Read in the Latin of the 2002 Missal (owner). Their early witnesses, found at
this stage (owner findings 6–8):

| Text | Witness read | What agrees | Bound |
| --- | --- | --- | --- |
| Collect | Old Gelasian, Wilson p. 218, page image: Postcommunion of the fourth Advent *Missa* (II.LXXXIII) | The petition for the will to go out with just works to meet Christ coming, and the closing clause, nearly word for word | The Gelasian prayer is a prayer after Communion, addressed to *cunctae familiae tuae*; Wilson's note names other books not read |
| Prayer over the Offerings | Verona, Feltoe p. 74, no. 372, *Mense Iulio*, page image | Whole prayer; *temporalis* for *temporali* | A July Mass of the Verona collection, not Advent |
| Prayer after Communion | Verona, Feltoe p. 134 (September) and p. 20 (*Preces in Ascensa Domini*), page images | The opening from one prayer, the close (*inter praetereuntia… iam nunc inhaerere mansuris*) from another | Neither context is Advent; no single antecedent found |
| Preface I of Advent | Verona, Feltoe p. 20, *Preces in Ascensa Domini*, page image | *secundo… adventu manifesto munere capiamus quod nunc audemus… promissum*; Verona *sperare*, the Preface *vigilantes… exspectare* | An Ascension prayer; the first half of the embolism was not found |
| Solemn blessing | not searched | — | named gap |

These are textual observations. They show that the Missal's Advent orations
and Preface reuse older Roman prayers, two of them from non-Advent contexts;
they do not show what the compilers intended. Any study sentence of the form
"the Church chose this prayer because…" would be an editorial claim and must
be labelled so.

### 3.8 The Preface's two comings: patristic witness

| Witness | Locus and form read | What it says | Role |
| --- | --- | --- | --- |
| Cyril of Jerusalem, *Catecheses* 15.1 | Tracked English (Gifford, NPNF 2.7, 1894), passage record verified | The translator's English: "We preach not one advent only of Christ, but a second also, far more glorious than the former"; his descents are twofold, the unobserved like rain on a fleece and the open coming to be; we rest not on the first only but look also for the second | carries Reading 1 |

### 3.9 Liturgical commentators

The `formulary` command found no held commentator locus on this Mass (40 loci,
none listed). No commentator was read for this formulary, and none is cited.
This is a bounded negative result: the index covers the commentators the
library holds, not every commentary on the Advent liturgy.

### 3.10 The ritual book

The *Book of Blessings* order for an Advent wreath was read in a third-party
transcription (`propers/verified.md`, Branches). It reuses Isaiah 63:16–17, 19;
64:2–7 among its readings outside Mass. It is not a commentary.

## 4. Named corpora not opened

- Cassiodorus on Psalms 24, 79 and 84 (held; no locus read in time).
- Cyril of Alexandria and Theodoret on Isaiah; Theodoret and Athanasius on the
  Psalms (Greek containers, not read).
- Lapide on 1 Corinthians 1:5 and 1:7 (held fragments, not read); Lapide on
  Isaiah (not held at the locus). Lapide on Mark is held and was checked at
  iteration 2: at Mark 13 he comments only on vv. 6 and 11 (section 3.1). His
  commentary on Matthew 24, in the same held volume, was not read.
- Albert, Hugh of Saint-Cher, Nicholas of Lyra, Denis the Carthusian, Peter
  Lombard, Rabanus Maurus, Walafrid Strabo on every passage: listed by
  discover, not held at the loci or held only in restricted whole-work
  artifacts not read.
- Bernard of Clairvaux's Advent sermons and Leo the Great's Advent (December
  fast) sermons: held works in the library, not read. Whether either comments
  on these passages was not checked.
- Jerome's DCO Latin text of *In Isaiam* (Pars 4, registered `…pars-4-pdf-97785e2b`):
  the site's TLS certificate had expired on 26 November 2026 (curl error 60);
  the registered Migne page images were read instead.

## 5. Sources read outside the library, and retrievals

All were fetched on 26 November 2026 over verified TLS, whole, and hashed.
None is retained in the repository by this stage; the receipts are held for
the source-registration stage. That stage re-hashed every receipt, registered
the deliveries marked *registered* below as restricted artifacts (identity and
hash only, no bytes retained), and left the two that are not the source
unregistered (section 11).

| Source | URL | Bytes | SHA-256 | Library relation |
| --- | --- | ---: | --- | --- |
| *Nova Vulgata*, *Liber Isaiae* | `https://www.vatican.va/archive/bible/nova_vulgata/documents/nova-vulgata_vt_isaiae_lt.html` | 204,149 | `9c9c78c444de0e449240afdddcb1e4f9839fa11327034d50f4a0f68bb4d68a85` | registered: `…nova-vulgata.vatican-official-web.liber-isaiae-9c9c78c4` |
| *Nova Vulgata*, *Liber Psalmorum* | `https://www.vatican.va/archive/bible/nova_vulgata/documents/nova-vulgata_vt_psalmorum_lt.html` | 269,126 | `e508ed1c4add8cd5f6962fcfaa6c70848023553307eb95ba1d9b62ed3575fb42` | byte-identical to the registered state |
| NABRE Isaiah 64 (USCCB) | `https://bible.usccb.org/bible/isaiah/64` | 58,899 | `35573e1b45418b88dda799e9c5aa85dd138edc246204d7dd370d173421d05455` | registered: `…new-american-bible-revised-edition.english-usccb-web-2026-11-26.isaiah-64-35573e1b` |
| NABRE Isaiah 63 (USCCB) | `https://bible.usccb.org/bible/isaiah/63` | 15,748 | `bc18b9070f08182a9347a4b57bd2ff7c8ff6da30ae608bf47e32afcd3822feeb` | HTTP 403 challenge page; nothing read; not registered (not the source) |
| Migne PL 24 (Internet Archive PDF) | `https://archive.org/download/sanctieusebiihie04jero/sanctieusebiihie04jero.pdf` | 67,109,688 | `e55e8bd27f2609985fe45f25ffe65333378fb55f24e7bb3bd804701c2a437c44` | matches registered remote artifact |
| Migne PL 26 (Internet Archive PDF; iteration 1) | `https://archive.org/download/patrologiaecurs240unkngoog/patrologiaecurs240unkngoog.pdf` | 63,426,233 | `0d889bd6856adae5240b240a56a3717f278d1abf5aad26b03c53fe686a0245e4` | matches registered remote artifact `…patrologia-latina-volume-26.paris-1845.internet-archive-google-pdf-0d889bd6`; PDF p. 98 (cols. 181–182) read on its page image; no text layer |
| Aquinas, *Super Isaiam* 50–66 (Corpus Thomisticum) | registered URL | 151,512 | `5300798b1f6652de2630e6e2fdab15d9b3b64ead517c44bf12b4c02163494f3a` | matches registered |
| Aquinas, *Super I Cor.* c. 1 (Corpus Thomisticum) | registered URL | 277,757 | `8be5b71c1f1d4660117dd4ed0f7716c085b63d66e820e15416aaad04ca2a8c7c` | matches registered |
| Augustine, *Ep.* 199 (augustinus.it) | registered URL | 88,756 | `5b570f96ac561d51c425172fcad0c906a285e7c2a308b89b30b300eee61c0dea` | matches registered |
| Feltoe, Verona sacramentary (Internet Archive PDF) | `https://archive.org/download/sacramentariumle00cath/sacramentariumle00cath.pdf` | 19,868,448 | `3b991b133889bbd4803831455bb4f49de30ecb4d8386534cee1f80f79541967a` | matches the registered tracked artifact, whose payload is absent from this checkout |
| Wilson, Old Gelasian (Internet Archive PDF) | `https://archive.org/download/LiberSacramentorumRomanaeEcclesiae/LiberSacramentorumRomanaeEcclesiae.pdf` | 13,625,474 | `006a38a39250d39c9745acfb4f4a098374027e719dc7ad7e32972fa6a82489bc` | matches registered remote artifact |
| *Book of Blessings*, Advent wreath (Catholic Culture transcription) | the registered artifact's URL | 58,627 | `25cf5943ac298899bd7384c72c0a4ceab186165a8dfb709ca208ec05cc3cc3a8` | differs from the registered state `…6be75b4e`; registered as its own state: `…2026-11-26-catholic-culture-1989-us-transcription.advent-wreath-html-25cf5943` |
| New Advent: Chrysostom, Hom. 1 on 1 Corinthians | `https://www.newadvent.org/fathers/220101.htm` | 33,688 | `73b75a828cab59d64e4fc86a6c68757d5e2264aa409784f99aec173c6505c5d9` | cross-check of the tracked CCEL text relied on; registered: `…homilies-on-first-corinthians.2026-11-26-new-advent.homily-1-73b75a82` |
| New Advent: Chrysostom, Hom. 2 on 1 Corinthians | `https://www.newadvent.org/fathers/220102.htm` | 40,114 | `3cdc75f90b5c6706f257a90c35f78b93e492a9da11515fbaf50f23d71ebe0c09` | cross-check of the tracked CCEL text relied on; registered: `…homilies-on-first-corinthians.2026-11-26-new-advent.homily-2-3cdc75f9` |
| New Advent: Chrysostom, Hom. 77 on Matthew | `https://www.newadvent.org/fathers/200177.htm` | 55,982 | `1f1f259214fb92230b2f3a98c3484ab0e3005e54556c8e70af361095251b08b2` | cross-check of the tracked CCEL text relied on; registered: `…homiliae-in-matthaeum.2026-11-26-new-advent.homily-77-1f1f2592` |
| New Advent: Augustine, *En. in Ps.* 24 (New Advent 'Psalm 25') | `https://www.newadvent.org/fathers/1801025.htm` | 23,980 | `68692606879b64f3c944ba20940076e3ff55ff877520698b6534bbcf886edf8d` | cross-check of the tracked CCEL text relied on; registered: `…enarrationes-in-psalmos.2026-11-26-new-advent.psalm-25-68692606` |
| New Advent: Augustine, *En. in Ps.* 79 (New Advent 'Psalm 80') | `https://www.newadvent.org/fathers/1801080.htm` | 41,126 | `4fde8c1de01dc929a6c61c54d292418573efe5845e2f3040e9b61c8e04c9615a` | cross-check of the tracked CCEL text relied on; registered: `…enarrationes-in-psalmos.2026-11-26-new-advent.psalm-80-4fde8c1d` |
| New Advent: Augustine, *En. in Ps.* 84 (New Advent 'Psalm 85') | `https://www.newadvent.org/fathers/1801085.htm` | 45,795 | `4f2451c80a330d62637be15b7fa50a1622036516305b3589feb0556bed3f0f18` | cross-check of the tracked CCEL text relied on; registered: `…enarrationes-in-psalmos.2026-11-26-new-advent.psalm-85-4f2451c8` |
| New Advent: Cyril of Jerusalem, *Catechesis* 15 | `https://www.newadvent.org/fathers/310115.htm` | 73,172 | `c51f9a4c717db926df67756df7388b53d580a4e84f256bafb39b044bbc0dec0d` | cross-check of the tracked text of section 1 relied on; registered: `…catechetical-lectures.2026-11-26-new-advent.lecture-15-c51f9a4c` |
| Augustine, *En. in Ps.* 24 (augustinus.it) | the registered artifact's URL | 4,608 | `e908b6d04072e053edfe49744b01e81f1fd7fd3b9a31805658aea218586795be` | not the page; nothing read; not registered (not the source) |

## 6. Negative results and their limits

- **Liturgical commentators.** None held for this formulary (section 3.9).
- **Collect.** No antecedent beyond the Gelasian was searched; the other books
  Wilson names were not read.
- **Prayer after Communion.** No single antecedent in the Verona or Gelasian
  text layers (searched for *frequentata mysteria*, *praetereuntia* and
  *inhaerere mansuris*); the Gregorian was not searched.
- **Preface.** The first half of the embolism (*primo adventu in humilitate
  carnis assumptae…*) was not found in the Verona text layer; other books not
  searched.
- **No Father read here comments on this Mass.** Every author is credited only
  with what he says of his own passage.

## 7. Material disagreement and complementary difference

- **Descendisti (Isaiah 64:2b).** Jerome: the Incarnation, as the prayer
  heard. Aquinas: three senses, the literal preferred being the Exodus memory.
  A real difference about the literal sense, which both admit can bear the
  Christological reading. Reading 1 keeps both and says which is literal for
  whom.
- **The hidden hour.** Jerome and Chrysostom, on Matthew 24 (concealed for our
  readiness; *you*, not *we*, do not know), and Augustine (the command
  fulfilled in each one's last day) are complementary. Bede repeats Jerome's
  answer on Mark 13:32–33 and is its transmitter, not its author.
  Gregory's three watches as ages (Luke 12) and Theophylact's four watches as
  ages (Mark 13, through the *Catena*) are different allegories of different
  texts and are not merged.
- **Jerome's polemic** (cols. 644, 647) is not adopted. It concerns omitted
  verses and claims about the Jewish people that the studies have no need to
  repeat; the profiles' rule on presenting other peoples applies.
- **Bede's sources.** Bede's comments on Mark 13:32 and 13:33–34 are Jerome's
  on Matthew 24:36 and 24:42–43 (PL 26 cols. 181–182); his identification of
  the man abroad, his sentence on the journey and his *vigilat qui…* are
  Gregory's (Hom. 9.1 and Hom. 13.3). Each is credited to its author, at his
  own work and on the Gospel he expounds, with Bede named as the one who
  carried it to Mark 13. Bede is cited in his own right for what no checked
  source supplies: the servants' power as the Spirit's grace for good works,
  the porter as the order of pastors, the command to all to guard the doors of
  their hearts, and each one's account for himself (Mark 13:34–37).

## 8. Chronology

### 8.1 Inputs and answers

`research/chronology-inputs.toml` was written from this leaf's verified
citations; Missal elements are owned by the shared owner, Lectionary elements
by this leaf. `tools/tpt proper-chronology record --write` and `annotations
--presentation orientation-v3 --write` generated `chronology.toml`,
`chronology-annotations.tex` and `chronology-table.tex`. At iteration 1, after
`propers/verified.md` was corrected, `record --write` and `annotations
--presentation orientation-v3 --write` were run again; the only change in the
record and the annotations is the fingerprint of `propers/verified.md`, the
table is unchanged, and the record and annotations `--check` runs and a
`--format table-tex` comparison of the table pass. Inspected answers:

| Element | Answer (display) | Inspection |
| --- | --- | --- |
| Entrance antiphon (Psalm 24) | Traditional attribution, disputed: David's reign, c. 1055–1015 B.C.; historical setting: occasion date unresolved; composition: before c. 165 B.C. | The psalm's title names David; no occasion is identified by any witness read; the unresolved row is honest |
| First reading | Traditional attribution: Isaias, B.C. 740–701 (Souvay); composition: oracles of Isaiah 56–66, after the exile | Two answers, not two dates for one thing. The Passage cell prints the Clementine/Douay numbering, *Is. 63:16b–17; 64:1, 3–8* (section 8.3) |
| Responsorial psalm (Psalm 79) | Historical setting: occasion date unresolved; composition: before c. 165 B.C. | The title names Asaph; the corpus gives no attribution row for it, and no witness read here dates an occasion (the Fathers read it of Christ's coming, which is not a date). Unresolved is preserved |
| Second reading | Composition, disputed: A.D. 56 or about Easter 57 | — |
| Alleluia verse (Psalm 84:8) | Historical setting: occasion date unresolved; composition: the Korahite collection, between Isaias and the return from exile | The element is keyed `acclamation`; the table gives it **no narrated-event row**, as required |
| Gospel | Narrated event: Jesus charges all the disciples to keep watch, on Mount Olivet opposite the Temple, c. A.D. 29 (derived; Maas; Passion dates disputed); composition of Mark, disputed, A.D. 38–70 | The event row exists in the shared corpus (`life-of-christ.closing-charge-to-watch`, bound to Mark 13:33–37); no repair was needed |
| Communion antiphon (Psalm 84:13) | As the acclamation's composition | — |
| Collect, Prayer over the Offerings, Preface, Prayer after Communion, solemn blessing | No Scripture; no date | Reasons recorded in the input |

### 8.2 The sources behind the answers, read

The Gospel event's basis was read: Mark 13:1–4 and 13:33–37 in the
Douay–Rheims (Olivet, the four disciples, the charge to all), and the verified
Catholic Encyclopedia passage `maas-ninth-journey-olivet-prophecies` (the
Tuesday discourse in Maas's harmony), with the era calibration passage.
The corpus's label "all the disciples" is narrower than Augustine's reading of
*all* (section 3.1); the label describes the narrated scene, not the command's
reach, and is accurate for that. The other answers were inspected in the
record, not re-sourced.

### 8.3 Planned place and numbering

- **Isaiah numbering on page 2.** The chronology's query system is the
  Clementine's; the Passage cell therefore prints *Is. 63:16b–17; 64:1, 3–8*
  with no numbering note (the generator adds notes only for Psalms). The study
  documents must give the Lectionary numbering beside it wherever Isaiah is
  cited in prose (`research/context.md`, Lawful study-text routes). The
  Clementine 64:3 is a whole-verse envelope (`chronology-inputs.toml`).
- **Places.** The Gospel row's place, the Mount of Olives opposite the Temple,
  is the corpus's, sourced from Mark 13:3–4. The first reading's place, Judah
  and Jerusalem, belongs to the traditional-attribution row, not to the
  composition row.

## 9. Rights

The approved United States English of the Lectionary, the psalm response and
the Missal is not reproduced anywhere in this research; the readings page and
the NABRE are described. The Latin typical texts are quoted only in short
phrases needed for the findings (the Collect's, Preface's and orations'
agreements with their early witnesses), as the owner does. Translators'
English is quoted only in short phrases and is credited to the translation
(Oxford, NPNF, Gifford, O'Sullivan, Dalgairns). The Verona and Gelasian
editions (Feltoe 1896, Wilson 1894) are public domain in the United States.

## 10. Unresolved leads

- Cassiodorus on Psalms 79 and 84; Lapide on 1 Corinthians 1:5 and 1:7.
- The Lectionary's 1970 translation of Isaiah 64:2 and the Hebrew of Psalm
  80:16b.
- The other sacramentaries Wilson names for the Collect; the solemn blessing's
  and the Preface's first half's antecedents.
- The registered augustinus.it state of Augustine on Psalm 24, which reportedly
  reads *qui te exspectant* (owner finding 5).
- The printed *Book of Blessings*.

## 11. Source registration

The source-registration stage of the same run (26 November 2026) re-hashed
every receipt of the context and research stages before relying on it; all
matched the values recorded here, in `research/context.md` and in
`propers/verified.md`.

- **Registered.** The deliveries read here that the library did not hold are
  registered as restricted artifacts (identity, hash and extent; no bytes
  retained): the *Nova Vulgata* Isaiah page; the NABRE Isaiah 64 page in a new
  dated edition; the readings page in its state of 26 November 2026
  (`…daily-readings.2026-11-26-page-for-2026-11-29.lectionary-2-7e0b44c0`),
  read by the context stage; the Internet Archive capture of General
  Instruction chapter II made at `20261015002800`
  (`…usccb-chapter-ii-wayback-2026-10-15-b6bc5b79`), read by the context
  stage; the Catholic Culture Advent-wreath transcription in its state of 26
  November; and the seven New Advent pages of section 5 in new dated editions,
  each recording New Advent's revision credit. The NABRE Isaiah 63 challenge
  page and the 4,608-byte augustinus.it response are not the source and are
  not registered.
- **Bindings reconciled.** `research/source-bindings.toml` now binds the states
  actually read in place of the unread registered states of the readings page
  and the transcription, binds the chapter II capture, the two Bible pages and
  the New Advent cross-checks, binds the Gelasian OCR and the inventory's
  Verona passage as context (they were read as finding aids, so they are not
  leads), and states the Chrysostom lines read (727–851, sections 4–8).
- **Admitted.** Chrysostom's Homily 2 on 1 Corinthians, sections 4–8, is a new
  verified passage under the existing segment of the tracked NPNF I.12 text,
  with its canonical edge 1 Cor 1:7–9 in
  `src/sources/commentary/fragment-loci.yaml`. The other admitted rows name
  passages that already stood in the Catena (Augustine on Psalms 24 and 84;
  Bellarmine on Psalms 24, 79 and 84; the *Catena aurea* on Mark 13:32–37).
- **Deferred, with what is missing.** Jerome on Isaiah (no checked
  transcription of the Migne columns read); Aquinas on Isaiah and on
  1 Corinthians and Augustine's letter 199 (restricted deliveries, no
  publishable controller); Augustine on Psalm 79 (no passage record; the
  translation abridges); Bede on Mark 13:32–37 (the work's locus grammar admits
  only Mark 10, and part of the block is Jerome's and Gregory's text); Jerome
  on Matthew 24:36 and 24:42–43, PL 26 cols. 181–182, as an analogue (added at
  iteration 1; read on a page image, no checked transcription); Gregory, Homilies 13
  and 9.1, as analogues on Luke 12:35–40 and Matthew 25:14; Chrysostom,
  Homily 77 on Matthew, as an analogue on Matthew 24:42–44; Cyril, Catechesis
  XV.1 (no Scripture extent can be fixed). `research/source-dispositions.toml`
  holds each row's exact pin, candidate extent and missing criteria.
- **Rejected for the Catena only.** The New Advent cross-checks: a modern
  revision of unresolved rights. Their use here as cross-checks is unchanged.
- **After research iteration 1** (source registration, iteration 1, the same
  day). Research iteration 1 read nothing the library did not hold: the
  Migne PL 26 PDF is the registered remote artifact, and its receipt was
  re-hashed again and matched. The library already holds Jerome's commentary
  on Matthew as a segment of that volume (PDF pp. 13–116), so the reading of
  cols. 181–182 is now also bound through that segment, with its own deferred
  row, and is identified as Jerome's work and not only as a page of the Migne
  volume. PDF p. 98 was rendered again from the receipt and both comments
  were confirmed on the image. Nothing was admitted: no checked transcription
  of the columns exists. The bindings now number 66 and the dispositions 69.
- **At research iteration 2** (the same day). Nothing was fetched. Jerome,
  PL 24 cols. 642–644 and 649, was read again on page images rendered from
  the research stage's receipt of the registered PDF, re-hashed and matched
  (`e55e8bd2…`); Aquinas [85023] again in the re-hashed Corpus Thomisticum
  receipt (`5300798b…`); the *Nova Vulgata* Isaiah 63:17 and Psalm 79 (80):4
  and 15 again in their re-hashed receipts. The contexts of bindings 29 and
  31 now record what each witness does with the two petitions to turn, and
  their dispositions' digests are refreshed. Lapide's held Gospel volume 3 was
  checked at Mark XIII for a negative result and is bound (67) with a rejected
  row, `lapide-in-marcum-13-negative`. Augustine's Oxford English at En. in
  Ps. 79 §3 (tracked, physical lines 39666–39677) and Aquinas on 1 Corinthians
  1:9 ([86234], re-hashed receipt `8be5b71c…`) were read again for Reading 3's
  allegorical sense. The bindings now number 67 and the dispositions 70.
- **Source registration, iteration 2** (the same day). Nothing new was read
  that the library did not hold, and nothing was registered or admitted. The
  receipts relied on were re-hashed and matched: Migne PL 24 (`e55e8bd2…`),
  on whose page images (PDF pp. 325–326) the lemma of 63:17 at col. 642 and
  *Convertere, ait, Domine, sive converte nos* at cols. 643–644 were
  confirmed; Aquinas on Isaiah [85023] (`5300798b…`) and on 1 Corinthians
  [86234] (`8be5b71c…`); the tracked Oxford English of Augustine on Psalm 79
  §3 (`d6841950…`); and Lapide's volume 3 (`b001cf78…`), whose Mark XIII
  comments only on 13:6 and 13:11. `discover` for Mark 13:33–37 lists that
  volume as containing the passage, and for Isaiah 63–64 lists no Lapide
  holding inside the chapters. Lapide's row is now rejected as a candidate
  on Mark 13:33–37 whose locus does not expound it (criterion
  `exposition-of-the-extent`); the criterion research iteration 2 had used
  was keyed to this Mass's appointment and so read as a rejection of his
  comments on 13:6 and 13:11, which nothing here judged. The contexts of the Augustine
  English binding and the Aquinas 1 Corinthians binding, and those rows'
  reasons, now record what Reading 3's allegorical sense takes from them;
  their digests are refreshed. Bindings 67, dispositions 70.
