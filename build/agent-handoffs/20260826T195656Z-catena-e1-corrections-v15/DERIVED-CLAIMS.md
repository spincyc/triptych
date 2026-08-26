# Derived claims

**Every number in this file was computed by `logs/derive-claims.py` at seal time and written from the same pass that wrote `claims.json`.** Nothing here was typed. Where a document in this package states a figure, this is the source it states it from, and `logs/head-consistency.py` refuses a package whose prose names a commit these claims do not entitle it to name.

## Identity

| | |
| --- | --- |
| parent | `69f2575421ba976271c936b1abd4b39dbe8b98fd` |
| head | `b9202882badbbbc364f1dd3d9057d2710ee47552` |
| review addressed | `0d11766ec232b2b4e46a7d1b0ada56ef22370004` |
| parent is an ancestor of head | True |
| working tree clean at head | True |
| workspace mode | `fresh-clone` |
| linked worktree | False |
| git dir kind | `directory` |

## Commits — 4

| # | sha | subject | files |
| --- | --- | --- | --- |
| 1 | `d53562245d75c6212a671f09779260295330d4b3` | Hold a request against the row that asked, all the way to the body | `src/web/browser/catena/catena-model.js`<br>`src/web/browser/catena/catena.js`<br>`tools/tests/test_catena_wave_1.py` |
| 2 | `fc643930b9509967f9d3b065137588f47d755289` | Record the V15 lane: pending work belongs to the row that asked | `PROJECT-WORK.md`<br>`guidance/corpus-browser-master-plan.md`<br>`guidance/corpus-browser-roadmap.md`<br>`promised-deliverables.toml` |
| 3 | `df246f77e1ade1d3af511eb9aec04e4f4d60ecce` | Disclose what the ownership split costs, and measure it | `PROJECT-WORK.md`<br>`guidance/corpus-browser-roadmap.md` |
| 4 | `b9202882badbbbc364f1dd3d9057d2710ee47552` | Correct which review in this sequence was the unpublished one | `PROJECT-WORK.md`<br>`guidance/corpus-browser-master-plan.md`<br>`guidance/corpus-browser-roadmap.md` |

## Diff — 7 file(s), 1620 insertion(s), 45 deletion(s)

| state | path | + | − |
| --- | --- | --- | --- |
| M | `PROJECT-WORK.md` | 205 | 0 |
| M | `guidance/corpus-browser-master-plan.md` | 1 | 1 |
| M | `guidance/corpus-browser-roadmap.md` | 96 | 1 |
| M | `promised-deliverables.toml` | 132 | 0 |
| M | `src/web/browser/catena/catena-model.js` | 88 | 0 |
| M | `src/web/browser/catena/catena.js` | 45 | 33 |
| M | `tools/tests/test_catena_wave_1.py` | 1053 | 10 |

## Payload — gzip -9, mtime 0

| file | parent whole | head whole | ceiling | parent stripped | head stripped | ceiling | parent comment share | head comment share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | 7629 | 7629 | 8000 | 2676 | 2676 | 2700 | 0.649 | 0.649 |
| `src/web/browser/catena/catena.js` | 12972 | 12958 | 13000 | 7546 | 7724 | 8800 | 0.418 | 0.404 |
| `src/web/browser/catena/catena-model.js` | 39724 | 41077 | none | 9396 | 9536 | none | 0.763 | 0.768 |

The page and the model together, because neither measure alone is the load a reader pays:

| | parent | head | delta |
| --- | --- | --- | --- |
| compressed as one stream | 51914 | 53267 | +1353 |
| compressed separately and summed | 52696 | 54035 | +1339 |

## Test delta

| | |
| --- | --- |
| `CORRECTED ORACLE` blocks | 23 |
| corrected blocks by marking lane | `?` 1, `V6` 8, `V7` 14 |
| classes holding a corrected oracle | 14 |
| test classes added | 3 |

Each block's marker tag names the lane that corrected it; nothing here assumes they all belong to one round.

Classes holding a corrected oracle: `ActionPartialArrivalTerminalStateTest`, `FindingOrderIndependenceTest`, `FrozenContractTest`, `GenuinelyLateStaleWorkTest`, `MalformedLanguageAttributeTest`, `MalformedRecordRenderingTest`, `MixedCollectionMemberTest`, `NumericVerseAndPathTest`, `RenderedScriptureTruthTest`, `RoutableIdentityTest`, `TypedAbsenceFindingTest`, `UnsupportedVoiceTest`, `UntypedProvenanceTest`, `V7UnreadableRootDomainClaimTest`.

### The V15 test file at the parent

The head's test file — the V15 file — replayed against the PARENT's production files: same scenarios, same oracles, other code. The decomposition, reported separately:

| | |
| --- | --- |
| methods run | 559 |
| control methods passing at the parent | 545 |
| methods failing at the parent | 14 |
| failing subtest identities | 17 |
| classes with a failure | 5 (2 added by V15, 3 pre-existing with a corrected oracle) |

Failing subtest identities at the parent:

- `ERROR: test_a_row_no_projection_made_owns_no_transport_and_writes_nothing (test_catena_wave_1.V15TransportOwnershipTest.test_a_row_no_projection_made_owns_no_transport_and_writes_nothing)`
- `ERROR: test_body_application_is_a_consumer_of_the_authoritative_projection (test_catena_wave_1.V15TransportOwnershipTest.test_body_application_is_a_consumer_of_the_authoritative_projection) (scenario='v14-authority-graph')`
- `ERROR: test_body_application_is_a_consumer_of_the_authoritative_projection (test_catena_wave_1.V15TransportOwnershipTest.test_body_application_is_a_consumer_of_the_authoritative_projection) (scenario='v15-same-path-together')`
- `ERROR: test_body_application_is_a_consumer_of_the_authoritative_projection (test_catena_wave_1.V15TransportOwnershipTest.test_body_application_is_a_consumer_of_the_authoritative_projection) (scenario='v15-settled-then-shared')`
- `FAIL: test_a_downstream_rerender_after_the_mutations_is_unchanged (test_catena_wave_1.V15DownstreamMutationTest.test_a_downstream_rerender_after_the_mutations_is_unchanged)`
- `FAIL: test_a_genuinely_late_completion_belongs_to_the_row_that_asked (test_catena_wave_1.V14RequestOwnershipTest.test_a_genuinely_late_completion_belongs_to_the_row_that_asked)`
- `FAIL: test_a_late_release_cannot_change_anything_of_b (test_catena_wave_1.V15TransportOwnershipTest.test_a_late_release_cannot_change_anything_of_b)`
- `FAIL: test_a_late_release_cannot_change_anything_of_b (test_catena_wave_1.V15TransportOwnershipTest.test_a_late_release_cannot_change_anything_of_b) (field='fragmentTexts')`
- `FAIL: test_a_settled_value_is_shared_and_applied_as_the_row_that_asked (test_catena_wave_1.V15TransportOwnershipTest.test_a_settled_value_is_shared_and_applied_as_the_row_that_asked)`
- `FAIL: test_an_unreadable_spine_is_one_substitute_however_often_it_is_asked (test_catena_wave_1.V15TransportOwnershipTest.test_an_unreadable_spine_is_one_substitute_however_often_it_is_asked)`
- `FAIL: test_b_settles_independently_while_a_is_still_held (test_catena_wave_1.V15TransportOwnershipTest.test_b_settles_independently_while_a_is_still_held)`
- `FAIL: test_one_owners_failure_is_not_another_owners (test_catena_wave_1.V15TransportOwnershipTest.test_one_owners_failure_is_not_another_owners)`
- `FAIL: test_the_distinguishable_bodies_are_not_doing_the_work (test_catena_wave_1.V15TransportOwnershipTest.test_the_distinguishable_bodies_are_not_doing_the_work)`
- `FAIL: test_the_model_is_byte_identical (test_catena_wave_1.FrozenContractTest.test_the_model_is_byte_identical)`
- `FAIL: test_the_roster_names_every_consumer_the_model_has (test_catena_wave_1.V14ConsumerIdentityTest.test_the_roster_names_every_consumer_the_model_has)`
- `FAIL: test_the_transport_owner_carries_the_row_and_its_projection (test_catena_wave_1.V15TransportOwnershipTest.test_the_transport_owner_carries_the_row_and_its_projection)`
- `FAIL: test_two_rows_in_one_turn_are_two_transports (test_catena_wave_1.V15TransportOwnershipTest.test_two_rows_in_one_turn_are_two_transports)`

Classes V15 adds that do **not** fail at the parent: `V15ObservationAccountingTest`. A class that passes at both ends closes a proof gap rather than a defect, and saying otherwise is the claim the V6 roadmap made against its own evidence.

## Suites

| suite | tests | failures | errors | skips | outcome | FAIL/ERROR identities |
| --- | --- | --- | --- | --- | --- | --- |
| browser_static_head | 5 | 0 | 0 | 0 | OK | 0 |
| focused_catena_head | 615 | 0 | 0 | 0 | OK | 0 |
| focused_catena_parent | 596 | 0 | 0 | 0 | OK | 0 |
| full_discovery_head | 1966 | 14 | 13 | 11 | FAILED | 27 |
| full_discovery_parent | 1947 | 14 | 13 | 11 | FAILED | 27 |
| head_tests_against_parent | 559 | 14 | 4 | 0 | FAILED | 17 |
| sealer | 157 | 0 | 0 | 0 | OK | 0 |

Full-discovery FAIL/ERROR identity sets at parent and head are **identical** — 27 entries, 0 only at the head, 0 only at the parent, 0 mentioning catena.

## Browser gate

| | parent | head |
| --- | --- | --- |
| browser | Chrome/151.0.7922.173 | Chrome/151.0.7922.173 |
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
| evidence members (frozen) | 63 |
| evidence bytes (sum of the rows) | 18441372 |
| derived members (named, unsized) | 6 |
| PNGs | 0 |
| before/after raster pairs | 0 |
| unpaired captures | 0 |

Derived members:

- `claims.json` — written by this derivation; it cannot inventory its own bytes
- `DERIVED-CLAIMS.md` — rendered from claims.json in the same pass that writes it
- `logs/attempts.json` — the attempt ledger rows this package was built from, composed after the consistency audit so it can carry this attempt's own terminal row
- `logs/attempt-06/derive-claims.log` — transcript of this derivation, written as the derivation prints
- `logs/attempt-06/head-consistency.log` — transcript of the consistency audit, which runs after this derivation
- `MANIFEST.sha256` — written by the manifest phase, after every other member is frozen

## Byte and control scan

71 file(s) scanned for NUL, carriage returns, forbidden control characters and invalid UTF-8: **clean**.
