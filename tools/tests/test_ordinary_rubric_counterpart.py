#!/usr/bin/env python3
"""A Missal rubric beside a lay paraphrase says it is not that English's source.

Batch B of the 2026-11-14 Ordinary integration joined the Missal's own Latin
rubric to 1861 lay-missal elements whose English paraphrases, rather than
translates, the direction at that place. `counterpart = "rubric-at-place"`
states that relation at the element; a heading whose 1861 English states a
superseded discipline may take an unpartitioned English replacement.
"""
import copy
import hashlib
import importlib.machinery
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _qualified_public_domain  # noqa: E402


def load_tool():
    loader = importlib.machinery.SourceFileLoader("ordinary_rubric_counterpart", str(ROOT / "tools/mass-ordinary"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    tool = importlib.util.module_from_spec(spec)
    loader.exec_module(tool)
    return tool


class RubricCounterpart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool()

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=ROOT / ".scratch")
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        (root / "latin.tsv").write_text("element_key\tseq\tlatin\nrubric\t1\tDeinde osculatur altare.\n")
        self.artifact = "artifact.synthetic.missal-rubric"
        self.witness = "edition.synthetic.missal"
        self.base = "edition.synthetic.lay-missal"
        self.library = {self.artifact: {"id": self.artifact, "path": "latin.tsv", "_source_root": root}}
        self.witnesses = {(self.witness, "la"): {"rights": "public-domain", "artifacts": [self.artifact]}}
        self.absences = {"lay-rubric": {"kind": "witness-gap"}}
        self.element = {
            "key": "section/rubric", "kind": "rubric", "speaker": None, "name": None,
            "conditions": [], "note": None,
            "absent": {"english": None, "latin": "lay-rubric"},
            "translations": [{"lang": "en", "source_id": self.base, "rights": "public-domain",
                              "text": "Then he kisses the Altar."}],
        }
        self.entry = {"element": "rubric", "latin": {
            "witness": self.witness, "artifact": self.artifact, "element": "rubric",
            "column": "latin", "relation": "antecedent", "collation": "collated",
            "collation_finding": "passage.synthetic.target", "target_wording": "word-exact",
            "counterpart": "rubric-at-place",
            "reading_note": "The Missal's rubric here; the English is a lay paraphrase, not its translation.",
            "note": "The Missal's own rubric at this place, not the source of the English.",
        }}

    def apply(self, entries, element=None):
        section = {"key": "section", "witness": self.base}
        section["additional_texts"] = entries
        elements = [copy.deepcopy(element or self.element)]
        self.tool.artifact_additional_texts(section, {"rubric"}, {}, elements, self.witnesses, {},
                                            self.library, self.absences, "synthetic")
        return elements[0]

    def test_counterpart_is_emitted_beside_the_untouched_lay_english(self):
        element = self.apply([self.entry])
        english, latin = element["translations"]
        self.assertEqual(english, self.element["translations"][0])
        self.assertEqual(latin["counterpart"], "rubric-at-place")
        self.assertEqual(latin["reading_note"], self.entry["latin"]["reading_note"])
        self.assertEqual(latin["coverage_relationship"], "exact-target")
        self.assertIsNone(element["absent"]["latin"])

    def test_absent_counterpart_makes_no_claim(self):
        block = {k: v for k, v in self.entry["latin"].items() if k != "counterpart"}
        latin = self.apply([{"element": "rubric", "latin": block}])["translations"][1]
        self.assertNotIn("counterpart", latin)

    def test_refused_without_its_conditions(self):
        no_note = {k: v for k, v in self.entry["latin"].items() if k != "reading_note"}
        cases = [
            ([{"element": "rubric", "latin": no_note}], None),
            ([{"element": "rubric", "latin": self.entry["latin"] | {"counterpart": "translation"}}], None),
            ([self.entry], self.element | {"kind": "prayer"}),
            ([self.entry], self.element | {"translations": [
                self.element["translations"][0] | {"source_id": "edition.synthetic.replacement"}]}),
            ([self.entry], self.element | {"translations": []}),
        ]
        for entries, element in cases:
            with self.subTest(entries=entries, element=element), self.assertRaises(self.tool.SourceError):
                if element is not None and element["kind"] == "prayer":
                    entries = [entries[0] | {"turns_basis": "Synthetic.",
                                             "latin_turns": [{"key": "one", "seq": [1]}]}]
                self.apply(entries, element)

    def test_only_an_additional_side_may_declare_it(self):
        with self.assertRaisesRegex(self.tool.SourceError, "outside an additional_texts side"):
            self.tool.side_text({"latin": self.entry["latin"]}, "la", self.witnesses, {},
                                self.library, "section/rubric", "synthetic")


class UnspokenEnglishReplacement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool()

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=ROOT / ".scratch")
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        (root / "old.tsv").write_text(
            "element_key\tseq\tkind\tenglish\tlatin_incipit\tprinted_page\tspeaker\n"
            "heading\t1\theading\tOn every Sunday in the Year.\t\t1\t\n"
            "other\t2\trubric\tHe bows.\t\t1\t\n")
        (root / "latin.tsv").write_text("element_key\tlatin\nother\tInclinat se.\n")
        (root / "new.tsv").write_text("element_key\tseq\tenglish\nstudy\t1\tTHE PREFACE\nstudy\t2\tSaid on Sundays of the second class.\n")
        self.library = {}
        for name in ("old", "latin", "new"):
            identifier = "artifact.synthetic." + name
            self.library[identifier] = {"id": identifier, "path": name + ".tsv", "_source_root": root,
                                        "rights_status": "public-domain"}
        self.witnesses = {
            ("edition.synthetic.old", "en"): {"lang": "en", "rights": "public-domain",
                                              "artifacts": ["artifact.synthetic.old"]},
            ("edition.synthetic.old", "la"): {"lang": "la", "rights": "public-domain",
                                              "artifacts": ["artifact.synthetic.latin"]},
            ("edition.synthetic.study", "en"): {"lang": "en", "rights": "project-created",
                                                "artifacts": ["artifact.synthetic.new"]},
        }
        provenance = {"relation": "antecedent", "collation": "uncollated", "note": "Old lay English."}
        self.section = {"key": "synthetic", "witness": "edition.synthetic.old",
                        "artifact": "artifact.synthetic.old", "artifact_latin": "artifact.synthetic.latin",
                        "absent_latin": "gap", "english": provenance, "latin": provenance}
        self.entry = {
            "element": "heading",
            "replaces": {"witness": "edition.synthetic.old", "artifact": "artifact.synthetic.old",
                         "text_sha256": hashlib.sha256(b"On every Sunday in the Year.").hexdigest()},
            "english": {"witness": "edition.synthetic.study", "artifact": "artifact.synthetic.new",
                        "element": "study", "column": "english", "relation": "own",
                        "reading_note": "Study translation of the target heading."},
        }

    def build(self, section):
        return self.tool.from_artifact(section, self.witnesses, {}, {"gap": {"kind": "witness-gap"}},
                                       self.library, "synthetic.toml")

    def test_heading_takes_an_unpartitioned_replacement(self):
        element = self.build(self.section | {"english_replacements": [self.entry]})[0][0]
        english = element["translations"][0]
        self.assertEqual(english["source_id"], "edition.synthetic.study")
        self.assertEqual(english["text"], "THE PREFACE\nSaid on Sundays of the second class.")
        self.assertNotIn("turns", english)
        self.assertEqual(english["relation"], "own")

    def test_heading_replacement_refuses_turns_and_stale_bodies(self):
        cases = [
            self.entry | {"english_turns": [{"key": "one", "seq": [1]}]},
            self.entry | {"turns_basis": "Not applicable."},
            self.entry | {"replaces": self.entry["replaces"] | {"text_sha256": "0" * 64}},
        ]
        for entry in cases:
            with self.subTest(entry=entry), self.assertRaises(self.tool.SourceError):
                self.build(self.section | {"english_replacements": [entry]})


class TerminalNotice(unittest.TestCase):
    """The terminal readers print a witness's notice beside its words, as the browser does."""

    def test_notice_follows_the_words_of_its_witness_only(self):
        from _ordinary_text import element_lines, witness_notices
        from _tooling import Style
        ordinary = {"translations": [
            {"lang": "la", "source_id": "edition.synthetic.qualified", "acknowledgement": "Qualified notice."},
            {"lang": "la", "source_id": "edition.synthetic.plain", "acknowledgement": None},
        ]}
        notices = witness_notices(ordinary)
        style = Style("plain")
        for kind in ("rubric", "heading"):
            element = {"key": "s/e", "kind": kind, "translations": [
                {"lang": "la", "source_id": "edition.synthetic.qualified", "text": "Tunc celebrans."}]}
            with self.subTest(kind=kind):
                lines = "\n".join(element_lines(element, "la", style, notices=notices))
                self.assertIn("Notice: Qualified notice.", lines)
                self.assertNotIn("Notice:", "\n".join(element_lines(element, "la", style)))
        plain = {"key": "s/p", "kind": "rubric", "translations": [
            {"lang": "la", "source_id": "edition.synthetic.plain", "text": "Deinde."}]}
        self.assertNotIn("Notice:", "\n".join(element_lines(plain, "la", style, notices=notices)))

    def test_a_head_printed_with_its_rubric_rules_only_the_title(self):
        """The 1962 Preface titles carry their rubric on a second line."""
        from _ordinary_text import element_lines
        from _tooling import Style
        style = Style("plain")
        element = {"key": "praefatio/h", "kind": "heading", "translations": [
            {"lang": "la", "source_id": "edition.synthetic.missal",
             "text": "PRAEFATIO COMMUNIS\nSequens praefatio dicitur in Missis."}]}
        lines = element_lines(element, "la", style)
        title = lines.index("  PRAEFATIO COMMUNIS")
        self.assertEqual("  " + "-" * len("PRAEFATIO COMMUNIS"), lines[title + 1])
        self.assertEqual("    [ Sequens praefatio dicitur in Missis. ]", lines[title + 2])
        hidden = element_lines(element, "la", style, show_rubrics=False)
        self.assertIn("  PRAEFATIO COMMUNIS", hidden)
        self.assertFalse(any("Sequens" in line for line in hidden))
        browser = (ROOT / "src/web/browser/liturgy/day.js").read_text(encoding="utf-8")
        self.assertIn("'composed ordinary-head-rubric'", browser)


class InstalledOrdinary(unittest.TestCase):
    """The installed inventories keep each claim at its element."""

    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool()
        library = cls.tool.artifact_records(ROOT / "src/sources")
        sources = ROOT / "src/sources"
        cls.roman = cls.tool.calendar_structure(
            sources, sources / "inventories/roman-1962-ordo-missae-v1.toml", library)
        cls.modern = cls.tool.calendar_structure(
            sources, sources / "inventories/postconciliar-ordo-missae-v1.toml", library)

    @staticmethod
    def element(structure, key):
        return next(one for section in structure["sections"] for one in section["elements"]
                    if one["key"] == key)

    @staticmethod
    def side(element, lang):
        return next(row for row in element["translations"] if row["lang"] == lang)

    def test_missal_rubric_beside_lay_english_is_labelled(self):
        element = self.element(self.roman, "oblatio/rubrica-lavabo")
        latin = self.side(element, "la")
        self.assertEqual(latin["counterpart"], "rubric-at-place")
        self.assertIn("not a translation", latin["reading_note"])
        self.assertEqual(self.side(element, "en")["source_id"],
                         "edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861")
        heading = self.side(self.element(self.roman, "canon/canon-heading"), "la")
        self.assertNotIn("counterpart", heading)

    def test_qualified_latin_and_study_english_carry_their_notices(self):
        witnesses = {(row["lang"], row["source_id"]): row for row in self.roman["translations"]}
        heading = self.element(self.roman, "praefatio/praefatio-de-nativitate-heading")
        latin, english = self.side(heading, "la"), self.side(heading, "en")
        self.assertEqual(latin["rights"], "qualified-public-domain")
        self.assertEqual(witnesses[("la", latin["source_id"])]["acknowledgement"],
                         _qualified_public_domain.notice("latin"))
        self.assertEqual(english["rights"], "project-created")
        self.assertEqual(witnesses[("en", english["source_id"])]["acknowledgement"],
                         _qualified_public_domain.notice("english_study"))
        self.assertTrue(english["text"].startswith("THE PREFACE OF THE NATIVITY OF THE LORD"))

    def test_lay_apparatus_and_requiem_rubric_keep_their_respective_sources(self):
        absences = {row["key"]: row for row in self.roman["absences"]}
        self.assertEqual(absences["lay-apparatus-no-missal-counterpart"]["kind"], "not-applicable")
        self.assertEqual(absences["lay-apparatus-no-missal-counterpart"]["count"], 13)
        element = self.element(self.roman, "communio/rubrica-oratio-omittenda")
        self.assertIsNone(element["absent"]["latin"])
        self.assertIn("præcedens Oratio", self.side(element, "la")["text"])
        self.assertIn("following", self.side(element, "en")["text"])
        self.assertIn("preceding prayer", self.side(element, "la")["reading_note"])

    def test_postconciliar_paschal_dismissal_is_carried_without_the_2008_option(self):
        element = self.element(self.modern, "ritus-conclusionis/dimissio-appointed")
        latin, english = self.side(element, "la"), self.side(element, "en")
        self.assertEqual(latin["text"], "Ite missa est, allelúja, allelúja.\nR. Deo grátias, allelúja, allelúja.")
        self.assertEqual(latin["target_wording"], "word-exact")
        self.assertEqual(english["text"],
                         "Go, the Mass is ended. Alleluia, alleluia.\nR. Thanks be to God. Alleluia, alleluia.")
        self.assertEqual([turn["speaker"] for turn in english["turns"]], ["deacon-or-priest", "all"])


if __name__ == "__main__":
    unittest.main()
