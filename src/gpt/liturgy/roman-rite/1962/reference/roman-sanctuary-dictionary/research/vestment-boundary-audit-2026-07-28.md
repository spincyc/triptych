# Sacristan vestment boundary audit — 2026-07-28

## Scope

This audit covers the nine existing pencil drawings used together on the
Sacristan vestment pages: amice, alb, cincture, maniple, priest's stole,
chasuble comparison, deacon's stole, dalmatic, and tunicle. It changes only
their page boundary treatment. The drawings, dimensions, crop geometry,
object relationships, object records apart from their exact asset bindings,
and inherited project-generated provenance remain unchanged.

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
values at or above 40/255 unchanged. This removes the residual paper field
while preserving substantive graphite, color channels, canvases, and geometry. Compositing over
the warm review field `#f5ecd8` showed continuous page blending without a
rectangular boundary or clipped object marks.

## Identities

| Object | Source SHA-256 | Successor | Successor SHA-256 | Geometry | Bytes |
|---|---|---|---|---|---:|
| Amice | `3215b44d265c2a2452a46285989c75c043837b2806912287bb037882199ac902` | `RPD-FIG-vestments-0001-amice-v3-alpha.png` | `e83d557d9c5d755f675d7cb4997d10adf44e0a8061742825e260928062f13dd9` | 900 × 1350 | 454193 |
| Alb | `0017169f71808e6108b7a3ff8d36d1654d3b90036b306174a1559884c7086bdf` | `RPD-FIG-vestments-0002-alb-v3-alpha.png` | `8303523bf3c106e3f8c7f75e8d4950e8b39d5cd59ca4af6df1fc33755ee5d959` | 900 × 1350 | 391228 |
| Cincture | `7c429d9cf7effa8e31a7e9f65e4a2944341e864bfe8c2557694e709f2ab51b75` | `RPD-FIG-vestments-0003-cincture-v3-alpha.png` | `370c3b4942d805345dbcaefea85dd18dc4f7cdbf592244e0f8391d11d09018ce` | 900 × 1350 | 140414 |
| Maniple | `d7cd099e4ab1ccb38b3b7d5e19451178e6bb900fe04303eef70c091b0b816286` | `RPD-FIG-vestments-0004-maniple-v3-alpha.png` | `47cf77323f3a1548f2b5556894fbdb7834c42cfbce5f8c7b018d629ed4b87724` | 900 × 1350 | 244212 |
| Priest's stole | `191d0cb33b7a54dceb9bff71265805bfec843bb24cd5adeebe3d34b945df500a` | `RPD-FIG-vestments-0005-priest-stole-v3-alpha.png` | `a7746371bc7efc66d44bcf3bdae30cbb4f0494070ebfeaa7795a3d979a3de467` | 900 × 1350 | 474516 |
| Chasuble comparison | `b2dea2cca53cd0f20bfed32b88ca5f762a9216fa5cc0f5250da600d85b82f6a9` | `RPD-FIG-vestments-0006-chasuble-comparison-v3-alpha.png` | `8fe0eaf6ac691cf4177aa886040ac33d0463540ba57f8c91c04d8ef03c98e3c3` | 1350 × 900 | 474377 |
| Deacon's stole | `2732ebb2b606bd6c29356f41f2fdcf202a19eb67619a51ee24bb25e4c22abc33` | `RPD-FIG-vestments-0007-deacon-stole-v4-alpha.png` | `eac7199f1433160269ec6c8daaca913ec89088b96fc569271c6e9e528b3d9b1c` | 900 × 1350 | 451967 |
| Dalmatic | `3fd85257e901c93f25e0b723d351498d04743d2f65a8b4f4bdd9861f0612e5a8` | `RPD-FIG-vestments-0008-dalmatic-v3-alpha.png` | `9d2f860c6cc99204277e0deb721daac25f907cd652cc379098e98b9050aeb45c` | 900 × 1350 | 401764 |
| Tunicle | `c2566fdc0460d058d04640be5ae17deef3a4638607fcffc1dda457b6dfcf3932` | `RPD-FIG-vestments-0009-tunicle-v3-alpha.png` | `df5e01c1a8ef2810723cb287060bc4a5e2d8f97829c4b3a59432365c918a854c` | 1350 × 900 | 297104 |

The canonical artwork manifest registers these nine successors as
deterministic alpha derivatives while retaining the `v2` precursor rows.

### Deacon's-stole lower-edge correction

The first `v3-alpha` derivative retained faint nonzero opacity on its final
row. That was unobtrusive on white but appeared as a straight lower cutoff on
the warm publication ground. The `v4-alpha` successor preserves the canvas,
color channel, and all opacity above row 1150, then multiplies only the final
200 alpha rows by a linear white-to-black ramp. Its last row is fully
transparent. White compositing has zero differing pixels across the retained
upper 900 × 1150 region, and the warm `#f3eadb` review composite shows the
existing garment fade ending naturally without a floating boundary.
The exact `v3-alpha` file remains registered as superseded provenance, and
the manifest records it explicitly between the source artwork and `v4-alpha`
so the deterministic custody chain remains reproducible.
