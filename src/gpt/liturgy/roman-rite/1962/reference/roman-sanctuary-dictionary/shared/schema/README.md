# Roman Sanctuary Dictionary Data Contract

This directory defines the declarative boundary between researched object
records, audience selections, artwork, and TeX rendering. It does not contain
verified object claims. A populated record may be rendered only after its
claim-level evidence and artwork review states permit that use.

## Files

- `inventory-schema.toml` is the normative field and controlled-vocabulary
  contract.
- `edition-selections.toml` defines the comprehensive volume and the smaller
  use-based editions as derived views of one inventory.
- `object.example.toml` is a non-evidentiary syntax fixture. Its prose is
  deliberately marked as placeholder text and must never be published.
- `object-record-api.tex` defines the TeX-side record interface expected from a
  generator. It contains presentation-neutral data setters, not page design.

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
distinguishes a lead, an identified record, a source-audited record, and a
publication-ready record. Every reader-facing factual field is represented by
one or more claim records with exact source bindings. A source-wide citation
does not make every field verified.

The comprehensive edition selects every publication-ready object within the
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
