"""Consultation links must resolve to the registered artifact and an actual Mass form."""
from __future__ import annotations

import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
loader = SourceFileLoader("missal_witness_link_producer", str(ROOT / "tools/mass-propers"))
spec = spec_from_loader(loader.name, loader)
producer = module_from_spec(spec)
loader.exec_module(producer)


class MissalWitnessLinks(unittest.TestCase):
    root = ROOT / "src/sources/calendars"
    document = {"sections": {"temporal": {"kind": "temporal", "masses": [
        {"key": "nativity", "forms": [{"id": "night"}, {"id": "dawn"}]}
    ]}}}
    artifact = {"record_type": "artifact", "sha256": "a" * 64,
                "source_url": "https://example.org/missal.pdf"}
    facsimile = {"edition_label": "Latin missal", "language": "la", "source_id": "artifact.test",
                 "sha256": "a" * 64, "page_count": 10,
                 "pages": [{"mass": "nativity", "form_id": "dawn", "locus": "Collect", "page": 4}]}

    def project(self, inventory):
        with patch.object(producer._calendars, "read_toml", return_value=inventory), \
                patch.object(producer, "_source_library_records", return_value=({"artifact.test": self.artifact}, [])):
            return producer.missal_witness_links(self.root, "roman-1962", self.document)

    def test_dawn_page_does_not_qualify_the_night_form(self):
        rows = self.project({"facsimiles": [self.facsimile]})
        self.assertEqual(set(rows), {("nativity", "dawn")})
        link, = rows["nativity", "dawn"]
        self.assertEqual(link["url"], self.artifact["source_url"] + "#page=4")
        self.assertEqual(link["scope"], "form")
        self.assertEqual(link["locus"], "Collect (PDF p. 4)")

    def test_invalid_source_page_fingerprint_and_identity_fail(self):
        for field, value in [("sha256", "b" * 64), ("page", 0), ("page", 11), ("form_id", "day")]:
            broken = copy.deepcopy(self.facsimile)
            target = broken if field == "sha256" else broken["pages"][0]
            target[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.project({"facsimiles": [broken]})

    def test_links_name_the_registered_document_and_preserve_distinct_languages(self):
        original = {"source_id": "artifact.test", "locus": "Mass antiphons", "mass": "nativity",
                    "form_id": "dawn", "language": "en", "url": self.artifact["source_url"] + "#page=4"}
        rows = self.project({"entries": [original], "facsimiles": [self.facsimile]})
        self.assertEqual([row["language"] for row in rows["nativity", "dawn"]], ["en", "la"])
        with self.assertRaises(ValueError):
            self.project({"entries": [dict(original, url="https://example.org/other.pdf#page=4")]})
        with self.assertRaises(ValueError):
            self.project({"entries": [original, original]})


    def test_published_prayer_links_require_the_exact_language_role_and_form(self):
        row = {"source_id": "artifact.test", "locus": "Dawn Mass, Collect", "mass": "nativity",
               "form_id": "dawn", "language": "en", "url": self.artifact["source_url"] + "#Dawn",
               "prayer_roles": ["Collect"]}
        projected = self.project({"entries": [row]})["nativity", "dawn"][0]
        self.assertEqual(projected["prayer_roles"], ["Collect"])
        for edit in [{"language": "la"}, {"prayer_roles": ["Entrance Antiphon"]},
                     {"prayer_roles": ["Collect", "Collect"]}, {"scope": "section", "form_id": "main"}]:
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                self.project({"entries": [row | edit]})


    def test_a_restricted_proper_uses_only_its_proven_occurrence_or_unambiguous_form(self):
        source = {"scope": "form", "language": "en", "source_id": "registered-pdf", "url": "https://example.org/lectionary#page=20"}
        target = {"role": "Verse Before the Gospel", "occurrence": 2}
        alternative = source | {"proper_targets": [target]}
        record = {"lang": "en", "cycle": "all", "extent": "body",
                  "reason": {"kind": "rights-withheld", "source_id": source["source_id"]}}
        consult = producer.published_proper_source
        self.assertEqual(consult([alternative], target["role"], 2, []), alternative)
        self.assertIsNone(consult([alternative], target["role"], 1, [record]))
        self.assertEqual(consult([source], target["role"], 1, [record]), source)
        self.assertIsNone(consult([source, source | {"url": "https://example.org/lectionary#page=21"}],
                                  target["role"], 1, [record]))

    def test_latin_and_english_target_their_exact_occurrence_independently(self):
        first = {"role": "Entrance Antiphon", "occurrence": 1}
        second = {"role": "Entrance Antiphon", "occurrence": 2}
        communion = {"role": "Communion Antiphon", "occurrence": 1}
        en = {"scope": "form", "language": "en", "source_id": "english", "proper_targets": [second, communion]}
        la = {"scope": "form", "language": "la", "source_id": "latin", "proper_targets": [second]}
        general = {"scope": "form", "language": "la", "source_id": "whole-form"}
        held = [la, en, general]
        lookup = producer.published_proper_source
        self.assertEqual(lookup(held, second["role"], 2, [], "la"), la)
        self.assertEqual(lookup(held, second["role"], 2, [], "en"), en)
        self.assertEqual(lookup(held, communion["role"], 1, [], "en"), en)
        self.assertIsNone(lookup(held, communion["role"], 1, [], "la"))
        self.assertIsNone(lookup(held, first["role"], 1, [], "la"))
        with self.assertRaisesRegex(ValueError, "conflicting printed la"):
            lookup([la, dict(la, source_id="other-latin")], second["role"], 2, [], "la")


class MemorialPrayers(unittest.TestCase):
    roles = ["Prayer over the Offerings", "Prayer after Communion"]

    def sources(self):
        return {"schema": 1, "current_feria": True, "rule_source_id": "girm363",
                "roles": self.roles, "common_groups": [
                    {"id": "bishop", "mass": "pastors", "form_ids": ["first"], "label": "For a bishop"}],
                "memorials": [{"mass": "saint", "common_group_ids": ["bishop"],
                               "source_id": "missal", "url": "https://example.org/missal#one",
                               "locus": "Collect and referral, p. 1"}]}

    def project(self, inventory, extra_own=()):
        records = {"girm363": {"record_type": "passage"},
                   "missal": {"record_type": "artifact", "source_url": "https://example.org/missal"}}
        document = {"sections": {
            "saints": {"kind": "sanctoral", "masses": [{"key": "saint",
                "propers": [{"name": role} for role in ("Collect", *extra_own)]}]},
            "commons": {"kind": "common", "masses": [{"key": "pastors", "forms": [
                {"id": "first", "propers": [{"name": role} for role in self.roles]}]}]}}}
        with patch.object(producer._calendars, "read_toml", return_value=inventory), \
                patch.object(producer, "_source_library_records", return_value=(records, [])):
            return producer.memorial_prayer_sources(MissalWitnessLinks.root, "postconciliar", document)

    def test_independent_sources_keep_the_memorial_collect(self):
        inventory = self.sources()
        row = self.project(inventory)["saint"]
        self.assertEqual(row["roles"], self.roles)
        self.assertTrue(row["current_feria"])
        self.assertEqual(row["groups"], inventory["common_groups"])
        with self.assertRaises(ValueError):
            self.project(inventory, extra_own=[self.roles[1]])

    def test_referral_requires_the_registered_edition_and_the_actual_form(self):
        for field in ("url", "form_ids", "rule_source_id"):
            inventory = self.sources()
            if field == "url":
                inventory["memorials"][0][field] = "https://example.org/other#one"
            elif field == "form_ids":
                inventory["common_groups"][0][field] = ["second"]
            else:
                inventory[field] = "missing"
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.project(inventory)


if __name__ == "__main__":
    unittest.main()
