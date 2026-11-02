# Celebration context and complete appointed inventory

Resolved 27 October 2026 for the `proper-study` v15 production of the Claude
1962 leaf, run `450355254538c1ba`, seeded at commit
`4f52b9ade338f9a9f4f39f312aa45989a0baf2ca`. The production-plan entry of
2026-10-26 in `guidance/liturgy/propers-production-plan.md` authorizes provider
`claude` for this one identity, independent of the other provider's leaf, and
does not open the commemorated Twenty-third Sunday after Pentecost as a target.
It grants no reference-only authorization, so this production runs in the
ordinary `complete` publication mode, which the manifest already declares
(`appointed_text_completeness = "complete"`, canonical label *Full PDF*).

`ARGS.research_handoff` is
`workflows/reviews/claude-1962-f02-revision-2026-10-27/HANDOFF.md`. It was read
as a set of untrusted leads. Every fact below that it also states was checked
against the sources named here, and the leads this stage did not check are
listed under *Remaining verification for research*. As the handoff requires,
the first run's archive under `evaluations/proper-study-results/427e2f58bb897a16/`
was not opened, no removed file was recovered from history, and the other
provider's leaf for this identity, its outputs and its workflow records were
not opened. No postconciliar record or calendar row is evidence here. The
Claude Christ the King context record was read only as a model of this
record's shape; none of its findings is relied on. This record settles what is
studied. It holds no study prose, spoken text, timing claim or review verdict.
The research stage collates the sources and may correct it from evidence.

## Identity, governing books and territory

- Canonical identity:
  `liturgy/roman-rite/1962/propers/temporal/f02-all-saints`, catalog ID `F02`
  in `guidance/liturgy/roman-1962-propers.md` (the `F` series of
  general-calendar feasts that fall on a Sunday), calendar family `roman-1962`.
  `tools/check-proper-identity` passes for the leaf. The finding-aid mass index
  `src/sources/calendars/roman-1962/propers.yaml` carries the formulary as
  `omnium-sanctorum`, `registry: 'F02'`, date `11-01`, rank `I`. That entry
  records scripture citations only and is a lead, never the source of record
  for wording (see *Shared records* for where it departs from the page).
- Governing edition: *Missale Romanum*, editio typica, Typis Polyglottis
  Vaticanis 1962 (`edition.catholic-church.missale-romanum.vatican-typica-1962`),
  controlled on the page images of
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.
  The copy read in this stage matched the registered SHA-256
  `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` and
  82,815,941 bytes before any page was read. The feast's formulary (PDF pp.
  783-784) and the Twenty-third Sunday's (PDF pp. 497-498) were read on page
  images at 200 dpi and again at 400 dpi, both columns of each page. The
  *Calendarium*, the general rubrics and the two Prefaces cited below as
  "read" were read on 200-dpi page images. The text layer served only to
  locate pages and to cross-check conclusions already read on the image; loci
  marked "located" were found on it and not re-read on an image.
- Printed place, heading and rank. The feast stands in the **Sanctorale**:
  printed p. 701 ends the formulary of Ss Simon and Jude; printed p. 702 (PDF
  783), headed *Festa novembris*, opens *Die 1 novembris* / *IN FESTO OMNIUM
  SANCTORUM* / *I classis*; the formulary runs through printed p. 703 (PDF 784),
  marginal nos. 3974-3983, whole and legible. Printed p. 704 (PDF 785) begins
  the separate *Missa votiva de omnibus Sanctis* (no. 3984 onward, with its own
  Tract and paschal Alleluia), which is a different formulary for other days
  and is excluded. No vigil of All Saints is printed between pp. 701 and 702.
- Governing books within that edition, read or located where cited below: the
  *Calendarium*; the *Rubricae generales* (part I of the 1960 code as printed,
  cited RG); the *Rubricae generales Missalis romani* (part III, cited RGMR);
  the *Ordo Missae*; the *Praefationes*; the Proper of Time (for the
  commemorated Sunday); the Sanctorale. Part II, the *Rubricae generales
  Breviarii romani*, is not printed in this witness.
- Territory: the universal 1962 General Roman Calendar. No diocese, church
  titular or dedication, religious institute or other particular calendar was
  supplied, so no local overlay is applied or computed.
- Language: Latin governs. Every English route below is a historical study
  aid, not an approved vernacular liturgical text.
- Cycle: the 1962 Missal appoints the readings with the formulary and has no
  Lectionary cycle. No A/B/C or I/II value exists. The requested identity and
  the formulary appointed on the requested date are the same; the Sunday that
  the feast displaces enters only as a commemoration (below).
- Season: *tempus « per annum »* after Pentecost; the feast's colour is white
  (RG 120 d, below), not the season's green.
- Homily audience for the later homily stage: adult parish assembly
  (`ARGS.audience`). The homily is authored preaching and adds no text to this
  inventory.

## Occurrence on 1 November 2026

**The date.** 1 January 2026 is a Thursday, so 1 November 2026 is a Sunday.
The *Calendarium* for November (printed p. LII, PDF 54, read) gives the
Kalends *OMNIUM SANCTORUM, I cl.* `tools/tpt calendar-days day --calendar
roman-1962 --date 2026-11-01` returns two candidates, `omnium-sanctorum` (I)
and `pentecost-23` (slot 23 of 26 Sundays after Pentecost), nothing
unresolved. The Twenty-third Sunday is not displaced to another date in 2026:
22 November is the Twenty-fourth and last Sunday after Pentecost, so the
transposition rubric printed with the Twenty-third Sunday (p. 417, for years
in which the last Sunday impedes it) does not apply.

**Precedence (computation is a finding aid; every locus was read).**
`tools/tpt calendar-rubrics day --calendar roman-1962 --date 2026-11-01`
gives the winner `omnium-sanctorum` (RG 91 row 11) and the Sunday commemorated
as privileged (RG 109 a) in every Mass, low and sung non-conventual alike. The
loci read on the page images:

- RG 91, table of precedence, printed p. XVII (PDF 15): row 11, the
  first-class feasts of the universal calendar, outranks row 15, *Dominicae II
  classis*. Row 8 (All Souls) is below a Sunday; RG 96 b transfers All Souls
  falling on a Sunday to the Monday. In 2026 All Souls is Monday 2 November in
  any case, so nothing is transferred.
- RG 109 a (printed p. XVIII, PDF 16): the commemoration of a Sunday is
  privileged. RG 111 a (same page) admits on a first-class day, and in sung
  non-conventual Masses, no commemoration *praeter unam privilegiatam*; RGMR
  434 a (printed p. XXXI, PDF 29) states the same for the Mass. RG 113 puts
  the commemoration *de Tempore* first. The Sunday is therefore commemorated,
  once, in every Mass of the day.
- RGMR 436-437 (PDF 29): the Mass's own oration is said under its own
  conclusion; commemorations are said *sub altera conclusione*. RGMR 480-481
  and 505 (PDF 32-33): as many Secrets and Postcommunions are said as orations
  were said at the beginning, in the same order and with the same
  conclusions.

The result is one branch: in every Mass of the day, sung or low, conventual or
not, the feast's formulary with the Sunday's Collect, Secret and Postcommunion
after the feast's own, each under its own conclusion. There is no low-versus-sung
difference in the orations.

**Orations excluded on this date** (RGMR, printed p. XXXII, PDF 30, read):
RGMR 457 d forbids the *oratio imperata* on all first- and second-class days,
and RGMR 461 (p. XXXIII, PDF 31) admits the *oratio votiva ad libitum* only on
fourth-class days. The ceiling of RGMR 434 a leaves no room for a third
oration. RGMR 449 (coronation and anniversaries of the Pope and of the
diocesan bishop) and RGMR 451 (*pro seipso sacerdote*) except only the days of
rows 1, 2, 3 and 8 of the table, and All Saints is row 11; they arise only on
those anniversaries, which are local and personal facts not computed here. A
study must not present either as part of the day's Mass.

**No substitute Mass.** The votive Mass of All Saints (p. 704) belongs to
other days. Masses of the dead and particular-calendar Masses are not
considered.

**Colour, Gloria, Credo, Offertory Alleluia, Preface and last Gospel** (read):

- White: RG 120 d (printed p. XIX, PDF 17) names the feast of All Saints.
- Gloria: RGMR 431 a-b (p. XXXI, PDF 29), the festive Mass of a day with the
  *Te Deum* at Matins.
- Credo: RGMR 475 a and b (p. XXXIII, PDF 31), *in qualibet dominica, etsi eius
  Officium alicui festo locum cedat*, and *in festis I classis*; printed cue
  *Credo.* after the Gospel.
- The Offertory's *alleluia*: RGMR 478 (PDF 31) keeps an *Alleluia* printed at
  the end of an Offertory antiphon outside paschal time, except from
  Septuagesima to Easter. It is therefore said.
- **Preface: unresolved; two candidates, neither asserted.** The feast's page
  prints no Preface direction. The Sunday's page prints *Praefatio de Ssma
  Trinitate.* after its Secret. RGMR 482 (printed p. XXXIV, PDF 32): *Praefatio
  dicitur quae cuique Missae propria est; qua deficiente, dicitur praefatio de
  Tempore, secus communis.* RGMR 494 b makes the Trinity Preface the Preface
  *de Tempore* *in dominicis Adventus, et in omnibus dominicis II classis,
  extra tempus natalicium et paschale*. RGMR 483: *Nulla commemoratio, in
  Missa occurrens, praefationem propriam inducit.* RGMR 498: the common Preface
  is said in Masses that lack a proper Preface *nec sumere debent praefationem
  de Tempore*. The seasonal rubrics on the same page extend their Prefaces to
  other Masses in express words (486 b, 489 b, 493 b: *in ceteris Missis quae
  celebrantur eodem tempore, et praefatione propria carent*; 487 b, 490 b: *in
  omnibus Missis … quae praefatione propria carent*); 494 b says only *in
  dominicis*. The governing edition's closest direction is the Vigil of the
  Nativity, a first-class Mass that is not the Sunday's, printed p. 16 (PDF 97,
  after Secret no. 105, page image read): *Praefatio communis; sed, si venerit
  in dominica, dicitur de Ss.ma Trinitate.* It is the only Preface direction
  conditioned on a Sunday that the facsimile's text layer shows. Read as an
  application of 482 and 494 b, it gives a Mass without its own Preface the
  Sunday's Preface *de Tempore*, and the same reasoning gives All Saints the
  Trinity Preface (candidate 1: *Praefatio de Ss.ma Trinitate*, *Praefationes
  sine cantu*, printed p. 293, no. 1082, PDF 374, read). Read as a special
  exception, printed because 494 b, unlike the seasonal rubrics, does not reach
  other Masses, it leaves a feast that takes the Sunday, which is present only
  as a commemoration inducing no Preface (483), with the common Preface
  (candidate 2: *Praefatio communis*, p. 297, no. 1086, PDF 378, read). The
  Vigil meets only an Advent Sunday, which 494 b names in its own clause; the
  Twenty-third Sunday after Pentecost falls under *in omnibus dominicis II
  classis* (research/scope.md 3.11). The dated ICRSP Ordo (below) directs the
  Trinity Preface; that is one institute's direction, not a rubric of the
  Missal. No registered rubrical commentary read treats the case; Murphy 1960
  was not re-read. The study names both candidates with their basis and
  asserts neither unless research finds a registered authority that settles it.
- **Last Gospel: John 1:1-14.** RGMR 509 (printed p. XXXV, PDF 33): *Pro ultimo
  Evangelio, in quavis Missa, regulariter sumitur initium Evangelii secundum
  Ioannem*, with only the Palm Sunday exception; none of the omission cases of
  RGMR 510 applies. The ICRSP Ordo instead gives the Twenty-third Sunday's
  Gospel as last Gospel, which is not the 1960 rubric. The discrepancy is
  recorded; the study follows RGMR 509.

**Dated official witnesses.** Ordos of institutes that celebrate with the 1962
books were fetched live for this date on 2026-10-27 (17:29 UTC) and held only in
this run's scratch area. Their SHA-256 values are recorded so that research can
compare them with the registered dated records from 2026-10-26.

- ICRSP France, *Ordo*, <https://icrspfrance.fr/ordo.php?d=2026-11-01>,
  111,041 bytes, SHA-256
  `b6fb36e5891ebddaedf518b47a00fef492f70afb6b671f6247bd3f10ca1310e3`
  (the registered artifact `artifact.icrsp-france.ordo.web-2026-10-26.html-af2285ec`
  has a different hash): *Toussaint*, first class, white; Gloria, Credo, no
  *Oratio pro Papa*; *Préface de la T. Ste Trinité*; *Mém. du XXIIIe Dim.*;
  *Dernier Évangile du XXIIIe dimanche*.
- FSSP France, *Ordo du mois*, <https://www.fssp.fr/ordo-du-mois/>, 165,226
  bytes, SHA-256
  `53571bf38150e5bfbe335e0cd445b60ebc29a9f6146c717e693d263f15674d6f`:
  *Toussaint (1ère classe, Blanc)*. One line per day; its silence on the
  commemoration is not read as evidence.
- FSSPX Ordo, texts API
  <https://ordo.fsspx.org/api/v1/calendar/2026/11/1/texts>, 11,425 bytes,
  SHA-256 `5404783db2625d3f59dbc4281080d7c6f954549803df227a51b714e8898d221f`,
  identical to the registered
  `artifact.fsspx.ordo.web-2026-10-26.texts-json-5404783d`: the celebration
  *Toussaint*, rank 1, white; the commemoration *23e Dimanche après la
  Pentecôte*, rank 2; the Collect, Secret and Postcommunion each followed by
  the Sunday's under its own conclusion; no Preface item; a day of precept.
  The day page <https://ordo.fsspx.org/day/2026-11-01> (186,674 bytes, SHA-256
  `af79f335dbd8550c4bf755530effe277a863f49a46da35f2a416c656a96cc66a`, same
  length as and different hash from the registered `day-html-81bb6438`) names
  no Preface.

Computation, the printed calendar and rubrics, and the three witnesses agree on
the identity, the first class, the white colour and the Sunday's
commemoration; the ICRSP and FSSPX entries agree on the Gloria, the Credo and
the commemoration in all three orations. They do not settle the Preface (one
names Trinity, two are silent), and the ICRSP last-Gospel line conflicts with
RGMR 509. Nothing else fails closed. The Missale Meum page and Murphy 1960,
registered by the earlier research, are leads only and were not relied on
here.

## Appointed proper

Loci are the printed page and marginal number of the controlling edition, read
on 200- and 400-dpi page images. Psalms are cited in the Missal's Vulgate
numbering, with the Hebrew number in parentheses, from the repository's
concordance
`artifact.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581.psalm-numbering-ee3c7757`
(TSV SHA-256 `535761886df2…` recomputed and matched). Vulgate Ps 32:1 is the
same verse as Hebrew 33:1; Vulgate Ps 33:1 is the title, so Vulgate 33:10-11
is Hebrew 34:10-11 and English Bibles that follow the Hebrew number it 34:9-10.
The Douay-Rheims keeps the Vulgate number. "Said" means said in every Mass of
1 November 2026. The keys are those of `proper-components.toml` (schema 2,
fourteen elements), which the inventory confirms.

| Order and key | Element and printed locus | Liturgical place, extent and status |
|---|---|---|
| 1 `introit` | *Antiphona ad Introitum*, no printed scriptural citation for the antiphon; verse *Ps. 32, 1* (33:1); p. 702, no. 3974 | Said. Antiphon *Gaudeamus omnes in Domino, diem festum celebrantes sub honore Sanctorum omnium: de quorum solemnitate gaudent Angeli, et collaudant Filium Dei.*; verse *Exsultate, iusti, in Domino: rectos decet collaudatio.*; cue *V. Gloria Patri.*; repetition (RGMR 427). No Alleluia outside paschal time. |
| 2 `collect` | *Oratio* *Omnipotens sempiterne Deus, qui nos omnium Sanctorum tuorum merita sub una tribuisti celebritate venerari*; p. 702, no. 3975 | Said, first oration, under its own conclusion (RGMR 436); printed cue *Per Dominum.* |
| 3 `commemoration-collect` | Collect of the Twenty-third Sunday after Pentecost, *Absolve, quaesumus, Domine, tuorum delicta populorum*; Proper of Time, p. 416, no. 1720 (PDF 497) | Said after the Collect, under its own conclusion (RG 109 a, 111 a; RGMR 437 a); printed conclusion *Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.* The Sunday's other proper texts are not said. |
| 4 `lesson` | *Lectio libri Apocalypsis beati Ioannis Apostoli*, *Apoc. 7, 2-12*; p. 702, no. 3976 | Said in the place of the Epistle (RGMR 466). Opens *In diebus illis: Ecce ego Ioannes vidi alterum Angelum ascendentem ab ortu solis*; ends *in saecula saeculorum. Amen.* No shorter form. |
| 5 `gradual` | *Graduale* *Ps. 33, 10 et 11* (34:10-11); p. 703, no. 3977 | Said (RGMR 469). Respond *Timete Dominum, omnes Sancti eius: quoniam nihil deest timentibus eum.*; verse *Inquirentes autem Dominum, non deficient omni bono.* |
| 6 `alleluia` | *Alleluia, alleluia*, verse *Matth. 11, 28*; p. 703, no. 3978 | Said. Verse *Venite ad me, omnes qui laboratis et onerati estis: et ego reficiam vos.*, then *Alleluia.* No Tract, Sequence or paschal form is printed in this formulary. |
| 7 `gospel` | *Sequentia sancti Evangelii secundum Matthaeum*, *Mt. 5, 1-12*; p. 703, no. 3979 | Said. Opens *In illo tempore: Videns Iesus turbas, ascendit in montem*; ends *gaudete et exsultate, quoniam merces vestra copiosa est in caelis.* (verse 12a). Printed cue *Credo.* follows. |
| 8 `offertory` | *Ant. ad Offertorium* *Sap. 3, 1, 2 et 3*; p. 703, no. 3980 | Said, with its *alleluia* (RGMR 478). *Iustorum animae in manu Dei sunt, et non tanget illos tormentum malitiae: visi sunt oculis insipientium mori: illi autem sunt in pace, alleluia.* |
| 9 `secret` | *Secreta* *Munera tibi, Domine, nostrae devotionis offerimus*; p. 703, no. 3981 | Said secretly, first Secret (RGMR 480-481); printed cue *Per Dominum.* No Preface direction is printed. |
| 10 `commemoration-secret` | Secret of the Twenty-third Sunday, *Pro nostrae servitutis augmento sacrificium tibi, Domine, laudis offerimus*; p. 417, no. 1726 (PDF 498) | Said after the Secret, in the same order and under its own conclusion (RGMR 480-481); printed conclusion *Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.*; the conclusion of this last Secret is said aloud from *Per omnia saecula saeculorum*. Followed on its page by *Praefatio de Ssma Trinitate.*, which belongs to the Sunday's own Mass (see the Preface entry above). |
| 11 `preface` | Not printed with the formulary. Candidate 1: *Praefatio de Ss.ma Trinitate*, p. 293, no. 1082 (PDF 374, read). Candidate 2: *Praefatio communis*, p. 297, no. 1086 (PDF 378, read) | Said or sung; unresolved between the two (above). The Missal's closest direction (p. 16, the Vigil of the Nativity on a Sunday: *Praefatio communis; sed, si venerit in dominica, dicitur de Ss.ma Trinitate*) supports either reading. Neither is a chosen or local option, and neither may be presented as settled until research finds a registered authority. The notated tones elsewhere in the Missal were not read and are not needed for the inventory. |
| 12 `communion` | *Antiphona ad Communionem* *Matth. 5, 8-10*; p. 703, no. 3982 | Said (RGMR 504). *Beati mundo corde, quoniam ipsi Deum videbunt: beati pacifici, quoniam filii Dei vocabuntur: beati qui persecutionem patiuntur propter iustitiam, quoniam ipsorum est regnum caelorum.* |
| 13 `postcommunion` | *Postcommunio* *Da, quaesumus, Domine, fidelibus populis omnium Sanctorum semper veneratione laetari*; p. 703, no. 3983 | Said, first Postcommunion (RGMR 505); printed cue *Per Dominum nostrum.* |
| 14 `commemoration-postcommunion` | Postcommunion of the Twenty-third Sunday, *Quaesumus, omnipotens Deus: ut, quos divina tribuis participatione gaudere*; p. 417, no. 1728 (PDF 498) | Said after the Postcommunion, under its own conclusion (RGMR 437 a, 505); printed conclusion *Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.* |

The orations are given above by incipit; their complete wording is collated by
research against the same page images (the earlier passage records
`passage.catholic-church.missale-romanum.vatican-typica-1962.all-saints-four-own-propers-word-collation-2026-10-20`
and `…temporal-pentecost-23-orations` are registered and are to be re-read,
not trusted). The formulary prints no Tract, Sequence, prophecy, proper
*Communicantes* or *Hanc igitur* (RGMR 501), *Oratio super populum*,
commemoration rubric, blessing or alternative reading. The commemoration
comes from the rubrics, not from a direction on the feast's page.

### Wording against the Clementine Vulgate

Compared against the tracked Clementine Vulgate
(`edition.catholic-church.vulgata-clementina.ebible-latvuc`) through
`tools/tpt mass-propers show --calendar roman-1962 --mass omnium-sanctorum
--bible clementine-vulgate`. These are textual observations about wording and
boundary. No origin is asserted for any form.

- **Introit.** The antiphon is not a biblical text. The verse is Ps 32:1
  without the Clementine's title words *Psalmus David.*
- **Lesson.** The liturgical opening *In diebus illis: Ecce ego Ioannes vidi*
  stands for the Clementine's *Et vidi* at 7:2. Otherwise only orthography
  differs (*milia* for *millia*, *Nephtali*, *Beniamin*, *Iuda*). At 7:11 it
  is the angels, standing round the throne, the ancients and the four living
  creatures, who fall on their faces before the throne.
- **Gradual.** It departs from the Clementine Ps 33:10-11: *omnes Sancti eius:
  quoniam nihil deest timentibus eum* where the Clementine has *quoniam non est
  inopia timentibus eum*; it omits *Divites eguerunt, et esurierunt*; and it
  reads *non deficient* for *non minuentur*. The source of the Gradual's form
  is for research; no psalter is named here.
- **Alleluia.** Agrees with Mt 11:28.
- **Gospel.** The liturgical opening *In illo tempore: Videns Iesus* stands
  for *Videns autem Jesus*. The pericope ends at 12a (*in caelis*) and omits
  *Sic enim persecuti sunt prophetas, qui fuerunt ante vos*.
- **Offertory.** Against Wis 3:1-3: omits *autem*; *tanget* for *tangent*;
  *malitiae* for *mortis*; omits 3:2b-3a (*et aestimata est afflictio exitus
  illorum, et quod a nobis est iter exterminium*); adds *alleluia*. This
  confirms handoff lead 3.
- **Communion.** Mt 5:8-10, verbatim apart from pointing.

## Other text-bearing parts of this Mass

Fixed or rubrically appointed texts of the 1962 *Ordo Missae*, not proper
text. The study refers to them and does not reproduce the Ordinary. *Ordo
Missae* marginal numbers are those of the registered passage records
`…vatican-typica-1962.ordo-missae-ad-gradum`, `…ordo-missae-kyrie-gloria`,
`…ordo-missae-credo`, `…ordo-missae-conclusio` and
`…ordo-ad-aspergendam-aquam-benedictam`, located and not re-read on images.

| Place | Text and appointment | Status and source |
|---|---|---|
| Before the principal Sunday Mass, where used | *Asperges me* with the blessing of water | A Sunday rite outside the Mass and outside this formulary; not part of the appointed inventory. Whether it is kept when a feast takes the Sunday is for research, only if the study relies on it. |
| Prayers at the foot of the altar | Ps 42 *Iudica me* through *Oramus te*; nos. 1013-1023 | Said: RGMR 425 (PDF 29, read) omits *Iudica* only in Passiontide and in Requiem Masses. |
| Introit doxology; Kyrie | *Gloria Patri*; ninefold Kyrie, no. 1024 | RGMR 427-428, 430 (PDF 29, read). |
| After the Kyrie | *Gloria in excelsis*, no. 1025 | Said: RGMR 431 (read). No chant setting is chosen. |
| Before and after the Gospel | *Munda cor meum*, Gospel dialogue; homily | RGMR 471, 474 (PDF 31); nos. 1026-1028. |
| After the Gospel or homily | *Credo*, no. 1029 | Said: RGMR 475 a, b (read); printed cue after no. 3979. |
| After the Secrets | Preface, then *Sanctus* | Element 11 above; unresolved between nos. 1082 and 1086. |
| Canon | *Te igitur* through the doxology | The one Roman Canon, said secretly (RGMR 500, read); no proper insertion (RGMR 501, read). |
| Conclusion | *Ite, missa est*, *Placeat*, blessing, last Gospel Jn 1:1-14 | RGMR 507-509 (509-510 read); nos. 1132-1139 per the registered conclusion passage. |

## Lawful study-text routes

The Latin rights basis follows
`src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`: the
1962 facsimile is a collation witness, and 17 U.S.C. 103(b) frees only
preexisting material, so each element needs a pre-1931 public-domain witness
collated with the 1962 page.

- **Latin, the feast.** The Mame 1922 typical-edition printing
  (`edition.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam`), parent PDF pp. 862-864 = printed pp. 748-750,
  in the registered page extract `…1922-tours-mame-editio-quarta-iuxta-typicam.all-saints-1922-pages-0682b2da`
  and the checked derivatives `…all-saints-four-propers-la-checked-82edd79a`
  and `…all-saints-scriptural-propers-la-checked-415a1d46`; each file matched
  its registered hash in this stage, and the Offertory page image was read
  (it prints *malitiae* and *alleluia*). Its forms are *Joannes*, *Juda*,
  *justitiam*, *Justorum* (handoff lead 6 confirmed). Research found that the
  scriptural derivative `…415a1d46` does not keep all of Mame's forms
  (research/scope.md section 2); the page images, not that derivative, carry
  Mame's orthography. The Latin provenance
  ledger `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml`
  has four `omnium-sanctorum` rows (Introit, Collect, Secret, Postcommunion)
  verified against the 1962 four-element collation; it has no row for the
  Lesson, Gradual, Alleluia, Gospel, Offertory or Communion. Research must
  collate those six against Mame 1922 and record the basis it relies on.
  A registered editorial projection from the earlier run,
  `…2026-10-25-f02-editorial-projection.f02-remaining-nine-latin-f645e8ee`,
  exists in the shared library; it was not read here, and research re-derives
  the collation rather than trusting it.
- **Latin, the commemoration.** The ledger has three `pentecost-23` rows
  (Collect, Secret, Postcommunion) verified against the 1962 passage record.
  The Pustet 1862 extract
  `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.pentecost-23-prayer-pages-7e6ef53b`
  (parent PDF pp. 443-444) matched its registered SHA-256
  `7e6ef53bd1a1114e23f1110fb81b8a221cb837932e06e9e5e82a5ebb2a0ca808`; its
  pages were not read in this stage (handoff lead 5 is for research; research
  read them, propers/verified.md).
- **Latin, the Preface.** Both candidates are ancient texts printed in the
  pre-1931 typical editions; research names the witness for whichever the
  study prints.
- **English, the orations.** The Lasance *New Roman Missal*, Benziger revision
  of 1945 (`edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945`;
  rights holding in `src/sources/inventories/lasance-new-roman-missal-rights-v1.toml`,
  public domain in the United States by nonrenewal). The feast's four orations
  stand at pp. 1265 and 1268 (artifact `…resume-orations-core193-2026-10-23-0736f65f`)
  and the Sunday's three at pp. 733 and 735-736 (`…resume-orations-phase2-2026-10-23-5a4e83f7`);
  `src/sources/inventories/roman-1962-proper-translations-v1.toml` has four
  `omnium-sanctorum` and three `pentecost-23` rows. It is the 1945 book's own
  English under its attribution, not an approved liturgical translation, and
  its surrounding rubrics are pre-1960.
- **English, the scriptural elements.** The Lasance English of pp. 1265-1268
  (`…all-saints-scriptural-propers-en-checked-ff92e98e`; its Offertory reads
  *torment of malice … Alleluia*) and the Douay-Rheims (Challoner) as
  registered (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  with `…american-1899-ebible` as the other registered Douay printing). The
  Douay does not carry the Missal's forms at the Lesson's and Gospel's
  liturgical openings, the Gradual and the Offertory (above). English must
  never be composed to fill those differences; where the Douay cannot carry
  the form, use the Lasance English under its own attribution or give the
  Latin with a description.

No source was registered or retained in this stage. The existing library was
read first; everything fetched was a registered artifact matched to its
registered hash or a live response whose identity and hash are written above.
The formulary is printed in this family's own Missal and is local to this
leaf; the commemoration's orations are cited from their own 1962 owner. No
liturgical owner is imported, so no shared-formulary Makefile dependency is
declared.

## Shared records: observations for their owners

This stage owns no source, calendar, ledger or tool record, so these are
reported rather than repaired.

- `src/sources/calendars/roman-1962/propers.yaml`, mass `omnium-sanctorum`:
  the Gospel is encoded as Mt 5:1-12 where the Missal ends at 12a, and the
  Offertory as Wis 3:1-3 entire where it omits 3:2b-3a; no Preface case is
  represented. `tools/tpt proper-chronology loci` therefore yields `Matt.5.1-12`
  and `Wis.3.1-3`. The other loci it yields (`Ps.32.1`, `Apoc.7.2-12`,
  `Ps.33.10-11`, `Matt.11.28`, `Matt.5.8-10`) agree with the page.
- `tools/tests/test_ordinary_appointments.py` (`allSaintsSunday1962`) asserts
  the common Preface, which the rubrics read here do not settle.
- The Latin provenance ledger lacks rows for the six scriptural elements
  (above). `commentary-work-index formulary` lists no liturgical commentator
  for `omnium-sanctorum` or `pentecost-23` (negative result).
- `src/sources/inventories/source-containment-v1.toml`, Victorinus
  constituent (about line 3621), bounds his extent at Rev 1, 5 and 19; the
  handoff reports that this produced a false negative for Apoc 7 (lead 1).
- `work.fsspx.ordo` declares English; the responses read here are French.
- The handoff further reports, unverified here, that `author-standing-v1.toml`
  lacks several authors and that Bede's *Explanatio Apocalypsis* has no passage
  records for Apoc 7:2-3.

## Remaining verification for research

- Collate every element word for word against the 1962 page images at 200 and
  400 dpi, with conclusions and orthography; write `propers/retrieved.txt` and
  `propers/verified.md`.
- Collate the six scriptural elements against Mame 1922 and record the
  publication basis; read the Pustet 1862 extract for the commemoration and
  bind it, or report no Pustet reading (lead 5).
- **The Offertory's history (lead 2).** The 1570 Venice text layer
  (`artifact.catholic-church.missale-romanum.venice-1570.missale-romanum-1570-text-563f4dd2`,
  SHA-256 `563f4dd2…aec` recomputed and matched), lines 71698-71701, reads
  *tormentum mortis* and has no *alleluia*; this was read on the OCR only.
  Confirm on a page image, and find witnessed evidence for when *malitiae* and
  the *alleluia* entered, or record the history as unresolved. The same text
  shows the 1570 Gospel ending at *in celis*.
- The Gradual's non-Clementine psalter form (above): identify its source on
  evidence, or say it is unidentified.
- The Preface: search for a registered authority that settles the
  feast-on-Sunday case; otherwise name both candidates (lead 11).
- Re-read any dated witness relied on, and register a dated passage for 1
  November 2026 if the study cites it (lead 10). Record the ICRSP last-Gospel
  line as that institute's practice.
- State the numbering basis of every psalm citation, including NPNF's Hebrew
  numbering of Augustine and Bellarmine's English (lead 4); Vulgate 33:12 is
  not said in the Gradual.
- Read each appointed passage in its literary context: Apoc 7 whole with
  Apoc 4-5 and 14:1-5; Mt 5:1-16 with the Sermon on the Mount's setting;
  Mt 11:25-30; Ps 32 and Ps 33 whole; Wis 2:21-3:9; and, for the commemoration,
  the Sunday's own Mass only as the source of its orations.
- Reception: Victorinus on Apoc 7 and 12, read in the text, not the
  containment bound (leads 1, STU-001); Bede on 7:9, in his order (lead 7);
  a second eligible witness on Apoc 7 (Caesarius of Arles named); the PL 35
  *Expositio in Apocalypsim* from col. 2425, registered from its tracked parent
  if used (lead 14); Bernard's All Saints sermons from a lawful text (leads
  15, STU-011); Augustine, Chrysostom, Hilary and Aquinas on the beatitudes at
  exact loci (STU-003, STU-012); Aquinas, *Super Psalmos* 33, and Bellarmine on
  Ps 33:10-11 (STU-004); Augustine on Ps 32 and Ps 33 with the handoff's
  caution about verses the Mass does not say (lead 12); Fromage on the
  Communion (French text).
- Chronology: generate rows from the narrowed loci; name and inspect the
  chronology sources the rows cite (lead 8).
- Bind the controlling sources in `research/source-bindings.toml` and declare
  the external owners in `research/review-dependencies.toml`, including the
  Lasance derivative artifacts (lead 9). The authorities adopted here are the
  1962 facsimile artifact and its passage records, the facsimile-rights
  inventory, the Latin provenance and translations ledgers, Mame 1922 and its
  derivatives, the Pustet 1862 extract, the 1570 text artifact (as a lead), the
  Lasance edition, artifacts and rights inventory, the Clementine and
  Douay-Rheims editions and the psalm concordance, and, as computation inputs,
  `src/sources/calendars/roman-1962/propers.yaml` and `rubrics.yaml`.
- Keep `carrying_authors` in `proper-components.toml` in agreement with
  `research/interpretations.md` (lead 13), and keep machine paths and scratch
  locations out of tracked records (lead 16).
