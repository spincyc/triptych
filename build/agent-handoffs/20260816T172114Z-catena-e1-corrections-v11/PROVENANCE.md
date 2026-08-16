# Provenance — which runs are authoritative, and how that is recorded

The exact head and parent SHAs and every derived figure of both batteries
are in `claims.json`. This file says where the runs happened, how their
provenance was captured, and which runs are not authoritative.

## Provenance is emitted as the runs happen, and read per command

Each battery's ordering ledger opens with a preflight the battery wrote
before its first step: the exact checked-out `sha=`, the
`git status --porcelain` result as `porcelain=clean` or a byte count, and
the working directory written as the `cwd=$REPO` token.

**The V11 correction is that the tree is read per command, not once.** The
V10 package attached one preflight `clean` to every command row of both
batteries, and that reading was provably false for the last two steps of the
parent battery, whose recorded command overlays the head's test file onto
the parent checkout and therefore dirties a tracked file before it runs.
Every row of both ledgers now carries its own `TREE-BEFORE:` and
`TREE-AFTER:` readings, taken immediately around that command. A step that
dirties the tree is recorded dirty on its own row, and so is every row after
it, instead of inheriting a preflight that stopped being true.

Concretely, in the parent battery the `head-tests-against-parent` step's
recorded command is the copy **and** the test run, because the substitution
is what makes the run mean what it means. The copy overwrites the tracked
file `tools/tests/test_catena_wave_1.py`, and the ledger records exactly
that: the step enters with `TREE-BEFORE: clean`, leaves with
`TREE-AFTER: DIRTY: 1 entries, 36 bytes; NOT CLEAN`, and the following
`request-journals` step opens with the same dirty reading. **The parent
battery's postflight closes DIRTY as well** — the overlay was not reverted
before the battery ended, and the ledger says so rather than reporting a
clean tree it did not observe. The two last parent rows therefore describe
the parent's production files with the head's test file laid over them,
which is what those two steps are for; every earlier parent row ran clean.

This is precisely the reading V10 got wrong. It attached one preflight
`clean` to every row of both batteries, which was false for these same two
steps. Read the ledger rows for the truth of any one command; the preflight
is a claim about the battery's first instant and about nothing else.

Each ledger closes with a postflight that re-reads the commit and the tree.
Both batteries record `sha-drift=none`. The head battery closes clean, at
the head `0255b84996e1dc24da3ce75ac318c4f774b7957c`.
The parent-side battery closes dirty, at
`ea15d16d22d7ceaed989ed9907c236f967738a03`, for the reason above. A
battery whose HEAD drifted mid-run is a failed battery and is discarded
rather than reported; neither of these drifted.

## The batteries

- **Head battery** — the V11 implementation clone, checked out at the exact
  V11 head `0255b84996e1dc24da3ce75ac318c4f774b7957c`, tree clean at
  preflight. Its ledger is `logs/order-head.txt`.
- **Parent battery** — a separate parent-side clone, checked out at this
  lane's exact parent `ea15d16d22d7ceaed989ed9907c236f967738a03`, which is
  the exact reviewed V10 head, tree clean at preflight and dirty at
  postflight for the reason stated above. Its ledger is
  `logs/order-parent.txt`.

Both are named with the attempt that produced them; `logs/LOG-INDEX.md`
joins every shipped log to its attempt, its slug, its exit and its per-row
tree readings, and is derived mechanically from the ledgers and the
directory rather than typed.

## Log identity comes from an attempt ledger, not from a counter

The V10 package numbered logs by position within a battery, so the same
number meant a different step on the head side and the parent side. V11
allocates the numeric part of a log name from an **append-only attempt
ledger that lives outside the package**, at
`build/agent-handoffs/attempt-ledger.jsonl`. The ordinal names the
ATTEMPT; within one attempt a log is keyed by its SLUG. So a step means the
same thing on both sides, the two sides carry two ordinals because they are
two attempts, and a rerun — including a rerun against a fresh log directory
— receives a new ordinal and cannot reuse a filename. A log target that
already exists is refused rather than overwritten.

`logs/attempts.json` carries the rows this package was built from, copied
from that outside ledger before the freeze, filtered only by attempt
identity. Each row states what one step did; the `record=attempt` row of the
same attempt states whether that attempt is authoritative or discarded, and
its **one** reason. Every failure path in the pipeline writes exactly one
such disposition, and a partially built package directory is marked in place
with a discard marker naming the phase and the one reason, rather than being
deleted or repaired. The correction for a failed assembly is a fresh UTC
stamp, never a deletion and never a reuse.

## What was discarded

This package does not claim that nothing was discarded. Five things are
true, and they are stated in one place so that no document contradicts
another. The enumerated authority is `logs/attempts.json`, not this prose:
it names every attempt this package was built from and gives each one a
terminal disposition with exactly one reason.

1. **Two assembly attempts were discarded, and neither stamp was reused.**
   Attempt `package-20260816T171438Z-03g4tknr` stopped at P1 for one reason:
   the sealer's own test suite failed, and a package sealed by an unproven
   sealer is not evidence of privacy. Attempt
   `package-20260816T171652Z-046xn6k4` stopped at P2 for one reason: the
   first normalize pass failed, because `screenshots/INDEX.md` named its own
   images by bare filename and the package-reference audit resolves
   references against the package root, so thirty-one real members read as
   thirty-one missing ones. Both refused rather than overwrote; both left a
   partially built directory carrying its own discard marker, a plain-text file naming the
   attempt, the phase, the reason and the exact head; and this package
   carries a later stamp because an existing target is never reused.

2. **The first of those two was a seam, not a guard failure, and is worth
   naming as such.** `logs/assemble.sh` runs the sealer's suite as a phase and
   exports its whole configuration first, so the suite's own throwaway
   assembly inherited the real run's `ASSEMBLE_INNER` marker, silently
   entered inner mode, and printed a refusal one line shorter than the one
   the test asserts. The guard never weakened — the refusal fired, and
   nothing was reused, merged, overwritten or deleted. Two corrections
   followed: the P0 refusal now words itself identically however it is
   reached, and the suite clears the pipeline's own environment rather than
   inheriting it.

3. **The attempt ledger was cleaned once, and the raw one is kept.** The
   same inheritance defect pointed throwaway batteries at this lane's
   `ATTEMPTS` path, so six attempts belonging to no lane work appended rows
   here. A reader would have counted several authoritative head batteries
   where this lane ran exactly one. Every one of those rows was truthful
   about the invocation that wrote it and misleading about what this package
   measured, which is the harder kind of wrong. They were SET ASIDE, not
   deleted: `logs/attempts.json` carries this lane's four attempts — the head
   battery, the parent battery, and the two discarded assemblies — and the
   unedited original is retained outside the package, beside the live ledger and under the same
   name with a raw suffix. The six set-aside identities are named here so
   the difference is checkable rather than asserted:
   `head-20260816T171455Z-03v5smpw`, `head-20260816T171456Z-03rhzj64`,
   `head-20260816T171617Z-03vty6mt`, `head-20260816T171618Z-03jxz23w`,
   `head-20260816T171704Z-04j24thj`, `head-20260816T171705Z-04v46hpp`. None
   of them measured this candidate, and no figure in this package derives
   from any of them.

4. **A raced measurement was discarded and is used for no figure.** Full
   discovery run concurrently with `make -k check` reports 250 errors rather
   than 13, because that target builds and then removes `build/.web-current`
   and the public site underneath the tests. The batteries run those two
   steps in sequence; the 1,885 / 14 / 13 / 11 figure this package states
   comes from an isolated run, and the raced run is not used for any claim.

5. **Informal pre-battery runs exist and are not evidence.** While
   implementing, the same checks were run informally and repeatedly. No
   packaged figure derives from any of them: every figure in `claims.json`
   and `checks.txt` comes from the two ledgered batteries above, and the
   ledgers' own per-command tree readings prove which tree each measured
   figure describes.

Earlier lanes' discarded assemblies and discarded smoke runs remain recorded
in their own sealed packages' provenance. They are used in no comparison, no
figure and no claim here.

## Where the paths went

Both clones' absolute path prefixes are normalized by the sealer, and the
scan re-derives the private values from the environment and asks whether any
survives. That is a post-seal fact, proved by `logs/seal.log` and
`logs/seal-check.log`, not by this sentence; `PRIVACY-AUDIT.md` states which
claims become true at which phase. The `cwd=$REPO` tokens in the ledgers
were written as tokens by the battery itself, so that identity was never in
the record for the sealer to catch.

This file says where the runs happened. It does not claim the environment
was hermetic, and nothing in this package does.
