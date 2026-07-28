# Selected-artwork boundary audit — 2026-07-28

## Scope

This audit covers every raster selected by the six generated dictionary
editions, together with the altar-server edition's two bespoke paten
comparisons. The union contained 48 selected rasters: 26 already had a
usable grayscale-alpha boundary, 20 were opaque grayscale drawings on a
paper field, and two were intentionally opaque document/detail cards.

The 20 safe opaque drawings received new grayscale-alpha successors. The
already-alpha combined Missal, stand, and marker formation also received a
successor because its nominally transparent corners retained opacity of
4/255. Every predecessor remains registered and unchanged. The exact
successor paths, dimensions, byte counts, and SHA-256 identities are recorded
in `artwork-manifest.toml`.

## Deterministic transformation

For an opaque grayscale source, inverse grayscale supplies the initial
opacity. For the existing Missal grayscale-alpha source, its alpha channel
supplies the initial opacity. In both cases the final opacity is:

- zero at or below 20/255;
- the original opacity multiplied by cubic smoothstep from 20/255 through
  40/255; and
- unchanged at or above 40/255.

The output color channel is black, matching the established pencil-boundary
representation. The transformation changes no canvas dimensions, crop,
resampling, geometry, object relationship, or TeX-owned label. It is a local
ImageMagick 7 transformation and uses no image-generation prompt or model.

## Deliberate opaque exclusions

`RPD-FIG-sacred-vessels-0003-comparison-paten-exemplar.png` and
`RPD-FIG-sacred-vessels-0004-communion-plate-paten-comparison.png` remain
opaque. They are tightly cropped source/detail comparison cards whose paper
ground and baked documentary composition are intentional; dissolving that
ground would misrepresent their boundary rather than merely remove a matte.

The marker-ribbon detail was treated separately with the same opacity rule.
Its existing tight crop and the book's intersection with the top and right
canvas edges are deliberate and unchanged. Full-size review confirmed that
the paper field disappears while the cropped book edge, page block, and all
six ribbons remain legible.

## Review

Every successor was composited at full canvas size over `#f5ecd8`, and all
six rebuilt dictionary PDFs were inspected in bounded contact sheets. The
review checked the pale linens, altar cloth outlines, white candle body,
sanctuary-lamp chains and glass, metallic highlights, fringes, cropped marker
detail, and other thin geometry. Eighty-three of the 84 successor corners are
fully transparent. The sole exception is the marker detail's top-right corner,
where the deliberately cropped dark book—not paper field—meets the existing
canvas boundary; forcing that object pixel transparent would alter the
drawing. No floating paper rectangle, color fringe, added object, clipped new
edge, solid-black render, or lost substantive graphite was found.

The successors inherit their predecessors' project-created rights
dispositions, source ceilings, representative-morphology qualifications, and
consumer constraints. Alpha derivation supplies no evidence and changes no
factual or ceremonial claim.
