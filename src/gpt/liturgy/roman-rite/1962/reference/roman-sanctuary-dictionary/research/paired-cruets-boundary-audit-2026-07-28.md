# Paired altar-cruets boundary audit — 2026-07-28

## Scope

This audit covers the existing paired altar-cruets pencil drawing. It changes
only the page-boundary treatment. The drawing, dimensions, crop geometry,
paired-object relationship, canonical artwork identity, and inherited
project-generated provenance remain unchanged.

## Deterministic transformation

The normalized grayscale source was converted to a stripped 8-bit
grayscale-plus-alpha successor. The successor stores black as the color
channel and the exact inverse of the source grayscale as opacity:

```text
magick SOURCE -colorspace Gray -fill black -colorize 100 \
  \( SOURCE -colorspace Gray -negate \) -alpha off \
  -compose CopyOpacity -composite -depth 8 -strip DESTINATION
```

This representation was refined by setting opacity at or below 20/255 to
zero, multiplying opacity from 20/255 to 40/255 by a cubic smoothstep, and
leaving opacity at or above 40/255 unchanged. The correction removes the
residual paper field while preserving substantive graphite and all geometry. Compositing it over the warm review
field `#f5ecd8` preserves the complete pencil drawing while allowing the page
stock to remain visible through the surrounding field and soft marks; visual
inspection found no rectangular boundary or clipped object marks.

## Identity

| Source | Source SHA-256 | Successor | Successor SHA-256 | Geometry | Bytes |
|---|---|---|---|---|---:|
| `RPD-FIG-service-objects-0103-paired-cruets.png` | `54af058e1504b3b919d7ff3fcf4e5895a1d77510c6a97e488dfc5a71a34efc7b` | `RPD-FIG-service-objects-0103-paired-cruets-v2-alpha.png` | `a485b88c70b29cffd130663619c1e15a86aac362de8336a10f3779b7b0517adc` | 1536 × 1024 | 384668 |

The canonical artwork manifest registers this deterministic alpha successor
while retaining the normalized grayscale precursor row.
