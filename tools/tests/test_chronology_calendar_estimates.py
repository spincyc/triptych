"""Calendar orientation preserves the underlying question, profile and evidence."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _chronology as chronology


class CalendarEstimateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = chronology.load()
        cls.document = chronology._document("orientation", chronology.CORPUS_ROOT)

    def load_estimates(self, rows):
        with patch.object(chronology, "_document", return_value={"calendar_estimates": rows}):
            return chronology._load_orientation_calendar_estimates(
                chronology.CORPUS_ROOT, self.corpus.events, self.corpus.units,
                self.corpus.bindings, self.corpus.policies)

    def test_invalid_selection_and_unqualified_dates_refuse(self):
        original = self.document["calendar_estimates"][0]
        changes = [
            {"subject": "unknown.subject"},
            {"relation": "narrated-event"},
            {"profile": "catholic-comprehensive-v1"},
            {"profile": "catholic-critical-v1"},
            {"inputs": ["missing.anchor"]},
            {"sources": []},
            {"qualification": ""},
            {"kind": "composition-date"},
            {"anchor": "israel.restoration.decree-of-cyrus"},
            {"date": {"precision": "year", "from": {"year": 740, "era": "bc"}, "label": "740 B.C."}},
        ]
        for change in changes:
            with self.subTest(change=change):
                row = copy.deepcopy(original)
                row.update(change)
                with self.assertRaises(chronology.ChronologyError):
                    self.load_estimates([row])
        row = copy.deepcopy(original)
        row["date"]["label"] = "740–536 B.C."
        with self.assertRaisesRegex(chronology.ChronologyError, "approximation"):
            self.load_estimates([row])
        with self.assertRaisesRegex(chronology.ChronologyError, "duplicate"):
            self.load_estimates([original, original])
        row = copy.deepcopy(original)
        row["date"]["label"] = "c. 123 B.C."
        with self.assertRaisesRegex(chronology.ChronologyError, "typed endpoints"):
            self.load_estimates([row])

    def test_calendar_boundary_is_typed_and_accepts_same_year(self):
        estimate = self.corpus.orientation_calendar_estimates[(
            "israel.monarchy.saul-reign", "superscription-setting", "catholic-traditional-v1")]
        self.assertEqual(estimate.date.precision, "boundary")
        self.assertEqual(estimate.date.boundary["direction"], "no-later-than")
        self.assertEqual(estimate.date.begin.year, 1055)

    def test_calendar_context_keeps_profile_and_open_ministry_limits(self):
        estimates = self.corpus.orientation_calendar_estimates
        ministry = estimates[("israel.exile.ezechiel.ministry", "prophecy-given", "catholic-traditional-v1")]
        self.assertEqual((ministry.date.begin.year, ministry.date.end.year), (594, 571))
        self.assertIn("may have continued", ministry.qualification)
        self.assertIn("derived", ministry.qualification)
        isaiah = estimates[("israel.exile.second-isaias-oracles", "prophecy-given", "catholic-critical-v1")]
        self.assertEqual(isaiah.kind, "anchor-context")
        self.assertEqual(isaiah.anchor, "israel.restoration.decree-of-cyrus")
        self.assertEqual(isaiah.date.begin.year, 538)
        self.assertNotIn((isaiah.subject, isaiah.relation, "catholic-traditional-v1"), estimates)
        for subject, relation in (("life-of-christ.last-supper", "narrated-event"),
                                  ("life-of-christ.resurrection", "prophetic-referent")):
            estimate = estimates[(subject, relation, "catholic-traditional-v1")]
            self.assertEqual(estimate.date.begin.year, 29)
            self.assertIn("Maas", estimate.qualification)
            self.assertIn("disputed", estimate.qualification)

    def test_anchor_context_cannot_change_its_subjects_anchor(self):
        row = copy.deepcopy(next(r for r in self.document["calendar_estimates"]
                                 if r["subject"] == "composition.jeremias-letter-to-the-exiles"))
        self.assertEqual(next(iter(self.load_estimates([row]).values())).kind, "anchor-context")
        row["anchor"] = "israel.restoration.decree-of-cyrus"
        row["inputs"].append(row["anchor"])
        with self.assertRaisesRegex(chronology.ChronologyError, "anchor does not belong"):
            self.load_estimates([row])

    def test_estimates_do_not_change_query_candidates(self):
        for locus in ("Ps.43.8", "Ps.84.2", "Ps.129.1", "Jer.29.11", "Ps.33.2", "Ps.3.2"):
            before = chronology.chronology(locus)
            with patch.object(chronology, "load", return_value=self.corpus._replace(
                    orientation_calendar_estimates={})):
                self.assertEqual(chronology.chronology(locus), before)

    def test_korahite_estimate_reaches_only_the_identified_group(self):
        key = ("composition.psalms-of-the-sons-of-korah", "composition", "catholic-traditional-v1")
        self.assertIn(key, self.corpus.orientation_calendar_estimates)
        for system, locus in (("vulgate", "Ps.43.8"), ("hebrew", "Ps.44.8"),
                              ("vulgate", "Ps.84.2"), ("hebrew", "Ps.85.2")):
            answer = chronology.chronology(chronology.parse_locus(locus, system=system))
            self.assertTrue(any((a.subject, a.relation, a.claim.profile) == key
                                for a in answer.assertions))
        self.assertFalse(any(a.subject == key[0]
                             for a in chronology.chronology("Ps.129.1").assertions))

    def test_davidic_proposal_and_lifetime_phases_remain_distinct(self):
        proposed = chronology.chronology("Ps.129.1")
        unit = "composition.psalm-129-possible-davidic-composition"
        claim = next(a for a in proposed.assertions if a.subject == unit)
        self.assertEqual(claim.relation, "composition")
        self.assertEqual(claim.claim.disposition, "disputed")
        self.assertIn("might", claim.claim.date.label)
        self.assertFalse(any(a.subject == unit for a in chronology.chronology("Ps.130.1").assertions))
        stages = {key[0]: estimate.date.begin.year
                  for key, estimate in self.corpus.orientation_calendar_estimates.items()}
        self.assertGreater(stages["israel.monarchy.david-at-geth"],
                           stages["israel.monarchy.david-traditional-era"])
        self.assertGreater(stages["israel.monarchy.david-traditional-era"],
                           stages["israel.monarchy.david-flight-from-absalom"])

    def test_new_proper_davidic_rows_keep_the_later_chronology_caveat(self):
        import _proper_chronology as wiring

        document = ("liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/"
                    "propers/temporal/pc-s58-thirty-second-sunday-in-ordinary-time-year-a")
        found = wiring.dossier(document, provider="gpt")
        rows = [row for row in wiring.orientation_rows(found)
                if any(claim.subject == "israel.monarchy.david-traditional-era"
                       for claim in row.group.claims)]
        self.assertEqual({passage.element_key for row in rows for passage in row.passages},
                         {"psalm", "communion-psalm"})
        for row in rows:
            self.assertEqual(row.group.relation, "traditional-attribution")
            value = wiring.orientation_date(row, compact=True)
            self.assertIn("c. 1055–1015 B.C.", value)
            self.assertIn("Corbett", value)
            self.assertIn("30–50 years later", value)

    def test_gospel_teaching_dates_are_event_dates_with_bounded_scopes(self):
        for locus, outside, subject, year in (
            ("Matt.13.24", "Matt.13.54", "life-of-christ.parables-by-the-sea", 27),
            ("Mark.11.24", "Mark.11.27", "life-of-christ.faith-and-prayer-after-the-fig-tree", 29),
        ):
            answer = chronology.chronology(locus)
            event = next(a for a in answer.assertions if a.subject == subject)
            self.assertEqual(event.relation, "narrated-event")
            self.assertEqual(event.claim.date.begin.year, year)
            self.assertTrue(event.claim.date.derived)
            self.assertTrue(any(a.relation == "composition" for a in answer.assertions))
            self.assertFalse(any(a.subject == subject for a in chronology.chronology(outside).assertions))


if __name__ == "__main__":
    unittest.main()
