"""Source-owned, form-qualified Proper discovery projection and public gate."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import json
import os
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src/web/data/structure/propers"


def load_tool(path: Path, name: str):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ProperSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_tool(ROOT / "tools/mass-propers", "proper_search_generator_test")
        cls.release = load_tool(ROOT / "tools/public-alpha", "proper_search_release_test")
        cls.structures = {
            calendar: json.loads((DATA / f"{calendar}.json").read_text(encoding="utf-8"))
            for calendar in ("roman-1962", "postconciliar", "roman-pre-1955")
        }
        cls.search = {
            calendar: cls.generator.search_structure(structure)
            for calendar, structure in cls.structures.items()
        }

    def test_forms_are_distinct_and_match_the_served_proper_scope(self) -> None:
        rows = [row for row in self.search["roman-1962"]["rows"] if row["key"] ==
                "commemoratione-omnium-fidelium-defunctorum"]
        self.assertEqual([row["form_id"] for row in rows], ["first", "second", "third"])
        self.assertEqual([row["coverage"]["languages"][1]["occurrences"] for row in rows],
                         [6, 6, 6])
        self.assertTrue(all(row["fixed_date"] == "11-02" for row in rows))
        self.assertTrue(all(row["form_name"] for row in rows))
        self.assertEqual(len({(row["key"], row["form_id"]) for row in
                              self.search["roman-1962"]["rows"]}),
                         len(self.search["roman-1962"]["rows"]))

    def test_index_keeps_citations_and_cycle_context_without_body_text(self) -> None:
        pentecost = next(row for row in self.search["roman-1962"]["rows"]
                         if row["key"] == "pentecost")
        self.assertIn("Spiritus Domini", {row["text"] for row in pentecost["incipits"]})
        self.assertTrue(any(row["ref"] == "Wisdom 1:7" and row["slot"] == "Introit"
                            for row in pentecost["citations"]))
        transfiguration = next(row for row in self.search["postconciliar"]["rows"]
                               if row["key"] == "transfiguration-lord")
        gospel_cycles = {row["cycle"] for row in transfiguration["citations"]
                         if row["slot"] == "Gospel" and row["cycle_family"] == "cycles"}
        self.assertEqual(gospel_cycles, {"A", "B", "C"})
        forbidden = {"text", "latin", "provenance", "caution", "source_refs", "loci",
                     "rights", "source_id", "artifact_id", "locator"}
        for index in self.search.values():
            def walk(value):
                if isinstance(value, dict):
                    self.assertFalse(forbidden.intersection(value))
                    for item in value.values():
                        walk(item)
                elif isinstance(value, list):
                    for item in value:
                        walk(item)
            # The only `text` field is a short incipit, with an exact schema
            # and a public-alpha length/rights guard.
            for row in index["rows"]:
                for incipit in row["incipits"]:
                    self.assertLessEqual(len(incipit["text"]), 160)
            walk({**index, "rows": [{**row, "incipits": []} for row in index["rows"]]})

    def test_public_gate_rejects_body_and_private_metadata(self) -> None:
        valid = copy.deepcopy(self.search["roman-1962"])
        valid["rows"] = [next(row for row in valid["rows"] if row["key"] == "pentecost")]
        self.release.validate_proper_search_payload(valid, "search fixture", "roman-1962")
        mutations = (
            ("row body", lambda doc: doc["rows"][0].update(text="protected text")),
            ("witness audit", lambda doc: doc["rows"][0]["witnesses"][0].update(
                source_id="artifact.private")),
            ("incipit body", lambda doc: doc["rows"][0]["incipits"][0].update(
                text="a" * 161)),
            ("wrong calendar", lambda doc: doc.update(calendar="postconciliar")),
        )
        for name, mutate in mutations:
            changed = copy.deepcopy(valid)
            mutate(changed)
            with self.subTest(name=name), self.assertRaises(self.release.ReleaseError):
                self.release.validate_proper_search_payload(
                    changed, "search fixture", "roman-1962")

    def test_tracked_indexes_rederive_exactly(self) -> None:
        for calendar, index in self.search.items():
            with self.subTest(calendar=calendar):
                path = DATA / "search" / f"{calendar}.json"
                self.assertEqual(path.read_text(encoding="utf-8"),
                                 self.generator._serialise(index))

    def test_scoped_check_preserves_siblings_and_unscoped_check_sees_orphans(self) -> None:
        scratch = Path(os.environ.get("TRIPTYCH_SEARCH_TEST_SCRATCH",
                                      ROOT / ".scratch/proper-search-tests"))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            output = Path(temporary)
            args = Namespace(root=str(ROOT / "src/sources/calendars"), out=str(output),
                             calendar="roman-1962", check=False, verbose=False)
            self.generator.run_structure(args)
            foreign = output / "structure/propers/search/foreign.json"
            foreign.write_text("{}\n", encoding="utf-8")
            nested = output / "structure/propers/search/extra/hidden.json"
            nested.parent.mkdir()
            nested.write_text("{}\n", encoding="utf-8")
            args.check = True
            scoped = self.generator.run_structure(args)
            self.assertEqual(scoped["status"], "ok")
            self.assertTrue(foreign.is_file() and nested.is_file())
            args.calendar = None
            full = self.generator.run_structure(args)
            self.assertEqual(full["status"], "stale")
            self.assertIn(str(foreign), full["drifted"])
            self.assertIn(str(nested), full["drifted"])


if __name__ == "__main__":
    unittest.main()
