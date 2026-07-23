# Legacy Source Inventory

This directory records migration coverage for source-bearing material that
predates the reusable source library. Its schema is deliberately separate from
source manifest schema version 1. Inventory rows describe what the repository
contains and what work remains; they do not assert that a source was acquired,
searched, inspected, or verified under the source-library contract.

## Coverage boundary

The publication universe is every `src/gpt/**/main.tex`, exactly as discovered
by the Makefile. A complete inventory also includes explicit nonpublication
research owners and source-bearing records outside publication `research/`
directories, including proper-verification records, retained locating aids,
edition registries, shared received texts, and other profile-authorized owner
records.

Ownership is explicit. Do not infer evidence inheritance merely by walking to
the nearest ancestor. Curriculum packets, derived prayer companions,
mechanically derived theological companions, proper instances, and shared
render fragments each retain their documented relationship kind. A render
dependency is not automatically an evidence dependency.

Every textual authoring file below `src/gpt/`, except global `common/`
typesetting primitives and generated metadata declarations, is part of the
conservative source-review surface. This deliberate superset prevents a claim,
citation, or audit from evading coverage because its filename was unexpected.
Each inventoried file records its repository-relative path and SHA-256. The
inventory checker recomputes the publication and source-review surface and
rejects missing rows, extra rows, stale hashes, broken owners, and a changed
snapshot. Generated discovery reports belong below ignored `build/sources/`.

The structural baseline is created and checked with:

```sh
scripts/source-inventory bootstrap \
  src/sources/inventories/publications-v1.toml --audited-on YYYY-MM-DD
scripts/source-inventory check
```

`bootstrap` deliberately begins every publication at `records-enumerated` with
an `unresolved` source category. It is a trace-bullet generator, not a semantic
classifier, and must not overwrite a reviewed inventory without examining the
diff. `check` is read-only and validates the tracked review state as well as its
current paths and hashes.

## Classification

Use broad intellectual families such as Scripture, liturgical books,
magisterial sources, canon law, patristic works, scholastic works, classical
works, prayer and devotional sources, historical primary sources, archival
material, current institutional sources, datasets and surveys, secondary
scholarship, finding aids, repository-internal material, and unresolved
candidates.

Keep these independent from:

- identity confidence and missing work, edition, artifact, or locus data;
- artifact availability and proposed tracked, remote, restricted, unavailable,
  or unknown disposition;
- mutability and currentness obligations;
- rights-review state;
- the strongest evidence state the legacy record can actually support; and
- the reviewed action: bind an existing source, canonicalize a shared family,
  retain a local judgment, keep a lead, or conduct more research.

An URL host is not an intellectual family. Exact URL, DOI, citation, or
byte-hash clustering supplies trace bullets for review and never authorizes an
automatic identity merge.

The publication inventory proves structural coverage of the review surface and owners. A
separate reviewed occurrence and family ledger may disaggregate citations
within those files. Until that ledger is complete, do not describe structural
coverage as atomic citation coverage.

## Migration states

Publication inventory states describe migration progress only:
`records-enumerated`, `sources-categorized`, `canonicalization-planned`,
`partially-migrated`, and `bindings-covered`. They must not reuse the
source-library evidence vocabulary. Legacy prose may be preserved verbatim for
audit purposes, but words such as “verified” in that prose do not create a
fingerprint, passage check, or publication binding.
