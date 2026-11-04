"""Source-first publication keeps substantive gates and exact review identities."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _document_schema as schema
import _proper_study as study
from _workflow import WorkflowError
from tools.tests.test_proper_components_v2 import fixture, save
from tools.tests.test_workflow_proper_study_artifact_routing import EngineFixture

DOCUMENT = "liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost"
CATALOG = "library/traditional-latin-mass.md"
SCRATCH = ROOT / ".scratch/authoring-pipeline"


class SourceFixture(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        data, path, provider = fixture(self.root)
        self.leaf = provider / DOCUMENT
        self.leaf.parent.mkdir(parents=True)
        shutil.move(path.parent, self.leaf)
        data["document"] = DOCUMENT
        for mode, suffix in study.EDITIONS.items():
            data["outputs"][mode] = DOCUMENT + suffix
        data["outputs"]["web"] = DOCUMENT
        for path in self.leaf.glob("*.tex"):
            path.write_text(path.read_text().replace("proper/", DOCUMENT + "/"))
        for name in ("research/context.md", "research/scope.md", "research/interpretations.md",
                     "propers/verified.md", "propers/retrieved.txt"):
            path = self.leaf / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Isolated structural fixture, not production evidence.\n")
        (self.leaf / "research/source-bindings.toml").write_text("bindings = []\n")
        (self.leaf / "research/review-dependencies.toml").write_text("paths = []\n")
        save(data, self.leaf / "proper-components.toml")
        self.declaration = schema.adapter_manifest(self.root, self.leaf)
        self.write_manifest()
        self.catalog = self.root / CATALOG
        self.catalog.parent.mkdir()
        self.catalog.write_text(
            f"<!-- triptych-publication-id: {DOCUMENT} -->\n"
            f"| Example | [Read](../web/gpt/{DOCUMENT}.html) |\n")
        release = self.root / "release/public-alpha.json"
        release.parent.mkdir()
        release.write_text(json.dumps({"provider": "gpt", "authorizations": {"standing": {}}}))
        for suffix in study.EDITIONS.values():
            output = DOCUMENT + suffix
            path = self.root / "release/publications/gpt" / f"{output}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"schema_version": 1, "id": output, "catalog": CATALOG,
                                        "status": "alpha", "authorization": "standing"}))
        self.generated = self.root / "build/web/gpt" / f"{DOCUMENT}.md"
        self.generated.parent.mkdir(parents=True)
        self.generated.write_text("# Isolated canonical conversion fixture\n\nComplete fixture text.\n")
        # No web edition is tracked; the gate converts current sources afresh,
        # which this fixture's converter double reproduces byte for byte.
        self.fresh_conversion = self.generated.read_text()
        study.snapshot(self.root, "gpt", DOCUMENT, web=True)

    def write_manifest(self):
        (self.leaf / "publication.toml").write_text(schema.dumps_manifest(self.declaration))

    def source_state(self):
        # Source/schema/component/chronology checks run normally. Only external
        # owning-tool invocations get fixture exits; no editorial PASS is made.
        with patch.object(schema.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")):
            return study.source_state(self.root, "gpt", DOCUMENT)

    def convert(self, root, *arguments):
        if "tools/web-edition" in str(arguments[1]) and "--output" in arguments:
            out = Path(arguments[arguments.index("--output") + 1]) / "gpt" / f"{arguments[-1]}.md"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(self.fresh_conversion)

    def publish(self, **kwargs):
        with patch.object(study, "scope", return_value=CATALOG), \
                patch.object(study, "run", side_effect=self.convert) as commands, \
                patch.object(schema.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")):
            study.publication(self.root, "gpt", DOCUMENT, **kwargs)
            return commands.call_args_list

    def test_declared_three_outputs_and_source_publication_need_no_pdf_access(self):
        original = Path.read_bytes
        pdf = self.root / "pdf/gpt" / f"{DOCUMENT}.pdf"
        pdf.parent.mkdir(parents=True)
        pdf.write_bytes(b"Unreviewed stale output must never be consulted.\n")

        def read_bytes(path):
            if path.suffix == ".pdf":
                raise AssertionError("source publication opened a PDF")
            return original(path)

        with patch.object(Path, "read_bytes", read_bytes), \
                patch.object(study, "artifacts", side_effect=AssertionError("print gate invoked")):
            state = self.source_state()
            commands = self.publish(mode="source")
        self.assertEqual(list(state["identities"]["outputs"]), ["canonical", "synthesis", "homily"])
        self.assertEqual(state["publication_mode"], "source")
        self.assertTrue(any("check-web-edition" in str(call) for call in commands))
        self.assertTrue(any("'check', '--leaf'" in str(call) for call in commands))
        self.assertFalse(any("--pdf" in str(call) for call in commands))

    def test_a_reviewed_conversion_current_sources_no_longer_produce_fails(self):
        self.fresh_conversion = "# Isolated canonical conversion fixture\n\nChanged since review.\n"
        with self.assertRaisesRegex(ValueError, "not what current sources convert to"):
            self.publish(mode="source")

    def test_missing_required_semantic_role_fails_source_gate(self):
        # A required record is declared by its registered path, so the role
        # fails only when the record itself is missing.
        self.declaration["structure"] = [item for item in self.declaration["structure"] if item["role"] != "scope"]
        self.write_manifest()
        (self.leaf / "research/scope.md").unlink()
        with self.assertRaisesRegex(ValueError, "missing required role: scope"):
            self.source_state()

    def test_held_companion_is_not_published_by_canonical_source_acceptance(self):
        path = self.root / "release/publications/gpt" / f"{DOCUMENT}-homily.json"
        record = json.loads(path.read_text())
        record["status"] = "hold"
        path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "release record does not authorize homily"):
            self.publish(mode="source")

    def test_missing_canonical_reader_fails_without_falling_back_to_print(self):
        self.catalog.write_text(f"<!-- triptych-publication-id: {DOCUMENT} -->\n| Example | unavailable |\n")
        with self.assertRaisesRegex(ValueError, "canonical web edition"):
            self.publish(mode="source")

    def test_missing_source_output_and_absent_pdf_link_fail(self):
        original = (self.leaf / "homily.tex").read_text()
        (self.leaf / "homily.tex").unlink()
        with self.assertRaises(ValueError):
            self.source_state()
        (self.leaf / "homily.tex").write_text(original)
        self.catalog.write_text(self.catalog.read_text().replace(
            " |\n", f" [Print](../pdf/gpt/{DOCUMENT}.pdf) |\n"))
        with self.assertRaisesRegex(ValueError, "absent site PDFs"):
            self.publish(mode="source")

    def test_source_web_seal_binds_content_evidence_and_render_inputs(self):
        seal = lambda: study.review_inputs(self.root, "gpt", DOCUMENT, "web", mode="source")
        before = seal()
        self.assertIn("source_publication", before)
        for filename in ("production-review.md", "artifacts.json"):
            (self.leaf / "research" / filename).write_text("Operational receipt only.\n")
        self.assertEqual(before, seal())
        (self.leaf / "sermon.tex").write_text("Changed separately authored homily fixture.\n")
        self.assertNotEqual(before, seal())
        self.assertNotIn("source_publication", study.review_inputs(self.root, "gpt", DOCUMENT, "web"))

    def test_research_source_seal_tracks_rights_metadata_without_witness_io(self):
        artifact = self.root / "src/sources/works/author/book/editions/edition/artifacts/witness"
        artifact.mkdir(parents=True)
        witness = artifact / "witness.pdf"
        metadata = artifact / "artifact.toml"
        metadata.write_text('sha256="' + "a" * 64 + '"\nrights="permitted"\n')
        (self.leaf / "research/review-dependencies.toml").write_text(
            'paths=["' + witness.relative_to(self.root).as_posix() + '"]\n')
        # The exact external witness is deliberately absent. Its metadata owner
        # remains part of the research seal, without claiming byte inspection.
        before = study.review_inputs(self.root, "gpt", DOCUMENT, "research", mode="source")
        self.assertIn(metadata.relative_to(self.root).as_posix(), before["files"])
        self.assertNotIn(witness.relative_to(self.root).as_posix(), before["files"])
        metadata.write_text(metadata.read_text().replace("permitted", "restricted"))
        self.assertNotEqual(before, study.review_inputs(self.root, "gpt", DOCUMENT, "research", mode="source"))

    def test_historical_default_and_explicit_print_retain_render_gate(self):
        for options in ({}, {"mode": "print"}):
            with self.subTest(options=options), patch.object(study, "artifacts", side_effect=ValueError("exact PDF required")), \
                    self.assertRaisesRegex(ValueError, "exact PDF required"):
                self.publish(**options)

    def test_source_mode_cannot_create_a_visual_print_approval(self):
        with patch.object(study, "artifact_state", side_effect=AssertionError("PDF read")), \
                self.assertRaisesRegex(ValueError, "explicit print export"):
            study.review_inputs(self.root, "gpt", DOCUMENT, "visual", mode="source")


class SourceWorkflowTests(unittest.TestCase):
    def test_v17_source_route_finishes_after_independent_source_and_web_reviews(self):
        fixture = EngineFixture(self, source_mode=True)
        self.assertEqual(fixture.workflow["version"], 17)
        self.assertNotIn("visual-review", fixture.stages)
        fixture.drive_to("artifact-gates")
        fixture.advance()
        self.assertEqual(fixture.state()["current_stage"], "generate-web")
        fixture.drive_to("ACCEPTED")
        for reviewer in ("research-review", "study-review", "synthesis-review", "homily-review", "web-review"):
            self.assertEqual(fixture.visited.count(reviewer), 1)

    def test_source_gate_failure_routes_to_study_owner_and_reopens_dependents(self):
        fixture = EngineFixture(self, source_mode=True)
        fixture.drive_to("artifact-gates")
        (fixture.root / "artifact-check-fails").touch()
        fixture.advance()
        self.assertEqual(fixture.state()["current_stage"], "author-study")
        self.assertEqual(fixture.last_result()["findings"][0]["repair_target"], "study")
        (fixture.root / "artifact-check-fails").unlink()
        fixture.drive_to("ACCEPTED")
        self.assertEqual(fixture.visited.count("study-review"), 2)
        self.assertEqual(fixture.visited.count("homily-review"), 2)

    def test_changed_source_or_web_cannot_accept_under_old_seal(self):
        for reviewer, owner in (("research-review", "research"), ("study-review", "author-study"),
                                ("web-review", "generate-web")):
            with self.subTest(reviewer=reviewer):
                fixture = EngineFixture(self, source_mode=True)
                fixture.drive_to("publication-gates")
                fixture.inputs[reviewer].write_text("Changed after independent fixture review.\n")
                fixture.advance()
                self.assertEqual(fixture.state()["current_stage"], owner)
                self.assertNotEqual(fixture.state()["disposition"], "ACCEPTED")

    def test_new_definition_does_not_migrate_historical_run_identity(self):
        fixture = EngineFixture(self)
        fixture.drive_to("ACCEPTED")
        before = (fixture.engine.run_dir(fixture.run_id) / "state.json").read_bytes()
        path = fixture.root / "workflows/pipelines/proper-study.json"
        workflow = json.loads(path.read_text())
        workflow["version"] = 16
        path.write_text(json.dumps(workflow))
        self.assertEqual(fixture.engine.status(fixture.run_id)["disposition"], "ACCEPTED")
        self.assertIsNone(fixture.engine.replay(fixture.run_id)["deterministic"])
        self.assertEqual(before, (fixture.engine.run_dir(fixture.run_id) / "state.json").read_bytes())
        with self.assertRaisesRegex(WorkflowError, "v15.*v16"):
            fixture.engine.load_bound_workflow(fixture.state())

    def test_unknown_per_check_repair_owner_is_rejected(self):
        def invalid(workflow):
            gate = next(stage for stage in workflow["stages"] if stage["id"] == "artifact-gates")
            gate["checks"][0]["repair_target"] = "unowned"
        with self.assertRaisesRegex(WorkflowError, "check repair_target"):
            EngineFixture(self, invalid, source_mode=True)


if __name__ == "__main__":
    unittest.main()
