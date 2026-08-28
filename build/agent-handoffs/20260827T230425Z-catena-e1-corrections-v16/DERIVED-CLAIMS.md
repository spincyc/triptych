# Derived claims

**Every number in this file was computed by `logs/derive-claims.py` at seal time and written from the same pass that wrote `claims.json`.** Nothing here was typed. Where a document in this package states a figure, this is the source it states it from, and `logs/head-consistency.py` refuses a package whose prose names a commit these claims do not entitle it to name.

## Identity

| | |
| --- | --- |
| parent | `b9202882badbbbc364f1dd3d9057d2710ee47552` |
| head | `cc1f2fb8625f044558c26edd358b99cd7dcc7646` |
| review addressed | `67247ecc39a6e5f6224c64ca3ab1af163ee023b1` |
| parent is an ancestor of head | True |
| working tree clean at head | True |
| workspace mode | `fresh-clone` |
| linked worktree | False |
| git dir kind | `directory` |

## Commits — 4

| # | sha | subject | files |
| --- | --- | --- | --- |
| 1 | `e34ab2b0564c69b05b0ac9e5e85e55cbc3565805` | Publish only a finished value, and carry its owner to the body | `src/web/browser/catena/catena-model.js`<br>`src/web/browser/catena/catena.js` |
| 2 | `208f086b55ce1ef53a66e3a15b865d3eae3e53b7` | Prove the interval closed, the owner carried, and the record earned | `tools/tests/test_catena_wave_1.py` |
| 3 | `251900b14a168b356297299d68b947c686c91768` | Record the V16 lane, and correct what this lane first corrected wrongly | `PROJECT-WORK.md`<br>`guidance/corpus-browser-master-plan.md`<br>`guidance/corpus-browser-roadmap.md`<br>`promised-deliverables.toml` |
| 4 | `cc1f2fb8625f044558c26edd358b99cd7dcc7646` | Do not state here what stating here would change | `PROJECT-WORK.md`<br>`guidance/corpus-browser-roadmap.md` |

## Diff — 7 file(s), 3979 insertion(s), 194 deletion(s)

| state | path | + | − |
| --- | --- | --- | --- |
| M | `PROJECT-WORK.md` | 831 | 5 |
| M | `guidance/corpus-browser-master-plan.md` | 1 | 1 |
| M | `guidance/corpus-browser-roadmap.md` | 331 | 2 |
| M | `promised-deliverables.toml` | 155 | 0 |
| M | `src/web/browser/catena/catena-model.js` | 241 | 23 |
| M | `src/web/browser/catena/catena.js` | 51 | 52 |
| M | `tools/tests/test_catena_wave_1.py` | 2369 | 111 |

## Payload — gzip -9, mtime 0

| file | parent whole | head whole | ceiling | parent stripped | head stripped | ceiling | parent comment share | head comment share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | 7629 | 7629 | 8000 | 2676 | 2676 | 2700 | 0.649 | 0.649 |
| `src/web/browser/catena/catena.js` | 12958 | 12965 | 13000 | 7724 | 7835 | 8800 | 0.404 | 0.396 |
| `src/web/browser/catena/catena-model.js` | 41077 | 44247 | none | 9536 | 10344 | none | 0.768 | 0.766 |

The page and the model together, because neither measure alone is the load a reader pays:

| | parent | head | delta |
| --- | --- | --- | --- |
| compressed as one stream | 53267 | 56462 | +3195 |
| compressed separately and summed | 54035 | 57212 | +3177 |

## Test delta

| | |
| --- | --- |
| `CORRECTED ORACLE` blocks | 23 |
| corrected blocks by marking lane | `?` 1, `V6` 8, `V7` 14 |
| classes holding a corrected oracle | 14 |
| test classes added | 8 |

Each block's marker tag names the lane that corrected it; nothing here assumes they all belong to one round.

Classes holding a corrected oracle: `ActionPartialArrivalTerminalStateTest`, `FindingOrderIndependenceTest`, `FrozenContractTest`, `GenuinelyLateStaleWorkTest`, `MalformedLanguageAttributeTest`, `MalformedRecordRenderingTest`, `MixedCollectionMemberTest`, `NumericVerseAndPathTest`, `RenderedScriptureTruthTest`, `RoutableIdentityTest`, `TypedAbsenceFindingTest`, `UnsupportedVoiceTest`, `UntypedProvenanceTest`, `V7UnreadableRootDomainClaimTest`.

### The V16 test file at the parent

The head's test file — the V16 file — replayed against the PARENT's production files: same scenarios, same oracles, other code. The decomposition, reported separately:

| | |
| --- | --- |
| methods run | 604 |
| control methods passing at the parent | 565 |
| methods failing at the parent | 39 |
| failing subtest identities | 288 |
| classes with a failure | 8 (6 added by V16, 2 pre-existing with a corrected oracle) |

Failing subtest identities at the parent:

- `FAIL: test_a_finished_value_rebinds_to_the_owner_that_reuses_it (test_catena_wave_1.V16CompletionEnvelopeTest.test_a_finished_value_rebinds_to_the_owner_that_reuses_it)`
- `FAIL: test_a_getter_one_level_above_the_record_is_never_invoked (test_catena_wave_1.V16FinalizedContentTest.test_a_getter_one_level_above_the_record_is_never_invoked)`
- `FAIL: test_a_late_publication_and_completion_cannot_reach_the_second (test_catena_wave_1.V16ReentrantPublicationTest.test_a_late_publication_and_completion_cannot_reach_the_second)`
- `FAIL: test_a_nested_record_altered_after_publication_is_out_of_reach (test_catena_wave_1.V16FinalizedContentTest.test_a_nested_record_altered_after_publication_is_out_of_reach)`
- `FAIL: test_a_polluted_boolean_survives_the_mint_and_is_still_refused (test_catena_wave_1.V16FinalizedContentTest.test_a_polluted_boolean_survives_the_mint_and_is_still_refused)`
- `FAIL: test_a_polluted_realm_supplies_no_member_of_a_finalized_value (test_catena_wave_1.V16FinalizedContentTest.test_a_polluted_realm_supplies_no_member_of_a_finalized_value)`
- `FAIL: test_a_prototype_planted_after_publication_reaches_no_later_owner (test_catena_wave_1.V16FinalizedContentTest.test_a_prototype_planted_after_publication_reaches_no_later_owner)`
- `FAIL: test_a_reentrant_owner_after_publication_gets_the_finished_value (test_catena_wave_1.V16ReentrantPublicationTest.test_a_reentrant_owner_after_publication_gets_the_finished_value)`
- `FAIL: test_a_reentrant_owner_after_publication_gets_the_finished_value (test_catena_wave_1.V16ReentrantPublicationTest.test_a_reentrant_owner_after_publication_gets_the_finished_value) (moment='get')`
- `FAIL: test_a_reentrant_owner_during_normalization_asks_for_itself (test_catena_wave_1.V16ReentrantPublicationTest.test_a_reentrant_owner_during_normalization_asks_for_itself)`
- `FAIL: test_a_reentrant_owner_during_normalization_asks_for_itself (test_catena_wave_1.V16ReentrantPublicationTest.test_a_reentrant_owner_during_normalization_asks_for_itself) (moment='get')`
- `FAIL: test_a_reported_failure_is_a_body_and_is_owned_as_one (test_catena_wave_1.V16CompletionEnvelopeTest.test_a_reported_failure_is_a_body_and_is_owned_as_one)`
- `FAIL: test_a_throwing_write_is_caught_and_leaves_no_applied_record (test_catena_wave_1.V16BodyApplicationJournalTest.test_a_throwing_write_is_caught_and_leaves_no_applied_record)`
- `FAIL: test_a_write_that_does_not_take_leaves_no_applied_record (test_catena_wave_1.V16BodyApplicationJournalTest.test_a_write_that_does_not_take_leaves_no_applied_record)`
- `FAIL: test_an_accessor_over_the_same_members_changes_none_of_it (test_catena_wave_1.V16TextObservationAccountingTest.test_an_accessor_over_the_same_members_changes_none_of_it)`
- `FAIL: test_an_actual_row_no_longer_authorizes_arbitrary_content (test_catena_wave_1.V16CompletionEnvelopeTest.test_an_actual_row_no_longer_authorizes_arbitrary_content)`
- `FAIL: test_an_own_accessor_never_becomes_the_pages_words (test_catena_wave_1.V16FinalizedContentTest.test_an_own_accessor_never_becomes_the_pages_words)`
- `FAIL: test_an_owner_local_retry_never_observes_a_partial_path_state (test_catena_wave_1.V16BodyApplicationJournalTest.test_an_owner_local_retry_never_observes_a_partial_path_state)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='acknowledgement-order', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='acknowledgement-order', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='default', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='fragment-retry', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='fragment-retry', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='malformed-action-then-retry', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='malformed-record', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='severian-open', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='severian-projected', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='synthetic-licence', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='synthetic-licence', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='unsafe-identities', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='unsafe-identities-opened', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='unsafe-identities-opened', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='unsafe-identities-opened', application=2)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='unsafe-identities-opened', application=3)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='unsafe-identities-opened', application=4)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='unsafe-identities-opened', application=5)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='unsafe-identities-opened', application=6)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v11-renderer-order-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v12-alternating-carried-path', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v12-drifting-carried-path', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v12-prewarmed-inherited-prefix', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v12-stable-carried-path-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-prewarmed-walking-path', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-prewarmed-walking-path', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-prewarmed-walking-path-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-prewarmed-walking-path-control', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-walking-carried-path', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-walking-carried-path-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-walking-chapter-members', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-walking-chapter-members-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-walking-refusals', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-walking-refusals-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-walking-sources', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-walking-sources-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-walking-spine-prefix', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v13-walking-spine-prefix-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-blocked', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-blocked-first', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-blocked-later', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-fragments', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-fragments-first', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-fragments-later', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-fragments-later', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-graph', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-graph', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-leads', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-leads-first', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-leads-later', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-refusals', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-refusals-first', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-refusals-later', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-sources', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-sources-first', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-sources-later', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-text_prefix-later', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-unfetched', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-authority-unfetched-first', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-late-same-path', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-add', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-add-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-add-control', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-remove', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-remove', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-remove-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-reorder', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-reorder', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-reorder-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-reorder-control', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-tally', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-tally', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-tally', application=2)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-tally-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-tally-control', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-members-tally-control', application=2)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-nested-data', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-nested-fields', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-nested-fields-throw', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-nested-forged-data', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-quiet-unfetched', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-same-path-rows', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-same-path-rows', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-two-projections-one-path', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-two-projections-one-path', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v14-walking-unfetched', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-authority-rerender', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-authority-rerender', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-authority-rerender', application=2)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-authority-rerender', application=3)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-descriptor-accounting', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-late-same-path', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-late-same-path-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-nested-edition', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-nested-edition-data', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-nested-edition-steady', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-nested-edition-throw', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-same-path-one-fails', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-same-path-one-fails', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-same-path-together', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-same-path-together', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-settled-then-shared', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v15-settled-then-shared', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-inherited-accessor', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-inherited-accessor', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-inherited-text', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-inherited-text', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-inherited-text-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-inherited-text-control', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-late-contamination', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-late-contamination', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-one-fails-probed', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-one-fails-probed', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-polluted-schema', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-polluted-schema', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-polluted-schema-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-polluted-schema-control', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-publication', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-reentrant-normalizing', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-reentrant-normalizing', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-reentrant-published', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-reentrant-published', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-retry-probed', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-retry-probed', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-text-accessor', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-text-accounting', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=10)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=11)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=12)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=13)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=2)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=3)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=4)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=5)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=6)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=7)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=8)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-whole-roster', application=9)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-write-fails', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-write-fails', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-write-fails-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-write-fails-control', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-write-modes-control', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-write-modes-control', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-write-silent', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-write-silent', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-write-throws', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v16-write-throws', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-hollow-fragments', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-hollow-fragments', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-hollow-fragments-reversed', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-hollow-fragments-reversed', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-inherited-id', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-inherited-id', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-null-fragment-text', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=10)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=11)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=2)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=3)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=4)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=5)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=6)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=7)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=8)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path', application=9)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path-no-prefix', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path-no-prefix', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path-no-prefix', application=2)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path-no-prefix', application=3)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path-no-prefix', application=4)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path-no-prefix', application=5)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path-no-prefix', application=6)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path-no-prefix', application=7)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path-no-prefix', application=8)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v7-text-path-no-prefix', application=9)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v8-wrong-namespace-carried', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v8-wrong-namespace-carried', application=1)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v8-wrong-namespace-carried', application=2)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v8-wrong-namespace-carried', application=3)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v8-wrong-namespace-carried', application=4)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v8-wrong-namespace-carried', application=5)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v8-wrong-namespace-carried', application=6)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v8-wrong-namespace-carried', application=7)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v8-wrong-namespace-carried', application=8)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v8-wrong-namespace-carried', application=9)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v9-absent-prefix-carried', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v9-prewarmed-fallback', application=0)`
- `FAIL: test_every_body_this_page_applied_is_a_finished_scalar_record (test_catena_wave_1.V16FinalizedContentTest.test_every_body_this_page_applied_is_a_finished_scalar_record) (scenario='v9-valid-prefix-carried', application=0)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-late-contamination', application=0)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-late-contamination', application=1)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-publication', application=0)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=0)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=1)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=10)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=11)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=12)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=13)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=2)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=3)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=4)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=5)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=6)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=7)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=8)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-whole-roster', application=9)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-write-fails-control', application=0)`
- `FAIL: test_every_journal_entry_binds_the_whole_chain_it_stands_for (test_catena_wave_1.V16BodyApplicationJournalTest.test_every_journal_entry_binds_the_whole_chain_it_stands_for) (scenario='v16-write-fails-control', application=1)`
- `FAIL: test_exactly_one_finished_value_is_ever_published (test_catena_wave_1.V16PublicationAtomicityTest.test_exactly_one_finished_value_is_ever_published)`
- `FAIL: test_no_failure_and_no_intermediate_value_is_published (test_catena_wave_1.V16PublicationAtomicityTest.test_no_failure_and_no_intermediate_value_is_published)`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-one-fails-probed', event=5, moment='set')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-one-fails-probed', event=6, moment='after-publication')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-one-fails-probed', event=7, moment='during-normalize')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-one-fails-probed', event=8, moment='before-publication')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-publication', event=4, moment='set')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-publication', event=5, moment='after-publication')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-publication', event=6, moment='during-normalize')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-publication', event=7, moment='before-publication')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-normalizing', event=10, moment='before-publication')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-normalizing', event=4, moment='set')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-normalizing', event=5, moment='after-publication')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-normalizing', event=6, moment='during-normalize')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-normalizing', event=7, moment='get')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-normalizing', event=8, moment='before-publication')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-normalizing', event=9, moment='during-normalize')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-published', event=10, moment='before-publication')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-published', event=4, moment='set')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-published', event=5, moment='after-publication')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-published', event=6, moment='get')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-published', event=7, moment='during-normalize')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-published', event=8, moment='before-publication')`
- `FAIL: test_no_lookup_of_the_path_ever_returns_anything_unfinished (test_catena_wave_1.V16PublicationAtomicityTest.test_no_lookup_of_the_path_ever_returns_anything_unfinished) (scenario='v16-reentrant-published', event=9, moment='during-normalize')`
- `FAIL: test_no_scenario_anywhere_lets_a_body_write_escape_the_page (test_catena_wave_1.V16BodyApplicationJournalTest.test_no_scenario_anywhere_lets_a_body_write_escape_the_page)`
- `FAIL: test_pollution_after_the_value_was_sealed_moves_nothing (test_catena_wave_1.V16FinalizedContentTest.test_pollution_after_the_value_was_sealed_moves_nothing)`
- `FAIL: test_the_envelope_can_be_minted_from_neither_half_alone (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_envelope_can_be_minted_from_neither_half_alone)`
- `FAIL: test_the_finalized_content_cannot_be_changed (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_finalized_content_cannot_be_changed) (attempt='addThrew')`
- `FAIL: test_the_finalized_content_cannot_be_changed (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_finalized_content_cannot_be_changed) (attempt='assignThrew')`
- `FAIL: test_the_finalized_content_cannot_be_changed (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_finalized_content_cannot_be_changed) (attempt='deleteThrew')`
- `FAIL: test_the_finalized_content_cannot_be_changed (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_finalized_content_cannot_be_changed) (attempt='protoThrew')`
- `FAIL: test_the_finalized_content_cannot_be_changed (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_finalized_content_cannot_be_changed) (value='held')`
- `FAIL: test_the_finalized_content_cannot_be_changed (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_finalized_content_cannot_be_changed) (value='keptBasis')`
- `FAIL: test_the_finalized_content_cannot_be_changed (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_finalized_content_cannot_be_changed) (value='noExtra')`
- `FAIL: test_the_finalized_content_cannot_be_changed (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_finalized_content_cannot_be_changed) (value='stillNullPrototype')`
- `FAIL: test_the_finalized_content_is_the_models_own_deterministic_schema (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_finalized_content_is_the_models_own_deterministic_schema)`
- `FAIL: test_the_journal_entry_follows_a_confirmed_write_and_nothing_else (test_catena_wave_1.V16CompletionEnvelopeTest.test_the_journal_entry_follows_a_confirmed_write_and_nothing_else)`
- `FAIL: test_the_model_is_byte_identical (test_catena_wave_1.FrozenContractTest.test_the_model_is_byte_identical)`
- `FAIL: test_the_only_value_read_of_the_file_is_the_transport_resolving_it (test_catena_wave_1.V16TextObservationAccountingTest.test_the_only_value_read_of_the_file_is_the_transport_resolving_it)`
- `FAIL: test_the_owner_state_stays_coherent_after_a_failed_write (test_catena_wave_1.V16BodyApplicationJournalTest.test_the_owner_state_stays_coherent_after_a_failed_write)`
- `FAIL: test_the_page_in_a_polluted_realm_is_the_page_in_a_clean_one (test_catena_wave_1.V16FinalizedContentTest.test_the_page_in_a_polluted_realm_is_the_page_in_a_clean_one)`
- `FAIL: test_the_page_reads_no_raw_chapter_member_after_projection (test_catena_wave_1.V14UnfetchedProjectionTest.test_the_page_reads_no_raw_chapter_member_after_projection)`
- `FAIL: test_the_page_states_no_body_sentence_the_model_states (test_catena_wave_1.V14UnfetchedProjectionTest.test_the_page_states_no_body_sentence_the_model_states) (sentence='The text of this fragment arrived in a f')`
- `FAIL: test_the_page_states_no_body_sentence_the_model_states (test_catena_wave_1.V14UnfetchedProjectionTest.test_the_page_states_no_body_sentence_the_model_states) (sentence='The text of this fragment could not be l')`
- `FAIL: test_the_page_states_no_body_sentence_the_model_states (test_catena_wave_1.V14UnfetchedProjectionTest.test_the_page_states_no_body_sentence_the_model_states) (sentence='The text of this fragment was not publis')`
- `FAIL: test_the_page_states_no_body_sentence_the_model_states (test_catena_wave_1.V14UnfetchedProjectionTest.test_the_page_states_no_body_sentence_the_model_states) (sentence='This fragment carries no text file')`
- `FAIL: test_the_path_is_empty_until_the_finished_value_exists (test_catena_wave_1.V16PublicationAtomicityTest.test_the_path_is_empty_until_the_finished_value_exists)`
- `FAIL: test_the_path_is_empty_until_the_finished_value_exists (test_catena_wave_1.V16PublicationAtomicityTest.test_the_path_is_empty_until_the_finished_value_exists) (moment='before-publication')`
- `FAIL: test_the_path_is_empty_until_the_finished_value_exists (test_catena_wave_1.V16PublicationAtomicityTest.test_the_path_is_empty_until_the_finished_value_exists) (moment='during-normalize')`
- `FAIL: test_the_projection_takes_four_own_descriptors_and_nothing_else (test_catena_wave_1.V16TextObservationAccountingTest.test_the_projection_takes_four_own_descriptors_and_nothing_else)`
- `FAIL: test_the_projection_takes_four_own_descriptors_and_nothing_else (test_catena_wave_1.V16TextObservationAccountingTest.test_the_projection_takes_four_own_descriptors_and_nothing_else) (member='acknowledgement')`
- `FAIL: test_the_projection_takes_four_own_descriptors_and_nothing_else (test_catena_wave_1.V16TextObservationAccountingTest.test_the_projection_takes_four_own_descriptors_and_nothing_else) (member='basis')`
- `FAIL: test_the_projection_takes_four_own_descriptors_and_nothing_else (test_catena_wave_1.V16TextObservationAccountingTest.test_the_projection_takes_four_own_descriptors_and_nothing_else) (member='date_basis')`
- `FAIL: test_the_projection_takes_four_own_descriptors_and_nothing_else (test_catena_wave_1.V16TextObservationAccountingTest.test_the_projection_takes_four_own_descriptors_and_nothing_else) (member='text')`
- `FAIL: test_the_sentence_and_the_envelope_refuse_inherited_authority_too (test_catena_wave_1.V16FinalizedContentTest.test_the_sentence_and_the_envelope_refuse_inherited_authority_too)`
- `FAIL: test_the_two_write_failures_leave_different_partial_states (test_catena_wave_1.V16BodyApplicationJournalTest.test_the_two_write_failures_leave_different_partial_states) (mode='silent')`
- `FAIL: test_the_two_write_failures_leave_different_partial_states (test_catena_wave_1.V16BodyApplicationJournalTest.test_the_two_write_failures_leave_different_partial_states) (mode='throw')`
- `FAIL: test_the_value_published_by_path_is_the_value_the_body_applied (test_catena_wave_1.V16PublicationAtomicityTest.test_the_value_published_by_path_is_the_value_the_body_applied)`
- `FAIL: test_words_supplied_from_above_the_record_are_not_its_words (test_catena_wave_1.V16FinalizedContentTest.test_words_supplied_from_above_the_record_are_not_its_words)`

Classes V16 adds that do **not** fail at the parent: `V16ConsumerIdentityRosterTest`, `V16PublicationBase`. A class that passes at both ends closes a proof gap rather than a defect, and saying otherwise is the claim the V6 roadmap made against its own evidence.

## Suites

| suite | tests | failures | errors | skips | outcome | FAIL/ERROR identities |
| --- | --- | --- | --- | --- | --- | --- |
| browser_static_head | 5 | 0 | 0 | 0 | OK | 0 |
| focused_catena_head | 660 | 0 | 0 | 0 | OK | 0 |
| focused_catena_parent | 615 | 0 | 0 | 0 | OK | 0 |
| full_discovery_head | 2011 | 14 | 13 | 11 | FAILED | 27 |
| full_discovery_parent | 1966 | 14 | 13 | 11 | FAILED | 27 |
| head_tests_against_parent | 604 | 288 | 0 | 0 | FAILED | 288 |
| sealer | 169 | 0 | 0 | 0 | OK | 0 |

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
| evidence members (frozen) | 70 |
| evidence bytes (sum of the rows) | 21895630 |
| derived members (named, unsized) | 6 |
| PNGs | 0 |
| before/after raster pairs | 0 |
| unpaired captures | 0 |

Derived members:

- `claims.json` — written by this derivation; it cannot inventory its own bytes
- `DERIVED-CLAIMS.md` — rendered from claims.json in the same pass that writes it
- `logs/attempts.json` — the attempt ledger rows this package was built from, composed after the consistency audit so it can carry this attempt's own terminal row
- `logs/attempt-32/derive-claims.log` — transcript of this derivation, written as the derivation prints
- `logs/attempt-32/head-consistency.log` — transcript of the consistency audit, which runs after this derivation
- `MANIFEST.sha256` — written by the manifest phase, after every other member is frozen

## Byte and control scan

78 file(s) scanned for NUL, carriage returns, forbidden control characters and invalid UTF-8: **clean**.
