# Illustrated Dictionaries of the Postconciliar Roman Sanctuary

This profile governs the comprehensive adult-reference illustrated dictionary of
the postconciliar Roman sanctuary and its use-derived editions beneath
`src/<provider>/liturgy/roman-rite/postconciliar/<edition-locale>/reference/roman-sanctuary-dictionary/`.
It supersedes the preliminary status of
`guidance/liturgy/postconciliar-illustrated-dictionary-handoff.md`, which
remains the design provenance record. Universal editorial, source, repository,
rights, metadata, review, and publication rules remain in force.

The family owner root is non-publishable. Each publishable leaf declares
`kind = "pictorial-dictionary-postconciliar"` (derived from its path) and the
`liturgy-reference-v1` document type in `publication.toml` under
[document schemas](../document-schemas.md). Canonical object records, edition
dispositions, artwork manifests, and plate manifests keep one owner at the
family root; smaller audience editions render curated projections from that
owner without creating independently drifting descriptions or artwork.

## Governing priorities

1. Declare one exact Latin typical edition, approved territorial translation and
   adaptation, jurisdiction, and as-of date before making any normative claim.
2. Separate universal Roman law, changes between typical editions, territorial
   adaptations, choices assigned to bishop/conference/celebrant, legitimate
   local arrangements, documented custom, and historically superseded
   postconciliar practice.
3. Let accurate, label-free monochrome graphite drawings and comparisons carry
   visual identification, with TeX owning all headwords, labels, callouts,
   scale notices, and movement overlays.
4. Keep one canonical inventory and shared artwork owner for the comprehensive
   volume and every use-based edition (altar server, sacristan, MC/trainer,
   general reader, episcopal/major ceremonies).
5. Never import 1962 terminology, roles, altar orientation, handling rules, or
   visual conventions into postconciliar entries as norms; record explicit
   1962 counterpart relationships only after direct edition comparison.

## Edition-locale dispositions and 1962 counterpart taxonomy

Every canonical object record carries a controlled edition-scoped disposition
rather than a bare boolean flag:

- `required`, `provided`, `permitted`, `optional`, `territorial adaptation`,
  `local selection`, `customary`, `superseded`, `not applicable`, or
  `unresolved`.

Where an object has a counterpart in the 1962 Roman Rite, record the exact
relationship after direct collation of the identified books:

- `continued`, `renamed`, `materially changed`, `changed use`, `optional`,
  `superseded`, `newly provided`, or `no established counterpart`.

Keep universal identity separate from edition-locale dispositions so other
territories can later add, qualify, or mark entries inapplicable without
rewriting base objects.

## Artwork and plate contract

- US Letter portrait pages; monochrome graphite or pencil drawings on white
  ground, seamlessly integrated with the page ground (no crop boxes, gray
  halos, or mismatched backgrounds).
- Generated raster artwork contains **no text, lettering, numerals, arrows,
  borders, or color-only encodings**. TeX places all labels, scale notices,
  liturgical-color keys, and callouts.
- Favor dense, image-dominant comparison plates (normally four to ten objects
  per plate, fewer for multi-view vestments or full sanctuary compositions).
  Supply folded/unfolded, front/back, empty/assembled, worn, or context insets
  whenever an isolated object would be ambiguous.
- Visually audit every raster plate at full size for invented parts, impossible
  folds or fastenings, mistaken ministers or insignia, misleading scale,
  duplicate objects, and impossible liturgical placement. A plausible image is
  never source evidence.
- Project-owned AI artwork generation is permitted when controlled strictly by
  the checked canonical object record and publicly reachable primary sources.

## Reader order and terminal apparatus

Open with a compact plate-reading key and a sanctuary composition plate, then
proceed functionally through the sanctuary, altar/ambo/chair/tabernacle/font,
vessels, linens, books, service equipment, incense, vesture (keeping ordained,
instituted, deputed, and extraordinary ministers distinct), Communion modes,
and special/adjacent rites. Place historically superseded postconciliar forms
in a clearly separated chronological historical section.

Put global apparatus in terminal sections: Latin pronunciation appendix for
commonly spoken terms, English--Latin and Latin--English indexes, chronological
postconciliar change table, keyed source notes, `Scope, Edition, and
Qualifications` (including completeness boundary and explicit remaining-gaps
record), references, and generation metadata. Keep immediate handling and
safety notices beside the affected object.

## Required records and alpha gate

The non-publishable owner root keeps `research/scope.md`,
`research/edition-manifest.md`, `research/object-inventory.md` (and/or its
canonical structured TOML inventory under `shared/`),
`research/artwork-manifest.md` (and/or `.toml`), `research/plate-manifest.md`,
`research/source-audit.md`, and `research/remaining-gaps.md`. Each publishable
leaf keeps `research/guide-map.md`, `research/source-bindings.toml`,
`publication.toml`, `web-edition.toml`, and `generation-metadata.tex`.

Alpha publication follows the six repository-wide concerns (source integrity,
rights and lawful distribution, safety, reproducibility and artifact identity,
mechanical validity, and basic visual usability). A bounded alpha release must
state its checked corpus boundary honestly in `remaining-gaps.md` and the
terminal scope appendix without placeholder prose or unverified completeness
claims. Web editions must provide object-level alt text, reading order, and
textual equivalents without duplicating authoritative prose.
