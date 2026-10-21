"""Source-order, repeated-Oratio identity and rubric boundaries of two Ember Masses."""
from pathlib import Path
import hashlib
import importlib.machinery
import json
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars
import _proper_latin

ORDERS = {'pentecost-ember-saturday/longer': ['Introit', 'Collect', 'First Lesson', 'First Alleluia', 'Oratio', 'Second Lesson', 'Second Alleluia', 'Oratio', 'Third Lesson', 'Third Alleluia', 'Oratio', 'Fourth Lesson', 'Fourth Alleluia', 'Oratio', 'Fifth Lesson', 'Fifth Alleluia', 'Oratio', 'Epistle', 'Tract', 'Sequence', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'pentecost-ember-saturday/shorter': ['Introit', 'Collect', 'Lesson', 'Alleluia', 'Oratio', 'Epistle', 'Second Alleluia', 'Sequence', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'september-ember-saturday/longer': ['Introit', 'Collect', 'First Lesson', 'First Gradual', 'Oratio', 'Second Lesson', 'Second Gradual', 'Oratio', 'Third Lesson', 'Third Gradual', 'Oratio', 'Fourth Lesson', 'Fourth Gradual', 'Oratio', 'Fifth Lesson', 'Hymn (Benedictus es)', 'Oratio', 'Epistle', 'Tract', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'september-ember-saturday/shorter': ['Introit', 'Collect', 'Lesson', 'Gradual', 'Oratio', 'Epistle', 'Tract', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion']}
EXPECTED = {('pentecost-ember-saturday', 'longer', 'Collect', 1): '22a8e592eb7d757fd260ea116c50c8e4b96f3141e1a12cfc6c2585cf5d7e30f6', ('pentecost-ember-saturday', 'longer', 'Oratio', 1): '6974518908b249285820d2b4edbbdd87c8828bc2128038801f5d0a21d25e3d1a', ('pentecost-ember-saturday', 'longer', 'Oratio', 2): 'a47159a190381741a0e1e7a95e90075773c11d4f73897bd54b252b42dabfc40b', ('pentecost-ember-saturday', 'longer', 'Oratio', 3): '9fe82184cb826da47a75bfe93bb84f37b774127f0daeeb84d2bdd5808b2330a8', ('pentecost-ember-saturday', 'longer', 'Fourth Alleluia', 1): '504014c49bb5f4edf71eefcda8bb6da4281f395ed3734dbff8a1e96267fec379', ('pentecost-ember-saturday', 'longer', 'Oratio', 4): '241f28f25e0131cccaab5f240e7f1a019c0270e9d6e42494cccb56f849582bcd', ('pentecost-ember-saturday', 'longer', 'Oratio', 5): '7c0f207aee56711c8e4caf64e2318abe602d7d48771675419dfd1066b484c38b', ('pentecost-ember-saturday', 'longer', 'Secret', 1): '155863a7462e84838b70c8286984ce63b4012b0be37be7dcd7b18b46d2a5c54b', ('pentecost-ember-saturday', 'longer', 'Postcommunion', 1): 'e42adb4760f296b180b6d8c35fc62a03bed1f362007ab995b1bfa21fda35f6c6', ('pentecost-ember-saturday', 'shorter', 'Collect', 1): 'e1597da87d856671f589c4fcec5fa55a99788a0f119c2ee98589db3cc4c88429', ('pentecost-ember-saturday', 'shorter', 'Oratio', 1): '6974518908b249285820d2b4edbbdd87c8828bc2128038801f5d0a21d25e3d1a', ('pentecost-ember-saturday', 'shorter', 'Second Alleluia', 1): '549ae56671df781349284412691153e94647f50c605a01ab7577d2a3d89481af', ('pentecost-ember-saturday', 'shorter', 'Secret', 1): '155863a7462e84838b70c8286984ce63b4012b0be37be7dcd7b18b46d2a5c54b', ('pentecost-ember-saturday', 'shorter', 'Postcommunion', 1): '9d66ea9b051dea3c388b3569261c7fef87992f7ccb2f212e608204f3a708d0eb', ('september-ember-saturday', 'longer', 'Collect', 1): '1a9be24d1a6d56f998969dee2bdb0c197670dec7567189a363f2e385759f4018', ('september-ember-saturday', 'longer', 'Oratio', 1): 'f1cde7cd725a5a05971c7bff4a46be39859a86976abd2ca698e439a76ba315f7', ('september-ember-saturday', 'longer', 'Oratio', 2): '51ca6f23c52dcf86c457be8dca32d5dd9782356e68a9af7494b33880fdbf5e85', ('september-ember-saturday', 'longer', 'Oratio', 3): '080caa860ae6f8bf79e7c0ee4c434a6141fa36060b73733e5e6e6c47f270a8bb', ('september-ember-saturday', 'longer', 'Oratio', 4): 'e9df4468735fdbd972598e908674dd5d721eeb9e39201deeba7ef4d22c0380f7', ('september-ember-saturday', 'longer', 'Oratio', 5): '7c0f207aee56711c8e4caf64e2318abe602d7d48771675419dfd1066b484c38b', ('september-ember-saturday', 'longer', 'Secret', 1): '97aded5e5ac006a9a16ad82ccbfdf90bf35a6b6f81f6ffdc02b694f2133cbb74', ('september-ember-saturday', 'longer', 'Postcommunion', 1): '00b153dd621063933460305a3484d48dbb3f223f12a03b198afa619c64be70a9', ('september-ember-saturday', 'shorter', 'Collect', 1): '1a9be24d1a6d56f998969dee2bdb0c197670dec7567189a363f2e385759f4018', ('september-ember-saturday', 'shorter', 'Oratio', 1): 'a8b6e4647b7c9e069fcf8a35ce95a0ec607224e549c5e0d5b60934bb3663897f', ('september-ember-saturday', 'shorter', 'Secret', 1): '97aded5e5ac006a9a16ad82ccbfdf90bf35a6b6f81f6ffdc02b694f2133cbb74', ('september-ember-saturday', 'shorter', 'Postcommunion', 1): '00b153dd621063933460305a3484d48dbb3f223f12a03b198afa619c64be70a9'}
HISTORICAL_ARTIFACT = 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ember-pentecost-september-la-checked-ea162251'
PROJECTION_ARTIFACT = 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.ember-pentecost-september-5fdd4f00'

class PentecostSeptemberEmberTests(unittest.TestCase):
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
        overlay = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
        for mass, form, proper, occurrence in EXPECTED:
            rows = [r for r in overlay["untranslated"] if (r["mass"], r.get("form_id", "main"), r["proper"], r.get("occurrence",1), r.get("cycle","all")) == (mass,form,proper,occurrence,"all")]
            self.assertEqual(1, len(rows), (mass,form,proper,occurrence))
            self.assertEqual("no-exemplar", rows[0]["reason"]["kind"])

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
