# Celebration context and complete appointed inventory

Resolved 26 October 2026 for the `proper-study` v15 production of the Claude
1962 leaf, run `427e2f58bb897a16`, seeded at commit
`c7dfb84c76a057079251e8c918243b787fa69494`. The production-plan entry of
2026-10-26 in `guidance/liturgy/propers-production-plan.md` authorizes provider
`claude` for this one identity and Sunday 1 November 2026, as an independent
production that is not a companion to or derivative of the published GPT leaf
for the same identity. The same entry states that it does not open the
commemorated Twenty-third Sunday after Pentecost. That Sunday enters this
record only as the commemoration the rubrics require inside this Mass: its
three orations are inventoried below, and nothing else of its formulary.

**Publication mode: full sourced material.** The same plan's *Reference-only
publication scope* says that no reference-only target is currently authorized,
so this leaf is not reference-only and `appointed_text_completeness` is not
`reference-only`.

`ARGS.research_handoff` is `none`, so no handoff was supplied. The GPT leaf
for this identity, its PDF and web edition, the GPT review record for its
production, every postconciliar record and every postconciliar calendar row
are outside this record's evidence; none was opened and nothing below is taken
from them. The Claude F01 context record was read only as a model of the
record's shape, and no finding of it is relied on. This record settles what is
studied. It holds no study prose, spoken text, timing claim or review verdict.
The research stage collates the sources and may correct it from evidence.

## Identity, governing books and territory

- Canonical identity:
  `liturgy/roman-rite/1962/propers/temporal/f02-all-saints`, catalog ID `F02`
  in `guidance/liturgy/roman-1962-propers.md`. That profile keeps the `F`
  series for a general-calendar feast that can occupy a Sunday without a
  temporal ordinal, and names `F02` as All Saints, the Missal's *In Festo
  Omnium Sanctorum*, I classis, printed pp. 702-703 (CMAA facsimile artifact
  pp. 783-784). It also says the fixed-date feast keeps this identity in every
  year and that the dated study records the Sunday commemoration the
  governing rubrics require. Calendar family `roman-1962`.
  `tools/check-proper-identity --document liturgy/roman-rite/1962/propers/temporal/f02-all-saints`
  passes ("Identity f02 is registered in the roman-1962 calendar"). The finding-aid mass index
  `src/sources/calendars/roman-1962/propers.yaml` carries the formulary as
  `omnium-sanctorum`, `registry: 'F02'`, `date: 11-01`, rank `I`, kind
  `sanctoral`. It is a lead and never the source of record for any wording
  (see *Shared records* below).
- Governing edition: *Missale Romanum*, editio typica, Typis Polyglottis
  Vaticanis 1962 (`edition.catholic-church.missale-romanum.vatican-typica-1962`),
  controlled on the page images of
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.
  Before any page was read, the copy used in this stage matched the registered
  SHA-256 `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a`
  and 82,815,941 bytes. The formulary was read on page images at 200 dpi and
  again at 400 dpi (artifact pp. 783-784, both columns). Also read on page
  images at 200 dpi: the neighbouring pages 782 and 785, the commemorated
  Sunday's pages (artifact pp. 497-498), the Trinity Preface (artifact p. 374),
  the *Calendarium* for November (artifact p. 54), the general rubrics at
  artifact pp. 15-16, 29-30 and 32-33, and the Vigil of the Nativity at
  artifact p. 97. The text layer was used only to find pages. Loci marked
  "located" were found on it and not re-read on an image.
- Printed place, heading and rank. The Missal prints the feast in the
  **Sanctorale**. Printed p. 701 (PDF 782), headed *Festa octobris (28)*, ends
  the formulary of Ss Simon and Jude with its Postcommunion *Perceptis, Domine,
  sacramentis* at no. 3972 and its votive Tract at no. 3973. Printed p. 702
  (PDF 783) has the running head *FESTA NOVEMBRIS*, then *Die 1 novembris* /
  *IN FESTO OMNIUM SANCTORUM* / *I classis*. Printed p. 703 (PDF 784) is
  headed *Festa novembris (1)*. Printed p. 704 (PDF 785), headed *Missa
  votiva de omnibus Sanctis*, opens a separate votive formulary at no. 3984;
  it is not this feast and contributes nothing here (its own rubric *Epistola
  ut in festo 702* and *Evangelium ut in festo 703* only point back to this
  formulary). The feast therefore runs from marginal no. 3974 to no. 3983 and
  is whole and legible on two pages.
- *Calendarium*, November, printed p. LII (PDF 54, read): *d · Kal. · 1 ·
  OMNIUM SANCTORUM, I classis.*; 2 November *IN COMMEMORATIONE OMNIUM FIDELIUM
  DEFUNCTORUM, I classis.*
- Governing books within that edition, read or located where cited below: the
  *Calendarium*; the *Rubricae generales* (cited RG); the *Rubricae generales
  Missalis romani* (cited RGMR); the *Ordo Missae*; the *Praefationes*; the
  Proper of Time (for the commemorated Sunday's orations only); the
  Sanctorale.
- Territory: the universal 1962 General Roman Calendar. No diocese, church
  titular or dedication, religious institute or other particular calendar was
  supplied, so no local overlay is applied or computed.
- Language: Latin governs. Every English route below is a historical study aid,
  not an approved vernacular liturgical text.
- Cycle: the 1962 Missal appoints the readings with the formulary and has no
  Lectionary cycle. No A/B/C or I/II value exists for this record. The
  requested identity and the formulary appointed on the requested date are the
  same, so there is no requested-versus-appointed difference to preserve.
- Season: *tempus « per annum »* after Pentecost (finding-aid season
  `after-pentecost`). The feast's colour is white (below). The commemorated
  Sunday's colour, green, is not used.
- Homily audience for the later homily stage: adult parish assembly
  (`ARGS.audience`). RGMR 474 (printed p. XXXIII, PDF 31, located) places a
  brief homily after the Gospel, *praesertim in dominicis et diebus festis de
  praecepto*. The homily is authored preaching and adds no text to this
  inventory.

## Occurrence on 1 November 2026

**The date.** 1 January 2026 is a Thursday, so the year's dominical letter is
D. The *Calendarium* gives 1 November the letter *d* (read), so 1 November
2026 is a Sunday. `tools/tpt calendar-days day --calendar roman-1962 --date
2026-11-01 --json` (finding aid only) returns two candidates and nothing
unresolved: `pentecost-23` ("slot 23 of 26 Sundays after Pentecost") and
`omnium-sanctorum` (fixed date, rank I). Pentecost 2026 fell on 24 May, so
1 November is the Twenty-third Sunday after Pentecost. The Sunday is not
displaced to another day: RG 14 (located) says *Officium et Missa dominicae
impeditae nec anticipantur nec resumuntur*.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
roman-1962 --date 2026-11-01 --json` is settled. The winner is
`omnium-sanctorum`, cited as RG 39 and RG 91 row 11 (RG 39 is located through
the tool and was not read). `pentecost-23` is commemorated as a privileged
commemoration (RG 109 a) "made in every Mass". The low-Mass and sung
non-conventual oration lists each have the feast's Collect followed by a second
collect of the Sunday under a second conclusion (RGMR 436-437, 480-481, 505).
`sungDiffers` is false. Every rubric this rests on was read on page images:

- RG 91, table of precedence, printed p. XVII (PDF 15): row 11, *Festa I
  classis Ecclesiae universae superius non nominata*, among the first-class
  days; row 15, *Dominicae II classis*, among the second-class days. RG 16
  (printed p. XII, located): *Dominica II classis, in occurrentia, festis II
  classis praefertur*. A first-class feast therefore outranks the Sunday. RG
  16 a, the clause on feasts of the Lord taking the Sunday's place without a
  commemoration, does not apply, because All Saints is not a feast of the Lord.
  For the same reason RG 112 b (no commemoration of a Sunday in a Mass of a
  feast of the Lord) does not apply.
- RG 107-109 (printed p. XVIII, PDF 16): RG 108, *Commemorationes privilegiatae
  fiunt in Laudibus et in Vesperis necnon in omnibus Missis*; RG 109, privileged
  commemorations are *a) de dominica* and the other listed kinds. RG 111 a
  (same page): *in diebus liturgicis I classis et in Missis in cantu non
  conventualibus, nulla admittitur commemoratio, praeter unam privilegiatam*.
- RGMR 434 a (printed p. XXXI, PDF 29): *in diebus liturgicis I classis …
  nulla alia admittitur oratio, praeter orationem sub unica conclusione
  dicendam et unam commemorationem privilegiatam, salvo praescripto n. 333*
  (n. 333 not read). RGMR 436-437 (same page): the Mass's own oration is said
  under its own conclusion, and *Sub altera conclusione semper dicuntur: a)
  commemorationes faciendae*.

The result is one branch for the orations. In every Mass of the day, low or
sung, conventual or not, the feast's Collect, Secret and Postcommunion are said,
and each is followed by the matching oration of the Twenty-third Sunday under
its own conclusion. No Scripture, chant or Preface of that Sunday is said.

**Additions that are excluded, and those that remain local facts** (RGMR,
printed p. XXXII, PDF 30, read, unless stated):

- RGMR 444 admits an oration *sub unica conclusione* only for a ritual oration
  (RGMR 447), the oration of an impeded votive Mass of I or II class, or one
  the rubrics expressly name (RGMR 110, 355, 449, 451, 453).
- RGMR 449 (the Pope's coronation and its anniversary; the anniversary of the
  diocesan bishop's election, consecration or translation) and RGMR 451 (*pro
  seipso sacerdote*, on the anniversary of the priest's own ordination) exclude
  only the days of rows 1, 2, 3 and 8. This day is row 11, so it is **not**
  excluded. Neither the papal coronation anniversary nor any universal
  appointment falls on this date. A diocesan bishop's anniversary or a
  celebrant's ordination anniversary on 1 November would be a local or personal
  fact. Such a fact is not computed here and adds nothing to the universal
  inventory. One dated web Ordo (ICRSP, below; registered as context
  only) marks *✕ Or. pro Papa*; that agrees with the computation but is not
  evidence the studies may cite.
- RGMR 453, the oration *pro Fidei propagatione*, belongs to the penultimate
  Sunday of October (in 2026, 18 October) or another day the Ordinary sets. It
  is not appointed on this date.
- RGMR 457 d forbids the *oratio imperata* on all I- and II-class days. RGMR
  461 (located) admits the *oratio votiva ad libitum* only on IV-class days.
- Ritual orations (RGMR 447-448), the nuptial oration and the other
  ceremony-bound additions are local facts and are not computed.

**No substitute Mass on this date.** RGMR 328 (printed p. XXIV, PDF 22,
located) permits a first-class votive Mass on every day except those of rows
1-8. A row-11 day is therefore not closed to the first-class votive Masses
listed in RGMR 329: the Dedication in the act of consecration, the sung Mass of
a Eucharistic Congress, and an extraordinary sung celebration under RGMR 340 a.
Any of these would be a local fact, is not computed, and is not the object of
study. RGMR 341 (located) allows second-class votive Masses only on days of II,
III and IV class. RGMR 361 (located) prohibits indulted external solemnities on
I-class days. The *Missa votiva de omnibus Sanctis* (printed p. 704) is a
votive formulary for other days and is excluded. Masses of the dead are not
considered.

**Colour, Gloria and Credo** (read unless stated). White: RG 120 d (printed p.
XIX, PDF 17, located), *Omnium Sanctorum (1 novembris)*. Gloria: RGMR 431 a-b
(p. XXXI, PDF 29), the Mass answering to an Office with the *Te Deum*, and the
festive Mass. Credo: RGMR 475 a and b (p. XXXIII, PDF 31, located), *in
qualibet dominica, etsi eius Officium alicui festo locum cedat*, and *in festis
I classis*. The printed cue *Credo.* follows the Gospel.

**Preface: disputed, not settled here.** The formulary prints no Preface
direction after its Secret (read, p. 703). The Missal's rules (printed p.
XXXIV, PDF 32, read) are as follows. RGMR 482: *Praefatio dicitur quae cuique
Missae propria est; qua deficiente, dicitur praefatio de Tempore, secus
communis*. RGMR 483: *Nulla commemoratio, in Missa occurrens, praefationem
propriam inducit*. RGMR 494: the Trinity Preface is said *b) tamquam de
Tempore in dominicis Adventus, et in omnibus dominicis II classis, extra
tempus natalicium et paschale*. RGMR 498: the common Preface is said *in
Missis quae praefatione propria carent, nec sumere debent praefationem de
Tempore*. The question is whether the Sunday's Preface *de Tempore* reaches a
first-class feast that has no proper Preface and is said on a II-class Sunday.
The two readings are:

1. **Trinity Preface, n. 1082** (printed p. 293, PDF 374, read): the day is a
   II-class Sunday after Pentecost, the feast lacks a proper Preface, and the
   Preface *de Tempore* therefore comes before the common one under RGMR 482.
   RGMR 483 forbids only a *proper* Preface induced by a commemoration, not the
   seasonal one. On the analogous case, the Missal prints after the Secret of
   the Vigil of the Nativity (printed p. 16, PDF 97, read): *Praefatio
   communis; sed, si venerit in dominica, dicitur de Ss.ma Trinitate.*
2. **Common Preface, n. 1086** (printed p. 297, PDF 378, located): RGMR 494 b
   reaches the Mass of the Sunday and not a feast said on one. This is the
   reading the repository's own test asserts (see *Shared records*).

The Vigil direction is a particular rubric for one formulary and could be
taken either as an instance of the general rule or as an exception to it, so
it does not settle the case alone. This context stage asked research to
settle the question from an official 1962-horizon Ordo or authentic
commentary, or to record that it stays open. Research has recorded it as
open: no registered source settles it (research/scope.md section 11, which
names the sources searched and gives authoring one fixed rule for the slot).
The inventory lists both Prefaces as the single disputed Preface slot, and
neither is chosen. The ICRSP Mass-text page (registered as context only,
below) adds a French particular usage (*In Galliis, in aliquibus diœcesibus :
præfatio de Sanctis*). That is a particular-calendar concession, outside the universal
territory, and is not imported.

**Last Gospel.** RGMR 509 (printed p. XXXV, PDF 33, read): *Pro ultimo
Evangelio, in quavis Missa, regulariter sumitur initium Evangelii secundum
Ioannem*. The only exception is Palm Sunday in Masses not following the
blessing and procession. None of the omission cases of RGMR 510 applies. The
last Gospel is therefore Jn 1:1-14. The ICRSP Ordo response (below,
registered as context only) has the line *Dernier Évangile du XXIIIe
dimanche*, which conflicts
with the plain text of RGMR 509. The page read here gives no basis for a
proper last Gospel of a commemorated Sunday in the 1962 books. Research
confirmed RGMR 509-510 on the page image and withdrew the ICRSP line from
the evidence: it is context only, not a variance the studies present or
cite.

**Dated witnesses: registered context, not evidence.** Five live sources
with liturgical content (six responses) were read for this date on
2026-10-26. Research (iteration 2) withdrew every reliance on them; the
Preface question and the last Gospel are stated from the registered RGMR and
Missal loci alone. The source-registration stage (iteration 2) then
registered each response as a dated restricted edition, artifact and passage,
with no bytes retained, and bound it as context in
research/source-bindings.toml (bindings 35-40), so that what was read has a
durable identity. Registration does not make them evidence: none is evidence
the studies may cite. They are witnesses of current usage under the 1962
books. None is the competent Ordo of a named territory, because none was
supplied.

- ICRSP France, *Ordo*, <https://icrspfrance.fr/ordo.php?d=2026-11-01>,
  response 111,933 bytes, SHA-256
  `af2285ece0d18823047773931938143d3461fb9fbbbdef179e7d7f5b0795792d`
  (`passage.icrsp-france.ordo.web-2026-10-26.2026-11-01`, binding 35):
  *dimanche 1 novembre 2026* — *Fête de tous les Saints, « Toussaint »*, *Ire
  classe*, white; *✓ Gloria ✓ Credo ✕ Or. pro Papa*; *Préface: de la T. Ste
  Trinité*; *Messe propre (Gaudeamus): Gloria. Mém. du XXIIIe Dim. après la
  Pentecôte. Credo. Préf. de la T. Ste Trinité. Dernier Évangile du XXIIIe
  dimanche.*; Vespers of the feast with the Sunday commemorated; Requiem Masses
  forbidden. The same day's Mass-text page,
  <https://icrspfrance.fr/textes-de-la-messe.php?d=2026-11-01>, 253,820 bytes,
  SHA-256 `fe5c66edac1959517e86bef714285b02c619a6168501437a56f18e094e7c59b2`
  (`passage.icrsp-france.textes-de-la-messe.web-2026-10-26.2026-11-01`,
  binding 36), repeats the summary, prints the commemoration's orations under
  *Mémoire de 23e Dim. après la Pentecôte*, and prints the French particular
  Preface note above.
- FSSP France, *Ordo du mois*, <https://www.fssp.fr/ordo-du-mois/>, response
  165,239 bytes, SHA-256
  `c0724ef596b1a3dab7c9d94c53514f102a16129a08d39d4e1e2d6aa4cc4f22a2`
  (`passage.fssp-france.ordo-du-mois.web-2026-10-26.2026-11-01`, binding
  37): *Dimanche 1 novembre Toussaint (1ère classe, Blanc)*. It gives one line
  per day, and its silence on commemorations and the Preface is not read as
  evidence.
- *Ordo* of the Society of St Pius X, <https://ordo.fsspx.org/day/2026-11-01>,
  page 186,674 bytes, SHA-256
  `81bb64383af0b5a453b4f619061f107e8b3a0a9f64e7f07a8dae8240ccdc4132`
  (`passage.fsspx.ordo.web-2026-10-26.2026-11-01-day-page`, binding 38),
  and its data endpoint
  <https://ordo.fsspx.org/api/v1/calendar/2026/11/1/texts>, 11,425 bytes,
  SHA-256 `5404783db2625d3f59dbc4281080d7c6f954549803df227a51b714e8898d221f`
  (`passage.fsspx.ordo.web-2026-10-26.2026-11-01-texts`, binding 39). Both
  are in French. They give: celebration *Toussaint*, rank 1, *albus*; one
  commemoration, *23e Dimanche après la Pentecôte*, rank 2. The endpoint
  prints the Mass texts in French translation; under the Collect, Secret and
  Postcommunion the feast's prayer is followed by the Sunday's, headed
  *Mémoire du 23e Dimanche après la Pentecôte*, each with its own conclusion.
  The day is marked as of precept (*Fête d’obligation*). No Preface is named
  in the parts read. Its canonical standing is not that of an approved
  institute, so it is evidence of usage only.
- Missale Meum, <https://www.missalemeum.com/en/calendar/2026-11-01>, 116,457
  bytes, SHA-256
  `d93d2d63a46621236362bcc791e24516d1bd968163f2bf9782897407ac3c087f`
  (`passage.missale-meum.calendar.web-2026-10-26.2026-11-01`, binding 40):
  *All Saints*, *XXIII Sunday after Pentecost*, *1st class*, white; it prints
  the Trinity Preface and no orations of the commemorated Sunday. It is a
  private aggregator, a lead only.
- The Divinum Officium request for the same date returned a 5,492-byte
  access-block page from the site's network provider, with no liturgical
  content. An earlier version of this note described a heading for it; the
  retained bytes carry none. Nothing from Divinum Officium was read, and it
  is not registered.

Computation and the printed calendar and rubrics establish the following
points by themselves: the identity, the first class, the white colour, the
Gloria and Credo, the commemoration of the Twenty-third Sunday in the
orations, and the absence of any other added oration. The witnesses above
agree with them and add nothing the studies rely on. Nothing fails closed. The
Preface remains disputed as stated above. The ICRSP's last-Gospel line is not
imported.

## Appointed proper

Loci are the printed page and marginal number of the controlling edition, read
on 200- and 400-dpi page images of artifact pp. 783-784 (printed pp. 702-703).
The commemoration's orations were read on 200-dpi images of artifact pp.
497-498 (printed pp. 416-417). Psalms are cited in the Missal's Vulgate
numbering, with the Hebrew and English numbers in parentheses, taken from the
repository concordance
`artifact.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581.psalm-numbering-ee3c7757`
(`psalm-numbering.tsv`). Vulgate Ps 32 equals Hebrew and English Ps 33 with the
same verse numbers. Vulgate Ps 33:1 is the inscription, so Vulgate 33:10-11
equals Hebrew 34:10-11 and English 34:9-10. "Said" means said in the Mass of
1 November 2026.

| Order and key | Element and printed locus | Liturgical place, extent and status |
|---|---|---|
| 1 `introit` | *Antiphona ad Introitum*, verse *Ps. 32, 1* (Heb./Eng. 33:1); p. 702 left column, no. 3974 | Said. Antiphon *Gaudeamus omnes in Domino, diem festum celebrantes sub honore Sanctorum omnium: de quorum solemnitate gaudent Angeli, et collaudant Filium Dei.* It is uncited, an ecclesiastical composition rather than a Bible verse. Psalm verse *Exsultate, iusti, in Domino: rectos decet collaudatio.*; printed cue *V. Gloria Patri.*; the antiphon is repeated (RGMR 427, read). No Alleluia outside paschal time (RGMR 429, read). |
| 2 `collect` | *Oratio* *Omnipotens sempiterne Deus, qui nos omnium Sanctorum tuorum merita sub una tribuisti celebritate venerari*; p. 702 left column, no. 3975 | Said, first. Printed conclusion *Per Dominum.*, a cue for the full conclusion. |
| 3 `commemoration-collect` | *Oratio* of the *Dominica XXIII post Pentecosten*, *Absolve, quaesumus, Domine, tuorum delicta populorum*; p. 416 right column, no. 1720 (PDF 497) | Said after the Collect, under its own second conclusion, printed in full: *Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.* Required by RG 108-109 a, 111 a and RGMR 434 a, 437 a. It is not an option. |
| 4 `lesson` | *Lectio libri Apocalypsis beati Ioannis Apostoli*, Apoc 7:2-12; p. 702 right column - p. 703 left column, no. 3976 | Said in the place of the Epistle. The liturgical incipit *In diebus illis: Ecce ego Ioannes vidi alterum Angelum ascendentem ab ortu solis* replaces the Clementine opening *Et vidi alterum angelum* (7:2). It ends *Deo nostro in saecula saeculorum. Amen.* (7:12). No shorter form. |
| 5 `gradual` | *Graduale* *Ps. 33, 10 et 11* (Heb. 34:10-11; Eng. 34:9-10); p. 703 left column, no. 3977 | Said. Respond *Timete Dominum, omnes Sancti eius: quoniam nihil deest timentibus eum.*; verse *Inquirentes autem Dominum, non deficient omni bono.* This is the second clause of v. 11 only. The Missal's wording is not the Clementine's (*non est inopia*, *non minuentur*). |
| 6 `alleluia` | *Alleluia, alleluia*, verse *Matth. 11, 28*; p. 703 left column, no. 3978 | Said. *Venite ad me, omnes qui laboratis et onerati estis: et ego reficiam vos.*, then *Alleluia*. No Sequence and no Tract. |
| 7 `gospel` | *Sequentia sancti Evangelii secundum Matthaeum*, Mt 5:1-12; p. 703 left and right columns, no. 3979 | Said. Opens *In illo tempore: Videns Iesus turbas* (Clementine *Videns autem Jesus*); ends *quoniam merces vestra copiosa est in caelis.* This is 5:12a; *Sic enim persecuti sunt prophetas …* is not read. Printed cue *Credo.* follows. |
| 8 `offertory` | *Ant. ad Offertorium* *Sap. 3, 1, 2 et 3*; p. 703 right column, no. 3980 | Said. *Iustorum animae in manu Dei sunt, et non tanget illos tormentum malitiae: visi sunt oculis insipientium mori: illi autem sunt in pace, alleluia.* The verses are selected and adapted: *malitiae* where the Clementine has *mortis*, and the intervening clauses of 3:2-3 are omitted. The *alleluia* is part of the antiphon. |
| 9 `secret` | *Secreta* *Munera tibi, Domine, nostrae devotionis offerimus*; p. 703 right column, no. 3981 | Said secretly, first (RGMR 480-481, read). Printed conclusion *Per Dominum.* |
| 10 `commemoration-secret` | *Secreta* of the Twenty-third Sunday, *Pro nostrae servitutis augmento sacrificium tibi, Domine, laudis offerimus*; p. 417 right column, no. 1726 (PDF 498) | Said secretly after the Secret, under its own conclusion. The conclusion is printed in full, and its last words *Per omnia saecula saeculorum* are said aloud before the Preface (RGMR 481). Required, as no. 3. The Sunday's rubric *Praefatio de Ss.ma Trinitate.* that follows it on p. 417 belongs to the Sunday's Mass and is not inherited (RGMR 483). |
| 11 `preface` | **Disputed.** Either *Praefatio de Ss. Trinitate*, *Praefationes sine cantu*, printed p. 293, no. 1082 (PDF 374, read), or *Praefatio communis*, printed p. 297, no. 1086 (PDF 378, located). Notated forms are in the *Praefationes* section, printed pp. 223-298 | Said or sung; one Preface, then *Sanctus*. Which one is appointed is unsettled (see *Occurrence*, Preface). Neither is a local choice. The formulary prints no Preface. |
| 12 `communion` | *Ant. ad Communionem* *Mt. 5, 8-10*; p. 703 right column, no. 3982 | Said (RGMR 504). *Beati mundo corde, quoniam ipsi Deum videbunt: beati pacifici, quoniam filii Dei vocabuntur: beati qui persecutionem patiuntur propter iustitiam, quoniam ipsorum est regnum caelorum.* |
| 13 `postcommunion` | *Postcommunio* *Da, quaesumus, Domine, fidelibus populis omnium Sanctorum semper veneratione laetari*; p. 703 right column, no. 3983 | Said, first (RGMR 505, read). Printed conclusion *Per Dominum nostrum.* (Mame 1922 has *Per Dominum.*). |
| 14 `commemoration-postcommunion` | *Postcommunio* of the Twenty-third Sunday, *Quaesumus, omnipotens Deus: ut, quos divina tribuis participatione gaudere*; p. 417 right column, no. 1728 (PDF 498) | Said after the Postcommunion, under its own conclusion, printed in full. Required, as no. 3. |

No element of the formulary is conditional, and no printed alternative, votive
Tract or paschal form belongs to these two pages. The votive Mass on p. 704 has
its own Tract and paschal variants, and they are not part of this feast.
Everything else in the Twenty-third Sunday's formulary (Introit *Dicit
Dominus*, Epistle Phil 3:17-4:3, Gradual, Alleluia, Gospel Mt 9:18-26,
Offertory, Communion) is **not said** on this date and is not inventoried.

### Wording against the Clementine Vulgate

The repository's Clementine verse artifacts were read for the cited verses
(`…vulgata-clementina.ebible-latvuc` verse-text artifacts
`verse-text-21-psalms-d20e21f8`, `verse-text-25-wisdom-bfeace21`,
`verse-text-47-matthew-2d02758d`, `verse-text-73-apocalypse-8f990cb5`). The
Missal's forms differ from them at the Lesson's incipit, at the Gradual (the
older Roman psalter wording, and the omission of v. 11a *Divites eguerunt, et
esurierunt*), at the Gospel's opening, at the Gospel's end (12a), and at the
Offertory (adapted and selected). The Introit verse matches Ps 32:1 without
the inscription *Psalmus David*, which the Clementine and Douay print inside
v. 1. The Alleluia verse and the Communion agree with the Clementine apart from
orthography and pointing. `tools/tpt mass-propers show --calendar roman-1962
--mass omnium-sanctorum --bible douay-rheims` therefore shows Douay
"reconstructions" that are not the Missal's forms: it gives Ps 33:10-11 whole
(with *The rich have wanted …*) and serves the Introit verse with *A psalm for
David.*

## Other text-bearing parts of this Mass

| Place | Text and appointment | Status and source |
|---|---|---|
| Before the principal Sunday Mass, where used | *Asperges me* with the blessing of water | A Sunday rite outside the Mass and outside this formulary (registered passage `…vatican-typica-1962.ordo-ad-aspergendam-aquam-benedictam`). It is not part of the appointed inventory, and its use on a feast falling on a Sunday is for research to confirm if the study mentions it. |
| Prayers at the foot of the altar | Ps 42 *Iudica me* through *Oramus te*; *Ordo Missae* nos. 1013-1023 | Said: RGMR 425 (read) omits *Iudica* only in Passiontide Masses of the season and in Requiems. Registered passage `…ordo-missae-ad-gradum`. |
| Introit doxology; Kyrie | *Gloria Patri*; ninefold Kyrie, no. 1024 | RGMR 427-428, 430 (read). |
| After the Kyrie | *Gloria in excelsis*, no. 1025 | Said: RGMR 431 (read). Registered `…ordo-missae-kyrie-gloria`. No chant setting is chosen. |
| Before and after the Gospel | *Munda cor meum*, Gospel dialogue; homily | RGMR 471, 474 (located); nos. 1026-1028. |
| After the Gospel or homily | *Credo*, no. 1029 | Said: RGMR 475 a, b (located); printed cue after no. 3979. Registered `…ordo-missae-credo`. |
| After the Secrets | One Preface | Inventoried above as element 11, disputed. |
| Canon | *Te igitur* through the doxology | The one Roman Canon, said secretly (RGMR 500, read). No proper *Communicantes* or *Hanc igitur* (RGMR 501, read: proper forms belong to the octaves of Christmas, Easter and Pentecost and to Masses printing them). |
| Conclusion | *Ite, missa est*, *Placeat*, blessing, last Gospel Jn 1:1-14 | RGMR 507-509 (read); nos. 1132-1139 per `…ordo-missae-conclusio`. |

## Lawful study-text routes

- **Latin, the four own non-scriptural proper bodies (Introit, Collect, Secret,
  Postcommunion): permitted.**
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` carries
  four `omnium-sanctorum` rows with `publication_status = "permitted"` and
  `publication_basis = "public-domain"`. Their basis is the Tours Mame 1922
  printing (`edition.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam`,
  printed pp. 748 and 750, artifact pp. 862 and 864), its checked artifact
  `…all-saints-four-propers-la-checked-82edd79a` and passage
  `…all-saints-four-own-propers-checked-2026-10-20`, collated against the 1962
  target in passage
  `passage.catholic-church.missale-romanum.vatican-typica-1962.all-saints-four-own-propers-word-collation-2026-10-20`.
  The projected text uses the calendar's *j* orthography and the target's
  pointing. Research decides whether the study displays *i* or *j* and states
  it.
- **Latin, the six scriptural bodies (Lesson, Gradual, Alleluia, Gospel,
  Offertory, Communion): a registered route exists; research binds it.** The
  Mame 1922 checked artifact
  `artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.all-saints-scriptural-propers-la-checked-415a1d46`
  (SHA-256 `415a1d46…22fe4f`, rights `public-domain`, United States) is
  carried by six passages `…all-saints-{lesson,gradual,alleluia,gospel,offertory,communion}-la-checked-2026-10-25`.
  Each passage gives the 1962 locus (nos. 3976-3980, 3982) and the Mame locus
  (printed pp. 748-750). The provenance ledger has no row for these six, and the
  calendar entry carries no Latin body for them. Research must confirm a
  publication basis under `guidance/liturgical-text-publication-policy.md` and
  collate each body word for word with the 1962 page before displaying it. The
  Clementine words themselves are public domain, but the Missal's received
  forms differ (above), and the received form, not a Bible reconstruction, is
  the text of the Mass.
- **Latin, the three commemoration orations: permitted.** The provenance
  ledger's `pentecost-23` Collect, Secret and Postcommunion rows have
  `publication_status = "permitted"`. They rest on a project editorial
  projection from the public-domain Pustet 1862 Missal, verified against
  `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-pentecost-23-orations`
  (nos. 1720, 1726, 1728).
- **Latin, the Preface candidates and the Ordinary.** The Preface texts are
  registered in `…vatican-typica-1962.praefationes` and
  `…praefationes-sine-cantu` (the latter the common Preface, n. 1086).
  `src/sources/inventories/roman-1962-ordo-missae-v1.toml` records the 1861
  Cummiskey antecedent collations: the common Preface is word-exact, and the
  Trinity Preface's proper clause is complete, with its opening compared
  separately. Research confirms the publication basis for whichever Preface
  is settled. The Ordinary's parts are registered in the `ordo-missae-*`
  passages.
- **English, the four own orations and Introit.** The Lasance *New Roman
  Missal*, Benziger revision of 1945
  (`edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945`,
  public domain in the United States by nonrenewal per
  `src/sources/inventories/lasance-new-roman-missal-rights-v1.toml`). Its
  English for the `omnium-sanctorum` Introit and Collect (printed p. 1265) and
  Secret and Postcommunion (printed p. 1268) stands in
  `src/sources/inventories/roman-1962-proper-translations-v1.toml` with
  `collation_result = "confirmed"`. The verify and publish passages are
  `…resume-orations-core193-2026-10-23-{verify,publish}-omnium-sanctorum--main--{introit,collect,secret,postcommunion}--all--1`
  and the publication artifact is `…resume-orations-core193-2026-10-23-0736f65f`.
  The Lasance surrounding rubrics are pre-1960 and are not the 1962 order. The
  Lasance English was not re-read on its page images in this stage.
- **English, the three commemoration orations.** Lasance 1945, printed p. 733
  (Collect), pp. 735-736 (Secret) and p. 736 (Postcommunion), confirmed in the
  same translations inventory under `pentecost-23` with
  `…resume-orations-phase2-2026-10-23-{verify,publish}-pentecost-23--main--…`
  passages.
- **English, the scriptural elements.** The Douay-Rheims (Challoner) as
  registered (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  with `…american-1899-ebible` as the other registered Douay printing), read
  through `tools/tpt mass-propers show … --bible douay-rheims`. The Douay
  cannot carry the Missal's forms at the Lesson's incipit, the Gradual, the
  Gospel's opening and end, the Offertory, or the Introit verse's omitted
  inscription. English must never be composed to fill those differences. Where
  the Douay cannot carry the Missal's form, the profile's rule is to say so and
  give the Latin with a description, or to use a hand missal's own English
  under its own attribution if research so decides. Lasance prints English for
  these elements, but no translations-inventory row registers it, so it is only
  a lead.
- **English, the Preface.** Not yet located for either candidate; a lead for
  research (the Lasance Ordinary's Prefaces, and the Ordo Missae inventory's
  antecedent English).

No source was registered or retained in this stage. The existing library was
read first. Everything fetched was either a registered artifact matched to its
registered hash or a live response whose identity and hash are written down
above. No liturgical owner is imported: the formulary is printed in this
family's own Missal and is local to this leaf, and the commemoration's three
orations are read from the same edition. There is therefore no shared-formulary
Makefile dependency to declare.

## Shared records: observations for their owners

This stage owns no source, calendar or tool record, so these are reported
rather than repaired.

- `tools/tests/test_ordinary_appointments.py` (fixture `allSaintsSunday1962`,
  date 2026-11-01) asserts `praefatio-communis` with the comment "494 b)
  reaches the Mass of the Sunday, not a feast said on one". It cites no
  authority, and it sits uneasily with the Missal's own direction for the
  Vigil of the Nativity on a Sunday. The rule is unsettled in the registered
  sources (above; research/scope.md section 11). The test's owner should
  either cite an authority for its reading or mark the assertion disputed.
- `src/sources/calendars/roman-1962/propers.yaml`, mass `omnium-sanctorum`:
  (1) its note "No Preface appointment is inferred" leaves the Sunday case
  unrepresented, while `pentecost-23` carries `ordinary_appointments.preface:
  trinitate`; (2) the six scriptural elements carry ranges only, although Mame
  1922 passages for their received Latin were registered on 2026-10-25, so
  `mass-propers show` labels them "Missal wording not established"; (3) the
  Gradual range `Ps 33:10-11`, Gospel `Mt 5:1-12` and Offertory `Wis 3:1-3` are
  wider than the said text, so Douay reconstructions include words the Mass
  does not read.
- `tools/tpt proper-chronology loci --document …f02-all-saints` resolves the
  Introit to `Ps.32.1`, the Lesson to `Apoc.7.2–12`, the Gradual to
  `Ps.33.10–11`, the Alleluia to `Matt.11.28`, the Gospel to `Matt.5.1–12`, the
  Offertory to `Wis.3.1–3` and the Communion to `Matt.5.8–10`. The Gradual,
  Gospel and Offertory ranges are wider than the said text, as in the item
  above.
- `commentary-work-index formulary --calendar roman-1962 --mass omnium-sanctorum`
  compares 40 loci and lists none: no liturgical commentator in
  `src/sources/commentary/formulary-loci.yaml` has this formulary.

## Remaining verification for research

- Collate every proper element and the three commemoration orations word for
  word against the 1962 page images at 200 and 400 dpi. Write
  `propers/retrieved.txt` and `propers/verified.md` with the loci, conclusions
  and orthography.
- **Settle the Preface** (Trinity n. 1082 or common n. 1086) from an
  authoritative source, or record it as open and present both with the
  evidence. Do not choose it locally. Leads: official or institute Ordos for
  2026 or an earlier year when 1 November fell on a Sunday under the 1960
  rubrics (1964, 1970 for historical practice; 2015, 2020 for current usage),
  and recognized commentaries on the 1960 code. Register any dated witness
  relied on.
- Confirm the last Gospel (Jn 1:1-14 under RGMR 509) against the ICRSP
  statement, and record the result.
- Confirm the publication basis for the six scriptural Latin bodies and either
  Preface, bind the Mame and commemoration-oration routes, and decide the
  English display: Douay where it carries the Missal's form, Latin with a
  description where it does not, and Lasance English for the orations under
  its own attribution, with its pre-1960 rubrics disclosed.
- Settle the chronology inputs before generating `research/chronology.toml`
  and `research/chronology-annotations.tex`. The distinct directly appointed
  passages said on 1 November, in canonical then verse order, are: Ps 32:1
  (verse without inscription); Ps 33:10 and 11b; Wis 3:1-3 (selected); Mt
  5:1-12a; Mt 5:8-10 (again, as the Communion); Mt 11:28; Apoc 7:2-12. The
  commemoration contributes no Scripture. No biblical date is asserted in this
  record.
- Read each appointed passage in its complete literary context: Apoc 7 whole
  with Apoc 6:12-17 and the sealing imagery; Ps 32 and Ps 33 whole; Wis 2:21-3:9;
  Mt 4:23-5:16 and the Sermon on the Mount; Mt 11:25-30. Run the reception
  sweep. `commentary-work-index` gives no liturgical commentator; record that
  negative and search the passages' exegetes directly. Leads among tracked
  works: Guéranger, Durandus, Sicard, Honorius, Rupert, Beleth, Schuster, Bede,
  Augustine (*De sermone Domini in monte*), Chrysostom and Bernard (whose
  sermons for All Saints are a known lead). Also the history of the feast:
  the dedication of the Pantheon under Boniface IV and Gregory IV's extension,
  as stated in the Roman Martyrology for 1 November (lead only, not read on a
  registered witness here).
- Resolve, only if the study relies on them: the Asperges on this Sunday, local
  anniversaries admitting RGMR 449 or 451, a local first-class votive Mass, a
  particular-calendar overlay, and the French *praefatio de Sanctis*
  concession. None is needed for the universal formulary on this date.
- Bind the controlling sources in `research/source-bindings.toml` and declare
  the external owners actually relied on in `research/review-dependencies.toml`.
  The authorities adopted here are: the 1962 facsimile artifact; the Latin
  provenance ledger; the Mame 1922 edition with its two All Saints artifacts
  and their passages; the 1962 collation passages
  (`…all-saints-four-own-propers-word-collation-2026-10-20`,
  `…temporal-pentecost-23-orations`, `…praefationes`,
  `…praefationes-sine-cantu`, `…rubricae-generales-missalis`, the `ordo-missae-*`
  passages); the Lasance edition, its scan and rights inventory, and the
  translations inventory; the Clementine Vulgate and the Douay-Rheims editions
  and the psalm concordance; and, as computation inputs only,
  `src/sources/calendars/roman-1962/propers.yaml` and `rubrics.yaml`.

## Research-stage verification (run 427e2f58bb897a16, 2026-10-26)

The research stage closed the list above as follows; the records cited are this
leaf's own.

- Collation: done at 200 and 400 dpi from the registered CMAA facsimile
  (PDF pp. 783-784 and 497-498). `propers/retrieved.txt` keeps the text-layer
  pulls and the misreadings lists; `propers/verified.md` carries the fourteen
  appointed elements in liturgical order with the fully accented 1962
  *i*-orthography text.
- Preface: **not settled**; recorded as open with the evidence. Element 11 of
  `propers/verified.md` is a slot, and `research/interpretations.md` section 6
  flags it for authoring. No registered Ordo or 1962-horizon rubrical
  commentary settles it; research/scope.md section 11 names the registered
  sources searched and gives authoring one fixed rule for the slot. The dated
  web witnesses above were withdrawn as evidence in iteration 2 and are
  registered and bound as context only (bindings 35-40).
- Last Gospel: Jn 1:1-14 confirmed (RGMR 507-510 read on the page image,
  iteration 2). The ICRSP line *Dernier Évangile du XXIIIe dimanche*
  conflicts with RGMR 509; it is context only (binding 35) and is neither
  imported nor presented.
- Publication basis and English display: the basis is stated in
  `propers/verified.md` (17 U.S.C. 103(b); Mame 1922 for the feast's ten
  elements; Pustet 1862 for the commemoration orations, read on the page
  images of the tracked extract `pentecost-23-prayer-pages-7e6ef53b`, printed
  pp. 357-358 = parent PDF pp. 443-444), and the English
  routes are given there element by element — Douay only where it carries the
  received form, the failures listed, the Lasance scriptural English named as
  a lead without an inventory row.
- Chronology inputs: the said-text list above was used; the over-wide ranges
  in `propers.yaml` and the chronology loci are reported in
  `research/scope.md` section 10, not adopted.
- Literary context and reception sweep: `research/scope.md` sections 2-4;
  the `commentary-work-index formulary` negative is recorded (section 3.1);
  the passages' exegetes were read directly (sections 3.2-3.10); the feast's
  history is given from Durandus VII.34, Beleth and Schuster, and the
  Martyrology lead was not read on a registered witness.
- Local contingencies (Asperges, anniversaries, votive overlays, *praefatio de
  Sanctis*): not relied on; the study addresses the universal formulary.
- Bindings and dependencies: `research/source-bindings.toml` (34 bindings
  after the iteration-1 repair; every used binding carries its full source
  fingerprint, taken 2026-10-26; binding 1 gained the RGMR Preface and
  last-Gospel loci and the Vigil of the Nativity rubric in iteration 2; the
  source-registration stage's iteration 2 appended bindings 35-41, the
  registered dated web witnesses and Murphy's 1960 rubrics commentary, as
  context only) and
  `research/review-dependencies.toml`, which since iteration 2 also declares
  the Lasance oration records named under *Lawful study-text routes* above: the publication artifacts `…0736f65f` and `…5a4e83f7`, the
  fourteen verify and publish passages, and the same-witness conclusion table
  `…resume-orations-conclusion-table-2026-10-23-7dbb4a25` with its two
  passages.
