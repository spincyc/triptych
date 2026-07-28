# Sacristy recognition source audit

Date: 2026-07-28

## Correction boundary

This pass corrects source identity before changing the sacristy records. The
60,347,644-byte Digital Library of India PDF, SHA-256
`10acb8de9b161ed2c08be7ce767515418bca5d1ed7ddfff2de902179e1b62c7a`,
was previously cataloged as Fortescue's 1917 first edition. Its title and
edition pages instead identify the seventh edition, further revised and
augmented by J. B. O'Connell, London, 1943. The exact artifact and all passage
records verified in its page images were migrated to the corrected 1943
edition. The 1917 first edition remains separately identified and now has an
exact 4,070,649-byte modern-typeset remote witness, SHA-256
`378d281408154d869833e61d8b4d2dc4cc3ec16340c7d1128bf51fb592666d36`;
that artifact is not a facsimile and is not used for the migrated page claims.

## Exact controls

- The 1962 *Missale Romanum*, *Ritus servandus* I.1, prescribes the priest's
  preparatory handwashing. It does not prescribe a basin, sink, plumbing,
  furniture, material, dimensions, or fixed lavatory morphology.
- The same Missal, II.1, directs the vested celebrant to bow his head toward
  the cross or image in the sacristy before proceeding to the altar. It does
  not narrow that alternative to a crucifix or prescribe support and ornament.
- Fortescue--O'Connell 1943, printed p. 59, directs the returning priest first
  to bow his head to the cross. This supplies a checked return witness without
  narrowing the Missal's broader cross-or-image wording.
- Fortescue--O'Connell 1943, printed p. 40, calls it practice in many churches
  for the server to ring a bell at the sacristy door on departure to warn that
  Mass is about to begin. This is local/usual practice, not a universal rubric.
- Andrew Meehan, “Sacristy,” *Catholic Encyclopedia* 13 (1912), in the exact
  New Advent HTML artifact, SHA-256
  `1bb5f7e4719b7079b0b1d7364e5bb784c5a0fa8f7b0949d519f477d7489ceaab`,
  names a crucifix or other suitable image for the departure and return bow, a
  lavatory for handwashing, and, as customary, a bell at the door toward the
  sanctuary. New Advent identifies Andrew Meehan, not J. F. G. Gilmartin, as
  the article's author.

The Missal controls the edition-specific rubric. The 1943 ceremonial and 1912
specialist article control only their stated return and local-practice
evidence. “Canonical custom” is not claimed.

## Canonical disposition

- `obj-sacristy-cross` is admitted for recognition as the locally appointed
  cross or suitable image. Handling says to follow local direction and never
  move, replace, or discard it from appearance.
- `obj-sacristy-bell` is admitted as a local signal separate from altar bells.
  Mechanism, placement, operator, dimensions, material, ornament, and cue
  remain local.
- `obj-sacristy-lavatory` is retained canonically under the period English
  name “sacristy lavatory,” with “clergy handwashing sink or basin” as its
  plain-language gloss. The universal action and the practical local
  furnishing are stated separately. No official Latin object name, artwork,
  or material morphology is admitted, so every pictorial edition excludes the
  record pending a checked material exemplar.
- `obj-piscina-sacrarium` remains held. No fitting's outlet or disposal use may
  be inferred from its appearance.

The rejected composite `art-sacristy-preparation-plate` retains its prompt,
hashes, and failed review as history but has no current consumer. Its invented
lavatory form, ornamented piscina candidates, crucifix-only narrowing, and
wall-mounted pull-bell mechanism are not reused.

## New pencil figures

The built-in image generator supplied two text-free figures without reference
images. Generation is production, not evidence.

### Representative cross

Prompt:

> Use case: scientific-educational
> Asset type: isolated pictorial-dictionary recognition figure for a
> monochrome Catholic sacristy reference
> Primary request: one simple freestanding Latin cross, viewed straight-on, as
> a representative sacristy cross
> Scene/backdrop: pure white blank background
> Subject: a plain upright wooden cross with modest base, no corpus, no
> surrounding room, no wall, no altar, no image frame
> Style/medium: restrained hand-drawn graphite pencil study, clean grayscale
> linework and gentle cross-hatching, matching a serious material-culture
> reference plate
> Composition/framing: single centered isolated object, generous white margin,
> fully visible
> Lighting/mood: neutral even study lighting
> Constraints: object recognition only; this is one representative cross, not
> a prescribed universal form; no dimensions or scale claim
> Avoid: crucifix corpus, sacred-heart motif, decorative carving, gothic
> ornament, rays, halo, lettering, labels, arrows, numbers, border, scenery,
> furniture, watermark, color

Received: 1024 × 1536 RGB, 1,465,273 bytes, SHA-256
`c30e6b16a704ff62f705b99f2de4135b17c1b7be28a7b90875e7e9752467de0a`.
Normalized without content edit to stripped 8-bit grayscale, 443,058 bytes,
SHA-256
`c28affcab66a3cfd629258811225c02daec4d6c746dc819482bdd2dffe5a8b8c`.
The base and wood treatment are explicitly representative.

### Local signal bell

Prompt:

> Use case: scientific-educational
> Asset type: isolated pictorial-dictionary recognition figure for a
> monochrome Catholic sacristy reference
> Primary request: one generic small signal bell, shown as a simple single
> bell with a short top grip and visible clapper, unmistakably separate from a
> cluster of altar bells
> Scene/backdrop: pure white blank background
> Subject: a modest single hand-sized signal bell only; no mount, no bracket,
> no cord, no stand, no room
> Style/medium: restrained hand-drawn graphite pencil study, clean grayscale
> linework and gentle cross-hatching, matching a serious material-culture
> reference plate
> Composition/framing: single centered isolated object, three-quarter view,
> generous white margin, fully visible
> Lighting/mood: neutral even study lighting
> Constraints: recognition only; mechanism, placement, operator, material,
> dimensions, and ornament remain locally variable; not an altar-bell cluster
> Avoid: wall bracket, pull cord, architecture, altar-bell cluster, multiple
> bells, inscription, monogram, cross, decorative motif, lettering, labels,
> arrows, numbers, border, scenery, furniture, watermark, color

Received: 1024 × 1536 RGB, 1,582,675 bytes, SHA-256
`30ff759b57bc34d630da6602000a2f833cbecb45763cbc758d5aa6fd2ae0aa8b`.
Normalized without content edit to stripped 8-bit grayscale, 501,390 bytes,
SHA-256
`96fea3fa35e785d0b3431752d8cf576ca71dcc06c2d84c2207ab1bbc408aa369`.

Both figures contain no lettering, semantic marks, architecture, room context,
or color. The project-generated rasters are distributed under the repository's
project-content terms.
