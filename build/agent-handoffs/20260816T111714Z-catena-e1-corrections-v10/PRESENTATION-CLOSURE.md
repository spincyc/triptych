# The presentation closure — contract, mechanism, evidence

## The contract

The V9 lane gave the spine's `text_prefix` three states and closed the
request layer; the V9 review passed that closure entire and found the third
state stopped at the model. This lane carries it to the reader. The two
no-text terminal states now make two different claims, because they are two
different facts:

    ABSENT           no text reference was supplied. The row, when its text
                     cannot be resolved, says: "This fragment carries no
                     text file, so nothing of it can be shown."

    REFUSED          a text reference was supplied, and was declined before
                     use. The row says: "A text reference was supplied for
                     this fragment, but it cannot be used as written, so no
                     text is shown." It does not say the corpus lacks the
                     text, the file is missing, a request failed, or
                     anything is blocked — none of which the refusal
                     establishes.

    PRESENT-VALID    unchanged: the composed request is made and the body
                     renders, with neither sentence anywhere on the row.

The refused sentence is stated once, in the unbudgeted model, as the
exported constant `TEXT_REFUSED`; the page renders the export and the suite
pins the page's rendering byte-exactly against it, so the two cannot drift.

The claim boundary is closed with the presentation. Absence at the exported
`fragmentRow` entry point is exactly one shape — `{stated: false,
trail: ''}`, the only absence `chapterFragments` ever builds — and every
contradictory or malformed direct claim, the review's exact
`{stated: false, trail: <valid>}` included, resolves no text and projects
as refused. Fail closed means classified closed: a contradictory claim is
not quietly read as absence, and no pairing of `text_refused` with a
usable-looking path can compose a request, substitute a cached body, or
leak body text, because the page consumes the refusal before it hands any
path to the request sink.

## The mechanism

Three edits — the diff is in `changes.patch`:

- `src/web/browser/catena/catena-model.js` states `TEXT_REFUSED` beside the
  namespace it answers to and exports it; `fragmentRow` derives
  `absent = claim.stated === false && claim.trail === ''` and uses it for
  the carried door, and projects
  `text_refused: !absent && !(stated === true && head !== '')` — everything
  that is neither the one absence shape nor a valid statement.
- `src/web/browser/catena/catena.js` consumes the projection first: the
  fragment-open handler checks `fragment.text_refused` BEFORE
  `fragmentText()`, renders `M.TEXT_REFUSED` under the existing muted
  style, and returns — so the request sink, the path-keyed body cache, and
  every late completion are unreachable from a refused row. The ordering is
  the fail-closed guarantee at the page: even a hypothetical contradictory
  row could not fetch.
- The V9 request-layer decision itself is untouched: composition, the
  carried door's own-stem requirement, and the thirteen-shape refusal
  matrix stand as reviewed.

## Valid-corpus evidence — real data, kept apart from the adversarial half

The production corpus emits exactly one prefix, `structure/catena/text/`,
on every tracked spine — every real spine is PRESENT-VALID and renders
exactly as before; no real row can show either no-text sentence unless its
text genuinely cannot be resolved. At the head, the Catena data check
replays the model over the real corpus and passes
(`logs/02-catena-check-head.log`), and the focused suite's valid-path
oracles hold (`logs/01-focused-catena-head.log`). The gzip budgets and
their unraised ceilings are measured in `logs/10-gzip-sizes-head.log`
against `logs/09-gzip-sizes-parent.log`: the page pays the refusal's
consumption inside its existing ceiling, and the sentence lives in the
model, which has none.

## Adversarial evidence — test fixtures, labelled as such

Every refused prefix in this package is an **adversarial test input, not a
corpus claim**; the fixtures carry the repository's standard adversarial
banner in their own bytes. The scenarios plant a real body at the carried
address — the reviewer's exact same-stem vector — so a leak is served and
rendered, caught by content and journal alike. The four terminal vectors
are pinned to EXPECTED VALUES, never to another snapshot, and the replay
now journals every request with its owning step and captures every
`replaceState` state argument and the standing `history.state`:

1. **Cold** — the reviewer's `structure/paragraphs/` prefix and its padded
   twin, each beside the valid carried path: the whole owned journal is the
   bootstrap, the row stands under its own identity and says the refused
   sentence with the absence sentence proven absent, and tally, the
   announcement journal and standing `statusText`, `aria-busy`, hash and
   history journals and `history.state`, focus pinned to its own expected
   value, and the error and failure sinks are each pinned.
2. **Present-valid** — the full terminal vector the V9 review found
   missing: the one composed request under its owning step, the rendered
   body, neither no-text sentence anywhere, and the same complete sink set
   pinned.
3. **Prewarmed** — chapter 1 loads the carried body legitimately under
   genuine absence; chapter 2 states a refused prefix while carrying the
   SAME path: the whole final journal is pinned entire — one fallback
   request ever, owned by the prewarm step — no cached substitution, no
   stale body, and the refused terminal pinned complete.
4. **Genuinely late** — A's carried resolution is HELD while B settles
   terminal in the refused chapter with its rows open; A releases only
   then: B's complete terminal baseline is pinned to expected values BEFORE
   and AFTER the release, the 36-field guarded comparison is retained on
   top, the journal's ownership shows the held request as A's own step, and
   the release is pinned at exactly zero-then-one.
5. **The claim boundary** — the exported `fragmentRow` is driven directly
   with eight contradictory claims beside the absence and valid controls:
   every contradictory claim resolves no text and projects as refused, and
   the model-level thirteen-shape matrix of V9 stands unchanged.
6. **The distinction itself** — a positive control each way: the
   genuine-absence scenario keeps the absence sentence, the refused
   scenario carries the refused sentence, the two are asserted unequal, and
   a neutrality sweep refuses any false claim inside the refused wording.

- `logs/11-request-journals-head.log` — the journals at the head: zero
  requests beyond bootstrap for the refused scenarios, exactly one carried
  request for the absence and prewarmed controls, the refused sentence at
  the terminal sinks.
- `logs/11-request-journals-parent.log` — the same scenarios at the parent:
  the false absence sentence standing over the refused rows, which is the
  presentation defect demonstrated rather than assumed.
- `logs/10-head-tests-against-parent.log` — the head's whole test file
  against the parent's production files; the distinguishing methods by
  name, decomposed in `DERIVED-CLAIMS.md` as methods run, controls passing
  at the parent, and failing subtest identities.
