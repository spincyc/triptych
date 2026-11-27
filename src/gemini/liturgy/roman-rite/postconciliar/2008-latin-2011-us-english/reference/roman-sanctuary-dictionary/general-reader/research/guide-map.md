# Guide Map — General Reader Visual Dictionary

- **Leaf:** `gemini/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/reference/roman-sanctuary-dictionary/general-reader`
- **Kind:** `pictorial-dictionary-postconciliar` (`liturgy-reference-v1`)
- **Role:** Concise use-derived illustrated survey for the general Catholic reader projected from the canonical family inventory (`shared/objects/**/*.toml`). Emphasizes visual identity, liturgical purpose, brief sourced symbolism, and direct continuity or change relative to the 1962 Roman Missal.

## Section and Plate Order

1. `sections/00-sanctuary-and-furnishings.tex` — Reader overview, Plate I, monochrome liturgical-color key, Plate II, and concise furnishings entries.
2. `sections/10-vessels-and-linens.tex` — Plate III (sacred vessels) and Plate IV (altar and vessel linens).
3. `sections/20-books-service-incense.tex` — Plate V (liturgical books), Plate VI (service equipment), and Plate VII (incense).
4. `sections/30-vesture-and-communion.tex` — Plate VIII (ordained vesture), Plate IX (choir and solemn vesture), and Plate X (Communion under both kinds and sacramental vessels).
5. `sections/40-postconciliar-continuity.tex` — Concise 1962 counterpart summary table and separated chronological overview of historically superseded postconciliar forms (1967–2011).
6. `sections/90-apparatus.tex` — Latin pronunciation, English–Latin and Latin–English indexes, keyed source notes, Scope appendix, and References.

## Derivation Contract

Projected deterministically by `shared/generate_editions.py` from `audience_text.general_reader`, `symbolism`, and `counterpart_1962` fields of the single canonical TOML corpus; verified byte-for-byte with `--check`.
