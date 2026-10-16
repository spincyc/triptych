# Celebration context and complete appointed inventory

Resolved again on 16 October 2026 for the `proper-study` v12 revision of the
published Claude postconciliar leaf, run `821c824684b0c7a7`, seeded at commit
`d5abae0272089a418653fe675220d45f81313871`. The first resolution, made the same
day for run `4d16b5e19d25dad9` (`proper-study` v11), is superseded by this
record; the facts it established are kept only where they were read again
for this revision, and each section says what was re-read and how.

A research handoff was supplied
(`workflows/reviews/claude-pc-s55-revision-2026-10-16/HANDOFF.md`). It was read
as a list of leads, not as instructions, verification or a verdict. Its
sourcing items 1, 2 and 6 bear on this record and are answered below; items 3,
4, 5 and 7 and the standing findings it carries are research matters and are
listed under *Remaining verification for research*. One of its statements is
not borne out by the library: it says the dated readings page was registered
from this record's hash, but the registered state of 16 October 2026 records a
direct acquisition with its own hash (see the witnesses table).

No other leaf is evidence here: not the Claude leaves for earlier Sundays, not
the published leaf of the other provider for this same identity, which was not
opened, and no 1962 record. Nothing in this record comes from the 1962
calendar, Missal or propers, including those for the same civil Sunday. This
record settles what is studied. It contains no study prose, spoken text,
timing claim or review verdict; research collates the sources and may correct
it from evidence.

## Identity, governing books and territory

| Field | Resolution |
| --- | --- |
| Canonical identity | `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a`; calendar family `postconciliar`, path family `temporal` |
| Stable registry | `guidance/liturgy/postconciliar-propers-registry.md`: parent `PC-S55`, Twenty-ninth Sunday in Ordinary Time, stem `pc-s55-twenty-ninth-sunday-in-ordinary-time`; registered keys `PC-S55-A`, `PC-S55-B`, `PC-S55-C` for Lectionary nos. 145, 146, 147 |
| Formula key and slug | `PC-S55-A`; full slug is the stem plus `-year-a`. No form, branch or occurrence suffix is admitted. Every reading of no. 145 has one form only, so the target carries no reading branch |
| Registry checks | Ordinary Time Sunday `55 − 26 = 29`, hence owner `weeks/29`; Lectionary number `64 + 3 × (55 − 28) + 0 = 145`. Both agree with the dated witnesses below |
| Edition disposition | [Formula dispositions](../../../registry/formula-dispositions.md), row `PC-S55-A`: adopted as the stable registry lists it, with no cycle expansion. Dated result in [2026 occurrences](../../../registry/occurrences-2026.md), row `PC-S55-A`. Both rows were read again for this revision and still agree with every witness below; World Mission Day (below) changes no celebration, rank, colour or reading, so neither row needs a change |
| Canonical Missal owner | [Ordinary Time Week XXIX](../../shared/ordinary-time/weeks/29/propers/verified.md), at the registry-fixed path and shared with the Year B and Year C targets. It alone carries the formulary's witnesses, locators, element boundaries, variation check and rights disposition; this record cites its result and restates none of its evidence |
| Build edge | The collection Makefile declares, against `$(POSTCONCILIAR_US_ROOT)`, the Week XXIX owner as a prerequisite of this identity's study, `-synthesis` and `-homily` PDFs, in the rule after the Week XXVIII edge (read again for this revision). No Makefile change is needed. The collection-wide edges on `shared/exposition-format.tex` and `registry/*.md` apply as well |
| Missal | *Roman Missal, Third Edition, for Use in the Dioceses of the United States of America*, English, implemented 27 November 2011; Latin base *Missale Romanum*, editio typica tertia (2002), in its *reimpressio emendata* (2008) |
| Lectionary | *Lectionary for Mass for Use in the Dioceses of the United States of America*, second typical edition (1998/2001), Volume I, no. 145, with the 2017 *Supplement* where applicable; based on the *Ordo lectionum Missae*, editio typica altera (1981), as emended. The national calendar's own front matter states this book identity (printed p. 5) |
| Other controlling books | *General Instruction of the Roman Missal*, United States English edition of 2011 with the 2021 emendations, in the states listed under *General Instruction states read*; *Universal Norms on the Liturgical Year and the Calendar* and the *Calendarium Romanum generale*, read in the Latin printed in the 2002 Missal; the USCCB *Liturgical Calendar for the Dioceses of the United States of America* for 2026 |
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
postconciliar --date 2026-10-18 --json`, run again for this revision, returns
candidate `ot-29`, "the Sunday of Ordinary Time week 29", season Ordinary Time,
Sunday cycle A, weekday cycle II, nothing unresolved, together with a second
candidate, the Feast of Saint Luke, Evangelist. The anchors are those of
`guidance/liturgy/calendar-computation.md` for 2026: Easter 5 April, Pentecost
24 May, Christ the King 22 November, First Sunday of Advent 29 November.
Pentecost is the Sunday of resumed week `R = 34 − (22 November − 24 May) ÷ 7 =
34 − 26 = 8`, and 18 October falls twenty-one weeks later: week 29. From the
other anchor, 18 October is five weeks before the Sunday of week 34: again week
29. The last week before Lent was the sixth (Sunday 15 February, Ash Wednesday
18 February), so `R = L + 2`: this is a thirty-three-week year, week 7 never
occurred, and nothing is renumbered. The national calendar's table of
principal celebrations (printed p. 5) gives Ash Wednesday 18 February,
Pentecost 24 May and the First Sunday of Advent 29 November 2026, read again for
this revision. `Y = 2026`, and `2026 mod 3 = 1` is Year A.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
postconciliar --date 2026-10-18 --json`, run again, returns `ot-29` on the
basis "place-6-sunday" (locus `NUALC 59 table 6`) and the Feast of Saint Luke
on the basis "place-7-feast". The governing loci were read again for this
revision in the Latin *Normae universales* as printed in the registered 2002
Missal artifact: no. 58 (physical PDF p. 70), no. 59 with its table, places 4,
5, 6, 7 and 8 (pp. 70–71), and no. 60 (p. 71). Place 6 is *Dominicae temporis
Nativitatis et dominicae "per annum"*; place 7 is *Festa beatae Mariae Virginis
et Sanctorum Calendarii generalis*. Under no. 60 the higher place is celebrated
and only an impeded solemnity is transferred. The *Calendarium Romanum
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
| USCCB, *Liturgical Calendar for the Dioceses of the United States of America* 2026 | Registered artifact `artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.usccb-pdf-4bd9add0`. A fresh copy fetched from the recorded publisher URL on 16 October 2026 for this revision matched the registered SHA-256 `4bd9add07512396a2323aa977bc4816a5fad6348262e12740bcee97c77372d02` and 839,777 bytes before any page was read. Restricted; not retained | Printed p. 5 (PDF p. 7): Sunday cycle Year A, 30 November 2025 to 22 November 2026; weekday Cycle 2 from 25 May to 28 November 2026; the book identities given above. Printed p. 41 (PDF p. 43), read in the text layer: 18 October, Sunday, Twenty-Ninth Sunday in Ordinary Time, green; Is 45:1, 4-6 / 1 Thes 1:1-5b / Mt 22:15-21; Lectionary (145); Psalter Week I. No other celebration and no bracketed optional memorial stands on the date. The whole text layer was searched again for this revision for *mission*, *evangeliz-*, *propagation*, *collection* and *world day*: it prints no mission observance, collection or designated day anywhere, so its silence on 18 October is a silence of the whole book, not of that entry. The only occurrence of Saint Luke on the date is the appended Spanish list *Títulos litúrgicos* (printed p. 57, PDF p. 59), a list of approved titles by date, not a dated entry for 2026 |
| USCCB daily readings page for 18 October 2026, `https://bible.usccb.org/bible/readings/101826.cfm` | Two states are registered, neither held: `…daily-readings.2026-10-18-web-2026-10-13.usccb-101826-623dee42` (57,444 bytes) and `…daily-readings.2026-10-18-web-2026-10-16.lectionary145-html-369f06fd` (58,047 bytes), the second recorded as a direct acquisition of 16 October 2026 with its own hash. Direct requests made for this revision on 16 October 2026 with browser request headers were all answered HTTP 403 with a 15,748-byte "Checking connection" challenge page; no attempt was made to defeat it. The page was instead read in an Internet Archive capture of that official URL, timestamp `20260315050321`, fetched in its original-bytes form (`id_`) twice, byte-identically: 60,138 bytes, SHA-256 `f20f2e3c8fa1d8eeede12438f37f897f73e424bf70cb0fe06bf105390d7800fe`. That is a third state, captured seven months before the date by a third party; it is not an official delivery and matches neither registered state. Restricted; nothing of its wording is retained | Heading Twenty-ninth Sunday in Ordinary Time; Lectionary: 145; Reading 1 Isaiah 45:1, 4-6; Responsorial Psalm 96:1, 3, 4-5, 7-8, 9-10 with response locator (7b); Reading 2 1 Thessalonians 1:1-5b; Alleluia Philippians 2:15d, 16a, without `Cf.` and phrased as an exhortation; Gospel Matthew 22:15-21. One form of every unit. Four psalm strophes: vv. 1 and 3; vv. 4–5; vv. 7–8, ending with v. 8b, the summons to bring an offering and enter the Lord's courts, so v. 8 is sung whole; and v. 9 with the first and last clauses of v. 10, not the middle clause. The response's second gift and the strophe's rendering of v. 7b differ. The copyright notice attributes the Lectionary text to CCD and the psalm refrain to ICEL. These are exactly the features the first resolution recorded from its own 16 October delivery, which this revision could not re-read |

Computation and both dated witnesses agree on the celebration, the cycle, the
Lectionary number and every reading; nothing fails closed. The one
disagreement is internal to the readings page, between the psalm locator it
prints and the verses it gives, and the Latin *Ordo* decides the boundary.
For the national calendar this revision re-read the registered bytes. For the
readings page it re-read no official delivery: the locators and the psalm's
verse selection rest on the archived capture, corroborated in every reading's
citation and Lectionary number by the national calendar and in every boundary
by the *Ordo*. The psalm's United States locator `9-10` and the strophe
division rest on that capture alone among the witnesses read here. The printed
United States Lectionary volume itself was not inspected.

**The days around it.** The Sunday's readings, Gloria, Creed and Sunday Preface
do not continue into the week. The national calendar (printed p. 41, read again)
gives Monday 19 October to the United States Memorial of Saints John de Brébeuf
and Isaac Jogues, Priests, and Companions, Martyrs (no. 473), Tuesday 20
October to the weekday (no. 474) with the optional United States memorial of
Saint Paul of the Cross, Wednesday 21 October to the weekday (no. 475),
Thursday 22 October to the weekday (no. 476) with the optional memorial of
Saint John Paul II, Friday 23 October to the weekday (no. 477) with the
optional memorial of Saint John of Capistrano, and Saturday 24 October to the
weekday (no. 478) with the optional memorials of Saint Anthony Mary Claret and
of the Blessed Virgin Mary, all from the independent Cycle II course. Saturday
17 October is the Memorial of Saint Ignatius of Antioch (no. 472); an
anticipated Mass of the Sunday on Saturday evening uses this same formulary and
readings, is not a Vigil form, and has no key. Sunday 25 October is the
Thirtieth Sunday (no. 148), with 1 Thessalonians 1:5c-10 and Matthew 22:34-40.

## World Mission Day on 18 October 2026

The first resolution recorded the conditional Mass for the Evangelization of
Peoples without seeking a dated witness for a mission observance. October 2026
has Sundays on the 4th, 11th, 18th and 25th, so the 18th is the penultimate
Sunday. The witnesses below were read on 16 October 2026; none is registered in
the source library.

| Witness | Identity and check | What it states |
| --- | --- | --- |
| Holy See, *Message of the Holy Father for the 100th World Mission Day 2026 [18 October 2026]*, Leo XIV, 25 January 2026 | `https://www.vatican.va/content/leo-xiv/en/messages/mission/documents/20260125-giornata-missionaria.html`, fetched directly: 49,817 bytes, SHA-256 `6b7809d9f045d5154df9d03f9ab44ea5ebf586384c9b32f4d463a468586d165e`. Found from the official index of Leo XIV's World Mission Day messages (`…/en/messages/mission.index.html`, 37,038 bytes, SHA-256 `dd1b05d528d17484ef63d1c226a30f4ab90c9c5651e6819126f3dbda48717b13`) | The heading dates the 100th World Mission Day to 18 October 2026. The opening paragraph calls it the centenary of a celebration established by Pius XI and gives the theme "One in Christ, united in mission". Section 3 appeals for prayer and for "practical support, particularly on World Mission Day". It is signed from the Vatican on 25 January 2026. It prescribes no Mass, reading, oration or other liturgical text |
| Holy See, *Video message of the Holy Father Leo XIV on the occasion of the 100th World Mission Sunday*, 7 October 2026 | `…/en/messages/mission/documents/20261007-videomessaggio-gmm.html`, fetched directly: 37,249 bytes, SHA-256 `89dd1465e522b1b9cd501f35b62bc9fe067e66ca2cc6f4dd86f7d752a9c96859` | Dated in its heading *[18 ottobre 2026]*. It calls the day World Mission Sunday, an annual celebration established by Pius XI a hundred years ago to foster in every diocese and parish understanding of the missionary task, prayer for evangelization, missionary vocations and support for the Pontifical Mission Societies. It prescribes no liturgical text |
| The Pontifical Mission Societies in the United States, *World Mission Sunday* 2026 page | `https://pontificalmissions.org/wms-2026` (reached from `missio.org`, which redirects there), fetched directly: 57,017 bytes, SHA-256 `4904919b1f38c5aa72c4259757656a0cd84ae934023bce2f5779ac9bc66ec13b` | Dates World Mission Sunday to October 18, 2026, and describes the World Mission Sunday collection and parish resources for World Mission Month. This is the national office of a pontifical work, not the Conference: it witnesses the United States observance and collection, not a liturgical norm. It prescribes no Mass or text |
| USCCB national collections page, `https://www.usccb.org/committees/national-collections` | One request on 16 October 2026 was answered (HTTP 200, 55,301 bytes), but its bytes were overwritten before reading and only its title was seen; every later request met the 15,748-byte challenge page | Nothing is claimed from it |
| *Missale Romanum* 2002, Masses for Various Needs no. 18, *Pro evangelizatione populorum* | Registered artifact `artifact.catholic-church.missale-romanum.vatican-typica-tertia-2002.secondary-digital-pdf-0b458944`, fetched again and matched to SHA-256 `0b458944…05523d7` and 3,333,382 bytes before reading; physical PDF p. 695, text layer | The rubric under the title: *Haec Missa adhiberi potest etiam dominicis "per annum", quando peculiares celebrationes pro opere missionum habentur, dummodo non occurrat dominica Adventus, Quadragesimae vel Paschae, aut sollemnitas quaedam.* The Mass *may* be used on a Sunday per annum when particular celebrations for the work of the missions are held |
| *Missale Romanum* 2002, introduction to the Masses for Various Needs, nos. 1–2 | Same artifact, physical PDF p. 667 | No. 2: in a graver need, a suitable Mass may be said by mandate or permission of the local Ordinary on every day except solemnities, the Sundays of Advent, Lent and Easter, the days within the Easter Octave, All Souls and Ash Wednesday and Holy Week |
| United States GIRM, nos. 373–374 | Chapter VIII state listed under *General Instruction states read* | No. 373: Masses for Various Needs and Occasions are used either as occasion arises or at fixed times; its United States paragraphs designate other days (fruits of the earth, human rights, justice and peace, penitential observances at times the Diocesan Bishop sets; 22 January) and name no mission day. No. 374: in a graver need or for pastoral advantage, at the direction or with the permission of the Diocesan Bishop, an appropriate Mass may be celebrated on any day except the days it lists, which do not include Sundays in Ordinary Time |

**Resolution.** World Mission Day, the 100th, is a dated observance of the
universal Church on Sunday 18 October 2026, and in the United States it is kept
with the World Mission Sunday collection. It is an observance of prayer and
support, not a liturgical day: no witness gives it a rank, colour, formulary,
reading or text, the national calendar prints nothing against the date, and
nothing in it displaces the Twenty-ninth Sunday, which remains the celebration
of the date and the formulary studied. Its one liturgical consequence is that
the condition of the Missal's rubric at p. 695 can be met on this Sunday: where
a particular celebration for the work of the missions is held, the Mass *Pro
evangelizatione populorum* *may* replace this formulary. The rubric permits
and does not prescribe, and no witness read appoints that Mass to this Sunday.
The branch therefore stays `conditional` and unselected (row below), and the
United States English of that Mass and its Lectionary readings were not
examined.

For the documents this means: the observance is a fact about the date, not part
of the Sunday's formulary. The terminal liturgical-resolution apparatus may
record it beside the conditional branch, with the witnesses above. It supplies
nothing to the inventory, the interpretations or the four senses, and the
evidence gives no warrant for reading the appointed texts as chosen for the
missions. Whether the homily mentions the day is an authoring choice; if it
does, it may say only what these witnesses state.

## Appointed inventory

Ten ritual places carry eleven text-bearing elements, because the Communion
antiphon is a closed pair. Missal elements are cited to the Week XXIX owner,
whose record holds their printed locators, incipits and summaries; for this
revision the order, incipits, locators, *Cf.* marks, the *Vel:* pair and each
oration's conclusion were read again in the text layer of the registered 2002
artifact at physical PDF pp. 291–292 (fresh copy, hash matched above) and agree
with the owner. Lectionary boundaries were read in three places that agree in
every reading: the national calendar and the archived readings page above, and
the *Ordo lectionum Missae*, editio typica altera (1981), no. 145, *Dominica
vigesima nona*, Year A, read again for this revision on 16 October 2026 at 150
dpi in the page image of printed p. 79 (artifact p. 133) of the registered scan
`artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e`
(fresh copy from the recorded Internet Archive location, SHA-256
`ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d`, 21,487,058
bytes, matched before reading). Under *Praenotanda* no. 119 and its note 123
(printed p. XLVIII, read in the first resolution in the text layer of the same
scan) the *Ordo* numbers chapters and verses after the *Nova Vulgata*, and
psalms after the 1969 *Nova Vulgata* psalter, which keeps the Vulgate psalm
numbers. Psalms are cited here in the Hebrew numbering of the United States
Lectionary with the Vulgate number, which the Latin books and the Douay–Rheims
use, in parentheses.

| Order | Key | Element and exact locus | Liturgical place, extent and boundary | Status |
| ---: | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | Entrance Antiphon *Ego clamavi, quoniam exaudisti me, Deus*; Week XXIX owner | Introductory Rites, at the entrance. The Missal cites Cf. Psalm 16:6, 8 in Vulgate numbering (Hebrew 17:6, 8). The owner's collation shows an adaptation that passes over v. 7 and trims and supplements v. 8 | required |
| 2 | `collect` | Collect *Omnipotens sempiterne Deus, fac nos tibi semper*; Week XXIX owner | Concludes the Introductory Rites, after the Gloria; long conclusion | required |
| 3 | `first-reading` | Isaiah 45:1, 4–6; Lectionary no. 145 | Liturgy of the Word, first reading. One form only, in two segments: v. 1, then vv. 4–6, omitting vv. 2–3. It ends with the whole of v. 6. The *Ordo*'s incipit is *Haec dicit Dominus de uncto meo Cyro* | required |
| 4 | `responsorial-psalm` | Psalm 96 (95):1 and 3, 4–5, 7–8, 9–10a and 10c, response from v. 7b; Lectionary no. 145 | After the first reading. Four strophes; v. 2, v. 6 and the middle clause of v. 10 are not sung, and v. 8 is sung whole. The *Ordo* prints the locator as *Ps 95, 1 et 3. 4-5. 7-8. 9-10a et c* and the response as *Afferte Domino gloriam et potentiam*; the United States page prints the locator as 9–10. Hebrew and Vulgate verse numbers coincide in this psalm | required |
| 5 | `second-reading` | 1 Thessalonians 1:1–5b; Lectionary no. 145 | Second reading. One form only, the letter's opening. It ends within v. 5; the rest of v. 5 and vv. 6–10 are the next Sunday's reading (1:5c–10). The *Ordo* adds no liturgical incipit: it begins with the letter's own first words, *Paulus et Silvanus et Timotheus* | required |
| 6 | `acclamation` | Alleluia with verse Philippians 2:15d, 16a; Lectionary no. 145 | Before the Gospel. Printed without `Cf.` in the *Ordo* and on the readings page. The *Ordo*'s Latin verse, *Lucetis sicut luminaria in mundo, verbum vitae continentes*, gives the last colon of v. 15 without its opening *inter quos* and the first colon of v. 16, in the indicative | required |
| 7 | `gospel` | Matthew 22:15–21; Lectionary no. 145 | Gospel. One form only. The Pharisees' plot, their disciples sent with the Herodians, the question of the tax to Caesar, the coin, and the closing saying of v. 21. It ends before v. 22. The Latin *Ordo* opens it with *In illo tempore: Abeuntes pharisaei* and names Jesus (*caperent Iesum*) where the Clementine has *eum* | required |
| 8 | `prayer-over-offerings` | Prayer over the Offerings *Tribue nos, Domine, quaesumus, donis tuis*; Week XXIX owner | Liturgy of the Eucharist, after the preparation of the gifts; short conclusion | required |
| 9a | `communion-antiphon-a` | Communion Antiphon, Cf. Psalm 33 (32):18–19; Week XXIX owner | At Communion. Printed first, with `Cf.` Hebrew and Vulgate verse numbers coincide | appointed alternative |
| 9b | `communion-antiphon-b` | Communion Antiphon, Mark 10:45; Week XXIX owner | At Communion. Printed second under *Vel:*, without `Cf.`, though the owner's collation shows it adapted | appointed alternative |
| 10 | `prayer-after-communion` | Prayer after Communion *Fac nos, quaesumus, Domine, caelestium rerum*; Week XXIX owner | Concludes the Communion Rite; short conclusion | required |

**The acclamation's key.** The published leaf keys element 6 `acclamation`,
a workaround for the orientation-v1 generator, which gave any key beginning
`gospel` a narrated-event row. The handoff reports that orientation-v2 gives
that row only to Gospel pericope keys, so the workaround is no longer needed.
This revision **keeps `acclamation`**. It is the published stable key, and the
study's appointed-text anchor `proper-acclamation`, which the web edition
carries, derives from it. Re-keying would change a published anchor and every
record that names the element, and would fix nothing the new generator still
gets wrong. Whether the generator treats the key correctly is checked when
research regenerates the chronology under orientation-v2.

The formulary prints no Offertory antiphon, Sequence, proper Preface, proper
Eucharistic Prayer insert, prayer over the people or solemn blessing. The
Lectionary prints no alternative or shorter form of any reading, no second
psalm response and no second acclamation verse for Year A.

**Boundary checks made against tracked Scripture.** The Douay–Rheims
(`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`)
and the Clementine Vulgate (`edition.catholic-church.vulgata-clementina.ebible-latvuc`)
were read at every boundary verse in the first resolution, and the tracked King
James Version (`edition.church-of-england.king-james-version.ebible-engkjv`)
where Hebrew numbering or verse division had to be confirmed. The research
stage re-read each of them and bound them in `research/source-bindings.toml`.
These checks concern extent only; they were not repeated for this revision
because no boundary changed and the *Ordo* page image was re-read.

- *Isaiah 44–45.* Isaiah 44:24–28 precedes the appointment and names Cyrus at
  44:28 as the Lord's shepherd who will see Jerusalem and the temple rebuilt;
  45:1 opens a new oracle addressed to Cyrus. The omitted vv. 2–3 promise that
  the Lord will go before him, break gates and give him hidden treasures, so
  that he may know who calls him by name. Verse 7, on forming light and
  creating darkness, making peace and creating evil, follows and lies outside
  the appointment. Verse numbers coincide in all three texts. In 45:1 the
  Clementine reads *christo meo Cyro*, where the *Ordo*'s incipit has *de uncto
  meo Cyro*; in 45:4 the Clementine has *assimilavi te*, which the Douay–Rheims
  renders "I have made a likeness of thee", where the King James Version has
  "I have surnamed thee". Which Latin text the *Ordo* follows, and how the
  Hebrew reads, are research matters.
- *Psalm 95 (96).* In the Clementine and the Douay–Rheims the psalm's title
  stands within v. 1, before *Cantate Domino canticum novum*; the tracked King
  James Version has no title. Verse numbers otherwise coincide in the three
  texts. Verse 10 has three clauses: the Lord reigns, he has set the world
  firm so that it will not be moved, and he will judge the peoples with
  equity. The *Ordo*'s `10a et c` takes the first and third, and the readings
  page's fourth strophe gives exactly those, whatever its locator says.
  Verse 8 has two members, the bringing of an offering (*tollite hostias*) and
  the entry into his courts; the *Ordo*'s `7-8` and the readings page's third
  strophe both include the whole verse, so both members are sung. The response
  is v. 7b: the Clementine's *afferte Domino gloriam et honorem*, the *Ordo*'s
  Latin response *gloriam et potentiam*, and the King James Version's "glory
  and strength" name the second gift differently, and the readings page's
  response and its own rendering of v. 7b in the third strophe differ in the
  same place. How the approved response stands to v. 7b is a research matter.
  In v. 5 the Clementine and the Douay–Rheims call the gods of the nations
  demons where the King James Version calls them idols; that is a difference
  of text, also for research.
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
  the indicative; the United States verse on the readings page is phrased as
  an exhortation. Whether the acclamation is therefore displayed as an
  adaptation is a research matter.
- *Matthew 22.* Matthew 21:23 sets the scene in the temple, where the chief
  priests and elders question Jesus' authority; three parables follow, ending
  with the wedding feast of 22:1–14, the previous Sunday's Gospel. 22:15 opens
  with *Tunc abeuntes pharisaei*, which the *Ordo* replaces with *In illo
  tempore: Abeuntes pharisaei*; in the same sentence it writes *Iesum* for the
  Clementine's *eum*. Verse 22, where the questioners marvel and leave him,
  lies outside the appointment, and v. 23 opens the Sadducees' question about
  the resurrection. The national calendar gives Matthew 22:34–40 for 25
  October, so the Sunday course passes over 22:22–33.
- *Missal antiphons.* Psalm 16:6, 8, Psalm 32:18–19 and Mark 10:45 were
  compared with the Clementine by the owner, whose findings 1–3 record the
  results. In the King James Version the clause about those who rise up stands
  at the end of Psalm 17:7, so the Hebrew v. 8 begins where the antiphon's v. 8
  does; in the Clementine and the Douay–Rheims *A resistentibus dexterae tuae*
  opens v. 8, before *custodi me*, and the antiphon leaves it out.

**Relationship classes, preliminary.** Under the 1981 *Praenotanda* nos.
105–107 (printed pp. XLIV–XLV) the first reading is `officially correlated`
with the Gospel, and the Gospel and the second reading each belong to a
`semi-continuous` course: Matthew in Year A from the Third Sunday, and the
apostolic letters as *Tabella II* distributes them. Under GIRM 61–62 (United
States English, chapter II state re-read for this revision) the psalm is
`responsorial`, which no. 61 says should correspond to each reading, and the
verse before the Gospel is `acclamatory`. *Tabella II* (printed p. LI) assigns
Philippians to the Twenty-fifth through Twenty-eighth Sundays of Year A and
First Thessalonians to the Twenty-ninth through Thirty-third, so this Sunday
opens the First Thessalonians course; the national calendar gives Philippians
4:12–14, 19–20 on 11 October and 1 Thessalonians 1:5c–10 on 25 October. The
Gospel's course runs from Matthew 22:1–14 on 11 October to Matthew 22:34–40
on 25 October. The Missal week's antiphons and orations are shared by all
three cycles. Every connection between them and the Year A readings is
editorial synthesis, as the three-document profile settles for every
formulary. World Mission Day adds no relationship class.

**The *Ordo*'s own tituli.** *Praenotanda* no. 106 says that the relation
between the readings of one Mass is shown by the careful choice of the tituli
set over the individual readings, and no. 123 (printed p. XLIX) that a titulus
indicates the chief theme of its reading and, where necessary, the link
between the readings of one Mass. At no. 145 (printed p. 79, page image re-read)
the *Ordo* prints three:

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
same printed page, re-read) appoints Mark 10:45 as that year's acclamation
verse and Mark 10:35–45 or 10:42–45 as its Gospel. The Missal's second
Communion antiphon is therefore drawn from the Year B Gospel. In Year A
neither antiphon comes from Matthew 22:15–21, and whether either agrees with
it, in the sense of *Tempus per annum* rubric 6, is a judgment the books do not
make. This stays in the research records; it says nothing about why the
antiphon was chosen.

## Branches and other text-bearing parts of this Mass

These branch IDs are the stable semantic IDs already used by the manifest, the
leaf audit and the resolution appendix; this revision keeps every one
unchanged. No local selection was supplied for any of them, and none is
inferred. The Missal rubrics cited were read again for this revision in the
registered 2002 artifact (*Tempus per annum* rubrics 3–6 at physical p. 268;
the solemn blessings and prayers over the people at pp. 370 and 379; the
Masses for Various Needs at pp. 667 and 695). The General Instruction loci
were read in the states listed under *General Instruction states read*.

| Branch ID | Authority and trigger | Status | Places affected | Resolution |
| --- | --- | --- | --- | --- |
| `communion-antiphon-psalm` | The Missal prints Cf. Psalm 33 (32):18–19 first | appointed alternative | 9 | Unselected; both antiphons receive full treatment |
| `communion-antiphon-gospel` | The Missal prints Mark 10:45 under *Vel:* | appointed alternative | 9 | Unselected. *Tempus per annum* rubric 6 (physical p. 268) lets either be chosen, preferring one that agrees with the Gospel of the Mass. This one is drawn from a Gospel, but not from the Year A Gospel; whether either antiphon agrees with Matthew 22:15–21 is a judgment the books do not make, and none is made here |
| `entrance-or-communion-chant-substitution` | GIRM 48 and 87 in the governing United States English, which give four options for each chant: (1) the Missal antiphon, or the *Graduale Romanum* antiphon with its psalm, in its own or another musical setting; (2) the antiphon and psalm of the *Graduale Simplex* for the liturgical time; (3) a chant from another collection of psalms and antiphons approved by the Conference of Bishops or the Diocesan Bishop, including psalms arranged in responsorial or metrical forms; (4) another suitable liturgical chant, likewise approved. Without singing, the Missal antiphon is recited (48) or may be recited (87) by the faithful, some of them, a reader or the priest | permitted | 1, 9 | Unselected. The Missal antiphons are the studied layer. A sung substitute replaces the antiphon's text at that celebration, so no claim resting on an antiphon's wording holds where it is not used |
| `psalm-or-acclamation-chant-substitution` | GIRM 61 and 62 a in the governing United States English: when the psalm is sung, texts of some responses and psalms chosen for the times of the year may be used instead of the text corresponding to the reading; in the dioceses of the United States, instead of the Lectionary's psalm, there may be sung the Responsorial Gradual of the *Graduale Romanum*, the Responsorial or Alleluia Psalm of the *Graduale Simplex*, or an antiphon and psalm from another collection of psalms and antiphons, including psalms in metrical form, approved by the Conference of Bishops or the Diocesan Bishop; songs or hymns may not replace the Responsorial Psalm. The Alleluia verse is taken from the Lectionary or the *Graduale* (62 a). The *Ordo*'s common texts for sung psalms (nos. 173–174, printed pp. 97–98) give common responses and psalms *per annum* and another psalm *in ultimis hebdomadis* | permitted | 4, 6 | Unselected. The Lectionary's psalm and verse are the studied layer. With two readings before the Gospel, GIRM 63 does not apply. The *Ordo* gives no common series of acclamation verses for the Sundays per annum (a bounded search of its text layer in the first resolution); *Praenotanda* no. 90 makes the verse either fixed for each Mass or chosen from a common series, and at no. 145 it is fixed |
| `offertory-chant` | GIRM 74 in the governing United States English: the Offertory chant accompanies the procession with the gifts at least until they are placed on the altar, its manner of singing follows the norms for the Entrance chant (no. 48, including its four United States options), and singing may always accompany the rite even without a procession | permitted | preparation of the gifts | Unselected. The Missal prints no Offertory antiphon; that silence does not mean the rite has no chant |
| `sprinkling-rite` | GIRM 51 (United States English): from time to time on Sundays, especially in Easter Time, the blessing and sprinkling of water may take place instead of the customary Penitential Act, as a reminder of Baptism | ritual substitution | Introductory Rites | Unselected; it brings its own texts and adds no proper of this formulary |
| `compatible-preface-and-eucharistic-prayer` | *Tempus per annum* rubric 5 (unless a Eucharistic Prayer with its own Preface is used, a Sunday Preface per annum is said on Sundays); GIRM 364, 365 (United States English) | permitted | Eucharistic Prayer | Unselected. One of the eight Prefaces of the Sundays in Ordinary Time with a compatible Eucharistic Prayer; a coupled choice. GIRM 365 a calls Prayer I especially suited to Sundays unless Prayer III is preferred for pastoral reasons, and 365 c prefers Prayer III on Sundays and festive days |
| `eucharistic-prayer-iv-with-preface` | GIRM 365 d (United States English): an invariable Preface; usable when a Mass has no Preface of its own and on Sundays in Ordinary Time | conditional | Eucharistic Prayer | Unselected. If Prayer IV is chosen, its invariable Preface excludes a Sunday Preface |
| `concluding-blessing-form` | The Missal's solemn blessings and prayers over the people, usable at the priest's discretion under the rubric opening each section (physical pp. 370 and 379) | permitted | Concluding Rites | Unselected. None is appointed to this Sunday |
| `mass-for-evangelization-of-peoples` | The Missal's Mass *Pro evangelizatione populorum* (Masses for Various Needs, no. 18; physical p. 695), whose own rubric admits it on Sundays per annum when particular celebrations for the work of the missions are held, unless a Sunday of Advent, Lent or Easter or a solemnity occurs. On 18 October 2026 the condition can be met: the Holy See dates the 100th World Mission Day to this Sunday, and the United States keeps it with the World Mission Sunday collection (see *World Mission Day on 18 October 2026*) | conditional | whole Mass | Not selected. The rubric permits and does not prescribe; no witness read appoints the Mass to this Sunday, and the national calendar prints no observance. Where a particular mission celebration is held and the Mass is used, it replaces this formulary entirely and nothing in this production holds for it. Its United States English and its readings were not examined |
| `ritual-or-various-needs-mass` | GIRM 372–374 (United States English): the days on which no. 372 prohibits Ritual Masses do not include Sundays in Ordinary Time, and due regard is owed to the norms of the ritual books; Masses for Various Needs are used as occasion arises or at fixed times (373); and in graver need or for pastoral advantage, at the direction or with the permission of the Diocesan Bishop, an appropriate Mass may be celebrated on any day except those listed, which do not include Sundays in Ordinary Time (374; the same rule in the Latin introduction to the Masses for Various Needs, no. 2, physical p. 667) | conditional | whole Mass | Not supplied. An actual replacement needs its own resolution and never a blended formulary |
| `local-proper-calendar` | Universal Norms 59–60 with a particular calendar: a proper solemnity at place 4, or a celebration lawfully assigned to this Sunday. On this date the case is concrete: in a church of which Saint Luke is the titular, the Solemnity of the Title (place 4 c) outranks the Sunday (place 6), while a feast of Saint Luke as principal patron of a diocese or region (place 8 a or 8 c) does not | conditional | whole Mass | Not supplied. An actual local celebration needs its own resolution and never a blended formulary |

| Place | Text and appointment | Status |
| --- | --- | --- |
| Gloria | Sung or said on Sundays outside Advent and Lent (*Tempus per annum* rubric 4; GIRM 53) | required |
| Creed | Sung or said on Sundays (rubric 4; GIRM 68) | required |
| Homily; Universal Prayer | Authored or locally composed; no appointed text. On Sundays a homily is required at every Mass with the people (GIRM 66). A parish may pray for the missions in its Universal Prayer on World Mission Day; that is local composition and adds nothing to this inventory | not applicable |
| Feast of Saint Luke, Evangelist | Omitted under Universal Norms 60; no Collect, commemoration or reading enters this Mass | omitted |
| World Mission Day | An observance of prayer and a collection on this date, with no rank, formulary or text; its only liturgical bearing is the conditional branch above | not applicable |
| Sequence; proper Eucharistic Prayer insert | None appointed | not applicable |

*Praenotanda* no. 79 (printed p. XXXVI) contemplates a Conference of Bishops
permitting only two readings in some places. Whether any such permission
applies in the United States was not examined; no branch is recorded for it.

## General Instruction states read

The United States English General Instruction governs every branch row above
that cites it. The handoff (item 1) asks that what was actually read be
registered and that the documents not rest on an unread text.

| Chapter | State read for this revision | Loci verified | Relation to the library |
| --- | --- | --- | --- |
| II, *The Structure of the Mass, Its Elements, and Its Parts* | Direct request to `https://www.usccb.org/prayer-and-worship/the-mass/general-instruction-of-the-roman-missal/girm-chapter-2` with browser request headers, 16 October 2026: HTTP 200, 109,916 bytes, SHA-256 `d10afff3888adfe8a0f397a792f5d07d941043f4d031fd89a492917facb580f1` | Nos. 48, 51, 53, 61, 62, 63, 66, 68, 74 and 87 | **Byte-identical to the registered state** `artifact.catholic-church.institutio-generalis-missalis-romani.english-us-2011-emended-2021.usccb-chapter-ii-html-2026-10-16-d10afff3`, which was registered from the first resolution's hash. That state is now re-read and its loci verified |
| VII, *The Choice of the Mass and Its Parts* | Direct requests the same day were answered HTTP 403 with the 15,748-byte challenge page, including after a request to the landing page; the challenge was not defeated. Read instead in the Internet Archive capture of the official URL at timestamp `20260613160611`, fetched twice byte-identically in original-bytes form (`id_`): 16,104 bytes gzip-encoded, SHA-256 `87f33dba3669434f6c708b9a6589c1db3e1deec0cbe8605f0f9dd49355df0606`; decoded HTML 58,095 bytes, SHA-256 `e973bb8ffe42f31b3eb4addba2acff9d7b9ef38406536a6667b8692b60d77631`, titled "Chapter VII: The Choice of the Mass and Its Parts \| USCCB" | Nos. 363, 364 and 365 a–d | Matches none of the eight registered chapter VII states (57,054 to 58,269 bytes; none has this hash); the state of 16 October 2026 that the first resolution read (`…usccb-chapter-vii-html-2026-10-16-e803093d`) could not be re-read |
| VIII, *Masses and Prayers for Various Needs and Occasions and Masses for the Dead* | As for chapter VII: direct requests refused. Internet Archive capture at timestamp `20260618180311`, fetched twice byte-identically: 14,128 bytes gzip-encoded, SHA-256 `dd244a19c76b6fc4e6b24087e87d8103b739cd50896c6072912f331fae52270c`; decoded HTML 53,258 bytes, SHA-256 `dbdf98d997624444d08d4d3533fa085138de5dafb357e79a70cd82e32dce32aa`. Its no. 373 carries the United States paragraphs (the 22 January day of prayer and its two Masses), which identify the United States text | Nos. 368–377 | Matches no registered state; the state of 16 October 2026 (`…usccb-chapter-viii-html-2026-10-16-273fc7cb`) could not be re-read |

What this means for the documents. Every branch row above that cites chapter
II rests on a re-read, registered official state. The rows citing chapters VII
and VIII (365 a, c and d; 372–374) rest on archived captures of the official
pages from June 2026, read in full at those loci, and on the Latin typical
rules read in the 2002 Missal where those exist (*Tempus per annum* rubric 5;
Masses for Various Needs, introduction no. 2 and no. 18). The captures are a
third party's copies of the official page: they show what the official page
said on those dates, not what it says on 16 October 2026. Nothing the documents
state from these chapters goes beyond the loci listed. The documents should
date the reading rather than name a production stage (standing finding
WEB-001): for example, chapter II read in its official chapter page on 16
October 2026; chapters VII and VIII read in Internet Archive captures of their
official pages made on 13 and 18 June 2026, because the publisher's site
refused direct requests that day.

## Lawful study-text routes

- **Scripture: the three readings, the psalm, the acclamation verse's source,
  and the scriptural sources of all three antiphons.** The Douay–Rheims
  (Challoner) as registered above; `…american-1899-ebible` is the other
  registered Douay printing. It is a study translation in Vulgate numbering and
  is not the proclaimed text; the standing notice of
  `guidance/liturgy/postconciliar-propers.md` is mandatory. Partial verses
  (Psalm 95 (96):10a and 10c, with 10b omitted; 1 Thessalonians 1:5b;
  Philippians 2:15d and 16a) must be shown as partial, with the excluded words
  marked as context, never silently trimmed or extended. The first reading's
  omitted Isaiah 45:2–3 and the psalm's omitted vv. 2 and 6 are marked as
  omissions, and the psalm's title, which stands within v. 1 in the
  Douay–Rheims, is not part of the first strophe. Psalm 95 (96):8 is sung whole
  and is shown whole. In 1 Thessalonians the Douay–Rheims carries the greeting
  at the start of v. 2; the appointment includes it either way.
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
  and `postconciliar-proper-latin-provenance-v1.toml`, read as leads only. The
  General Instruction, the readings page and the Holy See and Pontifical
  Mission Societies pages are described, not transcribed, beyond the short
  Latin rubric quoted above from the 2002 Missal.

## Sources read for this revision

The existing source library was read before anything was fetched: the artifact
records of the national calendar, the 2002 Missal, the 1981 *Ordo*, all
seventeen registered General Instruction states (chapters II, VII and VIII and
the landing page) and both registered states of the readings page, together
with the leaf's `research/source-bindings.toml`, the Week XXIX owner, the edition
registry rows and the finding-aid index. Three registered artifacts whose bytes
the repository identifies but does not hold were fetched again, whole, from
their recorded locations into ignored scratch space and matched to their
registered hashes before reading: the national calendar, the 2002 Missal and
the 1981 *Ordo*. General Instruction chapter II was re-read directly and
matched its registered state. Chapters VII and VIII and the readings page were
refused directly and read in the Internet Archive captures described above.
The World Mission Day witnesses were fetched directly from the Holy See and the
Pontifical Mission Societies in the United States. None of the new states
(the three captures, the two Holy See documents and their index, the
Pontifical Mission Societies page) is registered. Nothing fetched is retained
in the repository; protected English is described, not transcribed.

## Remaining verification for research

- **Register and bind what was read here** (handoff items 1, 2 and 6). Bind the
  re-read chapter II state already registered (`…usccb-chapter-ii-html-2026-10-16-d10afff3`)
  with the loci above. Register the chapter VII and VIII captures and the
  readings-page capture as their own artifacts, identified as Internet Archive
  captures of the official URLs with their timestamps and both the encoded and
  decoded hashes; the `id_` captures re-fetched byte-identically, so research
  can re-read rather than register from a hash. Correct or qualify the
  chapter VII and VIII bindings that rest on the unreadable 16 October states.
  Register the Holy See message, the video message and the Pontifical Mission
  Societies page if the documents or the resolution appendix rely on them.
  Bind the 2002 Missal's p. 667 and p. 695 rubrics if the mission branch is
  stated from them.
- **Readings page (item 2).** If a direct official delivery of the readings
  page can be had lawfully, read it and compare it with the capture; otherwise
  say in the records that the psalm locator `9-10` and the strophe division
  rest on the March 2026 capture, corroborated by the *Ordo* and the national
  calendar.
- **NABRE Psalms introduction (item 3).** Register the state actually read or
  rest on the registered state only for what its bytes show; reconcile
  standing finding RES-014 (scope.md 8.3 and lead 8; the Souvay binding's loci).
- **Gelasian (Wilson 1894) and Verona (Feltoe 1896) page images (item 4).**
  Register lawful public-domain page-image excerpts for every locus quoted and
  bind them; the current bindings are DjVu OCR records.
- **Schuster, Fromage and Honorius (item 5).** Verify every locus used against
  page images, register facsimile excerpts, and correct the records.
- **The *maiestas* lexical claim (item 7, RES-013).** Verify it in a lawful
  public-domain Latin lexicon such as Lewis and Short (1879) and register it,
  or drop it.
- **Standing findings owned by the research records.** STU-004 (NPNF's
  "worship and honour" against Augustine's *gloriam et honorem* at Ps. 95.8);
  HOM-002 (make `research/scope.md` §2 agree that v. 8 is sung whole, which
  this record's psalm row and boundary check now state from the *Ordo* and the
  capture); RES-015 (anchor the difficulty in Matthew 22:18, *cognita … nequitia
  eorum*).
- **Chronology under orientation-v2.** Regenerate `research/chronology.toml`
  and `research/chronology-annotations.tex` through `tools/tpt
  proper-chronology --presentation orientation-v2` and declare
  `chronology_presentation = "orientation-v2"`; confirm that the `acclamation`
  key gets no narrated-event row. Numbering hazards for the inputs: the
  Entrance antiphon is Hebrew Psalm 17:6, 8, and the finding-aid index gives it
  as Psalm 16 without a per-entry Vulgate flag; Communion antiphon A is Hebrew
  Psalm 33:18–19; the responsorial psalm is Hebrew Psalm 96, the *Ordo*'s
  Psalm 95, with v. 10 partial (10a, 10c); the second reading ends at
  1 Thessalonians 1:5b; the acclamation is Philippians 2:15d, 16a. No biblical
  date is asserted in this record.
- **Instance and leaf audit.** Bring `instance/manifest.md` and
  `propers/verified.md` into line with this record: the General Instruction
  states actually read, the readings-page witness, and the mission branch's
  resolution with its dated witnesses. The inventory, keys and branch IDs are
  unchanged.
- **Still open from the first resolution.** How the approved psalm locator
  stands to the verses sung (9–10 against 9–10a, c) and how the approved
  response stands to v. 7b and to the *Ordo*'s *gloriam et potentiam*, from an
  edition-identified witness to the printed Lectionary; how the adapted
  elements are displayed; and the text the Lectionary follows at Isaiah 45:1
  (*uncto* against *christo*) and 45:4, Psalm 96 (95):5 and 7b, and Matthew
  22:15–21. No textual judgment is made in this record.
- **Dependencies.** `research/review-dependencies.toml` declares the external
  owners relied on: the Week XXIX owner and the edition registry records. The
  authorities adopted here are the USCCB 2026 calendar artifact; the readings
  page for the date as witnessed above; the 2002 Missal artifact with its
  *Tempus per annum* rubrics, the *Normae universales* and General Calendar
  printed in it, its blessings and prayers over the people, and its Masses for
  Various Needs (introduction and no. 18); the United States English GIRM,
  chapters II, VII and VIII, in the states listed above; the 2008 variation
  list in *Notitiae* 44 and the ICEL antiphon excerpt, through the owner; the
  1981 *Ordo lectionum Missae* scan, including *Praenotanda* nos. 79, 89–90,
  105–107, 119 and 123, *Tabella II*, and nos. 145–146 and 173–174; the Holy
  See's two World Mission Day documents and the Pontifical Mission Societies
  page for the dated observance; the Douay–Rheims, Clementine and King James
  editions as read; and, as computation inputs only,
  `src/sources/calendars/postconciliar/propers.yaml` and `rubrics.yaml`.
