# Derived claims

**Every number in this file was computed by `logs/derive-claims.py` at seal time and written from the same pass that wrote `claims.json`.** Nothing here was typed. Where a document in this package states a figure, this is the source it states it from, and `logs/head-consistency.py` refuses a package whose prose names a commit these claims do not entitle it to name.

## Identity

| | |
| --- | --- |
| parent | `3c5b78249193df065c4e1c2ee5a98e5989c6e582` |
| head | `ea15d16d22d7ceaed989ed9907c236f967738a03` |
| review addressed | `55df5c236a1dfda12bb974efdbb9f46d0aeb3436` |
| parent is an ancestor of head | True |
| working tree clean at head | True |

## Commits — 3

| # | sha | subject | files |
| --- | --- | --- | --- |
| 1 | `78bf44b784e1e77d36317fe653832985f61bd28b` | Carry the refusal to the reader, and close the claim boundary behind it | `src/web/browser/catena/catena-model.js`<br>`src/web/browser/catena/catena.js` |
| 2 | `c51d0535366b4090cdf035e0ae56822721bfa9d6` | Pin the four terminal vectors exactly, and give every request an owner | `tools/tests/test_catena_wave_1.py` |
| 3 | `ea15d16d22d7ceaed989ed9907c236f967738a03` | Record the V10 lane: the refusal said truthfully, and the vectors pinned | `PROJECT-WORK.md`<br>`guidance/corpus-browser-roadmap.md`<br>`promised-deliverables.toml` |

## Diff — 6 file(s), 567 insertion(s), 58 deletion(s)

| state | path | + | − |
| --- | --- | --- | --- |
| M | `PROJECT-WORK.md` | 133 | 0 |
| M | `guidance/corpus-browser-roadmap.md` | 40 | 1 |
| M | `promised-deliverables.toml` | 54 | 0 |
| M | `src/web/browser/catena/catena-model.js` | 33 | 6 |
| M | `src/web/browser/catena/catena.js` | 7 | 0 |
| M | `tools/tests/test_catena_wave_1.py` | 300 | 51 |

## Payload — gzip -9, mtime 0

| file | parent whole | head whole | ceiling | parent stripped | head stripped | ceiling | parent comment share | head comment share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | 7629 | 7629 | 8000 | 2676 | 2676 | 2700 | 0.649 | 0.649 |
| `src/web/browser/catena/catena.js` | 12901 | 12987 | 13000 | 7530 | 7565 | 8800 | 0.416 | 0.417 |
| `src/web/browser/catena/catena-model.js` | 29179 | 29741 | none | 7571 | 7664 | none | 0.741 | 0.742 |

The page and the model together, because neither measure alone is the load a reader pays:

| | parent | head | delta |
| --- | --- | --- | --- |
| compressed as one stream | 41392 | 42010 | +618 |
| compressed separately and summed | 42080 | 42728 | +648 |

## Test delta

| | |
| --- | --- |
| `CORRECTED ORACLE` blocks | 23 |
| corrected blocks by marking lane | `?` 1, `V6` 8, `V7` 14 |
| classes holding a corrected oracle | 14 |
| test classes added | 1 |

Each block's marker tag names the lane that corrected it; nothing here assumes they all belong to one round.

Classes holding a corrected oracle: `ActionPartialArrivalTerminalStateTest`, `FindingOrderIndependenceTest`, `FrozenContractTest`, `GenuinelyLateStaleWorkTest`, `MalformedLanguageAttributeTest`, `MalformedRecordRenderingTest`, `MixedCollectionMemberTest`, `NumericVerseAndPathTest`, `RenderedScriptureTruthTest`, `RoutableIdentityTest`, `TypedAbsenceFindingTest`, `UnsupportedVoiceTest`, `UntypedProvenanceTest`, `V7UnreadableRootDomainClaimTest`.

### The V10 test file at the parent

The head's test file — the V10 file — replayed against the PARENT's production files: same scenarios, same oracles, other code. The decomposition, reported separately:

| | |
| --- | --- |
| methods run | 466 |
| control methods passing at the parent | 458 |
| methods failing at the parent | 8 |
| failing subtest identities | 10 |
| classes with a failure | 5 (1 added by V10, 4 pre-existing with a corrected oracle) |

Failing subtest identities at the parent:

- `FAIL: test_a_late_fallback_cannot_touch_the_refused_terminal_state (test_catena_wave_1.V9ComposedPrefixFallbackClosureTest.test_a_late_fallback_cannot_touch_the_refused_terminal_state) (snapshot='a-late')`
- `FAIL: test_a_late_fallback_cannot_touch_the_refused_terminal_state (test_catena_wave_1.V9ComposedPrefixFallbackClosureTest.test_a_late_fallback_cannot_touch_the_refused_terminal_state) (snapshot='b-opened')`
- `FAIL: test_a_prewarmed_fallback_is_not_substituted_into_the_refused_route (test_catena_wave_1.V9ComposedPrefixFallbackClosureTest.test_a_prewarmed_fallback_is_not_substituted_into_the_refused_route)`
- `FAIL: test_each_refused_fragment_states_its_own_terminal_claim (test_catena_wave_1.V8TextNamespaceRequestSinkTest.test_each_refused_fragment_states_its_own_terminal_claim)`
- `FAIL: test_every_contradictory_direct_claim_fails_closed (test_catena_wave_1.V10RefusedPresentationTest.test_every_contradictory_direct_claim_fails_closed)`
- `FAIL: test_the_model_is_byte_identical (test_catena_wave_1.FrozenContractTest.test_the_model_is_byte_identical)`
- `FAIL: test_the_reader_is_told_rather_than_left_loading (test_catena_wave_1.UnsafeTextPrefixTest.test_the_reader_is_told_rather_than_left_loading)`
- `FAIL: test_the_refused_route_terminates_truthfully_cold (test_catena_wave_1.V9ComposedPrefixFallbackClosureTest.test_the_refused_route_terminates_truthfully_cold) (scenario='v9-padded-prefix-carried')`
- `FAIL: test_the_refused_route_terminates_truthfully_cold (test_catena_wave_1.V9ComposedPrefixFallbackClosureTest.test_the_refused_route_terminates_truthfully_cold) (scenario='v9-refused-prefix-carried')`
- `FAIL: test_the_two_no_text_states_are_visibly_distinct (test_catena_wave_1.V10RefusedPresentationTest.test_the_two_no_text_states_are_visibly_distinct)`

Classes V10 adds that do **not** fail at the parent: none. A class that passes at both ends closes a proof gap rather than a defect, and saying otherwise is the claim the V6 roadmap made against its own evidence.

## Suites

| suite | tests | failures | errors | skips | outcome | FAIL/ERROR identities |
| --- | --- | --- | --- | --- | --- | --- |
| browser_static_head | 5 | 0 | 0 | 0 | OK | 0 |
| focused_catena_head | 522 | 0 | 0 | 0 | OK | 0 |
| focused_catena_parent | 519 | 0 | 0 | 0 | OK | 0 |
| full_discovery_head | 1873 | 14 | 13 | 11 | FAILED | 27 |
| full_discovery_parent | 1870 | 14 | 13 | 11 | FAILED | 27 |
| head_tests_against_parent | 466 | 10 | 0 | 0 | FAILED | 10 |
| sealer | 91 | 0 | 0 | 0 | OK | 0 |

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
| evidence members (frozen) | 54 |
| evidence bytes (sum of the rows) | 2060250 |
| derived members (named, unsized) | 5 |
| PNGs | 0 |
| before/after raster pairs | 0 |
| unpaired captures | 0 |

Derived members:

- `claims.json` — written by this derivation; it cannot inventory its own bytes
- `DERIVED-CLAIMS.md` — rendered from claims.json in the same pass that writes it
- `logs/derive-claims.log` — transcript of this derivation, written as the derivation prints
- `logs/head-consistency.log` — transcript of the consistency audit, which runs after this derivation
- `MANIFEST.sha256` — written by the manifest phase, after every other member is frozen

## Byte and control scan

61 file(s) scanned for NUL, carriage returns, forbidden control characters and invalid UTF-8: **clean**.
