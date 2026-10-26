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
from tools.tests import _source_batch_guards as source_batch
from tools.tests._source_recovery_assertions import assert_current_english_owner
from tools.tests.test_roman_1962_english_recovery_append209_strict165_20261023 import (
    ARTIFACT as STRICT_ARTIFACT, ARTIFACT_SHA as STRICT_ARTIFACT_SHA,
    ORACLES as STRICT_ENGLISH,
)
from tools.tests.test_roman_1962_english_recovery_append209_orth43_20261023 import (
    ARTIFACT as ORTH_ARTIFACT, ARTIFACT_SHA as ORTH_ARTIFACT_SHA,
    ORACLES as ORTH_ENGLISH,
)
from tools.tests.test_roman_1962_english_recovery_core193_20261023 import (
    ARTIFACT as CORE_ARTIFACT, ARTIFACT_SHA as CORE_ARTIFACT_SHA,
    ORACLES as CORE_ENGLISH,
)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars
import _missal_coverage
from _proper_latin import (
    LatinKey, SURFACES, decision_for, read_sidecar, sanitize_proper, text_sha256,
)

FIXTURE = ROOT / "tools/tests/fixtures/roman-1962-exact-primary-bodies.json"
CALENDARS = ROOT / "src/sources/calendars"
ENGLISH_LEDGER = ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml"
HISTORICAL_ABSENCES_SHA256 = "18bde347038bf4d3d1d946dc63e3419c83c68d41157138bc4495f4c6cadcface"
ENGLISH_RECOVERIES = (
    (STRICT_ENGLISH, STRICT_ARTIFACT, STRICT_ARTIFACT_SHA),
    (ORTH_ENGLISH, ORTH_ARTIFACT, ORTH_ARTIFACT_SHA),
    (CORE_ENGLISH, CORE_ARTIFACT, CORE_ARTIFACT_SHA),
)


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
        cls.english_ledger = tomllib.loads(ENGLISH_LEDGER.read_text())
        cls.english_overlay, _, stale, cls.witnesses = cls.propers.translation_overlay("roman-1962", CALENDARS)
        if stale:
            raise AssertionError(stale)

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

    def english_key(self, row):
        return (row["mass"], row["form_id"], row["proper"], "all", row["occurrence"])

    def historical_absence(self, row):
        scope = self.fixture["historical_english_absence_scope"]
        self.assertEqual("d648c842acf03fb345c22d6e5b54b7645e3c35b0", scope["source_revision"])
        self.assertEqual("f8dfe360c4af0dd7af40044d6979af5ad80449ad140b1fad0864bc93d8a38130", scope["source_ledger_sha256"])
        self.assertEqual(HISTORICAL_ABSENCES_SHA256, source_batch.digest(source_batch.canonical(scope["rows"])))
        return scope["rows"][source_batch.canonical(self.english_key(row))]

    def assert_english_owner(self, row, ledger):
        key = self.english_key(row)
        owned = assert_current_english_owner(
            self, key, ledger, self.propers, self.english_overlay, self.witnesses,
            latin_sha256=row["text_sha256"], independent_oracles=ENGLISH_RECOVERIES)
        if key == ("advent-1", "main", "Epistle", "all", 1):
            self.assertEqual(("untranslated", self.historical_absence(row)), owned)
        return owned

    def test_exact_english_absences_and_coverage_do_not_borrow_bible_english(self):
        # These ten recoveries are bound to accepted source bytes and independent
        # literal Latin/English oracles. Advent I remains an exact, explicit gap.
        source_batch.assert_current_english_entries(self.english_overlay)
        child = tomllib.loads((ROOT / "src/sources/inventories/roman-pre-1955-proper-translations-v1.toml").read_text())
        identity = lambda r: (r["mass"], r.get("form_id", "main"), r["proper"], r.get("cycle", "all"), r.get("occurrence",1), r.get("lang","en"), r.get("extent","body"))
        for row in self.fixture["rows"]:
            with self.subTest(mass=row["mass"]):
                address = (row["mass"],row["form_id"],row["proper"],"all",row["occurrence"],"en","body")
                group, entry = self.assert_english_owner(row, self.english_ledger)
                self.assertFalse([r for g in ("entries","untranslated") for r in child.get(g,[]) if identity(r)==address])
                proper = self.appointed(row)["proper"]
                if group == "entries":
                    published = [r for r in proper.get("translations", []) if r["lang"] == "en"]
                    self.assertEqual(1, len(published))
                    self.assertEqual(entry["translations"][0]["text"], published[0]["text"])
                    self.assertTrue(published[0].get("caution"))
                    self.assertFalse(proper.get("untranslated"))
                else:
                    self.assertFalse(proper.get("translations"))
                    self.assertTrue(proper.get("untranslated"))
                owner = dict(proper, citations=[{"ref":v["ref"]} for v in proper["verses"]])
                unit = _missal_coverage.unit(owner,target_id="target",occurrence_id="occurrence",
                    witnesses=self.witnesses,
                    absence_kinds=self.propers.body_absence_kinds([entry] if group == "untranslated" else [],"all"))
                languages = {r["lang"]:r for r in unit["languages"]}
                self.assertEqual(("available","collated","exact-target","public-domain"),tuple(languages["la"][k] for k in ("availability","collation","relationship","publication_basis")))
                self.assertEqual("available" if group == "entries" else "not-sourced",languages["en"]["availability"])
                self.assertEqual("bible-reconstruction",unit["scripture_component"]["relationship"])
                # The original absence assertions concern their pinned 2026-10-20
                # source scope, rather than contradicting later source admission.
                historical = self.historical_absence(row)
                self.assertEqual({"kind": "no-exemplar"}, historical["reason"])
                old_owner = dict(owner, translations=[], untranslated=self.propers.public_untranslated_records([historical]))
                old_unit = _missal_coverage.unit(old_owner,target_id="target",occurrence_id="occurrence",
                    absence_kinds=self.propers.body_absence_kinds([historical], "all"))
                self.assertEqual("not-sourced", next(r for r in old_unit["languages"] if r["lang"] == "en")["availability"])
        for calendar in ("roman-1962","roman-pre-1955"):
            report = self.propers.english_coverage(CALENDARS,calendar)
            self.assertEqual((0,0,0,0),tuple(report[k] for k in ("unaccounted","unmatched_records","stale_translation_records","outside_the_ledger")))

    def test_recovered_english_rejects_changed_body_and_publication_proof(self):
        for row in self.fixture["rows"]:
            if row["mass"] == "advent-1":
                continue
            _, entry = self.assert_english_owner(row, self.english_ledger)
            for defect in ("body", "proof"):
                broken = copy.deepcopy(entry)
                if defect == "body":
                    broken["translations"][0]["text"] += " Amen."
                else:
                    broken["publication_passage_id"] += "-unproved"
                with self.subTest(mass=row["mass"], defect=defect):
                    with self.assertRaises(ValueError):
                        self.propers.validate_translation_publication_binding(broken, CALENDARS, ENGLISH_LEDGER, self.witnesses)

    def test_original_gap_and_recovered_owners_cannot_exchange_states(self):
        for row in self.fixture["rows"]:
            group, entry = self.assert_english_owner(row, self.english_ledger)
            broken = copy.deepcopy(self.english_ledger)
            broken[group].remove(entry)
            if group == "entries":
                broken["untranslated"].append(self.historical_absence(row))
            else:
                changed = copy.deepcopy(entry)
                changed["reason"] = {"kind": "witness-gap"}
                broken[group].append(changed)
            with self.subTest(mass=row["mass"]):
                with self.assertRaises(AssertionError):
                    self.assert_english_owner(row, broken)

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
