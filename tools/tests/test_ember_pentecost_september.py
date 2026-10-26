"""Source-order, repeated-Oratio identity and rubric boundaries of two Ember Masses."""
from pathlib import Path
import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars
import _proper_latin
from tools.tests import _source_batch_guards as source_batch
from tools.tests._source_recovery_assertions import assert_current_english_owner

ORDERS = {'pentecost-ember-saturday/longer': ['Introit', 'Collect', 'First Lesson', 'First Alleluia', 'Oratio', 'Second Lesson', 'Second Alleluia', 'Oratio', 'Third Lesson', 'Third Alleluia', 'Oratio', 'Fourth Lesson', 'Fourth Alleluia', 'Oratio', 'Fifth Lesson', 'Fifth Alleluia', 'Oratio', 'Epistle', 'Tract', 'Sequence', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'pentecost-ember-saturday/shorter': ['Introit', 'Collect', 'Lesson', 'Alleluia', 'Oratio', 'Epistle', 'Second Alleluia', 'Sequence', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'september-ember-saturday/longer': ['Introit', 'Collect', 'First Lesson', 'First Gradual', 'Oratio', 'Second Lesson', 'Second Gradual', 'Oratio', 'Third Lesson', 'Third Gradual', 'Oratio', 'Fourth Lesson', 'Fourth Gradual', 'Oratio', 'Fifth Lesson', 'Hymn (Benedictus es)', 'Oratio', 'Epistle', 'Tract', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'september-ember-saturday/shorter': ['Introit', 'Collect', 'Lesson', 'Gradual', 'Oratio', 'Epistle', 'Tract', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion']}
EXPECTED = {('pentecost-ember-saturday', 'longer', 'Collect', 1): '22a8e592eb7d757fd260ea116c50c8e4b96f3141e1a12cfc6c2585cf5d7e30f6', ('pentecost-ember-saturday', 'longer', 'Oratio', 1): '6974518908b249285820d2b4edbbdd87c8828bc2128038801f5d0a21d25e3d1a', ('pentecost-ember-saturday', 'longer', 'Oratio', 2): 'a47159a190381741a0e1e7a95e90075773c11d4f73897bd54b252b42dabfc40b', ('pentecost-ember-saturday', 'longer', 'Oratio', 3): '9fe82184cb826da47a75bfe93bb84f37b774127f0daeeb84d2bdd5808b2330a8', ('pentecost-ember-saturday', 'longer', 'Fourth Alleluia', 1): '504014c49bb5f4edf71eefcda8bb6da4281f395ed3734dbff8a1e96267fec379', ('pentecost-ember-saturday', 'longer', 'Oratio', 4): '241f28f25e0131cccaab5f240e7f1a019c0270e9d6e42494cccb56f849582bcd', ('pentecost-ember-saturday', 'longer', 'Oratio', 5): '7c0f207aee56711c8e4caf64e2318abe602d7d48771675419dfd1066b484c38b', ('pentecost-ember-saturday', 'longer', 'Secret', 1): '155863a7462e84838b70c8286984ce63b4012b0be37be7dcd7b18b46d2a5c54b', ('pentecost-ember-saturday', 'longer', 'Postcommunion', 1): 'e42adb4760f296b180b6d8c35fc62a03bed1f362007ab995b1bfa21fda35f6c6', ('pentecost-ember-saturday', 'shorter', 'Collect', 1): 'e1597da87d856671f589c4fcec5fa55a99788a0f119c2ee98589db3cc4c88429', ('pentecost-ember-saturday', 'shorter', 'Oratio', 1): '6974518908b249285820d2b4edbbdd87c8828bc2128038801f5d0a21d25e3d1a', ('pentecost-ember-saturday', 'shorter', 'Second Alleluia', 1): '549ae56671df781349284412691153e94647f50c605a01ab7577d2a3d89481af', ('pentecost-ember-saturday', 'shorter', 'Secret', 1): '155863a7462e84838b70c8286984ce63b4012b0be37be7dcd7b18b46d2a5c54b', ('pentecost-ember-saturday', 'shorter', 'Postcommunion', 1): '9d66ea9b051dea3c388b3569261c7fef87992f7ccb2f212e608204f3a708d0eb', ('september-ember-saturday', 'longer', 'Collect', 1): '1a9be24d1a6d56f998969dee2bdb0c197670dec7567189a363f2e385759f4018', ('september-ember-saturday', 'longer', 'Oratio', 1): 'f1cde7cd725a5a05971c7bff4a46be39859a86976abd2ca698e439a76ba315f7', ('september-ember-saturday', 'longer', 'Oratio', 2): '51ca6f23c52dcf86c457be8dca32d5dd9782356e68a9af7494b33880fdbf5e85', ('september-ember-saturday', 'longer', 'Oratio', 3): '080caa860ae6f8bf79e7c0ee4c434a6141fa36060b73733e5e6e6c47f270a8bb', ('september-ember-saturday', 'longer', 'Oratio', 4): 'e9df4468735fdbd972598e908674dd5d721eeb9e39201deeba7ef4d22c0380f7', ('september-ember-saturday', 'longer', 'Oratio', 5): '7c0f207aee56711c8e4caf64e2318abe602d7d48771675419dfd1066b484c38b', ('september-ember-saturday', 'longer', 'Secret', 1): '97aded5e5ac006a9a16ad82ccbfdf90bf35a6b6f81f6ffdc02b694f2133cbb74', ('september-ember-saturday', 'longer', 'Postcommunion', 1): '00b153dd621063933460305a3484d48dbb3f223f12a03b198afa619c64be70a9', ('september-ember-saturday', 'shorter', 'Collect', 1): '1a9be24d1a6d56f998969dee2bdb0c197670dec7567189a363f2e385759f4018', ('september-ember-saturday', 'shorter', 'Oratio', 1): 'a8b6e4647b7c9e069fcf8a35ce95a0ec607224e549c5e0d5b60934bb3663897f', ('september-ember-saturday', 'shorter', 'Secret', 1): '97aded5e5ac006a9a16ad82ccbfdf90bf35a6b6f81f6ffdc02b694f2133cbb74', ('september-ember-saturday', 'shorter', 'Postcommunion', 1): '00b153dd621063933460305a3484d48dbb3f223f12a03b198afa619c64be70a9'}
HISTORICAL_ARTIFACT = 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ember-pentecost-september-la-checked-ea162251'
PROJECTION_ARTIFACT = 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.ember-pentecost-september-5fdd4f00'

class PentecostSeptemberEmberTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader("ember_recovery_propers", str(ROOT / "tools/mass-propers"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.propers = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.propers
        loader.exec_module(cls.propers)
        cls.overlay, _, stale, cls.witnesses = cls.propers.translation_overlay("roman-1962", ROOT / "src/sources/calendars")
        if stale:
            raise AssertionError(stale)
        cls.english_ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
        historical_path = ROOT / "tools/tests/fixtures/roman-1962-ember-english-absences-20261021.json"
        raw = historical_path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != "1001f48a074bef79f1f473e89d2bc5199e70e70755afd49c59b4a1932bc06ebe":
            raise AssertionError("exact original Ember English absence fixture")
        cls.historical_english = json.loads(raw)

    def assert_english_owner(self, key, ledger):
        mass, form, proper, occurrence = key
        return assert_current_english_owner(
            self, (mass, form, proper, "all", occurrence), ledger,
            self.propers, self.overlay, self.witnesses, latin_sha256=EXPECTED[key])

    def test_source_order_and_separate_direct_owners(self):
        document = _calendars.load_document(ROOT / "src/sources/calendars", "roman-1962")
        masses = _calendars.mass_index(document)
        actual = {}
        for masskey in ("pentecost-ember-saturday", "september-ember-saturday"):
            mass = masses[masskey]
            self.assertEqual("unavailable", mass["ordinary_frame"]["applicability"])
            for form in mass["forms"]:
                self.assertEqual(ORDERS[masskey + "/" + form["id"]], [p["name"] for p in form["propers"]])
                seen = {}
                for proper in form["propers"]:
                    seen[proper["name"]] = seen.get(proper["name"], 0) + 1
                    key = (masskey, form["id"], proper["name"], seen[proper["name"]])
                    if key not in EXPECTED:
                        continue
                    self.assertEqual("composed", proper["source"])
                    self.assertNotIn("takes_from", proper)
                    self.assertNotIn("text_status", proper)
                    self.assertEqual(EXPECTED[key], _proper_latin.text_sha256(proper["text"]))
                    actual[key] = proper
        self.assertEqual(set(EXPECTED), set(actual))
        # Repeating an oration body never changes its source occurrence identity.
        self.assertEqual(5, sum(k[0] == "pentecost-ember-saturday" and k[1] == "longer" and k[2] == "Oratio" for k in actual))
        self.assertEqual(1, sum(k[0] == "pentecost-ember-saturday" and k[1] == "shorter" and k[2] == "Oratio" for k in actual))

    def test_per_body_publication_and_english_absences(self):
        records, problems = _proper_latin.publication_records(ROOT / "src/sources/calendars", "roman-1962", ROOT / "src/sources/inventories")
        self.assertEqual([], problems)
        for key, digest in EXPECTED.items():
            mass, form, proper, occurrence = key
            label = "Longer form (forma missae longior)" if form == "longer" else "Shorter form"
            matches = [(k, r) for k, r in records.items() if (k.mass, k.form, k.proper, k.occurrence) == (mass, label, proper, occurrence)]
            self.assertEqual(1, len(matches), key)
            _, row = matches[0]
            self.assertEqual(digest, row["text_sha256"])
            self.assertEqual("collated", row["provenance_status"])
            self.assertEqual("permitted", row["publication_status"])
            self.assertEqual([PROJECTION_ARTIFACT, HISTORICAL_ARTIFACT], row["publication_source_ids"])
        for mass, form, proper, occurrence in EXPECTED:
            self.assert_english_owner((mass, form, proper, occurrence), self.english_ledger)

    def test_original_english_absences_keep_their_exact_historical_scope(self):
        scope = self.historical_english
        self.assertEqual("c726f83a1521c1355831bec579617d2cc2f37315", scope["source_revision"])
        self.assertEqual("9230a5534a0a05988aa0f6aa749feb39bc6a1291bb9e1cb2f0833fc830c67cdb", scope["source_ledger_sha256"])
        self.assertEqual("73cf09e120975fa6ca4e6f343e3e6f14a9a60eaa408c7fd6590101b29906893f",
                         source_batch.digest(source_batch.canonical(scope["rows"])))
        expected = {(mass, form, proper, "all", occurrence) for mass, form, proper, occurrence in EXPECTED}
        self.assertEqual(expected, {tuple(json.loads(key)) for key in scope["rows"]})
        for row in scope["rows"].values():
            self.assertEqual({"kind": "no-exemplar"}, row["reason"])
            self.assertEqual("unavailable", row["availability"])

    def test_current_english_state_cannot_revert_to_an_old_absence(self):
        for key in EXPECTED:
            group, entry = self.assert_english_owner(key, self.english_ledger)
            broken = copy.deepcopy(self.english_ledger)
            broken[group].remove(entry)
            if group == "entries":
                mass, form, proper, occurrence = key
                old_key = source_batch.canonical((mass, form, proper, "all", occurrence))
                broken["untranslated"].append(self.historical_english["rows"][old_key])
            else:
                changed = copy.deepcopy(entry)
                changed["reason"] = {"kind": "witness-gap"}
                broken[group].append(changed)
            with self.subTest(key=key):
                with self.assertRaises(AssertionError):
                    self.assert_english_owner(key, broken)

    def test_current_english_rejects_changed_body_and_publication_proof(self):
        for key in EXPECTED:
            group, entry = self.assert_english_owner(key, self.english_ledger)
            if group != "entries":
                continue
            for defect in ("body", "proof"):
                broken = copy.deepcopy(entry)
                if defect == "body":
                    broken["translations"][0]["text"] += " Amen."
                else:
                    broken["publication_passage_id"] += "-unproved"
                with self.subTest(key=key, defect=defect):
                    with self.assertRaises(ValueError):
                        self.propers.validate_translation_publication_binding(
                            broken, ROOT / "src/sources/calendars",
                            ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml", self.witnesses)

    def test_both_veni_chants_keep_the_genuflection_as_a_rubric(self):
        document = _calendars.load_document(ROOT / "src/sources/calendars", "roman-1962")
        mass = _calendars.mass_index(document)["pentecost-ember-saturday"]
        for form in mass["forms"]:
            name = "Fourth Alleluia" if form["id"] == "longer" else "Second Alleluia"
            proper = next(p for p in form["propers"] if p["name"] == name)
            self.assertNotIn("verses", proper)
            action = proper["text_structure"]["actions"]
            self.assertEqual([{"kind":"rubric", "offset":proper["text"].index("(Hic genuflectitur)"), "text":"(Hic genuflectitur)"}], action)
            self.assertEqual(_proper_latin.text_sha256(proper["text"]), proper["text_structure"]["text_sha256"])
            self.assertNotIn("speaker", proper)
            self.assertIn("℣. Veni, Sancte Spiritus", proper["text"])

if __name__ == "__main__":
    unittest.main()
