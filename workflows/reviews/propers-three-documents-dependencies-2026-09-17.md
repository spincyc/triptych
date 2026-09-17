# Dependency guidance cold review — 2026-09-17

Scope: the new paragraph under `Research before interpretation` in `guidance/liturgy/propers-three-documents.md`, checked against `scripts/_proper_study.py`, the source-library ancestry implementation, and the governing source/editorial rules. This is a bounded review of the dependency-audit clarification, not acceptance of the complete implementation or either publication.

## Initial finding

Initial verdict: **revision required** for profile SHA-256 `70f7961327d16c968f75f3ec7af33827ebb0bea7c780e42f740c1754b3bf1511`, at HEAD `af9b2d10a98a6aac2ce44cc84d6358ede8e630e8`.

**D1 — State how separately owned rights evidence enters the research seal.** At profile lines 94–99, saying that registered bindings seal their ancestry and directing rights evidence through source records does not explain that a prose reference to a separate rights inventory is not a traversed dependency. `bound_evidence()` in `scripts/_proper_study.py:147–178` includes each reached record, the IDs returned by `tools/source-library:_dependency_ids`, and any available payload. The ancestry function at `tools/source-library:904–935` does not follow paths in `rights_basis`, notes, or comments. The rights fields themselves are included in the record hash; the separately referenced file is not.

A concrete repository case is the 1962 Missal facsimile record: `src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1962/artifacts/cmaa-facsimile-pdf/artifact.toml` refers to `src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml`. The current 1962 publication's `research/review-dependencies.toml` explicitly lists that inventory, which is the necessary coverage to preserve. `guidance/sources.md:481–493` deliberately gives recurring rights judgments this separate owner. Omitting that explicit path while leaving its prose reference unchanged would leave a later inventory edit outside the bound-source traversal.

Required result: retain the `src/` restriction and exclusion of global guidance, `THIRD_PARTY.md`, and workflow review receipts as external source owners, but explicitly require controlling source-specific rights, permission, or collation records under `src/` in `research/review-dependencies.toml` unless already reached through registered binding ancestry. State that prose links alone do not establish a dependency edge. Owner: the three-document profile; no workflow or tooling change is necessary for this clarification.

The coordinator accepted D1 and proposed this explicit coverage amendment. No other defect was found in the paragraph: `research_dependencies()` enforces the `src/` boundary, and `bound_evidence()` supplies registered record ancestry and available payload bytes to the research review seal.

## Corrected paragraph re-review — 2026-09-17

Final verdict: **PASS** for profile SHA-256 `5864b809bb822b5892ca680e0316ad15c7918223ef49426c608f3550932c348c`.

Independently read the revised paragraph at profile lines 94–101. **D1 is resolved.** It now explicitly requires declaration of controlling rights inventories, permission evidence, and collation records beneath `src/` unless registered binding ancestry already reaches them. It also states that a prose link does not add a sealed dependency. This matches the two implemented inclusion routes: explicit paths handled by `research_dependencies()` and registered ancestry/payloads handled by `bound_evidence()`.

The correction preserves the separate rights-record owner required by `guidance/sources.md` and does not require duplicating its reasoning inside every artifact. Global policy and receipts remain controls or audit references, while the source-specific facts governing a publication's rights remain review inputs. No outstanding findings in this bounded clarification. `git diff --check -- guidance/liturgy/propers-three-documents.md` returned exit status 0.

## Verification boundary

This review used read-only source inspection. No implementation tests, complete research seals, rights merits, authored studies, or workflow acceptance events were verified. No subject file, frozen workflow definition, fragment, or tracked review copy was edited.

Inspected implementation and guidance hashes:

| File | SHA-256 |
| --- | --- |
| `scripts/_proper_study.py` | `d1fc61e47a08d8b39f2d5f95b25802b1e9748f48767e36c1517ce25ca75f2fe3` |
| `tools/source-library` | `092afe66161760f85431a4607def60b44af4b7c7370eb6f6953d50601cc4eee1` |
| `guidance/sources.md` | `645485a0bdfe000fed2126a44a66bf6ac4f6f9bd5d963c4689bf907a2effd70a` |
| `guidance/editorial.md` | `97ef02ac4ac914b1a1c18b60f447d741643ff9977adb949684c84da98c4b4777` |
