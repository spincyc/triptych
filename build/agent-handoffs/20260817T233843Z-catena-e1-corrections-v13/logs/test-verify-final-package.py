#!/usr/bin/env python3
"""THE P8 GATE, DRIVEN AT EVERY WAY A ZIP CAN LIE ABOUT ITSELF.

A gate that has only ever been run against a package that passes is a gate
nobody has seen refuse. Each test here builds an archive that is wrong in
exactly one way and asserts that the gate names THAT way -- and the first one
builds the archive that is right and asserts that the gate is silent, so the
refusals below are not simply a tool that always fails.

The malformed archives are built by writing BYTES, never by shelling out to
`zip`: the defects under test -- a prepended prefix, a trailing tail, an
end-of-central-directory record that miscounts, a local file header that
disagrees with its central directory entry -- are precisely the defects no
archiver will produce for you, which is why `zipfile` tolerating them went
unnoticed for four package revisions.

The trust anchor is a directory of STUB tools built into the fixture. That is
the correct anchor for a unit test: this gate's contract is "run the trusted
copy, hash the shipped one, and compare", and a stub proves the plumbing
without dragging the whole Catena toolchain into a temporary directory.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "verify-final-package.py"

NAME = "20260817T000000Z-catena-e1-corrections-v13"
HEAD = "1111111111111111111111111111111111111111"
PARENT = "2222222222222222222222222222222222222222"
ATTEMPT = "package-20260817T000000Z-03abcdef"
MARKER = "CORRUPT-ME-MARKER"

# The renderer the gate IMPORTS from the trust anchor. Deliberately tiny and
# deliberately claims-dependent, so a fixture that changes its row count and
# forgets to re-render is caught by the gate rather than by luck.
RENDERER_STUB = '''#!/usr/bin/env python3
"""A trusted renderer stub."""


def render(claims):
    return "DERIVED %d row(s)\\n" % len(claims["package"]["rows"])
'''

# The auditors the gate EXECUTES from the trust anchor, as subprocesses.
AUDITOR_STUB = '''#!/usr/bin/env python3
"""A trusted auditor stub: it reads its arguments and is satisfied."""
import sys

sys.exit(0)
'''

TOOL_SOURCES = {
    "derive-claims.py": RENDERER_STUB,
    "head-consistency.py": AUDITOR_STUB,
    "sanitize-and-seal.py": AUDITOR_STUB,
    "checks.py": AUDITOR_STUB,
    "assemble.sh": "#!/bin/sh\n# a trusted assembler stub\nexit 0\n",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Gate(unittest.TestCase):

    # -- fixtures ------------------------------------------------------

    def build_tree(self, evidence: bytes | None = None):
        """One correct package on disk, plus the trusted tool anchor.

        Returns (base, package directory, tools directory). Everything under
        `base` is removed on cleanup; nothing outside it is touched.
        """
        base = Path(tempfile.mkdtemp(prefix="p8-"))
        self.addCleanup(shutil.rmtree, base, ignore_errors=True)

        tools = base / "trusted"
        tools.mkdir()
        for name, source in TOOL_SOURCES.items():
            (tools / name).write_text(source, encoding="utf-8")

        package = base / NAME
        (package / "logs").mkdir(parents=True)
        (package / "evidence.txt").write_bytes(
            evidence if evidence is not None
            else f"the evidence, {MARKER}\n".encode("utf-8"))
        for name, source in TOOL_SOURCES.items():
            (package / "logs" / name).write_text(source, encoding="utf-8")

        # The frozen rows: everything whose bytes were settled before the
        # claims were taken. The derived members are named, never sized.
        rows = []
        for one in sorted(package.rglob("*")):
            if not one.is_file():
                continue
            relative = one.relative_to(package).as_posix()
            data = one.read_bytes()
            rows.append({"path": relative, "bytes": len(data),
                         "sha256": sha256(data)})
        claims = {
            "lane": "catena-e1",
            "tool": "test-verify-final-package.py",
            "identity": {"head": HEAD, "parent": PARENT,
                         "review_addressed": "V12 CHANGES REQUIRED"},
            "package": {
                "rows": rows,
                "evidence_bytes": sum(one["bytes"] for one in rows),
                "evidence_members": len(rows),
                "derived_members": [
                    {"path": "claims.json",
                     "reason": "written after the rows were frozen"},
                    {"path": "DERIVED-CLAIMS.md",
                     "reason": "rendered from claims.json"},
                    {"path": "MANIFEST.sha256",
                     "reason": "written by the sealer, over everything else"},
                ],
            },
        }
        (package / "claims.json").write_text(
            json.dumps(claims, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        (package / "DERIVED-CLAIMS.md").write_text(
            "DERIVED %d row(s)\n" % len(rows), encoding="utf-8")

        manifest = []
        for one in sorted(package.rglob("*")):
            if one.is_file():
                manifest.append(
                    f"{sha256(one.read_bytes())}  "
                    f"{one.relative_to(package).as_posix()}")
        (package / "MANIFEST.sha256").write_text(
            "\n".join(manifest) + "\n", encoding="utf-8")
        return base, package, tools

    def build_zip(self, base: Path, package: Path,
                  duplicate: str | None = None) -> Path:
        """The package, sealed. STORED on purpose: every test below that
        edits the archive edits bytes it can find."""
        archive = base / f"{NAME}.zip"
        members = sorted(one for one in package.rglob("*") if one.is_file())
        with warnings.catch_warnings():
            # The duplicate below is the point of one test; `zipfile` warning
            # about it would only make a passing suite look alarming.
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_STORED) as handle:
                for one in members:
                    arcname = f"{NAME}/{one.relative_to(package).as_posix()}"
                    handle.writestr(arcname, one.read_bytes())
                    if duplicate and arcname.endswith(duplicate):
                        handle.writestr(arcname, one.read_bytes())
        self.write_sidecar(archive)
        return archive

    def write_sidecar(self, archive: Path) -> None:
        data = archive.read_bytes()
        archive.with_name(archive.name + ".sha256").write_text(
            f"{sha256(data)}  {archive.name}\n{len(data)} bytes\n",
            encoding="utf-8")

    def executed_record(self, package: Path, base: Path,
                        omit: str | None = None,
                        wrong: str | None = None,
                        **override) -> Path:
        """The contemporaneous execution record the assembler must write."""
        runs = []
        for name in sorted(TOOL_SOURCES):
            if name == omit:
                continue
            data = (package / "logs" / name).read_bytes()
            recorded = sha256(data)
            if name == wrong:
                recorded = sha256(data + b"drift")
            runs.append({
                "tool": name,
                "path": f"logs/{name}",
                "attempt": ATTEMPT,
                "sha256": recorded,
                "at": "2026-08-17T19:45:20Z",
                "phase": f"P1 {name}",
                "log": "logs/attempt-05/seal.log",
                "class": "shipped-executed",
            })
        record = {"schema": "catena-executed-tools/1", "attempt": ATTEMPT,
                  "anchor": "$EVIDENCE", "runs": runs}
        record.update(override)
        path = base / f"{NAME}.zip.executed-tools.json"
        path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
        return path

    # -- the driver ----------------------------------------------------

    def run_gate(self, archive: Path, tools: Path, executed: Path | None = None,
                 table_out: Path | None = None, accept: bool = True):
        command = [sys.executable, "-B", str(GATE), "--zip", str(archive),
                   "--tools", str(tools)]
        if executed is not None:
            command += ["--executed", str(executed)]
        if table_out is not None:
            command += ["--table-out", str(table_out)]
        if accept:
            command.append("--accept-unversioned-tools")
        done = subprocess.run(
            command, capture_output=True, text=True,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        return done.returncode, done.stdout + done.stderr

    def sound(self):
        base, package, tools = self.build_tree()
        archive = self.build_zip(base, package)
        return base, package, tools, archive

    # -- the control ---------------------------------------------------

    def test_a_well_formed_package_passes(self):
        # WITHOUT THIS EVERY REFUSAL BELOW IS VACUOUS.
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 0, said)
        self.assertIn("P8 verification: PASS (0 problem(s))", said)
        self.assertIn("[3 structure] ok", said)
        self.assertIn("[4 crc] ok", said)
        self.assertIn("[11 tool bytes] ok", said)
        self.assertIn("checks skipped   : (none)", said)

    # -- check 4: the CRC-32 that was never explicitly checked ----------

    def test_a_corrupted_member_crc_is_a_crc_problem_not_a_layout_problem(self):
        base, package, tools, archive = self.sound()
        data = bytearray(archive.read_bytes())
        at = data.index(MARKER.encode("utf-8"))
        data[at] = data[at] ^ 0x20  # one bit, inside a member's stored bytes
        archive.write_bytes(bytes(data))
        self.write_sidecar(archive)
        executed = self.executed_record(package, base)
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("CRC-32 mismatch for", said)
        self.assertIn("[4 crc] FAILED", said)
        # THE MISATTRIBUTION THIS REPLACES: V12 reported this under layout.
        self.assertIn("[2 layout] ok", said)
        self.assertNotIn("archive unreadable", said)

    def test_a_failed_extraction_is_reported_and_the_skips_are_accounted(self):
        base, package, tools, archive = self.sound()
        data = bytearray(archive.read_bytes())
        at = data.index(MARKER.encode("utf-8"))
        data[at] = data[at] ^ 0x20
        archive.write_bytes(bytes(data))
        self.write_sidecar(archive)
        code, said = self.run_gate(archive, tools)
        self.assertEqual(code, 1, said)
        self.assertIn("[5 extraction] FAILED", said)
        self.assertIn("the archive does not extract", said)
        for label in ("6 manifest", "7 claims rows", "8 partition",
                      "9 rendering", "10 shipped audits"):
            self.assertIn(f"[{label}] SKIPPED", said)
        self.assertIn("checks skipped   : 6 manifest, 7 claims rows, "
                      "8 partition, 9 rendering, 10 shipped audits", said)

    # -- check 3: the bytes nobody counted ------------------------------

    def test_appended_trailing_bytes_are_refused(self):
        base, package, tools, archive = self.sound()
        with archive.open("ab") as handle:
            handle.write(b"\n# a note somebody stapled to the artifact\n")
        self.write_sidecar(archive)
        code, said = self.run_gate(archive, tools)
        self.assertEqual(code, 1, said)
        self.assertIn("trailing byte(s) after the end-of-central-directory "
                      "record", said)
        self.assertIn("[3 structure] FAILED", said)

    def test_prepended_bytes_are_refused(self):
        base, package, tools, archive = self.sound()
        archive.write_bytes(b"#!/bin/sh\n# a self-extracting stub\n"
                            + archive.read_bytes())
        self.write_sidecar(archive)
        code, said = self.run_gate(archive, tools)
        self.assertEqual(code, 1, said)
        self.assertIn("precede the first local file header", said)
        self.assertIn("[3 structure] FAILED", said)

    def test_a_miscounting_end_of_central_directory_is_refused(self):
        base, package, tools, archive = self.sound()
        data = bytearray(archive.read_bytes())
        at = data.rindex(b"PK\x05\x06")
        (here, total) = struct.unpack_from("<HH", data, at + 8)
        struct.pack_into("<HH", data, at + 8, here + 3, total + 3)
        archive.write_bytes(bytes(data))
        self.write_sidecar(archive)
        code, said = self.run_gate(archive, tools)
        self.assertEqual(code, 1, said)
        self.assertIn(f"claims {total + 3} entry(ies); the central directory "
                      f"holds {total}", said)
        self.assertIn("[3 structure] FAILED", said)

    def test_a_local_header_that_disagrees_with_its_central_entry(self):
        base, package, tools, archive = self.sound()
        with zipfile.ZipFile(archive) as handle:
            info = handle.getinfo(f"{NAME}/evidence.txt")
            offset, declared = info.header_offset, info.file_size
        data = bytearray(archive.read_bytes())
        struct.pack_into("<I", data, offset + 22, declared + 7)
        archive.write_bytes(bytes(data))
        self.write_sidecar(archive)
        code, said = self.run_gate(archive, tools)
        self.assertEqual(code, 1, said)
        self.assertIn(f"local header uncompressed size {declared + 7} "
                      f"disagrees with the central directory's {declared}",
                      said)
        self.assertIn("[3 structure] FAILED", said)

    # -- check 6: the manifest, cross-proved against the ZIP ------------

    def test_a_duplicate_entry_name_is_refused(self):
        base, package, tools = self.build_tree()
        archive = self.build_zip(base, package, duplicate="evidence.txt")
        code, said = self.run_gate(archive, tools)
        self.assertEqual(code, 1, said)
        self.assertIn("duplicate ZIP entry name: evidence.txt", said)
        self.assertIn("[6 manifest] FAILED", said)
        # And check 2 still names it too: the two checks are independent.
        self.assertIn(f"duplicate archive entry: {NAME}/evidence.txt", said)

    # -- check 11: every shipped tool, three ways -----------------------

    def test_an_executed_digest_that_differs_from_the_shipped_bytes(self):
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base, wrong="checks.py")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("what ran is not what shipped", said)
        self.assertIn("checks.py", said)
        self.assertIn("[11 tool bytes] FAILED", said)

    def test_a_shipped_tool_missing_from_the_executed_record(self):
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base, omit="gzip-sizes.py")
        # The tool that is really missing: drop assemble.sh's run rows.
        record = json.loads(executed.read_text(encoding="utf-8"))
        record["runs"] = [one for one in record["runs"]
                          if one["tool"] != "assemble.sh"]
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("shipped, unclassified", said)
        self.assertIn("assemble.sh", said)

    def test_a_run_row_naming_a_path_the_package_does_not_ship(self):
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        record = json.loads(executed.read_text(encoding="utf-8"))
        record["runs"].append({
            "tool": "phantom.py", "path": "logs/phantom.py",
            "attempt": ATTEMPT, "sha256": "0" * 64,
            "at": "2026-08-17T19:45:20Z", "phase": "P9",
            "log": "", "class": "shipped-executed"})
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("which the package does not ship", said)

    def test_the_bytes_changing_mid_run_are_named(self):
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        record = json.loads(executed.read_text(encoding="utf-8"))
        second = dict(next(one for one in record["runs"]
                           if one["tool"] == "checks.py"))
        second["sha256"] = "a" * 64
        second["phase"] = "P7 a second invocation"
        record["runs"].append(second)
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("the bytes changed mid-run", said)

    def test_an_executed_record_with_an_absolute_anchor_is_refused(self):
        base, package, tools, archive = self.sound()
        # COMPOSED, NEVER WRITTEN. An absolute anchor is what this test
        # plants, so spelling one in the source would make this module
        # unsealable and its shipped bytes differ from the bytes that ran.
        absolute = "/" + "ho" + "me/someone/pkgtools"
        executed = self.executed_record(package, base, anchor=absolute)
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("it must be the SANITIZED symbolic anchor identity",
                      said)

    def test_an_executed_record_with_an_unknown_run_key_is_refused(self):
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        record = json.loads(executed.read_text(encoding="utf-8"))
        record["runs"][0]["notes"] = "an extra key nobody agreed to"
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("carries the unknown key 'notes'", said)

    def test_without_executed_it_passes_but_says_the_claim_is_unproven(self):
        base, package, tools, archive = self.sound()
        code, said = self.run_gate(archive, tools)
        self.assertEqual(code, 0, said)
        self.assertIn("P8 verification: PASS (0 problem(s))", said)
        self.assertIn("EXECUTED-BYTE CLAIM: UNPROVEN", said)
        self.assertIn("no record", said)

    def test_the_table_carries_every_column_the_review_asked_for(self):
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        table_out = base / "tool-table.json"
        code, said = self.run_gate(archive, tools, executed, table_out)
        self.assertEqual(code, 0, said)
        table = json.loads(table_out.read_text(encoding="utf-8"))
        self.assertEqual(table["schema"], "catena-tool-byte-table/1")
        self.assertEqual(table["executed_proof"], "proved")
        self.assertEqual(table["executed_attempt"], ATTEMPT)
        self.assertEqual(table["executed_anchor"], "$EVIDENCE")
        self.assertEqual(len(table["rows"]), len(TOOL_SOURCES))
        for row in table["rows"]:
            for column in ("tool_id", "logical_path", "attempt",
                           "executed_sha256", "shipped_sha256", "equal",
                           "executed", "evidence_log", "class",
                           "trusted_sha256"):
                self.assertIn(column, row)
            self.assertTrue(row["equal"], row)
            self.assertTrue(row["executed"], row)
            self.assertEqual(row["class"], "shipped-executed")
            self.assertEqual(row["executed_sha256"], row["shipped_sha256"])
            self.assertEqual(row["trusted_sha256"], row["shipped_sha256"])

    def test_the_table_without_executed_marks_the_proof_unproven(self):
        base, package, tools, archive = self.sound()
        table_out = base / "tool-table.json"
        code, said = self.run_gate(archive, tools, None, table_out)
        self.assertEqual(code, 0, said)
        table = json.loads(table_out.read_text(encoding="utf-8"))
        self.assertEqual(table["executed_proof"], "unproven")
        for row in table["rows"]:
            self.assertIsNone(row["executed_sha256"])
            self.assertFalse(row["executed_recorded"])

    # -- check 0: the anchor that executes ------------------------------

    def test_an_unversioned_tool_anchor_is_a_problem_without_the_flag(self):
        base, package, tools, archive = self.sound()
        code, said = self.run_gate(archive, tools, accept=False)
        self.assertEqual(code, 1, said)
        self.assertIn("is unversioned", said)
        self.assertIn("--accept-unversioned-tools", said)
        self.assertIn("[0 trust anchor] FAILED", said)

    def test_the_flag_records_the_acceptance_in_the_transcript(self):
        base, package, tools, archive = self.sound()
        code, said = self.run_gate(archive, tools)
        self.assertEqual(code, 0, said)
        self.assertIn("ACCEPTED by --accept-unversioned-tools", said)

    # -- the archive itself ---------------------------------------------

    def test_a_missing_archive_exits_two(self):
        base, package, tools, archive = self.sound()
        code, said = self.run_gate(base / "absent.zip", tools)
        self.assertEqual(code, 2, said)
        self.assertIn("no such archive", said)

    def test_a_file_that_is_not_a_zip_is_reported_and_the_rest_skipped(self):
        base, package, tools, archive = self.sound()
        archive.write_bytes(b"this was never a ZIP container\n")
        self.write_sidecar(archive)
        code, said = self.run_gate(archive, tools)
        self.assertEqual(code, 1, said)
        self.assertIn("the archive is not a readable ZIP container", said)
        self.assertIn("[3 structure] SKIPPED", said)
        self.assertIn("[11 tool bytes] SKIPPED", said)


if __name__ == "__main__":
    unittest.main(verbosity=2)
