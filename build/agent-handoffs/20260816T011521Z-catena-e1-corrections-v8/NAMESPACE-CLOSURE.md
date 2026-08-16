# The namespace closure — contract, mechanism, evidence

## The contract

The only namespace a Catena text request may resolve in is, byte for byte:

    structure/catena/text/

A candidate address is valid only when it satisfies the existing path-safety
grammar **and** lies inside that directory, where "inside" is a
directory-boundary test: the trailing slash is part of the contract, so
`structure/catena/textual/` is another namespace and not a longer spelling of
this one. Same filename, same stem, same suffix, structural similarity and a
start under some other `structure/` directory each authorize nothing.

An address that fails is refused whole: not trimmed into validity, not
stringified, not URL-encoded into apparent safety, not stripped to a
basename, not rewritten into the namespace, not replaced by a same-stem
fallback, and not attempted in the hope of an HTTP failure. **Invalid
namespace means no request**, and the fragment's row stands and says it
carries no text file — no successful load, no refusal claim, no absence
claim, no other same-stem text, no stale content.

## The mechanism

One constant and two validators in `src/web/browser/catena/catena-model.js`,
beside the grammars
they narrow — the diff is in `changes.patch`:

- `TEXT_HOME` — the namespace, stated once.
- `textTrail` — `trail`'s grammar, AND the byte-exact namespace, AND no
  whitespace repair. Applied to the file-level `text_prefix` in
  `chapterFragments`, so a composed path is inside the namespace by
  construction: prefix in the namespace, stem the fragment's own validated
  id, suffix the corpus's own.
- `textLeaf` — `leaf`'s grammar, AND the byte-exact namespace, AND no
  whitespace repair. Applied to the carried fallback in `fragmentRow`, where
  the existing same-stem requirement still stands on top of it.

Both run before projection completes, which is earlier than any request
exists. `src/web/browser/catena/catena.js` is untouched: the page consumes the projected
`text_path` exactly as before, and an empty one composes no request, exactly
as before.

Type failures — object, array, number, boolean, null, empty, whitespace-only
— and grammar failures — traversal in or out, absolute, encoded traversal,
malformed encoding, duplicate separators — were already refused by `leaf`
and remain refused; the head's focused log shows the V7 classes that pin them
still green (`logs/focused-catena-head.log`).

## Valid-corpus evidence — real data, kept apart from the adversarial half

The production corpus emits exactly one prefix, `structure/catena/text/`, and
no per-fragment `text_path`; the fixture corpus carries per-fragment paths,
all inside the namespace. At the head, the Catena data check replays the
model over the real corpus and passes (`logs/catena-check-head.log`), and the
focused suite's existing valid-path oracles — the composed request set of a
real-shaped chapter, and the one owned carried path of the sample-corpus
shape — hold unchanged (`logs/focused-catena-head.log`). The gzip budgets
and their unraised ceilings are measured in `logs/gzip-sizes-head.log`
against `logs/gzip-sizes-parent.log`.

## Adversarial evidence — test fixtures, labelled as such

Every wrong-namespace path in this package is an **adversarial test input,
not a corpus claim**; the fixtures carry the repository's standard
adversarial banner in their own bytes. Nothing here asserts that the
production corpus emits hostile paths — the parent-side journal demonstrates
what the code *would do* if one arrived, which is the review's finding.

Three replay scenarios drive the closure at the real sink, each planting a
real text body at the wrong-namespace address so a leak would be served and
rendered rather than quietly 404ing:

1. the reviewer's prefix vector — `structure/paragraphs/` as `text_prefix`
   over readable ids;
2. the padded right-namespace prefix — whitespace around
   `structure/catena/text/`, which the parent trims into a valid address;
3. the carried matrix — same-stem `structure/paragraphs/text/`, sibling,
   parent and root `structure/` forms, another corpus directory, traversal in
   and out, absolute, the `textual/` boundary spoof, the padded valid form,
   and one genuinely owned path as the control.

The assertions pin the **entire fetched journal**, in order; assert the
planted words appear at no visible or announced sink; and hold the terminal
state — `aria-busy` released, status written once, rows standing and
truthful, no error section, no history write, nothing replaced.

- `logs/request-journals-head.log` — the journals at the head: zero requests
  beyond bootstrap for the two prefix scenarios, exactly one owned request
  for the carried matrix.
- `logs/request-journals-parent.log` — the same scenarios at the parent: the
  wrong-namespace and padded requests actually made, which is the defect
  demonstrated rather than assumed.
- `logs/v8-tests-against-parent.log` — the head's whole test file against
  the parent's production files; the namespace classes fail there by name,
  and `DERIVED-CLAIMS.md` carries the derived decomposition.
