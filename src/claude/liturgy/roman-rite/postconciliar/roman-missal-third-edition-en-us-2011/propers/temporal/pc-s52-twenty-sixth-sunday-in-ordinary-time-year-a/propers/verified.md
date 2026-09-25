# `PC-S52-A` — Target Composition Audit (Claude edition)

**Formula:** `PC-S52-A`, Twenty-sixth Sunday in Ordinary Time, Year A
**Canonical Missal owner:** [Ordinary Time Week XXVI](../../shared/ordinary-time/weeks/26/propers/verified.md)
**Identity record:** [`instance/manifest.md`](../instance/manifest.md)
**Collated:** 2026-09-24
**Provider:** Anthropic Claude

This record verifies the composition of the target: which units make up this
Mass, in what order, with what boundaries, branches and rights dispositions.
The Missal formulary's witnesses, locators, incipits and variation check belong
to the owner and are not restated. The Lectionary witnesses, with their hashes
and page locators, were collated at context resolution and are recorded in
[`research/context.md`](../research/context.md); this record states what the
research stage itself re-checked.

## What this stage checked, and what it relied on

| Matter | Basis |
| --- | --- |
| Sunday, cycle, occurrence, Lectionary no. 136 and every reading boundary | Re-collated at the research stage from bytes fetched whole over verified TLS and matched to their registered hashes: the USCCB 2026 calendar at printed pp. 5 and 39 (artifact pp. 7 and 41) and its Spanish title list at artifact p. 58; the dated readings page for 27 September 2026, byte-identical to the context stage's copy; and *Ordo lectionum Missae* 1981 no. 136 on a page image of printed p. 74 (artifact p. 128), with *Praenotanda* nos. 80 and 105–107 and *Tabella II*. Every figure agrees with `research/context.md`. All are bound in `research/source-bindings.toml` |
| Missal elements, order, *Vel:* structure, absent units, conclusions | The Week XXVI owner. Re-read at the research stage in the 2002 Latin at physical PDF pp. 289–290 and in the ICEL excerpt at printed p. 79; nothing differs from the owner's table. The owner's own additions of this date record what else was read |
| Precedence and the omitted memorial | Re-read in the 2002 artifact: the table of liturgical days, places 6 and 10, and no. 60 of the *Normae universales* (pp. 70–71), and 27 September in the *Calendarium Romanum generale* (p. 79) |
| Chant and branch rubrics | GIRM nos. 48, 51, 53, 61–64, 68, 74, 87 and 363–365, read in the United States English chapter pages fetched on 2026-09-24 and registered as their own dated states; the 2002 artifact's solemn blessings and prayers over the people, usable at the priest's discretion (artifact pp. 370 and 379), and the 2008 variation list's added dismissal formulas (journal p. 372) |
| Study-text boundaries | Re-read in this stage in the tracked Douay–Rheims (Challoner) and Clementine Vulgate at Ezekiel 18; Psalm 24 whole; Philippians 1:27–2:18; John 10:22–30; Matthew 21:23–46; Daniel 3:24–45; Psalm 118:49–56; 1 John 3:11–24; and in the tracked King James Version, for Hebrew numbering, at Daniel 3 (thirty verses, with no Prayer of Azarias) and Psalm 25:1–10 |
| Citation encoding | Every citation below was passed through `tools/citations parse` and returned its book, chapter and verse ranges with partial-verse letters intact |

## Ordered textual units

| Order | Key | Unit and boundary | Status | Rights disposition |
| --- | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | *Omnia, quae fecisti nobis*. A composite adaptation of Daniel 3:31, 29, 30, 43, 42 (Vulgate numbering of the Greek addition, the Prayer of Azariah), printed without `Cf.` | required | Latin incipit and original description only. The five Douay–Rheims verses may stand beside it as its identified scriptural source, labelled as such and with the Missal's departures stated; no English is composed for the antiphon |
| 2 | `collect` | *Deus, qui omnipotentiam tuam*; long conclusion | required | Latin incipit and original description only |
| 3 | `first-reading` | Ezekiel 18:25–28, whole verses | required | Douay–Rheims (Challoner), public domain, labelled as study text |
| 4 | `responsorial-psalm` | Psalm 25 (24):4–5, 6–7, 8–9; response from v. 6a | required | Douay–Rheims at Psalm 24. Verse 4 is shown from its second colon, the first (on the confusion of the wicked) marked as context; the response is shown as the first half of v. 6 only; finding 2 governs verse 5 |
| 5a | `second-reading-long` | Philippians 2:1–11 | appointed alternative | Douay–Rheims; shown as its own form |
| 5b | `second-reading-short` | Philippians 2:1–5 | appointed alternative | Douay–Rheims; shown as its own form, never merged with 5a |
| 6 | `gospel-acclamation` | Alleluia verse, John 10:27, with an added speaker formula | required | John 10:27 in Douay–Rheims as its identified text, with the added formula described and not translated; no English is composed for it |
| 7 | `gospel` | Matthew 21:28–32 | required | Douay–Rheims |
| 8 | `prayer-over-offerings` | *Concede nobis, misericors Deus*; short conclusion | required | Latin incipit and original description only |
| 9a | `communion-antiphon-a` | `Cf.` Psalm 119 (118):49–50 | appointed alternative | Douay–Rheims at Psalm 118:49–50 beside a description of the Missal's departures (finding 4); no English is composed for the antiphon |
| 9b | `communion-antiphon-b` | 1 John 3:16 | appointed alternative | Douay–Rheims at 1 John 3:16 |
| 10 | `prayer-after-communion` | *Sit nobis, Domine, reparatio mentis et corporis*; concludes *Qui vivit et regnat* | required | Latin incipit and original description only |

No Offertory antiphon, Sequence, proper Preface, proper Eucharistic Prayer
insert, prayer over the people or solemn blessing is appointed. The approved
United States English of the Missal and of the Lectionary is reproduced nowhere
in this leaf.

## Findings of this stage

1. **Matthew 21:29–31: the order of the sons and the answer.** The texts this
   Lectionary rests on agree: the *Ordo*'s titulus (*Paenitentia motus abiit*)
   names the son who repented and went; the *Nova Vulgata* as published by the
   Holy See (page retrieved 2026-09-24, 130,490 bytes, SHA-256
   `f2dd3344f740087470a623bf341f7d4d4b46b5dbcc9c892c023e7be7836ab108`,
   byte-identical to the state another leaf recorded on 2026-09-19; not
   registered, not retained) has the first son refuse and then go, the second
   promise and not go, and the answer *Primus*, with the present *praecedunt*
   that the titulus also has; the Clementine and the Douay–Rheims have the same
   order and answer, with the future *praecedent*. The United States
   Lectionary's own wording has them too, in the one edition-identified witness
   to it that this leaf seals: the dated USCCB readings page for 27 September,
   in the state fetched at the research re-entry of 24 September and
   registered as its own artifact (passage `gospel-order-and-answer`). There
   the father goes first to the son who refuses and afterward goes, then to
   the other, who assents and does not go, and the hearers answer by naming
   the first. The page is described here, not transcribed, and the printed
   volume was not inspected. **The tradition is not
   uniform.** The SBL Greek New Testament's apparatus
   (`artifact.society-of-biblical-literature.sbl-greek-new-testament.holmes-v1.2-2023.matt-app-927dbf27`,
   fetched whole and hash-matched) records that Westcott–Hort print the
   reversed order (the first son says he goes and does not; the second refuses
   and repents) and, with Tregelles, the answer ὁ ὕστερος, "the latter", where
   NA28, the Robinson–Pierpont Byzantine text and the SBL edition print the
   Lectionary's order and ὁ πρῶτος. In Latin, Jerome (*Comm. in Matt.* III,
   Migne PL 26, 1845, col. 156, page image) quotes the answer as *Novissimus*,
   adds that "in veris exemplaribus" it is not *novissimum* but *primum*, and
   gives an interpretation for either reading; Hilary's commentary (PL 9, 1844,
   cols. 1039–1041, page image) works with the order of the Lectionary and an
   answer naming the younger son, and the Maurist editor's note says that
   reading was current in Hilary's and Jerome's time. No manuscript was
   examined and none is named. The appointment is not in doubt, and the study
   text follows the Lectionary's order and answer.
2. **Psalm 25:5, the first strophe.** The *Ordo* cites *Ps 24, 4bc-5*, and the
   dated USCCB page cites Psalm 25:4–5, but the page's first strophe prints no
   line answering to the last colon of verse 5, on waiting for the Lord all the
   day, which the Douay–Rheims and the Clementine carry. Whether the printed
   United States Lectionary omits that colon was not established: no
   edition-identified witness of the printed volume was available. The study
   text shows verse 5 whole with its final colon marked as possibly outside the
   United States strophe, and makes no claim that rests on that colon.
3. **Entrance antiphon.** The owner's finding 1 and its research addition 5
   govern: a composite adaptation of five verses, printed without `Cf.`, whose
   Latin source text is not established. The chronology input therefore
   records Daniel 3:31, 29, 30, 43, 42 in the Missal's printed order as an
   `adaptation` in Vulgate numbering, which is the only numbering that has
   these verses; no Aramaic-numbered Daniel 3 may resolve them.
4. **Communion antiphon A.** Hebrew Psalm 119:49–50, Vulgate 118:49–50, marked
   `Cf.` in both Missal witnesses. The Missal's *Meménto* and added *Dómine*
   depart from the Clementine, and it ends before the verse's last clause; the
   owner's addition 6 records that *Memento* is an older Latin psalter reading.
   The chronology input enters the Missal's printed Vulgate locator with
   `Cf.` as an `adaptation`. The finding-aid index's omission of the `Cf.` is
   not followed.
5. **Acclamation.** The *Ordo* and the dated page both insert a speaker
   formula (*dicit Dominus*; in English the equivalent) into John 10:27, which
   neither the Clementine nor the Douay–Rheims has; no `Cf.` is printed. The
   verse is recorded as `appointed` with the insertion described. Verse 26, on
   those who do not believe because they are not his sheep, immediately
   precedes it.
6. **Incipits.** The *Ordo* prefixes *Haec dicit Dominus* to Ezekiel 18:25 and
   omits the *ergo* of Philippians 2:1. The Gospel's incipit names the chief
   priests and elders of the people, whom the narrative introduces at 21:23.
   These are liturgical incipits, not text of the verses, and the study text
   does not print them as Scripture.

## Relationship classes

| Relation | Class | Authority |
| --- | --- | --- |
| First reading ↔ Gospel | `officially correlated` | *Praenotanda* 1981, nos. 105–107. No. 106 says the relation between the readings of one Mass is shown by the careful choice of the tituli set over them (*Relatio autem inter lectiones eiusdem Missae ostenditur per accuratam selectionem titulorum qui singulis lectionibus praeponuntur*), and at no. 136 the *Ordo* heads the first reading with Ezekiel 18:27, the wicked man who turns and gives his soul life, and the Gospel with Matthew 21:29 and 31, the son who repented and went and the tax collectors and harlots who go before |
| Second reading, the *Ordo*'s emphasis | `semi-continuous` | Heads both forms with *Sentite in vobis quod et in Christo Iesu* (Philippians 2:5), a verse both forms contain. The three tituli are edition-controlled evidence of what the Lectionary singles out in each reading and of the one official correlation; they are not evidence of a whole-formulary design |
| Psalm → first reading | `responsorial` | GIRM 61 |
| Alleluia verse → Gospel | `acclamatory` | GIRM 62 |
| Second reading; Gospel | each `semi-continuous`; this is the second Sunday of the four-Sunday Philippians course (*Tabella II*), and the Gospel's course runs from Matthew 20:1–16a on 20 September to 21:33–43 on 4 October | *Praenotanda* 1981, no. 107 and *Tabella II*; national calendar |
| Missal antiphons and orations ↔ Year A readings | `source-grounded synthesis` or `editorial or AI proposal`, labelled case by case in `research/interpretations.md` | The week's Missal texts serve all three cycles |
| Recurrence of "way", "remember" and "humility" vocabulary across units | `textual observation` | The texts themselves (Douay–Rheims and Clementine); no source consulted states a design |

## Branches

The twelve branch IDs of `instance/manifest.md` apply unchanged. Statuses,
authorities and resolutions are those tabulated in `research/context.md`, whose
authorities were re-read as the first table above states; no selection was
supplied and none is inferred. For `second-reading-short-form`, every claim in
the research records that rests on Philippians 2:6–11 is marked as not holding
for a celebration that uses the shorter form.

## Outstanding

Greek manuscript evidence for Matthew 21:29–31 beyond the editions' apparatus;
whether the printed United States Lectionary omits the final colon of Psalm
25:5; whether the United States Lectionary admits another acclamation verse
from a common set on Sundays in Ordinary Time (GIRM 62 a, read here, says only
that the verses are taken from the Lectionary or the *Graduale*); the printed
United States Lectionary volume, which was not inspected; independent review of
this audit.
