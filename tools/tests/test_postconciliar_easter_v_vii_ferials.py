"""OLM nn.285-302: bounded source fidelity, fifteen held units, no body upgrade."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import yaml

if __package__:
    from .test_postconciliar_easter_ferials import context, ROOT, CALENDARS, INVENTORIES, ARTIFACT, L, P, C, tool
else:
    from test_postconciliar_easter_ferials import context, ROOT, CALENDARS, INVENTORIES, ARTIFACT, L, P, C, tool

DAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday")
KEYS = tuple(f"easter-{week}-{day}" for week in (5, 6, 7) for day in DAYS)
PRESERVED = {"easter-6-wednesday": "John 14:16", "easter-6-saturday": "John 16:28",
             "easter-7-tuesday": "John 14:16"}
HELD = set(KEYS) - PRESERVED.keys()
PASSAGE = ROOT / ("src/sources/works/catholic-church/ordo-lectionum-missae/editions/"
                 "latin-editio-typica-altera-1981/passages/easter-ferial-courses-285-302.toml")
# Independently collated appointment coordinates, not OLM body/rubric wording.
# N.285's printed 113B restart is first normalized to full Vulgate coordinates.
CORE = (
 ("Acts 14:5-18", "Psalm 113:9-10, 11-12, 23-24", "John 14:21-26"),
 ("Acts 14:19-28", "Psalm 144:10-11, 12-13ab, 21", "John 14:27-31a"),
 ("Acts 15:1-6", "Psalm 121:1-2, 3-4a, 4b-5", "John 15:1-8"),
 ("Acts 15:7-21", "Psalm 95:1-2a, 2b-3, 10", "John 15:9-11"),
 ("Acts 15:22-31", "Psalm 56:8-9, 10-12", "John 15:12-17"),
 ("Acts 16:1-10", "Psalm 99:2, 3, 5", "John 15:18-21"),
 ("Acts 16:11-15", "Psalm 149:1-2, 3-4, 5-6a, 9b", "John 15:26-16:4a"),
 ("Acts 16:22-34", "Psalm 137:1-2a, 2bc-3, 7c-8", "John 16:5-11"),
 ("Acts 17:15, 22-18:1", "Psalm 148:1-2, 11-12ab, 12c-14a, 14bcd", "John 16:12-15"),
 ("Acts 18:1-8", "Psalm 97:1, 2-3ab, 3cd-4", "John 16:16-20"),
 ("Acts 18:9-18", "Psalm 46:2-3, 4-5, 6-7", "John 16:20-23a"),
 ("Acts 18:23-28", "Psalm 46:2-3, 8-9, 10", "John 16:23b-28"),
 ("Acts 19:1-8", "Psalm 67:2-3, 4-5ac, 6-7ab", "John 16:29-33"),
 ("Acts 20:17-27", "Psalm 67:10-11, 20-21", "John 17:1-11a"),
 ("Acts 20:28-38", "Psalm 67:29-30, 33-35a, 35b-36c", "John 17:11b-19"),
 ("Acts 22:30; 23:6-11", "Psalm 15:1-2a, 5, 7-8, 9-10, 11", "John 17:20-26"),
 ("Acts 25:13b-21", "Psalm 102:1-2, 11-12, 19-20ab", "John 21:15-19"),
 ("Acts 28:16-20, 30-31", "Psalm 10:4, 5, 7", "John 21:20-25"),
)
BIBLES = ("douay-rheims", "douay-rheims-american-1899", "clementine-vulgate",
          "catholic-public-domain-version", "king-james-version",
          "world-english-bible-catholic", "revised-version-1895")


class EasterVViiFerialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc, cls.masses, cls.mp, cls.index, cls.canon, cls.tables, cls.public = context()
        cls.public_masses = {m["key"]: m for m in cls.public["masses"]}

    def test_all54_core_bounds_parts_and_existing_acts14_carriers(self):
        special = {"Acts 14:5-18": "Acts 14:5-17", "Acts 14:19-28": "Acts 14:18-27"}
        count = 0
        for key, refs in zip(KEYS, CORE):
            for role, ref in zip(("First Reading", "Responsorial Psalm", "Gospel"), refs):
                proper, = [p for p in self.masses[key]["propers"] if p["name"] == role]
                self.assertEqual(proper["source"], "scripture")
                self.assertNotIn("cycles", proper)
                self.assertNotIn("weekday_cycles", proper)
                expected = self.canon.parse_citation(ref)
                if role == "Responsorial Psalm":
                    expected["ranges"] = [piece for span in expected["ranges"]
                        for piece in P.convert_range_whole(expected["book"], span["begin"], span["end"],
                                                          "vulgate", "hebrew")]
                actual, = proper["verses"]
                self.assertEqual(actual["book"], expected["book"])
                self.assertEqual(actual["ranges"], expected["ranges"], (key, role))
                self.assertEqual(actual, self.canon.parse_citation(actual["ref"]))
                projection = self.mp.citation_structure(actual,
                    proper.get("psalm_numbering", self.doc["psalm_numbering"]),
                    self.mp.book_tokens(), self.tables)
                target = self.canon.parse_citation(special.get(ref, ref))
                self.assertEqual(projection["loci"]["vulgate"], [locus for span in target["ranges"]
                    for locus in self.mp.range_to_loci(span["begin"], span["end"])])
                count += 1
        self.assertEqual(count, 54)
        control = self.canon.parse_citation("Acts 14:21b-27")
        ranges, error = self.tables["vulgate"].apply(control, control["ranges"])
        self.assertFalse(error)
        self.assertEqual(ranges, self.canon.parse_citation("Acts 14:20b-26")["ranges"])
        for ref in special:
            entry = self.canon.parse_citation(ref)
            self.assertEqual(self.tables["hebrew"].apply(entry, entry["ranges"]),
                             (entry["ranges"], ""))

    def test_all18_whole_unit_classifications_and_exact_negative_owners(self):
        rows = tomllib.loads((INVENTORIES / "postconciliar-proper-translations-v1.toml").read_text())["untranslated"]
        rows = [r for r in rows if r["mass"] in KEYS and r["proper"] == "Gospel Acclamation"]
        self.assertEqual(len(rows), 15)
        self.assertEqual({r["mass"] for r in rows}, HELD)
        raw = (CALENDARS / "postconciliar/propers.yaml").read_text()
        for key in KEYS:
            proper, = [p for p in self.masses[key]["propers"] if p["name"] == "Gospel Acclamation"]
            if key in PRESERVED:
                self.assertEqual(proper["source"], "scripture")
                self.assertEqual(proper["verses"], [self.canon.parse_citation(PRESERVED[key])])
                continue
            self.assertEqual(proper["source"], "composed")
            self.assertEqual(proper["text_status"], {"state": "unavailable", "scope": "proper-body",
                "body_status": "held-unpublished",
                "reasons": [{"kind": "rights-withheld", "source_id": ARTIFACT}]})
            for field in ("text", "incipit", "translations", "verses", "takes_from", "cycles", "weekday_cycles"):
                self.assertNotIn(field, proper)
            self.assertIn('name: "Gospel Acclamation"', raw.split("    - key: " + key + "\n", 1)[1].split("    - key:", 1)[0])
            row, = [r for r in rows if r["mass"] == key]
            self.assertEqual({k: row[k] for k in ("form_id", "cycle", "occurrence", "extent", "lang", "reason")},
                {"form_id": "main", "cycle": "all", "occurrence": 1, "extent": "body", "lang": "en",
                 "reason": {"kind": "no-exemplar"}})
            for field in ("source_id", "witness_artifact_id", "witness_passage_id", "incipit", "quarantined_text_sha256"):
                self.assertNotIn(field, row)

    def test_english564_116_448_latin329_no_accounting_errors(self):
        coverage = self.mp.english_coverage(CALENDARS, "postconciliar")
        # 561->564/113->116: postconciliar-three-owner-adoption.json (accepted 2026-10-26).
        self.assertEqual({k: coverage[k] for k in ("slots", "with_english", "ledgered_untranslated", "rights_restricted")},
                         {"slots": 564, "with_english": 116, "ledgered_untranslated": 448, "rights_restricted": 0})
        for field in ("unaccounted", "outside_the_ledger", "unmatched_records", "stale_translation_records"):
            self.assertEqual(coverage[field], 0)
        self.assertEqual(len(list(L.body_owners(self.doc))), 329)
        self.assertEqual(sum(1 for _ in self.mp.masses_of(self.doc)), 619)
        # 3514->3517: the same adoption's three new Collect nodes.
        self.assertEqual(sum(1 for _, m in self.mp.masses_of(self.doc) for _ in self.mp.propers_of(m)), 3517)

    def test_no_incipit_or_bible_fallback_in_projection_and_english_renderer(self):
        for key in HELD:
            proper, = [p for p in self.public_masses[key]["propers"] if p["name"] == "Gospel Acclamation"]
            self.assertFalse(proper["citations"])
            self.assertFalse(proper.get("text"))
            self.assertFalse(proper["latin"].get("text"))
            self.assertEqual({r["lang"]: r["status"] for r in proper["languages"]},
                             {"en": "unavailable", "la": "unavailable"})
            self.assertTrue(all(not r["available"] and not r["held"] for r in proper["languages"]))
            args = argparse.Namespace(root=CALENDARS, calendar="postconciliar", mass=key, lang="en",
                bible=None, bible_root=ROOT / "src/sources/bibles")
            shown = self.mp.run_show_one(args)
            for i, appointed in enumerate(shown["appointed"]):
                if appointed["proper"]["name"] == "Gospel Acclamation":
                    self.assertEqual(self.mp.select_texts(appointed["proper"], "en", availability=args.absences[i]),
                        [("", "", "en translation unavailable: not yet sourced; Latin text unavailable")])

    def test_retained30_antiphon_owners_and_six_absent_roles_no_new_nodes(self):
        absent = {"easter-6-wednesday", "easter-6-thursday", "easter-7-saturday"}
        found = []
        for key in KEYS:
            owners = [p for p in self.masses[key]["propers"] if p["name"] in
                      ("Entrance Antiphon", "Communion Antiphon")]
            self.assertEqual(len(owners), 0 if key in absent else 2, key)
            found.extend(owners)
        self.assertEqual(len(found), 30)
        # Thirty-six scoped role positions are not thirty-six actual owners.
        self.assertEqual(2 * len(KEYS) - len(found), 6)

    def test_all378_whole_passages_and_three_n290_psalm_refusals(self):
        counts = {}
        for edition in BIBLES:
            config = self.index.EDITIONS[edition]
            bible = self.index.Bible(ROOT / "src/sources/works" / config["artifacts"])
            resolved, refused = 0, []
            for key in KEYS:
                for proper in self.masses[key]["propers"]:
                    if proper["name"] not in ("First Reading", "Responsorial Psalm", "Gospel"):
                        continue
                    entry, = proper["verses"]
                    _, ranges, problem = self.index.citation(entry,
                        proper.get("psalm_numbering", self.doc["psalm_numbering"]),
                        config["numbering"], self.mp, config["psalm_titles"])
                    if not problem:
                        ranges, problem = self.tables[config["numbering"]].apply(entry, ranges)
                    body = ""
                    if not problem:
                        body, problem = bible.passage(bible.token(entry["book"]), ranges)
                    if problem:
                        self.assertFalse(body, "a refusal must not return a partial body")
                        self.assertEqual((key, proper["name"], entry["ref"]),
                                         ("easter-5-saturday", "Responsorial Psalm", "Psalm 100:2, 3, 5"))
                        self.assertIn("divide Psalm 100 differently", problem)
                        refused.append(key)
                    else:
                        self.assertTrue(body)
                        resolved += 1
            expected = (54, 0) if config["numbering"] == "vulgate" else (53, 1)
            self.assertEqual((resolved, len(refused)), expected, edition)
            counts[edition] = expected
        self.assertEqual(sum(sum(row) for row in counts.values()), 378)

    def test_bounded_six_page_record_and_unknown_local_service_conditions(self):
        record = tomllib.loads(PASSAGE.read_text())
        self.assertEqual(record["schema"], 2)
        self.assertEqual(record["artifact_id"], ARTIFACT)
        self.assertEqual(record["artifact_sha256"], "ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d")
        self.assertEqual(record["artifact_page_ranges"], [[207, 212]])
        self.assertEqual(record["verified_on"], "2026-10-22")
        for number in range(285, 303):
            self.assertIn(f"N.{number} ", record["context"])
        self.assertIn("Greek Colossians", record["notes"])
        self.assertIn("no established independent exact lawful whole-unit", record["notes"])
        self.assertIn("not the Pentecost vigil", record["context"])
        self.assertIn("not a mandatory global Thursday replacement", record["context"])
        for key in KEYS:
            self.assertNotIn("proper_source_paths", self.masses[key])
        self.assertNotIn("proper_appointment_facts", self.doc)
        self.assertIn("Ascension", self.masses["easter-6-thursday"]["notes"])
        self.assertIn("morning", self.masses["easter-7-saturday"]["notes"])

    def test_negative_inventory_guards_reject_forged_owner_and_english_source(self):
        check = tool("check-calendar-masses")
        chunks = (INVENTORIES / "postconciliar-proper-translations-v1.toml").read_text().split("\n[[untranslated]]")
        target = next(i for i, chunk in enumerate(chunks[1:], 1)
            if (r := tomllib.loads("[[untranslated]]" + chunk)["untranslated"][0])["mass"] == "easter-5-monday"
            and r["proper"] == "Gospel Acclamation")
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch", prefix="easter-v-vii-negative-") as folder:
            temp = Path(folder)
            inv = temp / "inventories"
            inv.mkdir()
            source = temp / "postconciliar/propers.yaml"
            source.parent.mkdir()
            source.write_bytes((CALENDARS / "postconciliar/propers.yaml").read_bytes())
            for kind, old, new, message in (
                ("owner", "occurrence = 1", "occurrence = 99", "out of range"),
                ("source", 'kind = "no-exemplar"', 'kind = "no-exemplar"\nsource_id = "' + ARTIFACT + '"', "cannot name source_id"),
                ("rights", 'kind = "no-exemplar"', 'kind = "rights-withheld"\nsource_id = "' + ARTIFACT + '"', "requires a nonempty surfaces list"),
            ):
                with self.subTest(kind=kind):
                    changed = chunks.copy()
                    changed[target] = changed[target].replace(old, new)
                    (inv / "postconciliar-proper-translations-v1.toml").write_text("\n[[untranslated]]".join(changed))
                    with patch.object(check, "OVERLAY_DIR", inv):
                        errors, _ = check.overlay_problems([source])
                    self.assertIn(message, "\n".join(errors))
            changed = chunks.copy()
            changed.pop(target)
            (inv / "postconciliar-proper-translations-v1.toml").write_text("\n[[untranslated]]".join(changed))
            with patch.object(self.mp, "inventory_root", return_value=inv):
                self.assertEqual(self.mp.english_coverage(CALENDARS, "postconciliar")["unaccounted"], 1)
            changed_doc = copy.deepcopy(self.doc)
            proper = next(p for p in C.mass_index(changed_doc)["easter-5-monday"]["propers"] if p["name"] == "Gospel Acclamation")
            proper["source"] = "scripture"
            proper.pop("text_status")
            proper["verses"] = [self.canon.parse_citation("John 14:26")]
            source.write_text(yaml.safe_dump(changed_doc, sort_keys=False))
            (inv / "postconciliar-proper-translations-v1.toml").write_text("\n[[untranslated]]".join(chunks))
            with patch.object(check, "OVERLAY_DIR", inv):
                errors, _ = check.overlay_problems([source])
            self.assertIn("exact English rights-withheld body witness", "\n".join(errors))
            changed_doc = copy.deepcopy(self.doc)
            proper = next(p for p in C.mass_index(changed_doc)["easter-5-monday"]["propers"] if p["name"] == "Gospel Acclamation")
            proper["text_status"].pop("body_status")
            source.write_text(yaml.safe_dump(changed_doc, sort_keys=False))
            (inv / "postconciliar-proper-latin-provenance-v1.toml").write_bytes(
                (INVENTORIES / "postconciliar-proper-latin-provenance-v1.toml").read_bytes())
            problems = L.sidecar_problems([source], inventory_root=inv, required=True,
                                         registered_source_ids=check.source_ids()[0])
            self.assertIn("missing entry", "\n".join(problems))

    def test_browser_day_propers_seated_unseated_abc_from_fresh_projection(self):
        run = subprocess.run(["node", str(ROOT / "tools/tests/test_postconciliar_easter_v_vii_ferials.cjs")],
                             input=json.dumps(self.public), capture_output=True, text=True, timeout=120)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(report["staticForms"], 18)
        self.assertEqual(report["adapterExecutions"], 216)
        self.assertEqual(report["heldAcclamationChecks"], 180)


if __name__ == "__main__":
    if __import__("sys").argv[1:] == ["--projection"]:
        print(json.dumps(context()[-1]))
    else:
        unittest.main()
