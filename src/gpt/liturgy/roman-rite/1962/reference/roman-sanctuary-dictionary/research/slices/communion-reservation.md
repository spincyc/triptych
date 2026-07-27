# Communion and reservation inventory slice

Audit date: 2026-07-27 (America/Chicago).

Owner boundary: proposed Communion vessels and tools, Eucharistic reservation,
and exposition objects for later merger into the canonical object inventory.
This slice does not amend the aggregate manifests.

## Evidence ceiling

Every object below is an **identified lead**, not a publication-ready record.
The dictionary source audit presently records no claim-level verification for
this category. English and Latin names, morphology, use, handling, symbolism,
and 1962 status must therefore be checked directly against the exact official
books and competent contemporary material-culture sources before canonical
promotion. The generated plates are editorial search and layout aids; they are
not evidence for any claim.

## Proposed canonical records

| Proposed object ID | English working name | Latin lead | Category | Working scope | Server relation to verify |
|---|---|---|---|---|---|
| `obj-chalice` | chalice | `calix` | sacred vessels | Mass | recognizes; may assist only through prescribed service |
| `obj-mass-paten` | Mass paten | `patena` | sacred vessels | Mass | ordinarily recognizes only |
| `obj-ciborium` | ciborium | `pyxis` / `ciborium` | sacred vessels | Communion and reservation | ordinarily recognizes only |
| `obj-pyx` | pyx | `pyxis` | sacred vessels | reservation and carrying Communion | ordinarily recognizes only |
| `obj-communion-plate` | Communion plate | terminology unresolved | service objects | distribution of Communion | carries or presents where directed |
| `obj-tabernacle` | tabernacle | `tabernaculum` | altar and appointments | reservation | must not handle without competent direction |
| `obj-tabernacle-veil` | tabernacle veil | `conopaeum` lead | linens and textiles | reservation | recognizes; sacristan preparation to verify |
| `obj-sanctuary-lamp` | sanctuary lamp | terminology unresolved | altar and appointments | reservation indicator | recognizes; maintenance relation is local and practical |
| `obj-monstrance` | monstrance / ostensorium | `ostensorium` | sacred vessels | exposition, Benediction, procession | recognizes only |
| `obj-lunette` | lunette | `lunula` lead | sacred vessels | exposition | must not handle |

### Required variant pass

- Chalice, ciborium, pyx, monstrance, and Communion-plate forms may vary
  materially; decoration alone must not become a variant.
- The relationship among `pyxis`, English “pyx,” and English “ciborium” needs a
  lexical and period-specific audit rather than a one-to-one assumption.
- Tabernacle form, veil form, lamp suspension or stand, and the exposition
  assembly need exact universal-versus-local classification.
- The lunette must be related to, but not collapsed into, the monstrance.
- Reservation vessels used for the sick, Viaticum, or Holy Week require a
  ceremony-specific pass before inclusion here.

## Claim and source work required

1. Bind the exact 1962 *Missale Romanum* loci for the chalice, paten, ciborium,
   Communion distribution, purification, and reservation-related branches.
2. Bind the applicable exact *Rituale Romanum* edition and title for Communion
   outside Mass, Communion of the sick, Viaticum, exposition, reposition, and
   Benediction.
3. Bind the exact 1917 Code canons and then the material amendments in force at
   the 1962 horizon for reservation and the sanctuary lamp; legal findings
   must state jurisdiction, authority, and as-of date.
4. Use the edition-identified 1962 Fortescue/O'Connell/Reid ceremonial only
   after direct page inspection, preserving any difference between rubric,
   common practice, and editorial recommendation.
5. Add a provenanced material-culture source for construction and substantive
   forms. Retail listings and generated images may not serve this role.
6. Add symbolism only when a checked source expressly supports a brief
   traditional association; do not infer symbolism from shape or decoration.

Current repository lead:
`src/sources/works/adrian-fortescue/ceremonies-of-the-roman-rite-described/editions/twelfth-revised-1962/`.
Its present catalog artifact identifies an edition but does not itself verify
the object claims in this slice.

## Pencil plates

### `DIC-ART-CR-001`

- File:
  `shared/artwork/pencil/DIC-ART-CR-001-communion-vessels-tools.png`
- SHA-256:
  `b1cd7bb7e6795f11d0bb0e66c6020f8634d9c5eb9c70d27966797a741ef62674`
- Dimensions and mode: 1024 by 1536 pixels; received 8-bit sRGB, visually
  monochrome.
- Generator: built-in OpenAI image-generation interface; no model/version
  exposed.
- Reference image: none.
- Prompt summary: a dense portrait graphite comparison plate of a lidded
  ciborium, closed and open pyx views, handled Communion plate, plain Mass
  paten, and chalice, isolated on white without labels.
- Personal review: all requested object families are present and separated;
  the ciborium and chalice each have one coherent stem and foot; the pyx has
  closed and open views; the two paten forms are visually distinguishable;
  no baked-in text, arrows, people, color wash, watermark, or obvious duplicate
  vessel parts were observed.
- Review limit: morphology and relative scale remain **unverified**. The
  hinged case-like pyx and handled Communion plate especially require
  source-based form review before publication.
- Review state: `generated-lead`; not approved for a rendered edition.

### `DIC-ART-CR-002`

- File:
  `shared/artwork/pencil/DIC-ART-CR-002-reservation-exposition.png`
- SHA-256:
  `5fabdaec439eb9b9b3dd2428535abb08c25503f59e5fe86359abda1a6f4eb8ca`
- Dimensions and mode: 1024 by 1536 pixels; received 8-bit sRGB, visually
  monochrome.
- Generator: built-in OpenAI image-generation interface; no model/version
  exposed.
- Reference image: none.
- Prompt summary: a dense portrait graphite comparison plate of a one-door
  tabernacle, separate fitted tabernacle veil, hanging sanctuary lamp,
  sunburst monstrance, and isolated plus in-position lunette views, without
  labels.
- Personal review: one tabernacle door, one coherent monstrance support and
  foot, a three-chain hanging lamp, separate veil, and both lunette views are
  visibly present; no baked-in prose, labels, arrows, people, color wash, or
  watermark were observed.
- Review limit: the plate makes the lunette appear within an empty monstrance
  center and gives the veil a generic fitted-cover form. Exact construction,
  scale, liturgical status, and the veil's period-appropriate form remain
  unverified.
- Review state: `generated-lead`; not approved for a rendered edition.

## Merge gate

Do not copy these leads into canonical TOML or select either artwork asset for
publication until:

- each reader-facing claim has an exact verified source binding;
- lexical conflicts are resolved or preserved explicitly;
- an independent ceremonial and material-form review accepts the depicted
  object;
- the artwork is cropped or normalized without changing its content and the
  normalized hash is recorded; and
- the aggregate object, artwork, plate, completeness, variant, rights, and
  source records are updated coherently by their owner.
