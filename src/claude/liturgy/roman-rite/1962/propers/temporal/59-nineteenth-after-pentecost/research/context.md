# Celebration context and complete appointed inventory

Resolved 30 September 2026 for the `proper-study` v7 production of the Claude
1962 leaf, run `a27462e34ec9c09a`, seeded at commit
`56d8c30f24bd0e42234c88c7d71c801981a9f2f9`. The production-plan entry of
2026-09-30 in `guidance/liturgy/propers-production-plan.md` authorizes provider
`claude` for this one identity and Sunday 4 October 2026, as an independent
production. `ARGS.research_handoff` is `none`, so no handoff was supplied. The
other provider's leaf for this same identity, every postconciliar record, and
this provider's neighbouring Sundays are outside this record's evidence; none
was opened and nothing below is taken from them. Two provider-neutral records
in the source library were registered on 2026-09-28 in the course of that other
production (the 1862 page extraction and the checked 1861 English named under
*Lawful study-text routes*); they are used here only as library evidence, and
the pages behind them were read afresh in this stage rather than taken on their
recorded verification. This record settles what is studied. It holds no study
prose, spoken text, timing claim or review verdict; the research stage collates
the sources and may correct it from evidence.

## Identity, governing books and territory

- Canonical identity:
  `liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost`,
  catalog ID `59` in the 1962 temporal registry of
  `guidance/liturgy/roman-1962-propers.md` (IDs 41-63 run from the Second
  Sunday after Pentecost, with the Sacred Heart at 42, to the Twenty-third
  Sunday). Calendar family `roman-1962`. `tools/check-proper-identity
  --document … --calendar roman-1962` passes. The finding-aid mass index
  `src/sources/calendars/roman-1962/propers.yaml` carries the formulary as
  `pentecost-19`, `registry: '59'`; that index is a lead and never the source
  of record for any wording.
- Governing edition: *Missale Romanum*, editio typica, Typis Polyglottis
  Vaticanis 1962 (`edition.catholic-church.missale-romanum.vatican-typica-1962`),
  controlled on the page images of
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.
  A copy fetched in this stage from the registered `source_url` matched the
  registered SHA-256
  `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` and
  82,815,941 bytes before any page was read. Every locus below was read on
  page images rendered from that file (the formulary at 200 and 400 dpi; the
  rubrics and calendar at 200 dpi, with 400-dpi checks of RGMR 356-360), not
  on its text layer, which served only to locate pages.
- Printed heading and rank: *DOMINICA DECIMA NONA post Pentecosten*,
  *II classis*, Proper of Time, printed p. 411 left column (artifact PDF
  p. 492). The running head of p. 411 reads *Dominica XIX post Pentecosten*,
  although its left column still carries the end of the Eighteenth Sunday; the
  running head of p. 412, which carries most of this formulary, reads
  *Dominica XX post Pentecosten*, because the Twentieth Sunday begins in its
  right column. The running heads do not bound the formulary.
- Formulary boundary: it begins at marginal no. 1679 on p. 411, immediately
  after the Postcommunion *Gratias tibi referimus* (no. 1678) of the Eighteenth
  Sunday, and ends with its own Postcommunion, no. 1688, in the right column
  of p. 412 (artifact PDF p. 493), after which the heading *DOMINICA VIGESIMA
  post Pentecosten*, II classis, opens a different formulary at no. 1689.
  Marginal nos. 1679-1688. Every marginal number of the formulary, including
  those of the right-hand columns, is printed whole and legible on these two
  pages.
- Governing books within that edition, read where cited below: the
  *Calendarium*; the *Rubricae generales* (part I of the 1960 code as printed);
  the *Rubricae generales Missalis romani* (part III, cited RGMR); the *Ordo
  Missae*; the *Praefationes*; the appendix *Ordo ad faciendam et aspergendam
  aquam benedictam*. Part II, the *Rubricae generales Breviarii romani*
  (nn. 138-268), is printed only as a heading marked *Hic omittuntur.* on
  printed p. XX (PDF 18) and is not available in this witness.
- Territory: the universal 1962 General Roman Calendar. No diocese, church
  titular or dedication, religious institute or other particular calendar was
  supplied, so no local overlay is applied or computed. The study concerns the
  universal formulary on this date, not a direction to any particular church.
- Language: Latin governs. Every English route below is a historical study
  aid, not an approved vernacular liturgical text.
- Cycle: the 1962 Missal appoints the readings with the formulary and has no
  Lectionary cycle. No A/B/C or I/II value exists for this record. The
  requested identity and the formulary appointed on the requested date are the
  same, so there is no requested-versus-appointed cycle difference to preserve.
- Season: *tempus « per annum »*, which RG 77 (printed p. XVI, PDF 14, read)
  runs from I Vespers of Trinity Sunday to None of the Saturday before the
  First Sunday of Advent.
- Homily audience for the later homily stage: adult parish assembly
  (`ARGS.audience`). RGMR 474 (printed p. XXXIII, PDF 31, read) places a brief
  homily after the Gospel, *praesertim in dominicis*; the homily is authored
  preaching and adds no text to this inventory.

## Occurrence on 4 October 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
roman-1962 --date 2026-10-04 --json` returns candidate `pentecost-19`, "slot 19
of 26 Sundays after Pentecost", season after Pentecost, no Lectionary value and
nothing unresolved; its only other candidate is the fixed-date sanctoral entry
*S. Francisci Confessoris*, III class. The anchors are those tabulated in
`guidance/liturgy/calendar-computation.md` for 2026: Easter 5 April, Pentecost
24 May, Trinity Sunday 31 May (the first Sunday after Pentecost), First Sunday
of Advent 29 November; liturgical year 30 November 2025 - 28 November 2026.
Thirty-one May plus eighteen weeks is 4 October, the nineteenth Sunday of the
run. With `P = 26` for 2026 the resumed Sundays after the Epiphany occupy
slots 24 and 25 (RG 18 b, printed p. XII, PDF 10, read: with twenty-six
Sundays the twenty-fourth is the Fifth after the Epiphany and the twenty-fifth
the Sixth), and the resumption mechanism does not reach slot 19. As an
independent check, the *Calendarium* gives 4 October the dominical letter *d*,
and 2026, beginning on a Thursday, has *D* as its dominical letter. Under RG
19, printed pp. XII-XIII (PDF 10-11, read), the first Sunday of a month is the
one falling on its first to seventh day, so 4 October 2026 is the first Sunday
of October.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
roman-1962 --date 2026-10-04 --json` is settled: winner `pentecost-19`, a
second-class Sunday (RG 12; RG 91 row 15); St Francis is returned `omitted`
under RG 111 and RGMR 434 b; the low-Mass and sung non-conventual oration lists
each hold the one oration of the Mass. Every locus the computation cites was
read on the page images in this stage:

- RG 10 and 12, printed p. XII (PDF 10): Sundays are of I or II class, and
  every Sunday not named in RG 11 is of II class; this Sunday is not named
  there. RG 16 (same page): a II-class Sunday is preferred in occurrence to
  II-class feasts, save a feast of the Lord, and none falls on this date.
- *Calendarium*, printed p. LI (PDF 53): 4 October, *S. Francisci Conf., III
  classis.* The same page gives 7 October, *B. Mariae Virg. a Rosario, II
  classis*, which matters for the branch below. St Francis's own formulary
  stands at printed p. 675, no. 3769 onward (PDF 756).
- RG 91, table of precedence, printed pp. XVI-XVII (PDF 14-15): row 15
  *Dominicae II classis*; row 24 *Festa III classis, in calendario Ecclesiae
  universae inscripta*. Row 12, first-class *propria* (principal patron,
  dedication, titular and the like), outranks a II-class Sunday only in a
  particular church, which is an overlay not applied here.
- RG 95, printed p. XVII: a feast accidentally impeded is commemorated or
  omitted according to the rubrics.
- RG 111 b, printed p. XVIII (PDF 16): on a II-class Sunday only one
  commemoration is admitted, and that of a II-class feast. RGMR 434 b, printed
  p. XXXI (PDF 29): on a II-class Sunday no other oration is admitted beyond
  that commemoration. RG 111 a and RGMR 434 a (same pages) admit in a sung
  non-conventual Mass only a privileged commemoration, and none is due.
- RGMR 461, printed p. XXXIII (PDF 31): the *oratio votiva ad libitum* is
  permitted only on IV-class days, so none is added.

A third-class feast is therefore admitted neither as a commemoration nor as an
added oration on this Sunday: it is omitted outright, and the Mass has exactly
one Collect, one Secret and one Postcommunion (RGMR 433, 434 b, 480, 505). No
universal feast, vigil, octave, Ember day or seasonal substitution falls on the
date. Green vestments follow RG 127 b, printed p. XX (PDF 18): *a feria II post
dominicam I post Pentecosten, usque ad sabbatum ante Adventum*; the Sunday is
none of the excepted Ember ferias or vigils.

**A lawful alternative branch on this Sunday: the external solemnity of the
Most Holy Rosary.** 4 October 2026 is the first Sunday of October. RGMR 358 b,
printed p. XXVI (PDF 24), read at 200 and 400 dpi, gives the external
solemnity *ipso iure* to *festo B. Mariae Virg. a Rosario, in dominica I mensis
octobris*. RGMR 360 (same page) permits, of a feast so kept, one sung and one
low Mass, or two low Masses, *tamquam votivae II classis*; RGMR 341-343,
printed p. XXV (PDF 23), permit votive Masses of II class on II-class
liturgical days and give them the Gloria, the Credo *ratione dominicae*, and a
single commemoration. RG 109 a (p. XVIII) makes the commemoration of a Sunday
privileged, and RGMR 475 a (p. XXXIII) says the Credo on every Sunday even when
a votive Mass of II class is celebrated. The branch therefore changes the Mass
said in up to two Masses of a church that keeps it: those Masses take the
Rosary formulary of 7 October, printed pp. 677-679, nos. 3786-3800 (PDF
758-760; nos. 3789, 3798 and 3801 are that date's commemoration of St Mark,
which does not travel to this Sunday), with its own Preface *de B. Maria
Virg.* (printed direction on p. 679; RGMR 483, 495, p. XXXIV), and the
Sunday's Collect, Secret and Postcommunion are added as its commemoration under
a separate conclusion (RGMR 437 a, p. XXXI). The Rosary formulary prints its
festal Introit *Gaudeamus* and, under *In Missis votivis*, an alternative
Introit *Salve, sancta parens*; which of the two an external solemnity takes is
not settled here, and neither is imported. The branch is optional, bounded in
number of Masses, and does not alter the Sunday's formulary; the study remains
the study of the Sunday formulary, whose three orations are still said, as the
commemoration, in a Mass that takes the branch. RGMR 358
i (a feast of the universal calendar kept with a particular concourse of the
people, at the Ordinary's judgement) could in principle give St Francis an
external solemnity in some place; that is a local decision, not computed.

**Dated official witnesses.** Two dated Ordos of institutes that celebrate with
the 1962 books were read live for this date. Neither response was a re-read of
registered bytes; both are held only in this run's scratch area, are not
retained or registered, and change no registration. Their SHA-256 values are
recorded so the research stage can register a dated edition and passage if it
relies on them.

- FSSP France, *Ordo du mois*, <https://www.fssp.fr/ordo-du-mois/>, read
  2026-09-30, response 169,632 bytes, SHA-256
  `853c88698a59a2b4157825cdd8c4599a6c602cfa9d34716149f55eafbbf0b5f2`:
  *Dimanche 4 octobre* — 19th Sunday after Pentecost, with an optional
  solemnity of Our Lady of the Rosary, second class. The line prints a single
  colour, *Blanc*, for the Sunday and the optional solemnity together. White is
  the colour of the Rosary solemnity; the Sunday's own colour under RG 127 b is
  green, and the ICRSP entry below gives green for the Sunday. The single
  colour is recorded as a compression in that witness, not adopted. St Francis
  does not appear on that date at all, which agrees with his omission.
- ICRSP France, *Ordo*, <https://icrspfrance.fr/ordo.php?d=2026-10-01> (the
  site's own October navigation link; the bare page on 2026-09-30 carried only
  September), read 2026-09-30, response 115,751 bytes, SHA-256
  `675b65c8aa47becc7bce158f9399cf9ca582b7701617c1d28aed49c6e5abae02`:
  *dimanche 4 octobre 2026* — *Temps Per Annum*, second class, green; Gloria,
  Credo, *Or. pro Papa*, Trinity Preface; *Messe propre (Salus populi)*. Its
  notes carry the *Solennité de N.-D. du S. Rosaire* (second class, white),
  Mass *comme à la fête*, with commemoration and last Gospel of the Nineteenth
  Sunday.

Computation and both dated witnesses agree on the identity and the second
class; the ICRSP entry also gives the season and names the Sunday's Mass by its
Introit, and both witnesses independently carry the Rosary external solemnity
as an option for this Sunday. Nothing fails closed.
Three things in those witnesses are theirs and are not imported. The ICRSP
*Oratio pro Papa* is an institute observance whose basis was not examined;
RGMR 434 b admits no added oration on a II-class Sunday in the universal
books. The ICRSP note of a Sunday last Gospel in the Rosary Mass differs from
RGMR 509, printed p. XXXV (PDF 33, read), under which the last Gospel *in
quavis Missa* is the initium of John, save the Palm Sunday exception; its basis
was not examined. The FSSP single colour is noted above. The source library
already holds FSSP France deliveries of 2026-09-22 and 2026-09-28 and ICRSP
deliveries of 2026-09-17 and 2026-09-22; none carries a passage record for 4
October, and the FSSP record of 2026-09-22 itself measures that this site's
delivery is not byte-stable, so no registered hash can be re-obtained.

*Research-stage note, 30 September 2026.* The research stage does not adopt
either Ordo as evidence for any claim. The occurrence rests on the typical
edition's printed calendar and rubrics and on the computation above; the Rosary
branch rests on RGMR 358 b and 360. Both Ordos remain unregistered corroborating
leads, which no study of this leaf cites; a later stage that wants to print a
dated institute Ordo must first register a dated edition, artifact and passage
for 4 October 2026 (`research/scope.md` § 8).

## Appointed proper

Every element is required and none has an alternative within the formulary:
the page prints no option, no choice and no substitute. Loci are the printed
page and marginal number of the controlling edition, read on 200- and 400-dpi
page images of artifact PDF pp. 492-493. Psalms are cited in the Missal's
Vulgate numbering, with the Hebrew number of the repository's psalm concordance
(`.../challoner-gutenberg-1581/artifacts/psalm-numbering-ee3c7757/`, SHA-256
recomputed and matched) in parentheses; for all five psalms here the English
verse offset is zero.

| Order and key | Element and printed locus | Liturgical place, extent and boundary |
|---|---|---|
| 1 `introit` | *Antiphona ad Introitum* *Salus populi ego sum*; verse cited Ps 77:1 (78:1); p. 411 left column running into the right, no. 1679 | Entrance chant (RGMR 427, p. XXXI): antiphon, psalm verse *Attendite, popule meus, legem meam*, printed cue *V. Gloria Patri*, and repetition. The antiphon itself carries no printed scriptural citation: the Missal prints *Ps. 77, 1* only before the verse. No Alleluia is added outside paschal time (RGMR 429). |
| 2 `collect` | *Oratio* *Omnipotens et misericors Deus, universa nobis adversantia*; p. 411, no. 1680 | The one oration of the Mass (RGMR 433, 434 b). Printed conclusion *Per Dominum.*; the full form is RG 115 a's (printed p. XIX, PDF 17, read). |
| 3 `epistle` | Eph 4:23-28; p. 411, no. 1681 | *Lectio Epistolae beati Pauli Apostoli ad Ephesios*. Opens *Fratres: Renovamini spiritu mentis vestrae*; ends at v. 28, *ut habeat unde tribuat necessitatem patienti*. No shorter form. |
| 4 `gradual` | Ps 140:2 (141:2); p. 411, no. 1682 | After the Epistle (RGMR 469, p. XXXIII): respond *Dirigatur oratio mea sicut incensum in conspectu tuo, Domine*, verse *Elevatio manuum mearum sacrificium vespertinum*. Both halves are v. 2. |
| 5 `alleluia` | Ps 104:1 (105:1); p. 411, no. 1683 | *Alleluia, alleluia* with verse *Confitemini Domino, et invocate nomen eius: annuntiate inter gentes opera eius*, then *Alleluia*. No Tract and no Sequence. |
| 6 `gospel` | Mt 22:1-14; p. 411 right column to p. 412 left column, no. 1684 | *Sequentia sancti Evangelii secundum Matthaeum*. Opens *In illo tempore: Loquebatur Iesus principibus sacerdotum et pharisaeis in parabolis, dicens*; ends at v. 14, *Multi enim sunt vocati, pauci vero electi*. Printed cue *Credo.* follows. |
| 7 `offertory` | *Ant. ad Offertorium* Ps 137:7 (138:7); p. 412, no. 1685 | *Si ambulavero in medio tribulationis, vivificabis me, Domine*, through *et salvum me faciet dextera tua*. |
| 8 `secret` | *Secreta* *Haec munera, quaesumus, Domine, quae oculis tuae maiestatis offerimus*; p. 412, no. 1686 | Over the offerings, said secretly and as many as the opening orations (RGMR 480-481, p. XXXIV), hence one. Printed conclusion *Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.*, longer than the cue on the Collect and Postcommunion and still short of RG 115 a's full form; the printed length is a setting variable. Followed by the printed direction *Praefatio de Ssma Trinitate.* |
| 9 `communion` | *Ant. ad Communionem* Ps 118:4-5 (119:4-5); p. 412, no. 1687 | After the Communion rites (RGMR 504, p. XXXV): *Tu mandasti mandata tua custodiri nimis: utinam dirigantur viae meae, ad custodiendas iustificationes tuas.* |
| 10 `postcommunion` | *Postcommunio* *Tua nos, Domine, medicinalis operatio*; p. 412, no. 1688 | As many as the opening orations (RGMR 505, p. XXXV), hence one. Printed conclusion *Per Dominum.* |

This edition sets the chant rubrics both in full and abbreviated in the same
formulary: *Antiphona ad Introitum* at no. 1679 and *Ant. ad Offertorium*, *Ant.
ad Communionem* at nos. 1685 and 1687. The abbreviation is a setting variable,
not a different rubric. At the Offertory the citation *Ps. 137, 7* stands on
the rubric line and the marginal number on the first line of text.

The Vulgate comparisons below were made word by word against the tracked
Clementine Vulgate (`edition.catholic-church.vulgata-clementina.ebible-latvuc`,
its verse-text artifacts) after normalising i/j, ligatures, accents and
pointing, and cross-checked through `tools/tpt mass-propers show --calendar
roman-1962 --mass pentecost-19 --bible clementine-vulgate`. They are textual
observations about wording and boundary. Whether a chant follows an older
Latin psalter or another Latin text, and which, is left to research, and no
origin is asserted here.

- **Introit.** The antiphon *Salus populi ego sum, dicit Dominus …* is not a
  continuous Vulgate text and the Missal cites none for it. The Latin
  provenance ledger's row for this Introit describes the antiphon in a note as
  a psalm "centonisation" without a locus; that description is not adopted
  here. The verse omits the Clementine's title *Intellectus Asaph*, which the
  Clementine counts inside Ps 77:1.
- **Epistle.** The Missal prefixes the liturgical address *Fratres:* and omits
  the Clementine's connective *autem* (*Renovamini autem spiritu*). The rest of
  vv. 23-28 agrees word for word.
- **Gradual.** The Missal adds *Domine* after *in conspectu tuo*, which the
  Clementine at Ps 140:2 lacks.
- **Alleluia.** The Missal's verse omits the Clementine's opening *Alleluja*,
  which the Clementine counts inside Ps 104:1 as the psalm's title; otherwise
  the words agree.
- **Gospel.** The liturgical opening *In illo tempore: Loquebatur Iesus
  principibus sacerdotum et pharisaeis in parabolis, dicens* stands for the
  Clementine's *Et respondens Jesus, dixit iterum in parabolis eis, dicens*
  (v. 1). The addressees it names are those of Mt 21:45 (*principes sacerdotum
  et pharisaei*), the verse closing the preceding parable. At v. 13 the Missal
  reads *Tunc dixit rex ministris* where the Clementine reads *Tunc dicit rex
  ministris*. Every other word of vv. 1-14 agrees.
- **Offertory.** The Missal adds *Domine* after *vivificabis me* and reads the
  future *extendes* and *faciet* where the Clementine at Ps 137:7 reads the
  perfect *extendisti* and *fecit*.
- **Communion.** Agrees with the Clementine at Ps 118:4-5 word for word.

The formulary prints no Tract, Sequence, prophecy, proper *Communicantes* or
*Hanc igitur* (RGMR 501, p. XXXIV: such variations are noted in the proper
Mass, and none is noted here), *Oratio super populum* (RGMR 506, p. XXXV:
Lenten and Passiontide ferias), second or third oration, blessing, or
alternative reading. The 1862 antecedent's *Secunda Oratio A cunctis*, *Alia
Secreta Exaudi nos Deus*, *Alia Postcommunio Mundet et muniat* and *Tertia ad
libitum*, printed on the same pages, belong to the pre-1960 rubrics and are not
part of the 1962 formulary.

## Other text-bearing parts of this Mass

These are fixed or rubrically appointed texts of the 1962 *Ordo Missae*,
*Praefationes* and appendix, not proper text. The study refers to them and does
not reproduce the Ordinary. Every rubric number below was read on the page
images in this stage. The *Ordo Missae* marginal numbers were first taken from
the registered passage records `…vatican-typica-1962.ordo-missae-ad-gradum`,
`…ordo-missae-kyrie-gloria`, `…ordo-missae-credo` and `…ordo-missae-conclusio`;
*research-stage note, iteration 1, 30 September 2026:* each number and the
Trinity Preface locus were then re-read on page images of the same bound
facsimile bytes (digest re-matched), at artifact PDF pp. 297-301 (printed pp.
216-220), 374 (p. 293) and 404-408 (pp. 323-327), and those passage records and
`…vatican-typica-1962.praefationes` are bound in
`research/source-bindings.toml`. The re-reading corrected one row: no. 1024 is
the Kyrie and no. 1025 the *Gloria in excelsis* (printed pp. 217-219), not the
Introit doxology and Kyrie together.

| Place | Text and appointment | Status and source |
|---|---|---|
| Before the principal Mass, where used | Blessing of water *Die dominico* and *Aspersio aquae benedictae* extra tempus paschale: antiphon *Asperges me* with Ps 50:3, versicles, oration *Exaudi nos*; appendix, printed pp. [231]-[232], nos. 5919-5926 (PDF 1039-1040), read | A Sunday rite outside the Mass and outside this formulary. Whether and where it precedes a given Mass is not settled here; it is not part of the appointed inventory. |
| Prayers at the foot of the altar | Ps 42 *Iudica me* with its antiphon, Confiteor, through *Oramus te*; *Ordo Missae* nos. 1013-1023, printed pp. 216-217 (PDF 297-298), page images | Said: RGMR 425 (p. XXXI) omits *Iudica* only from Passion Sunday to Maundy Thursday and in Requiem Masses. |
| Introit doxology; Kyrie | *Gloria Patri* in the Introit; ninefold Kyrie, *Ordo Missae* no. 1024, printed p. 217 (PDF 298), page image | RGMR 427-428, 430 (p. XXXI); the Introit's printed *V. Gloria Patri* cue at no. 1679. |
| After the Kyrie | *Gloria in excelsis*, *Ordo Missae* no. 1025, printed pp. 217-219 (PDF 298-300), page images | Said. RGMR 431 a (p. XXXI) ties it to the Office's Te Deum at Matins, a Breviary rubric this Missal omits. The ICRSP dated entry also carries the Gloria for this date; it is an unadopted lead (see the research-stage note under *Dated official witnesses*). No chant setting is chosen. |
| Before the Gospel; after it | *Munda cor meum*, Gospel dialogue; homily | RGMR 471, 474 (p. XXXIII); *Ordo Missae* nos. 1026-1028, printed p. 219 (PDF 300), page image. |
| After the Gospel or homily | *Credo* | Said: RGMR 475 a, *in qualibet dominica* (p. XXXIII); printed cue after no. 1684; text *Ordo Missae* no. 1029, printed p. 220 (PDF 301), page image. |
| After the Secret | *Praefatio de Ss.ma Trinitate* | Appointed, not chosen: printed direction after no. 1686 and RGMR 494 b, *tamquam de Tempore … in omnibus dominicis II classis, extra tempus natalicium et paschale* (p. XXXIV, PDF 32). Complete unnotated text, with the same rubric, at printed p. 293, no. 1082 (PDF 374), read on the page image. |
| Canon | *Te igitur* through the doxology | The one Roman Canon, said secretly (RGMR 500, p. XXXIV). There is no alternative Eucharistic Prayer and no proper insertion for this day (RGMR 501). |
| Conclusion | *Ite, missa est*, *Placeat*, blessing, last Gospel Jn 1:1-14 | RGMR 507-509 (p. XXXV): *Ite, missa est*, since no procession is supplied (507 a); the last Gospel is the initium of John, and none of the omission cases of 510 applies. *Ordo Missae* nos. 1132 (*Ite*, printed p. 323, PDF 404), 1137 (*Placeat*, pp. 325-326, PDF 406-407), 1138 (blessing, p. 326) and 1139 (last Gospel, p. 327, PDF 408), page images. |

## Lawful study-text routes

- **Latin, all ten proper elements.** Control: the 1962 page images above.
  Publication basis: 17 U.S.C. 103(b) with a public-domain antecedent, as
  settled for the repository in
  `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`.
  The antecedent is the Pustet Ratisbon 1862 printing
  (`edition.catholic-church.missale-romanum.pustet-ratisbon-1862`), which
  prints the whole formulary at printed pp. 351-352 under *Dominica XIX. post
  Pentecosten*. Two witnesses to those pages exist in the library and both
  were read here:
  - the tracked public-domain text layer
    `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`
    (SHA-256 recomputed and matched), at physical lines 51814-51983: heading
    51814-51816, Introit 51818-51830, Collect 51832-51840, Epistle
    51846-51866, Gradual 51868-51873, Alleluia 51875-51879, page 352 from
    51885, Gospel 51891-51945, Offertory 51947-51952, Secret 51954-51960,
    Communion 51966-51970, Postcommunion 51972-51979, with the 1862's own
    pre-1960 extra orations at 51842-51844, 51962-51964 and 51981-51983; and
  - the tracked two-page extraction
    `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.pentecost-19-pages-351-352`
    (SHA-256
    `ac3f705034d2f649e07d3fff76d2ce5accf1d216fa68c8fa6ffe0b364374ed2c`
    recomputed and matched; derived from the
    registered complete scan PDF, Internet Archive leaves 436-437), whose
    page images were rendered and read here at display resolution.

  On the page images every element of this formulary agrees with the 1962 in
  its words, including each divergence from the Clementine listed above: the
  1862 already reads *Fratres.* without *autem*, *Domine* in the Gradual and
  Offertory, *extendes* and *faciet*, the liturgical Gospel opening naming the
  chief priests and Pharisees, and *Tunc dixit rex*. The differences seen are
  of orthography (*j* for *i*, *exequamur* for *exsequamur*, *majestatis* for
  *maiestatis*), capitalisation (*Principibus*, *Pharisaeis*), pointing,
  citation form (*Ps. 77.*, *c. 4.*, *cap. 22.* without verse numbers) and
  conclusion length (*Per Dominum.* on the Secret). This was a reading, not a
  word-for-word collation at full resolution. Four of the ten elements already
  carry collated `publication_status = "permitted"` rows in
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` —
  Introit, Collect, Secret and Postcommunion — each verified against
  `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-pentecost-19-orations`
  and cited to the 1862 text layer through
  `passage.catholic-church.missale-romanum.pustet-ratisbon-1862.pentecost-19-orations`.
  The Postcommunion row records one word, *inhaerere*, as inferred from the
  1604 because the 1862 text layer damages it; the 1862 page image of p. 352
  prints *inhaerere mandatis* whole. The six scriptural elements (Epistle,
  Gradual, Alleluia, Gospel, Offertory, Communion) have no ledger row and need
  one, or an equivalent recorded basis, before their Latin is published.
- **English, canonical Scripture.** The Douay-Rheims (Challoner) as registered
  (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  with `…american-1899-ebible` as the other registered Douay printing), read
  at the Vulgate loci and resolved in the Missal's Vulgate psalm numbering
  through `tools/tpt mass-propers show … --bible douay-rheims`. Its canonical
  verses are **not** the Missal's wording at the Epistle's liturgical address,
  the Gospel's opening, the Gradual's and Offertory's added *Domine*, or the
  Offertory's future tenses (the Douay gives *thou hast stretched forth … thy
  right hand hath saved me*). English must never be composed to fill those
  differences; where the Douay cannot carry the Missal's form the profile's
  rule is to say so and give the Latin with a description.
- **English, the Introit antiphon and the orations.** The 1861 Cummiskey hand
  missal (`edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861`),
  under the heading *XIX. SUNDAY after PENTECOST* at printed p. 445. Two
  library records carry it:
  - `passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.post-pentecosten-19`
    over the tracked payload `…philadelphia-1861.temporal-orations-en`
    (SHA-256 recomputed and matched), physical lines 167-169, the Collect,
    Secret and Postcommunion in liturgical order, states cataloged, acquired
    and inspected; and
  - `…philadelphia-1861.pentecost-19-checked-english`, a tracked
    transcription that its record calls model-assisted and checked against
    the page images (SHA-256 recomputed and matched), whose passages
    `…pentecost-19-introit-antiphon-checked`, `…-collect-checked`,
    `…-secret-checked` and `…-postcommunion-checked` also cover the Introit
    antiphon, with `…verify-post-pentecosten-19-introit` recording the whole
    Introit on the scan.

  The registered scan `…philadelphia-1861.ia-scan-pdf` was fetched in this
  stage, matched its registered SHA-256
  `85034c90d5cbfe891f4359fb2faff907d217dbd11a30458b55e4c48eae028898`, and its
  PDF pp. 454-457 (printed pp. 445-448) were read at display resolution: the
  Introit antiphon (pp. 445-446), Collect (p. 446), Secret (p. 447) and
  Postcommunion (pp. 447-448) stand there in the wording both payloads carry.
  The same pages print English for the whole Mass; that English is the 1861
  book's own and not the route for the scriptural elements, and two of its
  features are recorded so that no one takes it for the Missal's sense: its
  Gospel opening reads *Jesus spoke to the Scribes and Pharisees* where the
  Latin names the chief priests, and its Offertory keeps the Vulgate's past
  tenses. The finding-aid overlay
  `src/sources/inventories/roman-1962-proper-translations-v1.toml` still
  records the English of the Introit, Collect, Secret and Postcommunion as
  `unavailable` / `rights-withheld` pending an exact binding; that shared
  record belongs to its own owner and is unchanged here.
- **Trinity Preface.** Appointed by rubric and its Latin located (p. 293,
  no. 1082), within the registered
  `…vatican-typica-1962.praefationes` passage. The 1861 English exists as the
  Trinity clause of `…philadelphia-1861.praefationes-propriae` (printed
  pp. xxviii-xxix), not examined here. Any reproduction needs a public-domain
  Latin antecedent and that registered English; whether the study quotes or
  only cites the Preface is for research.

No source was registered or retained in this stage. The existing library was
read first and sufficed for resolution; everything fetched was either an
already registered artifact fetched to its registered hash or a live Ordo
response whose identity and hash are written down above. No liturgical owner is
imported: the formulary is local to this leaf, so there is no shared-formulary
Makefile dependency to declare.

One defect in the source library is reported rather than repaired, because this
stage owns no source record: the same FSSP France *Ordo du mois* is registered
under two work identities, `work.fssp-france.ordo-du-mois` (editions
2026-09-17 and 2026-09-22) and
`work.priestly-fraternity-of-saint-peter-france.ordo-du-mois` (edition
`web-2026-09-28`), both at the same `source_url`.

## Remaining verification for research

- Collate every proper element word for word at 200 and 400 dpi against the
  1962 page images and against the 1862 pages at full resolution; write
  `propers/retrieved.txt` and `propers/verified.md` with the loci,
  conclusions and orthographic transformations.
- Identify the textual source of the Introit antiphon, and of the Gradual's and
  Offertory's *Domine*, the Offertory's future tenses and the Gospel's *dixit*,
  or record the negative result. Nothing above asserts an origin for any of
  them.
- Establish or record a publication basis for the Latin of the six scriptural
  elements, which the provenance ledger does not yet carry, and decide the
  English display for the places where the Douay cannot carry the Missal's
  form.
- Choose between, or reconcile, the two registered Cummiskey routes for the
  orations and the Introit antiphon, collating the chosen payload against the
  1861 page images at full resolution; decide whether the Trinity Preface is
  quoted or only cited.
- Read each appointed passage in its complete biblical context, including Mt
  21:23-46 as the setting the Gospel's opening names, run the reception sweep,
  and generate `research/chronology.toml` and
  `research/chronology-annotations.tex` with `tools/tpt proper-chronology`. No
  biblical date is asserted in this record. `tools/tpt proper-chronology loci`
  already resolves every appointed locus under the default profile
  `catholic-comprehensive-v1`, and all seven return `composition-only`. The
  distinct directly appointed passages, in canonical then verse order, are
  Ps 77:1, Ps 104:1, Ps 118:4-5, Ps 137:7, Ps 140:2, Mt 22:1-14 and
  Eph 4:23-28; each is appointed once, Ps 140:2 supplying both halves of the
  Gradual. The Introit antiphon carries no printed citation and is not a
  directly appointed passage unless research establishes one.
- Register a dated edition and passage for 4 October 2026 if the study relies
  on either Ordo; no registered passage covers this date.
- Resolve, only if the study relies on them, the points this stage did not
  settle: the Breviary's Te Deum rubric behind the Gloria, the Asperges
  placement, the festal or votive Introit of the Rosary external solemnity,
  and any particular-calendar overlay. None is needed for the universal
  formulary on this date.
- Bind the controlling sources in `research/source-bindings.toml` and declare
  the external owners actually relied on in `research/review-dependencies.toml`.
  The authorities adopted here are the 1962 facsimile artifact and its
  `temporal-pentecost-19-orations` passage, the facsimile-rights inventory, the
  Latin provenance ledger, the 1862 Pustet text artifact, its
  `pentecost-19-orations` passage and its `pentecost-19-pages-351-352`
  extraction, the Douay-Rheims editions and the psalm-numbering concordance,
  the Clementine Vulgate edition, the Cummiskey passages and payloads named
  above with their registered scan, and, as computation inputs,
  `src/sources/calendars/roman-1962/propers.yaml` and `rubrics.yaml`.
