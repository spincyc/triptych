# Celebration context and complete appointed inventory

Resolved 18 September 2026 for the `proper-study` v3 production of the Claude
1962 leaf, run `1e02dc05f2df9940`, seeded at commit
`72616eb9cc25c7ea7cc061c0e82efffc8b5ea882`. The production-plan line of
2026-09-18 authorizes provider `claude` for this exact identity as an
independent production. No research handoff was supplied. The
other provider's leaf for the same identity and every postconciliar record are
outside this record's evidence; nothing below is taken from them. This record
settles what is studied. It contains no study prose, spoken text, timing claim
or review verdict; research collates the sources and may correct it from
evidence.

## Identity, governing books and territory

- Canonical identity: `liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost`,
  catalog ID `57` in the 1962 temporal registry of
  `guidance/liturgy/roman-1962-propers.md`. Calendar family `roman-1962`.
  The finding-aid mass index `src/sources/calendars/roman-1962/propers.yaml`
  carries it as `pentecost-17`, `registry: '57'`; the index is a lead and not
  the source of record for any wording.
- Governing edition: *Missale Romanum*, editio typica, Typis Polyglottis
  Vaticanis 1962 (`edition.catholic-church.missale-romanum.vatican-typica-1962`),
  controlled on the page images of
  `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`.
  A locally held copy matched the registered SHA-256
  `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a` and
  82,815,941 bytes before any page was read.
- Printed heading and rank: *Dominica decima septima post Pentecosten*,
  *II classis*, Proper of Time, printed p. 398 right column (artifact PDF p.
  479). Running heads on pp. 398–399 read *Dominica XVII post Pentecosten*.
- Formulary boundary: it begins after the Postcommunion of the Sixteenth
  Sunday (no. 1601) and ends with its own Postcommunion, no. 1611, at the head
  of p. 400 (PDF 481). The next heading, *Feria quarta Quatuor Temporum
  septembris*, II classis, no. 1612 onward, is a different formulary. Marginal
  nos. 1602–1611.
- Governing books within that edition: the *Calendarium*; the *Rubricae
  generales* (part I of the 1960 code as printed); the *Rubricae generales
  Missalis romani* (part III); the *Ordo Missae*; the *Praefationes*. Part II,
  the *Rubricae generales Breviarii romani* (nn. 138–268), is printed only as
  a heading marked *Hic omittuntur* on p. XX (PDF 18) and is therefore not
  available in this witness.
- Territory: the universal 1962 General Roman Calendar. No diocese, church
  titular or dedication, religious institute or other particular calendar was
  supplied, so no local overlay is applied or computed; the study concerns
  the universal formulary on that date, not a direction to a particular church.
- Language: Latin governs. Every English route below is a historical study aid,
  not an approved vernacular liturgical text.
- Cycle: the 1962 Missal appoints the readings with the formulary and has no
  Lectionary cycle. No A/B/C or I/II value exists for this record, and the
  requested date and the appointed formulary name the same identity, so there
  is no requested-versus-appointed cycle difference to preserve.
- Homily audience for the later homily stage: adult parish assembly. The
  Missal places a homily after the Gospel, "praesertim in dominicis", before
  the Creed (RGMR 474–475, p. XXXIII, PDF 31); the homily is authored
  preaching and adds no text to this inventory.

## Occurrence on 20 September 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
roman-1962 --date 2026-09-20 --json` returns candidate `pentecost-17`, "slot 17
of 26 Sundays after Pentecost", season after Pentecost, no Lectionary value and
nothing unresolved. The anchors are those tabulated in
`guidance/liturgy/calendar-computation.md` for 2026: Easter 5 April, Pentecost
24 May, Trinity Sunday 31 May (the first Sunday after Pentecost), First Sunday
of Advent 29 November; liturgical year 30 November 2025 – 28 November 2026.
Thirty-one May plus sixteen weeks is 20 September, so the date is the
seventeenth Sunday of the run. With `P = 26`, the resumed Fifth and Sixth
Sundays after the Epiphany occupy slots 24 and 25 and the Twenty-fourth
formulary slot 26; the resumption mechanism does not reach slot 17.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
roman-1962 --date 2026-09-20 --json` is settled: winner `pentecost-17`, a
second-class Sunday (the tool cites RG 12 and RG 91 row 15; this stage did not
reread RG 91, and the II-class rank is independently printed in the formulary
heading). The only other candidate is the calendar's ordinary commemoration of
Ss. Eustace and Companions, which the tool omits under RG 111 and RGMR 434 b.
Both loci were read on the page images:

- *Calendarium*, printed p. LI (PDF 53): 20 September, *Commemoratio Ss.
  Eustachii et Sociorum Mm.*, Comm.
- *Rubricae generales* 111 b, printed p. XVIII (PDF 16): on a II-class Sunday
  only one commemoration is admitted, and only of a II-class feast, itself
  omitted if a privileged commemoration is due.
- RGMR 434 b, printed p. XXXI (PDF 29): on a II-class Sunday no other oration
  is admitted beyond that commemoration of a II-class feast.

The commemoration is therefore omitted, not transferred and not added. No
universal feast, vigil, octave or seasonal substitution falls on the date.
Green vestments follow RG 127 b, printed p. XX (PDF 18), from Monday after the
First Sunday after Pentecost to the Saturday before Advent.

**Dated official witnesses.** Two dated annual Ordos of institutes that
celebrate with the 1962 books were checked for this date. Both are registered
in the source library, restricted, with only identity and factual-locus
metadata retained:

- `passage.fssp-france.ordo-du-mois.web-2026-09-17.2026-09-20` (artifact
  SHA-256 `aa1c6f1625c462c28d3142e26bebc9998983d22070555288353ad50e84cb8d88`):
  *Dimanche 20 septembre*, 17th Sunday after Pentecost, second class, green.
- `passage.icrsp-france.ordo.web-2026-09-17.2026-09-20` (artifact SHA-256
  `0c6c1fd531e0771adf9d573baca1c74b46bd7ce9738a7fb6158ff7a27aa8eeb7`): XVII
  Sunday after Pentecost, "3ᵉ de septembre", second class, green; proper Mass
  *Justus est*, Gloria, Credo, Trinity Preface, and an *Or. pro Papa*.

In this stage a held copy of each registered response was matched to its
registered SHA-256 and its 20 September entry read; both public pages were then
reopened on 18 September 2026 and show the same entries. The reopened
responses differ in bytes from the registered ones (169,630 and 111,598
bytes), are not retained, and change no registration. These Ordos witness the
occurrence for their own institutes' calendars; neither is an overlay for a
United States diocese or parish. The ICRSP *Oratio pro Papa* belongs to that
institute's practice, whose particular basis was not examined; RGMR 434 b
admits no such oration in the universal formulary, so it is not imported. The
entry's incipit spelling *Justus est* does not correct the Missal's *Iustus
es*. Computation and both dated witnesses agree; nothing fails closed.

Both Ordos place the September Ember days on Wednesday 23, Friday 25 and
Saturday 26 September, the week after this Sunday. They are separate
formularies (the Missal's next heading, p. 400, no. 1612) and change nothing
in the Sunday's Mass.

## Appointed proper

Every element is required and has no alternative branch. Loci are printed page
and marginal number of the controlling edition, read on 200-dpi page images of
PDF pp. 479–481. Psalms are cited in the Missal's Vulgate numbering, with the
Hebrew number of the repository's psalm concordance in parentheses.

| Order and key | Element and printed locus | Liturgical place, extent and boundary |
|---|---|---|
| 1 `introit` | *Antiphona ad Introitum*, Ps 118:137, 124 (119); verse Ps 118:1; p. 398, no. 1602 | Entrance chant: *Iustus es, Domine, et rectum iudicium tuum: fac cum servo tuo secundum misericordiam tuam*, psalm verse *Beati immaculati in via*, printed cue *Gloria Patri* and repetition (RGMR 427). The antiphon joins v. 137 to the first half of v. 124 only. |
| 2 `collect` | *Oratio* *Da, quaesumus, Domine, populo tuo*; p. 399, no. 1603 | The one oration of the Mass (RGMR 434 b). Printed conclusion *Per Dominum nostrum.* |
| 3 `epistle` | Eph 4:1–6; p. 399, no. 1604 | *Lectio Epistolae beati Pauli Apostoli ad Ephesios*. Opens *Fratres: Obsecro vos*, without the Vulgate's *itaque*; after v. 6 the Missal adds *Qui est benedictus in saecula saeculorum. Amen.*, which is not part of Eph 4. No shorter form. |
| 4 `gradual` | Ps 32:12, 6 (33); p. 399, no. 1605 | After the Epistle (RGMR 469): respond v. 12, verse v. 6, in that order. The respond reads *Dominus Deus eorum … quem elegit Dominus*, where the Clementine Vulgate reads *Dominus Deus ejus … quem elegit*. |
| 5 `alleluia` | Ps 101:2 (Hebrew 102:2); p. 399, no. 1606 | Alleluia with verse *Domine, exaudi orationem meam, et clamor meus ad te perveniat*; the Clementine reads *veniat*. English Bibles that leave the superscription unnumbered call the verse 102:1. |
| 6 `gospel` | Mt 22:34–46; p. 399, no. 1607 | *Sequentia sancti Evangelii secundum Matthaeum*. *In illo tempore: Accesserunt ad Iesum pharisaei* stands in place of v. 34 (*Pharisaei autem audientes quod silentium imposuisset sadducaeis, convenerunt in unum*); the text then follows vv. 35–46 through *amplius interrogare*. Printed cue *Credo* follows. The Gospel itself cites Deut 6:5, Lev 19:18 and Ps 109:1; those are embedded citations, not additional appointed readings. |
| 7 `offertory` | *Antiphona ad Offertorium*, cited Dan 9:17, 18 et 19; p. 399, no. 1608 | *Oravi Deum meum ego Daniel, dicens: Exaudi, Domine, preces servi tui: illumina faciem tuam super sanctuarium tuum: et propitius intende populum istum, super quem invocatum est nomen tuum, Deus.* A compiled adaptation, not a continuous quotation: the narrative opening lies outside vv. 17–19 (compare *Et oravi Dominum Deum meum*, 9:4, and *ego Daniel*, 9:2), and the petitions condense and rephrase vv. 17–19 (*illumina* for *ostende*). Research identifies its textual source; no origin is asserted here. |
| 8 `secret` | *Secreta* *Maiestatem tuam, Domine*; p. 399, no. 1609 | Over the offerings, said secretly (RGMR 480–481). Printed conclusion at length only as far as *… Qui tecum vivit et regnat in unitate.*; the full form is RG 115 a's (printed p. XIX), and the printed length is a typographic variable (`propers/verified.md` §8, corrected on the research stage's reentry, 2026-09-18). Followed by the printed direction *Praefatio de Ssma Trinitate.* |
| 9 `communion` | *Antiphona ad Communionem*, Ps 75:12–13 (Hebrew 76:12–13; 76:11–12 where the superscription is unnumbered); p. 399, no. 1610 | After the Communion rites (RGMR 504): *Vovete et reddite … terribili apud omnes reges terrae*; the Clementine lacks *omnes*. |
| 10 `postcommunion` | *Postcommunio* *Sanctificationibus tuis, omnipotens Deus*; p. 400, no. 1611 | As many as the collects (RGMR 505), hence one. Printed conclusion *Per Dominum nostrum.* |

The Vulgate comparisons above were made against the tracked Clementine
Vulgate (`edition.catholic-church.vulgata-clementina.ebible-latvuc`) through
`tools/tpt mass-propers show --bible clementine-vulgate` and its Daniel verse
file. They are textual observations about boundaries and wording; whether a
chant follows an older Latin psalter, and which, is left to research.

The formulary prints no Tract, Sequence, prophecy, proper *Communicantes* or
*Hanc igitur* (RGMR 501: such variations are noted in the proper Mass, and
none is noted here), *Oratio super populum* (RGMR 506: Lenten and Passiontide
ferias), second or third oration, blessing, or alternative reading. The 1862 antecedent's *Secunda Oratio A
cunctis*, *Alia Secreta*, *Alia Postcommunio* and *Tertia ad libitum* belong to
the pre-1960 rubrics and are not part of the 1962 formulary.

## Other text-bearing parts of this Mass

These are fixed or rubrically appointed texts of the 1962 *Ordo Missae* and
*Praefationes*, not proper text. The study refers to them and does not
reproduce the Ordinary. Rubric numbers marked "read" were read on the page
images in this stage; *Ordo Missae* marginal numbers come from the registered
passage records `…vatican-typica-1962.ordo-missae-credo` and
`…ordo-missae-conclusio` and were not reread.

| Place | Text and appointment | Status and source |
|---|---|---|
| Before the principal Mass, where used | *Aspersio aquae benedictae*, extra tempus paschale: antiphon *Asperges me* with Ps 50:3, versicles and oration *Exaudi nos*; appendix, printed p. [232], nos. 5925–5926 (PDF 1040), read | A Sunday rite outside the Mass and outside this formulary. Whether and where it precedes a given Mass was not resolved; it is not part of the appointed inventory. |
| Prayers at the foot of the altar | Ps 42 *Iudica me* with its antiphon, Confiteor | Said; RGMR 425 (p. XXXI, read) omits *Iudica* only from Passion Sunday to Maundy Thursday and in Requiem Masses. |
| Introit doxology; Kyrie | *Gloria Patri* in the Introit; ninefold Kyrie | RGMR 427–428, 430 (p. XXXI, read). |
| After the Kyrie | *Gloria in excelsis* | Said. RGMR 431 a (read) ties it to the Office's Te Deum at Matins, a Breviary rubric this Missal omits; the ICRSP dated entry corroborates the Gloria for this date. No chant setting is chosen. |
| Before the Gospel; after it | *Munda cor meum*, Gospel dialogue; homily | RGMR 471, 474 (p. XXXIII, read); *Ordo Missae* nos. 1026–1028. |
| After the Gospel or homily | *Credo* | Said: RGMR 475 a, every Sunday (read); printed cue after no. 1607; text *Ordo Missae* no. 1029. |
| After the Secret | *Praefatio de Ss.ma Trinitate* | Appointed, not chosen: printed direction after no. 1609 and RGMR 494 b, "in omnibus dominicis II classis, extra tempus natalicium et paschale" (p. XXXIV, PDF 32, read). Complete unnotated text p. 293, no. 1082 (PDF 374), read, with the same rubric. |
| Canon | *Te igitur* through the doxology | The one Roman Canon, said secretly (RGMR 500, read). There is no alternative Eucharistic Prayer and no proper insertion for this day. |
| Conclusion | *Ite, missa est*, *Placeat*, blessing, last Gospel Jn 1:1–14 | RGMR 507–509 (p. XXXV, PDF 33, read): *Ite, missa est*, since no procession is supplied (507 a); the last Gospel is the *Initium* of John, and none of the omission cases of 510 applies. *Ordo Missae* nos. 1132–1139. |

## Lawful study-text routes

- **Latin, all ten proper elements.** Control: the 1962 page images above.
  Publication basis: 17 U.S.C. 103(b) with a public-domain antecedent, as
  settled in `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`.
  The antecedent is the Pustet Ratisbon 1862 printing, whose tracked,
  public-domain page images
  `artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.ia-bookreader-leaf-426-50a5e6c3`
  (printed p. 341) and `…ia-bookreader-leaf-427-203fc51d` (printed p. 342)
  print the whole formulary under *Dominica XVII. post Pentecosten*; both files
  matched their registered hashes. Read at reduced display resolution in this
  stage, every element agrees with the 1962 in wording, with differences only
  of orthography, pointing and conclusion length (the 1862 prints *Per
  Dominum.* where the 1962 prints the longer conclusions of the Collect, Secret
  and Postcommunion). The three orations already carry collated rows in
  `src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml` against
  `passage.catholic-church.missale-romanum.vatican-typica-1962.temporal-pentecost-17-orations`
  and `passage.catholic-church.missale-romanum.pustet-ratisbon-1862.pentecost-17-orations`;
  the 1862 continuation page is registered as
  `passage.catholic-church.missale-romanum.pustet-ratisbon-1862.pentecost-17-continuation`.
- **English, canonical Scripture.** The Douay–Rheims (Challoner) as registered
  (`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`,
  with `…american-1899-ebible` as the other registered Douay printing), read at
  the Vulgate loci. Its canonical verses are not the Missal's adapted wording
  for the Epistle opening and doxology, the Gospel opening, the Offertory, or
  the chant verses noted above; English must never be composed to fill those
  differences.
- **English, orations.** The 1861 Cummiskey hand missal,
  `passage.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861.post-pentecosten-17`
  (tracked public-domain payload
  `…philadelphia-1861.temporal-orations-en`, lines 161–163, hash matched). In
  this stage the three orations were read on the registered scan
  (`…philadelphia-1861.ia-scan-pdf`, SHA-256 matched), printed pp. 431–433
  under *XVII. Sunday after Pentecost*, and agree with the payload word for
  word. The same pages print historical English for the chants and readings,
  including the Epistle's closing *who is blessed for ever more*, the Gospel's
  *The Pharisees come to Jesus* (cited there as Matt. xxii. 35–46) and the
  Offertory's *I Daniel prayed unto my God*; that English is not registered and
  may be used only after an exact passage record is made.
- **Trinity Preface.** Appointed by rubric and text located (p. 293, no. 1082).
  Any reproduction needs its own public-domain Latin antecedent and a
  registered historical English; the registered Cummiskey `praefationes-en`
  artifact was not examined here.

No source was registered or retained in this stage; the existing library
was read first and sufficed for resolution. The finding-aid overlay
`src/sources/inventories/roman-1962-proper-translations-v1.toml` still records
the English of these three orations as unavailable pending an exact binding,
although the passage record above now exists; that shared record belongs to
its own owner and is unchanged here. No liturgical owner is imported: the
formulary is local to this leaf, so there is no shared-formulary Makefile
dependency to declare.

## Remaining verification for research

- Collate every proper element word for word at 200 and 400 dpi against the
  1962 page images and the 1862 leaves at full resolution; write
  `propers/retrieved.txt` and `propers/verified.md` with the loci, conclusions
  and orthographic transformations.
- Identify the textual source of the Offertory compilation and of the chant
  wordings that differ from the Clementine Vulgate, or record the negative
  result.
- Decide the English display for the adapted elements (canonical Douay with
  the Latin shown, or a newly registered exact Cummiskey passage), and settle
  whether the Trinity Preface is quoted or only cited.
- Read each appointed passage in its complete biblical context, run the
  reception sweep, and generate `research/chronology.toml` and
  `research/chronology-annotations.tex` with `tools/tpt proper-chronology`.
  No biblical date is asserted in this record.
- Resolve, if the study relies on them, the points this stage did not reread:
  RG 91 (the precedence table the computation cites), the Breviary's Te Deum
  rubric behind the Gloria, and any particular-calendar overlay; none is
  needed for the universal formulary on this date.
- Bind the controlling sources in `research/source-bindings.toml` and declare
  the external owners actually relied on in `research/review-dependencies.toml`.
  The authorities adopted here are the 1962 facsimile artifact and its passage
  records, the facsimile-rights inventory, the Latin provenance ledger, the two
  dated Ordo passages, the 1862 leaves and passages, the Douay–Rheims
  editions, the Cummiskey passage, and, as computation inputs,
  `src/sources/calendars/roman-1962/propers.yaml` and `rubrics.yaml`.
