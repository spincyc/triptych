# Battery provenance — retained runs, and none discarded

The exact parent and head SHAs and every derived figure of both batteries
are in `claims.json`. The V9 review found provenance asserted only in this
file, after the fact; it is now **emitted by the batteries themselves as
they run**. Each ordering ledger opens with a preflight the battery wrote
before its first step — the exact checked-out `sha=`, the
`git status --porcelain` result as `porcelain=clean` or a byte count, and
the working directory as the `cwd=$REPO` token — and closes with a
postflight that re-reads the commit and records `sha-drift=none`; a drifted
battery is a failed battery. This file only says where the runs happened.

## The retained runs — authoritative

- **Head battery** — the V10 implementation clone, checked out at the exact
  V10 head with a clean tree. Ledger: `logs/order-head.txt`; every command,
  its unique indexed log, exit, timestamps, and the preflight/postflight
  are there, written as it ran.
- **Parent battery** — a separate parent-side clone, checked out at this
  lane's exact parent — the reviewed V9 candidate — with a clean tree at
  battery start. Ledger: `logs/order-parent.txt`. Its final steps overlay
  the head's test file over the parent's and re-run the replay — the
  overlay is part of the recorded command, which is what makes the run mean
  what it means — and the clone was restored to the exact parent state
  afterwards.

Both clones' absolute path prefixes are normalized by the sealer and the
sanitization scan proves no operator identity survived; the `cwd=$REPO`
tokens were written as tokens, not sanitized into them.

## Discarded runs — none among the batteries

Every V10 battery run is retained and its ledger is in the package;
the unique-log protocol would have preserved a discarded run's own marked
rows and logs had one existed. The V8-era discarded `/tmp` run remains
ledgered in the sealed V9 package's provenance and is used in no comparison,
figure, or claim here.

## The discarded assembly attempts — recorded, used nowhere

Two assembly attempts failed closed and were discarded, each retained
unmodified under the repository's ignored build tree, each superseded by a
fresh stamp rather than reused. Stamp `20260816T111559Z` stopped at P2: the
evidence-index check refused four document references that did not resolve
against the package root. Stamp `20260816T111641Z` stopped at P5: the
consistency audit refused two documents for naming the deliberately omitted
sources record by a resolvable filename. In both attempts the pipeline
refused before any manifest or archive existed; the documents were
corrected and no figure or claim derives from either attempt.

## Pre-battery working runs, used for no packaged claim

Before the batteries, the implementation session ran the same checks
informally while iterating (including one full-discovery and one
`make -k check` run that raced the in-progress durable-record edits and
were discarded as smoke). No packaged figure derives from any of them:
every figure in `claims.json` and `checks.txt` comes from the two
ledgered batteries above, and the ledgers' own preflights prove the trees
those batteries measured.
