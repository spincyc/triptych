# Triptych Source Library

This provider-neutral tree gives reusable external sources one canonical work,
edition, artifact, segment, passage, and corpus identity. It is governed by
[`guidance/sources.md`](../../guidance/sources.md).

Publication-local interpretations and evidence judgments do not move here.
They remain in each publication's research records and are connected to this
library through `research/source-bindings.toml`.

Migration coverage under `inventories/` has its own audit schema and checker.
It inventories legacy records and ownership without turning their prose labels
into source-manifest evidence; see
[`inventories/README.md`](inventories/README.md).

Schema version 1 remains frozen exactly as exercised by the 2026-07-22
complete-source City of God tracer and its consumer, rights, query, and impact
reviews. Schema version 2 is a narrow additive layer for a bounded constituent,
including one whose exact artifact is truthfully owned by a different container
work. It adds segment records, optional exact artifact page counts, and
passages and bindings that can name those segments; it does not reinterpret
version 1 or change its artifact-only corpora. During migration,
`scripts/source-library validate` checks only records already entered into
this tree and publication binding files that already exist. Generated indexes
and reports belong in ignored `build/sources/`.

## Commands

```sh
make check-sources
scripts/source-library validate
scripts/source-library fingerprint SOURCE_ID
scripts/source-library uses SOURCE_ID
scripts/source-library impact SOURCE_ID
scripts/source-library search SOURCE_ID QUERY
scripts/source-library search SOURCE_ID QUERY --count
```

The command-line queries are deterministic and read-only. They compute the
current graph from tracked manifests rather than treating a generated database
as authoritative. `fingerprint` prints the review pin required by bindings
whose states go beyond `cataloged`; it deliberately remains usable when an
otherwise valid graph contains stale binding fingerprints so those bindings can
be reviewed and updated.
`impact` retains each affected binding's source ID, loci, role, and states so
distinct review obligations in one publication remain distinguishable.

The built-in search is a case-insensitive literal search by default. It tests
each LF-delimited physical UTF-8 line independently and does not strip XML
markup, normalize whitespace, cross line boundaries, stem words, or infer
synonyms. Its empty result supports only that narrow raw-text statement.
Searches bound as evidence record a canonical mode and matching-line count that
validation replays.
Negative-search bindings use `text/plain` search representations; create and
register an exact normalized derivative when markup or layout affects content,
and record the actual method and limitations in the binding.
Artifact and corpus searches use their exact registered members. A segment
search uses only its validated 1-based physical-line ranges while still
rechecking the whole controlling artifact's hash and size; a page-only segment
cannot be searched by these raw-line modes. A passage search uses only its
validated physical-line ranges and remains bounded by its artifact or segment
controller.

`make check-sources` runs the three normal read-only gates in order: source
library validation, exhaustive inventory replay, and non-completion family
ledger validation. It permits review units that are explicitly still pending.
Use `make check-source-family-screening` only when auditing whether every
review unit has completed family screening; even that strict gate does not
claim atomic citation coverage. The focused tool regression targets are
`make check-source-library`, `make check-source-inventory-tool`, and
`make check-source-family-migration-tool`.

## Layout

```text
works/<namespace>/<work>/work.toml
works/<namespace>/<work>/editions/<edition>/edition.toml
works/<namespace>/<work>/editions/<edition>/artifacts/<artifact>/artifact.toml
works/<namespace>/<work>/editions/<edition>/segments/<segment>.toml
works/<namespace>/<work>/editions/<edition>/passages/<passage>.toml
corpora/<corpus>.toml
inventories/
schema/
```

Only artifacts whose manifest records an affirmative distribution basis may
carry tracked source bytes. A payload stays beneath its own manifest, is hashed
as exact bytes without Git line conversion, and has exactly one owner. Exact
acquired bytes and normalized derivatives are separate artifacts. Searchable
corpora list exact hashed artifacts; they never expand merely because a new
artifact is later attached to the same work or edition. When exact bytes embed
a relative companion filename, `support_artifacts` maps that literal reference
to another exact artifact without duplicating it or adding it to text search;
the reference is an undecoded, canonical relative POSIX path.

A segment has no payload, storage disposition, or independent rights grant.
It lives under the constituent's edition, points to exactly one controlling
artifact (including a container artifact owned by another work), pins that
artifact's hash, and inherits its storage and rights limits. Structural
ownership follows the segment's edition; fingerprints and impact also follow
the cross-work artifact evidence edge. Version 1 corpora continue to list only
exact hashed artifacts and do not accept segment members.
