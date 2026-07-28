# Communion plate source audit

Audit date: 2026-07-28
Scope: one source-bounded altar-server comparison entry at the 1962 horizon

## Liturgical control

The exact 1962 Vatican typical *Missale Romanum*, *Ritus servandus* X.7,
printed p. LXIII / artifact PDF p. 65, names the distinct *patina* placed
beneath communicants' chins and directs the celebrant to put any fragments
found upon it into the chalice. It controls identity, location, and function.
It does not establish a handle, raised rim, dimensions, material, ornament,
server assignment, or universal morphology.

## Material-culture control

The exact Internet Archive Additional Text PDF for *Hirten Church Goods 1952*
has SHA-256
`ccd22db7a72a5b3e38a9e4bb9ff8fec03ebc31966d883edcfaf5e5be6d66dcb3`.
Printed p. 111 / artifact PDF p. 113 was rendered and visually inspected.
Internet Archive metadata for item `hirten-religious-goods-1952` supplies a
Creative Commons Public Domain Mark 1.0 URL; Triptych records that host
metadata and retains the 10,388,490-byte scan remotely.

The page labels both products “Communion Paten”:

- No. 7701: round, 7 3/4 inches in diameter, metal gold-plated, with a wood
  handle; and
- No. 7702: round, 7 inches in diameter and 9 1/2 inches with handles, metal
  gold-plated.

The page image visibly distinguishes a one-handle from a two-handle form.
These are dated commercial exemplars, not normative ritual specifications.
The consumer drawing selects only the plain round catching surface and one
projecting wood handle of No. 7701. It does not encode gold color, exact rim
height or depth, ornament, material apart from the visibly distinct handle,
or the two-handle form.

## Comparison and handling ceiling

The smaller handleless priest's paten reuses the already controlled shallow
Metropolitan Museum of Art exemplar evidence. The plate is explicitly not to
common scale and shows neither object on a chalice. TeX, not the raster, owns
the under-chin function, dated catalog dimensions, two-handle variant,
conditional handling, priest-paten distinction, lavabo/tray confusables, and
fragment safety.

The selected Low-Mass action model supplies the server-facing instruction:
when assigned, keep the plate level beneath the communicant's chin without
touching the communicant; fragments remain for the priest. This model-specific
assignment is not promoted into a universal rubric.

## Verification result

The exact source records and local binding validate. The generated asset's
received and normalized hashes, exact prompt, source controls, omissions,
corrections, rights, and consumer are recorded in `artwork-manifest.toml`.
The 30-page PDF was built to settled references, visually inspected on every
page and at full size on the new entry, and installed byte-identically.

## Isolated generic-edition derivative

The five generated canonical-alpha editions use a versioned isolated
derivative rather than repeating the priest's paten on the Communion-plate
page. The bespoke altar-server page remains the sole consumer of the original
comparison raster and retains its explicit not-to-common-scale teaching.

The derivative crops the reviewed comparison at `1050x680+20+120`, excluding
the paten, then gives the crop a soft transparent perimeter. Its exact
deterministic ImageMagick command is recorded in `artwork-manifest.toml`.
Grayscale sample absolute error against the exact source crop is zero: only
alpha changes. The resulting 1050-by-680 8-bit grayscale-alpha PNG is 453,342
bytes with SHA-256
`062e1473023a680d3f54b53af6efa55bf3ac6a4cd6812ee5b5b1b78f048bdb53`.
This separation adds no morphological or liturgical claim.
