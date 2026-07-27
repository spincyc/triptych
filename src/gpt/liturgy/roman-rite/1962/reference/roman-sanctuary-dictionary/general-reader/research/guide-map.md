# General-reader edition guide map

Status: **held structural prototype; not approved for publication**
Audit date: 2026-07-27
Edition selection: `ed-general-reader`

## Reader and purpose

This concise use-derived edition is for a broad adult audience. Its eventual
audience layer emphasizes visual identification, purpose, at most one brief
source-bound symbolic association, and historical relationship while
preserving distinctions of period and status.

## Current placeholder selection

The present `main.tex` contains no selected canonical objects. It offers four
placeholders only: The Sanctuary; Objects and Linens; Vestments and Insignia;
and Historical Perspective. These are proposed survey groupings, not verified
captions, representative selections, or evidence of completeness.

When populated, `ed-general-reader` selects only `publication-ready` canonical
records whose `audience_relevance.general_reader` value is `required`.
Unlike the more operational use editions, records marked merely `useful` are
not selected. Records with unresolved status are excluded.

## Reader order

1. Compact title and visual/status key.
2. Concise sanctuary orientation.
3. High-density comparisons of representative objects and linens.
4. Vestments and insignia, including substantively different forms.
5. A visibly separate historical survey ordered chronologically and then by
   type where the selection contains more than one type in a period.
6. Terminal bilingual and visual indexes, qualifications, keyed source notes,
   generation metadata, and rights matter.

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
