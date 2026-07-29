# Historical artwork manifest

Audit date: 2026-07-27

Current status (2026-07-29): this manifest preserves a historical asset and
review snapshot. The linked priest-review sheet is non-operative research
history, not a current alpha admission path, release gate, or promise of
external review. Concrete source, rights, safety, reproducibility, mechanical,
and visual limitations stated here remain controlling.

| Artwork ID | Asset | Depicts | SHA-256 | Review state |
| --- | --- | --- | --- | --- |
| `art-rsd-hist-001` | `shared/artwork/pencil/RSD-HIST-001-early-medieval-objects.png` | flabellum; suspended Eucharistic dove; Eucharistic tower | `613ee9f2fbba6f64c0386bce82d53bda02205cf1a97540d94f53b30244957b69` | reviewed after removal of an impossible pedestal from the suspended dove |
| — (held asset `file-rsd-hist-002`) | `shared/artwork/pencil/RSD-HIST-002-pre-1955-objects.png` | folded chasuble; unresolved broad-stole lead; triple candle on reed | `3263d01430d30c57209f1e4ecbcf1e7279771aceb0d96c4a819566bd3b7b8916` | held outside artwork eligibility because the broad stole lacks a canonical, source-bound object record |

Both assets were generated on 2026-07-27 with the built-in image-generation
tool from project-written briefs. They are monochrome graphite reconstructions
on white, contain no semantic lettering, and are not to common scale.
Their publication files were normalized on the same date without resizing:
ImageMagick converted them to stripped 8-bit grayscale PNGs with no alpha or
embedded color profile. The table records the normalized identities.

The plate captions, names, dates, status, and interpretations remain typeset
outside the artwork. The drawings may teach morphology but do not independently
establish ritual status or historical chronology.

## Generation briefs

`art-rsd-hist-001` requested three separated museum-catalog graphite specimens:
a circular hand-held Western liturgical flabellum, a chain-suspended
dove-shaped Eucharistic vessel, and a Gothic tower-shaped Eucharistic
receptacle. The first result gave the suspended dove an incompatible pedestal.
A targeted edit removed that pedestal while preserving the three suspension
chains. The manifest hash names the corrected result.

The held `file-rsd-hist-002` asset requested two full-body construction views and one isolated
implement: a sacred minister in a folded chasuble, the broad stole as a wide
diagonal band over the alb, and an arundo topped by exactly three candles. The
brief prohibited generated labels, flames, extra vestments, and a Paschal
candle.

## Review boundary

Internal visual review checked count, silhouette, support, absence of generated
lettering, and gross construction errors. The questions preserved in
`historical-priest-review.md` do not certify exact artifact reproduction or
liturgical status and are not a current review requirement.

The second raster remains in exhaustive technical custody only. It is not an
eligible artwork record and is not rendered in a priestly-review copy. The
folded-chasuble and triple-candle identities remain in the canonical inventory,
but this composite cannot be linked to them without also laundering the
unresolved broad-stole depiction.
