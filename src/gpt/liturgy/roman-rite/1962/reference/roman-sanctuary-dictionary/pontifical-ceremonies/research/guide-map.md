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
generator-admitted `ed-pontifical` selection under `build/`. The authoritative
selection is empty because there are no publication-ready canonical objects.
The separately manifested priestly-review selection admits six ordinary
supporting-object records and visibly omits the other 37 records in the current
43-record inventory. It makes no verified rubrical or rank distinction and is
not a ceremonial sequence.

When populated, `ed-pontifical` selects only `publication-ready` records. It
includes the `pontifical-and-prelatial` category in union with records whose
`audience_relevance.pontifical` value is `required` or `useful`, allowing the
ordinary supporting objects needed to understand pontifical compositions.
Records with unresolved status are excluded.
The category and relevance branches form a union; the publication-ready and
unresolved-status gates apply to the resulting set. This does not imply that
every ordinary object is a pontifical supporting object.

## Priestly-review selection boundary

The priestly-review edition may expose only explicitly manifested canonical
records proposed by the pontifical category/relevance union, with workflow and
evidence state visible. Proposed distinctions of rank, privilege, bearer,
layering, station, and transfer remain questions until independently accepted.
Ordinary supporting objects enter only through recorded pontifical relevance;
visual proximity in a composition is insufficient.

## Visible omissions in the review edition

The review edition must list omitted ranks, privileges, ministers, Mass
forms, stations, vesture layers, insignia, furnishings, books, transfers, and
historical forms. It must state when a composition lacks evidence for a full
ceremonial relationship and must never make a partial roster appear complete.

## Reader order

1. Compact title with a conspicuous priestly-review/hold notice.
2. Visible omissions and review-state key.
3. Status and relationship key.
4. Pontifical vesture in laid-flat, layered, and worn views.
5. Insignia, with substantive forms and verified status distinctions.
6. Furnishings and books in relational compositions.
7. Ministers and source-verified object transfers.
8. Priestly-review questions and correction instructions.
9. Selective pronunciation, English--Latin and Latin--English indexes, visual
   index, variant and terminology notes, scope and qualifications, numbered
   source notes and references, generation metadata, and rights colophon.

Vesture proceeds from foundational layers to outer vesture and then
rank- or use-dependent forms. Insignia are grouped by verified bearer, status,
and use. Furnishings and books are arranged by composition and station;
minister and transfer plates follow verified ceremony sequence. The plate
manifest preserves intentional order within each section.

## Questions for priestly review

1. Are bearer, rank, privilege, occasion, and 1962 status correctly stated for
   every vestment and insignium?
2. Are foundational layers, outer vesture, and rank- or use-dependent forms
   shown in a possible and intelligible order?
3. Are throne, faldstool, station, book, and furnishing relationships correct
   for the named composition?
4. Are ministers and object transfers complete enough for the plate's stated
   purpose and distinguished from nearby but unrelated actions?
5. Do the drawings invent, omit, or conflate any diagnostic part, form, or
   manner of wearing?
6. Which claim requires narrower qualification by celebrant, place,
   privilege, or ceremony before another review?

## Canonical dependency

This leaf owns no independent claim about rank, privilege, use, wearing,
placement, minister, or transfer. All facts, variants, sources, artwork,
composition links, and audience relevance must come from canonical records
conforming to `shared/schema/inventory-schema.toml`; selection is governed by
`shared/schema/edition-selections.toml`. Audience notes may clarify a
relationship but may not contradict or enlarge the verified base record.

## Hold and nonpublication state

There are currently zero publication-ready canonical records and no approved
public pontifical selection. This leaf remains on hold. A priestly-review PDF
must not be used as ceremonial guidance; it solicits correction only.
Plate-manifest order remains a publication blocker.
