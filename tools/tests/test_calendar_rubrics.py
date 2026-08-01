#!/usr/bin/env python3
"""Regression checks for the rubrical precedence layer and its discovery.

The discovery tests are the important ones. `src/sources/calendars` held exactly
one kind of file for as long as there was only one kind, and the tools that read
it globbed by extension; the first companion source to land there was read as a
mass index and turned `make check` red. The fix must keep two properties at
once: a companion file is skipped and named, and a file nobody claims still
fails loudly.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from _calendars import (  # noqa: E402
    COMPANION_SCHEMAS,
    INDEX_OWNED,
    MASS_INDEX_SCHEMA,
    index_header,
    partition,
    restated_identity,
)

CALENDARS = ROOT / "src" / "sources" / "calendars"
TOOL = ROOT / "tools" / "calendar-rubrics"
DATA = ROOT / "src" / "web" / "data" / "structure" / "rubrics"


class DiscoveryTests(unittest.TestCase):
    def test_the_real_tree_splits_into_indexes_and_companions(self) -> None:
        indexes, companions, problems = partition(CALENDARS)
        self.assertEqual(problems, [])
        self.assertTrue(indexes, "no mass index was found")
        self.assertTrue(all(path.name == "propers.yaml" for path in indexes))
        self.assertEqual(
            sorted(row["path"].rsplit("/", 2)[-2] for row in companions),
            ["postconciliar", "roman-1962"],
        )
        self.assertTrue(all(row["owner"] == "calendar-rubrics" for row in companions))

    def test_an_unclaimed_schema_is_a_hard_problem(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as held:
            room = Path(held) / "roman-1962"
            room.mkdir()
            (room / "propers.yaml").write_text(f"schema: {MASS_INDEX_SCHEMA}\n", encoding="utf-8")
            (room / "stray.yaml").write_text("schema: something/v1\n", encoding="utf-8")
            indexes, companions, problems = partition(Path(held))
            self.assertEqual([path.name for path in indexes], ["propers.yaml"])
            self.assertEqual(companions, [])
            self.assertEqual(len(problems), 1)
            self.assertIn("stray.yaml", problems[0])
            self.assertIn("something/v1", problems[0])

    def test_a_file_declaring_no_schema_is_not_silently_skipped(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as held:
            room = Path(held) / "roman-1962"
            room.mkdir()
            (room / "propers.yaml").write_text(f"schema: {MASS_INDEX_SCHEMA}\n", encoding="utf-8")
            (room / "notes.yaml").write_text("calendar: roman-1962\n", encoding="utf-8")
            _, _, problems = partition(Path(held))
            self.assertEqual(len(problems), 1)
            self.assertIn("notes.yaml", problems[0])

    def test_the_companion_registry_names_the_rubrics_layer(self) -> None:
        self.assertIn("triptych-calendar-rubrics/v1", COMPANION_SCHEMAS)


class IdentityTests(unittest.TestCase):
    """One book per calendar directory, named in one file.

    `edition` was hand-typed in `propers.yaml` and again in `rubrics.yaml`, in
    both calendars: four copies of two strings that nothing compared. They
    agreed when they were finally read, which is the whole difficulty — a census
    kept the same way in this repository was found in three copies that all
    disagreed, and by then the wrong number had been served for months.
    """

    def restatement(self, held: str, line: str) -> list[str]:
        room = Path(held) / "roman-1962"
        room.mkdir()
        (room / "propers.yaml").write_text(
            f"schema: {MASS_INDEX_SCHEMA}\n"
            "edition: Missale Romanum, editio typica 1962\n"
            "edition_short: 1962 Missal\n",
            encoding="utf-8",
        )
        (room / "rubrics.yaml").write_text(
            "schema: triptych-calendar-rubrics/v1\ncalendar: roman-1962\n" + line,
            encoding="utf-8",
        )
        return restated_identity(Path(held))

    def test_the_real_tree_names_each_book_once(self) -> None:
        self.assertEqual(restated_identity(CALENDARS), [])

    def test_the_index_still_carries_both_names(self) -> None:
        for name in ("roman-1962", "postconciliar"):
            for field in INDEX_OWNED:
                self.assertTrue(
                    index_header(CALENDARS, name, field),
                    f"{name}: the mass index declares no {field}, and nothing else may",
                )

    def test_a_restatement_that_agrees_is_still_refused(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as held:
            problems = self.restatement(held, "edition: Missale Romanum, editio typica 1962\n")
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("rubrics.yaml", problems[0])
        self.assertIn("restates edition", problems[0])

    def test_two_files_claiming_different_editions_fail_and_name_both(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as held:
            problems = self.restatement(held, "edition: Missale Romanum, editio typica 1961\n")
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("editio typica 1961", problems[0])
        self.assertIn("editio typica 1962", problems[0])

    def test_the_short_name_has_one_home_too(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as held:
            problems = self.restatement(held, "edition_short: 1962 Missal\n")
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("restates edition_short", problems[0])


class LayerTests(unittest.TestCase):
    """The emitted layer, and the storage claim the design rests on."""

    def setUp(self) -> None:
        if not DATA.is_dir():
            self.skipTest("the rubrics layer has not been generated")

    def test_the_layer_is_one_file_per_calendar_plus_an_index(self) -> None:
        written = sorted(path.name for path in DATA.glob("*.json"))
        self.assertEqual(written, ["index.json", "postconciliar.json", "roman-1962.json"])

    def test_every_mass_in_each_calendar_is_classified(self) -> None:
        import yaml

        for name in ("roman-1962", "postconciliar"):
            source = yaml.safe_load((CALENDARS / name / "propers.yaml").read_text(encoding="utf-8"))
            keys = {
                mass["key"]
                for body in (source.get("sections") or {}).values()
                for mass in (body or {}).get("masses") or []
                if isinstance(mass, dict) and mass.get("key")
            }
            emitted = json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))
            self.assertEqual(keys - set(emitted["keys"]), set(), f"{name}: unclassified masses")

    def test_every_basis_names_a_row_the_table_carries_or_declines_to_compete(self) -> None:
        for name in ("roman-1962", "postconciliar"):
            emitted = json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))
            rows = {row["row"] for row in emitted["precedence"]["rows"]}
            for basis in emitted["bases"]:
                if basis.get("row") is None:
                    continue
                self.assertIn(basis["row"], rows, f"{name}: {basis['id']} names a row that is not in the table")

    def test_the_emitted_layer_carries_the_book_the_index_names(self) -> None:
        index = json.loads((DATA / "index.json").read_text(encoding="utf-8"))
        for row in index["calendars"]:
            for field in INDEX_OWNED:
                self.assertEqual(row[field], index_header(CALENDARS, row["calendar"], field))

    def test_the_layer_states_precedence_where_the_day_files_refuse_to(self) -> None:
        index = json.loads((DATA / "index.json").read_text(encoding="utf-8"))
        self.assertTrue(all(row["precedence_stated"] for row in index["calendars"]))
        days = ROOT / "src" / "web" / "data" / "structure" / "calendar" / "index.json"
        if days.is_file():
            self.assertFalse(json.loads(days.read_text(encoding="utf-8"))["precedence"]["stated"])


class SolvedCaseTests(unittest.TestCase):
    def test_the_tool_verifies_its_solved_cases(self) -> None:
        finished = subprocess.run(
            [sys.executable, str(TOOL), "check", "--json"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        if finished.returncode == 69:
            self.skipTest("PyYAML is not installed")
        self.assertEqual(finished.returncode, 0, finished.stderr or finished.stdout)
        payload = json.loads(finished.stdout)
        solved = payload["solved_cases"]
        if solved["skipped"]:
            self.skipTest(f"solved cases were not run: {solved['skipped']}")
        self.assertGreater(solved["declared"], 0)
        self.assertEqual(solved["verified"], solved["declared"])


if __name__ == "__main__":
    unittest.main()
