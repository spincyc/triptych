# Guide Map — Comprehensive Adult Reference Edition

- **Leaf:** `gemini/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/reference/roman-sanctuary-dictionary/comprehensive`
- **Kind:** `pictorial-dictionary-postconciliar` (`liturgy-reference-v1`)
- **Role:** Primary authoritative adult-reference illustrated dictionary projected from the canonical inventory at the family owner root (`shared/objects/**/*.toml` and `shared/schema/plates-and-editions.toml`).

## Section and Plate Order

1. `sections/00-key-and-sanctuary.tex` — Opening orientation, Plate I (Full Sanctuary Composition), controlled disposition tag key, and monochrome liturgical-color pattern key (US 2011 GIRM 346).
2. `sections/10-sanctuary-furnishings.tex` — Plate II and seven sanctuary furnishings (`altar`, `ambo`, `presidential-chair`, `credence-table`, `tabernacle`, `sanctuary-lamp`, `baptismal-font`).
3. `sections/20-sacred-vessels.tex` — Plate III and seven sacred and Communion vessels (`chalice`, `paten`, `ciborium`, `pyx`, `communion-cup`, `cruets`, `flagon`).
4. `sections/30-altar-linens.tex` — Plate IV and five altar and vessel linens (`altar-cloth`, `corporal`, `purificator`, `pall`, `lavabo-towel`).
5. `sections/40-liturgical-books.tex` — Plate V and five liturgical books and stands (`roman-missal`, `lectionary`, `book-of-the-gospels`, `book-of-the-chair`, `missal-stand`).
6. `sections/50-service-and-incense.tex` — Plate VI (processional and service equipment) and Plate VII (incense equipment).
7. `sections/60-vesture-and-ministry.tex` — Ministry distinctions table, Plate VIII (ordained vesture), and Plate IX (choir dress and solemn ceremonial vesture).
8. `sections/70-communion-and-adjacent.tex` — Plate X (Communion under both kinds arrangement, holy oils stocks, and baptismal font context).
9. `sections/80-superseded-postconciliar.tex` — Separated chronological section covering three historically superseded postconciliar forms (1967–2011).
10. `sections/90-pronunciation-and-indexes.tex` — Appendix A (Latin pronunciation) and Appendix B (English–Latin and Latin–English indexes).
11. `sections/95-chronology-and-notes.tex` — Appendix C (Chronological postconciliar change table, 1963–2021) and Appendix D (Keyed source notes).
12. `sections/98-scope-and-references.tex` — Appendix E (Scope, Edition, and Qualifications) and References.

## Derivation Contract

All section TeX files are generated deterministically by `shared/generate_editions.py` and verified byte-for-byte with `--check`. No independent prose edits are maintained inside `comprehensive/sections/`.
