"""A complete English witness replaces an exact body, never the Mass frame."""
from copy import deepcopy
import hashlib
import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class EnglishReplacementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader(
            "mass_ordinary_english_replacements", str(ROOT / "tools/mass-ordinary"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.tool = importlib.util.module_from_spec(spec)
        loader.exec_module(cls.tool)

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        self.payloads = {
            "old.tsv": ("element_key\tseq\tkind\tenglish\tlatin_incipit\tprinted_page\tspeaker\n"
                        "call\t1\tdialogue\tP. Old call, &c.\tInvocatio\t1\tpriest\n"
                        "call\t2\tdialogue\tR. Old answer.\tInvocatio\t1\tserver\n"
                        "rubric\t3\trubric\tThe old witness's instruction.\t\t1\t\n"),
            "latin.tsv": "element_key\tlatin\ncall\tLatina integra.\n",
            "new.tsv": ("element_key\tseq\tenglish\n"
                        "complete\t10\tP. Complete new call.\n"
                        "complete\t20\tR. Complete new answer.\n"),
        }
        self.library = {}
        for filename, content in self.payloads.items():
            (root / filename).write_text(content, encoding="utf-8")
            identifier = "artifact.synthetic." + filename.split(".")[0]
            self.library[identifier] = {
                "id": identifier, "path": filename, "_source_root": root,
                "rights_status": "public-domain",
            }
        self.witnesses = {
            ("edition.synthetic.old", "en"): {"lang": "en", "rights": "public-domain",
                "artifacts": ["artifact.synthetic.old"]},
            ("edition.synthetic.old", "la"): {"lang": "la", "rights": "public-domain",
                "artifacts": ["artifact.synthetic.latin"]},
            ("edition.synthetic.new", "en"): {"lang": "en", "rights": "public-domain",
                "artifacts": ["artifact.synthetic.new"]},
        }
        self.absences = {"gap": {"kind": "witness-gap", "label": "No facing column."}}
        self.provenance = {"relation": "antecedent", "collation": "uncollated",
                           "note": "The identified witness's words, not target-edition English."}
        self.section = {
            "key": "synthetic", "witness": "edition.synthetic.old",
            "artifact": "artifact.synthetic.old", "artifact_latin": "artifact.synthetic.latin",
            "absent_latin": "gap", "english": self.provenance, "latin": self.provenance,
            "turn_partitions": [{"element": "call", "lang": "en", "basis": "Old source marks.",
                "parts": [{"key": "old-call", "seq": [1], "speaker": "priest", "printed_marker": "P."},
                          {"key": "old-answer", "seq": [2], "speaker": "server", "printed_marker": "R."}]}],
        }
        self.entry = {
            "element": "call", "replaces": {
                "witness": "edition.synthetic.old", "artifact": "artifact.synthetic.old",
                "text_sha256": hashlib.sha256(b"P. Old call, &c.\nR. Old answer.").hexdigest()},
            "english": {"witness": "edition.synthetic.new", "artifact": "artifact.synthetic.new",
                        "element": "complete", "column": "english", **self.provenance},
            "english_turns": [
                {"key": "new-call", "seq": [10], "speaker": "priest", "printed_marker": "P."},
                {"key": "new-answer", "seq": [20], "speaker": "server", "printed_marker": "R."}],
            "turns_basis": "The new witness's own two marked source rows.",
        }

    def build(self, section=None, restricted=None):
        return self.tool.from_artifact(section or self.section, self.witnesses,
            restricted or {}, self.absences, self.library, "synthetic.toml")

    def test_replaces_only_the_exact_english_body_and_preserves_source_artifacts(self):
        before, exclusions = self.build()
        after, new_exclusions = self.build(self.section | {"english_replacements": [self.entry]})
        old = deepcopy(before)
        expected = self.tool.side_text(self.entry, "en", self.witnesses, {}, self.library,
                                      "synthetic/call", "synthetic.toml")
        old[0]["translations"][0] = expected
        self.assertEqual(after, old)
        self.assertEqual(new_exclusions, exclusions)
        self.assertEqual(after[0]["translations"][0]["text"],
                         "P. Complete new call.\nR. Complete new answer.")
        self.assertEqual(after[0]["translations"][0]["turns"][1]["speaker"], "server")
        self.assertEqual(after[0]["translations"][1], before[0]["translations"][1])
        for record in self.library.values():
            self.assertEqual((record["_source_root"] / record["path"]).read_text(),
                             self.payloads[record["path"]])

    def test_rejects_wrong_old_identity_hash_target_and_open_fields(self):
        changes = [
            self.entry | {"replaces": self.entry["replaces"] | {"witness": "edition.other"}},
            self.entry | {"replaces": self.entry["replaces"] | {"artifact": "artifact.other"}},
            self.entry | {"replaces": self.entry["replaces"] | {"text_sha256": "0" * 64}},
            self.entry | {"replaces": self.entry["replaces"] | {"text_sha256": "not-a-hash"}},
            self.entry | {"replaces": self.entry["replaces"] | {"fallback": True}},
            self.entry | {"element": "not-in-frame"},
            self.entry | {"element": "rubric"},
            self.entry | {"latin": self.entry["english"]},
            self.entry | {"english": self.entry["english"] | {"words": "Invented"}},
        ]
        for entry in changes:
            with self.subTest(entry=entry), self.assertRaises(self.tool.SourceError):
                self.build(self.section | {"english_replacements": [entry]})
        for entries in ([], [self.entry, self.entry]):
            with self.subTest(entries=entries), self.assertRaises(self.tool.SourceError):
                self.build(self.section | {"english_replacements": entries})

    def test_rejects_missing_or_restricted_witness_and_nonexact_turn_partition(self):
        changes = [
            self.entry | {"english": self.entry["english"] | {"witness": "edition.undeclared"}},
            self.entry | {"english": self.entry["english"] | {"artifact": "artifact.unlisted"}},
            self.entry | {"english_turns": []},
            self.entry | {"english_turns": [self.entry["english_turns"][0]]},
            self.entry | {"english_turns": list(reversed(self.entry["english_turns"]))},
            self.entry | {"turns_basis": ""},
        ]
        for entry in changes:
            with self.subTest(entry=entry), self.assertRaises(self.tool.SourceError):
                self.build(self.section | {"english_replacements": [entry]})
        with self.assertRaisesRegex(self.tool.SourceError, "rights-restricted"):
            self.build(self.section | {"english_replacements": [self.entry]},
                       {("edition.synthetic.new", "en"): {}})

    def test_new_body_must_obey_existing_conditional_phrase_contract(self):
        # The source-owned guard is checked on the newly selected English;
        # retaining a stale conditional marker from the old witness must fail.
        section = self.section | {"english_replacements": [self.entry],
            "conditional_spans": [{"element": "call", "lang": "en", "text": "Old call",
                "said": {"anchor": "pentecost", "from": -1, "to": 6},
                "rubric": "Said in this source window.", "locus": "Source locus."}]}
        with self.assertRaisesRegex(self.tool.SourceError, "exactly once"):
            self.build(section)
        section["conditional_spans"][0]["text"] = "Complete new call."
        result, _ = self.build(section)
        self.assertEqual(result[0]["translations"][0]["conditional_spans"][0]["text"],
                         "Complete new call.")

    def test_old_english_provenance_cannot_overwrite_new_witness_qualification(self):
        section = self.section | {"english_replacements": [self.entry],
            "element_provenance": [{"element": "call", "lang": "en", **self.provenance}]}
        with self.assertRaisesRegex(self.tool.SourceError, "cannot inherit English provenance"):
            self.build(section)

    def test_junction_replacement_binds_the_existing_prefix_not_the_discarded_tail(self):
        root = self.library["artifact.synthetic.old"]["_source_root"]
        (root / "old.tsv").write_text(
            "element_key\tseq\tkind\tenglish\tlatin_incipit\tprinted_page\tspeaker\n"
            "call\t1\tprayer\tOld head: Old continuation.\tInitium\t1\tpriest\n")
        (root / "latin.tsv").write_text(
            "element_key\tlatin\ncall\tInitium: Continuatio.\n")
        section = {key: value for key, value in self.section.items() if key != "turn_partitions"}
        section["junctions"] = [{"element": "call", "through": {
            "en": "Old head:", "la": "Initium:"}, "basis": "Exact target junction."}]
        entry = deepcopy(self.entry)
        entry["replaces"]["text_sha256"] = hashlib.sha256(b"Old head:").hexdigest()
        before, _ = self.build(section)
        after, _ = self.build(section | {"english_replacements": [entry]})
        self.assertEqual(after[0]["translations"][1], before[0]["translations"][1])
        self.assertEqual(after[0]["junction"], before[0]["junction"])
        self.assertEqual(after[0]["translations"][1]["text"], "Initium:")
        entry["replaces"]["text_sha256"] = hashlib.sha256(
            b"Old head: Old continuation.").hexdigest()
        with self.assertRaisesRegex(self.tool.SourceError, "exact existing English body"):
            self.build(section | {"english_replacements": [entry]})

    def test_inserted_text_from_another_artifact_cannot_claim_the_base_artifact(self):
        elements, _ = self.build()
        inserted = deepcopy(elements[0])
        inserted["key"] = "synthetic/inserted"
        entry = deepcopy(self.entry)
        entry["element"] = "inserted"
        with self.assertRaisesRegex(self.tool.SourceError, "not backed by the base English artifact"):
            self.tool.artifact_english_replacements(
                self.section | {"english_replacements": [entry]}, {"call", "rubric"},
                [*elements, inserted], self.witnesses, {}, self.library, "synthetic.toml")

    def test_a_spoken_body_cannot_be_replaced_entirely_by_glosses_or_actions(self):
        root = self.library["artifact.synthetic.new"]["_source_root"]
        (root / "new.tsv").write_text(
            "element_key\tseq\tenglish\ncomplete\t10\tSource note.\n"
            "complete\t20\tComplete spoken prayer.\n")
        for nonspoken in ("gloss", "action"):
            entry = deepcopy(self.entry)
            entry["english_turns"] = [{"key": "nonspoken", "seq": [10, 20], nonspoken: True}]
            with self.subTest(nonspoken=nonspoken), self.assertRaisesRegex(
                    self.tool.SourceError, "at least one spoken source turn"):
                self.build(self.section | {"english_replacements": [entry]})
        entry["english_turns"] = [
            {"key": "source-note", "seq": [10], "gloss": True},
            {"key": "prayer", "seq": [20], "speaker": "priest"}]
        result, _ = self.build(self.section | {"english_replacements": [entry]})
        turns = result[0]["translations"][0]["turns"]
        self.assertTrue(turns[0]["gloss"])
        self.assertEqual(turns[1]["text"], "Complete spoken prayer.")


if __name__ == "__main__":
    unittest.main()
