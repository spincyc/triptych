"""St Lucy's source-held antiphon has a typed English gap and sound Latin."""
from __future__ import annotations

import contextlib
import importlib.machinery
import importlib.util
import io
from pathlib import Path
import sys
import tomllib
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]


def tool(name):
    loader = importlib.machinery.SourceFileLoader(
        "st_lucy_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class StLucyDispositionTests(unittest.TestCase):
    def test_mixed_communion_has_one_exact_english_absence_in_both_calendars(self):
        inventory = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml")
                                  .read_text(encoding="utf-8"))
        rows = [row for row in inventory["untranslated"]
                if (row["mass"], row["form_id"], row["proper"], row["cycle"], row["occurrence"],
                    row["lang"], row["extent"]) ==
                ("s-luciae-virginis-martyris", "main", "Communion", "all", 1, "en", "body")]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["reason"], {"kind": "no-exemplar"})
        self.assertEqual(rows[0]["availability"], "unavailable")
        self.assertIn("quasi", rows[0]["note"])
        self.assertIn("sicut", rows[0]["note"])

        propers = tool("mass-propers")
        root = ROOT / "src/sources/calendars"
        for calendar in ("roman-1962", "roman-pre-1955"):
            with self.subTest(calendar=calendar):
                coverage = propers.english_coverage(root, calendar)
                self.assertEqual(coverage["unaccounted"], 0)
                self.assertGreater(coverage["ledgered_untranslated"], 0)

    def test_page_reading_exception_is_narrow_to_st_lucy_communion(self):
        audit = tool("audit-latin-body-substitutions")
        document = {"sections": {"test": {"masses": [
            {"key": "s-luciae-virginis-martyris",
             "propers": [{"name": "Communion", "text": "gratis"}]},
            {"key": "another-mass", "propers": [{"name": "Communion", "text": "gratis"}]},
            {"key": "known-form", "propers": [{"name": "Collect", "text": "gratiae " * 5}]},
        ]}}}
        with mock.patch.object(audit._calendars, "read_yaml", return_value=document), \
             mock.patch.object(sys, "argv", ["audit-latin-body-substitutions"]), \
             contextlib.redirect_stdout(io.StringIO()) as stdout, \
             contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(audit.main(), 0)
        self.assertEqual(stdout.getvalue().strip(),
                         "another-mass/Communion\tgratis\treads as\tgratiae")


if __name__ == "__main__":
    unittest.main()
