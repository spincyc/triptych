#!/usr/bin/env python3
"""Prove the shipped ZIP against every claim the package makes about itself.

WHY THIS EXISTS. The V8 pipeline's last word was `sanitize-and-seal.py
--verify`, which proved the ZIP against the manifest and the manifest against
the tree — and never opened `claims.json`. So an inventory captured at step 9
of a 14-step pipeline shipped with five rows describing bytes that steps 9-11
had already rewritten, 1,822 bytes short of the truth, and every mechanical
check still passed. The verification and the claims never met.

THIS IS P8, AND IT IS THE MEETING. It runs strictly READ-ONLY, from the final
ZIP alone — the artifact a reviewer actually receives, not the tree it was
built from — and its transcript is written OUTSIDE the package, because a
file created after the seal is not in the manifest that seal produced.

THE TRANSCRIPT IS BOUND TO THE ARCHIVE IT PROVES. Before the first check it
prints the ZIP's exact basename, byte size and sha256 — computed from the
archive bytes themselves, not read from the sidecar — the expected package
root, and a UTC verification timestamp. The V9 transcript carried none of
these, so it would have read identically for any other archive whose sidecar
happened to agree with it. Seven checks, in order:

  1. SIDECAR.    The ZIP's sha256 AND its byte size against the recorded
                 sidecar values. Size too: a truncated download that happens
                 to collide on nothing is still not the artifact.
  2. LAYOUT.     Exactly one top-level root, equal to the package name; no
                 duplicate entries, no absolute paths, no `..` segments.
  3. MANIFEST.   The extracted set minus `MANIFEST.sha256` equals the
                 manifest rows, and every digest matches. A path listed twice
                 in the manifest is a named failure — independent of the
                 duplicate-archive-entry check in 2, because a duplicate row
                 collapses silently into a dict and then proves half of what
                 it appears to.
  4. ROWS.       Every `claims.json` row matches the extracted member's bytes
                 and sha256, `evidence_bytes` is their sum and
                 `evidence_members` their count. A path frozen twice is a
                 named failure here for the same reason as in 3. A row that
                 fails otherwise is the V8 defect: a size claimed before the
                 last write.
  5. PARTITION.  rows ∪ derived_members is exactly the member set, the
                 intersection is empty, and no derived member carries a size
                 or digest — named, never sized, is the contract.
  6. RENDERING.  `DERIVED-CLAIMS.md` re-rendered from the extracted
                 `claims.json` with the SHIPPED renderer, byte-compared.
  7. AUDITS.     The shipped `head-consistency.py` and the shipped sanitizer's
                 `--check-only`, re-run over the extraction, both clean.

Between checks 5 and 6 the transcript prints the final-byte arithmetic,
derived from the extraction alone: the final member count, each derived
member's final byte size and their sum, the frozen-rows byte total, and the
total uncompressed bytes — so the transcript itself carries the figures the
V9 verifier left for a reader to compute.

Every check runs even after an earlier one fails, so one transcript names
every problem rather than the first. Nothing here writes anywhere except a
temporary extraction directory that is removed on exit; running it twice on
the same ZIP is the same run twice, which a reviewer can and should confirm
(the header's timestamp is the one line that moves).

Usage:
    verify-final-package.py --zip PACKAGE.zip [--sidecar PACKAGE.zip.sha256]
                            [--name PACKAGE_NAME]
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# READ-ONLY includes the extraction: this tool imports the shipped renderer
# from the extracted tree (check 6), and an import that writes bytecode would
# plant a `__pycache__` member the partition and audit re-runs then trip over.
sys.dont_write_bytecode = True

MANIFEST_NAME = "MANIFEST.sha256"


def digest(path: Path) -> str:
    hashed = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hashed.update(block)
    return hashed.hexdigest()


def load_tool(root: Path, name: str, alias: str):
    """A shipped tool, as a module. THE SHIPPED ONE: importing the copy from
    anywhere else would verify a renderer nobody received."""
    location = root / "logs" / name
    spec = importlib.util.spec_from_file_location(alias, location)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load the shipped tool: {location}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# The checks. Each returns problems; none stops the others. They are module-
# level functions on purpose: the test suite drives each one against a crafted
# failure so that "the verifier would catch it" is a pinned fact, not a hope.
# ---------------------------------------------------------------------------


def identity_header(archive: Path, expected_root: str,
                    hashed: str) -> list[str]:
    """The binding. Every `ok` below is about THESE bytes: the basename, the
    exact size, the sha256 computed from the archive itself, the root the
    layout check will demand, and when the run happened. A transcript without
    this header proves an archive; it just cannot say which one."""
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return [
        "== P8 final verification, bound to the exact archive",
        f"   archive : {archive.name}",
        f"   bytes   : {archive.stat().st_size}",
        f"   sha256  : {hashed}",
        f"   root    : {expected_root}",
        f"   verified: {stamp} (UTC)",
    ]


def parse_sidecar(text: str) -> tuple[str, int | None]:
    """The recorded digest and byte size. The first line stays `sha256sum`
    format so `sha256sum -c` keeps working; the size is its own line."""
    found = re.search(r"\b([0-9a-fA-F]{64})\b", text)
    recorded = found.group(1).lower() if found else ""
    sized = re.search(r"^(\d+) bytes\b", text, re.M)
    return recorded, int(sized.group(1)) if sized else None


def check_sidecar(archive: Path, sidecar: Path,
                  actual_digest: str | None = None) -> list[str]:
    """Check 1: the bytes a reviewer holds are the bytes that were sealed.
    The digest is computed once, in the header, and handed in; recomputing it
    here would let the header and the check describe different reads."""
    problems: list[str] = []
    if not sidecar.is_file():
        return [f"no sidecar: {sidecar.name}"]
    recorded, size = parse_sidecar(sidecar.read_text(encoding="utf-8"))
    if not recorded:
        problems.append(f"{sidecar.name} records no sha256")
    elif recorded != (actual_digest or digest(archive)):
        problems.append(f"archive sha256 does not match {sidecar.name}")
    actual = archive.stat().st_size
    if size is None:
        problems.append(f"{sidecar.name} records no byte size")
    elif size != actual:
        problems.append(f"archive is {actual} bytes; {sidecar.name} "
                        f"records {size}")
    return problems


def check_layout(names: list[str], expected_root: str) -> list[str]:
    """Check 2: one root, no duplicates, no path that escapes extraction."""
    problems: list[str] = []
    if len(names) != len(set(names)):
        seen: set[str] = set()
        for one in names:
            if one in seen:
                problems.append(f"duplicate archive entry: {one}")
            seen.add(one)
    roots = {one.split("/", 1)[0] for one in names}
    if roots != {expected_root}:
        problems.append(f"top-level entries {sorted(roots)}; expected exactly "
                        f"['{expected_root}']")
    for one in names:
        if one.startswith("/") or re.match(r"^[A-Za-z]:", one):
            problems.append(f"absolute archive path: {one}")
        if ".." in one.split("/"):
            problems.append(f"parent-escaping archive path: {one}")
    return problems


def check_manifest(root: Path) -> list[str]:
    """Check 3: extracted set minus the manifest == the manifest, digest by
    digest. This is what `--verify` already proved of the TREE; here it is
    proved of what the ZIP actually delivered."""
    problems: list[str] = []
    target = root / MANIFEST_NAME
    if not target.is_file():
        return [f"the archive carries no {MANIFEST_NAME}"]
    listed: dict[str, str] = {}
    for number, line in enumerate(
            target.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        found = re.match(r"^([0-9a-fA-F]{64})\s\s?(.+)$", line)
        if not found:
            problems.append(f"malformed manifest line {number}: {line!r}")
            continue
        # A path listed twice collapses into one dict key below and the rest
        # of the check then proves half of what the manifest appears to say.
        if found.group(2) in listed:
            problems.append(f"duplicate manifest row: {found.group(2)}")
        listed[found.group(2)] = found.group(1).lower()
    present = {one.relative_to(root).as_posix()
               for one in sorted(root.rglob("*")) if one.is_file()}
    for one in sorted(set(listed) - present):
        problems.append(f"manifest lists {one}, which the archive omits")
    for one in sorted(present - set(listed) - {MANIFEST_NAME}):
        problems.append(f"archive carries {one}, which the manifest does "
                        f"not list")
    for one in sorted(set(listed) & present):
        if digest(root / one) != listed[one]:
            problems.append(f"digest mismatch against the manifest: {one}")
    return problems


def check_claims_rows(claims: dict, root: Path) -> list[str]:
    """Check 4: every frozen row against the delivered bytes. A failing row is
    THE defect this protocol exists to make impossible: a (bytes, sha256)
    computed before the last write of the bytes it claims."""
    problems: list[str] = []
    package = claims["package"]
    rows = package["rows"]
    # A path frozen twice would double-count in evidence_bytes and let two
    # rows disagree about one member; named here, independently of check 2's
    # duplicate archive entries.
    seen: set[str] = set()
    for one in rows:
        if one["path"] in seen:
            problems.append(f"duplicate claims row: {one['path']}")
        seen.add(one["path"])
    for one in rows:
        path = root / one["path"]
        if not path.is_file():
            problems.append(f"claims row {one['path']}: not in the archive")
            continue
        if path.stat().st_size != one["bytes"]:
            problems.append(f"claims row {one['path']}: claims {one['bytes']} "
                            f"bytes, archive delivers "
                            f"{path.stat().st_size} -- a stale row")
        elif digest(path) != one["sha256"]:
            problems.append(f"claims row {one['path']}: sha256 does not match "
                            f"the delivered bytes -- a stale row")
    total = sum(one["bytes"] for one in rows)
    if package.get("evidence_bytes") != total:
        problems.append(f"evidence_bytes says {package.get('evidence_bytes')}; "
                        f"the rows sum to {total}")
    if package.get("evidence_members") != len(rows):
        problems.append(f"evidence_members says "
                        f"{package.get('evidence_members')}; there are "
                        f"{len(rows)} rows")
    return problems


def check_partition(claims: dict, root: Path) -> list[str]:
    """Check 5: rows ∪ derived_members is the member set, exactly, and a
    derived member is a name and a reason -- never a size, never a hash."""
    problems: list[str] = []
    package = claims["package"]
    frozen = {one["path"] for one in package["rows"]}
    derived_rows = package.get("derived_members") or []
    derived = {one["path"] for one in derived_rows}
    for one in derived_rows:
        extra = sorted(set(one) - {"path", "reason"})
        if extra:
            problems.append(f"derived member {one.get('path', '?')} carries "
                            f"{', '.join(extra)}: named, never sized")
    present = {one.relative_to(root).as_posix()
               for one in sorted(root.rglob("*")) if one.is_file()}
    for one in sorted(frozen & derived):
        problems.append(f"{one} is both a frozen row and a derived member")
    for one in sorted(present - frozen - derived):
        problems.append(f"{one} is in the archive but in neither rows nor "
                        f"derived_members")
    for one in sorted((frozen | derived) - present):
        problems.append(f"{one} is claimed (row or derived) but not in the "
                        f"archive")
    return problems


def final_bytes(claims: dict, root: Path) -> list[str]:
    """The final-byte arithmetic, derived from the extraction alone. The
    frozen rows carry their own total by construction; the derived members
    are named-never-sized in claims.json, so their FINAL sizes exist nowhere
    until somebody measures the delivered bytes — this is where. Reporting,
    not a check: any disagreement is already a partition or rows failure."""
    package = claims["package"]
    rows = package.get("rows") or []
    frozen_total = sum(one["bytes"] for one in rows)
    present = sorted(one for one in root.rglob("*") if one.is_file())
    total = sum(one.stat().st_size for one in present)
    lines = [
        "--- final bytes, derived from the archive alone",
        f"    members            : {len(present)}",
        f"    frozen rows        : {len(rows)} row(s), {frozen_total} bytes",
    ]
    derived_rows = package.get("derived_members") or []
    derived_total = 0
    for one in derived_rows:
        path = root / one["path"]
        if path.is_file():
            derived_total += path.stat().st_size
            lines.append(f"    derived {one['path']}: "
                         f"{path.stat().st_size} bytes")
        else:
            lines.append(f"    derived {one['path']}: (absent)")
    lines.append(f"    derived members    : {len(derived_rows)} member(s), "
                 f"{derived_total} bytes")
    summed = frozen_total + derived_total
    closing = (f"    total uncompressed : {total} bytes across "
               f"{len(present)} member(s)")
    if summed == total:
        closing += f" (= frozen {frozen_total} + derived {derived_total})"
    else:
        closing += (f"; frozen {frozen_total} + derived {derived_total} = "
                    f"{summed}, which does not add up -- see the partition "
                    f"check")
    lines.append(closing)
    return lines


def check_rendering(root: Path) -> list[str]:
    """Check 6: the shipped renderer, over the shipped claims, must reproduce
    the shipped page byte for byte. Two records of one fact, proved one."""
    try:
        deriver = load_tool(root, "derive-claims.py", "shipped_deriver")
    except (SystemExit, Exception) as error:  # noqa: BLE001 -- report, don't die
        return [f"cannot load the shipped renderer: {error}"]
    claims = json.loads((root / "claims.json").read_text(encoding="utf-8"))
    rendered = deriver.render(claims)
    shipped = (root / "DERIVED-CLAIMS.md").read_text(encoding="utf-8")
    if rendered != shipped:
        return ["DERIVED-CLAIMS.md does not re-render byte-identically from "
                "the shipped claims.json"]
    return []


def check_shipped_audits(root: Path) -> list[str]:
    """Check 7: the package's own auditors, replayed over the extraction.

    Run with the extraction as the working directory so the sanitizer's
    repo-root rule keys on nothing: what is being asked is whether the
    DELIVERED bytes are clean and consistent, on any machine."""
    problems: list[str] = []
    for label, command in (
            ("head-consistency",
             [sys.executable, str(root / "logs" / "head-consistency.py"),
              "--package", str(root)]),
            ("sanitizer check-only",
             [sys.executable, str(root / "logs" / "sanitize-and-seal.py"),
              str(root), "--check-only"])):
        done = subprocess.run(command, capture_output=True, text=True,
                              cwd=root)
        print(f"--- {label} over the extraction (exit {done.returncode})")
        sys.stdout.write(done.stdout)
        sys.stderr.write(done.stderr)
        if done.returncode != 0:
            problems.append(f"{label} fails over the extracted archive")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--zip", type=Path, required=True, dest="archive")
    parser.add_argument("--sidecar", type=Path, default=None)
    parser.add_argument("--name", default=None,
                        help="expected package root inside the archive "
                             "(default: the ZIP's own stem)")
    args = parser.parse_args(argv)

    archive = args.archive.resolve()
    if not archive.is_file():
        print(f"no such archive: {archive}", file=sys.stderr)
        return 2
    sidecar = args.sidecar or archive.with_name(archive.name + ".sha256")
    expected_root = args.name or archive.name.removesuffix(".zip")

    # THE BINDING, before the first check: the digest is computed here, from
    # the archive bytes themselves, and the sidecar check receives it rather
    # than reading twice.
    actual_digest = digest(archive)
    for line in identity_header(archive, expected_root, actual_digest):
        print(line)

    failed: list[str] = []

    def outcome(label: str, problems: list[str]) -> None:
        print(f"[{label}] {'ok' if not problems else 'FAILED'}"
              + (f" -- {len(problems)} problem(s)" if problems else ""))
        for one in problems:
            print(f"    {one}")
        failed.extend(problems)

    outcome("1 sidecar", check_sidecar(archive, sidecar, actual_digest))

    try:
        with zipfile.ZipFile(archive) as handle:
            names = [one.filename for one in handle.infolist()
                     if not one.is_dir()]
            layout = check_layout(names, expected_root)
            outcome("2 layout", layout)
            if any("path" in one for one in layout):
                # A path that could escape the extraction directory is the one
                # problem that makes extracting unsafe; everything below needs
                # the extraction, so this is the single early exit.
                print("REFUSING to extract an archive with escaping paths.",
                      file=sys.stderr)
                return 1
            with tempfile.TemporaryDirectory() as scratch:
                handle.extractall(scratch)
                root = Path(scratch) / expected_root
                if not root.is_dir():
                    outcome("3 manifest",
                            [f"no {expected_root}/ directory in the archive"])
                else:
                    outcome("3 manifest", check_manifest(root))
                    claims_path = root / "claims.json"
                    if not claims_path.is_file():
                        outcome("4 claims rows",
                                ["the archive carries no claims.json"])
                    else:
                        claims = json.loads(
                            claims_path.read_text(encoding="utf-8"))
                        outcome("4 claims rows",
                                check_claims_rows(claims, root))
                        outcome("5 partition", check_partition(claims, root))
                        for line in final_bytes(claims, root):
                            print(line)
                    outcome("6 rendering", check_rendering(root))
                    outcome("7 shipped audits", check_shipped_audits(root))
    except zipfile.BadZipFile as error:
        outcome("2 layout", [f"archive unreadable: {error}"])

    print(f"P8 verification: {'PASS' if not failed else 'FAIL'} "
          f"({len(failed)} problem(s))")
    if failed:
        print("P8 VERIFICATION FAILED: the shipped archive does not prove "
              "its own claims.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
