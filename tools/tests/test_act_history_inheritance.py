"""Ancestry-only edges cannot manufacture inherited liturgical text."""
import copy
import importlib.machinery
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


def load_tool():
    loader = importlib.machinery.SourceFileLoader("act_history_inheritance_test", str(ROOT / "tools/act-history"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class InheritanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool()
        cls.data = cls.tool.load(ROOT / "src/sources/inventories/latin-missal-acts-v1.toml")

    def test_real_use_continuity_never_carries_a_new_unit(self):
        data = copy.deepcopy(self.data)
        data["masses"].append({"id": "constructed", "at": "romanum-lugduni-1496", "title": "Constructed test", "day": "test", "hour": "test"})
        data["units"].append({"id": "constructed.collect", "at": "romanum-lugduni-1496", "mass": "constructed", "slot": "collect", "name": "Constructed test", "text": "Test text, not historical evidence.", "order": 1})
        _, states, _ = self.tool.build(data)
        self.assertIn("constructed.collect", states["romanum-lugduni-1496"].units)
        for identifier in ("romanum-venetiis-1501", "romanae-ecclesiae-parisiis-1516", "romanum-venetiis-1561"):
            self.assertNotIn("constructed.collect", states[identifier].units)
        note = "unestablished/text-inheritance-romanum-venetiis-1501.txt"
        self.assertIn(note, states["romanum-venetiis-1501"].files)
        self.assertFalse(self.tool.is_liturgy(note))
        parent = next(act for act in data["acts"] if act["id"] == "romanum-lugduni-1496")
        self.assertIn(self.tool.act_file(parent), states["romanum-venetiis-1501"].files)

    def test_printing_requires_explicit_scope_and_basis(self):
        act = {"id": "print", "station_kind": "printed", "parents": ["earlier"], "parent_kind": "book-states-it"}
        self.assertEqual([], self.tool.text_parents(act))
        act["text_inheritance"] = {"parents": ["earlier"], "scope": "recorded-units", "basis": "Constructed exact unit collation evidence."}
        self.assertEqual(["earlier"], self.tool.text_parents(act))
        del act["text_inheritance"]["basis"]
        with self.assertRaisesRegex(self.tool.Problem, "scope and evidence basis"):
            self.tool.text_parents(act)

    def test_use_continuity_cannot_be_upgraded_by_an_inheritance_flag(self):
        act = {"id": "print", "parents": ["earlier"], "parent_kind": "use-continuity",
               "text_inheritance": {"parents": ["earlier"], "scope": "recorded-units", "basis": "test"}}
        with self.assertRaisesRegex(self.tool.Problem, "cannot authorize"):
            self.tool.text_parents(act)

    def test_merge_base_does_not_cross_an_ancestry_only_edge(self):
        vocab = self.tool.vocabulary_of(self.data)
        acts = {"root": {"parents": [], "date": "1500"},
                "left": {"parents": ["root"], "parent_kind": "use-continuity", "date": "1501"},
                "right": {"parents": ["root"], "parent_kind": "act-states-it", "date": "1502"}}
        states = {key: self.tool.State(vocab) for key in acts}
        states["root"].units["must-not-be-the-base"] = {"text": "test"}
        self.assertEqual({}, self.tool.common_ancestor(["left", "right"], acts, states, vocab).units)

    def test_effect_flag_alone_does_not_remove_a_promulgated_chain(self):
        _, states, _ = self.tool.build(self.data)
        self.assertEqual(38, len(states["editio-typica-1920"].units))
        self.assertEqual(20, len(states["reimpressio-emendata-2008"].units))
        self.assertEqual(31, len(states["rescriptum-traditionis-custodes-2023"].units))

    def test_reception_cannot_be_selected_for_text_carry(self):
        act = {"id": "receiving", "parents": ["own", "foreign"], "receptions": [{"from": "foreign"}],
               "text_inheritance": {"parents": ["foreign"], "scope": "recorded-units", "basis": "test"}}
        with self.assertRaisesRegex(self.tool.Problem, "own-line parents"):
            self.tool.text_parents(act)
        del act["text_inheritance"]
        self.assertEqual(["own"], self.tool.text_parents(act))


if __name__ == "__main__":
    unittest.main()
