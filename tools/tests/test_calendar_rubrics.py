#!/usr/bin/env python3
"""Regression checks for the rubrical precedence layer and its discovery.

The discovery tests are the important ones. `src/sources/calendars` held exactly
one kind of file for as long as there was only one kind, and the tools that read
it globbed by extension; the first companion source to land there was read as a
mass index and turned `make check` red. The fix must keep two properties at
once: a companion file is skipped and named, and a file nobody claims still
fails loudly.
"""

import argparse
import inspect
import json
import subprocess
import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from unittest import mock

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


def load_tool(name: str):
    loader = SourceFileLoader(f"_{name.replace('-', '_')}", str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


rubrics = load_tool("calendar-rubrics")


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
        # There is no `skipped` to consult any more, and this test no longer
        # excuses itself on one. Every reason the cases could not run is a
        # failure inside the tool, so reaching here at all means they ran.
        self.assertNotIn("skipped", solved)
        self.assertGreater(solved["declared"], 0)
        self.assertEqual(solved["verified"], solved["declared"])
        self.assertTrue(solved["asserted"], "the cases assert no part of the model's result")


class UnrunIsNotPassedTests(unittest.TestCase):
    """A gate that could not run must not report that it passed.

    Both were skips returning `status: ok`: deleting `assembly-model.js`, or
    running where `node` is absent, printed a green line over a derivation
    nobody had exercised. That is the TASK-110 failure — "0 stale bindings"
    printed over twenty-one real ones — and a green line asserts that something
    was confirmed.
    """

    def arguments(self) -> argparse.Namespace:
        return argparse.Namespace(
            root=str(CALENDARS), out=str(ROOT / "src" / "web" / "data"),
            calendar=None, verbose=False, json=False, format="text",
        )

    def setUp(self) -> None:
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("PyYAML is not installed")

    def test_an_absent_model_is_a_failure(self) -> None:
        with mock.patch.object(rubrics, "MODEL", ROOT / "src/web/browser/liturgy/nothing-here.js"):
            with self.assertRaises(rubrics.SourceError) as raised:
                rubrics.run_check(self.arguments())
        self.assertIn("absent", str(raised.exception))

    def test_an_absent_interpreter_is_a_failure(self) -> None:
        with mock.patch.object(rubrics.shutil, "which", return_value=None):
            with self.assertRaises(rubrics.SourceError) as raised:
                rubrics.run_check(self.arguments())
        self.assertIn("node is not installed", str(raised.exception))


class ExpectedFieldTests(unittest.TestCase):
    """A field nobody asserted must not read like a field that passed.

    `compare_one` asked `if "<field>" in expect` against no list at all, so a
    solved case with every one of its field names misspelled compared nothing
    and still counted towards "15 of 15 verified". The tool already knew the
    stricter idiom one screen above: `REQUIRED_TOP` lists the fields a source
    must carry rather than inferring them.
    """

    BRANCH = {
        "option": None,
        "winner": {"id": "passion-wednesday", "row": 22, "source": "index"},
        "settled": True,
        "losers": [{"id": "s-patricii-episcopi-confessoris", "disposition": "commemorated"}],
        "orations": {"low_mass": [{}, {}], "sung_non_conventual": [{}]},
        "conditions": [],
    }

    def result(self) -> dict:
        return {"options": [json.loads(json.dumps(self.BRANCH))]}

    def case(self, **fields) -> dict:
        return {"id": "case-1a", "source": "worked-cases.md", "date": "2027-03-17",
                "why": "a worked ruling", **fields}

    def test_a_case_whose_fields_agree_reports_nothing(self) -> None:
        found = rubrics.compare(
            self.case(expect={"winner": "passion-wednesday", "winner_row": 22, "settled": True,
                              "commemorated": ["s-patricii-episcopi-confessoris"],
                              "orations_low_mass": 2, "orations_sung_non_conventual": 1}),
            self.result(), "roman-1962",
        )
        self.assertEqual(found, [])

    def test_a_misspelled_field_is_an_error_and_not_silence(self) -> None:
        found = rubrics.compare(
            self.case(expect={"winnner": "passion-wednesday"}), self.result(), "roman-1962")
        self.assertEqual(len(found), 1, found)
        self.assertIn("winnner", found[0])

    def test_one_misspelling_beside_correct_fields_is_still_caught(self) -> None:
        found = rubrics.compare(
            self.case(expect={"winner": "passion-wednesday", "winner_rows": 22}),
            self.result(), "roman-1962",
        )
        self.assertEqual(len(found), 1, found)
        self.assertIn("winner_rows", found[0])

    def test_a_case_that_expects_nothing_is_refused(self) -> None:
        found = rubrics.compare(self.case(expect={}), self.result(), "roman-1962")
        self.assertEqual(len(found), 1, found)
        self.assertIn("asserts nothing", found[0])

    def test_a_case_carrying_no_expectation_block_is_refused(self) -> None:
        found = rubrics.compare(self.case(), self.result(), "roman-1962")
        self.assertEqual(len(found), 1, found)
        self.assertIn("exactly one", found[0])

    def test_a_case_carrying_both_blocks_is_refused(self) -> None:
        found = rubrics.compare(
            self.case(expect={"winner": "passion-wednesday"}, expect_by_option={}),
            self.result(), "roman-1962",
        )
        self.assertEqual(len(found), 1, found)
        self.assertIn("exactly one", found[0])

    def test_an_unknown_field_on_the_case_itself_is_refused(self) -> None:
        found = rubrics.compare(
            self.case(note="a stray field", expect={"winner": "passion-wednesday"}),
            self.result(), "roman-1962",
        )
        self.assertEqual(len(found), 1, found)
        self.assertIn("note", found[0])

    def test_an_empty_branch_table_asserts_nothing_and_is_refused(self) -> None:
        found = rubrics.compare(self.case(expect_by_option={}), self.result(), "roman-1962")
        self.assertEqual(len(found), 1, found)
        self.assertIn("asserts nothing", found[0])

    def test_every_declared_field_is_one_compare_one_actually_compares(self) -> None:
        """The list and the comparison must not drift apart.

        A careful enumeration and a careless comparison sitting in one file with
        nothing between them is how this defect arose in the first place.
        """
        source = inspect.getsource(rubrics.compare_one)
        for field in rubrics.EXPECTATIONS:
            with self.subTest(field=field):
                self.assertIn(f'"{field}"', source, f"{field} is declared and never compared")

    def test_every_declared_field_names_a_part_of_the_model_result(self) -> None:
        self.assertLessEqual(set(rubrics.EXPECTATIONS.values()), set(self.BRANCH))


if __name__ == "__main__":
    unittest.main()
