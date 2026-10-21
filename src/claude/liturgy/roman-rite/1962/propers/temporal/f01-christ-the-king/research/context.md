# Celebration context and complete appointed inventory

Resolved 19 October 2026 for the `proper-study` v12 production of the Claude
1962 leaf, run `7397c12187517ff2`, seeded at commit
`9b87d598b34870344f3df756982af1ff5990d993`. The production-plan entry of
2026-10-19 in `guidance/liturgy/propers-production-plan.md` authorizes provider
`claude` for this one identity and Sunday 25 October 2026, as an independent
production that is not a companion to or derivative of any other leaf. The
same entry states that it does not open the displaced Twenty-second Sunday
after Pentecost or the other provider's target for this identity.
`ARGS.research_handoff` is `none`, so no handoff was supplied. The other
provider's records, every postconciliar record and every postconciliar
calendar row are outside this record's evidence; none was opened and nothing
below is taken from them. One earlier context record of this provider was read
only as a model of the record's shape, and no finding of it is relied on. This
record settles what is studied. It holds no study prose, spoken text, timing
claim or review verdict. The research stage collates the sources and may
correct it from evidence.

## Identity, governing books and territory

- Canonical identity:
  `liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king`, catalog ID
  `F01` in `guidance/liturgy/roman-1962-propers.md`, which reserves the `F`
  series for a general-calendar feast assigned to Sunday without a temporal
  ordinal and names `F01` as Our Lord Jesus Christ the King. It is the first
  `F` leaf in the repository. Calendar family `roman-1962`.
  `tools/check-proper-identity --document … --calendar roman-1962` passes. The
  finding-aid mass index `src/sources/calendars/roman-1962/propers.yaml`
  carries the formulary as `christ-the-king`, `registry: 'F01'`, rank `I`,
  filed under the seasonal section. That entry records scripture citations
  only, notes that its orations are appointed and not transcribed, and is a
  lead, never the source of record for any wording (see *Shared records* below
  for three places where it departs from the page).
- Governing edition: *Missale Romanum*, editio typica, Typis Polyglottis
  Vaticanis 1962 (`edition.catholic-church.missale-romanum.vatican-typica-1962`),
  controlled on the page images of
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.
  The copy read in this stage matched the registered SHA-256
  `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` and
  82,815,941 bytes before any page was read. The formulary was read on page
  images rendered at 200 dpi and again at 400 dpi (both columns of both
  pages); the *Calendarium*, the general rubrics and the Preface cited below as
  "read" were read at 200 dpi. The text layer served only to locate pages, and
  loci marked "located" were found on it and not re-read on an image.
- Printed place, heading and rank. The Missal prints the feast in the
  **Sanctorale**, among the October feasts, not in the Proper of Time: printed
  p. 696 (PDF 777), headed *Festa octobris (24)*, ends St Raphael's formulary
  with its Postcommunion *Dirigere dignare* at marginal no. 3937; printed p. 697
  (PDF 778), which carries no running head, opens with a full-width engraved
  headpiece captioned *ET TRANSTULIT NOS IN REGNUM FILII DILECTIONIS SUAE*, then
  the heading *Dominica ultima octobris* / *D. N. IESU CHRISTI REGIS* / *I
  classis*; printed p. 698 (PDF 779) is headed *Festa octobris (dominica
  ultima)*; printed p. 699 (PDF 780), headed *Festa octobris (25)*, opens a
  different formulary at no. 3950, *Die 25 octobris*, *Ss. Chrysanthi et Dariae
  Mm.*, *Commemoratio*. The formulary therefore runs from marginal no. 3938 to
  no. 3949, whole and legible on two pages. The headpiece and its caption are
  decoration, not a liturgical text, and are not reproduced (the 1962
  arrangement and illustration are not freed by any record here).
- Governing books within that edition, read or located where cited below: the
  *Calendarium*; the *Rubricae generales* (part I of the 1960 code as printed,
  cited RG); the *Rubricae generales Missalis romani* (part III, cited RGMR);
  the *Ordo Missae*; the *Praefationes*; the Sanctorale. Part II, the
  *Rubricae generales Breviarii romani*, is not printed in this witness.
- Instituting act (context, not a liturgical text of the Mass): Pius XI,
  encyclical *Quas primas*, 11 December 1925, n. 28, read on 2026-10-19 in the
  English of the Holy See's website
  (<https://www.vatican.va/content/pius-xi/en/encyclicals/documents/hf_p-xi_enc_11121925_quas-primas.html>,
  response 65,042 bytes, SHA-256
  `f17b882faf9d5498fbb9f207ee20765164f9952c5cf157b5b301b7d271e4167c`), which
  institutes the feast "on the last Sunday of the month of October - the
  Sunday, that is, which immediately precedes the Feast of All Saints" and
  ordains that the yearly renewal of the dedication of mankind to the Sacred
  Heart be made on that day. Not retained or registered; the Latin text and its
  official publication were not read.
- Territory: the universal 1962 General Roman Calendar. No diocese, church
  titular or dedication, religious institute or other particular calendar was
  supplied, so no local overlay is applied or computed. The study concerns the
  universal formulary on this date.
- Language: Latin governs. Every English route below is a historical study
  aid, not an approved vernacular liturgical text.
- Cycle: the 1962 Missal appoints the readings with the formulary and has no
  Lectionary cycle. No A/B/C or I/II value exists for this record. The
  requested identity and the formulary appointed on the requested date are the
  same, so there is no requested-versus-appointed difference to preserve.
- Season: *tempus « per annum »* after Pentecost (finding-aid season
  `after-pentecost`); the feast's own colour is white (below), not the
  season's green.
- Homily audience for the later homily stage: adult parish assembly
  (`ARGS.audience`). RGMR 474 (printed p. XXXIII, PDF 31, read) places a brief
  homily after the Gospel, *praesertim in dominicis et diebus festis de
  praecepto*; the homily is authored preaching and adds no text to this
  inventory.

## Occurrence on 25 October 2026

**The rule.** RG 17 (printed p. XII, PDF 10, read): *Dominica excludit, per
se, assignationem perpetuam festorum*, with exceptions, among them *d) festum
D. N. Iesu Christi Regis, celebrandum dominica ultima mensis octobris*; and
*Haec festa locum tenent dominicae occurrentis cum omnibus iuribus et
privilegiis; de dominica, proinde, nulla fit commemoratio.* The *Calendarium*
for October (printed p. LI, PDF 53, read) gives no date to the feast and
prints at the foot of the month *Dominica ultima octobris: D. N. IESU CHRISTI
REGIS, I classis.*

**The date (computation, finding aid only).** `tools/tpt calendar-days day
--calendar roman-1962 --date 2026-10-25 --json` returns three candidates:
`christ-the-king` (I, "general rubric 17 d: the last Sunday of October"),
`pentecost-22` ("slot 22 of 26 Sundays after Pentecost") and the fixed-date
commemoration `comm-ss-chrysanthi-dariae-martyrum`, nothing unresolved. As an
independent check: 1 January 2026 is a Thursday, so the year's dominical letter
is D; the *Calendarium* gives 25 October the letter *d* and the entry
*Commemoratio Ss. Chrysanthi et Dariae Mm., Comm.* (read). 25 October 2026 is
therefore a Sunday; 1 November 2026, All Saints, is the next Sunday, so 25
October is both the last Sunday of October and the Sunday immediately before
All Saints, which satisfies RG 17 d and *Quas primas* n. 28 alike.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
roman-1962 --date 2026-10-25 --json` is settled: winner `christ-the-king`, RG
91 row 3; `pentecost-22` omitted (RG 112 b); the commemoration of Ss Chrysanthus
and Daria omitted (RG 111; RGMR 434 a); the low-Mass and sung non-conventual
oration lists each hold the feast's Collect alone. Every locus it cites, and
the further loci the result depends on, were read on the page images:

- RG 91, table of precedence, printed p. XVII (PDF 15): row 3, *Festa
  Epiphaniae et Ascensionis Domini, Ss.mae Trinitatis, Corporis Christi, Cordis
  Iesu et Christi Regis*, among the first-class days; row 15, *Dominicae II
  classis*. RG 10-12 (p. XII): every Sunday not named in RG 11 is of II class;
  the Twenty-second Sunday after Pentecost is not named there.
- RG 14 (p. XII): *Officium et Missa dominicae impeditae nec anticipantur nec
  resumuntur.* RG 16 a (same page) states the same displacement for any feast
  of the Lord of I or II class on a II-class Sunday, *de dominica, proinde,
  nulla fit commemoratio*.
- RG 112 b (printed p. XVIII, PDF 16): *Officium, Missa aut commemoratio de
  dominica excludit commemorationem aut orationem de festo vel mysterio Domini,
  et vicissim.* The formulary itself prints *Et non fit commemoratio
  dominicae.* after the Collect, after the Secret and after the Postcommunion.
- RG 107-109 (p. XVIII): Ss Chrysanthus and Daria are an ordinary
  commemoration (RG 109 names the privileged kinds, and a commemoration
  inscribed in the calendar is none of them). RG 111 a (same page): *in diebus
  liturgicis I classis et in Missis in cantu non conventualibus, nulla
  admittitur commemoratio, praeter unam privilegiatam*; RGMR 434 a (printed p.
  XXXI, PDF 29, read) states the same for the Mass. RG 94 (p. XVII): a
  commemoration fixed to its day is not transferred, *sed fit suo die vel
  omittitur*. The commemoration is therefore omitted in every Mass, sung or
  low, and is not kept elsewhere.

The result is a single branch: in every Mass of the day, sung or low,
conventual or not, the feast's own formulary with its one Collect, one Secret
and one Postcommunion. There is no low-versus-sung difference in the orations.

**Orations that are excluded on this date.** Each was read on the page images
(RGMR, printed p. XXXII, PDF 30, unless stated):

- RGMR 453, the oration *pro Fidei propagatione*, belongs to the *penultimate*
  Sunday of October (in 2026, 18 October) and in any case excepts the days of
  rows 1, 2, 3 and 8; it is not said.
- RGMR 449 (coronation of the Pope, anniversaries of the Pope and of the
  diocesan bishop) and RGMR 451 (*pro seipso sacerdote*) each except rows 1, 2,
  3 and 8; neither is said, whatever local anniversary falls on the day. The
  appendix of *Orationes diversae* repeats the exclusion of Christ the King for
  the priest's own oration (printed p. [106], PDF 914, located).
- RGMR 457 d forbids the *oratio imperata* on all I- and II-class days.
- RGMR 461 (printed p. XXXIII, PDF 31, read) admits the *oratio votiva ad
  libitum* only on IV-class days.

**No substitute Mass on this date.** RGMR 328 (printed p. XXIV, PDF 22,
located) excludes first-class votive Masses on the days of rows 1-8, saving
only RGMR 332, the Dedication Mass that is part of the rite of consecrating a
church; RGMR 341 (p. XXV, PDF 23, located) permits second-class votive Masses
only on days of II, III and IV class; RGMR 361 (p. XXVI, PDF 24, located)
prohibits indulted external solemnities on I-class days. The votive Mass *de
Christo Rege* (RGMR 308 a 5, PDF 21, located) is a votive use of this same
formulary on other days and is not the object of study. A church consecration
on this Sunday is a local fact, not computed. Masses of the dead are not
considered.

**Colour, Gloria, Credo and Preface** (read unless stated). White: RG 120 a
(printed p. XIX, PDF 17), *Domini, exceptis festis de mysteriis et
instrumentis Passionis*. Gloria: RGMR 431 a-b (p. XXXI, PDF 29), the feast's
festive Mass. Credo: RGMR 475 a and b (p. XXXIII, PDF 31), *in qualibet
dominica, etsi eius Officium alicui festo locum cedat*, and *in festis I
classis*; printed cue *Credo.* after the Gospel. Preface: the printed
direction *Praefatio propria.* after the Secret, and RGMR 492 (p. XXXIV, PDF
32): *Praefatio de D. N. Iesu Christo Rege dicitur in Missis festivis et
votivis de D. N. Iesu Christo Rege*; RGMR 482-483 (same page) make the proper
Preface the Mass's own. Last Gospel: RGMR 509 (p. XXXV, PDF 33, located), the
initium of John *in quavis Missa*; none of the omission cases of RGMR 510
applies.

**Dated official witnesses.** Two dated Ordos of institutes that celebrate
with the 1962 books were read live for this date on 2026-10-19. Neither
response is retained or registered; both are held only in this run's scratch
area, and their SHA-256 values are recorded so that the research stage can
register a dated edition and passage if it relies on them.

- FSSP France, *Ordo du mois*, <https://www.fssp.fr/ordo-du-mois/>, response
  169,685 bytes, SHA-256
  `f6dfd214b4ce7c7b7882a70ea83c27c900c50892c97548e35c2207f1cfeb85a6`:
  *Dimanche 25 octobre* — *Fête du Christ-Roi (1ère classe, Blanc)*. One line
  per day; its silence on commemorations is not read as evidence.
- ICRSP France, *Ordo*, <https://icrspfrance.fr/ordo.php?d=2026-10-01>,
  response 119,887 bytes, SHA-256
  `47db2ef8c5505be91315e75e65fbade457b51b407b968a2123382b1f1acc18d9`:
  *dimanche 25 octobre 2026* — *Notre-Seigneur Jésus-Christ Roi*, *Temps Per
  Annum*, first class, white; Gloria, Credo, no *Oratio pro Papa*, *Préface du
  Christ Roi*; *Messe propre (Dignus est)*; *Rien du XXIIe Dim.*; office
  *propre, sans mém.*; notes: the act of consecration of mankind to the Sacred
  Heart preceded by the Litany of the Sacred Heart (Pius XI), and a plenary
  indulgence in the Institute's chapels.

Computation, the printed calendar and rubrics, and both dated witnesses agree
on the identity, the first class, the white colour and the displacement of the
Sunday; the ICRSP entry also agrees on the Introit, the Gloria, the Credo, the
proper Preface and the absence of any added oration or commemoration. Nothing
fails closed. Four things in the ICRSP entry are its own and are not imported:
the feast as the Institute's titular feast (a particular calendar); the
indulgence; its note that the Twenty-second Sunday's Mass may be said on the
first free day of the week, which concerns other days and not this one; and its
note on the Breviary's October weeks, which concerns the Office. The act of
consecration with the Litany is a papal prescription outside the Mass
(*Quas primas* n. 28, above); the Missal prints neither (a search of the text
layer for the act found nothing), so neither enters the inventory.

## Appointed proper

Loci are the printed page and marginal number of the controlling edition, read
on 200- and 400-dpi page images of artifact PDF pp. 778-779 (printed pp.
697-698). Psalms are cited in the Missal's Vulgate numbering, with the Hebrew
number in parentheses (from the Hebrew columns of the repository's concordance
`artifact.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581.psalm-numbering-ee3c7757`,
SHA-256 `535761886df2…` recomputed and matched); Psalm 71:1 is a special case
noted below. "Said" means said in the Mass of 25 October 2026; the two printed
elements that are not said belong to votive use of the formulary on other
days and are recorded because they are text-bearing parts of the printed
formulary.

| Order and key | Element and printed locus | Liturgical place, extent and status |
|---|---|---|
| 1 `introit` | *Ant. ad Introitum*, printed citation *Apoc. 5, 12; 1, 6*; verse *Ps. 71, 1* (72:1); p. 697 left column, no. 3938 | Said. Antiphon *Dignus est Agnus, qui occisus est, accipere virtutem, et divinitatem, et sapientiam, et fortitudinem, et honorem. Ipsi gloria et imperium in saecula saeculorum.*; psalm verse *Deus, iudicium tuum Regi da: et iustitiam tuam Filio Regis.*; printed cue *V. Gloria Patri.*; repetition (RGMR 427). No Alleluia outside paschal time (RGMR 429). |
| 2 `collect` | *Oratio* *Omnipotens sempiterne Deus, qui in dilecto Filio tuo, universorum Rege, omnia instaurare voluisti*; p. 697 left column, no. 3939 | Said, the only Collect. Printed conclusion *Qui tecum vivit et regnat in unitate.* (RG 115 c, read p. XIX: the prayer names the Son at its end). Followed by the rubric *Et non fit commemoratio dominicae.* |
| 3 `epistle` | *Lectio Epistolae beati Pauli Apostoli ad Colossenses*, Col 1:12-20; p. 697 right column - p. 698 left column, no. 3940 | Said. Opens *Fratres: Gratias agimus Deo Patri*; ends *in Christo Iesu Domino nostro.* No shorter form. |
| 4 `gradual` | *Graduale* Ps 71:8 et 11 (72:8, 11); p. 698 left column, no. 3941 | Said (RGMR 469). Respond *Dominabitur a mari usque ad mare: et a flumine usque ad terminos orbis terrarum*; verse *Et adorabunt eum omnes reges terrae: omnes gentes servient ei.* |
| 5 `alleluia` | *Alleluia, alleluia*, verse Dan 7:14; p. 698 left column, no. 3942 | Said. Verse *Potestas eius, potestas aeterna, quae non auferetur: et regnum eius, quod non corrumpetur.*, then *Alleluia*. No Sequence. |
| — `tract` | Rubric *In Missis votivis post Septuagesimam, omissis Alleluia et versu sequenti, dicitur* *Tractus* Ps 88:27-28 et 30 (89:27-28, 30); p. 698 left column, no. 3943 | **Not said on this date.** Printed alternative for the votive Mass after Septuagesima: *Ipse invocabit me: Pater meus es tu … et thronum eius sicut dies caeli.* |
| — `paschal-alleluia` | Rubric *Tempore autem paschali omittitur graduale, et eius loco dicitur:* *Alleluia* with verses Dan 7:14 and Apoc 19:16; p. 698 left column, no. 3944 | **Not said on this date.** Printed alternative for paschal time, which the feast never reaches, so it serves votive use: the Dan 7:14 verse as at no. 3942, then *Habet in vestimento et in femore suo scriptum: Rex regum et Dominus dominantium. Alleluia.* |
| 6 `gospel` | *Sequentia sancti Evangelii secundum Ioannem*, Jn 18:33-37; p. 698 left and right columns, no. 3945 | Said. Opens *In illo tempore: Dixit Pilatus ad Iesum: Tu es Rex Iudaeorum?*; ends *omnis qui est ex veritate, audit vocem meam.* Printed cue *Credo.* follows. |
| 7 `offertory` | *Ant. ad Offertorium* Ps 2:8 (2:8); p. 698 right column, no. 3946 | Said. *Postula a me, et dabo tibi gentes hereditatem tuam, et possessionem tuam terminos terrae.* |
| 8 `secret` | *Secreta* *Hostiam tibi, Domine, humanae reconciliationis offerimus*; p. 698 right column, no. 3947 | Said secretly, the only Secret (RGMR 480-481). Printed conclusion *Qui tecum vivit et regnat in unitate.* Followed by *Et non fit commemoratio dominicae.* and *Praefatio propria.* |
| 9 `preface` | *Praefatio de D. N. Iesu Christo Rege*, *Praefationes sine cantu*, printed p. 291, no. 1080 (PDF 372, read); notated also at pp. 240-241 (solemn tone, PDF 321-322), pp. 268-269 (ferial tone, PDF 349-350) and appendix pp. [250]-[251] (*in tono solemniori*, PDF 1058-1059), located | Said or sung; appointed by the formulary's direction and RGMR 492, not chosen. Rubric *Sequens praefatio dicitur in Missis festivis et votivis de D. N. Iesu Christo Rege*; the dialogue; *Vere dignum … Qui unigenitum Filium tuum, Dominum nostrum Iesum Christum, Sacerdotem aeternum et universorum Regem, oleo exsultationis unxisti … regnum veritatis et vitae; regnum sanctitatis et gratiae; regnum iustitiae, amoris et pacis. Et ideo cum Angelis …*; then *Sanctus*. Printed outside the formulary but proper to this Mass, so it is inventoried here. |
| 10 `communion` | *Antiphona ad Communionem* Ps 28:10 et 11 (29:10-11); p. 698 right column, no. 3948 | Said (RGMR 504). *Sedebit Dominus Rex in aeternum: Dominus benedicet populo suo in pace.* |
| 11 `postcommunion` | *Postcommunio* *Immortalitatis alimoniam consecuti, quaesumus, Domine*; p. 698 right column, no. 3949 | Said, the only Postcommunion (RGMR 505). Printed conclusion *Qui tecum vivit et regnat in unitate.* Followed by *Et non fit commemoratio dominicae.* |

The keys above are the stable element keys this record proposes for the
manifest; whether `tract` and `paschal-alleluia` become manifest element keys
or are recorded only as printed options not said is for the authoring stages,
which must not present either as part of the 25 October Mass. The chant
rubrics are set both abbreviated and in full in this one formulary (*Ant. ad
Introitum*, *Ant. ad Offertorium*, but *Antiphona ad Communionem*); the
Communion's citation stands on the first text line after its rubric and the
Alleluia's inside its verse line. These are setting variables.

The formulary prints no Sequence, prophecy, proper *Communicantes* or *Hanc
igitur* (RGMR 501, read p. XXXIV: such variations are noted in the proper Mass,
and none is noted here), *Oratio super populum*, second or third oration of its
own, blessing, or alternative reading.

### Wording against the Clementine Vulgate

The comparisons below were made against the tracked Clementine Vulgate
(`edition.catholic-church.vulgata-clementina.ebible-latvuc`, its verse-text
artifacts) through `tools/tpt mass-propers show --calendar roman-1962 --mass
christ-the-king --bible clementine-vulgate` and the verse files directly; the
Epistle and Gospel were compared token by token by script after normalising
i/j, ligatures, accents, capitals and pointing. They are textual observations
about wording and boundary. No origin is asserted for any form.

- **Introit.** A cento. From Apoc 5:12 it takes *Dignus est Agnus … et
  honorem* without the Clementine's opening *dicentium voce magna* and without
  its closing *et gloriam, et benedictionem*; from Apoc 1:6 it takes only *ipsi
  gloria et imperium in saecula saeculorum*, without *et fecit nos regnum, et
  sacerdotes Deo et Patri suo* and without *Amen*. The verse is the first
  clause of the psalm: in all three tracked editions (Clementine, Challoner
  Douay, 1899 Douay) verse 71:1 is the title alone (*Psalmus, in Salomonem*; *A
  psalm on Solomon*) and the Missal's words stand at the head of their 71:2,
  which also carries *judicare populum tuum in justitia …*. The Missal's *Ps.
  71, 1* is therefore not the tracked editions' 71:1.
- **Epistle.** The Missal reads *Fratres: Gratias agimus* where the Clementine
  at v. 12 reads *gratias agentes*, and closes with *in Christo Iesu Domino
  nostro*, which the Clementine's v. 20 does not have. Every other word of vv.
  12-20 agrees.
- **Gradual.** *Dominabitur* without the Clementine's initial *Et* (v. 8); the
  verse agrees with v. 11.
- **Alleluia.** The verse is the second half of Dan 7:14 only, without *Et
  dedit ei potestatem, et honorem, et regnum: et omnes populi, tribus, et
  linguae ipsi servient*.
- **Tract (not said).** Agrees with Ps 88:27, 28 and 30, omitting v. 29.
- **Paschal Alleluia (not said).** Dan 7:14 as above; Apoc 19:16 without the
  Clementine's initial *Et*.
- **Gospel.** The liturgical opening *In illo tempore: Dixit Pilatus ad
  Iesum:* stands for the Clementine's *Introivit ergo iterum in praetorium
  Pilatus: et vocavit Jesum, et dixit ei:* at v. 33. Every other word of vv.
  33-37 agrees.
- **Offertory.** Agrees with Ps 2:8 (*hereditatem* for *haereditatem*).
- **Communion.** A cento of two half-verses: *Sedebit Dominus Rex in aeternum*
  is the second half of v. 10, without *Dominus diluvium inhabitare facit, et*;
  *Dominus benedicet populo suo in pace* is the second half of v. 11, without
  *Dominus virtutem populo suo dabit*.

## Other text-bearing parts of this Mass

These are fixed or rubrically appointed texts of the 1962 *Ordo Missae* and
appendix, not proper text. The study refers to them and does not reproduce the
Ordinary. *Ordo Missae* marginal numbers are those of the registered passage
records `…vatican-typica-1962.ordo-missae-ad-gradum`, `…ordo-missae-kyrie-gloria`,
`…ordo-missae-credo`, `…ordo-missae-conclusio` and
`…ordo-ad-aspergendam-aquam-benedictam`, which were not re-read on images here.

| Place | Text and appointment | Status and source |
|---|---|---|
| Before the principal Mass, where used | *Asperges me* with the Sunday blessing of water | A Sunday rite outside the Mass and outside this formulary (registered passage `…ordo-ad-aspergendam-aquam-benedictam`); not part of the appointed inventory. |
| Prayers at the foot of the altar | Ps 42 *Iudica me* through *Oramus te*; *Ordo Missae* nos. 1013-1023 | Said: RGMR 425 (p. XXXI, read) omits *Iudica* only in Passiontide Masses of the season and in Requiem Masses. |
| Introit doxology; Kyrie | *Gloria Patri*; ninefold Kyrie, no. 1024 | RGMR 427-428, 430 (p. XXXI, read). |
| After the Kyrie | *Gloria in excelsis*, no. 1025 | Said: RGMR 431 (read). No chant setting is chosen. |
| Before and after the Gospel | *Munda cor meum*, Gospel dialogue; homily | RGMR 471, 474 (p. XXXIII, read); nos. 1026-1028. |
| After the Gospel or homily | *Credo*, no. 1029 | Said: RGMR 475 a, b (read); printed cue after no. 3945. |
| After the Secret | Proper Preface, no. 1080 | Inventoried above as element 9. |
| Canon | *Te igitur* through the doxology | The one Roman Canon, said secretly (RGMR 500, read). No proper insertion (RGMR 501, read). |
| Conclusion | *Ite, missa est*, *Placeat*, blessing, last Gospel Jn 1:1-14 | RGMR 507-509 (located); nos. 1132-1139 per the registered conclusion passage. |
| After Mass, where kept | Act of consecration of mankind to the Sacred Heart with the Litany of the Sacred Heart | Prescribed by *Quas primas* n. 28 for this day; not printed in the Missal, outside the Mass, not part of the inventory. |

## Lawful study-text routes

- **Latin, the proper elements and the Preface: no settled basis yet.** The
  feast was instituted in December 1925, and
  `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`
  names *D. N. Jesu Christi Regis* (instituted 1925) among the formularies
  first published after the 1920 typical edition; it holds that 17 U.S.C.
  103(b) frees only preexisting material, and the 1962 facsimile is a
  collation witness, not a licence. None of the tracked typical-edition
  antecedents (1570, 1604, 1862, 1922 Mame) can carry a feast of 1925, and
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` has no
  row for this formulary. The scriptural elements are verbatim or centonized
  Vulgate, whose words stand in the public-domain Clementine, but the
  centonized forms (Introit, Communion, Epistle ending, Gospel opening) are the
  Mass's own arrangement; the orations and the Preface are 1925 compositions.
  `guidance/missals.md` §5 records the United States line as first publication
  abroad *before 1931*. The route to establish is therefore a witness to the
  formulary's first publication, or another printing of 1925-1930, read on page
  images and collated word for word with the 1962 page; leads, none checked
  here: the Holy See's own publication of the Mass and Office after *Quas
  primas*, and 1926-1930 Missal printings or their supplements. The tracked
  Lasance printing (next item) prints the Latin of every element but is a
  1945 American edition whose freedom from renewal covers Benziger's own
  contribution; whether it can carry the Holy See's Latin is for research to
  decide on the rights record, not assumed here.
- **The Lasance *New Roman Missal*, Benziger revision of 1945**
  (`edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945`;
  rights holding in `src/sources/inventories/lasance-new-roman-missal-rights-v1.toml`,
  public domain in the United States by nonrenewal, with the excluded
  appendix at pp. 1298a-1298n and insert at pp. 1302a-1302d, neither of which
  is concerned here). The registered scan
  `artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.internet-archive-facsimile-pdf-6cf3c3d0`
  was read from a copy matching its registered SHA-256
  `6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70`: PDF pp.
  1257-1261 (printed pp. 1256-1260) at 150 dpi. Printed p. 1256 is an
  engraving bearing *Copyright, 1936, by Benziger Brothers* with an English
  epigraph from 1 Paral 29:11-12; neither is used. Printed pp. 1257-1260
  print *Feast of Our Lord Jesus Christ, King, (White)*, *(Last Sunday in
  October)*, *Double of the First Class*, Latin and English in parallel for
  the Introit, Collect, Epistle, Gradual, Alleluia, Tract, Greater (paschal)
  Alleluia, Gospel, Offertory, Secret, Communion and Postcommunion. Its Latin
  orations agree in their words with the 1962 page as read here (orthography
  *ejus*, *Gentium*, *Ipse*; abbreviated conclusions *Qui tecum*). Its rubrics
  are pre-1960 and are not the 1962 order: it directs a commemoration of the
  occurring Sunday after each oration, which the 1962 forbids, and refers to
  *Preface No. 10, page 813*. Printed p. 813 (PDF 812, read at 150 dpi)
  prints *10. Preface of Jesus Christ, King*, Latin and English. In the tracked
  text artifact
  `…benziger-revised-1945.new-roman-missal-text-80b34759` (SHA-256
  `80b34759fb18…` recomputed and matched) the formulary runs from physical line
  136381 (heading) to 136832, and the Preface heading stands at line 86322. No
  passage record addresses either.
- **English, canonical Scripture.** The Douay-Rheims (Challoner) as registered
  (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  with `…american-1899-ebible` as the other registered Douay printing), read
  through `tools/tpt mass-propers show … --bible douay-rheims`. Its verses are
  not the Missal's forms at the centonized Introit and Communion, the Epistle's
  address and closing clause (Douay *Giving thanks to God the Father*), the
  Gospel's opening, and the Alleluia's half-verse. In the tracked printings
  the Introit's psalm verse stands inside Douay 71:2 (*Give to the king thy
  judgment, O God …*), not at 71:1, which they give to the title. English must
  never be composed to fill those differences; where the Douay cannot carry
  the Missal's form, the profile's rule is to say so and give the Latin with a
  description, or to use the hand missal's own English under its own
  attribution if research so decides.
- **English, the orations and the Preface.** No pre-1925 hand missal can carry
  them. The Lasance 1945 English above is the located route: Collect
  (*Almighty and eternal God, Who hast wished to restore all things through
  Thy beloved Son, the King of the universe*), Secret (*O Lord, we offer Thee
  this host for the reconciliation of humanity*), Postcommunion (*Fed with
  this immortal nourishment*) and Preface No. 10, read on the page images
  above. It is the 1945 book's own English, not an approved liturgical
  translation, and it renders a formulary whose surrounding rubrics differ from
  1962. No English for this formulary stands in
  `src/sources/inventories/roman-1962-proper-translations-v1.toml`, which is a
  shared record belonging to its own owner and is unchanged here.

No source was registered or retained in this stage. The existing library was
read first; everything fetched was either a registered artifact matched to its
registered hash or a live response whose identity and hash are written down
above. No liturgical owner is imported: the formulary and its Preface are
printed in this family's own Missal and are local to this leaf, so there is no
shared-formulary Makefile dependency to declare.

## Shared records: observations for their owners

This stage owns no source, calendar or tool record, so these are reported
rather than repaired.

- `src/sources/calendars/roman-1962/propers.yaml`, mass `christ-the-king`: (1)
  the Communion is encoded as Psalm 28:10 alone where the Missal prints *Ps.
  28, 10 et 11* and the antiphon's second half is v. 11; (2) the votive Tract
  is encoded as an ordinary proper of the day without its *In Missis votivis
  post Septuagesimam* condition, and the paschal Alleluia (no. 3944, Dan 7:14
  with Apoc 19:16) is absent; (3) the orations and the Preface are not
  represented. The entry's `registry: 'F01'` now matches the profile, while
  the file's header note still says the F series has no enumerated identity
  and that the feast carries a synthetic id.
- Psalm 71:1. The Missal cites its Introit verse *Deus, iudicium tuum Regi da*
  as Ps 71:1, but the three tracked editions and the psalm concordance
  (`…challoner-gutenberg-1581.psalm-numbering-ee3c7757`, Vulgate 71:1 marked
  "psalm inscription") make 71:1 the title, and no verse-alias row in the
  Clementine (`…ebible-latvuc.verse-aliases-52634891`) or the Douay redirects
  it. `tools/tpt mass-propers show` therefore serves the title for this verse,
  and `tools/tpt proper-chronology loci` resolves the Introit to `Ps.71.1`, the
  title, with the Communion as `Ps.28.10` only and the not-said Tract
  (`Ps.88.27`, `Ps.88.28`, `Ps.88.30`) as an element.
- `commentary-work-index formulary --calendar roman-1962 --mass christ-the-king`
  compares 40 loci and lists none: no liturgical commentator in
  `src/sources/commentary/formulary-loci.yaml` has this formulary.
- The 1962 passage records hold no passage for this formulary's orations
  (`temporal-…-orations` has no Christ the King entry) or for its Preface
  (`…praefationes-sine-cantu` covers the common Preface only).

## Remaining verification for research

- Collate every proper element and the Preface word for word against the 1962
  page images at 200 and 400 dpi; write `propers/retrieved.txt` and
  `propers/verified.md` with the loci, conclusions and orthography.
- Establish, or record the absence of, a lawful basis for publishing the Latin
  of this 1925 formulary and its Preface (above); until then the studies give
  locators, incipits and descriptions rather than the full Latin. Decide on
  the record whether the Lasance printing can carry the Latin, and register
  any passage relied on.
- Decide the English display: Douay-Rheims for the scriptural elements where it
  carries the Missal's form, and the Lasance 1945 English for the orations and
  Preface under its own attribution, with the differences listed above
  disclosed; record the Lasance's pre-1960 rubrics as not the 1962 order.
- Settle the chronology inputs before generating `research/chronology.toml` and
  `research/chronology-annotations.tex`: the Introit verse must resolve to the
  words *Deus, iudicium tuum Regi da …*, not the title; the Communion needs both
  Ps 28:10 and 28:11; and the not-said Tract and paschal Alleluia should not be
  dated as elements of this Mass unless the manifest keeps them, labelled. No
  biblical date is asserted in this record. The distinct directly appointed
  passages said on 25 October, in canonical then verse order, are Ps 2:8, Ps
  28:10-11, Ps 71:1 (the *Deus, iudicium* clause), Ps 71:8 and 11, Dan 7:14, Jn
  18:33-37, Col 1:12-20, Apoc 1:6 and Apoc 5:12; each is appointed once. The
  printed, not-said options add Ps 88:27-28, 30 and Apoc 19:16.
- Read each appointed passage in its complete literary context: Apoc 1:4-8 and
  the throne-room vision of Apoc 4-5; Ps 71 whole as a royal psalm; Dan 7:9-14
  with its interpretation; Col 1:9-23; Jn 18:28-19:16 with the trial before
  Pilate; Ps 2 whole; Ps 28 whole; and, for the printed options, Ps 88:20-38
  and Apoc 19:11-16. Run the reception sweep. `commentary-work-index` offers no
  liturgical commentator for this formulary; record that negative result and
  search the passages' exegetes directly.
- Register a dated edition and passage for 25 October 2026 if the study relies
  on either dated Ordo, and register *Quas primas* if the study cites it.
- Resolve, only if the study relies on them, what this stage did not settle:
  the Asperges placement, a local church consecration, any particular-calendar
  overlay, and the Latin text and official publication of *Quas primas* and of
  the Mass. None is needed for the universal formulary on this date.
- Bind the controlling sources in `research/source-bindings.toml` and declare
  the external owners actually relied on in `research/review-dependencies.toml`.
  The authorities adopted here are the 1962 facsimile artifact, the
  facsimile-rights inventory, the Latin provenance ledger (for its negative
  result), the Lasance edition, its registered scan and text artifact and its
  rights inventory, the Clementine Vulgate edition and verse-alias artifact,
  the Douay-Rheims editions and the psalm concordance, `guidance/missals.md`
  §5 as the governing statement of the pre-1931 line (guidance, not a source
  owner), and, as computation inputs, `src/sources/calendars/roman-1962/propers.yaml`
  and `rubrics.yaml`.

## Research-stage verification (19 October 2026)

The research stage of the same run read this record against the evidence and
leaves its inventory, occurrence, branch and loci unchanged: the formulary,
the Preface and their marginal numbers were re-read on the 1962 page images at
200 and 400 dpi and agree with the table above (`propers/verified.md`). Three
statements above are now superseded, and are corrected here rather than
rewritten:

- **The Communion range.** *Shared records* item (1) and the Ps 71:1 item's
  "with the Communion as `Ps.28.10` only" describe the calendar before commit
  `aa94dd3b4`, which encoded the Communion as Ps 28:10-11 with the
  maintainer's authorization before research began. `tools/tpt
  proper-chronology loci` now yields `Ps.28.10 Ps.28.11`, verified in this
  stage. The other shared-record items stand.
- **The Latin's publication basis is settled.** The formulary and its Preface
  were first published by the Sacred Congregation of Rites in *Acta Apostolicae
  Sedis* 17 (1925), fascicle n. 15 of 28 December 1925, pp. 666-668, with the
  decree *Urbis et Orbis* of 12 December 1925. Read on page images of a
  microfilm scan registered by the research stage and collated word for word
  with the 1962 page, it carries every word of every element and of the
  Preface's body, with three bounded exceptions recorded in
  `propers/verified.md`. The Latin is therefore published on 17 U.S.C. 103(b)
  plus that pre-1931 witness. The Lasance printing is not used as a Latin
  witness.
- **The English display is decided** as `propers/verified.md` records:
  Douay-Rheims for the scriptural elements, with the Missal's liturgical frames
  given in Latin (or in the Lasance English under its attribution), and the
  Lasance 1945 English for the orations and the Preface, its pre-1960 rubrics
  disclosed.
- **The not-said Tract and paschal Alleluia on page 2 (iteration 1).** The
  task list's "should not be dated as elements of this Mass unless the
  manifest keeps them, labelled" cannot be followed as written. The chronology
  wiring reads the calendar entry, which carries the Tract and omits the
  paschal Alleluia, and the `orientation-v2` gate prints every generated row
  whatever the manifest declares. The calendar entry stays unchanged in this
  run. So the Tract's two rows print on page 2 with the rubric's label
  (*printed for votive Masses after Septuagesima, never said on this feast*),
  and the paschal Alleluia has no row; `research/scope.md` §8 records both.
