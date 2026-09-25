# Celebration context and complete appointed inventory

Resolved 24 September 2026 for the `proper-study` v7 production of the Claude
postconciliar leaf, run `ed9acebf389f8706`, seeded at commit
`8f5a1fa0fec4b255f89e124503b541bba816ecf5`. The production-plan line of
2026-09-24 authorizes provider `claude` for this exact identity as an
independent production. No research handoff was supplied. Every fact below was
established in this stage from the witnesses it names. No other leaf is
evidence here: not the Claude leaf for the Twenty-fifth Sunday, not any leaf
of the other provider, and no 1962 record. Nothing in this record comes from
the 1962 calendar, Missal or propers, including those for the same civil
Sunday. This record settles what is studied. It contains no study prose, spoken
text, timing claim or review verdict; research collates the sources and may
correct it from evidence.

## Identity, governing books and territory

| Field | Resolution |
| --- | --- |
| Canonical identity | `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s52-twenty-sixth-sunday-in-ordinary-time-year-a`; calendar family `postconciliar`, path family `temporal` |
| Stable registry | `guidance/liturgy/postconciliar-propers-registry.md`: parent `PC-S52`, Twenty-sixth Sunday in Ordinary Time, stem `pc-s52-twenty-sixth-sunday-in-ordinary-time`; registered keys `PC-S52-A`, `PC-S52-B`, `PC-S52-C` for Lectionary nos. 136, 137, 138 |
| Formula key and slug | `PC-S52-A`; full slug is the stem plus `-year-a`. No form, branch or occurrence suffix is admitted; the two forms of the second reading are branches inside this target, not keys |
| Registry checks | Ordinary Time Sunday `52 − 26 = 26`, hence owner `weeks/26`; Lectionary number `64 + 3 × (52 − 28) + 0 = 136`. Both agree with the dated witnesses below |
| Edition disposition | [Formula dispositions](../../../registry/formula-dispositions.md), row `PC-S52-A`, added in this stage: adopted as the stable registry lists it, with no cycle expansion. Dated result in [2026 occurrences](../../../registry/occurrences-2026.md) |
| Canonical Missal owner | [Ordinary Time Week XXVI](../../shared/ordinary-time/weeks/26/propers/verified.md), opened in this stage at the registry-fixed path and shared with the Year B and Year C targets. It alone carries the formulary's witnesses, locators, element boundaries, variation check and rights disposition; this record cites its result and restates none of its evidence |
| Build edge | Added to the collection Makefile in this stage: the owner above is a prerequisite of this identity's study, `-synthesis` and `-homily` PDFs, in a rule written against the provider-selected source root beside the existing Week XXV edge. `make -n -p PROVIDER=claude` was read after the change and resolves the prerequisite to the Claude owner above. The collection-wide edges on `shared/exposition-format.tex` and `registry/*.md` apply as well |
| Missal | *Roman Missal, Third Edition, for Use in the Dioceses of the United States of America*, English, implemented 27 November 2011; Latin base *Missale Romanum*, editio typica tertia (2002), in its *reimpressio emendata* (2008) |
| Lectionary | *Lectionary for Mass for Use in the Dioceses of the United States of America*, second typical edition (1998/2001), Volume I, no. 136, with the 2017 *Supplement* where applicable; based on the *Ordo lectionum Missae*, editio typica altera (1981), as emended. The national calendar's own front matter states this book identity (printed p. 5) |
| Other controlling books | *General Instruction of the Roman Missal*, United States English edition of 2011 with the 2021 emendations; *Universal Norms on the Liturgical Year and the Calendar*; the USCCB *Liturgical Calendar for the Dioceses of the United States of America* for 2026 |
| Territory | Dioceses of the United States of America, national calendar only. No diocesan, religious, parish, titular, dedication or patronal calendar was supplied, so none is applied, computed or excluded for an unnamed church |
| Language | The approved United States English governs the celebration. This production prints none of it: Scripture appears in the public-domain Douay–Rheims (Challoner) as a study translation, orations by Latin incipit and description |
| Requested study cycle | Year A, stated by the identity's `-year-a` suffix |
| Cycle appointed on the date | Year A, from 30 November 2025 through 22 November 2026. The requested and the appointed cycle coincide; no substitution is made or needed. The independent weekday cycle (II in this year) governs no Sunday and is not applicable |
| Homily audience | Adult parish assembly, for the later homily stage. The homily is authored preaching and adds no text to this inventory |

The finding-aid index `src/sources/calendars/postconciliar/propers.yaml`
carries this Mass as `ot-26`, `registry: pc-s52`. It is a lead, not a source of
record. Its own note marks all three antiphons as unread; its Communion
antiphon A lacks the Missal's *Cf.*; and its responsorial psalm carries the
Latin *Ordo*'s colon letters into Hebrew numbering (below, and the owner's
finding 2).

## Occurrence on 27 September 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
postconciliar --date 2026-09-27 --json` returns candidate `ot-26`, "the Sunday
of Ordinary Time week 26", season Ordinary Time, Sunday cycle A, weekday cycle
II, nothing unresolved, together with a second candidate, the memorial of Saint
Vincent de Paul. The anchors are those of
`guidance/liturgy/calendar-computation.md` for 2026: Easter 5 April, Pentecost
24 May, Christ the King 22 November, First Sunday of Advent 29 November.
Pentecost is the Sunday of resumed week `R = 34 − (22 November − 24 May) ÷ 7 =
34 − 26 = 8`, and 27 September falls eighteen weeks later: week 26. From the
other anchor, 27 September is eight weeks before the Sunday of week 34: again
week 26. The last week before Lent was the sixth (Sunday 15 February, Ash
Wednesday 18 February), so `R = L + 2`: this is a thirty-three-week year, week
7 never occurred, and nothing is renumbered. The national calendar corroborates
both ends in its own entries, read in this stage in its text layer: Sunday 15
February is its Sixth Sunday in Ordinary Time, and Monday 25 May carries the
label of the Eighth Week (the registered passage
`passage.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.ordinary-time-week-numbering`).
`Y = 2026`, and `2026 mod 3 = 1` is Year A.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
postconciliar --date 2026-09-27 --json` returns winner `ot-26`, a Sunday in
Ordinary Time at place 6 of the table of liturgical days, and one loser: the
obligatory memorial of Saint Vincent de Paul, Priest, place 10, disposition
omitted. Both loci were read in this stage in the Latin *Normae universales* as
printed in the registered 2002 Missal artifact (physical PDF pp. 70–71): the
table at no. 59, places 6 and 10, and no. 60, under which the higher place is
celebrated, only an impeded solemnity is transferred, and the remaining
celebrations are omitted for that year. The *Calendarium Romanum generale* in
the same artifact (physical PDF p. 79) inscribes the memorial on 27 September
with the rank *Memoria*. It is therefore omitted, not transferred, not
commemorated, and supplies no text to this Mass.

**Dated official witnesses.**

| Witness | Identity and check | What it states |
| --- | --- | --- |
| USCCB, *Liturgical Calendar for the Dioceses of the United States of America* 2026 | Registered artifact `artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.usccb-pdf-4bd9add0`. A copy fetched from the publisher on 24 September 2026 matched the registered SHA-256 `4bd9add07512396a2323aa977bc4816a5fad6348262e12740bcee97c77372d02` and 839,777 bytes before any page was read. Restricted; not retained | Printed p. 5 (PDF p. 7): Sunday cycle Year A, 30 November 2025 to 22 November 2026; weekday Cycle 2 from 25 May to 28 November 2026; the book identities given above. Printed p. 39 (PDF p. 41), read in a rendered page image and in the text layer: 27 September, Sunday, Twenty-Sixth Sunday in Ordinary Time, green; Ez 18:25-28 / Phil 2:1-11 or 2:1-5 / Mt 21:28-32; Lectionary (136); Psalter Week II. No other celebration and no bracketed optional memorial stands on the date. The whole text layer was searched for Saint Vincent de Paul: the English dated entries nowhere name him in 2026, and the only occurrence is the appended Spanish list *Títulos litúrgicos, Propio de los Santos*, which prints his title against 27 September on printed p. 56 (PDF p. 58). That is a list of approved titles by date, not a dated entry for 2026, and it changes nothing in the occurrence. No devotional designation or special observance is printed against the date |
| USCCB daily readings page for 27 September 2026, `https://bible.usccb.org/bible/readings/092726.cfm` | Complete page retrieved 24 September 2026 (59,014 bytes, SHA-256 `a220529b15c2248257ce939ab52393198535366e1b0793a6026361a2a2b3af55`), answered at the first request. Not registered in the source library; its wording is restricted and nothing of it is retained | Heading Twenty-sixth Sunday in Ordinary Time; Lectionary: 136; Reading 1 Ezekiel 18:25-28; Responsorial Psalm 25:4-5, 6-7, 8-9 with response locator (6a); Reading 2 Philippians 2:1-11, then "or" and Philippians 2:1-5; Alleluia John 10:27; Gospel Matthew 21:28-32. It prints one form of every unit except the second reading |

Computation and both dated witnesses agree; nothing fails closed. The printed
United States Lectionary volume itself was not inspected; the two official
USCCB witnesses stand for its content at no. 136, and the Latin *Ordo* below
corroborates every boundary, subject to the versification note on the psalm.

**The days around it.** The Sunday's readings, Gloria, Creed and Sunday Preface
do not continue into the week. The national calendar gives Monday 28 September
to the weekday course (no. 455) with two optional memorials, Tuesday 29
September to the Feast of Saints Michael, Gabriel and Raphael (no. 647), and
the rest of the week to memorials and ferias of the independent weekday course
(nos. 457–460, with the proper Gospel no. 650 on 2 October). The edition's
occurrence record carries the detail. Saturday 26 September is a weekday (no.
454); an anticipated Mass of the Sunday on Saturday evening uses this same
formulary and readings, is not a Vigil form, and has no key.

## Appointed inventory

Ten ritual places carry twelve text-bearing elements, because the second
reading has a longer and a shorter form and the Communion antiphon is a closed
pair. Missal elements are cited to the Week XXVI owner, whose record holds
their printed locators, incipits and summaries. Lectionary boundaries were read
in three places that agree in every figure: the two dated witnesses above and
the *Ordo lectionum Missae*, editio typica altera (1981), no. 136, *Dominica
vigesima sexta*, Year A, read on 24 September 2026 at 200 dpi in the page image
of printed p. 74 (artifact p. 128) of the registered scan
`artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e`
(SHA-256 `ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d`,
21,487,058 bytes, matched before reading). Psalms are cited in the Hebrew
numbering of the United States Lectionary with the Vulgate number, which the
Latin books and the Douay–Rheims use, in parentheses.

| Order | Key | Element and exact locus | Liturgical place, extent and boundary | Status |
| ---: | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | Entrance Antiphon *Omnia, quae fecisti nobis*; Week XXVI owner | Introductory Rites, at the entrance. The Missal cites Daniel 3:31, 29, 30, 43, 42, in the Vulgate numbering of the Greek addition to Daniel 3 (the Prayer of Azariah), and prints no *Cf.* The owner's collation shows a composite adaptation of those five verses, not a quotation of any of them | required |
| 2 | `collect` | Collect *Deus, qui omnipotentiam tuam*; Week XXVI owner | Concludes the Introductory Rites, after the Gloria; long conclusion | required |
| 3 | `first-reading` | Ezekiel 18:25–28; Lectionary no. 136 | Liturgy of the Word, first reading. Whole verses; one form only. The Latin *Ordo* prefixes the prophetic formula *Haec dicit Dominus* to v. 25, which itself opens on the people's complaint about the Lord's way | required |
| 4 | `responsorial-psalm` | Psalm 25 (24):4–5, 6–7, 8–9, response from v. 6a; Lectionary no. 136 | After the first reading. Three strophes; the response is the first half of v. 6 only. The Latin *Ordo* cites *Ps 24, 4bc-5*: the Vulgate's v. 4 opens with a colon on the confusion of the wicked that Hebrew numbering places at v. 3b, so Vulgate 4bc and Hebrew v. 4 are the same words, and the numbers from v. 5 onward coincide | required |
| 5a | `second-reading-long` | Philippians 2:1–11; Lectionary no. 136 | Second reading, longer form (*longior*), printed first. Through the hymn of vv. 6–11 | appointed alternative |
| 5b | `second-reading-short` | Philippians 2:1–5; Lectionary no. 136 | Second reading, shorter form (*brevior*), printed after "or". It ends at v. 5, before the hymn | appointed alternative |
| 6 | `gospel-acclamation` | Alleluia with verse John 10:27; Lectionary no. 136 | Before the Gospel. Printed without `Cf.`; the *Ordo*'s Latin verse inserts *dicit Dominus* into the saying, and the dated page carries the same insertion in English | required |
| 7 | `gospel` | Matthew 21:28–32; Lectionary no. 136 | Gospel. The parable of the two sons and its application to John's preaching. Whole verses. The Latin *Ordo* opens it with a liturgical incipit naming the chief priests and elders of the people as those addressed, whom the narrative introduces at 21:23. No shorter form | required |
| 8 | `prayer-over-offerings` | Prayer over the Offerings *Concede nobis, misericors Deus*; Week XXVI owner | Liturgy of the Eucharist, after the preparation of the gifts; short conclusion | required |
| 9a | `communion-antiphon-a` | Communion Antiphon, Cf. Psalm 119 (118):49–50; Week XXVI owner | At Communion. Printed first, with `Cf.` | appointed alternative |
| 9b | `communion-antiphon-b` | Communion Antiphon, 1 John 3:16; Week XXVI owner | At Communion. Printed second under *Vel:*, without `Cf.` | appointed alternative |
| 10 | `prayer-after-communion` | Prayer after Communion *Sit nobis, Domine, reparatio mentis et corporis*; Week XXVI owner | Concludes the Communion Rite; concludes with *Qui vivit et regnat*, not the short conclusion | required |

The formulary prints no Offertory antiphon, Sequence, proper Preface, proper
Eucharistic Prayer insert, prayer over the people or solemn blessing. The
Lectionary prints no alternative first reading, no shorter Gospel, no second
psalm response and no second acclamation verse for Year A.

**Boundary checks made against tracked Scripture.** The Douay–Rheims
(`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`)
and the Clementine Vulgate (`edition.catholic-church.vulgata-clementina.ebible-latvuc`)
were read at every boundary verse, and the tracked King James Version where
Hebrew numbering had to be confirmed.

- *Ezekiel 18.* Verse 24, on the just man who turns to iniquity, precedes the
  appointment, and v. 26 restates it within it. Verse 29 repeats the complaint
  of v. 25 and lies outside the appointment.
- *Psalm 24 (25).* In both tracked Vulgate-numbered texts v. 4 has three cola,
  the first on the confusion of those who act unjustly; in the King James
  Version that colon closes v. 3 and v. 4 has two cola. The *Ordo*'s *4bc* and
  the United States *4* therefore name the same words. Verse 5 in the
  Douay–Rheims and the Clementine ends with a third colon on waiting for the
  Lord all the day, and the dated page's first strophe does not visibly include
  a line corresponding to it, although both headings cite v. 5 whole. Whether
  the United States strophe is a partial v. 5 is left to research. The response
  agrees word for word with the Clementine's v. 6a.
- *Philippians 2.* Verse 1 opens with *ergo*, "therefore", joining the
  exhortation to 1:27–30, the chapter from which the previous Sunday's reading
  was taken; the *Ordo*'s incipit omits the particle. The shorter form ends at
  v. 5; the longer ends at v. 11, and v. 12 continues the exhortation.
- *John 10:27.* Neither tracked text has *dicit Dominus* or "says the Lord";
  v. 26, on those who do not believe because they are not his sheep, precedes
  it.
- *Matthew 21.* Verses 23–27, the question of Jesus' authority and of John's
  baptism, precede the appointment; v. 33 opens the next parable, which is the
  following Sunday's Gospel. Both tracked texts give the order in which the
  first son refuses and then goes, and the answer "the first". Whether Greek or
  Latin witnesses differ in the order of the sons or in the answer of v. 31 was
  not examined here.
- *Missal antiphons.* The Entrance antiphon's five Daniel verses, Psalm
  118:49–50 and 1 John 3:16 were compared with the Clementine by the owner, and
  its findings 1–3 record the result. Daniel 3:24–90 exists only in Bibles that
  print the Greek additions within Daniel; the King James Version's chapter 3
  has thirty verses, and its 3:29–30 are a different text.

These are observations about extent; the textual history of each is left to
research.

**Relationship classes, preliminary.** Under the 1981 *Praenotanda* nos.
105–107, read in this stage in page images of printed pp. XLIV–XLV, the first
reading is `officially correlated` with the Gospel, and the Gospel and the
second reading each belong to a `semi-continuous` course. Under GIRM 61–62 the
psalm is `responsorial` to the first reading and the verse before the Gospel is
`acclamatory`. *Tabella II* (printed p. LI, read in a page image) assigns
Philippians to the Twenty-fifth through Twenty-eighth Sundays of Year A, so
this Sunday is the second of that letter's course; the national calendar gives
Philippians 1:20c–24, 27a on 20 September and Philippians 4:6–9 on 4 October.
The Gospel's course runs from Matthew 20:1–16a on 20 September to Matthew
21:33–43 on 4 October. The Missal week's antiphons and orations are shared by
all three cycles. Every connection between them and the Year A readings is
editorial synthesis, as the three-document profile settles for every
formulary.

**The *Ordo*'s own tituli.** *Praenotanda* no. 106 says that the relation
between the readings of one Mass is shown by the careful choice of the tituli
set over the individual readings. At no. 136 (printed p. 74) the *Ordo* prints
three:

| Reading | Titulus | Source of the words |
| --- | --- | --- |
| Lectio I | *Cum averterit se impius ab impietate sua, animam suam vivificabit* | Ezekiel 18:27, condensed |
| Lectio II | *Sentite in vobis quod et in Christo Iesu* | Philippians 2:5, without the Clementine's opening *Hoc enim* |
| Evangelium | *Paenitentia motus abiit. Publicani et meretrices praecedunt vos in regnum Dei* | Matthew 21:29 and 21:31; the titulus has the present *praecedunt* where the Clementine reads the future *praecedent* |

These are edition-controlled evidence of what the Lectionary singles out in
each reading. For the first reading and the Gospel they are, on the *Ordo*'s own
account, how the official correlation is shown: the wicked man who turns from
his wickedness and lives is set beside the son who repented and went, and the
tax collectors and harlots who go before. The second reading's titulus belongs
to its semi-continuous course. They are evidence of the Lectionary's emphasis
within each reading and of that one correlation, not of a design joining the
Missal texts or the second reading to the rest.

## Branches and other text-bearing parts of this Mass

These branch IDs are proposed as the stable semantic IDs for the manifest, the
leaf audit and the resolution appendix. No local selection was supplied for
any of them, and none is inferred.

| Branch ID | Authority and trigger | Status | Places affected | Resolution |
| --- | --- | --- | --- | --- |
| `second-reading-long-form` | Lectionary no. 136 prints Philippians 2:1–11 as the longer form (*Ordo*: *longior*) | appointed alternative | 5 | Unselected. Under *Praenotanda* no. 80 (printed p. XXXVI, read in a page image) the choice between the two forms follows a pastoral criterion: the hearers' capacity to listen with profit to a longer or shorter reading, and to hear a fuller text to be explained in the homily. Both forms receive full treatment |
| `second-reading-short-form` | Lectionary no. 136 prints Philippians 2:1–5 as the shorter form (*Ordo*: *brevior*) | appointed alternative | 5 | Unselected; mutually exclusive with the longer form. It omits the hymn of vv. 6–11, so no claim resting on those verses holds for a celebration that uses it |
| `communion-antiphon-psalm` | The Missal prints Cf. Psalm 119 (118):49–50 first | appointed alternative | 9 | Unselected; both antiphons receive full treatment |
| `communion-antiphon-epistle` | The Missal prints 1 John 3:16 under *Vel:* | appointed alternative | 9 | Unselected. *Tempus per annum* rubric 6 prefers an antiphon that agrees with the Gospel of the Mass. Neither is drawn from a Gospel, and whether either agrees with Matthew 21:28–32 is a judgment the books do not make; none is made here |
| `entrance-or-communion-chant-substitution` | GIRM 48 and 87: in the United States the Missal antiphon, the *Graduale Romanum* or *Graduale Simplex* chant, or another approved chant | permitted | 1, 9 | Unselected. The Missal antiphons are the studied layer |
| `psalm-or-acclamation-chant-substitution` | GIRM 61 and 62 a: a sung psalm may come from the *Graduale Romanum*, the *Graduale Simplex* or another approved collection, and a seasonal common response and psalm may replace the proper one when the psalm is sung; the Alleluia verse from the Lectionary or the *Graduale* | permitted | 4, 6 | Unselected. The Lectionary's psalm and verse are the studied layer. With two readings before the Gospel, GIRM 63 does not apply |
| `offertory-chant` | GIRM 74, under the norms of no. 48 | permitted | preparation of the gifts | Unselected. The Missal prints no Offertory antiphon; that silence does not mean the rite has no chant |
| `sprinkling-rite` | GIRM 51 and the Order of Mass: on Sundays the blessing and sprinkling of water may replace the Penitential Act | ritual substitution | Introductory Rites | Unselected; it brings its own texts and adds no proper of this formulary |
| `compatible-preface-and-eucharistic-prayer` | *Tempus per annum* rubric 5; GIRM 364, 365 | permitted | Eucharistic Prayer | Unselected. One of the eight Prefaces of the Sundays in Ordinary Time with a compatible Eucharistic Prayer; a coupled choice |
| `eucharistic-prayer-iv-with-preface` | GIRM 365 d | conditional | Eucharistic Prayer | Unselected. If Prayer IV is chosen, its invariable Preface excludes a Sunday Preface |
| `concluding-blessing-form` | The Missal's solemn blessings and prayers over the people, usable at the priest's discretion (2002 artifact, physical pp. 370 and 379) | permitted | Concluding Rites | Unselected. None is appointed to this Sunday; the 2008 variation list adds alternative dismissal formulas to the Order of Mass, which are Ordinary and not proper |
| `local-proper-calendar` | Universal Norms 59–60 with a particular calendar: a proper solemnity, or a celebration lawfully assigned to this Sunday | conditional | whole Mass | Not supplied. An actual local celebration needs its own resolution and never a blended formulary |

| Place | Text and appointment | Status |
| --- | --- | --- |
| Gloria | Sung or said on Sundays outside Advent and Lent (rubric 4; GIRM 53) | required |
| Creed | Sung or said on Sundays (rubric 4; GIRM 68) | required |
| Homily; Universal Prayer | Authored or locally composed; no appointed text | not applicable |
| Memorial of Saint Vincent de Paul | Omitted under Universal Norms 60; no Collect, commemoration or reading enters this Mass | omitted |
| Sequence; proper Eucharistic Prayer insert | None appointed | not applicable |

## Lawful study-text routes

- **Scripture: the three readings in both forms of the second, the psalm, the
  acclamation verse, both Communion antiphons, and the Daniel verses on which
  the Entrance antiphon draws.** The Douay–Rheims (Challoner) as registered
  above, whose per-book verse files for Ezechiel, Psalms, Philippians, John,
  Matthew, Daniel and 1 John were read in this stage;
  `…american-1899-ebible` is the other registered Douay printing. It is a
  study translation in Vulgate numbering and is not the proclaimed text; the
  standing notice of `guidance/liturgy/postconciliar-propers.md` is mandatory.
  Partial verses (Psalm 24 (25):4, of which the appointment takes only the last
  two cola in Douay numbering, and v. 6a in the response) must be shown as
  partial, with the excluded words marked as context, never silently trimmed or
  extended. The two forms of the second reading are shown as two forms, not
  merged.
- **Adapted texts.** The Entrance antiphon and Communion antiphon A are
  adaptations. Douay–Rheims verses may stand beside each as its identified
  scriptural source, labelled as such and with the Missal's departures stated,
  never as the antiphon's own text. English must never be composed to stand for
  either antiphon, or for the speaker formula that the acclamation verse adds
  and neither tracked Bible has.
- **Latin comparison text.** The Clementine Vulgate as registered above,
  public domain, for verse boundaries and for comparing the antiphons. It is
  not the Missal's or the Lectionary's Latin.
- **Orations.** Latin incipit and an original description of what each prayer
  asks, cited to the owner. No rendering of the project's own, and no
  paraphrase close enough to reconstruct the approved English.
- **Approved English.** Not reproduced in any of the three PDFs. The rights
  records that control it are `guidance/liturgical-text-publication-policy.md`
  and the `ot-26` rows of `src/sources/inventories/postconciliar-proper-translations-v1.toml`
  and `postconciliar-proper-latin-provenance-v1.toml`, which were read here as
  leads only.

The existing source library was read before anything was fetched: the artifact
and passage records of the national calendar, the 2002 Missal, the 2008
*Notitiae* issue, the ICEL antiphon excerpt, the 1981 *Ordo* and the United
States GIRM, and the finding-aid and rights inventories named above. It
sufficed to identify every witness. Five registered artifacts whose bytes the
repository identifies but does not hold were fetched again, whole, from their
recorded locations into ignored scratch space, matched to their registered
hashes and read: the national calendar, the 2002 Missal, the 2008 *Notitiae*
issue, the ICEL antiphon excerpt and the 1981 *Ordo*. The dated readings page
and the two GIRM chapter pages were read live; the GIRM responses matched the
byte lengths of their 2026-09-19 registered states but not their hashes.
Nothing fetched is retained, and no source was registered, altered or bound in
this stage.

## Remaining verification for research

- Complete the Week XXVI owner's collation: register a correctly located
  passage record for the 2002 artifact at physical PDF pp. 289–290 (the
  existing record for *Dominica XXVI per annum* is mislocated; see below) and
  one for the ICEL excerpt's printed p. 79 as it bears on this week; establish
  which Latin text the Entrance antiphon's wording follows; establish the
  antecedents and redaction of the three orations, beginning with the
  translations inventory's lead that the Collect is verbatim in the Hadrianum;
  and record the limits that remain for the 2008 reprint and for a named United
  States altar book.
- Write `instance/manifest.md` and the leaf's `propers/verified.md` with the
  ordered inventory above, its keys and branch IDs, and
  `research/chronology-inputs.toml`. Three versification hazards bear on the
  chronology inputs: the psalm is Hebrew Psalm 25:4–9 whatever the *Ordo*'s
  colon letters; Communion antiphon A is Hebrew Psalm 119:49–50; and the
  Entrance antiphon's Daniel 3:29–31, 42–43 are verses of the Greek addition
  and must not be resolved against an Aramaic-numbered Daniel 3. The
  finding-aid index's `Psalm 25:4bc-5` must not override the first.
- Decide how the adapted elements are displayed: the Entrance antiphon and
  Communion antiphon A by incipit, description and labelled scriptural source;
  the acclamation verse with its added speaker formula identified.
- Establish whether the United States first strophe is a partial v. 5, from an
  edition-identified witness to the printed Lectionary; and whether the
  Lectionary admits another acclamation verse from a common set on Sundays in
  Ordinary Time. The daily page prints one verse; the rule was not examined
  here.
- Establish from edition-identified Greek and Latin witnesses the text of
  Matthew 21:28–32 that the Lectionary follows, including the order of the two
  sons and the answer in v. 31. No textual judgment is made in this record.
- Read each appointed passage in its complete biblical context, run the
  bounded reception sweep for every element in both second-reading forms and
  both Communion branches, and generate `research/chronology.toml` and
  `research/chronology-annotations.tex` through `tools/tpt proper-chronology`.
  No biblical date is asserted in this record.
- Register the dated USCCB readings page if the study relies on it beyond this
  record, bind the controlling sources in `research/source-bindings.toml`, and
  declare in `research/review-dependencies.toml` the external owners actually
  relied on: the Week XXVI owner and the three edition registry records. The
  authorities adopted here are the USCCB 2026 calendar artifact; the 2002
  Missal artifact with its *Tempus per annum* rubrics, the *Normae
  universales* and General Calendar printed in it, and its blessings and
  prayers over the people; the 2008 variation list in *Notitiae* 44; the ICEL
  antiphon excerpt; the 1981 *Ordo lectionum Missae* scan, including
  *Praenotanda* nos. 80 and 105–107 and *Tabella II*; the United States GIRM
  pages; the Douay–Rheims, Clementine and King James editions as read above;
  and, as computation inputs only,
  `src/sources/calendars/postconciliar/propers.yaml` and `rubrics.yaml`.
- Two neighbouring library records were found inconsistent with their
  artifacts and were not relied on. They belong to their own owners and are
  unchanged here. The registered passage for *Dominica XXVI per annum* gives
  physical pages 302–303 and printed pp. 487–488, but in the hash-matched
  artifact those pages carry the end of Christ the King, the heading stands at
  physical p. 289, and the artifact's index leaves no Ordinary Time Sunday at
  printed pp. 487–488; the record is bound only by another provider's 1962
  leaf. The registered passage for the calendar's Spanish September titles
  gives artifact page 57 and printed p. 55, but in the same hash-matched
  calendar the September list, including 20 and 27 September, stands on artifact
  page 58, printed p. 56; artifact page 57 carries June through the beginning
  of August.
