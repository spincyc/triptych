"""Execute proper-study recipes in isolated fixtures, never production runs."""
from __future__ import annotations

import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from _workflow import WorkflowEngine, WorkflowError

DOCUMENT = "liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost"
FIXTURE_RUN = "0000000000000001"


class IsolatedRecipeTests(unittest.TestCase):
    def setUp(self):
        parent = ROOT / "build/test-tmp"
        parent.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="proper-study-recipes-", dir=parent)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name in ("tools/tpt", "tools/web-edition", "tools/pdf-review", "tmt.json",
                     "scripts/_tooling.py", "scripts/_corpus.py", "scripts/_workflow.py",
                     "scripts/_proper_study.py", "scripts/_proper_components.py", "scripts/_markdown_render.py",
                     "scripts/web-shim.tex"):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)
        self.environment = os.environ.copy()
        for name in tuple(self.environment):
            if name.startswith("TRIPTYCH_PDF_REVIEW_"):
                del self.environment[name]
        temporary_root = self.root / "build/tmp"
        temporary_root.mkdir(parents=True)
        for name in ("TMPDIR", "TMP", "TEMP"):
            self.environment[name] = str(temporary_root)

    def require_tools(self, *names):
        missing = [name for name in names if shutil.which(name) is None]
        if missing:
            self.skipTest("real recipe smoke requires " + ", ".join(missing))

    def command(self, fragment, prefix, *, provider="gpt"):
        lines = (ROOT / "workflows/fragments/proper-study" / fragment).read_text().splitlines()
        recipe = next(line.strip() for line in lines if line.strip().startswith(prefix))
        recipe = recipe.replace("{provider}", provider).replace("{proper}", DOCUMENT)
        recipe = recipe.replace("<run-id>", FIXTURE_RUN).replace("<iteration>", "0")
        return shlex.split(recipe)

    def execute(self, arguments):
        result = subprocess.run(arguments, cwd=self.root, env=self.environment,
                                capture_output=True, text=True, timeout=180)
        self.assertEqual(result.returncode, 0,
                         f"{shlex.join(arguments)}\n{result.stdout}\n{result.stderr}")
        return result

    def test_real_conversion_lands_at_snapshot_path_once_per_provider(self):
        self.require_tools("pandoc")
        for provider in ("gpt", "claude"):
            with self.subTest(provider=provider):
                leaf = self.root / "src" / provider / DOCUMENT
                leaf.mkdir(parents=True)
                (leaf / "main.tex").write_text(
                    "\\documentclass{article}\n"
                    "\\hypersetup{pdftitle={Command recipe fixture}}\n"
                    "\\begin{document}\n\\section{Collect and Readings}\n"
                    "The fixture preserves the Collect and the reading in one paragraph.\n"
                    "\\AIDocumentRevisionTimestamp{2026-09-20T00:00:00Z}\n"
                    "\\end{document}\n")
                converted = self.execute(self.command("generate-web.md", "tools/tpt web-edition", provider=provider))
                expected = self.root / "build/web" / provider / f"{DOCUMENT}.md"
                self.assertTrue(expected.is_file(), converted.stdout)
                self.assertFalse((self.root / "build/web" / provider / provider).exists())
                self.assertIn("The fixture preserves the Collect", expected.read_text())
                self.execute(self.command("generate-web.md", "python3 scripts/_proper_study.py snapshot-web", provider=provider))
                receipt = json.loads((leaf / "research/web-artifact.json").read_text())
                self.assertEqual(receipt["web"], expected.relative_to(self.root).as_posix())
                self.assertEqual(receipt["sha256"], hashlib.sha256(expected.read_bytes()).hexdigest())
                self.assertFalse((self.root / "web").exists(), "recipe must not install a web edition")

    def test_real_renderer_replaces_only_its_child_and_preserves_sibling_evidence(self):
        self.require_tools("pdflatex", "pdftoppm", "magick", "kpsewhich")
        fixture = self.root / "build/tiny.tex"
        fixture.write_text("\\documentclass{article}\n\\begin{document}\n"
                           "One page for the command recipe regression.\n\\end{document}\n")
        self.execute(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                      "-output-directory=build", str(fixture)])
        for suffix in ("", "-synthesis", "-homily"):
            target = self.root / "build/gpt" / f"{DOCUMENT}{suffix}.pdf"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.root / "build/tiny.pdf", target)
        artifacts = self.root / "build/tpt-runs" / FIXTURE_RUN / "artifacts"
        artifacts.mkdir(parents=True)
        sentinel = artifacts / "author-proof.json"
        sentinel.write_bytes(b'{"fixture_evidence":"must survive raster replacement"}\n')
        before = sentinel.read_bytes()
        command = self.command("build-artifacts.md", "tools/tpt pdf-review")
        destination = self.root / command[command.index("--output") + 1]
        command.extend(["--jobs", "1", "--cache", "build/recipe-review-cache"])
        self.execute(command)
        self.assertTrue(sentinel.is_file(), "renderer replaced the shared evidence namespace")
        self.assertEqual(sentinel.read_bytes(), before)
        self.assertEqual(destination, artifacts / "build-artifacts-0/rasters")
        manifest = json.loads((destination / "review-run.json").read_text())
        self.assertEqual(len(manifest["pdfs"]), 3)
        pages = list(destination.rglob("pages/page-*.png"))
        sheets = list(destination.rglob("contact-sheets/sheet-*.png"))
        self.assertEqual(len(pages), 3)
        self.assertEqual(len(sheets), 3)
        self.assertTrue(all(path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n") for path in pages + sheets))
        stale = destination / "obsolete-raster-marker.txt"
        stale.write_text("Must disappear on replacement, unlike sibling evidence.")
        self.execute(command)
        self.assertFalse(stale.exists())
        self.assertEqual(sentinel.read_bytes(), before)

    def test_version_change_preserves_terminal_integrity_not_active_recompilation(self):
        workflows = self.root / "workflows"
        (workflows / "pipelines").mkdir(parents=True)
        (workflows / "fragments/fixture").mkdir(parents=True)
        (workflows / "fragments/fixture/author.md").write_text("Fixture only; no production deliverable.\n")
        (workflows / "schema").mkdir()
        for name in ("worker-result.json", "gate-result.json"):
            shutil.copy2(ROOT / "workflows/schema" / name, workflows / "schema" / name)
        pipeline = {"id": "recipe-history-fixture", "version": 1,
                    "document_argument": "doc", "document_root": "src/gpt/{doc}",
                    "argument_schema": {"doc": {"type": "string", "required": True}},
                    "stages": [
                        {"id": "author", "type": "linear", "execution": {"mode": "single"},
                         "fragments": ["fixture/author.md"], "next": "finish"},
                        {"id": "finish", "type": "gate", "execution": {"mode": "program"},
                         "checks": [{"id": "fixture", "command": "true"}],
                         "max_iterations": 1, "pass_transition": "ACCEPTED", "fail_transition": "BLOCKED"}]}
        definition = workflows / "pipelines/recipe-history-fixture.json"
        definition.write_text(json.dumps(pipeline))
        v1 = definition.read_bytes()
        engine = WorkflowEngine(self.root, workflows)
        engine.standing_findings_root = None
        with patch.object(engine, "get_repo_commit", return_value="a" * 40):
            run_id = engine.seed(pipeline["id"], {"doc": "fixture"})["run_id"]
        self.assertTrue(engine.replay(run_id)["deterministic"])
        pipeline["version"] = 2
        definition.write_text(json.dumps(pipeline))
        with self.assertRaisesRegex(WorkflowError, "seeded against .* v1"):
            engine.replay(run_id)
        definition.write_bytes(v1)
        result = self.root / "fixture-result.json"
        result.write_text(json.dumps({"stage": "author", "iteration": 0, "disposition": "PASS",
                                      "summary": "Synthetic engine test only; no publication evidence."}))
        engine.advance(run_id, result_path=str(result))
        engine.advance(run_id, run_gate=True)
        before = {path.relative_to(engine.run_dir(run_id)): path.read_bytes()
                  for path in engine.run_dir(run_id).rglob("*") if path.is_file()}
        terminal_v1 = engine.replay(run_id)
        self.assertIsNone(terminal_v1["deterministic"])
        self.assertIsNone(terminal_v1["recompiled_hash"])
        definition.write_text(json.dumps(pipeline))
        engine.verify_document(run_id, "fixture")
        self.assertEqual(engine.status(run_id)["workflow_version"], 1)
        self.assertEqual(engine.status(run_id)["disposition"], "ACCEPTED")
        self.assertEqual(engine.replay(run_id), terminal_v1)
        self.assertTrue(terminal_v1["recorded_file_intact"])
        after = {path.relative_to(engine.run_dir(run_id)): path.read_bytes()
                 for path in engine.run_dir(run_id).rglob("*") if path.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
