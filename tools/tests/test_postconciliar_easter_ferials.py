"""OLM nn267-284: source facts, explicit unavailable units and native choice.

No source wording or generated fixture. Numbering/concordance and appointment
identities are derived only by their existing production owners.
"""
from __future__ import annotations
import argparse
import copy
from functools import lru_cache
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import yaml

if __package__:
    from .test_postconciliar_lenten_ferial_courses import tool
else:
    from test_postconciliar_lenten_ferial_courses import tool

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars as C
import _proper_latin as L
import _psalms as P

CALENDARS = ROOT / "src/sources/calendars"
INVENTORIES = ROOT / "src/sources/inventories"
ARTIFACT = "artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e"
PASSAGE = ROOT / "src/sources/works/catholic-church/ordo-lectionum-missae/editions/latin-editio-typica-altera-1981/passages/easter-ferial-courses-267-284.toml"
FACT = "easter-4-sunday-john-10-1-10-actually-read"
DAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday")
KEYS = tuple(f"easter-{week}-{day}" for week in (2, 3, 4) for day in DAYS)
# Independently keyed from AP201-206 / printed147-152. These are appointment
# coordinates, not the source's titles, responses, incipits or rubrics.
CORE = (
 ("Acts 4:23-31", "Psalm 2:1-3, 4-6, 7-9", "John 3:1-8"),
 ("Acts 4:32-37", "Psalm 92:1ab, 1c-2, 5", "John 3:7b-15"),
 ("Acts 5:17-26", "Psalm 33:2-3, 4-5, 6-7, 8-9", "John 3:16-21"),
 ("Acts 5:27-33", "Psalm 33:2, 9, 17-18, 19-20", "John 3:31-36"),
 ("Acts 5:34-42", "Psalm 26:1, 4, 13-14", "John 6:1-15"),
 ("Acts 6:1-7", "Psalm 32:1-2, 4-5, 18-19", "John 6:16-21"),
 ("Acts 6:8-15", "Psalm 118:23-24, 26-27, 29-30", "John 6:22-29"),
 ("Acts 7:51-8:1a", "Psalm 30:3cd-4, 6ab, 7b, 8a, 17, 21ab", "John 6:30-35"),
 ("Acts 8:1b-8", "Psalm 65:1-3a, 4-5, 6-7a", "John 6:35-40"),
 ("Acts 8:26-40", "Psalm 65:8-9, 16-17, 20", "John 6:44-51"),
 ("Acts 9:1-20", "Psalm 116:1, 2", "John 6:52-59"),
 ("Acts 9:31-42", "Psalm 115:12-13, 14-15, 16-17", "John 6:60-69"),
 ("Acts 11:1-18", "Psalm 41:2-3; 42:3, 4", "John 10:1-10"),
 ("Acts 11:19-26", "Psalm 86:1-3, 4-5, 6-7", "John 10:22-30"),
 ("Acts 12:24-13:5a", "Psalm 66:2-3, 5, 6, 8", "John 12:44-50"),
 ("Acts 13:13-25", "Psalm 88:2-3, 21-22, 25, 27", "John 13:16-20"),
 ("Acts 13:26-33", "Psalm 2:6-7, 8-9, 10-11", "John 14:1-6"),
 ("Acts 13:44-52", "Psalm 97:1, 2-3ab, 3cd-4", "John 14:7-14"),
)
PRESERVED = {"easter-2-friday", "easter-3-monday"}
UNAVAILABLE = set(KEYS) - PRESERVED


@lru_cache(maxsize=1)
def context():
    mp, index, canon = (tool(name) for name in ("mass-propers", "index-bible", "citations"))
    doc = mp.load_calendar(CALENDARS, "postconciliar")
    entries = [entry for _, mass in mp.masses_of(doc)
               for entry, _ in mp.numbered_entries(mass, doc["psalm_numbering"])]
    tables = {target: mp.Divergences("postconciliar", doc, entries, canon, target,
               numberings=tuple(n for n in mp.SYSTEMS if n != mp.RESOLVED_IN)) for target in mp.SYSTEMS}
    public = mp.calendar_structure(CALENDARS, "postconciliar", mp.book_tokens())
    return doc, C.mass_index(doc), mp, index, canon, tables, public


class EasterFerialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc, cls.masses, cls.mp, cls.index, cls.canon, cls.tables, cls.public = context()

    def test_all54_exact_bounds_parts_and_vulgate_carriers(self):
        specials = {"Acts 7:51-8:1a": "Acts 7:51-59", "John 6:44-51": "John 6:44-52",
                    "John 6:52-59": "John 6:53-60", "John 6:60-69": "John 6:61-70"}
        count = 0
        for key, references in zip(KEYS, CORE):
            mass = self.masses[key]
            for role, ref in zip(("First Reading", "Responsorial Psalm", "Gospel"), references):
                rows = [p for p in mass["propers"] if p["name"] == role]
                self.assertEqual(len(rows), 2 if key == "easter-4-monday" and role == "Gospel" else 1)
                proper = rows[0]
                self.assertEqual(proper["source"], "scripture")
                self.assertNotIn("cycles", proper)
                self.assertNotIn("weekday_cycles", proper)
                parsed = self.canon.parse_citation(ref)
                expected = copy.deepcopy(parsed)
                if role == "Responsorial Psalm":
                    expected["ranges"] = [piece for span in parsed["ranges"]
                        for piece in P.convert_range_whole(parsed["book"], span["begin"], span["end"],
                                                          "vulgate", "hebrew")]
                actual = proper["verses"][0]
                self.assertEqual(actual["book"], expected["book"])
                self.assertEqual(actual["ranges"], expected["ranges"], (key, role))
                self.assertEqual(actual, self.canon.parse_citation(actual["ref"]))
                projected = self.mp.citation_structure(actual,
                    proper.get("psalm_numbering", self.doc["psalm_numbering"]), self.mp.book_tokens(), self.tables)
                target = self.canon.parse_citation(specials.get(ref, ref))
                self.assertEqual(projected["loci"]["vulgate"],
                    [locus for span in target["ranges"]
                     for locus in self.mp.range_to_loci(span["begin"], span["end"])])
                count += 1
        self.assertEqual(count, 54)

    def test_sixteen_units_are_held_not_published_and_exact_english_no_exemplar(self):
        rows = tomllib.loads((INVENTORIES / "postconciliar-proper-translations-v1.toml").read_text())["untranslated"]
        rows = [r for r in rows if r["mass"] in KEYS and r["proper"] == "Gospel Acclamation"]
        self.assertEqual({r["mass"] for r in rows}, UNAVAILABLE)
        self.assertEqual(len(rows), 16)
        for row in rows:
            proper = next(p for p in self.masses[row["mass"]]["propers"] if p["name"] == row["proper"])
            self.assertEqual(proper["source"], "composed")
            self.assertEqual(proper["text_status"], {"state": "unavailable", "scope": "proper-body",
                "body_status": "held-unpublished", "reasons": [{"kind": "rights-withheld", "source_id": ARTIFACT}]})
            self.assertEqual({k: row[k] for k in ("form_id", "cycle", "occurrence", "extent", "lang", "reason")},
                {"form_id": "main", "cycle": "all", "occurrence": 1, "extent": "body", "lang": "en",
                 "reason": {"kind": "no-exemplar"}})
            for key in ("text", "incipit", "verses", "translations", "takes_from"):
                self.assertNotIn(key, proper)
            for key in ("source_id", "witness_artifact_id", "witness_passage_id", "incipit", "quarantined_text_sha256"):
                self.assertNotIn(key, row)
        for key in PRESERVED:
            proper = next(p for p in self.masses[key]["propers"] if p["name"] == "Gospel Acclamation")
            self.assertEqual(proper["source"], "scripture")
            self.assertEqual(proper["verses"], [self.canon.parse_citation("Matthew 4:4b")])

    def test_n279_exact_optional_relation_not_a_date_or_selection_attestation(self):
        mass = self.masses["easter-4-monday"]
        relation = C.public_proper_source_paths(self.doc, mass)[0]
        self.assertEqual((relation["id"], relation["form_id"], relation["source_edition"]),
                         ("easter-4-monday-gospel", "main", "postconciliar"))
        for path, ident, cycles, occurrence, material in zip(relation["paths"],
            ("john-10-1-10", "john-10-11-18-a"), (["A", "B", "C"], ["A"]), (1, 2),
            ({"family": None, "cycle": "all"}, {"family": "cycles", "cycle": "A"})):
            self.assertEqual(path["id"], ident)
            self.assertEqual(path["calendar_cycles"], {"family": "sunday", "in": cycles})
            self.assertEqual(path["members"], [{"appointment": {"mass": mass["key"], "form_id": "main",
                "proper": "Gospel", "occurrence": occurrence}, "material_cycle": material}])
            if occurrence == 1:
                self.assertEqual(path["standing"], "principal")
                self.assertNotIn("when", path)
            else:
                self.assertEqual(path["standing"], "optional")
                self.assertEqual(path["when"], {"fact": FACT, "is": True})
        gospels = [p for p in mass["propers"] if p["name"] == "Gospel"]
        self.assertEqual(len(gospels), 2)
        self.assertEqual(gospels[1]["cycles"], {"A": {"verses": [self.canon.parse_citation("John 10:11-18")]}})
        self.assertNotIn("verses", gospels[1])
        self.assertNotIn("proper_appointment_facts", self.doc)

    def test_english564_116_448_latin329_no_accounting_errors(self):
        coverage = self.mp.english_coverage(CALENDARS, "postconciliar")
        # 561->564/113->116: postconciliar-three-owner-adoption.json (accepted 2026-10-26).
        self.assertEqual({k: coverage[k] for k in ("slots", "with_english", "ledgered_untranslated", "rights_restricted")},
                         {"slots": 564, "with_english": 116, "ledgered_untranslated": 448, "rights_restricted": 0})
        for field in ("unaccounted", "outside_the_ledger", "unmatched_records", "stale_translation_records"):
            self.assertEqual(coverage[field], 0)
        self.assertEqual(len(list(L.body_owners(self.doc))), 329)

    def test_no_bible_fallback_in_public_or_resolved_english(self):
        for key in UNAVAILABLE:
            public = next(m for m in self.public["masses"] if m["key"] == key)
            proper = next(p for p in public["propers"] if p["name"] == "Gospel Acclamation")
            self.assertFalse(proper["citations"])
            self.assertFalse(proper.get("text"))
            self.assertFalse(proper["latin"].get("text"))
            self.assertEqual({r["lang"]: r["status"] for r in proper["languages"]},
                             {"en": "unavailable", "la": "unavailable"})
            self.assertTrue(all(not r["available"] and not r["held"] for r in proper["languages"]))
            args = argparse.Namespace(root=CALENDARS, calendar="postconciliar", mass=key, lang="en",
                bible=None, bible_root=ROOT / "src/sources/bibles")
            shown = self.mp.run_show_one(args)
            for index, appointed in enumerate(shown["appointed"]):
                row = appointed["proper"]
                if row["name"] == "Gospel Acclamation":
                    self.assertEqual(self.mp.select_texts(row, "en", availability=args.absences[index]),
                        [("", "", "en translation unavailable: not yet sourced; Latin text unavailable")])

    def test_bounded_passage_has_six_page_locus_and_honest_limits(self):
        record = tomllib.loads(PASSAGE.read_text())
        self.assertEqual(record["artifact_id"], ARTIFACT)
        self.assertEqual(record["artifact_page_ranges"], [[201, 206]])
        self.assertEqual(record["verified_on"], "2026-10-22")
        for number in range(267, 285):
            self.assertIn(f"N.{number} ", record["context"])
        self.assertIn("unresolved", record["context"])
        self.assertIn("no established independent lawful whole-unit", record["notes"])

    def test_new_n272_gap_rejects_forged_english_and_latin_dispositions(self):
        check = tool("check-calendar-masses")
        english = (INVENTORIES / "postconciliar-proper-translations-v1.toml").read_text()
        chunks = english.split("\n[[untranslated]]")
        target = next(i for i, chunk in enumerate(chunks[1:], 1)
            if (r := tomllib.loads("[[untranslated]]" + chunk)["untranslated"][0])["mass"] == "easter-2-saturday"
            and r["proper"] == "Gospel Acclamation")
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch", prefix="easter-gap-controls-") as folder:
            temp = Path(folder)
            inv = temp / "inventories"
            inv.mkdir()
            path = temp / "postconciliar/propers.yaml"
            path.parent.mkdir()
            for mutation, message in (("occurrence", "out of range"),
                ("English-source", "cannot name source_id"), ("Bible-fallback", "exact English rights-withheld")):
                with self.subTest(mutation=mutation):
                    doc = copy.deepcopy(self.doc)
                    changed = chunks.copy()
                    if mutation == "occurrence":
                        changed[target] = changed[target].replace("occurrence = 1", "occurrence = 99")
                    elif mutation == "English-source":
                        changed[target] = changed[target].replace('kind = "no-exemplar"',
                            'kind = "no-exemplar"\nsource_id = "' + ARTIFACT + '"')
                    else:
                        proper = next(p for p in C.mass_index(doc)["easter-2-saturday"]["propers"]
                                      if p["name"] == "Gospel Acclamation")
                        proper["source"] = "scripture"
                        proper.pop("text_status")
                        proper["verses"] = [self.canon.parse_citation("John 6:16-21")]
                    path.write_text(yaml.safe_dump(doc, sort_keys=False))
                    (inv / "postconciliar-proper-translations-v1.toml").write_text("\n[[untranslated]]".join(changed))
                    with patch.object(check, "OVERLAY_DIR", inv):
                        errors, _ = check.overlay_problems([path])
                    self.assertIn(message, "\n".join(errors))
            missing = chunks.copy()
            missing.pop(target)
            (inv / "postconciliar-proper-translations-v1.toml").write_text("\n[[untranslated]]".join(missing))
            with patch.object(self.mp, "inventory_root", return_value=inv):
                self.assertEqual(self.mp.english_coverage(CALENDARS, "postconciliar")["unaccounted"], 1)
            doc = copy.deepcopy(self.doc)
            proper = next(p for p in C.mass_index(doc)["easter-2-saturday"]["propers"]
                          if p["name"] == "Gospel Acclamation")
            proper["text_status"].pop("body_status")
            path.write_text(yaml.safe_dump(doc, sort_keys=False))
            (inv / "postconciliar-proper-latin-provenance-v1.toml").write_bytes(
                (INVENTORIES / "postconciliar-proper-latin-provenance-v1.toml").read_bytes())
            errors = L.sidecar_problems([path], inventory_root=inv, required=True,
                                       registered_source_ids=check.source_ids()[0])
            self.assertIn("missing entry", "\n".join(errors))

    def test_browser_matrix_from_fresh_canonical_projection(self):
        run = subprocess.run(["node", str(ROOT / "tools/tests/test_postconciliar_easter_ferials.cjs")],
                             input=json.dumps(self.public), capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        report = json.loads(run.stdout)
        self.assertGreater(report["executions"], 200)
        self.assertGreater(report["refusals"], 100)


if __name__ == "__main__":
    if sys.argv[1:] == ["--projection"]:
        print(json.dumps(context()[-1]))
    else:
        unittest.main()
