# Celebration context and complete appointed inventory

Resolved 15 October 2026 for the `proper-study` v11 production of the Claude
1962 leaf, run `a8bcc37ea3420a07`, seeded at commit
`cc2e968320e2416ef9049f1c6910ac281df8feb9`. The production-plan entry of
2026-10-15 in `guidance/liturgy/propers-production-plan.md` authorizes provider
`claude` for this one identity and Sunday 18 October 2026, as an independent
production that is not a companion to or derivative of any other leaf, the GPT
leaf for the same identity included. `ARGS.research_handoff` is `none`, so no
handoff was supplied. The other provider's leaf for this identity, every
postconciliar record, and this provider's neighbouring Sundays are outside this
record's evidence; none was opened and nothing below is taken from them. The
Twentieth Sunday's context record of this provider was read only as a model of
the record's shape; no finding of it is relied on unless re-read here. Several
provider-neutral library records were registered on 2026-10-12 in the course of
the other production (the Cummiskey St Luke checked English and the Lasance
*Pro Fidei propagatione* checked orations, named below); they are used here
only as library evidence, and the pages behind them were read afresh in this
stage. This record settles what is studied. It holds no study prose, spoken
text, timing claim or review verdict; the research stage collates the sources
and may correct it from evidence.

## Identity, governing books and territory

- Canonical identity:
  `liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost`,
  catalog ID `61` in the 1962 temporal registry of
  `guidance/liturgy/roman-1962-propers.md` (IDs 41-63 run from the Second
  Sunday after Pentecost, with the Sacred Heart at 42, to the Twenty-third
  Sunday). Calendar family `roman-1962`. `tools/check-proper-identity
  --document … --calendar roman-1962` passes. The finding-aid mass index
  `src/sources/calendars/roman-1962/propers.yaml` carries the formulary as
  `pentecost-21`, `registry: '61'`; that index is a lead and never the source
  of record for any wording.
- Governing edition: *Missale Romanum*, editio typica, Typis Polyglottis
  Vaticanis 1962 (`edition.catholic-church.missale-romanum.vatican-typica-1962`),
  controlled on the page images of
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.
  A copy fetched in this stage from the registered `source_url` matched the
  registered SHA-256
  `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` and
  82,815,941 bytes before any page was read. The formulary was read on page
  images rendered from that file at 200 and 400 dpi; the commemorated
  formulary, the *Tabula orationum* page, the *Calendarium* and the rubrics
  cited below as "read" at 200 or 300 dpi. The text layer served only to
  locate pages, and loci marked "located" were found on it and not re-read on
  an image.
- Printed heading and rank: *DOMINICA VIGESIMA PRIMA post Pentecosten*, *II
  classis*, Proper of Time, printed p. 413 right column (artifact PDF p. 494).
  The running head of p. 413 already reads *Dominica XXI post Pentecosten*,
  although its left column and most of its right column carry the Twentieth
  Sunday; p. 414 (PDF 495) is headed *Dominica XXI post Pentecosten*; p. 415
  (PDF 496), whose left column ends this formulary, is headed *Dominica XXII
  post Pentecosten*. The running heads do not bound the formulary.
- Formulary boundary: it begins at marginal no. 1699 in the right column of
  p. 413, immediately after the Postcommunion *Ut sacris, Domine, reddamur
  digni muneribus* (no. 1698) of the Twentieth Sunday, and ends with its own
  Postcommunion, no. 1708, in the left column of p. 415, after which the
  heading *DOMINICA VIGESIMA SECUNDA post Pentecosten*, II classis, opens a
  different formulary at no. 1709. Marginal nos. 1699-1708, each printed whole
  and legible on these three pages.
- Governing books within that edition, read or located where cited below: the
  *Calendarium*; the *Rubricae generales* (part I of the 1960 code as printed,
  cited RG); the *Rubricae generales Missalis romani* (part III, cited RGMR);
  the *Ordo Missae*; the *Praefationes*; the *Tabula orationum* that closes the
  Proper of Time; the Sanctorale (for the commemorated feast); the votive Mass
  *Pro Fidei propagatione* among the *Missae votivae ad diversa*. Part II, the
  *Rubricae generales Breviarii romani*, is not printed in this witness.
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
  (`ARGS.audience`). RGMR 474 (printed p. XXXIII, PDF 31, located) places a
  brief homily after the Gospel, *praesertim in dominicis*; the homily is
  authored preaching and adds no text to this inventory.

## Occurrence on 18 October 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
roman-1962 --date 2026-10-18 --json` returns candidate `pentecost-21`, "slot 21
of 26 Sundays after Pentecost", season after Pentecost, no Lectionary value and
nothing unresolved, and a second candidate, the fixed-date feast
`s-lucae-evangelistae`, II class. The 2026 anchors in
`guidance/liturgy/calendar-computation.md` are Easter 5 April, Pentecost 24
May, Trinity Sunday 31 May (the first Sunday after Pentecost) and First Sunday
of Advent 29 November; liturgical year 30 November 2025 - 28 November 2026.
Thirty-one May plus twenty weeks is 18 October, the twenty-first Sunday of the
run. With 26 Sundays after Pentecost in 2026, RG 18 b (printed p. XII, PDF 10,
read) places the resumed Fifth and Sixth Sundays after the Epiphany at slots 24
and 25, so the resumption does not reach slot 21. As an independent check, the
*Calendarium* (printed p. LI, PDF 53, read) gives 18 October the dominical
letter *d*; 2026, beginning on a Thursday, has *D* as its dominical letter.
The Sundays of October 2026 fall on the 4th, 11th, 18th and 25th: under RG 19
(printed p. XII, read) 18 October is the third Sunday of the month, and it is
the penultimate Sunday of October, which matters for RGMR 453 below. The last
Sunday, 25 October, is Christ the King (RG 17 d; *Calendarium* note under
October, read) and does not touch this date.

**The occurring feast.** The *Calendarium*, printed p. LI, gives 18 October as
*S. Lucae Evangelistae, II classis*. Its formulary stands in the Sanctorale
under *Die 18 octobris*, *S. LUCAE EVANGELISTAE*, *II classis*, printed
pp. 689-691, nos. 3882-3892 (PDF 770-772), read on the page images for the
heading and orations: Introit *Mihi autem nimis honorati* no. 3882; Collect
*Interveniat pro nobis, quaesumus, Domine, sanctus tuus Lucas Evangelista*
no. 3883; Epistle 2 Cor 8:16-24 no. 3884; Gradual no. 3885; Alleluia no. 3886;
Gospel Lk 10:1-9 no. 3887; Offertory no. 3888; Secret *Donis caelestibus da
nobis, quaesumus, Domine, libera tibi mente servire* no. 3889, followed by the
direction *Praefatio de Apostolis*; Communion no. 3890; Postcommunion *Praesta,
quaesumus, omnipotens Deus: ut, quod de sancto altari tuo accepimus* no. 3891;
votive Tract no. 3892 (p. 691, located). Each of the three orations prints the
conclusion *Per Dominum.*, which is RG 115 a's form (printed p. XIX, PDF 17,
located).

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
roman-1962 --date 2026-10-18 --json` is settled: winner `pentecost-21`, a
second-class Sunday (RG 12; RG 91 row 15); St Luke is returned `commemorated`
as an ordinary commemoration (RG 109) of a row-16 feast; the low-Mass oration
list holds the Sunday Collect and a second collect of St Luke "with a second
conclusion", and the sung non-conventual list holds the Sunday Collect alone.
That computation does not carry RGMR 453, which governs this date (see below),
so its oration lists are incomplete for 18 October 2026. Every locus it cites,
and the further loci the result depends on, were read on the page images in
this stage:

- RG 10 and 12, printed p. XII (PDF 10): Sundays are of I or II class, and
  every Sunday not named in RG 11 is of II class; this Sunday is not named
  there. RG 16 (same page): a II-class Sunday is preferred in occurrence to
  II-class feasts, save a feast of the Lord (16 a). St Luke's feast is not a
  feast of the Lord.
- RG 91, table of precedence, printed pp. XVI-XVII (PDF 14-15): row 15
  *Dominicae II classis*; row 16 *Festa II classis Ecclesiae universae, quae
  non sunt Domini*. Row 12, first-class *propria*, outranks a II-class Sunday
  only in a particular church, an overlay not applied here.
- RG 94-95, printed p. XVII (PDF 15): a commemoration fixed to its day is not
  transferred; a feast other than I class that is accidentally impeded is
  commemorated or, that year, omitted, according to the rubrics. St Luke is
  therefore neither transferred nor celebrated on another day.
- RG 107-109, printed p. XVIII (PDF 16): commemorations are privileged or
  ordinary; the privileged are those of a Sunday, a I-class day, the days
  within the Christmas octave, the September Ember ferias, the Advent, Lent and
  Passiontide ferias, and the Greater Litanies; all others, this one included,
  are ordinary. RG 108: ordinary commemorations are made only at Lauds, in
  conventual Masses and in all low Masses (*in omnibus Missis lectis*).
- RG 111, printed p. XVIII: (a) on I-class days and *in Missis in cantu non
  conventualibus* no commemoration is admitted save one privileged; (b) *in
  dominicis II classis* one commemoration only, of a II-class feast. RGMR 434
  a and b, printed p. XXXI (PDF 29), state the same for the orations of the
  Mass, and RGMR 435 omits any oration beyond the number allowed.
- RGMR 437 a, printed p. XXXI: commemorations are always said under a
  separate conclusion. RGMR 480 (printed p. XXXIV, PDF 32, read) and 505
  (p. XXXV, PDF 33, located): as many Secrets and Postcommunions as orations at
  the beginning, in the same number, manner and order.
- RGMR 483, printed p. XXXIV (PDF 32): *Nulla commemoratio, in Missa occurrens,
  praefationem propriam inducit.* St Luke's Preface of the Apostles (RGMR 497)
  is therefore not taken in the Sunday Mass.

**The oration *Pro Fidei propagatione* (RGMR 453).** RGMR 453, printed p.
XXXII (PDF 30), read: *Paenultima dominica mensis octobris, aut alia ab
Ordinario loci statuta « pro Missionibus », in omnibus Missis, orationi Missae
additur, sub unica conclusione, oratio pro Fidei propagatione, exceptis diebus
sub nn. 1, 2, 3 et 8 in tabella praecedentiae recensitis.* On the same page,
RGMR 444 c lists n. 453 among the orations said under one conclusion with the
oration of the Mass; RGMR 445 admits only one such oration; and RGMR 446
counts it together with the Mass's oration and requires it *etiam in Missis in
cantu*. A II-class Sunday is row 15, not one of the excepted rows 1, 2, 3 and
8 (RG 91, read). On 18 October 2026, the penultimate Sunday of October, the
oration is therefore added in every Mass, sung or low, unless the local
Ordinary has appointed another day *pro Missionibus*, which is a local fact not
computed here. The texts are printed in the *Tabula orationum*, printed p. 427
(PDF 508), read on a 300-dpi image, under *PRO FIDEI PROPAGATIONE*: *Oratio*
*Deus, qui omnes homines vis salvos fieri et ad agnitionem veritatis venire*
no. 1806, concluding *Qui tecum vivit et regnat in unitate* (RG 115 c's form
for a prayer that names the Son at its end); *Secreta* *Protector noster,
aspice, Deus, et respice in faciem Christi tui* no. 1807, concluding *Per
eundem Dominum*; *Postcommunio* *Redemptionis nostrae munere vegetati* no.
1808, concluding *Per Dominum*. The same three prayers stand in the votive Mass
*18. Pro Fidei propagatione*, appendix pp. [85]-[87], nos. 4833, 4841 and 4843
(PDF 893-895, located). How the Sunday oration and this one are joined and
concluded when said under one conclusion is not settled here.

The rubrical result for this date is a branch by kind of Mass, not by choice:

- **Low Mass, and any conventual Mass:** the Sunday Mass with the oration *pro
  Fidei propagatione* under one conclusion with each Sunday oration, then the
  commemoration of St Luke under a separate conclusion. Collects: *Familiam
  tuam* with *Deus, qui omnes homines* (one conclusion), then *Interveniat pro
  nobis*. Secrets: *Suscipe, Domine, propitius hostias* with *Protector
  noster*, then *Donis caelestibus*. Postcommunions: *Immortalitatis
  alimoniam* with *Redemptionis nostrae*, then *Praesta, quaesumus, omnipotens
  Deus*. Nothing else of St Luke's formulary travels: not its chants, lessons,
  Preface (RGMR 483) or colour.
- **Sung Mass that is not conventual (a parish *Missa cantata* or *solemnis*):**
  the Sunday Mass with the oration *pro Fidei propagatione* under one
  conclusion with each Sunday oration, and no commemoration of St Luke (RG
  111 a; RGMR 434 a, 446).
- **Where the Ordinary has fixed another day *pro Missionibus*:** the two
  branches above without the *Pro Fidei propagatione* orations.

No other universal feast, vigil, octave, Ember day or seasonal substitution
falls on the date. Green vestments follow RG 127 b, printed p. XX (PDF 18,
located): *a feria II post dominicam I post Pentecosten, usque ad sabbatum
ante Adventum*; neither the commemoration nor the added oration changes the
colour. RGMR 461 (printed p. XXXIII, located) permits the *oratio votiva ad
libitum* only on IV-class days, so none is added. Other orations added by
local fact are not computed: an *oratio imperata* (RGMR 454-457, read; 457 d
forbids it on I- and II-class days in any case) and the oration for a diocesan
bishop's anniversary (RGMR 449, read), which depends on the diocese.

**Closed alternative: the votive Mass *Pro Fidei propagatione*.** RGMR 369,
printed p. XXVII (PDF 25), read, permits in each church one Mass *Pro Fidei
propagatione*, *tamquam votiva II classis*, *die quo peculiares habentur
celebrationes pro Missionibus*, and RGMR 341 (p. XXV, PDF 23, read) permits
II-class votive Masses on all days of II, III and IV class, this Sunday
included. Where that one Mass is said, it replaces the Sunday's formulary at
that Mass only: violet (RG 129 a, located), with the Credo because of the
Sunday (RGMR 475 a, located; RGMR 343 a, read), and under RGMR 343 b with only
one commemoration. Its full order is not resolved here because it is not the
object of study. Whether a given church has such a celebration is local.

**No ipso-iure external solemnity on this Sunday.** RGMR 358, printed p. XXVI
(PDF 24), read, gives an external solemnity *ipso iure* only to (a) the Sacred
Heart, (b) the Rosary *in dominica I mensis octobris* (in 2026, 4 October),
(c) the Purification under its condition, and (d)-(h) principal patrons,
titulars, dedications and founders, all particular to a place or institute.
Under RGMR 358 i a feast of the universal calendar kept *cum peculiari populi
concursu* may have an external solemnity at the local Ordinary's judgement,
and RGMR 359 lets one be kept on the day the feast is impeded; whether any
place keeps St Luke in that way on this Sunday is local and not computed.
RGMR 360 would then admit one sung and one low Mass, or two low Masses,
*tamquam votivae II classis*. None of these alters the Sunday's formulary,
which remains the object of study.

**Dated official witnesses.** Two dated Ordos of institutes that celebrate with
the 1962 books were read live for this date. Neither response is retained or
registered, and neither changes any registration; both are held only in this
run's scratch area. Their SHA-256 values are recorded so that the research
stage can register a dated edition and passage if it relies on them.

- FSSP France, *Ordo du mois*, <https://www.fssp.fr/ordo-du-mois/>, read
  2026-10-15, response 169,686 bytes, SHA-256
  `d9441774025259f670de062cd04f29151e905e935e017fb15571b9cdfd50a99f`:
  *Dimanche 18 octobre* — *21e Dimanche après la Pentecôte (2ème classe,
  Vert)*. The line names no commemoration and no added oration; the Ordo
  prints one line per day and this silence is not read as an omission.
- ICRSP France, *Ordo*, <https://icrspfrance.fr/ordo.php?d=2026-10-01>, read
  2026-10-15, response 115,868 bytes, SHA-256
  `77759ed6f4055628e77afb9835d16d18186d7caca622cd9c81747b4177c5673a`:
  *dimanche 18 octobre 2026* — *XXIe Dimanche après la Pentecôte (4e
  d'octobre)*, *Temps Per Annum*, second class, green; Gloria, Credo, Trinity
  Preface; at Lauds *Mémoire de S. Luc, Évangéliste*; notes: *Le IVe Dim.
  d'octobre est chaque année consacré aux Missions. L'oraison pro Fidei
  Propagatione remplace celle pour le Pape (une seule oraison impérée par
  messe)*; Mass *Messe propre (In voluntate tua)*, *Mém. pro Fidei
  Propagatione sous la même conclusion que les oraisons de la Messe & de S.
  Luc*, Credo, Trinity Preface.

Computation, the printed calendar and both dated witnesses agree on the
identity, the second class and the green colour; the ICRSP entry also names
the Mass by its Introit, gives the Trinity Preface, carries the oration *pro
Fidei propagatione* and remembers St Luke. Nothing fails closed. Three things
in that witness are its own and are not imported. Its numbering of the Sunday
as the fourth of October, and its note that the third week of October is
omitted this year, belong to the Breviary's reckoning of the Office, not to
the Mass; RG 19 makes 18 October the third Sunday of the month. Its *Oratio
pro Papa*, displaced here by the mission oration, is an institute observance
whose basis was not examined. Its phrase placing the mission oration "under
the same conclusion as the orations of the Mass and of St Luke" is not adopted
as stated: RGMR 453 joins it to the oration of the Mass, and RGMR 437 a says a
commemoration under a separate conclusion; the witness also does not
distinguish low from sung Mass, which RG 108 and 111 a do. This record follows
the books.

## Appointed proper

Every element is required and none has an alternative within the formulary:
the pages print no option, no choice and no substitute. Loci are the printed
page and marginal number of the controlling edition, read on 200- and 400-dpi
page images of artifact PDF pp. 494-496. Psalms are cited in the Missal's
Vulgate numbering, with the Hebrew number of the repository's psalm concordance
(`…/challoner-gutenberg-1581/artifacts/psalm-numbering-ee3c7757/psalm-numbering.tsv`,
SHA-256 `535761886df2…` recomputed and matched) in parentheses; the English
verse offset is zero for Pss 89, 113:1-8 and 118.

| Order and key | Element and printed locus | Liturgical place, extent and boundary |
|---|---|---|
| 1 `introit` | *Antiphona ad Introitum* *In voluntate tua, Domine*, printed citation *Esth. 13, 9 et 10-11*; verse Ps 118:1 (119:1); p. 413 right column, no. 1699 | Entrance chant (RGMR 427, p. XXXI): antiphon *In voluntate tua, Domine, universa sunt posita, et non est qui possit resistere voluntati tuae: tu enim fecisti omnia, caelum et terram, et universa quae caeli ambitu continentur: Dominus universorum tu es*; psalm verse *Beati immaculati in via: qui ambulant in lege Domini*; printed cue *V. Gloria Patri*; repetition. No Alleluia outside paschal time (RGMR 429). |
| 2 `collect` | *Oratio* *Familiam tuam, quaesumus, Domine, continua pietate custodi*; p. 414 left column, no. 1700 | First oration of the Mass (RGMR 433). The conclusion is printed in full, *Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate Spiritus Sancti Deus: per omnia saecula saeculorum. R. Amen.* On this date the oration *pro Fidei propagatione* is joined to it under one conclusion, and at low and conventual Masses St Luke's Collect follows under a separate conclusion (see *Occurrence*). |
| 3 `epistle` | Eph 6:10-17; p. 414 left column, no. 1701 | *Lectio Epistolae beati Pauli Apostoli ad Ephesios*. Opens *Fratres: Confortamini in Domino*; ends at v. 17, *et gladium spiritus, quod est verbum Dei*. No shorter form. |
| 4 `gradual` | Ps 89:1-2 (90:1-2); p. 414 left column, no. 1702 | After the Epistle (RGMR 469): respond *Domine, refugium factus es nobis, a generatione et progenie*, verse *Priusquam montes fierent, aut formaretur terra et orbis: a saeculo et usque in saeculum tu es, Deus*. |
| 5 `alleluia` | Ps 113:1 (114:1); p. 414 left column, no. 1703 | *Alleluia, alleluia* with verse *In exitu Israel de Aegypto, domus Iacob de populo barbaro*, then *Alleluia*. No Tract and no Sequence. |
| 6 `gospel` | Mt 18:23-35; p. 414 right column, no. 1704 | *Sequentia sancti Evangelii secundum Matthaeum*. Opens *In illo tempore: Dixit Iesus discipulis suis parabolam hanc: Assimilatum est regnum caelorum homini regi*; ends at v. 35, *si non remiseritis unusquisque fratri suo de cordibus vestris*. Printed cue *Credo.* follows. |
| 7 `offertory` | *Ant. ad Offertorium*, printed citation *Iob 1*; p. 415 left column, no. 1705 | *Vir erat in terra Hus, nomine Iob: simplex et rectus, ac timens Deum: quem Satan petiit, ut tentaret: et data est ei potestas a Domino in facultates et in carnem eius: perdiditque omnem substantiam ipsius et filios: carnem quoque eius gravi ulcere vulneravit.* |
| 8 `secret` | *Secreta* *Suscipe, Domine, propitius hostias*; p. 415, no. 1706 | Said secretly, as many as the opening orations (RGMR 480-481). Printed conclusion *Per Dominum nostrum.* Followed by the printed direction *Praefatio de Ssma Trinitate.* |
| 9 `communion` | *Antiphona ad Communionem* Ps 118:81, 84 et 86 (119:81, 84, 86); p. 415, no. 1707 | After the Communion rites (RGMR 504): *In salutari tuo anima mea, et in verbum tuum speravi: quando facies de persequentibus me iudicium? iniqui persecuti sunt me, adiuva me, Domine Deus meus.* |
| 10 `postcommunion` | *Postcommunio* *Immortalitatis alimoniam consecuti*; p. 415, no. 1708 | As many as the opening orations (RGMR 505). Printed conclusion *Per Dominum nostrum.* |

This edition sets the chant rubrics both in full and abbreviated in the same
formulary (*Antiphona ad Introitum* and *Antiphona ad Communionem*, but *Ant.
ad Offertorium*); the abbreviation is a setting variable. At the Communion the
citation is printed on the first text line after the rubric, and at the
Alleluia the citation *Ps. 113, 1* inside the verse line. The Collect prints
its conclusion in full while the Secret and Postcommunion print *Per Dominum
nostrum.*; the printed length is a setting variable.

### Orations added on this date

These are not part of the Sunday's formulary. Each is said after the
corresponding Sunday oration.

| Place | Text and printed locus | Status |
|---|---|---|
| With the Collect, one conclusion | *Pro Fidei propagatione* *Deus, qui omnes homines vis salvos fieri*; *Tabula orationum*, p. 427 right column, no. 1806 (PDF 508) | Every Mass, sung or low, on the penultimate Sunday of October unless the Ordinary appointed another day (RGMR 444 c, 445-446, 453). Printed conclusion *Qui tecum vivit et regnat in unitate.* |
| With the Secret, one conclusion | *Protector noster, aspice, Deus*; p. 427, no. 1807 | As above (RGMR 480). Printed conclusion *Per eundem Dominum.* |
| With the Postcommunion, one conclusion | *Redemptionis nostrae munere vegetati*; p. 427, no. 1808 | As above (RGMR 505). Printed conclusion *Per Dominum.* |
| After the Collect, separate conclusion | St Luke Collect *Interveniat pro nobis*; p. 689 right column, no. 3883 (PDF 770) | Commemoration, low and conventual Mass only (RG 108, 111 b; RGMR 434 b, 437 a). Printed conclusion *Per Dominum.* |
| After the Secret, separate conclusion | St Luke Secret *Donis caelestibus da nobis*; p. 690 right column, no. 3889 (PDF 771) | As above. Its Preface direction does not apply (RGMR 483). |
| After the Postcommunion, separate conclusion | St Luke Postcommunion *Praesta, quaesumus, omnipotens Deus: ut, quod de sancto altari tuo accepimus*; p. 690 right column, no. 3891 (PDF 771) | As above. |

### Wording against the Clementine Vulgate

The comparisons below were made against the tracked Clementine Vulgate
(`edition.catholic-church.vulgata-clementina.ebible-latvuc`, its verse-text
artifacts) through `tools/tpt mass-propers show --calendar roman-1962 --mass
pentecost-21 --bible clementine-vulgate`, with the Epistle and Gospel compared
token by token by script after normalising i/j, ligatures, accents and
pointing. They are textual observations about wording and boundary. Whether a
chant follows an older Latin text, and which, is left to research, and no
origin is asserted here.

- **Introit.** The antiphon is not a continuous Vulgate text. The Clementine
  at Esth 13:9-11, Mardochai's prayer, reads *in ditione enim tua cuncta sunt
  posita, et non est qui possit tuae resistere voluntati, si decreveris
  salvare Israel. Tu fecisti caelum et terram, et quidquid caeli ambitu
  continetur. Dominus omnium es, nec est qui resistat majestati tuae.* The
  Missal reads *In voluntate tua* for *in ditione enim tua*, *universa* for
  *cuncta*, *resistere voluntati tuae* in another order, adds *enim … omnia*,
  reads *universa quae … continentur* for *quidquid … continetur* and *Dominus
  universorum tu es* for *Dominus omnium es*, and has nothing of *si decreveris
  salvare Israel* or the closing clause. The verse omits the Clementine's
  title *Alleluja* and letter heading *Aleph*, which the Clementine counts
  inside Ps 118:1.
- **Epistle.** The Missal reads *Fratres: Confortamini* where the Clementine
  opens v. 10 *De cetero, fratres, confortamini*, and spells *exstinguere* for
  *extinguere*. Every other word of vv. 10-17 agrees.
- **Gradual.** The Missal reads *a generatione et progenie* where the
  Clementine at Ps 89:1 reads *a generatione in generationem*, and omits the
  title *Oratio Moysi, hominis Dei*. The verse agrees.
- **Alleluia.** The verse agrees with Ps 113:1, without the Clementine's title
  *Alleluja*.
- **Gospel.** The liturgical opening *In illo tempore: Dixit Iesus discipulis
  suis parabolam hanc:* stands for the Clementine's *Ideo* at the head of
  v. 23. The Missal reads *suffocabat* where the Clementine at v. 28 reads
  *suffocavit*, and spells *milia* and *venumdari* for *millia* and
  *venundari*. Every other word of vv. 23-35 agrees.
- **Offertory.** The Missal cites only *Iob 1*. Its first clause agrees with
  Job 1:1 in shortened form (the Clementine reads *et erat vir ille simplex,
  et rectus, ac timens Deum, et recedens a malo*); the rest narrates the
  testing in words that are not the Clementine's: *quem Satan petiit, ut
  tentaret* has no counterpart, *data est ei potestas … in facultates et in
  carnem eius* summarises Job 1:12 and 2:6, *perdiditque omnem substantiam
  ipsius et filios* summarises Job 1:13-19, and *carnem quoque eius gravi
  ulcere vulneravit* stands for Job 2:7, *percussit Job ulcere pessimo*. The
  finding aid resolves the element to Job 1:1, 1:12 and 2:6-7.
- **Communion.** The Missal reads *In salutari tuo* for the Clementine's
  *Defecit in salutare tuum* (v. 81), *speravi* for *supersperavi*, *iniqui*
  for *inique* (v. 86), omits *Quot sunt dies servi tui?* (v. 84) and *Omnia
  mandata tua veritas* (v. 86), and adds *Domine Deus meus* after *adiuva me*.
  It omits the letter heading *Caph*.

The formulary prints no Tract, Sequence, prophecy, proper *Communicantes* or
*Hanc igitur* (RGMR 501: such variations are noted in the proper Mass, and none
is noted here), *Oratio super populum* (RGMR 506: Lenten and Passiontide
ferias), second or third oration of its own, blessing, or alternative reading.
The 1862 antecedent's *Secunda Oratio A cunctis*, *Alia Secreta Exaudi nos
Deus*, *Alia Postcommunio Mundet et muniat* and *Tertia ad libitum*, printed on
the same pages, belong to the pre-1960 rubrics and are not part of the 1962
formulary.

## Other text-bearing parts of this Mass

These are fixed or rubrically appointed texts of the 1962 *Ordo Missae*,
*Praefationes* and appendix, not proper text. The study refers to them and does
not reproduce the Ordinary. RGMR 474-475, 507-510 and RG 127 were located on
the text layer; RGMR 483 and 494 were read on the page image (PDF 32). The
*Ordo Missae* numbers below are those of the registered passage records
`…vatican-typica-1962.ordo-missae-ad-gradum`, `…ordo-missae-kyrie-gloria`,
`…ordo-missae-credo`, `…ordo-missae-conclusio`, `…praefationes` and
`…ordo-ad-aspergendam-aquam-benedictam`; the Trinity Preface (no. 1082, PDF
374) and the last Gospel (no. 1139, PDF 408) were located on the text layer
and were not re-read on images in this stage.

| Place | Text and appointment | Status and source |
|---|---|---|
| Before the principal Mass, where used | *Asperges me* with the Sunday blessing of water, appendix | A Sunday rite outside the Mass and outside this formulary; not part of the appointed inventory. |
| Prayers at the foot of the altar | Ps 42 *Iudica me* through *Oramus te*; *Ordo Missae* nos. 1013-1023 | Said: RGMR 425 (p. XXXI, read) omits *Iudica* only from Passion Sunday to Maundy Thursday and in Requiem Masses. |
| Introit doxology; Kyrie | *Gloria Patri*; ninefold Kyrie, *Ordo Missae* no. 1024 | RGMR 427-428, 430 (p. XXXI, read); the Introit's printed *V. Gloria Patri* cue at no. 1699. |
| After the Kyrie | *Gloria in excelsis*, *Ordo Missae* no. 1025 | Said. RGMR 431 a (p. XXXI, read) ties it to the Office's Te Deum at Matins, a Breviary rubric this Missal omits. The ICRSP dated entry carries the Gloria for this date; it is an unadopted lead. No chant setting is chosen. |
| Before and after the Gospel | *Munda cor meum*, Gospel dialogue; homily | RGMR 471, 474; *Ordo Missae* nos. 1026-1028. |
| After the Gospel or homily | *Credo* | Said: RGMR 475 a, *in qualibet dominica*; printed cue after no. 1704; text *Ordo Missae* no. 1029. |
| After the Secrets | *Praefatio de Ss.ma Trinitate* | Appointed, not chosen: printed direction after no. 1706 and RGMR 494 b, *tamquam de Tempore … in omnibus dominicis II classis, extra tempus natalicium et paschale* (p. XXXIV, PDF 32, read); RGMR 483 excludes the commemorated feast's Preface. Text at printed p. 293, no. 1082. |
| Canon | *Te igitur* through the doxology | The one Roman Canon, said secretly (RGMR 500, read). No alternative Eucharistic Prayer and no proper insertion for this day (RGMR 501, read). |
| Conclusion | *Ite, missa est*, *Placeat*, blessing, last Gospel Jn 1:1-14 | RGMR 507-509: *Ite, missa est*, since no procession is supplied; the last Gospel *in quavis Missa* is the initium of John, and none of the omission cases of 510 applies. *Ordo Missae* nos. 1132, 1137, 1138, 1139. |

## Lawful study-text routes

- **Latin, all ten proper elements.** Control: the 1962 page images above.
  Publication basis: 17 U.S.C. 103(b) with a public-domain antecedent, as
  settled for the repository in
  `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`.
  The antecedent is the Pustet Ratisbon 1862 printing
  (`edition.catholic-church.missale-romanum.pustet-ratisbon-1862`), which
  prints the whole formulary at printed pp. 354-355 under *Dominica XXI. post
  Pentecosten*. Two witnesses to those pages were read here:
  - the tracked public-domain text layer
    `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`
    (SHA-256 `f34bc7cf9293…` recomputed and matched), at physical lines
    52146-52334: heading 52146-52148, Introit 52150-52165, Collect
    52167-52175, Epistle 52184-52211, Gradual 52213-52220, Alleluia
    52221-52224, Gospel 52226-52289 (page 355 from 52238), Offertory
    52292-52303, Secret 52305-52311, Communion 52317-52323, Postcommunion
    52325-52330, with the 1862's own pre-1960 extra orations at 52177-52179,
    52313-52315 and 52332-52334; and
  - the registered complete scan
    `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.ia-facsimile-pdf-363d6fc3`,
    fetched in this stage from its `source_url` to the registered SHA-256
    `363d6fc3f556bf596f3b56d4efcb7be849b7e9904304ba886b7977c39e8f7474` and
    102,880,787 bytes; PDF pp. 440-441 (printed pp. 354-355) were rendered at
    150 dpi and read. Printed p. 354 is also the third page of the tracked
    extraction `…pustet-ratisbon-1862.pentecost-20-pages-352-354`, which was
    not separately reopened. No extraction covers p. 355.

  On the page images every element of this formulary agrees with the 1962 in
  its words, including each divergence from the Clementine listed above: the
  1862 already reads the Introit *In voluntate tua … Dominus universorum tu
  es*, *Fratres.* without *De cetero*, *a generatione et progenie*, the
  liturgical Gospel opening *Dixit Jesus discipulis suis parabolam hanc*,
  *suffocabat*, the Offertory narrative and the Communion *In salutari tuo …
  Domine Deus meus*. The differences seen are of orthography (*justitiae*,
  *extinguere*, *Jesus*, *ejus*, *millia*, *coelestis*, *obedire* and the like),
  pointing, citation form (*Esth. 13.*, *Ps. 118.*, *cap. 6*, *Ps. 89.*,
  *Ps. 113.*, *c. 18.*, *Job 1.* without verse numbers) and conclusion length.
  The text layer misreads the Gospel citation as *c. 28*; the page reads *c.
  18*. This was a reading, not a word-for-word collation at full resolution.
  Four of the ten elements already carry collated `publication_status =
  "permitted"` rows in
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` —
  Collect, Offertory, Secret and Postcommunion — each verified against
  `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-pentecost-21-orations`
  and cited to the 1862 text layer through
  `passage.catholic-church.missale-romanum.pustet-ratisbon-1862.pentecost-21-orations`.
  The Introit and the five scriptural elements (Epistle, Gradual, Alleluia,
  Gospel, Communion) have no ledger row and need one, or an equivalent recorded
  basis, before their Latin is published.
- **Latin, St Luke's commemorated orations.** The ledger carries `permitted`
  rows for all three (`mass = "s-lucae-evangelistae"`), verified against
  `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-s-lucae-evangelistae-orations`
  and publishing on the 1922 Tours Mame at printed pp. 738, 726 and 739, with
  the 1862 text layer as corroboration. The 1862's own St Luke formulary, *Die
  xviii. S. Lucae, Evangelistae*, printed pp. 560-561 (scan PDF pp. 646-647,
  read at display resolution; text-layer lines 76658-76680, 76756-76763 and
  76771-76779), prints all three orations in the 1962's words apart from
  orthography and pointing, with *Praefatio de Apostolis* after the Secret.
- **Latin, the *Pro Fidei propagatione* orations.** The ledger carries no row
  for nos. 1806-1808 or 4833, 4841, 4843. A public-domain witness to their
  wording exists in the library: the 1889 Tournai Desclée Missal's tracked
  public-domain text layer
  `artifact.catholic-church.missale-romanum.1889-tournai-desclee-leo-xiii-recognitum.ia-djvu-ocr-715f57fd`
  (SHA-256 `715f57fd58ab…` recomputed and matched) prints *Missa votiva pro
  Fidei propagatione*, introduced as said *ad normam Decreti S. Congregationis
  de Propaganda Fide, de die 21. Augusti 1841*, with the Collect *Deus, qui
  omnes homines vis salvos fieri* at physical lines 100882-100892, the Secret
  *Protector noster adspice Deus* at 101004-101014 and the Postcommunion
  *Redemptionis nostrae munere vegetati* at 101026-101030, in words that on
  the text layer agree with the 1962 apart from orthography and pointing
  (*adspice*, *eumdem*). That was read on the text layer only; no page image
  of the 1889 was read.
- **English, canonical Scripture.** The Douay-Rheims (Challoner) as registered
  (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  with `…american-1899-ebible` as the other registered Douay printing), read
  at the Vulgate loci through `tools/tpt mass-propers show … --bible
  douay-rheims`, which resolves the Missal's Vulgate psalm numbering. Its
  canonical verses are **not** the Missal's wording at the Introit (the Douay
  at Esth 13:9-11 gives *for all things are in thy power … Thou art Lord of
  all, and there is none that can resist thy majesty*), the Epistle's
  liturgical address (Douay *Finally, brethren*), the Gradual (Douay *from
  generation to generation*), the Gospel's opening, the Offertory narrative
  (Job 1:1, 1:12, 2:6-7 in the Douay are other sentences) and the Communion
  (Douay *My soul hath fainted after thy salvation … do thou help me*). English
  must never be composed to fill those differences; where the Douay cannot
  carry the Missal's form the profile's rule is to say so and give the Latin
  with a description.
- **English, the Sunday's orations.** The 1861 Cummiskey hand missal
  (`edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861`),
  under *XXI. SUNDAY after PENTECOST*, printed pp. 450-452, through
  `passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.post-pentecosten-21`
  over the tracked payload `…philadelphia-1861.temporal-orations-en`
  (physical lines 173-175; states through `inspected`). The registered scan
  `…philadelphia-1861.ia-scan-pdf` was fetched in this stage, matched its
  registered SHA-256
  `85034c90d5cbfe891f4359fb2faff907d217dbd11a30458b55e4c48eae028898`, and its
  PDF pp. 459-461 (printed pp. 450-452) were read at 300 dpi: the Collect
  (*Familiam.—Preserve thy family*), Secret (*Mercifully receive*) and
  Postcommunion (*Immortalitatis.—Having received the food of immortality*)
  stand there in the payload's wording. The same pages print the 1861 book's
  own English for the whole Mass, including the Introit (*All things, O Lord,
  are in thy power*), the Offertory narrative (*There was a man whose name was
  Job … and Satan asked to tempt him*) and the Communion (*My soul hath looked
  to be saved by thee … help me, O Lord my God*), which no registered passage
  covers; that English is the 1861 book's own and is not the profile's route
  for the scriptural elements. The finding-aid overlay
  `src/sources/inventories/roman-1962-proper-translations-v1.toml` is a shared
  record belonging to its own owner and is unchanged here.
- **English, St Luke's orations.** The same 1861 book prints them under
  *XVIII. St. LUKE the Evangelist*, printed pp. 677-678, carried by the
  tracked transcription `…philadelphia-1861.s-lucae-checked-english`
  (SHA-256 `932cb5278b1d…` recomputed and matched), which its record calls
  model-assisted and checked against the page images. No passage record
  addresses it. Its PDF pp. 686-687 were read in this stage at 300 dpi: the
  three prayers stand there in the payload's wording. The 1861 renders the
  Secret's *Domine* as *O Almighty God* and the Postcommunion's *per quod tuti
  esse possimus* as *and preserve us from all danger*; that is the book's own
  English.
- **English, the *Pro Fidei propagatione* orations.** The Lasance *New Roman
  Missal*, Benziger revision of 1945
  (`edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945`),
  prints them in its *Mass for Propagation of Faith*, printed pp. 1453, 1456
  and 1457, carried by the tracked
  `…benziger-revised-1945.pro-fidei-propagatione-checked-orations` payload
  (SHA-256 `3791f8b0f8c9…` recomputed and matched), whose rights basis is the
  nonrenewal recorded in the Lasance rights inventory. No passage record
  addresses it. The registered scan
  `…benziger-revised-1945.internet-archive-facsimile-pdf-6cf3c3d0` was fetched
  in this stage, matched its registered SHA-256
  `6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70` and
  75,268,976 bytes, and PDF pp. 1474, 1477 and 1478 were read at 250 dpi: the
  three prayers, Latin and English, stand there in the payload's wording.
- **Trinity Preface.** Appointed by rubric and its Latin located (p. 293,
  no. 1082), within the registered `…vatican-typica-1962.praefationes`
  passage. Whether the study quotes or only cites the Preface is for research.

No source was registered or retained in this stage. The existing library was
read first and sufficed for resolution; everything fetched was either an
already registered artifact fetched to its registered hash or a live Ordo
response whose identity and hash are written down above. No liturgical owner is
imported: the formulary, the commemorated orations and the added orations are
local to this leaf's own family and are referenced in the Missal itself, so
there is no shared-formulary Makefile dependency to declare.

Observations about shared records are reported rather than repaired, because
this stage owns no source or tool record:

- `tools/tpt calendar-rubrics` and `src/sources/calendars/roman-1962/rubrics.yaml`
  carry no rule for RGMR 453, so the computed oration lists for the
  penultimate Sunday of October omit the oration *pro Fidei propagatione*,
  which the Missal requires in every Mass.
- The ledger's St Luke rows publish on 1922 Mame pages whose own evidence
  notes report token alignments at other formularies (the Secret row records
  the day's-saint slot reading as a different saint), while the 1862's own St
  Luke formulary at printed pp. 560-561 carries all three orations and is
  cited only as corroboration.
- No passage record addresses the Cummiskey St Luke or the Lasance *Pro Fidei
  propagatione* payloads.

## Remaining verification for research

- Collate every proper element word for word at 200 and 400 dpi against the
  1962 page images and against the 1862 pages at full resolution; write
  `propers/retrieved.txt` and `propers/verified.md` with the loci,
  conclusions and orthographic transformations. Collate St Luke's three
  orations (pp. 689-690) and the three *Pro Fidei propagatione* orations
  (p. 427) in the same way if the study prints them.
- Identify, or record the negative result for, the textual source of the
  Introit (its relation to Esth 13:9-11 and to Mardochai's prayer in its Greek
  and Old Latin forms), the Gradual's *a generatione et progenie*, the
  Gospel's *suffocabat*, the Offertory's narrative cento and its loci, and the
  Communion's *In salutari tuo … speravi … iniqui … Domine Deus meus*. Nothing
  above asserts an origin for any of them.
- Establish or record a publication basis for the Latin of the Introit and the
  five scriptural elements without ledger rows, and for the three *Pro Fidei
  propagatione* orations (the 1889 Desclée text layer above, read on a page
  image, or another public-domain witness); verify on a page image the 1862's
  St Luke orations if the study prints them; decide the English display for
  the places where the Douay cannot carry the Missal's form, including whether
  the 1861 book's own Introit, Offertory and Communion English is used under
  its own attribution or the Latin is given with a description.
- Decide, with the authoring stages, how the studies present the day's added
  orations: the *Pro Fidei propagatione* oration belongs to every Mass on this
  date unless the Ordinary moved it, and St Luke's commemoration to low and
  conventual Masses only; neither belongs to the formulary, and neither adds
  Scripture. Settle the form of the joint conclusion if it is described.
- Read each appointed passage in its complete biblical context — Mardochai's
  prayer, Esth 13:8-18 (Clementine numbering), and Esther's story around it,
  for the Introit; Eph 6:10-20 within the letter's close; Ps 89 whole; Ps 113:1
  with the Exodus it recalls; Mt 18:21-35 with Peter's question on forgiveness
  that the liturgical opening omits; Job 1-2 for the Offertory; Ps 118:81-88
  for the Communion — run the reception sweep, and generate
  `research/chronology.toml` and `research/chronology-annotations.tex` with
  `tools/tpt proper-chronology`. No biblical date is asserted in this record.
  `tools/tpt proper-chronology loci` already resolves every appointed locus
  under the default profile `catholic-comprehensive-v1`: Introit (Esth 13:9,
  13:10, 13:11, Ps 118:1) `composition-only`; Epistle `composition-only`;
  Gradual `composition-only`; Alleluia (Ps 113:1) `dated`; Gospel
  `composition-only`; Offertory (Job 1:1, 1:12, 2:6, 2:7) `composition-only`;
  Communion (Ps 118:81, 84, 86) `composition-only`. The distinct directly
  appointed passages as printed, in canonical then verse order, are Esth
  13:9-11, Job 1 (resolved as 1:1, 1:12, 2:6-7), Ps 89:1-2, Ps 113:1, Ps
  118:1, Ps 118:81, 84, 86, Mt 18:23-35 and Eph 6:10-17; each is appointed
  once. Whether the Offertory's printed *Iob 1* or the verses carrying its
  sense are the right chronology inputs is for research to settle before
  generation.
- Register a dated edition and passage for 18 October 2026 if the study relies
  on either dated Ordo.
- Resolve, only if the study relies on them, the points this stage did not
  settle: the Breviary's Te Deum rubric behind the Gloria, the Asperges
  placement, the order of the II-class votive Mass *Pro Fidei propagatione*,
  and any particular-calendar overlay, local mission day or local external
  solemnity. None is needed for the universal formulary on this date.
- Bind the controlling sources in `research/source-bindings.toml` and declare
  the external owners actually relied on in `research/review-dependencies.toml`.
  The authorities adopted here are the 1962 facsimile artifact with its
  `temporal-pentecost-21-orations` and
  `temporal-s-lucae-evangelistae-orations` passages, the facsimile-rights
  inventory, the Latin provenance ledger, the 1862 Pustet text artifact, its
  `pentecost-21-orations` passage and its registered scan, the 1889 Desclée
  text artifact, the Douay-Rheims editions and the psalm-numbering
  concordance, the Clementine Vulgate edition, the Cummiskey passage and
  payloads named above with their registered scan, the Lasance *Pro Fidei
  propagatione* payload with its registered scan and the Lasance rights
  inventory, and, as computation inputs,
  `src/sources/calendars/roman-1962/propers.yaml` and `rubrics.yaml`.
