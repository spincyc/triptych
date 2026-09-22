# Celebration context and complete appointed inventory

Resolved 22 September 2026 for the `proper-study` v6 production of the Claude
1962 leaf, run `71b6f89518984232`, seeded at commit
`fa5355745b5e973584f047a7f59a20ad22676d64`. The production-plan line of
2026-09-22 authorizes provider `claude` for this exact identity as an
independent production and opens nothing else. `ARGS.research_handoff` is
`none`, so no handoff was supplied. The other provider's 1962 leaves, every
postconciliar record, and this provider's own neighbouring Sundays are outside
this record's evidence; nothing below is taken from them. This record settles
what is studied. It contains no study prose, spoken text, timing claim or
review verdict; the research stage collates the sources and may correct it
from evidence.

## Identity, governing books and territory

- Canonical identity: `liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost`,
  catalog ID `58` in the 1962 temporal registry of
  `guidance/liturgy/roman-1962-propers.md`. Calendar family `roman-1962`.
  `tools/check-proper-identity --document … --calendar roman-1962` passes.
  The finding-aid mass index `src/sources/calendars/roman-1962/propers.yaml`
  carries it as `pentecost-18`, `registry: '58'`; that index is a lead and
  never the source of record for any wording.
- Governing edition: *Missale Romanum*, editio typica, Typis Polyglottis
  Vaticanis 1962 (`edition.catholic-church.missale-romanum.vatican-typica-1962`),
  controlled on the page images of
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.
  A copy fetched into this run's scratch directory from the registered
  `source_url` matched the registered SHA-256
  `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` and
  82,815,941 bytes before any page was read.
- Printed heading and rank: *DOMINICA DECIMA OCTAVA post Pentecosten*,
  *II classis*, Proper of Time, printed p. 410 left column (artifact PDF
  p. 491). The running head of p. 410 reads *Dominica XVIII post Pentecosten*;
  the running head of p. 411, which carries the second half of this formulary,
  reads *Dominica XIX post Pentecosten*, because the Nineteenth Sunday begins
  on that page. The running head does not bound the formulary.
- Formulary boundary: it begins at marginal no. 1669 on p. 410, immediately
  after the Postcommunion (no. 1668) of the preceding formulary, *Sabbato
  Quatuor Temporum septembris* (whose running head stands over p. 409,
  artifact PDF p. 490, where its Tract, Gospel Lc 13:6-17 and Offertory
  Ps 87:2-3 are nos. 1663-1665). It ends with its own Postcommunion, no. 1678, on p. 411, where
  the next heading, *DOMINICA DECIMA NONA post Pentecosten*, II classis, no.
  1679, begins a different formulary. Marginal nos. 1669-1678.
- Governing books within that edition: the *Calendarium*; the *Rubricae
  generales* (part I of the 1960 code as printed); the *Rubricae generales
  Missalis romani* (part III); the *Ordo Missae*; the *Praefationes*. Part II,
  the *Rubricae generales Breviarii romani* (nn. 138-268), is printed only as
  a heading marked *Hic omittuntur.* on p. XX (PDF 18) and is therefore not
  available in this witness.
- Territory: the universal 1962 General Roman Calendar. No diocese, church
  titular or dedication, religious institute or other particular calendar was
  supplied, so no local overlay is applied or computed. The study concerns the
  universal formulary on that date, not a direction to a particular church.
  Both dated witnesses consulted below carry a French particular observance on
  this date; it is recorded as theirs and is not imported.
- Language: Latin governs. Every English route below is a historical study aid,
  not an approved vernacular liturgical text.
- Cycle: the 1962 Missal appoints the readings with the formulary and has no
  Lectionary cycle. No A/B/C or I/II value exists for this record, and the
  requested date and the appointed formulary name the same identity, so there
  is no requested-versus-appointed cycle difference to preserve.
- Homily audience for the later homily stage: adult parish assembly
  (`ARGS.audience`). The Missal places a brief homily after the Gospel,
  *praesertim in dominicis*, before the Creed (RGMR 474-475, p. XXXIII, PDF 31,
  read here); the homily is authored preaching and adds no text to this
  inventory.

## Occurrence on 27 September 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
roman-1962 --date 2026-09-27 --json` returns candidate `pentecost-18`, "slot 18
of 26 Sundays after Pentecost", season after Pentecost, no Lectionary value and
nothing unresolved; its only other candidate is the fixed-date sanctoral entry
*Ss. Cosmae et Damiani Martyrum*, III class. The anchors are those tabulated in
`guidance/liturgy/calendar-computation.md` for 2026: Easter 5 April, Pentecost
24 May, Trinity Sunday 31 May (the first Sunday after Pentecost), First Sunday
of Advent 29 November; liturgical year 30 November 2025 - 28 November 2026.
Thirty-one May plus seventeen weeks is 27 September, so the date is the
eighteenth Sunday of the run. With `P = 26` for 2026, the resumed Fifth and
Sixth Sundays after the Epiphany occupy slots 24 and 25 and the Twenty-fourth
formulary slot 26; the resumption mechanism does not reach slot 18.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
roman-1962 --date 2026-09-27 --json` is settled: winner `pentecost-18`, a
second-class Sunday (the tool cites RG 12 and RG 91 row 15; this stage did not
reread RG 91, and the II-class rank is independently printed in the formulary
heading). The one competing candidate, Ss. Cosmas and Damian, is returned as
`omitted` under RG 111 and RGMR 434 b. All three loci were read on the page
images in this stage:

- *Calendarium*, printed p. LI (PDF 53): 27 September, *Ss. Cosmae et Damiani
  Mm., III classis.*
- *Rubricae generales* 111 b, printed p. XVIII (PDF 16): *in dominicis II
  classis, una tantum admittitur commemoratio, scilicet de festo II classis,
  quae tamen omittitur si commemoratio privilegiata facienda sit.*
- RGMR 434 b, printed p. XXXI (PDF 29): on a II-class Sunday no other oration
  is admitted beyond that commemoration of a II-class feast.

A third-class feast is therefore admitted neither as a commemoration nor as an
oration: it is omitted outright, not transferred and not added, and the Mass
has exactly one oration (RGMR 433, 434 b, 505). No universal feast, vigil,
octave or seasonal substitution falls on the date. Green vestments follow RG
127 b, printed p. XX (PDF 18), which assigns green *a feria II post dominicam I
post Pentecosten, usque ad sabbatum ante Adventum*, excepting the September
Ember ferias and II- and III-class vigils; this Sunday is none of those.

The September Ember days of 2026 fall on Wednesday 23, Friday 25 and Saturday
26 September, the week **before** this Sunday, and the Ember Saturday formulary
is the one the Missal prints immediately before this one. They are separate
formularies and change nothing in the Sunday's Mass.

**Dated official witnesses.** Two dated annual Ordos of institutes that
celebrate with the 1962 books were read for this date, at the same URLs as the
registered editions `edition.fssp-france.ordo-du-mois.web-2026-09-17` and
`edition.icrsp-france.ordo.web-2026-09-17`. **These were fresh live readings,
not re-reads of the registered bytes:** the responses retrieved on 22 September
2026 are 169,631 and 111,681 bytes against the registered artifacts' 169,614
and 112,647, so neither registered SHA-256 could be matched and no registered
passage covers 27 September. The retrieved responses are held only in this
run's scratch directory, are not retained, are not registered, and change no
registration; their SHA-256 values are recorded here so that the research stage
can register a dated edition and passage for this date if it relies on them.

- FSSP France, *Ordo du mois*, <https://www.fssp.fr/ordo-du-mois/>, read
  2026-09-22, response SHA-256
  `2d06b46f708259cf7807a151f74274f64a36169e0412efda9bc01b8ef96c40cb`:
  *Dimanche 27 septembre* — 18th Sunday after Pentecost, second class, green,
  with an optional solemnity of St Thérèse of the Child Jesus.
- ICRSP France, *Ordo*, <https://icrspfrance.fr/ordo.php>, read 2026-09-22,
  response SHA-256
  `8cfb0aac194bd85a5fa35e725130e2cb6725eb66287cbba94446cfc462756e50`:
  *dimanche 27 septembre 2026* — XVIII Sunday after Pentecost, "4ᵉ de
  septembre", second class, green, with Gloria, Credo, an *Or. pro Papa* and
  the Trinity Preface; its notes carry a particular solemnity of St Thérèse of
  the Child Jesus and the Holy Face as secondary patroness of the Institute,
  with a commemoration and last Gospel of the Sunday.

Computation and both dated witnesses agree on the identity, the second class
and the colour; nothing fails closed. Two things in those witnesses are theirs
and are not imported. The St Thérèse observance is a French particular and
institute observance whose basis was not examined here; the universal
formulary on this date is the Sunday's, and RGMR 434 b admits no added oration,
so the ICRSP *Oratio pro Papa* is likewise not imported. One defect is recorded
rather than smoothed: the FSSP page prints **two** paragraphs headed *Dimanche
27 septembre*, the second reading *de la férie (4ème classe, Vert)*. A
fourth-class feria cannot occur on a Sunday under RG 91, the following
paragraph is correctly headed *Lundi 28 septembre*, and the second row is
therefore a defect in that witness. It does not disturb the Sunday's
identification, which the first row and the whole ICRSP entry agree on.

## Appointed proper

Every element is required and has no alternative branch: the formulary prints
no option, no choice and no substitute. Loci are the printed page and marginal
number of the controlling edition, read on 200- and 400-dpi page images of
artifact PDF pp. 491-492. Psalms are cited in the Missal's Vulgate numbering,
with the Hebrew number of the repository's psalm concordance
(`.../challoner-gutenberg-1581/artifacts/psalm-numbering-ee3c7757/`) in
parentheses.

| Order and key | Element and printed locus | Liturgical place, extent and boundary |
|---|---|---|
| 1 `introit` | *Ant. ad Introitum*, cited Eccli. 36, 18; verse Ps 121:1 (122); p. 410, no. 1669 | Entrance chant: *Da pacem, Domine, sustinentibus te, ut prophetae tui fideles inveniantur: exaudi preces servi tui, et plebis tuae Israel*, psalm verse *Laetatus sum in his, quae dicta sunt mihi: in domum Domini ibimus*, printed cue *V. Gloria Patri* and repetition (RGMR 427). |
| 2 `collect` | *Oratio* *Dirigat corda nostra*; p. 410, no. 1670 | The one oration of the Mass (RGMR 433, 434 b). Printed conclusion *Per Dominum.* |
| 3 `epistle` | 1 Cor 1:4-8; p. 410, no. 1671 | *Lectio Epistolae beati Pauli Apostoli ad Corinthios*. Opens *Fratres: Gratias ago Deo meo semper*, the address being liturgical and not part of 1 Cor 1:4. Ends at v. 8, *in die adventus Domini nostri Iesu Christi*, with no added doxology. No shorter form. |
| 4 `gradual` | Ps 121:1 et 7 (122); p. 410, no. 1672 | After the Epistle (RGMR 469): respond v. 1, *Laetatus sum in his*, verse v. 7, *Fiat pax in virtute tua: et abundantia in turribus tuis*, in that order. The respond omits the psalm's title *Canticum graduum*, which the Clementine counts inside v. 1. |
| 5 `alleluia` | Ps 101:16 (Hebrew 102:16); p. 410, no. 1673 | Alleluia with verse *Timebunt gentes nomen tuum, Domine, et omnes reges terrae gloriam tuam*, then *Alleluia*. English Bibles that leave the superscription unnumbered call the verse 102:15. |
| 6 `gospel` | Mt 9:1-8; p. 410-411, no. 1674 | *Sequentia sancti Evangelii secundum Matthaeum*. *In illo tempore: Ascendens Iesus in naviculam* stands in place of the Clementine's *Et ascendens in naviculam* (v. 1), the liturgical opening supplying the subject; the text then follows vv. 2-8 through *qui dedit potestatem talem hominibus*, ending on p. 411. Printed cue *Credo.* follows. |
| 7 `offertory` | *Ant. ad Offertorium*, cited Exodi 24, 4 et 5; p. 411, no. 1675 | *Sanctificavit Moyses altare Domino, offerens super illud holocausta, et immolans victimas: fecit sacrificium vespertinum in odorem suavitatis Domino Deo, in conspectu filiorum Israel.* A compiled adaptation and not a continuous quotation: it shares only the substance of *aedificavit altare* (v. 4) and *obtulerunt holocausta, immolaveruntque victimas* (v. 5), while *sanctificavit*, *fecit sacrificium vespertinum in odorem suavitatis Domino Deo* and *in conspectu filiorum Israel* stand in neither verse. Research identifies its textual source; no origin is asserted here. |
| 8 `secret` | *Secreta* *Deus, qui nos, per huius sacrificii*; p. 411, no. 1676 | Over the offerings, said secretly and in the same number as the opening orations (RGMR 480-481), hence one. Printed conclusion *Per Dominum.*; the full form is RG 115 a's (printed p. XIX, PDF 17, read here), and the printed length is a typographic variable: on the same page the preceding formulary's Secret at no. 1666 prints *Per Dominum nostrum Iesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.*, itself short of RG 115 a's full form. Followed by the printed direction *Praefatio de Ss.ma Trinitate.* |
| 9 `communion` | *Ant. ad Communionem*, Ps 95:8-9 (96); p. 411, no. 1677 | After the Communion rites (RGMR 504): *Tollite hostias, et introite in atria eius: adorate Dominum in aula sancta eius.* It begins inside v. 8, omitting *afferte Domino gloriam nomini eius*, and stops before *Commoveatur a facie eius universa terra* in v. 9. |
| 10 `postcommunion` | *Postcommunio* *Gratias tibi referimus*; p. 411, no. 1678 | As many as the opening orations (RGMR 505), hence one. Printed conclusion *Per Dominum.* |

Two observations about the loci themselves, recorded so that a later reader
does not take them for transcription errors. First, **the marginal numbers of
the right-hand column of printed p. 410 run off the fore-edge in both
registered digitisations of this edition**: at 400 dpi the CMAA scan shows
`167` and a fragment of a fourth digit (the word boxes end at x≈367 pt on a
≈371 pt page), and the Internet Archive scan
`artifact.…vatican-typica-1962.ia-sp07-facsimile-pdf-902cfa92` clips them
entirely. Numbers 1671-1674 are therefore fixed by continuity between the
fully legible 1670 on the same page and 1675-1678 on p. 411, not read whole.
Second, this edition sets the chant rubrics both in full and abbreviated: p. 410
prints *Antiphona ad Communionem* for the preceding formulary at no. 1667 and
*Ant. ad Introitum* for this one at no. 1669, while p. 411 prints *Ant. ad
Offertorium* and *Ant. ad Communionem* for this formulary at nos. 1675 and 1677
and then *Antiphona ad Introitum* in full for the next at no. 1679. The
abbreviation is a setting variable and not a different rubric.

The Vulgate comparisons above were made against the tracked Clementine Vulgate
(`edition.catholic-church.vulgata-clementina.ebible-latvuc`) through
`tools/tpt mass-propers show --calendar roman-1962 --mass pentecost-18 --bible
clementine-vulgate` and its chapter files. Three further divergences are
textual observations about wording and boundaries, and whether a chant follows
an older Latin psalter or another Latin text, and which, is left to research:

- **Introit.** The Clementine at Ecclus 36:18 reads *Da mercedem sustinentibus
  te, ut prophetae tui fideles inveniantur: et exaudi orationes servorum
  tuorum*. The Missal keeps the middle clause word for word, reads *Da pacem,
  Domine, sustinentibus te* for *Da mercedem sustinentibus te*, and closes
  *exaudi preces servi tui, et plebis tuae Israel* where the Clementine has
  *et exaudi orationes servorum tuorum*.
- **Alleluia.** The Clementine at Ps 101:16 opens *Et timebunt gentes*; the
  Missal drops the connective and ends the sentence where the Clementine
  continues into v. 17.
- **Communion.** The Missal reads *in aula sancta eius* where the Clementine
  at Ps 95:9 reads *in atrio sancto eius*.

The formulary prints no Tract, Sequence, prophecy, proper *Communicantes* or
*Hanc igitur* (RGMR 501: such variations are noted in the proper Mass, and none
is noted here), *Oratio super populum* (RGMR 506: Lenten and Passiontide
ferias), second or third oration, blessing, or alternative reading. The 1862
antecedent's *Secunda Oratio A cunctis*, *Alia Secreta Exaudi nos Deus*, *Alia
Postcommunio Mundet et muniat* and *Tertia ad libitum*, printed on the same
leaves, belong to the pre-1960 rubrics and are not part of the 1962 formulary.

## Other text-bearing parts of this Mass

These are fixed or rubrically appointed texts of the 1962 *Ordo Missae* and
*Praefationes*, not proper text. The study refers to them and does not
reproduce the Ordinary. Every rubric number below was read on the page images
in this stage; *Ordo Missae* marginal numbers are taken from the registered
passage records `…vatican-typica-1962.ordo-missae-credo` and
`…ordo-missae-conclusio` and were not reread.

| Place | Text and appointment | Status and source |
|---|---|---|
| Before the principal Mass, where used | *Aspersio aquae benedictae*, extra tempus paschale: antiphon *Asperges me* with Ps 50:3, versicles, and the oration *Exaudi nos*; appendix, printed p. [232], nos. 5925-5926 (PDF 1040), read | A Sunday rite outside the Mass and outside this formulary. Whether and where it precedes a given Mass was not resolved; it is not part of the appointed inventory. |
| Prayers at the foot of the altar | Ps 42 *Iudica me* with its antiphon, Confiteor | Said; RGMR 425 (p. XXXI, read) omits *Iudica* only from Passion Sunday to Maundy Thursday and in Requiem Masses. |
| Introit doxology; Kyrie | *Gloria Patri* in the Introit; ninefold Kyrie | RGMR 427-428, 430 (p. XXXI, read); the Introit's printed *V. Gloria Patri* cue at no. 1669. |
| After the Kyrie | *Gloria in excelsis* | Said. RGMR 431 a (read) ties it to the Office's Te Deum at Matins, a Breviary rubric this Missal omits; the ICRSP dated entry independently carries the Gloria for this date. No chant setting is chosen. |
| Before the Gospel; after it | *Munda cor meum*, Gospel dialogue; homily | RGMR 471, 474 (p. XXXIII, read); *Ordo Missae* nos. 1026-1028. |
| After the Gospel or homily | *Credo* | Said: RGMR 475 a, *in qualibet dominica* (read); printed cue after no. 1674; text *Ordo Missae* no. 1029. |
| After the Secret | *Praefatio de Ss.ma Trinitate* | Appointed, not chosen: printed direction after no. 1676 and RGMR 494 b, *tamquam de Tempore in dominicis Adventus, et in omnibus dominicis II classis, extra tempus natalicium et paschale* (p. XXXIV, PDF 32, read). Complete unnotated text, with the same rubric, at printed p. 293, no. 1082 (PDF 374), read. |
| Canon | *Te igitur* through the doxology | The one Roman Canon, said secretly (RGMR 500, read). There is no alternative Eucharistic Prayer and no proper insertion for this day (RGMR 501). |
| Conclusion | *Ite, missa est*, *Placeat*, blessing, last Gospel Jn 1:1-14 | RGMR 507-509 (p. XXXV, PDF 33, read): *Ite, missa est*, since no procession is supplied (507 a); the last Gospel is the *Initium* of John, and none of the omission cases of 510 applies. *Ordo Missae* nos. 1132-1139. |

## Lawful study-text routes

- **Latin, all ten proper elements.** Control: the 1962 page images above.
  Publication basis: 17 U.S.C. 103(b) with a public-domain antecedent, as
  settled for the repository in
  `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`.
  The antecedent is the Pustet Ratisbon 1862 printing, which prints the whole
  of this formulary at printed pp. 350-351 under *Dominica XVIII. post
  Pentecosten*. Two witnesses to those pages exist and both were read here:
  - the tracked, public-domain OCR text artifact
    `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf`
    (SHA-256 recomputed here and matched), at physical lines 51670-51811 —
    the heading at 51670, the Introit at 51673, and the Postcommunion ending
    at 51807, with 51809-51811 carrying the 1862's own pre-1960 *Alia
    Postcommunio* and *Tertia ad libitum*. This is the antecedent the Latin
    provenance ledger already cites for this Mass; and
  - the Internet Archive BookReader page images of leaves n435 and n436, which
    are **not registered**. They were fetched into this run's scratch directory
    from `https://archive.org/download/bub_gb_E7sPAAAAIAAJ/page/n435_w2500.jpg`
    and `…/n436_w2500.jpg`, read at reduced display resolution, and retained
    nowhere; SHA-256
    `dd53758ee5398bde65d46ffd2f0fd8650e48ea0230a5d5fc0459af60fcf0bc13`
    (1,215,681 bytes) and
    `5dfc6948ecdc4e1e9225fd706142904b6c15ee59cfb05f2c8f7817e8ce35804e`
    (1,156,625 bytes). The leaf-to-page offset was confirmed against the
    already registered neighbours n425-n427, which are printed pp. 340-342.
    Registering them, if the study relies on the images rather than on the text
    layer, is research-stage work.

  On both witnesses, read here at reduced display resolution and not yet
  collated word for word, every element of this formulary agrees with the 1962
  in wording, with differences only of orthography, pointing, capitalisation
  and conclusion length: the 1862 prints *Prophetae* where the 1962 prints
  *prophetae*, *ejus*/*hujus* where the 1962 prints *eius*/*huius*, *Israel*
  plain where the 1962 prints *Israël*, *Exodi 24* without the verse numbers,
  and *Per Dominum.* throughout. Four of the ten elements already carry
  collated, `publication_status = "permitted"` rows in
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` —
  Collect, Offertory, Secret, Postcommunion — each verified against
  `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-pentecost-18-orations`
  and cited to the 1862 antecedent at the loci above, with the ledger's own
  list of pointing differences. The six scriptural elements have no such row
  and need one, or an equivalent recorded basis, before their Latin is
  published.
- **English, canonical Scripture.** The Douay-Rheims (Challoner) as registered
  (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  with `…american-1899-ebible` as the other registered Douay printing), read at
  the Vulgate loci and resolved in the Missal's Vulgate psalm numbering. Its
  canonical verses are **not** the Missal's wording for the Introit antiphon,
  the Epistle's liturgical address, the Gospel's opening, the Offertory, or the
  Alleluia and Communion readings noted above; English must never be composed
  to fill those differences, and where the Douay cannot carry the Missal's
  form the profile's rule is to say so and give the Latin with a description.
- **English, orations.** The 1861 Cummiskey hand missal,
  `passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.post-pentecosten-18`
  over the tracked public-domain payload
  `…philadelphia-1861.temporal-orations-en` (SHA-256 recomputed here and
  matched), physical
  lines 164-166, printed pp. 444-445, Internet Archive leaves 452-453, under
  the heading *XVIII. SUNDAY AFTER PENTECOST*. The three rows are the Collect,
  Secret and Postcommunion in liturgical order. This stage read them in the
  tracked payload only; it did **not** open the 1861 scan
  (`…philadelphia-1861.ia-scan-pdf`), so the payload has not been checked
  against its own page images here.
- **Trinity Preface.** Appointed by rubric and text located (p. 293, no. 1082).
  Any reproduction needs its own public-domain Latin antecedent and a
  registered historical English; the registered Cummiskey `praefationes-en`
  artifact was not examined here.

No source was registered or retained in this stage. The existing library was
read first and sufficed for resolution; everything fetched was either an
already registered artifact fetched to its registered hash, or a candidate
whose identity and hash are written down above for the research stage to
register. The finding-aid overlay
`src/sources/inventories/roman-1962-proper-translations-v1.toml` records the
English of this Mass's four non-scriptural or compiled elements — Collect,
Offertory, Secret and Postcommunion — as `unavailable` / `rights-withheld`
pending an exact binding, although the Cummiskey passage record for the three
orations now exists; that shared record belongs to its own owner and is
unchanged here. No liturgical owner is
imported: the formulary is local to this leaf, so there is no shared-formulary
Makefile dependency to declare.

One defect in the source library was found and is reported rather than
repaired, because this stage owns no source record: the registered `source_url`
of `artifact.catholic-church.missale-romanum.vatican-typica-1962.ia-sp07-facsimile-pdf-902cfa92`,
`https://archive.org/download/sp07mr62-editio-typica/sp07mr62-editio-typica.pdf`,
returns 404. The item's own metadata names the file `Missale Romanum (1962).pdf`
at the registered 51,166,555 bytes, and fetching that path yields the registered
SHA-256 `902cfa92ac559144be7d656715be611c25aeeab5aa98d139b07b6a247d79bd20`.
The artifact is correct; only its recorded URL is stale.

## Remaining verification for research

- Collate every proper element word for word at 200 and 400 dpi against the
  1962 page images and against both 1862 witnesses at full resolution; write
  `propers/retrieved.txt` and `propers/verified.md` with the loci,
  conclusions and orthographic transformations, and record there that the
  marginal numbers 1671-1674 are clipped in both digitisations.
- Identify the textual source of the Offertory compilation and of the Introit,
  Alleluia and Communion wordings that differ from the Clementine Vulgate, or
  record the negative result. Nothing above asserts an origin for any of them.
- Establish or record a publication basis for the Latin of the six scriptural
  elements, which the provenance ledger does not yet carry, and decide the
  English display for the elements the Douay cannot carry.
- Check the tracked Cummiskey oration payload against the 1861 scan's own page
  images at printed pp. 444-445, and decide whether the Trinity Preface is
  quoted or only cited.
- Read each appointed passage in its complete biblical context, run the
  reception sweep, and generate `research/chronology.toml` and
  `research/chronology-annotations.tex` with `tools/tpt proper-chronology`.
  No biblical date is asserted in this record. `tools/tpt proper-chronology
  loci` already resolves every appointed locus under the default profile
  `catholic-comprehensive-v1`: Introit, Epistle, Gradual, Alleluia and Gospel
  return `composition-only`, and the Offertory (Ex 24:4-5) and Communion
  (Ps 95:8-9) return `dated`. The distinct directly appointed passages are
  Ex 24:4-5, Ps 95:8-9, Ps 101:16, Ps 121:1, Ps 121:7, Ecclus 36:18,
  Mt 9:1-8 and 1 Cor 1:4-8; Ps 121:1 is appointed twice, by the Introit verse
  and by the Gradual respond, and is inventoried once.
- Register a dated edition and passage for 27 September 2026 if the study
  relies on either Ordo; neither registered passage covers this date, and the
  live pages differ in bytes from the registered artifacts.
- Resolve, if the study relies on them, the points this stage did not reread:
  RG 91 (the precedence table the computation cites), the Breviary's Te Deum
  rubric behind the Gloria, and any particular-calendar overlay, including the
  French and institute St Thérèse observances the two Ordos carry; none is
  needed for the universal formulary on this date.
- Bind the controlling sources in `research/source-bindings.toml` and declare
  the external owners actually relied on in `research/review-dependencies.toml`.
  The authorities adopted here are the 1962 facsimile artifact and its
  `temporal-pentecost-18-orations` passage, the facsimile-rights inventory, the
  Latin provenance ledger, the 1862 Pustet text artifact and its
  `pentecost-18-orations` passage, the Douay-Rheims editions, the Clementine
  Vulgate edition, the Cummiskey `post-pentecosten-18` passage and its
  `temporal-orations-en` artifact, the psalm-numbering concordance, and, as
  computation inputs, `src/sources/calendars/roman-1962/propers.yaml` and
  `rubrics.yaml`.
