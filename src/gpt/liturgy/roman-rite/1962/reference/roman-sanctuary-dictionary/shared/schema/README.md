# Roman Sanctuary Dictionary Data Contract

This directory defines the declarative boundary between researched object
records, audience selections, artwork, and TeX rendering. It does not contain
verified object claims. A populated record may be rendered only after its
claim-level evidence and artwork review states permit that use.

## Files

- `inventory-schema.toml` is the normative field and controlled-vocabulary
  contract.
- `artwork-manifest-schema.toml` defines canonical artwork provenance,
  technical identity, object/variant linkage, consumers, rights, and review
  states.
- `artwork-manifest.example.toml` is a non-evidentiary empty-manifest syntax
  fixture.
- `edition-selections.toml` defines the comprehensive volume and the smaller
  use-based editions as derived views of one inventory.
- `object.example.toml` is a non-evidentiary syntax fixture. Its prose is
  deliberately marked as placeholder text and must never be published.
- `object-record-api.tex` defines the TeX-side record interface expected from a
  generator. It contains presentation-neutral data setters, not page design.
- `validate_inventory.py` validates records, cross-record references,
  publication gates, and derived-edition selection.
- `test_validate_inventory.py` exercises the validator without adding
  dictionary entries.

## Validation

Keep canonical records one independently taught object per file under
`shared/objects/`. A subordinate functional set that is always prepared,
stored, presented, and understood together may use one record while retaining
the distinct names and functions of its components; the incense boat and
spoon are the controlling example. From this directory, validate them with:

```sh
python3 validate_inventory.py ../objects
python3 validate_inventory.py ../objects --list-edition ed-altar-server
python3 test_validate_inventory.py
```

The first command reports all structural, reference, and publication-gate
errors. The second prints the stable object IDs selected for one derived
edition after successful validation. An empty derived edition is valid while
the inventory is being developed; it is not evidence of completeness.

## Ownership and generated output

Authoritative object, variant, appearance, use, handling, symbolism, evidence,
and artwork records belong in TOML. TeX consumers receive generated calls to
the API; they must not restate facts in publication-local TeX. Generated TeX
is a reproducible intermediate and belongs under `build/`, not beside the
authoritative records.

The generator must:

1. parse TOML strictly and reject unknown fields;
2. validate IDs, enumerations, references, and unique `(object, variant)` keys;
3. resolve edition selection from tags and explicit exclusions;
4. reject publication of unverified required claims or unapproved artwork;
5. preserve the source order declared by each plate rather than alphabetizing
   silently;
6. escape all TeX-special characters; and
7. emit one `\RSDObjectRecord` block per selected object, followed by its
   names, claims, variants, sources, artwork, and cross-references.

Before generation, `tools/tpt check-roman-sanctuary-artwork` reconciles the
canonical `research/artwork-manifest.toml` against every populated record
under `shared/objects/`. The check is deliberately valid with an empty held
manifest and no object records. Once records exist, it rejects one-way links,
unknown objects or variants, missing normalized files, mismatched PNG
dimensions, mode, byte count, or hash, and incomplete publication-ready
object or substantive-variant coverage.

The manifest's `asset_files` table is exhaustive technical custody: every
tracked dictionary PNG, including a rejected or otherwise held lead, must
appear exactly once with its current byte identity and audit record.
Canonical publishing assets remain stripped 8-bit grayscale PNGs. An
8-bit grayscale-plus-alpha PNG is also eligible only when its custody row
declares `boundary_treatment = "transparent"`; the validator rejects alpha
under every opaque, framed, full-bleed, or legacy-undeclared boundary state.
Unreconciled artwork links on non-publication-ready object records are printed
as held notices so prototype development remains checkable; the same gap on a
publication-ready object is a validation error.

Selection controls inclusion, not wording. Audience-specific wording may be
stored only in the `audience_note` table of the same canonical object record.
It must not contradict or silently enlarge the verified base claims.

## Stable identifiers

All IDs are lowercase kebab-case with a namespace prefix:

- objects: `obj-...`
- variants: `var-...`
- claims: `clm-...`
- sources/bindings: `src-...`
- artwork: `art-...`
- plates: `plt-...`
- editions: `ed-...`

IDs survive renaming and rearrangement. Printed order, page number, and
filename are never identifiers.

## Evidence and completeness

An object can be inventoried before it is publishable. `workflow_state`
distinguishes a lead, an identified record, a source-audited record, an
art-reviewed record, a publication-ready record, and a held record. Concrete
source, claim, artwork, terminology, scope, rights, or variant defects belong
in `unresolved_gaps`; they do not create a deferred external-review workflow.
Every reader-facing factual field is represented by one or more claim records
with exact source bindings. A source-wide citation does not make every field
verified.

The canonical alpha generator admits a source-audited or later record only
when identity and governing status are resolved, every rendered factual claim
uses a claim-verified binding, artwork has canonical manifest identity and
rights/provenance, and each rendered asset has passed identity and basic
visual review. Editorial proposals remain in research data but are not
rendered as facts. This is the only active admission path; external review is
not a release gate.

An artwork custody row uses `canonical-alpha-eligible` when that exact asset
has completed the source, rights, identity, safety, and basic visual-usability
checks required by this path. `consumer-eligible` remains a narrower
consumer-specific state and does not admit an asset into another edition.
Assets with concrete unresolved defects remain `held`; the custody vocabulary
contains no external-review state.

Artwork IDs are shared identities, not object-local IDs. A comparison or
composition may therefore repeat the same artwork ID in each object record
listed by its `depicts` field. The validator requires the core artwork
definition to agree across those repetitions and requires each linking object
to appear in `depicts`; an object-local review note may differ. Generated
editions render a shared artwork with exactly one linking object. The optional
`render_owner` names that object explicitly; otherwise the first object in
`depicts` that links the artwork is the deterministic owner. An empty
`artwork` array is valid while a record is not publication-ready.
Publication-ready records still require approved artwork.

The comprehensive edition selects every alpha-admitted object within the
declared universal Roman 1962 corpus plus reviewed regional, religious-order,
and historical supplements. The historical section is ordered first by
period, then by functional type. Postconciliar status is intentionally absent:
a parallel postconciliar work must add edition-specific use records rather
than treating 1962 status as current.

The use-based editions are views:

- the altar-server edition includes everything that may be present around a
  server, including items the server only recognizes and must not touch;
- the sacristan edition selects preparation, placement, care, storage, and
  changeover relevance;
- the MC/trainer edition selects role, handoff, branch, cue, and recovery
  relevance;
- the general-reader edition selects a curated visual survey;
- the pontifical edition selects pontifical objects and the ordinary objects
  needed to understand their compositions.

No derived edition owns a copied inventory.
