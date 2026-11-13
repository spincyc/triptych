"""Cold producer boundaries: selected source families, no installed baseline."""
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _browser_product_recipes as recipes
import _browser_products as products

SCRATCH = ROOT / ".scratch/browser-product-recipe-tests"


class RecipeTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)

    def test_twelve_public_data_recipes_and_one_site_build_recipe(self):
        actual = products._recipes()
        self.assertEqual(len(actual), 13)
        deliveries = {recipe["id"]: recipe["delivery"] for recipe in actual}
        # Web readers are read while the site is assembled, never published as data.
        self.assertEqual(deliveries.pop("web-editions"), "site-build")
        self.assertEqual(set(deliveries.values()), {"browser-data"})
        self.assertFalse(any(prefix.startswith("print") for recipe in actual for prefix in recipe["output_prefixes"]))

    def test_web_editions_recipe_converts_every_reader_from_canonical_sources(self):
        recipe = next(recipe for recipe in products._recipes() if recipe["id"] == "web-editions")
        self.assertEqual(recipe["argv"], ["tools/web-edition", "products"])
        self.assertEqual(recipe["output_prefixes"], ["web-editions"])
        self.assertEqual(recipe["input_trees"], ["src", "release/publications"])

    def test_review_records_are_excluded_and_calendar_and_bible_scopes_are_narrow(self):
        # Audited 2026-11-12: no producer opens these records, and these
        # families read nothing outside the narrowed trees.
        actual = {recipe["id"]: recipe for recipe in products._recipes()}
        self.assertEqual(actual["bibles"]["input_trees"], ["src/sources/bibles"])
        self.assertEqual(actual["calendar"]["input_trees"], ["src/sources/calendars"])
        self.assertEqual(actual["rubrics"]["input_trees"], ["src/sources/calendars"])
        self.assertEqual(recipes._REVIEW_RECORDS, [
            "src/sources/inventories/classification-review-v1.toml",
            "src/sources/inventories/claude-classification-review-v1.toml",
            "src/sources/inventories/claude-publications-v1.toml",
            "src/sources/inventories/publications-v1.toml",
            "src/sources/inventories/source-family-migration-v1.toml",
        ])
        inventories = "src/sources/inventories"
        for identifier, recipe in actual.items():
            with self.subTest(family=identifier):
                holds = any(inventories == tree or inventories.startswith(tree + "/") for tree in recipe["input_trees"])
                # Reader lookup metadata is keyed by name alone wherever a tree holds it.
                index = any(recipes._READER_INDEX.startswith(tree + "/") for tree in recipe["input_trees"])
                self.assertEqual(recipe["exclude_paths"],
                                 (recipes._REVIEW_RECORDS if holds else []) + (["src/index"] if index else []))
        self.assertEqual({identifier for identifier, recipe in actual.items() if "src/index" in recipe["exclude_paths"]},
                         {"documents", "web-editions"})

    def test_recipe_factory_requires_delivery_and_runner_expands_out_once(self):
        with self.assertRaises(TypeError):
            recipes._recipe("missing", "missing", ["producer.py"], [])
        selected = next(recipe for recipe in recipes.RECIPES if recipe["id"] == "bibles")
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            out = Path(temporary) / "output"
            with patch.object(recipes.subprocess, "run", return_value=SimpleNamespace(returncode=0)) as run:
                recipes._run(ROOT, out, selected, {})
            command = run.call_args.args[0]
            self.assertEqual(command.count("--out"), 1)
            self.assertEqual(command[command.index("--out") + 1], str(out))
            self.assertNotIn("{out}", command)

    def test_recipe_cannot_emit_another_family_or_raw_asset_files(self):
        for name in ("structure/documents/corpus.json", "bibles.json/font.woff2"):
            def wrong(root, out, recipe, environment):
                target = out / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}")
            with self.subTest(name=name), tempfile.TemporaryDirectory(dir=SCRATCH) as temporary, patch.object(recipes, "_run", side_effect=wrong):
                out = Path(temporary) / "output"
                with self.assertRaises(recipes.RecipeError):
                    recipes.generate(ROOT, out, ["bibles"])

    def test_selected_cold_family_has_no_unrequested_products(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            out = Path(temporary) / "data"
            result = recipes.generate(ROOT, out, ["bibles"])
            self.assertEqual(result, {"products": [{"id": "bibles", "files": 1}], "files": 1})
            self.assertEqual([p.relative_to(out).as_posix() for p in out.rglob("*.json")], ["bibles.json"])
            manifest = json.loads((out / "bibles.json").read_bytes())
            self.assertTrue(manifest["bibles"])
            self.assertNotIn("knox", {edition["id"] for edition in manifest["bibles"]})

    def test_independent_passes_cannot_inherit_parser_or_bytecode_caches(self):
        environments = []
        def capture(root, out, recipe, environment):
            environments.append(environment.copy())
            (out / "bibles.json").write_text('{"bibles": []}')
        inherited = {key: "1" for key in (
            "TRIPTYCH_CORPUS_CACHE", "TRIPTYCH_YAML_CACHE",
            "TRIPTYCH_CONTAINMENT_CACHE", "TRIPTYCH_SOURCE_LIBRARY_CACHE",
        )}
        inherited.update(PYTHONPYCACHEPREFIX="old-python-cache", TRIPTYCH_LIBRARY_CACHE_DIR="old-library-cache")
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary, patch.dict(os.environ, inherited), patch.object(recipes, "_run", side_effect=capture):
            for name in ("first", "second"):
                recipes.generate(ROOT, Path(temporary) / name, ["bibles"])
        self.assertEqual(len(environments), 2)
        for environment in environments:
            for name in inherited:
                if name.startswith("TRIPTYCH_") and name.endswith("_CACHE"):
                    self.assertEqual(environment[name], "0")
            self.assertEqual(environment["PYTHONDONTWRITEBYTECODE"], "1")
        for key in ("PYTHONPYCACHEPREFIX", "TRIPTYCH_LIBRARY_CACHE_DIR"):
            self.assertNotEqual(environments[0][key], environments[1][key])
            self.assertNotEqual(environments[0][key], inherited[key])

    def test_families_run_side_by_side_and_report_the_first_failure_in_recipe_order(self):
        import threading
        import time
        table = tuple(recipes._recipe(name, f"structure/{name}", [f"scripts/{name}.py"], ["src/sources"],
                                      delivery="browser-data") for name in ("first", "second", "third"))
        both = threading.Barrier(3, timeout=30)
        def concurrent(root, out, recipe, environment):
            both.wait()  # would time out if the families ran one after another
            (out / "structure" / recipe["id"]).mkdir(parents=True)
            (out / "structure" / recipe["id"] / "index.json").write_text('{"id": "%s"}' % recipe["id"])
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary, patch.object(recipes, "RECIPES", table), \
             patch.object(recipes, "_run", side_effect=concurrent):
            result = recipes.generate(ROOT, Path(temporary) / "data")
            self.assertEqual([item["id"] for item in result["products"]], ["first", "second", "third"])
        def failing(root, out, recipe, environment):
            if recipe["id"] == "second":
                time.sleep(0.5)  # fails last in time, first in recipe order
                raise recipes.RecipeError("second failed")
            if recipe["id"] == "third":
                raise recipes.RecipeError("third failed")
            (out / "structure/first").mkdir(parents=True)
            (out / "structure/first/index.json").write_text("{}")
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary, patch.object(recipes, "RECIPES", table), \
             patch.object(recipes, "_run", side_effect=failing):
            with self.assertRaisesRegex(recipes.RecipeError, "second failed"):
                recipes.generate(ROOT, Path(temporary) / "data")

    def test_a_wrong_family_output_cannot_enter_staging(self):
        def wrong(root, out, recipe, environment):
            (out / "unowned.json").write_text("{}")
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary, patch.object(recipes, "_run", side_effect=wrong):
            out = Path(temporary) / "data"
            with self.assertRaisesRegex(recipes.RecipeError, "outside its owned paths"):
                recipes.generate(ROOT, out, ["bibles"])
            self.assertEqual(list(out.iterdir()), [])

    def test_cold_subprocess_refuses_originals_and_accepts_attested_metadata(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            root = Path(temporary)
            release = root / "release/papal-documents"
            originals = release / "inputs"
            originals.mkdir(parents=True)
            (originals / "snapshot.json").write_text('{"historical": true}')
            (release / "input-records.json").write_text('{"attested": true}')
            (release / "input-delivery.json").write_text('{"sha256": "recorded"}')
            script = root / "producer.py"
            prefix = (
                "from pathlib import Path\nimport argparse, json, os\n"
                "parser = argparse.ArgumentParser(); parser.add_argument('--out'); args = parser.parse_args()\n"
                "root = Path(__file__).parent\n"
            )
            recipe = recipes._recipe("probe", "bibles.json", ["producer.py"], [], delivery="browser-data")
            for label, body in (
                ("path", "(root / 'release/papal-documents/inputs/snapshot.json').read_bytes()\n"),
                ("descriptor", "parent = os.open(root / 'release/papal-documents', os.O_RDONLY | os.O_DIRECTORY)\nos.open('inputs/snapshot.json', os.O_RDONLY, dir_fd=parent)\n"),
            ):
                script.write_text(prefix + body)
                with patch.object(recipes, "RECIPES", (recipe,)):
                    with self.assertRaisesRegex(recipes.RecipeError, "may not open historical input originals"):
                        recipes.generate(root, root / ("denied-" + label), ["probe"])
            script.write_text(prefix +
                "record = json.loads((root / 'release/papal-documents/input-records.json').read_bytes())\n"
                "record['delivery'] = json.loads((root / 'release/papal-documents/input-delivery.json').read_bytes())\n"
                "out = Path(args.out); (out / 'bibles.json').write_text(json.dumps(record))\n")
            with patch.object(recipes, "RECIPES", (recipe,)):
                result = recipes.generate(root, root / "allowed", ["probe"])
            self.assertEqual(result["files"], 1)
            self.assertEqual(json.loads((root / "allowed/bibles.json").read_bytes()),
                             {"attested": True, "delivery": {"sha256": "recorded"}})

    def test_unknown_family_is_refused_before_any_output_is_created(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            out = Path(temporary) / "data"
            with self.assertRaisesRegex(recipes.RecipeError, "unknown browser product"):
                recipes.generate(ROOT, out, ["unregistered"])
            self.assertFalse(out.exists())

    def test_old_source_projection_is_never_a_cold_output(self):
        with self.assertRaisesRegex(recipes.RecipeError, "separate unsealed staging"):
            recipes.generate(ROOT, ROOT / "src/web/data", ["bibles"])

    def test_default_writer_refuses_the_sealed_cache_root(self):
        loader = importlib.machinery.SourceFileLoader("recipe_test_document_library", str(ROOT / "tools/document-library"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        tool = importlib.util.module_from_spec(spec)
        loader.exec_module(tool)
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            cache = Path(temporary) / "sealed"
            with patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": str(cache)}):
                with self.assertRaisesRegex(products.ProductError, "sealed browser product cache"):
                    tool.run_structure(SimpleNamespace(provider="claude", sort="leaf", out=str(cache), check=False))
            self.assertFalse(cache.exists())

    def test_default_working_root_follows_cache_override_but_is_separate(self):
        with patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": ".scratch/browser-data"}):
            self.assertEqual(products.working_data_root(ROOT), ROOT / ".scratch/browser-data-work")

    def test_explicit_working_output_check_never_looks_up_a_sealed_descriptor(self):
        loader = importlib.machinery.SourceFileLoader("explicit_working_catalogue", str(ROOT / "tools/document-library"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        tool = importlib.util.module_from_spec(spec)
        loader.exec_module(tool)
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            work = Path(temporary) / "working"
            arguments = SimpleNamespace(provider="claude", sort="leaf", out=str(work), check=False)
            with patch.object(tool, "working_data_root", return_value=work), patch.object(
                tool, "committed_data_root", side_effect=AssertionError("unexpected descriptor lookup")
            ):
                tool.run_structure(arguments)
                arguments.check = True
                self.assertEqual(tool.run_structure(arguments)["status"], "ok")


class CatenaCommandCacheTests(unittest.TestCase):
    def setUp(self):
        import _catena
        self.catena = _catena
        SCRATCH.mkdir(parents=True, exist_ok=True)

    def test_exact_bytes_are_parsed_once_and_changed_bytes_reparse(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            path = Path(temporary) / "source.yaml"
            path.write_text("value: first\n")
            original = path.stat()
            parser = self.catena._yaml().safe_load
            @self.catena._command_yaml
            def derive():
                first = self.catena._load_yaml(path)
                repeated = self.catena._load_yaml(path)
                path.write_text("value: later\n")
                os.utime(path, ns=(original.st_atime_ns, original.st_mtime_ns))
                changed = self.catena._load_yaml(path)
                return first, repeated, changed
            with patch.object(self.catena._yaml(), "safe_load", wraps=parser) as parse:
                first, repeated, changed = derive()
            self.assertIsNot(first, repeated)
            self.assertEqual(first, {"value": "first"})
            self.assertEqual(changed, {"value": "later"})
            self.assertEqual(parse.call_count, 2)

    def test_a_callers_mutation_cannot_change_the_next_source_read(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            path = Path(temporary) / "source.yaml"
            path.write_text("rows:\n  - title: original\n")
            @self.catena._command_yaml
            def derive():
                first = self.catena._load_yaml(path)
                first["rows"][0]["title"] = "mutated"
                first["rows"].append({"title": "invented"})
                return self.catena._load_yaml(path)
            self.assertEqual(derive(), {"rows": [{"title": "original"}]})

    def test_each_derivation_and_failure_release_their_parsed_sources(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            path = Path(temporary) / "source.yaml"
            path.write_text("value: first\n")
            @self.catena._command_yaml
            def derive(fail=False):
                result = self.catena._load_yaml(path)
                if fail:
                    raise RuntimeError("stopped derivation")
                return result
            self.assertIsNot(derive(), derive())
            with self.assertRaisesRegex(RuntimeError, "stopped derivation"):
                derive(True)
            self.assertIsNone(self.catena._COMMAND_YAML.get())


if __name__ == "__main__":
    unittest.main()
