# Limitations — E1 Catena correction V14

Each heading is one thing this lane did not close, or closed only within a
stated boundary. Nothing here is presented as done.

## The V13 review has no published ref

`origin` carries no `review/catena-wave-1-e1-corrections-v13-independent`; the
branch exists only in a local reviewer checkout at the reviewed head with no
review commit on it. The disposition, the findings and the exact next action
reach this lane through its brief. No review SHA is recorded for V14, the
provenance chain every earlier lane had is broken at this link, and this lane
cannot publish another lane's review.

## The authority gate's negative roster is neither confirmed nor reopened

V13's `authority-negative-fixtures` requirement stays `open` in the promise
ledger. The disposition as received does not name the gate's negative roster
either way, and marking it passed would be this lane answering a question the
review did not.

## The mutation probe covers one scenario

Freeze and prototype state are reported for every scenario that normalizes a
chapter. The thirteen actual assignment attempts run only for
`v14-authority-graph`. At the parent an unfrozen entry really moves, so a probe
running everywhere would contaminate the file it is reporting on.

## Identity is proved through a seam the production file carries

`chapterWitness` lives in `src/web/browser/catena/catena-model.js`. With no recorder installed it is
one `if` on a `null`, and the rest of the suite green is the evidence that the
page is unchanged by it — but the seam is in shipped bytes, not in the harness.

## Nested source closure is fail-closed and therefore wider than the defect

An own accessor at a nested source key now makes the chapter unreadable rather
than contributing an unreadable member. That is coherent and it is a widening.
No tracked corpus record uses an accessor.

## Six of the seven walked chapter members already held at the parent

Only `unfetched` moved the page at the reviewed head. The other six walks are
recorded as coverage that pins an existing closure, not as closures this lane
made, and their non-vacuity is proved by their steady walked-to controls rather
than by a parent failure.

## Add, remove and reorder of members already held at the parent

The V14 member matrix pins five structural effects. Only the phantom count and
the length read count fail at the parent; add, remove and reorder pass at both
endpoints because `records()` already snapshotted the list. They are recorded
as coverage with steady controls, not as closures.

## This lane's first attempt ledger is retired, and it is retired for an operator error

A parent battery that appeared dead was still running; it was closed out by
hand as `failed` and then wrote its own `complete` row, so one attempt carried
two dispositions and the ledger audit refused the file with four problems. The
head battery beside it was killed rather than allowed to finish into a record
nothing could be sealed against. Nothing was deleted: the incoherent ledger is
kept whole in the workspace under a retired name, a fresh ledger was opened,
and both batteries were rerun end to end. No figure in this package comes from
any attempt in the retired file. Two things this costs the reviewer: the
retired file is workspace state and is not a member of this package, so
`PROVENANCE.md` §1 states its contents and the gate's exact verdict on it
rather than shipping it; and one ordinal, the third, names an attempt in each
file — a preflight-refused attempt that ran nothing in the retired one, and a
real battery in the fresh one. Uniqueness of an ordinal *within* a ledger is
enforced by the allocator and holds; uniqueness *across* the retired file and
its replacement is not claimed.

## P10's rows do not reach the ledger slice shipped beside the archive

P9 derives the per-package attempt slice before P10 runs, and unlike P11 —
which copies its own row across — P10 has none. So the two post-seal gates and
the phase completion appear in the lane ledger and not in the slice a reviewer
holding this package opens. This lane's scope is semantic authority, not
packaging tooling, so it states the omission rather than changing the tool: the
only in-package record that P10 ran is the pair of gate transcripts named in
`HANDOFF.md` §10.

## The discard and supersession markers are covered by no sanitize pass

`<pkg>/DISCARDED.txt`, `<pkg>/logs/DISCARDED-<attempt>.txt`,
`<zip>.DISCARDED.txt`, `<stamp>-<name>.SUPERSEDED.txt` and the battery's own
`DISCARDED-<attempt>.txt` are outside every sanitize walk and every named
sibling list, and `logs/assemble.sh` skips P11 entirely on a run that already
failed — which is exactly the run on which a marker exists. Their contents are
symbolic by construction, and this package's own standard is that "by
construction" is an argument and not a check. No such marker is committed for
this lane's authoritative attempt unless one exists, and if one does it is
scanned by hand before it is added.

## The model is unbudgeted and grew again

36,679 to 39,724 gzipped whole and 8,873 to 9,396 stripped. Disclosed, not
presented as unchanged load. Whether the model and the combined route payload
need a governed ceiling is the budget owner's question and is now four lanes
old.

## `src/web/browser/catena/catena.js` has 28 gzipped bytes of headroom

12,972 against a 13,000 ceiling. The page is smaller than the parent left it,
and every semantic addition in this lane went into the model for that reason.
A later lane adding page prose will hit the ceiling before it hits a defect.

## Four release bindings remain stale and unsigned

`src/web/browser/catena/catena-model.js`, `src/web/browser/catena/catena.js`, `src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html`. None is
re-signed by this lane. `src/web/browser/catena/catena.css` and `src/web/browser/catena/index.html` are byte-identical to the
parent and are stale for reasons this lane did not create.

## Screenshots are omitted

This lane changes no ordinary visible composition: `src/web/browser/catena/catena.css` and
`src/web/browser/catena/index.html` are byte-identical at both endpoints and `src/web/browser/catena/catena.js` changes four
statements. The visible differences it does produce are adversarial-only and
are asserted at the exact DOM sinks. `guidance/external-review-handoffs.md`
requires raster evidence where a review concerns browser-visible behaviour;
this one concerns projection authority, and the DOM assertions are exact.

## The browser gate is red at both endpoints

2,290 assertions with an inherited failing set. It is identical at both
endpoints and identical to the V10–V13 reports, so it is compared rather than
passed. Nothing in this lane touches its causes.

## `make -k check` is red at both endpoints

The same four inherited targets. Compared as a set, not as an exit code.

## Every broader E1 blocker stays open

Full sole-source semantic projection beyond this bounded chapter projection;
orphan raw sources; source-only fragments still counting; scalar and nested
translator coercion beyond the edition list normalized here; malformed and
padded absence rows; the broader selection and ordering defects; refusal verse
typing; unreadable roots and the unreadable `src/web/data/bibles.json` prose; the broader
terminal and corrected-oracle proofs; the CLI/web duplicated semantic model;
the historical data seam. Release bindings, the common gate, B0/shared shell,
real-device and assistive-technology evidence, protected Liturgy and PDFs are
separately owned. E1 is not integrated.
