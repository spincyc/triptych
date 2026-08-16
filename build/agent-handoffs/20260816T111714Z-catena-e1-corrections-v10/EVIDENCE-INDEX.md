# Evidence index — every artifact, what it supports, what it does not

Every member of this package is named below. `logs/head-consistency.py`
refuses a package containing a member nothing references, so this list being
complete is checked rather than promised — its transcript is
`logs/head-consistency.log`.

**No figure appears in this file.** Every count, size, digest and identity
is in `claims.json` and its rendering `DERIVED-CLAIMS.md`, both written in
one pass from the frozen member inventory by `logs/derive-claims.py`.

---

## The argument

| Member | Supports | Does not prove |
| --- | --- | --- |
| `HANDOFF.md` | the task, the ten protocol items — branch, head and base, uncommitted-state, focused files, startup and route state, summary, limitations, decisions, inventory — and how to verify | nothing on its own; every claim in it points at an artifact |
| `PRESENTATION-CLOSURE.md` | the two-sentence contract — absence against refusal — the three edits that enforce it, the closed claim boundary, and the four terminal vectors pinned to expected values | that the refused sentence is truthful enough — `REVIEW_REQUEST.md` §1 asks |
| `PROVENANCE.md` | which battery runs are authoritative, where each ran, that provenance was emitted by the batteries as they ran, and that nothing was discarded | that the environment was hermetic |
| `REVIEW_REQUEST.md` | the decisions this lane could not make for itself, as Blockers and Optional feedback | it asserts nothing; it is questions only |
| `UNRESOLVED-BLOCKERS.md` | every finding left open, in the V7 review's numbering as the V8 and V9 reviews reconfirmed it, each with its owner | that any of them is small |
| `LIMITATIONS.md` | what this package does not prove | — |
| `PRIVACY-AUDIT.md` | the sanitization method, the ledger-born `cwd=$REPO` tokens, and the captured transcripts | that no private token exists that no pattern can recognise |

## The derived record

| Member | Supports | Does not prove |
| --- | --- | --- |
| `claims.json` | **the source for every figure**: identity, ancestry, commits, diffstat, gzip payload at both ends, suite counts and identity sets, gate totals, the un-collapsed parent decomposition, the frozen package inventory with its named derived members, and the byte scan | a judgement; it records what is |
| `DERIVED-CLAIMS.md` | the same values, rendered in the same pass under accurate V10 lane labels | — |
| `logs/derive-claims.py` | how each is computed from the head, the parent and the frozen inventory alone — the lane parameterization, the decomposition reported as methods run, controls passing, and failing subtest identities, and why derived members are named, never sized or hashed | — |
| `logs/derive-claims.log` | that derivation's transcript; a named derived member, so its bytes are claimed nowhere | — |
| `logs/head-consistency.py` | that no member names a commit this package may not name, that no frozen row drifted, that the residue is exactly the declared derived members, and that no member goes unreferenced | that a correct SHA is used in the right sentence |
| `logs/head-consistency.log` | that audit's run; a named derived member | — |
| `logs/named-commits.json` | the commits this package **discusses** but was not produced from, each declared with its reason; the audit's default is refusal | that a declared SHA is used in the right sentence |

## Git-derived

| Member | Supports | Does not prove |
| --- | --- | --- |
| `commits.txt` | the ancestry, each commit with its date and subject | — |
| `changed-files.txt` | `--name-status` and `--stat` against the parent | — |
| `changes.patch` | the exact parent→head diff, regenerated at the sealed head | that the diff is correct — only that it is what it is |
| `checks.txt` | every command, invocation, exit, ledger timestamps, unique log, and each battery's own `sha`/`clean`/`cwd` preflight — composed by `logs/checks.py` from the two ordering ledgers, never typed | that a result is acceptable |
| `logs/checks.py` | how that composition is done, provenance fields included | — |

## The closure, driven at the request sink

| Member | Supports | Does not prove |
| --- | --- | --- |
| `logs/journal-dump.py` | how the request journals are captured: the replay harness run exactly as the suite runs it, journals and terminal sinks printed per scenario | — |
| `logs/11-request-journals-head.log` | the journals at the head: zero requests after a refused prefix, no cached substitution, no late injection, the preserved absence and valid-prefix requests, and the refused sentence standing at each refused terminal | — |
| `logs/11-request-journals-parent.log` | the same scenarios at the parent: the false absence sentence standing over the refused rows — the presentation defect demonstrated | that the production corpus emits hostile prefixes; the fixtures are adversarial and labelled |
| `logs/10-head-tests-against-parent.log` | the head's test file — the upgraded V8/V9 vectors and the new V10 presentation methods alike — against the parent's production files; the distinguishing methods by name, decomposed un-collapsed in `DERIVED-CLAIMS.md` | that a method passing at both ends is worthless |
| `logs/01-focused-catena-head.log`, `logs/01-focused-catena-parent.log` | the focused Catena suite at each end, verbose | — |

## The wider suites, at both ends

| Member | Supports | Does not prove |
| --- | --- | --- |
| `logs/04-full-discovery-head.log`, `logs/04-full-discovery-parent.log` | full discovery at each end; the FAIL/ERROR identity sets are extracted and diffed by `logs/derive-claims.py` | a count identity; the head runs more tests and the identity SET is what is compared |
| `logs/05-make-check-head.log`, `logs/05-make-check-parent.log` | `make -k check` at each end — the inherited failing targets, plus the record-staleness target the head's own durable-record edit makes red | that those targets should fail; they are separately owned |
| `logs/03-promised-head.log`, `logs/03-promised-parent.log`, `logs/02-catena-check-head.log`, `logs/02-catena-check-parent.log`, `logs/06-release-bindings-head.log`, `logs/06-release-bindings-parent.log`, `logs/10-gzip-sizes-head.log`, `logs/09-gzip-sizes-parent.log`, `logs/07-public-site-head.log`, `logs/07-public-site-parent.log` | the promise ledger, the Catena data check, the read-only release-binding status, the gzip budgets and the site build at each end | — |
| `logs/gzip-sizes.py` | the budget measurement, identical in method to the suite's own | — |
| `logs/browser-gate-head.json`, `logs/browser-gate-parent.json` | the two whole browser-gate reports, real Chromium over the built site — each shipped once, as the one artifact of its run | anything specific to this route; the failures belong to the shared shell |
| `logs/08-browser-gate-head.log`, `logs/08-browser-gate-parent.log` | the gate invocations' short transcripts, each naming the JSON report its recorded command wrote | — |
| `logs/compare-gate.py`, `logs/gate-comparison.log` | the two gate reports compared field by field, identical under the named volatile exclusions the tool prints | — |
| `logs/09-browser-static-head.log` | the browser scripts no test loads, parsed and pinned at the head | behaviour; it is a syntax and digest check |
| `logs/order-head.txt`, `logs/order-parent.txt` | the ordering ledger for each battery: preflight `sha`/`porcelain`/`cwd`, every command with its unique log, start, end and exit in the order run, and the postflight drift check | that the environment was hermetic — `PROVENANCE.md` states where each ran |
| `logs/battery.sh` | the one script that ran each battery and wrote its ledger, provenance included, as it ran | — |

## The sealer

| Member | Supports | Does not prove |
| --- | --- | --- |
| `logs/sanitize-and-seal.py` | the corrected sealer: normalization to fixpoint, the scan, the index check, and the freeze-respecting manifest pass that refuses drift | reproducible archive construction; ZIP entry timestamps are local mtimes |
| `logs/test-sanitize-and-seal.py`, `logs/sealer-tests.log` | the pipeline's own tests — sealer, verifier binding and duplicate-row checks, battery ledger and refusal behaviour — and that run | — |
| `logs/seal.log` | every normalization pass, each under its header, to the fixpoint | — |
| `logs/seal-check.log` | the `--check-only` pass whose transcript is byte-identical to this member — the fixpoint proof — captured with its exit | — |
| `logs/assemble.sh` | the whole assembly — refusal preflight, evidence, fixpoint, freeze, single derivation, audit, manifest, archive, sidecar, verification — as one script whose header states the order's reasons | — |
| `logs/verify-final-package.py` | the read-only post-seal verification, opened by a header binding it to the exact ZIP basename, byte size and SHA-256: sidecar, layout, manifest with duplicate-row checks, every claimed row against the delivered bytes, the partition with derived final-byte totals, the re-rendered claims prose, and the replayed audits — from the final ZIP alone | that the claims are wise; only that they are true of the bytes |
| `MANIFEST.sha256` | the authoritative member list and content proof, written once after the last member write | transport integrity — that is the ZIP's sidecar, which also records the archive's byte size |

---

## What is deliberately absent

**Screenshots and a route-specific Chromium probe** — `LIMITATIONS.md` §3
and the `HANDOFF.md` inventory. **A sources record** — no external source
was consumed; every input is the repository's own records, so the
conditional source-listing class is omitted. **A pair audit** —
there are no pairs to audit. **A discarded-run ledger** — nothing was
discarded (`PROVENANCE.md`). **The sealed V7–V9 packages** — named,
untouched, on the evidence branch, each as its review left it. **The P8
transcript** — the verification of the final bytes cannot be among the
final bytes; its transcript is archived beside the ZIP on the evidence
branch, bound to the ZIP's exact name, size and digest.
