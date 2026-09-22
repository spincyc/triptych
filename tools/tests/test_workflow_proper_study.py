"""Three-document routing, family boundaries, request identity and review receipts."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _proper_study as study
from _workflow import WorkflowEngine, WorkflowError
from tools.tests.test_proper_components_v2 import fixture as component_fixture, save as save_components

TLM = "liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost"
PC = ("liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/"
      "propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a")

loader = importlib.machinery.SourceFileLoader("study_launcher", str(ROOT / "tools/tpt"))
spec = importlib.util.spec_from_loader(loader.name, loader)
launcher = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = launcher
spec.loader.exec_module(launcher)


class DefinitionTests(unittest.TestCase):
    def setUp(self):
        self.engine = WorkflowEngine(ROOT, ROOT / "workflows")
        self.workflow = self.engine.load_workflow("proper-study")
        self.stages = {stage["id"]: stage for stage in self.workflow["stages"]}

    def test_each_substantive_deliverable_has_its_own_cold_review(self):
        for author, review in (("research", "research-review"),
                               ("author-study", "study-review"),
                               ("derive-synthesis", "synthesis-review"),
                               ("derive-homily", "homily-review")):
            with self.subTest(author=author):
                self.assertEqual(self.stages[author]["execution"], {"mode": "single"})
                gate = self.stages[self.stages[author]["next"]]
                self.assertEqual(gate["type"], "gate")
                self.assertEqual(gate["pass_transition"], review)
                self.assertEqual(self.stages[review]["effort"], "xhigh")
                self.assertIn("proper-study/review.md", self.stages[review]["fragments"])

    def test_upstream_repair_cannot_skip_downstream_authors_and_reviews(self):
        route = {item["repair_target"]: item["transition"]
                 for item in self.stages["homily-review"]["repair_routes"]}
        self.assertEqual(route["research"], "research")
        self.assertEqual(route["study"], "author-study")
        visited, stage = [], route["study"]
        while stage != "ACCEPTED":
            visited.append(stage)
            entry = self.stages[stage]
            stage = entry.get("next", entry.get("pass_transition"))
        for required in ("study-review", "derive-synthesis", "synthesis-review",
                         "derive-homily", "homily-review", "visual-review", "web-review"):
            self.assertIn(required, visited)
        self.assertLess(visited.index("web-review"), visited.index("install-publication"))

    def test_no_legacy_two_page_or_gallery_gate(self):
        pipeline = json.dumps(self.workflow)
        for obsolete in ("--aux", "proposal-fields", "traditional-latin-mass.md"):
            self.assertNotIn(obsolete, pipeline)
        for stage in self.stages.values():
            for fragment in stage.get("fragments", []):
                self.assertTrue((ROOT / "workflows/fragments" / fragment).is_file())

    def test_date_and_audience_change_run_identity(self):
        args = {"proper": TLM, "provider": "gpt", "date": "2026-09-20"}
        first = self.engine.compute_run_id("proper-study", 1, "a" * 40, args)
        self.assertNotEqual(first, self.engine.compute_run_id(
            "proper-study", 1, "a" * 40, {**args, "date": "2026-09-27"}))
        self.assertNotEqual(first, self.engine.compute_run_id(
            "proper-study", 1, "a" * 40, {**args, "audience": "children"}))


class RegistryTests(unittest.TestCase):
    def test_both_families_resolve_to_their_own_catalog(self):
        self.assertEqual(study.identity(ROOT, TLM), "library/traditional-latin-mass.md")
        self.assertEqual(study.identity(ROOT, PC), "library/novus-ordo-liturgy.md")

    def test_unregistered_formula_and_wrong_stem_are_refused(self):
        for invalid in (PC.replace("pc-s51", "pc-s99"),
                        PC.replace("twenty-fifth", "twenty-fourth"),
                        PC + "-vigil", "/" + PC, PC.replace("/temporal/", "/../")):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                study.identity(ROOT, invalid)

    def test_edition_and_authorization_are_exact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "guidance/liturgy"
            path.mkdir(parents=True)
            shutil.copy(ROOT / "guidance/liturgy/postconciliar-propers-registry.md", path)
            (path / "propers-production-plan.md").write_text(
                f"- Authorized 2026-09-17: provider `gpt`, identity `{PC}`.\n")
            registry = root / "src/gpt" / PC.split("/propers/")[0] / "propers/registry"
            registry.mkdir(parents=True)
            self.assertEqual(study.scope(root, "gpt", PC), "library/novus-ordo-liturgy.md")
            for provider, document in (("claude", PC), ("gpt", PC.replace("year-a", "year-b")),
                                       ("gpt", PC.replace("en-us-2011", "en-gb-2011"))):
                with self.subTest(provider=provider, document=document), self.assertRaises(ValueError):
                    study.scope(root, provider, document)


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.engine = WorkflowEngine(ROOT, ROOT / "workflows")

    def test_declared_request_flags_reach_seed_without_seeding_a_real_run(self):
        output = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
        with patch.object(self.engine, "seed_bytes", return_value=b"{}") as seed, patch.object(sys, "stdout", output):
            launcher._workflow_seed(self.engine, "proper-study", TLM, [
                "--provider", "gpt", "--date", "2026-09-20", "--audience", "adult parish assembly",
                "--research-handoff", ".scratch/research/dossier.md"])
        self.assertEqual(seed.call_args.args[1], {
            "proper": TLM, "provider": "gpt", "date": "2026-09-20",
            "audience": "adult parish assembly", "research_handoff": ".scratch/research/dossier.md"})

    def test_unknown_duplicate_and_missing_flags_fail_closed(self):
        for options in (["--date"], ["--date", "--provider", "gpt"],
                        ["--date", "2026-09-20", "--date", "2026-09-21"], ["--invented", "x"]):
            with self.subTest(options=options), self.assertRaises(launcher.ToolError):
                launcher._workflow_seed(self.engine, "proper-study", TLM, options)
        with self.assertRaises(launcher.ToolError):
            launcher._workflow_seed(self.engine, "proper", TLM, ["--date", "2026-09-20"])


class ExecutionTests(unittest.TestCase):
    """Exercise routing using fixture verdicts; never seed a production run."""

    def test_homily_upstream_finding_reopens_all_dependent_reviews(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "workflows", root / "workflows")
            pipeline_path = root / "workflows/pipelines/proper-study.json"
            pipeline = json.loads(pipeline_path.read_text())
            pipeline["document_discovery"].pop("validator")
            for stage in pipeline["stages"]:
                if "review_input_command" in stage:
                    stage["review_input_command"] = "python3 -c 'import json; print(json.dumps({\"fixture\": \"stable\"}))'"
                for check in stage.get("checks", []):
                    check["command"] = "true"
            pipeline_path.write_text(json.dumps(pipeline))
            engine = WorkflowEngine(root, root / "workflows")
            engine.standing_findings_root = None
            with patch.object(engine, "get_repo_commit", return_value="a" * 40):
                seeded = engine.seed("proper-study", {
                    "proper": TLM, "date": "2026-09-20", "audience": "adult parish assembly",
                    "research_handoff": ".scratch/family-research/dossier.md"})
            self.assertEqual(seeded["normalized_args"]["date"], "2026-09-20")
            run_id = seeded["run_id"]
            stages = {stage["id"]: stage for stage in pipeline["stages"]}
            submitted, rejected_once = [], False
            for index in range(100):
                state = engine.load_state(run_id)
                if state["disposition"]:
                    self.assertEqual(state["disposition"], "ACCEPTED")
                    break
                current = state["current_stage"]
                if current == "resolve-context":
                    packet_text = (root / state["packet_hashes"][-1]["path"]).read_text()
                    for expected in ('"date":"2026-09-20"',
                                     '"audience":"adult parish assembly"',
                                     '"research_handoff":".scratch/family-research/dossier.md"'):
                        self.assertIn(expected, packet_text)
                if stages[current]["type"] == "gate":
                    engine.advance(run_id, run_gate=True)
                    continue
                packet = state["packet_hashes"][-1]
                body = {"stage": current, "iteration": packet["iteration"],
                        "disposition": "PASS", "summary": "Fixture result only."}
                if stages[current]["type"] == "evaluator":
                    body["findings"] = []
                if current == "homily-review" and not rejected_once:
                    rejected_once = True
                    body.update(disposition="CHANGES_REQUIRED", findings=[{
                        "id": "HOM-FIXTURE-001", "severity": "blocking",
                        "location": "study argument", "problem": "fixture upstream defect",
                        "required_result": "repair the study and rederive both companions",
                        "repair_target": "study"}])
                forwarded = state.get("findings_forwarded_ids", {}).get(current, [])
                if forwarded:
                    body["finding_dispositions"] = [
                        {"id": value, "outcome": "repaired"} for value in forwarded]
                path = root / f"result-{index}.json"
                path.write_text(json.dumps(body))
                engine.advance(run_id, result_path=str(path))
                submitted.append(current)
            else:
                self.fail("fixture workflow did not terminate")
            for stage in ("author-study", "study-review", "derive-synthesis",
                          "synthesis-review", "derive-homily", "homily-review"):
                self.assertEqual(submitted.count(stage), 2, stage)
            self.assertEqual(submitted.count("research-review"), 1)
            self.assertEqual(submitted.count("visual-review"), 1)



class ReviewSealExecutionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        shutil.copytree(ROOT / "workflows", self.root / "workflows")
        path = self.root / "workflows/pipelines/proper-study.json"
        pipeline = json.loads(path.read_text())
        pipeline["document_discovery"].pop("validator")
        for stage in pipeline["stages"]:
            if "review_input_command" in stage:
                name = stage["id"].removesuffix("-review")
                (self.root / (name + ".txt")).write_text("original")
                stage["review_input_command"] = (
                    "python3 -c 'import json,pathlib; print(json.dumps({\"input\": pathlib.Path(\""
                    + name + ".txt\").read_text()}))'")
            for check in stage.get("checks", []):
                check["command"] = "true"
        path.write_text(json.dumps(pipeline))
        self.engine = WorkflowEngine(self.root, self.root / "workflows")
        self.engine.standing_findings_root = None
        with patch.object(self.engine, "get_repo_commit", return_value="a" * 40):
            self.run_id = self.engine.seed("proper-study", {"proper": TLM})["run_id"]
        self.stages = {stage["id"]: stage for stage in pipeline["stages"]}
        self.submitted = []

    def advance(self, supplied=None):
        state = self.engine.load_state(self.run_id)
        stage = state["current_stage"]
        if self.stages[stage]["type"] == "gate":
            return self.engine.advance(self.run_id, run_gate=True)
        body = {"stage": stage, "iteration": state["packet_hashes"][-1]["iteration"],
                "disposition": "PASS", "summary": "Fixture verdict, not production evidence."}
        if self.stages[stage]["type"] == "evaluator":
            body["findings"] = []
        forwarded = state.get("findings_forwarded_ids", {}).get(stage, [])
        if forwarded:
            body["finding_dispositions"] = [{"id": value, "outcome": "repaired"} for value in forwarded]
        body.update(supplied or {})
        path = self.root / "result.json"
        path.write_text(json.dumps(body))
        result = self.engine.advance(self.run_id, result_path=str(path))
        self.submitted.append(stage)
        return result

    def drive_to(self, target):
        for _ in range(100):
            current = self.engine.load_state(self.run_id)["current_stage"]
            if current == target:
                return
            self.assertNotIn(current, ("ACCEPTED", "BLOCKED"))
            self.advance()
        self.fail("fixture did not reach " + target)

    def test_changed_study_cannot_accept_and_routes_through_all_downstream_reviews(self):
        self.drive_to("publication-gates")
        (self.root / "study.txt").write_text("changed after artifact and cold reviews")
        self.advance()
        self.assertEqual(self.engine.load_state(self.run_id)["current_stage"], "author-study")
        self.drive_to("ACCEPTED")
        for stage in ("study-review", "synthesis-review", "homily-review", "visual-review", "web-review"):
            self.assertEqual(self.submitted.count(stage), 2, stage)
        self.assertEqual(self.submitted.count("research-review"), 1)
        # Historical replay checks the stored seal, not today's changed source.
        with patch.object(self.engine, "get_repo_commit", return_value="a" * 40):
            self.engine.seed("proper-study", {"proper": TLM})

    def test_changed_during_dispatch_rejects_pass_and_replay_stays_stable(self):
        self.drive_to("study-review")
        before = self.engine.replay(self.run_id)
        (self.root / "study.txt").write_text("changed while reviewer works")
        self.assertEqual(before, self.engine.replay(self.run_id))
        self.advance()
        state = self.engine.load_state(self.run_id)
        self.assertEqual(state["current_stage"], "author-study")
        body = json.loads((self.root / state["result_hashes"][-1]["path"]).read_text())
        self.assertEqual(body["disposition"], "CHANGES_REQUIRED")
        self.assertEqual(body["review_inputs"], {"input": "original"})

    def test_worker_cannot_choose_its_own_seal(self):
        self.drive_to("research-review")
        with self.assertRaisesRegex(WorkflowError, "reserved"):
            self.advance({"review_inputs": {"input": "forged"}})

    def test_terminal_audit_refuses_stale_review_even_when_gate_is_stubbed(self):
        self.drive_to("publication-gates")
        (self.root / "research.txt").write_text("changed evidence")
        stage = self.stages["publication-gates"]
        state = self.engine.load_state(self.run_id)
        fake = {"stage": stage["id"], "iteration": state["packet_hashes"][-1]["iteration"],
                "disposition": "PASS", "findings": []}
        with patch.object(self.engine, "_run_gate", return_value=fake), \
             self.assertRaisesRegex(WorkflowError, "STALE-RESEARCH-REVIEW"):
            self.advance()

    def test_artifact_and_web_mutations_route_to_their_actual_owners(self):
        self.drive_to("publication-gates")
        (self.root / "visual.txt").write_text("rebuilt PDF and refreshed mutable receipt")
        (self.root / "web.txt").write_text("regenerated web and refreshed mutable receipt")
        self.advance()
        self.assertEqual(self.engine.load_state(self.run_id)["current_stage"], "build-artifacts")
        self.drive_to("ACCEPTED")
        self.assertEqual(self.submitted.count("study-review"), 1)
        self.assertEqual(self.submitted.count("visual-review"), 2)
        self.assertEqual(self.submitted.count("web-review"), 2)


class ResearchSealTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.leaf = self.root / "src/gpt" / TLM
        (self.leaf / "research").mkdir(parents=True)
        for name in ("context.md", "scope.md", "interpretations.md"):
            (self.leaf / "research" / name).write_text("Evidence " + name)
        (self.leaf / "research/source-bindings.toml").write_text("bindings = []\n")
        (self.leaf / "research/review-dependencies.toml").write_text("paths = []\n")
        (self.leaf / "propers").mkdir()
        (self.leaf / "propers/verified.md").write_text("Complete appointed prayers and readings")

    def seal(self):
        return study.review_inputs(self.root, "gpt", TLM, "research")

    def test_research_and_appointed_text_mutations_are_sealed_but_audit_receipts_are_not(self):
        before = self.seal()
        (self.leaf / "research/production-review.md").write_text("honest new production audit")
        (self.leaf / study.RECEIPT).write_text("refreshed mutable receipt")
        self.assertEqual(before, self.seal())
        (self.leaf / "propers/verified.md").write_text("different Collect witness")
        self.assertNotEqual(before, self.seal())
        before = self.seal()
        (self.leaf / "research/interpretations.md").write_text("different interpretation")
        self.assertNotEqual(before, self.seal())

    def test_declared_cross_family_evidence_is_refused(self):
        opposite = self.root / "src/gpt" / PC / "propers/verified.md"
        opposite.parent.mkdir(parents=True)
        opposite.write_text("opposite family's prayers")
        (self.leaf / "research/review-dependencies.toml").write_text(
            "paths = [" + json.dumps(str(opposite.relative_to(self.root))) + "]\n")
        with self.assertRaisesRegex(ValueError, "boundary"):
            self.seal()

    def test_lane_source_mutation_changes_the_study_seal(self):
        data, manifest, _ = component_fixture(self.root)
        save_components(data, manifest)
        leaf = manifest.parent
        for entry in study.EDITIONS:
            path = leaf / ("main.tex" if entry == "research" else entry + ".tex")
            path.write_text(path.read_text().replace("\\input{proper/generation-metadata}\n", ""))
        before = study.review_inputs(self.root, "gpt", "proper", "study")
        lane_source = leaf / "research/sources.md"
        lane_source.write_text("Changed evidence map after study review.\n")
        self.assertNotEqual(before, study.review_inputs(self.root, "gpt", "proper", "study"))


class PostconciliarOwnerTests(unittest.TestCase):
    EDITION = "roman-missal-third-edition-en-us-2011"

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def fixture(self, family: str, slug: str, owner: str) -> tuple[str, Path]:
        document = (f"liturgy/roman-rite/postconciliar/{self.EDITION}/"
                    f"propers/{family}/{slug}")
        leaf = self.root / "src/gpt" / document
        (leaf / "research").mkdir(parents=True)
        proper_root = self.root / "src/gpt/liturgy/roman-rite/postconciliar" / self.EDITION / "propers"
        record = proper_root / owner / "propers/verified.md"
        record.parent.mkdir(parents=True)
        record.write_text("Canonical edition formulary owner.\n")
        registry = proper_root / "registry/formula-dispositions.md"
        registry.parent.mkdir(parents=True, exist_ok=True)
        relative = Path("..") / owner / "propers/verified.md"
        registry.write_text(
            "| Formula | Full publication slug | Canonical owner |\n"
            "| --- | --- | --- |\n"
            f"| `FORMULA` | `{slug}` | [Owner]({relative.as_posix()}) |\n"
        )
        (leaf / "research/review-dependencies.toml").write_text(
            "paths = [" + json.dumps(record.relative_to(self.root).as_posix()) + "]\n"
        )
        return document, record

    def test_exact_temporal_and_general_calendar_owners_are_accepted(self):
        cases = (
            ("temporal", "pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a",
             "temporal/shared/ordinary-time/weeks/25"),
            ("general-calendar", "pc-r07-all-saints-abc",
             "general-calendar/shared/formularies/pc-r07-all-saints"),
        )
        for family, slug, owner in cases:
            with self.subTest(family=family):
                document, record = self.fixture(family, slug, owner)
                self.assertIn(record, study.research_dependencies(self.root, "gpt", document))

    def test_similarly_named_neutral_path_cannot_spoof_the_canonical_owner(self):
        document, _ = self.fixture(
            "temporal", "pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a",
            "temporal/shared/ordinary-time/weeks/25",
        )
        fake = self.root / "src/sources/unrelated/propers/temporal/shared/not-an-owner.txt"
        fake.parent.mkdir(parents=True)
        fake.write_text("Unrelated provider-neutral record.\n")
        leaf = self.root / "src/gpt" / document
        (leaf / "research/review-dependencies.toml").write_text(
            "paths = [" + json.dumps(fake.relative_to(self.root).as_posix()) + "]\n"
        )
        with self.assertRaisesRegex(ValueError, "canonical shared Missal formulary owner"):
            study.research_dependencies(self.root, "gpt", document)

    def test_target_slug_mentioned_in_another_rows_qualification_is_not_its_row(self):
        slug = "pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a"
        document, record = self.fixture(
            "temporal", slug, "temporal/shared/ordinary-time/weeks/25",
        )
        registry = record.parents[6] / "registry/formula-dispositions.md"
        registry.write_text(
            "| Full publication slug | Canonical owner | Qualification |\n"
            "| --- | --- | --- |\n"
            "| `pc-s50-twenty-fourth-sunday-in-ordinary-time-year-a` | "
            "[Owner](../temporal/shared/ordinary-time/weeks/25/propers/verified.md) | "
            f"See `{slug}` for comparison. |\n"
        )
        with self.assertRaisesRegex(ValueError, "exact target slug row"):
            study.postconciliar_shared_owner(self.root, "gpt", document)



class EvidenceAndMetadataTests(unittest.TestCase):
    def source_fixture(self):
        from tools.tests.test_source_library import SourceLibraryTests
        fixture = SourceLibraryTests()
        fixture.setUp()
        self.addCleanup(fixture.tearDown)
        fixture.add_valid_vertical_fixture()
        return fixture

    def test_new_leaf_binding_requires_then_accepts_honest_owner_scaffold(self):
        from tools.tests.test_source_library import SOURCE_LIBRARY
        fixture = self.source_fixture()
        original = fixture.root / "src/gpt/theology/demo/research/source-bindings.toml"
        target = fixture.root / "src/gpt" / TLM
        (target / "research").mkdir(parents=True)
        (target / "research/source-bindings.toml").write_text(
            original.read_text().replace('document = "theology/demo"', 'document = "' + TLM + '"'))
        errors = SOURCE_LIBRARY.load_library(fixture.root).errors
        self.assertTrue(any("document has no main.tex" in error for error in errors), errors)
        (target / "main.tex").write_text("% Proper-study source owner reserved; author-study supplies the document.\n")
        self.assertEqual(SOURCE_LIBRARY.load_library(fixture.root).errors, [])
        self.assertIn("if `main.tex` does not yet exist", (ROOT / "workflows/fragments/proper-study/resolve-context.md").read_text())

    def test_bound_source_ancestor_and_payload_bytes_are_included(self):
        fixture = self.source_fixture()
        binding = fixture.root / "src/gpt/theology/demo/research/source-bindings.toml"
        paths = study.bound_evidence(fixture.root, binding)
        names = {path.name for path in paths}
        self.assertTrue({"work.toml", "edition.toml", "artifact.toml", "city-of-god.txt"} <= names)
        before = {str(path): study.digest(path) for path in paths}
        payload = next(path for path in paths if path.name == "city-of-god.txt")
        payload.write_text("changed physical source payload")
        after = {str(path): study.digest(path) for path in study.bound_evidence(fixture.root, binding)}
        self.assertNotEqual(before, after)

    def test_finalizing_pure_metadata_preserves_content_review_but_changes_visual_seal(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        leaf = root / "src/gpt" / TLM
        (leaf / "sections").mkdir(parents=True)
        (leaf / "proper-components.toml").write_text(
            'schema=2\ndocument="' + TLM + '"\ncalendar="roman-1962"\nelement_keys=["collect"]\nlanes=[]\n'
            '[[components]]\nkey="body"\nkind="proper-treatment"\npath="sections/body.tex"\nmodes=["research"]\nreferences=[]\n')
        (leaf / "sections/body.tex").write_text("Meaning-bearing study with source notes.")
        metadata = leaf / "generation-metadata.tex"
        metadata.write_text("\\AIDocumentRevisionTimestamp{2026-09-17T10:00:00Z}\n"
                            "\\AIGenerationProvenance{proper-study}{1}{digest}{run}{commit}{unknown}\n"
                            "\\AIModelContribution{model}{effort=high}{runtime}\n")
        for mode, suffix in study.EDITIONS.items():
            source = leaf / ("main.tex" if mode == "research" else mode + ".tex")
            source.write_text("\\input{" + TLM + "/generation-metadata}\n\\input{" + TLM + "/sections/body}\n")
            output = root / "build/gpt" / (TLM + suffix)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.with_suffix(".pdf").write_bytes(b"fixture")
            output.with_suffix(".fls").write_text(f"INPUT {source}\nINPUT {metadata}\n")
        semantic = study.review_inputs(root, "gpt", TLM, "study")
        visual = study.review_inputs(root, "gpt", TLM, "visual")
        metadata.write_text(metadata.read_text().replace("10:00:00", "11:00:00") +
                            "\\AIModelContribution{model}{effort=high}{later actual contribution}\n")
        self.assertEqual(semantic, study.review_inputs(root, "gpt", TLM, "study"))
        self.assertNotEqual(visual, study.review_inputs(root, "gpt", TLM, "visual"))
        (leaf / "synthesis.tex").write_text("new concise text")
        self.assertEqual(semantic, study.review_inputs(root, "gpt", TLM, "study"))
        metadata.write_text(metadata.read_text() + "Hidden meaning-bearing sermon text.\n")
        with self.assertRaisesRegex(ValueError, "meaning-bearing"):
            study.review_inputs(root, "gpt", TLM, "study")


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.leaf = self.root / "src/gpt" / TLM
        self.leaf.mkdir(parents=True)
        (self.leaf / "proper-components.toml").write_text("schema = 2\n")
        self.shared = self.root / "src/common/preamble.tex"
        self.shared.parent.mkdir(parents=True)
        self.shared.write_text("Shared typesetting\n")
        for mode, suffix in study.EDITIONS.items():
            source = "main.tex" if mode == "research" else f"{mode}.tex"
            (self.leaf / source).write_text("Stable " + mode)
            path = self.root / "build/gpt" / f"{TLM}{suffix}"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.with_suffix(".pdf").write_bytes(b"fixture pdf " + mode.encode())
            path.with_suffix(".fls").write_text(
                f"PWD {self.root / 'src/gpt'}\nINPUT {self.shared}\nINPUT {self.leaf / source}\n")

    def test_snapshot_binds_all_three_pdfs_and_actual_shared_inputs(self):
        study.snapshot(self.root, "gpt", TLM)
        stored = json.loads((self.leaf / study.RECEIPT).read_text())
        self.assertEqual(stored, study.artifact_state(self.root, "gpt", TLM))
        self.assertEqual(len(stored["pdfs"]), 3)
        self.assertIn("src/common/preamble.tex", stored["render_inputs"])
        self.assertNotIn(str(self.root), json.dumps(stored))
        self.shared.write_text("Changed shared typesetting\n")
        self.assertNotEqual(stored, study.artifact_state(self.root, "gpt", TLM))

    def test_a_new_render_file_or_changed_homily_invalidates_snapshot(self):
        stored = study.artifact_state(self.root, "gpt", TLM)
        (self.leaf / "new.tex").write_text("new render material")
        self.assertNotEqual(stored, study.artifact_state(self.root, "gpt", TLM))
        (self.root / "build/gpt" / f"{TLM}-homily.pdf").write_bytes(b"different")
        self.assertNotEqual(stored["pdfs"], study.artifact_state(self.root, "gpt", TLM)["pdfs"])

    def test_missing_recorder_refuses_unbound_artifact(self):
        (self.root / "build/gpt" / f"{TLM}-homily.fls").unlink()
        with self.assertRaisesRegex(ValueError, "missing build recorder"):
            study.artifact_state(self.root, "gpt", TLM)

    def test_cross_family_input_in_actual_recorder_is_refused(self):
        other = self.root / "src/gpt" / PC / "main.tex"
        other.parent.mkdir(parents=True)
        other.write_text("wrong family's appointed text")
        recorder = self.root / "build/gpt" / f"{TLM}-homily.fls"
        with recorder.open("a") as handle:
            handle.write(f"INPUT {other}\n")
        with self.assertRaises(ValueError):
            study.artifact_state(self.root, "gpt", TLM)

    def test_web_snapshot_records_generated_bytes_without_installing(self):
        web = self.root / "build/web/gpt" / f"{TLM}.md"
        web.parent.mkdir(parents=True)
        web.write_text("# Reviewed conversion\n")
        study.snapshot(self.root, "gpt", TLM, web=True)
        stored = json.loads((self.leaf / study.WEB_RECEIPT).read_text())
        self.assertEqual(stored["sha256"], study.digest(web))
        self.assertEqual(stored["web"], str(web.relative_to(self.root)))
        self.assertFalse((self.root / "web").exists())


class PublicationTests(unittest.TestCase):
    def setUp(self):
        SnapshotTests.setUp(self)
        self.catalog = "library/traditional-latin-mass.md"
        lines = []
        (self.leaf / "proper-components.toml").write_text(
            'schema = 2\n[outputs]\n' + '\n'.join(
                f'{mode} = "{TLM}{suffix}"' for mode, suffix in study.EDITIONS.items()))
        release = self.root / "release"
        release.mkdir()
        (release / "public-alpha.json").write_text(json.dumps({
            "provider": "gpt", "authorizations": {"standing": {}}}))
        for suffix in study.EDITIONS.values():
            output = TLM + suffix
            pdf = self.root / "pdf/gpt" / f"{output}.pdf"
            pdf.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(self.root / "build/gpt" / f"{output}.pdf", pdf)
            record = release / "publications/gpt" / f"{output}.json"
            record.parent.mkdir(parents=True, exist_ok=True)
            record.write_text(json.dumps({"schema_version": 1, "id": output,
                "catalog": self.catalog, "status": "alpha", "authorization": "standing"}))
            lines.append(f"[PDF](../pdf/gpt/{output}.pdf)")
        for folder in ("web", "build/web"):
            web = self.root / folder / "gpt" / f"{TLM}.md"
            web.parent.mkdir(parents=True)
            web.write_text("# Canonical web\n")
        study.snapshot(self.root, "gpt", TLM, web=True)
        lines.append(f"[Read](../web/gpt/{TLM}.html)")
        catalog = self.root / self.catalog
        catalog.parent.mkdir()
        catalog.write_text(f"<!-- triptych-publication-id: {TLM} -->\n| " + " · ".join(lines) + " |\n")

    def check(self):
        with patch.object(study, "scope", return_value=self.catalog), \
             patch.object(study, "artifacts"), patch.object(study, "run"):
            study.publication(self.root, "gpt", TLM)

    def test_three_installed_and_reviewed_outputs_pass(self):
        self.check()

    def test_changed_installed_homily_fails(self):
        (self.root / "pdf/gpt" / f"{TLM}-homily.pdf").write_bytes(b"unreviewed")
        with self.assertRaisesRegex(ValueError, "installed homily"):
            self.check()

    def test_opposite_family_release_catalog_fails(self):
        path = self.root / "release/publications/gpt" / f"{TLM}-homily.json"
        record = json.loads(path.read_text())
        record["catalog"] = "library/novus-ordo-liturgy.md"
        path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "release record"):
            self.check()

    def test_unknown_authorization_is_not_a_release(self):
        path = self.root / "release/publications/gpt" / f"{TLM}.json"
        record = json.loads(path.read_text())
        record["authorization"] = "invented"
        path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "release record"):
            self.check()

    def test_changed_web_or_a_second_web_owner_fails(self):
        path = self.root / "web/gpt" / f"{TLM}.md"
        path.write_text("unreviewed installed web")
        with self.assertRaisesRegex(ValueError, "installed web"):
            self.check()
        shutil.copy(self.root / "build/web/gpt" / f"{TLM}.md", path)
        path.with_name(path.stem + "-homily.md").write_text("second authority")
        with self.assertRaisesRegex(ValueError, "separate web prose"):
            self.check()


if __name__ == "__main__":
    unittest.main()
