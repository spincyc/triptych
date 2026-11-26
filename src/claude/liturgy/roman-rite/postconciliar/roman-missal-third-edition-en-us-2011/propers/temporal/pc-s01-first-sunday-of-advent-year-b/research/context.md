# Celebration context and complete appointed inventory

Resolved on 26 November 2026 for the `proper-study` v20 production of this
new Claude postconciliar leaf, run `99f04ef5cf9b711b`, seeded at commit
`cbccbfcb3be4896c95225d8cd281e2b0684a12e9`. This is the leaf's first
resolution. No research handoff was supplied.

No other leaf is evidence here: not the Claude leaves for other Sundays, not the
published leaf of the other provider for this same identity or its production
and release records, none of which was opened, and no 1962 record. Nothing in
this record comes from the 1962 calendar, Missal or propers, including those for
the same civil Sunday. This record settles what is studied. It contains no study
prose, spoken text, timing claim or review verdict; research collates the
sources and may correct it from evidence.

## Identity, governing books and territory

| Field | Resolution |
| --- | --- |
| Canonical identity | `liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers/temporal/pc-s01-first-sunday-of-advent-year-b`; calendar family `postconciliar`, path family `temporal` |
| Stable registry | `guidance/liturgy/postconciliar-propers-registry.md`: parent `PC-S01`, First Sunday of Advent, stem `pc-s01-first-sunday-of-advent`; registered keys `PC-S01-A`, `PC-S01-B`, `PC-S01-C` for Lectionary nos. 1, 2, 3 |
| Formula key and slug | `PC-S01-B`; full slug is the stem plus `-year-b`. No form, branch or occurrence suffix is admitted. Every reading of no. 2 has one form only, so the target carries no reading branch |
| Registry checks | The Ordinary Time owner arithmetic does not apply to a `PC-S` parent outside Ordinary Time II–XXXIII. The registry's owner rule for such a parent is `temporal/shared/formularies/<required-slug-stem>/`, here `pc-s01-first-sunday-of-advent`. Lectionary no. 2 for Year B agrees with both national calendars, the readings page and the *Ordo lectionum Missae* below |
| Edition disposition | [Formula dispositions](../../../registry/formula-dispositions.md), row `PC-S01-B`, added at this resolution: adopted as the stable registry lists it, with no cycle expansion. Dated result in [2026 occurrences](../../../registry/occurrences-2026.md), row `PC-S01-B`, added at this resolution, with the ferial note for the First Week of Advent. The registry [README](../../../registry/README.md) records the addition |
| Canonical Missal owner | [First Sunday of Advent](../../shared/formularies/pc-s01-first-sunday-of-advent/propers/verified.md), at the registry-fixed path, opened at this resolution and shared with the Year A and Year C targets. It alone carries the formulary's witnesses, locators, element boundaries, variation check and rights disposition; this record cites its result and restates none of its evidence |
| Build edge | The collection Makefile already declares, against `$(POSTCONCILIAR_US_ROOT)`, `temporal/shared/formularies/pc-s01-first-sunday-of-advent/propers/verified.md` as a prerequisite of this identity's study, `-synthesis` and `-homily` PDFs (read for this resolution). No Makefile change is needed. The collection-wide edges on `shared/exposition-format.tex` and `registry/*.md` apply as well |
| Missal | *Roman Missal, Third Edition, for Use in the Dioceses of the United States of America*, English, implemented 27 November 2011; Latin base *Missale Romanum*, editio typica tertia (2002), in its *reimpressio emendata* (2008) |
| Lectionary | *Lectionary for Mass for Use in the Dioceses of the United States of America*, second typical edition (1998/2001), Volume I, no. 2, with the 2017 *Supplement* where applicable; based on the *Ordo lectionum Missae*, editio typica altera (1981). Both national calendars state this book identity on their printed p. 5 |
| Other controlling books | *General Instruction of the Roman Missal*, United States English edition of 2011 with the 2021 emendations, in the states listed under *General Instruction states read*; *Universal Norms on the Liturgical Year and the Calendar* and the *Calendarium Romanum generale*, read in the Latin printed in the 2002 Missal; the USCCB *Liturgical Calendar for the Dioceses of the United States of America* for 2026 and for 2027 |
| Territory | Dioceses of the United States of America, national calendar only. No diocesan, religious, parish, titular, dedication or patronal calendar was supplied, so none is applied, computed or excluded for an unnamed church |
| Language | The approved United States English governs the celebration. This production prints none of it: Scripture appears in the public-domain Douay–Rheims (Challoner) as a study translation, the orations, Preface and blessing by Latin incipit and description |
| Publication mode | Full three-document study under the postconciliar rights position, authorized for provider `claude` on 26 November 2026 by `guidance/liturgy/propers-production-plan.md`, which makes this an independent production and excludes publication to main from that decision. No reference-only scope is authorized for any target, so this leaf is not reference-only. Protected Lectionary, psalm-refrain and Missal English is treated by description and locus only, as for the edition's other leaves |
| Requested study cycle | Year B, stated by the identity's `-year-b` suffix |
| Cycle appointed on the date | Year B, from 29 November 2026; this Sunday opens it. The requested and the appointed cycle coincide; no substitution is made or needed. The weekday cycle (I in the liturgical year 2027) governs no Sunday, and the Advent weekdays have an annual course (see *The days around it*) |
| Homily audience | Adult parish assembly, for the later homily stage. The homily is authored preaching and adds no text to this inventory |

The finding-aid index `src/sources/calendars/postconciliar/propers.yaml`
carries this Mass as `advent-1`, `registry: pc-s01`. It is a lead, not a source
of record. Its Year B Lectionary citations agree with the *Ordo* read below,
including the first reading's `64:2b-7` and the psalm's `2ac, 3b`, given in
Hebrew numbering by the file's declared `psalm_numbering: hebrew`. It gives
the Entrance antiphon as `Psalm 25:1-3`, without the Missal's *Cf.* and
without a per-entry numbering flag, and the Communion antiphon as `Psalm
85:13`; the Missal prints Vulgate Psalm 24 and 84. The index's own notes say
the antiphons were not read. It carries the three orations as unavailable. This
record controls; the index belongs to its own owner and is unchanged here.

## Occurrence on 29 November 2026

**Computation (finding aid only).** `tools/tpt calendar-days day --calendar
postconciliar --date 2026-11-29 --json` returns the single candidate
`advent-1`, First Sunday of Advent, season Advent, Sunday cycle B, weekday cycle
I, liturgical year 2027, nothing unresolved. Under Universal Norms 40 Advent
begins with Evening Prayer I of the Sunday that falls on or nearest 30
November; in 2026, 30 November is a Monday, so the Sunday is 29 November, one
week after Christ the King (22 November). The Sunday opens the liturgical year
that ends in 2027: `Y = 2027`, and `2027 mod 3 = 2` is Year B. The computed
anchors of that year are Ash Wednesday 10 February, Easter 28 March, Pentecost
16 May and the next First Sunday of Advent 28 November 2027.

**Precedence (finding aid only).** `tools/tpt calendar-rubrics day --calendar
postconciliar --date 2026-11-29 --json` returns `advent-1` on the basis
"place-2-great-day" (locus "NUALC 59 table 2; NUALC 5"). The governing loci were
read in the Latin *Normae universales* as printed in the registered 2002 Missal
artifact: no. 5 (physical PDF pp. 64–65), under which the Sundays of Advent,
Lent and Easter take precedence over every feast of the Lord and every
solemnity, and a solemnity falling on one of them is transferred to the
following Monday, except on Palm Sunday or Easter Sunday; nos. 39–42 (pp.
67–68), on Advent's two characters, its beginning, the naming of its Sundays
and the ferias from 17 December; no. 59 with its table, where *Dominicae
Adventus, Quadragesimae et Paschae* stand at place 2 (p. 70); and no. 60 (pp.
70–71). The *Calendarium Romanum generale* printed in the same artifact
(physical PDF p. 80) inscribes nothing on 29 November and gives 30 November to
*S. Andreae, apostoli*, with the rank *Festum*. Nothing in the General Calendar
competes with the Sunday, and no local celebration could displace it (see
`local-proper-calendar` below).

**Dated official witnesses.**

| Witness | Identity and check | What it states |
| --- | --- | --- |
| USCCB, *Liturgical Calendar for the Dioceses of the United States of America* 2026 | Registered artifact `artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2026.usccb-pdf-4bd9add0`. A fresh copy fetched from the recorded publisher URL on 26 November 2026 matched the registered SHA-256 `4bd9add07512396a2323aa977bc4816a5fad6348262e12740bcee97c77372d02` and 839,777 bytes before any page was read. Restricted; not retained | Printed p. 5 (PDF p. 7): the First Sunday of Advent falls on 29 November 2026; the Sunday cycle is Year B from 29 November 2026 to 21 November 2027; weekday Cycle 2 ends on 28 November 2026; the book identities given above. Printed p. 45 (PDF p. 47), under the running heading for Year B and weekday Cycle I, read in the text layer: 29 November, Sunday, First Sunday of Advent, violet; Is 63:16b-17, 19b; 64:2-7 / 1 Cor 1:3-9 / Mk 13:33-37; Lectionary (2); Psalter Week I. No other celebration and no bracketed optional memorial stands on the date. The Liturgy of the Hours turns to Volume I on the same date |
| USCCB, *Liturgical Calendar for the Dioceses of the United States of America* 2027 | Registered artifact `artifact.united-states-conference-of-catholic-bishops.liturgical-calendar-dioceses-united-states.2027.usccb-pdf-d7997b57`. A fresh copy fetched from the recorded publisher URL on 26 November 2026 matched the registered SHA-256 `d7997b57de96fdbf6433af917a65597b108c720c930f3c39356bf0f5058074ce` and 662,348 bytes before any page was read. Restricted; not retained | Printed p. 5 (PDF p. 7): the liturgical year 2027 begins with the First Sunday of Advent, 29 November 2026; Sunday cycle Year B, 29 November 2026 to 21 November 2027; weekday Cycle 1. Its miscellaneous note 6 says the same of the year's beginning. Printed p. 11 (PDF p. 13): the same entry for 29 November as the 2026 calendar, with the same citations, Lectionary number, Psalter week and colour, and the week that follows (see *The days around it*) |
| USCCB daily readings page for 29 November 2026, `https://bible.usccb.org/bible/readings/112926.cfm` | One state is registered, not held: `artifact.united-states-conference-of-catholic-bishops.daily-readings.2026-11-23-page-for-2026-11-29.lectionary-2-27c3cb63` (retrieved 23 November 2026, 55,747 bytes). A direct request with browser request headers on 26 November 2026 was answered HTTP 200 with 56,311 bytes, SHA-256 `7e0b44c0704f2f7d71440d12a300b6574a40b56b92ae371e38ff9b00677e83d5`. That is a second official state, not byte-identical to the registered one; it was not registered when this record was written, and the source-registration stage of the same run has since registered it as `artifact.united-states-conference-of-catholic-bishops.daily-readings.2026-11-26-page-for-2026-11-29.lectionary-2-7e0b44c0` from this stage's re-hashed receipt. Restricted; nothing of its wording is retained | Heading First Sunday of Advent; Lectionary: 2; Reading 1 Isaiah 63:16b-17, 19b; 64:2-7; Responsorial Psalm 80:2-3, 15-16, 18-19 with response locator (4); Reading 2 1 Corinthians 1:3-9; Alleluia Psalm 85:8, without `Cf.`; Gospel Mark 13:33-37. One form of every unit. Three psalm strophes: the first gives v. 2a, v. 2c and v. 3b only, not the whole of vv. 2–3 that its locator states; the second gives vv. 15–16, ending with a line naming the son of man at v. 16b; the third gives vv. 18–19. In the first reading the clause answering to Hebrew 64:2a, the awesome deeds not hoped for, is present, and the clause of the mountains quaking stands once, after the cry to rend the heavens. The copyright notice attributes the Lectionary text to CCD and the psalm refrain to ICEL |

Computation and all three dated witnesses agree on the celebration, the cycle,
the Lectionary number and every reading's chapter and opening; nothing fails
closed. Two citation differences stand between the United States witnesses and
the Latin *Ordo*, and both are kept, not resolved, in the inventory below: the
first reading's `64:2-7` against the *Ordo*'s `64:2b-7`, and the readings
page's psalm locator `2-3` against the *Ordo*'s `2ac et 3b`, which the page's
own first strophe follows. The printed United States Lectionary volume itself
was not inspected.

**The days around it.** The Sunday's readings, Creed and Preface do not
continue into the week; the Missal gives each Advent weekday its own formulary,
and Monday of the First Week reuses the Sunday's Prayer over the Offerings and
Prayer after Communion (see the owner). The 2027 calendar (printed p. 11) gives
Monday 30 November to the Feast of Saint Andrew, Apostle, with its proper
readings (no. 684); Tuesday 1 and Wednesday 2 December to the Advent weekday
(nos. 176, 177); Thursday 3 December to the Memorial of Saint Francis Xavier,
Priest (no. 178); Friday 4 December to the Advent weekday (no. 179) with the
optional memorial of Saint John Damascene; Saturday 5 December to the Advent
weekday (no. 180); and Sunday 6 December to the Second Sunday of Advent. These
weekday readings are the same every year: *Praenotanda* no. 69.3 makes the
course of the Advent ferias annual, and no. 94 divides it at 17 December. The
2026 calendar (printed p. 45) gives Saturday 28 November to the weekday (no.
508) with the optional memorial of the Blessed Virgin Mary on Saturday. Because
Advent begins with Evening Prayer I of the Sunday, an anticipated Mass of the
Sunday on Saturday evening uses this same formulary and readings; it is not a
Vigil form and has no key.

## Appointed inventory

Twelve ritual places carry twelve text-bearing elements: eleven required and
one optional. Missal elements are cited to the owner, whose record holds their
printed locators, incipits and summaries; the formulary was read for this
resolution at physical PDF pp. 82–83 of the registered 2002 artifact, the
appointed Preface at p. 311 and the Advent solemn blessing at p. 370 (fresh
copy, hash matched; see the owner). Lectionary boundaries were read in four
places: the two national calendars and the readings page above, and the *Ordo
lectionum Missae*, editio typica altera (1981), no. 2, *Dominica prima
Adventus*, Year B, read on 26 November 2026 at 150 dpi in the page image of
printed p. 5 (artifact p. 59) of the registered scan
`artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e`
(fresh copy from the recorded Internet Archive location, SHA-256
`ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d`, 21,487,058
bytes, matched before reading). Under *Praenotanda* no. 119 (printed p.
XLVIII, text layer) the *Ordo* gives chapters and verses after the *Nova
Vulgata*, adding the original-language numbering where they differ; its note
123 numbers the psalms after the 1969 *Nova Vulgata* psalter, which keeps the
Vulgate psalm numbers. The same number lets vernacular editions keep the
numbering of their own approved version. Psalms are cited here in the Hebrew
numbering of the United States Lectionary with the Vulgate number, which the
Latin books and the Douay–Rheims use, in parentheses.

| Order | Key | Element and exact locus | Liturgical place, extent and boundary | Status |
| ---: | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | Entrance Antiphon *Ad te levavi animam meam*; owner | Introductory Rites, at the entrance. The Missal cites Cf. Psalm 24:1–3 in Vulgate numbering (Hebrew 25:1–3). The owner's collation shows an adaptation: no vocative after *Ad te*, and *qui te exspectant* for the Clementine's *qui sustinent te* | required |
| 2 | `collect` | Collect *Da, quaesumus, omnipotens Deus, hanc tuis fidelibus voluntatem*; owner | Concludes the Introductory Rites. No Gloria precedes it on this Sunday. Long conclusion | required |
| 3 | `first-reading` | Isaiah 63:16b–17, 19b; 64:2b–7 (*Ordo*), cited 63:16b–17, 19b; 64:2–7 by the United States witnesses; Lectionary no. 2 | Liturgy of the Word, first reading. One form only, in three segments. It opens at the second half of 63:16, the confession of the Lord as Father and Redeemer, with the *Ordo*'s incipit *Tu, Domine, pater noster*; omits 63:18–19a; gives 63:19b, the cry that the Lord rend the heavens and come down; omits 64:1 and, in the *Ordo*, 64:2a; and runs from 64:2b to the end of 64:7, the clay and the potter. It ends before the plea of 64:8. Numbering hazard: see *Boundary checks* | required |
| 4 | `responsorial-psalm` | Psalm 80 (79):2ac and 3b, 15–16, 18–19, response from v. 4; Lectionary no. 2 | After the first reading. Three strophes. V. 2b, v. 3a, vv. 4–14 (v. 4 except as the response) and v. 17 are not sung. The *Ordo* prints the locator as *Ps 79, 2ac et 3b. 15-16. 18-19* and the response (v. 4) as *Deus, converte nos, illustra faciem tuam, et salvi erimus*; the United States page prints the locator as 2–3 and sings only 2a, 2c and 3b. Hebrew and Vulgate verse numbers coincide in this psalm; the tracked King James Version, which does not number the title, is one lower | required |
| 5 | `second-reading` | 1 Corinthians 1:3–9; Lectionary no. 2 | Second reading. One form only. It opens with the greeting of grace and peace (v. 3), after the address of vv. 1–2, and ends with v. 9, God's faithfulness in calling them into fellowship with his Son. V. 10 begins the appeal for unity and is not read. The *Ordo*'s incipit is *Fratres: Gratia vobis et pax* | required |
| 6 | `acclamation` | Alleluia with verse Psalm 85 (84):8; Lectionary no. 2 | Before the Gospel. The *Ordo* prints it as *Ut supra, n. 1*, the same verse as Year A: *Ostende nobis, Domine, misericordiam tuam, et salutare tuum da nobis*, which agrees with the tracked Clementine word for word. Printed without `Cf.` on the readings page | required |
| 7 | `gospel` | Mark 13:33–37; Lectionary no. 2 | Gospel. One form only. The command to watch because the time is unknown, the parable of the man gone abroad who leaves his servants their work and the doorkeeper his watch, the four watches of the night, and the closing word to all, *Watch*. It opens after v. 32, the saying that no one knows the day or hour, and ends before 14:1. The *Ordo* opens it with *In illo tempore: Dixit Iesus discipulis suis: Videte, vigilate* | required |
| 8 | `prayer-over-offerings` | Prayer over the Offerings *Suscipe, quaesumus, Domine, munera quae de tuis offerimus collata beneficiis*; owner | Liturgy of the Eucharist, after the preparation of the gifts; short conclusion | required |
| 9 | `preface` | *Praefatio I de Adventu*, *De duobus adventibus Christi*; owner (the formulary's rubric *Praefatio I de Adventu, p. 518*; Order of Mass no. 33, physical p. 311) | Opens the Eucharistic Prayer. Appointed by the formulary; the Preface's own rubric assigns it to Masses of the season from the First Sunday of Advent to 16 December | required |
| 10 | `communion-antiphon` | Communion Antiphon *Dominus dabit benignitatem*, Psalm 85 (84):13; owner | At Communion. Printed without `Cf.`, though the owner's collation shows the opening *Etenim* omitted. One antiphon only | required |
| 11 | `prayer-after-communion` | Prayer after Communion *Prosint nobis, quaesumus, Domine, frequentata mysteria*; owner | Concludes the Communion Rite; short conclusion | required |
| 12 | `solemn-blessing` | Solemn blessing *In Adventu*, *Omnipotens et misericors Deus, cuius Unigeniti adventum*; owner (the formulary's rubric *Adhiberi potest formula benedictionis sollemnis, p. 606*; physical p. 370) | Concluding Rites, in place of the simple blessing. Three invocations, each answered *Amen*, then the Trinitarian blessing | optional |

**The acclamation's key.** Element 6 is keyed `acclamation`, as in the
edition's other leaves, not with a key beginning `gospel`. Research confirms,
when it generates the chronology under `orientation-v3`, that the key receives
no narrated-event row.

The formulary prints no Offertory antiphon, Sequence, proper Eucharistic
Prayer insert, prayer over the people, second Communion antiphon or second
Collect. The Lectionary prints no alternative or shorter form of any reading,
no second psalm response and no second acclamation verse for Year B.

**Boundary checks made against tracked Scripture.** The Douay–Rheims
(`edition.english-college-of-douay.douay-rheims-bible.challoner-gutenberg-1581`),
the Clementine Vulgate (`edition.catholic-church.vulgata-clementina.ebible-latvuc`)
and the King James Version (`edition.church-of-england.king-james-version.ebible-engkjv`)
were read at Isaiah 63:15–64:9, Psalm 79 (80), Psalm 24 (25):1–4, Psalm 84
(85):1, 8 and 13, 1 Corinthians 1:1–10 and Mark 13:32–14:1.

- *Isaiah: the chapter division.* All three tracked editions keep the older
  division of chapters 63–64: the cry *Utinam dirumperes caelos, et
  descenderes*, which the *Ordo* and the United States witnesses number 63:19b,
  stands in them as 64:1, together with the mountains flowing down before the
  Lord; their 63:19 has only the first half of the Hebrew verse. Hebrew 64:1–7
  is therefore their 64:2–8. In tracked-edition numbering the *Ordo*'s
  appointment is 63:16b–17; 64:1, 3b–8, and the whole verses touched are
  63:16–17; 64:1, 3–8. 63:16b begins at the Clementine's second *tu, Domine,
  pater noster*, after the denial that Abraham and Israel know the people. The
  reading ends with Clementine 64:8, *nos vero lutum; et fictor noster tu*; the
  plea *Ne irascaris* (Clementine 64:9) is not read.
- *Isaiah: 64:2 against 64:2b.* Clementine 64:3, Hebrew 64:2, has two members:
  *Cum feceris mirabilia, non sustinebimus* and *descendisti, et a facie tua
  montes defluxerunt*. The *Ordo* begins at the second, so that its Latin
  reading would state the mountains' flowing twice, at 63:19b and 64:2b. The
  United States witnesses cite the whole of v. 2, and the readings page's text
  carries a clause answering to the first member while giving the quaking of
  the mountains only once. How the approved English arranges and numbers
  63:19–64:2, and whether the United States citation reflects *Praenotanda* no.
  119's permission to follow the approved version's numbering, are research
  questions. No textual judgment is made here.
- *Psalm 80 (79).* The Clementine and Douay–Rheims number the title as v. 1,
  as the *Ordo* and the United States Lectionary do. V. 2 has three members
  (the Shepherd of Israel addressed, Joseph led like a flock, the one enthroned
  on the cherubim asked to shine forth) and the appointment omits the second;
  v. 3 has two (before Ephraim, Benjamin and Manasseh; stir up your might and
  come to save us) and the appointment keeps the second. The refrain v. 4
  recurs as vv. 8 and 20. In the Clementine and Douay–Rheims v. 16 ends with
  *et super filium hominis quem confirmasti tibi*, the same words that end v.
  18; the King James Version, translating the Hebrew, has *the branch that
  thou madest strong for thyself* in the corresponding verse (its 80:15). The
  *Ordo*'s response reads *illustra faciem tuam* where the Clementine v. 4
  reads *ostende*.
- *1 Corinthians 1.* Clementine and Douay–Rheims v. 3 is the greeting, v. 9
  ends *in societatem filii ejus Jesu Christi Domini nostri*, and v. 10 opens
  the appeal *Obsecro autem vos*. The King James numbering coincides.
- *Mark 13.* V. 32 is the saying about that day or hour; v. 33 opens *Videte,
  vigilate, et orate*; v. 37 is the closing word to all, *Vigilate*; 14:1 turns
  to the Passover two days later. The three editions' verse numbers coincide.
- *The antiphons' sources.* Clementine Psalm 24:1 carries the title before *Ad
  te, Domine, levavi animam meam*; Psalm 84:1 is a title and 84:13 opens with
  *Etenim*. Vulgate 24 and 84 are Hebrew 25 and 85, the King James Version's
  numbering; the Douay–Rheims follows the Vulgate.

**Relationship classes, preliminary.** The 1981 *Praenotanda* control. No. 67
(printed pp. XXXII–XXXIII) describes the best harmony between the Old and New
Testament readings as one Scripture itself suggests, and says that in Advent,
Lent and Easter, seasons with their own character, the readings of each Mass
are composed in another way, while only the Sundays *per annum* have
semi-continuous apostolic and Gospel readings. No. 68 refuses a thematic
composition imposed for the convenience of preaching. No. 93 (printed p. XL)
describes the Sundays of Advent: the Gospel of the First Sunday concerns the
Lord's coming at the end of time; the Old Testament readings are prophecies of
the Messiah and the messianic time, chiefly from Isaiah; the apostolic
readings give exhortations and proclamations according to the season's
different characters. The Isaiah reading, the 1 Corinthians reading and the
Gospel are therefore each `seasonal or ritual`, chosen for Advent and for this
Sunday's character, and none is `semi-continuous`; the *Ordo* gives no
`officially correlated` pairing of the first reading with the Gospel in the
terms it uses for the Sundays *per annum*, and any connection between them
beyond what nos. 93 and 123 support is research. Under GIRM 61–62 (United
States English, in the chapter II state read for this resolution) the psalm is
`responsorial` and the verse before the Gospel `acclamatory`. Universal Norms
39 (physical p. 67) gives Advent a double character, preparation for the
Nativity's remembrance of the first coming and direction of minds to the
second coming at the end of time; the appointed Preface's title and
embolism name the same two comings. That correspondence is a `textual
observation` about the Missal's own words. The Missal antiphons, orations,
Preface and blessing are shared by all three cycles; every connection between
them and the Year B readings is `source-grounded synthesis` or an `editorial
or AI proposal`, as the three-document profile settles for every formulary.

**The *Ordo*'s own tituli.** *Praenotanda* no. 123 (printed p. XLIX) says that a
titulus indicates the chief theme of its reading and, where necessary, the link
between the readings of one Mass. At no. 2 (printed p. 5, page image) the
*Ordo* prints three:

| Reading | Titulus | Source of the words |
| --- | --- | --- |
| Lectio I | *Utinam dirumperes caelos et descenderes!* | Isaiah 63:19b (Clementine 64:1, *Utinam dirumperes caelos, et descenderes*), without the following *a facie tua montes defluerent* |
| Lectio II | *Revelationem exspectamus Domini nostri Iesu Christi* | 1 Corinthians 1:7, recast; the Clementine has *exspectantibus revelationem Domini nostri Jesu Christi*, a participle referring to the Corinthians |
| Evangelium | *Vigilate: nescitis quando dominus domus veniat* | Mark 13:35, without the Clementine's *ergo* and *enim* |

These are edition-controlled evidence of what the Lectionary singles out in
each reading: the plea for the Lord's descent, the waiting for Christ's
revelation, and the watch for the master's return. What, if anything, they
establish about a link between the readings is for research and the studies;
no. 123 permits a link to be shown by tituli and does not say that these three
show one.

## Branches and other text-bearing parts of this Mass

No local selection was supplied for any branch, and none is inferred. The
Missal rubrics cited were read for this resolution in the registered 2002
artifact (the formulary at pp. 82–83; the Preface rubric at p. 311; the solemn
blessings at p. 370; the Reconciliation Eucharistic Prayers' rubric at p. 390
and the Eucharistic Prayer for Various Needs at p. 399). The General
Instruction loci were read in the states listed under *General Instruction
states read*.

| Branch ID | Authority and trigger | Status | Places affected | Resolution |
| --- | --- | --- | --- | --- |
| `entrance-or-communion-chant-substitution` | GIRM 48 and 87 in the governing United States English, which give four options for each chant: the Missal antiphon, or the *Graduale Romanum* antiphon with its psalm; the antiphon and psalm of the *Graduale Simplex* for the liturgical time; a chant from another collection of psalms and antiphons approved by the Conference of Bishops or the Diocesan Bishop; or another suitable liturgical chant, likewise approved. Without singing, the Missal antiphon is recited (48) or may be recited (87) | permitted | 1, 10 | Unselected. The Missal antiphons are the studied layer. A sung substitute replaces the antiphon's text at that celebration, so no claim resting on an antiphon's wording holds where it is not used |
| `psalm-or-acclamation-chant-substitution` | GIRM 61 and 62 a in the governing United States English: when the psalm is sung, responses and psalms chosen for the times of the year may be used instead of the text corresponding to the reading; in the United States, the Responsorial Gradual of the *Graduale Romanum*, the Responsorial or Alleluia Psalm of the *Graduale Simplex*, or an approved antiphon and psalm from another collection may be sung instead; songs or hymns may not replace the Responsorial Psalm. The Alleluia verse is taken from the Lectionary or the *Graduale* (62 a). The *Ordo*'s common texts for sung psalms (nos. 173–174, printed pp. 97–98, read at artifact pp. 151–152) give for Advent the common response *Veni, Domine, ad liberandum nos!* and the common psalms Psalm 25 (24):4bc–5ab, 8–9, 10 and 14 (response v. 1b) and Psalm 85 (84):9ab–10, 11–12, 13–14 (response v. 8a) | permitted | 4, 6 | Unselected. The Lectionary's psalm and verse are the studied layer. With two readings before the Gospel, GIRM 63 does not apply. The *Ordo*'s common texts were read here for their Advent response and psalms only. A common psalm replaces Psalm 80 and its refrain wherever it is sung |
| `offertory-chant` | GIRM 74 in the governing United States English: the Offertory chant accompanies the procession with the gifts at least until they are placed on the altar, follows the norms for the Entrance chant (no. 48), and may accompany the rite even without a procession | permitted | preparation of the gifts | Unselected. The Missal prints no Offertory antiphon; that silence does not mean the rite has no chant |
| `sprinkling-rite` | GIRM 51 (United States English): from time to time on Sundays, especially in Easter Time, the blessing and sprinkling of water may take place instead of the customary Penitential Act, as a reminder of Baptism | ritual substitution | Introductory Rites | Unselected; it brings its own texts and adds no proper of this formulary. Advent is not excluded by the rule |
| `eucharistic-prayer-with-appointed-preface` | The formulary's rubric appoints Preface I of Advent; GIRM 364 and 365 a–c (United States English). Prayer I may always be used and is called especially suited to Sundays unless Prayer III is preferred for pastoral reasons (365 a); Prayer II, though it has its own Preface, may be used with other Prefaces (365 b); Prayer III may be said with any Preface and is preferred on Sundays and festive days (365 c) | permitted | 9 and the Eucharistic Prayer | Unselected. The Preface is fixed; the Eucharistic Prayer said with it is a choice among I, II and III. If Prayer II is used with its own Preface rather than Preface I of Advent, element 9 is not said, so that combination is recorded here and not assumed |
| `eucharistic-prayer-iv-with-preface` | GIRM 365 d (United States English): Prayer IV has an invariable Preface and may be used when a Mass has no Preface of its own and on Sundays in Ordinary Time | not admitted | 9 and the Eucharistic Prayer | This Mass has an appointed Preface and is not a Sunday in Ordinary Time, so neither condition of 365 d is met. Recorded as excluded on the governing text's own terms |
| `reconciliation-or-various-needs-eucharistic-prayer` | The 2002 Missal's rubric for the Reconciliation Eucharistic Prayers (p. 390): usable in Masses that convey the mystery of reconciliation in a particular way, for example the listed Masses for Various Needs and Masses in Lent, with their own Prefaces or with other Prefaces of penance and conversion. The rubric of the Eucharistic Prayer for Various Needs (p. 399): fitted to the formularies of Masses for Various Needs, with its own invariable Prefaces | not applicable | 9 and the Eucharistic Prayer | Neither rubric names a Sunday of Advent or a Preface of Advent. The United States English rubrics of these prayers were not read; research confirms before the documents say more than that they are not part of this Mass's appointment |
| `concluding-blessing-form` | The formulary's rubric (*Adhiberi potest formula benedictionis sollemnis, p. 606*) and the section rubric of the solemn blessings (p. 370), which makes them usable at the priest's discretion at the end of Mass; the prayers over the people (p. 379) are likewise optional | permitted | 12 | Unselected. Where no solemn blessing is used, element 12 is not said and the simple blessing of the Order of Mass is given. The Advent blessing is the one the formulary names; the use of another solemn blessing or a prayer over the people is not resolved here |
| `ritual-or-various-needs-mass` | GIRM 372 (United States English): Ritual Masses are prohibited on the Sundays of Advent; 374: a Mass for graver need or pastoral advantage, at the direction or with the permission of the Diocesan Bishop, may be celebrated on any day except, among others, the Sundays of Advent; both read in the chapter VIII state below | not admitted | whole Mass | Excluded on this date by the governing text. No replacement formulary applies |
| `local-proper-calendar` | Universal Norms 5, 59 and 60: a proper solemnity of a particular calendar stands at place 4 of the table, below the Sundays of Advent at place 2; a solemnity falling on an Advent Sunday is transferred to the Monday | not admitted | whole Mass | No local celebration displaces this Sunday. A local solemnity on 29 November moves to Monday 30 November, where it meets the Feast of Saint Andrew; that further case belongs to a local resolution and is not made here |
| `advent-wreath-blessing` | *Book of Blessings* nos. 1509–1527, read by the research stage in the Catholic Culture transcription of 26 November 2026 (`propers/verified.md`, Branches); the printed ritual book was not read | permitted | Universal Prayer (its conclusion) | Unselected. Resolved by the research stage (`propers/verified.md`, Branches): the order within Mass concludes the general intercessions with the prayer of blessing; it adds a blessing, replaces no proper text and changes no reading. When this record was written it was an unverified lead; nothing in the Missal formulary or the General Instruction read here appoints it |

| Place | Text and appointment | Status |
| --- | --- | --- |
| Gloria | Omitted by the formulary's rubric *Non dicitur Gloria in excelsis*; GIRM 53 (United States English) has the Gloria on Sundays outside Advent and Lent | omitted |
| Creed | Said by the formulary's rubric *Dicitur Credo*; GIRM 68 has the Creed on Sundays | required |
| Homily; Universal Prayer | Authored or locally composed; no appointed text. On Sundays a homily is required at every Mass with the people (GIRM 66) | not applicable |
| Feast of Saint Andrew, Apostle | Falls on Monday 30 November and does not touch this Mass; no Collect, commemoration or reading enters it | not applicable |
| Sequence; proper Eucharistic Prayer insert | None appointed | not applicable |

## General Instruction states read

The United States English General Instruction governs every branch row above
that cites it. Direct requests to the publisher's chapter pages for chapters
II, VII and VIII on 26 November 2026, with browser request headers, were each
answered HTTP 403 with a 15,748-byte "Checking connection" challenge page
(SHA-256 `639e2732…`); no attempt was made to defeat it. Each chapter was read
whole instead in an Internet Archive capture of its official URL, fetched in
original-bytes form (`id_`).

| Chapter | State read for this resolution | Loci verified | Relation to the library |
| --- | --- | --- | --- |
| II, *The Structure of the Mass, Its Elements, and Its Parts* | Capture of `https://www.usccb.org/prayer-and-worship/the-mass/general-instruction-of-the-roman-missal/girm-chapter-2` at timestamp `20261015002800`, fetched twice byte-identically: gzip-encoded transfer 31,013 bytes, SHA-256 `0d88e106c814bac0116c4e76c7169ea299b62fcdddab57359c204425736a6ae0`; decoded HTML 108,769 bytes, SHA-256 `b6bc5b799ad6ddee1c64270dbf3f122706ddbaa1ab94e8daa1f0eb324b15d6eb` | Nos. 48, 51, 53, 61, 62, 63, 66, 68, 74 and 87 | Matched no registered chapter II state when read; the nearest, registered from a direct delivery of 16 October 2026 (`…usccb-chapter-ii-html-2026-10-16-d10afff3`, 109,916 bytes), could not be re-read. Since registered by the source-registration stage of the same run as `artifact.catholic-church.institutio-generalis-missalis-romani.english-us-2011-emended-2021.usccb-chapter-ii-wayback-2026-10-15-b6bc5b79` |
| VII, *The Choice of the Mass and Its Parts* | Capture at timestamp `20260613160611`: decoded HTML 58,095 bytes, SHA-256 `e973bb8ffe42f31b3eb4addba2acff9d7b9ef38406536a6667b8692b60d77631` | Nos. 363, 364 and 365 a–d | **Byte-identical to the registered state** `artifact.catholic-church.institutio-generalis-missalis-romani.english-us-2011-emended-2021.usccb-chapter-vii-wayback-2026-06-13-e973bb8f` |
| VIII, *Masses and Prayers for Various Needs and Occasions and Masses for the Dead* | Capture at timestamp `20260618180311`: gzip-encoded transfer 14,128 bytes; decoded HTML SHA-256 `dbdf98d997624444d08d4d3533fa085138de5dafb357e79a70cd82e32dce32aa` | Nos. 372–376 | **Byte-identical to the registered state** `artifact.catholic-church.institutio-generalis-missalis-romani.english-us-2011-emended-2021.usccb-chapter-viii-wayback-2026-06-18-dbdf98d9` |

The captures are a third party's copies of the official pages: they show what
the official page said on the capture dates, not what it says on 26 November
2026. Nothing the documents state from these chapters should go beyond the
loci listed, and the documents should date the reading, for example: chapter
II read in an Internet Archive capture of its official page made on 15 October
2026, chapters VII and VIII in captures made on 13 and 18 June 2026, because
the publisher's site refused direct requests on 26 November 2026. Where the
Latin typical rules exist they were read in the 2002 Missal and agree with
the rows above (the formulary's Gloria, Creed, Preface and blessing rubrics;
Universal Norms 5, 59 and 60).

## Lawful study-text routes

- **Scripture: the three readings, the psalm, the acclamation verse's source,
  and the scriptural sources of both antiphons.** The Douay–Rheims
  (Challoner) as registered above; `…american-1899-ebible` is the other
  registered Douay printing. It is a study translation in Vulgate numbering and
  is not the proclaimed text; the standing notice of
  `guidance/liturgy/postconciliar-propers.md` is mandatory. Because its
  chapter division of Isaiah differs from the Lectionary's, every Isaiah
  citation must give both numberings: the reading is Lectionary 63:16b–17, 19b;
  64:2(b)–7, shown from Douay–Rheims 63:16b–17; 64:1, 3(b)–8. Partial verses
  (Isaiah 63:16b and 63:19b; the *Ordo*'s 64:2b; Psalm 80 (79):2a, 2c and 3b)
  must be shown as partial, with the excluded words marked as context, never
  silently trimmed or extended; until research settles 64:2, the excluded or
  disputed first member is shown as context, not as appointed text. The
  omitted Isaiah 63:18–19a and 64:1 (Douay–Rheims 64:2), and the psalm's
  omitted vv. 4–14 and 17, are marked as omissions. The psalm's title, which stands as
  v. 1 in the Douay–Rheims, is not part of the first strophe.
- **Adapted texts.** Both antiphons are adaptations: the Entrance antiphon
  marked *Cf.*, the Communion antiphon unmarked but without *Etenim*. The
  *Ordo*'s psalm response and two of its tituli are recast extracts.
  Douay–Rheims verses may stand beside each as its identified scriptural
  source, labelled as such and with the departures stated, never as the
  adapted text itself. English must never be composed to stand for any of them.
- **Latin comparison text.** The Clementine Vulgate as registered above,
  public domain, for verse boundaries and for comparing the antiphons, the
  response and the acclamation verse. It is not the Missal's or the
  Lectionary's Latin.
- **Orations, Preface and blessing.** Latin incipit and an original description
  of what each asks or proclaims, cited to the owner. No rendering of the
  project's own, and no paraphrase close enough to reconstruct the approved
  English.
- **Approved English.** Not reproduced in any of the three PDFs. The rights
  records that control it are `guidance/liturgical-text-publication-policy.md`
  and the `advent-1` rows of `src/sources/inventories/postconciliar-proper-translations-v1.toml`
  and `postconciliar-proper-latin-provenance-v1.toml`, read as leads only. The
  General Instruction and the readings page are described, not transcribed,
  beyond the short Latin rubrics quoted above from the 2002 Missal.

## Sources read for this resolution

The existing source library was read before anything was fetched: the artifact
records of both national calendars, the 2002 Missal and the 2008 *reimpressio*
edition record, the 2008 *Notitiae* variation list, the ICEL antiphon excerpt,
the 1981 *Ordo*, the registered General Instruction states (chapters II, VII
and VIII), the registered state of the readings page, the passage records for
this formulary's Communion antiphon and Prayer over the Offerings, the
edition registry, the stable registry, the Makefile edge, the finding-aid
index and the `advent-1` rows of the translations, Latin-provenance,
seasonal-collation, Missal-witness-link and e-Missal-link inventories. Six
registered artifacts whose bytes the repository identifies but does not hold
were fetched again, whole, from their recorded locations into ignored scratch
space and matched to their registered hashes before reading: the two national
calendars, the 2002 Missal, the 1981 *Ordo*, the *Notitiae* issue and the ICEL
excerpt. The readings page was fetched directly and gave an unregistered state.
The General Instruction chapters were refused directly and read in the captures
described above, two of them matching registered states. The tracked
Douay–Rheims, Clementine and King James editions were read at the loci
listed. Nothing fetched is retained in the repository; protected English is
described, not transcribed. Neither printing of the United States English
altar book named in the source library (a publisher's preview and an
unidentified Internet Archive printing) was read.

## Remaining verification for research

*Status after the research stage (iterations 0–2, 26 November 2026).* Each
item below is marked with where it was settled. What remains open is: the
printed United States Lectionary and its 1970 English at Isaiah 64:2; the
Hebrew of Psalm 80:16b; a named United States altar-book printing; the printed
*Book of Blessings*; the other sacramentaries Wilson names for the Collect;
and the antecedents of the solemn blessing and of the Preface's first half
(`propers/verified.md`, Outstanding; `research/scope.md` section 10).

- **Register and bind what was read here.** Done by the research and
  source-registration stages of the same run: the readings-page state of 26
  November 2026 is registered as `…daily-readings.2026-11-26-page-for-2026-11-29.lectionary-2-7e0b44c0`
  and the chapter II capture as
  `…usccb-chapter-ii-wayback-2026-10-15-b6bc5b79`; both, the chapter VII and
  VIII states, the Missal (pp. 64–65, 67–68, 70–71, 80, 82–83, 311, 370, 379,
  390 and 399), the *Ordo* (no. 2, *Praenotanda* nos. 67–69, 93–94, 119 and
  123, nos. 173–174) and both national calendars are bound in
  `research/source-bindings.toml` with these loci.
- **Isaiah 63:19–64:2 (first reading).** Establish from an edition-identified
  witness to the printed United States Lectionary, and to the approved
  translation it uses, how 63:19b and 64:2 are arranged and numbered, and so
  whether the United States citation `64:2-7` and the *Ordo*'s `64:2b-7`
  differ in extent or only in numbering. Compare the *Nova Vulgata* at Isaiah
  63:19–64:2, which no tracked edition witnesses. *Settled in part:*
  `propers/verified.md` finding 1 compares the *Nova Vulgata* and the
  readings page and explains the difference by the NABRE note on 64:2; the
  printed Lectionary and its 1970 English remain unread (open).
- **Psalm 80 (first strophe and v. 16).** Record how the printed Lectionary
  states the psalm's locator against the verses sung (2–3 against 2ac, 3b),
  and how the Lectionary's v. 16b stands to the Hebrew *ben* and the Vulgate's
  *filium hominis*; compare the *Ordo*'s response *illustra* with the *Nova
  Vulgata* psalter. *Settled in part:* `propers/verified.md` finding 2 (the
  locator against the verses sung; *illustra* is the *Nova Vulgata*'s; v. 16b
  in the Latin, Douay and King James); the Hebrew of v. 16b was not read
  (open).
- **The owner's open questions.** Through the owner: the antiphons' wording
  against the *Nova Vulgata* (*exspectant*; the omitted *Etenim*); the
  antecedents of the Collect, Prayer over the Offerings, Prayer after
  Communion, Preface and blessing, with the inventories' Verona lead for the
  Prayer over the Offerings checked against its witness; the repetition of the
  Sunday's orations on Advent weekdays and of the Communion antiphon in the
  Mass *In agris conserendis*; collation of a named United States altar-book
  printing, including the English rubric for the Preface and the
  Reconciliation and Various Needs prayers; passage records for the pages read.
  *Settled in part:* owner findings 5–8 (the antiphons against the *Nova
  Vulgata*; the Collect in the Gelasian; the Prayer over the Offerings,
  Prayer after Communion and Preface in the Verona) and `research/scope.md`
  section 3.7. Open: the solemn blessing's antecedent, the Preface's first
  half, the other books Wilson names, and a named altar-book printing.
- **Ritual book lead.** Read the United States *Book of Blessings* on the
  Advent wreath before any document mentions it, and either record the
  branch's authority and place from that reading or drop it. *Settled:*
  `propers/verified.md`, Branches (read in the transcription; permitted,
  unselected). The printed book remains unread (open).
- **Chronology under `orientation-v3`.** Write `research/chronology-inputs.toml`
  against the twelve keys above, in order, with the owner as `shared_owner`,
  and generate the annotations and `research/chronology-table.tex` through
  `tools/tpt proper-chronology annotations --presentation orientation-v3`.
  Numbering hazards for the inputs: the first reading's chapter division (the
  Lectionary's 63:19b is Vulgate and King James 64:1, and its 64:2–7 their
  64:3–8); the psalm is Hebrew Psalm 80, the *Ordo*'s Psalm 79, with v. 2
  partial (2a, 2c) and v. 3 partial (3b), and the King James numbering one
  lower; the Entrance antiphon is Hebrew Psalm 25:1–3, which the finding-aid
  index gives without a numbering flag or *Cf.*; the Communion antiphon and
  the acclamation are Hebrew Psalm 85:13 and 85:8. The Preface and the blessing
  are not Scripture. No biblical date is asserted in this record. *Settled:*
  `research/chronology-inputs.toml`, `research/chronology.toml`, the
  annotations and `research/chronology-table.tex` are written and checked
  (`research/scope.md` section 8).
- **Instance and leaf audit.** Write `instance/manifest.md`, whose ordered
  inventory rows the chronology adapter reads, and `propers/verified.md` in
  line with this record: the keys and order above, the branch IDs, the
  witnesses actually read and their states, and the two citation differences
  kept open. *Settled:* both records are written (`instance/manifest.md`;
  `propers/verified.md`).
- **Dependencies.** `research/review-dependencies.toml` declares the external
  owners relied on: the First Sunday of Advent owner and the edition registry
  records (`README.md`, `formula-dispositions.md`, `occurrences-2026.md`). The
  authorities adopted here are the USCCB 2026 and 2027 calendar artifacts; the
  readings page for the date as witnessed above; the 2002 Missal artifact with
  this formulary, its Preface and blessing, the *Normae universales* and
  General Calendar printed in it, and its Eucharistic Prayer rubrics; the
  United States English GIRM, chapters II, VII and VIII, in the states listed
  above; the 2008 variation list in *Notitiae* 44 and the ICEL antiphon
  excerpt, through the owner; the 1981 *Ordo lectionum Missae* scan, including
  *Praenotanda* nos. 67–69, 93–94, 119 and 123 and nos. 2 and 173–174; the
  Douay–Rheims, Clementine and King James editions as read; and, as
  computation inputs only, `src/sources/calendars/postconciliar/propers.yaml`
  and `rubrics.yaml`. *Settled:* `research/review-dependencies.toml` is
  written: it declares the owner, the edition registry and the calendar
  inputs among its paths, and the other authorities are bound by source ID in
  `research/source-bindings.toml`.
