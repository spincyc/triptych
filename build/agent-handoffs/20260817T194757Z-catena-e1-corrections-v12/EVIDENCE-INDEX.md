# Evidence index

What each member of this package is, what it supports, and — the column that
matters — what it does **not** prove. A reviewer who reads only this file
should be able to tell which claims rest on evidence and which rest on a
lane's word.

**No figure appears in this file.** Every count, size, digest and identity is
in `claims.json` and its rendering `DERIVED-CLAIMS.md`. Where a number would
belong here, the member that carries it is named instead.

This file names itself, and it names every member. `MANIFEST.sha256` covers
every member except itself; the archive digest and byte size live in the
sidecar beside the archive, never inside it.

## The argument

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `HANDOFF.md` | staged | The ten required contents of the handoff protocol, as content. | Nothing on its own; every claim in it is carried by a member below. |
| `CLAIM-CLOSURE.md` | staged | The technical argument: the three findings as one defect, the snapshot contract, the cost of the contamination rule, and what proves it. | That the argument is right. It is prose; the vectors are in `changes.patch` and their runs are in the logs. |
| `REVIEW_REQUEST.md` | staged | Six questions, four of them blockers, each naming the acceptance decision it gates. | Nothing. It asks; it does not answer. |
| `PROVENANCE.md` | staged | The attempt state machine, why the terminal row can honestly be written where it is, the one-root-per-attempt rule, and what was discarded. | Its own accuracy — `logs/attempts.json` is the authority, and where the two could disagree the ledger is right and this file is a defect. |
| `LIMITATIONS.md` | staged | The boundaries of what this lane did, stated by the lane that did it. | That the list is complete. A limitation nobody noticed is not in it. |
| `UNRESOLVED-BLOCKERS.md` | staged | Every blocker left open on purpose, with its owner. | That the enumeration is complete; item 11 of its own list says so explicitly. |
| `PRIVACY-AUDIT.md` | staged | What the sanitizer looks for, where it looked, and what a reviewer can run to reproduce it. | That these bytes are clean — that is the seal transcript's claim, not this file's. |

## The derived record

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `claims.json` | declared, pending — P4 | Every identity, count, size and digest, derived mechanically from the repository and the frozen member inventory. | Anything about the archive: the ZIP does not exist when this is written. |
| `DERIVED-CLAIMS.md` | declared, pending — P4 | The same dict, rendered. Byte-reproducible from `claims.json` by the final verification. | Nothing beyond `claims.json`; it is a rendering, not a second source. |
| `checks.txt` | staged | Every command that ran, with its exit, order, start, end, tree state before and after, attempt, and log. | That a command's *result* was correct — only that it ran, and what it exited with. |
| `commits.txt` | staged | The exact commit range from parent to head. | That the range is the whole change; `changed-files.txt` and `changes.patch` carry that. |
| `changed-files.txt` | staged | Every path this range touches, with its status and the diff stat. | Intent. It shows what moved, not why. |
| `changes.patch` | staged | The complete diff, including every regression and every harness hook. | That the regressions are sufficient. The parent replay is what argues that. |
| `MANIFEST.sha256` | declared, pending — P6 | A digest for every member except itself. | The archive's own identity, which is in the sidecar. |
| `EVIDENCE-INDEX.md` | staged | This table. | Anything. It is a map. |

## The runs

Two validation batteries — one at this head, one at the exact reviewed
parent — and the assembly. Each has its own log root, so a failed attempt's
transcripts stay with that attempt and cannot be overwritten by the attempt
that replaces it.

`logs/LOG-INDEX.md` is the mechanically derived index of every log in this
package, with the attempt that owns it. It is the correct entry point, and
it is derived rather than written.

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `logs/attempts.json` | declared, pending — P5 | The attempt ledger: every attempt under this lane's name, discarded ones included, each with its terminal disposition and its one reason. **The authority on which package is authoritative.** | That the archive verified — the archive does not exist when the terminal row is written. `PROVENANCE.md` §2 states exactly what the row claims and what the sidecar and outer log carry instead. |
| `logs/LOG-INDEX.md` | declared, pending — P1 | Every log, its attempt and its role, derived from what is on disk. | That a log's contents are what its name says. |
| `logs/attempt-01/focused-catena-head.log` | staged | The focused Catena suite at this head. | Anything about the parent; its own log is the parent battery's. |
| `logs/attempt-01/catena-check-head.log` | staged | The generator-side structural check at this head. | Anything about the browser surface. |
| `logs/attempt-01/promised-head.log` | staged | The promise ledger validates at this head. | That a promise is *met* — only that the ledger is internally valid. |
| `logs/attempt-01/full-discovery-head.log` | staged | The whole suite at this head, including the inherited failures. | That a failure is inherited. Only the parent battery beside it can say that. |
| `logs/attempt-01/make-check-head.log` | staged | `make -k check` at this head, and which targets are red. | Which of them this lane caused. The parent battery answers that. |
| `logs/attempt-01/release-bindings-head.log` | staged | The stale release bindings, fail-closed and unsigned. | That they are this lane's to fix. They are not, and none was re-signed. |
| `logs/attempt-01/public-site-head.log` | staged | The built artifact the browser gate runs over. | That the artifact is publishable; `public-alpha verify` is a separate gate and was not run. |
| `logs/attempt-01/browser-gate-head.log` | staged | That the gate ran. The report itself is the JSON beside it. | The gate's findings — those are in the JSON. |
| `logs/attempt-01/browser-gate-head.json` | staged | The full real-Chromium gate report at this head. | That headless Chromium is a device or an assistive technology. It is neither. |
| `logs/attempt-01/browser-static-head.log` | staged | The static browser-surface assertions at this head. | Runtime behaviour. |
| `logs/attempt-01/gzip-sizes-head.log` | staged | The measured payloads against their ceilings. | That the unbudgeted model's growth is acceptable; that question is open and re-asked. |
| `logs/attempt-01/request-journals-head.log` | staged | The packaged request-ownership journals: sequence, address, kind, owning step, outcome. | Anything a journal does not record. |
| `logs/attempt-02/focused-catena-parent.log`, and the rest of that root | staged | The same battery at the exact reviewed parent, so a failure set can be compared rather than an exit code. Its whole contents are listed in `logs/LOG-INDEX.md`. | — |
| `logs/attempt-02/head-tests-against-parent.log` | staged | **The non-vacuity proof of the whole lane**: this head's test file replayed against the uncorrected parent, failing where the correction is absent. | That the corrections are complete — only that they are not vacuous. |
| `logs/v11-authority-reproduction.txt` | staged | The coherence gate run against the **sealed V11 package**, refusing it and naming the review's own finding without being told what it was. | That this package is coherent; the gate's run against *this* package is the sibling .authority-coherence.log. |

## The pipeline, shipped as members

The tools that assembled this package, and the ones that gate it, are
shipped so a reviewer can read what produced the evidence rather than take
its word. They are read as bytes by the final verification and are never
executed from inside the archive.

`logs/assemble.sh`, `logs/battery.sh`, `logs/checks.py`,
`logs/derive-claims.py`, `logs/head-consistency.py`,
`logs/sanitize-and-seal.py`, `logs/test-sanitize-and-seal.py`,
`logs/verify-final-package.py`, `logs/handoff-inventory.py`,
`logs/compare-gate.py`, `logs/gzip-sizes.py`, `logs/journal-dump.py`,
`logs/gate-summary.py`,
`logs/authority-coherence.py`, `logs/test-authority-coherence.py`.

The two test suites among them are the ones that prove a refusal fires:
`logs/test-sanitize-and-seal.py` for the sealer and the log-and-attempt
protocol, `logs/test-authority-coherence.py` for the authority gate. A gate
that has only ever been run against a package that passes is a gate nobody
has seen refuse.

## The pictures

| Member | State | Supports | Does not prove |
| --- | --- | --- | --- |
| `screenshots/INDEX.md` | staged | What each image is, and what visibly differs in each pair. | — |
| `screenshots/capture-metadata.json` | staged | Per image: its digest, its route, its viewport, the checkout it was taken from, and **the sentence read back out of the DOM before the shutter**. | That the fixture corpus resembles the tracked corpus. It does not, deliberately. |
| the twelve PNGs | staged | Three inputs, at two viewports, before and after — the parent serving a body it should not, and the head refusing. | Anything about the tracked corpus, about a real device, or about assistive technology. |

## The siblings, which are not members

They live beside this directory because four of them cannot exist until
after the manifest is taken, and the fifth is the manifest's own subject:
20260817T194757Z-catena-e1-corrections-v12.zip, its digest-and-size sidecar
20260817T194757Z-catena-e1-corrections-v12.zip.sha256, the outer invocation log
20260817T194757Z-catena-e1-corrections-v12.assemble.log, the final verification transcript
20260817T194757Z-catena-e1-corrections-v12.verify-final.log, and the authority gate's transcript
20260817T194757Z-catena-e1-corrections-v12.authority-coherence.log.
