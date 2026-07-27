# Production manifest

Status: **scaffold only; not approved for full publication**
Audit date: 2026-07-27

## Leaves

| Leaf | Source exists | Canonical records rendered | PDF built/reviewed/installed | Web edition reviewed | Release state |
| --- | --- | --- | --- | --- | --- |
| Comprehensive | Yes, prototype | No | No recorded completed gate | No | Hold |
| Altar server | Yes, prototype | No | No recorded completed gate | No | Hold |
| Sacristan | Yes, prototype | No | No recorded completed gate | No | Hold |
| MC/trainer | Yes, prototype | No | No recorded completed gate | No | Hold |
| General reader | Yes, prototype | No | No recorded completed gate | No | Hold |
| Pontifical ceremonies | Yes, prototype | No | No recorded completed gate | No | Hold |

Each leaf still requires its own `research/guide-map.md` and any required
source bindings. Presence of `main.tex`, generation metadata, or
`web-edition.toml` is not publication approval.

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
8. Print and monochrome-photocopy representative dense, linen, vestment, and
   composition plates.
9. Verify PDF structure, embedded fonts, metadata, extracted text, web reading
   order, and reviewed-build/installed byte identity.
10. Record independent source, factual-artwork, production, and distribution
    approvals separately.

## Artifact ledger

No dictionary PDF identity, page count, installed byte hash, raster
normalization result, print-test result, or approved web snapshot is recorded
as complete in this manifest.

## Full-publish readiness

**Not ready.** The present source tree is a structural prototype prepared for
future production. It must not be described as complete, source-audited,
independently reviewed, ecclesiastically approved, or distribution-approved.

## Publication-control handoff

The following controls are intentionally deferred until all six leaves have
passed the profile gate. Performing them against scaffold sources would create
broken catalog links or imply a publication state that does not yet exist.

### Stable leaf IDs

```text
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/comprehensive
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/altar-server
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/sacristan
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/mc-trainer
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/general-reader
liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/pontifical-ceremonies
```

For each leaf, replace `scaffold.tex` with the reviewed `main.tex` entry point
and replace `web-edition.plan.toml` with a final `web-edition.toml`. The final
web record must describe the actual reviewed publication. It must not retain a
`source-hold` rationale after the source and artwork gates have closed.

### Build, review, and installation

Build and raster each stable ID with:

```sh
make review-doc DOC=<stable-leaf-id>
```

After every page, ambiguous figure, print sample, monochrome photocopy, PDF
structure, font, metadata, and extracted-text check has been recorded, install
the exact reviewed bytes with:

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

After catalog and installed PDFs exist, add each stable ID to the exhaustive
manifest in a nonpublic state:

```sh
make add-publication \
  ID=<stable-leaf-id> \
  CATALOG=library/traditional-latin-mass.md \
  STATUS=hold
```

Run `make check-release-bindings` and `make prepare-public-alpha`. Promotion
from `hold` and exact-PDF authorization occur only after the six installed
hashes and all outstanding gates have been reviewed. The user's instruction
to approve and prepare for full publication authorizes that later release
operation, but it does not make scaffold or unreviewed bytes approvable.
Record the exact operator instruction in the dated release supplement through
the repository approval command; do not invent a broader approval note.

The terminal public gates are:

```sh
make check
make check-public-alpha
make public-site
make verify-public-site
```
