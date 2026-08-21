# Derived claims

**Every number in this file was computed by `logs/derive-claims.py` at seal time and written from the same pass that wrote `claims.json`.** Nothing here was typed. Where a document in this package states a figure, this is the source it states it from, and `logs/head-consistency.py` refuses a package whose prose names a commit these claims do not entitle it to name.

## Identity

| | |
| --- | --- |
| parent | `6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3` |
| head | `69f2575421ba976271c936b1abd4b39dbe8b98fd` |
| review addressed | `—` |
| parent is an ancestor of head | True |
| working tree clean at head | True |

## Commits — 2

| # | sha | subject | files |
| --- | --- | --- | --- |
| 1 | `5273bd00c368c461834f4259c495043510aa178b` | Take the chapter once, and let the row that asked own what it asked for | `src/web/browser/catena/catena-model.js`<br>`src/web/browser/catena/catena.js`<br>`tools/tests/test_catena_wave_1.py` |
| 2 | `69f2575421ba976271c936b1abd4b39dbe8b98fd` | Record the V14 lane: the row that asked owns what it asked for | `PROJECT-WORK.md`<br>`guidance/corpus-browser-master-plan.md`<br>`guidance/corpus-browser-roadmap.md`<br>`promised-deliverables.toml` |

## Diff — 7 file(s), 2343 insertion(s), 65 deletion(s)

| state | path | + | − |
| --- | --- | --- | --- |
| M | `PROJECT-WORK.md` | 267 | 0 |
| M | `guidance/corpus-browser-master-plan.md` | 1 | 1 |
| M | `guidance/corpus-browser-roadmap.md` | 102 | 1 |
| M | `promised-deliverables.toml` | 163 | 19 |
| M | `src/web/browser/catena/catena-model.js` | 232 | 30 |
| M | `src/web/browser/catena/catena.js` | 8 | 8 |
| M | `tools/tests/test_catena_wave_1.py` | 1570 | 6 |

## Payload — gzip -9, mtime 0

| file | parent whole | head whole | ceiling | parent stripped | head stripped | ceiling | parent comment share | head comment share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | 7629 | 7629 | 8000 | 2676 | 2676 | 2700 | 0.649 | 0.649 |
| `src/web/browser/catena/catena.js` | 12974 | 12972 | 13000 | 7546 | 7546 | 8800 | 0.418 | 0.418 |
| `src/web/browser/catena/catena-model.js` | 36679 | 39724 | none | 8873 | 9396 | none | 0.758 | 0.763 |

The page and the model together, because neither measure alone is the load a reader pays:

| | parent | head | delta |
| --- | --- | --- | --- |
| compressed as one stream | 48877 | 51914 | +3037 |
| compressed separately and summed | 49653 | 52696 | +3043 |

## Test delta

| | |
| --- | --- |
| `CORRECTED ORACLE` blocks | 23 |
| corrected blocks by marking lane | `?` 1, `V6` 8, `V7` 14 |
| classes holding a corrected oracle | 14 |
| test classes added | 7 |

Each block's marker tag names the lane that corrected it; nothing here assumes they all belong to one round.

Classes holding a corrected oracle: `ActionPartialArrivalTerminalStateTest`, `FindingOrderIndependenceTest`, `FrozenContractTest`, `GenuinelyLateStaleWorkTest`, `MalformedLanguageAttributeTest`, `MalformedRecordRenderingTest`, `MixedCollectionMemberTest`, `NumericVerseAndPathTest`, `RenderedScriptureTruthTest`, `RoutableIdentityTest`, `TypedAbsenceFindingTest`, `UnsupportedVoiceTest`, `UntypedProvenanceTest`, `V7UnreadableRootDomainClaimTest`.

### The V14 test file at the parent

The head's test file — the V14 file — replayed against the PARENT's production files: same scenarios, same oracles, other code. The decomposition, reported separately:

| | |
| --- | --- |
| methods run | 540 |
| control methods passing at the parent | 511 |
| methods failing at the parent | 29 |
| failing subtest identities | 43 |
| classes with a failure | 7 (6 added by V14, 1 pre-existing with a corrected oracle) |

Failing subtest identities at the parent:

- `FAIL: test_a_detonating_accessor_never_reaches_the_render_tail (test_catena_wave_1.V14NestedSourceAuthorityTest.test_a_detonating_accessor_never_reaches_the_render_tail)`
- `FAIL: test_a_genuinely_late_completion_belongs_to_the_row_that_asked (test_catena_wave_1.V14RequestOwnershipTest.test_a_genuinely_late_completion_belongs_to_the_row_that_asked)`
- `FAIL: test_a_nested_field_accessor_is_declined_by_every_consumer_alike (test_catena_wave_1.V14NestedSourceAuthorityTest.test_a_nested_field_accessor_is_declined_by_every_consumer_alike)`
- `FAIL: test_a_phantom_count_cannot_manufacture_an_unavailable_chapter (test_catena_wave_1.V14MemberAuthorityTest.test_a_phantom_count_cannot_manufacture_an_unavailable_chapter)`
- `FAIL: test_a_row_belongs_to_the_projection_that_made_it (test_catena_wave_1.V14ProjectionImmutabilityTest.test_a_row_belongs_to_the_projection_that_made_it)`
- `FAIL: test_a_row_no_projection_made_addresses_nothing (test_catena_wave_1.V14RequestOwnershipTest.test_a_row_no_projection_made_addresses_nothing)`
- `FAIL: test_a_second_chapter_is_a_second_identity_and_no_more (test_catena_wave_1.V14ConsumerIdentityTest.test_a_second_chapter_is_a_second_identity_and_no_more)`
- `FAIL: test_an_unreadable_chapter_is_two_chapters_and_says_so (test_catena_wave_1.V14ConsumerIdentityTest.test_an_unreadable_chapter_is_two_chapters_and_says_so)`
- `FAIL: test_every_consumer_received_the_object_the_normalization_made (test_catena_wave_1.V14ConsumerIdentityTest.test_every_consumer_received_the_object_the_normalization_made)`
- `FAIL: test_every_nested_accessor_produces_one_coherent_result (test_catena_wave_1.V14NestedSourceAuthorityTest.test_every_nested_accessor_produces_one_coherent_result) (scenario='v14-nested-accessor')`
- `FAIL: test_every_nested_accessor_produces_one_coherent_result (test_catena_wave_1.V14NestedSourceAuthorityTest.test_every_nested_accessor_produces_one_coherent_result) (scenario='v14-nested-accessor-late')`
- `FAIL: test_every_nested_accessor_produces_one_coherent_result (test_catena_wave_1.V14NestedSourceAuthorityTest.test_every_nested_accessor_produces_one_coherent_result) (scenario='v14-nested-accessor-steady')`
- `FAIL: test_every_nested_accessor_produces_one_coherent_result (test_catena_wave_1.V14NestedSourceAuthorityTest.test_every_nested_accessor_produces_one_coherent_result) (scenario='v14-nested-accessor-throws')`
- `FAIL: test_every_raw_chapter_member_is_asked_exactly_once (test_catena_wave_1.V14UnfetchedProjectionTest.test_every_raw_chapter_member_is_asked_exactly_once) (member='unfetched')`
- `FAIL: test_every_trusted_structure_is_frozen (test_catena_wave_1.V14ProjectionImmutabilityTest.test_every_trusted_structure_is_frozen) (structure='blocked')`
- `FAIL: test_every_trusted_structure_is_frozen (test_catena_wave_1.V14ProjectionImmutabilityTest.test_every_trusted_structure_is_frozen) (structure='lead')`
- `FAIL: test_no_consumer_invokes_a_nested_source_accessor (test_catena_wave_1.V14NestedSourceAuthorityTest.test_no_consumer_invokes_a_nested_source_accessor) (scenario='v14-nested-accessor')`
- `FAIL: test_no_consumer_invokes_a_nested_source_accessor (test_catena_wave_1.V14NestedSourceAuthorityTest.test_no_consumer_invokes_a_nested_source_accessor) (scenario='v14-nested-accessor-late')`
- `FAIL: test_no_consumer_invokes_a_nested_source_accessor (test_catena_wave_1.V14NestedSourceAuthorityTest.test_no_consumer_invokes_a_nested_source_accessor) (scenario='v14-nested-accessor-steady')`
- `FAIL: test_no_consumer_invokes_a_nested_source_accessor (test_catena_wave_1.V14NestedSourceAuthorityTest.test_no_consumer_invokes_a_nested_source_accessor) (scenario='v14-nested-accessor-throws')`
- `FAIL: test_no_mutation_of_the_authority_survives (test_catena_wave_1.V14ProjectionImmutabilityTest.test_no_mutation_of_the_authority_survives) (value='blockedWhy')`
- `FAIL: test_no_mutation_of_the_authority_survives (test_catena_wave_1.V14ProjectionImmutabilityTest.test_no_mutation_of_the_authority_survives) (value='leadTitle')`
- `FAIL: test_one_address_across_two_projections_stays_with_its_own (test_catena_wave_1.V14RequestOwnershipTest.test_one_address_across_two_projections_stays_with_its_own)`
- `FAIL: test_the_exported_row_builder_seals_what_it_returns (test_catena_wave_1.V14ProjectionImmutabilityTest.test_the_exported_row_builder_seals_what_it_returns)`
- `FAIL: test_the_forged_second_answer_reaches_no_sink (test_catena_wave_1.V14UnfetchedProjectionTest.test_the_forged_second_answer_reaches_no_sink)`
- `FAIL: test_the_four_accessor_shapes_render_one_page (test_catena_wave_1.V14NestedSourceAuthorityTest.test_the_four_accessor_shapes_render_one_page) (scenario='v14-nested-accessor-late')`
- `FAIL: test_the_four_accessor_shapes_render_one_page (test_catena_wave_1.V14NestedSourceAuthorityTest.test_the_four_accessor_shapes_render_one_page) (scenario='v14-nested-accessor-steady')`
- `FAIL: test_the_four_accessor_shapes_render_one_page (test_catena_wave_1.V14NestedSourceAuthorityTest.test_the_four_accessor_shapes_render_one_page) (scenario='v14-nested-accessor-throws')`
- `FAIL: test_the_inventory_is_asked_once (test_catena_wave_1.V14MemberAuthorityTest.test_the_inventory_is_asked_once) (scenario='v14-members-add')`
- `FAIL: test_the_inventory_is_asked_once (test_catena_wave_1.V14MemberAuthorityTest.test_the_inventory_is_asked_once) (scenario='v14-members-phantom')`
- `FAIL: test_the_inventory_is_asked_once (test_catena_wave_1.V14MemberAuthorityTest.test_the_inventory_is_asked_once) (scenario='v14-members-remove')`
- `FAIL: test_the_inventory_is_asked_once (test_catena_wave_1.V14MemberAuthorityTest.test_the_inventory_is_asked_once) (scenario='v14-members-reorder')`
- `FAIL: test_the_inventory_is_asked_once (test_catena_wave_1.V14MemberAuthorityTest.test_the_inventory_is_asked_once) (scenario='v14-members-tally')`
- `FAIL: test_the_journal_names_the_owner_by_object_and_not_by_path (test_catena_wave_1.V14RequestOwnershipTest.test_the_journal_names_the_owner_by_object_and_not_by_path)`
- `FAIL: test_the_lead_and_blocked_builders_seal_what_they_return (test_catena_wave_1.V14ProjectionImmutabilityTest.test_the_lead_and_blocked_builders_seal_what_they_return)`
- `FAIL: test_the_model_is_byte_identical (test_catena_wave_1.FrozenContractTest.test_the_model_is_byte_identical)`
- `FAIL: test_the_page_reads_no_raw_chapter_member_after_projection (test_catena_wave_1.V14UnfetchedProjectionTest.test_the_page_reads_no_raw_chapter_member_after_projection)`
- `FAIL: test_the_roster_names_every_consumer_the_model_has (test_catena_wave_1.V14ConsumerIdentityTest.test_the_roster_names_every_consumer_the_model_has)`
- `FAIL: test_the_tally_is_a_consumer_of_its_own (test_catena_wave_1.V14ConsumerIdentityTest.test_the_tally_is_a_consumer_of_its_own)`
- `FAIL: test_the_walked_members_never_move_the_page (test_catena_wave_1.V14UnfetchedProjectionTest.test_the_walked_members_never_move_the_page) (member='unfetched')`
- `FAIL: test_the_walked_page_is_the_page_that_was_never_walked (test_catena_wave_1.V14UnfetchedProjectionTest.test_the_walked_page_is_the_page_that_was_never_walked)`
- `FAIL: test_the_walked_record_is_asked_once (test_catena_wave_1.V14UnfetchedProjectionTest.test_the_walked_record_is_asked_once)`
- `FAIL: test_two_rows_carrying_one_address_are_two_owners (test_catena_wave_1.V14RequestOwnershipTest.test_two_rows_carrying_one_address_are_two_owners)`

Classes V14 adds that do **not** fail at the parent: `V14ProjectionAuthorityBase`. A class that passes at both ends closes a proof gap rather than a defect, and saying otherwise is the claim the V6 roadmap made against its own evidence.

## Suites

| suite | tests | failures | errors | skips | outcome | FAIL/ERROR identities |
| --- | --- | --- | --- | --- | --- | --- |
| browser_static_head | 5 | 0 | 0 | 0 | OK | 0 |
| focused_catena_head | 596 | 0 | 0 | 0 | OK | 0 |
| focused_catena_parent | 555 | 0 | 0 | 0 | OK | 0 |
| full_discovery_head | 1947 | 14 | 13 | 11 | FAILED | 27 |
| full_discovery_parent | 1906 | 14 | 14 | 11 | FAILED | 28 |
| head_tests_against_parent | 540 | 43 | 0 | 0 | FAILED | 43 |
| sealer | 157 | 0 | 0 | 0 | OK | 0 |

Full-discovery FAIL/ERROR identity sets at parent and head are **NOT identical** — 27 entries, 0 only at the head, 1 only at the parent, 0 mentioning catena.

## Browser gate

| | parent | head |
| --- | --- | --- |
| browser | Chrome/151.0.7922.169 | Chrome/151.0.7922.169 |
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
| evidence bytes (sum of the rows) | 17769579 |
| derived members (named, unsized) | 6 |
| PNGs | 0 |
| before/after raster pairs | 0 |
| unpaired captures | 0 |

Derived members:

- `claims.json` — written by this derivation; it cannot inventory its own bytes
- `DERIVED-CLAIMS.md` — rendered from claims.json in the same pass that writes it
- `logs/attempts.json` — the attempt ledger rows this package was built from, composed after the consistency audit so it can carry this attempt's own terminal row
- `logs/attempt-13/derive-claims.log` — transcript of this derivation, written as the derivation prints
- `logs/attempt-13/head-consistency.log` — transcript of the consistency audit, which runs after this derivation
- `MANIFEST.sha256` — written by the manifest phase, after every other member is frozen

## Byte and control scan

71 file(s) scanned for NUL, carriage returns, forbidden control characters and invalid UTF-8: **clean**.
