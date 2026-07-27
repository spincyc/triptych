# Pontifical-ceremonies edition guide map

Status: **held structural prototype; not approved for publication**
Audit date: 2026-07-27
Edition selection: `ed-pontifical`

## Reader and purpose

This use-derived edition is a focused visual reference to pontifical vesture,
insignia, furnishings, ministers, and object relationships. Full
compositions and detail insets are required where an isolated object cannot
explain layering, rank-dependent use, placement, or transfer.

## Current placeholder selection

The present `main.tex` contains no selected canonical objects and makes no
rubrical or rank distinction. It offers four placeholders only: Pontifical
Vesture; Insignia; Furnishings and Books; and Ministers and Object Transfers.
These headings are a proposed relational route, not a verified inventory or
ceremonial sequence.

When populated, `ed-pontifical` selects only `publication-ready` records. It
includes the `pontifical-and-prelatial` category in union with records whose
`audience_relevance.pontifical` value is `required` or `useful`, allowing the
ordinary supporting objects needed to understand pontifical compositions.
Records with unresolved status are excluded.

## Reader order

1. Compact title and status/relationship key.
2. Pontifical vesture in laid-flat, layered, and worn views.
3. Insignia, with substantive forms and verified status distinctions.
4. Furnishings and books in relational compositions.
5. Ministers and source-verified object transfers.
6. Terminal indexes, qualifications, keyed source notes, generation metadata,
   and rights matter.

## Canonical dependency

This leaf owns no independent claim about rank, privilege, use, wearing,
placement, minister, or transfer. All facts, variants, sources, artwork,
composition links, and audience relevance must come from canonical records
conforming to `shared/schema/inventory-schema.toml`; selection is governed by
`shared/schema/edition-selections.toml`. Audience notes may clarify a
relationship but may not contradict or enlarge the verified base record.

## Hold and nonpublication state

There are currently zero publication-ready canonical records, and no
pontifical object, rank distinction, layered vesture study, composition, or
transfer sequence has passed the required source and artwork audits. This
leaf remains on hold. Its placeholders must not be used as ceremonial
guidance, and any scaffold PDF is a production test only.
