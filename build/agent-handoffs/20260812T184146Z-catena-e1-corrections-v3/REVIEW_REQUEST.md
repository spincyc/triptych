# REVIEW_REQUEST — what needs external judgment

Reviewed head `f2c9bc49dd29499734193b264ba9da21304b27f1`, base
`17f031b37840d8320c664a128d72b502108fe075` (the exact V2 head the 2026-08-12
review dispositioned), branch `impl/catena-wave-1-e1-corrections-v3`.

Only questions are below. What was implemented is in `HANDOFF.md` §7; what was
measured is in `checks.txt`; what this evidence cannot establish is in
`LIMITATIONS.md`.

## Blockers

Each item names the acceptance decision that cannot be made without an answer,
and the artifact or state to look at.

### 1. Failing closed is the unsupported-voice "state" — is that the state you meant?

The review's remaining-work column asked this lane to "distinguish the closed
supported-language set from grammatical form and render an unsupported-voice
state without inventing an absence", and finding 8 asked for "the
unsupported-voice state and exact contradiction assertion".

V3 routes an unsupported voice into the **existing** invalid-address state
rather than adding a distinct surface. The reasoning: `bible=nope` is the same
category of error — well formed, unsupported — and already fails closed there;
that state already leaves the address as written, names the exact value, offers
recovery without the offending key, and suppresses any "none here" label; and
the ceilings had no room for a new surface. The contradiction assertion is
`UnsupportedVoiceTest.test_no_unsupported_voice_ever_claims_a_holding`.

**Decision blocked:** whether a shared refusal surface satisfies "render an
unsupported-voice state", or whether E1 acceptance requires a visually distinct
unsupported-voice presentation. If the latter, it will need a ceiling waiver.

**Look at:** `changes.patch` (`hashProblems`), `HANDOFF.md` §7.1,
`tools/tests/test_catena_wave_1.py` class `UnsupportedVoiceTest`.

### 2. The supported set is a language axis; `translation:grc` is accepted

`index.held[].languages` is the only Catena-owned corpus-wide truth in memory
at validation time, and it records languages, not voices. So
`voice=translation:grc` is accepted and then truthfully reports that this
chapter holds no Greek translation — though the corpus holds no Greek
translation anywhere. A true voice-axis set exists only on the chapter spine,
which is fetched *after* validation; using it would add a request that the
pinned first-load assertion forbids.

**Decision blocked:** whether "a language this corpus holds commentary in" is
the right closed set, or whether acceptance requires a voice-axis set — which
would mean either publishing a voice list in the index (generator/data owner) or
deferring the refusal until after the spine loads (a larger route change).

**Look at:** `LIMITATIONS.md` §5, `HANDOFF.md` §7.1.

### 3. A bare-string `translators` now renders as one name

`[].concat(fragment.translators).filter(sound)` withholds objects, numbers,
booleans, `null`, blanks and array-like non-arrays, and removes the `TypeError`
that used to kill the render. It also treats `"translators": "A Name"` as a
one-item list rather than refusing it. The stricter `Array.isArray` form was
measured and does not fit inside the unraised ceilings.

**Decision blocked:** whether accepting a bare string is an acceptable reading
of the contract (a real recorded name under the correct label) or a widening
that must be refused even at the cost of a ceiling waiver.

**Look at:** `LIMITATIONS.md` §4, `changes.patch` (`renderFragment`),
`UntypedProvenanceTest`.

### 4. Stranger-key discard is stated but not tested

`STRANGER-KEYS.md` states the exact behaviour and labels precisely which cases
are proven and which are read from the code. V3 added no test for the discard
cases, because each would newly pin URL behaviour the review did not ask to
change.

**Decision blocked:** whether the corrected statement is sufficient, or whether
acceptance requires the four scenarios named in `STRANGER-KEYS.md` §3 to pin
the discard as contract. Pinning it makes partial-address canonicalisation a
promise; not pinning it leaves it free to change.

**Look at:** `STRANGER-KEYS.md`, `LIMITATIONS.md` §2.

### 5. The three release bindings remain deliberately stale

Unchanged from V2 and still not this lane's to repair. `src/web/browser/catena/catena.js` changed
again, so its actual digest differs again; the failure identity is the same
three paths and `stale: 3 stale binding(s)`.

**Decision blocked:** whether a correction candidate may be accepted with
`check-release-bindings` and its one derived `check-examples` divergence red —
i.e. whether fail-closed-unsigned is the correct posture for an unaccepted
candidate, or whether acceptance requires the release owner to re-sign first,
and in what order relative to review.

**Look at:** `logs/release-bindings-head.log`, `BASELINE-COMPARISON.md` §3,
`UNRESOLVED-BLOCKERS.md` row 4.

### 6. The real assistive-technology sequence is still not met

Unchanged, and not attemptable here. The V2 package's stated *reason* was false
and is corrected; the conclusion is not.

**Decision blocked:** whether E1 may be accepted with the real-AT requirement
recorded as an unmet pre-release evidence prerequisite — which is how the
2026-08-12 review characterised it — or whether it blocks acceptance itself.

**Look at:** `AT-LIMITATION.md`, `UNRESOLVED-BLOCKERS.md` row 6.

### 7. The code-only ceiling now stands one byte clear

12,995/13,000 whole and 8,799/8,800 comment-stripped, both unraised and both
paid for by deletion. The cost was the source prose: the new refusal branch
carries no comment, and `joinNames` now consumes its argument with the
precondition pinned by test rather than stated in the file.

**Decision blocked:** whether the ceilings should stand as recorded, with this
lane's prose cost accepted, or whether the reviewer wants a waiver proposed to
the owner so the source can carry its own explanation. This lane has no
authority to raise a ceiling and did not.

**Look at:** `LIMITATIONS.md` §3, `checks.txt` §D,
`FrozenContractTest.test_the_name_joiner_is_only_ever_handed_a_fresh_list`.

## Optional feedback

None of these blocks acceptance.

1. **Refusal wording.** An unsupported voice reports
   `voice=translation:zz is not a voice this corpus holds.` Is "this corpus"
   the right scope word for a reader, given the check is corpus-wide while the
   neighbouring "none here" is chapter-scoped?
2. **Three-state legibility.** A reader who mistypes `translation:EN` gets the
   grammar message, and `translation:de` gets the holdings message. Are the two
   distinguishable enough in a reader's terms, or should the grammar message
   also say the code must be lower case?
3. **Deleted dead lookup.** `M.chapterVoices(file).find(…) || M.parseVoiceKey(…)`
   is argued in `HANDOFF.md` §7.3 to be exactly `M.parseVoiceKey(…)`. That
   argument is load-bearing for the budget; it deserves an independent read.
   (Evidence: `changes.patch`, four sites.)
4. **Author typing placement.** The author name is typed once where groups are
   built, so the heading, the filter label and the exclusion set cannot
   disagree. Is that the right seam, or should `renderFragment` type its own
   chip independently?
5. **Refusal-note trimming.** `sound()` trims, so a refusal note with leading
   whitespace now renders trimmed where it previously kept the space and
   upper-cased it. Harmless, but it is a rendering change beyond the two named
   defects. (Evidence: `changes.patch`, `renderRefusal`.)
6. **Harness projection.** `inspect()` gained `authors`, `works`, `dates` and
   `extents` because the existing global no-coercion sweep could not see those
   nodes. Are there other rendered nodes still outside the projection?
