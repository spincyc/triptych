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
    # The V3 MISS: the account name as a free-standing token.
    made.append((re.compile(r"\b" + user + r"\b", re.IGNORECASE), PLACEHOLDER_USER))
    made.append((re.compile(r"\b" + host + r"(\.local)?\b", re.IGNORECASE),
                 PLACEHOLDER_HOST))
    made.append((re.compile(r"\b:\d+\.\d+\b"), " " + PLACEHOLDER_DBUS))
    made.append((re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
                            r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"), PLACEHOLDER_UUID))
    made.append((re.compile(r"\b(?:127\.0\.0\.1|localhost):\d+\b"),
                 PLACEHOLDER_HOST + ":<port>"))
    made.append((re.compile(r"\b(?:10|192\.168|172\.(?:1[6-9]|2\d|3[01]))"
                            r"(?:\.\d{1,3}){2,3}\b"), "<ip>"))
    made.append((re.compile(r"[+-]\d{2}:\d{2}\b"), PLACEHOLDER_TZ))
    made.append((re.compile(r"\b(?:America|Europe|Asia|Africa|Australia|Pacific)"
                            r"/[A-Za-z_]+\b"), PLACEHOLDER_TZ))
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
        ("dbus-name", re.compile(r"(?<![\w.])[:]\d+\.\d+\b")),
        ("uuid", re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
                            r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")),
        ("scratch-dir", re.compile(r"/tmp/[A-Za-z0-9._-]*claude")),
        ("loopback", re.compile(r"\b(?:127\.0\.0\.1|localhost):\d+\b")),
        ("iana-timezone", re.compile(r"\b(?:America|Europe|Asia|Africa|Australia"
                                     r"|Pacific)/[A-Za-z_]+\b")),
        ("utc-offset", re.compile(r"\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}")),
    ]
    if root:
        made.append(("repo-path", re.compile(re.escape(root))))
    return made


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
