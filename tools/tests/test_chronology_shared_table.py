"""The provider-neutral table owns its complete wording, order and evidence."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _chronology as corpus
import _proper_chronology as chronology
from tools.tests.test_chronology import load_tool

BASE = "liturgy/roman-rite/1962/propers/temporal/"


class SharedTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.found = chronology.dossier(BASE + "f02-all-saints", provider="gpt")
        cls.projection = chronology.annotations(cls.found)

    def test_same_appointments_and_evidence_have_identical_provider_tables(self):
        for name in ("f01-christ-the-king", "f02-all-saints"):
            projections = [chronology.annotations(chronology.dossier(BASE + name, provider=provider))
                           for provider in ("gpt", "claude")]
            self.assertEqual(chronology.render_orientation_table(projections[0]),
                             chronology.render_orientation_table(projections[1]))
            self.assertEqual(projections[0].orientation_rows, projections[1].orientation_rows)

    def test_shorter_display_preserves_every_candidate_and_exact_locus(self):
        expected = {(e.key, r.locus, c.subject, c.relation, c.profile, c.label)
                    for e in self.found.elements for c in e.claims for r in c.reaches}
        actual = {(p.element_key, locus, c.subject, c.relation, c.profile, c.label)
                  for row in self.projection.orientation_rows for p in row.passages
                  for locus in p.loci for c in row.group.claims}
        self.assertEqual(actual, expected)
        self.assertEqual(sum(c.subject == "composition.gospel-of-matthew"
                             for row in self.projection.orientation_rows for c in row.group.claims), 6)

    def test_different_undated_episodes_stay_distinct_same_episode_forms_consolidate(self):
        other = chronology.dossier(BASE + "66-resumed-fifth-after-epiphany", provider="gpt")
        a = self.found.element("gospel")._replace(key="gospel-long")
        b = other.element("gospel")._replace(key="gospel-short")
        found = self.found._replace(elements=(a, b), profile_comparisons=())
        events = [r for r in chronology.orientation_rows(found) if r.group.relation == "narrated-event"]
        self.assertEqual(len(events), 2)
        self.assertTrue(any("Beatitudes" in row.context_label for row in events))
        self.assertTrue(any("tells the parable" in row.context_label for row in events))
        same = found._replace(elements=(a, a._replace(key="gospel-short")))
        events = [r for r in chronology.orientation_rows(same) if r.group.relation == "narrated-event"]
        self.assertEqual(len(events), 1)
        self.assertEqual(len(events[0].passages), 2)

    def test_context_does_not_supply_a_date_or_borrow_an_uncovered_passage(self):
        event = next(r for r in self.projection.orientation_rows if r.group.relation == "narrated-event")
        self.assertEqual(chronology.orientation_date(event), "Date unresolved")
        self.assertTrue(event.context_sources)
        gospel = self.found.element("gospel")
        extended = self.found._replace(elements=(gospel._replace(loci=gospel.loci + ("Matt.5.13",)),))
        events = [r for r in chronology.orientation_rows(extended) if r.group.relation == "narrated-event"]
        self.assertEqual(len(events), 2)
        self.assertEqual(sum(not r.context_label for r in events), 1)

    def test_numbering_parts_and_era_typography_preserve_the_named_system(self):
        cite = chronology.Citation("Psalm 24:1bc-2", "Psalms", "hebrew",
                                   (((24, 1, "bc"), (24, 2, "")),))
        self.assertIn("Ps. 24:1bc–2 (Heb.; Vg. 23)", chronology._passage_display_v3("Psalm", (cite,)))
        rendered = chronology.render_annotations_tex(self.projection)
        self.assertIn("c.~A.D.~50", rendered)
        self.assertIn("221--204 B.C.", rendered)
        self.assertIn("A.M.~2944 (Haydock edition reporting Ussher)", rendered)
        self.assertIn("Composition: Matthew", rendered)
        # Source wording remains sealed, not rewritten to match typography.
        claim = next(c for row in self.projection.orientation_rows for c in row.group.claims
                     if c.subject == "composition.book-of-wisdom")
        self.assertIn("{" + chronology.tex_escape(claim.label) + "}", rendered)

    def test_gate_refuses_reordered_augmented_and_inline_tables(self):
        preflight = load_tool("check-content-preflight")
        leaf = ROOT / "src/gpt" / self.found.document
        path = leaf / chronology.ORIENTATION_TABLE_RECORD
        table = chronology.render_orientation_table(self.projection)
        check = lambda p, text: preflight._orientation_tables(
            {p: preflight.active_tex(text)}, self.found, leaf, required=True)[0]
        self.assertEqual(check(path, table), [])
        lines = table.splitlines()
        first = next(i for i, line in enumerate(lines) if line.startswith(r"\chronologyorientationrow"))
        lines[first], lines[first + 1] = lines[first + 1], lines[first]
        self.assertTrue(check(path, "\n".join(lines)))
        self.assertTrue(check(path, table.replace("}{}", "}{Additional context.}", 1)))
        self.assertTrue(check(leaf / "sections/forged.tex", table))

    def test_display_metadata_rejects_dates_overlap_and_unknown_subjects(self):
        scratch = ROOT / ".scratch/chronology-lane"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            root = Path(directory)
            path = root / "orientation.yaml"
            original = (ROOT / "src/sources/chronology/orientation.yaml").read_text()
            path.write_text(original.replace("Jesus teaches the Beatitudes", "A.D. 30 Jesus teaches the Beatitudes"))
            with self.assertRaisesRegex(corpus.ChronologyError, "without dates"):
                corpus._load_orientation_contexts(root, corpus._canon_books())
            path.write_text(original.replace("chapter: 13, first: 24, last: 30", "chapter: 5, first: 1, last: 12"))
            with self.assertRaisesRegex(corpus.ChronologyError, "overlapping"):
                corpus._load_orientation_contexts(root, corpus._canon_books())
            path.write_text(original)
            with self.assertRaisesRegex(corpus.ChronologyError, "unknown temporal subject"):
                corpus._load_orientation_subject_labels(root, set())


if __name__ == "__main__":
    unittest.main()
