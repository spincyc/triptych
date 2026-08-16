# The Ark and the Mother of the Lord — Source Audit

## Identity and audit rule

- **Document:** `theology/mariology/ark-of-the-covenant`
- **Provider:** GPT
- **Profile:** `guidance/theology/mariology.md`
- **Audit date:** 2026-08-16
- **As-of date for mutable sources:** 2026-08-16

This audit governs the rendered study together with `scope.md`,
`source-bindings.toml`, and the focused research records in this leaf. It is a
faithful Catholic source audit: it receives Scripture, Tradition, and the
Church's Marian teaching positively while refusing false quotation, false
unanimity, invented geography, and arguments that ask typology to do work that
belongs to dogmatic definition.

The evidence classes remain separate throughout:

1. literal biblical narrative or assertion;
2. canonical typology within the unity of the Testaments;
3. patristic or liturgical reception;
4. magisterial teaching;
5. later saintly or theological fittingness;
6. project synthesis and spiritual application.

`cataloged` in the binding record identifies a controlled source-library
record. It does not by itself claim that this publication replayed another
leaf's acquisition, inspection, search, or verification event. Exact
publication-level verification belongs in the focused audits and must be
upgraded in `source-bindings.toml` only with the canonical fingerprint and date.

## Companion claim controls

The following records own the detailed evidence rather than being replaced by
this summary:

- `ark-journey-audit.md` — station order, versional differences, duration, and
  confidence grades;
- `lexical-parallels-audit.md` — Hebrew, Septuagint, and Greek New Testament
  forms and corpus counts;
- `patristic-typology-audit.md` — exact work, locus, language, date,
  authenticity, edition, and translation status;
- `dogma-and-typology-inventory.md` — exact defined objects and the unequal
  relation of Ark imagery to the four Marian dogmas;
- `virginal-marriage-typology.md` — Joseph's true marriage and the strict
  boundary on Uzzah analogies;
- `pedagogy-plan.md` — the bounded use of Lewis, Chautard, and
  Garrigou-Lagrange;
- `map-provenance.md` — cartographic sources, uncertainty grammar, artwork,
  accessibility, provenance, and rights;
- `ark-diagram-audit.md` — sanctuary and Ark diagrams, source geometry, and
  visual-claim control.

## Canonical itinerary audit

| Claim or episode | Principal loci | Status | Publication boundary |
| --- | --- | --- | --- |
| The Ark is fashioned for covenant testimony and divine meeting. | Exodus 25:10–22; 37:1–9 | Direct canonical text. | The Ark is not an autonomous divine object or talisman. God meets and speaks according to his covenantal gift. |
| Acacia/shittim wood is rendered “incorruptible wood” in the Greek tradition. | Exodus 25:10 Hebrew and LXX | Direct material and translation datum; Marian application is later reception. | The material is not a Lukan allusion or an independent proof of the Immaculate Conception or Assumption. |
| The cloud overshadows the completed Tent and the glory fills it after the Ark is installed. | Exodus 40:1–38 LXX | Direct canonical text and strong sanctuary-presence lexical background. | The grammatical object is the Tent, not the Ark alone. Mary may be contemplated with Ark and Tabernacle imagery within the wider indwelling pattern. |
| The Ark goes before Israel in the wilderness and Jordan crossing. | Numbers 10:33–36; Joshua 3–4 | Direct canonical narrative. | Map lines show narrative sequence, not an excavated road. Shittim and Gilgal require graded rather than absolute placement. |
| Jericho, the Ebal–Gerizim assembly, Shiloh, and Bethel belong to the canonical itinerary with unequal certainty. | Joshua 6–8; 18–19; Judges 20–21; 1 Samuel 3–4 | Direct Ark mentions plus some narrative inference. | Judges 20 has a material versional difference: Hebrew, Greek, and most modern versions read Bethel; the Clementine/Douay tradition reads Shiloh. Both are disclosed. |
| The Ark is captured and moves through Philistia before returning by Beth-shemesh to Kiriath-jearim. | 1 Samuel 4–7 | Direct canonical narrative with a material versional branch. | Hebrew, Vulgate, and Douay narrate Ashdod–Gath–Ekron; the registered Brenton Septuagint narrates Ashdod–Gath–Ashkelon. The five-lord offering list names Ashdod, Gaza, Ashkelon, Gath, and Ekron, but Gaza is not a narrated Ark stop. The Beth-shemesh death count is textually unstable and is not used without edition identification. |
| The first Davidic transfer ends in the breach at Uzzah; the second uses appointed Levitical bearing and ends in joy at Zion. | 2 Samuel 6; 1 Chronicles 13; 15–16; Numbers 4; 7:9 | Direct complementary canonical witnesses. | Samuel and Chronicles are not flattened into a supposed verbatim single account. Nacon/Nodan/Chidon, Perez-uzzah, and Obed-edom's house remain geographically unlocated. |
| The Ark remains at Obed-edom's house three months before entering Jerusalem. | 2 Samuel 6:10–17; 1 Chronicles 13:13–14; 15:25–29 | Direct canonical narrative. | The three months are exact; Obed-edom's house is not assigned an invented coordinate. |
| The Ark rests in Solomon's Temple and later passes into prophetic and apocalyptic horizons. | 1 Kings 8; 2 Chronicles 5–6; Jeremiah 3:16; 2 Maccabees 2:1–8; Hebrews 9; Revelation 11:19–12:17 | Canonical narrative, prophecy, deuterocanonical tradition, apostolic interpretation, and apocalypse. | The study invents no post-Temple itinerary. Revelation's woman retains Israel-Church-Mary polyvalence; the vision is not treated as a photograph. |

## Luke, Samuel, and lexical claims

The lexical work used identified Greek witnesses and a reproducible corpus
method. Counts are edition- and corpus-specific. “Unique” is not used without
naming the boundary.

SBLGNT v1.2 is the Greek textual witness and retains the Society of Biblical
Literature/Logos Bible Software attribution and CC BY 4.0 license. The exact
Luke and Revelation surface files from Faithlife commit
`c4d241a9c1c479a55b989ba35a4976c1d0b8052c` are separately tracked and carry
replayable verse-label search receipts. MorphGNT 6.12 is a distinct
morphological dataset under CC BY-SA 3.0. Its exact commit
`aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d` supplies a tracked,
one-lemma-per-line projection for replayable New Testament frequency counts;
that projection omits the separately licensed SBLGNT surface-text fields.

Exploratory Greek Old Testament frequency work used the exact CATSS LXXM Unicode
snapshot at `fddec9bd17e4eeeb2ed9410650923692601a4f13`, with CenterBLC commit
`4829f3746c84d75576702498e75a68856358f289` for normalized-lemma checking and
Wong commit `a1b5ff1c739f93cdd18dbab4c9e3fc6b1043141c` for the derivative provenance
and rights chain. Their access conditions do not permit placing the complete
Greek payloads in this public repository. Exact remote/restricted,
non-indexable artifact records therefore identify the bytes consulted, while
the publication binding deliberately records only acquisition/consultation,
not the repository's replayable `searched` state. The external commands,
complete hit lists, method, date, and corpus limitations remain in
`lexical-parallels-audit.md`. Because this research record does not
affirmatively establish satisfaction of the CATSS registration and User
Declaration conditions, those results are quarantined as non-publication-
controlling leads. No reader-facing numerical or exclusivity claim depends on
them; public claims instead name individually identified Greek loci and
witnesses.

| Proposed correspondence | Evidence state | Controlled conclusion |
| --- | --- | --- |
| David and Mary “arose and went.” | 2 Reigns 6:2 and Luke 1:39 share ordinary travel diction. | A direct but weak verbal echo alone; it gains force only within the ordered cluster. |
| Judah and upland geography. | Structural geographical correspondence, not identical Greek wording. | Both journeys unfold in Judah's uplands; neither the biblical road nor Luke's unnamed town is reconstructed. |
| Entry into a house and blessing. | Shared household and blessing pattern. | The Ark's arrival blesses Obed-edom's house; Elizabeth blesses Mary and her child under the Spirit. Luke does not say Mary mechanically causes household blessing. |
| David dances; unborn John leaps. | The standard Rahlfs Septuagint uses `orchēomai` and `anakrouō` for David while Luke uses `skirtaō` for John. Frederick Field, *Origenis Hexaplorum quae supersunt* I (1875), 555, prints a Symmachus fragment at 2 Reigns 6:16 with the `skirtaō` lemma. | The standard-LXX correspondence is narrative rather than verbal. The same-lemma observation is attributed to the alternative Symmachus/Hexaplaric tradition, with different inflected forms, and is not silently imported into Rahlfs. |
| Elizabeth's question and David's question. | Strong structural and content echo; not word-for-word identity. | Elizabeth's Spirit-filled wonder transforms the cadence of David's fearful question. |
| Three months. | Exact phrase `mēnas treis` within a larger house-stay pattern; not corpus-unique. | One of the strongest cumulative correspondences, not an isolated proof. |
| `anaphōneō` at Luke 1:42. | One token in the replayably bound MorphGNT New Testament lemma projection; individually identified Greek Chronicles loci at 1 Chr 15:28; 16:4, 5, 42; and 2 Chr 5:13. | Safe claim: Luke uses a verb found nowhere else in the checked New Testament corpus, while the identified Chronicles witnesses place the lemma in Ark and sanctuary worship. No restricted Old Testament corpus total or exclusivity claim is published. |
| `episkiazō` in Luke 1:35 and Exodus 40:35. | Exact lemma correspondence. | Strong sanctuary-presence echo; it recalls the cloud over the Tent containing the Ark, not an “exclusive Ark verb.” |

The cumulative Ark reading is presented as a strong Catholic canonical and
traditional interpretation. The publication does not claim that every verbal
correspondence is unique or that modern critical scholarship is unanimous
about Luke's deliberate compositional intent.

## Patristic, saintly, and liturgical reception

| Witness | Exact control | Status and safe use |
| --- | --- | --- |
| St. Ephrem the Syrian | Genuine Syriac *Hymns on the Nativity* 4.112–13 and 16.16–17; Edmund Beck, CSCO 186–187 (1959) | Joseph serves the Lord within Mary as priestly ministry before the Ark, and Mary is a pure tablet. Do not assign later Greek Ephremiana or the David–John comparison to Ephrem. |
| St. Epiphanius of Salamis | *On Weights and Measures* §35, CPG 3746; complete relevant passage in the Syriac version, James Elmer Dean, SAOC 11 (1935), 52–54 | Secure fourth-century David–John and written-Word/living-Word Ark reception, quoted as preserved in Syriac rather than falsely claimed as checked Greek. |
| St. Maximus of Turin | *Sermon* 42.5; A. Mutzenbecher, CCSL 23 (1962), 171–172 | Most-probably-genuine direct Latin Marian-Ark witness. Older Ambrosian attribution is not retained. |
| St. Proclus of Constantinople | *Homily 5 on the Theotokos*, CPG 5804, §3; PG 65.716–721; critical discussion in Nicholas Constas | Secure direct title: Mary among mother, servant, cloud, bridal chamber, and Ark of the Lord. Pseudo-Proclus works remain excluded. |
| St. Hesychius of Jerusalem | *Homily V on the Theotokos*, CPG 6569, §§1–3; Michel Aubineau, SH 59 (1978), 158–168 | Secure witness to Mary as ark of incorruptible life and to Psalm 132's Ark applied to the Virgin Theotokos. The opening comparison also invokes Noah's ark and is not silently collapsed. |
| Chrysippus of Jerusalem | *Oratio in sanctam Mariam Deiparam* §2, CPG 6705; M. Jugie, *Patrologia Orientalis* 19, 338 | The manuscript attributes the homily to Chrysippus and Jugie defended it; modern authenticity recheck remains desirable, so the transmission status is disclosed. |
| Syriac Visitation homily transmitted under Jacob of Serugh's name | Homily III in Paul Bedjan, Syriac pp. 661–685, especially 670–671; English translation Mary Hansbury (1998) | Audited but unused in the reader. It is a strong David-dancing/John-leaping and Ark-of-the-Godhead reception lead, but attribution remains qualified because a modern authenticity demonstration was not established. |
| Anonymous Akathist | Oikos 23; C. A. Trypanis, *Fourteen Early Byzantine Cantica* (1968) | Early Byzantine liturgical reception of Mary as Ark gilded by the Spirit. It is not attributed unqualifiedly to Romanos. |
| St. John Damascene | *Second Homily on the Dormition* §§2, 12–13, CPG 8062; critical text Bonifatius Kotter, PTS 29 (1988) | Mature eighth-century synthesis of Mary as the holy and living Ark entering heavenly rest, procession, and the heavenly Holy of Holies. It is not projected backward as pre-Nicene evidence. |
| St. Bonaventure | Authentic *De Purificatione BMV*, Sermo I, *collatio*; Quaracchi IX, 638b; retained by J.-G. Bougerol | Secure, focused gold-and-overshadowing witness. The richer *De Nativitate BMV*, Sermo V printed in the older Quaracchi corpus was not retained as secure by modern critical work and is labeled a thirteenth-century Marian sermon rather than simply Bonaventure. |

### Dogma-synopsis witness controls

The following entries control the compact historical claims in the four-dogma
synopsis. They identify exact works and loci and delimit the conclusion drawn;
they do not create a new claim of artifact inspection or repository-bound
verification beyond the states actually recorded in `source-bindings.toml` and
the owning research inventories.

| Witness or milestone | Exact control | Status and safe use |
| --- | --- | --- |
| St. Ignatius of Antioch | *Ephesians* 18--19; *Smyrnaeans* 1--3 | Early anti-docetic witness to Mary's real virgin conception and Christ's real birth, flesh, suffering, and resurrection. It is not the later three-moment perpetual-virginity formula or an advance transcript of Ephesus. |
| St. Justin Martyr | *Dialogue with Trypho* 100.5--6 | Early New-Eve contrast between the virgin Eve's disobedience and the Virgin Mary's believing obedience. It does not state the 1854 first-instant object. |
| St. Irenaeus of Lyons | *Against Heresies* III.21.10 and III.22.4 | III.21.10 protects the Word's real humanity taken from Mary; III.22.4 develops the New-Eve obedience/recapitulation pattern. Neither passage supplies the later conciliar or immaculate-definition formula verbatim. |
| St. Gregory Nazianzen | Epistle 101 to Cledonius | The *Theotokos* test belongs to Gregory's anti-Apollinarian defense of the Incarnation. The synopsis paraphrases the argument; critical Greek/translation comparison remains pending and no verbatim quotation is used. |
| St. Epiphanius of Salamis | *Ancoratus* 119.5; *Panarion* 78.11 | *Ancoratus* witnesses the received *ever-Virgin* title. *Panarion* 78.11 preserves uncertainty about Mary's earthly end, so it is evidence against inventing an apostolic death/Assumption narrative, not against the later dogma. Disputed death-language quotations are excluded. |
| St. Jerome | *Against Helvidius* 5--17 | Vigorous defense of Mary's enduring virginity through the disputed terms “brothers,” “until,” and “firstborn.” Jerome's rhetoric and particular kinship reconstruction are not themselves the dogmatic object. |
| St. Augustine | *Sermon* 186.1; *On Nature and Grace* 36.42 | *Sermon* 186.1 confesses Mary's virgin conception, birth, maternity, and enduring virginity. *On Nature and Grace* 36.42 exempts Mary when discussing personal sin because of the Lord's honor and grace; it is not an explicit doctrine of preservation from original sin at the first instant. |
| St. Germanus of Constantinople | *Dormition Sermon I*, received in *Munificentissimus Deus* 22--23 | A mature seventh-/eighth-century witness to Mary's bodily glorification and incorruption within Dormition reception. Its later homiletic narrative is not apostolic memoir or the source of the 1950 definition. |
| Sixtus IV | *Cum praeexcelsa* (1476) and *Grave nimis* (1483) | Establishes authorized liturgical reception of the Conception and prohibits the opposing parties from branding one another heretical before definition. No exact day is asserted for *Cum praeexcelsa*, and neither constitution is treated as the 1854 definition. |
| Council of Trent | Session V, Decree on Original Sin, §6 (17 June 1546; DS 1516) | Deliberately excludes the Blessed Virgin from the decree's universal application and renews Sixtus IV's constitutions. This is a decisive reception control, not yet the positive first-instant definition. |
| Alexander VII | *Sollicitudo omnium ecclesiarum* (1661) | States the object with increased precision around Mary's preservation from original sin from the first instant of creation and infusion of her soul. It is a major pre-definition clarification, not an ex cathedra definition substituted for *Ineffabilis Deus*. |

Consequential rejected or quarantined attributions:

- Hippolytus, *Commentary on Daniel* 4.24.3, makes the Ark Christ's body; it is
  not a secure text directly calling Mary the Ark.
- Pseudo-Gregory Thaumaturgus, CPG 1775, is labeled an anonymous later Greek
  homily transmitted under Gregory's name, never third-century evidence.
- the Turin Pseudo-Athanasius homily is anonymous Sahidic Coptic, not a secure
  Athanasian Greek witness; the famous English “Ark of the Covenant” includes
  editorial supplementation;
- Cyril of Alexandria's genuine *Scholia on the Incarnation* uses Ark imagery
  Christologically. No direct Marian-Ark sentence is assigned to Cyril without
  a secure work and locus;
- no claim of patristic unanimity is made, and early ecclesial readings of
  Revelation 12 remain visible.

Positive virginal-marriage synthesis is controlled separately by Origen,
*Homilies on Luke* 13.7; Ambrose, *Exposition of Luke* II.2 and II.5 and *De
institutione virginis* 8.52–57; Jerome, *Commentary on Ezekiel* XIII on
44:1–3 (PL 25, 430A; CCSL 75, 646–647); Augustine, *On Marriage and
Concupiscence* I.11.12–13 and *Sermon* 51; Bernard, *In Praise of the Virgin
Mother* II.16; Aquinas, ST III, q.29, a.2; Vatican II, *Gaudium et spes*
48–49; John Paul II, *Familiaris consortio* 16 and *Redemptoris custos* 7–8
and 17–21; and the Roman *Collection of Masses of the Blessed Virgin Mary*.
Ambrose receives Ezekiel's closed eastern gate as a Marian figure and relates
its remaining closed to Joseph; Jerome reports that “some” beautifully read it
of Mary, which prevents a claim of patristic unanimity. The figure supplies
neither literal exegesis of Ezekiel, anatomy, nor Joseph's psychology. These
sources establish true marriage, the dignity of marital intimacy, freely
chosen mutual continence, obedient reception, affectionate custody, and
a love both marital and virginal (the study's independent English paraphrase
of the official Latin formulary). None identifies Joseph with Uzzah.

Liturgical reception is identified by exact register: the anonymous Akathist;
the Byzantine Annunciation and Dormition formularies, with traditional
authorship disclosed rather than promoted into critical certainty; the Litany
of Loreto; and the Roman *Collectio missarum de Beata Maria Virgine*, especially
the Visitation and “Mary, Temple of the Lord” formularies. Paul VI's *Marialis
cultus* 6 and 26, CCC 2676, Benedict XVI's 2006 and 2011 Assumption homilies,
and his Angelus of 23 December 2012 establish modern official Catholic
reception without replacing literal exegesis or dogmatic definition. Francis,
*Misericordiae vultus* 24, says Mary was prepared “from the outset” by divine
love to be the Ark of the Covenant; that papal theological application does
not itself state the 1854 definition's exact first-instant formula.

## Four dogmas and the Ark

| Dogma | Controlling object and authority | Relation to Ark typology |
| --- | --- | --- |
| Divine motherhood | The one born of Mary is the eternal Son truly made man; Ephesus (431), Cyril's received letters, Chalcedon (451), and *Lumen gentium* 52–53. | Most direct relation: Mary bears the divine Lord and incarnate Word, as the old Ark bore covenant testimony and marked God's throne-presence. |
| Perpetual virginity | A dogma of the Church's universal Tradition and ordinary universal Magisterium: Mary is virgin before, in, and after Christ's birth. Constantinople II confesses the ever-Virgin Theotokos; Lateran 649 canon 3 gives the explicit threefold content; the ancient liturgy and CCC 496–507 receive the same faith. | Ark holiness, sealed-dwelling, and undivided consecration illuminate fittingness; they do not turn marriage into impurity, reduce the dogma to one local synod in isolation, or supply an anatomical proof. |
| Immaculate Conception | From the first instant of conception Mary was preserved immune from every stain of original sin by singular grace and privilege in view of Christ's merits; Pius IX, *Ineffabilis Deus* (1854). | Gold and “incorruptible wood” belong to later typological reception of graced holiness. They do not replace the defined first-instant and prevenient-redemption clauses. |
| Assumption | Mary, having completed the course of earthly life, was assumed body and soul into heavenly glory; Pius XII, *Munificentissimus Deus* 44 (1950). | Psalm 132:8, the living Ark's rest, John Damascene, and Revelation's heavenly horizon supply ecclesially received fittingness. Scripture contains no hidden canonical Assumption narrative, and the definition leaves undefined whether Mary died. |

Christ fulfills the covenant. Mary is the new Ark because she bears him. The
four dogmas are neither four properties of an ancient chest nor four deductions
from selected materials.

## Joseph, Uzzah, and virginal marriage

The direct canonical controls are 2 Samuel 6 and 1 Chronicles 13 for Uzzah,
and Matthew 1–2 and Luke 1–2 for Joseph. Scripture supplies no verbal or
narrative equation between the two men. The publication therefore rejects
“Joseph feared death if he touched Mary” as a canonical claim.

The positive synthesis is Joseph's Davidic, obedient vocation: he receives Mary
as his true wife, names Jesus, protects mother and Child, heads a covenantal
household, and freely shares a virginal marriage. Genuine Ephremic priest-before-
Ark imagery may illuminate reverent service. It cannot make Mary physically
dangerous, marital union unclean, or continence a product of panic. Any later
saintly use of Uzzah must be attributed exactly and labeled accommodation or
fittingness.

## Spiritual pedagogy and rights

- C. S. Lewis's *Miracles* contributes a movement from concrete wonder through
  clarified supernatural reason. No Lewis pastiche or extended quotation is
  used; the twentieth-century work remains copyrighted.
- Dom Jean-Baptiste Chautard's *The Soul of the Apostolate* contributes the
  priority of interior union with God over merely external activity and the
  movement from prayer to apostolic fruit. Edition and translation rights must
  accompany any direct quotation.
- Réginald Garrigou-Lagrange's *The Three Ages of the Interior Life*, not
  M.-J. Lagrange, contributes the purgative, illuminative, and unitive
  progression as a formation pattern. It is spiritual pedagogy, not a claim
  about the Ark narrative's historical stages.

The publication adapts these techniques in original prose. They are not
patristic witnesses, dogmatic authorities, or sources for a Marian definition.

## Map, plates, and geography

The current map is a source-first v3 relief composition built from Natural
Earth 5.1.2 vector data and pinned Mapzen Terrarium terrain tiles. The project-created
semantic overlay supplies the route geometry, station symbols, labels, textual
content, confidence encoding, and Old/New Testament correspondence layers from
the controlled evidence. The underlying cartographic sources remain identified
and attributed rather than being presented as an unaudited external map or as
project-created geography. Solid site markers, approximate areas, candidate
sites, uncertain event corridors, traditional locations, and purely
typological connectors remain visually distinct. Specific controls include:

- no exact route between named termini unless the biblical text supplies it;
- no pins for Perez-uzzah or Obed-edom's house;
- the Hebrew/Vulgate/Douay route retains Ekron as the third narrated
  Philistine city, while the registered Brenton Septuagint branch substitutes
  Ashkelon; both branches are disclosed in the figure or its shared textual
  key, and neither is silently harmonized. Departure toward Beth-shemesh is a
  strong narrative implication rather than a newly repeated departure notice;
  Gaza remains Philistine-lordship context, not an Ark stop;
- the Judges 20 Bethel/Shiloh branch shown textually as a versional difference,
  not converted into two simultaneous Ark routes;
- Ein Karem labeled traditional rather than named by Luke;
- Old Testament and New Testament routes shown as separate layers, not one
  geographically coincident road;
- a complete textual route and correspondence key present in both PDF and web;
- five fine graphite interpretive plates---the Ark, the wilderness Tabernacle,
  Shiloh, David's tent, and Solomon's Temple---distinguish biblical
  prescription from editorial reconstruction and typological overlay.

`map-provenance.md` owns the exact coordinates, Natural Earth 5.1.2 and Mapzen
source records, pinned terrain receipt, deterministic assembly script, source
and output hashes, artwork dimensions, mode, bytes, effective resolution,
accessibility text, and visual review. `ark-diagram-audit.md` owns the five
AI-generated graphite plates' prompts, output identities, interpretive limits,
source geometry, and visual-claim controls. Earlier AI-texture and vector-only
map prototypes remain historical provenance in their owning records; they are
not the current publication artwork or evidence.

## Translation, quotation, and rights limits

- The study cites Scripture principally by chapter and verse and does not
  reproduce a modern translation in bulk.
- Repository public-domain Bible witnesses are comparison texts, not silently
  substituted for Hebrew, Greek, or a modern Catholic edition.
- Patristic translations are identified as critical, working, public-domain,
  or modern copyrighted translations. A working English translation never
  becomes the original author's exact wording by repetition.
- Holy See English pages are cited as official delivery states where supplied;
  the promulgated Latin and exact defining locus control when a translation's
  authorship or rights are uncertain.
- Modern scholarship, Lewis, Chautard translations, Garrigou-Lagrange
  translations, Constas, Aubineau, Beck, Kotter, Trypanis, and Hansbury remain
  third-party works. Quotation is short and attribution-specific; nothing is
  vendored or reproduced at chapter length.
- The prose, cartographic composition, and semantic overlay are project-created
  contributions under the repository's license boundary. Natural Earth 5.1.2,
  the pinned Mapzen terrain tiles and their incorporated source data, received
  texts, translations, fonts, and third-party scholarship retain their own
  status. The five AI-generated graphite plates are disclosed with their
  prompts and output histories in `ark-diagram-audit.md`; they are interpretive
  illustrations and supply no independent historical, geographic, or
  theological evidence.

## Consequential negative results

1. No ancient or modern road reconstruction is presented as the Ark's route.
2. No post-Temple itinerary is invented.
3. No “same Greek verb” claim is made for David's dance and John's leap.
4. No ordinary travel verb is promoted into a unique lexical proof.
5. No Father is said to teach a later definition in its final vocabulary
   without the exact evidence.
6. No Pseudo-Gregory, Pseudo-Athanasius, Pseudo-Proclus, or disputed Syriac
   homily is cited under an unqualified famous name.
7. No direct Uzzah–Joseph canonical parallel is asserted.
8. No marital intimacy is described as unclean and no Marian holiness as
   lethal physical taboo.
9. No Ark material or event independently proves any Marian dogma.
10. No Revelation 12 reading suppresses the woman-sign's Israel and Church
    dimensions.
11. No Lewis, Chautard, or Garrigou-Lagrange technique is passed off as
    patristic testimony or magisterial teaching.
12. No ecclesiastical approval or independent human specialist review is
    claimed.

## Production state

The source and reader claims were reconciled against the focused audits on
2026-08-16. The final reviewed build is 46 letter-size pages. Its log has no
fatal error, undefined reference, rerun request, or overflow warning; its only
two underfull-box warnings were located, inspected in the page rasters, and
visually accepted. PDF metadata, structure, embedding, Unicode maps, and
extracted text pass, with no replacement character. The 6.83 MB output crossed
the size-investigation trigger; the investigation found the intended
high-resolution relief-map and graphite-plate rasters rather than an
unexplained payload or rasterized body text. Every final page raster and the
bounded contact sheets were inspected, with full-size review of both map
panels, all five graphite plates, and all four dogma synopses. The reviewed PDF
recorded by `build/pdf-review/gpt-ark-postff-2026-08-16/review-run.json` and the installed PDF are
byte-identical at SHA-256
`0d995ac1d447f53cc55496fa8907c16a7940639b986fee02579b16e87d7164da`.

The generated and installed web editions are byte-identical at SHA-256
`8083f51e35ce1d72fdd306d23c378361e70f778ee27f1a7acaeb915c1e27a2d4`.
This audit does not anticipate commit, push, release-binding refresh,
public-site gates, or deployed-route verification; those states are recorded
in the work register only after they occur. External specialist and
ecclesiastical review remain unclaimed and nonblocking for this explicitly
qualified alpha publication.
