# Production manifest

Status: **public-alpha priestly-review copies; not authoritative releases**
Audit date: 2026-07-27

## Leaves

| Leaf | Source exists | Canonical records rendered | PDF state | Web edition reviewed | Distribution state |
| --- | --- | --- | --- | --- | --- |
| Comprehensive | Yes | Six review-eligible records | Built and installed; production review remains open | No | Public-alpha priestly review |
| Altar server | Yes | Six review-eligible records | Built and installed; production review remains open | No | Public-alpha priestly review |
| Sacristan | Yes | Six review-eligible records | Built and installed; production review remains open | No | Public-alpha priestly review |
| MC/trainer | Yes | Six review-eligible records | Built and installed; production review remains open | No | Public-alpha priestly review |
| General reader | Yes | Six review-eligible records | Built and installed; production review remains open | No | Public-alpha priestly review |
| Pontifical ceremonies | Yes | Six review-eligible records | Built and installed; production review remains open | No | Public-alpha priestly review |

Each leaf has its own `research/guide-map.md`. Presence of `main.tex`,
generation metadata, an installed review PDF, or `web-edition.toml` is not
authoritative-release approval.

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

The six installed priestly-review snapshots were regenerated and rebuilt
after the review-admission gate was tightened. Each is six portrait pages and
renders six admitted records with candidate artwork conspicuously marked
`ARTWORK UNDER REVIEW`. Automated PDF inspection finds six embedded images in
each copy and no image below 300 effective dpi. Full-size visual, physical
print, and monochrome-photocopy review of these exact snapshots remains open.

| Leaf | Installed PDF SHA-256 |
| --- | --- |
| comprehensive | `517d5c3d517cbf9395fef165c817b8751bd879bae28f6a1b42bb932a1379b1d6` |
| altar-server | `02be3ff41f7fffe88d023012473de6efc0fe38f64190dc7714239b944dd486cc` |
| sacristan | `b2dd757c495941dc82cdef981aac394ab746305777fd5c029a117e41957bb406` |
| mc-trainer | `7d1373a6cc522cddc5795fff10a63dd8454b86ee5924a2a10fcb2d88006f54f1` |
| general-reader | `c831b1e852b6378f0600f9366543ca046f8964db0a77c6bd393f69bbe18004c7` |
| pontifical-ceremonies | `aebfc52d1aec0b04cf761760f0a55f8db36806bd7c1c17eec1d1ed08a0445c1e` |

All six snapshots admit the same six records presently capable of the bounded
review gate and print a 32-record omission register. This is an honest
review corpus, not the promised complete dictionary or a claim that the
audience editions have reached their final differentiated scope.

Those exact installed snapshots predate five subsequently added historical
`identified` records. The canonical structured inventory now contains 43
records. With the admission set unchanged, fresh generator output would retain
the six admitted records and list 37 omissions. This ledger records no such
regeneration or rebuild; the hashes above remain identities of the installed
six-plus-32 snapshots.

The project convention now makes every installed review paper publicly
discoverable in the public alpha. That distribution rule does not promote a
record, close an open gate, authorize operational reliance, or authorize an
authoritative release.

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

Each `web-edition.toml` remains ineligible because this distribution is
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

The six stable IDs are registered at `status = review`, retain their
unresolved dictionary gates, and have no authoritative-release approval. They
are eligible for conspicuously labelled public-alpha review distribution.
Promotion to authoritative release and exact-PDF authorization require fresh
non-review builds after the gates close; no review hash or distribution
decision carries forward.

The terminal public gates are:

```sh
make check
make check-public-alpha
make public-site
make verify-public-site
```
