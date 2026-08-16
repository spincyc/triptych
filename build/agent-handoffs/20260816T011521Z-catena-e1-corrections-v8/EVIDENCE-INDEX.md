# Evidence index — every artifact, what it supports, what it does not

Every member of this package is named below. `logs/head-consistency.py`
refuses a package containing a member nothing references, so this list being
complete is checked rather than promised — its transcript is
`logs/head-consistency.log`.

**No figure appears in this file.** Every count, size, digest and identity is
in `claims.json` and its rendering `DERIVED-CLAIMS.md`, both written in one
pass by `logs/derive-claims.py` at seal time.

---

## The argument

| Member | Supports | Does not prove |
| --- | --- | --- |
| `HANDOFF.md` | the task, the lineage in words, and how to verify | nothing on its own; every claim in it points at an artifact |
| `NAMESPACE-CLOSURE.md` | the exact namespace contract, the two validators, and the evidence — valid corpus kept apart from adversarial fixtures | that the boundary is drawn at the right altitude — `REVIEW_REQUEST.md` §1–2 ask |
| `REVIEW_REQUEST.md` | the decisions this lane could not make for itself | it asserts nothing; it is questions only |
| `UNRESOLVED-BLOCKERS.md` | every V7 finding left open, in the review's numbering, each with its owner | that any of them is small |
| `LIMITATIONS.md` | what this package does not prove | — |
| `PRIVACY-AUDIT.md` | the sanitization method and its captured transcripts | that no private token exists that no pattern can recognise |

## The derived record

| Member | Supports | Does not prove |
| --- | --- | --- |
| `claims.json` | **the source for every figure**: identity, ancestry, commits, diffstat, gzip payload at both ends, suite counts and identity sets, gate totals, the test delta, the package inventory and the byte scan | a judgement; it records what is |
| `DERIVED-CLAIMS.md` | the same values, rendered in the same pass | — |
| `logs/derive-claims.py` | how each is computed from the head, the parent and the package alone | — |
| `logs/derive-claims.log` | that derivation's transcript | — |
| `logs/head-consistency.py` | that no member names a commit this package may not name, calls the head a parent, names a missing path, or goes unreferenced | that a correct SHA is used in the right sentence |
| `logs/head-consistency.log` | that audit's run | — |
| `logs/named-commits.json` | the commits this package **discusses** but was not produced from, each declared with its reason; the audit's default is refusal | that a declared SHA is used in the right sentence |

## Git-derived

| Member | Supports | Does not prove |
| --- | --- | --- |
| `commits.txt` | the ancestry, each commit with its date and subject | — |
| `changed-files.txt` | `--name-status` and `--stat` against the parent | — |
| `changes.patch` | the exact parent→head diff, regenerated at the sealed head | that the diff is correct — only that it is what it is |
| `checks.txt` | every command, invocation, exit, ledger timestamps and log — composed by `logs/checks.py` from the two ordering ledgers, never typed | that a result is acceptable |
| `logs/checks.py` | how that composition is done | — |

## The closure, driven at the request sink

| Member | Supports | Does not prove |
| --- | --- | --- |
| `logs/journal-dump.py` | how the request journals are captured: the replay harness run exactly as the suite runs it, journals and terminal sinks printed per scenario | — |
| `logs/request-journals-head.log` | the fetched journals at the head: zero wrong-namespace requests, zero same-stem fallbacks, the preserved valid request, and the terminal state of each rejected path | — |
| `logs/request-journals-parent.log` | the same scenarios at the parent: the wrong-namespace requests actually made — the defect demonstrated | that the production corpus emits hostile paths; the fixtures are adversarial and labelled |
| `logs/v8-tests-against-parent.log` | the head's test file against the parent's production files; the distinguishing classes by name, decomposed in `DERIVED-CLAIMS.md` | that a class passing at both ends is worthless |
| `logs/focused-catena-head.log`, `logs/focused-catena-parent.log` | the focused Catena suite at each end, verbose | — |

## The wider suites, at both ends

| Member | Supports | Does not prove |
| --- | --- | --- |
| `logs/full-discovery-head.log`, `logs/full-discovery-parent.log` | full discovery at each end; the FAIL/ERROR identity sets are extracted and diffed by `logs/derive-claims.py` | a count identity; the head runs more tests and the identity SET is what is compared |
| `logs/make-check-head.log`, `logs/make-check-parent.log` | `make -k check` at each end, same inherited failing targets | that those targets should fail; they are separately owned |
| `logs/promised-head.log`, `logs/promised-parent.log`, `logs/catena-check-head.log`, `logs/catena-check-parent.log`, `logs/release-bindings-head.log`, `logs/release-bindings-parent.log`, `logs/gzip-sizes-head.log`, `logs/gzip-sizes-parent.log`, `logs/public-site-head.log`, `logs/public-site-parent.log` | the promise ledger, the Catena data check, the read-only release-binding status, the gzip budgets and the site build at each end | — |
| `logs/gzip-sizes.py` | the budget measurement, identical in method to the suite's own | — |
| `logs/browser-gate-head.json`, `logs/browser-gate-parent.json` | the two whole browser-gate reports, real Chromium over the built site | anything specific to this route; the failures belong to the shared shell |
| `logs/browser-gate-head.log`, `logs/browser-gate-parent.log` | their invocations and exits | — |
| `logs/compare-gate.py`, `logs/gate-comparison.log` | the two gate reports compared field by field, excluding the volatile keys the tool names | — |
| `logs/browser-static-head.log` | the browser scripts no test loads, parsed and pinned at the head | behaviour; it is a syntax and digest check |
| `logs/order-head.txt`, `logs/order-parent.txt` | the ordering ledger for each battery: every command, start, end and exit, in the order run | that the environment was hermetic |
| `logs/battery.sh` | the one script that ran each battery and wrote its ledger as it ran | — |

## The sealer

| Member | Supports | Does not prove |
| --- | --- | --- |
| `logs/sanitize-and-seal.py` | the corrected V7 sealer, reused unchanged | reproducible archive construction; ZIP entry timestamps are local mtimes |
| `logs/test-sanitize-and-seal.py`, `logs/sealer-tests.log` | the sealer's own tests, and that run | — |
| `logs/seal-check.log` | the `--check-only` pass, captured with its exit | — |
| `logs/seal.log` | the first sealing pass's transcript; the manifest you hold was written by a second pass over a tree differing only in the logs written between the passes, and a third pass makes no change — checkable by running the sealer again | that the second pass is in the package; `logs/assemble.sh` is the process |
| `logs/assemble.sh` | the whole assembly, derivation, audit and seal as one script | — |
| `MANIFEST.sha256` | the authoritative member list and content proof | transport integrity — that is the ZIP's sidecar |

---

## What is deliberately absent

**Screenshots and a route-specific Chromium probe** — `LIMITATIONS.md` §3.
**A pair audit** — there are no pairs to audit. **A supersession** — this
package supersedes nothing and no earlier package of this lane exists; the
two V7 packages it names belong to the parent's lane and are untouched.
