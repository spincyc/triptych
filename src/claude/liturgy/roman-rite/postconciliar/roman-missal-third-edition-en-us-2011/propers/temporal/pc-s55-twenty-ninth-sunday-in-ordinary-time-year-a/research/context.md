# Celebration context and complete appointed inventory

Resolved 16 October 2026 for the `proper-study` v11 production of the Claude
postconciliar leaf, run `4d16b5e19d25dad9`, seeded at commit
`fd99f7289aeb120b0a598e053dd292593a2f6576`. The production-plan line of
2026-10-16 authorizes provider `claude` for this exact identity as an
independent production. No research handoff was supplied. Every fact below was
established in this stage from the witnesses it names. No other leaf is
evidence here: not the Claude leaves for earlier Sundays, not the published
leaf of the other provider for this same identity, which was not opened, and no
1962 record. Nothing in this record comes from the 1962 calendar, Missal or
propers, including those for the same civil Sunday. This record settles what
is studied. It contains no study prose, spoken text, timing claim or review
verdict; research collates the sources and may correct it from evidence.

## Identity, governing books and territory

| Field | Resolution |
| --- | --- |
| Canonical identity | `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a`; calendar family `postconciliar`, path family `temporal` |
| Stable registry | `guidance/liturgy/postconciliar-propers-registry.md`: parent `PC-S55`, Twenty-ninth Sunday in Ordinary Time, stem `pc-s55-twenty-ninth-sunday-in-ordinary-time`; registered keys `PC-S55-A`, `PC-S55-B`, `PC-S55-C` for Lectionary nos. 145, 146, 147 |
| Formula key and slug | `PC-S55-A`; full slug is the stem plus `-year-a`. No form, branch or occurrence suffix is admitted. Every reading of no. 145 has one form only, so the target carries no reading branch |
| Registry checks | Ordinary Time Sunday `55 − 26 = 29`, hence owner `weeks/29`; Lectionary number `64 + 3 × (55 − 28) + 0 = 145`. Both agree with the dated witnesses below |
| Edition disposition | [Formula dispositions](../../../registry/formula-dispositions.md), row `PC-S55-A`, added in this stage: adopted as the stable registry lists it, with no cycle expansion. Dated result in [2026 occurrences](../../../registry/occurrences-2026.md), also added in this stage |
| Canonical Missal owner | [Ordinary Time Week XXIX](../../shared/ordinary-time/weeks/29/propers/verified.md), opened in this stage at the registry-fixed path and shared with the Year B and Year C targets. It alone carries the formulary's witnesses, locators, element boundaries, variation check and rights disposition; this record cites its result and restates none of its evidence |
| Build edge | The collection Makefile already declares, against the provider-selected source root, the Week XXIX owner as a prerequisite of this identity's study, `-synthesis` and `-homily` PDFs, in the rule after the Week XXVIII edge. No Makefile change was needed. `make -n -p PROVIDER=claude` was read after the owner was created and resolves the prerequisite to the Claude owner above. The collection-wide edges on `shared/exposition-format.tex` and `registry/*.md` apply as well |
| Missal | *Roman Missal, Third Edition, for Use in the Dioceses of the United States of America*, English, implemented 27 November 2011; Latin base *Missale Romanum*, editio typica tertia (2002), in its *reimpressio emendata* (2008) |
| Lectionary | *Lectionary for Mass for Use in the Dioceses of the United States of America*, second typical edition (1998/2001), Volume I, no. 145, with the 2017 *Supplement* where applicable; based on the *Ordo lectionum Missae*, editio typica altera (1981), as emended. The national calendar's own front matter states this book identity (printed p. 5) |
| Other controlling books | *General Instruction of the Roman Missal*, United States English edition of 2011 with the 2021 emendations, read in this stage in its official chapter pages (see the source paragraph below); *Universal Norms on the Liturgical Year and the Calendar* and the *Calendarium Romanum generale*, read in the Latin printed in the 2002 Missal; the USCCB *Liturgical Calendar for the Dioceses of the United States of America* for 2026 |
| Territory | Dioceses of the United States of America, national calendar only. No diocesan, religious, parish, titular, dedication or patronal calendar was supplied, so none is applied, computed or excluded for an unnamed church |
| Language | The approved United States English governs the celebration. This production prints none of it: Scripture appears in the public-domain Douay–Rheims (Challoner) as a study translation, orations by Latin incipit and description |
| Requested study cycle | Year A, stated by the identity's `-year-a` suffix |
| Cycle appointed on the date | Year A, from 30 November 2025 through 22 November 2026. The requested and the appointed cycle coincide; no substitution is made or needed. The independent weekday cycle (II in this year) governs no Sunday and is not applicable |
| Homily audience | Adult parish assembly, for the later homily stage. The homily is authored preaching and adds no text to this inventory |

The finding-aid index `src/sources/calendars/postconciliar/propers.yaml`
carries this Mass as `ot-29`, `registry: pc-s55`. It is a lead, not a source of
record. Its own note marks the antiphon citations and wording as uncollated.
Its Lectionary citations agree with the *Ordo* read below, including the
psalm's `9-10a, 10c`, given in Hebrew numbering by its declared convention. Its
antiphons keep the Missal's Vulgate numbering under its `citation_convention`;
Communion antiphon A carries an explicit `psalm_numbering: vulgate`, but the
Entrance antiphon (Psalm 16:6 and 16:8) carries none, so a reader applying the
file-level `psalm_numbering: hebrew` would resolve it to the wrong psalm. It
records no *Cf.* on either psalm antiphon. This record controls; the index
belongs to its own owner and is unchanged here.

## Occurrence on 18 October 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
postconciliar --date 2026-10-18 --json` returns candidate `ot-29`, "the Sunday
of Ordinary Time week 29", season Ordinary Time, Sunday cycle A, weekday cycle
II, nothing unresolved, together with a second candidate, the Feast of Saint
Luke, Evangelist. The anchors are those of
`guidance/liturgy/calendar-computation.md` for 2026: Easter 5 April, Pentecost
24 May, Christ the King 22 November, First Sunday of Advent 29 November.
Pentecost is the Sunday of resumed week `R = 34 − (22 November − 24 May) ÷ 7 =
34 − 26 = 8`, and 18 October falls twenty-one weeks later: week 29. From the
other anchor, 18 October is five weeks before the Sunday of week 34: again week
29. The last week before Lent was the sixth (Sunday 15 February, Ash Wednesday
18 February), so `R = L + 2`: this is a thirty-three-week year, week 7 never
occurred, and nothing is renumbered. The national calendar corroborates the
anchors in its own entries, read in this stage in its text layer: Ash
Wednesday, Pentecost and the First Sunday of Advent 2026 in its table of
principal celebrations (printed p. 5), Sunday 15 February as its Sixth Sunday
in Ordinary Time (printed p. 18), the entries after Pentecost Sunday labelled
the Eighth Week (printed p. 27), and 22 November as Our Lord Jesus Christ,
King of the Universe (printed p. 44). `Y = 2026`, and `2026 mod 3 = 1` is
Year A.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
postconciliar --date 2026-10-18 --json` returns winner `ot-29`, a Sunday in
Ordinary Time at place 6 of the table of liturgical days, and one loser: the
Feast of Saint Luke, Evangelist, place 7, disposition omitted. The governing
loci were read in this stage in the Latin *Normae universales* as printed in
the registered 2002 Missal artifact: no. 58 (physical PDF p. 70), no. 59 with
its table, places 4, 6, 7 and 8 (pp. 70–71), and no. 60 (p. 71), under which
the higher place is celebrated, only an impeded solemnity is transferred, and
the remaining celebrations are omitted for that year. The *Calendarium Romanum
generale* printed in the same artifact (physical PDF p. 79) inscribes 18
October *S. Lucae, evangelistae*, with the rank *Festum*. A feast of a saint of
the General Calendar stands at place 7, below the Sunday at place 6, so under
no. 60 it is omitted, not transferred and not commemorated, and supplies no
text to this Mass. No. 58 lets a Sunday per annum take a weekday celebration
dear to the faithful only where that celebration precedes the Sunday in the
table, which a feast at place 7 does not. A church of which Saint Luke is the
titular is a different case; see `local-proper-calendar` below.

**Dated official witnesses.**

| Witness | Identity and check | What it states |
| --- | --- | --- |
| USCCB, *Liturgical Calendar for the Dioceses of the United States of America* 2026 | Registered artifact `artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.usccb-pdf-4bd9add0`. A copy fetched from the publisher on 16 October 2026 matched the registered SHA-256 `4bd9add07512396a2323aa977bc4816a5fad6348262e12740bcee97c77372d02` and 839,777 bytes before any page was read. Restricted; not retained | Printed p. 5 (PDF p. 7): Sunday cycle Year A, 30 November 2025 to 22 November 2026; weekday Cycle 2 from 25 May to 28 November 2026; the book identities given above. Printed p. 41 (PDF p. 43), read in the text layer: 18 October, Sunday, Twenty-Ninth Sunday in Ordinary Time, green; Is 45:1, 4-6 / 1 Thes 1:1-5b / Mt 22:15-21; Lectionary (145); Psalter Week I. No other celebration and no bracketed optional memorial stands on the date, and no devotional designation, collection or special observance is printed against it. The whole text layer was searched for Luke: the English dated entries nowhere name the Feast of Saint Luke in 2026, and the only occurrence is the appended Spanish list *Títulos litúrgicos*, which prints *San Lucas, evangelista* against 18 October on printed p. 57 (PDF p. 59). That is a list of approved titles by date, not a dated entry for 2026, and it changes nothing in the occurrence |
| USCCB daily readings page for 18 October 2026, `https://bible.usccb.org/bible/readings/101826.cfm` | Complete page retrieved 16 October 2026 (58,047 bytes, SHA-256 `5e325b08b81338a7dd80227ecb6512a349ede493eb632a34723942c129768bd6`). A request with a browser user-agent was answered; a later request without one was refused (HTTP 403). The bytes match no registered state: the library's artifact `artifact.united-states-conference-of-catholic-bishops.daily-readings.2026-10-18-web-2026-10-13.usccb-101826-623dee42` records a 57,444-byte delivery of 13 October with another hash, which this stage could not compare because its bytes are not held. Restricted; nothing of its wording is retained | Heading Twenty-ninth Sunday in Ordinary Time; Lectionary: 145; Reading 1 Isaiah 45:1, 4-6; Responsorial Psalm 96:1, 3, 4-5, 7-8, 9-10 with response locator (7b); Reading 2 1 Thessalonians 1:1-5b; Alleluia Philippians 2:15d, 16a, without `Cf.`; Gospel Matthew 22:15-21. It prints one form of every unit. Its fourth psalm strophe carries v. 9 and the first and last clauses of v. 10, not the middle clause; see the boundary checks |

Computation and both dated witnesses agree on the celebration, the cycle, the
Lectionary number and every reading; nothing fails closed. The one
disagreement is internal to the dated page, between the psalm locator it
prints and the verses it gives, and the Latin *Ordo* decides the boundary. The
printed United States Lectionary volume itself was not inspected; the two
official USCCB witnesses stand for its content at no. 145, and the Latin *Ordo*
below corroborates every boundary.

**The days around it.** The Sunday's readings, Gloria, Creed and Sunday Preface
do not continue into the week. The national calendar (printed p. 41) gives Monday 19 October to the United States
Memorial of Saints John de Brébeuf and Isaac Jogues, Priests, and Companions,
Martyrs (no. 473), Tuesday 20 October to the weekday (no. 474) with the
optional United States memorial of Saint Paul of the Cross, Wednesday 21
October to the weekday (no. 475), Thursday 22 October to the weekday (no. 476)
with the optional memorial of Saint John Paul II, Friday 23 October to the
weekday (no. 477) with the optional memorial of Saint John of Capistrano, and
Saturday 24 October to the weekday (no. 478) with the optional memorials of
Saint Anthony Mary Claret and of the Blessed Virgin Mary, all from the
independent Cycle II course. The edition's occurrence record carries the
detail. Saturday 17 October is the Memorial of Saint Ignatius of Antioch (no.
472); an anticipated Mass of the Sunday on Saturday evening uses this same
formulary and readings, is not a Vigil form, and has no key.

## Appointed inventory

Ten ritual places carry eleven text-bearing elements, because the Communion
antiphon is a closed pair. Missal elements are cited to the Week XXIX owner,
whose record holds their printed locators, incipits and summaries. Lectionary
boundaries were read in three places that agree in every reading: the two
dated witnesses above and the *Ordo lectionum Missae*, editio typica altera
(1981), no. 145, *Dominica vigesima nona*, Year A, read on 16 October 2026 at
200 dpi in the page image of printed p. 79 (artifact p. 133) of the registered
scan
`artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e`
(SHA-256 `ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d`,
21,487,058 bytes, matched before reading). Under *Praenotanda* no. 119 and its
note 123 (printed p. XLVIII, read in the text layer) the *Ordo* numbers
chapters and verses after the *Nova Vulgata*, and psalms after the 1969 *Nova
Vulgata* psalter, which keeps the Vulgate psalm numbers. Psalms are cited here
in the Hebrew numbering of the United States Lectionary with the Vulgate number,
which the Latin books and the Douay–Rheims use, in parentheses.

| Order | Key | Element and exact locus | Liturgical place, extent and boundary | Status |
| ---: | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | Entrance Antiphon *Ego clamavi, quoniam exaudisti me, Deus*; Week XXIX owner | Introductory Rites, at the entrance. The Missal cites Cf. Psalm 16:6, 8 in Vulgate numbering (Hebrew 17:6, 8). The owner's collation shows an adaptation that passes over v. 7 and trims and supplements v. 8 | required |
| 2 | `collect` | Collect *Omnipotens sempiterne Deus, fac nos tibi semper*; Week XXIX owner | Concludes the Introductory Rites, after the Gloria; long conclusion | required |
| 3 | `first-reading` | Isaiah 45:1, 4–6; Lectionary no. 145 | Liturgy of the Word, first reading. One form only, in two segments: v. 1, then vv. 4–6, omitting vv. 2–3. It ends with the whole of v. 6. The *Ordo*'s incipit is *Haec dicit Dominus de uncto meo Cyro* | required |
| 4 | `responsorial-psalm` | Psalm 96 (95):1 and 3, 4–5, 7–8, 9–10a and 10c, response from v. 7b; Lectionary no. 145 | After the first reading. Four strophes; v. 2, v. 6 and the middle clause of v. 10 are not sung. The *Ordo* prints the locator as *Ps 95, 1 et 3. 4-5. 7-8. 9-10a et c* and the response as *Afferte Domino gloriam et potentiam*; the United States page prints the locator as 9–10. Hebrew and Vulgate verse numbers coincide in this psalm | required |
| 5 | `second-reading` | 1 Thessalonians 1:1–5b; Lectionary no. 145 | Second reading. One form only, the letter's opening. It ends within v. 5; the rest of v. 5 and vv. 6–10 are the next Sunday's reading (1:5c–10). The *Ordo* adds no liturgical incipit: it begins with the letter's own first words | required |
| 6 | `acclamation` | Alleluia with verse Philippians 2:15d, 16a; Lectionary no. 145 | Before the Gospel. Printed without `Cf.` in the *Ordo* and on the dated page. The *Ordo*'s Latin verse gives the last colon of v. 15 without its opening *inter quos* and the first colon of v. 16, in the indicative | required |
| 7 | `gospel` | Matthew 22:15–21; Lectionary no. 145 | Gospel. One form only. The Pharisees' plot, their disciples sent with the Herodians, the question of the tax to Caesar, the coin, and the closing saying of v. 21. It ends before v. 22. The Latin *Ordo* opens it with *In illo tempore* and names Jesus where the Clementine has *eum* | required |
| 8 | `prayer-over-offerings` | Prayer over the Offerings *Tribue nos, Domine, quaesumus, donis tuis*; Week XXIX owner | Liturgy of the Eucharist, after the preparation of the gifts; short conclusion | required |
| 9a | `communion-antiphon-a` | Communion Antiphon, Cf. Psalm 33 (32):18–19; Week XXIX owner | At Communion. Printed first, with `Cf.` Hebrew and Vulgate verse numbers coincide | appointed alternative |
| 9b | `communion-antiphon-b` | Communion Antiphon, Mark 10:45; Week XXIX owner | At Communion. Printed second under *Vel:*, without `Cf.`, though the owner's collation shows it adapted | appointed alternative |
| 10 | `prayer-after-communion` | Prayer after Communion *Fac nos, quaesumus, Domine, caelestium rerum*; Week XXIX owner | Concludes the Communion Rite; short conclusion | required |

The formulary prints no Offertory antiphon, Sequence, proper Preface, proper
Eucharistic Prayer insert, prayer over the people or solemn blessing. The
Lectionary prints no alternative or shorter form of any reading, no second
psalm response and no second acclamation verse for Year A.

**Boundary checks made against tracked Scripture.** The Douay–Rheims
(`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`)
and the Clementine Vulgate (`edition.catholic-church.vulgata-clementina.ebible-latvuc`)
were read at every boundary verse, and the tracked King James Version
(`edition.church-of-england.king-james-version.ebible-engkjv`) where Hebrew
numbering or verse division had to be confirmed.

- *Isaiah 44–45.* Isaiah 44:24–28 precedes the appointment and names Cyrus at
  44:28 as the Lord's shepherd who will see Jerusalem and the temple rebuilt;
  45:1 opens a new oracle addressed to Cyrus. The omitted vv. 2–3 promise that
  the Lord will go before him, break gates and give him hidden treasures, so
  that he may know who calls him by name. Verse 7, on forming light and
  creating darkness, making peace and creating evil, follows and lies outside
  the appointment. Verse numbers coincide in all three texts. In 45:1 the
  Clementine reads *christo meo Cyro*, where the *Ordo*'s incipit has *de uncto
  meo Cyro*; in 45:4 the Clementine has *assimilavi te*, which the Douay–Rheims renders
  "I have made a likeness of thee", where the King James Version has "I have
  surnamed thee". Which
  Latin text the *Ordo* follows, and how the Hebrew reads, are left to
  research.
- *Psalm 95 (96).* In the Clementine and the Douay–Rheims the psalm's title
  stands within v. 1, before *Cantate Domino canticum novum*; the tracked King
  James Version has no title. Verse numbers otherwise coincide in the three
  texts. Verse 10 has three clauses: the Lord reigns, he has set the world
  firm so that it will not be moved, and he will judge the peoples with
  equity. The *Ordo*'s `10a et c` takes the first and third, and the dated
  page's fourth strophe gives exactly those, whatever its locator says. The
  response is v. 7b: the Clementine's *afferte Domino gloriam et honorem*, the
  *Ordo*'s Latin response *gloriam et potentiam*, and the King James Version's
  "glory and strength" name the second gift differently, and the dated
  page's response and its own rendering of v. 7b in the third strophe differ
  in the same place. How the approved response stands to v. 7b is left to
  research. In v. 5 the Clementine and the Douay–Rheims call the gods of the
  nations demons where the King James Version calls them idols; that is a
  difference of text, also left to research.
- *1 Thessalonians 1.* The Clementine and the Douay–Rheims begin v. 2 with
  the greeting of grace and peace, which the King James Version, like the
  *Nova Vulgata* division the *Ordo* follows, keeps at the end of v. 1; the
  appointment includes both verses, so its extent is unaffected. Verse 5 has
  three parts: the gospel came not in word only (5a), but in power, in the Holy
  Spirit and in much fullness (5b), as the readers know what manner of men the
  missionaries were among them (5c). The appointment ends with 5b, and the
  national calendar gives 1:5c–10 for 25 October. The partial verse must be
  shown as partial.
- *Philippians 2:15–16.* In the Clementine and the Douay–Rheims v. 15 runs
  from being blameless and sincere children of God, through the crooked and
  perverse generation, to *inter quos lucetis sicut luminaria in mundo*; v. 16
  opens *verbum vitae continentes* and continues with Paul's glory in the day
  of Christ. 15d is the last colon of v. 15 and 16a the first colon of v. 16.
  The Clementine, the Douay–Rheims and the *Ordo*'s Latin verse state this in
  the indicative; the United States verse on the dated page is phrased as an
  exhortation. Whether the acclamation is therefore displayed as an adaptation
  is left to research.
- *Matthew 22.* Matthew 21:23 sets the scene in the temple, where the chief
  priests and elders question Jesus' authority; three parables follow, ending
  with the wedding feast of 22:1–14, the previous Sunday's Gospel. 22:15 opens
  with *Tunc abeuntes pharisaei*, which the *Ordo* replaces with *In illo
  tempore: Abeuntes pharisaei*; in the same sentence it writes *Iesum* for the
  Clementine's *eum*. Verse 22, where the questioners marvel and leave him, lies
  outside the appointment, and v. 23 opens the Sadducees' question about the
  resurrection. The national calendar gives Matthew 22:34–40 for 25 October,
  so the Sunday course passes over 22:22–33. Whether Greek or Latin witnesses
  differ in vv. 15–21 was not examined here.
- *Missal antiphons.* Psalm 16:6, 8, Psalm 32:18–19 and Mark 10:45 were
  compared with the Clementine by the owner, whose findings 1–3 record the
  results. In the King James Version the clause about those who rise up stands
  at the end of Psalm 17:7, so the Hebrew v. 8 begins where the antiphon's v. 8
  does.

These are observations about extent; the textual history of each is left to
research.

**Relationship classes, preliminary.** Under the 1981 *Praenotanda* nos.
105–107, read in this stage in the text layer of printed pp. XLIV–XLV, the
first reading is `officially correlated` with the Gospel, and the Gospel and
the second reading each belong to a `semi-continuous` course: Matthew in Year
A from the Third Sunday, and the apostolic letters as *Tabella II* distributes
them. Under GIRM 61–62 (United States English) the psalm is `responsorial`,
corresponding to the reading it follows, and the verse before the Gospel is
`acclamatory`. *Tabella II* (printed p. LI, read in the text layer) assigns
Philippians to the Twenty-fifth through Twenty-eighth Sundays of Year A and
First Thessalonians to the Twenty-ninth through Thirty-third, so this Sunday
opens the First Thessalonians course; the national calendar gives Philippians
4:12–14, 19–20 on 11 October and 1 Thessalonians 1:5c–10 on 25 October. The
Gospel's course runs from Matthew 22:1–14 on 11 October to Matthew 22:34–40
on 25 October. The Missal week's antiphons and orations are shared by all
three cycles. Every connection between them and the Year A readings is
editorial synthesis, as the three-document profile settles for every
formulary.

**The *Ordo*'s own tituli.** *Praenotanda* no. 106 says that the relation
between the readings of one Mass is shown by the careful choice of the tituli
set over the individual readings, and no. 123 (printed p. XLIX) that a titulus
indicates the chief theme of its reading and, where necessary, the link
between the readings of one Mass. At no. 145 (printed p. 79) the *Ordo*
prints three:

| Reading | Titulus | Source of the words |
| --- | --- | --- |
| Lectio I | *Apprehendi dexteram Cyri ut subiciam ante faciem eius gentes* | Isaiah 45:1, where the Clementine has *cujus apprehendi dexteram*; the titulus names Cyrus in place of the relative pronoun |
| Lectio II | *Memores fidei vestrae et caritatis et spei* | 1 Thessalonians 1:3, condensed; the Clementine has *memores operis fidei vestrae, et laboris, et caritatis, et sustinentiae spei* |
| Evangelium | *Reddite quae sunt Caesaris Caesari, et quae sunt Dei Deo* | Matthew 22:21, without the Clementine's *ergo* |

These are edition-controlled evidence of what the Lectionary singles out in
each reading. For the first reading and the Gospel they are, on the *Ordo*'s own
account, how the official correlation is shown: each titulus names a gentile
ruler, Cyrus grasped by the Lord's hand and Caesar given what is his. What the
correlation means is for research and the studies. The second reading's
titulus belongs to its semi-continuous course. They are evidence of the
Lectionary's emphasis within each reading and of that one correlation, not of
a design joining the Missal texts or the second reading to the rest.

**One cross-cycle fact bearing on rubric 6.** The *Ordo* at no. 146 (Year B,
same printed page) appoints Mark 10:45 as that year's acclamation verse and
Mark 10:35–45 or 10:42–45 as its Gospel. The Missal's second Communion
antiphon is therefore drawn from the Year B Gospel. In Year A neither antiphon
comes from Matthew 22:15–21, and whether either agrees with it, in the sense of
*Tempus per annum* rubric 6, is a judgment the books do not make. This stays in
the research records; it says nothing about why the antiphon was chosen.

## Branches and other text-bearing parts of this Mass

These branch IDs are proposed as the stable semantic IDs for the manifest, the
leaf audit and the resolution appendix. No local selection was supplied for
any of them, and none is inferred.

| Branch ID | Authority and trigger | Status | Places affected | Resolution |
| --- | --- | --- | --- | --- |
| `communion-antiphon-psalm` | The Missal prints Cf. Psalm 33 (32):18–19 first | appointed alternative | 9 | Unselected; both antiphons receive full treatment |
| `communion-antiphon-gospel` | The Missal prints Mark 10:45 under *Vel:* | appointed alternative | 9 | Unselected. *Tempus per annum* rubric 6 (2002 artifact, physical p. 268) prefers an antiphon that agrees with the Gospel of the Mass. This one is drawn from a Gospel, but not from the Year A Gospel; whether either antiphon agrees with Matthew 22:15–21 is a judgment the books do not make, and none is made here |
| `entrance-or-communion-chant-substitution` | GIRM 48 and 87 in the governing United States English, which give four options for each chant: (1) the Missal antiphon, or the *Graduale Romanum* antiphon with its psalm, in its own or another musical setting; (2) the antiphon and psalm of the *Graduale Simplex* for the liturgical time; (3) a chant from another collection of psalms and antiphons approved by the Conference of Bishops or the Diocesan Bishop, including psalms arranged in responsorial or metrical forms; (4) another suitable liturgical chant, likewise approved. Without singing, the Missal antiphon is recited (48) or may be recited (87) by the faithful, some of them, a reader or the priest | permitted | 1, 9 | Unselected. The Missal antiphons are the studied layer. A sung substitute replaces the antiphon's text at that celebration, so no claim resting on an antiphon's wording holds where it is not used |
| `psalm-or-acclamation-chant-substitution` | GIRM 61 and 62 a in the governing United States English: when the psalm is sung, a common response and psalm chosen for the time of year may replace the text corresponding to the reading; in the dioceses of the United States, instead of the Lectionary's psalm, there may be sung the Responsorial Gradual of the *Graduale Romanum*, the Responsorial or Alleluia Psalm of the *Graduale Simplex*, or an antiphon and psalm from another collection of psalms and antiphons, including psalms in metrical form, approved by the Conference of Bishops or the Diocesan Bishop; songs or hymns may not replace the Responsorial Psalm. The Alleluia verse is taken from the Lectionary or the *Graduale* (62 a). The *Ordo*'s common texts for sung psalms (nos. 173–174, printed pp. 97–98, read in the text layer) give common responses and psalms *per annum* and another psalm *in ultimis hebdomadis* | permitted | 4, 6 | Unselected. The Lectionary's psalm and verse are the studied layer. With two readings before the Gospel, GIRM 63 does not apply. The *Ordo* gives no common series of acclamation verses for the Sundays per annum (a bounded search of its text layer); *Praenotanda* no. 90 makes the verse either fixed for each Mass or chosen from a common series, and at no. 145 it is fixed |
| `offertory-chant` | GIRM 74 in the governing United States English: the Offertory chant accompanies the procession with the gifts at least until they are placed on the altar, its manner of singing follows the norms for the Entrance chant (no. 48, including its four United States options), and singing may accompany the rite even without a procession | permitted | preparation of the gifts | Unselected. The Missal prints no Offertory antiphon; that silence does not mean the rite has no chant |
| `sprinkling-rite` | GIRM 51 (United States English) and the Order of Mass: on Sundays the blessing and sprinkling of water may replace the Penitential Act | ritual substitution | Introductory Rites | Unselected; it brings its own texts and adds no proper of this formulary |
| `compatible-preface-and-eucharistic-prayer` | *Tempus per annum* rubric 5; GIRM 364, 365 (United States English) | permitted | Eucharistic Prayer | Unselected. One of the eight Prefaces of the Sundays in Ordinary Time with a compatible Eucharistic Prayer; a coupled choice |
| `eucharistic-prayer-iv-with-preface` | GIRM 365 d (United States English): an invariable Preface; usable on Sundays in Ordinary Time | conditional | Eucharistic Prayer | Unselected. If Prayer IV is chosen, its invariable Preface excludes a Sunday Preface |
| `concluding-blessing-form` | The Missal's solemn blessings and prayers over the people, usable at the priest's discretion under the rubric opening each section (2002 artifact, physical pp. 370 and 379) | permitted | Concluding Rites | Unselected. None is appointed to this Sunday |
| `mass-for-evangelization-of-peoples` | The Missal's Mass *Pro evangelizatione populorum* (Masses for Various Needs, no. 18; 2002 artifact, physical p. 695), whose own rubric admits it on Sundays per annum when particular celebrations for the work of the missions are held, unless a Sunday of Advent, Lent or Easter or a solemnity occurs | conditional | whole Mass | Not supplied. The national calendar prints no mission observance against 18 October, and this stage established no such celebration for the date from any witness. Were the Mass used, it would replace this formulary and nothing in this production would hold for it; its readings were not examined |
| `ritual-or-various-needs-mass` | GIRM 372 and 374 (United States English): the days on which no. 372 prohibits Ritual Masses do not include Sundays in Ordinary Time, and due regard is owed to the norms of the ritual books; and in graver need or for pastoral advantage, at the direction or with the permission of the Diocesan Bishop, an appropriate Mass may be celebrated on any day except those listed, which do not include Sundays in Ordinary Time | conditional | whole Mass | Not supplied. An actual replacement needs its own resolution and never a blended formulary |
| `local-proper-calendar` | Universal Norms 59–60 with a particular calendar: a proper solemnity at place 4, or a celebration lawfully assigned to this Sunday. On this date the case is concrete: in a church of which Saint Luke is the titular, the Solemnity of the Title (place 4 c) outranks the Sunday (place 6), while a feast of Saint Luke as principal patron of a diocese or region (place 8) does not | conditional | whole Mass | Not supplied. An actual local celebration needs its own resolution and never a blended formulary |

| Place | Text and appointment | Status |
| --- | --- | --- |
| Gloria | Sung or said on Sundays outside Advent and Lent (*Tempus per annum* rubric 4; GIRM 53) | required |
| Creed | Sung or said on Sundays (rubric 4; GIRM 68) | required |
| Homily; Universal Prayer | Authored or locally composed; no appointed text | not applicable |
| Feast of Saint Luke, Evangelist | Omitted under Universal Norms 60; no Collect, commemoration or reading enters this Mass | omitted |
| Sequence; proper Eucharistic Prayer insert | None appointed | not applicable |

*Praenotanda* no. 79 (printed p. XXXVI) contemplates a Conference of Bishops
permitting only two readings in some places. Whether any such permission
applies in the United States was not examined; no branch is recorded for it.

## Lawful study-text routes

- **Scripture: the three readings, the psalm, the acclamation verse's source,
  and the scriptural sources of all three antiphons.** The Douay–Rheims
  (Challoner) as registered above, whose verse files for Isaias 44–45, Psalms
  16, 32 and 95, 1 Thessalonians 1, Philippians 2, Matthew 21–22 and Mark 10
  were read in this stage; `…american-1899-ebible` is the other registered
  Douay printing. It is a study translation in Vulgate numbering and is not the
  proclaimed text; the standing notice of
  `guidance/liturgy/postconciliar-propers.md` is mandatory. Partial verses
  (Psalm 95 (96):10a and 10c, with 10b omitted; 1 Thessalonians 1:5b;
  Philippians 2:15d and 16a) must be shown as partial, with the excluded words
  marked as context, never silently trimmed or extended. The first reading's
  omitted Isaiah 45:2–3 and the psalm's omitted vv. 2 and 6 are marked as
  omissions, and the psalm's title, which stands within v. 1 in the Douay–Rheims,
  is not part of the first strophe. In 1 Thessalonians the Douay–Rheims carries
  the greeting at the start of v. 2; the appointment includes it either way.
- **Adapted texts.** The Entrance antiphon and both Communion antiphons are
  adaptations, and the acclamation verse's Latin is a recast extract.
  Douay–Rheims verses may stand beside each as its identified scriptural
  source, labelled as such and with the departures stated, never as the
  adapted text itself. English must never be composed to stand for any of
  them, for the Entrance antiphon's added vocative, or for the second Communion
  antiphon's shortened clause.
- **Latin comparison text.** The Clementine Vulgate as registered above,
  public domain, for verse boundaries and for comparing the antiphons and the
  acclamation verse. It is not the Missal's or the Lectionary's Latin.
- **Orations.** Latin incipit and an original description of what each prayer
  asks, cited to the owner. No rendering of the project's own, and no
  paraphrase close enough to reconstruct the approved English.
- **Approved English.** Not reproduced in any of the three PDFs. The rights
  records that control it are `guidance/liturgical-text-publication-policy.md`
  and the `ot-29` rows of `src/sources/inventories/postconciliar-proper-translations-v1.toml`
  and `postconciliar-proper-latin-provenance-v1.toml`, which were read here as
  leads only.

The existing source library was read before anything was fetched: the artifact
records of the national calendar, the 2002 Missal, the 2008 *Notitiae* issue,
the ICEL antiphon excerpt, the 1981 *Ordo* and the United States GIRM chapter
pages, and the finding-aid and rights inventories named above. Two
provider-neutral library records for this Sunday already existed, the edition
and artifact records of the dated readings page registered on 2026-10-13; they
were used only to identify that witness, and every statement here rests on
this stage's own reading. The library has no passage record for *Dominica XXIX
per annum* in the 2002 Missal artifact, for no. 145 in the *Ordo*, or for 18
October in the national calendar. Five registered artifacts whose bytes the
repository identifies but does not hold were fetched again, whole, from their
recorded locations into ignored scratch space, matched to their registered
hashes and read: the national calendar, the 2002 Missal, the 2008 *Notitiae*
issue, the ICEL antiphon excerpt and the 1981 *Ordo*. The dated readings page
was read live as described above. The United States GIRM chapter pages
answered HTTP 403 to a bare request and were then fetched whole over verified
HTTPS with browser request headers on 2026-10-16: chapter II (109,916 bytes,
SHA-256 `d10afff3888adfe8a0f397a792f5d07d941043f4d031fd89a492917facb580f1`),
read at nos. 48, 51, 53, 61–63, 68, 74 and 87; chapter VII (58,214 bytes,
SHA-256 `e803093d4b26fc530eedffa91377942edbe81cdd012858fae5014f0274aa9a2f`),
read at nos. 363–365; and chapter VIII (53,383 bytes, SHA-256
`273fc7cbcd1ddea3c3f4f077b4cdfa3a4a74a0a3959f69ea6a1070f0b9761d28`), read at
nos. 368–376. None of the three states matches a registered artifact. The
branch rows above follow the United States English, which governs. Nothing
fetched is retained; the protected English is described, not transcribed.

## Remaining verification for research

- Complete the Week XXIX owner's collation: register passage records for the
  2002 artifact at physical PDF pp. 291–292 and for the ICEL excerpt's printed
  p. 81; compare the three antiphons with the *Nova Vulgata*; establish the
  antecedents of the three orations, beginning with the translations
  inventory's leads that the Collect is verbatim in the Old Gelasian and the
  Prayer over the Offerings nearly so in the Verona sacramentary; and say what,
  if anything, the repeated wording the owner records means for this formulary
  (the Entrance antiphon on Tuesday of the Third Week of Lent, the shared
  closing clause with Week IX's Prayer over the Offerings, the Mark antiphon in
  the Common of Pastors).
- Bind the readings page, GIRM chapter II, chapter VII and chapter VIII states
  actually relied on in `research/source-bindings.toml`, registering the states
  read here or re-reading registered ones. None of the four states read in this
  stage is registered.
- Write `instance/manifest.md` and the leaf's `propers/verified.md` with the
  ordered inventory above, its keys and branch IDs, and
  `research/chronology-inputs.toml`. Numbering hazards for the chronology
  inputs: the Entrance antiphon is Hebrew Psalm 17:6, 8, and the finding-aid
  index gives it as Psalm 16 without a per-entry Vulgate flag; Communion
  antiphon A is Hebrew Psalm 33:18–19; the responsorial psalm is Hebrew Psalm
  96, the *Ordo*'s Psalm 95, with v. 10 partial (10a, 10c); the second reading
  ends at 1 Thessalonians 1:5b; the acclamation is Philippians 2:15d, 16a.
- Establish, from an edition-identified witness to the printed Lectionary, how
  the approved psalm locator stands to the verses actually sung (9–10 against
  9–10a, c) and how the approved response stands to v. 7b and to the *Ordo*'s
  *gloriam et potentiam*.
- Decide how the adapted elements are displayed: the three antiphons by
  incipit, description and labelled scriptural source; the acclamation verse
  with its excerpting and its mood identified.
- Establish from edition-identified Latin, Greek and Hebrew witnesses the text
  the Lectionary follows at the points marked above: Isaiah 45:1 (*uncto*
  against *christo*) and 45:4, Psalm 96 (95):5 and 7b, and Matthew 22:15–21. No
  textual judgment is made in this record.
- Read each appointed passage in its complete biblical context, run the
  bounded reception sweep for every element and both Communion branches, and
  generate `research/chronology.toml` and
  `research/chronology-annotations.tex` through `tools/tpt proper-chronology`.
  No biblical date is asserted in this record.
- Declare in `research/review-dependencies.toml` the external owners actually
  relied on: the Week XXIX owner and the three edition registry records. The
  authorities adopted here are the USCCB 2026 calendar artifact; the USCCB
  readings page for the date; the 2002 Missal artifact with its *Tempus per
  annum* rubrics, the *Normae universales* and General Calendar printed in it,
  its blessings and prayers over the people, and its Mass for the
  Evangelization of Peoples; the United States English GIRM, chapters II, VII
  and VIII, in the states read here; the 2008 variation list in *Notitiae* 44;
  the ICEL antiphon excerpt; the 1981 *Ordo lectionum Missae* scan, including
  *Praenotanda* nos. 79, 89–90, 105–107, 119 and 123, *Tabella II*, and
  nos. 145–146 and 173–174; the Douay–Rheims, Clementine and King James
  editions as read above; and, as computation inputs only,
  `src/sources/calendars/postconciliar/propers.yaml` and `rubrics.yaml`.
- If the studies mention a mission observance on this Sunday, it needs a dated
  witness first; this record establishes none.
