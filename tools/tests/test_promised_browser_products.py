"""Promise evidence keeps its logical identity while products are held verified."""

from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
LOADER = importlib.machinery.SourceFileLoader(
    "promised_browser_products_checker", str(ROOT / "tools/check-promised-deliverables")
)
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)
PRODUCTS = CHECKER._browser_products
LOGICAL_FILE = "src/web/data/structure/demo/index.json"


class PromisedBrowserProductsTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/next-promise-products"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.cache = self.root / ".scratch/cache"
        self.ledger = self.root / "candidate-ledger.toml"
        self.write("src/demo/main.tex", "Canonical promise owner.\n")
        self.write("scripts/_browser_products.py", "Fixture product declaration.\n")
        (self.root / "release").mkdir()
        self.recipes = [{
            "id": "demo", "version": 1, "delivery": "browser-data", "output_prefixes": ["structure/demo"],
            "argv": [["offline", "demo"]], "input_trees": ["src/demo"],
            "input_files": [], "exclude_paths": [],
        }]
        self.enterContext(patch.object(PRODUCTS, "_recipes", side_effect=lambda: copy.deepcopy(self.recipes)))
        self.enterContext(patch.dict(os.environ, {"TRIPTYCH_BROWSER_DATA_ROOT": str(self.cache)}))
        with patch.object(PRODUCTS, "_generate", side_effect=self.generate):
            self.manifest = PRODUCTS.record(self.root)
        self.enterContext(patch.object(CHECKER, "ROOT", self.root))
        self.enterContext(patch.object(CHECKER, "external_pdf_evidence", return_value=(set(), {})))
        self.enterContext(patch.object(PRODUCTS, "_generate", side_effect=AssertionError("no generation during checks")))
        self.enterContext(patch.object(PRODUCTS, "build", side_effect=AssertionError("no build during checks")))
        self.enterContext(patch.object(CHECKER._artifact_store, "urlopen", side_effect=AssertionError("no network")))

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def generate(self, root, out, product_ids=None):
        path = out / "structure/demo/index.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"text": "Exact fixture words."}) + "\n")

    def payload(self):
        return self.cache / self.manifest["products"][0]["key"] / "data/structure/demo/index.json"

    def ledger_text(self, evidence=(LOGICAL_FILE,), *, check="path_exists", status="pass", state="complete"):
        body = (
            'schema_version = 1\n[[deliverables]]\nid = "demo"\nowner = "src/demo"\n'
            f'promise = "Retain the exact evidence."\nstate = "{state}"\n'
            '[[deliverables.requirements]]\nid = "projection"\ncriterion = "Retain the projection."\n'
            f'status = "{status}"\nevidence = {json.dumps(list(evidence))}\ncheck = "{check}"\n'
        )
        if check == "contains":
            body += f'path = "{LOGICAL_FILE}"\nneedle = "Exact fixture words."\n'
        self.ledger.write_text(body)

    def validate(self, required=()):
        return CHECKER.validate(self.ledger, set(required))

    def test_complete_file_directory_and_root_use_one_verified_snapshot(self):
        self.ledger_text((LOGICAL_FILE, "src/web/data/structure/demo", "src/web/data", "src/demo/main.tex"))
        held = []
        original = CHECKER._validate

        def inspect(ledger, required, products):
            held.append(products.data_root)
            self.assertTrue(products.data_root.is_dir())
            self.assertNotEqual(products.data_root, self.root / "src/web/data")
            return original(ledger, required, products)

        with patch.object(CHECKER, "_validate", side_effect=inspect), \
                patch.object(PRODUCTS, "verified_products", wraps=PRODUCTS.verified_products) as verify:
            self.assertEqual([], self.validate(required=["demo"]))
            self.assertEqual(1, verify.call_count)
        self.assertEqual(1, len(held))
        self.assertFalse(held[0].exists())
        self.assertFalse((self.root / "src/web/data").exists())

    def test_contains_reads_the_verified_file_without_a_legacy_tree(self):
        self.ledger_text(check="contains")
        self.assertEqual([], self.validate())
        self.ledger.write_text(self.ledger.read_text().replace('needle = "Exact fixture words."', 'needle = "Absent words."'))
        self.assertIn("required literal is absent", "\n".join(self.validate()))

    def test_undeclared_file_and_directory_cannot_be_supplied_by_old_data(self):
        for relative in ("src/web/data/not-declared.json", "src/web/data/structure/demo-empty"):
            with self.subTest(relative=relative):
                self.write(relative, "Old unverified evidence.\n")
                self.ledger_text((relative,))
                errors = "\n".join(self.validate())
                self.assertIn("missing evidence " + relative, errors)
                self.assertIn("not declared", errors)

    def test_missing_descriptor_never_falls_back_to_old_data(self):
        self.ledger_text()
        self.write(LOGICAL_FILE, "Unverified legacy data.\n")
        (self.root / PRODUCTS.MANIFEST_RELATIVE).unlink()
        self.assertIn("browser products", "\n".join(self.validate()))

    def test_missing_cache_never_builds_or_uses_old_data(self):
        self.ledger_text()
        self.write(LOGICAL_FILE, "Unverified legacy data.\n")
        shutil.rmtree(self.cache)
        self.assertIn("browser products", "\n".join(self.validate()))

    def test_missing_product_file_fails_closed(self):
        self.ledger_text()
        self.payload().unlink()
        self.assertIn("browser products", "\n".join(self.validate()))

    def test_corrupt_product_bytes_fail_closed(self):
        self.ledger_text()
        self.payload().write_bytes(b"?" * self.payload().stat().st_size)
        self.assertIn("browser products", "\n".join(self.validate()))

    def test_extra_product_member_fails_exact_membership(self):
        self.ledger_text()
        self.payload().with_name("undeclared.json").write_text("{}\n")
        self.assertIn("browser products", "\n".join(self.validate()))

    def test_symlink_product_file_fails_closed(self):
        self.ledger_text()
        outside = self.write(".scratch/outside.json", self.payload().read_text())
        self.payload().unlink()
        self.payload().symlink_to(outside)
        self.assertIn("browser products", "\n".join(self.validate()))

    def test_stale_canonical_input_fails_closed(self):
        self.ledger_text()
        self.write("src/demo/main.tex", "Changed canonical owner.\n")
        self.assertIn("inputs changed", "\n".join(self.validate()))

    def test_products_remain_held_until_final_input_revalidation(self):
        self.ledger_text()
        original = CHECKER._validate

        def change_after_evidence(ledger, required, products):
            self.assertEqual([], original(ledger, required, products))
            self.write("src/demo/main.tex", "Changed during the check.\n")
            return []

        with patch.object(CHECKER, "_validate", side_effect=change_after_evidence):
            self.assertIn("inputs changed", "\n".join(self.validate()))

    def test_descriptor_without_regular_owning_module_is_not_a_legacy_fixture(self):
        self.ledger_text()
        module = self.root / "scripts/_browser_products.py"
        module.unlink()
        self.assertIn("require a regular", "\n".join(self.validate()))
        module.symlink_to(self.root / "src/demo/main.tex")
        self.assertIn("require a regular", "\n".join(self.validate()))

    def test_undeclared_sparse_fixture_retains_legacy_evidence_logic(self):
        (self.root / "scripts/_browser_products.py").unlink()
        (self.root / PRODUCTS.MANIFEST_RELATIVE).unlink()
        self.write(LOGICAL_FILE, "Legacy fixture evidence.\n")
        self.ledger_text()
        with patch.object(PRODUCTS, "verified_products", side_effect=AssertionError("no product contract")):
            self.assertEqual([], self.validate())

    def test_valid_products_do_not_complete_open_or_candidate_promises(self):
        self.ledger_text(status="open")
        self.assertIn("complete state has unmet requirements", "\n".join(self.validate()))
        self.ledger_text(state="candidate")
        self.assertIn("completion required", "\n".join(self.validate(required=["demo"])))


if __name__ == "__main__":
    unittest.main()
