# Derived claims

**Every number in this file was computed by `logs/derive-claims.py` at seal time and written from the same pass that wrote `claims.json`.** Nothing here was typed. Where a document in this package states a figure, this is the source it states it from, and `logs/head-consistency.py` refuses a package whose prose names a commit these claims do not entitle it to name.

## Identity

| | |
| --- | --- |
| parent | `d312786dd2b23926aa88e29ea15647dfcc7e7e6e` |
| head | `6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3` |
| review addressed | `728c3e3b3d0d6e899f0da33e06a08a116375896f` |
| parent is an ancestor of head | True |
| working tree clean at head | True |

## Commits — 2

| # | sha | subject | files |
| --- | --- | --- | --- |
| 1 | `42959f4c9ff31e64cebe55b911bd8da75343575a` | Normalize the chapter once, and let nothing read it again | `src/web/browser/catena/catena-model.js`<br>`src/web/browser/catena/catena.js`<br>`tools/tests/test_catena_wave_1.py` |
| 2 | `6cc85e1a1dea317a48c0bfcfd6f774201ea3a6c3` | Record the V13 lane: the chapter was read once, and everything read that | `PROJECT-WORK.md`<br>`guidance/corpus-browser-master-plan.md`<br>`guidance/corpus-browser-roadmap.md`<br>`promised-deliverables.toml` |

## Diff — 7 file(s), 1473 insertion(s), 103 deletion(s)

| state | path | + | − |
| --- | --- | --- | --- |
| M | `PROJECT-WORK.md` | 219 | 0 |
| M | `guidance/corpus-browser-master-plan.md` | 1 | 1 |
| M | `guidance/corpus-browser-roadmap.md` | 112 | 1 |
| M | `promised-deliverables.toml` | 103 | 7 |
| M | `src/web/browser/catena/catena-model.js` | 258 | 73 |
| M | `src/web/browser/catena/catena.js` | 2 | 2 |
| M | `tools/tests/test_catena_wave_1.py` | 778 | 19 |

## Payload — gzip -9, mtime 0

| file | parent whole | head whole | ceiling | parent stripped | head stripped | ceiling | parent comment share | head comment share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `src/web/browser/catena/catena.css` | 7629 | 7629 | 8000 | 2676 | 2676 | 2700 | 0.649 | 0.649 |
| `src/web/browser/catena/catena.js` | 12980 | 12974 | 13000 | 7554 | 7546 | 8800 | 0.418 | 0.418 |
| `src/web/browser/catena/catena-model.js` | 34367 | 36679 | none | 8258 | 8873 | none | 0.76 | 0.758 |

The page and the model together, because neither measure alone is the load a reader pays:

| | parent | head | delta |
| --- | --- | --- | --- |
| compressed as one stream | 46581 | 48877 | +2296 |
| compressed separately and summed | 47347 | 49653 | +2306 |

## Test delta

| | |
| --- | --- |
| `CORRECTED ORACLE` blocks | 23 |
| corrected blocks by marking lane | `?` 1, `V6` 8, `V7` 14 |
| classes holding a corrected oracle | 14 |
| test classes added | 1 |

Each block's marker tag names the lane that corrected it; nothing here assumes they all belong to one round.

Classes holding a corrected oracle: `ActionPartialArrivalTerminalStateTest`, `FindingOrderIndependenceTest`, `FrozenContractTest`, `GenuinelyLateStaleWorkTest`, `MalformedLanguageAttributeTest`, `MalformedRecordRenderingTest`, `MixedCollectionMemberTest`, `NumericVerseAndPathTest`, `RenderedScriptureTruthTest`, `RoutableIdentityTest`, `TypedAbsenceFindingTest`, `UnsupportedVoiceTest`, `UntypedProvenanceTest`, `V7UnreadableRootDomainClaimTest`.

### The V13 test file at the parent

The head's test file — the V13 file — replayed against the PARENT's production files: same scenarios, same oracles, other code. The decomposition, reported separately:

| | |
| --- | --- |
| methods run | 499 |
| control methods passing at the parent | 486 |
| methods failing at the parent | 13 |
| failing subtest identities | 27 |
| classes with a failure | 3 (1 added by V13, 2 pre-existing with a corrected oracle) |

Failing subtest identities at the parent:

- `FAIL: test_a_drifting_carried_descriptor_never_reaches_its_second_value (test_catena_wave_1.V12PlantedRequestSinkTest.test_a_drifting_carried_descriptor_never_reaches_its_second_value)`
- `FAIL: test_a_second_chapter_is_a_second_projection_and_no_more (test_catena_wave_1.V13OneChapterProjectionTest.test_a_second_chapter_is_a_second_projection_and_no_more)`
- `FAIL: test_a_walking_carried_path_reaches_only_its_first_answer (test_catena_wave_1.V13OneChapterProjectionTest.test_a_walking_carried_path_reaches_only_its_first_answer)`
- `FAIL: test_a_walking_refusal_never_becomes_rule_four (test_catena_wave_1.V13OneChapterProjectionTest.test_a_walking_refusal_never_becomes_rule_four)`
- `FAIL: test_a_walking_spine_prefix_composes_only_its_first_answer (test_catena_wave_1.V13OneChapterProjectionTest.test_a_walking_spine_prefix_composes_only_its_first_answer)`
- `FAIL: test_a_warm_cache_answers_the_projection_that_was_validated (test_catena_wave_1.V13OneChapterProjectionTest.test_a_warm_cache_answers_the_projection_that_was_validated)`
- `FAIL: test_all_six_walks_are_non_vacuous (test_catena_wave_1.V13OneChapterProjectionTest.test_all_six_walks_are_non_vacuous) (scenario='v13-prewarmed-walking-path')`
- `FAIL: test_all_six_walks_are_non_vacuous (test_catena_wave_1.V13OneChapterProjectionTest.test_all_six_walks_are_non_vacuous) (scenario='v13-walking-carried-path')`
- `FAIL: test_all_six_walks_are_non_vacuous (test_catena_wave_1.V13OneChapterProjectionTest.test_all_six_walks_are_non_vacuous) (scenario='v13-walking-chapter-members')`
- `FAIL: test_all_six_walks_are_non_vacuous (test_catena_wave_1.V13OneChapterProjectionTest.test_all_six_walks_are_non_vacuous) (scenario='v13-walking-refusals')`
- `FAIL: test_all_six_walks_are_non_vacuous (test_catena_wave_1.V13OneChapterProjectionTest.test_all_six_walks_are_non_vacuous) (scenario='v13-walking-sources')`
- `FAIL: test_all_six_walks_are_non_vacuous (test_catena_wave_1.V13OneChapterProjectionTest.test_all_six_walks_are_non_vacuous) (scenario='v13-walking-spine-prefix')`
- `FAIL: test_every_walk_was_really_a_walk (test_catena_wave_1.V13OneChapterProjectionTest.test_every_walk_was_really_a_walk) (scenario='v13-prewarmed-walking-path')`
- `FAIL: test_every_walk_was_really_a_walk (test_catena_wave_1.V13OneChapterProjectionTest.test_every_walk_was_really_a_walk) (scenario='v13-walking-carried-path')`
- `FAIL: test_every_walk_was_really_a_walk (test_catena_wave_1.V13OneChapterProjectionTest.test_every_walk_was_really_a_walk) (scenario='v13-walking-chapter-members')`
- `FAIL: test_every_walk_was_really_a_walk (test_catena_wave_1.V13OneChapterProjectionTest.test_every_walk_was_really_a_walk) (scenario='v13-walking-refusals')`
- `FAIL: test_every_walk_was_really_a_walk (test_catena_wave_1.V13OneChapterProjectionTest.test_every_walk_was_really_a_walk) (scenario='v13-walking-sources')`
- `FAIL: test_every_walk_was_really_a_walk (test_catena_wave_1.V13OneChapterProjectionTest.test_every_walk_was_really_a_walk) (scenario='v13-walking-spine-prefix')`
- `FAIL: test_one_page_load_makes_exactly_one_chapter_projection (test_catena_wave_1.V13OneChapterProjectionTest.test_one_page_load_makes_exactly_one_chapter_projection) (scenario='v13-walking-carried-path')`
- `FAIL: test_one_page_load_makes_exactly_one_chapter_projection (test_catena_wave_1.V13OneChapterProjectionTest.test_one_page_load_makes_exactly_one_chapter_projection) (scenario='v13-walking-chapter-members')`
- `FAIL: test_one_page_load_makes_exactly_one_chapter_projection (test_catena_wave_1.V13OneChapterProjectionTest.test_one_page_load_makes_exactly_one_chapter_projection) (scenario='v13-walking-refusals')`
- `FAIL: test_one_page_load_makes_exactly_one_chapter_projection (test_catena_wave_1.V13OneChapterProjectionTest.test_one_page_load_makes_exactly_one_chapter_projection) (scenario='v13-walking-sources')`
- `FAIL: test_one_page_load_makes_exactly_one_chapter_projection (test_catena_wave_1.V13OneChapterProjectionTest.test_one_page_load_makes_exactly_one_chapter_projection) (scenario='v13-walking-spine-prefix')`
- `FAIL: test_the_model_is_byte_identical (test_catena_wave_1.FrozenContractTest.test_the_model_is_byte_identical)`
- `FAIL: test_the_request_is_owned_by_the_projection_that_validated_it (test_catena_wave_1.V13OneChapterProjectionTest.test_the_request_is_owned_by_the_projection_that_validated_it)`
- `FAIL: test_walking_chapter_members_render_only_what_readability_approved (test_catena_wave_1.V13OneChapterProjectionTest.test_walking_chapter_members_render_only_what_readability_approved)`
- `FAIL: test_walking_editions_never_reach_the_provenance_line (test_catena_wave_1.V13OneChapterProjectionTest.test_walking_editions_never_reach_the_provenance_line)`

Classes V13 adds that do **not** fail at the parent: none. A class that passes at both ends closes a proof gap rather than a defect, and saying otherwise is the claim the V6 roadmap made against its own evidence.

## Suites

| suite | tests | failures | errors | skips | outcome | FAIL/ERROR identities |
| --- | --- | --- | --- | --- | --- | --- |
| browser_static_head | 5 | 0 | 0 | 0 | OK | 0 |
| focused_catena_head | 555 | 0 | 0 | 0 | OK | 0 |
| focused_catena_parent | 544 | 0 | 0 | 0 | OK | 0 |
| full_discovery_head | 1906 | 14 | 13 | 11 | FAILED | 27 |
| full_discovery_parent | 1895 | 14 | 13 | 11 | FAILED | 27 |
| head_tests_against_parent | 499 | 27 | 0 | 0 | FAILED | 27 |
| sealer | 157 | 0 | 0 | 0 | OK | 0 |

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
| evidence members (frozen) | 63 |
| evidence bytes (sum of the rows) | 15554009 |
| derived members (named, unsized) | 6 |
| PNGs | 0 |
| before/after raster pairs | 0 |
| unpaired captures | 0 |

Derived members:

- `claims.json` — written by this derivation; it cannot inventory its own bytes
- `DERIVED-CLAIMS.md` — rendered from claims.json in the same pass that writes it
- `logs/attempts.json` — the attempt ledger rows this package was built from, composed after the consistency audit so it can carry this attempt's own terminal row
- `logs/attempt-18/derive-claims.log` — transcript of this derivation, written as the derivation prints
- `logs/attempt-18/head-consistency.log` — transcript of the consistency audit, which runs after this derivation
- `MANIFEST.sha256` — written by the manifest phase, after every other member is frozen

## Byte and control scan

71 file(s) scanned for NUL, carriage returns, forbidden control characters and invalid UTF-8: **clean**.
