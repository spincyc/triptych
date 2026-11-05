# Celebration context and complete appointed inventory

Resolved 5 November 2026 for the `proper-study` v17 production of the Claude
1962 leaf, run `eb621aedbeee828e`, seeded at commit
`2629d99f4848b3be111d792a88a48635cd4edc97`. The production-plan entry of
2026-11-05 in `guidance/liturgy/propers-production-plan.md` (prose paragraph and
the line "Authorized 2026-11-05: provider `claude`, identity
`liturgy/roman-rite/1962/propers/temporal/66-resumed-fifth-after-epiphany`")
authorizes provider `claude` for this one identity and Sunday 8 November 2026,
under the three-document contract, as an independent production that is not a
companion to or derivative of the published GPT leaf for the same identity. It
does not open the ordinary Fifth Sunday after the Epiphany or any other resumed
Sunday. `ARGS.research_handoff` is `none`, so no handoff was supplied. The
other provider's leaf, review records and reader links for this identity, every
postconciliar record, and this provider's neighbouring Sundays are outside this
record's evidence; none was opened and nothing below is taken from them. The
Claude Twenty-first Sunday's context record was read only as a model of this
record's shape; no finding of it is relied on. Provider-neutral library records
under `src/sources/` are used as library evidence and are named where used.
This record settles what is studied. It holds no study prose, spoken text,
timing claim or review verdict; the research stage collates the sources and may
correct it from evidence.

## Publication mode

The section *Reference-only publication scope* of the production plan states
that no reference-only target is currently authorized, and no line of the form
`- Authorized reference-only …` names this provider and identity. This study
is therefore **not** reference-only: the ordinary schema-2 appointed-text mode
applies, with `propers/retrieved.txt` and `propers/verified.md` as a focused
pull and a facsimile-collated transcription under the 1962 profile, and with the
lawful-text and English rules of that profile. Whether every element can be
published complete, or only some (`rights-limited`), is decided by the routes
recorded below and not assumed here.

## Identity, governing books and territory

- Canonical identity:
  `liturgy/roman-rite/1962/propers/temporal/66-resumed-fifth-after-epiphany`,
  catalog ID `66` in the 1962 temporal registry of
  `guidance/liturgy/roman-1962-propers.md`, where `64`-`67` are the resumed
  Third through Sixth Sundays after the Epiphany, each a full identity and not
  a variant. Calendar family `roman-1962`. `tools/check-proper-identity
  --document … --calendar roman-1962` passes. The finding-aid mass index
  `src/sources/calendars/roman-1962/propers.yaml` carries the formulary as
  `resumed-epiphany-5`, `registry: '66'`, season `after-pentecost`, and records
  it by reference (`takes_from` `epiphany-5`; Introit, Gradual, Alleluia,
  Offertory and Communion `takes_from` `pentecost-23`, citing RGMR 298). That
  index is a lead and never the source of record for any wording.
- Distinct neighbouring identities, not studied here: `16`, the Fifth Sunday
  after the Epiphany in its own season, whose orations, Epistle and Gospel are
  the same texts but whose chants are the Epiphany set (*Adorate Deum*, Ps
  96:7-8; Gradual *Timebunt gentes*, Ps 101:16-17; Alleluia Ps 96:1; Offertory
  *Dextera Domini*, Ps 117:16-17; Communion *Mirabantur omnes*, Lk 4:22),
  printed pp. 47-48, nos. 326-335 (PDF 128-129, located on the text layer); and
  `63`, the Twenty-third Sunday after Pentecost, whose chants this formulary
  shares by rubric (pp. 416-417, nos. 1719-1728, PDF 497-498, located). Neither
  formulary's other texts travel into this one.
- Governing edition: *Missale Romanum*, editio typica, Typis Polyglottis
  Vaticanis 1962 (`edition.catholic-church.missale-romanum.vatican-typica-1962`),
  controlled on the page images of
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.
  A copy fetched in this stage (2026-11-05) from the registered `source_url`
  matched the registered SHA-256
  `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` and
  82,815,941 bytes before any page was read. The formulary was read on page
  images rendered from that file at 200 and 400 dpi (PDF 501-502); the rubric
  note closing the Twenty-third Sunday at 300 dpi (PDF 498); the *Calendarium*
  for November (PDF 54), RG 1-19 (PDF 10), RG 96-112 (PDF 16), RGMR 285-300
  (PDF 20) and RGMR 480-503 (PDF 32) at 200 dpi. Printed front-matter pages run
  two ahead of the PDF page (PDF 10 is printed p. XII). The text layer served
  only to locate pages; loci marked "located" were found on it and not re-read
  on an image.
- Printed heading and rank: *DOMINICA QUINTA quae superfuit post Epiphaniam*,
  *II classis*, printed p. 420, foot of the left column (PDF 501). The running
  head of p. 420 reads *Dominica V quae superfuit post Epiphaniam*, although
  most of the page carries the end of the resumed Fourth Sunday; the running
  head of p. 421 (PDF 502) reads *Dominica VI quae superfuit post Epiphaniam*,
  although its left column and the top of its right column carry the rest of
  this formulary. The running heads do not bound the formulary.
- Formulary boundary: it begins under that heading with the Introit, marginal
  no. 1749, immediately after the Postcommunion *Munera tua nos, Deus, a
  delectationibus terrenis expediant* (no. 1748) of the resumed Fourth Sunday,
  and ends with its Postcommunion, no. 1758, at the head of the right column of
  p. 421, after which *DOMINICA SEXTA quae superfuit post Epiphaniam*, II
  classis, opens a different formulary at no. 1759. Marginal nos. 1749-1758,
  each printed whole and legible on these two pages.
- The edition prints this resumed formulary in full in the Proper of Time after
  the Twenty-third Sunday after Pentecost, with its chants written out, not as a
  cross-reference. The rubric note closing the Twenty-third Sunday, printed
  p. 417 right column (PDF 498), read at 300 dpi: *Si dominicae post Pentecosten
  fuerint plures quam XXIV, tunc post XXIII resumuntur Missae dominicarum, quae
  superfuerunt post Epiphaniam, ut infra habentur, iuxta ordinem qui in rubricis
  invenitur. Et ultimo loco semper ponitur Missa dominicae XXIV, ut infra 422.*
- RGMR 298, printed p. XXII (PDF 20), read: *Omnes dominicae, sive I sive II
  classis, propriam Missam habent. Attamen dominicae post Epiphaniam, quae
  transferuntur inter dominicam XXIII et XXIV post Pentecosten, sumunt
  antiphonas ad Introitum, ad Offertorium et ad Communionem, necnon graduale et
  Alleluia cum suo versu a dominica XXIII post Pentecosten, retentis
  orationibus, Epistola et Evangelio propriis.* The printed formulary agrees:
  its five chants are those of the Twenty-third Sunday (nos. 1719, 1722, 1723,
  1725, 1727, located on the text layer of PDF 497-498 in the same words), and
  its orations and lessons are those of the Fifth Sunday after the Epiphany.
- Governing books within that edition, read or located where cited below: the
  *Calendarium*; the *Rubricae generales* (part I of the 1960 code as printed,
  cited RG); the *Rubricae generales Missalis romani* (part III, cited RGMR);
  the *Ordo Missae*; the *Praefationes*; the Proper of Time; the Sanctorale
  (for the calendar commemoration of the day). Part II, the *Rubricae generales
  Breviarii romani*, is not printed in this witness.
- Territory: the universal 1962 General Roman Calendar. No diocese, church
  titular or dedication, religious institute or other particular calendar was
  supplied, so no local overlay is applied or computed. The study concerns the
  universal formulary on this date, not a direction to any particular church.
- Language: Latin governs. Every English route below is a historical study aid,
  not an approved vernacular liturgical text.
- Cycle: the 1962 Missal appoints the readings with the formulary and has no
  Lectionary cycle. No A/B/C or I/II value exists for this record. The
  requested identity and the formulary appointed on the requested date are the
  same (see *Occurrence*), so there is no requested-versus-appointed difference
  to preserve.
- Season: *tempus « per annum »* after Pentecost. Although the formulary is
  named for a Sunday after the Epiphany, it is said in November in the season
  after Pentecost; nothing of Christmastide or Epiphanytide (Preface, colour,
  seasonal rubric) travels with it.
- Homily audience for the later homily stage: adult parish assembly
  (`ARGS.audience`). RGMR 474 (printed p. XXXIII, PDF 31, located) places a
  brief homily after the Gospel, *praesertim in dominicis*; the homily is
  authored preaching and adds no text to this inventory.

## Occurrence on 8 November 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
roman-1962 --date 2026-11-08 --json` returns appointed `resumed-epiphany-5`,
"Fifth Sunday after the Epiphany, resumed after Pentecost", rule "resumption
slot 24 of 26 Sundays after Pentecost", season after Pentecost, no Lectionary
value and nothing unresolved, with a second candidate, the calendar
commemoration `comm-ss-quatuor-coronatorum-martyrum`. The 2026 anchors in
`guidance/liturgy/calendar-computation.md` (its 1962 table gives 2026 `E` = 3,
`P` = 26, three unused Sundays after the Epiphany and two resumption slots)
and in the computed result are: Septuagesima 1 February, Easter 5 April,
Pentecost 24 May, Trinity Sunday 31 May (the first Sunday after Pentecost),
Sunday before Advent 22 November, First Sunday of Advent 29 November;
liturgical year 30 November 2025 - 28 November 2026. Recomputed here: the
Sundays after the Epiphany were 11, 18 and 25 January (the first carrying the
Holy Family), so the Fourth, Fifth and Sixth were impeded by Septuagesima on
1 February; 31 May plus twenty-five weeks is 22 November, so there are 26
Sundays after Pentecost, and 8 November is the twenty-fourth.

**The rubric that places it.** RG 18, printed p. XII (PDF 10), read:
*Dominicae post Epiphaniam quae, superveniente Septuagesima, impediuntur,
transferuntur post dominicam XXIII post Pentecosten, hoc ordine: … b) si
dominicae fuerint 26, dominica XXIV erit quae inscribitur V post Epiphaniam; et
XXV, quae inscribitur VI; … Ultimo tamen loco semper ponitur ea quae in ordine
est XXIV post Pentecosten, omissis, si opus sit, ceteris, quae aliquando locum
habere non possunt.* In 2026, therefore: slot 23, 1 November, the Twenty-third
Sunday (impeded by All Saints, which is not this record's object); slot 24,
8 November, the resumed **Fifth** Sunday after the Epiphany; slot 25,
15 November, the resumed Sixth; slot 26, 22 November, the Twenty-fourth and
last. The Fourth Sunday after the Epiphany finds no place and is omitted this
year under the same clause. RG 14 (same page, read) says the Office and Mass of
an impeded Sunday are neither anticipated nor resumed; RG 18 is the express
provision for these Sundays. RG 10 and 12 (same page, read): Sundays are of I
or II class, and every Sunday not named in RG 11 is of II class, as the printed
heading also says.

**The calendar of the day.** The *Calendarium*, printed p. LII (PDF 54), read:
8 November carries dominical letter *d* and the entry *Commemoratio Ss. Quatuor
Coronatorum Mm., Comm.* — a commemoration only, no feast. The year 2026 begins
on a Thursday, so its dominical letter is *D* and 8 November is a Sunday. The
same page gives 9 November, a Monday in 2026, *In Dedicatione Archibasilicae
Ss.mi Salvatoris, II classis*; it does not touch this Sunday. The commemoration
stands in the Sanctorale under *Die 8 novembris*, *Ss. Quatuor Coronatorum
Martyrum*, *Commemoratio*, printed p. 712 (PDF 793, located), Introit
*Intret in conspectu tuo* no. 4044, Collect *Praesta, quaesumus, omnipotens
Deus: ut, qui gloriosos Martyres* no. 4045.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
roman-1962 --date 2026-11-08 --json` is settled: winner `resumed-epiphany-5`, a
second-class Sunday (RG 12; RG 91 row 15); the commemoration is returned
`omitted` because "a second-class Sunday admits a commemoration of a
second-class feast and of nothing else" (RG 111; RGMR 434 b); the low-Mass and
the sung non-conventual oration lists each hold the Sunday Collect alone. Every
locus that result depends on was checked:

- RG 91, table of precedence, printed p. XVII (PDF 15, located): row 14 *Festa
  Domini II classis*, row 15 *Dominicae II classis*, row 16 II-class feasts of
  the universal Church that are not of the Lord. A calendar commemoration
  occupies no row.
- RG 107-109, printed p. XVIII (PDF 16), read: commemorations are privileged or
  ordinary; the privileged are those of a Sunday, a I-class day, the days
  within the Christmas octave, the September Ember ferias, the Advent, Lent and
  Passiontide ferias and the Greater Litanies; all others, this one included,
  are ordinary (RG 109).
- RG 111, same page, read: *b) in dominicis II classis, una tantum admittitur
  commemoratio, scilicet de festo II classis*; and *a)* in sung non-conventual
  Masses no commemoration save one privileged. The Four Crowned Martyrs are
  neither a II-class feast nor privileged, so at no Mass of this Sunday, low,
  sung or conventual, is their commemoration made. RGMR 434 (printed p. XXXI,
  PDF 29, located) states the same for the orations of the Mass.

The rubrical result has no branch: one formulary, one Collect, one Secret, one
Postcommunion, in every Mass. No other universal feast, vigil, octave, Ember
day or seasonal substitution falls on the date. Green vestments follow RG 127
b, printed p. XX (PDF 18, located): *a feria II post dominicam I post
Pentecosten, usque ad sabbatum ante Adventum*. No oration is added by universal
rubric on this date (the RGMR 453 mission oration belongs to October). Orations
added by local fact are not computed: an *oratio imperata* (RGMR 454-457,
located), which RGMR 457 forbids on I- and II-class days in any case, and the
oration for a diocesan bishop's anniversary (RGMR 449, located). RGMR 461
(printed p. XXXIII, located) permits the *oratio votiva ad libitum* only in low
Masses of IV-class days, so none is added. Whether any church keeps an external
solemnity or a II-class votive Mass on this Sunday is local and not computed;
none alters the Sunday's formulary, which remains the object of study.

**Dated official witnesses.** Two dated Ordos of institutes that celebrate with
the 1962 books were read live for this date. Neither response is retained or
registered, and neither changes any registration; both are held only in this
run's scratch area. Their SHA-256 values are recorded so that the research
stage can register a dated edition and passage if it relies on them. (The
research stage, iteration 1, re-hashed both responses, registered each as a
dated edition with a passage for 8 November 2026, and bound both passages;
research/scope.md section 1.)

- FSSP France, *Ordo du mois*, <https://www.fssp.fr/ordo-du-mois/>, read
  2026-11-05, response 165,240 bytes, SHA-256
  `446c71a417e11b3bafeab169a7d6e65d24c902b321d9543cffa0f3bce1c01608`:
  *Dimanche 8 novembre* — *5e dimanche après l'Épiphanie (transféré) (2ème
  classe, Vert)*; also *Dimanche 15 novembre* — *6e dimanche après l'Épiphanie
  (transféré)*, and *Lundi 9 novembre* — the Lateran dedication, II class. The
  Ordo prints one line per day; it names no commemoration for 8 November, and
  that silence is not read as evidence either way.
- ICRSP France, *Ordo*, <https://icrspfrance.fr/ordo.php?d=2026-11-01>, read
  2026-11-05, response 110,141 bytes, SHA-256
  `2827905d3ba86d9fc4ae6fff09c7f89c60c8ee13a9d439c87893ccdb764a05a8`:
  *dimanche 8 novembre 2026* — *XXIVᵉ Dimanche après la Pentecôte (3ᵉ de nov.,
  5ᵉ après l'Épiph.)*, *Temps Per Annum*, II class, green; Gloria, Credo,
  Trinity Preface; no *Mémoires* listed; Mass *Messe propre (Dicit Dominus)*,
  *Gloria. Or. pro Papa. Credo. Préf. de la T. Ste Trinité*; at Matins, lessons
  of the third Sunday of November and the homily of the Fifth Sunday after the
  Epiphany; note *La IIe semaine de novembre est toujours omise*.

Computation, the printed rubric and calendar, and both dated witnesses agree on
the identity, the twenty-fourth place after Pentecost, the second class and the
green colour; the ICRSP entry also names the Mass by its Introit *Dicit
Dominus*, which is the resumed formulary and not the Epiphany-season one, gives
the Trinity Preface, and carries no commemoration. Nothing fails closed. Two
things in that witness are its own and are not imported. Its numbering of the
Sunday as the third of November, and its note that the second week of November
is omitted, belong to the Breviary's reckoning of the Office's Scripture
lessons; RG 19 (printed pp. XII-XIII, read on PDF 10, continuation located on
PDF 11) counts the first Sunday of November as the one falling on the 1st to
7th, here 1 November. Its *Oratio pro Papa* is an institute observance whose
basis was not examined and which the books do not appoint on this date. This
record follows the books.

## Appointed proper

Every element is required and none has an alternative within the formulary:
the pages print no option, no choice and no substitute. Loci are the printed
page and marginal number of the controlling edition, read on 200- and 400-dpi
page images of artifact PDF pp. 501-502. Psalms are cited in the Missal's
Vulgate numbering, with the Hebrew number of the repository's psalm concordance
(`…/challoner-gutenberg-1581/artifacts/psalm-numbering-ee3c7757/psalm-numbering.tsv`,
SHA-256 `535761886df2…` recomputed and matched) in parentheses. That concordance
gives English verse offsets of one for Pss 43 and 84 (Vg. 43:8-9 is English
44:7-8; Vg. 84:2 is English 85:1, the inscription being v. 1 in the Vulgate)
and zero for Ps 129.

| Order and key | Element and printed locus | Liturgical place, extent and boundary |
|---|---|---|
| 1 `introit` | *Antiphona ad Introitum* *Dicit Dominus: Ego cogito cogitationes pacis*, printed citation *Ierem. 29, 11, 12 et 14*; verse Ps 84:2 (85:2); p. 420 left column, no. 1749 | Entrance chant (RGMR 427, p. XXXI): antiphon *Dicit Dominus: Ego cogito cogitationes pacis, et non afflictionis: invocabitis me, et ego exaudiam vos: et reducam captivitatem vestram de cunctis locis*; psalm verse *Benedixisti, Domine, terram tuam: avertisti captivitatem Iacob*; printed cue *V. Gloria Patri*; repetition. Chant of the Twenty-third Sunday (RGMR 298). |
| 2 `collect` | *Oratio* *Familiam tuam, quaesumus, Domine, continua pietate custodi*; p. 420 right column, no. 1750 | First and only oration of the Mass (RGMR 433; RG 111 b). Asks that the family that leans on the hope of heavenly grace alone be defended by God's protection. Printed conclusion in full: *Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.* Not to be confused with the Twenty-first Sunday's Collect of the same incipit, which continues *ut a cunctis adversitatibus*. |
| 3 `epistle` | Col 3:12-17; p. 420 right column, no. 1751 | *Lectio Epistolae beati Pauli Apostoli ad Colossenses*. Opens *Fratres: Induite vos sicut electi Dei*; ends at v. 17, *gratias agentes Deo et Patri per Iesum Christum Dominum nostrum*. No shorter form. |
| 4 `gradual` | Ps 43:8-9 (44:8-9); p. 420 right column, no. 1752 | After the Epistle (RGMR 469, located): respond *Liberasti nos, Domine, ex affligentibus nos: et eos, qui nos oderunt, confudisti*; verse *In Deo laudabimur tota die, et in nomine tuo confitebimur in saecula*. Chant of the Twenty-third Sunday. |
| 5 `alleluia` | Ps 129:1-2 (130:1-2); p. 420 right column, no. 1753 | *Alleluia, alleluia* with verse *De profundis clamavi ad te, Domine: Domine, exaudi orationem meam*, then *Alleluia*. No Tract and no Sequence. Chant of the Twenty-third Sunday. |
| 6 `gospel` | Mt 13:24-30; p. 421 left column, no. 1754 | *Sequentia sancti Evangelii secundum Matthaeum*. Opens *In illo tempore: Dixit Iesus turbis parabolam hanc: Simile factum est regnum caelorum homini, qui seminavit bonum semen in agro suo*; ends at v. 30, *triticum autem congregate in horreum meum*. Printed cue *Credo.* follows. No shorter form; the parable's explanation (Mt 13:36-43) is not appointed. |
| 7 `offertory` | *Ant. ad Offertorium* Ps 129:1-2 (130:1-2); p. 421 left column, no. 1755 | *De profundis clamavi ad te, Domine: Domine, exaudi orationem meam: de profundis clamavi ad te, Domine.* The same psalm verses as the Alleluia, with the first line repeated. Chant of the Twenty-third Sunday. |
| 8 `secret` | *Secreta* *Hostias tibi, Domine, placationis offerimus*; p. 421 left column, no. 1756 | Said secretly (RGMR 480-481, read). Asks that God, receiving the offering of propitiation, absolve sins and direct wavering hearts (*nutantia corda tu dirigas*). Printed conclusion *Per Dominum.* Followed by the printed direction *Praefatio de Ssma Trinitate.* |
| 9 `communion` | *Ant. ad Communionem* Mk 11:24, printed *Marc. 11, 24*; p. 421 left column, no. 1757 | After the Communion rites (RGMR 504, located): *Amen dico vobis, quidquid orantes petitis, credite quia accipietis, et fiet vobis.* Chant of the Twenty-third Sunday. |
| 10 `postcommunion` | *Postcommunio* *Quaesumus, omnipotens Deus: ut illius salutaris capiamus effectum*; p. 421 right column, no. 1758 | Asks that the effect of the salvation whose pledge was received in these mysteries be obtained. Printed conclusion *Per Dominum.* (RGMR 505, located). |

Setting variables observed on the page images, not textual differences: this
formulary sets *Antiphona ad Introitum* in full but *Ant. ad Offertorium* and
*Ant. ad Communionem* abbreviated; the Collect prints its conclusion in full and
the Secret and Postcommunion print *Per Dominum.* The Epiphany-season printing
of the same Postcommunion (identity `16`, p. 48, no. 335) carries the expanded
conclusion according to the Latin provenance ledger, and the finding aid's
resolved text carries that expanded conclusion too; the resumed printing at
no. 1758 prints the short cue. The study's Latin follows the printing it
reproduces, and the research stage records which.

The formulary prints no Tract, Sequence, prophecy, proper *Communicantes* or
*Hanc igitur* (RGMR 501, read: such variations are noted in the proper Mass,
and none is noted here), *Oratio super populum*, second or third oration of its
own, blessing, or alternative reading. The 1862 antecedent's second and third
orations *ad poscenda suffragia Sanctorum* and *ad libitum* belong to the
pre-1960 rubrics and are not part of the 1962 formulary.

### Wording against the Clementine Vulgate

The comparisons below were made against the tracked Clementine Vulgate
(`edition.catholic-church.vulgata-clementina.ebible-latvuc`, its verse-text
artifacts) through `tools/tpt mass-propers show --calendar roman-1962 --mass
resumed-epiphany-5 --bible clementine-vulgate`, with the Epistle and Gospel
compared token by token by script against a reading of the 400-dpi page
images, after normalising i/j, ligatures and accents and ignoring pointing.
They are textual observations about wording and boundary. Whether a chant
follows an older Latin text, and which, is left to research, and no origin is
asserted here.

- **Introit.** The antiphon is not a continuous Vulgate text. The Clementine at
  Jer 29:11 reads *Ego enim scio cogitationes quas ego cogito super vos, ait
  Dominus, cogitationes pacis et non afflictionis, ut dem vobis finem et
  patientiam*; v. 12 *Et invocabitis me, et ibitis: et orabitis me, et ego
  exaudiam vos*; v. 14 *et reducam captivitatem vestram, et congregabo vos de
  universis gentibus et de cunctis locis ad quae expuli vos …*. The Missal opens
  *Dicit Dominus: Ego cogito cogitationes pacis*, has nothing of *ut dem vobis
  finem et patientiam*, *et ibitis: et orabitis me*, v. 13, or *et congregabo
  vos de universis gentibus*, and joins *reducam captivitatem vestram* directly
  to *de cunctis locis*. The psalm verse agrees with Ps 84:2.
- **Epistle.** The Missal reads *Fratres: Induite vos sicut* where the
  Clementine opens v. 12 *Induite vos ergo, sicut*, and ends v. 17 *per Iesum
  Christum Dominum nostrum* where the Clementine reads *per ipsum*. Every other
  word of vv. 12-17 agrees.
- **Gradual.** The Missal reads *Liberasti nos, Domine, ex affligentibus nos:
  et eos, qui nos oderunt, confudisti* where the Clementine at Ps 43:8 reads
  *salvasti enim nos de affligentibus nos, et odientes nos confudisti*, and *in
  saecula* where v. 9 reads *in saeculum*.
- **Alleluia and Offertory.** Both read *Domine, exaudi orationem meam* where
  the Clementine at Ps 129:2 reads *Domine, exaudi vocem meam*; both stop before
  v. 2b and omit the title *Canticum graduum*. The Offertory repeats its first
  line at the end.
- **Gospel.** The liturgical opening *In illo tempore: Dixit Iesus turbis
  parabolam hanc:* stands for the Clementine's *Aliam parabolam proposuit
  illis, dicens:* at the head of v. 24. Every other word of vv. 24-30 agrees.
- **Communion.** The Missal reads *Amen dico vobis, quidquid orantes petitis …
  et fiet vobis* where the Clementine at Mk 11:24 reads *Propterea dico vobis,
  omnia quaecumque orantes petitis … et evenient vobis*; *credite quia
  accipietis* agrees.

## Other text-bearing parts of this Mass

These are fixed or rubrically appointed texts of the 1962 *Ordo Missae*,
*Praefationes* and appendix, not proper text. The study refers to them and does
not reproduce the Ordinary. RGMR 425-431 (PDF 29), 474-475 (PDF 31) and
507-510 (PDF 33) were located on the text layer; RGMR 480-483, 494 and 500-501
were read on the page image (PDF 32). The Trinity Preface (printed p. 293,
no. 1082) and the *Ordo Missae* numbers below were not re-read in this stage;
they are cited from the registered passage records
`…vatican-typica-1962.ordo-missae-ad-gradum`, `…ordo-missae-kyrie-gloria`,
`…ordo-missae-credo`, `…ordo-missae-conclusio` and `…praefationes`, which the
research stage confirms before relying on them.

| Place | Text and appointment | Status and source |
|---|---|---|
| Before the principal Mass, where used | *Asperges me* with the Sunday blessing of water, appendix | A Sunday rite outside the Mass and outside this formulary; not part of the appointed inventory. |
| Prayers at the foot of the altar | Ps 42 *Iudica me* through *Oramus te* | Said: RGMR 425 omits *Iudica* only from Passion Sunday to Maundy Thursday and in Requiem Masses. |
| Introit doxology; Kyrie | *Gloria Patri*; ninefold Kyrie | RGMR 427-428, 430; the Introit's printed *V. Gloria Patri* cue at no. 1749. |
| After the Kyrie | *Gloria in excelsis* | Said: RGMR 431 a ties it to the Office's Te Deum at Matins, a Breviary rubric this Missal omits; the ICRSP dated entry carries the Gloria for this date, an unadopted lead. No chant setting is chosen. |
| Before and after the Gospel | *Munda cor meum*, Gospel dialogue; homily | RGMR 471, 474. |
| After the Gospel or homily | *Credo* | Said: RGMR 475 a, *in qualibet dominica*; printed cue after no. 1754. |
| After the Secret | *Praefatio de Ss.ma Trinitate* | Appointed, not chosen: printed direction after no. 1756 and RGMR 494 b, *tamquam de Tempore … in omnibus dominicis II classis, extra tempus natalicium et paschale* (p. XXXIV, PDF 32, read). Neither the Epiphany Preface (RGMR 485, read: only the Epiphany, the Baptism and 7-13 January) nor any other applies. |
| Canon | *Te igitur* through the doxology | The one Roman Canon, said secretly (RGMR 500, read). No alternative Eucharistic Prayer and no proper insertion for this day (RGMR 501, read). |
| Conclusion | *Ite, missa est*, *Placeat*, blessing, last Gospel Jn 1:1-14 | RGMR 507-509; none of the omission cases of RGMR 510 applies. |

## Lawful study-text routes

- **Latin, the three orations.** Control: the 1962 page images above.
  Publication basis: 17 U.S.C. 103(b) with a public-domain antecedent, as
  settled for the repository in
  `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`. The
  Latin provenance ledger
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` carries
  collated `publication_status = "permitted"` rows for `mass = "epiphany-5"`
  Collect, Secret and Postcommunion, verified against
  `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-epiphany-5-orations`
  at the **Epiphany-season** printing (pp. 47-48, nos. 327, 333, 335) and
  publishing on the tracked 1862 text layer
  (`artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`,
  SHA-256 `f34bc7cf9293…` recomputed and matched) at fol. 42-44, physical lines
  18021-18026, 18147-18151 and 18178-18183. No ledger row, passage record or
  expected-target verification addresses the resumed printing at nos. 1750,
  1756 and 1758; the expected-target inventory
  (`src/sources/inventories/missal-expected-targets-v1.toml`,
  `roman-1962.temporal.resumed-epiphany-5:*`) locates its slots at PDF 501-502
  without a wording collation. On the page images read here, the resumed
  printing's words agree with the ledger's Collect and Secret; its
  Postcommunion differs only by the short conclusion noted above.
- **Latin, the five chants.** The ledger carries no row for the Introit,
  Gradual, Alleluia, Offertory or Communion of this formulary or of
  `pentecost-23`, whose chants they are. A public-domain antecedent is located
  in the same 1862 text layer under *Dominica XXIII post Pentecosten*, printed
  pp. 357-358: Introit lines 52511-52524, Gradual 52577-52584, Alleluia
  52585-52597, Offertory 52634-52638, Communion 52655-52658. On the text layer
  these agree in words with the 1962, including every divergence from the
  Clementine listed above (*Dicit Dominus … de cunctis locis*, *Liberasti nos*,
  *in saecula*, *orationem meam*, *Amen dico vobis, quidquid … et fiet
  vobis*), apart from orthography, pointing and citation form (*Jeremiae 29.*,
  *Ps. 84.*, *Ps. 43.*, *Ps. 129.*, *Marci 11.*). That is a text-layer reading,
  not a page-image collation. The same 1862 pages carry, after the Twenty-third
  Sunday, its rubric for the resumed Sundays (printed pp. 358-359, lines
  52671-52727): the Masses of the Sundays left over after the Epiphany are
  resumed *quoad Orationes, Epistolas et Evangelia*, with the order for 25-28
  Sundays, and *Introitus autem, Graduale, Offertorium, et Communio in
  praedictis Dominicis semper dicuntur ut in Dominica vigesimatertia*. The 1862
  prints no resumed formulary of its own; it refers to the Epiphany-season one.
- **Latin, the two lessons.** The ledger carries no row for this Epistle or
  Gospel. The 1862 Epiphany-season formulary *Dominica V. post Epiphaniam*
  prints them at fol. 43 (Epistle lines 18066-18095; Gospel lines
  18105-18138), on the text layer in the 1962's words, including *Fratres.
  Induite vos sicut electi Dei*, *per Jesum Christum Dominum nostrum* and the
  liturgical Gospel opening *Dixit Jesus turbis parabolam hanc*. Text layer
  only. The registered 1862 scan
  (`artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.ia-facsimile-pdf-363d6fc3`)
  was not fetched in this stage.
- **English, canonical Scripture.** The Douay-Rheims (Challoner) as registered
  (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  with `…american-1899-ebible` as the other registered Douay printing), read at
  the Vulgate loci through `tools/tpt mass-propers show … --bible
  douay-rheims`, which resolves the Missal's Vulgate psalm numbering. Its
  canonical verses are **not** the Missal's wording at the Introit (Douay Jer
  29:11-14 *For I know the thoughts that I think towards you, saith the Lord …
  and I will bring back your captivity, and I will gather you out of all
  nations, and from all the places*), the Epistle's liturgical address and
  close (Douay *Put ye on therefore … by him*), the Gradual (Douay *But thou
  hast saved us from them that afflict us … for ever*), the Alleluia and
  Offertory (Douay *Lord, hear my voice*), the Gospel's opening (Douay *Another
  parable he proposed to them*) and the Communion (Douay *Therefore I say unto
  you, all things, whatsoever you ask … and they shall come unto you*). English
  must never be composed to fill those differences; where the Douay cannot
  carry the Missal's form, the profile's rule is to say so and give the Latin
  with a description.
- **English, the orations.** Two registered public-domain hand-missal routes
  exist and neither was read on a page image in this stage:
  - the 1945 Benziger revision of Lasance's *New Roman Missal*
    (`edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945`),
    through the English overlay
    `src/sources/inventories/roman-1962-proper-translations-v1.toml`, rows for
    `mass = "epiphany-5"`: Collect printed p. 196 and Postcommunion p. 198
    (passages `…resume-orations-phase2-2026-10-23-publish-epiphany-5--main--collect--all--1`
    and `…--postcommunion--all--1`), Secret printed p. 746 under that book's
    "Supplementary Mass No. 3" (passage
    `…publish-phase4-en31-epiphany-5--main--secret--all--1`), the record
    stating that it is a historical prayer and not a recipient appointment;
    the relation of Lasance's supplementary Masses to the resumed Sundays is
    unestablished and is for research;
  - the 1861 Cummiskey *Roman Missal* for the laity
    (`edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861`),
    `passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.epiph-05`
    under *V. SUNDAY AFTER EPIPHANY*, printed pp. 101-102, over the tracked
    `…temporal-orations-en` payload (states through `inspected`), with a
    verified Postcommunion row
    (`…publish-epiph-05-postcommunion`). Its record quotes the 1861 book's own
    rubric at p. 101 that omitted Sundays are *taken in between the XXIII. and
    the last Sunday after Pentecost*.
  Both books print the orations of the Epiphany-season Mass; the English is
  that edition's own and is used under its own attribution.
- **Trinity Preface.** Appointed by rubric (p. 293, no. 1082), within the
  registered `…vatican-typica-1962.praefationes` passage. Whether the study
  quotes or only cites the Preface is for research.

No source was registered or retained in this stage. The existing library was
read first; everything fetched was either an already registered artifact
fetched to its registered hash or a live Ordo response whose identity and hash
are written down above. No liturgical owner is imported: the formulary is
printed whole in this leaf's own edition and family, and identities `16` and
`63` are not imported as owners, so there is no shared-formulary Makefile
dependency to declare.

Observations about shared records, reported rather than repaired, because this
stage owns no source or tool record:

- The finding aid resolves this Mass's Postcommunion through `epiphany-5` with
  the expanded conclusion of the Epiphany-season printing, while the resumed
  printing at no. 1758 prints *Per Dominum.*; nothing records that the 1962
  prints the oration twice at two conclusion lengths.
- No ledger row, passage record or wording collation addresses the resumed
  printing nos. 1749-1758, and no ledger row covers the chants of
  `pentecost-23` or the Epistle and Gospel of `epiphany-5`.

## Remaining verification for research

- Collate every element word for word at 200 and 400 dpi against the 1962 page
  images (PDF 501-502) and against the 1862 antecedent pages at full resolution
  (fol. 42-44 for the orations and lessons; pp. 357-358 for the chants), and
  write `propers/retrieved.txt` and `propers/verified.md` with the loci,
  conclusions and orthographic transformations. Decide and record whether the
  study's Latin follows the resumed printing or the Epiphany-season printing
  where they differ (the Postcommunion's conclusion length).
- Establish or record a publication basis for the Latin of the five chants and
  the two lessons, which have no ledger row; and for the English of the
  orations, verify the chosen route on its page images.
- Decide the English display for the places where the Douay cannot carry the
  Missal's form (Introit, Epistle opening and close, Gradual, Alleluia,
  Offertory, Gospel opening, Communion), and test whether any registered
  historical hand missal prints English for this resumed Mass's chants; never
  compose English to fill a gap.
- Identify, or record the negative result for, the textual source of the
  Introit's Jeremiah cento, the Gradual's *Liberasti nos … in saecula*, the
  *orationem meam* of the Alleluia and Offertory, and the Communion's *Amen dico
  vobis, quidquid … fiet vobis*. Nothing above asserts an origin for any of
  them. Record compilation history only where a specific fact changes a claim;
  the RGMR 298 and 1862 rubrics above are the documented assignment of the
  chants, recorded as facts and not as evidence of a designed pairing.
- Read each appointed passage in its complete biblical context — Jer 29:1-14
  (the letter to the exiles in Babylon) for the Introit, with Ps 84 whole for
  its verse; Col 3:1-17 within the letter; Ps 43 whole, a communal lament whose
  remembered deliverance (vv. 2-9) precedes the complaint of vv. 10-26; Ps 129
  whole; Mt 13:24-30 with the parable chapter around it and its explanation at
  Mt 13:36-43, which the liturgy does not appoint; Mk 11:20-25, where the
  saying on prayer is joined to forgiveness — run the passage-by-passage
  reception sweep, and generate `research/chronology.toml` and
  `research/chronology-annotations.tex` with `tools/tpt proper-chronology`. No
  biblical date is asserted in this record. `tools/tpt proper-chronology loci`
  already resolves every appointed locus under the default profile
  `catholic-comprehensive-v1`: Introit (Jer 29:11, 29:12, 29:14, Ps 84:2),
  Epistle (Col 3:12-17), Gradual (Ps 43:8-9), Alleluia and Offertory (Ps
  129:1-2), Gospel (Mt 13:24-30) and Communion (Mk 11:24), each
  `composition-only`; Collect, Secret and Postcommunion carry no Scripture. The
  distinct directly appointed passages, in canonical then verse order, are Ps
  43:8-9, Ps 84:2, Ps 129:1-2 (appointed twice, at the Alleluia and the
  Offertory), Jer 29:11-12, 14, Mt 13:24-30, Mk 11:24 and Col 3:12-17.
- Identify each liturgical commentator's Mass by its elements, as the
  three-document profile requires. A commentator's "Fifth Sunday after the
  Epiphany" will ordinarily carry the Epiphany-season chants, and his
  Twenty-third or Twenty-fourth Sunday after Pentecost the *Dicit Dominus*
  chants with another Epistle and Gospel; neither is this formulary as a whole,
  and each is evidence only for the elements it shares with it.
- Register a dated edition and passage for 8 November 2026 if the study relies
  on either dated Ordo.
- Resolve, only if the study relies on them, the points this stage did not
  settle: the Breviary's Te Deum rubric behind the Gloria, the Asperges
  placement, and any particular-calendar overlay or local external solemnity.
  None is needed for the universal formulary on this date.
- Bind the controlling sources in `research/source-bindings.toml` and declare
  the external owners actually relied on in `research/review-dependencies.toml`.
  The authorities adopted here are the 1962 facsimile artifact with its
  `temporal-epiphany-5-orations` passage and the expected-target inventory rows
  for `resumed-epiphany-5`, the facsimile-rights inventory, the Latin provenance
  ledger, the 1862 Pustet text artifact and its registered scan, the
  Clementine Vulgate edition, the Douay-Rheims editions and the psalm-numbering
  concordance, the Lasance and Cummiskey English routes named above with the
  English overlay, and, as computation inputs,
  `src/sources/calendars/roman-1962/propers.yaml` and `rubrics.yaml`.
