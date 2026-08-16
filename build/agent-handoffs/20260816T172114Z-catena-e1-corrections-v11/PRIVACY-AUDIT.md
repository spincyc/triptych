# Sanitization — the method, and when each claim becomes true

**Read the tense.** This document is written with the package staged and not
yet sealed. Where it describes what the sealer does, that is a statement
about the tool, verifiable by reading `logs/sanitize-and-seal.py`. Where it
describes what the package contains, that becomes true **at the seal** and
is proved by the transcripts named here, not by this prose. The V10 package
said "the scan proves no un-normalized identity survived" while its staged
ledgers still carried raw operator paths; that sentence was true of the
sealed bytes and false of the bytes it was written over, and the difference
is the reason for this heading.

## The method

`logs/sanitize-and-seal.py` runs over the package in the phases
`logs/assemble.sh` states:

    P1 stage -> P2 normalize to a fixpoint -> scan -> index check
      -> P3 FREEZE -> P4 derive once from the freeze -> P5 consistency audit
      -> P6 re-hash + hard gate + write MANIFEST.sha256 -> P7 archive
      -> sidecar -> P8 read-only verification from the final ZIP

`normalize` rewrites the operator's absolute paths to `$REPO`, `$HOME` and
`$SCRATCH` placeholders and rewrites localizable timestamps, repeated to a
fixpoint so that the seal transcripts are themselves normalized. `scan`
then re-derives the private values from the environment and asks,
independently of whether any rule fired, whether any of them survives —
account name, host name, uid, home path, absolute paths outside the known
roots. A single hit and no manifest is written.

## What V11 changed here, and why

- **Prefix repair is not identity repair.** The home rule rewrote only the
  home-directory prefix, and its account class stopped at a separator.
  That left the two segments that identify one line of work — project and
  slug, under a worktrees root — standing in every path the package
  carried, and no check looked for them: a seal transcript could report
  zero hits over a package that named the workspace dozens of times. The
  sanitizer gained a rule matched against the **convention** rather than
  against any one name: a worktrees root, then exactly the project and slug
  segments. It accepts the prefix both raw and already tokenized, because
  ordering means the home rules usually get there first and the tokenized
  form is exactly the same disclosure.
- **The lane evidence directory is a session identity.** The agent
  directory segment plus the lane name under it says which round of which
  correction built the package. It is now matched wherever it appears,
  absolute or relative.
- **A local-offset timestamp is moved, not blanked.** V10 replaced the
  offset, which left a local wall-clock reading beside a package name
  stamped in UTC; the difference between the two disclosed the builder's
  zone. V11 rewrites the whole stamp to its UTC instant, marked `Z`, so
  ordering and elapsed time survive and the offset does not.
- **The archive no longer discloses the builder's clock or umask.** ZIP
  entries are written with a fixed DOS-epoch timestamp and suffix-derived
  mode bits.
- **One prior test pinned the leak as correct behaviour.** It is corrected,
  and the sealer's own suite says so.

## What was written as a token rather than sanitized into one

The battery ledgers go further than sanitization: their `cwd=$REPO` rows
were **written as tokens by `logs/battery.sh` itself** at preflight, so the
working-directory identity never existed in the record for the sealer to
have to catch. Every path stated in a package document is
repository-relative or package-relative by authorship, not by rewriting.

## Where the proof will be

Every pass is captured to a file with its exit status rather than quoted
from memory. `logs/seal.log` carries every normalization pass under its own
header, to the fixpoint. `logs/seal-check.log` carries the `--check-only`
pass whose transcript must be byte-identical to its own in-tree copy — that
byte identity is the fixpoint proof. The sealer's own tests run first, and
their transcript is `logs/sealer-tests.log`. All four are written during
assembly and do not exist while this document is being staged; they are
declared here and are named as declared-and-pending in `EVIDENCE-INDEX.md`
for exactly that reason.

Commit identities are confined to the entitled set — the head, the parent,
the review addressed, and the commits of the range — plus the commits this
package discusses rather than was produced from, each declared with its
reason in `logs/named-commits.json`. `logs/head-consistency.py` refuses a
package whose prose names any other commit; the default is refusal.

## Verification, with the exact invocations

Each of the three commands below was checked against the tool's own
argument parser before being published here, because the V10 package
published two invocations that could not run: it wrote
`sanitize-and-seal.py --verify` without the package positional that parser
requires, and `verify-final-package.py <zip>` positionally when that parser
takes the archive as `--zip`.

From the extracted package root:

    python3 logs/sanitize-and-seal.py . --verify

`package` is a required positional and `--verify` is one of the mutually
exclusive mode flags; this mode writes nothing. It checks every member
listed in `MANIFEST.sha256` against its recorded digest, reports any member
present but unlisted, and — when the sibling archive and its sha256 sidecar
sidecar are beside the extracted directory — compares the archive against
the sidecar digest and audits the archive's members.

For the scan alone, without the manifest check:

    python3 logs/sanitize-and-seal.py . --check-only

And the whole read-only post-seal proof, run from a trusted directory
outside the archive:

    python3 verify-final-package.py --zip PACKAGE.zip --sidecar PACKAGE.zip.sha256

`--zip` is required and takes the archive; `--sidecar` defaults to the
archive's name plus the sha256 suffix; `--name` defaults to the ZIP's own stem; and
`--tools` defaults to **the directory holding the verifier that is running**
— which is why the verifier must be run from an out-of-archive copy and not
from the one extracted out of the package under review. Substitute the
package's own name for `PACKAGE` in both arguments.

## What the post-seal transcript will state, and what it will not

The transcript opens with a binding header: the exact archive basename, its
byte size and its SHA-256, computed from the archive bytes before the first
check. It records the verifier's own path and digest, the trusted tools
directory, and for every shared tool it runs, the trusted digest beside the
digest of the copy the archive ships — failing hard on divergence rather
than trusting the archive to audit itself. It recomputes the archive's size
and SHA-256 **after every check** and states the pre-check and post-check
values with an explicit equality verdict.

That equality verdict is the whole of what this package claims about
re-running: the verifier is read-only by construction and the transcript
carries a pre/post pair proving the bytes it read did not move under it.
This package does **not** claim that running the verifier twice was
observed to change nothing, because it ships one transcript, not two.

The transcript also states, verbatim, that its trust anchor is outside the
archive but is not independent of the party that built the package. The
pipeline is not under version control in this workspace, so the anchor is
recorded by path and per-tool SHA-256 rather than by a commit
(`LIMITATIONS.md` §5).
