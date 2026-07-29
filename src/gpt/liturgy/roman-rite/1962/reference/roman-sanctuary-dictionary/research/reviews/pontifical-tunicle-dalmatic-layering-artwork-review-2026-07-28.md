# Pontifical tunicle, dalmatic, and layering artwork review

Date: 2026-07-28

Scope: superseding asset-local review of one project-generated worn cutaway.
This review rejects and removes the preceding three-plate proposal. It does
not admit the replacement to the shared artwork manifest, bind it to object
records, rebuild a publication, or establish a universal vestment morphology.

## Source ceiling

The 1962 Missal controls the distinct objects and their order: the bishop wears
the chasuble over the dalmatic and tunicle, and the pontifical vesting prayers
name the tunicle and dalmatic separately. The checked 1948 *Caeremoniale
Episcoporum* additionally supports cords tightened on each side over the
shoulders when these two vestments are put on. None of these loci establishes a
universal cut, dimensions, ornament, textile, sleeve relation, or isolated
visual distinction between the pontifical tunicle and pontifical dalmatic.

## Rejected precursor set

Independent review rejected all three prior candidates. The isolated tunicle
and horizontally mirrored dalmatic were visibly copy-like and did not teach
why two separately named objects belong in the dictionary. Their associated
PNG and TOML files have been removed rather than retained as alternatives.
The exploded-shell plate likewise failed the requested one-wearer cutaway and
read as three floating garments.

The initial 24-percent color-distance removal also left portions of the
nonuniform generated chroma field outside the subject. Transparent corners
alone did not prove the absence of a semi-opaque rectangular gradient. The
review therefore rejects the prior alpha audit as insufficient.

## Replacement

The replacement shows exactly one coherent faceless wearer. The intact
picture-left half establishes the outer chasuble. A vertical picture-right
peel-back exposes the middle and inner plain sleeved layers on the same
shoulder and torso. Their two restrained cord ends and nesting order provide
the only baked-in distinction; later TeX labels must name the pontifical
dalmatic and pontifical tunicle explicitly. The plate does not use different
ornament, color, cut, sleeve length, sleeve width, body width, or asserted hem
relation to distinguish them.

## Pixel and boundary review

The replacement is a 1024 by 1536, 8-bit grayscale-alpha PNG. Independent
review rejected an intermediate HSL-saturation matte because a low-saturation
portion of the generated field remained visible as a gray gradient on warm and
dark grounds. Transparent corners and a white composite had concealed that
failure.

The superseding matte treats every pixel whose normalized green channel
exceeds both red and blue by more than 0.03 as part of the connected generated
field. The inverse mask received a 0.45-sigma edge blur, retained pixels were
converted to grayscale, and metadata was stripped. This criterion clears both
the bright green field and its darker or less-saturated vignette while
preserving the grayscale graphite subject.

Every corner is fully transparent. The nonzero-alpha bounds are 826 by 1515
pixels at offset +101+21, not the full canvas, and the image has 29 observed
alpha levels rather than a binary edge. The candidate was composited over a
checkerboard, dark `#1d1a22`, and warm `#e8d8bd` ground. All three show a clean
subject boundary with no floating rectangle, gray gradient, vignette, or green
fringe. These checks supersede both the inadequate corner-only test and the
white-only intermediate review.

The subject count, coherent-wearer relationship, three-layer order, crop
safety, restrained cords, and absence of embedded text, decorative bows,
symbols, ornament, accessories, architecture, border, and watermark were
checked.

## Disposition

Accepted as one asset-local replacement candidate for later canonical
object-record and manifest integration. Publication treatment must label the
three layers by order and name and state that the image does not establish a
diagnostic tunicle/dalmatic cut.
