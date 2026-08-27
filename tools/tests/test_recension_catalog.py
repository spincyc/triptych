"""The recension catalog names support gaps without creating fake calendars."""

from __future__ import annotations

import copy
import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src" / "sources" / "calendars"
sys.path.insert(0, str(ROOT / "scripts"))

import _recensions  # noqa: E402
from _calendars import partition  # noqa: E402


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = SourceFileLoader(f"_{name.replace('-', '_')}", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


checker = load_tool("check-calendar-masses")


class RealCatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = _recensions.load_catalog(CALENDARS)

    def test_catalog_and_every_reference_validate(self) -> None:
        self.assertEqual(
            _recensions.catalog_problems(
                CALENDARS, repository=ROOT, required=True
            ),
            [],
        )

    def test_catalog_is_not_a_calendar_index_or_companion(self) -> None:
        indexes, companions, problems = partition(CALENDARS)
        self.assertEqual(problems, [])
        self.assertTrue(indexes)
        self.assertTrue(all(path.name == "propers.yaml" for path in indexes))
        self.assertNotIn(
            CALENDARS / _recensions.CATALOG,
            indexes,
        )
        self.assertFalse(
            any(row["path"].endswith(_recensions.CATALOG) for row in companions)
        )

    def test_every_named_book_state_and_the_english_expression_are_explicit(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.catalog["recensions"]],
            [
                "roman-1920",
                "roman-transition-1956-1960",
                "roman-1962",
                "roman-1970",
                "roman-1971-reimpressio-emendata",
                "roman-1975-editio-typica-altera",
                "roman-2002-editio-typica-tertia",
                "roman-2008-reimpressio-emendata",
            ],
        )
        self.assertEqual(
            [(row["id"], row["parent"]) for row in self.catalog["expressions"]],
            [("roman-missal-en-us-2011", "roman-2008-reimpressio-emendata")],
        )

    def test_transitional_gap_is_unavailable_and_cannot_be_discovered(self) -> None:
        transition = next(
            row
            for row in self.catalog["recensions"]
            if row["id"] == "roman-transition-1956-1960"
        )
        self.assertEqual(transition["kind"], "interval-gap")
        self.assertNotIn("calendar", transition)
        self.assertEqual(
            {
                row["data_availability"]
                for row in transition["capabilities"].values()
            },
            {"unavailable"},
        )
        self.assertFalse((CALENDARS / transition["id"]).exists())

    def problems_after(self, change) -> list[str]:
        document = copy.deepcopy(self.catalog)
        change(document)
        with mock.patch.object(_recensions, "load_catalog", return_value=document):
            return _recensions.catalog_problems(
                CALENDARS, repository=ROOT, required=True
            )

    def test_interval_gap_cannot_name_even_a_real_calendar(self) -> None:
        def change(document: dict) -> None:
            document["recensions"][1]["calendar"] = "roman-1962"

        problems = self.problems_after(change)
        self.assertTrue(any("interval-gap must not name a calendar" in row for row in problems))

    def test_as_of_must_be_a_real_calendar_date(self) -> None:
        problems = self.problems_after(
            lambda document: document.__setitem__("as_of", "2026-99-99")
        )
        self.assertTrue(any("as_of must be a quoted ISO date" in row for row in problems))

    def test_deleting_a_supported_calendar_record_is_detected(self) -> None:
        def change(document: dict) -> None:
            document["recensions"] = [
                row for row in document["recensions"] if row["id"] != "roman-1962"
            ]

        problems = self.problems_after(change)
        self.assertTrue(any("unregistered calendar indexes: roman-1962" in row for row in problems))

    def test_unavailable_capability_cannot_claim_a_collation(self) -> None:
        def change(document: dict) -> None:
            document["recensions"][1]["capabilities"]["propers"]["collation"] = "mixed"

        problems = self.problems_after(change)
        self.assertTrue(any("is unavailable but collation is 'mixed'" in row for row in problems))

    def test_unavailable_capability_needs_an_activation_requirement(self) -> None:
        def change(document: dict) -> None:
            row = document["recensions"][3]
            row["activation_requirements"] = [
                requirement
                for requirement in row["activation_requirements"]
                if "calendar" not in requirement["capabilities"]
            ]

        problems = self.problems_after(change)
        self.assertTrue(
            any("does not account for unavailable capabilities: calendar" in row for row in problems)
        )

    def test_evidence_record_id_must_exist_in_its_source(self) -> None:
        def change(document: dict) -> None:
            document["recensions"][1]["evidence_refs"][0] = (
                "src/sources/inventories/missal-acquisition-audit-v1.toml"
                "#id=no-such-book"
            )

        problems = self.problems_after(change)
        self.assertTrue(any("absent record id 'no-such-book'" in row for row in problems))

    def test_dated_rows_must_be_chronological_and_may_not_overlap(self) -> None:
        reversed_problems = self.problems_after(
            lambda document: document["recensions"].reverse()
        )
        self.assertTrue(any("recensions are not chronological" in row for row in reversed_problems))

        def overlap(document: dict) -> None:
            document["recensions"][1]["period"] = {"from": 1919, "through": 1963}

        overlap_problems = self.problems_after(overlap)
        self.assertTrue(any("dated recension rows overlap" in row for row in overlap_problems))

    def test_supported_data_requires_a_typed_coverage_reference(self) -> None:
        def change(document: dict) -> None:
            del document["recensions"][2]["coverage_ref"]

        problems = self.problems_after(change)
        self.assertTrue(
            any("coverage_ref is required when target data is available or partial" in row for row in problems)
        )

    def test_coverage_reference_must_identify_its_calendar_and_recension(self) -> None:
        def change(document: dict) -> None:
            document["recensions"][2]["coverage_ref"] = (
                "src/sources/inventories/postconciliar-english-2011-recension-coverage-v1.toml"
            )

        problems = self.problems_after(change)
        self.assertTrue(
            any("names recension 'roman-missal-en-us-2011', expected 'roman-1962'" in row for row in problems)
        )
        self.assertTrue(
            any("names calendar 'postconciliar', expected 'roman-1962'" in row for row in problems)
        )

    def test_coverage_reference_must_resolve_to_a_supported_schema(self) -> None:
        def change(document: dict) -> None:
            document["recensions"][2]["coverage_ref"] = "tmt.json"

        problems = self.problems_after(change)
        self.assertTrue(any("unsupported coverage schema" in row for row in problems))

    def test_language_coverage_reference_must_identify_the_language(self) -> None:
        def change(document: dict) -> None:
            document["recensions"][2]["language_capabilities"][0][
                "coverage_ref"
            ] = "src/sources/inventories/roman-1962-finding-aid-coverage-v1.toml"

        problems = self.problems_after(change)
        self.assertTrue(
            any("does not identify language 'la'" in row for row in problems)
        )

    def test_expression_parent_must_be_an_identified_book_state_and_precede_it(self) -> None:
        def unresolved_parent(document: dict) -> None:
            document["expressions"][0]["parent"] = "roman-transition-1956-1960"

        problems = self.problems_after(unresolved_parent)
        self.assertTrue(any("parent must name an identified book-state" in row for row in problems))

        def predates_parent(document: dict) -> None:
            document["expressions"][0]["year"] = 2007

        problems = self.problems_after(predates_parent)
        self.assertTrue(any("predates parent" in row for row in problems))

    def test_calendar_text_from_must_name_a_catalogued_calendar(self) -> None:
        source = CALENDARS / "roman-pre-1955" / "propers.yaml"
        original = _recensions._document

        def changed(path: Path):
            document = original(path)
            if path == source:
                document = copy.deepcopy(document)
                document["text_from"] = "uncatalogued"
            return document

        with mock.patch.object(_recensions, "_document", side_effect=changed):
            problems = _recensions.catalog_problems(
                CALENDARS, repository=ROOT, required=True
            )
        self.assertTrue(any("text_from names uncatalogued calendar 'uncatalogued'" in row for row in problems))

    def test_catalogued_calendar_text_from_cycle_is_refused(self) -> None:
        source = CALENDARS / "roman-1962" / "propers.yaml"
        original = _recensions._document

        def changed(path: Path):
            document = original(path)
            if path == source:
                document = copy.deepcopy(document)
                document["text_from"] = "roman-pre-1955"
            return document

        with mock.patch.object(_recensions, "_document", side_effect=changed):
            problems = _recensions.catalog_problems(
                CALENDARS, repository=ROOT, required=True
            )
        self.assertTrue(any("catalogued calendar text_from cycle" in row for row in problems))


class CheckerIntegrationTests(unittest.TestCase):
    def test_checker_calls_the_catalog_validator_before_rejecting_an_empty_fixture(self) -> None:
        with TemporaryDirectory() as held:
            root = Path(held)
            with mock.patch.object(checker, "catalog_problems", return_value=[]) as called:
                with self.assertRaisesRegex(ValueError, "no calendar index"):
                    checker.run(root, None)
            called.assert_called_once()


if __name__ == "__main__":
    unittest.main()
