"""Exact, reviewed subpassages must never become inferred commentary edges."""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _catena
import _catena_snippets as snippets
from tools.tests.test_catena import CatenaFixture


class SnippetTests(CatenaFixture):
    def setUp(self):
        super().setUp()
        self.identifier = "passage.augustine.de-civitate-dei.dods-1871.11.7"
        self.sources = _catena.load_sources(self.root)
        self.edges = _catena.load_edges(self.root)
        self.text = self.sources.passages[self.identifier]["text"]
        self.snippet = {"id": "light", "start": 0, "end": len(self.text),
                        "extent": {"token": "Gen", "first_chapter": 1, "first_verse": 3,
                                   "last_chapter": 1, "last_verse": 3},
                        "locator": "XI.7, making of light", "basis": "Explicit lemma and explanation."}
        self.document = {"schema": snippets.SCHEMA, "numbering": "vulgate",
                         "offset_unit": "unicode-code-point", "reviewed_on": "2026-11-08",
                         "passages": [{"passage_id": self.identifier,
                                       "text_sha256": hashlib.sha256(self.text.encode()).hexdigest(),
                                       "snippets": [self.snippet]}]}

    def review(self):
        self.write(snippets.PATH.as_posix(), yaml.safe_dump(self.document))
        return snippets.reviewed(self.root, self.sources, self.edges)

    def test_checked_subpassage_projects_without_rewriting_parent(self):
        rows, errors = self.review()
        self.assertEqual(errors, [])
        projected = snippets.project(self.text, rows[self.identifier])[0]
        self.assertEqual(self.text[projected["start"]:projected["end"]], self.text)
        self.assertEqual(self.edges["fragments"][0]["extent"]["last_verse"], 5)
        self.assertEqual(self.sources.passages[self.identifier]["states"],
                         ["cataloged", "acquired", "inspected"])

    def test_stale_text_never_repairs_its_own_hash_or_publishes_partial_review(self):
        self.sources.passages[self.identifier]["text"] = self.text + " changed"
        rows, errors = self.review()
        self.assertEqual(rows, {})
        self.assertIn("stale parent text hash", " ".join(errors))
        with self.assertRaisesRegex(_catena.CatenaError, "stale parent text hash"):
            # Use the real producer after changing the on-disk pin instead.
            self.document["passages"][0]["text_sha256"] = "0" * 64
            self.review()
            _catena.fragments_for_book(self.root, "Gen")

    def test_unknown_parent_cannot_admit_a_new_fragment(self):
        self.document["passages"][0]["passage_id"] = "passage.unadmitted"
        self.assertIn("not an admitted fragment", " ".join(self.review()[1]))

    def test_narrower_excerpt_cannot_widen_scripture_claim(self):
        for field, value in (("first_verse", 2), ("last_verse", 6), ("token", "Ps")):
            with self.subTest(field=field):
                previous = self.snippet["extent"][field]
                self.snippet["extent"][field] = value
                self.assertIn("beyond its parent", " ".join(self.review()[1]))
                self.snippet["extent"][field] = previous

    def test_offsets_ids_order_and_basis_fail_closed(self):
        cases = [{"start": True}, {"end": len(self.text)+1}, {"start": 1},
                 {"id": "../escape"}, {"basis": ""}, {"extent": {}}]
        for change in cases:
            with self.subTest(change=change):
                self.document["passages"][0]["snippets"] = [{**self.snippet, **change}]
                self.assertEqual(self.review()[0], {})
                self.assertTrue(self.review()[1])
        self.document["passages"][0]["snippets"] = [self.snippet, copy.deepcopy(self.snippet)]
        self.assertIn("duplicate snippet id", " ".join(self.review()[1]))
        self.assertIn("without overlap", " ".join(self.review()[1]))

    def test_source_state_is_required_without_upgrading_it(self):
        self.sources.passages[self.identifier]["states"] = ["acquired"]
        self.assertIn("has not been inspected", " ".join(self.review()[1]))

    def test_extent_coordinates_do_not_coerce_booleans_or_strings(self):
        for value in (True, "3", 3.5, 0):
            with self.subTest(value=value):
                self.snippet["extent"]["first_verse"] = value
                self.assertIn("positive integer endpoints", " ".join(self.review()[1]))

    def test_utf16_offsets_preserve_astral_characters(self):
        text = "Intro 😀\n\nLemma 😀 and commentary.\n\nContext"
        start, end = text.index("Lemma"), text.index("\n\nContext")
        row = snippets.project(text, [{**self.snippet, "start": start, "end": end}])[0]
        self.assertEqual(row["start"], start + 1)
        self.assertEqual(row["end"], end + 2)
        body = text.encode("utf-16-le")[2*row["start"]:2*row["end"]].decode("utf-16-le")
        self.assertEqual(body, text[start:end])

    def test_citations_do_not_generate_snippets(self):
        self.sources.passages[self.identifier]["text"] += " See also John 1:1 and Romans 8:1."
        self.assertEqual(snippets.reviewed(self.root, self.sources, self.edges), ({}, []))

    def test_controller_metadata_preserves_container_and_segment_identity(self):
        passage = {"edition_id": "edition.constituent", "segment_id": "segment.constituent",
                   "artifact_sha256": "a" * 64, "physical_line_ranges": [[20, 30]],
                   "artifact_page_ranges": [[4, 6]]}
        record = snippets.source_record(passage, {"id": "artifact.anthology"})
        self.assertEqual(record["artifact_id"], "artifact.anthology")
        self.assertEqual(record["edition_id"], "edition.constituent")
        self.assertEqual(record["segment_id"], "segment.constituent")
        self.assertEqual(record["physical_line_ranges"], [[20, 30]])


class HeldCorpusTests(unittest.TestCase):
    def test_real_pass_all_admitted_fragments_accounted_and_exact_slices_replay(self):
        sources, edges = _catena.load_sources(ROOT), _catena.load_edges(ROOT)
        rows, errors = snippets.reviewed(ROOT, sources, edges)
        self.assertEqual(errors, [])
        self.assertGreaterEqual(sum(map(len, rows.values())), 24)
        for identifier, reviewed in rows.items():
            text = sources.passages[identifier]["text"]
            for source, public in zip(reviewed, snippets.project(text, reviewed)):
                replay = text.encode("utf-16-le")[public["start"]*2:public["end"]*2].decode("utf-16-le")
                self.assertEqual(replay, text[source["start"]:source["end"]])
        report = snippets.audit(ROOT)
        self.assertEqual(report["errors"], [])
        self.assertGreaterEqual(report["counted"]["fragments"], 1560)
        self.assertEqual(len(report["fragments"]), report["counted"]["fragments"])
        self.assertTrue(report["large_parents_without_snippets"])

    def test_philippians_and_gregory_have_real_explanations_not_incidental_citations(self):
        sources, edges = _catena.load_sources(ROOT), _catena.load_edges(ROOT)
        rows, errors = snippets.reviewed(ROOT, sources, edges)
        self.assertEqual(errors, [])
        identifier = "passage.john-chrysostom.homilies-on-philippians.ccel-web-2026-09-17.3"
        row = next(row for row in rows[identifier] if row["id"] == "verse-21")
        text = sources.passages[identifier]["text"][row["start"]:row["end"]]
        self.assertTrue(text.startswith('Ver. 21. "For to me,"'))
        self.assertIn("For even in dying", text)
        self.assertNotIn("Ver. 22.", text)
        # Galatians is cited in the argument but receives no snippet edge.
        self.assertIn("Gal. ii. 20.", text)
        self.assertEqual({row["extent"]["token"] for row in rows[identifier]}, {"Phil"})
        gregory = next(identifier for identifier in rows if identifier.endswith("gregory-de-hominis-opificio"))
        self.assertLess(max(row["end"]-row["start"] for row in rows[gregory]), 5000)

    def test_colossians_objection_stays_with_its_answer(self):
        sources, edges = _catena.load_sources(ROOT), _catena.load_edges(ROOT)
        rows, errors = snippets.reviewed(ROOT, sources, edges)
        self.assertEqual(errors, [])
        identifier = "passage.john-chrysostom.homilies-on-colossians.ccel-web-2026-09-05.4.col-1.21-23"
        verse23 = next(row for row in rows[identifier] if row["id"] == "verse-23")
        text = sources.passages[identifier]["text"][verse23["start"]:verse23["end"]]
        self.assertTrue(text.startswith("But, since he ascribed"))
        self.assertIn("we need nothing", text)
        self.assertIn("If so be that ye continue", text)


if __name__ == "__main__":
    unittest.main()
