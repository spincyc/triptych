# Comprehensive volume guide map

Status: **held structural prototype; not approved for publication**
Audit date: 2026-07-27
Edition selection: `ed-comprehensive`

## Reader and purpose

This is the adult-reference owner volume for the publication family. It is
intended to identify and compare the material objects of the Roman Rite at the
1962 horizon, with documented earlier Roman practice segregated in a
historical section. It does not yet contain verified dictionary entries.

## Current placeholder selection

The present `main.tex` renders only a title, a short explanation of the future
plate system, the section placeholders in `shared/comprehensive-sections.tex`,
and terminal placeholder matter. The placeholders name the intended coverage;
they are not object records, verified captions, exhaustive inventories, or
approved plates.

When populated, `ed-comprehensive` selects every `publication-ready` canonical
record admitted by `shared/schema/edition-selections.toml`: the declared Roman
1962 corpus and reviewed regional, religious-community, institutional, and
pre-1962 historical supplements. Records with unresolved status are excluded.

## Reader order

1. Compact title and plate/symbol key.
2. An actual sanctuary-composition plate.
3. Church and sanctuary.
4. Altar and appointments.
5. Sacred vessels.
6. Linens and textile articles.
7. Books and printed objects.
8. Service objects.
9. Incense.
10. Priestly vestments.
11. Deacon and subdeacon.
12. Pontifical and prelatial vesture and insignia.
13. Servers, ministers, and choir.
14. Requiem Mass.
15. Nuptial and ritual Masses.
16. Holy Week.
17. Pontifical Mass compositions.
18. Related Roman ceremonies.
19. Earlier Roman practice, ordered chronologically and then by functional
    type within each period.
20. Pronunciation, bilingual and visual indexes, variant and terminology
    notes, scope and qualifications, numbered source notes, references,
    generation metadata, and rights colophon.

## Canonical dependency

This leaf owns no publication-local object facts. Its entries must be
generated from canonical TOML records conforming to
`shared/schema/inventory-schema.toml`, selected by
`shared/schema/edition-selections.toml`, and reconciled with the owner
inventory, completeness, variant, artwork, plate, source, rights, and
production records. Publication-local TeX may arrange plates but may not copy,
contradict, or enlarge canonical claims.

## Hold and nonpublication state

The canonical inventory currently contains zero source-audited,
art-reviewed, or publication-ready objects. The source corpus and
completeness matrix remain open, and no reviewed artwork or plate is approved.
This leaf therefore remains on hold. A successful TeX build would demonstrate
only that the scaffold compiles; it would not authorize installation,
cataloging as a completed dictionary, web publication, or a completeness
claim.
