# `PC-S51-A` — Target Composition Audit (Claude edition)

**Formula:** `PC-S51-A`, Twenty-fifth Sunday in Ordinary Time, Year A
**Canonical Missal owner:** [Ordinary Time Week XXV](../../shared/ordinary-time/weeks/25/propers/verified.md)
**Identity record:** [`instance/manifest.md`](../instance/manifest.md)
**Collated:** 2026-09-19
**Provider:** Anthropic Claude

This record verifies the composition of the target: which units make up this
Mass, in what order, with what boundaries, branches and rights dispositions.
The Missal formulary's witnesses, locators, incipits and variation check belong
to the owner and are not restated. The Lectionary witnesses, with their hashes
and page locators, were collated at context resolution and are recorded in
[`research/context.md`](../research/context.md); this record states what the
research stage itself re-checked and what it did not.

## What this stage checked, and what it relied on

| Matter | Basis |
| --- | --- |
| Sunday, cycle, occurrence, Lectionary no. 133 and every reading boundary | Collated at context resolution (`research/context.md`). Re-collated on the research re-entry: the USCCB 2026 calendar at printed pp. 5 and 38, the dated readings page, and *Ordo lectionum Missae* 1981 no. 133 were each re-read from bytes matched to their recorded hashes, and every figure agrees. All three are bound in `research/source-bindings.toml` |
| Missal elements, order, *Vel:* structure, absent units | The Week XXV owner. Re-read on the research re-entry in the 2002 Latin at physical PDF pp. 288–289 and in the ICEL excerpt at printed p. 79; nothing differs from the owner's table |
| Study-text boundaries | Re-read in this stage in the tracked Douay–Rheims (Challoner) and Clementine Vulgate at Isaiah 55, Psalm 144, Psalm 118:1–8, Psalm 36:37–40, Philippians 1:1–2:4, Acts 16:9–15 and 40, Matthew 19:16–20:19 and John 9:39–10:30 |
| Citation encoding | Every citation below was passed through `tools/citations parse` and returned `ok` with its partial-verse letters intact |

## Ordered textual units

| Order | Key | Unit and boundary | Status | Rights disposition |
| --- | --- | --- | --- | --- |
| 1 | `entrance-antiphon` | *Salus populi ego sum*. Composed first-person oracle; the Missal prints no locator | required | Latin incipit and original description only. No Scripture translation stands for it |
| 2 | `collect` | *Deus, qui sacrae legis omnia constituta*; long conclusion | required | Latin incipit and original description only |
| 3 | `first-reading` | Isaiah 55:6–9, whole verses | required | Douay–Rheims (Challoner), public domain, labelled as study text |
| 4 | `responsorial-psalm` | Psalm 145 (144):2–3, 8–9, 17–18; response from v. 18a | required | Douay–Rheims at Psalm 144; the response shown as the first half of v. 18 only |
| 5 | `second-reading` | Philippians 1:20c–24, 27a | required | Douay–Rheims; v. 20 entered at its third clause, vv. 25–26 omitted, v. 27 ended after its opening command, each shown as partial |
| 6 | `gospel-acclamation` | Alleluia verse `Cf.` Acts 16:14b | required | Acts 16:14 in Douay–Rheims as an identified basis, beside a description of the adaptation. No English is composed for the verse |
| 7 | `gospel` | Matthew 20:1–16a | required | Douay–Rheims; the second sentence of v. 16 marked as not appointed |
| 8 | `prayer-over-offerings` | *Munera, quaesumus, Domine, tuae plebis*; short conclusion | required | Latin incipit and original description only |
| 9a | `communion-antiphon-a` | Psalm 119 (118):4–5 | appointed alternative | Douay–Rheims at Psalm 118:4–5 |
| 9b | `communion-antiphon-b` | John 10:14, with the Missal's *dicit Dominus* and supplied *oves* | appointed alternative | Douay–Rheims at John 10:14; the Missal's two additions described, not translated |
| 10 | `prayer-after-communion` | *Quos tuis, Domine, reficis sacramentis*; short conclusion | required | Latin incipit and original description only |

No Offertory antiphon, Sequence, proper Preface, proper Eucharistic Prayer
insert, prayer over the people or solemn blessing is appointed. The approved
United States English of the Missal and of the Lectionary is reproduced nowhere
in this leaf.

## Findings of this stage

1. **Matthew 20:16.** The tracked Clementine Vulgate and Douay–Rheims both
   print a second sentence in v. 16, on the many called and the few chosen. The
   *Nova Vulgata* as published by the Holy See prints v. 16 with the first
   sentence only (page retrieved 19 September 2026, 130,490 bytes, SHA-256
   `f2dd3344f740087470a623bf341f7d4d4b46b5dbcc9c892c023e7be7836ab108`; not
   registered, not retained). Chrysostom's lemma (*Hom. in Matt.* 64.3) and
   Gregory's (*Hom. in Evang.* 19) both carry the second sentence and both
   expound it. **Not established:** which Greek witnesses carry or lack the
   sentence. No critical apparatus was opened in this stage, and no manuscript
   is named. **Open observation:** if the Lectionary's base text has one
   sentence in v. 16, the designation `16a` is not explained by it; whether the
   *Ordo*'s lettering follows the *Nova Vulgata* or an older division was not
   determined. The appointment itself is not in doubt: all three witnesses in
   `research/context.md` give `20:1-16a`.
2. **Entrance antiphon basis.** The ICEL excerpt's compiler names Psalm 36
   (37):39–40. Against the Clementine text that psalm shares *salus* and
   *tribulationis* with the antiphon and no clause. Closer verbal contacts are
   Psalm 34:3 (*Salus tua ego sum*), Psalm 33:18 (*clamaverunt … exaudivit … ex
   omnibus tribulationibus*) and Psalm 90:15 (*clamabit ad me, et ego exaudiam
   eum … in tribulatione*). None is a quotation and the Missal identifies none.
   The antiphon is therefore entered in `research/chronology-inputs.toml` as a
   composed element with no citation, and receives no date.
3. **Acclamation.** Acts 16:14 is third-person narrative about Lydia at
   Philippi. `Cf.` is retained and the relationship is `adaptation`.
4. **Communion antiphon A numbering.** Hebrew Psalm 119:4–5, Vulgate 118:4–5,
   as the owner's finding 2 establishes. The finding-aid index's `Psalm
   118:4-5` under a Hebrew-numbered file is not followed.

## Relationship classes

| Relation | Class | Authority |
| --- | --- | --- |
| First reading ↔ Gospel | `officially correlated` | *Praenotanda* 1981, nos. 105–107. No. 106 says the relation between the readings of a Mass is shown by the tituli set over them, and at no. 133 (printed p. 72) the *Ordo* heads the first reading with Isaiah 55:8 on God's thoughts not being ours and the Gospel with Matthew 20:15, the householder's question whether the eye is evil because he is good |
| Second reading, the *Ordo*'s emphasis | `semi-continuous` | At no. 133 the *Ordo* heads it *Mihi vivere Christus est* (Philippians 1:21). The three tituli are edition-controlled evidence of what the Lectionary singles out in each reading and of the one official correlation; they are not evidence of a whole-formulary design |
| Psalm → first reading | `responsorial` | GIRM 61 |
| Alleluia verse → Gospel | `acclamatory` | GIRM 62 |
| Second reading; Gospel | each `semi-continuous`; Philippians opens its four-Sunday course here | *Praenotanda* 1981, *Tabella II* |
| Acts 16:14 (Lydia of Philippi) ↔ Philippians | `textual observation` | The texts themselves; no source consulted states a design |
| Missal antiphons and orations ↔ Year A readings | `source-grounded synthesis` or `editorial or AI proposal`, labelled case by case in `research/interpretations.md` | The week's Missal texts serve all three cycles |

## Branches

The ten branch IDs of `instance/manifest.md` apply unchanged. Statuses,
authorities and resolutions are those tabulated in `research/context.md`; no
selection was supplied and none is inferred.

## Outstanding

Greek textual evidence for Matthew 20:16; the basis of the *Ordo*'s `16a`
lettering; whether the United States Lectionary admits another acclamation
verse from a common set; the printed United States Lectionary volume, which
was not inspected; independent review of this audit.
