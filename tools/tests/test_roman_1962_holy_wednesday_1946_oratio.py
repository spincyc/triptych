"""Keep the ordinary Holy Wednesday prayer bound to its actual1946 witness."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import copy
import hashlib
import json
import re
import sys
import tomllib
import unicodedata
import unittest

ROOT = Path(__file__).resolve().parents[2]
CAL = ROOT / "src/sources/calendars"
LEDGER = ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml"
KEY = ("holy-wednesday", "main", "Oratio super populum", "all", 1)
PREFIX = "artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945-printing-1946."
EDITION = "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945-printing-1946"
PDF = PREFIX + "ia-google-facsimile-pdf-4573991d"
PDF_SHA = "4573991d962eb6a6391bc2555b8445bdfebd84de1ccffd7828f84e74d308ca77"
TABLE = PREFIX + "prayer-conclusions-checked-20261023"
TABLE_SHA = "b90aa8e6630ca32be43f8405f71c95aefbd870ddac5dd2c71ff1b9831f3d4b59"
PUBLICATION = PREFIX + "resume-orations-holyweek6-oratio1946-1-2f3842da"
PUBLICATION_SHA = "2f3842daef686a971f42369c899250e2aa56de82f81fae4360fdd8e77e48f7c4"
LATIN_SHA = "359843b7ed66997981419510228d5d61620c45bb9a42b835dc42d5c8deb61d47"
HISTORICAL_SHA = "df6670046a6d3e069e19efdd6021f89f4a270dccbda0201456b5260869fd5c8f"
ENGLISH_SHA = "e925aef0719e104a889d0abcb6e5cc7540392ab7908b1bfbc890e20c29f8a38f"


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def words(value):
    value = value.casefold().replace("æ", "ae").replace("œ", "oe")
    value = "".join(c for c in unicodedata.normalize("NFKD", value) if not unicodedata.combining(c))
    return re.findall("[a-z]+|[0-9]+", value)


class HolyWednesday1946OrdinaryPrayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = SourceFileLoader("holy_wednesday_1946_propers", str(ROOT / "tools/mass-propers"))
        spec = spec_from_loader(loader.name, loader)
        cls.p = module_from_spec(spec)
        sys.modules[spec.name] = cls.p
        loader.exec_module(cls.p)
        cls.doc = cls.p.load_calendar(CAL, "roman-1962")
        cls.overlay, cls.absent, cls.stale, cls.witnesses = cls.p.translation_overlay("roman-1962", CAL)
        cls.records, cls.trouble = cls.p._source_library_records(CAL)
        cls.entry = cls.overlay[KEY]
        cls.slots = {}
        for _, mass in cls.p.masses_of(cls.doc):
            for form, body, taken in cls.p.appointed_propers(cls.doc, mass):
                owner = cls.p.source_slot_identity(cls.doc, mass, form, body, taken)
                cls.slots.update(dict(cls.p.coverage_slot_units(body, owner)))

    def test_actual_physical_witness_and_unresolved_whole_scan(self):
        self.assertFalse(self.stale)
        self.assertFalse(self.trouble)
        artifact = self.records[PDF]
        self.assertEqual((artifact["edition_id"], artifact["sha256"]), (EDITION, PDF_SHA))
        self.assertEqual((artifact["storage"], artifact["rights_status"]), ("remote", "unresolved"))
        self.assertEqual((artifact["byte_size"], artifact["page_count"]), (135628123, 1884))
        self.assertEqual(self.records[EDITION]["date"], "1946")
        ledger = tomllib.loads(LEDGER.read_text())
        witness = next(row for row in ledger["sources"] if row["id"] == "lasance-1945-printing-1946")
        self.assertEqual(witness["source_id"], EDITION)
        self.assertEqual(witness["rights"], "public-domain")
        self.assertIn("unresolved", witness["caution"])

    def test_distinct_oratio_publication_and_complete_target_proof(self):
        entry = self.entry
        self.assertEqual(entry["artifact_id"], PDF)
        self.assertEqual(entry["publication_artifact_id"], PUBLICATION)
        self.assertEqual(entry["publication_artifact_sha256"], PUBLICATION_SHA)
        self.assertEqual(sha(entry["translations"][0]["text"]), ENGLISH_SHA)
        verification = self.records[entry["passage_id"]]
        publication = self.records[entry["publication_passage_id"]]
        self.assertIn("oratio-super-populum", verification["id"])
        self.assertEqual((verification["artifact_id"], verification["artifact_page_ranges"]), (PDF, [[455, 455]]))
        self.assertEqual(publication["artifact_id"], PUBLICATION)
        self.assertEqual(publication["physical_line_ranges"], [[2, 2]])
        self.assertEqual(sha(self.slots[KEY]["text"]), LATIN_SHA)
        latin = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text())["entries"]
        proof = [row for row in latin if row["mass"] == KEY[0] and row["proper"] == KEY[2] and not row["form"] and not row["course"] and not row["cycle"] and row["occurrence"] == 1]
        self.assertEqual(len(proof), 1)
        self.assertEqual(proof[0]["text_sha256"], LATIN_SHA)
        self.assertIn("Existing target Latin verification " + proof[0]["verification_source_id"] + " retained", verification["notes"])
        self.assertIn("Complete canonical Latin SHA256 " + LATIN_SHA, publication["notes"])

    def test_complete_petitions_and_actual_own_book_endings(self):
        record = self.records[TABLE]
        self.assertEqual((record["edition_id"], record["sha256"], record["derived_from"]), (EDITION, TABLE_SHA, PDF))
        payload = (ROOT / record["path"]).read_bytes()
        self.assertEqual(sha(payload), TABLE_SHA)
        table = json.loads(payload)
        self.assertEqual((table["pdf_page"], table["printed_page"]), (829, "819"))
        family = next(row for row in table["formulas"] if row["key"] == "who-with-thee")
        verification = self.records[self.entry["passage_id"]]
        historical = verification["notes"].split("Historical Latin comparison transcription: ", 1)[1].split(" Complete checked English SHA256 ", 1)[0]
        self.assertEqual(sha(historical), HISTORICAL_SHA)
        self.assertIn(TABLE, verification["notes"])
        source = words(historical)
        target = words(self.slots[KEY]["text"])
        self.assertEqual(source[-2:], ["qui", "tecum"])
        self.assertEqual(target[-7:], ["qui", "tecum", "vivit", "et", "regnat", "in", "unitate"])
        self.assertEqual(source[:-2], target[:-7])
        self.assertEqual(source[-2:], words(family["full_latin"])[:2])
        self.assertEqual(target[-7:], words(family["full_latin"])[:7])
        self.assertEqual(words(self.entry["translations"][0]["text"])[-4:], words(family["full_english"])[:4])
        self.assertNotIn("amen", target)
        self.assertNotIn("amen", words(self.entry["translations"][0]["text"]))

    def test_exact_publication_rejects_changed_english_and_other_day_controller(self):
        self.p.validate_translation_publication_binding(self.entry, CAL, LEDGER, self.witnesses)
        artifact = self.records[PUBLICATION]
        self.assertEqual((artifact["edition_id"], artifact["derived_from"]), (EDITION, PDF))
        self.assertEqual(sha((ROOT / artifact["path"]).read_bytes()), PUBLICATION_SHA)
        changed = copy.deepcopy(self.entry)
        changed["translations"][0]["text"] += " Amen."
        with self.assertRaisesRegex(ValueError, "translation body differs from its exact publication passage"):
            self.p.validate_translation_publication_binding(changed, CAL, LEDGER, self.witnesses)
        changed = copy.deepcopy(self.entry)
        other = next(row for key, row in self.overlay.items() if key[:3] == ("mass-of-the-lords-supper", "main", "Secret"))
        changed["passage_id"] = other["passage_id"]
        with self.assertRaises(ValueError):
            self.p.validate_translation_publication_binding(changed, CAL, LEDGER, self.witnesses)


if __name__ == "__main__":
    unittest.main()
