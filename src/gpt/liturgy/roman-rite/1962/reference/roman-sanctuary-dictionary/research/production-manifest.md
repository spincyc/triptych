# Production manifest

Status: **bounded public alphas**
Audit date: 2026-07-28

## Leaves

| Leaf | Source exists | Canonical records rendered | PDF state | Web edition reviewed | Distribution state |
| --- | --- | --- | --- | --- | --- |
| Comprehensive | Yes | Six alpha records | Built, inspected, and installed | No | Alpha |
| Altar server | Yes | Ten alpha records | Built, inspected, and installed | No | Alpha |
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

The current convention permits a bounded alpha when source integrity, rights,
safety, reproducibility and identity, mechanical validity, and basic visual
usability pass.

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
