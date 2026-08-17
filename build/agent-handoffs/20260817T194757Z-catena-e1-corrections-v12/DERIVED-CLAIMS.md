# Derived claims

**Every number in this file was computed by `logs/derive-claims.py` at seal time and written from the same pass that wrote `claims.json`.** Nothing here was typed. Where a document in this package states a figure, this is the source it states it from, and `logs/head-consistency.py` refuses a package whose prose names a commit these claims do not entitle it to name.

## Identity

| | |
| --- | --- |
| parent | `0255b84996e1dc24da3ce75ac318c4f774b7957c` |
| head | `d312786dd2b23926aa88e29ea15647dfcc7e7e6e` |
| review addressed | `22b9bdad5e71920a103e3ec3bcf2f79bba50cebb` |
| parent is an ancestor of head | True |
| working tree clean at head | True |

## Commits — 2

| # | sha | subject | files |
| --- | --- | --- | --- |
| 1 | `79a306fe50a98e8315d96bb9386c6fe4cacf6e89` | Take the request-critical state once, and hold what it said | `src/web/browser/catena/catena-model.js`<br>`tools/tests/test_catena_wave_1.py` |
| 2 | `d312786dd2b23926aa88e29ea15647dfcc7e7e6e` | Record the V12 lane: the record was asked once, and the ledger said which | `PROJECT-WORK.md`<br>`guidance/corpus-browser-master-plan.md`<br>`guidance/corpus-browser-roadmap.md`<br>`promised-deliverables.toml` |

## Diff — 6 file(s), 1285 insertion(s), 50 deletion(s)

| state | path | + | − |
| --- | --- | --- | --- |
| M | `PROJECT-WORK.md` | 160 | 0 |
| M | `guidance/corpus-browser-master-plan.md` | 1 | 1 |
| M | `guidance/corpus-browser-roadmap.md` | 85 | 1 |
| M | `promised-deliverables.toml` | 69 | 3 |
| M | `src/web/browser/catena/catena-model.js` | 131 | 20 |
| M | `tools/tests/test_catena_wave_1.py` | 839 | 25 |

## Payload — gzip -9, mtime 0

| file | parent whole | head whole | ceiling | parent stripped | head stripped | ceiling | parent comment share | head comment share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | 7629 | 7629 | 8000 | 2676 | 2676 | 2700 | 0.649 | 0.649 |
| `src/web/browser/catena/catena.js` | 12980 | 12980 | 13000 | 7554 | 7554 | 8800 | 0.418 | 0.418 |
| `src/web/browser/catena/catena-model.js` | 32406 | 34367 | none | 7973 | 8258 | none | 0.754 | 0.76 |

The page and the model together, because neither measure alone is the load a reader pays:

| | parent | head | delta |
| --- | --- | --- | --- |
| compressed as one stream | 44643 | 46581 | +1938 |
| compressed separately and summed | 45386 | 47347 | +1961 |

## Test delta

| | |
| --- | --- |
| `CORRECTED ORACLE` blocks | 23 |
| corrected blocks by marking lane | `?` 1, `V6` 8, `V7` 14 |
| classes holding a corrected oracle | 14 |
| test classes added | 2 |

Each block's marker tag names the lane that corrected it; nothing here assumes they all belong to one round.

Classes holding a corrected oracle: `ActionPartialArrivalTerminalStateTest`, `FindingOrderIndependenceTest`, `FrozenContractTest`, `GenuinelyLateStaleWorkTest`, `MalformedLanguageAttributeTest`, `MalformedRecordRenderingTest`, `MixedCollectionMemberTest`, `NumericVerseAndPathTest`, `RenderedScriptureTruthTest`, `RoutableIdentityTest`, `TypedAbsenceFindingTest`, `UnsupportedVoiceTest`, `UntypedProvenanceTest`, `V7UnreadableRootDomainClaimTest`.

### The V12 test file at the parent

The head's test file — the V12 file — replayed against the PARENT's production files: same scenarios, same oracles, other code. The decomposition, reported separately:

| | |
| --- | --- |
| methods run | 488 |
| control methods passing at the parent | 477 |
| methods failing at the parent | 11 |
| failing subtest identities | 12 |
| classes with a failure | 4 (2 added by V12, 2 pre-existing with a corrected oracle) |

Failing subtest identities at the parent:

- `ERROR: test_a_carried_path_descriptor_is_read_once_and_never_twice (test_catena_wave_1.V12StableRequestSnapshotTest.test_a_carried_path_descriptor_is_read_once_and_never_twice)`
- `FAIL: test_a_drifting_carried_descriptor_never_reaches_its_second_value (test_catena_wave_1.V12PlantedRequestSinkTest.test_a_drifting_carried_descriptor_never_reaches_its_second_value)`
- `FAIL: test_a_prewarmed_body_is_not_substituted_into_a_contaminated_route (test_catena_wave_1.V12PlantedRequestSinkTest.test_a_prewarmed_body_is_not_substituted_into_a_contaminated_route)`
- `FAIL: test_an_inherited_refusal_marker_closes_an_own_valid_claim (test_catena_wave_1.V12StableRequestSnapshotTest.test_an_inherited_refusal_marker_closes_an_own_valid_claim)`
- `FAIL: test_an_inherited_refusal_marker_reaches_no_request_or_body (test_catena_wave_1.V12PlantedRequestSinkTest.test_an_inherited_refusal_marker_reaches_no_request_or_body) (scenario='v12-inherited-refusal-carried')`
- `FAIL: test_an_inherited_refusal_marker_reaches_no_request_or_body (test_catena_wave_1.V12PlantedRequestSinkTest.test_an_inherited_refusal_marker_reaches_no_request_or_body) (scenario='v12-inherited-refusal-valid-prefix')`
- `FAIL: test_an_inherited_spine_prefix_reaches_no_request_cache_or_body (test_catena_wave_1.V12PlantedRequestSinkTest.test_an_inherited_spine_prefix_reaches_no_request_cache_or_body)`
- `FAIL: test_an_inherited_valid_spine_prefix_never_becomes_absence (test_catena_wave_1.V12StableRequestSnapshotTest.test_an_inherited_valid_spine_prefix_never_becomes_absence)`
- `FAIL: test_no_inherited_or_accessor_claim_member_reopens_anything (test_catena_wave_1.V11InheritedClaimBoundaryTest.test_no_inherited_or_accessor_claim_member_reopens_anything)`
- `FAIL: test_the_model_is_byte_identical (test_catena_wave_1.FrozenContractTest.test_the_model_is_byte_identical)`
- `FAIL: test_the_source_names_a_request_critical_field_only_at_the_snapshot (test_catena_wave_1.V12StableRequestSnapshotTest.test_the_source_names_a_request_critical_field_only_at_the_snapshot)`
- `FAIL: test_the_spine_is_asked_for_its_own_prefix_too (test_catena_wave_1.V11InheritedClaimBoundaryTest.test_the_spine_is_asked_for_its_own_prefix_too)`

Classes V12 adds that do **not** fail at the parent: none. A class that passes at both ends closes a proof gap rather than a defect, and saying otherwise is the claim the V6 roadmap made against its own evidence.

## Suites

| suite | tests | failures | errors | skips | outcome | FAIL/ERROR identities |
| --- | --- | --- | --- | --- | --- | --- |
| browser_static_head | 5 | 0 | 0 | 0 | OK | 0 |
| focused_catena_head | 544 | 0 | 0 | 0 | OK | 0 |
| focused_catena_parent | 534 | 0 | 0 | 0 | OK | 0 |
| full_discovery_head | 1895 | 14 | 13 | 11 | FAILED | 27 |
| full_discovery_parent | 1885 | 14 | 13 | 11 | FAILED | 27 |
| head_tests_against_parent | 488 | 11 | 1 | 0 | FAILED | 12 |
| sealer | 123 | 0 | 0 | 0 | OK | 0 |

Full-discovery FAIL/ERROR identity sets at parent and head are **identical** — 27 entries, 0 only at the head, 0 only at the parent, 0 mentioning catena.

## Browser gate

| | parent | head |
| --- | --- | --- |
| browser | Chrome/151.0.7922.137 | Chrome/151.0.7922.137 |
| assertions | 2290 | 2290 |
| failed | 226 | 226 |
| pages | 171 | 171 |
| passed | 1836 | 1836 |
| routes | 19 | 19 |
| skipped | 228 | 228 |
| states | 9 | 9 |

Failure categories at the head: `primary-controls-meet-target-size` 82, `single-main-element` 117, `skip-link-targets-existing-element` 27.

## Package

The inventory below covers ONLY the members frozen before this file was written. A member written at or after the derivation is named under *derived members*, never sized or hashed: its bytes did not exist when the rows froze, and a number typed for it here would be the V8 defect this file corrects. The package-total and final-byte authority is `MANIFEST.sha256` together with the ZIP and its sidecar.

| | |
| --- | --- |
| evidence members (frozen) | 75 |
| evidence bytes (sum of the rows) | 4229353 |
| derived members (named, unsized) | 6 |
| PNGs | 12 |
| before/after raster pairs | 6 |
| unpaired captures | 0 |

Derived members:

- `claims.json` — written by this derivation; it cannot inventory its own bytes
- `DERIVED-CLAIMS.md` — rendered from claims.json in the same pass that writes it
- `logs/attempts.json` — the attempt ledger rows this package was built from, composed after the consistency audit so it can carry this attempt's own terminal row
- `logs/attempt-05/derive-claims.log` — transcript of this derivation, written as the derivation prints
- `logs/attempt-05/head-consistency.log` — transcript of the consistency audit, which runs after this derivation
- `MANIFEST.sha256` — written by the manifest phase, after every other member is frozen

## Byte and control scan

70 file(s) scanned for NUL, carriage returns, forbidden control characters and invalid UTF-8: **clean**.
