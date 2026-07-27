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

## Priestly-review selection boundary

The priestly-review edition may expose only explicitly manifested canonical
records proposed for the `required` general-reader selection, with workflow
and evidence state visible. The review is of representativeness, clarity,
status, and accuracy; it does not authorize a claim that the sample is
complete or that an attractive form is normative.

## Visible omissions in the review edition

The review edition must list omitted categories, periods, ceremony-specific
objects, substantive variants, and unresolved terminology. Because this is a
concise survey, it must also say that deliberate curation is not evidence that
unselected objects or forms are unimportant or non-Roman.

## Reader order

1. Compact title with a conspicuous priestly-review/hold notice.
2. Visible omissions and review-state key.
3. Visual and status key.
4. Concise sanctuary orientation.
5. High-density comparisons of representative objects and linens.
6. Vestments and insignia, including substantively different forms.
7. A visibly separate historical survey ordered chronologically and then by
   type where the selection contains more than one type in a period.
8. Priestly-review questions and correction instructions.
9. Selective pronunciation, English--Latin and Latin--English indexes, visual
   index, variant and terminology notes, scope and qualifications, numbered
   source notes and references, generation metadata, and rights colophon.

The sanctuary section moves from orientation compositions to individual
furnishings. Objects and linens are arranged as functional comparisons;
vesture and insignia are grouped by minister and substantive form. Historical
selections follow the comprehensive volume's chronology and then category.
The plate manifest preserves intentional order within each section.

## Questions for priestly review

1. Is the selection genuinely representative without presenting a preferred
   artistic form as the Roman norm?
2. Can a non-specialist distinguish universal, conditional, regional,
   religious-community, practical, and historical status?
3. Are identity and purpose lines both accurate and short enough for a visual
   survey?
4. Is each symbolic association appropriately sourced, qualified, and
   subordinate to identification?
5. Does the historical section prevent obsolete objects from being mistaken
   for ordinary 1962 use?
6. Which omission or simplification would materially mislead a general
   reader?

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
public curation. This leaf remains on hold and must not be installed or
published. A priestly-review PDF solicits correction only and does not
authorize a completeness claim.
Plate-manifest order remains a publication blocker.
