# Special-equipment artwork boundary audit — 2026-07-28

## Scope

This audit covers four existing project-generated pencil drawings: the
portable holy-water vessel, aspergillum, basilical conopaeum, and Eucharistic
ombrellino. It changes only their publication boundary treatment. The
drawings, pixel dimensions, crop geometry, object relationships, source
claims, and project-generated provenance remain unchanged.

The four exact object bindings now select the deterministic alpha successors.
The canonical artwork manifest must retain the `v2` precursors and add the
successors in a coordinated manifest-owned tranche; this audit does not modify
that concurrently owned shared file.

## Deterministic transformation

Each grayscale `v2` source was converted to a stripped 8-bit grayscale-plus-
alpha `v3-alpha` successor. The successor stores black as the color channel
and the exact inverse of the source grayscale as opacity:

```text
magick SOURCE -colorspace Gray -fill black -colorize 100 \
  \( SOURCE -colorspace Gray -negate \) -alpha off \
  -compose CopyOpacity -composite -depth 8 -strip DESTINATION
```

The opacity was then refined by setting values at or below 20/255 to zero,
multiplying values from 20/255 to 40/255 by a cubic smoothstep, and leaving
values at or above 40/255 unchanged. This introduces no generative redrawing,
crop, resampling, color-channel change, or geometric change. Full-size composites over the warm review
field `#f5ecd8` retain the complete pencil drawing and soft graphite edges
without a floating white rectangle, clipping, or color fringe.

## Exact identities

| Object | `v2` source SHA-256 | Successor | Successor SHA-256 | Geometry | Bytes |
|---|---|---|---|---|---:|
| Portable holy-water vessel | `0beb2cc255d667231beae30a3f0d1eaf0147964685e571e21a952792045770ef` | `RPD-FIG-related-ceremonies-0001-iso-holy-water-vessel-v3-alpha.png` | `41dd7753545e01d72d430de9d833e0d2ef7dcd28c36b31cefa602f0b1e6ec899` | 1024 x 1535 | 396718 |
| Aspergillum | `c8453019c107c7b0b85ab4847577867bf56463353ea4aacfc2e97c390dc8e9f1` | `RPD-FIG-related-ceremonies-0002-iso-aspergillum-v3-alpha.png` | `6a8d03bd409aad6abab6cbeb03e96606d317faf59d20f4b31cbf5cc121494b70` | 1536 x 1024 | 147612 |
| Basilical conopaeum | `2bc2433289c6fc6d119354c61c53ae800f10405a3dd711fa262d5ff8d5db51bc` | `RPD-FIG-related-ceremonies-0003-basilical-conopaeum-v3-alpha.png` | `31402c7c3c0891b8d28f1cb05df7bda34a053e77c2dc99d72ac7bcabececac0e` | 900 x 1350 | 203547 |
| Eucharistic ombrellino | `bcdffc7d0ae4677ab7490fc2a25e727df8fbc0b2947c50bccd57bff8f6d4ceca` | `RPD-FIG-related-ceremonies-0004-eucharistic-ombrellino-v3-alpha.png` | `b831e0ef96e8b845498749f3a812b17ef90c9f45972550be9f79304677081a40` | 900 x 1350 | 105526 |

Each successor inherits its precursor's project-generated rights disposition,
source-controlled identity, deliberate omissions, representative-morphology
ceiling, and consumer qualifications. Alpha derivation supplies no evidence
and changes no factual or ceremonial claim.
