"""The research seal covers what a chronology answer is computed from.

Under the `proper-study-v3` seal contract the research review sealed the
chronology computation's code and nothing the code read. The Claude
postconciliar Twenty-fifth Sunday run spent two review cycles on that: 153
verse files the computation opened were undeclared, and then none of the nine
sources its chronology record cites had a file in the seal. `proper-study-v4`
reads the inputs off the computation itself, so these tests run it rather than
restating what it opens.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools.tests.test_proper_components_v2 import ROOT
import _proper_chronology
import _proper_study as study

NINETEENTH = "liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost"
TWENTY_FIFTH = ("liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/"
                "propers/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a")
CORPUS = tuple(f"src/sources/chronology/{name}.yaml"
               for name in ("bindings", "composition", "events", "gaps", "profiles"))


class ComputationReadsTests(unittest.TestCase):
    """What the trace reports for real leaves, from the installed computation."""

    @classmethod
    def setUpClass(cls):
        # Warm the calendar parse cache in this process first: with it warm the
        # computation would open a JSON copy under build/ instead of the
        # calendar, and the trace must report the calendar regardless.
        _proper_chronology.dossier(NINETEENTH, provider="gpt")
        cls.nineteenth = _proper_chronology.computation_reads(NINETEENTH, ROOT, "gpt")
        cls.twenty_fifth = _proper_chronology.computation_reads(TWENTY_FIFTH, ROOT, "claude")

    def test_the_calendar_corpus_and_verse_files_are_reported(self):
        reads = set(self.nineteenth["reads"])
        self.assertIn("src/sources/calendars/roman-1962/propers.yaml", reads)
        self.assertTrue(set(CORPUS) <= reads)
        # The verse counts that close an open citation, and the concordance
        # editions behind the Psalter conversions: about 1,500 files.
        self.assertGreater(
            sum(name.startswith("src/sources/bibles/clementine-vulgate/") for name in reads), 1000)
        self.assertTrue(any(name.startswith("src/sources/works/") for name in reads))

    def test_no_cache_copy_and_no_code_is_reported_as_data(self):
        for traced in (self.nineteenth, self.twenty_fifth):
            for name in traced["reads"]:
                with self.subTest(name=name):
                    self.assertFalse(name.startswith("build/"))
                    self.assertNotIn("__pycache__", name)
                    self.assertFalse(name.endswith((".py", ".pyc")))
                    self.assertFalse(name.startswith(("scripts/", "tools/")))

    def test_the_named_computation_inputs_cover_every_module_compiled(self):
        """The v3 seal's hand list is still complete; v4 seals the trace either way."""
        self.assertIn("scripts/_chronology.py", self.nineteenth["modules"])
        self.assertTrue(set(self.nineteenth["modules"]) <= set(study.CHRONOLOGY_COMPUTATION_INPUTS))
        self.assertIn("tools/citations", self.twenty_fifth["modules"])
        self.assertTrue(set(self.twenty_fifth["modules"]) <= set(
            study.CHRONOLOGY_COMPUTATION_INPUTS + study.POSTCONCILIAR_CHRONOLOGY_INPUTS))

    def test_the_postconciliar_adapter_inputs_are_reported(self):
        reads = set(self.twenty_fifth["reads"])
        edition = "src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/propers"
        self.assertIn(f"{edition}/temporal/shared/ordinary-time/weeks/25/propers/verified.md", reads)
        self.assertIn(f"{edition}/registry/formula-dispositions.md", reads)
        self.assertIn("guidance/liturgy/postconciliar-propers-registry.md", reads)

    def test_cited_sources_are_exactly_what_the_record_cites(self):
        # The trace describes today's computation. A historical leaf may keep
        # its reviewed snapshot while a corpus change awaits consumer rereview;
        # its freshness gate is separate from this source-completeness check.
        record = tomllib.loads(_proper_chronology.render(
            _proper_chronology.dossier(TWENTY_FIFTH, provider="claude")))
        cited = {source
                 for holder in (*record.get("elements", []), *record.get("profile_comparisons", []))
                 for claim in holder.get("claims", [])
                 for source in claim.get("sources", [])}
        library = {source for source in cited if not source.startswith("bible")}
        self.assertEqual(set(self.twenty_fifth["sources"]), library)
        self.assertTrue(any(source.startswith("artifact.catholic-encyclopedia")
                            for source in library))

    def test_a_derived_copy_under_build_is_refused_not_reported(self):
        scratch = ROOT / "build" / "proper-chronology-reads-test"
        scratch.mkdir(parents=True, exist_ok=True)
        self.addCleanup(shutil.rmtree, scratch, ignore_errors=True)
        copy = scratch / "propers.json"
        copy.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(_proper_chronology.ChronologyWiringError,
                                    "derived copy under build/"):
            _proper_chronology._traced(str(ROOT), NINETEENTH, "gpt", [str(copy)], [])


class InterpreterBoundaryTests(unittest.TestCase):
    def test_a_virtualenv_inside_the_checkout_is_not_repository_evidence(self):
        scratch = ROOT / ".scratch/pagination-contract"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            root = Path(temporary)
            interpreter = root / ".scratch/venv"
            package = interpreter / "lib/python/site-packages/yaml"
            compiled = package / "loader.py"
            loaded = package / "_yaml.so"
            data = package / "data.json"
            repository = root / "scripts/computation.py"
            for path in (compiled, loaded, data, repository):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture")
            found = SimpleNamespace(elements=[], profile_comparisons=[])
            with (patch.object(sys, "prefix", str(interpreter)),
                  patch.dict(sys.modules, {
                      "chronology_test_extension": SimpleNamespace(__file__=str(loaded)),
                  }),
                  patch.object(_proper_chronology, "dossier", return_value=found),
                  patch.object(_proper_chronology, "render"),
                  patch.object(_proper_chronology, "annotations"),
                  patch.object(_proper_chronology, "render_annotations_tex")):
                traced = _proper_chronology._traced(
                    str(root), NINETEENTH, "gpt",
                    [str(compiled), str(loaded), str(data), str(repository)],
                    [str(compiled), str(repository)],
                )
            self.assertEqual(traced["modules"], ["scripts/computation.py"])
            self.assertEqual(traced["reads"], [])


class RealLeafSealTests(unittest.TestCase):
    """The v4 seal of a published leaf, against its v3 seal."""

    def test_v4_adds_reads_and_cited_sources_and_keeps_everything_v3_sealed(self):
        v3 = study.review_inputs(ROOT, "gpt", NINETEENTH, "research",
                                 review_contract=study.RESEARCH_REVIEW_CONTRACT)
        v4 = study.review_inputs(ROOT, "gpt", NINETEENTH, "research",
                                 review_contract=study.CHRONOLOGY_READS_CONTRACT)
        self.assertEqual(v4["review_contract"], "proper-study-v4")
        for name, value in v3["files"].items():
            self.assertEqual(v4["files"].get(name), value, name)
        traced = _proper_chronology.computation_reads(NINETEENTH, ROOT, "gpt")
        for name in traced["reads"]:
            if not name.startswith(f"src/gpt/{NINETEENTH}/"):
                self.assertIn(name, v4["files"])
        for path in study.source_evidence(ROOT, traced["sources"]):
            self.assertIn(path.relative_to(ROOT).as_posix(), v4["files"])
        self.assertEqual(v4["chronology_cited_sources"], traced["sources"])
        # This leaf declared none of them by hand, and v3 sealed none of them.
        self.assertGreater(len(set(v4["files"]) - set(v3["files"])), 1000)

    def test_the_component_manifest_is_never_research_evidence(self):
        sealed = study.review_inputs(ROOT, "claude", TWENTY_FIFTH, "research",
                                     review_contract=study.CHRONOLOGY_READS_CONTRACT)
        self.assertNotIn(f"src/claude/{TWENTY_FIFTH}/proper-components.toml", sealed["files"])
        self.assertIn("src/sources/chronology/events.yaml", sealed["files"])


class SealCompositionTests(unittest.TestCase):
    """How the seal treats what the trace reports, on a fixture leaf."""

    def setUp(self):
        scratch = ROOT / ".scratch/pagination-contract"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.document = NINETEENTH
        self.leaf = self.root / "src/gpt" / self.document
        (self.leaf / "research").mkdir(parents=True)
        for name in ("context.md", "scope.md", "interpretations.md"):
            (self.leaf / "research" / name).write_text("Checked fixture evidence.")
        (self.leaf / "research/source-bindings.toml").write_text("bindings = []\n")
        (self.leaf / "research/review-dependencies.toml").write_text("paths = []\n")
        (self.leaf / "research/chronology.toml").write_text('date = "A.D. 60"\n')
        (self.leaf / "research/chronology-annotations.tex").write_text("Generated dates.")
        for name in study.CHRONOLOGY_COMPUTATION_INPUTS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Computation fixture: " + name)
        self.corpus = self.root / "src/sources/chronology/events.yaml"
        self.chapter = self.root / "src/sources/bibles/douay-rheims/chapters/Jer/25.json"
        self.module = self.root / "scripts/_new_dependency.py"
        for path in (self.corpus, self.chapter, self.module):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Original bytes.")
        (self.leaf / "proper-components.toml").write_text("schema = 2\n")
        self.trace = {
            "reads": ["src/sources/chronology/events.yaml",
                      f"src/gpt/{self.document}/research/chronology.toml",
                      f"src/gpt/{self.document}/proper-components.toml"],
            "modules": ["scripts/_chronology.py", "scripts/_new_dependency.py"],
            "sources": [],
            "source_files": ["src/sources/bibles/douay-rheims/chapters/Jer/25.json"],
        }

    def seal(self, contract=study.CHRONOLOGY_READS_CONTRACT):
        with patch.object(_proper_chronology, "computation_reads",
                          return_value=json.loads(json.dumps(self.trace))):
            return study.review_inputs(self.root, "gpt", self.document, "research",
                                       review_contract=contract)

    def test_reads_cited_chapters_and_extra_modules_enter_the_seal(self):
        sealed = self.seal()
        self.assertIn("src/sources/chronology/events.yaml", sealed["files"])
        self.assertIn("src/sources/bibles/douay-rheims/chapters/Jer/25.json", sealed["files"])
        self.assertIn("scripts/_new_dependency.py", sealed["chronology_computation_inputs"])
        self.assertEqual(sealed["chronology_cited_sources"], [])
        for path in (self.corpus, self.chapter, self.module):
            before = self.seal()
            path.write_text("Changed bytes.")
            with self.subTest(path=path.name):
                self.assertNotEqual(self.seal(), before)

    def test_v3_is_unchanged_by_anything_the_trace_reports(self):
        before = self.seal(study.RESEARCH_REVIEW_CONTRACT)
        self.assertNotIn("chronology_cited_sources", before)
        for path in (self.corpus, self.chapter, self.module):
            path.write_text("Changed bytes.")
        self.assertEqual(self.seal(study.RESEARCH_REVIEW_CONTRACT), before)

    def test_leaf_reads_follow_the_leaf_rule(self):
        sealed = self.seal()
        self.assertNotIn(f"src/gpt/{self.document}/proper-components.toml", sealed["files"])
        before = sealed
        (self.leaf / "proper-components.toml").write_text('schema = 2\npresentation = "later"\n')
        self.assertEqual(self.seal(), before)
        (self.leaf / "notes.md").write_text("A leaf file outside the rule.")
        self.trace["reads"].append(f"src/gpt/{self.document}/notes.md")
        with self.assertRaisesRegex(ValueError, "does not cover"):
            self.seal()

    def test_an_unregistered_cited_source_fails_closed(self):
        self.trace["sources"] = ["artifact.not-in-this-library"]
        with self.assertRaisesRegex(ValueError, "unregistered chronology source"):
            self.seal()

    def test_the_current_pipeline_selects_v4_for_research_review_only(self):
        pipeline = json.loads((ROOT / "workflows/pipelines/proper-study.json").read_text())
        selected = [stage["id"] for stage in pipeline["stages"]
                    if "--review-contract proper-study-v4" in stage.get("review_input_command", "")]
        self.assertEqual(selected, ["research-review"])
        with self.assertRaisesRegex(ValueError, "only to research"):
            study.review_inputs(self.root, "gpt", self.document, "study",
                                review_contract=study.CHRONOLOGY_READS_CONTRACT)


if __name__ == "__main__":
    unittest.main()
