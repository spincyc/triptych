# Privacy and sanitization — what leaked, why the sealer missed it, what changed

The V3 independent review found that the sealed V3 package published private
session identifiers **while its own sanitizer reported zero hits**. That is the
part worth dwelling on: the failure was not that sanitization was skipped. It
ran, it passed, and it was wrong.

## What the V3 package published

Confirmed by re-reading the sealed V3 package read-only. Four of its 27 files
carried something private; 23 were clean.

| file | what it published |
| --- | --- |
| `AT-LIMITATION.md` | the **account name** as a bare column of pasted `busctl` output, a host **PID** (twice), the **uid** by way of a systemd user unit and a session-bus path, and a **D-Bus unique connection name** |
| `logs/sanitize-and-seal.py` | **five private workspace and clone paths**, written into its own pattern table as literals |
| `logs/make-k-check-head.log` | an **IANA timezone** and a UTC offset |
| `commits.txt` | a UTC offset |

The V3 seal log reads, in full agreement with itself and in complete
disagreement with the package: `sanitization scan: 0 private-token hit(s)`.

## Why it reported zero

Five defects. The first two are the ones that matter.

**1. It only ever knew the username as a path component.** Every rule in the
V3 table was anchored on `/home/<x>` or `/Users/<x>`. The sanitizer never read
the account name from the environment — it inferred it structurally, as
"whatever follows `/home/`". A username printed as a free-standing column by
`busctl` is not preceded by a slash, so **no pattern in the table could ever
match it**. Every command that names a user without a path prefix — `busctl`,
`ps -u`, `id`, `whoami`, `who`, `ls -l`, `git config user.name` — was a hole.

**2. It shipped its own denylist, and was structurally blind to it.** The V3
table hard-coded five private workspace paths as regex literals. Its own scan
pattern `/home/[A-Za-z0-9._-]+` cannot match the literal source text
`/home/[A-Za-z0-9._-]+/git/...`, because the next character is `[`, which is
not in the character class. The metacharacters that make a pattern general are
exactly what hides that pattern from itself. So the most private-path-dense
file in the package sailed through its own scan.

**3. The seal was written even when the scan failed.** The manifest was
written unconditionally; a failing scan produced a non-zero exit and a fully
sealed package anyway. The scan was advisory, not a gate.

**4. The walk was a suffix allowlist.** `.sha256`, extensionless files and
unknown suffixes were neither normalized nor scanned, and **file names were
never examined at all** — only contents.

**5. The scratch rule was over-greedy**, consuming the whole remainder of a
path. Sixty-four baseline traceback lines were reduced to `File "$SCRATCH"`,
destroying the identity of the test that raised. Sanitization silently
degraded the evidence it was protecting.

## What V4 changed

`logs/sanitize-and-seal.py` in this package is a different program. Its
docstring records the same five defects at the point of fix.

- **Identities are values, read at run time.** Account name, hostname and uid
  come from the environment, and the account name is matched on **word
  boundaries wherever it appears**, with no path context required. This is the
  V3 miss, closed directly.
- **No private literal is written in the file.** Every private value is
  derived, so the sanitizer is not itself a disclosure and is not immune to
  its own scan.
- **The scan is a hard gate.** One hit and no manifest is written.
- **Every file is walked**, text decided by sniffing bytes rather than
  trusting a suffix, and **relative paths are scanned as well as contents**.
- **Replacements preserve their tails**, so a traceback still says which file
  raised.
- **Categories V3 had no rule for at all** are covered: PIDs, uid, D-Bus
  connection names, UUIDs, private IP ranges, IANA timezones and UTC offsets.
- **The ambiguous `normalized 0` is gone.** The log reports files changed and
  substitutions applied, and says plainly that a zero means either
  already-clean inputs or broken rules — and that the scan is what decides.

One thing V3 got right is kept exactly: **normalize, scan, index-check, then
manifest.** Sanitizing after the manifest is computed silently invalidates
every digest in it. The ordering was never the bug; the coverage and the
gating were.

## Proof that the new sanitizer would have caught it

The V4 sanitizer was run in `--check-only` mode against the **sealed V3
package**, unmodified. Where V3's own sealer reported `0 private-token
hit(s)`, the V4 sealer refuses to seal and reports the leaks, including the
one that mattered most:

```
REFUSING TO SEAL: private tokens are still present.
sanitization scan: 9 private-token hit(s)
  AT-LIMITATION.md:58: [account-name] '<user>'
  AT-LIMITATION.md:58: [user-slice] 'user@<uid>.service'
  AT-LIMITATION.md:58: [dbus-name] ':<n>.<n>'
  AT-LIMITATION.md:80: [session-bus] '/run/user/<uid>'
  commits.txt:9: [utc-offset] ...
  logs/make-k-check-head.log:25: [iana-timezone] ...
  logs/sanitize-and-seal.py:38: [scratch-dir] ...
```

(The values are elided here for the obvious reason. The check is reproducible:
run this package's sealer against the V3 package with `--check-only`.)

## The V3 package is not mutated

The V3 package remains exactly as sealed, at its evidence commit, with its
recorded digest intact. It is **immutable evidence of a review that happened**,
and correcting it after the fact would destroy that. This package replaces it
for the purposes of the next review; it does not amend it.

## This package

- No command transcript is pasted into any document here. `AT-LIMITATION.md`
  states findings as findings, which is what made V3's leak possible in the
  first place.
- The seal was run to completion, and its output is at
  `logs/SANITIZATION-AND-INDEX-CHECK.log`.
- The scan gate passed **before** the manifest was written, so the manifest
  covers sanitized bytes.
