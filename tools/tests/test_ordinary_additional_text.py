#!/usr/bin/env python3
"""Additional witnesses fill one language without replacing source-owned data."""
import copy
import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


class OrdinaryAdditionalText(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader("ordinary_additional_tool", str(ROOT / "tools/mass-ordinary"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.tool = importlib.util.module_from_spec(spec)
        loader.exec_module(cls.tool)

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=ROOT / ".scratch")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "latin.tsv").write_text("element_key\tseq\tlatin\nunit\t1\tPer evangelica dicta.\n")
        self.artifact = "artifact.synthetic.additional-latin"
        self.witness = "edition.synthetic.additional"
        self.library = {self.artifact: {"id": self.artifact, "path": "latin.tsv", "_source_root": self.root}}
        self.witnesses = {(self.witness, "la"): {"rights": "public-domain", "artifacts": [self.artifact]}}
        self.absences = {"no-facing-latin": {"kind": "witness-gap"}}
        self.element = {
            "key": "section/unit", "kind": "prayer", "speaker": "all", "name": "Source prayer",
            "conditions": [], "note": "Source-owned English context.",
            "absent": {"english": None, "latin": "no-facing-latin"},
            "translations": [{"lang": "en", "source_id": "edition.synthetic.english",
                              "rights": "public-domain", "text": "Source English."}],
        }
        self.entry = {
            "element": "unit", "turns_basis": "Synthetic page assigns this Latin prayer to the priest.",
            "latin_turns": [{"key": "priest-prayer", "seq": [1], "speaker": "priest"}],
            "latin": {"witness": self.witness, "artifact": self.artifact, "elements": ["unit"],
                      "column": "latin", "relation": "antecedent", "collation": "uncollated",
                      "note": "The base witness lacks Latin; this separate witness supplies it."},
        }

    def apply(self, entries=None, *, element=None, keys=None, excluded=None, restricted=None):
        section = {"key": "section", "absent_latin_by_element": {"unit": "no-facing-latin"}}
        if entries is not None:
            section["additional_texts"] = entries
        elements = [copy.deepcopy(element if element is not None else self.element)]
        self.tool.artifact_additional_texts(
            section, {"unit"} if keys is None else keys, excluded or {}, elements,
            self.witnesses, restricted or {}, self.library, self.absences, "synthetic",
        )
        return section, elements[0]

    def test_absent_table_is_an_exact_noop(self):
        section, element = self.apply()
        self.assertEqual(element, self.element)
        self.assertEqual(section["absent_latin_by_element"], {"unit": "no-facing-latin"})

    def test_one_separate_latin_side_preserves_source_identity_and_english_actor(self):
        section, element = self.apply([self.entry])
        self.assertEqual(element | {"translations": self.element["translations"],
                                    "absent": self.element["absent"]}, self.element)
        self.assertEqual(element["speaker"], "all")
        self.assertEqual(element["translations"][0], self.element["translations"][0])
        latin = element["translations"][1]
        self.assertEqual((latin["lang"], latin["source_id"], latin["rights"], latin["text"]),
                         ("la", self.witness, "public-domain", "Per evangelica dicta."))
        self.assertEqual((latin["turns"][0]["speaker"], latin["turns"][0]["dialogue_role"]),
                         ("priest", None))
        self.assertIsNone(element["absent"]["latin"])
        self.assertEqual(section["absent_latin_by_element"], {"unit": "no-facing-latin"})
        self.assertEqual(self.entry["latin"]["relation"], "antecedent")

    def test_target_must_be_an_emitted_original_missing_language(self):
        cases = [
            {"entries": [self.entry | {"element": "unknown"}]},
            {"entries": [self.entry], "excluded": {"unit": "source-only"}},
            {"entries": [self.entry], "keys": {"other"}},
            {"entries": [self.entry], "element": self.element | {"occurrence_of": "section/other"}},
            {"entries": [self.entry], "element": self.element | {"absent": {"english": None, "latin": None}}},
            {"entries": [self.entry], "element": self.element | {"translations": [{"lang": "la", "text": "Held."}]}},
            {"entries": [self.entry, self.entry]},
        ]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(self.tool.SourceError):
                self.apply(**case)

    def test_closed_fields_require_explicit_source_and_one_language(self):
        malformed = [[], [None], [self.entry | {"speaker": "priest"}],
                     [self.entry | {"english": self.entry["latin"]}],
                     [{"element": "unit"}], [self.entry | {"latin": {}}],
                     [self.entry | {"english_turns": self.entry["latin_turns"]}]]
        for field in ("witness", "artifact", "column", "relation", "elements"):
            block = copy.deepcopy(self.entry["latin"])
            block.pop(field)
            malformed.append([self.entry | {"latin": block}])
        for extra in ({"unused": "ignored"}, {"element": "unit"}, {"elements": ["unit", "unit"]},
                      {"elements": []}, {"column": ""}, {"witness": {"id": self.witness}}):
            malformed.append([self.entry | {"latin": self.entry["latin"] | extra}])
        for entries in malformed:
            with self.subTest(entries=entries), self.assertRaises(self.tool.SourceError):
                self.apply(entries)

    def test_source_membership_and_restriction_are_not_bypassed(self):
        for block in (self.entry["latin"] | {"witness": "edition.unlisted"},
                      self.entry["latin"] | {"artifact": "artifact.unlisted"},
                      self.entry["latin"] | {"elements": ["missing-row"]}):
            with self.subTest(block=block), self.assertRaises(self.tool.SourceError):
                self.apply([self.entry | {"latin": block}])
        with self.assertRaisesRegex(self.tool.SourceError, "rights-restricted witness"):
            self.apply([self.entry], restricted={(self.witness, "la"): {}})

    def test_source_partition_needs_basis_and_exact_rows(self):
        for entry in (self.entry | {"turns_basis": ""},
                      {key: value for key, value in self.entry.items() if key != "turns_basis"},
                      {key: value for key, value in self.entry.items() if key != "latin_turns"},
                      {key: value for key, value in self.entry.items() if key not in ("turns_basis", "latin_turns")},
                      self.entry | {"latin_turns": []},
                      self.entry | {"latin_turns": [{"key": "wrong", "seq": [2], "speaker": "priest"}]}):
            with self.subTest(entry=entry), self.assertRaises(self.tool.SourceError):
                self.apply([entry])

    def test_unknown_added_actor_does_not_inherit_the_english_all(self):
        unknown = self.entry | {
            "turns_basis": "The synthetic source does not establish an actor; none is imported from English.",
            "latin_turns": [{"key": "actor-unknown", "seq": [1]}],
        }
        _section, element = self.apply([unknown])
        latin = element["translations"][1]
        self.assertEqual(element["speaker"], "all")
        self.assertIsNone(latin["turns"][0]["speaker"])
        self.assertIsNone(latin["turns"][0]["dialogue_role"])
        self.assertEqual(latin["turns"][0]["text"], "Per evangelica dicta.")

    def test_inline_sections_reject_the_artifact_only_table(self):
        library = self.tool.artifact_records(ROOT / "src/sources")
        path = ROOT / "src/sources/inventories/postconciliar-ordo-missae-v1.toml"
        inventory = self.tool.read_toml(path)
        inventory["sections"][0]["additional_texts"] = [self.entry]
        with patch.object(self.tool, "read_toml", return_value=inventory):
            with self.assertRaisesRegex(self.tool.SourceError, "artifact-only additional_texts"):
                self.tool.calendar_structure(ROOT / "src/sources", path, library)


if __name__ == "__main__":
    unittest.main()
