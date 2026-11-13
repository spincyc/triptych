"""Browser product family keys cover exactly what each producer reads.

The static tests pin the code-closure scan. The audit tests run a fixture
producer under the open-audit hook, including a Python child process. The
full-corpus audit of every real family is slow and opt-in:

    TRIPTYCH_BROWSER_PRODUCT_AUDIT=1 python -m unittest test_browser_product_inputs
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _browser_product_inputs as inputs
import _browser_product_recipes as recipes
import _browser_products as products

SCRATCH = ROOT / ".scratch/browser-product-input-tests"


def _write(root: Path, name: str, body: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(body).lstrip("\n"))


class StaticClosureTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.root = Path(self.enterContext(tempfile.TemporaryDirectory(dir=SCRATCH)))
        files = {
            "tools/producer": '''
                #!/usr/bin/env python3
                """Mentions tools/doc-only in prose, which is not a load."""
                import importlib
                from importlib.machinery import SourceFileLoader
                from pathlib import Path
                import sys
                ROOT = Path(__file__).resolve().parents[1]
                sys.path.insert(0, str(ROOT / "scripts"))
                import _plain
                from pkg import sub
                importlib.import_module("pkg.dynamic")
                for name in ("one",):
                    importlib.import_module(f"plugins.{name}")
                SourceFileLoader("sibling", str(ROOT / "tools" / "sibling")).load_module()
                def load(name):
                    return ROOT / "tools" / name
                load("loaded")
                Path(__file__).with_name("data.json")
                ASSET = "scripts/asset.js"
                REGISTRY = ("unrelated", "tests")
                FIXTURE = ROOT / "tools" / "tests" / "fixture.py"
                import _browser_products
            ''',
            "tools/sibling": "#!/usr/bin/env python3\nimport _from_sibling\n",
            "tools/loaded": "#!/usr/bin/env python3\n",
            "tools/data.json": "{}\n",
            "tools/unrelated": "#!/usr/bin/env python3\n",
            "tools/doc-only": "#!/usr/bin/env python3\n",
            "tools/tests/fixture.py": "",
            "scripts/_plain.py": "",
            "scripts/_from_sibling.py": "this is not python (\n",
            "scripts/asset.js": "",
            "scripts/pkg/__init__.py": "",
            "scripts/pkg/sub.py": "from . import neighbour\nfrom .deep import leaf\n",
            "scripts/pkg/neighbour.py": "",
            "scripts/pkg/deep/__init__.py": "",
            "scripts/pkg/deep/leaf.py": "",
            "scripts/pkg/dynamic.py": "",
            "scripts/pkg/unused.py": "",
            "scripts/plugins/__init__.py": "",
            "scripts/plugins/one.py": "",
            "scripts/plugins/two.py": "",
            "scripts/_browser_products.py": "import _receipt\nRECIPES = ['tools/unrelated']\n",
            "scripts/_receipt.py": "",
            "scripts/_browser_product_recipes.py": "",
            "scripts/_browser_product_inputs.py": "",
        }
        for name, body in files.items():
            _write(self.root, name, body)

    def closure(self, *entrypoints):
        harness = inputs.code_closure(self.root, inputs.HARNESS, literals=False)
        return inputs.code_closure(self.root, entrypoints, opaque=harness)

    def test_imports_dynamic_imports_and_path_literals_are_followed(self):
        found = self.closure("tools/producer")
        for name in ("tools/producer", "scripts/_plain.py", "scripts/pkg/__init__.py", "scripts/pkg/sub.py",
                     "scripts/pkg/neighbour.py", "scripts/pkg/deep/__init__.py", "scripts/pkg/deep/leaf.py",
                     "scripts/pkg/dynamic.py", "scripts/plugins/one.py", "scripts/plugins/two.py",
                     "tools/sibling", "scripts/_from_sibling.py", "tools/loaded", "tools/data.json",
                     "scripts/asset.js", "scripts/_browser_products.py", "scripts/_receipt.py"):
            self.assertIn(name, found)

    def test_names_that_are_data_or_tests_are_not_code(self):
        found = self.closure("tools/producer")
        for name in ("tools/unrelated", "tools/doc-only", "tools/tests/fixture.py", "scripts/pkg/unused.py"):
            self.assertNotIn(name, found)

    def test_harness_closure_follows_imports_only(self):
        harness = inputs.code_closure(self.root, inputs.HARNESS, literals=False)
        self.assertEqual(harness, {"scripts/_browser_products.py", "scripts/_receipt.py",
                                   "scripts/_browser_product_recipes.py", "scripts/_browser_product_inputs.py"})

    def test_unparseable_source_is_a_leaf(self):
        self.assertEqual(self.closure("scripts/_from_sibling.py") - inputs.code_closure(self.root, inputs.HARNESS, literals=False),
                         {"scripts/_from_sibling.py"})

    def test_family_code_includes_entrypoint_adapter_and_harness(self):
        recipe = {"id": "act-history", "argv": ["tools/producer"]}
        _write(self.root, inputs.ADAPTERS["act-history"], "import _plain\n")
        code = inputs.family_code(self.root, [recipe])["act-history"]
        self.assertIn(inputs.ADAPTERS["act-history"], code)
        self.assertIn("scripts/_browser_product_recipes.py", code)
        self.assertIn("tools/producer", code)

    def test_links_and_special_files_in_code_trees_fail_closed(self):
        for kind in ("symlink", "fifo"):
            with self.subTest(kind=kind):
                path = self.root / "scripts/_linked.py"
                if kind == "symlink":
                    path.symlink_to(self.root / "scripts/_plain.py")
                else:
                    os.mkfifo(path)
                try:
                    with self.assertRaises(inputs.ClosureError):
                        inputs.code_closure(self.root, ["tools/producer"])
                finally:
                    path.unlink()


class RepositoryClosureTests(unittest.TestCase):
    """Fast static checks over the real recipes; the audit is the proof."""

    @classmethod
    def setUpClass(cls):
        cls.recipes = products._recipes()
        cls.code = inputs.family_code(ROOT, cls.recipes)
        cls.harness = inputs.code_closure(ROOT, inputs.HARNESS, literals=False)

    def test_every_family_closure_has_its_producer_and_the_harness(self):
        self.assertEqual(len(self.recipes), 13)
        for recipe in self.recipes:
            with self.subTest(family=recipe["id"]):
                code = self.code[recipe["id"]]
                self.assertTrue(set(inputs.entrypoints(recipe)) <= code)
                self.assertTrue(set(inputs.HARNESS) <= code)
                self.assertTrue(self.harness <= code)

    def test_reader_metadata_cannot_create_a_publication_input_cycle(self):
        # Broad source scopes must remain sensitive to authored bodies without
        # binding lookup output back through the release descriptor into itself.
        SCRATCH.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            root = Path(directory)
            _write(root, "src/sources/body.tsv", "original body\n")
            _write(root, "src/index/corpus/index.json", '{"binding":"first"}\n')
            recipe = copy.deepcopy(next(row for row in self.recipes if row["id"] == "documents"))
            recipe.update(input_trees=["src"], input_files=[])
            with patch.object(products, "family_code", return_value={"documents": set()}):
                original = products._identity_batch(root, [recipe])["documents"]
                _write(root, "src/index/corpus/index.json", '{"binding":"second"}\n')
                _write(root, "src/index/documents/readers.json", '{}\n')
                self.assertEqual(original, products._identity_batch(root, [recipe])["documents"])
                _write(root, "src/sources/body.tsv", "changed body\n")
                self.assertNotEqual(original, products._identity_batch(root, [recipe])["documents"])

    def test_no_family_takes_tests_guidance_or_project_records_wholesale(self):
        # A single file the audit shows a producer reading may be declared; a
        # whole guidance, review or code tree, or a project record, may not.
        for recipe in self.recipes:
            with self.subTest(family=recipe["id"]):
                self.assertFalse(any(name.startswith("tools/tests/") for name in self.code[recipe["id"]]))
                for tree in recipe["input_trees"]:
                    for forbidden in ("guidance", "docs", "tools", "scripts", "workflows/reviews"):
                        self.assertFalse(tree == forbidden or tree.startswith(forbidden + "/")
                                         or forbidden.startswith(tree + "/"), tree)
                for name in recipe["input_files"]:
                    self.assertFalse(name.startswith(("tools/", "scripts/")), name)
                    self.assertNotIn(name, {"AGENTS.md", "PROJECT-WORK.md", "Makefile", "tmt.json",
                                            ".gitignore", ".gitattributes", "LICENSE", "THIRD_PARTY.md"})

    def test_a_tool_name_registry_does_not_join_every_closure(self):
        # `_tooling` names every tool as data; the calendar must not inherit them.
        self.assertIn("scripts/_tooling.py", self.code["calendar"])
        self.assertNotIn("tools/mass-propers", self.code["calendar"])
        self.assertNotIn("tools/public-alpha", self.code["propers"])
        self.assertLess(len(self.code["calendar"]), len(self.code["documents"]))


class AuditHookTests(unittest.TestCase):
    """A fixture producer and its Python child are observed and judged."""

    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.root = Path(self.enterContext(tempfile.TemporaryDirectory(dir=SCRATCH))).resolve()
        _write(self.root, "src/in/declared.txt", "declared\n")
        _write(self.root, "other/undeclared.txt", "undeclared\n")
        _write(self.root, "other/child.txt", "child\n")
        _write(self.root, "scripts/producer.py", '''
            import argparse, json, os, subprocess, sys
            from pathlib import Path
            parser = argparse.ArgumentParser(); parser.add_argument("--out"); parser.add_argument("--strip", action="store_true")
            args = parser.parse_args()
            root = Path(__file__).resolve().parents[1]
            values = [(root / "src/in/declared.txt").read_text(), (root / "other/undeclared.txt").read_text()]
            environment = {"PATH": os.environ["PATH"]} if args.strip else None
            subprocess.run([sys.executable, "-c", "print(open('other/child.txt').read())"], cwd=root, env=environment, check=True)
            (Path(args.out) / "bibles.json").write_text(json.dumps(values))
        ''')
        self.recipe = recipes._recipe("probe", "bibles.json", ["scripts/producer.py"], ["src/in"], delivery="browser-data")
        self.enterContext(patch.object(recipes, "RECIPES", (self.recipe,)))
        self.enterContext(patch.object(products, "_recipes", side_effect=lambda: [copy.deepcopy(self.recipe)]))

    def test_reads_outside_the_key_fail_including_a_python_child(self):
        report = inputs.audit(self.root)["probe"]
        self.assertFalse(report["ok"])
        self.assertEqual(report["outside"], ["other/child.txt", "other/undeclared.txt"])
        self.assertTrue(report["where"]["other/undeclared.txt"].endswith("scripts/producer.py:6"))
        self.assertIn("src/in/declared.txt", report["opened_paths"])
        self.assertIn("scripts/producer.py", report["opened_paths"])
        self.assertEqual(report["unaudited_children"], [])

    def test_declared_reads_pass(self):
        self.recipe["input_files"] = ["other/child.txt", "other/undeclared.txt"]
        report = inputs.audit(self.root)["probe"]
        self.assertTrue(report["ok"], report)

    def test_a_python_child_that_drops_the_audit_environment_fails(self):
        self.recipe["argv"] = ["scripts/producer.py", "--strip"]
        self.recipe["input_files"] = ["other/child.txt", "other/undeclared.txt"]
        report = inputs.audit(self.root)["probe"]
        self.assertFalse(report["ok"])
        self.assertEqual(len(report["unaudited_children"]), 1)


class ExcludedPathAuditTests(unittest.TestCase):
    """An excluded path is keyed by name only; the audit holds producers to that."""

    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.root = Path(self.enterContext(tempfile.TemporaryDirectory(dir=SCRATCH))).resolve()
        _write(self.root, "src/in/declared.txt", "declared\n")
        _write(self.root, "src/in/review.toml", "review\n")
        _write(self.root, "src/in/archive/run/record.json", "{}\n")
        _write(self.root, "scripts/producer.py", '''
            import argparse, json, os
            from pathlib import Path
            parser = argparse.ArgumentParser(); parser.add_argument("--out"); parser.add_argument("--mode")
            args = parser.parse_args()
            source = Path(__file__).resolve().parents[1] / "src/in"
            values = [(source / "declared.txt").read_text(), sorted(os.listdir(source)),
                      (source / "review.toml").is_file(), (source / "archive").is_dir()]
            if args.mode == "open-file":
                values.append((source / "review.toml").read_text())
            elif args.mode == "list-directory":
                values.append(os.listdir(source / "archive"))
            elif args.mode == "probe-beneath":
                values.append((source / "archive/run/record.json").exists())
            (Path(args.out) / "bibles.json").write_text(json.dumps(values))
        ''')
        self.recipe = recipes._recipe("probe", "bibles.json", ["scripts/producer.py"], ["src/in"],
                                      excludes=["src/in/archive", "src/in/review.toml"], delivery="browser-data")
        self.enterContext(patch.object(recipes, "RECIPES", (self.recipe,)))
        self.enterContext(patch.object(products, "_recipes", side_effect=lambda: [copy.deepcopy(self.recipe)]))

    def audit(self, mode=None):
        if mode is not None:
            self.recipe["argv"] = ["scripts/producer.py", "--mode", mode]
        return inputs.audit(self.root)["probe"]

    def test_listing_the_parent_and_probing_the_excluded_path_itself_pass(self):
        report = self.audit()
        self.assertTrue(report["ok"], report)
        self.assertIn("src/in/review.toml", report["probed_paths"])
        self.assertIn("src/in", report["listed_paths"])

    def test_opening_an_excluded_file_fails(self):
        report = self.audit("open-file")
        self.assertFalse(report["ok"])
        self.assertEqual(report["outside"], ["src/in/review.toml"])

    def test_listing_an_excluded_directory_fails(self):
        report = self.audit("list-directory")
        self.assertFalse(report["ok"])
        self.assertEqual(report["listed_outside"], ["src/in/archive"])

    def test_probing_beneath_an_excluded_directory_fails(self):
        report = self.audit("probe-beneath")
        self.assertFalse(report["ok"])
        self.assertEqual(report["outside"], ["src/in/archive/run/record.json"])

    def test_excluded_root_is_the_declared_path_and_never_a_name_prefix(self):
        excludes = ("src/in/archive", "src/in/review.toml")
        self.assertEqual(inputs.excluded_root("src/in/archive", excludes), "src/in/archive")
        self.assertEqual(inputs.excluded_root("src/in/archive/run/record.json", excludes), "src/in/archive")
        self.assertEqual(inputs.excluded_root("src/in/review.toml", excludes), "src/in/review.toml")
        for name in ("src/in/archive-neighbor/x", "src/in/review.toml.bak", "src/in", "src/in/declared.txt"):
            self.assertIsNone(inputs.excluded_root(name, excludes), name)
        self.assertIsNone(inputs.excluded_root("src/in/archive", ()))
        # `**` spans whole segments and stops at the shallowest match.
        deep = ("src/p/**/evaluations",)
        self.assertEqual(inputs.excluded_root("src/p/evaluations", deep), "src/p/evaluations")
        self.assertEqual(inputs.excluded_root("src/p/a/b/evaluations/run/evaluations/x", deep), "src/p/a/b/evaluations")
        for name in ("src/p/a/evaluations-old/x", "src/q/a/evaluations/x", "src/p/a/my-evaluations/x"):
            self.assertIsNone(inputs.excluded_root(name, deep), name)


@unittest.skipUnless(os.environ.get("TRIPTYCH_BROWSER_PRODUCT_AUDIT") == "1",
                     "set TRIPTYCH_BROWSER_PRODUCT_AUDIT=1 to run every real producer cold (about ten minutes)")
class FullAuditTests(unittest.TestCase):
    def test_every_family_reads_only_its_key(self):
        report = inputs.audit(ROOT)
        self.assertEqual(len(report), 13)
        failures = {family: {key: result[key] for key in ("outside", "non_canonical", "unaudited_children")}
                    for family, result in report.items() if not result["ok"]}
        self.assertEqual(failures, {}, json.dumps(failures, indent=1)[:4000])


if __name__ == "__main__":
    unittest.main()
