# Review request — Catena E1 V9

**The exact head, the parent, the review answered and every count in this
package are in `DERIVED-CLAIMS.md` and `claims.json`, computed from the
frozen member inventory by `logs/derive-claims.py`.** No identity or figure
is typed into this file, and `logs/head-consistency.py` refuses a package
whose prose names a commit those claims do not entitle it to name.

This file is questions only. The review that dispatched this lane asked for
a fresh independent review of the exact head, **scoped to the composed
prefix/fallback closure and the package's final-byte correctness**; the
questions below are in that order.

---

## The closure itself

### 1. Is absence defined at the right place?

Absence is property absence on the spine record itself (`Object.hasOwn`);
everything carried — `null`, a record, a list, a number, a flag, `''`,
whitespace, any invalid string — is a statement, and a failed statement is
refused, never demoted to missing. Is property presence the right line, or
does the schema entitle some carried shape (for instance `null`) to mean
"no statement"?

### 2. Is the refusal's terminal sentence truthful enough?

A refused statement projects `text_path: ''` and the page prints the
existing sentence — "This fragment carries no text file, so nothing of it
can be shown." The row keeps the distinction as `text_refused`, but the
page does not yet print a distinct sentence for it: `src/web/browser/catena/catena.js` is
untouched, and its whole-file budget holds 99 bytes of headroom. The
correction brief authorized the existing truthful terminal state where
appropriate. Should the next lane spend the bytes to say "the record's
stated text location was refused" instead, or is the row-level fact with
the shared sentence the right economy?

### 3. Is `text_refused` at the right altitude?

The refusal is a spine-level fact projected per row, following the
`acknowledgement_broken` idiom, so the row — the only channel across the
model/page boundary — carries it to any consumer. Should it instead be a
chapter-level fact, or is per-row projection right for a per-row decision?

### 4. Is the sink evidence sufficient?

The journals pin the replay harness's stubbed `fetch`, the same seam the V7
and V8 reviews used to prove their defects; the prewarmed and genuinely
late scenarios drive the same seam with the harness's deferred-release
primitives. No real-Chromium probe of this route is included, for the
reason `LIMITATIONS.md` §3 states. Is that the right economy, or should the
fresh review require one?

## The package correction

### 5. Is the frozen-inventory partition the right sealing contract?

`claims.json` now claims bytes and hashes only for members frozen before
derivation, names the five derivation-time members without sizing or
hashing them, and the two sets must partition the member set exactly; the
final-byte authorities are `MANIFEST.sha256`, the ZIP and the sidecar, and
`logs/verify-final-package.py` re-derives every claim read-only from the
final ZIP. Is naming-without-sizing the right treatment of the members that
cannot truthfully carry their own final bytes, or should the protocol go
further and move all derived members outside the archive?

## The lane's boundaries

### 6. Is the record update proportionate?

The durable records gain one lane section, one roadmap section and row, one
ownership-row move, and one ledger deliverable; the review's own record is
referenced by SHA and deliberately not merged into implementation history.
Is anything missing that the next lane will need, or anything present that
overstates this lane?

## Standing questions this lane re-asks rather than answers

### 7. The uncapped combined payload

The model grew by the closure's own bytes and carries no ceiling; the two
files' combined gzipped payload is measured at both ends in
`logs/gzip-sizes-head.log` and `logs/gzip-sizes-parent.log` and disclosed
in the durable records. The V5, V6, V7 and V8 reviews each asked the owner
whether the model should be capped and none was answered. The question
stands a fifth time; this lane could not answer it for itself.
