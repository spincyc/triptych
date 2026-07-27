# General-reader edition guide map

Status: **held structural prototype; not approved for publication**
Audit date: 2026-07-27
Edition selection: `ed-general-reader`

## Reader and purpose

This concise use-derived edition is for a broad adult audience. Its eventual
audience layer emphasizes visual identification, purpose, at most one brief
source-bound symbolic association, and historical relationship while
preserving distinctions of period and status.

## Current generated selection

The present `main.tex` is a publication-capable shell that consumes only the
generator-admitted `ed-general-reader` selection under `build/`. That
generated selection is empty because there are no publication-ready
canonical objects. It therefore renders a held notice, not verified captions,
a representative selection, or evidence of completeness.

When populated, `ed-general-reader` selects only `publication-ready` canonical
records whose `audience_relevance.general_reader` value is `required`.
Unlike the more operational use editions, records marked merely `useful` are
not selected. Records with unresolved status are excluded.
This is a deliberate concise-survey threshold: presence in the comprehensive
volume does not itself make an object representative enough for this leaf.

## Reader order

1. Compact title and visual/status key.
2. Concise sanctuary orientation.
3. High-density comparisons of representative objects and linens.
4. Vestments and insignia, including substantively different forms.
5. A visibly separate historical survey ordered chronologically and then by
   type where the selection contains more than one type in a period.
6. Terminal bilingual and visual indexes, qualifications, keyed source notes,
   generation metadata, and rights matter.

The sanctuary section moves from orientation compositions to individual
furnishings. Objects and linens are arranged as functional comparisons;
vesture and insignia are grouped by minister and substantive form. Historical
selections follow the comprehensive volume's chronology and then category.
The plate manifest preserves intentional order within each section.

## Canonical dependency

This leaf is a curated visual survey, not a second inventory. Identity,
purpose, symbolism, historical status, variants, sources, artwork, and
audience relevance must come from canonical records conforming to
`shared/schema/inventory-schema.toml`; selection is governed by
`shared/schema/edition-selections.toml`. Simplified reader wording may appear
only in canonical `audience_note` data and may not erase qualifications or
change verified claims.

## Hold and nonpublication state

There are currently zero publication-ready canonical records and no approved
curation, representative set, historical plate, or artwork. This leaf remains
on hold and must not be installed or published. A scaffold PDF, if built,
does not establish factual review or authorize a completeness claim.
Plate-manifest order remains a publication blocker.
