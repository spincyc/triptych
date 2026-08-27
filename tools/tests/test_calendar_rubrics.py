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
    load_document,
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
calendar_days = load_tool("calendar-days")


class DiscoveryTests(unittest.TestCase):
    def test_the_real_tree_splits_into_indexes_and_companions(self) -> None:
        indexes, companions, problems = partition(CALENDARS)
        self.assertEqual(problems, [])
        self.assertTrue(indexes, "no mass index was found")
        self.assertTrue(all(path.name == "propers.yaml" for path in indexes))
        self.assertEqual(
            sorted(row["path"].rsplit("/", 2)[-2] for row in companions),
            ["postconciliar", "roman-1962", "roman-pre-1955"],
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


class LatinTextRightsTests(unittest.TestCase):
    """Withheld rubric wording stays out while its structural rules remain."""

    STATUS = {
        "state": "unavailable",
        "scope": "rubric-wording",
        "kind": "rights-withheld",
    }
    ROMAN_PATHS = (
        ("precedence", "latin"),
        ("precedence", "occurrence", "latin"),
        ("precedence", "effect", "latin"),
        ("saturday_office", "latin"),
        ("saturday_office", "mass", "latin"),
        ("mass_choices", 0, "latin"),
        ("mass_choices", 1, "latin"),
        ("impediment", "transfer", "latin"),
        ("impediment", "transfer", "proper_seats", 0, "latin"),
        ("impediment", "transfer", "proper_seats", 1, "latin"),
        ("impediment", "transfer", "keeps_its_class", "latin"),
        ("impediment", "fixed_commemoration", "latin"),
        ("impediment", "sunday_not_resumed", "latin"),
        ("commemoration", "kinds", "latin"),
        ("commemoration", "ceilings", "latin"),
        ("commemoration", "order", "latin"),
        ("commemoration", "surplus", "latin"),
        ("orations", "absolute_cap", "latin"),
        ("appointed_across", 0, "latin"),
        ("appointed_across", 1, "latin"),
        ("mass_category", "latin"),
    )
    PROTECTED_WITNESS = (
        "artifact.catholic-church.missale-romanum."
        "vatican-typica-1962.cmaa-facsimile-pdf"
    )

    @staticmethod
    def roman_source() -> dict:
        import yaml

        return yaml.safe_load(
            (CALENDARS / "roman-1962" / "rubrics.yaml").read_text(encoding="utf-8")
        )

    @staticmethod
    def parent_at(document: object, path: tuple[object, ...]) -> dict:
        value = document
        for part in path[:-1]:
            value = value[part]
        return value

    def test_the_exact_twenty_one_roman_bodies_are_absent(self) -> None:
        source = self.roman_source()
        self.assertEqual(source["latin_text_status"], self.STATUS)
        self.assertEqual(rubrics.latin_body_paths(source), [])
        self.assertEqual(len(self.ROMAN_PATHS), 21)
        for path in self.ROMAN_PATHS:
            with self.subTest(path=path):
                self.assertNotIn("latin", self.parent_at(source, path))

    def test_reintroducing_whole_scope_wording_is_a_source_problem(self) -> None:
        source = self.roman_source()
        source["precedence"]["latin"] = "protected wording"
        found = rubrics.check_latin_text_status(source, "roman-1962/rubrics.yaml")
        self.assertEqual(len(found), 1, found)
        self.assertIn("precedence.latin", found[0])

    def test_the_public_status_has_no_audit_or_authority_extension(self) -> None:
        source = self.roman_source()
        source["latin_text_status"]["authority"] = self.PROTECTED_WITNESS
        found = rubrics.check_latin_text_status(source, "roman-1962/rubrics.yaml")
        self.assertEqual(len(found), 1, found)
        self.assertIn("unknown fields ['authority']", found[0])

    def test_path_scoped_status_allows_only_unlisted_latin(self) -> None:
        source = {
            "latin_text_status": {**self.STATUS, "paths": ["impediment.transfer.latin"]},
            "precedence": {"latin": "public-domain wording"},
            "impediment": {"transfer": {}},
        }
        self.assertEqual(rubrics.check_latin_text_status(source, "rubrics.yaml"), [])
        source["impediment"]["transfer"]["latin"] = "protected wording"
        found = rubrics.check_latin_text_status(source, "rubrics.yaml")
        self.assertEqual(len(found), 1, found)
        self.assertIn("impediment.transfer.latin", found[0])

    def test_fresh_projection_excludes_bodies_and_audit_graph(self) -> None:
        built, problems, _ = rubrics.build(CALENDARS, "roman-1962")
        self.assertEqual(problems, [])
        emitted = built[0]
        self.assertEqual(emitted["latin_text_status"], {"kind": "rights-withheld"})
        self.assertEqual(rubrics.latin_body_paths(emitted), [])
        self.assertNotIn("derived_from", emitted)
        self.assertNotIn(self.PROTECTED_WITNESS, json.dumps(emitted, sort_keys=True))

        self.assertEqual(emitted["precedence"]["locus"], "RG 91")
        self.assertEqual(len(emitted["precedence"]["rows"]), 28)
        self.assertEqual(emitted["orations"]["absolute_cap"]["value"], 3)
        transfer = emitted["impediment"]["transfer"]
        self.assertEqual(transfer["applies_to"], "first-class feasts only")
        self.assertEqual(
            [seat["locus"] for seat in transfer["proper_seats"]],
            ["RG 96 a", "RG 96 b"],
        )


class LayerTests(unittest.TestCase):
    """The emitted layer, and the storage claim the design rests on."""

    def setUp(self) -> None:
        if not DATA.is_dir():
            self.skipTest("the rubrics layer has not been generated")

    def test_the_layer_is_one_file_per_calendar_plus_an_index(self) -> None:
        written = sorted(path.name for path in DATA.glob("*.json"))
        self.assertEqual(
            written,
            ["index.json", "postconciliar.json", "roman-1962.json", "roman-pre-1955.json"],
        )

    def test_every_celebration_in_each_calendar_is_classified(self) -> None:
        """Every mass a calendar can keep, which is every mass but the Commons.

        The Commune Sanctorum is formularies, not days. A Common has no date, no
        season and no rank; it never occurs, never competes, and takes the rank
        and the rubrics of whatever day takes it. Requiring an assignment basis
        for one would put a celebration in the precedence table that the
        calendar never keeps, so the section is excluded here and in
        `calendar-rubrics.load_masses`, which is the only other place that
        knows.
        """
        import yaml

        for name in ("roman-1962", "postconciliar", "roman-pre-1955"):
            source = load_document(CALENDARS, name, effective=True)
            keys = {
                mass["key"]
                for section, body in (source.get("sections") or {}).items()
                if str((body or {}).get("kind") or section) != "common"
                for mass in (body or {}).get("masses") or []
                if isinstance(mass, dict) and mass.get("key")
            }
            emitted = json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))
            self.assertEqual(keys - set(emitted["keys"]), set(), f"{name}: unclassified masses")
            commons = {
                mass["key"]
                for section, body in (source.get("sections") or {}).items()
                if str((body or {}).get("kind") or section) == "common"
                for mass in (body or {}).get("masses") or []
                if isinstance(mass, dict) and mass.get("key")
            }
            self.assertEqual(
                commons & set(emitted["keys"]), set(), f"{name}: a Common was classified"
            )

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


class LiturgicalYearUnresolvedScopeTests(unittest.TestCase):
    """MassAssembly must not turn a date-scoped refusal into a year-wide one."""

    @classmethod
    def setUpClass(cls) -> None:
        if not rubrics.shutil.which("node"):
            raise unittest.SkipTest("node is not installed")
        year_path = DATA.parent / "calendar" / "postconciliar" / "2026.json"
        if not year_path.is_file():
            raise unittest.SkipTest(f"no calendar year file at {year_path}")
        year = json.loads(year_path.read_text(encoding="utf-8"))
        owner = next(
            row
            for row in year["liturgical_years"]
            if row["begins"] <= "2026-08-07" <= row["ends"]
        )
        owner["unresolved"] = [
            {"what": "legacy-year-wide", "why": "an unscoped refusal"},
            {
                "what": "scoped-window",
                "why": "a refusal for five dates only",
                "from": "2026-08-05",
                "to": "2026-08-09",
            },
        ]
        built, problems, _ = rubrics.build(CALENDARS, "postconciliar")
        if problems:
            raise AssertionError("; ".join(problems))
        answered = rubrics.run_model(
            {
                "cases": [
                    {"id": "inside", "date": "2026-08-07", "year": year, "rubrics": built[0]},
                    {"id": "outside", "date": "2026-08-11", "year": year, "rubrics": built[0]},
                ]
            }
        )
        cls.by_id = {row["id"]: row for row in answered["results"]}
        for row in cls.by_id.values():
            if not row.get("ok"):
                raise AssertionError(row.get("error"))

    def names_on(self, case: str) -> list[str]:
        return [
            row["what"]
            for row in self.by_id[case]["result"]["liturgicalYear"]["unresolved"]
        ]

    def test_a_scoped_refusal_is_present_inside_its_window(self) -> None:
        self.assertIn("scoped-window", self.names_on("inside"))

    def test_a_scoped_refusal_is_absent_outside_its_window(self) -> None:
        self.assertNotIn("scoped-window", self.names_on("outside"))

    def test_an_unscoped_refusal_retains_legacy_year_wide_behavior(self) -> None:
        self.assertIn("legacy-year-wide", self.names_on("inside"))
        self.assertIn("legacy-year-wide", self.names_on("outside"))

    def test_a_scoped_refusal_blocks_its_day(self) -> None:
        branch, = self.by_id["inside"]["result"]["options"]
        self.assertFalse(branch["settled"])
        self.assertIsNone(branch["winner"])
        self.assertEqual([row["what"] for row in branch["unsettled"]], ["scoped-window"])

    def test_a_legacy_year_notice_does_not_block_an_unrelated_day(self) -> None:
        branch, = self.by_id["outside"]["result"]["options"]
        self.assertTrue(branch["settled"])
        self.assertIsNotNone(branch["winner"])
        self.assertEqual(branch["unsettled"], [])


class ActiveCalendarRefusalTests(unittest.TestCase):
    """A live calendar refusal outranks every rubrical occurrence override."""

    CALENDARS = ("roman-1962", "roman-pre-1955")
    DATE = "2038-11-21"
    EXPECTED = [
        "last-sunday-after-pentecost",
        "pentecost-23",
        "praesentatione-beatae-mariae-virginis",
    ]

    @classmethod
    def setUpClass(cls) -> None:
        if not rubrics.shutil.which("node"):
            raise unittest.SkipTest("node is not installed")
        cases = []
        for calendar in cls.CALENDARS:
            built, problems, _ = rubrics.build(CALENDARS, calendar)
            if problems:
                raise AssertionError("; ".join(problems))
            built[0]["overrides"] = list(built[0].get("overrides") or []) + [
                {
                    "id": "fixture-last-sunday-would-win",
                    "key": "last-sunday-after-pentecost",
                    "over_key_matches": r"^pentecost-\d+$",
                    "when_same_row": True,
                    "locus": "adversarial regression fixture",
                    "why": "this would choose the last Sunday if the refusal did not stop ranking",
                }
            ]
            year_path = DATA.parent / "calendar" / calendar / "2038.json"
            if not year_path.is_file():
                raise unittest.SkipTest(f"no calendar year file at {year_path}")
            cases.append(
                {
                    "id": calendar,
                    "date": cls.DATE,
                    "year": json.loads(year_path.read_text(encoding="utf-8")),
                    "rubrics": built[0],
                }
            )
        answered = rubrics.run_model({"cases": cases})
        cls.results = {}
        for row in answered["results"]:
            if not row.get("ok"):
                raise AssertionError(row.get("error"))
            cls.results[row["id"]] = row["result"]

    def test_the_real_p23_refusal_is_scoped_to_its_date(self) -> None:
        for calendar, result in self.results.items():
            with self.subTest(calendar=calendar):
                refusal, = result["liturgicalYear"]["unresolved"]
                self.assertEqual(refusal["what"], "the last Sunday after Pentecost")
                self.assertEqual(refusal["from"], self.DATE)
                self.assertEqual(refusal["to"], self.DATE)
                self.assertIn("23 Sundays after Pentecost", refusal["why"])

    def test_the_active_refusal_cannot_become_a_settled_winner(self) -> None:
        for calendar, result in self.results.items():
            with self.subTest(calendar=calendar):
                branch, = result["options"]
                self.assertFalse(branch["settled"])
                self.assertIsNone(branch["winner"])
                self.assertFalse(branch["choiceRequired"])
                self.assertIsNone(branch["choice"])
                self.assertEqual(branch["unsettled"], result["liturgicalYear"]["unresolved"])
                self.assertEqual(branch["losers"], [])

    def test_every_real_candidate_remains_readable_only_as_unresolved(self) -> None:
        for calendar, result in self.results.items():
            with self.subTest(calendar=calendar):
                branch, = result["options"]
                self.assertEqual([row["id"] for row in branch["candidates"]], self.EXPECTED)
                self.assertEqual([row["key"] for row in branch["candidates"]], self.EXPECTED)
                self.assertEqual([row["id"] for row in branch["readable"]], self.EXPECTED)
                self.assertTrue(all(row["state"] == "unresolved" for row in branch["readable"]))


class SourceDrivenAssignmentTests(unittest.TestCase):
    """Distinct celebrations inherit precedence from their source attributes."""

    def test_august_seventh_optional_memorials_share_the_generic_rank_rule(self) -> None:
        source = rubrics.load_source(CALENDARS, "postconciliar")
        assigned, problems = rubrics.assign(
            source,
            rubrics.load_masses(CALENDARS, "postconciliar"),
            "postconciliar",
        )
        self.assertEqual(problems, [])

        expected_rule = {
            "basis": "place-12-optional-memorial",
            "dated": True,
            "rank": "Optional memorial",
        }
        for key in (
            "saints-sixtus-ii-pope-companions-martyrs",
            "saint-cajetan-priest",
        ):
            with self.subTest(key=key):
                row = assigned[key]
                self.assertEqual(row["basis"], "place-12-optional-memorial")
                self.assertEqual(source["assignment"][row["rule"]], expected_rule)


class OverrideValidationTests(unittest.TestCase):
    def test_every_override_row_must_be_a_mapping(self) -> None:
        found = rubrics.check_overrides(
            {"overrides": [None]}, {}, {}, "fixture/rubrics.yaml"
        )
        self.assertEqual(len(found), 1, found)
        self.assertIn("must be a mapping", found[0])

    def test_reduction_override_must_name_the_targets_assigned_basis(self) -> None:
        document = {
            "overrides": [
                {
                    "id": "joint-reduction",
                    "key": "memorial",
                    "when_with_basis": "place-10",
                    "reduce_with_to_basis": "place-12",
                    "locus": "fixture",
                    "why": "fixture",
                }
            ]
        }
        assigned = {"memorial": {"basis": "place-3"}}
        found = rubrics.check_overrides(
            document,
            assigned,
            {"place-3": 0, "place-10": 1, "place-12": 2},
            "fixture/rubrics.yaml",
        )
        self.assertEqual(len(found), 1, found)
        self.assertIn("expects 'memorial' to have basis 'place-10'", found[0])

    def test_override_patterns_are_validated_by_the_javascript_consumer(self) -> None:
        for pattern in ("(?#comment)a", "(?>a)", "a++"):
            with self.subTest(pattern=pattern):
                document = {
                    "overrides": [
                        {
                            "id": "consumer-regex",
                            "key": "target",
                            "over_key_matches": pattern,
                            "when_same_row": True,
                            "locus": "fixture",
                            "why": "fixture",
                        }
                    ]
                }
                found = rubrics.check_overrides(
                    document,
                    {"target": {"basis": "place-1"}},
                    {"place-1": 0},
                    "fixture/rubrics.yaml",
                )
                self.assertEqual(len(found), 1, found)
                if rubrics.shutil.which("node"):
                    self.assertIn("JavaScript's RegExp", found[0])
                else:
                    self.assertIn("cannot be proved portable", found[0])

        if rubrics.shutil.which("node"):
            # JavaScript named groups are valid consumer syntax but not valid
            # Python `re` syntax.  Accepting one proves this boundary is not a
            # Python-flavoured blacklist under another name.
            self.assertIsNone(rubrics.javascript_regex_problem("(?<key>a)"))

    def test_node_free_regex_validation_accepts_only_the_portable_subset(self) -> None:
        with mock.patch.object(rubrics.shutil, "which", return_value=None):
            self.assertIsNone(rubrics.javascript_regex_problem(r"^pentecost-\d+$"))
            for pattern in ("(?#comment)a", "(?>a)", "a++"):
                with self.subTest(pattern=pattern):
                    self.assertIn(
                        "cannot be proved portable",
                        rubrics.javascript_regex_problem(pattern),
                    )


class OptionalDayChoiceTests(unittest.TestCase):
    """Optional memorial permissions are choices among selectable formularies."""

    EXPECTED = {
        "single": [
            "saint-apollinaris-bishop-martyr",
            "ot-16-monday",
        ],
        "joint-reduction": [
            "immaculate-heart-blessed-virgin-mary",
            "saint-boniface-bishop-martyr",
            "ot-9-saturday",
        ],
    }

    @classmethod
    def setUpClass(cls) -> None:
        if not rubrics.shutil.which("node"):
            raise unittest.SkipTest("node is not installed")
        built, problems, _ = rubrics.build(CALENDARS, "postconciliar")
        if problems:
            raise AssertionError("; ".join(problems))
        index = calendar_days.load_calendar(CALENDARS, "postconciliar")
        years = calendar_days.build_years(index, [2026, 2027])
        calendar_days.with_fixed(index, [2026])
        fresh_2026 = calendar_days.year_document(index, 2026, years)
        cases = []
        for identifier, date in (("single", "2026-07-20"), ("joint-reduction", "2027-06-05")):
            if identifier == "single":
                year = fresh_2026
            else:
                year_path = DATA.parent / "calendar" / "postconciliar" / f"{date[:4]}.json"
                if not year_path.is_file():
                    raise unittest.SkipTest(f"no calendar year file at {year_path}")
                year = json.loads(year_path.read_text(encoding="utf-8"))
            cases.append(
                {
                    "id": identifier,
                    "date": date,
                    "year": year,
                    "rubrics": built[0],
                }
            )
        answered = rubrics.run_model({"cases": cases})
        cls.branches = {}
        for row in answered["results"]:
            if not row.get("ok"):
                raise AssertionError(row.get("error"))
            options = row["result"]["options"]
            if len(options) != 1:
                raise AssertionError(f"{row['id']}: expected one branch, got {len(options)}")
            cls.branches[row["id"]] = options[0]
        cls.formularies = rubrics.all_formularies(CALENDARS, "postconciliar")

    def test_choice_is_first_class_and_never_a_silent_winner(self) -> None:
        for identifier, branch in self.branches.items():
            with self.subTest(case=identifier):
                self.assertTrue(branch["choiceRequired"])
                self.assertIsNone(branch["winner"])
                self.assertTrue(branch["settled"])
                self.assertEqual(branch["unsettled"], [])
                self.assertEqual(branch["choice"]["id"], "calendar-formulary")
                self.assertTrue(branch["choice"]["required"])

    def test_a_lone_optional_memorial_keeps_the_weekday_candidate(self) -> None:
        branch = self.branches["single"]
        expected = [
            (
                "ot-16-monday",
                "Monday of the Sixteenth Week in Ordinary Time",
            ),
            (
                "saint-apollinaris-bishop-martyr",
                "Saint Apollinaris, Bishop and Martyr",
            ),
        ]
        self.assertEqual(
            [(row["key"], row["name"]) for row in branch["candidates"]],
            expected,
        )
        self.assertEqual(
            [row["id"] for row in branch["candidates"]],
            [key for key, _ in expected],
        )

    def test_choice_provenance_covers_reduction_permission_and_weekday(self) -> None:
        ordinary = self.branches["single"]["choice"]["locus"]
        joint = self.branches["joint-reduction"]["choice"]["locus"]
        for locus in (ordinary, joint):
            self.assertIn("NUALC 14", locus)
            self.assertIn("NUALC 59 table 12", locus)
            self.assertIn("NUALC 16 c", locus)
            self.assertIn("NUALC 59 table 13", locus)
        self.assertNotIn("2671/98/L", ordinary)
        self.assertIn("Notification Prot. n. 2671/98/L", joint)
        self.assertIn("Notitiae 35 (1999), 157", joint)

    def test_every_choice_arm_is_the_same_selectable_formulary_identity(self) -> None:
        for identifier, branch in self.branches.items():
            with self.subTest(case=identifier):
                options = branch["choice"]["among"]
                keys = [one["key"] for one in options]
                self.assertEqual(keys, self.EXPECTED[identifier])
                self.assertEqual([one["id"] for one in options], keys)
                self.assertTrue(set(keys) <= self.formularies)
                readable = branch["readable"]
                self.assertEqual([one["key"] for one in readable], keys)
                self.assertTrue(all(one["state"] == "option" for one in readable))
                self.assertTrue(
                    all(one["choice"] == "calendar-formulary" for one in readable)
                )
                self.assertNotIn("said", {one["state"] for one in readable})


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
        "massChoices": [],
        "readable": [{"key": "passion-wednesday", "state": "said"}],
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
