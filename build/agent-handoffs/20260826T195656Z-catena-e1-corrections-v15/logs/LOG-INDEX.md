# Log index

DERIVED, NOT TYPED. `logs/checks.py` writes this file from the two
battery ordering ledgers and from this directory, in the same pass
that composes `checks.txt`. Every log the package ships is listed
here with the attempt that produced it. This index is
`logs/LOG-INDEX.md`.

NAMING. Every attempt writes into a root of its own under `logs/`,
named attempt- followed by the two-digit ATTEMPT ORDINAL, and a
battery transcript inside it is <slug>-<side>.log. The ordinal names
THE ATTEMPT, not the position of the step: it is allocated from the
append-only attempt ledger that lives outside the package, so a rerun
-- including a rerun against a fresh logs directory -- receives a new
root and cannot reuse a path. Within one attempt a transcript is
keyed by its slug, so a step means the same thing on both sides; the
two sides are two attempts and therefore carry two ordinals, which is
why the roots differ between them.

WHY THE ORDINAL IS THE DIRECTORY. V11 put it in the battery filename
and left the package-phase transcripts -- the gate comparison, the
sealer tests, the seal passes, the derivation, the consistency audit
-- with no ordinal at all. In the reviewed package the
gate-comparison transcript was claimed by six different attempts and
the sealer-tests transcript by five: a failed attempt's logs did not
stay with that attempt, the next attempt opened the same path and
overwrote them. The root carries the ordinal now, so battery and
package phases are carried by one rule instead of one and none, and
`logs/checks.py --audit-logs` refuses a package in which any
transcript is claimed by other than exactly one attempt.

WHERE THE COMMANDS ARE. The exact command string of every row below
is recorded verbatim in `checks.txt`, on the row for the same log.
It is also carried as data in `logs/attempts.json`, together
with the disposition of every attempt this package was built
from. Commands are NOT repeated in this document: a recorded
command contains bare artifact names that are its arguments and
not members of this package, and the audits that read documents
would read them as promises the package had made.

## PARENT battery

- ledger: `logs/order-parent.txt`
- attempt: parent-20260826T190950Z-014jgstx
- log root: attempt-01 (under logs/)
- tree at preflight: clean
- tree at postflight: clean

- `logs/attempt-01/focused-catena-parent.log`
    - slug focused-catena; order 1; exit 0; attempt parent-20260826T190950Z-014jgstx
    - tree before clean; after clean
- `logs/attempt-01/catena-check-parent.log`
    - slug catena-check; order 2; exit 0; attempt parent-20260826T190950Z-014jgstx
    - tree before clean; after clean
- `logs/attempt-01/promised-parent.log`
    - slug promised; order 3; exit 0; attempt parent-20260826T190950Z-014jgstx
    - tree before clean; after clean
- `logs/attempt-01/full-discovery-parent.log`
    - slug full-discovery; order 4; exit 1; attempt parent-20260826T190950Z-014jgstx
    - tree before clean; after clean
- `logs/attempt-01/make-check-parent.log`
    - slug make-check; order 5; exit 2; attempt parent-20260826T190950Z-014jgstx
    - tree before clean; after clean
- `logs/attempt-01/release-bindings-parent.log`
    - slug release-bindings; order 6; exit 2; attempt parent-20260826T190950Z-014jgstx
    - tree before clean; after clean
- `logs/attempt-01/public-site-parent.log`
    - slug public-site; order 7; exit 0; attempt parent-20260826T190950Z-014jgstx
    - tree before clean; after clean
- `logs/attempt-01/browser-gate-parent.log`
    - slug browser-gate; order 8; exit 1; attempt parent-20260826T190950Z-014jgstx
    - tree before clean; after clean
- `logs/attempt-01/gzip-sizes-parent.log`
    - slug gzip-sizes; order 9; exit 0; attempt parent-20260826T190950Z-014jgstx
    - tree before clean; after clean
- `logs/attempt-01/head-tests-against-parent.log`
    - slug head-tests-against-parent; order 10; exit 1; attempt parent-20260826T190950Z-014jgstx
    - tree before clean; after DIRTY: 1 entries, 36 bytes; NOT CLEAN
- `logs/attempt-01/request-journals-parent.log`
    - slug request-journals; order 11; exit 0; attempt parent-20260826T190950Z-014jgstx
    - tree before DIRTY: 1 entries, 36 bytes; NOT CLEAN; after DIRTY: 1 entries, 36 bytes; NOT CLEAN
- `logs/attempt-01/restore-parent-tree.log`
    - slug restore-parent-tree; order 12; exit 0; attempt parent-20260826T190950Z-014jgstx
    - tree before DIRTY: 1 entries, 36 bytes; NOT CLEAN; after clean

## HEAD battery

- ledger: `logs/order-head.txt`
- attempt: head-20260826T192452Z-02kjv34n
- log root: attempt-02 (under logs/)
- tree at preflight: clean
- tree at postflight: clean

- `logs/attempt-02/focused-catena-head.log`
    - slug focused-catena; order 1; exit 0; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean
- `logs/attempt-02/catena-check-head.log`
    - slug catena-check; order 2; exit 0; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean
- `logs/attempt-02/promised-head.log`
    - slug promised; order 3; exit 0; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean
- `logs/attempt-02/full-discovery-head.log`
    - slug full-discovery; order 4; exit 1; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean
- `logs/attempt-02/make-check-head.log`
    - slug make-check; order 5; exit 2; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean
- `logs/attempt-02/release-bindings-head.log`
    - slug release-bindings; order 6; exit 2; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean
- `logs/attempt-02/public-site-head.log`
    - slug public-site; order 7; exit 0; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean
- `logs/attempt-02/browser-gate-head.log`
    - slug browser-gate; order 8; exit 1; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean
- `logs/attempt-02/browser-static-head.log`
    - slug browser-static; order 9; exit 0; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean
- `logs/attempt-02/gzip-sizes-head.log`
    - slug gzip-sizes; order 10; exit 0; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean
- `logs/attempt-02/request-journals-head.log`
    - slug request-journals; order 11; exit 0; attempt head-20260826T192452Z-02kjv34n
    - tree before clean; after clean

## Everything else this directory carries

- `logs/LOG-INDEX.md` -- this index, written after the roster below was taken
- `logs/assemble.sh` -- the pipeline script itself, shipped so the package is replayable
- `logs/attempt-01/browser-gate-parent.json` -- the gate's own JSON report, written by the recorded command; the log beside it is the short transcript
- `logs/attempt-02/browser-gate-head.json` -- the gate's own JSON report, written by the recorded command; the log beside it is the short transcript
- `logs/attempt-06/gate-comparison.log` -- P1: the two gate reports compared object for object, as a recorded pipeline step
- `logs/authority-coherence.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/battery.sh` -- the pipeline script itself, shipped so the package is replayable
- `logs/checks.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/compare-gate.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/derive-claims.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/gate-summary.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/gzip-sizes.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/handoff-inventory.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/head-consistency.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/journal-dump.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/named-commits.json` -- the commits this package discusses, each with a reason
- `logs/order-head.txt` -- the ordering ledger one battery wrote as it ran
- `logs/order-parent.txt` -- the ordering ledger one battery wrote as it ran
- `logs/sanitize-and-seal.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/test-attempt-history.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/test-authority-coherence.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/test-handoff-inventory.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/test-sanitize-and-seal.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/test-verify-final-package.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/verify-final-package.py` -- the pipeline tool itself, shipped so the package is replayable

## Declared, and written after this index

These members do not exist when this index is composed at P1. They
are named here as declarations, exactly as `logs/assemble.sh`
declares them deferred, and the phase that writes each is stated:

- `logs/attempt-06/sealer-tests.log` -- P1: the sealer's own test suite
- `logs/attempt-06/seal.log` -- P2: every normalization pass, appended
- `logs/attempt-06/seal-check.log` -- P2: the check-only pass that closed the fixpoint
- `logs/attempt-06/derive-claims.log` -- P4: the derivation, as it printed
- `logs/attempt-06/head-consistency.log` -- P5: the consistency audit
- `logs/attempts.json` -- P5: the attempt rows this package was built from, composed after the consistency audit so it carries the sealing attempt's own terminal row
