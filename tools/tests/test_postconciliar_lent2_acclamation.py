"""Keep Lent II's uncited acclamation distinct from Bible reconstruction.

OLM ed4bc14e artifact p. 74 / printed p. 20, nn. 25-27: the source prints
one uncited composed unit and two referrals. No liturgical wording is needed.
"""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import sys
import tomllib
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src/sources/calendars"
INVENTORIES = ROOT / "src/sources/inventories"
ARTIFACT = "artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e"


class PostconciliarLentTwoAcclamationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = SourceFileLoader("_lent2_acclamation_mass_propers", str(ROOT / "tools/mass-propers"))
        spec = spec_from_loader(loader.name, loader)
        cls.owner = module_from_spec(spec)
        sys.modules[loader.name] = cls.owner
        loader.exec_module(cls.owner)
        cls.document = yaml.safe_load((CALENDARS / "postconciliar/propers.yaml").read_text())
        cls.mass = next(m for s in cls.document["sections"].values() for m in s["masses"] if m["key"] == "lent-2")

    def test_unit_is_retained_without_an_inferred_scripture_appointment(self):
        names = [p["name"] for p in self.mass["propers"]]
        index = names.index("Verse Before the Gospel")
        self.assertEqual(names[index-1:index+2], ["Second Reading", "Verse Before the Gospel", "Gospel"])
        slot = self.mass["propers"][index]
        self.assertEqual(slot["source"], "composed")
        self.assertEqual(slot["text_status"], {"state":"unavailable", "scope":"proper-body", "reasons":[{"kind":"witness-gap", "source_id":ARTIFACT}]})
        for field in ("verses", "text", "incipit", "translations", "cycles", "weekday_cycles", "takes_from"):
            self.assertNotIn(field, slot)
        communion = next(p for p in self.mass["propers"] if p["name"] == "Communion Antiphon")
        self.assertEqual(communion["source"], "scripture")
        self.assertEqual(communion["verses"][0]["ref"], "Matthew 17:5")

    def test_english_absence_is_exact_and_latin_quarantine_is_not_fabricated(self):
        en = tomllib.loads((INVENTORIES / "postconciliar-proper-translations-v1.toml").read_text())
        rows = [r for r in en["untranslated"] if r.get("mass")=="lent-2" and r.get("proper")=="Verse Before the Gospel"]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual({k:row[k] for k in ("form_id","cycle","occurrence","lang","extent","availability","reason")}, {"form_id":"main","cycle":"all","occurrence":1,"lang":"en","extent":"body","availability":"unavailable","reason":{"kind":"no-exemplar"}})
        for field in ("text","translation","translations","source_id","witness_artifact_id","quarantined_text_sha256"):
            self.assertNotIn(field,row)
        latin = tomllib.loads((INVENTORIES / "postconciliar-proper-latin-provenance-v1.toml").read_text())
        self.assertFalse(any(r.get("mass")=="lent-2" and r.get("proper")=="Verse Before the Gospel" for r in latin.get("entries",[])))

    def test_public_owner_has_an_unavailable_unit_without_bible_substitution(self):
        structure = self.owner.calendar_structure(CALENDARS, "postconciliar", self.owner.book_tokens())
        mass = next(m for m in structure["masses"] if m["key"]=="lent-2")
        unit = next(p for p in mass["propers"] if p["name"]=="Verse Before the Gospel")
        self.assertEqual(unit["source"],"composed")
        self.assertFalse(unit.get("citations"))
        self.assertFalse(unit.get("cycles"))
        self.assertIsNone(unit.get("latin"))
        self.assertIsNone(unit.get("text"))
        self.assertEqual(unit["text_status"],{"state":"unavailable","scope":"proper-body"})
        self.assertEqual({r["lang"]:r["status"] for r in unit["languages"]},{"la":"unavailable","en":"unavailable"})
        self.assertEqual(len(unit["untranslated"]),1)

    def test_english_accounting_has_no_silent_or_stale_units(self):
        coverage = self.owner.english_coverage(CALENDARS,"postconciliar")
        for field in ("unaccounted","outside_the_ledger","unmatched_records","stale_translation_records"):
            self.assertEqual(coverage[field],0,(field,coverage))


if __name__ == "__main__":
    unittest.main()
