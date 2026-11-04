"""The provider-neutral table owns its complete wording, order and evidence."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from collections import Counter
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _chronology as corpus
import _proper_chronology as chronology
import chronology_review_diff as review
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
        for key in ("gospel", "alleluia", "communion"):
            self.assertEqual(sum(c.subject == "composition.gospel-of-matthew"
                                 for row in self.projection.orientation_rows
                                 if row.passages[0].element_key == key for c in row.group.claims), 6)

    def test_different_undated_episodes_and_appointed_forms_keep_their_identity(self):
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
        self.assertEqual(len(events), 2)
        self.assertEqual({r.passages[0].element_key for r in events}, {"gospel-long", "gospel-short"})
        self.assertEqual(len({r.context_label for r in events}), 1)

    def test_every_orientation_consumer_has_ordered_disjoint_passages_and_complete_evidence(self):
        manifests = [p for p in ROOT.glob("src/*/liturgy/**/proper-components.toml")
                     if tomllib.loads(p.read_text()).get("chronology_presentation")]
        self.assertGreaterEqual(len(manifests), 10)
        for path in manifests:
            provider = path.relative_to(ROOT / "src").parts[0]
            document = str(path.parent.relative_to(ROOT / "src" / provider))
            with self.subTest(provider=provider, document=document):
                found = chronology.dossier(document, provider=provider)
                self.assertEqual(found.presentation, chronology.ORIENTATION_V3)
                projection = chronology.annotations(found)
                rows = projection.orientation_rows
                # Derive the expected content from the appointments and queried
                # evidence, independently of the presentation's grouping.
                expected_loci = Counter((e.key, locus) for e in found.elements for locus in e.loci)
                visible_loci = Counter((p.element_key, locus) for row in rows if row.passage_start
                                       for p in row.passages for locus in p.loci)
                self.assertEqual(visible_loci, expected_loci)
                order = [min(chronology._locus_order(locus) for p in row.passages for locus in p.loci)
                         for row in rows if row.passage_start]
                self.assertEqual(order, sorted(order))
                self.assertTrue(all(len(row.passages) == 1 for row in rows))
                for index, row in enumerate(rows):
                    if not row.passage_start:
                        self.assertEqual(row.passages, rows[index - 1].passages)
                    if not row.passage_end:
                        self.assertEqual(row.passages, rows[index + 1].passages)
                fact = lambda key, locus, c: (key, locus, c.subject, c.relation,
                                              c.profile, c.disposition, c.label)
                # A subject whose dates the corpus admits only by an unqualified
                # reporting exception is withheld as a pending row, not printed.
                withheld = {(e.key, r.locus, c.relation) for e in found.elements for c in e.claims
                            for r in c.reaches if c.reporting_exception and not c.orientation_qualification}
                pending = {(p.element_key, locus, row.group.relation) for row in rows
                           if row.group.status == chronology.QUALIFICATION_PENDING
                           for p in row.passages for locus in p.loci}
                self.assertEqual(pending, withheld)
                expected = Counter(fact(e.key, r.locus, c) for e in found.elements
                                   for c in e.claims for r in c.reaches
                                   if (e.key, r.locus, c.relation) not in withheld)
                actual = Counter(fact(p.element_key, locus, c) for row in rows
                                 if not row.group.requested_profile and not row.group.anchor_context
                                 for p in row.passages for locus in p.loci for c in row.group.claims)
                self.assertEqual(actual, expected)
                expected_comparisons = Counter((comparison.requested_profile, *fact(comparison.element_key, r.locus, c))
                                               for comparison in found.profile_comparisons
                                               for c in comparison.claims for r in c.reaches)
                actual_comparisons = Counter((row.group.requested_profile, *fact(p.element_key, locus, c))
                                             for row in rows if row.group.requested_profile
                                             for p in row.passages for locus in p.loci for c in row.group.claims)
                self.assertEqual(actual_comparisons, expected_comparisons)

    def test_context_does_not_supply_a_date_or_borrow_an_uncovered_passage(self):
        event = next(r for r in self.projection.orientation_rows if r.group.relation == "narrated-event")
        self.assertEqual(chronology.orientation_date(event), "Date unresolved")
        self.assertTrue(event.context_sources)
        gospel = self.found.element("gospel")
        extended = self.found._replace(elements=(gospel._replace(loci=gospel.loci + ("Matt.5.13",)),))
        events = [r for r in chronology.orientation_rows(extended) if r.group.relation == "narrated-event"]
        self.assertEqual(len(events), 2)
        self.assertEqual(sum(not r.context_label for r in events), 1)

    def test_strict_subrange_comparison_partitions_the_default_passage(self):
        found = chronology.dossier(BASE + "61-twenty-first-after-pentecost", provider="claude")
        gospel = found.element("gospel")
        first = gospel.loci[0]
        comparison = next(c for c in found.profile_comparisons if c.element_key == gospel.key)
        comparison = comparison._replace(claims=tuple(c._replace(
            reaches=tuple(r for r in c.reaches if r.locus == first)) for c in comparison.claims))
        found = found._replace(elements=(gospel,), profile_comparisons=(comparison,), anchor_contexts=())
        rows = chronology.orientation_rows(found)
        visible = Counter(locus for row in rows if row.passage_start for p in row.passages for locus in p.loci)
        self.assertEqual(visible, Counter(gospel.loci))
        self.assertEqual([p.loci for r in rows if r.group.requested_profile for p in r.passages], [(first,)])
        expected = Counter((c.subject, r.locus, c.label) for c in gospel.claims for r in c.reaches)
        actual = Counter((c.subject, locus, c.label) for row in rows if not row.group.requested_profile
                         for c in row.group.claims for p in row.passages for locus in p.loci)
        self.assertEqual(actual, expected)

    def test_strict_subrange_anchor_and_comparison_partition_each_other(self):
        found = chronology.dossier(BASE + "61-twenty-first-after-pentecost", provider="claude")
        gospel = found.element("gospel")
        first, second = gospel.loci[:2]
        comparison = next(c for c in found.profile_comparisons if c.element_key == gospel.key)
        comparison = comparison._replace(claims=tuple(c._replace(
            reaches=tuple(r for r in c.reaches if r.locus == first)) for c in comparison.claims))
        template = chronology.dossier(BASE + "60-twentieth-after-pentecost", provider="gpt").anchor_contexts[0]
        # This fixture exercises projection coverage independently of research
        # policy: a two-verse anchor crosses a one-verse comparison boundary.
        reaches = tuple(r for c in gospel.claims[:1] for r in c.reaches if r.locus in (first, second))
        anchor = template._replace(element_key=gospel.key, parent=template.parent._replace(reaches=reaches))
        found = found._replace(elements=(gospel,), profile_comparisons=(comparison,), anchor_contexts=(anchor,))
        rows = chronology.orientation_rows(found)
        visible = Counter(locus for row in rows if row.passage_start for p in row.passages for locus in p.loci)
        self.assertEqual(visible, Counter(gospel.loci))
        anchors = [row for row in rows if row.group.anchor_context]
        self.assertEqual([p.loci for row in anchors for p in row.passages], [(first,), (second,)])
        for row in anchors:
            self.assertEqual(tuple(c.label for c in row.group.claims), tuple(c.claim.label for c in anchor.candidates))

    def test_middle_comparison_does_not_pull_later_verses_ahead_of_its_passage(self):
        found = chronology.dossier(BASE + "61-twenty-first-after-pentecost", provider="claude")
        gospel = found.element("gospel")
        middle = gospel.loci[len(gospel.loci) // 2]
        comparison = next(c for c in found.profile_comparisons if c.element_key == gospel.key)
        comparison = comparison._replace(claims=tuple(c._replace(
            reaches=tuple(r for r in c.reaches if r.locus == middle)) for c in comparison.claims))
        rows = chronology.orientation_rows(found._replace(
            elements=(gospel,), profile_comparisons=(comparison,), anchor_contexts=()))
        visible = [locus for row in rows if row.passage_start for p in row.passages for locus in p.loci]
        self.assertEqual(visible, sorted(gospel.loci, key=chronology._locus_order))
        self.assertEqual(sum(row.passage_start for row in rows), 3)

    def test_numbering_parts_and_era_typography_preserve_the_named_system(self):
        cite = chronology.Citation("Psalm 24:1bc-2", "Psalms", "hebrew",
                                   (((24, 1, "bc"), (24, 2, "")),))
        self.assertIn("Ps. 24:1bc–2 (Heb.; Vg. 23)", chronology._passage_display_v3("Psalm", (cite,)))
        # An adapted citation keeps its "Cf." and spells its book as any other.
        adapted = chronology.Citation("Cf. Psalm 33:11", "Psalms", "vulgate", (((33, 11, ""), (33, 11, "")),))
        self.assertEqual(chronology._passage_display_v3("Psalm", (adapted,)),
                         "Psalm: Cf. Ps. 33:11 (Vg.; Heb. 34)")
        adapted = chronology.Citation("Cf. Ephesians 1:17-18", "Ephesians", "", (((1, 17, ""), (1, 18, "")),))
        self.assertEqual(chronology._passage_display_v3("Alleluia Verse", (adapted,)),
                         "Alleluia Verse: Cf. Eph. 1:17–18")
        rendered = chronology.render_annotations_tex(self.projection)
        self.assertIn("c.~A.D.~50", rendered)
        self.assertIn("221--204 B.C.", rendered)
        self.assertIn("A.M.~2944 (Haydock edition reporting Ussher)", rendered)
        self.assertIn("Composition: Matthew", rendered)
        # Source wording remains sealed, not rewritten to match typography.
        claim = next(c for row in self.projection.orientation_rows for c in row.group.claims
                     if c.subject == "composition.book-of-wisdom")
        self.assertIn("{" + chronology.tex_escape(claim.label) + "}", rendered)

    def test_settings_are_sourced_and_bound_to_their_date_relation(self):
        found = chronology.dossier(BASE + "61-twenty-first-after-pentecost", provider="claude")
        rows = chronology.orientation_rows(found)
        by_subject = {r.group.claims[0].subject: r for r in rows if r.group.claims}
        for subject, phrase in (
                ("composition.book-of-esther", "story at Susa; writing in Persia conjectured"),
                ("critical.book-of-job", "story in Hus; writing site unspecified"),
                ("composition.epistle-to-the-ephesians", "Rome or Caesarea"),
                ("critical.gospel-of-matthew", "Antioch suggested")):
            row = by_subject[subject]
            self.assertIn(phrase, chronology.orientation_subject(row, found.presentation))
            self.assertTrue(row.context_sources)
        event = next(r for r in rows if r.group.relation == "narrated-event")
        self.assertIn("Capharnaum by narrative continuity", event.context_label)
        self.assertEqual(chronology.orientation_date(event), "Date unresolved")
        # A place bound to a traditional composition claim must not migrate to
        # a different profile's subject or to an event in the same appointment.
        self.assertNotIn("Rome", by_subject["critical.ephesians-later-disciple"].setting_label)
        self.assertNotIn("Palestine", event.setting_label)
        changed = dict(found.orientation_settings)
        key = "composition.book-of-esther"
        changed[key] = changed[key]._replace(relation="narrated-event")
        mismatch = next(r for r in chronology.orientation_rows(found._replace(orientation_settings=changed))
                        if r.group.claims and r.group.claims[0].subject == key)
        self.assertEqual(mismatch.setting_label, "")

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
            subjects = set(corpus.load().events) | set(corpus.load().units)
            with self.assertRaisesRegex(corpus.ChronologyError, "unknown temporal subject"):
                corpus._load_orientation_settings(root, set())
            path.write_text(original.replace("story at Susa;", "A.D. 30 story at Susa;"))
            with self.assertRaisesRegex(corpus.ChronologyError, "without dates"):
                corpus._load_orientation_settings(root, subjects)

    def test_review_diff_detects_a_setting_only_change_through_the_real_worker(self):
        scratch = ROOT / ".scratch/proper-table-repair/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            root = Path(directory)
            (root / "scripts").symlink_to(ROOT / "scripts", target_is_directory=True)
            data = root / "corpus"
            shutil.copytree(ROOT / "src/sources/chronology", data)
            worker = root / "worker.py"
            worker.write_text(review.WORKER)

            def snapshot():
                run = subprocess.run([sys.executable, str(worker), str(data)],
                                     check=True, capture_output=True, text=True)
                return json.loads(run.stdout)

            before = snapshot()
            path = data / "orientation.yaml"
            path.write_text(path.read_text().replace("Antioch suggested", "Antioch tentatively suggested"))
            after = snapshot()
            for section in ("claims", "profiles", "bindings", "gaps"):
                self.assertEqual(before[section], after[section])
            subject = "critical.gospel-of-matthew"
            setting = after["orientation"]["settings"][subject]
            self.assertEqual(set(setting), {"relation", "label", "sources", "basis"})
            self.assertEqual(setting["label"], "Antioch tentatively suggested")
            with mock.patch.object(review, "load_revision", side_effect=(before, after)):
                result = review.build(ROOT, "before", "after", ("orientation",), "full")
            self.assertEqual(len(result["orientation"]), 1)
            detail = json.loads(result["orientation"][0]["detail"])
            self.assertEqual(detail["before"]["settings"][subject]["label"], "Antioch suggested")
            self.assertEqual(detail["after"]["settings"][subject], setting)


if __name__ == "__main__":
    unittest.main()
