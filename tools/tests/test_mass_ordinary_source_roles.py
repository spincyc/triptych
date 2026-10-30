"""Source-explicit actors preserve individual and pontifical utterances."""
from copy import deepcopy
import importlib.machinery
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


class OrdinarySourceActors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader(
            "ordinary_source_actors", str(ROOT / "tools/mass-ordinary"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.tool = importlib.util.module_from_spec(spec)
        loader.exec_module(cls.tool)

    def resolve(self, declarations, texts=None):
        texts = texts or ["Source words."]
        rows = [{"seq": str(index), "element_key": "body", "english": text}
                for index, text in enumerate(texts, 1)]
        with patch.object(self.tool, "payload_rows", return_value=rows):
            return self.tool.structured_turns(
                {"english_turns": declarations}, "english", {"source": {}},
                "source", ["body"], "english", "synthetic/body", "synthetic",
                "\n".join(texts))

    def test_only_the_finite_source_roles_are_added(self):
        self.assertEqual(self.tool.TURN_SPEAKERS,
                         ("all", "priest", "server", "bishop", "communicant",
                          "deacon-or-priest", "lector", "deacon"))
        for actor in self.tool.TURN_SPEAKERS:
            declared = [{"key": "source-utterance", "seq": [1], "speaker": actor}]
            before = deepcopy(declared)
            turn = self.resolve(declared)[0]
            self.assertEqual(declared, before)
            self.assertEqual(turn["speaker"], actor)
            self.assertIsNone(turn["dialogue_role"])
            self.assertEqual(turn["text"], "Source words.")

    def test_communion_response_belongs_to_one_communicant(self):
        turns = self.resolve([
            {"key": "minister", "seq": [1], "speaker": "deacon-or-priest"},
            {"key": "recipient", "seq": [2], "speaker": "communicant"},
        ], ["The Body of Christ.", "Amen."])
        self.assertEqual([row["speaker"] for row in turns],
                         ["deacon-or-priest", "communicant"])
        self.assertEqual("\n".join(row["text"] for row in turns),
                         "The Body of Christ.\nAmen.")
        self.assertTrue(all(row["dialogue_role"] is None for row in turns))

    def test_missing_actor_remains_unspecified(self):
        turn = self.resolve([{"key": "unassigned", "seq": [1]}])[0]
        self.assertIsNone(turn["speaker"])
        self.assertIsNone(turn["dialogue_role"])

    def test_unknown_or_broader_actor_names_are_refused(self):
        for actor in ("minister", "congregation", "recipient", "Bishop", "reader"):
            with self.subTest(actor=actor), self.assertRaisesRegex(
                    self.tool.SourceError, "has speaker"):
                self.resolve([{"key": "unproved", "seq": [1], "speaker": actor}])

    def test_gospel_book_conditions_are_closed_and_unknown_without_reading_context(self):
        expected = {"gospel-book-matthew", "gospel-book-mark",
                    "gospel-book-luke", "gospel-book-john"}
        self.assertEqual({value for value in self.tool.CONDITION_PREDICATES
                          if value.startswith("gospel-book-")}, expected)
        for predicate in expected:
            entry = {"conditions": [{"kind": "include-when-any",
                        "predicates": [predicate], "basis": "Source-owned named heading."}]}
            conditions = self.tool.element_conditions(entry, {}, "synthetic/gospel", "synthetic")
            self.assertEqual(conditions, [entry["conditions"][0] | {"unknown": "unresolved"}])
            self.assertEqual(self.tool.element_applicability(
                {"key": "synthetic/gospel", "conditions": conditions}, {}),
                (False, conditions))
        with self.assertRaisesRegex(self.tool.SourceError, "closed predicate table"):
            self.tool.element_conditions({"conditions": [{"kind": "include-when-any",
                "predicates": ["gospel-book-inferred"], "basis": "Unproved."}]},
                {}, "synthetic/gospel", "synthetic")

    def test_new_actors_cannot_turn_an_action_into_spoken_text(self):
        for actor in ("bishop", "communicant", "deacon-or-priest", "lector", "deacon"):
            with self.subTest(actor=actor), self.assertRaisesRegex(
                    self.tool.SourceError, "both an action and a spoken turn"):
                self.resolve([{"key": "action", "seq": [1], "speaker": actor,
                               "action": True}])


if __name__ == "__main__":
    unittest.main()
