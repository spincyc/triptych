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

## Priestly-review selection boundary

The priestly-review edition may expose only explicitly manifested canonical
records proposed for `ed-sacristan`, with workflow and evidence state visible.
It may ask for review of preparation, assembly, placement, folding, storage,
or changeover claims, but none becomes a public direction until its canonical
record and artwork satisfy the publication gates. The review packet is not a
conservation manual or a parish procedure sheet.

## Visible omissions in the review edition

The review edition must list omitted object families, ceremonies, seasonal or
branch-dependent changes, and any preparation, fold, storage, cleaning, or
disposition question not yet source-audited. Silence must not imply that a
local method is universal or that an omitted care practice is safe.

## Reader order

1. Compact title with a conspicuous priestly-review/hold notice.
2. Visible omissions and review-state key.
3. Status and handling key.
4. Sanctuary and altar preparation compositions.
5. Vessels, linens, and books, using multiple views where construction,
   folding, or placement would otherwise be ambiguous.
6. Vestments and insignia, including verified preparation relationships.
7. Equipment for special Masses and related ceremonies, grouped by
   changeover need and retaining exact status labels.
8. Priestly-review questions and correction instructions.
9. Selective pronunciation, English--Latin and Latin--English indexes, visual
   index, variant and terminology notes, scope and qualifications, numbered
   source notes and references, generation metadata, and rights colophon.

The first section draws from sanctuary, altar, appointment, service, and
composition records with preparation or placement relevance. Vessels,
textiles, books, incense, and service objects are then grouped by verified
preparation relationship rather than alphabetically. Wearables and insignia
are grouped by minister. Ceremony-limited or changeover-dependent equipment
follows by special Mass or ceremony. Canonical relationships and the plate
manifest preserve intentional order within each section.

## Questions for priestly review

1. Are preparation and placement claims liturgically correct for the named
   Mass or ceremony and clearly distinguished from local practice?
2. Are clergy-only handling and disposition boundaries correctly stated?
3. Do linen folds, vessel assembly, vestment preparation, and book setup avoid
   unsupported prescription?
4. Are special-Mass, Holy Week, pontifical, and related-ceremony changeovers
   accurately separated?
5. Does any storage or care wording exceed the evidence or stray into
   conservation advice?
6. Which omitted preparation relationships would make the review packet
   misleading if not shown before the next review?

## Canonical dependency

This leaf owns no preparation fact or copied inventory. Identity, placement,
handling, preparation, storage, variants, claims, sources, artwork, and
audience relevance must come from canonical records conforming to
`shared/schema/inventory-schema.toml`; selection is governed by
`shared/schema/edition-selections.toml`. Sacristan-specific notes must remain
in canonical `audience_note` data and may not silently turn common practice
into a universal prescription.

## Hold and nonpublication state

There are currently zero publication-ready canonical records, and no public
preparation selection has passed the required gates. The leaf remains on hold
and must not be installed, published, or used operationally. A priestly-review
PDF solicits corrections only. Plate-manifest order remains a publication
blocker.
