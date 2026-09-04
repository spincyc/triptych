#!/usr/bin/env python3
"""Regression coverage for the authoring-to-publication propers rescue."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / "workflows"
PIPELINES = WORKFLOWS / "pipelines"
SCHEMAS = WORKFLOWS / "schema"
PREFLIGHT = ROOT / "tools" / "check-content-preflight"
GENERATION_CHECKER = ROOT / "tools" / "check-generation-metadata"
DOC = (
    "liturgy/roman-rite/1962/propers/temporal/"
    "55-fifteenth-after-pentecost"
)
STAGES = [
    "author-proper",
    "content-preflight",
    "content-evaluation",
    "content-revision",
    "build-artifacts",
    "mechanical-gates",
    "artifact-revision",
    "visual-evaluation",
    "visual-revision",
    "final-acceptance",
    "publish-artifacts",
    "generate-web",
    "web-evaluation",
    "web-revision",
    "install-publication",
    "publication-gates",
    "publication-revision",
]

sys.path.insert(0, str(ROOT / "scripts"))
from _workflow import (  # noqa: E402
    CHANGES_REQUIRED,
    EVALUATOR,
    WorkflowEngine,
    WorkflowError,
    _validate_result,
)


LOADER = importlib.machinery.SourceFileLoader(
    "triptych_proper_finish_generation_checker", str(GENERATION_CHECKER)
)
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {GENERATION_CHECKER}")
CHECKER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


def pipeline(name: str) -> dict:
    return json.loads((PIPELINES / f"{name}.json").read_text(encoding="utf-8"))


def raw_stages(name: str) -> dict[str, str]:
    """Return each stage object's exact source bytes decoded as UTF-8."""
    text = (PIPELINES / f"{name}.json").read_text(encoding="utf-8")
    marker = '"stages": ['
    position = text.index(marker) + len(marker)
    decoder = json.JSONDecoder()
    found: dict[str, str] = {}
    while True:
        while text[position] in " \t\r\n,":
            position += 1
        if text[position] == "]":
            return found
        stage, end = decoder.raw_decode(text, position)
        found[stage["id"]] = text[position:end]
        position = end


class DefinitionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = WorkflowEngine(ROOT, WORKFLOWS)
        self.full = pipeline("proper")
        self.finish = pipeline("proper-finish")

    def test_finish_pipeline_loads_end_to_end(self) -> None:
        loaded = self.engine.load_workflow("proper-finish")
        self.assertEqual(loaded["id"], "proper-finish")
        self.assertEqual(loaded["version"], 1)
        self.assertEqual([stage["id"] for stage in loaded["stages"]], STAGES)

    def test_document_contract_is_copied_verbatim(self) -> None:
        for field in ("document_argument", "document_discovery", "argument_schema"):
            with self.subTest(field=field):
                self.assertEqual(self.finish[field], self.full[field])

    def test_retained_stage_objects_preserve_the_v21_finish_contract(self) -> None:
        original = raw_stages("proper")
        finish = raw_stages("proper-finish")
        self.assertEqual(list(finish), STAGES)
        for stage_id in STAGES:
            if stage_id == "content-evaluation":
                continue
            with self.subTest(stage=stage_id):
                self.assertEqual(finish[stage_id], original[stage_id])

        expected = original["content-evaluation"].replace(
            '"result_schema": "content-evaluation-result.json"',
            '"result_schema": "content-evaluation-finish-result.json"',
        ).replace(
            '        {\n'
            '          "repair_target": "research",\n'
            '          "transition": "research"\n'
            '        },\n'
            '        {\n'
            '          "repair_target": "brief",\n'
            '          "transition": "research-synthesis"\n'
            '        },\n',
            "",
        ).replace(
            '"max_iterations": 4',
            '"max_iterations": 3',
        )
        self.assertEqual(finish["content-evaluation"], expected)

    def test_content_findings_are_authoring_only_and_fail_closed(self) -> None:
        stage = next(
            stage for stage in self.finish["stages"]
            if stage["id"] == "content-evaluation"
        )
        self.assertEqual(stage["repair_routes"], [{
            "repair_target": "authoring",
            "transition": "content-revision",
        }])
        self.assertEqual(stage["result_schema"],
                         "content-evaluation-finish-result.json")
        schema = self.engine.load_schema(stage["result_schema"])
        self.assertEqual(schema["finding_enums"]["repair_target"],
                         ["authoring"])

        research_owned = {
            "stage": "content-evaluation",
            "iteration": 0,
            "disposition": CHANGES_REQUIRED,
            "findings": [{
                "id": "CON-TEST-001",
                "severity": "blocking",
                "location": "research/scope.md",
                "problem": "the evidence is absent",
                "required_result": "run the full workflow",
                "repair_target": "research",
            }],
        }
        with self.assertRaisesRegex(
            WorkflowError, "expected one of: authoring"
        ):
            _validate_result(research_owned, schema, EVALUATOR)

    def test_finish_seed_starts_at_authoring_and_has_a_distinct_run_id(self) -> None:
        runs = Path(tempfile.mkdtemp(
            prefix="tpt-runs-test-proper-finish-", dir=ROOT / "build"
        ))
        self.addCleanup(shutil.rmtree, runs, ignore_errors=True)
        self.engine.runs_dir = runs
        try:
            seeded = self.engine.seed("proper-finish", {
                "proper": DOC,
                "provider": "gpt",
            })
            self.assertEqual(seeded["workflow_id"], "proper-finish")
            self.assertEqual(seeded["workflow_version"], 1)
            self.assertEqual(seeded["stage"], "author-proper")
            packet = (
                self.engine.run_dir(seeded["run_id"])
                / "packets" / "author-proper-0000.txt"
            ).read_text(encoding="utf-8")
            self.assertIn("WORKFLOW: proper-finish v1", packet)
            self.assertIn("STAGE: author-proper", packet)

            commit = self.engine.load_state(seeded["run_id"])["repo_commit"]
            normalized = {"proper": DOC, "provider": "gpt"}
            ordinary = self.engine.compute_run_id(
                "proper", self.full["version"], commit, normalized
            )
            self.assertNotEqual(seeded["run_id"], ordinary)
        finally:
            shutil.rmtree(runs, ignore_errors=True)


class ProvenanceTests(unittest.TestCase):
    DIGEST = "a" * 64
    RUN_ID = "b" * 16
    COMMIT = "c" * 40
    PROVENANCE = (
        rf"\AIGenerationProvenance{{proper-finish}}{{1}}"
        rf"{{{DIGEST}}}{{{RUN_ID}}}{{{COMMIT}}}{{unknown}}"
    )

    def test_provenance_preflight_accepts_the_finish_workflow_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            leaf = root / "src" / "gpt" / DOC
            leaf.mkdir(parents=True)
            (leaf / "generation-metadata.tex").write_text(
                self.PROVENANCE + "\n", encoding="utf-8"
            )
            result = subprocess.run(
                [
                    str(PREFLIGHT), "--root", str(root),
                    "--provider", "gpt", "--document", DOC,
                    "--check", "provenance-matches-run",
                    "--run-workflow", "proper-finish",
                    "--run-workflow-version", "1",
                    "--run-workflow-digest", self.DIGEST,
                    "--run-id", self.RUN_ID,
                    "--run-seed-commit", self.COMMIT,
                ],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("proper-finish v1", result.stdout)

    def test_generation_metadata_accepts_the_finish_workflow_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source_root = Path(temporary) / "src" / "gpt"
            leaf = source_root / DOC
            leaf.mkdir(parents=True)
            (leaf / "main.tex").write_text(
                rf"\input{{{DOC}/generation-metadata}}" + "\n",
                encoding="utf-8",
            )
            (leaf / "generation-metadata.tex").write_text(
                "\n".join((
                    r"\AIDocumentRevisionTimestamp{2026-09-04T04:18:43Z}",
                    self.PROVENANCE,
                    r"\AIModelContribution{GPT-5-based Codex agent}"
                    r"{unexposed: exact model identifier and model qualifiers}"
                    r"{OpenAI Codex agent; API workspace; "
                    r"unexposed: client version and server revision}",
                    "",
                )),
                encoding="utf-8",
            )
            record = CHECKER.audit_document(source_root, DOC)
            self.assertEqual(record.production.workflow_id, "proper-finish")
            self.assertEqual(record.production.workflow_version, "1")

    def test_promised_deliverables_has_no_workflow_id_special_case(self) -> None:
        source = (ROOT / "tools" / "check-promised-deliverables").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("workflow_id", source)
        self.assertNotRegex(source, r"['\"]proper['\"]")


if __name__ == "__main__":
    unittest.main()
