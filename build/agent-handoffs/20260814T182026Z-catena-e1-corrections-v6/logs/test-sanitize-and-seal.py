#!/usr/bin/env python3
"""Tests for the V6 sealer.

Every behaviour changed in V6 is pinned here, together with regressions for
the privacy detections V6 preserves. Run it standalone:

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
import os
import re
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

HERE = Path(__file__).resolve().parent
SEALER_PATH = HERE / "sanitize-and-seal.py"
TEST_PATH = Path(__file__).resolve()

_spec = importlib.util.spec_from_file_location("sealer_under_test", SEALER_PATH)
assert _spec and _spec.loader
sealer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sealer)

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
        for one in self.OFFSETS:
            with self.subTest(text=one):
                self.assertIn("utc-offset", labels(one))
                self.assertIn(sealer.PLACEHOLDER_TZ, normalized(one))

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

    def test_failing_check_only_removes_the_previous_manifest(self):
        with Package(self.files) as package:
            code, out, _err = package.run("--check-only")
            self.assertEqual(1, code)
            self.assertFalse(package.exists("MANIFEST.sha256"), out)
            # --check-only still rewrites nothing.
            self.assertIn(HOME, package.read("logs/present.txt"))

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

    def _zip_it(self, package: Package) -> Path:
        archive = package.root.parent / (package.root.name + ".zip")
        with zipfile.ZipFile(archive, "w") as handle:
            for path in sealer.members(package.root):
                handle.write(path, path.relative_to(package.root).as_posix())
        return archive

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
