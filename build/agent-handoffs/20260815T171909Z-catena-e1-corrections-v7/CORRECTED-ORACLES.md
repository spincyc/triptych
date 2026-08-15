# Corrected oracles — every test expectation V7 changed, and why

An oracle that expects a defect is worse than no oracle: it is a standing
argument that the defect is correct, and the next lane has to overturn a
committed decision rather than notice a gap. So none of these was deleted.
Each is corrected in place, in a block beginning `CORRECTED ORACLE (V7)`, with
the reason recorded beside the assertion it replaced.

**The counts are in `DERIVED-CLAIMS.md`, under "Test delta", and are derived
by `logs/derive-claims.py` from the sealed head rather than typed here.** Two
of the annotated sites are class constants that several tests read, and the
rest are individual test methods or a helper the tests call; every one of them
pinned behaviour the V6 independent review named as a defect, which is the
reason they had to move and the reason the V6 suite was green while the
defects stood.

The grep that finds them all:

    grep -n 'CORRECTED ORACLE (V7)' tools/tests/test_catena_wave_1.py

The sections below are the argument, one site at a time. They are numbered for
reference and the numbering is not a count of anything.

---

## 1. `FindingOrderIndependenceTest.REASONS`

**Pinned:** four absence reasons, the third being `typed.work4`'s — the work
whose record carries **two valid findings that say different things**.

**Why it was wrong:** V6 blanked the finding for a contradictory set, and then
selected one of the two contradicting records' `reason` by ranking the pair on
length and rendered it. So the page declined to say which rights claim the
record made, and printed one of them anyway, chosen by a rule nothing in the
contract supports. The review's words: *"Finding resolution still speaks after
it says it has declined."*

**Now:** three reasons. A reason is licensed by the finding it belongs to;
where no one finding can be read, no reason stands for the row. The row itself
survives with its author and its work — declining a finding is not deleting
the record.

## 2. `FindingOrderIndependenceTest.test_valid_facts_survive_beside_the_records_the_page_refuses`

**Pinned:** *"work4's finding is declined, and work4's reason — the third
entry, a fact the record states in its own words — still renders."*

**Why it was wrong:** it is the sentence above, stated as a principle. A
reason belonging to one side of a contradiction is not a fact standing apart
from the choice the page refused to make; it **is** that choice, in prose.

**Now:** the assertion is that neither side speaks, made by count — exactly
one of each sentence is on the page, and both belong to works that state them
legitimately.

## 3. `FindingOrderIndependenceTest.test_a_malformed_record_never_stands_in_for_the_valid_finding_beside_it`

**Kept, and strengthened.** Its original claim — that a malformed neighbour's
prose never reaches the page — was correct and is unchanged. V7 adds the
count assertion for the contradictory work, so the same test now also fails if
either side of `work4` speaks.

## 4. `TypedAbsenceFindingTest.test_a_valid_finding_survives_malformed_sibling_metadata`

**Pinned:** three reasons, the middle being `typed.work2`'s — a sound sentence
standing beside a finding that is a **record**, so no finding could be read
for that row at all.

**Why it was wrong:** the review's *"Zero recognized findings can likewise leak
arbitrary rights prose."* The fixture's own name for that value —
`"A reason that outlives its finding."` — was asserting the defect as the
contract.

**Now:** two reasons. The half of this test that was always right is
untouched: `typed.work3` states `in-copyright` beside a `reason` that is not
text, the finding is counted and the reason withheld, and V7 does not disturb
it. A **readable** finding still speaks with a malformed reason beside it;
what changed is that an **unreadable** one no longer speaks with a readable
reason beside it.

## 5. `MalformedRecordRenderingTest.test_a_malformed_payload_body_renders_nothing_of_itself`

**Pinned:** `fragmentTexts == [""]` — an empty paragraph where a father's
prose belongs.

**Why it was wrong:** the review's *"Malformed lazy text is still normalized
to an empty string, so a route may finish without truthfully reporting the
unreadable payload."* The page opened a fragment, fetched its text, could not
read it, and said nothing — and an empty paragraph is also what a fragment
whose text is genuinely blank would look like.

**Now:** `["The text of this fragment arrived in a form this page cannot
read."]`. Nothing of the payload is rendered, which was always the
requirement; what is added is the page saying so.

## 6. `RoutableIdentityTest.test_an_edition_that_cannot_name_itself_is_not_a_route`

**Pinned:** `bible=../../escape is not a published edition.`

**Why it was wrong:** the manifest in that fixture carries four records that
cannot name themselves, one of them holding the very value cited. The page
could not read the set of published editions whole, so *"is not a published
edition"* is a claim about what this project publishes, made out of a manifest
it failed to read. The review: *"an unreadable Bible root can render an
edition as unpublished."*

**Now:** *"is not a value this page could match; the record it would be
matched against could not be read whole."* Everything else in the test is
unchanged and is the whole of the security claim: the reader's text is kept,
no request is composed through the refused id, the recovery link stands.

## 7. `ActionPartialArrivalTerminalStateTest.refusal_for`

**Pinned:** a refusal sentence per chapter, produced by interpolating whichever
chapter the page was rendering.

**Why it was wrong:** it read as though the refusal were per-chapter and it
was not. The one refusal record in `MIXED_COLLECTION_FIXTURE` states
`"chapter": 1`, and V6 printed it under Genesis 2 as readily as under Genesis
1. The review: a refusal established *"without the closed refusal kind or
matching locus required by the source contract."*

**Now:** the helper is unchanged; what changed is that only the Genesis 1
route may call it. The fixture is untouched and is now the evidence.

## 8. `ActionPartialArrivalTerminalStateTest.test_the_late_arrival_manufactures_no_absence_and_no_false_refusal`

**Pinned:** `refusalCount == 1` and the chapter-2 sentence, on a Genesis 2
route.

**Why it was wrong:** it is the false refusal the test's own name forbids.

**Now:** `refusalCount == 0`, `refusal is None`. The test means its name.

## 9. `ActionPartialArrivalTerminalStateTest.test_every_route_into_the_malformed_chapter_renders_the_same_content`

**Pinned:** `refusalCount` compared across all four routes as though shared,
beside a per-chapter refusal sentence — the two assertions contradicted each
other and both passed, because the count really was the same and the sentence
really was one record printed twice.

**Now:** `refusalCount` leaves the shared set and is asserted per route with
the sentence; the Genesis 1 route shows a refusal and the three Genesis 2
routes show none. `dataStates` likewise, since the refusal is the one member
that may differ.

## 10. `UnsupportedVoiceTest.test_the_supported_set_is_read_from_the_index_not_from_the_key`

**Pinned:** the literal source text `!list(index.voices).includes(voice)` in
`src/web/browser/catena/catena.js`.

**Why it was wrong:** a source-text assertion cannot see that the line it
names is wrong. `list(index.voices)` answers `[]` for a voices value nobody
can read, so every address was then told this corpus holds no such voice — a
negative about the corpus drawn from a parse failure. The requirement the
assertion existed for is unchanged; the line moved to
`src/web/browser/catena/catena-model.js` with the rest of the address
judgment, and got a `whole` flag.

**Now:** the assertion follows the line to the file that carries it, in its
corrected form.

## 11. `GenuinelyLateStaleWorkTest.GUARDED`

**Pinned:** thirteen keys, and the review found the omission: the **final
status sink**. `statusWrites` is the journal of everything ever spoken, which
a late completion cannot shorten and could only lengthen; what a reader or a
screen reader meets is `statusText`, the live region's current contents. A
stale write that REPLACED the standing announcement with an older one would
have left the journal identical and the region wrong.

**Now:** thirty-six keys — every projection the page writes on a settled
route, enumerated rather than sampled, so a sink added later is guarded by
having to be added here too. The guard also asserts `released` increased, so a
completion that changed nothing is told apart from one that never happened.

## 12. `FrozenContractTest.test_the_name_joiner_is_only_ever_handed_a_fresh_list`

**Pinned:** that exactly two lines of `src/web/browser/catena/catena.js` call
`joinNames`, and that both hand it `.map(...)`.

**Why it was wrong:** the precondition expired at V5. V3 had rewritten
`joinNames` to `pop()` to buy bytes, which consumed the caller's array, and
the ceiling left no room for a comment saying so — hence a source-text pin.
V5 moved the function to the unbudgeted model and restored the non-mutating
form. The assertion went on passing for two whole corrections because it read
the SHAPE of two call sites rather than the property they existed to protect.

**Now:** it runs the real function and asks the real question — does it leave
its argument alone? The file's own doctrine is that a source-text assertion is
the fallback for what a replay cannot reach, and this was reachable all along.

## 13. A new guard, where nothing guarded anything

`V7SharedFieldDriftTest` relates `SHARED_WITH_EDITION` in
`scripts/_catena.py` to the list of the same name in
`src/web/browser/catena/catena-model.js`. Nothing did. A field added to the
generator's tuple would have been written once under `sources` and silently
dropped from every fragment — a real fact of the corpus, gone, with no test to
notice. The guard also asserts the other direction, which is the one V7 got
wrong first: no per-fragment field may be inheritable.

## 14. `NumericVerseAndPathTest` and `RenderedScriptureTruthTest` — `test_a_mark_that_is_not_a_mark_opens_no_paragraph`

**Pinned:** that `MALFORMED_BREAKS` renders one unmarked paragraph — which is
V5's correction and is right — **and** that the note beneath it reads "No
paragraph division is held for this chapter in this edition, so it runs on."

**Why the second half was wrong:** the review's *"a malformed paragraph root
can render `No paragraph division held`"*, for this exact record.
`MALFORMED_BREAKS` STATES a division at verses 1, 3 and 9, in three ways this
page cannot read. Denying that the edition divides the chapter is a claim
about how it sets its text, drawn from a record nobody could read. The two
assertions sat in one test and only one of them was ever examined.

**Now:** the paragraphs and the projected marks are unchanged; the note says
the record could not be read. One readable mark among unreadable ones still
speaks — the sibling rule holds here as everywhere, and
`v7-breaks-one-readable` pins it.

## 15. `V7UnreadableRootDomainClaimTest.test_a_readable_paragraph_layer_still_says_it_holds_none`

**Pinned:** the same `malformed-verses` scenario as the CONTROL for "a
readable layer still says it holds none".

**Why it was wrong:** it is this lane's own test, written two rounds earlier,
and it used as its control an example of the very thing it exists to
distinguish from. That fixture's `breaks` states three marks and none is
readable.

**Now:** `v7-empty-breaks` is the control — a paragraph record this page reads
perfectly, which records no break. That is the one shape entitled to say the
edition holds no division here, and the test now asserts the exact sentence.

---

## Two harness corrections, which are not oracles

**`_zip_it` in `logs/test-sanitize-and-seal.py`** built the sealer's test
archive with its members at the root — the layout
`guidance/external-review-handoffs.md` forbids, and the opposite of what the
real shipped archives have. Nothing noticed, because the two tests using it
only ever compared the archive's own bytes to a digest computed from those
same bytes. It now builds the archive the protocol requires, and the
mis-rooted shape is pinned as the finding it is.

**`StaleManifest.test_failing_check_only_removes_the_previous_manifest`**
pinned `--check-only` deleting `MANIFEST.sha256`, in a mode documented as
"scan and report; never rewrite a member", and which `PRIVACY-AUDIT.md`
instructs a **reviewer** to run against a sealed package. See
`PRIVACY-AUDIT.md` for the correction and the reason the V5 defect it was
meant to answer belongs to the writing path instead.
