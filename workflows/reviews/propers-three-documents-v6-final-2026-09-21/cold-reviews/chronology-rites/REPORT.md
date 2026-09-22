# Final cold review: chronology contract and rite isolation

**Verdict: PASS**

Reviewed the exact working-tree subjects listed in `HASHES.sha256` with repository `HEAD` at `6caf8946d2b78d6733c47b89deda3c1c89c8750b`. No release blocker remains in the assigned chronology, provenance, source-rights, component-closure, or TLM/postconciliar isolation scope. This review made no tracked edits, builds, workflow advances, commits, or installs.

## Comparison-profile sealing

All four target leaves declare one leaf-owned `critical-matthew-composition` selection. It requests `catholic-critical-v1` only for the Gospel `composition` relation and `critical.gospel-of-matthew`. The generated schema-3 records carry that answer under `profile_comparisons`, with its requested and returned profiles, sources, and complete reach. The subject is absent from every element's default `claims` and `publication_claims`. Generated TeX preserves the same boundary through the dedicated comparison group and claim macros.

The selection loader rejects wrong document identity, default-profile cascade, missing selection, wrong relation or subject, symlinks, and paths outside the exact leaf. Existing leaves without comparisons remain schema 2 and byte-stable; the final 566-test run includes the legacy record and annotation regressions.

## Manual chronology claims

The content preflight now checks era-qualified manual dates throughout each edition and era-less date prose inside the date-dossier API. Direction and precision are semantic: after/post, before/pre, approximate, and exact are distinct. Raw sortable endpoints no longer authorize prose that drops an approximate source label. A nearby era-qualified date also cannot mask a separate era-less date; only overlap with the same recognized date suppresses the era-less diagnostic. The direct adversarial probe produced:

- `about A.D. 50; about 140--142` -> the era-less range remains detectable;
- `about 140--142; about A.D. 50` -> the era-less range remains detectable;
- `about A.D. 140--142` and `about 140--142 A.D.` -> no false era-omission finding.

All four target leaves pass `chronology-claims-supported` after restoring the canonical approximate wording of the Matthew alternatives.

## Entrance-antiphon basis

Both postconciliar inputs identify Psalm 37:39-40 in Hebrew numbering as `kind = "identified-basis"`. Both generated records resolve that basis to Vulgate Psalm 36:39-40. Their source-owner records consistently describe the antiphon as composed text whose identified scriptural basis is Psalm 37:39-40; no residual “no identified verse” claim remains. The chronology date therefore belongs to the Psalm basis and does not purport to date the composed antiphon.

## Isaiah relations

The former whole-book composition assertion has been replaced by two scoped relations:

- `traditional-attribution` associates the book with Isaias and displays 740-701 B.C. only as the ministry/reference era in Souvay's traditional account. The notes expressly deny that this dates each oracle, the book's writing or assembly, or the prophet's death.
- `prophecy-given` applies the NABRE critical horizon only to Isaiah 40-55 and describes prophetic activity toward the end of the Babylonian exile. It reaches Isaiah 55 but neither Isaiah 39 nor 56, and it imports no unsupported absolute year from Cyrus's decree.

Both postconciliar records and annotations carry those relations separately. No live `composition.book-of-isaias` unit or claim remains.

## Official-source provenance and rights

The official USCCB NABRE Isaiah, Matthew, and Psalms introduction records identify their official URLs, retrieval date, byte sizes, and SHA-256 digests. Their artifacts are `storage = "restricted"`, `rights_status = "restricted"`, and `indexable = false`; the repository retains bounded passage summaries rather than protected payloads. `source-library validate` passes with 2,746 artifacts, 992 editions, 5,182 passages, 89 segments, 726 works, and 2,867 bindings. Each target binding fingerprint is current, and each relevant source is cataloged, acquired, and inspected. All four leaf rights checks report that restricted sources are not reproduced.

The refreshed publication source inventory also passes: 142 publications, 2,305 source-surface files, and 11 owners.

## Absolute rite isolation

The four manifests have the correct calendar family, outputs, components, sources, and entrypoints. The component validator constrains every reference/import to the same provider and liturgical family (or approved common material), and the postconciliar adapter resolves only the same edition's canonical owners. It has no 1962 fallback. The direct audit examined 159 path-valued liturgical references and found zero cross-family paths or bindings.

Direct scans found no 1962 tree path or calendar in either postconciliar leaf and no postconciliar tree path or calendar in either 1962 leaf. The active Claude 1962 research no longer applies postconciliar Ordinary Time or semi-continuous-Lectionary premises: its historical argument rests on the 1962 Missal's own Pauline sequence and Time-after-Pentecost transmission. Its only active uses of “postconciliar” are explicit exclusion statements. Older evaluation packets preserve earlier workflow snapshots but are not imported by any manifest, research dependency, document entrypoint, generated record, or source binding.

Shared NABRE introductions are external Scripture sources, not liturgical-tree imports. Their Matthew use in the TLM leaves is the explicitly selected comparison evidence and remains sealed from the default answer.

## Final verification

- 566 chronology, derivation-lineage, content-preflight, annotation, postconciliar-adapter, component, source-inventory, source-library, and workflow tests passed in 198.295 seconds.
- All 8 generated record/annotation checks passed.
- All 4 complete leaf content-preflight sweeps passed.
- Direct contract audit: 4 records, 4 comparison selections, 2 postconciliar Entrance inputs, 2 postconciliar Isaiah dossiers, 0 problems.
- Direct rite audit: 4 leaves, 159 path-valued liturgical references, 0 problems.
- Scripture chronology validation and coverage check passed: 3 profiles, 287 events, 77 composition units, 382 bindings, 23 gaps, 73 books; 1,883 coverage rows and no missing dates in the enumerated universe.
- `git diff --check`, source-library validation, source-inventory validation, active semantic scans, cross-tree path scans, and all 101 subject-hash checks passed.

The command transcript is in `COMMANDS.md`; exact reviewed bytes are bound by `HASHES.sha256`.
