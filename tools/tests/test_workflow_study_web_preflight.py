"""The real converter refuses an unrenderable study before its cold review."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from _workflow import WorkflowEngine

DOCUMENT = "liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost"
CHECK = "study-web-conversion"


@unittest.skipUnless(shutil.which("pandoc"), "pandoc is not installed")
class StudyWebPreflightTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for directory in ("scripts", "src/common", "workflows/fragments", "workflows/schema"):
            shutil.copytree(ROOT / directory, self.root / directory,
                            ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("tools/tpt", "tools/web-edition", "tmt.json",
                     "requirements-public-alpha.txt", "workflows/pipelines/proper-study.json"):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)

        path = self.root / "workflows/pipelines/proper-study.json"
        pipeline = json.loads(path.read_text())
        self.assertGreaterEqual(pipeline["version"], 11)
        pipeline["document_discovery"].pop("validator")
        self.stages = {stage["id"]: stage for stage in pipeline["stages"]}
        gate = self.stages["study-preflight"]
        self.assertEqual(gate["fail_transition"], "author-study")
        self.assertEqual(gate["pass_transition"], "study-review")
        self.assertIn(CHECK, {check["id"] for check in gate["checks"]})
        # This fixture owns converter behavior and native routing, not source
        # scholarship, PDF production or review seals. Other checks are stubs;
        # the new gate command is copied verbatim from the production pipeline.
        for stage in pipeline["stages"]:
            if "review_input_command" in stage:
                stage["review_input_command"] = "printf '%s\\n' '{\"fixture\": true}'"
            for check in stage.get("checks", []):
                if stage["id"] != "study-preflight" or check["id"] != CHECK:
                    check["command"] = "true"
        path.write_text(json.dumps(pipeline))

        self.leaf = self.root / "src/gpt" / DOCUMENT
        (self.leaf / "sections").mkdir(parents=True)
        (self.leaf / "proper-components.toml").write_text(
            'schema = 2\nformat_contract = "propers-format-v1"\n'
            'element_keys = ["collect"]\n'
            'synthesis_entrypoint = "synthesis.tex"\nhomily_entrypoint = "homily.tex"\n'
            '[[components]]\nkey = "texts"\npath = "sections/texts.tex"\n'
            'modes = ["research"]\n'
            '[[components]]\nkey = "concise"\npath = "sections/concise.tex"\n'
            'modes = ["synthesis"]\n'
            '[[components]]\nkey = "spoken"\npath = "sections/spoken.tex"\n'
            'modes = ["homily"]\n')
        (self.leaf / "main.tex").write_text(
            "\\input{common/preamble}\n\\input{common/propers-format}\n"
            "\\hypersetup{pdftitle={Study},pdfsubject={Synthetic conversion proof}}\n"
            "\\begin{document}\n"
            f"\\input{{{DOCUMENT}/sections/texts}}\n"
            f"\\input{{{DOCUMENT}/generation-metadata}}\n"
            "\\end{document}\n")
        (self.leaf / "generation-metadata.tex").write_text(
            "\\AIDocumentRevisionTimestamp{2026-10-13T12:00:00Z}\n"
            "\\AIModelContribution{test-model}{effort=high}{Test CLI 1.0}\n")
        self.write_source(r"\section{Collect}\label{proper-collect} Appointed prayer.")
        self.engine = WorkflowEngine(self.root, self.root / "workflows")
        self.engine.standing_findings_root = None
        with patch.object(self.engine, "get_repo_commit", return_value="a" * 40):
            self.run_id = self.engine.seed("proper-study", {
                "proper": DOCUMENT, "provider": "gpt"})["run_id"]
        self.drive_to_preflight()

    def write_source(self, body):
        (self.leaf / "sections/texts.tex").write_text(body + "\n")

    def drive_to_preflight(self):
        for _ in range(15):
            state = self.engine.load_state(self.run_id)
            stage = state["current_stage"]
            if stage == "study-preflight":
                return
            self.assertNotIn(stage, ("study-review", "BLOCKED", "ACCEPTED"))
            if self.stages[stage]["type"] == "gate":
                self.engine.advance(self.run_id, run_gate=True)
                continue
            body = {"stage": stage, "iteration": state["packet_hashes"][-1]["iteration"],
                    "disposition": "PASS", "summary": "Synthetic fixture result."}
            if self.stages[stage]["type"] == "evaluator":
                body["findings"] = []
            forwarded = state.get("findings_forwarded_ids", {}).get(stage, [])
            if forwarded:
                body["finding_dispositions"] = [
                    {"id": value, "outcome": "repaired"} for value in forwarded]
            path = self.root / "result.json"
            path.write_text(json.dumps(body))
            self.engine.advance(self.run_id, result_path=str(path))
        self.fail("fixture did not reach study preflight")

    def probe(self):
        return self.engine.advance(self.run_id, run_gate=True)

    def log(self, iteration=0):
        return (self.engine.run_dir(self.run_id) / "gate-logs" /
                f"study-preflight-{iteration:04d}-{CHECK}.log").read_text()

    def output(self):
        return (self.engine.run_dir(self.run_id) / "artifacts/study-web-probe/gpt" /
                f"{DOCUMENT}.md")

    def assert_refused(self, diagnostic):
        out = self.probe()
        self.assertEqual(out["stage"], "author-study")
        self.assertIn(diagnostic, self.log())
        state = self.engine.load_state(self.run_id)
        self.assertFalse(any(packet["stage"] == "study-review"
                             for packet in state["packet_hashes"]))
        self.assertIn("GATE-STUDY-WEB-CONVERSION",
                      state["findings_forwarded_ids"]["author-study"])

    def test_valid_research_converts_before_future_companions_exist(self):
        for name in ("synthesis.tex", "homily.tex", "sections/concise.tex", "sections/spoken.tex"):
            self.assertFalse((self.leaf / name).exists())
        self.assertEqual(self.probe()["stage"], "study-review", self.log())
        self.assertIn("proper-collect", self.output().read_text())
        self.assertFalse((self.leaf / "research/web-artifact.json").exists())
        self.assertFalse((self.root / "web").exists())
        self.assertFalse((self.root / "build/web").exists())

    def test_missing_label_returns_to_author_before_review(self):
        self.write_source("\\section{Collect} Prayer.\n% \\label{proper-collect}")
        self.assert_refused("missing schema-2 source proper anchor(s): proper-collect")

    def test_duplicate_label_returns_to_author_before_review(self):
        self.write_source(r"\section{Collect}\label{proper-collect}\label{proper-collect} Prayer.")
        self.assert_refused("duplicate schema-2 source proper anchor(s): proper-collect")

    def test_undeclared_label_returns_to_author_before_review(self):
        self.write_source(r"\section{Collect}\label{proper-collect}\label{proper-other} Prayer.")
        self.assert_refused("undeclared schema-2 source proper anchor(s): proper-other")

    def test_source_label_lost_in_rendering_returns_to_author_before_review(self):
        main = self.leaf / "main.tex"
        main.write_text(main.read_text().replace(
            r"\begin{document}", r"\newcommand{\discard}[1]{}" + "\n" + r"\begin{document}"))
        self.write_source(r"\section{Collect}\discard{\label{proper-collect}} Prayer.")
        self.assert_refused("missing schema-2 rendered proper anchor(s): proper-collect")

    def test_other_conversion_failure_also_returns_to_author(self):
        self.write_source(r"\section{Collect}\label{proper-collect}\unknownsourcecommand{Prayer.}")
        self.assert_refused("unknownsourcecommand")

    def test_wrong_renderer_dependency_is_not_silently_skipped(self):
        lock = self.root / "requirements-public-alpha.txt"
        lock.write_text("Markdown==0.0.0\n")
        self.assert_refused("installed Python Markdown does not match the bound dependency lock")

    def test_stale_probe_output_cannot_make_a_failed_attempt_pass(self):
        self.output().parent.mkdir(parents=True)
        self.output().write_text("An earlier attempt's disposable output.\n")
        self.write_source(r"\section{Collect} Prayer.")
        self.assert_refused("missing schema-2 source proper anchor(s): proper-collect")
        self.assertEqual(self.output().read_text(), "An earlier attempt's disposable output.\n")

    def test_repair_runs_conversion_again_and_keeps_the_failed_attempt_log(self):
        self.write_source(r"\section{Collect} Prayer.")
        self.assert_refused("missing schema-2 source proper anchor(s): proper-collect")
        original_log = self.log()
        self.write_source(r"\section{Collect}\label{proper-collect} Prayer.")
        self.drive_to_preflight()
        self.assertEqual(self.probe()["stage"], "study-review", self.log(1))
        self.assertEqual(self.log(), original_log)
        self.assertIn("exit 0", self.log(1))


if __name__ == "__main__":
    unittest.main()
