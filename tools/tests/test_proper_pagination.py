"""Physical pagination, source ownership, and historical-contract isolation."""
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools.tests.test_proper_components_v2 import ROOT, components, fixture, load, save
import _proper_study as study


class PaginationTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/pagination-contract"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.data, self.path, self.provider = fixture(self.root)
        self.leaf = self.path.parent
        self.data["presentation_contract"] = components.PRESENTATION_CONTRACT
        self.data["presentation"] = {role: role for role in components.PRESENTATION_ROLES}
        self.data["presentation"]["commentary"] = "integrated"
        for role in components.PRESENTATION_ROLES[:-1]:
            self.data["components"].insert(0, dict(
                key=role, kind="front-matter", modes=["synthesis"], path=role + ".tex",
                element_keys=self.data["element_keys"], references=[]))
        for role, names in components.MARKERS.items():
            key = self.data["presentation"][role]
            body = "\n".join("\\zlabel{" + components.MARKER_PREFIX + label + "}\nText."
                             for label in names)
            (self.leaf / (key + ".tex")).write_text(body)
        chronology = next(item for item in self.data["components"] if item["key"] == "chronology")
        chronology["references"] = ["research/chronology-annotations.tex"]
        (self.leaf / "research").mkdir(exist_ok=True)
        (self.leaf / chronology["references"][0]).write_text("% Generated annotation fixture.\n")
        path = self.leaf / "chronology.tex"
        end = "\\zlabel{triptych:concise:chronology:end}"
        path.write_text(path.read_text().replace(end,
                        "\\input{proper/research/chronology-annotations}\n"
                        "\\chronodate{gospel}{\\chronologyannotation{gospel}}\n" + end))
        self.entry = self.leaf / "synthesis.tex"
        self.entry.write_text("\n".join("\\input{proper/" + self.data["presentation"][role] + "}"
                                       for role in components.PRESENTATION_ROLES)
                              + "\n\\input{proper/terminal}\n")
        self.build = self.root / "build/gpt"
        self.build.mkdir(parents=True)
        for mode in components.MODES:
            base = self.build / self.data["outputs"][mode]
            base.with_suffix(".pdf").write_bytes(b"%PDF-1.7\nfixture")
            base.with_suffix(".log").write_text("Settled fixture log.\n")
            base.with_suffix(".aux").write_text(self.aux())
            base.with_suffix(".fls").write_text("INPUT " + str(self.leaf / components.ENTRYPOINTS[mode]))
        self.save()

    def save(self):
        data = copy.deepcopy(self.data)
        mapping = data.pop("presentation", None)
        save(data, self.path)
        if mapping is not None:
            self.path.write_text(self.path.read_text() + "\n[presentation]\n" + "\n".join(
                key + " = " + json.dumps(value) for key, value in mapping.items()) + "\n")

    def aux(self):
        return "\n".join("\\zref@newlabel{" + components.MARKER_PREFIX + label
                         + "}{\\default{}\\page{99}\\abspage{" + str(page) + "}}"
                         for group in components.MARKERS.values() for label, page in group.items())

    def audit(self, **kwargs):
        components.audit_v2(self.data, self.path, self.provider, **kwargs)

    def artifacts(self, research=20, synthesis=10):
        def pdfinfo(arguments, **kwargs):
            pages = synthesis if "synthesis" in arguments[1] else research
            return subprocess.CompletedProcess(arguments, 0, f"Pages: {pages}\n", "")
        with patch.object(components.subprocess, "run", side_effect=pdfinfo):
            self.audit(phase="artifacts", build_root=self.build)

    def test_source_contract_and_physical_ranges(self):
        self.audit()
        self.artifacts()
        self.artifacts(research=50, synthesis=12)

    def test_outside_page_ranges_fails(self):
        for values in ({"research": 19}, {"research": 51}, {"synthesis": 9}, {"synthesis": 13}):
            with self.subTest(values=values), self.assertRaisesRegex(ValueError, "physical pages"):
                self.artifacts(**values)

    def test_misplaced_missing_duplicate_and_unresolved_physical_markers_fail(self):
        aux = self.build / "proper-synthesis.aux"
        original = self.aux()
        variants = [original.replace("\\abspage{3}", "\\abspage{4}"),
                    original.replace("\\abspage{1}", "\\abspage{2}"),
                    "\n".join(original.splitlines()[1:]),
                    original + "\n" + original.splitlines()[0],
                    original.replace("\\abspage{5}", "\\abspage{0}"),
                    original.replace("\\abspage{5}", "\\abspage{??}")]
        for value in variants:
            aux.write_text(value)
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "marker|physical page"):
                self.artifacts()

    def test_unsettled_log_and_missing_aux_fail(self):
        log = self.build / "proper-synthesis.log"
        for warning in ("LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.",
                        "LaTeX Warning: There were undefined references."):
            log.write_text(warning)
            with self.assertRaisesRegex(ValueError, "settled"):
                self.artifacts()
        log.write_text("Package: rerunfilecheck loaded\n")
        self.artifacts()
        (self.build / "proper-synthesis.aux").unlink()
        with self.assertRaises(OSError):
            self.artifacts()

    def test_marker_cannot_move_to_another_source_owner(self):
        inventory = self.leaf / "inventory.tex"
        label = "\\zlabel{triptych:concise:inventory:start}"
        inventory.write_text(inventory.read_text().replace(label, ""))
        self.entry.write_text(label + self.entry.read_text())
        with self.assertRaisesRegex(ValueError, "owner|missing"):
            self.audit()

    def test_reordered_and_repeated_imports_fail(self):
        original = self.entry.read_text()
        for value in (original.replace("proper/inventory", "proper/TEMP")
                      .replace("proper/overview", "proper/inventory").replace("proper/TEMP", "proper/overview"),
                      original + "\n\\input{proper/inventory}\n"):
            self.entry.write_text(value)
            with self.assertRaisesRegex(ValueError, "include order"):
                self.audit()

    def test_missing_sense_marker_and_incomplete_inventory_fail(self):
        overview = self.leaf / "overview.tex"
        overview.write_text(overview.read_text().replace("\\zlabel{triptych:concise:sense:moral}", ""))
        with self.assertRaisesRegex(ValueError, "markers"):
            self.audit()
        next(item for item in self.data["components"] if item["key"] == "inventory")["element_keys"] = ["gospel"]
        with self.assertRaisesRegex(ValueError, "every appointed"):
            self.audit()

    def test_chronology_must_use_its_canonical_owner_and_generated_cells(self):
        path = self.leaf / "chronology.tex"
        original = path.read_text()
        for value in (original.replace("\\input{proper/research/chronology-annotations}", ""),
                      original.replace("\\chronologyannotation{gospel}", "Invented date")):
            path.write_text(value)
            with self.assertRaisesRegex(ValueError, "import canonical|generated annotations"):
                self.audit()
        path.write_text(original)
        cell = "\\chronodate{gospel}{\\chronologyannotation{gospel}}"
        path.write_text(original.replace(cell, "") + cell)
        with self.assertRaisesRegex(ValueError, "between their physical"):
            self.audit()
        path.write_text(original)
        self.entry.write_text(self.entry.read_text() + "\\chronodate{gospel}{Date}\n")
        with self.assertRaisesRegex(ValueError, "sole page-two"):
            self.audit()

    def test_duplicate_direct_and_indirect_annotation_imports_fail_source_and_artifact_gates(self):
        chronology = self.leaf / "chronology.tex"
        original = chronology.read_text()
        duplicate = "\\input{proper/research/chronology-annotations}\n"
        indirect = self.leaf / "research/indirect.tex"
        indirect.write_text(duplicate)
        owner = next(item for item in self.data["components"] if item["key"] == "chronology")
        owner["references"].append("research/indirect.tex")
        for value in (duplicate, "\\input{proper/research/indirect}\n"):
            chronology.write_text(original + value)
            for phase in ("content", "artifacts"):
                with self.subTest(value=value, phase=phase), self.assertRaisesRegex(ValueError, "annotations exactly once"):
                    self.audit(phase=phase, build_root=self.build)

    def test_chronology_can_also_have_a_research_home(self):
        next(item for item in self.data["components"] if item["key"] == "chronology")["modes"].append("research")
        path = self.leaf / "main.tex"
        path.write_text(path.read_text() + "\n\\input{proper/chronology}\n")
        self.audit()

    def test_unknown_contract_and_incomplete_or_reused_role_mappings_fail(self):
        original = copy.deepcopy(self.data)
        for mutation in (lambda: self.data.update(presentation_contract="unknown"),
                         lambda: self.data["presentation"].pop("themes"),
                         lambda: self.data["presentation"].update(themes="overview")):
            self.data = copy.deepcopy(original)
            mutation()
            with self.assertRaises(ValueError):
                self.audit(phase="scope")

    def test_historical_schema_two_and_explicit_v3_requirement(self):
        self.data.pop("presentation_contract")
        self.data.pop("presentation")
        self.audit()
        self.assertFalse(components.presentation_contract(self.data))
        with self.assertRaisesRegex(ValueError, "presentation_contract"):
            components.presentation_contract(self.data, required=True)
        self.save()
        with patch.object(study, "scope"), self.assertRaisesRegex(ValueError, "presentation_contract"):
            study.check(self.root, "gpt", "proper", "content", "research", require_presentation=True)

    def test_v3_pipeline_requires_contract_in_all_content_and_terminal_gates(self):
        pipeline = json.loads((ROOT / "workflows/pipelines/proper-study.json").read_text())
        self.assertGreaterEqual(pipeline["version"], 3)
        gates = [check["command"] for stage in pipeline["stages"] for check in stage.get("checks", [])
                 if "scripts/_proper_study.py check" in check["command"]
                 and any("--phase " + name in check["command"] for name in ("content", "artifacts", "publication"))]
        self.assertEqual(len(gates), 5)
        self.assertTrue(all("--require-presentation" in command for command in gates))

    def test_aux_and_log_are_bound_into_visual_snapshot(self):
        before = study.artifact_state(self.root, "gpt", "proper")
        self.assertEqual(len(before["pagination_evidence"]), 4)
        path = self.build / "proper-synthesis.aux"
        path.write_text(path.read_text() + "\nChanged build evidence")
        self.assertNotEqual(before, study.artifact_state(self.root, "gpt", "proper"))

    def test_child_aux_labels_are_checked_and_every_child_byte_is_sealed(self):
        aux = self.build / "proper-synthesis.aux"
        child = self.build / "chapter.aux"
        child.write_text(aux.read_text())
        aux.write_text("\\@input{chapter.aux}\n")
        self.artifacts()
        before = study.artifact_state(self.root, "gpt", "proper")
        self.assertIn("build/gpt/chapter.aux", before["pagination_evidence"])
        child.write_text(child.read_text().replace("\\abspage{2}", "\\abspage{3}"))
        self.assertNotEqual(before, study.artifact_state(self.root, "gpt", "proper"))
        with self.assertRaisesRegex(ValueError, "physical page 2"):
            self.artifacts()

    def test_unsafe_duplicate_cyclic_and_missing_aux_imports_fail_closed(self):
        aux = self.build / "proper-synthesis.aux"
        child = self.build / "chapter.aux"
        outside = self.root / "outside.aux"
        outside.write_text(self.aux())
        (self.build / "escape.aux").symlink_to(outside)
        cases = [("\\@input{../outside.aux}", self.aux()),
                 ("\\@input{" + str(outside) + "}", self.aux()),
                 ("\\@input{escape.aux}", self.aux()),
                 ("\\@input{chapter.aux}\\@input{chapter.aux}", self.aux()),
                 ("\\@input{chapter.aux}", "\\@input{proper-synthesis.aux}"),
                 ("\\@input{missing.aux}", self.aux()),
                 ("\\@input\\dynamic", self.aux())]
        for parent, nested in cases:
            aux.write_text(parent)
            child.write_text(nested)
            with self.subTest(parent=parent), self.assertRaises((OSError, ValueError)):
                self.artifacts()
            with self.subTest(parent=parent), self.assertRaises((OSError, ValueError)):
                study.artifact_state(self.root, "gpt", "proper")

    def test_opted_in_chronology_is_required_only_concise_has_complete_cell_discipline(self):
        preflight = load("check-content-preflight")
        self.assertEqual(preflight._chronology_scope(self.leaf, "synthesis")[:2], (True, True))
        self.assertEqual(preflight._chronology_scope(self.leaf, "research")[:2], (True, False))
        self.assertEqual(preflight._chronology_scope(self.leaf, "homily")[:2], (True, False))
        (self.leaf / "research/chronology-annotations.tex").unlink()
        self.assertTrue(preflight._annotations_scope(self.leaf)[0])

    def test_concise_chronology_rejects_omitted_and_duplicate_scriptural_cells(self):
        preflight = load("check-content-preflight")
        element = SimpleNamespace(key="gospel", loci=["Mt.1.1"], publication_claims=[])
        found = SimpleNamespace(state=preflight._wiring().APPOINTED, elements=[element],
                                element=lambda key: element if key == "gospel" else None)
        path = self.leaf / "chronology.tex"
        original = path.read_text()
        cell = "\\chronodate{gospel}{\\chronologyannotation{gospel}}"
        with patch.object(preflight, "_corpus_answer", return_value=found):
            self.assertEqual(preflight.check_chronology_claims_supported(
                self.leaf, self.root, "synthesis")[0], [])
            path.write_text(original.replace(cell, ""))
            problems, _ = preflight.check_chronology_claims_supported(self.leaf, self.root, "synthesis")
            self.assertTrue(any("no date cell" in problem for problem in problems), problems)
            path.write_text(original.replace(cell, cell + cell))
            problems, _ = preflight.check_chronology_claims_supported(self.leaf, self.root, "synthesis")
            self.assertTrue(any("more than one" in problem for problem in problems), problems)

    def test_leaf_chronology_checks_each_reading_experience_separately(self):
        preflight = load("check-content-preflight")
        element = SimpleNamespace(key="gospel", loci=["Matt.1.1"], publication_claims=[])
        found = SimpleNamespace(state=preflight._wiring().APPOINTED, elements=[element],
                                element=lambda key: element if key == "gospel" else None)
        cell = "\\chronodate{gospel}{\\chronologyannotation{gospel}}"
        # The expansive study can develop a separate historical appendix; its
        # cell is not a duplicate row on the concise physical page two.
        (self.leaf / "treatment.tex").write_text(cell)
        with patch.object(preflight, "_corpus_answer", return_value=found):
            for edition in ("research", "synthesis", "leaf"):
                with self.subTest(edition=edition):
                    problems, _ = preflight.check_chronology_claims_supported(
                        self.leaf, self.root, edition)
                    self.assertEqual(problems, [])
            # A research cell must not satisfy missing concise coverage.
            path = self.leaf / "chronology.tex"
            original = path.read_text()
            path.write_text(original.replace(cell, ""))
            problems, _ = preflight.check_chronology_claims_supported(self.leaf, self.root)
            self.assertTrue(any("no date cell" in problem for problem in problems), problems)
            # Duplicate cells inside the concise edition remain forbidden.
            path.write_text(original.replace(cell, cell + cell))
            problems, _ = preflight.check_chronology_claims_supported(self.leaf, self.root)
            self.assertTrue(any("more than one" in problem for problem in problems), problems)

    @unittest.skipUnless(shutil.which("pdflatex") and shutil.which("pdfinfo"), "requires TeX and Poppler")
    def test_real_pdf_uses_absolute_pages_even_after_printed_counter_reset(self):
        # Synthetic layout evidence only; these intentionally tiny bodies do not
        # claim substantive prose, typography, or production review acceptance.
        for mode, count in (("research", 20), ("synthesis", 10)):
            name = self.data["outputs"][mode]
            source = self.build / (name + ".tex")
            body = "\\documentclass{article}\n\\usepackage{zref-user,zref-abspage}\n\\begin{document}\n"
            for page in range(1, count + 1):
                page_body = "Physical fixture page.\\setcounter{page}{99}\n"
                if mode == "synthesis":
                    for group in components.MARKERS.values():
                        for label, expected in group.items():
                            if expected == page:
                                page_body += "\\zlabel{" + components.MARKER_PREFIX + label + "}\n"
                if mode == "synthesis" and page == 2:
                    (self.build / "chronology-page.tex").write_text(page_body)
                    body += "\\include{chronology-page}\n"
                else:
                    body += page_body
                if page < count:
                    body += "\\clearpage\n"
            source.write_text(body + "\\end{document}\n")
            for _ in range(3):
                result = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", source.name],
                                        cwd=self.build, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout[-2000:])
        components.presentation_artifacts(self.data, self.build, ("research", "synthesis"))


class ChronologyComputationSealTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/pagination-contract"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.document = ("liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/"
                         "propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a")
        self.leaf = self.root / "src/gpt" / self.document
        (self.leaf / "research").mkdir(parents=True)
        for name in ("context.md", "scope.md", "interpretations.md"):
            (self.leaf / "research" / name).write_text("Checked fixture evidence.")
        (self.leaf / "research/source-bindings.toml").write_text("bindings = []\n")
        self.owner = self.leaf.parent / "shared/ordinary-time/weeks/25/propers/verified.md"
        self.owner.parent.mkdir(parents=True)
        self.owner.write_text("Owning edition appointment witness.")
        registry = self.leaf.parents[1] / "registry/formula-dispositions.md"
        registry.parent.mkdir(parents=True)
        registry.write_text(
            "| Full publication slug | Canonical owner |\n"
            "| --- | --- |\n"
            "| `pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a` | "
            "[owner](../temporal/shared/ordinary-time/weeks/25/propers/verified.md) |\n"
        )
        (self.leaf / "research/review-dependencies.toml").write_text(
            "paths = [" + json.dumps(self.owner.relative_to(self.root).as_posix()) + "]\n")
        self.manifest = self.leaf / "proper-components.toml"
        self.manifest.write_text('schema = 2\n')
        for name in (*study.CHRONOLOGY_COMPUTATION_INPUTS, *study.POSTCONCILIAR_CHRONOLOGY_INPUTS):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Original computation fixture: " + name)

    def seal(self, contract=study.RESEARCH_REVIEW_CONTRACT):
        return study.review_inputs(self.root, "gpt", self.document, "research", review_contract=contract)

    def chronology(self):
        (self.leaf / "research/chronology.toml").write_text('date = "A.D. 60"\n')
        (self.leaf / "research/chronology-annotations.tex").write_text("Generated dates.")

    def test_all_historical_schema_two_seals_are_unchanged(self):
        for dated in (False, True):
            if dated:
                self.chronology()
            before = self.seal(contract=None)
            self.assertNotIn("chronology_computation_inputs", before)
            path = self.root / "scripts/_proper_chronology_inputs.py"
            path.write_text(path.read_text() + "\nNew adapter")
            self.assertEqual(self.seal(contract=None), before)

    def test_explicit_review_contract_binds_code_and_registry_before_manifest_exists(self):
        self.chronology()
        self.manifest.unlink()
        sealed = self.seal()
        self.assertEqual(set(sealed["chronology_computation_inputs"]),
                         set(study.CHRONOLOGY_COMPUTATION_INPUTS + study.POSTCONCILIAR_CHRONOLOGY_INPUTS))
        self.assertFalse(any(name.startswith("src/") for name in sealed["chronology_computation_inputs"]))
        # Presentation is authored after research; its bytes are not evidence.
        self.manifest.write_text('schema = 2\npresentation_contract = "interpretive-pagination-v1"\n'
                                 '[presentation]\nchronology = "revised-layout"\n')
        self.assertEqual(self.seal(), sealed)

    def test_adapter_query_parser_registry_and_source_drift_invalidate_without_date_changes(self):
        self.chronology()
        record = self.leaf / "research/chronology.toml"
        for name in ("scripts/_proper_chronology_inputs.py",
                     "scripts/_proper_chronology_comparisons.py",
                     "scripts/_chronology.py", "tools/citations",
                     "guidance/liturgy/postconciliar-propers-registry.md", self.owner.relative_to(self.root).as_posix()):
            before = self.seal()
            path = self.root / name
            path.write_text(path.read_text() + "\nChanged evidence or computation.")
            with self.subTest(name=name):
                self.assertNotEqual(before, self.seal())
                self.assertEqual(record.read_text(), 'date = "A.D. 60"\n')

    def test_v3_requires_both_generated_records_and_missing_code_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "canonical chronology input"):
            self.seal()
        self.chronology()
        self.assertIn("chronology_computation_inputs", self.seal())
        (self.root / "scripts/_proper_chronology_inputs.py").unlink()
        with self.assertRaises(OSError):
            self.seal()

    def test_only_current_pipeline_research_seal_selects_v3_contract(self):
        pipeline = json.loads((ROOT / "workflows/pipelines/proper-study.json").read_text())
        selected = [stage["id"] for stage in pipeline["stages"]
                    if "--review-contract proper-study-v3" in stage.get("review_input_command", "")]
        self.assertEqual(selected, ["research-review"])
        with self.assertRaisesRegex(ValueError, "only to research"):
            study.review_inputs(self.root, "gpt", self.document, "study", review_contract=study.RESEARCH_REVIEW_CONTRACT)

    def test_1962_computation_does_not_depend_on_opposite_family_adapter_or_registry(self):
        document = "liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost"
        leaf = self.root / "src/gpt" / document
        (leaf / "research").mkdir(parents=True)
        (leaf / "research/chronology.toml").write_text("Generated chronology fixture.")
        result = study.chronology_computation_inputs(self.root, "gpt", document)
        self.assertEqual(set(result), set(study.CHRONOLOGY_COMPUTATION_INPUTS))


if __name__ == "__main__":
    unittest.main()
