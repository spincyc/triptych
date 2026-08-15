# Evidence index — every artifact, what it supports, what it does not

Every member of this package is named below. `logs/head-consistency.py`
refuses a package containing a member nothing references, so this list being
complete is checked rather than promised — and its transcript,
`logs/head-consistency.log`, is here.

**No figure appears in this file.** Every count, size, digest and identity is
in `claims.json` and its rendering `DERIVED-CLAIMS.md`, both written in one
pass by `logs/derive-claims.py` at seal time. That is the direct answer to the
V6 review's five wrong counts: a number typed into prose is a second record of
a fact, and this package keeps one.

---

## The argument

| Member | Supports | Does not prove |
| --- | --- | --- |
| `HANDOFF.md` | the task, the branch, what was wrong, what was done, and the inventory | nothing on its own; every claim in it points at an artifact |
| `TYPED-PROJECTION.md` | what crosses the typed boundary and what does not, field by field, and why each gate is the gate it is | that the line is drawn in the right place — that is a judgement, and `REVIEW_REQUEST.md` asks about the two places it is closest |
| `CORRECTED-ORACLES.md` | every test expectation this correction changed, with the defect each had blessed | that no other oracle needs correcting |
| `REVIEW_REQUEST.md` | the six decisions this lane could not make for itself, and three optional questions | it asserts nothing; it is questions only |
| `LIMITATIONS.md` | what this package does not prove, opening with the V6 evidence faults | — |
| `UNRESOLVED-BLOCKERS.md` | the open items this lane did not touch, each with its owner | that any of them is small |
| `DATA-TEST-CONTRADICTION.md` | the `src/web/data/` guard contradiction, preserved untouched | which of the two contradicting records is wrong |
| `PRIVACY-AUDIT.md` | the sanitization method, its captured transcripts, and the sealer's own two corrected defects | that no private token exists that no pattern can recognise — §"What remains unsolvable by pattern" |

## The derived record

| Member | Supports | Does not prove |
| --- | --- | --- |
| `claims.json` | **the source for every figure in this package**: identity, ancestry, commits, diffstat, gzip payload at both ends, suite counts and identity sets, gate totals, the test delta, the package inventory and the byte scan | a judgement. It records what is; it cannot say whether it should be |
| `DERIVED-CLAIMS.md` | the same values, rendered, written in the same pass from the same dict | — |
| `logs/derive-claims.py` | how each of them is computed, from the head, the parent and the package directory alone | — |
| `logs/derive-claims.log` | that derivation's own transcript | — |
| `logs/head-consistency.py` | that no member names a commit this package may not name, calls the head a parent, names a path the package lacks, or goes unreferenced | that a *correct* SHA is used in the *right* sentence |
| `logs/head-consistency.log` | that audit's run, including the inventory gap between derivation time and seal time, derived rather than hidden | — |
| `logs/named-commits.json` | the commits this package **discusses** but was not produced from — the V5 head, the V5 review, the V6 evidence commit, `origin/main`, the Day-reader guard's base, and the head V6 wrongly claimed — each declared with its reason. The audit's default is refusal, so a SHA not here and not in the range fails | that a declared SHA is used in the right sentence; the declaration says which commit and why, not where |

## Git-derived

| Member | Supports | Does not prove |
| --- | --- | --- |
| `commits.txt` | the ancestry, each commit with its date, subject and file list | — |
| `changed-files.txt` | `--name-status` and `--stat` against the parent, bare | — |
| `changes.patch` | the exact parent→head diff, regenerated at the sealed head | that the diff is correct — only that it is what it is |
| `checks.txt` | every command, its exact invocation, its numeric exit, its log, and the commit it ran at — **composed by `logs/checks.py` from the ledgers the batteries wrote as they ran**, never typed | that a result is acceptable; it records what each command printed and nothing about what it means |
| `logs/checks.py` | how that composition is done, and which line of each log it takes as the headline | — |
| `logs/browser-static-head.log` | the seven browser scripts no test loads, parsed and pinned at the head | anything about behaviour; it is a syntax and digest check |

## The correction, driven at production sinks

| Member | Supports | Does not prove |
| --- | --- | --- |
| `logs/v7-tests-against-parent.log` | the V7 test file replayed against the **parent's** production files — same scenarios, same oracles, other code. Every assertion distinguishing the two heads is here by name, and the class decomposition is derived from it | that a class passing at both ends is worthless; two of them close proof gaps, and `DERIVED-CLAIMS.md` names them rather than rounding them away |
| `logs/focused-catena-head.log`, `logs/focused-catena-parent.log` | the focused Catena suite at each end, verbose | — |

## The wider suites, at both ends

| Member | Supports | Does not prove |
| --- | --- | --- |
| `logs/full-discovery-head.log`, `logs/full-discovery-parent.log` | full discovery at each end; the FAIL/ERROR identity sets are extracted and diffed by `logs/derive-claims.py` in both directions | a count identity. The head runs more tests; what is compared is the identity SET |
| `logs/make-check-head.log`, `logs/make-check-parent.log` | `make -k check` at each end, and that the failing targets are the same ones | that those targets should fail; they are inherited and separately owned |
| `logs/promised-head.log`, `logs/promised-parent.log`, `logs/catena-check-head.log`, `logs/catena-check-parent.log`, `logs/release-bindings-head.log`, `logs/release-bindings-parent.log`, `logs/gzip-sizes-head.log`, `logs/gzip-sizes-parent.log`, `logs/public-site-head.log`, `logs/public-site-parent.log` | the promise ledger, the Catena data check, the read-only release-binding status, the gzip budgets and the site build at each end, one log per command rather than several folded into one | — |
| `logs/browser-gate-head.json`, `logs/browser-gate-parent.json` | the two whole browser-gate reports, from real Chromium over the built site | anything specific to this route; the gate's failures belong to the shared shell |
| `logs/browser-gate-head.log`, `logs/browser-gate-parent.log` | their invocations, exits and counts | — |
| `logs/compare-gate.py`, `logs/gate-comparison.log` | the two reports compared field by field, excluding four volatile keys named in the tool | that four is the right number of exclusions — the tool states them so a reader can judge |
| `logs/order-head.txt`, `logs/order-parent.txt` | the ordering ledger for each battery: every command's start, end and exit, in the order run | that the environment was hermetic. It was sequential and separate, which is a weaker and true claim |

## The sealer

| Member | Supports | Does not prove |
| --- | --- | --- |
| `logs/sanitize-and-seal.py` | the sealer, with `--check-only`'s member deletion removed and every ZIP member now proved against the manifest | reproducible archive construction; ZIP entry timestamps are local mtimes |
| `logs/test-sanitize-and-seal.py`, `logs/sealer-tests.log` | tests over the sealer's own behaviours, and that run | — |
| `logs/seal-check.log` | the sanitization pass in `--check-only`, which writes nothing, **captured with its exit** rather than quoted from memory | — |
| `logs/seal.log` | the FIRST sealing pass's transcript. A transcript of a sealing run cannot be inside the set that run seals — the manifest is written while the run is still writing the log — so the seal runs twice: this is the first pass, and the manifest you hold was written by a second pass over a tree differing only in this file. The second pass normalizes the two or three logs written between the passes, and a THIRD pass over the result makes zero substitutions and rewrites no file — which is the idempotence claim, and it is checkable by running the sealer again | that the second pass is in the package. It is not, by construction; `logs/assemble.sh` is the process, and re-running the sealer reproduces it |
| `logs/assemble.sh` | the whole assembly, derivation, audit and seal as one script, so the package is a function of the head rather than of the order somebody did things in | — |
| `MANIFEST.sha256` | the authoritative member list and the content proof; it survives repacking | transport integrity — that is the ZIP's sidecar |

---

## What is deliberately absent

**Screenshots.** The stylesheet and the markup are byte-identical to the
parent and this correction is semantic. A raster of a valid chapter would be
identical at both ends. `logs/derive-claims.py` counts PNGs and pairs from the
sealed directory anyway and reports zero, because a count derived is a
different kind of claim from an absence described.

**A Chromium probe of this route.** V5 and V6 shipped one; V7 does not,
because what it would capture — a rendered valid chapter — is the thing that
did not change, and what did change is proved by replaying the same oracles
against the parent's code. The gate ran in real Chromium at both ends and its
reports are here.

**A pair audit.** There are no pairs to audit.
