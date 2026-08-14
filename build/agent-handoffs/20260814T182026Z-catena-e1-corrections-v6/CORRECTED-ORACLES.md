# Every oracle this correction changed, and why

The V5 independent review's sharpest finding was about the proofs rather than
the code: several V5 oracles could not fail on the defect they were written for,
and several actively expected the defect. §22 of the correction brief requires
every one to be documented. This is that list: **nine corrected-oracle notes
over ten test methods**, one note covering two. Nothing here was deleted to make
a suite green; each was corrected in place, carrying its reason, so a reader of
the file learns what the oracle used to bless.

All line references are to `tools/tests/test_catena_wave_1.py`.

## A. Oracles that could not fail on their own defect

### A1. The word tally, counted from a deduplicated set

`NumericVerseAndPathTest.test_a_word_tally_is_a_number_the_record_wrote`

Read `page["classes"]`, which the replay harness builds as
`[...new Set(nodes.map(one => one.className))].sort()`. One chip and seven
chips both reduce to `["fragment-length"]`, so the assertion had exactly two
reachable outcomes and neither of them was "too many tallies printed".
**Demonstrated**: reverting the gate to `Number(x) > 0` renders
`['1,200 words', '1,200 words', '1,200 words', '1 words', '12.5 words']` and
the V5 oracle still passed.

Now reads `page["lengths"]`, a new projection of every `.fragment-length`
chip's text in rendered order, uncounted by any set, pinned as
`["1,200 words"]`.

### A2. The verse-coercion sweep, over the wrong document

`NumericVerseAndPathTest.test_no_verse_value_is_coerced_into_scripture`

Swept `page["fragmentTexts"]` — the commentary fragments — while its fixture
`MALFORMED_VERSES` corrupts the **bible chapter**. The harness projected no
rendered Scripture at all, so no test in the file could see a value coerced
into a verse. Now sweeps `page["verseTexts"]`, and
`RenderedScriptureTruthTest` carries the sweep across every chapter fixture.

### A3. "Stated once", asserted by substring

`MixedCollectionMemberTest.test_one_valid_refusal_among_malformed_members_is_stated_once`

Asserted `assertIsNotNone` plus one `assertIn`. A page rendering the refusal
four times satisfies both. Now pins `refusalCount == 1` and the whole sentence.

### A4. "Nothing stale", with nothing late

`RouteCompletionAfterMalformedDataTest.test_nothing_stale_survives_the_rejected_payload`
and its neighbours released the deferred payload **before** navigating, and
every harness step is followed by a full settle. No late completion ever
existed, so the class could not fail on a stale write.

The scenarios `genuinely-late-action`, `genuinely-late-action-failure`,
`genuinely-late-malformed` and `late-after-invalidation` hold action A, let
action B settle completely, and only then release A.
`GenuinelyLateStaleWorkTest.test_the_late_work_is_really_late` reads the step
order out of `SCENARIOS` and asserts it, and
`LateWorkReallyHappenedTest` asserts the new `released` counter — the number of
parked requests the harness actually let go — because a late completion that
changes nothing is otherwise indistinguishable from one that never happened.

## B. Oracles that expected the defect

### B1. Guessed English, pinned as survival

`MalformedLanguageAttributeTest.test_the_sound_language_survives_its_malformed_neighbours`
required `["fragment-text=la"] + ["fragment-text=en"] * 8`. Eight of those nine
records intend **Latin** and state a language nobody can read; the page
answered each with `en`, telling a screen reader to read Latin commentary in an
English voice on the authority of `|| 'en'`. Now requires
`["fragment-text=la"]` alone: the claim is omitted.

### B2. Guessed English, required of a malformed Bible

`MalformedLanguageAttributeTest.test_a_malformed_bible_language_reaches_no_passage_attribute`
asserted `assertIn("passage=en", ...)` for an edition whose language is
`{"code": "en"}` — that is, it required the page to read the malformed value
and act on what it guessed the value meant. Now asserts no `passage=` attribute
at all, and that the edition option reads `Douay-Rheims` without a
parenthetical.

### B3. Blank rows, counted

`MixedCollectionMemberTest.test_the_tally_counts_only_the_valid_members` pinned
`3 fragments held · 3 works held, not renderable yet · 3 lead entries`, and
`test_valid_lead_and_blocked_siblings_survive_their_neighbours` pinned
`["Lead One …", "", "Lead Two …"]` — the blank row asserted as correct output.
`MalformedRecordRenderingTest` did the same at
`["", "", "Origen — Homiliae in Genesim (240)"]` and
`["", "", "Anonymous — Catena in Genesim…"]`.

V5's comment defended the count explicitly: *"THREE, not two: a malformed
RECORD is still a record the spine wrote, so it counts and renders nothing of
itself."* The review rejected the argument. A count is a claim about what
stands here, and a record naming neither a work nor a man supports no part of
it. Now `3 fragments held · 2 works held, not renderable yet · 2 lead entries`,
with the announcement pinned to the same clauses in the same order.

The fragment count stays **three**, and the asymmetry is deliberate: that
fragment states its author, work, date and extent and only its id is
unreadable. See `REVIEW_REQUEST.md` §3.

### B4. A refusal manufactured from a note nobody could read

`UntypedProvenanceTest.test_an_untyped_refusal_note_is_not_coerced_into_the_sentence`
required `"Boundary not established."` to stand over
`{"note": {"broken": True}}` and merely forbade the coercion artefact inside
it. But the sentence **is** the claim: it tells a reader that Scripture's own
verse division moves in this edition and that this page will not guess where
to. Now asserts no refusal renders, no `refusal` state, and a terminated page.

### B5. The model byte-pin

`FrozenContractTest.test_the_model_is_byte_identical` pins
`src/web/browser/catena/catena-model.js` by digest. Updated to the V6 digest,
with the arithmetic that justified moving work into the unbudgeted model
restated for V6 rather than left describing V5.

## C. Projections added, because an oracle cannot read a sink that is not projected

Each of these existed in the page and in no assertion:

| Projection | The sink it reads | The claim it makes assertable |
| --- | --- | --- |
| `verseNumbers`, `verseTexts` | `.verse-num`, `.verse` | verse 1 renders once; no value is coerced into Scripture |
| `lengths` | `.fragment-length` | exactly one tally is printed |
| `bibleLabels`, `bibleValues` | `#bible-select` option text and value | no `([object Object])`, no guessed `(en)`, and only nameable editions are route values |
| `referenceBookText` | `#reference-book` | no testament claim from an unreadable value |
| `absenceAuthors`, `absenceWorks` | `.absence-author`, `.absence-work` | which work each absence row is about, said rather than inferred from counts |
| `refusalCount` | count of `.refusal` | "once" is counted |
| `failureText` | `#reading > p.error` | the failure a reader SEES, not only the one it is told |
| `released` | the harness's parked-request ledger | late work really happened |

## D. Scenarios added because an assertion was vacuous rather than passing

A delegated lane reported two of its own assertions unfalsifiable, which is
recorded here because the report is the reason they exist:

- `unsafe-identities` opened only the SAFE fragment, so "no unsafe path was
  requested" held because nothing asked. `unsafe-identities-opened` opens all
  six refused ids; the only fragment text requested is the safe sibling's.
- `bible-identity-forms` never selected an edition, so an unnameable edition id
  had no occasion to become a request. `unsafe-bible-route` cites one in the
  address; it fails closed and nothing is fetched through it.

Both were confirmed to fail against the uncorrected parent.

## E. What was NOT changed

No oracle was deleted. No oracle was weakened to accommodate the correction.
The neutral refusal umbrella copy, the exact voice-key set, the budget
ceilings, the protected-selector list and the print/forced-colors assertions
are untouched, and `NeutralRefusalUmbrellaTest` pins the umbrella's three
strings verbatim so that remains checkable.
