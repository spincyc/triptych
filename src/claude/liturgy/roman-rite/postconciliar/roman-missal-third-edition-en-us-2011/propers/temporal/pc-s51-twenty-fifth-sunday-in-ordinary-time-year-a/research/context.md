# Celebration context and complete appointed inventory

Resolved 19 September 2026 for the `proper-study` v4 production of the Claude
postconciliar leaf, run `472e2eb20876b22a`, seeded at commit
`02bae3f417048707bf5f76a9ef50b3236bf60701`. The production-plan line of
2026-09-19 authorizes provider `claude` for this exact identity as an
independent production. No research handoff was supplied. Every fact below was
established in this stage from the witnesses it names. The other provider's
leaf for the same identity, that leaf's verdicts, and every 1962 record are not
evidence here, and nothing in this record comes from the 1962 calendar, Missal
or propers. This record settles what is studied. It contains no study prose,
spoken text, timing claim or review verdict; research collates the sources and
may correct it from evidence.

## Identity, governing books and territory

| Field | Resolution |
| --- | --- |
| Canonical identity | `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a`; calendar family `postconciliar`, path family `temporal` |
| Stable registry | `guidance/liturgy/postconciliar-propers-registry.md`: parent `PC-S51`, Twenty-fifth Sunday in Ordinary Time, stem `pc-s51-twenty-fifth-sunday-in-ordinary-time`; registered keys `PC-S51-A`, `PC-S51-B`, `PC-S51-C` for Lectionary nos. 133, 134, 135 |
| Formula key and slug | `PC-S51-A`; full slug is the stem plus `-year-a`. No form, branch or occurrence suffix is admitted |
| Registry checks | Ordinary Time Sunday `51 − 26 = 25`, hence owner `weeks/25`; Lectionary number `64 + 3 × (51 − 28) + 0 = 133`. Both agree with the dated witnesses below |
| Edition disposition | [Formula dispositions](../../../registry/formula-dispositions.md), row `PC-S51-A`, added in this stage: adopted as the stable registry lists it, with no cycle expansion. Dated result in [2026 occurrences](../../../registry/occurrences-2026.md) |
| Canonical Missal owner | [Ordinary Time Week XXV](../../shared/ordinary-time/weeks/25/propers/verified.md), opened in this stage at the registry-fixed path and shared with the Year B and Year C targets. It alone carries the formulary's witnesses, locators, element boundaries, variation check and rights disposition; this record cites its result and restates none of its evidence |
| Build edge | The collection Makefile already lists that owner as a prerequisite of this identity's study, `-synthesis` and `-homily` PDFs, in a rule written against the provider-selected source root. `make -n -p PROVIDER=claude` was read in this stage and resolves the prerequisite to the Claude owner above. The collection-wide edges on `shared/exposition-format.tex` and `registry/*.md` apply as well |
| Missal | *Roman Missal, Third Edition, for Use in the Dioceses of the United States of America*, English, implemented 27 November 2011; Latin base *Missale Romanum*, editio typica tertia (2002), in its *reimpressio emendata* (2008) |
| Lectionary | *Lectionary for Mass for Use in the Dioceses of the United States of America*, second typical edition (1998/2001), Volume I, no. 133, with the 2017 *Supplement* where applicable; based on the *Ordo lectionum Missae*, editio typica altera (1981), as emended. The national calendar's own front matter states this book identity (printed p. 5) |
| Other controlling books | *General Instruction of the Roman Missal*, United States English edition of 2011 with the 2021 emendations; *Universal Norms on the Liturgical Year and the Calendar*; the USCCB *Liturgical Calendar for the Dioceses of the United States of America* for 2026 |
| Territory | Dioceses of the United States of America, national calendar only. No diocesan, religious, parish, titular, dedication or patronal calendar was supplied, so none is applied, computed or excluded for an unnamed church |
| Language | The approved United States English governs the celebration. This production prints none of it: Scripture appears in the public-domain Douay–Rheims (Challoner) as a study translation, orations by Latin incipit and description |
| Requested study cycle | Year A, stated by the identity's `-year-a` suffix |
| Cycle appointed on the date | Year A, from 30 November 2025 through 22 November 2026. The requested and the appointed cycle coincide; no substitution is made or needed. The independent weekday cycle (II in this year) governs no Sunday and is not applicable |
| Homily audience | Adult parish assembly, for the later homily stage. The homily is authored preaching and adds no text to this inventory |

The finding-aid index `src/sources/calendars/postconciliar/propers.yaml`
carries this Mass as `ot-25`, `registry: pc-s51`. It is a lead, not a source of
record, and one of its entries is wrong for this Mass; see the owner's finding 2.

## Occurrence on 20 September 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
postconciliar --date 2026-09-20 --json` returns candidate `ot-25`, "the Sunday
of Ordinary Time week 25", season Ordinary Time, Sunday cycle A, nothing
unresolved. The anchors are those of `guidance/liturgy/calendar-computation.md`
for 2026: Easter 5 April, Pentecost 24 May, Christ the King 22 November, First
Sunday of Advent 29 November. Pentecost is the Sunday of resumed week
`R = 34 − 26 = 8`, and 20 September falls seventeen weeks later: week 25. From
the other anchor, 20 September is nine weeks before the Sunday of week 34:
again week 25. The last week before Lent was the sixth (Sunday 15 February, Ash
Wednesday 18 February), so this is a thirty-three-week year and week 7 never
occurred; nothing is renumbered. The national calendar corroborates both ends
in its own entries: Sunday 15 February is its Sixth Sunday in Ordinary Time,
and Monday 25 May carries the label of the Eighth Week. Both entries were read
here in the calendar's text layer; the week label belongs to the registered
passage `passage.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.ordinary-time-week-numbering`.
`Y = 2026`, and `2026 mod 3 = 1` is Year A.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
postconciliar --date 2026-09-20 --json` returns winner `ot-25`, a Sunday in
Ordinary Time at place 6 of the table of liturgical days, and one loser: the
obligatory memorial of Saints Andrew Kim Tae-gon, Paul Chong Ha-sang and
Companions, place 10, disposition omitted. Both loci were read in this stage in
the Latin *Normae universales* as printed in the registered 2002 Missal
artifact (physical PDF pp. 70–71): the table at no. 59, places 6 and 10, and
no. 60, under which the higher place is celebrated, only an impeded solemnity
is transferred, and the remaining celebrations are omitted for that year. The
*Calendarium Romanum generale* in the same artifact (physical PDF p. 78)
inscribes the memorial on 20 September. It is therefore omitted, not
transferred, not commemorated, and supplies no text to this Mass.

**Dated official witnesses.**

| Witness | Identity and check | What it states |
| --- | --- | --- |
| USCCB, *Liturgical Calendar for the Dioceses of the United States of America* 2026 | Registered artifact `artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.usccb-pdf-4bd9add0`. A copy fetched from the publisher on 19 September 2026 matched the registered SHA-256 `4bd9add07512396a2323aa977bc4816a5fad6348262e12740bcee97c77372d02` and 839,777 bytes before any page was read. Restricted; not retained | Printed p. 5 (PDF p. 7): Sunday cycle Year A, 30 November 2025 to 22 November 2026; weekday Cycle 2; the book identities given above. Printed p. 38 (PDF p. 40), read in a rendered page image and in the text layer: 20 September, Sunday, Twenty-Fifth Sunday in Ordinary Time, green; Is 55:6-9 / Phil 1:20c-24, 27a / Mt 20:1-16a; Lectionary (133); Psalter Week I. No other celebration and no bracketed optional memorial stands on the date, and the English day-by-day entries nowhere name the Korean martyrs. **Corrected on research re-entry:** the calendar does print their Spanish title against 20 September in its appended list *Títulos litúrgicos, Propio de los Santos* (printed p. 55, PDF p. 57). That is a list of approved titles by date, not a dated entry for 2026, and it changes nothing in the occurrence |
| USCCB daily readings page for 20 September 2026, `https://bible.usccb.org/bible/readings/092026.cfm` | Complete page retrieved 19 September 2026 (58,503 bytes, SHA-256 `9581da4f98293b2551dfbe2db4ff7939d26898ea3255c732bf4610d7b02e9015`). Not registered in the source library; its wording is restricted and nothing of it is retained | Heading Twenty-fifth Sunday in Ordinary Time; Lectionary: 133; Reading 1 Isaiah 55:6-9; Responsorial Psalm 145:2-3, 8-9, 17-18 with response locator (18a); Reading 2 Philippians 1:20c-24, 27a; Alleluia Cf. Acts 16:14b; Gospel Matthew 20:1-16a. It prints one form of each unit and no "or" alternative |

Computation and both dated witnesses agree; nothing fails closed. The printed
United States Lectionary volume itself was not inspected; the two official
USCCB witnesses stand for its content at no. 133, and the Latin *Ordo* below
corroborates every boundary.

**The week that follows.** The Sunday's readings, Gloria, Creed and Sunday
Preface do not continue into the week. The national calendar gives Monday 21
September to the Feast of Saint Matthew (no. 643) and the remaining days to the
independent weekday course (nos. 450–454). The edition's occurrence record
carries the detail.

## Appointed inventory

Ten ritual places carry eleven text-bearing elements, because the Communion
antiphon is a closed pair. Missal elements are cited to the Week XXV owner,
whose record holds their printed locators, incipits and summaries. Lectionary
boundaries were read in three places that agree in every figure: the two
dated witnesses above and the *Ordo lectionum Missae*, editio typica altera
(1981), no. 133, *Dominica vigesima quinta*, Year A, read on 19 September 2026
at 200 dpi in the page image of printed p. 72 (artifact p. 126) of the
registered scan `artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e`
(SHA-256 `ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d`,
21,487,058 bytes, matched before reading). Psalms are cited in the Hebrew
numbering of the United States Lectionary with the Vulgate number, which the
Latin books and the Douay–Rheims use, in parentheses.

| Order | Key | Element and exact locus | Liturgical place, extent and boundary | Status |
| ---: | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | Entrance Antiphon *Salus populi ego sum*; Week XXV owner | Introductory Rites, at the entrance. A composed first-person oracle with no locator in the Latin Missal; the official ICEL Antiphonary identifies Psalm 36[37]:39–40 as its basis. It is neither the appointed wording of those verses nor an adaptation of them | required |
| 2 | `collect` | Collect *Deus, qui sacrae legis omnia constituta*; Week XXV owner | Concludes the Introductory Rites, after the Gloria; long conclusion | required |
| 3 | `first-reading` | Isaiah 55:6–9; Lectionary no. 133 | Liturgy of the Word, first reading. Whole verses; one form only | required |
| 4 | `responsorial-psalm` | Psalm 145 (144):2–3, 8–9, 17–18, response from v. 18a; Lectionary no. 133 | After the first reading. Three two-verse strophes; the response is the first half of v. 18 only. The verse numbers are the same in both numberings | required |
| 5 | `second-reading` | Philippians 1:20c–24, 27a; Lectionary no. 133 | Second reading. It enters v. 20 at its third clause, where Christ is magnified in Paul's body by life or by death; omits vv. 25–26; and takes from v. 27 only the opening command to live worthily of the Gospel. The rest of v. 27 and vv. 28–30 are context, not appointed text | required |
| 6 | `gospel-acclamation` | Alleluia with verse `Cf.` Acts 16:14b; Lectionary no. 133 | Before the Gospel. `Cf.` marks an adaptation: the verse turns the narrative statement that the Lord opened Lydia's heart to heed what Paul said into a petition in the first person plural about hearing the Son's words. Acts 16:14 is its identified basis and never a substitute acclamation | required |
| 7 | `gospel` | Matthew 20:1–16a; Lectionary no. 133 | Gospel. The labourers in the vineyard, through the first sentence of v. 16. The Latin *Ordo* opens it with a liturgical incipit addressing the parable to the disciples. The cut at 16a excludes the second sentence that the Clementine Vulgate and the Douay–Rheims print in v. 16, on the many called and the few chosen. No shorter form | required |
| 8 | `prayer-over-offerings` | Prayer over the Offerings *Munera, quaesumus, Domine, tuae plebis*; Week XXV owner | Liturgy of the Eucharist, after the preparation of the gifts; short conclusion | required |
| 9a | `communion-antiphon-a` | Communion Antiphon, Psalm 119 (118):4–5; Week XXV owner | At Communion. Printed first, without `Cf.` | appointed alternative |
| 9b | `communion-antiphon-b` | Communion Antiphon, John 10:14; Week XXV owner | At Communion. Printed second under *Vel:*, without `Cf.`, though the Missal inserts *dicit Dominus* and supplies *oves* | appointed alternative |
| 10 | `prayer-after-communion` | Prayer after Communion *Quos tuis, Domine, reficis sacramentis*; Week XXV owner | Concludes the Communion Rite; short conclusion | required |

The formulary prints no Offertory antiphon, Sequence, proper Preface, proper
Eucharistic Prayer insert, prayer over the people or solemn blessing, and the
Lectionary prints no alternative or shorter reading, no second psalm response
and no second acclamation verse for Year A. A Saturday-evening anticipated Mass
uses this same formulary; it is not a Vigil form and has no key.

**Boundary checks made against tracked Scripture.** The Douay–Rheims
(`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`)
and the Clementine Vulgate (`edition.catholic-church.vulgata-clementina.ebible-latvuc`)
were read at every boundary verse. Psalm 118:4–5 in both agrees with antiphon
A clause for clause. Matthew 20:16 in both carries the second sentence that the
appointment excludes. Philippians 1:20 in both begins before the appointed
clause and 1:27 runs on beyond it. Acts 16:14 in both is third-person narrative. Psalm 36:39–40,
which the official ICEL Antiphonary identifies as the Entrance antiphon's
basis, shares its theme and little of its wording; the relation is therefore
`identified-basis`, not `adaptation`. These are observations about extent; the
textual history of each is left to research.

**Relationship classes, preliminary.** Under the 1981 *Praenotanda* nos.
105–107, read in page images of printed pp. XLIV–XLV (and re-read on research
re-entry), the first reading is `officially correlated` with the Gospel, and the Gospel and the second reading
each belong to a `semi-continuous` course. Under GIRM 61–62 the psalm is
`responsorial` to the first reading and the verse before the Gospel is
`acclamatory`. *Tabella II*
(printed p. LI) assigns Philippians to the Twenty-fifth through Twenty-eighth
Sundays of Year A, so this Sunday opens that letter's course, and the national
calendar confirms Philippians 2:1–11 for 27 September. The Missal week's
antiphons and orations are shared by all three cycles. Every connection between
them and the Year A readings is editorial synthesis, as the three-document
profile settles for every formulary.

**The Ordo's own tituli (added on research re-entry).** *Praenotanda* no. 106
says that the relation between the readings of one Mass "is shown by the
careful choice of the tituli set over the individual readings". At no. 133
(printed p. 72) the *Ordo* prints three:

| Reading | Titulus | Source of the words |
| --- | --- | --- |
| Lectio I | *Non sunt cogitationes meae cogitationes vestrae* | Isaiah 55:8 |
| Lectio II | *Mihi vivere Christus est* | Philippians 1:21 |
| Evangelium | *An oculus tuus nequam est, quia ego bonus sum?* | Matthew 20:15 |

These are edition-controlled evidence of what the Lectionary singles out in
each reading. For the first reading and the Gospel they are, on the *Ordo*'s own
account, how the official correlation is shown: God's thoughts that are not
ours are set beside the householder's question about his goodness. The second
reading's titulus belongs to its semi-continuous course. They are evidence of
the Lectionary's emphasis within each reading and of that one correlation. They
are not evidence of a design joining the Missal texts or the second reading to
the rest. *Tabella II* stands on printed p. LI in the scan read, although the
*Ordo*'s footnote 117 points to p. LII.

## Branches and other text-bearing parts of this Mass

These branch IDs are proposed as the stable semantic IDs for the manifest, the
leaf audit and the resolution appendix. No local selection was supplied for
any of them, and none is inferred.

| Branch ID | Authority and trigger | Status | Places affected | Resolution |
| --- | --- | --- | --- | --- |
| `communion-antiphon-psalm` | The Missal prints Psalm 119 (118):4–5 first | appointed alternative | 9 | Unselected; both antiphons receive full treatment |
| `communion-antiphon-good-shepherd` | The Missal prints John 10:14 under *Vel:* | appointed alternative | 9 | Unselected. *Tempus per annum* rubric 6 prefers an antiphon that agrees with the Gospel of the Mass; whether either agrees with Matthew 20:1–16a is a judgment the books do not make, and none is made here |
| `entrance-or-communion-chant-substitution` | GIRM 48 and 87: in the United States the Missal antiphon, the *Graduale Romanum* or *Graduale Simplex* chant, or another approved chant | permitted | 1, 9 | Unselected. The Missal antiphons are the studied layer; the same articles provide for reciting them where there is no singing |
| `psalm-or-acclamation-chant-substitution` | GIRM 61 and 62 a: a sung psalm may come from the *Graduale Romanum*, the *Graduale Simplex* or another approved collection; the Alleluia verse from the Lectionary or the *Graduale* | permitted | 4, 6 | Unselected. The Lectionary's psalm and verse are the studied layer. With two readings before the Gospel, GIRM 63 does not apply |
| `offertory-chant` | GIRM 74, under the norms of no. 48 | permitted | preparation of the gifts | Unselected. The Missal prints no Offertory antiphon; that silence does not mean the rite has no chant |
| `sprinkling-rite` | GIRM 51 and the Order of Mass: on Sundays the blessing and sprinkling of water may replace the Penitential Act | ritual substitution | Introductory Rites | Unselected; it brings its own texts and adds no proper of this formulary |
| `compatible-preface-and-eucharistic-prayer` | *Tempus per annum* rubric 5; GIRM 364, 365 | permitted | Eucharistic Prayer | Unselected. One of the eight Prefaces of the Sundays in Ordinary Time with a compatible Eucharistic Prayer; a coupled choice |
| `eucharistic-prayer-iv-with-preface` | GIRM 365 d | conditional | Eucharistic Prayer | Unselected. If Prayer IV is chosen, its invariable Preface excludes a Sunday Preface |
| `concluding-blessing-form` | The Missal's blessings at the end of Mass and prayers over the people, usable at the priest's discretion | permitted | Concluding Rites | Unselected. None is appointed to this Sunday; the 2008 reprint adds alternative dismissal formulas to the Order of Mass, which are Ordinary and not proper |
| `local-proper-calendar` | Universal Norms 59–60 with a particular calendar: a proper solemnity, or a celebration lawfully assigned to this Sunday | conditional | whole Mass | Not supplied. An actual local celebration needs its own resolution and never a blended formulary |

| Place | Text and appointment | Status |
| --- | --- | --- |
| Gloria | Sung or said on Sundays outside Advent and Lent (rubric 4; GIRM 53) | required |
| Creed | Sung or said on Sundays (rubric 4; GIRM 68) | required |
| Homily; Universal Prayer | Authored or locally composed; no appointed text | not applicable |
| Memorial of the Korean martyrs | Omitted under Universal Norms 60; no Collect, commemoration or reading enters this Mass | omitted |
| Sequence; proper Eucharistic Prayer insert | None appointed | not applicable |

## Lawful study-text routes

- **Scripture: the three readings, the psalm, both Communion antiphons, and
  the scriptural bases of the acclamation and the Entrance antiphon.** The
  Douay–Rheims (Challoner) as registered above, whose per-book verse files for
  Isaias, Psalms, Matthew, John, Acts and Philippians were read in this stage;
  `…american-1899-ebible` is the other registered Douay printing. It is a
  study translation in Vulgate numbering and is not the proclaimed text; the
  standing notice of `guidance/liturgy/postconciliar-propers.md` is mandatory.
  Partial verses (Philippians 1:20c, 27a; Matthew 20:16a; Psalm 144:18a in the
  response) must be shown as partial, with the excluded words marked as
  context, never silently trimmed or extended. English must never be composed
  to stand for the adapted acclamation verse or for the Entrance antiphon.
- **Latin comparison text.** The Clementine Vulgate as registered above,
  public domain, for verse boundaries and for the wording of antiphon A. It is
  not the Missal's or the Lectionary's Latin.
- **Orations.** Latin incipit and an original description of what each prayer
  asks, cited to the owner. No rendering of the project's own, and no
  paraphrase close enough to reconstruct the approved English.
- **Entrance antiphon.** Latin incipit and description from the owner. It has
  no scriptural locator, so no Scripture translation supplies its English; the
  absence is stated at that element's own place.
- **Approved English.** Not reproduced in any of the three PDFs. The rights
  records that control it are `guidance/liturgical-text-publication-policy.md`
  and the `ot-25` rows of `src/sources/inventories/postconciliar-proper-translations-v1.toml`
  and `postconciliar-proper-latin-provenance-v1.toml`, which were read here as
  leads only.

The existing source library was read before anything was fetched, and it
sufficed for resolution. Five registered artifacts whose bytes the repository
identifies but does not hold were fetched again, whole, from their recorded
locations into ignored scratch space, matched to their registered hashes and
read: the national calendar, the 2002 Missal, the 2008 *Notitiae* issue, the
ICEL antiphon excerpt and the 1981 *Ordo*. The dated readings page and the two
GIRM chapter pages were read live; the GIRM responses differ by a few bytes
from the registered ones. Nothing fetched is retained, and no source was
registered, altered or bound in this stage.

## Remaining verification for research

- Complete the Week XXV owner's collation: register a passage record for the
  2002 artifact at physical PDF pp. 288–289; pursue the textual source and
  earlier liturgical use of *Salus populi ego sum* and test the psalm basis the
  ICEL excerpt's compiler names; establish the antecedents and redaction of the
  three orations; and record the limits that remain for the 2008 reprint and
  for a named United States altar book.
- Write `instance/manifest.md` and the leaf's `propers/verified.md` with the
  ordered inventory above, its keys and branch IDs, and
  `research/chronology-inputs.toml` with Hebrew Psalm 119:4–5 for antiphon A.
  The finding-aid index's `Psalm 118:4-5` must not override it.
- Decide how the adapted elements are displayed: Acts 16:14 as an identified
  basis beside a description of the adaptation, and the Entrance antiphon by
  incipit and description alone or with a labelled basis if research
  establishes one.
- Establish from an edition-identified witness why the appointment ends at
  Matthew 20:16a: which Latin and Greek texts carry the second sentence of
  v. 16 and which do not. No textual judgment is made in this record.
- Check whether the United States Lectionary admits another acclamation verse
  from a common set on Sundays in Ordinary Time. The daily page prints one
  verse; the rule was not examined here.
- Read each appointed passage in its complete biblical context, run the
  bounded reception sweep for every element in both Communion branches, and
  generate `research/chronology.toml` and `research/chronology-annotations.tex`
  through `tools/tpt proper-chronology`. No biblical date is asserted in this
  record.
- Register the dated USCCB readings page if the study relies on it beyond this
  record, bind the controlling sources in `research/source-bindings.toml`, and
  declare in `research/review-dependencies.toml` the external owners actually
  relied on: the Week XXV owner and the three edition registry records. The
  authorities adopted here are the USCCB 2026 calendar artifact; the 2002
  Missal artifact with its *Tempus per annum* rubrics and the *Normae
  universales* and General Calendar printed in it; the 2008 variation list in
  *Notitiae* 44; the ICEL antiphon excerpt; the 1981 *Ordo lectionum Missae*
  scan; the United States GIRM pages; the Douay–Rheims and Clementine
  editions; and, as computation inputs only,
  `src/sources/calendars/postconciliar/propers.yaml` and `rubrics.yaml`.
- One neighbouring library record was found inconsistent with its artifact and
  was not relied on: the registered passage for *Dominica XXVI per annum* gives
  physical pages 302–303 and printed pp. 487–488, but the artifact carries that
  heading at physical p. 289, and its own index places the Most Holy Trinity at
  printed p. 485. It belongs to its own owner and is unchanged here.

## Research re-entry, iteration 1 (19 September 2026)

The research stage re-read this record against its witnesses after review. The
five registered artifacts named above (national calendar, 2002 Missal, 2008
*Notitiae* issue, ICEL antiphon excerpt, 1981 *Ordo*) were fetched again whole
over verified TLS, matched to their registered SHA-256 values, and re-read at
every locus this record cites; the two GIRM chapters were read in responses
registered as new dated states. One error was found and corrected in place
above (the Spanish title list), and the *Ordo*'s tituli were added. Every
authority this record adopts is now bound in `research/source-bindings.toml`,
with passage records registered for the loci that had none. The dated USCCB
readings page was registered and bound as well: two requests were answered
with an HTTP 403 challenge page, and a third returned the page, whose 58,503
bytes are identical to the acquisition recorded by hash above. The row's
"Not registered in the source library" describes the state at context
resolution and is superseded by this paragraph.
