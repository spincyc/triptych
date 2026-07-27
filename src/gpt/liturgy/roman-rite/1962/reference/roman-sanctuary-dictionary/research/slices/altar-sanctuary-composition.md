# Altar and core sanctuary composition inventory slice

Audit date: 2026-07-27 (America/Chicago).

Owner boundary: the altar, its architectural setting, gradines, tabernacle,
altar cards, altar cross or crucifix, reliquaries or images, fixed canopies,
steps, predella, and the relationships among them. This is a research slice
for later merger into the canonical object inventory; it does not amend the
aggregate manifests or make any entry publication-ready.

## Evidence checked in this pass

The 1962 *Missale Romanum* artifact acquired in the run-owned temporary tree
was inspected directly. The following narrow claims are supported at the
printed loci stated:

- *Rubricae generales Missalis Romani* XI.526 says that the altar is covered
  with three duly blessed cloths, one long enough to reach the ground at the
  sides.
- *Rubricae generales* XI.527 says that a sufficiently large cross with a
  crucifix is in the middle of the altar, with the candlesticks required by
  the class of Mass and lighted candles on either side; the three objects
  called *tabellae secretarum* are put there only for the time of Mass.
- *Ritus servandus* II.2 distinguishes the reverence made when the altar has a
  tabernacle of the Blessed Sacrament and describes ascending to the middle of
  the altar.
- *Ritus servandus* IV.5 provides for relics or images of saints on the altar
  and their incensation after the cross, while expressly accommodating their
  absence.

These loci establish presence or ceremonial relationships only. They do not
establish the morphology, dimensions, materials, architectural taxonomy, or
English and Latin headwords proposed below. The acquired PDF and text extract
remain transient leads until the dictionary owner creates a lawful canonical
source binding under `src/sources/` in accordance with `guidance/sources.md`.

## Proposed canonical records

| Proposed object ID | English working name | Latin lead | Category | Evidence ceiling after this pass | Principal unresolved point |
|---|---|---|---|---|---|
| `obj-altar` | altar / high altar | `altare` | church and sanctuary | source text located for its liturgical relationships | Construction, consecration components, and high/side-altar taxonomy |
| `obj-altar-mensa` | altar table / mensa | `mensa altaris` | altar and appointments | term located in *Ritus servandus* IV.4 | Relationship to the whole altar and to the altar stone |
| `obj-gradine` | gradine / altar shelf | lexical lead unresolved | altar and appointments | identified lead only | Whether and where it is assumed, permitted, or merely common |
| `obj-tabernacle` | tabernacle | `tabernaculum sanctissimi Sacramenti` | altar and appointments | checked liturgical presence/relationship | Reservation law, morphology, veiling, and altar-placement conditions |
| `obj-altar-card-center` | center altar card | `tabella secretarum` lead | books and printed objects | collective three-card presence checked | Exact singular terminology, content, dimensions, and print history |
| `obj-altar-card-epistle` | Epistle-side altar card | `tabella secretarum` lead | books and printed objects | collective three-card presence checked | Exact contents and placement |
| `obj-altar-card-gospel` | Gospel-side altar card | `tabella secretarum` lead | books and printed objects | collective three-card presence checked | Exact contents and placement |
| `obj-altar-crucifix` | altar cross with crucifix | `Crux ... cum Crucifixo` | altar and appointments | checked placement relationship | Substantive forms, dimensions, and visibility rules |
| `obj-altar-candlestick` | altar candlestick | `candelabrum` | altar and appointments | checked variable presence by class of Mass | Counts and arrangements by ceremony; material forms |
| `obj-altar-reliquary` | altar reliquary | `reliquiae` (contents), container term unresolved | altar and appointments | conditional presence checked | Reliquary versus image, permissions, contents, and morphology |
| `obj-altar-image` | image of a saint on the altar | `imago Sancti` | altar and appointments | conditional presence checked | Image types, placement, and relationship to reliquaries |
| `obj-predella` | predella / footpace | terminology unresolved | church and sanctuary | identified lead only | Universal terminology, dimensions, and relationship to steps |
| `obj-altar-step` | altar step | `gradus altaris` | church and sanctuary | lowest step and ascent relationships checked | Count, proportions, and local architectural variation |
| `obj-fixed-baldachin` | fixed baldachin / altar ciborium | `ciborium` / `baldachinum` leads | church and sanctuary | identified lead only | Terminology, fixed architectural forms, privileges, and chronology |
| `obj-processional-canopy` | portable processional canopy | terminology unresolved | related ceremonies | confusable lead only | Must be kept distinct from a fixed altar canopy |

## Composition and variant rules to preserve

- Do not make the familiar six-candlestick arrangement a universal Low Mass
  requirement merely because it appears in the artwork. The checked Missal
  locus expressly varies required candlesticks with the quality of the Mass.
- Keep a fixed architectural ciborium or baldachin distinct from a portable
  textile canopy and from the English vessel called a ciborium.
- Treat reliquaries and saint images as conditional altar appointments, not
  as mandatory ornaments.
- Treat decoration, architectural style, and carving as non-substantive until
  a material-culture audit proves a difference relevant to identification or
  use.
- The artwork's two flanking reliquary-like objects, two gradines, three
  steps, and particular baldachin design are editorial exemplars, not
  verified universal forms.

## Pencil composition plate

### `DIC-ART-SA-001`

- File:
  `shared/artwork/pencil/DIC-ART-SA-001-sanctuary-composition.png`
- Received generator output: 1024 by 1536 pixels, 8-bit sRGB PNG,
  2,124,584 bytes; SHA-256
  `912da7472ef6e9347d521b1e62a793d7d9dca621aaeeea4269dd2a8548e1f1df`.
- Repository normalization: stripped 8-bit grayscale PNG, 1024 by 1536
  pixels, 687,999 bytes; SHA-256
  `d4b5016d233dcef703d3326ed740b7b6df3f315932f7a0b2a484bf02595e8cbb`.
- Generator: built-in OpenAI image-generation interface; no model or version
  was exposed. Generated 2026-07-27. No reference image was supplied.
- Prompt summary: a dense, unlabelled US-Letter-portrait graphite
  architectural plate showing a traditional high altar, cloths, tabernacle,
  gradines, exactly six principal candlesticks, central crucifix, three blank
  framed altar cards, two modest reliquary-like ornaments, sanctuary lamp,
  three steps and predella, beneath a fixed four-column baldachin; with
  tabernacle/gradine and side-composition insets; no people, color, writing,
  labels, arrows, or watermark.
- Intended consumer: `plt-sanctuary-orientation` and
  `plt-altar-composition`, after object-level audit and TeX labelling.
- Personal visual review: passed at full raster size for monochrome finish,
  portrait density, six-candle count, one central crucifix and tabernacle,
  three blank cards, sanctuary lamp, steps/predella, useful insets, absence of
  people and readable text, and absence of obvious duplicate or impossible
  structural parts.
- Factual review: **held**. The image accurately satisfies its editorial
  brief, but its particular morphology and whole composition have not been
  verified against a material-culture corpus. It is not approved for a
  publication plate.
- Rights: newly generated project asset; no external visual reference was
  supplied. Repository licensing and release review remain pending.

## Next source work

1. Create the exact repository-wide source binding for the inspected 1962
   Missal artifact and record its identity, rights status, and checked loci.
2. Inspect the governing reservation law and contemporary ceremonial sources
   for the tabernacle and sanctuary arrangement.
3. Acquire a provenanced architectural and material-culture corpus for altar,
   gradine, reliquary, candlestick, tabernacle, and canopy forms.
4. Resolve the overloaded term “ciborium” before any index or cross-reference
   is rendered.
5. Generate separate isolated/comparison views only after morphology and
   substantive variants are source controlled.
