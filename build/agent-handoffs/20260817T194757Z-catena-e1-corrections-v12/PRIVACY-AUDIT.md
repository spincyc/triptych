# Privacy audit

**Read the tense.** This file separates two kinds of statement, because
conflating them is how a privacy claim becomes untrue without anyone lying.

- **Present tense** describes the *tool*: what the sanitizer looks for and
  what it does about it. Those statements are true when this file is
  written, and they are checkable by reading `logs/sanitize-and-seal.py` and
  running `logs/test-sanitize-and-seal.py`.
- **Past tense** describes *this package*: what a scan of these exact bytes
  found. Those statements only become true at the seal, and the figures
  behind them are derived by the pipeline, not typed here. `checks.txt` and
  the seal transcript named in `logs/LOG-INDEX.md` carry them.

No figure in this file is typed. Where a count belongs, it is named and the
member that carries it is named beside it.

## What is looked for

The sanitizer derives the identities to remove at run time rather than
carrying them as literals — an account name, a hostname, a numeric user id
and a home directory — and then applies two families of rule.

**Value-free classes**, matched by shape, so the rule works for a value it
has never seen: the session scratch directory, a home path, the agent
workspace path, the lane evidence directory, `/proc/<pid>`, a labelled
process id, an email address, a D-Bus name, a UUID in either spelling, a
loopback address with a port, an RFC1918 address, a UTC offset on a date or
a time, a tokenized local time, and an IANA timezone by area or by bare
name. A local-offset timestamp is rewritten to its UTC instant rather than
deleted, so ordering and elapsed time survive while the offset does not.

**Value-keyed checks**, run independently of whether any rule fired, so the
scan cannot report clean while the identity survives: the account name, the
hostname, the literal home directory, the session bus path, the user slice,
the uid pair, a labelled uid, and the repository path.

**Member names are scanned as well as member bodies.** A name is a leak with
a filesystem in front of it.

**The sanitizer refuses to seal if its own source contains a private value
as a literal**, because a scanner that carries the string it is looking for
cannot see its own leak.

## Where it was looked

The scan covers, and the seal is refused unless every one of them is clean:

- every package member's bytes;
- every package member's **name**;
- the logs, including every attempt's log root;
- the attempt ledger `logs/attempts.json`;
- the outer invocation log;
- the ZIP sidecar carrying the digest and byte size;
- the screenshots and `screenshots/capture-metadata.json`;
- the P8 transcript;
- ZIP entry metadata.

## ZIP metadata

Entry timestamps are written at a fixed DOS epoch and mode bits are derived
from the file suffix, so the archive discloses no builder timezone, no UTC
offset, no umask and no platform. This is not asserted from the writing code
alone: a test in `logs/test-sanitize-and-seal.py` inspects the built
archive's own entry metadata directly, and the V11 review verified the
result independently.

## Screenshots

The adversarial captures are driven from a scratchpad fixture corpus, and
`screenshots/capture-metadata.json` records `$REPO` and `$SCRATCH`
placeholders rather than absolute paths. Every PNG carries only `IHDR`,
`IDAT` and `IEND` chunks — no `tEXt`, `iTXt`, `zTXt`, `eXIf`, `tIME` or
`iCCP` — and the chunk inspection is recorded rather than assumed. No
absolute path, account name, hostname, port, local timestamp or session
identifier appears in an image, in an image's name, or in the metadata.

## What a reviewer can run

These are the invocations that reproduce the audit against the extracted
package. Each is read-only.

    python3 logs/test-sanitize-and-seal.py
    python3 logs/sanitize-and-seal.py . --check-only
    python3 logs/authority-coherence.py --package . --head <the head this package names>
    python3 logs/test-authority-coherence.py

The first proves the tool; the second proves these bytes are at the
sanitizer's fixpoint; the third and fourth prove the package's authority
records agree and that the gate proving it can actually refuse.

`logs/sanitize-and-seal.py --check-only` is also run inside P8, from a
trusted copy outside the archive, so the reviewer's run and the sealing run
are the same check from two directions.

## What this audit does not claim

It does not claim that the tracked corpus is free of anything, that the
repository's history is free of anything, or that any file outside this
package was scanned. It claims what a scan of these member bytes, these
member names, these logs, this ledger, this sidecar, these screenshots and
this archive's metadata found.
