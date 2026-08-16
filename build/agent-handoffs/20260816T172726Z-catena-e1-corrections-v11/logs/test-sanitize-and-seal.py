#!/usr/bin/env python3
"""Tests for the V9 sealer toolchain.

Every behaviour changed in V6 through V9 is pinned here, together with
regressions for the privacy detections those rounds preserve. The V9 pins are
the frozen-inventory protocol: `--normalize-only` writes no manifest,
`--check-only` fails a tree the substitution table would still touch,
`--manifest-only` refuses a frozen row that drifted, `derived_members` are
named and never sized, rows and derived_members partition the member set, and
the P8 verifier catches a stale row, an unpartitioned member, and a sidecar
whose recorded size is wrong. The V10 pins: the P8 transcript opens with a
header binding it to the exact archive (basename, bytes, sha256, root, UTC
time), a duplicate manifest or claims row is a named failure, the battery
refuses an existing ledger and writes provenance plus unique indexed log
paths as it runs, and the assembler refuses an existing handoff directory or
archive instead of removing it. Run it standalone:

    python3 test-sanitize-and-seal.py

The sealer is loaded from THIS FILE'S directory, so the pair can be copied
anywhere together. The identities are fixed synthetic values set in the
environment before the sealer is loaded, so no assertion depends on -- or can
leak -- the host this runs on.

THIS FILE SHIPS INSIDE THE PACKAGE IT TESTS, so it has to survive the tool it
tests: a module full of raw adversarial literals would be hard-blocked by the
sealer's own scan, and a test module that cannot pass its tool is not evidence.
The rule followed here is therefore mechanical:

    NO LINE OF THIS SOURCE MAY MATCH ANY forbidden() PATTERN.

Every adversarial fixture is COMPOSED AT RUNTIME from fragments -- see the
FIXTURES section -- so the value under test is exactly what it always was and
only the source text differs. The property is pinned by
`SelfBlindness.test_the_test_module_is_itself_sealable`, which scans this very
file and fails the moment a raw literal comes back.

Fixtures that are supposed to be CLEAN -- the false-positive corpus, the
exempt addresses, the time ranges -- are deliberately left as plain literals.
They must not match, so writing them out is itself a second, independent proof
that they do not.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# FIXTURES. Assembled from fragments so that no line below is itself a hit.
# `_j` is the only assembly primitive; the character constants exist so that a
# separator never appears adjacent to the text that would make it a token.
# ---------------------------------------------------------------------------

_COLON = chr(58)
_DOT = chr(46)
_SLASH = chr(47)
_PLUS = chr(43)
_AT = chr(64)


def _j(*parts: str) -> str:
    """Join fragments into the value under test. Composition only."""
    return "".join(parts)


def zone(*parts: str) -> str:
    """An area/city zone name, assembled so no line here carries one whole."""
    return _SLASH.join(parts)


def tz_context(label: str, name: str) -> str:
    """A bare zone name behind the context that makes it a zone."""
    return label + name


def offset(sign: str, hours: str, minutes: str) -> str:
    return _j(sign, hours, _COLON, minutes)


# Fixed synthetic identities. Composed for the same reason as everything else,
# and chosen so they cannot appear in the sealer's own source (which would trip
# its self-blindness check) or collide with this machine's real values.
USER = _j("qzv", "testacct")
HOST = _j("qzv", "testhost")
UID = _j("42", "4242")
HOME = _j(_SLASH, "home", _SLASH, USER)
os.environ["SANITIZE_USER"] = USER
os.environ["SANITIZE_HOST"] = HOST
os.environ["SANITIZE_UID"] = UID
os.environ["SANITIZE_HOME"] = HOME

# A unique D-Bus bus name, in the three positions one is really printed in.
DBUS_A = _j(_COLON, "1", _DOT, "42")
DBUS_B = _j(_COLON, "1", _DOT, "107")
DBUS_C = _j(_COLON, "1", _DOT, "9")

PID = _j("313", "37")
PROC_STATUS = _j(_SLASH, "proc", _SLASH, PID, _SLASH, "status")
OTHER_HOME = _j(_SLASH, "home", _SLASH, "someoneelse", _SLASH, "work")
SCRATCH = _j(_SLASH, "tmp", _SLASH, "claude", "-shell-snapshot")
EMAIL = _j("someone", _AT, "example", _DOT, "org")
UUID_HYPHENATED = _j("6ba7b810", "-9dad", "-11d1", "-80b4", "-00c04fd430c8")
MACHINE_HEX = _j("7b1f0e2c4a9d4f6b", "8c0e2a4d6f8b0c1e")
IP_PRIVATE = _j("10", _DOT, "1", _DOT, "2", _DOT, "3")
IP_GATEWAY = _j("192", _DOT, "168", _DOT, "1", _DOT, "1")
LOOPBACK_PORT = _j("127", _DOT, "0", _DOT, "0", _DOT, "1", _COLON, "9222")
TIMESTAMP = _j("2026-08-14T12", _COLON, "35", _COLON, "24")

# V11 fixtures. An agent workspace path and a lane evidence directory, composed
# the same way as everything above -- and for the same reason, since the rules
# that match them are in `forbidden()` now and this file is scanned by it.
#
# The names are synthetic AND arbitrary, which is the point of the second
# workspace below: the rule under test is a naming CONVENTION -- a worktrees
# root, then the project and the slug that identify one line of work -- so two
# workspaces spelled nothing alike must both collapse. The alternate one also
# uses the other home root and a different intermediate segment.
WORKTREES = _j("work", "trees")
WS_PROJECT = _j("qzv", "proj")
WS_SLUG = _j("qzv", "slug")
WORKSPACE_RAW = _j(HOME, _SLASH, "git", _SLASH, WORKTREES,
                   _SLASH, WS_PROJECT, _SLASH, WS_SLUG)
# The same disclosure after the home rule has already fired. This is the form
# V10 shipped 89 times: prefix repaired, identity intact.
WORKSPACE_TOKENIZED = _j("$HOME", _SLASH, "git", _SLASH, WORKTREES,
                         _SLASH, WS_PROJECT, _SLASH, WS_SLUG)
WS_ALT_PROJECT = _j("alpha", "-lab")
WS_ALT_SLUG = _j("beta", "-9")
WORKSPACE_ALT = _j(_SLASH, "Users", _SLASH, _j("qzv", "other"),
                   _SLASH, "src", _SLASH, WORKTREES,
                   _SLASH, WS_ALT_PROJECT, _SLASH, WS_ALT_SLUG)
LANE = _j("qzv", "lane", "-evidence")
LANE_DIR = _j(_DOT, "agents", _SLASH, LANE)
LANE_PATH = _j(WORKSPACE_RAW, _SLASH, LANE_DIR, _SLASH, "stage",
               _SLASH, "logs", _SLASH, "gate.json")
LANE_TAIL = _j("stage", _SLASH, "logs", _SLASH, "gate.json")

# A local-offset provenance stamp of the shape `date -Is` writes, and a second
# one 17 minutes 30 seconds later: the pair is what proves ORDER and ELAPSED
# time survive the repair.
LOCAL_OFFSET = offset("-", "05", "00")
LOCAL_START = _j("2026-08-16T06", _COLON, "00", _COLON, "04") + LOCAL_OFFSET
LOCAL_END = _j("2026-08-16T06", _COLON, "17", _COLON, "34") + LOCAL_OFFSET
LOCAL_ELAPSED = 17 * 60 + 30

HERE = Path(__file__).resolve().parent
SEALER_PATH = HERE / "sanitize-and-seal.py"
DERIVER_PATH = HERE / "derive-claims.py"
AUDITOR_PATH = HERE / "head-consistency.py"
VERIFIER_PATH = HERE / "verify-final-package.py"
TEST_PATH = Path(__file__).resolve()


def _load(alias: str, location: Path):
    spec = importlib.util.spec_from_file_location(alias, location)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sealer = _load("sealer_under_test", SEALER_PATH)
deriver = _load("deriver_under_test", DERIVER_PATH)
auditor = _load("auditor_under_test", AUDITOR_PATH)
verifier = _load("verifier_under_test", VERIFIER_PATH)

WHO = {"user": USER, "host": HOST, "uid": UID, "home": HOME}
CHECKS = sealer.forbidden(WHO, "")
RULES = sealer.rules(WHO, "")


def labels(text: str) -> set[str]:
    """Every check label that fires on a single line of text."""
    return {label for label, pattern in CHECKS if pattern.search(text)}


def normalized(text: str) -> str:
    """The text after every normalize rule has run, in order."""
    for pattern, replacement in RULES:
        text = pattern.sub(replacement, text)
    return text


def clock_seconds(stamp: str) -> int:
    """Seconds-of-day read out of the first `HH:MM:SS` in a stamp.

    Used to prove that the elapsed time between two ledger entries survives
    the UTC shift; both entries move by the same amount, so the difference is
    invariant.
    """
    found = re.search(r"(\d{2})" + _COLON + r"(\d{2})" + _COLON + r"(\d{2})",
                      stamp)
    assert found, stamp
    hours, minutes, seconds = (int(one) for one in found.groups())
    return hours * 3600 + minutes * 60 + seconds


class Package:
    """A throwaway package directory built from a {relative path: content} map."""

    def __init__(self, files: dict[str, str | bytes]):
        self._temp = tempfile.TemporaryDirectory()
        self.root = Path(self._temp.name) / "package"
        self.root.mkdir()
        for relative, content in files.items():
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(content, bytes):
                target.write_bytes(content)
            else:
                target.write_text(content, encoding="utf-8")

    def __enter__(self) -> "Package":
        return self

    def __exit__(self, *exc) -> None:
        self._temp.cleanup()

    def run(self, *flags: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = sealer.main([str(self.root), *flags])
        return code, out.getvalue(), err.getvalue()

    def read(self, relative: str) -> str:
        return (self.root / relative).read_text(encoding="utf-8")

    def exists(self, relative: str) -> bool:
        return (self.root / relative).exists()


class TimezoneAreas(unittest.TestCase):
    """Item 1: areas, path prefixes and signed-offset zones that escaped V5."""

    ESCAPED = [
        zone("Mideast", "Riyadh87"),
        zone("SystemV", "AST4"),
        zone("Chile", "Continental"),
        zone("Indian", "Mauritius"),
        zone("posix", "Europe", "Paris"),
        zone("right", "Asia", "Tokyo"),
        zone("Etc", _j("GMT", _PLUS, "5")),
        zone("Etc", _j("GMT", "-14")),
        zone("Arctic", "Longyearbyen"),
        zone("Antarctica", "DumontDUrville"),
        zone("America", "Argentina", "Ushuaia"),
    ]
    STILL_CAUGHT = [
        zone("Europe", "Berlin"),
        zone("Australia", "Sydney"),
        zone("US", "Pacific"),
    ]

    def test_previously_escaping_forms_are_flagged(self):
        for one in self.ESCAPED:
            with self.subTest(zone=one):
                self.assertIn("iana-timezone", labels(f"zone {one} here"))

    def test_previously_escaping_forms_are_normalized(self):
        for one in self.ESCAPED:
            with self.subTest(zone=one):
                self.assertNotIn(one, normalized(f"zone {one} here"))

    def test_known_forms_are_still_caught(self):
        for one in self.STILL_CAUGHT:
            with self.subTest(zone=one):
                self.assertIn("iana-timezone", labels(f"TZ file {one}"))
                self.assertNotIn(one, normalized(f"TZ file {one}"))


class TimezoneBareNames(unittest.TestCase):
    """Item 1: the bare zone names, in a widened set of zone contexts."""

    IN_CONTEXT = [
        tz_context("TZ=", "Factory"),
        tz_context("TZ=", "localtime"),
        tz_context("TZ=", "UTC"),
        tz_context(_j("zoneinfo", _SLASH), "Zulu"),
        tz_context(_j("time", "zone: "), "Iceland"),
        tz_context(_j("time zone", " = "), "GMT"),
        tz_context(_j("time_zone", "="), "Kwajalein"),
        tz_context(_j("ZoneInfo", '("'), "Japan") + '")',
        tz_context("tzname=", "EST5EDT"),
        tz_context("TZID:", "W-SU"),
    ]

    def test_bare_names_in_context_are_flagged_and_repaired(self):
        for one in self.IN_CONTEXT:
            with self.subTest(text=one):
                self.assertIn("timezone-name", labels(one))
                self.assertNotEqual(one, normalized(one))

    def test_bare_names_out_of_context_are_left_alone(self):
        # Ordinary English words; a check that flagged them bare would flag the
        # sealer's own pattern list. These are safe to write out literally --
        # that they do not match is exactly what is being asserted.
        for one in ("Universal agreement was reached",
                    "the turkey was roasted",
                    "an iceland of calm"):
            with self.subTest(text=one):
                self.assertEqual(set(), labels(one) & {"timezone-name",
                                                       "iana-timezone"})
                self.assertEqual(one, normalized(one))


class UtcOffsetSymmetry(unittest.TestCase):
    """Item 1: the utc-offset rule and check are one pattern, not two."""

    OFFSETS = [
        TIMESTAMP + offset("+", "02", "00"),
        _j("2026-08-14 12", _COLON, "35", _COLON, "24", _DOT, "512")
        + offset("-", "05", "00"),
        _j("2026-08-14T12", _COLON, "35") + offset("+", "05", "30"),
        "started " + _j("12", _COLON, "34", _COLON, "56")
        + offset("-", "08", "00") + " sharp",
        _j("12", _COLON, "34", _COLON, "56") + _j("+", "0200"),
    ]
    # Clean by construction: written out because they must NOT match.
    NOT_OFFSETS = [
        "range 10:00-11:30",
        "slots 09:15-09:45 and 13:00-14:00",
        "duration 12:34:56.789",
        "commit 2026-08-14T12:35:24Z",
        "issue -12:30 in the log",
    ]

    def test_offsets_are_flagged_and_repaired(self):
        """CORRECTED ORACLE (V11), and the V10 review found it.

        The second assertion used to read

            self.assertIn(sealer.PLACEHOLDER_TZ, normalized(one))

        which pinned the repair as "put `<tz>` where the offset was, and keep
        everything else" -- that is, it pinned the defect. The rule kept the
        local wall clock, and the package name carries a UTC stamp, so the two
        differed by exactly the builder's offset and the archive never had to
        be opened. The property that was wanted is asserted instead: the
        offset marker is gone, the check no longer fires, and the stamp really
        moved. What it moved TO is `UtcNormalization` below.
        """
        for one in self.OFFSETS:
            with self.subTest(text=one):
                self.assertIn("utc-offset", labels(one))
                done = normalized(one)
                self.assertNotEqual(one, done)
                self.assertNotIn("utc-offset", labels(done))
                self.assertNotIn(sealer.PLACEHOLDER_TZ, done,
                                 "a provenance stamp is shifted, not blanked")

    def test_time_ranges_are_neither_flagged_nor_rewritten(self):
        for one in self.NOT_OFFSETS:
            with self.subTest(text=one):
                self.assertNotIn("utc-offset", labels(one))
                self.assertEqual(one, normalized(one))

    def test_rule_and_check_agree_on_every_sample(self):
        for one in self.OFFSETS + self.NOT_OFFSETS:
            with self.subTest(text=one):
                self.assertEqual("utc-offset" in labels(one),
                                 normalized(one) != one)

    def test_every_shared_pattern_backs_both_a_rule_and_a_check(self):
        shared = sealer.SHARED_BEFORE_IDS + sealer.SHARED_AFTER_IDS
        rule_patterns = {pattern.pattern for pattern, _ in RULES}
        check_patterns = {pattern.pattern for _, pattern in CHECKS}
        for label, pattern, _replacement, _flags in shared:
            with self.subTest(label=label):
                self.assertIn(pattern, rule_patterns)
                self.assertIn(pattern, check_patterns)


class WorkspaceIdentity(unittest.TestCase):
    """V11 defect 1: the workspace and the lane survived a prefix-only repair.

    The V10 home rules rewrote `/home/<account>` and stopped -- their account
    class cannot cross a separator -- so the two segments that name the line of
    work stood in every path, and `forbidden()` had no entry for them either.
    Rule and check were blind together, which is why the seal transcript could
    report zero hits over a package that named the workspace 89 times and the
    lane directory 88. These pin both halves.
    """

    def test_both_the_raw_and_the_already_tokenized_prefix_collapse(self):
        """Ordering must not decide the outcome.

        The home rules run first, so in practice this rule meets a path whose
        prefix is already `$HOME` -- exactly the form V10 shipped. It has to
        match that as readily as the raw one.
        """
        for one in (WORKSPACE_RAW, WORKSPACE_TOKENIZED):
            with self.subTest(path=one):
                self.assertIn("workspace-path", labels(one))
                done = normalized(one)
                self.assertEqual(sealer.PLACEHOLDER_WORKSPACE, done)
                self.assertNotIn(WS_PROJECT, done)
                self.assertNotIn(WS_SLUG, done)
                self.assertEqual(set(), labels(done))

    def test_a_differently_named_workspace_is_the_same_rule(self):
        """The rule is the CONVENTION, not one project and one slug.

        Different home root, different intermediate segment, and a project and
        slug that share no text with the pair above.
        """
        self.assertIn("workspace-path", labels(WORKSPACE_ALT))
        done = normalized(WORKSPACE_ALT)
        self.assertEqual(sealer.PLACEHOLDER_WORKSPACE, done)
        self.assertNotIn(WS_ALT_PROJECT, done)
        self.assertNotIn(WS_ALT_SLUG, done)
        self.assertEqual(set(), labels(done))

    def test_the_lane_evidence_directory_is_flagged_and_collapsed(self):
        self.assertIn("evidence-dir", labels(LANE_DIR))
        self.assertEqual(sealer.PLACEHOLDER_EVIDENCE, normalized(LANE_DIR))
        self.assertNotIn(LANE, normalized(LANE_DIR))

    def test_a_whole_evidence_path_collapses_to_two_tokens_and_a_tail(self):
        """And the TAIL survives, for the reason `_scratch` survives its tail:
        a rule that ate the remainder would cost the identity of the artifact
        the path names, which is the evidence."""
        self.assertIn("workspace-path", labels(LANE_PATH))
        self.assertIn("evidence-dir", labels(LANE_PATH))
        self.assertEqual(_j(sealer.PLACEHOLDER_WORKSPACE, _SLASH,
                            sealer.PLACEHOLDER_EVIDENCE, _SLASH, LANE_TAIL),
                         normalized(LANE_PATH))
        self.assertEqual(set(), labels(normalized(LANE_PATH)))

    def test_occurrences_in_a_log_body_and_in_metadata_are_repaired(self):
        files = {
            "HANDOFF.md": ("# Handoff\n\nSee [log](logs/run.log) and "
                           "[meta](logs/meta.json).\n"),
            "logs/run.log": (f"started under {WORKSPACE_RAW}\n"
                             f"wrote {LANE_PATH}\n"),
            "logs/meta.json": json.dumps(
                {"root": WORKSPACE_TOKENIZED, "lane": LANE_DIR,
                 "artifact": LANE_PATH}, indent=1) + "\n",
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            self.assertIn("0 private-token hit(s)", out)
            for member in ("logs/run.log", "logs/meta.json"):
                body = package.read(member)
                with self.subTest(member=member):
                    self.assertNotIn(WORKTREES, body)
                    self.assertNotIn(WS_PROJECT, body)
                    self.assertNotIn(WS_SLUG, body)
                    self.assertNotIn(LANE, body)
                    self.assertIn(sealer.PLACEHOLDER_WORKSPACE, body)
                    self.assertIn(sealer.PLACEHOLDER_EVIDENCE, body)
            # The artifact the path named is still identifiable.
            self.assertIn(LANE_TAIL, package.read("logs/run.log"))

    def test_the_identity_in_a_member_name_is_a_hard_hit(self):
        """A NAME cannot be rewritten -- normalize() moves bytes, not paths --
        so the only correct behaviour is to refuse. That is why the check
        matters independently of the rule."""
        cases = [
            ("evidence-dir",
             _j("mirror", _SLASH, LANE_DIR, _SLASH, "note.txt")),
            ("workspace-path",
             _j("logs", _SLASH, "Users", _SLASH, _j("qzv", "other"),
                _SLASH, "src", _SLASH, WORKTREES, _SLASH, WS_ALT_PROJECT,
                _SLASH, WS_ALT_SLUG, _SLASH, "note.txt")),
        ]
        for label, relative in cases:
            with self.subTest(label=label):
                with Package({"HANDOFF.md": "# Handoff\n\nnothing linked\n",
                              relative: "harmless content\n"}) as package:
                    code, out, err = package.run("--check-only")
                    self.assertEqual(1, code, out)
                    self.assertIn(f"[name/{label}]", out)
                    self.assertIn("private tokens are still present", err)

    # Clean by construction, and written out as plain literals for the reason
    # the false-positive corpus is: they must NOT match, and this file is
    # scanned by the checks that would match them.
    BENIGN = [
        "each of the worktrees holds one line of work",
        "see docs/worktrees-guide.md for the layout",
        "the agents directory is not a repository",
        "agents/registry.json",
        "evidence/stage/logs/run.json",
        "a workspace is named project and slug",
    ]

    def test_benign_text_is_neither_flagged_nor_rewritten(self):
        for one in self.BENIGN:
            with self.subTest(text=one):
                self.assertEqual(set(),
                                 labels(one) & {"workspace-path",
                                                "evidence-dir"})
                self.assertEqual(one, normalized(one))


class UtcNormalization(unittest.TestCase):
    """V11 defect 2: the offset marker was replaced and the LOCAL CLOCK kept.

    `battery.sh` writes `date -Is`, so the package carried a local wall-clock
    time while its own archive name carried a UTC stamp. Subtracting one from
    the other returned the builder's offset without the archive being opened.
    Redaction would close it and destroy the ledger; the stamp is shifted to
    UTC instead, so ordering and elapsed time survive exactly.
    """

    def test_a_local_timestamp_becomes_its_utc_equivalent(self):
        self.assertEqual(
            _j("2026-08-16T11", _COLON, "00", _COLON, "04", "Z"),
            normalized(LOCAL_START))
        self.assertEqual(set(), labels(normalized(LOCAL_START)))

    def test_neither_the_offset_nor_the_local_clock_survives(self):
        done = normalized(LOCAL_START)
        self.assertNotIn(LOCAL_OFFSET, done)
        self.assertNotIn(_j("06", _COLON, "00", _COLON, "04"), done,
                         "the local clock beside a UTC package stamp IS the "
                         "offset, one subtraction away")
        self.assertNotIn(sealer.PLACEHOLDER_TZ, done)

    def test_ordering_and_elapsed_time_survive_the_shift(self):
        first, last = normalized(LOCAL_START), normalized(LOCAL_END)
        self.assertLess(first, last,
                        "a provenance ledger is worthless without order")
        self.assertEqual(LOCAL_ELAPSED,
                         clock_seconds(last) - clock_seconds(first),
                         "both ends move by the same amount, so every "
                         "duration is preserved to the second")

    def test_a_shift_crossing_midnight_moves_the_date(self):
        one = (_j("2026-08-16T22", _COLON, "30", _COLON, "00")
               + offset("-", "05", "00"))
        self.assertEqual(
            _j("2026-08-17T03", _COLON, "30", _COLON, "00", "Z"),
            normalized(one))

    def test_the_written_shape_survives_the_shift(self):
        one = (_j("2026-08-16 06", _COLON, "00", _COLON, "04", _DOT, "512")
               + offset("-", "05", "00"))
        self.assertEqual(
            _j("2026-08-16 11", _COLON, "00", _COLON, "04", _DOT, "512", "Z"),
            normalized(one),
            "the separator and the fraction are the record's shape, not the "
            "disclosure")

    def test_a_time_with_no_date_wraps_within_the_day(self):
        one = _j("22", _COLON, "30", _COLON, "00") + offset("+", "05", "30")
        self.assertEqual(_j("17", _COLON, "00", _COLON, "00", "Z"),
                         normalized(one))

    def test_the_previous_versions_residue_is_flagged_and_dropped(self):
        """The V10 output shape, met as input. The instant cannot be recovered
        -- that repair threw the offset away -- so this is the one class the
        tool redacts rather than moves, and it has its own check so a package
        carrying it cannot be sealed silently."""
        one = (_j("2026-08-16T06", _COLON, "00", _COLON, "04")
               + sealer.PLACEHOLDER_TZ)
        self.assertIn("local-time-tokenized", labels(one))
        self.assertEqual(sealer.PLACEHOLDER_TZ, normalized(one))
        self.assertEqual(set(), labels(normalized(one)))

    def test_a_sealed_ledger_still_reads_in_order(self):
        files = {
            "HANDOFF.md": "# Handoff\n\nSee [ledger](logs/order.txt).\n",
            "logs/order.txt": (f"START {LOCAL_START}\n"
                               f"END {LOCAL_END}\n"),
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            self.assertIn("0 private-token hit(s)", out)
            body = package.read("logs/order.txt")
            self.assertNotIn(LOCAL_OFFSET, body)
            self.assertNotIn(sealer.PLACEHOLDER_TZ, body)
            first, last = (line.split()[1] for line in body.splitlines())
            self.assertLess(first, last)
            self.assertEqual(LOCAL_ELAPSED,
                             clock_seconds(last) - clock_seconds(first))


class StaleManifest(unittest.TestCase):
    """Item 2: no manifest survives a run that does not seal."""

    @property
    def files(self) -> dict[str, str | bytes]:
        return {
            "HANDOFF.md": "# Handoff\n\nSee [gone](logs/gone.txt).\n",
            "logs/present.txt": f"path {HOME}/work\n",
            "MANIFEST.sha256": "0" * 64 + "  logs/present.txt\n",
        }

    def test_failing_seal_removes_the_previous_manifest(self):
        with Package(self.files) as package:
            code, out, _err = package.run()
            self.assertEqual(1, code)
            self.assertFalse(package.exists("MANIFEST.sha256"), out)
            # And the removal happened BEFORE normalization: the member was
            # rewritten, which is exactly what would have made the old
            # manifest describe bytes the package no longer has.
            self.assertIn("$HOME", package.read("logs/present.txt"))
            self.assertNotIn(HOME, package.read("logs/present.txt"))

    def test_failing_check_only_keeps_the_manifest_it_promised_not_to_touch(self):
        """CORRECTED ORACLE (V7), and the V6 review found it.

        This pinned `--check-only` DELETING `MANIFEST.sha256` on any failure,
        in a mode documented as "scan and report; never rewrite a member" and
        which `PRIVACY-AUDIT.md` instructs a REVIEWER to run against a sealed
        package. The same document concedes the account-name pattern raises a
        false hit on an operator whose username is an ordinary English word,
        so a reviewer named `will` was told to run a read-only check and had
        the package's integrity proof destroyed by it.

        The staleness the removal answers is real and belongs to the WRITING
        path, where `normalize()` rewrites bytes before the gate: that case is
        `test_failing_seal_removes_the_previous_manifest` above and is
        unchanged. `--check-only` normalizes nothing, so nothing can go stale
        and nothing is removed.
        """
        with Package(self.files) as package:
            before = package.read("MANIFEST.sha256")
            code, out, _err = package.run("--check-only")
            self.assertEqual(1, code)
            self.assertTrue(package.exists("MANIFEST.sha256"), out)
            self.assertEqual(before, package.read("MANIFEST.sha256"),
                             "a read-only mode rewrote a package member")
            # --check-only still rewrites nothing else either.
            self.assertIn(HOME, package.read("logs/present.txt"))

    def test_a_failing_verify_removes_nothing_either(self):
        with Package(self.files) as package:
            before = package.read("MANIFEST.sha256")
            code, _out, _err = package.run("--verify")
            self.assertEqual(1, code)
            self.assertEqual(before, package.read("MANIFEST.sha256"))

    def test_successful_seal_writes_a_fresh_manifest(self):
        files = {
            "HANDOFF.md": "# Handoff\n\nSee [present](logs/present.txt).\n",
            "logs/present.txt": "clean\n",
            "MANIFEST.sha256": "0" * 64 + "  logs/present.txt\n",
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            body = package.read("MANIFEST.sha256")
            self.assertNotIn("0" * 64, body)
            self.assertIn("logs/present.txt", body)


class FalsePositives(unittest.TestCase):
    """Item 3: ordinary coordinates, versions, times and digests seal cleanly.

    Written out literally on purpose: every string here must fail every check,
    and this file is scanned by those checks.
    """

    BENIGN = [
        '{"x":12.5,"y":34.0}',
        '{"scrollHeight":900.0,"scrollWidth":1440.0}',
        "width:1440.0;height:900.0",
        "elapsed 12:34:56.789",
        "node 10.24.1",
        "viewport 10.20.30",
        "chromium 120.0.6099.109",
        "range 10:00-11:30",
        "md5  d41d8cd98f00b204e9800998ecf8427e",
        "digest 5d41402abc4b2a76b9719d911017c592 of the payload",
        "sha1 356a192b7913b04c54574d18c28d46e6395428ab",
    ]

    def test_benign_data_is_not_flagged(self):
        for one in self.BENIGN:
            with self.subTest(text=one):
                self.assertEqual(set(), labels(one))

    def test_benign_data_is_not_rewritten(self):
        for one in self.BENIGN:
            with self.subTest(text=one):
                self.assertEqual(one, normalized(one))

    def test_a_probe_package_full_of_coordinates_seals(self):
        files = {
            "HANDOFF.md": "# Handoff\n\nSee [probe](logs/probe.json).\n",
            "logs/probe.json": (
                '{"viewport":{"x":12.5,"y":34.0,"width":1440.0},'
                '"scrollHeight":900.0,"t":"12:34:56.789",'
                '"build":"10.24.1","md5":"d41d8cd98f00b204e9800998ecf8427e",'
                '"window":"10:00-11:30"}\n'),
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            self.assertIn("0 private-token hit(s)", out)


class PreservedDetections(unittest.TestCase):
    """Item 3 again, from the other side: nothing real was given up."""

    CASES = [
        ("dbus-name", f"NAME {DBUS_A} ACTIVATABLE"),
        ("dbus-name", f"sender={DBUS_B} destination=org.freedesktop.DBus"),
        ("dbus-name", f"({DBUS_C})"),
        ("account-name", f"COMMAND {USER} 0.4 chrome"),
        ("hostname", f"connected to {HOST} ok"),
        ("home-path", OTHER_HOME),
        ("home-literal", f"{HOME}/git/thing"),
        ("session-bus", f"/run/user/{UID}/bus"),
        ("user-slice", f"user@{UID}.service"),
        ("uid-labelled", f"Uid:\t{UID}\t{UID}"),
        ("uid-pair", f"--user {UID}:{UID}"),
        ("pid", f"pid={PID}"),
        ("proc-pid", f"{PROC_STATUS}"),
        ("email", f"{EMAIL}"),
        ("uuid", f"{UUID_HYPHENATED}"),
        ("uuid-compact", f"machine-id: {MACHINE_HEX}"),
        ("uuid-compact", '"targetId":"%s"' % MACHINE_HEX),
        ("private-ip", f"bound to {IP_PRIVATE}"),
        ("private-ip", f"gateway {IP_GATEWAY}"),
        ("loopback", f"http://{LOOPBACK_PORT}/json"),
        ("scratch-dir", SCRATCH),
        ("iana-timezone", "TZ file " + zone("Europe", "Berlin")),
    ]

    def test_private_tokens_are_still_flagged(self):
        for label, text in self.CASES:
            with self.subTest(label=label, text=text):
                self.assertIn(label, labels(text))

    def test_private_tokens_are_still_repaired(self):
        for label, text in self.CASES:
            with self.subTest(label=label, text=text):
                self.assertNotEqual(set(), labels(text))
                self.assertEqual(set(), labels(normalized(text)),
                                 f"{label}: {normalized(text)!r}")

    def test_public_addresses_stay_exempt(self):
        # Literal on purpose: these are published identities, they must not
        # match, and this file is scanned by the check that would match them.
        for one in ("Co-Authored-By: Claude <noreply@anthropic.com>",
                    "1234+name@users.noreply.github.com",
                    "dbus-broker@bus.service"):
            with self.subTest(text=one):
                self.assertNotIn("email", labels(one))

    def test_a_leaky_package_is_refused(self):
        files = {
            "HANDOFF.md": "# Handoff\n\nSee [log](logs/busctl.txt).\n",
            "logs/busctl.txt": f"NAME {DBUS_A} PID {PID}\n",
        }
        with Package(files) as package:
            # --check-only never rewrites, so the hits stand.
            code, out, err = package.run("--check-only")
            self.assertEqual(1, code)
            self.assertIn("[dbus-name]", out)
            self.assertIn("REFUSING TO SEAL", err)


class IndexCheck(unittest.TestCase):
    """Item 4: bare names count, and resolution is against the package root."""

    def test_missing_top_level_artifact_is_detected(self):
        files = {
            "HANDOFF.md": ("# Handoff\n\nThe results are in `checks.txt` and "
                           "the diff is `changes.patch`.\n"),
            "checks.txt": "ok\n",
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(1, code)
            self.assertIn("changes.patch", out)
            self.assertIn("referenced but absent", out)
            self.assertNotIn("checks.txt (referenced", out)
            self.assertIn("evidence index is incomplete", err)

    def test_a_document_may_name_the_manifest_this_tool_writes(self):
        """The manifest is written AFTER the index check, by this tool.

        A document that names it names something the sealed package really
        contains. Refusing the reference because the file does not exist yet is
        an ordering bug in the checker, and it made a package that documents its
        own integrity proof unsealable.
        """
        files = {
            "LIMITATIONS.md": ("# Limitations\n\n`MANIFEST.sha256` is the "
                               "content proof and survives repacking.\n"),
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, err)
            self.assertNotIn("MANIFEST.sha256 (referenced", out)
            self.assertIn("0 missing reference(s)", out)
            self.assertTrue((package.root / "MANIFEST.sha256").exists(),
                            "and the manifest it named is really written")

    def test_external_references_are_not_package_members(self):
        files = {
            "HANDOFF.md": (
                "# Handoff\n\n"
                "See [upstream](https://example.org/thing.html), "
                "[mail](mailto:someone@users.noreply.github.com), "
                "[anchor](#results), the repository file `src/main.rs`, "
                "`tools/checker.py`, and [local](notes.md).\n"),
            "notes.md": "notes\n",
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            self.assertIn("0 missing reference(s)", out)

    def test_wrong_directory_reference_does_not_pass(self):
        # `shot.png` sits beside the referring document, but the reference is
        # written as a package-root path that does not exist.
        files = {
            "logs/NOTES.md": "# Notes\n\nSee [shot](shot.png).\n",
            "logs/shot.png": "not really a png\n",
        }
        with Package(files) as package:
            code, out, _err = package.run()
            self.assertEqual(1, code)
            self.assertIn("logs/NOTES.md -> shot.png", out)

    def test_unreferenced_members_are_reported_as_data(self):
        files = {
            "HANDOFF.md": "# Handoff\n\nnothing linked here\n",
            "logs/orphan.txt": "nobody points at me\n",
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            self.assertIn("unreferenced: logs/orphan.txt", out)


class VerifyMode(unittest.TestCase):
    """Item 5: the seal, and the archive digest, are actually checked."""

    FILES = {
        "HANDOFF.md": "# Handoff\n\nSee [log](logs/run.txt).\n",
        "logs/run.txt": "clean output\n",
    }

    def seal(self, package: Package) -> None:
        code, out, err = package.run()
        self.assertEqual(0, code, out + err)

    def test_verify_passes_on_a_sealed_package(self):
        with Package(dict(self.FILES)) as package:
            self.seal(package)
            code, out, err = package.run("--verify")
            self.assertEqual(0, code, out + err)
            self.assertIn("0 problem(s)", out)

    def test_verify_writes_nothing(self):
        with Package(dict(self.FILES)) as package:
            self.seal(package)
            before = {path: path.read_bytes()
                      for path in sealer.members(package.root)}
            package.run("--verify")
            after = {path: path.read_bytes()
                     for path in sealer.members(package.root)}
            self.assertEqual(before, after)

    def test_verify_fails_on_a_tampered_member(self):
        with Package(dict(self.FILES)) as package:
            self.seal(package)
            (package.root / "logs/run.txt").write_text("tampered\n",
                                                       encoding="utf-8")
            code, out, err = package.run("--verify")
            self.assertEqual(1, code)
            self.assertIn("digest mismatch: logs/run.txt", out)
            self.assertIn("VERIFY FAILED", err)

    def test_verify_fails_on_a_removed_or_added_member(self):
        with Package(dict(self.FILES)) as package:
            self.seal(package)
            (package.root / "logs/run.txt").unlink()
            (package.root / "logs/extra.txt").write_text("new\n",
                                                         encoding="utf-8")
            code, out, _err = package.run("--verify")
            self.assertEqual(1, code)
            self.assertIn("missing: logs/run.txt", out)
            self.assertIn("unlisted member: logs/extra.txt", out)

    def _zip_it(self, package: Package, *, rooted: bool = True) -> Path:
        """The archive as the protocol requires it: the package DIRECTORY is
        the single top-level entry.

        V7 CORRECTION. This built the archive with the members at the root,
        which is what `guidance/external-review-handoffs.md` forbids and the
        opposite of what the real shipped archives do — and nothing noticed,
        because the two tests using it only ever compared the archive's own
        bytes to a digest computed from those same bytes. Now that
        `--verify` proves the ZIP's members against the manifest, a helper
        that builds the wrong shape is a failing test rather than a silent
        disagreement between the tool and its own protocol. `rooted=False`
        keeps the old shape so the mis-rooted archive can be pinned as the
        finding it is.
        """
        archive = package.root.parent / (package.root.name + ".zip")
        prefix = (package.root.name + "/") if rooted else ""
        with zipfile.ZipFile(archive, "w") as handle:
            for path in sealer.members(package.root):
                handle.write(path,
                             prefix + path.relative_to(package.root).as_posix())
        return archive

    def _sidecar_for(self, archive: Path) -> None:
        recorded = hashlib.sha256(archive.read_bytes()).hexdigest()
        archive.with_suffix(".zip.sha256").write_text(
            f"{recorded}  {archive.name}\n", encoding="utf-8")

    def test_verify_proves_every_archive_member_against_the_manifest(self):
        """V7. The ZIP is what a reviewer receives, and V6 never opened it.

        The tree was proved against the manifest and the archive against its
        sidecar, and nothing joined the two — so an archive built from a
        different tree verified clean, because its sidecar is always computed
        from it after the fact.
        """
        with Package(dict(self.FILES)) as package:
            self.seal(package)
            # An archive whose LOGS/RUN.TXT differs from the sealed tree's,
            # built cleanly rather than by appending a duplicate entry — a
            # duplicate would be caught by the ZIP format itself and would
            # prove nothing about the check under test.
            archive = package.root.parent / (package.root.name + ".zip")
            with zipfile.ZipFile(archive, "w") as handle:
                for path in sealer.members(package.root):
                    relative = path.relative_to(package.root).as_posix()
                    name = package.root.name + "/" + relative
                    if relative == "logs/run.txt":
                        handle.writestr(name, "tampered\n")
                    else:
                        handle.write(path, name)
            self._sidecar_for(archive)
            code, out, err = package.run("--verify")
            self.assertEqual(1, code, out + err)
            self.assertIn("archive member does not match the manifest:"
                          " logs/run.txt", out)
            self.assertIn("archive verify: package.zip matches", out,
                          "the sidecar still agrees, which is the whole point")

    def test_verify_names_a_member_the_archive_carries_and_the_seal_does_not(self):
        with Package(dict(self.FILES)) as package:
            self.seal(package)
            archive = self._zip_it(package)
            with zipfile.ZipFile(archive, "a") as handle:
                handle.writestr(package.root.name + "/logs/smuggled.txt", "x\n")
            self._sidecar_for(archive)
            code, out, _err = package.run("--verify")
            self.assertEqual(1, code)
            self.assertIn("archive carries an unlisted member:"
                          " logs/smuggled.txt", out)

    def test_verify_names_a_member_the_archive_omits(self):
        with Package(dict(self.FILES)) as package:
            self.seal(package)
            archive = package.root.parent / (package.root.name + ".zip")
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr(package.root.name + "/HANDOFF.md",
                                package.read("HANDOFF.md"))
            self._sidecar_for(archive)
            code, out, _err = package.run("--verify")
            self.assertEqual(1, code)
            self.assertIn("archive omits: logs/run.txt", out)

    def test_verify_refuses_an_archive_that_is_not_rooted_at_the_package(self):
        """The layout the protocol requires, asserted rather than assumed."""
        with Package(dict(self.FILES)) as package:
            self.seal(package)
            archive = self._zip_it(package, rooted=False)
            self._sidecar_for(archive)
            code, out, _err = package.run("--verify")
            self.assertEqual(1, code)
            self.assertIn("archive member outside package/", out)

    def test_verify_checks_the_archive_digest(self):
        with Package(dict(self.FILES)) as package:
            self.seal(package)
            archive = self._zip_it(package)
            recorded = hashlib.sha256(archive.read_bytes()).hexdigest()
            sidecar = archive.with_suffix(".zip.sha256")
            sidecar.write_text(f"{recorded}  {archive.name}\n", encoding="utf-8")
            code, out, err = package.run("--verify")
            self.assertEqual(0, code, out + err)
            self.assertIn("matches", out)

    def test_verify_fails_on_a_wrong_archive_digest(self):
        with Package(dict(self.FILES)) as package:
            self.seal(package)
            archive = self._zip_it(package)
            sidecar = archive.with_suffix(".zip.sha256")
            sidecar.write_text(f"{'a' * 64}  {archive.name}\n", encoding="utf-8")
            code, out, err = package.run("--verify")
            self.assertEqual(1, code)
            self.assertIn("archive digest mismatch", out)
            self.assertIn("VERIFY FAILED", err)

    def test_a_changed_file_at_the_repository_root_is_not_a_package_reference(self):
        """V7. `EXTERNAL_REFERENCE` knows a repository's directory prefixes and
        cannot know its root-level filenames, so a document naming a changed
        file like `PROJECT-WORK.md` read as a dangling package reference. The
        package's own changed-file record names exactly the repository paths,
        by construction."""
        files = {
            "HANDOFF.md": ("# Handoff\n\nChanged: `PROJECT-WORK.md` and\n"
                           "`notes.toml`; see [run](logs/run.txt).\n"),
            "changed-files.txt": ("# parent x\n# head y\n\n"
                                  "M\tPROJECT-WORK.md\n"
                                  "M\tnotes.toml\n"
                                  "R100\told.md\tnotes.toml\n"),
            "logs/run.txt": "ok\n",
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            self.assertIn("0 missing reference(s)", out)

    def test_a_dangling_reference_is_still_caught_beside_one(self):
        files = {
            "HANDOFF.md": ("# Handoff\n\n`PROJECT-WORK.md` and `gone.json`;\n"
                           "see [run](logs/run.txt).\n"),
            "changed-files.txt": "M\tPROJECT-WORK.md\n",
            "logs/run.txt": "ok\n",
        }
        with Package(files) as package:
            code, out, _err = package.run()
            self.assertEqual(1, code)
            self.assertIn("gone.json", out)
            self.assertNotIn("-> PROJECT-WORK.md", out)

    def test_verify_needs_a_manifest(self):
        with Package(dict(self.FILES)) as package:
            code, _out, err = package.run("--verify")
            self.assertEqual(1, code)
            self.assertIn("no MANIFEST.sha256", err)


class ScreenshotPairs(unittest.TestCase):
    """Item 6: an identical pair described as showing a difference is refused."""

    IMAGE = b"\x89PNG\r\n\x1a\n" + b"pretend pixels" * 8
    OTHER = b"\x89PNG\r\n\x1a\n" + b"different pixels" * 8

    def files(self, after: bytes, prose: str) -> dict[str, str | bytes]:
        return {
            "HANDOFF.md": (
                "# Handoff\n\n"
                "Evidence: [before](logs/before--viewport.png) and "
                "[after](logs/after--viewport.png).\n\n"
                + prose + "\n"),
            "logs/before--viewport.png": self.IMAGE,
            "logs/after--viewport.png": after,
        }

    def test_identical_pair_with_a_difference_claim_fails(self):
        prose = ("The after frame is visibly different: the banner is no "
                 "longer clipped in logs/after--viewport.png.")
        with Package(self.files(self.IMAGE, prose)) as package:
            code, out, err = package.run()
            self.assertEqual(1, code)
            self.assertIn("1 byte-identical", out)
            self.assertIn("byte-identical", err)
            self.assertFalse(package.exists("MANIFEST.sha256"))

    def test_identical_pair_with_an_accurate_description_passes(self):
        prose = ("logs/after--viewport.png shows no visual difference from "
                 "the before frame; the two files are byte-identical.")
        with Package(self.files(self.IMAGE, prose)) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            self.assertIn("1 byte-identical", out)

    def test_differing_pair_with_a_difference_claim_passes(self):
        prose = ("The after frame is visibly different: the banner is no "
                 "longer clipped in logs/after--viewport.png.")
        with Package(self.files(self.OTHER, prose)) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            self.assertIn("0 byte-identical, 1 differing", out)

    def test_pairs_are_reported_as_data(self):
        prose = "Both frames are identical; see logs/after--viewport.png."
        with Package(self.files(self.IMAGE, prose)) as package:
            _code, out, _err = package.run()
            self.assertIn("identical  logs/viewport.png", out)

    def test_pair_detection_finds_the_pair(self):
        with Package(self.files(self.OTHER, "prose")) as package:
            rows = sealer.screenshot_pairs(package.root)
            self.assertEqual(
                [("logs/viewport.png", "logs/before--viewport.png",
                  "logs/after--viewport.png", False)], rows)


class Robustness(unittest.TestCase):
    """Item 7: late binary bytes, and honest truncation."""

    LATE_BINARY = b"a clean utf-8 head\n" + b"x" * 9000 + b"\xff\xfe not utf-8\n"

    def test_a_file_that_decodes_only_at_the_head_does_not_abort_the_run(self):
        files = {
            "HANDOFF.md": ("# Handoff\n\nSee [odd](logs/odd.bin) and "
                           "[home](logs/home.txt).\n"),
            "logs/odd.bin": self.LATE_BINARY,
            "logs/home.txt": f"{HOME}/git\n",
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            self.assertIn("not decodable as utf-8", out)
            self.assertIn("logs/odd.bin", out)
            # The other member was still normalized.
            self.assertIn("$HOME", package.read("logs/home.txt"))
            # And the undecodable member was left byte-for-byte alone.
            self.assertEqual(self.LATE_BINARY,
                             (package.root / "logs/odd.bin").read_bytes())

    def test_is_text_sniffs_only_the_head(self):
        with Package({"odd.bin": self.LATE_BINARY}) as package:
            path = package.root / "odd.bin"
            self.assertTrue(sealer.is_text(path))
            self.assertIsNone(sealer.read_text_or_none(path))

    def test_truncated_reporting_says_it_is_truncated(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            sealer.report([f"hit {n}" for n in range(60)], "hit")
        text = out.getvalue()
        self.assertIn("hit 49", text)
        self.assertNotIn("hit 50", text)
        self.assertIn("... 10 further hit(s) not shown", text)
        self.assertIn("showing the first 50 of 60", text)

    def test_short_reporting_says_nothing_extra(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            sealer.report(["only one"], "hit")
        self.assertNotIn("not shown", out.getvalue())


class SelfBlindness(unittest.TestCase):
    """Preserved: both shipped files are package members and pass the checks."""

    def test_the_sealer_seals_a_package_containing_itself(self):
        with Package({"logs/sanitize-and-seal.py":
                      SEALER_PATH.read_text(encoding="utf-8")}) as package:
            code, out, err = package.run("--check-only")
            self.assertEqual(0, code, out + err)
            self.assertIn("0 private-token hit(s)", out)

    def test_the_test_module_is_itself_sealable(self):
        """THE PIN. Every adversarial fixture in this file is composed at
        runtime; the moment one is written back as a raw literal, this fails
        here rather than at seal time, in the reviewer's package."""
        with Package({TEST_PATH.name:
                      TEST_PATH.read_text(encoding="utf-8")}) as package:
            hits, undecodable = sealer.scan(package.root,
                                            sealer.forbidden(WHO, ""))
            self.assertEqual([], hits)
            self.assertEqual([], undecodable)

    def test_the_shipped_pair_seals_together(self):
        files = {
            "HANDOFF.md": (
                "# Handoff\n\n"
                "The sealer is [logs/sanitize-and-seal.py]"
                "(logs/sanitize-and-seal.py) and its tests are "
                f"[logs/{TEST_PATH.name}](logs/{TEST_PATH.name}).\n"),
            "logs/sanitize-and-seal.py":
                SEALER_PATH.read_text(encoding="utf-8"),
            f"logs/{TEST_PATH.name}": TEST_PATH.read_text(encoding="utf-8"),
        }
        with Package(files) as package:
            code, out, err = package.run("--check-only")
            self.assertEqual(0, code, out + err)
            self.assertIn("0 private-token hit(s)", out)

    def test_a_private_value_written_as_a_literal_is_refused(self):
        found = sealer.own_source_literals(
            {"user": "sanitize", "host": HOST, "uid": UID, "home": HOME})
        self.assertIn("user", found)

    def test_clean_identities_pass_the_self_check(self):
        self.assertEqual([], sealer.own_source_literals(WHO))


class ManifestCoverage(unittest.TestCase):
    """Preserved: the manifest covers every member, itself excepted."""

    def test_manifest_lists_every_member(self):
        files = {
            "HANDOFF.md": "# Handoff\n\nSee [a](a.txt) and [b](logs/b.txt).\n",
            "a.txt": "a\n",
            "logs/b.txt": "b\n",
        }
        with Package(files) as package:
            code, out, err = package.run()
            self.assertEqual(0, code, out + err)
            rows = package.read("MANIFEST.sha256").strip().splitlines()
            names = {re.split(r"\s\s", row, maxsplit=1)[1] for row in rows}
            self.assertEqual({"HANDOFF.md", "a.txt", "logs/b.txt"}, names)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _row(root: Path, relative: str) -> dict:
    path = root / relative
    return {"path": relative, "bytes": path.stat().st_size,
            "sha256": _sha(path)}


class PipelineModes(unittest.TestCase):
    """V9: the seal is two modes, and check-only asks the fixpoint question."""

    def test_normalize_only_normalizes_and_writes_no_manifest(self):
        files = {
            "HANDOFF.md": "# Handoff\n\nSee [log](logs/present.txt).\n",
            "logs/present.txt": f"path {HOME}/work\n",
        }
        with Package(files) as package:
            code, out, err = package.run("--normalize-only")
            self.assertEqual(0, code, out + err)
            self.assertIn("$HOME", package.read("logs/present.txt"))
            self.assertFalse(package.exists("MANIFEST.sha256"),
                             "normalize-only must never write a manifest")
            self.assertIn("no manifest written", out)

    def test_check_only_fails_a_tree_the_table_would_still_touch(self):
        files = {
            "HANDOFF.md": "# Handoff\n\nSee [log](logs/present.txt).\n",
            "logs/present.txt": f"path {HOME}/work\n",
        }
        with Package(files) as package:
            before = package.read("logs/present.txt")
            code, out, err = package.run("--check-only")
            self.assertEqual(1, code)
            self.assertIn("would-be substitution(s)", out)
            self.assertIn("NOT AT A FIXPOINT", err)
            # And it really was a dry run.
            self.assertEqual(before, package.read("logs/present.txt"))

    def test_check_only_reports_zero_would_be_on_a_clean_tree(self):
        files = {
            "HANDOFF.md": "# Handoff\n\nSee [log](logs/present.txt).\n",
            "logs/present.txt": "clean\n",
        }
        with Package(files) as package:
            code, out, err = package.run("--check-only")
            self.assertEqual(0, code, out + err)
            self.assertIn("0 would-be substitution(s)", out)

    def test_a_deferred_reference_may_be_absent(self):
        files = {"HANDOFF.md":
                 "# Handoff\n\nThe seal transcript is `logs/seal.log`.\n"}
        with Package(files) as package:
            code, out, _err = package.run("--check-only",
                                          "--defer", "logs/seal.log")
            self.assertEqual(0, code, out)
            self.assertIn("deferred", out)
        with Package(files) as package:
            code, out, _err = package.run("--check-only")
            self.assertEqual(1, code,
                             "an undeclared absence must still fail")
            self.assertIn("referenced but absent", out)

    def _frozen_package(self) -> dict[str, str]:
        return {
            "HANDOFF.md": "# Handoff\n\nSee [log](logs/a.txt).\n",
            "logs/a.txt": "alpha\n",
        }

    def _write_claims(self, package: Package) -> None:
        rows = [_row(package.root, one)
                for one in ("HANDOFF.md", "logs/a.txt")]
        claims = {"package": {"rows": rows,
                              "evidence_members": len(rows),
                              "evidence_bytes": sum(r["bytes"] for r in rows),
                              "derived_members": [
                                  {"path": "claims.json",
                                   "reason": "written after the freeze"},
                                  {"path": "MANIFEST.sha256",
                                   "reason": "written by the manifest phase"}]}}
        (package.root / "claims.json").write_text(
            json.dumps(claims, indent=1, sort_keys=True) + "\n",
            encoding="utf-8")

    def test_manifest_only_seals_a_held_freeze(self):
        with Package(self._frozen_package()) as package:
            self._write_claims(package)
            code, out, err = package.run("--manifest-only", "--claims",
                                         str(package.root / "claims.json"))
            self.assertEqual(0, code, out + err)
            self.assertIn("0 drifted", out)
            body = package.read("MANIFEST.sha256")
            for member in ("HANDOFF.md", "logs/a.txt", "claims.json"):
                self.assertIn(member, body,
                              "the manifest covers every member, itself "
                              "excepted")

    def test_manifest_only_refuses_a_drifted_frozen_row(self):
        with Package(self._frozen_package()) as package:
            self._write_claims(package)
            (package.root / "logs/a.txt").write_text("altered\n",
                                                     encoding="utf-8")
            code, out, err = package.run("--manifest-only", "--claims",
                                         str(package.root / "claims.json"))
            self.assertEqual(1, code)
            self.assertIn("drifted after the freeze", out + err)
            self.assertFalse(package.exists("MANIFEST.sha256"),
                             "no manifest may describe a broken freeze")

    def test_manifest_only_never_rewrites_a_member(self):
        files = {
            "HANDOFF.md": "# Handoff\n\nSee [log](logs/a.txt).\n",
            "logs/a.txt": f"path {HOME}/work\n",
        }
        with Package(files) as package:
            self._write_claims(package)
            before = package.read("logs/a.txt")
            code, _out, err = package.run("--manifest-only", "--claims",
                                          str(package.root / "claims.json"))
            self.assertEqual(1, code, "a leaky tree still cannot acquire "
                                      "a manifest")
            self.assertIn("private tokens", err)
            self.assertEqual(before, package.read("logs/a.txt"),
                             "manifest-only rewrote a member")


class FreezeAndPartition(unittest.TestCase):
    """V9: the snapshot is the inventory, and the partition is the invariant."""

    def test_freeze_rows_snapshot_the_current_bytes(self):
        with Package({"a.txt": "alpha\n", "logs/b.txt": "beta\n"}) as package:
            rows = deriver.freeze_rows(package.root)
            self.assertEqual(["a.txt", "logs/b.txt"],
                             [one["path"] for one in rows])
            for one in rows:
                path = package.root / one["path"]
                self.assertEqual(path.stat().st_size, one["bytes"])
                self.assertEqual(_sha(path), one["sha256"])

    def test_derived_members_carry_only_a_path_and_a_reason(self):
        for one in deriver.package_members([])["derived_members"]:
            self.assertEqual({"path", "reason"}, set(one),
                             "a derived member is named, never sized "
                             "or hashed")

    def test_package_section_sums_only_the_frozen_rows(self):
        rows = [{"path": "a.txt", "bytes": 3, "sha256": "0" * 64},
                {"path": "b.txt", "bytes": 4, "sha256": "1" * 64}]
        section = deriver.package_members(rows)
        self.assertEqual(2, section["evidence_members"])
        self.assertEqual(7, section["evidence_bytes"])
        self.assertNotIn("members", section)
        self.assertNotIn("bytes", section,
                         "claims.json must not carry a package total; the "
                         "manifest and the sidecar are the authority")

    def test_partition_problems_flags_a_member_in_both_sets(self):
        found = deriver.partition_problems({"a"}, {"a"}, {"a"})
        self.assertTrue(any("both" in one for one in found), found)

    def test_partition_problems_flags_a_member_in_neither_set(self):
        found = deriver.partition_problems({"a", "b"}, {"a"}, set())
        self.assertTrue(any("neither" in one for one in found), found)

    def test_partition_problems_flags_a_vanished_row(self):
        found = deriver.partition_problems(set(), {"a"}, set())
        self.assertTrue(any("gone" in one for one in found), found)

    def test_an_exact_partition_raises_no_problem(self):
        self.assertEqual([], deriver.partition_problems(
            {"a", "b"}, {"a"}, {"b"}))


class FrozenDriftAudit(unittest.TestCase):
    """V9: head-consistency hard-fails undeclared drift instead of printing it."""

    HEAD = "a" * 40
    PARENT = "b" * 40

    def _package(self, *, derived, tamper=None, extra=None) -> Package:
        files = {
            "INDEX.md": ("# Index\n\nMembers: `INDEX.md`, `logs/a.txt`,\n"
                         "`claims.json`, `logs/late.log`.\n"),
            "logs/a.txt": "alpha\n",
        }
        package = Package(files)
        rows = [_row(package.root, one) for one in ("INDEX.md", "logs/a.txt")]
        claims = {
            "identity": {"head": self.HEAD, "parent": self.PARENT,
                         "review_addressed": ""},
            "commits": [],
            "package": {"rows": rows, "derived_members": derived},
        }
        (package.root / "claims.json").write_text(
            json.dumps(claims, indent=1, sort_keys=True) + "\n",
            encoding="utf-8")
        if extra:
            for relative, content in extra.items():
                target = package.root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
        if tamper:
            (package.root / tamper).write_text("moved after the freeze\n",
                                               encoding="utf-8")
        return package

    def _audit(self, package: Package, *flags: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), \
                contextlib.redirect_stderr(out):
            code = auditor.main(["--package", str(package.root), *flags])
        return code, out.getvalue()

    DECLARED = [{"path": "claims.json", "reason": "written by derivation"},
                {"path": "logs/late.log", "reason": "audit transcript"}]

    def test_declared_residue_passes(self):
        with self._package(derived=self.DECLARED,
                           extra={"logs/late.log": "late\n"}) as package:
            code, out = self._audit(package)
            self.assertEqual(0, code, out)

    def test_frozen_drift_is_a_hard_failure(self):
        with self._package(derived=self.DECLARED,
                           extra={"logs/late.log": "late\n"},
                           tamper="logs/a.txt") as package:
            code, out = self._audit(package)
            self.assertEqual(1, code, "V8 printed this as residue; V9 exits "
                                      "nonzero")
            self.assertIn("drifted after the freeze", out)

    def test_an_undeclared_late_write_is_a_hard_failure(self):
        declared = [{"path": "claims.json", "reason": "written by derivation"}]
        with self._package(derived=declared,
                           extra={"logs/late.log": "late\n"}) as package:
            code, out = self._audit(package)
            self.assertEqual(1, code)
            self.assertIn("without a derived_members declaration", out)

    def test_a_derived_member_carrying_bytes_is_refused(self):
        declared = [{"path": "claims.json", "reason": "written by derivation",
                     "bytes": 123},
                    {"path": "logs/late.log", "reason": "audit transcript"}]
        with self._package(derived=declared,
                           extra={"logs/late.log": "late\n"}) as package:
            code, out = self._audit(package)
            self.assertEqual(1, code)
            self.assertIn("named, never sized", out)

    def test_pending_permits_only_a_declared_absence(self):
        declared = self.DECLARED + [{"path": "MANIFEST.sha256",
                                     "reason": "written by the next phase"}]
        with self._package(derived=declared,
                           extra={"logs/late.log": "late\n"}) as package:
            code, out = self._audit(package)
            self.assertEqual(1, code, "a declared member that never arrived "
                                      "fails without --pending")
            self.assertIn("never written", out)
        with self._package(derived=declared,
                           extra={"logs/late.log": "late\n"}) as package:
            code, out = self._audit(package, "--pending", "MANIFEST.sha256")
            self.assertEqual(0, code, out)


class FinalVerifier(unittest.TestCase):
    """V9: the P8 checks, each driven against the failure it exists to catch."""

    def _zip_and_sidecar(self, scratch: Path, *, size_offset: int = 0,
                         drop_size: bool = False) -> tuple[Path, Path]:
        archive = scratch / "pkg.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("pkg/x.txt", "x\n")
        recorded = hashlib.sha256(archive.read_bytes()).hexdigest()
        size = archive.stat().st_size + size_offset
        body = f"{recorded}  {archive.name}\n"
        if not drop_size:
            body += f"{size} bytes  {archive.name}\n"
        sidecar = scratch / "pkg.zip.sha256"
        sidecar.write_text(body, encoding="utf-8")
        return archive, sidecar

    def test_a_correct_sidecar_passes(self):
        with tempfile.TemporaryDirectory() as scratch:
            archive, sidecar = self._zip_and_sidecar(Path(scratch))
            self.assertEqual([], verifier.check_sidecar(archive, sidecar))

    def test_a_wrong_sidecar_size_is_caught(self):
        with tempfile.TemporaryDirectory() as scratch:
            archive, sidecar = self._zip_and_sidecar(Path(scratch),
                                                     size_offset=7)
            found = verifier.check_sidecar(archive, sidecar)
            self.assertTrue(any("bytes" in one and "records" in one
                                for one in found), found)

    def test_a_sidecar_without_a_size_is_caught(self):
        with tempfile.TemporaryDirectory() as scratch:
            archive, sidecar = self._zip_and_sidecar(Path(scratch),
                                                     drop_size=True)
            found = verifier.check_sidecar(archive, sidecar)
            self.assertTrue(any("no byte size" in one for one in found),
                            found)

    def _extraction(self, scratch: Path) -> Path:
        root = scratch / "pkg"
        (root / "logs").mkdir(parents=True)
        (root / "logs/a.txt").write_text("alpha\n", encoding="utf-8")
        return root

    def _claims(self, root: Path, rows, derived) -> dict:
        return {"package": {
            "rows": rows,
            "evidence_members": len(rows),
            "evidence_bytes": sum(one["bytes"] for one in rows),
            "derived_members": derived}}

    def test_a_stale_claims_row_is_caught(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = self._extraction(Path(scratch))
            row = _row(root, "logs/a.txt")
            good = self._claims(root, [row], [])
            self.assertEqual([], verifier.check_claims_rows(good, root))
            stale = dict(row, bytes=row["bytes"] + 1822)
            claims = self._claims(root, [stale], [])
            claims["package"]["evidence_bytes"] = stale["bytes"]
            found = verifier.check_claims_rows(claims, root)
            self.assertTrue(any("stale row" in one for one in found), found)

    def test_evidence_sums_are_checked(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = self._extraction(Path(scratch))
            claims = self._claims(root, [_row(root, "logs/a.txt")], [])
            claims["package"]["evidence_bytes"] += 1
            found = verifier.check_claims_rows(claims, root)
            self.assertTrue(any("evidence_bytes" in one for one in found),
                            found)

    def test_a_member_in_neither_rows_nor_derived_is_caught(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = self._extraction(Path(scratch))
            (root / "smuggled.txt").write_text("late\n", encoding="utf-8")
            claims = self._claims(root, [_row(root, "logs/a.txt")], [])
            found = verifier.check_partition(claims, root)
            self.assertTrue(any("smuggled.txt" in one and "neither" in one
                                for one in found), found)

    def test_a_member_in_both_rows_and_derived_is_caught(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = self._extraction(Path(scratch))
            row = _row(root, "logs/a.txt")
            claims = self._claims(root, [row],
                                  [{"path": "logs/a.txt", "reason": "also"}])
            found = verifier.check_partition(claims, root)
            self.assertTrue(any("both" in one for one in found), found)

    def test_a_sized_derived_member_is_caught_by_the_verifier_too(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = self._extraction(Path(scratch))
            (root / "claims.json").write_text("{}\n", encoding="utf-8")
            claims = self._claims(
                root, [_row(root, "logs/a.txt")],
                [{"path": "claims.json", "reason": "derived",
                  "sha256": "0" * 64}])
            found = verifier.check_partition(claims, root)
            self.assertTrue(any("named, never sized" in one for one in found),
                            found)

    def test_an_exact_partition_passes(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = self._extraction(Path(scratch))
            (root / "claims.json").write_text("{}\n", encoding="utf-8")
            claims = self._claims(root, [_row(root, "logs/a.txt")],
                                  [{"path": "claims.json",
                                    "reason": "derived"}])
            self.assertEqual([], verifier.check_partition(claims, root))

    def test_layout_catches_duplicates_wrong_roots_and_escapes(self):
        self.assertEqual([], verifier.check_layout(["pkg/a", "pkg/b"], "pkg"))
        self.assertTrue(any("duplicate" in one for one in
                            verifier.check_layout(["pkg/a", "pkg/a"], "pkg")))
        self.assertTrue(any("expected exactly" in one for one in
                            verifier.check_layout(["other/a"], "pkg")))
        up = _j("pkg", _SLASH, _DOT, _DOT, _SLASH, "x")
        self.assertTrue(any("escaping" in one for one in
                            verifier.check_layout([up], "pkg")))


class DuplicateRows(unittest.TestCase):
    """V10: a path listed twice is a named failure, not a silent collapse.

    Check 2 already catches duplicate ARCHIVE entries; these are the
    independent row-level checks over MANIFEST.sha256 and the claims.json
    frozen rows, where a duplicate collapses into a dict or double-counts a
    sum and the transcript then proves half of what it appears to."""

    def test_a_duplicate_claims_row_is_caught(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch) / "pkg"
            (root / "logs").mkdir(parents=True)
            (root / "logs/a.txt").write_text("alpha\n", encoding="utf-8")
            row = _row(root, "logs/a.txt")
            claims = {"package": {"rows": [row, dict(row)],
                                  "evidence_members": 2,
                                  "evidence_bytes": row["bytes"] * 2,
                                  "derived_members": []}}
            found = verifier.check_claims_rows(claims, root)
            self.assertTrue(any("duplicate claims row" in one
                                for one in found), found)

    def test_a_duplicate_manifest_row_is_caught(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch) / "pkg"
            root.mkdir(parents=True)
            (root / "a.txt").write_text("alpha\n", encoding="utf-8")
            line = f"{_sha(root / 'a.txt')}  a.txt\n"
            (root / "MANIFEST.sha256").write_text(line + line,
                                                  encoding="utf-8")
            found = verifier.check_manifest(root)
            self.assertEqual(["duplicate manifest row: a.txt"], found,
                             "the duplicate is the only problem; the digest "
                             "itself matches")

    def test_unduplicated_rows_raise_no_duplicate_problem(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch) / "pkg"
            (root / "logs").mkdir(parents=True)
            (root / "logs/a.txt").write_text("alpha\n", encoding="utf-8")
            row = _row(root, "logs/a.txt")
            claims = {"package": {"rows": [row], "evidence_members": 1,
                                  "evidence_bytes": row["bytes"],
                                  "derived_members": []}}
            self.assertEqual([], verifier.check_claims_rows(claims, root))


class BindingHeader(unittest.TestCase):
    """V10: the P8 transcript names the exact archive it proves."""

    def _archive(self, scratch: Path) -> Path:
        archive = scratch / "pkg.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("pkg/x.txt", "x\n")
        return archive

    def test_header_carries_name_bytes_digest_root_and_utc_time(self):
        with tempfile.TemporaryDirectory() as scratch:
            archive = self._archive(Path(scratch))
            hashed = _sha(archive)
            text = "\n".join(verifier.identity_header(archive, "pkg", hashed))
            self.assertIn("archive : pkg.zip", text)
            self.assertIn(f"bytes   : {archive.stat().st_size}", text)
            self.assertIn(hashed, text)
            self.assertIn("root    : pkg", text)
            self.assertRegex(text, r"\d{4}-\d\d-\d\dT\d\d.\d\d.\d\dZ \(UTC\)")

    def test_the_transcript_opens_with_the_header(self):
        with tempfile.TemporaryDirectory() as scratch:
            archive = self._archive(Path(scratch))
            recorded = _sha(archive)
            sidecar = Path(scratch) / "pkg.zip.sha256"
            sidecar.write_text(f"{recorded}  pkg.zip\n"
                               f"{archive.stat().st_size} bytes  pkg.zip\n",
                               encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), \
                    contextlib.redirect_stderr(err):
                code = verifier.main(["--zip", str(archive),
                                      "--sidecar", str(sidecar)])
            text = out.getvalue()
            self.assertEqual(1, code, "a bare archive cannot pass the audits;"
                                      " the header must appear regardless")
            self.assertIn("archive : pkg.zip", text)
            self.assertIn(recorded, text)
            self.assertIn("[1 sidecar] ok", text,
                          "and the hoisted digest still satisfies check 1")


# THE PIPELINE'S OWN STATE IS NOT INHERITED BY THE PIPELINE UNDER TEST.
#
# V11: `assemble.sh` runs this suite as one of its phases and exports its
# whole configuration before doing so, so a test that spawned `assemble.sh`
# or `battery.sh` with the ambient environment handed the run under test the
# REAL run's identity. Two things went wrong at once, and both are the same
# mistake. `ASSEMBLE_INNER` silently put the assembly under test into inner
# mode, where the refusal it printed was one line shorter than the refusal
# this suite asserts — a test failure that looked like a broken guard and was
# a broken harness. And `ATTEMPTS` pointed the throwaway batteries at the
# LANE'S OWN attempt ledger, so runs against temporary repositories appended
# rows there and a reader would have counted several authoritative head
# batteries where the lane ran one.
#
# A test that drives a fresh pipeline must give it a fresh environment. These
# names are CLEARED, never merely overwritten, because the defect was the
# ones the caller did not think to set.
PIPELINE_ENV = ("ASSEMBLE_INNER", "ATTEMPT", "ATTEMPT_NO", "ATTEMPTS",
                "TOOLS", "REPO", "PARENT", "REVIEW", "STAMP", "SRC",
                "NAME", "LANE", "MEASURED")


def unpiped(**extra: str) -> dict:
    """The ambient environment with the pipeline's own names removed."""
    return {**{name: value for name, value in os.environ.items()
               if name not in PIPELINE_ENV}, **extra}


class ProtocolRefusals(unittest.TestCase):
    """V10: an existing handoff target or battery record is refused, never
    removed, reused or overwritten. Driven through the real scripts under
    `bash`, because the refusal IS the interface."""

    STAMP = "20260101T000000Z"

    def _assemble(self, repo: Path) -> "subprocess.CompletedProcess[str]":
        return subprocess.run(
            ["bash", str(HERE / "assemble.sh")],
            env=unpiped(REPO=str(repo), STAMP=self.STAMP,
                        NAME="pkg", SRC=str(repo)),
            capture_output=True, text=True)

    def test_assemble_refuses_an_existing_package_directory(self):
        with tempfile.TemporaryDirectory() as scratch:
            repo = Path(scratch) / "repo"
            (repo / "build/agent-handoffs"
             / f"{self.STAMP}-pkg").mkdir(parents=True)
            done = self._assemble(repo)
            self.assertNotEqual(0, done.returncode)
            self.assertIn("REFUSING", done.stderr)
            self.assertIn("fresh UTC STAMP", done.stderr)
            self.assertTrue((repo / "build/agent-handoffs"
                             / f"{self.STAMP}-pkg").is_dir(),
                            "the refusal must not remove the existing target")

    def test_assemble_refuses_an_existing_archive(self):
        with tempfile.TemporaryDirectory() as scratch:
            repo = Path(scratch) / "repo"
            handoffs = repo / "build/agent-handoffs"
            handoffs.mkdir(parents=True)
            (handoffs / f"{self.STAMP}-pkg.zip").write_bytes(b"stale")
            done = self._assemble(repo)
            self.assertNotEqual(0, done.returncode)
            self.assertIn("REFUSING", done.stderr)
            self.assertEqual(b"stale",
                             (handoffs / f"{self.STAMP}-pkg.zip").read_bytes())

    def test_battery_refuses_an_existing_ledger(self):
        with tempfile.TemporaryDirectory() as scratch:
            logs = Path(scratch) / "logs"
            logs.mkdir()
            (logs / "order-head.txt").write_text("previous run\n",
                                                 encoding="utf-8")
            done = subprocess.run(
                ["bash", str(HERE / "battery.sh"), scratch, str(logs),
                 "head"],
                env=unpiped(), capture_output=True, text=True)
            self.assertNotEqual(0, done.returncode)
            self.assertIn("REFUSING", done.stderr)
            self.assertEqual("previous run\n",
                             (logs / "order-head.txt")
                             .read_text(encoding="utf-8"),
                             "the refusal must not touch the existing record")


class BatteryLedger(unittest.TestCase):
    """V10: provenance is emitted during execution, and every entry's log is
    unique. The battery runs against a throwaway git repository none of whose
    steps can succeed; the LEDGER is what is under test, and it must record
    the preflight, the postflight, and one indexed log path per entry."""

    def test_battery_writes_provenance_and_unique_indexed_logs(self):
        with tempfile.TemporaryDirectory() as scratch:
            repo = Path(scratch) / "repo"
            repo.mkdir()
            author = _j("t", _AT, "example", _DOT, "invalid")
            for cmd in (["git", "init", "-q"],
                        ["git", "-c", "user.email=" + author,
                         "-c", "user.name=t", "commit", "-q",
                         "--allow-empty", "-m", "seed"]):
                subprocess.run(cmd, cwd=repo, check=True,
                               capture_output=True)
            logs = Path(scratch) / "logs"
            done = subprocess.run(
                ["bash", str(HERE / "battery.sh"), str(repo), str(logs),
                 "head"],
                env=unpiped(), capture_output=True, text=True)
            self.assertEqual(0, done.returncode, done.stderr)
            ledger = (logs / "order-head.txt").read_text(encoding="utf-8")
            self.assertIn("PREFLIGHT battery=head", ledger)
            self.assertIn("POSTFLIGHT battery=head", ledger)
            self.assertIn("porcelain=clean", ledger)
            self.assertIn("cwd=" + "$" + "REPO", ledger,
                          "the cwd is the token, never the real path")
            self.assertIn("sha-drift=none", ledger)
            self.assertNotIn(str(repo), ledger,
                             "no real path may reach the ledger")
            recorded = re.findall(r"^LOG: (logs/\d\d-\S+)$", ledger, re.M)
            self.assertTrue(recorded, "every entry records its log path")
            self.assertEqual(len(recorded), len(set(recorded)),
                             "every ledger entry writes a unique log path")
            for one in recorded:
                self.assertTrue((logs / Path(one).name).is_file(), one)
            self.assertEqual(len(re.findall(r"^START ", ledger, re.M)),
                             len(recorded),
                             "one recorded log per started entry")


if __name__ == "__main__":
    unittest.main(verbosity=2)
