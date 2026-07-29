# Pontifical gloves and ring artwork audit — 2026-07-28

## Scope and source boundary

This audit covers three new asset-local staging records only:

- `RPD-FIG-pontifical-0101-episcopal-gloves-pair-alpha`;
- `RPD-FIG-pontifical-0102-episcopal-ring-alpha`; and
- `RPD-FIG-pontifical-0103-ring-over-right-glove-alpha`.

No canonical object record, shared artwork manifest, edition selection, installed
publication, or public metadata is changed here.

The relationship is controlled by the exact 1948 Marietti third post-typical
edition of the *Cæremoniale Episcoporum*, book II, chapter VIII. At n. 19
(printed p. 116; exact artifact PDF p. 127), the deacon puts the glove on the
bishop's right hand and the subdeacon puts the glove on his left. At n. 22
(printed p. 117; exact artifact PDF p. 128), after the intervening vesting
actions, the assistant priest puts the pontifical ring on the ring finger of
the bishop's right hand. Both pages were read in the OCR layer and visually
collated against the exact page images on 2026-07-28.

The public-domain Benziger Brothers 1893 commercial catalog, printed p. 47
(exact artifact PDF p. 57), supplies a rights-clear dated material-variation
control. It lists bishops' gloves in several colors, either plain or with
embroidered crosses, and identifies episcopal rings as a manufactured class.
It does not picture or prescribe a universal ring form. Consequently the new
assets deliberately avoid treating a glove embroidery scheme, cuff treatment,
ring stone, bezel, metal, heraldry, dimensions, or ornament as universal.
For the isolated ring, its visually substantial scale and plain raised oval
setting are non-normative editorial recognition conventions; neither is a
source-controlled feature.

The visual forms are project-generated graphite recognition studies. No
external image was supplied to the generator as a visual reference.

## Separation and combined-use decision

The gloves and ring can each be drawn and understood as separate objects, so
they receive separate recognition assets. Their liturgical relationship cannot
be taught adequately by the two isolated forms alone, so a third asset shows
the combined formation: one ring on the right ring finger, visibly outside the
already donned glove. This follows the project rule that separately intelligible
objects remain separate while an often-together or sequence-dependent
formation receives its own appropriately labeled use view.

## Generation and alpha production

All three drawings were generated through the OpenAI built-in image-generation
interface, whose model and version were not exposed. Each prompt required a
uniform green background, monochrome graphite subject, generous crop safety,
and no baked-in text, labels, arrows, border, watermark, cast shadow, or
unsupported ornament.

The exact generated green-background sources remain only in the ignored build
tree. The repository assets were produced with the imagegen skill's local
Pillow chroma-key helper using border auto-key sampling, a soft matte,
transparent threshold 12, opaque threshold 220, and despill. Each final is a
1254 × 1254 RGBA PNG with true alpha:

| Asset | SHA-256 | Nontransparent bounding box | Review |
|---|---|---:|---|
| Gloves pair | `1740377da967dfdd457b56cdbe9d45f3a5373ff0dc319d7a5ee43316218a7a0b` | 1080 × 1021 at +85,+104 | Accepted |
| Isolated ring | `30be5030e9949eaa9db037d09ec8b1881a65097c281900f955fa2881a29c87f4` | 927 × 883 at +174,+179 | Accepted after substantial size and raised oval setting were classified as editorial conventions |
| Ring over right glove | `c5cbcb91127323b5d54cb7a57548de9505ba1e371deb6dd85e433b075db7a594` | 702 × 1164 at +312,+32 | Accepted |

Transparent corners, interior negative spaces, complete silhouettes, crop
margin, and the absence of a floating rectangular background were checked on
the alpha files. The combined asset was also composited over warm page stock:
the ring remains legible on the second finger from the little-finger side, the
right hand has exactly five fingers, and no green fringe is visible.

## Admission boundary

These assets are suitable candidates for a later canonical-manifest and object
record integration pass. This audit does not itself claim canonical admission,
consumer eligibility, complete pontifical coverage, or competent ceremonial
review beyond the exact identity and relationship checks stated above.
