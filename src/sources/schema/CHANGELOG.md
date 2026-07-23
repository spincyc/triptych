# Source Schema Changelog

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
