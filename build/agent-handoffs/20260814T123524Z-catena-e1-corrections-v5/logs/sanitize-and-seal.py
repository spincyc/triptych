#!/usr/bin/env python3
"""Sanitize a handoff package, prove it clean, and only then seal it.

WHY THIS IS NOT THE V3 SCRIPT
=============================

The V3 sealer reported `0 private-token hit(s)` over a package that published
the operator's account name, a host PID, a uid, a systemd user unit and a
D-Bus session bus path. It was not unlucky; it could not have found them. Four
defects, each fixed here:

1. IT ONLY KNEW THE USERNAME AS A PATH COMPONENT. Every rule was anchored on
   `/home/<x>` or `/Users/<x>`, so the account name was matchable only when it
   followed a slash. `busctl` prints it as a bare column. Nothing in the table
   could ever match it. THE FIX: identities are read from the environment as
   VALUES -- account, host, uid -- and matched on word boundaries wherever they
   appear, independent of any path context.

2. IT SHIPPED ITS OWN DENYLIST, AND WAS BLIND TO IT. The table hard-coded five
   private workspace paths as regex literals. Scanning `/home/[A-Za-z0-9._-]+`
   against the literal text `/home/[A-Za-z0-9._-]+/git/...` fails, because `[`
   is not in the character class: the metacharacters that generalise a pattern
   are exactly what hides it from itself. THE FIX: no private literal is
   written in this file. Every private value is derived at run time, and this
   script is scanned like any other member of the package.

3. THE SEAL WAS WRITTEN EVEN WHEN THE SCAN FAILED. `manifest()` ran
   unconditionally; a dirty package still got a manifest and a non-zero exit
   nobody read. THE FIX: the scan is a HARD GATE. A single hit and no manifest
   is written at all.

4. THE WALK WAS A SUFFIX ALLOWLIST. `.sha256`, extensionless files and unknown
   suffixes were neither normalised nor scanned, and file NAMES were never
   examined. THE FIX: every file is walked, text is decided by sniffing the
   bytes, and the relative paths are scanned too.

One thing V3 got right is kept exactly: normalise, scan, index-check, THEN
manifest. Sanitising after the manifest is computed silently invalidates every
digest in it. The ordering was never the bug.

A fifth, quieter defect is also fixed: V3's scratch rule consumed the whole
remainder of a path, so 64 baseline tracebacks read `File "$SCRATCH"` and lost
the test file that raised. Replacements here preserve the tail.

WHAT V5 ADDS TO V4.1
====================

V4.1 closed the four defects above. An audit of it found six holes, all of them
"the class is named but not covered", and all of them closed here:

a. A PID PLACEHOLDER WITH NO RULE AND NO CHECK. `PLACEHOLDER_PID` was declared
   and never referenced: a labelled process id passed clean, and a process id
   is one of the five values V3 was faulted for publishing.
b. THE UID WAS KNOWN IN THREE SHAPES ONLY -- `/run/user/N`, `user@N.service`,
   `uid=N`. The shapes `/proc/status` and command lines actually print it in
   were not among them.
c. THE TIMEZONE RULE KNEW SIX AREAS out of the IANA set, so most of the world
   passed clean.
d. THE UUID RULE KNEW ONLY THE HYPHENATED FORM, so `/etc/machine-id` and CDP
   target ids -- 32 unbroken hex digits -- passed clean.
e. THERE WAS NO EMAIL RULE AND NO EMAIL CHECK AT ALL.
f. THE `dbus-name` RULE AND ITS CHECK DISAGREED ON THEIR LEFT BOUNDARY, and
   disagreed exactly, not partially: the rule required a word character before
   the colon, the check required the absence of one. The rule could therefore
   never repair a single thing the check flagged, and the check was a pure hard
   blocker. Rule and check now share one pattern string wherever they cover the
   same class -- see the constants below -- because that drift is invisible in
   review and fatal in operation.

TWO CONSTRAINTS SHAPE WHAT IS EXPRESSIBLE HERE, both consequences of defect 2:

* NO PRIVATE VALUE MAY BE A LITERAL IN THIS FILE. `own_source_literals()` now
  asserts this at startup instead of trusting the author to remember it.
* THIS FILE IS A PACKAGE MEMBER AND IS SCANNED BY ITS OWN CHECKS, so a check
  that flags a bare word flags this file's own source for containing that word
  in its own pattern. That is why bare timezone names are matched only in a
  timezone context, and why the examples in the comments below are written with
  `N` where a real leak would carry a digit. A denylist that cannot be written
  down safely is a denylist this design will not accept.

Usage:  sanitize-and-seal.py PACKAGE_DIR [--check-only]
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import os
import re
import socket
import subprocess
import sys
from pathlib import Path

PLACEHOLDER_USER = "<user>"
PLACEHOLDER_HOST = "<host>"
PLACEHOLDER_UID = "<uid>"
PLACEHOLDER_PID = "<pid>"
PLACEHOLDER_DBUS = "<dbus-name>"
PLACEHOLDER_UUID = "<uuid>"
PLACEHOLDER_TZ = "<tz>"
PLACEHOLDER_EMAIL = "<email>"

# ---------------------------------------------------------------------------
# SHARED PATTERNS. Every class below is covered by BOTH a normalize rule and a
# scan check, and they are built from the SAME string. Defect (f) was two
# hand-written boundaries that drifted until they no longer intersected; a
# shared constant makes that particular failure unrepresentable. Patterns that
# need a runtime identity value (the uid) cannot be constants, so for those the
# shared part -- the risky part, the boundary -- is the constant and only the
# value is spliced in at call time.
# ---------------------------------------------------------------------------

# (a) A process id is identifiable ONLY by the label in front of it. A bare
# integer is indistinguishable from a byte count, a duration or a line number,
# so no value-keyed rule could be safe. Covers `pid=N`, `Pid:<tab>N`, `PID N`,
# `--pid N` and `ppid=N`; the label is captured so the replacement keeps it.
# `pids: N` and prose like `the pid is N` deliberately do not match.
PID_LABELLED = r"\b(p?pid\b[ \t:=]+)\d+"
PROC_PID = r"/proc/\d+\b"

# (b) The uid labels V4.1 did not know. Same reasoning as the pid: the uid IS a
# value we hold, but matching it bare would rewrite every occurrence of that
# integer in every log, so the label carries the match and the value confirms
# it. `[ers]?[ug]id` covers uid/gid/euid/egid/ruid/rgid/suid/sgid; the optional
# `--` covers command-line flags. The `\b` sits after the dashes because there
# is no word boundary before one.
UID_LABEL = r"(?:--)?\b(?:[ers]?[ug]id|user|group|owner)\b[ \t:=]+"

# (f) A unique bus name as it really appears: standing in a `busctl` column,
# after an `=`, inside parentheses. LOOSE is V4.1's rule verbatim and is kept
# so nothing it caught is lost; NAME is V4.1's check verbatim and is now a rule
# as well. Their union is what normalizes, so the rule set covers every
# position the check can flag.
DBUS_TAIL = r":\d+\.\d+\b"
DBUS_LOOSE = r"\b" + DBUS_TAIL
DBUS_NAME = r"(?<![\w.])" + DBUS_TAIL

# (d) Both spellings of a 128-bit id. The compact form is what `/etc/machine-id`
# and CDP target ids use. The word boundaries keep it from biting a chunk out
# of a 40-hex git object name or a 64-hex sha256 digest.
UUID_HYPHENATED = (r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
                   r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
UUID_COMPACT = r"\b[0-9a-fA-F]{32}\b"

# (c) The IANA area set in full, plus the legacy single-word areas. Written as
# separate string fragments so that no `Area/City` sequence exists in this
# file's own source -- see the header: this file is scanned by this pattern.
TZ_AREA = (r"\b(?:Africa|America|Antarctica|Arctic|Asia|Atlantic|Australia"
           r"|Brazil|Canada|Chile|Etc|Europe|Indian|Mexico|Pacific|US)"
           r"/[A-Za-z_+-]+(?:/[A-Za-z_+-]+)?")

# (c, continued) The bare zone names -- the ones with no area prefix -- are
# matched ONLY after something that establishes they are a zone. Two reasons,
# and both are hard: several of them are ordinary English words and a package
# is free to discuss them in prose, and a check listing them as bare words
# would flag THIS FILE for containing that list. The context prefix is captured
# so the replacement can keep it.
TZ_BARE_NAMED = (r"(?:UTC|GMT|Japan|Israel|Egypt|Cuba|Poland|Turkey|Iceland"
                 r"|Iran|Jamaica|Libya|Portugal|Singapore|Hongkong|Eire|Navajo"
                 r"|Greenwich|Universal|Zulu|Kwajalein|PRC|ROK|ROC|GB|NZ|W-SU"
                 r"|EST5EDT|CST6CDT|MST7MDT|PST8PDT|EST|MST|HST|CET|EET|MET|WET)")
TZ_CONTEXT = (r"(TZ=|zoneinfo/|(?i:time ?zone)[ \t]*[:=][ \t]*)"
              + TZ_BARE_NAMED + r"\b")

# (e) An address, with the public forms this repository legitimately carries
# held out by name: the Anthropic no-reply trailer address and GitHub's
# per-account no-reply domain are published identities, not machine-private
# ones, and flagging them would make the hard gate fire on every commit trailer
# in the package. The systemd instance suffixes are held out for a different
# reason -- `user@N.service` is not an address at all, and without this it
# would be rewritten as one.
EMAIL_EXEMPT = (r"(?:noreply@anthropic\.com"
                r"|[A-Za-z0-9._%+-]+@users\.noreply\.github\.com"
                r"|noreply@github\.com"
                r"|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:service|socket|scope"
                r"|slice|target|timer|mount|device|path))"
                r"(?![A-Za-z0-9._%+-])")
# The lookbehind is load-bearing: without it the engine simply restarts one
# character into an exempt address and matches its tail.
EMAIL = (r"(?<![A-Za-z0-9._%+-])(?!" + EMAIL_EXEMPT + r")"
         r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def identities() -> dict[str, str]:
    """The private values, read from the environment rather than guessed.

    Overridable so a reviewer can re-run this against the sealed package with
    the operator's values and reproduce the zero-hit result themselves.
    """
    user = os.environ.get("SANITIZE_USER") or getpass.getuser()
    host = os.environ.get("SANITIZE_HOST") or socket.gethostname()
    uid = os.environ.get("SANITIZE_UID") or str(os.getuid())
    home = os.environ.get("SANITIZE_HOME") or str(Path.home())
    return {"user": user, "host": host, "uid": uid, "home": home}


def repo_root() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return ""


def rules(who: dict[str, str], root: str) -> list[tuple[re.Pattern[str], str]]:
    """Ordered substitutions. Longest, most specific paths first."""
    user = re.escape(who["user"])
    host = re.escape(who["host"])
    uid = re.escape(who["uid"])
    home = re.escape(who["home"])
    made: list[tuple[re.Pattern[str], str]] = []
    if root:
        made.append((re.compile(re.escape(root)), "$REPO"))
    # Sibling clones and worktrees under the home directory. ONLY THE PREFIX is
    # replaced, so the tail survives: V3's rule consumed the remainder and
    # reduced 64 baseline tracebacks to `File "$SCRATCH"`, destroying the
    # identity of the test that raised. Sanitizing must not cost evidence.
    made.append((re.compile(home), "$HOME"))
    made.append((re.compile(r"/tmp/[A-Za-z0-9._-]*claude[A-Za-z0-9._-]*"
                            r"(/[^\s\"'>)\],]*)?"),
                 lambda m: "$SCRATCH" + (m.group(1) or "")))
    made.append((re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+"), "$HOME"))
    made.append((re.compile(r"/run/user/" + uid), "/run/user/" + PLACEHOLDER_UID))
    made.append((re.compile(r"\buser@" + uid + r"\.service\b"),
                 "user@" + PLACEHOLDER_UID + ".service"))
    made.append((re.compile(r"\buid=" + uid + r"\b"), "uid=" + PLACEHOLDER_UID))
    # THE V4.1 MISS (b): every other shape the uid is printed in. The pair form
    # goes first -- `--user N:N` -- because the labelled rule below would
    # otherwise stop at the colon and leave the second half standing. The
    # labelled rule takes a RUN of values, not one, because `/proc/status`
    # prints four uid columns on a line and repairing only the first would
    # leave three behind for the check to block on.
    made.append((re.compile(r"\b" + uid + r":" + uid + r"\b"),
                 PLACEHOLDER_UID + ":" + PLACEHOLDER_UID))
    made.append((re.compile(UID_LABEL + r"(?:" + uid + r"[ \t,]*)+",
                            re.IGNORECASE),
                 lambda m: re.sub(r"\b" + uid + r"\b", PLACEHOLDER_UID,
                                  m.group(0))))
    # THE V4.1 MISS (a): the placeholder existed, the rule did not.
    made.append((re.compile(PROC_PID), "/proc/" + PLACEHOLDER_PID))
    made.append((re.compile(PID_LABELLED, re.IGNORECASE),
                 lambda m: m.group(1) + PLACEHOLDER_PID))
    # THE V4.1 MISS (e): addresses. Before the account-name rule, so a full
    # address is placeheld as one token rather than being left as a mangled
    # `<user>@domain` that no later check would recognise. After the
    # `user@<uid>.service` rule for the same reason in reverse.
    made.append((re.compile(EMAIL), PLACEHOLDER_EMAIL))
    # The V3 MISS: the account name as a free-standing token.
    made.append((re.compile(r"\b" + user + r"\b", re.IGNORECASE), PLACEHOLDER_USER))
    made.append((re.compile(r"\b" + host + r"(\.local)?\b", re.IGNORECASE),
                 PLACEHOLDER_HOST))
    # THE V4.1 MISS (f): LOOSE is V4.1's rule, kept exactly; NAME is the form a
    # bus name is actually written in, which V4.1 flagged but could not repair.
    # LOOSE runs first so its output -- and its leading space -- is unchanged.
    made.append((re.compile(DBUS_LOOSE), " " + PLACEHOLDER_DBUS))
    made.append((re.compile(DBUS_NAME), PLACEHOLDER_DBUS))
    made.append((re.compile(UUID_HYPHENATED), PLACEHOLDER_UUID))
    # THE V4.1 MISS (d): the same id with the hyphens taken out.
    made.append((re.compile(UUID_COMPACT), PLACEHOLDER_UUID))
    made.append((re.compile(r"\b(?:127\.0\.0\.1|localhost):\d+\b"),
                 PLACEHOLDER_HOST + ":<port>"))
    made.append((re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2\d|3[01]))"
                            r"(?:\.\d{1,3}){2,3}\b"), "<ip>"))
    made.append((re.compile(r"[+-]\d{2}:\d{2}\b"), PLACEHOLDER_TZ))
    # THE V4.1 MISS (c): six areas became all of them, plus the bare zone names
    # in a zone context. The context prefix is kept; only the zone is replaced.
    made.append((re.compile(TZ_AREA), PLACEHOLDER_TZ))
    made.append((re.compile(TZ_CONTEXT), lambda m: m.group(1) + PLACEHOLDER_TZ))
    return made


def forbidden(who: dict[str, str], root: str) -> list[tuple[str, re.Pattern[str]]]:
    """The verification pass. Independent of the rules above by construction:
    these ask "is any private VALUE still present", not "did a rule fire"."""
    user = re.escape(who["user"])
    host = re.escape(who["host"])
    uid = re.escape(who["uid"])
    home = re.escape(who["home"])
    made = [
        ("account-name", re.compile(r"\b" + user + r"\b", re.IGNORECASE)),
        ("hostname", re.compile(r"\b" + host + r"\b", re.IGNORECASE)),
        ("home-path", re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+")),
        ("home-literal", re.compile(home)),
        ("session-bus", re.compile(r"/run/user/" + uid)),
        ("user-slice", re.compile(r"user@" + uid + r"\.service")),
        # The uid in every other shape it is printed in. The optional run of
        # already-substituted placeholders is what lets this catch a column
        # that a partial repair left behind: `Uid:<tab><uid><tab>N`.
        ("uid-pair", re.compile(r"\b" + uid + r":" + uid + r"\b")),
        ("uid-labelled", re.compile(UID_LABEL
                                    + r"(?:" + re.escape(PLACEHOLDER_UID)
                                    + r"[ \t,]*)*" + uid + r"\b",
                                    re.IGNORECASE)),
        ("pid", re.compile(PID_LABELLED, re.IGNORECASE)),
        ("proc-pid", re.compile(PROC_PID)),
        ("email", re.compile(EMAIL)),
        ("dbus-name", re.compile(DBUS_NAME)),
        ("uuid", re.compile(UUID_HYPHENATED)),
        ("uuid-compact", re.compile(UUID_COMPACT)),
        ("scratch-dir", re.compile(r"/tmp/[A-Za-z0-9._-]*claude")),
        ("loopback", re.compile(r"\b(?:127\.0\.0\.1|localhost):\d+\b")),
        ("iana-timezone", re.compile(TZ_AREA)),
        ("timezone-name", re.compile(TZ_CONTEXT)),
        ("utc-offset", re.compile(r"\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}")),
    ]
    if root:
        made.append(("repo-path", re.compile(re.escape(root))))
    return made


def own_source_literals(who: dict[str, str]) -> list[str]:
    """Assert that no private value is written into this file as a literal.

    Defect 2 was not that V3 shipped a bad denylist; it was that the denylist
    was a REGEX, and a pattern's own metacharacters hide it from a scan for the
    thing it describes. V4.1 fixed that by deriving every private value at run
    time -- but nothing stopped the next editor from pasting a real value into
    a pattern, and if they did, this file would go blind to that value in
    exactly the way V3 did, silently, with a clean report.

    So the property is checked instead of assumed. This is cheap and it is not
    a substitute for the scan: the scan below covers this file's CONTENT like
    any other member's, and would catch a plain literal. What it cannot catch
    is a literal buried in a character class or an alternation, which is
    precisely the shape defect 2 had. This runs before anything is written.

    A short or word-like identity value -- an account named for a word this
    file uses -- will trip this. That is not a new fragility: such a value
    would already make the rules rewrite that word throughout the package and
    the checks flag every file containing it. Refusing loudly is the correct
    end state either way.
    """
    try:
        source = Path(__file__).read_text(encoding="utf-8")
    except (OSError, NameError):
        # Not readable (frozen, stdin, deleted): report it rather than passing
        # a check that was never performed.
        return ["<source unreadable>"]
    found: list[str] = []
    for label in ("user", "host", "uid"):
        if re.search(r"\b" + re.escape(who[label]) + r"\b", source, re.IGNORECASE):
            found.append(label)
    # The home path is matched as a substring: it carries separators, so word
    # boundaries would be the wrong instrument.
    if who["home"] in source:
        found.append("home")
    return found


def is_text(path: Path) -> bool:
    """Sniffed, not guessed from the suffix. V3's allowlist skipped
    `MANIFEST.sha256` and every extensionless file."""
    try:
        head = path.read_bytes()[:8192]
    except OSError:
        return False
    if b"\x00" in head:
        return False
    try:
        head.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def members(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file():
            yield path


def normalize(root: Path, table) -> tuple[int, int]:
    touched = 0
    applied = 0
    for path in members(root):
        if path.name == "MANIFEST.sha256" or not is_text(path):
            continue
        original = path.read_text(encoding="utf-8")
        text = original
        for pattern, replacement in table:
            text, count = pattern.subn(replacement, text)
            applied += count
        if text != original:
            path.write_text(text, encoding="utf-8")
            touched += 1
    return touched, applied


def scan(root: Path, checks) -> list[str]:
    hits: list[str] = []
    for path in members(root):
        relative = path.relative_to(root).as_posix()
        for label, pattern in checks:
            # THE NAME IS SCANNED TOO. V3 examined contents only.
            if pattern.search(relative):
                hits.append(f"{relative}: [name/{label}]")
        if not is_text(path):
            continue
        for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1):
            for label, pattern in checks:
                found = pattern.search(line)
                if found:
                    hits.append(f"{relative}:{number}: [{label}] {found.group(0)!r}")
    return hits


def index_check(root: Path) -> list[str]:
    """Every path a markdown file names must resolve inside the package."""
    # Not a package reference: absolute system paths, repository-relative
    # source paths, git refs, URLs, placeholders, and anything carrying an `=`
    # or a `:line` suffix. V3's check accepted any file anywhere in the package
    # with a matching basename, so a wrong-directory reference passed; this one
    # resolves the path as written, and simply does not claim jurisdiction over
    # things that were never package members.
    external = re.compile(r"^(?:https?:|mailto:|#|/|\$REPO|\$HOME|\$SCRATCH|src/|"
                          r"tools/|scripts/|guidance/|build/|release/|web/|pdf/|"
                          r"impl/|review/|evidence/|origin/|refs/)")
    missing: list[str] = []
    for path in sorted(root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        named = set(re.findall(r"\[[^\]]*\]\(([^)]+)\)", text))
        named |= {one for one in re.findall(r"`([^`]+)`", text)
                  if "/" in one and not one.endswith("/") and " " not in one}
        for one in sorted(named):
            if external.match(one) or one.startswith("<") or "=" in one:
                continue
            if re.search(r":\d+$", one):
                continue
            if not (root / one).exists() and not (path.parent / one).exists():
                missing.append(f"{path.relative_to(root).as_posix()} -> {one}")
    return missing


def manifest(root: Path) -> int:
    target = root / "MANIFEST.sha256"
    if target.exists():
        target.unlink()
    rows = []
    for path in members(root):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(root).as_posix()}")
    target.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("package", type=Path)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args(argv)
    root = args.package.resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    who = identities()
    where = repo_root()

    # THE SELF-CHECK, BEFORE ANY WRITE. A private value hard-coded into this
    # file's patterns is the one defect that makes every number this tool
    # prints meaningless. Nothing is normalized, and no manifest is written,
    # while that is true. Silent on success: the stdout shapes are quoted
    # verbatim elsewhere and must not gain a line.
    blind = own_source_literals(who)
    if blind:
        print("REFUSING TO SEAL: this file contains a private value as a "
              f"literal ({', '.join(blind)}); it cannot see its own leak.",
              file=sys.stderr)
        return 1

    if not args.check_only:
        touched, applied = normalize(root, rules(who, where))
        # V3 printed `normalized 0` and read it as a pass. It is ambiguous
        # between "already clean" and "patterns broken", so both numbers are
        # reported and the distinction is stated.
        print(f"normalized {touched} file(s), {applied} substitution(s)")
        if touched == 0:
            print("  (no file changed: inputs were already normalized, or the "
                  "rules matched nothing -- the scan below is what decides)")

    hits = scan(root, forbidden(who, where))
    print(f"sanitization scan: {len(hits)} private-token hit(s)")
    for hit in hits[:50]:
        print(f"  {hit}")

    missing = index_check(root)
    print(f"evidence-index check: {len(missing)} missing reference(s)")
    for one in missing[:50]:
        print(f"  {one}")

    # THE HARD GATE. V3 wrote the manifest regardless.
    if hits:
        print("REFUSING TO SEAL: private tokens are still present.", file=sys.stderr)
        return 1
    if missing:
        print("REFUSING TO SEAL: the evidence index is incomplete.", file=sys.stderr)
        return 1

    if not args.check_only:
        count = manifest(root)
        print(f"MANIFEST.sha256 written: {count} file(s) covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
