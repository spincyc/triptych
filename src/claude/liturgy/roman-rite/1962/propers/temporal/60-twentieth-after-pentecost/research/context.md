# Celebration context and complete appointed inventory

Resolved 7 October 2026 for the `proper-study` v9 production of the Claude
1962 leaf, run `9c1136f1f8d1241c`, seeded at commit
`1fa591a03c11d064c9f1afda6c44ccdbe7903bf2`. The production-plan entry of
2026-10-07 in `guidance/liturgy/propers-production-plan.md` authorizes provider
`claude` for this one identity and Sunday 11 October 2026, as an independent
production that is not a companion to or derivative of any other leaf, the GPT
leaf for the same identity included. `ARGS.research_handoff` is `none`, so no
handoff was supplied. The other provider's leaf for this identity, every
postconciliar record, and this provider's neighbouring Sundays are outside this
record's evidence; none was opened and nothing below is taken from them. Several
provider-neutral library records were registered on 2026-10-05 in the course of
that other production (the 1862 page extraction, the Cummiskey and Lasance
checked English, and a dated FSSP Ordo passage, each named below); they are used
here only as library evidence, and the pages behind them were read afresh in
this stage rather than taken on their recorded verification. This record
settles what is studied. It holds no study prose, spoken text, timing claim or
review verdict; the research stage collates the sources and may correct it from
evidence.

## Identity, governing books and territory

- Canonical identity:
  `liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost`,
  catalog ID `60` in the 1962 temporal registry of
  `guidance/liturgy/roman-1962-propers.md` (IDs 41-63 run from the Second
  Sunday after Pentecost, with the Sacred Heart at 42, to the Twenty-third
  Sunday). Calendar family `roman-1962`. `tools/check-proper-identity
  --document … --calendar roman-1962` passes. The finding-aid mass index
  `src/sources/calendars/roman-1962/propers.yaml` carries the formulary as
  `pentecost-20`, `registry: '60'`; that index is a lead and never the source
  of record for any wording.
- Governing edition: *Missale Romanum*, editio typica, Typis Polyglottis
  Vaticanis 1962 (`edition.catholic-church.missale-romanum.vatican-typica-1962`),
  controlled on the page images of
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.
  A copy fetched in this stage from the registered `source_url` matched the
  registered SHA-256
  `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` and
  82,815,941 bytes before any page was read. The formulary was read on page
  images rendered from that file at 200 and 400 dpi, the commemorated
  formulary, the *Calendarium* and the rubrics at 200 dpi; the text layer
  served only to locate pages.
- Printed heading and rank: *DOMINICA VIGESIMA post Pentecosten*, *II
  classis*, Proper of Time, printed p. 412 right column (artifact PDF p. 493).
  The running head of p. 412 reads *Dominica XX post Pentecosten*, although its
  left column still carries the end of the Nineteenth Sunday; the running head
  of p. 413, which carries most of this formulary, reads *Dominica XXI post
  Pentecosten*, because the Twenty-first Sunday begins in its right column. The
  running heads do not bound the formulary.
- Formulary boundary: it begins at marginal no. 1689 in the right column of
  p. 412, immediately after the Postcommunion *Tua nos, Domine, medicinalis
  operatio* (no. 1688) of the Nineteenth Sunday, and ends with its own
  Postcommunion, no. 1698, in the right column of p. 413 (artifact PDF p. 494),
  after which the heading *DOMINICA VIGESIMA PRIMA post Pentecosten*, II
  classis, opens a different formulary at no. 1699. Marginal nos. 1689-1698,
  each printed whole and legible on these two pages.
- Governing books within that edition, read where cited below: the
  *Calendarium*; the *Rubricae generales* (part I of the 1960 code as printed,
  cited RG); the *Rubricae generales Missalis romani* (part III, cited RGMR);
  the *Ordo Missae*; the *Praefationes*; the Sanctorale (for the commemorated
  feast); the appendix *Ordo ad faciendam et aspergendam aquam benedictam*.
  Part II, the *Rubricae generales Breviarii romani* (nn. 138-268), is printed
  only as a heading marked *Hic omittuntur.* on printed p. XX (PDF 18) and is
  not available in this witness.
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

## Occurrence on 11 October 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
roman-1962 --date 2026-10-11 --json` returns candidate `pentecost-20`, "slot 20
of 26 Sundays after Pentecost", season after Pentecost, no Lectionary value and
nothing unresolved, and a second candidate, the fixed-date Marian entry
`maternitatis-beatae-mariae-virginis`, II class. The anchors are those
tabulated in `guidance/liturgy/calendar-computation.md` for 2026: Easter 5
April, Pentecost 24 May, Trinity Sunday 31 May (the first Sunday after
Pentecost), First Sunday of Advent 29 November; liturgical year 30 November
2025 - 28 November 2026. Thirty-one May plus nineteen weeks is 11 October, the
twentieth Sunday of the run. With `P = 26` for 2026 the resumed Sundays after
the Epiphany occupy slots 24 and 25 (RG 18 b, printed p. XII, PDF 10, read),
and the resumption mechanism does not reach slot 20. As an independent check,
the *Calendarium* (printed p. LI, PDF 53, read) gives 11 October the dominical
letter *d*, and 2026, beginning on a Thursday, has *D* as its dominical letter.
Under RG 19 (printed pp. XII-XIII) the first Sunday of a month falls on its
first to seventh day, so 11 October 2026 is the second Sunday of October, not
the first.

**The occurring feast.** The *Calendarium*, printed p. LI, gives 11 October as
*Maternitatis B. Mariae Virg., II classis*. Its formulary stands in the
Sanctorale under *Die 11 octobris*, *MATERNITATIS BEATAE MARIAE VIRGINIS*, *II
classis*, printed pp. 685-686, nos. 3846-3857 (PDF 766-767), read on the page
images: Introit *Ecce Virgo concipiet* no. 3846; Collect *Deus, qui de beatae
Mariae Virginis utero Verbum tuum* no. 3847; Lesson Ecclus 24:23-31 no. 3848;
Gradual no. 3849; Alleluia no. 3850 (Tract no. 3851, paschal Alleluia no.
3852); Gospel Lk 2:43-51 no. 3853; Offertory no. 3854; Secret *Tua, Domine,
propitiatione* no. 3855, followed by the direction *Praefatio de B. Maria
Virg. Et te in festivitate*; Communion no. 3856; Postcommunion *Haec nos
communio, Domine, purget a crimine* no. 3857. The Collect, Secret and
Postcommunion each print the conclusion *Per eundem Dominum* (the Collect in
full, *Per eundem Dominum nostrum Iesum Christum Filium tuum: Qui tecum vivit
et regnat in unitate.*), which is RG 115 b's form for a prayer naming the Son
at its opening (printed p. XIX, PDF 17, read).

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
roman-1962 --date 2026-10-11 --json` is settled: winner `pentecost-20`, a
second-class Sunday (RG 12; RG 91 row 15); the Maternity is returned
`commemorated` as an ordinary commemoration (RG 109) of a row-16 feast; the
low-Mass oration list holds the Sunday Collect and a second collect of the
Maternity "with a second conclusion", and the sung non-conventual list holds
the Sunday Collect alone. Every locus the computation cites, and the further
loci its result depends on, were read on the page images in this stage:

- RG 10 and 12, printed p. XII (PDF 10): Sundays are of I or II class, and
  every Sunday not named in RG 11 is of II class; this Sunday is not named
  there. RG 16 (same page): a II-class Sunday is preferred in occurrence to
  II-class feasts, save a feast of the Lord (16 a). The Maternity is a feast of
  the Blessed Virgin, not of the Lord.
- RG 91, table of precedence, printed pp. XVI-XVII (PDF 14-15): row 15
  *Dominicae II classis*; row 16 *Festa II classis Ecclesiae universae, quae
  non sunt Domini*. Row 12, first-class *propria*, outranks a II-class Sunday
  only in a particular church, an overlay not applied here.
- RG 94-95, printed p. XVII (PDF 15): a commemoration fixed to its day is not
  transferred; a feast other than I class that is accidentally impeded is
  commemorated or, that year, omitted, according to the rubrics. The Maternity
  is therefore neither transferred nor celebrated on another day.
- RG 107-109, printed p. XVIII (PDF 16): commemorations are privileged or
  ordinary; privileged are those of a Sunday, a I-class day, the days within
  the Christmas octave, the September Ember ferias, the Advent, Lent and
  Passiontide ferias, and the Greater Litanies; all others, this one included,
  are ordinary. RG 108: ordinary commemorations are made only at Lauds, in
  conventual Masses and in all low Masses (*in omnibus Missis lectis*).
- RG 111, printed p. XVIII: (a) on I-class days and *in Missis in cantu non
  conventualibus* no commemoration is admitted save one privileged; (b) *in
  dominicis II classis* one commemoration only, of a II-class feast. RGMR 434
  a and b, printed p. XXXI (PDF 29), state the same for the orations of the
  Mass. RG 114 (p. XIX) and RGMR 435 omit any commemoration beyond the number
  allowed.
- RGMR 437 a, printed p. XXXI: commemorations are always said under a
  separate conclusion. RGMR 480 and 505, printed pp. XXXIV-XXXV (PDF 32-33):
  as many Secrets and Postcommunions as orations at the beginning, in the same
  order and manner.
- RGMR 483, printed p. XXXIV (PDF 32): *Nulla commemoratio, in Missa occurrens,
  praefationem propriam inducit.* The Maternity's Marian Preface is therefore
  not taken in the Sunday Mass.
- RGMR 461, printed p. XXXIII (PDF 31): the *oratio votiva ad libitum* is
  permitted only on IV-class days, so none is added.

The rubrical result for this date is a branch by kind of Mass, not by choice:

- **Low Mass, and any conventual Mass:** the Sunday Mass with the commemoration
  of the Maternity. Two Collects (the Sunday's *Largire* under its own
  conclusion, then the Maternity's *Deus, qui de beatae Mariae Virginis utero*
  under a separate conclusion), two Secrets (*Caelestem nobis* and *Tua,
  Domine, propitiatione*) and two Postcommunions (*Ut sacris* and *Haec nos
  communio*). Nothing else of the Maternity's formulary travels: not its
  chants, lesson or Gospel, not its Preface (RGMR 483), not its colour.
- **Sung Mass that is not conventual (a parish *Missa cantata* or *solemnis*):**
  the Sunday Mass alone, with one Collect, one Secret and one Postcommunion (RG
  111 a; RGMR 434 a).

No other universal feast, vigil, octave, Ember day or seasonal substitution
falls on the date. Green vestments follow RG 127 b, printed p. XX (PDF 18):
*a feria II post dominicam I post Pentecosten, usque ad sabbatum ante
Adventum*; the Sunday is none of the excepted Ember ferias or vigils, and the
commemoration does not change the colour.

**No ipso-iure external solemnity on this Sunday.** RGMR 358, printed p. XXVI
(PDF 24), read, gives an external solemnity *ipso iure* only to (a) the Sacred
Heart, (b) the Rosary *in dominica I mensis octobris*, (c) the Purification
under its condition, and (d)-(h) principal patrons, titulars, dedications and
founders, all particular to a place or institute. The Rosary branch belongs to
the first Sunday of October, which in 2026 is 4 October, and does not reach
this date. Under RGMR 358 i a feast of the universal calendar kept *cum
peculiari populi concursu* may have an external solemnity at the local
Ordinary's judgement, and RGMR 359 lets such a solemnity be kept on the day the
feast is impeded; whether any place keeps the Maternity, or a neighbouring
feast, in that way on this Sunday is a local decision and is not computed.
RGMR 360 would then admit one sung and one low Mass, or two low Masses,
*tamquam votivae II classis*. RGMR 369, printed p. XXVII (PDF 25), read, permits
one Mass *Pro Fidei propagatione* as a votive Mass of II class *die quo
peculiares habentur celebrationes pro Missionibus*; the Missal fixes no date
for that day and none is computed here. Other votive Masses of II class
(RGMR 341-342, printed p. XXV, PDF 23, read) depend on local occasions and are
not computed. None of these alters the Sunday's formulary, which remains the
object of study.

**Dated official witnesses.** Two dated Ordos of institutes that celebrate with
the 1962 books were read live for this date. Neither response is retained or
registered, and neither changes any registration; both are held only in this
run's scratch area. Their SHA-256 values are recorded so that the research
stage can register a dated edition and passage if it relies on them.

- FSSP France, *Ordo du mois*, <https://www.fssp.fr/ordo-du-mois/>, read
  2026-10-07, response 169,685 bytes, SHA-256
  `72dbb99be7ef59f8a9261a6a0c11e4e9bdaa873908aa926a61709699ad769a25`:
  *Dimanche 11 octobre* — *20e Dimanche après la Pentecôte (2ème classe,
  Vert)*. The line names no commemoration; the Ordo prints one line per day and
  this silence is not read as an omission of the Maternity. The source library
  already holds a dated passage for this entry,
  `passage.fssp-france.ordo-du-mois.web-2026-10-05.2026-10-11` over
  `artifact.fssp-france.ordo-du-mois.web-2026-10-05.html-185e6519` (restricted,
  SHA-256 `185e6519…`, 169,633 bytes), whose recorded context matches what was
  read today; the live bytes differ from the registered hash, as that site's
  delivery is not byte-stable.
- ICRSP France, *Ordo*, <https://icrspfrance.fr/ordo.php?d=2026-10-01>, read
  2026-10-07, response 116,307 bytes, SHA-256
  `31028aa7f06e52a678fa7893c59266123121d10c4c72e766f2d51122e715681d`:
  *dimanche 11 octobre 2026* — *XXe Dimanche après la Pentecôte (2e
  d'octobre)*, *Temps Per Annum*, second class, green; Gloria, Credo, *Or. pro
  Papa*, Trinity Preface; at Lauds *Mémoire de la Maternité de la Très Sainte
  Vierge Marie*; Mass *Messe propre (Omnia)*, with *Mém. de la Maternité … &
  pro Papa*, Credo, Trinity Preface.

Computation, the printed calendar and both dated witnesses agree on the
identity, the second class and the green colour; the ICRSP entry also names
the Sunday's Mass by its Introit, gives the Trinity Preface, and carries the
commemoration of the Maternity. Nothing fails closed. Two things in that
witness are its own and are not imported. Its *Oratio pro Papa* is an
institute observance whose basis was not examined; RGMR 434 b admits no
oration on a II-class Sunday beyond the one commemoration. It states the
commemoration without distinguishing low from sung Mass; the universal books
make that distinction (RG 108, 111 a), and this record follows the books.

## Appointed proper

Every element is required and none has an alternative within the formulary:
the page prints no option, no choice and no substitute. Loci are the printed
page and marginal number of the controlling edition, read on 200- and 400-dpi
page images of artifact PDF pp. 493-494. Psalms are cited in the Missal's
Vulgate numbering, with the Hebrew number of the repository's psalm concordance
(`…/challoner-gutenberg-1581/artifacts/psalm-numbering-ee3c7757/psalm-numbering.tsv`,
SHA-256 `535761886df2…` recomputed and matched) in parentheses. The English
verse offset is zero for Pss 118, 136 and 144; for Ps 107 the concordance counts
the inscription as v. 1, so the Missal's Ps 107:2 is Hebrew 108:2 and English
108:1.

| Order and key | Element and printed locus | Liturgical place, extent and boundary |
|---|---|---|
| 1 `introit` | *Antiphona ad Introitum* *Omnia, quae fecisti nobis, Domine*, printed citation *Dan. 3, 31, 29 et 35*; verse Ps 118:1 (119:1); p. 412 right column, no. 1689 | Entrance chant (RGMR 427, p. XXXI): antiphon *Omnia, quae fecisti nobis, Domine, in vero iudicio fecisti, quia peccavimus tibi, et mandatis tuis non oboedivimus: sed da gloriam nomini tuo, et fac nobiscum secundum multitudinem misericordiae tuae*; psalm verse *Beati immaculati in via: qui ambulant in lege Domini*; printed cue *V. Gloria Patri*; repetition. No Alleluia outside paschal time (RGMR 429). |
| 2 `collect` | *Oratio* *Largire, quaesumus, Domine, fidelibus tuis indulgentiam placatus et pacem*; p. 412, no. 1690 | First oration of the Mass (RGMR 433). Printed conclusion *Per Dominum.*; the full form is RG 115 a's (p. XIX). In a low or conventual Mass the Maternity's Collect follows under a separate conclusion (see *Commemorated orations* below). |
| 3 `epistle` | Eph 5:15-21; p. 412 right column to p. 413 left column, no. 1691 | *Lectio Epistolae beati Pauli Apostoli ad Ephesios*. Opens *Fratres: Videte quomodo caute ambuletis*; ends at v. 21, *Subiecti invicem in timore Christi*. No shorter form. |
| 4 `gradual` | Ps 144:15-16 (145:15-16); p. 413, no. 1692 | After the Epistle (RGMR 469, p. XXXIII): respond *Oculi omnium in te sperant, Domine: et tu das illis escam in tempore opportuno*, verse *Aperis tu manum tuam: et imples omne animal benedictione*. |
| 5 `alleluia` | Ps 107:2 (108:2; English 108:1); p. 413, no. 1693 | *Alleluia, alleluia* with verse *Paratum cor meum, Deus, paratum cor meum: cantabo, et psallam tibi, gloria mea*, then *Alleluia*. No Tract and no Sequence. |
| 6 `gospel` | Jn 4:46-53; p. 413 left column to right column, no. 1694 | *Sequentia sancti Evangelii secundum Ioannem*. Opens *In illo tempore: Erat quidam regulus, cuius filius infirmabatur Capharnaum*; ends at v. 53, *et credidit ipse, et domus eius tota*. Printed cue *Credo.* follows. |
| 7 `offertory` | *Ant. ad Offertorium* Ps 136:1 (137:1); p. 413, no. 1695 | *Super flumina Babylonis illic sedimus, et flevimus: dum recordaremur tui, Sion.* |
| 8 `secret` | *Secreta* *Caelestem nobis praebeant haec mysteria, quaesumus, Domine, medicinam*; p. 413, no. 1696 | Said secretly, as many as the opening orations (RGMR 480-481, p. XXXIV). Printed conclusion *Per Dominum.* Followed by the printed direction *Praefatio de Ssma Trinitate.* |
| 9 `communion` | *Ant. ad Communionem* Ps 118:49-50 (119:49-50); p. 413, no. 1697 | After the Communion rites (RGMR 504, p. XXXV): *Memento verbi tui servo tuo, Domine, in quo mihi spem dedisti: haec me consolata est in humilitate mea.* |
| 10 `postcommunion` | *Postcommunio* *Ut sacris, Domine, reddamur digni muneribus*; p. 413, no. 1698 | As many as the opening orations (RGMR 505, p. XXXV). Printed conclusion *Per Dominum nostrum.*, longer than the cue on the Collect and Secret and still short of RG 115 a's full form; the printed length is a setting variable. |

This edition sets the chant rubrics both in full and abbreviated in the same
formulary: *Antiphona ad Introitum* at no. 1689 and *Ant. ad Offertorium*,
*Ant. ad Communionem* at nos. 1695 and 1697. The abbreviation is a setting
variable, not a different rubric. At the Gradual, Offertory and Communion the
citation stands on the rubric line and the marginal number on the first line
of text; at the Alleluia the citation *Ps. 107, 2* is printed inside the verse
line.

### Commemorated orations on this date

These are not part of the Sunday's formulary. They are added by rubric on 11
October 2026 in a low Mass and in a conventual Mass, and omitted in a sung
non-conventual Mass (see *Occurrence*). Each is required where it applies and
is said under its own conclusion after the corresponding Sunday oration.

| Place | Text and printed locus | Status |
|---|---|---|
| After the Collect | Maternity Collect *Deus, qui de beatae Mariae Virginis utero Verbum tuum, Angelo nuntiante, carnem suscipere voluisti*; p. 685 right column, no. 3847 (PDF 766) | Commemoration, low and conventual Mass only (RG 108, 111 b; RGMR 434 b, 437 a). Printed conclusion *Per eundem Dominum nostrum Iesum Christum Filium tuum: Qui tecum vivit et regnat in unitate.* |
| After the Secret | Maternity Secret *Tua, Domine, propitiatione, et beatae Mariae semper Virginis, Unigeniti tui Matris, intercessione*; p. 686 right column, no. 3855 (PDF 767) | As above (RGMR 480). Printed conclusion *Per eundem Dominum.* Its Preface direction does not apply (RGMR 483). |
| After the Postcommunion | Maternity Postcommunion *Haec nos communio, Domine, purget a crimine*; p. 686 right column, no. 3857 (PDF 767) | As above (RGMR 505). Printed conclusion *Per eundem Dominum.* |

### Wording against the Clementine Vulgate

The comparisons below were made word by word against the tracked Clementine
Vulgate (`edition.catholic-church.vulgata-clementina.ebible-latvuc`, its
verse-text artifacts, Daniel read directly at
`…/verse-text-32-daniel-3ca259b5/32-daniel.tsv`) after normalising i/j,
ligatures, accents and pointing, through `tools/tpt mass-propers show
--calendar roman-1962 --mass pentecost-20 --bible clementine-vulgate`, with the
Epistle and Gospel compared token by token by script. They are textual
observations about wording and boundary. Whether a chant follows an older Latin
psalter or another Latin text, and which, is left to research, and no origin is
asserted here.

- **Introit.** The antiphon is not a continuous Vulgate text, and its words do
  not stand at all of the verses the Missal cites. Its first clause shares
  *quae fecisti nobis … in vero iudicio fecisti* with Clementine Dan 3:31 (which
  reads *Omnia ergo, quae induxisti super nos, et universa quae fecisti
  nobis*); *peccavimus* stands at v. 29; *mandatis tuis non oboedivimus* has no
  word-for-word Clementine counterpart (v. 30 reads *praecepta tua non
  audivimus, nec observavimus*); and the closing *da gloriam nomini tuo, et fac
  nobiscum secundum multitudinem misericordiae tuae* corresponds to words of
  vv. 43 and 42, while Clementine v. 35, which the Missal cites, reads *neque
  auferas misericordiam tuam a nobis, propter Abraham …*. The verse omits the
  Clementine's title *Alleluja* and the letter heading *Aleph*, which the
  Clementine counts inside Ps 118:1.
- **Epistle.** The Missal prefixes the liturgical address *Fratres:* and omits
  the Clementine's *itaque* and its vocative *fratres* (*Videte itaque, fratres,
  quomodo caute ambuletis*). It spells *intellegentes* for the Clementine's
  *intelligentes*. Every other word of vv. 15-21 agrees.
- **Gradual.** The Missal reads *et tu das illis escam* where the Clementine at
  Ps 144:15 reads *et tu das escam illorum*. The verse agrees.
- **Alleluia.** The Missal reads *cantabo, et psallam tibi, gloria mea* where
  the Clementine at Ps 107:2 reads *cantabo, et psallam in gloria mea*.
- **Gospel.** The liturgical opening *In illo tempore: Erat quidam regulus*
  stands for the first half of v. 46, *Venit ergo iterum in Cana Galilaeae, ubi
  fecit aquam vinum. Et erat quidam regulus*, so the pericope begins within the
  verse it cites and leaves the Cana setting unread. Every other word of
  vv. 46-53 agrees.
- **Offertory.** The Missal omits the Clementine's title *Psalmus David,
  Jeremiae*, reads *dum* for *cum*, and adds *tui* (*dum recordaremur tui,
  Sion*; Clementine *cum recordaremur Sion*).
- **Communion.** The Missal reads *Memento* for the Clementine's *Memor esto*,
  adds *Domine* after *servo tuo*, and ends at *in humilitate mea*, before the
  Clementine's close of v. 50, *quia eloquium tuum vivificavit me*. It omits the
  letter heading *Zain*.

The formulary prints no Tract, Sequence, prophecy, proper *Communicantes* or
*Hanc igitur* (RGMR 501, p. XXXIV: such variations are noted in the proper
Mass, and none is noted here), *Oratio super populum* (RGMR 506, p. XXXV:
Lenten and Passiontide ferias), second or third oration of its own, blessing,
or alternative reading. The 1862 antecedent's *Secunda Oratio A cunctis*,
*Alia Secreta Exaudi nos Deus*, *Alia Postcommunio Mundet et muniat* and
*Tertia ad libitum*, printed on the same pages, belong to the pre-1960 rubrics
and are not part of the 1962 formulary.

## Other text-bearing parts of this Mass

These are fixed or rubrically appointed texts of the 1962 *Ordo Missae*,
*Praefationes* and appendix, not proper text. The study refers to them and does
not reproduce the Ordinary. The rubric numbers below were read on the page
images in this stage. The *Ordo Missae* marginal numbers were located on the
same facsimile's text layer at the artifact pages given, and the Trinity
Preface (no. 1082) and last Gospel (no. 1139) were also read on page images;
the other *Ordo Missae* numbers and the Asperges appendix were not re-read on
images here. The registered passage records covering them are
`…vatican-typica-1962.ordo-missae-ad-gradum`, `…ordo-missae-kyrie-gloria`,
`…ordo-missae-credo`, `…ordo-missae-conclusio`, `…praefationes` and
`…ordo-ad-aspergendam-aquam-benedictam`.

| Place | Text and appointment | Status and source |
|---|---|---|
| Before the principal Mass, where used | Blessing of water *Die dominico* and *Aspersio aquae benedictae* extra tempus paschale (*Asperges me*); appendix nos. 5919-5926 (PDF 1039-1040), located | A Sunday rite outside the Mass and outside this formulary. Whether and where it precedes a given Mass is not settled here; it is not part of the appointed inventory. |
| Prayers at the foot of the altar | Ps 42 *Iudica me* with its antiphon, Confiteor, through *Oramus te*; *Ordo Missae* nos. 1013-1023 (PDF 297-298) | Said: RGMR 425 (p. XXXI) omits *Iudica* only from Passion Sunday to Maundy Thursday and in Requiem Masses. |
| Introit doxology; Kyrie | *Gloria Patri* in the Introit; ninefold Kyrie, *Ordo Missae* no. 1024 (PDF 298) | RGMR 427-428, 430 (p. XXXI); the Introit's printed *V. Gloria Patri* cue at no. 1689. |
| After the Kyrie | *Gloria in excelsis*, *Ordo Missae* no. 1025 (PDF 298-300) | Said. RGMR 431 a (p. XXXI) ties it to the Office's Te Deum at Matins, a Breviary rubric this Missal omits. The ICRSP dated entry also carries the Gloria for this date; it is an unadopted lead. No chant setting is chosen. |
| Before the Gospel; after it | *Munda cor meum*, Gospel dialogue; homily | RGMR 471, 474 (p. XXXIII); *Ordo Missae* nos. 1026-1028 (PDF 300). |
| After the Gospel or homily | *Credo* | Said: RGMR 475 a, *in qualibet dominica* (p. XXXIII); printed cue after no. 1694; text *Ordo Missae* no. 1029 (PDF 301). |
| After the Secret(s) | *Praefatio de Ss.ma Trinitate* | Appointed, not chosen: printed direction after no. 1696 and RGMR 494 b, *tamquam de Tempore … in omnibus dominicis II classis, extra tempus natalicium et paschale* (p. XXXIV, PDF 32); RGMR 483 excludes the commemorated feast's Preface. Complete unnotated text, with the same rubric, at printed p. 293, no. 1082 (PDF 374), read on the page image. |
| Canon | *Te igitur* through the doxology | The one Roman Canon, said secretly (RGMR 500, p. XXXIV). There is no alternative Eucharistic Prayer and no proper insertion for this day (RGMR 501). |
| Conclusion | *Ite, missa est*, *Placeat*, blessing, last Gospel Jn 1:1-14 | RGMR 507-509 (p. XXXV): *Ite, missa est*, since no procession is supplied (507 a); the last Gospel *in quavis Missa* is the initium of John, and none of the omission cases of 510 applies; the commemoration supplies no proper last Gospel. *Ordo Missae* nos. 1132 (*Ite*, PDF 404), 1137 (*Placeat*, PDF 406), 1138 (blessing, PDF 407) and 1139 (last Gospel, printed p. 327, PDF 408, read on the page image). |

## Lawful study-text routes

- **Latin, all ten proper elements.** Control: the 1962 page images above.
  Publication basis: 17 U.S.C. 103(b) with a public-domain antecedent, as
  settled for the repository in
  `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`.
  The antecedent is the Pustet Ratisbon 1862 printing
  (`edition.catholic-church.missale-romanum.pustet-ratisbon-1862`), which
  prints the whole formulary at printed pp. 352-354 under *Dominica XX. post
  Pentecosten*. Two witnesses to those pages exist in the library and both
  were read here:
  - the tracked public-domain text layer
    `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`
    (SHA-256 `f34bc7cf9293…` recomputed and matched), at physical lines
    51986-52142: heading 51986-51988, Introit 51990-52011 (page 353 from
    52002), Collect 52013-52020, Epistle 52026-52047, Gradual 52049-52056,
    Alleluia 52057-52065, Gospel 52067-52099, Offertory 52101-52104, Secret
    52106-52112, page 354 from 52119, Communion 52126-52130, Postcommunion
    52132-52138, with the 1862's own pre-1960 extra orations at 52021-52024,
    52121-52124 and 52140-52142; and
  - the tracked three-page extraction
    `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.pentecost-20-pages-352-354`
    (SHA-256
    `1f171dea09c09014742cdcffcac175baa2fe39a0dfcae94316e300439a4d8768`
    recomputed and matched; derived from the registered complete scan PDF,
    parent PDF pages 438-440), whose page images were rendered and read here
    at display resolution.

  On the page images every element of this formulary agrees with the 1962 in
  its words, including each divergence from the Clementine listed above: the
  1862 already reads the Introit cento in the same words, *Fratres.* without
  *itaque*, *das illis escam*, *psallam tibi, gloria mea*, the liturgical
  Gospel opening at *Erat quidam regulus*, *dum recordaremur tui Sion*, and
  *Memento … Domine* ending at *humilitate mea*. The differences seen are of
  orthography (*judicio*, *obedivimus*, *intelligentes*, *Jesu*, *ejus*,
  *cujus*, *Cœlestem*, *obedire*), capitalisation (*Spiritu sancto*), pointing,
  citation form (*Dan. 3.*, *Ps. 118.*, *c. 5.*, *Ps. 144.*, *Ps. 107.*,
  *c. 4.*, *Ps. 136.* without verse numbers) and conclusion length (*Per
  Dominum.* on the Postcommunion). This was a reading, not a word-for-word
  collation at full resolution. Three of the ten elements already carry
  collated `publication_status = "permitted"` rows in
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` —
  Collect, Secret and Postcommunion — each verified against
  `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-pentecost-20-orations`
  and cited to the 1862 text layer through
  `passage.catholic-church.missale-romanum.pustet-ratisbon-1862.pentecost-20-orations`.
  The Introit and the six scriptural elements (Epistle, Gradual, Alleluia,
  Gospel, Offertory, Communion) have no ledger row and need one, or an
  equivalent recorded basis, before their Latin is published.
- **Latin, the commemorated Maternity orations.** The rights inventory names
  sanctoral formularies first published after the 1920-family printing as the
  1962 edition's own contribution, and directs that their wording be searched
  by incipit in the public-domain witnesses wherever it stands. The provenance
  ledger carries `permitted` rows for all three orations, verified against
  `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-maternitatis-beatae-mariae-virginis-orations`,
  whose recorded locus names the Collect (no. 3847) and Secret (no. 3855) but
  not the Postcommunion (no. 3857). The rows locate antecedent wording in the
  1922 Tours Mame at other formularies (printed pp. 3, 937 and 36) and cite
  the 1862 text layer at other places with partial token agreement (34 of 44,
  16 of 26 and 15 of 22 tokens). A closer antecedent was found in this stage
  on the same 1862 text layer: among its Masses for certain places, under
  *Festa Octobris*, *Dominica II*, *Festum Maternitatis B. Mariae Virginis*
  (appendix pp. [171]-[172], indexed there as *Dom. II. Maternitatis B. M. V.
  dpl. majus*), the 1862 prints the Collect *Deus, qui de beatae Mariae
  Virginis utero Verbum tuum* at physical lines 99579-99589, the Secret *Tua,
  Domine, propitiatione, et beatae Mariae semper Virginis Unigeniti tui matris
  intercessione* at 99658-99667 and the Postcommunion *Haec nos communio,
  Domine, purget a crimine* at 99676-99683, each concluding *Per eumdem
  Dominum*, in words that on the text layer agree with the 1962's apart from
  orthography and pointing. That formulary has its own Introit *Salve, sancta
  parens* and is directed to be said with a commemoration of the occurring
  Sunday and the Sunday's Gospel at the end (lines 99590-99591, 99685-99686);
  it is a different, local Mass and supplies nothing to the 1962 Sunday
  except the antecedent wording of the three orations. Neither the ledger's
  loci nor these lines were read on page images in this stage.
- **English, canonical Scripture.** The Douay-Rheims (Challoner) as registered
  (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  with `…american-1899-ebible` as the other registered Douay printing), read
  at the Vulgate loci through `tools/tpt mass-propers show … --bible
  douay-rheims`, which resolves the Missal's Vulgate psalm numbering. Its
  canonical verses are **not** the Missal's wording at the Introit (a cento the
  Douay verses at Dan 3:31, 29 and 35 do not carry), the Epistle's liturgical
  address, the Gospel's opening, the Alleluia's *psallam tibi, gloria mea* (the
  Douay gives *will give praise, with my glory*), the Offertory's *tui* (the
  Douay gives *when we remembered Sion*), and the Communion's *Memento …
  Domine* and shortened close (the Douay gives *Be thou mindful of thy word …
  because thy word hath enlivened me*). English must never be composed to fill
  those differences; where the Douay cannot carry the Missal's form the
  profile's rule is to say so and give the Latin with a description.
- **English, the Sunday's orations.** The 1861 Cummiskey hand missal
  (`edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861`),
  under the heading *XX. SUNDAY after PENTECOST* at printed p. 448. Two
  library records carry it:
  - `passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.post-pentecosten-20`
    over the tracked payload `…philadelphia-1861.temporal-orations-en`,
    physical lines 170-172, with the per-oration passages
    `…post-pentecosten-20.collect` and `…post-pentecosten-20.secret` (states
    through `verified`, 2026-10-05); and
  - `…philadelphia-1861.pentecost-20-checked-english`, a tracked
    transcription that its record calls model-assisted and checked against
    the page images (SHA-256 `0f45cd314efb…` recomputed and matched), giving
    the Collect (p. 448), Secret (p. 449) and Postcommunion (pp. 449-450).

  The registered scan `…philadelphia-1861.ia-scan-pdf` was fetched in this
  stage, matched its registered SHA-256
  `85034c90d5cbfe891f4359fb2faff907d217dbd11a30458b55e4c48eae028898`, and its
  PDF pp. 457-459 (printed pp. 448-450) were read at display resolution: the
  Collect (*Largire.—Favourably grant*) and Secret (*May these mysteries*)
  stand there in the wording both payloads carry, and the Postcommunion begins
  *Ut sacris.—That we may be worthy* at the foot of p. 449. The same pages
  print the 1861 book's own English for the whole Mass, including the Introit
  cento (*Whatever thou hast done to us, O Lord, thou hast done by a just
  judgment*), which no registered passage covers; that English is the 1861
  book's own and is not the profile's route for the scriptural elements. Two
  of its features are recorded so that no one takes it for the Missal's sense:
  its Offertory reads *when we remembered thee, O Sion*, and its Communion
  reads *Remember, O Lord, what thou saidst to thy servant*. The finding-aid
  overlay `src/sources/inventories/roman-1962-proper-translations-v1.toml`
  still records the English of this Sunday's Collect, Secret and Postcommunion
  as `unavailable` / `rights-withheld` pending an exact binding; that shared
  record belongs to its own owner and is unchanged here.
- **English, the commemorated Maternity orations.** No registered Cummiskey
  passage covers them, and none was looked for in that book here. The Lasance *New Roman Missal*, Benziger revision of
  1945 (`edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945`),
  prints all three under *Oct. 11—Feast of the Maternity of the Blessed Virgin
  Mary*, printed pp. 1233, 1235 and 1236, through
  `passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.maternity-checked-english`
  over the tracked `…maternity-checked-english` payload (SHA-256
  `661c88187ac1…` recomputed and matched), whose rights basis is the
  nonrenewal recorded in the Lasance rights inventory. The registered scan
  `…benziger-revised-1945.internet-archive-facsimile-pdf-6cf3c3d0` was
  fetched in this stage, matched its registered SHA-256
  `6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70` and
  75,268,976 bytes, and PDF pp. 1234, 1236 and 1237 were read at display
  resolution: the three prayers stand there in the payload's wording. The
  payload's own record notes that its Postcommunion renders *caelestis
  remedii* as Christ (*companions of Him, Who is our heavenly healing*); that
  is the translators' interpretation. The overlay records the Maternity English
  as `unavailable` / `no-exemplar`; unchanged here.
- **Trinity Preface.** Appointed by rubric and its Latin located (p. 293,
  no. 1082), within the registered `…vatican-typica-1962.praefationes`
  passage. The 1861 English exists as the Trinity clause of
  `…philadelphia-1861.praefationes-propriae`, not examined here. Whether the
  study quotes or only cites the Preface is for research.

No source was registered or retained in this stage. The existing library was
read first and sufficed for resolution; everything fetched was either an
already registered artifact fetched to its registered hash or a live Ordo
response whose identity and hash are written down above. No liturgical owner is
imported: the formulary and the commemorated orations are local to this leaf's
own family and are referenced in the Missal itself, so there is no
shared-formulary Makefile dependency to declare.

Two observations about shared library records are reported rather than
repaired, because this stage owns no source record: the 1962 Maternity passage
record's locus omits the Postcommunion (no. 3857, p. 686) for which the
provenance ledger cites it as verification; and the ledger's three Maternity
rows rest their antecedent on text-layer matches in the 1922 Mame and partial
token agreement at other places in the 1862, while the 1862's own Maternity
formulary at appendix pp. [171]-[172] carries all three orations and is not
cited by them.

## Remaining verification for research

- Collate every proper element word for word at 200 and 400 dpi against the
  1962 page images and against the 1862 pages at full resolution; write
  `propers/retrieved.txt` and `propers/verified.md` with the loci,
  conclusions and orthographic transformations. Collate the three commemorated
  Maternity orations against p. 685-686 in the same way if the study prints
  them.
- Identify the textual source of the Introit antiphon and decide how its
  citation is to be represented: the Missal prints *Dan. 3, 31, 29 et 35*, but
  the closing clause's words stand at Clementine Dan 3:42-43, and v. 35 reads
  otherwise. Identify likewise the source of the Gradual's *illis*, the
  Alleluia's *tibi, gloria mea*, the Offertory's *dum … tui* and the
  Communion's *Memento … Domine*, or record the negative result. Nothing above
  asserts an origin for any of them.
- Establish or record a publication basis for the Latin of the Introit and the
  six scriptural elements, which the provenance ledger does not yet carry;
  verify on page images an antecedent for the three Maternity orations (the
  1862 appendix pp. [171]-[172], or the loci the ledger gives) before printing
  their Latin; and decide the English
  display for the places where the Douay cannot carry the Missal's form,
  including whether the 1861 book's own Introit English is used under its own
  attribution or the Latin is given with a description.
- Choose between, or reconcile, the two registered Cummiskey routes for the
  Sunday's orations, collating the chosen payload against the 1861 page images
  at full resolution; collate the Lasance Maternity payload at full resolution
  if the study prints the commemoration; decide whether the Trinity Preface is
  quoted or only cited.
- Decide, with the authoring stages, how the studies present the commemoration:
  it belongs to this date's low and conventual Masses and not to the
  formulary or to a sung parish Mass, and its orations add no Scripture.
- Read each appointed passage in its complete biblical context — the Prayer of
  Azariah, Dan 3:24-45 (Clementine numbering), for the Introit; Eph 5 and its
  surrounding exhortation; Jn 4:43-54 with the first Cana sign it recalls,
  which the liturgical opening omits — run the reception sweep, and generate
  `research/chronology.toml` and `research/chronology-annotations.tex` with
  `tools/tpt proper-chronology`. No biblical date is asserted in this record.
  `tools/tpt proper-chronology loci` already resolves every appointed locus
  under the default profile `catholic-comprehensive-v1`: Introit (Dan 3:31,
  3:29, 3:35, Ps 118:1) `dated`; Epistle `composition-only`; Gradual
  `composition-only`; Alleluia `composition-only`; Gospel `dated`; Offertory
  `dated`; Communion `composition-only`. The distinct directly appointed
  passages as printed, in canonical then verse order, are Ps 107:2, Ps 118:1,
  Ps 118:49-50, Ps 136:1, Ps 144:15-16, Dan 3:29, Dan 3:31, Dan 3:35,
  Jn 4:46-53 and Eph 5:15-21; each is appointed once. Whether the Introit's
  printed Daniel loci or the verses carrying its words are the right chronology
  inputs is for research to settle before generation.
- Register a dated edition and passage for 11 October 2026 if the study relies
  on the ICRSP Ordo; the registered FSSP passage of 2026-10-05 covers that
  institute's line for the date.
- Resolve, only if the study relies on them, the points this stage did not
  settle: the Breviary's Te Deum rubric behind the Gloria, the Asperges
  placement, and any particular-calendar overlay or local external solemnity.
  None is needed for the universal formulary on this date.
- Bind the controlling sources in `research/source-bindings.toml` and declare
  the external owners actually relied on in `research/review-dependencies.toml`.
  The authorities adopted here are the 1962 facsimile artifact with its
  `temporal-pentecost-20-orations` and
  `temporal-maternitatis-beatae-mariae-virginis-orations` passages, the
  facsimile-rights inventory, the Latin provenance ledger, the 1862 Pustet text
  artifact, its `pentecost-20-orations` passage and its
  `pentecost-20-pages-352-354` extraction, the Douay-Rheims editions and the
  psalm-numbering concordance, the Clementine Vulgate edition, the Cummiskey
  passages and payloads named above with their registered scan, the Lasance
  Maternity passage and payload with their registered scan and the Lasance
  rights inventory, and, as computation inputs,
  `src/sources/calendars/roman-1962/propers.yaml` and `rubrics.yaml`.
