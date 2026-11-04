"""Regression checks over the real course source hierarchy and typed selections."""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _document_schema as schemas
from document_schema_checks import curriculum

COURSE = Path("curriculums/ecclesiastical-latin")
PACKET = COURSE / "01-foundations/01-form-case-and-agreement"


class CurriculumSchemaTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/schema-lit-checks"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.owner = self.root / "src/gpt" / COURSE
        shutil.copytree(ROOT / "src/gpt" / COURSE, self.owner)
        self.leaf = self.root / "src/gpt" / PACKET
        self.record = self.publication(PACKET)

    def publication(self, leaf):
        manifest = schemas.adapter_manifest(self.root, self.root / "src/gpt" / leaf)
        return schemas._normalise(self.root, manifest, None)

    def errors(self):
        return "\n".join(curriculum.check(self.root, self.record))

    def test_real_source_registry_and_six_part_skeleton_pass_without_pdfs(self):
        self.assertEqual(self.errors(), "")

    def test_deleting_a_required_part_is_refused(self):
        path = self.leaf / "main.tex"
        path.write_text(path.read_text().replace(r"\part{Reading and Composition}", ""))
        self.assertIn("six canonical Parts", self.errors())

    def test_detaching_a_leaf_from_its_document_type_is_refused(self):
        path = self.leaf / "publication.toml"
        text = path.read_text()
        path.write_text(text[:text.index("[document]")])
        self.assertIn("must declare [document] type curriculum-packet-v<N>", self.errors())

    def test_detaching_a_leaf_from_its_module_selection_is_refused(self):
        path = self.leaf / "main.tex"
        path.write_text(path.read_text().replace("\\input{" + PACKET.as_posix() + "/module-data}", ""))
        self.assertIn("module selection exactly once", self.errors())

    def test_answers_cannot_consume_a_different_existing_exercise_source(self):
        path = self.leaf / "main.tex"
        text = path.read_text()
        position = text.rfind(r"\input{\ModuleExerciseSource}")
        text = text[:position] + text[position:].replace(r"\input{\ModuleExerciseSource}", r"\input{\ModuleLessonSource}", 1)
        path.write_text(text)
        self.assertIn("Answers and Models must render the same authoritative exercise source", self.errors())

    def test_four_variants_are_not_just_a_nonempty_selection(self):
        path = self.leaf / "module-data.tex"
        path.write_text(path.read_text().replace(r"\ModuleWorksheetVariants}{A,B,C,D}", r"\ModuleWorksheetVariants}{A,B,C}"))
        self.assertIn("A,B,C,D", self.errors())

    def test_a_lesson_source_must_define_the_selected_stable_lessons(self):
        path = self.owner / "shared/content/volume1/all.tex"
        path.write_text(path.read_text().replace(r"\begin{courseunit}{I.2}", r"\begin{courseunit}{I.99}", 1))
        self.assertIn("courseunit I.2", self.errors())

    def test_duplicate_worksheet_id_is_refused(self):
        path = self.owner / "shared/exercises/volume1/all.tex"
        path.write_text(path.read_text().replace(r"\begin{worksheet}{I.2}{B}", r"\begin{worksheet}{I.1}{B}", 1))
        self.assertIn("repeats worksheet ID I.1", self.errors())

    def test_an_empty_closed_answer_is_refused(self):
        path = self.owner / "shared/exercises/volume1/all.tex"
        text = path.read_text()
        from document_schema_checks.liturgy import _calls
        args, start, end = next(_calls(text, "Exercise", 2))
        text = text[:start] + "\\Exercise{" + args[0] + "}{}" + text[end:]
        path.write_text(text)
        self.assertIn("prompt and matching answer/model", self.errors())

    def test_main_cannot_substitute_for_the_module_selection_role(self):
        for item in self.record["structure"]:
            if item["role"] == "module-selection":
                item["source"] = "main.tex"
                item.pop("data", None)
        self.assertIn("module-selection must name", self.errors())

    def test_changed_shared_source_invalidates_a_previously_passing_audit(self):
        self.assertEqual(self.errors(), "")
        path = self.owner / "shared/exercises/volume1/all.tex"
        path.write_text(path.read_text().replace(r"\begin{worksheet}{I.2}{B}", r"\begin{worksheet}{I.1}{B}", 1))
        self.assertIn("repeats worksheet ID", self.errors())

    def test_assessment_task_and_answer_selections_share_one_owner(self):
        self.record = self.publication(COURSE / "05-stage-assessments/01-foundations")
        self.assertEqual(self.errors(), "")
        path = self.owner / "05-stage-assessments/01-foundations/main.tex"
        text = path.read_text()
        position = text.rfind(r"\SelectAssessments{\AssessmentSelection}")
        text = text[:position] + text[position:].replace(r"\SelectAssessments{\AssessmentSelection}", r"\SelectAssessments{C-A,C-B}", 1)
        path.write_text(text)
        self.assertIn("same canonical review IDs", self.errors())

    def test_review_answer_mode_must_precede_the_source_rendering(self):
        self.record = self.publication(COURSE / "05-stage-assessments/01-foundations")
        path = self.owner / "05-stage-assessments/01-foundations/main.tex"
        path.write_text(path.read_text().replace(r"\solutionstrue", r"\solutionsfalse"))
        self.assertIn("select its solution mode before rendering", self.errors())


if __name__ == "__main__":
    unittest.main()
