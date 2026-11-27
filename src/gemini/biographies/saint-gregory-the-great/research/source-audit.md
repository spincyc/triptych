# Pope Saint Gregory the Great — source audit

Provider: Google Gemini (`gemini-4-neon`, effort `xhigh`). Inspection date:
2026-11-27. All inspections were performed offline against exact tracked local
files in `src/sources/works/` (zero network access). No untracked text is
claimed as directly inspected; every reported witness carries its exact local
reporting carrier and ceiling.

## Tracked local editions and translation basis

1. **NPNF Series 2, Vol. 12** (`nicene-and-post-nicene-fathers/series-2-volume-12`,
   unrevised CCEL text `ccel-text-7bb1db6e/source.txt`, 48,066 lines; Gregory
   begins at line 20,973). Contains James Barmby's Prolegomena (1895), complete
   *Book of Pastoral Rule* (*Regula Pastoralis*, Parts I–IV), and *Selected
   Epistles* Books I–VIII in Benedictine/Maurist (Migne PL 77) numbering.
2. ***Moralia in Iob*** (`gregory-the-great/moralia-in-iob`, Oxford Library of
   the Fathers 1844–1850 complete English text `complete-text-d9f9ed86/source.txt`).
   Inspected directly at Preface (§§1–21), Epistle Dedicatory to Leander
   (§§1–5), Book I opening, and Book XIV.56 (§§72–77).
3. **Gregory of Tours, *Historia Francorum* Book X.1**
   (`gregory-of-tours/historia-francorum`): O. M. Dalton 1927 Oxford English
   Vol. 2 (`historyoffranks0002greg_djvu.txt`, lines 20040–20308) collated with
   W. Arndt 1884 MGH Latin (`monumentagerman01hann_djvu.txt`, lines 31960–32116).
4. ***Homiliae XL in Evangelia*** (`gregory-the-great/homiliae-in-evangelia`):
   complete tracked Wikisource Latin (`gregory-whole.txt`), six individually
   checked Migne PL 76 Garnier 1878 Latin texts (`1.1-opening`,
   `1.5-world-grown-old`, `8.1-bethlehem`, `8.1-manger`, `8.1-masses-and-census`,
   `20-heading`), and full PL 76 DjVu OCR (`patrologiaecursu76mign_djvu.txt`,
   lines 104420–104543 for *Oratio ad plebem de mortalitate*, cols. 1311–1314).
5. ***Homiliae in Hiezechihelem Prophetam***
   (`gregory-the-great/homiliae-in-hiezechihelem-prophetam`, Migne PL 76 1849
   complete Latin `homiliae-in-ezechielem.wiki`). Inspected directly at Book II,
   Homilies 6, 7, and 10.
6. **Gregorian Sacramentary (*Hadrianum*)**
   (`catholic-church/sacramentarium-gregorianum-hadrianum`, H. A. Wilson 1915
   HBS 49 `pdf-text-layout-6ca97fd7/source.txt` and verified Latin *Hanc igitur*
   `canon-hanc-igitur-checked-latin-b46e0e89/text.txt`).
7. **Migne *Patrologia Latina* Vol. 78**
   (`jacques-paul-migne/patrologia-latina-volume-78`, OCR
   `patrologiaecursu78mign_djvu.txt`). Inspected at cols. 17–26 (Sacramentary
   prefaces & Hadrian I's letter to Charlemagne) and cols. 649–652 (Antiphonary
   prefaces & Goussainville quoting John the Deacon *Vita* II.6–9).
8. **Adrian Fortescue, *The Mass* (1922)**
   (`adrian-fortescue/the-mass-a-study-of-the-roman-liturgy`): verified passage
   records `p-172.toml` and `p-234-235.toml`.
9. ***Martyrologium Romanum* (1902)**
   (`catholic-church/martyrologium-romanum`, Propaganda Fide
   `gtu_32400004276022_djvu.txt`): inspected at 12 March (p. 36, lines
   9241–9301) and 3 September (p. 132, lines 16790–16844).
10. **Benedict of Nursia, *Regula Benedicti***
    (`benedict-of-nursia/regula-benedicti`, Latin `regula-latin-text/regula-benedicti.txt`),
    consulted for sixth-century Italian monastic context beside *Dialogi* II.

## Claim-by-claim audit: Subject-authored loci (Class A)

| Work and locus | Claim / quotation verified | Tracked artifact & lines | Witness date & genre | Function & limit |
|---|---|---|---|---|
| *Moralia*, Ep. Ded. 1–2 | "Long time did I put off the grace of conversion"; monastic retreat; forced summoning to Constantinople; Leander friendship; Genesis of oral *Moralia* lectures | `moralia-in-iob` `source.txt`, lines 506–605 | c. 595; dedicatory epistle (autobiographical retrospect) | Primary self-account of conversion & Constantinople; written 15–20 years later |
| *Moralia*, Ep. Ded. 3–5 | Threefold sense (historical, allegorical, moral); "foundation of the history"; chronic stomach/fever infirmities; refusal to bend Scripture to Donatus's grammar | `moralia-in-iob` `source.txt`, lines 606–728 | c. 595; dedicatory epistle | Primary exegetical method and bodily-suffering witness |
| *Moralia*, Pref. 2 | "Job" / *dolens*; Christological and ecclesiological frame of Job | `moralia-in-iob` `source.txt`, lines 1–90 | c. 595; treatise preface | Programmatic key to the 35-book commentary |
| *Moralia* XIV.56 (§§72–77) | Dispute with Patriarch Eutychius on palpable risen body (Luke 24:39); Emperor Tiberius orders Eutychius's treatise burned; Eutychius grasping his skin before death | `moralia-in-iob` `source.txt`, lines 23210–23320 | c. 582–595; theological commentary with eyewitness anecdote | Firsthand Constantinople theological witness (Gregory's side only; Eutychius's treatise lost) |
| *Regula Pastoralis* I.1–5 | "The government of souls is the art of arts"; warning against unlearned/hypocritical rulers; pastoral duty of feeding the flock (John 21:17) | NPNF2-12 `source.txt`, lines 22815–23100 | 590–591; pastoral treatise to John of Ravenna | Core theology of pastoral vocation |
| *Regula Pastoralis* I.6–7 | Humility that flees office vs. perverse obstinacy (I.6, 23101–23118); Isaiah and Jeremiah contrast (I.7, 23119–23168) | NPNF2-12 `source.txt`, lines 23101–23168 | 590–591; pastoral treatise | Exact loci for reluctant-vocation dialectic |
| *Regula Pastoralis* II.1, 4–6 | "Pure in thought, in action chief; discreet in keeping silence, profitable in speech" (II.1); golden bells and pomegranates (II.4); compassion and contemplation (II.5); natural equality of all men (II.6) | NPNF2-12 `source.txt`, lines 23472–23492, 23658–24099 | 590–591; pastoral treatise | Ideal portrait of the pastor's interior life |
| *Regula Pastoralis* III Prol., 1–2 | Strings of a harp struck differently; thirty-six contrasting pairs of souls (men/women, rich/poor, joyful/sad, etc.) | NPNF2-12 `source.txt`, lines 24699–24911 | 590–591; pastoral treatise | Individualized pastoral psychology |
| *Regula Pastoralis* IV | Final warning against pride after preaching well; "an ill-favoured painter pourtraying a handsome man" | NPNF2-12 `source.txt`, lines 28681–28786 | 590–591; treatise epilogue | Self-indicting pastoral humility |
| *Ep.* I.5 (to Theoctista; cf. I.6–7) | "Under colour of the episcopate I have been brought back to the world"; Rachel/Leah and Mary/Martha; ape ordered to be made a lion | NPNF2-12 `source.txt`, lines 28964–29070 (I.6: 29071–29154; I.7: 29155–29210) | Oct. 590 (Indiction IX); personal letter to emperor's sister | Primary window into Gregory's post-election grief |
| *Ep.* I.10, I.35 (Terracina) | Restoring confiscated synagogue; Jews live "under the protection of the Roman laws" (I.10); persuasion by "gentleness, kindness, admonition" (I.35) | NPNF2-12 `source.txt`, lines 29248–29283 (I.10), 30060–30085 (I.35) | Nov. 590 (I.10) & Mar. 591 (I.35); episcopal directives | Maurist I.35 = MGH I.34; paired with ban on Christian slaves held by Jews |
| *Ep.* I.16–17 | Three Chapters schism in Istria/Aquileia (I.16); death of Autharis and warning to Italian bishops (I.17) | NPNF2-12 `source.txt`, lines 29333–29370 (I.16), 29371–29409 (I.17) | 590–591; official letters | Early doctrinal impasse and Lombard political anchor |
| *Ep.* I.25 (Synodical) | Confesses the four Ecumenical Councils "as the four books of the Gospel", plus venerates the Fifth Council | NPNF2-12 `source.txt`, lines 29550–29709 | Feb. 591; synodical profession to Eastern patriarchs | Classic patristic conciliar formula |
| *Ep.* I.36 (to Peter Subdeacon) | Salutation *servus servorum Dei* and Sicilian patrimonial instructions | NPNF2-12 `source.txt`, lines 30086–30172 | Mar. 591; administrative letter | Attests *servus servorum Dei* papal title |
| *Ep.* I.43 (to Leander) | Church as "the old and rotten ship"; joy at Visigothic King Reccared's conversion; single vs. triple immersion permissible in one faith ("where there is one faith, a diversity of usage does no harm to holy Church") | NPNF2-12 `source.txt`, lines 30260–30355 ("Given in the month of May" at line 30332) | May 591; personal/episcopal letter (MGH I.41) | Shows liturgical flexibility where dogma is intact |
| *Ep.* I.44 (to Peter in Sicily) | Agrarian justice for *rustici*/*coloni*: 18-*sextarii* *modius*, *burdatio* tax advance, 1-*solidus* marriage fee, inheritance rights, restitution, public charters; moderate subdeacon continence rule | NPNF2-12 `source.txt`, lines 30356–30810 | May 591; patrimonial administrative instruction | Premier primary witness to Gregorian economic justice and pastoral realism |
| *Ep.* I.47 (to Virgilius & Theodorus) | Forbids forced baptism of Jews at Marseilles ("not by the sweetness of preaching, but by compulsion") | NPNF2-12 `source.txt`, lines 30838–30875 | June 591; papal letter to Gallic bishops (MGH I.45) | Foundational medieval papal anti-coercion text |
| *Ep.* I.74 (to Gennadius) | Urges imperial Exarch of Africa to suppress lingering Donatist schismatics | NPNF2-12 `source.txt`, lines 31351–31418 | July 591; papal letter to imperial magistrate | Documents sixth-century reliance on imperial penal laws against schism |
| *Ep.* II.46 (to John of Ravenna) | Ariulf's march toward Rome; Exarch Romanus "both evades fighting against our enemies and also forbids our making peace"; Three Chapters friction | NPNF2-12 `source.txt`, lines 32886–33023 | 592; official letter | Documents military abandonment of Rome |
| *Ep.* II.54 (Licinianus) | Contemporary Spanish bishop praises *Regula Pastoralis* as "a palace of all virtues" | NPNF2-12 `source.txt`, lines 33509–33667 | c. 592; incoming letter preserved in *Registrum* | Class N contemporary reception |
| *Ep.* III.65 (to Maurice) | Protests imperial law barring soldiers/officials from monasteries while dutifully promulgating it | NPNF2-12 `source.txt`, lines 35550–35651 | Aug. 593; papal letter to emperor | Exact articulation of obedience + prophetic dissent |
| *Ep.* IV.26 (to Januarius of Cagliari) | Authorizes fiscal pressure and penal discipline against obstinate pagan peasants on Sardinian Church estates | NPNF2-12 `source.txt`, lines 36674–36811 | May 594; episcopal directive | Direct primary witness to sterner policy toward rural pagans |
| *Ep.* IV.30 (to Constantina) | Refuses request for St. Paul's head; Roman awe before apostolic tombs; *brandea* cloths and filings of St. Peter's chains | NPNF2-12 `source.txt`, lines 36916–37025 | June 594; letter to empress | Crucial Class A witness to Roman relic piety |
| *Ep.* V.18–21, V.43 | Campaign against Patriarch John IV the Faster's title *Oikoumenikos* ("Universal Bishop"); Petrine texts (John 21, Luke 22, Matt 16); refusal of sole-bishop claim. **Textual note:** NPNF2-12 *Ep.* V.21 line 38537 prints "seven years" among Lombard swords, whereas Barmby's Prolegomena (line 21034, following Latin *viginti septem*) gives "twenty-seven years" | NPNF2-12 `source.txt`, lines 37979–38600 (V.18: 37979–38258; V.19: 38259–38310; V.20: 38311–38458; V.21: 38459–38600) & 39153–39321 (V.43) | Jan. 595 in Barmby/Benedictine text of V.18 (*Kalends of January; Indiction 13*, line 38232; Prolegomena line 22112) / June 595 in MGH; five coordinated diplomatic letters | Primary dossier of the Universal Bishop controversy |
| *Ep.* V.39–42 | Anastasius of Antioch (V.39); Agilulf's siege: "Romans tied by the neck with ropes like dogs" and reply to Maurice's "simple" taunt (V.40); Sardinia/Corsica/Sicily tax abuses to Constantina (V.41); Exarch Romanus "surpassed the swords of the Lombards" (V.42) | NPNF2-12 `source.txt`, lines 38794–39152 (V.39: 38794–38877; V.40: 38878–39015; V.41: 39016–39093; V.42: 39094–39152) | June 595; diplomatic letters | Eyewitness testimony to 593 siege and imperial fiscal cruelty |
| *Ep.* V.49 (to Leander) | Dispatches completed *Moralia* and *Regula Pastoralis* to Spain | NPNF2-12 `source.txt`, lines 39375–39398 | July 595; personal letter | Anchors publication date of *Moralia* |
| *Ep.* VI.5 (to Queen Brunichild) | Diplomatic praise to Frankish queen seeking support for Gallic ecclesiastical order | NPNF2-12 `source.txt`, lines 40105–40191 | Sept. 595; diplomatic letter | Illustrates late-Roman courtly diplomatic style |
| *Ep.* VI.7 (to Candidus) | Instructs buying English boys aged 17–18 in Gaul to educate in monasteries for God's service | NPNF2-12 `source.txt`, lines 40243–40275 | Sept. 595; administrative letter | First dated epistolary trace of Gregory's English concern (before 596 mission) |
| *Ep.* VI.14–17 | Eastern appeals of presbyters against Constantinople (to Narses, John, Maurice, and Theotistus; VI.16 praises Maurice as "most Christian of princes") | NPNF2-12 `source.txt`, lines 40416–40629 | 595–596; papal appellate letters | Documents active papal jurisdiction in the East and pre-602 esteem for Maurice |
| *Ep.* VI.51–59 | Dispatch of Augustine and monks to England (23 July 596): encouragement after turnaround (VI.51), letters to Frankish kings, Queen Brunehild, and bishops | NPNF2-12 `source.txt`, lines 41445–41798 | July 596; missionary dossier | Gold-standard Class A anchor for the English mission |
| *Ep.* VII.33–34, 38, 40 | "Precursor of Antichrist" for Universal Priest (VII.33); admitting lack of Greek patristic witness on Eudoxius (VII.34); selling church silver for captives (VII.38); one Petrine chair shared by Rome, Alexandria, Antioch (VII.40) | NPNF2-12 `source.txt`, lines 43529–43597 (VII.33), 43598–43728 (VII.34), 43756–43783 (VII.38), 43821–43908 (VII.40) | 597; papal letters | Clarifies collegial Petrine ecclesiology, linguistic limit, and mercy for captives |
| *Ep.* VIII.30 (to Eulogius) | Announces 10,000+ English baptized at Christmas 597; rebukes "Universal Pope" and *sicut jussistis* ("my honour is the solid vigour of my brethren") | NPNF2-12 `source.txt`, lines 44858–44959 (Book VIII ends at line 45196) | July 598; letter to Patriarch of Alexandria | Verifies both English mission breakthrough and *servus servorum Dei* humility |
| *Hom. in Evang.* Praef.; 1.1, 1.5; 8.1; 20 | Letter to Secundinus on weak voice / notary reading; *mundus senescens* ("world grown old"); Bethlehem *domus panis* & three Christmas Masses on one day (preached at St. Mary Major); stational rubrics | `homiliae-in-evangelia` checked Garnier 1878 texts & `gregory-whole.txt`, lines 3–60 | 590–592; Roman stational homilies | Verified directly in Latin; shows stational liturgy and eschatological urgency |
| *Hom. in Evang.* 37.7–9; 38.15–16 | Weekly Masses loosing a captive's chains (37.8); Bishop Cassius of Narni's daily Mass (37.9); virgin aunts Tharsilla, Gordiana, Aemiliana; Pope Felix III as *atavus meus*; mother at Tharsilla's deathbed; monastery beside SS. John and Paul (38.15–16) | `homiliae-in-evangelia` `gregory-whole.txt`, lines 523–526, 547 | 591–592; Roman homilies | Crucial Class A family testimony and direct Gregorian parallel to *Dialogi* IV |
| *Hom. in Evang.* 40.7, 11–12 | Irreversibility of hell (no deliverance for the damned); Romula "pearl on a dunghill" | `homiliae-in-evangelia` `gregory-whole.txt`, lines 570–575 | 591–592; Roman homily | Direct Class A theological counter-evidence to the later Trajan legend |
| *Oratio ad plebem de mortalitate* | Plague exhortation commanding the sevenfold litany | Migne PL 76 OCR `patrologiaecursu76mign_djvu.txt`, cols. 1311–1314 (lines 104420–104543) | 590; plague address | Cross-checks *HF* X.1 |
| *Hom. in Hiez.* II.6.1, 22–23; II.7.7–9; II.10.24 | *Ubi enim senatus? Ubi jam populus? ... jam vacua ardet Roma* (II.6.22); seven gifts of the Spirit (II.7.7), humility (II.7.8), and faith as threshold (II.7.9); breaking off preaching during Agilulf's 593 siege (*undique gladiis circumfusi sumus ... detruncatis ad nos manibus redeunt*, II.10.24) | `homiliae-in-ezechielem.wiki`, Book II Hom. 6, 7 (lines 565–568), 10 | Late 593; Roman homilies | Unrivaled firsthand testimony to Rome's urban collapse and Agilulf's siege |

## Claim-by-claim audit: Contemporary, liturgical, and scholarly witnesses (N/L/M/K)

| Witness & locus | Claim / quotation verified | Tracked artifact & lines | Class & ceiling |
|---|---|---|---|
| Gregory of Tours, *Historia Francorum* X.1 | Eyewitness Tours deacon in Rome (590): Nov. 589 Tiber flood, Jan./Feb. 590 *lues inguinaria*, death of Pelagius II, Gregory's senatorial wealth, 6 Sicilian + 1 Roman monastery, silk attire, intercepted letter to Maurice by Prefect Germanus, *Oratio*, *litania septiformis* to St. Mary Major, 80 deaths in one hour (zero mention of Archangel Michael), flight & consecration | Dalton 1927 `historyoffranks0002greg_djvu.txt` (lines 20040–20308); Arndt 1884 `monumentagerman01hann_djvu.txt` (lines 31960–32116) | **N** — Gold-standard contemporary eyewitness report (written before Gregory of Tours died in 594) |
| H. A. Wilson, *Hadrianum* (1915), Intro. pp. xv–xxxii, p. 25, pp. 145–146; checked *Hanc igitur* | Hadrian I sends Sacramentary to Charlemagne (784–791); Mass *Natale Sancti Gregorii Papae* (12 March, p. 25) proves later Roman additions; Carolingian *Hucusque* preface (pp. 145–146) marks Gregory's own feast with *virgulae*; checked Latin *Hanc igitur* clause (*diesque nostros in tua pace disponas...*) | `sacramentarium-gregorianum-hadrianum` `source.txt` (lines 642–1529, 3393–3404, 9245–9316) & `canon-hanc-igitur-checked-latin-b46e0e89/text.txt` | **L / M / K** — Decisive primary + scholarly control against whole-book Gregorian authorship |
| Migne PL 78, cols. 17–26 & 649–652 | Benedictine prefaces on *Liber Sacramentorum* (printing Hadrian I's letter to Charlemagne) and *Antiphonarium* (Goussainville quoting John the Deacon *Vita* II.6–9: *Antiphonarium centonem*, *schola cantorum*, sickbed & *flagellum*, Metz/Charlemagne chant rivalry) | `patrologia-latina-volume-78` `patrologiaecursu78mign_djvu.txt` (lines 640–1050, 56362–56500) | **L / K** — Verified Latin excerpts of Hadrian I and John the Deacon II.6–9 |
| Adrian Fortescue, *The Mass* (1922), pp. 172, 234–235 | p. 172 summarizes Gregory's three changes (*Kyrie eleison*, *Hanc igitur* addition, *Pater noster* before Communion) and Benedict XIV's dictum on the Canon; pp. 234–235 quote *Ep.* IX.12 on Roman *Kyrie*/*Christe eleison* and reject John the Deacon's ascription of the *Kyrie*'s introduction to Gregory via the Council of Vaison (529) | `adrian-fortescue/the-mass-a-study-of-the-roman-liturgy` passage records `p-172.toml` & `p-234-235.toml` | **K** (with **A** quotation of *Ep.* IX.12 at Fortescue's reporting ceiling) |
| *Martyrologium Romanum* (1902), 12 March & 3 September | 12 March (p. 36): *Magnus est dictus, et Anglorum Apostolus appellatus*; 3 September (p. 132): *ordinatio in Summum Pontificem* | `martyrologium-romanum` `gtu_32400004276022_djvu.txt` (lines 9241–9301, 16790–16844) | **M** — Official liturgical reception witness |
| James Barmby, Prolegomena & notes (1895) | Survey of life, *Registrum* Books IX–XIV (Phocas, Theodelinda, *Ep.* XI English mission, *Ep.* VIII.25/IX.36 Jews, IV.26/IX.65 pagans), *Dialogi* summary & authorship, Whitby/Bede/Paul/John *Vitae*, epitaph (*Consul Dei*), posthumous famine episode | NPNF2-12 `source.txt`, lines 20970–22764 | **K** — Controlled secondary carrier for all untracked witnesses below |
| *Regula Benedicti* | Sixth-century Italian monastic legislation consulted as contextual control beside reported *Dialogi* II | `benedict-of-nursia/regula-benedicti` `regula-benedicti.txt` | **N/Context** — Confirms sixth-century Italian cenobitic rule; does not prove Gregory lived under Benedict's Rule on the Caelian |

## Bounded negative checks and reporting ceilings

1. **Untracked local works:** Verified directly that `src/sources/works/gregory-the-great/dialogi/work.toml` and `src/sources/works/bede/historia-ecclesiastica-gentis-anglorum/work.toml` hold catalog entries only (no editions or artifacts), and that `src/sources/works/nicene-and-post-nicene-fathers/` lacks `series-2-volume-13` (*Registrum* IX–XIV). Likewise, the Whitby *Vita*, Paul the Deacon's *Vita* and *Historia Langobardorum*, John the Deacon's complete *Vita*, *Legenda Aurea*, and Boniface VIII's 1298 decretal are not tracked verbatim locally (except John the Deacon II.6–9 as quoted in Migne PL 78 cols. 650–651). Every reference to these texts in the publication explicitly states its reporting carrier.
2. **Epistle VIII.25 check:** Inspected NPNF2-12 Book VIII directly; *Ep.* VIII.25 (on restoring a Palermo synagogue) is NOT among Barmby's translated selections in Book VIII and is therefore never quoted verbatim as inspected, whereas *Ep.* I.10, I.35, and I.47 WERE read and quoted verbatim.
3. **Negative check in *HF* X.1:** Full line-by-line inspection of both Dalton (1927) and Arndt (1884) for Book X.1 confirms **zero** mention of Archangel Michael, a drawn or sheathed sword, or Hadrian's Mausoleum during the 590 sevenfold litany.
4. **Negative check on *Gens Anicia*:** Neither *Hom. in Evang.* 38.15 (which names Pope Felix III as *atavus* and names his aunts) nor *HF* X.1 nor *Moralia* Ep. Ded. names the *Gens Anicia*; the Anician pedigree rests on later hagiographic/scholarly inference and is explicitly flagged as such.
