# Artwork manifest

Status: **generated candidates present; none accepted or approved**
Audit date: 2026-07-27

The canonical machine-readable manifest is `artwork-manifest.toml`. Its format
is governed by `shared/schema/artwork-manifest-schema.toml` and checked by
`scripts/check-roman-sanctuary-artwork`. This Markdown record explains the
human audit boundary; it does not duplicate asset rows.

The altar-server-guide pencil assets elsewhere in the repository are not
automatically dictionary assets. Reuse requires an explicit dictionary
artwork record, object-level factual audit, rights review, and full-size
approval.

## Visual contract

- US Letter portrait consumers; monochrome graphite/pencil on white.
- Generated image pixels contain no lettering, arrows, numbers, borders, or
  semantic marks. TeX owns all labels.
- Dense ordinary plates normally contain six to ten distinctive objects, four
  to six confusables, two or three multi-view vestments, or one composition
  with detail insets.
- Ambiguous objects require isolated and contextual/folded/unfolded/worn views.
- Common scale is used when diagnostic; otherwise the plate carries a sourced
  scale or `not to common scale` notice.
- Publishing rasters should ordinarily be stripped 8-bit grayscale PNG at no
  less than 300 effective dpi. Repository review triggers remain applicable.

## Current inventory

The canonical manifest's `[[asset_files]]` inventory covers every tracked
dictionary PNG, including held research leads and explicitly rejected
studies. Full `[[artworks]]` records preserve prompt, provenance, consumer,
rights, and review detail where that audit has been reconciled. An asset-file
row is technical custody only: it neither approves the raster nor supplies a
missing object-level link. The sacristy-preparation comparison remains held
at `generated` because of its recorded unsupported ornaments and uncontrolled
cabinet morphology.

The Communion/reservation corrected leads and the pre-1955 composite remain
only as held `asset_files`. Their former artwork-link records were removed
because source-controlled canonical identities do not exist for every object
they depict. The negative findings remain in the owning slice and historical
inventory; technical custody must not be mistaken for eligibility.

## Required audit per asset

Record prompt or brief; exact creator/model/runtime disclosure where exposed;
creation date; source/reference identities and rights; pixel dimensions,
color mode, bytes, SHA-256, planned placement and effective dpi; depicted
object and variant IDs; corrections; consumer plates; and separate factual,
visual, monochrome-print, rights, and release states.

Every artwork ID is reconciled bidirectionally with the `artwork` table in
each canonical object TOML record. Unknown object IDs, orphan assets, broken
precursor/reference links, mismatched technical properties, or a
publication-ready object without consumer-reviewed artwork fail validation.
Every substantive variant of a publication-ready object must likewise name
consumer-reviewed artwork that links back to its variant ID.

Reject invented or missing parts, impossible folds or wearing, false
ornament, misleading scale, duplicate figures, impossible placement, false
material cues, and an object that remains ambiguous in monochrome.

The reusable prompt grammar, semantic ID rules, cutaway and sanctuary-scene
supplements, entry template, candidate lifecycle, and downstream invalidation
rules are owned by `artwork-system.md`. Before commissioning an asset, lock
the visual invariants in the object inventory, assign its `art-` or
`RPD-SCN` identity, and create its manifest entry in the `unreviewed` state.
Before composing a plate, advance every dependency through factual and
visual/technical review and create the corresponding `RPD-PLT` entry. A
TeX-only plate records `generator: none` and lists all consumed figure IDs.
