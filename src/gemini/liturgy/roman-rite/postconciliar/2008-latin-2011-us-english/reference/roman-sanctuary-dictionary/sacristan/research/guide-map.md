# Guide Map — Sacristan Visual Dictionary

- **Leaf:** `gemini/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/reference/roman-sanctuary-dictionary/sacristan`
- **Kind:** `pictorial-dictionary-postconciliar` (`liturgy-reference-v1`)
- **Role:** Use-derived visual dictionary for sacristans projected from the canonical family inventory (`shared/objects/**/*.toml`). Emphasizes authorized preparation, assembly, placement, linen folding, liturgical-book setting, seasonal color changes, and vessel care without unverified conservation advice.

## Section and Plate Order

1. `sections/00-sacristan-key-and-sanctuary.tex` — Sacristy preparation overview, Plate I, monochrome liturgical-color pattern key (US 2011 GIRM 346), Plate II, and sanctuary furnishings preparation.
2. `sections/10-vessels-and-communion.tex` — Plate III and Plate X covering sacred vessels, Communion under both kinds setup, USCCB vessel material norms, pre-consecration pouring rules, and holy oils care.
3. `sections/20-linens-and-books.tex` — Plate IV (folding and care of altar linens) and Plate V (setting Missal ribbons/tabs, Lectionary cycles, Book of the Gospels, and Book of the Chair).
4. `sections/30-service-incense-vesture.tex` — Plate VI, Plate VII, Plate VIII, and Plate IX covering cruets, candles, charcoal/incense preparation, and laying out vestments for ordained, instituted, and server ministers.
5. `sections/90-apparatus.tex` — Sacristy Preparation Checklist by Liturgical Moment, Latin pronunciation, indexes, keyed source notes, Scope appendix, and References.

## Derivation Contract

Projected deterministically by `shared/generate_editions.py` from `audience_text.sacristan`, `identification.placement_and_use`, and `ministers_and_handling` fields of the single canonical TOML corpus; verified byte-for-byte with `--check`.
