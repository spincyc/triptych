"""`check-calendar-masses` refuses a mapping key written twice in a calendar file.

A YAML loader keeps the last value of a repeated key and reports nothing. On
2026-10-19 the 1962 index carried 154 `notes` keys written twice on one proper,
so one of each pair, often the page-image provenance note, never reached any
tool. The fix merged the pairs; this holds the gate that keeps them merged.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src/sources/calendars"


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = SourceFileLoader(f"_{name.replace('-', '_')}_dupkeys", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


checker = load_tool("check-calendar-masses")

DUPLICATED = """\
schema: triptych-calendar-masses/v1
sections:
  seasonal:
    masses:
    - key: fixture
      propers:
      - name: Collect
        notes: >-
          The first value, which a loader drops.
        text: |
          Fixture body.
        notes: The second value, which a loader keeps.
"""


class DuplicateKeyTests(unittest.TestCase):
    def write(self, root: Path, relative: str, text: str) -> Path:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_a_key_written_twice_on_one_proper_is_refused_with_both_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write(root, "fixture/propers.yaml", DUPLICATED)
            problems = checker.duplicate_key_problems(root, None)
        self.assertEqual(len(problems), 1, problems)
        self.assertIn("duplicate mapping key 'notes'", problems[0])
        self.assertIn("propers.yaml:12:", problems[0])
        self.assertIn("first at line 8", problems[0])

    def test_every_calendar_file_is_read_whatever_schema_it_declares(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write(root, "fixture/rubrics.yaml",
                       "schema: something-else/v1\nlabel: one\nnested:\n- a: 1\n  a: 2\nlabel: two\n")
            problems = checker.duplicate_key_problems(root, None)
            self.assertEqual(len(problems), 2, problems)
            # The calendar filter narrows the scan to one directory.
            self.assertEqual(checker.duplicate_key_problems(root, "other"), [])

    def test_distinct_keys_and_repeated_list_items_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write(root, "fixture/propers.yaml",
                       "sections:\n  s:\n    masses:\n    - key: a\n      notes: x\n    - key: b\n      notes: y\n")
            self.assertEqual(checker.duplicate_key_problems(root, None), [])

    def test_the_tracked_calendars_carry_no_duplicate_key(self):
        self.assertEqual(checker.duplicate_key_problems(CALENDARS, None), [])

    def test_the_gate_reports_through_run(self):
        sentinel = "fixture: duplicate mapping key 'notes'"
        with mock.patch.object(checker, "duplicate_key_problems", return_value=[sentinel]) as called:
            payload = checker.run(Path("src/sources/calendars"), "roman-pre-1955")
        called.assert_called_once()
        self.assertIn(sentinel, payload["problems"])


if __name__ == "__main__":
    unittest.main()
