# Gospel-book ceremonial artwork review

Date: 2026-07-28

Asset:
`shared/artwork/pencil/books/RPD-FIG-books-0007-gospel-book-in-use-v2-alpha.png`

Asset-side provenance:
`shared/artwork/pencil/books/RPD-FIG-books-0007-gospel-book-in-use-v2-alpha.toml`

## Superseded candidate

The first `v1` candidate is rejected and removed. Its center minister carried
long vertical bands that could be read as a stole rather than an unmistakable
subdeacon's tunicle and maniple. Its alpha-channel review was also inadequate:
the record inferred a usable matte from a warm-paper preview without recording
the channel/type checks required to exclude a floating rectangle. No
publication should use that candidate.

## Scope and source boundary

This illustration identifies the Gospel book through its verified ceremonial
use at Solemn Mass. The central subdeacon holds one open book between exactly
two candle-bearing acolytes. The formation is controlled by the 1962
*Missale Romanum*, *Ritus servandus* VI.5, as recorded in
`../books-and-book-supports-source-pass.md` and the repository source record
`src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/passages/ritus-servandus-acolyte-candlesticks.toml`.

The center minister wears a broad, short-sleeved tunicle over the alb, with a
short maniple hanging from his left forearm and no stole or neck-descending
bands. The drawing does not claim a distinctive cover, binding, ornament,
material, dimension, or local furnishing. The open pages and ministerial
relationship, not invented morphology, distinguish the book.

## Generation and boundary treatment

The built-in image-generation tool produced a graphite-pencil scene on a flat
chroma field. The field was removed locally, the RGB subject was normalized to
monochrome, and the extracted matte was feathered with a 0.55-sigma Gaussian
blur before the final PNG was explicitly written as 8-bit sRGBA. This lets the
figures blend into each publication's page field without a floating
rectangular boundary.

Final prompt:

The exact final prompt is retained in the asset-side TOML.

## Visual acceptance

- exactly three figures are present;
- the center minister is visibly a subdeacon in a broad short-sleeved tunicle,
  with one maniple on his left forearm and no stole or neck-descending bands;
- the subdeacon supports one open book with both hands;
- exactly two candle-bearing acolytes flank him, one on each side;
- exactly two upright candlesticks are present;
- no deacon, priest, extra server, lectern, altar, or scenery is present;
- no cover ornament or book-specific morphology is asserted;
- full figures and candle flames remain inside the image boundary;
- ImageMagick reports `1536x1024`, `srgba 4.0`, `opaque=False`, `Depth:
  8-bit`, `Alpha: 8-bit`, alpha minimum `0`, alpha maximum `1`, and corner
  pixel `srgba(0,0,0,0)`;
- an extracted-alpha histogram contains 39 distinct levels, rather than the
  rejected binary matte's two levels;
- the alpha mean is `0.390751`, demonstrating mixed subject/background
  coverage rather than an all-opaque rectangle;
- a separate composite on warm paper shows feathered monochrome graphite edges
  without a green fringe or rectangular field.

SHA-256:
`75d3edccb57ee23aaad467663526e44344ebf4ab51c994d543f0042366cf0d9b`.

Status: accepted as an Alpha educational illustration, pending placement and
whole-publication review by the dictionary integration lane.
