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
8. Assemble review packets, collect role-specific answers through
   `artwork-review-workflow.md`, and resolve every critical and major issue
   through an individually verified correction, redraw, TeX-only change, or
   evidence hold.
9. Print and monochrome-photocopy representative dense, linen, vestment, and
   composition plates.
10. Verify PDF structure, embedded fonts, metadata, extracted text, web reading
   order, and reviewed-build/installed byte identity.
11. Record independent source, factual-artwork, production, and distribution
    approvals separately.

## Artifact ledger

The six installed priestly-review snapshots were rebuilt for two passes,
metadata-checked, rasterized, and visually inspected on every page on
2026-07-27. Build and installed bytes are identical. Each is seven portrait
pages:

| Leaf | Installed PDF SHA-256 |
| --- | --- |
| comprehensive | `54af355b7ea622cff00f8fc702c8b031a8a7a7f80d4edc889cb8f101dbba22dd` |
| altar-server | `7ed33097ef754b004c46d953d1822fecfb7aa065ae31824bb9eb097b915fa365` |
| sacristan | `5a0a58a910f2e0cb169c18f0f9663bb8bc4360df4bf218750bd4f944cdf65dcb` |
| mc-trainer | `dee24bc6d4b357345151ec474b30b59ef684406df83307e87e50659530b9d4c5` |
| general-reader | `50900f6b50973e693a58575acd6397523c838d9863ea1d392f8564d00cb7fd14` |
| pontifical-ceremonies | `140e9f0c915c2d26f64380bfbe53bcf31a8897306e8ab5e26fd9d75acecd699d` |

All six snapshots admit the same 14 records presently capable of the bounded
review gate and print a 24-record omission register. This is an honest
review corpus, not the promised complete dictionary or a claim that the
audience editions have reached their final differentiated scope.

User authorization for this review distribution is the exact session
instruction: “yes”, answering the question whether all six should be prepared
as explicitly labeled priestly-review editions, publishable for expert
evaluation but incomplete and not authoritative. This authorization is
snapshot-specific and does not authorize an authoritative release.

## Full-publish readiness

**Not ready.** The installed files are distributable only as conspicuously
labeled priestly-review copies. They must not be described as complete,
authoritative, independently reviewed, ecclesiastically approved, suitable for
instruction, or approved for ordinary public reliance.

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

Each `web-edition.plan.toml` remains ineligible because this distribution is
PDF-only review. A future final web record must describe the actual reviewed
publication and must not inherit the review snapshot's status.

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

The six stable IDs are registered at `status = review`, retain four unresolved
dictionary gates, and have `approval = null`. They are eligible only for the
private no-index review preview and direct reviewer distribution. Promotion to
ordinary release and exact-PDF authorization require fresh non-review builds
after the gates close; no review hash or authorization carries forward.

The terminal public gates are:

```sh
make check
make check-public-alpha
make public-site
make verify-public-site
```
