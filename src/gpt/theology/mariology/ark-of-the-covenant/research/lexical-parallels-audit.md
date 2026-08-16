# Lexical and Canonical Parallels Audit — Luke 1 and the Ark

This audit supports `sections/50-overshadowing-hill-country.tex` and
`sections/60-scripture-recognizes-scripture.tex`. It records the exact Greek
and Hebrew controls behind the publication's Catholic New-Ark synthesis. Its
governing conclusion is affirmative and cumulative: Luke 1 does not explicitly
call Mary the Ark, but the ordered convergence of sanctuary-cloud language,
Ark-journey motifs, rare cultic diction, ecclesial reception, and the
Christological identity of the child makes the New-Ark reading strong. Exact
linguistic limits protect that reading from brittle claims that it does not
need.

## Verification legend

- **T — direct textual observation:** exact wording checked in the identified
  Hebrew or Greek textual witness.
- **M — morphology/corpus result:** form parsed or count made in the identified
  machine-readable corpus and cross-checked where stated.
- **C — canonical correspondence:** relation depends upon two or more biblical
  passages read within the complete canon.
- **S — structural echo:** narrative order, role, geography, or theological
  relation corresponds without exact lexical identity.
- **R — received Catholic interpretation:** an official Catholic, patristic,
  or liturgical source receives the relation; this does not retroactively turn
  typology into explicit grammar.
- **P — project synthesis:** source-grounded constructive conclusion, not a
  quotation from one authority.
- **L — bounded lead or limitation:** useful evidence whose edition,
  transmission, or scholarly status prevents a stronger claim.
- **X — rejected formulation:** contradicted by the checked text or broader
  than the evidence permits.

## Texts, editions, and corpus bounds

The full Git commit IDs below are the immutable artifact fingerprints used for
the count and spot-check boundaries. No mutable branch head carries a result.

### New Testament

- Morphology and lemma counts use MorphGNT's SBLGNT-aligned files at
  <https://github.com/morphgnt/sblgnt> commit
  `aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d` (version 6.12 lineage).
  MorphGNT's parsing and lemmatization are declared CC BY-SA 3.0. These are
  properly “MorphGNT lemma counts over its SBLGNT-aligned corpus,” not bare
  SBLGNT counts.
- The embedded SBLGNT surface text is a distinct rights layer, copyright 2010
  Society of Biblical Literature and Logos Bible Software and governed by the
  linked SBLGNT text license; it is not relicensed by MorphGNT's CC BY-SA terms.
- Surface forms were spot-checked independently in the official Faithlife
  SBLGNT repository, <https://github.com/Faithlife/SBLGNT>, version 1.2 commit
  `c4d241a9c1c479a55b989ba35a4976c1d0b8052c`, declared CC BY 4.0. This official
  repository has no morphology and did not supply the lemma counts.
- Edition information is also available from <https://sblgnt.com/download/>.
  Counts are bounded token counts in the identified MorphGNT artifact, not
  claims about every historical manuscript or later printed edition.

### Greek Old Testament

- Exploratory count queries used the CATSS LXXM Unicode artifact at
  <https://github.com/nathans/lxxmorph-unicode> commit
  `fddec9bd17e4eeeb2ed9410650923692601a4f13`. Its declared terms carry the CCAT
  conditions: noncommercial study/education, User Declaration/registration,
  acknowledgment, and access control. It is not an open-content license.
- Normalized-lemma checking used the CenterBLC Text-Fabric RLXX1935 artifact at
  <https://github.com/CenterBLC/LXX> commit
  `4829f3746c84d75576702498e75a68856358f289`. The repository's MIT license
  covers its software and additions; its README says the Greek data derive
  through Wong from CATSS, so MIT is not represented as relicensing that
  upstream text/data.
- The provenance layer was checked at
  <https://github.com/eliranwong/LXX-Rahlfs-1935> commit
  `a1b5ff1c739f93cdd18dbab4c9e3fc6b1043141c`. Its README declares CC BY-NC-SA
  4.0 and additionally requires compliance with CATSS User Declaration
  restrictions. It was not the primary count query.
- CATSS, Wong, and CenterBLC are a derivative lineage, not independent textual
  witnesses. CenterBLC cross-checks normalization and token handling. In
  particular, raw CATSS has a malformed Genesis 25:22 lemma and returns five
  exact `σκιρτάω` lemma hits; CenterBLC's normalized correction supports the
  six-locus count reported below.
- The retained records establish the payload identities and restrictions, but
  do not affirm that this research session satisfied the CATSS registration
  and User Declaration conditions. The results are therefore quarantined as
  non-publication-controlling research leads. No reader-facing numerical or
  exclusivity claim depends on them.
- Public running-text controls include the German Bible Society Rahlfs--Hanhart
  presentation, <https://www.die-bibel.de/en/bible/LXX/2SA.6>, the official
  NETS translation of 2 Reigns,
  <https://ccat.sas.upenn.edu/nets/edition/10-2reigns-nets.pdf>, and the
  Rahlfs-derived corpus at
  <https://github.com/eliranwong/LXX-Rahlfs-1935>.
- The Septuagint book is *2 Reigns* or *2 Kingdoms* (*Basileiōn B*),
  corresponding to modern 2 Samuel. The relevant chapter and verse numbers
  remain 6:2--16.
- These searchable CATSS/RLXX1935 derivatives were not a fresh collation of
  Rahlfs page images, the Rahlfs--Hanhart apparatus, or a Göttingen critical
  edition. CATSS also reports correction and adaptation toward Göttingen
  editions. Accordingly the results are called CATSS/RLXX1935-derived
  electronic-corpus counts, not unqualified counts of printed Rahlfs.
- Search method, 2026-08-15: exact lemma-field token count for the three
  frequency claims, followed by inspection of every returned locus and exact
  surface-form comparison where stated. The CenterBLC normalized lexeme field
  was used to cross-check the `σκιρτάω` count. The complete hit lists appear
  below; no extrapolation was made from a partial book or search-result page.

### Search receipts

The MorphGNT files have columns for reference, part of speech, parse, text,
normalized word, and lemma. The CATSS Unicode files use verse headers and
split some compound lemmas into root and prefix. These exact read-only queries
produced the enumerated hit lists:

```sh
awk '$NF=="ἀναφωνέω"{print $1,$3,$4,$NF}' *-morphgnt.txt
awk '$NF=="ἐπισκιάζω"{print $1,$3,$4,$NF}' *-morphgnt.txt
awk '$NF=="σκιρτάω"{print $1,$3,$4,$NF}' *-morphgnt.txt

awk '/^[^ ]+ [0-9]+:[0-9]+/{v=$0;next}
     $3=="φωνέω"&&$4=="ἀνα"{print v,$1,$2}' *.txt
awk '/^[^ ]+ [0-9]+:[0-9]+/{v=$0;next}
     $3=="σκιάζω"&&$4=="ἐπι"{print v,$1,$2}' *.txt

rg -n '^ἀναφωνέω$|^ἐπισκιάζω$|^σκιρτάω$' tf/1935/lex_utf8.tf

rg -n 'Luke 1:(35|39|41|42|44|56)' data/sblgnt/text/Luke.txt
rg -n 'Rev 11:19|Rev 12:(1|3)' data/sblgnt/text/Rev.txt
```

### Hebrew Exodus

- The Masoretic wording and morphology of Exodus 40:34--35 were checked
  against the Open Scriptures Hebrew Bible / Westminster Leningrad Codex
  resources: <https://github.com/openscriptures/morphhb>.
- The Hebrew observation controls popular claims about “overshadowing” and
  “Shekinah”; it does not negate the Greek Exodus's real importance for Luke's
  Greek diction.

## Exact morphology and frequency register

| Item | Exact morphology and corpus result | Evidentiary use |
| --- | --- | --- |
| Luke 1:42 `ἀνεφώνησεν` | Lemma `ἀναφωνέω`; aorist active indicative, third person singular. Exactly **1** MorphGNT lemma token, hence an NT hapax in the checked SBLGNT-aligned corpus. | T / M. A genuinely rare Lucan choice with cultic resonance. |
| CATSS/RLXX1935-derived `ἀναφωνέω` lead | The exploratory query returned 1 Chr 15:28; 16:4, 5, 42; and 2 Chr 5:13. The forms are participles or infinitives, not Luke's exact finite form. | Quarantined lead, not publication evidence. The reader instead names the individually identified Chronicles loci and their Ark/sanctuary settings without a corpus-total or exclusivity claim. |
| Exod 40:35 `ἐπεσκίαζεν` | Lemma `ἐπισκιάζω`; imperfect active indicative, third person singular. The cloud is the grammatical subject and the tent the object; the Ark had been installed inside at Exod 40:21. | T / M. Strong sanctuary-cloud resonance; not a claim that the verb grammatically modifies the Ark. |
| Luke 1:35 `ἐπισκιάσει σοι` | `ἐπισκιάσει`: lemma `ἐπισκιάζω`; future active indicative, third person singular. `σοι`: dative second-person singular pronoun. The power of the Most High is the subject; Mary is the dative complement. | T / M. Same rare lemma as Greek Exodus; direct divine-presence resonance. |
| CATSS/RLXX1935-derived `ἐπισκιάζω` lead | The exploratory query returned Exod 40:35; Ps 90:4; Ps 139:8; and Prov 18:11. Ps 90:4 has the exact two-word collocation `ἐπισκιάσει σοι`, followed by sheltering-wing imagery. | Quarantined lead, not publication-count evidence. The individually controlled Exodus and Psalm loci support layered sanctuary-cloud and protecting-wing resonances. |
| NT `ἐπισκιάζω` | Exactly **5** MorphGNT lemma tokens: Matt 17:5; Mark 9:7; Luke 1:35; Luke 9:34; Acts 5:15. | M. Luke 9:34's overshadowing cloud reinforces Luke's divine-presence register. The word is rare, not unique. |
| Luke 1:41, 44 `ἐσκίρτησεν` | Lemma `σκιρτάω`; aorist active indicative, third person singular. MorphGNT has exactly **3** tokens, all Luke: 1:41, 44 and 6:23 (`σκιρτήσατε`, aorist active imperative, second plural). | T / M. Notable Lucan concentration; John bodily “leaps” or “bounds” for joy. |
| CATSS/RLXX1935-derived `σκιρτάω` lead | The exploratory normalized query returned Gen 25:22; Ps 113:4, 6; Wis 17:18; Mal 3:20; and Jer 27:11, with related forms elsewhere. | Quarantined lead. The publication's David--John distinction is controlled directly by the identified 2 Reigns 6 and Luke 1 witnesses, not by this restricted-corpus result. |
| 2 Reigns 6:2 `ἀνέστη καὶ ἐπορεύθη` | `ἀνέστη`: lemma `ἀνίστημι`, aorist active indicative, third singular. `ἐπορεύθη`: lemma `πορεύομαι`, aorist passive-form/deponent indicative, third singular. | T / M. Direct but common biblical travel formula; weak alone. |
| Luke 1:39 `Ἀναστᾶσα … Μαριὰμ … ἐπορεύθη` | `Ἀναστᾶσα`: `ἀνίστημι`, aorist active participle, nominative feminine singular. `ἐπορεύθη`: identical finite form and lemma to 2 Reigns 6:2. | T / M. Same two verbs and order, but not the same exact phrase or morphology. Cumulative force only. |
| `μῆνας τρεῖς` | Exact adjacent words in 2 Reigns 6:11 and Luke 1:56: accusative masculine plural noun plus numeral; 1 Chr 13:14 has the reverse `τρεῖς μῆνας`. | T / M / S. Exact core phrase, strong within the house-stay sequence, not corpus-unique. Luke adds `ὡς`, “about.” |
| Rev 11:19; 12:1 `ὤφθη` | Lemma `ὁράω`; aorist passive indicative, third singular. | T / M. Repeated vision language and immediate literary adjacency; Rev 12:3 repeats the vision formula, so the wording is not a unique identifying signal. |

## Overshadowing: Hebrew, Greek, and Lucan controls

| Locus | Checked wording | Exact claim and boundary |
| --- | --- | --- |
| Exod 40:34 MT | `וַיְכַס הֶעָנָן אֶת־אֹהֶל מוֹעֵד`; `וַיְכַס`, lemma כסה, Piel wayyiqtol 3ms. | The cloud **covered** the tent. X: “The Hebrew says overshadow.” |
| Exod 40:35 MT | `כִּי־שָׁכַן עָלָיו הֶעָנָן`; `שָׁכַן`, lemma שכן, Qal perfect 3ms. | The cloud **settled/dwelt** upon it. The verb is present; the later noun שכינה (*Shekinah*) is not. X: “The verse calls the cloud the Shekinah.” |
| Exod 40:34 LXX | `ἐκάλυψεν ἡ νεφέλη τὴν σκηνὴν τοῦ μαρτυρίου`; `ἐκάλυψεν`, `καλύπτω`, aorist active indicative 3sg. | The Greek also first says the cloud covered the tent. |
| Exod 40:35 LXX | `ἐπεσκίαζεν ἐπ᾽ αὐτὴν ἡ νεφέλη … δόξης κυρίου ἐπλήσθη ἡ σκηνή`. | The cloud was overshadowing the tent, and the tent was filled with the Lord's glory. The sanctuary contains the installed Ark; the grammar does not say “the cloud overshadowed the Ark.” |
| Luke 1:35 | `Πνεῦμα ἅγιον ἐπελεύσεται ἐπὶ σέ, καὶ δύναμις Ὑψίστου ἐπισκιάσει σοι`. | The Holy Spirit will come upon Mary; the Most High's power will overshadow her. The climax is Christological: the holy one born will be called Son of God. |
| Ps 90:4 LXX | `ἐν τοῖς μεταφρένοις αὐτοῦ ἐπισκιάσει σοι, καὶ ὑπὸ τὰς πτέρυγας αὐτοῦ ἐλπιεῖς`. | Exact Luke collocation plus sheltering wings. This does not cancel Exodus; it shows that Luke's wording can join sanctuary-presence and protective-wing resonances. |

Publication-safe synthesis (**C / P / R**):

> The Greek Exodus says that the cloud was overshadowing the completed
> sanctuary in which the Ark had been placed; Gabriel says that the power of
> the Most High will overshadow Mary. The rare shared verb, reinforced by
> Luke's Transfiguration cloud, gives the Annunciation a sanctuary resonance.
> Psalm 90:4 supplies Luke's exact two-word collocation and adds the tenderness
> of sheltering wings. The old dwelling held the sign of the Presence; Mary
> freely receives the incarnate Son himself.

## Luke 1 / 2 Reigns 6 correspondence matrix

| Correspondence | Exact textual control | Classification | Safe publication claim |
| --- | --- | --- | --- |
| Arise and go | 2 Reigns 6:2 `ἀνέστη καὶ ἐπορεύθη Δαυιδ`; Luke 1:39 `Ἀναστᾶσα … Μαριὰμ … ἐπορεύθη`. | T / M; direct but common verbal echo | Luke opens Mary's journey with the same ordinary biblical travel verbs and the identical final finite form used of David. Its importance emerges only with the following parallels. |
| Judah and uplands | 2 Reigns 6:2 names Judah; v. 3 has Abinadab's house `ἐν τῷ βουνῷ`. Luke 1:39 has `εἰς τὴν ὀρεινὴν … εἰς πόλιν Ἰούδα`. | S; geographic and structural | Both journeys unfold in Judah amid upland geography. X: identical hill vocabulary, an identified same town, or a recovered common road. |
| Entry into a house | Ark: `εἰς οἶκον Αβεδδαρα` (2 Reigns 6:10). Mary: `εἰσῆλθεν εἰς τὸν οἶκον Ζαχαρίου` (Luke 1:40). | T / S; shared `οἶκος`, distinct households | A holy bearer enters a household in each narrative. |
| Blessing at the arrival | The Lord blesses Obed-edom's whole house (2 Reigns 6:11). Elizabeth is filled with the Spirit and pronounces Mary and the child blessed (Luke 1:41--42). | S / C; strong sequence, different syntax and objects | The Ark enters a house and the Lord blesses it; Mary enters bearing the Lord and Spirit-filled blessing erupts. X: “Luke says Mary caused the whole house to be blessed.” |
| Cry and voice | Ark ascent: `μετὰ κραυγῆς καὶ μετὰ φωνῆς` (2 Reigns 6:15). Elizabeth: `ἀνεφώνησεν κραυγῇ μεγάλῃ`; later `ἡ φωνὴ τοῦ ἀσπασμοῦ σου` (Luke 1:42, 44). | T / M; direct lexical field plus rare cultic verb | The Ark's ascent sounds with cry and voice; Elizabeth's great cry and the voice of Mary's greeting welcome the hidden Lord. The publication follows SBLGNT's `κραυγῇ` at Luke 1:42. |
| David and John | Standard 2 Reigns 6:16: David `ὀρχούμενον καὶ ἀνακρουόμενον`, present middle participles from `ὀρχέομαι` and `ἀνακρούω`. Luke 1:41, 44: John `ἐσκίρτησεν` from `σκιρτάω`. | S; strong narrative image, no standard-LXX same-verb echo | David's body becomes praise before the arriving Ark; John's body becomes praise before the mother of his Lord. The standard Septuagint verbs differ. |
| Wondering question | 2 Reigns 6:9 `πῶς εἰσελεύσεται πρός με ἡ κιβωτὸς κυρίου;`; Luke 1:43 `πόθεν μοι τοῦτο ἵνα ἔλθῃ ἡ μήτηρ τοῦ κυρίου μου πρὸς ἐμέ;`. | T / S; strong structural and theological echo | Elizabeth's question is shaped strikingly like David's. It is not a verbatim quotation: `εἰσελεύσεται` is future middle indicative 3sg of `εἰσέρχομαι`; `ἔλθῃ` is aorist active subjunctive 3sg of `ἔρχομαι`. The lexically closer coming-question at 2 Reigns 24:21 qualifies but does not cancel the Ark-context echo; see below. |
| Three months | 2 Reigns 6:11 `ἐκάθισεν ἡ κιβωτὸς … μῆνας τρεῖς`; Luke 1:56 `ἔμεινεν δὲ Μαριὰμ … ὡς μῆνας τρεῖς`. | T / M / S; exact core phrase, different verbs | The Ark remains in Obed-edom's house three months; Mary remains with Elizabeth about three months. |
| Return home | 2 Reigns 6:19 `ἀπῆλθεν … εἰς τὸν οἶκον αὐτοῦ`; 6:20 `ἐπέστρεψεν … τὸν οἶκον αὐτοῦ`; Luke 1:56 `ὑπέστρεψεν εἰς τὸν οἶκον αὐτῆς`. | S; weak generic closure; verbs differ | May serve as a closing cadence, not a pillar of the argument. |

The narrative sequences are not mechanically identical. In Samuel the public
cry and David's dance follow the three-month stay; in Luke Elizabeth's cry and
John's leap precede Mary's stay. “Constellation,” “ordered cluster,” or “chain
of echoes” is accurate. “Exact lockstep rewriting” is not.

The serious alternative for Elizabeth's question is 2 Reigns 24:21:
`Τί ὅτι ἦλθεν ὁ κύριός μου ὁ βασιλεὺς πρὸς τὸν δοῦλον αὐτοῦ;`. Its
coming-question frame and `ἦλθεν … πρὸς` are lexically closer to Luke's
`πόθεν μοι … ἵνα ἔλθῃ … πρὸς ἐμέ` than 6:9 is. It lacks the Ark context,
however. The proposed 6:9 echo therefore rests on the complete Ark-journey
cluster, while 24:21 prevents an exaggerated claim of exclusive verbal source.

### The `ἀναφωνέω` result

The publication may say that Luke gives Elizabeth a verb found nowhere else
in the replayably checked Greek New Testament lemma boundary and that the
identified Greek Chronicles passages use the same lemma in Ark and sanctuary
worship (1 Chr 15:28; 16:4, 5, 42; 2 Chr 5:13). It must not publish a restricted
Old Testament corpus total, imply an exhaustive search, say that every locus
describes Ark transport, or claim that the word alone proves the typology.

### David, John, standard LXX, and Symmachus

The Rahlfs 1935 main text at 2 Reigns 6:14, 16, also visible in the public
Rahlfs--Hanhart running-text presentation, uses
`ἀνακρούω` and, in v. 16, `ὀρχέομαι`; it does **not** use `σκιρτάω` of David.
The adjective `ἔξαλλον` in v. 14 modifies a garment and is not a verb meaning
“leaped.” Luke uses `σκιρτάω` of John.

Benedict XVI's Assumption homily of 15 August 2011 carefully says that “one of
the ancient Greek translations of the Old Testament” uses the same term for
David's dance that Luke uses for John's leap:
<https://www.vatican.va/content/benedict-xvi/en/homilies/2011/documents/hf_ben-xvi_hom_20110815_assunzione.html>.
Field, *Origenis Hexaplorum quae supersunt* I (1875), p. 555, prints the
fragment at 2 Reigns 6:16 under `Σ.` (Symmachus) as
`σκιρτῶντα καὶ καγχάζοντα`. `σκιρτῶντα` is the present active participle,
accusative masculine singular, of `σκιρτάω`; Luke's `ἐσκίρτησεν` is an aorist
active indicative, third singular. Thus this is a same-lemma/same-family link,
not the same inflected form. Benedict does not name Symmachus in the homily.
Brooke--McLean--Thackeray, *The Old Testament in Greek* II.1 (1927), p. 125,
independently gives the same Symmachus reading in its apparatus. Symmachus is
later than Luke, and the fragment survives indirectly; it witnesses an ancient
Greek rendering and later reception of the image, not Luke's dependence.
The checked scans are Field at
<https://archive.org/details/origenishexaplor01origuoft/page/n666/mode/1up>
and Brooke--McLean--Thackeray at
<https://archive.org/details/p2oldtestamentin01broouoft>.
The publication therefore distinguishes three claims:

1. **T / S:** the standard LXX and Luke have different verbs but a strong
   narrative-image correspondence;
2. **R:** Benedict officially receives the David--John correspondence and
   accurately describes his same-term observation as belonging to one ancient
   Greek translation, without claiming the same inflected form; and
3. **L / T:** the same-lemma detail belongs to the Symmachus fragment
   tradition, not the standard LXX. Field's printed fragment has been visually
   checked, but its fragmentary transmission is recorded rather than merged
   into Rahlfs or represented as a fresh critical reconstruction.

X: “The Septuagint uses the same word for David and John.”

## Ark contents and Christological fulfillment

| Canonical witness | Exact inventory claim | Publication boundary |
| --- | --- | --- |
| Exod 25:10--22; Deut 10:1--5 | Acacia-wood Ark overlaid with gold; covenant tablets placed inside. | The tablets are the Torah's unambiguous interior deposit. |
| Exod 16:32--34 | Manna jar placed “before the Lord” and “in front of the covenant.” | Exodus does not explicitly place it inside the chest. |
| Num 17:25 (17:10 in some traditions) | Aaron's sprouted staff returned “in front of the covenant.” | Numbers does not explicitly place it inside. Record the versification difference. |
| Deut 31:24--26 | Completed Torah scroll placed beside the Ark. | Do not merge scroll and tablets or put the scroll inside. |
| 1 Kgs 8:9; 2 Chr 5:10 | At Solomon's dedication only the two tablets are inside. | Do not invent a removal/loss chronology for manna and staff. |
| Heb 9:3--5 | Greek `ἐν ᾗ` naturally refers to feminine `κιβωτός`; Hebrews presents the manna jar, Aaron's staff, and tablets “in” the Ark. | Direct canonical source for the familiar threefold interior inventory. |

Publication-safe Catholic synthesis (**C / P / R**):

> The old Ark bore the covenant's sacred witnesses; Mary bore the one Person in
> whom their promises converge: the living Word and New Covenant, the true
> Bread from heaven, and the definitive High Priest.

The tablets/Word and manna/Bread relations are explicit canonical and Catholic
syntheses (John 6:32--51). The staff/vindicated priesthood relation is a
theological synthesis from Numbers 17 and Hebrews. Christ is not simply
Aaron's successor; Hebrews calls his priesthood Melchizedekian (Heb 5:5--10;
7:11--17). The inventory explains the Christological density of the Ark title;
it is not a mechanical code and does not reduce Mary to a container.

## Revelation 11:19--12:1

- Revelation 11:19 shows the heavenly temple opened and the Covenant Ark seen
  within it.
- Revelation 12:1 immediately presents a great sign in heaven, a Woman who
  bears the messianic ruler; 12:17 requires a corporate people-of-God horizon
  because the Woman has further offspring who keep God's commandments and
  testify to Jesus.
- Both scenes use `ὤφθη` and heavenly vision language. The syntax is not
  identical: in 11:19 `ὁ ἐν τῷ οὐρανῷ` modifies the temple and precedes
  `ὤφθη ἡ κιβωτός`; in 12:1 the sequence is
  `σημεῖον μέγα ὤφθη ἐν τῷ οὐρανῷ`.
- Revelation 12:3 then repeats the vision formula:
  `καὶ ὤφθη ἄλλο σημεῖον ἐν τῷ οὐρανῷ`. This internal control excludes a
  claim that the 11:19--12:1 wording is unique.
- Revelation gives no grammatical apposition “the Ark, that is, the Woman.”

Publication-safe reception (**C / R / P**):

> John sees the Covenant Ark in the opened heavenly temple; immediately
> afterward a great sign appears in heaven, the Woman who bears the Messiah.
> Revelation does not grammatically rename the Ark as the Woman. Yet their
> adjacency, the repeated heavenly manifestation, Mary's personal motherhood
> of the Messiah, and her inseparability from Israel and the Church make the
> sequence a natural home for Catholic New-Ark contemplation.

The Roman Assumption Lectionary proclaims Rev 11:19a; 12:1--6a, 10ab together.
Benedict XVI's 2011 Assumption homily receives the sequence as a suggestion of
Mary's bodily glory. This is strong liturgical and canonical fittingness, not
a standalone photographic proof of the Assumption.

## Official Catholic reception

- CCC 2676 calls Mary “the ark of the covenant” and the place where the Lord's
  glory dwells:
  <https://www.vatican.va/content/catechism/en/part_four/section_one/chapter_two/article_2/the_way_of_prayer.html>.
- Benedict XVI, Assumption homily, 15 August 2011, calls Mary the living Ark,
  traces the Ark/Visitation correspondence, makes the ancient-Greek-version
  distinction, and joins the heavenly Ark to Assumption fittingness:
  <https://www.vatican.va/content/benedict-xvi/en/homilies/2011/documents/hf_ben-xvi_hom_20110815_assunzione.html>.
- Benedict XVI, Angelus, 23 December 2012, grounds the threefold Ark inventory
  in Hebrews 9:4 and calls Mary the Ark because she carries Jesus:
  <https://www.vatican.va/content/benedict-xvi/en/angelus/2012/documents/hf_ben-xvi_ang_20121223.html>.
- The Roman-rite Assumption reading is Rev 11:19a; 12:1--6a, 10ab:
  <https://bible.usccb.org/es/node/18968>.

These official witnesses establish Catholic reception of the typology. They
do not replace the direct textual controls above or convert every theological
fittingness into the literal sense of a verse.

## Rejected or bounded formulations

| Formulation | Disposition | Reason |
| --- | --- | --- |
| “Luke explicitly calls Mary the Ark.” | X | Luke never uses `κιβωτός` of Mary. The identification is cumulative canonical typology and received interpretation. |
| “The Hebrew Exodus says the Shekinah overshadowed the Ark.” | X | Hebrew says the cloud covered the tent and settled/dwelt upon it; the noun *Shekinah* is absent. Greek Exodus uses `ἐπισκιάζω` of the tent containing the installed Ark. |
| “Overshadow is a unique Ark word.” | X | The identified witnesses use the verb outside Ark settings, including the Transfiguration and apostolic contexts; the exact Luke phrase also appears in Ps 90:4. |
| “Luke uses the same dance verb as the Septuagint.” | X | Standard Rahlfs uses `ὀρχέομαι` and `ἀνακρούω`; the same-lemma link belongs to a Symmachus-attributed rendering preserved in later Hexaplaric witnesses. |
| “Every Septuagint use of `ἀναφωνέω` describes the Ark being carried.” | X | 1 Chr 16:42 is sanctuary music but does not name Ark or transport in that verse. |
| “Elizabeth quotes David word for word.” | X | Strong structural question; different interrogative, motion verbs, syntax, and referent. |
| “The events occur in exactly the same order.” | X | Samuel's public joy follows the three-month stay; Luke's precedes it. The cluster, not lockstep order, is the evidence. |
| “Exodus says tablets, manna, and staff were all inside the Ark.” | X | Exodus and Numbers say “before”; Hebrews 9:4 supplies the direct threefold interior inventory. |
| “Revelation grammatically identifies the Woman as the Ark.” | X | Immediate adjacency and repeated vision language, not apposition or identical syntax. |
| “Uzzah proves Joseph could not touch Mary.” | X | No Lucan lexical or narrative link; no authenticated patristic source located for that claim; Matthew gives Joseph a positive command to take Mary as wife. At most Uzzah supplies a distant devotional contrast between unappointed handling and commanded reception. |

## Scholarly disagreement and confidence statement

The Ark reading is strong but not an uncontested modern critical consensus.
Jan M. Kozłowski's “Mary as the Ark of the Covenant in the Scene of the
Visitation (Luke 1:39–56) Reconsidered” supports the reading while documenting
objections from Raymond Brown, François Bovon, Heinz Schürmann, Joseph
Fitzmyer, and Mark Strauss, including the alternative verbal analogue of
2 Reigns 24:21 for Elizabeth's question:
<https://czasopismowst.pl/index.php/wst/article/download/159/100/318>.

The publication's confidence rests on the whole evidence set:

1. direct sanctuary-presence resonance at Luke 1:35;
2. an ordered 2 Reigns 6 / Luke 1 cluster too dense to dismiss as one common
   phrase;
3. the NT-hapax `ἀναφωνέω` concentrated in Septuagintal Ark/sanctuary worship;
4. the canonical contents fulfilled in the identity of Christ;
5. ancient patristic and continuing liturgical recognition; and
6. explicit modern Catholic reception.

This supports “strong, cumulative Catholic typology.” It does not require
“philologically certain authorial code,” and it is much more than a free later
analogy.

## Rights, quotation, and review state

- Greek and Hebrew snippets are short, claim-specific portions used for
  textual analysis. No modern translation or critical apparatus is reproduced
  at length.
- SBLGNT, the CATSS/RLXX1935-derived machine corpora, official Bible
  presentations, and Vatican pages retain their own edition, license,
  restrictions, and hosting status. Links do not imply repository ownership.
- Repository-replayable New Testament counts are bound to the retained
  MorphGNT lemma projection. Restricted Greek Old Testament query receipts
  remain transparent research leads only; no published total or exclusivity
  claim depends on them, and their bindings deliberately do not claim a
  replayable searched state.
- Internal Greek, Hebrew, canonical, and adversarial checks support this audit.
  Independent human specialist review in Septuagint, Hexaplaric fragments,
  Lucan studies, and Catholic biblical theology remains outstanding.
- This audit records research review only. It does not claim completed PDF/web
  production review, ecclesiastical approval, or external scholarly approval.
