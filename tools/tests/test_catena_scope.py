"""Active Catholic commentary follows reviewed authors, not delivery editors."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _catena_scope


class TrackedScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = _catena_scope.Scope(ROOT)

    def test_registry_is_valid(self):
        self.assertEqual(self.scope.errors, [])

    def test_luther_aliases_and_authored_work_are_excluded(self):
        for name in ("Martin Luther", "Luther", "  MARTIN   LUTHER ", "Martinus Lutherus"):
            decision = self.scope.author_decision(name)
            self.assertEqual(decision["status"], "excluded")
            self.assertTrue(decision["basis_sources"])
        self.assertFalse(self.scope.allowed_work("work.martin-luther.lectures-on-genesis"))

    def test_held_anglican_commentaries_are_explicitly_excluded(self):
        for name, work_id in (
            ("Brooke Foss Westcott", "work.brooke-foss-westcott.the-gospel-according-to-st-john"),
            ("Henry Latham", "work.henry-latham.the-risen-master"),
        ):
            with self.subTest(author=name):
                author = self.scope.author_decision(name)
                work = self.scope.work_decision(work_id)
                self.assertEqual(author["status"], "excluded")
                self.assertEqual(work["status"], "excluded")
                self.assertEqual(author["person_id"], work["person_id"])
                self.assertIn(work_id, author["basis_sources"])

    def test_pre_schism_fathers_and_catholic_writers_are_received(self):
        for name in ("Basil the Great", "Gregory of Nyssa", "Ephrem the Syrian",
                     "Severian of Gabala", "Remigius of Auxerre", "Alcuin of York",
                     "Angelomus of Luxeuil", "Nicholas of Lyra", "Denis the Carthusian"):
            with self.subTest(name=name):
                self.assertTrue(self.scope.allowed_author(name))

    def test_unknown_author_is_not_silently_catholic(self):
        decision = self.scope.author_decision("A newly harvested commentator")
        self.assertEqual(decision["status"], "unreviewed")
        self.assertFalse(decision["eligible"])
        self.assertIsNone(decision["person_id"])

    def test_a_catholic_author_label_cannot_launder_a_non_catholic_work(self):
        result = self.scope.lead_decision({"author": "Thomas Aquinas", "work_id": "work.martin-luther.lectures-on-genesis"})
        self.assertEqual(result["status"], "excluded")
        result = self.scope.lead_decision({"author": "Thomas Aquinas", "work_id": "work.augustine.de-civitate-dei"})
        self.assertEqual(result["status"], "unreviewed")

    def test_theophylact_retains_only_his_explicit_received_exception(self):
        result = self.scope.author_decision("Theophylact of Ohrid")
        self.assertEqual(result["status"], "eligible")
        self.assertIn("liturgical-commentators-plan-2026-09-22.md", result["policy_exception"])
        self.assertIn("contrary evidence", result["reason"])
        self.assertEqual(self.scope.author_decision("Unknown Byzantine exegete")["status"], "unreviewed")

    def test_anthology_editor_does_not_classify_constituent_authors(self):
        result = self.scope.work_decision("work.nicene-and-post-nicene-fathers.series-2-volume-8")
        self.assertEqual(result["status"], "unreviewed")
        self.assertIn("constituent", result["reason"])
        self.assertTrue(self.scope.allowed_work("work.basil-of-caesarea.homiliae-in-hexaemeron"))

    def test_every_active_fragment_has_an_eligible_intellectual_author(self):
        data = yaml.safe_load((ROOT / "src/sources/commentary/fragment-loci.yaml").read_text())
        for section in ("fragments", "blocked"):
            for work_id in sorted({row["work_id"] for row in data.get(section, [])}):
                with self.subTest(section=section, work=work_id):
                    self.assertTrue(self.scope.allowed_work(work_id), self.scope.work_decision(work_id))


class IsolatedScopeTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/catholic-scope"
        scratch.mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.registry = self.root / "src/sources/inventories/author-standing-v1.toml"
        self.registry.parent.mkdir(parents=True)

    def write_registry(self, confession="Catholic", standing="ecclesiastical-writer"):
        person = dict(id="reviewed-author", name="Reviewed Author", names=["Reviewed Author"],
                      died="Not dated", standing=standing, standing_basis="Cited identity review.",
                      basis_sources=["https://example.org/review"], confession=confession)
        self.registry.write_text(
            'schema = "triptych-author-standing/v1"\nrecord_type = "author-standing"\n'
            'audited_on = "2026-11-07"\n[[persons]]\n' +
            "".join(f"{key} = {json.dumps(value)}\n" for key, value in person.items())
        )

    def test_invalid_or_missing_registry_cannot_admit(self):
        self.assertFalse(_catena_scope.Scope(self.root).allowed_author("Reviewed Author"))
        self.write_registry()
        with self.registry.open("a") as out:
            out.write('role = "doctor"\n')
        scope = _catena_scope.Scope(self.root)
        self.assertTrue(scope.errors)
        self.assertEqual(scope.author_decision("Reviewed Author")["status"], "unreviewed")

    def test_confession_is_exact_not_a_catholic_substring(self):
        self.write_registry(confession="Not Catholic")
        self.assertFalse(_catena_scope.Scope(self.root).allowed_author("Reviewed Author"))

    def test_a_registered_byzantine_writer_does_not_inherit_the_named_exception(self):
        self.write_registry(confession="Byzantine, after 1054")
        result = _catena_scope.Scope(self.root).author_decision("Reviewed Author")
        self.assertEqual(result["status"], "unreviewed")
        self.assertNotIn("policy_exception", result)

    def test_non_catholic_standing_wins_over_conflicting_confession(self):
        self.write_registry(standing="non-catholic")
        self.assertEqual(_catena_scope.Scope(self.root).author_decision("Reviewed Author")["status"], "excluded")

    def test_delivery_translator_cannot_exclude_catholic_work(self):
        self.write_registry()
        work_id = "work.reviewed-author.commentary"
        works = {work_id: dict(id=work_id, responsible="Reviewed Author", work_type="biblical-commentary")}
        scope = _catena_scope.Scope(self.root, works=works)
        self.assertTrue(scope.allowed_work(work_id))
        # Edition credits and artifact ownership are deliberately absent from
        # this API: they cannot change an intellectual work's author decision.
        self.assertFalse(scope.allowed_author("Protestant Translator"))

    def test_editor_and_namespace_cannot_launder_authored_commentary(self):
        self.write_registry()
        works = {
            "work.reviewed-author.anthology": dict(responsible="Reviewed Author", work_type="patristic-translation-anthology"),
            "work.reviewed-author.other": dict(responsible="Unknown Commentator", work_type="biblical-commentary"),
        }
        scope = _catena_scope.Scope(self.root, works=works)
        self.assertFalse(scope.allowed_work("work.reviewed-author.anthology"))
        self.assertFalse(scope.allowed_work("work.reviewed-author.other"))

    def test_new_snapshot_observes_registry_changes(self):
        self.write_registry()
        self.assertTrue(_catena_scope.Scope(self.root).allowed_author("Reviewed Author"))
        self.write_registry(standing="non-catholic")
        self.assertFalse(_catena_scope.Scope(self.root).allowed_author("Reviewed Author"))


if __name__ == "__main__":
    unittest.main()
