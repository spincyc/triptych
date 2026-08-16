# The composed closure — contract, mechanism, evidence

## The contract

The spine's `text_prefix` has three states, and the carried fallback door
answers to the state, not to a truthy value:

    ABSENT           the spine record does not carry the property.
                     A carried `text_path` MAY be consulted, and stands only
                     when it is byte-exact inside `structure/catena/text/`
                     with the fragment's own validated stem.

    PRESENT-VALID    the statement passes `textTrail`: byte-exact inside the
                     owned namespace, no whitespace repair. The request is
                     composed from the statement and the fragment's own id;
                     the carried path is never consulted.

    PRESENT-INVALID  the statement fails `textTrail` — null, a record, a
                     list, a number, a flag, an empty string, whitespace, a
                     wrong namespace, the padded right namespace, traversal,
                     an absolute path, malformed encoding, the `textual/`
                     boundary spoof. The statement is REFUSED, and the
                     refusal is terminal for that text resolution: no
                     composed request, no carried fallback, no rewrite into
                     the namespace, no cached substitution, no late
                     completion. The row stands, says it carries no text
                     file, and keeps the refusal as `text_refused`.

Absence is defined precisely: the `text_prefix` property is not carried by
the spine record itself (`Object.hasOwn`). Everything carried — whatever its
type or value — is a statement, and a statement this page cannot validate is
refused, never reinterpreted as missing.

## The mechanism

Two functions in `src/web/browser/catena/catena-model.js` — the diff is in
`changes.patch`:

- `chapterFragments` derives the statement `{stated, trail}` once per spine:
  `stated` is property presence on the record itself, `trail` the
  `textTrail`-validated value or `''`. The V8 defect was here and in the
  consumer: `textTrail` alone mapped ABSENT and REFUSED to the same `''`.
- `fragmentRow` re-asks both members (it is an exported entry point),
  composes `trail + id + '.json'` only from a valid statement, opens the
  carried door only on `stated === false` with the pre-existing
  `textLeaf` + own-stem requirement on top, and projects
  `text_refused` so the refusal survives onto the row. The decision uses
  explicit comparisons, not truthiness.

Both run before projection completes, which is earlier than any request
exists. `src/web/browser/catena/catena.js` is untouched: a refused statement
projects `text_path: ''`, which the page already treats as terminal — no
request, the truthful no-text sentence — and the path-keyed body cache is
never consulted because no path is ever composed.

The isolated V8 validators — `TEXT_HOME`, `textTrail`, `textLeaf` — are
unchanged, and the V8 classes that pin them stay green
(`logs/focused-catena-head.log`).

## Valid-corpus evidence — real data, kept apart from the adversarial half

The production corpus emits exactly one prefix, `structure/catena/text/`,
on every tracked spine — every real spine is PRESENT-VALID, and its composed
request set is byte-identical under the three-state derivation. At the head,
the Catena data check replays the model over the real corpus and passes
(`logs/catena-check-head.log`), and the focused suite's valid-path oracles
hold unchanged (`logs/focused-catena-head.log`). The gzip budgets and their
unraised ceilings are measured in `logs/gzip-sizes-head.log` against
`logs/gzip-sizes-parent.log`.

## Adversarial evidence — test fixtures, labelled as such

Every refused prefix in this package is an **adversarial test input, not a
corpus claim**; the fixtures carry the repository's standard adversarial
banner in their own bytes. The scenarios plant a real body at the carried
address — structure/catena/text/fallback-owned.json, the reviewer's exact
same-stem vector — so a leak is served and rendered, caught by content and
journal alike:

1. **Cold** — the reviewer's `structure/paragraphs/` prefix, and the padded
   right-namespace prefix, each beside the valid carried path: the entire
   fetched journal is pinned to the bootstrap, the planted body reaches no
   sink, and every terminal projection is asserted — rows, tally, the
   announcement journal AND the standing `statusText`, `aria-busy`, hash,
   history, `activeElement`, error and failure sinks.
2. **Prewarmed** — chapter 1 loads the carried body legitimately under
   genuine absence; chapter 2 states a refused prefix while carrying the
   SAME path: one fallback request ever, no cached substitution, the
   no-text terminal stands.
3. **Genuinely late** — A's carried resolution is HELD while B settles
   terminal in the refused chapter with its rows open; A releases only
   then: every guarded projection compared entire, the release proved to
   have happened, nothing moved.
4. **The doors kept open** — genuine absence still fetches and renders the
   carried body; a valid prefix composes its own address while the planted
   carried body goes unasked.
5. **The model-level matrix** — the exported `chapterFragments` classifies
   thirteen refused shapes beside the absent and valid states, each
   terminal with `text_refused` kept.

- `logs/request-journals-head.log` — the journals at the head: zero
  requests beyond bootstrap for the refused scenarios, exactly one carried
  request for the absence and prewarmed controls.
- `logs/request-journals-parent.log` — the same scenarios at the parent:
  the carried fallback request actually made after the refused prefix,
  which is the defect demonstrated rather than assumed.
- `logs/v8-tests-against-parent.log` — the head's whole test file against
  the parent's production files; the composed-closure classes fail there by
  name, and `DERIVED-CLAIMS.md` carries the derived decomposition.
