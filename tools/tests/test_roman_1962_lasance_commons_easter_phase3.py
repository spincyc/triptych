"""Seven checked Lasance prayers, reused only at 21 exact complete Latin owners."""
from __future__ import annotations

import copy
import csv
import hashlib
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import tomllib
import unicodedata
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src/sources/calendars"
LEDGER = ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml"
LATIN_LEDGER = ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"
PREFIX = "francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945"
EDITION = "edition." + PREFIX
EDITION_PATH = ROOT / (
    "src/sources/works/francis-xavier-lasance/the-new-roman-missal/"
    "editions/benziger-revised-1945"
)
PDF = "artifact." + PREFIX + ".internet-archive-facsimile-pdf-6cf3c3d0"
PDF_SHA = "6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70"
TARGET_SHA = "648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a"
ARTIFACT_SLUG = "commons-easter-orations-en-checked-c50bc1b6"
ARTIFACT = "artifact." + PREFIX + "." + ARTIFACT_SLUG
ARTIFACT_SHA = "c50bc1b6cbb2f258ab9868d20ca3f08701dc72fd4a4c8c2117dbff88c1837372"

# Seed identity, entire canonical Latin hash, exact checked English, historical
# PDF/printed page and separately inspected 1962 seed PDF page. No incipit join.
SOURCES = {
    "lasance-common-virgin-3-secret": (
        ("commune-virginum-3", "Secret"),
        "8bb5053f890faaf48c65987a87742c3e47ad2ab77cb7c3477f27c20308cfa63d",
        "May the offering of Thy consecrated people be accepted by Thee, O Lord, "
        "in honor of Thy saints, by whose merits it knoweth that it hath received "
        "aid in time of trouble. Through our Lord.",
        1392, "1373", 841,
    ),
    "lasance-common-virgin-3-postcommunion": (
        ("commune-virginum-3", "Postcommunion"),
        "2fce5ba4bdcb315093b386dd6b9cf76b5da1950b9d82876e7c95d0c0957bf0db",
        "Thou hast filled Thy household, O Lord, with sacred gifts; ever comfort "
        "us, we beseech Thee, through her intercession whose festival we "
        "celebrate. Through our Lord.",
        1392, "1373", 841,
    ),
    "lasance-common-confessor-bishop-1-secret": (
        ("commune-confessoris-pontificis-1", "Secret"),
        "5602efa256b603e14aabf412065bf0c5dc2aab9abf552d7036e81a1ad0563a3d",
        "May Thy saints, we beseech Thee, O Lord, everywhere make us joyful, "
        "that, while we venerate their merits, we may experience their "
        "patronage. Through our Lord.",
        1359, "1340", 828,
    ),
    "lasance-common-plural-martyrs-1-postcommunion": (
        ("commune-plurimorum-martyrum-1", "Postcommunion"),
        "4c1c2346c8b7418b612fb577305c02b2cfc636c81304a6266877f1468fc12f56",
        "Filled with the mysteries of salvation, we beseech Thee, O Lord, "
        "that we may be helped by the prayers of those whose festival we "
        "celebrate. Through our Lord.",
        1339, "1320", 819,
    ),
    "lasance-common-paschal-martyr-postcommunion": (
        ("commune-martyrum-tempore-paschali-1", "Postcommunion (Pro Martyre tantum)"),
        "f0a57d5f46075d85a70c9118853d24a262fb85570c39d24e59ad72143637166f",
        "Grant, we beseech Thee, O Lord, that we who on earth discharge with joy "
        "the duty of honouring Thy saints may be gladdened by their company "
        "forever in heaven. Through our Lord.",
        1352, "1333", 824,
    ),
    "lasance-easter-5-postcommunion": (
        ("easter-5", "Postcommunion"),
        "b49a24f871cea1d49713ee9849b708c682f833b7dea0d6d7a351487e00ab97a6",
        "Grant, O Lord, unto us, who have been regaled with the virtue of the "
        "heavenly table, both to desire what is right and to obtain what we "
        "desire. Through our Lord.",
        576, "578", 428,
    ),
    "lasance-holy-saturday-secret": (
        ("easter-sunday", "Secret"),
        "dce82177ab5f5f17769452580b48615019f12d028f9ac618787fb4f546f62980",
        "Receive, we beseech Thee, O Lord, the prayers of Thy people, with the "
        "offerings of sacrifices, that the sacred mysteries begun with these "
        "sacraments of Easter may avail us under grace a remedy unto life "
        "everlasting. Through our Lord.",
        533, "535", 411,
    ),
}
EXPECTED = {
    ("commune-virginum-3", "Secret"): "lasance-common-virgin-3-secret",
    ("s-monicae-viduae", "Secret"): "lasance-common-virgin-3-secret",
    ("comm-s-praxedis-virginis", "Secret"): "lasance-common-virgin-3-secret",
    ("s-marthae-virginis", "Secret"): "lasance-common-virgin-3-secret",
    ("s-birgittae-viduae", "Secret"): "lasance-common-virgin-3-secret",
    ("s-luciae-virginis-martyris", "Secret"): "lasance-common-virgin-3-secret",
    ("commune-virginum-3", "Postcommunion"): "lasance-common-virgin-3-postcommunion",
    ("s-monicae-viduae", "Postcommunion"): "lasance-common-virgin-3-postcommunion",
    ("comm-s-praxedis-virginis", "Postcommunion"): "lasance-common-virgin-3-postcommunion",
    ("s-luciae-virginis-martyris", "Postcommunion"): "lasance-common-virgin-3-postcommunion",
    ("commune-confessoris-pontificis-1", "Secret"): "lasance-common-confessor-bishop-1-secret",
    ("s-antonini-episcopi-confessoris", "Secret"): "lasance-common-confessor-bishop-1-secret",
    ("s-gregorii-thaumaturgi-episcopi-confessoris", "Secret"): "lasance-common-confessor-bishop-1-secret",
    ("commune-plurimorum-martyrum-1", "Postcommunion"): "lasance-common-plural-martyrs-1-postcommunion",
    ("ss-philippi-iacobi-apostolorum", "Postcommunion"): "lasance-common-plural-martyrs-1-postcommunion",
    ("commune-martyrum-tempore-paschali-1", "Postcommunion (Pro Martyre tantum)"): "lasance-common-paschal-martyr-postcommunion",
    ("s-hermenegildi-martyris", "Postcommunion"): "lasance-common-paschal-martyr-postcommunion",
    ("easter-5", "Postcommunion"): "lasance-easter-5-postcommunion",
    ("vigil-of-the-ascension", "Postcommunion"): "lasance-easter-5-postcommunion",
    ("easter-sunday", "Secret"): "lasance-holy-saturday-secret",
    ("easter-monday", "Secret"): "lasance-holy-saturday-secret",
}
WITHHELD = {
    ("comm-s-agapiti-martyris", "Postcommunion"),
    ("comm-s-mennae-martyris", "Postcommunion"),
    ("comm-ss-faustini-iovitae-martyrum", "Postcommunion"),
    ("commune-confessoris-non-pontificis-2", "Secret"),
    ("commune-unius-martyris-3", "Postcommunion"),
    ("easter-vigil", "Secret"),
    ("s-birgittae-viduae", "Postcommunion"),
    ("s-caietani-confessoris", "Secret"),
    ("s-francisci-xaverii-confessoris", "Secret"),
    ("s-marthae-virginis", "Postcommunion"),
    ("s-titi-episcopi-confessoris", "Secret"),
}


def identity(pair):
    return pair[0], "main", pair[1], "all", 1


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def typography_words(value):
    """Historical typography comparison only; NEVER controls cross-owner reuse."""
    value = value.casefold().replace("æ", "ae").replace("œ", "oe")
    value = "".join(c for c in unicodedata.normalize("NFKD", value)
                    if not unicodedata.combining(c))
    return re.findall("[a-z]+|[0-9]+", value)


class LasanceCommonsEasterPhase3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader(
            "lasance_commons_easter_phase3_propers", str(ROOT / "tools/mass-propers")
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.propers = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.propers
        loader.exec_module(cls.propers)
        cls.document = tomllib.loads(LEDGER.read_text())
        cls.overlay, _, cls.stale, cls.witnesses = cls.propers.translation_overlay(
            "roman-1962", CALENDARS
        )
        cls.entries = {k: r for k, r in cls.overlay.items()
                       if r.get("publication_artifact_id") == ARTIFACT}
        cls.records, cls.trouble = cls.propers._source_library_records(CALENDARS)
        cls.artifact = cls.records[ARTIFACT]
        cls.bodies, cls.direct = {}, set()
        calendar = cls.propers.load_calendar(CALENDARS, "roman-1962")
        for _, mass in cls.propers.masses_of(calendar):
            for form, proper, taken in cls.propers.appointed_propers(calendar, mass):
                owner = cls.propers.source_slot_identity(calendar, mass, form, proper, taken)
                for key, body in cls.propers.coverage_slot_units(proper, owner):
                    cls.bodies[key] = body
                    if taken is None and key[0] == mass["key"]:
                        cls.direct.add(key)
        cls.latin_rows = {
            (r["mass"], r["form"], r["proper"], r["cycle"], r["occurrence"]): r
            for r in tomllib.loads(LATIN_LEDGER.read_text())["entries"]
        }
        cls.payload = (ROOT / cls.artifact["path"]).read_bytes()
        cls.table = list(csv.DictReader(io.StringIO(cls.payload.decode()), delimiter="\t"))

    def assert_exact_reuse(self, target, seed, bodies=None):
        self.assertIn(target, {identity(pair) for pair in EXPECTED})
        source = SOURCES[EXPECTED[target[0], target[2]]]
        self.assertEqual(seed, identity(source[0]))
        bodies = self.bodies if bodies is None else bodies
        self.assertEqual(bodies[target]["text"], bodies[seed]["text"])
        self.assertEqual(sha(bodies[target]["text"]), source[1])

    def test_only_the_selected_21_terminal_owners_are_attached(self):
        targets = {identity(pair) for pair in EXPECTED}
        self.assertEqual(set(self.entries), targets)
        self.assertEqual(len(self.entries), 21)
        absences = {
            (r["mass"], r["form_id"], r["proper"], r["cycle"], r["occurrence"])
            for r in self.document["untranslated"]
        }
        self.assertFalse(targets & absences)
        for pair, source_key in EXPECTED.items():
            target, source = identity(pair), SOURCES[source_key]
            row = self.entries[target]
            with self.subTest(target=target):
                self.assertIn(target, self.direct)
                self.assertEqual(row.get("incipit"), self.bodies[target].get("incipit"))
                self.assertEqual(row["witness"], "lasance-1945")
                self.assertEqual(row["collation_result"], "confirmed")
                self.assertEqual(row["translations"], [{
                    "lang": "en", "rights": "public-domain",
                    "source_id": EDITION, "text": source[2],
                }])
                self.assertFalse({"actor", "speaker", "text_structure"} & row.keys())

    def test_entire_latin_and_conclusion_bytes_and_permitted_provenance(self):
        for pair, source_key in EXPECTED.items():
            target, source = identity(pair), SOURCES[source_key]
            with self.subTest(target=target):
                self.assert_exact_reuse(target, identity(source[0]))
                self.assertTrue(self.bodies[target]["text"].endswith("Per Dominum.\n"))
                self.assertIn(source[1], self.entries[target]["witness_note"])
                lp = self.latin_rows[pair[0], "", pair[1], "", 1]
                self.assertEqual(lp["text_sha256"], source[1])
                self.assertEqual(
                    (lp["provenance_status"], lp["publication_status"], lp["publication_basis"]),
                    ("collated", "permitted", "public-domain"),
                )
                self.assertIn(lp["source_id"], self.records)
                self.assertIn(lp["verification_source_id"], self.records)

    def test_historical_comparison_includes_every_word_and_actual_conclusion(self):
        for key, source in SOURCES.items():
            verify = self.records["passage." + PREFIX + ".verify-phase3-" + key]
            historical = verify["notes"].split(
                "Historical Latin transcription (layout reflowed): ", 1
            )[1].split(" Source Latin ending: ", 1)[0]
            with self.subTest(source=key):
                self.assertEqual(
                    typography_words(historical),
                    typography_words(self.bodies[identity(source[0])]["text"]),
                )
                self.assertEqual(typography_words(historical)[-2:], ["per", "dominum"])
                self.assertIn("Source Latin ending: Per Dominum.", verify["notes"])
                self.assertIn("Target Latin ending: Per Dominum.", verify["notes"])
                self.assertIn("English ending: Through our Lord.", verify["notes"])
                self.assertTrue(source[2].endswith("Through our Lord."))
                self.assertNotIn("Amen.", source[2])
                self.assertNotIn("N.", source[2])

    def test_exact_payload_recipient_columns_and_historical_rights_boundary(self):
        self.assertEqual((sha(self.payload), len(self.payload)), (ARTIFACT_SHA, 4868))
        self.assertEqual((self.artifact["sha256"], self.artifact["byte_size"]),
                         (ARTIFACT_SHA, 4868))
        self.assertEqual((self.artifact["edition_id"], self.artifact["derived_from"]),
                         (EDITION, PDF))
        self.assertEqual(
            (self.artifact["storage"], self.artifact["rights_status"],
             self.artifact["rights_jurisdiction"]),
            ("tracked", "public-domain", "United States"),
        )
        for phrase in ("A110108", "A192159", "1298a-1298n", "1302a-1302d",
                       "80b34759fb18ec60f6205460c2ac24dc9e4a861938a94ef1f8e04a08a398ac9a"):
            self.assertIn(phrase, self.artifact["rights_basis"])
        self.assertIn("Independent cold source review remains required", self.artifact["provenance"])
        self.assertEqual(
            (self.records[PDF]["sha256"], self.records[PDF]["storage"],
             self.records[PDF]["rights_status"]),
            (PDF_SHA, "remote", "unresolved"),
        )
        self.assertEqual(len(self.table), 21)
        self.assertEqual(list(self.table[0]),
                         ["mass", "form_id", "proper", "cycle", "occurrence", "english_json"])
        keys = [(r["mass"], r["form_id"], r["proper"], r["cycle"], int(r["occurrence"]))
                for r in self.table]
        self.assertEqual(keys, sorted(identity(pair) for pair in EXPECTED))
        for row, key in zip(self.table, keys):
            self.assertEqual(json.loads(row["english_json"]), self.entries[key]["translations"][0]["text"])
        self.assertEqual(len({sha(json.loads(r["english_json"])) for r in self.table}), 7)

    def test_seven_genuine_source_inspections_and_21_separate_publication_bindings(self):
        verifications = set()
        for line, table_row in enumerate(self.table, 2):
            target = (table_row["mass"], table_row["form_id"], table_row["proper"],
                      table_row["cycle"], int(table_row["occurrence"]))
            row = self.entries[target]
            source_key = EXPECTED[target[0], target[2]]
            source = SOURCES[source_key]
            verify, publish = self.records[row["passage_id"]], self.records[row["publication_passage_id"]]
            verifications.add(verify["id"])
            with self.subTest(target=target):
                self.assertEqual(verify["id"], "passage." + PREFIX + ".verify-phase3-" + source_key)
                self.assertEqual(
                    (verify["artifact_id"], verify["artifact_sha256"], verify["artifact_page_ranges"]),
                    (PDF, PDF_SHA, [[source[3], source[3]]]),
                )
                self.assertEqual(
                    (row["printed_page"], row["ia_leaf"], row["ia_leaf_range"]),
                    (source[4], source[3] - 1, [source[3] - 1, source[3] - 1]),
                )
                self.assertIn("Genuine Phase3 page-image inspection", verify["notes"])
                self.assertIn(TARGET_SHA, verify["notes"])
                self.assertIn(f"artifact PDF p. {source[5]}", verify["notes"])
                self.assertIn(sha(source[2]), verify["notes"])
                self.assertEqual(publish["locus"], verify["locus"])
                self.assertEqual(publish["physical_line_ranges"], [[line, line]])
                self.assertIn("No new image-inspection event", publish["notes"])
                self.assertEqual(verify["verified_on"], "2026-10-22")
                self.assertEqual(publish["verified_on"], "2026-10-22")
                self.propers.validate_translation_publication_binding(
                    row, CALENDARS, LEDGER, self.witnesses
                )
        self.assertEqual(len(verifications), 7)
        self.assertEqual(len(list((EDITION_PATH / "passages").glob("verify-phase3-*.toml"))), 7)
        self.assertEqual(len(list((EDITION_PATH / "passages").glob("publish-phase3-*.toml"))), 21)

    def test_normalized_petitions_cannot_hide_changed_conclusions_or_wrapping(self):
        target = identity(("s-monicae-viduae", "Secret"))
        seed = identity(SOURCES[EXPECTED[target[0], target[2]]][0])
        text = self.bodies[seed]["text"]
        for changed in (
            text.replace("Per Dominum.\n", "Per Dominum nostrum.\n"),
            text.replace("Per Dominum.", "Per Dominum ."),
            text.replace("\n", " ", 1),
        ):
            bodies = dict(self.bodies)
            bodies[seed] = dict(self.bodies[seed], text=changed)
            with self.subTest(changed=changed), self.assertRaises(AssertionError):
                self.assert_exact_reuse(target, seed, bodies)
        for wrong in (
            ("another-owner", *seed[1:]), (seed[0], "another-form", *seed[2:]),
            (*seed[:3], "A", seed[4]), (*seed[:4], 2),
        ):
            with self.subTest(wrong=wrong), self.assertRaises(AssertionError):
                self.assert_exact_reuse(target, wrong)

    def test_all_eleven_mismatches_and_advent_ii_collect_remain_unserved(self):
        self.assertEqual(len(WITHHELD), 11)
        for pair in WITHHELD | {("advent-2", "Collect")}:
            with self.subTest(pair=pair):
                self.assertNotIn(identity(pair), self.overlay)
        gap = [r for r in self.document["untranslated"]
               if (r["mass"], r["proper"]) == ("advent-2", "Collect")]
        self.assertEqual(len(gap), 1)
        self.assertEqual(gap[0]["reason"]["kind"], "witness-gap")
        holy = self.records["passage." + PREFIX + ".verify-phase3-lasance-holy-saturday-secret"]
        self.assertIn("Holy Saturday, older order", holy["locus"])
        self.assertIn("does not assert a whole-formulary match", holy["notes"])
        self.assertNotIn("easter-vigil", {r["mass"] for r in self.entries.values()})
        female = {k[0] for k, row in self.entries.items()
                  if "through her intercession" in row["translations"][0]["text"]}
        self.assertEqual(female, {"commune-virginum-3", "s-monicae-viduae",
                                 "comm-s-praxedis-virginis", "s-luciae-virginis-martyris"})

    def test_partial_stale_mistargeted_and_changed_english_fail_closed(self):
        original = self.entries[identity(("commune-virginum-3", "Secret"))]
        for field in ("publication_artifact_id", "publication_artifact_sha256",
                      "publication_passage_id"):
            changed = copy.deepcopy(original)
            del changed[field]
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.propers.validate_translation_publication_binding(
                    changed, CALENDARS, LEDGER, self.witnesses
                )
        for field, value in (
            ("publication_artifact_sha256", "0" * 64),
            ("mass", "another-owner"), ("form_id", "another-form"),
            ("cycle", "A"), ("occurrence", 2),
        ):
            changed = dict(original, **{field: value})
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.propers.validate_translation_publication_binding(
                    changed, CALENDARS, LEDGER, self.witnesses
                )
        changed = copy.deepcopy(original)
        changed["translations"][0]["text"] += " Amen."
        with self.assertRaisesRegex(ValueError, "body differs"):
            self.propers.validate_translation_publication_binding(
                changed, CALENDARS, LEDGER, self.witnesses
            )

    def test_page_proof_hash_range_state_and_wrong_row_fail_closed(self):
        original = self.entries[identity(("commune-virginum-3", "Secret"))]
        for passage, field, value in (
            (original["passage_id"], "artifact_sha256", "0" * 64),
            (original["passage_id"], "artifact_page_ranges", [[1391, 1392]]),
            (original["passage_id"], "states", ["inspected"]),
            (original["publication_passage_id"], "physical_line_ranges", [[2, 2]]),
        ):
            records = dict(self.records)
            records[passage] = dict(records[passage], **{field: value})
            with self.subTest(field=field), mock.patch.object(
                self.propers, "_source_library_records", return_value=(records, self.trouble)
            ), self.assertRaises(ValueError):
                self.propers.validate_translation_publication_binding(
                    original, CALENDARS, LEDGER, self.witnesses
                )

    def test_both_calendar_overlays_remain_accounted_and_roman_coverage_is_exact(self):
        self.assertFalse(self.stale)
        self.assertEqual(self.witnesses[EDITION]["witness_relation"], "antecedent")
        for calendar in ("roman-1962", "roman-pre-1955"):
            row = self.propers.english_coverage(CALENDARS, calendar)
            for field in ("unaccounted", "outside_the_ledger", "unmatched_records",
                          "stale_translation_records", "rights_restricted"):
                self.assertEqual(row[field], 0, (calendar, field))
            if calendar == "roman-1962":
                self.assertEqual((row["slots"], row["with_english"],
                                  row["ledgered_untranslated"]), (1427, 219, 1208))


if __name__ == "__main__":
    unittest.main()
