#!/usr/bin/env python3
"""The checked internal-structure contract for Proper bodies (C2 gap G14).

`text_structure` records stanza boundaries and typed inline actions as offsets
into an exact, hash-pinned text, beside the text and never inside it. These
tests hold the validator to its refusals, the public projection to the
browser's own string units, and the 1962 Pentecost exemplar to what its page
images showed: a Sequence printed in strophes and a genuflection direction
printed inside the Alleluia.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tomllib
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
STRUCTURE = ROOT / "src/web/data/structure/propers/roman-1962.json"
CALENDAR = ROOT / "src/sources/calendars/roman-1962/propers.yaml"
OVERLAY = ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml"


def load(name: str, tool: str):
    loader = SourceFileLoader(name, str(ROOT / "tools" / tool))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


PROPERS = load("text_structure_mass_propers", "mass-propers")
CHECKER = load("text_structure_checker", "check-calendar-masses")

# Synthetic, non-liturgical fixture: three sentences, the second a stanza of
# its own and the third holding a parenthesised direction.
TEXT = "Alpha beta gamma.\nDelta epsilon. Zeta (do this) eta theta."


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def valid() -> dict:
    return {
        "text_sha256": sha(TEXT),
        "checked": "Read on a page image.",
        "stanzas": [
            {"offset": 0, "opens": "Alpha beta"},
            {"offset": TEXT.index("Delta"), "opens": "Delta"},
            {"offset": TEXT.index("Zeta"), "opens": "Zeta"},
        ],
        "actions": [
            {"kind": "rubric", "offset": TEXT.index("(do"), "text": "(do this)"},
        ],
    }


class ValidatorTests(unittest.TestCase):
    def problems(self, structure, text=TEXT, lines=None):
        return PROPERS.text_structure_problems(text, structure, lines)

    def test_a_checked_structure_passes(self) -> None:
        self.assertEqual(self.problems(valid()), [])

    def test_a_changed_text_cannot_keep_its_structure(self) -> None:
        found = self.problems(valid(), TEXT.replace("eta", "iota"))
        self.assertTrue(any("text_sha256" in problem for problem in found), found)

    def test_boundaries_fall_at_words_and_name_the_words_they_open(self) -> None:
        held = valid()
        held["stanzas"][1] = {"offset": TEXT.index("Delta") + 1, "opens": "elta"}
        self.assertTrue(any("start of a word" in p for p in self.problems(held)))
        held = valid()
        held["stanzas"][1]["opens"] = "Epsilon"
        self.assertTrue(any(".opens" in p for p in self.problems(held)))
        held = valid()
        held["stanzas"][0]["offset"] = 6
        self.assertTrue(any("must be 0" in p for p in self.problems(held)))

    def test_actions_are_typed_exact_and_inside_one_stanza(self) -> None:
        held = valid()
        held["actions"][0]["kind"] = "spoken"
        self.assertTrue(any(".kind" in p for p in self.problems(held)))
        held = valid()
        held["actions"][0]["text"] = "(do that)"
        self.assertTrue(any("own span" in p for p in self.problems(held)))
        held = valid()
        held["actions"] = [{"kind": "rubric", "offset": TEXT.index("epsilon"), "text": "epsilon. Zeta"}]
        self.assertTrue(any("straddles" in p for p in self.problems(held)))

    def test_unknown_fields_and_an_empty_record_are_refused(self) -> None:
        held = valid()
        held["lines"] = []
        self.assertTrue(any("unknown" in p for p in self.problems(held)))
        self.assertTrue(any("neither" in p for p in self.problems(
            {"text_sha256": sha(TEXT), "checked": "x"})))
        self.assertTrue(self.problems(valid(), None))

    def test_witness_lines_need_a_witness_and_stay_inside_it(self) -> None:
        held = valid()
        held["stanzas"][0]["witness_line"] = 3
        self.assertTrue(any("needs a witness_artifact_id" in p for p in self.problems(held)))
        held = valid()
        held["witness_artifact_id"] = "artifact.example"
        for index, stanza in enumerate(held["stanzas"]):
            stanza["witness_line"] = 10 + index
        self.assertEqual(self.problems(held, lines=lambda _: 20), [])
        self.assertTrue(any("past the witness" in p for p in self.problems(held, lines=lambda _: 11)))
        self.assertTrue(any("not registered" in p for p in self.problems(
            held, lines=lambda _: "not registered")))
        held["stanzas"][2]["witness_line"] = 9
        self.assertTrue(any("backwards" in p for p in self.problems(held, lines=lambda _: 20)))


class ProjectionTests(unittest.TestCase):
    def test_public_offsets_are_the_browsers_string_units(self) -> None:
        text = "\U0001d504 alpha (beta) gamma.\n\nDelta."
        structure = {
            "text_sha256": sha(text), "checked": "x",
            "stanzas": [{"offset": 0, "opens": "\U0001d504"}, {"offset": text.index("Delta"), "opens": "Delta."}],
            "actions": [{"kind": "rubric", "offset": text.index("("), "text": "(beta)"}],
        }
        projected = PROPERS.public_text_structure(text, structure)
        utf16 = lambda i: len(text[:i].encode("utf-16-le")) // 2
        self.assertEqual(projected["stanzas"], [0, utf16(text.index("Delta"))])
        self.assertEqual(projected["actions"], [{
            "kind": "rubric", "start": utf16(text.index("(")), "end": utf16(text.index(")") + 1)}])
        self.assertNotIn("checked", projected)

    def test_a_broken_structure_fails_the_build_rather_than_vanishing(self) -> None:
        with self.assertRaises(ValueError):
            PROPERS.public_text_structure(TEXT.upper(), valid())


class CheckerWiringTests(unittest.TestCase):
    def test_the_calendar_gate_refuses_a_broken_proper_structure(self) -> None:
        proper = {"name": "Sequence", "source": "composed", "text": TEXT, "text_structure": valid()}
        problems: list[str] = []
        CHECKER.check_proper("fixture", proper, problems)
        self.assertEqual(problems, [])
        proper["text_structure"] = dict(valid(), text_sha256="0" * 64)
        CHECKER.check_proper("fixture", proper, problems)
        self.assertTrue(any("text_sha256" in problem for problem in problems), problems)

    def test_a_reference_carries_no_structure_of_its_own(self) -> None:
        problems: list[str] = []
        CHECKER.check_proper("fixture", {
            "name": "Sequence", "takes_from": {"mass": "elsewhere"}, "text_structure": valid(),
        }, problems)
        self.assertTrue(any("text_structure" in problem for problem in problems), problems)

    def test_the_gate_refuses_a_broken_translation_structure(self) -> None:
        problems: list[str] = []
        CHECKER.check_translation_list("fixture", [{
            "lang": "en", "rights": "project-created", "text": TEXT,
            "text_structure": dict(valid(), checked=""),
        }], problems)
        self.assertTrue(any("checked" in problem for problem in problems), problems)


class PentecostExemplarTests(unittest.TestCase):
    """The 1962 C2 exemplar, read from the tracked sources and generated file."""

    @classmethod
    def setUpClass(cls) -> None:
        document = yaml.safe_load(CALENDAR.read_text(encoding="utf-8"))
        cls.source = next(
            mass for section in document["sections"].values()
            for mass in section["masses"] if mass["key"] == "pentecost")
        cls.served = next(
            mass for mass in json.loads(STRUCTURE.read_text(encoding="utf-8"))["masses"]
            if mass["key"] == "pentecost")
        cls.overlay = tomllib.loads(OVERLAY.read_text(encoding="utf-8"))

    def proper(self, mass, name):
        return next(row for row in mass["propers"] if row["name"] == name)

    def test_published_words_are_unchanged_by_their_structure(self) -> None:
        for name in ("Alleluia", "Sequence"):
            source = self.proper(self.source, name)
            served = self.proper(self.served, name)
            self.assertEqual(served["text"], source["text"])
            self.assertEqual(served["text_structure"], PROPERS.public_text_structure(
                source["text"], source["text_structure"]))

    def test_the_sequence_is_served_in_its_checked_strophes(self) -> None:
        source = self.proper(self.source, "Sequence")["text_structure"]
        served = self.proper(self.served, "Sequence")["text_structure"]
        # Ten strophes and the closing Alleluia line, each tied to the Pustet
        # text-layer line where it begins, and checked on the 1962 page.
        self.assertEqual(len(served["stanzas"]), 11)
        self.assertNotIn("actions", served)
        self.assertEqual(CHECKER.witness_line_count(source["witness_artifact_id"]) >= max(
            row["witness_line"] for row in source["stanzas"]), True)
        self.assertIn("artifact p. 438", source["checked"])

    def test_the_genuflection_is_one_rubric_in_both_languages(self) -> None:
        served = self.proper(self.served, "Alleluia")
        text = served["text"]
        (action,) = served["text_structure"]["actions"]
        self.assertEqual(action["kind"], "rubric")
        self.assertTrue(text[action["start"]:action["end"]].startswith("("))
        (english,) = [row for row in served["translations"] if row["lang"] == "en"]
        (rubric,) = english["text_structure"]["actions"]
        span = english["text"][rubric["start"]:rubric["end"]]
        self.assertTrue(span.startswith("(") and span.endswith(")"), span)
        coverage = {row["lang"]: row for row in served["coverage"]["languages"]}
        self.assertEqual(coverage["en"]["availability"], "available")

    def test_the_alleluia_english_is_bound_on_its_page_and_no_gap_remains(self) -> None:
        entries = [row for row in self.overlay["entries"]
                   if row.get("mass") == "pentecost" and row.get("proper") == "Alleluia"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["passage_id"],
                         "passage.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.whitsunday-alleluia")
        self.assertEqual(entries[0]["printed_page"], "599")
        self.assertFalse([row for row in self.overlay["untranslated"]
                          if row.get("mass") == "pentecost" and row.get("proper") == "Alleluia"])

    def test_the_reading_view_sets_the_same_stanzas(self) -> None:
        source = self.proper(self.source, "Sequence")
        paragraphs = PROPERS.stanza_paragraphs(source["text"], source).split("\n\n")
        self.assertEqual(len(paragraphs), len(source["text_structure"]["stanzas"]))
        self.assertEqual(" ".join(paragraphs), " ".join(source["text"].split()))
        # Words with no structure recorded against them are left as they are.
        self.assertEqual(PROPERS.stanza_paragraphs(TEXT, source), TEXT)

    def test_the_english_sequence_keeps_its_ten_checked_stanzas(self) -> None:
        sequence = self.proper(self.served, "Sequence")
        english = [row for row in sequence["translations"] if row["lang"] == "en"]
        self.assertEqual(len(english), 2)  # the edition and its tracked artifact: one witness
        self.assertEqual({len(row["text_structure"]["stanzas"]) for row in english}, {10})


if __name__ == "__main__":
    unittest.main()
