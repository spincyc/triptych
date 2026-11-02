"""Finite formulary scopes permit distinct English bodies at one Ordinary seat."""
from copy import deepcopy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRATCH = Path(os.environ.get("TRIPTYCH_TEST_SCRATCH", ROOT / ".scratch"))


class ScopedEnglishOrdinary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader(
            "ordinary_scoped_english_tool", str(ROOT / "tools/mass-ordinary"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.tool = importlib.util.module_from_spec(spec)
        loader.exec_module(cls.tool)

    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        directory = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.library = {}
        self.witnesses = {}
        self.blocks = []
        for label, rights, formulary in (
                ("historical", "public-domain", "march-19"),
                ("study", "project-created", "may-1")):
            filename = label + ".tsv"
            artifact = "artifact.synthetic." + label
            witness = "edition.synthetic." + label
            (self.root / filename).write_text(
                "element_key\tseq\tenglish\nbody\t1\t" + label + " source words.\n")
            self.library[artifact] = {
                "id": artifact, "path": filename, "_source_root": self.root}
            self.witnesses[witness, "en"] = {
                "lang": "en", "rights": rights, "artifacts": [artifact],
                "label": label + " witness"}
            self.blocks.append({
                "witness": witness, "artifact": artifact, "element": "body",
                "column": "english", "relation": "antecedent",
                "collation": "uncollated", "note": label + " source qualification.",
                "reading_note": "  " + label + " literal reading qualification.  ",
                "applicability": {"kind": "formulary", "calendar": "roman-1962",
                                  "formularies": [formulary], "basis": "Synthetic source scope."},
            })
        self.entry = {
            "key": "joseph", "kind": "prayer", "speaker": "priest",
            "name": "Synthetic Joseph Preface", "absent_latin": "no-latin",
            "english": self.blocks[0], "english_alternatives": [self.blocks[1]],
        }
        self.absences = {"no-latin": {"kind": "witness-gap", "label": "No Latin witness"}}

    def resolve(self, entry=None, restricted=None):
        return self.tool.from_inventory(
            {"key": "preface", "elements": [self.entry if entry is None else entry]},
            self.witnesses, restricted or {}, self.absences, {}, self.library,
            "synthetic.toml")[0]

    def report(self, entry=None):
        source = {"schema": self.tool.SCHEMA, "calendar": "roman-1962",
                  "title": "Synthetic frame", "advisory": "Synthetic only",
                  "derived_from": "Synthetic source",
                  "sections": [{"key": "preface", "elements": [entry or self.entry]}]}
        with patch.object(self.tool, "read_toml", return_value=source), \
             patch.object(self.tool, "restricted_witness_table", return_value={}), \
             patch.object(self.tool, "witness_table", return_value=self.witnesses), \
             patch.object(self.tool, "absence_table", return_value=self.absences), \
             patch.object(self.tool._calendars, "index_header", return_value="Synthetic edition"):
            return self.tool.calendar_structure(
                self.root, Path("roman-1962-ordo-missae-v1.toml"), self.library)

    def test_inline_source_offers_keep_literal_bodies_scopes_and_qualifications(self):
        before = deepcopy(self.entry)
        element = self.resolve()
        self.assertEqual(self.entry, before)
        self.assertEqual(element["key"], "preface/joseph")
        self.assertEqual(element["absent"], {"english": None, "latin": "no-latin"})
        self.assertEqual(len(element["translations"]), 2)
        for row, block in zip(element["translations"], self.blocks):
            self.assertEqual(row["source_id"], block["witness"])
            self.assertEqual(row["applicability"], block["applicability"])
            self.assertIsNot(row["applicability"]["formularies"], block["applicability"]["formularies"])
            self.assertEqual(row["reading_note"], block["reading_note"])
            self.assertEqual(row["note"], block["note"])
        self.assertEqual([row["text"] for row in element["translations"]],
                         ["historical source words.", "study source words."])
        self.assertEqual([row["rights"] for row in element["translations"]],
                         ["public-domain", "project-created"])

    def test_inserted_element_uses_the_same_resolution_and_requires_primary(self):
        entry = deepcopy(self.entry)
        entry["after"] = "anchor"
        entry["conditions"] = [{"kind": "unappointed", "variable": "preface",
                                "basis": "Synthetic appointment evidence."}]
        section = {"key": "preface", "inserted": [entry]}
        before, after = self.tool.artifact_inserted(
            section, {"anchor"}, {}, self.absences, {}, {"preface": {}},
            "synthetic.toml", self.witnesses, {}, self.library)
        self.assertEqual(before, {})
        self.assertEqual(after["anchor"][0]["translations"], self.resolve()["translations"])
        del entry["english"]
        with self.assertRaises(self.tool.SourceError):
            self.tool.artifact_inserted(
                section, {"anchor"}, {}, self.absences, {}, {"preface": {}},
                "synthetic.toml", self.witnesses, {}, self.library)

    def test_no_alternatives_preserves_the_original_single_side_projection(self):
        entry = {key: value for key, value in self.entry.items() if key != "english_alternatives"}
        # Legacy single blocks retain their existing permissive side contract.
        entry["english"] = {key: value for key, value in entry["english"].items()
                            if key not in {"applicability", "relation"}}
        row = self.tool.side_text(entry, "en", self.witnesses, {}, self.library,
                                  "joseph", "synthetic.toml")
        self.assertEqual(self.resolve(entry)["translations"], [row])
        self.assertNotIn("applicability", row)
        self.assertEqual(row["relation"], "own")

    def test_primary_turns_do_not_get_assigned_to_a_different_source_body(self):
        entry = deepcopy(self.entry)
        entry["english_turns"] = [{"key": "prayer", "seq": [1], "speaker": "priest"}]
        rows = self.resolve(entry)["translations"]
        self.assertEqual(rows[0]["turns"][0]["text"], rows[0]["text"])
        self.assertNotIn("turns", rows[1])

    def test_coverage_counts_one_element_and_two_explicit_witness_offers(self):
        report = self.report()
        english = next(row for row in report["language_coverage"] if row["lang"] == "en")
        self.assertEqual(english, {"lang": "en", "elements": 1, "held": 1,
                                   "missing": 0, "absent": 0})
        self.assertEqual(next(row for row in report["languages"] if row["lang"] == "en")["held"], 1)
        self.assertEqual([row["held"] for row in report["translations"]], [1, 1])
        self.assertEqual(sum(row["count"] for row in report["relation_coverage"]
                             if row["lang"] == "en"), 2)
        typed = next(row for row in report["coverage"]["languages"] if row["lang"] == "en")
        self.assertEqual(typed["available"], 1)
        self.assertEqual(len(typed["witnesses"]), 2)
        self.assertEqual({relation for row in typed["witnesses"] for relation in row["relationships"]},
                         {"historical-antecedent", "study-translation"})
        self.tool._missal_coverage.validate_summary(report["coverage"])

    def test_rejects_nonarrays_nontables_and_missing_primary(self):
        for alternatives in (None, {}, [], "body", [None], [{}], ["body"]):
            with self.subTest(alternatives=alternatives), self.assertRaises(self.tool.SourceError):
                self.resolve(self.entry | {"english_alternatives": alternatives})
        for primary in (None, {}, [], "body"):
            with self.subTest(primary=primary), self.assertRaises(self.tool.SourceError):
                self.resolve(self.entry | {"english": primary})

    def test_all_candidates_require_explicit_closed_source_blocks(self):
        for index in (0, 1):
            for field in ("witness", "artifact", "element", "column", "relation", "applicability"):
                entry = deepcopy(self.entry)
                block = entry["english"] if index == 0 else entry["english_alternatives"][0]
                del block[field]
                with self.subTest(index=index, missing=field), self.assertRaises(self.tool.SourceError):
                    self.resolve(entry)
            for update in ({"text": "unbound words"}, {"english_turns": []},
                           {"elements": ["body"]}, {"witness": []}, {"artifact": ""},
                           {"note": []}, {"relation": "unreviewed"}, {"reading_note": " "}):
                entry = deepcopy(self.entry)
                block = entry["english"] if index == 0 else entry["english_alternatives"][0]
                block.update(update)
                with self.subTest(index=index, update=update), self.assertRaises(self.tool.SourceError):
                    self.resolve(entry)

    def test_rejects_unrestricted_overlapping_duplicate_and_foreign_scopes(self):
        for update in ({"formularies": ["march-19"]}, {"formularies": []},
                       {"formularies": ["may-1", "may-1"]}, {"formularies": [None]},
                       {"calendar": "postconciliar"}, {"kind": "date"},
                       {"basis": " "}, {"unknown": True}):
            entry = deepcopy(self.entry)
            entry["english_alternatives"][0]["applicability"].update(update)
            with self.subTest(update=update), self.assertRaises(self.tool.SourceError):
                self.resolve(entry)
        entry = deepcopy(self.entry)
        entry["english_alternatives"][0]["witness"] = self.blocks[0]["witness"]
        with self.assertRaisesRegex(self.tool.SourceError, "repeats an English witness"):
            self.resolve(entry)
        entry = deepcopy(self.entry)
        entry["english_alternatives"].append(deepcopy(entry["english_alternatives"][0]))
        with self.assertRaises(self.tool.SourceError):
            self.resolve(entry)

    def test_alternatives_retain_existing_rights_source_and_collation_validation(self):
        for update in ({"witness": "edition.undeclared"}, {"artifact": "artifact.undeclared"},
                       {"element": "missing"}, {"collation": "collated"},
                       {"collation": "uncollated", "collation_finding": "Unwarranted finding."}):
            entry = deepcopy(self.entry)
            entry["english_alternatives"][0].update(update)
            with self.subTest(update=update), self.assertRaises(self.tool.SourceError):
                self.resolve(entry)
        with self.assertRaisesRegex(self.tool.SourceError, "rights-restricted"):
            self.resolve(restricted={(self.blocks[1]["witness"], "en"): {}})


if __name__ == "__main__":
    unittest.main()
