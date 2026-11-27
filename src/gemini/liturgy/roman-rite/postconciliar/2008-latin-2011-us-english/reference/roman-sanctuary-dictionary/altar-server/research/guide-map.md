# Guide Map — Altar Server Visual Dictionary

- **Leaf:** `gemini/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/reference/roman-sanctuary-dictionary/altar-server`
- **Kind:** `pictorial-dictionary-postconciliar` (`liturgy-reference-v1`)
- **Role:** Use-derived visual dictionary for altar servers projected from the canonical family inventory (`shared/objects/**/*.toml`). Covers every sanctuary object a server encounters — including clergy-reserved items the server recognizes without handling — emphasizing location, handoffs, handling boundaries, confusion risks, and immediate safety.

## Section and Plate Order

1. `sections/00-server-key-and-sanctuary.tex` — Server orientation, Plate I (Full Sanctuary Composition), and explicit handling boundary key.
2. `sections/10-sanctuary-and-furnishings.tex` — Plate II and server interaction boundaries for sanctuary furnishings.
3. `sections/20-vessels-and-linens.tex` — Plate III and Plate IV with explicit preparation vs clergy-reserved boundaries for consecrated vessels and linens.
4. `sections/30-books-service-incense.tex` — Plate V, Plate VI, and Plate VII emphasizing carrying, presenting, ringing, and charcoal/fire safety.
5. `sections/40-vesture-and-ministers.tex` — Ministry distinctions table, Plate VIII, Plate IX, and Plate X so servers distinguish bishop, priest, deacon, instituted acolyte/lector, extraordinary minister, and server dress accurately.
6. `sections/90-apparatus.tex` — Quick-Reference Handling Chart, Latin pronunciation, English–Latin and Latin–English indexes, keyed source notes, Scope appendix, and References.

## Derivation Contract

Projected deterministically by `shared/generate_editions.py` from `audience_text.altar_server` and `ministers_and_handling` fields of the single canonical TOML corpus; verified byte-for-byte with `--check`.
