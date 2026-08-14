# The new regressions, run against the parent implementation

A regression that passes on the code it was written to catch is not a
regression. Every V5 test was therefore replayed against the **parent**,
`f93757854b54c19e50bdcb97ca0fed9b48d22bb7`, by copying only
`tools/tests/test_catena_wave_1.py` into a clean clone of it and running the
file. The clone was restored to a clean parent afterwards; `git status` there
is empty.

## First result: the parent cannot run the suite at all

With every V5 scenario present, the node harness **dies**:

```
TypeError: Cannot read properties of null (reading 'token')
    at start (…:1006:25)
```

`catena.js:1006` at the parent is
`list(index.canon).map((book) => ({ value: book.token, label: book.name })))`
— the bootstrap line this correction identified as throwing between the last
fetch and the first render, outside both funnels. One malformed canon member
takes the whole process down, and with it every one of the 254 tests.

That is the blocker-4 bootstrap finding, demonstrated as starkly as it can be.

## Second result: with the two bootstrap scenarios removed, 23 fail

To get a per-class reading, the `malformed-canon` and `scalar-index` scenarios
were filtered out of `SCENARIOS` for the parent run only — the filter is five
lines and is quoted in the log — so the harness survives and the remaining V5
scenarios can report. The parent then runs 254 tests with **31 failures and 3
errors**, of which the following are the V5 regressions:

### MalformedLanguageAttributeTest — 5 failing at the parent

- `test_a_malformed_bible_language_reaches_no_passage_attribute`
- `test_a_malformed_language_reaches_no_visible_prose`
- `test_every_language_attribute_is_a_language_subtag`
- `test_no_language_attribute_is_ever_a_coerced_value`
- `test_the_sound_language_survives_its_malformed_neighbours`

### MixedCollectionMemberTest — 5 failing at the parent

- `test_a_malformed_id_addresses_no_text_file_and_erases_no_sibling`
- `test_one_valid_refusal_among_malformed_members_is_stated_once`
- `test_the_tally_counts_only_the_valid_members`
- `test_valid_fragment_siblings_survive_a_scalar_and_a_null`
- `test_valid_lead_and_blocked_siblings_survive_their_neighbours`

### NumericVerseAndPathTest — 5 failing at the parent

- `test_a_malformed_canon_never_leaves_the_page_loading`
- `test_a_malformed_held_path_is_never_requested`
- `test_a_mark_that_is_not_a_mark_opens_no_paragraph`
- `test_an_unreadable_present_list_proves_no_absence`
- `test_only_plainly_numbered_verses_with_readable_words_are_shown`

### RouteCompletionAfterMalformedDataTest — 5 failing at the parent

- `test_a_malformed_action_payload_settles_its_own_fragment_only`
- `test_a_partial_arrival_completes_when_the_malformed_spine_lands`
- `test_a_partial_arrival_keeps_its_valid_siblings_and_claims_nothing`
- `test_the_move_announces_itself_exactly_once_more`
- `test_the_valid_siblings_and_the_tally_survive_the_move`

### TypedAbsenceFindingTest — 3 failing at the parent

- `test_a_malformed_finding_supports_no_claim_and_no_count`
- `test_each_finding_speaks_only_for_itself`
- `test_not_surveyed_never_becomes_a_publishing_negative`

Twenty-three, across all five of the review's blocking classes, plus the two
scenarios that crash the harness outright.

## What passes at the parent, and why that is right

Not every new test fails there, and none was written expecting to. Several
pin behaviour the V4.1 review recorded as already sound — the render catch
clearing `aria-busy`, the page announcing once, the terminal funnel completing
after a caught throw. Those tests exist to hold that behaviour while the
boundary moved underneath it, and passing at both ends is exactly what they
are for.

The log is `logs/new-tests-against-base.log`.
