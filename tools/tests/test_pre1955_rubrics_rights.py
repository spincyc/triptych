#!/usr/bin/env python3
"""Rights boundary for the pre-1955 rubrics finding aid."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src" / "sources" / "calendars"
PRE1955 = CALENDARS / "roman-pre-1955" / "rubrics.yaml"
ROMAN_1962 = CALENDARS / "roman-1962" / "rubrics.yaml"
TOOL = ROOT / "tools" / "calendar-rubrics"

WITHHELD = (
    "impediment.transfer.proper_seats[0].latin",
    "impediment.transfer.proper_seats[1].latin",
    "impediment.transfer.keeps_its_class.latin",
    "impediment.fixed_commemoration.latin",
    "impediment.sunday_not_resumed.latin",
    "commemoration.kinds.latin",
    "commemoration.ceilings.latin",
    "commemoration.order.latin",
    "commemoration.surplus.latin",
    "mass_category.latin",
)
AUTHORIZED_LATIN = frozenset(("precedence.latin", "saturday_office.latin"))
STATUS = {
    "state": "unavailable",
    "scope": "rubric-wording",
    "kind": "rights-withheld",
    "paths": list(WITHHELD),
}
MISSING = object()


def load(path: Path) -> dict:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise AssertionError(f"{path}: expected a mapping")
    return document


def values_at_key(value: object, wanted: str) -> list[object]:
    found: list[object] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == wanted:
                found.append(child)
            found.extend(values_at_key(child, wanted))
    elif isinstance(value, list):
        for child in value:
            found.extend(values_at_key(child, wanted))
    return found


def keyed_paths(value: object, wanted: str, path: str = "") -> dict[str, object]:
    found: dict[str, object] = {}
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if key == wanted:
                found[child_path] = child
            found.update(keyed_paths(child, wanted, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.update(keyed_paths(child, wanted, f"{path}[{index}]"))
    return found


def path_value(document: object, path: str) -> object:
    current = document
    for part in path.split("."):
        name, marker, index = part.partition("[")
        if not isinstance(current, dict) or name not in current:
            return MISSING
        current = current[name]
        if marker:
            if not index.endswith("]") or not index[:-1].isdigit():
                return MISSING
            position = int(index[:-1])
            if not isinstance(current, list) or position >= len(current):
                return MISSING
            current = current[position]
    return current


class Pre1955RubricsRightsTests(unittest.TestCase):
    def assert_quarantine(self, document: dict) -> None:
        self.assertEqual(document.get("latin_text_status"), STATUS)
        for path in WITHHELD:
            self.assertIs(path_value(document, path), MISSING, path)
        latin = keyed_paths(document, "latin")
        self.assertEqual(set(latin), AUTHORIZED_LATIN)
        self.assertTrue(all(isinstance(value, str) and value.strip() for value in latin.values()))

    def assert_public_quarantine(self, document: dict) -> None:
        self.assertEqual(document.get("latin_text_status"), {"kind": "rights-withheld"})
        for path in WITHHELD:
            self.assertIs(path_value(document, path), MISSING, path)
        latin = keyed_paths(document, "latin")
        self.assertEqual(set(latin), AUTHORIZED_LATIN)

    def test_source_retains_only_independently_supported_latin(self) -> None:
        source = load(PRE1955)
        self.assert_quarantine(source)

        # A recension may share structure with its descendant, but it may not
        # acquire a Latin witness by copying the descendant's wording.
        later_latin = set(keyed_paths(load(ROMAN_1962), "latin").values())
        self.assertTrue(set(keyed_paths(source, "latin").values()).isdisjoint(later_latin))

    def test_fresh_public_projection_keeps_the_typed_absence_not_the_audit(self) -> None:
        with tempfile.TemporaryDirectory() as held:
            out = Path(held) / "data"
            finished = subprocess.run(
                [
                    sys.executable,
                    str(TOOL),
                    "structure",
                    "--root",
                    str(CALENDARS),
                    "--calendar",
                    "roman-pre-1955",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(finished.returncode, 0, finished.stderr or finished.stdout)
            projection = json.loads(
                (out / "structure" / "rubrics" / "roman-pre-1955.json").read_text(
                    encoding="utf-8"
                )
            )

        self.assert_public_quarantine(projection)
        self.assertNotIn("derived_from", projection)
        self.assertEqual(values_at_key(projection, "derived_from"), [])


if __name__ == "__main__":
    unittest.main()
