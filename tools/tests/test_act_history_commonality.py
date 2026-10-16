"""Commonality counts prayers separately from container and order files."""

import argparse
import contextlib
import copy
import importlib.machinery
import importlib.util
import io
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
INVENTORIES = ROOT / "src/sources/inventories"
KEYS = ("same_text", "differing_text", "only_a", "only_b")


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "act_history_commonality_test", str(ROOT / "tools/act-history")
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class CommonalityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool()
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = pathlib.Path(cls.tmp.name)
        cls.data = cls.tool.load(INVENTORIES / "latin-missal-acts-v1.toml")
        cls.repo = cls.root / "missal"
        cls.tool.emit(cls.data, cls.repo)

    def pair(self, left, right):
        return self.tool.commonality(self.data, self.repo, (left, right))["pairs"][0]

    def test_real_roman_comparison_counts_units_and_order_changes_separately(self):
        row = self.pair("typica", "usus-antiquior")
        self.assertEqual(["editio-typica-1962"], row["shared_base"])
        self.assertEqual((18, 2, 0, 11), tuple(len(row["units"][key]) for key in KEYS))
        self.assertEqual((9, 1, 0, 0), tuple(len(row["structural_files"][key]) for key in KEYS))
        self.assertEqual(
            ["ordo-missae/ordo-missae/order.txt"],
            row["structural_files"]["differing_text"],
        )
        self.assertEqual(
            {"ordo-missae/ordo-missae/confiteor.txt",
             "ordo-missae/ordo-missae/psalmus-lavabo.txt"},
            set(row["units"]["differing_text"]),
        )
        # Preserve the existing file-level JSON contract, including its order diff.
        self.assertEqual((27, 3, 0, 11), tuple(len(row[key]) for key in KEYS))
        for key in KEYS:
            self.assertEqual(set(row[key]), set(row["units"][key]) | set(row["structural_files"][key]))
            self.assertFalse(set(row["units"][key]) & set(row["structural_files"][key]))

    def test_an_empty_text_line_does_not_acquire_units_from_structure(self):
        row = self.pair("sarum", "typica")
        self.assertEqual([], row["shared_base"])
        self.assertEqual((0, 0, 0, 20), tuple(len(row["units"][key]) for key in KEYS))
        self.assertEqual((0, 0, 0, 10), tuple(len(row["structural_files"][key]) for key in KEYS))

    def test_a_group_title_change_changes_no_unit(self):
        data = copy.deepcopy(self.data)
        data["lines"].append({"id": "constructed", "label": "Constructed test line"})
        parent = next(row for row in data["acts"] if row["id"] == "rescriptum-traditionis-custodes-2023")
        act = {**parent, "id": "constructed-title-change", "line": "constructed",
               "date": "2024-01-01", "parents": [parent["id"]],
               "title": "Constructed test, not a historical claim",
               "parent_basis": "Constructed by the commonality test."}
        data["acts"].append(act)
        data["departures"].append({
            "act": act["id"], "mass": "ordo-missae", "kind": "renamed",
            "title": "Constructed heading", "basis": "Constructed by this test.",
        })
        repo = self.root / "title-change"
        self.tool.emit(data, repo)
        row = self.tool.commonality(data, repo, ("constructed", "usus-antiquior"))["pairs"][0]
        self.assertEqual((31, 0, 0, 0), tuple(len(row["units"][key]) for key in KEYS))
        self.assertEqual(
            ["ordo-missae/ordo-missae/mass.txt"],
            row["structural_files"]["differing_text"],
        )
        self.assertEqual(9, len(row["structural_files"]["same_text"]))

    def test_law_division_headers_are_not_canons(self):
        data = self.tool.load(INVENTORIES / "canon-law-acts-v1.toml")
        repo = self.root / "law"
        self.tool.emit(data, repo)
        rows = self.tool.commonality(data, repo, None)["pairs"]
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(lines=(row["a"], row["b"])):
                structure = [path for key in KEYS for path in row["structural_files"][key]]
                self.assertTrue(structure)
                self.assertTrue(all(path.endswith(("/division.txt", "/order.txt")) for path in structure))
                units = [path for key in KEYS for path in row["units"][key]]
                self.assertTrue(units)
                self.assertFalse(any(path.endswith(("/division.txt", "/order.txt")) for path in units))
                for key in KEYS:
                    self.assertEqual(set(row[key]), set(row["units"][key]) | set(row["structural_files"][key]))

    def test_cli_labels_the_two_counts_separately(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.tool.render(
                {"pairs": [self.pair("typica", "usus-antiquior")]},
                argparse.Namespace(command="commonality", json=False),
            )
        self.assertIn("units       : 18 identical, 2 differing", output.getvalue())
        self.assertIn("structure   : 9 identical, 1 differing", output.getvalue())
        self.assertNotIn("units       : 27", output.getvalue())


if __name__ == "__main__":
    unittest.main()
