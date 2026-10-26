# All Saints — resolved national-calendar instance

Context resolution: 2026-10-25. This record identifies the study object and
branches; it does not certify completed research or a local enactment.

| Field | Resolution |
| --- | --- |
| Provider / calendar family | `gpt` / `postconciliar` |
| Governing edition-locale | `roman-missal-third-edition-en-us-2011` |
| Territory | Dioceses of the United States of America; national calendar only |
| Parent / formula key | `PC-R07` / `PC-R07-ABC` |
| Full publication slug | `pc-r07-all-saints-abc` |
| Celebration / rank / color | All Saints / Solemnity / white |
| Date / temporal setting | Sunday 2026-11-01 / Ordinary Time week 31 displaced by All Saints |
| Coverage / appointed reading cycle | Annual common `ABC` coverage / `not applicable` |
| Surrounding Sunday cycle | A, liturgical interval 2025-11-30 through 2026-11-28 |
| Weekday cycle | `not applicable` to this Sunday celebration |
| Lectionary | U.S. second typical edition, Volume I, n. 667; OLM 1981 n. 667 |
| Form / ritual context | Mass of the Solemnity; no separate appointed Vigil; no special ritual substitution established |
| Publication mode | `rights-limited`; public-domain study Scripture is not the approved proclaimed English |
| Stable authority | `guidance/liturgy/postconciliar-propers-registry.md` |
| Edition authority | `propers/registry/README.md`, `formula-dispositions.md`, `occurrences-2026.md` in this edition tree |
| Canonical Missal owner | [All Saints shared owner](../../shared/formularies/pc-r07-all-saints/propers/verified.md) |

Governing Missal and calendar witnesses, source limits and dated checks are
identified in [context](../research/context.md), [composition audit](../propers/verified.md)
and the canonical owner. The complete ordered element list is the
[composition audit's inventory](../propers/verified.md#ordered-inventory).
Its keys remain stable in research, components and reader-facing resolution.

## Ordered element keys for the chronology adapter

These are the composition audit's complete units in liturgical order. The
source owner named there controls each Missal unit; this key list contains
no second Missal collation.

| Order | Key | Element |
| --- | --- | --- |
| 1 | entrance-antiphon | Entrance antiphon |
| 2 | collect | Collect |
| 3 | first-reading | First Reading |
| 4 | responsorial-psalm | Responsorial Psalm |
| 5 | second-reading | Second Reading |
| 6 | gospel-acclamation | Gospel acclamation |
| 7 | gospel | Gospel |
| 8 | prayer-over-offerings | Prayer over the Offerings |
| 9 | proper-preface | Proper Preface |
| 10 | communion-antiphon | Communion antiphon |
| 11 | prayer-after-communion | Prayer after Communion |
| 12 | solemn-blessing | Optional solemn blessing |

## Branch universe

| Semantic branch ID | Authority and trigger | Status | Units affected | Resolution |
| --- | --- | --- | --- | --- |
| `annual-lectionary-667` | U.S. daily readings for 2026-11-01; OLM n. 667 | `required` | `first-reading`, `responsorial-psalm`, `second-reading`, `gospel-acclamation`, `gospel` | One annual appointment set; no closed alternative or short form found in these sources. The acclamation is the appointed sung verse. |
| `missal-antiphons` | U.S. GIRM 48, 87; this proper | `appointed alternative` | `entrance-antiphon`, `communion-antiphon` | The study treats the appointed Missal antiphons; no actual parish singing choice is claimed. |
| `other-lawful-chants` | U.S. GIRM 48, 61–62, 74, 87 | `permitted` | Entrance, psalm/acclamation and Communion; Preparation chant if chosen | Open classes remain unresolved; no specific Graduale or other approved chant is invented or added to the closed inventory. GIRM 63's one-reading arrangements do not describe this three-reading solemnity. |
| `preface-with-ep-i` | Proper Preface; U.S. GIRM 365(a) | `permitted` | `proper-preface`; Eucharistic Prayer selection | Roman Canon with the day's proper Preface is an eligible path; no local selection. |
| `preface-with-ep-iii` | Proper Preface; U.S. GIRM 365(c) | `permitted` | `proper-preface`; Eucharistic Prayer selection | EP III permits the proper Preface; no local selection. |
| `preface-with-ep-ii` | U.S. GIRM 365(b), qualifying use with another Preface | `conditional` | `proper-preface`; Eucharistic Prayer selection | Retain the All Saints Preface; do not substitute EP II's own Preface as another All Saints appointment. No local choice or special circumstance is established. |
| `ep-iv` | U.S. GIRM 365(d), invariable Preface | `not applicable` | Eucharistic Prayer selection | The celebration has its own proper Preface. A Sunday civil date does not turn it into the displaced Ordinary Time Sunday. |
| `all-saints-solemn-blessing` | Proper's referred numbered blessing, documented at the owner | `permitted` | `solemn-blessing` | Treat as a named optional concluding text, without asserting selection; the ordinary simple blessing remains the general concluding form. |
| `gloria-and-creed` | Proper's rubrics, documented at the owner | `required` | Ordinary of Mass | Both used; their Ordinary texts do not become new proper elements. |
| `sunday-sprinkling` | U.S. GIRM 51, occasional Sunday use | `permitted` | Introductory Rites | General possibility in place of the Penitential Act; no actual selection or blessing formula established. |
| `sequence` | No Sequence appointed in n. 667 or inspected proper | `not applicable` | Sequence | No text added. |
| `proper-ep-insert` | No festival-specific insert identified in inspected proper | `not applicable` | Eucharistic Prayer insert | No invented All Saints insert. The general Order of Mass audit remains a research check. |
| `local-ritual-overlay` | Would require competent particular authority and a documented enactment | `conditional` | Any affected unit | Unresolved beyond this national-calendar scope; no Reconciliation, Various Needs, initiation or other ritual form is silently selected. |

The Lectionary branches are closed at the stated loci. General lawful chant
and Ordinary selection classes are open, not an unbounded list of invented
formula alternatives. If research establishes a further governing branch, it
must correct this record explicitly before authoring.
