# Liturgical Instance Manifest — `PC-S01-B`

**Full publication slug:** `pc-s01-first-sunday-of-advent-year-b`
**Provider:** Anthropic Claude
**As of:** 2026-11-26 (research stage of the `proper-study` v20 production, run `99f04ef5cf9b711b`)

This is the authoritative identity and resolution record of the leaf. The
witnesses behind each resolution, with their hashes and page locators, are in
[`research/context.md`](../research/context.md); the research stage re-read the
Lectionary witnesses and recorded what it found in
[`propers/verified.md`](../propers/verified.md). The Missal formulary's
evidence is in the canonical owner and is not restated here.

## Registry identity

| Field | Resolution | Control |
| --- | --- | --- |
| Stable registry | `guidance/liturgy/postconciliar-propers-registry.md` | Parent `PC-S01`, stem `pc-s01-first-sunday-of-advent` |
| Permanent formula key | `PC-S01-B` | Registered A/B/C shape; Lectionary nos. 1, 2, 3 |
| Full publication slug | `pc-s01-first-sunday-of-advent-year-b` | Stem plus `-year-b`; no form, branch or occurrence suffix |
| Edition registry | [`propers/registry/`](../../../registry/README.md) | [Formula dispositions](../../../registry/formula-dispositions.md), row `PC-S01-B`; [2026 occurrences](../../../registry/occurrences-2026.md), row `PC-S01-B` |
| Canonical formulary owner | [First Sunday of Advent](../../shared/formularies/pc-s01-first-sunday-of-advent/propers/verified.md) | Owner rule for a `PC-S` parent outside Ordinary Time II–XXXIII: `temporal/shared/formularies/<required-slug-stem>/`; shared with Years A and C |
| Calendar family | `postconciliar`, path family `temporal` | Registry path rule for `PC-S` leaves |
| Registry count check | Lectionary no. 2 | The Ordinary Time arithmetic does not apply; no. 2 agrees with both national calendars, the readings page and the *Ordo lectionum Missae* |

## Governing books and jurisdiction

| Field | Resolution |
| --- | --- |
| Missal | *Roman Missal, Third Edition, for Use in the Dioceses of the United States of America* (2011); Latin base *Missale Romanum*, editio typica tertia (2002), *reimpressio emendata* (2008) |
| Lectionary | *Lectionary for Mass for Use in the Dioceses of the United States of America*, second typical edition, Volume I, no. 2; based on the *Ordo lectionum Missae*, editio typica altera (1981). The printed United States volume was not inspected |
| General Instruction | United States English edition of 2011 with the 2021 emendations. Chapter II read in an Internet Archive capture of its official page made on 15 October 2026 (nos. 48, 51, 53, 61, 62, 63, 66, 68, 74, 87); chapters VII and VIII in captures made on 13 and 18 June 2026, byte-identical to registered states (nos. 363–365; 372–376). The publisher's site refused direct requests on 26 November 2026 |
| Calendar | *Universal Norms on the Liturgical Year and the Calendar* and the *Calendarium Romanum generale*, in the Latin printed in the 2002 Missal; USCCB *Liturgical Calendar for the Dioceses of the United States of America*, 2026 and 2027 |
| Territory and language | Dioceses of the United States of America; English. No diocesan, religious, parish, titular, dedication or patronal calendar is resolved |

## Resolved liturgical instance

| Field | Resolution |
| --- | --- |
| Celebration and rank | First Sunday of Advent; a Sunday of Advent, place 2 of the table of liturgical days; violet. Gloria omitted, Creed said |
| Sunday cycle | Year B, from 29 November 2026, which this Sunday opens, through 21 November 2027. The weekday cycle (I) governs no Sunday |
| Occurrence | Sunday 29 November 2026, Psalter Week I. Nothing is inscribed in the General Calendar or the national calendar on the date; the Feast of Saint Andrew falls on Monday 30 November and does not touch this Mass |
| Form | The single Sunday form. An anticipated Saturday-evening Mass uses it; there is no Vigil form and no key for one |
| Homily audience | Adult parish assembly |

## Ordered inventory of appointed elements

| Order | Key | Element | Locus | Status |
| ---: | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | Entrance Antiphon *Ad te levavi animam meam* | Owner; the Missal prints Cf. Ps 24, 1-3 (Hebrew 25:1–3); an adaptation | required |
| 2 | `collect` | Collect *Da, quaesumus, omnipotens Deus, hanc tuis fidelibus voluntatem* | Owner | required |
| 3 | `first-reading` | First Reading | Isaiah 63:16b–17, 19b; 64:2b–7 (*Ordo*); the United States witnesses cite 64:2–7, and their text gives the first member of 64:2 and does not repeat the second, whose words repeat 63:19b (see `propers/verified.md`); Douay–Rheims and Clementine numbering 63:16b–17; 64:1, 3–8; Lectionary no. 2 | required |
| 4 | `responsorial-psalm` | Responsorial Psalm | Psalm 80 (79):2a, 2c, 3b, 15–16, 18–19; response v. 4. The readings page's locator says 2–3 | required |
| 5 | `second-reading` | Second Reading | 1 Corinthians 1:3–9 | required |
| 6 | `acclamation` | Alleluia verse | Psalm 85 (84):8, printed without `Cf.` | required |
| 7 | `gospel` | Gospel | Mark 13:33–37 | required |
| 8 | `prayer-over-offerings` | Prayer over the Offerings *Suscipe, quaesumus, Domine, munera* | Owner | required |
| 9 | `preface` | Preface I of Advent, *De duobus adventibus Christi* | Owner; appointed by the formulary's rubric | required |
| 10 | `communion-antiphon` | Communion Antiphon *Dominus dabit benignitatem* | Owner; the Missal prints Ps 84, 13 (Hebrew 85:13) without `Cf.`, the opening *Etenim* omitted | required |
| 11 | `prayer-after-communion` | Prayer after Communion *Prosint nobis, quaesumus, Domine, frequentata mysteria* | Owner | required |
| 12 | `solemn-blessing` | Solemn blessing *In Adventu* | Owner; the formulary's rubric says it may be used | optional |

Psalms are cited in Hebrew numbering with the Vulgate number in parentheses.
Isaiah is cited in the Lectionary's numbering, which follows the Hebrew
chapter division; the Douay–Rheims and the Clementine Vulgate number the
same text 63:16b–17; 64:1, 3–8.

## Branches and unresolved selections

Branch IDs are those of `research/context.md` and are used unchanged in the
leaf audit: `entrance-or-communion-chant-substitution`,
`psalm-or-acclamation-chant-substitution`, `offertory-chant`,
`sprinkling-rite`, `eucharistic-prayer-with-appointed-preface`,
`eucharistic-prayer-iv-with-preface`,
`reconciliation-or-various-needs-eucharistic-prayer`,
`concluding-blessing-form`, `ritual-or-various-needs-mass`,
`local-proper-calendar` and `advent-wreath-blessing`. No selection was supplied
for any of them and none is inferred. `eucharistic-prayer-iv-with-preface`,
`ritual-or-various-needs-mass` and `local-proper-calendar` are not admitted on
this date; `reconciliation-or-various-needs-eucharistic-prayer` is not
applicable. The research stage read the ritual book for
`advent-wreath-blessing` in a third-party transcription and records it as a
permitted, unselected rite that adds a blessing to the Universal Prayer and
changes no proper text (`propers/verified.md`, Branches).
