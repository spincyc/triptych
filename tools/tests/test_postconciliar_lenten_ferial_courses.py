"""OLM1981 nn.236/243/250, n252's explicit gap, and n238 source bounds.

Appointment facts only: no source words, generated fixtures or inferred actual
Sunday use. --projection feeds the paired browser-contract test from raw owners.
"""
from __future__ import annotations

import argparse
import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars as C
import _proper_latin as L

CALENDARS = ROOT / "src/sources/calendars"
INVENTORIES = ROOT / "src/sources/inventories"
ENGLISH = "postconciliar-proper-translations-v1.toml"
LATIN = "postconciliar-proper-latin-provenance-v1.toml"
ARTIFACT = "artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e"
FACT = "lent-5-sunday-john-8-1-11-actually-read"
DAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday")
KEYS = tuple(f"lent-{week}-{day}" for week in (3, 4, 5) for day in DAYS)
ROLES = ("First Reading", "Responsorial Psalm", "Verse Before the Gospel", "Gospel")
COURSES = {
    3: (236, "Exodus 17:1-7", "Psalm 94:1-2, 6-7, 8-9", "John 4:5-42"),
    4: (243, "Micah 7:7-9", "Psalm 26:1, 7-8a, 8b-9abc, 13-14", "John 9:1-41"),
    5: (250, "2 Kings 4:18b-21, 32-37", "Psalm 16:1, 6-7, 8b, 15", "John 11:1-45"),
}


def tool(name):
    loader = SourceFileLoader("_lenten_courses_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


def document():
    return yaml.safe_load((CALENDARS / "postconciliar/propers.yaml").read_text())


def projection(doc):
    masses = C.mass_index(doc)
    result = []
    for key in KEYS:
        mass = masses[key]
        appointed, problems = C.resolve_propers(doc, mass, appointments=True)
        assert not problems, (key, problems)
        result.append({"key": key, "propers": [p for _, p, _ in appointed
                       if p["name"] in (*ROLES, "First Reading (shorter form)")],
                       "proper_source_paths": C.public_proper_source_paths(doc, mass)})
    return {"calendar": "postconciliar", "masses": result}


def target_rows(doc, member):
    appointment = member["appointment"]
    return [p for p in C.mass_index(doc)[appointment["mass"]]["propers"]
            if p["name"] == appointment["proper"]][appointment["occurrence"] - 1]


class LentenFerialCourseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = document()
        cls.masses = C.mass_index(cls.doc)
        cls.mp, cls.check, cls.citations = (tool(n) for n in ("mass-propers", "check-calendar-masses", "citations"))
        cls.english_text = (INVENTORIES / ENGLISH).read_text()
        cls.negative_rows = [r for r in tomllib.loads(cls.english_text)["untranslated"]
                             if r["mass"] in KEYS and r["proper"] == "Verse Before the Gospel"
                             and (r["occurrence"] == 2 or r["mass"] == "lent-5-tuesday")]
        cls.public = cls.mp.calendar_structure(CALENDARS, "postconciliar", cls.mp.book_tokens())
        cls.public_masses = {m["key"]: m for m in cls.public["masses"]}

    def test_exact_complete_courses_and_no_sunday_or_missal_borrow(self):
        paths = 0
        for key in KEYS:
            mass = self.masses[key]
            week = int(key.split("-")[1])
            number, reading, psalm, gospel = COURSES[week]
            relations = C.public_proper_source_paths(self.doc, mass)
            self.assertEqual(len(relations), 1)
            relation = relations[0]
            self.assertEqual((relation["id"], relation["form_id"], relation["source_edition"]),
                             (key + "-reading-course", "main", "postconciliar"))
            optional = next(p for p in relation["paths"] if p["id"] == "course-" + str(number))
            self.assertEqual(optional["standing"], "optional")
            self.assertEqual(optional["id"], "course-" + str(number))
            self.assertEqual(optional["calendar_cycles"], {"family": "sunday", "in": ["A", "B", "C"]})
            self.assertNotIn("when", optional, "Sunday nonuse is a preference, not eligibility")
            self.assertEqual([m["appointment"]["proper"] for m in optional["members"]], list(ROLES))
            owners = [target_rows(self.doc, m) for m in optional["members"]]
            if key == "lent-3-thursday":
                psalm = "Psalm 95:1-2, 6-7, 8-9"
            for owner, ref in zip((owners[0], owners[1], owners[3]), (reading, psalm, gospel)):
                self.assertEqual(owner["verses"], [self.citations.parse_citation(ref)])
                self.assertEqual(owner["source"], "scripture")
                self.assertNotIn("cycles", owner)
                self.assertNotIn("weekday_cycles", owner)
                self.assertNotIn("takes_from", owner)
            self.assertEqual(owners[1].get("psalm_numbering", self.doc["psalm_numbering"]),
                             "hebrew" if key == "lent-3-thursday" else "vulgate")
            # The shared Thursday owner is Hebrew95, not a duplicate Vulgate94.
            if key == "lent-3-thursday":
                self.assertEqual(owners[1]["verses"], [self.citations.parse_citation("Psalm 95:1-2, 6-7, 8-9")])
            self.assertNotIn("forms", mass)
            self.assertFalse(any(p["name"] == "Second Reading" for p in mass["propers"]))
            self.assertEqual(len(relation["paths"]), 7 if key == "lent-5-monday" else 2)
            paths += len(relation["paths"])
            for p in mass["propers"]:
                for derived in ("appointment_identity", "source_path_relation", "appointment_applicability", "source_edition"):
                    self.assertNotIn(derived, p)
        self.assertEqual(paths, 41)

    def test_all_nineteen_composed_owners_are_typed_and_untranscribed(self):
        expected = {(key, 2) for key in KEYS} | {("lent-5-tuesday", 1)}
        self.assertEqual({(r["mass"], r["occurrence"]) for r in self.negative_rows}, expected)
        self.assertEqual(len(self.negative_rows), 19)
        for row in self.negative_rows:
            proper = [p for p in self.masses[row["mass"]]["propers"]
                      if p["name"] == "Verse Before the Gospel"][row["occurrence"] - 1]
            self.assertEqual(proper["source"], "composed")
            self.assertEqual(proper["text_status"], {
                "state": "unavailable", "scope": "proper-body", "body_status": "held-unpublished",
                "reasons": [{"kind": "rights-withheld", "source_id": ARTIFACT}]})
            self.assertEqual({k: row[k] for k in ("form_id", "proper", "cycle", "extent", "lang", "availability", "reason")},
                             {"form_id": "main", "proper": "Verse Before the Gospel", "cycle": "all",
                              "extent": "body", "lang": "en", "availability": "unavailable",
                              "reason": {"kind": "no-exemplar"}})
            for field in ("text", "verses", "incipit", "translations", "takes_from"):
                self.assertNotIn(field, proper)
            for field in ("source_id", "witness_artifact_id", "witness_passage_id", "incipit", "surfaces", "quarantined_text_sha256"):
                self.assertNotIn(field, row)

    def test_lent_five_tuesday_gap_is_a_distinct_native_fourth_role(self):
        mass = self.masses["lent-5-tuesday"]
        native, optional = mass["proper_source_paths"][0]["paths"]
        for selected, occurrence in ((native, 1), (optional, 2)):
            self.assertEqual([m["appointment"]["proper"] for m in selected["members"]], list(ROLES))
            verse = selected["members"][2]
            self.assertEqual(verse["appointment"]["occurrence"], occurrence)
            self.assertEqual(target_rows(self.doc, verse)["text_status"]["state"], "unavailable")
        self.assertEqual(native["choices"]["verse-before-gospel"], "ferial")
        self.assertEqual(optional["choices"]["verse-before-gospel"], "course-250")

    def test_monday_native_cross_product_and_shared_psalm_owners(self):
        mass = self.masses["lent-5-monday"]
        for name, ref in (
            ("First Reading", "Daniel 13:1-9, 15-17, 19-30, 33-62"),
            ("First Reading (shorter form)", "Daniel 13:41c-62"),
        ):
            native = next(p for p in mass["propers"] if p["name"] == name)
            self.assertEqual(native["verses"], [self.citations.parse_citation(ref)])
        relation = self.masses["lent-5-monday"]["proper_source_paths"][0]
        self.assertEqual([p["id"] for p in relation["paths"]], [
            base + "-" + daniel for base in ("john-8-1-11-ab", "john-8-1-11-c", "john-8-12-20-c")
            for daniel in ("longer", "shorter")] + ["course-250"])
        for path in relation["paths"][:6]:
            self.assertEqual(len(path["members"]), 4)
            member = path["members"][0]["appointment"]
            self.assertEqual(member["proper"], "First Reading (shorter form)" if path["id"].endswith("-shorter") else "First Reading")
            self.assertEqual(member["occurrence"], 1)
            self.assertEqual(path["calendar_cycles"]["in"], ["A", "B"] if "-ab-" in path["id"] else ["C"])
            if path["id"].startswith("john-8-12-20"):
                self.assertEqual(path["standing"], "optional")
                self.assertEqual(path["when"], {"fact": FACT, "is": True})
            else:
                self.assertEqual(path["standing"], "principal")
                self.assertNotIn("when", path)
        thursday = self.masses["lent-3-thursday"]
        psalms = [p for p in thursday["propers"] if p["name"] == "Responsorial Psalm"]
        self.assertEqual(len(psalms), 1)
        for path in thursday["proper_source_paths"][0]["paths"]:
            self.assertEqual(path["members"][1]["appointment"]["occurrence"], 1)
            self.assertNotIn("responsorial-psalm", path["choices"])

    def test_english_and_latin_census_have_exact_terminal_owners(self):
        coverage = self.mp.english_coverage(CALENDARS, "postconciliar")
        self.assertEqual({k: coverage[k] for k in ("slots", "with_english", "ledgered_untranslated", "rights_restricted")},
                         {"slots": 561, "with_english": 113, "ledgered_untranslated": 448, "rights_restricted": 0})
        for field in ("unaccounted", "outside_the_ledger", "unmatched_records", "stale_translation_records"):
            self.assertEqual(coverage[field], 0)
        source_records, trouble = self.check.source_records()
        self.assertFalse(trouble)
        records, problems = L.publication_records(CALENDARS, "postconciliar",
            registered_sources={k: dict(v.data) for k, v in source_records.items()})
        self.assertEqual(problems, [])
        self.assertEqual(len(records), 329)
        self.assertEqual(len(list(L.body_owners(self.doc))), 329)
        self.assertEqual(L.sidecar_problems([CALENDARS / "postconciliar/propers.yaml"],
            inventory_root=INVENTORIES, required=True, registered_source_ids=self.check.source_ids()[0]), [])

    def test_public_and_actual_terminal_owners_cannot_fall_back_to_bible_bodies(self):
        for key in KEYS:
            args = argparse.Namespace(root=CALENDARS, calendar="postconciliar", mass=key,
                                      lang="en", bible=None, bible_root=ROOT / "src/sources/bibles")
            shown = self.mp.run_show_one(args)
            wanted = {r["occurrence"] for r in self.negative_rows if r["mass"] == key}
            found = 0
            for index, appointed in enumerate(shown["appointed"]):
                proper = appointed["proper"]
                if proper["name"] != "Verse Before the Gospel" or proper["appointment_identity"]["occurrence"] not in wanted:
                    continue
                found += 1
                self.assertEqual(proper["text_status"], {"state": "unavailable", "scope": "proper-body"})
                self.assertEqual(self.mp.select_texts(proper, "en", availability=args.absences[index]),
                                 [("", "", "en translation unavailable: not yet sourced; Latin text unavailable")])
                public = next(p for p in self.public_masses[key]["propers"]
                              if p.get("appointment_identity") == proper["appointment_identity"])
                self.assertFalse(public.get("citations"))
                for field in ("text", "incipit", "translations"):
                    self.assertFalse(public.get(field))
                self.assertEqual({k: public["latin"][k] for k in ("state", "held", "available")},
                                 {"state": "unavailable", "held": False, "available": False})
                self.assertFalse(public["latin"].get("text"))
                self.assertEqual({p["lang"]: p["status"] for p in public["languages"]},
                                 {"la": "unavailable", "en": "unavailable"})
                self.assertTrue(all(not p["held"] and not p["available"] for p in public["languages"]))
            self.assertEqual(found, len(wanted))

    def test_five_bad_english_controls_and_two_bad_latin_controls_refuse(self):
        # Full source documents; only temporary sidecars/owners are malformed.
        # Registry/publication owners remain production validators, never mocks.
        # Render all existing rows from their original bytes, replacing only the
        # last new target where necessary. No positive entry is reserialized.
        blocks = self.english_text.split("\n[[untranslated]]")
        prefix = blocks[0]
        for block in blocks[1:]:
            row = tomllib.loads("[[untranslated]]" + block)["untranslated"][0]
            if row not in self.negative_rows:
                prefix += "\n[[untranslated]]" + block
        def render(rows):
            text = prefix
            for row in rows:
                text += "\n[[untranslated]]\n"
                for key, value in row.items():
                    if key != "reason":
                        text += f"{key} = {json.dumps(value)}\n"
                text += "[untranslated.reason]\n"
                for key, value in row["reason"].items():
                    text += f"{key} = {json.dumps(value)}\n"
            return text
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch", prefix="lenten-course-controls-") as folder:
            temp = Path(folder)
            inv = temp / "inventories"
            inv.mkdir()
            path = temp / "postconciliar/propers.yaml"
            path.parent.mkdir()
            for mutation, message in (
                ("wrong-occurrence", "out of range"), ("wrong-cycle", "no source-owned proper"),
                ("no-exemplar-source", "cannot name source_id"), ("body-incipit", "must not carry incipit"),
                ("Bible-substitution", "exact English rights-withheld body witness"),
            ):
                with self.subTest(mutation=mutation):
                    doc = copy.deepcopy(self.doc)
                    rows = copy.deepcopy(self.negative_rows)
                    if mutation == "wrong-occurrence": rows[0]["occurrence"] = 99
                    if mutation == "wrong-cycle": rows[0]["cycle"] = "A"
                    if mutation == "no-exemplar-source": rows[0]["reason"]["source_id"] = ARTIFACT
                    if mutation == "body-incipit": rows[0]["incipit"] = "invalid-test-marker"
                    if mutation == "Bible-substitution":
                        verse = [p for p in C.mass_index(doc)["lent-3-monday"]["propers"] if p["name"] == "Verse Before the Gospel"][1]
                        verse["source"] = "scripture"
                        verse.pop("text_status")
                        verse["verses"] = [self.citations.parse_citation("John 4:42, 15")]
                    path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
                    (inv / ENGLISH).write_text(render(rows))
                    with patch.object(self.check, "OVERLAY_DIR", inv):
                        errors, _ = self.check.overlay_problems([path])
                    self.assertIn(message, "\n".join(errors))
            for mutation, message in (
                ("missing-held-marker", "missing entry"), ("invented-removed-hash", "orphan entry"),
            ):
                with self.subTest(mutation=mutation):
                    doc = copy.deepcopy(self.doc)
                    latin = (INVENTORIES / LATIN).read_text()
                    if mutation == "missing-held-marker":
                        verse = [p for p in C.mass_index(doc)["lent-3-monday"]["propers"] if p["name"] == "Verse Before the Gospel"][1]
                        verse["text_status"].pop("body_status")
                    else:
                        latin += '\n[[entries]]\nmass = "lent-3-monday"\nform = ""\nproper = "Verse Before the Gospel"\ncourse = ""\ncycle = ""\noccurrence = 1\nbody_status = "removed"\ntext_sha256 = "' + "0" * 64 + '"\n'
                    path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
                    (inv / LATIN).write_text(latin)
                    errors = L.sidecar_problems([path], inventory_root=inv, required=True,
                                               registered_source_ids=self.check.source_ids()[0])
                    self.assertIn(message, "\n".join(errors))
            # A genuinely omitted exact negative row must become unaccounted.
            (inv / ENGLISH).write_text(render(self.negative_rows[:-1]))
            with patch.object(self.mp, "inventory_root", return_value=inv):
                self.assertEqual(self.mp.english_coverage(CALENDARS, "postconciliar")["unaccounted"], 1)

    def test_fresh_browser_admission_560_plus_explicit_condition_controls(self):
        result = subprocess.run(["node", str(ROOT / "tools/tests/test_postconciliar_lenten_ferial_courses.cjs")],
                                input=json.dumps(projection(self.doc)), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual((report["executions"], report["negativeControls"], report["staticForms"]), (560, 202, 18))
        self.assertEqual((report["additionalControls"], report["additionalExecutions"],
                          report["conditionExecutions"], report["conditionNegatives"]),
                         (150, 480, 360, 284))

    def test_native_finding_aid_49_said_and_five_displacements_not_an_ordo(self):
        days, rubrics = tool("calendar-days"), tool("calendar-rubrics")
        calendar = days.load_calendar(CALENDARS, "postconciliar")
        built = days.build_years(calendar, list(range(2025, 2030)))
        days.with_fixed(calendar, list(range(2025, 2029)))
        years = {y: days.year_document(calendar, y, built) for y in (2026, 2027, 2028)}
        rb, problems, _ = rubrics.build(CALENDARS, "postconciliar")
        self.assertEqual(problems, [])
        cases = []
        for year, yd in years.items():
            for date, candidates in yd["days"].items():
                wanted = {p["key"] for p in candidates} & set(KEYS)
                if wanted:
                    cases.append({"id": date, "date": date, "year": yd, "rubrics": rb[0], "wanted": wanted})
        results = rubrics.run_model({"cases": [
            {k: case[k] for k in ("id", "date", "year", "rubrics")} for case in cases]})["results"]
        said = {2026: 0, 2027: 0, 2028: 0}
        displaced = {}
        for case, result in zip(cases, results):
            self.assertTrue(result["ok"])
            active = {p["key"] for option in result["result"]["options"] for p in option["readable"] if p["state"] == "said"}
            if active & case["wanted"]:
                said[int(case["date"][:4])] += 1
            else:
                displaced[case["date"]] = (case["wanted"], active)
        self.assertEqual(len(cases), 54)
        self.assertEqual(said, {2026: 16, 2027: 17, 2028: 16})
        for date, feria, feast in (
            ("2026-03-19", "lent-4-thursday", "joseph"),
            ("2026-03-25", "lent-5-wednesday", "annunciation"),
            ("2027-03-19", "lent-5-friday", "joseph"),
            ("2028-03-20", "lent-3-monday", "joseph"),
            ("2028-03-25", "lent-3-saturday", "annunciation"),
        ):
            self.assertEqual(displaced[date][0], {feria})
            self.assertTrue(any(feast in key for key in displaced[date][1]))
            self.assertNotIn(feria, displaced[date][1])
        self.assertEqual(len(displaced), 5)


if __name__ == "__main__":
    if sys.argv[1:] == ["--projection"]:
        print(json.dumps(projection(document())))
    else:
        unittest.main()
