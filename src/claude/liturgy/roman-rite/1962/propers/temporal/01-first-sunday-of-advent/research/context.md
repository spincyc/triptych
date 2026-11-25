# Celebration context and complete appointed inventory

Resolved 25 November 2026 for the `proper-study` v20 production of the Claude
1962 leaf, run `77c1ca91ef2d5e93`, seeded at commit
`81696af68345984cc763e2f6f2771c4185ceb1b1`. The production-plan entry of
2026-11-25 in `guidance/liturgy/propers-production-plan.md` (the prose
paragraph and the line "Authorized 2026-11-25: provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/01-first-sunday-of-advent`")
authorizes provider `claude` for this one identity and for Sunday
29 November 2026, under the current three-document contract, as an
independent Claude production that is not a companion to or derivative of the
GPT leaf for the same identity or of any other leaf. It opens nothing else,
and publication to main is not part of that decision. `ARGS.research_handoff`
is `none`, so no handoff was supplied. The other provider's leaf, review and
release records for this identity, and every postconciliar record (including
the postconciliar rows that share the calendar key `advent-1`), are outside
this record's evidence; none was opened and nothing below is taken from them.
This provider's Twenty-fourth Sunday context record (identity `68`) was read
only as a model of this record's shape; no finding of it is relied on, and
every locus below was read or located afresh in this stage. Provider-neutral
library records under `src/sources/` are used as library evidence and are
named where used. This record settles what is studied. It holds no study
prose, spoken text, timing claim or review verdict; the research stage
collates the sources and may correct it from evidence.

## Publication mode

The section *Reference-only publication scope* of the production plan states
that no reference-only target is currently authorized, and no line of the form
`- Authorized reference-only …` names this provider and identity. This study
is therefore **not** reference-only: the ordinary schema-2 appointed-text mode
applies, with `propers/retrieved.txt` and `propers/verified.md` as a focused
pull and a facsimile-collated transcription under the 1962 profile, and with
the lawful-text and English rules of that profile. Whether every element can
be published complete (`complete`), or only some (`rights-limited`), is decided
by the routes recorded below and by research, not assumed here.

## Identity, governing books and territory

- Canonical identity:
  `liturgy/roman-rite/1962/propers/temporal/01-first-sunday-of-advent`,
  catalog ID `01`, the First Sunday of Advent, the first entry of the 1962
  temporal registry in `guidance/liturgy/roman-1962-propers.md` (band
  `01`-`04`). Calendar family `roman-1962`. `tools/check-proper-identity
  --document liturgy/roman-rite/1962/propers/temporal/01-first-sunday-of-advent
  --calendar roman-1962` passes ("Identity 01 is registered in the roman-1962
  calendar"). The finding-aid mass index
  `src/sources/calendars/roman-1962/propers.yaml` carries the formulary as
  `advent-1`, `registry: '01'`, season `advent`, with its ten propers
  (orations with text, the Epistle with a Mame 1922 text, the rest by
  Scripture reference), a conditional disposition on the Alleluia for Advent
  ferias, and a Trinity Preface appointment. That index is a lead and never the
  source of record for any wording.
- Distinct neighbouring identities, not studied here: `02`, the Second Sunday
  of Advent, which follows on the next page under its own heading (printed
  p. 3, PDF 84, *DOMINICA SECUNDA ADVENTUS*, *I classis*, *Statio ad S. Crucem
  in Ierusalem*, Introit *Populus Sion*, no. 11, read at 200 dpi); and the
  last formulary of the Proper of Time, `68`, said on 22 November 2026. No text
  of either travels into this formulary. The Advent ferias of the following
  week use this Mass (rubrics below); they are not this identity.
- Governing edition: *Missale Romanum*, editio typica, Typis Polyglottis
  Vaticanis 1962 (`edition.catholic-church.missale-romanum.vatican-typica-1962`),
  controlled on the page images of
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.
  A copy fetched in this stage (2026-11-25) from the registered `source_url`
  matched the registered SHA-256
  `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` and
  82,815,941 bytes before any page was read. The formulary was read on page
  images rendered from that file at 200 dpi (whole pages, PDF 82-84) and at
  400 dpi (crops of the lower half of PDF 82 across both columns and of the
  whole left column of PDF 83). Also read on 200-dpi images: RG 1-19 (PDF 10),
  RG 19-42 (PDF 11), RG 96-112 (PDF 16), RG 126-137 (PDF 18), RGMR 424-442
  (PDF 29), the *Calendarium* for November and early December (PDF 54), and the
  Sanctorale for 29 November (PDF 509). Printed front-matter pages run two
  ahead of the PDF page (PDF 10 is printed p. XII; PDF 54 is printed p. LII);
  in the Proper of Time and the Sanctorale the PDF page runs 81 ahead of the
  printed page (PDF 82 is printed p. 1, which carries no printed folio; PDF 83
  is printed p. 2; PDF 509 is printed p. 428). The text layer served only to
  locate pages; loci marked "located" were found on it and not re-read on an
  image.
- Printed heading and rank: *PROPRIUM DE TEMPORE*, *TEMPUS ADVENTUS*,
  *DOMINICA PRIMA ADVENTUS*, *I classis*, *Statio ad S. Mariam maiorem*,
  printed p. 1 (PDF 82), under the illustrated headpiece that opens the
  Proper of Time. The station is a printed heading of place and not an
  appointed text; it is also recorded in the registered text-free control
  `passage.catholic-church.missale-romanum.vatican-typica-1962.advent-primer-20261119-advent-christmas-stations`.
  The headpiece's engraved scrolls and banner (*Ecce virgo concipiet et pariet
  filium*, *Universi qui te exspectant non confundentur*, *Ecce Agnus Dei*,
  *Sol iustitiae*) are decoration of the page, not text of the Mass, and are
  not part of the inventory. The running head of p. 2 is *Dominica prima
  Adventus*.
- Formulary boundary: it begins under that heading with the Introit, marginal
  no. 1, the first numbered unit of the Proper of Time, and ends with the
  Postcommunion, no. 10, in the right column of p. 2 (PDF 83), followed by two
  rubrics on ferial use that run over to the head of p. 3 (PDF 84), after which
  the heading of the Second Sunday and its Introit, no. 11, begin. Marginal
  nos. 1-10, each printed whole and legible on these two pages. The
  expected-target inventory `src/sources/inventories/missal-expected-targets-v1.toml`
  carries the same form, `roman-1962.temporal.advent-1` ("artifact PDF pp.
  82–83, printed pp. 1–2; numbered units 1–10"), with one slot row per
  element.
- Governing books within that edition, read or located where cited below: the
  *Calendarium*; the *Rubricae generales* (part I of the 1960 code as printed,
  cited RG); the *Rubricae generales Missalis romani* (part III, cited RGMR);
  the *Ordo Missae*; the *Praefationes*; the Proper of Time; the Sanctorale
  (for the commemoration of the day that this Sunday excludes). Part II, the
  *Rubricae generales Breviarii romani*, is not printed in this witness ("Hic
  omittuntur", printed p. XX, PDF 18, read).
- Territory: the universal 1962 General Roman Calendar. No diocese, church
  titular or dedication, religious institute or other particular calendar was
  supplied, so no local overlay is applied or computed. The study concerns the
  universal formulary on this date, not a direction to any particular church.
- Language: Latin governs. Every English route below is a historical study
  aid, not an approved vernacular liturgical text.
- Cycle: the 1962 Missal appoints the readings with the formulary and has no
  Lectionary cycle. No A/B/C or I/II value exists for this record, and
  `calendar-days` returns `lectionary: null`. The requested identity and the
  formulary appointed on the requested date are the same (see *Occurrence*),
  so there is no requested-versus-appointed difference to preserve. The
  computation tool labels the day with liturgical year `2027`, the year this
  Sunday begins; that label is the tool's and names no cycle.
- Season: *Tempus Adventus*, its first Sunday. RG 71 (printed p. XV, PDF 13,
  located): Advent runs from I Vespers of this Sunday to None of the Vigil of
  the Nativity inclusive. The Second Sunday of Advent follows on
  6 December 2026.
- Homily audience for the later homily stage: adult parish assembly
  (`ARGS.audience`). RGMR 474 (printed p. XXXIII, PDF 31, located) places a
  brief homily after the Gospel, *praesertim in dominicis*; the homily is
  authored preaching and adds no text to this inventory.

## Occurrence on 29 November 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
roman-1962 --date 2026-11-29 --json` returns `appointed: advent-1`, "First
Sunday of Advent", rule "the fourth Sunday before 25 December", season
`advent`, no Lectionary value, nothing unresolved, and a second candidate, the
fixed-date `comm-s-saturnini-martyris` ("Comm. S. Saturnini Martyris"), which
it lists under `commemorations` while reporting `ranked: false`: the day layer
ranks nothing, and precedence belongs to the rubrics layer. Recomputed here:
1 January 2026 is a Thursday, so the year's dominical letter is *D*; the
*Calendarium* gives 29 November the letter *d*, so it is a Sunday; 30 November
2026 is a Monday, and 29 November is therefore the Sunday nearest 30 November;
25 December 2026 is a Friday, and 29 November is the fourth Sunday before it
(29 November, 6, 13 and 20 December).

**The rubric that places it.** RG 20, printed p. XIII (PDF 11), read:
*Dominica I Adventus ea est, quae cadit die 30 novembris vel est ipsi
proximior.* In 2026 that Sunday is **29 November**. RG 11 a, printed p. XII
(PDF 10), read: the Sundays I-IV of Advent are *Dominicae I classis*, as the
printed heading also says.

**The calendar of the day.** The *Calendarium*, printed p. LII (PDF 54), read:
29 November carries dominical letter *d*, *III* [Kal. Dec.], epact *XXII*, and
the entry *Commemoratio S. Saturnini Mart., Comm.*; 30 November carries *S.
Andreae Ap., II classis*; no vigil is printed for 29 November. In the
Sanctorale, which opens with this day, *FESTA NOVEMBRIS*, *Die 29 novembris*,
*S. Saturnini Mart.*, *Commemoratio*, *Missa Laetabitur, de Communi unius
Martyris IV loco [8], cum orationibus ut infra*, with its Oratio *Deus, qui nos
beati Saturnini*, no. 1809, Secreta no. 1810 and Postcommunio no. 1811, each
marked *P*, printed p. 428 (PDF 509, read at 200 dpi).

**Precedence.** `tools/tpt calendar-rubrics day --calendar roman-1962 --date
2026-11-29 --json` could not be run in this stage: it refused with "no rubrics
file … run `calendar-rubrics structure` first", because the generated rubrics
product was absent from the workspace browser-data root while a concurrent
browser-products build was running, and this stage starts no build. The
result below therefore rests on the printed rubrics alone, read or located at
these loci:

- RG 15, printed p. XII (PDF 10), read: *Dominica I classis, in occurrentia,
  festis quibuslibet praefertur*, the one exception named there being the
  Immaculate Conception against an Advent Sunday, which does not arise in 2026
  (8 December 2026 is a Tuesday).
- RG 91, table of precedence (printed p. XVII, PDF 15, located): row 6
  *Dominicae Adventus, Quadragesimae et Passionis, et dominica in albis*, among
  the days of the I class.
- RG 107-109, printed p. XVIII (PDF 16), read: commemorations are privileged
  or ordinary; the privileged are those of a Sunday, a I-class day, the days
  within the Christmas octave, the September Ember ferias, the Advent, Lent and
  Passiontide ferias and the Greater Litanies; *omnes aliae commemorationes
  sunt commemorationes ordinariae*.
- RG 111 a, same page, read: *in diebus liturgicis I classis et in Missis in
  cantu non conventualibus, nulla admittitur commemoratio, praeter unam
  privilegiatam*. RGMR 434 a, printed p. XXXI (PDF 29), read, says the same of
  the Mass's orations: on I-class days no other oration is admitted besides
  one privileged commemoration (and an oration said under the one conclusion,
  which the rubrics do not appoint here).
- The commemoration of St Saturninus is of the ordinary kind (it is none of
  those RG 109 names), so it is not made at any Mass of this Sunday, low, sung
  or conventual. No privileged commemoration occurs on 29 November 2026: the
  day is itself the Sunday, and no I-class day, octave day, Ember feria or
  Advent feria falls on it.

The rubrical result has no branch: one formulary, one Collect, one Secret, one
Postcommunion, in every Mass. No other universal feast, vigil, octave or Ember
day falls on the date, and RG 33 (printed p. XIII, PDF 11, read) would omit a
vigil of the II or III class falling on any Sunday in any case. Violet
vestments follow RG 128 a, printed p. XX (PDF 18), read: *a dominica I
Adventus usque ad vigiliam Nativitatis Domini inclusive*. Rose (RG 131, same
page) belongs to the Third Sunday of Advent and not to this one. No oration is
added by universal rubric on this date. Orations added by local fact are not
computed: an *oratio imperata*, which RGMR 457 d (printed p. XXXII, PDF 30,
located) prohibits on all I- and II-class days in any case, and the oration
for the Pope's or the diocesan bishop's anniversary (RGMR 449, same page,
located), which depends on a local date. Any external solemnity or votive
Mass a particular church might keep is local, not computed, and in any case
yields to a I-class Sunday (RG 15); none alters the Sunday's formulary.

**Dated official witnesses.** Two dated Ordos of institutes that celebrate with
the 1962 books were read live for this date on 2026-11-25. Neither response is
retained or registered in this stage; both are held only in this run's scratch
area. Their SHA-256 values are recorded so that the research stage can register
a dated edition and passage if it relies on them; the pages are mutable, so a
later fetch may differ.

- FSSP France, *Ordo du mois*, <https://www.fssp.fr/ordo-du-mois/>, read
  2026-11-25, response 165,314 bytes, SHA-256
  `80c8062754aa92d263edb6876c1fcbcc99c20e3c3b426ae7096972ff1157eacb`:
  *Dimanche 29 novembre* — *1er dimanche de l'Avent (1ère classe, Violet)*.
  The Ordo prints one line per day and names no commemoration for
  29 November; that silence is not read as evidence either way.
- ICRSP France, *Ordo*, <https://icrspfrance.fr/ordo.php?d=2026-11-29>, read
  2026-11-25, response 110,126 bytes, SHA-256
  `7376f82d7312eba94c2af3ee2d42a74424b6867546d851f825e28d272ea3b4be`:
  *dimanche 29 novembre 2026* — *Iᵉʳ Dimanche de l'Avent*, *Temps de
  l'Avent*, I class, violet; Gloria marked as not said, Credo said, Trinity
  Preface; no commemoration listed; Mass *Messe propre (Ad Te levavi) : Or.
  pro Papa. Credo. Préf. de la T. Ste Trinité*; I Vespers of the Sunday on
  Saturday 28 November. The page states that it is the institute's own Ordo,
  to which each church adds its local feasts.

Computation, the printed rubrics and calendar, and both dated witnesses agree
on the formulary (the First Sunday of Advent), the first class and the violet
colour; the ICRSP entry also names the Mass by its Introit *Ad te levavi*,
omits the Gloria, gives the Credo and the Trinity Preface, and carries no
commemoration of St Saturninus. Nothing fails closed. One thing in that
witness is its own and is not imported: its *Oratio pro Papa* is an institute
observance whose basis was not examined and which the books do not appoint on
this date by universal rubric. This record follows the books.

## Appointed proper

Every element is required on this Sunday and none has an alternative within
the formulary: the pages print no option, no choice and no substitute. The one
conditional rubric on the page, which drops the Alleluia, applies only to
Advent ferias that take this Mass, not to the Sunday (below). Loci are the
printed page and marginal number of the controlling edition, read on 200- and
400-dpi page images of artifact PDF pp. 82-83. Psalms are cited in the
Missal's Vulgate numbering, with the Hebrew number of the repository's psalm
concordance
(`src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/psalm-numbering-ee3c7757/psalm-numbering.tsv`,
SHA-256 `535761886df263b55bf39aa6c5f8ec1a4997abd6c33627c50518d65a0965b721`
recomputed and matched) in parentheses. That concordance gives an English
verse offset of zero for Ps 24 and of one for Ps 84 vv. 2-14, the inscription
being v. 1 in the Vulgate: Vg. 84:8 is English 85:7 and Vg. 84:13 is English
85:12.

| Order and key | Element and printed locus | Liturgical place, extent and boundary |
|---|---|---|
| 1 `introit` | *Ant. ad Introitum* *Ad te levavi animam meam*, printed citation *Ps. 24, 1-3* (25:1-3); verse *Ps. ibid., 4* (25:4); p. 1 left column, no. 1 | Entrance chant (RGMR 427, read on PDF 29): antiphon *Ad te levavi animam meam: Deus meus, in te confido, non erubescam: neque irrideant me inimici mei: etenim universi, qui te exspectant, non confundentur*; psalm verse *Vias tuas, Domine, demonstra mihi: et semitas tuas edoce me*; *Gloria Patri* printed in full; *Quo finito, repetitur Ad te levavi usque ad psalmum*, with the rubric *Hic modus repetendi antiphonam ad Introitum servatur per totum annum*. |
| 2 `collect` | *Oremus.* *Oratio* *Excita, quaesumus, Domine, potentiam tuam, et veni*; p. 1 right column, no. 2 | First and only oration of the Mass (RGMR 433-434, read; RG 111 a). Asks the Lord to stir up his power and come, so that from the threatening dangers of our sins we may deserve to be rescued by his protection and saved by his deliverance. Printed conclusion in full: *Qui vivis et regnas cum Deo Patre in unitate Spiritus Sancti, Deus: per omnia saecula saeculorum. R. Amen.* The conclusion addresses the prayer to the Son. Preceded on the page by the rubric *Non dicitur Gloria in excelsis in Missis de Tempore ab hac dominica usque ad vigiliam Nativitatis Domini inclusive.* |
| 3 `epistle` | Rom 13:11-14, printed *Rom. 13, 11-14*; p. 1 right column foot to p. 2 left column, no. 3 | *Lectio Epistolae beati Pauli Apostoli ad Romanos*. Opens *Fratres: Scientes, quia hora est iam nos de somno surgere*; ends *sed induimini Dominum Iesum Christum.*, which is v. 14a: the lesson does not print v. 14b. No shorter form. |
| 4 `gradual` | *Graduale*, printed citation *Ps. 24, 3 et 4* (25:3-4); p. 2 left column, no. 4 | After the Epistle: respond *Universi, qui te exspectant, non confundentur, Domine*; verse *Vias tuas, Domine, notas fac mihi: et semitas tuas edoce me*. The Gradual's verse gives Ps 24:4b with *notas fac mihi* where the Introit's verse, on the facing column, has *demonstra mihi*. |
| 5 `alleluia` | *Alleluia, alleluia. V. Ps. 84, 8* (85:8; English 85:7); p. 2 left column, no. 5 | *Ostende nobis, Domine, misericordiam tuam: et salutare tuum da nobis. Alleluia.* Required on the Sunday. The rubric printed between nos. 4 and 5, *In feriis Adventus, quando per hebdomadam adhibetur Missa de dominica, non dicitur Alleluia, nec versus sequens, sed tantum graduale*, governs only the ferias of the week (the finding aid's `advent-1-alleluia-use` disposition records the same condition). No Tract and no Sequence. |
| 6 `gospel` | Lk 21:25-33, printed *Luc. 21, 25-33*; p. 2 left column, no. 6 | *Sequentia sancti Evangelii secundum Lucam*. Opens *In illo tempore: Dixit Iesus discipulis suis: Erunt signa in sole, et luna, et stellis*; carries the signs in sun, moon and stars and the distress of nations (vv. 25-26), the Son of man coming in a cloud with great power and majesty (v. 27), the command to look up and lift up the head because redemption draws near (v. 28), and the likeness of the fig tree with the sayings on this generation and on heaven, earth and Christ's words (vv. 29-33); ends at v. 33, *verba autem mea non transibunt*. Printed rubric follows: *Credo, quod dicitur in qualibet dominica …; non dicitur autem in feriis, quando adhibetur Missa dominicae praecedentis.* No shorter form. |
| 7 `offertory` | *Ant. ad Offertorium* Ps 24:1-3 (25:1-3), printed *Ps. 24, 1-3*; p. 2 right column, no. 7 | *Ad te levavi animam meam: Deus meus, in te confido, non erubescam: neque irrideant me inimici mei: etenim universi, qui te exspectant, non confundentur.* The same words as the Introit antiphon. |
| 8 `secret` | *Secreta* *Haec sacra nos, Domine, potenti virtute mundatos*; p. 2 right column, no. 8 | Said secretly (RGMR 480-481). Asks that these holy things, having cleansed us by their mighty power, make us come purer to their source (*ad suum … principium*). Printed conclusion in full: *Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate Spiritus Sancti, Deus: per omnia saecula saeculorum. R. Amen.* Followed by the printed direction *Praefatio de sanctissima Trinitate: quae dicitur tamquam de Tempore in dominicis Adventus et in omnibus dominicis II classis, extra tempus natalicium et paschale; non vero in feriis, quando adhibetur Missa harum dominicarum, sed tunc dicitur praefatio communis.* |
| 9 `communion` | *Ant. ad Communionem* Ps 84:13 (85:13; English 85:12), printed *Ps. 84, 13*; p. 2 right column, no. 9 | *Dominus dabit benignitatem: et terra nostra dabit fructum suum.* |
| 10 `postcommunion` | *Oremus.* *Postcommunio* *Suscipiamus, Domine, misericordiam tuam in medio templi tui*; p. 2 right column, no. 10 | Asks that we receive God's mercy in the midst of his temple, so as to go before the coming solemnities of our restoration (*reparationis nostrae ventura solemnia*) with fitting honours. Printed conclusion *Per Dominum nostrum.* |

The three orations close at three lengths on these pages: the Collect with the
full conclusion to the Son, *Qui vivis et regnas cum Deo Patre*; the Secret
with the full *Per Dominum nostrum Iesum Christum … per omnia saecula
saeculorum. R. Amen.*; the Postcommunion with the cue *Per Dominum nostrum.*
The finding aid's oration texts carry the same three conclusions.

Two further rubrics close the formulary, from the foot of p. 2 right column to
the head of p. 3 (PDF 83-84, read): through the year, when a ferial Mass is
said in the week, the preceding Sunday's Mass is used unless a proper Mass is
assigned, and the Sunday's orations are likewise taken when a feria without
its own Mass is to be commemorated; and *De feriis Adventus fit commemoratio in
omnibus Missis, tam in cantu quam lectis.* With the Alleluia, Credo and Preface
rubrics above, they define the ferial use of this Mass in the following week.
None of them changes what is said on 29 November 2026.

The formulary prints no Tract, Sequence, prophecy, proper *Communicantes* or
*Hanc igitur* (RGMR 501, printed p. XXXIV, PDF 32, located: such variations are
noted in the proper Mass, and none is noted here), *Oratio super populum*,
second or third oration of its own, blessing, or alternative reading. The 1862
antecedent's rubric adding, from this day to the Vigil of the Nativity, the
oration *Deus, qui de beatae Mariae* with *Ecclesiae tuae* or *Deus omnium
fidelium* after the oration of the day, and its corresponding *De S. Maria*
and *Contra persecutores Ecclesiae* or *pro Papa* Secrets and Postcommunions
(text layer, lines 13242-13305, 13408-13441 and 13455 onward), belong to the
pre-1960 rubrics and are not part of the 1962 formulary.

### Wording against the Clementine Vulgate

The comparisons below were made against the tracked Clementine Vulgate
(`edition.catholic-church.vulgata-clementina.ebible-latvuc`, its verse-text
artifacts) through `tools/tpt mass-propers show --calendar roman-1962 --mass
advent-1 --bible clementine-vulgate`, with the Epistle and Gospel compared
token by token by script against a reading of the page images, after
normalising i/j, ligatures and accents and ignoring pointing and capitals. They
are textual observations about wording and boundary. Whether a chant or lesson
follows an older Latin psalter or Bible text, and which, is left to research,
and no origin is asserted here.

- **Introit and Offertory.** Both antiphons read *Ad te levavi animam meam*
  where the Clementine at Ps 24:1 reads *Ad te, Domine, levavi animam meam*,
  and *etenim universi, qui te exspectant* where Ps 24:3 reads *etenim
  universi qui sustinent te*. Both omit the title *In finem. Psalmus David*.
  The Introit's verse agrees with Ps 24:4b and omits v. 4a, *Confundantur
  omnes iniqua agentes supervacue*.
- **Epistle.** The Missal's *Fratres: Scientes* stands for the Clementine's
  *Et hoc scientes tempus: quia*, so the lesson begins within v. 11 and drops
  *Et hoc … tempus*. It ends at v. 14a, *sed induimini Dominum Iesum
  Christum*, without v. 14b, *et carnis curam ne feceritis in desideriis*. The
  Missal spells *Abiciamus* (Clementine *Abjiciamus*) and *comessationibus*
  (as the Clementine); every other word of vv. 11-14a agrees.
- **Gradual.** The respond *Universi, qui te exspectant, non confundentur,
  Domine* has no *etenim*, reads *qui te exspectant* for *qui sustinent te*,
  and adds *Domine*. The verse reads *notas fac mihi* where Ps 24:4b reads
  *demonstra mihi*; the rest of the verse agrees.
- **Alleluia.** Agrees with Ps 84:8 in every word.
- **Gospel.** The liturgical opening *In illo tempore: Dixit Iesus discipulis
  suis: Erunt signa* stands for the Clementine's *Et erunt signa* at the head of
  v. 25, dropping *Et*, which in Luke ties these signs to the preceding
  prophecy of Jerusalem's fall (vv. 20-24). Every other word of vv. 25-33
  agrees, with pointing differences only (for instance *movebuntur. Et tunc*
  against *movebuntur: et tunc*).
- **Communion.** The Missal reads *Dominus dabit benignitatem* where the
  Clementine at Ps 84:13 reads *Etenim Dominus dabit benignitatem*; the rest
  agrees.

## Other text-bearing parts of this Mass

These are fixed or rubrically appointed texts of the 1962 *Ordo Missae*,
*Praefationes* and appendix, not proper text. The study refers to them and
does not reproduce the Ordinary. RGMR 424-442 were read on the page image (PDF
29); RGMR 474-476 (PDF 31), 494 and 501 (PDF 32) and 507-510 (PDF 33) were
located on the text layer. The Trinity Preface (*Praefationes sine cantu*,
printed p. 293, no. 1082, PDF 374, located) and the *Ordo Missae* were not
re-read on an image in this stage; they are cited from the registered passage
records `…vatican-typica-1962.ordo-missae-ad-gradum`, `…ordo-missae-kyrie-gloria`,
`…ordo-missae-credo`, `…ordo-missae-conclusio` and `…praefationes`, which the
research stage confirms before relying on them.

| Place | Text and appointment | Status and source |
|---|---|---|
| Before the principal Mass, where used | *Asperges me* with the Sunday blessing of water, appendix | A Sunday rite outside the Mass and outside this formulary; not part of the appointed inventory. |
| Prayers at the foot of the altar | Ps 42 *Iudica me* through *Oramus te* | Said: RGMR 425 omits *Iudica* only from the First Sunday of the Passion to Maundy Thursday and in Masses for the dead. |
| Introit doxology; Kyrie | *Gloria Patri*; ninefold Kyrie | RGMR 427-428, 430: the *Gloria Patri* at the Introit is omitted only in Passiontide and in Masses for the dead; printed in full at no. 1. |
| After the Kyrie | *Gloria in excelsis* | **Not said**: the printed rubric at no. 2 and RGMR 432 b (*in omnibus Missis in quibus adhibetur color violaceus paramentorum*, read). |
| Gospel and homily | Gospel dialogue (*Dominus vobiscum*, *Sequentia sancti Evangelii*); homily | RGMR 471 and 474 (located). |
| After the Gospel or homily | *Credo* | Said: printed rubric after no. 6 and RGMR 475 a, *in qualibet dominica*. |
| After the Secret | *Praefatio de Ss.ma Trinitate* | Appointed, not chosen: printed direction after no. 8 and RGMR 494 b, *tamquam de Tempore in dominicis Adventus, et in omnibus dominicis II classis, extra tempus natalicium et paschale*. RGMR 483: no commemoration brings in a proper Preface. No other Preface applies on the Sunday; the common Preface belongs only to the ferias that use this Mass. |
| Canon | *Te igitur* through the doxology | The one Roman Canon, said secretly. No alternative Eucharistic Prayer and no proper insertion for this day (RGMR 501). |
| Conclusion | *Ite, missa est*, *Placeat*, blessing, last Gospel Jn 1:1-14 | RGMR 507: *Ite, missa est* is said; *Benedicamus Domino* replaces it only before a procession or after the Maundy Thursday evening Mass. RGMR 508-509; none of the omission cases of RGMR 510 applies. |

## Lawful study-text routes

- **Latin, the three orations.** Control: the 1962 page images above and the
  registered passage
  `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-advent-1-orations`
  (verified 2026-09-03 at the same loci). Publication basis: 17 U.S.C. 103(b)
  with a public-domain antecedent, as settled for the repository in
  `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`. The
  Latin provenance ledger
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` carries
  collated `publication_status = "permitted"` rows for `mass = "advent-1"`
  Collect, Secret and Postcommunion, each at provenance confidence `high`,
  publishing on the tracked 1862 text layer
  (`artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`,
  SHA-256 `f34bc7cf9293ffb353159e94118f4316bb4cc0a60230b315904dc77ba2502162`
  recomputed and matched) at printed pp. 1-3, lines 13230-13240, 13400-13406
  and 13446-13453, through the editorial-projection passages
  `passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-09-03.advent-1-{collect,secret,postcommunion}`.
  On the page images read here, the 1962 words of all three agree with the
  finding aid's bodies and conclusions. The 1862 text layer prints the Secret's
  conclusion as the cue *Per Dominum.*; the ledger carries the 1962's fuller
  printed conclusion as a declared transformation.
- **Latin, the Epistle.** The ledger carries a collated `permitted` row for
  `mass = "advent-1"`, Epistle, at confidence `high`, through
  `passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.primary-advent-1-epistle`,
  publishing on the registered public-domain Mame 1922 witness
  (`edition.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam`,
  artifact `…adapted-primary-readings-la-checked-e3a67098`, Mame artifact page
  116, printed p. 2) and verified against the 1962 page images by
  `passage.catholic-church.missale-romanum.vatican-typica-1962.primary-advent-1-epistle-word-collation-2026-10-20`.
  That body keeps the Mame spellings *Abjiciamus* and *commessationibus*
  against the 1962's *Abiciamus* and *comessationibus*, disclosed there as
  received spellings. The 1862 text layer prints the same lesson (lines
  13310-13330, citation line *c. 13.*), in the 1962's words apart from
  orthography, OCR damage and pointing.
- **Latin, the five chants and the Gospel.** The ledger carries no row for the
  Introit, Gradual, Alleluia, Gospel, Offertory or Communion of this
  formulary. A public-domain antecedent is located in the same 1862 text layer
  under *Dominica I Adventus*, *Statio ad S. Mariam Majorem*, *Ad Missam*
  (heading lines 13185-13194), printed pp. 1-3: Introit lines 13196-13220,
  Gradual 13331-13335, Alleluia 13336-13340 with the ferial rubric
  13342-13346, Gospel 13347-13388 (citation line *c. 21.*) with *Et dicitur
  Credo* at 13390, Offertory 13392-13398, Communion 13443-13445. On the text
  layer these agree in words with the 1962, including every divergence from
  the Clementine listed above (*Ad te levavi* without *Domine*, *qui te
  expectant*, *Universi … Domine*, *notas fac mihi*, the liturgical Gospel
  opening *Dixit Jesus discipulis suis: Erunt signa*, *Dominus dabit* without
  *Etenim*), apart from orthography, pointing, OCR damage and citation form;
  the Communion's citation line reads *Ps. 81* on the text layer; the page
  image (PDF p. 89, printed p. 3) reads *Ps. 84*, so the layer misreads.
  The research stage read printed pp. 1-3 on the page images and found every
  element in the same words as the 1962 (propers/verified.md, *The publication
  basis of the Latin*). The registered 1862 scan
  (`artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.ia-facsimile-pdf-363d6fc3`)
  was not fetched in the context stage; research fetched and matched it.
  The registered Mame 1922 edition, whose artifact p. 115 opens *Dominica I
  Adventus* and whose p. 116 carries the
  Epistle followed by the Gradual (the ledger's Epistle locus), is a possible
  second route that research would read on its images; no retained Mame text
  covers these six elements.
- **English, canonical Scripture.** The Douay-Rheims (Challoner) as registered
  (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  with `…american-1899-ebible` as the other registered Douay printing), read at
  the Vulgate loci through `tools/tpt mass-propers show … --bible
  douay-rheims`, which resolves the Missal's Vulgate psalm numbering. Its
  canonical verses are **not** the Missal's wording at the Introit and
  Offertory (Douay Ps 24:1 *To thee, O Lord, have I lifted up my soul*, with
  *O Lord* that the Missal lacks, and v. 3 *none of them that wait on thee*,
  rendering *sustinent te*), the Gradual (Douay v. 4 *Shew, O Lord, thy ways to
  me*, rendering *demonstra* and not the Gradual's *notas fac*, and no
  *Domine* after *confounded*), the Epistle's opening and end (Douay v. 11
  *And that, knowing the season*, and v. 14 continuing *and make not provision
  for the flesh in its concupiscences*), the Gospel's opening (Douay *And there
  shall be signs*) and the Communion (Douay *For the Lord will give goodness*).
  The Alleluia's verse agrees (Douay Ps 84:8 *Shew us, O Lord, thy mercy; and
  grant us thy salvation*). English must never be composed to fill those
  differences; where the Douay cannot carry the Missal's form, the profile's
  rule is to say so and give the Latin with a description.
- **English, the orations.** Two registered public-domain hand-missal routes
  exist and neither was read on a page image in this stage:
  - the 1945 Benziger revision of Lasance's *New Roman Missal*
    (`edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945`),
    through the English overlay
    `src/sources/inventories/roman-1962-proper-translations-v1.toml`, rows for
    `mass = "advent-1"`: Collect printed p. 103, Secret p. 105, Postcommunion
    p. 106 (IA leaves 103, 105, 106), each `collation_result = "confirmed"` on
    2026-10-21 with verify and publish passages
    `…benziger-revised-1945.{verify,publish}-advent-1--main--{collect,secret,postcommunion}--all--1`
    and the petition-level control
    `passage.catholic-church.missale-romanum.vatican-typica-1962.advent-1-lasance-three-orations-collation-2026-10-21`.
    Lasance prints the conclusions short (*Who livest.*, *Through our Lord.*);
    the overlay supplies no expansion;
  - the 1861 Cummiskey *Roman Missal* for the laity
    (`edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861`),
    `passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.adv-01`,
    under that book's heading *FIRST SUNDAY OF ADVENT*, printed pp. 50-52, over
    the tracked `…temporal-orations-en` payload (states through `inspected`),
    whose record says its correspondence to the 1962 Latin was checked on the
    facsimile's text layer only.
  The English is each edition's own and is used under its own attribution.
- **English, the Epistle: not a lawful route for this study.** The English
  overlay's Epistle row for `advent-1` carries `rights = "project-created"`
  English from a repository translation campaign. The 1962 profile forbids a
  guide to compose, translate, adapt or paraphrase English and requires a
  registered public-domain witness, so that row is excluded from this study.
- **English, the chants and lessons in a hand missal.** Lasance 1945
  (printed pp. 103-106) prints English for all ten elements; the research
  stage read it on page images. Its chant and lesson English follows the Douay
  with the liturgical openings and drops "For" from the Communion; it renders
  neither the Gradual's *notas fac* nor its added *Dómine*
  (propers/verified.md, *English*; research/scope.md 2.4). No overlay row
  covers it.
- **Trinity Preface.** Appointed by rubric (printed p. 293, no. 1082), within
  the registered `…vatican-typica-1962.praefationes` passage. Whether the study
  quotes or only cites the Preface is for research.

No source was registered or retained in this stage. The existing library was
read first; everything fetched was either an already registered artifact
fetched to its registered hash or a live Ordo response whose identity and hash
are written down above. No liturgical owner is imported: the formulary is
printed whole in this leaf's own edition and family, so there is no
shared-formulary Makefile dependency to declare.

Observations about shared records and tools, reported rather than repaired,
because this stage owns no source or tool record:

- No ledger row, passage record or wording collation addresses this
  formulary's five chants or its Gospel (nos. 1, 4-7, 9).
- `tools/tpt calendar-rubrics day` depends on a generated browser-data
  product and refused while that product was absent; the precedence finding
  above was made from the printed rubrics instead. `calendar-days` lists the
  commemoration of St Saturninus as a commemoration of the day without
  ranking it; read with RG 109 and 111 a, it is not made.
- `tools/tpt proper-chronology loci --document
  liturgy/roman-rite/1962/propers/temporal/01-first-sunday-of-advent` resolves
  the Gospel, Lk 21:25-33, as `composition-only`: the corpus gives no date for
  the narrated occasion of the discourse. Whether that is a gap for the
  chronology corpus's owner is for research to judge; this record asserts no
  date.
- `tools/commentary-work-index formulary --calendar roman-1962 --mass
  advent-1` compares 40 loci and lists none: the commentator index holds no
  locus for this formulary. The search for liturgical commentators therefore
  has no finding aid here and must be made directly.

## Remaining verification for research

- Collate every element word for word at 200 and 400 dpi against the 1962 page
  images (PDF 82-84) and against the 1862 antecedent pages at full resolution
  (pp. 1-3), and write `propers/retrieved.txt` and `propers/verified.md` with
  the loci, conclusions and orthographic transformations. Read the 1862
  Communion citation line on the image.
- Establish or record a publication basis for the Latin of the five chants and
  the Gospel, which have no ledger row; for the English of the orations, verify
  the chosen route on its page images.
- Decide the English display for the places where the Douay cannot carry the
  Missal's form (Introit and Offertory, Gradual, Epistle opening and its end
  at v. 14a, Gospel opening, Communion), and test whether a registered or
  registrable historical hand missal prints English for this Mass's chants;
  never compose English to fill a gap.
- Identify, or record the negative result for, the textual source of the
  chants' *qui te exspectant*, the Introit and Offertory's *Ad te levavi*
  without *Domine*, the Gradual's added *Domine* and its *notas fac mihi*
  beside the Introit verse's *demonstra mihi*, and the Communion's *Dominus
  dabit* without *Etenim*. Nothing above asserts an origin for any of them.
  Record compilation history only where a specific fact changes a claim; that
  the Introit, Gradual and Offertory all draw on Ps 24 is recorded as a fact of
  the book and not as evidence of a designed pairing.
- Read each appointed passage in its complete biblical context — Ps 24 whole,
  an alphabetic psalm of trust and petition for guidance and forgiveness, for
  the Introit, Gradual and Offertory; Ps 84 whole, a prayer for restoration
  after a return from captivity, for the Alleluia and the Communion; Rom 13:8-14
  within Rom 12-13, where the summons to wake follows the love that fulfils the
  law (vv. 8-10); Lk 21:25-33 within the discourse of Lk 21:5-36, its occasion
  in the Temple (vv. 5-7), the prophecy of Jerusalem's siege and fall that
  precedes the signs (vv. 20-24), the call to watch and pray that follows
  (vv. 34-36), and Luke's notice of Jesus teaching in the Temple by day
  (vv. 37-38); the prophetic texts the Gospel echoes (for instance Isa 13:10,
  Joel 2:10, Dan 7:13) and the synoptic parallels Mt 24:29-35 and Mk
  13:24-31 — run the passage-by-passage reception sweep, and generate
  `research/chronology.toml` and `research/chronology-annotations.tex` with
  `tools/tpt proper-chronology`. No biblical date is asserted in this record.
  `tools/tpt proper-chronology loci` already resolves every appointed locus
  under the default profile `catholic-comprehensive-v1`: Introit (Ps 24:1-4),
  Epistle (Rom 13:11-14), Gradual (Ps 24:3-4), Alleluia (Ps 84:8), Gospel (Lk
  21:25-33), Offertory (Ps 24:1-3) and Communion (Ps 84:13), each
  `composition-only`; Collect, Secret and Postcommunion carry no Scripture.
  The distinct directly appointed passages, in canonical then verse order, are
  Ps 24:1-3 (Introit antiphon and Offertory; v. 3 again in the Gradual's
  respond), Ps 24:4 (v. 4b, as the Introit verse and the Gradual verse, in two
  wordings), Ps 84:8, Ps 84:13, Lk 21:25-33 and Rom 13:11-14. The research
  stage decides how the chronology record consolidates the repeated Ps 24
  loci; the Introit's printed citation is *Ps. 24, 1-3* with the verse *ibid.,
  4*.
- Search the passage exegetes and the liturgical commentators directly, since
  the commentator index has no locus for this formulary, and identify each
  commentator's Mass by its elements, as the three-document profile requires.
  Leads already in the library, not yet read for this study and supporting no
  claim until read: the Matins lessons of this Sunday in the registered
  Breviary witnesses, among them the seventh lesson from St Gregory the
  Great's first homily on the Gospels on Lk 21:25
  (`passage.catholic-church.breviarium-romanum.blackwood-bute-winter-1908.advent-primer-advent-1-mattins-lesson-7`)
  and the fourth from St Leo the Great's eighth sermon on the December fast
  (`…advent-primer-advent-1-mattins-lesson-4`). A Breviary lesson is the
  Office's use of a Father, not the Mass; research reads the underlying work
  at its own locus.
- Register a dated edition and passage for 29 November 2026 if the study
  relies on either dated Ordo.
- Resolve, only if the study relies on them, the points this stage did not
  settle: the Asperges placement, the generated precedence result once the
  rubrics product exists, and any particular-calendar overlay or local
  observance. None is needed for the universal formulary on this date.
- Bind the controlling sources in `research/source-bindings.toml` and declare
  the external owners actually relied on in `research/review-dependencies.toml`.
  The authorities adopted here are the 1962 facsimile artifact with its
  `temporal-advent-1-orations`, `primary-advent-1-epistle-word-collation-2026-10-20`,
  `advent-1-lasance-three-orations-collation-2026-10-21` and
  `advent-primer-20261119-advent-christmas-stations` passages and the
  expected-target inventory rows `roman-1962.temporal.advent-1` and its slots
  (`src/sources/inventories/missal-expected-targets-v1.toml`), the
  facsimile-rights inventory, the Latin provenance ledger with its
  editorial-projection passages, the 1862 Pustet text artifact and its
  registered scan, the Mame 1922 edition and its Epistle artifact, the
  Clementine Vulgate edition, the Douay-Rheims editions and the
  psalm-numbering concordance, the Lasance and Cummiskey English routes named
  above with the English overlay, and, as computation inputs,
  `src/sources/calendars/roman-1962/propers.yaml` and `rubrics.yaml`.
