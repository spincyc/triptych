"""Selected print orchestration preserves owning gates and never installs PDFs."""
from __future__ import annotations

import json
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _print_document as printing


class RecipeTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/print-document/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        self.leaf = self.root / "src/gpt/articles/faith/example"
        self.leaf.mkdir(parents=True)
        (self.leaf / "main.tex").write_text("\\documentclass{article}\n\\begin{document}Exact words.\\end{document}\n")
        (self.leaf / "generation-metadata.tex").write_text("metadata\n")
        (self.root / "Makefile").write_text("# fixture\n")

    def tearDown(self):
        self.temp.cleanup()

    def recipe(self):
        with patch("_corpus.title_of", side_effect=ValueError("fixture has no title")):
            return printing.publication_recipe("gpt", "articles/faith/example", root=self.root)

    def test_recipe_works_without_installed_pdf_and_offers_no_lossy_html(self):
        recipe = self.recipe()
        self.assertEqual(recipe["entrypoint"], "src/gpt/articles/faith/example/main.tex")
        self.assertEqual(recipe["formats"], ["pdf"])
        self.assertFalse((self.root / "pdf").exists())
        self.assertEqual(recipe["command"][-1], "publication:gpt/articles/faith/example")

    def test_arbitrary_synthesis_file_is_not_a_declared_companion(self):
        (self.leaf / "synthesis.tex").write_text("unregistered companion\n")
        with self.assertRaisesRegex(printing.PrintError, "declared companion"):
            printing.publication_recipe("gpt", "articles/faith/example-synthesis", root=self.root)

    def test_traversal_shell_characters_and_unknown_providers_are_refused(self):
        for identity in ("publication:gpt/../secret", "publication:gpt/a;touch-x", "publication:unknown/foo", "bible:knox"):
            with self.subTest(identity=identity), self.assertRaises(printing.PrintError):
                printing.select(identity, root=self.root)

    def test_selected_make_build_names_one_document_and_no_install(self):
        command, pdf = printing._make_arguments(self.recipe(), self.root / ".scratch/run")
        self.assertEqual(command[2], "doc")
        self.assertIn("DOC=articles/faith/example", command)
        self.assertIn("DOCUMENTS=articles/faith/example", command)
        self.assertNotIn("install", command)
        self.assertTrue(pdf.is_relative_to(self.root / ".scratch/run"))

    def test_declared_graph_is_queried_without_running_recipes(self):
        recipe = self.recipe()
        _, target = printing._make_arguments(recipe, printing._work_root(self.root, recipe))
        source = "src/gpt/articles/faith/example/main.tex"
        result = subprocess.CompletedProcess([], 1, str(target) + ": " + source + " | source-check\n", "")
        with patch.object(printing.subprocess, "run", return_value=result) as run:
            dependencies = printing._declared_dependencies(self.root, recipe)
        self.assertIn("-qp", run.call_args.args[0])
        self.assertIn(source, dependencies)
        self.assertNotIn("source-check", dependencies)

    def test_publication_source_check_is_not_a_pdf_check(self):
        recipe = self.recipe()
        with patch.object(printing, "_run") as run, patch.object(printing, "_declared_dependencies", return_value=recipe["dependencies"]):
            checked = printing.check(recipe, root=self.root)
        self.assertIn("--document", run.call_args.args[0])
        self.assertNotIn("--pdf", run.call_args.args[0])
        self.assertEqual(checked["status"], "valid")

    def test_build_failure_exports_nothing(self):
        recipe = self.recipe()
        destination = self.root / ".scratch/result"
        with patch.object(printing, "check", return_value=recipe), patch.object(printing, "_run", side_effect=printing.PrintError("gate failed")):
            with self.assertRaisesRegex(printing.PrintError, "gate failed"):
                printing.build(recipe, out=destination, root=self.root)
        self.assertFalse(destination.exists())

    def test_selected_success_exports_one_pdf_and_hash_bound_receipt(self):
        recipe = self.recipe()
        destination = self.root / ".scratch/result"
        _, product = printing._make_arguments(recipe, printing._work_root(self.root, recipe))

        def compile_selected(*args, **kwargs):
            product.parent.mkdir(parents=True, exist_ok=True)
            product.write_bytes(b"%PDF-1.4\nselected test bytes\n")
            return ""

        with patch.object(printing, "check", return_value=recipe), patch.object(printing, "_run", side_effect=compile_selected), patch.object(printing, "_render_environment", return_value={"identity_scope": "source-output-attestation"}):
            result = printing.build(recipe, out=destination, root=self.root)
        self.assertEqual(len(list(destination.glob("*.pdf"))), 1)
        self.assertEqual(Path(result["output"]).read_bytes(), product.read_bytes())
        receipt = json.loads(Path(result["receipt"]).read_text())
        self.assertEqual(receipt["output_sha256"], result["output_sha256"])
        self.assertEqual(receipt["review_status"], "generated-unreviewed")
        self.assertEqual(receipt["path_base"], "receipt-directory")
        self.assertEqual(receipt["output"], Path(result["output"]).name)
        self.assertNotIn(str(self.root), Path(result["receipt"]).read_text())
        self.assertTrue(receipt["inputs"])
        self.assertFalse((self.root / "pdf").exists())

    def test_source_changed_during_build_is_not_exported(self):
        recipe = self.recipe()
        _, product = printing._make_arguments(recipe, printing._work_root(self.root, recipe))
        destination = self.root / ".scratch/result"

        def changing_build(*args, **kwargs):
            product.parent.mkdir(parents=True, exist_ok=True)
            product.write_bytes(b"%PDF fixture\n")
            (self.leaf / "main.tex").write_text("changed while building\n")

        with patch.object(printing, "check", return_value=recipe), patch.object(printing, "_run", side_effect=changing_build), patch.object(printing, "_render_environment", return_value={}):
            with self.assertRaisesRegex(printing.PrintError, "changed during printing"):
                printing.build(recipe, out=destination, root=self.root)
        self.assertFalse(destination.exists())

    def test_protected_output_and_symlink_destinations_are_rejected(self):
        for name in ("src/overwrite", "pdf/new", "web/new", "release/new", ".git/new", ".scratch", "build"):
            with self.subTest(name=name), self.assertRaises(printing.PrintError):
                printing._destination(self.root / name, self.root)
        link = self.root / ".scratch/link"
        link.parent.mkdir(exist_ok=True)
        link.symlink_to(self.leaf, target_is_directory=True)
        with self.assertRaises(printing.PrintError):
            printing._destination(link, self.root)

    def test_papal_current_plan_is_resolved_before_selecting_a_reader(self):
        row = {"id": "papal.current", "language": "la", "title": "Current selection",
               "text_path": "src/sources/works/test/text.txt", "rights_basis": "fixture"}
        current = {"schema": "triptych-papal-typeset/v1", "revision": "2026-01-01T00:00:00Z", "documents": [row]}
        with patch.object(printing, "_papal_plan", return_value=current) as planned:
            recipe = printing.select("papal:papal.current/la", root=self.root)
            with self.assertRaisesRegex(printing.PrintError, "current print recipe"):
                printing.select("papal:papal.withdrawn/la", root=self.root)
        self.assertEqual(planned.call_count, 2)
        self.assertEqual(recipe["_source_row"], row)
        self.assertNotIn("_source_row", printing.public_recipe(recipe))

    def test_companion_selection_does_not_apply_to_bibles(self):
        with self.assertRaisesRegex(printing.PrintError, "only to provider"):
            printing.select("bible:douay-rheims", "homily", root=self.root)

    def test_bible_destination_accepts_transient_scratch_but_refuses_source_targets(self):
        loader = SourceFileLoader("_print_test_typeset_bible", str(ROOT / "tools/typeset-bible"))
        spec = spec_from_loader(loader.name, loader)
        bible = module_from_spec(spec)
        sys.modules[spec.name] = bible
        try:
            loader.exec_module(bible)
            with patch.object(bible, "ROOT", self.root), patch.object(bible, "WRITABLE_ROOT", self.root / "build"):
                self.assertEqual(bible.destination(self.root / ".scratch/selected"), self.root / ".scratch/selected")
                self.assertEqual(bible.destination(self.root / "build/selected"), self.root / "build/selected")
                for name in ("src/selected", "pdf/selected", "web/selected", ".scratch/../src/selected"):
                    with self.subTest(name=name), self.assertRaises(ValueError):
                        bible.destination(self.root / name)
                link = self.root / ".scratch/escape"
                link.parent.mkdir(exist_ok=True)
                link.symlink_to(self.root / "src", target_is_directory=True)
                with self.assertRaises(ValueError):
                    bible.destination(link / "selected")
        finally:
            sys.modules.pop(spec.name, None)

    def test_generated_pdf_waits_for_auxiliary_fixed_point(self):
        folder = self.root / ".scratch/settle"
        folder.mkdir(parents=True)
        product = folder / "selected.pdf"
        product.with_suffix(".aux").write_text("old references")
        product.with_suffix(".log").write_text("no warnings")

        def compile_pass(*args, **kwargs):
            product.with_suffix(".aux").write_text("settled references")
            return ""

        with patch.object(printing, "_run", side_effect=compile_pass) as run:
            self.assertEqual(printing._settle_generated_pdf(self.root, product, folder), 2)
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args.args[0][-1], str(product.with_suffix(".tex")))

    def test_persistent_missing_glyph_prevents_generated_pdf_acceptance(self):
        folder = self.root / ".scratch/settle"
        folder.mkdir(parents=True)
        product = folder / "selected.pdf"
        product.with_suffix(".log").write_text("Missing character: no glyph")
        with patch.object(printing, "_run", return_value=""):
            with self.assertRaisesRegex(printing.PrintError, "glyphs did not settle"):
                printing._settle_generated_pdf(self.root, product, folder)

    def test_portable_receipt_redacts_nested_work_paths_and_rejects_other_local_paths(self):
        work = self.root / ".scratch/print-document/job"
        destination = self.root / ".scratch/export"
        result = {"output": str(destination / "selected.pdf"), "receipt": str(destination / "selected.print.json"),
                  "mechanical_validation": {"command": ["make", "BUILD_ROOT=" + str(work / "build")]}}
        saved = printing._portable_receipt(result, self.root, work, destination)
        self.assertEqual(saved["mechanical_validation"]["command"][1], "BUILD_ROOT=<print-work>/build")
        result["machine_path"] = "/home/unrelated-user/private-font"
        with self.assertRaisesRegex(printing.PrintError, "machine-local path"):
            printing._portable_receipt(result, self.root, work, destination)

    def test_new_papal_withdrawal_after_selection_refuses_export(self):
        recipe = {"document": "papal.before", "language": "la",
                  "_source_row": {"id": "papal.before", "language": "la"}}
        with patch.object(printing, "_papal_plan", return_value={"documents": []}):
            with self.assertRaisesRegex(printing.PrintError, "withdrawn during printing"):
                printing._assert_papal_current(recipe, self.root)


if __name__ == "__main__":
    unittest.main()
