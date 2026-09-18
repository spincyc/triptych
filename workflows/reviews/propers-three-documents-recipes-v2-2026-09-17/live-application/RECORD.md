# Actual live v2 application and verification

Coordinator record. Both real productions had reached **ACCEPTED** and their
terminal archives were complete before the prepared patch was applied. This
records execution and identities; the separate final integration review owns
independent acceptance of the integrated result.

The applied patch is the final six-file preparation:
`55622214a655db4414b196319274d2ebbc528e268b44230ffd9447427bc85a13`.
The original five-file variants were not applied. Before execution the
coordinator verified the exact reviewed patch, guard-helper and base-hash
manifest identities; the guard checked both real terminal states against their
immutable manifests and checked every old/new subject hash.

| Actual command | Exit | Result |
| --- | ---: | --- |
| `python3 .scratch/workflow-audit/v2-installation-preparation/apply-prepared.py --repo . --apply` | 0 | Applied exactly the six approved result files. `v2-live-application.log`, `v2-applied-subjects.json`. |
| `python3 -m unittest tools.tests.test_workflow_proper_study tools.tests.test_workflow_proper_study_recipes tools.tests.test_workflow_engine tools.tests.test_workflow_determinism tools.tests.test_workflow_seed_idempotency -q` | 0 | 106 tests passed in the live tree, no skips; `v2-live-tests.log`. Temporary fixtures were routed under the task scratch directory; bytecode writes were disabled. |
| Four `tools/tpt proper-study <owning-id> status/replay <run-id>` commands, expanded exactly in `v1-after-v2-checks.json` | 0 each | Both original runs still report ACCEPTED, original v1 identity, and intact terminal packets. |
| `make document-catalogue` | 0 | 142 works, 194 documents, 218 issues, 6,220 pages. Only the top-level current-workflow declaration changed; every work record remains equal. |

The current definition is proper-study v2, digest
`4e4bbd64b71b60bd9e04c9fa7592ecb52c85e05cad1349c41941fa4d31e4e4d2`.
`v2-applied-subjects.json` identifies all six exact applied files. Both actual
Sunday productions remain v1, digest
`1375f708d8670b2f4ccaf1869cfaa6fe67fe6946dc2b962c766bcdc499d3b47e`,
seeded at `af9b2d10a98a6aac2ce44cc84d6358ede8e630e8`. Their actual state and
immutable-manifest files remained byte-identical across application; before
identities and after status/replay captures are retained here. A real v2 Sunday
production is not claimed. Terminal replay reports `deterministic=null` and
`recorded_file_intact=true`; it checks integrity, not historical recompilation.

`final-artifact-identity.json` independently exports exact current review-result
hashes, all six installed/build/accepted PDF identities and page counts, and
both installed/build/accepted web identities. All final accepted review seals
were checked against current files before export. This does not constitute a
new scholarly or visual review.

The final source-inventory refresh preserves all 142 reviewed classification
arrays. The source-family ledger retains 153 pending units, no screened
families, and no claim of complete family screening. The document projection
keeps the publications' produced-v1 records while declaring the current v2
workflow separately. Scoped binding refresh adopts only that changed document
projection. Final source/release checks and integration review are recorded
in the production evaluation and integration evidence.

The archive manifest maps these verbatim captures to their original working
paths. Referenced preparation scripts and temporary fixtures are not included
here; their exact independently reviewed identities remain in the preparation
reviews. Original commands, failures and limits have not been rewritten.
