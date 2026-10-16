# Source audit — Then Face to Face (rewrite of 16 October 2026)

Every quotation printed in the body was read by the authoring agent on
2026-10-16 (UTC) at the locus named, in the witness named. A mechanical check
(every quoted string and block quotation in `sections/00`–`80`, split at
ellipses, matched against the normalised text of the witnesses listed below)
was run on 2026-10-16; its residual non-matches were each resolved by eye and
are explained in the "OCR and typography" section. Downloaded working copies
used for reading were not retained in the repository.

Rights classes: **PD** = public domain (US, by publication date, unless stated);
**Official ©** = the Holy See's copyrighted English, quoted briefly with
attribution.

## Scripture and liturgy

| Claim or quotation | Witness and locus | Check (2026-10-16) | Rights |
| --- | --- | --- | --- |
| All Scripture quoted: Ex 33:18–23; Ps 26:8; 35:10; 41:2–3; 83:2–5; Ecclus 24:29; Matt 5:8; 13:43; 24:30; 25:21, 23, 34; Luke 16:20–22; 21:28; John 14:3; 17:24; 1 Cor 13:12; 15:41–44, 53–55; Phil 3:20–21; 1 Thess 4:16–17 (Vulgate numbering); 1 Tim 6:16; Heb 12:14, 22–23; 1 John 3:1–3; Apoc 7:9; 19:9; 21:1–27; 22:3–5 | Douay–Rheims (Challoner), PG eBook 1581, edition `challoner-gutenberg-1581`; read in `src/sources/bibles/douay-rheims/chapters/<Book>/<n>.json` | Each verse printed from the JSON by a lookup script and compared | PD |
| 1962 Missal: All Saints Gospel Matt 5:1–12, Communion Matt 5:8–10; Last Sunday after Pentecost Gospel Matt 24:15–35; Advent I Gospel Luke 21:25–33 | `src/sources/calendars/roman-1962/propers.yaml` (Omnium Sanctorum, l. 47676ff; Dominica XXIV et ultima, l. 15981; Advent I, l. 663) | Read | citations only |
| Postconciliar: All Saints (Apoc 7:2–4, 9–14; 1 John 3:1–3; Matt 5:1–12a; OLM n. 667); 33rd Sunday Year A Gospel Matt 25:14–30; Christ the King Year A Gospel Matt 25:31–46 | `src/sources/calendars/postconciliar/propers.yaml` (all-saints l. 50555ff; ot-33; Christ the King l. 38699ff) | Read; Year A cycles identified at their `A:` keys | citations only |
| *Subvenite* (In exspiratione, pp. 131–132) and the rite at the grave after *In paradisum* (blessing of the tomb, *Benedictus* with *Ego sum resurrectio*, Kyrie, Pater noster; pp. 142–143) | *Rituale Romanum* (Pustet, 1872), IA OCR text | Read 2026-10-16 | PD |
| *In paradisum*, Latin, with accents, and the rubric "Finita Oratione, corpus defertur ad sepulchrum … Clerici cantant Antiphonam" | *Rituale Romanum* (Ratisbon: Pustet, 1872), Exsequiarum ordo, p. 141; IA `ritualeromanumpa00cath_0` (the registered facsimile `internet-archive-pdf-b21a0f45`) | Page image leaf n154 read; OCR text cross-checked | PD |
| *In paradisum*, English: "May the angels lead thee into Paradise; at thy coming may the martyrs receive thee, and bring thee into the holy city, Jerusalem. May the choir of angels receive thee, and with Lazarus, once a beggar, mayest thou have eternal rest." | Lasance and Walsh, *The New Roman Missal*, rev. ed. (Benziger, 1945), "Absolution of the Corpse", p. 1524; IA `fr-lasance-missal-1937`, leaf n1544 | Page image read; tracked OCR (`new-roman-missal-text-80b34759`, l. 166330ff) cross-checked | PD in the US, copyright not renewed (`src/sources/inventories/lasance-new-roman-missal-rights-v1.toml`); p. 1524 lies outside the excluded pp. 1298a–n and 1302a–d |

## Councils and the Magisterium

| Claim or quotation | Witness and locus | Check | Rights |
| --- | --- | --- | --- |
| *Benedictus Deus*: "viderunt et vident divinam essentiam visione intuitiva et etiam faciali, nulla mediante creatura in ratione obiecti visi se habente, sed divina essentia immediate se nude, clare et aperte eis ostendente"; "vere beatae"; souls of saints see God "etiam ante resumptionem suorum corporum et iudicium generale" (stated in English) | DS 1000, Latin *Enchiridion*, patristica.net (`latin-patristica-web-2026-07-25`) | Page re-fetched and read | PD (act) |
| Florence, *Laetentur caeli*: "sicuti est, pro meritorum tamen diversitate alium alio perfectius" — the defined measure is **merits** (V7); charity is attributed to Aquinas as his explanation | DS 1305, same | Read | PD |
| Trent VI can. 32: "gloriae augmentum"; works both gifts of God and merits | DS 1582, same | Read | PD |
| Lateran IV: "cum suis propriis resurgent corporibus, quae nunc gestant" | DS 801, same | Read | PD |
| Vienne, *Ad nostrum qui* (1312), error 5: "anima non indiget lumine gloriae, ipsam elevante ad Deum videndum" (condemned; censure DS 899) | DS 895, 899, patristica.net Latin *Enchiridion* | Read 2026-10-16 | PD |
| Trent session XXV (3 Dec. 1563), decree on the invocation of saints: "orationes suas pro hominibus Deo offerre"; Tridentine Profession of Faith (Pius IV, *Iniunctum nobis*, 1564): "eosque orationes Deo pro nobis offerre" | DS 1821; DS 1867, same | Read 2026-10-16 | PD |
| *Munificentissimus Deus* 44: "having completed the course of her earthly life, was assumed body and soul into heavenly glory" | vatican.va English (edition `english-vatican-web-2026-07-25`) | Fetched and read | Official © |
| *Credo of the People of God* 15: "likened to her risen Son in anticipation of the future lot of all the just"; n. 29 summarised and cited through CCC 1053 | vatican.va English | Fetched and read | Official © |
| CCC 1023 (official English of DS 1000 clause), 1024, 1027, 1028, 1045, 1053 (quoting *Credo* 29: "fraternal concern"), 1054 | vatican.va `__P2M`, `__P2N`, `__P2Q`, `__P2R` | Fetched and read; 1024's spaced hyphens set as dashes | Official © |
| *Spe salvi* 12: "suggests to us the idea of something interminable, and this frightens us"; "is not an unending succession of days in the calendar"; "a plunging ever anew into the vastness of being, in which we are simply overwhelmed with joy" | vatican.va English | Fetched and read | Official © |

## Fathers

| Claim or quotation | Witness and locus | Check | Rights |
| --- | --- | --- | --- |
| Irenaeus IV.20.5 (two block quotations), 20.6 ("Men therefore shall see God …"), 20.7 ("For the glory of God is a living man …"; "preserving at the same time the invisibility of the Father …") | ANF 1 (Roberts–Rambaut 1887), CCEL text `ccel-text-ee9c7f0a`, l. 46560–46690 | Read whole; footnote markers omitted | PD |
| Cyprian, *De mortalitate* 26 (block; "There the glorious company …"; "He who will give the larger rewards …") | ANF 5 (Wallis), CCEL text `ccel-text-a02b61c3`, l. 47190–47222 | Read whole | PD |
| Augustine, *Confessions* I.1; IX.10.23–25 (blocks and run-in); IX.11.27 ("scarcely five days after, or not much more" — paraphrased as "not many days before … fell sick") | NPNF 1/1 (Pilkington), CCEL text `ccel-text-21000696`, l. 2950ff, 12854–12975 | Read | PD |
| Augustine, *De civ.* XXII.29 ("By 'the face' of God …"; "that we shall see Him by the spirit in ourselves, in one another …"); XXII.30 (degrees without envy; "for, as there is nothing greater or better, He has promised Himself"; "He shall be the end of our desires …"; "brought to a close, not by an evening …"; "There we shall rest and see …"; "What power of movement such bodies shall possess …"; "the body shall forthwith be wherever the spirit wills …"; "All the members and organs …") | Dods 1871, `pg45305-body-lf`, l. 21214–21590 | Read whole chapters | PD |
| Gregory of Nyssa, *On the Soul and the Resurrection*: "The All-creating Wisdom fashioned these souls … The fountain of blessings wells up unceasingly"; the speaker is "his sister the Teacher" | NPNF 2/5 (Moore), p. 452 (page anchor in CCEL npnf205.x.iii.ii.html); newadvent.org/fathers/2915.htm | Fetched and read | PD |
| Gregory the Great, *Dialogues* IV.33: "in heaven the good know the good"; "the reward likewise to both parts increaseth …"; block "Beside all this … that know him who knoweth all things?" | P. W. (1608), ed. Gardner (London: Philip Lee Warner, 1911), pp. 217–219; tertullian.org/fathers/gregory_04_dialogues_book4.htm | Fetched and read | PD; **edition needs registration** |

## Doctors and saints

| Claim or quotation | Witness and locus | Check | Rights |
| --- | --- | --- | --- |
| Bernard, *De diligendo Deo* XI: "think to obtain increase of glory …"; "when the soul leaves the body, it is gain, and greater gain when it rejoins it"; block "The body then is for the soul a faithful companion …"; "whether living, dead, or risen …"; "From thence comes satiety which is never satisfied …" | Patmore 1884, `ia-ocr-8a4037c2`, l. 1381–1545 | Read whole chapter | PD |
| Aquinas *ST* I q.12 a.1 (bat and sun), a.4, a.5 (sed contra Ps 35:10; corpus block incl. translators' "[Vulg.: 'because']"; ad 2 block; ad 3), a.6 (corpus block; ad 3 "the same object …"; "on the part of the diverse faculty …"), a.7 ("It is impossible …"; "Hence it is impossible that it should comprehend God") | English Dominican, PG 17611, `pg17611-body-9c99a67a`, l. 4670–5205 | Read. The English is this printing's own; no New Advent attribution is made (V8) | PD |
| Aquinas *ST* I-II q.4 a.5 ad 4, ad 5 | PG 17897, `pg17897-body-6d5b93fb`, art. at l. 2409 | Read | PD |
| Aquinas *ST* II-II q.26 a.13 ("It will however be possible in heaven …"; "for advancing by means of merit to a yet greater reward"); q.28 a.3 (corpus; ad 2) | PG 18755, `pg18755-body-13b14d17`, l. 13280–13360, 14110–14175 | Read | PD |
| Aquinas *ST* III q.28 a.2 ad 3 ("these gifts of a glorified body result from an overflow of the soul's glory on to the body") | PG 19950, `pg19950-body-4597132e`, l. 14068–14073 | Read | PD |
| Supplement q.82 a.1 ("the human body and all that it contains …"); q.85 a.1 ("in the glorified body the glory of the soul will be known …"); qq.82–85 named as the four gifts | English Dominican (2nd ed. 1920) at newadvent.org/summa/5082.htm, 5085.htm (edition `english-newadvent-web-2026-07-25`) | Fetched and read. The four gifts' names follow the question titles; their one-phrase glosses in the text rest on q.82 a.1, q.85 a.1 and Augustine XXII.30 | PD translation |
| Aquinas, *Collationes in Symbolum* a.12: "Deus enim solus satiat, et in infinitum excedit"; "intra in gaudium domini tui"; "totum gaudium non intrabit in gaudentes, sed toti gaudentes intrabunt in gaudium" (given by Thomas as Augustine's); "in omnium beatorum iucunda societate"; "Nam quilibet diliget alium sicut seipsum …"; structure (union in vision, praise, satiety; security; company) | Corpus Thomisticum, csv.html, [86694] | Fetched and read. English beside the Latin is labelled in the note as glosses, not a published translation | Latin PD; **needs registration** |
| Anselm, *Proslogion* 26: "Non ergo totum illud gaudium intrabit in gaudentes, sed toti gaudentes intrabunt in gaudium" — the source of the saying Aquinas (*In Symbolum* a.12) gives under Augustine's name; the body now says so | The Latin Library, anselmproslogion.html, ch. 26 ("An hoc sit gaudium plenum quod promittit Dominus") | Fetched and read 2026-10-16 | PD; **needs registration** |
| Dante, *Paradiso* III.49, 51 ("the slowest sphere"), 70–72, 85–87, 88–90, 106–107 (the cloister) | Longfellow (1867), PG eBook 1004 | Fetched; verse numbers counted from the canto heading | PD; **edition needs registration** |
| Thérèse, thimble and tumbler (ch. 2); "I WILL SPEND MY HEAVEN IN DOING GOOD UPON EARTH" (printed in capitals; set in ordinary case) and "Nor is this impossible …" (Epilogue, said to Mother Agnes of Jesus) | *Soeur Thérèse of Lisieux*, ed. T. N. Taylor (Burns, Oates & Washbourne, 1912; PG eBook 16772) | Fetched and read | PD in the US (1912); quoted briefly; **needs registration** |
| de Sales, *Introduction* I.16 (consideration 1 block; consideration 3; affections 2 and 4) | Rivingtons 1876, `historical-ocr-8159693d`, l. 2961–3050 | Read whole meditation | PD |
| Alphonsus, *Preparation for Death* XXIX: horse and hay (p. 350); "rejoining there her relatives or friends" (p. 351); "In that kingdom of love …" (p. 354); "shall always desire … no tediousness" (pp. 359–360); "When, therefore, the crosses …", Philip Neri, "Heaven! Heaven!", "as long as God shall be God" (pp. 360–361); affection "Heaven! Heaven! When, O Lord … never more offend you" (p. 362) | Duffy 1843, `historical-ocr-d25bba22`, l. 14343–14886; page images IA `preparation_for_death_1893-st_alphonsus_m_liguori` leaves n366, 367, 370, 376–378 | Read; OCR "eid" confirmed as "end" on p. 361 | PD |
| Newman, PPS I.1 (text Heb 12:14): block "Heaven then is not like this world …"; "Ah! he could not bear …"; block "Nay, I will venture …"; "Fire does not inflame iron …"; "Outward acts, done on principle, create inward habits" | Rivingtons 1869, `ia-ocr-9947fafd`, l. 480–800 | Read | PD |

## OCR and typography

- Line-break hyphens and page headers/footnotes interrupting the OCR text
  (Bernard "incom-parable", "com-panion"; Newman p. 4–5 footnote; Alphonsus
  p. 359–360) were closed; the wording was confirmed on page images where an
  OCR error was possible (Alphonsus, Lasance, Rituale).
- CCEL's "--" is set as an em dash; bracketed translator insertions in
  Irenaeus ("[His]") and the English Dominican *Summa* ("[Vulg.: 'because']")
  are reproduced.
- Italics in Alphonsus ("Paradise! Paradise!", "Heaven! Heaven!") are not
  reproduced inside quotation marks.

## Cold-review errors relevant here

- **V7** resolved: Florence's defined measure is stated as merits; charity is
  Aquinas's explanation (§4, Appendix A).
- **V8** resolved: Aquinas is quoted from the Gutenberg English Dominican
  text; New Advent is named only for the Supplement, quoted exactly.
- **V9** avoided: neither *Lumen gentium* 49 nor *Ne super his* is cited.
- **V10** removed with the Palamas section.
- **Heaven 60:53** resolved: the reunion is affirmed on Cyprian, Gregory and
  Aquinas, graded as common teaching.
- **Review corrections (16 Oct.)** applied: Vienne graded Defined with *Benedictus Deus*; intercession graded Defined (DS 1821, 1867); the welcome by angels and martyrs graded as the Church's prayer; Anselm attribution; Bernard order; *In Symbolum* count; Ostia as a shared conversation; Supplement "order of subjection"; *In paradisum* placed on the way to the grave.
- **D6** observed: quotation-mark wording checked mechanically and by eye.
