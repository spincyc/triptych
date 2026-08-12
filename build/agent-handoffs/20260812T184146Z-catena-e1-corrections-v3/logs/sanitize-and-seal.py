#!/usr/bin/env python3
"""Sanitize, index-check, manifest and seal an external-review handoff package.

Usage:
  sanitize-and-seal.py PACKAGE_DIR [--check-only]

Runs, in order:
  1. Normalization of text artifacts: machine-private absolute paths, the
     account name, loopback hosts and ephemeral ports become portable
     placeholders ($REPO, $HANDOFF, <USER>, <HOST>, <PORT>).
  2. A sanitization scan that FAILS if any private token survives anywhere
     in the package (text or binary-named text artifacts).
  3. An evidence-index completeness check: every path referenced by a
     Markdown link, backtick path, or bare artifact filename inside the
     package's Markdown files must resolve to a file that exists in the
     package. Zero missing references is required (directions §27).
  4. MANIFEST.sha256 covering every file except itself, written last.

Exit 0 only when sanitization and the index check both pass. --check-only
skips normalization and manifest writing (audit an already-sealed package).
"""

from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path

# Tokens that must never appear in a package. Each is (pattern, replacement).
PRIVATE = [
    (re.compile(r"/home/[A-Za-z0-9._-]+/git/worktrees/triptych/e1-catena-v3/spincyc/triptych"), "$REPO"),
    (re.compile(r"/home/[A-Za-z0-9._-]+/git/claude/triptych-e1-correction-2"), "$REPO_V2"),
    (re.compile(r"/home/[A-Za-z0-9._-]+/git/claude/triptych-e1-baseline"), "$REPO_BASELINE"),
    (re.compile(r"/home/[A-Za-z0-9._-]+/git/claude/triptych-e1-correction\b"), "$REPO_V1"),
    (re.compile(r"/home/[A-Za-z0-9._-]+/git/claude/triptych\b"), "$REPO_MAIN"),
    (re.compile(r"/tmp/claude-\d+/[^\s\"'>)\]]*"), "$SCRATCH"),
    (re.compile(r"/home/[A-Za-z0-9._-]+"), "$HOME"),
    (re.compile(r"/Users/[A-Za-z0-9._-]+"), "$HOME"),
    (re.compile(r"\bhttp://(?:localhost|127\.0\.0\.1)(?::\d+)?"), "http://<HOST>:<PORT>"),
    (re.compile(r"\b(?:localhost|127\.0\.0\.1):\d+"), "<HOST>:<PORT>"),
    (re.compile(r"\bport\s+\d{4,5}\b", re.I), "port <PORT>"),
]

# After normalization, none of these may survive. (Bare "localhost" without a
# port is permitted only inside a documented startup command, so the scan
# looks for the private forms: user paths, loopback with a port, /tmp scratch.)
FORBIDDEN = [
    re.compile(r"/home/[A-Za-z0-9._-]+"),
    re.compile(r"/Users/[A-Za-z0-9._-]+"),
    re.compile(r"127\.0\.0\.1"),
    re.compile(r"localhost:\d+"),
    re.compile(r"/tmp/claude-\d+"),
]

TEXT_SUFFIXES = {".md", ".txt", ".log", ".json", ".patch", ".csv", ".mjs", ".py", ".sh", ".html"}


def text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def normalize(root: Path) -> list[str]:
    changed = []
    for path in text_files(root):
        raw = path.read_text(encoding="utf-8", errors="replace")
        out = raw
        for pattern, replacement in PRIVATE:
            out = pattern.sub(replacement, out)
        if out != raw:
            path.write_text(out, encoding="utf-8")
            changed.append(str(path.relative_to(root)))
    return changed


def scan(root: Path) -> list[str]:
    hits = []
    for path in text_files(root):
        raw = path.read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(raw.splitlines(), 1):
            for pattern in FORBIDDEN:
                found = pattern.search(line)
                if found:
                    hits.append(f"{path.relative_to(root)}:{number}: {found.group(0)}")
    return hits


REFERENCE = re.compile(
    r"(?:\]\((?P<link>[^)\s]+)\)"                      # markdown link target
    r"|`(?P<tick>[A-Za-z0-9._/-]+\.[A-Za-z0-9]{2,5})`"  # backticked path
    r"|(?P<bare>\b[A-Za-z0-9._-]+\.(?:png|pdf|json|log|txt|patch|mjs|py|sha256)\b))"
)

# References that are repository paths or external URLs, not package artifacts.
EXTERNAL = re.compile(r"^(?:https?:|mailto:|#|\$|src/|tools/|guidance/|release/|scripts/|"
                      r"build/|Makefile|PROJECT-WORK\.md|promised-deliverables\.toml)")


def index_check(root: Path) -> list[str]:
    missing = []
    for path in sorted(root.rglob("*.md")):
        raw = path.read_text(encoding="utf-8", errors="replace")
        for match in REFERENCE.finditer(raw):
            target = match.group("link") or match.group("tick") or match.group("bare")
            if not target or EXTERNAL.match(target):
                continue
            if target.endswith("/"):
                continue
            candidates = [root / target, path.parent / target]
            if any(one.exists() for one in candidates):
                continue
            # A bare filename may live anywhere in the package.
            if any(one.name == Path(target).name for one in root.rglob("*")):
                continue
            missing.append(f"{path.relative_to(root)}: {target}")
    return missing


def manifest(root: Path) -> int:
    target = root / "MANIFEST.sha256"
    if target.exists():
        target.unlink()
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            rows.append(f"{digest}  {path.relative_to(root)}")
    target.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(rows)


def main(argv: list[str]) -> int:
    if not argv:
        sys.exit(__doc__)
    root = Path(argv[0]).resolve()
    check_only = "--check-only" in argv
    if not root.is_dir():
        print(f"not a directory: {root}")
        return 1

    if not check_only:
        changed = normalize(root)
        print(f"normalized {len(changed)} text artifact(s)")
        for one in changed:
            print(f"  normalized: {one}")

    hits = scan(root)
    print(f"sanitization scan: {len(hits)} private-token hit(s)")
    for one in hits[:40]:
        print(f"  LEAK {one}")

    missing = index_check(root)
    print(f"evidence-index check: {len(missing)} missing reference(s)")
    for one in missing[:40]:
        print(f"  MISSING {one}")

    if not check_only:
        count = manifest(root)
        print(f"MANIFEST.sha256 written: {count} file(s) covered")

    return 0 if not hits and not missing else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
