# Privacy and sanitization audit

## Method

`logs/sanitize-and-seal.py`, carried forward from the V4.1 package with six
named additions recorded below. Four phases, in this fixed order, because
sanitizing after hashing would silently invalidate every digest:

1. **normalize** — every text member rewritten through an ordered substitution
   table. Text is decided by byte-sniffing, not by suffix, so extensionless
   files and `.py` are included. `MANIFEST.sha256` is skipped by name.
2. **scan** — an *independent* verification pass. It does not ask "did a rule
   fire"; it asks "is any private value still present", over both file
   **contents and file names**.
3. **index_check** — every markdown link target and every backticked token
   containing a slash must resolve inside the package.
4. **manifest** — SHA-256 of every member, `MANIFEST.sha256` unlinked first so
   it is never a member of itself.

**Phases 2 and 3 are a hard gate.** Any hit, or any unresolvable reference, and
the tool writes no manifest and exits 1. Every private value is derived at
runtime from the environment; no private literal appears anywhere in the
script, which is what lets it scan itself honestly.

## Result

First run, over the assembled package:

```
normalized 7 file(s), 170 substitution(s)
sanitization scan: 0 private-token hit(s)
evidence-index check: 0 missing reference(s)
MANIFEST.sha256 written: 60 file(s) covered
```

The 170 substitutions were absolute paths inside test tracebacks and one gate
report; the seven files are named under "What was removed" below.

Final run, after this record itself was completed, and the run whose manifest
ships:

```
normalized 0 file(s), 0 substitution(s)
  (no file changed: inputs were already normalized, or the rules matched
   nothing -- the scan below is what decides)
sanitization scan: 0 private-token hit(s)
evidence-index check: 0 missing reference(s)
MANIFEST.sha256 written: 60 file(s) covered
```

Zero substitutions on the second pass is the property that matters: the
normalizer is idempotent over this package, so nothing was still being rewritten
when the digests were taken.

## The six additions, and why they were made

The V3 predecessor of this sealer published an account name, a PID, a uid, a
D-Bus name and a session-bus path **while reporting zero hits**, because its
rules knew the username only as a path component and its own denylist was
invisible to its own scan. `PROJECT-WORK.md` records that failure. V4.1 fixed
it structurally. Auditing V4.1 against that same record found six residual
gaps, every one verified against the code before anything was changed:

| Gap | Verified | Closed by |
| --- | --- | --- |
| `PLACEHOLDER_PID` was declared and never used — no PID rule, no PID check, so a labelled process id passed clean. This is one of the five classes the predecessor was faulted for. | real | paired rule and check for labelled pids and `/proc/<pid>/` paths |
| A bare uid passed clean; only `/run/user/`, `user@…service` and `uid=` were known. | real | a shared uid-label prefix, a `/proc/status` column-run rule, and a `uid:uid` pair rule, each with a matching check |
| The IANA timezone rule covered six continent prefixes only. | real | the full area set including the legacy single-word areas, three-segment zones, and bare zone names under a timezone-context rule |
| The UUID rule knew only the canonical hyphenated form, so a machine id or a CDP target id passed clean. | real | a compact 32-hex rule and check |
| No email rule or check existed at all. | real | an email rule and check, with an exemption for the known-public no-reply forms |
| The `dbus-name` rule and its check disagreed on the left boundary — **exactly disjoint**, so the normalizer was inert for every real bus name while the check was a pure blocker. | real, and worse than reported | rule and check are now built from shared pattern constants; the rule set is the union |

The last one is the structural fix and the important one: **a rule and its
check are now built from one string**, so they cannot drift apart again the way
these two had.

One further addition has no counterpart in V4.1: before any write, the tool
now asserts that none of its own derived identity values appears as a literal
in its own source, and refuses if one does. V4.1 stayed honest only by
discipline — a private value written into a regex literal there would have made
the tool blind to it exactly as the predecessor was. That is now checked rather
than remembered.

## What was removed

Seven files carried absolute paths, all of them machine-generated logs quoting
tracebacks or a report root:

| File | Class replaced | Placeholder |
| --- | --- | --- |
| `logs/all-tests-head.log`, `logs/all-tests-base.log` | repository root in tracebacks | `$REPO` |
| `logs/make-k-check-head.log` | repository root | `$REPO` |
| `logs/browser-gate-head.json`, `logs/browser-gate-base.json` | report root | `$REPO` |
| `logs/new-tests-against-base.log` | repository root | `$REPO` |
| `logs/probe-head.json`, `logs/probe-base.json` | scratch and home paths | `$SCRATCH`, `$HOME` |

No screenshot, no record and no shipped tool required a substitution.

## What was deliberately not changed

- **Bare, unlabelled uids and pids are still not caught.** Matching a bare
  four-digit number by value would rewrite every byte count in every log in
  this package. This is a residual manual-review item, not a covered class.
- **An absolute path outside `$HOME`, the repository root and the scratch
  directory is unrecognisable as private** and cannot be solved by pattern.
  Handled by policy: this package contains no such path.
- **One pre-existing rule is wrong and was left alone.** V4.1's loose D-Bus
  rule mangles timestamps of the form `HH:MM:SS.mmm`. It was kept verbatim
  because this lane's instruction was to add coverage and remove none. Its only
  effects are damaging that one timestamp shape and matching bus names in the
  one position they never occur; nothing it uniquely covers is flagged by any
  check, so a maintainer can delete it and lose nothing. **Recorded here rather
  than fixed, so the decision is the maintainer's.**

## Independent verification

Run separately from the sealer, against the sealed package:

| Token | Files containing it |
| --- | --- |
| the operating account name | 0 |
| the host name | 0 |
| `/home/<account>` | 0 |
| the scratch directory name | 0 |
| a session UUID | 0 |

```
cd <package> && sha256sum -c MANIFEST.sha256      # every member OK
python3 logs/sanitize-and-seal.py <package> --check-only
```

## Two things a reviewer should not over-read

1. **`0 missing reference(s)` is not proof that every named artifact exists.**
   The index checker inspects backticked tokens containing a slash and markdown
   link targets. A prose mention of a file, or a backticked name with no slash,
   is not checked.
2. **The scan cannot see what it has no pattern for.** It is a verification of
   the classes named above, not a guarantee of privacy in general. The
   inventory in `HANDOFF.md` §10 and the artifact review it records are what
   bound the contents.

## Screenshots

Twenty PNGs, all `Page.captureScreenshot` over the DevTools Protocol, written
straight to disk. Chromium's encoder emits no `tEXt`, `iTXt`, `zTXt`, `eXIf`,
`pHYs` or `tIME` chunks, so none carried metadata and none had to be stripped.
They are page-content captures, not desktop grabs: no browser chrome, title
bar, path, account name or host name appears in any of them.
