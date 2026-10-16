# Liturgical Instance Manifest — `PC-S55-A`

**Full publication slug:** `pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a`
**Provider:** Anthropic Claude
**As of:** 2026-10-16 (revised the same day for the `proper-study` v12 revision, run `821c824684b0c7a7`)

This is the authoritative identity and resolution record of the leaf. The
witnesses behind each resolution, with their hashes and page locators, are in
[`research/context.md`](../research/context.md) and were re-read at the research
stage as [`propers/verified.md`](../propers/verified.md) records; the Missal
formulary's evidence is in the canonical owner and is not restated here.

## Registry identity

| Field | Resolution | Control |
| --- | --- | --- |
| Stable registry | `guidance/liturgy/postconciliar-propers-registry.md` | Parent `PC-S55`, stem `pc-s55-twenty-ninth-sunday-in-ordinary-time` |
| Permanent formula key | `PC-S55-A` | Registered A/B/C shape; Lectionary nos. 145, 146, 147 |
| Full publication slug | `pc-s55-twenty-ninth-sunday-in-ordinary-time-year-a` | Stem plus `-year-a`; no form, branch or occurrence suffix |
| Edition registry | [`propers/registry/`](../../../registry/README.md) | [Formula dispositions](../../../registry/formula-dispositions.md), row `PC-S55-A`; [2026 occurrences](../../../registry/occurrences-2026.md) |
| Canonical formulary owner | [Ordinary Time Week XXIX](../../shared/ordinary-time/weeks/29/propers/verified.md) | Owner rule `55 − 26 = 29`; shared with Years B and C |
| Calendar family | `postconciliar`, path family `temporal` | Registry path rule for `PC-S` leaves |
| Registry count check | `64 + 3 × (55 − 28) + 0 = 145` | Agrees with both dated witnesses and the *Ordo lectionum Missae* |

## Governing books and jurisdiction

| Field | Resolution |
| --- | --- |
| Missal | *Roman Missal, Third Edition, for Use in the Dioceses of the United States of America* (2011); Latin base *Missale Romanum*, editio typica tertia (2002), *reimpressio emendata* (2008) |
| Lectionary | *Lectionary for Mass for Use in the Dioceses of the United States of America*, second typical edition, Volume I, no. 145; based on the *Ordo lectionum Missae*, editio typica altera (1981) |
| General Instruction | United States English edition of 2011 with the 2021 emendations, which governs. Chapter II: the official chapter page, re-read directly on 16 October 2026 and byte-identical to its registered state, at nos. 48, 51, 53, 61, 62, 63, 66, 68, 74 and 87. Chapters VII and VIII: the publisher's site refused direct requests that day, so they were read whole in Internet Archive captures of the official pages made on 13 and 18 June 2026 (chapter VII at nos. 363–365; chapter VIII at nos. 372–374), registered and bound in `research/source-bindings.toml`; the captures show the official text as of those dates. The branch rows of `research/context.md` follow that text and, where they exist, the Latin typical rules of the 2002 Missal |
| Calendar | *Universal Norms on the Liturgical Year and the Calendar* and the *Calendarium Romanum generale*, in the Latin printed in the 2002 Missal; USCCB *Liturgical Calendar for the Dioceses of the United States of America*, 2026 |
| Territory and language | Dioceses of the United States of America; English. No diocesan, religious, parish, titular, dedication or patronal calendar is resolved |

## Resolved liturgical instance

| Field | Resolution |
| --- | --- |
| Celebration and rank | Twenty-ninth Sunday in Ordinary Time; Sunday in Ordinary Time, place 6 of the table of liturgical days; green |
| Sunday cycle | Year A, 30 November 2025 through 22 November 2026. The weekday cycle (II) governs no Sunday |
| Occurrence | Sunday 18 October 2026, Psalter Week I. The Feast of Saint Luke, Evangelist, inscribed on 18 October in the *Calendarium Romanum generale* with the rank of feast (place 7), is omitted under Universal Norms 60 and supplies no text. A church of which Saint Luke is the titular is the separate `local-proper-calendar` case. The same Sunday is the 100th World Mission Day (Holy See message dated to 18 October 2026; in the United States, World Mission Sunday with its collection): an observance of prayer and support with no rank, colour, formulary or text, which displaces nothing; its one liturgical bearing is the conditional branch `mass-for-evangelization-of-peoples` below |
| Form | The single Sunday form. An anticipated Saturday-evening Mass uses it; there is no Vigil form and no key for one |
| Homily audience | Adult parish assembly |

## Ordered inventory of appointed elements

| Order | Key | Element | Locus | Status |
| ---: | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | Entrance Antiphon *Ego clamavi, quoniam exaudisti me, Deus* | Week XXIX owner; the Missal prints Cf. Ps 16, 6.8 (Hebrew 17:6, 8); an adaptation that passes over v. 7, trims the opening phrase of v. 8 and adds a vocative | required |
| 2 | `collect` | Collect *Omnipotens sempiterne Deus, fac nos tibi semper* | Week XXIX owner | required |
| 3 | `first-reading` | First Reading | Isaiah 45:1, 4–6 (vv. 2–3 omitted); Lectionary no. 145 | required |
| 4 | `responsorial-psalm` | Responsorial Psalm | Psalm 96 (95):1 and 3, 4–5, 7–8, 9–10a and 10c; response from v. 7b | required |
| 5 | `second-reading` | Second Reading | 1 Thessalonians 1:1–5b | required |
| 6 | `acclamation` | Alleluia verse | Philippians 2:15d, 16a, printed without `Cf.`; the *Ordo*'s Latin excerpts the two cola | required |
| 7 | `gospel` | Gospel | Matthew 22:15–21 | required |
| 8 | `prayer-over-offerings` | Prayer over the Offerings *Tribue nos, Domine, quaesumus, donis tuis* | Week XXIX owner | required |
| 9a | `communion-antiphon-a` | Communion Antiphon, first | `Cf.` Psalm 33 (32):18–19 | appointed alternative |
| 9b | `communion-antiphon-b` | Communion Antiphon, under *Vel:* | Mark 10:45, adapted, printed without `Cf.` | appointed alternative |
| 10 | `prayer-after-communion` | Prayer after Communion *Fac nos, quaesumus, Domine, caelestium rerum* | Week XXIX owner | required |

Psalms are cited in Hebrew numbering with the Vulgate number in parentheses.

## Branches and unresolved selections

Branch IDs are those of `research/context.md` and are used unchanged in the
leaf audit: `communion-antiphon-psalm`, `communion-antiphon-gospel`,
`entrance-or-communion-chant-substitution`,
`psalm-or-acclamation-chant-substitution`, `offertory-chant`,
`sprinkling-rite`, `compatible-preface-and-eucharistic-prayer`,
`eucharistic-prayer-iv-with-preface`, `concluding-blessing-form`,
`mass-for-evangelization-of-peoples`, `ritual-or-various-needs-mass` and
`local-proper-calendar`. No selection was supplied for any of them and none is
inferred. Both Communion antiphons are studied in full, and a claim resting on
one of them is marked with that antiphon. The three whole-Mass branches
(`mass-for-evangelization-of-peoples`, `ritual-or-various-needs-mass`,
`local-proper-calendar`) would replace this formulary entirely; nothing in this
leaf holds for a celebration that uses one of them. On 18 October 2026 the
condition of the Missal's rubric for the Mass *Pro evangelizatione populorum*
(a particular celebration for the work of the missions) can be met, because
the date is World Mission Day; the rubric permits that Mass and appoints it to
no Sunday, so the branch stays `conditional` and unselected
(`research/context.md`, World Mission Day on 18 October 2026).
