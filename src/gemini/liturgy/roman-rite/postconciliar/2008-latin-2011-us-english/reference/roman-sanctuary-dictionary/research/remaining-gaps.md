# Remaining Gaps and Bounded-Alpha Completeness Accounting

- **Owner:** `src/gemini/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/reference/roman-sanctuary-dictionary`
- **Declared edition-locale:** `2008-latin-2011-us-english`
- **As-of date:** `2026-11-25`

This record prevents the claim of bounded completeness from outrunning the checked corpus (`guidance/liturgy/postconciliar-pictorial-dictionaries.md` and `guidance/liturgy/postconciliar-illustrated-dictionary-handoff.md`).

## 1. Completed in This Bounded Alpha Corpus

- **40 core current postconciliar sanctuary objects** across seven functional areas (Sanctuary Furnishings [7], Sacred Vessels & Communion Vessels [7], Altar & Vessel Linens [5], Liturgical Books & Stands [5], Service Equipment & Incense [6], Vesture & Ministry Distinctions [9], Adjacent Sacramental Vessels [1: Holy Oils Stocks & Ambry]).
- **3 historically superseded postconciliar forms** (1967–1972 subdeacon's tunicle and maniple; 1970–2004 breakable/porous vessels and post-consecration flagon pouring; 1970/1975 vs. 2002/2008 GIRM sanctuary/altar-cross/tabernacle/chalice-veil clarifications), strictly separated chronologically.
- **10 bespoke monochrome 8-bit grayscale graphite plates** passing all six Phase 3 visual hard cases (full sanctuary composition, reflective metal vessels, white linens on white stock, worn priest/deacon vestments, black cassock beside white surplice, and dense comparison plates), normalized to pure white ground with zero embedded lettering.
- **4 coordinated publication leaves** projected deterministically with zero prose drift from one canonical TOML owner: `comprehensive`, `altar-server`, `sacristan`, and `general-reader`.

## 2. Deferred Categories Reserved for Future Expansion

The following domains outlined in the handoff discovery scaffold are intentionally outside this bounded alpha corpus and are **not** claimed as covered:

1. **Episcopal and Pontifical Insignia and Furnishings:** Mitre (*mitra*), crosier (*baculus pastoralis*), pectoral cross (*crux pectoralis*), episcopal ring (*anulus*), zucchetto (*pileolus*), cathedra, gremiale, pontifical dalmatic beneath chasuble, bugia (if historically noted), vimpa (specifically distinguished from Eucharistic humeral veil), and the dedicated **Episcopal and Major-Ceremony Visual Reference** leaf.
2. **Master of Ceremonies & Trainer Derived Edition:** A fifth use-based leaf emphasizing MC handoffs, concelebration branching, and recovery points remains planned for a future phase once episcopal and Triduum items enter the canonical inventory.
3. **Full Paschal Triduum & Holy Week Apparatus:** Paschal candle (*cereus paschalis*) and stand, Easter fire brazier and wax grains/stylus, Holy Thursday altar-of-reposition appointments, *crotalus* (wooden clapper), Good Friday veiled adoration cross, and Palm Sunday palms/processional appointments.
4. **Funerals and Masses for the Dead:** Funeral pall (*palla funebris* covering the coffin), paschal candle placement beside the casket, and historical comparison with the catafalque.
5. **Expanded Eucharistic Devotion Outside Mass:** Monstrance (*ostensorium*), luna/lunette (*lunula*), custode (*custodia*), baldachin/canopy (*baldachinum*) and *ombrellino* for Corpus Christi processions, and thabor/exposition throne.
6. **Additional Customary / Optional Mass Accessories:** Chalice veil (*velum calicis*, praised in GIRM 118, noted in our historical clarification and chalice entry without its own separate plate specimen), burse (*bursa*, customary), Communion-plate (*patina pro Communione fidelium*, discussed inside the Paten entry without a separate isolated drawing), altar chimes/gong, processional banners, and choir/chant books (*Graduale Romanum*, *Graduale Simplex*).
7. **Other Territorial Edition-Locales:** Dispositions for England and Wales, Canada, Australia, Ireland, and non-English conferences are not yet populated; the TOML schema keeps universal identity separated from `edition_disposition` so additional locales can layer onto the same canonical objects later.

## 3. Source-Library Registration Gaps (External Primary Texts)

Because this authoring lane has no write authority over shared `src/sources/works/`, several primary postconciliar acts verified externally via official Vatican (`vatican.va`) and USCCB (`usccb.org`) witnesses are documented in `research/source-audit.md` as externally verified official controls rather than locally registered `src/sources/` passage TOMLs:

- *Redemptionis Sacramentum* (25 March 2004) — AAS 96 container exists in `src/sources/`, but no standalone work record yet.
- *Caeremoniale Episcoporum* (14 September 1984 *editio typica*) — `src/sources/works/catholic-church/caeremoniale-episcoporum` currently holds only the preconciliar 1948 edition.
- USCCB *Norms for the Distribution and Reception of Holy Communion under Both Kinds* (2002/2011) and *Excerpts from the Roman Missal* (2018).
- *Inter Oecumenici* (1964), *Tres abhinc annos* (1967), *Ordo benedicendi oleum* (1970), *Immensae caritatis* (1973), and *De sacra communione et de cultu mysterii eucharistici extra Missam* (1973).
- Individual passage TOMLs for GIRM Chapters III–VI and CIC 1983 cann. 847, 858, 910, 938–940, and 1235–1239.
- Complete scanned artifact for the 2008 Latin *reimpressio emendata* (currently verified via the locally registered *Notitiae* 44 [2008] nos. 503–504 notice and variations list).

## 4. Infrastructure Follow-Ups Identified Outside This Lane

Two repository-wide tooling enhancements identified during production are noted for shared infrastructure follow-up outside this leaf's write scope:
- Extending `scripts/_native_print_artwork.py` and `scripts/_native_print_bundles.py` if positive dictionary-manifest artwork checking is desired for `pictorial-dictionary-postconciliar` beyond active literal `\includegraphics` discovery.
- Adding a dedicated `pictorial-dictionary-postconciliar` content validator hook under `scripts/document_schema_checks/liturgy.py` alongside the existing 1962 `pictorial-dictionary` validator.
