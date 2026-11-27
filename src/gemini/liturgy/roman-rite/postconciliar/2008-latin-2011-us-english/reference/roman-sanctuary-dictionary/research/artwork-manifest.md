# Artwork Manifest and Visual Audit Record

- **Owner:** `src/gemini/liturgy/roman-rite/postconciliar/2008-latin-2011-us-english/reference/roman-sanctuary-dictionary`
- **Asset root:** `shared/artwork/graphite/`
- **As-of date:** 2026-11-25
- **Machine-readable record:** `research/artwork-manifest.toml`

## Visual Contract and Normalization

All ten plates are project-owned monochrome graphite drawings rendered specifically for the postconciliar Roman sanctuary dictionary. Each received raster was normalized deterministically into an 8-bit lossless grayscale PNG (`1200 x 896`, `dpi=300` metadata) with pure white (`255`) perimeter ground (`border_mean = 255.00`, `border_min = 255`) so every unframed drawing merges seamlessly into white US Letter print stock with zero crop boxes, gray halos, or rectangular seams.

No raster contains embedded lettering, abbreviations, numerals, arrows, frames, or color-only coding. All headwords, position keys, scale notices, liturgical-color monochrome pattern keys, and note keys are typeset in LaTeX from the canonical object records.

## Phase 3 Hard Visual Cases Covered

| Hard Visual Case | Plate ID | Verification Outcome |
| --- | --- | --- |
| Full sanctuary composition | `pc-art-01-sanctuary-composition` | Passed: freestanding altar, stone ambo, wooden presidential chair, credence table, and recessed tabernacle with lamp; no 1962 altar cards, gradines, or rail. |
| Reflective metal vessels | `pc-art-03-sacred-vessels`, `pc-art-07-incense-set` | Passed: luminous specular graphite modeling distinguishes chalice, wide paten, lidded ciborium, flagon, Communion cup, open pyx, chained thurible, open fire-pan, and incense boat. |
| White linens on white stock | `pc-art-04-white-linens` | Passed: unfolded 3x3 corporal creases, folded corporal, folded purificator, rigid square pall, lavabo towel, and draped altar cloth corner remain legible without gray background boxes. |
| Worn vestments (priest vs deacon) | `pc-art-08-priest-deacon-vesture` | Passed on v3 after two liturgical audit rejections (see Corrections Log below). |
| Black garments beside white linen | `pc-art-09-black-cassock-surplice-cope` | Passed on v2: deep charcoal-black cassock sustains strong contrast under bright pleated white surplice alongside cope and enveloped humeral veil. |
| Dense multi-object comparison plates | `pc-art-02`, `pc-art-03`, `pc-art-04`, `pc-art-05`, `pc-art-06`, `pc-art-10` | Passed: clear whitespace separation allows unambiguous TeX position keys without arrows or baked numerals. |

## Plate Registry and Full-Size Visual Audit

| Artwork ID | File | Dimensions | Bytes | SHA-256 (prefix) | Visual & Liturgical Audit |
| --- | --- | --- | --- | --- | --- |
| `pc-art-01-sanctuary-composition` | `shared/artwork/graphite/pc-art-01-sanctuary-composition.png` | 1200x896 (8-bit gray) | 320,981 | `8d26f74fa6d8` | Approved (v1) |
| `pc-art-02-altar-ambo-chair` | `shared/artwork/graphite/pc-art-02-altar-ambo-chair.png` | 1200x896 (8-bit gray) | 124,088 | `84e53bfbfd70` | Approved (v1) |
| `pc-art-03-sacred-vessels` | `shared/artwork/graphite/pc-art-03-sacred-vessels.png` | 1200x896 (8-bit gray) | 185,917 | `cdbba37ba00e` | Approved (v1) |
| `pc-art-04-white-linens` | `shared/artwork/graphite/pc-art-04-white-linens.png` | 1200x896 (8-bit gray) | 271,907 | `ff6750e0e616` | Approved (v1) |
| `pc-art-05-liturgical-books` | `shared/artwork/graphite/pc-art-05-liturgical-books.png` | 1200x896 (8-bit gray) | 422,821 | `e43520dd5ba8` | Approved (v1) |
| `pc-art-06-service-cruets-bells` | `shared/artwork/graphite/pc-art-06-service-cruets-bells.png` | 1200x896 (8-bit gray) | 213,409 | `8a8d95838336` | Approved (v2; v1 rejected) |
| `pc-art-07-incense-set` | `shared/artwork/graphite/pc-art-07-incense-set.png` | 1200x896 (8-bit gray) | 203,218 | `a323e592191c` | Approved (v1) |
| `pc-art-08-priest-deacon-vesture` | `shared/artwork/graphite/pc-art-08-priest-deacon-vesture.png` | 1200x896 (8-bit gray) | 240,266 | `591ef299af54` | Approved (v3; v1 & v2 rejected) |
| `pc-art-09-black-cassock-surplice-cope` | `shared/artwork/graphite/pc-art-09-black-cassock-surplice-cope.png` | 1200x896 (8-bit gray) | 290,184 | `cf8d77041ff8` | Approved (v2; v1 rejected) |
| `pc-art-10-communion-triduum-vessels` | `shared/artwork/graphite/pc-art-10-communion-triduum-vessels.png` | 1200x896 (8-bit gray) | 196,396 | `7e7ea6f62b73` | Approved (v1) |

## Liturgical & Visual Audit Corrections Log

Full-size inspection caught and rejected three defective drafts prior to normalization:

1. **`pc-art-06-service-cruets-bells` (v1 rejected):** The processional cross titulus included baked `INRI` lettering (violating the zero-embedded-text contract), and the sanctuary bell showed two impossibly fused hand bells. Regenerated as v2 with a blank cross top and a proper four-cup mounted brass altar bell.
2. **`pc-art-08-priest-deacon-vesture` (v1 and v2 rejected):** Draft v1 placed the deacon's diagonal stole over the outside of the dalmatic contrary to GIRM 340. Draft v2 separated the deacon into two figures (alb + diagonal stole without dalmatic; dalmatic over stole) but placed the peeking fringed stole tail under the deacon's left hem instead of his right hem. Targeted edit v3 relocated the fringed stole tail to the deacon's right side (viewer's left), matching the center figure.
3. **`pc-art-09-black-cassock-surplice-cope` (v1 rejected):** Draft v1 showed the priest grasping an uncovered chalice bare-handed while the humeral veil hung unused beside his arms. Regenerated as v2 so the fringed cloth of the humeral veil properly envelops both hands supporting a closed lidded ciborium.

## Rights Status

All ten final PNG plates are newly created project assets owned under the repository license (CC BY 4.0). No third-party scans, photographs, museum images, or copyrighted liturgical illustrations were copied or traced.
