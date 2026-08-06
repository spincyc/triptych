# Measurements

These are deltas from the untouched reviewed baseline at
`0f3567dc509a2d5b42fd58a0e4c77c8f5e5dc113`, not only final values.

| State | Baseline | Corrected | Delta |
| --- | ---: | ---: | ---: |
| Read width, 768×1024 | 726px / ~86 chars | 636px / ~75 chars | −90px / −11 chars |
| Missal first principal text, 1440×900 | 474.58px | 316.98px | −157.60px |
| Missal first principal text, 393×852 | 441.77px | 324.09px | −117.68px |
| Missal first principal text, 320×852 | 458.83px | 340.28px | −118.55px |
| Roman partial first held text, 393×852 | 591.14px | 393.75px | −197.39px |
| Postconciliar first held text, 1440×900 | 741.11px | 542.45px | −198.66px |

The final 320px division is two balanced lines and 53.17px high. The desktop
shell is 68px wide at x=184.5, transparent, square, shadowless, and ruled on
the plane-facing edge. The 393px dock is opaque `rgb(250, 248, 242)`, square,
73.19px high, and ruled at the top. Every required state reports zero horizontal
overflow; exact route/hash, viewport, scroll, geometry, focus, semantic state,
and error counts are in `evidence/capture-metadata.json`.
