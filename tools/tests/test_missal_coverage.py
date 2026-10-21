"""Shared Missal accounting: identities, uses, witnesses, and evidence axes."""
from __future__ import annotations

import copy
import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import tomllib
from collections import Counter
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _missal_coverage as coverage


def tool(name):
    loader = importlib.machinery.SourceFileLoader("coverage_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def english(report):
    return next(row for row in report["languages"] if row["lang"] == "en")


class CoverageTests(unittest.TestCase):
    def test_duplicate_witness_and_alias_do_not_inflate_targets_or_available_uses(self):
        witness = {"source_id": "edition.one", "artifact_id": "artifact.one", "label": "Witness"}
        owner = {"source": "composed", "translations": [
            {"lang": "en", "source_id": identifier, "rights": "public-domain", "text": "Body"}
            for identifier in ("edition.one", "artifact.one", "edition.one")
        ]}
        one = coverage.unit(owner, target_id="target", occurrence_id="one",
                            witnesses={"edition.one": witness, "artifact.one": witness})
        two = copy.deepcopy(one)
        two["occurrence_id"] = "two"
        report = coverage.summarize([one, two, one], "calendar")
        self.assertEqual(report["counts"], {"canonical_targets": 1, "occurrences": 2, "witness_alternatives": 1})
        self.assertEqual(english(report)["available"], 2)
        self.assertEqual(english(report)["available_targets"], 1)
        self.assertEqual(english(report)["witnesses"][0]["aliases"], ["artifact.one", "edition.one"])
        self.assertEqual(english(one)["publication_basis"], "public-domain")
        self.assertEqual(english(report)["witnesses"][0]["publication_bases"], ["public-domain"])
        self.assertNotIn('"rights":', json.dumps([one, report]))
        coverage.validate_summary(report)

    def test_private_metadata_alias_is_not_added_to_public_witnesses(self):
        one = coverage.unit({"translations": [{
            "lang": "en", "source_id": "edition.public", "text": "Held",
            "rights": "public-domain",
        }]}, target_id="target", occurrence_id="use", witnesses={
            "edition.public": {"source_id": "edition.public",
                               "artifact_id": "artifact.private"},
        })
        self.assertEqual(english(one)["witnesses"][0]["aliases"], ["edition.public"])
        self.assertNotIn("artifact.private", json.dumps(coverage.summarize([one], "mass")))

    def test_fidelity_rights_and_availability_remain_independent(self):
        rows = []
        for index, (relation, collation, rights) in enumerate((
            ("antecedent", "collated", "public-domain"),
            ("antecedent", "uncollated", "public-domain"),
            (None, None, "project-created"),
            (None, None, "public-domain"),
        )):
            rows.append(coverage.unit({"translations": [{
                "lang": "en", "text": "Held", "source_id": str(index),
                "relation": relation, "collation": collation, "rights": rights,
            }]}, target_id=str(index), occurrence_id=str(index)))
        report = coverage.summarize(rows, "ordinary")
        row = english(report)
        self.assertEqual(row["available"], 4)
        self.assertEqual(row["exact_target"], 0)
        self.assertEqual(row["relationships"]["historical-antecedent"], 2)
        self.assertEqual(row["relationships"]["study-translation"], 1)
        self.assertEqual(row["relationships"]["unresolved"], 1)
        self.assertEqual(row["collations"]["collated"], 1)
        coverage.validate_summary(report)

    def test_conflicting_alias_bodies_fail_instead_of_claiming_availability(self):
        witness = {"source_id": "edition.one", "artifact_id": "artifact.one"}
        with self.assertRaisesRegex(ValueError, "conflicting bodies"):
            coverage.unit({"translations": [
                {"lang": "en", "source_id": "edition.one", "text": "One"},
                {"lang": "en", "source_id": "artifact.one", "text": "Different"},
            ]}, target_id="target", occurrence_id="one",
                witnesses={"edition.one": witness, "artifact.one": witness})

    def test_bible_reconstruction_does_not_fill_composed_wording(self):
        one = coverage.unit({"source": "scripture", "citations": [{"ref": "Psalm 1"}]},
                            target_id="scripture", occurrence_id="scripture")
        report = coverage.summarize([one], "mass")
        self.assertEqual(english(report)["targets"], 0)
        self.assertEqual(english(report)["scripture_targets"], 1)
        self.assertEqual(english(report)["available"], 0)
        self.assertEqual(one["languages"][0]["relationship"], "bible-reconstruction")
        coverage.validate_summary(report)

    def test_exact_witness_is_counted_once_beside_an_antecedent_alternative(self):
        one = coverage.unit({"translations": [
            {"lang": "en", "text": "Exact", "source_id": "a", "relation": "own", "rights": "public-domain"},
            {"lang": "en", "text": "Earlier", "source_id": "b", "relation": "antecedent", "rights": "public-domain"},
        ]}, target_id="target", occurrence_id="one")
        report = coverage.summarize([one], "mass")
        self.assertEqual(english(report)["exact_target"], 1)
        self.assertEqual(english(report)["exact_target_targets"], 1)
        self.assertEqual(english(report)["relationships"]["unresolved"], 1)
        self.assertEqual(report["counts"]["witness_alternatives"], 2)

    def test_mixed_body_keeps_its_independent_bible_component(self):
        one = coverage.unit({"source": "mixed", "text": "Latin",
                             "citations": [{"ref": "Psalm 1"}]},
                            target_id="target", occurrence_id="one")
        report = coverage.summarize([one], "mass")
        self.assertEqual(report["counts"]["canonical_targets"], 1)
        self.assertEqual(report["counts"]["occurrences"], 1)
        self.assertEqual(english(report)["occurrences"], 1)
        self.assertEqual(english(report)["scripture_occurrences"], 1)
        self.assertEqual(english(report)["mixed_occurrences"], 1)
        self.assertNotEqual(one["scripture_component"]["target_id"], one["target_id"])
        coverage.validate_summary(report)

    def test_absence_dispositions_do_not_export_source_evidence(self):
        one = coverage.unit({
            "untranslated": [{"lang": "en", "state": "rights-restricted",
                               "artifact_sha256": "SECRET", "witness_artifact_id": "PRIVATE"}],
            "latin": {"state": "unavailable", "withheld": True, "private": "SECRET"},
        }, target_id="target", occurrence_id="one")
        self.assertEqual(english(one)["availability"], "not-publishable")
        self.assertEqual(english(one)["publication_basis"], "restricted")
        self.assertEqual(one["languages"][0]["availability"], "unresolved")
        self.assertNotIn("SECRET", json.dumps(one))
        self.assertNotIn("PRIVATE", json.dumps(one))
        other = coverage.unit({}, target_id="other", occurrence_id="other",
                              ordinary_absences={"la": "inapplicable", "en": "absent-in-witness"})
        self.assertEqual(other["languages"][0]["availability"], "inapplicable")
        self.assertEqual(english(other)["availability"], "absent-in-witness")

    def latin(self, relationship="editorial-projection-exact-to-target", status="collated",
              basis="public-domain"):
        return {"text_sha256": "0" * 64, "withheld": False, "reason": None,
                "provenance": {"status": status, "relationship": relationship},
                "publication": {"status": "permitted", "basis": basis}}

    def test_word_exact_collated_projection_is_exact_target_latin(self):
        # G1: the 2026-09-03 rule makes a collated, word-exact projection the
        # target's wording; its record, not its availability, says so.
        one = coverage.unit({"source": "composed", "text": "Deus", "latin": self.latin()},
                            target_id="collect", occurrence_id="collect")
        latin = one["languages"][0]
        self.assertEqual((latin["availability"], latin["relationship"], latin["collation"],
                          latin["publication_basis"]),
                         ("available", "exact-target", "collated", "public-domain"))
        report = coverage.summarize([one], "mass")
        self.assertEqual(report["languages"][0]["exact_target"], 1)
        self.assertEqual(report["languages"][0]["exact_target_targets"], 1)
        self.assertEqual(report["languages"][0]["collations"]["collated"], 1)
        coverage.validate_summary(report)

    def test_uncollated_or_other_witness_latin_is_not_exact_target(self):
        cases = (
            # identified but never collated against the target
            (self.latin(status="identified"), "unresolved", "uncollated"),
            # exact to some witness, not declared exact to the target
            (self.latin(relationship="collated-exact"), "unresolved", "collated"),
            (self.latin(relationship="exact-transcription"), "unresolved", "collated"),
            (self.latin(relationship="collated-non-exact"), "unresolved", "collated"),
            # a body with no provenance record at all
            (None, "unresolved", "unresolved"),
        )
        for record, relation, collation in cases:
            with self.subTest(record=record):
                owner = {"source": "composed", "text": "Deus"}
                if record is not None:
                    owner["latin"] = record
                latin = coverage.unit(owner, target_id="t", occurrence_id="o")["languages"][0]
                self.assertEqual(latin["availability"], "available")
                self.assertEqual(latin["relationship"], relation)
                self.assertEqual(latin["collation"], collation)
                report = coverage.summarize([coverage.unit(owner, target_id="t", occurrence_id="o")], "mass")
                self.assertEqual(report["languages"][0]["exact_target"], 0)

    def test_inherited_latin_is_uncollated_and_never_exact_target(self):
        # Pre-1955 carries 1962's bodies by `text_from`; their collation was
        # against 1962, so the same record is not exact for the inheriting target.
        one = coverage.unit({"source": "composed", "text": "Deus", "latin": self.latin()},
                            target_id="t", occurrence_id="o", latin_inherited=True)
        latin = one["languages"][0]
        self.assertEqual((latin["relationship"], latin["collation"]), ("unresolved", "uncollated"))
        self.assertEqual(coverage.summarize([one], "mass")["languages"][0]["exact_target"], 0)

    def test_witness_declared_antecedent_types_its_bodies_and_entries_still_win(self):
        # G2: a source row's own relation covers every body it supplies.
        witnesses = {
            "edition.caswall": {"source_id": "edition.caswall", "witness_relation": "antecedent"},
            "edition.irons": {"source_id": "edition.irons"},
        }
        one = coverage.unit({"translations": [
            {"lang": "en", "text": "Holy Spirit!", "source_id": "edition.caswall", "rights": "public-domain"},
        ]}, target_id="t", occurrence_id="o", witnesses=witnesses)
        self.assertEqual(english(one)["relationship"], "historical-antecedent")
        self.assertEqual(english(one)["witnesses"][0]["relationship"], "historical-antecedent")
        both = coverage.unit({"translations": [
            {"lang": "en", "text": "Day of wrath", "source_id": "edition.caswall", "rights": "public-domain"},
            {"lang": "en", "text": "Day of ire", "source_id": "edition.irons", "rights": "public-domain"},
        ]}, target_id="t2", occurrence_id="o2", witnesses=witnesses)
        relations = {row["id"]: row["relationship"] for row in english(both)["witnesses"]}
        self.assertEqual(relations, {"edition.caswall": "historical-antecedent",
                                     "edition.irons": "unresolved"})
        self.assertEqual(english(both)["relationship"], "unresolved")
        own = coverage.unit({"translations": [
            {"lang": "en", "text": "Exact", "source_id": "edition.caswall", "relation": "own"},
        ]}, target_id="t3", occurrence_id="o3", witnesses=witnesses)
        self.assertEqual(english(own)["relationship"], "exact-target")

    def test_typed_source_absences_name_their_class_without_their_evidence(self):
        # G3: a slot whose only blocker is an unbound passage is not sourced,
        # not rights restricted; the public projection still says `unavailable`.
        public = {"untranslated": [{"lang": "en", "state": "unavailable"}]}
        for kinds, expected in (
            (["no-exemplar"], "not-sourced"),
            (["rights-withheld"], "not-publishable"),
            (["witness-gap"], "unresolved"),
            (["no-exemplar", "witness-gap"], "unresolved"),
            (["no-exemplar", "rights-withheld"], "not-publishable"),
            (None, "unresolved"),
        ):
            with self.subTest(kinds=kinds):
                one = coverage.unit(public, target_id="t", occurrence_id="o",
                                    absence_kinds={"en": kinds} if kinds else None)
                self.assertEqual(english(one)["availability"], expected)
                self.assertEqual(english(one)["publication_basis"],
                                 "restricted" if expected == "not-publishable" else "unresolved")
        # A publicly restricted translation stays restricted whatever the ledger says.
        restricted = coverage.unit({"unavailable_translations": [{"lang": "en", "state": "rights-restricted"}]},
                                   target_id="t", occurrence_id="o", absence_kinds={"en": ["no-exemplar"]})
        self.assertEqual(english(restricted)["availability"], "not-publishable")

    def test_report_refuses_conflicting_occurrences_and_bad_partition(self):
        one = coverage.unit({}, target_id="target", occurrence_id="one")
        other = copy.deepcopy(one)
        other["target_id"] = "another"
        with self.assertRaisesRegex(ValueError, "conflicting"):
            coverage.summarize([one, other], "mass")
        report = coverage.summarize([one], "mass")
        english(report)["available"] = 1
        with self.assertRaisesRegex(ValueError, "inconsistent"):
            coverage.validate_summary(report)

    def test_summary_validation_checks_witness_counts(self):
        one = coverage.unit({"translations": [{"lang": "en", "text": "Held",
                                               "source_id": "a", "rights": "public-domain"}]},
                            target_id="target", occurrence_id="one")
        report = coverage.summarize([one], "mass")
        report["counts"]["witness_alternatives"] = 999
        with self.assertRaisesRegex(ValueError, "witness alternatives"):
            coverage.validate_summary(report)
        report = coverage.summarize([one], "mass")
        english(report)["witnesses"][0]["available"] = 999
        with self.assertRaisesRegex(ValueError, "exceeds"):
            coverage.validate_summary(report)


class GeneratorCoverageTests(unittest.TestCase):
    def test_translation_only_sunday_and_weekday_owners_survive_generation(self):
        propers = tool("mass-propers")
        for family, cycle in (("cycles", "A"), ("weekday_cycles", "I")):
            for rights in ("public-domain", "licensed"):
                source = {"name": "Acclamation", "source": "composed", family: {
                    cycle: {"source": "composed", "translations": [{
                        "lang": "en", "text": "Public fixture", "source_id": "edition.a",
                        "rights": rights,
                    }]}
                }}
                document = {"psalm_numbering": "vulgate", "sections": {
                    "temporal": {"kind": "seasonal", "masses": [{"key": "owner", "propers": [source]}]}
                }}
                with self.subTest(family=family, rights=rights), \
                     mock.patch.object(propers, "load_calendar", return_value=document), \
                     mock.patch.object(propers, "translation_overlay", return_value=({}, {}, [], {})), \
                     mock.patch.object(propers, "publication_records", return_value=({}, [])), \
                     mock.patch.object(propers, "sanitize_proper", side_effect=lambda value, *args: value), \
                     mock.patch.object(propers._missal_coverage, "expectations", return_value={"state": "unresolved"}):
                    report = propers.calendar_structure(ROOT / "src/sources/calendars", "postconciliar", {})
                child = report["masses"][0]["propers"][0][family][cycle]
                self.assertEqual(english(child["coverage"])["availability"],
                                 "available" if rights == "public-domain" else "not-publishable")
                self.assertEqual(report["coverage"]["counts"]["occurrences"], 1)
                self.assertEqual(english(report["coverage"])["available"],
                                 1 if rights == "public-domain" else 0)

    def test_generator_visits_nested_cycles_and_reuses_canonical_owner(self):
        propers = tool("mass-propers")
        source = {"name": "Acclamation", "cycles": {
            "A": {"source": "composed", "text": "Latin"},
            "B": {"source": "scripture", "verses": []},
        }}
        owner = {"key": "owner", "name": "Owner", "propers": [source]}
        borrowed = {"key": "borrowed", "name": "Borrowed", "takes_from": {"mass": "owner"}}
        document = {"calendar": "postconciliar", "psalm_numbering": "vulgate",
                    "sections": {"temporal": {"kind": "seasonal", "masses": [owner, borrowed]}}}
        # A citation is enough to make the scripture cycle a generated owner.
        source["cycles"]["B"]["verses"] = [{"book": "Psalms", "ranges": [], "ref": "Psalm 1"}]
        with mock.patch.object(propers, "load_calendar", return_value=document), \
             mock.patch.object(propers, "translation_overlay", return_value=({}, {}, [], {})), \
             mock.patch.object(propers, "publication_records", return_value=({}, [])), \
             mock.patch.object(propers, "sanitize_proper", side_effect=lambda value, *args: value), \
             mock.patch.object(propers, "citation_structure", return_value={"ref": "Psalm 1"}), \
             mock.patch.object(propers._missal_coverage, "expectations", return_value={"state": "unresolved"}):
            report = propers.calendar_structure(ROOT / "src/sources/calendars", "postconciliar", {})
        self.assertEqual(report["coverage"]["counts"]["canonical_targets"], 2)
        self.assertEqual(report["coverage"]["counts"]["occurrences"], 4)
        self.assertEqual(english(report["coverage"])["occurrences"], 2)
        self.assertEqual(english(report["coverage"])["scripture_occurrences"], 2)
        self.assertIsNone(report["masses"][0]["propers"][0]["coverage"])
        left, right = [coverage.proper_units(mass) for mass in report["masses"]]
        self.assertEqual(left[0]["target_id"], right[0]["target_id"])
        self.assertNotEqual(left[0]["occurrence_id"], right[0]["occurrence_id"])
        coverage.validate_summary(report["coverage"])

    def test_generator_passes_latin_record_and_keeps_inherited_latin_below_target(self):
        propers = tool("mass-propers")
        latin = {"text_sha256": "0" * 64, "withheld": False, "reason": None,
                 "provenance": {"status": "collated",
                                "relationship": "editorial-projection-exact-to-target"},
                 "publication": {"status": "permitted", "basis": "public-domain"}}

        def mass(key, stamp):
            row = {"key": key, "name": key, "propers": [
                {"name": "Collect", "source": "composed", "text": "Deus", "latin": dict(latin)}
            ]}
            if stamp is not None:
                row["recension"] = stamp
            return row

        masses = [
            mass("own", None),
            mass("stated", {"calendar": "roman-1962", "kind": "replaced", "stated": True,
                            "text_from": "", "basis": "", "also": []}),
            mass("inherited", {"calendar": "roman-1962", "kind": "", "stated": False,
                               "text_from": "roman-1962", "basis": "", "also": []}),
        ]
        document = {"psalm_numbering": "vulgate",
                    "sections": {"temporal": {"kind": "seasonal", "masses": masses}}}
        with mock.patch.object(propers, "load_calendar", return_value=document), \
             mock.patch.object(propers, "translation_overlay", return_value=({}, {}, [], {})), \
             mock.patch.object(propers, "publication_records", return_value=({}, [])), \
             mock.patch.object(propers, "sanitize_proper", side_effect=lambda value, *args: value), \
             mock.patch.object(propers._missal_coverage, "expectations", return_value={"state": "unresolved"}):
            report = propers.calendar_structure(ROOT / "src/sources/calendars", "roman-pre-1955", {})
        latin_rows = {row["key"]: row["propers"][0]["coverage"]["languages"][0]
                      for row in report["masses"]}
        self.assertEqual((latin_rows["own"]["relationship"], latin_rows["own"]["collation"]),
                         ("exact-target", "collated"))
        self.assertEqual(latin_rows["stated"]["relationship"], "exact-target")
        self.assertEqual((latin_rows["inherited"]["relationship"], latin_rows["inherited"]["collation"]),
                         ("unresolved", "uncollated"))
        self.assertEqual(latin_rows["inherited"]["publication_basis"], "public-domain")
        self.assertEqual(report["coverage"]["languages"][0]["exact_target"], 2)
        coverage.validate_summary(report["coverage"])

    def test_source_row_relation_requires_evidence_and_an_established_attestation(self):
        propers = tool("mass-propers")
        good = {"id": "w", "source_id": "edition.w", "label": "W", "rights": "public-domain",
                "attests": "si-quid-est-1634", "witness_relation": "antecedent",
                "witness_relation_basis": "dated before the target"}
        for row, message in (
            (dict(good, witness_relation="own"), "must be 'antecedent'"),
            ({key: value for key, value in good.items() if key != "witness_relation_basis"},
             "requires witness_relation_basis"),
            (dict(good, attests="unestablished"), "established attestation"),
        ):
            with self.subTest(message=message), tempfile.TemporaryDirectory() as tmp:
                inventories = Path(tmp) / "inventories"
                inventories.mkdir()
                lines = ["[[sources]]"] + [f"{key} = {json.dumps(value)}" for key, value in row.items()]
                (inventories / "fixture-proper-translations-v1.toml").write_text("\n".join(lines) + "\n")
                with mock.patch.object(propers, "inventory_root", return_value=inventories), \
                     mock.patch.object(propers, "translation_ledger_calendars", return_value=["fixture"]), \
                     mock.patch.object(propers._calendars, "load_document", return_value={}), \
                     self.assertRaisesRegex(ValueError, message):
                    propers.translation_overlay("fixture", Path(tmp))
        with tempfile.TemporaryDirectory() as tmp:
            inventories = Path(tmp) / "inventories"
            inventories.mkdir()
            lines = ["[[sources]]"] + [f"{key} = {json.dumps(value)}" for key, value in good.items()]
            (inventories / "fixture-proper-translations-v1.toml").write_text("\n".join(lines) + "\n")
            with mock.patch.object(propers, "inventory_root", return_value=inventories), \
                 mock.patch.object(propers, "translation_ledger_calendars", return_value=["fixture"]), \
                 mock.patch.object(propers._calendars, "load_document", return_value={}):
                witnesses = propers.translation_overlay("fixture", Path(tmp))[3]
            self.assertEqual(witnesses["edition.w"]["witness_relation"], "antecedent")


class RealCorpusCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.propers = tool("mass-propers")
        cls.files = {
            calendar: cls.propers.calendar_structure(
                ROOT / "src/sources/calendars", calendar, cls.propers.book_tokens()
            ) for calendar in ("roman-1962", "postconciliar", "roman-pre-1955")
        }

    def test_immaculate_feast_qualifies_secret_and_accounts_shared_english_absences(self):
        name = 'conceptione-immaculata-beatae-mariae-virginis'
        expected = {'Collect': '3dd9b9b0db918ec4f65b9a175e77347c0a54b5875fb874f50ed0bbe636b311f2', 'Secret': '6755a936e24660ef77e7c0ceffba13c28d21a82cc941bf8fb9ba5b57863f31a9', 'Communion': 'e26ba7251680129e9e04187733f30e4601c1479cdc157f20b6d160dbe4007936', 'Postcommunion': 'aa2efdb79676b0a403afaeb0f5bfacd9e9888af5af507f6d0cd09296cf5bf5d0'}
        mass = next(row for row in self.files["roman-1962"]["masses"] if row["key"] == name)
        found = {p["name"]: p for p in mass["propers"] if p["name"] in expected}
        self.assertEqual(set(expected), set(found))
        for role, digest in expected.items():
            proper = found[role]
            self.assertEqual(digest, hashlib.sha256(proper["text"].encode()).hexdigest())
            languages = {r["lang"]: r for r in proper["coverage"]["languages"]}
            self.assertEqual(("available", "collated", "public-domain"),
                             (languages["la"]["availability"], languages["la"]["collation"],
                              languages["la"]["publication_basis"]))
            self.assertEqual("unresolved" if role == "Secret" else "exact-target",
                             languages["la"]["relationship"])
            self.assertEqual("not-sourced", languages["en"]["availability"])
            self.assertFalse(proper["translations"])
        self.assertNotIn("Tract", [p["name"] for p in mass["propers"]])
        self.assertEqual("composed", found["Communion"]["source"])
        self.assertFalse(found["Communion"]["citations"])
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
        for role in expected:
            rows = [r for r in ledger["untranslated"] if
                    (r["mass"], r["form_id"], r["proper"], r["cycle"], r["occurrence"],
                     r["lang"], r["extent"]) == (name, "main", role, "all", 1, "en", "body")]
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["reason"], {"kind": "no-exemplar"})
            self.assertFalse([r for r in ledger["entries"] if r["mass"] == name and r["proper"] == role])
        child = tomllib.loads((ROOT / "src/sources/inventories/roman-pre-1955-proper-translations-v1.toml").read_text())
        self.assertFalse([r for r in child.get("untranslated", []) if r["mass"] == name and r["proper"] in expected])
        for calendar in ("roman-1962", "roman-pre-1955"):
            report = self.propers.english_coverage(ROOT / "src/sources/calendars", calendar)
            self.assertEqual((0, 0, 0), (report["unaccounted"], report["unmatched_records"],
                                       report["stale_translation_records"]))

    def test_published_english_targets_agree_with_source_identity_census(self):
        for calendar, document in self.files.items():
            source = self.propers.english_coverage(ROOT / "src/sources/calendars", calendar)
            self.assertEqual(english(document["coverage"])["targets"], source["slots"], calendar)
            self.assertEqual(english(document["coverage"])["available_targets"], source["with_english"], calendar)
            coverage.validate_summary(document["coverage"])

    def test_pre1955_inheritance_is_not_promoted_to_target_wording(self):
        document = self.files["roman-pre-1955"]
        self.assertGreater(english(document["coverage"])["available"], 0)
        self.assertTrue(any(mass.get("recension") for mass in document["masses"]))
        self.assertTrue(all(row["exact_target"] == 0 for row in document["coverage"]["languages"]))

    def test_pentecost_exemplar_accounts_truthfully(self):
        """The C2 exemplar, 1962 Pentecost (2026-05-24), after G1-G3 and C3."""
        def mass(calendar):
            return next(row for row in self.files[calendar]["masses"] if row["key"] == "pentecost")

        def bodies(calendar):
            return {row["name"]: row["coverage"]["languages"] for row in mass(calendar)["propers"]
                    if (row.get("form_id") or "main") in {"main", "day"}
                    and row.get("coverage") and row["coverage"]["component"] != "scripture"}

        roman = bodies("roman-1962")
        missal_text = {"Introit", "Lesson", "Gospel", "Offertory", "Communion"}
        self.assertEqual(set(roman), {"Collect", "Alleluia", "Sequence", "Secret", "Postcommunion"}
                         | missal_text)
        for name, (latin, _) in roman.items():
            with self.subTest(name=name):
                self.assertEqual((latin["availability"], latin["relationship"], latin["collation"],
                                  latin["publication_basis"]),
                                 ("available", "exact-target", "collated", "public-domain"))
        # C3: the chants and readings carry the Missal's own wording, not a
        # Bible reconstruction. Their scriptural constituents stay typed apart,
        # on the unit's scripture component, and no unit is itself a
        # reconstruction any more.
        for proper in mass("roman-1962")["propers"]:
            with self.subTest(unit=proper["name"]):
                unit = proper["coverage"]
                self.assertNotEqual(unit["component"], "scripture")
                self.assertTrue(all(row["relationship"] != "bible-reconstruction"
                                    for row in unit["languages"]))
                if proper["name"] in missal_text:
                    self.assertEqual(proper["source"], "mixed")
                    self.assertTrue(proper["text"].strip())
                    self.assertTrue(proper["citations"])
                    self.assertEqual(unit["scripture_component"]["relationship"],
                                     "bible-reconstruction")
        english_witness = {"Collect": "edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861",
                           "Secret": "edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861",
                           "Postcommunion": "edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861",
                           "Introit": "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945",
                           "Gospel": "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945",
                           "Offertory": "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945",
                           "Communion": "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945",
                           # Bound 2026-10-19 (G14 lane), its genuflection a typed rubric.
                           "Alleluia": "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945",
                           "Sequence": "edition.edward-caswall.lyra-catholica.london-1849"}
        for name, (_, english_row) in roman.items():
            with self.subTest(name=name, lang="en"):
                if name in english_witness:
                    self.assertEqual((english_row["availability"], english_row["relationship"]),
                                     ("available", "historical-antecedent"))
                    self.assertEqual([row["id"] for row in english_row["witnesses"]],
                                     [english_witness[name]])
                    self.assertEqual([row["relationship"] for row in english_row["witnesses"]],
                                     ["historical-antecedent"])
                else:
                    # Both public-domain witnesses lack the Missal's discipuli:
                    # a typed witness gap, not a missing binding.
                    self.assertEqual(name, "Lesson")
                    self.assertEqual(english_row["availability"], "unresolved")
                    self.assertEqual(english_row["witnesses"], [])
        latin_summary, english_summary = mass("roman-1962")["coverage"]["languages"]
        self.assertEqual((latin_summary["targets"], latin_summary["exact_target"]), (10, 10))
        self.assertEqual((english_summary["available"],
                          english_summary["relationships"]["historical-antecedent"]), (9, 9))
        # Pre-1955 inherits 1962's bodies uncollated: never exact-target there.
        for name, (latin, english_row) in bodies("roman-pre-1955").items():
            with self.subTest(calendar="roman-pre-1955", name=name):
                self.assertNotEqual(latin["relationship"], "exact-target")
                if name == "Sequence":
                    self.assertEqual(english_row["relationship"], "historical-antecedent")
        sequence = bodies("postconciliar")["Sequence"][1]
        self.assertEqual(sequence["relationship"], "historical-antecedent")

    def test_christ_the_king_checked_orations_preserve_other_wording_and_conditional_gaps(self):
        document = self.files["roman-1962"]
        mass = next(row for row in document["masses"] if row["key"] == "christ-the-king")
        propers = {row["name"]: row for row in mass["propers"]}
        prefix = "roman-1962:sanctoral-form:p778-l1"
        report = coverage.expectations(
            ROOT / "src/sources/inventories/missal-expected-targets-v1.toml",
            "roman-1962", [mass])
        states = {row["id"]: row["state"] for row in report["targets"]
                  if row["id"].startswith(prefix)}
        self.assertEqual(states[prefix], "represented")
        # F01 established these three appointments. The bounded MVP recovery
        # supplies only their independently witnessed Latin prayer words.
        for suffix, name in (("slot:p778-l15:collect", "Collect"),
                             ("slot:p779-l60:secret", "Secret"),
                             ("slot:p779-l74:postcommunion", "Postcommunion")):
            with self.subTest(proper=name):
                self.assertEqual(states[f"{prefix}:{suffix}"], "represented")
                proper = propers[name]
                self.assertEqual(proper["source"], "composed")
                self.assertIsNone(proper["text_status"])
                self.assertTrue(proper["text"])
                self.assertFalse(proper["translations"])
                languages = {row["lang"]: row for row in proper["coverage"]["languages"]}
                self.assertEqual((languages["la"]["availability"],
                                  languages["la"]["relationship"]),
                                 ("available", "exact-target"))
                self.assertEqual(languages["en"]["availability"], "unresolved")
                self.assertEqual(languages["en"]["witnesses"], [])
                self.assertEqual(hashlib.sha256(proper["text"].encode()).hexdigest(), {
                    "Collect": "6af5e3a4069557becc63497526bb1e3b76fa5bb0a7eb67f4ec4fb86a27097eb4",
                    "Secret": "406851c5d1ce570d8dd192b412ece7ef1ee85fea81135b2839ba7a22d320e0ff",
                    "Postcommunion": "d0615d75979ceaa5f7ca2b366c1b584a2b532ded87b65e5e04533a3cfd8e0b37",
                }[name])
                self.assertNotIn("Et non fit commemoratio", proper["text"])
        # The source still inventories the seasonal-votive Tract, but it is
        # not appointed in October: its old represented join is removed.
        self.assertNotIn("Tract", propers)
        self.assertEqual(states[f"{prefix}:slot:p779-l19:tract"], "not-represented")
        # Neither printed Alleluia alternative is joined to the held October
        # Alleluia. The held Preface appointment likewise supplies no new join.
        self.assertEqual(sum(row["name"] == "Alleluia" for row in mass["propers"]), 1)
        self.assertEqual(mass["ordinary_appointments"]["preface"]["option"], "christo-rege")
        self.assertEqual({key for key, value in states.items() if value == "unresolved"}, {
            f"{prefix}:slot:p779-l12:alleluia",
            f"{prefix}:slot:p779-l29:alleluia",
            f"{prefix}:preface:p779-l69",
        })
        bounded = next(row for row in coverage.bounded_form_text_slots(report)
                       if row["mass"] == "christ-the-king")
        self.assertEqual((bounded["lower_bound"], bounded["represented"],
                          bounded["not_represented"], bounded["unresolved"]), (13, 9, 1, 3))
        self.assertEqual((bounded["denominator_state"], bounded["expected"],
                          bounded["whole_form_state"]), ("unresolved", None, "unresolved"))

    def test_cummiskey_and_lasance_rows_declare_the_evidenced_antecedent_relation(self):
        """C3: every date-bound hand-missal row is typed as Caswall's is."""
        import tomllib
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml")
                               .read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in ledger["sources"]}
        for source_id in ("cummiskey-1861", "cummiskey-1843", "cummiskey-1861-transcription",
                          "lasance-1945", "caswall-1849"):
            with self.subTest(source=source_id):
                row = rows[source_id]
                self.assertEqual(row["witness_relation"], "antecedent")
                self.assertTrue(row["witness_relation_basis"].strip())
                self.assertEqual(row["attests_kind"], "date-bound")
                self.assertNotEqual(row["attests"], "unestablished")
        # The Anglican hymn book attests no Roman act and stays untyped.
        self.assertNotIn("witness_relation", rows["hymns-ancient-and-modern-1890"])
        # Every positive Cummiskey or Lasance body therefore counts as a
        # historical antecedent, never as unresolved.
        relations = set()
        for mass in self.files["roman-1962"]["masses"]:
            for proper in mass["propers"]:
                english_row = (proper.get("coverage") or {}).get("languages", [{}, {}])[1]
                for witness in english_row.get("witnesses") or []:
                    if "cummiskey" in witness["id"] or "lasance" in witness["id"]:
                        relations.add(witness["relationship"])
        self.assertEqual(relations, {"historical-antecedent"})

    def test_no_public_domain_witness_absence_is_typed_rights_withheld(self):
        # G3: `rights-withheld` asserts a restriction. The only 1962 rows that
        # keep it are the Supreme-Pontiff readings on Lasance's excluded insert.
        import tomllib
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml")
                               .read_text(encoding="utf-8"))
        withheld = [row for row in ledger["untranslated"] if row["reason"]["kind"] == "rights-withheld"]
        self.assertEqual({row["mass"] for row in withheld}, {"commune-summorum-pontificum"})
        self.assertEqual(len(withheld), 5)
        retyped = [row for row in ledger["untranslated"] if "(C2 gap G3)" in row["note"]]
        # 336 since 2026-10-19 (C3): the Pentecost Collect, Secret and
        # Postcommunion were bound and left the untranslated ledger; 335 once
        # the Pentecost Alleluia was bound the same day (G14 lane).
        self.assertEqual(len(retyped), 335)
        self.assertEqual({row["reason"]["kind"] for row in retyped}, {"no-exemplar"})
        restricted = [unit for mass in self.files["roman-1962"]["masses"]
                      for unit in coverage.proper_units(mass)
                      if english(unit)["availability"] == "not-publishable"]
        self.assertTrue(restricted)
        self.assertTrue(all("summorum-pontificum" in unit["target_id"] for unit in restricted))

    def test_pentecost_19_keeps_all_seven_scripture_bearing_propers(self):
        mass = next(row for row in self.files["roman-1962"]["masses"] if row["key"] == "pentecost-19")
        report = english(mass["coverage"])
        self.assertEqual(sum(bool(row["citations"]) for row in mass["propers"]), 7)
        self.assertEqual(report["scripture_occurrences"], 7)
        self.assertEqual(report["mixed_occurrences"], 1)
        self.assertEqual(report["occurrences"], 4)


class ExpectedInventoryTests(unittest.TestCase):
    def test_ember_advent_lent_english_owners_keep_each_source_form_and_oratio_occurrence(self):
        expected = set([('advent-ember-saturday', 'longer', 'Collect', 1), ('advent-ember-saturday', 'longer', 'Oratio', 1), ('advent-ember-saturday', 'longer', 'Oratio', 2), ('advent-ember-saturday', 'longer', 'Oratio', 3), ('advent-ember-saturday', 'longer', 'Oratio', 4), ('advent-ember-saturday', 'longer', 'Oratio', 5), ('advent-ember-saturday', 'longer', 'Postcommunion', 1), ('advent-ember-saturday', 'longer', 'Secret', 1), ('advent-ember-saturday', 'shorter', 'Collect', 1), ('advent-ember-saturday', 'shorter', 'Oratio', 1), ('advent-ember-saturday', 'shorter', 'Postcommunion', 1), ('advent-ember-saturday', 'shorter', 'Secret', 1), ('lent-1-ember-saturday', 'longer', 'Collect', 1), ('lent-1-ember-saturday', 'longer', 'Oratio', 1), ('lent-1-ember-saturday', 'longer', 'Oratio', 2), ('lent-1-ember-saturday', 'longer', 'Oratio', 3), ('lent-1-ember-saturday', 'longer', 'Oratio', 4), ('lent-1-ember-saturday', 'longer', 'Oratio', 5), ('lent-1-ember-saturday', 'longer', 'Oratio', 6), ('lent-1-ember-saturday', 'longer', 'Postcommunion', 1), ('lent-1-ember-saturday', 'longer', 'Secret', 1), ('lent-1-ember-saturday', 'shorter', 'Collect', 1), ('lent-1-ember-saturday', 'shorter', 'Oratio', 1), ('lent-1-ember-saturday', 'shorter', 'Oratio', 2), ('lent-1-ember-saturday', 'shorter', 'Postcommunion', 1), ('lent-1-ember-saturday', 'shorter', 'Secret', 1)])
        expected.add(("lent-1-ember-saturday", "longer", "Hymn (Benedictus es)", 1))
        masses = {row[0] for row in expected}
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
        rows = [row for row in ledger["untranslated"] if row["mass"] in masses]
        self.assertEqual(27, len(rows))
        actual = {(row["mass"], row["form_id"], row["proper"], row["occurrence"]) for row in rows}
        self.assertEqual(expected, actual)
        self.assertFalse([row for row in ledger["entries"] if row["mass"] in masses])
        for row in rows:
            self.assertEqual(("all", "en", "body", "unavailable"),
                             tuple(row[k] for k in ("cycle", "lang", "extent", "availability")))
            self.assertEqual({"kind": "no-exemplar"}, row["reason"])
            self.assertNotIn("text", row)
            self.assertNotIn("text-free", row["note"])
        propers = tool("mass-propers")
        for calendar in ("roman-1962", "roman-pre-1955"):
            report = propers.english_coverage(ROOT / "src/sources/calendars", calendar)
            self.assertEqual((0, 0, 0), (report["outside_the_ledger"], report["unaccounted"], report["unmatched_records"]))

    def test_christmas_existing_nine_english_absences_keep_stable_form_ids(self):
        propers = tool("mass-propers")
        root = ROOT / "src/sources/calendars"
        path = ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml"
        ledger = tomllib.loads(path.read_text())
        rows = [row for row in ledger["untranslated"] if row["mass"] == "nativitate-domini-octave"]
        expected = {(form_id, name) for form_id in ("night", "dawn", "day")
                    for name in ("Collect", "Secret", "Postcommunion")}
        self.assertEqual(9, len([row for row in rows if row["proper"] != "Alleluia"]))
        expected.add(("day", "Alleluia"))
        self.assertEqual(10, len(rows))
        self.assertEqual(expected, {(row["form_id"], row["proper"]) for row in rows})
        for row in rows:
            with self.subTest(form=row["form_id"], proper=row["proper"]):
                self.assertEqual(("all", 1, "en", "body", "unavailable"),
                                 tuple(row[key] for key in ("cycle", "occurrence", "lang", "extent", "availability")))
                self.assertEqual({"kind": "no-exemplar"}, row["reason"])
                self.assertNotIn("text", row)
                self.assertNotIn("text-free", row["note"])
        self.assertFalse([row for row in ledger["entries"] if row["mass"] == "nativitate-domini-octave"])
        pre55 = tomllib.loads((ROOT / "src/sources/inventories/roman-pre-1955-proper-translations-v1.toml").read_text())
        self.assertFalse([row for row in pre55.get("untranslated", []) if row["mass"] == "nativitate-domini-octave"])
        for calendar in ("roman-1962", "roman-pre-1955"):
            report = propers.english_coverage(root, calendar)
            for key in ("unaccounted", "unmatched_records", "stale_translation_records"):
                self.assertEqual(0, report[key], (calendar, key))

    def inventory(self):
        return '''schema = "triptych-missal-expected-targets/v1"
as_of = "2026-10-19"
[[slices]]
id = "fixed"
calendar = "roman-1962"
recension_id = "roman-1962"
territory = "universal"
languages = ["la", "en"]
date_range = "edition snapshot"
source_refs = ["source.toml"]
enumeration_state = "complete-within-slice"
basis = "Independent calendar identities only"
[[targets]]
id = "feast"
slice_id = "fixed"
kind = "celebration"
calendar_mass_key = "feast"
identity_state = "established"
[[boundaries]]
id = "unclosed"
slice_id = "fixed"
kind = "text-slots"
state = "unenumerated"
'''

    def test_heterogeneous_inventory_does_not_become_text_denominator(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.toml"
            path.write_text(self.inventory())
            report = coverage.expectations(path, "roman-1962", [{"key": "feast"}])
        self.assertEqual(report["targets"][0]["state"], "represented")
        self.assertEqual(report["slices"][0]["kinds"], [{"kind": "celebration", "states": {"represented": 1}}])
        self.assertEqual(report["boundaries"][0]["state"], "unenumerated")
        self.assertNotIn("expected_text_slots", report)
        self.assertEqual(report["slices"][0]["source_refs"], ["source.toml"])

    def test_invalid_inventory_rows_fail_closed(self):
        mutations = (
            self.inventory().replace('slice_id = "fixed"', 'slice_id = "unknown"'),
            self.inventory().replace('kind = "celebration"', 'kind = "typo"'),
            self.inventory().replace('calendar_mass_key = "feast"', 'calendar_mass_key = 42'),
            self.inventory() + '\n[[targets]]\nid="feast"\nslice_id="fixed"\nkind="common"\nidentity_state="established"\n',
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.toml"
            for value in mutations:
                path.write_text(value)
                with self.subTest(value=value), self.assertRaises(ValueError):
                    coverage.expectations(path, "roman-1962", [])

    def test_form_cycle_mapping_stays_inside_its_form_and_accepts_implicit_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.toml"
            path.write_text(self.inventory().replace('kind = "celebration"', 'kind = "form"\nform_id = "main"'))
            main = {"key": "feast", "propers": [{"form_id": "main"}]}
            self.assertEqual(coverage.expectations(path, "roman-1962", [main])["targets"][0]["state"], "represented")
            path.write_text(self.inventory().replace('kind = "celebration"',
                                                     'kind = "cycle"\nform_id = "vigil"\ncycle = "A"\ncycle_family = "sunday"'))
            mass = {"key": "feast", "forms": [{"id": "vigil"}, {"id": "day"}], "propers": [
                {"form_id": "day", "cycles": {"A": {"coverage": coverage.unit({}, target_id="t", occurrence_id="o", cycle="A", cycle_family="cycles")}}},
            ]}
            self.assertEqual(coverage.expectations(path, "roman-1962", [mass])["targets"][0]["state"], "not-represented")

    def test_form_id_is_only_a_calendar_form_join(self):
        """`form_id` once also named a parent target; that use is `parent_id` now.

        Decision 2026-10-19: the validator reads `form_id` beside
        `calendar_mass_key` as a form of the held Mass, so a parent reference in
        the same field would be misread the moment its row gained a join. The
        13,926 parent references moved to `parent_id` and the 1,175 source-local
        formulary keys to `source_form_key`; `form_id` without a join is refused.
        """
        parent = ('\n[[targets]]\nid="slot"\nslice_id="fixed"\nkind="text-slot"\n'
                  'identity_state="established"\n')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.toml"
            for extra in (parent + 'form_id="feast"\n', parent + 'parent_id="nowhere"\n',
                          parent + 'parent_id="slot"\n'):
                path.write_text(self.inventory() + extra)
                with self.subTest(extra=extra), self.assertRaises(ValueError):
                    coverage.expectations(path, "roman-1962", [{"key": "feast"}])
            path.write_text(self.inventory() + parent + 'parent_id="feast"\nsource_form_key="1.A"\n')
            report = coverage.expectations(path, "roman-1962", [{"key": "feast"}])
        self.assertEqual([row["state"] for row in report["targets"]], ["represented", "unresolved"])

    def test_tracked_inventory_joins_formularies_without_the_parent_hazard(self):
        path = ROOT / "src/sources/inventories/missal-expected-targets-v1.toml"
        document = tomllib.loads(path.read_text(encoding="utf-8"))
        ids = {row["id"] for row in document["targets"]}
        self.assertFalse([row["id"] for row in document["targets"]
                          if "form_id" in row and "calendar_mass_key" not in row])
        self.assertFalse([row["id"] for row in document["targets"]
                          if "parent_id" in row and row["parent_id"] not in ids])
        propers = tool("mass-propers")
        root = ROOT / "src/sources/calendars"
        # The formulary-level join (G4), pinned 2026-10-19: every joined form
        # row names a held Mass (and form). Update these counts only with the
        # inventory's own join rows, never to absorb a not-represented target.
        for calendar, joined in (("roman-1962", 489), ("roman-pre-1955", 463)):
            masses = [mass for _, mass in propers.masses_of(propers.load_calendar(root, calendar))]
            for mass in masses:
                if mass.get("forms"):
                    mass["forms"] = [{"id": form.get("id")} for form in mass["forms"]]
            report = coverage.expectations(path, calendar, masses)
            forms = Counter(row["state"] for row in report["targets"] if row["kind"] == "form")
            with self.subTest(calendar=calendar):
                self.assertEqual(forms["represented"], joined)
                self.assertEqual(forms["not-represented"], 0)
                if calendar == "roman-1962":
                    # AP111-112 / printed30-31 names this exact December29
                    # commemoration; it is not an inferred same-title join.
                    target = "roman-1962.temporal.thomas-canterbury"
                    self.assertEqual(next(row["state"] for row in report["targets"]
                                          if row["id"] == target), "represented")
                    without = [mass for mass in masses
                               if mass["key"] != "comm-s-thomae-episcopi-martyris"]
                    negative = coverage.expectations(path, calendar, without)
                    self.assertEqual(next(row["state"] for row in negative["targets"]
                                          if row["id"] == target), "not-represented")

    def test_new_parent_alleluia_absence_only_excludes_the_existing_absent_recension_mass(self):
        # This is inherited-ledger accounting for an already absent child Mass,
        # not new pre-1955 wording, calendar scope, or witness acceptance.
        root = ROOT / "src/sources/calendars"
        child = tomllib.loads((ROOT / "src/sources/inventories/roman-pre-1955-proper-translations-v1.toml").read_text())
        wanted = {"record": "untranslated", "mass": "s-ioseph-opificis-sponsi-beatae-mariae",
                  "form_id": "main", "proper": "Alleluia", "cycle": "all", "occurrence": 1,
                  "reason": "recension-absent", "basis": "calendar-departure"}
        self.assertEqual([row for row in child["inherited_inapplicable"]
                          if row["mass"] == wanted["mass"] and row["proper"] == "Alleluia"],
                         [wanted])
        parent = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
        records = [row for row in parent["untranslated"]
                   if (row["mass"], row["form_id"], row["proper"], row["cycle"], row["occurrence"])
                   == (wanted["mass"], "main", "Alleluia", "all", 1)]
        self.assertEqual(len(records), 1)
        self.assertEqual((records[0]["lang"], records[0]["extent"], records[0]["reason"]),
                         ("en", "body", {"kind": "no-exemplar"}))
        self.assertNotIn("text", records[0])
        propers = tool("mass-propers")
        raw = propers.load_calendar(root, "roman-pre-1955", effective=False)
        departure = next(mass for _, mass in propers.masses_of(raw)
                         if mass["key"] == wanted["mass"])
        self.assertEqual(departure["departure"], "absent")
        self.assertNotIn(wanted["mass"], {mass["key"] for _, mass in propers.masses_of(
            propers.load_calendar(root, "roman-pre-1955"))})
        report = propers.english_coverage(root, "roman-pre-1955")
        self.assertEqual((0, 0, 0), (report["unmatched_records"], report["unaccounted"],
                                   report["stale_translation_records"]))

    def test_1962_new_ember_oratios_join_only_the_exact_source_form_and_occurrence(self):
        # The source already owns twelve separately printed Oratio appointments.
        # Opening Collects, commemoration/ordination referrals and other slots
        # retain their previous independent dispositions.
        targets = [('roman-1962.temporal.pentecost-ember-sat-long:collect:2', 'pentecost-ember-saturday', 'longer', 1, 1377, 448), ('roman-1962.temporal.pentecost-ember-sat-long:collect:3', 'pentecost-ember-saturday', 'longer', 2, 1380, 448), ('roman-1962.temporal.pentecost-ember-sat-long:collect:4', 'pentecost-ember-saturday', 'longer', 3, 1383, 449), ('roman-1962.temporal.pentecost-ember-sat-long:collect:5', 'pentecost-ember-saturday', 'longer', 4, 1386, 449), ('roman-1962.temporal.pentecost-ember-sat-long:collect:6', 'pentecost-ember-saturday', 'longer', 5, 1389, 450), ('roman-1962.temporal.pentecost-ember-sat-short:collect:2', 'pentecost-ember-saturday', 'shorter', 1, 1402, 451), ('roman-1962.temporal.september-ember-sat-long:collect:2', 'september-ember-saturday', 'longer', 1, 1637, 485), ('roman-1962.temporal.september-ember-sat-long:collect:3', 'september-ember-saturday', 'longer', 2, 1640, 486), ('roman-1962.temporal.september-ember-sat-long:collect:4', 'september-ember-saturday', 'longer', 3, 1643, 486), ('roman-1962.temporal.september-ember-sat-long:collect:5', 'september-ember-saturday', 'longer', 4, 1646, 486), ('roman-1962.temporal.september-ember-sat-long:collect:6', 'september-ember-saturday', 'longer', 5, 1649, 487), ('roman-1962.temporal.september-ember-sat-short:collect:2', 'september-ember-saturday', 'shorter', 1, 1661, 489)]
        path = ROOT / "src/sources/inventories/missal-expected-targets-v1.toml"
        inventory = tomllib.loads(path.read_text())
        by_id = {row["id"]: row for row in inventory["targets"]}
        propers = tool("mass-propers")
        document = propers.load_calendar(ROOT / "src/sources/calendars", "roman-1962")
        masses = [mass for _, mass in propers.masses_of(document)]
        by_mass = {mass["key"]: mass for mass in masses}
        states = {row["id"]: row["state"] for row in coverage.expectations(path, "roman-1962", masses)["targets"]}
        for target_id, mass_key, form_id, occurrence, marginal, physical_page in targets:
            with self.subTest(target=target_id):
                row = by_id[target_id]; parent = by_id[row["parent_id"]]
                self.assertEqual((parent["calendar_mass_key"], parent["form_id"],
                                  row["calendar_proper_name"], row["calendar_proper_occurrence"]),
                                 (mass_key, form_id, "Oratio", occurrence))
                self.assertIn("numbered text " + str(marginal) + ";", row["source_locus"])
                self.assertIn("physical PDF p. " + str(physical_page) + ",", row["source_locus"])
                form = next(form for form in by_mass[mass_key]["forms"] if form["id"] == form_id)
                exact = [proper for proper in form["propers"] if proper["name"] == "Oratio"][occurrence - 1]
                self.assertIn("no." + str(marginal) + ";", exact["notes"])
                self.assertEqual(states[target_id], "represented")
        damaged = copy.deepcopy(masses)
        for mass in damaged:
            if mass["key"] in {"pentecost-ember-saturday", "september-ember-saturday"}:
                for form in mass["forms"]:
                    form["propers"] = [proper for proper in form["propers"] if proper["name"] != "Oratio"]
        missing = {row["id"]: row["state"] for row in coverage.expectations(path, "roman-1962", damaged)["targets"]}
        self.assertEqual({target_id: missing[target_id] for target_id, *_ in targets},
                         {target_id: "not-represented" for target_id, *_ in targets})

    def test_1962_pentecost_text_slots_join_their_appointed_units(self):
        path = ROOT / "src/sources/inventories/missal-expected-targets-v1.toml"
        propers = tool("mass-propers")
        document = propers.load_calendar(ROOT / "src/sources/calendars", "roman-1962")
        masses = [mass for _, mass in propers.masses_of(document)]

        def slots(rows):
            return {row["id"]: row["state"] for row in coverage.expectations(
                path, "roman-1962", rows)["targets"]
                if row["id"].startswith("roman-1962.temporal.pentecost:")}

        joined = slots(masses)
        self.assertEqual(len(joined), 13)
        self.assertEqual(set(joined.values()), {"represented"})

        changed = copy.deepcopy(masses)
        pentecost = next(mass for mass in changed if mass["key"] == "pentecost")
        pentecost["propers"] = [row for row in pentecost["propers"] if row["name"] != "Lesson"]
        pentecost["ordinary_appointments"]["preface"]["option"] = "trinitate"
        damaged = slots(changed)
        self.assertEqual({key for key, state in damaged.items() if state == "not-represented"}, {
            "roman-1962.temporal.pentecost:reading:1",
            "roman-1962.temporal.pentecost:preface:1",
        })

    def test_1962_source_inventoried_proper_joins_stay_one_to_one(self):
        path = ROOT / "src/sources/inventories/missal-expected-targets-v1.toml"
        inventory = tomllib.loads(path.read_text(encoding="utf-8"))
        by_id = {row["id"]: row for row in inventory["targets"]}
        expected = {
            "roman-1962-temporal-pre-holy-week-slots": 348,
            "roman-1962-temporal-lent-source-forms-slots": 362,
            "roman-1962-temporal-easter-through-last-sunday": 561,
            "roman-1962-sanctoral-printed-slots": 1936,
            "roman-1962-body-commons-slots": 220,
        }
        joined = [row for row in inventory["targets"]
                  if row["slice_id"] in expected and row.get("calendar_proper_name")]
        self.assertEqual(Counter(row["slice_id"] for row in joined), expected)
        calendar_units = set()
        for row in joined:
            parent = by_id[row["parent_id"]]
            self.assertEqual((row["identity_state"], parent["identity_state"], parent["kind"]),
                             ("established", "established", "form"))
            self.assertTrue(row.get("source_record") and row.get("source_locus"))
            unit_key = (parent["calendar_mass_key"], parent.get("form_id") or "main",
                        row["calendar_proper_name"], row.get("calendar_proper_occurrence", 1))
            self.assertNotIn(unit_key, calendar_units,
                             "two independently inventoried slots cannot borrow one held Proper")
            calendar_units.add(unit_key)

        propers = tool("mass-propers")
        document = propers.load_calendar(ROOT / "src/sources/calendars", "roman-1962")
        masses = [mass for _, mass in propers.masses_of(document)]
        current = {row["id"]: row["state"] for row in coverage.expectations(
            path, "roman-1962", masses)["targets"]}
        self.assertEqual(Counter(current[row["id"]] for row in joined),
                         {"represented": 3133, "not-represented": 294})
        gap_id = "roman-1962:sanctoral-form:p511-l46:slot:p511-l62:secret"
        self.assertEqual(current[gap_id], "represented")

        damaged = copy.deepcopy(masses)
        by_key = {mass["key"]: mass for mass in damaged}
        for key, name in (("advent-1", "Introit"),
                          ("comm-s-saturnini-martyris", "Collect"),
                          ("commune-summorum-pontificum", "Introit")):
            mass = by_key[key]
            mass["propers"] = [row for row in mass["propers"] if row["name"] != name]
        ember = by_key["advent-ember-saturday"]
        longer = next(form for form in ember["forms"] if form["id"] == "longer")
        shorter = next(form for form in ember["forms"] if form["id"] == "shorter")
        self.assertTrue(any(row["name"] == "Introit" for row in shorter["propers"]))
        longer["propers"] = [row for row in longer["propers"] if row["name"] != "Introit"]
        # The now represented source-named Secret stops resolving if its
        # exact direct appointment is removed; inherited wording is no substitute.
        bibiana = by_key["s-bibianae-virginis-martyris"]
        bibiana["propers"] = [row for row in bibiana["propers"] if row["name"] != "Secret"]
        changed = {row["id"]: row["state"] for row in coverage.expectations(
            path, "roman-1962", damaged)["targets"]}
        self.assertEqual(changed[gap_id], "not-represented")
        for target_id in (
            "roman-1962.temporal.advent-1:introit:1",
            "roman-1962:sanctoral-form:p509-l16:slot:p509-l22:collect",
            "roman-1962:body:common-popes:introit:1",
            "roman-1962.temporal.advent-ember-saturday-long:introit:1",
        ):
            self.assertEqual((current[target_id], changed[target_id]),
                             ("represented", "not-represented"))

    def test_1962_normal_chant_slots_keep_exact_occurrences_beside_paschal_alternatives(self):
        # These printed local units precede the separate Paschal Common referral.
        # AP629/630 units2750,2754,2756,2758; AP716/717 units3444,3450,3452.
        targets = {
            "p629-l45:slot:p629-l49:introit": ("s-barnabae-apostoli", "Introit"),
            "p629-l45:slot:p630-l17:alleluia": ("s-barnabae-apostoli", "Alleluia"),
            "p629-l45:slot:p630-l43:offertory-antiphon": ("s-barnabae-apostoli", "Offertory"),
            "p629-l45:slot:p630-l55:communion-antiphon": ("s-barnabae-apostoli", "Communion"),
            "p716-l42:slot:p716-l45:introit": ("s-bartholomaei-apostoli", "Introit"),
            "p716-l42:slot:p717-l33:offertory-antiphon": ("s-bartholomaei-apostoli", "Offertory"),
            "p716-l42:slot:p717-l46:communion-antiphon": ("s-bartholomaei-apostoli", "Communion"),
        }
        path = ROOT / "src/sources/inventories/missal-expected-targets-v1.toml"
        inventory = tomllib.loads(path.read_text())
        by_id = {row["id"]: row for row in inventory["targets"]}
        propers = tool("mass-propers")
        document = propers.load_calendar(ROOT / "src/sources/calendars", "roman-1962")
        masses = {mass["key"]: mass for _, mass in propers.masses_of(document)}
        states = {row["id"]: row["state"] for row in coverage.expectations(
            path, "roman-1962", list(masses.values()))["targets"]}
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "inventory.toml"
            for suffix, (mass_key, name) in targets.items():
                target_id = "roman-1962:sanctoral-form:" + suffix
                row = by_id[target_id]
                with self.subTest(target=target_id):
                    self.assertEqual((row["calendar_proper_name"], row.get("calendar_proper_occurrence")),
                                     (name, 1))
                    self.assertEqual(by_id[row["parent_id"]]["calendar_mass_key"], mass_key)
                    matches = [p for p in masses[mass_key]["propers"] if p["name"] == name]
                    self.assertEqual(len(matches), 2)
                    self.assertEqual([p["ordinary_disposition"]["option"] for p in matches],
                                     ["non-paschal", "paschal"])
                    self.assertNotIn("takes_from", matches[0])
                    self.assertEqual(matches[1]["takes_from"]["mass"],
                                     "commune-martyrum-tempore-paschali-1")
                    self.assertEqual(states[target_id], "represented")
                    # The original ambiguity and an out-of-range ordinal both
                    # refuse. An occurrence is a source coordinate, not a
                    # permission to choose the first convenient same-name row.
                    parent = self.inventory().replace('kind = "celebration"', 'kind = "form"')
                    parent = parent.replace('calendar_mass_key = "feast"',
                                            'calendar_mass_key = ' + json.dumps(mass_key))
                    slot = ('\n[[targets]]\nid="slot"\nslice_id="fixed"\nkind="text-slot"\n'
                            'identity_state="established"\nparent_id="feast"\ncalendar_proper_name='
                            + json.dumps(name) + '\n')
                    for occurrence, wanted in ((None, "not-represented"), (1, "represented"),
                                                (3, "not-represented")):
                        value = parent + slot
                        if occurrence is not None:
                            value += f"calendar_proper_occurrence={occurrence}\n"
                        fixture.write_text(value)
                        found = coverage.expectations(fixture, "roman-1962", [masses[mass_key]])
                        self.assertEqual(found["targets"][-1]["state"], wanted)

    def test_1962_matthias_votive_alleluia_does_not_borrow_the_paschal_referral(self):
        # AP562/printed481 line17 is unit2225 under the votive-only heading;
        # the distinct normal-Paschal Protexisti referral starts at line20.
        target_id = "roman-1962:sanctoral-form:p560-l59:slot:p562-l17:alleluia"
        path = ROOT / "src/sources/inventories/missal-expected-targets-v1.toml"
        inventory = tomllib.loads(path.read_text())
        row = next(row for row in inventory["targets"] if row["id"] == target_id)
        self.assertEqual(row["calendar_proper_name"], "Alleluia")
        self.assertEqual(row["source_locus"],
                         "artifact p. 562 / printed p. 481, raw page-local line 17")
        propers = tool("mass-propers")
        document = propers.load_calendar(ROOT / "src/sources/calendars", "roman-1962")
        mass = next(mass for _, mass in propers.masses_of(document)
                    if mass["key"] == "s-matthiae-apostoli")
        self.assertFalse([p for p in mass["propers"] if p["name"] == "Alleluia"])
        paschal = [p for p in mass["propers"] if p["name"] == "Alleluia (Tempore paschali)"]
        self.assertEqual(len(paschal), 1)
        self.assertEqual(paschal[0]["takes_from"]["mass"],
                         "commune-martyrum-tempore-paschali-1")
        states = {r["id"]: r["state"] for r in coverage.expectations(
            path, "roman-1962", [mass])["targets"]}
        self.assertEqual(states[target_id], "not-represented")

    def test_1962_effective_sanctoral_repairs_join_the_printed_slots(self):
        propers = tool("mass-propers")
        document = propers.calendar_structure(
            ROOT / "src/sources/calendars", "roman-1962", propers.book_tokens())
        masses = {mass["key"]: mass for mass in document["masses"]}
        joins = {
            "roman-1962:sanctoral-form:p518-l3:slot:p518-l21:collect":
                ("conceptione-immaculata-beatae-mariae-virginis", "Collect", None),
            "roman-1962:sanctoral-form:p511-l74:slot:p512-l44:alleluia":
                ("s-francisci-xaverii-confessoris", "Alleluia", "James 1:12"),
            "roman-1962:sanctoral-form:p520-l55:slot:p521-l10:alleluia":
                ("s-luciae-virginis-martyris", "Alleluia", "Psalms 44:3"),
            "roman-1962:sanctoral-form:p520-l55:slot:p521-l57:communion-antiphon":
                ("s-luciae-virginis-martyris", "Communion", "Psalms 118:161-162"),
            "roman-1962:sanctoral-form:p564-l51:slot:p564-l58:collect":
                ("ss-perpetuae-felicitatis-martyrum",
                 "Collect (Pro pluribus Martyribus quae non sint Virgines)", None),
            "roman-1962:sanctoral-form:p564-l51:slot:p564-l66:secret":
                ("ss-perpetuae-felicitatis-martyrum",
                 "Secret (Pro pluribus Martyribus quae non sint Virgines)", None),
            "roman-1962:sanctoral-form:p589-l34:slot:p589-l40:collect":
                ("ss-soteris-caii-paparum-martyrum", "Collect (in plurali)", None),
            "roman-1962:sanctoral-form:p590-l75:slot:p591-l14:secret":
                ("s-fidelis-sigmaringa-martyris", "Secret (Pro Martyre tantum)", None),
            "roman-1962:sanctoral-form:p590-l75:slot:p591-l21:postcommunion":
                ("s-fidelis-sigmaringa-martyris", "Postcommunion (Pro Martyre tantum)", None),
            "roman-1962:sanctoral-form:p601-l74:slot:p602-l9:secret":
                ("s-stanislai-episcopi-martyris", "Secret (Item altera secreta)", None),
            "roman-1962:sanctoral-form:p601-l74:slot:p602-l15:postcommunion":
                ("s-stanislai-episcopi-martyris", "Postcommunion (Item altera postcommunio)", None),
        }
        states = {row["id"]: row["state"] for row in coverage.expectations(
            ROOT / "src/sources/inventories/missal-expected-targets-v1.toml",
            "roman-1962", document["masses"])["targets"]}
        for target_id, (mass_key, proper_name, citation) in joins.items():
            with self.subTest(target=target_id):
                self.assertEqual(states[target_id], "represented")
                held = [proper for proper in masses[mass_key]["propers"]
                        if proper["name"] == proper_name]
                self.assertEqual(len(held), 1)
                if citation:
                    self.assertEqual([row["ref"] for row in held[0]["citations"]], [citation])
        published = document["coverage"]["expected_inventory"]
        self.assertEqual(published["target_states"],
                         {"represented": 4196, "not-represented": 90, "unresolved": 3705})
        self.assertEqual({row["id"] for row in published["not_represented"]} & joins.keys(), set())
        # The source's Tract1877 is explicitly votive after Septuagesima;
        # it remains an expected source obligation outside this feast model.
        self.assertIn("roman-1962:sanctoral-form:p518-l3:slot:p519-l29:tract",
                      {row["id"] for row in published["not_represented"]})

    def test_1962_source_checked_scripture_roles_join_in_ritual_order(self):
        propers = tool("mass-propers")
        document = propers.calendar_structure(
            ROOT / "src/sources/calendars", "roman-1962", propers.book_tokens())
        masses = {mass["key"]: mass for mass in document["masses"]}
        # Expected-target identifiers and citations come from the 1962 facsimile's
        # numbered Sanctoral roles, independently of the YAML proper rows.
        rows = (
            ("p524-l43:slot:p525-l19:gospel", "s-pauli-primi-eremitae-confessoris", "Gospel", "Matthew 11:25-30", "Alleluia", "Offertory"),
            ("p527-l61:slot:p528-l50:gospel", "comm-ss-marii-marthae-audifacis-abachum", "Gospel", "Matthew 24:3-13", "Tract", "Offertory"),
            ("p572-l5:slot:p573-l19:gospel", "s-ioseph-sponsi-beatae-mariae-virginis", "Gospel", "Matthew 1:18-21", "Tract", "Secret"),
            ("p641-l21:slot:p642-l5:offertory-antiphon", "s-paulini-episcopi-confessoris", "Offertory", "Psalms 88:21-22", "Gospel", "Secret"),
            ("p663-l27:slot:p664-l28:gospel", "ss-septem-fratrum-martyrum-ac-ss", "Gospel", "Matthew 12:46-50", "Gradual", "Offertory"),
            ("p672-l66:slot:p673-l39:gospel", "s-vincentii-a-paulo-confessoris", "Gospel", "Luke 10:1-9", "Gradual", "Offertory"),
            ("p644-l1:slot:p645-l27:communion-antiphon", "nativitate-s-ioannis-baptistae", "Communion", "Luke 1:76", "Secret", "Postcommunion"),
            ("p722-l52:slot:p723-l17:gradual", "decollatione-s-ioannis-baptistae", "Gradual", "Psalm 91:13-14, 3", "Lesson", "Alleluia"),
            ("p755-l21:slot:p756-l14:gospel", "s-teresiae-a-iesu-infante-virginis", "Gospel", "Matthew 18:1-4", "Alleluia", "Offertory"),
            ("p758-l42:slot:p759-l48:gospel", "beatae-mariae-virginis-a-rosario", "Gospel", "Luke 1:26-38", "Gradual", "Offertory"),
            ("p764-l45:slot:p765-l43:gospel", "comm-ss-dionysii-episcopi-rustici-eleutherii", "Gospel", "Luke 12:1-8", "Alleluia", "Offertory"),
            ("p770-l57:slot:p771-l25:gradual", "s-lucae-evangelistae", "Gradual", "Psalms 18:5,2", "Epistle", "Alleluia"),
            ("p781-l46:slot:p782-l21:gospel", "ss-simonis-iudae-apostolorum", "Gospel", "John 15:17-25", "Alleluia", "Offertory"),
            ("p799-l15:slot:p799-l67:gospel", "s-iosaphat-episcopi-martyris", "Gospel", "John 10:11-16", "Gradual", "Secret"),
        )
        states = {row["id"]: row["state"] for row in coverage.expectations(
            ROOT / "src/sources/inventories/missal-expected-targets-v1.toml",
            "roman-1962", document["masses"])["targets"]}
        for locus, key, role, citation, before, after in rows:
            with self.subTest(locus=locus):
                target_id = f"roman-1962:sanctoral-form:{locus}"
                self.assertEqual(states[target_id], "represented")
                named = [proper for proper in masses[key]["propers"] if proper["name"] == role]
                self.assertEqual(len(named), 1)
                self.assertEqual([row["ref"] for row in named[0]["citations"]], [citation])
                order = [proper["name"] for proper in masses[key]["propers"]]
                self.assertLess(order.index(before), order.index(role))
                self.assertLess(order.index(role), order.index(after))
        published = document["coverage"]["expected_inventory"]
        self.assertEqual(published["target_states"],
                         {"represented": 4196, "not-represented": 90, "unresolved": 3705})
        gaps = {row["id"] for row in published["not_represented"]}
        self.assertTrue(all(f"roman-1962:sanctoral-form:{locus}" not in gaps
                            for locus, *_ in rows))
        # These three source appointments are now joined. Removing the exact
        # roles must reopen exactly these targets; role presence does not
        # establish a whole Missal body or Bible-wording correspondence.
        repaired = (
            ("p529-l59:slot:p530-l26:gradual", "ss-fabiani-papae-sebastiani-martyrum", "Gradual"),
            ("p538-l32:slot:p539-l2:alleluia", "s-ioannis-chrysostomi-episcopi-confessoris-ecclesiae", "Alleluia"),
            ("p572-l5:slot:p573-l37:offertory-antiphon", "s-ioseph-sponsi-beatae-mariae-virginis", "Offertory"),
        )
        repaired_ids = {f"roman-1962:sanctoral-form:{locus}" for locus, _, _ in repaired}
        self.assertTrue(all(states[target] == "represented" for target in repaired_ids))
        damaged = copy.deepcopy(document["masses"])
        damaged_by_key = {mass["key"]: mass for mass in damaged}
        for _, key, role in repaired:
            matches = [p for p in damaged_by_key[key]["propers"] if p["name"] == role]
            self.assertEqual(len(matches), 1)
            damaged_by_key[key]["propers"] = [p for p in damaged_by_key[key]["propers"]
                                               if p["name"] != role]
        changed = {row["id"]: row["state"] for row in coverage.expectations(
            ROOT / "src/sources/inventories/missal-expected-targets-v1.toml",
            "roman-1962", damaged)["targets"]}
        self.assertEqual({target for target in states if changed[target] != states[target]},
                         repaired_ids)
        self.assertTrue(all(changed[target] == "not-represented" for target in repaired_ids))
        # These independently inventoried chant appointments are still
        # structurally missing. A represented role or Bible reconstruction alone
        # would not establish exact Missal wording.
        for locus in (
            "p535-l10:slot:p536-l78:communion-antiphon",
            "p688-l2:slot:p688-l45:gradual",
        ):
            self.assertIn(f"roman-1962:sanctoral-form:{locus}", gaps)
        # The March 24 Gabriel heading says Luc. 2, 26-38 but prints Luke 1's
        # Annunciation; no Bible passage is published under the wrong locator.
        self.assertIn("roman-1962:sanctoral-form:p574-l14:slot:p575-l19:gospel", gaps)

    def test_1962_st_thomas_introit_uses_exact_missal_words(self):
        propers = tool("mass-propers")
        root = ROOT / "src/sources/calendars"
        document = propers.calendar_structure(root, "roman-1962", propers.book_tokens())
        mass = next(row for row in document["masses"] if row["key"] == "s-thomae-apostoli")
        introit = mass["propers"][0]
        self.assertEqual((introit["name"], introit["source"]), ("Introit", "mixed"))
        self.assertEqual([row["ref"] for row in introit["citations"]],
                         ["Psalms 138:17", "Psalms 138:1-2"])
        # Independently collated spoken words of Mame 1922 printed p. 498
        # and the controlling 1962 edition printed p. 441. Their punctuation
        # and accents differ, but neither prints the Bible's honorificati.
        witness_words = ("Mihi autem nimis honorati sunt amici tui Deus nimis "
                         "confortatus est principatus eorum Domine probasti me "
                         "et cognovisti me tu cognovisti sessionem meam et "
                         "resurrectionem meam V Gloria Patri")
        self.assertEqual(re.findall(r"[A-Za-z]+", introit["text"]),
                         witness_words.split())
        self.assertNotIn("honorificati", introit["text"])
        projection = (ROOT / "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection"
                      "/editions/2026-09-03-editorial-projection/artifacts"
                      "/s-thomae-introit-74c5a893/s-thomae-introit-74c5a893.txt")
        self.assertEqual(projection.read_text(), introit["text"])
        latin = introit["latin"]
        self.assertEqual(hashlib.sha256(projection.read_bytes()).hexdigest(),
                         latin["text_sha256"])
        self.assertEqual(latin["provenance"]["relationship"],
                         "editorial-projection-exact-to-target")
        self.assertEqual(latin["provenance"]["verification_source_id"],
                         "passage.catholic-church.missale-romanum.vatican-typica-1962.s-thomae-apostoli-introit")
        self.assertIn("artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a",
                      latin["publication"]["source_ids"])
        self.assertFalse(latin["withheld"])
        states = {row["id"]: row["state"] for row in coverage.expectations(
            ROOT / "src/sources/inventories/missal-expected-targets-v1.toml",
            "roman-1962", document["masses"])["targets"]}
        self.assertEqual(states["roman-1962:sanctoral-form:p522-l16:slot:p522-l19:introit"],
                         "represented")
        for held in (
            "roman-1962:sanctoral-form:p526-l24:slot:p527-l8:offertory-antiphon",
            "roman-1962:sanctoral-form:p751-l15:slot:p751-l19:introit",
        ):
            self.assertEqual(states[held], "represented")

    def test_1962_two_missal_chants_do_not_substitute_bible_words(self):
        propers = tool("mass-propers")
        document = propers.calendar_structure(
            ROOT / "src/sources/calendars", "roman-1962", propers.book_tokens())
        masses = {row["key"]: row for row in document["masses"]}
        artifact_root = (ROOT / "src/sources/works/triptych"
                         "/roman-1962-latin-proper-editorial-projection"
                         "/editions/2026-09-03-editorial-projection/artifacts")
        for key, name, artifact, citation, missal_words, bible_only in (
            ("s-antonii-abbatis", "Offertory", "s-antonii-offertory-28fd4214",
             "Psalms 20:3-4", "Desiderium animae eius", "in praevenisti"),
            ("dedicatione-s-michaelis-archangeli", "Introit",
             "s-michaelis-introit-dfe07c30", "Psalms 102:20",
             "qui facitis verbum eius", "facientes verbum eius"),
        ):
            with self.subTest(mass=key):
                proper = next(row for row in masses[key]["propers"]
                              if row["name"] == name)
                self.assertEqual(proper["source"], "mixed")
                self.assertEqual(proper["citations"][0]["ref"], citation)
                self.assertIn(missal_words, " ".join(proper["text"].split()))
                self.assertNotIn(bible_only, proper["text"])
                projection = next((artifact_root / artifact).glob("*.txt"))
                self.assertEqual(projection.read_text(), proper["text"])
                self.assertEqual(hashlib.sha256(projection.read_bytes()).hexdigest(),
                                 proper["latin"]["text_sha256"])
                self.assertEqual(proper["latin"]["provenance"]["relationship"],
                                 "editorial-projection-exact-to-target")

    def test_all_saints_new_own_bodies_have_shared_english_absences(self):
        propers = tool("mass-propers")
        root = ROOT / "src/sources/calendars"
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml")
                               .read_text())
        names = {"Introit", "Collect", "Secret", "Postcommunion"}
        for name in names:
            with self.subTest(proper=name):
                rows = [row for row in ledger["untranslated"]
                        if (row["mass"], row["form_id"], row["proper"], row["cycle"],
                            row["occurrence"], row["lang"], row["extent"]) ==
                        ("omnium-sanctorum", "main", name, "all", 1, "en", "body")]
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["reason"], {"kind": "no-exemplar"})
                self.assertEqual(rows[0]["availability"], "unavailable")
                self.assertNotIn("text", rows[0])
                self.assertFalse([row for row in ledger["entries"]
                                  if row["mass"] == "omnium-sanctorum"
                                  and row["proper"] == name])
        pre55 = tomllib.loads((ROOT / "src/sources/inventories/roman-pre-1955-proper-translations-v1.toml")
                              .read_text()).get("untranslated", [])
        self.assertFalse([row for row in pre55 if row["mass"] == "omnium-sanctorum"
                          and row["proper"] in names])
        for calendar in ("roman-1962", "roman-pre-1955"):
            with self.subTest(calendar=calendar):
                report = propers.english_coverage(root, calendar)
                self.assertEqual(report["unaccounted"], 0)
                self.assertEqual(report["unmatched_records"], 0)
                self.assertEqual(report["stale_translation_records"], 0)

    def test_six_new_own_orations_have_shared_english_absences(self):
        propers = tool("mass-propers")
        root = ROOT / "src/sources/calendars"
        masses = {"s-antonii-padua-confessoris-ecclesiae-doctoris",
                  "s-bibianae-virginis-martyris", "comm-s-sabbae-abbatis"}
        names = {"Secret", "Postcommunion"}
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml")
                               .read_text())
        expected = {(mass, "main", name, "all", 1, "en", "body")
                    for mass in masses for name in names}
        actual = []
        for row in ledger["untranslated"]:
            if row["mass"] not in masses or row["proper"] not in names:
                continue
            actual.append(tuple(row[field] for field in
                                ("mass", "form_id", "proper", "cycle", "occurrence", "lang", "extent")))
            self.assertEqual(row["availability"], "unavailable")
            self.assertEqual(row["reason"], {"kind": "no-exemplar"})
            self.assertNotIn("source_id", row)
            self.assertNotIn("text", row)
            self.assertNotIn("translations", row)
        self.assertEqual(len(actual), 6)
        self.assertEqual(set(actual), expected)
        self.assertFalse([row for row in ledger["entries"]
                          if row["mass"] in masses and row["proper"] in names])
        pre55 = tomllib.loads((ROOT / "src/sources/inventories/roman-pre-1955-proper-translations-v1.toml")
                              .read_text()).get("untranslated", [])
        self.assertFalse([row for row in pre55
                          if row["mass"] in masses and row["proper"] in names])
        for calendar in ("roman-1962", "roman-pre-1955"):
            with self.subTest(calendar=calendar):
                document = propers.load_calendar(root, calendar)
                source_masses = propers._calendars.mass_index(document)
                overlay, absent, stale, witnesses = propers.translation_overlay(calendar, root)
                for mass_key in masses:
                    mass = source_masses[mass_key]
                    appointed = [row for row in propers.appointed_propers(document, mass)
                                 if row[1]["name"] in names]
                    self.assertEqual(len(appointed), 2)
                    for form, proper, origin in appointed:
                        self.assertIsNone(origin)
                        self.assertEqual(proper["source"], "composed")
                        identity = propers.source_slot_identity(document, mass, form, proper, origin)
                        self.assertEqual(identity, (mass_key, "main", proper["name"], 1))
                        key = propers.overlay_key(mass, form, proper, origin)
                        self.assertEqual(key, (mass_key, "", proper["name"]))
                        carried = propers.carry_translations(calendar, key, proper, overlay,
                                                             stale, identity, witnesses)
                        self.assertFalse([row for row in carried.get("translations") or []
                                          if row.get("lang") == "en"])
                        records = propers.matching_untranslated_records(
                            carried, absent.get(propers.untranslated_key(identity)) or [], identity[3])
                        self.assertEqual(len(records), 1)
                        self.assertEqual(records[0]["reason"], {"kind": "no-exemplar"})
                report = propers.english_coverage(root, calendar)
                self.assertEqual(report["unaccounted"], 0)
                self.assertEqual(report["unmatched_records"], 0)
                self.assertEqual(report["stale_translation_records"], 0)

    def test_theodore_own_orations_have_shared_english_absences(self):
        propers = tool("mass-propers")
        root = ROOT / "src/sources/calendars"
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml")
                               .read_text())
        for name in ("Secret", "Postcommunion"):
            with self.subTest(proper=name):
                rows = [row for row in ledger["untranslated"]
                        if (row["mass"], row["form_id"], row["proper"], row["cycle"],
                            row["occurrence"], row["lang"], row["extent"]) ==
                        ("comm-s-theodori-martyris", "main", name, "all", 1, "en", "body")]
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["reason"], {"kind": "no-exemplar"})
                self.assertEqual(rows[0]["availability"], "unavailable")
                self.assertNotIn("text", rows[0])
                self.assertFalse([row for row in ledger["entries"]
                                  if row["mass"] == "comm-s-theodori-martyris"
                                  and row["proper"] == name])
        for calendar in ("roman-1962", "roman-pre-1955"):
            with self.subTest(calendar=calendar):
                report = propers.english_coverage(root, calendar)
                self.assertEqual(report["unaccounted"], 0)
                self.assertEqual(report["unmatched_records"], 0)
                self.assertEqual(report["stale_translation_records"], 0)
                absent = tomllib.loads((ROOT / "src/sources/inventories/roman-pre-1955-proper-translations-v1.toml")
                                       .read_text()).get("untranslated", [])
                self.assertFalse([row for row in absent
                                  if row["mass"] == "comm-s-theodori-martyris"
                                  and row["proper"] in {"Secret", "Postcommunion"}])

    def test_st_thomas_english_body_is_ledgered_for_both_calendars(self):
        propers = tool("mass-propers")
        root = ROOT / "src/sources/calendars"
        for calendar in ("roman-1962", "roman-pre-1955"):
            with self.subTest(calendar=calendar):
                result = propers.english_coverage(root, calendar)
                self.assertEqual(result["unaccounted"], 0)
                self.assertEqual(result["unmatched_records"], 0)
                rows = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml")
                                     .read_text())["untranslated"]
                self.assertEqual(len([row for row in rows
                                      if row["mass"] == "s-thomae-apostoli"
                                      and row["proper"] == "Introit"]), 1)

    def test_duplicate_held_proper_does_not_resolve_a_single_source_slot(self):
        slot = ('\n[[targets]]\nid="slot"\nslice_id="fixed"\nkind="text-slot"\n'
                'identity_state="established"\nparent_id="feast"\n'
                'calendar_proper_name="Introit"\n')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.toml"
            path.write_text(self.inventory().replace('kind = "celebration"',
                                                     'kind = "form"\nform_id = "main"') + slot)
            mass = {"key": "feast", "propers": [{"name": "Introit"}, {"name": "Introit"}]}
            states = {row["id"]: row["state"] for row in coverage.expectations(
                path, "roman-1962", [mass])["targets"]}
        self.assertEqual(states, {"feast": "represented", "slot": "not-represented"})

    def test_source_calendar_keeps_missing_christmas_commemoration_visible(self):
        propers = tool("mass-propers")
        document = propers.load_calendar(ROOT / "src/sources/calendars", "roman-1962")
        report = coverage.expectations(
            ROOT / "src/sources/inventories/missal-expected-targets-v1.toml",
            "roman-1962", [mass for _, mass in propers.masses_of(document)],
        )
        fixed = [row for row in report["targets"]
                 if row["slice_id"] == "roman-1962-universal-fixed-calendar"]
        self.assertEqual(len(fixed), 336)
        self.assertEqual(sum(row["state"] == "represented" for row in fixed), 335)
        missing = [row for row in fixed if row["state"] == "not-represented"]
        self.assertEqual([row["id"] for row in missing],
                         ["roman-1962:commemoration:1962-12-25-comm"])
        published = coverage.published_expectations(report)
        self.assertEqual(len(published["not_represented"]), 295)
        self.assertEqual([row["id"] for row in published["not_represented"]
                          if row["slice_id"] == "roman-1962-universal-fixed-calendar"],
                         ["roman-1962:commemoration:1962-12-25-comm"])

    def test_published_inventory_keeps_exact_totals_without_target_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.toml"
            path.write_text(self.inventory() + (
                '\n[[targets]]\nid="absent"\nslice_id="fixed"\nkind="commemoration"\n'
                'calendar_mass_key="absent"\nidentity_state="established"\n'
                '\n[[targets]]\nid="unmapped"\nslice_id="fixed"\nkind="preface"\n'
                'identity_state="target-correspondence-unresolved"\n'
            ))
            report = coverage.expectations(path, "roman-1962", [{"key": "feast"}])
        published = coverage.published_expectations(report)
        self.assertNotIn("targets", published)
        self.assertEqual(published["target_states"],
                         {"represented": 1, "not-represented": 1, "unresolved": 1})
        self.assertEqual(published["not_represented"],
                         [{"id": "absent", "slice_id": "fixed", "kind": "commemoration"}])
        # The boundaries and inventory state are carried whole, and the slice
        # summaries whole except `source_refs` (2026-10-19): those name
        # repository records, including restricted editions', which public
        # data must not carry.
        expected = {key: value for key, value in report.items() if key != "targets"}
        expected["slices"] = [{key: value for key, value in row.items() if key != "source_refs"}
                              for row in report["slices"]]
        self.assertTrue(all("source_refs" in row for row in report["slices"]))
        self.assertEqual({key: value for key, value in published.items()
                          if key not in {"target_states", "not_represented"}}, expected)
        # Totals agree with the slice summaries a reader can also add up.
        totals = {}
        for row in published["slices"]:
            for kind in row["kinds"]:
                for state, count in kind["states"].items():
                    totals[state] = totals.get(state, 0) + count
        self.assertEqual(totals, {key: value for key, value in published["target_states"].items() if value})
        with self.assertRaises(ValueError):
            coverage.published_expectations({"targets": [{"id": "x", "slice_id": "s", "kind": "form", "state": "typo"}]})

    def test_nested_summary_drops_only_file_level_constants(self):
        report = coverage.summarize([coverage.unit({"text": "x"}, target_id="t", occurrence_id="o")], "mass")
        nested = coverage.nested(report)
        self.assertEqual(set(report) - set(nested), {"count_basis", "denominator"})
        self.assertEqual({key: nested[key] for key in nested}, {key: report[key] for key in nested})
        coverage.validate_summary(nested)

    def test_unrecorded_inventory_projects_zero_totals(self):
        report = coverage.expectations(Path("/nonexistent/inventory.toml"), "roman-1962", [])
        published = coverage.published_expectations(report)
        self.assertEqual(published["state"], "unresolved")
        self.assertEqual(published["target_states"],
                         {"represented": 0, "not-represented": 0, "unresolved": 0})
        self.assertEqual(published["not_represented"], [])

    def test_uncited_own_chants_have_shared_english_absences(self):
        propers = tool("mass-propers")
        root = ROOT / "src/sources/calendars"
        identities = [('nativitate-beatae-mariae-virginis', 'Alleluia'), ('nativitate-beatae-mariae-virginis', 'Communion'), ('nativitate-beatae-mariae-virginis', 'Gradual'), ('nativitate-beatae-mariae-virginis', 'Introit'), ('nativitate-beatae-mariae-virginis', 'Offertory'), ('s-laurentii-martyris', 'Alleluia'), ('s-martini-episcopi-confessoris', 'Alleluia'), ('s-matthaei-apostoli-evangelistae', 'Alleluia')]
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
        absent_pre55 = tomllib.loads((ROOT / "src/sources/inventories/roman-pre-1955-proper-translations-v1.toml").read_text()).get("untranslated", [])
        for mass, name in identities:
            with self.subTest(mass=mass, proper=name):
                selected = [row for row in ledger["untranslated"]
                    if (row.get("mass"), row.get("form_id"), row.get("proper"), row.get("cycle"),
                        row.get("occurrence"), row.get("lang"), row.get("extent")) ==
                       (mass, "main", name, "all", 1, "en", "body")]
                self.assertEqual(len(selected), 1)
                self.assertEqual(selected[0]["availability"], "unavailable")
                self.assertEqual(selected[0]["reason"], {"kind": "no-exemplar"})
                self.assertNotIn("text", selected[0])
                self.assertFalse([row for row in ledger["entries"]
                                  if row["mass"] == mass and row["proper"] == name])
                self.assertFalse([row for row in absent_pre55
                                  if row["mass"] == mass and row["proper"] == name])
        for calendar in ("roman-1962", "roman-pre-1955"):
            with self.subTest(calendar=calendar):
                report = propers.english_coverage(root, calendar)
                for axis in ("unaccounted", "outside_the_ledger", "unmatched_records", "stale_translation_records"):
                    self.assertEqual(report[axis], 0)


if __name__ == "__main__":
    unittest.main()
