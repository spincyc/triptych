# Heresies in Catholic History — Controlling Corpus Inventory

## Status, claim, and limits

This is the controlling census for `heresies-in-catholic-history`. It fixes the bounded objects and completed routing against which the narrative, timeline, notices, aliases, contexts, and exclusions are checked. It is **not** an official ecclesial register, a finding of personal culpability, a critical edition, or an independently peer-reviewed specialist census.

The present inventory is an **enumeratively complete, source-mapped census against the disclosed working corpus below**. It does four things:

1. gives stable keys and exact prose destinations to every normalized dossier head in the survey;
2. gives separate stable keys and completed records to source-limited notices, alias groups, contextual controversies, and exclusions;
3. accounts for every standard number in the four disclosed numbered patristic catalogues; and
4. records the edition, attribution, and specialist-review limits that remain after that routing is complete.

It does **not** claim that every act has been collated in its best edition, that every catalogue heading is an independent historical group, that every papal or local investigation in Catholic history belongs to this corpus, or that source mapping settles every disputed identity. A catalogue occurrence is accounted for when it has a source-occurrence key and a completed route; that is not the same as proving that the occurrence names an organized movement or deserves a full historical dossier.

Checked for inventory structure and prose destinations: **2026-07-16**. Critical-edition collation and independent specialist review remain outstanding as stated below.

## Stable-key and disposition rules

Keys are permanent identifiers. A later correction may change the displayed name or disposition but should not recycle a key for a different object.

- `HC.D.<era>.<slug>` — normalized historical or proposition-complex dossier head.
- `HC.N.<era>.<slug>` — compact source-limited notice; normally opponent-only, late, obscure, or too thinly documented for a full dossier.
- `HC.A.<era>.<slug>` — alias or subgroup ledger entry routed to another key.
- `HC.C.<era>.<slug>` — contextual controversy or comparison that must be explained but not counted as a heresy dossier.
- `HC.X.<scope>.<slug>` — explicit exclusion.
- `HC.CAT.<catalogue>.<number>` — one source occurrence in a numbered catalogue. Numbers are zero-padded in data use; a displayed range such as `001–020` includes every intervening occurrence key.

Completion dispositions are:

| Code | Meaning |
|---|---|
| `DOSSIER` | A dedicated four-field historical dossier is present at the recorded destination. |
| `ROUTED` | The head is treated within a named combined four-field dossier; it is not silently counted twice. |
| `ERROR` | A completed proposition- or error-level dossier is present; the act is not rewritten as creation of a named heresy. |
| `NOTICE` | A completed compact source-limited record gives the attributed object, attestation or response, aftermath, and evidence limit. |
| `ALIAS` | No independent count; route to the named dossier or notice. |
| `CONTEXT` | Explain historically, but do not count as a heresy dossier. |
| `EXCLUDE` | Reasoned exclusion from the Christian-heresy census. |
| `CATALOGUE` | A source occurrence is mapped to a dossier, notice, context, or exclusion without creating another historical-object count. |

The evidence grades A–D in the prose measure documentary access, not doctrinal gravity. The source anchors below identify the basis and remaining limit of each compressed treatment; they do not claim a new critical text.

## Disclosed working corpus

The closed enumerative claim comprises: every standard occurrence in Epiphanius 1–80, Philastrius 1–156 in the CSEL 38 sequence, Augustine 1–88, and John Damascene 1–103 in common modern numbering; the named material routed by book and chapter from Irenaeus I and Hippolytus I–X; the movements and propositions actually treated from the received ecumenical councils and the identified papal, Roman, regional-synodal, medieval, Reformation, and modern acts cited in the dossier source map and timeline; and the official ecumenical texts used to qualify inherited labels.

Pseudo-Tertullian's *Adversus omnes haereses* and Theodoret's *Haereticarum fabularum compendium* remain comparison witnesses, not enumerative baselines: no checked individual extraction sufficient for an honest closed crosswalk was completed in this edition. Likewise, the corpus does not purport to enumerate every local accusation, prohibited book, disciplinary decree, or twentieth- and twenty-first-century notification. Those limits are part of the completion claim, not silent omissions.

## Baseline source registry

| Source key | Fixed corpus or source family | Census role | Present verification state |
|---|---|---|---|
| `HC.SRC.NT` | New Testament doctrinal boundaries | Apostolic doctrinal objects and responses | Exact loci used in §05 are mapped. |
| `HC.SRC.IREN` | Irenaeus, *Adversus haereses* I | Early named schools, genealogies, attributed propositions | Book/chapter routing below; critical SC collation outstanding. |
| `HC.SRC.HIPP` | Hippolytus or the author of the *Refutatio omnium haeresium* | Early schools and target fragments | Book-level routing below; authorship, chapter numbering, and critical text outstanding. |
| `HC.SRC.PSEUDOTERT` | Pseudo-Tertullian, *Adversus omnes haereses* | Comparison-only dependent Latin witness; outside the closed occurrence baseline | No checked individual extraction was completed; no completeness claim is made against this work. |
| `HC.SRC.EPIPH` | Epiphanius, *Panarion* 1–80 | Complete numbered occurrence census | All standard numbers routed below; GCS/Williams spelling and number collation outstanding. |
| `HC.SRC.PHIL` | Philastrius, *Diversarum hereseon liber* 1–156 | Complete numbered Latin occurrence census | CSEL 38 *Conspectus operis* ranges transcribed below; chapter text not line-collated. |
| `HC.SRC.AUG` | Augustine, *De haeresibus* 1–88 | Complete numbered Latin occurrence census | Standard headings routed below; CCSL text and dependence audit outstanding. |
| `HC.SRC.THEOD` | Theodoret, *Haereticarum fabularum compendium* I–IV | Comparison-only retrospective synthesis; outside the closed occurrence baseline | No checked book-level extraction was completed; no completeness claim is made against this work. |
| `HC.SRC.DAM` | John Damascene, *De haeresibus* 1–103 in the common modern numbering | Dependent epitome plus later additions | Ranges routed below; Kotter recension and 100/103 numbering problem outstanding. |
| `HC.SRC.COUNCILS` | Received ecumenical councils as cited in the dossier source map | Named groups, propositions, definitions, anathemas | Every council locus used by this bounded survey is mapped; no complete canon-by-canon extraction is claimed. |
| `HC.SRC.SYNODS` | Identified consequential regional synods and papally received local acts | Local or regionally received responses | Used acts are mapped with jurisdictional qualification; no exhaustive local-synod census is claimed. |
| `HC.SRC.PAPAL` | Identified papal letters, constitutions, decretals, professions, and bullaria | Proposition- and movement-level responses | Used acts are mapped; the corpus is not every papal rescript or investigation. |
| `HC.SRC.CANON` | Identified medieval canonical collections and inquisitorial records | Reception, procedure, and local classifications | Selective records used by the dossiers are mapped; no exhaustive trial census is claimed. |
| `HC.SRC.DH45` | Denzinger–Hünermann, 45th ed. | Finding index and standard paragraph cross-reference | Used only as a locator, never as the promulgating authority or an exhaustive register. |
| `HC.SRC.ASS-AAS` | *Acta Sanctae Sedis* and *Acta Apostolicae Sedis* | Official publication record from 1865 onward | The named acts used by the modern dossiers are mapped; no complete OCR sweep is claimed. |
| `HC.SRC.DDF` | Selected Holy Office/CDF/DDF documents through 2026-07-16 | Modern act genre and censure boundary | The documents represented in §80 are mapped, including the distinct SSPX response sequence of the 13 May warning, 29 June papal letter, and 2 July signed decree and note responding to the completed 1 July act; the disclosed exclusions deny an exhaustive notification census. |
| `HC.SRC.DIALOGUE` | Official common declarations and agreed ecumenical texts used in the prose | Later qualification of inherited labels | The Christological and Reformation aftermath texts used by the survey are mapped. |

## Normalized dossier-head ledger

The tables enumerate the completed normalized heads. `DOSSIER`, `ROUTED`, and `ERROR` describe the form of treatment, not a judgment that every attributed proposition is authentic or that every adherent was personally culpable. Exact LaTeX destination labels are fixed in the completion crosswalk below.

### Apostolic doctrinal boundary

| Key | Normalized object | Disposition | Seed anchors and unresolved boundary | Target |
|---|---|---|---|---|
| `HC.D.APO.JUDAIZING-NECESSITY` | Circumcision or Mosaic observance imposed as a condition of salvation for Gentiles | `DOSSIER` | Acts 15; Galatians; distinguish Jewish identity and voluntary observance from the necessity claim | §05 |
| `HC.D.APO.RESURRECTION-DENIAL` | Denial or evacuation of bodily resurrection | `DOSSIER` | 1 Corinthians 15; 2 Timothy 2:17–18; later spiritualizing systems require separate evidence | §05 |
| `HC.D.APO.INCARNATION-DENIAL` | Denial that Jesus Christ truly came in the flesh | `DOSSIER` | 1 John 4; 2 John 7; later Docetism is related but not projected into an apostolic trial | §05 |

### Second and third centuries

| Key | Normalized object | Disposition | Seed anchors and unresolved boundary | Target |
|---|---|---|---|---|
| `HC.D.EARLY.DOCETISM` | Docetic Christologies | `DOSSIER` | Ignatius and later refuters; distinguish an attributed tendency from one organized sect | §10 |
| `HC.D.EARLY.EBIONISM` | Ebionite currents | `DOSSIER` | Irenaeus, Origen, Epiphanius; taxonomy and internal diversity disputed | §10 |
| `HC.D.EARLY.CERINTHIANISM` | Teaching attributed to Cerinthus | `DOSSIER` | Irenaeus I.26; Eusebius; distinguish incompatible reports | §10 |
| `HC.D.EARLY.SIMONIANISM` | Simonian teaching | `DOSSIER` | Acts 8 is not itself a full account of the later school; Irenaeus I.23 and later catalogues | §10 |
| `HC.D.EARLY.MENANDRIANISM` | Menandrian teaching | `DOSSIER` | Irenaeus I.23 and dependent witnesses; target text lost | §10 |
| `HC.D.EARLY.SATURNILIANISM` | Saturnilus/Satornilus and attributed school | `DOSSIER` | Irenaeus I.24; later catalogues; spelling and genealogy vary | §10 |
| `HC.D.EARLY.BASILIDEANISM` | Basilides and Basilidean trajectories | `DOSSIER` | Irenaeus I.24, Hippolytus VII, Clement; sources describe different systems | §10 |
| `HC.D.EARLY.CARPOCRATIANISM` | Carpocratian teaching | `DOSSIER` | Irenaeus I.25; Clement; moral allegations need special caution | §10 |
| `HC.D.EARLY.GNOSTIC-CURRENTS` | Related ancient “Gnostic” currents as a comparative complex | `DOSSIER` | Irenaeus, Hippolytus, recovered texts; not one centrally governed church | §10 |
| `HC.D.EARLY.VALENTINIANISM` | Valentinus and Valentinian schools | `DOSSIER` | Irenaeus I.1–21; target-side fragments; schools remain separately aliased | §10 |
| `HC.D.EARLY.MARCIONISM` | Marcionite doctrine and church | `DOSSIER` | Tertullian, Irenaeus I.27, reconstructed *Antitheses* and gospel/apostolikon | §10 |
| `HC.D.EARLY.ENCRATISM` | Encratite and Tatian-associated rejection of marriage or created foods | `DOSSIER` | Irenaeus I.28; Tatian fragments; do not merge every ascetic rigorist | §10 |
| `HC.D.EARLY.ELCHASAITISM` | Elchasaite/Elkesai/Sampsaean currents | `ROUTED` | Hippolytus IX; Epiphanius 53; Jewish-Christian taxonomy disputed | §10 |
| `HC.D.EARLY.MONTANISM` | New Prophecy/Montanist trajectories | `DOSSIER` | Eusebius V; Epiphanius; original prophecy, rigor, and later doctrine require phases | §10 |
| `HC.D.EARLY.DYNAMIC-MONARCHIANISM` | Dynamic Monarchian or adoptionist Christologies | `DOSSIER` | Theodotus, Artemon, related Roman evidence; not Spanish Adoptionism | §10 |
| `HC.D.EARLY.PAUL-SAMOSATA` | Propositions attributed to Paul of Samosata | `ROUTED` | Antioch synods and Eusebius VII; act and terminology reconstruction required | §10/§20 |
| `HC.D.EARLY.MODALIST-MONARCHIANISM` | Noetian, Praxean, Patripassian, and Sabellian formulas | `DOSSIER` | Hippolytus IX, Tertullian, later synodal reception; aliases not perfectly coextensive | §10 |
| `HC.D.EARLY.NOVATIANISM` | Novatianist rigor, ecclesiology, and schism | `DOSSIER` | Cyprian and Cornelius; distinguish schism from doctrinal claims and later rebaptism | §10 |

### Fourth through sixth centuries

| Key | Normalized object | Disposition | Seed anchors and unresolved boundary | Target |
|---|---|---|---|---|
| `HC.D.PAT.DONATISM` | Donatist ecclesiology and sacramental claims | `DOSSIER` | African councils, Augustine, Collatio 411; coercion separately recorded | §20 |
| `HC.D.PAT.ARIANISM` | Arius and Arian trajectories | `DOSSIER` | Nicaea I, Arius fragments, later creeds; “Arian” not a timeless polemical synonym | §20 |
| `HC.D.PAT.ANOMOEANISM` | Aetian/Eunomian “unlike” theology | `DOSSIER` | Eunomius, Basil, Constantinople I canon 1; distinguish from all anti-Nicene formulas | §20 |
| `HC.D.PAT.PNEUMATOMACHIANISM` | Pneumatomachian/Macedonian denial concerning the Holy Spirit | `DOSSIER` | Constantinople I and Cappadocian witnesses; “Macedonian” attribution requires care | §20 |
| `HC.D.PAT.MARCELLIANISM` | Propositions associated with Marcellus of Ancyra | `ROUTED` | Fragmentary writings, councils, Constantinople I canon 1; development and retractions | §20 |
| `HC.D.PAT.PHOTINIANISM` | Photinus’s Christology | `ROUTED` | Sirmium and Constantinople I canon 1; relation to Paul of Samosata | §20 |
| `HC.D.PAT.APOLLINARIANISM` | Apollinarian denial of complete human rational soul/mind in Christ | `DOSSIER` | Apollinaris fragments, Roman synods, Constantinople I canon 1 | §20 |
| `HC.D.PAT.PRISCILLIANISM` | Propositions attributed to Priscillian and followers | `DOSSIER` | Extant tractates, synods, imperial trial; execution was civil and attribution contested | §20 |
| `HC.D.PAT.JOVINIANISM` | Propositions attributed to Jovinian | `DOSSIER` | Roman and Milanese responses; Jerome is an interested polemical witness | §20 |
| `HC.D.PAT.MESSALIANISM` | Messalian/Euchite propositions | `DOSSIER` | Synodal records, Theodoret, Ephesus-related reception; multiple lists and groups | §20 |
| `HC.D.PAT.PELAGIANISM` | Pelagian and Caelestian propositions on sin, grace, and freedom | `DOSSIER` | Carthage, Roman responses, Ephesus, target and Augustinian writings | §20 |
| `HC.D.PAT.SEMIPELAGIAN-CONTROVERSY` | Massilian propositions later called “Semi-Pelagian” | `DOSSIER` | Prosper, Cassian boundary, Orange II and papal reception; retrospective label | §20 |
| `HC.D.PAT.NESTORIAN-PROPOSITIONS` | Christological propositions condemned at Ephesus | `DOSSIER` | Cyril’s letters and anathematisms, Ephesus acts, Formula of Union; present Assyrian Church separately qualified | §20 |
| `HC.D.PAT.EUTYCHIANISM` | Eutyches’s condemned Christological formulations | `DOSSIER` | Constantinople 448, Robber Council context, Chalcedon; not a synonym for Oriental Orthodoxy | §20 |
| `HC.D.PAT.STRICT-MONOPHYSITE-FORMULAS` | Strict one-nature formulas incompatible with Chalcedon | `DOSSIER` | Chalcedon and later controversies; distinguish Cyrilline *mia physis* and modern agreements | §20 |
| `HC.D.PAT.ORIGENISM-FIRST` | First Origenist controversy and attributed propositions | `DOSSIER` | Origen’s extant works, Epiphanius, Jerome, Theophilus; attribution and translation limits | §20 |
| `HC.D.PAT.ORIGENISM-SIXTH` | Sixth-century Origenist propositions | `ROUTED` | 543 act and 553 context; provenance of the fifteen anathemas remains disputed | §20 |
| `HC.D.PAT.APOKATASTASIS-NECESSITATED` | Necessitated universal restoration or finite punishment propositions | `ROUTED` | Origenist and later loci; distinguish hope, speculation, and necessitated restoration | §20 |
| `HC.D.PAT.APHTHARTODOCETISM` | Julianist/Gaianite incorruptibility teaching | `DOSSIER` | Justinian-era sources and John Damascene 84; opponent-heavy evidence | §20 |
| `HC.D.PAT.AGNOETISM` | Themistian/Agnoete proposition concerning Christ’s human knowledge | `DOSSIER` | Gregory the Great and Greek witnesses; exact object and historical group require audit | §20 |
| `HC.D.PAT.TRITHEISM` | Tritheist formulations | `DOSSIER` | John Philoponus and sixth-century responses; do not infer from every use of “three” | §20 |

### Seventh through tenth centuries

| Key | Normalized object | Disposition | Seed anchors and unresolved boundary | Target |
|---|---|---|---|---|
| `HC.D.BYZ.MONENERGISM` | One-operation formula in Christ | `ROUTED` | *Ekthesis* prehistory, Lateran 649 and Constantinople III context | §30 |
| `HC.D.BYZ.MONOTHELITISM` | One-will formula in Christ | `DOSSIER` | Lateran 649, Constantinople III, papal confirmations; persons and formulas separately treated | §30 |
| `HC.D.BYZ.ICONOCLASM` | Rejection of the defined legitimacy of venerating sacred images | `DOSSIER` | Hieria context, Nicaea II, later restoration; worship and veneration distinguished | §30 |
| `HC.D.BYZ.SPANISH-ADOPTIONISM` | Elipandus/Felix-era Spanish Adoptionism | `DOSSIER` | Frankfurt and Carolingian sources; not dynamic Monarchianism | §30 |
| `HC.D.BYZ.LUCIDUS-PREDESTINATION` | Propositions retracted by Lucidus | `DOSSIER` | Arles/Lyon-era regional evidence; exact synodal authority to verify | §30 |
| `HC.D.BYZ.GOTTSCHALK-PREDESTINATION` | Gottschalk’s double-predestination controversy | `DOSSIER` | Mainz, Quierzy, Valence, target writings; mixed and contested reception | §30 |
| `HC.D.BYZ.PAULICIANISM` | Paulician movements and attributed dualist/Christological teaching | `DOSSIER` | Byzantine and Armenian witnesses; opponent-heavy and regionally diverse | §30 |

### Eleventh through thirteenth centuries

| Key | Normalized object | Disposition | Seed anchors and unresolved boundary | Target |
|---|---|---|---|---|
| `HC.D.MED.BOGOMILISM` | Bogomil movements | `DOSSIER` | Cosmas and Byzantine/Slavic witnesses; genealogy to western dualism not presumed | §40 |
| `HC.D.MED.BERENGARIANISM` | Berengar’s Eucharistic controversy | `DOSSIER` | Roman councils and professions of 1059/1079; development and recantations | §40 |
| `HC.D.MED.CATHARISM` | Cathar/Albigensian dualist movements | `DOSSIER` | Lateran III/IV, polemical and inquisitorial records; regional diversity and “Cathar” historiography | §40 |
| `HC.D.MED.TANCHELM` | Teaching attributed to Tanchelm | `DOSSIER` | Near-contemporary reports; formal doctrinal act and proposition recovery uncertain | §40 |
| `HC.D.MED.PETROBRUSIANS` | Petrobrusian teaching | `DOSSIER` | Peter the Venerable and regional evidence; opponent summary | §40 |
| `HC.D.MED.HENRICIANS` | Teaching attributed to Henry of Lausanne and followers | `ROUTED` | Bernard and regional evidence; relationship to Petrobrusians unresolved | §40 |
| `HC.D.MED.ARNOLDISTS` | Arnoldist teaching named in *Ad abolendam* | `DOSSIER` | Distinguish Arnold of Brescia’s politics, discipline, and attributed doctrine | §40 |
| `HC.D.MED.WALDENSIAN-ERRORS` | Early Poor of Lyon/Waldensian disputes and later doctrinal development | `DOSSIER` | *Ad abolendam*, professions, later confessions; unauthorized preaching is not by itself heresy | §40 |
| `HC.D.MED.HUMILIATI-FACTION` | Faction called Humiliati in *Ad abolendam* | `DOSSIER` | Do not apply the censure to the later approved order as a whole | §40 |
| `HC.D.MED.PASSAGIANS` | Passagian/Pasagian propositions | `DOSSIER` | *Ad abolendam* and later reports; sparse evidence | §40 |
| `HC.D.MED.JOSEPHINES` | Josephines named in *Ad abolendam* | `DOSSIER` | Name is securely listed; doctrinal identity remains open | §40 |
| `HC.D.MED.AMALRICIANISM` | Propositions associated with Amalric of Bène and followers | `DOSSIER` | Paris 1210/Lateran IV; trial reports and pantheist vocabulary require audit | §40 |
| `HC.D.MED.DAVID-DINANT` | Propositions attributed to David of Dinant | `ERROR` | Paris condemnations and surviving fragments; local academic act | §40 |
| `HC.D.MED.JOACHIM-TRINITY` | Trinitarian proposition condemned from Joachim’s work | `ERROR` | Lateran IV both condemns the proposition/book and protects Joachim’s monastery and submission | §40 |
| `HC.D.MED.RADICAL-JOACHIMISM` | Later radical Joachimite claims | `DOSSIER` | Distinguish Joachim, later pseudonymous texts, and Spiritual reception | §40/§50 |
| `HC.D.MED.ABELARD-PROPOSITIONS` | Propositions censured in Abelard’s cases | `ERROR` | Soissons/Sens, correspondence, papal confirmation; not a stable “Abelardian church” | §40 |
| `HC.D.MED.GILBERT-POITIERS` | Gilbert of Poitiers controversy | `ERROR` | Reims 1148 and disputed formulae; final status requires exact act audit | §40 |
| `HC.D.MED.LATIN-AVERROIST-ERRORS` | One-intellect, eternity, and related Latin Aristotelian propositions | `ERROR` | Paris 1270/1277 and Lateran V; local syllabi and later universal act kept distinct | §40/§50 |
| `HC.D.MED.APOSTOLIC-BRETHREN` | Apostolic Brethren and Dolcinian development | `DOSSIER` | Papal and inquisitorial sources; phases and apocalyptic claims | §40/§50 |
| `HC.D.MED.FREE-SPIRIT` | Propositions grouped under “Free Spirit” | `DOSSIER` | Vienne and local records; modern umbrella may exaggerate unity | §40/§50 |
| `HC.D.MED.VIENNE-BEGUARD-ERRORS` | Eight errors attributed to certain Beguards and Beguines | `ERROR` | Vienne, *Ad nostrum*; never generalized to all Beguines | §40/§50 |

### Fourteenth and fifteenth centuries

| Key | Normalized object | Disposition | Seed anchors and unresolved boundary | Target |
|---|---|---|---|---|
| `HC.D.MED.FRATICELLI` | Fraticelli movements | `DOSSIER` | Multiple factions and acts; not all Spiritual Franciscans | §50 |
| `HC.D.MED.ABSOLUTE-POVERTY` | Proposition that Christ and the apostles possessed nothing individually or in common | `ERROR` | John XXII, *Cum inter nonnullos*; distinguish doctrine, Franciscan obedience, and politics | §50 |
| `HC.D.MED.MARSILIANISM` | Propositions extracted from Marsilius of Padua | `ERROR` | *Licet iuxta doctrinam* and *Defensor pacis*; censure wording requires exact collation | §50 |
| `HC.D.MED.VIENNE-SOUL-FORM` | Denial that the rational or intellectual soul is per se and essentially the form of the body | `ERROR` | Council of Vienne; anonymous contradictory rather than named movement | §50 |
| `HC.D.MED.ECKHART-PROPOSITIONS` | Propositions from Meister Eckhart’s works | `ERROR` | *In agro dominico*: individual grades and Eckhart’s protest/submission must be retained | §50 |
| `HC.D.MED.WYCLIFFISM` | Wyclif’s attributed and censured propositions | `DOSSIER` | Oxford, Roman, and Constance materials; extraction and mixed censures | §50 |
| `HC.D.MED.LOLLARDY` | English Lollard receptions | `DOSSIER` | Conclusions, episcopal proceedings, civil statutes; not identical with every Wyclif proposition | §50 |
| `HC.D.MED.HUSSITISM` | Hus and Hussite doctrinal complexes | `DOSSIER` | Constance, target writings, later Bohemian developments; ecclesial and civil actions separated | §50 |
| `HC.D.MED.UTRAQUISM` | Necessity claims and discipline surrounding communion under both kinds | `DOSSIER` | Constance and later Compactata; practice alone is not the whole doctrinal object | §50 |
| `HC.D.MED.TABORITISM` | Taborite doctrinal and apocalyptic currents | `ROUTED` | Bohemian sources; distinguish political coalition from propositions | §50 |
| `HC.D.MED.RADICAL-CONCILIARISM` | Claim that a council is categorically superior to the pope in the relevant radical sense | `ERROR` | Constance session/reception disputes, *Execrabilis*, Lateran V, Vatican I | §50 |
| `HC.D.MED.LATERAN-V-SOUL` | Soul mortality or one-soul-for-all propositions answered at Lateran V | `ERROR` | *Apostolici regiminis*; relation to “Averroism” must not be assumed in every case | §50 |

### Sixteenth-century Reformations

| Key | Normalized object | Disposition | Seed anchors and unresolved boundary | Target |
|---|---|---|---|---|
| `HC.D.REF.LUTHER-PROPOSITIONS` | Propositions censured in *Exsurge Domine* and related acts | `ERROR` | Mixed censure in globo; Luther’s writings and procedural history required | §60 |
| `HC.D.REF.LUTHERAN-CONFESSIONS` | Lutheran confessional doctrines in Catholic comparison | `DOSSIER` | Augsburg Confession, Book of Concord, Trent, 1999 JDDJ; no judgment of descendants’ culpability | §60 |
| `HC.D.REF.SACRAMENTARIANISM` | Zwinglian and related “Sacramentarian” Eucharistic positions | `DOSSIER` | Target writings and Catholic sacramental definitions; label varies polemically | §60 |
| `HC.D.REF.REFORMED-DOCTRINES` | Reformed/Calvinist doctrinal complex in Catholic comparison | `DOSSIER` | Calvin and confessions, Trent and later responses; not one personally culpable subject | §60 |
| `HC.D.REF.ANABAPTIST-CURRENTS` | Heterogeneous Anabaptist teachings | `DOSSIER` | Schleitheim and other target witnesses; do not impute one radical group’s claims to all | §60 |
| `HC.D.REF.SCHWENCKFELDIANISM` | Schwenckfeldian teaching | `ROUTED` | Target writings and local responses; universal Catholic censure anchor unresolved | §60 |
| `HC.D.REF.RADICAL-SPIRITUALISM` | Radical Spiritualist and Familist currents | `DOSSIER` | Several distinct movements; may split after source sweep | §60 |
| `HC.D.REF.SERVETIAN-ANTITRINITARIANISM` | Servetus’s anti-Trinitarian propositions | `ROUTED` | Target texts; Catholic and Reformed judgments distinguished | §60 |
| `HC.D.REF.SOCINIANISM` | Socinian and early Unitarian trajectories | `DOSSIER` | Racovian and other target texts; later Unitarianism not automatically identical | §60 |
| `HC.D.REF.ANGLICAN-FORMULARIES` | English Reformation formularies in Catholic comparison | `DOSSIER` | Thirty-Nine Articles and Catholic responses; Anglicanism is not one personal verdict | §60 |

### Post-Reformation controversies

| Key | Normalized object | Disposition | Seed anchors and unresolved boundary | Target |
|---|---|---|---|---|
| `HC.D.POST.BAIANISM` | Propositions associated with Michael Baius | `ERROR` | *Ex omnibus afflictionibus* and later clarification; proposition numbering/grades | §70 |
| `HC.D.POST.JANSENISM` | Five propositions and the Jansenist grace controversy | `ERROR` | *Augustinus*, *Cum occasione*, later acts; text/fact distinction | §70 |
| `HC.D.POST.JANSENIST-FACT-SILENCE` | “Fact,” right, and respectful-silence controversy | `ERROR` | *Ad sanctam beati Petri sedem*, *Vineam Domini*; not a separate ancient-style sect | §70 |
| `HC.D.POST.QUESNELLISM` | Quesnel’s propositions | `ERROR` | *Unigenitus*; collective qualifications may not be assigned indiscriminately to each sentence | §70 |
| `HC.D.POST.MOLINOS-QUIETISM` | Molinos’s Quietist propositions | `ERROR` | *Coelestis Pastor*; target context and individual censure language | §70 |
| `HC.D.POST.FENELON-PROPOSITIONS` | Fénelon’s condemned “pure love” propositions | `ERROR` | *Cum alias*; submission and censure grades must be preserved | §70 |
| `HC.D.POST.RICHERISM` | Richerist ecclesiological propositions | `ERROR` | University, episcopal, and Roman responses need jurisdiction audit | §70 |
| `HC.D.POST.GALLICAN-ARTICLES` | Four Gallican Articles of 1682 | `ERROR` | Assembly act and papal responses; political and theological aspects | §70 |
| `HC.D.POST.FEBRONIANISM` | Febronian ecclesiology | `ERROR` | *Justinus Febronius*, episcopal/Roman reception; exact universal act anchor | §70 |
| `HC.D.POST.JOSEPHINISM` | Josephinist church-state and doctrinal program | `ERROR` | Mixed political, administrative, and doctrinal object; may remain contextual | §70 |
| `HC.D.POST.PISTOIA` | Propositions of the Synod of Pistoia | `ERROR` | *Auctorem fidei* assigns distinct proposition-level grades | §70 |
| `HC.D.POST.LAXIST-PROPOSITIONS` | Seventeenth-century condemned laxist moral propositions | `ERROR` | Alexander VII/Innocent XI lists; not one named heresy | §70 |
| `HC.D.POST.RIGORIST-PROPOSITIONS` | Condemned rigorist moral or sacramental propositions | `ERROR` | Exact acts and relation to Jansenism require item-level audit | §70 |
| `HC.D.POST.ALUMBRADO-PROPOSITIONS` | Propositions attributed to particular Alumbrado groups | `ERROR` | Local Spanish inquisitorial records; heterogeneous and jurisdiction-limited | §70 |

### Modern and contemporary

| Key | Normalized object | Disposition | Seed anchors and unresolved boundary | Target |
|---|---|---|---|---|
| `HC.D.MOD.RATIONALISM-NATURALISM` | Rationalist and naturalist proposition complexes | `ERROR` | *Dei Filius*, antecedent acts, exact proposition families; not every use of reason | §80 |
| `HC.D.MOD.PANTHEISM-MATERIALISM` | Pantheist and materialist propositions answered by Vatican I | `ERROR` | *Dei Filius* canons; distinguish external philosophies from baptized denial | §80 |
| `HC.D.MOD.FIDEISM-TRADITIONALISM` | Fideist and philosophical Traditionalist errors about reason and faith | `ERROR` | Bautain, Bonnetty, Vatican I; not contemporary Catholic traditionalism | §80 |
| `HC.D.MOD.HERMESIANISM` | Hermesian propositions | `ERROR` | Gregory XVI and later Roman acts; exact extracted propositions | §80 |
| `HC.D.MOD.GUNTHERIANISM` | Güntherian propositions | `ERROR` | Pius IX acts; philosophical system and formal censure distinguished | §80 |
| `HC.D.MOD.ONTOLOGISM` | Ontologist propositions | `ERROR` | Holy Office decree and later reception; exact seven-proposition text | §80 |
| `HC.D.MOD.INDIFFERENTISM-LIBERALISM` | Religious indifferentist and doctrinal-liberal propositions | `ERROR` | *Mirari vos*, *Quanta cura*, source acts behind the *Syllabus*; political senses distinguished | §80 |
| `HC.D.MOD.ROSMINI-PROPOSITIONS` | Forty propositions condemned in *Post obitum* | `ERROR` | 2001 CDF note: condemned reading remains objectively rejected but is not Rosmini’s authentic position | §80 |
| `HC.D.MOD.OLD-CATHOLIC-VATICAN-I` | Rejection of Vatican I definitions in the Old Catholic separation | `DOSSIER` | Vatican I and subsequent professions/acts; schism and proposition kept distinct | §80 |
| `HC.D.MOD.AMERICANISM` | Tendencies conditionally rejected under the name “Americanism” | `ERROR` | *Testem benevolentiae* is conditional and expresses confidence in the U.S. bishops | §80 |
| `HC.D.MOD.MODERNISM` | Propositions and synthesis addressed by *Lamentabili* and *Pascendi* | `ERROR` | Exact proposition list and encyclical synthesis; later generic polemical use excluded | §80 |
| `HC.D.MOD.HUMANI-GENERIS-ERRORS` | Specific unsafe or erroneous opinions treated in *Humani generis* | `ERROR` | Does not make evolution or every contemporary school a named heresy | §80 |
| `HC.D.MOD.MILLENARIANISM` | Millenarian and mitigated-millenarian propositions | `ERROR` | Early chiliastic diversity and 1944 Holy Office response kept distinct | §80 |
| `HC.D.MOD.FEENEY-ERROR` | Restrictive interpretation associated with Leonard Feeney | `ERROR` | *Suprema haec sacra*, canonical history, reconciliation; “Feeneyism” is shorthand | §80 |
| `HC.D.MOD.SITUATION-ETHICS` | Situation ethics as a Catholic moral method | `ERROR` | Holy Office instruction of 2 February 1956; prohibited method, not formally graded “heresy” | §80 |
| `HC.D.MOD.CDF-1966-ERRORS` | Errors catalogued in the 1966 CDF circular letter | `ERROR` | Anonymous proposition clusters, not a new named sect | §80 |
| `HC.D.MOD.LIBERATION-THEOLOGY-ERRORS` | Propositions corrected in Roman instructions or notifications concerning liberation theologies | `ERROR` | Multiple schools and act genres; “liberation theology” not condemned wholesale | §80 |
| `HC.D.MOD.WOMENS-ORDINATION` | Thesis that the Church can confer priestly ordination on women | `ERROR` | *Ordinatio sacerdotalis* and the 1995 responsum; definitive second-paragraph teaching, not automatically canonical heresy | §80 |
| `HC.D.MOD.RELIGIOUS-PLURALISM` | Relativist theses concerning revelation, Christ, the Church, and religions | `ERROR` | *Dominus Iesus* 5–22; several propositions contrary to Catholic faith, without one penal finding against every author | §80 |

## Exact completion crosswalk for normalized heads

This table is controlling for prose destination. Every `HC.D` key above appears exactly once below. A row may contain several keys only when the named four-field dossier deliberately treats them together.

| Section and exact destination label | Normalized heads and completion disposition |
|---|---|
| §05, `dossier:judaizing` | `HC.D.APO.JUDAIZING-NECESSITY` — `DOSSIER` |
| §05, `dossier:resurrection-denial` | `HC.D.APO.RESURRECTION-DENIAL` — `DOSSIER` |
| §05, `dossier:incarnation-denial` | `HC.D.APO.INCARNATION-DENIAL` — `DOSSIER` |
| §10, `dossier:simonianism` | `HC.D.EARLY.SIMONIANISM` — `DOSSIER` |
| §10, `dossier:cerinthianism` | `HC.D.EARLY.CERINTHIANISM` — `DOSSIER` |
| §10, `dossier:docetism` | `HC.D.EARLY.DOCETISM` — `DOSSIER` |
| §10, `dossier:ebionites-elchasaites` | `HC.D.EARLY.EBIONISM` — `DOSSIER`; `HC.D.EARLY.ELCHASAITISM` — `ROUTED` |
| §10, `dossier:menandrianism` | `HC.D.EARLY.MENANDRIANISM` — `DOSSIER` |
| §10, `dossier:saturnilianism` | `HC.D.EARLY.SATURNILIANISM` — `DOSSIER` |
| §10, `dossier:basilideanism` | `HC.D.EARLY.BASILIDEANISM` — `DOSSIER` |
| §10, `dossier:carpocratianism` | `HC.D.EARLY.CARPOCRATIANISM` — `DOSSIER` |
| §10, `dossier:valentinianism` | `HC.D.EARLY.VALENTINIANISM` — `DOSSIER` |
| §10, `dossier:gnostic-schools` | `HC.D.EARLY.GNOSTIC-CURRENTS` — `DOSSIER` |
| §10, `dossier:marcionism` | `HC.D.EARLY.MARCIONISM` — `DOSSIER` |
| §10, `dossier:montanism` | `HC.D.EARLY.MONTANISM` — `DOSSIER` |
| §10, `dossier:encratism` | `HC.D.EARLY.ENCRATISM` — `DOSSIER` |
| §10, `dossier:modal-monarchianism` | `HC.D.EARLY.MODALIST-MONARCHIANISM` — `DOSSIER` |
| §10, `dossier:dynamic-monarchianism` | `HC.D.EARLY.DYNAMIC-MONARCHIANISM` — `DOSSIER`; `HC.D.EARLY.PAUL-SAMOSATA` — `ROUTED` |
| §10, `dossier:novatianism` | `HC.D.EARLY.NOVATIANISM` — `DOSSIER` |
| §20, `dossier:donatism` | `HC.D.PAT.DONATISM` — `DOSSIER` |
| §20, `dossier:jovinianism` | `HC.D.PAT.JOVINIANISM` — `DOSSIER` |
| §20, `dossier:strict-one-nature-formulas` | `HC.D.PAT.STRICT-MONOPHYSITE-FORMULAS` — `DOSSIER` |
| §20, `dossier:aphthartodocetism` | `HC.D.PAT.APHTHARTODOCETISM` — `DOSSIER` |
| §20, `dossier:agnoetism` | `HC.D.PAT.AGNOETISM` — `DOSSIER` |
| §20, `dossier:tritheism` | `HC.D.PAT.TRITHEISM` — `DOSSIER` |
| §20, `dossier:arianism` | `HC.D.PAT.ARIANISM` — `DOSSIER` |
| §20, `dossier:eunomianism` | `HC.D.PAT.ANOMOEANISM` — `DOSSIER` |
| §20, `dossier:pneumatomachi` | `HC.D.PAT.PNEUMATOMACHIANISM` — `DOSSIER` |
| §20, `dossier:apollinarian-marcellian-photinian` | `HC.D.PAT.APOLLINARIANISM` — `DOSSIER`; `HC.D.PAT.MARCELLIANISM` and `HC.D.PAT.PHOTINIANISM` — `ROUTED` |
| §20, `dossier:priscillianism` | `HC.D.PAT.PRISCILLIANISM` — `DOSSIER` |
| §20, `dossier:pelagianism` | `HC.D.PAT.PELAGIANISM` — `DOSSIER` |
| §20, `dossier:semi-pelagianism-orange` | `HC.D.PAT.SEMIPELAGIAN-CONTROVERSY` — `DOSSIER` |
| §20, `dossier:nestorian-controversy` | `HC.D.PAT.NESTORIAN-PROPOSITIONS` — `DOSSIER` |
| §20, `dossier:messalianism` | `HC.D.PAT.MESSALIANISM` — `DOSSIER` |
| §20, `dossier:eutychianism-chalcedon` | `HC.D.PAT.EUTYCHIANISM` — `DOSSIER` |
| §20, `dossier:origenism` | `HC.D.PAT.ORIGENISM-FIRST` — `DOSSIER`; `HC.D.PAT.ORIGENISM-SIXTH` and `HC.D.PAT.APOKATASTASIS-NECESSITATED` — `ROUTED` |
| §30, `dossier:monothelitism` | `HC.D.BYZ.MONOTHELITISM` — `DOSSIER`; `HC.D.BYZ.MONENERGISM` — `ROUTED` |
| §30, `dossier:lucidus-predestination` | `HC.D.BYZ.LUCIDUS-PREDESTINATION` — `DOSSIER` |
| §30, `dossier:iconoclasm` | `HC.D.BYZ.ICONOCLASM` — `DOSSIER` |
| §30, `dossier:spanish-adoptionism` | `HC.D.BYZ.SPANISH-ADOPTIONISM` — `DOSSIER` |
| §30, `dossier:paulicians` | `HC.D.BYZ.PAULICIANISM` — `DOSSIER` |
| §30, `dossier:gottschalk-predestination` | `HC.D.BYZ.GOTTSCHALK-PREDESTINATION` — `DOSSIER` |
| §30, `dossier:bogomilism` | `HC.D.MED.BOGOMILISM` — `DOSSIER` |
| §40, `dossier:tanchelm` | `HC.D.MED.TANCHELM` — `DOSSIER` |
| §40, `dossier:passagians` | `HC.D.MED.PASSAGIANS` — `DOSSIER` |
| §40, `dossier:josephines` | `HC.D.MED.JOSEPHINES` — `DOSSIER` |
| §40, `dossier:david-dinant` | `HC.D.MED.DAVID-DINANT` — `ERROR` |
| §40, `dossier:radical-joachimism` | `HC.D.MED.RADICAL-JOACHIMISM` — `DOSSIER` |
| §40, `dossier:abelard-propositions` | `HC.D.MED.ABELARD-PROPOSITIONS` — `ERROR` |
| §40, `dossier:gilbert-poitiers` | `HC.D.MED.GILBERT-POITIERS` — `ERROR` |
| §40, `dossier:berengar` | `HC.D.MED.BERENGARIANISM` — `DOSSIER` |
| §40, `dossier:petrobrusians-henricians` | `HC.D.MED.PETROBRUSIANS` — `DOSSIER`; `HC.D.MED.HENRICIANS` — `ROUTED` |
| §40, `dossier:cathars` | `HC.D.MED.CATHARISM` — `DOSSIER` |
| §40, `dossier:waldensians` | `HC.D.MED.WALDENSIAN-ERRORS` — `DOSSIER` |
| §40, `dossier:arnoldists` | `HC.D.MED.ARNOLDISTS` — `DOSSIER` |
| §40, `dossier:humiliati` | `HC.D.MED.HUMILIATI-FACTION` — `DOSSIER` |
| §40, `dossier:amalricians` | `HC.D.MED.AMALRICIANISM` — `DOSSIER` |
| §40, `dossier:joachim-fiore` | `HC.D.MED.JOACHIM-TRINITY` — `ERROR` |
| §40, `dossier:apostolics-dolcinians` | `HC.D.MED.APOSTOLIC-BRETHREN` — `DOSSIER` |
| §40, `dossier:paris-condemnations` | `HC.D.MED.LATIN-AVERROIST-ERRORS` — `ERROR` |
| §50, `dossier:beguards-beguines` | `HC.D.MED.FREE-SPIRIT` — `DOSSIER`; `HC.D.MED.VIENNE-BEGUARD-ERRORS` — `ERROR` |
| §50, `dossier:vienne-soul-form` | `HC.D.MED.VIENNE-SOUL-FORM` — `ERROR` |
| §50, `dossier:eckhart-propositions` | `HC.D.MED.ECKHART-PROPOSITIONS` — `ERROR` |
| §50, `dossier:lateran-v-soul` | `HC.D.MED.LATERAN-V-SOUL` — `ERROR` |
| §50, `dossier:spiritual-franciscans` | `HC.D.MED.FRATICELLI` — `DOSSIER`; `HC.D.MED.ABSOLUTE-POVERTY` — `ERROR` |
| §50, `dossier:marsilius-jandun` | `HC.D.MED.MARSILIANISM` — `ERROR` |
| §50, `dossier:wyclif` | `HC.D.MED.WYCLIFFISM` — `DOSSIER` |
| §50, `dossier:lollardy` | `HC.D.MED.LOLLARDY` — `DOSSIER` |
| §50, `dossier:hus` | `HC.D.MED.HUSSITISM` — `DOSSIER` |
| §50, `dossier:hussites-utraquists` | `HC.D.MED.UTRAQUISM` — `DOSSIER`; `HC.D.MED.TABORITISM` — `ROUTED` |
| §50, `dossier:conciliarism` | `HC.D.MED.RADICAL-CONCILIARISM` — `ERROR` |
| §60, `dossier:luther-exsurge` | `HC.D.REF.LUTHER-PROPOSITIONS` — `ERROR` |
| §60, `dossier:lutheran-confessional-axis` | `HC.D.REF.LUTHERAN-CONFESSIONS` — `DOSSIER` |
| §60, `dossier:zwinglian-axis` | `HC.D.REF.SACRAMENTARIANISM` — `DOSSIER` |
| §60, `dossier:reformed-axis` | `HC.D.REF.REFORMED-DOCTRINES` — `DOSSIER` |
| §60, `dossier:anabaptist-axis` | `HC.D.REF.ANABAPTIST-CURRENTS` — `DOSSIER` |
| §60, `dossier:anglican-axis` | `HC.D.REF.ANGLICAN-FORMULARIES` — `DOSSIER` |
| §60, `dossier:radical-spiritualist-axis` | `HC.D.REF.RADICAL-SPIRITUALISM` — `DOSSIER`; `HC.D.REF.SCHWENCKFELDIANISM` — `ROUTED` |
| §60, `dossier:socinian-axis` | `HC.D.REF.SOCINIANISM` — `DOSSIER`; `HC.D.REF.SERVETIAN-ANTITRINITARIANISM` — `ROUTED` |
| §70, `dossier:alumbrado-propositions` | `HC.D.POST.ALUMBRADO-PROPOSITIONS` — `ERROR` |
| §70, `dossier:baianism` | `HC.D.POST.BAIANISM` — `ERROR` |
| §70, `dossier:richerism` | `HC.D.POST.RICHERISM` — `ERROR` |
| §70, `dossier:jansenism-five-propositions` | `HC.D.POST.JANSENISM` and `HC.D.POST.JANSENIST-FACT-SILENCE` — `ERROR` |
| §70, `dossier:laxist-propositions` | `HC.D.POST.LAXIST-PROPOSITIONS` — `ERROR` |
| §70, `dossier:quesnel-unigenitus` | `HC.D.POST.QUESNELLISM` — `ERROR` |
| §70, `dossier:molinos-quietism` | `HC.D.POST.MOLINOS-QUIETISM` — `ERROR` |
| §70, `dossier:gallican-articles` | `HC.D.POST.GALLICAN-ARTICLES` — `ERROR` |
| §70, `dossier:rigorist-propositions` | `HC.D.POST.RIGORIST-PROPOSITIONS` — `ERROR` |
| §70, `dossier:fenelon-pure-love` | `HC.D.POST.FENELON-PROPOSITIONS` — `ERROR` |
| §70, `dossier:febronian-josephin-boundary` | `HC.D.POST.FEBRONIANISM` and `HC.D.POST.JOSEPHINISM` — `ERROR` |
| §70, `dossier:pistoia` | `HC.D.POST.PISTOIA` — `ERROR` |
| §80, `dossier:indifferentism-naturalism` | `HC.D.MOD.INDIFFERENTISM-LIBERALISM` — `ERROR` |
| §80, `dossier:hermesianism` | `HC.D.MOD.HERMESIANISM` — `ERROR` |
| §80, `dossier:fideism-traditionalism` | `HC.D.MOD.FIDEISM-TRADITIONALISM` — `ERROR` |
| §80, `dossier:guntherianism` | `HC.D.MOD.GUNTHERIANISM` — `ERROR` |
| §80, `dossier:ontologism` | `HC.D.MOD.ONTOLOGISM` — `ERROR` |
| §80, `dossier:vatican-i-modern-systems` | `HC.D.MOD.RATIONALISM-NATURALISM` and `HC.D.MOD.PANTHEISM-MATERIALISM` — `ERROR` |
| §80, `dossier:old-catholics` | `HC.D.MOD.OLD-CATHOLIC-VATICAN-I` — `DOSSIER` |
| §80, `dossier:rosmini-post-obitum` | `HC.D.MOD.ROSMINI-PROPOSITIONS` — `ERROR` |
| §80, `dossier:americanism` | `HC.D.MOD.AMERICANISM` — `ERROR` |
| §80, `dossier:modernism` | `HC.D.MOD.MODERNISM` — `ERROR` |
| §80, `dossier:millenarianism-1944` | `HC.D.MOD.MILLENARIANISM` — `ERROR` |
| §80, `dossier:feeneyism` | `HC.D.MOD.FEENEY-ERROR` — `ERROR` |
| §80, `dossier:humani-generis-errors` | `HC.D.MOD.HUMANI-GENERIS-ERRORS` — `ERROR` |
| §80, `dossier:situation-ethics` | `HC.D.MOD.SITUATION-ETHICS` — `ERROR` |
| §80, `dossier:postconciliar-error-inventory` | `HC.D.MOD.CDF-1966-ERRORS` — `ERROR` |
| §80, `dossier:liberation-theology` | `HC.D.MOD.LIBERATION-THEOLOGY-ERRORS` — `ERROR` |
| §80, `dossier:womens-ordination` | `HC.D.MOD.WOMENS-ORDINATION` — `ERROR` |
| §80, `dossier:religious-pluralism` | `HC.D.MOD.RELIGIOUS-PLURALISM` — `ERROR` |

## Source-limited notice ledger

These labels are enumerated so that obscurity does not become silent omission. A notice is not an endorsement of the catalogue’s genealogy, moral allegations, or claim that an organized group existed exactly as described. All fifty-five completed records are printed in the “Census Notices for Obscure or Source-Limited Labels” appendix, `app:census-notices`; that table supplies the attributed object, attestation or response, aftermath or inability to trace one, and evidence limit. The controlling rows below fix the label and route.

| Key | Label or attributed object | Disposition and routing | Principal limit |
|---|---|---|---|
| `HC.N.EARLY.NICOLAITANS` | Nicolaitans | `NOTICE`; related to §05/§10 | Revelation supplies a name but later founder stories and practices conflict. |
| `HC.N.EARLY.BORBORITES` | Borborites/Phibionites/Stratiotics and related labels | `NOTICE`; compare `HC.D.EARLY.GNOSTIC-CURRENTS` | Sensational moral allegations are largely opponent testimony. |
| `HC.N.EARLY.OPHITES` | Ophites/Naassenes as catalogue groupings | `NOTICE`; compare Gnostic currents | Ancient and modern taxonomies do not align neatly. |
| `HC.N.EARLY.CAINITES` | Cainites/Caiani | `NOTICE`; compare Gnostic currents | Known principally from refuters. |
| `HC.N.EARLY.SETHIANS` | Sethians | `NOTICE`; compare Gnostic currents | Modern “Sethian” textual taxonomy is not simply Epiphanius’s sect. |
| `HC.N.EARLY.ARCHONTICS` | Archontics | `NOTICE`; compare Gnostic currents | Opponent-heavy evidence. |
| `HC.N.EARLY.LUCIANISTS` | Pre-Constantinian Lucianists in Epiphanius | `NOTICE`; route near Marcionism | Do not confuse with Lucian of Antioch. |
| `HC.N.EARLY.APELLEANS` | Apelleans | `NOTICE`; route near Marcionism | Apelles’s relation to Marcion and target fragments require care. |
| `HC.N.EARLY.SEVERIANS` | Severians associated with Encratism | `NOTICE`; route near Encratism | Do not confuse with Severus of Antioch. |
| `HC.N.EARLY.ALOGI` | Alogi/Alogians | `NOTICE` | Opponent label for rejection of Johannine writings or Logos theology. |
| `HC.N.EARLY.ADAMITES` | Adamites/Adamians | `NOTICE` | Sparse and polemical evidence; later reuse of name is not descent. |
| `HC.N.EARLY.MELCHIZEDEKIANS` | Melchizedekians | `NOTICE`; compare dynamic Monarchianism | Several distinct claims occur under the label. |
| `HC.N.EARLY.BARDESANISTS` | Bardesanists | `NOTICE` | Bardaisan’s own position and later school reports differ. |
| `HC.N.EARLY.VALESIANS` | Valesians | `NOTICE` | Source-limited ascetic/castration report. |
| `HC.N.EARLY.ANGELICS` | Angelici | `NOTICE` | Augustine and Epiphanius admit uncertainty about the name. |
| `HC.N.EARLY.APOTACTICS` | Apostolics/Apotactics | `NOTICE`; compare Encratism | Renunciation practice alone does not establish all attributed doctrine. |
| `HC.N.EARLY.ORIGENISTS-OBSCENE` | “Origenists” of Epiphanius 63/Augustine 42 | `NOTICE` | Explicitly distinct from followers of Origen Adamantius; historicity uncertain. |
| `HC.N.EARLY.HIERACITES` | Hieracites | `NOTICE` | Known largely through catalogues and refutation. |
| `HC.N.PAT.AUDIANS` | Audians/Anthropomorphites | `NOTICE` | Epiphanius calls the initial object schism and reports later doctrinal errors. |
| `HC.N.PAT.HOMOIOUSIAN-TRAJECTORIES` | Homoiousians/“Semi-Arians” | `NOTICE`; compare Arianism | Retrospective umbrella; many persons and formulas moved toward Nicene settlement. |
| `HC.N.PAT.AERIANS` | Aerians | `NOTICE` | Discipline, hierarchy, prayer for the dead, and Paschal claims are mixed. |
| `HC.N.PAT.ANTIDICOMARIANITES` | Antidicomarianites | `NOTICE` | Epiphanian label; distinguish Helvidius and later debates. |
| `HC.N.PAT.COLLYRIDIANS` | Collyridians | `NOTICE` | Epiphanius is effectively the sole substantive witness; historicity and scale uncertain. |
| `HC.N.PAT.HELVIDIANS` | Helvidians | `NOTICE` | Jerome is the main witness; no extant universal sentence identified yet. |
| `HC.N.PAT.BONOSIANS` | Bonosians | `NOTICE` | Marian, Christological, and later adoptionist attributions need separation. |
| `HC.N.PAT.VIGILANTIUS` | Propositions attributed to Vigilantius | `NOTICE` | Jerome’s refutation dominates; no checked formal act is identified in the disclosed sources. |
| `HC.N.PAT.METANGISMONITES` | Metangismonites | `NOTICE` | Catalogue-defined spatial metaphor for Son in Father; group historicity unclear. |
| `HC.N.PAT.SELEUCIANS-HERMIANS` | Seleucians/Hermians | `NOTICE` | Late catalogue reports combine cosmological claims. |
| `HC.N.PAT.PROCLIANS-HERMEONITES` | Proclians/Hermeonites | `NOTICE` | Source identity and relation to Seleucians unresolved. |
| `HC.N.PAT.PATRICIANS` | Patricians | `NOTICE` | Catalogue label for anti-creator proposition; not medieval St Patrick. |
| `HC.N.PAT.ASCITAE` | Ascitae | `NOTICE` | Ritual report principally preserved in catalogue tradition. |
| `HC.N.PAT.PASSALORHYNCHITES` | Passalorhynchites/Tascodrugite-related “peg-nose” ascetics | `NOTICE` | Names and relationship vary across catalogues. |
| `HC.N.PAT.AQUARIANS` | Aquarians/Hydroparastatae | `NOTICE` | Water-only Eucharistic practice; doctrinal inference requires care. |
| `HC.N.PAT.COLUTHIANS` | Coluthians | `NOTICE` | Catalogue occurrence may derive from a local schism/ordination dispute. |
| `HC.N.PAT.FLORINIANS` | Florinians | `NOTICE` | Relation to Florinus, Carpocratians, or “milites” differs by source. |
| `HC.N.PAT.RHETORIANS` | Rhetorians | `NOTICE` | Reported as praising all heresies; very thin evidence. |
| `HC.N.PAT.ARABICI` | Arabici | `NOTICE` | Reported soul-death controversy; Origen’s conference is the main narrative. |
| `HC.N.PAT.PATERNIANS` | Paternians/Venustians | `NOTICE` | Augustine’s concise opponent report is principal witness. |
| `HC.N.PAT.TERTULLIANISTS` | Tertullianists at Carthage | `NOTICE` | Augustine reports a separate remnant later reconciled; relation to Tertullian’s own development requires care. |
| `HC.N.PAT.ABELONIANS` | Abelonians/Abeloites | `NOTICE` | Source-limited ascetic group reported by Augustine. |
| `HC.N.PAT.BARSANOUPHITES` | Barsanouphites/Semidalites | `NOTICE` | John Damascene’s later catalogue is the principal routing witness. |
| `HC.N.PAT.HICETAE` | Hicetae | `NOTICE` | John describes an otherwise orthodox ascetic practice; heresy classification doubtful. |
| `HC.N.PAT.GNOSIMACHI` | Gnosimachi | `NOTICE` | Catalogue abstraction opposed to scriptural/theological study; historical group uncertain. |
| `HC.N.PAT.HELIOTROPITES` | Heliotropites | `NOTICE` | Catalogue cosmological proposition; group uncertain. |
| `HC.N.PAT.THNETOPSYCHITES` | Thnetopsychites | `NOTICE` | Soul-mortality proposition; group identity uncertain. |
| `HC.N.PAT.AGONOCLINITAE` | Agonoclinites | `NOTICE` | Standing-prayer practice may be disciplinary rather than heresy. |
| `HC.N.PAT.THEOCATAGNOSTAE` | Theocatagnostae | `NOTICE` | Catalogue-defined blasphemous reading; group uncertain. |
| `HC.N.PAT.CHRISTOLYTAE` | Christolytae | `NOTICE` | Catalogue proposition about Christ leaving his body after resurrection. |
| `HC.N.PAT.ETHNOPHRONES` | Ethnophrones | `NOTICE` | Christian adoption of astrology/pagan customs; boundary with practice. |
| `HC.N.PAT.ETHICOPROSCOPTAE` | Ethicoproscoptae | `NOTICE` | Catalogue moral category rather than securely attested movement. |
| `HC.N.PAT.PARERMENEUTAE` | Parermeneutae | `NOTICE` | Catalogue category for scriptural misinterpretation; not a specific recoverable school. |
| `HC.N.PAT.LAMPETIANS` | Lampetians | `NOTICE` | Ascetic/disciplinary positions; documentary identity requires audit. |
| `HC.N.BYZ.AUTOPROSCOPTAE` | Autoproscoptae | `NOTICE`; compare schism | John calls them orthodox in doctrine but self-separated. |
| `HC.N.BYZ.APOSCHISTAE` | Aposchistae/Doxarii | `NOTICE` | Source-unique or nearly source-unique late catalogue group; numbering and historicity unresolved. |
| `HC.N.MED.JOSEPHINES-DOCTRINE` | Doctrinal identity attributed to medieval Josephines | `NOTICE`; linked to `HC.D.MED.JOSEPHINES` | Name occurs in *Ad abolendam*; specific propositions remain unresolved. |

## Alias and subgroup ledger

The alias key accounts for the words but does not assert that every source used them with identical extension.

| Alias key | Labels accounted for | Route | Qualification |
|---|---|---|---|
| `HC.A.EARLY.GNOSTIC-GENERIC` | Gnostics, “false gnosis,” Barbeloites, Borborites, Coddians, Phibionites, Stratiotics, Zacchaeans, and related catalogue names | `HC.D.EARLY.GNOSTIC-CURRENTS` and named notices | A source-by-source map is required; never one sociological church. |
| `HC.A.EARLY.VALENTINIAN-SCHOOLS` | Secundians, Ptolemaeans, Marcosians, Colorbasians, Heracleonites; Epiphanes, Isidore, Flora | `HC.D.EARLY.VALENTINIANISM` | Subschools receive notices within the dossier unless independent evidence requires a split. |
| `HC.A.EARLY.MARCIONITE-LINE` | Cerdonians, Lucianists, Apelleans | `HC.D.EARLY.MARCIONISM` plus source notices | Cerdo and Apelles are not erased; routing is genealogical, not identity. |
| `HC.A.EARLY.ENCRATITE-LINE` | Tatianists, Encratites, Severians, Apotactics, Artotyrites where treated as ascetic offshoots | `HC.D.EARLY.ENCRATISM` | Artotyrite and Apotactic labels remain separately noticed. |
| `HC.A.EARLY.MONTANIST-LINE` | Cataphrygians, Phrygians, Montanists, Tascodrugites/Ascodrugites, Pepuzians, Quintillians | `HC.D.EARLY.MONTANISM` | Regional and chronological doctrinal development remains visible. |
| `HC.A.EARLY.ELCHASAITE-NAMES` | Elchasaites, Elkesaites, Helcesaites, Sampsaeans | `HC.D.EARLY.ELCHASAITISM` | Nazoraeans and Ebionites are not merged into this key. |
| `HC.A.EARLY.DYNAMIC-NAMES` | Theodotians, Artemonites, psilanthropist/adoptionist formulas | `HC.D.EARLY.DYNAMIC-MONARCHIANISM` | Paul of Samosata retains a separate dossier. |
| `HC.A.EARLY.MODALIST-NAMES` | Noetians, Praxeans, Patripassians, Sabellians | `HC.D.EARLY.MODALIST-MONARCHIANISM` | Source-specific differences must be stated. |
| `HC.A.EARLY.NOVATIAN-NAMES` | Novatians, Novatianists, Cathari/Catharoe | `HC.D.EARLY.NOVATIANISM` | Never confuse ancient Cathari with medieval Cathars. |
| `HC.A.PAT.ARIAN-TRAJECTORIES` | Eusebian, Homoean/Homoian, Acacian, “Semi-Arian,” and other anti- or non-Nicene labels | `HC.D.PAT.ARIANISM` or `HC.N.PAT.HOMOIOUSIAN-TRAJECTORIES` | Formula and date decide routing; not all are synonyms. |
| `HC.A.PAT.ANOMOEAN-NAMES` | Aetians, Eunomians, Anomoeans, Exoucontians | `HC.D.PAT.ANOMOEANISM` | Preserve teacher and formula distinctions inside the dossier. |
| `HC.A.PAT.PNEUMATOMACHIAN-NAMES` | Pneumatomachians, Macedonians, Tropici where the Spirit is the object | `HC.D.PAT.PNEUMATOMACHIANISM` | “Macedonian” is a later attribution, not a proven self-name. |
| `HC.A.PAT.APOLLINARIAN-NAMES` | Dimoerites, Apollinarists | `HC.D.PAT.APOLLINARIANISM` | Christological formula controls the route. |
| `HC.A.PAT.PELAGIAN-NAMES` | Caelestians/Celestians, Pelagians | `HC.D.PAT.PELAGIANISM` | Pelagius and Caelestius are not assumed to have authored every same proposition. |
| `HC.A.PAT.SEMIPELAGIAN-NAMES` | Massilians; later “Semi-Pelagians” | `HC.D.PAT.SEMIPELAGIAN-CONTROVERSY` | Retrospective label; Cassian is not reduced to a slogan. |
| `HC.A.PAT.NESTORIAN-BOUNDARY` | “Nestorianism,” dyophysite polemical labels | `HC.D.PAT.NESTORIAN-PROPOSITIONS` | No unqualified application to the present Assyrian Church of the East. |
| `HC.A.PAT.MONOPHYSITE-BOUNDARY` | Eutychians, strict Monophysites, Acephali, Severians, “Egyptians/Schematics” in John Damascene | Separate Eutychian/strict-formula dossiers and context | Modern Oriental Orthodox Miaphysite faith is not collapsed into Eutyches. |
| `HC.A.PAT.APHTHARTODOCETE-NAMES` | Aphthartodocetae, Julianists, Gaianites | `HC.D.PAT.APHTHARTODOCETISM` | Severian background remains contextual. |
| `HC.A.PAT.AGNOETE-NAMES` | Agnoetae, Themistians | `HC.D.PAT.AGNOETISM` | Exact Christological object to be stated. |
| `HC.A.PAT.MESSALIAN-NAMES` | Messalians, Massalians, Euchites, Euphemites | `HC.D.PAT.MESSALIANISM` | Do not confuse with Massilians/Semi-Pelagians. |
| `HC.A.BYZ.ADOPTIONISM` | Spanish Adoptionism, Elipandianism, Felicianism | `HC.D.BYZ.SPANISH-ADOPTIONISM` | Not routed to ancient dynamic Monarchianism. |
| `HC.A.MED.CATHAR-NAMES` | Cathars, Albigensians, Patarenes, Publicani, “good men,” medieval “Manichaeans” | `HC.D.MED.CATHARISM` | These source labels overlap imperfectly and may be generic polemic. |
| `HC.A.MED.WALDENSIAN-NAMES` | Poor of Lyon, Leonists, Waldenses/Waldensians | `HC.D.MED.WALDENSIAN-ERRORS` | Early dispute, reconciled branches, and later Reformed church require phases. |
| `HC.A.MED.APOSTOLIC-BRETHREN` | Apostolics, Apostolic Brethren, Gerard Segarelli’s followers, Dolcinians | `HC.D.MED.APOSTOLIC-BRETHREN` | Ancient “Apostolici” are not the same group. |
| `HC.A.MED.FREE-SPIRIT` | Brethren of the Free Spirit, certain Beghards/Beguards, “Free Spirit” umbrella | `HC.D.MED.FREE-SPIRIT` or `HC.D.MED.VIENNE-BEGUARD-ERRORS` | Identity must be established locally; all Beguines are not included. |
| `HC.A.MED.FRANCISCAN-POVERTY` | Spiritual Franciscans, Fraticelli, Michaelists, absolute-poverty proposition | Separate `FRATICELLI` and `ABSOLUTE-POVERTY` heads | Persons, orders, factions, and propositions are not interchangeable. |
| `HC.A.MED.WYCLIF-LOLLARD` | Wycliffites, Wycliffism, Lollards | Separate Wycliffism and Lollardy dossiers | Reception is not simple identity. |
| `HC.A.MED.HUSSITE-BRANCHES` | Hussites, Utraquists/Calixtines, Taborites | Separate Hussitism, Utraquism, and Taboritism dossiers | Common origin does not erase later doctrinal divergence. |
| `HC.A.REF.SACRAMENTARIAN` | Sacramentarians, Zwinglians, memorialist labels | `HC.D.REF.SACRAMENTARIANISM` | Exact Eucharistic proposition controls inclusion. |
| `HC.A.POST.JANSENIST-LINE` | Jansenists, Appellants, Quesnellists, respectful-silence controversy | Separate Jansenist, fact/silence, and Quesnel heads | One historical family, several acts and objects. |
| `HC.A.POST.QUIETIST-LINE` | Quietism, Molinosianism, “Semi-Quietism,” Fénelon’s pure-love propositions | Separate Molinos and Fénelon heads | Censure language differs. |
| `HC.A.MOD.TRADITIONALISM` | Philosophical Traditionalism, fideist Traditionalism | `HC.D.MOD.FIDEISM-TRADITIONALISM` | Never use for contemporary liturgical or political traditionalists without qualification. |
| `HC.A.MOD.MODERNISM` | Modernists in the precise 1907 documentary sense | `HC.D.MOD.MODERNISM` | “Neo-Modernist” and generic “modern” remain excluded polemical labels. |
| `HC.A.MOD.FEENEYISM` | Feeneyism | `HC.D.MOD.FEENEY-ERROR` | Editorial shorthand, not the title of the Holy Office act. |

## Contextual controversy ledger

| Key | Context | Disposition | Reason and required treatment |
|---|---|---|---|
| `HC.C.APO.JEWISH-CHRISTIAN-DIVERSITY` | Jewish-Christian observance and identity | `CONTEXT` | Prevent the Judaizing necessity claim from becoming an indictment of Jews or all Torah-observant Christians. |
| `HC.C.EARLY.MANICHAEISM` | Manichaeism | `CONTEXT` | Rival universal religion deeply involved in Christian polemic and Augustine’s life; not simply a baptized dissenting school. |
| `HC.C.EARLY.QUARTODECIMAN` | Quartodeciman Paschal practice | `CONTEXT` | Calendar/communion dispute; not automatically a defined heresy. |
| `HC.C.PAT.MELETIAN` | Meletian schisms | `CONTEXT` | Multiple Meletian disputes; principal object is communion/discipline. |
| `HC.C.PAT.LUCIFERIAN` | Luciferian schism | `CONTEXT` | Rigorist communion dispute; Augustine 81 is accounted without upgrading it automatically. |
| `HC.C.PAT.AUDIAN` | Initial Audian schism | `CONTEXT` | Epiphanius himself distinguishes schism from later attributed anthropomorphism. |
| `HC.C.PAT.THREE-CHAPTERS` | Three Chapters controversy | `CONTEXT` | Constantinople II condemned persons/writings within Christological reception, not a new popular sect. |
| `HC.C.BYZ.HONORIUS` | Honorius I in the Monothelite controversy | `CONTEXT` | Exact Sixth Council sentence and Leo II’s confirmation; no slogan about later papal infallibility. |
| `HC.C.BYZ.PHOTIAN` | Photian conflict and schism | `CONTEXT` | Jurisdiction, communion, creed, and disputed council reception require separate treatment. |
| `HC.C.ECUM.ORIENTAL-ORTHODOX` | Present Oriental Orthodox churches | `CONTEXT` | Modern common declarations materially qualify inherited “Monophysite” labels. |
| `HC.C.ECUM.ASSYRIAN` | Present Assyrian Church of the East | `CONTEXT` | 1994 common Christological confession prevents unqualified present use of “Nestorian.” |
| `HC.C.MED.COERCION` | Crusade, inquisition, imprisonment, torture, execution, and civil penalties | `CONTEXT` | Ecclesial doctrine, procedure, and civil enforcement must appear as separate events. |
| `HC.C.MED.PARIS-1277` | Paris condemnation of 1277 | `CONTEXT` | Local academic syllabus with 219 propositions; not 219 universal dogmatic definitions. |
| `HC.C.MED.TEMPLARS` | Templar proceedings | `CONTEXT` | Procedural history and individual allegations, not a reliably reconstructed coherent heresy. |
| `HC.C.MED.EAST-WEST-1054` | The 1054 rupture and its later reception | `CONTEXT` | Mutual censures, jurisdiction, creed, rite, and later hardening of separation cannot be reduced to one named heresy. |
| `HC.C.MED.FLAGELLANTS` | Black Death flagellant companies | `CONTEXT` | The 1349 prohibition addressed unauthorized associations and attributed quasi-sacramental claims, not penitential discipline as such. |
| `HC.C.REF.TRENT-TOPICS` | Trent’s canons by doctrinal axis | `CONTEXT` | Original sin, justification, sacraments, Mass, Orders, and related canons answer propositions rather than one monolithic denomination. |
| `HC.C.ECUM.REFORMATION-AFTERMATH` | Present separated descendants and ecumenical qualification | `CONTEXT` | Later confessions and agreed texts determine whether sixteenth-century condemnations apply to a partner’s teaching as now presented. |
| `HC.C.POST.DE-AUXILIIS` | *De auxiliis* dispute | `CONTEXT` | Catholic schools remained permitted; neither Thomism nor Molinism may be entered as heresy. |
| `HC.C.MOD.INDEX` | Index of Forbidden Books | `CONTEXT` | Prohibition of a book does not prove that every author or sentence was formally heretical. |
| `HC.C.MOD.DDF-NOTIFICATIONS` | Modern notifications concerning individual authors/books | `CONTEXT` | Genre and exact finding matter; representative examples explain why no automatic new “heresy” is created. |
| `HC.C.MOD.NEO-GNOSTIC-PELAGIAN` | Recent analogies to “neo-Gnosticism” or “neo-Pelagianism” | `CONTEXT` | Analogical diagnosis is not historical identity or genealogy. |
| `HC.C.PHIL.TOPICAL-093-106` | Philastrius 93–106, cosmological, anthropological, and chronological miscellanea | `CONTEXT` | Every heading is accounted as catalogue architecture; no independent movement or formal act is evidenced by the headings alone. |
| `HC.C.PHIL.TOPICAL-107-120` | Philastrius 107–120, eschatological, chronological, Genesis, and marriage miscellanea | `CONTEXT` | Items are source occurrences, not adjudged historical heresies; chapters 107, 115, and 117 remain edition-sensitive. |
| `HC.C.PHIL.TOPICAL-121-136` | Philastrius 121–136, soul, Christological, biblical, and canonical miscellanea | `CONTEXT` | Checked headings route relevant analogues to dossiers, but do not prove separate groups or acts. |
| `HC.C.PHIL.TOPICAL-137-156` | Philastrius 137–156, exegetical, liturgical, translation, and angelological miscellanea | `CONTEXT` | Items remain contextual catalogue opinions; chapters 140, 151, and 154 remain edition-sensitive. |

## Explicit exclusion ledger

| Key | Excluded object | Disposition | Reason |
|---|---|---|---|
| `HC.X.RELIGION.JUDAISM` | Judaism as a religion and the Jewish people | `EXCLUDE` | Not a Christian heresy; ancient catalogue placement is historical evidence about the catalogue, not adopted classification. |
| `HC.X.RELIGION.ISLAM` | Islam as a religion | `EXCLUDE` | Not a Christian heresy for this census; John Damascene 101 is contextually accounted. |
| `HC.X.RELIGION.PAGAN` | Pagan religions and cults | `EXCLUDE` | Outside the Christian-heresy object. |
| `HC.X.PHILOSOPHY.ANCIENT-SCHOOLS` | Stoicism, Platonism, Pythagoreanism, Epicureanism, and other philosophies as schools | `EXCLUDE` | Not Christian heresies, notwithstanding ancient heresiological architecture. |
| `HC.X.DISCIPLINE.SCHISM-ONLY` | Schisms without a defining doctrinal proposition | `EXCLUDE` | Heresy, apostasy, and schism remain distinct. |
| `HC.X.DISCIPLINE.ABUSES` | Simony, sacrilege, clerical abuse, ordinary moral sins, and disciplinary violations as such | `EXCLUDE` | Wrongdoing does not by itself create a doctrinal dossier. |
| `HC.X.ALLEGATION.WITCHCRAFT-SECTS` | Alleged witchcraft or satanic “sects” without reliable doctrinal evidence | `EXCLUDE` | Procedural and evidentiary defects prevent a coherent heresy reconstruction. |
| `HC.X.ALLEGATION.TEMPLAR-HERESY` | Knights Templar as one coherent heretical system | `EXCLUDE` | Charges and coerced testimony do not establish a common doctrine; proceedings remain context. |
| `HC.X.PERSON.SAVONAROLA` | Savonarola as a named heresy | `EXCLUDE` | Political, disciplinary, and penal history does not establish one censured doctrinal system for this census. |
| `HC.X.PERSON.GALILEO` | Galileo affair as a named heresy | `EXCLUDE` | Distinct scriptural, scientific, procedural, and disciplinary case. |
| `HC.X.POLITICS.ACTION-FRANCAISE` | Action Française | `EXCLUDE` | Disciplinary/political condemnation, not a Christian heresy dossier. |
| `HC.X.POLITICS.SILLON` | Le Sillon as a named heresy | `EXCLUDE` | Social-political correction; propositions may be contextually cited but not counted as a heresy. |
| `HC.X.IDEOLOGY.FREEMASONRY` | Freemasonry | `EXCLUDE` | Condemned association and principles, but not a baptized Christian doctrinal school; treated elsewhere in the library. |
| `HC.X.IDEOLOGY.COMMUNISM` | Communism/socialism as political ideologies | `EXCLUDE` | Doctrinally condemned principles do not make the movements Christian heresies. |
| `HC.X.IDEOLOGY.NAZISM` | Nazism and racial totalitarianism | `EXCLUDE` | Condemned ideology, not a Christian heresy census object. |
| `HC.X.IDEOLOGY.THEOSOPHY-SPIRITISM` | Theosophy, Spiritism, and occult systems as religions or movements | `EXCLUDE` | External religious systems; individual baptized adherence is a different canonical question. |
| `HC.X.SCHOOL.PROBABILISM` | Probabilism as such | `EXCLUDE` | Permitted/disputed Catholic moral schools may not be converted into heresies. |
| `HC.X.SCHOOL.NOUVELLE-THEOLOGIE` | *Nouvelle théologie* as a blanket label | `EXCLUDE` | No single stable condemned proposition or universal named-heresy act. |
| `HC.X.POLEMIC.NEO-MODERNISM` | “Neo-Modernism” used generically | `EXCLUDE` | Unbounded polemical label; only exact propositions and acts qualify. |
| `HC.X.CURRENT.SSPX` | SSPX canonical rupture as a named heresy | `EXCLUDE` | The completed 1 July 2026 act and the 2 July five-plus-one penalty allocation, minister-status, lay-adherence, and sacramental determinations remain canonical responses and are not reduced to one proposition-level named heresy. |
| `HC.X.CURRENT.SEDEVACANTISM` | Sedevacantism as one universally adjudicated named heresy | `EXCLUDE` | Heterogeneous claims; exact propositions may be compared only with competent acts. |
| `HC.X.CURRENT.LIVING-PERSONS` | Unadjudicated living persons | `EXCLUDE` | The work does not infer obstinacy, crime, internal culpability, or salvation. |
| `HC.X.LOGIC.UNATTESTED-NEGATIONS` | Every logically possible denial of every dogma | `EXCLUDE` | Census concerns historically attested public proposition complexes and responses, not an infinite logical complement. |
| `HC.X.BOOKS.ALL-INDEXED` | Every work ever prohibited or investigated | `EXCLUDE` | Indexing, monitum, notification, and proposition-level heresy are distinct acts. |
| `HC.X.NOTIFICATION.EVERY-MODERN-CASE` | Every twentieth- or twenty-first-century doctrinal investigation as a new named heresy | `EXCLUDE` | Representative cases establish genre distinctions; an exhaustive case history is a different work. |

## Exact routing of contextual and excluded live dossiers

These prose dossiers explain boundaries but do not add normalized heresy counts. A target may route to two keys when the prose supplies context for an explicit exclusion.

| Section and exact destination label | Controlling route | Completion reason |
|---|---|---|
| §10, `dossier:manichaeism` | `HC.C.EARLY.MANICHAEISM` — `CONTEXT` | Rival universal religion used in Christian polemic, not simply an internal baptized school. |
| §20, `dossier:three-chapters` | `HC.C.PAT.THREE-CHAPTERS` — `CONTEXT` | Condemned persons and writings in Chalcedonian reception, not a new popular sect. |
| §30, `dossier:photian-rupture` | `HC.C.BYZ.PHOTIAN` — `CONTEXT` | A communion, jurisdictional, creedal, and council-reception conflict. |
| §40, `dossier:east-west-1054` | `HC.C.MED.EAST-WEST-1054` — `CONTEXT` | Mutual censures and later schism, not one homogeneous eastern heresy. |
| §50, `dossier:templars` | `HC.C.MED.TEMPLARS` — `CONTEXT`; `HC.X.ALLEGATION.TEMPLAR-HERESY` — `EXCLUDE` | Proceedings are treated; a coherent corporate creed is not asserted. |
| §50, `dossier:flagellants` | `HC.C.MED.FLAGELLANTS` — `CONTEXT` | Specific unauthorized associations and attributed claims, not penance as such. |
| §60, `dossier:trent-reformations` | `HC.C.REF.TRENT-TOPICS` — `CONTEXT` | Trent’s several doctrinal axes are not another denominational dossier. |
| §60, `dossier:reformation-ecumenical-aftermath` | `HC.C.ECUM.REFORMATION-AFTERMATH` — `CONTEXT` | Present confessions and agreed texts qualify inherited applications. |
| §70, `dossier:de-auxiliis` | `HC.C.POST.DE-AUXILIIS` — `CONTEXT` | The disputed Catholic schools remained permitted. |
| §80, `dossier:atheistic-communism-boundary` | `HC.X.IDEOLOGY.COMMUNISM` — `EXCLUDE` | A condemned political ideology is not thereby a Christian heresy school. |
| §80, `dossier:kung-judgment`; `dossier:modern-notifications` | `HC.C.MOD.DDF-NOTIFICATIONS` — `CONTEXT` | A teaching authorization or notification must retain its own genre and findings. |
| §80, `dossier:sspx-sedevacant-boundary` | `HC.X.CURRENT.SSPX` and `HC.X.CURRENT.SEDEVACANTISM` — `EXCLUDE` | Current competent status acts and heterogeneous claims are not converted into one adjudicated named heresy. |
| §80, `dossier:neo-gnostic-pelagian-analogy` | `HC.C.MOD.NEO-GNOSTIC-PELAGIAN` — `CONTEXT` | Contemporary analogy is not historical identity or descent. |

The remaining modern live dossiers `dossier:situation-ethics`, `dossier:womens-ordination`, and `dossier:religious-pluralism` are proposition-level normalized heads and therefore appear in the `HC.D.MOD` completion crosswalk rather than in this contextual table.

## Patristic catalogue coverage ledger

### How to read these tables

Each standard occurrence has an implicit stable key, for example Epiphanius 21 is `HC.CAT.EPIPH.021`, Philastrius 107 is `HC.CAT.PHIL.107`, Augustine 88 is `HC.CAT.AUG.088`, and John Damascene 101 is `HC.CAT.DAM.101`. A range row accounts for every intervening key. Names are normalized English/Latin finding labels used for routing, not newly verified translations. The route identifies a dossier family, notice, context, or exclusion; it does not certify the catalogue’s historical claim.

### Irenaeus and Hippolytus: non-serial chapter routing

These works do not present one simple modern numbered list comparable to the four catalogues below. Their book/chapter routing is therefore recorded without inventing occurrence numbers.

| Witness locus | Named material routed | Inventory route | Edition or evidence limit |
|---|---|---|---|
| Irenaeus, *AH* I.1–9, 11–21 | Valentinian system; Valentinus; Secundus; Ptolemaean/Marcosian trajectories | `HC.D.EARLY.VALENTINIANISM`; alias ledger | Collate SC text and distinguish Irenaeus’s constructed system from target fragments. |
| Irenaeus, *AH* I.23 | Simon and Menander | Simonian and Menandrian dossiers | Acts 8 and later Simonian claims require separation. |
| Irenaeus, *AH* I.24–28 | Saturnilus, Basilides, Carpocrates, Cerinthus, Ebionites, Nicolaitans, Cerdo, Marcion, Tatian/Encratites | Corresponding dossiers/notices | Chapter boundaries and dependent claims need critical collation. |
| Irenaeus, *AH* I.29–31 | Barbelo-type account, Ophite-type account, Cainites | Gnostic dossier and notices | Modern Gnostic textual classifications are not assumed identical. |
| Hippolytus, *Refutatio* I–IV | Greek philosophy, astrology, magic, and source theory | Context/exclusion | Not Christian dossier counts; authorship and edition numbering unresolved. |
| Hippolytus, *Refutatio* V | Naassenes, Peratae, Sethians, Justin’s group | Gnostic dossier and source notices | Extract individual target fragments after critical check. |
| Hippolytus, *Refutatio* VI–VII | Simon, Valentinian schools, Basilides, Saturnilus, Marcion, Carpocrates, Cerinthus, Ebionites, Theodotus | Corresponding dossier/alias keys | Chapter numbering differs among editions. |
| Hippolytus, *Refutatio* VIII–IX | Docetae, Monoimus, Tatian, Hermogenes, Quartodecimans, Montanists, Encratites, Noetus, Callistus, Elchasaites, Jewish groups | Dossiers, notices, and contexts | Callistus polemic and Jewish material require especially careful genre treatment. |
| Hippolytus, *Refutatio* X | Recapitulation | No new count | Dependency and variant-name audit outstanding. |

### Comparison-only patristic witnesses outside the closed occurrence baseline

Pseudo-Tertullian and Theodoret are cited only where an individual dossier independently identifies a useful comparison. Because this edition did not complete a checked entry-by-entry extraction of either work, it neither presents a false range crosswalk nor includes them in the enumerative-completeness denominator. A future edition may expand the baseline by adding a source-occurrence ledger for them; that would be a corpus expansion, not discovery of a silent gap in the present disclosed corpus.

### Epiphanius, *Panarion* 1–80

| Occurrences | Names in numerical order | Completed route |
|---|---|---|
| 1–4 | Barbarism; Scythianism; Hellenism; Judaism | `EXCLUDE` as religions/civilizational constructs; catalogue architecture retained as context. |
| 5–8 | Stoics; Platonists; Pythagoreans; Epicureans | `EXCLUDE` as philosophical schools. |
| 9–13 | Samaritans; Essenes; Sebuaeans; Gorothenes; Dositheans | `EXCLUDE` as non-Christian religious groups; Dosithean influence may be context. |
| 14–20 | Sadducees; Scribes; Pharisees; Hemerobaptists; Nasaraeans; Ossaeans; Herodians | `EXCLUDE` as Jewish groups; no adoption of Epiphanius’s classification. |
| 21–26 | Simonians; Menandrians; Saturnilians; Basilidians; Nicolaitans; Gnostics/Borborites | Four early dossiers, Nicolaitan notice, Gnostic dossier/notice cluster. |
| 27–32 | Carpocratians; Cerinthians; Nazoraeans; Ebionites; Valentinians; Secundians | Carpocratian, Cerinthian, Ebionite, Valentinian dossiers; Nazoraean context; Secundian alias. |
| 33–38 | Ptolemaeans; Marcosians; Colorbasians; Heracleonites; Ophites; Cainites | Valentinian aliases; Ophite and Cainite notices. |
| 39–44 | Sethians; Archontics; Cerdonians; Marcionites; Lucianists; Apelleans | Gnostic notices; Marcion dossier and related notices. |
| 45–50 | Severians; Tatianists; Encratites; Cataphrygians/Montanists/Tascodrugites; Pepuzians/Quintillians/Artotyrites; Quartodecimans | Encratite/Montanist dossiers and aliases; Quartodeciman context. |
| 51–56 | Alogi; Adamites; Sampsaeans/Elkesaites; Theodotians; Melchizedekians; Bardesanists | Elchasaite/dynamic-Monarchian dossiers; other labels as notices. |
| 57–62 | Noetians; Valesians; Cathari/Novatians; Angelics; Apostolics/Apotactics; Sabellians | Modalist and Novatian dossiers; Valesian, Angelic, Apotactic notices. |
| 63–68 | “Origenists” of the obscene-doer report; Origenists of Adamantius; Paulianists; Manichaeans; Hieracites; Meletians | First label notice; Origenism/Paul dossiers; Manichaean and Meletian contexts; Hieracite notice. |
| 69–74 | Arians; Audians; Photinians; Marcellians; Semi-Arians; Pneumatomachians | Arian, Photinian, Marcellian, Pneumatomachian dossiers; Audian and Semi-Arian notices/context. |
| 75–80 | Aerians; Anomoeans; Dimoerites/Apollinarians; Antidicomarianites; Collyridians; Messalians | Anomoean, Apollinarian, Messalian dossiers; three source-limited notices. |

Standard numbering 1–80 is stable at the macro level. Transliteration, compound aliases, internal tome labels, and whether a secondary name is a subgroup or synonym still require collation against the selected GCS text and Williams translation.

### Philastrius, *Diversarum hereseon liber* 1–156

The finding labels follow Friedrich Marx’s CSEL 38 *Conspectus operis*, pp. 138–141. They are not a completed collation of all chapter texts.

| Occurrences | Names/topics in numerical order | Completed route |
|---|---|---|
| 1–7 | Ophites; Cainites; Sethians; Dositheus; Sadducees; Pharisees; Samaritans | First three to Gnostic notices; 4–7 `EXCLUDE` as pre-Christian/non-Christian groups. |
| 8–14 | Nazoraeans; Essenes; Heliognosti/Deinvictiaci; frog worshippers; Musoritae; worshippers of the fly of Accaron; Troglodytes | `EXCLUDE`/context; catalogue’s pre-Christian architecture, not Christian dossiers. |
| 15–21 | worshippers of Queen/Fortune of Heaven; Baal idolaters; Astarte and Chemosh; Moloch and Remphan; Topheth altar; Puteoritae; bronze-serpent sacrificers | `EXCLUDE` as biblical/pagan cult classifications. |
| 22–28 | cave-image sacrificers; women worshipping Tammuz; Baalite idols; derivation of Baal from Balaam; medium raising Samuel; Astar/Astaroth worshippers; Herodians | `EXCLUDE` as biblical/pagan/Jewish classifications. |
| 29–37 | Simon Magus; Menander; Saturnilus; Basilides; Nicolaus and Gnostics; “heresy from Judas”; Carpocrates; Cerinthus; Ebion | Corresponding early dossiers/notices; Judas item `CONTEXT` as a catalogue construction. |
| 38–47 | Valentinus; Ptolemy; Secundus; Heracleon; Marcus; Colorbasus; Cerdo; Marcion; Lucanus; Apelles | Valentinian and Marcionite dossier/alias clusters. |
| 48–56 | Tatian; Cataphrygian Montanus; Theodotus of Byzantium; Metangismon; Melchizedek as divine power; Noetians; Sabellian/Patripassian/Praxean; Seleucus and Hermias; Proclians and Hermeonites | Encratite, Montanist, dynamic/modalist dossiers; other labels notices. |
| 57–65 | Florinians/Carpocratians/Milites; Paschal-day dispute; Chiliontaetitae; rejecters of John and Revelation; Manichaeans; Patricians; Symmachians; Paul of Samosata; Photinus | Dossiers/notices; Paschal dispute context; Manichaeism context; Symmachians `CONTEXT`. |
| 66–73 | Arians; Semi-Arians; Eunomians; errors about incarnation; Tropitae; errors about the Passion; Aerians/Encratites; Borborians | Arian/Anomoean and related dossiers; generic proposition items `CONTEXT`; notices/aliases. |
| 74–81 | Artotyrites; Ascodrugitae; Passalorhynchites; Aquarians; continuing prophets; Coluthians; world-not-changing proposition; barefoot-walking proposition | Notices/aliases/context; 80–81 are proposition notices, not established schools. |
| 82–92 | Novatians; Montenses; Abstinentes; Circuitores; refusal to eat with others; keeping Pascha with Jews; using only apocrypha; denying Pauline authorship of Hebrews; Meletians; Rhetorius; passible-divinity proposition | Novatian dossier; Montenses/Circuitores compared with Donatism; remaining items routed to notices or catalogue context, with passible-divinity compared to the Trinitarian dossiers. |
| 93–106 | God; heaven; earth; water; human body; soul and inspiration; soul and intellect; animals/birds/serpents; bad kings and false prophets; earthquakes; star names; language(s); name of language; announced year | `CONTEXT` proposition/topic occurrences under `HC.C.PHIL.TOPICAL-093-106`; not presumed groups or formal heresies. |
| 107–120 | end of the age; giants; paganism not instituted by God; chronological relation of Christianity/paganism/Judaism; origin of paganism; years from creation; weekday names; innumerable worlds; expulsion of Adam not from envy; Adam and Eve not blind; garments of skins; angel meeting Moses; Deuteronomy; legitimacy of marriage | `CONTEXT` occurrences under `HC.C.PHIL.TOPICAL-107-120`; the headings are accounted without creating groups or formal censures. |
| 121–136 | Noah’s division of the earth; Deucalion’s flood; zodiacal birth; souls not passing into demons/beasts; descent into hell not saving confessors there; substance of the soul; Savior’s generation; Pharaoh; David’s writing; inequality of Psalter; Cain; Cain again; stars not fixed in heaven; Ecclesiastes; Song of Songs; commandment | `CONTEXT` occurrences under `HC.C.PHIL.TOPICAL-121-136`; 124, 125, and 127 also cross-reference the soul, restoration, and Christological dossiers without becoming new heads. |
| 137–156 | image of God in humanity; languages of God; four living creatures; Epiphany date; eight ecclesial feasts; Septuagint and Aquila; thirty translators; six translators; Theodotion and Symmachus; books found in a jar; cursing foreign gods; Melchizedek; fasts; Solomon’s concubines; Joshua’s stone knives; breath received by Adam; Zechariah’s measuring line; Elijah’s ravens; cherubim/seraphim covering and praising God; cherub sent to Isaiah | `CONTEXT` proposition/topic occurrences under `HC.C.PHIL.TOPICAL-137-156`; many are exegetical/liturgical opinions rather than defensible heresy dossiers. |

Edition warning: CSEL 38 presents 28 pre-passion and 128 post-passion entries. Its prolegomena report a principal manuscript omitting chapters 107, 115, 117, 140, 151, and 154; earlier printings and manuscript witnesses therefore do not all yield the same visible sequence. The CSEL numbering is the disclosed working reference here, but the six restored chapters and their witnesses have not been independently collated; this crosswalk is complete for routing, not critical.

### Augustine, *De haeresibus* 1–88

| Occurrences | Names/topics in numerical order | Completed route |
|---|---|---|
| 1–10 | Simonians; Menandrians; Saturninians; Basilidians; Nicolaitans; Gnostics; Carpocratians; Cerinthians/Merinthians; Nazoraeans; Ebionites | Corresponding early dossiers/notices; Nazoraeans context. |
| 11–20 | Valentinians; Secundians; Ptolemaeans; Marcosians; Colorbasians; Heracleonites; Ophites; Cainites; Sethians; Archontics | Valentinian aliases; Gnostic notices. |
| 21–30 | Cerdonians; Marcionites; Apelleans; Severians; Tatianists/Encratites; Cataphrygians; Pepuzians/Quintillians; Artotyrites; Quartodecimans; Alogi | Marcion/Encratite/Montanist dossiers and notices; Quartodeciman context. |
| 31–40 | Adamians; Elchasaites/Sampsaeans; Theodotians; Melchizedekians; Bardesanists; Noetians; Valesians; Cathari/Novatians; Angelics; Apostolics | Dossiers/notices and aliases as above. |
| 41–50 | Sabellians/Patripassians; first “Origenists”; Origenists of Adamantius; Paulianists; Photinians; Manichaeans; Hieracites; Meletians; Arians; Audians/Anthropomorphites | Modalist, Origenist, Paulian, Photinian, Arian dossiers; notices/contexts for the rest. |
| 51–60 | Semi-Arians; Macedonians; Aerians; Aetians; Apollinarists; Antidicomarianites; Massalians; Metangismonites; Seleucians; Proclianites | Arian/Pneumatomachian/Anomoean/Apollinarian/Messalian dossiers; notices for remaining labels. |
| 61–70 | Patricians; Ascitae; Passalorhynchites; Aquarians; Coluthians; Florinians; world-state dissenters; barefoot walkers; Donatists; Priscillianists | Donatist/Priscillian dossiers; the other labels route to notices or catalogue context. |
| 71–80 | those refusing meals with others; Rhetorians; passible-divinity claim; “triform God”; water coeternal with God; denial that soul is God’s image; innumerable worlds; souls becoming demons/animals; universal liberation in Christ’s descent; temporal beginning assigned to the Son’s birth from the Father | `CONTEXT` proposition notices, except tritheist/apokatastasis/Arian cross-references after exact text audit. |
| 81–88 | Luciferians; Jovinianists; Arabici; Helvidians; Paternians/Venustians; Tertullianists; Abelonians; Pelagians/Caelestians | Luciferian context; Jovinian/Pelagian dossiers; six compact notices. |

The standard 1–88 chapter sequence is the disclosed working reference. Headings, Latin spelling, dependence on the *Anacephalaeosis*, and Augustine’s corrections to Epiphanius/Philastrius have not been newly collated in a critical edition. A matching number in Augustine and Epiphanius must never be assumed to name the same item.

### John Damascene, *De haeresibus* 1–103

| Occurrences | Names/topics in numerical order | Completed route |
|---|---|---|
| 1–20 | Epitome of Epiphanius’s pre-Christian architecture: Barbarism through Herodians | `EXCLUDE`/context, routed through `HC.CAT.EPIPH.001-020`; exact order of the four philosophical schools varies in presentations. |
| 21–46 | Epitome of Epiphanius’s Christian entries: Simonians through Tatianists | Route through the corresponding early dossiers/notices; dependency means no automatic independent witness count. |
| 47–80 | Encratites through Messalians | Route through Epiphanius 47–80; later expansions in the Messalian chapter are separately source-audited. |
| 81–83 | Nestorians; Eutychians; “Egyptians/Schematics/Monophysites” | Nestorian and Eutychian dossiers; third label to strict-formula/ecumenical-boundary context, not a present communion verdict. |
| 84–88 | Aphthartodocetae/Gaianites; Agnoetae/Themistians; Barsanouphites/Semidalites; Hicetae; Gnosimachi | Two dossiers and three source-limited notices. |
| 89–93 | Heliotropites; Thnetopsychites; Agonoclinitae; Theocatagnostae; Christolytae | Source-limited notices; historical group status unresolved. |
| 94–98 | Ethnophrones; Donatists; Ethicoproscoptae; Parermeneutae; Lampetians | Donatist cross-reference and four source-limited notices. |
| 99–103 | Monothelites; Autoproscoptae; Ishmaelites; Christianocategori/iconoclasts; Aposchistae/Doxarii | Monothelite and Iconoclast dossiers; Autoproscoptae notice/schism context; Islam explicit exclusion/context; Aposchistae notice. |

Numbering warning: modern presentations commonly speak of 103 chapters, with Islam at 101, the “accusers of Christians” or iconoclasts at 102, and Aposchistae at 103. The work’s closing claim about “a hundred,” recensional variation, compound continuations, and editions that organize the final material differently require collation against Bonifatius Kotter, PTS 22, before the numbering is treated as critically settled.

## Completion claim and remaining scholarly limits

The census is **enumeratively complete against its disclosed working corpus**: every admitted normalized head, notice, alias, context, exclusion, and numbered catalogue occurrence has a stable key and a completed destination. The prose is source-mapped in the sense that each dossier identifies the witnesses and acts on which its compressed account rests.

That bounded completion leaves meaningful work for a future edition or independent review:

1. collate patristic headings and passages afresh against the selected critical editions, especially the Philastrian restored chapters and the Damascene 100/103 problem;
2. expand, if desired, the enumerative baseline to checked individual occurrences in Pseudo-Tertullian and Theodoret and to a finer proposition-level extraction from Irenaeus and Hippolytus;
3. undertake an exhaustive canon-by-canon, papal-rescript, local-synod, medieval-trial, ASS/AAS, or DDF-notification sweep beyond the acts expressly admitted to this edition;
4. deepen target-side checking and modern specialist bibliography where a dossier presently depends mainly on refuters, judicial extracts, or late catalogues; and
5. obtain independent historical, theological, canonical, ecumenical, and textual review.

Accordingly, the permissible maturity claim is **“enumeratively complete against the disclosed working corpus and source-mapped,”** not “a critical edition,” “an exhaustive register of every act or accusation in Catholic history,” “an official ecclesial catalogue,” or “independently specialist-reviewed.”
