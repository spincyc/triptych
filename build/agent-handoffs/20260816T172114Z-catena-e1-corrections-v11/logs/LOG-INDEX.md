# Log index

DERIVED, NOT TYPED. `logs/checks.py` writes this file from the two
battery ordering ledgers and from this directory, in the same pass
that composes `checks.txt`. Every log the package ships is listed
here with the attempt that produced it. This index is
`logs/LOG-INDEX.md`.

NAMING. A battery log is <attempt ordinal>-<slug>-<side>.log. The
two-digit ordinal names THE ATTEMPT, not the position of the step:
it is allocated from the append-only attempt ledger that lives
outside the package, so a rerun -- including a rerun against a fresh
logs directory -- receives a new ordinal and cannot reuse a
filename. Within one attempt a log is keyed by its slug, so a step
means the same thing on both sides; the two sides are two attempts
and therefore carry two ordinals, which is why the numbers differ
between them.

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
- attempt: parent-20260816T165256Z-02whnw23
- log prefix: 02
- tree at preflight: clean
- tree at postflight: DIRTY: 1 entries, 36 bytes; NOT CLEAN

- `logs/02-focused-catena-parent.log`
    - slug focused-catena; order 1; exit 0; attempt parent-20260816T165256Z-02whnw23
    - tree before clean; after clean
- `logs/02-catena-check-parent.log`
    - slug catena-check; order 2; exit 0; attempt parent-20260816T165256Z-02whnw23
    - tree before clean; after clean
- `logs/02-promised-parent.log`
    - slug promised; order 3; exit 0; attempt parent-20260816T165256Z-02whnw23
    - tree before clean; after clean
- `logs/02-full-discovery-parent.log`
    - slug full-discovery; order 4; exit 1; attempt parent-20260816T165256Z-02whnw23
    - tree before clean; after clean
- `logs/02-make-check-parent.log`
    - slug make-check; order 5; exit 2; attempt parent-20260816T165256Z-02whnw23
    - tree before clean; after clean
- `logs/02-release-bindings-parent.log`
    - slug release-bindings; order 6; exit 2; attempt parent-20260816T165256Z-02whnw23
    - tree before clean; after clean
- `logs/02-public-site-parent.log`
    - slug public-site; order 7; exit 0; attempt parent-20260816T165256Z-02whnw23
    - tree before clean; after clean
- `logs/02-browser-gate-parent.log`
    - slug browser-gate; order 8; exit 1; attempt parent-20260816T165256Z-02whnw23
    - tree before clean; after clean
- `logs/02-gzip-sizes-parent.log`
    - slug gzip-sizes; order 9; exit 0; attempt parent-20260816T165256Z-02whnw23
    - tree before clean; after clean
- `logs/02-head-tests-against-parent.log`
    - slug head-tests-against-parent; order 10; exit 1; attempt parent-20260816T165256Z-02whnw23
    - tree before clean; after DIRTY: 1 entries, 36 bytes; NOT CLEAN
- `logs/02-request-journals-parent.log`
    - slug request-journals; order 11; exit 0; attempt parent-20260816T165256Z-02whnw23
    - tree before DIRTY: 1 entries, 36 bytes; NOT CLEAN; after DIRTY: 1 entries, 36 bytes; NOT CLEAN

## HEAD battery

- ledger: `logs/order-head.txt`
- attempt: head-20260816T163721Z-01p59qj3
- log prefix: 01
- tree at preflight: clean
- tree at postflight: clean

- `logs/01-focused-catena-head.log`
    - slug focused-catena; order 1; exit 0; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean
- `logs/01-catena-check-head.log`
    - slug catena-check; order 2; exit 0; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean
- `logs/01-promised-head.log`
    - slug promised; order 3; exit 0; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean
- `logs/01-full-discovery-head.log`
    - slug full-discovery; order 4; exit 1; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean
- `logs/01-make-check-head.log`
    - slug make-check; order 5; exit 2; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean
- `logs/01-release-bindings-head.log`
    - slug release-bindings; order 6; exit 2; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean
- `logs/01-public-site-head.log`
    - slug public-site; order 7; exit 0; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean
- `logs/01-browser-gate-head.log`
    - slug browser-gate; order 8; exit 1; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean
- `logs/01-browser-static-head.log`
    - slug browser-static; order 9; exit 0; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean
- `logs/01-gzip-sizes-head.log`
    - slug gzip-sizes; order 10; exit 0; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean
- `logs/01-request-journals-head.log`
    - slug request-journals; order 11; exit 0; attempt head-20260816T163721Z-01p59qj3
    - tree before clean; after clean

## Everything else this directory carries

- `logs/LOG-INDEX.md` -- this index, written after the roster below was taken
- `logs/assemble.sh` -- the pipeline script itself, shipped so the package is replayable
- `logs/attempts.json` -- the attempt ledger rows this package was built from, copied in before the freeze
- `logs/battery.sh` -- the pipeline script itself, shipped so the package is replayable
- `logs/browser-gate-head.json` -- the gate's own JSON report, written by the recorded command; the log beside it is the short transcript
- `logs/browser-gate-parent.json` -- the gate's own JSON report, written by the recorded command; the log beside it is the short transcript
- `logs/checks.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/compare-gate.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/derive-claims.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/gate-comparison.log` -- P1: the two gate reports compared object for object, as a recorded pipeline step
- `logs/gzip-sizes.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/handoff-inventory.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/head-consistency.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/journal-dump.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/named-commits.json` -- the commits this package discusses, each with a reason
- `logs/order-head.txt` -- the ordering ledger one battery wrote as it ran
- `logs/order-parent.txt` -- the ordering ledger one battery wrote as it ran
- `logs/sanitize-and-seal.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/test-sanitize-and-seal.py` -- the pipeline tool itself, shipped so the package is replayable
- `logs/verify-final-package.py` -- the pipeline tool itself, shipped so the package is replayable

## Declared, and written after this index

These transcripts do not exist when this index is composed at P1.
They are named here as declarations, exactly as `logs/assemble.sh`
declares them deferred, and the phase that writes each is stated:

- `logs/sealer-tests.log` -- P1: the sealer's own test suite
- `logs/seal.log` -- P2: every normalization pass, appended
- `logs/seal-check.log` -- P2: the check-only pass that closed the fixpoint
- `logs/derive-claims.log` -- P4: the derivation, as it printed
- `logs/head-consistency.log` -- P5: the consistency audit
