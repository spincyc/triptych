# Privacy and sanitization audit

## Method

Sealed with `logs/sanitize-and-seal.py`, carried forward unmodified from the V4
package (where it was itself an evidence artifact, not repository tooling). It
runs four phases: **normalize → scan → index_check → manifest**, and it is a
**hard gate** — any scan hit or unresolvable in-package reference refuses to seal
and writes no manifest.

The scan is an *independent* verification pass, not a re-run of the normalizer,
so a substitution rule that missed something is still caught. It decides text by
byte-sniffing rather than by file suffix, and it scans **file names as well as
contents**.

## Result

    normalized 6 file(s), 136 substitution(s)
    sanitization scan: 0 private-token hit(s)
    evidence-index check: 0 missing reference(s)
    MANIFEST.sha256 written

## What was removed

136 substitutions across 6 files, all in raw test and check logs that quote
absolute paths in tracebacks:

| Class | Replaced with |
| --- | --- |
| repository root | `$REPO` |
| home directory and `/home/<account>` | `$HOME` |
| bare account name (word-boundary, case-insensitive) | placeholder |
| scratch/session directories | `$SCRATCH`, path tail preserved |
| host name | placeholder |
| session/D-Bus identifiers, UUIDs | placeholders |
| loopback host:port, RFC1918 addresses | placeholders |
| timezone offsets and IANA zones | `<tz>` |

## Independent verification

Beyond the sealer's own scan, a direct probe over every text member:

| Token | Files containing it |
| --- | --- |
| `/home/<account>` | **0** |
| bare account name | **0** |
| this session's UUID | **0** |
| host name (`<host>`) | **0** |
| the disposable clone directory name | **0** |

The disposable clone this lane worked in is named nowhere in the package. All
in-package paths are package-relative; all repository paths are written
repository-relative or under `$REPO`.

## Two findings worth the reviewer's attention

   `REFUSING TO SEAL` on two `[dbus-name]` hits — a colon followed by each of
   the fractional pixel values 767.59375 and 6749.875 — which were **screenshot
   clip coordinates** in an evidence
   index, not D-Bus names. This is a false positive of the `:N.N` rule. It was
   fixed by rewriting that index with integer coordinates and a cleaner shape.
   **The sealer was not weakened, and no rule was relaxed to get past it.**

2. **The index checker does not catch every dangling reference.** It only
   inspects backticked tokens containing `/`, so a referenced file whose name
   has no slash (for example this file) is not verified. One real defect it did
   catch was a backticked browser-version string being read as a path; that was
   reworded. Reviewers should not read `0 missing reference(s)` as proof that
   every named artifact exists.

## Screenshots

53 PNGs. They render only published repository content — Scripture text,
commentary fragments and their recorded apparatus — at real routes. No browser
chrome, no window title bar, no file path, no user name and no host name appears
in any image, because each capture is a page-content screenshot taken over the
DevTools Protocol rather than a desktop or window grab.
