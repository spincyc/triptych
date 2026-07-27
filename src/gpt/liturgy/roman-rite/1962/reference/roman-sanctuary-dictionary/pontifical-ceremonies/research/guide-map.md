# Pontifical-ceremonies edition guide map

Status: **held structural prototype; not approved for publication**
Audit date: 2026-07-27
Edition selection: `ed-pontifical`

## Reader and purpose

This use-derived edition is a focused visual reference to pontifical vesture,
insignia, furnishings, ministers, and object relationships. Full
compositions and detail insets are required where an isolated object cannot
explain layering, rank-dependent use, placement, or transfer.

## Current generated selection

The present `main.tex` is a publication-capable shell that consumes only the
generator-admitted `ed-pontifical` selection under `build/`. That generated
selection is empty because there are no publication-ready canonical objects,
and the shell makes no rubrical or rank distinction. It therefore renders a
held notice, not a verified inventory or ceremonial sequence.

When populated, `ed-pontifical` selects only `publication-ready` records. It
includes the `pontifical-and-prelatial` category in union with records whose
`audience_relevance.pontifical` value is `required` or `useful`, allowing the
ordinary supporting objects needed to understand pontifical compositions.
Records with unresolved status are excluded.
The category and relevance branches form a union; the publication-ready and
unresolved-status gates apply to the resulting set. This does not imply that
every ordinary object is a pontifical supporting object.

## Reader order

1. Compact title and status/relationship key.
2. Pontifical vesture in laid-flat, layered, and worn views.
3. Insignia, with substantive forms and verified status distinctions.
4. Furnishings and books in relational compositions.
5. Ministers and source-verified object transfers.
6. Terminal indexes, qualifications, keyed source notes, generation metadata,
   and rights matter.

Vesture proceeds from foundational layers to outer vesture and then
rank- or use-dependent forms. Insignia are grouped by verified bearer, status,
and use. Furnishings and books are arranged by composition and station;
minister and transfer plates follow verified ceremony sequence. The plate
manifest preserves intentional order within each section.

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
leaf remains on hold. Its generated held notice must not be used as
ceremonial guidance, and any scaffold PDF is a production test only.
Plate-manifest order remains a publication blocker.
