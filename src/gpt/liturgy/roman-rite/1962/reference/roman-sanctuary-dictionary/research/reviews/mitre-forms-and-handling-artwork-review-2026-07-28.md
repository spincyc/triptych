# Mitre forms and handling artwork production review

Date: 2026-07-28

Assets:

- `shared/artwork/pencil/pontifical-insignia/RPD-FIG-pontifical-0001-three-mitre-forms-v1-alpha.png`
- `shared/artwork/pencil/pontifical-insignia/RPD-FIG-pontifical-0002-mitre-lappets-handling-v1-alpha.png`
- `shared/artwork/pencil/pontifical-insignia/RPD-FIG-pontifical-0002-mitre-minister-veil-v2-alpha.png`

Asset-side provenance is recorded in the same directory in matching TOML
files. This record includes the producing agent's factual-boundary and
visual-production review and the first independent review disposition. It is
not canonical artwork-manifest admission.

## Evidence boundary

The checked *Caeremoniale Episcoporum*, book I, chapter XVII, distinguishes
the precious, gold-cloth, and simple mitres by material and ornament and
identifies the hanging *vittae*. It does not prescribe one universal profile,
height, construction method, iconographic program, or dimensions. Book I,
chapter XI, section 6 directs the mitre minister to use an oblong silk veil or
cloth to support the mitre without touching it with bare hands, unless he is
vested in a cope.

The Metropolitan Museum of Art's circa-1830 mitre is used only as a dated
material-culture check for a two-panel body and paired hanging lappets. The
generated comparison does not copy the object's decorative program, does not
adopt its measured dimensions as a norm, and does not classify that object as
one of the Ceremonial's three forms.

The equal heights in the comparison are an editorial common drawing scale.
They are not a claim that the three classes had prescribed equal dimensions.
TeX must say this wherever the comparison is printed.

## Production and boundary treatment

The built-in image-generation tool created both graphite studies on a flat
green chroma field. Because the installed chroma helper's Pillow dependency
was unavailable, ImageMagick was used to normalize the subject to grayscale,
extract the keyed field, and feather the matte with a 0.55-sigma Gaussian
blur. Both final PNGs are 1536 by 1024 pixels, 8-bit sRGBA, have transparent
corner pixels, report `opaque=False`, and contain graduated rather than binary
alpha:

- comparison: 38 alpha levels; SHA-256
  `0ebde2873a29f7c00d87ae716e3b3916eaf3155dc5df0943d9e550ec6db20b14`;
- lappet/handling detail: 42 alpha levels; SHA-256
  `654195fd04a6efd7b6dd8ef5e0648df6b83531f77570e64b9dc94d7c1edf4631`.

Warm-paper composites show graphite edges blending with the page field and no
floating rectangle or visible green fringe.

## Producing-agent visual audit

The comparison contains exactly three mitres at one drawn scale. All points
and all six lappets are inside the crop. The precious example has generic
jewel-like enrichment; the gold-cloth example has restrained non-jeweled
edging; the simple example has no ornament beyond seams and edge construction.
There are no labels, crosses, arms, museum-display elements, or baked-in scale
claims.

The detail asset contains one rear three-quarter mitre with exactly two
separate lappets and one handling study. The handling study has one mitre, two
anatomical hands, and one continuous cloth visibly interposed between the
hands and the mitre. It does not show a stand, case, full minister, transfer
sequence, or invented fastening.

That first handling study nevertheless fails the official source's object
identity: the loose cloth over disembodied hands does not show that the
oblong veil is worn from the mitre minister's neck.

The corrected portrait contains one minister, one mitre, one continuous veil,
and two supporting hands. The veil is visibly suspended behind the neck,
descends in two uninterrupted panels, and folds over both hands at the
mitre's base. No bare hand touches the mitre. The plain cassock and surplice
provide generic minister context; the image does not claim a rank, a cope
exception, veil dimensions, fastening, color, or a transfer sequence.

The corrected PNG is 1024 by 1536 pixels, 8-bit sRGBA, has a transparent
corner pixel, reports `opaque=False`, and contains 28 alpha levels. Its
SHA-256 is
`3cc335dd32d2906ac1f3e64607c5d54c07079d62fc2b972b4350f3b54728bfc2`.
A warm-paper composite shows feathered edges without a rectangular field or
green fringe.

## Disposition

Independent review accepted the three-mitre comparison. It rejected the first
lappet/handling candidate because a loose cloth over disembodied hands did not
establish a neck-hung oblong mitre-minister veil. That precursor remains
retained and marked rejected.

The corrected neck-hung-veil portrait resolves the observed identity defect
and is candidate-ready for independent factual and production re-review. It
must not enter the canonical shared artwork manifest or a publication until
that re-review and the integration lane's object and plate reconciliation are
complete.
