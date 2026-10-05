"""The research seal retains evidence for a link, distinct from a dated event."""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _chronology as core
import _proper_chronology as proper
import _proper_study as study

DOCUMENT = "liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost"
SOURCE = "passage.george-leo-haydock.douay-rheims-with-haydock-commentary.2014-loreto-feeney-memorial.psalm-118-attribution-and-occasions"
PASSAGE = "src/sources/works/george-leo-haydock/douay-rheims-with-haydock-commentary/editions/2014-loreto-feeney-memorial/passages/psalm-118-attribution-and-occasions.toml"
PROFILE = "catholic-traditional-v1"


class BindingQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = core.load()
        cls.binding = next(b for b in cls.corpus.bindings if SOURCE in b.sources)
        cls.event = cls.corpus.events[cls.binding.event]

    def fixture(self, bindings, events=None):
        corpus = self.corpus._replace(bindings=tuple(bindings), units={},
                                      events=events or {self.event.id: self.event})
        index = {"Ps": ((), tuple(bindings), ())}
        return corpus, index

    def query(self, bindings, events=None, **options):
        corpus, index = self.fixture(bindings, events)
        with patch.object(core, "load", return_value=corpus), patch.object(core, "_by_book", return_value=index):
            return core.chronology("Ps.118.49", profile=PROFILE, **options)

    def test_actual_psalm_warrant_is_separate_from_david_date_sources(self):
        for verse in (1, 49, 50):
            answer = core.chronology(f"Ps.118.{verse}")
            claim = next(a for a in answer.assertions if a.relation == "traditional-attribution")
            self.assertEqual(claim.binding_sources, (SOURCE,))
            self.assertNotIn(SOURCE, claim.claim.sources)
            self.assertIn("corbett-david-usual-chronology", " ".join(claim.claim.sources))

    def test_normal_route_keeps_all_matches_and_excludes_other_scopes(self):
        other = self.binding._replace(scope=(core.Span("vulgate", "Ps", 117, None, None),),
                                      sources=("fixture.not-this-psalm",))
        second = self.binding._replace(sources=("fixture.second-warrant",))
        found = self.query((self.binding, second, other))
        sources = {s for a in found.assertions for s in a.binding_sources}
        self.assertEqual(sources, {SOURCE, "fixture.second-warrant"})

    def test_native_route_keeps_only_native_matching_link_evidence(self):
        native = self.binding._replace(scope=(core.Span("greek", "Ps", 118, 49, 50),),
                                       sources=("fixture.native-warrant",))
        wrong = native._replace(scope=(core.Span("greek", "Ps", 118, 1, 2),),
                                sources=("fixture.wrong-native-verses",))
        corpus, _ = self.fixture((self.binding, native, wrong))
        found = core._native_assertions(corpus, core.Locus("greek", "Ps", 118, 49), (PROFILE,))
        self.assertEqual({s for a in found for s in a.binding_sources}, {"fixture.native-warrant"})

    def test_broad_psalm_route_excludes_verse_scoped_warrants(self):
        narrow = self.binding._replace(scope=(core.Span("vulgate", "Ps", 118, 49, 50),),
                                       sources=("fixture.unsafe-verse-warrant",))
        corpus, index = self.fixture((self.binding, narrow))
        with patch.object(core, "_by_book", return_value=index):
            found = core._broad_preferred_assertions(corpus, core.Locus("vulgate", "Ps", 118, 999), (PROFILE,), None)
        self.assertEqual({s for a in found for s in a.binding_sources}, {SOURCE})

    def test_profile_and_answerability_filters_do_not_leak_binding_evidence(self):
        claim = self.event.claims[0]
        for excluded in (claim._replace(answerability="preserved"),
                         claim._replace(profile="catholic-critical-v1")):
            event = self.event._replace(claims=(excluded,))
            found = self.query((self.binding,), {event.id: event})
            self.assertEqual(found.assertions, ())
        preserved = self.event._replace(claims=(claim._replace(answerability="preserved"),))
        evidence = self.query((self.binding,), {preserved.id: preserved}, evidence=True)
        self.assertEqual(evidence.assertions[0].binding_sources, (SOURCE,))
        self.assertEqual(evidence.assertions[0].claim.answerability, "preserved")

    def test_shared_native_dedup_retains_both_warrants_without_extra_assertion(self):
        assertion = next(a for a in core.chronology("Ps.118.49").assertions
                         if a.relation == "traditional-attribution")
        native = assertion._replace(scope="Ps.118.49-50", binding_sources=("fixture.native-warrant",))
        shared = [assertion]
        core._merge_native_assertions(shared, (native,))
        self.assertEqual(len(shared), 1)
        self.assertEqual(shared[0].binding_sources, tuple(sorted((SOURCE, "fixture.native-warrant"))))
        self.assertEqual(shared[0].claim, assertion.claim)
        # Native-only routes were never deduplicated by the existing contract.
        empty = []
        core._merge_native_assertions(empty, (native, native._replace(scope="Ps.118")))
        self.assertEqual(len(empty), 2)


class BindingAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.found = proper.dossier(DOCUMENT, provider="gpt")
        cls.claim = next(c for c in cls.found.element("communion").claims
                         if c.relation == "traditional-attribution")

    def test_aggregation_unions_warrants_without_changing_date_identity(self):
        first = self.claim._replace(binding_sources=("fixture.first",))
        second = self.claim._replace(binding_sources=("fixture.second",))
        self.assertEqual(first.identity_key(), second.identity_key())
        answers = [("Ps.118.49", "attribution-only", "", [first]),
                   ("Ps.118.50", "attribution-only", "", [second])]
        common, status, _ = proper._common_claims(answers)
        self.assertNotEqual(status, proper.NONUNIFORM)
        self.assertEqual(len(common), 1)
        self.assertEqual(common[0].binding_sources, ("fixture.first", "fixture.second"))
        self.assertEqual(common[0].sources, self.claim.sources)
        # A mixed appointment keeps its audit-only warrant without promoting
        # that assertion to its common Date cell.
        answers[1] = ("Dan.3.29", "research-pending", "", [])
        self.assertEqual(proper._common_claims(answers)[0], ())
        self.assertEqual(proper._all_claims(answers)[0].binding_sources, ("fixture.first",))

    def test_absence_compatibility_and_reader_record_bytes_are_unchanged(self):
        assertion = next(a for a in core.chronology("Ps.118.49").assertions
                         if a.relation == "traditional-attribution")
        fields = assertion._asdict()
        del fields["binding_sources"]
        self.assertEqual(proper._assertion_claim(SimpleNamespace(**fields), "Ps.118.49").binding_sources, ())
        altered = self.found._replace(elements=tuple(e._replace(
            claims=tuple(c._replace(binding_sources=("fixture.changed-warrant",)) for c in e.claims),
            publication_claims=tuple(c._replace(binding_sources=("fixture.changed-warrant",)) for c in e.publication_claims))
            for e in self.found.elements))
        # Context parents also retain their matching internal metadata.
        altered = altered._replace(anchor_contexts=tuple(context._replace(
            parent=context.parent._replace(binding_sources=("fixture.changed-warrant",)))
            for context in altered.anchor_contexts))
        self.assertEqual(proper.render(self.found), proper.render(altered))
        self.assertEqual(proper.render_annotations_tex(proper.annotations(self.found)),
                         proper.render_annotations_tex(proper.annotations(altered)))


class BindingSealTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.traced = proper.computation_reads(DOCUMENT, ROOT, "gpt")

    def test_actual_trace_includes_warrant_and_ancestry(self):
        self.assertIn(SOURCE, self.traced["sources"])
        evidence = study.source_evidence(ROOT, self.traced["sources"], "chronology source")
        self.assertIn(ROOT / PASSAGE, evidence)
        owner = (ROOT / PASSAGE).parent.parent
        self.assertIn(owner / "edition.toml", evidence)
        self.assertTrue(any(p.name == "artifact.toml" and p.is_relative_to(owner)
                            for p in evidence))

    def test_binding_only_source_changes_invalidate_the_research_seal(self):
        scratch = ROOT / ".scratch/test-chronology-binding-sources"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temp:
            root = Path(temp)
            for source in study.source_evidence(ROOT, [SOURCE]):
                destination = root / source.relative_to(ROOT)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            leaf = root / "src/gpt" / DOCUMENT
            research = leaf / "research"
            research.mkdir(parents=True)
            for name in ("context.md", "scope.md", "interpretations.md",
                         "chronology.toml", "chronology-annotations.tex"):
                (research / name).write_text("unchanged fixture input\n")
            (research / "source-bindings.toml").write_text("bindings = []\n")
            (research / "review-dependencies.toml").write_text("paths = []\n")
            # The tested automatic trace supplies this ID. Narrow the fixture
            # to its source closure so no actual leaf or source is modified.
            ids = [s for s in self.traced["sources"] if s == SOURCE]
            with patch.object(study, "chronology_reads", return_value=(set(), {}, ids)), \
                 patch.object(study, "chronology_computation_inputs", return_value={}):
                before = study.review_inputs(root, "gpt", DOCUMENT, "research",
                                             review_contract="proper-study-v4")
                self.assertIn(PASSAGE, before["files"])
                path = root / PASSAGE
                path.write_text(path.read_text() + "\n# Evidence-only revision.\n")
                after = study.review_inputs(root, "gpt", DOCUMENT, "research",
                                            review_contract="proper-study-v4")
            self.assertEqual(set(before["files"]), set(after["files"]))
            self.assertEqual([name for name in before["files"]
                              if before["files"][name] != after["files"][name]], [PASSAGE])


if __name__ == "__main__":
    unittest.main()
