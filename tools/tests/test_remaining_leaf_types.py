"""The last hand-written entrypoints that fit a document type are generated.

The two postconciliar calendar references sit on liturgy-reference-v1 and the
Low Mass flash cards on server-flash-cards-v1. Their rendered pages were proved
unchanged by scripts/render_compare.py when they moved; these checks keep the
declarations current and the flash-card entrypoint free of authored substance.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _document_types as types

CALENDAR = "liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/reference/liturgical-calendar"
FLASH_CARDS = "liturgy/roman-rite/1962/reference/altar-server-guides/01-low-mass-flash-cards"
LEAVES = {
    "gpt/" + CALENDAR: "liturgy-reference-v1",
    "claude/" + CALENDAR: "liturgy-reference-v1",
    "gpt/" + FLASH_CARDS: "server-flash-cards-v1",
}


class RemainingLeafTypeTests(unittest.TestCase):
    def test_each_leaf_declares_its_type_and_its_entrypoint_is_current(self):
        found = types.discover_types(ROOT)
        for name, type_id in LEAVES.items():
            with self.subTest(leaf=name):
                leaf = ROOT / "src" / name
                self.assertEqual(types.declaration(ROOT, leaf, found).type.id, type_id)
                [result] = types.refresh(ROOT, [leaf], check=True)
                self.assertEqual((result.changed, result.conflicts, result.orphans), ((), (), ()))

    def test_the_flash_card_type_is_one_canonical_deck_of_server_cards(self):
        found = types.discover_types(ROOT)["server-flash-cards-v1"]
        self.assertEqual(found.kinds, ("server-cards",))
        self.assertEqual(list(found.editions), ["main"])
        edition = found.editions["main"]
        self.assertEqual((edition.role, edition.entrypoint), ("canonical", "main.tex"))
        self.assertEqual(edition.regions, {"sheets": True})
        self.assertEqual(set(edition.fields), {"pdftitle", "pdfsubject"})

    def test_the_flash_card_entrypoint_holds_inputs_not_faces_or_commands(self):
        text = (ROOT / "src/gpt" / FLASH_CARDS / "main.tex").read_text(encoding="utf-8")
        for authored in ("\\newcommand", "\\newlength", "tikzpicture", "LowMassFrontCard",
                         "LowMassBackCard", "\\ServerLatinData"):
            with self.subTest(authored=authored):
                self.assertNotIn(authored, text)
        for relative in ("format", "generation-metadata", "sections/response-cards"):
            with self.subTest(input=relative):
                self.assertEqual(text.count("\\input{" + FLASH_CARDS + "/" + relative + "}"), 1)
        # The sheets come before the close the type owns: the last back sheet
        # prints the notice, then the companion's terminal sheet follows once.
        sheets = text.index("\\input{" + FLASH_CARDS + "/sections/response-cards}")
        self.assertLess(sheets, text.index("\\global\\TriptychRightsNoticeRenderedtrue"))
        self.assertEqual(text.count("\\CardCompanionTerminalApparatus"), 1)


if __name__ == "__main__":
    unittest.main()
