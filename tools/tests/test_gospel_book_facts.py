"""The source-selected Gospel book is derived once for browser and terminal."""
from __future__ import annotations

import importlib.machinery
import importlib.util
from pathlib import Path
import subprocess
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[2]


class GospelBookFacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader("gospel_book_mass_today", str(ROOT / "tools/mass-today"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.tool = importlib.util.module_from_spec(spec)
        loader.exec_module(cls.tool)

    def test_shared_model_and_browser_adapter_contracts(self):
        result = subprocess.run(
            ["node", "--test", "tools/tests/gospel_book_facts.mjs"], cwd=ROOT,
            capture_output=True, text=True, timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_mass_cli_uses_the_same_prepared_gospel_book_and_preserves_context(self):
        tool = self.tool
        file = {"sections": [{"key": "word", "elements": [
            {"key": "word/heading-" + book, "conditions": [{"kind": "include-when-any",
             "predicates": ["gospel-book-" + book], "basis": "Synthetic source heading."}]}
            for book in ("matthew", "mark", "luke", "john")
        ] + [{"key": "word/proclamation"}, {"key": "word/closing"}]}],
            "slots": [{"key": "gospel", "propers": ["Gospel"], "anchor": "word/proclamation", "where": "after"}]}
        proper = {"name": "Gospel", "form_id": "main", "source": "scripture", "cycles": {
            "A": {"citations": [{"book": "Matthew", "ref": "Matthew 1:1"}]},
            "B": {"citations": [{"book": "Mark", "ref": "Mark 1:1"}]}}}
        for cycle, expected in (("A", "matthew"), ("B", "mark"), (None, None)):
            context = {"settled": True, "weekday": "sunday", "nature": "sunday", "season": "ordinary",
                       "date": "2026-10-04", "calendarCycles": {"sunday": cycle, "weekday": "II"}}
            before = repr(context)
            result = tool.mass_events(file, [proper], None, context)
            headings = [event["element"]["key"] for event in result["events"]
                        if event["kind"] == "ordinary_element" and event["element"]["key"].startswith("word/heading-")]
            self.assertEqual(headings, [] if expected is None else ["word/heading-" + expected])
            self.assertEqual(repr(context), before)

    def test_cli_retains_original_parent_citations_privately_before_cycle_flattening(self):
        tool = self.tool
        ordinary = {"sections": [{"key": "word", "elements": [
            {"key": "word/heading-luke", "conditions": [{"kind": "include-when-any",
             "predicates": ["gospel-book-luke"], "basis": "Synthetic source heading."}]},
            {"key": "word/proclamation"}, {"key": "word/closing"}]}],
            "slots": [{"key": "gospel", "propers": ["Gospel"], "anchor": "word/proclamation", "where": "after"}]}
        for parent, child, expected in (("John", {"citations": [{"book": "Luke", "ref": "Luke 1:1"}]}, False),
                                         ("Luke", {"text": "Synthetic selected child wording."}, True)):
            raw = {"name": "Gospel", "source": "scripture", "form_id": "main",
                   "citations": [{"book": parent, "ref": parent + " 1:1"}], "cycles": {"A": child}}
            payload = {"mass": {"key": "synthetic"}, "appointed": [{"proper": raw, "form_id": "main"}]}
            result = tool.propers_of("synthetic-edition", "synthetic", SimpleNamespace(form=None),
                                     {"sunday": "A", "weekday": "II"}, payload=payload)
            self.assertNotIn("refused", result)
            originals = result["_ordinary_source_rows"]
            self.assertEqual(originals[0]["proper"]["citations"], raw["citations"])
            context = {"properRows": originals, "calendarCycles": {"sunday": "A", "weekday": "II"}}
            events = tool.mass_events(ordinary, result["propers"], None, context)["events"]
            headings = [event for event in events if event["kind"] == "ordinary_element"
                        and event["element"]["key"] == "word/heading-luke"]
            self.assertEqual(bool(headings), expected)


if __name__ == "__main__":
    unittest.main()
