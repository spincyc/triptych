"""Source qualifications accompany held Ordinary words in the default CLI."""
from __future__ import annotations

from copy import deepcopy
import importlib.machinery
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from _ordinary_text import element_lines  # noqa: E402
from _tooling import Style  # noqa: E402


class OrdinaryTextQualification(unittest.TestCase):
    WORDS = "Preserve these source words exactly."
    NOTE = "HISTORICAL ENGLISH ANTECEDENT; target English remains uncollated."
    FULL_NOTE = "Full source apparatus and its detailed collation evidence."

    def element(self, kind="prayer", **translation):
        return {"kind": kind, "name": "An Ordinary element", "locus": "n. 1",
                "translations": [{"lang": "en", "text": self.WORDS,
                                  "reading_note": self.NOTE, "note": self.FULL_NOTE,
                                  **translation}]}

    def render(self, element=None, *, tier="unicode", lang="en", **options):
        return "\n".join(element_lines(element or self.element(), lang,
                                      Style(tier), **options))

    def test_default_reading_qualifies_the_words_before_they_are_printed(self):
        shown = self.render()
        self.assertIn(f"[ Source note: {self.NOTE} ]", " ".join(shown.split()))
        self.assertIn(self.WORDS, shown)
        self.assertLess(shown.index("[ Source note:"), shown.index(self.WORDS))
        self.assertNotIn(self.FULL_NOTE, shown)
        self.assertNotIn("[n. 1]", shown)

    def test_full_source_apparatus_is_available_only_when_requested(self):
        shown = self.render(why=True)
        self.assertIn(f"[ Source note: {self.FULL_NOTE} ]", " ".join(shown.split()))
        self.assertIn("[n. 1]", shown)
        self.assertIn(self.WORDS, shown)
        self.assertNotIn(self.NOTE, " ".join(shown.split()))
        without_full_note = self.render(self.element(note=None), why=True)
        self.assertIn(self.NOTE, " ".join(without_full_note.split()))

    def test_headings_retain_their_source_note_without_verbose_loci(self):
        shown = self.render(self.element("heading"))
        self.assertIn(self.WORDS, shown)
        self.assertIn(f"[ Source note: {self.NOTE} ]", " ".join(shown.split()))
        self.assertNotIn("[n. 1]", shown)

    def test_note_is_not_formatted_as_spoken_dialogue(self):
        element = self.element(reading_note="V. A source annotation. R. A qualification.")
        shown = self.render(element)
        self.assertIn("[ Source note: V. A source annotation. R. A qualification. ]", shown)
        self.assertNotIn("℣", shown)
        self.assertNotIn("℟", shown)

    def test_structured_dialogue_and_hidden_actions_keep_the_qualification(self):
        turns = [{"speaker": "priest", "dialogue_role": "versicle",
                  "printed_marker": "P.", "text": "P. Printed call."},
                 {"action": True, "text": "Printed action."},
                 {"speaker": "server", "dialogue_role": "response",
                  "printed_marker": "R.", "text": "R. Printed answer."},
                 {"gloss": True, "text": "Printed gloss."}]
        element = self.element("dialogue", turns=turns,
                               text="\n".join(turn["text"] for turn in turns))
        for rubrics in (True, False):
            with self.subTest(show_rubrics=rubrics):
                shown = self.render(element, show_rubrics=rubrics)
                self.assertIn("[ Source note:", shown)
                self.assertIn("℣ — Priest: Printed call.", shown)
                self.assertIn("℟ — Server: Printed answer.", shown)
                self.assertIn("[ Source translation: Printed gloss. ]", shown)
                self.assertEqual("[ Printed action. ]" in shown, rubrics)
                self.assertLess(shown.index("[ Source note:"), shown.index("Printed call."))

    def test_outside_applicability_neither_source_note_nor_words_are_executed(self):
        scope = {"kind": "formulary", "calendar": "roman-1962",
                 "formularies": ["easter-sunday"], "basis": "A checked source direction."}
        for kind in ("prayer", "heading"):
            element = self.element(kind, applicability=scope)
            for context in (None, {"calendar": "roman-1962", "formulary": "easter-vigil"}):
                with self.subTest(kind=kind, context=context):
                    shown = self.render(element, context=context)
                    self.assertIn("applicability", shown)
                    self.assertNotIn(self.WORDS, shown)
                    self.assertNotIn(self.NOTE, shown)
                    self.assertNotIn("[ Source note:", shown)
                    self.assertNotIn(self.FULL_NOTE, self.render(element, why=True,
                                                                context=context))
            shown = self.render(element, context={"calendar": "roman-1962",
                                                 "formulary": "easter-sunday"})
            self.assertIn(self.WORDS, shown)
            self.assertIn("[ Source note:", shown)

    def test_only_the_selected_languages_note_is_printed(self):
        element = self.element()
        element["translations"].append({"lang": "la", "text": "Other-language words.",
                                        "reading_note": "Other-language source qualification."})
        english = self.render(element)
        latin = self.render(element, lang="la")
        self.assertIn(self.NOTE, " ".join(english.split()))
        self.assertNotIn("Other-language", english)
        self.assertIn("Other-language source qualification.", latin)
        self.assertNotIn(self.NOTE, " ".join(latin.split()))

    def test_plain_tier_folds_source_notes_and_retains_nonspoken_brackets(self):
        shown = self.render(self.element(reading_note="A witness’s note — æ, ℣ and ©."), tier="plain")
        self.assertTrue(shown.isascii(), shown)
        self.assertIn("[ Source note: A witness's note -- ae, V. and (c). ]", shown)
        self.assertIn(self.WORDS, shown)

    def test_no_note_is_invented_and_hidden_rubrics_stay_hidden(self):
        for note in (None, "", " \n "):
            with self.subTest(note=note):
                shown = self.render(self.element(reading_note=note))
                self.assertIn(self.WORDS, shown)
                self.assertNotIn("[ Source note:", shown)
                self.assertNotIn(self.FULL_NOTE, shown)
        self.assertEqual(self.render(self.element("rubric"), show_rubrics=False), "")


class ScopedOrdinaryTranslations(unittest.TestCase):
    MARCH = "s-ioseph-sponsi-beatae-mariae-virginis"
    MAY = "s-ioseph-opificis-sponsi-beatae-mariae"

    def pair(self):
        def translation(formulary, label):
            turns = [{"speaker": "priest", "dialogue_role": "versicle",
                      "printed_marker": "P.", "text": f"P. {label} source call."},
                     {"speaker": "server", "dialogue_role": "response",
                      "printed_marker": "R.", "text": f"R. {label} source answer."}]
            return {"lang": "en", "source_id": f"edition.synthetic.{label.lower()}",
                    "text": "\n".join(turn["text"] for turn in turns), "turns": turns,
                    "reading_note": f"{label} source qualification.",
                    "note": f"{label} full source evidence.",
                    "applicability": {"kind": "formulary", "calendar": "roman-1962",
                                      "formularies": [formulary],
                                      "basis": f"Checked {label} source direction."}}
        return [translation(self.MARCH, "Historical"), translation(self.MAY, "Study")]

    def render(self, rows, formulary=None, *, kind="dialogue", context=None, **options):
        if formulary is not None:
            context = {"calendar": "roman-1962", "formulary": formulary}
        element = {"kind": kind, "name": "Preface of St Joseph", "speaker": "priest",
                   "translations": rows}
        return "\n".join(element_lines(element, "en", Style("unicode"),
                                      context=context, **options))

    def test_each_context_selects_its_own_body_and_note_in_either_order(self):
        rows = self.pair()
        original = deepcopy(rows)
        for ordered in (rows, rows[::-1]):
            for formulary, wanted, excluded in ((self.MARCH, "Historical", "Study"),
                                                (self.MAY, "Study", "Historical")):
                with self.subTest(order=ordered[0]["source_id"], formulary=formulary):
                    shown = self.render(ordered, formulary)
                    self.assertIn("Preface of St Joseph (priest)", shown)
                    self.assertIn(f"℣ — Priest: {wanted} source call.", shown)
                    self.assertIn(f"℟ — Server: {wanted} source answer.", shown)
                    self.assertIn(f"[ Source note: {wanted} source qualification. ]", shown)
                    self.assertNotIn(excluded, shown)
                    verbose = self.render(ordered, formulary, why=True)
                    self.assertIn(f"{wanted} full source evidence.", verbose)
                    self.assertNotIn(excluded, verbose)
        self.assertEqual(rows, original)

    def test_unknown_or_outside_context_exposes_no_candidate_words_or_notes(self):
        rows = self.pair()
        contexts = [(None, "unresolved"), ({}, "unresolved"),
                    ({"calendar": "roman-1962", "formulary": "unknown"}, "inapplicable"),
                    ({"calendar": "roman-pre-1955", "formulary": self.MAY}, "inapplicable")]
        for ordered in (rows, rows[::-1]):
            for context, status in contexts:
                for kind in ("prayer", "heading"):
                    with self.subTest(context=context, kind=kind):
                        shown = self.render(ordered, context=context, kind=kind, why=True)
                        self.assertIn("applicability " + status, shown)
                        self.assertNotIn("Historical", shown)
                        self.assertNotIn("Study", shown)
                        self.assertNotIn("Source note:", shown)

    def test_overlap_and_duplicate_unscoped_bodies_fail_closed(self):
        for kind in ("prayer", "heading"):
            for scoped in (True, False):
                rows = self.pair()
                if scoped:
                    rows[0]["applicability"]["formularies"].append(self.MAY)
                else:
                    for row in rows:
                        del row["applicability"]
                for ordered in (rows, rows[::-1]):
                    with self.subTest(kind=kind, scoped=scoped):
                        shown = self.render(ordered, self.MAY, kind=kind, why=True)
                        self.assertIn("applicability ambiguous", shown)
                        self.assertNotIn("Historical", shown)
                        self.assertNotIn("Study", shown)

    def test_an_unknown_competing_scope_does_not_lose_to_an_unscoped_row(self):
        rows = self.pair()
        del rows[0]["applicability"]
        for ordered in (rows, rows[::-1]):
            shown = self.render(ordered)
            self.assertIn("applicability unresolved", shown)
            self.assertNotIn("Historical", shown)
            self.assertNotIn("Study", shown)

    def test_a_malformed_competing_scope_is_not_ignored(self):
        rows = self.pair()
        rows[1]["applicability"]["formularies"] = []
        for ordered in (rows, rows[::-1]):
            with self.assertRaisesRegex(ValueError, "malformed Ordinary translation applicability"):
                self.render(ordered, self.MARCH)

    def test_heading_uses_the_selected_language_body_without_first_row_leaks(self):
        rows = self.pair()
        for ordered in (rows, rows[::-1]):
            shown = self.render(ordered, self.MAY, kind="heading")
            self.assertIn(rows[1]["text"].strip(), shown)
            self.assertIn("Study source qualification.", shown)
            self.assertNotIn("Historical", shown)

    def test_an_unscoped_single_body_preserves_the_existing_plain_layout(self):
        element = {"kind": "prayer", "name": "A prayer", "translations": [
            {"lang": "en", "text": "Literal source words."}]}
        self.assertEqual(element_lines(element, "en", Style("unicode")),
                         ["", "  A prayer", "    Literal source words."])


class OrdinarySourceActorLabels(unittest.TestCase):
    ACTORS = {"bishop": "Bishop", "communicant": "Communicant",
              "deacon-or-priest": "Deacon or priest", "lector": "Reader", "deacon": "Deacon"}

    def render(self, actor, turns, *, tier="unicode", **options):
        element = {"kind": "dialogue", "name": "A source exchange", "speaker": actor,
                   "translations": [{"lang": "en", "text": "\n".join(t["text"] for t in turns),
                                     "turns": turns}]}
        return "\n".join(element_lines(element, "en", Style(tier), **options))

    def test_source_actors_have_literal_labels_in_headers_and_turns(self):
        for actor, label in self.ACTORS.items():
            for tier in ("plain", "unicode", "rich"):
                with self.subTest(actor=actor, tier=tier):
                    shown = self.render(actor, [{"speaker": actor, "printed_marker": "R.",
                                                 "text": "R. Printed words."}], tier=tier)
                    self.assertIn(f"A source exchange ({label})", shown)
                    self.assertIn(f"{label}: Printed words.", shown)
                    self.assertNotIn("℟", shown)
                    self.assertNotIn("℣", shown)
                    if actor == "deacon-or-priest":
                        self.assertNotIn(actor, shown)

    def test_dialogue_roles_are_printed_only_when_explicit(self):
        for actor, label in self.ACTORS.items():
            for role, glyph in (("versicle", "℣"), ("response", "℟")):
                with self.subTest(actor=actor, role=role):
                    shown = self.render(actor, [{"speaker": actor, "dialogue_role": role,
                                                 "printed_marker": "P.", "text": "P. Source words."}])
                    self.assertIn(f"{glyph} — {label}: Source words.", shown)

    def test_actions_and_glosses_do_not_become_actors_or_dialogue(self):
        turns = [{"action": True, "text": "A source action."},
                 {"gloss": True, "text": "A source gloss."}]
        for actor, label in self.ACTORS.items():
            for rubrics in (True, False):
                with self.subTest(actor=actor, show_rubrics=rubrics):
                    shown = self.render(actor, turns, show_rubrics=rubrics)
                    self.assertEqual("[ A source action. ]" in shown, rubrics)
                    self.assertIn("[ Source translation: A source gloss. ]", shown)
                    self.assertNotIn(f"{label}: A source", shown)
                    self.assertNotIn("℟", shown)
                    self.assertNotIn("℣", shown)

    def test_unknown_actors_create_no_header_or_turn_cue(self):
        shown = self.render("unknown-actor", [{"speaker": "unknown-actor",
                                               "printed_marker": "R.", "text": "R. Source words."}])
        self.assertIn("A source exchange\n", shown)
        self.assertIn("R. Source words.", shown)
        self.assertNotIn("unknown-actor", shown)
        self.assertNotIn("℟", shown)

    def test_legacy_actor_headers_and_turn_labels_keep_their_existing_bytes(self):
        for actor, label in (("priest", "Priest"), ("server", "Server"), ("all", "All")):
            with self.subTest(actor=actor):
                shown = self.render(actor, [{"speaker": actor, "text": "Printed words."}])
                self.assertEqual(shown, f"\n  A source exchange ({actor})\n    {label}: Printed words.")


class SaintJosephSourceSelection(unittest.TestCase):
    """Exercise the actual registered English bodies through their owning builder."""
    MARCH = ScopedOrdinaryTranslations.MARCH
    MAY = ScopedOrdinaryTranslations.MAY

    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader(
            "ordinary_qualification_source_tool", str(ROOT / "tools/mass-ordinary"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        tool = importlib.util.module_from_spec(spec)
        loader.exec_module(tool)
        ordinary = tool.build(SimpleNamespace(root=ROOT / "src/sources",
                                              calendar="roman-1962"))[0]
        cls.preface = next(element for section in ordinary["sections"]
                           for element in section["elements"]
                           if element["key"] == "praefatio/praefatio-sancto-ioseph")

    @staticmethod
    def normalized(value):
        return " ".join(value.split())

    def render(self, element, context=None):
        return "\n".join(element_lines(element, "en", Style("unicode"), context=context))

    def test_actual_march_and_may_sources_select_independently_of_row_order(self):
        english = [row for row in self.preface["translations"] if row["lang"] == "en"]
        self.assertEqual(len(english), 2)
        self.assertEqual(len({row["source_id"] for row in english}), 2)
        for formulary in (self.MARCH, self.MAY):
            wanted = next(row for row in english
                          if row["applicability"]["formularies"] == [formulary])
            excluded = next(row for row in english if row is not wanted)
            outputs = []
            for reverse in (False, True):
                element = deepcopy(self.preface)
                if reverse:
                    element["translations"].reverse()
                shown = self.render(element, {"calendar": "roman-1962",
                                              "formulary": formulary})
                outputs.append(shown)
                with self.subTest(formulary=formulary, reverse=reverse):
                    self.assertTrue(shown.startswith("\n  Preface of St Joseph (priest)\n"))
                    flat = self.normalized(shown)
                    self.assertIn(self.normalized(wanted["text"]), flat)
                    self.assertIn(self.normalized(wanted["reading_note"]), flat)
                    self.assertNotIn(self.normalized(excluded["text"]), flat)
                    self.assertNotIn(self.normalized(excluded["reading_note"]), flat)
                    if wanted.get("note"):
                        self.assertNotIn(self.normalized(wanted["note"]), flat)
            self.assertEqual(outputs[0], outputs[1])

    def test_actual_sources_remain_closed_without_their_exact_formulary_context(self):
        for context, status in ((None, "unresolved"),
                                ({"calendar": "roman-1962", "formulary": "easter-sunday"},
                                 "inapplicable")):
            shown = self.render(self.preface, context)
            self.assertIn("applicability " + status, shown)
            for row in self.preface["translations"]:
                self.assertNotIn(self.normalized(row["text"]), self.normalized(shown))
                self.assertNotIn(self.normalized(row["reading_note"]), self.normalized(shown))

    def test_actual_overlapping_sources_expose_only_an_ambiguity(self):
        element = deepcopy(self.preface)
        for row in element["translations"]:
            row["applicability"]["formularies"] = [self.MARCH, self.MAY]
        shown = self.render(element, {"calendar": "roman-1962", "formulary": self.MAY})
        self.assertIn("applicability ambiguous", shown)
        for row in element["translations"]:
            self.assertNotIn(self.normalized(row["text"]), self.normalized(shown))
            self.assertNotIn(self.normalized(row["reading_note"]), self.normalized(shown))


class PostconciliarSourceActorLabels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader(
            "ordinary_qualification_actor_source_tool", str(ROOT / "tools/mass-ordinary"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        tool = importlib.util.module_from_spec(spec)
        loader.exec_module(tool)
        ordinary = tool.build(SimpleNamespace(root=ROOT / "src/sources",
                                              calendar="postconciliar"))[0]
        cls.invitation = next(element for section in ordinary["sections"]
                              for element in section["elements"]
                              if element["key"] == "ritus-communionis/offerte-vobis-pacem")

    def test_actual_peace_invitation_names_its_source_actor_without_inventing_a_role(self):
        self.assertEqual(self.invitation["speaker"], "deacon-or-priest")
        for language in ("en", "la"):
            row = next(row for row in self.invitation["translations"] if row["lang"] == language)
            self.assertEqual(len(row["turns"]), 1)
            self.assertEqual(row["turns"][0]["speaker"], "deacon-or-priest")
            self.assertIsNone(row["turns"][0]["dialogue_role"])
            shown = "\n".join(element_lines(self.invitation, language, Style("unicode")))
            flat = " ".join(shown.split())
            self.assertIn(self.invitation["name"] + " (Deacon or priest)", shown)
            self.assertIn("Deacon or priest: " + " ".join(row["text"].split()), flat)
            self.assertNotIn("deacon-or-priest", shown)
            self.assertNotIn("℣", shown)
            self.assertNotIn("℟", shown)


if __name__ == "__main__":
    unittest.main()
