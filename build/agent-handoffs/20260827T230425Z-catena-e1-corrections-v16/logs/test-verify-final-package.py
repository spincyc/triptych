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
import importlib.util
import json
import os
import re
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
ASSEMBLER = HERE / "assemble.sh"


def gate_module():
    """`verify-final-package.py`, imported, so its ACCEPTANCE RULE can be
    applied directly to a record rather than inferred from a transcript."""
    spec = importlib.util.spec_from_file_location("verify_final_package", GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def writer_source() -> str:
    """The REAL `emit_executed_tools` body, lifted out of `assemble.sh`.

    Not a copy of it. A copy is a second implementation, and a round-trip
    test against a copy proves the copy agrees with the verifier while the
    shipped writer goes on disagreeing -- which is exactly the failure this
    test exists to make impossible.
    """
    body = ASSEMBLER.read_text(encoding="utf-8")
    start = body.index("emit_executed_tools() {")
    found = re.search(r"<<'PY'\n(.*?)\nPY\n", body[start:], flags=re.S)
    if not found:
        raise AssertionError("assemble.sh: emit_executed_tools has no PY "
                             "heredoc; this test extracts the real writer")
    return found.group(1)

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

    def build_tree(self, evidence: bytes | None = None,
                   attempts: object = None):
        """One correct package on disk, plus the trusted tool anchor.

        Returns (base, package directory, tools directory). Everything under
        `base` is removed on cleanup; nothing outside it is touched.

        `attempts`, when given, is written as `logs/attempts.json` BEFORE the
        rows are frozen, so the shipped history is a manifested member like
        any other rather than a file the seal does not cover.
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
        if attempts is not None:
            (package / "logs" / "attempts.json").write_text(
                attempts if isinstance(attempts, str)
                else json.dumps(attempts, indent=2, sort_keys=True) + "\n",
                encoding="utf-8")

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
        # V16: /2. `phase_view` labels the instant this rendering describes
        # -- V15 shipped two figure sets for one quantity, neither labelled --
        # and `shipped_not_executed` is a ROSTER rather than six manufactured
        # invocation rows folded into `runs`. `omit` now moves a tool into the
        # roster rather than deleting it, which is exactly the distinction:
        # "deliberately not run" is a class, not a silence.
        roster = []
        if omit is not None and (package / "logs" / omit).is_file():
            roster.append({
                "tool": omit, "path": f"logs/{omit}", "attempt": ATTEMPT,
                "sha256": sha256((package / "logs" / omit).read_bytes()),
                "class": "shipped-not-executed",
                "why": "this attempt did not execute it",
            })
        record = {"schema": "catena-executed-tools/2", "attempt": ATTEMPT,
                  "anchor": "$EVIDENCE", "runs": runs,
                  "phase_view": "P8 final verification",
                  "shipped_not_executed": roster,
                  "counts": {
                      "execution_invocations": len(runs),
                      "unique_executed_tools": len({one["tool"]
                                                    for one in runs}),
                      "trusted_not_executed_tools": len(roster),
                      "unique_referenced_tools": len(
                          {one["tool"] for one in runs}
                          | {one["tool"] for one in roster}),
                      "driver_invocations": 0,
                      "external_system_tool_rows": 0,
                  }}
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

    # -- V16, DEFECT 5: TOOL ACCOUNTING DERIVED, NEVER MANUFACTURED ------

    def test_a_record_without_a_phase_view_is_refused(self):
        """V15 shipped `executed_tools 11, executed_invocations 24` in the P8
        table and `executed_tools 14, executed_invocations 27` in the P10 log
        line, for one lane, with neither labelled by phase. Both were true of
        different instants; nothing said which.
        """
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        record = json.loads(executed.read_text(encoding="utf-8"))
        del record["phase_view"]
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("'phase_view'", said)
        self.assertIn("two answers", said)

    def test_a_labelled_phase_view_passes(self):
        """THE MATCHED POSITIVE."""
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 0, said)

    def test_a_roster_row_that_pretends_to_be_an_invocation_is_refused(self):
        """THE SIX MANUFACTURED PLACEHOLDERS, EXACTLY.

        V15 synthesized `at` (the render instant), `phase` ("P10 the post-seal
        gates") and `log` (the assemble log) for six tools that had not run,
        put them in `runs`, and counted them as invocations. All six carried
        the same fabricated instant.
        """
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base, omit="checks.py")
        record = json.loads(executed.read_text(encoding="utf-8"))
        self.assertTrue(record["shipped_not_executed"])
        for one in record["shipped_not_executed"]:
            one["at"] = "2026-08-26T19:58:12Z"
            one["phase"] = "P10 the post-seal gates"
            one["log"] = "outer.assemble.log"
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("a tool that did not run has no instant", said)
        self.assertIn("six invocations that describe nothing", said)

    def test_a_roster_row_carrying_only_what_is_true_passes(self):
        """THE MATCHED POSITIVE: the class, the digest, and no more."""
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base, omit="checks.py")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 0, said)
        record = json.loads(executed.read_text(encoding="utf-8"))
        self.assertEqual([one["tool"]
                          for one in record["shipped_not_executed"]],
                         ["checks.py"])

    def test_a_count_that_does_not_recompute_from_the_rows_is_refused(self):
        """A figure a record states about itself and nobody recomputes is
        prose. V15's `invocations 33` counted six roster rows.
        """
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        record = json.loads(executed.read_text(encoding="utf-8"))
        record["counts"]["execution_invocations"] = (
            len(record["runs"]) + 6)
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("counts['execution_invocations']", said)
        self.assertIn("must recompute from the rows", said)

    def test_a_tool_in_both_the_runs_and_the_roster_is_refused(self):
        """A tool either ran or it did not."""
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        record = json.loads(executed.read_text(encoding="utf-8"))
        ran = record["runs"][0]
        record["shipped_not_executed"] = [{
            "tool": ran["tool"], "path": ran["path"],
            "attempt": ran["attempt"], "sha256": ran["sha256"],
            "class": "shipped-not-executed",
        }]
        record["counts"]["trusted_not_executed_tools"] = 1
        record["counts"]["unique_referenced_tools"] = len(
            {one["tool"] for one in record["runs"]})
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("a tool either ran or it did not", said)

    def test_a_driver_row_is_an_executed_invocation(self):
        """`assemble.sh` and `battery.sh` drove the build and V15 classed both
        never-executed, because neither recorder could see itself.
        """
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        record = json.loads(executed.read_text(encoding="utf-8"))
        for one in record["runs"]:
            if one["tool"] == "assemble.sh":
                one["kind"] = "driver"
        record["counts"]["driver_invocations"] = sum(
            1 for one in record["runs"] if one.get("kind") == "driver")
        self.assertGreater(record["counts"]["driver_invocations"], 0)
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 0, said)

    def test_an_unknown_kind_is_refused(self):
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        record = json.loads(executed.read_text(encoding="utf-8"))
        record["runs"][0]["kind"] = "conductor"
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("'conductor'", said)

    def test_the_v1_schema_is_refused_and_the_reason_is_named(self):
        base, package, tools, archive = self.sound()
        executed = self.executed_record(package, base)
        record = json.loads(executed.read_text(encoding="utf-8"))
        record["schema"] = "catena-executed-tools/1"
        executed.write_text(json.dumps(record, indent=2, sort_keys=True),
                            encoding="utf-8")
        code, said = self.run_gate(archive, tools, executed)
        self.assertEqual(code, 1, said)
        self.assertIn("six manufactured not-executed placeholder rows", said)

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

    # -- the writer and the verifier state ONE contract -------------------
    #
    # V15, FOUND AT SEAL TIME AND NOT BY THIS SUITE. `assemble.sh` wrote an
    # explanatory sentence into `path` for an `external-system-tool` row --
    # "(external: python3 is a system tool, not a package member)" -- and
    # `verify-final-package.py` requires that field to be "" for exactly that
    # class, and says so in its own refusal. Both sides were defensible
    # alone; they simply did not agree, and nothing here noticed, because
    # every fixture above HAND-WRITES its executed record and so tests the
    # verifier against a record the writer never produced.
    #
    # These two drive the REAL writer, lifted out of `assemble.sh`, over a
    # RUNS file that reaches every branch it has, and put its output through
    # the verifier's own acceptance rule.

    def round_trip(self, base: Path) -> dict:
        """Run the real writer over every branch; return the record it wrote."""
        package = base / "pkg"
        (package / "logs" / "attempt-04").mkdir(parents=True)
        for name in ("alpha.py", "beta.py", "gamma.py"):
            (package / "logs" / name).write_text(
                f"#!/usr/bin/env python3\n# {name}\n", encoding="utf-8")
        # The battery transcript a merged row is admitted by: the package
        # ships it, so the row for the tool that wrote it may enter.
        (package / "logs" / "attempt-04" / "gamma.log").write_text(
            "ran\n", encoding="utf-8")

        digest = lambda seed: hashlib.sha256(seed).hexdigest()  # noqa: E731
        runs = base / "runs.jsonl"
        runs.write_text("".join(json.dumps(one, sort_keys=True) + "\n" for one in [
            # the interpreter and git: `record_external_tool`, kind=system
            {"tool": "python3", "sha256": digest(b"python3"),
             "at": "2026-08-26T14:41:18Z", "phase": "P0 preflight",
             "log": "outer.assemble.log", "kind": "system"},
            {"tool": "git", "sha256": digest(b"git"),
             "at": "2026-08-26T14:41:18Z", "phase": "P0 preflight",
             "log": "outer.assemble.log", "kind": "system"},
            # one of ours, shipped under logs/: `run_tool`, kind=shipped
            {"tool": "alpha.py", "sha256": digest(b"#!/usr/bin/env python3\n# alpha.py\n"),
             "at": "2026-08-26T14:41:19Z", "phase": "P1 staging",
             "log": "logs/attempt-04/gamma.log", "kind": "shipped"},
            # one of ours the package does NOT ship: the `else` branch, which
            # wrote an out-of-package location into `path` before V15
            {"tool": "delta.py", "sha256": digest(b"delta"),
             "at": "2026-08-26T14:41:20Z", "phase": "P8 final verification",
             "log": "outer.verify-final.log", "kind": "shipped"},
        ]), encoding="utf-8")

        # and the batteries' own contemporaneous digests, merged by transcript
        toolruns = base / "executed-tools.jsonl"
        toolruns.write_text(json.dumps({
            "tool": "gamma.py",
            "sha256": digest(b"#!/usr/bin/env python3\n# gamma.py\n"),
            "at": "2026-08-26T14:20:00Z", "phase": "gzip-sizes",
            "log": "logs/attempt-04/gamma.log",
            "attempt": "parent-20260826T140000Z-04ab", "kind": "battery",
        }, sort_keys=True) + "\n", encoding="utf-8")

        out = base / f"{NAME}.executed-tools.json"
        done = subprocess.run(
            [sys.executable, "-B", "-", str(runs), str(out), ATTEMPT,
             "$EVIDENCE", str(package), "P10 the post-seal gates",
             "outer.assemble.log", str(toolruns)],
            input=writer_source(), capture_output=True, text=True)
        self.assertEqual(0, done.returncode,
                         done.stdout + done.stderr)
        return json.loads(out.read_text(encoding="utf-8"))

    def test_every_row_the_writer_emits_is_accepted_by_the_verifier(self):
        with tempfile.TemporaryDirectory() as scratch:
            base = Path(scratch)
            record = self.round_trip(base)
            gate = gate_module()
            path = base / f"{NAME}.executed-tools.json"
            loaded, problems = gate.load_executed(path)
            # `Problem` IS a str; joining and comparing them needs nothing.
            self.assertEqual([], [str(one) for one in problems],
                             "the writer produced a record its own verifier "
                             "refuses; the two do not state one contract")
            self.assertEqual(len(record["runs"]), len(loaded["runs"]),
                             "a row was dropped by the acceptance rule")

            # THE TEST MUST REACH THE BRANCH THAT BROKE. A round trip that
            # never emits an external row would pass while the defect stood.
            classes = {one["class"] for one in record["runs"]}
            self.assertIn(gate.CLASS_EXTERNAL, classes)
            self.assertIn(gate.CLASS_SHIPPED_EXECUTED, classes)
            # V16: `shipped-not-executed` IS NO LONGER A RUN ROW, and that is
            # the point of the change. V15 synthesized an `at` (the render
            # instant), a `phase` and a `log` for a tool that had not run,
            # appended it to `runs` beside real invocations, and counted the
            # result as an invocation. The roster is its own list now, and it
            # carries none of those three because a tool that did not run has
            # none of them.
            self.assertNotIn(gate.CLASS_SHIPPED_NOT_EXECUTED, classes,
                             "a roster entry is not an invocation row")
            roster = record.get("shipped_not_executed") or []
            self.assertTrue(roster, "the writer emits the roster")
            for one in roster:
                self.assertEqual(one["class"],
                                 gate.CLASS_SHIPPED_NOT_EXECUTED)
                for forbidden in ("at", "phase", "log"):
                    self.assertNotIn(forbidden, one,
                                     f"a tool that did not run has no "
                                     f"{forbidden}")
            # AND THE FIVE FIGURES RECOMPUTE FROM THE ROWS THEY DESCRIBE.
            counts = record["counts"]
            self.assertEqual(counts["execution_invocations"],
                             len(record["runs"]))
            self.assertEqual(counts["trusted_not_executed_tools"],
                             len(roster))
            self.assertEqual(counts["unique_referenced_tools"],
                             len({one["tool"] for one in record["runs"]}
                                 | {one["tool"] for one in roster}))
            # THE PHASE IS ON THE RECORD. V15 shipped two figure sets for one
            # quantity with neither labelled by phase.
            self.assertEqual(record["phase_view"], "P10 the post-seal gates")
            self.assertTrue(classes <= set(gate.TOOL_CLASSES),
                            f"the writer emits a class the verifier does not "
                            f"accept: {sorted(classes - set(gate.TOOL_CLASSES))}")

            # And the contract itself, in the words both sides now use.
            shipped = {f"logs/{one.name}" for one
                       in (base / "pkg" / "logs").iterdir() if one.is_file()}
            for one in record["runs"]:
                if one["class"] == gate.CLASS_EXTERNAL:
                    self.assertEqual("", one["path"],
                                     f"{one['tool']}: an external system tool "
                                     f"ships nothing, so its path is \"\"")
                else:
                    self.assertIn(one["path"], shipped,
                                  f"{one['tool']}: a non-external row names a "
                                  f"path the package does not ship")

    def test_the_old_prose_path_would_have_been_caught_here(self):
        # The seal-time defect itself, reintroduced into a record the writer
        # produced, so this test is known to be able to see it.
        with tempfile.TemporaryDirectory() as scratch:
            base = Path(scratch)
            record = self.round_trip(base)
            for one in record["runs"]:
                if one["class"] == "external-system-tool":
                    one["path"] = (f"(external: {one['tool']} is a system "
                                   f"tool, not a package member)")
            path = base / f"{NAME}.executed-tools.json"
            path.write_text(json.dumps(record, indent=2, sort_keys=True)
                            + "\n", encoding="utf-8")
            _loaded, problems = gate_module().load_executed(path)
            said = " ".join(str(one) for one in problems)
            self.assertIn("an external system tool ships nothing", said)
            self.assertIn("python3", said)
            self.assertIn("git", said)

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


    # -- check 12: THE SHIPPED HISTORY, ON BOTH AXES ---------------------
    #
    # Before V16 this gate read no attempt disposition at all: it verified
    # the archive, the manifest, the claims partition and the tool bytes, and
    # the attempt history reached it only as bytes to hash. That was a hole
    # exactly where the V15 review looked -- the shipped history is what a
    # reviewer opens to find out which runs the figures came from.

    SOUND_HISTORY = {"rows": [], "attempts": [
        {"attempt": "head-01", "execution_disposition": "complete",
         "evidence_disposition": "authoritative"},
        {"attempt": "parent-02", "execution_disposition": "complete",
         "evidence_disposition": "set-aside"},
        {"attempt": "head-03", "execution_disposition": "abandoned",
         "evidence_disposition": "unevidenced"},
        {"attempt": "parent-04", "execution_disposition": "failed",
         "evidence_disposition": "unevidenced"},
    ]}

    def sound_with(self, attempts):
        base, package, tools = self.build_tree(attempts=attempts)
        archive = self.build_zip(base, package)
        return base, package, tools, archive

    def test_a_package_with_no_attempt_history_says_so_rather_than_failing(
            self):
        """THE CONTROL. Not every package ships the member, and a missing
        optional member is not a verification failure."""
        base, package, tools, archive = self.sound()
        code, said = self.run_gate(archive, tools,
                                   self.executed_record(package, base))
        self.assertEqual(code, 0, said)
        self.assertIn("[12 attempt dispositions] ok", said)
        self.assertIn("ships no logs/attempts.json", said)

    def test_both_axes_are_reported_and_abandoned_is_named(self):
        base, package, tools, archive = self.sound_with(self.SOUND_HISTORY)
        code, said = self.run_gate(archive, tools,
                                   self.executed_record(package, base))
        self.assertEqual(code, 0, said)
        self.assertIn("[12 attempt dispositions] ok", said)
        self.assertIn("EXECUTION   EVIDENCE", said)
        self.assertIn("execution: abandoned 1, complete 2, failed 1", said)
        self.assertIn("evidence : authoritative 1, set-aside 1, "
                      "unevidenced 2", said)
        self.assertIn("abandoned: 1 -- head-03; resolved terminal history, "
                      "in no successful and no authoritative tally", said)

    def test_evidence_on_an_attempt_that_measured_nothing_is_refused(self):
        """THE MATCHED NEGATIVE. Abandonment is accepted as history and
        refused as evidence, which is the whole distinction."""
        for word in ("failed", "abandoned", "discarded"):
            with self.subTest(execution=word):
                history = {"rows": [], "attempts": [
                    {"attempt": "head-09", "execution_disposition": word,
                     "evidence_disposition": "authoritative"}]}
                base, package, tools, archive = self.sound_with(history)
                code, said = self.run_gate(
                    archive, tools, self.executed_record(package, base))
                self.assertEqual(code, 1, said)
                self.assertIn("[12 attempt dispositions] FAILED", said)
                self.assertIn("measured nothing that could be carried or "
                              "declined", said)

    def test_an_attempt_left_open_in_the_shipped_history_is_refused(self):
        history = {"rows": [], "attempts": [
            {"attempt": "head-09", "evidence_disposition": "unevidenced"}]}
        base, package, tools, archive = self.sound_with(history)
        code, said = self.run_gate(archive, tools,
                                   self.executed_record(package, base))
        self.assertEqual(code, 1, said)
        self.assertIn("carries no execution disposition", said)

    def test_a_history_with_no_summary_is_refused(self):
        base, package, tools, archive = self.sound_with({"rows": []})
        code, said = self.run_gate(archive, tools,
                                   self.executed_record(package, base))
        self.assertEqual(code, 1, said)
        self.assertIn("carries no `attempts` summary", said)

    def test_an_unreadable_history_is_refused_rather_than_passed_over(self):
        base, package, tools, archive = self.sound_with("{not json")
        code, said = self.run_gate(archive, tools,
                                   self.executed_record(package, base))
        self.assertEqual(code, 1, said)
        self.assertIn("present and unreadable as JSON", said)


if __name__ == "__main__":
    unittest.main(verbosity=2)
