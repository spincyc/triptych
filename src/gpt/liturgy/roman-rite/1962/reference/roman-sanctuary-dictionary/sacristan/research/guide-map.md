# Sacristan edition guide map

Status: **held structural prototype; not approved for publication**
Audit date: 2026-07-27
Edition selection: `ed-sacristan`

## Reader and purpose

This use-derived edition is for sacristans. Its eventual audience layer
emphasizes verified preparation, assembly, placement, folding, storage, and
ceremony-specific changeover. It is a liturgical visual reference, not a
conservation manual and not a substitute for documented local procedures.

## Current generated selection

The present `main.tex` is a publication-capable shell that consumes only the
generator-admitted `ed-sacristan` selection under `build/`. That generated
selection is empty because there are no publication-ready canonical objects.
It therefore renders a held notice, not verified preparation directions,
folds, storage rules, or an exhaustive equipment list.

When populated, `ed-sacristan` selects only `publication-ready` canonical
records whose `audience_relevance.sacristan` value is `required` or `useful`.
Records with unresolved status are excluded.
Selection requires recorded sacristan relevance; an object's presence in the
comprehensive volume alone does not place it in this leaf.

## Reader order

1. Compact title and status/handling key.
2. Sanctuary and altar preparation compositions.
3. Vessels, linens, and books, using multiple views where construction,
   folding, or placement would otherwise be ambiguous.
4. Vestments and insignia, including verified preparation relationships.
5. Equipment for special Masses and related ceremonies, grouped by
   changeover need and retaining exact status labels.
6. Terminal indexes, qualifications, keyed source notes, generation metadata,
   and rights matter.

The first section draws from sanctuary, altar, appointment, service, and
composition records with preparation or placement relevance. Vessels,
textiles, books, incense, and service objects are then grouped by verified
preparation relationship rather than alphabetically. Wearables and insignia
are grouped by minister. Ceremony-limited or changeover-dependent equipment
follows by special Mass or ceremony. Canonical relationships and the plate
manifest preserve intentional order within each section.

## Canonical dependency

This leaf owns no preparation fact or copied inventory. Identity, placement,
handling, preparation, storage, variants, claims, sources, artwork, and
audience relevance must come from canonical records conforming to
`shared/schema/inventory-schema.toml`; selection is governed by
`shared/schema/edition-selections.toml`. Sacristan-specific notes must remain
in canonical `audience_note` data and may not silently turn common practice
into a universal prescription.

## Hold and nonpublication state

There are currently zero publication-ready canonical records, and no
preparation sequence, fold, storage direction, artwork, or plate has passed
the required audits. The leaf remains on hold and must not be installed,
published, or used operationally. A scaffold PDF, if built, proves only the
rendering shell. Plate-manifest order remains a publication blocker.
