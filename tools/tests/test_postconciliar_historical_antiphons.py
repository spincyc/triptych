"""Verify the historical antiphon transcriptions, study translations, and appointment boundaries."""

from collections import Counter
import hashlib
import re
from pathlib import Path
import tomllib
import unittest
import unicodedata

import yaml


SOURCES = Path(__file__).resolve().parents[2] / "src/sources"
COLLECTION = "2026-11-24-historical-antiphons"
EDITION = SOURCES / "works/triptych/postconciliar-latin-proper-editorial-projection/editions" / COLLECTION
INVENTORIES = SOURCES / "inventories"


def toml(path):
    with path.open("rb") as handle:
        return tomllib.load(handle)


class HistoricalAntiphonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        calendar = yaml.load(
            (SOURCES / "calendars/postconciliar/propers.yaml").read_bytes(), Loader=yaml.CSafeLoader
        )
        cls.masses = {mass["key"]: mass for section in calendar["sections"].values() for mass in section["masses"]}
        cls.manifest = toml(next(EDITION.glob("artifacts/*/artifact.toml")))
        cls.tsv = next(EDITION.glob("artifacts/*/antiphons.tsv")).read_bytes()
        cls.lines = [line.split("\t") for line in cls.tsv.decode().splitlines()]
        cls.passages = {row["id"]: row for path in (EDITION / "passages").glob("*.toml") if (row := toml(path))}
        cls.latin = [
            row for row in toml(INVENTORIES / "postconciliar-proper-latin-provenance-v1.toml")["entries"]
            if COLLECTION in row.get("source_id", "")
        ]
        cls.english = {
            (row["mass"], row["form_id"], row["proper"], row["occurrence"]): row
            for row in toml(INVENTORIES / "postconciliar-proper-translations-v1.toml")["entries"]
            if COLLECTION in row.get("source_latin_passage_id", "")
        }

    def test_each_appointment_resolves_to_its_qualified_lines(self):
        self.assertEqual(hashlib.sha256(self.tsv).hexdigest(), self.manifest["sha256"])
        self.assertEqual(Counter(row[1] for row in self.lines), {"la": 79, "en": 79})
        self.assertEqual(len(self.latin), 89)
        self.assertEqual(len(self.english), 89)
        self.assertEqual(sum(row["mass"].startswith("commune-") for row in self.latin), 10)
        public_sources = set(self.manifest["projected_from"])
        self.assertTrue(all("vulgata-clementina" in source or "1922-tours-mame" in source for source in public_sources))
        for record in self.latin:
            with self.subTest(mass=record["mass"], form=record["form"], proper=record["proper"], n=record["occurrence"]):
                mass = self.masses[record["mass"]]
                form = next(f for f in mass["forms"] if f["name"] == record["form"]) if record["form"] else mass
                # English counts every printed option. Latin counts only locally held body owners.
                translation_key, = [
                    key for key, entry in self.english.items()
                    if key[:3] == (record["mass"], form.get("id", "main"), record["proper"])
                    and entry["source_latin_passage_id"] == record["source_id"]
                ]
                proper = [p for p in form["propers"] if p["name"] == record["proper"]][translation_key[3] - 1]
                passage = self.passages[record["source_id"]]
                self.assertEqual(passage["artifact_sha256"], self.manifest["sha256"])
                start, end = passage["physical_line_ranges"][0]
                self.assertEqual(start, end)
                key, lang, body = self.lines[start - 1]
                self.assertEqual((lang, body), ("la", proper["text"]))
                self.assertEqual(record["text_sha256"], hashlib.sha256(body.encode()).hexdigest())
                self.assertEqual(record["relationship"], "editorial-projection-exact-to-target")
                self.assertEqual(record["publication_basis"], "public-domain")
                self.assertIn("vatican-typica-tertia-2002", record["verification_source_id"])
                self.assertIn("2008", record["notice"])
                projection, historical = record["publication_source_ids"]
                self.assertEqual(projection, self.manifest["id"])
                self.assertIn(historical, public_sources)
                english = self.english[translation_key]
                self.assertEqual(english["source_latin_passage_id"], record["source_id"])
                self.assertEqual(english["source_latin_sha256"], record["text_sha256"])
                translation, = english["translations"]
                self.assertEqual((translation["lang"], translation["rights"]), ("en", "project-created"))
                self.assertEqual(self.lines[start], [key, "en", translation["text"]])

    def test_biblical_extents_are_contiguous_in_the_registered_public_verses(self):
        def words(text):
            expanded = text.lower().replace("æ", "ae").replace("œ", "oe").replace("j", "i").replace("v", "u")
            folded = "".join(c for c in unicodedata.normalize("NFD", expanded) if not unicodedata.combining(c))
            return re.findall("[a-z]+", folded)

        bible = SOURCES / "works/catholic-church/vulgata-clementina/editions/ebible-latvuc"
        historical = {p.stem.removeprefix("historical-antiphon-"): toml(p)
                      for p in (bible / "passages").glob("historical-antiphon-*.toml")}
        manifests = {m["id"]: (m, path.parent) for path in (bible / "artifacts").glob("verse-text-*/artifact.toml")
                     if (m := toml(path))}
        self.assertEqual(len(historical), 69)
        for slug, lang, text in self.lines:
            if lang != "la" or slug not in historical:
                continue
            with self.subTest(antiphon=slug):
                source = historical[slug]
                first, last = source["physical_line_ranges"][0]
                manifest, directory = manifests[source["artifact_id"]]
                self.assertEqual(manifest["rights_status"], "public-domain")
                raw = next(directory.glob("*.tsv")).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), source["artifact_sha256"])
                rows = [line.split("\t") for line in raw.decode().splitlines()[first - 1:last]]
                book, chapter, verse = rows[0][:3]
                locus = f"{book}.{chapter}.{verse}"
                if first != last:
                    locus += "-" + rows[-1][2]
                self.assertEqual(source["locus"], locus)
                source_words = " " + " ".join(words(" ".join(row[3] for row in rows))) + " "
                self.assertIn(" " + " ".join(words(text)) + " ", source_words)

    def test_historical_extent_and_optional_course_are_distinct(self):
        lent = [p for p in self.masses["lent-4"]["propers"] if p["name"] == "Communion Antiphon"]
        self.assertEqual(lent[1]["ordinary_disposition"]["option"], "prodigal-son-gospel")
        self.assertTrue(lent[1]["text"].startswith("Oportet te, fili, gaudere"))
        self.assertNotIn("Oportet", lent[0].get("text", ""))
        ordinary = [p for p in self.masses["ot-4"]["propers"] if p["name"] == "Communion Antiphon"]
        self.assertEqual(ordinary[0]["verses"][0]["ref"], "Psalm 31:17-18")
        self.assertNotIn("Beati", ordinary[0].get("text", ""))
        self.assertEqual(ordinary[1]["text"].lower().count("beati"), 2)
        night = next(f for f in self.masses["nativity-lord"]["forms"] if f["id"] == "night")
        self.assertEqual(night["propers"][0]["takes_from"]["mass"], "nativity")

        forms = {f["id"]: f for f in self.masses["commune-martyrum"]["forms"]}
        choices = [p for p in forms["martyr-one-easter-1"]["propers"] if p["name"] == "Communion Antiphon"]
        self.assertTrue(choices[1]["text"].endswith("Alleluja."))
        mary = next(f for f in self.masses["commune-beatae-mariae-virginis"]["forms"] if f["id"] == "mary-ordinary-6")
        entrance = next(p for p in mary["propers"] if p["name"] == "Entrance Antiphon")
        self.assertTrue(entrance["text"].endswith("ima summis."))
