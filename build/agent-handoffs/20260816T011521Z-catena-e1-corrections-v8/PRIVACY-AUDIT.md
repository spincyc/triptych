# Sanitization

## The method

`logs/sanitize-and-seal.py` — the corrected V7 sealer, reused unchanged —
runs one pipeline over the package:

    self-check -> clear manifest -> normalize -> scan -> index-check
               -> screenshot-pair audit -> HARD GATE -> write MANIFEST.sha256

`normalize` rewrites the operator's absolute paths to `$REPO`, `$HOME` and
`$SCRATCH` and localizable timestamps to placeholder offsets; `scan`
re-derives the private values from the environment and asks, independently
of whether any rule fired, whether any survives — account name, host name,
uid, home path, absolute paths outside the known roots. A single hit and no
manifest is written.

**Every pass is captured to a file with its exit status**, not quoted from
memory: `logs/seal.log` is the first sealing pass, `logs/seal-check.log` the
`--check-only` pass over the normalized tree. The sealer's own tests ran
first (`logs/sealer-tests.log`). `logs/assemble.sh` is the one script that
ran all of it, in the order whose reasons its own header states.

## Paths and identities

Every path a document states is repository-relative or package-relative. The
battery ledgers and logs were written from live runs in an operator clone and
a parent-side clone; their absolute prefixes are normalized to `$REPO` and
`$SCRATCH` by the sealer, and the scan proves no un-normalized identity
survived. Commit identities are confined to the entitled set —
`claims.json`'s head, parent, review and range — plus the deliberate
mentions declared with reasons in `logs/named-commits.json`.

## Verification

Run `logs/sanitize-and-seal.py <package> --check-only` for the scan alone,
or `--verify` to prove every archive member against `MANIFEST.sha256`. Both
are read-only; the V7 correction that made `--check-only` truly read-only is
part of the reused tool and covered by its shipped tests.
