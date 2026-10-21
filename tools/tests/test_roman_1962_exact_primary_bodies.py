"""Exact adapted Missal readings retain their own cuts beside Bible apparatus."""
from __future__ import annotations

import copy
import hashlib
from importlib.machinery import SourceFileLoader
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib
import unicodedata
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars
import _missal_coverage
from _proper_latin import (
    LatinKey, SURFACES, decision_for, read_sidecar, sanitize_proper, text_sha256,
)

FIXTURE = ROOT / "tools/tests/fixtures/roman-1962-exact-primary-bodies.json"
CALENDARS = ROOT / "src/sources/calendars"


def record(identifier):
    kind, owner, work, edition, name = identifier.split(".")
    directory = ("2026-10-20-editorial-projection"
                 if edition == "editorial-projection-2026-10-20" else edition)
    p = ROOT / "src/sources/works" / owner / work / "editions" / directory
    p = p / "artifacts" / name / "artifact.toml" if kind == "artifact" else p / "passages" / (name + ".toml")
    result = tomllib.loads(p.read_text())
    if result["id"] != identifier:
        raise AssertionError(identifier)
    return result


def words(value):
    value = "".join(c for c in unicodedata.normalize("NFD", value)
                    if unicodedata.category(c) != "Mn")
    value = value.replace("æ", "ae").replace("œ", "oe").replace("Æ", "Ae").replace("Œ", "Oe")
    return re.findall("[A-Za-z]+", value.lower())


class ExactPrimaryBodiesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.document = _calendars.load_document(CALENDARS, "roman-1962")
        cls.masses = {m["key"]: m for s in cls.document["sections"].values() for m in s["masses"]}
        cls.records, problems = read_sidecar(ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml")
        if problems:
            raise AssertionError(problems)
        cls.propers = SourceFileLoader("exact_primary_propers", str(ROOT / "tools/mass-propers")).load_module()
        command = [sys.executable, "-B", str(ROOT / "tools/mass-propers"), "show",
                   "--calendar", "roman-1962", "--format", "json", "--bible", "clementine-vulgate"]
        for row in cls.fixture["rows"]:
            command += ["--mass", row["mass"]]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        if result.returncode:
            raise AssertionError(result.stderr or result.stdout)
        cls.payloads = {p["mass"]["key"]: p for p in json.loads(result.stdout)["masses"]}

    def node(self, row):
        mass = self.masses[row["mass"]]
        groups = mass.get("forms", [{"id": "main", "name": "", "propers": mass.get("propers", [])}])
        form = next(f for f in groups if f["id"] == row["form_id"])
        self.assertEqual(row["form"], form["name"])
        return [p for p in form["propers"] if p["name"] == row["proper"]][row["occurrence"] - 1]

    def appointed(self, row):
        return [p for p in self.payloads[row["mass"]]["appointed"]
                if p["form_id"] == row["form_id"] and p["name"] == row["proper"]][row["occurrence"] - 1]

    def test_eleven_dated_exact_bodies_keep_independent_source_words_and_permissions(self):
        self.assertEqual(11, len(self.fixture["rows"]))
        self.assertEqual(1733, sum(r["word_count"] for r in self.fixture["rows"]))
        retained = set()
        for row in self.fixture["rows"]:
            with self.subTest(mass=row["mass"], proper=row["proper"]):
                node = self.node(row)
                body = node["text"]
                self.assertEqual(row["text_sha256"], text_sha256(body))
                self.assertEqual(row["word_count"], len(words(body)))
                self.assertEqual("mixed", node["source"])
                self.assertNotIn("text_status", node)
                self.assertFalse({"translations", "actor", "speaker", "role"} & set(node))
                key = LatinKey(row["mass"], row["form"], row["proper"], "", "", row["occurrence"])
                ledger = self.records[key]
                self.assertEqual(row["text_sha256"], ledger["text_sha256"])
                self.assertEqual("collated", ledger["provenance_status"])
                self.assertEqual("editorial-projection-exact-to-target", ledger["relationship"])
                self.assertEqual("permitted", ledger["publication_status"])
                self.assertEqual("public-domain", ledger["publication_basis"])
                self.assertEqual(set(SURFACES), set(ledger["surfaces"]))
                self.assertEqual(row["projection_passage"], ledger["source_id"])
                self.assertEqual(row["target_passage"], ledger["verification_source_id"])
                self.assertEqual([self.fixture["projection_artifact"], self.fixture["historical_artifact"]], ledger["publication_source_ids"])
                projection = record(row["projection_passage"])
                artifact = record(projection["artifact_id"])
                payload = (ROOT / artifact["path"]).read_bytes()
                self.assertEqual(artifact["sha256"], hashlib.sha256(payload).hexdigest())
                a, z = projection["physical_line_ranges"][0]
                self.assertEqual(body, "\n".join(payload.decode().splitlines()[a-1:z]) + "\n")
                retained.add((a, z))
                historical = record(row["source_passage"])
                artifact = record(historical["artifact_id"])
                self.assertEqual("public-domain", artifact["rights_status"])
                payload = (ROOT / artifact["path"]).read_bytes()
                self.assertEqual(artifact["sha256"], hashlib.sha256(payload).hexdigest())
                a, z = historical["physical_line_ranges"][0]
                self.assertEqual(words(body), words("\n".join(payload.decode().splitlines()[a-1:z])))
                target = record(row["target_passage"])
                self.assertEqual("artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf", target["artifact_id"])
                self.assertEqual(["cataloged", "acquired", "inspected", "verified"], target["states"])
        self.assertEqual(11, len(retained))

    def test_printed_appointments_and_other_node_fields_are_preserved(self):
        def has_part(value):
            if isinstance(value, dict):
                return "part" in value or any(has_part(v) for v in value.values())
            return isinstance(value, list) and any(has_part(v) for v in value)
        for row in self.fixture["rows"]:
            with self.subTest(mass=row["mass"]):
                node = self.node(row)
                self.assertEqual(row["preserved_fields"], {k:v for k,v in node.items() if k not in {"source", "text", "notes", "text_status"}})
                self.assertFalse(has_part(node["verses"]), "No source prints a part-verse letter for these appointments")
                appointed = self.appointed(row)
                self.assertIsNone(appointed["taken_from"])
                self.assertEqual(row["text_sha256"], text_sha256(appointed["proper"]["text"]))
                group = self.masses[row["mass"]].get("forms", [{"id":"main", "propers":self.masses[row["mass"]].get("propers",[])}])
                form = next(f for f in group if f["id"] == row["form_id"])
                self.assertEqual(row["source_order"], [p["name"] for p in form["propers"]])

    def test_liturgical_cuts_introductions_and_cento_order_are_literal(self):
        bodies = {row["mass"]: " ".join(self.node(row)["text"].split()) for row in self.fixture["rows"]}
        self.assertTrue(bodies["friday-after-ash-wednesday"].startswith("Haec dicit Dominus Deus: Clama"))
        self.assertTrue(bodies["friday-after-ash-wednesday"].endswith("Quia misericors sum, Dominus Deus tuus."))
        self.assertTrue(bodies["saturday-after-ash-wednesday"].startswith("Haec dicit Dominus Deus: Si abstuleris"))
        self.assertTrue(bodies["saturday-after-ash-wednesday"].endswith("Os enim Domini locutum est."))
        self.assertTrue(bodies["lent-3-wednesday"].endswith("in omni loco in quo memoria fuerit nominis mei."))
        self.assertTrue(bodies["lent-3-monday"].endswith("nisi tantum in Israel."))
        self.assertIn("Date nobis aquam, ut bibamus.", bodies["lent-3-friday"])
        self.assertIn("Domine Deus, audi clamorem hujus populi", bodies["lent-3-friday"])
        self.assertIn("Profiteor hodie coram Domino Deo tuo, qui exaudivit nos", bodies["pentecost-ember-saturday"])
        self.assertNotIn("Suscipiensque", bodies["pentecost-ember-saturday"])
        self.assertTrue(bodies["pentecost-ember-saturday"].endswith("quae Dominus Deus tuus dederit tibi."))
        self.assertTrue(bodies["epiphany-2"].endswith("sed humilibus consentientes."))
        self.assertTrue(bodies["epiphany-3"].startswith("Fratres: Nolite esse prudentes apud vosmetipsos:"))
        self.assertTrue(bodies["advent-1"].endswith("sed induimini Dominum Jesum Christum."))
        self.assertTrue(bodies["s-nicolai-episcopi-confessoris"].endswith("quasi rationem pro animabus vestris reddituri."))
        cento = bodies["s-gregorii-thaumaturgi-episcopi-confessoris"]
        previous = -1
        for phrase in ["Ecce sacerdos magnus", "Non est inventus similis illi", "Ideo jurejurando", "Benedictionem omnium gentium", "Agnovit eum", "Magnificavit eum", "Statuit illi", "Fungi sacerdotio", "in odorem suavitatis."]:
            found = cento.index(phrase)
            self.assertGreater(found, previous)
            previous = found

    def test_whole_bible_expansions_cannot_replace_a_permitted_missal_body(self):
        for row in self.fixture["rows"]:
            with self.subTest(mass=row["mass"]):
                node = self.node(row)
                passages = self.payloads[row["mass"]]["bible"]["passages"]
                bible = " ".join(passages[v["ref"]]["text"] for v in node["verses"])
                self.assertNotEqual(words(node["text"]), words(bible))
                key = LatinKey(row["mass"], row["form"], row["proper"], "", "", row["occurrence"])
                self.assertTrue(decision_for(key, node["text"], self.records).permits(SURFACES))
                rejected = decision_for(key, bible, self.records)
                self.assertFalse(rejected.permits(SURFACES))
                self.assertIn("stale text hash", rejected.reason)
                changed = copy.deepcopy(node)
                changed["text"] = bible
                self.assertIsNone(sanitize_proper(changed, key, self.records, SURFACES).get("text"))

    def test_exact_english_absences_and_coverage_do_not_borrow_bible_english(self):
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
        child = tomllib.loads((ROOT / "src/sources/inventories/roman-pre-1955-proper-translations-v1.toml").read_text())
        identity = lambda r: (r["mass"], r.get("form_id", "main"), r["proper"], r.get("cycle", "all"), r.get("occurrence",1), r.get("lang","en"), r.get("extent","body"))
        for row in self.fixture["rows"]:
            with self.subTest(mass=row["mass"]):
                address = (row["mass"],row["form_id"],row["proper"],"all",row["occurrence"],"en","body")
                owned = [(g,r) for g in ("entries","untranslated") for r in ledger.get(g,[]) if identity(r)==address]
                self.assertEqual(1,len(owned))
                self.assertEqual("untranslated",owned[0][0])
                self.assertEqual({"kind":"no-exemplar"},owned[0][1]["reason"])
                self.assertFalse([r for g in ("entries","untranslated") for r in child.get(g,[]) if identity(r)==address])
                proper = self.appointed(row)["proper"]
                self.assertFalse(proper.get("translations"))
                self.assertTrue(proper.get("untranslated"))
                owner = dict(proper, citations=[{"ref":v["ref"]} for v in proper["verses"]])
                unit = _missal_coverage.unit(owner,target_id="target",occurrence_id="occurrence",
                    absence_kinds=self.propers.body_absence_kinds([owned[0][1]],"all"))
                languages = {r["lang"]:r for r in unit["languages"]}
                self.assertEqual(("available","collated","exact-target","public-domain"),tuple(languages["la"][k] for k in ("availability","collation","relationship","publication_basis")))
                self.assertEqual("not-sourced",languages["en"]["availability"])
                self.assertEqual("bible-reconstruction",unit["scripture_component"]["relationship"])
        for calendar in ("roman-1962","roman-pre-1955"):
            report = self.propers.english_coverage(CALENDARS,calendar)
            self.assertEqual((0,0,0,0),tuple(report[k] for k in ("unaccounted","unmatched_records","stale_translation_records","outside_the_ledger")))

    def test_english_reading_view_labels_the_full_bible_expansion_separately(self):
        result = subprocess.run(
            [sys.executable,"-B",str(ROOT/"tools/mass-propers"),"show",
             "--calendar","roman-1962","--mass","advent-1","--lang","en",
             "--bible","douay-rheims","--format","text"],
            cwd=ROOT,text=True,capture_output=True,check=False)
        self.assertEqual(0,result.returncode,result.stderr)
        epistle = result.stdout.split("\nEpistle\n",1)[1].split("\nGradual\n",1)[0]
        self.assertIn("Romans 13:11-14",epistle)
        self.assertIn("Bible reconstruction · Missal wording not established",epistle)
        self.assertIn("provision for the flesh in its concupiscences.",epistle)
        self.assertIn("en translation unavailable: not yet sourced",epistle)
        self.assertNotIn("Fratres:",epistle)


if __name__ == "__main__":
    unittest.main()
