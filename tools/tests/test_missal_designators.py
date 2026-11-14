"""Every coherent missal has one affirmative designator, read from one registry."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src" / "sources" / "calendars"
sys.path.insert(0, str(ROOT / "scripts"))

import _calendars  # noqa: E402
import _missal_designators  # noqa: E402


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = SourceFileLoader(f"_{name.replace('-', '_')}_designators", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


READER = {
    "roman-pre-1955": ("Roman Missal, 1920 typical edition", "1920 typical edition"),
    "roman-1962": ("Roman Missal, 1962 typical edition", "1962 typical edition"),
    "postconciliar": (
        "Roman Missal, 2002 third typical edition, 2008 emended reprint",
        "2008 emended reprint",
    ),
}


class RegistryTests(unittest.TestCase):
    def test_the_registry_validates_against_its_records(self) -> None:
        self.assertEqual(_missal_designators.problems(ROOT, required=True), [])

    def test_each_reader_calendar_is_named_by_the_registry(self) -> None:
        for calendar, (designator, short) in READER.items():
            with self.subTest(calendar=calendar):
                self.assertEqual(_calendars.index_header(CALENDARS, calendar, "edition"), designator)
                self.assertEqual(_calendars.index_header(CALENDARS, calendar, "edition_short"), short)
                document = _calendars.load_document(CALENDARS, calendar)
                self.assertEqual((document["edition"], document["edition_short"]), (designator, short))
                qualification = _missal_designators.calendar_identity(ROOT, calendar)["edition_qualification"]
                self.assertTrue(qualification.strip())

    def test_no_calendar_index_restates_the_name(self) -> None:
        self.assertEqual(_calendars.restated_identity(CALENDARS), [])
        for calendar in READER:
            source = (CALENDARS / calendar / "propers.yaml").read_text(encoding="utf-8")
            self.assertNotRegex(source, r"(?m)^edition(_short)?:")

    def test_the_short_form_is_the_final_segment(self) -> None:
        self.assertEqual(_missal_designators.short_form("Roman Missal, 1962 typical edition"),
                         "1962 typical edition")
        self.assertEqual(_missal_designators.short_form(
            "Roman Missal, 1970 typical edition, 1971 emended reprint"), "1971 emended reprint")

    def test_relative_and_hedged_names_are_refused(self) -> None:
        for name in (
            "Pre-1955 Missal",
            "Postconciliar Missal",
            "Roman Missal — Bonn 2004 witness study",
            "Roman Missal — 2008 base with recorded additions",
            "Roman Missal, transitional state 1956-1960",
            "Roman Missal, c. 1954 state",
        ):
            with self.subTest(name=name):
                self.assertIsNotNone(_missal_designators.RELATIVE.search(name))
        for row in _missal_designators.rows(ROOT):
            with self.subTest(key=row["key"]):
                self.assertIsNone(_missal_designators.RELATIVE.search(row["designator"]))

    def test_unestablished_editions_are_leads_and_never_designated(self) -> None:
        document = _missal_designators.load(ROOT)
        leads = {row["key"]: row for row in document["leads"]}
        keys = {row["key"] for row in document["missals"]}
        self.assertFalse(set(leads) & keys)
        for key in ("roman-1884", "praedicatorum-1933-1939-1965", "ambrosianum-1609", "bracarense-1538"):
            self.assertIn(key, leads)
        for key in ("praedicatorum-1553", "cisterciense-1657", "bellovacense-1756", "ambrosianum-1712"):
            self.assertIn(key, keys)

    def test_witnesses_never_receive_a_designator(self) -> None:
        witnesses = {
            witness for row in _missal_designators.rows(ROOT) for witness in row.get("witnesses", [])
        }
        keys = {row["key"] for row in _missal_designators.rows(ROOT)}
        # The Bonn reprint, the Mame and Benziger printings are witnesses of the
        # 1920 typical edition, never missals of their own.
        self.assertIn(
            "edition.catholic-church.missale-romanum.2004-bonn-palmarum-reimpressio-editio-28-iuxta-typicam-1920",
            witnesses,
        )
        self.assertFalse(any("bonn" in key or "benziger" in key or "mame" in key for key in keys))


class SyntheticRegistryTests(unittest.TestCase):
    """The checks fire on a registry that fails them."""

    def repository(self, rows: str, *, header: str = "") -> Path:
        held = Path(self.enterContext(tempfile.TemporaryDirectory()))
        calendars = held / "src/sources/calendars/demo"
        calendars.mkdir(parents=True)
        (calendars / "propers.yaml").write_text(
            f"schema: {_calendars.MASS_INDEX_SCHEMA}\n{header}calendar: demo\n", encoding="utf-8"
        )
        inventories = held / "src/sources/inventories"
        inventories.mkdir(parents=True)
        (inventories / "evidence.toml").write_text('[[books]]\nid = "demo-book"\n', encoding="utf-8")
        (inventories / "missal-designators-v1.toml").write_text(
            'schema = "triptych-missal-designators/v1"\nas_of = "2026-11-14"\n' + rows,
            encoding="utf-8",
        )
        return held

    ROW = '''
[[missals]]
key = "demo"
designator = "{designator}"
kind = "typical-edition"
rite = "roman"
language = "la"
year = 1920
calendar = "demo"
qualification = "A stated limit. No separate act row is recorded."
sources = ["src/sources/inventories/evidence.toml#id=demo-book"]
'''

    def test_a_valid_synthetic_registry_passes_and_names_the_calendar(self) -> None:
        held = self.repository(self.ROW.format(designator="Roman Missal, 1920 typical edition"))
        self.assertEqual(_missal_designators.problems(held, required=True), [])
        root = held / "src/sources/calendars"
        self.assertEqual(_calendars.index_header(root, "demo", "edition_short"), "1920 typical edition")

    def test_a_missal_without_an_act_row_must_say_so(self) -> None:
        held = self.repository(
            self.ROW.format(designator="Roman Missal, 1920 typical edition").replace(
                " No separate act row is recorded.", ""
            )
        )
        problems = _missal_designators.problems(held, required=True)
        self.assertTrue(any("no act row must say" in row for row in problems), problems)

    def test_a_lead_needs_a_known_status_and_resolving_sources(self) -> None:
        held = self.repository(
            self.ROW.format(designator="Roman Missal, 1920 typical edition")
            + '\n[[leads]]\nkey = "demo-lead"\nsubject = "A named edition"\nstatus = "probable"\n'
            'reason = "Reported only."\nsources = ["src/sources/inventories/evidence.toml#id=absent"]\n'
        )
        problems = _missal_designators.problems(held, required=True)
        self.assertTrue(any("status has unknown value 'probable'" in row for row in problems), problems)
        self.assertTrue(any("absent record id 'absent'" in row for row in problems), problems)

    def test_a_relative_designator_is_refused(self) -> None:
        held = self.repository(self.ROW.format(designator="Roman Missal, pre-1955 1920 edition"))
        problems = _missal_designators.problems(held, required=True)
        self.assertTrue(any("rather than naming it" in row for row in problems), problems)

    def test_the_final_segment_must_carry_the_year(self) -> None:
        held = self.repository(self.ROW.format(designator="Roman Missal, typical edition of 1920"))
        problems = _missal_designators.problems(held, required=True)
        self.assertTrue(any("segment for its own year 1920" in row for row in problems), problems)

    def test_a_calendar_index_restating_the_name_is_refused(self) -> None:
        held = self.repository(
            self.ROW.format(designator="Roman Missal, 1920 typical edition"),
            header="edition: Missale Romanum, editio typica Vaticana 1920\n",
        )
        problems = _calendars.restated_identity(held / "src/sources/calendars")
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("restates edition", problems[0])

    def test_an_undesignated_calendar_is_reported(self) -> None:
        held = self.repository(
            self.ROW.format(designator="Roman Missal, 1920 typical edition").replace(
                'calendar = "demo"\n', ""
            )
        )
        problems = _missal_designators.problems(held, required=True)
        self.assertTrue(any("reader calendar 'demo' has no designator" in row for row in problems), problems)

    def test_a_fixture_without_a_registry_keeps_its_own_header(self) -> None:
        held = Path(self.enterContext(tempfile.TemporaryDirectory()))
        room = held / "demo"
        room.mkdir()
        (room / "propers.yaml").write_text(
            f"schema: {_calendars.MASS_INDEX_SCHEMA}\nedition: Fixture Missal\n", encoding="utf-8"
        )
        self.assertEqual(_calendars.index_header(held, "demo", "edition"), "Fixture Missal")
        self.assertEqual(_calendars.restated_identity(held), [])


class ContributionFilterTests(unittest.TestCase):
    """A missal is offered only where it contributes actual text of its own."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.propers = load_tool("mass-propers")

    @staticmethod
    def mass(*, stated: bool | None, la: tuple[int, int] = (0, 0), en: tuple[int, int] = (0, 0)) -> dict:
        row = {"coverage": {"languages": [
            {"lang": "la", "available": la[0], "collations": {"collated": la[1]}},
            {"lang": "en", "available": en[0], "collations": {"collated": en[1]}},
        ]}}
        if stated is not None:
            row["recension"] = {"stated": stated, "text_from": "" if stated else "base"}
        return row

    def test_placeholders_and_empty_records_contribute_nothing(self) -> None:
        self.assertEqual(self.propers.contributed_bodies({"masses": [self.mass(stated=None)]}), 0)
        self.assertEqual(self.propers.contributed_bodies({"masses": []}), 0)

    def test_an_ordinary_calendar_counts_any_published_body(self) -> None:
        self.assertEqual(self.propers.contributed_bodies(
            {"masses": [self.mass(stated=None, en=(2, 0))]}), 2)

    def test_a_recension_does_not_borrow_its_base_contribution(self) -> None:
        inherited = self.mass(stated=False, la=(0, 0), en=(5, 0))
        self.assertEqual(self.propers.contributed_bodies({"masses": [inherited]}), 0)
        attested = self.mass(stated=False, la=(3, 3), en=(5, 0))
        self.assertEqual(self.propers.contributed_bodies({"masses": [attested]}), 3)
        stated = self.mass(stated=True, en=(1, 0))
        self.assertEqual(self.propers.contributed_bodies({"masses": [stated]}), 1)

    def test_the_tracked_reader_discovery_offers_only_contributing_missals(self) -> None:
        for calendar in READER:
            with self.subTest(calendar=calendar):
                structure = json.loads((ROOT / "src/index/propers" / f"{calendar}.json").read_text(encoding="utf-8"))
                self.assertGreater(self.propers.contributed_bodies(structure), 0)


if __name__ == "__main__":
    unittest.main()
