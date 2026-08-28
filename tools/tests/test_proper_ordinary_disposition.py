"""Exact source-to-public semantics for non-cumulative Proper rows."""

from __future__ import annotations

import argparse
import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _calendars  # noqa: E402


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = SourceFileLoader(f"_ordinary_disposition_{name.replace('-', '_')}", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


checker = load_tool("check-calendar-masses")
propers_tool = load_tool("mass-propers")
today_tool = load_tool("mass-today")

BASIS = "The source prints these as coequal forms of one appointment."
FORM_BASIS = "The source rite cannot use the generic Mass frame."


def alternative(option: str, *, group: str = "gospel-form", basis: str = BASIS) -> dict:
    return {
        "kind": "alternative",
        "group": group,
        "option": option,
        "basis": basis,
    }


def unplaced(region: str = "before-frame") -> dict:
    return {
        "kind": "unplaced",
        "group": "blessing-outside-mass",
        "region": region,
        "basis": "The source prints this blessing outside the Mass frame.",
    }


def composed(name: str, text: str, disposition: dict | None = None) -> dict:
    proper = {"name": name, "source": "composed", "text": text}
    if disposition is not None:
        proper[_calendars.ORDINARY_DISPOSITION] = disposition
    return proper


def document(masses: list[dict]) -> dict:
    return {
        "calendar": "synthetic",
        "edition": "Synthetic source edition",
        "edition_short": "Synthetic Missal",
        "psalm_numbering": "vulgate",
        "sections": {"seasonal": {"kind": "seasonal", "masses": masses}},
    }


class ClosedShapeTests(unittest.TestCase):
    def test_the_two_exact_shapes_round_trip_unchanged(self) -> None:
        for value in (alternative("principal"), unplaced("after-frame")):
            with self.subTest(kind=value["kind"]):
                self.assertEqual(
                    _calendars.validate_ordinary_disposition(value), value
                )
                self.assertEqual(propers_tool.public_ordinary_disposition(value), value)

    def test_unknown_missing_and_mistyped_fields_are_refused(self) -> None:
        malformed = (
            None,
            {"kind": "selected", "group": "gospel-form", "basis": BASIS},
            {"kind": "alternative", "group": "gospel-form", "basis": BASIS},
            {**alternative("principal"), "extra": True},
            alternative("Principal"),
            {**alternative("principal"), "basis": ""},
            {**unplaced(), "region": "after-seat"},
        )
        for value in malformed:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    _calendars.validate_ordinary_disposition(value)

    def test_calendar_checker_accepts_the_field_on_propers_and_frames_on_forms(self) -> None:
        mass = {
            "key": "synthetic-mass",
            "name": "Synthetic Mass",
            "registry": "synthetic",
            "season": "advent",
            "forms": [
                {
                    "id": "long-form",
                    "name": "Long form",
                    "ordinary_frame": {
                        "applicability": "unavailable",
                        "basis": FORM_BASIS,
                    },
                    "propers": [
                        composed("Gospel", "Long", alternative("long")),
                        composed(
                            "Gospel (shorter)", "Short", alternative("short")
                        ),
                    ],
                }
            ],
        }
        problems: list[str] = []
        checker.check_entry(mass, 0, problems, "seasonal", "synthetic")
        _, resolution_problems = _calendars.resolve_propers(document([mass]), mass)
        self.assertEqual(problems, [])
        self.assertEqual(resolution_problems, [])


class ResolutionTests(unittest.TestCase):
    def test_reference_wrappers_keep_appointment_local_dispositions(self) -> None:
        target = {
            "key": "printed-there",
            "propers": [
                composed("Gospel", "Long wording"),
                composed("Gospel (shorter)", "Short wording"),
            ],
        }
        appointed = {
            "key": "appointed-here",
            "propers": [
                {
                    "name": "Gospel",
                    "takes_from": {"mass": "printed-there"},
                    "ordinary_disposition": alternative("long"),
                },
                {
                    "name": "Gospel (shorter)",
                    "takes_from": {"mass": "printed-there"},
                    "ordinary_disposition": alternative("short"),
                },
            ],
        }
        entries, problems = _calendars.resolve_propers(
            document([target, appointed]), appointed
        )
        self.assertEqual(problems, [])
        self.assertEqual(
            [proper["text"] for _, proper, _ in entries],
            ["Long wording", "Short wording"],
        )
        self.assertEqual(
            [proper["ordinary_disposition"] for _, proper, _ in entries],
            [alternative("long"), alternative("short")],
        )

    def test_whole_formulary_inheritance_keeps_target_annotations(self) -> None:
        target = {
            "key": "printed-there",
            "propers": [
                composed("Gospel", "Long", alternative("long")),
                composed("Gospel (shorter)", "Short", alternative("short")),
            ],
        }
        appointed = {"key": "appointed-here", "takes_from": {"mass": "printed-there"}}
        entries, problems = _calendars.resolve_propers(
            document([target, appointed]), appointed
        )
        self.assertEqual(problems, [])
        self.assertEqual(
            [proper["ordinary_disposition"]["option"] for _, proper, _ in entries],
            ["long", "short"],
        )

    def test_text_override_keeps_the_inherited_slot_disposition(self) -> None:
        target = {
            "key": "printed-there",
            "propers": [
                composed("Gospel", "Long", alternative("long")),
                composed("Gospel (shorter)", "Short", alternative("short")),
            ],
        }
        appointed = {
            "key": "appointed-here",
            "takes_from": {"mass": "printed-there"},
            "propers": [composed("Gospel", "Locally printed long wording")],
        }
        entries, problems = _calendars.resolve_propers(
            document([target, appointed]), appointed
        )
        self.assertEqual(problems, [])
        self.assertEqual(
            [proper["ordinary_disposition"]["option"] for _, proper, _ in entries],
            ["long", "short"],
        )
        self.assertEqual(entries[0][1]["text"], "Locally printed long wording")

    def test_effective_group_validation_is_self_cleaning(self) -> None:
        cases = {
            "singleton": [composed("Gospel", "Long", alternative("long"))],
            "basis drift": [
                composed("Gospel", "Long", alternative("long")),
                composed(
                    "Gospel (shorter)",
                    "Short",
                    alternative("short", basis="A different asserted basis."),
                ),
            ],
            "mixed kinds": [
                composed("Gospel", "Long", alternative("long", group="shared")),
                composed(
                    "Gospel (shorter)",
                    "Short",
                    alternative("short", group="shared"),
                ),
                composed(
                    "Blessing",
                    "Bless",
                    {**unplaced(), "group": "shared"},
                ),
            ],
            "unplaced mismatch": [
                composed("Blessing", "One", unplaced("before-frame")),
                composed("Dismissal", "Two", unplaced("after-frame")),
            ],
            "noncontiguous alternative": [
                composed("Gospel", "Long", alternative("long")),
                composed("Offertory", "Middle"),
                composed("Gospel (shorter)", "Short", alternative("short")),
            ],
            "before-frame is not a prefix": [
                composed("Introit", "First"),
                composed("Blessing", "Second", unplaced("before-frame")),
            ],
            "after-frame is not a suffix": [
                composed("Dismissal", "First", unplaced("after-frame")),
                composed("Postcommunion", "Second"),
            ],
        }
        for label, propers in cases.items():
            with self.subTest(case=label):
                mass = {"key": "synthetic", "propers": propers}
                _, problems = _calendars.resolve_propers(document([mass]), mass)
                self.assertTrue(problems)

    def test_one_option_may_bundle_several_rows(self) -> None:
        mass = {
            "key": "synthetic",
            "propers": [
                composed("Gospel (principal, part one)", "One", alternative("principal")),
                composed("Gospel (principal, part two)", "Two", alternative("principal")),
                composed("Gospel (other, part one)", "Three", alternative("other")),
                composed("Gospel (other, part two)", "Four", alternative("other")),
            ],
        }
        _, problems = _calendars.resolve_propers(document([mass]), mass)
        self.assertEqual(problems, [])


class ProjectionTests(unittest.TestCase):
    def source_document(self) -> dict:
        return document(
            [
                {
                    "key": "flat",
                    "name": "Flat",
                    "season": "advent",
                    "registry": "flat",
                    "propers": [composed("Blessing", "Bless", unplaced())],
                },
                {
                    "key": "formed",
                    "name": "Formed",
                    "season": "advent",
                    "registry": "formed",
                    "forms": [
                        {
                            "id": "long-form",
                            "name": "Long form",
                            "ordinary_frame": {
                                "applicability": "unavailable",
                                "basis": FORM_BASIS,
                            },
                            "propers": [
                                composed("Gospel", "Long", alternative("long")),
                                composed(
                                    "Gospel (shorter)",
                                    "Short",
                                    alternative("short"),
                                ),
                            ],
                        }
                    ],
                },
            ]
        )

    def test_structure_preserves_dispositions_in_flat_and_nested_form_views(self) -> None:
        source = self.source_document()
        with (
            patch.object(propers_tool, "load_calendar", return_value=source),
            patch.object(
                propers_tool, "translation_overlay", return_value=({}, {}, [], {})
            ),
            patch.object(propers_tool, "publication_records", return_value=({}, [])),
        ):
            structure = propers_tool.calendar_structure(ROOT, "synthetic", {})
        masses = {mass["key"]: mass for mass in structure["masses"]}
        self.assertEqual(masses["flat"]["propers"][0]["ordinary_disposition"], unplaced())
        formed = masses["formed"]
        self.assertEqual(
            [row["ordinary_disposition"] for row in formed["propers"]],
            [alternative("long"), alternative("short")],
        )
        self.assertEqual(
            [row["ordinary_disposition"] for row in formed["forms"][0]["propers"]],
            [alternative("long"), alternative("short")],
        )
        self.assertEqual(
            formed["forms"][0]["ordinary_frame"],
            {"applicability": "unavailable", "basis": FORM_BASIS},
        )

    def test_mass_today_uses_form_frame_before_mass_frame(self) -> None:
        payload = {
            "edition": "Synthetic",
            "mass": {
                "rank": "test",
                "ordinary_frame": {
                    "applicability": "none",
                    "basis": "Mass-level fallback.",
                },
                "forms": [
                    {
                        "id": "long-form",
                        "name": "Long form",
                        "ordinary_frame": {
                            "applicability": "unavailable",
                            "basis": FORM_BASIS,
                        },
                        "propers": [],
                    },
                    {"id": "short-form", "name": "Short form", "propers": []},
                ],
            },
            "appointed": [
                {
                    "form": "Long form",
                    "form_id": "long-form",
                    "proper": composed("Gospel", "Long"),
                },
                {
                    "form": "Short form",
                    "form_id": "short-form",
                    "proper": composed("Gospel", "Short"),
                },
            ],
        }
        long = today_tool.propers_of(
            "synthetic", "formed", argparse.Namespace(form="long-form"), payload=payload
        )
        short = today_tool.propers_of(
            "synthetic", "formed", argparse.Namespace(form="short-form"), payload=payload
        )
        self.assertEqual(long["ordinary_frame"]["basis"], FORM_BASIS)
        self.assertEqual(short["ordinary_frame"]["basis"], "Mass-level fallback.")
        self.assertEqual(long["forms"][0]["ordinary_frame"], long["ordinary_frame"])


if __name__ == "__main__":
    unittest.main()
