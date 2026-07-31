# Legacy Source Inventory

This directory records migration coverage for source-bearing material that
predates the reusable source library. Its schema is deliberately separate from
source manifest schema version 1. Inventory rows describe what the repository
contains and what work remains; they do not assert that a source was acquired,
searched, inspected, or verified under the source-library contract.

## Coverage boundary

Each provider branch keeps its own inventory record (`publications-v1.toml`
for `gpt`, `<provider>-publications-v1.toml` for later providers), and each
record's publication universe is every `src/<provider>/**/main.tex`, exactly
as discovered by the Makefile. A complete inventory also includes explicit nonpublication
research owners and source-bearing records outside publication `research/`
directories, including proper-verification records, retained locating aids,
edition registries, shared received texts, and other profile-authorized owner
records.

Ownership is explicit. Do not infer evidence inheritance merely by walking to
the nearest ancestor. Curriculum packets, derived prayer companions,
mechanically derived theological companions, proper instances, and shared
render fragments each retain their documented relationship kind. A render
dependency is not automatically an evidence dependency.

Every textual authoring file below a provider branch of `src/`, except
provider-neutral `src/common/` typesetting primitives and generated metadata
declarations, is part of the conservative source-review surface. This deliberate superset prevents a claim,
citation, or audit from evading coverage because its filename was unexpected.
Each inventoried file records its repository-relative path and SHA-256. The
inventory checker recomputes the publication and source-review surface and
rejects missing rows, extra rows, stale hashes, broken owners, and a changed
snapshot. Generated discovery reports belong below ignored `build/sources/`.

The structural baseline is created and checked with:

```sh
tools/tpt source-inventory bootstrap \
  src/sources/inventories/publications-v1.toml --audited-on YYYY-MM-DD
tools/tpt source-inventory bootstrap-classification-review \
  src/sources/inventories/classification-review-v1.toml \
  --audited-on YYYY-MM-DD
tools/tpt source-inventory classify
tools/tpt source-inventory check
```

`bootstrap` deliberately begins every publication at `records-enumerated` with
an `unresolved` source category. It is a trace-bullet generator, not a semantic
classifier, and must not overwrite a reviewed inventory without examining the
diff. `classify` requires the exact publication set pinned in
`classification-review-v1.toml`, applies the broad source strata recorded there
for each exact publication, and fails closed if a new publication has not been
added to that review checkpoint. Bootstrapping a new checkpoint emits an
`unresolved` row for every publication. Refreshing an existing checkpoint
preserves its reviewed rows, drops publications no longer present, and adds
only newly discovered publications as `unresolved`; replace every placeholder
through an actual source-record audit before running `classify`. The review
file pins both the exact publication set and the complete category map, so
later tool changes cannot silently reinterpret an old review.
These strata say which kinds of source occur in the publication's
records; they are not a claim that every individual source has already been
disaggregated or canonicalized. `check` is read-only and validates the tracked
review state as well as its current paths and hashes. Once any publication is
categorized, `check` also requires the review checkpoint and rejects a category
row that diverges from its pinned reviewed value even if the inventory's own
snapshot has been recomputed.

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

## Reviewed family migration ledger

`source-family-migration-v1.toml` is that separate planning contract. It pins
the exact publication inventory, classification review, and canonical-manifest
catalog; records reviewed decisions about recurring source families; and gives
every publication or nonpublication owner a hash of its complete owned file surface. It remains
outside source-manifest schema version 1: `family.*` IDs cannot be cited by a
publication or used as source-binding targets.

Family rows keep identity confidence and gaps, candidate-artifact
availability, proposed storage, candidate-artifact rights review, mutability,
the legacy evidence ceiling, priority, and migration disposition independent.
`canonical_ids` is the exhaustive sorted membership already present in the
central source library for that family, not merely a suggested entry point.
`all-known-artifacts-reviewed` records completion of that rights review; it
does not mean that redistribution was cleared, and the canonical artifact's
own rights status remains controlling. A reviewed family decision may remain
in the ledger with no current presence so refresh cannot silently erase the
migration backlog when its last known trace disappears.
An evidence ceiling describes only what the pinned legacy records could support
without new source work; it is not a source-library evidence state. Stored
trace paths are replayable record-level discovery evidence. They do not prove
that every mention in the record was found, that two citations have the same
edition, or that the family identity applies without review.

Every review unit begins `pending`. `family-screened` means the exact pinned
owner surface was reviewed for recurring-family presence; it still does not
mean atomic citations were enumerated. The schema therefore requires
`atomic_citation_coverage = false` even when all units are screened. Shared
owner reuse is derived through the explicit inventory ownership edges rather
than copied into every consumer.

The family fields use these fixed meanings:

- `artifact_availability` distinguishes records already `canonicalized`, a
  known `candidate-complete` or `candidate-partial` artifact, a
  `citation-only` lead, an `unavailable` or `unknown` artifact, and a `mixed`
  cluster whose members differ.
- `storage_plan` records the intended `tracked`, `remote`, `restricted`,
  `unavailable`, or `unknown` treatment. It is a plan, not evidence that a
  payload was acquired.
- `rights_review` is `all-known-artifacts-reviewed`, `partially-reviewed`,
  `unreviewed`, or `blocked`. Review completion never overrides the rights
  status on an artifact manifest.
- `mutability` is `fixed`, `officially-mutable`, `serial`, `mixed`, or
  `unknown`. Every non-fixed family needs an operational `freshness_rule`.
- `evidence_ceiling` describes the strongest replayable legacy support:
  `work-only` identifies only the intellectual work; `edition-locus` names an
  edition and locator without pinning exact bytes; `artifact-pin` identifies
  exact artifact bytes; `passage-pin` also identifies a checked passage;
  `bounded-corpus` records an exact searched scope; and `mixed` means members
  have different ceilings. These values are not current evidence states.
- `disposition` chooses `bind-existing`, `canonicalize`,
  `split-then-canonicalize`, `research-identity`, `research-rights`,
  `retain-local`, `keep-lead`, or `defer`.

`trace_patterns` are case-insensitive Python regular expressions evaluated
with DOTALL semantics. Every stored trace path must be owned by its review unit
and match at least one pattern. A screened unit pins a
`family_screening_snapshot` covering family identity boundaries and trace
patterns; adding a family or changing those screening semantics returns the
unit to pending on refresh. Migration-only changes such as priority or storage
do not invalidate source-surface screening.

That reset is the default and is correct whenever the new family's semantics
were not actually carried through the screened surface. Refresh compares each
unit's pinned snapshot against the one computed from the ledger as it stands on
disk, so an operator who has genuinely rescreened may keep the completed review
by doing the rescreen and the re-pin together, by hand, before running refresh:
evaluate the added family's `trace_patterns` over every owner's pinned files,
record any match as `family_presence`, and only then write the new snapshot onto
each unit that is still `family-screened`. Re-pinning without that scan asserts
a screening that never happened, and the tool cannot detect the difference.
Choose narrow patterns for exactly that reason — a bare surname or a common
title matches unrelated prose and manufactures presence a later reader will
trust. The top-level
`canonical_catalog_snapshot` hashes every canonical source manifest's path and
bytes, so new records or changes to rights, storage, relationships, hashes, or
other manifest metadata force a fresh ledger review.

Use the standalone tool directly:

```sh
tools/tpt source-family-migration bootstrap \
  src/sources/inventories/source-family-migration-v1.toml \
  --audited-on YYYY-MM-DD
tools/tpt source-family-migration check
tools/tpt source-family-migration check --require-family-screened
tools/tpt source-family-migration refresh --audited-on YYYY-MM-DD
tools/tpt source-family-migration refresh --audited-on YYYY-MM-DD \
  --accept-canonical-catalog
```

Bootstrap creates only pending review units and performs no semantic family
classification. Refresh preserves family decisions and unchanged review
units. A new or owner-surface-changed unit becomes pending; an existing path is
retained only when it remains owned by that unit and still replays as trace
evidence. Refresh never discovers or adds a new family presence. Review and add
that presence explicitly.

A canonical-manifest addition or edit intentionally blocks ordinary refresh.
First run `tools/tpt source-library validate`, review the changed manifests, and
update their family membership. Version 1 uses a conservative global catalog
checkpoint: every family with canonical IDs must then be re-reviewed and set
to a `reviewed_on` equal to the new ledger audit date, even when its own
manifests did not change. Then use
`--accept-canonical-catalog`. That explicit acceptance seals reviewed ledger
edits as the operator's semantic-review checkpoint, independently reruns the
full source-library validator, requires every current canonical ID to belong
to exactly one family, updates the catalog pin, and still applies the ordinary
surface-refresh and screening-invalidation rules. Without the flag, catalog
drift is never adopted silently.

For routine maintenance, refresh the publication inventory first, complete any
new classification review and rerun `classify` when needed, then refresh this
family ledger. Inspect newly pending or surface-changed units and add newly
discovered family presence manually; neither refresh command performs that
semantic judgment. Finish with `make check-sources`, which permits explicit
pending work while checking all three contracts. Reserve
`make check-source-family-screening` for the explicit family-screening
completion audit.

Family-specific review records may preserve the human semantic audit that
precedes canonicalization and binding. They supplement the ledger rather than
becoming source manifests or evidence states. The first such record is the
[Catechism family review](catechism-family-review-2026-07-23.md), which
disaggregates the work, official expressions, amendment act, delivery
artifacts, rights boundary, 42 positive owner occurrences, and inherited
consumers before migration.

## Migration states

Publication inventory states describe migration progress only:
`records-enumerated`, `sources-categorized`, `canonicalization-planned`,
`partially-migrated`, and `bindings-covered`. They must not reuse the
source-library evidence vocabulary. Legacy prose may be preserved verbatim for
audit purposes, but words such as “verified” in that prose do not create a
fingerprint, passage check, or publication binding.
