# Evidence index — every artifact, what it supports, what it does not

Every member of this package is named below, and so is every artifact that
ships beside it. **This file, `EVIDENCE-INDEX.md`, is itself a member and is
named in its own list**; the V10 package asserted that every member was
named below while omitting itself, the archive, the archive's sidecar and
the post-seal transcript, and that omission is the reason this sentence
exists.

`logs/head-consistency.py` refuses a package containing a member that
nothing references, so this list being complete is checked rather than
promised; its transcript is `logs/head-consistency.log`.

**No figure appears in this file.** Every count, size, digest and identity
is in `claims.json` and its rendering `DERIVED-CLAIMS.md`, both written in
one pass from the frozen member inventory by `logs/derive-claims.py`.

## How to read the STATE column

- **staged** — the member's bytes existed before assembly began and were
  copied into the package at P1.
- **declared, pending** — the member does **not** exist while these
  documents are being written. A named phase of `logs/assemble.sh` writes
  it. It is named here as a declaration, and the phase that writes it is
  stated. The V10 package carried index rows for logs that did not yet
  exist without saying so; these rows say so.

---

## The core four the protocol requires

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `HANDOFF.md` | staged | the factual entry point, containing all ten of the protocol's required contents as content: (1) task and intended outcome, (2) branch, (3) head SHA and base commit, (4) whether the reviewed state has uncommitted changes, (5) focused files changed, (6) exact startup commands with route state, (7) implementation summary, (8) known limitations stated inline, (9) unresolved decisions stated inline, and (10) the artifact inventory with the reason for every omitted conditional class. That is ten items, counted | that any of the ten is well judged; it states them, and the members below carry the evidence |
| `REVIEW_REQUEST.md` | staged | the judgements this lane could not make for itself, as `Blockers` and `Optional feedback`, each blocker naming the acceptance decision it gates | it asserts nothing; it is questions only |
| `changes.patch` | declared, pending — P1 git-derived | the exact parent-to-head diff, regenerated at the sealed head | that the diff is correct — only that it is what it is |
| `checks.txt` | declared, pending — P1, composed by `logs/checks.py` from the two ordering ledgers | every command of both batteries with its exact invocation, numeric exit, ledger timestamps, unique log, and the per-command tree readings | that any result is acceptable |

## The argument

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `EVIDENCE-INDEX.md` | staged | this list: every member and every sibling, each with its state, what it supports, and what it does not | anything about the work; it is a map |
| `CLAIM-CLOSURE.md` | staged | the three-state sentence contract, the own-data descriptor reading, why a partly-inherited contract fails closed and what that costs, the boundary the correction does not reach, and the vectors that pin it | that the conservative sentence is truthful enough, or that fail-closed is right — `REVIEW_REQUEST.md` asks both |
| `PROVENANCE.md` | staged | where each battery ran, that provenance is emitted as the runs happen and read per command, how log identity is allocated from the attempt ledger, and what was discarded | that the environment was hermetic; nothing in this package claims that |
| `LIMITATIONS.md` | staged | twelve limitations at full strength, including the byte-identical screenshot pairs, the three capture classes not produced, the unversioned pipeline, and the harness-seam request sink | — |
| `UNRESOLVED-BLOCKERS.md` | staged | every finding left open, each with the lane or role that owns it, and one item stated plainly as unenumerated | that any of them is small |
| `PRIVACY-AUDIT.md` | staged | the sanitization method, what V11 changed in it, the verified reviewer invocations, and which claims become true only at the seal | that no private token exists that no pattern can recognise |

## The derived record

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `claims.json` | declared, pending — P4, derived once from the P3 freeze | the source for every figure: identity, ancestry, commits, diffstat, gzip payload at both ends, suite counts and identity sets, gate totals, the frozen package inventory with its named derived members, and the byte scan | a judgement; it records what is |
| `DERIVED-CLAIMS.md` | declared, pending — P4 | the same values rendered in the same pass, under accurate V11 lane labels | — |
| `MANIFEST.sha256` | declared, pending — P6, written once after the last member write | the authoritative member list and content proof | transport integrity — that is the archive's sidecar, which also records the archive's byte size |
| `commits.txt` | declared, pending — P1 | the ancestry: each commit of the range with its date and subject | — |
| `changed-files.txt` | declared, pending — P1 | `--name-status` and `--stat` against the parent | — |

## The screenshots

`screenshots/INDEX.md` is the capture lane's own record — the sentence
table, the two capture classes, the per-pair pixel results and the bounds.
`screenshots/capture-metadata.json` records, per image, the browser, the
viewport, the emulation, the checkout, and the rendered text read back out
of the DOM before the shutter; a mismatch against the expected sentence
aborted the capture without writing an image.

Every head-side image was captured at
`3b93f74f032e74de9a50c1e2f1b35aa5b567f8d8`, the first of this lane's two
commits, and the metadata says so. The exact head is one commit later and
differs only in durable records; the four Catena files a browser loads are
byte-identical between the two, which is why these captures bind to the
head. See `LIMITATIONS.md` §8.

**The adversarial before/after pairs — eight pairs, six byte-identical.**
Six of the eight PNG pairs are the same bytes before and after, by design:
the absent, present-valid and refused states render exactly as the parent
rendered them. Two pairs differ, both of them the unestablished state. No
claim is made here about any image that was not captured.

| Member | State | Pair result |
| --- | --- | --- |
| `screenshots/before--catena--fragment-absent--1440x900.png`, `screenshots/after--catena--fragment-absent--1440x900.png` | staged | byte-identical; 0 of 1,296,000 pixels differ |
| `screenshots/before--catena--fragment-absent--393x852.png`, `screenshots/after--catena--fragment-absent--393x852.png` | staged | byte-identical; 0 of 334,836 pixels differ |
| `screenshots/before--catena--fragment-present-valid--1440x900.png`, `screenshots/after--catena--fragment-present-valid--1440x900.png` | staged | byte-identical; 0 of 1,296,000 pixels differ |
| `screenshots/before--catena--fragment-present-valid--393x852.png`, `screenshots/after--catena--fragment-present-valid--393x852.png` | staged | byte-identical; 0 of 334,836 pixels differ |
| `screenshots/before--catena--fragment-refused--1440x900.png`, `screenshots/after--catena--fragment-refused--1440x900.png` | staged | byte-identical; 0 of 1,296,000 pixels differ — the control for the correction |
| `screenshots/before--catena--fragment-refused--393x852.png`, `screenshots/after--catena--fragment-refused--393x852.png` | staged | byte-identical; 0 of 334,836 pixels differ — the control for the correction |
| `screenshots/before--catena--fragment-unestablished--1440x900.png`, `screenshots/after--catena--fragment-unestablished--1440x900.png` | staged | **differ**; 11,392 of 1,296,000 pixels, in x 830-1436, y 121-899. This is the correction |
| `screenshots/before--catena--fragment-unestablished--393x852.png`, `screenshots/after--catena--fragment-unestablished--393x852.png` | staged | **differ**; 13,639 of 334,836 pixels, in x 16-376, y 686-851. This is the correction |

**The real-corpus captures.** Every tracked fragment is present-valid, so no
no-text sentence can appear in any of these. They are shell, layout and
accessibility-derivative evidence, and evidence that the correction
disturbed none of it.

| Member | State | Surface and emulation |
| --- | --- | --- |
| `screenshots/catena-index--desktop-1440x900--1440x900.png` | staged | the changed route, desktop |
| `screenshots/catena-index--laptop-1024x768--1024x768.png` | staged | the changed route, laptop |
| `screenshots/catena-index--tablet-768x1024--768x1024.png` | staged | the changed route, tablet |
| `screenshots/catena-index--handset-393x852--393x852.png` | staged | the changed route, handset |
| `screenshots/catena-index--narrow-320x852--320x852.png` | staged | the changed route, narrow |
| `screenshots/catena-index--handset-393x852-forced-colors--393x852.png` | staged | the changed route under forced colors |
| `screenshots/catena-index--handset-393x852-reduced-motion--393x852.png` | staged | the changed route under reduced motion |
| `screenshots/catena-index--handset-393x852-scale-400--393x852.png` | staged | the changed route at 400% page scale |
| `screenshots/catena-index--handset-393x852-text-200--393x852.png` | staged | the changed route at 200% text |
| `screenshots/index--desktop-1440x900--1440x900.png` | staged | Home shell, untouched by this correction |
| `screenshots/index--handset-393x852--393x852.png` | staged | Home shell, untouched |
| `screenshots/index--narrow-320x852--320x852.png` | staged | Home shell, untouched |
| `screenshots/liturgy-day-reader--desktop-1440x900--1440x900.png` | staged | Reader shell, untouched |
| `screenshots/sources-index--desktop-1440x900--1440x900.png` | staged | Source Library shell, untouched |
| `screenshots/texts-index--desktop-1440x900--1440x900.png` | staged | Publications catalogue shell, untouched |
| `screenshots/INDEX.md` | staged | the capture lane's own record, including its stated bounds |
| `screenshots/capture-metadata.json` | staged | per-image browser, viewport, emulation, checkout and the DOM text read back before the shutter |

Not produced: print, no-JavaScript and keyboard-focus captures. The first
two have stated reasons; the third does not. `LIMITATIONS.md` §7 carries all
three.

## The logs tree

`logs/LOG-INDEX.md` is the **derived** roster of this directory: written by
`logs/checks.py` in the same pass that composes `checks.txt`, from the two
battery ordering ledgers and from the directory itself, never typed. It
names every log the package ships with the attempt that produced it, its
slug, its numeric exit and its per-row tree readings, and it names the
transcripts that are written after it as declarations. Take every exact log
filename from it.

A log filename is `<attempt ordinal>-<slug>-<side>.log`. The ordinal names
the ATTEMPT and is allocated from the append-only ledger outside the
package, so a rerun cannot reuse a filename; within one attempt a log is
keyed by its SLUG, so a step means the same thing on both sides. The two
sides carry different ordinals because they are two attempts. This is the
V11 correction to the V10 scheme, under which the same number meant a
different step on each side.

| Member group | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `logs/order-head.txt`, `logs/order-parent.txt` | staged | each battery's ordering ledger: preflight `sha`/`porcelain`/`cwd`, then every command with its unique log, its `TREE-BEFORE:` and `TREE-AFTER:` readings, start, end and exit, in the order run, and the postflight drift check | that the environment was hermetic |
| `logs/LOG-INDEX.md` | declared, pending — P1 | the mechanical join from every shipped log to its attempt, slug, exit and tree readings | — |
| `logs/attempts.json` | declared, pending — P1, copied before the P3 freeze | the attempt-ledger rows this package was built from, each attempt with its terminal disposition — authoritative or discarded — and its one reason | that no attempt outside this package's set ever existed; the ledger beside the package is longer |
| `logs/browser-gate-head.json`, `logs/browser-gate-parent.json` | staged | the two whole gate reports, real Chromium over the built site, each shipped once as the one artifact of its run | anything specific to this route; the failures belong to the shared shell |
| `logs/gate-comparison.log` | declared, pending — P1, a recorded pipeline step with its own exit | the two gate reports compared object for object under the named volatile exclusions | that a difference would be a failure; a difference is a finding |
| `logs/named-commits.json` | staged | the commits this package discusses but was not produced from, each declared with its reason; the audit's default is refusal | that a declared SHA is used in the right sentence |
| `logs/sealer-tests.log` | declared, pending — P1 | the sealer's own suite, run before anything is normalized | — |
| `logs/seal.log`, `logs/seal-check.log` | declared, pending — P2 | every normalization pass under its header to the fixpoint, and the `--check-only` pass whose byte identity with its in-tree copy is the fixpoint proof | that no private token exists that no pattern can recognise |
| `logs/derive-claims.log` | declared, pending — P4 | the derivation's transcript | — |
| `logs/head-consistency.log` | declared, pending — P5 | that no member names a commit this package may not name, that no frozen row drifted, that the residue is exactly the declared derived members, and that no member goes unreferenced | that a correct SHA is used in the right sentence |
| the pipeline sources under `logs/` | staged | how every one of the above was produced: the battery, the checks composer, the claim derivation, the consistency audit, the gate comparison, the journal dump, the gzip measurement, the sealer and its own tests, the assembler, the post-seal verifier, and the handoff-inventory tool | — |

`logs/LOG-INDEX.md` is the complete, derived enumeration of this directory;
the table above groups it by role and does not replace it.

### The battery logs, by name

These names are read from the two ordering ledgers, which are what
`logs/LOG-INDEX.md` is derived from. Nothing here is a guess and nothing is
carried over from V10, whose numbering scheme no longer exists. The exit
status of each is in `checks.txt`, not here.

| Slug — what the step is | Head battery, attempt ordinal 01 | Parent battery, attempt ordinal 02 |
| --- | --- | --- |
| focused-catena — the focused Catena suite, verbose | `logs/01-focused-catena-head.log` | `logs/02-focused-catena-parent.log` |
| catena-check — the Catena data check over the real corpus | `logs/01-catena-check-head.log` | `logs/02-catena-check-parent.log` |
| promised — the promise ledger | `logs/01-promised-head.log` | `logs/02-promised-parent.log` |
| full-discovery — the whole discovered suite, isolated | `logs/01-full-discovery-head.log` | `logs/02-full-discovery-parent.log` |
| make-check — `make -k check`, all targets | `logs/01-make-check-head.log` | `logs/02-make-check-parent.log` |
| release-bindings — the read-only release-binding status | `logs/01-release-bindings-head.log` | `logs/02-release-bindings-parent.log` |
| public-site — the site build the gate then drives | `logs/01-public-site-head.log` | `logs/02-public-site-parent.log` |
| browser-gate — the gate invocation; its report is the JSON beside it | `logs/01-browser-gate-head.log` | `logs/02-browser-gate-parent.log` |
| browser-static — the browser scripts no test loads, parsed and pinned | `logs/01-browser-static-head.log` | not run on the parent side |
| gzip-sizes — the budget measurement, identical in method to the suite's | `logs/01-gzip-sizes-head.log` | `logs/02-gzip-sizes-parent.log` |
| head-tests-against-parent — the head's whole test file over the parent's production files; the step whose recorded command dirties the tree | not run on the head side | `logs/02-head-tests-against-parent.log` |
| request-journals — the per-scenario owned journals and terminal sinks, printed by `logs/journal-dump.py` | `logs/01-request-journals-head.log` | `logs/02-request-journals-parent.log` |

The parent side runs two steps the head side does not, and the head side
runs one the parent side does not; that is why the two columns are not the
same length. `PROVENANCE.md` states which of these rows ran against a dirty
tree and why.

## Beside the package, not inside it

Four artifacts ship as siblings of the package directory. Each is named for
the package's own UTC stamp and slug; `STAMP` below stands for the UTC
timestamp the assembly allocates, because the assembly is what fixes it.

| Sibling | State | Supports | Does not prove |
| --- | --- | --- | --- |
| 20260816T172114Z-catena-e1-corrections-v11.zip | declared, pending — P7 | the transport copy of the complete package directory, single top-level root, sorted paths, fixed-epoch entry timestamps and suffix-derived modes | that it is a second hand-authored record; it is a copy of the directory |
| 20260816T172114Z-catena-e1-corrections-v11.zip.sha256 | declared, pending — P7 | the archive's SHA-256 and its exact byte size | anything about the members; that is `MANIFEST.sha256` |
| 20260816T172114Z-catena-e1-corrections-v11.verify-final.log | declared, pending — P8 | the read-only post-seal verification from the final archive alone: the binding header, the out-of-archive trust anchor with per-tool trusted and shipped digests, sidecar, layout, manifest, every claimed row against the delivered bytes, the derived final-byte totals, the re-rendered claims prose, the replayed audits, and the pre-check/post-check archive rehash with an explicit equality verdict | that the claims are wise; only that they are true of the bytes. It ships beside the archive because the verification of the final bytes cannot be among them |
| 20260816T172114Z-catena-e1-corrections-v11.assemble.log | declared, pending — written throughout, outside the package | the outer assembly invocation: every phase, its exit, and the attempt it belongs to, written while the package is still being built | — |

The append-only attempt ledger at
`build/agent-handoffs/attempt-ledger.jsonl` lives outside the package and
outside this inventory; it spans every attempt ever made, and the rows this
package was built from are copied into `logs/attempts.json` before the
freeze.

## Conditional artifact classes

- **`screenshots/`** — present. The correction changes browser-visible copy,
  so before and after images are required and are here, with the byte-level
  result of every pair stated above.
- **`logs/`** — present.
- **A sources record** — omitted, and the reason is that this lane consumed
  no external source: every input is this repository's own review records,
  code, tests and durable records, so there is nothing whose locus, date or
  rights a reviewer would need to evaluate.

## What is deliberately absent, and what was discarded

- **A print, a no-JavaScript and a keyboard-focus capture.** The first two
  have reasons; the third does not. `LIMITATIONS.md` §7.
- **Real-device and assistive-technology evidence.** Headless Chromium is
  neither. Separately owned; `UNRESOLVED-BLOCKERS.md`.
- **A second post-seal verification transcript.** One is shipped, so this
  package claims only what one transcript backs.
- **The earlier sealed packages.** Named, untouched, on their evidence
  branches, each as its review left it.
- **Discarded runs.** This package does not claim that nothing was
  discarded. `logs/attempts.json` is the enumerated authority: it gives
  every attempt this package was built from a terminal disposition and one
  reason. `PROVENANCE.md` states the two discards that are known without it
  — a raced full-discovery measurement, and the informal pre-battery runs —
  and neither is used for any figure here.
