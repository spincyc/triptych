# Production manifest

Status: **bounded public alphas**
Audit date: 2026-07-28

## Leaves

| Leaf | Source exists | Canonical records rendered | PDF state | Web edition reviewed | Distribution state |
| --- | --- | --- | --- | --- | --- |
| Comprehensive | Yes | Six alpha records | Built, inspected, and installed | No | Alpha |
| Altar server | Yes | Eighteen alpha records | Built, inspected, and installed | No | Alpha |
| Sacristan | Yes | Six alpha records | Built, inspected, and installed | No | Alpha |
| MC/trainer | Yes | Six alpha records | Built, inspected, and installed | No | Alpha |
| General reader | Yes | Six alpha records | Built, inspected, and installed | No | Alpha |
| Pontifical ceremonies | Yes | Six alpha records | Built, inspected, and installed | No | Alpha |

Each leaf has its own `research/guide-map.md`. Presence of `main.tex`,
generation metadata, an installed PDF, or `web-edition.toml` does not imply
completeness or official approval.

## Required pipeline

1. Close the official and material-culture corpus.
2. Populate and validate canonical object, variant, source, artwork, and plate
   records.
3. Implement strict generation from TOML to ignored `build/` TeX; reject
   unknown fields, dangling IDs, unverified required claims, and unapproved
   artwork.
4. Prove edition selections and explicit exclusions from canonical data.
5. Build enough passes to settle contents, references, and indexes.
6. Reject fatal errors, undefined references, overflows, unresolved layout
   warnings, automatic PDF dates, and nondeterministic trailer IDs.
7. Use only the repository review helpers for rasters/contact sheets; inspect
   every page and every ambiguous figure at full size.
8. Resolve every critical and major internal audit issue through a verified
   correction, redraw, TeX-only change, or evidence hold.
9. Verify PDF structure, embedded fonts, metadata, extracted text, web reading
   order, and reviewed-build/installed byte identity.
10. Record source, rights, safety, reproducibility, mechanical validity, basic
    visual usability, alpha status, and deployment separately.

## Artifact ledger

The six installed historical review snapshots were regenerated and rebuilt
after the artwork-hold and review-admission records were reconciled. Each is six portrait pages and
renders six admitted records with candidate artwork conspicuously marked
`ARTWORK UNDER REVIEW`. Those immutable artifact facts are historical and
non-operative under the current Alpha policy. Automated PDF inspection found six embedded images in
each copy and no image below 300 effective dpi. A bounded every-page visual
screen found no clipping, overlap, spill page, or obvious monochrome
legibility defect.

| Leaf | Installed PDF SHA-256 |
| --- | --- |
| comprehensive | `5f5035d78a27be9df4b89a5d1304f0f45bae5317e554c6f81c80618d130d70a6` |
| altar-server | `56e3660b43bac59022da925eee3200b0bab9558b62909843a326504959b202f6` |
| sacristan | `4d30250f9bf8d53d2b64660d67a27b4eb698a01795b025cebf4e47666631dea0` |
| mc-trainer | `bf7fa938b1d2920e670f243da0e18fce64c3699c590c2ac0b2f6d29e46d35a5c` |
| general-reader | `e2d4b8e2bd9210050a8ee6056d6359d8c09fd7ba00c90a3f2ec1653ae18b8678` |
| pontifical-ceremonies | `6ba98cfd997b99aa138e0a129ffe6124361bf3c14c0f5e68ede3d7a529f9ae7f` |

All six snapshots admit the same six records presently capable of the bounded
alpha admission and print a 37-record omission register from the current 43-record
inventory. This is an honest
alpha corpus, not the promised complete dictionary or a claim that the
audience editions have reached their final differentiated scope.

The altar-server snapshot now contains ten pages and renders four additional
source-audited books-and-supports records: altar Missal, Missal stand, Missal
cushion, and book markers. Its four no-reference, project-generated pencil
assets passed exact-hash, rights, factual-boundary, print, and consumer checks.
The stand and cushion are explicitly mutually alternative; the freestanding
Holy Week lectern appears only as a qualified confusable comparison. Every
page was inspected at rendered size; the PDF has embedded fonts, extractable
text, no overfull boxes or undefined references, and exact build/installed
byte identity. Installed SHA-256:
`5b2f4bae00b864922c520506a852cbb8538a5c354e976f1ea0b4caeea7889a79`.

The altar-server snapshot also uses the consumer-reviewed, dimensioned Met
catalog-exemplar paten plate with a Missal-controlled prepared inset. It
textually distinguishes the Communion plate while preserving the unresolved
period-morphology boundary; it does not admit a Communion-plate drawing.

The next altar-server tranche adds the source-audited Epistle and Gospel books
as the first Solemn-Mass recognition pair. Its TeX-native relational plate uses
generic unornamented graphite-style book symbols rather than representative
bindings. Minister and use labels follow the exact ceiling of *Ritus
servandus* VI.4--5: the subdeacon carries the Epistle book in both hands
against his breast and sings from it; the deacon places and later takes the
Gospel book, and the subdeacon holds it open between the candle-bearing
acolytes while the deacon sings. It does not insert a freestanding lectern into
that ordinary Gospel formation.

The resulting eleven-page bounded alpha was rebuilt for settled references,
rastered through the repository review helper, and visually inspected on every
page and at full size on the new relational plate. It has embedded fonts,
extractable text, no fatal error, undefined reference, overfull box, clipping,
or overlap, and exact build/installed byte identity. Installed SHA-256:
`e8c155d85d07cf9996e18e06301cbb2655c736d0797bbfc79aae341449ea283f`.

The current altar-server tranche adds the directly handled paired altar
cruets. Its exact evidence chain comprises the checked 1914 Gorham catalog
leaves N36-N37, exact Met Open Access metadata and images for objects 467483
and 200141, and the existing Missal/manual handling controls. The
project-generated grayscale plate teaches only a generic hand-scale pair with
stable bases, pouring lips, and graspable handles. Wine/water labels and the
local-variation boundary remain in TeX; the art contains no fixed order,
marking, material, ornament, tray, closure, liquid, or semantic mark. The
earlier household-decanter-like single asset remains held.

The resulting 13-page bounded alpha was built for two settled passes, rastered
through the repository review helper, and visually inspected on every page and
at full size on the new paired-cruets page. It has embedded fonts, extractable
text, no fatal error, undefined reference, overfull box, clipping, overlap, or
spill page, and exact build/installed byte identity. Installed SHA-256:
`8732e866bcf195372ce59d4401cf7d5f43ed2b615e7494da7df248bec1166efe`.

The next altar-server tranche splits the former grouped incense candidate into
stable `obj-incense-boat` and `obj-incense-spoon` records. Exact 1962 Missal
controls at *Ritus servandus* IV.4 and VII.10 establish the distinct
*navicula* and *cochlear* and the named deacon-to-celebrant relationship;
VII.10 repeats the boat service without repeating the spoon term.
Met Open Access object 236950 supplies one dated boat-and-spoon exemplar and
their catalog lengths without being generalized into a ritual norm. Loose
incense remains consumable material, not a peer vessel.

The generated pencil plate is a non-destructive successor to the held
candidate: unsupported granular contents were removed, while the supportable
open boat and separate spoon remain. Its material and decorative morphology
are explicitly illustrative. The page teaches the local/model boundary for a
lay boat-bearer and gives hot-thurible safety without charcoal-lighting,
loading, or fire-tending instructions.

The resulting 14-page bounded alpha was rebuilt, rastered through the
repository review helper, and visually inspected on every page and at full
size on the new incense spread. It has embedded fonts, extractable text, no
fatal error, undefined reference, overfull box, clipping, overlap, or spill
page, and exact build/installed byte identity. Installed SHA-256:
`1605612c27b5b854d1809bac432dfa8b89345e1a1d7ba95e29a5f9149861b229`.

The current convention permits a bounded alpha when source integrity, rights,
safety, reproducibility and identity, mechanical validity, and basic visual
usability pass.

The next altar-server incense tranche adds the thurible as a sixteenth
source-audited record. Exact 1962 Missal loci control the object identity and
named thurifer relationships. Benziger Brothers' 1927 catalog, exact PDF
SHA-256
`b09d9bf5920d3a0e137519e53e8064fb42a6e0702aa26779edf2178200df8ab0`,
controls the neutral component-recognition drawing and bounded scale;
Metropolitan Museum of Art object 464340 remains a variation control only.
The project-generated graphite figure visibly separates three bowl-support
chains from the central lid-lifting chain, contains no text or operational
action, and makes no material, ornament, or universal-silhouette claim.
The entry limits instruction to a trained thurifer, cold empty rehearsal,
upper-ring and chain control, and an appointed safe resting place. It gives no
charcoal-lighting, loading, extinguishing, or swinging procedure.

The resulting 15-page bounded alpha was rebuilt for settled passes, rastered
through the repository review helper, and visually inspected on every page
and at full size on the new thurible page and dense terminal pages. The
thurible's three support chains and separate central lid chain remain
unambiguous at rendered size. The PDF has embedded fonts, extractable text, no
fatal error, undefined reference, overfull box, clipping, overlap, or spill
page, and exact build/installed byte identity. Installed SHA-256:
`b8de0ef1588aabe26390e781b20a81460205f3ad3262d1b35d30a66270e411b3`.

The next altar-server carrying tranche adds the source-audited acolyte
candlestick and optional processional cross while correcting the retained
torch record. The exact 1962 Missal controls the two candle-bearing acolytes;
Fortescue's exact 1917 first edition controls the footed/self-standing
candlestick distinction, the footless elevation torch, the non-self-standing
processional-cross staff, and the cross's optional local status at a priest's
High Mass. The existing empty-candlestick drawing is reused only as
representative morphology. The current footed torch drawing remains held and
is not rendered.

The resulting 17-page bounded alpha was rebuilt for settled passes, rastered
through the repository review helper, and visually inspected on every page and
at full size on both new pages. The PDF has embedded fonts, extractable text,
no fatal error, undefined reference, overfull box, clipping, overlap, or spill
page, and exact build/installed byte identity. Its 7,319,228-byte size reflects
the accumulated reviewed grayscale artwork in this image-dominant alpha; no
source artifact is embedded. Installed SHA-256:
`9d333dab8fef9b860f1fa90fccc44156f3427e1ba116cd944c968ece1d1b7aed`.

The elevation-torch follow-up replaces the held footed candidate with a fresh
project-generated graphite figure whose narrow lower shaft has no foot, base,
stand, rack, actor, flame, or handling pose. Fortescue's exact 1917 printed
pp. 17 and 89--90 control the non-self-standing morphology, Elevation-service
identity, and distinction from the acolytes' candlesticks. The exact 1962
Missal, *Ritus servandus* VIII.8, is recorded as a negative control: it names
the thurifer at the elevations but does not name torchbearers or torches. The
entry therefore gives no universal number, arrangement, height, grip, or
handling method and confines safety text to a non-operational supervision and
clearance boundary.

The resulting 18-page, nineteen-object bounded alpha was built for settled
passes, rastered through the repository review helper, and visually inspected
on every page. The elevation-torch page and both terminal pages were also
inspected at full rendered size. The footless lower endpoint, unlit state,
object identity, labels, and safety boundary are unambiguous; no content is
clipped or overlapped. The PDF has embedded fonts and extractable text, and
the log has no fatal error, undefined reference, or overfull box. Build and
installed bytes are identical at 7,630,753 bytes. Installed SHA-256:
`206e14d0508feeb2d5cb64e80eca1ab17f2c16d25266d5450ab5e1abd094d137`.

The Holy Week lectern tranche promotes `obj-lectern` to `source-audited` and
adds it as the twentieth rendered record without importing it into the
Low-Mass core. The altar-server binding identifies Palm Sunday n. 8, Good
Friday nn. 7, 9--10, and Easter Vigil nn. 13 and 13a in the exact 1962 Missal
facsimile. The standalone page distinguishes the freestanding support from
the low altar Missal stand and teaches only the rites' checked bare and
white-cloth-covered states. The retained pencil figure is project-generated
and rights-cleared; its pedestal construction, material, height, ornament,
and silhouette are labelled illustrative, and no universal position or
server setup method is inferred.

The resulting 19-page, twenty-object bounded alpha was built for settled
passes, rastered through the repository review helper, and visually inspected
on every page. The standalone lectern page and both terminal pages were also
inspected at full rendered size. The object silhouette, low-stand distinction,
ritual-state labels, handling boundary, source key, and illustrative-morphology
notice are legible and unambiguous; no content is clipped or overlapped. The
PDF has embedded fonts and extractable text, and the log has no fatal error,
undefined reference, overfull box, or unresolved LaTeX warning. Build and
installed bytes are identical at 7,633,995 bytes. Installed SHA-256:
`d85fc4cbfdeee6428d5e88d1b043f7ffab98c4a8832a693380460c53e199699c`.

## Alpha readiness

Each rebuilt leaf is alpha-eligible when the six current concerns pass. The
bounded editions do not claim completeness or official liturgical status.

## Publication-control handoff

The six review leaves now have `main.tex`, installed PDFs, catalog links, and
`status = review` publication records with null approvals. Their authoritative
release controls remain deferred until the recorded gates close.

### Stable leaf IDs

```text
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/comprehensive
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/altar-server
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/sacristan
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/general-reader
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies
```

Each `web-edition.toml` remains ineligible only because no matching web
rendering has passed the mechanical and visual checks.

### Build, review, and installation

Build and raster each stable ID with:

```sh
make review-doc DOC=<stable-leaf-id>
```

After every page, ambiguous figure, PDF structure, font, metadata, and
extracted-text check has been recorded, install the exact checked bytes with:

```sh
make install-doc DOC=<stable-leaf-id>
```

The installed paths are the stable IDs mirrored below `doc/gpt/`, with a
`.pdf` suffix. Verify byte identity between each `build/gpt/` PDF and its
installed mirror.

### Catalog

Only after all six installed files exist, add an **Illustrated Roman Sanctuary
Dictionary** subsection to `library/traditional-latin-mass.md`. Give the
comprehensive volume the primary row and identify the other five as
use-derived editions. Link each title to:

```text
../doc/gpt/<stable-leaf-id>.pdf
```

The row must retain the 1962 horizon and held or incomplete status unless the
completeness gate has actually closed. `README.md` and `LIBRARY.md` already
route readers through `library/traditional-latin-mass.md`; revise their short
section descriptions only if the dictionary is meant to be advertised at the
top-level index.

### Source inventory

After final `main.tex`, web records, source bindings, and rendered-source
files exist, refresh the inventory and review the resulting dictionary owner
and six publication units:

```sh
scripts/source-inventory refresh --audited-on YYYY-MM-DD
scripts/source-inventory classify \
  --review src/sources/inventories/classification-review-v1.toml
scripts/source-family-migration refresh --audited-on YYYY-MM-DD
make check-sources
```

The owner remains
`owner.liturgy.roman-rite.1962.roman-sanctuary-dictionary`. Each publishable
leaf must become its own document entry and name that owner with a
`source-owner` relationship; leaf-local records remain locally owned. Review
new source-family presence rather than mechanically marking it screened.

### Release manifest and exact-byte approval

The six stable IDs are bounded alpha publications. Completeness work continues
without creating an external-review or authoritative-release gate.

The terminal public gates are:

```sh
make check
make check-public-alpha
make public-site
make verify-public-site
```
