# Source Schema Changelog

## Papal collection inventory ownership — added 2026-10-26

The source-tree validator recognizes the exact catalog, archive, source-link,
publication-approval, typesetting-manifest, and page-review comparison JSON names documented in
`papal-documents/README.md`, with their versioned ownership envelopes, and
immediate collection Markdown records. The catalog/acquisition/typesetting
tools own semantic checks. Unknown names, nested files, malformed JSON,
duplicate keys, incorrect envelopes and unmanifested payloads remain rejected.
These project-created inventories do not add source record types or change
manifest, fingerprint, binding, search, or rights semantics.

## Eucharistic stage inventory ownership — added 2026-10-16

The source-tree validator recognizes immediate
`inventories/eucharistic-stages/<slug>.json` dossiers with the
`eucharistic-book-stages` version 1 envelope, and the exact
`inventories/eucharistic-stage-coverage-v1.json` audit with the
`eucharistic-book-stage-coverage-audit` version 1 envelope. These are
project-authored research inventories, not external artifacts or new source
record types. Invalid JSON, wrong envelopes, nested payloads and unrelated JSON
remain rejected. `act-history` retains ownership of stage evidence, scope and
reference validation. No source manifest, binding, rights rule, fingerprint or
search-receipt meaning changes.

## Optional work composition date — added 2026-08-01

A `work` record may now carry `composed` and `composed_basis`, and stating one
requires the other. `composed` is when the work was **written**; an edition's
`date` remains when that edition was printed or translated.
`guidance/sources.md` owns the rule and its single exception, bible
translations, for which the act of translating is the work.

Both fields are optional and additive: no existing record changes meaning, and
no fingerprint moves until a work record is edited. That last clause is the
whole cost of the backfill, because an edition depends on its work and every
passage and binding above it depends on the edition — adding the field to a
work with pinned consumers hands each of them a review obligation.

`composed` is a free-form string, not a year, because composition dates are
ranges and approximations far more often than they are points: "c. 401-415",
"saec. VIII in.", "between 796 and 800". Rounding those to an integer asserts a
precision nobody has, and `guidance/sources.md` requires a range to be recorded
as a range and an unknown to be recorded unknown.

## Version 2 — added 2026-07-23

Version 2 adds first-class `segment` records for bounded constituents. Segments
live beneath the constituent edition, may point across work boundaries to an
exact container artifact, pin its SHA-256, inherit its storage and rights
limits, and record line or artifact-page bounds. Structural ownership remains
distinct from the cross-work evidence dependency used for fingerprints and
impact.

Version 2 also permits `page_count` on an artifact; permits a passage to choose
exactly one direct artifact or segment controller while retaining the ultimate
artifact's bare SHA-256; and requires a version 2 binding when it directly names
a version 2 record. Line-ranged segments are searchable only inside their
declared bounds, while page-only segments are not searchable by raw-line modes.
Corpora remain version 1 artifact-only snapshots. No accepted version 1 record,
fingerprint, search result, or receipt changes meaning.

## Version 1 — frozen 2026-07-22

The first frozen schema follows the complete-source City of God tracer. That
tracer retained exact distributable English and Latin witnesses, represented
remote acquisition parents and a companion image, defined fixed corpus
snapshots, mapped checked passage text to exact LF-delimited artifact lines,
recorded publication-local search receipts and evidence roles, and exercised
dependency fingerprints, reverse uses, and impact reporting across four
consumers.

Version 1 includes the five canonical source record types (`work`, `edition`,
`artifact`, `passage`, and `corpus`) plus publication-local `bindings`. Its
compatibility boundary and versioning rules are governed by
`guidance/sources.md`.
