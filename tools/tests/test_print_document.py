"""Selected print orchestration preserves owning gates and never installs PDFs."""
from __future__ import annotations

import json
import shutil
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

    def test_request_scratch_roots_keep_auxiliaries_separate(self):
        recipe = self.recipe()
        with patch.dict(printing.os.environ, {}, clear=True):
            default = printing._work_root(self.root, recipe)
        self.assertEqual(default.parent, self.root / ".scratch/print-document")
        first = self.root / ".scratch/request-one"
        second = self.root / ".scratch/request-two"
        with patch.dict(printing.os.environ, {"TRIPTYCH_PRINT_WORK_ROOT": str(first)}):
            first_work = printing._work_root(self.root, recipe)
            _, first_pdf = printing._make_arguments(recipe, first_work)
            first_pdf.parent.mkdir(parents=True)
            first_pdf.with_suffix(".aux").write_text("references from the first request")
        with patch.dict(printing.os.environ, {"TRIPTYCH_PRINT_WORK_ROOT": str(second)}):
            second_work = printing._work_root(self.root, recipe)
            command, second_pdf = printing._make_arguments(recipe, second_work)
        self.assertEqual(first_work.name, second_work.name)
        self.assertTrue(first_pdf.is_relative_to(first))
        self.assertTrue(second_pdf.is_relative_to(second))
        self.assertFalse(second_pdf.with_suffix(".aux").exists())
        self.assertIn("BUILD_ROOT=" + str(second_work / "build/gpt"), command)

    def test_request_scratch_refuses_ambiguous_protected_or_symlink_paths(self):
        protected = self.root / "src/reused-work"
        link = self.root / ".scratch/request-link"
        link.parent.mkdir(parents=True)
        link.symlink_to(self.leaf, target_is_directory=True)
        for value in ("", "relative/job", "/", str(protected), str(link / "job")):
            with self.subTest(value=value), patch.dict(printing.os.environ, {"TRIPTYCH_PRINT_WORK_ROOT": value}):
                with self.assertRaises(printing.PrintError):
                    printing._work_root(self.root, self.recipe())

    def test_papal_selection_plan_uses_request_scratch(self):
        scratch = self.root / ".scratch/papal-request"
        plan = {"schema": "triptych-papal-typeset/v1", "documents": []}

        def make_plan(argv, root):
            filename = next(value.split("=", 1)[1] for value in argv
                            if value.startswith("PAPAL_CURRENT_MANIFEST="))
            target = Path(filename)
            self.assertTrue(target.is_relative_to(scratch))
            target.write_text(json.dumps(plan))

        with patch.dict(printing.os.environ, {"TRIPTYCH_PRINT_WORK_ROOT": str(scratch)}), \
                patch.object(printing, "_run", side_effect=make_plan):
            self.assertEqual(printing._papal_plan(self.root), plan)
        self.assertEqual(list(scratch.iterdir()), [])

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

    def test_batch_checks_preserve_each_selected_dependency_set_and_metadata_gate(self):
        first = self.recipe()
        second = dict(first, id="publication:gpt/articles/faith/second", document="articles/faith/second")
        peer = dict(first, id="publication:claude/articles/faith/example", provider="claude")
        shared = self.root / "src/common"
        shared.mkdir(parents=True)
        (shared / "format.tex").write_text("shared format")
        order_only = self.root / "source-check"
        order_only.write_text("order-only validator")
        selected = [first, peer, second]

        def database(argv, **kwargs):
            lines = [f"{target}: src/common {first['entrypoint']} | source-check"
                     for target in argv if target.endswith(".pdf")]
            return subprocess.CompletedProcess(argv, 1, "\n".join(lines), "")

        with patch.object(printing.subprocess, "run", side_effect=database):
            individual = {recipe["id"]: printing._declared_dependencies(self.root, recipe)
                          for recipe in selected}
        with patch.object(printing.subprocess, "run", side_effect=database) as make, \
                patch.object(printing, "_run") as metadata:
            result = printing.check_many(selected, root=self.root)
        self.assertEqual([recipe["id"] for recipe in result], [recipe["id"] for recipe in selected])
        self.assertEqual({recipe["id"]: recipe["dependencies"] for recipe in result}, individual)
        self.assertEqual(make.call_count, 2)
        for call in make.call_args_list:
            command = call.args[0]
            self.assertIn("-qp", command)
            self.assertNotIn("doc", command)
            documents = next(value for value in command if value.startswith("DOCUMENTS="))
            expected = "DOCUMENTS=articles/faith/example"
            if "PROVIDER=gpt" in command:
                expected += " articles/faith/second"
            self.assertEqual(documents, expected)
        # The gates run side by side, so their call order is not fixed.
        self.assertCountEqual(
            [call.args[0] for call in metadata.call_args_list],
            [printing._tool(self.root, "check-generation-metadata", "--provider", recipe["provider"],
                            "--document", recipe["document"]) for recipe in selected])
        self.assertTrue(all(recipe["status"] == "valid" for recipe in result))
        self.assertTrue(all("source-check" not in recipe["dependencies"] for recipe in result))

    def test_batch_metadata_gates_raise_the_first_failure_in_selection_order(self):
        first = self.recipe()
        selected = [dict(first, id=f"publication:gpt/articles/faith/{name}",
                         document=f"articles/faith/{name}") for name in ("a", "b", "c")]

        def gate(argv, root, **kwargs):
            document = argv[argv.index("--document") + 1]
            if document != "articles/faith/a":
                raise printing.PrintError(f"bad metadata: {document}")
            return ""

        with patch.object(printing, "_run", side_effect=gate) as metadata, \
                patch.object(printing, "_declared_dependencies_many") as dependencies:
            with self.assertRaisesRegex(printing.PrintError, "bad metadata: articles/faith/b"):
                printing.check_many(selected, root=self.root)
        self.assertEqual(metadata.call_count, len(selected))
        dependencies.assert_not_called()

    def test_batch_make_failure_or_absent_target_does_not_return_partial_checks(self):
        recipe = self.recipe()
        for result in (subprocess.CompletedProcess([], 2, "", "bad make graph"),
                       subprocess.CompletedProcess([], 1, "unrelated.pdf: absent.tex", "")):
            with self.subTest(result=result), patch.object(printing, "_run"), \
                    patch.object(printing.subprocess, "run", return_value=result):
                with self.assertRaises(printing.PrintError):
                    printing.check_many([recipe], root=self.root)

    def test_batch_metadata_failure_stops_before_make_discovery(self):
        with patch.object(printing, "_run", side_effect=printing.PrintError("invalid source metadata")), \
                patch.object(printing.subprocess, "run") as make:
            with self.assertRaisesRegex(printing.PrintError, "invalid source metadata"):
                printing.check_many([self.recipe()], root=self.root)
        make.assert_not_called()

    def test_batch_has_no_cross_call_cache_and_keeps_nonpublication_checks(self):
        recipe = self.recipe()
        first = self.root / "src/common/first.tex"
        second = self.root / "src/common/second.tex"
        first.parent.mkdir(parents=True)
        first.write_text("first")
        second.write_text("second")
        _, target = printing._make_arguments(recipe, printing._scratch_root(self.root) / "dependency-query/gpt")
        responses = [subprocess.CompletedProcess([], 1, f"{target}: {value}", "")
                     for value in ("src/common/first.tex", "src/common/second.tex")]
        source = {"family": "bible", "id": "bible:fixture"}
        with patch.object(printing, "_run"), patch.object(printing, "check", return_value=source) as gate, \
                patch.object(printing.subprocess, "run", side_effect=responses) as make:
            one = printing.check_many([recipe, source], root=self.root)
            two = printing.check_many([source, recipe], root=self.root)
        self.assertIn("src/common/first.tex", one[0]["dependencies"])
        self.assertNotIn("src/common/first.tex", two[1]["dependencies"])
        self.assertIn("src/common/second.tex", two[1]["dependencies"])
        self.assertEqual(make.call_count, 2)
        self.assertEqual(gate.call_count, 2)
        self.assertIs(one[1], source)
        self.assertIs(two[0], source)

    def test_batch_rejects_duplicate_publication_identities(self):
        recipe = self.recipe()
        with patch.object(printing, "_run"), patch.object(printing.subprocess, "run") as make:
            with self.assertRaisesRegex(printing.PrintError, "unique document identities"):
                printing.check_many([recipe, recipe], root=self.root)
        make.assert_not_called()

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
                  "mechanical_validation": {"command": ["make", "BUILD_ROOT=" + str(work / "build"),
                                                        "PYTHON=/home/build-user/venv/bin/python"]}}
        with patch.object(printing.sys, "executable", "/home/build-user/venv/bin/python"):
            saved = printing._portable_receipt(result, self.root, work, destination)
        self.assertEqual(saved["mechanical_validation"]["command"][1], "BUILD_ROOT=<print-work>/build")
        self.assertEqual(saved["mechanical_validation"]["command"][2], "PYTHON=<python>")
        result["mechanical_validation"]["command"].pop()
        result["machine_path"] = "/home/unrelated-user/private-font"
        with self.assertRaisesRegex(printing.PrintError, "machine-local path"):
            printing._portable_receipt(result, self.root, work, destination)

    def test_new_papal_withdrawal_after_selection_refuses_export(self):
        recipe = {"document": "papal.before", "language": "la",
                  "_source_row": {"id": "papal.before", "language": "la"}}
        with patch.object(printing, "_papal_plan", return_value={"documents": []}):
            with self.assertRaisesRegex(printing.PrintError, "withdrawn during printing"):
                printing._assert_papal_current(recipe, self.root)


@unittest.skipUnless(shutil.which("pdflatex") and shutil.which("make"), "requires the native TeX toolchain")
class DictionaryGeneratedRootTests(unittest.TestCase):
    def test_make_selects_isolated_generated_body_and_omissions_without_losing_bundle_default(self):
        scratch = printing._scratch_root(ROOT) / "tests"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            root = Path(temporary)
            source = root / "src/gpt"
            source.mkdir(parents=True)
            template_root = ROOT / "src/common/document-types/sanctuary-dictionary-v1"
            template = (template_root / "main.template.tex").read_text()
            definitions = "\n".join(line for line in template.splitlines()
                                    if r"\RSDGeneratedRoot" in line or r"\RSDGeneratedFile" in line)
            definitions += "\n" + (template_root / "omissions/generated.tex").read_text()
            definitions = definitions.replace("@{selection}", "ed-fixture")
            (source / "main.tex").write_text(
                "\\documentclass{article}\n" + definitions + "\n\\begin{document}\n"
                "\\input{\\RSDGeneratedFile}\n\\input{\\RSDOmissionFile}\n\\end{document}\n")
            default = root / "build/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/shared/generated"
            isolated = root / "isolated/generated"
            for directory, marker in ((default, "DEFAULT"), (isolated, "ISOLATED")):
                directory.mkdir(parents=True)
                (directory / "ed-fixture.tex").write_text(f"\\typeout{{{marker}BODY}}Body.\n")
                (directory / "ed-fixture.review-omissions.tex").write_text(f"\\typeout{{{marker}OMISSIONS}}Omissions.\n")

            # Browser bundles retain the original relative virtual build tree.
            default_out = root / "default-output"
            default_out.mkdir()
            result = subprocess.run([shutil.which("pdflatex"), "-halt-on-error", "-interaction=nonstopmode",
                                     "-output-directory=" + str(default_out), "main.tex"],
                                    cwd=source, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout[-3000:])
            self.assertIn("DEFAULTBODY", result.stdout)
            self.assertIn("DEFAULTOMISSIONS", result.stdout)

            # Exercise the production Make compiler macro, with both trees
            # present: an accidental fallback must not silently render stale data.
            make = (ROOT / "Makefile").read_text()
            macro = "define PDFLATEX_TO_FIXED_POINT\n" + make.split(
                "define PDFLATEX_TO_FIXED_POINT\n", 1)[1].split("\nendef", 1)[0] + "\nendef\n"
            assembly = root / "isolated/.assembly/output/selected"
            assembled_entry = assembly / "src/gpt/main.tex"
            assembled_entry.parent.mkdir(parents=True)
            assembled_entry.write_text("\\typeout{ASSEMBLEDENTRY}\n" + (source / "main.tex").read_text())
            (assembly / "entrypoint").write_text(str(assembled_entry) + "\n")
            (root / "Makefile").write_text(
                "SOURCE_ROOT := src/gpt\nPROVIDER := gpt\nBUILD_ROOT := isolated\nPDFLATEX := "
                + shutil.which("pdflatex") + "\n"
                "PDFLATEX_MAX_PASSES := 4\nSHA256 := sha256sum\n"
                "ROMAN_SANCTUARY_DICTIONARY_BUILD_PDFS := isolated/output/selected.pdf\n"
                "ROMAN_SANCTUARY_DICTIONARY_GENERATED := isolated/generated\n" + macro +
                "isolated/output/selected.pdf:\n\t@mkdir -p $(@D)\n"
                "\t@$(call PDFLATEX_TO_FIXED_POINT,selected,main.tex,isolated/output/selected)\n")
            result = subprocess.run([shutil.which("make"), "--no-print-directory", "isolated/output/selected.pdf"],
                                    cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, (result.stdout + result.stderr)[-3000:])
            self.assertIn("ASSEMBLEDENTRY", result.stdout)
            self.assertIn("ISOLATEDBODY", result.stdout)
            self.assertIn("ISOLATEDOMISSIONS", result.stdout)
            self.assertNotIn("DEFAULTBODY", result.stdout)
            self.assertNotIn("DEFAULTOMISSIONS", result.stdout)


if __name__ == "__main__":
    unittest.main()
