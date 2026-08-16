# Derived claims

**Every number in this file was computed by `logs/derive-claims.py` at seal time and written from the same pass that wrote `claims.json`.** Nothing here was typed. Where a document in this package states a figure, this is the source it states it from, and `logs/head-consistency.py` refuses a package whose prose names a commit these claims do not entitle it to name.

## Identity

| | |
| --- | --- |
| parent | `ea15d16d22d7ceaed989ed9907c236f967738a03` |
| head | `0255b84996e1dc24da3ce75ac318c4f774b7957c` |
| review addressed | `f7cad8b0219de8343a0b2cce95e89558ded6946e` |
| parent is an ancestor of head | True |
| working tree clean at head | True |

## Commits — 2

| # | sha | subject | files |
| --- | --- | --- | --- |
| 1 | `3b93f74f032e74de9a50c1e2f1b35aa5b567f8d8` | Ask the claim for its own members, and say no more than they establish | `src/web/browser/catena/catena-model.js`<br>`src/web/browser/catena/catena.js`<br>`tools/tests/test_catena_wave_1.py` |
| 2 | `0255b84996e1dc24da3ce75ac318c4f774b7957c` | Record the V11 lane: the members asked, and the vectors said whole | `PROJECT-WORK.md`<br>`guidance/corpus-browser-master-plan.md`<br>`guidance/corpus-browser-roadmap.md`<br>`promised-deliverables.toml` |

## Diff — 7 file(s), 1208 insertion(s), 47 deletion(s)

| state | path | + | − |
| --- | --- | --- | --- |
| M | `PROJECT-WORK.md` | 173 | 1 |
| M | `guidance/corpus-browser-master-plan.md` | 1 | 1 |
| M | `guidance/corpus-browser-roadmap.md` | 90 | 1 |
| M | `promised-deliverables.toml` | 76 | 4 |
| M | `src/web/browser/catena/catena-model.js` | 168 | 23 |
| M | `src/web/browser/catena/catena.js` | 1 | 1 |
| M | `tools/tests/test_catena_wave_1.py` | 699 | 16 |

## Payload — gzip -9, mtime 0

| file | parent whole | head whole | ceiling | parent stripped | head stripped | ceiling | parent comment share | head comment share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | 7629 | 7629 | 8000 | 2676 | 2676 | 2700 | 0.649 | 0.649 |
| `src/web/browser/catena/catena.js` | 12987 | 12980 | 13000 | 7565 | 7554 | 8800 | 0.417 | 0.418 |
| `src/web/browser/catena/catena-model.js` | 29741 | 32406 | none | 7664 | 7973 | none | 0.742 | 0.754 |

The page and the model together, because neither measure alone is the load a reader pays:

| | parent | head | delta |
| --- | --- | --- | --- |
| compressed as one stream | 42010 | 44643 | +2633 |
| compressed separately and summed | 42728 | 45386 | +2658 |

## Test delta

| | |
| --- | --- |
| `CORRECTED ORACLE` blocks | 23 |
| corrected blocks by marking lane | `?` 1, `V6` 8, `V7` 14 |
| classes holding a corrected oracle | 14 |
| test classes added | 3 |

Each block's marker tag names the lane that corrected it; nothing here assumes they all belong to one round.

Classes holding a corrected oracle: `ActionPartialArrivalTerminalStateTest`, `FindingOrderIndependenceTest`, `FrozenContractTest`, `GenuinelyLateStaleWorkTest`, `MalformedLanguageAttributeTest`, `MalformedRecordRenderingTest`, `MixedCollectionMemberTest`, `NumericVerseAndPathTest`, `RenderedScriptureTruthTest`, `RoutableIdentityTest`, `TypedAbsenceFindingTest`, `UnsupportedVoiceTest`, `UntypedProvenanceTest`, `V7UnreadableRootDomainClaimTest`.

### The V11 test file at the parent

The head's test file — the V11 file — replayed against the PARENT's production files: same scenarios, same oracles, other code. The decomposition, reported separately:

| | |
| --- | --- |
| methods run | 478 |
| control methods passing at the parent | 471 |
| methods failing at the parent | 7 |
| failing subtest identities | 7 |
| classes with a failure | 3 (2 added by V11, 1 pre-existing with a corrected oracle) |

Failing subtest identities at the parent:

- `ERROR: test_no_inherited_or_accessor_claim_member_reopens_anything (test_catena_wave_1.V11InheritedClaimBoundaryTest.test_no_inherited_or_accessor_claim_member_reopens_anything)`
- `ERROR: test_the_model_and_the_page_cannot_drift_apart (test_catena_wave_1.V11UnestablishedPresentationTest.test_the_model_and_the_page_cannot_drift_apart)`
- `FAIL: test_every_unestablished_prefix_says_only_that (test_catena_wave_1.V11UnestablishedPresentationTest.test_every_unestablished_prefix_says_only_that)`
- `FAIL: test_the_model_is_byte_identical (test_catena_wave_1.FrozenContractTest.test_the_model_is_byte_identical)`
- `FAIL: test_the_ordinary_claims_the_boundary_does_honour_are_unchanged (test_catena_wave_1.V11InheritedClaimBoundaryTest.test_the_ordinary_claims_the_boundary_does_honour_are_unchanged)`
- `FAIL: test_the_projection_carries_only_own_data_properties (test_catena_wave_1.V11InheritedClaimBoundaryTest.test_the_projection_carries_only_own_data_properties)`
- `FAIL: test_the_spine_is_asked_for_its_own_prefix_too (test_catena_wave_1.V11InheritedClaimBoundaryTest.test_the_spine_is_asked_for_its_own_prefix_too)`

Classes V11 adds that do **not** fail at the parent: `V11RendererOrderTest`. A class that passes at both ends closes a proof gap rather than a defect, and saying otherwise is the claim the V6 roadmap made against its own evidence.

## Suites

| suite | tests | failures | errors | skips | outcome | FAIL/ERROR identities |
| --- | --- | --- | --- | --- | --- | --- |
| browser_static_head | 5 | 0 | 0 | 0 | OK | 0 |
| focused_catena_head | 534 | 0 | 0 | 0 | OK | 0 |
| focused_catena_parent | 522 | 0 | 0 | 0 | OK | 0 |
| full_discovery_head | 1885 | 14 | 13 | 11 | FAILED | 27 |
| full_discovery_parent | 1873 | 14 | 13 | 11 | FAILED | 27 |
| head_tests_against_parent | 478 | 5 | 2 | 0 | FAILED | 7 |
| sealer | 106 | 0 | 0 | 0 | OK | 0 |

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
| evidence members (frozen) | 90 |
| evidence bytes (sum of the rows) | 6878050 |
| derived members (named, unsized) | 5 |
| PNGs | 31 |
| before/after raster pairs | 8 |
| unpaired captures | 0 |

Derived members:

- `claims.json` — written by this derivation; it cannot inventory its own bytes
- `DERIVED-CLAIMS.md` — rendered from claims.json in the same pass that writes it
- `logs/derive-claims.log` — transcript of this derivation, written as the derivation prints
- `logs/head-consistency.log` — transcript of the consistency audit, which runs after this derivation
- `MANIFEST.sha256` — written by the manifest phase, after every other member is frozen

## Byte and control scan

67 file(s) scanned for NUL, carriage returns, forbidden control characters and invalid UTF-8: **clean**.
