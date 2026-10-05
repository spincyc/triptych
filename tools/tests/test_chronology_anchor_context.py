"""An event anchor supplies qualified context, never an invented Psalm date."""
from __future__ import annotations

import argparse
import ast
import json
import sys
import tomllib
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _chronology as corpus
import _proper_chronology as proper
import chronology_review_diff as review
from tools.tests.test_chronology import load_tool
from tools.tests.test_content_preflight_study import StudyLeaf, PREFLIGHT
from tools.tests.test_proper_chronology_reads import resolved_binding_sources

TWENTIETH = "liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost"
FIFTEENTH = "liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost"
ANCHOR = "israel.exile.third-captivity"
PARENT = "israel.exile.psalm-136-captive-lament"


class AnchorQualificationReviewTests(unittest.TestCase):
    """A source limitation cannot disappear from either semantic review view."""

    @classmethod
    def setUpClass(cls):
        # Exercise the actual revision worker's serializer, including its
        # compatibility fallbacks, without running a second corpus loader.
        functions = [node for node in ast.parse(review.WORKER).body
                     if isinstance(node, ast.FunctionDef)]
        namespace = {}
        exec(compile(ast.Module(body=functions, type_ignores=[]),
                     "<chronology review worker functions>", "exec"), namespace)
        cls.serialize = staticmethod(namespace["claim"])
        cls.claim = corpus.load().events[ANCHOR].claims[3]

    def test_qualification_only_addition_change_and_removal_are_semantic(self):
        key = f"event:{ANCHOR}#3"
        full = self.serialize(self.claim)
        empty = self.serialize(self.claim._replace(context_qualification=""))
        shortened = self.serialize(self.claim._replace(
            context_qualification="Petavius table reported by Sloet"))
        self.assertIn("printed-page verification still pending", full["context_qualification"])
        for before, after in ((empty, full), (full, shortened), (full, empty)):
            for fields in (review.FIELDS_MANIFEST, review.FIELDS_FULL):
                with self.subTest(before=before["context_qualification"], fields=fields):
                    rows = review.diff_claims({"claims": {key: before}},
                                              {"claims": {key: after}}, fields)
                    self.assertEqual(rows, [{"kind": "claim", "id": key,
                        "why": "changed:context_qualification", "detail": ""}])

    def test_historical_claim_and_missing_serialized_field_mean_empty(self):
        fields = self.claim._asdict()
        del fields["context_qualification"]
        old = self.serialize(SimpleNamespace(**fields))
        self.assertEqual(old["context_qualification"], "")
        explicit = self.serialize(self.claim._replace(context_qualification=""))
        self.assertEqual(old, explicit)
        missing = dict(old)
        del missing["context_qualification"]
        for fields in (review.FIELDS_MANIFEST, review.FIELDS_FULL):
            self.assertEqual(review.diff_claims({"claims": {"old": missing}},
                                                {"claims": {"old": explicit}}, fields), [])


class AnchorQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.answer = corpus.chronology("Ps.136.1")
        cls.context = corpus.anchor_contexts(cls.answer)[0]

    def test_context_does_not_change_locus_assertions_or_convert_eras(self):
        self.assertEqual(self.context.subject, ANCHOR)
        self.assertEqual(self.context.parent.subject, PARENT)
        self.assertEqual(self.context.direction, "after")
        self.assertEqual([str(c.date) for _, c in self.context.claims],
                         ["3416 A.M.", "586 B.C.", "587 B.C.", "588 B.C."])
        self.assertEqual([i for i, _ in self.context.claims], [0, 1, 2, 3])
        self.assertNotIn(ANCHOR, [a.subject for a in self.answer.assertions])
        self.assertEqual(self.answer, corpus.chronology("Ps.136.1"))
        self.assertTrue(all(c.profile == self.context.parent.claim.profile
                            for _, c in self.context.claims))
        self.assertIn("printed-page verification still pending",
                      self.context.claims[-1][1].context_qualification)

    def test_evidence_mode_never_promotes_preserved_contradiction(self):
        contexts = corpus.anchor_contexts(corpus.chronology("Ps.136.1", evidence=True))
        self.assertEqual(contexts, (self.context,))
        self.assertTrue(all(c.answerability == "answerable"
                            for context in contexts for _, c in context.claims))
        # The underlying contradiction is still retained, not deleted to pass.
        self.assertIn("536 B.C.", [str(c.date) for c in corpus.load().events[ANCHOR].claims])

    def test_no_recursive_relative_duration_unit_or_profile_expansion(self):
        parent = self.context.parent
        source = corpus.load()
        for date in (
            parent.claim.date._replace(precision="relative", boundary=None,
                                      relative={"of": ANCHOR}),
            parent.claim.date._replace(precision="duration", boundary=None,
                                      duration={"within": ANCHOR}),
            parent.claim.date._replace(boundary={"anchor": "composition.psalter",
                                                 "direction": "after"}),
        ):
            answer = self.answer._replace(assertions=(parent._replace(
                claim=parent.claim._replace(date=date)),))
            self.assertEqual(corpus.anchor_contexts(answer), ())
        # A second boundary is retained as the anchor's own claim, not followed.
        nested = source.events[ANCHOR].claims[0]._replace(date=parent.claim.date)
        event = source.events[ANCHOR]._replace(claims=(nested,))
        other_profile = nested._replace(profile="catholic-critical-v1")
        for claims, expected in (((nested,), 1), ((other_profile,), 0)):
            mocked = source._replace(events={**source.events, ANCHOR: event._replace(claims=claims)})
            with patch.object(corpus, "load", return_value=mocked):
                contexts = corpus.anchor_contexts(self.answer)
            self.assertEqual(len(contexts), expected)
            if contexts:
                self.assertEqual(contexts[0].claims, ((0, nested),))

    def test_cli_context_is_typed_separately_and_keeps_exact_evidence(self):
        tool = load_tool("scripture-chronology")
        payload = tool.query(argparse.Namespace(locus="Ps.136.1", profile=None,
                            system=None, root=None, evidence=False))
        held = json.loads(json.dumps(payload))["anchor_contexts"][0]
        self.assertEqual(held["parent"]["subject"], PARENT)
        self.assertEqual(held["subject"], ANCHOR)
        for row, (index, claim) in zip(held["candidates"], self.context.claims):
            self.assertEqual(row["index"], index)
            self.assertEqual(row["label"], claim.date.label)
            self.assertEqual(row["sources"], list(claim.sources))
            self.assertEqual(row["qualification"], claim.context_qualification)


class AnchorProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.found = proper.dossier(TWENTIETH, provider="gpt")

    def test_schema_four_is_separate_and_schema_two_three_remain_available(self):
        record = tomllib.loads(proper.render(self.found))
        self.assertEqual(record["schema"], 4)
        context = record["anchor_contexts"][0]
        self.assertEqual(context["parent"]["subject"], PARENT)
        self.assertEqual(context["subject"], ANCHOR)
        self.assertEqual(context["direction"], "after")
        off = next(e for e in record["elements"] if e["key"] == "offertory")
        self.assertNotIn(ANCHOR, [c["subject"] for c in off["publication_claims"]])
        self.assertEqual(len(context["candidates"]), 4)
        plain = proper.dossier(FIFTEENTH)
        for found, schema in ((plain, 2), (plain._replace(
                comparison_dependencies=(("fixture", "a" * 64),)), 3)):
            payload = tomllib.loads(proper.render(found))
            self.assertEqual(payload["schema"], schema)
            self.assertNotIn("anchor_contexts", payload)
            self.assertNotIn("chronologyannotationanchor", proper.render_annotations_tex(proper.annotations(found)))

    def test_context_requires_boundary_common_to_every_locus(self):
        off = self.found.element("offertory")
        mixed = off._replace(loci=(*off.loci, "Ps.118.1"), publication_claims=tuple(
            c for c in off.publication_claims if c.subject != PARENT))
        self.assertEqual(proper._anchor_contexts((mixed,), None), ())
        projected = proper.annotations(self.found._replace(elements=(mixed,)))
        self.assertFalse(any(g.anchor_context for g in projected.elements[0].groups))

    def test_context_sources_are_in_the_computation_read_seal(self):
        traced = proper.computation_reads(TWENTIETH, ROOT, "gpt")
        context_sources = {s for context in self.found.anchor_contexts
                           for candidate in context.candidates for s in candidate.claim.sources}
        ordinary_sources = {s for element in self.found.elements
                            for claim in element.claims for s in claim.sources}
        compared_sources = {s for comparison in self.found.profile_comparisons
                            for claim in comparison.claims for s in claim.sources}
        self.assertEqual(set(traced["sources"]), {
            s for s in context_sources | ordinary_sources | compared_sources | resolved_binding_sources(self.found)
            if not s.startswith("bible")})
        self.assertTrue(context_sources - ordinary_sources)


class AnchorRoundTripTests(StudyLeaf, unittest.TestCase):
    document = TWENTIETH

    def setUp(self):
        super().setUp()
        self.write_provenance(version="9")
        self.shared_date_wrapper()

    def test_generated_context_validates_and_web_keeps_its_boundary_and_qualification(self):
        found = self.corpus()
        tex = proper.render_annotations_tex(proper.annotations(found))
        (self.leaf / proper.ANNOTATIONS_RECORD).write_text(tex)
        self.write("research", r"\chronodate{offertory}{\chronologyannotation{offertory}}" + "\n")
        for check in ("chronology-record-current", "chronology-annotations-current", "chronology-claims-supported"):
            self.assertEqual(self.check(check)[0], [], check)
        web = load_tool("web-edition")
        expanded, _ = web.expand_chronology_annotations(
            r"\chronologyannotation{offertory}", tex)
        for text in ("Historical background", "The third captivity of Juda",
                     "The represented event is after this historical event",
                     "A.M. 3416", "B.C. 586", "B.C. 587", "B.C. 588",
                     "Haydock reporting Ussher", "printed-page verification still pending",
                     "not to the passage or its composition", "same year"):
            self.assertIn(text, expanded)
        for jargon in ("Anchor context", "this anchor", "the boundary"):
            self.assertNotIn(jargon, expanded)
        self.assertNotIn("536", expanded)
        self.assertNotIn("after B.C. 586", expanded)
        # Removing a qualification from generated TeX invalidates the projection.
        path = self.leaf / proper.ANNOTATIONS_RECORD
        path.write_text(tex.replace("printed-page verification still pending", ""))
        self.assertTrue(self.check("chronology-annotations-current")[0])

    def test_context_is_not_a_global_passage_date_permission(self):
        self.corpus()
        self.write("research", r"\chronodate{offertory}{\chronology{" + PARENT +
                   r"}{historical-setting}{586 B.C.}}" + "\n")
        self.assertTrue(self.check("chronology-claims-supported")[0])
        self.write("research", r"\chronodate{offertory}{\chronology{" + ANCHOR +
                   r"}{anchor-context}{586 B.C.}}" + "\n")
        self.assertTrue(self.check("chronology-claims-supported")[0])
        self.write("research", "The Psalm was composed in 586 B.C.\n")
        self.assertTrue(self.check("chronology-claims-supported")[0])
        self.write("research", r"\chronologyannotationanchorclaim{x}{0}{p}{preferred}"
                   r"{s}{basis}{586 B.C.}{}{The Psalm was composed in 586 B.C.}")
        self.assertIn("anchor context helpers may occur only", " ".join(
            self.check("chronology-annotations-current")[0]))


if __name__ == "__main__":
    unittest.main()
