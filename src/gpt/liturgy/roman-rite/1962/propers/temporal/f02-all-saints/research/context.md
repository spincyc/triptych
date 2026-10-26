# All Saints — celebration and appointed-text inventory

Publication mode: **complete**. The production plan authorizes provider `gpt`, identity `liturgy/roman-rite/1962/propers/temporal/f02-all-saints`, on 25 October 2026 and explicitly states that no reference-only target is authorized. The intended canonical label is `Full PDF`. This context settles identity and appointments; the research stage must complete the source-text and reception work in [source-plan.md](source-plan.md).

## Identity and governing scope

| Field | Resolution |
| --- | --- |
| Provider and source owner | GPT; this canonical leaf, with `main.tex`, `synthesis.tex` and `homily.tex` ultimately sharing one research and generation record |
| Permanent identity | F02, All Saints; a fixed-date general-calendar feast, not a temporal Sunday number |
| Governing book | *Missale Romanum*, Vatican editio typica 1962; its incorporated *Rubricae generales* and *Rubricae generales Missalis romani* |
| Printed identity | *Die 1 novembris — In Festo Omnium Sanctorum — I classis*, Sanctorale, printed pp. 702–703 |
| Calendar and territory | Roman Rite, 1962 General Roman Calendar; no national, diocesan, religious, titular, patronal or dedication supplement has been requested or established |
| Language | Latin appointments; original English study commentary; human historical public-domain study English under the profile, with its source identified |
| Requested civil occurrence | Sunday, 1 November 2026 |
| Actually appointed Mass | All Saints, I classis, white; privileged commemoration of the Twenty-third Sunday after Pentecost |
| Cycle | Annual 1962 appointments; A/B/C and I/II are inapplicable |
| Audience | Adult parish assembly for the eventual standalone homily |
| Excluded questions | Present canonical permission to use the book, local Mass schedules, territorial holy-day discipline and particular-calendar overrides |

The study follows the 1962 proper profile and schema-2 three-document profile. The latter owns its extent, interpretation requirements and concise opening. The identity remains F02 in other years; the three Sunday commemoration prayers below belong to this dated occurrence. No second Sunday study or postconciliar companion identity is established by that commemoration.

## Dated occurrence and primary rubrics

On 25 October 2026, `calendar-rubrics day --calendar roman-1962 --date 2026-11-01 --json` returned Sunday, All Saints as winner, and `pentecost-23` as privileged commemoration. Its anchors are Easter 5 April, Pentecost 24 May, and next Advent 29 November 2026. The nominal twenty-third slot is 23 weeks after Pentecost, before the resumed Sundays; occurrence is applied after that slot assignment. The computation is a finding aid.

The dated institutional [FSSPX Ordo for 1 November 2026](https://ordo.fsspx.org/day/2026-11-01?lang=en), inspected independently on 25 October 2026, identifies Sunday, All Saints, white, first class, and commemoration of XXIII Sunday after Pentecost. The default feast view also places the Sunday prayer after each feast oration. This is the issuing institute's dated Ordo witness, agreeing with the universal-book result; it does not establish a diocesan or parish calendar or confer present canonical authorization. The query selecting `celebration=114` instead displays the commemorated Sunday's full Mass and must not control the feast inventory. A whole HTML retrieval was acquired and hashed: SHA-256 `a7d8fbbf6c4569e91dee98ea2c3c4f8714220884d28dfa47f866d5eadbdacc40`. No Ordo wording is adopted as a transcription authority or published payload.

The controlling CMAA facsimile is `artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf`, [public source](https://media.churchmusicassociation.org/pdf/missale62.pdf), SHA-256 `648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a`, 82,815,941 bytes, 1,088 PDF pages. The exact held whole-file hash was recomputed on 25 October 2026. Page references below use **one-based PDF artifact pages**, independently of the book's printed pagination.

Independent image inspection on 25 October 2026 reached PDF pp. 15–17, 31–33, 333–334, 497–498 and 783–785. The images establish these appointment decisions:

- RG 91, precedence rows 11 and 15, printed p. xvii / PDF 15: a universal first-class feast precedes a second-class Sunday. RG 93 distinguishes the resulting impediment from the preceding rank decision.
- RG 106, 108, 109(a), 111(a), printed p. xviii / PDF 16: these commemoration rules apply to Mass; the Sunday commemoration is privileged, made in all Masses, and the first-class day admits one privileged commemoration. RG 113, printed p. xix / PDF 17, orders the de Tempore commemoration first. This feast is not one of the Lord's feasts to which the RG 112(b) exclusion applies.
- RG 120(d), printed p. xix / PDF 17, explicitly assigns white to All Saints.
- The feast prints `Credo` after its Gospel, printed p. 703 / PDF 784. RGMR 475(a–b), printed p. xxxiii / PDF 31, also requires it for Sundays whose Office yields and for first-class feasts.
- RGMR 482–483, 494(b), 498, printed p. xxxiv / PDF 32: the **Common Preface** follows by application of the rules. The feast has no proper Preface and is not a second-class Sunday requiring Trinity de Tempore. A commemoration introduces no proper Preface. The Trinity directive printed in the standalone Sunday's Mass, p. 417 / PDF 498, therefore supplies no Preface for this celebration.
- RGMR 480, same page, appoints as many Secrets, in the same order, as the opening orations. RGMR 505, printed p. xxxv / PDF 33, does the same for Postcommunions. The dated Ordo independently confirms all three commemoration-prayer positions.

These inspections establish appointment and boundaries, not a new all-word, dual-resolution Latin/English collation. Existing library verification events retain their own dates and scope. Completion of publication-text verification remains assigned to research.

## Complete ordered proper inventory

Every row is **required** for the resolved General Calendar celebration on 1 November 2026; none is an optional branch. The ten feast propers have marginal numbers 3974–3983. The three commemoration orations are additional texts, and the selected common Preface is included explicitly. Short incipits identify received texts; this record composes no missing text.

| Stable key | Liturgical place and appointment | Exact controlling locus and boundary |
| --- | --- | --- |
| `introit` | Entrance: *Gaudeamus omnes in Domino*; composed antiphon, Ps. 32:1 (modern 33:1), doxology cue | Printed p. 702 / PDF 783, left, no. 3974. The composed antiphon ends at *Filium Dei*; the Psalm citation applies only to the following verse. Literal `Gloria Patri` cue, not a written-out doxology. |
| `collect` | Principal opening oration: *Omnipotens sempiterne Deus* | P. 702 / PDF 783, left, no. 3975; conclusion printed `Per Dominum`. |
| `commemoration-collect` | Second opening oration, XXIII Sunday: *Absolve, quaesumus, Domine* | P. 416 / PDF 497, right, no. 1720; full printed conclusion begins `Per Dominum nostrum Iesum Christum` and is abbreviated at `in unitate`. |
| `epistle` | Lesson: Apocalypse 7:2–12 | Pp. 702–703 / PDF 783 right–784 left, no. 3976. Liturgical opening *In diebus illis: Ecce ego Ioannes*; includes the full enumeration of twelve tribes; ends with the final *Amen* of v. 12. |
| `gradual` | After the Lesson: Ps. 33:10 and selected 11 (modern 34:10–11) | P. 703 / PDF 784, left, no. 3977; v. 10 and only the *Inquirentes* clause of v. 11. The first clause of v. 11 is unappointed. |
| `alleluia` | After the Gradual: Matthew 11:28 with Alleluia framing | P. 703 / PDF 784, left, no. 3978; single appointed verse; no Tract substitution for this November occurrence. |
| `gospel` | Gospel: Matthew 5:1–12a | P. 703 / PDF 784, left–right, no. 3979; printed citation is 5:1–12. The actual body begins with *In illo tempore*, preserves the Vulgate beatitude order (meek before mourners), and ends at the abundant reward in heaven. The subsequent biblical clause concerning the prophets is omitted. `Credo` follows outside the Gospel body. |
| `offertory` | Offertory chant: Wisdom 3:1, 2 and 3, selected/adapted | P. 703 / PDF 784, right, no. 3980; begins *Iustorum animae*, omits several biblical clauses, reads *tormentum malitiae*, and ends with the feast's Alleluia. It is not the unchanged consecutive Bible verses. |
| `secret` | Principal Secret: *Munera tibi, Domine* | P. 703 / PDF 784, right, no. 3981; printed `Per Dominum`. |
| `commemoration-secret` | Second Secret, XXIII Sunday: *Pro nostrae servitutis augmento* | P. 417 / PDF 498, right, no. 1726; full printed conclusion through the abbreviation `in unitate`. |
| `preface` | Common Preface, before Sanctus and Roman Canon | Appointment by RGMR 482–483, 494(b), 498, p. xxxiv / PDF 32. *Praefatio communis*, solemn setting, printed pp. 252–253 / PDF 333–334, no. 1057; dialogue and body from *Vere dignum* through *supplici confessione dicentes*, followed by the stable Sanctus. Musical setting is not a different prayer. |
| `communion` | Communion chant: Matthew 5:8–10 | P. 703 / PDF 784, right, no. 3982; the three beatitudes on purity of heart, peacemaking and persecution for justice; not the whole Gospel. |
| `postcommunion` | Principal Postcommunion: *Da, quaesumus, Domine* | P. 703 / PDF 784, right, no. 3983; the target prints `Per Dominum nostrum`, differing in cue length from the historical Mame witness. |
| `commemoration-postcommunion` | Second Postcommunion, XXIII Sunday: *Quaesumus, omnipotens Deus* | P. 417 / PDF 498, right, no. 1728; full printed conclusion through the abbreviation `in unitate`. |

The Common Preface's target setting, dialogue, body and transition to the Sanctus were inspected at those exact pages. Its historical-source word collation remains research work. The ten feast texts and three commemoration texts were likewise inspected at their actual target loci.

## Ordinary, branches and exclusions

The stable Order of Mass supplies the preparatory prayers, Kyrie, Gloria, Creed, offering prayers, Sanctus, Roman Canon, Lord's Prayer and communion rites, dismissal, blessing and last Gospel. Their place is acknowledged, without creating new proper-text owners or implying a locally selected chant setting. The feast's Creed is explicit. There is one Roman Canon, with no feast-specific *Communicantes* or *Hanc igitur* appointed here; postconciliar Eucharistic Prayer alternatives have no place in this inventory. RGMR 507–510, printed p. xxxv / PDF 33, give the regular *Ite, missa est*, blessing and Johannine last Gospel for the case resolved here, with no feast-specific replacement or following procession appointed. Research should verify the remaining Ordinary execution cues, including the Gloria rule, from the governing rubrics before stating them in the publication.

No Sequence, blessing, procession text, sacramental appendix, long/short lesson, alternate Gospel, optional proper chant or local Preface is appointed in the complete feast on pp. 702–703. The next page, p. 704 / PDF 785, begins the distinct *Missa votiva de omnibus Sanctis*. Its seasonal Introit, Tract and Paschal substitutions are excluded. The older Mame octave/votive provisions likewise do not become 1962 feast branches. The Sunday contributes its three orations only, not its Lesson, Gospel, chants or Trinity Preface. The following All Souls Masses are a separate celebration. Particular-calendar conditions remain outside the resolved universal-calendar case.

## Research handoff and source plan

The preliminary handoff was read as untrusted leads. Its adopted identity, rank, date, commemoration, Creed and Preface conclusions were checked independently as recorded above; no prior PASS was inherited. All reception suggestions remain unverified for this study until research examines their exact sources. No material from the postconciliar family is imported.

The existing source library was inspected before the sole new whole-page Ordo acquisition. It already holds the target facsimile identity, Mame four-own-text witness/projection, the Sunday oration witnesses/projection, Lasance historical English and the preferred Douay–Rheims/Challoner Bible. [source-plan.md](source-plan.md) names the concrete routes, lawful-text controls, unperformed checks and reusable-source registration work. Research will create `propers/retrieved.txt`, `propers/verified.md`, `research/scope.md`, `research/chronology.toml`, `research/chronology-annotations.tex`, `research/interpretations.md` and the required source bindings/handoff before independent review. No missing text is composed at this stage.
