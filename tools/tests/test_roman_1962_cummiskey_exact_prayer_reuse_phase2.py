"""Twenty-one literal whole-Latin reuses of checked Cummiskey English."""
from __future__ import annotations

import copy
import csv
import hashlib
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import sys
import tomllib
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src/sources/calendars"
LEDGER = ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml"
LATIN_LEDGER = ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"
PREFIX = "eugene-cummiskey.roman-missal-english-laity.philadelphia-1861"
EDITION = "edition." + PREFIX
EDITION_PATH = ROOT / (
    "src/sources/works/eugene-cummiskey/roman-missal-english-laity/"
    "editions/philadelphia-1861"
)
PDF = "artifact." + PREFIX + ".ia-scan-pdf"
PDF_SHA = "85034c90d5cbfe891f4359fb2faff907d217dbd11a30458b55e4c48eae028898"
ARTIFACT_SLUG = "roman-1962-exact-prayer-reuse-en-386eed26"
ARTIFACT = "artifact." + PREFIX + "." + ARTIFACT_SLUG
ARTIFACT_SHA = "386eed26fa0bd7ddec6e188cde9db5d53597fbf406442586db07e3fe869e7c7c"
ORIGINAL_ARTIFACT_SHAS = {
    "roman-1962-recovered-en": "c61752839c8b04282bac27592749d63a4f0227d3fa051e62418f609c562eb54a",
    "roman-1962-pentecost-en": "d0bd7b139ba8b2df99df66a09a6e91ec050bcf940ae47fc6f99966a4e460700b",
}
# These are full retained bodies, not incipits or normalized petitions.
LATIN_SHAS = {
    ("comm-s-bonifatii-martyris", "Secret"): "7136443afcf7107246f1dc917fdacadb4424768c52943b27722560da283fe077",
    ("comm-ss-symphorosae-septem-eius-filiorum", "Secret"): "e393cd6bbcfc7d56e0d2ca6ca4ecce278f1fc055c1a271c40ac0fecc5debabb5",
    ("praesentatione-beatae-mariae-virginis", "Secret"): "d3716a299d12e2a147f7bfbbb34f9fe6b79354fb20d65e1ccfcd4da998fa0ca5",
    ("praesentatione-beatae-mariae-virginis", "Postcommunion"): "49c8bdb0217cd8c342ccea0f988346316b06ee99e5ba979d73ad9feb705e2350",
    ("commune-confessoris-non-pontificis-1", "Secret"): "a615d91669e7135cbd9addeb815d9243da1e51a45e297c1ff461089347d8fcd8",
    ("commune-confessoris-non-pontificis-1", "Postcommunion"): "ebc9e676d622755e29bf9f334168521a47819a5182c5107f9f604e89730cef9f",
    ("comm-s-petri-apostoli-2", "Collect"): "274535bfa80a76eaf0bc15a1cd2092ec0cb6bb419100a4b4ced618d91b62edad",
    ("comm-s-petri-apostoli-2", "Secret"): "ded8f4b1cb3703e5aa22307216031d41f66359f3ba6474a3e46a497135b6cb1c",
    ("s-petri-nolasci-confessoris", "Secret"): "3d708b45db2a4c142d792148f0f4363dfdb4ae8246095a399c7a19cd76adf5d4",
    ("s-petri-nolasci-confessoris", "Postcommunion"): "f44835f0248173a9698a0e561d9d51944c2aefd3e9216d706709c4749d465e1c",
    ("pentecost", "Secret"): "784537ace944dabcb76aa34f5947d1ab6806629f27280a69cb888bda131ff9df",
}
EXPECTED = {
    ("commune-unius-martyris-3", "Secret"): ("comm-s-bonifatii-martyris", "Secret"),
    ("commune-plurimorum-martyrum-2", "Secret"): ("comm-ss-symphorosae-septem-eius-filiorum", "Secret"),
    ("commune-festorum-bmv", "Secret"): ("praesentatione-beatae-mariae-virginis", "Secret"),
    ("commune-festorum-bmv", "Postcommunion"): ("praesentatione-beatae-mariae-virginis", "Postcommunion"),
    ("sanctissimi-nominis-beatae-mariae-virginis", "Secret"): ("praesentatione-beatae-mariae-virginis", "Secret"),
    ("sanctissimi-nominis-beatae-mariae-virginis", "Postcommunion"): ("praesentatione-beatae-mariae-virginis", "Postcommunion"),
    ("s-pauli-primi-eremitae-confessoris", "Secret"): ("commune-confessoris-non-pontificis-1", "Secret"),
    ("s-pauli-primi-eremitae-confessoris", "Postcommunion"): ("commune-confessoris-non-pontificis-1", "Postcommunion"),
    ("ss-vincentii-anastasii-martyrum", "Secret"): ("comm-ss-symphorosae-septem-eius-filiorum", "Secret"),
    ("comm-s-petri-apostoli", "Collect"): ("comm-s-petri-apostoli-2", "Collect"),
    ("comm-s-petri-apostoli", "Secret"): ("comm-s-petri-apostoli-2", "Secret"),
    ("s-ioannis-a-deo-confessoris", "Postcommunion"): ("commune-confessoris-non-pontificis-1", "Postcommunion"),
    ("s-hermenegildi-martyris", "Secret"): ("comm-s-bonifatii-martyris", "Secret"),
    ("s-ioannis-baptistae-la-salle-confessoris", "Secret"): ("commune-confessoris-non-pontificis-1", "Secret"),
    ("s-bernardini-senensis-confessoris", "Secret"): ("s-petri-nolasci-confessoris", "Secret"),
    ("comm-s-alexii-confessoris", "Postcommunion"): ("commune-confessoris-non-pontificis-1", "Postcommunion"),
    ("comm-s-romani-martyris", "Secret"): ("comm-s-bonifatii-martyris", "Secret"),
    ("s-iosephi-cupertino-confessoris", "Secret"): ("s-petri-nolasci-confessoris", "Secret"),
    ("s-iosephi-cupertino-confessoris", "Postcommunion"): ("s-petri-nolasci-confessoris", "Postcommunion"),
    ("advent-ember-friday", "Secret"): ("comm-s-bonifatii-martyris", "Secret"),
    ("pentecost-thursday", "Secret"): ("pentecost", "Secret"),
}


def identity(pair):
    return pair[0], "main", pair[1], "all", 1


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def publication_body(entry):
    # The existing consumer removes exactly one structural terminal TOML LF.
    return entry["translations"][0]["text"].removesuffix("\n")


class CummiskeyExactPrayerReusePhase2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader(
            "cummiskey_exact_reuse_phase2_propers", str(ROOT / "tools/mass-propers")
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.propers = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.propers
        loader.exec_module(cls.propers)
        cls.document = tomllib.loads(LEDGER.read_text())
        cls.overlay, _, cls.stale, cls.witnesses = cls.propers.translation_overlay(
            "roman-1962", CALENDARS
        )
        cls.entries = {
            key: row for key, row in cls.overlay.items()
            if row.get("publication_artifact_id") == ARTIFACT
        }
        cls.records, cls.trouble = cls.propers._source_library_records(CALENDARS)
        cls.artifact = cls.records[ARTIFACT]
        cls.bodies = {}
        cls.direct_owners = set()
        calendar = cls.propers.load_calendar(CALENDARS, "roman-1962")
        for _, mass in cls.propers.masses_of(calendar):
            for form, proper, taken in cls.propers.appointed_propers(calendar, mass):
                owner = cls.propers.source_slot_identity(
                    calendar, mass, form, proper, taken
                )
                for key, body in cls.propers.coverage_slot_units(proper, owner):
                    cls.bodies[key] = body
                    if key[0] == mass["key"] and taken is None:
                        cls.direct_owners.add(key)
        cls.latin_proofs = tomllib.loads(LATIN_LEDGER.read_text())["entries"]

    def assert_exact_pair(self, target, donor, bodies=None):
        self.assertIn(target, {identity(pair) for pair in EXPECTED})
        expected_donor = identity(EXPECTED[target[0], target[2]])
        self.assertEqual(donor, expected_donor)
        bodies = self.bodies if bodies is None else bodies
        self.assertIn(target, bodies)
        self.assertIn(donor, bodies)
        target_text, donor_text = bodies[target]["text"], bodies[donor]["text"]
        self.assertEqual(target_text, donor_text)
        self.assertEqual(sha(target_text), LATIN_SHAS[donor[0], donor[2]])

    def test_only_the_exact_21_terminal_identities_replace_their_absences(self):
        targets = {identity(pair) for pair in EXPECTED}
        self.assertEqual(len(self.entries), 21)
        self.assertEqual(set(self.entries), targets)
        self.assertFalse(targets & {
            identity((r["mass"], r["proper"]))
            for r in self.document["untranslated"]
            if r["form_id"] == "main" and r["cycle"] == "all" and r["occurrence"] == 1
        })
        for target, row in self.entries.items():
            with self.subTest(target=target):
                self.assertIn(target, self.direct_owners)
                donor = self.overlay[identity(EXPECTED[target[0], target[2]])]
                self.assertEqual(row["translations"], donor["translations"])
                self.assertEqual(row["collated"], donor["collated"])
                self.assertEqual(row["collation_result"], "confirmed")
                self.assertEqual(row["witness"], "cummiskey-1861")
                # A missing target incipit is not filled from the donor.
                self.assertEqual(row.get("incipit"), self.bodies[target].get("incipit"))
                self.assertEqual(
                    [(t["lang"], t["rights"], t["source_id"]) for t in row["translations"]],
                    [("en", "public-domain", EDITION)],
                )
                self.assertIn("Complete registered Latin body AND conclusion", row["witness_note"])
                self.assertIn("/".join(map(str, identity(EXPECTED[target[0], target[2]]))),
                              row["witness_note"])
                self.assertFalse({"speaker", "actor", "text_structure"} & row.keys())

    def test_complete_latin_conclusions_and_existing_source_proofs_match(self):
        for pair, donor_pair in EXPECTED.items():
            target, donor = identity(pair), identity(donor_pair)
            with self.subTest(target=target):
                self.assert_exact_pair(target, donor)
                self.assertIn(LATIN_SHAS[donor_pair], self.entries[target]["witness_note"])
                for key in (target, donor):
                    proofs = [
                        r for r in self.latin_proofs
                        if (r["mass"], r.get("form", ""), r["proper"],
                            r.get("cycle", ""), r["occurrence"])
                        == (key[0], "", key[2], "", key[4])
                    ]
                    self.assertEqual(len(proofs), 1)
                    proof = proofs[0]
                    self.assertEqual(proof["text_sha256"], sha(self.bodies[key]["text"]))
                    self.assertEqual(
                        (proof["provenance_status"], proof["publication_status"],
                         proof["publication_basis"]),
                        ("collated", "permitted", "public-domain"),
                    )
                    self.assertIn(proof["source_id"], self.records)
                    self.assertIn(proof["verification_source_id"], self.records)

    def test_only_required_recipient_columns_duplicate_unchanged_english(self):
        artifact = self.artifact
        self.assertEqual((artifact["edition_id"], artifact["derived_from"]), (EDITION, PDF))
        self.assertEqual(
            (artifact["storage"], artifact["rights_status"], artifact["rights_jurisdiction"]),
            ("tracked", "public-domain", "United States"),
        )
        payload = (ROOT / artifact["path"]).read_bytes()
        self.assertEqual((sha(payload), len(payload)), (ARTIFACT_SHA, 4768))
        self.assertEqual((artifact["sha256"], artifact["byte_size"]), (ARTIFACT_SHA, 4768))
        reader = csv.DictReader(io.StringIO(payload.decode()), delimiter="\t")
        self.assertEqual(reader.fieldnames,
                         ["mass", "form_id", "proper", "cycle", "occurrence", "english_json"])
        rows = list(reader)
        self.assertEqual(len(rows), 21)
        self.assertEqual([(r["mass"], r["proper"]) for r in rows], list(EXPECTED))
        for row in rows:
            target = row["mass"], row["form_id"], row["proper"], row["cycle"], int(row["occurrence"])
            english = json.loads(row["english_json"])
            self.assertEqual(english, publication_body(self.entries[target]))
            self.assertEqual(
                english, publication_body(self.overlay[identity(EXPECTED[target[0], target[2]])])
            )
            self.assertTrue(english.endswith(("Thro'.", "Who livest.")))
        self.assertEqual(len({sha(json.loads(r["english_json"])) for r in rows}), 9)
        pdf = self.records[PDF]
        self.assertEqual((pdf["sha256"], pdf["storage"], pdf["rights_status"]),
                         (PDF_SHA, "remote", "unresolved"))
        for slug, expected_sha in ORIGINAL_ARTIFACT_SHAS.items():
            original = self.records["artifact." + PREFIX + "." + slug]
            self.assertEqual(original["sha256"], expected_sha)
            self.assertEqual(sha((ROOT / original["path"]).read_bytes()), expected_sha)

    def test_dual_bindings_reuse_eleven_original_page_verification_owners(self):
        verification_ids = set()
        for line, (pair, donor_pair) in enumerate(EXPECTED.items(), 2):
            target, donor = identity(pair), identity(donor_pair)
            row, donor_row = self.entries[target], self.overlay[donor]
            with self.subTest(target=target):
                self.assertEqual(row["passage_id"], donor_row["passage_id"])
                self.assertEqual(row["artifact_id"], PDF)
                verification_ids.add(row["passage_id"])
                verify = self.records[row["passage_id"]]
                publish = self.records[row["publication_passage_id"]]
                self.assertEqual(publish["locus"], verify["locus"])
                self.assertEqual(publish["physical_line_ranges"], [[line, line]])
                self.assertEqual(publish["verified_on"], "2026-10-22")
                self.assertIn("not a fresh page-image inspection", publish["notes"])
                self.assertIn(donor_row["publication_passage_id"], publish["notes"])
                self.assertEqual(row["ia_leaf_range"], donor_row["ia_leaf_range"])
                for candidate in (row, donor_row):
                    self.propers.validate_translation_publication_binding(
                        candidate, CALENDARS, LEDGER, self.witnesses
                    )
        self.assertEqual(len(verification_ids), 11)
        self.assertEqual(
            len(list((EDITION_PATH / "passages").glob("publish-phase2-exact-reuse-*.toml"))), 21
        )
        self.assertFalse(list((EDITION_PATH / "passages").glob("verify-phase2-exact-reuse-*.toml")))

    def test_changed_conclusion_and_wrong_owner_form_cycle_occurrence_are_refused(self):
        target = identity(("comm-s-petri-apostoli", "Collect"))
        donor = identity(EXPECTED[target[0], target[2]])
        changed = dict(self.bodies)
        changed[donor] = dict(self.bodies[donor])
        text = changed[donor]["text"]
        changed[donor]["text"] = text.replace("Qui vivis et regnas", "Qui tecum vivit et regnat")
        self.assertNotEqual(changed[donor]["text"], text)
        with self.assertRaises(AssertionError):
            self.assert_exact_pair(target, donor, changed)
        for wrong in (
            ("another-owner", *donor[1:]),
            (donor[0], "another-form", *donor[2:]),
            (*donor[:3], "A", donor[4]),
            (*donor[:4], 2),
        ):
            with self.subTest(wrong=wrong), self.assertRaises(AssertionError):
                self.assert_exact_pair(target, wrong)
        with self.assertRaises(AssertionError):
            self.assert_exact_pair((*target[:4], 2), donor)

    def test_equal_english_does_not_merge_different_latin_conclusions(self):
        common = identity(("commune-confessoris-non-pontificis-1", "Secret"))
        nolasco = identity(("s-petri-nolasci-confessoris", "Secret"))
        self.assertEqual(publication_body(self.overlay[common]), publication_body(self.overlay[nolasco]))
        self.assertNotEqual(self.bodies[common]["text"], self.bodies[nolasco]["text"])
        self.assertNotEqual(LATIN_SHAS[common[0], common[2]], LATIN_SHAS[nolasco[0], nolasco[2]])
        with self.assertRaises(AssertionError):
            self.assert_exact_pair(identity(("s-bernardini-senensis-confessoris", "Secret")), common)

    def test_partial_stale_or_mistargeted_publication_edges_fail_closed(self):
        original = self.entries[identity(("commune-festorum-bmv", "Secret"))]
        mutations = [
            ("publication_artifact_sha256", "0" * 64, "artifact hash is stale"),
            ("artifact_id", "artifact." + PREFIX + ".roman-1962-recovered-en",
             "not derived from the verification artifact"),
            ("passage_id",
             self.overlay[identity(("commune-confessoris-non-pontificis-1", "Secret"))]["passage_id"],
             "publication and verification passages name different targets"),
            ("publication_passage_id",
             self.overlay[identity(("praesentatione-beatae-mariae-virginis", "Secret"))]["publication_passage_id"],
             "publication passage does not bind its named artifact"),
            ("occurrence", 2, "cycle/occurrence does not match"),
            ("cycle", "A", "cycle/occurrence does not match"),
            ("form_id", "another-form", "form_id does not match"),
            ("mass", "another-owner", "mass does not match"),
            ("proper", "Collect", "proper does not match"),
        ]
        for field, value, diagnostic in mutations:
            changed = copy.deepcopy(original)
            changed[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, diagnostic):
                self.propers.validate_translation_publication_binding(
                    changed, CALENDARS, LEDGER, self.witnesses
                )
        for field in ("publication_artifact_id", "publication_artifact_sha256", "publication_passage_id"):
            changed = copy.deepcopy(original)
            del changed[field]
            with self.subTest(missing=field), self.assertRaisesRegex(ValueError, "partial translation publication"):
                self.propers.validate_translation_publication_binding(
                    changed, CALENDARS, LEDGER, self.witnesses
                )
        changed = copy.deepcopy(original)
        changed["translations"][0]["text"] += " Amen."
        with self.assertRaisesRegex(ValueError, "body differs"):
            self.propers.validate_translation_publication_binding(
                changed, CALENDARS, LEDGER, self.witnesses
            )

    def test_changed_page_proof_or_wrong_derivative_line_fails_closed(self):
        original = self.entries[identity(("commune-festorum-bmv", "Secret"))]
        for field, value, diagnostic in (
            ("artifact_sha256", "0" * 64, "verification passage artifact hash is stale"),
            ("artifact_page_ranges", [[517, 517]], "exact IA leaf range"),
            ("states", ["inspected"], "not inspected and dated verified"),
        ):
            records = dict(self.records)
            records[original["passage_id"]] = dict(records[original["passage_id"]], **{field: value})
            with self.subTest(proof_field=field), mock.patch.object(
                self.propers, "_source_library_records", return_value=(records, self.trouble)
            ):
                with self.assertRaisesRegex(ValueError, diagnostic):
                    self.propers.validate_translation_publication_binding(
                        original, CALENDARS, LEDGER, self.witnesses
                    )
        records = dict(self.records)
        records[original["publication_passage_id"]] = dict(
            records[original["publication_passage_id"]], physical_line_ranges=[[2, 2]]
        )
        with mock.patch.object(
            self.propers, "_source_library_records", return_value=(records, self.trouble)
        ), self.assertRaisesRegex(ValueError, "mass does not match"):
            self.propers.validate_translation_publication_binding(
                original, CALENDARS, LEDGER, self.witnesses
            )

    def test_advent_ii_collect_refuses_cummiskey_reuse_and_both_censuses_are_accounted(self):
        refused = identity(("advent-2", "Collect"))
        # 8d7e3b301 replaced the witness-gap (Lasance "Who livest." against "Qui
        # tecum.") with one separately reviewed, conclusion-compatible Lefebvre
        # 1925 English (english_sha256 in finite-source-methods-next18.json under
        # workflows/reviews/missal-reader-completion-2026-10-26; [[accepted]]
        # next17 in src/sources/inventories/roman-1962-english-recovery-2026-10-23.toml).
        self.assertNotIn(refused, self.entries)
        self.assertFalse([r for r in self.document["untranslated"]
                          if (r["mass"], r["form_id"], r["proper"], r["cycle"], r["occurrence"]) == refused])
        served = self.overlay[refused]
        self.assertEqual((served["witness"], served["collation_result"]), ("lefebvre-1925", "confirmed"))
        self.assertEqual([sha(t["text"]) for t in served["translations"]],
                         ["477de70209b91ea3ae16ca9caffbebc481aa704ec066456c436129c997c98cc5"])
        self.assertNotIn(PREFIX, served["passage_id"] + served["publication_artifact_id"])
        # The phase-2 censuses were (1427, 219, 1208) and (1378, 206, 1172); these
        # are the current_coverage of the accepted receipt
        # workflows/reviews/missal-reader-completion-2026-10-26/source-review-final-source180.json.
        for calendar, expected in (
            ("roman-1962", (1448, 1188, 260)),
            ("roman-pre-1955", (1391, 1168, 223)),
        ):
            census = self.propers.english_coverage(CALENDARS, calendar)
            self.assertEqual(
                (census["slots"], census["with_english"], census["ledgered_untranslated"]),
                expected,
            )
            for field in ("unaccounted", "outside_the_ledger", "unmatched_records",
                          "stale_translation_records", "rights_restricted"):
                self.assertEqual(census[field], 0, (calendar, field))
        self.assertEqual(self.stale, [])


if __name__ == "__main__":
    unittest.main()
