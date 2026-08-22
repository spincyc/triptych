# `PC-S41-A` — Target Composition Audit

**Formula:** `PC-S41-A` · **Occurrence:** Sunday 26 July 2026 · **Lectionary:** no. 109
**Canonical formulary owner:** [Ordinary Time Week XVII](../../shared/ordinary-time/weeks/17/propers/verified.md)
**Identity control:** [instance manifest](../instance/manifest.md)
**Collated:** 2026-07-25 · **Provider:** Anthropic Claude

This record verifies the composition of one target: which textual units belong to it, where their boundaries fall, which branches exist, what was actually checked, and what was not. It does not re-own the Missal formulary, which belongs to the shared Week XVII record.

## Complete ordered textual-unit inventory

| # | Ritual position | Unit | Source and boundary | Verified at |
| ---: | --- | --- | --- | --- |
| 1 | Entrance | Entrance Antiphon | Missal, `Cf.` Ps 67:6–7, 36 | 2002 typical edition, PDF pp. 281–282; official *Antiphonary* p. 75 |
| 2 | Introductory Rites | Penitential Act | No proper text; sprinkling rite may substitute | GIRM and the Missal's Order of Mass |
| 3 | Introductory Rites | Collect | Missal, Week XVII | 2002 typical edition, PDF p. 282 |
| 4 | Liturgy of the Word | First Reading | 1 Kings 3:5, 7–12 | USCCB 2026 national calendar; official occurrence page |
| 5 | Liturgy of the Word | Responsorial Psalm | Ps 119:57, 72, 76–77, 127–128, 129–130; response `Cf.` Ps 119:97a | Same |
| 6 | Liturgy of the Word | Second Reading | Romans 8:28–30 | Same |
| 7 | Liturgy of the Word | Gospel Acclamation | `Cf.` Matthew 11:25 | Official occurrence page |
| 8 | Liturgy of the Word | Gospel | Matthew 13:44–52, or 13:44–46 | USCCB 2026 national calendar, printed as “Mt 13:44-52 or 13:44-46” |
| 9 | Liturgy of the Eucharist | Offertory chant | None supplied by the Missal | 2002 typical edition |
| 10 | Liturgy of the Eucharist | Prayer over the Offerings | Missal, Week XVII | 2002 typical edition, PDF p. 282 |
| 11 | Liturgy of the Eucharist | Preface | None proper; selected under the Ordinary Time rubrics and GIRM 365 | 2002 typical edition; GIRM 365(b), 365(d) |
| 12 | Liturgy of the Eucharist | Eucharistic Prayer | No proper insert; coupled to the Preface decision | GIRM 365 |
| 13 | Communion Rites | Communion Antiphon | Ps 102:2, **or** Matthew 5:7–8 | 2002 typical edition, PDF p. 282; *Antiphonary* p. 75 |
| 14 | Communion Rites | Prayer after Communion | Missal, Week XVII | 2002 typical edition, PDF p. 282 |
| 15 | Concluding Rites | Blessing and dismissal | No proper text | 2002 typical edition |

## Lectionary boundaries actually checked

The official 2026 national calendar prints the day's Lectionary line as `1 Kgs 3:5, 7-12/Rom 8:28-30/Mt 13:44-52 or 13:44-46 (109) Pss I`. The official occurrence page for 26 July 2026 supplies the psalm boundary and response citation and the acclamation source. Three boundary facts follow and are recorded because they change what is proclaimed:

1. **1 Kings 3:6 is inside the span and is not read.** The reading jumps from the offer in v. 5 to Solomon's self-description in v. 7, omitting his recital of God's mercy to David.
2. **The reading stops at v. 12.** Verses 13–14, in which God adds the riches and glory Solomon did not ask for and makes long life conditional, are not proclaimed; neither is the judgment between the two women at 3:16–28.
3. **The psalm is a selection, not a pericope.** Verse 57 is the first verse of the eighth alphabetic stanza (HETH); v. 72 is the last verse of the ninth (TETH); vv. 76–77 stand within the tenth (JOD); vv. 127–128 are the last two of the sixteenth (AIN); vv. 129–130 the first two of the seventeenth (PHE); and the response verse 97a is the first verse of the thirteenth (MEM), whose other verses are not sung. The stanza boundaries were checked verse by verse in a public-domain Douay-Rheims text of Psalm 118.

## Semantic branches

| Branch ID | Authority and trigger | Status | Units affected | Resolution |
| --- | --- | --- | --- | --- |
| `gospel-long-form` | Lectionary no. 109 prints a longer and a shorter Gospel | appointed alternative | Unit 8 | Unresolved; mutually exclusive with the short form |
| `gospel-short-form` | Same | appointed alternative | Unit 8 | Unresolved; ends at 13:46 |
| `communion-antiphon-psalm` | Missal prints Ps 102:2 first | appointed alternative | Unit 13 | Unresolved |
| `communion-antiphon-beatitudes` | Missal prints Mt 5:7–8 under *Vel* | appointed alternative | Unit 13 | Unresolved |
| `sprinkling-rite` | Missal permits the blessing and sprinkling of water on Sundays | ritual substitution | Unit 2 | Unresolved; substitutes its own texts and adds no proper of this formulary |
| `compatible-preface-and-eucharistic-prayer` | Ordinary Time rubrics; GIRM 365(b) | permitted | Units 11–12 | Unresolved; a Sunday Preface with a compatible Eucharistic Prayer |
| `eucharistic-prayer-iv-with-preface` | GIRM 365(d) | conditional | Units 11–12 | Unresolved; if Prayer IV is chosen its own Preface is inseparable and no Sunday Preface is used |
| `entrance-or-communion-chant-substitution` | GIRM 48, 87 | permitted | Units 1, 13 | Unresolved; an approved chant may replace the Missal antiphon |

The omitted Memorial of Saints Joachim and Anne is **not** a branch. It contributes no text, no title, and no option; it is an occurrence result recorded in the manifest.

## Relationship classification

| Relation | Class | Basis |
| --- | --- | --- |
| 1 Kings 3 ↔ Matthew 13 | `officially correlated` | The Lectionary's own Ordinary Time principle of harmonizing the Old Testament reading with the Gospel |
| Psalm 119 ↔ 1 Kings 3 | `responsorial` | The psalm is the assembly's response to the first reading |
| `Cf.` Matthew 11:25 ↔ Gospel | `acclamatory` | Acclamation before the Gospel; an adaptation, not the whole verse |
| Romans 8:28–30 ↔ the rest | `semi-continuous` | Apostolic course in Ordinary Time; not correlated |
| Missal orations ↔ readings | `source-grounded synthesis` | Shared A/B/C texts; no evidence of composition for no. 109 |
| Entrance antiphon ↔ Dedication of a Church | `textual observation` | The same text under the same citation in the same typical edition |
| Collect ↔ pre-conciliar Third Sunday after Pentecost Collect | `documented reception` | Verbatim first half with a rewritten petition; pre-conciliar side from a community transcription |
| Any proposal in the interpretive section | `editorial or AI proposal` | Labelled as such in the guide with one global disclosure |

## Discrepancies and negative checks

- The Missal's Entrance antiphon reads *unanimes in domo*, which agrees with neither the Clementine Vulgate (*unius moris*) nor the *Nova Vulgata* (*desolatos*). Verified in all three; explained as chant-book inheritance, which is **not** collated.
- The 2008 official variation list contains exactly two *Tempus per annum* entries, at printed Missal pp. 457 and 471, and none at Week XVII. Bounded no-listed-change evidence only.
- The Latin text of the *Summa theologiae* (Prima, Prima Secundae, Secunda Secundae, Tertia) contains no citation of Matthew 13:45–46, and Matthew 13:44 appears once, at II-II q. 66 a. 5 ad 2. Bounded search result; the *Supplementum* was not searched.
- *Summa theologiae* II-II q. 83, on prayer, does not cite Solomon's request. Bounded negative result at the most natural systematic locus.
- Romans 8:28–30 is not cited in the Council of Trent's Decree on Justification. Bounded search of the full English decree.
- No text of Augustine's *Ad Simplicianum* I.2 or of his early *Expositio quarundam propositionum* could be opened; both are used only through Augustine's own verbatim self-quotation in *De praedestinatione sanctorum* 7–8.

## Rights disposition for this target

The United States Lectionary text, the Psalm response, and the approved English orations and antiphons are protected and are **not reproduced** in the guide or in these records. Scriptural wording quoted in the guide is public-domain Douay-Rheims, named as such at the point of use, and is expressly not the text proclaimed. The Latin typical edition is likewise protected: only short incipits and the few short phrases on which a stated philological argument turns are retained. No complete oration is reproduced in any language.
