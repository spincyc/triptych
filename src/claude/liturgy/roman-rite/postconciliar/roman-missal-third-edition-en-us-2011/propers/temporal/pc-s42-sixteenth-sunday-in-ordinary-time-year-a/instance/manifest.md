# PC-S40-A — Liturgical Instance Manifest

This is the authoritative identity and resolution record for the publication leaf `pc-s42-sixteenth-sunday-in-ordinary-time-year-a`.

## Identity

| Field | Resolution |
| --- | --- |
| Stable registry | [`guidance/liturgy/postconciliar-propers-registry.md`](../../../../../../../../../../guidance/liturgy/postconciliar-propers-registry.md), adopted without modification |
| Edition-locale registry | [`propers/registry/`](../../../registry/README.md) of this edition-locale. This leaf's disposition is recorded in [formula dispositions](../../../registry/formula-dispositions.md) and its date in the [2026 occurrence record](../../../registry/occurrences-2026.md). It asserts no edition-specific delta and adds no key, slug, position, or count; every target not listed in that registry remains unassessed. |
| Permanent parent | `PC-S40` — Sixteenth Sunday in Ordinary Time |
| Formula key | `PC-S40-A` |
| Full publication slug | `pc-s42-sixteenth-sunday-in-ordinary-time-year-a` |
| Canonical formulary owner | [Ordinary Time, Week XVI](../../shared/ordinary-time/weeks/16/propers/verified.md) in this provider tree. Exactly one owner; this leaf does not duplicate protected owner wording. |
| Missal edition | Roman Missal, Third Edition, for Use in the Dioceses of the United States of America; English; confirmed 2010, implemented 2011-11-27. Latin base: *Missale Romanum*, editio typica tertia, reimpressio emendata (2008). |
| Lectionary edition and locator | Lectionary for Mass for Use in the Dioceses of the United States of America, second typical edition; no. 106 |
| Language | English (liturgical); Latin (typical edition, for identity and analysis) |
| Territory | Dioceses of the United States of America |
| Calendars | General Roman Calendar as implemented nationally in the United States. No diocesan, religious, parish, titular, dedication, or patronal calendar was resolved. |
| Rank and precedence | Sunday in Ordinary Time; rank 6 of the Table of Liturgical Days |
| Season and colour | Ordinary Time, Week XVI; green |
| Cycle | Sunday cycle A (the liturgical year that began 2025-11-30). The adjacent ferial Lectionary cycle is II and is independent; it is not derived from the Sunday letter. |
| Psalter week | IV |
| Form | The single Mass form of the day; no Vigil, Night, Dawn, or Day distinction exists for this parent |
| Ritual context | None. No Ritual Mass, Mass for Various Needs, or Votive Mass is treated; none was shown to have been admitted. |
| Occurrence | Sunday, 19 July 2026. The national calendar for 2026 lists no celebration on that date capable of replacing the Sunday, and the Sunday is celebrated. |
| Branch universe | Ten branches, listed with stable IDs in [the leaf composition audit](../propers/verified.md) and reproduced in the guide's liturgical-resolution appendix |
| As-of date | 2026-07-25 |

## Resolved selections

- The complete appointed textual inventory of the Mass, in ritual order, is fixed by the Week XVI Missal formulary and Lectionary 106; it is recorded in the leaf composition audit.
- Both Gospel forms and both Communion antiphons are treated in full as appointed alternatives.
- The Gloria and the Creed are required, the day being a Sunday (*Tempus per annum* rubric 4).
- No Offertory antiphon, proper Preface, or Eucharistic Prayer insert exists for this formulary.

## Unresolved choices

- `entrance-chant-selection`, `communion-chant-selection`, `offertory-chant-selection`: the music actually used, and whether either printed antiphon was used at all.
- `sunday-sprinkling`: whether the blessing and sprinkling of water replaced the Penitential Act at any celebration.
- `gospel-long-form` / `gospel-short-form`: which of the two appointed forms was proclaimed.
- `preface-sunday-ordinary-time` / `eucharistic-prayer-iv-coupled`: the coupled Preface and Eucharistic Prayer selection.
- `communion-antiphon-psalm-111` / `communion-antiphon-revelation-3`: which printed antiphon, if either, was used.

None of these is narrated in the publication as though it had been enacted.

## Dependencies

- The Week XVI formulary owner named above (evidence and structure; not imported into the rendered document).
- `../../../shared/exposition-format.tex` — render dependency. A change to it requires rebuilding this leaf.
- `../../../../../../../../common/preamble.tex` — repository-wide render dependency.

## Record set

`instance/manifest.md` (this file); `propers/verified.md`; `research/scope.md`; `research/source-audit.md`; `research/source-bindings.toml`; `generation-metadata.tex`; `web-edition.toml`; `main.tex` with `sections/`.
