# Celebration context and complete appointed inventory

Resolved 8 October 2026 for the `proper-study` v9 production of the Claude
postconciliar leaf, run `0b0f756d95e3ee20`, seeded at commit
`643a137fb493003f1d9928036b870ce96d0240e3`. The production-plan line of
2026-10-08 authorizes provider `claude` for this exact identity as an
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
| Canonical identity | `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s54-twenty-eighth-sunday-in-ordinary-time-year-a`; calendar family `postconciliar`, path family `temporal` |
| Stable registry | `guidance/liturgy/postconciliar-propers-registry.md`: parent `PC-S54`, Twenty-eighth Sunday in Ordinary Time, stem `pc-s54-twenty-eighth-sunday-in-ordinary-time`; registered keys `PC-S54-A`, `PC-S54-B`, `PC-S54-C` for Lectionary nos. 142, 143, 144 |
| Formula key and slug | `PC-S54-A`; full slug is the stem plus `-year-a`. No form, branch or occurrence suffix is admitted; the two forms of the Gospel are branches inside this target, not keys |
| Registry checks | Ordinary Time Sunday `54 − 26 = 28`, hence owner `weeks/28`; Lectionary number `64 + 3 × (54 − 28) + 0 = 142`. Both agree with the dated witnesses below |
| Edition disposition | [Formula dispositions](../../../registry/formula-dispositions.md), row `PC-S54-A`, added in this stage: adopted as the stable registry lists it, with no cycle expansion. Dated result in [2026 occurrences](../../../registry/occurrences-2026.md) |
| Canonical Missal owner | [Ordinary Time Week XXVIII](../../shared/ordinary-time/weeks/28/propers/verified.md), opened in this stage at the registry-fixed path and shared with the Year B and Year C targets. It alone carries the formulary's witnesses, locators, element boundaries, variation check and rights disposition; this record cites its result and restates none of its evidence |
| Build edge | The collection Makefile already declares, against the provider-selected source root, the Week XXVIII owner as a prerequisite of this identity's study, `-synthesis` and `-homily` PDFs, in the rule beside the Week XXVII edge. No Makefile change was needed. `make -n -p PROVIDER=claude` was read after the owner was created and resolves the prerequisite to the Claude owner above. The collection-wide edges on `shared/exposition-format.tex` and `registry/*.md` apply as well |
| Missal | *Roman Missal, Third Edition, for Use in the Dioceses of the United States of America*, English, implemented 27 November 2011; Latin base *Missale Romanum*, editio typica tertia (2002), in its *reimpressio emendata* (2008) |
| Lectionary | *Lectionary for Mass for Use in the Dioceses of the United States of America*, second typical edition (1998/2001), Volume I, no. 142, with the 2017 *Supplement* where applicable; based on the *Ordo lectionum Missae*, editio typica altera (1981), as emended. The national calendar's own front matter states this book identity (printed p. 5) |
| Other controlling books | *General Instruction of the Roman Missal*, United States English edition of 2011 with the 2021 emendations. This record first read its numbers in the Latin text printed in the 2002 Missal; the research re-entry of 8 October 2026 read the governing United States English in hash-identified states, and the branch rows below now rest on it (see the source paragraph below); *Universal Norms on the Liturgical Year and the Calendar*; the USCCB *Liturgical Calendar for the Dioceses of the United States of America* for 2026 |
| Territory | Dioceses of the United States of America, national calendar only. No diocesan, religious, parish, titular, dedication or patronal calendar was supplied, so none is applied, computed or excluded for an unnamed church |
| Language | The approved United States English governs the celebration. This production prints none of it: Scripture appears in the public-domain Douay–Rheims (Challoner) as a study translation, orations by Latin incipit and description |
| Requested study cycle | Year A, stated by the identity's `-year-a` suffix |
| Cycle appointed on the date | Year A, from 30 November 2025 through 22 November 2026. The requested and the appointed cycle coincide; no substitution is made or needed. The independent weekday cycle (II in this year) governs no Sunday and is not applicable |
| Homily audience | Adult parish assembly, for the later homily stage. The homily is authored preaching and adds no text to this inventory |

The finding-aid index `src/sources/calendars/postconciliar/propers.yaml`
carries this Mass as `ot-28`, `registry: pc-s54`. It is a lead, not a source of
record. Its own note marks the antiphon citations and wording as uncollated; it
gives the antiphons in the Missal's Vulgate numbering and the responsorial
psalm in Hebrew numbering, as its declared convention says; its Communion
antiphon A lacks the Missal's *Cf.* and its Gospel acclamation lacks the
*Ordo*'s *Cf.*; and it keeps the shorter Gospel only in a note. This record
controls; the index belongs to its own owner and is unchanged here.

## Occurrence on 11 October 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
postconciliar --date 2026-10-11 --json` returns candidate `ot-28`, "the Sunday
of Ordinary Time week 28", season Ordinary Time, Sunday cycle A, weekday cycle
II, nothing unresolved, together with a second candidate, the optional memorial
of Saint John XXIII, Pope. The anchors are those of
`guidance/liturgy/calendar-computation.md` for 2026: Easter 5 April, Pentecost
24 May, Christ the King 22 November, First Sunday of Advent 29 November.
Pentecost is the Sunday of resumed week `R = 34 − (22 November − 24 May) ÷ 7 =
34 − 26 = 8`, and 11 October falls twenty weeks later: week 28. From the other
anchor, 11 October is six weeks before the Sunday of week 34: again week 28.
The last week before Lent was the sixth (Sunday 15 February, Ash Wednesday 18
February), so `R = L + 2`: this is a thirty-three-week year, week 7 never
occurred, and nothing is renumbered. The national calendar corroborates both
ends in its own entries, read in this stage in its text layer: Sunday 15
February is its Sixth Sunday in Ordinary Time (printed p. 18), and the entries
after Pentecost Sunday carry the label of the Eighth Week (printed p. 27).
`Y = 2026`, and `2026 mod 3 = 1` is Year A.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
postconciliar --date 2026-10-11 --json` returns winner `ot-28`, a Sunday in
Ordinary Time at place 6 of the table of liturgical days, and one loser: the
optional memorial of Saint John XXIII, Pope, place 12, disposition omitted.
The governing loci were read in this stage in the Latin *Normae universales* as
printed in the registered 2002 Missal artifact: no. 14 (physical PDF p. 65), no.
59 (p. 70) with its table, places 6, 10, 11 and 12 (p. 71), and no. 60 (p. 71),
under which the higher place is celebrated, only an impeded solemnity is
transferred, and the remaining celebrations are omitted for that year. The
*Calendarium Romanum generale* printed in the same artifact (physical PDF p. 79)
leaves 11 October empty: the memorial is a later inscription in the General
Calendar, and the act that inscribed it was not read in this stage. Its rank
therefore rests on the finding aid alone; but every memorial stands at place
10, 11 or 12, below the Sunday at place 6, so under no. 60 it is omitted,
not transferred, not commemorated, and supplies no text to this Mass whatever
its exact rank.

**Dated official witnesses.**

| Witness | Identity and check | What it states |
| --- | --- | --- |
| USCCB, *Liturgical Calendar for the Dioceses of the United States of America* 2026 | Registered artifact `artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.usccb-pdf-4bd9add0`. A copy fetched from the publisher on 8 October 2026 matched the registered SHA-256 `4bd9add07512396a2323aa977bc4816a5fad6348262e12740bcee97c77372d02` and 839,777 bytes before any page was read. Restricted; not retained | Printed p. 5 (PDF p. 7): Sunday cycle Year A, 30 November 2025 to 22 November 2026; weekday Cycle 2 from 25 May to 28 November 2026; the book identities given above. Printed p. 40 (PDF p. 42), read in a rendered page image and in the text layer: 11 October, Sunday, Twenty-Eighth Sunday in Ordinary Time, green; Is 25:6-10a / Phil 4:12-14, 19-20 / Mt 22:1-14 or 22:1-10; Lectionary (142); Psalter Week IV. No other celebration and no bracketed optional memorial stands on the date. The whole text layer was searched for John XXIII: the English dated entries nowhere name him in 2026, and the only occurrence is the appended Spanish list *Títulos litúrgicos*, which prints his title against 11 October on printed p. 57 (PDF p. 59). That is a list of approved titles by date, not a dated entry for 2026, and it changes nothing in the occurrence. The calendar's list of proper United States celebrations has no entry for 11 October, and no devotional designation or special observance is printed against the date |
| USCCB daily readings page for 11 October 2026, `https://bible.usccb.org/bible/readings/101126.cfm` | Complete page retrieved 8 October 2026 (60,371 bytes, SHA-256 `9e5efac5f7c81db419919ce4f4870cacc9769c9b6fc58f82ab90628d1fbf6d98`), answered at the first request. The bytes are identical to the registered artifact `artifact.united-states-conference-of-catholic-bishops.daily-readings.2026-10-11-web-2026-10-06.lectionary142-html-9e5efac5`. Restricted; nothing of its wording is retained | Heading Twenty-eighth Sunday in Ordinary Time; Lectionary: 142; Reading 1 Isaiah 25:6-10a; Responsorial Psalm 23:1-3a, 3b-4, 5, 6 with response locator (6cd); Reading 2 Philippians 4:12-14, 19-20; Alleluia Cf. Ephesians 1:17-18; Gospel Matthew 22:1-14, then "or" and Matthew 22:1-10. It prints one form of every unit except the Gospel |

Computation and both dated witnesses agree; nothing fails closed. The printed
United States Lectionary volume itself was not inspected; the two official
USCCB witnesses stand for its content at no. 142, and the Latin *Ordo* below
corroborates every boundary.

**The days around it.** The Sunday's readings, Gloria, Creed and Sunday Preface
do not continue into the week. The national calendar (printed pp. 40–41) gives
Monday 12 and Tuesday 13 October to the weekday course (nos. 467, 468),
Wednesday 14 October to the weekday (no. 469) with the optional memorial of
Saint Callistus I, Thursday 15 October to the Memorial of Saint Teresa of Jesus
(no. 470), Friday 16 October to the weekday (no. 471) with two optional
memorials, and Saturday 17 October to the Memorial of Saint Ignatius of
Antioch (no. 472), all from the independent Cycle II course. The edition's
occurrence record carries the detail. Saturday 10 October is a weekday (no. 466)
with the optional Saturday memorial of the Blessed Virgin Mary; an anticipated
Mass of the Sunday on Saturday evening uses this same formulary and readings,
is not a Vigil form, and has no key.

## Appointed inventory

Ten ritual places carry twelve text-bearing elements, because the Gospel has a
longer and a shorter form and the Communion antiphon is a closed pair. Missal
elements are cited to the Week XXVIII owner, whose record holds their printed
locators, incipits and summaries. Lectionary boundaries were read in three
places that agree in every figure: the two dated witnesses above and the *Ordo
lectionum Missae*, editio typica altera (1981), no. 142, *Dominica vigesima
octava*, Year A, read on 8 October 2026 at 200 dpi in the page image of printed
p. 77 (artifact p. 131) of the registered scan
`artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e`
(SHA-256 `ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d`,
21,487,058 bytes, matched before reading). Psalms are cited in the Hebrew
numbering of the United States Lectionary with the Vulgate number, which the
Latin books and the Douay–Rheims use, in parentheses.

| Order | Key | Element and exact locus | Liturgical place, extent and boundary | Status |
| ---: | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | Entrance Antiphon *Si iniquitates observaveris, Domine*; Week XXVIII owner | Introductory Rites, at the entrance. The Missal cites Psalm 129:3–4 in Vulgate numbering (Hebrew 130:3–4) and prints no *Cf.* The owner's collation shows v. 3 and the first colon of v. 4 followed by a closing vocative that the Clementine psalm does not have: an adaptation, not a quotation | required |
| 2 | `collect` | Collect *Tua nos, quaesumus, Domine, gratia*; Week XXVIII owner | Concludes the Introductory Rites, after the Gloria; long conclusion | required |
| 3 | `first-reading` | Isaiah 25:6–10a; Lectionary no. 142 | Liturgy of the Word, first reading. One form only. It ends with the first clause of v. 10, on the hand of the Lord resting on the mountain; the *Ordo*'s explicit is *in monte isto*, and the rest of v. 10, on Moab, is excluded | required |
| 4 | `responsorial-psalm` | Psalm 23 (22):1–3a, 3b–4, 5, 6, response from v. 6cd; Lectionary no. 142 | After the first reading. Four strophes, the first ending and the second beginning within v. 3. Hebrew and Vulgate verse numbers coincide in this psalm. The Latin *Ordo* prints the response as *Inhabitabo in domo Domini, in longitudinem dierum*, an adaptation of v. 6cd; on the United States response see the boundary checks | required |
| 5 | `second-reading` | Philippians 4:12–14, 19–20; Lectionary no. 142 | Second reading. Two segments; vv. 15–18 are omitted between them. One form only. The *Ordo* opens it with the liturgical incipit *Fratres* | required |
| 6 | `gospel-acclamation` | Alleluia with verse Cf. Ephesians 1:17–18; Lectionary no. 142 | Before the Gospel. Printed with `Cf.` in the *Ordo* and on the dated page. The *Ordo*'s Latin verse recasts Paul's prayer for his readers as a prayer of the assembly in the first person plural and shortens it | required |
| 7a | `gospel-long` | Matthew 22:1–14; Lectionary no. 142 | Gospel, longer form (*longior*), printed first. The parable of the wedding feast through the guest without a wedding garment and the closing saying of v. 14. The Latin *Ordo* opens it with a liturgical incipit naming the chief priests and elders of the people as those addressed, whom the narrative introduces at 21:23 | appointed alternative |
| 7b | `gospel-short` | Matthew 22:1–10; Lectionary no. 142 | Gospel, shorter form (*brevior*), printed after "or". It ends at v. 10, with the hall filled, before vv. 11–14 | appointed alternative |
| 8 | `prayer-over-offerings` | Prayer over the Offerings *Suscipe, Domine, fidelium preces*; Week XXVIII owner | Liturgy of the Eucharist, after the preparation of the gifts; short conclusion | required |
| 9a | `communion-antiphon-a` | Communion Antiphon, Cf. Psalm 34 (33):11; Week XXVIII owner | At Communion. Printed first, with `Cf.` The verse is 34:10 in English Bibles that do not number the psalm's title | appointed alternative |
| 9b | `communion-antiphon-b` | Communion Antiphon, 1 John 3:2; Week XXVIII owner | At Communion. Printed second under *Vel:*, without `Cf.`, though the owner's collation shows it adapted | appointed alternative |
| 10 | `prayer-after-communion` | Prayer after Communion *Maiestatem tuam, Domine, suppliciter deprecamur*; Week XXVIII owner | Concludes the Communion Rite; short conclusion | required |

The formulary prints no Offertory antiphon, Sequence, proper Preface, proper
Eucharistic Prayer insert, prayer over the people or solemn blessing. The
Lectionary prints no alternative first reading, no shorter second reading, no
second psalm response and no second acclamation verse for Year A.

**Boundary checks made against tracked Scripture.** The Douay–Rheims
(`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`)
and the Clementine Vulgate (`edition.catholic-church.vulgata-clementina.ebible-latvuc`)
were read at every boundary verse, and the tracked King James Version
(`edition.church-of-england.king-james-version.ebible-engkjv`) where Hebrew
numbering had to be confirmed.

- *Isaiah 25.* Verses 1–5, a song of thanks for the fall of a fortified city,
  precede the appointment; v. 6 opens with *et*, "and", joining the banquet to
  that song and to the Lord's reign on Mount Sion at 24:23. Verse 10 has two
  clauses in all three texts: the hand of the Lord resting on the mountain, and
  Moab trodden down. The appointment takes the first; vv. 10b–12 on Moab lie
  outside it. The partial verse must be shown as partial.
- *Psalm 22 (23).* In the Clementine, the Douay–Rheims and the King James
  Version the verse numbers coincide, the title standing within v. 1 in the
  two Vulgate-numbered texts and absent from the tracked King James text.
  Verse 3 has two cola,
  the restoring of the soul and the leading in paths of justice, so 3a and 3b
  name them respectively. Verse 6 has four: mercy following all the days of
  life, and dwelling in the house of the Lord for length of days; 6cd is the
  second pair. The *Ordo*'s Latin response follows 6cd. The response printed on
  the dated United States page also speaks of the whole span of life, which in
  both Vulgate-numbered texts belongs to 6ab, while it gives the locator 6cd;
  how the approved response stands to the verse is left to research.
- *Philippians 4.* Verses 10–11, Paul's joy at the Philippians' renewed care
  and his having learned contentment, precede v. 12, which continues that
  thought; vv. 15–18, on their past gifts and the gift brought by
  Epaphroditus, are omitted between the two segments; v. 20 is a doxology
  ending in *Amen*, and vv. 21–23 are the letter's closing greetings. The
  previous Sunday's reading was Philippians 4:6–9.
- *Ephesians 1:17–18.* In the Clementine the prayer is in the second person
  plural and speaks of *Deus Domini nostri Jesu Christi, Pater gloriae* giving a
  spirit of wisdom and revelation, with eyes of the heart enlightened to know
  the hope of *his* calling. The *Ordo*'s verse names the Father of our Lord
  Jesus Christ as subject, omits the spirit of wisdom and revelation, and puts
  the enlightening and the hope of *our* calling in the first person plural. It
  is an adaptation, as its *Cf.* says.
- *Matthew 22.* Matthew 21:33–46 precedes the appointment, ending with the
  chief priests and Pharisees recognizing that the parables were spoken about
  them; 22:1 opens *Et respondens Jesus, dixit iterum in parabolis eis*. The
  shorter form ends at v. 10; the longer at v. 14; v. 15 opens the question of
  the tribute, which is the following Sunday's Gospel. The *Ordo*'s incipit
  names the addressees with the words of 21:23, not those of 21:45. Whether
  Greek or Latin witnesses differ in vv. 1–14 was not examined here.
- *Missal antiphons.* Psalm 129:3–4, Psalm 33:11 and 1 John 3:2 were compared
  with the Clementine by the owner, and its findings 1–3 record the results. In
  the King James Version Psalm 34:10 has young lions where the Vulgate-numbered
  texts have the rich; that is a difference of text, not only of numbering, and
  is left to research.

These are observations about extent; the textual history of each is left to
research.

**Relationship classes, preliminary.** Under the 1981 *Praenotanda* nos.
105–107, read in this stage in page images of printed pp. XLIV–XLV, the first
reading is `officially correlated` with the Gospel, and the Gospel and the
second reading each belong to a `semi-continuous` course. Under GIRM 61–62 (in
the Latin and in the United States English alike) the psalm is `responsorial`
to the first reading and the verse before the Gospel is `acclamatory`. *Tabella II* (printed p. LI, read in a page image) assigns
Philippians to the Twenty-fifth through Twenty-eighth Sundays of Year A and
First Thessalonians from the Twenty-ninth, so this Sunday is the last of the
Philippians course; the national calendar gives Philippians 4:6–9 on 4 October
and 1 Thessalonians 1:1–5b on 18 October. The Gospel's course runs from
Matthew 21:33–43 on 4 October to Matthew 22:15–21 on 18 October. The Missal
week's antiphons and orations are shared by all three cycles. Every connection
between them and the Year A readings is editorial synthesis, as the
three-document profile settles for every formulary.

**The *Ordo*'s own tituli.** *Praenotanda* no. 106 says that the relation
between the readings of one Mass is shown by the careful choice of the tituli
set over the individual readings. At no. 142 (printed p. 77) the *Ordo* prints
three:

| Reading | Titulus | Source of the words |
| --- | --- | --- |
| Lectio I | *Faciet Dominus convivium, et absterget lacrimam ab omni facie* | Isaiah 25:6 and 25:8, condensed; the Clementine has *auferet* where the titulus has *absterget* |
| Lectio II | *Omnia possum in eo, qui me confortat* | Philippians 4:13, as in the Clementine |
| Evangelium | *Quoscumque inveneritis, vocate ad nuptias* | Matthew 22:9, without the Clementine's opening *et*; the verse stands in both Gospel forms |

These are edition-controlled evidence of what the Lectionary singles out in
each reading. For the first reading and the Gospel they are, on the *Ordo*'s own
account, how the official correlation is shown: the feast the Lord makes for
all peoples set beside the wedding feast to which whoever is found is called.
The second reading's titulus belongs to its semi-continuous course. They are
evidence of the Lectionary's emphasis within each reading and of that one
correlation, not of a design joining the Missal texts or the second reading to
the rest.

## Branches and other text-bearing parts of this Mass

These branch IDs are proposed as the stable semantic IDs for the manifest, the
leaf audit and the resolution appendix. No local selection was supplied for
any of them, and none is inferred.

| Branch ID | Authority and trigger | Status | Places affected | Resolution |
| --- | --- | --- | --- | --- |
| `gospel-long-form` | Lectionary no. 142 prints Matthew 22:1–14 as the longer form (*Ordo*: *longior*) | appointed alternative | 7 | Unselected. Under *Praenotanda* no. 80 (printed p. XXXVI, read in a page image) the choice between the two forms follows a pastoral criterion: the hearers' capacity to listen with profit to a longer or shorter reading, and to hear a fuller text to be explained in the homily. Both forms receive full treatment |
| `gospel-short-form` | Lectionary no. 142 prints Matthew 22:1–10 as the shorter form (*Ordo*: *brevior*) | appointed alternative | 7 | Unselected; mutually exclusive with the longer form. It omits the guest without a wedding garment and the saying of v. 14, so no claim resting on vv. 11–14 holds for a celebration that uses it |
| `communion-antiphon-psalm` | The Missal prints Cf. Psalm 34 (33):11 first | appointed alternative | 9 | Unselected; both antiphons receive full treatment |
| `communion-antiphon-epistle` | The Missal prints 1 John 3:2 under *Vel:* | appointed alternative | 9 | Unselected. *Tempus per annum* rubric 6 prefers an antiphon that agrees with the Gospel of the Mass. Neither is drawn from a Gospel, and whether either agrees with Matthew 22:1–14 or 22:1–10 is a judgment the books do not make; none is made here |
| `entrance-or-communion-chant-substitution` | GIRM 48 and 87 in the governing United States English, which give four options for each chant: (1) the Missal antiphon, or the *Graduale Romanum* antiphon with its psalm, in its own or another musical setting; (2) the antiphon and psalm of the *Graduale Simplex* for the liturgical time; (3) a chant from another collection of psalms and antiphons approved by the Conference of Bishops or the Diocesan Bishop, including psalms arranged in responsorial or metrical forms; (4) another suitable liturgical chant, likewise approved by the Conference of Bishops or the Diocesan Bishop. Without singing, the Missal antiphon is recited (48) or may be recited (87) by the faithful, some of them, a reader or the priest. The Latin *Institutio* (2002) gives the *Graduale Romanum* or *Graduale Simplex* antiphon with its psalm, or another suitable chant approved by the Conference of Bishops (at no. 48, its text); it names neither other collections of psalms and antiphons nor the Diocesan Bishop | permitted | 1, 9 | Unselected. The Missal antiphons are the studied layer. A sung substitute replaces the antiphon's text at that celebration, so no claim resting on an antiphon's wording holds where it is not used |
| `psalm-or-acclamation-chant-substitution` | GIRM 61 and 62 a in the governing United States English: when the psalm is sung, a seasonal common response and psalm may replace the text corresponding to the reading; in the dioceses of the United States, instead of the Lectionary's psalm, there may be sung the Responsorial Gradual of the *Graduale Romanum*, the Responsorial or Alleluia Psalm of the *Graduale Simplex*, or an antiphon and psalm from another collection of psalms and antiphons, including psalms in metrical form, approved by the Conference of Bishops or the Diocesan Bishop; songs or hymns may not be used in place of the Responsorial Psalm. The Alleluia verse is taken from the Lectionary or the *Graduale* (62 a) | permitted | 4, 6 | Unselected. The Lectionary's psalm and verse are the studied layer. With two readings before the Gospel, GIRM 63 does not apply |
| `offertory-chant` | GIRM 74 in the governing United States English: the Offertory chant accompanies the procession with the gifts at least until they are placed on the altar, its manner of singing follows the norms for the Entrance chant (no. 48, including its four United States options and their approval by the Conference of Bishops or the Diocesan Bishop), and singing may accompany the rite even without a procession | permitted | preparation of the gifts | Unselected. The Missal prints no Offertory antiphon; that silence does not mean the rite has no chant |
| `sprinkling-rite` | GIRM 51 (United States English) and the Order of Mass: on Sundays the blessing and sprinkling of water may replace the Penitential Act | ritual substitution | Introductory Rites | Unselected; it brings its own texts and adds no proper of this formulary |
| `compatible-preface-and-eucharistic-prayer` | *Tempus per annum* rubric 5; GIRM 364, 365 (United States English) | permitted | Eucharistic Prayer | Unselected. One of the eight Prefaces of the Sundays in Ordinary Time with a compatible Eucharistic Prayer; a coupled choice |
| `eucharistic-prayer-iv-with-preface` | GIRM 365 d (United States English): an invariable Preface; usable on Sundays in Ordinary Time | conditional | Eucharistic Prayer | Unselected. If Prayer IV is chosen, its invariable Preface excludes a Sunday Preface |
| `concluding-blessing-form` | The Missal's solemn blessings and prayers over the people, usable at the priest's discretion (2002 artifact, physical pp. 370 and 379) | permitted | Concluding Rites | Unselected. None is appointed to this Sunday; the 2008 variation list adds alternative dismissal formulas to the Order of Mass, which are Ordinary and not proper |
| `local-proper-calendar` | Universal Norms 59–60 with a particular calendar: a proper solemnity, or a celebration lawfully assigned to this Sunday | conditional | whole Mass | Not supplied. An actual local celebration needs its own resolution and never a blended formulary |

| Place | Text and appointment | Status |
| --- | --- | --- |
| Gloria | Sung or said on Sundays outside Advent and Lent (rubric 4; GIRM 53) | required |
| Creed | Sung or said on Sundays (rubric 4; GIRM 68) | required |
| Homily; Universal Prayer | Authored or locally composed; no appointed text | not applicable |
| Memorial of Saint John XXIII | Omitted under Universal Norms 60; no Collect, commemoration or reading enters this Mass | omitted |
| Sequence; proper Eucharistic Prayer insert | None appointed | not applicable |

## Lawful study-text routes

- **Scripture: the three readings in both forms of the Gospel, the psalm, the
  acclamation verse's source, and the scriptural sources of all three
  antiphons.** The Douay–Rheims (Challoner) as registered above, whose verse
  files for Isaias 24–25, Psalms 22, 33 and 129, Philippians 4, Ephesians 1,
  Matthew 21–22, 1 John 3 and 2 Peter 1 were read in this stage;
  `…american-1899-ebible` is the other registered Douay printing. It is a
  study translation in Vulgate numbering and is not the proclaimed text; the
  standing notice of `guidance/liturgy/postconciliar-propers.md` is mandatory.
  Partial verses (Isaiah 25:10a; Psalm 22 (23):3a and 3b; the response from v.
  6cd) must be shown as partial, with the excluded words marked as context,
  never silently trimmed or extended. The two forms of the Gospel are shown as
  two forms, not merged, and the second reading's omitted vv. 15–18 are marked
  as an omission.
- **Adapted texts.** The Entrance antiphon, both Communion antiphons and the
  acclamation verse are adaptations. Douay–Rheims verses may stand beside each
  as its identified scriptural source, labelled as such and with the departures
  stated, never as the adapted text itself. English must never be composed to
  stand for any of them, for the Entrance antiphon's closing vocative, or for
  the subject the second Communion antiphon supplies.
- **Latin comparison text.** The Clementine Vulgate as registered above,
  public domain, for verse boundaries and for comparing the antiphons and the
  acclamation verse. It is not the Missal's or the Lectionary's Latin.
- **Orations.** Latin incipit and an original description of what each prayer
  asks, cited to the owner. No rendering of the project's own, and no
  paraphrase close enough to reconstruct the approved English.
- **Approved English.** Not reproduced in any of the three PDFs. The rights
  records that control it are `guidance/liturgical-text-publication-policy.md`
  and the `ot-28` rows of `src/sources/inventories/postconciliar-proper-translations-v1.toml`
  and `postconciliar-proper-latin-provenance-v1.toml`, which were read here as
  leads only.

The existing source library was read before anything was fetched: the artifact
and passage records of the national calendar, the 2002 Missal, the 2008
*Notitiae* issue, the ICEL antiphon excerpt, the 1981 *Ordo* and the United
States GIRM, and the finding-aid and rights inventories named above. Two
library records for this Sunday already existed, the dated readings page
artifact named above and the passage
`passage.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.dominica-xxviii-per-annum-142`,
both registered on 2026-10-06; they were used only to identify those
witnesses, and every statement here rests on this stage's own reading. Five
registered artifacts whose bytes the repository identifies but does not hold
were fetched again, whole, from their recorded locations into ignored scratch
space, matched to their registered hashes and read: the national calendar, the
2002 Missal, the 2008 *Notitiae* issue, the ICEL antiphon excerpt and the 1981
*Ordo*. The dated readings page was read live and matched its registered
bytes. The United States GIRM chapter II and chapter VII pages answered HTTP
403 at context resolution on 2026-10-08, so the numbers this record cites were
first read in the Latin *Institutio generalis* printed in the 2002 Missal
artifact (physical PDF pp. 17–24 and 55). At the research re-entry the same
day both chapter pages were fetched whole over verified HTTPS and read: chapter
II (109,916 bytes, SHA-256
`d8ae3c14445d1915495fd122c75e3889d3dd826cfad92bb625575792592cd673`) is
byte-identical to the registered artifact
`artifact.catholic-church.institutio-generalis-missalis-romani.english-us-2011-emended-2021.girm2-html-d8ae3c14`
and was read at nos. 48, 51, 53, 61–64, 68, 74 and 87; chapter VII (58,213
bytes, SHA-256
`a6786170ac7b4736a21c0f8f1bec9ba133c19a136929c7f37c66d36930c3b214`) matched no
registered state and was registered as
`artifact.catholic-church.institutio-generalis-missalis-romani.english-us-2011-emended-2021.usccb-chapter-vii-html-2026-10-08-a6786170`,
then read at nos. 363–365. Both are bound in `research/source-bindings.toml`.
The branch rows above follow the United States English, which governs; the
Latin is kept only where the two agree. Where they differ, at nos. 48, 61 and
87, the United States text names the Missal antiphon among the sung options,
adds other collections of psalms and antiphons, including psalms in
responsorial or metrical form, extends approval to the Diocesan Bishop, and at
no. 61 excludes songs or hymns in place of the Responsorial Psalm; the Latin
already admits the *Graduale Romanum* and the *Graduale Simplex*, and, at nos.
48 and 87, another chant approved by the Conference of Bishops. Nothing
fetched is retained; the protected English is described, not transcribed.

## Remaining verification for research

- Complete the Week XXVIII owner's collation: register passage records for the
  2002 artifact at physical PDF p. 291 and for the ICEL excerpt's printed p. 80
  as it bears on this week; establish which Latin text the Entrance antiphon's
  closing vocative follows; establish the antecedents of the three orations,
  beginning with the translations inventory's leads that the Collect is
  verbatim in the Hadrianum and the Prayer after Communion in the Verona
  sacramentary, and what the Missal's repetition of the Prayer over the
  Offerings and the Prayer after Communion in other formularies means, if
  anything, for this one; and record the limits that remain for the 2008
  reprint and for a named United States altar book.
- The United States English of GIRM 48, 61–62, 74, 87 and 363–365, which this
  record first read only in the Latin, was read in hash-identified states at
  the research re-entry of 8 October 2026 (source paragraph above); no reading
  of it remains outstanding.
- Write `instance/manifest.md` and the leaf's `propers/verified.md` with the
  ordered inventory above, its keys and branch IDs, and
  `research/chronology-inputs.toml`. Three numbering hazards bear on the
  chronology inputs: the Entrance antiphon is Hebrew Psalm 130:3–4; Communion
  antiphon A is Hebrew Psalm 34:11 in the count that numbers the title and 34:10
  in English Bibles that do not, and the Hebrew and Vulgate texts differ in its
  subject; and the responsorial psalm is Hebrew Psalm 23, whose verse numbers
  coincide with the Vulgate's 22. The finding-aid index's antiphon citations
  are in Vulgate numbering by its own convention and must not be resolved as
  Hebrew.
- Decide how the adapted elements are displayed: the three antiphons by
  incipit, description and labelled scriptural source; the acclamation verse
  with its first-person-plural recasting identified.
- Establish how the approved United States psalm response stands to v. 6cd,
  from an edition-identified witness to the printed Lectionary; and whether the
  Lectionary admits another acclamation verse from a common set on Sundays in
  Ordinary Time. The dated page prints one verse; the rule was not examined
  here.
- Establish from edition-identified Greek and Latin witnesses the text of
  Matthew 22:1–14 that the Lectionary follows. No textual judgment is made in
  this record.
- Read each appointed passage in its complete biblical context, run the
  bounded reception sweep for every element in both Gospel forms and both
  Communion branches, and generate `research/chronology.toml` and
  `research/chronology-annotations.tex` through `tools/tpt proper-chronology`.
  No biblical date is asserted in this record.
- Bind the controlling sources in `research/source-bindings.toml`, and declare
  in `research/review-dependencies.toml` the external owners actually relied
  on: the Week XXVIII owner and the three edition registry records. The
  authorities adopted here are the USCCB 2026 calendar artifact; the USCCB
  readings page for the date; the 2002 Missal artifact with its *Tempus per
  annum* rubrics, the *Institutio generalis*, the *Normae universales* and
  General Calendar printed in it, and its blessings and prayers over the
  people; the United States English GIRM, chapters II and VII, in the states
  read at the research re-entry; the 2008 variation list in *Notitiae* 44; the
  ICEL antiphon excerpt;
  the 1981 *Ordo lectionum Missae* scan, including *Praenotanda* nos. 80 and
  105–107 and *Tabella II*; the Douay–Rheims, Clementine and King James
  editions as read above; and, as computation inputs only,
  `src/sources/calendars/postconciliar/propers.yaml` and `rubrics.yaml`.
- The inscription of Saint John XXIII in the General Calendar was not read in
  any official act. Nothing in this production depends on it, because the
  memorial is omitted at any memorial rank; if the studies mention the omitted
  memorial at all, its rank needs that witness first.
