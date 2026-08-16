# Sanitization

## The method

`logs/sanitize-and-seal.py` — the corrected V7 sealer, its sanitization
semantics unchanged, its ordering corrected for V9 — runs over the package
in the phases `logs/assemble.sh` states:

    normalize to fixpoint -> scan -> index-check -> screenshot-pair audit
      -> FREEZE -> derive once from the freeze -> consistency audit
      -> re-hash + HARD GATE -> write MANIFEST.sha256 -> archive -> sidecar
      -> read-only verification from the final ZIP

`normalize` rewrites the operator's absolute paths to `$REPO`, `$HOME` and
`$SCRATCH` and localizable timestamps to placeholder offsets, repeated to a
fixpoint so the seal transcripts themselves are normalized; `scan`
re-derives the private values from the environment and asks, independently
of whether any rule fired, whether any survives — account name, host name,
uid, home path, absolute paths outside the known roots. A single hit and no
manifest is written.

**Every pass is captured to a file with its exit status**, not quoted from
memory: `logs/seal.log` carries every normalization pass with its header,
`logs/seal-check.log` the `--check-only` pass whose transcript must be
byte-identical to its own in-tree copy — the fixpoint proof. The sealer's
own tests ran first (`logs/sealer-tests.log`). `logs/assemble.sh` is the
one script that ran all of it, in the order whose reasons its own header
states.

## Paths and identities

Every path a document states is repository-relative or package-relative.
The battery ledgers and logs were written from live runs in an operator
clone and a parent-side clone; their absolute prefixes are normalized to
`$REPO`, `$HOME` and `$SCRATCH` by the sealer, and the scan proves no
un-normalized identity survived. Commit identities are confined to the
entitled set — `claims.json`'s head, parent, review and range — plus the
deliberate mentions declared with reasons in `logs/named-commits.json`.

## Verification

Run `logs/sanitize-and-seal.py <package> --check-only` for the scan alone,
or `logs/verify-final-package.py <zip>` for the whole read-only proof —
sidecar digest and size, layout, manifest, every claimed row against the
delivered bytes, the rows/derived partition, the re-rendered claims prose,
and the replayed consistency and sanitization audits over the extraction.
Both are read-only; running the verifier twice is proved to change nothing.
