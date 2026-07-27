# Comprehensive volume guide map

Status: **held structural prototype; not approved for publication**
Audit date: 2026-07-27
Edition selection: `ed-comprehensive`

## Reader and purpose

This is the adult-reference owner volume for the publication family. It is
intended to identify and compare the material objects of the Roman Rite at the
1962 horizon, with documented earlier Roman practice segregated in a
historical section. It does not yet contain verified dictionary entries.

## Current generated selection

The present `main.tex` is a publication-capable shell that consumes only the
generator-admitted `ed-comprehensive` selection under `build/`. That
generated selection is empty because there are no publication-ready
canonical objects. The shell therefore renders a held notice, not object
records, verified captions, an exhaustive inventory, or approved plates.

When populated, `ed-comprehensive` selects every `publication-ready` canonical
record admitted by `shared/schema/edition-selections.toml`: the declared Roman
1962 corpus and reviewed regional, religious-community, institutional, and
pre-1962 historical supplements. Records with unresolved status are excluded.
Selection does not make every documented variant a separate entry:
substantive variants remain attached to their canonical object record and are
shown only when their reviewed plate plan calls for them.

## Priestly-review selection boundary

The priestly-review edition is a held review packet, not the comprehensive
publication. Its public `ed-comprehensive` selection remains empty until
records are `publication-ready`. A nonempty review packet may show only
canonical records explicitly named in a review-only manifest and must print
each record's workflow and evidence state. It may expose an image, proposed
headword, source-bound claim, qualification, or unresolved question for
review; it may not silently admit an `identified`, `source-audited`,
`art-reviewed`, or `held` record to the public selection.

## Visible omissions in the review edition

The review edition must visibly state that unselected categories and
unrendered records are omitted, that the official and material-culture corpus
is not closed, that historical coverage is not complete, and that missing
plates or variants are open work rather than evidence of absence. It must not
use an unqualified title or contents treatment that suggests a complete
dictionary.

## Reader order

1. Compact title with a conspicuous priestly-review/hold notice.
2. Visible omissions and review-state key.
3. Plate and symbol key.
4. An actual sanctuary-composition plate.
5. Church and sanctuary.
6. Altar and appointments.
7. Sacred vessels.
8. Linens and textile articles.
9. Books and printed objects.
10. Service objects.
11. Incense.
12. Priestly vestments.
13. Deacon and subdeacon.
14. Pontifical and prelatial vesture and insignia.
15. Servers, ministers, and choir.
16. Requiem Mass.
17. Nuptial and ritual Masses.
18. Holy Week.
19. Pontifical Mass compositions.
20. Related Roman ceremonies.
21. Earlier Roman practice, ordered chronologically and then by functional
    type within each period.
22. Priestly-review questions and correction instructions.
23. Pronunciation, bilingual and visual indexes, variant and terminology
    notes, scope and qualifications, numbered source notes, references,
    generation metadata, and rights colophon.

Roman-1962-horizon records follow this functional order. Historical records
follow the five periods declared in `historical_order`, earliest first, and
then the same functional categories within each period. The plate manifest,
not alphabetical sorting, controls intentional order within a section.

## Questions for priestly review

1. Does each rendered item's stated liturgical status match the 1962 horizon,
   including conditional, privileged, regional, religious-community, and
   merely practical use?
2. Are Mass objects kept distinct from objects of surrounding ceremonies?
3. Do the sanctuary and pontifical compositions show possible arrangements
   without turning one legitimate form into a universal prescription?
4. Are historical objects visibly separated from ordinary 1962 use?
5. Are handling, minister, placement, and brief symbolism statements accurate,
   sufficiently qualified, and pastorally intelligible?
6. Which depicted forms or terminology require a narrower jurisdiction,
   period, or source note before another review?

## Canonical dependency

This leaf owns no publication-local object facts. Its entries must be
generated from canonical TOML records conforming to
`shared/schema/inventory-schema.toml`, selected by
`shared/schema/edition-selections.toml`, and reconciled with the owner
inventory, completeness, variant, artwork, plate, source, rights, and
production records. Publication-local TeX may arrange plates but may not copy,
contradict, or enlarge canonical claims.

## Hold and nonpublication state

The canonical inventory contains working records but no
`publication-ready` selection. The source corpus and completeness matrix
remain open, and consumer-reviewed artwork and plates are not yet sufficient
for this volume. This leaf therefore remains on hold. A successful review
build solicits correction only; it does not authorize installation,
cataloging as a completed dictionary, web publication, or a completeness
claim. Plate-manifest order remains a publication blocker.
