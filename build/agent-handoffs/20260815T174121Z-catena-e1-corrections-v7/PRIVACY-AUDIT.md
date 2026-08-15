# Sanitization, and the sealer's own two defects

## The method

`logs/sanitize-and-seal.py` runs one pipeline over the package:

    self-check -> clear manifest -> normalize -> scan -> index-check
               -> screenshot-pair audit -> HARD GATE -> write MANIFEST.sha256

`normalize` rewrites the operator's absolute paths to `$REPO`, `$HOME` and
`$SCRATCH`; `scan` then looks for what normalization could not reach — account
name, host name, uid, home path, UTC offsets, absolute paths outside the three
known roots. The gate refuses to seal on any hit.

**Every pass this lane ran is captured to a file**, not quoted from memory.
`logs/seal-check.log` and `logs/seal.log` are the transcripts with their exit
statuses. That is the V6 correction on this document: V6's first pass existed
only as five lines of hand-typed prose here, its second pass was said to be
"quoted in `checks.txt` with its exit" and appears nowhere in that file at
all, and the one figure of the five that could be checked against a shipped
artifact was the only one that happened to be right.

## Paths

Every path this package states is repository-relative or package-relative. No
evidence claim depends on an unrecorded absolute path. Where a tool's identity
matters for reproducibility it is recorded as identity and version — `node`,
`python3`, `chromium` — and never as a path through somebody's home directory.

`logs/head-consistency.py` additionally refuses a package that names a
package-relative path it does not contain, and refuses any commit SHA in a
claim-bearing member that is neither the head, the parent, the review
answered, a commit of the range, nor declared with a reason in
`logs/named-commits.json`. The default is refusal, which is the point: a stale
head from a superseded round cannot appear silently, and a deliberate mention
of another commit has to say what it is. That check exists because the V6
package's machine-readable pair audit recorded all thirty-two of its capture
paths under a `shots/` directory that package did not have: the digests were
right, the files were present under `screenshots/`, and every path in the
machine-readable record was unresolvable.

## Screenshots

**There are none, and that is a measured claim rather than an omission.**

`src/web/browser/catena/catena.css` and
`src/web/browser/catena/index.html` are byte-identical to the parent —
`git diff --stat` over them is empty, and the changed-file list in
`DERIVED-CLAIMS.md` is derived rather than typed. This correction changes what
the page *says* in states a valid corpus cannot produce: an unreadable
paragraph record, a payload whose words cannot be read, an address judged
against a root that could not be read whole. A raster of a valid chapter would
be identical at both ends, and offering one would be offering evidence that
cannot bear on the claim.

The evidence that replaces it is stronger and is machine-comparable: the V7
test file replayed against the **parent's** production files, same scenarios
and same oracles, in `logs/v7-tests-against-parent.log`. Every assertion that
distinguishes the two heads is in that log by name.

`logs/derive-claims.py` counts PNGs and before/after pairs from the sealed
directory regardless, and reports zero. A count is derived even when it is
zero, because "no screenshots" stated in prose and "zero screenshots" counted
by a program are different kinds of claim, and V6's screenshot counts are the
reason to prefer the second.

## The sealer's defects — two the V6 review found, one this lane did

### 1. `--check-only` deleted a package member

The mode's own `--help` says *"scan and report; never rewrite a member"*, and
on any failure it removed `MANIFEST.sha256` — the package's integrity proof.

This is not theoretical. This document, in its V6 form, instructed a
**reviewer** to run `--check-only` against the sealed package; and the same
document conceded that the account-name pattern is built from the operator's
runtime identity on word boundaries, so a reviewer whose username is an
ordinary English word sees a false hit on ordinary prose. Such a reviewer,
following these instructions, destroyed the proof and then met `sha256sum -c
MANIFEST.sha256` failing for a second, unrelated reason.

The V5 defect the removal was meant to answer is real and is a **different**
one: `normalize()` rewrites bytes, and a failing scan then returned before
`manifest()` ran, leaving a manifest describing bytes the package no longer
had. That can only arise in a mode that writes. `--check-only` never calls
`normalize()`, so nothing can go stale there and there is nothing to clear.
The clearing moved to the writing path, where the staleness it answers
actually happens. Two tests pin both halves.

### 2. The ZIP's members were never proved against the manifest

`verify()` proved the tree's bytes against the manifest's digests, and the
archive's bytes against the sidecar's digest, and **nothing joined them**.
`zipfile` was not imported; the archive was never opened. Since the sidecar is
computed from the archive after the fact, it always agrees with it — so an
archive built from a different tree, or carrying an injected member, verified
clean. The ZIP is what a reviewer actually receives, and it was the one
artifact whose contents nothing checked.

`archive_members()` now opens the archive, hashes every entry, and reports a
member the archive omits, a member it carries that the seal does not list, a
member whose bytes differ from the manifest's digest, and an archive not
rooted at the package directory. Four tests pin those four findings.

Writing that check immediately caught a third thing: the sealer's **own test
helper** built its archive with the members at the root, which is the layout
`guidance/external-review-handoffs.md` forbids and the opposite of what the
real shipped archives have. Nothing had noticed, because the two tests using
it only ever compared the archive's bytes to a digest computed from those same
bytes. The helper is corrected and the mis-rooted shape is pinned as a
finding.

### 3. A changed file at the repository root read as a dangling reference

Not a V6 finding — this one appeared while assembling V7, and it is recorded
because a reviewer will otherwise see the check pass and not know it was ever
wrong. The index check skips a reference that looks like a REPOSITORY path,
using a list of directory prefixes: `src/`, `tools/`, `scripts/`, `guidance/`
and so on. It cannot know a repository's ROOT-LEVEL filenames, so a document
naming a changed file like `PROJECT-WORK.md` was reported as naming a package
member the package does not contain — and the seal refused.

The fix is not a list of names. Every package under this protocol carries a
changed-file record, which is `git diff --name-status` against the parent, so
every path it names is a repository path by construction. The check reads that
record. A package without one gets the prefix heuristic it always had, and a
genuinely dangling reference standing beside a repository path is still
caught — two tests pin both halves. `logs/head-consistency.py` had the same
gap and took the same fix.

`logs/sealer-tests.log` is the run; its count is derived into
`DERIVED-CLAIMS.md` rather than typed, which is how V6 came to say 45 in three
documents where its own log says 46.

## What remains unsolvable by pattern

An absolute path outside `$HOME`, the repository root and the scratch
directory is not recognisable as private by any rule. It is handled by policy
— this package contains no such path — and not by the tool. Inherently, the
account-name and host-name checks match the operator's runtime identity, so a
reviewer whose account name is an ordinary word may see a false hit; the
documented answer is `SANITIZE_USER` / `SANITIZE_HOST`, and after the
correction above a false hit no longer costs anything.

## Verifying this package

    cd <package> && sha256sum -c MANIFEST.sha256
    python3 <package>/logs/sanitize-and-seal.py <package> --verify
    python3 <package>/logs/sanitize-and-seal.py <package> --check-only
    python3 <package>/logs/head-consistency.py --package <package>
    python3 <package>/logs/test-sanitize-and-seal.py

The second and third are written with the package named twice on purpose. V6
published them as `cd <package> && python3 logs/sanitize-and-seal.py <package>
--verify`, which cannot run: after the `cd`, the script path resolves and the
argument does not.
