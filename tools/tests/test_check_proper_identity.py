"""A proper's identity is the calendar's to grant, and the tool must not invent one.

The check exists so that a scope-gate stage can refuse an unregistered 1962
proper before anything is written under its name, and a gate judges by exit
code alone. So the tests here come in two kinds. Most call the tool's own
functions, because that is where the precise refusal lives. Two run it as a
process, because a gate that reads exit status is buying the one thing an
in-process assertion cannot prove.

The last test is the one that would catch a real regression. It walks every
proper leaf both providers actually hold and asserts the tool agrees the
identity is registered. A rule derived from the calendar and a tree published
against the profile the calendar transcribes must not disagree; if they ever
do, one of the two is wrong and this is where it surfaces.

Ritual identities are the deliberate asymmetry. No mass entry in any calendar
here carries an `M` registry value -- the calendar transcribes the book's
temporal and sanctoral cycles, and a nuptial Mass is appointed by a rite rather
than by a day -- while `ritual/m01-nuptial-mass` is a real published leaf. So
the tool accepts an `m` prefix on grammar alone, and the test below pins the
part that keeps that honest: the success line has to SAY the check was grammar,
not enumeration, or a reader takes the exit code for something it is not.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "check-proper-identity"
LOADER = importlib.machinery.SourceFileLoader("triptych_proper_identity", str(TOOL))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {TOOL}")
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)

CALENDAR = "roman-1962"
COLLECTION = "liturgy/roman-rite/1962/propers"
PROVIDERS = ("gpt", "claude")


def leaf(klass: str, slug: str) -> str:
    return f"{COLLECTION}/{klass}/{slug}"


class IdentityFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registered = CHECKER.registered_identities(CHECKER.CALENDAR_ROOT, CALENDAR)

    def verified(self, document: str) -> str:
        identity = CHECKER.parse_identity(document)
        return CHECKER.verify(identity, self.registered, CALENDAR)

    def refusal(self, document: str) -> str:
        with self.assertRaises(ValueError) as raised:
            self.verified(document)
        return str(raised.exception)


class RegisteredIdentityTests(IdentityFixture):
    def test_the_calendar_registers_the_catalog_series_and_nothing_else(self) -> None:
        """01-68 and F01: the synthetic registry ids are not identities."""
        self.assertEqual(
            list(self.registered),
            [f"{number:02d}" for number in range(1, 69)] + ["f01"],
        )

    def test_a_registered_temporal_identity_passes(self) -> None:
        for slug in ("54-fourteenth-after-pentecost", "51-eleventh-after-pentecost"):
            with self.subTest(slug=slug):
                line = self.verified(leaf("temporal", slug))
                self.assertIn("is registered in the roman-1962 calendar", line)
                self.assertIn(slug, line)

    def test_an_unregistered_numeric_identity_fails_closed(self) -> None:
        message = self.refusal(leaf("temporal", "99-invented-sunday"))
        self.assertIn("'99'", message)
        self.assertIn("registered by no mass entry", message)

    def test_the_f_series_resolves_case_insensitively(self) -> None:
        """The path spells it `f01`; the calendar spells it `F01`."""
        self.assertIn("F01", [
            mass["registry"]
            for mass in CHECKER._calendars.mass_index(
                CHECKER._calendars.load_document(CHECKER.CALENDAR_ROOT, CALENDAR)
            ).values()
            if isinstance(mass.get("registry"), str)
        ])
        line = self.verified(leaf("temporal", "f01-christ-the-king"))
        self.assertIn("Identity f01 is registered", line)


class GrammarTests(IdentityFixture):
    def test_a_malformed_path_fails_closed(self) -> None:
        for document in (
            "propers/temporal/54-fourteenth-after-pentecost",
            "liturgy/roman-rite/1970/propers/temporal/54-fourteenth-after-pentecost",
            "liturgy/roman-rite/1962/propers/votive/54-fourteenth-after-pentecost",
            "54-fourteenth-after-pentecost",
            "",
        ):
            with self.subTest(document=document):
                self.assertTrue(self.refusal(document))

    def test_a_slug_without_a_recognised_prefix_fails_closed(self) -> None:
        for slug in ("54", "54-", "fourteenth-after-pentecost", "540-x", "x54-y"):
            with self.subTest(slug=slug):
                self.assertIn("must be a two-digit", self.refusal(leaf("temporal", slug)))

    def test_a_slug_and_its_class_must_agree(self) -> None:
        self.assertIn(
            "belongs under ritual/", self.refusal(leaf("temporal", "m01-nuptial-mass"))
        )
        self.assertIn(
            "belongs under temporal/",
            self.refusal(leaf("ritual", "54-fourteenth-after-pentecost")),
        )
        self.assertIn(
            "belongs under temporal/", self.refusal(leaf("ritual", "f01-christ-the-king"))
        )


class RitualCeilingTests(IdentityFixture):
    def test_the_published_ritual_leaf_passes(self) -> None:
        self.assertTrue(
            (ROOT / "src" / "gpt" / COLLECTION / "ritual" / "m01-nuptial-mass").is_dir(),
            "the leaf this asymmetry exists for is gone; revisit the rule",
        )
        self.verified(leaf("ritual", "m01-nuptial-mass"))

    def test_no_calendar_entry_registers_an_m_identity(self) -> None:
        """The premise of the grammar-only rule, asserted rather than assumed."""
        self.assertEqual([one for one in self.registered if one.startswith("m")], [])

    def test_the_success_line_says_the_check_was_grammar_not_enumeration(self) -> None:
        line = self.verified(leaf("ritual", "m01-nuptial-mass"))
        self.assertIn("valid by path grammar only", line)
        self.assertIn("nothing here enumerates them", line)

    def test_an_unpublished_ritual_identity_also_passes(self) -> None:
        """Grammar cannot tell m02 from m01, and the tool must not pretend it can."""
        self.assertIn(
            "grammar only", self.verified(leaf("ritual", "m02-not-yet-written"))
        )


class PublishedTreeTests(IdentityFixture):
    """Every leaf on disk, both providers: the tool must agree with reality."""

    def leaves(self) -> list[tuple[str, str]]:
        found = []
        for provider in PROVIDERS:
            base = ROOT / "src" / provider / COLLECTION
            for klass in CHECKER.CLASSES:
                for path in sorted((base / klass).glob("*")):
                    if path.is_dir():
                        found.append((provider, leaf(klass, path.name)))
        return found

    def test_every_published_leaf_holds_a_valid_identity(self) -> None:
        leaves = self.leaves()
        self.assertGreaterEqual(len(leaves), 19, "the tree shrank; check the glob")
        for provider, document in leaves:
            with self.subTest(provider=provider, document=document):
                self.verified(document)

    def test_every_published_temporal_leaf_is_registered(self) -> None:
        temporal = [
            document for _, document in self.leaves() if f"/{CHECKER.TEMPORAL}/" in document
        ]
        self.assertTrue(temporal)
        for document in temporal:
            with self.subTest(document=document):
                self.assertIn("is registered in", self.verified(document))


class ExitStatusTests(unittest.TestCase):
    """A program gate reads the exit code and nothing else."""

    def run_tool(self, *argv: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOL), *argv],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )

    def test_a_registered_identity_exits_zero(self) -> None:
        result = self.run_tool(
            "--document", leaf("temporal", "54-fourteenth-after-pentecost")
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")

    def test_an_unregistered_identity_exits_one_with_the_error_on_stderr(self) -> None:
        result = self.run_tool("--document", leaf("temporal", "99-invented-sunday"))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.startswith(CHECKER.ERROR), result.stderr)

    def test_naming_neither_a_document_nor_a_listing_fails_rather_than_passes(self) -> None:
        result = self.run_tool()
        self.assertEqual(result.returncode, 1)
        self.assertIn("give --document ID, or --list", result.stderr)

    def test_an_unknown_calendar_fails_rather_than_reporting_an_empty_registry(self) -> None:
        result = self.run_tool(
            "--calendar", "no-such-calendar",
            "--document", leaf("temporal", "54-fourteenth-after-pentecost"),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot read calendar", result.stderr)

    def test_the_listing_prints_one_identity_a_line(self) -> None:
        result = self.run_tool("--list")
        self.assertEqual(result.returncode, 0, result.stderr)
        printed = result.stdout.strip().split("\n")
        self.assertEqual(len(printed), 69)
        self.assertEqual(printed, sorted(printed), "the listing must be byte-stable")
        self.assertEqual(printed[0], "01")
        self.assertEqual(printed[-1], "f01")


if __name__ == "__main__":
    unittest.main()
